#!/usr/bin/env node
/**
 * RECORDATORIO DE SESION. Inyecta el contrato de lectura una vez por
 * sesion, antes de que el agente toque nada.
 *
 * Por que existe. la skill desarrollo-riguroso se carga cuando el modelo
 * decide que aplica, y ahi ya perdimos. Este hook no depende de esa
 * decision, corre al abrir la sesion.
 *
 * Y por que no bloquea. SessionStart NO puede bloquear, verificado en la
 * documentacion. Solo agrega contexto. El que bloquea es el hermano,
 * exigir-higiene.mjs, que corre en PreToolUse sobre el commit.
 *
 * Los 2 se necesitan. este dice QUE hay que hacer antes de empezar, y
 * aquel impide terminar sin haberlo hecho.
 */
process.stdout.write(
  '[estandar-kumo] Antes de escribir codigo en cualquier repo, la skill '
  + '`desarrollo-riguroso` es OBLIGATORIA y se lee COMPLETA.\n'
  + '  1. Cargala y leela hasta ver su marcador de cierre. Si no lo viste, la lectura '
  + 'quedo truncada y hay que seguir leyendo con Read desde donde quedaste. Actuar con '
  + 'media skill es peor que no haberla abierto, porque da la sensacion de haberla '
  + 'consultado.\n'
  + '  2. Su seccion «Higiene continua del repo» no es opcional. Un repo sin su aparato '
  + 'de higiene instalado NO puede commitear, y un hook lo va a impedir.\n'
  + '  3. Si el repo no lo tiene, instalalo con los 7 pasos del anexo ANTES de trabajar, '
  + 'no despues.\n',
)
