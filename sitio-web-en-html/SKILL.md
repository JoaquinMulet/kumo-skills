---
name: sitio-web-en-html
description: "Guía al diseñador que arma un sitio web en HTML puro para un cliente de Kumo Cloud, desde las preguntas antes de diseñar hasta la entrega revisada. Dice qué resuelve el HTML, qué queda para Kumo (formulario, pago, seguridad, publicación) y cuándo el sitio necesita Astro o Next.js. Trae 2 revisores automáticos que miden la carpeta y abren cada página en 375, 768 y 1440 píxeles. Usar cuando se diseña, arma, corrige o entrega una página web, landing o maqueta en HTML para Kumo, cuando el usuario dice «hagamos la página de», «maqueta HTML», «entregar el sitio a Kumo», «revisa mi HTML», o cuando Kumo recibe un HTML de un diseñador para publicarlo."
---

# Sitio web en HTML para Kumo Cloud

Esta skill sirve al diseñador que arma un sitio en HTML y a la inteligencia artificial que lo ayuda.
También la usa Kumo para recibir esa entrega. El resultado es una carpeta que Kumo publica tal cual,
sin rehacer el diseño.

La regla de fondo es una sola. Lo que se ve y se mueve en la pantalla lo hace el diseñador en HTML.
Lo que recibe datos, guarda datos o usa una clave secreta lo hace Kumo.

## Paso 1. Antes de diseñar, confirma que el sitio cabe en HTML

Pregunta al cliente qué tiene que hacer el sitio. Si la respuesta incluye un punto de esta lista,
avisa a Kumo antes de partir, porque Kumo construye esa parte en otro sistema.

- Las personas inician sesión, o hay zonas privadas.
- El sitio guarda datos, como reservas, cupos o una lista de clientes.
- El pago confirma la reserva solo, sin que el cliente revise su panel.
- El sitio muestra datos que cambian en el momento, como los cupos que quedan o un precio que viene
  de otro sistema.
- El cliente quiere un panel para editar tours, precios o fotos sin llamar a nadie.
- El sitio usa un servicio que exige una llave secreta.

Si el sitio no pide nada de esa lista, el HTML sirve. Estas piezas caben en HTML.

- Páginas, textos, fotos y videos.
- 2 idiomas, con un archivo para cada idioma.
- Botones que llevan a otro lugar, como WhatsApp, un link de pago, Instagram o Google Maps.
- Un mapa de Google puesto dentro de la página.
- Menús, pestañas, carruseles y animaciones.
- El diseño del formulario. Kumo lo hace funcionar, como dice el paso 6.

## Paso 2. Arma la carpeta

```text
sitio/
  index.html        la página principal en español
  en/index.html     la misma página en inglés, si el cliente compró 2 idiomas
  gracias.html      aparece cuando el formulario llega
  error.html        aparece cuando el formulario falla
  CAMBIOS.txt       la fecha y la lista de cambios de esta entrega
  assets/           fotos, video, estilos, programas
  assets/fuentes/   las letras en formato woff2
```

- Los nombres de archivo van en minúscula, sin espacios ni tildes, con guion entre palabras. Por
  ejemplo, `sendero-rio-botapiedra.webp`.
- Todo lo que está en la carpeta se publica. Borra las fotos y los videos que ninguna página usa.
- Los datos del cliente salen de su ficha, nunca de memoria. Revisa letra por letra el dominio, el
  correo y el teléfono.

## Paso 3. Diseña para todas las pantallas

- El sitio se ve completo en 375, 768 y 1440 píxeles de ancho. En ningún ancho la página se mueve
  hacia el lado.
- Los estilos van en el archivo de estilos o en la etiqueta `<style>` de la cabeza. Un `style`
  escrito dentro de una etiqueta gana sobre las reglas del teléfono. Es el error que más se repite.
- Las animaciones andan fluidas en un teléfono barato.
- El sitio respeta a quien pidió menos movimiento en su teléfono, con
  `@media (prefers-reduced-motion: reduce)`.
