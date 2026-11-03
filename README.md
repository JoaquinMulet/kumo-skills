# Kumo Skills

Biblioteca canónica de **Agent Skills** de Kumo para Claude.

Una skill es una carpeta con un `SKILL.md` que le enseña a Claude un procedimiento. Las de este repo
son de 2 orígenes. Las de Kumo traen lo que es propio de la empresa (finanzas chilenas, documentos
LaTeX, sitios web, las reglas de Joaquín). Las de pstack, de Lauren Tan (licencia MIT, copiadas el
3 de noviembre de 2026 desde `github.com/cursor/plugins`), traen los principios de ingeniería.

La decisión que ordena el repo desde esa fecha es de Joaquín. Un trabajo queda bien hecho cuando una
comprobación automática lo demuestra. Por eso las skills que dependían de agentes que revisan a otros
agentes se retiraron a [`_deprecated/`](_deprecated/), y lo que valía de ellas pasó a scripts.

Para la gobernanza interna (cómo agregar una skill, convenciones, checklist antes de mergear), ver
[CLAUDE.md](CLAUDE.md).

## Skills de Kumo

| Skill | Qué hace |
|---|---|
| [`desarrollo-riguroso`](desarrollo-riguroso/) | La portada del estándar de desarrollo. Dice qué skill de pstack leer en cada situación de código y agrega las reglas propias de Kumo. Un hook obliga a leerla al abrir cada sesión. |
| [`verificacion-adversarial`](verificacion-adversarial/) | Comprueba cada cifra y cita de un texto que se publica, con un script que busca la frase en el archivo de la fuente primaria. |
| [`doc-prueba-de-uso`](doc-prueba-de-uso/) | Prueba un documento haciendo la tarea. Un lector frío ejecuta lo que la sección habilita y se califica contra una pauta previa. Trae un script que falla si un término se usa antes de explicarse. |
| [`unslop`](unslop/) | Quita las marcas de texto de IA, en español de Chile y con las reglas de prosa de Joaquín. |
| [`analisis-de-empresas`](analisis-de-empresas/) | La puerta de gobernanza y las 70 preguntas a los estados financieros, con un validador del anexo. |
| [`documentos-latex`](documentos-latex/) | Documentos LaTeX con calidad editorial, con geometría medida, gráficos de ECharts y cada cifra contra su fuente. |
| [`aeo-sitios-web`](aeo-sitios-web/) | Deja un sitio listo para agentes y búsqueda por IA, verificado con curl y con el puntaje de isitagentready. |

## Skills de pstack

No se cargan solas (llevan `disable-model-invocation: true`). Las nombra la tabla de
`desarrollo-riguroso`, y Claude las lee con `Read` cuando la situación lo pide.

| Skill | Cuándo |
|---|---|
| [`principle-prove-it-works`](principle-prove-it-works/) | Antes de decir «listo». |
| [`principle-encode-lessons-in-structure`](principle-encode-lessons-in-structure/) | Una corrección se repite. Se vuelve lint, hook, script o prueba. |
| [`principle-fix-root-causes`](principle-fix-root-causes/) | Al depurar. |
| [`principle-attack-the-premise`](principle-attack-the-premise/) | 2 arreglos con la misma premisa fallaron. |
| [`principle-model-the-domain`](principle-model-the-domain/) | Código con estado o con muchas ramas. |
| [`principle-type-system-discipline`](principle-type-system-discipline/) | Al diseñar tipos. |
| [`principle-boundary-discipline`](principle-boundary-discipline/) | Validación y errores en los bordes del sistema. |
| [`principle-test-behavior-not-implementation`](principle-test-behavior-not-implementation/) | Al escribir o conservar un test. |
| [`principle-build-the-lever`](principle-build-the-lever/) | Trabajo no trivial. Se construye el script que lo hace o lo prueba. |
| [`principle-sequence-verifiable-units`](principle-sequence-verifiable-units/) | Trabajo de varios pasos. |
| [`principle-make-operations-idempotent`](principle-make-operations-idempotent/) | Un proceso que puede correr 2 veces o cortarse. |
| [`principle-explain-the-number`](principle-explain-the-number/) | Antes de reportar un número medido. |
| [`principle-subtract-before-you-add`](principle-subtract-before-you-add/) | Antes de agregar a un sistema que existe. |
| [`tdd`](tdd/) | Un bug con un test barato. |
| [`correct`](correct/) | El usuario corrigió algo. Reemplaza a la antigua retrospectiva. |
| [`create-verification-skill`](create-verification-skill/) | El proyecto no tiene un script que maneje la app real y junte evidencia. |
| [`maintain-verification-skill`](maintain-verification-skill/) | La app cambió y el script de verificación puede estar atrasado. |
| [`create-formal-verification-skill`](create-formal-verification-skill/) | Código donde un error cuesta caro y los tests no llegan. |
| [`maintain-formal-verification-skill`](maintain-formal-verification-skill/) | El código verificado cambió. |
| [`statechart`](statechart/) | Revisar un modelo TLA+ y dibujarlo como diagrama de estados. Baja Java y TLC con mise la 1.ª vez. |
| [`blast-radius`](blast-radius/) | Qué puede romper un cambio fuera del diff. |
| [`interrogate`](interrogate/) | Revisión de un cambio donde cada hallazgo trae su corrida. |
| [`technical-writing`](technical-writing/) | Documentos, README y mensajes de commit. |
| [`show-me-your-work`](show-me-your-work/) | Bitácora de decisiones de un trabajo largo sin supervisión. |

