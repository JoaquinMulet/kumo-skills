---
name: retrospectiva-de-sesion
description: El procedimiento de Kumo para cerrar una sesión de desarrollo de CÓDIGO aprendiendo de ella — cosecha las correcciones del usuario, destila el principio detrás de cada una, y las compone en el CLAUDE.md del proyecto (lo específico) y en el estándar de desarrollo de la empresa (lo universal), endureciendo y adaptando el proceso de desarrollo sesión a sesión. Usa esta skill al terminar una sesión de código sustantiva, o cuando el usuario dice "cerremos la sesión", "qué aprendimos", "hagamos la retro", "actualiza el CLAUDE.md con esto", "mejoremos el proceso de desarrollo", "captura los aprendizajes de código", "anota esto para la próxima", o pide corregir/robustecer cómo desarrollaste — en cualquier idioma. NO es para mejorar prompts (eso es escritura-de-prompts) ni procesos operacionales no-código.
---

# Retrospectiva de sesión. Endurecer el proceso, sesión a sesión

El estándar de desarrollo (`desarrollo-riguroso`) no es estático: es la base que cada proyecto **adapta y endurece con el uso**. Cada sesión de código produce correcciones y descubrimientos que, si no se capturan, se pierden, y el próximo agente (o tú en dos semanas) repite el mismo error. Esta skill es el **ritual de cierre** que convierte una sesión en aprendizaje durable y decide **dónde vive** cada aprendizaje.

Es lo que hace que el estándar de Kumo sea un organismo vivo por proyecto y no un documento muerto. El `CLAUDE.md` de cada proyecto empieza sembrado desde `desarrollo-riguroso` y se vuelve más afilado con cada retro.

## Cuándo correrla

Al final de una sesión de desarrollo **sustantiva**, no un one-liner. Especialmente si (a) el usuario te corrigió o redirigió, (b) hubo un bug no trivial, o (c) descubriste un patrón, una filosofía o un invariante del proyecto que no estaba escrito. Si la sesión no dejó nada durable, decirlo y no inventar aprendizajes para llenar.

## El flujo. 5 pasos

**Prerrequisito: `desarrollo-riguroso` leída EN ESTA sesión** (si no la has leído, o el
contexto se compactó desde entonces, léela completa ahora). No es ceremonia, tres pasos
dependen de su contenido: el paso 3 clasifica contra lo que el estándar YA cubre (sin
leerlo, duplicas o contradices), el paso 4 usa sus definiciones con el significado canónico
y no con el que suene razonable, y el paso 5 inserta lo universal en el lugar correcto de
ese archivo.

### 1. Cosechar las correcciones

Recorrer la sesión completa y cosechar dos cosas:

- **Cada punto donde el usuario te corrigió, redirigió o mostró fricción.** Verbatim cuando se pueda. Una corrección es oro. Es la distancia exacta entre lo que hiciste y lo que el proyecto esperaba.
- **Los descubrimientos técnicos no obvios.** Un gotcha del stack, un supuesto roto, una forma de dato que no habías considerado.

Si durante la sesión operó la **paranoia del compounding** (`desarrollo-riguroso` §«Cómo crece este estándar»), la cosecha debe encontrar los principios YA escritos en el momento de cada corrección. Esta retro los **verifica y completa**, no los estrena. Cada corrección que aparezca aquí sin compoundear es, en sí misma, un hallazgo, el reflejo no disparó, y el porqué va a la cosecha.

### 2. Destilar el principio, no el caso

Por cada corrección, extraer el **principio general** detrás, no el arreglo puntual. El caso puntual se olvida. El principio se reusa.

- ❌ "El pago del 22-jun había que calzarlo contra las 3 facturas."
- ✅ "Un pago que baja un pasivo sin ligar su factura no se silencia. Se explica o se grita."

**Prueba de fuego:** si no puedes formular el principio en una frase reusable, todavía no lo entendiste, el aprendizaje aún es un caso, no una lección.

### 3. Clasificar: específico del proyecto vs universal

Por cada aprendizaje decidir dónde vive. **Regla de la duda.** Si sirve en el próximo proyecto de OTRO dominio, es universal.**

| Va al `CLAUDE.md` del proyecto (ESPECÍFICO) | Va a `desarrollo-riguroso` (UNIVERSAL) |
|---|---|
| Un invariante de dominio, un comando del stack, un gotcha de una librería, cuál es el oráculo de verdad, un patrón de arquitectura del proyecto | Una verdad de ingeniería que aplica a cualquier proyecto de Kumo (una postura de testing, un anti-patrón, una regla de honestidad u observabilidad) |

