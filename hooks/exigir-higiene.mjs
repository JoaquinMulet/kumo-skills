#!/usr/bin/env node
/**
 * PORTON DE HIGIENE. Bloquea el commit en un repo que no tiene el
 * aparato de higiene instalado.
 *
 * Por que existe, dicho por el dueno el 21 de agosto de 2026.
 * «obliga la lectura y aplicacion de la tarea de higiene cada vez que se
 * trabaje, porque si no quedamos a merced del modelo si decide o no
 * aplicar eso».
 *
 * Tiene razon y la skill lo dice de si misma. NADA EXISTE HASTA QUE ALGO
 * LO DISPARA. Una obligacion escrita en prosa la cumple quien se acuerda
 * de leerla, o sea nadie de forma confiable. Escribir la regla otra vez,
 * mas grande o en mayusculas, no cambia eso.
 *
 * Este es el disparador. Corre como hook PreToolUse sobre Bash, mira si
 * el comando es un commit o un push, y si el repo no tiene su porton de
 * higiene, NIEGA la herramienta.
 *
 * QUE CUENTA COMO INSTALADO. que el repo tenga `core.hooksPath` apuntando
 * a una carpeta versionada con un `pre-commit` adentro. Se mide con git,
 * no leyendo archivos sueltos, porque lo que importa es el efecto.
 *
 * LA SALIDA DE EMERGENCIA, que es obligatoria. un guardia sin salida
 * explicita no protege, bloquea. Hay 2.
 *   - Un archivo `.kumo-sin-higiene` en la raiz del repo, con la razon
 *     escrita adentro. Vacio no sirve, porque la razon es el punto.
 *   - La variable KUMO_SIN_HIGIENE=1, para una vez.
 * La primera es la buena, porque deja la decision en el repo y con
 * nombre. La segunda es para emergencias y no deja rastro.
 *
 * Contrato del hook, verificado en la documentacion el 21 de agosto de
 * 2026. Recibe el JSON del evento por la entrada estandar y niega
 * imprimiendo `permissionDecision: "deny"`.
 */
import { execFileSync } from 'node:child_process'
import { existsSync, readFileSync } from 'node:fs'
import { join } from 'node:path'

/** Deja pasar. Un hook que no opina no imprime nada. */
function pasar() {
  process.exit(0)
}

function negar(razon) {
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason: razon,
    },
  }))
  process.exit(0)
}

function git(args, cwd) {
  try {
    return execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()
  } catch {
    return ''
  }
}

let evento
try {
  evento = JSON.parse(readFileSync(0, 'utf8'))
} catch {
  // Si no entiendo el evento, no soy quien para bloquear el trabajo.
  // Este guardia protege un proceso, no una frontera de seguridad.
  pasar()
}

if (evento.tool_name !== 'Bash') pasar()

const comando = String(evento.tool_input?.command ?? '')

/**
 * Los 2 momentos donde la higiene importa. Al registrar el cambio y al
 * publicarlo. Todo lo demas pasa sin ruido.
 *
 * Acepta las banderas GLOBALES que pueden ir entre `git` y su
 * subcomando, porque la version corta `git\s+(commit|push)` dejaba pasar
 * `git -C <ruta> commit` sin siquiera mirarlo. Era un paso libre y nadie
 * lo habia notado, justamente porque un guardia que no se dispara no
 * hace ruido. Lo encontre el 22 de agosto de 2026 escribiendo la prueba
 * de los 4 casos.
 *
 * No lleva un `.*` suelto a proposito. eso haria que `git log --grep
 * commit` disparara el guardia, y un guardia que se mete donde no lo
 * llaman se termina apagando.
 */
