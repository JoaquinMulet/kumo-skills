# Paso 4. La revisión forense, paso a paso

Responde una pregunta. ¿Los estados financieros muestran el negocio o lo tapan? Sigue las 15
manipulaciones de «Financial Shenanigans» (Schilit, Perler y Engelhart, 4.ª edición). La idea que
ordena todo es del libro. Un truco contable casi siempre tapa un deterioro del negocio, así que
cada hallazgo termina diciendo qué problema estaría tapando.

La revisión la hace una sola persona o un solo agente, en orden, sin repartirla. Son 6 acciones y
producen un anexo de 15 veredictos que un script valida.

## Qué necesita antes de partir

Sale del paso 3. Si algo falta, la prueba que lo usa queda en SIN DATO. Nunca queda en LIMPIO.

| Insumo | En una empresa chilena | En una empresa de Estados Unidos |
|---|---|---|
| Informe del período, completo, con sus notas | Estados financieros consolidados de la CMF | 10-K o 10-Q |
| El mismo informe del período anterior | Estados del año anterior | 10-K o 10-Q anterior |
| Explicación de la gerencia | Análisis razonado | MD&A, que viene dentro del 10-K |
| Lo que la empresa destaca | Comunicado y presentación de resultados | Comunicado de resultados (anexo 99 de un 8-K) |
| Compensación de los ejecutivos | Memoria anual | Proxy (DEF 14A) |
| Avisos fuera de calendario | Hechos esenciales del año | 8-K, NT 10-K, 10-K/A |
| Cifras de 5 años, o las que existan | Estados de cada año | 10-K de cada año |

Con 2 períodos se puede correr. Con 5 se ven los patrones, que es lo que el libro pide mirar.

## Las 6 acciones

### 1. Armar la tabla de cifras y calcular las razones

Copia a `analisis/cifras.csv` las cifras de cada período, una fila por concepto. Los períodos
tienen que ser comparables entre sí, o sea años completos o el mismo trimestre de cada año.

```
uv run python -I scripts/razones_forenses.py analisis/cifras.csv
```

| Concepto del CSV | De dónde sale | Nombre habitual en estados chilenos |
|---|---|---|
| `ingresos`, `costo_ventas`, `utilidad_neta` | Estado de resultados | Ingresos de actividades ordinarias, Costo de ventas, Ganancia |
| `utilidad_operacional` | Estado de resultados | No siempre viene. Se arma como ganancia bruta menos costos de distribución y gastos de administración |
| `flujo_operacional`, `capex`, `adquisiciones`, `dividendos` | Estado de flujo de efectivo | Flujos de actividades de operación, Compras de propiedades, planta y equipo, Flujos para obtener el control de subsidiarias, Dividendos pagados |
| `cuentas_por_cobrar`, `provision_incobrables` | Balance y nota de cuentas por cobrar | Deudores comerciales y otras cuentas por cobrar, y su deterioro |
| `cuentas_por_cobrar_vendidas` | Nota de cuentas por cobrar | Cartera cedida, securitizada o en factoring que sigue pendiente |
| `documentos_por_cobrar` | Balance y notas | Documentos por cobrar, pagarés y letras de clientes |
| `inventario`, `inventario_largo_plazo` | Balance y nota de inventarios | Inventarios corrientes y no corrientes |
| `cuentas_por_pagar` | Balance | Cuentas por pagar comerciales y otras cuentas por pagar |
| `ingreso_diferido` | Balance y notas | Ingresos diferidos, suele estar en Otros pasivos no financieros |
| `pasivos_blandos` | Balance | Otras provisiones más Otros pasivos no financieros, sin el ingreso diferido |
| `activos_blandos` | Balance | Otros activos no financieros, gastos anticipados, costos diferidos |
| `cartera_morosa`, `provision_cartera` | Notas de una financiera | Cartera con mora o deteriorada, y su provisión |
| `dias` | Largo del período | 365 en un año, 91.25 en un trimestre |

El script entrega las razones y una lista de avisos. Un aviso dice qué pruebas abrir primero. No es
un hallazgo, porque la tabla no ve las notas.

### 2. Comparar el informe con el del período anterior

Es la técnica que el libro más recomienda. Una empresa cambia la redacción de una nota solo cuando
algo cambió.

```
uv run python -I scripts/comparar_notas.py fuente/anterior.txt fuente/actual.txt --max 80
```

El script lista las frases que cambiaron, las nuevas y las que desaparecieron, sin contar las que
solo cambiaron sus cifras. En un informe entero salen cientos. Primero se lee la lista de las que
CAMBIARON, que son pocas y son las que más dicen. Después se acota por tema con `--contiene`, usando
los términos que da cada prueba en [`forense-pruebas.md`](forense-pruebas.md).

