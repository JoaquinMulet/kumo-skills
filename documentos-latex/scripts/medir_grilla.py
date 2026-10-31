"""Mide si las líneas de un PDF caen sobre la grilla de línea base.

Uso:
  uv run --with pymupdf python -I -X utf8 scripts/medir_grilla.py documento.pdf
      [--paso 15] [--tope-mm 37.125] [--lineas 35] [--cuerpo 12] [--tol 0.15] [--todos]

Los valores por defecto son los de plantillas/estilo-informe.tex.
Para cada línea de texto toma la línea base (campo «origin» de PyMuPDF, el origen del primer
glifo) y calcula su resto respecto de la grilla, (y - tope) mod paso. Una línea está en la
grilla si el resto es menor que la tolerancia, en puntos PDF (1/72 in, que difieren de los pt de
TeX en 72/72,27).
Imprime una tabla por tamaño de letra. La fila «cuerpo» es la que debe quedar con 0 fuera. Las
otras filas (portada, títulos de varias líneas, texto de las tablas) se miran caso a caso.
Devuelve código 0 si todo el cuerpo está en la grilla, 1 si no, y 2 si el PDF no se puede leer.
"""
import argparse
import collections
import sys

import pymupdf

ap = argparse.ArgumentParser()
ap.add_argument("pdf")
ap.add_argument("--paso", type=float, default=15.0, help="interlineado en pt de TeX")
ap.add_argument("--tope-mm", type=float, default=37.125, help="margen superior de la caja")
# 0,15 pt es menos que lo que se ve a ojo y más que el redondeo de PyMuPDF.
ap.add_argument("--tol", type=float, default=0.15)
ap.add_argument("--cuerpo", type=float, default=12.0, help="tamaño del texto del cuerpo")
ap.add_argument("--lineas", type=int, default=35, help="líneas de la caja de texto")
ap.add_argument("--todos", action="store_true", help="listar también las líneas en grilla")
a = ap.parse_args()

PT = 72 / 72.27                       # 1 pt de TeX en puntos PDF
paso = a.paso * PT
tope = a.tope_mm / 25.4 * 72          # borde superior de la caja de texto
try:
    doc = pymupdf.open(a.pdf)
except Exception as e:  # PDF ausente o cortado
    print(f"No pude abrir {a.pdf}: {e}", file=sys.stderr)
    sys.exit(2)
total = collections.Counter()
fuera = []
for npag, pag in enumerate(doc, 1):
    vistos = set()
    for b in pag.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            spans = [s for s in ln["spans"] if s["text"].strip()]
            if not spans:
                continue
            s0 = max(spans, key=lambda s: len(s["text"]))
            y = round(ln["spans"][0]["origin"][1], 2)
            x = round(ln["spans"][0]["origin"][0], 1)
            if (y, x) in vistos:
                continue
            vistos.add((y, x))
            if (y - tope) / paso > a.lineas + 0.5:
                continue  # folio o pie de página, fuera de la caja de texto
            tam = round(s0["size"], 2)
            texto = "".join(s["text"] for s in ln["spans"]).strip()[:50]
            resto = (y - tope) % paso
            resto = min(resto, paso - resto)
            ok = resto < a.tol
            # la expansión de microtype cambia el tamaño informado en unas décimas
            clase = "cuerpo" if abs(tam - a.cuerpo) < 0.3 else f"{tam}pt"
            total[(clase, ok)] += 1
            if not ok or a.todos:
                linea = round((y - tope) / paso, 2)
                fuera.append((npag, clase, linea, round(resto, 2), x, texto))

print("clase          en_grilla  fuera")
for c in sorted({k[0] for k in total}):
    print(f"{c:<14} {total[(c, True)]:>9}  {total[(c, False)]:>5}")
print()
print("pag  clase       linea  resto_pt  x      texto")
for f in fuera:
    print(f"{f[0]:<4} {f[1]:<11} {f[2]:>6}  {f[3]:>7}  {f[4]:<6} {f[5]}")
sys.exit(1 if total[("cuerpo", False)] else 0)
