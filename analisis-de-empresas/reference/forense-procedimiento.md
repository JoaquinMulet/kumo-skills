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

| Concepto del CSV | De dónde sale | En estados chilenos | En un 10-K |
|---|---|---|---|
| `ingresos`, `costo_ventas`, `utilidad_neta` | Estado de resultados | Ingresos de actividades ordinarias, Costo de ventas, Ganancia atribuible a los propietarios de la controladora. Si la empresa vende con crédito propio y el costo de ventas trae intereses o provisiones de la cartera, `costo_ventas` lleva solo el costo de la mercadería, que la nota abre, para que el DSI y el DPO tengan sentido | Total revenues o Net sales, Cost of sales, Net income de la empresa, sin el interés minoritario |
| `utilidad_operacional` | Estado de resultados | No siempre viene. Se arma como ganancia bruta menos costos de distribución y gastos de administración | Operating income o Income from operations |
| `flujo_operacional`, `capex`, `adquisiciones`, `dividendos` | Estado de flujo de efectivo | Flujos de actividades de operación, Compras de propiedades, planta y equipo, Flujos para obtener el control de subsidiarias, Dividendos pagados | Net cash provided by operating activities, Capital expenditures, Acquisitions net of cash acquired, Dividends paid |
| `cuentas_por_cobrar`, `provision_incobrables` | Balance y nota de cuentas por cobrar | Deudores comerciales y otras cuentas por cobrar, corrientes y no corrientes, y su deterioro. La parte no corriente puede estar en «Otros activos financieros, no corrientes». Lo que la nota ya cuenta dentro de la línea, como los cheques por cobrar, no se suma otra vez en `documentos_por_cobrar` | Accounts receivable, net, y Allowance for doubtful accounts |
| `cuentas_por_cobrar_vendidas` | Nota de cuentas por cobrar | Cartera cedida, securitizada o en factoring que sigue pendiente y que salió del balance. Si la empresa consolida al patrimonio separado o al vehículo que la compró, la cartera sigue en el balance y no va aquí, porque se contaría 2 veces | Receivables sold, factored o securitized que siguen pendientes y salieron del balance. Si el vehículo consolida, no van |
| `documentos_por_cobrar` | Balance y notas | Documentos por cobrar, pagarés y letras de clientes | Notes receivable, y todo saldo por cobrar a clientes guardado en otra línea, como efectivo. Los cobros de tarjetas en tránsito no van |
| `inventario`, `inventario_largo_plazo` | Balance y nota de inventarios | Inventarios corrientes y no corrientes | Inventories, y el inventario que esté dentro de Other assets |
| `cuentas_por_pagar` | Balance | Cuentas por pagar comerciales y otras cuentas por pagar | Accounts payable |
| `ingreso_diferido` | Balance y notas | Ingresos diferidos, suele estar en Otros pasivos no financieros | Deferred revenue o Unearned revenue |
| `pasivos_blandos` | Balance y su nota | Otras provisiones más Otros pasivos no financieros, sin el ingreso diferido, sin los dividendos por pagar (también el dividendo mínimo legal) y sin el precio pendiente de una compra de empresa | Accrued expenses más Other current liabilities, sin impuestos por pagar, ingreso diferido, dividendos por pagar ni precio pendiente de una compra. Si la nota no abre la línea, va entera y se dice |
| `activos_blandos` | Balance | Otros activos no financieros, gastos anticipados, costos diferidos | Prepaid expenses and other current assets más Other assets |
| `cartera_morosa`, `provision_cartera` | Notas de una financiera o de quien vende con crédito propio | Cartera con mora o deteriorada (la suma de los tramos vencidos de la estratificación), y su provisión | Nonaccrual o nonperforming loans, y Allowance for loan losses |
| `cartera_repactada` | Las mismas notas | Cartera repactada, renegociada o refinanciada, si la nota la da | Modifications to borrowers experiencing financial difficulty, antes Troubled debt restructurings |
| `utilidad_antes_impuestos`, `impuestos` | Estado de resultados | Ganancia antes de impuestos, Gasto por impuestos a las ganancias | Income before income taxes, Provision for income taxes |
| `dias` | Largo del período | Los días reales. 365 en un año, 371 en un año de 53 semanas, 91.25 en un trimestre | Igual |

