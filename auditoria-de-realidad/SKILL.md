---
name: auditoria-de-realidad
description: Auditoría adversarial del estado REAL de un proyecto — un agente FRESCO y escéptico, en frío, hurga los artefactos reales (repo, git, deploy, prod, secretos, código) con una pregunta ABIERTA sobre qué está roto, peligroso o inconsistente que nadie ve, NO un test pass/fail. Cubre a propósito las superficies aburridas (backups, secretos en el filesystem, qué se despliega de verdad) que el aparato sofisticado ignora. Usa esta skill antes de dar por bueno un sistema o una entrega, al heredar un proyecto ajeno, cuando sospechas que hay algo grave que nadie ve, o cuando el usuario dice «audita esto de verdad», «qué se nos está escapando», «algo huele mal», «revisa el estado real» o «por qué no invocas un agente fresco». Es el complemento ABIERTO de VERIFY-REAL — VERIFY-REAL confronta lo que ya sabes que hay que chequear; esta caza lo latente y lo de otra dimensión (infra, secretos, proceso) que no sabías buscar.
---

# Auditoría de realidad. El escéptico fresco sobre el mundo, no el modelo

El error más peligroso es el que tu propio aparato de validación no está mirando. Todo test, review o skill que **tú** diseñaste comparte **tus** puntos ciegos: valida el modelo que tienes en la cabeza, no el mundo. La única forma de romper ese lazo cerrado es traer un ojo SIN tu contexto, apuntarlo a los artefactos REALES, y hacerle una pregunta abierta.

*(caso origen: meses de aparato, TDD, observabilidad, skills, retrospectivas, un `VERIFY-REAL` que "pasó", no vieron que el trunk desplegado a prod vivía solo en un disco sin backup, ni que los secretos de prod se sincronizaban a la nube por el filesystem, ni un bug de moneda latente en el motor contable. Un agente fresco lo encontró en 6 minutos con un `git ls-remote` y una lectura escéptica del código.)*

## Qué la hace distinta de un test

- **Contexto FRESCO.** El auditor no vivió la sesión. No comparte las racionalizaciones ni los puntos ciegos del que construyó. Contexto fresco de verdad, no "yo mismo con otro sombrero".
- **Artefactos REALES.** El repo, git, el prod, el `.env`, el script de deploy que **de verdad existen.** No fixtures ni proyectos inventados. Validar sobre datos sintéticos es exactamente el teatro que esta skill existe para romper (ver "la trampa del validador autorreferencial" en `desarrollo-riguroso`).
- **Pregunta ABIERTA, no pass/fail.** *"¿Qué está mal, peligroso o inconsistente acá?"*, no *"¿pasa X?"*. El test cerrado solo encuentra lo que anticipaste. El open-ended encuentra la esquina que no miraste.

## El método

1. **Un nodo FRESCO propone las superficies. Tú conservas el veto, no la propuesta.** Esta es la corrección más importante del método. Quien orquesta es exactamente quien tiene el punto ciego que la skill existe para romper, así que pedirle que enumere qué mirar es pedirle al ciego que apunte la linterna. El primer agente del grafo no audita nada, recorre el proyecto en frío y propone **qué superficies merecen un escéptico**, con la lista de abajo como piso, no como techo. Después tú tachas lo que no aplica y agregas lo que falte.

   **Su schema lleva tope explícito** (`máximo 5 superficies, ordenadas por peligro real`). Un proponedor sin tope no cuesta un agente, cuesta lo que decida abanicar, es un multiplicador del ancho del fan-out, y va a proponer de más justamente porque se puso ahí para mirar lo que tú no mirabas. Sin tope, el presupuesto de la corrida lo fija el agente menos informado del grafo.

   El piso obligatorio, las superficies **aburridas**, que son las peores y las que todo aparato sofisticado ignora:
   - **Proceso / infra:** ¿el trunk está en un remoto o vive solo en un disco? ¿qué está DESPLEGADO de verdad? ¿el deploy es trazable a un ref de git o empaqueta el working tree? ¿dónde viven los secretos, los filtra el filesystem (OneDrive/Dropbox)? ¿hay backup?
   - **Código:** los invariantes que se pueden violar en **silencio** (mezcla de unidades/monedas, saldos negativos, redondeo, concurrencia). El bug que pasa los tests porque la forma de los datos de HOY no lo gatilla.
   - **Docs / skills:** ¿lo que declaran coincide con lo que el sistema hace? ¿hay algún "validado" que en realidad es no-validado? ¿alguna regla obligatoria que ningún gate hace cumplir?
