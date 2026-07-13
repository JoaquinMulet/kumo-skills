# Kumo Skills

Repositorio canónico de las **Agent Skills** de Kumo. Fuente única de verdad: cualquier skill que la empresa use con Claude (en claude.ai, la API o Claude Code) vive primero acá, versionada en git, y desde acá se distribuye a las superficies correspondientes.

Documentación oficial de Anthropic (autoridad para todo lo no cubierto acá):

- Overview: https://docs.claude.com/en/agents-and-tools/agent-skills/overview
- Best practices: https://docs.claude.com/en/agents-and-tools/agent-skills/best-practices
- Enterprise governance: https://docs.claude.com/en/agents-and-tools/agent-skills/skills-for-enterprise

Este `CLAUDE.md` cubre **lo específico de Kumo**: decisiones de la casa, convenciones, checklist de review y proceso de distribución. Para mecánica general, leer los docs.

---

## Qué es una skill

Una carpeta con un `SKILL.md` que extiende las capacidades de Claude con conocimiento de dominio: workflows, contexto, mejores prácticas. Claude carga el `name` + `description` al iniciar y lee el cuerpo solo cuando detecta que aplica a la tarea (progressive disclosure).

## Estructura del repo

Una skill = una carpeta en el root del repo, nombrada igual que el campo `name` de su frontmatter.

```
kumo-skills/
├── CLAUDE.md                       # este archivo
├── LICENSE
├── README.md                       # instalación y uso
├── escritura-de-prompts/
│   └── SKILL.md
├── analisis-de-cartolas/
│   ├── SKILL.md
│   ├── reference/
│   │   ├── plan-de-cuentas.md
│   │   └── ejemplos.md
│   └── scripts/
│       └── validar_cuadre.py
└── ...
```

Reglas:

- **No anidar skills dentro de skills.**
- **No crear carpetas `shared/` ni `tools/` en el root.** Si un asset se reutiliza, vive duplicado en cada skill que lo necesita. Cada skill debe ser autosuficiente y portable (la persona que la instale en `~/.claude/skills/` solo copia esa carpeta).
- El nombre de la carpeta DEBE coincidir con el campo `name` del frontmatter.

## Anatomía mínima de una skill

```yaml
---
name: nombre-de-la-skill
description: Qué hace + cuándo usarla. Tercera persona. Máximo 1024 caracteres.
---

# Título

[Cuerpo de instrucciones, máximo 500 líneas]
```

Validaciones del frontmatter (las exige el runtime, no son opcionales):

- `name` — minúsculas, números y guiones únicamente; máximo 64 caracteres; sin las palabras `anthropic` o `claude`; idéntico al nombre de la carpeta.
- `description` — no vacío, **tercera persona** ("Procesa archivos Excel", nunca "Yo te ayudo con Excel"), debe incluir tanto QUÉ hace como CUÁNDO usarla.

## Convenciones de Kumo

### Naming

- **Skills de dominio interno** (procesos contables, financieros, operacionales de la empresa): español, sustantivo descriptivo o gerundio — `analisis-de-cartolas`, `calce-bancario`, `escritura-de-prompts`.
- **Skills genéricamente técnicas** (procesamiento de archivos, formatos estándar): inglés si la convención lo pide — `pdf-extraction`, `xlsx-formatting`.
- Prohibido: nombres vagos (`helper`, `utils`, `tools`, `documents`).

### Idioma

Una skill, un idioma. Si el `SKILL.md` está en español, los comentarios del código, los `reference/*.md` y los nombres de archivos descriptivos también van en español. Skills de Kumo orientadas al equipo interno → español por defecto.

### Descriptions

La `description` es el **único** criterio que Claude usa para elegir tu skill entre las decenas instaladas. Si es vaga, la skill no se invoca nunca o se invoca mal.

Patrón obligatorio:

1. Verbo de acción + objeto + dominio.
2. Disparadores explícitos: lista de términos que el usuario probablemente diga ("Usar cuando el usuario menciona X, Y, Z, o adjunta archivo tipo W").

**Buena:**
> `Calza el libro de banco con el libro diario y el registro de compra y ventas del mes. Usar cuando el usuario menciona cuadrar, conciliar, calce, cierre mensual, o adjunta cartola bancaria junto a libros contables.`

**Mala:**
> `Ayuda con contabilidad.`

### Cuerpo del SKILL.md

- **Máximo 500 líneas** en el `SKILL.md` principal. Si excede, splittear a archivos hermanos referenciados (`reference/<tema>.md`), no anidar más profundo.
- **Referencias a un solo nivel** desde `SKILL.md`. Nada de `SKILL.md → A.md → B.md → C.md` — Claude puede leer parcialmente los archivos anidados y perder contenido.
- **Asumir que Claude es inteligente.** No explicar qué es un PDF, qué es JSON, qué es un asiento contable. Solo aportar lo que Claude no puede inferir: vocabulario propio de Kumo, reglas del proceso, plantillas, datos.
- **Paths con forward slashes** (`scripts/validar.py`), nunca backslashes — el repo se usa en Windows y Linux.
- **Sin información con fecha de caducidad** en el flujo principal ("hasta agosto 2025..."). Cambios de versión van en una sección colapsada `## Patrones antiguos` al final.
- **Terminología consistente** dentro de una skill. Elegir un término y usarlo siempre (no mezclar "cuenta corriente" / "cuenta bancaria" / "CC" en el mismo documento).