Las reglas de la tabla son 5.

1. Si la empresa no tiene un concepto, porque no paga dividendos o no tiene costo de ventas, la
   fila no va. Si lo tiene y ese período vale 0, como un año sin compras de empresas, va 0. Los
   dividendos son solo los pagados en efectivo. Un dividendo pagado en acciones no va.
2. Si el informe actual cambió cifras de años ya publicados, se usan las del informe más nuevo, y
   el cambio se anota como señal para KM 2.
3. Los años que el informe actual no trae se sacan del informe anterior. Con 2 informes anuales
   salen 3 años de balance y 4 o 5 de resultados y de flujo.
4. Con un informe trimestral, los resultados y el flujo se comparan con el mismo trimestre del año
   anterior, que el informe trae. Un CSV no mezcla columnas de un trimestre con columnas de un año,
   porque las razones que dividen por ingresos dejan de ser comparables. Si hacen falta los 2, van
   en 2 CSV. El balance solo se puede comparar con el cierre del año anterior.
   Las razones de balance mezclan entonces la temporada, y un aviso que salga de ahí se anota con
   esa advertencia.
5. Si hay un informe trimestral más nuevo que el anual, la revisión es del anual y su CSV es
   `cifras.csv`. El trimestral se compara con el anual en la acción 2, y sus cifras van en un CSV
   aparte, `cifras-trimestre.csv`, con el mismo trimestre del año anterior.

El script entrega las razones y una lista de avisos. Un aviso dice qué pruebas abrir primero. No es
un hallazgo, porque la tabla no ve las notas.

### 2. Comparar el informe con el del período anterior

Es la técnica que el libro más recomienda. Una empresa cambia la redacción de una nota solo cuando
algo cambió.

```
uv run python -I scripts/comparar_notas.py fuente/anterior.txt fuente/actual.txt --max 80
```

El script lista las frases que cambiaron, las nuevas y las que desaparecieron, sin contar las que
solo cambiaron sus cifras. Sin opciones muestra solo las que tocan temas contables, y aun así en un
informe entero salen entre 30 y 250 por lista. Esa primera corrida sirve para ver el tamaño del
cambio y leer por encima las que CAMBIARON. El trabajo se hace después, prueba por prueba, acotando
con `--contiene` y los términos que da cada una en [`forense-pruebas.md`](forense-pruebas.md).
Una política que cambió sin cambiar de redacción no aparece aquí. Por eso la acción 3 manda leer
las secciones completas. Tampoco aparece una tabla o una columna que se dejó de publicar, porque el
script compara frases. Las tablas de la nota de cuentas por cobrar se comparan a mano, una por una.

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

Las reglas del formato son 7.

1. El veredicto es LIMPIO, BAJA, MEDIA, ALTA, CRÍTICA o SIN DATO.
2. «Qué se revisó» nombra las cifras, la nota o la página que se miraron, también en un LIMPIO.
   Un LIMPIO no necesita cita.
3. Un hallazgo lleva «Efecto», «Qué estaría tapando» y al menos una fila «Cita».
4. La cita es texto copiado tal cual, corto, de una sola frase y sin el carácter `|`. Va una fila
   por cita. Se copia con sus espacios y sus símbolos, y se prueba antes con
   `scripts/buscar_en_fuente.py --cita`.
5. Un SIN DATO lleva la fila «Qué falta» en vez de «Qué se revisó».
6. SIN DATO es para cuando falta el documento que el paso principal de la prueba necesita. Si el
   paso principal se pudo hacer y faltó un documento de apoyo, la prueba lleva su veredicto y
   «Qué se revisó» dice qué no se pudo mirar.
