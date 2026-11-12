"""Comprueba un borrador en Markdown antes de mostrárselo al autor.

Hace 2 cosas.
1. Busca cada cita entre comillas angulares («...») de las notas al pie del borrador en el texto de
   las fuentes. Una cita con «[...]» se parte en trozos y se busca cada trozo. Los espacios, los
   saltos de línea y los apóstrofos curvos se normalizan antes de buscar.
2. Revisa la prosa (todo lo que no es nota al pie, título ni referencia) contra las reglas de la casa.
   Marca los dos puntos usados como conector, las rayas, las frases que abren negando («No es…») y
   las frases de índice que mandan al lector a otra parte del texto.
3. Lista las frases que pueden ser bisagra o catafóricas, es decir, frases cortas que abren con un
   demostrativo o un colectivo («Esa…», «Las dos…», «Cada una de esas…») y no traen nota, cifra ni
   nombre propio. A cada una se le aplica la prueba de borrar. Si al borrarla no se pierde ningún
   hecho, se elimina. Esta lista no cambia el código de salida, porque el juicio es del que escribe.
4. Lista las frases con una negación que puede ser el contraste retórico prohibido («X no es Y, sino Z»,
   «y no el…», «distinto de…», «no da lo mismo»). Tampoco cambia el código de salida, porque una
   negación de un hecho («ninguno usa un marco general») sí vale.
5. Compara cada frase del último párrafo de la prosa con todas las frases anteriores y marca con
   «REPITE?» la que comparte 4 o más palabras largas con una frase ya escrita. Sirve para ver si el
   párrafo nuevo vuelve a explicar algo que el texto ya explicó. Tampoco cambia el código de salida.

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
CITA_ENTRE_PARENTESIS = re.compile(
    r"\((?:[^()]*\b(?:1[5-9]|20)\d{2}\b[^()]*|pp?\. \d[^()]*)\)"
)
DOS_PUNTOS_CONECTOR = re.compile(r"[a-záéíóúñ»\)]: [a-záéíóúñ«]")
ABRE_REFIRIENDO = re.compile(
    r"^(?:Por eso, |Así, |Entonces, |Además, |Pero )?(?:Cada (?:una|uno) de )?"
    r"(?:esa|ese|esas|esos|esta|este|estas|estos|esto|eso|ambas|ambos|las dos|los dos|las tres|los tres|todo ello)\b",
    re.I,
)
CONTRASTE = re.compile(
    r"\b(?:no es|no son|sino|no da lo mismo|no basta|y no (?:el|la|los|las)|distint[oa]s? del?|no significa|tampoco|no duplica)\b",
    re.I,
)
NOTA = re.compile(r"^\[\^[^\]]+\]:\s*(.*)$")
CITA = re.compile(r"«([^»]+)»")


def puede_ser_bisagra(frase: str) -> bool:
    palabras = frase.split()
    if len(palabras) > 18 or "[^" in frase or re.search(r"\d", frase):
        return False
    if any(p[:1].isupper() for p in palabras[1:]):
        return False
    return bool(ABRE_REFIRIENDO.match(frase))


def palabras_de_contenido(frase: str) -> set[str]:
    sin_notas = re.sub(r"\[\^\d+\]", " ", frase.lower())
    return {p[:5] for p in re.findall(r"[a-záéíóúñü]{5,}", sin_notas) if p not in VACIAS}


VACIAS = {"entre", "sobre", "desde", "hasta", "donde", "cuando", "porque", "aunque", "también", "además", "cada", "todos", "todas", "otros", "otras", "puede", "pueden", "parte"}


def repeticiones(prosa: list[str], minimo: int = 4) -> list[tuple[str, str, list[str]]]:
    parrafos = [p for p in prosa if not re.match(r"^\d+\. |^Borrador|^- ", p)]
    if len(parrafos) < 2:
        return []
    anteriores = [
        f for p in parrafos[:-1] for f in re.split(r"(?<=[.?!])\s+", p) if f.strip()
    ]
    hallazgos = []
    for frase in re.split(r"(?<=[.?!])\s+", parrafos[-1]):
        propias = palabras_de_contenido(frase)
        mejor = max(anteriores, key=lambda a: len(propias & palabras_de_contenido(a)))
        comunes = sorted(propias & palabras_de_contenido(mejor))
        if len(comunes) >= minimo:
            hallazgos.append((frase, mejor, comunes))
    return hallazgos


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
    bisagras = []
    contrastes = []

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
        for m in CITA_ENTRE_PARENTESIS.finditer(linea):
            print(f"FALLA   cita entre paréntesis {m.group(0)}, va en nota al pie")
            fallas += 1
        if "—" in linea or "–" in linea:
            print(f"FALLA   raya en «{corta}»")
            fallas += 1
        for frase in re.split(r"(?<=[.?!])\s+", linea):
            if puede_ser_bisagra(frase):
                bisagras.append(frase)
            if CONTRASTE.search(frase):
                contrastes.append(frase)
            if frase.startswith("No es "):
                print(f"REVISA  frase que abre negando «{frase[:70]}»")
                fallas += 1
        bajo = linea.lower()
        for frase in FRASES_DE_INDICE:
            if frase in bajo:
                print(f"FALLA   frase de índice «{frase}» en «{corta}»")
                fallas += 1

    for frase in contrastes:
        print(f"CONTRASTE? frase que puede negar para corregir «{frase[:80]}»")
    if contrastes:
        print(
            f"\n{len(contrastes)} frase(s) con negación. Si niega una idea para afirmar otra, se reescribe diciendo solo lo que es."
        )
    for frase in bisagras:
        print(f"BORRAR? frase que puede no tener contenido «{frase[:80]}»")
    if bisagras:
        print(
            f"\n{len(bisagras)} frase(s) para la prueba de borrar. Si al borrarla no se pierde ningún hecho, se elimina."
        )
    for frase, anterior, comunes in repeticiones(prosa):
        print(f"REPITE? «{frase[:70]}»\n        se parece a «{anterior[:70]}» ({', '.join(comunes[:6])})")
    print(f"\n{fallas} problema(s)." if fallas else "\nTodo pasa.")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
