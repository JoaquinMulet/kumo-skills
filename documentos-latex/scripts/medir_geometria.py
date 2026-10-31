"""Mide la geometría de cada página de un PDF compuesto sobre una caja y una grilla.

Uso:
  uv run --with pymupdf python -I -X utf8 scripts/medir_geometria.py documento.pdf
      [--x0-mm 39.375] [--ancho-mm 131.25] [--tope-mm 37.125] [--paso 15] [--lineas 35]
      [--cuerpo 12] [--colgado-mm 16]

Los valores por defecto son los de plantillas/estilo-informe.tex (canon KOMA DIV 8 sobre A4).
Comprueba 4 cosas por página, salvo la portada:
1. Que todo el contenido quede dentro de la caja: del borde izquierdo de la columna al derecho,
   y del tope al fondo de la última línea. Los números de sección y de nota pueden colgar en el
   margen izquierdo hasta --colgado-mm.
2. Que el texto del cuerpo empiece en el borde izquierdo de la columna.
3. Cuántas líneas de la grilla quedan vacías al pie de la página.
4. Equilibrio (BM), equilibrio del centro (EM) y densidad (DM) según Ngo, Teo y Byrne (2003),
   con los bloques de texto, las imágenes y los rellenos como objetos. Van de 0 a 1.

Devuelve código 0 si no hay elementos fuera de la caja ni texto mal alineado, y 1 si los hay.
"""

import argparse
import sys

import pymupdf

MM = 72 / 25.4
PT = 72 / 72.27  # 1 pt de TeX en puntos PDF
# 1 mm de tolerancia horizontal. microtype saca la puntuación unos 0,6 mm al margen a propósito.
TOL = 1.0


def argumentos():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--x0-mm", type=float, default=39.375, help="borde izquierdo de la columna")
    ap.add_argument("--ancho-mm", type=float, default=131.25, help="ancho de la columna")
    ap.add_argument("--tope-mm", type=float, default=37.125, help="borde superior de la caja")
    ap.add_argument("--paso", type=float, default=15.0, help="interlineado en pt de TeX")
    ap.add_argument("--lineas", type=int, default=35, help="líneas de la caja")
    ap.add_argument("--cuerpo", type=float, default=12.0, help="tamaño del texto del cuerpo")
    ap.add_argument("--colgado-mm", type=float, default=16.0, help="cuánto pueden colgar los números")
    return ap.parse_args()


def objetos(pagina, fondo):
    """Cajas de los bloques de texto, imágenes y rellenos dentro del área de la caja."""
    cajas = []
    for b in pagina.get_text("blocks"):
        x0, y0, x1, y1 = b[:4]
        if y0 < fondo + 4 * MM:
            cajas.append((x0, y0, x1, y1))
    for im in pagina.get_image_info():
        cajas.append(tuple(im["bbox"]))
    for dib in pagina.get_drawings():
        r = dib["rect"]
        if dib.get("fill") is not None and r.width > 20 and r.height > 8 and r.y0 < fondo:
            cajas.append((r.x0, r.y0, r.x1, r.y1))
    return cajas


def equilibrio(cajas, ancho, alto):
    """BM, EM y DM de Ngo, Teo y Byrne con el color y la forma fijos."""
    if not cajas:
        return 1.0, 1.0, 1.0
    xc, yc = ancho / 2, alto / 2
    areas = [(x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in cajas]
    amax = max(areas) or 1e-9
    w = {"I": 0, "D": 0, "A": 0, "B": 0}
    for (x0, y0, x1, y1), a in zip(cajas, areas):
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        w["I" if cx < xc else "D"] += abs(cx - xc) * a / amax
        w["A" if cy < yc else "B"] += abs(cy - yc) * a / amax
    bv = (w["I"] - w["D"]) / max(w["I"], w["D"], 1e-9)
    bh = (w["A"] - w["B"]) / max(w["A"], w["B"], 1e-9)
    bm = 1 - (abs(bv) + abs(bh)) / 2
    n, suma = len(cajas), sum(areas) or 1e-9
    emx = 2 * sum(a * ((x0 + x1) / 2 - xc) for (x0, _, x1, _), a in zip(cajas, areas)) / (n * ancho * suma)
    emy = 2 * sum(a * ((y0 + y1) / 2 - yc) for (_, y0, _, y1), a in zip(cajas, areas)) / (n * alto * suma)
    em = 1 - (abs(emx) + abs(emy)) / 2
    dm = 1 - suma / (ancho * alto)
    return bm, em, dm


def main():
    a = argumentos()
    x0_caja, x1_caja = a.x0_mm, a.x0_mm + a.ancho_mm
    tope = a.tope_mm * MM
    paso = a.paso * PT
    fondo = tope + a.lineas * paso
    try:
        doc = pymupdf.open(a.pdf)
    except Exception as e:  # PDF ausente o cortado: se dice claro y se sale con error
        print(f"No pude abrir {a.pdf}: {e}", file=sys.stderr)
        sys.exit(2)
    if doc.page_count == 0:
        print("El PDF no tiene páginas. Revisa que el log diga «Output written».", file=sys.stderr)
        sys.exit(2)
    print(f"{'pág':>3} {'fuera de caja':>13} {'texto mal alineado':>18} {'vacías al pie':>13} {'BM':>5} {'EM':>5} {'DM':>5}")
    fallas = 0
    for i, pag in enumerate(doc):
        if i == 0:
            continue
        cajas = objetos(pag, fondo)
        fuera = sum(1 for x0, y0, x1, y1 in cajas
                    if y0 <= fondo + 4 * MM
                    and (x0 / MM < x0_caja - a.colgado_mm or x1 / MM > x1_caja + TOL or y0 < tope - 2))
        mal, ultima = 0, tope
        for b in pag.get_text("dict")["blocks"]:
            for linea in b.get("lines", []):
                for s in linea["spans"]:
                    if abs(s["size"] - a.cuerpo) < 0.5 and s["origin"][1] < fondo + 2:
                        x = s["origin"][0] / MM
                        ultima = max(ultima, s["origin"][1])
                        if x < x0_caja - TOL:
                            mal += 1
                        break
        for _, _, _, y1 in cajas:
            if y1 < fondo + 2:
                ultima = max(ultima, y1)
        vacias = max(0, round((fondo - ultima) / paso))
        bm, em, dm = equilibrio(cajas, pag.rect.width, pag.rect.height)
        fallas += fuera + mal
        print(f"{i + 1:>3} {fuera:>13} {mal:>18} {vacias:>13} {bm:5.2f} {em:5.2f} {dm:5.2f}")
    print(f"Total de elementos fuera de la caja o mal alineados: {fallas}")
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
