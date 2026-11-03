#!/usr/bin/env node
/**
 * INSTALADOR DE LOS HOOKS DEL REPO.
 *
 * Por que existe, dicho por el dueno el 21 de agosto de 2026. «estas
 * cosas son parte de la skill, si alguien consume el repo la idea es que
 * tambien se apliquen todas estas instrucciones que no van como skill
 * pero son parte de ella».
 *
 * Un repo de skills que solo trae TEXTO deja sus disparadores del lado
 * de quien lo clona, o sea en ninguna parte. Los hooks son la mitad que
 * hace cumplir lo que las skills dicen, y viajan con el repo.
 *
 * Que hace. mezcla los hooks en el settings.json del usuario SIN pisar
 * lo que ya tenga, y con las rutas absolutas de ESTE clon, para que
 * funcione desde donde sea que este.
 *
 * Uso.
 *   node hooks/instalar.mjs            instala
 *   node hooks/instalar.mjs --listar   dice que haria, no escribe
 *   node hooks/instalar.mjs --quitar   los saca
 */
import { existsSync, readFileSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { homedir } from 'node:os'

const AQUI = dirname(fileURLToPath(import.meta.url))
const AJUSTES = join(homedir(), '.claude', 'settings.json')
const SOLO_LISTAR = process.argv.includes('--listar')
const QUITAR = process.argv.includes('--quitar')

/** La marca que permite reconocer NUESTROS hooks entre los del usuario. */
const MARCA = 'kumo-skills/hooks/'

const NUESTROS = [
  {
    evento: 'PreToolUse',
    matcher: 'Bash',
    script: 'exigir-higiene.mjs',
    que: 'niega el commit en un repo sin aparato de higiene',
  },
  {
    evento: 'SessionStart',
    script: 'recordar-estandar.mjs',
    que: 'inyecta el contrato de lectura al abrir la sesion',
  },
  {
    evento: 'Stop',
    script: 'revisar-respuesta.mjs',
    que: 'devuelve la respuesta con &&, huecos, voseo o rayas',
  },
]

function leerAjustes() {
  if (!existsSync(AJUSTES)) return {}
  try {
    return JSON.parse(readFileSync(AJUSTES, 'utf8'))
  } catch (e) {
    process.stdout.write(
      `NO PUEDO SEGUIR. ${AJUSTES} no es JSON valido, y sobrescribirlo te borraria la `
      + `configuracion. Arreglalo a mano primero.\n  ${e.message}\n`)
    process.exit(2)
  }
}

const ajustes = leerAjustes()
ajustes.hooks ??= {}

// Sacar SIEMPRE los nuestros primero. Asi reinstalar no duplica, y
// --quitar es el mismo camino sin el paso de agregar.
// Se quita hook por hook, no la entrada entera. Una entrada puede mezclar un hook nuestro con
// uno ajeno (pasó el 3 nov 2026 con heredoc-barras.py junto a exigir-higiene.mjs), y borrar la
// entrada completa se llevaba el ajeno sin avisar.
const esNuestro = (h) => String(h.command ?? '').includes(MARCA)
let quitados = 0
for (const evento of Object.keys(ajustes.hooks)) {
  for (const entrada of ajustes.hooks[evento]) {
    const antes = (entrada.hooks ?? []).length
    entrada.hooks = (entrada.hooks ?? []).filter((h) => !esNuestro(h))
    quitados += antes - entrada.hooks.length
  }
  ajustes.hooks[evento] = ajustes.hooks[evento].filter((entrada) => entrada.hooks.length > 0)
  if (ajustes.hooks[evento].length === 0) delete ajustes.hooks[evento]
}

if (!QUITAR) {
  for (const n of NUESTROS) {
    const ruta = join(AQUI, n.script).replace(/\\/g, '/')
    if (!existsSync(join(AQUI, n.script))) {
      process.stdout.write(`FALTA el script ${n.script}. No instalo nada.\n`)
      process.exit(2)
    }
    ajustes.hooks[n.evento] ??= []
    const entrada = { hooks: [{ type: 'command', command: `node "${ruta}"`, timeout: 15 }] }
    if (n.matcher) entrada.matcher = n.matcher
    ajustes.hooks[n.evento].push(entrada)
  }
}

process.stdout.write(`${AJUSTES}\n`)
process.stdout.write(`  hooks nuestros que habia y se sacaron: ${quitados}\n`)
if (QUITAR) {
  process.stdout.write('  modo quitar. no se agrega ninguno.\n')
} else {
  for (const n of NUESTROS) {
    process.stdout.write(`  + ${n.evento.padEnd(14)} ${n.script.padEnd(24)} ${n.que}\n`)
  }
}
const otros = Object.entries(ajustes.hooks)
  .flatMap(([e, xs]) => xs.flatMap((x) => (x.hooks ?? []).filter((h) => !esNuestro(h)).map(() => e)))
process.stdout.write(`  hooks de otros que se conservan: ${otros.length}${otros.length ? ' (' + [...new Set(otros)].join(', ') + ')' : ''}\n`)

if (SOLO_LISTAR) {
  process.stdout.write('\nModo listar. no se escribio nada.\n')
  process.exit(0)
}

// Respaldo antes de tocar. La red de seguridad va antes del cambio, no
// despues, porque protege aunque yo me equivoque.
if (existsSync(AJUSTES)) {
  copyFileSync(AJUSTES, AJUSTES + '.antes-de-kumo')
  process.stdout.write(`  respaldo en ${AJUSTES}.antes-de-kumo\n`)
}
mkdirSync(dirname(AJUSTES), { recursive: true })
// Sin BOM a proposito. lo agrega Out-File de PowerShell y rompe al
// siguiente programa que lea el archivo.
writeFileSync(AJUSTES, JSON.stringify(ajustes, null, 2) + '\n', 'utf8')
process.stdout.write('\nLISTO. Los hooks corren desde la proxima sesion.\n')
process.stdout.write('Comprueba el porton con: node hooks/probar-exigir-higiene.mjs\n')
