---
name: sitio-web-en-html
description: "Guía al diseñador que arma un sitio web en HTML puro para un cliente de Kumo Cloud, desde las preguntas antes de diseñar hasta la entrega revisada. Cubre el estándar de Kumo (teléfono primero, accesibilidad WCAG 2.2 AA, ley 21.719 de datos personales, velocidad, SEO, sello de huella de carbono), qué queda para Kumo (formulario, pago, publicación en AWS Amplify, monitoreo) y cuándo el sitio necesita Next.js. Trae 2 revisores automáticos que miden la carpeta y abren cada página en 375, 768 y 1440 píxeles. Usar cuando se diseña, arma, corrige o entrega una página web, landing o maqueta en HTML para Kumo, cuando el usuario dice «hagamos la página de», «maqueta HTML», «entregar el sitio a Kumo», «revisa mi HTML», o cuando Kumo recibe un HTML de un diseñador para publicarlo."
---

# Sitio web en HTML para Kumo Cloud

Esta skill sirve al diseñador que arma un sitio en HTML y a la inteligencia artificial que lo ayuda.
También la usa Kumo para recibir esa entrega. El resultado es una carpeta que Kumo publica tal cual
en AWS Amplify, sin rehacer el diseño.

La regla de fondo es una sola. Lo que se ve y se mueve en la pantalla lo hace el diseñador en HTML.
Lo que recibe datos, guarda datos o usa una clave secreta lo hace Kumo.

Las reglas salen de los documentos de Kumo. Las principales son la especificación del brief web
(secciones 0.9, E7 y E9 y sus 2 listas de chequeo), el catálogo de precios y los procedimientos.

## Paso 1. Antes de diseñar, confirma que el sitio cabe en HTML

Pregunta al cliente qué tiene que hacer el sitio. Si la respuesta incluye un punto de esta lista,
avisa a Kumo antes de partir, porque Kumo construye esa parte en Next.js.

- Las personas inician sesión, o hay zonas privadas.
- El sitio guarda datos, como reservas, cupos o una lista de clientes.
- El pago confirma la reserva solo, sin que el cliente revise su panel.
- El sitio muestra datos que cambian en el momento, como los cupos que quedan o un precio que viene
  de otro sistema.
- El cliente quiere publicar o editar textos, tours, precios o fotos sin llamar a nadie. En HTML
  puro cada cambio lo hace el diseñador. Un editor para el cliente es otro ítem de la cotización.
- El sitio usa un servicio que exige una llave secreta.

Si el sitio no pide nada de esa lista, el HTML sirve. Estas piezas caben en HTML.

- Páginas, textos, fotos y videos.
- 2 idiomas, con un archivo para cada idioma.
- Botones que llevan a otro lugar, como WhatsApp, teléfono, un link de pago, Instagram o Google Maps.
- Un mapa de Google puesto dentro de la página.
- Menús, pestañas, carruseles y animaciones.
- El diseño del formulario y del aviso de privacidad. Kumo hace funcionar el formulario.

## Paso 2. Arma la carpeta

```text
sitio/
  index.html        la página principal en español
  en/index.html     la misma página en inglés, si el cliente compró 2 idiomas
  gracias.html      aparece cuando el formulario llega
  error.html        aparece cuando el formulario falla
  privacidad.html   el aviso de privacidad, si hay formulario
  CAMBIOS.txt       la fecha y la lista de cambios de esta entrega
  assets/           fotos, video, estilos, programas
  assets/fuentes/   las letras en formato woff2
```

- Todo lo que está en la carpeta se publica, y cualquier persona puede bajarlo aunque ninguna
  página lo enlace. Borra cada foto, video o nota que ninguna página usa.
- Los nombres de archivo van en minúscula, sin espacios ni tildes, con guion entre palabras.
- El nombre de una foto lleva primero la palabra que la gente busca, en 3 a 5 palabras. Por ejemplo,
  `navegacion-lago-victoria.webp`.
- Ningún nombre delata trabajo interno. Palabras como simulado, borrador, prueba, copia o maqueta
  quedan fuera del nombre.
