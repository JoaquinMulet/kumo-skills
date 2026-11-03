---
name: doc-narrativa
description: >-
  Reestructura un documento denso en un relato claro (storytelling) con más prosa
  explicativa, SIN perder contenido. Úsala cuando un documento técnico esté
  "demasiado denso" — lleno de tablas, listas de campos o bloques de código — y
  quieras que se lea como una historia, para entregarlo a un equipo, un cliente o
  un sponsor. Dispara con frases como "reescríbelo con storytelling", "está muy
  denso, agrega prosa", "reestructura esto en un plan de redacción", "hazlo más
  fácil de entender", "que se lea como un relato", "ordénalo con más sentido
  narrativo". Orquesta con el tool Workflow: editores con lentes distintas
  recomiendan, se sintetiza un plan de redacción, se reescribe, y un verificador
  confirma que quedó igual o más completo (no se pierde nada).
---

# Doc Storytelling Restructure. De esquema a relato

Convierte un documento correcto pero plano y denso en uno que se **lea como una
historia**, con prosa que explica y referencia técnica ordenada en apéndices. La
garantía clave: **sube el techo (que se lea bien) sin bajar el piso (que nada se
pierda)**, un verificador compara la reescritura contra un inventario del
contenido original.

## Cuándo usarla
- Un documento técnico es completo pero abrumador: muchas tablas, listas de
  campos, bullets apilados, poca prosa.
- El usuario quiere storytelling, un hilo conductor, un gancho, transiciones, o
  "que el equipo lo entienda sin sufrir".
- Pide un "plan de redacción" o "reestructurar con más sentido narrativo".

Es la hermana de `doc-completitud`: aquélla asegura que **nada falte**;
ésta asegura que **se lea bien**. Si quieres ambas, corre primero completitud y
luego storytelling (este loop termina verificando que no se haya perdido nada).

> **⚠ Antes de correr esta skill, pasa por `doc-cadena-causal`.** Esta juzga el
> texto *como texto*, si fluye, si es denso, si está ordenado, y por diseño **no
> detecta el concepto nombrado pero no fundado**: el que está presente, definido,
> bien ubicado y hasta con analogía, y del que el lector igual no puede decir
> *por qué existe*. Peor. El plan de redacción que produce reordena y comprime,
> así que sobre un concepto sin fundamento **comprime el síntoma**. Caso real:
> este flujo dejó un capítulo mejor escrito, arco, analogías, fórmulas al
> apéndice, y no tocó el hueco, que el lector encontró después. El orden con
> dependencia real es: completitud → **cadena causal** → narrativa → prueba de uso.

## Si reordenas, vuelve a medir el orden

Esta skill mueve material de sitio. Mover un bloque hacia adelante puede dejar
**usado antes de explicado** un concepto que estaba bien, y ese defecto no se ve
releyendo: cada párrafo sigue leyéndose bien por separado.

Corre el **contrato de vocabulario** después de reescribir, no antes
([`doc-cadena-causal`](../doc-cadena-causal/SKILL.md), «La deuda de orden»). Si
el documento usa estructura en espiral, corre además el guardia de la primera
pasada, que falla si se coló una cifra derivada donde todavía no puede haberla.

## Antes de reescribir: los arreglos ganados se convierten en centinelas

**Esta es la regla que más caro sale saltarse, y aplica a las cuatro skills de
documentación.**

Cada pasada de auditoría (completitud, cadena causal, prueba de uso) termina en
parches al texto. Un parche vive en una redacción concreta. **Cuando el documento
se reescribe, y esta skill reescribe, la redacción cambia y el parche desaparece
sin que nadie lo note**, porque el resultado sigue leyéndose bien: el hueco no
deja hueco visible, deja un texto fluido al que le falta una respuesta.

El inventario duro (encabezados, tablas, cifras) sobrevive porque se verifica
mecánicamente. Los **arreglos semánticos** no sobreviven a nada.

Por eso, antes de invocar la reescritura:

1. **Lista los arreglos que las pasadas anteriores dejaron en el documento**,
   cada «esto no se entendía y lo explicamos» de esta sesión y de las previas.
2. **Convierte cada uno en un centinela**: una frase textual, corta y distintiva,
   en un test de regresión que falla si desaparece. Una línea por arreglo.
3. **Corre el test antes y después de reescribir.** Antes, para comprobar que el
   centinela da verde sobre el texto viejo, un centinela que nunca estuvo en
   verde no prueba nada. Después, para ver qué se cayó.

```python
REQUERIDO = {
    'por que el banco toma el otro lado': 'El banco no se queda con el riesgo: lo pasa',
    'punto base definido':                'la centésima parte de un punto porcentual',
}
```

