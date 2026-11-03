---
name: documentos-latex
description: "Diseña, compone, verifica y entrega documentos LaTeX que comunican con calidad editorial: informes, documentos de inversión, reportes de análisis, síntesis de un texto ajeno y cualquier PDF largo para leer o compartir. Cubre la línea gráfica elegida con evidencia, la geometría medida (canon de página, grilla de línea base, escala tipográfica), los gráficos diseñados y capturados desde ECharts, las tablas y la evidencia sobre cómo leen los inversionistas, la verificación de cada cifra contra su fuente con citas APA, y la compilación en Windows con MiKTeX. Usar cuando el usuario pide un documento, informe o PDF en LaTeX, traducir o sintetizar un artículo a un documento, rehacer los gráficos de un documento, darle una línea gráfica o un sello, dejar la geometría perfecta, o verificar las cifras de un documento contra un prospecto, estado financiero u otra fuente primaria."
---

# Documentos LaTeX que comunican

Esta skill reúne lo que aprendimos al construir el documento de inversión sobre la salida a bolsa de Anthropic (octubre de 2026). Ese documento pasó por muchas rondas de correcciones del lector. Cada regla de abajo nació de una de ellas, y el porqué va con la regla.

El orden importa. Un documento bien medido con cifras falsas no sirve, y uno con cifras exactas y una página rara se lee mal. Las 6 etapas van en este orden, y cada una tiene una prueba que la cierra.

| Etapa | Qué se decide | Prueba que la cierra |
|---|---|---|
| 1. Contenido | Qué dice el documento y en qué orden | Esquema aprobado, citas resueltas |
| 2. Línea gráfica | Cómo se ve, elegido por el lector entre 3 o 4 propuestas | El lector eligió una |
| 3. Geometría | Canon, grilla, escala | Cuerpo 100 % en la grilla, 0 fuera de la caja |
| 4. Gráficos y tablas | Formato, diseño y datos de cada gráfico y tabla | Cada PNG mirado, sin textos montados |
| 5. Cifras | Cada número contra su fuente primaria | Informe de verificación cifra por cifra |
| 6. Entrega | PDF abierto, carpeta ordenada | El lector lo tiene abierto |

## Antes de empezar

1. Si el documento lleva gráficos, carga la skill `dataviz` ANTES de escribir la primera línea de un gráfico. En el documento de Anthropic no la cargué y entregué 5 gráficos de barras de 6.
2. Si el texto va a nombre del usuario, aplica la skill `unslop` a la prosa.
3. Copia `plantillas/estilo-informe.tex` a `estilo/` del proyecto como punto de partida, salvo que el lector elija otra línea gráfica en la etapa 2.
4. Crea la carpeta del proyecto fuera de OneDrive o de cualquier carpeta sincronizada, por ejemplo en `C:/dev/`. La compilación y las capturas reescriben archivos sin parar.

## Etapa 1. Contenido

**Un texto ajeno se sintetiza, no se traduce entero.** Un artículo con derechos de autor se reescribe con palabras propias, más corto, con el orden y las cifras del original. Las citas textuales son pocas, cortas y entre comillas, y cada una lleva después una frase que dice qué significa.

**La introducción narrativa va primero.** Cuenta la empresa, la industria y las preguntas que el documento responde, en párrafos de 3 frases como máximo. El lector que no conoce el tema tiene que poder seguir el resto.

**Cada capítulo abre con un recuadro de resumen**, justo bajo el título. El entorno `resumen` de la plantilla ya cae en la grilla.

**Las palabras difíciles van en un glosario al inicio**, con el macro `\termino`. Una palabra que aparece antes de explicarse es un defecto de orden. Para medirlo usa el script `verificar_orden.py` de `doc-prueba-de-uso`, que lee los `\section` del `.tex`.

**El resumen tiene el mismo equilibrio que el texto.** Los resúmenes cambian el juicio del lector, y los escritos por quien tiene interés salen más positivos que el documento (Cardinaels y coautores, 2019). Cada recuadro de resumen nombra también el riesgo principal.

**Un texto claro pesa más en la decisión.** Con un texto más legible, los inversionistas confían más en el documento y reaccionan más fuerte (Rennekamp, 2012). Por eso la lectura optimista y la pesimista van con el mismo cuidado.

**Lo que se calla también es un dato.** Si el documento sabe algo que le importa al lector, lo dice. La incertidumbre va junto al dato, nunca en su lugar.

## Etapa 2. Línea gráfica

El formato por defecto de LaTeX se ve como un apunte de clases. El lector lo llamó «demasiado fome sin un sello o línea gráfica clara».

