import argparse
import functools
import json
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ANCHOS_PX = (375, 768, 1440)
ALTO_VENTANA_PX = 900
PESO_INICIAL_MAX_BYTES = 3 * 1024 * 1024
PLAZO_CARGA_MS = 30000
PASO_DESPLAZAMIENTO_PX = 600
PAUSA_DESPLAZAMIENTO_MS = 150
PAGINAS_DE_RESPUESTA = {"gracias.html", "error.html"}

MEDIR_DESBORDE = """
() => {
  const ancho = document.documentElement.clientWidth;
  const anchoTotal = document.documentElement.scrollWidth;
  const culpables = [];
  for (const el of document.body.querySelectorAll('*')) {
    const caja = el.getBoundingClientRect();
    if (caja.width === 0 || caja.right <= ancho + 1) continue;
    let fijo = false;
    for (let p = el.parentElement; p; p = p.parentElement) {
      const s = getComputedStyle(p);
      if (s.overflowX === 'hidden' || s.overflowX === 'clip' || s.overflowX === 'auto' || s.overflowX === 'scroll') { fijo = true; break; }
    }
    if (fijo) continue;
    const id = el.id ? '#' + el.id : '';
    const clase = (typeof el.className === 'string' && el.className.trim()) ? '.' + el.className.trim().split(/ +/).join('.') : '';
    culpables.push(el.tagName.toLowerCase() + id + clase + ' llega a ' + Math.round(caja.right) + 'px');
    if (culpables.length >= 5) break;
  }
  return { ancho, anchoTotal, culpables };
}
"""

PESO_CARGADO = """
() => {
  const nav = performance.getEntriesByType('navigation')[0];
  const recursos = performance.getEntriesByType('resource');
  const suma = recursos.reduce((t, r) => t + (r.encodedBodySize || r.transferSize || 0), 0);
  return suma + (nav ? (nav.encodedBodySize || 0) : 0);
}
"""


