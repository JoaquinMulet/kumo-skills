# Genera la version Markdown de cada pagina de un sitio estatico (index.md
# junto a cada index.html), para servirla ante Accept: text/markdown.
# Version generica de la skill markdown-para-agentes; la implementacion de
# referencia vive en kumo-cloud-web/scripts/generar_md.py.
#
#   uv run python generar_md.py --raiz public --base https://tudominio.cl
#
# Determinista: la transformacion vive en el codigo, no en un modelo.
# Falla (exit 1) si una pagina produce markdown sin H1 o demasiado corto.

import argparse
import io
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class ExtractorMd(HTMLParser):
    """Convierte el contenido util de una pagina a Markdown."""

    BLOQUES = {"h1": "# ", "h2": "## ", "h3": "### ", "p": "", "li": "- "}

    def __init__(self, base: str):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.md: list[str] = []
        self.pila: list[str] = []
        self.buffer: list[str] = []
        self.en_footer = False
        self.en_tabla = False
        self.fila: list[str] = []
        self.tabla: list[list[str]] = []
        self.href: str | None = None
        self.ol_n = 0
        self.en_ol = False
        self.saltar = 0  # dentro de <script>/<style>/<noscript>/<svg>/<canvas>

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript", "svg", "canvas"):
            self.saltar += 1
            return
        if self.saltar:
            return
        if tag == "footer":
            self.en_footer = True
            return
        if self.en_footer:
            return
        if tag == "table":
            self.en_tabla = True
            self.tabla = []
            return
        if self.en_tabla:
            if tag == "tr":
                self.fila = []
            elif tag in ("td", "th"):
                self.buffer = []
            return
        if tag == "ol":
            self.en_ol = True
            self.ol_n = 0
        if tag == "a":
            href = a.get("href", "")
            if href.startswith("/"):
                href = self.base + href
            self.href = href
            self.buffer.append("[")
            return
        if tag in ("strong", "b"):
            self.buffer.append("**")
            return
        if tag in self.BLOQUES:
            self.pila.append(tag)
            self.buffer = []

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg", "canvas"):
            self.saltar = max(0, self.saltar - 1)
            return
        if tag == "footer":
            self.en_footer = False
            return
        if self.en_footer or self.saltar:
            return
        if tag == "table":
            self.en_tabla = False
            if self.tabla:
                ancho = max(len(f) for f in self.tabla)
                filas = [f + [""] * (ancho - len(f)) for f in self.tabla]
                out = ["| " + " | ".join(filas[0]) + " |",
                       "|" + "---|" * ancho]
                out += ["| " + " | ".join(f) + " |" for f in filas[1:]]
                self.md.append("\n".join(out))
            return
        if self.en_tabla:
            if tag in ("td", "th"):
                self.fila.append(" ".join("".join(self.buffer).split()))
                self.buffer = []
            elif tag == "tr" and self.fila:
                self.tabla.append(self.fila)
            return
        if tag == "ol":
            self.en_ol = False
            return
        if tag == "a":
            self.buffer.append(f"]({self.href})" if self.href else "]")
            self.href = None
            return
        if tag in ("strong", "b"):
            self.buffer.append("**")
            return
        if self.pila and tag == self.pila[-1]:
            self.pila.pop()
            texto = " ".join("".join(self.buffer).split())
            self.buffer = []
            if not texto:
                return
            prefijo = self.BLOQUES[tag]
            if tag == "li" and self.en_ol:
                self.ol_n += 1
                prefijo = f"{self.ol_n}. "
            self.md.append(prefijo + texto)

    def handle_data(self, data):
        if self.saltar or self.en_footer:
            return
        if self.pila or self.en_tabla or self.href is not None:
            self.buffer.append(data)


def convertir(html_path: Path, base: str) -> str:
    html = io.open(html_path, encoding="utf-8").read()
    desc = re.search(r'<meta name="description" content="([^"]*)"', html)
    canon = re.search(r'<link rel="canonical" href="([^"]*)"', html)
    p = ExtractorMd(base)
    p.feed(html)
    cuerpo = "\n\n".join(p.md)
    cab = []
    if canon:
        cab.append(f"<!-- {canon.group(1)} -->")
    if desc:
        cab.append(f"> {desc.group(1)}")
    return ("\n\n".join(cab + [cuerpo])).strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, help="directorio publicado (ej: public)")
    ap.add_argument("--base", required=True, help="origen absoluto (ej: https://tudominio.cl)")
    args = ap.parse_args()
    raiz = Path(args.raiz)
    paginas = sorted(raiz.rglob("index.html"))
    errores = 0
    for pag in paginas:
        md = convertir(pag, args.base.rstrip("/"))
        if "# " not in md or len(md) < 200:
            print(f"ERROR: markdown sospechosamente vacio para {pag}")
            errores += 1
            continue
        destino = pag.with_name("index.md")
        io.open(destino, "w", encoding="utf-8", newline="\n").write(md)
        print(f"OK  {destino}  ({len(md)} chars)")
    if errores:
        return 1
    print(f"{len(paginas)} paginas convertidas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
