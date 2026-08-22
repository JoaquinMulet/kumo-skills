# Kumo Skills

Biblioteca canónica de **Agent Skills** de Kumo para Claude.

Las skills extienden las capacidades de Claude con conocimiento de dominio: workflows, contexto, plantillas, mejores prácticas. Cuando Claude detecta que una skill aplica a la tarea que le pediste, la carga automáticamente y la aplica. Acá viven las que usa Kumo, versionadas en git.

Para detalles de gobernanza interna (cómo agregar una skill, convenciones de naming, checklist de review antes de mergear), ver [CLAUDE.md](CLAUDE.md).

## Skills disponibles

| Skill | Qué hace |
|---|---|
| [`desarrollo-riguroso`](desarrollo-riguroso/) | El estándar de desarrollo de Kumo para cualquier proyecto: TDD, verificación contra datos reales, prevención sistémica de bugs, observabilidad y honestidad. Se siembra en el `CLAUDE.md` de cada proyecto. |
| [`retrospectiva-de-sesion`](retrospectiva-de-sesion/) | Ritual de cierre de una sesión de código: destila las correcciones en aprendizajes y los compone en el `CLAUDE.md` del proyecto (lo específico) y en `desarrollo-riguroso` (lo universal). |
| [`escritura-de-prompts`](escritura-de-prompts/) | Metodología para escribir, mejorar, auditar o diagnosticar prompts dirigidos a Claude. |
| [`doc-completitud`](doc-completitud/) | **Pipeline de calidad documental, paso 1.** Endurece un texto hasta que un lector frío pueda explicar cada sección sin vacíos (que no falte nada). |
| [`doc-cadena-causal`](doc-cadena-causal/) | **Pipeline documental, paso 2.** Audita que cada concepto se sostenga solo: por qué existe, quién lo hace, de dónde sale su número, qué pasaría sin él (que cada cosa tenga fundamento). |
| [`doc-narrativa`](doc-narrativa/) | **Pipeline documental, paso 3.** Reestructura un texto denso en un relato claro, sin perder contenido (que se lea bien). |
| [`doc-prueba-de-uso`](doc-prueba-de-uso/) | **Pipeline documental, paso 4.** Valida que un lector frío débil pueda EJECUTAR la tarea que el texto habilita (que sirva para hacer, no solo para entender). |
| [`unslop`](unslop/) | **Pipeline documental, paso 5 y último.** Quita las marcas que delatan que un texto lo escribió una IA y le devuelve voz: relleno, vocabulario inflado, puntuación de muleta, voz pasiva y metáforas que tapan la palabra concreta. |
| [`auditoria-de-realidad`](auditoria-de-realidad/) | Un agente fresco y escéptico hurga el estado REAL (repo, git, deploy, secretos, código) con pregunta abierta. Caza lo que el propio aparato no está viendo. El complemento abierto de VERIFY-REAL. |
| [`verificacion-adversarial`](verificacion-adversarial/) | Aduana de hechos para un texto que se publica: buscadores reúnen evidencia y refutadores independientes intentan destruirla. El producto es un veredicto por afirmación, no un informe nuevo. |
| [`agents-sdk`](agents-sdk/) | Conocimiento técnico versionado del Cloudflare Agents SDK: tabla de retrieval a las docs oficiales (verificada URL por URL), harness Think, MCP, workflows, estado. Sesga a Claude a leer las docs actuales en vez de su pre-entrenamiento. |
| [`aeo-sitios-web`](aeo-sitios-web/) | El playbook para dejar un sitio web listo para la era agéntica y la búsqueda por IA (SEO/AEO): acceso de crawlers, descubrimiento, Markdown de origen sin plan Pro, y puerta MCP con confirmación humana. Con verificación mecánica por nivel. |
| [`gobernanza-primero`](gobernanza-primero/) | La puerta que corre ANTES de cualquier analisis de una empresa: si los incentivos estan mal, la historia de asignacion de capital ya predice el futuro y no hay para que seguir. |
| [`checklist-lehman`](checklist-lehman/) | Las 70 preguntas que hay que hacerle a unos estados financieros, derivadas del 10-K de Lehman 2007 anotado por Buffett. Pasada obligatoria de todo informe de analisis de empresa. |

