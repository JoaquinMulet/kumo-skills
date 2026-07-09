#!/usr/bin/env python3
"""Gate de kumo-skills: valida el frontmatter de cada SKILL.md ANTES del commit.

Existe porque la disciplina manual no sostiene los checks. Dos veces mordio:
  1. Se pusheo una description de 1086 chars (sobre 1024) por medir DESPUES de commitear.
  2. Se aprobo una description con ': ' sin comillas que el cargador YAML real rechazo
     ("mapping values are not allowed in this context"): el gate raspaba el YAML con regex
     en vez de parsearlo, y esa regex compartia el punto ciego del que la escribio.

La leccion (universal, vive en `desarrollo-riguroso`): un validador que APROXIMA el sistema
real comparte tu punto ciego. Este gate INVOCA un parser YAML de verdad (el mismo tipo de
parseo que hace el cargador de skills) y valida tipos/valores sobre el objeto resultante,
en vez de sobre un texto raspado. Cae a checks manuales endurecidos solo si no hay YAML.

Chequea, por cada <carpeta>/SKILL.md:
  - frontmatter = YAML VALIDO (parseado, no raspado)
  - name: string, == carpeta, [a-z0-9-]{1,64}, sin 'anthropic'/'claude'
  - description: string, no vacia, <= 1024 chars (sobre el valor YA parseado)
  - SKILL.md <= 500 lineas
  - sin voseo (regla dura de idioma)
Sale != 0 si algo falla.

Ejecucion recomendada (parser YAML real, sin ensuciar el sistema):
    uv run --with pyyaml python scripts/validar-skills.py
El pre-commit hook la corre asi. Sin 'uv'/'yaml' cae a un parser manual endurecido que
cubre las clases criticas (tab, ': ' sin comillas, comillas sin balancear, clave duplicada,
valor que roba la linea siguiente, '...', indicadores de flujo). Para probar el fallback a
proposito: KUMO_GATE_FORCE_MANUAL=1 python scripts/validar-skills.py
"""
import re
import sys
import glob
import os

VOSEO = re.compile(
    r"\b(revisá|avisá|poné|andá|tenés|querés|elegí|quitá|guardá|mirá|hacé|podés|"
    r"entendés|usá|escribí|corré|vení|salí|sabés|dejá|mandá|probá|decime|fijate|"
    r"acordate|quedate|llevate|ponete|hacete)\b",
    re.I,
)
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
BLOCK_INDICATORS = (">", ">-", ">+", "|", "|-", "|+")
# chars que, al inicio de un scalar plano SIN comillas, cambian el sentido para YAML
FLOW_START = set("[]{}!&*@`%#")


def read_normalized(path):
    """Lee, quita BOM y normaliza CRLF -> LF para no divergir del loader."""
    text = open(path, encoding="utf-8").read()
    return text.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")


