# Las 15 pruebas de la revisión forense

Se corren todas, en este orden. Cada una termina en un veredicto para el anexo, con la escala de
[`forense-procedimiento.md`](forense-procedimiento.md). Los términos de búsqueda van en español y en
inglés, y se usan con `scripts/comparar_notas.py --contiene` o con `scripts/buscar_en_fuente.py
--contar`. Los casos que sirven de vara están en [`forense-casos.md`](forense-casos.md).

Las 7 primeras miran la utilidad. EM 1 a EM 5 la inflan hoy. EM 6 y EM 7 la guardan para mañana, y
aparecen en empresas que quieren verse parejas o que estrenan gerente.

## EM 1. Registrar ingresos demasiado pronto

El ingreso es real y se reconoce antes de ganarlo. La venta se gana cuando el producto se entregó y
el cliente lo aceptó, y la firma de un contrato no gana nada.

Qué se hace.

1. Mira el DSO de cada período en la tabla de razones, calculado con el saldo final. Suma las
   cuentas por cobrar de largo plazo y las no facturadas.
2. Compara la nota de reconocimiento de ingresos con la del período anterior, palabra por palabra.
   Términos. `se reconoce`, `reconocimiento de ingresos`, `grado de avance`, `despacho`, `entrega`,
   `consignación`, `distribuidor`, `plazo`, `recognized`, `revenue recognition`, `shipment`,
   `delivery`, `percentage-of-completion`, `bill-and-hold`, `consignment`, `distributor`,
   `sell-through`, `payment terms`, `extended`.
3. Busca en el análisis de la gerencia y en la conferencia si se dieron plazos de pago más largos o
   financiamiento al cliente.
4. Revisa si la fecha de cierre del período es la de siempre.

Es hallazgo cuando el DSO sube sin que la empresa lo explique, cuando la política pasó a reconocer
antes (del despacho en vez de la entrega, del distribuidor en vez del usuario final, o un cambio a
grado de avance), cuando cambió una estimación del grado de avance y eso sumó ingresos, o cuando
aparecen ventas facturadas sin despachar, en consignación o con plazos nuevos.

Lo descarga un cambio de mezcla de clientes o de países que la nota explica con cifras, o una
adquisición que trajo cuentas por cobrar y que se puede separar.

Vara. Trex pasó de 18 a 70 días en 2 años. Computer Associates subió 20 días en un año hasta 247.
Keurig cambió 2 frases de su nota. Ulvac habría caído 21 por ciento sin su cambio de política.

## EM 2. Registrar ingresos falsos

El ingreso no existe o está inflado. La operación tiene forma de venta y no tiene sustancia.

Qué se hace.

1. Lee completa la nota de partes relacionadas y la de concentración de clientes. Anota qué parte de
   los ingresos y de las cuentas por cobrar viene de la matriz, de socios, de proveedores o de
   entidades relacionadas.
2. Compara el crecimiento de los ingresos con el de la utilidad y mira el margen neto en la tabla de
   razones.
3. Busca operaciones en que la plata va y vuelve con la misma contraparte. Términos. `permuta`, `no
   monetaria`, `recompra`, `relacionada`, `negocio conjunto`, `barter`, `nonmonetary`, `repurchase`,
   `related party`, `joint venture`, `reciprocal`.
4. Revisa si la empresa registra el total de la operación o solo su comisión. Términos. `agente`,
   `principal`, `bruto`, `neto`, `gross`, `net basis`.
5. Mira si dentro de los ingresos hay ganancias por venta de activos, intereses o descuentos de
   proveedores.

Es hallazgo cuando un cliente relacionado explica una parte importante del crecimiento y sus cuentas
no se cobran, cuando hay ventas sin dinero cuyo monto fija la propia empresa, cuando la empresa
recompra a su cliente, o cuando los ingresos crecen mucho más rápido que cualquier competidor con un
margen mínimo. Lo último es la prueba de Enron. Un crecimiento sin precedente en la industria se
presume falso.

Lo descarga que la venta a la relacionada se cobre en plazo normal y a precio de mercado, con la
caja a la vista en el flujo operacional.

Vara. Hanergy le vendía a su matriz y su DSO llegó a 500 días. Groupon registraba en bruto y sus
ingresos estaban inflados en más de 100 por ciento. comScore sumó 5 por ciento de ventas con trueque.

