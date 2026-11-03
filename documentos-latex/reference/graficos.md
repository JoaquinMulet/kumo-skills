# Gráficos diseñados para un documento LaTeX

Los gráficos del documento de Anthropic se dibujaron con ECharts en una página web y se capturaron a PNG con el Edge instalado. Esta guía explica por qué y cómo.

## 1. Por qué no matplotlib

El lector rechazó 2 rondas. La primera con matplotlib y su estilo por defecto. La segunda con 10 «estilos» que eran el mismo gráfico de líneas con otro fondo y otra letra. Aprobó la tercera, hecha como una pieza editorial con jerarquía tipográfica, un solo color de acento y una anotación con el dato que importa.

Cuando le pidas elegir, las opciones difieren en el diseño, o sea en el tipo de gráfico, la composición y la forma de anotar.

## 2. Antes de dibujar

Carga la skill `dataviz`. Después escribe para cada gráfico la pregunta que responde y el tipo que le toca.

| Tarea del dato | Tipo |
|---|---|
| Totales por período | Columnas |
| Tendencia en el tiempo | Líneas |
| Ranking | Barras horizontales alineadas |
| Parte de un todo | Barra de parte y todo, o barras alineadas con su porcentaje |
| Cómo se arma un total | Cascada |
| Un valor contra un rango | Puntos sobre una recta con la banda marcada |
| Pocas cifras clave | Fichas de indicadores |
| Una serie protagonista | Énfasis con el resto en gris |

Un estilo elegido fija letra, color y terminación. No fija el tipo de gráfico. Con el estilo 10D elegido, entregué 5 barras de 6 gráficos, y el lector escribió «no todos los gráficos deben ser de barras».

Talbot y coautores (2014) midieron que una barra apilada se lee peor que barras alineadas. Por eso los proveedores de cómputo fueron en barras horizontales con su porcentaje escrito al lado.

## 3. Títulos

El título describe lo que se muestra y nunca lo interpreta. Nombra la variable, la entidad, la unidad y el período.

- Mal. «El flujo de caja libre aparece recién en el año 3».
- Bien. «Flujo de caja libre proyectado, años 1 a 10».

La conclusión va en el párrafo que comenta el gráfico. Una anotación puede marcar un dato, sin adjetivos. Esta regla la fijó el lector aunque la literatura (Kong y coautores, 2018) muestre que un título con la conclusión se recuerda más.

Bajo el título va un subtítulo con la unidad, por ejemplo «Miles de millones de US$ y variación porcentual sobre el trimestre anterior». Al pie va la fuente con su página.

## 4. Color

- Paleta Blues de ColorBrewer (Harrower y Brewer, 2003, The Cartographic Journal). Ese artículo recibió el premio Henry Johns de la Sociedad Cartográfica Británica en 2004. Lo comprobé en la fuente antes de decirlo.
- Un naranja de contraste (`#E6550D`) para la serie que debe separarse de los azules.
- Valida toda paleta de varias series con `scripts/validate_palette.js` de la skill `dataviz`.
- Sin arcoíris. Liu y Heer (2018) midieron que la paleta jet fue la peor en tiempo y error.

## 5. La página de gráficos

`plantillas/graficos.html` es la página del documento de Anthropic. Úsala como base.

- **TEMA** guarda colores y letras en un solo objeto.
- **lamina(id, titulo, sub, fuente, cuerpo)** agrega una lámina. `cuerpo.opcion()` devuelve una opción de ECharts, y `cuerpo.html()` devuelve HTML para fichas o barras dibujadas a mano.
- **?linea=nombre** en la dirección elige la línea gráfica. La línea `investigacion` quita fondo, tarjeta y margen lateral, para que el gráfico vaya sobre el blanco de la hoja y el título quede alineado con el borde del texto.
- **window.listo = true** avisa al capturador que la página terminó. La página espera `document.fonts.ready` antes de dibujar, para que las letras de Google Fonts ya estén cargadas.
- **El gráfico parte bajo el subtítulo**, midiendo dónde termina, aunque el título ocupe 2 líneas.
- Los números van con coma decimal y punto de miles (`coma()` y `miles()`), y el signo menos es el verdadero (−).

**El tamaño de la lámina sale de la grilla.** La lámina mide 1200 × 774,1 px. A 131,25 mm de ancho, la imagen mide 240 pt de alto, que son 16 líneas de 15 pt. Si cambias el ancho de la columna o el alto en líneas, recalcula el alto en px con alto = 1200 × (líneas × 15 pt) / (ancho en pt).

## 6. Captura

```bash
uv run --with playwright python scripts/capturar.py plantillas/graficos.html figuras investigacion
```

El capturador usa `channel="msedge"`, así que no descarga navegadores. Captura a escala 2 para que el PNG se vea nítido impreso. Si la página escribe errores en la consola, el capturador los imprime y sale con código 1.

También mide los textos superpuestos. Con el renderer SVG de ECharts cada etiqueta es un `<text>`, y si 2 textos visibles se cruzan más de 1,5 px por lado, el capturador imprime «TEXTO SUPERPUESTO» con los 2 textos y sale con código 1. Por cada lámina dice cuántos textos midió. Una lámina con 0 textos medidos, como las fichas de indicadores hechas en HTML, no se midió, y esa hay que mirarla en el PNG.

## 7. Mirar cada PNG

Lee cada imagen con la herramienta de lectura antes de entregarla. Busca:

- Etiquetas que chocan entre sí. En el gráfico de márgenes, al cambiar los datos, la etiqueta final «Costo de cómputo 48 %» se montó sobre «Margen operacional ajustado 19 %». Se arregló con desplazamientos verticales (`endLabel.offset`) de −16, 4 y 30 px.
- Una leyenda que se monta sobre sí misma o sobre los datos. Si cada línea lleva su nombre al final, la leyenda sobra y se quita (Franconeri y coautores, 2021).
- Etiquetas finales cortadas por el borde. Dales margen derecho en `grid.right`.
- Números redondeados que ya no cuadran con el texto del documento.

Después de cambiar datos, vuelve a mirar todos los PNG. Un cambio de valores mueve las etiquetas.

## 8. En el documento

El macro `\figura{archivo.png}{pie}` de la plantilla pone el gráfico a todo el ancho y 16 líneas de alto, y compone el pie en la grilla. El pie nombra la fuente con su cita APA, por ejemplo «Datos de Anthropic, PBC (2026, p. 158).», o dice «según la estimación de Damodaran» si los datos son de un autor.

Mantén el PNG de cada línea gráfica en su carpeta, por ejemplo `figuras/investigacion/`. No copies las láminas de una línea encima de las de otra. Pasó una vez con un `cp` apurado, y hubo que regenerar las láminas pisadas.
