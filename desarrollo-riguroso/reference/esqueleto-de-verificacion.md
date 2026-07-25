# Esqueleto de verificación multi-agente

La forma reusable de cualquier grafo de verificación de Kumo, y los modos de fallo que
cada instancia pagó por separado. Léelo antes de escribir un `Workflow` nuevo o de
convertir un flujo lineal en grafo. Las skills que ya lo instancian (`doc-completitud`,
`doc-narrativa`, `doc-prueba-de-uso`, `auditoria-de-realidad`,
`verificacion-adversarial`) apuntan acá en vez de recontarlo.

**Estado: v1**, y esta es la última ronda de destilación por decisión explícita — un esqueleto
que se reescribe en cada uso no es un esqueleto. La v0 salió de esas cinco instancias; la v1
cerró los vacíos que encontró su propia **prueba de uso**: un lector frío débil, con este
archivo como única fuente, escribió el workflow para auditar una librería ajena. Cumplió 6 de
8 criterios del rubric y dejó al descubierto lo que faltaba: el guard mal generalizado, el
contrato del tool que el archivo daba por sabido, qué hace el orquestador con un hallazgo
dudoso, y un presupuesto que estaba escrito arriba pero no operativo en el andamiaje. Los
cuatro están corregidos abajo.

## Antes de nada: ¿esto merece un grafo?

Un grafo paga cuando hay **lentes independientes sobre el mismo objeto** y el costo del
error es alto. No paga cuando la tarea es chica, cuando los pasos se leen entre sí de
verdad, o cuando quien tiene que decidir es el humano y el fan-out solo le agrega texto
que revisar. **Umbral explícito, escrito en la skill que lo invoca** — si no está
escrito, la skill dispara una flota sobre un correo de cinco líneas.

Y la puerta de la casa: **nunca lanzar el fan-out sin visto bueno explícito de la
persona a cargo.** Que el usuario haya pedido el trabajo autoriza el trabajo, no el
tamaño de la corrida. Presentar en una línea qué se hará, con cuántos agentes y en
cuántas fases, y esperar respuesta.

**Default de la casa: ≤6 agentes por corrida.** Toda skill que instancie este esqueleto se
escribe con constantes baratas (pocas lentes, pocas corridas, un juez) y una nota de cómo
escalar. Subir de ahí es una decisión del dueño del entregable, caso a caso, y se pide con
la aritmética en la mano: `agentes = lentes × objetos × jueces`. Escalar por default es
cómo un grafo útil se vuelve un gasto que nadie autorizó.

## La forma canónica

```
ancla  →  fan-out de lentes independientes  →  síntesis en un nodo
       →  verificación contra el ancla  →  decisión del orquestador
```

1. **Ancla** — el criterio contra el que se juzgará todo, producido ANTES de ver
   ninguna salida (un inventario del contenido original, un rubric, la lista de
   afirmaciones). Es lo único que evita que la fase final confirme alegremente lo que
   la primera dejó fuera.
2. **Fan-out de lentes** — agentes que miran el MISMO objeto por flancos distintos.
   Lentes distintas, no copias: tres agentes idénticos repiten el mismo punto ciego;
   tres lentes cubren fallos distintos.
3. **Síntesis** — un nodo resuelve las tensiones entre lentes y deja un producto único.
   Varias lentes escribiendo sobre el mismo objeto se pisan.
4. **Verificación contra el ancla** — no contra la impresión del verificador.
5. **Decisión del orquestador** — verificación de fantasmas, ranking y escritura final
   son SIEMPRE suyos. Tiene el contexto que los subagentes no tienen.

## Las reglas duras

### El ancla no se puede argumentar

Un ancla producida por un solo agente débil es una opinión con nombre de ancla: si nace
incompleta, todo lo que cuelga de ella hereda el hueco y el verificador final certifica
un vacío. Deriva mecánicamente todo lo que sea contable (`grep` de cifras, tablas,
encabezados, rutas) y deja al agente solo lo semántico. Si el ancla igual la produce un
agente, **duplícala con un segundo agente independiente** — pero ver la regla siguiente
antes de unir las dos listas.

### No mezcles un oráculo duro con uno blando en la misma lista

Unir un inventario mecánico con uno de agente sube el recall **y los fantasmas**, y cada
ítem alucinado que entra al ancla es un "faltante" que un reparador automático va a
insertar en el documento: contenido que nunca existió, escrito sin que nadie decidiera.
La separación correcta:

