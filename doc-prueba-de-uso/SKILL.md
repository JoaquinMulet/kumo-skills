---
name: doc-prueba-de-uso
description: >-
  Valida un documento con la PRUEBA DE USO: un lector frío (modelo débil, sin
  contexto, leyendo SOLO la sección) debe poder EJECUTAR la tarea que esa
  sección existe para habilitar — construir la base de datos desde el anexo de
  esquema, reconstruir el modelo financiero desde el capítulo financiero,
  escribir el backlog desde el capítulo de producto — y su artefacto se
  califica contra un rubric escrito ANTES. Úsala cuando un documento "completo"
  y "bien escrito" igual no le sirve a quien debe actuar con él, cuando el
  usuario diga "no se entiende nada", "con esto no se puede construir",
  "pruébalo con la tarea real", "pásaselo a haiku y que lo haga", o después de
  correr doc-completitud y doc-narrativa (esta es la
  prueba más exigente de las tres: explicar ≠ poder hacer). Orquesta lectores
  débiles con el tool Workflow; el rubric, la verificación de fantasmas y el
  parchado son SIEMPRE del orquestador.
---

# Doc Prueba de Uso — el documento se prueba HACIENDO, no explicando

## La lección que originó esta skill (el error del Anexo D, Aero360, 07-2026)

Un informe estratégico pasó **dos** controles de calidad con lectores débiles:
un loop de completitud ("¿puedes explicar cada sección sin vacíos?" → sí) y una
reestructura de storytelling ("¿se lee como un relato?" → sí). Aun así, cuando
el usuario abrió el anexo del esquema de datos, su veredicto fue *"no se
entiende nada"* — y tenía razón: el anexo nombraba 28 tablas sin un solo
atributo, sin llaves, sin política de IDs. Un diseñador no podía construir la
base de datos desde él.

**El error no fue de escritura: fue de criterio de validación.** Los lectores
verificaban que el contenido *se pudiera explicar*; nadie verificaba que
*sirviera para ejecutar su propósito*. Un lector puede resumir perfectamente un
anexo que es inservible como referencia de diseño — porque resumir solo exige
lo que está, y ejecutar exige lo que falta.

La prueba correcta apareció con el arreglo (propuesta por el usuario): *"pásale
el anexo a Haiku y pídele que te arme la base de datos; analiza su respuesta e
itera el anexo hasta que el resultado sea el esperado"*. Tres rondas después el
anexo era una referencia real: esquema relacional con llaves subrayadas,
diagramas E-R con cardinalidades y un diccionario de ~30 entidades.

**Regla madre: a cada sección de un documento se le exige lo mismo que a un
plano — que alguien que no estuvo en la conversación pueda construir con él.**

## Cuándo usarla

- El usuario dice que un documento "no se entiende", "está muy condensado" o
  "con esto no se puede trabajar", aunque haya pasado revisiones previas.
- Antes de entregar un documento a quien debe ACTUAR con él (un desarrollador,
  un CFO, un abogado, un socio que decide).
- Como tercera etapa del pipeline de calidad documental:
  `doc-completitud` (que no falte nada) → `doc-narrativa`
  (que se lea bien) → **`doc-prueba-de-uso` (que sirva para hacer)**.

## El método, paso a paso

