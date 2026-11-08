#!/usr/bin/env node
/**
 * Prueba la revision del disco con una carpeta de proyectos falsa en una
 * carpeta temporal: que vea lo que sobra, que no marque lo que esta en uso, y
 * que no escriba NADA (ni siquiera el indice de un repo que revisa).
 *
 * Uso.  node hooks/probar-revisar-disco.mjs
 * Sale con 0 si todos los casos dan lo esperado, y con 1 si alguno falla.
 */
import { execFileSync } from 'node:child_process'
import { mkdtempSync, mkdirSync, writeFileSync, rmSync, utimesSync, readdirSync, lstatSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), 'revisar-disco.mjs')
const base = mkdtempSync(join(tmpdir(), 'disco-'))
const raiz = join(base, 'dev')
const DIA = 24 * 60 * 60 * 1000
const hace = (dias) => new Date(Date.now() - dias * DIA)
const envejecer = (ruta, dias) => utimesSync(ruta, hace(dias), hace(dias))

mkdirSync(raiz)
for (const n of ['cmf-commit.log', 'cmf_push.txt', 'sf-deploy.log']) writeFileSync(join(raiz, n), 'x')

mkdirSync(join(raiz, 'vieja'))
writeFileSync(join(raiz, 'vieja', 'a.txt'), 'x')
envejecer(join(raiz, 'vieja', 'a.txt'), 30)
envejecer(join(raiz, 'vieja'), 30)

mkdirSync(join(raiz, 'nueva'))
writeFileSync(join(raiz, 'nueva', 'a.txt'), 'x')

// Un repo quieto con un archivo sin commit y sin remoto: borrarlo pierde trabajo.
const repo = join(raiz, 'repo-viejo')
execFileSync('git', ['init', '-q', repo])
writeFileSync(join(repo, 'sin-commit.txt'), 'x')
envejecer(join(repo, 'sin-commit.txt'), 30)
envejecer(repo, 30)

// Un arbol de trabajo de 5 dias de un repo que vive fuera de la raiz.
const adm = join(base, 'principal', '.git', 'worktrees', 'arbol')
mkdirSync(adm, { recursive: true })
writeFileSync(join(adm, 'gitdir'), join(raiz, 'arbol', '.git'))
envejecer(join(adm, 'gitdir'), 5)
mkdirSync(join(raiz, 'arbol'))
writeFileSync(join(raiz, 'arbol', '.git'), `gitdir: ${adm}\n`)

/** Cada ruta de la carpeta de prueba con su fecha y su tamano, para ver si algo cambio. */
function foto(dir, acc = []) {
  for (const e of readdirSync(dir)) {
    const p = join(dir, e)
    const st = lstatSync(p)
    acc.push(`${p}|${st.mtimeMs}|${st.isFile() ? st.size : 'd'}`)
    if (st.isDirectory()) foto(p, acc)
  }
  return acc.sort().join('\n')
}

const antes = foto(base)
const correr = (...args) => execFileSync('node', [SCRIPT, '--raiz', raiz, ...args],
  { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] })
const r = JSON.parse(correr('--json'))
const texto = correr()
const despues = foto(base)

const quieta = (n) => r.quietas.find((q) => q.nombre === n)
const casos = [
  ['cuenta los 3 archivos sueltos', r.archivosSueltos === 3],
  ['agrupa cmf-commit.log y cmf_push.txt en la familia cmf', r.familias.find((f) => f.familia === 'cmf')?.archivos === 2],
  ['marca la carpeta vieja como quieta', quieta('vieja')?.dias >= 29],
  ['no marca la carpeta nueva', !quieta('nueva')],
  ['dice que el repo quieto tiene un cambio sin commit', quieta('repo-viejo')?.git?.cambios === 1],
  ['dice que el repo quieto no tiene remoto', quieta('repo-viejo')?.git?.remotos === 0],
  ['ve el arbol de trabajo y su edad de 5 dias', r.arboles.find((a) => a.nombre === 'arbol')?.dias === 5],
  ['nombra el repo principal del arbol', r.arboles[0]?.principal?.endsWith('principal')],
  ['el informe de texto dice que solo lee', texto.includes('Este informe solo lee')],
  ['el informe avisa que el arbol ya deberia estar quitado', texto.includes('ya deberia estar quitado')],
  ['no escribio ni cambio ningun archivo', antes === despues],
]

let malos = 0
for (const [nombre, bien] of casos) {
  if (!bien) malos++
  process.stdout.write(`  ${bien ? 'ok  ' : 'MAL '} ${nombre}\n`)
}
rmSync(base, { recursive: true, force: true })
process.stdout.write(`\n${casos.length - malos} de ${casos.length} casos correctos.\n`)
process.stdout.write(malos ? 'ROJO.\n' : 'VERDE.\n')
process.exit(malos ? 1 : 0)