- **Ancla dura** (derivada mecánicamente) → puede disparar reposición automática.
- **Ancla blanda** (producida por un agente) → sus faltantes van al **orquestador**, no
  al parchador. Es el "nombrar residuales" del oráculo blando aplicado al grafo.

### Todo nodo debe demostrar que ejerció el objeto

Un agente que puede devolver "sin hallazgos" sin haber leído nada cumple el schema
midiendo el vacío, y la salida estructurada **enmascara** el fallo aguas arriba. Exige en
el schema una prueba de lectura (campo obligatorio `resumen_leido`: el título real y el
tema en una frase; el conteo de lo procesado; una línea textual). Trata el **cero
hallazgos de la primera pasada como sospecha de instrumento roto**, no como éxito.

### El contrato del caller: incrusta los literales

El objeto sobre el que corre el grafo (rutas, superficies, secciones) se **incrusta como
constante literal en el script**, con un guard que revienta si quedó el placeholder:

```js
const DOC = '<RUTA-ABSOLUTA>'
if (!DOC || DOC.includes('<RUTA')) throw new Error('Incrusta la ruta real antes de correr')
```

El guard chequea **el placeholder y el vacío**, nunca el valor real. Escribirlo como
`if (DOC === 'C:/ruta/real/...') throw` —comparar contra el valor que sí quieres— hace que
el script reviente exactamente cuando está bien configurado. *(Lo produjo un lector frío
generalizando mal este ejemplo: el guard es una lista negra de "sin configurar", no una
comparación con lo esperado.)*

El tool `Workflow` sí acepta `args` cuando se pasa como JSON real; lo que llega
`undefined` es el caso —fácil de cometer— en que se pasa como string JSON-encodeado. Ahí
el prompt dice «lee SOLO undefined», el agente audita la nada y devuelve un veredicto
perfectamente schema-válido. Incrustar literales quita esa superficie de fallo entera por
construcción; el guard y la prueba de trabajo son la segunda y tercera línea.
*(Caso real: dos rondas de lectores ciegos devolvieron "SIN_VACIOS" sobre una lista de
archivos vacía.)*

### El que propone el fan-out necesita tope

Un nodo fresco que propone qué mirar (superficies, variantes, dimensiones) **no cuesta un
agente: cuesta lo que decida abanicar** — es un multiplicador del ancho, no una
constante. Y va a proponer de más justamente porque se puso ahí para mirar lo que el
orquestador no miraba. Su schema lleva tope explícito: *máximo N, ordenadas por peligro
real*. Sin tope, el presupuesto de la corrida lo fija el agente menos informado del grafo.

### El juez: ciego no basta

Anonimizar quita la señal de autoría, no la de estilo propio — el sesgo de
auto-preferencia correlaciona con familiaridad, y el sesgo posicional es un efecto
aparte. Un juez que sea el mismo modelo que produjo las variantes es contexto limpio con
sangre contaminada. Las tres defensas se acumulan: **juez de otra familia de modelo que
los escritores**, **ensemble de jueces** con decisión por mayoría, y **randomización de
posición** de las variantes.

### El verificador se sienta sobre la señal cruda, no sobre la curada

Si el nodo que verifica recibe la lista que otro nodo (o el propio orquestador
contaminado) ya filtró, hereda su omisión y valida felizmente lo que sí subió. Dale la
señal primaria —los turnos originales, el documento original, el diff completo— y hazle
**dos preguntas, no una**: ¿lo producido corresponde a esta señal? y **¿hay señal que no
produjo nada?** La segunda es la que atrapa la omisión, y es la que nadie hace por default.

La señal primaria se **extrae mecánicamente**, no se entrega curada ni completa: los turnos
del usuario, no la sesión entera con mi razonamiento adentro; el documento original, no mi
resumen de él. Entregar la sesión completa vuelve a contaminar al verificador con las
racionalizaciones que existe para no compartir; entregar la lista curada lo ciega. La
extracción mecánica es el único punto medio que no depende de mi buena fe.

### Verificar la fidelidad comparando dos lecturas frías

Cuando el grafo **transforma** un artefacto en vez de juzgarlo (reescribir, editar, resumir,
traducir), el invariante en riesgo no es la completitud sino la **voz**: mensaje, tono e
intención del autor. Se verifica con dos lectores fríos independientes —uno lee SOLO el
original, otro SOLO la versión nueva, ninguno ve al otro— y se comparan sus dos
descripciones. Si divergen, hubo drift y se revierte. Es evidencia, no impresión, y aplica
a cualquier transformación de texto, no solo a las skills de documentos.

