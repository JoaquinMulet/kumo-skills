#!/usr/bin/env node
/**
 * Prueba el porton de higiene en las 4 situaciones que le importan, y en
 * las 2 direcciones. que bloquee cuando debe y que NO estorbe cuando no.
 *
 * La segunda mitad es la que casi nadie escribe y es la que decide si el
 * guardia se puede vivir con el. Un porton que bloquea de mas se termina
 * apagando, y ahi se pierde entero.
 */
import { execFileSync } from 'node:child_process'
import { mkdtempSync, rmSync, writeFileSync, mkdirSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const HOOK = join(dirname(fileURLToPath(import.meta.url)), 'exigir-higiene.mjs')

function correr(evento, env = {}) {
  const r = execFileSync('node', [HOOK], {
    input: JSON.stringify(evento),
    encoding: 'utf8',
    env: { ...process.env, ...env },
  })
  if (r.trim() === '') return { decision: 'pasa' }
  try {
    const j = JSON.parse(r)
    return { decision: j.hookSpecificOutput?.permissionDecision ?? '?', razon: j.hookSpecificOutput?.permissionDecisionReason ?? '' }
  } catch {
    return { decision: 'salida ilegible', razon: r.slice(0, 120) }
  }
}

function repoNuevo({ conHooks }) {
  const dir = mkdtempSync(join(tmpdir(), 'higiene-'))
  execFileSync('git', ['init', '-q'], { cwd: dir })
  writeFileSync(join(dir, 'algo.txt'), 'hola\n')
  if (conHooks) {
    mkdirSync(join(dir, '.githooks'))
    writeFileSync(join(dir, '.githooks', 'pre-commit'), '#!/bin/sh\nexit 0\n')
    execFileSync('git', ['config', 'core.hooksPath', '.githooks'], { cwd: dir })
  }
  return dir
}

const casos = []
function caso(nombre, esperado, fn) {
  let dir = null
  try {
    const res = fn((d) => { dir = d })
    const ok = res.decision === esperado
    casos.push({ nombre, esperado, obtenido: res.decision, ok, razon: res.razon })
  } finally {
    if (dir) rmSync(dir, { recursive: true, force: true })
  }
}

// 1. Repo SIN higiene, comando de commit. tiene que NEGAR.
caso('repo sin higiene + git commit', 'deny', (reg) => {
  const dir = repoNuevo({ conHooks: false }); reg(dir)
  return correr({ tool_name: 'Bash', cwd: dir, tool_input: { command: 'git commit -m "x"' } })
})

// 2. El mismo repo, con la higiene instalada. tiene que DEJAR PASAR.
caso('repo con higiene + git commit', 'pasa', (reg) => {
  const dir = repoNuevo({ conHooks: true }); reg(dir)
  return correr({ tool_name: 'Bash', cwd: dir, tool_input: { command: 'git commit -m "x"' } })
})

// 3. Repo sin higiene, pero un comando que NO es commit. no debe estorbar.
caso('repo sin higiene + git status', 'pasa', (reg) => {
  const dir = repoNuevo({ conHooks: false }); reg(dir)
  return correr({ tool_name: 'Bash', cwd: dir, tool_input: { command: 'git status --short' } })
})

// 4. El push tambien cuenta, porque publica.
caso('repo sin higiene + git push', 'deny', (reg) => {
  const dir = repoNuevo({ conHooks: false }); reg(dir)
  return correr({ tool_name: 'Bash', cwd: dir, tool_input: { command: 'git push origin main' } })
})

// 5. La salida de emergencia CON razon escrita. pasa.
caso('excusa con razon escrita', 'pasa', (reg) => {
  const dir = repoNuevo({ conHooks: false }); reg(dir)
  writeFileSync(join(dir, '.kumo-sin-higiene'), 'Clon de solo lectura del upstream, no se edita.\n')
  return correr({ tool_name: 'Bash', cwd: dir, tool_input: { command: 'git commit -m "x"' } })
})

// 6. La salida de emergencia VACIA. no pasa, porque la razon es el punto.
caso('excusa vacia', 'deny', (reg) => {
  const dir = repoNuevo({ conHooks: false }); reg(dir)
  writeFileSync(join(dir, '.kumo-sin-higiene'), '   \n')
  return correr({ tool_name: 'Bash', cwd: dir, tool_input: { command: 'git commit -m "x"' } })
})

// 7. La variable de una vez.
caso('KUMO_SIN_HIGIENE=1', 'pasa', (reg) => {
  const dir = repoNuevo({ conHooks: false }); reg(dir)
  return correr({ tool_name: 'Bash', cwd: dir, tool_input: { command: 'git commit -m "x"' } }, { KUMO_SIN_HIGIENE: '1' })
})

// 8. Otra herramienta que no es Bash. ni se mete.
caso('tool que no es Bash', 'pasa', () =>
  correr({ tool_name: 'Read', cwd: process.cwd(), tool_input: { file_path: 'x' } }))

// 9. Fuera de un repo git. no hay higiene que exigir.
caso('carpeta que no es un repo', 'pasa', (reg) => {
  const dir = mkdtempSync(join(tmpdir(), 'norepo-')); reg(dir)
  return correr({ tool_name: 'Bash', cwd: dir, tool_input: { command: 'git commit -m "x"' } })
})

// --- El repo que se juzga es el del COMANDO, no el de la sesion --------
//
// Los 4 casos siguientes vienen de 2 defectos reales del 22 de agosto de
// 2026. El porton bloqueo un commit en un repositorio que SI tenia el
// aparato, porque el directorio de la sesion habia quedado dentro de un
// clon anidado y el comando empezaba con `cd "<el repo bueno>"`. Y al
// escribir estos casos aparecio el hermano mudo. la expresion que decide
// si un comando es un commit no reconocia `git -C <ruta> commit`, asi que
// esa forma nunca disparaba el guardia.
const conAparato = repoNuevo({ conHooks: true })
const sinAparato = repoNuevo({ conHooks: false })
try {
  // 10. La sesion esta en un repo sin aparato y el comando entra a uno que
  //     si lo tiene. Este es el falso positivo que me bloqueo a mi.
  caso('cd hacia el repo equipado', 'pasa', () =>
    correr({ tool_name: 'Bash', cwd: sinAparato, tool_input: { command: `cd '${conAparato}' && git commit -m "x"` } }))

  // 11. Al reves, y es el lado peligroso porque es mudo. la sesion esta en
  //     un repo equipado y el comando commitea en otro que no lo esta.
  caso('cd hacia el repo SIN aparato', 'deny', () =>
    correr({ tool_name: 'Bash', cwd: conAparato, tool_input: { command: `cd '${sinAparato}' && git commit -m "x"` } }))

  // 12. La forma explicita de git para elegir directorio.
  caso('git -C hacia el repo sin aparato', 'deny', () =>
    correr({ tool_name: 'Bash', cwd: conAparato, tool_input: { command: `git -C '${sinAparato}' commit -m "x"` } }))

  // 13. Y la expresion ensanchada no puede meterse donde no la llaman. Si
  //     esto se pone rojo, el guardia empezo a molestar en comandos de
  //     lectura, y un guardia que molesta se apaga.
  caso('git log --grep commit', 'pasa', () =>
    correr({ tool_name: 'Bash', cwd: sinAparato, tool_input: { command: 'git log --grep commit' } }))
} finally {
  rmSync(conAparato, { recursive: true, force: true })
  rmSync(sinAparato, { recursive: true, force: true })
}

let fallos = 0
for (const c of casos) {
  if (!c.ok) fallos++
  process.stdout.write(`  ${c.ok ? 'ok  ' : 'MAL '} ${c.nombre.padEnd(34)} esperaba ${c.esperado}, dio ${c.obtenido}\n`)
}
process.stdout.write(`\n${casos.length - fallos} de ${casos.length} casos correctos.\n`)
if (fallos > 0) {
  process.stdout.write('ROJO. El porton no se comporta como dice su documentacion.\n')
  process.exit(1)
}
process.stdout.write('VERDE. Bloquea cuando debe y no estorba cuando no.\n')
