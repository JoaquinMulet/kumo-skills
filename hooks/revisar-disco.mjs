#!/usr/bin/env node
/**
 * REVISION DEL DISCO. Lista lo que sobra en la carpeta de proyectos (C:/dev por
 * defecto) para que el dueno decida que se borra. SOLO LEE: no borra, no mueve
 * y no escribe ningun archivo.
 *
 * Por que existe. El 8 nov 2026 la raiz de C:/dev tenia 425 archivos sueltos y
 * 248 carpetas, muchas de pruebas viejas, y el dueno dijo «se me esta llenando
 * el PC de basura». La regla 4 del plan de higiene pide una revision semanal
 * que muestre lo que sobra, y que nada se borre sin su ok. La corre una tarea
 * programada cada lunes.
 *
 * Que lista.
 * 1. Los archivos sueltos de la raiz, agrupados por familia (la parte del nombre
 *    antes del primer guion, guion bajo o punto).
 * 2. Las carpetas sin cambios en N dias (14 por defecto). Si la carpeta es un
 *    repo de git, dice si tiene cambios sin commit o commits sin subir, porque
 *    eso decide si borrarla pierde trabajo.
 * 3. Los arboles de trabajo de git (carpetas con un archivo .git) y su edad.
 * 4. Los enlaces (symlink o junction) que encontro: borrar una carpeta con un
 *    enlace adentro puede vaciar el destino (21 ago 2026).
 *
 * Uso.
 *   node hooks/revisar-disco.mjs                 informe en texto de C:/dev
 *   node hooks/revisar-disco.mjs --raiz D:/x     otra carpeta
 *   node hooks/revisar-disco.mjs --dias 30       otro umbral de carpetas quietas
 *   node hooks/revisar-disco.mjs --json          el mismo informe como dato
 *
 * Los avisos de progreso van por la salida de error, para no romper --json.
 */
import { readdirSync, lstatSync, statSync, readFileSync, existsSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const DIA = 24 * 60 * 60 * 1000
// Carpetas que se regeneran solas: su contenido no dice si alguien uso el proyecto.
const PESADAS = new Set(['node_modules', '.venv', 'venv', '.git', '.next', '__pycache__', 'dist', 'build',
  '.turbo', 'target', '.cache', '.pytest_cache', '.mypy_cache', '.ruff_cache'])
const MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

export const fecha = (ms) => {
  const d = new Date(ms)
  return `${d.getDate()} ${MESES[d.getMonth()]} ${d.getFullYear()}`
}

export const familia = (nombre) => {
  const sin = nombre.replace(/^\.+/, '')
  return (sin.split(/[-_.\s]/)[0] || nombre).toLowerCase()
}

function tamano(bytes) {
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))} KB`
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB`
  return `${(bytes / 1024 / 1024 / 1024).toFixed(1)} GB`
}

/** El ultimo cambio dentro de una carpeta, mirando hasta 3 niveles y sin entrar a las pesadas. */
function recorrer(dir, profundidad = 3, tope = 5000) {
  let ultimo = 0
  const enlaces = []
  let vistos = 0
  const pila = [[dir, 0]]
  try { ultimo = statSync(dir).mtimeMs } catch { /* nada */ }
  while (pila.length && vistos < tope) {
    const [d, nivel] = pila.pop()
    let entradas
    try { entradas = readdirSync(d, { withFileTypes: true }) } catch { continue }
    for (const e of entradas) {
      if (++vistos > tope) break
      const ruta = join(d, e.name)
      let st
      try { st = lstatSync(ruta) } catch { continue }
      if (st.isSymbolicLink()) { enlaces.push(ruta.replace(/\\/g, '/')); continue }
      // La fecha de una carpeta pesada cambia sola (un git status, un npm install) y no dice que
      // alguien trabajo en el proyecto: no cuenta.
      if (st.isDirectory() && PESADAS.has(e.name)) continue
      ultimo = Math.max(ultimo, st.mtimeMs)
      if (st.isDirectory() && nivel + 1 < profundidad) pila.push([ruta, nivel + 1])
    }
  }
  return { ultimo, enlaces }
}

// --no-optional-locks: sin esto, git status reescribe el indice del repo que revisa, y la revision
// dejaria de ser de solo lectura.
function git(dir, ...args) {
  return execFileSync('git', ['--no-optional-locks', '-C', dir, ...args], { encoding: 'utf8', timeout: 20000, stdio: ['ignore', 'pipe', 'ignore'] })
}

/** Que se pierde si se borra el repo: cambios sin commit y commits que ningun remoto tiene. */
function estadoGit(dir) {
  try {
    const cambios = git(dir, 'status', '--porcelain').split('\n').filter(Boolean).length
    const remotos = git(dir, 'remote').split('\n').filter(Boolean).length
    const sinSubir = git(dir, 'log', '--branches', '--not', '--remotes', '--oneline').split('\n').filter(Boolean).length
    return { cambios, remotos, sinSubir }
  } catch {
    return null
  }
}

/** Un arbol de trabajo tiene un ARCHIVO .git que apunta a su carpeta en el repo principal. */
function arbolDeTrabajo(dir, ahora) {
  const punto = join(dir, '.git')
  try {
    if (!lstatSync(punto).isFile()) return null
    const adm = readFileSync(punto, 'utf8').match(/^gitdir:\s*(.+)$/m)?.[1]?.trim()
    if (!adm) return null
    const gitdir = join(adm, 'gitdir')
    const creado = existsSync(gitdir) ? statSync(gitdir).mtimeMs : null
    const principal = adm.replace(/\\/g, '/').replace(/\/\.git\/worktrees\/[^/]+$/, '')
    return { principal, dias: creado ? Math.floor((ahora - creado) / DIA) : null }
  } catch {
    return null
  }
}

