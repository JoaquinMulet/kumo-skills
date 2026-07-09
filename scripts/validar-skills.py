#!/usr/bin/env python3
"""Gate de kumo-skills: valida el frontmatter de cada SKILL.md ANTES del commit.

Existe porque la disciplina manual no sostiene los checks — este repo pusheó una vez una
description de 1086 chars (sobre el límite de 1024) porque se midió DESPUÉS de commitear.
Un gate lo hace cumplir, no la memoria. Lo corre el pre-commit hook (.githooks/pre-commit).

Chequea, por cada <carpeta>/SKILL.md: name == carpeta, name bien formado (minúsculas/
números/guiones, <=64, sin anthropic/claude), description no vacía y <=1024 chars,
SKILL.md <=500 líneas, y sin voseo (regla dura de idioma). Sale != 0 si algo falla.

Sin dependencias externas (parsea el frontmatter a mano) para que el hook sea rápido y fiable.
Uso: python scripts/validar-skills.py
"""
import re
import sys
import glob
import os

# Solo formas voseo INEQUÍVOCAS (acento en la última sílaba, o imperativo sin
# cambio de raíz): "hacé"/"mirá"/"usá" (voseo) — NO "hace"/"mira"/"usa" (correcto).
# Evitar `[aá]`/`[eé]` que matchea la forma estándar y genera falsos positivos.
VOSEO = re.compile(
    r"\b(revisá|avisá|poné|andá|tenés|querés|elegí|quitá|guardá|mirá|hacé|podés|"
    r"entendés|usá|escribí|corré|vení|salí|sabés|dejá|mandá|probá|decime|fijate|"
    r"acordate|quedate|llevate|ponete|hacete)\b",
    re.I,
)
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def parse_frontmatter(text):
    """Extrae name y description del bloque YAML entre los primeros dos '---'.
    Soporta description en una línea (plain) o en bloque folded ('>-')."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None
    fm = m.group(1)
    out = {}
    nm = re.search(r"^name:\s*(.+)$", fm, re.M)
    if nm:
        out["name"] = nm.group(1).strip().strip("\"'")
    dm = re.search(r"^description:\s*(.*)$", fm, re.M)
    if dm:
        first = dm.group(1).strip()
        if first in (">-", ">", "|", "|-", "|+", ">+", ""):
            # bloque folded: juntar las líneas siguientes indentadas
            cont = []
            for ln in fm[dm.end():].split("\n"):
                if ln.strip() == "" or ln.startswith(" "):
                    cont.append(ln.strip())
                else:
                    break
            out["description"] = " ".join(x for x in cont if x).strip()
        else:
            out["description"] = first.strip("\"'")
    return out


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills = sorted(glob.glob(os.path.join(root, "*", "SKILL.md")))
    errors = []
    for skill_md in skills:
        folder = os.path.basename(os.path.dirname(skill_md))
        text = open(skill_md, encoding="utf-8").read()
        where = f"{folder}/SKILL.md"
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{where}: sin frontmatter válido (--- ... ---)")
            continue
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if name != folder:
            errors.append(f'{where}: name "{name}" != carpeta "{folder}"')
        if not NAME_RE.match(name):
            errors.append(f'{where}: name "{name}" mal formado (minúsculas/números/guiones, <=64)')
        if "anthropic" in name or "claude" in name:
            errors.append(f"{where}: name no puede contener 'anthropic' ni 'claude'")
        if not desc:
            errors.append(f"{where}: description vacía")
        elif len(desc) > 1024:
            errors.append(f"{where}: description {len(desc)} chars > 1024")
        nlines = text.count("\n") + 1
        if nlines > 500:
            errors.append(f"{where}: SKILL.md {nlines} líneas > 500")
        vs = sorted({v.lower() for v in VOSEO.findall(text)})
        if vs:
            errors.append(f"{where}: voseo detectado ({', '.join(vs[:5])})")

    if errors:
        print(f"GATE kumo-skills — FALLO ({len(errors)}):", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print(f"GATE kumo-skills — OK ({len(skills)} skills válidas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
