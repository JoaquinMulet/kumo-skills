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

### 1. Cosechar las correcciones

Recorrer la sesión y listar **cada punto donde el usuario te corrigió, redirigió o mostró fricción** — verbatim cuando se pueda. Una corrección es oro: es la distancia exacta entre lo que hiciste y lo que el proyecto esperaba. Incluir también los descubrimientos técnicos no obvios (un gotcha del stack, un supuesto roto, una forma de dato que no habías considerado).

### 2. Destilar el principio, no el caso

Por cada corrección, extraer el **principio general** detrás, no el arreglo puntual. El caso puntual se olvida; el principio se reusa.

- ❌ "El pago del 22-jun había que calzarlo contra las 3 facturas."
- ✅ "Un pago que baja un pasivo sin ligar su factura no se silencia: se explica o se grita."

Si no puedes formular el principio en una frase reusable, todavía no lo entendiste — el aprendizaje aún es un caso, no una lección.

### 3. Clasificar: específico del proyecto vs universal

Por cada aprendizaje decidir dónde vive. **Regla de la duda: si sirve en el próximo proyecto de OTRO dominio, es universal.**

| Va al `CLAUDE.md` del proyecto (ESPECÍFICO) | Va a `desarrollo-riguroso` (UNIVERSAL) |
|---|---|
| Un invariante de dominio, un comando del stack, un gotcha de una librería, cuál es el oráculo de verdad, un patrón de arquitectura del proyecto | Una verdad de ingeniería que aplica a cualquier proyecto de Kumo (una postura de testing, un anti-patrón, una regla de honestidad u observabilidad) |

La mayoría de los aprendizajes son **específicos** — resistir la tentación de subir todo al estándar universal (lo infla y lo vuelve inútil). Un aprendizaje solo asciende a universal cuando ya lo viste morder en más de un contexto o es claramente independiente del dominio.

### 4. Analizar la filosofía del proyecto y adaptar estrategias externas

Preguntar explícitamente por el proyecto de esta sesión:

- **¿Qué invariantes lo rigen?** (correctitud de dinero, latencia, seguridad, compatibilidad con un estándar…). Eso define qué rigor merece cada área.
- **¿Cuál es su oráculo de verdad, duro o blando?** (ver `desarrollo-riguroso`). Determina cómo se hace el VERIFY-REAL y si se espeja fiel o se nombran residuales.
- **¿Qué estrategia probada de la industria conviene adoptar** (de una referencia que admires)? Aplicar el **filtro del invariante** de `desarrollo-riguroso` (adoptar el principio, re-derivar el mecanismo al stack y la escala reales, descartar lo que no paga su costo ni sobrevive tres meses sin cuidado). No re-derivar la regla acá — vive allá.

El output de este paso es concreto: uno a tres cambios al **flujo de desarrollo o de testing** del proyecto (un paso nuevo en el bug-fix workflow, un tipo de test que faltaba, una alarma de observabilidad, una guarda), no una reflexión abstracta.

### 5. Escribir y verificar

- **Al `CLAUDE.md` del proyecto:** una entrada en *Lessons Learned* con el formato **qué falló → causa raíz → prescripción accionable**, más cualquier *Pattern* nuevo. Concreto, con nombres de funciones/archivos reales.
- **Al estándar de Kumo:** si el aprendizaje es universal, editar `desarrollo-riguroso` — **una skill, un commit** (convención del repo `kumo-skills`); si tocas el frontmatter, corre el test de descubrimiento del checklist antes de mergear.
- **Verificar honestamente:** releer lo escrito como lo leería alguien sin contexto. ¿Se entiende el principio sin haber vivido la sesión? Si no, reescribir.

## Errores de la propia retro (evitarlos)

- **Transcribir el caso como si fuera el principio** → se sobre-ajusta y no se reusa.
- **Subir todo al estándar universal** → lo infla; la mayoría es específico del proyecto.
- **Relajar un estándar existente para justificar lo que hiciste** → si un estándar estorbó, cuestiónalo **explícitamente** (di por qué y qué lo reemplaza), nunca lo borres o lo ablandes en silencio. Bajar la vara es exactamente lo contrario de endurecer el proceso.
- **Inventar aprendizajes para llenar** → una retro honesta a veces concluye "esta sesión no dejó nada durable".
- **Escribir un markdown que narre el código** → los aprendizajes son convenciones, lecciones y contratos; el "cómo funciona" vive en el código (ver `desarrollo-riguroso`).

Sin este ritual cada proyecto empieza de cero y cada agente tropieza con las mismas piedras; con él, el próximo proyecto de Kumo **arranca ya sabiendo lo que este proyecto aprendió a los golpes.**
