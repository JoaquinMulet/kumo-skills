---
name: verificacion-adversarial
description: >-
  Somete a refutación adversarial las afirmaciones, cifras y citas de un texto YA
  ESCRITO: buscadores reúnen la evidencia y refutadores independientes intentan destruir
  cada afirmación; el producto es un veredicto por afirmación —sobrevive, se cae, y la
  corrección exacta—, nunca un informe nuevo. Usar cuando un texto que afirma hechos va
  a publicarse o enviarse —informe a cliente, artículo, tesis de inversión, peritaje— y
  el usuario pide comprobar si es cierto, contrastar cifras contra su fuente, anticipar
  por dónde lo van a refutar desde fuera, o dice "verifica estas cifras", "esto se
  publica", "refuta esto", "qué de esto es verdad", "audita las fuentes". NO usar si no
  hay afirmaciones previas que juzgar (pregunta abierta: deep-research), ni si el objeto
  es un proyecto, repo o infraestructura en vez de un texto (auditoria-de-realidad), ni
  para juzgar si el texto se entiende o está completo (doc-completitud): juzga si lo que
  dice es VERDAD, no si se entiende.
---

# Verificación adversarial

Separa lo que se puede imprimir de lo que no. La idea central: **quien busca la
evidencia nunca es quien la valida.** Un agente reúne el material. Otro agente
distinto, sin cariño por el hallazgo, intenta destruirlo. Solo lo que sobrevive
llega al documento.

No es una revisión de estilo ni un chequeo de completitud. Es una aduana de hechos.

## Cuándo aplica y cuándo no

Aplica cuando existe un texto (o un borrador, o una tesis) que **ya afirma cosas** y
esas afirmaciones van a salir con el nombre de alguien encima.

- Sí: un informe a cliente, un artículo, una tesis de inversión, un peritaje, una
  carta pública, un capítulo con cifras y citas.
- No: una pregunta abierta sin afirmaciones previas, eso es investigar, no verificar.
- No: el estado real de un sistema o un repo, para eso está `auditoria-de-realidad`.
- No: si el documento se entiende mal pero sus hechos no están en duda, para eso
  están `doc-completitud` y `doc-narrativa`.

## La puerta: confirmar antes de abrir la flota

**Nunca lanzar el fan-out sin visto bueno explícito de la persona a cargo.** Que el
usuario haya pedido "verifica esto" autoriza la verificación, no el tamaño de la
corrida. Antes de lanzar, presentar en una línea: qué se verificará, con cuántos
agentes y en cuántas fases, y esperar la respuesta.

Dimensionar al riesgo del entregable, no al entusiasmo:

| Entregable | Buscadores | Lentes por afirmación |
|---|---|---|
| Nota interna, decisión de diseño | 3–4 | 1 |
| Informe a cliente, documento con cifras | 5–8 | 1 |
| Publicación, precios, peritaje, compra | 6–10 | 3 |

**Lente** es el flanco por el que un refutador ataca. Tres refutadores idénticos repiten
el mismo punto ciego. Tres lentes distintas cubren fallos distintos. Las tres del
andamiaje son **fuente** (¿existe el documento, dice literalmente eso, lo abrió?),
**medición** (¿la cifra mide el período, el perímetro y la unidad que se le atribuyen?)
e **inferencia** (¿la conclusión se sigue, o hay un salto de causalidad, extrapolación o
muestra?). Se implementan como un texto que se añade al final del prompt del refutador
, constante `LENTES` en el script, y con tres se decide por mayoría.

Aritmética antes de lanzar: refutadores = buscadores × afirmaciones cargantes × lentes.
Si el plan supera unos quince agentes y no es un entregable de alto riesgo, achicarlo
antes de proponerlo.

## El reparto de roles

Tres papeles, y **no se intercambian**:

- **Buscador.** Subagente que reúne evidencia sobre un frente acotado. Devuelve
  afirmaciones estructuradas, cada una con su cita textual, su fuente y su fecha.
- **Refutador.** Subagente distinto, sin memoria del buscador, cuya única instrucción
  es **destruir** la afirmación. No "evaluarla": destruirla. Desconfía por defecto.
- **Editor.** El orquestador, o sea quien invoca esta skill. Recibe los veredictos,
  decide qué entra al texto y con qué salvaguardas, y escribe las correcciones.

El editor nunca delega la redacción final a un agente: tiene el contexto del documento
que los subagentes no tienen.

## El pipeline

Usar el tool `Workflow` con dos etapas encadenadas. **Pipeline, no barrera**: cada
afirmación pasa a refutación en cuanto su buscador termina, sin esperar a los demás.

