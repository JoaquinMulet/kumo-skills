---
name: doc-cadena-causal
description: >-
  Audita si CADA concepto de un documento se sostiene solo: por qué existe, quién
  lo hace, de dónde sale su número, qué pasaría sin él y si le aplica al lector.
  Detecta el hueco que las revisiones de estilo NO ven — el concepto presente,
  definido, bien ubicado y hasta con analogía, del que el lector igual no puede
  decir para qué existe. Úsala antes de reescribir un documento didáctico o
  técnico, cuando alguien pregunta "¿y de dónde salió esto?", "¿por qué hay que
  hacer esto?" o "no entiendo de dónde viene", cuando un lector razona
  correctamente sobre tu texto y llega a una pregunta sin respuesta, o cuando un
  material pasó revisión de redacción y sigue sin entenderse. Dispara con
  "audita si se entiende por qué", "revisa la cadena causal", "busca conceptos
  sin fundamento", "por qué existe cada cosa". Orquesta con el tool Workflow
  auditores que aplican una rejilla de cinco preguntas; el orquestador verifica
  los hallazgos y redacta los parches.
---

# Doc Causal Chain — "¿por qué existe esta cosa?"

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

Las tres pasan y el hueco sobrevive. Caso real: un curso explicaba que «la tasa de
descuento depende de la garantía del contrato» y explicaba *qué* era la garantía
— sin decir nunca por qué existe una garantía, qué problema resuelve, quién la
pone, de cuánto es, ni que al lector **no le aplicaba** porque describía el
mercado interbancario. El lector razonó bien sobre el texto y llegó a una
pregunta que no tenía respuesta.

## Dónde va en el orden (importa)

1. `doc-completitud` — ¿está todo?
2. **`doc-cadena-causal` — ¿cada cosa se sostiene sola?** ← esta
3. `doc-narrativa` — ¿se lee bien?
4. `doc-prueba-de-uso` — ¿se puede actuar con esto?

**Antes de narrativa, nunca después.** Narrativa produce un plan que reordena y
comprime; si comprimes un concepto sin fundamento, comprimes el síntoma. En el
caso real, el flujo de tres lentes dejó el capítulo mejor escrito —arco,
analogías, fórmulas al apéndice— y no tocó el hueco.

## La rejilla — cinco preguntas por concepto

Se evalúan **en el orden en que el documento presenta el concepto**: explicarlo
bien pero *después* del primer uso ya es fallar.

1. **¿POR QUÉ EXISTE?** ¿Se dice qué problema resuelve, antes de usarlo? Si el
   lector no puede completar «esto existe porque si no, pasaría X», falla.
2. **¿QUIÉN Y A QUIÉN?** Quién lo hace, quién paga, quién recibe, y si eso puede
   cambiar de lado.
3. **¿DE DÓNDE SALE EL NÚMERO?** Cómo se calcula u observa — o aparece como cifra
   caída del cielo.
4. **¿QUÉ PASARÍA SI NO ESTUVIERA?** El contrafactual.
5. **¿ME APLICA A MÍ?** ¿Se dice explícitamente si aplica al caso del lector, o
   describe otro mundo? (Este es el que más duele cuando falta.)

Veredicto por pregunta: `OK` / `DEBIL` / `FALTA`, **con cita textual** del
documento que lo demuestra y una frase de arreglo.

## El patrón — dónde buscar primero

**No fallan los conceptos que el documento *calcula*.** El cálculo obliga a
explicar la causa: si no explicas el arbitraje, la fórmula del forward no se
sostiene.

**Fallan los que solo se *nombran*:** requisitos administrativos, categorías de
presentación, precios que se toman como dato, y los fundamentos que se dan por
sabidos porque «todos saben qué es eso». Ninguno tiene una fórmula que lo delate.

Y fallan casi siempre en **P1 y P4 juntas** — son la misma pregunta vista por los
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

## Cómo ejecutar

1. **Enumera los conceptos tú mismo** antes de invocar nada, leyendo el
   documento. No se lo pidas a un agente: es barato para ti y evita que la
   auditoría se salte lo que no vio.
2. **Repártelos en grupos temáticos** de 10-15 conceptos por auditor. Menos, y
   desperdicias agentes; más, y el auditor se apura y empieza a inventar.
3. **Invoca el tool `Workflow`** con el script de abajo, incrustando la ruta y
   los grupos como constantes.
4. **Verifica los hallazgos graves TÚ, con `Grep`, antes de reparar nada.** Los
   auditores débiles producen falsos positivos con evidencia inventada — en la
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
cruzan entre sí — un bono que se emite «a la par» con un cupón incompatible con
su propia curva, por ejemplo.

Eso no se audita después: **se previene al construir**. La regla es *un solo
origen de verdad, y las identidades corriendo como test*: ninguna cifra escrita a
mano si un modelo puede calcularla, y las condiciones que deben cumplirse
impresas como `True`/`False` cada vez que el modelo corre. Es disciplina de
autoría, no etapa de revisión — un agente leyendo el documento no puede
recalcular el modelo. Ver `desarrollo-riguroso`.

## Skills hermanas

- `doc-completitud` — que **nada falte** (inventario presente).
- `doc-narrativa` — que **se lea bien** (arco, densidad, estructura).
- `doc-prueba-de-uso` — que **se pueda actuar** (el lector ejecuta la tarea).
- `verificacion-adversarial` — que **sea verdad** (afirmaciones contra fuentes).

Esta cubre el eje que ninguna cubría: que **cada pieza se sostenga sola**.
