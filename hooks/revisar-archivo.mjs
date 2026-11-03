#!/usr/bin/env node
/**
 * REVISOR DEL ARCHIVO ESCRITO. Hook PostToolUse de Write y Edit. Mira los
 * BYTES del archivo que el agente acaba de escribir, porque los 3 defectos
 * que revisa no se ven en el editor.
 *
 * 1. BOM al inicio de un archivo de configuracion (.json, .env, .toml,
 *    .yaml, .ini). El siguiente programa que lo lee lo trata como invalido
 *    (10 ago 2026, un settings.json).
 * 2. CRLF en un script de shell (.sh, .bash). Bash lee el retorno de carro
 *    como parte del comando (regla del 30 oct 2026).
 * 3. Un caracter BOM escondido en medio de un archivo de codigo. El tool
 *    Write convirtio un escape de texto en el caracter real el 29 sep 2026,
 *    y otra vez el 3 nov 2026 con una raya.
 *
 * No puede deshacer la escritura. Le devuelve al agente el defecto y como
 * repararlo por bytes. Un error propio deja pasar.
 */
import { readFileSync, existsSync } from 'node:fs'
import { extname, basename, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const CONFIG = new Set(['.json', '.jsonc', '.toml', '.yaml', '.yml', '.ini', '.cfg', '.env'])
const SHELL = new Set(['.sh', '.bash'])
const CODIGO = new Set(['.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.py', '.sh', '.json', '.toml', '.yaml', '.yml'])

export function revisar(ruta, bytes) {
  const ext = extname(ruta).toLowerCase()
  const nombre = basename(ruta).toLowerCase()
  const esConfig = CONFIG.has(ext) || nombre === '.env' || nombre.startsWith('.env.')
  const defectos = []
  const conBom = bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf
  if (esConfig && conBom) {
    defectos.push(`${ruta} empieza con BOM (EF BB BF). Escríbelo sin BOM, por ejemplo con Python y write_bytes.`)
  }
  if (SHELL.has(ext) && bytes.includes(13)) {
    defectos.push(`${ruta} trae CRLF. Pásalo a LF reemplazando los bytes 13 10 por 10.`)
  }
  if (CODIGO.has(ext)) {
    for (let i = conBom ? 3 : 0; i + 2 < bytes.length; i++) {
      if (bytes[i] === 0xef && bytes[i + 1] === 0xbb && bytes[i + 2] === 0xbf) {
        defectos.push(`${ruta} trae un carácter BOM escondido en el byte ${i}. Arma el texto con String.fromCharCode o chr().`)
        break
      }
    }
  }
  return defectos
}

function main() {
  let evento
  try { evento = JSON.parse(readFileSync(0, 'utf8')) } catch { return }
  if (!['Write', 'Edit', 'MultiEdit'].includes(evento.tool_name)) return
  const ruta = evento.tool_input?.file_path
  if (!ruta || !existsSync(ruta)) return
  let defectos
  try { defectos = revisar(ruta, readFileSync(ruta)) } catch { return }
  if (!defectos.length) return
  process.stdout.write(JSON.stringify({ decision: 'block', reason: '[revisar-archivo] ' + defectos.join(' ') }))
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main()