2. **Un agente fresco por superficie** (las que sobrevivieron tu veto), con la orden: *"Eres un senior escéptico que heredó esto en frío. NO valides, CAZA. Lee los archivos reales (Read/Grep/Bash. Git es read-only). Cada hallazgo con EVIDENCIA concreta (file:line, salida de git). Di por qué el equipo estuvo ciego a esto. Y lo único que te quitaría el sueño."* (script abajo).
3. **Ghost discipline (SIEMPRE del orquestador).** Los escépticos también inventan. VERIFICA cada hallazgo grave contra el artefacto real antes de creerlo o actuar, sobre todo los de dinero y seguridad. Un hallazgo sin verificar no se toca (igual que en `doc-prueba-de-uso`). Dos formas del fantasma que no son "inventó todo", y por eso se cuelan:

   - **Mitad fantasma, mitad real, y en otro lugar del que nombra.** El hallazgo acierta el TIPO de riesgo y falla la ubicación. No lo descartes al comprobar que la ruta es falsa: pregúntate si el mismo riesgo existe en otra parte, porque el escéptico olió algo real sin poder ubicarlo. *(Caso real: un hallazgo afirmó que las transcripciones de sesión vivían en una carpeta sincronizada a la nube, falso, esa ruta no sincroniza. Pero el REPO sí estaba dentro de la carpeta sincronizada, y eso no lo dijo. Descartarlo por la ruta equivocada habría enterrado el punto correcto.)*
   - **El mecanismo deliberado disfrazado de vulnerabilidad.** Un escéptico sin contexto rankea como crítico lo que el equipo construyó a propósito (los hooks corren código, el deploy tiene permisos, el script lee el filesystem). No es un hallazgo. Es la descripción del diseño. La prueba para separarlos es: ¿existe un ESCENARIO concreto en que esto daña, o solo la posibilidad genérica de que algo ejecutable ejecute? Sin escenario, es ruido con severidad inflada.
4. **Rankea por peligro REAL, no por sofisticación.** El aparato sofisticado mira la corrección fina mientras la casa se incendia. **Criterio de orden.** Pérdida de datos irreversible (trunk sin backup) > fuga de secretos > corrupción silenciosa de dinero/estado > todo lo demás. Un bug elegante rankea SIEMPRE por debajo de un trunk sin remoto.
5. **Encontrarlo y NO cerrarlo tampoco cuenta.** Un riesgo #1 ya identificado y accionable no es un ítem de backlog: se **cierra antes** de seguir optimizando lo demás, o se declara EXPLÍCITAMENTE por qué se posterga y hasta cuándo. El modo de falla es sutil y se *siente* productivo: sigues entregando trabajo impecable, tests, fixes, deploys, mientras el hallazgo dominante envejece en una lista. *(ej. real: los secretos de prod y la access key estática de AWS vivían en una carpeta sincronizada a la nube. Se detectó al INICIO de la sesión, se anotó como "acción del usuario", y siguió abierto durante 13 commits de trabajo fino sobre bugs de MUCHO menor impacto. El aparato no falló en detectar: falló en priorizar la ejecución.)* Regla: si el #1 no lo puedes cerrar tú, **bloquea y pide**. No lo dejes flotando entre tareas menores.
6. **Encontrarlo por suerte NO cuenta.** Si esta auditoría no es una **rutina** (un gate al cerrar sesión / antes de dar por bueno un sistema), volverás a depender de que un humano señale el fuego, y eso no es que el sistema funcione.

