#!/usr/bin/env node
/**
 * Prueba el revisor de encargos a subagentes en las 2 direcciones.
 *
 * Uso.  node hooks/probar-revisar-encargo.mjs
 * Sale con 0 si todos los casos dan lo esperado, y con 1 si alguno falla.
 */
import { execFileSync } from 'node:child_process'
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const HOOK = join(dirname(fileURLToPath(import.meta.url)), 'revisar-encargo.mjs')
const tmp = mkdtempSync(join(tmpdir(), 'encargo-'))
const conRegla = join(tmp, 'ENCARGO.md').replace(/\\/g, '/')
const sinRegla = join(tmp, 'OTRO.md').replace(/\\/g, '/')
writeFileSync(conRegla, 'Corre todo en primer plano con timeout.\n')
writeFileSync(sinRegla, 'Revisa el modulo de pagos.\n')

function correr(input, herramienta = 'Agent') {
  const r = execFileSync('node', [HOOK], { input: JSON.stringify({ tool_name: herramienta, tool_input: input }), encoding: 'utf8' })
  if (r.trim() === '') return 'pasa'
  try { return JSON.parse(r).hookSpecificOutput.permissionDecision === 'deny' ? 'niega' : '?' } catch { return 'ilegible' }
}

const PP = 'Corre tus comandos en primer plano. '
const casos = [
  ['sin primer plano (29 oct 2026)', { prompt: 'Corre las pruebas y arregla lo rojo.' }, 'niega'],
  ['con primer plano', { prompt: PP + 'Corre las pruebas.' }, 'pasa'],
  ['primer plano en el archivo nombrado', { prompt: `Lee el encargo completo en ${conRegla} y cúmplelo.` }, 'pasa'],
  ['archivo nombrado sin la regla', { prompt: `Lee el encargo completo en ${sinRegla} y cúmplelo.` }, 'niega'],
  ['lee la web sin robots.txt (21 oct 2026)', { prompt: PP + 'Busca en la web el precio y usa WebFetch.' }, 'niega'],
  ['lee la web con robots.txt', { prompt: PP + 'Usa WebFetch. Respeta robots.txt y no envíes cabeceras falsas.' }, 'pasa'],
  ['árboles de trabajo sin la regla del stash (26 sep 2026)', { prompt: PP + 'Trabaja en tu worktree propio.' }, 'niega'],
  ['árboles de trabajo con la regla', { prompt: PP + 'Trabaja en tu worktree. No uses git stash.' }, 'pasa'],
  ['un fork hereda las reglas', { prompt: 'Sigue con lo tuyo.', subagent_type: 'fork' }, 'pasa'],
]
let malos = 0
for (const [nombre, input, esperado] of casos) {
  const dio = correr(input)
  if (dio !== esperado) malos++
  process.stdout.write(`  ${dio === esperado ? 'ok  ' : 'MAL '} ${nombre.padEnd(52)} esperaba ${esperado}, dio ${dio}\n`)
}
const otra = correr({ command: 'ls' }, 'Bash')
if (otra !== 'pasa') malos++
process.stdout.write(`  ${otra === 'pasa' ? 'ok  ' : 'MAL '} ${'otra herramienta no se revisa'.padEnd(52)} dio ${otra}\n`)
rmSync(tmp, { recursive: true, force: true })
process.stdout.write(`\n${casos.length + 1 - malos} de ${casos.length + 1} casos correctos.\n`)
process.stdout.write(malos ? 'ROJO.\n' : 'VERDE.\n')
process.exit(malos ? 1 : 0)
