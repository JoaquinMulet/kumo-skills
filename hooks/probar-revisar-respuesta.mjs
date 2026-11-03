#!/usr/bin/env node
/**
 * Prueba el revisor de respuestas en las 2 direcciones. Cada defecto real
 * que el usuario corrigio desde agosto de 2026 tiene que bloquear, y una
 * respuesta sana no tiene que estorbar. Un guardia que bloquea de mas se
 * termina apagando entero.
 *
 * Uso.  node hooks/probar-revisar-respuesta.mjs
 * Sale con 0 si todos los casos dan lo esperado, y con 1 si alguno falla.
 */
import { execFileSync } from 'node:child_process'
import { mkdtempSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const HOOK = join(dirname(fileURLToPath(import.meta.url)), 'revisar-respuesta.mjs')
const F = '```'
const RAYA = String.fromCharCode(0x2014)

function correr(evento) {
  const r = execFileSync('node', [HOOK], { input: JSON.stringify(evento), encoding: 'utf8' })
  if (r.trim() === '') return 'pasa'
  try { return JSON.parse(r).decision === 'block' ? 'bloquea' : '?' } catch { return 'salida ilegible' }
}

/** Un transcript falso con la forma real de Claude Code, una entrada por linea. */
function transcript(texto) {
  const dir = mkdtempSync(join(tmpdir(), 'revisar-'))
  const ruta = join(dir, 'sesion.jsonl')
  const lineas = [
    { type: 'user', message: { content: 'hola' } },
    { type: 'assistant', message: { content: [{ type: 'text', text: 'texto viejo con && suelto' }] } },
    { type: 'assistant', message: { content: [{ type: 'thinking', thinking: 'x' }] } },
    { type: 'assistant', message: { content: [{ type: 'text', text: texto }] } },
    { type: 'assistant', message: { content: [{ type: 'tool_use', name: 'Bash', input: {} }] } },
  ]
  writeFileSync(ruta, lineas.map((l) => JSON.stringify(l)).join('\n') + '\n')
  return ruta
}

const casos = [
  ['&& en un bloque bash (4 ago 2026)', `Corre esto.\n${F}bash\ncd "C:/x" && npm test\n${F}`, 'bloquea'],
  ['hueco <id> (21 ago 2026)', `${F}bash\ngh run view <id> --json conclusion\n${F}`, 'bloquea'],
  ['hueco TU_CLAVE', `${F}powershell\nsetx API TU_CLAVE\n${F}`, 'bloquea'],
  ['pedir pegar un secreto (5 sep 2026)', `${F}powershell\n$k = Read-Host 'pega la llave'\n${F}`, 'bloquea'],
  ['Out-File con BOM (10 ago 2026)', `${F}powershell\n$j | Out-File -Encoding utf8 "C:/a.json"\n${F}`, 'bloquea'],
  ['chrome:// en un bloque (17 ago 2026)', `${F}bash\nchrome://gpu\n${F}`, 'bloquea'],
  ['voseo con tilde', 'Revisá el archivo y avisame.', 'bloquea'],
  ['raya en la prosa', `Listo ${RAYA} quedó publicado.`, 'bloquea'],
  ['respuesta sana con ; y ruta absoluta', `Corre esto.\n${F}bash\ncd "C:/x"; npm test\n${F}\nRevisa el resultado.`, 'pasa'],
  ['&& dentro de codigo en linea no cuenta', 'El `&&` de bash rompe PowerShell.', 'pasa'],
  ['&& en un bloque js no cuenta', `${F}js\nif (a && b) {}\n${F}`, 'pasa'],
  ['heredoc << no es un hueco', `${F}bash\ncat <<'EOF'\nhola\nEOF\n${F}`, 'pasa'],
  ['raya dentro de un bloque no cuenta', `${F}text\nA ${RAYA} B\n${F}`, 'pasa'],
  ['voseo dentro de codigo en linea no cuenta', 'La regla prohibe `revisá`.', 'pasa'],
  ['pretérito «escribí» no es voseo', 'Escribí el archivo y elegí la ruta corta.', 'pasa'],
  ['raya en una celda de tabla no cuenta', `| Skill | Camino |\n|---|---|\n| tdd | ${RAYA} |`, 'pasa'],
  ['error de la API no lo escribió el agente', `API Error: Can't reach the API server ${RAYA} check DNS`, 'pasa'],
]

let malos = 0
for (const [nombre, texto, esperado] of casos) {
  const dio = correr({ transcript_path: transcript(texto) })
  const ok = dio === esperado
  if (!ok) malos++
  process.stdout.write(`  ${ok ? 'ok  ' : 'MAL '} ${nombre.padEnd(44)} esperaba ${esperado}, dio ${dio}\n`)
}
const bucle = correr({ transcript_path: transcript(`${F}bash\na && b\n${F}`), stop_hook_active: true })
if (bucle !== 'pasa') malos++
process.stdout.write(`  ${bucle === 'pasa' ? 'ok  ' : 'MAL '} ${'segundo intento del turno deja pasar'.padEnd(44)} dio ${bucle}\n`)
const roto = correr({ transcript_path: 'C:/no/existe.jsonl' })
if (roto !== 'pasa') malos++
process.stdout.write(`  ${roto === 'pasa' ? 'ok  ' : 'MAL '} ${'transcript que no existe falla abierto'.padEnd(44)} dio ${roto}\n`)

process.stdout.write(`\n${casos.length + 2 - malos} de ${casos.length + 2} casos correctos.\n`)
process.stdout.write(malos ? 'ROJO.\n' : 'VERDE. Bloquea cuando debe y no estorba cuando no.\n')
process.exit(malos ? 1 : 0)