7. Una práctica que se ve desde 2 pruebas se anota en las 2, y suma una sola vez. La venta de
   cuentas por cobrar, por ejemplo, se anota en CF 1 y también en KM 2, porque baja el DSO. La
   práctica se cuenta en la prueba donde su veredicto es más alto, que suele ser la prueba donde
   se pudo medir. Si empatan, se cuenta en la de menor número en el orden del anexo. Las demás
   llevan la fila «Misma práctica que» con ese código, y no suman. Si una prueba reúne varias
   prácticas, su veredicto es el de la más grave que no esté contada en otra prueba, y la fila
   «Misma práctica que» se usa solo cuando todo lo que sostiene el veredicto ya está contado allá.
   El validador marca en rojo una prueba con «Misma práctica que» cuyo veredicto es más alto que
   el de la prueba que nombra.

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

La escala es una convención de Kumo. El libro no da ninguna. Los cortes de 5 y de 20 por ciento son
un supuesto sin medir. Los puntos y los tramos se ajustaron con una prueba de campo sobre 7 informes
reales, el 27 de noviembre de 2026. Sirven para que 2 personas lleguen al mismo veredicto con la
misma evidencia.

| Veredicto | Puntos | Cuándo corresponde |
|---|---|---|
| LIMPIO | 0 | Se miró lo que la prueba pide y no hay señal, o la señal tiene una explicación con cifras que se comprobó en la fuente |
| BAJA | 0 | Hay señal y su efecto es menor que 5 por ciento, o no se puede medir. Es una observación menor. Queda anotada y no suma |
| MEDIA | 2 | El efecto está entre 5 y 20 por ciento. También una práctica legítima que explica la mayor parte de la mejora del período, cuando la empresa no dice que se vaya a repetir |
| ALTA | 3 | El efecto es de 20 por ciento o más. También un cambio de política contable o de definición de una métrica, sin explicación, que mejora una cifra que la empresa reporta o destaca. También una investigación abierta por un regulador o un fiscal sobre la contabilidad o la divulgación de la empresa, confirmada por un documento de la empresa o del regulador. Una demanda de accionistas no cuenta como investigación, y va como BAJA. También dejar de publicar, sin explicación, una métrica o una apertura que el informe anterior traía y que mide el riesgo principal del negocio, como la mora por tramos de quien presta |
| CRÍTICA | 4 | El efecto cambia el signo de la utilidad o del flujo operacional. También ingresos o activos sin sustancia, un auditor que no certifica, una reformulación o una investigación interna en curso sobre la contabilidad, la divulgación o el control interno. Una investigación interna sobre otro tema, como la conducta de un ejecutivo, va al paso 1 |
| SIN DATO | No suma | Falta el documento o la cifra. El informe lo dice junto al puntaje |

Cuando 2 filas calzan, manda la más alta. Un cambio de política sin explicación es ALTA aunque su
efecto no se pueda medir, porque el libro trata el cambio mismo como la señal. Esa excepción vale
solo para un cambio real en cómo se reconoce, se clasifica o se define una cifra, y para una métrica
o una apertura del riesgo principal que se dejó de publicar. Cualquier otra señal que no se puede
medir es BAJA. Una explicación de la empresa que no trae cifras no baja el
veredicto. Queda anotada en «Qué se revisó».

Esa regla tiene 5 límites, que salieron de las pruebas a ciegas del 27 de noviembre de 2026.

1. Un cambio que empeora la cifra, o que no mueve ninguna cifra consolidada, como un traslado de
   costos entre segmentos con el total igual, es BAJA. Pasa a MEDIA solo si cambia el signo del
   crecimiento del segmento que trae más ingresos, porque eso tapa el deterioro de lo principal
   del negocio.
2. Una política que aparece escrita por primera vez no es un cambio. Lo es si contradice lo que el
   informe anterior decía de esa misma práctica.
