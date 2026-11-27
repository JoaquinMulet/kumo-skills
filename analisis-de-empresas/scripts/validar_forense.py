"""Valida el anexo de la revisión forense y calcula su puntaje.

Qué espera. La ruta del anexo en Markdown. El anexo trae 15 secciones, una por prueba, cada una con
un título de nivel 2 que empieza con su código (EM 1 a EM 7, CF 1 a CF 3, KM 1, KM 2, AA 1 a AA 3)
y una tabla de 2 columnas con estas filas.

  | Veredicto | LIMPIO, BAJA, MEDIA, ALTA, CRÍTICA o SIN DATO |
  | Qué se revisó | la cifra, la nota o la página que se miró |
  | Efecto | cuánto mueve la utilidad, el flujo o el patrimonio (solo en un hallazgo) |
  | Cita | «texto exacto de la fuente» en ruta/del/archivo (una fila por cita) |
  | Qué falta | lo que hay que conseguir (solo con SIN DATO) |

Qué comprueba. Que estén las 15 pruebas. Que cada veredicto exista. Que un LIMPIO diga qué cifra o
nota miró. Que un hallazgo (BAJA, MEDIA, ALTA o CRÍTICA) traiga su efecto y al menos una cita, y
que cada cita aparezca en el archivo de la fuente. Una cita se busca sin mayúsculas y juntando los
espacios, igual que en `buscar_en_fuente.py`. La ruta de una cita se busca desde la carpeta
del anexo y desde la que la contiene (la carpeta de trabajo), o solo desde la que diga --fuentes.

Qué devuelve. El puntaje, que suma 1 punto por BAJA, 2 por MEDIA, 3 por ALTA y 4 por CRÍTICA, y su
tramo. La escala es una convención de Kumo. El libro de Schilit no da ninguna. Sale con 0 si el
anexo está completo, con 1 si tiene huecos y con 2 si el uso o el archivo están mal.

Uso.
  uv run python -I scripts/validar_forense.py analisis/anexo-forense.md
  uv run --with pymupdf python -I scripts/validar_forense.py analisis/anexo-forense.md --fuentes fuente
"""

import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from buscar_en_fuente import buscar, leer_partes

CODIGOS = ["EM 1", "EM 2", "EM 3", "EM 4", "EM 5", "EM 6", "EM 7", "CF 1", "CF 2", "CF 3", "KM 1", "KM 2", "AA 1", "AA 2", "AA 3"]
PUNTOS = {"LIMPIO": 0, "BAJA": 1, "MEDIA": 2, "ALTA": 3, "CRITICA": 4}
SIN_DATO = "SIN DATO"
TRAMOS = [(3, "Limpio"), (7, "Dudas"), (12, "Dudas importantes")]
TRAMO_MAYOR = "Manipulación seria"
TITULO = re.compile(r"^##[ \t]+((?:EM|CF|KM|AA)[ \t-]?\d)\b.*$", re.M)
FILA = re.compile(r"^\|[ \t]*([^|]+?)[ \t]*\|[ \t]*(.*?)[ \t]*\|[ \t]*$", re.M)
CITA = re.compile(r"^«(.+)»[ \t]+en[ \t]+(\S.*)$")
EVIDENCIA_DE_REVISION = re.compile(r"\d|\bnota\b|\bpágina\b|\bpagina\b", re.I)


