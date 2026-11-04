#!/usr/bin/env node
/**
 * Prueba el post-commit que copia las skills del repo a la instalación, con un
 * repo de git real y una carpeta de instalación falsa (KUMO_SKILLS_DESTINO).
 * Cada caso nace de un defecto real del 4 nov 2026. No copiaba las
 * plantillas/, sí copiaba _deprecated/, y no borraba lo borrado.
 *
 * Uso.  node hooks/probar-post-commit.mjs
 * Sale con 0 si todos los casos dan lo esperado, y con 1 si alguno falla.
 */
import { execFileSync } from 'node:child_process'
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, existsSync, rmSync, copyFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const HOOK = join(dirname(fileURLToPath(import.meta.url)), '..', '.githooks', 'post-commit')
const tmp = mkdtempSync(join(tmpdir(), 'postcommit-'))
const repo = join(tmp, 'repo')
const dest = join(tmp, 'instalada')
mkdirSync(join(repo, '.githooks'), { recursive: true })
mkdirSync(dest)
copyFileSync(HOOK, join(repo, '.githooks', 'post-commit'))

// Dentro del pre-commit del repo real git exporta GIT_DIR y otras, y harían que el repo de prueba
// apunte al real.
// HOME y USERPROFILE falsos, para que ni este hook ni una versión vieja que no conozca
// KUMO_SKILLS_DESTINO escriban en el ~/.claude/skills real (pasó cerca el 4 nov 2026).
const HOME_FALSO = join(tmp, 'home')
mkdirSync(HOME_FALSO)
const ENV = {
  ...Object.fromEntries(Object.entries(process.env).filter(([k]) => !k.startsWith('GIT_'))),
  KUMO_SKILLS_DESTINO: dest, HOME: HOME_FALSO, USERPROFILE: HOME_FALSO,
}
const g = (...args) => execFileSync('git', args, { cwd: repo, env: ENV, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] })
const escribir = (rel, texto) => { mkdirSync(dirname(join(repo, rel)), { recursive: true }); writeFileSync(join(repo, rel), texto) }
const commit = (msg) => { g('add', '-A'); g('commit', '-q', '-m', msg) }
const hay = (rel) => existsSync(join(dest, rel))
const lee = (rel) => readFileSync(join(dest, rel), 'utf8')

g('init', '-q')
g('config', 'user.email', 'prueba@ejemplo.cl')
g('config', 'user.name', 'Prueba')
g('config', 'core.autocrlf', 'false')
g('config', 'core.hooksPath', '.githooks')

escribir('mi-skill/SKILL.md', 'uno\n')
escribir('mi-skill/plantillas/estilo.tex', 'v1\n')
escribir('mi-skill/LICENSE', 'MIT\n')
escribir('_deprecated/vieja/SKILL.md', 'retirada\n')
escribir('README.md', 'raiz\n')
escribir('scripts/del-repo.py', 'raiz\n')
commit('inicio')

const casos = []
const caso = (nombre, ok) => casos.push([nombre, ok])
caso('copia SKILL.md', hay('mi-skill/SKILL.md'))
caso('copia plantillas/ (antes no)', hay('mi-skill/plantillas/estilo.tex'))
caso('copia LICENSE (antes no)', hay('mi-skill/LICENSE'))
caso('no copia _deprecated/ (antes sí)', !hay('_deprecated/vieja/SKILL.md'))
caso('no copia archivos de la raíz', !hay('README.md') && !hay('scripts/del-repo.py'))

escribir('mi-skill/plantillas/estilo.tex', 'v2\n')
commit('cambio')
caso('actualiza un archivo cambiado', hay('mi-skill/plantillas/estilo.tex') && lee('mi-skill/plantillas/estilo.tex') === 'v2\n')

mkdirSync(join(dest, 'mi-skill'), { recursive: true })
writeFileSync(join(dest, 'mi-skill/SKILL.md'), 'edición local\n')
escribir('mi-skill/SKILL.md', 'dos\n')
commit('choca')
caso('no pisa una edición local no portada', lee('mi-skill/SKILL.md') === 'edición local\n')

g('rm', '-q', 'mi-skill/LICENSE')
g('commit', '-q', '-m', 'borra')
caso('borra en la instalada lo borrado en el repo', !hay('mi-skill/LICENSE'))

let malos = 0
for (const [nombre, ok] of casos) {
  if (!ok) malos++
  process.stdout.write(`  ${ok ? 'ok  ' : 'MAL '} ${nombre}\n`)
}
rmSync(tmp, { recursive: true, force: true })
process.stdout.write(`\n${casos.length - malos} de ${casos.length} casos correctos.\n`)
process.stdout.write(malos ? 'ROJO.\n' : 'VERDE.\n')
process.exit(malos ? 1 : 0)
