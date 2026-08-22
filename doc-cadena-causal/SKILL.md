---
name: doc-cadena-causal
description: >-
  Audita si CADA concepto de un documento se sostiene solo y llega A TIEMPO: por
  qué existe, quién lo hace, de dónde sale su número, qué pasaría sin él, si le
  aplica al lector, y si se explica ANTES de usarse. Detecta los dos huecos que
  las revisiones de estilo NO ven: el concepto presente y hasta con analogía del
  que el lector no puede decir para qué existe, y el que se menciona en párrafos
  anteriores a donde se explica, calcula o deduce — un defecto de ORDEN que se
  denuncia como "no se entiende nada" o "es muy árido" y se mide con un contrato
  de vocabulario. Úsala antes de reescribir un documento didáctico o técnico, o
  cuando un material pasó revisión de redacción y sigue sin entenderse. Dispara
  con "revisa la cadena causal", "busca conceptos sin fundamento", "está
  desordenado", "de dónde salió esto", "por qué existe cada cosa". Orquesta con
  el tool Workflow auditores que aplican una rejilla de cinco preguntas; el
  orquestador verifica los hallazgos y redacta los parches.
---

# Doc Causal Chain. "¿por qué existe esta cosa?"

Encuentra los conceptos **nombrados pero no fundados**. Es el hueco que sobrevive
a toda revisión de estilo, porque el estilo juzga el texto *como texto* y este
defecto no es de redacción: es de que falta un eslabón del razonamiento.

## Por qué hace falta una etapa aparte

Las otras tres skills de documentos preguntan cosas que un concepto sin causa
**responde bien**:

| Skill | Pregunta | Un concepto sin causa… |
|---|---|---|
| `doc-completitud` | ¿está el ítem presente? | …está presente. **Pasa.** |
| `doc-narrativa` | ¿se lee bien? | …se lee bien, con analogía y todo. **Pasa.** |
| `doc-prueba-de-uso` | ¿puedes ejecutar la tarea? | …no bloquea la tarea. **Pasa.** |
| **(ninguna de las tres)** | **nadie pregunta por el ORDEN** | …y un concepto usado seis capítulos antes de explicarse **pasa las tres**. |

Las tres pasan y el hueco sobrevive. Caso real: un curso explicaba que «la tasa de
descuento depende de la garantía del contrato» y explicaba *qué* era la garantía
, sin decir nunca por qué existe una garantía, qué problema resuelve, quién la
pone, de cuánto es, ni que al lector **no le aplicaba** porque describía el
mercado interbancario. El lector razonó bien sobre el texto y llegó a una
pregunta que no tenía respuesta.

## Dónde va en el orden (importa)

1. `doc-completitud`. ¿está todo?
2. **`doc-cadena-causal`, ¿cada cosa se sostiene sola?** ← esta
3. `doc-narrativa`. ¿se lee bien?
4. `doc-prueba-de-uso`. ¿se puede actuar con esto?

**Antes de narrativa, nunca después.** Narrativa produce un plan que reordena y
comprime. Si comprimes un concepto sin fundamento, comprimes el síntoma. En el
caso real, el flujo de tres lentes dejó el capítulo mejor escrito, arco,
analogías, fórmulas al apéndice, y no tocó el hueco.

## La deuda de orden: usado antes de explicado

**Este es el defecto estructural más grave y el más invisible de los tres que
esta skill persigue.** Un concepto puede estar perfectamente explicado, con su
causa, su fórmula y su ejemplo, y aun así romper el documento, si aparece
mencionado **en párrafos anteriores** a donde se explica, se calcula o se deduce.

No es un problema de redacción. Es un problema de **orden**, y por eso ninguna
lente de estilo lo ve: cada párrafo, leído aisladamente, está bien escrito. El
daño se produce en el lector, que se topa con una cifra o un término que no
puede evaluar, y a partir de ahí lee todo lo demás con una deuda encima. Cuando
llega la explicación, tres capítulos después, ya decidió que el material no se
entiende.

