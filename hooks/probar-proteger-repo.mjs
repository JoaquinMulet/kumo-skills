#!/usr/bin/env node
/**
 * Prueba el protector del repo en las 2 direcciones, con repos de git
 * reales en una carpeta temporal. Cada regla tiene su caso que debe negar
 * y su vecino que debe pasar, porque un guardia que niega de mas se apaga.
 *
 * Uso.  node hooks/probar-proteger-repo.mjs
 * Sale con 0 si todos los casos dan lo esperado, y con 1 si alguno falla.
 */
import { execFileSync } from 'node:child_process'
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const HOOK = join(dirname(fileURLToPath(import.meta.url)), 'proteger-repo.mjs')
const SALTO = String.fromCharCode(10)
const CRLF = String.fromCharCode(13, 10)

function correr(command, { cwd, fondo = false } = {}) {
  const r = execFileSync('node', [HOOK], {
    input: JSON.stringify({ tool_name: 'Bash', tool_input: { command, run_in_background: fondo }, cwd }),
    env: ENV,
    encoding: 'utf8',
  })
  if (r.trim() === '') return 'pasa'
  try { return JSON.parse(r).hookSpecificOutput.permissionDecision === 'deny' ? 'niega' : '?' } catch { return 'ilegible' }
}

// Dentro de un pre-commit, git exporta GIT_DIR, GIT_INDEX_FILE y otras. Heredarlas haría que los
// repos de prueba apunten al repo real y que `git worktree add` falle.
const ENV = Object.fromEntries(Object.entries(process.env).filter(([k]) => !k.startsWith('GIT_')))
const g = (args, cwd) => execFileSync('git', args, { cwd, env: ENV, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] })
const tmp = mkdtempSync(join(tmpdir(), 'proteger-'))
const solo = join(tmp, 'solo')
const conArboles = join(tmp, 'con-arboles')
for (const d of [solo, conArboles]) {
  execFileSync('git', ['init', '-q', d], { env: ENV })
  g(['config', 'user.email', 'prueba@ejemplo.cl'], d)
  g(['config', 'user.name', 'Prueba'], d)
  g(['config', 'core.autocrlf', 'false'], d)
  writeFileSync(join(d, 'a.txt'), 'hola' + SALTO)
  g(['add', 'a.txt'], d)
  g(['commit', '-q', '-m', 'inicio'], d)
}
g(['worktree', 'add', '-q', join(tmp, 'hermano'), '-b', 'hermano'], conArboles)

// Un .sh sin permiso y otro con CRLF, en el indice de "solo".
writeFileSync(join(solo, 'sin-permiso.sh'), '#!/bin/sh' + SALTO + 'echo hola' + SALTO)
g(['add', 'sin-permiso.sh'], solo)

// La carpeta del árbol sale de TODOS los cd que corren antes del `git worktree add`, no solo del
// primero ni de la carpeta de la sesión. Caso real del 8 nov 2026: la sesión estaba en un clon de
// OneDrive, el comando entraba por una variable a una carpeta temporal, y el gancho negó un árbol que
// iba fuera de OneDrive.
const fuera = join(tmp, 'fuera')
const enOneDrive = join(tmp, 'OneDrive', 'Proyectos', 'clon')
mkdirSync(fuera)
mkdirSync(enOneDrive, { recursive: true })

