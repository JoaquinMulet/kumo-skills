import argparse
import functools
import json
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ANCHOS_PX = (375, 768, 1440)
ALTO_VENTANA_PX = 900
PESO_INICIAL_AVISO_BYTES = 3 * 1024 * 1024
PLAZO_CARGA_MS = 60000
PASO_DESPLAZAMIENTO_PX = 600
PAUSA_DESPLAZAMIENTO_MS = 150
ESPERA_TRAS_CARGA_MS = 3000
LCP_MAX_MS = 2500
CLS_MAX = 0.1
CONTRASTE_TEXTO_NORMAL = 4.5
CONTRASTE_TEXTO_GRANDE = 3.0
OBJETIVO_TACTIL_MIN_PX = 24
MAX_CULPABLES = 8
PAGINAS_SECUNDARIAS = {"gracias.html", "error.html", "privacidad.html", "privacy.html"}
RED_LENTA = {"offline": False, "latency": 150, "downloadThroughput": 1.6 * 1024 * 1024 / 8, "uploadThroughput": 750 * 1024 / 8}
CPU_LENTA = 4

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

MEDIR_CONTRASTE = """
([normal, grande, maximo]) => {
  const rgba = (c) => { const m = c.match(/[\\d.]+/g); if (!m) return null; return { r: +m[0], g: +m[1], b: +m[2], a: m.length > 3 ? +m[3] : 1 }; };
  const lineal = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const luz = (c) => 0.2126 * lineal(c.r) + 0.7152 * lineal(c.g) + 0.0722 * lineal(c.b);
  const mezcla = (arriba, abajo) => ({ r: arriba.r * arriba.a + abajo.r * (1 - arriba.a), g: arriba.g * arriba.a + abajo.g * (1 - arriba.a), b: arriba.b * arriba.a + abajo.b * (1 - arriba.a), a: 1 });
  const fondo = (el) => {
    const capas = [];
    for (let p = el; p; p = p.parentElement) {
      const s = getComputedStyle(p);
      if (s.backgroundImage !== 'none') return null;
      const c = rgba(s.backgroundColor);
      if (c && c.a > 0) { capas.push(c); if (c.a >= 1) break; }
    }
    let resultado = { r: 255, g: 255, b: 255, a: 1 };
    for (const capa of capas.reverse()) resultado = mezcla(capa, resultado);
    return resultado;
  };
  const culpables = [];
  let dudosos = 0;
  const vistos = new Set();
  const recorrido = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (recorrido.nextNode()) {
    const texto = recorrido.currentNode.textContent.trim();
    const el = recorrido.currentNode.parentElement;
    if (!texto || !el || vistos.has(el)) continue;
    vistos.add(el);
    const s = getComputedStyle(el);
    const caja = el.getBoundingClientRect();
    if (caja.width === 0 || caja.height === 0 || s.visibility === 'hidden' || +s.opacity === 0) continue;
    el.scrollIntoView({ block: 'center' });
    const centro = el.getBoundingClientRect();
    const debajo = document.elementsFromPoint(centro.left + centro.width / 2, centro.top + centro.height / 2);
    if (debajo.some(d => ['IMG', 'VIDEO', 'PICTURE', 'CANVAS', 'SVG', 'IFRAME'].includes(d.tagName.toUpperCase()))) { dudosos++; continue; }
    const f = fondo(el);
    if (!f) { dudosos++; continue; }
    const c = rgba(s.color);
    if (!c) continue;
    const frente = mezcla(c, f);
    const [a, b] = [luz(frente), luz(f)].sort((x, y) => y - x);
    const razon = (a + 0.05) / (b + 0.05);
    const tam = parseFloat(s.fontSize);
    const esGrande = tam >= 24 || (tam >= 18.66 && (+s.fontWeight || 400) >= 700);
    const minimo = esGrande ? grande : normal;
    if (razon < minimo) {
      culpables.push('"' + texto.slice(0, 40) + '" tiene ' + razon.toFixed(2) + ':1 y necesita ' + minimo + ':1');
      if (culpables.length >= maximo) break;
    }
  }
  return { culpables, dudosos };
}
"""