**El caso real.** Una reescritura estructural completa perdió la explicación de
por qué la contraparte quiere el otro lado del contrato. Las cuatro skills habían
corrido sobre el documento viejo y dieron ese hueco por cerrado. Sobre el nuevo
nadie las volvió a correr. **Lo cazó el test de regresión**, y solo porque en una
sesión anterior ese arreglo se había escrito como centinela. De los otros arreglos
de la lista, diez aparecieron como «perdidos» y en realidad estaban reformulados:
hubo que revisarlos uno por uno para separar «reformulado» de «perdido». Ese
ejercicio de separar es justamente el trabajo que el centinela existe para hacer,
y por eso el centinela debe apuntar a la **idea mínima** (`sin haberlo pedido`,
`lo decide la norma`) y no a la frase larga. Una frase larga falla con cualquier
reescritura y se vuelve ruido.

Corolario. Una reescritura estructural invalida las auditorías previas. No
son arreglos sobre un texto que sigue ahí. Son arreglos sobre un texto que ya no
existe. Si la estructura cambió, el ciclo se corre otra vez sobre el texto nuevo
, y el test de regresión es lo que hace que la segunda corrida sea barata en vez
de empezar de cero.

## Cómo ejecutar

1. **Identifica el archivo objetivo.** Pide la ruta absoluta si no está clara.
   Recomienda respaldar/commitear antes, porque reescribe el archivo en su lugar.
2. **Parámetros opcionales:**
   - `editorModel`. Modelo de los editores/verificador (lectores baratos).
     Default `haiku`.
3. **Deriva el inventario DURO tú mismo, antes de invocar nada.** Todo lo contable se
   extrae mecánicamente y se incrusta en el script como constante, no se le pregunta a
   un agente lo que un `grep` sabe:

   ```bash
   grep -nE '^#{1,6} '            doc.md   # encabezados
   grep -nE '^\|'                 doc.md   # filas de tabla
   grep -noE '[0-9][0-9.,]*%?'    doc.md   # cifras
   grep -nE '^```'                doc.md   # bloques de código
   ```

   (En PowerShell: `Select-String -Path doc.md -Pattern '^#{1,6} '`, etc.)

4. **Invoca el tool `Workflow`** con el `script` de abajo, **incrustando la ruta del
   documento y el inventario duro como constantes** (contrato del caller del esqueleto
   compartido: una ruta vacía hace que los editores lean «SOLO undefined» y la fase de
   inventario devuelva un checklist-error schema-válido, lee
   [`desarrollo-riguroso/reference/esqueleto-de-verificacion.md`](../desarrollo-riguroso/reference/esqueleto-de-verificacion.md)
   antes de tocar el script). Al recibir el resultado, **verifica el inventario blando
   antes de seguir**: si no nombra contenido real del documento, la corrida es inválida.

   **Los dos inventarios NO se mezclan en una sola lista.** El duro es un oráculo duro y
   por eso puede disparar reposición automática. El blando lo produjo un agente y sus
   faltantes van **a ti**, nunca al parchador. Unirlos sube el recall y también los
   fantasmas, y cada ítem alucinado que entre al ancla es contenido inexistente que un
   reparador automático va a escribir en el documento sin que nadie lo decida. Es
   «nombrar residuales» del oráculo blando, aplicado al grafo.
5. **Al terminar**, muestra al usuario: (a) el **plan de redacción** sintetizado
   (para que lo apruebe o ajuste), (b) el **veredicto de completitud** del inventario
   duro (COMPLETO / qué se repuso), y (c) los **faltantes del inventario blando**, que
   resuelves tú a mano: cada uno se busca con `Grep` en el documento antes de reponerlo
, si el agente lo inventó, se descarta. Si el usuario quiere afinar el plan antes de
   aceptar, puedes reusar el plan y reescribir de nuevo.

> El loop hace cinco cosas: **inventaría** lo semántico del original (el ancla dura,
> lo contable, ya la derivaste tú con `grep`), pide recomendaciones a **editores con
> lentes distintas** (narrativa, densidad, estructura), **sintetiza** un plan de
> redacción, **reescribe** según el plan, y **verifica contra los dos inventarios**
>, repone automático lo que falte del duro, y te devuelve los faltantes del blando
> para que los confirmes con `Grep` antes de tocar el documento.

> **⚠ Documentos con contenido gestionado por generador (citas numeradas, notas al
> pie, numeración continua entre archivos): la variante "Solo el plan" es OBLIGATORIA.**
> Un agente reescritor a ciegas puede separar un marcador de cita de su frase o romper
> el anclaje de la numeración. El flujo correcto: los editores recomiendan → el plan
> lista EDICIONES PUNTUALES (no reescritura total) → **el orquestador ejecuta con
> `Edit`** (marcadores pegados a su frase. Cortes de párrafo solo entre oraciones
> completas) → cierre doble: verificación de inventario + **corrida del generador**
> confirmando que el conteo y el anclaje de las citas no cambiaron. (Caso real: 8
> ediciones sobre un capítulo con 21 citas gestionadas, inventario 351/351 presente
> y generador sin cambios.)

## Script para el tool Workflow

```js
export const meta = {
  name: 'doc-narrativa',
  description: 'Reestructura un documento denso en un relato sin perder contenido',
  phases: [
    { title: 'Inventario' },
    { title: 'Editorial' },
    { title: 'Plan' },
    { title: 'Reescritura' },
    { title: 'Verificación' },
  ],
}