## Qué hace el orquestador con lo que vuelve

El grafo **no cierra el loop solo**. Cuando un nodo de verificación marca un hallazgo como
dudoso, el script no lo descarta ni lo arregla: lo devuelve etiquetado y **para**. El
orquestador entonces (1) abre el artefacto real y confirma o mata el hallazgo a mano —
verificación de fantasmas—, (2) rankea por daño real, no por sofisticación, y (3) escribe.
Automatizar ese paso convierte una disciplina de fantasmas en un agente parchando sobre
alucinaciones, y ningún nodo tiene el contexto para decidirlo. Corolario práctico: el `return`
del script es un informe con etiquetas, nunca un veredicto ejecutado.

## Andamiaje mínimo

Esto **no es JavaScript autónomo**: `agent()`, `pipeline()`, `parallel()`, `phase()`, `log()`
y `args` los inyecta el tool `Workflow`, y su contrato exacto (firmas, opciones, límites de
concurrencia) vive en la descripción de ese tool — **léela ahí antes de escribir el script**;
este archivo cubre la forma del grafo, no la API. No hay acceso a filesystem ni a APIs de
Node: todo lo que necesite leer disco lo hace un `agent()` con sus propias tools, o lo derivas
tú antes y lo incrustas.

Presupuesto, siempre a la vista: **`agentes = ancla + (lentes × objetos) + verificadores +
síntesis`**. Cuéntalo antes de correr y compáralo con el tope de ≤6; un grafo de 4 lentes con
un verificador cada una ya son 10 y necesita visto bueno explícito.

`pipeline` por default (cada ítem avanza por todas sus etapas sin esperar a los demás ítems —
es concurrente, no serial); `parallel` solo cuando la etapa siguiente necesita de verdad todos
los resultados juntos (deduplicar, cortar por total cero, comparar entre sí).

```js
export const meta = {
  name: 'nombre-del-grafo',
  description: 'Una linea: que verifica y contra que',
  phases: [{ title: 'Ancla' }, { title: 'Lentes' }, { title: 'Verificar' }],
}

const OBJETO = '<INCRUSTAR>'                       // literal, nunca args
if (OBJETO.includes('<INCRUSTAR')) throw new Error('Incrusta el objeto real')

const PRUEBA_DE_TRABAJO = {                        // en TODO schema de nodo lector
  resumen_leido: { type: 'string', description: 'titulo real y tema del objeto, en una frase' },
}

phase('Ancla')
const ancla = await agent(`...deriva el criterio ANTES de ver ninguna salida...`,
  { label: 'ancla', schema: ANCLA_SCHEMA })

phase('Lentes')
const LENTES = [ /* flancos distintos, no copias */ ]
const hallazgos = await pipeline(
  LENTES,
  (l) => agent(l.prompt, { label: `lente:${l.k}`, phase: 'Lentes', schema: LENTE_SCHEMA }),
  (r, l) => r && agent(`Verifica contra el ancla:\n${ancla}\n\n${JSON.stringify(r)}`,
    { label: `verificar:${l.k}`, phase: 'Verificar', schema: VEREDICTO_SCHEMA })
)

return hallazgos.filter(Boolean)   // fantasmas, ranking y escritura: del ORQUESTADOR
```

## Por qué es un `.md` y no un workflow guardado

Un archivo que los agentes copian a mano sigue siendo **biblioteca**; la versión
**máquina** sería un workflow guardado que las skills invocan por nombre. El runtime lo
soporta —el contrato del tool `Workflow` documenta `workflow(nombre | {scriptPath}, args)`
y una carpeta `.claude/workflows/`, con anidamiento de un solo nivel— ⚠️ confirmar con una
corrida real, todavía no ejecutada.

Lo que bloquea la versión máquina no es el runtime sino la **distribución**: una skill de
Kumo debe funcionar copiada sola a `~/.claude/skills/`, y un workflow guardado vive fuera
de la carpeta de la skill. Mientras eso no se resuelva —por ejemplo, con un instalador que
deposite los workflows compartidos junto con las skills— este archivo es la respuesta
correcta, y es una limitación asumida, no una preferencia.
