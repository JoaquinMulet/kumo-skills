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

# Doc Storytelling Restructure — de esquema a relato

Convierte un documento correcto pero plano y denso en uno que se **lea como una
historia**, con prosa que explica y referencia técnica ordenada en apéndices. La
garantía clave: **sube el techo (que se lea bien) sin bajar el piso (que nada se
pierda)** — un verificador compara la reescritura contra un inventario del
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

## Cómo ejecutar

1. **Identifica el archivo objetivo.** Pide la ruta absoluta si no está clara.
   Recomienda respaldar/commitear antes, porque reescribe el archivo en su lugar.
2. **Parámetros opcionales:**
   - `editorModel` — modelo de los editores/verificador (lectores baratos).
     Default `haiku`.
3. **Invoca el tool `Workflow`** con el `script` de abajo, **incrustando la ruta del
   documento como constante en el script** — no la pases por `args`: si el harness
   entrega los args como string, `args.docPath` llega `undefined`, los editores
   reciben «Lee SOLO undefined» y la fase de inventario devuelve un checklist-error
   perfectamente schema-válido (caso real). Al recibir el resultado, **verifica el
   inventario antes de seguir**: si no nombra contenido real del documento, la
   corrida entera es inválida.
4. **Al terminar**, muestra al usuario: (a) el **plan de redacción** sintetizado
   (para que lo apruebe o ajuste), (b) el **veredicto de completitud** (COMPLETO /
   qué se repuso). Si el usuario quiere afinar el plan antes de aceptar, puedes
   reusar el plan y reescribir de nuevo.

> El loop hace cinco cosas: **inventaría** el contenido original (para no perder
> nada), pide recomendaciones a **editores con lentes distintas** (narrativa,
> densidad, estructura), **sintetiza** un plan de redacción, **reescribe** según
> el plan, y **verifica** contra el inventario — reponiendo lo que falte.

> **⚠ Documentos con contenido gestionado por generador (citas numeradas, notas al
> pie, numeración continua entre archivos): la variante "Solo el plan" es OBLIGATORIA.**
> Un agente reescritor a ciegas puede separar un marcador de cita de su frase o romper
> el anclaje de la numeración. El flujo correcto: los editores recomiendan → el plan
> lista EDICIONES PUNTUALES (no reescritura total) → **el orquestador ejecuta con
> `Edit`** (marcadores pegados a su frase; cortes de párrafo solo entre oraciones
> completas) → cierre doble: verificación de inventario + **corrida del generador**
> confirmando que el conteo y el anclaje de las citas no cambiaron. (Caso real: 8
> ediciones sobre un capítulo con 21 citas gestionadas — inventario 351/351 presente
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

// Ruta INCRUSTADA, no `args` (ver paso 3 arriba: args-como-string ⇒ undefined):
const doc = '<RUTA-ABSOLUTA-DEL-DOCUMENTO>'
const weak = 'haiku'
if (doc.includes('<RUTA')) throw new Error('Incrusta la ruta real en el script antes de correrlo')

// 1 · INVENTARIO — checklist exhaustivo del contenido original (para verificar al final)
phase('Inventario')
const INV = { type: 'object', properties: { items: { type: 'array', items: { type: 'string' } } }, required: ['items'] }
const inv = await agent(
  `Lee SOLO ${doc}. Extrae un checklist EXHAUSTIVO de TODO el contenido sustantivo: cada dato, cifra, ` +
  `entidad, tabla, regla, ejemplo, definición, diagrama. Un ítem por línea, concreto. Esta lista se usará ` +
  `para verificar que una reescritura no pierda nada.`,
  { label: 'inventario', model: weak, schema: INV }
)
const checklist = (inv?.items || []).map((s, i) => `${i + 1}. ${s}`).join('\n')

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

// 5 · VERIFICACIÓN — la reescritura no debe perder contenido
phase('Verificación')
const VER = { type: 'object', properties: { faltantes: { type: 'array', items: { type: 'string' } }, veredicto: { type: 'string', enum: ['COMPLETO', 'INCOMPLETO'] } }, required: ['faltantes', 'veredicto'] }
let verif = await agent(
  `Lee SOLO ${doc} (ya reescrito). Confirma que CADA ítem de este checklist sigue presente en alguna ` +
  `parte (cuerpo o apéndices); búscalo en todo el archivo antes de marcarlo como faltante:\n${checklist}\n\n` +
  `Devuelve los ítems faltantes (o lista vacía) y el veredicto.`,
  { label: 'verificacion', model: weak, schema: VER }
)
if (verif?.veredicto === 'INCOMPLETO' && verif.faltantes?.length) {
  await agent(
    `La reescritura de ${doc} perdió estos contenidos:\n- ${verif.faltantes.join('\n- ')}\n\nRepónlos en el ` +
    `lugar adecuado (cuerpo o apéndice) sin romper el relato ni la estructura. Edita el archivo en su lugar.`,
    { label: 'reponer-faltantes' }
  )
  verif = await agent(
    `Verifica de nuevo SOLO ${doc} contra el checklist; devuelve faltantes y veredicto:\n${checklist}`,
    { label: 'verificacion-2', model: weak, schema: VER }
  )
}

return { plan, faltantes: verif?.faltantes || [], veredicto: verif?.veredicto || 'DESCONOCIDO' }
```

## Variantes
- **Solo el plan (sin reescribir):** corta el workflow tras la fase `Plan` y
  muéstrale el plan de redacción al usuario para que lo apruebe antes de tocar el
  archivo. Recomendado para documentos grandes o sensibles; **obligatorio** para
  archivos con contenido gestionado por generador (ver advertencia arriba) — ahí
  el plan no va al usuario sino al orquestador, que lo ejecuta con `Edit`.
- **Más lentes:** agrega editores (p. ej. "tono para sponsor no técnico",
  "ruta de lectura por rol") al arreglo `LENTES`.
- **Combo con completitud:** corre primero `doc-completitud` (que no falte
  nada) y luego este (que se lea bien); este loop ya re-verifica completitud al
  final, así no deshace el trabajo del primero.
- **Sin el tool Workflow:** si el entorno no tiene `Workflow` disponible, corre las lentes
  con uno o dos `Agent` secuenciales en vez del fan-out y sintetiza el plan tú mismo. El
  método no cambia —lentes → plan → reescritura → verificación de que no se perdió nada—,
  solo va en serie; conviene igual pausar en el plan para aprobación (variante de arriba).