- Un texto importante nunca depende de una animación para aparecer.

## Paso 4. Prepara las fotos y el video

- Fotos en WebP, de máximo 1600 píxeles de ancho y 200 KB cada una.
- La foto para compartir en redes va en JPG de 1200 por 630 píxeles, de máximo 600 KB.
- Cada `<img>` lleva `width`, `height` y un `alt` que describe la foto.
- Las imágenes que están más abajo de la primera pantalla llevan `loading="lazy"`.
- El video que parte solo pesa menos de 1,5 MB y lleva `autoplay muted playsinline` y un `poster`.
  Sin `muted` y `playsinline` el video no parte en un iPhone.
- Una imagen hecha con inteligencia artificial dice «Imagen referencial» en su pie.
- La página entera pesa menos de 3 MB al abrir en un teléfono. Es un límite de Kumo para que la
  página cargue con señal móvil, no una medida de Google.

## Paso 5. Escribe los textos, los idiomas y el SEO

- Todo el texto viene escrito en el HTML. Google y los robots de las IA leen el texto escrito y casi
  nunca ejecutan JavaScript. Un texto que aparece con un programa no existe para ellos.
- Cada idioma es un archivo propio. Los botones ES y EN son links simples entre los 2 archivos.
  Un programa que cambia los textos en la misma página deja el inglés fuera de Google.
- Las letras van dentro de la carpeta. El sitio no carga letras desde Google, porque eso le entrega
  a Google los datos de cada visita y hace más lenta la página.

Cada página trae esta cabeza. Cambia los textos y las direcciones por los del cliente.

```html
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Nombre del cliente · Qué ofrece y dónde</title>
  <meta name="description" content="1 o 2 frases con lo que ofrece el cliente.">
  <link rel="canonical" href="https://dominio.cl/">
  <link rel="alternate" hreflang="es" href="https://dominio.cl/">
  <link rel="alternate" hreflang="en" href="https://dominio.cl/en/">
  <meta property="og:title" content="...">
  <meta property="og:description" content="...">
  <meta property="og:image" content="https://dominio.cl/assets/og-portada.jpg">
  <link rel="icon" href="/assets/icono.png">
  <link rel="stylesheet" href="/assets/estilos.css">
</head>
```

- Cada página tiene 1 solo `<h1>`.
- Los links `hreflang` van solo si el sitio tiene 2 idiomas.

## Paso 6. Deja el formulario y los botones listos para Kumo

El formulario sigue este modelo. Puedes agregar campos, cada uno con su `name`.

```html
<form action="/api/contacto" method="POST">
  <input name="nombre" required>
  <input name="correo" type="email" required>
  <input name="telefono" type="tel">
  <textarea name="mensaje" required></textarea>
  <div id="kumo-verificacion"></div>
  <button type="submit">Enviar</button>
</form>
```

- Diseña `gracias.html` y `error.html` con el mismo estilo del sitio.
- El formulario nunca usa `mailto:`. Un `mailto:` abre el programa de correo del visitante, y en
  muchos teléfonos ese programa no está configurado. El mensaje se pierde sin aviso.
- El botón de WhatsApp lleva a `https://wa.me/` seguido del número, con el código 56 y sin el signo
  más.
- El botón de pago lleva al link de pago de la pasarela del cliente. Si el link todavía no existe,
  el botón queda con `href="#pago-pendiente"` y Kumo lo completa.

Nunca pongas en el HTML ninguna de estas piezas.

- Llaves, claves o códigos de comercio.
- Programas de terceros, como estadísticas, chats o píxeles de publicidad. Kumo los agrega cuando el
  cliente los aprueba.
- Formularios de servicios externos.

## Paso 7. Revisa la entrega de punta a punta

La entrega está lista cuando pasa las 3 revisiones. Corre los comandos desde la carpeta de esta skill.

**Revisión 1. La carpeta.** Este revisor lee los archivos sin abrir un navegador. Tarda segundos.