// Ruta INCRUSTADA con guard (contrato del caller del esqueleto compartido):
const doc = '<RUTA-ABSOLUTA-DEL-DOCUMENTO>'
const weak = 'haiku'
if (doc.includes('<RUTA')) throw new Error('Incrusta la ruta real en el script antes de correrlo')

// ANCLA DURA — derivada MECANICAMENTE por el orquestador antes de invocar (paso 3 arriba:
// grep de encabezados, filas de tabla, cifras, bloques de codigo). Es un oraculo DURO: sus
// faltantes SI pueden disparar reposicion automatica, porque no puede alucinar items.
const DURO = [ /* '## Metodologia', '| Region | Monto |', '61%', ... — literales del grep */ ]
if (!DURO.length) throw new Error('Incrusta el inventario duro (grep) antes de correrlo')
const checklistDuro = DURO.map((s, i) => `${i + 1}. ${s}`).join('\n')

// 1 · INVENTARIO BLANDO — lo SEMANTICO, que el grep no ve (reglas, ejemplos, definiciones,
// relaciones). Lo produce un agente, asi que es un oraculo BLANDO: sus faltantes van al
// ORQUESTADOR, jamas al parchador automatico — un item alucinado se convertiria en
// contenido inexistente escrito en el documento.
phase('Inventario')
const INV = { type: 'object', properties: {
  resumen_leido: { type: 'string', description: 'titulo y tema del documento en una frase — prueba de lectura' },
  items: { type: 'array', items: { type: 'string' } } }, required: ['resumen_leido', 'items'] }
const inv = await agent(
  `Lee SOLO ${doc}. Extrae un checklist del contenido SEMANTICO sustantivo: reglas, ejemplos, ` +
  `definiciones, entidades, relaciones y afirmaciones. NO listes encabezados, filas de tabla ni ` +
  `cifras sueltas — esos ya se extrajeron mecanicamente. Un item por linea, concreto.`,
  { label: 'inventario-blando', model: weak, schema: INV }
)
const checklistBlando = (inv?.items || []).map((s, i) => `${i + 1}. ${s}`).join('\n')

// 2 · EDITORIAL — recomendadores con lentes distintas, en paralelo
phase('Editorial')
const LENTES = [
  { k: 'narrativa', p: 'Eres EDITOR de arco narrativo / storytelling. Define en 1 frase el MENSAJE CENTRAL del documento; identifica el GANCHO (el problema o dato que arrastra al lector); propón el arco en 5-7 actos con título (problema → descubrimiento → solución → prueba); señala el "momento ajá". Da 5-8 recomendaciones concretas Y di explícitamente cuáles partes YA funcionan y no hay que tocar.' },
  { k: 'densidad', p: 'Eres EDITOR de legibilidad. El documento está demasiado denso. Señala las 5 zonas más densas (tablas, listas de campos, código apilado); di qué PROSA explicativa agregar y dónde; qué ANALOGÍAS cotidianas ayudarían; y qué conviene mover a un APÉNDICE de referencia para aligerar el cuerpo.' },
  { k: 'estructura', p: 'Eres EDITOR de estructura/arquitectura de la información. Diagnostica el orden de secciones, las REDUNDANCIAS (ideas repetidas) y la MEZCLA DE NIVELES (relato vs referencia técnica). Propón una estructura reordenada (lista de secciones con una línea de propósito) y la SEÑALIZACIÓN a agregar (transiciones entre secciones, "qué te llevas" al cierre de cada una).' },
]
const recs = (await parallel(
  LENTES.map(l => () =>
    agent(`${l.p}\n\nLee SOLO ${doc}. Cita secciones reales del documento. Sé concreto y conciso.`,
      { label: `editor-${l.k}`, model: weak, phase: 'Editorial' })
  )
)).filter(Boolean)

