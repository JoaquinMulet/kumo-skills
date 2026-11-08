#!/usr/bin/env node
/**
 * Prueba el hook de la raiz limpia con carpetas reales en una carpeta
 * temporal, en las 2 direcciones: niega o devuelve cuando aparece un archivo
 * suelto en la raiz, y no estorba en todo lo demas.
 *
 * Uso.  node hooks/probar-raiz-limpia.mjs
 * Sale con 0 si todos los casos dan lo esperado, y con 1 si alguno falla.
 */
import { execFileSync } from 'node:child_process'
import { mkdtempSync, mkdirSync, writeFileSync, rmSync, existsSync, readdirSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const HOOK = join(dirname(fileURLToPath(import.meta.url)), 'raiz-limpia.mjs')
const base = mkdtempSync(join(tmpdir(), 'raiz-'))
const RAIZ = join(base, 'dev')
mkdirSync(join(RAIZ, 'proyecto'), { recursive: true })
writeFileSync(join(RAIZ, 'viejo.log'), 'deuda vieja')
const FUERA = join(base, 'otra')
mkdirSync(FUERA)
const SESION = `prueba-${process.pid}`
const BARRA = String.fromCharCode(92)

function correr(evento, raices = RAIZ) {
  const r = execFileSync('node', [HOOK], {
    input: JSON.stringify({ session_id: SESION, ...evento }),
    encoding: 'utf8',
    env: { ...process.env, KUMO_RAICES_LIMPIAS: raices },
  })
  if (r.trim() === '') return 'pasa'
  try {
    const j = JSON.parse(r)
    if (j.hookSpecificOutput?.permissionDecision === 'deny') return 'niega'
    if (j.decision === 'block') return 'devuelve'
    return '?'
  } catch { return 'ilegible' }
}

const escribir = (herramienta, ruta, raices) =>
  correr({ hook_event_name: 'PreToolUse', tool_name: herramienta, tool_input: { file_path: ruta } }, raices)

/** Corre el hook antes y despues de un comando simulado por la funcion `hace`. */
function comando(herramienta, hace, id) {
  const ev = { tool_name: herramienta, tool_use_id: id, tool_input: { command: 'simulado' } }
  const antes = correr({ ...ev, hook_event_name: 'PreToolUse' })
  if (antes !== 'pasa') return `antes ${antes}`
  hace()
  return correr({ ...ev, hook_event_name: 'PostToolUse' })
}

// join() escribe con la barra del sistema. Esta forma prueba la otra barra en Windows.
const barrasNormales = (ruta) => ruta.split(BARRA).join('/')
const casos = [
  ['Write nuevo en la raiz', () => escribir('Write', join(RAIZ, 'commit.log')), 'niega'],
  ['Write nuevo en la raiz, con barras normales', () => escribir('Write', barrasNormales(join(RAIZ, 'x.txt'))), 'niega'],
  ['NotebookEdit nuevo en la raiz', () => correr({ hook_event_name: 'PreToolUse', tool_name: 'NotebookEdit',
    tool_input: { notebook_path: join(RAIZ, 'n.ipynb') } }), 'niega'],
  ['Write nuevo en la carpeta de un proyecto', () => escribir('Write', join(RAIZ, 'proyecto', 'a.log')), 'pasa'],
  ['Edit de un archivo que ya estaba en la raiz', () => escribir('Edit', join(RAIZ, 'viejo.log')), 'pasa'],
  ['Write nuevo fuera de la raiz', () => escribir('Write', join(FUERA, 'a.log')), 'pasa'],
  ['Write de desktop.ini en la raiz', () => escribir('Write', join(RAIZ, 'desktop.ini')), 'pasa'],
  ['Read en la raiz no se revisa', () => escribir('Read', join(RAIZ, 'commit.log')), 'pasa'],
  ['raiz que no existe', () => escribir('Write', join(base, 'nada', 'a.log'), join(base, 'nada')), 'pasa'],
  ['Bash que deja un archivo suelto', () => comando('Bash', () => writeFileSync(join(RAIZ, 'push.log'), 'x'), 'b1'), 'devuelve'],
  ['PowerShell que deja un archivo suelto', () => comando('PowerShell', () => writeFileSync(join(RAIZ, 'ps.txt'), 'x'), 'p1'), 'devuelve'],
  ['Bash que no crea nada', () => comando('Bash', () => {}, 'b2'), 'pasa'],
  ['Bash que crea una carpeta de proyecto', () => comando('Bash', () => mkdirSync(join(RAIZ, 'nuevo')), 'b3'), 'pasa'],
  ['Bash que escribe dentro de un proyecto', () => comando('Bash', () => writeFileSync(join(RAIZ, 'proyecto', 'b.log'), 'x'), 'b4'), 'pasa'],
  ['Bash que solo agrega a un archivo viejo', () => comando('Bash', () => writeFileSync(join(RAIZ, 'viejo.log'), 'mas'), 'b5'), 'pasa'],
  ['PostToolUse sin foto previa', () => correr({ hook_event_name: 'PostToolUse', tool_name: 'Bash', tool_use_id: 'sin-foto' }), 'pasa'],
  ['entrada que no es JSON', () => execFileSync('node', [HOOK], { input: 'no', encoding: 'utf8' }).trim() === '' ? 'pasa' : 'ilegible', 'pasa'],
]
if (process.platform === 'win32') {
  const gitBash = '/' + RAIZ[0].toLowerCase() + RAIZ.slice(2).split(BARRA).join('/')
  casos.push(['raiz escrita al estilo Git Bash', () => escribir('Write', join(RAIZ, 'g.log'), gitBash), 'niega'])
  casos.push(['Write nuevo en la raiz, en MAYUSCULAS', () => escribir('Write', join(RAIZ.toUpperCase(), 'm.log')), 'niega'])
}

let malos = 0
for (const [nombre, hacer, esperado] of casos) {
  let dio
  try { dio = hacer() } catch (e) { dio = `error ${e.message.slice(0, 60)}` }
  if (dio !== esperado) malos++
  process.stdout.write(`  ${dio === esperado ? 'ok  ' : 'MAL '} ${nombre.padEnd(46)} esperaba ${esperado}, dio ${dio}\n`)
}

// El hook no deja basura propia: cada PostToolUse borra la foto de su PreToolUse.
const fotos = join(tmpdir(), 'kumo-raiz-limpia')
const restos = existsSync(fotos) ? readdirSync(fotos).filter((n) => n.startsWith(SESION)) : []
if (restos.length) malos++
process.stdout.write(`  ${restos.length ? 'MAL ' : 'ok  '} ${'no quedan fotos de esta prueba'.padEnd(46)} quedaron ${restos.length}\n`)

rmSync(base, { recursive: true, force: true })
process.stdout.write(`\n${casos.length + 1 - malos} de ${casos.length + 1} casos correctos.\n`)
process.stdout.write(malos ? 'ROJO.\n' : 'VERDE.\n')
process.exit(malos ? 1 : 0)
