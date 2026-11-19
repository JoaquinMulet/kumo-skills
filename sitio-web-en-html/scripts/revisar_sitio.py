import argparse
import json
import re
import struct
import sys
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

KB = 1024
MB = 1024 * KB

FOTO_MAX_BYTES = 200 * KB
FOTO_OG_MAX_BYTES = 600 * KB
FOTO_MAX_ANCHO_PX = 1600
VIDEO_AUTOMATICO_MAX_BYTES = int(1.5 * MB)
ARCHIVO_MAX_BYTES = 25 * MB
ANCHO_TELEFONO_PX = 375
TEXTO_MINIMO_CARACTERES = 200

EXTENSIONES_FOTO = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif"}
EXTENSIONES_VIDEO = {".mp4", ".webm", ".mov"}
EXTENSIONES_FUENTE_LENTA = {".ttf", ".otf", ".woff"}
EXTENSIONES_TEXTO_REVISABLE = {".html", ".htm", ".css", ".js", ".json", ".txt", ".xml"}
ARCHIVOS_DE_KUMO = {"robots.txt", "sitemap.xml", "llms.txt", "huella.json", "amplify.yml", "customHttp.yml"}
PAGINAS_DE_RESPUESTA = {"gracias.html", "error.html"}
PAGINAS_DE_PRIVACIDAD = {"privacidad.html", "privacy.html"}
IFRAMES_PERMITIDOS = ("www.google.com/maps", "maps.google.com", "www.youtube-nocookie.com", "www.youtube.com/embed", "player.vimeo.com")
PREFIJOS_WHATSAPP = ("https://wa.me/", "https://api.whatsapp.com/")
CAMPOS_SIN_ETIQUETA = {"submit", "button", "reset", "image", "hidden"}
ID_SELLO_HUELLA = "kumo-huella"
NOMBRE_VALIDO = re.compile(r"^_?[a-z0-9]+(?:[._-][a-z0-9]+)*$")
PALABRAS_QUE_DELATAN = re.compile(r"(?:^|[-_.])(simulad[a-z]*|borrador|draft|prueba|test|copia|old|viejo|temp|tmp|maqueta|mockup|prompt|final)(?=$|[-_.0-9])", re.I)
PATRONES_SECRETO = [
    re.compile(r"sk_(?:live|test)_[0-9A-Za-z]{10,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)tbk-api-key"),
    re.compile(r"(?i)(?:api[_-]?key|secret|token|password|clave)[\"']?\s*[:=]\s*[\"'][^\"'\s]{12,}[\"']"),
]
ESTILO_GRILLA = re.compile(r"grid-template-columns", re.I)
ESTILO_ANCHO = re.compile(r"(?<![-a-z])(?:min-)?width\s*:\s*(\d+(?:\.\d+)?)px", re.I)
URL_EN_CSS = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", re.I)
ETIQUETAS_VACIAS = {"meta", "link", "img", "input", "source", "br", "hr", "base", "wbr", "area", "track", "embed", "col", "param"}


@dataclass
class Hallazgo:
    nivel: str
    regla: str
    archivo: str
    detalle: str


@dataclass
class Pagina:
    ruta: Path
    lang: str = ""
    charset: bool = False
    viewport: bool = False
    titulo: str = ""
    h1: int = 0
    texto_visible: int = 0
    metas: dict = field(default_factory=dict)
    links: list = field(default_factory=list)
    imagenes: list = field(default_factory=list)
    videos: list = field(default_factory=list)
    scripts: list = field(default_factory=list)
    formularios: list = field(default_factory=list)
    anclas: list = field(default_factory=list)
    botones: list = field(default_factory=list)
    iframes: list = field(default_factory=list)
    estilos_en_linea: list = field(default_factory=list)
    referencias: list = field(default_factory=list)
    ids: set = field(default_factory=set)
    etiquetas_para: set = field(default_factory=set)


