#!/usr/bin/env node
/**
 * RAIZ LIMPIA. Hook de Write y Edit (PreToolUse) y de los comandos de Bash y
 * PowerShell (PreToolUse y PostToolUse).
 *
 * Por que existe. El 8 nov 2026 la raiz de C:/dev tenia 425 archivos sueltos:
 * registros de commits, de despliegues y de pruebas que el agente escribio ahi
 * en vez de usar la carpeta de borradores de la conversacion. El dueno lo dijo
 * asi: «se me esta llenando el PC de basura por no estar preocupandonos de
 * tener un plan para desarrollar de manera limpia y eficiente». La regla «lo
 * temporal va a la carpeta de borradores» ya existia en prosa y no alcanzo.
 *
 * Que hace.
 * 1. Write o Edit que CREA un archivo directo en una raiz limpia: lo niega
 *    antes de escribir. Editar un archivo que ya estaba ahi pasa, porque esos
 *    son deuda vieja y la limpia la revision semanal, no este hook.
 * 2. Un comando de Bash o PowerShell: antes de correr guarda la lista de
 *    archivos de cada raiz, y al terminar la compara. Si aparecio un archivo
 *    nuevo, se lo devuelve al agente para que lo mueva en ese mismo turno. Un
 *    comando no se puede adivinar leyendolo (un script de Python escribe donde
 *    quiere), por eso se mide el efecto y no el texto del comando.
 *
 * Las carpetas nuevas en la raiz pasan: una carpeta por proyecto es la regla.
 *
 * Las raices salen de KUMO_RAICES_LIMPIAS, separadas por punto y coma. Si no
 * esta, es C:/dev. Una raiz que no existe no se revisa. Un error propio del
 * hook deja pasar, porque un hook roto no puede trabar el trabajo.
 */
import { readFileSync, writeFileSync, existsSync, readdirSync, mkdirSync, rmSync, statSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { tmpdir } from 'node:os'
import { fileURLToPath } from 'node:url'

const ESCRIBEN = new Set(['Write', 'Edit', 'MultiEdit', 'NotebookEdit'])
const COMANDOS = new Set(['Bash', 'PowerShell'])
const IGNORAR = new Set(['desktop.ini', 'thumbs.db', '.ds_store'])
const FOTOS = join(tmpdir(), 'kumo-raiz-limpia')
const UN_DIA = 24 * 60 * 60 * 1000

/** Barras normales, sin barra final, y la forma /c/dev de Git Bash como C:/dev. */
export function normalizar(ruta) {
  let r = String(ruta ?? '').trim().replace(/\\/g, '/')
  const unidad = r.match(/^\/([a-zA-Z])(\/|$)/)
  if (unidad) r = `${unidad[1].toUpperCase()}:/${r.slice(3)}`
  return r.replace(/\/+$/, '')
}

/** La forma de comparar 2 rutas. En Windows no importan las mayusculas. */
export function clave(ruta) {
  const r = normalizar(ruta)
  return process.platform === 'win32' ? r.toLowerCase() : r
}

export function raices(env = process.env) {
  return String(env.KUMO_RAICES_LIMPIAS ?? 'C:/dev').split(';').map(normalizar).filter(Boolean)
}

/** La raiz limpia donde cae la ruta, si cae DIRECTO en una. Si no, null. */
export function raizDe(ruta, lista = raices()) {
  const r = clave(ruta)
  const padre = r.slice(0, r.lastIndexOf('/'))
  return lista.find((x) => clave(x) === padre) ?? null
}

export function archivosSueltos(raiz) {
  try {
    return readdirSync(raiz, { withFileTypes: true })
      .filter((e) => e.isFile() && !IGNORAR.has(e.name.toLowerCase()))
      .map((e) => e.name)
  } catch {
    return null
  }
}

function rutaFoto(ev) {
  const id = `${ev.session_id ?? 'sin-sesion'}-${ev.tool_use_id ?? 'sin-id'}`
  return join(FOTOS, id.replace(/[^A-Za-z0-9_-]/g, '_') + '.json')
}

/** Borra las fotos de mas de 1 dia: quedan cuando otro hook niega el comando y no hay PostToolUse. */
function barrerFotosViejas() {
  try {
    for (const n of readdirSync(FOTOS)) {
      const p = join(FOTOS, n)
      if (Date.now() - statSync(p).mtimeMs > UN_DIA) rmSync(p, { force: true })
    }
  } catch { /* sin carpeta de fotos */ }
}

const nombreDe = (ruta) => normalizar(ruta).split('/').pop()

export function revisarEscritura(ruta, lista = raices()) {
  if (!ruta) return ''
  const raiz = raizDe(ruta, lista)
  if (!raiz || !existsSync(raiz) || existsSync(ruta)) return ''
  if (IGNORAR.has(nombreDe(ruta).toLowerCase())) return ''
  return `No se crean archivos sueltos en la raiz de ${raiz} (plan de higiene del 8 nov 2026). `
    + 'Lo temporal (registros, scripts de una vez, capturas) va a la carpeta de borradores de la '
    + `conversacion. Lo que es de un proyecto va a la carpeta de ese proyecto, por ejemplo ${raiz}/<proyecto>/_trabajo/.`
}

export function nuevos(antes, lista = raices()) {
  const hallados = []
  for (const raiz of lista) {
    if (!(raiz in antes)) continue
    const previos = new Set(antes[raiz])
    for (const n of archivosSueltos(raiz) ?? []) {
      if (!previos.has(n)) hallados.push(`${raiz}/${n}`)
    }
  }
  return hallados
}

function main() {
  let ev
  try { ev = JSON.parse(readFileSync(0, 'utf8')) } catch { return }
  const lista = raices()
  const evento = ev.hook_event_name

  if (evento === 'PreToolUse' && ESCRIBEN.has(ev.tool_name)) {
    let razon = ''
    try { razon = revisarEscritura(ev.tool_input?.file_path ?? ev.tool_input?.notebook_path, lista) } catch { return }
    if (!razon) return
    process.stdout.write(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'deny',
        permissionDecisionReason: '[raiz-limpia] ' + razon,
      },
    }))
    return
  }

  if (!COMANDOS.has(ev.tool_name)) return

  if (evento === 'PreToolUse') {
    try {
      const foto = {}
      for (const raiz of lista) {
        const sueltos = archivosSueltos(raiz)
        if (sueltos) foto[raiz] = sueltos
      }
      mkdirSync(FOTOS, { recursive: true })
      barrerFotosViejas()
      writeFileSync(rutaFoto(ev), JSON.stringify(foto))
    } catch { /* sin foto no hay comparacion */ }
    return
  }

  if (evento === 'PostToolUse') {
    const p = rutaFoto(ev)
    let hallados = []
    try {
      if (!existsSync(p)) return
      hallados = nuevos(JSON.parse(readFileSync(p, 'utf8')), lista)
    } catch { return } finally {
      try { rmSync(p, { force: true }) } catch { /* nada */ }
    }
    if (!hallados.length) return
    process.stdout.write(JSON.stringify({
      decision: 'block',
      reason: `[raiz-limpia] Este comando dejo ${hallados.length} archivo(s) suelto(s) en una raiz que se `
        + `mantiene limpia: ${hallados.join(', ')}. Muevelos ahora, antes de seguir. Lo temporal va a la carpeta `
        + 'de borradores de la conversacion, y lo que es de un proyecto va a la carpeta de ese proyecto. Si '
        + 'otro programa los creo al mismo tiempo y no este comando, diselo al usuario y no los toques.',
    }))
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main()