### El mapa. Por qué existe cada skill

Las catorce responden seis preguntas distintas. Cada nombre dice su propósito, no su mecanismo.

- **Cómo desarrollamos, y cómo mejora ese cómo.** `desarrollo-riguroso` es la constitución de ingeniería de Kumo, siembra el `CLAUDE.md` de cualquier proyecto nuevo; `retrospectiva-de-sesion` es cómo se enmienda, convierte cada sesión de código en aprendizaje durable (lo específico va al proyecto, lo universal al estándar).
- **Cómo hacemos que un texto sirva.** El pipeline de calidad documental (detalle abajo): `doc-completitud` → `doc-cadena-causal` → `doc-narrativa` → `doc-prueba-de-uso` → `unslop`. Existe porque un documento puede estar completo, leerse bien, y aun así ser inútil para actuar. Y el paso 5 existe porque puede además ser útil y sonar a máquina, que es lo primero que un lector nota y lo último que las otras cuatro miran.
- **Cómo le hablamos al modelo.** `escritura-de-prompts`, el modelo está fijo. El prompt es la única palanca real, así que el prompting se vuelve método.
- **Cómo confrontamos la realidad.** `auditoria-de-realidad` (sobre un proyecto: repo, deploy, secretos) y `verificacion-adversarial` (sobre un texto que se publica: cifras, citas, afirmaciones). Existen porque todo nuestro propio aparato de validación comparte nuestros puntos ciegos. Solo un contexto sin nuestro contexto encuentra lo que no sabíamos buscar.
- **Cómo analizamos una empresa.** `gobernanza-primero` corre primero y es una PUERTA, no un capítulo. Si los incentivos están mal, la historia de asignación de capital es la mejor predicción del futuro y el resto del análisis sobra. Recién después entra `checklist-lehman`, las 70 preguntas que se le hacen a los estados financieros. Existen en ese orden porque leer bien unos números malos no sirve de nada.
- **Con qué construimos agentes.** `agents-sdk`, conocimiento técnico de una plataforma que cambia más rápido que el pre-entrenamiento del modelo. Su valor no es explicar el SDK sino apuntar a las docs vivas: cada URL de su tabla se verificó con una petición real antes de escribirse. Y `aeo-sitios-web`, el playbook para que cualquier sitio nuestro o de un cliente quede listo para la era agéntica (SEO/AEO): nació de la implementación verificada en kumocloud.cl (21→36 puntos el 2026-08-06).

### El ciclo. Lo único que hay que entender el primer día

Kumo no guarda su experiencia en la cabeza de nadie: la guarda en dos archivos que se
alimentan entre sí. **El estándar de la casa** dice cómo se trabaja en cualquier proyecto. **El
manual de un proyecto** dice cómo se trabaja en ese proyecto en particular. Cada vez que
cierras una sesión de trabajo, lo que aprendiste se reparte entre esos dos según a quién le
sirva. Sigue las flechas numeradas:

```mermaid
flowchart TD
  EST["EL ESTANDAR DE LA CASA<br/>como trabaja Kumo en cualquier proyecto<br/>(la skill desarrollo-riguroso)"]
  MAN["EL MANUAL DE ESTE PROYECTO<br/>sus comandos, sus reglas, sus tropiezos<br/>(el archivo CLAUDE.md del proyecto)"]
  TRA["TU, TRABAJANDO<br/>codigo, documentos, informes"]
  RET["EL CIERRE DE LA SESION<br/>que me corrigieron hoy, y por que<br/>(la skill retrospectiva-de-sesion)"]

  DEC{"4. cada leccion va a UN solo lado:<br/>sirve solo en este proyecto,<br/>o en cualquier proyecto?"}

  EST -->|"1. al empezar un proyecto, le escribe su manual"| MAN
  MAN -->|"2. te dice como se trabaja aca"| TRA
  TRA -->|"3. al terminar"| RET
  RET --> DEC
  DEC -->|"solo en este proyecto"| MAN
  DEC -->|"en cualquier proyecto"| EST
```