Cada carpeta copiada de pstack lleva su `LICENSE`. Antes de seguir una de estas skills en Claude
Code, la tabla de traducción de nombres está en
[`desarrollo-riguroso/reference/pstack-en-claude-code.md`](desarrollo-riguroso/reference/pstack-en-claude-code.md).

## Los hooks. La mitad que hace cumplir lo que las skills dicen

Una skill es texto, y el texto lo aplica quien se acuerda de leerlo. Este repo trae ademas
los **disparadores** que convierten 2 de sus reglas en algo que ocurre solo, y sin ellos
esas 2 reglas quedan a merced de que el modelo decida aplicarlas.

Viven en [`hooks/`](hooks/) y se instalan con un comando.

```bash
node hooks/instalar.mjs
```

El instalador mezcla los hooks en tu `~/.claude/settings.json` **sin pisar lo que ya
tengas**, deja un respaldo antes de tocar nada, y usa las rutas de TU clon para que
funcione desde donde lo hayas puesto. `--listar` dice que haria sin escribir, y `--quitar`
los saca.

| Hook | Cuando corre | Que hace |
|---|---|---|
| `recordar-estandar.mjs` | al abrir la sesion | Inyecta el contrato de lectura de `desarrollo-riguroso` antes de que el agente toque nada. No bloquea, porque `SessionStart` no puede. |
| `exigir-higiene.mjs` | antes de cada `git commit` o `git push` | **Niega** la herramienta si el repo no tiene su aparato de higiene instalado. |
| `revisar-respuesta.mjs` | al terminar cada respuesta | Devuelve la respuesta al agente si un bloque de shell trae `&&`, un hueco como `<id>`, un `Read-Host` u `Out-File -Encoding utf8`, o si la prosa trae voseo o raya. Se prueba con `node hooks/probar-revisar-respuesta.mjs`. |

### Por que el segundo bloquea, y como se sale de el

La skill `desarrollo-riguroso` dice de si misma que **nada existe hasta que algo lo
dispara**. Su seccion de higiene son 7 pasos que hay que aplicar en cada repo, y escribirlos
mas grande no hace que se apliquen. El hook los vuelve obligatorios en el unico momento que
importa, cuando vas a registrar o publicar un cambio.

Lo que mide es concreto. que el repo tenga una carpeta de hooks **versionada** con un
`pre-commit` adentro, activada con `git config core.hooksPath <carpeta>`. Si no la tiene, el
commit no ocurre y el mensaje dice que leer y que hacer.

Un guardia sin salida explicita no protege, bloquea. Hay 2 salidas.

- Un archivo `.kumo-sin-higiene` en la raiz del repo **con la razon escrita adentro**. Vacio
  no sirve, porque la razon es el punto. Esta es la buena, porque deja la decision en el
  repo y con nombre.
- La variable `KUMO_SIN_HIGIENE=1` para una vez, sin dejar rastro.

El hook se prueba solo, en las 2 direcciones, que es lo unico que lo hace valer.

```bash
node hooks/probar-exigir-higiene.mjs
```

Son 9 casos. que bloquee el commit y el push en un repo sin higiene, que NO estorbe cuando
la higiene esta, cuando el comando no es un commit, cuando la herramienta no es Bash, cuando
la carpeta no es un repo, y que las 2 salidas de emergencia funcionen, incluida la de que
una excusa vacia no sirve.