```bash
uv run python scripts/revisar_sitio.py ruta/al/sitio
```

**Revisión 2. Las pantallas.** Este revisor abre cada página en un navegador real, en los 3 anchos.
Mide si la página se sale de la pantalla, cuánto pesa al abrir en un teléfono, y si hay errores o
archivos que no cargan. Guarda una captura completa de cada página en cada ancho. Tarda 1 o 2
minutos.

```bash
uv run --with playwright python scripts/revisar_pantallas.py ruta/al/sitio --capturas ruta/fuera/del/sitio
```

Si avisa que falta el navegador, corre 1 vez `uv run --with playwright python -m playwright install chromium`.

Cada revisor sale con código 0 cuando no hay fallas. Un aviso no bloquea la entrega, pero se lee.

**Revisión 3. Tus ojos.** Los revisores miden, pero no ven si el diseño se ve bien.

1. Mira cada captura de la revisión 2, en los 3 anchos. Busca textos montados, botones cortados y
   fotos deformadas.
2. Abre el sitio en un teléfono de verdad y recorre todas las secciones.
3. Presiona cada botón y cada link.
4. Lee cada texto contra la ficha del cliente, con el dominio, el correo y el teléfono.
5. Revisa que las imágenes hechas con inteligencia artificial digan «Imagen referencial».

## Paso 8. Entrega

- Un archivo `.zip` con la carpeta del sitio, sin las capturas.
- `CAMBIOS.txt` con la fecha y lo que cambió.
- La salida de los 2 revisores, con 0 fallas.

Kumo corre los mismos revisores al recibir. Si una revisión falla, la entrega vuelve con la lista.

## Lo que hace Kumo después

- **Formulario.** Kumo escribe el programa que recibe `/api/contacto` en el servidor de Cloudflare.
  El programa comprueba que escribe una persona, revisa los campos, guarda el mensaje, envía el
  correo al cliente y muestra `gracias.html`. La dirección `/api/contacto` es pública en cualquier
  sitio con formulario, también en Astro o Next.js. Por eso el programa lleva 8 defensas, cada una
  con su prueba automática que envía el ataque y comprueba el rechazo.
  1. Comprueba en el servidor el token de Turnstile, el filtro contra robots de Cloudflare.
  2. Limita los envíos por minuto y por día de cada dirección de internet, y el total del sitio.
  3. Envía siempre al correo fijo del cliente. Ningún dato del visitante cambia el destinatario.
  4. Convierte en texto simple todo lo que escribe el visitante antes de ponerlo en el correo.
  5. Rechaza un envío de más de 10 KB, y cada campo tiene un largo máximo.
  6. Acepta solo envíos que vienen del dominio del cliente.
  7. Muestra al visitante solo `gracias.html` o `error.html`, nunca el detalle de un error.
  8. Guarda las llaves en los secretos de Cloudflare, nunca en el código.
- **Pago.** El link de pago sale de la pasarela del cliente, como el Link de Pago de webpay.cl, Flow
  o Mercado Pago. La cuenta va a nombre del cliente, porque el dinero le llega a él. Con un link de
  pago el sitio no sabe si el visitante pagó, y el cliente confirma cada reserva en su panel. El pago
  que confirma solo es otro proyecto, porque la llave secreta vive en un servidor.
- **Caché.** Cloudflare guarda copias de los archivos cerca del visitante. Kumo configura que el HTML
  se revise en cada visita y que las fotos se guarden 1 día. Cuando cambias una foto, dale un nombre
  nuevo, y la foto nueva se ve de inmediato.
- **Seguridad.** Kumo configura los encabezados de seguridad y el certificado del candado.
- **SEO del sitio completo.** Kumo agrega los datos estructurados del negocio, `sitemap.xml`,
  `robots.txt`, la preparación para las IA y el alta en Google Search Console.
- **Publicación.** Kumo publica la carpeta en Cloudflare Pages y conecta el dominio y el correo.

## Quién responde por qué

