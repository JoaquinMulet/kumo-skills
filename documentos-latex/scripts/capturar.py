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
    for ident in pag.eval_on_selector_all(".lamina", "els => els.map(e => e.id)"):
        pag.locator(f"#{ident}").screenshot(path=str(SAL / f"{ident}.png"))
        print("Escrita", ident, file=sys.stderr)
    nav.close()
for e in errores:
    print("ERROR EN LA PÁGINA:", e, file=sys.stderr)
sys.exit(1 if errores else 0)
