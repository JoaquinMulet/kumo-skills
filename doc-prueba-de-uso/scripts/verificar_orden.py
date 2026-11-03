"""Comprueba que ningún término de un documento se use antes de la sección donde se explica.

Qué espera. La ruta del documento (.md, .html o .tex) y la de un contrato JSON con la forma
  {"término": {"patron": "expresión regular", "seccion": "título o id de la sección que lo explica"}}
Las claves que empiezan con _ son comentarios. Si falta "patron", se busca el término tal cual.

Las secciones son los títulos «#» de Markdown, los `<section id="...">` de HTML y los
`\\section{...}` de LaTeX. En Markdown y LaTeX la sección se nombra por su título exacto.

Qué devuelve. Una tabla con la 1.ª aparición de cada término y su veredicto. Sale con 0 si ningún
término se adelanta, 1 si alguno se usa antes de su sección, 2 si el uso o el contrato están mal.

Uso.
  uv run python -I scripts/verificar_orden.py documento.md contrato.json

Por qué existe. Un concepto que se usa antes de explicarse se lee como «no se entiende nada», y
ningún lector frío lo marca, porque al final del documento sí está explicado. En un curso de IFRS 9
este defecto sumó 22 secciones de deuda y solo se vio cuando alguien se trabó.
"""

import json
import re
import sys
from pathlib import Path

PATRONES_SECCION = [
    re.compile(r"^#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$", re.M),  # Markdown
    re.compile(r'<section[^>]*\bid="([^"]+)"'),  # HTML
    re.compile(r"\\(?:chapter|section|subsection)\*?\{([^}]*)\}"),  # LaTeX
]


def secciones(texto):
    """Lista ordenada de (posición, nombre de la sección)."""
    halladas = [(m.start(), m.group(1).strip()) for p in PATRONES_SECCION for m in p.finditer(texto)]
    return sorted(halladas)


def seccion_en(secs, posicion):
    actual = "(antes de toda sección)"
    for inicio, nombre in secs:
        if inicio > posicion:
            break
        actual = nombre
    return actual


def main(argv):
    for flujo in (sys.stdout, sys.stderr):
        flujo.reconfigure(encoding="utf-8", errors="replace")
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    doc, ruta_contrato = Path(argv[1]), Path(argv[2])
    for ruta in (doc, ruta_contrato):
        if not ruta.is_file():
            print(f"No existe {ruta}.", file=sys.stderr)
            return 2
    texto = doc.read_bytes().decode("utf-8-sig")
    try:
        contrato = json.loads(ruta_contrato.read_bytes().decode("utf-8-sig"))
    except json.JSONDecodeError as e:
        print(f"El contrato no es JSON válido. {e}", file=sys.stderr)
        return 2

    secs = secciones(texto)
    orden = [nombre for _, nombre in secs]
    print(f"Leí {doc} con {len(secs)} secciones y {len(contrato)} entradas en el contrato.")
    if not secs:
        print("No encontré ninguna sección. Revisa que el documento use títulos #, <section id> o \\section.", file=sys.stderr)
        return 2

    adelantados, problemas = [], []
    for termino, spec in contrato.items():
        if termino.startswith("_"):
            continue
        seccion = spec.get("seccion")
        if seccion not in orden:
            problemas.append(f"«{termino}». La sección «{seccion}» no existe en el documento.")
            continue
        m = re.search(spec.get("patron") or re.escape(termino), texto)
        if not m:
            problemas.append(f"«{termino}». No aparece en el documento. ¿Se perdió?")
            continue
        donde = seccion_en(secs, m.start())
        distancia = orden.index(seccion) - (orden.index(donde) if donde in orden else -1)
        if distancia > 0:
            adelantados.append((distancia, termino, donde, seccion))
            print(f"  ADELANTADO  «{termino}» se usa en «{donde}» y se explica en «{seccion}»")
        else:
            print(f"  ok          «{termino}» aparece primero en «{donde}»")

    for p in problemas:
        print(f"  REVISAR     {p}")
    if adelantados or problemas:
        print(f"\nROJO. {len(adelantados)} términos adelantados y {len(problemas)} entradas por revisar.")
        return 1
    print("\nVERDE. Ningún término se usa antes de su sección.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
