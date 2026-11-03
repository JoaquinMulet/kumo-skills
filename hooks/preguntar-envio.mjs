#!/usr/bin/env node
/**
 * PREGUNTAR ANTES DE ENVIAR. Hook PreToolUse de las herramientas de
 * conectores (mcp__*) que mandan un mensaje o publican algo a nombre del
 * dueno. Pide su confirmacion en pantalla, aunque la sesion este en modo
 * automatico.
 *
 * Por que existe. Ningun mensaje sale a su nombre sin que el vise el
 * texto exacto (regla de su CLAUDE.md global). Una vez salieron 20 correos
 * reales sin que viera la pieza, porque la orden de enviar se tomo como
 * aprobacion del texto (caso contado en desarrollo-riguroso hasta el 3 nov
 * 2026). La regla escrita no lo impidio.
 *
 * Que cuenta como envio. Un nombre de herramienta con send, schedule,
 * post, publish, reply, forward, invite o los canvas de Slack que se crean
 * o editan. Un borrador (draft) no sale y no pregunta.
 */
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const ENVIA = /(?:^|_)(send|schedule|post|publish|reply|forward|invite|create_canvas|update_canvas)(?:_|$)/i
const BORRADOR = /draft/i

export function esEnvio(nombre) {
  if (!String(nombre).startsWith('mcp__')) return false
  const herramienta = String(nombre).split('__').pop()
  return ENVIA.test(herramienta) && !BORRADOR.test(herramienta)
}

function main() {
  let evento
  try { evento = JSON.parse(readFileSync(0, 'utf8')) } catch { return }
  if (!esEnvio(evento.tool_name)) return
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'ask',
      permissionDecisionReason: '[preguntar-envio] Esto envía o publica a nombre de Joaquín. '
        + 'Confirma solo si ya viste el texto exacto en el chat.',
    },
  }))
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main()