class LectorHtml(HTMLParser):
    def __init__(self, pagina):
        super().__init__(convert_charrefs=True)
        self.p = pagina
        self.pila = []
        self.ancla_abierta = None
        self.boton_abierto = None
        self.video_abierto = None
        self.formulario_abierto = None
        self.etiquetas_abiertas = 0
        self.en_body = False

    def handle_starttag(self, tag, attrs_lista):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs_lista}
        if tag not in ETIQUETAS_VACIAS:
            self.pila.append(tag)
        if a.get("id"):
            self.p.ids.add(a["id"])
        if tag == "body":
            self.en_body = True
        if "style" in a:
            self.p.estilos_en_linea.append(a["style"])
            self.p.referencias.extend(URL_EN_CSS.findall(a["style"]))
        if tag == "html":
            self.p.lang = a.get("lang", "").strip()
        elif tag == "meta":
            if "charset" in a:
                self.p.charset = True
            nombre = (a.get("name") or a.get("property") or "").lower()
            if nombre == "viewport":
                self.p.viewport = True
            if nombre:
                self.p.metas[nombre] = a.get("content", "").strip()
        elif tag == "link":
            self.p.links.append(a)
            if a.get("href"):
                self.p.referencias.append(a["href"])
        elif tag == "h1":
            self.p.h1 += 1
        elif tag == "img":
            self.p.imagenes.append(a)
            self.p.referencias.append(a.get("src", ""))
            self.p.referencias.extend(partes_srcset(a.get("srcset", "")))
            for abierto in (self.ancla_abierta, self.boton_abierto):
                if abierto is not None:
                    abierto["texto"] += a.get("alt", "")
        elif tag == "source":
            if a.get("src"):
                self.p.referencias.append(a["src"])
                if self.video_abierto is not None:
                    self.video_abierto["fuentes"].append(a["src"])
            self.p.referencias.extend(partes_srcset(a.get("srcset", "")))
        elif tag == "video":
            self.video_abierto = {"attrs": a, "fuentes": [a["src"]] if a.get("src") else []}
            self.p.videos.append(self.video_abierto)
            for clave in ("src", "poster"):
                if a.get(clave):
                    self.p.referencias.append(a[clave])
        elif tag == "script":
            self.p.scripts.append(a)
            if a.get("src"):
                self.p.referencias.append(a["src"])
        elif tag == "form":
            self.formulario_abierto = {"attrs": a, "campos": []}
            self.p.formularios.append(self.formulario_abierto)
        elif tag == "label":
            self.etiquetas_abiertas += 1
            if a.get("for"):
                self.p.etiquetas_para.add(a["for"])
        elif tag == "a":
            self.ancla_abierta = {"attrs": a, "texto": ""}
            self.p.anclas.append(self.ancla_abierta)
            self.p.referencias.append(a.get("href", ""))
        elif tag == "button":
            self.boton_abierto = {"attrs": a, "texto": ""}
            self.p.botones.append(self.boton_abierto)
        elif tag == "iframe":
            self.p.iframes.append(a)
        if tag in {"input", "textarea", "select"} and self.formulario_abierto is not None:
            self.formulario_abierto["campos"].append({"tag": tag, "attrs": a, "dentro_de_etiqueta": self.etiquetas_abiertas > 0})

    def handle_endtag(self, tag):
        if tag in self.pila:
            while self.pila and self.pila.pop() != tag:
                pass
        if tag == "a":
            self.ancla_abierta = None
        elif tag == "button":
            self.boton_abierto = None
        elif tag == "video":
            self.video_abierto = None
        elif tag == "form":
            self.formulario_abierto = None
        elif tag == "label":
            self.etiquetas_abiertas = max(0, self.etiquetas_abiertas - 1)

    def handle_data(self, datos):
        actual = self.pila[-1] if self.pila else ""
        if actual == "title":
            self.p.titulo += datos.strip()
        elif actual == "style":
            self.p.referencias.extend(URL_EN_CSS.findall(datos))
        elif actual == "script":
            return
        elif self.en_body:
            self.p.texto_visible += len(datos.strip())
        for abierto in (self.ancla_abierta, self.boton_abierto):
            if abierto is not None:
                abierto["texto"] += datos