En una frase: **el estándar escribe el manual del proyecto, el manual guía el trabajo, y el
cierre de cada sesión devuelve lo aprendido a uno de los dos.** Por eso el próximo proyecto de
Kumo arranca sabiendo lo que este aprendió a los golpes, sin que nadie tenga que acordarse.

Quién hace cada flecha, en concreto: las cuatro las ejecuta **Claude**, no un humano con una
plantilla. En el paso 1 le pides empezar un proyecto, Claude carga la skill `desarrollo-riguroso`
y escribe el `CLAUDE.md` de ese proyecto siguiendo
[la plantilla del repo](desarrollo-riguroso/reference/plantilla-claude-md.md), comandos exactos
del stack, reglas del dominio, y una sección de lecciones que arranca casi vacía. En el paso 3
le pides cerrar la sesión y Claude carga `retrospectiva-de-sesion`, que es la que reparte. Tú
apruebas y corriges. El trabajo mecánico no es tuyo.

### Las otras diez. Herramientas para momentos concretos del paso 3

No son parte del ciclo. Son las que se invocan **mientras trabajas**, cuando aparece una de
estas diez situaciones.

| Cuando te pasa esto… | …se usa esta skill |
|---|---|
| Escribiste un documento y no sabes si a otro le va a faltar contexto | [`doc-completitud`](doc-completitud/) |
| Un lector razona bien sobre tu texto y llega a un "¿y esto de dónde salió?" sin respuesta | [`doc-cadena-causal`](doc-cadena-causal/) |
| El documento no le falta nada, pero es un muro de tablas y listas que cuesta leer | [`doc-narrativa`](doc-narrativa/) |
| El documento se lee bien, pero quien tiene que **hacer algo** con él no puede | [`doc-prueba-de-uso`](doc-prueba-de-uso/) |
| Un informe con cifras se va a enviar a un cliente y no quieres publicar un dato falso | [`verificacion-adversarial`](verificacion-adversarial/) |
| Heredaste un proyecto, o sospechas que hay algo grave que nadie está viendo | [`auditoria-de-realidad`](auditoria-de-realidad/) |
| Le pediste algo a Claude y te respondió cualquier cosa | [`escritura-de-prompts`](escritura-de-prompts/) |
| Vas a empezar a analizar una empresa y quieres saber si vale la pena | [`gobernanza-primero`](gobernanza-primero/) |
| Tienes al frente unos estados financieros y no sabes qué preguntarles | [`checklist-lehman`](checklist-lehman/) |
| Un texto está correcto y aun así suena a IA | [`unslop`](unslop/) |

### Pipeline de calidad documental. Los textos también se testean

No solo el código se testea. Un `CLAUDE.md`, una skill o un spec pueden "leerse bien" y ser inútiles, *un artefacto que pasa un control de coherencia todavía puede fallar en su propósito*. Kumo endurece cualquier texto de valor con cuatro skills **en orden**:

**`doc-completitud`** (que no falte nada) → **`doc-cadena-causal`** (que cada concepto se sostenga solo) → **`doc-narrativa`** (que se lea como relato) → **`doc-prueba-de-uso`** (que un lector frío pueda ejecutar la tarea que el texto habilita) → **`unslop`** (que suene a persona).

`unslop` va al final y no es negociable, porque las cuatro anteriores AGREGAN texto y todo texto que agrega un modelo llega con sus marcas puestas. Correrlo antes es limpiar una casa mientras siguen entrando cajas. Y si después vuelves a editar con un modelo, hay que correrlo de nuevo.

