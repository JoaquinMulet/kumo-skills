#!/usr/bin/env node
/**
 * Prueba la funcion que dice en que carpeta corre una parte de un comando de
 * Bash (carpeta-del-comando.mjs), con los casos de borde que un gancho no
 * puede juzgar mal: los que se siguen y los que tienen que dar null.
 *
 * Uso.  node hooks/probar-carpeta-del-comando.mjs
 * Sale con 0 si todos los casos dan lo esperado, y con 1 si alguno falla.
 */
import { resolve, join } from 'node:path'
import { homedir } from 'node:os'
import { carpetaEn, carpetaDeGit } from './carpeta-del-comando.mjs'

const SESION = resolve('/sesion/repo')
const A = resolve('/uno')
const enGit = (comando) => carpetaDeGit(comando, comando.indexOf('git '), SESION)

const casos = [
  ['sin cd es la sesion', enGit('git commit -m x'), SESION],
  ['1 cd al principio', enGit('cd /uno && git commit -m x'), A],
  ['2 cd, manda el ultimo', enGit('cd /uno && cd /dos && git commit -m x'), resolve('/dos')],
  ['cd relativo sobre el anterior', enGit('cd /uno && cd sub/x && git commit'), resolve('/uno/sub/x')],
  ['cd con punto y coma', enGit('cd /uno; git status; git commit'), A],
  ['cd entre comillas dobles con espacios', enGit('cd "/uno/con espacio" && git commit'), resolve('/uno/con espacio')],
  ['cd entre comillas simples', enGit("cd '/uno' && git commit"), A],
  ['ruta de Git Bash /c/dev', enGit('cd /c/dev/x && git commit'), resolve('C:/dev/x')],
  ['cd solo va a la carpeta personal', enGit('cd && git commit'), homedir()],
  ['cd ~/x', enGit('cd ~/x && git commit'), join(homedir(), 'x')],
  ['cd con variable no se sabe', enGit('S=/uno; cd "$S" && git commit'), null],
  ['cd - no se sabe', enGit('cd /uno && cd - && git commit'), null],
  ['cd despues de || no se sabe', enGit('cd /uno || cd /dos; git commit'), null],
  ['cd en un subshell no se sabe', enGit('(cd /uno) && git commit'), null],
  ['cd dentro de un if no se sabe', enGit('if true; then cd /uno; fi; git commit'), null],
  ['"cd x" dentro de un texto no cuenta', enGit('echo "luego hago cd /uno" && git commit'), SESION],
  ['echo cd no es un cd', enGit('echo cd /uno && git commit'), SESION],
  ['un cd DESPUES del git no cuenta', enGit('git commit -m x && cd /uno'), SESION],
  ['git -C absoluto manda', enGit('cd /uno && git -C /dos commit'), resolve('/dos')],
  ['git -C relativo sobre el cd', enGit('cd /uno && git -C sub commit'), resolve('/uno/sub')],
  ['git -C con variable no se sabe', enGit('git -C "$R" commit'), null],
  ['el -C de git commit no es una carpeta', enGit('git commit -C HEAD'), SESION],
  ['la posicion manda en carpetaEn', carpetaEn('cd /uno && x; cd /dos && y', 'cd /uno && x; '.length, SESION), A],
]

let malos = 0
for (const [nombre, dio, esperado] of casos) {
  const bien = dio === esperado
  if (!bien) malos++
  process.stdout.write(`  ${bien ? 'ok  ' : 'MAL '} ${nombre.padEnd(42)} esperaba ${esperado}, dio ${dio}\n`)
}
process.stdout.write(`\n${casos.length - malos} de ${casos.length} casos correctos.\n`)
process.stdout.write(malos ? 'ROJO.\n' : 'VERDE.\n')
process.exit(malos ? 1 : 0)
