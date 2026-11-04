---
name: analisis-de-empresas
description: Analiza una empresa para invertir, en pasos obligatorios y en orden. Primero la puerta de gobernanza e incentivos, que decide si vale la pena seguir. Después las 70 preguntas a los estados financieros (Lehman 2007 anotado por Buffett) con un anexo validado por script, la auditoría forense de manipulaciones contables (Schilit), el owner earnings con su capex de mantenimiento ajustado por inflación (Greenwald y Buffett), la valoración por DCF y comparables, el riesgo (Taleb y Marks) y el veredicto. Usa esta skill al partir el análisis de CUALQUIER empresa, al leer una memoria anual, un 10-K, un proxy o estados financieros, al calcular owner earnings o capex de mantenimiento, al valorar una acción, o cuando el usuario menciona gobernanza, incentivos, asignación de capital, calidad de las utilidades, contabilidad forense, valor intrínseco, DCF, margen de seguridad, tesis de inversión, Lehman, o "qué preguntas hacerle a estos números".
---

# Análisis de empresas

Son 8 pasos, en este orden. La puerta decide si el análisis parte. El checklist decide si el
análisis está completo. Los pasos 4 a 8 dicen cuánto vale y qué puede salir mal. Aquí se juntaron
`gobernanza-primero` y `checklist-lehman` el 3 de noviembre de 2026, y `deep-financial-analysis` y
`owner-earnings` el 4 de noviembre de 2026.

Las 4 revisiones forenses que antes corrían como agentes en paralelo ahora se hacen una tras otra, y
cada hallazgo se prueba con la cita de la nota en el archivo de la fuente. Es el criterio de Joaquín
del 3 de noviembre de 2026. Un trabajo queda bien hecho cuando una comprobación lo demuestra.

## Paso 1. La puerta de gobernanza


Decidido por el dueño el 14 de agosto de 2026, tras el análisis de Cencosud:
**si una empresa tiene mal los incentivos, no tiene para qué analizarse más.**
Los incentivos predicen la asignación de capital, la asignación de capital
predice el retorno del accionista minoritario, y ninguna valoración
sobrevive a una gerencia que asigna mal el capital de forma sistemática.
Esta puerta corre PRIMERO, antes de transcribir estados, antes del modelo,
antes de la valoración. Si la empresa reprueba, el entregable es una
advertencia corta con su evidencia, no un informe completo: el trabajo
grande se ahorra, que es el punto.

### Principio rector: el que pide capital tiene que sentir su precio

El estándar de referencia es el de Buffett, leído en sus cartas (no de
memoria: se citan con año y se releen antes de usarlas):

- **Carta de 1994 (Scott Fetzer / Ralph Schey):** al gerente se le cobra
  una tasa alta por el capital incremental que emplea y se le abona esa
  misma tasa por el capital que devuelve. La consecuencia textual: le
  conviene, y le conviene mucho, mandar a la matriz cualquier caja que no
  pueda usar con ventaja. El precio del capital viaja hasta el bono del
  gerente, en las 2 direcciones. El "premio" por devolver caja no es un
  interés pagado a la filial: es un abono en la fórmula del bono del
  gerente (la filial es 100% del grupo. No hay a quién más compensar).
- **Carta de 1996 (GEICO):** la fórmula separa crecer de operar para que el
  cargo no fabrique cortoplacismo: el bono mide (1) el crecimiento en
  pólizas y (2) la rentabilidad SOLO del negocio maduro (pólizas con más de
  un año), excluyendo explícitamente las pérdidas de primer año que el
  propio crecimiento causa. Sembrar hoy nunca castiga el bono de hoy.
- **El complemento (caso Clayton Homes):** el préstamo OPERATIVO de la
  matriz a la filial va casi al costo (costo de fondeo + ~1 punto), porque
  su fin es prestar la espalda crediticia del grupo. El cargo CARO va en el
  bono, por el capital propio empleado, y su tasa es el costo de
  oportunidad de la matriz, no su costo de fondeo. Son 2 instrumentos
  distintos y no se confunden.