### Scripts incluidos

Si la skill incluye scripts ejecutables:

- **Python con `uv`** (convención global de Kumo). Documentar el comando exacto: `uv run python scripts/foo.py <args>`. Nunca asumir que `pip` está instalado.
- **Manejo de errores explícito**: no devolver el problema al modelo con un `raise` desnudo. El script captura, imprime mensaje claro y o bien devuelve un default sensato o sale con código distinto de cero + mensaje accionable.
- **Constantes documentadas**, no magic numbers. Si hay un timeout de 30s, comentar por qué 30 y no 5.
- **Cabecera del script**: docstring inicial con qué espera, qué devuelve, ejemplo de uso.
- **Sin secretos hardcoded** (API keys, tokens, credenciales). Bloqueador automático en review.

### Decisión: ¿esto debería ser una skill o un prompt?

Una skill **vale la pena** cuando:

- El proceso se va a repetir muchas veces en muchas conversaciones.
- Tiene reglas, validaciones o vocabulario propio de Kumo que conviene codificar.
- Múltiples personas del equipo la van a invocar.

Una skill **no vale la pena** cuando:

- Es un prompt que vas a usar una o dos veces.
- Es contexto único de un proyecto específico (eso va en el `CLAUDE.md` del proyecto, no acá).
- Es algo que la propia inteligencia de Claude hace bien sin guía adicional.

Cuando duden, escribir el prompt directo primero. Si lo repiten tres veces, recién entonces convertirlo en skill.

## Checklist obligatorio antes de mergear

> **Gate automático (no confíes en la memoria).** Un pre-commit hook corre el validador
> (`scripts/validar-skills.py`) y **bloquea el commit** si algún `SKILL.md` tiene YAML de frontmatter
> inválido, `name` != carpeta o no-string, `description` vacía / no-string / > 1024 chars, > 500
> líneas, o voseo. **Parsea el YAML de verdad** (vía `uv run --with pyyaml`, con fallback a checks
> manuales) — no lo raspa con regex — porque el gate viejo aprobó una `description` con `: ` sin
> comillas que el cargador real rechazó, y antes una de 1086 chars por medir *después* de commitear.
> Cubre los puntos 1 y 6 de este checklist de forma mecánica. Actívalo una vez por clon:
> `git config core.hooksPath .githooks` (necesita `uv`, ya estándar en Kumo). Lo demás (2, 3, 5, 7)
> sigue siendo revisión humana.

Ningún PR se mergea sin completar esto en la descripción:

1. **Frontmatter válido** — `name` coincide con la carpeta, `description` en tercera persona con QUÉ + CUÁNDO, dentro de los límites de caracteres. *(El gate lo verifica.)*
2. **Test de descubrimiento** — el autor probó la skill con **al menos 3 prompts representativos** y Claude la invocó cuando correspondía (y NO la invocó en un cuarto prompt no relacionado). Pegar los prompts y los resultados en el PR.
3. **Coexistencia** — la nueva skill no canibaliza disparadores de skills ya existentes en el repo. Si dos skills compiten por los mismos prompts, decidir en el PR: fusionar, o angostar una de las dos descriptions.
4. **Seguridad** — si la skill incluye scripts ejecutables, llamadas de red, lectura de archivos fuera de su carpeta, o referencias a servidores MCP, justificarlo explícitamente. Secretos hardcoded = bloqueador.
5. **Autocontenida** — la carpeta de la skill funciona si se copia sola a `~/.claude/skills/`. No depende de archivos del root del repo ni de ASSETS de otras skills (scripts, `reference/`). Referenciar OTRA skill por su nombre («ver `desarrollo-riguroso`») sí está permitido — esa dependencia se resuelve en runtime invocando la otra skill, no copiando archivos — pero entonces rige la **regla de la ruta de lectura**: si el flujo de la skill REQUIERE contenido de la otra, debe ORDENAR su lectura en el punto donde la necesita (un puntero que nadie sigue es letra muerta).
6. **Idioma consistente** — todo en un mismo idioma a lo largo del `SKILL.md` y archivos referenciados.
7. **Lectura rápida** — alguien que abre el `SKILL.md` por primera vez entiende qué hace y cuándo usarla en menos de un minuto.

## Distribución a las superficies de Claude

**Las superficies NO sincronizan skills entre sí.** El repo es la fuente; cada superficie se actualiza manualmente cuando hay cambios.