La prueba de uso es a la prosa lo que un test de integración es al código: **explicar ≠ poder hacer**. Se aplican a cualquier documento para cualquier fin, desde un anexo técnico hasta las skills de este mismo repo.

Las cuatro hacen la misma pregunta con una vara cada vez más alta. Cada caja es una pregunta que
el texto tiene que aprobar antes de pasar a la siguiente:

```mermaid
flowchart TD
  T(["Un texto recien escrito"]) --> C1

  C1{"1. Le falta algo a alguien<br/>que llega sin contexto?<br/>(doc-completitud)"}
  CC{"2. Cada concepto se sostiene solo?<br/>Se sabe por que existe y de<br/>donde sale su numero?<br/>(doc-cadena-causal)"}
  C2{"3. Se puede leer sin sufrir,<br/>o es un muro de tablas?<br/>(doc-narrativa)"}
  C3{"4. Quien tiene que HACER algo<br/>con esto, puede?<br/>(doc-prueba-de-uso)"}

  F1["Se rellenan los huecos"]
  FC["Se funda el concepto"]
  F2["Se reescribe como relato"]

  C1 -->|"no falta nada"| CC
  C1 -->|"si falta"| F1
  F1 --> C1

  CC -->|"todo fundado"| C2
  CC -->|"hay conceptos sin fundamento"| FC
  FC --> CC

  C2 -->|"ya se lee bien"| C3
  C2 -->|"es un muro"| F2
  F2 --> C2

  C3 -->|"pudo hacerlo"| OK(["Listo para entregar"])
  C3 -->|"tuvo que adivinar"| C1
```

El orden importa y no es negociable. No sirve pulir la redacción de un texto al que todavía le
faltan datos. Y la última pregunta es la que sorprende, un documento puede estar completo y
bien escrito, y aun así quien debe construir algo con él no puede. **Explicar no es lo mismo
que habilitar.**

Dos aclaraciones sobre el dibujo: **se pueden usar por separado** (si tu texto ya está completo
y solo es denso, corres la de narrativa sola), pero cuando se usan juntas van en ese orden. Y hay
dos tipos de flecha de vuelta que conviene no confundir: las **cortas**, cada pregunta arregla lo
suyo y se vuelve a preguntar a sí misma, y la **larga**, que devuelve hasta el principio y **solo
se recorre si la pregunta 4 falla**. Esa última es la importante: lo que el lector tuvo que
adivinar es exactamente lo que faltaba, así que se rellena y se baja de nuevo por todo el
pipeline. Si nadie tuvo que adivinar, el texto sale por la derecha y no hay loop largo.

## Cómo funcionan por dentro. Las seis hacen lo mismo

Seis de las diez skills no le piden a Claude que revise algo él solo: **lanzan varios agentes
en paralelo**, cada uno mirando el mismo material desde un ángulo distinto, y después alguien
junta los resultados. Las seis siguen exactamente la misma secuencia de cinco pasos.

Para verla, un caso real de una de ellas: un informe con cifras que se va a enviar a un cliente.

```mermaid
flowchart TD
  P1["PASO 1 - Antes de revisar nada, se escribe la lista de<br/>las afirmaciones que el informe hace. Esa lista es la<br/>vara con la que se juzgara todo lo demas."]

  ABA["Se toma UNA afirmacion de la lista<br/>(esto se repite por cada afirmacion)"]
  P1 --> ABA

  ABA --> A1
  ABA --> A2
  ABA --> A3

  A1["PASO 2a - Agente FUENTE<br/>Existe el documento citado?<br/>Dice literalmente eso, o esta parafraseado?"]
  A2["PASO 2b - Agente MEDICION<br/>La cifra mide el periodo, el lugar y la<br/>unidad que la frase le atribuye?"]
  A3["PASO 2c - Agente INFERENCIA<br/>La conclusion se sigue de la evidencia,<br/>o hay un salto que nadie justifico?"]

  A1 --> P3
  A2 --> P3
  A3 --> P3

  P3["PASO 3 - Un solo agente junta los tres veredictos<br/>y resuelve los que se contradicen entre si."]
  P3 --> P4
  P4{"PASO 4 - Contra la lista del paso 1:<br/>quedo alguna afirmacion sin revisar?"}
  P4 -->|"no, todas revisadas"| P5
  P4 -.->|"si: esa afirmacion vuelve al abanico"| ABA
  P5["PASO 5 - Se decide: que se imprime, que se<br/>corrige, que se borra del informe."]
```