- Las capas que evitan el cortoplacismo: fórmula a la medida de cada
  negocio, gerentes que duran más que sus proyectos (décadas), nada de
  presupuestos a la matriz ni guía trimestral ni opciones sobre acciones
  del holding para gerentes de unidad, y los negocios de maduración larga
  (energía, ferrocarril) retienen sus utilidades porque su reinversión
  rinde sobre la vara: la caja vive donde rinde más, no en Omaha por
  decreto.

### Los 4 exámenes de la puerta

Correr los 4. Cada uno con evidencia citada (documento, página) y grado de
respaldo declarado. La búsqueda mecánica se hace con script sobre el PDF
(pypdf o similar), declarando que es sensible a la extracción de texto.

**Examen 1, ¿El capital tiene precio por dentro?**
Fuente: la nota de segmentos (NIIF 8 / ASC 280) de los estados auditados.
Mirar dónde vive el costo financiero. Si los negocios se presentan con
costo financiero cero y todo el interés del grupo está estacionado en la
columna corporativa, desde el asiento de cada gerente el capital es gratis.
La nota refleja cómo el tomador de decisiones mira el negocio (esa es la
definición de la norma), así que es señal fuerte, pero es PRESENTACIÓN. No
prueba sola la ausencia de un cargo interno. Se combina con el examen 2.

**Examen 2, ¿Qué paga el bono?**
Fuente: memoria anual / proxy statement, sección de compensaciones.
Preguntas: ¿el bono anual depende del resultado de la unidad del gerente o
del consolidado? ¿Hay cargo por el capital empleado o retorno sobre capital
en la fórmula? ¿Cuánto del plan de largo plazo paga por PERMANENCIA (
quedarse no es desempeño)? Búsqueda mecánica de menciones: ROIC, retorno
sobre el capital, capital empleado, EVA, cargo por capital. Contar y citar
páginas. Una memoria que promete "asignación de capital disciplinada" y
menciona el retorno sobre el capital 0 veces en 200+ páginas es un
hallazgo, no una casualidad.

**Examen 3, El historial es el testigo (mínimo 10 años, ideal todo).**
El patrón de mala asignación es medible y tiene 4 huellas: (1) comprar
caro en la cima del ciclo (caja libre negativa en los años de compras, con
la utilidad viéndose sana). (2) el crecimiento comprado que no rinde
(ingreso real por debajo de peaks viejos, crecimiento orgánico ≈ 0);
(3) vender las joyas en el valle para pagar la fiesta (desinversiones de
los mejores negocios en los años de apriete). (4) una matriz que no se
achica con nada (costo corporativo real constante o creciente a través de
las desinversiones). Las 3 curvas (utilidad, caja libre, owner earnings)
más el capex ejecutado contra la necesidad de reposición son el
instrumento. La subinversión en mantenimiento durante los aprietes es la
quinta huella.

**Examen 4, El contraste explícito contra el estándar.**
Poner lado a lado lo que la empresa publica contra el arreglo de las
cartas de 1994 y 1996. El contraste hace legible el veredicto para
cualquier lector. No es "gobernanza mediocre" en abstracto, es "el precio
del capital no viaja al bono, y el estándar contrario existe publicado
desde 1994".

### El veredicto y sus consecuencias

- **Reprueba** (capital gratis por dentro + bono sin retorno sobre capital
  + historial con las huellas): el análisis TERMINA aquí. Entregable: 1 a 2
  páginas con la advertencia («cuidado: no invertir aquí hasta que esto
  cambie»), la evidencia citada y las señales de reapertura. No se
  construye modelo ni valoración: un negocio regular con esa gobernanza no
  es una inversión, es una apuesta a que esta vez sea distinto.
- **Aprueba con nota** (señales mixtas: por ejemplo, cargo interno
  mencionado pero sin fórmula publicada): el análisis sigue, con la
  gobernanza como riesgo nombrado y con las preguntas abiertas en la lista
  de lo que falta.
