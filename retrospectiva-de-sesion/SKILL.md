---
name: retrospectiva-de-sesion
description: El procedimiento de Kumo para cerrar una sesión de desarrollo de CÓDIGO aprendiendo de ella — cosecha las correcciones del usuario, destila el principio detrás de cada una, y las compone en el CLAUDE.md del proyecto (lo específico) y en el estándar de desarrollo de la empresa (lo universal), endureciendo y adaptando el proceso de desarrollo sesión a sesión. Usa esta skill al terminar una sesión de código sustantiva, o cuando el usuario dice "cerremos la sesión", "qué aprendimos", "hagamos la retro", "actualiza el CLAUDE.md con esto", "mejoremos el proceso de desarrollo", "captura los aprendizajes de código", "anota esto para la próxima", o pide corregir/robustecer cómo desarrollaste — en cualquier idioma. NO es para mejorar prompts (eso es escritura-de-prompts) ni procesos operacionales no-código.
---

# Retrospectiva de sesión — endurecer el proceso, sesión a sesión

El estándar de desarrollo (`desarrollo-riguroso`) no es estático: es la base que cada proyecto **adapta y endurece con el uso**. Cada sesión de código produce correcciones y descubrimientos que, si no se capturan, se pierden — y el próximo agente (o tú en dos semanas) repite el mismo error. Esta skill es el **ritual de cierre** que convierte una sesión en aprendizaje durable y decide **dónde vive** cada aprendizaje.

Es lo que hace que el estándar de Kumo sea un organismo vivo por proyecto y no un documento muerto: el `CLAUDE.md` de cada proyecto empieza sembrado desde `desarrollo-riguroso` y se vuelve más afilado con cada retro.

## Cuándo correrla

Al final de una sesión de desarrollo **sustantiva** — no un one-liner. Especialmente si (a) el usuario te corrigió o redirigió, (b) hubo un bug no trivial, o (c) descubriste un patrón, una filosofía o un invariante del proyecto que no estaba escrito. Si la sesión no dejó nada durable, decirlo y no inventar aprendizajes para llenar.

## El flujo — 5 pasos

**Prerrequisito: `desarrollo-riguroso` leída EN ESTA sesión** (si no la has leído, o el
contexto se compactó desde entonces, léela completa ahora). No es ceremonia — tres pasos
dependen de su contenido: el paso 3 clasifica contra lo que el estándar YA cubre (sin
leerlo, duplicas o contradices), el paso 4 usa sus definiciones con el significado canónico
y no con el que suene razonable, y el paso 5 inserta lo universal en el lugar correcto de
ese archivo.

### 1. Cosechar las correcciones

Recorrer la sesión completa y cosechar dos cosas:

- **Cada punto donde el usuario te corrigió, redirigió o mostró fricción** — verbatim cuando se pueda. Una corrección es oro: es la distancia exacta entre lo que hiciste y lo que el proyecto esperaba.
- **Los descubrimientos técnicos no obvios**: un gotcha del stack, un supuesto roto, una forma de dato que no habías considerado.

### 2. Destilar el principio, no el caso

Por cada corrección, extraer el **principio general** detrás, no el arreglo puntual. El caso puntual se olvida; el principio se reusa.

- ❌ "El pago del 22-jun había que calzarlo contra las 3 facturas."
- ✅ "Un pago que baja un pasivo sin ligar su factura no se silencia: se explica o se grita."

**Prueba de fuego:** si no puedes formular el principio en una frase reusable, todavía no lo entendiste — el aprendizaje aún es un caso, no una lección.

### 3. Clasificar: específico del proyecto vs universal

Por cada aprendizaje decidir dónde vive. **Regla de la duda: si sirve en el próximo proyecto de OTRO dominio, es universal.**

| Va al `CLAUDE.md` del proyecto (ESPECÍFICO) | Va a `desarrollo-riguroso` (UNIVERSAL) |
|---|---|
| Un invariante de dominio, un comando del stack, un gotcha de una librería, cuál es el oráculo de verdad, un patrón de arquitectura del proyecto | Una verdad de ingeniería que aplica a cualquier proyecto de Kumo (una postura de testing, un anti-patrón, una regla de honestidad u observabilidad) |

La mayoría de los aprendizajes son **específicos** — resistir la tentación de subir todo al estándar universal (lo infla y lo vuelve inútil). Un aprendizaje solo asciende a universal cuando ya lo viste **morder** (costar un error real) en más de un contexto o es claramente independiente del dominio.

### 4. Analizar la filosofía del proyecto y adaptar estrategias externas

Preguntarse explícitamente por el proyecto de esta sesión (es un marco de análisis tuyo — involucra al usuario solo si la respuesta no está en el repo ni en la sesión). **Output de este paso:** uno a tres cambios concretos al **flujo de desarrollo o de testing** del proyecto (un paso nuevo en el bug-fix workflow, un tipo de test que faltaba, una alarma de observabilidad, una guarda), no una reflexión abstracta. Las preguntas que llevan a ese output:

