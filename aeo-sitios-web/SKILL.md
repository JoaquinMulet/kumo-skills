---
name: aeo-sitios-web
description: "El playbook de Kumo para que un sitio web quede listo para la era agéntica y la búsqueda por IA (SEO/AEO). Usa esta skill SIEMPRE que construyas, publiques u optimices un sitio web (propio o de un cliente), al hacer SEO o AEO, cuando el usuario diga «optimiza el sitio para la IA», «que aparezca en ChatGPT/Perplexity», «agent readiness», «AEO», «GEO», «markdown para agentes», «content signals», «que los agentes puedan agendar/comprar», o cuando el escáner isitagentready.com marque brechas. Cubre los cuatro niveles: acceso de crawlers, descubrimiento, Markdown de origen (sin pagar plan Pro de Cloudflare) y puerta MCP con confirmación humana. Implementado y verificado en kumocloud.cl (21→36 puntos el mismo día)."
---

# Sitios web listos para la era agéntica (SEO/AEO)

Más de la mitad de las peticiones HTML de la web ya son de bots, y los
compradores B2B parten su investigación en chatbots de IA. Un sitio que
hacemos u optimizamos tiene DOS audiencias: el humano que lee y el agente que
resume, compara, recomienda y actúa. Este playbook deja el sitio listo para
ambas, por niveles y con verificación mecánica de cada nivel.

El instrumento de medición es **isitagentready.com** (escáner público de
Cloudflare): puntaje 0-100 en 5 categorías. Se corre ANTES de tocar nada
(línea base) y DESPUÉS de cada nivel. Referencia real: kumocloud.cl pasó de
21/100 a 36/100 en un día (2026-08-06) con los niveles 1 a 3.

## Antes de empezar: qué es humo (decírselo al cliente primero)

- **llms.txt casi no se consume**: Google declaró que ningún sistema de IA lo
  usa (Mueller/Illyes, 2025) y Ahrefs midió que el 97 % de los publicados
  recibió cero peticiones (mayo 2026). Se publica igual (cuesta minutos, es
  apuesta barata), pero JAMÁS se vende como la solución.
- **«Ranking en IA» no existe como métrica**: las recomendaciones de los
  asistentes cambian casi en cada consulta (SparkToro, enero 2026, 2.961
  consultas). Lo que resiste es el porcentaje de visibilidad agregado.
- **Google no exige ningún archivo especial**: sus funciones de IA usan los
  sistemas de ranking de siempre. Fragmentar contenido «para la IA» es
  contraproducente (guía oficial de AI features). El contenido claro y con
  fuentes fechadas sigue siendo la base (paper GEO, KDD 2024: estadísticas
  +37 %, citas +30 %. El keyword stuffing RESTA).
- **Cloudflare cobra por dos ejes que no se tocan**: Workers Paid (US$5/mes)
  es plan de CUENTA. Pro (US$20-25/mes) es plan de ZONA por dominio. Antes de
  recomendar una feature, verificar en la doc viva de qué plan cuelga y si el
  origen puede darla gratis (caso resuelto: Markdown for Agents → nivel 3).

## Nivel 1: acceso y postura (una hora, cualquier sitio)

1. **robots.txt** con reglas explícitas `Allow` para los bots de IA: GPTBot,
   OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User,
   PerplexityBot, Google-Extended, Applebot-Extended. Más `Sitemap:`.
2. **Content Signals** en robots.txt, según la postura del dueño:
   `Content-Signal: search=yes, ai-input=yes, ai-train=yes` (postura Kumo:
   máxima exposición. Un cliente puede elegir otra, pero que sea SU decisión
   declarada). Solo el 4 % de los grandes dominios lo tiene. Ventaja fácil.
3. **sitemap.xml** válido con `lastmod` reales.
4. **OJO Cloudflare**: jamás activar el robots.txt administrado ni el bloqueo
   de AI crawlers del dashboard: inyectan `Disallow` + 403 que contradicen la
   postura declarada.
5. **OJO dominios .cl en Cloudflare**: el asistente Add a domain se queda con
   el spinner para siempre, con o sin archivo de zona (visto el 2026-09-04 con
   aerostratus.cl). En la red, `registrar/domains/batch_check?id=<dominio>`
   responde 422 porque Cloudflare Registrar no maneja .cl, y el asistente no
   tolera ese error. Salida: desde la pestaña del panel con la sesión del
   dueño, `POST /api/v4/zones` (`{name, account:{id}, type:'full'}`), después
   `POST /zones/<id>/subscription` con `{rate_plan:{id:'free'}}` (sin esto
   la zona no sale de `initializing` y sus NS devuelven REFUSED), después
   `POST /zones/<id>/dns_records/import` con el archivo BIND, y abrir
   `dash.cloudflare.com/<cuenta>/<dominio>` para terminar el asistente. La
   zona nace sin los ajustes del asistente: fijar `ssl` en `strict` y
   `always_use_https` en `on`, y comprobar en `bot_management` que
   `ai_bots_protection` siga `disabled` e `is_robots_txt_managed` en `false`.

**Verificación (política declarada no es control):**
```bash
for UA in ClaudeBot GPTBot PerplexityBot Googlebot; do curl -s -o /dev/null -w "$UA %{http_code}\n" -A "Mozilla/5.0 (compatible; $UA/1.0)" https://tudominio.cl/; done
# todos 200; y el robots.txt servido debe ser el del repo, no uno inyectado
```