- **Aprueba**: el análisis sigue normal, y la sección de gestión del
  informe cita esta puerta como pasada.

Si el análisis completo ya existe cuando la evidencia aparece (caso
Cencosud), el hallazgo no se agrega como una sección más. **El hallazgo
central manda el orden**, capítulo propio, la conclusión abre con él, y
las demás cifras pasan a ser su respaldo.

**Señales de reapertura** (observables, no promesas): bonos de gerentes de
unidad atados al retorno sobre el capital que emplean. Un cargo interno por
capital publicado. Una matriz que se achica cuando el grupo vende. Cambio
de controlador o de CEO con historial probado de asignador. Las frases de
la memoria («asignación disciplinada», «visión de largo plazo») no son
señales. Son marketing hasta que una fórmula de bono las respalde.

**La excepción declarada.** Un precio de saldo no cura la gobernanza para
un minoritario, porque el descuento lo administra la misma gerencia que lo
causó. La excepción existe y se declara: cambio de control plausible,
activista adentro, o liquidación en curso. Sin catalizador, barato con mala
gobernanza es barato para siempre.

### Caso canónico: Cencosud, agosto 2026

El ejemplo completo vive en el análisis de Cencosud (informe, sección
5 bis). Las cifras que hacen de patrón:

- Examen 1: los 5 negocios presentados con costo financiero CERO en la
  nota de segmentos. 408 mil millones de CLP de interés del año
  estacionados enteros en la columna corporativa.
- Examen 2: memoria integrada 2025, página 53: bono anual que depende
  «fundamentalmente de los resultados de la Compañía en el último
  ejercicio» más permanencia. LTI que paga 20% al año durante 3 años SOLO
  por quedarse. ROIC y «retorno sobre el capital»: 0 menciones en 244
  páginas cuya carta del presidente promete «adecuada asignación de
  capital».
- Examen 3: 2010-2014 caja libre negativa 5 años seguidos comprando en la
  cima (Carrefour Colombia 2012 en subasta). Ingreso real de 2025 bajo el
  peak de 2013. Venta del 51% de las tarjetas (2015) y IPO de los malls
  (2019) para pagar deuda. Subinversión en mantenimiento 5 de 6 años entre
  2015 y 2020. Matriz de ~275 mil millones netos anuales que no se achicó
  con ninguna desinversión (407 en 2010 con la mitad del grupo). Recompra
  en la cima de liquidez (The Fresh Market 2022).
- Veredicto: reprueba. La conclusión del informe abre con la advertencia y
  el precio va segundo a propósito.

### Caso de contraste: ILC, agosto 2026 (aprueba con nota)

Mismo país, misma bolsa, y la otra cara. El análisis completo vive en
`Experimentos con AI/ILC/gobernanza-ilc.md`. Lo que lo hace ejemplo:

- Examen 1: holding de empresas REGULADAS, cada filial con su directorio,
  su capital regulatorio y su deuda propia. El capital no es gratis por
  dentro por construcción. La matriz declara su rol («analizar cada
  requerimiento de capital y aportar si es necesario para generar valor»)
  y los aportes van individualizados con monto.
- Examen 2: el variable de los ejecutivos SÍ nombra la rentabilidad sobre
  el patrimonio como métrica (con la nota: «entre otras», sin pesos
  publicados). Los directores llevan participación en utilidades con
  techo. ROIC y cargo por capital: 0 menciones igual. El estándar de
  Buffett tampoco está, pero el resultado se reporta en métricas de dueño.
- Examen 3 (verificado contra estados de la CMF): ROAE de 2 dígitos
  sostenido (12 a 23 por ciento), utilidad por acción de 0,84 a 2,84 en
  12 años, dividendos acumulados iguales al 93 por ciento del precio de
  la apertura a bolsa REPORTADOS POR LA EMPRESA como métrica de portada,
  recompra 2021 con la acción castigada y CANCELACIÓN de acciones, venta
  de la mitad de la joya (Habitat) pero a precio de socio estratégico con
  ganancia de 229 mil millones, entrada al banco POR ETAPAS mientras el
  activo mejoraba. Fracasos acotados y visibles (Vida Cámara Perú,
  RedSalud como sumidero vigilado).