**El síntoma con el que llega el usuario** no es «está mal ordenado», es «no se
entiende nada», «esto es muy árido», «me perdí al principio». Si escuchas eso
sobre un documento que a ti te parece completo y bien escrito, **mide el orden
antes de tocar una sola frase**.

### La medición: el contrato de vocabulario

Se mecaniza entero, y por eso es barato correrlo tantas veces como haga falta.

1. **Enumera los términos y las cifras derivadas** del documento, y asigna a cada
   uno **la sección donde se introduce** (se define, se calcula o se deduce). Eso
   es el contrato: un JSON de `término → sección`.
2. **Un script busca la PRIMERA aparición** de cada término y falla si es
   anterior a su sección asignada. El veredicto es una cifra: *deuda total en
   secciones-concepto*.
3. **Exime la navegación.** El índice, el encabezado y los «lo veremos en el
   capítulo N» nombran conceptos sin usarlos. Contarlos produce ruido que hace
   que se ignore el informe entero.

```json
{ "inefectividad":  {"patron": "inefectividad",     "capitulo": "c5"},
  "punto base":     {"patron": "puntos? base|\\bpb\\b", "capitulo": "c8"} }
```

Los instrumentos están escritos y probados en
[`reference/`](reference/), cópialos y cambia el contrato:

| Archivo | Qué hace |
|---|---|
| `contrato_vocabulario.ejemplo.json` | el formato del contrato `término → sección` |
| `verificar_orden.py` | falla si un término aparece antes de su sección; exime la navegación |
| `guardia_primera_pasada.py` | falla si hay una cifra derivada en la primera pasada (lista blanca explícita) |
| `objetivo.py` | resuelve el archivo objetivo en un solo sitio — ver [`desarrollo-riguroso`](../desarrollo-riguroso/SKILL.md), «un verde debe poder ponerse rojo» |

En el caso real, la primera medición dio **8 conceptos con deuda, 22
secciones-concepto**. Ese número fue lo que justificó una reescritura estructural
completa en vez de una pasada de edición, y es la clase de argumento que un
«creo que está desordenado» nunca gana.

### El remedio no es mover párrafos: es la estructura en espiral

Reordenar suele ser imposible, porque las dependencias son circulares: para
explicar A hace falta B, y para explicar B hace falta A. La salida es **recorrer
el material más de una vez, cada vez con más precisión**:

1. **Primera pasada, formas, sin ninguna cifra derivada.** Qué existe, quién
   hace qué, en qué dirección se mueve cada cosa. El lector construye el modelo
   mental completo sin necesitar un solo número calculado.
2. **Segunda pasada, magnitudes.** Ahora sí las cifras, sobre un esqueleto que
   el lector ya tiene.
3. **Tercera pasada, el caso real.**

Y la primera pasada se protege con **su propio guardia mecánico**: un script que
falla si aparece cualquier cifra derivada en esos capítulos, con una lista blanca
explícita de los datos *crudos* que sí pueden estar (los observados, el nocional,
las fechas). Sin ese guardia, una cifra se cuela en la primera pasada en la
primera edición que hagas, **el riesgo no es alto, es certeza**.

### Por qué hace falta el guardia y no basta la disciplina

El autor es estructuralmente ciego a este defecto: **él ya sabe lo que viene
después**, así que cada mención adelantada le parece natural. Es el mismo motivo
por el que no se puede autoevaluar la claridad de lo que uno escribió. La deuda
de orden solo la ve un lector que llega en frío… o un `grep` con un contrato.

## La rejilla. Cinco preguntas por concepto

Se evalúan **en el orden en que el documento presenta el concepto**: explicarlo
bien pero *después* del primer uso ya es fallar, ver la sección anterior, que es
la versión mecanizada de esta misma exigencia.

1. **¿POR QUÉ EXISTE?** ¿Se dice qué problema resuelve, antes de usarlo? Si el
   lector no puede completar «esto existe porque si no, pasaría X», falla.