1. **Inventario de propósitos.** Para cada capítulo/sección del documento,
   completa la frase: *"después de leer SOLO esto, el lector debe poder
   \_\_\_"*. Si no puedes completarla, esa sección no tiene propósito operativo
   (o es puramente narrativa — está bien, se excluye de la prueba). El
   propósito define el **rol** del lector de prueba (DBA, CFO, PM, abogado…) y
   su **tarea** ("arma el DDL", "reconstruye el modelo en una tabla", "escribe
   el backlog").

2. **Rubric ANTES de la prueba.** El orquestador escribe, por sección, los
   criterios verificables del artefacto esperado (para un esquema: PKs, FKs,
   constraints exactos; para finanzas: los supuestos y cifras que deben poder
   reconstruirse). Sin rubric previo, la calificación se contamina con lo que
   el lector haya producido. Separa CRÍTICOS (si falla uno, iterar) de
   IMPORTANTES.

3. **Extracción aislada.** Cada sección se copia a un archivo propio en el
   scratchpad. El lector recibe SOLO ese archivo — si lee el documento entero,
   la prueba no mide la autosuficiencia de la sección.

4. **Lector débil con tarea + prueba de lectura + vacíos.** El prompt del
   lector (modelo barato, p. ej. haiku) tiene cuatro partes obligatorias:
   - *Rol y tarea*: "Eres el [rol] recién llegado. Tu ÚNICA fuente es este
     archivo. [Haz la tarea]."
   - *Prueba de lectura*: 2-3 preguntas cuya respuesta exige haber leído de
     verdad (citar una línea textual, nombrar elementos específicos). Detecta
     lectores que inventan sin leer — pasó en producción.
   - *El artefacto completo* (no resumido).
   - *AMBIGÜEDADES/VACÍOS*: todo lo que tuvo que adivinar, indicando dónde
     buscó. Con la **regla de referencias canónicas**: si el dato está
     explícitamente referenciado a otra sección ("ver §5.3"), NO es un vacío —
     es la arquitectura del documento (cada número vive en un solo lugar);
     se anota aparte como referencia externa.

5. **Calificación + disciplina de fantasmas.** El orquestador compara el
   artefacto contra el rubric y **verifica cada vacío reclamado contra el
   documento antes de parchar** (grep/lectura directa). Los lectores débiles
   producen fantasmas en cantidad — en el caso origen, ~10 de 12 hallazgos de
   una ronda eran falsos (el lector no vio una entidad que SÍ estaba en el
   diagrama, ignoró convenciones declaradas en la leyenda). Señales de lector
   degradado: responde en otro idioma, inventa valores que el documento niega,
   demasiadas herramientas usadas. Un hallazgo sin verificación no se parcha.

6. **Parche mínimo, del orquestador.** Se corrige SOLO lo real, con la
   aclaración más pequeña que desbloquea la tarea (una frase, una fila, una
   convención explicitada). Nunca se le pide al lector que "arregle" el
   documento: no tiene el contexto.

7. **Iterar hasta convergencia.** Ronda nueva con lector fresco (nunca el
   mismo, ya está contaminado). Convergencia = artefacto pasa los CRÍTICOS del
   rubric **y** el lector declara explícitamente que no encontró ambigüedades
   reales. Típico: 2-3 rondas. En la última ronda conviene variar la prueba de
   lectura hacia lo recién agregado, para confirmar que las correcciones se
   captan en frío.

## Reglas de oro

- **Probar haciendo, no explicando.** "¿Se entiende?" mide prosa; "hazlo" mide
  utilidad. Solo la segunda encuentra los atributos que faltan.
- **El rubric se escribe antes de ver respuestas.**
- **Fantasma no verificado = no se toca el documento.**
- **Referencia canónica ≠ vacío.** No degradar la arquitectura del documento
  duplicando números para complacer al lector aislado.
- **Cada sección, su rol y su tarea.** Un solo "¿puedes explicarlo?" genérico
  es exactamente el error que esta skill corrige.
- **El artefacto del lector es descartable.** No es código para producción; es
  el instrumento de medición del documento.

## Script para el tool Workflow (fan-out por secciones)

```js
export const meta = {
  name: 'doc-prueba-de-uso',
  description: 'Prueba de uso por seccion: lectores frios ejecutan la tarea de cada seccion',
  phases: [{ title: 'Prueba de uso' }],
}
// args: [{ id, file, rol, tarea, pruebaLectura }, ...]  — preparado por el orquestador
const SCHEMA = {
  type: 'object',
  properties: {
    prueba_lectura: { type: 'string' },
    artefacto: { type: 'string' },
    vacios_bloqueantes: { type: 'array', items: { type: 'object', properties: {
      descripcion: { type: 'string' }, donde_busco: { type: 'string' } },
      required: ['descripcion', 'donde_busco'] } },
    vacios_menores: { type: 'array', items: { type: 'string' } },
    referencias_externas: { type: 'array', items: { type: 'string' } },
  },
  required: ['prueba_lectura', 'artefacto', 'vacios_bloqueantes', 'vacios_menores', 'referencias_externas'],
}
const res = await parallel(args.map(s => () =>
  agent(
    `Eres ${s.rol}, recién llegado al proyecto. Tu ÚNICA fuente es este archivo ` +
    `(no tienes acceso a nada más; léelo COMPLETO, por partes si es largo): ${s.file}\n\n` +
    `PRUEBA DE LECTURA (responde primero): ${s.pruebaLectura}\n\n` +
    `TU TAREA: ${s.tarea}\n\n` +
    `Al final, lista VACÍOS BLOQUEANTES (lo que tuviste que adivinar para poder ejecutar ` +
    `la tarea, indicando dónde lo buscaste) y VACÍOS MENORES. REGLA: si el documento ` +
    `remite explícitamente un dato a otra sección o capítulo ("ver §X"), NO es un vacío — ` +
    `regístralo en referencias_externas. Si no hay vacíos reales, dilo con listas vacías.`,
    { label: `uso:${s.id}`, model: 'haiku', schema: SCHEMA }
  ).then(r => ({ id: s.id, ...r }))
))
return res.filter(Boolean)
// La calificación contra el rubric, la verificación de fantasmas y los parches
// son del ORQUESTADOR, en el turno siguiente — nunca de un agente.
```

## Variantes

- **Sección única** (el caso origen): sin Workflow — un solo `Agent` con model
  haiku por ronda, iterando 2-3 veces. Más simple y suficiente.
- **Prueba de consistencia**: cuando una sección presenta la misma información
  en varias representaciones (texto + diagrama + tabla), pide además "reporta
  toda contradicción entre las representaciones". Ojo: produce más fantasmas
  (leer diagramas SVG degrada a los lectores débiles) — la disciplina del paso
  5 se vuelve crítica.
- **Rubric implícito**: para secciones narrativas (una tesis, un cierre), la
  "tarea" es reproducir la decisión y sus porqués ante un tercero exigente; el
  rubric es la lista de decisiones/argumentos que deben sobrevivir.