**Ese abanico del paso 2 es el punto.** Los tres agentes corren **al mismo tiempo y sin verse
entre sí**, ninguno sabe qué encontró el otro. Si en vez de tres ángulos distintos pusieras
tres agentes con la misma instrucción, los tres repetirían el mismo punto ciego y la
coincidencia se sentiría como triple confirmación.

**El diagrama es esquemático. Dibuja lo que le pasa a UNA afirmación.** La lista del paso 1 se
escribe una sola vez para todo el informe. De ahí en adelante, cada afirmación de esa lista
recorre su propio camino 2 → 3 → 4 por separado. Si el informe tiene 10 afirmaciones, el abanico
se abre 10 veces: 30 agentes en total. Y esas 10 no esperan entre sí, cada afirmación avanza en
cuanto sus tres ángulos terminan, hasta el tope de agentes simultáneos que la máquina permite;
el resto hace fila. Por eso la cuenta (**ángulos × afirmaciones**) se hace *antes* de lanzar:
tres ángulos parecen baratos hasta que se multiplican por veinte afirmaciones.

Las tres decisiones de diseño que explican por qué es así, y no de otra forma:

- **La lista del paso 1 se escribe ANTES**, nunca después. Un revisor que no sabe qué buscar
  aprueba felizmente lo que la primera fase dejó afuera. Confirma lo que hay, no detecta lo que
  falta.
- **Los agentes del paso 2 son distintos entre sí**, no copias. Tres agentes con la misma
  instrucción repiten el mismo punto ciego tres veces y eso se siente como triple confirmación.
- **La decisión del paso 5 no se delega nunca.** Los agentes también inventan cosas, y solo
  quien conduce tiene el contexto para saber cuál hallazgo es real. El grafo entrega un informe
  etiquetado, jamás un cambio ya aplicado.

Sobre ese paso 5: **quien decide es Claude conduciendo la skill**, el que lanzó los agentes y
tiene el documento completo a la vista, no uno de los agentes lanzados. Antes de aplicar un
cambio va a buscar el hallazgo en el archivo real para descartar los inventados, y te muestra lo
grave para que decidas tú. La regla de la casa es que ningún agente suelto escribe el resultado
final.

Dentro del repo esos cinco pasos se llaman **ancla → lentes → síntesis → verificación →
decisión del orquestador**. Los vas a ver con esos nombres en el código de las skills. Y esto es
lo que cada una pone en cada paso:

| Skill | Su lista del paso 1 (la vara) | Sus agentes del paso 2 | Lo que se decide al final |
|---|---|---|---|
| `verificacion-adversarial` | las afirmaciones del texto y sus fuentes | uno por ángulo: fuente, medición, inferencia | qué se imprime y qué no |
| `doc-completitud` | el documento mismo | lectores sin contexto que marcan qué no entienden | qué vacío se rellena y cómo |
| `doc-cadena-causal` | la lista de conceptos del texto, enumerada a mano antes de invocar a nadie | auditores que aplican a cada concepto la rejilla de cinco preguntas (por qué existe, quién lo hace, de dónde sale su número, qué pasa sin él, si le aplica al lector) | qué concepto se funda y con qué parche |
| `doc-narrativa` | un inventario de todo lo que el texto ya dice | editores de narrativa, densidad y estructura | el plan de reescritura |
| `doc-prueba-de-uso` | una pauta de corrección escrita antes de ver nada | lectores que intentan HACER la tarea del documento | qué hay que concretar en el texto |
| `auditoria-de-realidad` | los archivos reales del proyecto (repo, git, deploy) | un escéptico por cada zona de riesgo | qué hallazgo es real y qué se arregla primero |

