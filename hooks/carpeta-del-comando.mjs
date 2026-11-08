/**
 * LA CARPETA DONDE CORRE UNA PARTE DE UN COMANDO DE BASH.
 *
 * La usan proteger-repo.mjs y exigir-higiene.mjs, que juzgan el repo que toca
 * un comando. Antes los 2 miraban solo un `cd` al principio del comando, y el
 * 8 nov 2026 eso fallo en las 2 direcciones. Un comando que entraba por una
 * variable (`S=...; cd "$S" && ... && cd r && git worktree add -q ../w`) se
 * juzgo desde la carpeta de la sesion, que estaba en OneDrive, y el gancho
 * nego un arbol que iba fuera. Con 2 `cd` seguidos se juzgaba el primero, y
 * un commit en un repo sin aparato pasaba callado.
 *
 * Sigue en orden cada `cd` que corre antes de la posicion. Devuelve null
 * cuando la carpeta no se puede saber sin ejecutar: un `cd` con variable o
 * `cd -`, uno despues de `||` o de una tuberia (puede no correr), y uno dentro
 * de un subshell, de un bloque o de un if (no cuenta afuera, o depende de una
 * condicion). Quien la llama no juzga lo que no ve.
 */
import { resolve, isAbsolute, join } from 'node:path'
import { homedir } from 'node:os'

/** La forma /c/dev de Git Bash como C:/dev, para que resolve() de Windows la entienda. */
export const msys = (ruta) => String(ruta).replace(/^\/([a-zA-Z])(\/|$)/, (_, unidad) => `${unidad.toUpperCase()}:/`)

/**
 * Tapa lo que va entre comillas sin mover las posiciones, para que un texto
 * como "luego hago cd x" no cuente como un cd.
 */
export const tapar = (texto) => String(texto).replace(/"(?:[^"\\]|\\.)*"|'[^']*'/g,
  (s) => s[0] + '_'.repeat(s.length - 2) + s[s.length - 1])

const CD = /(^|&&|\|\||[;&|(\n{]|\bthen|\belse|\bdo)\s*cd(?=\s|;|&|\||\)|$)/g
const DESTINO = /^\s+("([^"]*)"|'([^']*)'|([^\s;&|)]+))/
const NO_SEGURO = new Set(['||', '|', '(', '{', 'then', 'else', 'do'])

/** La carpeta en la que corre lo que empieza en `indice` de `texto`, o null si no se puede saber. */
export function carpetaEn(texto, indice, porDefecto) {
  const antes = String(texto).slice(0, indice)
  let dir = resolve(msys(porDefecto))
  for (const m of tapar(antes).matchAll(CD)) {
    if (NO_SEGURO.has(m[1])) return null
    const d = DESTINO.exec(antes.slice(m.index + m[0].length))
    if (!d) { dir = homedir(); continue }
    const destino = d[2] ?? d[3] ?? d[4]
    if (/[$`]/.test(destino) || destino === '-') return null
    if (destino === '~' || destino.startsWith('~/')) { dir = join(homedir(), destino.slice(2)); continue }
    dir = resolve(dir, msys(destino))
  }
  return dir
}

// Las opciones globales entre `git` y su subcomando. Un `-C` despues del
// subcomando es otra cosa (en `git commit -C <commit>` es el mensaje a reusar).
const GLOBALES = /^git\s+((?:(?:-[A-Za-z]\s*|--[a-z-]+[= ])(?:"[^"]*"|'[^']*'|[^\s;&|]+)\s+|--[a-z-]+\s+)*)/
const OPCION_C = /(?:^|\s)-C\s*("([^"]*)"|'([^']*)'|(\S+))/

/** La carpeta de un `git` que empieza en `indice`: la de los cd de antes, movida por su `-C`. */
export function carpetaDeGit(texto, indice, porDefecto) {
  const dir = carpetaEn(texto, indice, porDefecto)
  const c = OPCION_C.exec(GLOBALES.exec(String(texto).slice(indice))?.[1] ?? '')
  if (!c) return dir
  const destino = c[2] ?? c[3] ?? c[4]
  if (/[$`]/.test(destino)) return null
  if (isAbsolute(msys(destino))) return resolve(msys(destino))
  return dir === null ? null : resolve(dir, msys(destino))
}