## EM 3. Inflar la utilidad con algo de una sola vez

La utilidad sube por un evento que no se repite, o por cómo se ordenaron las líneas.

Qué se hace.

1. Compara el crecimiento de la utilidad operacional con el de los ingresos y el del margen bruto.
   Si la utilidad operacional crece mucho más y el margen bruto no lo explica, busca la ganancia.
2. Lee la nota de otros ingresos y gastos, y el detalle de los gastos de administración y ventas.
   En NIIF mira «Otras ganancias (pérdidas)» y «Otros ingresos, por función».
3. Cuenta en cuántos de los últimos 5 a 10 años hubo cargos de reestructuración o «no recurrentes».
4. Si hay una operación discontinuada, compara los costos que se le asignan ahora con los que tenía
   como segmento un año antes.
5. Si la empresa vendió un negocio y firmó a la vez un contrato de suministro o de servicios con el
   comprador, lee la revelación de las 2 partes.
6. Mira cuántas filiales se consolidan con poco más de 50 por ciento y el tamaño del interés
   minoritario.
7. Compara el crecimiento de la utilidad antes de impuestos con el de la utilidad neta, y la tasa
   efectiva de impuestos con la del período anterior. Lee la conciliación de la tasa en la nota de
   impuestos.

Es hallazgo cuando una ganancia por venta de un activo o un negocio está dentro de una línea
operacional, cuando los cargos «de una vez» aparecen casi todos los años, cuando la unidad que sale
absorbe más costos que antes, o cuando un contrato firmado junto con la venta convierte precio de
venta en ingresos futuros. También cuando la utilidad neta crece más que la utilidad antes de
impuestos por una baja de la tasa que no se repite, como un beneficio tributario de una vez.

Lo descarga que la ganancia esté en una línea propia, bajo la utilidad operacional, y explicada.

Vara. IBM mostró en 1999 un alza de 30 por ciento de su utilidad operacional con ventas que crecían
7 por ciento. Sin la ganancia escondida en gastos, caía 14 por ciento. Whirlpool tuvo cargos de
reestructuración en 23 de 27 años.

## EM 4. Trasladar gastos de hoy al futuro

Un gasto del período queda en el balance como activo, o un activo que perdió valor no se castiga.

Qué se hace.

1. Mira en la tabla de razones el flujo de caja libre contra el flujo operacional, el capex sobre
   ingresos, los activos blandos, el DSI y las 2 provisiones.
2. Recorre el balance buscando cuentas de activo nuevas, con nombre raro o que crecen más que las
   ventas. Términos. `costos diferidos`, `anticipos`, `gastos pagados por anticipado`, `activados`,
   `capitalizados`, `deferred`, `prepaid`, `capitalized`, `advances`, `deposits`.
3. Compara las vidas útiles y los plazos de amortización con los del período anterior. Términos.
   `vida útil`, `useful life`, `useful lives`, `amortization period`.
4. Mira el gasto por obsolescencia y la provisión de incobrables como proporción de su saldo. En una
   financiera, la provisión contra la cartera morosa y la cartera repactada.
5. En NIIF revisa los costos de desarrollo activados (NIC 38) como proporción del gasto total en
   desarrollo.

Es hallazgo cuando el flujo de caja libre cae mientras el flujo operacional sube, cuando el capex
sube contra lo que la propia empresa anunció, cuando un costo pasó de gasto a activo, cuando una
vida útil se alargó, cuando el inventario crece más que las ventas esperadas, o cuando una provisión
baja mientras su saldo sube. Si bajan varias provisiones a la vez, la señal es de las más fuertes
del libro.

Lo descarga un programa de inversión anunciado antes y que se ve en capacidad nueva, o una baja de
provisión respaldada por una caída de la mora que la nota muestra.

Vara. WorldCom pasó de 2.289 a 3.818 negativos de flujo de caja libre mientras su utilidad se veía
sana. AOL tenía activados costos de marketing por 33 por ciento de sus activos. Vitesse provisionó
2,2 millones contra 49,9 del año anterior. New Century bajó su cobertura de 29,5 a 23,4 por ciento.

## EM 5. Esconder gastos o pérdidas por otras vías