1. Investiga referencias reales del género (bancos de inversión, consultoras, el informe de la propia empresa) y la evidencia sobre comunicación y visualización. El resumen de esa evidencia está en [reference/evidencia.md](reference/evidencia.md). No hace falta repetir la investigación si el género es el mismo.
2. Propón 3 o 4 líneas gráficas. Cada una con portada y una página interior real, compiladas y renderizadas a PNG. Las propuestas difieren en el diseño (densidad, letra, columna, rótulos), no solo en el color.
3. El lector elige. Una decisión de diseño nunca se anuncia como tomada.
4. La línea fija portada, pie de página, sistema de color, letras, recuadros y un sello que se repite. Los gráficos siguen la misma línea.

**Nada decorativo que no informe.** El lector pidió borrar el encabezado repetido con el título del documento y los rótulos de portada tipo «Serie Valoraciones, Documento N.º 1». El pie lleva solo «página X de Y».

**Si la línea imita a una empresa real, el documento lleva un aviso de que no está afiliado a ella**, y no usa su marca.

## Etapa 3. Geometría

La geometría se mide con programas, nunca a ojo. El detalle de cada medida, las fórmulas y las trampas de TeX están en [reference/geometria.md](reference/geometria.md). Léelo antes de tocar el estilo.

Las 4 reglas de fondo:

1. **Canon de página.** KOMA-Script con DIV 8 sobre A4 da una columna de 131,25 mm con 69 caracteres por línea en XCharter de 12 pt.
2. **Grilla de línea base.** Todo espacio vertical es múltiplo del interlineado (15 pt). Títulos, recuadros, tablas, pies y notas se componen para caer en ella.
3. **Escala tipográfica.** Cuarta justa, 12 × (4/3)^(k/2). Ningún tamaño se elige suelto.
4. **Texto y gráficos comparten el ancho.** Una versión con texto de 105 mm y gráficos de 157,5 mm le pareció al lector «extremadamente rara». La medición decía que todo estaba perfecto, porque medía la grilla y no la coherencia de la página. Cuando quitas un elemento del diseño, revisa qué medidas existían solo para él.

Después de cada cambio corre los 2 medidores. El cuerpo tiene que dar 0 líneas fuera y la geometría 0 elementos fuera.

```bash
uv run --with pymupdf python -I -X utf8 scripts/medir_grilla.py documento.pdf
```

```bash
uv run --with pymupdf python -I -X utf8 scripts/medir_geometria.py documento.pdf
```

Medir no reemplaza mirar. Renderiza las páginas a PNG con PyMuPDF y míralas como las mira el lector.

## Etapa 4. Gráficos y tablas

El proceso completo, con el código de la página de ECharts y el capturador, está en [reference/graficos.md](reference/graficos.md).

Las reglas que el lector impuso:

1. **Un gráfico se diseña, no se configura.** Matplotlib con su estilo por defecto fue rechazado, y 10 variantes del mismo gráfico con otro fondo también. Lo aprobado fue ECharts en una página web, capturado con Edge.
2. **El tipo sale de la tarea del dato.** Totales por período van en columnas, tendencias en líneas, rankings en barras horizontales, la suma de un total en cascada, un valor contra un rango en puntos sobre una recta, pocas cifras clave en fichas.
3. **El título describe, nunca interpreta.** Nombra la variable, la entidad, la unidad y el período, por ejemplo «Flujo de caja libre proyectado, años 1 a 10». La conclusión va en el texto. Esto rige aunque una guía recomiende títulos con la conclusión.
4. **La paleta tiene respaldo.** Azules de ColorBrewer (Harrower y Brewer, 2003), validada con el script de la skill `dataviz`.
5. **Dentro de la página, el gráfico va sobre el fondo de la hoja**, sin tarjeta ni marco de otro color.
6. **Cada línea lleva su nombre al final** en vez de una leyenda.
7. **Antes de entregar, mira cada PNG.** Ningún texto puede montarse sobre otro, sobre una barra o sobre un eje. En el documento de Anthropic la leyenda y las etiquetas finales chocaron después de cambiar los datos, y solo se vio al mirar la imagen.
8. **Las barras parten en cero y su largo es proporcional al valor.** Una distorsión mayor de 10 % cambia lo que percibe el lector (Beattie y Jones, 2002). Si el eje no parte en cero, va un gráfico de líneas o de puntos.
9. **Toda cifra ajustada va junto a la cifra contable.** Una conciliación con la cifra contable reduce el peso del énfasis en la ajustada (Elliott, 2006).
10. **La fuente de cada gráfico cita la página.** Si los datos salen de una fuente primaria, la línea de fuente dice «Fuente. Anthropic, PBC (2026), p. 158.». Si son estimaciones de un autor, lo dice.

### Tablas

El detalle y las fuentes están en [reference/tablas-y-lectores.md](reference/tablas-y-lectores.md).

