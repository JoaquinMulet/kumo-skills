# Plantilla de CLAUDE.md — el esqueleto probado

El `CLAUDE.md` es el **manual operativo** del proyecto para cualquier agente o dev que llegue: no un ensayo sobre desarrollo, sino instrucciones densas y accionables. Esta es la columna vertebral que usa Kumo (derivada de CLAUDE.md que funcionan en producción). Cópiala en la raíz del repo y **rellena cada sección con lo REAL del proyecto** — comandos que se pueden pegar, nombres de archivos que existen, reglas que se cumplen.

## Reglas de densidad y voz (lo que separa un buen CLAUDE.md de uno genérico)

- **Comandos EXACTOS, no genéricos.** `pnpm --filter web test src/foo.test.ts`, no "corre los tests". Con sus flags y su gotcha si lo tiene (`# NUNCA uses X directo — no incluye tu build`).
- **Nombres reales.** Rutas, funciones, tablas, cuentas que existen (`packages/db/repository.ts::calzarPagos`), no "el módulo de datos".
- **Reglas duras marcadas.** `NUNCA`, `SIEMPRE`, `CRÍTICO`, `OBLIGATORIO` — el lector tiene que distinguir una convención de una ley.
- **Cero relleno filosófico.** La filosofía general (TDD, honestidad) vive en el estándar `desarrollo-riguroso`; el `CLAUDE.md` la **aterriza** con los comandos y decisiones de ESTE proyecto. No repitas el estándar; concrétalo.
- **Marca lo inventado.** Todo default que asumas sin confirmar (un puerto, un TTL, un nombre de tabla) va con `⚠️ confirmar` — para que nadie lo tome como verdad.
- **Describe el estado ACTUAL, no la historia.** La historia vive en git. Nada de "antes era X"; el código es ground truth (no narres cómo funciona el código, se desactualiza y miente).

## Esqueleto (secciones en orden)