def extract_block(text):
    """Bloque de frontmatter entre los primeros dos '---', o None."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else None


def precheck_block(block):
    """Checks deterministas que corren SIEMPRE (con o sin YAML). Devuelve error|None."""
    if "\t" in block:
        return "tab dentro del frontmatter (YAML prohibe tabs)"
    for key in ("name", "description"):
        if len(re.findall(rf"^{key}:", block, re.M)) > 1:
            return f"clave '{key}' duplicada (el loader se queda con la ultima, el gate veia la primera)"
    if re.search(r"^\.\.\.\s*$", block, re.M):
        return "marcador de fin de documento '...' dentro del frontmatter"
    return None


def validate_with_yaml(block):
    """Parseo REAL con PyYAML. Devuelve (dict|None, error|None)."""
    import yaml
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as e:
        return None, "YAML invalido: " + str(e).replace("\n", " ")
    if not isinstance(data, dict):
        return None, "el frontmatter no es un mapping YAML"
    return data, None


def validate_manual(block):
    """Fallback sin PyYAML. Reconstruye los valores en la MISMA linea (no cruza el \\n,
    que era el peor bug del gate viejo) y rechaza lo que el loader real rechaza."""
    data = {}
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "" or line.startswith(" "):
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):(.*)$", line)
        if not m:
            i += 1
            continue
        key, v = m.group(1), m.group(2).strip()
        if v == "" or v in BLOCK_INDICATORS:
            # block scalar (o vacio): juntar continuaciones indentadas como texto literal
            cont, j = [], i + 1
            while j < len(lines) and (lines[j].strip() == "" or lines[j].startswith(" ")):
                cont.append(lines[j].strip())
                j += 1
            data[key] = " ".join(x for x in cont if x).strip()
            i = j
            continue
        if v[0] in ("\"", "'"):
            q = v[0]
            if not (len(v) >= 2 and v.endswith(q)):
                return None, f"comillas sin balancear en '{key}'"
            data[key] = v[1:-1]
        else:
            if v[0] in FLOW_START:
                return None, f"'{key}' arranca con indicador YAML '{v[0]}' sin comillas"
            if ": " in v or v.endswith(":"):
                return None, f"'{key}' tiene ': ' sin comillas (YAML lo lee como mapping)"
            if " #" in v:
                return None, f"'{key}' tiene ' #' sin comillas (YAML lo lee como comentario)"
            data[key] = v
        i += 1
    return data, None


def check_skill(skill_md, yaml_ok):
    folder = os.path.basename(os.path.dirname(skill_md))
    where = f"{folder}/SKILL.md"
    text = read_normalized(skill_md)
    block = extract_block(text)
    if block is None:
        return [f"{where}: sin frontmatter valido (--- ... ---)"]
    pre = precheck_block(block)
    if pre:
        return [f"{where}: {pre}"]
    data, err = validate_with_yaml(block) if yaml_ok else validate_manual(block)
    if err:
        return [f"{where}: {err}"]

    errs = []
    name, desc = data.get("name"), data.get("description")
    if not isinstance(name, str):
        errs.append(f"{where}: name no es string (YAML lo tipo como {type(name).__name__}) — encierralo en comillas")
        name = ""
    if desc is not None and not isinstance(desc, str):
        errs.append(f"{where}: description no es string (YAML lo tipo como {type(desc).__name__}) — encierrala en comillas")
        desc = None
    desc = desc or ""

    if name != folder:
        errs.append(f'{where}: name "{name}" != carpeta "{folder}"')
    if not NAME_RE.match(name):
        errs.append(f'{where}: name "{name}" mal formado (minusculas/numeros/guiones, <=64)')
    if "anthropic" in name or "claude" in name:
        errs.append(f"{where}: name no puede contener 'anthropic' ni 'claude'")
    if not desc:
        errs.append(f"{where}: description vacia")
    elif len(desc) > 1024:
        errs.append(f"{where}: description {len(desc)} chars > 1024")
    nlines = text.count("\n") + 1
    if nlines > 500:
        errs.append(f"{where}: SKILL.md {nlines} lineas > 500")
    if VOSEO.search(text):
        vs = sorted({v.lower() for v in VOSEO.findall(text)})
        errs.append(f"{where}: voseo detectado ({', '.join(vs[:5])})")
    return errs


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills = sorted(glob.glob(os.path.join(root, "*", "SKILL.md")))
    yaml_ok = True
    if os.environ.get("KUMO_GATE_FORCE_MANUAL"):
        yaml_ok = False
    else:
        try:
            import yaml  # noqa: F401
        except ImportError:
            yaml_ok = False
    if not yaml_ok and not os.environ.get("KUMO_GATE_FORCE_MANUAL"):
        print("nota: PyYAML no disponible — checks manuales. Para parseo YAML real: "
              "uv run --with pyyaml python scripts/validar-skills.py", file=sys.stderr)

    errors = []
    for skill_md in skills:
        errors.extend(check_skill(skill_md, yaml_ok))
    if errors:
        print(f"GATE kumo-skills — FALLO ({len(errors)}):", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print(f"GATE kumo-skills — OK ({len(skills)} skills validas, parseo {'YAML real' if yaml_ok else 'manual'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
