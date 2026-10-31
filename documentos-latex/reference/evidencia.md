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

## 5. Si investigas de nuevo

- Dimensiona con 4 a 6 agentes de búsqueda y 1 auditor, y pide confirmación al usuario antes de lanzarlos.
- El encargo a los agentes prohíbe por escrito saltarse el robots.txt, hacerse pasar por un navegador o mandar cabeceras falsas.
- Ninguna cita de un agente se usa sin abrir la fuente descargada y buscar la frase.