La mayoría de los aprendizajes son **específicos**, resistir la tentación de subir todo al estándar universal (lo infla y lo vuelve inútil). Un aprendizaje solo asciende a universal cuando ya lo viste **morder** (costar un error real) en más de un contexto o es claramente independiente del dominio.

### 4. Analizar la filosofía del proyecto y adaptar estrategias externas

Preguntarse explícitamente por el proyecto de esta sesión (es un marco de análisis tuyo, involucra al usuario solo si la respuesta no está en el repo ni en la sesión). **Output de este paso:** uno a tres cambios concretos al **flujo de desarrollo o de testing** del proyecto (un paso nuevo en el bug-fix workflow, un tipo de test que faltaba, una alarma de observabilidad, una guarda), no una reflexión abstracta. Las preguntas que llevan a ese output:

- **¿Qué invariantes lo rigen?** (correctitud de dinero, latencia, seguridad, compatibilidad con un estándar…). Eso define qué rigor merece cada área.
- **¿Cuál es su oráculo de verdad, duro o blando, y cómo se hace su VERIFY-REAL, espejar fiel o nombrar residuales?** (los cuatro conceptos, oráculo duro/blando, VERIFY-REAL, espejar fiel, nombrar residuales, viven definidos en `desarrollo-riguroso`).
- **¿Qué estrategia probada de la industria conviene adoptar** (una referencia aportada por ti o por el usuario, ambas valen)? Aplicar el **filtro del invariante** de `desarrollo-riguroso` (adoptar el principio, re-derivar el mecanismo al stack y la escala reales, descartar lo que no paga su costo ni sobrevive tres meses sin cuidado). No re-derivar la regla acá, vive allá.

### 5. Escribir y verificar

- **Al `CLAUDE.md` del proyecto.** Una entrada en *Lessons Learned* (una viñeta por lección) con el formato **qué falló → causa raíz → prescripción accionable**, más cualquier *Pattern* nuevo, un **Pattern** es una convención o procedimiento del proyecto que se va a repetir (formato: nombre + cuándo aplica + los pasos), y se escribe como viñeta o sección propia en el mismo `CLAUDE.md`. Concreto, con nombres de funciones/archivos reales.
- **Al estándar de Kumo:** si el aprendizaje es universal, editar `desarrollo-riguroso`, **una skill, un commit**. Si tocas el frontmatter, corre el **test de descubrimiento** (3 prompts representativos que deben invocarla + 1 no relacionado que no debe) del checklist «Antes de mergear» del `CLAUDE.md` del repo `kumo-skills`, antes de mergear. Y antes de editar cualquier skill: ver «Si vas a editar una skill instalada», más abajo.
- **Verificar honestamente, y no solo releyendo.** La relectura propia es la forma más débil de verificación. El autor es ciego a su propio drift. Escala según lo que escribiste: (a) una viñeta o lección puntual → releerla como la leería alguien sin contexto (¿se entiende el principio sin haber vivido la sesión? si no, reescribir). (b) una skill nueva o reestructurada, o una sección sustantiva de `CLAUDE.md` → pasarla por el pipeline documental de `desarrollo-riguroso` §«Los documentos también se testean» (`doc-completitud` → `doc-narrativa` → `doc-prueba-de-uso`. Como mínimo, una ronda de lector frío de completitud). (c) Si tocaste un `CLAUDE.md`, correr además el gate de **claims contra el código** sobre lo escrito, cada afirmación verificable (rutas, nombres, conteos, «validado») cruzada contra código/tests/`git`, que ese mismo apartado de `desarrollo-riguroso` ordena hacer rutina de la retro.
- **Cerrar con la pregunta adversarial** que `desarrollo-riguroso` ordena para toda sesión (§«La trampa del validador autorreferencial»): *«¿qué problema real y grave es invisible para mi aparato AHORA?»*, contra el repo/prod real, no un fixture. Lo que aparezca es cosecha de esta misma retro (vuelve al paso 1). Si no aparece nada, decirlo explícitamente.

### 5b. La aduana de los aprendizajes (con agentes, sobre el umbral)

`desarrollo-riguroso` ya exige aduana adversarial de contexto fresco para el **código** que va
al trunk y para toda **propuesta** que ve el operador. Las lecciones de esta retro son el
tercer producto que sale de tu cabeza y hasta ahora salía sin aduana, y peor: el estándar que
podrías estar relajando lo revisa el único agente con incentivo de bajar la vara. Eso no se
arregla con fuerza de voluntad, se arregla estructuralmente.