export function revisar(raiz, { dias = 14, ahora = Date.now(), avisar = () => {} } = {}) {
  const entradas = readdirSync(raiz, { withFileTypes: true })
  const archivos = []
  const carpetas = []
  for (const e of entradas) {
    const ruta = join(raiz, e.name)
    let st
    try { st = lstatSync(ruta) } catch { continue }
    if (st.isSymbolicLink()) carpetas.push({ nombre: e.name, enlace: true })
    else if (st.isFile()) archivos.push({ nombre: e.name, bytes: st.size, cambio: st.mtimeMs })
    else if (st.isDirectory()) carpetas.push({ nombre: e.name })
  }

  const familias = new Map()
  for (const a of archivos) {
    const f = familias.get(familia(a.nombre)) ?? { familia: familia(a.nombre), archivos: 0, bytes: 0, ultimo: 0 }
    f.archivos++
    f.bytes += a.bytes
    f.ultimo = Math.max(f.ultimo, a.cambio)
    familias.set(f.familia, f)
  }

  avisar(`Revisando ${carpetas.length} carpetas de ${raiz}. Suele tardar entre 30 segundos y 3 minutos.`)
  const quietas = []
  const arboles = []
  const enlaces = []
  let n = 0
  for (const c of carpetas) {
    if (++n % 50 === 0) avisar(`  ${n} de ${carpetas.length} carpetas revisadas`)
    const ruta = join(raiz, c.nombre)
    if (c.enlace) { enlaces.push(ruta.replace(/\\/g, '/')); continue }
    const { ultimo, enlaces: adentro } = recorrer(ruta)
    enlaces.push(...adentro)
    const arbol = arbolDeTrabajo(ruta, ahora)
    if (arbol) arboles.push({ nombre: c.nombre, ...arbol })
    const quieta = Math.floor((ahora - ultimo) / DIA)
    if (quieta >= dias) {
      const esRepo = existsSync(join(ruta, '.git'))
      quietas.push({ nombre: c.nombre, ultimo, dias: quieta, git: esRepo ? estadoGit(ruta) : undefined })
    }
  }
  quietas.sort((a, b) => a.ultimo - b.ultimo)
  return {
    raiz: raiz.replace(/\\/g, '/'),
    fecha: ahora,
    umbralDias: dias,
    archivosSueltos: archivos.length,
    bytesSueltos: archivos.reduce((s, a) => s + a.bytes, 0),
    familias: [...familias.values()].sort((a, b) => b.archivos - a.archivos),
    carpetas: carpetas.length,
    quietas,
    arboles,
    enlaces,
  }
}

function textoGit(g) {
  if (g === undefined) return 'no es repo'
  if (g === null) return 'git no respondio'
  const partes = []
  if (g.cambios) partes.push(`${g.cambios} cambios sin commit`)
  if (!g.remotos) partes.push('sin remoto')
  else if (g.sinSubir) partes.push(`${g.sinSubir} commits sin subir`)
  return partes.length ? partes.join(', ') : 'todo subido'
}

export function informe(r) {
  const l = []
  l.push(`Revision del disco de ${r.raiz}, ${fecha(r.fecha)}`)
  l.push('Este informe solo lee. No borro ni movio nada.')
  l.push('')
  l.push(`1. Archivos sueltos en la raiz: ${r.archivosSueltos} (${tamano(r.bytesSueltos)})`)
  for (const f of r.familias.slice(0, 15)) {
    l.push(`   ${f.familia.padEnd(22)} ${String(f.archivos).padStart(4)} archivos, el ultimo del ${fecha(f.ultimo)}`)
  }
  if (r.familias.length > 15) l.push(`   y ${r.familias.length - 15} familias mas`)
  l.push('')
  l.push(`2. Carpetas sin cambios en ${r.umbralDias} dias o mas: ${r.quietas.length} de ${r.carpetas}`)
  for (const q of r.quietas) {
    l.push(`   ${q.nombre.padEnd(34)} ${String(q.dias).padStart(4)} dias  ${textoGit(q.git)}`)
  }
  l.push('')
  l.push(`3. Arboles de trabajo de git: ${r.arboles.length}`)
  for (const a of r.arboles) {
    const edad = a.dias === null ? 'edad desconocida' : `${a.dias} dias${a.dias >= 3 ? ', ya deberia estar quitado' : ''}`
    l.push(`   ${a.nombre}, de ${a.principal}, ${edad}`)
  }
  l.push('')
  l.push(`4. Enlaces encontrados (borrar su carpeta puede vaciar el destino): ${r.enlaces.length}`)
  for (const e of r.enlaces.slice(0, 20)) l.push(`   ${e}`)
  if (r.enlaces.length > 20) l.push(`   y ${r.enlaces.length - 20} mas`)
  return l.join('\n') + '\n'
}

function main() {
  const args = process.argv.slice(2)
  const valor = (nombre, defecto) => {
    const i = args.indexOf(nombre)
    return i >= 0 && args[i + 1] ? args[i + 1] : defecto
  }
  const raiz = valor('--raiz', 'C:/dev')
  const dias = Number(valor('--dias', '14'))
  if (!existsSync(raiz)) {
    process.stderr.write(`No existe la carpeta ${raiz}. No revise nada.\n`)
    process.exit(2)
  }
  const r = revisar(raiz, { dias, avisar: (m) => process.stderr.write(m + '\n') })
  process.stdout.write(args.includes('--json') ? JSON.stringify(r, null, 1) + '\n' : informe(r))
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main()
