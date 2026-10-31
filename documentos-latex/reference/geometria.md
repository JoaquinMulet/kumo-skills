# Geometría medida de un documento LaTeX

Esta guía explica cada medida de `plantillas/estilo-informe.tex` y cómo cambiarla sin romper la grilla. El objetivo que el lector fijó fue «que geométricamente todo se vea perfecto», y la prueba es numérica: el cuerpo 100 % en la grilla y 0 elementos fuera de la caja.

## 1. Canon de página

La plantilla usa el canon de KOMA-Script (guía de KOMA, tabla 2.2) con DIV 8 sobre A4.

| Medida | Cálculo | Valor |
|---|---|---|
| Módulo horizontal u | 210 / 8 | 26,25 mm |
| Módulo vertical v | 297 / 8 | 37,125 mm |
| Ancho de la columna | 5u | 131,25 mm |
| Margen izquierdo y derecho | 1,5u | 39,375 mm |
| Margen superior | 1v | 37,125 mm |
| Alto de la caja | 35 líneas × 15 pt | 525 pt |
| Pie de página | a 1v del borde inferior | footskip 37,55 mm |

Con XCharter de 12 pt, esa columna da 69 caracteres por línea en promedio. Mídelo con PyMuPDF en un párrafo largo cada vez que cambies letra o ancho. El rango sano es de 60 a 70 caracteres (KOMA) o de 45 a 75 (Bringhurst).

Para otro canon, cambia DIV y recalcula todo con la tabla. Un DIV mayor da márgenes más chicos y columna más ancha. Si la columna supera 75 caracteres, sube la letra o baja el DIV.

**Una sola columna para texto, gráficos y tablas.** Una columna de notas al margen solo se justifica si tiene notas. Cuando las notas pasaron al texto, la columna quedó vacía, el texto quedó angosto junto a gráficos anchos, y el lector lo encontró «extremadamente raro».

## 2. Grilla de línea base

Todo espacio vertical es múltiplo del interlineado, `\rejL` = 15 pt (125 % de 12 pt). Así las líneas de 2 páginas enfrentadas quedan a la misma altura, y el ojo lee la página como un sistema.

Cómo cae cada elemento en la grilla:

- **Texto corrido.** `\lineskiplimit=-\maxdimen` fuerza siempre el interlineado. Sin eso, una línea con una letra alta o un número volado agrega 1 pt y se sale (TeX by Topic, capítulo 15).
- **Títulos.** `\rej@titulo{arriba}{abajo}{texto}` compone el título en una caja, redondea su alto a líneas enteras y deja la última línea base en la grilla. Los argumentos son líneas en blanco antes y después.
- **Recuadros y bloques sueltos.** `\rej@colocar{arriba}{abajo}` coloca la caja 0 para que la línea base anterior y la siguiente queden a un número entero de líneas.
- **Flotantes.** Solo `[tp]`, al tope de página o en página propia. Un flotante en medio del texto (`[h]`) quedó 2,41 pt fuera de la grilla, y compensarlo desalineó las otras 2 ubicaciones. El bloque entero mide un número entero de líneas.
- **Pies de figura y tabla.** No usan el paquete caption, que agrega 4,2 pt. El pie se guarda y se compone después como un párrafo de 10,39 sobre 15 pt.
- **Tablas.** Dentro de la tabla vuelve la regla normal (`\lineskiplimit\z@`), porque LaTeX apila las filas con interlineado 0 y con el interlineado forzado se encimaban. Los filetes de booktabs se calcularon para que cada fila mida 15 pt. Filete superior más su espacio suman 4,5 pt, que con los 10,5 pt de alto de la primera fila dan 15. El filete del medio más sus 2 espacios dan 7,25 + 0,5 + 7,25 = 15.
- **Notas.** Cada nota es un párrafo de la columna de texto con su número colgado en el margen y 1 línea en blanco antes y después. `\footnote` guarda la nota y `\notaspendientes`, escrito después del párrafo, la compone. `\footnotetext` después de una tabla la compone de inmediato. Una nota al margen larga chocaba con los gráficos.
- **Gráficos.** Miden 16 líneas de alto (240 pt) a todo el ancho. La lámina HTML se captura con la misma proporción, así que no se deforma. Ver [graficos.md](graficos.md).