El gasto no se registra, se registra por menos, o se compensa con una reserva vieja.

Qué se hace.

1. Mira en la tabla de razones los pasivos blandos sobre ingresos y la diferencia entre flujo
   operacional y utilidad.
2. Compara, trimestre a trimestre si se puede, los gastos de administración y ventas. Un trimestre
   malo con gastos que bajan de golpe pide explicación.
3. Lee el movimiento de cada provisión (garantías, reestructuración, juicios, bonos). Términos.
   `reverso`, `reversa`, `liberación`, `reversal`, `release`, `reversed`, `accrual`.
4. Lee la nota de beneficios al personal y compara la tasa de descuento, la mortalidad, el alza de
   sueldos y la fecha de medición con las del período anterior.
5. Busca entradas de caja o créditos desde proveedores. Términos. `descuentos de proveedores`,
   `rebates`, `vendor credits`, `allowances`.
6. Lee la nota de compromisos y contingencias y anota lo que no está en el balance.
7. En arriendos como arrendador, mira el valor residual estimado.

Es hallazgo cuando una provisión se revierte contra resultados, cuando un supuesto actuarial cambió
y bajó el gasto, cuando un proveedor le paga a la empresa, cuando el ingreso por pensiones explica
buena parte de la utilidad operacional, o cuando hay compromisos fuera de balance de tamaño
comparable a la deuda.

Lo descarga que la reversión esté revelada en su propia línea y que la empresa la excluya de sus
cifras recurrentes.

Vara. Under Armour revirtió 48 millones de bonos en un trimestre y lo dijo en una nota al pie sobre
estacionalidad. Lucent sacó 91 por ciento de su utilidad operacional de su plan de pensiones. Deere
subió su valor residual de 55 a 63 por ciento.

## EM 6. Guardar ingresos de hoy para el futuro

La empresa reporta menos de lo que ganó para verse pareja y tener de dónde sacar después.

Qué se hace.

1. Sigue el ingreso diferido trimestre a trimestre, con su saldo inicial, sus adiciones y su uso.
2. Compara la volatilidad de la utilidad con la del entorno del negocio (tasas, precios, ciclo).
3. Lee la nota de derivados. Compara la ganancia de cobertura con la pérdida de lo cubierto.
4. Si la empresa compró otra, mira los ingresos de la adquirida en sus últimos meses por separado.

Es hallazgo cuando el ingreso diferido crece mucho más que las ventas en un período muy bueno y
después deja de crecer, cuando la utilidad es mucho más pareja que el negocio, cuando una cobertura
gana varias veces lo que pierde lo cubierto, o cuando los ingresos de la adquirida se desploman
justo antes del cierre de la compra.

Lo descarga un cambio en la forma de vender, como pasar a suscripciones, que la empresa haya
anunciado y que explique el ingreso diferido.

Vara. La adición neta de ingresos no devengados de Microsoft pasó de 643 millones a 44 y después a
110 negativos. U.S. Robotics registró 15 millones en 2 meses contra 690 del trimestre anterior.

## EM 7. Traer gastos del futuro al presente

Se carga hoy todo lo posible, bajo la línea, para que los períodos siguientes queden livianos.

Qué se hace.

1. Lee el detalle de cada cargo especial del período. Separa lo que es de verdad de una vez de lo
   que es un gasto normal (publicidad, inventario, estudios).
2. Mira si el cargo coincide con un gerente general nuevo, con una crisis de mercado o con una
   adquisición.
3. Sigue el movimiento de la reserva de reestructuración. Mira cuánto se usó y cuánto se revirtió.
4. Mira los márgenes de los períodos siguientes a un cargo grande, y si después se vendió
   inventario que estaba castigado.
5. En NIIF revisa las reversiones de deterioro.

Es hallazgo cuando un cargo incluye gastos corrientes, cuando la reserva se revierte, cuando los
márgenes saltan justo después del cargo, cuando hay reservas genéricas o por «riesgos» sin
identificar, o cuando hay reestructuraciones todos los años.

Lo descarga un cierre real de plantas o tiendas, con sus fechas y su gente, que se pueda contrastar.

Vara. Sunbeam multiplicó su utilidad operacional de 4 a 133 millones después de su cargo, mientras
sus cuentas por cobrar subían 59 por ciento y su flujo operacional empeoraba. NVIDIA vendió 51
millones de inventario que había castigado.