- Veredicto: aprueba con nota (opacidad de la fórmula, controlador
  gremial, RedSalud). El análisis sigue, con esas 3 notas como riesgo
  nombrado.

La lección del par Cencosud e ILC. La retórica es idéntica en las 2
memorias («asignación de capital disciplinada» y «adecuada asignación de
capital»). Lo que separa a una de otra es la MÉTRICA en el bono, la
contabilidad POR ACCIÓN en la portada, y el historial verificado. La
puerta se pasa con esas 3 cosas, nunca con la retórica.

### Los 4 arquetipos medidos (agosto 2026, bolsa chilena)

La puerta corrida sobre 4 holdings el mismo dia dejo un mapa que sirve de
referencia rapida. Los analisis completos viven en las carpetas de cada
empresa dentro de «Experimentos con AI»:

| Empresa | Veredicto | Lo que decide |
| --- | --- | --- |
| Cencosud | Reprueba | Capital gratis por dentro, bono por resultado del ano y permanencia, historial con las 5 huellas |
| ILC | Aprueba con nota | ROE en la formula del bono, recompra con cancelacion, dividendos medidos contra el precio de origen; notas: pesos de la formula sin publicar, controlador gremial, RedSalud |
| Quinenco | Aprueba | Alineamiento por propiedad (82,9 por ciento), matriz de 69 personas con caja neta, NAV por accion publicado contra el precio, devolvio el windfall en dividendos en vez de comprar en la cima; notas: 1 independiente de 8, descuento de NAV sin recompras |
| Empresas Copec | Aprueba con nota dura | Propiedad familiar sin senales de agencia, PERO utilidad por accion plana 12 anos con ~15 mil millones de dolares de capex. La maquina reinvierte a un digito medio sin metrica que la obligue a rendir la vara |

Las 2 lecciones del mapa:

- **La propiedad familiar alinea contra el fraude, no contra la
  reinversion mediocre.** Quinenco y Copec tienen el mismo alineamiento
  por propiedad. Los separa la disciplina de devolver la caja cuando no
  hay precio (Quinenco) contra la conviccion de reinvertir siempre
  (Copec). La prueba del dolar retenido de Buffett es el instrumento que
  los distingue: cada peso retenido debe crear al menos un peso de valor.
- **La reclasificacion contable tambien es una senal.** Copec imprime los
  dividendos pagados en el flujo de OPERACION desde 2022 (financiacion en
  0). Legal, y viste el flujo de financiacion. Reclasificar antes de toda
  prueba de caja, y anotar quien elige presentaciones que favorecen.

### Trampas del instrumento (aprendidas corriendo la puerta)

- La búsqueda mecánica necesita BORDES DE PALABRA y normalización de
  acentos: «eva» aparece en «nueva» y en «eva-luación» cortada por el
  salto de línea. «tir» vive adentro de «invertir». Sin eso, el conteo
  miente en las 2 direcciones.
- El índice GRI o NCG de las memorias repite los títulos de capítulos
  («creación de valor» suele ser el capítulo de sostenibilidad): filtrar
  las páginas de índices antes de leer apariciones.
- Los estados principales pueden no imprimir el número de acciones: la
  ganancia por acción básica impresa sirve de segunda copia para
  reconstruirlo, declarando que es derivado.

## Paso 2. Las 70 preguntas a los estados financieros

Lee [`reference/checklist-lehman.md`](reference/checklist-lehman.md) completo y responde las 70
preguntas en un anexo del informe. Cada respuesta empieza con su número («23.») y lleva su evidencia
(una cifra, un documento con su página, una nota o un módulo del modelo), o la marca [SIN DATO] con lo
que falta conseguir.

El anexo se valida con un script, que falla si falta una pregunta o si una respuesta no trae ni
evidencia ni [SIN DATO].