## 3. Escala tipográfica

Cuarta justa (4/3) con una hebra intermedia, 12 × (4/3)^(k/2). Ningún tamaño se elige suelto.

| Uso | k | Tamaño | Interlineado |
|---|---|---|---|
| Notas pequeñas | −1,0 | 9 pt | 11,25 |
| Pies, tablas, notas | −0,5 | 10,39 pt | 15 |
| Cuerpo | 0 | 12 pt | 15 |
| Subsección | 0,5 | 13,86 pt | 15 |
| Sección | 1 | 16 pt | 22,5 |
| Subtítulo de portada | 2 | 21,33 pt | 30 |
| Capítulo | 3 | 28,44 pt | 30 |
| Título de portada | 4 | 37,93 pt | 45 |

Los interlineados son múltiplos o mitades de 15 para que todo caiga en la grilla.

## 4. Letras

pdfLaTeX en MiKTeX tiene XCharter, Fira Sans, Libertinus e IBM Plex. Lora, Source Serif 4 y Source Sans 3 no tienen archivos para pdfLaTeX y necesitan fontspec con XeLaTeX o LuaLaTeX. Cambiar de motor cambia las medidas, así que se decide en la etapa de línea gráfica, no después.

Tener o no serifa no cambia la velocidad de lectura (ver [evidencia.md](evidencia.md)). La elección es de estilo: serifa para el cuerpo y sin serifa para títulos, pies y tablas da 2 voces distinguibles.

## 5. Títulos que se parten bien

- `\raggedright` en los títulos. ragged2e estira el espacio hasta 2em y un título largo no se partía.
- Penalidades de viuda y huérfana en 0 dentro del título. Con 10000 el título no se partía en 2 líneas.
- Sin división silábica en títulos (`\hyphenpenalty\@M`).

## 6. Cómo medir

Los 2 medidores leen el PDF con PyMuPDF.

```bash
uv run --with pymupdf python -I -X utf8 scripts/medir_grilla.py documento.pdf --paso 15 --tope-mm 37.125 --lineas 35 --cuerpo 12
```

`medir_grilla.py` imprime una tabla por tamaño de letra. La fila `cuerpo` tiene que dar 0 fuera. Las otras filas (portada, títulos de varias líneas con su interlineado propio, texto de tablas) se revisan caso a caso, porque algunas quedan fuera a propósito.

```bash
uv run --with pymupdf python -I -X utf8 scripts/medir_geometria.py documento.pdf --x0-mm 39.375 --ancho-mm 131.25
```

`medir_geometria.py` cuenta por página los elementos fuera de la caja, el texto mal alineado, las líneas vacías al pie y 3 índices de equilibrio de Ngo, Teo y Byrne (2003). El total tiene que ser 0.

Un elemento fuera de la caja que no da Overfull en el log existe. Pasó con un URL largo en la lista de referencias, que se salió 1,2 mm. Se arregló con `\raggedright` en esa lista.

## 7. Medir no es mirar

El medidor de la versión de 2 anchos decía que todo estaba perfecto. Medía la grilla, no la coherencia de la página. Después de medir, renderiza cada página y mírala.

```bash
uv run --with pymupdf python -I -c "import pymupdf,sys; d=pymupdf.open(sys.argv[1]); [p.get_pixmap(dpi=75).save(f'pagina_{i+1}.png') for i,p in enumerate(d)]" documento.pdf
```

Revisa sobre todo:

- Un flotante que quedó antes del título de su sección.
- Páginas con muchas líneas vacías al pie.
- Tablas o gráficos que se ven más anchos que el texto.