### El contrato de lectura

La otra regla que los hooks hacen cumplir es que `desarrollo-riguroso` **se lee completa**.

Su declaracion vive en la `description` del frontmatter, no en el cuerpo, y la razon
importa. La `description` es lo unico que llega entero y sin truncar antes de que el modelo
decida nada. Ahi dice que el archivo termina con el marcador `FIN-DESARROLLO-RIGUROSO`, asi
que si el agente no lo vio, su lectura quedo cortada y tiene que seguir leyendo con `Read`
antes de actuar.

Media skill es peor que ninguna, porque da la sensacion de haberla consultado.

Y el contrato no es una promesa. `scripts/centinelas.py` comprueba que la declaracion y el
marcador existan los 2, y corre en el `pre-commit` de este repo. Si alguien borra uno, el
commit se bloquea.

## Instalación

Las skills se instalan **distinto en cada superficie de Claude**, y no se sincronizan automáticamente entre ellas. Si usas Claude en varios lugares, hay que instalar en cada uno.

### Claude Code

Las skills viven en el filesystem como carpetas. Claude Code las descubre automáticamente al iniciar una sesión.

**Instalación personal** (disponible en todos tus proyectos):

```bash
git clone https://github.com/JoaquinMulet/kumo-skills.git
cp -r kumo-skills/desarrollo-riguroso ~/.claude/skills/
```

**Instalación a nivel proyecto** (compartida con quien clone ese repo):

```bash
cp -r kumo-skills/desarrollo-riguroso /ruta/al/proyecto/.claude/skills/
```

En Windows con PowerShell:

```powershell
git clone https://github.com/JoaquinMulet/kumo-skills.git
Copy-Item -Recurse kumo-skills/desarrollo-riguroso $HOME/.claude/skills/
```

Si la carpeta `~/.claude/skills/` no existe, créala antes. Reiniciar la sesión de Claude Code para que la nueva skill aparezca.

**Cuál de las dos elegir.** La personal (`~/.claude/skills/`) vive en tu equipo. La ves tú en
todos tus proyectos y nadie más. La de proyecto (`<proyecto>/.claude/skills/`) se commitea junto
al código. La ve cualquiera que clone ese repo, y solo dentro de él. Regla práctica: las skills
transversales de Kumo van en la personal. Una skill que solo tiene sentido en un proyecto
concreto va en la de ese proyecto.

### claude.ai (Pro / Max / Team / Enterprise)

Requiere code execution habilitado en tu cuenta.

1. Descarga la carpeta de la skill desde GitHub (por ejemplo `desarrollo-riguroso/`).
2. Comprímela en un archivo `.zip`.
3. En claude.ai: **Settings → Features → Skills → Upload**.

Las skills en claude.ai son **por usuario**: cada miembro del equipo las sube a su propia cuenta. No hay distribución central org-wide.

### Claude API

Las skills se suben con el endpoint `POST /v1/skills`. Requiere tres headers beta:

- `code-execution-2025-08-25`
- `skills-2025-10-02`
- `files-api-2025-04-14`

Una vez subida, referencia el `skill_id` retornado en el parámetro `container` de tu request, junto al tool de code execution. Detalles y ejemplos en la [documentación oficial de Anthropic](https://docs.claude.com/en/build-with-claude/skills-guide).

Las skills subidas vía API son **workspace-wide**: todos los miembros del workspace pueden usarlas.

## Cómo se invocan

Una vez instalada, no hay que invocar la skill explícitamente. Pídele a Claude la tarea en lenguaje natural y, si la `description` de la skill calza con la petición, Claude la usa solo. Por ejemplo, con `desarrollo-riguroso` instalada basta con pedir «arregla este bug» o «escribe
el test primero». Las skills de pstack son la excepción, porque no se cargan solas. Las
nombra la portada de `desarrollo-riguroso`, o tú con su nombre.

## Contribuir

Antes de proponer una skill nueva o modificar una existente, leer [CLAUDE.md](CLAUDE.md). Cubre estructura mínima de una skill, convenciones de Kumo (naming, idioma, descriptions efectivas), cuándo vale la pena hacer skill vs solo prompt, y el checklist de review obligatorio antes de mergear cualquier PR.

## Licencia

[MIT](LICENSE).