const ST = 'git diff --cached --stat; '
const casos = [
  ['cd por variable y worktree relativo (8 nov 2026)', `S="${fuera}"; cd "$S" && git init -q r && cd r && git worktree add -q ../wt1 -b r1`, { cwd: enOneDrive }, 'pasa'],
  ['2 cd, el ultimo hacia OneDrive', `cd "${fuera}" && cd "${enOneDrive}" && git worktree add -q ../w -b w`, { cwd: fuera }, 'niega'],
  ['2 cd, el ultimo fuera de OneDrive', `cd "${enOneDrive}" && cd "${fuera}" && git worktree add -q w -b w`, { cwd: enOneDrive }, 'pasa'],
  ['cd relativo hacia OneDrive', `cd "${tmp}" && cd OneDrive/Proyectos && git worktree add -q w -b w`, { cwd: fuera }, 'niega'],
  ['cd en un subshell no cuenta afuera', `(cd "${enOneDrive}") && git worktree add -q w -b w`, { cwd: fuera }, 'pasa'],
  ['ruta absoluta en OneDrive con cd por variable', `cd "$S" && git worktree add -q "${enOneDrive}/w" -b w`, { cwd: fuera }, 'niega'],
  ['pytest | tail sin pipefail', 'uv run pytest tests/ | tail -5', {}, 'niega'],
  ['gh run watch | tail', 'gh run watch 123 --exit-status | tail', {}, 'niega'],
  ['pytest | tail con PIPESTATUS', 'uv run pytest | tail -5; echo ${PIPESTATUS[0]}', {}, 'pasa'],
  ['PIPESTATUS entre comillas cuenta', 'node hooks/probar-x.mjs | tail -2; echo "PRUEBA ${PIPESTATUS[0]}"', {}, 'pasa'],
  ['git log | head no es verificador', 'git log --oneline | head -5', {}, 'pasa'],
  ['& dentro de un comando en segundo plano', 'cd /tmp; npm run build & echo listo', { fondo: true }, 'niega'],
  ['2>&1 en segundo plano no es un &', 'npm run build 2>&1', { fondo: true }, 'pasa'],
  ['&& en segundo plano no es un &', 'npm ci && npm run build', { fondo: true }, 'pasa'],
  ['git stash con arboles hermanos', 'git stash push', { cwd: conArboles }, 'niega'],
  ['git reset --hard con arboles hermanos', 'git reset --hard HEAD', { cwd: conArboles }, 'niega'],
  ['git stash en un repo solo', 'git stash push', { cwd: solo }, 'pasa'],
  ['git stash list solo lee', 'git stash list | wc -l', { cwd: conArboles }, 'pasa'],
  ['git stash pelado escribe', 'git stash; git status', { cwd: conArboles }, 'niega'],
  ['grep que nombra validar-skills.py no es verificador', 'grep -n voseo scripts/validar-skills.py | head -5', {}, 'pasa'],
  ['uv run validar-skills.py | tail', 'uv run --with pyyaml python scripts/validar-skills.py | tail -1', {}, 'niega'],
  ['node probar-x.mjs | tail', 'node hooks/probar-x.mjs | tail -2', {}, 'niega'],
  ['worktree con ruta de MSYS /c/dev', 'git worktree add -q /c/dev/w -b w', { cwd: solo }, 'pasa'],
  ['worktree con -q antes de la ruta en OneDrive', 'git worktree add -q "C:/Users/x/OneDrive/w" master', { cwd: solo }, 'niega'],
  ['worktree con variable no se puede juzgar', 'git worktree add -q "$W" master', { cwd: solo }, 'pasa'],
  ['mensaje de commit que nombra worktree add', ST + "git commit -F - <<'EOF'\n- git worktree add hacia OneDrive.\nEOF", { cwd: conArboles }, 'pasa'],
  ['git checkout -- . via cd al repo con arboles', `cd "${conArboles}"; git checkout -- .`, { cwd: solo }, 'niega'],
  ['worktree dentro de OneDrive', 'git worktree add "C:/Users/x/OneDrive/Desktop/w" -b w', { cwd: solo }, 'niega'],
  ['worktree en C:/dev', 'git worktree add "C:/dev/w" -b w', { cwd: solo }, 'pasa'],
  ['commit sin diff --cached --stat antes', 'git commit -m "x"', { cwd: conArboles }, 'niega'],
  ['commit con el stat despues no sirve', 'git commit -m "x"; git diff --cached --stat', { cwd: conArboles }, 'niega'],
  ['commit con el stat antes', ST + 'git commit -m "x"', { cwd: conArboles }, 'pasa'],
  ['texto "git commit" dentro de comillas', 'echo "luego hago git commit"', { cwd: conArboles }, 'pasa'],
  ['commit con un .sh sin 100755', ST + 'git commit -m "x"', { cwd: solo }, 'niega'],
]

let malos = 0
for (const [nombre, comando, opciones, esperado] of casos) {
  const dio = correr(comando, { cwd: opciones.cwd ?? solo, fondo: opciones.fondo })
  if (dio !== esperado) malos++
  process.stdout.write(`  ${dio === esperado ? 'ok  ' : 'MAL '} ${nombre.padEnd(46)} esperaba ${esperado}, dio ${dio}\n`)
}

// El .sh arreglado con permiso pasa, y con CRLF en el indice vuelve a negar.
g(['update-index', '--chmod=+x', 'sin-permiso.sh'], solo)
const conPermiso = correr(ST + 'git commit -m "x"', { cwd: solo })
writeFileSync(join(solo, 'sin-permiso.sh'), '#!/bin/sh' + CRLF + 'echo hola' + CRLF)
g(['add', 'sin-permiso.sh'], solo)
g(['update-index', '--chmod=+x', 'sin-permiso.sh'], solo)
const conCrlf = correr(ST + 'git commit -m "x"', { cwd: solo })
for (const [nombre, dio, esperado] of [['.sh con 100755 y LF', conPermiso, 'pasa'], ['.sh con 100755 y CRLF', conCrlf, 'niega']]) {
  if (dio !== esperado) malos++
  process.stdout.write(`  ${dio === esperado ? 'ok  ' : 'MAL '} ${nombre.padEnd(46)} esperaba ${esperado}, dio ${dio}\n`)
}

const total = casos.length + 2
try { g(['worktree', 'remove', '--force', join(tmp, 'hermano')], conArboles) } catch {}
rmSync(tmp, { recursive: true, force: true })
process.stdout.write(`\n${total - malos} de ${total} casos correctos.\n`)
process.stdout.write(malos ? 'ROJO.\n' : 'VERDE. Niega cuando debe y no estorba cuando no.\n')
process.exit(malos ? 1 : 0)