2. **¿QUIÉN Y A QUIÉN?** Quién lo hace, quién paga, quién recibe, y si eso puede
   cambiar de lado.
3. **¿DE DÓNDE SALE EL NÚMERO?** Cómo se calcula u observa, o aparece como cifra
   caída del cielo.
4. **¿QUÉ PASARÍA SI NO ESTUVIERA?** El contrafactual.
5. **¿ME APLICA A MÍ?** ¿Se dice explícitamente si aplica al caso del lector, o
   describe otro mundo? (Este es el que más duele cuando falta.)

Veredicto por pregunta: `OK` / `DEBIL` / `FALTA`, **con cita textual** del
documento que lo demuestra y una frase de arreglo.

## El patrón. Dónde buscar primero

**No fallan los conceptos que el documento *calcula*.** El cálculo obliga a
explicar la causa: si no explicas el arbitraje, la fórmula del forward no se
sostiene.

**Fallan los que solo se *nombran*:** requisitos administrativos, categorías de
presentación, precios que se toman como dato, y los fundamentos que se dan por
sabidos porque «todos saben qué es eso». Ninguno tiene una fórmula que lo delate.

Y fallan casi siempre en **P1 y P4 juntas**, son la misma pregunta vista por los
dos lados. La P3 casi nunca falla en documentos numéricos.

### El detector barato: ratio lista / prosa

Cuenta las apariciones de un término **en formato lista** (viñetas, celdas de
tabla, «Requisitos: A + B + C») contra las apariciones **en prosa**. La lista es
el formato que permite nombrar sin explicar.

```bash
grep -o "designación formal" doc.html | wc -l      # apariciones totales
grep -c "La designación formal es" doc.html        # apariciones en prosa
```

En el caso real: **seis en lista, cero en prosa**. Ese ratio era el hueco.

## La sexta pregunta: el contrato del rótulo

La rejilla de arriba audita **conceptos**. Le falta auditar **promesas**, que es
un defecto distinto y que la rejilla no puede ver: un capítulo puede tener todos
sus conceptos bien fundados y aun así no entregar lo que su propio rótulo anunció.

Todo rótulo es un contrato con el lector. En un documento didáctico hay cuatro
tipos, y todos son verificables:

| Rótulo | Promesa | Se comprueba |
|---|---|---|
| Título de sección | que la sección trate de eso | ¿el cuerpo responde el título? |
| «Qué sabrás hacer al terminar» | cada objetivo declarado | ¿el cuerpo enseña a hacerlo? |
| «Pregunta que queda abierta» | que se responda | ¿existe la sección que la cierra, y la cierra? |
| «lo veremos en el capítulo N» | que N lo trate | ¿N existe y lo trata? |

**El caso que originó esto.** Un capítulo titulado «Alguien te vende el otro
lado» explicaba qué es el instrumento y nunca decía por qué la contraparte quiere
ese lado. Las cuatro skills de redacción lo dieron por bueno. Y el diagnóstico
fino es peor que el síntoma: **sus tres objetivos declarados tampoco mencionaban
la promesa del título**. Había dos rótulos en el mismo capítulo contradiciéndose
entre sí, y ninguna lente compara rótulo contra rótulo.

**Por eso el primer cotejo es título ↔ objetivos, antes de mirar el cuerpo.** Es
el más barato de los tres y el que delata el hueco de origen: si la promesa del
título no aparece entre los objetivos, nadie que revise «objetivos vs. cuerpo»
la va a echar de menos.

### Qué NO funciona: el solape léxico

Es tentador automatizarlo comparando las palabras del título con las de los
objetivos. **Se probó y no sirve:** marcó 12 de 24 capítulos, casi todos falsos
positivos, porque los buenos títulos son evocativos a propósito («El swap
compensa casi todo. Casi.») y no repiten el vocabulario del objetivo. Un
detector con 50 % de falsos positivos se ignora a la tercera corrida.