## Por qué VERIFY-REAL no basta (y esta lo complementa)

`VERIFY-REAL` confronta el código contra los datos REALES de **HOY**, y por eso **no puede** cazar un bug LATENTE que los datos de hoy no gatillan (un FIFO que mezcla EUR y USD no explota mientras todos los cobros sean USD. El `VERIFY-REAL` del cierre "pasó" justo por eso). Esta auditoría lee el código buscando la **violación de invariante**, no la falla observable. Son complementarias. VERIFY-REAL caza lo que ya está mal. La auditoría fresca caza lo que está latente y lo que es de otra dimensión (infra, secretos, proceso).

## Script para el tool Workflow (dos fases: proponer, y un escéptico por superficie)

Son **dos invocaciones**, no una: la primera devuelve las superficies propuestas, tú las
vetas y recortas a mano, y recién entonces incrustas las sobrevivientes en la segunda. El
corte humano en el medio es el punto, si el proponedor alimentara el fan-out directo,
nadie habría ejercido el veto.

**Fase A, el proponedor fresco (1 agente).** El tope vive en su schema y en su prompt.

```js
export const meta = {
  name: 'auditoria-superficies',
  description: 'Un agente fresco propone que superficies merecen un esceptico, con tope',
  phases: [{ title: 'Proponer superficies' }],
}
const RAIZ = '<RUTA-ABSOLUTA-DEL-PROYECTO>'
if (RAIZ.includes('<RUTA')) throw new Error('Incrusta la ruta real antes de correrlo')
const MAX_SUPERFICIES = 5   // tope duro: el proponedor multiplica el ancho del fan-out

const PROP_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    resumen_leido: { type: 'string', description: 'que es este proyecto, en una frase — prueba de que lo recorriste' },
    superficies: {
      type: 'array', maxItems: MAX_SUPERFICIES,
      items: { type: 'object', additionalProperties: false, properties: {
        id: { type: 'string' }, ruta: { type: 'string' }, superficie: { type: 'string' },
        porque_peligrosa: { type: 'string' },
        peligro: { type: 'string', enum: ['critico','alto','medio'] } },
        required: ['id','ruta','superficie','porque_peligrosa','peligro'] },
    },
    lo_que_no_alcanzo_a_mirar: { type: 'string', description: 'que quedo fuera por el tope — para que el orquestador decida si sube el tope' },
  }, required: ['resumen_leido','superficies','lo_que_no_alcanzo_a_mirar'],
}

const res = await agent(
  `Eres un ingeniero senior que acaba de heredar este proyecto EN FRIO, en: ${RAIZ}\n` +
  `NO audites todavia: RECONOCE EL TERRENO. Recorre el repo (Read/Grep/Bash; git read-only) y ` +
  `propon COMO MAXIMO ${MAX_SUPERFICIES} superficies que merecen un escéptico dedicado, ordenadas ` +
  `por peligro REAL (perdida de datos irreversible > fuga de secretos > corrupcion silenciosa de ` +
  `dinero/estado > el resto). Piso obligatorio, no techo: incluye las superficies ABURRIDAS ` +
  `(backup del trunk, donde viven los secretos y si el filesystem los filtra, que se despliega de ` +
  `verdad) — son las peores y las que todo aparato sofisticado ignora. Si el tope te dejo cosas ` +
  `fuera, dilas en 'lo_que_no_alcanzo_a_mirar'.`,
  { label: 'proponer-superficies', phase: 'Proponer superficies', schema: PROP_SCHEMA }
)
return res
```

**Fase B, un escéptico por superficie sobreviviente.**