El diseñador responde por el diseño, los textos, las fotos, los idiomas y que la entrega pase las 3
revisiones. Los cambios de diseño futuros también son suyos. Cambia su HTML y lo entrega de nuevo.

Kumo responde por que el sitio esté en línea y cargue rápido, que el formulario llegue y el link de
pago funcione, y por la seguridad, las actualizaciones, la caché y los respaldos. Cualquier falla
técnica después de publicar es de Kumo.

## Cuándo el sitio pasa a Astro o Next.js

El HTML puro no da menos SEO ni menos seguridad. Un sitio en Astro termina siendo HTML igual. Kumo
pasa un sitio a otro sistema por mantenimiento o por funciones.

- **Astro** conviene cuando el sitio tiene muchas páginas que comparten el menú y el pie, contenido
  que crece como un blog o un catálogo, o muchas fotos que hay que preparar por pantalla. Astro arma
  los 2 idiomas desde 1 sola plantilla. El HTML del diseñador entra a Astro casi igual.
- **Next.js, o Astro con servidor,** hace falta para cualquier punto de la lista del paso 1.

En los 2 casos el diseñador sigue entregando su diseño en HTML, y Kumo lo lleva al sistema.

## Las reglas de los revisores

Cada hallazgo trae su código. Esta tabla dice qué mide cada uno y dónde está la regla.

| Código | Mide | Paso |
|---|---|---|
| R00-carpeta | Hay `index.html` en la raíz | 2 |
| R01-idioma | La etiqueta `<html>` trae `lang` | 5 |
| R02-cabeza-basica | `charset` y `viewport` | 5 |
| R03-titulo-y-descripcion | `<title>` y descripción con texto | 5 |
| R04-un-h1 | 1 solo `<h1>` por página | 5 |
| R05-open-graph | La ficha para compartir en redes | 5 |
| R06-icono | El ícono de la pestaña | 5 |
| R07-canonical | La dirección oficial de la página | 5 |
| R08-imagen-atributos | `alt`, `width` y `height` en cada imagen | 4 |
| R09-enlace-roto | Cada archivo que se nombra existe | 2 |
| R10-formulario | El formulario sigue el modelo | 6 |
| R11-paginas-respuesta | `gracias.html` y `error.html` | 6 |
| R12-externo | Programas, estilos o letras de afuera | 5 y 6 |
| R13-secreto | Llaves o claves en los archivos | 6 |
| R14-estilo-en-linea | Grillas o anchos fijos dentro de una etiqueta | 3 |
| R15-whatsapp | El botón de WhatsApp lleva a `wa.me` | 6 |
| R16-idiomas | Cada idioma enlaza con el otro | 5 |
| R17-texto-en-html | El texto viene escrito en el HTML | 5 |
| R18-peso-imagen | Peso de cada foto | 4 |
| R19-ancho-imagen | Ancho de cada foto | 4 |
| R20-video | Peso y atributos del video que parte solo | 4 |
| R21-nombre-archivo | Nombres sin mayúsculas, espacios ni tildes | 2 |
| R22-archivo-sin-uso | Archivos que ninguna página usa | 2 |
| R23-cambios | `CAMBIOS.txt` | 8 |
| R24-limite-cloudflare | Ningún archivo pasa de 25 MB | 4 |
| R25-fuentes | Letras en woff2 | 5 |
| R26-formato-imagen | Fotos en WebP | 4 |
| P01-desborde | La página no se sale de la pantalla en los 3 anchos | 3 |
| P02-peso-inicial | La página pesa menos de 3 MB al abrir en un teléfono | 4 |
| P03-error-de-programa | El navegador no muestra errores de programa | 3 |
| P04-archivo-no-carga | Todos los archivos cargan | 2 |

Las pruebas del revisor de la carpeta están en `scripts/probar_revisar_sitio.py`. Arman un sitio
bueno, lo rompen de 20 formas y comprueban que cada falla aparece. Se corren con
`uv run python scripts/probar_revisar_sitio.py`.
