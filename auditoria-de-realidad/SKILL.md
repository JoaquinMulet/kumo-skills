---
name: auditoria-de-realidad
description: Auditoría adversarial del estado REAL de un proyecto — uno o más agentes FRESCOS y escépticos, en frío, hurgan los artefactos reales (repo, git, deploy, prod, secretos, docs, código) con una pregunta ABIERTA ("¿qué está roto, peligroso o inconsistente que nadie está viendo?"), NO un test pass/fail. Cubre a propósito las superficies "aburridas" (backups, secretos en el filesystem, qué se despliega de verdad) que el aparato sofisticado ignora. Usa esta skill antes de dar por bueno un sistema o una entrega, al heredar un proyecto ajeno, cuando sospechas que hay algo grave que nadie está viendo, o cuando el usuario dice "¿qué se nos está escapando?", "audita esto de verdad", "algo huele mal", "qué no estamos viendo", "revisa el estado real", "¿por qué no invocas un agente fresco?", o equivalentes. (Distinta de retrospectiva-de-sesion, que aprende de las correcciones de la sesión: esta CAZA lo que está roto o latente en el estado real.) Es el complemento ABIERTO de VERIFY-REAL: VERIFY-REAL confronta lo que ya sabes que hay que chequear; esta caza lo que no sabías que buscar.
---

# Auditoría de realidad — el escéptico fresco sobre el mundo, no el modelo

El error más peligroso es el que tu propio aparato de validación no está mirando. Todo test, review o skill que **tú** diseñaste comparte **tus** puntos ciegos: valida el modelo que tienes en la cabeza, no el mundo. La única forma de romper ese lazo cerrado es traer un ojo SIN tu contexto, apuntarlo a los artefactos REALES, y hacerle una pregunta abierta.

*(caso origen: meses de aparato —TDD, observabilidad, skills, retrospectivas, un `VERIFY-REAL` que "pasó"— no vieron que el trunk desplegado a prod vivía solo en un disco sin backup, ni que los secretos de prod se sincronizaban a la nube por el filesystem, ni un bug de moneda latente en el motor contable. Un agente fresco lo encontró en 6 minutos con un `git ls-remote` y una lectura escéptica del código.)*

## Qué la hace distinta de un test

- **Contexto FRESCO.** El auditor no vivió la sesión; no comparte las racionalizaciones ni los puntos ciegos del que construyó. Contexto fresco de verdad — no "yo mismo con otro sombrero".
- **Artefactos REALES.** El repo, git, el prod, el `.env`, el script de deploy que **de verdad existen** — no fixtures ni proyectos inventados. Validar sobre datos sintéticos es exactamente el teatro que esta skill existe para romper (ver "la trampa del validador autorreferencial" en `desarrollo-riguroso`).
- **Pregunta ABIERTA, no pass/fail.** *"¿Qué está mal, peligroso o inconsistente acá?"*, no *"¿pasa X?"*. El test cerrado solo encuentra lo que anticipaste; el open-ended encuentra la esquina que no miraste.

## El método

1. **Enumera las superficies reales de alto riesgo — y NO olvides las aburridas.** Las peores suelen ser las mundanas, no las elegantes:
   - **Proceso / infra:** ¿el trunk está en un remoto o vive solo en un disco? ¿qué está DESPLEGADO de verdad? ¿el deploy es trazable a un ref de git o empaqueta el working tree? ¿dónde viven los secretos — los filtra el filesystem (OneDrive/Dropbox)? ¿hay backup?
   - **Código:** los invariantes que se pueden violar en **silencio** (mezcla de unidades/monedas, saldos negativos, redondeo, concurrencia). El bug que pasa los tests porque la forma de los datos de HOY no lo gatilla.
   - **Docs / skills:** ¿lo que declaran coincide con lo que el sistema hace? ¿hay algún "validado" que en realidad es no-validado? ¿alguna regla obligatoria que ningún gate hace cumplir?
