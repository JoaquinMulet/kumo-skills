# Evidencia sobre comunicación y visualización

Resumen de la investigación del 28 y 29 de octubre de 2026 para el documento de Anthropic. Trabajaron 5 agentes de búsqueda y 1 auditor sin contexto, que comprobó 17 citas en las fuentes descargadas. Resultaron 13 confirmadas, 4 parciales y ninguna inventada. Las parciales van aquí con su alcance corregido.

## 1. Respaldo fuerte

| Regla | Evidencia | Cómo se aplica |
|---|---|---|
| Comparar cantidades con posición sobre una escala común | Heer y Bostock (2010) replicaron el orden de Cleveland y McGill. La posición gana al largo. El ángulo no salió peor que el largo, así que el orden completo no se replicó | Barras alineadas, líneas y puntos. Sin tortas para comparar |
| No apilar lo que hay que comparar | Talbot, Setlur y Anand (2014). Las barras apiladas se leen peor | Barras horizontales alineadas |
| El título manda sobre lo que se recuerda | Kong, Liu y Karahalios (2018). 65 de cada 100 mensajes recordados reflejaban el título. Borkin y coautores (2016). El título fue lo más descrito | Títulos descriptivos y fieles a los datos |
| Barras desde cero | Correll, Bertini y Franconeri (2020). Cortar el eje exagera en barras y en líneas | Toda barra parte en cero. En líneas, el rango se ve en el eje |
| Etiquetas directas en vez de leyenda | Franconeri y coautores (2021). Consultar una leyenda exige memoria de trabajo | Cada línea lleva su nombre al final |
| Sin arcoíris | Liu y Heer (2018). La paleta jet fue la peor en tiempo y error | Una escala de azules y un naranja de contraste |
| Gráfico junto al texto que lo comenta | Noetel y coautores (2021) citan contigüidad espacial con g = 0,63 en 58 comparaciones | El gráfico flota al tope de la página donde se nombra |
| Títulos numerados que muestren la jerarquía | Lorch, Lemarié y Grant (2011). Señalar la organización dio esquemas más completos | Capítulos y secciones numerados, repetidos en el índice |
| Señalar lo esencial con moderación | Noetel y coautores (2021) citan señalización con g = 0,43 en 209 comparaciones | Un recuadro de resumen por capítulo, nada más |

## 2. Respaldo medio o bajo

- Tener o no serifa no cambia la velocidad de lectura (Arditi y Cho, 2005, con 4 participantes y texto de 18 pt). La letra es una elección estética.
- El tamaño crítico de lectura ronda 0,2 grados de altura x (Legge y Bigelow, 2011). 12 pt deja margen de sobra.
- Líneas de 60 a 70 caracteres e interlineado de 1,2 a 1,5 veces la letra (Lonsdale, 2016, y otros).
- El texto justificado perjudicó solo con líneas cortas de unas 7 palabras (Gregory y Poulton, 1970). Con 11 palabras por línea, justificar con división silábica deja una columna rectangular sin costo medido.
- Poner la conclusión primero no tiene ensayos controlados. El resumen al inicio de cada capítulo tiene apoyo indirecto.
- La lectura en papel rinde algo mejor (Delgado y coautores, 2018, g = −0,21). El PDF debe imprimirse bien en A4.

## 3. Referencias del género

Para un documento de inversión se revisaron J.P. Morgan, Goldman Sachs, BCG, Bain, Deloitte, PwC y los informes de Anthropic. De ahí salieron 3 líneas gráficas.

| Elemento | Banca de inversión | Consultora editorial | Informe de investigación |
|---|---|---|---|
| Portada | Franja de color con ficha y tesis en 3 puntos | Campo de color con recuadro blanco | Fondo blanco, título con serifa en 2 tonos |
| Letra del texto | IBM Plex Serif | Libertinus Serif | XCharter |
| Letra de títulos | IBM Plex Sans | Inter | Fira Sans |
| Densidad | Alta | Media | Baja, con mucho blanco |

El lector eligió el informe de investigación. Es la base de `plantillas/estilo-informe.tex`.

## 4. Huecos

- McKinsey, el research de Goldman Sachs y Morgan Stanley bloquean a los programas, y los agentes respetaron el bloqueo.
- Ningún estudio usa lectores financieros. La evidencia viene de público general o estudiantes.

