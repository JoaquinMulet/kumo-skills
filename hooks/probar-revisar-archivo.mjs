#!/usr/bin/env node
/**
 * Prueba el revisor de archivos con archivos reales en una carpeta
 * temporal, en las 2 direcciones.
 *
 * Uso.  node hooks/probar-revisar-archivo.mjs
 * Sale con 0 si todos los casos dan lo esperado, y con 1 si alguno falla.
 */
import { execFileSync } from 'node:child_process'
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const HOOK = join(dirname(fileURLToPath(import.meta.url)), 'revisar-archivo.mjs')
const BOM = Buffer.from([0xef, 0xbb, 0xbf])
const tmp = mkdtempSync(join(tmpdir(), 'archivo-'))

function correr(nombre, bytes, herramienta = 'Write') {
  const ruta = join(tmp, nombre)
  writeFileSync(ruta, bytes)
  const r = execFileSync('node', [HOOK], {
    input: JSON.stringify({ tool_name: herramienta, tool_input: { file_path: ruta } }),
    encoding: 'utf8',
  })
  if (r.trim() === '') return 'pasa'
  try { return JSON.parse(r).decision === 'block' ? 'devuelve' : '?' } catch { return 'ilegible' }
}

const t = (s) => Buffer.from(s, 'utf8')
const casos = [
  ['settings.json con BOM (10 ago 2026)', 'settings.json', Buffer.concat([BOM, t('{}')]), 'devuelve'],
  ['.env con BOM', '.env', Buffer.concat([BOM, t('A=1')]), 'devuelve'],
  ['settings.json sin BOM', 'settings.json', t('{}'), 'pasa'],
  ['script .sh con CRLF', 'a.sh', t('#!/bin/sh\r\necho hola\r\n'), 'devuelve'],
  ['script .sh con LF', 'a.sh', t('#!/bin/sh\necho hola\n'), 'pasa'],
  ['BOM escondido en un .mjs (29 sep 2026)', 'a.mjs', Buffer.concat([t('const x = /'), BOM, t('/\n')]), 'devuelve'],
  ['.mjs normal con tildes', 'a.mjs', t("const s = 'canción'\n"), 'pasa'],
  ['README.md con BOM no es config', 'README.md', Buffer.concat([BOM, t('# hola')]), 'pasa'],
  ['.txt con CRLF no es shell', 'notas.txt', t('a\r\nb\r\n'), 'pasa'],
]
let malos = 0
for (const [nombre, archivo, bytes, esperado] of casos) {
  const dio = correr(archivo, bytes)
  if (dio !== esperado) malos++
  process.stdout.write(`  ${dio === esperado ? 'ok  ' : 'MAL '} ${nombre.padEnd(42)} esperaba ${esperado}, dio ${dio}\n`)
}
const otra = correr('x.json', Buffer.concat([BOM, t('{}')]), 'Read')
if (otra !== 'pasa') malos++
process.stdout.write(`  ${otra === 'pasa' ? 'ok  ' : 'MAL '} ${'otra herramienta no se revisa'.padEnd(42)} dio ${otra}\n`)
rmSync(tmp, { recursive: true, force: true })
process.stdout.write(`\n${casos.length + 1 - malos} de ${casos.length + 1} casos correctos.\n`)
process.stdout.write(malos ? 'ROJO.\n' : 'VERDE.\n')
process.exit(malos ? 1 : 0)