```
uv run python -I scripts/validar_anexo.py anexo.md
```

Toda búsqueda de un término en una memoria (ROIC, EVA, «costo de capital») va con el script, que
usa bordes de palabra, decodifica entidades y junta los espacios. Un cero se confirma con una 2.ª
formulación.

```
uv run --with pymupdf python -I scripts/buscar_en_fuente.py memoria.pdf --contar ROIC --contar "costo de capital" --sin-acentos
```

## Paso 3. Preparar los datos

Lee [`reference/fase1-preparacion.md`](reference/fase1-preparacion.md). Junta la memoria o el 10-K,
el análisis de la gerencia y todas las notas, convierte los PDF a texto, y ubica las notas de
reconocimiento de ingresos, propiedades y depreciación, impuestos diferidos, partes relacionadas y
segmentos. Saca los ingresos por país y la inflación de cada país, porque el paso 5 los necesita. Dónde
está cada dato en un 10-K y en unos estados chilenos lo dice
[`reference/datos-donde-encontrarlos.md`](reference/datos-donde-encontrarlos.md).

La carpeta de trabajo va en `C:/dev/`, fuera de OneDrive, con `fuente/`, `analisis/` y `salida/`.

## Paso 4. Auditoría forense de manipulaciones contables

Lee [`reference/fase2-revision-forense.md`](reference/fase2-revision-forense.md) y aplica sus 4
revisiones una tras otra, sin agentes en paralelo.

| Revisión | Técnicas | Dónde mirar |
|---|---|---|
| Manipulación de utilidades | EM-1 a EM-7 | Reconocimiento de ingresos, impuestos diferidos, partes relacionadas |
| Flujo de caja | CF-1 a CF-3 | Estado de flujo completo, notas de cuentas por cobrar y por pagar |
| Métricas clave | KM-1 a KM-2 | Segmentos, cifras fuera de norma, definición de cada indicador |
| Contabilidad de adquisiciones | AA-1 a AA-3 | Combinaciones de negocios, plusvalía, intangibles |

Cada hallazgo lleva su severidad (`CLEAN`, `LOW`, `MEDIUM`, `HIGH` o `CRITICAL`) y la cita de la nota.
La cita se prueba con `scripts/buscar_en_fuente.py --cita` sobre el archivo de la fuente. Un hallazgo
cuya cita no aparece no entra al informe. El detalle de cada técnica está en la skill
`financial-shenanigans`, que es el resumen del libro de Schilit.

El puntaje de manipulaciones va de 0 a 100, ponderando la severidad de las 4 revisiones.

| Puntaje | Lectura | Efecto en la tasa de descuento |
|---|---|---|
| 0 a 20 | Limpio | Ninguno |
| 21 a 40 | Dudas menores | Suma 1 a 2 puntos |
| 41 a 60 | Dudas importantes | Suma 3 a 5 puntos |
| 61 a 80 | Manipulación seria | Suma 6 a 8 puntos, y se considera pasar |
| 81 a 100 | Probable fraude | No se invierte |

Con los hallazgos se arma la matriz de cruce (cuánto mueve cada uno la utilidad, el flujo y el
patrimonio) y las preguntas para el gerente de finanzas, según
[`reference/fase3-sintesis.md`](reference/fase3-sintesis.md).

## Paso 5. Owner earnings

Lee [`reference/owner-earnings.md`](reference/owner-earnings.md) completo y sigue sus pasos 1 a 9.
Sus anexos son [`reference/oe-ajustes-sin-caja.md`](reference/oe-ajustes-sin-caja.md),
[`reference/oe-factor-de-eficiencia.md`](reference/oe-factor-de-eficiencia.md),
[`reference/oe-negocios-en-declive.md`](reference/oe-negocios-en-declive.md),
[`reference/oe-plantilla-python.md`](reference/oe-plantilla-python.md) y el caso trabajado
[`reference/oe-ejemplo-pool-corp.md`](reference/oe-ejemplo-pool-corp.md).

