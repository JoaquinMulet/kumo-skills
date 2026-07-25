# Esqueleto de verificación multi-agente

La forma reusable de cualquier grafo de verificación de Kumo, y los modos de fallo que
cada instancia pagó por separado. Léelo antes de escribir un `Workflow` nuevo o de
convertir un flujo lineal en grafo. Las skills que ya lo instancian (`doc-completitud`,
`doc-narrativa`, `doc-prueba-de-uso`, `auditoria-de-realidad`,
`verificacion-adversarial`) apuntan acá en vez de recontarlo.

**Estado: v1.** La destilación está cerrada —no se agrega doctrina nueva; un esqueleto que se
reescribe en cada uso no es un esqueleto— pero los **defectos que un test exponga sí se
arreglan**: eso no es otra ronda, es mantenimiento.

La v0 salió de cinco instancias de este patrón. La v1 cerró lo que encontraron **dos pruebas de
uso con calibraciones distintas**, que es la disciplina de `doc-prueba-de-uso`:

- **Lector débil** (mide si la información alcanza): cumplió 6 de 8 criterios del rubric y
  expuso el guard mal generalizado, el contrato del tool que el archivo daba por sabido, qué
  hace el orquestador con un hallazgo dudoso, y un presupuesto escrito pero no operativo.
- **Lector fuerte** (mide si el texto admite una sola lectura): rellenó los huecos sin
  esfuerzo y en cambio encontró cinco **ambigüedades** — qué cuenta como «objeto» y su default,
  si `verificadores` suma o multiplica, si un ancla puede ser puramente estructural cuando la
  tarea es juzgar calidad, cuándo aplica el nodo juez, y una contradicción real entre `pipeline`
  y el chequeo de «cero hallazgos». Aplicando la fórmula al pie de la letra presupuestó 43
  agentes donde el default correcto son 10.

Todos corregidos abajo. La lección de método: el lector débil encuentra lo que **falta**; el
fuerte encuentra lo que se puede **entender mal**, y esos son los defectos que sobreviven toda
revisión porque nadie los ve como vacíos.

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

**Cuando la tarea ES juzgar calidad, el ancla puede ser puramente estructural.** Si lo que
se evalúa es inherentemente semántico («¿este mensaje de error es bueno?», «¿esta prosa
convence?»), no hay nada contable que anclar más allá del inventario de qué existe — y ese
inventario estructural **basta como ancla**. El criterio de calidad no es un ancla: es un
**rubric que escribes TÚ** y que va incrustado en el prompt de cada lente. No gastes un
agente en producir el rubric: sería un ancla blanda innecesaria, con el fantasma que eso
arrastra, para algo que puedes escribir a mano y congelar.

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

### Un nodo vacío es "no testeado", jamás un aprobado

Un agente puede terminar **sin llamar** a la herramienta de salida estructurada y devolver
`null`. El grafo sigue, el conteo final cuadra, y el caso queda sin veredicto disfrazado de
caso resuelto. Pasa sobre todo con **modelo débil + esfuerzo bajo**, que es justo la
combinación barata que uno elige para las corridas grandes. Tres defensas:

1. **Un reintento explícito** por ítem antes de darlo por perdido, con la instrucción
   *"responde ÚNICAMENTE llamando a la herramienta de salida estructurada"*.
2. **Etiqueta el vacío como `NO_TESTEADO`** en el resultado, nunca lo filtres con
   `.filter(Boolean)` antes de contar: filtrar convierte un agujero en un aprobado.
3. **Reporta la cuenta de vacíos junto a la de aciertos.** «11 de 14 respondieron, 11
   correctos» y «11 de 14 correctos» son afirmaciones distintas y solo una es honesta.

El chequeo de «cero hallazgos» es **del orquestador sobre el conjunto ya devuelto**, no un gate
dentro del grafo: se hace cuando la corrida terminó y tienes todos los resultados en la mano.
No lo implementes como una condición intermedia entre etapas —eso obligaría a una barrera que
mata la concurrencia de `pipeline`, y con ítems a medio camino daría falsos «instrumento roto»
sobre los pocos que ya terminaron.

