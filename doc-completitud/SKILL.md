---
name: doc-completitud
description: >-
  Endurece un documento hasta que un lector "en frío" (un modelo débil, sin
  contexto previo y leyendo SOLO el archivo) pueda explicar cada sección sin
  vacíos. Úsala para volver un documento autoexplicativo, verificar que esté
  completo, o cerrar huecos de contexto antes de entregarlo a otro equipo —
  sirve para specs, READMEs, propuestas de diseño, skills, .md, .html o
  cualquier texto. Dispara con frases como "haz este doc autoexplicativo",
  "verifica que se entienda solo", "déjalo a prueba de Haiku", "cierra los
  vacíos del documento", "que cualquiera lo entienda sin contexto", "asegúrate
  que esté completo". Orquesta con el tool Workflow un agente lector ciego que
  marca los vacíos; el parchado lo hace EL PROPIO ORQUESTADOR (que tiene el
  contexto del documento), nunca un agente editor a ciegas — en bucle hasta
  cero vacíos bloqueantes.
---

# Doc Completeness Loop. "a prueba de Haiku"

Hace que un documento se explique solo. La idea central: **usar el modelo más
débil como vara**. Si un lector barato y sin contexto, leyendo únicamente el
archivo, logra explicar *qué dice, qué hay que hacer, por qué y el porqué del
porqué* de cada sección, entonces el documento está completo. Si él lo entiende,
cualquiera lo entiende.

## El reparto de roles (lo más importante)

Hay dos papeles, y NO se intercambian:

- **Lector = agente ciego.** Un subagente nuevo, sin memoria ni contexto, que lee
  SOLO el archivo. Su ceguera es justo lo que lo hace valioso: detecta los huecos
  que tú ya no ves porque los rellenas de memoria. Va en el Workflow.
- **Editor = TÚ, el orquestador.** El que invoca esta skill es quien parcha, porque
  **tiene todo el contexto** (el repo, el dominio, la intención del documento). Un
  agente editor a ciegas parcharía peor: inventa, se desvía del estilo, o malinterpreta.
  Por eso el parchado **nunca** se delega a un subagente. Lo haces tú con `Edit`.

En una frase: **el ciego encuentra, el que sabe arregla.**

## Cuándo usarla
- El usuario quiere que un documento se entienda sin contexto previo (hand-off a
  otro equipo, onboarding, entrega a un cliente, una skill autocontenida).
- Quiere verificar que una spec/propuesta/README no tenga huecos, siglas sin
  definir ni saltos lógicos.
- Pide explícitamente "que un Haiku lo explique", "a prueba de tontos", "que se
  entienda solo".

NO la uses para mejorar el estilo o la narrativa de un documento, para eso está
la skill hermana `doc-narrativa`. Esta solo sube el **piso** (que
nada falte), no el techo (que se lea lindo).

Tampoco la uses para saber si cada concepto **se sostiene solo**: esta skill
verifica que el ítem *esté presente*, y un concepto puede estar presente,
definido y explicado sin que el lector pueda decir nunca **por qué existe** ni
**si le aplica**. Ese eje lo cubre `doc-cadena-causal`, y va inmediatamente
después de esta: completitud → **cadena causal** → narrativa → prueba de uso.

## Cómo ejecutar

El bucle lo conduces **tú**, alternando entre el Workflow (que solo audita) y tus
propias ediciones:

1. **Identifica el/los archivo(s) objetivo.** Pide la ruta absoluta si no está clara.
   Soporta un solo documento o un **bundle** (un archivo principal + sus referencias,
   p.ej. una skill con `SKILL.md` + `references/*.md`): pásalos todos y el lector
   juzga el conjunto, abriendo las referencias que el principal menciona.
2. **Parámetros** (defaults salvo que el usuario pida otra cosa):
   - `readerModel`. El "lector débil" que mide la comprensión. Default `haiku`.
   - `readers`. Cuántos lectores ciegos independientes por ronda. Default `2`
     (dos lecturas en frío divergen y cubren más. Útil para cazar más huecos).
   - `maxRounds`. Tope de iteraciones que **tú** correrás. Default `5`.
