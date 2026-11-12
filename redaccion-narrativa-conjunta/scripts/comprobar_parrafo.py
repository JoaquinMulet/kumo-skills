"""Comprueba un borrador en Markdown antes de mostrárselo al autor.

Hace 2 cosas.
1. Busca cada cita entre comillas angulares («...») de las notas al pie del borrador en el texto de
   las fuentes. Una cita con «[...]» se parte en trozos y se busca cada trozo. Los espacios, los
   saltos de línea y los apóstrofos curvos se normalizan antes de buscar.
2. Revisa la prosa (todo lo que no es nota al pie, título ni referencia) contra las reglas de la casa.
   Marca los dos puntos usados como conector, las rayas, las frases que abren negando («No es…») y
   las frases de índice que mandan al lector a otra parte del texto.

Uso:
    uv run --with pymupdf python scripts/comprobar_parrafo.py BORRADOR.md FUENTE [FUENTE ...]

Las fuentes pueden ser .pdf, .txt, .md o .html (el html se lee como texto plano, sin etiquetas).
Sale con código 0 si todo pasa y con código 1 si algo falla, e imprime qué falló y dónde.
"""

import html
import re
import sys
from pathlib import Path

FRASES_DE_INDICE = (
    "más adelante",
    "como veremos",
    "en la sección siguiente",
    "en el capítulo siguiente",
    "la sección siguiente",
    "se ocupa de ellas en el orden",
    "como se explicará",
)
DOS_PUNTOS_CONECTOR = re.compile(r"[a-záéíóúñ»\)]: [a-záéíóúñ«]")
NOTA = re.compile(r"^\[\^[^\]]+\]:\s*(.*)$")
CITA = re.compile(r"«([^»]+)»")


def normalizar(texto: str) -> str:
    texto = texto.replace("’", "'").replace("‘", "'").replace("­", "")
    texto = texto.replace("ﬁ", "fi").replace("ﬂ", "fl")
    return " ".join(texto.split())


def leer_fuente(ruta: Path) -> str:
    if ruta.suffix.lower() == ".pdf":
        try:
            import pymupdf
        except ImportError:
            print(
                "Falta pymupdf. Corre el script con: uv run --with pymupdf python ..."
            )
            sys.exit(2)
        with pymupdf.open(ruta) as documento:
            return " ".join(pagina.get_text() for pagina in documento)
    texto = ruta.read_bytes().decode("utf-8", errors="replace")
    if ruta.suffix.lower() in (".html", ".htm"):
        texto = html.unescape(re.sub(r"<[^>]+>", " ", texto))
    return texto


def separar(borrador: str) -> tuple[list[str], list[str]]:
    notas, prosa = [], []
    en_referencias = False
    for linea in borrador.splitlines():
        if linea.startswith("#"):
            en_referencias = (
                linea.lower().lstrip("# ").startswith(("referencias", "fuentes"))
            )
            continue
        nota = NOTA.match(linea)
        if nota:
            notas.append(nota.group(1))
        elif linea.strip() and not en_referencias and linea.strip() != "---":
            prosa.append(linea)
    return notas, prosa


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    borrador = Path(sys.argv[1]).read_bytes().decode("utf-8")
    fuentes = " ".join(normalizar(leer_fuente(Path(r))) for r in sys.argv[2:])
    notas, prosa = separar(borrador)
    fallas = 0

    for nota in notas:
        for cita in CITA.findall(nota):
            for trozo in (t.strip() for t in cita.split("[...]")):
                if not trozo:
                    continue
                if normalizar(trozo) in fuentes:
                    print(f"ok      cita  «{trozo[:70]}»")
                else:
                    print(f"FALTA   cita  «{trozo[:70]}» no está en las fuentes")
                    fallas += 1

    for linea in prosa:
        corta = linea[:60]
        for m in DOS_PUNTOS_CONECTOR.finditer(linea):
            print(
                f"FALLA   dos puntos como conector cerca de «{linea[max(0, m.start() - 30) : m.end() + 10]}»"
            )
            fallas += 1
        if "—" in linea or "–" in linea:
            print(f"FALLA   raya en «{corta}»")
            fallas += 1
        for frase in re.split(r"(?<=[.?!])\s+", linea):
            if frase.startswith("No es "):
                print(f"REVISA  frase que abre negando «{frase[:70]}»")
                fallas += 1
        bajo = linea.lower()
        for frase in FRASES_DE_INDICE:
            if frase in bajo:
                print(f"FALLA   frase de índice «{frase}» en «{corta}»")
                fallas += 1

    print(f"\n{fallas} problema(s)." if fallas else "\nTodo pasa.")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
