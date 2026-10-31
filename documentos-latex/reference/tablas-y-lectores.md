# Tablas, números y lectores de documentos financieros

Esta guía sale de una investigación del 31 de octubre de 2026 con OpenAlex, Semantic Scholar, Crossref y Europe PMC. Cada regla lleva su fuente y dice si la fuente es un experimento o el precepto de un experto. Las fuentes están en [evidencia.md](evidencia.md), secciones 6 y 7.

## 1. Tabla, gráfico o texto

La elección depende de la tarea del lector (Vessey, 1991).

| El lector necesita | Formato |
|---|---|
| Leer o comparar valores exactos | Tabla |
| Ver una tendencia, una forma o un orden de magnitud | Gráfico |
| Entender una idea con 1 o 2 cifras | Texto |

**Una serie de más de 3 cifras no va escrita en un párrafo.** Tablas y gráficos se procesan más rápido que los mismos datos en el texto (Kelly, 1993). Si un párrafo enumera 4 trimestres de ingresos, esos números van en una tabla o en un gráfico, y el párrafo dice qué significan.

**La comparación central del documento va en una tabla corta.** Un ensayo prerregistrado con 2.305 personas encontró que una tabla simple se entendió mejor que el mismo contenido en texto, con d = 0,39, en todos los niveles de manejo numérico (Brick y coautores, 2020). En un documento de inversión, eso son el caso optimista contra el pesimista, o los 3 escenarios.

## 2. Cómo se arma una tabla

Estas reglas son de Ehrenberg (1977). Son preceptos de un experto con un argumento de percepción y memoria, no resultados de un experimento.

1. **Redondea a 2 o 3 dígitos efectivos las cifras que se comparan.** Un dígito efectivo es uno que cambia entre las cifras de la columna. 3.465 y 3.320 se comparan mejor como 3,5 y 3,3 miles. La guía de la European Association of Science Editors pide 2 a 3 dígitos (Cole, 2015).
2. **Agrega un promedio o un total** por fila o por columna, como punto de referencia para el ojo.
3. **Pon en columnas las cifras que se comparan.** Se leen mejor hacia abajo que hacia el lado.
4. **Ordena las filas por tamaño** cuando el orden de las etiquetas no significa nada. Si las filas son años o trimestres, mantén el orden del tiempo.
5. **Espaciado simple y columnas juntas.** Deja un hueco cada 5 filas más o menos, y usa pocos filetes, solo para separar partes grandes. La plantilla ya usa booktabs con 3 filetes.
6. **Sin franjas de color alternadas.** En un experimento con 590 personas, las franjas y los bordes de fila no aceleraron la lectura, y menos relleno en las celdas sí la aceleró (Tensmeyer y coautores, 2023). Una sola fila destacada, la conclusión, sí sirve.

**El redondeo choca con la regla de reconciliar exacto con la fuente.** Las 2 reglas valen para tablas distintas.

- Una tabla que reproduce la fuente, como los gastos trimestrales del S-1, lleva las cifras exactas, para que el lector pueda cuadrarlas con la página citada.
- Una tabla para comparar, como los escenarios o los márgenes, se redondea, y el pie dice la unidad.
- Si una tabla redondeada viene de la fuente, el pie dice que las cifras están redondeadas y cita la página donde está el valor exacto.

## 3. Lo que se sabe de los lectores de documentos financieros

La evidencia viene casi toda de inversionistas no profesionales y estudiantes de MBA. Hay muy poca con analistas, y ninguna con informes largos de inversión.

**La legibilidad aumenta la confianza del lector, para bien y para mal.** Con un texto más legible, los inversionistas reaccionan más fuerte a las noticias buenas y a las malas, porque la fluidez de lectura les hace confiar más en el documento (Rennekamp, 2012). Con un texto menos legible, se apoyan más en fuentes externas (Asay y coautores, 2016). Un documento claro pesa más en la decisión, y por eso tiene que ser equilibrado. Las 2 lecturas, la optimista y la pesimista, van con el mismo cuidado.

**El tono pesa cuando el texto cuesta.** El tono positivo influyó solo con un texto poco legible (Tan y coautores, 2013). Un texto claro y un tono neutro, con títulos que describen sin interpretar, dejan al lector juzgar las cifras.

**Toda cifra ajustada va junto a la cifra contable y a su conciliación.** El énfasis en una cifra ajustada influyó en los inversionistas no profesionales, y una conciliación cuantitativa redujo ese efecto (Elliott, 2006). En el documento de Anthropic, el margen operacional ajustado va en el mismo gráfico que el margen operacional, con la página del S-1 donde está su definición. Nunca se muestra una métrica ajustada sola.

**El resumen pesa en la decisión, así que tiene el mismo equilibrio que el texto.** Los resúmenes cambian los juicios de los inversionistas, y los escritos por la empresa salen más positivos que el documento que resumen (Cardinaels y coautores, 2019). El recuadro «En pocas palabras» de cada capítulo nombra también el riesgo principal, no solo lo bueno.

**Una distorsión de más de 10 % en un gráfico cambia la percepción.** En informes anuales del Reino Unido, 30 de cada 100 gráficos financieros estaban distorsionados, con una exageración promedio de 10,7 % (Beattie y Jones, 1992). Una distorsión mayor de 10 % cambia lo que percibe el lector, y los de menos formación financiera son los más expuestos (Beattie y Jones, 2002). Las barras parten en cero y su largo es proporcional al valor. Si el eje no parte en cero, se usa un gráfico de líneas o de puntos.

**El diseño no es neutro.** La forma de organizar el contenido cambió en qué se fijaban los inversionistas con una posición tomada (Ko y coautores, 2023). El mismo contenido con otro diseño cambió la atención y el atractivo del producto (Ceravolo y coautores, 2019). El orden de los capítulos sigue las preguntas de la valoración, y cada pregunta muestra las 2 lecturas.

**No midas la legibilidad de un texto financiero con el índice Fog.** Cuenta como difíciles palabras comunes del área, como «company» o «financial» en inglés, y funciona mal con estos textos (Loughran y McDonald, 2014).

## 4. Lo que no cambió

La evidencia de esta investigación confirma reglas que la skill ya tenía:

- Títulos descriptivos.
- Barras desde cero.
- Cada cifra verificada contra su fuente.
- La tabla de las 2 lecturas del prospecto.