- Los datos del cliente salen de su ficha, nunca de memoria. Revisa letra por letra el dominio, el
  correo y el teléfono.

## Paso 3. Diseña primero para el teléfono

La mayoría de las visitas llega desde un teléfono, por un QR, una tarjeta NFC o WhatsApp. Diseña
primero la versión de teléfono y de ahí deriva la de computador.

- El sitio se ve completo en 375, 768 y 1440 píxeles de ancho. En ningún ancho la página se mueve
  hacia el lado.
- Los estilos van en el archivo de estilos o en la etiqueta `<style>` de la cabeza. Un `style`
  escrito dentro de una etiqueta gana sobre las reglas del teléfono. Es el error que más se repite.
- El teléfono y el WhatsApp quedan a la vista en el teléfono, sin abrir el menú.
- Las animaciones andan fluidas en un teléfono barato.
- El sitio respeta a quien pidió menos movimiento, con `@media (prefers-reduced-motion: reduce)`.
- Un texto importante nunca depende de una animación ni de un clic para aparecer.

## Paso 4. Cumple la accesibilidad WCAG 2.2 nivel AA

Kumo la incluye en todo sitio. Estos son los puntos que dependen del diseño.

- Contraste de 4,5 a 1 para el texto normal, y de 3 a 1 para el texto grande, los bordes de los
  campos y los íconos. El texto grande mide 24 píxeles o más, o 18,66 píxeles en negrita.
- Los colores van como variables en `:root` del archivo de estilos. Así se revisa cada par de color
  de texto y fondo 1 sola vez.
- Cada botón, link y campo mide al menos 24 por 24 píxeles.
- El foco del teclado se ve siempre, y ninguna barra fija lo tapa.
- Todo el sitio se recorre solo con el teclado, incluido el formulario.
- Cada campo tiene su etiqueta visible encima. El texto de ejemplo dentro del campo no es una
  etiqueta.
- Cada link y cada botón tiene texto, o un `aria-label` si es solo un ícono.
- Un error se marca con borde y con texto, nunca solo con color.
- Nada de widgets que prometen accesibilidad automática.

## Paso 5. Prepara las fotos, el video y la velocidad

- Fotos en WebP, de máximo 1600 píxeles de ancho y 200 KB cada una.
- La foto para compartir en redes va en JPG de 1200 por 630 píxeles, de máximo 600 KB.
- Cada `<img>` lleva `width`, `height` y un `alt` que describe la foto.
- Las imágenes que están más abajo de la primera pantalla llevan `loading="lazy"`.
- El video que parte solo pesa menos de 1,5 MB y lleva `autoplay muted playsinline` y un `poster`.
  Sin `muted` y `playsinline` el video no parte en un iPhone.
- Una imagen hecha con inteligencia artificial dice «Imagen referencial» en su pie.
- Usa 2 tipografías como máximo.
- La velocidad sigue los umbrales de Google. El contenido principal aparece en 2,5 segundos o menos,
  y la página no salta mientras carga. El revisor 2 lo mide con señal lenta de teléfono.

## Paso 6. Escribe los textos, los idiomas y el SEO

- Todo el texto viene escrito en el HTML. Google y los robots de las IA leen el texto escrito y casi
  nunca ejecutan JavaScript.
- Cada idioma es un archivo propio, con el mismo contenido y los mismos `alt`. Los botones ES y EN
  son links simples entre los 2 archivos.
- Las letras van dentro de la carpeta. El sitio no carga letras desde Google.

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
- `gracias.html` y `error.html` llevan `<meta name="robots" content="noindex">`, porque no van en
  Google.

## Paso 7. Deja el formulario, la privacidad y los botones listos para Kumo

El formulario sigue este modelo. Puedes agregar campos, cada uno con su `name` y su etiqueta.

```html
<form action="/api/contacto" method="POST">
  <label for="nombre">Nombre</label>
  <input id="nombre" name="nombre" required>
  <label for="correo">Correo</label>
  <input id="correo" name="correo" type="email" required>
  <label for="mensaje">Mensaje</label>
  <textarea id="mensaje" name="mensaje" required></textarea>
  <label>
    <input type="checkbox" name="consentimiento" required>
    Acepto el <a href="/privacidad.html">aviso de privacidad</a>
  </label>
  <div id="kumo-verificacion"></div>
  <button type="submit">Enviar</button>
</form>
```