Los hallazgos del paso 4 entran aquí. Las utilidades que no se repiten salen, los impuestos
diferidos que no se van a recuperar se castigan, y las reclasificaciones del flujo se anotan.

```
Edad de los activos = Depreciación acumulada / Depreciación anual
Piso de inflación   = Depreciación x (1 + inflación ponderada)^edad x uso de capacidad
Capex de mantenimiento = MAX(método alfa, piso de inflación)
Owner earnings      = Utilidad ajustada + Depreciación + Partidas sin caja - Capex de mantenimiento
```

Siempre van 3 escenarios. El pesimista no aplica el factor de eficiencia, el base usa el factor
calculado, y el optimista usa el capex real.

## Paso 6. Valoración

Lee [`reference/fase4-dcf.md`](reference/fase4-dcf.md) y
[`reference/fase5-comparables.md`](reference/fase5-comparables.md).

El DCF descuenta el owner earnings y no el flujo de caja libre estándar, porque separa el capex de
mantenimiento del de crecimiento. Un flujo que crece lleva restada su inversión en el mismo flujo.

```
Valor intrínseco = Suma(OE_t / (1+r)^t) + Valor terminal / (1+r)^n
Valor terminal   = OE_n x (1+g) / (r-g), con g de largo plazo nunca mayor a 3 por ciento
```

La tasa mínima depende de la calidad. Es 15 por ciento para una empresa con foso amplio, 20 para una
con foso angosto y 25 o más sin foso, y se le suman 3 a 8 puntos si el puntaje del paso 4 pasa de 40.
Se muestra una matriz de 5 por 5 de crecimiento contra tasa, con el precio actual marcado.

Los comparables se eligen por modelo de negocio, entre 5 y 10, y se usa EV sobre owner earnings además
de los múltiplos de siempre. El resultado va en un rango que junta el DCF, los comparables y el
múltiplo de owner earnings contra el precio actual.

Antes de comparar con el precio, el valor de los negocios pasa por el puente a la acción. Se resta la
deuda neta, se resta la parte de otros accionistas y se suma lo que no opera, y cada obligación se
resta una sola vez.

## Paso 7. Riesgo

Lee [`reference/fase6-riesgo.md`](reference/fase6-riesgo.md). Son 4 revisiones.
- La fragilidad (Taleb), de 1 a 5 en ingresos, balance, operación, competencia y gerencia, sobre 25.
- Las 5 fuentes de pérdida permanente de capital (Marks).
- El mapa de cisnes negros por categoría.
- El pensamiento de segundo nivel contra la opinión del consenso.

## Paso 8. Veredicto

Lee [`reference/filosofia-berkshire.md`](reference/filosofia-berkshire.md). Las 10 preguntas del
veredicto van con su evidencia.

| N.º | Pregunta |
|---|---|
| 1 | ¿Entiendo este negocio? |
| 2 | ¿Tiene un foso competitivo durable? |
| 3 | ¿La gerencia es honesta y capaz? (el paso 1) |
| 4 | ¿Los estados están limpios? (puntaje del paso 4 menor a 40) |
| 5 | ¿El owner earnings es positivo y crece? |
| 6 | ¿El ROIC supera al WACC de forma consistente? |
| 7 | ¿El balance es fuerte? (fragilidad mayor a 15 de 25) |
| 8 | ¿El precio está bajo el valor intrínseco, con margen de seguridad mayor a 25 por ciento? |
| 9 | ¿Se puede mantener 10 años o más? |
| 10 | ¿Estaría tranquilo si la bolsa cerrara 5 años? |

Con las 10 aprobadas es compra fuerte, con 8 o 9 es compra chica, con 6 o 7 va a la lista de
seguimiento, y con menos de 6 no se compra, por barata que esté. El margen de seguridad se calcula
desde el valor intrínseco ponderado de los 3 métodos del paso 6.

Los informes de salida tienen el formato de
[`reference/plantillas-de-informe.md`](reference/plantillas-de-informe.md).