MEDIR_OBJETIVOS = """
([minimo, maximo]) => {
  const culpables = [];
  const sel = 'a[href], button, input:not([type=hidden]), select, textarea, [role=button]';
  for (const el of document.querySelectorAll(sel)) {
    const s = getComputedStyle(el);
    if (s.display === 'inline' || s.display === 'none' || s.visibility === 'hidden') continue;
    const caja = el.getBoundingClientRect();
    if (caja.width === 0 || caja.height === 0) continue;
    if (caja.width < minimo || caja.height < minimo) {
      const nombre = (el.innerText || el.getAttribute('aria-label') || el.getAttribute('name') || el.tagName).trim().slice(0, 30);
      culpables.push(el.tagName.toLowerCase() + ' "' + nombre + '" mide ' + Math.round(caja.width) + ' por ' + Math.round(caja.height) + 'px');
      if (culpables.length >= maximo) break;
    }
  }
  return culpables;
}
"""

OBSERVAR_VELOCIDAD = """
window.__kumo = { lcp: 0, cls: 0 };
new PerformanceObserver((lista) => { for (const e of lista.getEntries()) window.__kumo.lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true });
new PerformanceObserver((lista) => { for (const e of lista.getEntries()) if (!e.hadRecentInput) window.__kumo.cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
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


class SinNavegador(Exception):
    pass


class ServidorSinRuido(ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        pass


def levantar_servidor(raiz):
    manejador = functools.partial(ServidorCallado, directory=str(raiz))
    servidor = ServidorSinRuido(("127.0.0.1", 0), manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor


def abrir_navegador(p):
    for opciones in ({}, {"channel": "msedge"}, {"channel": "chrome"}):
        try:
            return p.chromium.launch(**opciones)
        except Exception:
            continue
    raise SinNavegador()


def desplazar_hasta_el_fondo(pagina):
    alto = pagina.evaluate("document.documentElement.scrollHeight")
    posicion = 0
    while posicion < alto:
        posicion += PASO_DESPLAZAMIENTO_PX
        pagina.evaluate(f"window.scrollTo(0, {posicion})")
        pagina.wait_for_timeout(PAUSA_DESPLAZAMIENTO_MS)
        alto = pagina.evaluate("document.documentElement.scrollHeight")
    pagina.evaluate("window.scrollTo(0, 0)")


def medir_velocidad_en_telefono(navegador, url):
    contexto = navegador.new_context(viewport={"width": ANCHOS_PX[0], "height": ALTO_VENTANA_PX}, is_mobile=True, has_touch=True)
    pagina = contexto.new_page()
    sesion = contexto.new_cdp_session(pagina)
    sesion.send("Network.enable")
    sesion.send("Network.emulateNetworkConditions", RED_LENTA)
    sesion.send("Emulation.setCPUThrottlingRate", {"rate": CPU_LENTA})
    pagina.add_init_script(OBSERVAR_VELOCIDAD)
    pagina.goto(url, wait_until="load", timeout=PLAZO_CARGA_MS)
    pagina.wait_for_timeout(ESPERA_TRAS_CARGA_MS)
    medida = pagina.evaluate("window.__kumo")
    peso = pagina.evaluate(PESO_CARGADO)
    contexto.close()
    return medida, peso


def revisar(raiz, carpeta_capturas):
    from playwright.sync_api import sync_playwright

    hallazgos = []
    paginas_html = sorted(p.relative_to(raiz).as_posix() for p in raiz.rglob("*.html"))
    servidor = levantar_servidor(raiz)
    base = f"http://127.0.0.1:{servidor.server_address[1]}/"
    carpeta_capturas.mkdir(parents=True, exist_ok=True)
    print(f"Reviso {len(paginas_html)} páginas en {len(ANCHOS_PX)} anchos y mido la velocidad con señal lenta. Puede tardar de 1 a 4 minutos.", file=sys.stderr)

    def anotar(nivel, regla, archivo, detalle):
        hallazgos.append({"nivel": nivel, "regla": regla, "archivo": archivo, "detalle": detalle})

    try:
        with sync_playwright() as p:
            navegador = abrir_navegador(p)
            for relativa in paginas_html:
                principal = Path(relativa).name not in PAGINAS_SECUNDARIAS
                if principal:
                    medida, peso = medir_velocidad_en_telefono(navegador, base + relativa)
                    if medida["lcp"] > LCP_MAX_MS:
                        anotar("FALLA", "P07-velocidad", relativa, f"Con señal lenta de teléfono, el contenido principal aparece a los {medida['lcp'] / 1000:.1f} segundos. Google pide 2,5 segundos o menos.")
                    if medida["cls"] > CLS_MAX:
                        anotar("FALLA", "P07-velocidad", relativa, f"La página se mueve mientras carga, con un CLS de {medida['cls']:.2f}. Google pide 0,1 o menos. Reserva el alto y el ancho de cada imagen y bloque.")
                    if peso > PESO_INICIAL_AVISO_BYTES:
                        anotar("AVISO", "P02-peso-inicial", relativa, f"Al abrir en un teléfono la página baja {peso / 1048576:.1f} MB.")

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
                    pagina.on("pageerror", lambda e, errores_consola=errores_consola: errores_consola.append(str(e)))
                    pagina.on("response", lambda r, fallidos=fallidos: fallidos.append(f"{r.status} {r.url}") if r.status >= 400 else None)
                    pagina.goto(base + relativa, wait_until="load", timeout=PLAZO_CARGA_MS)

                    desplazar_hasta_el_fondo(pagina)
                    medida = pagina.evaluate(MEDIR_DESBORDE)
                    if medida["anchoTotal"] > medida["ancho"] + 1:
                        anotar("FALLA", "P01-desborde", relativa, f"A {ancho}px la página mide {medida['anchoTotal']}px y se mueve hacia el lado. Culpables: " + "; ".join(medida["culpables"] or ["no identificados"]))

                    if ancho == ANCHOS_PX[0]:
                        contraste = pagina.evaluate(MEDIR_CONTRASTE, [CONTRASTE_TEXTO_NORMAL, CONTRASTE_TEXTO_GRANDE, MAX_CULPABLES])
                        for culpable in contraste["culpables"]:
                            anotar("FALLA", "P05-contraste", relativa, f"El texto {culpable}.")
                        if contraste["dudosos"]:
                            anotar("AVISO", "P05-contraste", relativa, f"{contraste['dudosos']} textos van sobre una foto o un degradado. Revisa su contraste a ojo en las capturas.")
                        for culpable in pagina.evaluate(MEDIR_OBJETIVOS, [OBJETIVO_TACTIL_MIN_PX, MAX_CULPABLES]):
                            anotar("FALLA", "P06-objetivo-tactil", relativa, f"El elemento {culpable}. Lo mínimo es {OBJETIVO_TACTIL_MIN_PX} por {OBJETIVO_TACTIL_MIN_PX}px.")

                    for texto in errores_consola:
                        anotar("FALLA", "P03-error-de-programa", relativa, f"A {ancho}px el navegador mostró este error: {texto[:200]}")
                    for texto in sorted(set(fallidos)):
                        anotar("FALLA", "P04-archivo-no-carga", relativa, f"A {ancho}px no cargó: {texto}")

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
        "Mide si la página se sale de la pantalla, el contraste de los textos, el tamaño de los botones, "
        "la velocidad con señal lenta de teléfono, y si hay errores o archivos que no cargan. "
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

    fallas = [h for h in hallazgos if h["nivel"] == "FALLA"]
    if argumentos.json:
        print(json.dumps(hallazgos, ensure_ascii=False, indent=2))
    else:
        for h in sorted(hallazgos, key=lambda h: (h["nivel"] != "FALLA", h["regla"])):
            print(f"{h['nivel']}  {h['regla']}  {h['archivo']}")
            print(f"       {h['detalle']}")
        print()
        print(f"Resultado: {len(fallas)} fallas y {len(hallazgos) - len(fallas)} avisos. Capturas en {capturas}")
        print("La velocidad es una medición de laboratorio. Google aprueba con datos de visitas reales, que Kumo revisa en Search Console después de publicar.")
        print("Mira cada captura antes de entregar. El programa mide, pero no ve si el diseño se ve bien.")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