1. **Tabla para valores exactos, gráfico para tendencias, texto para 1 o 2 cifras** (Vessey, 1991). Una serie de más de 3 cifras no va escrita en un párrafo.
2. **La comparación central del documento va en una tabla corta.** Una tabla simple se entendió mejor que el mismo contenido en texto en un ensayo con 2.305 personas (Brick y coautores, 2020).
3. **Una tabla para comparar se redondea a 2 o 3 dígitos efectivos**, con las cifras que se comparan en columnas, un total o promedio, y las filas ordenadas por tamaño si su orden no significa nada (Ehrenberg, 1977).
4. **Una tabla que reproduce la fuente lleva las cifras exactas**, para que el lector las cuadre con la página citada.
5. **Sin franjas de color alternadas.** No aceleraron la lectura en un experimento con 590 personas (Tensmeyer y coautores, 2023).

## Etapa 5. Cifras

El método completo, con el buscador de páginas y la plantilla del informe, está en [reference/cifras-y-fuentes.md](reference/cifras-y-fuentes.md).

1. **Toda cifra verificable se contrasta con la fuente primaria**, no con quien la cita. En el documento de Anthropic, 12 datos del autor original tenían diferencias con el prospecto S-1, y otros 6 no estaban en el S-1.
2. **La duda no se escribe, se resuelve.** Si la fuente está a mano, el documento lleva la cifra correcta con su cita APA y nada más. El lector rechazó notas como «conviene confirmarlo» y «lo confirmé en el S-1».
3. **Las citas van en APA con página**, por ejemplo (Anthropic, PBC, 2026, p. 158), y la lista de referencias va en el capítulo de fuentes.
4. **Lo que la fuente no trae se atribuye a quien lo dijo**, por ejemplo «según Damodaran», sin narrar la verificación.
5. **El detalle de la verificación va en un informe aparte**, con cada cifra, el valor anterior, el de la fuente, la página y el estado.
6. **Una suma que escribes se calcula antes de escribirla.** Una nota del documento de Anthropic decía que 4 trimestres sumaban 20.608 millones, sin haberlos sumado, y sumaban 19.708.
7. **2 cifras del mismo documento que se pueden comparar se comparan.** Si un límite y una acumulación conviven, la resta va escrita.

## Etapa 6. Compilación y entrega

```bash
bash scripts/compilar.sh documento.tex
```

El script compila 3 veces, quita del PATH la entrada rota de `cl.exe` y da el PDF por bueno solo si el log dice «Output written» y el PDF tiene páginas. El código de salida de MiKTeX no sirve como veredicto.

Al entregar:

1. Corre los 2 medidores y muestra sus números en el mensaje.
2. Abre el PDF en su programa con `Start-Process -FilePath 'ruta.pdf' -WindowStyle Normal` y envíalo con `SendUserFile`.
3. La raíz del proyecto lleva un `LEEME.md` que dice qué abrir primero, cómo compilar, cómo rehacer los gráficos y cómo medir.
4. Lo que se lee va separado de lo técnico. Las versiones descartadas van en `trabajo/`, no en la raíz.

## Trampas que ya costaron caro

- **Barras invertidas por la línea de comando.** Un `sed`, un heredoc o un `python -c` convierte `\t`, `\b` o `\n` de LaTeX en caracteres invisibles, o se come la barra de `\$`. Todo texto con barra invertida se edita con Edit o Write. Después de cualquier edición por script, cuenta los bytes 7, 8 y 12 del `.tex`, que tienen que dar 0.
- **Letras que pdfLaTeX no tiene.** Lora, Source Serif y Source Sans necesitan fontspec y XeLaTeX. Con pdfLaTeX funcionan XCharter, Fira Sans, Libertinus e IBM Plex.
- **El paquete caption agrega 4,2 pt** sobre el pie. La plantilla compone el pie como un párrafo propio.
- **ragged2e estira el espacio hasta 2em** y un título largo no se parte. Los títulos usan `\raggedright` con penalidades de viuda y huérfana en 0.
- **Una columna `p{}` sale justificada** y en un ancho angosto deja huecos grandes entre palabras, o parte una palabra con guion. La plantilla trae la columna `P{ancho}`, alineada a la izquierda y sin partir palabras.
- **Una tabla ancha se sale de la columna** sin aviso visible. Encabezados en 9,5 pt, `\tabcolsep` de 3 pt y primera columna con ancho fijo.
- **Un texto de 2 a 3 palabras de un URL largo se sale de la caja** sin Overfull en el log. Usa `\raggedright` en la lista de referencias.

## Archivos de la skill

- `plantillas/estilo-informe.tex` es la línea «Informe de investigación» con toda la geometría resuelta.
- `plantillas/graficos.html` es la página de ECharts del documento de Anthropic, con sus 7 láminas de ejemplo.
- `scripts/compilar.sh`, `scripts/medir_grilla.py`, `scripts/medir_geometria.py`, `scripts/capturar.py` y `scripts/buscar_fuente.py` son los programas de las etapas 3 a 6.
- `reference/` guarda el detalle de geometría, gráficos, tablas y lectores, cifras y evidencia.