Las otras cuatro (`desarrollo-riguroso`, `retrospectiva-de-sesion`, `escritura-de-prompts`,
`agents-sdk`) no lanzan agentes: las tres primeras son método que Claude aplica leyéndolas, y
`agents-sdk` es conocimiento técnico que lo manda a leer las docs vivas de Cloudflare. Y eso es literal, no hay que invocarlas
a mano: al iniciar la sesión Claude lee el nombre y la descripción de cada skill instalada, y
cuando le pides algo que calza con una, la carga completa y la sigue (ver
[Cómo se invocan](#cómo-se-invocan) más abajo). El detalle técnico de la maquinaria
, incluidos los errores que cada skill pagó por separado, vive en
[`desarrollo-riguroso/reference/esqueleto-de-verificacion.md`](desarrollo-riguroso/reference/esqueleto-de-verificacion.md).

## Instalación

Las skills se instalan **distinto en cada superficie de Claude**, y no se sincronizan automáticamente entre ellas. Si usas Claude en varios lugares, hay que instalar en cada uno.

### Claude Code

Las skills viven en el filesystem como carpetas. Claude Code las descubre automáticamente al iniciar una sesión.

**Instalación personal** (disponible en todos tus proyectos):

```bash
git clone https://github.com/JoaquinMulet/kumo-skills.git
cp -r kumo-skills/escritura-de-prompts ~/.claude/skills/
```

**Instalación a nivel proyecto** (compartida con quien clone ese repo):

```bash
cp -r kumo-skills/escritura-de-prompts /ruta/al/proyecto/.claude/skills/
```

En Windows con PowerShell:

```powershell
git clone https://github.com/JoaquinMulet/kumo-skills.git
Copy-Item -Recurse kumo-skills/escritura-de-prompts $HOME/.claude/skills/
```

Si la carpeta `~/.claude/skills/` no existe, créala antes. Reiniciar la sesión de Claude Code para que la nueva skill aparezca.

**Cuál de las dos elegir.** La personal (`~/.claude/skills/`) vive en tu equipo. La ves tú en
todos tus proyectos y nadie más. La de proyecto (`<proyecto>/.claude/skills/`) se commitea junto
al código. La ve cualquiera que clone ese repo, y solo dentro de él. Regla práctica: las skills
transversales de Kumo van en la personal. Una skill que solo tiene sentido en un proyecto
concreto va en la de ese proyecto.

### claude.ai (Pro / Max / Team / Enterprise)

Requiere code execution habilitado en tu cuenta.

1. Descarga la carpeta de la skill desde GitHub (por ejemplo `escritura-de-prompts/`).
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

Una vez instalada, no hay que invocar la skill explícitamente. Pídele a Claude la tarea en lenguaje natural y, si la `description` de la skill calza con la petición, Claude la usa solo. Por ejemplo, con `escritura-de-prompts` instalada basta con:

> "Ayúdame a escribir un prompt para hacer X."
>
> "Revísame este prompt antes de usarlo en producción."
>
> "¿Por qué Claude me respondió esto y no lo que yo quería?"

## Contribuir

Antes de proponer una skill nueva o modificar una existente, leer [CLAUDE.md](CLAUDE.md). Cubre estructura mínima de una skill, convenciones de Kumo (naming, idioma, descriptions efectivas), cuándo vale la pena hacer skill vs solo prompt, y el checklist de review obligatorio antes de mergear cualquier PR.

## Licencia

[MIT](LICENSE).