def partes_srcset(valor):
    return [trozo.strip().split(" ")[0] for trozo in valor.split(",") if trozo.strip()]


def es_externa(url):
    return url.startswith(("http://", "https://", "//"))


def es_no_archivo(url):
    return url == "" or url.startswith(("#", "mailto:", "tel:", "data:", "javascript:", "sms:"))


def resolver(raiz, archivo_base, url):
    if es_no_archivo(url) or es_externa(url):
        return None
    camino = unquote(urlparse(url).path)
    if not camino:
        return None
    destino = (raiz / camino.lstrip("/")) if camino.startswith("/") else (archivo_base.parent / camino)
    if camino.endswith("/"):
        destino = destino / "index.html"
    return destino.resolve()


def medidas_imagen(ruta):
    try:
        datos = ruta.read_bytes()[: 256 * KB]
    except OSError:
        return None
    if datos[:8] == b"\x89PNG\r\n\x1a\n" and len(datos) >= 24:
        return struct.unpack(">II", datos[16:24])
    if datos[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", datos[6:10])
    if datos[:4] == b"RIFF" and datos[8:12] == b"WEBP":
        tipo = datos[12:16]
        if tipo == b"VP8 ":
            ancho, alto = struct.unpack("<HH", datos[26:30])
            return ancho & 0x3FFF, alto & 0x3FFF
        if tipo == b"VP8L":
            b = datos[21:25]
            ancho = 1 + (((b[1] & 0x3F) << 8) | b[0])
            alto = 1 + (((b[3] & 0x0F) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
            return ancho, alto
        if tipo == b"VP8X":
            ancho = 1 + int.from_bytes(datos[24:27], "little")
            alto = 1 + int.from_bytes(datos[27:30], "little")
            return ancho, alto
    if datos[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(datos):
            if datos[i] != 0xFF:
                i += 1
                continue
            marca = datos[i + 1]
            if marca in (0xD8, 0x01) or 0xD0 <= marca <= 0xD7:
                i += 2
                continue
            largo = struct.unpack(">H", datos[i + 2 : i + 4])[0]
            if 0xC0 <= marca <= 0xCF and marca not in (0xC4, 0xC8, 0xCC):
                alto, ancho = struct.unpack(">HH", datos[i + 5 : i + 9])
                return ancho, alto
            i += 2 + largo
    return None


def nombre_pagina(pagina, raiz):
    return pagina.ruta.relative_to(raiz).as_posix()


def es_pagina_de_respuesta(pagina):
    return pagina.ruta.name in PAGINAS_DE_RESPUESTA


def es_pagina_de_privacidad(pagina):
    return pagina.ruta.name in PAGINAS_DE_PRIVACIDAD


def revisar_pagina(pagina, raiz, hallazgos):
    nombre = nombre_pagina(pagina, raiz)

    def falla(regla, detalle):
        hallazgos.append(Hallazgo("FALLA", regla, nombre, detalle))

    def aviso(regla, detalle):
        hallazgos.append(Hallazgo("AVISO", regla, nombre, detalle))

    if not pagina.lang:
        falla("R01-idioma", "La etiqueta <html> no trae lang, por ejemplo lang=\"es\".")
    if not pagina.charset or not pagina.viewport:
        falla("R02-cabeza-basica", "Faltan <meta charset=\"UTF-8\"> o <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">.")
    if not pagina.titulo:
        falla("R03-titulo-y-descripcion", "La página no tiene <title> con texto.")
    respuesta = es_pagina_de_respuesta(pagina)
    secundaria = respuesta or es_pagina_de_privacidad(pagina)
    if respuesta and "noindex" not in pagina.metas.get("robots", "").lower():
        falla("R32-no-indexar", "Esta página no va en Google. Agrega <meta name=\"robots\" content=\"noindex\">.")
    if pagina.ruta.name == "error.html" and not any(a["attrs"].get("href", "").startswith(PREFIJOS_WHATSAPP + ("tel:",)) for a in pagina.anclas):
        falla("R11-paginas-respuesta", "error.html tiene que ofrecer otro canal, con un link a WhatsApp o a un teléfono.")
    if not secundaria:
        if not pagina.metas.get("description"):
            falla("R03-titulo-y-descripcion", "Falta <meta name=\"description\"> con texto.")
        if pagina.h1 != 1:
            falla("R04-un-h1", f"La página tiene {pagina.h1} títulos <h1>. Tiene que tener 1.")
        faltan_og = [clave for clave in ("og:title", "og:description", "og:image") if not pagina.metas.get(clave)]
        if faltan_og:
            falla("R05-open-graph", "Faltan las etiquetas " + ", ".join(faltan_og) + ".")
        if not any("canonical" in l.get("rel", "").lower().split() for l in pagina.links):
            falla("R07-canonical", "Falta <link rel=\"canonical\"> con la dirección completa de la página.")
        if pagina.texto_visible < TEXTO_MINIMO_CARACTERES and pagina.scripts:
            falla("R17-texto-en-html", "La página casi no trae texto escrito y tiene programas. El texto tiene que venir escrito en el HTML.")
        if ID_SELLO_HUELLA not in pagina.ids:
            falla("R27-huella", f"Falta el espacio del sello de huella de carbono en el pie, <div id=\"{ID_SELLO_HUELLA}\"></div>.")
        if not any(a["attrs"].get("href", "").startswith("tel:") for a in pagina.anclas):
            aviso("R34-telefono", "La página no tiene un link tel:. Si el cliente atiende por teléfono, el número se marca con un toque.")
    if not any("icon" in l.get("rel", "").lower().split() for l in pagina.links):
        falla("R06-icono", "Falta <link rel=\"icon\">.")

    for img in pagina.imagenes:
        src = img.get("src", "")
        faltan = [clave for clave in ("alt", "width", "height") if clave not in img]
        if faltan:
            falla("R08-imagen-atributos", f"La imagen {src} no trae " + ", ".join(faltan) + ".")

    for formulario in pagina.formularios:
        a = formulario["attrs"]
        accion = a.get("action", "").strip()
        if accion.lower().startswith("mailto:"):
            falla("R10-formulario", "El formulario usa mailto. Tiene que enviar a /api/contacto.")
        elif not accion.startswith("/api/"):
            falla("R10-formulario", f"El formulario envía a \"{accion}\". Tiene que enviar a una dirección /api/, por ejemplo /api/contacto.")
        if a.get("method", "").lower() != "post":
            falla("R10-formulario", "El formulario no trae method=\"POST\".")
        casillas = []
        for campo in formulario["campos"]:
            c = campo["attrs"]
            tipo = c.get("type", "text").lower()
            descripcion = f"<{campo['tag']} name=\"{c.get('name', '')}\">"
            if tipo == "checkbox":
                casillas.append(c)
            if tipo in {"submit", "button", "reset", "image"}:
                continue
            if not c.get("name"):
                falla("R10-formulario", f"Un campo <{campo['tag']}> del formulario no tiene name.")
            if tipo in CAMPOS_SIN_ETIQUETA:
                continue
            tiene_etiqueta = campo["dentro_de_etiqueta"] or (c.get("id") and c["id"] in pagina.etiquetas_para) or c.get("aria-label") or c.get("aria-labelledby")
            if not tiene_etiqueta:
                falla("R29-etiquetas", f"El campo {descripcion} no tiene una etiqueta <label> visible. El texto de ejemplo no cuenta como etiqueta.")
        consentimiento = [c for c in casillas if "checked" not in c and "required" in c]
        if not consentimiento:
            falla("R28-privacidad", "El formulario necesita una casilla de consentimiento obligatoria y sin marcar, por la ley 21.719.")
        if not any(any(p in a2["attrs"].get("href", "") for p in ("privacidad", "privacy")) for a2 in pagina.anclas):
            falla("R28-privacidad", "La página del formulario no enlaza al aviso de privacidad.")

    for elemento, lista in (("link", pagina.anclas), ("botón", pagina.botones)):
        for item in lista:
            at = item["attrs"]
            if not item["texto"].strip() and not at.get("aria-label") and not at.get("title"):
                destino = at.get("href", "") if elemento == "link" else at.get("type", "")
                falla("R30-vacio", f"Un {elemento} no tiene texto ni aria-label ({destino}). Un lector de pantalla no sabe qué hace.")

    for script in pagina.scripts:
        if es_externa(script.get("src", "")):
            falla("R12-externo", f"La página carga un programa de afuera: {script['src']}. Kumo agrega los programas de terceros.")
    for link in pagina.links:
        rel = link.get("rel", "").lower().split()
        if "stylesheet" in rel and es_externa(link.get("href", "")):
            falla("R12-externo", f"La página carga estilos o letras de afuera: {link['href']}. Las letras van en assets/fuentes/.")
        if "preconnect" in rel or "dns-prefetch" in rel:
            aviso("R12-externo", f"Sobra la conexión previa a {link.get('href', '')}.")
    for iframe in pagina.iframes:
        src = iframe.get("src", "")
        if es_externa(src) and not any(p in src for p in IFRAMES_PERMITIDOS):
            falla("R12-externo", f"La página incrusta un sitio de afuera: {src}.")

    for estilo in pagina.estilos_en_linea:
        if ESTILO_GRILLA.search(estilo):
            falla("R14-estilo-en-linea", f"Un style escrito en la etiqueta define la grilla y gana sobre la regla del teléfono: \"{estilo.strip()[:80]}\".")
        for valor in ESTILO_ANCHO.findall(estilo):
            if float(valor) > ANCHO_TELEFONO_PX:
                falla("R14-estilo-en-linea", f"Un style escrito en la etiqueta fija un ancho de {valor}px, más que un teléfono de {ANCHO_TELEFONO_PX}px.")

    for ancla in pagina.anclas:
        a = ancla["attrs"]
        pista = " ".join([ancla["texto"], a.get("id", ""), a.get("class", ""), a.get("aria-label", "")]).lower()
        if ("whatsapp" in pista or "wsp" in pista) and not a.get("href", "").startswith(PREFIJOS_WHATSAPP):
            falla("R15-whatsapp", f"Un botón de WhatsApp lleva a \"{a.get('href', '')}\". Tiene que llevar a https://wa.me/ con el número.")


def revisar_idiomas(paginas, raiz, hallazgos):
    principales = [p for p in paginas if not es_pagina_de_respuesta(p) and not es_pagina_de_privacidad(p)]
    idiomas = {p.lang.split("-")[0].lower() for p in principales if p.lang}
    if len(idiomas) <= 1:
        hallazgos.append(Hallazgo("AVISO", "R16-idiomas", "(sitio)", "El sitio tiene 1 solo idioma. Confirma que el cliente compró 1 solo idioma."))
        return
    for p in principales:
        alternos = {l.get("hreflang", "").split("-")[0].lower() for l in p.links if "alternate" in l.get("rel", "").lower().split() and l.get("hreflang")}
        faltan = idiomas - alternos
        if faltan:
            hallazgos.append(Hallazgo("FALLA", "R16-idiomas", nombre_pagina(p, raiz), "Faltan los links hreflang de " + ", ".join(sorted(faltan)) + "."))


def revisar_archivos(raiz, paginas, hallazgos):
    referenciados = set()
    og = set()
    automaticos = set()
    hay_formulario = any(p.formularios for p in paginas)

    for p in paginas:
        for url in p.referencias:
            destino = resolver(raiz, p.ruta, url.strip())
            if destino is None:
                continue
            referenciados.add(destino)
            if not destino.exists():
                hallazgos.append(Hallazgo("FALLA", "R09-enlace-roto", nombre_pagina(p, raiz), f"Apunta a {url}, que no está en la carpeta."))
        imagen_og = p.metas.get("og:image", "")
        if imagen_og:
            destino = resolver(raiz, p.ruta, urlparse(imagen_og).path or imagen_og)
            if destino is not None:
                og.add(destino)
                referenciados.add(destino)
        for video in p.videos:
            if "autoplay" in video["attrs"]:
                for fuente in video["fuentes"]:
                    destino = resolver(raiz, p.ruta, fuente)
                    if destino is not None:
                        automaticos.add(destino)
                faltan = [clave for clave in ("muted", "playsinline", "poster") if clave not in video["attrs"]]
                if faltan:
                    hallazgos.append(Hallazgo("FALLA", "R20-video", nombre_pagina(p, raiz), "Un video que parte solo no trae " + ", ".join(faltan) + "."))

    for css in raiz.rglob("*.css"):
        texto = css.read_text(encoding="utf-8", errors="replace")
        for url in URL_EN_CSS.findall(texto):
            destino = resolver(raiz, css, url.strip())
            if destino is not None:
                referenciados.add(destino)
                if not destino.exists():
                    hallazgos.append(Hallazgo("FALLA", "R09-enlace-roto", css.relative_to(raiz).as_posix(), f"Apunta a {url}, que no está en la carpeta."))

    if hay_formulario:
        for nombre in sorted(PAGINAS_DE_RESPUESTA):
            if not (raiz / nombre).exists():
                hallazgos.append(Hallazgo("FALLA", "R11-paginas-respuesta", "(sitio)", f"El sitio tiene formulario y falta {nombre} en la raíz."))
        if not (raiz / "privacidad.html").exists():
            hallazgos.append(Hallazgo("FALLA", "R28-privacidad", "(sitio)", "El sitio tiene formulario y falta privacidad.html con el aviso de privacidad."))

    if not (raiz / "CAMBIOS.txt").exists():
        hallazgos.append(Hallazgo("FALLA", "R23-cambios", "(sitio)", "Falta CAMBIOS.txt con la fecha y la lista de cambios de esta entrega."))

    for archivo in sorted(raiz.rglob("*")):
        if not archivo.is_file():
            continue
        relativo = archivo.relative_to(raiz)
        nombre = relativo.as_posix()
        tamano = archivo.stat().st_size
        extension = archivo.suffix.lower()
        en_raiz = len(relativo.parts) == 1
        es_de_kumo = nombre in ARCHIVOS_DE_KUMO or (en_raiz and extension in {".txt", ".md"})

        for parte in relativo.parts:
            mayuscula_permitida = en_raiz and extension in {".txt", ".md"}
            if not NOMBRE_VALIDO.match(parte.lower() if mayuscula_permitida else parte):
                hallazgos.append(Hallazgo("FALLA", "R21-nombre-archivo", nombre, f"El nombre \"{parte}\" tiene mayúsculas, espacios, tildes u otros signos."))
                break
        if not es_de_kumo:
            delata = PALABRAS_QUE_DELATAN.search(archivo.stem)
            if delata:
                hallazgos.append(Hallazgo("FALLA", "R33-nombre-que-delata", nombre, f"El nombre trae \"{delata.group(1)}\". Cualquier visitante puede leer el nombre de un archivo publicado."))

        if tamano > ARCHIVO_MAX_BYTES:
            hallazgos.append(Hallazgo("FALLA", "R24-archivo-enorme", nombre, f"Pesa {tamano / MB:.1f} MB. Un archivo de más de 25 MB no va dentro del sitio."))

        if extension in EXTENSIONES_TEXTO_REVISABLE:
            texto = archivo.read_text(encoding="utf-8", errors="replace")
            for patron in PATRONES_SECRETO:
                if patron.search(texto):
                    hallazgos.append(Hallazgo("FALLA", "R13-secreto", nombre, "El archivo parece traer una llave o clave secreta. Bórrala y avisa a Kumo."))
                    break

        destino = archivo.resolve()
        if extension in EXTENSIONES_FOTO:
            limite = FOTO_OG_MAX_BYTES if destino in og else FOTO_MAX_BYTES
            if tamano > limite:
                hallazgos.append(Hallazgo("FALLA", "R18-peso-imagen", nombre, f"Pesa {tamano / KB:.0f} KB. El máximo es {limite / KB:.0f} KB."))
            medidas = medidas_imagen(archivo)
            if medidas and medidas[0] > FOTO_MAX_ANCHO_PX:
                hallazgos.append(Hallazgo("FALLA", "R19-ancho-imagen", nombre, f"Mide {medidas[0]} píxeles de ancho. El máximo es {FOTO_MAX_ANCHO_PX}."))
            if extension in {".jpg", ".jpeg", ".png"} and destino not in og and archivo.name not in {"icono.png", "favicon.png"}:
                hallazgos.append(Hallazgo("AVISO", "R26-formato-imagen", nombre, "Conviene pasarla a WebP, que pesa menos con la misma calidad."))
        if extension in EXTENSIONES_VIDEO and destino in automaticos and tamano > VIDEO_AUTOMATICO_MAX_BYTES:
            hallazgos.append(Hallazgo("FALLA", "R20-video", nombre, f"El video parte solo y pesa {tamano / MB:.1f} MB. El máximo es 1,5 MB."))
        if extension in EXTENSIONES_FUENTE_LENTA:
            hallazgos.append(Hallazgo("AVISO", "R25-fuentes", nombre, "Las letras van en formato woff2, que pesa menos."))

        es_pagina = extension in {".html", ".htm"}
        if not es_pagina and not es_de_kumo and destino not in referenciados:
            hallazgos.append(Hallazgo("FALLA", "R22-archivo-sin-uso", nombre, "Ninguna página usa este archivo, pero igual se publica y cualquiera puede bajarlo. Bórralo."))


def revisar(raiz):
    hallazgos = []
    paginas = []
    for ruta in sorted(list(raiz.rglob("*.html")) + list(raiz.rglob("*.htm"))):
        pagina = Pagina(ruta=ruta.resolve())
        LectorHtml(pagina).feed(ruta.read_text(encoding="utf-8", errors="replace"))
        paginas.append(pagina)
        revisar_pagina(pagina, raiz, hallazgos)
    if not (raiz / "index.html").exists():
        hallazgos.append(Hallazgo("FALLA", "R00-carpeta", "(sitio)", "Falta index.html en la raíz de la carpeta."))
    revisar_idiomas(paginas, raiz, hallazgos)
    revisar_archivos(raiz, paginas, hallazgos)
    return hallazgos


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    lector = argparse.ArgumentParser(
        description="Revisa la carpeta de un sitio HTML contra el estándar de Kumo Cloud sin abrir un navegador. "
        "Sale con 0 si no hay fallas, con 1 si hay fallas y con 2 si la carpeta no existe.",
    )
    lector.add_argument("carpeta", help="Carpeta del sitio, la que tiene index.html")
    lector.add_argument("--json", action="store_true", help="Entrega los hallazgos en JSON")
    argumentos = lector.parse_args()

    raiz = Path(argumentos.carpeta).resolve()
    if not raiz.is_dir():
        print(f"No encuentro la carpeta {raiz}.", file=sys.stderr)
        return 2

    hallazgos = revisar(raiz)
    fallas = [h for h in hallazgos if h.nivel == "FALLA"]
    avisos = [h for h in hallazgos if h.nivel == "AVISO"]

    if argumentos.json:
        print(json.dumps([asdict(h) for h in hallazgos], ensure_ascii=False, indent=2))
    else:
        for h in sorted(hallazgos, key=lambda h: (h.nivel != "FALLA", h.regla, h.archivo)):
            print(f"{h.nivel}  {h.regla}  {h.archivo}")
            print(f"       {h.detalle}")
        print()
        print(f"Resultado: {len(fallas)} fallas y {len(avisos)} avisos.")
        print("La carpeta pasa la revisión 1. Sigue con la revisión de pantallas." if not fallas else "La entrega todavía no está lista. Corrige las fallas y vuelve a correr la revisión.")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