**Umbral.** Corre la aduana completa si (a) hay **tres o más** lecciones candidatas, o (b)
alguna se propone para **ascender a universal** (editar `desarrollo-riguroso` afecta a todos
los proyectos de la empresa). Con una o dos lecciones específicas del proyecto, el paso 5
normal alcanza. Un grafo ahí es sobrecosto, y la retro es justo el momento donde más quieres
leer y aprobar tú. Rige la puerta de la casa. Presenta la cuenta de agentes y espera el visto
bueno.

**El diseño, con el presupuesto barato de la casa (≤6 agentes):**

1. **Un nodo por lección, ¿es nueva, y dónde vive?** (hasta 4. Si hay más, agrúpalas). Lee el
   `CLAUDE.md` del proyecto y `desarrollo-riguroso`, y responde dos cosas: si el principio **ya
   está escrito** (resuelve mecánicamente la paranoia del compounding que el paso 1 pide
   verificar a ojo) y si es **específico o universal** aplicando la regla de la duda. Que ya
   esté escrito es el resultado más común y el más valioso. Te ahorra escribir por segunda vez
   lo que la retro misma prohíbe duplicar.
2. **Un nodo de claims.** Ejecuta `grep` y `git` sobre TODO lo que escribiste en el paso 5,
   rutas, nombres de funciones, conteos, cada «validado». No es una intención de verificar. Es
   un nodo que corre los comandos. Es el ancla dura de la retro entera.
3. **El juez frío, sobre la señal CRUDA.** Recibe (a) los turnos del usuario extraídos
   mecánicamente y (b) las lecciones propuestas, nunca tu lista de correcciones cosechada, ni
   la sesión completa con tu razonamiento dentro. Y responde **dos** preguntas:
   - ¿cada lección **captura** la corrección que dice capturar, o es una versión suavizada que
     le da la razón al agente?
   - **¿hay correcciones del usuario que no produjeron ninguna lección?**

   La segunda es la que importa y hoy no la hace nadie: si el cosechador del paso 1 omitió la
   corrección incómoda, un juez que solo mira la lista cosechada la valida felizmente. Por eso
   la señal se extrae con un script y no con tu memoria:

   ```bash
   uv run python scripts/extraer-turnos-usuario.py --ultima -o turnos.md
   ```

   (Acepta también la ruta explícita del `.jsonl`. Cero turnos extraídos es señal de
   instrumento roto, no de sesión vacía.)

El andamiaje reusable, schemas con prueba de trabajo, topes, por qué el ancla va primero, vive
en `desarrollo-riguroso`, `reference/esqueleto-de-verificacion.md`: **léelo antes de escribir el
workflow.** Lo que el juez devuelva vuelve al paso 1 como cosecha: una lección suavizada se
reescribe, y una corrección sin lección es el hallazgo más importante de la retro.

## Errores de la propia retro (evitarlos)

- **Transcribir el caso como si fuera el principio** → se sobre-ajusta y no se reusa.
- **Subir todo al estándar universal** → lo infla. La mayoría es específico del proyecto.
- **Relajar un estándar existente para justificar lo que hiciste** → si un estándar estorbó, cuestiónalo **explícitamente** (di por qué y qué lo reemplaza), nunca lo borres o lo ablandes en silencio. Bajar la vara es exactamente lo contrario de endurecer el proceso. *(Este error es estructural, no de disciplina. Quien lo comete es el único con incentivo de cometerlo. Sobre el umbral, lo caza el juez frío del paso 5b. Bajo el umbral, lo cazas leyendo tu propia lección al lado de la corrección verbatim que la origina.)*
- **Inventar aprendizajes para llenar** → una retro honesta a veces concluye "esta sesión no dejó nada durable".
- **Escribir un markdown que narre el código** → los aprendizajes son convenciones, lecciones y contratos. El "cómo funciona" vive en el código (ver `desarrollo-riguroso`).

## Si vas a editar una skill instalada. Dos lugares, siempre

`~/.claude/skills/` es la **copia instalada** (no tiene `.git`). La fuente única de verdad es el repo `kumo-skills`. El ciclo completo, `diff` previo en ambas direcciones, merge si hay drift, commit con gate, resync al instalado, push, **vive documentado en el `CLAUDE.md` del repo `kumo-skills`** (sección «Cuando Claude edite una skill INSTALADA»): localiza el repo en el disco y léelo ANTES de editar cualquier skill, esta incluida. Editar solo la copia instalada crea drift bidireccional silencioso.

Sin este ritual cada proyecto empieza de cero y cada agente tropieza con las mismas piedras. Con él, el próximo proyecto de Kumo **arranca ya sabiendo lo que este proyecto aprendió a los golpes.**