3. Un hecho posterior al cierre, como un acuerdo, una venta o una demanda presentada después, no se
   mide contra el período que se revisa. Se anota en «Qué estaría tapando» como dato para
   proyectar. Un hecho anunciado dentro del período y que se cierra después sí cuenta. Una
   investigación de un regulador o un fiscal no se mide, así que este límite no la toca. Cuenta si
   está abierta a la fecha del análisis, aunque haya empezado después del cierre, cuando la
   confirma un documento de la empresa o del regulador (un hecho esencial, un 8-K, un 10-Q, un
   comunicado del regulador). Si solo la informa la prensa, es BAJA y va a las preguntas para el
   gerente de finanzas.
4. 2 cambios en la misma nota y con el mismo efecto, como 2 frases nuevas en la política de
   ingresos, son una sola práctica. Van en una prueba, y la otra lleva «Misma práctica que».
5. Una clasificación que la norma deja elegir, como la de los intereses en la NIC 7, no es un
   cambio si el informe la aplica igual a los 2 años y también la aplicaba así el informe
   anterior. Se usa para dejar comparable la cifra y es BAJA, sea cual sea su tamaño. Si el
   informe anterior la aplicaba de otra forma, es un cambio de clasificación y sigue la escala.
   En los principios de Estados Unidos (ASC 230) casi no hay elección. Los intereses pagados van en
   la operación, y las retenciones de impuestos por acciones entregadas a empleados van en
   financiamiento. Una clasificación que la norma fija no es hallazgo, y la prueba queda LIMPIO.
   Lo que dice si cambió es el informe anterior, aunque el nuevo haya rehecho las cifras del año
   anterior con la clasificación nueva. El CSV lleva las cifras del informe nuevo (regla 2 de la
   tabla), y el flujo comparable con los intereses adentro va en «Efecto».

El efecto se mide contra una cifra distinta según la prueba.

| Prueba | Se mide contra |
|---|---|
| EM 1 a EM 7 y AA 1 | La utilidad neta del período |
| CF 1, CF 2 y AA 2 | El flujo operacional del período |
| CF 3 | El flujo operacional del período. Se mide cuánto de él viene de las líneas de capital de trabajo cuyos días mejoraron |
| KM 1 y AA 3 | La cifra contable de lo mismo que mide la métrica. Para un EBITDA, la utilidad operacional más la depreciación y la amortización |
| KM 2 | Lo que el indicador mide, como los días del DSO, la provisión o la deuda |
| Obligaciones fuera de balance que funcionan como deuda, en cualquier prueba | La deuda financiera del balance |
| Un efecto antes de impuestos, como una provisión revertida | La utilidad antes de impuestos |

Si la empresa pierde plata, o su utilidad neta es menor que 1 por ciento de los ingresos, la
utilidad neta no sirve de vara, porque todo queda bajo 5 por ciento o sobre 20 según el año. El
efecto se mide entonces contra los ingresos totales del mismo período que el efecto, con cortes de
0,5 y de 2 por ciento. Son los órdenes de
magnitud con que la auditoría fija su materialidad, y aquí son también un supuesto sin medir. Lo
mismo vale para las pruebas que se miden contra el flujo operacional cuando ese flujo es negativo o
casi cero. Un efecto que cae en otro período, como un gasto que se evita el año siguiente, se mide
contra la cifra del período en que cae si el informe la trae. Si no la trae, queda BAJA con su
monto anotado.

La cifra de comparación es la del período del documento donde aparece el hallazgo. Una garantía
revelada en el informe anual se mide contra la deuda del balance de ese informe, aunque haya un
trimestral más nuevo con otra deuda. Un hallazgo que aparece solo en el trimestral se mide contra
las cifras de ese trimestre, que salen de `cifras-trimestre.csv`.

Un hallazgo no exige fraude. El libro insiste en que muchas prácticas son legales y aun así no se
repiten, como vender cuentas por cobrar o estirar el pago a proveedores. Se anotan igual, porque lo
que se mide es cuánto del resultado va a seguir ahí el próximo año.

## El puntaje y su efecto

El puntaje suma 2 puntos por cada MEDIA, 3 por cada ALTA y 4 por cada CRÍTICA. Una BAJA no suma. Una
prueba que dice «Misma práctica que» otra tampoco, porque esa práctica ya se contó. Los efectos de
esta tabla son también convención de Kumo, sin medir.