```markdown
# <Proyecto> — CLAUDE.md

> ⚠️ **LEE ESTE ARCHIVO COMPLETO ANTES DE ACTUAR.** Crece con cada sesión (efecto compounding)
> y puede exceder el límite de una sola lectura: **si tu Read se trunca, continúa con `offset=`
> hasta el final.** No respondas ni actúes desde una página parcial.

Guía operativa del repo. Describe el estado ACTUAL del sistema, no su historia.

**Estándar de la casa (OBLIGATORIO):** este proyecto sigue la skill `desarrollo-riguroso` —
LÉELA antes de escribir o corregir código o diseñar tests: este archivo la CONCRETA, no la
repite, y sus términos (IDENTIFY→VERIFY-REAL, preflight, oráculo duro/blando, trunk) vienen
definidos allá. Al cerrar una sesión sustantiva, corre `retrospectiva-de-sesion`.

## Qué es esto
<Una o dos frases: qué hace el proyecto y para quién.> Más las FUENTES DE DATOS y
dependencias externas (DB, APIs, servicios) con cómo se accede a cada una.

## Build & comandos
Comandos EXACTOS del stack (pegar-y-correr), cada uno con su gotcha si lo tiene:
- build: `<cmd>`
- dev / correr local: `<cmd>` (+ variables de entorno necesarias)
- test (suite): `<cmd>`
- correr UN test: `<cmd -run/-t/--filter ...>`
- **preflight** (checks pre-commit que NINGÚN commit saltea): `<cmd>` — lista qué
  corre (formato, lint, tipos, tests, build) y en qué orden; si uno falla, no se commitea.

## Ramas y deploy
Cuál es el TRUNK (la rama viva = la que se despliega) y cómo se despliega — arriba y explícito,
porque si no está escrito, el trabajo deriva a la rama activa por default:
- trunk: `<rama>` — commitea y branchea desde acá; ramas cortas que mergean al trunk cuando están verdes.
- deploy a prod: `<cmd>` — se corre SIEMPRE desde el trunk. Di si el mecanismo empaqueta el
  working tree o un ref git; si es lo primero, prod == la rama en que estás parado (incluso sin commitear).
- ⚠️ Si el flujo multi-rama/CI todavía es FUTURO, dilo como futuro; documenta el flujo MANUAL de HOY.

## Arquitectura
Estructura de carpetas/módulos con QUÉ hace cada uno (una línea por módulo). El
lector debe saber dónde vive cada cosa sin abrir el código.
- `<ruta/>` — <responsabilidad>
- ...

## Invariantes de dominio y oráculo de verdad
Las verdades que el código NUNCA debe violar (reglas de negocio, unidades, límites),
en reglas duras. Y **cuál es el oráculo de verdad** del proyecto:
- ORÁCULO: <duro (test suite/spec/estándar bit-exacto → espejar fiel) | blando (humano/
  sistema legado que se atrasa → espejar pero nombrar residuales cuando la realidad difiere)>.

## Bug-fix workflow (6 pasos, con los comandos de este stack)
1. IDENTIFY — <cómo se nombra el bug acá>.
2. REPLICATE con la forma de los datos REALES — <casos borde propios del dominio>.
3. FAILING TEST — `<cmd para correr el test y verlo fallar>`.
4. FIX — cambio mínimo.
5. CONFIRM — test verde + `<cmd preflight>`.
6. VERIFY-REAL — <para detectores/reconciliadores/lo que compara contra el oráculo:
   cómo se confronta contra datos reales ANTES de desplegar>.

## Testing
Dónde viven los tests (`<convención>`), cómo se escriben, y cómo se prueba que un
test falla por la RAZÓN correcta (borrar la cláusula portante del fix debe romper un test).

## Patterns to Follow
Patrones propios del proyecto (no los del estándar general): decisiones de diseño,
convenciones de datos, "esto se hace así acá y por qué". 3-8 items, concretos.

## Lessons Learned
Arranca casi vacía en un proyecto nuevo; se llena con `retrospectiva-de-sesion` tras
cada sesión. Formato de cada entrada: **qué falló → causa raíz → prescripción accionable**.
(Semilla: "— (aún sin lecciones; se agregan tras la primera sesión sustantiva)".)

## Gotchas / Known pending issues
Lo no obvio que muerde: cosas frágiles, deuda conocida, trampas del stack/entorno.

## Deploy
Cómo se despliega, a dónde, con qué comando, y qué verificar después.
```

## Ejemplo trabajado (una sección bien rellenada)

Así se ve **"Build & comandos"** con densidad real (proyecto Go de ejemplo) — nota los comandos exactos, el gotcha marcado, y el preflight explícito:

```markdown
## Build & comandos
- build: `go build -o bin/api ./cmd/api`
- dev: `DATABASE_URL=... REDIS_URL=... go run ./cmd/api` (puerto 8080 ⚠️ confirmar)
- test (suite): `go test ./...`
- correr UN test: `go test -run TestResolveSlug ./internal/resolve`
- **preflight** (ningún commit lo salta; si uno falla, no commitear):
  `go fmt ./... && go vet ./... && go test ./... && go build -o /dev/null ./...`
  # NUNCA commitear con `go test` fallando ni con `go vet` en rojo.
```

Compara con la versión genérica que NO sirve: *"Compila con Go. Corre los tests. Formatea el código."* — no se puede pegar, no dice qué comando, no marca la ley. Esa es la diferencia entre un CLAUDE.md que habilita y uno que solo suena bien.

## Cómo se valida que un CLAUDE.md quedó bien

Un CLAUDE.md es un documento de información, y **los documentos se testean** (ver la sección "Los documentos también se testean" del `SKILL.md`): pásaselo a un lector frío débil con una tarea real ("con SOLO este archivo, levanta el proyecto y corre un test") y mira si puede ejecutarla. Lo que tuvo que adivinar es lo que falta concretar.