Adaptar los frentes (`FRENTES`) y el contexto (`CONTEXTO`) a cada encargo. El resto
del andamiaje se reutiliza tal cual.

```js
export const meta = {
  name: 'verificacion-adversarial',
  description: 'Buscadores reunen evidencia; refutadores independientes intentan destruir cada afirmacion',
  phases: [
    { title: 'Buscar', detail: 'un agente por frente' },
    { title: 'Refutar', detail: 'un refutador por afirmacion que sostiene la conclusion' },
  ],
}

const CONTEXTO = `
[Quien es el cliente/medio, que se va a publicar, y con que vara.]

REGLAS DE EVIDENCIA (inviolables):
- Fuente primaria o nada. Si citas un documento, debes haberlo ABIERTO, no un resumen.
- Cita textual literal y breve, con su ubicacion exacta dentro del documento.
- Si un recurso devuelve 403 o esta tras muro de pago, intenta rutas alternativas
  (busqueda de texto completo del organismo, sitio del emisor, Internet Archive,
  repositorios academicos) y DOCUMENTA cuales intentaste.
- Si no lo consigues, dilo con esas palabras. "No verificable con fuentes publicas"
  es un entregable valido. Rellenar el hueco con una secundaria disfrazada es falta grave.
- Distingue SIEMPRE lo que se dijo ENTONCES de lo que se concluyo DESPUES.
`

const FRENTES = [
  { key: 'frente-1', prompt: `${CONTEXTO}\n\n[Encargo acotado del buscador 1.]` },
  { key: 'frente-2', prompt: `${CONTEXTO}\n\n[Encargo acotado del buscador 2.]` },
]

const CLAIMS_SCHEMA = {
  type: 'object',
  properties: {
    claims: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          claim: { type: 'string' },
          verbatim: { type: 'string', description: 'cita literal con su ubicacion en el documento' },
          evidence: { type: 'string' },
          source: { type: 'string' },
          sourceDate: { type: 'string' },
          sourceUrl: { type: 'string' },
          openedDirectly: { type: 'boolean', description: 'true SOLO si abriste el documento primario' },
          primaryAccess: {
            type: 'string',
            description: 'como llegaste al primario, o por que no llegaste: que rutas intentaste y como fallaron. El refutador lo necesita para decidir si el primario era obtenible.',
          },
          loadBearing: { type: 'boolean', description: 'true si la conclusion cambia sin esta afirmacion' },
          bearing: { type: 'string', enum: ['apoya', 'refuta', 'matiza'] },
        },
        required: ['claim', 'evidence', 'source', 'sourceDate', 'openedDirectly', 'primaryAccess', 'loadBearing', 'bearing'],
      },
    },
    routesTried: { type: 'string', description: 'que rutas de acceso fallaron y como' },
    narrative: { type: 'string' },
    stillOpen: { type: 'string', description: 'que quedo sin cerrar y por que importa' },
  },
  required: ['claims', 'routesTried', 'narrative', 'stillOpen'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    refuted: { type: 'boolean' },
    severity: { type: 'string', enum: ['fatal', 'material', 'menor', 'ninguna'] },
    negativeBasis: {
      type: 'string',
      enum: ['inspeccionado', 'inferido', 'no-aplica'],
      description: 'si refutas por ausencia: abriste el primario (inspeccionado) o lo dedujiste (inferido)',
    },
    correction: { type: 'string', description: 'la formulacion imprimible corregida' },
    reasoning: { type: 'string' },
  },
  required: ['refuted', 'severity', 'negativeBasis', 'correction', 'reasoning'],
}

// Lentes del refutador: el flanco por el que ataca. Tres refutadores identicos repiten
// el mismo punto ciego; tres lentes distintas cubren fallos distintos. Con una basta
// para entregables internos; para publicacion, usar las tres y decidir por mayoria.
const LENTES = [
  'LENTE FUENTE: concentrate en si el documento existe, si dice LITERALMENTE eso, y si el investigador lo abrio de verdad o uso un resumen. Busca el documento tu mismo.',
  'LENTE MEDICION: concentrate en si la cifra mide el periodo, el perimetro y la unidad que se le atribuyen. Busca confusiones de categoria y cambios de denominador.',
  'LENTE INFERENCIA: concentrate en si la conclusion se sigue de la evidencia. Busca saltos de causalidad, extrapolaciones, muestras no representativas y citas cortadas.',
]
const LENTES_ACTIVAS = LENTES.slice(0, 1) // publicacion / peritaje / compra: usar LENTES completo

const REFUTADOR = (c, lente) => `${CONTEXTO}

ERES EL VERIFICADOR ADVERSARIAL. Tu trabajo es REFUTAR, no evaluar. Esto se va a
publicar y una cifra falsa cuesta la credibilidad entera. Desconfia por defecto.