## Nivel 2: descubrimiento (una tarde)

1. **Link headers (RFC 8288)** en la portada, con rel registrados o
   reconocidos: `rel="api-catalog"`, `rel="service-doc"`, `rel="sitemap"`.
   El escáner descarta rel inventados: usar los de la lista IANA.
2. **Catálogo de APIs (RFC 9727)** en `/.well-known/api-catalog`
   (`application/linkset+json`. Si el archivo no tiene extensión, fijar el
   content-type en `_headers`). Solo si el sitio TIENE endpoints públicos.
3. **llms.txt** honesto: qué es el negocio, cómo leer el sitio, cifras con
   fecha y método, enlaces a cada página. Es un derivado. Se re-verifica
   contra las reglas de contenido del sitio cada vez que el sitio cambia.
4. **Server card MCP** en `/.well-known/mcp/server-card.json` SOLO si el
   nivel 4 existe o va a existir: anunciar un endpoint que da 404 es peor
   que no anunciarlo.

## Nivel 3: Markdown de origen (sin plan Pro)

Los agentes que piden `Accept: text/markdown` reciben Markdown (hasta 80 %
menos tokens). Cloudflare lo vende en el plan Pro de zona. Nosotros lo
servimos del origen gratis:

1. **Generador determinista**: `scripts/generar_md.py` (en esta skill)
   convierte cada `index.html` en un `index.md` co-ubicado. Falla en rojo si
   una página queda sin H1 o demasiado corta. Se corre tras editar cualquier
   página (dejarlo como centinela del proyecto).
   ```bash
   uv run python scripts/generar_md.py --raiz public --base https://tudominio.cl
   ```
2. **Middleware de negociación** (Cloudflare Pages, `functions/_middleware.js`):
   GET con `Accept: text/markdown` en ruta de página → servir el `index.md`
   con `Content-Type: text/markdown; charset=utf-8` y **`Vary: Accept`**
   (obligatorio: sin él un caché puede cruzar las audiencias). Todo lo demás
   sale por `next()` sin tocarse. En nginx/Express el patrón es el mismo:
   detectar el Accept, servir el archivo pre-generado, declarar Vary.
3. Si una página genera su contenido por JavaScript, su `.md` se cura a mano
   (mismo criterio que el texto indexable en HTML plano).

**Verificación** (en Pages, PRIMERO contra la URL del deploy
`https://<hash>.<proyecto>.pages.dev`: la propagación del dominio entre colos
no es atómica. Y en Git Bash exportar `MSYS_NO_PATHCONV=1` o curl rompe los
`-w` que empiezan con `/`):
```bash
curl -s -H "Accept: text/markdown" -o /dev/null -w "%{http_code} %{content_type}\n" https://tudominio.cl/   # 200 text/markdown
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" https://tudominio.cl/                              # 200 text/html
curl -s -H "Accept: text/markdown" https://tudominio.cl/ | head -5                                          # el contenido curado
```

## Nivel 4: puerta MCP (el sitio ACTÚA para agentes)

Si el sitio tiene un agente o acciones (agendar, cotizar, consultar), se
exponen por MCP (spec 2026-07-28, stateless) para que el agente del cliente
las use. Patrón verificado en kumo-agente (Cloudflare Agents SDK:
`createMcpHandler` de `agents/mcp/server` + `McpServer` v2):

- **Herramientas de lectura libres** (preguntar, consultar disponibilidad) y
  **acciones con confirmación humana en dos pasos.** La primera llamada
  devuelve `input_required` (elicitation) con el resumen. Sin `confirmar:
  true` del humano del agente visitante NO hay acción. Un cliente sin
  capacidad de elicitation recibe error y no puede ejecutar: correcto, sin
  canal de confirmación no hay acción.
- **La validación final vive en el servidor** (el mismo endpoint que valida
  al chat humano): aunque el agente alucine, la acción inválida se rechaza.
- **Seguridad**: el endpoint público pasa por un proxy con rate limit por IP;
  el Worker solo acepta con token compartido. SIN geo (el agente corre en
  cualquier datacenter aunque su humano esté en el país) y SIN Turnstile
  (está diseñado para bloquear agentes. Esta puerta existe para atenderlos).
  Gotcha. El rate limit en KV no atrapa ráfagas sub-minuto (consistencia
  eventual). Acota el abuso sostenido, y el costo del abuso se acota por
  diseño (confirmación en dos pasos).
- El handler exige `Accept: application/json, text/event-stream` (406 si no).

## Cierre: medir, publicar y predicar con el ejemplo

- Re-escanear en isitagentready.com y guardar el antes/después con fecha.
- El antes/después medido es material de marketing honesto de primera: un
  artículo «qué hicimos y cuánto subió» con cada cifra citada con fuente,
  fecha y enlace verificado con petición real (y sección escéptica incluida:
  la honestidad radical es la marca de la casa).
- WebMCP (bridge en el navegador) es toggle del dashboard de Cloudflare
  (Agent Readiness → Labs), acción del dueño de la cuenta. Con `data-mcp-url`
  se apunta al MCP propio. DNS-AID, Web Bot Auth y los protocolos de comercio
  (x402/UCP/ACP) siguen en borrador o sin adopción: se vigilan, no se
  implementan todavía.