- La casilla de consentimiento es obligatoria y parte sin marcar. Lo exige la ley 21.719 de datos
  personales, que rige completa desde el 1 de diciembre de 2026.
- Diseña `privacidad.html` con el estilo del sitio. El texto del aviso lo define Kumo con el cliente.
- Diseña `gracias.html` y `error.html`. La página de error ofrece otro canal, con el WhatsApp y el
  teléfono del cliente.
- El formulario usa 1 sola columna y pide solo los datos que el cliente de verdad necesita.
- El formulario nunca usa `mailto:`. Un `mailto:` abre el programa de correo del visitante, y en
  muchos teléfonos ese programa no está configurado. El mensaje se pierde sin aviso.
- El botón de WhatsApp lleva a `https://wa.me/` seguido del número, con el código 56 y sin el signo
  más.
- El teléfono va como link `tel:`, para llamar con un toque.
- El botón de pago lleva al link de pago de la pasarela del cliente. Si el link todavía no existe,
  el botón queda con `href="#pago-pendiente"` y Kumo lo completa.
- El pie de cada página trae el espacio para el sello de huella de carbono de Kumo,
  `<div id="kumo-huella"></div>`. Kumo pone el sello.

Nunca pongas en el HTML ninguna de estas piezas.

- Llaves, claves o códigos de comercio.
- Programas de terceros, como estadísticas, chats o píxeles de publicidad. Kumo los agrega cuando el
  cliente los aprueba, y los que rastrean personas cargan solo con su permiso.
- Formularios de servicios externos.

## Paso 8. Revisa la entrega de punta a punta

La entrega está lista cuando pasa las 3 revisiones. Corre los comandos desde la carpeta de esta skill.

**Revisión 1. La carpeta.** Este revisor lee los archivos sin abrir un navegador. Tarda segundos.

```bash
uv run python scripts/revisar_sitio.py ruta/al/sitio
```

**Revisión 2. Las pantallas.** Este revisor abre cada página en un navegador real, en los 3 anchos.
Mide si la página se sale de la pantalla, el contraste de los textos, el tamaño de los botones, la
velocidad con señal lenta de teléfono, y si hay errores o archivos que no cargan. Guarda una captura
completa de cada página en cada ancho. Tarda de 1 a 4 minutos.

```bash
uv run --with playwright python scripts/revisar_pantallas.py ruta/al/sitio --capturas ruta/fuera/del/sitio
```

Si avisa que falta el navegador, corre 1 vez `uv run --with playwright python -m playwright install chromium`.

Cada revisor sale con código 0 cuando no hay fallas. Un aviso no bloquea la entrega, pero se lee.

**Revisión 3. Tus ojos.** Los revisores miden, pero no ven si el diseño se ve bien.

1. Mira cada captura de la revisión 2, en los 3 anchos. Busca textos montados, botones cortados y
   fotos deformadas.
2. Revisa a ojo el contraste de los textos que van sobre una foto. El revisor 2 los cuenta, pero
   no los puede medir.
3. Abre el sitio en un teléfono de verdad y recorre todas las secciones.
4. Recorre el sitio solo con la tecla Tab. El foco se ve en cada paso y llega a todos los botones.
5. Activa en tu teléfono la opción de reducir el movimiento y mira que las animaciones se calmen.
6. Presiona cada botón y cada link, incluidos los del pie.
7. Lee cada texto contra la ficha del cliente, con el dominio, el correo y el teléfono. Cero erratas.
8. Revisa que las imágenes hechas con inteligencia artificial digan «Imagen referencial».

## Paso 9. Entrega

- Un archivo `.zip` con la carpeta del sitio, sin las capturas.
- `CAMBIOS.txt` con la fecha y lo que cambió.
- La salida de los 2 revisores, con 0 fallas.

Kumo corre los mismos revisores al recibir. Si una revisión falla, la entrega vuelve con la lista.