2. **Un agente fresco por superficie**, con la orden: *"Eres un senior escéptico que heredó esto en frío. NO valides, CAZA. Lee los archivos reales (Read/Grep/Bash; git es read-only). Cada hallazgo con EVIDENCIA concreta (file:line, salida de git). Di por qué el equipo estuvo ciego a esto. Y lo único que te quitaría el sueño."* (script abajo).
3. **Ghost discipline (SIEMPRE del orquestador).** Los escépticos también inventan. VERIFICA cada hallazgo grave contra el artefacto real antes de creerlo o actuar — sobre todo los de dinero y seguridad. Un hallazgo sin verificar no se toca (igual que en `doc-prueba-de-uso`).
4. **Rankea por peligro REAL, no por sofisticación.** El aparato sofisticado mira la corrección fina mientras la casa se incendia. **Criterio de orden:** pérdida de datos irreversible (trunk sin backup) > fuga de secretos > corrupción silenciosa de dinero/estado > todo lo demás. Un bug elegante rankea SIEMPRE por debajo de un trunk sin remoto.
5. **Encontrarlo por suerte NO cuenta.** Si esta auditoría no es una **rutina** (un gate al cerrar sesión / antes de dar por bueno un sistema), volverás a depender de que un humano señale el fuego — y eso no es que el sistema funcione.

## Por qué VERIFY-REAL no basta (y esta lo complementa)

`VERIFY-REAL` confronta el código contra los datos REALES de **HOY** — y por eso **no puede** cazar un bug LATENTE que los datos de hoy no gatillan (un FIFO que mezcla EUR y USD no explota mientras todos los cobros sean USD; el `VERIFY-REAL` del cierre "pasó" justo por eso). Esta auditoría lee el código buscando la **violación de invariante**, no la falla observable. Son complementarias: VERIFY-REAL caza lo que ya está mal; la auditoría fresca caza lo que está latente y lo que es de otra dimensión (infra, secretos, proceso).

## Script para el tool Workflow (un escéptico fresco por superficie)

```js
export const meta = {
  name: 'auditoria-de-realidad',
  description: 'Agentes frescos escepticos hurgan el estado REAL con pregunta abierta',
  phases: [{ title: 'Auditar la realidad' }],
}
// args: [{ id, ruta, superficie }]  — preparado por el orquestador
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
const res = await parallel(args.map(s => () =>
  agent(`${BASE}\n\nSUPERFICIE (${s.superficie}), en: ${s.ruta}\n` +
    `Pregunta abierta: que aca es peligroso o mentira que nadie esta mirando? No te limites a lo conocido.`,
    { label: `auditar:${s.id}`, phase: 'Auditar la realidad', schema: SCHEMA })
    .then(r => ({ id: s.id, ...r }))
))
return res.filter(Boolean)
// La verificacion de fantasmas, el ranking por peligro real y las acciones son del ORQUESTADOR.
```

## Variante sin Workflow

Si no hay tool `Workflow` disponible, divide el trabajo en las **tres superficies del paso 1** (proceso/infra, código, docs/skills) y corre un `Agent` fresco por cada una en secuencia con la misma orden — o, para una revisión puntual, un solo `Agent` sobre la superficie más crítica. **Modelo fuerte, no haiku** — cazar bugs necesita capacidad. La verificación de fantasmas y el ranking siguen siendo tuyos, corras en paralelo o en serie.

## Por qué existe

Es la herramienta para el universo de errores **DESCONOCIDOS**. Los principios que destilas defienden la esquina pasada; los tests cerrados encuentran lo que anticipaste; VERIFY-REAL caza lo que los datos de hoy gatillan. Solo un ojo fresco con pregunta abierta sobre lo real encuentra lo que **no sabías buscar**. No elimina el universo de errores escondidos —es inabarcable e incerrable— pero **achica el tiempo-hasta-detección**, que es el objetivo honesto. Córrela como rutina, no cuando ya es tarde.
