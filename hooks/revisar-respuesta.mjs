#!/usr/bin/env node
/**
 * REVISOR DE LA RESPUESTA. Hook Stop. Lee el ultimo texto que el agente
 * le escribio al usuario y lo devuelve si trae un defecto que el usuario
 * ya corrigio varias veces.
 *
 * Por que existe, decidido por el dueno el 3 de noviembre de 2026. Las
 * reglas de su CLAUDE.md global sobre los comandos que le entregamos
 * nacieron de errores repetidos desde agosto de 2026, y como texto se
 * siguieron repitiendo. Un hook las hace cumplir sin depender de la
 * memoria del agente.
 *
 * Que revisa en cada bloque de codigo de shell (bash, sh, powershell, ps1).
 *   - `&&`, que en Windows PowerShell 5.1 es un ParserError (4 ago 2026).
 *   - Un hueco como `<id>` o `TU_CLAVE`. El boton de ejecutar lo manda
 *     tal cual, y `<` es un operador reservado (21 ago 2026).
 *   - Read-Host o Get-Credential. Un comando que pide pegar un secreto
 *     termina con el secreto en el chat (4 y 5 sep 2026).
 *   - Out-File -Encoding utf8, que en PS 5.1 antepone BOM (10 ago 2026).
 *   - Un bloque que es solo una URL o un chrome://, que no se ejecuta en
 *     la terminal (17 ago 2026).
 * Y en la prosa, fuera del codigo.
 *   - Voseo.
 *   - La raya o el guion largo como separador.
 *
 * Lo que NO revisa, porque necesita juicio. Los dos puntos (a veces
 * presentan una lista legitima), las rutas relativas y el tono.
 *
 * Como responde. Sin defectos, no escribe nada y deja terminar. Con
 * defectos, devuelve {"decision":"block","reason":...} y el agente tiene
 * que reescribir. Si ya hubo un bloqueo en este turno (stop_hook_active),
 * deja pasar, para no entrar en un bucle. Un error propio deja pasar
 * (falla abierto), porque un hook roto traba todas las sesiones.
 */
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const LENGUAJES_SHELL = /^(bash|sh|shell|zsh|powershell|ps1|ps|pwsh|console|cmd|bat)$/i
// Bordes Unicode. Con el \b de JS, una palabra que termina en tilde («revisá») nunca calza.
// Sin «escribí», «elegí» ni «salí», que también son el pretérito normal («escribí el archivo»).
// Medido el 3 nov 2026 sobre 2.095 respuestas reales, eran 75 falsos positivos.
const VOSEO = /(?<!\p{L})(revisá|avisá|poné|andá|tenés|querés|quitá|guardá|mirá|hacé|podés|entendés|usá|corré|vení|sabés|dejá|mandá|probá|decime|fijate|acordate|quedate|llevate|ponete|hacete)(?!\p{L})/iu
const RAYA = new RegExp('[' + String.fromCharCode(0x2014, 0x2013) + ']') // raya y guion largo

function ultimoTexto(evento) {
  if (typeof evento.last_assistant_message === 'string') return evento.last_assistant_message
  if (!evento.transcript_path) return ''
  const lineas = readFileSync(evento.transcript_path, 'utf8').split('\n')
  for (let i = lineas.length - 1; i >= 0; i--) {
    if (!lineas[i].trim()) continue
    let d
    try { d = JSON.parse(lineas[i]) } catch { continue }
    if (d.type !== 'assistant') continue
    const c = d.message?.content
    if (!Array.isArray(c)) continue
    const textos = c.filter((b) => b.type === 'text').map((b) => b.text)
    if (textos.length) return textos.join('\n')
  }
  return ''
}

/** Separa el texto en bloques de codigo (con su lenguaje) y prosa sin codigo. */
function partir(texto) {
  const bloques = []
  const prosa = texto.replace(/```([^\n`]*)\n([\s\S]*?)```/g, (_, leng, cuerpo) => {
    bloques.push({ leng: leng.trim(), cuerpo })
    return ' '
  })
  return { bloques, prosa: prosa.replace(/`[^`\n]*`/g, ' ') }
}

export function revisar(texto) {
  const defectos = []
  const { bloques, prosa } = partir(texto)
  for (const b of bloques) {
    if (!LENGUAJES_SHELL.test(b.leng)) continue
    const c = b.cuerpo
    if (/&&/.test(c)) defectos.push('Un bloque de shell trae `&&`. En PowerShell 5.1 es ParserError. Usa `;`.')
    if (/(^|[^<])<[A-Za-záéíóúñ_][A-Za-z0-9áéíóúñ_ -]{0,30}>/.test(c) || /\bTU_[A-Z_]+\b/.test(c)) {
      defectos.push('Un bloque de shell trae un hueco como `<id>` o `TU_CLAVE`. Resuelve el valor, o cambia el comando por uno que lo averigue solo.')
    }
    if (/\b(Read-Host|Get-Credential)\b/i.test(c)) {
      defectos.push('Un bloque pide escribir o pegar un valor (Read-Host o Get-Credential). Si es un secreto, el comando lo lee del archivo o del portapapeles.')
    }
    if (/Out-File\b[^\n]*-Encoding\s+utf8\b/i.test(c)) {
      defectos.push('Out-File -Encoding utf8 antepone BOM en PS 5.1. Usa [IO.File]::WriteAllText con UTF8Encoding $false.')
    }
    const solo = c.trim()
    if (/^(https?:\/\/|chrome:\/\/|edge:\/\/|about:)\S*$/.test(solo)) {
      defectos.push('Un bloque de shell trae solo una direccion. Eso no se ejecuta en la terminal. Va en texto, diciendo donde se escribe.')
    }
  }
  const v = prosa.match(VOSEO)
  if (v) defectos.push(`La respuesta trae voseo («${v[0]}»). Usa «tú».`)
  // Una celda de tabla con raya suele ser el símbolo de «no aplica».
  const sinTablas = prosa.split('\n').filter((l) => !l.trimStart().startsWith('|')).join('\n')
  if (RAYA.test(sinTablas)) defectos.push('La respuesta trae raya o guion largo fuera del codigo. Usa punto seguido o una coma.')
  return defectos
}

function main() {
  let evento
  try { evento = JSON.parse(readFileSync(0, 'utf8') || '{}') } catch { return }
  if (evento.stop_hook_active) return
  let texto
  try { texto = ultimoTexto(evento) } catch { return }
  // Un error de la API se guarda como texto del asistente, pero no lo escribió el agente.
  if (!texto || texto.startsWith('API Error')) return
  const defectos = revisar(texto)
  if (!defectos.length) return
  process.stdout.write(JSON.stringify({
    decision: 'block',
    reason: '[revisar-respuesta] Antes de entregar, corrige y vuelve a escribir la respuesta completa:\n- '
      + defectos.join('\n- '),
  }))
}

// Corre solo si se lanza como programa. La prueba lo importa para llamar a revisar().
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main()