*(Caso real: en un test de descubrimiento de 14 casos, 2 agentes no llamaron al schema. El
resumen decía 11 aciertos y 0 fallos — cierto y engañoso: dos disparadores, uno de ellos
central, no se habían medido.)*

### Los scripts generados van con LF, no CRLF

Si generas el script con un programa (lo correcto cuando inyectas literales derivados en vez
de transcribirlos a mano), escríbelo con **fin de línea LF explícito**. En Windows el
`\r` cuenta como carácter de control y el script es **rechazado antes de ejecutarse**, con un
error que habla de la validación y no de tu archivo. En Python: `open(ruta, 'w',
newline='\n')`.

### El que propone el fan-out necesita tope

Un nodo fresco que propone qué mirar (superficies, variantes, dimensiones) **no cuesta un
agente: cuesta lo que decida abanicar** — es un multiplicador del ancho, no una
constante. Y va a proponer de más justamente porque se puso ahí para mirar lo que el
orquestador no miraba. Su schema lleva tope explícito: *máximo N, ordenadas por peligro
real*. Sin tope, el presupuesto de la corrida lo fija el agente menos informado del grafo.

### El juez: ciego no basta

**Aplica solo cuando el grafo produce varios candidatos que COMPITEN** y hay que elegir o
rankear entre ellos (variantes de un prompt, reescrituras alternativas, propuestas rivales). Si
la síntesis solo reconcilia hallazgos complementarios de lentes distintas —el caso más común—
no hay nada que juzgar y un nodo juez es presupuesto tirado. Cuando sí aplica:

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

Presupuesto, siempre a la vista y **contado antes de correr**:

```
agentes = ancla + (lentes × objetos × (1 + verificadores_por_lente)) + síntesis
```

Dos aclaraciones que la fórmula sola no da, y que sin ellas se subestima el costo por un
factor de N:

- **`verificadores_por_lente` es un multiplicador, no un sumando.** El andamiaje de abajo
  corre un verificador por CADA salida de lente, no uno final para toda la corrida. Con 4
  lentes y un verificador cada una son 8, no 5.
- **`objetos` es cuántas veces se repite el fan-out completo, y su default es 1.** Cuando el
  target es un conjunto (una carpeta, un bundle, varias secciones), la decisión de si es **un
  objeto lógico** —las lentes lo leen entero, `objetos = 1`— o **N objetos independientes** es
  tuya y hay que tomarla explícitamente, porque cambia el costo linealmente. Colapsar a un
  objeto lógico es el default; separar en N se justifica solo si los ítems se juzgan de forma
  independiente y el veredicto de uno no informa al de otro.

*(Cuenta real de un lector que aplicó la fórmula al pie de la letra sobre una carpeta de 5
archivos con 4 lentes y no vio el default: 43 agentes. Con `objetos = 1`, la misma tarea son
10 — que igual cruza el tope de ≤6 y por lo tanto necesita visto bueno explícito. La lección
no es que la fórmula esté mal: es que hacer la cuenta ANTES es la única forma de que la puerta
de la casa signifique algo.)*

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
**máquina** sería un workflow guardado que las skills invocan por nombre. **El runtime lo
soporta: verificado con una corrida real** — un workflow padre invocó
`workflow({ scriptPath })` y recibió de vuelta el objeto completo del hijo, schema-válido
(anidamiento de un solo nivel; el hijo comparte el cupo de concurrencia y el presupuesto
del padre).

Lo que bloquea la versión máquina no es el runtime sino la **distribución**: una skill de
Kumo debe funcionar copiada sola a `~/.claude/skills/`, y un workflow guardado vive fuera
de la carpeta de la skill. Mientras eso no se resuelva —por ejemplo, con un instalador que
deposite los workflows compartidos junto con las skills— este archivo es la respuesta
correcta, y es una limitación asumida, no una preferencia.