## Lo que hace Kumo después

- **Publicación.** Kumo sube la carpeta a un repositorio y la publica en AWS Amplify, como los demás
  sitios de Kumo. Cada cambio se publica solo desde el repositorio, y cualquier versión anterior se
  puede recuperar.
- **Formulario.** Kumo conecta `/api/contacto` con el flujo que recibe los datos y envía el correo
  al cliente. La dirección del formulario es pública en cualquier sitio, también en Next.js. Por eso
  el flujo lleva 8 defensas, cada una con su prueba.
  1. Un campo trampa que los robots llenan y las personas no ven, más el filtro de Turnstile.
  2. Un límite de envíos por minuto y por día de cada dirección de internet.
  3. El correo llega siempre al destino fijo del cliente. Ningún dato del visitante cambia el
     destinatario.
  4. Todo lo que escribe el visitante pasa a texto simple antes de ir en el correo.
  5. Un tamaño máximo para el envío y para cada campo.
  6. Solo se aceptan envíos que vienen del dominio del cliente.
  7. El visitante ve solo `gracias.html` o `error.html`, nunca el detalle de un error.
  8. Las llaves viven en los secretos del servidor, nunca en el código.
- **Si el formulario falla.** El visitante ve `error.html` con el WhatsApp y el teléfono, y la
  visita no se cuenta como contacto. Cada mensaje queda guardado además fuera del correo, para que
  una falla del correo no borre la solicitud.
- **Llegada del correo.** Kumo configura los registros SPF, DKIM y DMARC del dominio, y comprueba que
  el correo llega a la bandeja de entrada de Gmail y de Outlook, no a la carpeta de spam.
- **Pago.** La pasarela la elige el cliente, entre opciones que Kumo le presenta con su costo. Un link
  de pago, como el Link de Pago de webpay.cl, Flow o Mercado Pago, cabe en un botón. La cuenta va a
  nombre del cliente, porque el dinero le llega a él. Con un link de pago el sitio no sabe si el
  visitante pagó, y el cliente confirma cada pago en su panel. La integración con Flow o Fintoc, con
  pagos únicos, mensuales o suscripciones, es otro ítem de la cotización y la construye Kumo.
- **Sello de huella de carbono.** Kumo pone en el espacio `kumo-huella` el sello que muestra los kilos
  de CO2 que emitió el sitio el último mes. La cifra sale del tráfico real que mide Amplify.
- **Caché y seguridad.** Kumo configura en Amplify que el HTML se revise en cada visita y que las fotos
  se guarden 1 día. Cuando cambias una foto, dale un nombre nuevo. Kumo también configura los
  encabezados de seguridad y el certificado del candado.
- **SEO del sitio completo.** Kumo agrega los datos estructurados del negocio, `sitemap.xml`,
  `robots.txt` y la preparación para las IA. Kumo da de alta el sitio en Google Search Console y
  revisa que la ficha de Google del negocio diga lo mismo que el sitio.
- **Sitio anterior.** Si el cliente tenía un sitio, Kumo redirige cada dirección vieja a la nueva. El
  sitio de prueba queda fuera de Google, y Kumo lo comprueba buscándolo.
- **Medición.** Kumo mide cada botón de contacto, el formulario, el WhatsApp y el teléfono. Las
  herramientas que rastrean personas, como Google Analytics, cargan solo después del permiso del
  visitante.
- **Después de publicar.** Kumo vigila el sitio las 24 horas, guarda respaldos y responde ante caídas.
  Kumo revisa la velocidad con datos de visitas reales en Search Console. Durante 30 días Kumo corrige
  sin costo cualquier defecto de lo entregado.

## Quién responde por qué

El diseñador responde por el diseño, los textos, las fotos, los idiomas y que la entrega pase las 3
revisiones. Los cambios de diseño futuros también son suyos. Cambia su HTML y lo entrega de nuevo.

Kumo responde por que el sitio esté en línea y cargue rápido, que el formulario llegue y el link de
pago funcione, y por la seguridad, las actualizaciones, la caché, el monitoreo y los respaldos.
Cualquier falla técnica después de publicar es de Kumo.