class ServidorCallado(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def levantar_servidor(raiz):
    manejador = functools.partial(ServidorCallado, directory=str(raiz))
    servidor = ThreadingHTTPServer(("127.0.0.1", 0), manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor


def desplazar_hasta_el_fondo(pagina):
    alto = pagina.evaluate("document.documentElement.scrollHeight")
    posicion = 0
    while posicion < alto:
        posicion += PASO_DESPLAZAMIENTO_PX
        pagina.evaluate(f"window.scrollTo(0, {posicion})")
        pagina.wait_for_timeout(PAUSA_DESPLAZAMIENTO_MS)
        alto = pagina.evaluate("document.documentElement.scrollHeight")
    pagina.evaluate("window.scrollTo(0, 0)")


class SinNavegador(Exception):
    pass


def abrir_navegador(p):
    intentos = [{}, {"channel": "msedge"}, {"channel": "chrome"}]
    for opciones in intentos:
        try:
            return p.chromium.launch(**opciones)
        except Exception:
            continue
    raise SinNavegador()


def revisar(raiz, carpeta_capturas):
    from playwright.sync_api import sync_playwright

    hallazgos = []
    paginas_html = sorted(p.relative_to(raiz).as_posix() for p in raiz.rglob("*.html"))
    servidor = levantar_servidor(raiz)
    base = f"http://127.0.0.1:{servidor.server_address[1]}/"
    carpeta_capturas.mkdir(parents=True, exist_ok=True)
    print(f"Reviso {len(paginas_html)} páginas en {len(ANCHOS_PX)} anchos. Puede tardar 1 o 2 minutos.", file=sys.stderr)

    try:
        with sync_playwright() as p:
            navegador = abrir_navegador(p)
            for relativa in paginas_html:
                for ancho in ANCHOS_PX:
                    contexto = navegador.new_context(viewport={"width": ancho, "height": ALTO_VENTANA_PX})
                    pagina = contexto.new_page()
                    errores_consola, fallidos = [], []
                    def anotar_consola(m, errores_consola=errores_consola, fallidos=fallidos):
                        if m.type != "error":
                            return
                        if m.text.startswith("Failed to load resource"):
                            fallidos.append(m.text.split("status of ")[-1].split(" ")[0] + " " + (m.location or {}).get("url", "dirección desconocida"))
                        else:
                            errores_consola.append(m.text)

                    pagina.on("console", anotar_consola)
                    pagina.on("pageerror", lambda e: errores_consola.append(str(e)))
                    pagina.on("response", lambda r: fallidos.append(f"{r.status} {r.url}") if r.status >= 400 else None)
                    pagina.goto(base + relativa, wait_until="load", timeout=PLAZO_CARGA_MS)

                    if ancho == ANCHOS_PX[0] and relativa not in PAGINAS_DE_RESPUESTA:
                        peso = pagina.evaluate(PESO_CARGADO)
                        if peso > PESO_INICIAL_MAX_BYTES:
                            hallazgos.append({"nivel": "FALLA", "regla": "P02-peso-inicial", "archivo": relativa, "detalle": f"Al abrir en un teléfono la página baja {peso / 1048576:.1f} MB. El máximo es 3 MB."})

                    desplazar_hasta_el_fondo(pagina)
                    medida = pagina.evaluate(MEDIR_DESBORDE)
                    if medida["anchoTotal"] > medida["ancho"] + 1:
                        hallazgos.append({"nivel": "FALLA", "regla": "P01-desborde", "archivo": relativa, "detalle": f"A {ancho}px la página mide {medida['anchoTotal']}px y se mueve hacia el lado. Culpables: " + "; ".join(medida["culpables"] or ["no identificados"])})

                    for texto in errores_consola:
                        hallazgos.append({"nivel": "FALLA", "regla": "P03-error-de-programa", "archivo": relativa, "detalle": f"A {ancho}px el navegador mostró este error: {texto[:200]}"})
                    for texto in sorted(set(fallidos)):
                        hallazgos.append({"nivel": "FALLA", "regla": "P04-archivo-no-carga", "archivo": relativa, "detalle": f"A {ancho}px no cargó: {texto}"})

                    nombre_captura = relativa.replace("/", "_").replace(".html", "") + f"-{ancho}.png"
                    pagina.screenshot(path=str(carpeta_capturas / nombre_captura), full_page=True)
                    contexto.close()
            navegador.close()
    finally:
        servidor.shutdown()
    return hallazgos


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    lector = argparse.ArgumentParser(
        description="Abre cada página del sitio en un navegador de verdad, en 375, 768 y 1440 píxeles de ancho. "
        "Mide si la página se sale de la pantalla, cuánto pesa al abrir en un teléfono, y si hay errores o archivos que no cargan. "
        "Guarda una captura completa de cada página en cada ancho. Sale con 0 si no hay fallas y con 1 si hay fallas.",
    )
    lector.add_argument("carpeta", help="Carpeta del sitio, la que tiene index.html")
    lector.add_argument("--capturas", default="capturas-revision", help="Carpeta donde quedan las capturas. Queda fuera de la entrega.")
    lector.add_argument("--json", action="store_true", help="Entrega los hallazgos en JSON")
    argumentos = lector.parse_args()

    raiz = Path(argumentos.carpeta).resolve()
    if not (raiz / "index.html").exists():
        print(f"No encuentro index.html en {raiz}.", file=sys.stderr)
        return 2
    capturas = Path(argumentos.capturas).resolve()
    if raiz in capturas.parents or capturas == raiz:
        print("La carpeta de capturas no puede quedar dentro del sitio, porque se publicaría.", file=sys.stderr)
        return 2

    try:
        hallazgos = revisar(raiz, capturas)
    except (ImportError, SinNavegador):
        print("No encuentro un navegador para la revisión. Corre una vez: uv run --with playwright python -m playwright install chromium", file=sys.stderr)
        return 2

    if argumentos.json:
        print(json.dumps(hallazgos, ensure_ascii=False, indent=2))
    else:
        for h in hallazgos:
            print(f"{h['nivel']}  {h['regla']}  {h['archivo']}")
            print(f"       {h['detalle']}")
        print()
        print(f"Resultado: {len(hallazgos)} fallas. Capturas en {capturas}")
        print("Mira cada captura antes de entregar. El programa mide, pero no ve si el diseño se ve bien.")
    return 1 if hallazgos else 0


if __name__ == "__main__":
    sys.exit(main())
