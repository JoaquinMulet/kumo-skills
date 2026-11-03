#!/usr/bin/env node
/**
 * REVISOR DEL ENCARGO A UN SUBAGENTE. Hook PreToolUse del tool Agent.
 * Niega el encargo si le falta una instruccion que el dueno ya tuvo que
 * pagar con un error, porque lo que no se escribe el agente lo interpreta
 * a favor de terminar.
 *
 * 1. Que corra sus comandos en primer plano. El 29 oct 2026 un subagente
 *    lanzo sus pruebas en segundo plano, se quedo esperando el aviso, y el
 *    sistema lo corto a los 10 minutos con las pruebas ya en verde.
 * 2. Si va a leer la web, que respete robots.txt y no se haga pasar por un
 *    navegador. El 21 oct 2026 unos agentes mandaron un Referer falso y
 *    entraron por rutas que robots.txt cierra.
 * 3. Si trabaja en arboles de trabajo en paralelo, que no use git stash.
 *    El 26 sep 2026 un `pop` le copio 5 archivos ajenos a otro agente.
 *
 * Un fork (subagent_type "fork") hereda la conversacion entera y con ella
 * estas reglas, asi que no se revisa. Un error propio deja pasar.
 */
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const PRIMER_PLANO = /primer plano|foreground|sin segundo plano|no uses? (el )?segundo plano/i
// Verbos y herramientas de leer la web, no una URL suelta. Una URL de repo o de documentación
// en un encargo de código no es leer la web (medido el 3 nov 2026 sobre 251 encargos reales).
const LEE_WEB = /\b(WebFetch|WebSearch|navega|naveg[ao]r|busca en (la )?web|en internet|descarga(r)? (el|los|la|las)? ?(pdf|documento|archivo)|scrap|curl\s+-?\S*\s*https?:)/i
const ROBOTS = /robots\.txt/i
const EN_PARALELO = /\b(worktree|árbol(es)? de trabajo|arbol(es)? de trabajo)\b/i
const STASH = /stash/i

/**
 * Muchos encargos dicen «lee el encargo completo en C:/dev/x/ENCARGO.md». La instrucción
 * puede estar en ese archivo, así que se lee junto con el texto del encargo.
 */
function conArchivosNombrados(texto) {
  const rutas = texto.match(/[A-Za-z]:[\\/][^\s"'`<>|]*?\.(?:md|txt)\b/g) ?? []
  let todo = texto
  for (const r of rutas.slice(0, 5)) {
    try { todo += '\n' + readFileSync(r, 'utf8') } catch { /* el archivo no existe todavía */ }
  }
  return todo
}

export function revisar(entrada) {
  if (entrada.subagent_type === 'fork') return []
  // Lo que dispara una regla se busca solo en el texto del encargo. Las reglas cumplidas se
  // buscan también en los archivos que nombra. Si no, el texto de un documento que el agente
  // va a traducir («en internet») parecía un encargo de leer la web.
  const encargo = String(entrada.prompt ?? '')
  const todo = conArchivosNombrados(encargo)
  const faltan = []
  if (!PRIMER_PLANO.test(todo)) {
    faltan.push('Dile que corra sus comandos en primer plano, con timeout, y nunca en segundo plano.')
  }
  if (LEE_WEB.test(encargo) && !ROBOTS.test(todo)) {
    faltan.push('Va a leer la web. Dile que respete robots.txt y las condiciones de uso, que se identifique como programa y que no envíe cabeceras falsas.')
  }
  if (EN_PARALELO.test(encargo) && !STASH.test(todo)) {
    faltan.push('Trabaja en árboles de trabajo. Dile que no use git stash, git checkout -- . ni git reset --hard.')
  }
  return faltan
}

function main() {
  let evento
  try { evento = JSON.parse(readFileSync(0, 'utf8')) } catch { return }
  if (evento.tool_name !== 'Agent' && evento.tool_name !== 'Task') return
  let faltan
  try { faltan = revisar(evento.tool_input ?? {}) } catch { return }
  if (!faltan.length) return
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason: '[revisar-encargo] Al encargo le falta esto. ' + faltan.join(' '),
    },
  }))
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main()
