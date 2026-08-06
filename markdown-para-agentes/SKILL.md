---
name: markdown-para-agentes
description: Implementa negociación de contenido Markdown de ORIGEN en cualquier sitio web (responder text/markdown cuando un agente de IA pide Accept':' text/markdown), sin pagar el plan Pro de zona de Cloudflare. Usa esta skill al preparar un sitio para agentes de IA, cuando el escáner de agent-readiness marque «no Markdown content negotiation», cuando alguien proponga contratar Cloudflare Pro solo por «Markdown for Agents», o cuando el usuario diga «markdown para agentes», «sirve markdown a los bots», «agent readiness del sitio». Aplica a Cloudflare Pages/Workers y a cualquier origen que controlemos (nginx, Express, etc.).
---

# Markdown para agentes, desde el origen (sin plan Pro)

Los agentes de IA que piden una página con `Accept: text/markdown` esperan
una versión en Markdown: pesa hasta 80 % menos tokens que el HTML. Cloudflare
vende esto como «Markdown for Agents», gratis PERO solo desde el plan **Pro
de zona** (US$20-25/mes por dominio). La propia doc de Cloudflare reconoce la
alternativa: **que el origen sirva `text/markdown` él mismo**. Si controlamos
el origen (Pages, Workers, nginx), eso cuesta cero y entrega mejor Markdown,
porque lo curamos nosotros en vez de convertirlo al vuelo.

Distinción que evita compras innecesarias: **Workers Paid (US$5/mes) es plan
de CUENTA; Pro es plan de ZONA por dominio. Tener uno no da acceso al otro.**
Antes de recomendar cualquier feature de Cloudflare, verificar en la doc viva
de qué plan cuelga y si el origen puede darla gratis.

## El método (dos piezas + verificación)

### 1. Generador determinista de Markdown

La transformación HTML → Markdown es determinista: va en un script, no en un
modelo ni a mano. `scripts/generar_md.py` (en esta skill) convierte cada
`index.html` en un `index.md` co-ubicado: extrae h1/h2/h3, párrafos, listas,
tablas y enlaces (absolutizados), y descarta scripts, estilos y el footer.

```bash
uv run python scripts/generar_md.py --raiz public --base https://tudominio.cl
```

Reglas del generador:
- El `.md` vive JUNTO al `.html` (`/ia/index.md` junto a `/ia/index.html`):
  queda desplegado como asset estático y además es fetchable directo.
- **Falla en rojo**: si una página produce un Markdown sin H1 o sospechosamente
  corto, el script termina con error. Un verde debe poder ponerse rojo.
- Se corre **cada vez que se edita una página** (es parte del checklist de
  publicación, igual que actualizar `dateModified`). Un `.md` desactualizado
  miente en silencio: conviene dejarlo como centinela del proyecto.

### 2. Negociación en el borde del origen

**Cloudflare Pages** — `functions/_middleware.js`:

```js
export async function onRequest(context) {
  const { request, env, next } = context;
  if (request.method === "GET") {
    const accept = request.headers.get("Accept") || "";
    if (accept.includes("text/markdown")) {
      const url = new URL(request.url);
      if (url.pathname.endsWith("/")) {
        const md = await env.ASSETS.fetch(
          new Request(url.origin + url.pathname + "index.md")
        );
        if (md.ok) {
          return new Response(md.body, {
            status: 200,
            headers: {
              "Content-Type": "text/markdown; charset=utf-8",
              "Vary": "Accept",
              "Cache-Control": "public, max-age=0, must-revalidate",
            },
          });
        }
      }
    }
  }
  return next();
}
```

- `Vary: Accept` es obligatorio: sin él, un caché intermedio puede servirle
  el Markdown a un humano (o el HTML a un agente).
- El middleware envuelve TODAS las rutas: el camino sin `Accept: text/markdown`
  debe salir por `next()` de inmediato, sin tocar APIs ni assets.
- Si el sitio declara Content Signals en robots.txt, repetir la declaración
  como header `Content-Signal` en la respuesta Markdown es coherente (es lo
  que hace el producto de Cloudflare).
- **Worker puro**: misma lógica en el `fetch` antes del resto del router.
- **nginx**: `map $http_accept $md_suffix { default ""; "~text/markdown" "index.md"; }`
  + `try_files` hacia el `.md`; **Express**: middleware con
  `req.accepts()` que haga `res.sendFile` del `.md` con el content-type
  correcto. El patrón es el mismo: detectar el Accept, servir el archivo
  pre-generado, declarar `Vary: Accept`.

### 3. Verificación con peticiones reales (obligatoria)

Una política declarada no es un control: se comprueba con curl, y en un
despliegue de Cloudflare Pages se comprueba PRIMERO contra la URL propia del
deploy (`https://<hash>.<proyecto>.pages.dev`), porque la propagación entre
colos del dominio no es atómica y el dominio puede servir lo viejo unos
minutos.

```bash
# 1. El agente recibe Markdown de verdad:
curl -s -H "Accept: text/markdown" -o /dev/null -w "%{http_code} %{content_type}\n" https://tudominio.cl/
# esperado: 200 text/markdown; charset=utf-8

# 2. El humano sigue recibiendo HTML:
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" https://tudominio.cl/
# esperado: 200 text/html

# 3. El contenido es el curado, no un octet-stream ni un 404 suave:
curl -s -H "Accept: text/markdown" https://tudominio.cl/ | head -5

# 4. Las rutas que NO son páginas no cambiaron (API, assets):
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" https://tudominio.cl/api/loquesea
```

El escáner de referencia es **isitagentready.com** (Cloudflare): su check
«Markdown Negotiation» pide la portada con `Accept: text/markdown` y aprueba
si el `Content-Type` de vuelta es `text/markdown`. Re-escanear después de
desplegar.

## Gotchas aprendidos

- **Git Bash rompe los `-w` de curl que empiezan con `/`** (los convierte en
  rutas de Windows: `C:/Program Files/Git/...`). Exportar
  `MSYS_NO_PATHCONV=1` antes de verificar, o no empezar el formato con `/`.
- El check del escáner solo mira el content-type de la PORTADA: eso hace
  fácil el teatro (servir Markdown solo en `/`). No hacerlo: el valor real es
  que el agente lea barato TODAS las páginas; el generador cubre el sitio
  completo o no cumple su función.
- Si el HTML de una página se genera por JavaScript, el generador estático
  queda ciego: el `.md` de esa página se cura a mano (mismo criterio que el
  texto indexable en HTML plano).
- Los headers `x-markdown-tokens` / `x-original-tokens` del producto de
  Cloudflare son informativos; ningún check los exige. Omitirlos está bien.

## Implementación de referencia (verificada en producción)

kumocloud.cl, 2026-08-06: `scripts/generar_md.py` (17 páginas) +
`functions/_middleware.js` en el repo `kumo-cloud-web`. Verificado: agente
recibe `text/markdown` curado, humano recibe HTML, API y MCP intactos.