3. **El bucle (lo corres tú):**
   - a. **Audita:** invoca el tool `Workflow` con el `script` de abajo (reader-only).
        Te devuelve los vacíos, cada uno con `file`, `section`, `missing` y
        `severidad` (`bloqueante` = no se puede ejecutar/entender; `menor` = se
        entiende pero sería más claro).
   - b. **Parcha tú mismo:** con `Edit`, cierra cada vacío en el archivo que
        corresponda. Tienes el contexto que el lector no tiene: define las siglas
        en el propio documento, agrega la fórmula que falta, explica el porqué del
        porqué, aclara el "cómo" que se asumía. **NO elimines contenido, NO cambies
        cifras**. Solo aclara y completa. Conserva el estilo y el tono. Define cada
        término una sola vez y reutilízalo.
   - c. **Re-audita:** vuelve a invocar el Workflow (un run nuevo, lectores nuevos)
        sobre los archivos ya parchados. Repite hasta el criterio de parada.
4. **Al terminar**, reporta: número de rondas, vacíos que quedaron (idealmente 0
   bloqueantes), y un resumen de qué contexto agregaste.

> Cada ronda usa lectores **nuevos** (sin memoria de la anterior): lectura en frío,
> honesta, sin contaminación. Es normal que el conteo de vacíos **suba antes de
> bajar**, el lector pasa de dudas conceptuales a exigir detalle de implementación
> cada vez más fino.