Lo que sí acota el trabajo es **filtrar por forma del rótulo**: los títulos
**interrogativos o promisorios**, los que preguntan algo, prometen una revelación
o nombran un agente sin identificarlo («alguien», «el que decide», «lo que
nadie te cuenta»), son un subconjunto pequeño y son donde vive el defecto. Esos
se revisan semánticamente, uno por uno. Los descriptivos («El bono, cierre a
cierre») casi nunca fallan.

## Cómo ejecutar

1. **Enumera los conceptos tú mismo** antes de invocar nada, leyendo el
   documento. No se lo pidas a un agente: es barato para ti y evita que la
   auditoría se salte lo que no vio.
2. **Repártelos en grupos temáticos** de 10-15 conceptos por auditor. Menos, y
   desperdicias agentes. Más, y el auditor se apura y empieza a inventar.
3. **Invoca el tool `Workflow`** con el script de abajo, incrustando la ruta y
   los grupos como constantes.
4. **Verifica los hallazgos graves TÚ, con `Grep`, antes de reparar nada.** Los
   auditores débiles producen falsos positivos con evidencia inventada, en la
   corrida real, uno citó una sigla que aparecía **cero veces** en el archivo, y
   otro marcó como ausente un concepto explicado dos veces.
5. **Redacta los parches tú**, no un agente a ciegas: tienes el contexto del
   documento y el registro del resto del material.

## Script para el tool Workflow

```js
export const meta = {
  name: 'auditoria-cadena-causal',
  description: 'Audita cada concepto con la rejilla de 5 preguntas causales',
  phases: [{ title: 'Auditoria' }, { title: 'Sintesis' }],
}

const doc = '<RUTA-ABSOLUTA-DEL-DOCUMENTO>'
const weak = 'haiku'
if (doc.includes('<RUTA')) throw new Error('Incrusta la ruta real antes de correr')

// Grupos de conceptos, enumerados POR EL ORQUESTADOR leyendo el documento.
const GRUPOS = [
  { k: 'grupo-1', c: 'concepto A; concepto B; concepto C; …' },
  // …10-15 conceptos por grupo
]
if (GRUPOS.some(g => g.c.includes('concepto A'))) throw new Error('Incrusta los conceptos reales')

const REJILLA = `Para CADA concepto asignado responde estas cinco preguntas mirando SOLO lo que el ` +
  `documento dice, y en el ORDEN en que lo dice (explicado bien pero DESPUES de usarlo = falla):\n` +
  `  P1 ¿POR QUE EXISTE? ¿Se dice que problema resuelve, ANTES de usarlo?\n` +
  `  P2 ¿QUIEN Y A QUIEN? ¿Quien lo hace, quien paga, quien recibe, y si cambia de lado?\n` +
  `  P3 ¿DE DONDE SALE EL NUMERO? ¿Como se calcula u observa, o cae del cielo?\n` +
  `  P4 ¿QUE PASARIA SI NO ESTUVIERA? El contrafactual.\n` +
  `  P5 ¿ME APLICA A MI? ¿Se dice si aplica al caso del lector o describe otro mundo?\n\n` +
  `Veredicto OK/DEBIL/FALTA por pregunta. Si es DEBIL o FALTA, CITA el texto exacto que lo ` +
  `demuestra (o di "no hay texto") y escribe en UNA frase que habria que agregar.`

const SCHEMA = { type: 'object', properties: {
  conceptos: { type: 'array', items: { type: 'object', properties: {
    concepto: { type: 'string' }, ubicacion: { type: 'string' },
    p1_por_que_existe: { type: 'string', enum: ['OK','DEBIL','FALTA'] },
    p2_quien:          { type: 'string', enum: ['OK','DEBIL','FALTA'] },
    p3_de_donde_sale:  { type: 'string', enum: ['OK','DEBIL','FALTA'] },
    p4_contrafactual:  { type: 'string', enum: ['OK','DEBIL','FALTA'] },
    p5_me_aplica:      { type: 'string', enum: ['OK','DEBIL','FALTA'] },
    gravedad: { type: 'string', enum: ['critica','media','menor'] },
    evidencia: { type: 'string' }, arreglo: { type: 'string' } },
    required: ['concepto','ubicacion','p1_por_que_existe','p2_quien','p3_de_donde_sale',
               'p4_contrafactual','p5_me_aplica','gravedad','evidencia','arreglo'] } } },
  required: ['conceptos'] }

phase('Auditoria')
const res = (await parallel(GRUPOS.map(g => () => agent(
  `${REJILLA}\n\nTUS CONCEPTOS (audita SOLO estos, todos):\n${g.c}\n\nLee ${doc} completo. ` +
  `El estandar: un lector que parte de cero debe poder responder las cinco preguntas SIN buscar ` +
  `fuera del documento y SIN haber leido nada posterior. No seas generoso.`,
  { label: `audita-${g.k}`, model: weak, schema: SCHEMA, phase: 'Auditoria' }
)))).filter(Boolean)

phase('Sintesis')
const filas = res.flatMap(r => r.conceptos || [])
const sintesis = await agent(
  `Cinco auditores aplicaron la rejilla a ${filas.length} conceptos:\n\n` +
  `${JSON.stringify(filas, null, 1).slice(0, 60000)}\n\nLee tu tambien ${doc}. Tu tarea:\n` +
  `(1) DESCARTA falsos positivos: verifica con Grep cada hallazgo grave antes de darlo por bueno, ` +
  `y di cuales descartaste y por que.\n` +
  `(2) Ordena los sobrevivientes por cuanto rompen la comprension.\n` +
  `(3) Escribe YA REDACTADO el parrafo que habria que agregar, en el estilo del documento.\n` +
  `(4) Identifica el PATRON: que tipo de concepto falla y en cual de las cinco preguntas.`,
  { label: 'sintesis-auditoria' }
)
return { totalConceptos: filas.length, sintesis, filas }
```