${lente}

AFIRMACION: "${c.claim}"
${c.verbatim ? `Cita alegada: "${c.verbatim}"` : ''}
Evidencia alegada: ${c.evidence}
Fuente: ${c.source} (${c.sourceDate}) ${c.sourceUrl || ''}
El investigador declara haber abierto el primario: ${c.openedDirectly}
Acceso al primario segun el investigador: ${c.primaryAccess}

Verifica de forma independiente, con busquedas propias:
1. Existe la fuente y dice LITERALMENTE lo que se le atribuye? Si hay cita textual,
   es verbatim o esta parafraseada como si fuera literal?
2. Si declaro openedDirectly=true, hay senales de que uso un resumen secundario?
   Busca el documento tu mismo y compara.
3. La cifra esta redondeada, desactualizada o sacada de contexto? Mide el periodo y
   el perimetro que se le atribuye?
4. Se confunden categorias? (generado vs almacenado vs cobrado; comprometido vs
   ejecutado; extrapolacion estadistica presentada como dato oficial; una metrica
   local presentada como nacional.)
5. La cita esta cortada justo antes de una clausula que invierte su sentido?
6. Se confunde correlacion con causalidad?
7. Hay evidencia contraria creible que el investigador omitio?

REGLA DEL RECLAMO NEGATIVO — la mas importante. Si vas a refutar diciendo que la
fuente NO dice algo o que la cifra NO existe, declara en 'negativeBasis' si lo
INSPECCIONASTE (abriste el primario y no estaba) o lo INFERISTE (lo dedujiste de un
secundario, o simplemente no lo encontraste). Un negativo inferido NO es una
refutacion: es una sospecha. En ese caso devuelve OBLIGATORIAMENTE refuted=false,
severity='menor', y explica en 'correction' que habria que abrir para zanjarlo. Solo
un negativo INSPECCIONADO puede llevar refuted=true.

severity: "fatal" si es falso o inventado; "material" si la distorsion cambia la
conclusion; "menor" si es imprecision inocua; "ninguna" si sobrevive intacta.
Si no logras verificarla de forma independiente Y el campo de acceso al primario
muestra que era obtenible, eso ES refutacion inspeccionada. Si el primario estaba
fuera de alcance (muro de pago, documento no publico), es negativo inferido.
Lo que no se verifica, no se imprime.

En 'correction' escribe la formulacion EXACTA que si se puede imprimir.`

// Tope de afirmaciones refutadas por frente. Existe porque el costo es multiplicativo:
// agentes = frentes x MAX_POR_FRENTE x LENTES_ACTIVAS. Con 8 frentes y 3 lentes, este
// tope de 8 ya son 192 refutadores. Subirlo solo si un frente concreto trae mas de ocho
// afirmaciones que sostienen la conclusion, y recalcular el total antes de lanzar.
const MAX_POR_FRENTE = 8

phase('Buscar')
const resultados = await pipeline(
  FRENTES,
  (f) => agent(f.prompt, { label: `busca:${f.key}`, phase: 'Buscar', schema: CLAIMS_SCHEMA }),
  (r, f) => {
    if (!r) return null
    const cargantes = r.claims.filter((c) => c.loadBearing).slice(0, MAX_POR_FRENTE)
    if (cargantes.length < r.claims.filter((c) => c.loadBearing).length) {
      log(`AVISO ${f.key}: quedaron afirmaciones cargantes sin refutar por el tope de ${MAX_POR_FRENTE}`)
    }
    return parallel(
      cargantes.map((c) => () =>
        // Una lente = un refutador. Con varias, se decide por mayoria: la afirmacion cae
        // si mas de la mitad de las lentes la refutan.
        parallel(
          LENTES_ACTIVAS.map((lente) => () =>
            agent(REFUTADOR(c, lente), { label: `refuta:${f.key}`, phase: 'Refutar', schema: VERDICT_SCHEMA })
          )
        ).then((vs) => {
          const v = vs.filter(Boolean)
          const caen = v.filter((x) => x.refuted)
          return { ...c, veredictos: v, verdict: caen.length > v.length / 2 ? caen[0] : (v[0] || null) }
        })
      )
    ).then((vs) => ({ frente: f.key, narrative: r.narrative, routesTried: r.routesTried, stillOpen: r.stillOpen, verificadas: vs.filter(Boolean) }))
  }
)

const ok = resultados.filter(Boolean)
const todas = ok.flatMap((r) => r.verificadas)
const sobreviven = todas.filter((c) => !c.verdict?.refuted)
// Los inferidos NUNCA son refutaciones (el refutador devuelve refuted=false): son
// sospechas que el editor resuelve a mano abriendo el primario.
const inferidos = todas.filter((c) => c.veredictos?.some((v) => v.negativeBasis === 'inferido'))
log(`${sobreviven.length}/${todas.length} sobreviven · ${inferidos.length} con sospecha por negativo INFERIDO (revisar a mano)`)

return {
  sobreviven,
  refutadas: todas.filter((c) => c.verdict?.refuted),
  inferidos,
  porFrente: ok.map((r) => ({ frente: r.frente, narrative: r.narrative, routesTried: r.routesTried, stillOpen: r.stillOpen })),
}
```