// 3 · PLAN — síntesis en un plan de redacción
phase('Plan')
const plan = await agent(
  `Eres el REDACTOR JEFE. Con estas recomendaciones de tres editores:\n\n${recs.join('\n\n---\n\n')}\n\n` +
  `Sintetiza UN plan de redacción accionable para reescribir ${doc} como relato (léelo tú también con Read antes de decidir: los editores pueden estar criticando una impresión desactualizada del documento, y tu plan debe declarar los NO-OPS con su porqué). Incluye: (a) el mensaje ` +
  `central y el gancho de apertura; (b) los actos en orden, cada uno con su propósito y de qué sección ` +
  `actual sale; (c) qué baja a APÉNDICES de referencia; (d) reglas de prosa (un párrafo introduce cada ` +
  `tabla/figura, un "qué te llevas" cierra cada acto, analogías donde ayuden, transiciones entre actos); ` +
  `(e) qué fusionar o cortar por redundante. Resuelve tú las tensiones entre editores y deja un plan único.`,
  { label: 'plan-redaccion' }
)

// 4 · REESCRITURA — siguiendo el plan, editando el archivo en su lugar
phase('Reescritura')
await agent(
  `Reescribe COMPLETO el archivo ${doc} siguiendo este plan de redacción:\n\n${plan}\n\n` +
  `Reglas estrictas: el CUERPO se lee como relato, con prosa que explica (no solo bullets); el detalle ` +
  `técnico (tablas de campos, listas largas, reglas de implementación, glosario) baja a APÉNDICES ` +
  `claramente rotulados; NO pierdas NADA de contenido — todo lo técnico debe seguir presente, en el ` +
  `cuerpo o en un apéndice; conserva diagramas, figuras y cifras tal cual. Mantén el mismo formato de ` +
  `archivo (si es HTML, sigue siendo HTML válido y autocontenido). Edita el archivo en su lugar.`,
  { label: 'reescritura' }
)

// 5 · VERIFICACIÓN — dos anclas, dos destinos. La dura puede reponerse automatico; la
// blanda vuelve al orquestador SIN tocar el documento.
phase('Verificación')
const VER = { type: 'object', properties: { faltantes: { type: 'array', items: { type: 'string' } }, veredicto: { type: 'string', enum: ['COMPLETO', 'INCOMPLETO'] } }, required: ['faltantes', 'veredicto'] }
const contra = (checklist, label) => agent(
  `Lee SOLO ${doc} (ya reescrito). Confirma que CADA ítem de este checklist sigue presente en alguna ` +
  `parte (cuerpo o apéndices); búscalo en todo el archivo antes de marcarlo como faltante:\n${checklist}\n\n` +
  `Devuelve los ítems faltantes (o lista vacía) y el veredicto.`,
  { label, model: weak, schema: VER }
)

let duro = await contra(checklistDuro, 'verificacion-duro')
if (duro?.veredicto === 'INCOMPLETO' && duro.faltantes?.length) {
  // Reposicion AUTOMATICA solo sobre el ancla dura: cada item existe en el original por
  // construccion (salio de un grep), asi que no hay fantasma que insertar.
  await agent(
    `La reescritura de ${doc} perdió estos contenidos:\n- ${duro.faltantes.join('\n- ')}\n\nRepónlos en el ` +
    `lugar adecuado (cuerpo o apéndice) sin romper el relato ni la estructura. Edita el archivo en su lugar.`,
    { label: 'reponer-faltantes' }
  )
  duro = await contra(checklistDuro, 'verificacion-duro-2')
}

// El ancla BLANDA no dispara escritura: se devuelve para que el orquestador verifique con
// Grep cada faltante contra el documento y descarte los alucinados antes de reponer.
const blando = await contra(checklistBlando, 'verificacion-blando')

return {
  plan,
  duro: { faltantes: duro?.faltantes || [], veredicto: duro?.veredicto || 'DESCONOCIDO' },
  blandoParaRevisionManual: blando?.faltantes || [],
  pruebaLectura: inv?.resumen_leido || '(sin prueba de lectura — corrida sospechosa)',
}
```

## Variantes
- **Solo el plan (sin reescribir).** Corta el workflow tras la fase `Plan` y
  muéstrale el plan de redacción al usuario para que lo apruebe antes de tocar el
  archivo. Recomendado para documentos grandes o sensibles. **obligatorio** para
  archivos con contenido gestionado por generador (ver advertencia arriba), ahí
  el plan no va al usuario sino al orquestador, que lo ejecuta con `Edit`.
- **Más lentes.** Agrega editores (p. ej. "tono para sponsor no técnico",
  "ruta de lectura por rol") al arreglo `LENTES`.
- **Combo con completitud.** Corre primero `doc-completitud` (que no falte
  nada) y luego este (que se lea bien). Este loop ya re-verifica completitud al
  final, así no deshace el trabajo del primero.
- **Sin el tool Workflow.** Si el entorno no tiene `Workflow` disponible, corre las lentes
  con uno o dos `Agent` secuenciales en vez del fan-out y sintetiza el plan tú mismo. El
  método no cambia, lentes → plan → reescritura → verificación de que no se perdió nada,
  solo va en serie. Conviene igual pausar en el plan para aprobación (variante de arriba).