## CF 1. Pasar entradas de financiamiento a la operación

La plata viene de un banco y se muestra como si viniera del negocio.

Qué se hace.

1. Mira la línea de cuentas por cobrar del flujo operacional, período contra período. Un giro grande
   se explica.
2. Busca ventas o cesiones de cuentas por cobrar y anota el saldo vendido que sigue pendiente al
   cierre. Va al CSV como `cuentas_por_cobrar_vendidas`. El ajuste del flujo usa la variación de
   ese saldo entre un cierre y el siguiente, no el total vendido en el año. Términos. `factoring`, `securitización`,
   `cesión`, `con responsabilidad`, `securitization`, `factored`, `sold`, `recourse`, `transferred`.
3. Compara los factores de riesgo con los del período anterior.
4. Busca ventas con pacto de recompra a un banco o a una entidad que la empresa controla.
5. En NIIF anota dónde clasifica la empresa los intereses y los dividendos (NIC 7) y deja el flujo
   operacional comparable antes de usarlo.

Es hallazgo cuando el flujo operacional mejoró por vender cuentas por cobrar, cuando la venta
conserva el riesgo de no pago y aun así se muestra en la operación, o cuando una «venta» de
inventario a un banco tiene recompra. Con la venta sin riesgo retenido la práctica es legítima, y
se anota como mejora que no se repite.

Se calcula el flujo operacional sin la variación del saldo vendido, y ese es el número que sigue.

Lo descarga un programa de venta de cartera estable, con un saldo vendido que no cambia de un
período a otro.

Vara. Sanmina mostró 175 millones de flujo operacional en un trimestre y 139 venían de vender
cuentas. Delphi registró como venta un préstamo de 200 millones, y su flujo real del año era 68.

## CF 2. Sacar salidas de caja de la operación

Un costo de operar se muestra como inversión o como pago de deuda.

Qué se hace.

1. Lee la sección de inversión línea por línea. Marca toda salida que suene a costo del negocio
   (contenido, licencias, derechos, contratos, clientes).
2. Lee la sección de financiamiento. Busca pagos de arriendos y de deuda con proveedores que
   reemplazan un gasto. En NIIF 16 todos los arriendos van ahí, así que se resta el pago de arriendos
   para comparar con años anteriores o con empresas bajo otra norma.
3. Lee la información complementaria de operaciones sin caja y busca compras pagadas con pagarés.
4. Compara la clasificación con la de un competidor.
5. Busca clientes que a la vez reciben pagos o compromisos de inversión de la empresa.

Es hallazgo cuando una compra que se repite todos los años y sirve para operar está en inversión,
cuando un gasto pasó a ser arriendo financiero o deuda, o cuando lo que se le cobra a un cliente
entra por operación y lo que se le paga sale por inversión.

Se calcula el flujo operacional con esas salidas adentro, y el flujo de caja libre, que resiste
este truco.

Lo descarga que la partida sea de verdad un activo que dura años y no se repone todos los períodos.

Vara. Netflix mostraba 292 millones de flujo operacional y 68 con el criterio de Blockbuster. El de
Cephalon pasaba de 179 positivos a 350 negativos al restar los derechos que compraba.

## CF 3. Inflar el flujo operacional con algo que no se repite

La caja mejoró por el capital de trabajo o por un cobro único. Es legítimo. Lo que se mide es
cuánto de la mejora va a seguir.

Qué se hace.

1. Descompón el cambio del flujo operacional en utilidad, cuentas por pagar, inventario, cuentas
   por cobrar, anticipos de clientes e impuestos. El efecto se mide con esa descomposición, como
   la parte de la mejora que explican las líneas de capital de trabajo. El DPO de la tabla de
   razones confirma la dirección y no sirve para medir.
2. Lee la explicación de la gerencia sobre el flujo. Términos. `capital de trabajo`, `proveedores`,
   `confirming`, `anticipos`, `working capital`, `payables`, `days payable`, `early payment`,
   `deposits`, `supplier finance`.
3. Busca deuda de corto plazo usada para pagar a proveedores.
4. Por cada ganancia de una vez del estado de resultados, pregunta dónde quedó en el flujo.

