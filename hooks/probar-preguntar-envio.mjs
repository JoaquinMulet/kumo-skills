#!/usr/bin/env node
/**
 * Prueba que el hook pregunte ante cada herramienta que envía o publica, y
 * que no estorbe con las que solo leen o dejan un borrador.
 *
 * Uso.  node hooks/probar-preguntar-envio.mjs
 * Sale con 0 si todos los casos dan lo esperado, y con 1 si alguno falla.
 */
import { execFileSync } from 'node:child_process'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const HOOK = join(dirname(fileURLToPath(import.meta.url)), 'preguntar-envio.mjs')
const S = 'mcp__e2bd06ed-27f1-4d66-8c3f-418ae12666d1__'

function correr(tool_name) {
  const r = execFileSync('node', [HOOK], { input: JSON.stringify({ tool_name, tool_input: {} }), encoding: 'utf8' })
  if (r.trim() === '') return 'pasa'
  try { return JSON.parse(r).hookSpecificOutput.permissionDecision } catch { return 'ilegible' }
}

const casos = [
  [S + 'slack_send_message', 'ask'],
  [S + 'slack_schedule_message', 'ask'],
  [S + 'slack_create_canvas', 'ask'],
  [S + 'slack_update_canvas', 'ask'],
  ['mcp__gmail__send_email', 'ask'],
  ['mcp__gmail__reply_to_thread', 'ask'],
  [S + 'slack_send_message_draft', 'pasa'],
  [S + 'slack_read_channel', 'pasa'],
  [S + 'slack_search_public', 'pasa'],
  ['mcp__cmf-chile__cmf_empresa_info', 'pasa'],
  ['Bash', 'pasa'],
]
let malos = 0
for (const [nombre, esperado] of casos) {
  const dio = correr(nombre)
  if (dio !== esperado) malos++
  process.stdout.write(`  ${dio === esperado ? 'ok  ' : 'MAL '} ${nombre.split('__').pop().padEnd(28)} esperaba ${esperado}, dio ${dio}\n`)
}
process.stdout.write(`\n${casos.length - malos} de ${casos.length} casos correctos.\n`)
process.stdout.write(malos ? 'ROJO.\n' : 'VERDE.\n')
process.exit(malos ? 1 : 0)