const ES_COMMIT_O_PUSH = /\bgit\s+(?:(?:-[A-Za-z]\s*|--[a-z-]+[= ])(?:"[^"]*"|'[^']*'|[^\s;&|]+)\s+|--[a-z-]+\s+)*(commit|push)\b/
if (!ES_COMMIT_O_PUSH.test(comando)) pasar()

if (process.env.KUMO_SIN_HIGIENE === '1') pasar()

/**
 * EL DIRECTORIO QUE SE JUZGA SALE DEL COMANDO, NO DE LA SESION.
 *
 * El 22 de agosto de 2026 este porton bloqueo un commit en un repositorio
 * que SI tenia el aparato instalado. La causa. el directorio de la sesion
 * habia quedado dentro de un clon de solo lectura anidado, y el comando
 * empezaba con `cd "<el repo de verdad>" && git commit`. El porton miro
 * el clon, no vio aparato, y nego.
 *
 * El falso positivo es la mitad visible. La otra mitad es peor y es muda.
 * con la sesion parada en un repo equipado y un comando que commitea
 * dentro de otro sin equipar, el porton DEJA PASAR. Un guardia que juzga
 * un objeto distinto del que la accion toca falla en las 2 direcciones, y
 * solo se nota en una.
 *
 * Regla general. lo que un guardia mide tiene que ser el MISMO objeto que
 * la accion modifica, y se resuelve desde la accion.
 */
function directorioDelComando(texto, porDefecto) {
  // `git -C <ruta>` es la forma explicita de git y manda sobre todo.
  const conC = /\bgit\s+-C\s+("([^"]+)"|'([^']+)'|(\S+))/.exec(texto)
  if (conC) return conC[2] ?? conC[3] ?? conC[4]
  // Un `cd <ruta>` al principio de la cadena. Solo al principio, porque
  // uno en medio puede estar dentro de un subshell o de otra rama.
  const conCd = /^\s*cd\s+("([^"]+)"|'([^']+)'|([^\s;&|]+))/.exec(texto)
  if (conCd) return conCd[2] ?? conCd[3] ?? conCd[4]
  return porDefecto
}

const cwd = directorioDelComando(comando, evento.cwd || process.cwd())
const raiz = git(['rev-parse', '--show-toplevel'], cwd)
if (!raiz) pasar()

const excusa = join(raiz, '.kumo-sin-higiene')
if (existsSync(excusa)) {
  const razon = readFileSync(excusa, 'utf8').trim()
  if (razon.length > 0) pasar()
  negar(
    `El repo tiene un archivo .kumo-sin-higiene VACIO. Ese archivo existe para dejar `
    + `escrita la razon de saltarse el aparato de higiene, y sin razon no cumple su unico `
    + `proposito. Escribe adentro por que este repo no lo lleva, o instala el aparato.`)
}

const carpeta = git(['config', '--get', 'core.hooksPath'], raiz)
const instalado = carpeta !== '' && existsSync(join(raiz, carpeta, 'pre-commit'))

if (instalado) pasar()

negar(
  `PORTON DE HIGIENE. Este repositorio no tiene el aparato de higiene instalado, asi que `
  + `no se puede commitear todavia.\n\n`
  + `Lo pidio el dueno para que la higiene deje de depender de que el modelo se acuerde. `
  + `El procedimiento completo son 7 pasos y esta en la skill desarrollo-riguroso, seccion `
  + `«Higiene continua del repo», con el detalle en su anexo reference/higiene-continua.md. `
  + `LEE LA SKILL COMPLETA antes de instalar, hasta su marcador de fin.\n\n`
  + `El minimo que este porton mide es que exista una carpeta de hooks VERSIONADA en el `
  + `repo con un pre-commit adentro, activada con:\n`
  + `  git config core.hooksPath <carpeta>\n\n`
  + `Y ese pre-commit tiene que correr TODO lo que se puede saber sin red. compilar, la `
  + `suite completa, las comprobaciones de clase y los instrumentos. Jamas se recorta por `
  + `lo que tarda.\n\n`
  + `Si este repo de verdad no lleva higiene (un scratch, un clon de solo lectura), `
  + `escribe la razon en un archivo .kumo-sin-higiene en su raiz. Vacio no sirve.`)