## 6. Tablas y números (investigación del 31 de octubre de 2026)

Hecha sin agentes, con OpenAlex, Semantic Scholar, Crossref y Europe PMC. «Texto completo» quiere decir que se leyó el artículo entero. «Resumen» quiere decir que solo se leyó el resumen oficial.

| Hallazgo | Fuente | Qué se leyó |
|---|---|---|
| La ventaja de tabla o gráfico depende del ajuste entre formato y tarea | Vessey (1991), Decision Sciences | Resumen |
| Revisión que ordena los estudios de formato bajo ese ajuste | Kelton, Pennington y Tuttle (2010), Journal of Information Systems | Resumen |
| Tablas y gráficos se procesan más rápido que los datos escritos en el texto | Kelly (1993), Journalism Quarterly | Resumen |
| Una tabla simple se entendió mejor que el texto, con d = 0,39, en un ensayo prerregistrado con 2.305 personas | Brick, McDowell y Freeman (2020), Royal Society Open Science | Resumen en Europe PMC |
| 6 reglas para tablas, con el argumento de la memoria de corto plazo. Son preceptos, no experimentos | Ehrenberg (1977), Journal of the Royal Statistical Society A | Texto completo |
| La European Association of Science Editors pide 2 a 3 dígitos efectivos | Cole (2015), Archives of Disease in Childhood | Texto completo |
| Menos relleno de celda acelera la lectura. Las franjas alternadas no la aceleran | Tensmeyer, Bylinskii, Cai y Miller (2023), WWW, 590 personas | Resumen |

## 7. Lectores de documentos financieros (misma investigación)

| Hallazgo | Fuente | Qué se leyó |
|---|---|---|
| Un texto más legible produce reacciones más fuertes y más confianza en el documento | Rennekamp (2012), Journal of Accounting Research | Resumen en Crossref |
| Con un texto menos legible, el lector se apoya más en fuentes externas | Asay, Elliott y Rennekamp (2016), The Accounting Review | Resumen |
| El tono positivo influye solo con un texto poco legible | Tan, Wang y Zhou (2013), Journal of Accounting Research | Resumen |
| Una conciliación cuantitativa reduce el efecto del énfasis en una cifra ajustada | Elliott (2006), The Accounting Review | Resumen |
| El formato cambia cuánto pesa una información | Maines y McDaniel (2000), The Accounting Review | Resumen |
| Los resúmenes cambian los juicios, y los de la empresa salen más positivos | Cardinaels, Hollander y White (2019), Review of Accounting Studies | Resumen |
| 30 de cada 100 gráficos financieros estaban distorsionados, con 10,7 % de exageración promedio | Beattie y Jones (1992), Accounting and Business Research | Resumen |
| Una distorsión mayor de 10 % cambia la percepción | Beattie y Jones (2002), Accounting, Auditing & Accountability Journal | Resumen |
| La organización del contenido cambia en qué se fija el lector | Ko, Cheng y Green (2023), European Accounting Review | Resumen |
| El diseño cambia atención y atractivo con el mismo contenido | Ceravolo y coautores (2019), International Journal of Bank Marketing | Resumen |
| Para los analistas, hablar con la gerencia es más útil que los informes 10-K y 10-Q | Brown, Call, Clement y Sharp (2015), Journal of Accounting Research | Resumen en Crossref |
| El índice Fog funciona mal con textos financieros | Loughran y McDonald (2014), The Journal of Finance | Resumen |

Descartado. Hunton y McEwen (1997) está retractado. Hirst y Hopkins (1998) y Bloomfield (2002) no se citan porque no se pudo leer ni su resumen.

Límites. Casi todos los participantes son inversionistas no profesionales o estudiantes de MBA, y ningún estudio mide informes largos de inversión.

## 5. Si investigas de nuevo

- Dimensiona con 4 a 6 agentes de búsqueda y 1 auditor, y pide confirmación al usuario antes de lanzarlos.
- El encargo a los agentes prohíbe por escrito saltarse el robots.txt, hacerse pasar por un navegador o mandar cabeceras falsas.
- Ninguna cita de un agente se usa sin abrir la fuente descargada y buscar la frase.