| Superficie | Cómo instalar una skill del repo |
|---|---|
| **Claude Code** | Copiar la carpeta de la skill a `~/.claude/skills/<nombre>/` (personal del usuario) o `.claude/skills/<nombre>/` (compartida con un proyecto específico). |
| **claude.ai** (Pro/Max/Team/Enterprise) | Comprimir la carpeta de la skill en `.zip`, subir en Settings → Features → Skills. Por usuario, no se comparte org-wide automáticamente. |
| **Claude API** | Subir vía endpoint `/v1/skills` con los headers beta `code-execution-2025-08-25`, `skills-2025-10-02`, `files-api-2025-04-14`. Workspace-wide. Referenciar el `skill_id` retornado en cada request. |

Detalles oficiales y limitaciones: ver el bloque "Where Skills work" del overview de Anthropic.

## Versionado

- Una skill = una carpeta = un `SKILL.md`. **El versionado lo da git**, no campos internos.
- Cambios que rompan disparadores existentes (rename del `name`, cambio fuerte de `description`, eliminación de scripts referenciados) → commit separado con mensaje prefijado `BREAKING: <skill> — <qué cambió>` y aviso al canal correspondiente antes de pushear.
- Skills ya distribuidas a claude.ai o la API **no se actualizan solas**: hay que resubir/redesplegar manualmente tras el merge.
- Para deprecar una skill: moverla a una carpeta `_deprecated/` en el root durante un ciclo de release antes de borrar.

## Cuando Claude trabaje en este repo

Si una instancia de Claude (Code u otra) edita o crea una skill acá:

1. Antes de tocar nada, leer el `SKILL.md` afectado **completo** y el frontmatter de las skills vecinas (para detectar overlap de disparadores).
2. Para crear una skill nueva desde cero, invocar la skill `skill-creator` (o `create-agent-skills`) si está disponible en la instalación — son metaskills oficiales de Anthropic justo para esto.
3. Tras cualquier cambio en `name` o `description`, recorrer el checklist de "Antes de mergear" punto por punto antes de declarar la skill lista.
4. **No mezclar cambios a múltiples skills en un solo commit.** Una skill, un commit (o una serie de commits sobre la misma skill).
5. Si el cambio toca el flujo de descubrimiento (frontmatter), correr los 3 prompts del test de descubrimiento antes de commitear y dejarlos registrados.
6. **Si editas un `SKILL.md`, revisa en la misma pasada sus assets (`reference/`, `scripts/`).** Son nodos del mismo grafo y quedan desactualizados en silencio: una enumeración en el SKILL.md que describe la plantilla, un ejemplo que contradice la instrucción nueva. *(Caso real: la plantilla de CLAUDE.md quedó atrás de dos evoluciones de la skill — la enumeración de secciones y el gate de claims — hasta que el usuario lo notó, no el aparato.)*

## Cuando Claude edite una skill INSTALADA (desde otro proyecto): el ciclo completo

El caso típico: una retrospectiva u otra sesión que trabaja en OTRO proyecto quiere mejorar una skill que está en `~/.claude/skills/`. Esa carpeta es la **copia instalada** — no tiene `.git`, y que no sea un repo NO significa que no exista el repo. La fuente única de verdad es este repo (`github.com/JoaquinMulet/kumo-skills`; localizar el clon en el disco o clonarlo).

El ciclo, en orden — saltarse un paso crea **drift bidireccional silencioso** que nadie ve hasta que las dos versiones divergen en direcciones opuestas:

1. **`diff` ANTES de editar** — la copia instalada contra la del repo. El drift puede preexistir **en ambas direcciones** (lecciones que quedaron solo en la instalada; mejoras commiteadas que nunca se re-distribuyeron). Si lo hay, el punto de partida es el **merge (unión)** de ambos lados, nunca una copia ciega en ninguna dirección.
2. **Editar y commitear en el repo** — con las reglas de la sección anterior (una skill, un commit; gate verde).
3. **Copiar al instalado en el mismo acto** — y verificar que el `diff` quedó vacío. (En máquinas con `core.hooksPath` configurado, el hook `post-commit` hace esta copia automáticamente al commitear, con guardia: si la instalada tenía ediciones no portadas, avisa por stderr y NO la pisa. Verifica igual el diff final: el hook cubre la dirección repo→instalada, no la inversa.)
4. **Push** — las skills distribuidas no se actualizan solas; un commit sin push es drift en potencia para el resto de las máquinas.

*(Caso real que originó esta sección, 12-jul-2026: la copia instalada de `desarrollo-riguroso` acumuló cinco lecciones de retros que nunca llegaron al repo, mientras el repo recibió una mejora que nunca llegó a la copia — lo descubrió el usuario preguntando, no el sistema.)*

Las skills que instruyen editar skills (`retrospectiva-de-sesion`, `desarrollo-riguroso`) **referencian esta sección** en lugar de duplicar el procedimiento: el procedimiento vive en un solo lugar, que es este.