Es hallazgo cuando la mayor parte de la mejora viene de pagar más tarde, cobrar antes o comprar
menos inventario, cuando un banco paga a los proveedores, o cuando un cobro único está dentro del
flujo operacional sin línea propia.

Si el flujo operacional no mejoró, no hay mejora que explicar y la prueba queda en LIMPIO, salvo
que un cobro único esté sosteniendo un flujo que sin él habría caído más.

Lo descarga un cambio permanente de condiciones con proveedores que se mantiene los años siguientes.

Vara. Home Depot subió su flujo operacional de 2.796 a 5.963 millones, y 2.233 de esos 3.167 venían
de cuentas por pagar, pasivos acumulados e inventario, según su informe de ese año. Al año siguiente cayó a 4.802. En Tesla, 88 por ciento de la
mejora de 2016 eran depósitos de clientes.

## KM 1. Exhibir métricas que exageran el desempeño

La empresa dirige la atención a una cifra que ella misma define.

Qué se hace.

1. Lista cada métrica que el comunicado destaca y copia su definición. Compárala con la del período
   anterior y con la de un competidor. Sin comunicado, se usan las métricas que destaca la
   explicación de la gerencia, y «Qué se revisó» dice que faltó el comunicado.
2. Arma, para varios años, la diferencia entre la utilidad ajustada y la utilidad neta, y entre la
   métrica de caja de la empresa y el flujo de caja libre.
3. Lee qué se excluye. Marca lo que es un costo normal del negocio o lo que aparece todos los años.
4. Si la métrica es de ventas comparables, calcula el ingreso por tienda y compara las 2 tendencias.
5. Si la empresa informa pedidos o cartera, comprueba que cartera inicial más pedidos netos menos
   ingresos dé la cartera final.
6. Compara los dividendos con el flujo de caja libre, que ya está en la tabla de razones.

Es hallazgo cuando la definición cambió, cuando la métrica ajustada es siempre mucho mejor que la
contable, cuando excluye costos que se pagan en efectivo todos los períodos, cuando una partida se
incluye un período y se excluye al siguiente, o cuando la empresa reparte más que su flujo de caja
libre. La prueba que propone el libro es formular qué pregunta responde la métrica y juzgar si esa
pregunta sirve.

Lo descarga una conciliación completa con la cifra contable, con exclusiones que de verdad no se
repiten.

Vara. Valeant sumó 9.600 millones de «cash earnings» en 4 años con una pérdida contable de 2.700.
Linn repartió más que su flujo distribuible con un flujo de caja libre de 694 millones negativos.

## KM 2. Distorsionar las métricas del balance

Una cuenta que iba a delatar el problema se baja, se mueve o se mide de otra forma.

Qué se hace.

1. Mira si el DSO cayó de golpe después de subir. Calcula el DSO ajustado, con las cuentas vendidas
   y los documentos por cobrar.
2. Busca cuentas por cobrar fuera de la línea comercial (documentos, letras, «otras»), también
   dentro de efectivo y equivalentes. Lo que aparezca va al CSV como `documentos_por_cobrar`.
3. Busca inventario fuera de la línea de inventarios, en no corrientes o en otros activos.
4. Revisa si la empresa cambió la forma de calcular o de presentar un indicador, o estrenó uno
   justo cuando el habitual empeoraba.
5. En una financiera, compara cómo se presenta la provisión en el comunicado con cómo estaba antes.
6. Lee el informe del auditor, la sección de control interno y los hechos esenciales. Busca deuda
   en entidades que no consolidan, debilidades materiales de control, ajustes de períodos
   anteriores y cifras comparativas que cambiaron respecto del informe anterior.

Es hallazgo cuando el DSO ajustado sube aunque el reportado baje, cuando un saldo cambió de línea,
cuando un indicador cambió de fórmula o de presentación, o cuando el auditor no puede certificar
una operación. También cuando la empresa admite una debilidad material de control, o cuando las
cifras de un año ya publicado cambiaron sin una explicación específica.

Lo descarga que la reclasificación esté explicada y aplicada también a los períodos anteriores.

Vara. Symbol bajó su DSO de 119 a 90 días convirtiendo cuentas en pagarés. Tellabs informó un alza
de 5 días que con su fórmula anterior era de 16. Parmalat discutió en público con su auditor.