Por cada cambio de política, de estimación o de definición se hacen las 2 preguntas del libro. Por
qué cambió, y por qué ahora. Después se calcula cómo se habría visto el período sin el cambio. La
nota del cambio suele dar el monto.

### 3. Leer completas las secciones donde se esconden las cosas

Lo favorable va al comunicado. Lo necesario y poco favorable va al fondo del informe, en letra
chica. Estas secciones se leen enteras, sin saltarse párrafos.

| Sección | En un 10-K | En estados chilenos | Qué se busca |
|---|---|---|---|
| Política de ingresos | Nota 1 o 2, Revenue Recognition | Nota de criterios contables, Reconocimiento de ingresos | Cuándo se reconoce, ventas por distribuidores, grado de avance, devoluciones |
| Por qué se movió la caja | MD&A, Liquidity and Capital Resources | Análisis razonado, flujo de efectivo y liquidez | Qué explica el cambio del flujo operacional, línea por línea |
| Riesgos | Item 1A, Risk Factors | Nota de gestión de riesgos y factores de riesgo de la memoria | Frases nuevas respecto del año anterior |
| Cuentas por cobrar | Nota de receivables, Schedule II | Deudores comerciales, con estratificación por mora, cartera repactada y securitizada | Concentración, clientes relacionados, ventas de cartera, movimiento de la provisión |
| Cuentas por pagar | Nota de payables, supplier finance | Cuentas por pagar comerciales, operaciones de confirming | Proveedores pagados por un banco, plazos estirados |
| Partes relacionadas | Related Party Transactions | Saldos y transacciones con entidades relacionadas | Clientes, proveedores y socios que son a la vez dueños o relacionados |
| Adquisiciones y ventas de negocios | Business Combinations, Dispositions | Combinaciones de negocios, Plusvalía, Operaciones discontinuadas | Reservas creadas, pagos contingentes, contratos firmados junto con la operación |
| Provisiones y contingencias | Commitments and Contingencies | Provisiones, Contingencias y restricciones | Juicios, compromisos de compra, covenants |
| Beneficios al personal | Pension, Postretirement Benefits | Beneficios a los empleados | Cambios de tasa de descuento y de otros supuestos actuariales |
| Derivados | Derivatives and Hedging | Instrumentos financieros, coberturas | Ganancias de cobertura fuera de proporción |
| Segmentos | Segment Information | Información por segmentos | Costos cargados a lo que se vende o se discontinúa |
| Operaciones sin caja | Supplemental Cash Flow Information | Nota del flujo de efectivo, transacciones no monetarias | Compras pagadas con pagarés u obligaciones |
| Auditor y control interno | Report of Independent Registered Public Accounting Firm, Item 9A | Informe del auditor independiente, párrafos de énfasis | Salvedades, debilidades, cambio de auditor |
| Métricas de la empresa | Comunicado y presentación | Comunicado, presentación y análisis razonado | Qué encabeza el titular y cómo se define |

### 4. Correr las 15 pruebas

Abre [`forense-pruebas.md`](forense-pruebas.md) y corre las 15, una por una, en su orden. Cada
prueba dice qué se calcula o se lee, cuándo es hallazgo y qué explicación la descarga. Ninguna se
salta porque la tabla de razones no haya avisado. Cuando una señal aparece, el caso del libro que
más se le parece está en [`forense-casos.md`](forense-casos.md) y sirve para medir el tamaño.

### 5. Escribir el anexo y validarlo

El anexo tiene 15 secciones con este formato exacto, una por prueba.

```
## EM 1. Registrar ingresos demasiado pronto

| Campo | Contenido |
|---|---|
| Veredicto | ALTA |
| Qué se revisó | DSO de 5 años (41, 42, 40, 43 y 58 días) y la nota 2 contra la de 2015 |
| Efecto | Las ventas a distribuidores subieron 180 millones, 22 por ciento de la utilidad neta |
| Qué estaría tapando | Una caída de la demanda del usuario final |
| Cita | «texto exacto copiado de la fuente» en fuente/actual.txt |
```

Las reglas del formato son 5.

1. El veredicto es LIMPIO, BAJA, MEDIA, ALTA, CRÍTICA o SIN DATO.
2. «Qué se revisó» nombra las cifras, la nota o la página que se miraron, también en un LIMPIO.
3. Un hallazgo lleva «Efecto», «Qué estaría tapando» y al menos una fila «Cita».
4. La cita es texto copiado tal cual, corto, de una sola frase y sin el carácter `|`. Va una fila
   por cita.