def sin_tildes(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def partir(texto):
    marcas = list(TITULO.finditer(texto))
    secciones = {}
    for k, m in enumerate(marcas):
        codigo = re.sub(r"[ \t-]?(\d)", r" \1", m.group(1))
        fin = marcas[k + 1].start() if k + 1 < len(marcas) else len(texto)
        secciones.setdefault(codigo, texto[m.end():fin])
    return secciones


def filas(cuerpo):
    salida = {}
    for m in FILA.finditer(cuerpo):
        campo = sin_tildes(m.group(1)).casefold()
        if set(m.group(1)) <= set("-: "):
            continue
        salida.setdefault(campo, []).append(m.group(2))
    return salida


def revisar(codigo, cuerpo, carpetas, cache):
    f = filas(cuerpo)
    veredicto_crudo = (f.get("veredicto") or [""])[0].strip()
    veredicto = sin_tildes(veredicto_crudo).upper()
    if not veredicto:
        return None, [f"{codigo}. Falta la fila Veredicto."]
    if veredicto == SIN_DATO:
        if not any(v.strip() for v in f.get("que falta", [])):
            return SIN_DATO, [f"{codigo}. Dice SIN DATO y no trae la fila «Qué falta»."]
        return SIN_DATO, []
    if veredicto not in PUNTOS:
        return None, [f"{codigo}. El veredicto «{veredicto_crudo}» no existe. Usa LIMPIO, BAJA, MEDIA, ALTA, CRÍTICA o SIN DATO."]
    problemas = []
    revisado = " ".join(f.get("que se reviso", []))
    if not EVIDENCIA_DE_REVISION.search(revisado):
        problemas.append(f"{codigo}. «Qué se revisó» no nombra ninguna cifra, nota ni página.")
    if PUNTOS[veredicto] == 0:
        return veredicto, problemas
    if not any(v.strip() for v in f.get("efecto", [])):
        problemas.append(f"{codigo}. Es un hallazgo y le falta la fila Efecto.")
    citas = f.get("cita", [])
    if not citas:
        problemas.append(f"{codigo}. Es un hallazgo y no trae ninguna cita de la fuente.")
    for cita in citas:
        m = CITA.match(cita.strip())
        if not m:
            problemas.append(f"{codigo}. La cita no tiene la forma «texto» en ruta. Dice: {cita[:80]}")
            continue
        texto, escrita = m.group(1), m.group(2).strip()
        ruta = next((base / escrita for base in carpetas if (base / escrita).is_file()), None)
        if ruta is None:
            donde = ", ".join(str(base) for base in carpetas)
            problemas.append(f"{codigo}. No existe el archivo de la cita, {escrita}. Lo busqué en {donde}.")
            continue
        if ruta not in cache:
            cache[ruta] = leer_partes(ruta)
        if not buscar(cache[ruta], texto, False, False):
            problemas.append(f"{codigo}. La cita no aparece en {ruta.name}. Dice: «{texto[:90]}»")
    return veredicto, problemas


def tramo(puntos):
    for tope, nombre in TRAMOS:
        if puntos <= tope:
            return nombre
    return TRAMO_MAYOR


def main(argv):
    for flujo in (sys.stdout, sys.stderr):
        flujo.reconfigure(encoding="utf-8", errors="replace")
    args = argv[1:]
    carpeta_fuentes = None
    if "--fuentes" in args:
        k = args.index("--fuentes")
        if k + 1 >= len(args):
            print("A --fuentes le falta la carpeta.", file=sys.stderr)
            return 2
        carpeta_fuentes = Path(args[k + 1])
        del args[k:k + 2]
    if len(args) != 1 or args[0].startswith("--"):
        print(__doc__, file=sys.stderr)
        return 2
    ruta = Path(args[0])
    if not ruta.is_file():
        print(f"No existe {ruta}.", file=sys.stderr)
        return 2
    # El anexo vive en analisis/ y las fuentes en fuente/, las 2 dentro de la carpeta de trabajo.
    # Por eso una cita «en fuente/actual.txt» se busca también desde la carpeta que contiene a la del anexo.
    carpetas = [carpeta_fuentes] if carpeta_fuentes else [ruta.resolve().parent, ruta.resolve().parent.parent]
    secciones = partir(ruta.read_bytes().decode("utf-8-sig"))

    problemas, veredictos, cache = [], {}, {}
    for codigo in CODIGOS:
        if codigo not in secciones:
            problemas.append(f"{codigo}. Falta la sección.")
            continue
        veredicto, lios = revisar(codigo, secciones[codigo], carpetas, cache)
        veredictos[codigo] = veredicto
        problemas.extend(lios)

    hallazgos = {c: v for c, v in veredictos.items() if v in PUNTOS and PUNTOS[v] > 0}
    sin_dato = [c for c, v in veredictos.items() if v == SIN_DATO]
    puntos = sum(PUNTOS[v] for v in hallazgos.values())
    criticos = [c for c, v in hallazgos.items() if v == "CRITICA"]
    print(f"Leí {ruta}. Encontré {len(secciones.keys() & set(CODIGOS))} de {len(CODIGOS)} pruebas.")
    for codigo, veredicto in hallazgos.items():
        print(f"  {codigo}. {veredicto}")
    print(f"Puntaje de {puntos} puntos, tramo «{tramo(puntos)}». {len(hallazgos)} hallazgos y {len(sin_dato)} sin dato.")
    if sin_dato:
        print(f"  Sin dato en {', '.join(sin_dato)}. El puntaje no las cuenta, y el informe tiene que decirlo.")
    if criticos:
        print(f"  Hay un hallazgo crítico en {', '.join(criticos)}. Con un crítico no se invierte, sume lo que sume el puntaje.")
    if problemas:
        for lio in problemas:
            print("  " + lio)
        print("ROJO. El anexo tiene huecos.")
        return 1
    print("VERDE. Las 15 pruebas tienen veredicto, y cada hallazgo tiene su cita en la fuente.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
