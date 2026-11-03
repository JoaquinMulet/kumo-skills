"""Comprueba en el archivo de una fuente primaria que una cita existe, o cuenta un término.

Qué espera. La ruta de un archivo ya bajado al disco (.txt, .md, .html, .htm, .xml o .pdf) y una o
más consultas.

Qué devuelve. Por cada consulta, si aparece y dónde (página en un PDF, línea en el resto), con un
trozo del texto alrededor. Sale con 0 si todas las citas aparecen, 1 si alguna falta, 2 si el uso o
el archivo están mal.

Uso.
  uv run --with pymupdf python -I scripts/buscar_en_fuente.py fuente.pdf --cita "texto exacto"
  uv run python -I scripts/buscar_en_fuente.py memoria.txt --contar ROIC --contar "capital empleado"
  Agrega --sin-acentos para que «séptimo» y «septimo» cuenten igual.

Por qué normaliza antes de buscar. Las 3 veces que una búsqueda dio cero y parecía una ausencia, el
texto sí estaba. Un XML de leychile escribe «séptimo» como entidad HTML, y el texto de un PDF trae
saltos de línea dentro de las frases. Por eso el script decodifica las entidades, junta los
espacios y compara sin mayúsculas. En --contar busca con bordes de palabra, porque «roce» está
dentro de «proceso» y «eva» dentro de «eleva».

Un cero en --contar no prueba que el término no exista. Prueba que no está escrito así. Antes de
publicar una ausencia, corre una 2.ª formulación.
"""

import html
import re
import sys
import unicodedata
from pathlib import Path

CONTEXTO = 60  # caracteres que se muestran a cada lado de la coincidencia
MAXIMO = 5  # coincidencias que se muestran por consulta, el total se cuenta igual


def normalizar(texto, sin_acentos):
    texto = " ".join(html.unescape(texto).split()).casefold()
    if sin_acentos:
        texto = "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")
    return texto


def leer_partes(ruta):
    """Devuelve una lista de (rótulo, texto). En un PDF una parte por página, en el resto una por línea."""
    if ruta.suffix.lower() == ".pdf":
        try:
            import pymupdf
        except ImportError:
            print("Para leer un PDF corre el script con: uv run --with pymupdf python -I ...", file=sys.stderr)
            sys.exit(2)
        with pymupdf.open(ruta) as doc:
            return [(f"página {i + 1}", pagina.get_text()) for i, pagina in enumerate(doc)]
    texto = ruta.read_bytes().decode("utf-8-sig", errors="replace")
    if ruta.suffix.lower() in (".html", ".htm", ".xml"):
        texto = re.sub(r"<[^>]+>", " ", texto)
    return [("todo el archivo", texto)]


def buscar(partes, consulta, sin_acentos, contar):
    q = normalizar(consulta, sin_acentos)
    if contar:
        patron = re.compile(r"(?<!\w)" + re.escape(q) + r"(?!\w)")
    else:
        patron = re.compile(re.escape(q))
    hallazgos = []
    for rotulo, texto in partes:
        plano = normalizar(texto, sin_acentos)
        for m in patron.finditer(plano):
            ini, fin = max(0, m.start() - CONTEXTO), min(len(plano), m.end() + CONTEXTO)
            hallazgos.append((rotulo, plano[ini:fin]))
    return hallazgos


def main(argv):
    # La consola de Windows no usa UTF-8 por defecto y muestra los acentos rotos.
    for flujo in (sys.stdout, sys.stderr):
        flujo.reconfigure(encoding="utf-8", errors="replace")
    if len(argv) < 3 or argv[1].startswith("--"):
        print(__doc__, file=sys.stderr)
        return 2
    ruta = Path(argv[1])
    if not ruta.is_file():
        print(f"No existe el archivo {ruta}. Baja primero la fuente al disco.", file=sys.stderr)
        return 2
    sin_acentos = "--sin-acentos" in argv
    consultas, i = [], 2
    while i < len(argv):
        if argv[i] in ("--cita", "--contar") and i + 1 < len(argv):
            consultas.append((argv[i], argv[i + 1]))
            i += 2
        elif argv[i] == "--sin-acentos":
            i += 1
        else:
            print(f"No entiendo «{argv[i]}». Usa --cita, --contar o --sin-acentos.", file=sys.stderr)
            return 2
    if not consultas:
        print("Falta al menos una --cita o un --contar.", file=sys.stderr)
        return 2

    partes = leer_partes(ruta)
    total_caracteres = sum(len(t) for _, t in partes)
    print(f"Leí {ruta} ({len(partes)} partes, {total_caracteres} caracteres).")
    if total_caracteres == 0:
        print("El archivo no tiene texto. Un PDF escaneado necesita OCR antes de buscar.", file=sys.stderr)
        return 2

    falta_cita = False
    for modo, consulta in consultas:
        hallazgos = buscar(partes, consulta, sin_acentos, modo == "--contar")
        if modo == "--cita":
            estado = "APARECE" if hallazgos else "NO APARECE"
            falta_cita = falta_cita or not hallazgos
        else:
            estado = f"{len(hallazgos)} veces"
        print(f"\n{modo[2:]} «{consulta}». {estado}")
        for rotulo, trozo in hallazgos[:MAXIMO]:
            print(f"  {rotulo}. …{trozo}…")
        if len(hallazgos) > MAXIMO:
            print(f"  y {len(hallazgos) - MAXIMO} más")
    return 1 if falta_cita else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
