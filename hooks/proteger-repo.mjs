#!/usr/bin/env node
/**
 * PROTECTOR DEL REPO. Hook PreToolUse de Bash. Niega 6 comandos que ya
 * rompieron un repo o escondieron un error, cada uno escrito como regla
 * en el CLAUDE.md global del dueno y repetido igual.
 *
 * 1. Una tuberia que esconde el codigo de salida de un verificador
 *    (`pytest | tail`, `gh run watch | tail`) sin `pipefail` ni
 *    `PIPESTATUS`. El 3 nov 2026 un `| tail` reporto 0 sobre 2 pruebas
 *    que habian salido con 1.
 * 2. Un `&` dentro de un comando que ya va en segundo plano. El aviso de
 *    termino llega al lanzarlo y lo que sigue corre en otra carpeta
 *    (21 y 22 oct 2026).
 * 3. `git stash`, `git checkout -- .` o `git reset --hard` en un repo con
 *    arboles de trabajo hermanos. `refs/stash` es compartido, y el 26 sep
 *    2026 un `pop` le copio 5 archivos ajenos a otro agente.
 * 4. `git worktree add` hacia una carpeta dentro de OneDrive. El 26 sep
 *    2026 OneDrive llego a 90 mil segundos de CPU y trabo 4 agentes.
 * 5. `git commit` sin `git diff --cached --stat` antes en el mismo
 *    comando. Un indice que venia cargado se lleva todo (4 sep 2026, y
 *    otra vez el 3 nov 2026 con 120 archivos).
 * 6. `git commit` con un script `.sh` en el indice sin modo 100755 o sin
 *    fin de linea LF. El 25 sep 2026 un deploy murio con «Permission
 *    denied».
 *
 * Un error propio deja pasar (falla abierto). Este guardia protege un
 * proceso, no una frontera de seguridad.
 */
import { execFileSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { resolve, isAbsolute } from 'node:path'
import { fileURLToPath } from 'node:url'
import { carpetaDeGit, msys, tapar } from './carpeta-del-comando.mjs'

// El verificador tiene que ser el comando que corre, al inicio de un tramo, no un argumento.
// Un `grep validar-skills.py | head` solo nombra el archivo (falso positivo medido el 3 nov 2026).
const VERIFICADOR = new RegExp(
  String.raw`(?:^|[;&|(]|&&|\|\|)\s*(?:timeout\s+\d+\s+|env\s+\S+=\S+\s+)*`
  + String.raw`(?:uv\s+run\s+(?:--[\w-]+(?:[= ]\S+)?\s+)*(?:python\s+(?:-\S+\s+)*)?|npx\s+|node\s+|python3?\s+(?:-\S+\s+)*|pnpm\s+(?:--filter\s+\S+\s+)?)?`
  + String.raw`\S*(pytest|npm\s+(?:run\s+)?test|test\b|vitest|jest|cargo\s+test|go\s+test|gh\s+run\s+watch|git\s+push|probar-[\w-]+\.mjs|validar[\w-]*\.py|centinelas\.py)`
  + String.raw`[^;|&]*\|\s*(tail|head|grep|sed|awk|cut|less|more|tee)\b`)
const GIT_GLOBAL = String.raw`\bgit\s+(?:(?:-[A-Za-z]\s*|--[a-z-]+[= ])(?:"[^"]*"|'[^']*'|[^\s;&|]+)\s+|--[a-z-]+\s+)*`
const ES_COMMIT = new RegExp(GIT_GLOBAL + String.raw`commit\b`)
// Solo los subcomandos de stash que escriben. `git stash list` y `show` solo leen.
const DESTRUCTIVO = new RegExp(GIT_GLOBAL
  + String.raw`(stash(?:\s+(?:push|pop|apply|drop|clear|save|branch|-u|-k|--include-untracked|--keep-index)\b|\s*(?:$|[;&|)]))|checkout\s+--\s+\.|reset\s+--hard\b)`, 'm')
const WORKTREE_ADD = new RegExp(GIT_GLOBAL + String.raw`worktree\s+add\s+([^;&|]*)`)
// Opciones de `git worktree add` que se comen el argumento que les sigue.
const CON_ARGUMENTO = new Set(['-b', '-B', '--reason'])

/** La ruta de destino de `git worktree add`, o '' si no se puede saber sin ejecutar. */
function destinoDelArbol(resto) {
  const fichas = resto.match(/"[^"]*"|'[^']*'|\S+/g) ?? []
  for (let i = 0; i < fichas.length; i++) {
    const f = fichas[i]
    if (CON_ARGUMENTO.has(f)) { i++; continue }
    if (f.startsWith('-')) continue
    const ruta = f.replace(/^["']|["']$/g, '')
    if (ruta.includes('$')) return ''
    // Ruta de MSYS como /c/dev/x. resolve() de Windows la leeria como C:/c/dev/x.
    return ruta.replace(/^\/([a-zA-Z])\//, '$1:/')
  }
  return ''
}

// Sin las variables GIT_* del ambiente, para que git mire el repo de la carpeta y no otro.
const ENV = Object.fromEntries(Object.entries(process.env).filter(([k]) => !k.startsWith('GIT_')))

function git(args, cwd) {
  try {
    return execFileSync('git', args, { cwd, env: ENV, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()
  } catch {
    return ''
  }
}

/** Quita lo que va entre comillas y los heredocs, para no juzgar texto que no se ejecuta. */
function sinHeredocs(texto) {
  return texto.replace(/<<-?\s*'?(\w+)'?[\s\S]*?\n\1\b/g, ' ')
}

function soloCodigo(texto) {
  return sinHeredocs(texto)
    .replace(/"(?:[^"\\]|\\.)*"/g, '""')
    .replace(/'[^']*'/g, "''")
}

export function revisar(comando, { enSegundoPlano = false, cwd = process.cwd() } = {}) {
  const codigo = soloCodigo(comando)

  // PIPESTATUS se busca en el comando original, porque casi siempre va entre comillas
  // («echo "EXIT ${PIPESTATUS[0]}"») y soloCodigo() las vacía.
  if (VERIFICADOR.test(codigo) && !/pipefail|PIPESTATUS/.test(comando)) {
    return 'La tuberia esconde el codigo de salida del verificador. `cmd | tail` reporta el de tail. '
      + 'Corre el verificador solo, o agrega `set -o pipefail`, o lee `${PIPESTATUS[0]}`.'
  }

  if (enSegundoPlano && /(^|[^&<>|])&(?![&>])/.test(codigo.replace(/[0-9]?>&[0-9-]?|&>>?/g, ' '))) {
    return 'El comando ya va en segundo plano y trae un `&` adentro. El aviso de termino llegaria al lanzarlo. '
      + 'Saca el `&`, y si son 2 trabajos lanzalos en 2 llamadas.'
  }

  // La carpeta de cada git sale de los cd que corren ANTES de ese git (carpeta-del-comando.mjs). Si no
  // se puede saber sin ejecutar, es null y esa regla no juzga. Las posiciones se buscan con las
  // comillas tapadas, para que un texto entre comillas no cuente como comando.
  const texto = sinHeredocs(comando)
  const tapado = tapar(texto)
  const carpetaDe = (re) => {
    const m = re.exec(tapado)
    return m ? carpetaDeGit(texto, m.index, cwd) : null
  }

  const dirDestructivo = DESTRUCTIVO.test(codigo) ? carpetaDe(DESTRUCTIVO) : null
  if (dirDestructivo) {
    const arboles = git(['worktree', 'list', '--porcelain'], dirDestructivo).split('\n').filter((l) => l.startsWith('worktree ')).length
    if (arboles > 1) {
      return `Este repo tiene ${arboles} arboles de trabajo. git stash, git checkout -- . y git reset --hard `
        + 'tocan estado compartido entre ellos. Revierte a mano, o prueba en un `git worktree add` desechable.'
    }
  }

  // Sin heredocs, porque un mensaje de commit puede nombrar el comando (pasó el 3 nov 2026).
  // Las comillas se quedan, porque la ruta del árbol suele ir entre ellas.
  const wt = WORKTREE_ADD.exec(texto)
  const ruta = wt ? destinoDelArbol(wt[1]) : ''
  if (ruta) {
    // Una ruta absoluta se juzga siempre. Una relativa, solo si se sabe desde qué carpeta corre.
    const base = isAbsolute(msys(ruta)) ? '' : carpetaDeGit(texto, wt.index, cwd)
    const destino = base === null ? '' : resolve(base || '', msys(ruta))
    if (/onedrive/i.test(destino)) {
      return `El arbol de trabajo iria dentro de OneDrive (${destino}). OneDrive sincroniza cada archivo que `
        + 'escriben los procesos y traba la maquina. Crealo en C:/dev/.'
    }
  }

  if (ES_COMMIT.test(codigo)) {
    const iCommit = codigo.search(ES_COMMIT)
    const iStat = codigo.search(/\bgit\s+(?:-C\s+\S+\s+)?diff\s+--cached\s+--stat\b/)
    if (iStat < 0 || iStat > iCommit) {
      return 'Antes del commit, en el mismo comando, corre `git diff --cached --stat` y confirma que la lista '
        + 'es la que el mensaje describe. Un indice que venia cargado se lleva todo.'
    }
    const dirCommit = carpetaDe(ES_COMMIT)
    const raiz = dirCommit ? git(['rev-parse', '--show-toplevel'], dirCommit) : ''
    if (raiz) {
      const scripts = git(['diff', '--cached', '--name-only', '--diff-filter=AM'], raiz)
        .split('\n').filter((f) => f.endsWith('.sh'))
      for (const f of scripts) {
        const modo = git(['ls-files', '-s', '--', f], raiz).split(/\s+/)[0]
        const eol = git(['ls-files', '--eol', '--', f], raiz)
        if (modo && modo !== '100755') {
          return `${f} entra al indice con modo ${modo}. Corre \`git update-index --chmod=+x ${f}\` despues del git add.`
        }
        if (eol && !eol.startsWith('i/lf')) {
          return `${f} entra al indice sin fin de linea LF (${eol.split(/\s+/)[0]}). Pasalo a LF antes del commit.`
        }
      }
    }
  }
  return ''
}

function main() {
  let evento
  try { evento = JSON.parse(readFileSync(0, 'utf8')) } catch { return }
  if (evento.tool_name !== 'Bash') return
  let razon = ''
  try {
    razon = revisar(String(evento.tool_input?.command ?? ''), {
      enSegundoPlano: evento.tool_input?.run_in_background === true,
      cwd: evento.cwd || process.cwd(),
    })
  } catch { return }
  if (!razon) return
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason: '[proteger-repo] ' + razon,
    },
  }))
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main()