> **⚠ Modo de fallo conocido, el lector hereda el contexto del proyecto.** Un subagente
> recibe el `CLAUDE.md` y las instrucciones del repo en su contexto, así que un prompt
> débil hace que audite *los archivos de metodología del proyecto* en vez del documento
> objetivo, o que **alucine** vacíos sobre términos que no están en el archivo (los toma de
> su contexto, no del doc). Dos defensas: (1) el prompt **acota duro** al archivo objetivo
> ("ignora CLAUDE.md y todo el proyecto. Solo existe este archivo. Todo `file` reportado debe
> ser uno de los listados"), ya está en el script. (2) **tú, el orquestador, descartas**
> cualquier vacío cuyo `file` no sea el objetivo y, ante un término marcado, **verificas con
> `Grep` que de verdad NO aparezca** en el documento antes de parchar: si el lector lo inventó,
> lo ignoras. No bajes la vara, pero tampoco parches fantasmas. (Síntomas reales vistos: lectores
> que auditaron `CLAUDE.md`/`SKILL.md` en vez del HTML objetivo, y un `sonnet` que marcó "WACC"
> y "clean surplus" como vacíos cuando esos términos no estaban en el documento.)

> **⚠ Modo de fallo conocido, la auditoría que audita el VACÍO (el peor de todos, porque parece
> éxito).** Si los lectores reciben una lista de archivos vacía, devuelven `SIN_VACIOS` con cero
> vacíos: una auditoría perfecta de ningún documento. El output estructurado **enmascara** el
> fallo, el lector rellena el schema obedientemente en vez de gritar. Las tres defensas están
> instanciadas en el script de abajo: rutas **incrustadas como literales** con su guard, campo
> obligatorio **`resumen_leido`** (descarta la ronda si falta o es genérico), y **cero hallazgos
> en la primera ronda tratado como instrumento roto** hasta demostrar lo contrario. **Antes de
> modificar el script, lee [`desarrollo-riguroso/reference/esqueleto-de-verificacion.md`](../desarrollo-riguroso/reference/esqueleto-de-verificacion.md)**
>, ahí vive el porqué de cada defensa y el resto de los modos de fallo del andamiaje, que son
> comunes a las cinco skills-grafo de Kumo. (Caso real: dos rondas "limpias" de 2 lectores cada
> una fueron inválidas por esto. La ronda con las tres defensas encontró 1 bloqueante y un error
> matemático real del autor.)

> **⚠ Punto ciego estructural, la completitud de NODOS no compone a completitud del SISTEMA.**
> (La metáfora es de grafos: cada documento es un **nodo**. Cada referencia o dependencia de un
> documento hacia otro es una **arista**. Esta skill audita nodos, un documento a la vez.)
> La regla «una referencia explícita a otro documento cuenta como definición» es correcta para medir
> la autosuficiencia de UN documento, y exime exactamente las ARISTAS: ningún lector individual
> audita si el puntero apunta a algo que existe y contiene lo prometido, si las obligaciones
> cruzadas están operacionalizadas en AMBOS lados (A declara «B lo hace rutina» pero B no lo
> incluye), ni si existe una **ruta de lectura garantizada** que haga que el documento apuntado se
> lea cuando se necesita, un puntero que nadie sigue es letra muerta. Para un conjunto de
> documentos vinculados (skills que se referencian entre sí, un `CLAUDE.md` + su estándar), corre
> además la **auditoría de grafo**: lectores con TODOS los archivos del conjunto cuya única tarea es
> auditar las aristas, (1) cada referencia resuelve a contenido real en el destino, (2) cada
> obligación cruzada existe en los dos lados, (3) cada dependencia funcional declara cuándo y cómo
> se lee el documento del que depende. (Caso real: cuatro rondas de lectores dieron por completa una
> skill cuyo estándar de referencia podía no leerse NUNCA en una sesión real, la regla de género
> eximió la arista y nadie la miró. Lo encontró el usuario, no el aparato.)

> **Nota, la cláusula aritmética paga su costo.** Exigir al lector que pueda «reproducir cada paso
> aritmético» no solo caza prosa floja: caza errores del AUTOR. (Caso real: en un capítulo de
> finanzas, un lector recalculó un ejemplo y descubrió que una afirmación era matemáticamente falsa
>, el despeje trataba como constante una variable que dependía del precio evaluado. Obligó a
> reformular la fórmula central de la sección, no la prosa.) No quites esa cláusula del prompt
> para acelerar la ronda.

> **⚠ Modo de fallo conocido, el glosario remoto no basta para términos *load-bearing*. Defínelos
> inline.** En un bundle, un término *crítico* (uno que sostiene un riesgo, una cifra o el argumento
> central) definido SOLO en el glosario de otro archivo se marca igual como **bloqueante**, ronda tras
> ronda: el lector ciego recorre el archivo donde el término se *usa* y no abre el glosario del archivo
> que lo *define*. La pista de que estás ante esto: el mismo término reaparece como vacío aunque YA lo
> agregaste al glosario compartido. La defensa NO es repetir "está en el glosario": es **definirlo inline
> en el punto de uso** (un paréntesis breve la primera vez que aparece en ese archivo). Regla práctica:
> glosario para términos de comodidad. **inline** para los que cargan un riesgo o una cifra del veredicto.
> (Caso testigo: "ICB" y "FDP" estaban en el glosario y aun así fueron bloqueantes dos rondas seguidas
> hasta definirlos inline donde frenan el crecimiento del negocio.)

> **Nota de convergencia, con `sonnet` el loop baja a 0 bloqueantes pero nunca a 0 menores.** Con
> lectores `sonnet` (vara más alta que el `haiku` estándar) el conteo de bloqueantes oscila en 1-3
> varias rondas, cada vez en un archivo distinto y más fino: pasa de huecos conceptuales a
> inconsistencias aritméticas cruzadas y citas faltantes, y por último a "este dato no muestra su
> derivación". Eso es señal de **éxito**, no de estancamiento: para cuando una ronda vuelve con **0
> bloqueantes** (verdict `SOLO_MENORES`). Los menores residuales, jerga estándar, una cifra sin su
> aritmética completa, una conversión FX sin tasa, son la cola fina aceptable. Perseguirlos uno a uno
> infla el documento. Dos sub-lecciones que ahorran rondas: (1) **arregla las inconsistencias numéricas
> cruzadas de verdad** (la misma cifra distinta entre dos archivos, una suma que no cuadra), esas
> escalan de `menor` a `bloqueante` con lectores nuevos. (2) cuando un número es un **juicio** (un
> supuesto, una estimación), decláralo como tal y muestra su composición, en vez de dejarlo como punto-
> estimado huérfano que el lector no puede reproducir.

## Criterio de parada (evita el bucle infinito y el bloat)

Un lector ciego **siempre** encontrará algo más fino que pedir (el límite exacto de
un recorte, qué hacer con un caso de banco, etc.). Si parchas cada micro-detalle, el
documento se infla y contradice su propósito. Reglas de convergencia:

- **Para cuando no queden vacíos `bloqueante`** y el documento sea ejecutable por un
  operador competente (no por un autómata literal). Los `menor` residuales son
  aceptables.
- **Distingue vacío de borde de juicio.** Si el documento delega a propósito ciertos
  casos límite al criterio del lector (p.ej. una sección "principio de juicio"), eso
  **no** es un vacío: el documento puede declarar explícitamente que los bordes no
  cubiertos se resuelven con juicio, y eso cierra la clase entera de "¿y si pasa X
  raro?" sin una regla por cada borde.
- **No bajes la vara para ganar.** No edites el prompt del lector para que deje de
  encontrar cosas. Lo legítimo es enfocar el criterio de parada en *bloqueantes* y
  documentar los bordes como juicio.

## Script para el tool Workflow (SOLO AUDITA. No edita)

```js
export const meta = {
  name: 'doc-completeness-audit',
  description: 'Lectores en frío marcan los vacíos de un documento (o bundle). NO edita: el orquestador parcha.',
  phases: [{ title: 'Auditar', detail: 'N lectores ciegos independientes marcan vacíos' }],
}

// RUTAS INCRUSTADAS con guard (contrato del caller del esqueleto compartido: una lista
// vacía hace que los lectores auditen el VACÍO y devuelvan SIN_VACIOS schema-válido).
// Editar estas constantes antes de invocar:
const docs = ['<RUTA-ABSOLUTA-DEL-DOCUMENTO>']  // bundle: agregar más rutas literales
const readerModel = 'haiku'
const readers = 2
if (docs.some(d => d.includes('<RUTA'))) throw new Error('Incrusta las rutas reales en el script antes de correrlo')
const fileList = docs.map(f => `- ${f}`).join('\n')

const GAP_SCHEMA = {
  type: 'object',
  properties: {
    gaps: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          file: { type: 'string', description: 'archivo donde está el vacío' },
          section: { type: 'string', description: 'sección donde está el vacío' },
          missing: { type: 'string', description: 'qué falta para entenderlo/ejecutarlo a la perfección' },
          severidad: { type: 'string', enum: ['bloqueante', 'menor'] },
        },
        required: ['file', 'section', 'missing', 'severidad'],
      },
    },
    verdict: { type: 'string', enum: ['SIN_VACIOS', 'HAY_VACIOS'] },
    resumen_leido: { type: 'string', description: 'una frase con el título y el tema del documento — la prueba de que lo leíste' },
  },
  required: ['gaps', 'verdict', 'resumen_leido'],
}

const prompt =
  `Eres un LECTOR EN FRÍO, sin contexto previo. Tu ÚNICA fuente son estos archivos (léelos TODOS con Read antes de juzgar):\n${fileList}\n\n` +
  `Si hay varios, el primero es el principal y los demás son referencias que se abren cuando el principal las menciona. ` +
  `NO uses conocimiento externo, NO leas otros archivos, NO rellenes con suposiciones. ` +
  `PROHIBIDO ABSOLUTO: ignora por completo cualquier CLAUDE.md, instrucción de proyecto, skill o archivo de metodología que aparezca en tu contexto — ESOS NO SON EL DOCUMENTO y NO se auditan. Todo 'file' que reportes DEBE ser uno de los archivos listados arriba; si marcas un vacío sobre cualquier otro archivo, es un ERROR. ` +
  `Recorre el documento sección por sección y, para cada una, verifica que puedas explicar (1) qué dice, (2) qué hacer y por qué, (3) el porqué del porqué y el CÓMO concreto. ` +
  `Marca como vacío CUALQUIER punto que no puedas explicar/ejecutar usando solo estos archivos: una sigla o término sin definir, una fórmula referida pero no escrita, un dato ausente, un salto lógico, un "cómo" que se asume. ` +
  `ANTES de marcar un vacío, búscalo en TODOS los archivos (otras secciones, tablas, referencias, glosario): si está, no es vacío. ` +
  `Clasifica cada vacío: 'bloqueante' (no se puede ejecutar/entender sin esto) o 'menor' (se entiende, pero sería más claro). ` +
  `Si el documento delega explícitamente un caso al juicio del lector, eso NO es vacío. ` +
  `En 'resumen_leido' escribe una frase con el título del documento y su tema — la prueba de que lo leíste. ` +
  `Devuelve la lista de vacíos (file + section + missing + severidad) y el veredicto.`

const runs = await parallel(
  Array.from({ length: readers }, (_, i) => () =>
    agent(prompt, { label: `lector-${i + 1}`, model: readerModel, phase: 'Auditar', schema: GAP_SCHEMA })
  )
)

const all = runs.filter(Boolean)
const gaps = all.flatMap(r => r.gaps || [])
const bloqueantes = gaps.filter(g => g.severidad === 'bloqueante')
log(`${all.length} lectores · ${gaps.length} vacíos (${bloqueantes.length} bloqueantes)`)
return {
  verdict: bloqueantes.length ? 'HAY_VACIOS' : (gaps.length ? 'SOLO_MENORES' : 'SIN_VACIOS'),
  bloqueantes,
  menores: gaps.filter(g => g.severidad === 'menor'),
  por_lector: all.map((r, i) => ({ lector: i + 1, verdict: r.verdict, n: (r.gaps || []).length })),
}
```

Tras recibir los vacíos, **tú** los parchas con `Edit` (paso 3b) y vuelves a invocar
el Workflow (paso 3c) hasta que `verdict` sea `SIN_VACIOS` o `SOLO_MENORES`.

## Su punto ciego: «presente» no es «a tiempo»

Esta skill cuenta **presencia**. Un concepto usado seis capítulos antes de
explicarse está presente, así que **pasa**, y es el defecto que más se denuncia
como «no se entiende nada». Presencia y orden son ejes distintos: el inventario
completo puede estar entero y el documento seguir siendo ilegible.

El orden se mide aparte, con un contrato de vocabulario:
[`doc-cadena-causal`](../doc-cadena-causal/SKILL.md), sección «La deuda de orden».

## Tus hallazgos deben sobrevivir a la próxima reescritura

Los parches que produce esta skill viven en una redacción concreta y **no
sobreviven a una reescritura del documento**: la redacción cambia, el arreglo
desaparece y el resultado sigue leyéndose bien, así que nadie lo nota.

Antes de cerrar, convierte cada arreglo en un **centinela**, una frase textual,
corta y distintiva, dentro de un test de regresión que falle si desaparece. La
doctrina completa, con el caso real que la originó, está en
[`doc-narrativa`](../doc-narrativa/SKILL.md), sección «Antes de reescribir».

## Variantes
- **Solo auditar (sin parchar):** corre el Workflow una vez y reporta los vacíos.
  Útil para un "¿qué le falta a este doc?".
- **Lector más exigente:** sube `readerModel` a `sonnet` para una vara más alta
  (encuentra vacíos más sutiles. "a prueba de Haiku" es el estándar barato). Para la
  ronda de **cierre**, un solo lector `sonnet` enfocado en bloqueantes da un veredicto
  fiable de "ejecutable / bloqueado".
- **Doc muy largo:** si el archivo es enorme, parte el documento y corre el loop por
  secciones para que el lector no se sature.
- **Sin el tool Workflow:** si el entorno no tiene `Workflow` disponible (o el doc es
  corto), corre el paso de auditoría con un solo `Agent` (`model: haiku`) por ronda en vez
  del fan-out. El método es idéntico, lector ciego audita → el orquestador parcha → lector
  nuevo re-audita, y solo pierdes los lectores en paralelo. Para una o dos secciones alcanza.