## AA 1. Inflar ingresos y utilidades con una adquisición

Las 3 pruebas que siguen se corren si la empresa compró o vendió negocios en los últimos 3 años.
Si no lo hizo, el veredicto es LIMPIO y «Qué se revisó» lo dice con la nota de combinaciones de
negocios, o con el conteo de `acquisition`, `adquisición` y `goodwill` cuando esa nota no existe.

Qué se hace.

1. Mira los ingresos de la adquirida en sus últimos trimestres antes del cierre, y los primeros
   dentro del comprador.
2. Lee la nota de la adquisición. Anota las reservas creadas, los castigos hechos al cierre y la
   contraprestación contingente.
3. Busca ganancias por reducción de pagos contingentes. Términos. `contraprestación contingente`,
   `contingent consideration`, `earn-out`, `change in fair value`.
4. Busca contratos de licencia, suministro o servicios firmados junto con la compra o la venta.
5. Revisa si la adquirida cambió de política contable apenas entró.
6. Compara el crecimiento de la plusvalía y los intangibles con el del negocio.

Es hallazgo cuando las ventas de la adquirida caen antes del cierre y saltan después, cuando una
reserva de la compra se revierte contra resultados, cuando hay una ganancia por pagar menos de lo
pactado, o cuando un contrato anexo convierte precio en ingresos.

Lo descarga que la adquirida informe sus cifras por separado y que no muestren el quiebre.

Vara. Salix vendió 13 millones y después cero en los 2 trimestres antes del cierre, contra más de
300 antes y después. Li & Fung sacó 51 por ciento de su utilidad operacional de un semestre de
reducir un pago contingente.

## AA 2. Inflar el flujo de caja con una adquisición

Una compra entra por inversión y sus cobros entran por operación. Le pasa a toda empresa que compra.

Qué se hace.

1. Calcula el flujo de caja libre tras adquisiciones de cada año. Ya está en la tabla de razones.
2. Mira cuántas compras hizo y cuántas reveló con detalle.
3. Busca en inversión líneas de «adquisición» de contratos, clientes o cuentas.
4. Si vendió un negocio, mira si se quedó con las cuentas por cobrar o si parte del precio entró
   como anticipo. Si compró, mira si dejó fuera las cuentas por pagar.
5. Busca líneas nuevas en el estado de flujo de efectivo y efectivo restringido que financie a una
   unidad.

Es hallazgo cuando el flujo operacional es positivo y el flujo de caja libre tras adquisiciones es
negativo año tras año, cuando costos de captar clientes se registran como adquisiciones, o cuando
la estructura de una compraventa pasó caja de inversión a operación.

Lo descarga una compra aislada y grande, con el flujo tras adquisiciones positivo en los demás años.

Con un flujo operacional negativo el paso 1 no dice nada, y la prueba se decide con los pasos 3 a 5.

Vara. Tyco mostró flujo operacional positivo y flujo tras adquisiciones negativo los 4 años, hasta
8.971 millones negativos en 2001. Tenet vendió hospitales y se quedó con 394 millones por cobrar.

## AA 3. Manipular métricas con una adquisición

Lo comprado se cuenta como crecimiento propio, o sus costos se excluyen para siempre.

Qué se hace.

1. Recalcula el crecimiento sin lo comprado, con la nota de ventas pro forma o con el aporte de la
   adquirida a los ingresos.
2. Lee cómo define la empresa su crecimiento orgánico.
3. Mira si las tiendas o unidades compradas entran de inmediato a la base comparable.
4. Suma los costos de adquisición e integración que la empresa excluye, año por año.
5. Revisa si dejó de publicar una métrica.

Es hallazgo cuando el crecimiento orgánico informado es mayor que el recalculado, cuando la base
comparable cambia con cada compra, cuando una empresa que compra todos los años excluye sus costos
de compra como si fueran de una vez, o cuando una métrica deja de publicarse al volverse negativa.

Lo descarga una definición de crecimiento orgánico que excluye todo ingreso de lo comprado durante
12 meses.

Vara. Starbucks dejó de publicar sus ventas comparables el trimestre en que se volvieron negativas.
Affiliated Computer Systems restaba una cifra fija y contaba como propio lo que la adquirida crecía.