| Puntaje | Lectura | En la tasa de descuento del paso 6 | En la pregunta 4 del paso 8 |
|---|---|---|---|
| 0 a 2 | Limpio | No cambia | Aprobada |
| 3 a 6 | Dudas | Suma 2 puntos | Aprobada |
| 7 a 11 | Dudas importantes | Suma 5 puntos | Reprobada |
| 12 o más | Manipulación seria | Suma 8 puntos, y se considera pasar | Reprobada |
| Cualquier CRÍTICA | No se invierte | No aplica | Reprobada |

Junto al puntaje, el informe dice siempre cuántas observaciones menores hubo y qué pruebas quedaron
sin dato. En la prueba de campo, la empresa de control quedó en 0 puntos y los 6 casos del libro
quedaron entre 3 y 9.

## Lo que cambia según la empresa

| Si la empresa | Entonces |
|---|---|
| Crece comprando empresas | El flujo operacional no sirve solo. Se usa el flujo de caja libre tras adquisiciones, y las 3 pruebas AA pesan más que las demás |
| Es un banco, una financiera o vende con crédito propio | Mandan la provisión de cartera contra la cartera morosa, la cartera repactada y la forma en que se presentan. La nota de cuentas por cobrar se lee entera en los 2 informes y se compara tabla por tabla. Si el informe dejó de traer una apertura que traía el anterior (tramos de mora, provisión por tramo, cartera repactada), es un cambio de presentación de KM 2 y es ALTA aunque no se pueda medir, porque el libro trata como señal dejar de publicar una métrica justo cuando empeora. Aplicar las tasas de la apertura vieja a los saldos nuevos no lo descarga, porque lo que está en duda son los saldos. Lo descarga solo una explicación con cifras, como un cambio de norma que el informe nombre. Si ninguno de los 2 informes cuantifica la cartera repactada, se anota en «Qué se revisó» de EM 4 y va a las preguntas para el gerente de finanzas |
| Reconoce ingresos por grado de avance o por programa | Mandan los cambios de estimación del avance y los costos acumulados en el balance |
| Vende por distribuidores | Manda saber si reconoce al despachar al distribuidor o cuando este vende |
| Aplica NIIF | No existen partidas extraordinarias y las ganancias de una vez suelen ir en «Otras ganancias (pérdidas)». La NIC 7 deja elegir dónde van los intereses y los dividendos. Desde 2019 la NIIF 16 lleva los arriendos al balance y su pago al flujo de financiamiento. Antes, con la NIC 17, un arriendo operativo no pasa por el balance ni por el flujo de financiamiento, y su compromiso está en la nota. Un deterioro se puede reversar, salvo el de la plusvalía |
| Su informe anterior es el de la primera adopción de las NIIF, o uno preliminar o pro forma | Las cifras del año anterior salen del informe actual (regla 2 de la tabla). Un cambio de política o de clasificación frente al informe preliminar cuenta igual que cualquier otro, y lo descarga solo la nota de adopción con cifras. Las cifras comparativas que cambiaron se anotan en KM 2 |
| Presenta el flujo por el método directo | La descomposición de CF 3 se arma con la variación de los saldos del balance, si el informe no trae la conciliación con la utilidad, y «Qué se revisó» lo dice |
| Presume de una racha de metas cumplidas | Cada cambio contable del período se mira 2 veces |
| Pierde plata o gana muy poco | El efecto se mide contra los ingresos, como dice la sección de veredictos |
| Vende al contado, con poco margen y mucha rotación | Las pruebas de ingresos dan poca señal. Mandan las de inventario, proveedores y flujo |

## Lo que la revisión no hace

No reemplaza al paso 1, que mira la gobernanza y los incentivos. Los usa. Si el paso 1 encontró un
bono atado a una métrica ajustada, las pruebas KM 1 y AA 3 parten por esa métrica.

No declara un fraude. Declara qué parte del resultado no se entiende o no se repite, con su cita, y
deja la pregunta escrita para quien pueda contestarla.