## Cuándo el sitio pasa a Next.js

El HTML puro no da menos SEO ni menos seguridad. Kumo construye en Next.js, también sobre Amplify,
cuando el sitio pide un punto de la lista del paso 1, o cuando tiene muchas páginas que comparten el
menú y el pie, o contenido que crece, como un blog o un catálogo. En esos casos el diseñador sigue
entregando su diseño en HTML, y Kumo lo lleva a Next.js.

## Las reglas de los revisores

Cada hallazgo trae su código. Esta tabla dice qué mide cada uno y en qué paso está la regla.

| Código | Mide | Paso |
|---|---|---|
| R00-carpeta | Hay `index.html` en la raíz | 2 |
| R01-idioma | La etiqueta `<html>` trae `lang` | 6 |
| R02-cabeza-basica | `charset` y `viewport` | 6 |
| R03-titulo-y-descripcion | `<title>` y descripción con texto | 6 |
| R04-un-h1 | 1 solo `<h1>` por página | 6 |
| R05-open-graph | La ficha para compartir en redes | 6 |
| R06-icono | El ícono de la pestaña | 6 |
| R07-canonical | La dirección oficial de la página | 6 |
| R08-imagen-atributos | `alt`, `width` y `height` en cada imagen | 5 |
| R09-enlace-roto | Cada archivo que se nombra existe | 2 |
| R10-formulario | El formulario sigue el modelo | 7 |
| R11-paginas-respuesta | `gracias.html` y `error.html`, con otro canal en la de error | 7 |
| R12-externo | Programas, estilos o letras de afuera | 6 y 7 |
| R13-secreto | Llaves o claves en los archivos | 7 |
| R14-estilo-en-linea | Grillas o anchos fijos dentro de una etiqueta | 3 |
| R15-whatsapp | El botón de WhatsApp lleva a `wa.me` | 7 |
| R16-idiomas | Cada idioma enlaza con el otro | 6 |
| R17-texto-en-html | El texto viene escrito en el HTML | 6 |
| R18-peso-imagen | Peso de cada foto | 5 |
| R19-ancho-imagen | Ancho de cada foto | 5 |
| R20-video | Peso y atributos del video que parte solo | 5 |
| R21-nombre-archivo | Nombres sin mayúsculas, espacios ni tildes | 2 |
| R22-archivo-sin-uso | Archivos que ninguna página usa | 2 |
| R23-cambios | `CAMBIOS.txt` | 9 |
| R24-archivo-enorme | Ningún archivo pasa de 25 MB | 5 |
| R25-fuentes | Letras en woff2 | 6 |
| R26-formato-imagen | Fotos en WebP | 5 |
| R27-huella | El espacio del sello de huella en el pie | 7 |
| R28-privacidad | Casilla de consentimiento, link y `privacidad.html` | 7 |
| R29-etiquetas | Cada campo con su etiqueta visible | 4 |
| R30-vacio | Links y botones con texto | 4 |
| R32-no-indexar | `gracias.html` y `error.html` fuera de Google | 6 |
| R33-nombre-que-delata | Nombres sin palabras de trabajo interno | 2 |
| R34-telefono | Un link `tel:` en la página | 7 |
| P01-desborde | La página no se sale de la pantalla en los 3 anchos | 3 |
| P02-peso-inicial | Aviso si la página baja más de 3 MB al abrir en un teléfono | 5 |
| P03-error-de-programa | El navegador no muestra errores de programa | 3 |
| P04-archivo-no-carga | Todos los archivos cargan | 2 |
| P05-contraste | Contraste de cada texto sobre su fondo | 4 |
| P06-objetivo-tactil | Botones, links y campos de 24 por 24 píxeles o más | 4 |
| P07-velocidad | Contenido principal en 2,5 segundos y página sin saltos, con señal lenta | 5 |

Las pruebas del revisor de la carpeta están en `scripts/probar_revisar_sitio.py`. Arman un sitio
bueno, lo rompen de 29 formas y comprueban que cada falla aparece. Se corren con
`uv run python scripts/probar_revisar_sitio.py`.