- **¿Qué invariantes lo rigen?** (correctitud de dinero, latencia, seguridad, compatibilidad con un estándar…). Eso define qué rigor merece cada área.
- **¿Cuál es su oráculo de verdad, duro o blando, y cómo se hace su VERIFY-REAL — espejar fiel o nombrar residuales?** (los cuatro conceptos — oráculo duro/blando, VERIFY-REAL, espejar fiel, nombrar residuales — viven definidos en `desarrollo-riguroso`).
- **¿Qué estrategia probada de la industria conviene adoptar** (una referencia aportada por ti o por el usuario — ambas valen)? Aplicar el **filtro del invariante** de `desarrollo-riguroso` (adoptar el principio, re-derivar el mecanismo al stack y la escala reales, descartar lo que no paga su costo ni sobrevive tres meses sin cuidado). No re-derivar la regla acá — vive allá.

### 5. Escribir y verificar

- **Al `CLAUDE.md` del proyecto:** una entrada en *Lessons Learned* (una viñeta por lección) con el formato **qué falló → causa raíz → prescripción accionable**, más cualquier *Pattern* nuevo — un **Pattern** es una convención o procedimiento del proyecto que se va a repetir (formato: nombre + cuándo aplica + los pasos), y se escribe como viñeta o sección propia en el mismo `CLAUDE.md`. Concreto, con nombres de funciones/archivos reales.
- **Al estándar de Kumo:** si el aprendizaje es universal, editar `desarrollo-riguroso` — **una skill, un commit**; si tocas el frontmatter, corre el **test de descubrimiento** (3 prompts representativos que deben invocarla + 1 no relacionado que no debe) del checklist «Antes de mergear» del `CLAUDE.md` del repo `kumo-skills`, antes de mergear. Y antes de editar cualquier skill: ver «Si vas a editar una skill instalada», más abajo.
- **Verificar honestamente — y no solo releyendo.** La relectura propia es la forma más débil de verificación: el autor es ciego a su propio drift. Escala según lo que escribiste: (a) una viñeta o lección puntual → releerla como la leería alguien sin contexto (¿se entiende el principio sin haber vivido la sesión? si no, reescribir); (b) una skill nueva o reestructurada, o una sección sustantiva de `CLAUDE.md` → pasarla por el pipeline documental de `desarrollo-riguroso` §«Los documentos también se testean» (`doc-completitud` → `doc-narrativa` → `doc-prueba-de-uso`; como mínimo, una ronda de lector frío de completitud). (c) Si tocaste un `CLAUDE.md`, correr además el gate de **claims contra el código** sobre lo escrito — cada afirmación verificable (rutas, nombres, conteos, «validado») cruzada contra código/tests/`git` — que ese mismo apartado de `desarrollo-riguroso` ordena hacer rutina de la retro.
- **Cerrar con la pregunta adversarial** que `desarrollo-riguroso` ordena para toda sesión (§«La trampa del validador autorreferencial»): *«¿qué problema real y grave es invisible para mi aparato AHORA?»* — contra el repo/prod real, no un fixture. Lo que aparezca es cosecha de esta misma retro (vuelve al paso 1); si no aparece nada, decirlo explícitamente.

## Errores de la propia retro (evitarlos)

- **Transcribir el caso como si fuera el principio** → se sobre-ajusta y no se reusa.
- **Subir todo al estándar universal** → lo infla; la mayoría es específico del proyecto.
- **Relajar un estándar existente para justificar lo que hiciste** → si un estándar estorbó, cuestiónalo **explícitamente** (di por qué y qué lo reemplaza), nunca lo borres o lo ablandes en silencio. Bajar la vara es exactamente lo contrario de endurecer el proceso.
- **Inventar aprendizajes para llenar** → una retro honesta a veces concluye "esta sesión no dejó nada durable".
- **Escribir un markdown que narre el código** → los aprendizajes son convenciones, lecciones y contratos; el "cómo funciona" vive en el código (ver `desarrollo-riguroso`).

## Si vas a editar una skill instalada — dos lugares, siempre

`~/.claude/skills/` es la **copia instalada** (no tiene `.git`); la fuente única de verdad es el repo `kumo-skills`. El ciclo completo — `diff` previo en ambas direcciones, merge si hay drift, commit con gate, resync al instalado, push — **vive documentado en el `CLAUDE.md` del repo `kumo-skills`** (sección «Cuando Claude edite una skill INSTALADA»): localiza el repo en el disco y léelo ANTES de editar cualquier skill, esta incluida. Editar solo la copia instalada crea drift bidireccional silencioso.

Sin este ritual cada proyecto empieza de cero y cada agente tropieza con las mismas piedras; con él, el próximo proyecto de Kumo **arranca ya sabiendo lo que este proyecto aprendió a los golpes.**