5. Un SIN DATO lleva la fila «Qué falta» en vez de «Qué se revisó».

```
uv run python -I scripts/validar_forense.py analisis/anexo-forense.md
```

El script falla si falta una prueba, si un LIMPIO no dice qué miró, o si una cita no aparece en el
archivo de la fuente. Un hallazgo cuya cita no aparece no entra al informe. Con una fuente en PDF se
corre con `uv run --with pymupdf`.

### 6. Pasar los hallazgos al resto del análisis

Con el anexo en verde, [`fase3-sintesis.md`](fase3-sintesis.md) arma la matriz de cruce y las
preguntas para el gerente de finanzas. Los ajustes entran al paso 5, y el puntaje entra a los pasos
6 y 8.

## Los veredictos

La escala es una convención de Kumo. El libro no da ninguna, y los cortes de 5 y de 20 por ciento
son un supuesto sin medir. Sirven para que 2 personas lleguen al mismo veredicto con la misma
evidencia.

| Veredicto | Puntos | Cuándo corresponde |
|---|---|---|
| LIMPIO | 0 | Se miró lo que la prueba pide y no hay señal, o la señal tiene una explicación comprobada en la fuente |
| BAJA | 1 | Hay señal y su efecto es menor que 5 por ciento de la utilidad neta o del flujo operacional, o no se puede medir |
| MEDIA | 2 | El efecto está entre 5 y 20 por ciento. También una práctica legítima que no se repite y que explica la mayor parte de la mejora del período |
| ALTA | 3 | El efecto es de 20 por ciento o más. También un cambio de política contable o de definición de una métrica, sin explicación, que mejora el resultado |
| CRÍTICA | 4 | El efecto cambia el signo de la utilidad o del flujo operacional. También ingresos o activos sin sustancia, un auditor que no certifica, una reformulación o una investigación interna en curso |
| SIN DATO | No suma | Falta el documento o la cifra. El informe lo dice junto al puntaje |

El efecto se mide contra la utilidad neta en las pruebas EM, contra el flujo operacional en las CF
y en AA 2, y contra la cifra contable equivalente en las KM y en AA 3.

Un hallazgo no exige fraude. El libro insiste en que muchas prácticas son legales y aun así no se
repiten, como vender cuentas por cobrar o estirar el pago a proveedores. Se anotan igual, porque lo
que se mide es cuánto del resultado va a seguir ahí el próximo año.

## El puntaje y su efecto

El puntaje es la suma de los puntos de las 15 pruebas. Los efectos de esta tabla son también
convención de Kumo, sin medir.

| Puntaje | Lectura | En la tasa de descuento del paso 6 | En la pregunta 4 del paso 8 |
|---|---|---|---|
| 0 a 3 | Limpio | No cambia | Aprobada |
| 4 a 7 | Dudas | Suma 2 puntos | Aprobada |
| 8 a 12 | Dudas importantes | Suma 5 puntos | Reprobada |
| 13 o más | Manipulación seria | Suma 8 puntos, y se considera pasar | Reprobada |
| Cualquier CRÍTICA | No se invierte | No aplica | Reprobada |

## Lo que cambia según la empresa

| Si la empresa | Entonces |
|---|---|
| Crece comprando empresas | El flujo operacional no sirve solo. Se usa el flujo de caja libre tras adquisiciones, y las 3 pruebas AA pesan más que las demás |
| Es un banco, una financiera o vende con crédito propio | Mandan la provisión de cartera contra la cartera morosa y la forma en que se presenta |
| Reconoce ingresos por grado de avance o por programa | Mandan los cambios de estimación del avance y los costos acumulados en el balance |
| Vende por distribuidores | Manda saber si reconoce al despachar al distribuidor o cuando este vende |
| Aplica NIIF | No existen partidas extraordinarias y las ganancias de una vez suelen ir en «Otras ganancias (pérdidas)». La NIC 7 deja elegir dónde van los intereses y los dividendos. La NIIF 16 llevó el pago de los arriendos al flujo de financiamiento. Un deterioro se puede reversar, salvo el de la plusvalía |
| Presume de una racha de metas cumplidas | Cada cambio contable del período se mira 2 veces |

## Lo que la revisión no hace

No reemplaza al paso 1, que mira la gobernanza y los incentivos. Los usa. Si el paso 1 encontró un
bono atado a una métrica ajustada, las pruebas KM 1 y AA 3 parten por esa métrica.

No declara un fraude. Declara qué parte del resultado no se entiende o no se repite, con su cita, y
deja la pregunta escrita para quien pueda contestarla.