```js
export const meta = {
  name: 'auditoria-de-realidad',
  description: 'Agentes frescos escepticos hurgan el estado REAL con pregunta abierta',
  phases: [{ title: 'Auditar la realidad' }],
}
// SUPERFICIES INCRUSTADAS con guard: las que salieron de la fase A y SOBREVIVIERON tu veto.
// (Contrato del caller del esqueleto compartido — lee
// desarrollo-riguroso/reference/esqueleto-de-verificacion.md antes de tocar esto.)
const SUPERFICIES = [ /* { id, ruta, superficie }, ... — literales */ ]
if (!SUPERFICIES.length) throw new Error('Incrusta las superficies en el script antes de correrlo')
const SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    hallazgos: { type: 'array', items: { type: 'object', additionalProperties: false, properties: {
      titulo: { type: 'string' }, severidad: { type: 'string', enum: ['critico','alto','medio','bajo'] },
      evidencia: { type: 'string' }, porque_invisible: { type: 'string' } },
      required: ['titulo','severidad','evidencia','porque_invisible'] } },
    lo_mas_peligroso: { type: 'string' },
  }, required: ['hallazgos','lo_mas_peligroso'],
}
const BASE = `Eres un ingeniero senior ESCEPTICO que acaba de heredar esto en frio — no confias en nada. ` +
  `NO valides ("funciona?"); CAZA ("que esta roto, peligroso, inconsistente, latente?"). Lee los archivos ` +
  `REALES (Read/Grep/Bash; git es read-only). Cada hallazgo con EVIDENCIA concreta (file:line, salida de git) ` +
  `— nada de sospechas sin prueba. Por cada uno di "porque_invisible": por que el equipo estuvo ciego. Al final, ` +
  `"lo_mas_peligroso": el unico que te quitaria el sueno. Incluye las superficies ABURRIDAS (backup del trunk, ` +
  `secretos en el filesystem, que se despliega de verdad), no solo la logica elegante.`
const res = await parallel(SUPERFICIES.map(s => () =>
  agent(`${BASE}\n\nSUPERFICIE (${s.superficie}), en: ${s.ruta}\n` +
    `Pregunta abierta: que aca es peligroso o mentira que nadie esta mirando? No te limites a lo conocido.`,
    { label: `auditar:${s.id}`, phase: 'Auditar la realidad', schema: SCHEMA })
    .then(r => ({ id: s.id, ...r }))
))
return res.filter(Boolean)
// La verificacion de fantasmas, el ranking por peligro real y las acciones son del ORQUESTADOR.
```

## Variante sin Workflow

Si no hay tool `Workflow` disponible, el orden no cambia: primero **un `Agent` fresco que solo propone** las superficies con el mismo tope, tú lo vetas, y después un `Agent` escéptico por superficie sobreviviente, en secuencia. Si vas a saltarte el proponedor por costo, usa el **piso de las tres superficies aburridas** (proceso/infra, código, docs/skills) y ten presente qué estás perdiendo: el piso lo escribiste tú, así que hereda tus puntos ciegos, que es exactamente lo que el proponedor existe para romper. Para una revisión puntual, un solo `Agent` sobre la superficie más crítica, o, para una revisión puntual, un solo `Agent` sobre la superficie más crítica. **Modelo fuerte, no haiku**, cazar bugs necesita capacidad. La verificación de fantasmas y el ranking siguen siendo tuyos, corras en paralelo o en serie.

## Por qué existe

Es la herramienta para el universo de errores **DESCONOCIDOS**. Los principios que destilas defienden la esquina pasada. Los tests cerrados encuentran lo que anticipaste. VERIFY-REAL caza lo que los datos de hoy gatillan. Solo un ojo fresco con pregunta abierta sobre lo real encuentra lo que **no sabías buscar**. No elimina el universo de errores escondidos, es inabarcable e incerrable, pero **achica el tiempo-hasta-detección**, que es el objetivo honesto. Córrela como rutina, no cuando ya es tarde.