## Lo que esta skill NO cubre (y hay que hacer aparte)

Hay un defecto hermano que **ninguna revisión de texto encuentra**, por muchas
lentes que se le pongan: la **incoherencia interna de las cifras**. Un documento
puede tener cada concepto perfectamente fundado y aun así afirmar números que no
cruzan entre sí, un bono que se emite «a la par» con un cupón incompatible con
su propia curva, por ejemplo.

Eso no se audita después: **se previene al construir**. La regla es *un solo
origen de verdad, y las identidades corriendo como test*: ninguna cifra escrita a
mano si un modelo puede calcularla, y las condiciones que deben cumplirse
impresas como `True`/`False` cada vez que el modelo corre. Es disciplina de
autoría, no etapa de revisión, un agente leyendo el documento no puede
recalcular el modelo. Ver `desarrollo-riguroso`.

## Tus hallazgos deben sobrevivir a la próxima reescritura

Los parches que produce esta skill viven en una redacción concreta y **no
sobreviven a una reescritura del documento**: la redacción cambia, el arreglo
desaparece y el resultado sigue leyéndose bien, así que nadie lo nota.

Antes de cerrar, convierte cada arreglo en un **centinela**, una frase textual,
corta y distintiva, dentro de un test de regresión que falle si desaparece. La
doctrina completa, con el caso real que la originó, está en
[`doc-narrativa`](../doc-narrativa/SKILL.md), sección «Antes de reescribir».

## Skills hermanas

- `doc-completitud`. Que **nada falte** (inventario presente).
- `doc-narrativa`. Que **se lea bien** (arco, densidad, estructura).
- `doc-prueba-de-uso`. Que **se pueda actuar** (el lector ejecuta la tarea).
- `verificacion-adversarial`. Que **sea verdad** (afirmaciones contra fuentes).

Esta cubre el eje que ninguna cubría: que **cada pieza se sostenga sola**.
