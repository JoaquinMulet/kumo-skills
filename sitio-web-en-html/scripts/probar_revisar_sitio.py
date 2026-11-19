import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

REVISOR = Path(__file__).with_name("revisar_sitio.py")
PLAZO_SEGUNDOS = 60


def png(ancho, alto, relleno_bytes=0):
    def bloque(tipo, datos):
        return struct.pack(">I", len(datos)) + tipo + datos + struct.pack(">I", zlib.crc32(tipo + datos) & 0xFFFFFFFF)

    filas = b"".join(b"\x00" + b"\x00" * ancho for _ in range(alto))
    cuerpo = b"\x89PNG\r\n\x1a\n" + bloque(b"IHDR", struct.pack(">IIBBBBB", ancho, alto, 8, 0, 0, 0, 0))
    cuerpo += bloque(b"IDAT", zlib.compress(filas)) + bloque(b"tEXt", b"x\x00" + b"a" * relleno_bytes) + bloque(b"IEND", b"")
    return cuerpo


def cabeza(lang, ruta, titulo):
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="Descripción de prueba">
<link rel="canonical" href="https://ejemplo.cl{ruta}">
<link rel="alternate" hreflang="es" href="https://ejemplo.cl/">
<link rel="alternate" hreflang="en" href="https://ejemplo.cl/en/">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="Descripción de prueba">
<meta property="og:image" content="https://ejemplo.cl/assets/og-portada.png">
<link rel="icon" href="/assets/icono.png">
<link rel="stylesheet" href="/assets/estilos.css">
</head>
"""


TEXTO = "Navegamos por el lago y caminamos por el bosque con guías locales. " * 5

CUERPO_ES = f"""<body>
<h1>Aventura en el lago</h1>
<p>{TEXTO}</p>
<a href="/en/">EN</a>
<img src="/assets/portada.png" alt="Lago al amanecer" width="40" height="20">
<a id="whatsapp" href="https://wa.me/56912345678">Escríbenos por WhatsApp</a>
<a href="#pago-pendiente">Pagar</a>
<a href="tel:+56912345678">Llámanos</a>
<form action="/api/contacto" method="POST">
<label for="nombre">Nombre</label>
<input id="nombre" name="nombre" required>
<label for="correo">Correo</label>
<input id="correo" name="correo" type="email" required>
<label>Mensaje <textarea name="mensaje"></textarea></label>
<label><input type="checkbox" name="consentimiento" required> Acepto el <a href="/privacidad.html">aviso de privacidad</a></label>
<div id="kumo-verificacion"></div>
<button type="submit">Enviar</button>
</form>
<footer><div id="kumo-huella"></div></footer>
</body></html>
"""

CUERPO_EN = f"""<body>
<h1>Lake adventure</h1>
<p>{TEXTO}</p>
<a href="/">ES</a>
<img src="/assets/portada.png" alt="Lake at dawn" width="40" height="20">
<a href="tel:+56912345678">Call us</a>
<footer><div id="kumo-huella"></div></footer>
</body></html>
"""

RESPUESTA = """<!doctype html><html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Gracias</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/assets/icono.png"></head><body><p>Listo.</p>
<a href="https://wa.me/56912345678">Escríbenos por WhatsApp</a></body></html>
"""

PRIVACIDAD = """<!doctype html><html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Aviso de privacidad</title>
<link rel="icon" href="/assets/icono.png"></head><body><h1>Aviso de privacidad</h1><p>Texto del aviso.</p></body></html>
"""


def armar_sitio_bueno(raiz):
    (raiz / "assets").mkdir(parents=True)
    (raiz / "en").mkdir()
    (raiz / "index.html").write_bytes((cabeza("es", "/", "Aventura") + CUERPO_ES).encode("utf-8"))
    (raiz / "en" / "index.html").write_bytes((cabeza("en", "/en/", "Adventure") + CUERPO_EN).encode("utf-8"))
    (raiz / "gracias.html").write_bytes(RESPUESTA.encode("utf-8"))
    (raiz / "error.html").write_bytes(RESPUESTA.encode("utf-8"))
    (raiz / "privacidad.html").write_bytes(PRIVACIDAD.encode("utf-8"))
    (raiz / "CAMBIOS.txt").write_bytes("19 de noviembre de 2026. Primera entrega.\n".encode("utf-8"))
    (raiz / "assets" / "estilos.css").write_bytes(b"body{font-family:sans-serif}\na,button,input,textarea{display:inline-block;min-height:44px;min-width:44px}\ninput[type=checkbox]{width:24px;height:24px}\n")
    (raiz / "assets" / "portada.png").write_bytes(png(40, 20))
    (raiz / "assets" / "og-portada.png").write_bytes(png(40, 20))
    (raiz / "assets" / "icono.png").write_bytes(png(16, 16))


def correr(raiz):
    resultado = subprocess.run(
        [sys.executable, "-I", str(REVISOR), str(raiz), "--json"],
        capture_output=True, text=True, encoding="utf-8", timeout=PLAZO_SEGUNDOS,
    )
    import json
    return resultado.returncode, json.loads(resultado.stdout or "[]"), resultado.stderr


def reemplazar(ruta, viejo, nuevo):
    texto = ruta.read_text(encoding="utf-8")
    assert viejo in texto, f"La prueba no encontró {viejo!r} en {ruta.name}"
    ruta.write_bytes(texto.replace(viejo, nuevo).encode("utf-8"))


CASOS = [
    ("formulario con mailto", "R10-formulario", lambda r: reemplazar(r / "index.html", 'action="/api/contacto"', 'action="mailto:hola@ejemplo.cl"')),
    ("campo sin name", "R10-formulario", lambda r: reemplazar(r / "index.html", '<textarea name="mensaje">', "<textarea>")),
    ("campo sin etiqueta", "R29-etiquetas", lambda r: reemplazar(r / "index.html", '<label for="nombre">Nombre</label>', "")),
    ("casilla premarcada", "R28-privacidad", lambda r: reemplazar(r / "index.html", 'name="consentimiento" required', 'name="consentimiento" required checked')),
    ("falta aviso de privacidad", "R28-privacidad", lambda r: (r / "privacidad.html").unlink()),
    ("falta sello de huella", "R27-huella", lambda r: reemplazar(r / "index.html", '<div id="kumo-huella"></div>', "")),
    ("gracias indexable", "R32-no-indexar", lambda r: reemplazar(r / "gracias.html", '<meta name="robots" content="noindex">', "")),
    ("error sin otro canal", "R11-paginas-respuesta", lambda r: reemplazar(r / "error.html", '<a href="https://wa.me/56912345678">Escríbenos por WhatsApp</a>', "")),
    ("boton vacio", "R30-vacio", lambda r: reemplazar(r / "index.html", '<button type="submit">Enviar</button>', '<button type="submit"></button>')),
    ("archivo sin uso", "R22-archivo-sin-uso", lambda r: (r / "assets" / "sobra.png").write_bytes(png(4, 4))),
    ("nombre que delata", "R33-nombre-que-delata", lambda r: (r / "assets" / "mirador-simulado.png").write_bytes(png(4, 4))),
    ("whatsapp que abre correo", "R15-whatsapp", lambda r: reemplazar(r / "index.html", 'href="https://wa.me/56912345678"', 'href="mailto:hola@ejemplo.cl"')),
    ("letras de Google", "R12-externo", lambda r: reemplazar(r / "index.html", '<link rel="stylesheet" href="/assets/estilos.css">', '<link rel="stylesheet" href="/assets/estilos.css"><link href="https://fonts.googleapis.com/css2?family=Manrope" rel="stylesheet">')),
    ("grilla en la etiqueta", "R14-estilo-en-linea", lambda r: reemplazar(r / "index.html", "<p>", '<p style="grid-template-columns:1.2fr .8fr">')),
    ("ancho fijo en la etiqueta", "R14-estilo-en-linea", lambda r: reemplazar(r / "index.html", "<p>", '<p style="width:600px">')),
    ("sin open graph", "R05-open-graph", lambda r: reemplazar(r / "index.html", '<meta property="og:image" content="https://ejemplo.cl/assets/og-portada.png">', "")),
    ("sin canonical", "R07-canonical", lambda r: reemplazar(r / "index.html", '<link rel="canonical" href="https://ejemplo.cl/">', "")),
    ("2 h1", "R04-un-h1", lambda r: reemplazar(r / "index.html", "</h1>", "</h1><h1>Otro</h1>")),
    ("imagen sin medidas", "R08-imagen-atributos", lambda r: reemplazar(r / "index.html", 'width="40" height="20"', "")),
    ("sin hreflang", "R16-idiomas", lambda r: reemplazar(r / "en" / "index.html", '<link rel="alternate" hreflang="es" href="https://ejemplo.cl/">', "")),
    ("foto pesada", "R18-peso-imagen", lambda r: (r / "assets" / "portada.png").write_bytes(png(40, 20, relleno_bytes=300 * 1024))),
    ("foto ancha", "R19-ancho-imagen", lambda r: (r / "assets" / "portada.png").write_bytes(png(2000, 4))),
    ("nombre con espacio", "R21-nombre-archivo", lambda r: (r / "assets" / "Foto Lago.png").write_bytes(png(4, 4))),
    ("enlace roto", "R09-enlace-roto", lambda r: (r / "assets" / "portada.png").unlink()),
    ("falta gracias", "R11-paginas-respuesta", lambda r: (r / "gracias.html").unlink()),
    ("falta cambios", "R23-cambios", lambda r: (r / "CAMBIOS.txt").unlink()),
    ("llave en el código", "R13-secreto", lambda r: reemplazar(r / "index.html", "</body>", '<script>const api_key = "sk_live_abcdefghijklmnop";</script></body>')),
    ("video sin muted", "R20-video", lambda r: reemplazar(r / "index.html", "</h1>", '</h1><video autoplay playsinline poster="/assets/portada.png" src="/assets/portada.png"></video>')),
    ("texto solo con programa", "R17-texto-en-html", lambda r: (reemplazar(r / "index.html", f"<p>{TEXTO}</p>", '<p id="t"></p>'), reemplazar(r / "index.html", "</body>", '<script src="/assets/estilos.css"></script></body>'))),
]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    errores = []
    with tempfile.TemporaryDirectory() as temporal:
        base = Path(temporal) / "base"
        armar_sitio_bueno(base)

        codigo, hallazgos, error = correr(base)
        fallas = [h for h in hallazgos if h["nivel"] == "FALLA"]
        if codigo != 0 or fallas:
            errores.append(f"El sitio bueno tiene que pasar y dio código {codigo} con {fallas} {error}")
        else:
            print("ok    el sitio bueno pasa")

        for nombre, regla, estropear in CASOS:
            sitio = Path(temporal) / nombre.replace(" ", "-")
            shutil.copytree(base, sitio)
            estropear(sitio)
            codigo, hallazgos, error = correr(sitio)
            reglas = {h["regla"] for h in hallazgos if h["nivel"] == "FALLA"}
            if codigo == 1 and regla in reglas:
                print(f"ok    {nombre} da {regla}")
            else:
                errores.append(f"{nombre}: esperaba {regla} con código 1 y obtuve código {codigo} con {sorted(reglas)} {error}")

    for e in errores:
        print("MAL   " + e)
    print(f"\n{len(CASOS) + 1 - len(errores)} de {len(CASOS) + 1} pruebas pasan.")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
