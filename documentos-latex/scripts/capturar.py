"""Captura cada lámina de una página de gráficos como PNG, con el Edge instalado en Windows.

Uso:
  uv run --with playwright python scripts/capturar.py ruta/graficos.html carpeta/de/salida [linea]

Espera que la página marque window.listo = true cuando terminó de dibujar, y que cada lámina
sea un elemento con la clase «lamina» y un id, que pasa a ser el nombre del archivo.
El argumento opcional [linea] se manda como ?linea=... para que la página elija su estilo.
Usa channel="msedge", así que no descarga navegadores. En Linux o Mac, cambia el canal por
"chrome" o quita la línea para usar el Chromium de Playwright.
Sale con código 1 si la página escribió errores en la consola, y los imprime.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# La página de ejemplo dibuja 7 láminas en unos 10 segundos. 60 segundos dan margen a una máquina
# ocupada sin dejar colgado un error de la página.
ESPERA_MS = 60000

# Un gráfico no se entrega con textos montados (regla del CLAUDE.md global, desde el 14 ago 2026).
# Con el renderer SVG de ECharts cada etiqueta es un <text> del DOM, así que el choque se mide en
# vez de mirarse. Se ignoran los textos invisibles y los cruces de menos de 1,5 px por lado, que
# son el borde de la caja de la letra y no se ven.
CHOQUES_JS = """lamina => {
  const visibles = [...lamina.querySelectorAll('text')].filter(t => {
    const r = t.getBoundingClientRect()
    const s = getComputedStyle(t)
    const opaco = Number(t.getAttribute('fill-opacity') ?? 1) * Number(t.getAttribute('opacity') ?? 1) * Number(s.opacity)
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && opaco > 0.05 && t.textContent.trim()
  }).map(t => ({ texto: t.textContent.trim(), r: t.getBoundingClientRect() }))
  const pares = []
  for (let i = 0; i < visibles.length; i++)
    for (let j = i + 1; j < visibles.length; j++) {
      const a = visibles[i].r, b = visibles[j].r
      const ancho = Math.min(a.right, b.right) - Math.max(a.left, b.left)
      const alto = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top)
      if (ancho > 1.5 && alto > 1.5) pares.push([visibles[i].texto, visibles[j].texto])
    }
  return { pares, medidos: visibles.length }
}"""

if len(sys.argv) < 3:
    print(__doc__, file=sys.stderr)
    sys.exit(2)
PAGINA = Path(sys.argv[1]).resolve()
SAL = Path(sys.argv[2]).resolve()
LINEA = sys.argv[3] if len(sys.argv) > 3 else ""
if not PAGINA.exists():
    print(f"No existe la página {PAGINA}", file=sys.stderr)
    sys.exit(2)
SAL.mkdir(parents=True, exist_ok=True)

print("Abriendo Edge y dibujando las láminas. Tarda de 10 a 30 segundos.", file=sys.stderr)
with sync_playwright() as p:
    nav = p.chromium.launch(channel="msedge")
    # Escala 2 para que el PNG tenga el doble de píxeles y se vea nítido impreso.
    pag = nav.new_page(viewport={"width": 1260, "height": 900}, device_scale_factor=2)
    errores = []
    pag.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.goto(PAGINA.as_uri() + (f"?linea={LINEA}" if LINEA else ""))
    pag.wait_for_function("window.listo === true", timeout=ESPERA_MS)
    pag.wait_for_timeout(500)  # deja terminar las animaciones de entrada
    choques = []
    for ident in pag.eval_on_selector_all(".lamina", "els => els.map(e => e.id)"):
        pag.locator(f"#{ident}").screenshot(path=str(SAL / f"{ident}.png"))
        medida = pag.eval_on_selector(f"#{ident}", CHOQUES_JS)
        # El conteo es la prueba de que se midió algo. 0 textos en una lámina con gráfico
        # significa que el gráfico no usa el renderer SVG y el choque no se pudo medir.
        print(f"Escrita {ident}, {medida['medidos']} textos medidos", file=sys.stderr)
        for a, b in medida["pares"]:
            choques.append(f"{ident}: «{a}» se monta con «{b}»")
    nav.close()
for e in errores:
    print("ERROR EN LA PÁGINA:", e, file=sys.stderr)
for c in choques:
    print("TEXTO SUPERPUESTO:", c, file=sys.stderr)
sys.exit(1 if errores or choques else 0)