## Modos de fallo documentados

Cada uno costó un error real. Leerlos antes de confiar en una corrida.

### 1. El negativo inferido (el más caro)

Un refutador dictamina «esa cifra no es de tal autor» porque **otro** autor citaba
otra cosa, sin abrir jamás el documento del primero. La inferencia es inválida: que
Z cite 3% no implica que Y no escribiera 2,7%. Ambas cosas pueden ser ciertas.

Por eso el schema exige `negativeBasis`. Un negativo **inferido** nunca se releva al
usuario como hecho, y el orquestador debe ir al primario antes de descartar nada.
«No lo encuentro» no es «no existe».

*(Caso real: se descartó una cifra por «no rastreable». El usuario abrió el artículo
original y ahí estaba, verbatim, de un reportero con nombre y fecha exacta.)*

### 2. Convergencia no es corroboración cuando el origen es único

Tres buscadores independientes afirmaron el mismo dato y eso se leyó como triple
confirmación. Los tres bebían del mismo autor, que lo había escrito sin nota al pie.

Rastrear siempre hasta la fuente primaria, no hasta el consenso de secundarias. Si
varias afirmaciones coinciden, comprobar que sus fuentes **no sean la misma**.

### 3. La cita cortada antes de la cláusula que invierte

Una frase se citó completa hasta justo antes de un cierre que le daba la vuelta al
sentido. El refutador debe leer el párrafo entero alrededor de la cita, no la cita.

### 4. Errores de categoría

Los más frecuentes, en cualquier dominio: mezclar lo **generado** con lo
**almacenado** con lo **cobrado**. Presentar gasto **comprometido** como demanda
**absorbida**. Presentar una **extrapolación estadística** como guía o dato oficial;
elevar una medición **local** a **nacional**. Cada uno produce una cifra correcta que
mide otra cosa.

### 5. El sesgo de dirección

En una corrida real, de nueve refutaciones materiales, **siete tumbaron afirmaciones
que apoyaban la tesis**. No es azar: los números que confirman lo que uno quiere creer
circulan más, y circular es lo que erosiona su procedencia. Cada repetición los aleja
de la fuente y los redondea hacia el extremo más vistoso.

Consecuencia operativa: **verificar con más dureza lo que conviene**, no lo que
incomoda. El instinto natural es el inverso y está mal calibrado.

## Qué hace el editor con los resultados

1. **Lista blanca.** Lo que sobrevive, con su cita y su fuente. Marcar cuáles exigen
   una salvaguarda de redacción obligatoria y escribirla palabra por palabra.
2. **Lista negra.** Lo que no se imprime y por qué. Ser implacable.
3. **Revisar a mano los `inferido`.** No son refutaciones, son sospechas. O se
   confirman abriendo el primario, o se devuelven a la lista blanca.
4. **Corregir en la fuente.** Si el documento no se ha enviado, el error se arregla
   en el texto y desaparece. No conservar el fallo como auto-corrección visible: eso
   solo se justifica si el error llegó de verdad a un lector.
5. **Publicar la tasa de error** cuando el entregable lo permita: cuántas afirmaciones
   entraron, cuántas cayeron. Un documento que declara su propia tasa de fallos es más
   creíble que uno que finge no tener ninguna.

## La ausencia como hallazgo

Cuando un dato no se puede verificar, la tentación es rellenarlo. La alternativa suele
ser mejor material: **decir que no existe y por qué**.

«El regulador dejó de publicar esa serie justo el año en que empezó el problema» o
«ninguna de las cinco empresas divulga esa métrica» son hallazgos publicables, no
huecos. Una ausencia sistemática dice algo sobre el mundo. Un número inventado, no.

## Criterio de cierre

Parar cuando ninguna afirmación que sostiene la conclusión siga en pie sin verificar,
y cuando todo negativo `inferido` haya sido resuelto a mano. Las imprecisiones
menores son cola aceptable: perseguirlas una a una infla el trabajo sin mover el
veredicto.

No bajar la vara para terminar. Lo legítimo es acotar el criterio a las afirmaciones
que cargan peso, no ablandar el prompt del refutador para que encuentre menos.
