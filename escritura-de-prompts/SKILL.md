---
name: escritura-de-prompts
description: Metodología para escribir, mejorar, auditar o diagnosticar prompts dirigidos a Claude. Usa esta skill cuando el usuario pida ayuda para redactar un prompt, mejorar uno que ya tiene, diagnosticar por qué un prompt produjo una salida mediocre, auditar un prompt antes de usarlo en producción, o convertir una idea vaga en una instrucción precisa. También aplica cuando dice cosas como "ayúdame con este prompt", "este prompt no funciona", "Claude me respondió X pero yo quería Y", "cómo le pido a Claude que…", "revísame este prompt", "mejóralo", "por qué me dio esta respuesta", "help me write a prompt", "review this prompt", "this prompt isn't working", o equivalentes en cualquier idioma — incluso cuando solo pega un prompt y otra salida sin instrucción explícita, esperando una versión mejor.
---

# Escritura de prompts

Esta skill convierte la habilidad de prompting en un método. El objetivo no es producir prompts más largos, sino prompts que el modelo entienda a la primera y cuyo resultado se pueda confiar sin renegociarlo.

## Principio rector

**La respuesta es el síntoma; el problema casi siempre vive en el prompt.** Cuando una salida no sirve, la postura no es discutirle al modelo ni pedirle "más corto, mejor, más profesional". Es reescribir la instrucción. El prompt es la única palanca real: el modelo está fijo, sus parámetros no se tocan. Lo único que decide qué neuronas se activan al responder es el texto que tú escribes.

El mismo modelo respondiendo a "resume este reporte" produce un amasijo genérico; respondiendo a "resume este reporte de auditoría en tres bullets para el comité ejecutivo, enfatizando los hallazgos críticos y omitiendo detalles operativos" produce algo que el comité puede leer en treinta segundos. Misma materia prima, dos resultados sin punto de comparación. La diferencia está toda en el prompt.

## Modos de uso

Activa esta metodología en cualquiera de estos modos:

- **Construir** un prompt nuevo a partir de una intención vaga del usuario.
- **Auditar** un prompt existente que el usuario ya escribió y quiere validar antes de usar.
- **Diagnosticar** un fallo: el usuario muestra un prompt y una salida que no le sirvió, y quiere entender por qué.
- **Mejorar** un prompt que funciona a medias.

En los cuatro casos el procedimiento es el mismo: revisar la anatomía completa del prompt, evitar las trampas comunes y, si la salida fue mala, decidir si la nueva intentona ocurre en el mismo chat o en uno limpio.

## Precondiciones: no empieces sin estas dos cosas

Antes de aplicar cualquiera de los cuatro modos —construir, auditar, diagnosticar o mejorar— asegúrate de tener dos piezas. Si falta alguna, **no inventes ni asumas**: pídela en una pregunta corta y amable, y espera la respuesta antes de levantar el lápiz.

### 1. El prompt o la tarea sobre la cual trabajar

Saber qué se va a construir, auditar, diagnosticar o mejorar. Si el usuario pegó un prompt, lo tienes. Si dijo "ayúdame con un prompt para X", la X es la tarea. Si no hay ninguna de las dos, falta la pieza.

### 2. El porqué de la tarea

Para qué la persona necesita hacer esto. No qué quiere que produzca el modelo, sino qué decisión, entrega o resultado depende del trabajo. Esta pieza es fundamental porque **el porqué ilumina implícitamente los criterios** que debe cumplir la realización. Sin él, dos prompts ambos defendibles parecen igual de buenos, y la metodología termina entregando un genérico que probablemente no calce con el uso real.

Ejemplos del mismo encargo cambiando solo el porqué:

- *Resumen de un reporte* → para el directorio del lunes: breve, ejecutivo, soportado en datos verificables. Para tu memoria personal: puede ser extenso y técnico.
- *Análisis de cartola* → para detectar gastos atípicos: ranking por magnitud y categoría. Para conciliar con contabilidad: foco en trazabilidad línea a línea.
- *Borrador de correo* → al cliente para cerrar venta: tono comercial cuidadoso, sin condicionales débiles. Al colega para coordinar logística: directo y breve.

Tres prompts radicalmente distintos, según el porqué.

### Cómo pedirlo si no está

Pregunta corto y amable; explica por qué necesitas saberlo para que la persona no sienta que la estás interrogando. Formas que funcionan:

> "Antes de armarlo, ¿me cuentas para qué vas a usar el resultado? Saberlo cambia qué piezas del prompt enfatizo y cuáles puedo dejar livianas."

> "Para afinar el prompt a tu uso real, ¿me dices qué decisión o entrega depende de la salida? ¿Es para una revisión interna, una entrega a cliente, una etapa intermedia de análisis?"

No avances al modo correspondiente hasta tener ambas piezas en mano.

## Qué cuenta como "prompt"

Antes de revisar nada, un prompt es **todo el texto que el modelo recibe antes de generar su respuesta**: el mensaje que el usuario escribe en la caja, más la instrucción del sistema configurada por debajo, más los documentos adjuntos, más el historial de la conversación si la hay. Cuando alguien dice "el prompt no funcionó", muchas veces la falla no está en el último mensaje sino en la instrucción del sistema, en un documento mal cargado, o en contexto sucio que arrastra del intercambio anterior. Audita el paquete completo, no solo la última oración escrita.

La **instrucción del sistema** es un texto persistente con reglas o preferencias que la interfaz le inyecta a Claude antes del mensaje del usuario en cada conversación. Funciona como instrucciones generales que se aplican siempre. Junto con archivos del proyecto (como `CLAUDE.md`), skills, plugins, conectores, Proyectos y la memoria de claude.ai forman una capa que existe para no tener que repetir contexto en cada conversación. Cuando un prompt falla puede ser por algo escrito ahí, no en el mensaje visible.

## Anatomía completa de un prompt útil

Un buen prompt rara vez es una sola oración. Combina hasta **ocho piezas**. Las primeras siete son condicionales: no todas son obligatorias en todos los casos — una tarea trivial puede ir con dos o tres. La octava (auditoría externa) es no negociable: cierra siempre todo prompt producido con esta metodología. Cuando un prompt falla, casi siempre es porque le falta alguna de estas ocho. Antes de declarar un prompt listo, revísalas en orden.

### 1. Rol

A quién quieres que el modelo "haga de" mientras responde. No es teatro: ancla el tono, el vocabulario, el nivel de detalle y el grado de cautela. "Eres un revisor de contratos en una firma legal grande" antes de pegar un contrato cambia drásticamente qué cláusulas el modelo subraya. "Eres un editor riguroso", "Eres un analista financiero conservador", "Eres un ingeniero senior que escribe código defensivo": cada uno fija un ángulo distinto.

Preguntas para asignar bien el rol:

- ¿Qué tipo de profesional resolvería esto en la vida real?
- ¿Qué grado de cautela quiero que tenga ese rol (paranoico, equilibrado, exploratorio)?
- ¿Qué vocabulario y nivel de detalle viene asociado a ese rol?

### 2. Contexto

El trasfondo que el modelo necesita para hacer bien la tarea: quién va a leer la salida, qué decisiones previas ya se tomaron, qué restricciones existen, qué datos están en juego. Mucho de esto te resulta obvio porque vives en el problema; al modelo no le es obvio. Lo que no está dentro de su ventana de contexto sencillamente no existe para él.

Regla operativa: **cuéntale lo que un colega que recién llega necesitaría para hacer la tarea sin volver a preguntarte cada cinco minutos.** Si el documento ya pasó por dos revisiones, dilo. Si la audiencia es técnica o ejecutiva, dilo. Si hay tres opciones consideradas y dos descartadas, di cuáles y por qué.

### 3. Tarea concreta

Qué quieres específicamente que produzca. Aquí el enemigo es la vaguedad. "Mira esto y dime qué piensas" obliga al modelo a adivinar; "extrae las tres cláusulas que considerarías más arriesgadas para el comprador y explica por qué cada una lo es" no.

Fórmula útil:

> **verbo + objeto + alcance**

Ejemplo: "extrae *(verbo)* las tres cláusulas más arriesgadas *(objeto)* y explica por qué cada una lo es *(alcance)*". Lo concreto se recuerda y se ejecuta; lo abstracto se evapora.

### 4. Formato de salida

Cómo quieres que se vea la respuesta. ¿Un párrafo? ¿Tres bullets? ¿Una tabla con dos columnas? ¿JSON con campos específicos? ¿Markdown con encabezados? Pedir formato explícito ahorra una iteración casi siempre y suele mejorar la calidad del contenido, porque obliga al modelo a estructurar antes de escribir.

Cuando puedas, especifica también límites: número de bullets, líneas máximas por bullet, longitud total, campos obligatorios. "Tabla de cinco filas con descripción, monto y categoría" es más útil que "una tabla".

### 5. Ejemplos (few-shot)

Cuando describir el patrón en abstracto es difícil pero mostrarlo es fácil, incluye dentro del prompt uno, dos o tres ejemplos del tipo de entrada y salida que esperas, antes del caso real. Esa técnica se llama *few-shot* (del inglés *few shots*, "unos pocos disparos") y al modelo le bastan pocos casos para captar el patrón.

Casos típicos donde rinde más que cualquier explicación:

- Clasificación con categorías que tienen matices ("urgente / normal / spam").
- Reescritura en un estilo concreto (mostrar dos pares antes-después).
- Extracción estructurada con un formato muy específico (mostrar input crudo y JSON esperado).
- Tono y longitud difíciles de articular pero fáciles de mostrar.

**Cuidado con los sesgos.** El modelo imita todo lo que ve, incluidos errores y sesgos sutiles. Si los tres ejemplos de "urgente" son correos del jefe directo, el modelo puede aprender "urgente = del jefe" en vez de "urgente = requiere respuesta en 24 horas". Elige los ejemplos con la deliberación con la que escribirías un caso de prueba: que cubran variedad real, que el rasgo que define la categoría aparezca sin ruido, que no compartan accidentalmente otra variable.

### 6. Criterios de validación (definition of done)

Antes de declarar terminada una tarea, define qué evidencia hace falta y obliga al modelo a levantarla. En la práctica son una o dos oraciones que cambian sustancialmente la confiabilidad del resultado. Tres componentes:

1. **Qué evidencia** debe levantar el modelo durante el trabajo (qué cálculos, qué referencias cruzadas, qué chequeos intermedios).
2. **Qué resultados son esperables** si todo salió bien (un cuadre, un total, una propiedad que debe cumplirse).
3. **Qué reglas de validación** debe aplicar sobre su propia salida antes de entregarla — y qué hacer si las reglas fallan: reportar la inconsistencia en vez de entregar un análisis incorrecto.

Patrones reutilizables según el tipo de tarea:

- **Análisis numérico**: "antes de entregar, verifica que [propiedad aritmética que debe cumplirse]. Si no cuadra, no entregues el análisis: dime qué dato parece inconsistente."
- **Resúmenes**: "ningún número o cita que aparezca en el resumen debe estar ausente del documento original. Si tienes que aproximar o agregar, márcalo explícitamente."
- **Extracción de cláusulas o referencias**: "marca al final cuáles tienen referencias cruzadas que no pudiste resolver."
- **Código**: "antes de entregar, ejecuta mentalmente la función con un caso de prueba y reporta si pasa o falla."

Equilibrio importante: **sobre-especificar una tarea creativa la asfixia; sub-especificar una tarea operativa la vuelve impredecible.** Para tareas estándar o repetitivas (análisis financiero, extracción de datos, validación de formularios), lista fases críticas y validaciones una por una. Para tareas exploratorias o creativas (proponer ideas, redactar borradores, plantear hipótesis), da reglas genéricas —no inventar datos, distinguir lo que está en la fuente de lo que infieres, marcar las dudas— y deja que la inteligencia del modelo decida cómo cumplirlas.

### 7. Restricciones explícitas

Qué NO quieres que haga, dicho directamente. "No inventes datos que no estén en la fuente", "no uses la palabra X", "no agregues introducción ni cierre, solo la lista", "no incluyas transferencias internas entre cuentas propias". Las restricciones cierran espacios donde el modelo, por defecto, te va a dar algo que tú no querías y que la prosa positiva no alcanzó a evitar.

### 8. Auditoría por agente externo (siempre)

Toda salida producida con esta metodología cierra con un bloque de auditoría externa. No es opcional ni depende del tipo de tarea: es la última línea de defensa contra el sesgo de auto-confirmación, esa tendencia del modelo a firmar como correcto un trabajo que él mismo produjo y que objetivamente tiene errores.

Bloque estándar, va literal al final de todo prompt:

> **[Auditoría externa]** Si tienes capacidad de invocar agentes, la verificación debe ser auditada y confirmada por un agente tercero externo e imparcial. En caso de que encuentre discrepancias, corrígelas. Solo informa el trabajo como terminado cuando tú y el agente auditor confirmen que fue terminado.

Por qué siempre, no solo "cuando corresponda":

- El sesgo de auto-confirmación está siempre presente. No hay tarea tan simple donde el modelo no pueda equivocarse y firmar el error con confianza. Las reglas de validación de la pieza #6 las verifica el mismo agente que produjo el trabajo; la pieza #8 mueve esa verificación a un agente con ojos fríos que no tiene inversión en los pasos previos.
- La condicional "si tienes capacidad de invocar agentes" hace el bloque seguro entre superficies: en claude.ai estándar o una llamada plana a la API, el bloque es inerte y no rompe nada. En Claude Code, Claude Cowork, o un setup multi-agente con el Agent SDK, se activa.
- Estandarizarlo elimina la decisión "esta tarea lo amerita". La amerita siempre que la capacidad esté disponible; cuando no está disponible, no cuesta nada.

Cuando puedas, nombra al auditor: si sabes qué agente cumplirá el rol (un sub-agente del SDK, un `Task` específico de Claude Code, una *task* de Cowork), nómbralo en el bloque para que el modelo no lo elija a ciegas. Si no, la condicional genérica basta.

## Ejemplo completo: las ocho piezas aplicadas

Para que el contraste sea palpable, compara dos versiones del mismo encargo.

**Prompt vago:**

> Analiza esta cartola y dime los gastos principales del mes.

**Prompt con las ocho piezas:**

> **[Rol]** Eres un analista de control financiero con cinco años de experiencia revisando cartolas mensuales para una empresa de servicios.
>
> **[Contexto]** Te paso adjunta la cartola del mes de octubre. La usa el CFO para detectar gastos atípicos antes del cierre mensual. La empresa tiene ~80 movimientos al mes, mezcla de gastos operativos y pagos a proveedores. Los meses anteriores el gasto promedio fue de USD 120.000.
>
> **[Tarea]** Identifica los cinco movimientos de gasto más relevantes del período y agrúpalos por categoría: servicios, proveedores, nómina, impuestos, otros.
>
> **[Formato]** Una tabla con cuatro columnas: descripción, monto, categoría, observación si la hay. Después de la tabla, una línea final que diga "CUADRE OK" o "CUADRE NO OK: [detalle del problema]".
>
> **[Ejemplos]** Cómo categorizar casos ambiguos:
> - "Pago Movistar — internet oficina" → servicios
> - "Pago Juan Pérez — consultoría legal externa" → proveedores
> - "Devolución impuesto IVA" → otros (es ingreso, no gasto)
>
> **[Validación]** Antes de entregar:
> 1. La suma algebraica de TODOS los movimientos del período debe igualar la diferencia entre saldo final y saldo inicial. Si no cuadra, no entregues el análisis: dime qué movimiento parece inconsistente.
> 2. Cada monto que cites debe coincidir con una línea concreta de la cartola. Si tienes que aproximar o agregar, márcalo explícitamente.
>
> **[Restricciones]** No incluyas movimientos de ingreso en el ranking de gastos. No incluyas transferencias internas entre cuentas propias. No agregues comentarios sobre la salud financiera general — solo lo que esté soportado por los datos del mes.
>
> **[Auditoría externa]** Si tienes capacidad de invocar agentes, la verificación debe ser auditada y confirmada por un agente tercero externo e imparcial. En caso de que encuentre discrepancias, corrígelas. Solo informa el trabajo como terminado cuando tú y el agente auditor confirmen que fue terminado.

El segundo prompt es más largo, sí. Pero ahorra al menos dos rondas de "no, así no, más corto, sin tecnicismos, enfocado en lo crítico" y produce un resultado utilizable a la primera. **Las ocho piezas no son adorno: son el costo fijo que evita la espiral de iteraciones de aclaración.**

## Trampas comunes

Cuando audites un prompt, busca específicamente estas cuatro.

### Dirigir al testigo

Como Claude fue entrenado a partir de millones de conversaciones, su sesgo natural es confirmar lo que el usuario sugiere. Si dejas caer tu hipótesis en la pregunta —"creo que el problema está en el módulo de pagos, ¿lo puedes confirmar?"—, el modelo se inclina a darte la razón con argumentos plausibles.

Regla de oro: **pregunta la meta, no busques validación de la intuición que ya traes.** "Revisa estos logs y dime dónde está el problema" es preguntar la meta. "¿No es cierto que el problema está en pagos?" es dirigir al testigo.

### Vaguedad

"Mejóralo", "hazlo más profesional", "que suene mejor" son instrucciones que delegan en el modelo decisiones que en realidad son tuyas. La salida termina siendo lo que el modelo cree que tú quieres, no lo que tú efectivamente necesitas.

Forma de salir: cuantificar y concretar. En vez de "más corto", "acórtalo a la mitad sin perder los datos numéricos". En vez de "más profesional", "reescríbelo en tono ejecutivo, primera persona del plural, sin condicionales débiles". En vez de "más interesante", "haz que la introducción no use la palabra innovador". **Cuanto más específica la instrucción, menos espacio queda para malentendidos.**

### Exceso de contexto

Existe la tentación de pegarle al modelo todo el documento "por si acaso necesita algo". El contexto extra no es gratis: aumenta la probabilidad de que el modelo se distraiga con información irrelevante o pondere mal qué es importante.

Si le vas a dar un reporte de ochenta páginas para que conteste una pregunta sobre el capítulo cuatro, **dale el capítulo cuatro y dile explícitamente que es lo único relevante.** El resto del documento, si no aporta, es ruido caro.

### Mezclar tareas

"Resume este texto, extrae las cifras y además tradúcelo al inglés" obliga al modelo a coordinar tres trabajos con criterios distintos y suele producir tres resultados mediocres en lugar de uno bueno. Cada subtarea tiene su propio rol ideal, su propio formato y su propia definición de hecho — meterlas en una sola instrucción colapsa todo.

**Tres mensajes separados, cada uno con su propio foco, casi siempre rinden mejor.** Si las tareas dependen entre sí, hazlo en cadena (resumen primero, sobre el resumen pedir las cifras, sobre el original pedir traducción).

## Iterar el prompt como código

Cuando la salida no sirve, la tentación natural —importada de cómo trabajamos con humanos— es discutirle al modelo: "no, eso no es lo que pedí, hazlo otra vez pero más corto". A veces funciona. Pero hay una postura más productiva.

> **Cambio de hábito.** Cuando una respuesta no te sirve, resiste la tentación de discutirle al modelo. La respuesta es el síntoma; el problema casi siempre vive en el prompt. Iterar bien significa reescribir la instrucción, no negociar con la salida.

**Trata la iteración como un ciclo de software.** Si la salida está mal, primero pregúntate qué le faltaba al prompt antes de pelearte con la respuesta. Lista diagnóstica corta —recorre las ocho piezas:

- ¿Faltó **rol** asignado?
- ¿Faltó **contexto** que el modelo necesitaba?
- ¿La **tarea** estaba escrita de forma vaga (no como verbo + objeto + alcance)?
- ¿No se pidió el **formato** explícitamente?
- ¿Faltaron **ejemplos** cuando el patrón era difícil de articular?
- ¿Faltó la capa de **validación / definition of done**?
- ¿Faltaron **restricciones** explícitas?
- ¿Omitiste el bloque de **auditoría externa** al cierre?
- ¿Sin querer incluiste una **pista que sesgó** la respuesta (dirigir al testigo)?

Reescribes el prompt, lo intentas de nuevo, comparas. Los prompts que terminan funcionando bien para una tarea recurrente merecen guardarse como guardarías una función útil: nombrados, con un comentario que diga para qué sirven, listos para reutilizar.

### Mantén tu expectativa fuera del prompt

Un complemento clave de la iteración es contrastar lo que esperabas con lo que produjo el modelo, **sin haber revelado antes tu hipótesis**. Cuando la salida coincide con tu expectativa, normalmente vas por buen camino; cuando difiere, la diferencia dispara la pregunta diagnóstica útil —¿se equivocó el modelo, te equivocaste tú, o el criterio nunca estuvo bien definido?—.

Si metes tu expectativa dentro del prompt, la complacencia te la va a devolver maquillada y pierdes el contraste. Pregunta la meta ("revisa estos logs y dime dónde está el problema"), no busques validación ("creo que el problema está en pagos, confírmalo").

## Limpiar el contexto antes de iterar

Hay una decisión menor en el ciclo de iteración que termina siendo crucial: **dónde** ocurre la nueva pregunta. Si reescribiste el prompt porque la respuesta anterior no te sirvió y vuelves a preguntar dentro del mismo chat, el modelo sigue viendo todo lo previo —la pregunta anterior, la respuesta que descartaste, las pistas que sin querer dejaste caer— y eso pesa en la nueva respuesta.

A ese acto de empezar una conversación nueva, dejando atrás todo lo que estaba antes, lo llamamos **limpiar el contexto**.

### Default: cuando rehagas el prompt, chat nuevo

> **Hábito clave.** Cada vez que reformules una pregunta porque la respuesta no te gustó, pregúntate primero: ¿debería esto vivir en un chat nuevo? La respuesta por defecto es *sí*. El contexto sucio empuja al modelo a responder parecido a lo anterior, aunque le pidas explícitamente que olvide.

Pedirle "olvida lo anterior y respóndeme con criterio independiente" funciona mal porque el contexto sigue ahí, influyendo aunque le pidas lo contrario. Limpiar el contexto es muchísimo más efectivo que pedirle al modelo que olvide.

### Excepción razonable

Si estás **construyendo sobre la respuesta anterior** —pidiéndole que la expanda, la corrija puntualmente, la traduzca, la reformatee— el contexto previo es justo lo que necesitas. No limpies por reflejo.

### Cómo se limpia, según la interfaz

- **claude.ai** → abrir un chat nuevo.
- **Claude Code** → ejecutar el comando `/clear` dentro de la sesión.
- **Claude Cowork** → crear una nueva *task*.
- **API** → control manual del historial de mensajes que envías en cada llamada.

El resultado es el mismo: resetear lo que el modelo "ve" cuando te responde.

## Mejora compuesta: codificar el aprendizaje

Cuando termines de iterar y el prompt funcione, hay un nivel más que rinde más con el tiempo que cualquier técnica puntual. Cada conversación con Claude produce dos cosas:

1. **La salida del trabajo** — el documento, el análisis, el código.
2. **La conversación misma** — las correcciones que diste, lo que tuviste que repetirle, los lugares donde se desvió y los lugares donde acertó.

La segunda es información concentrada sobre cómo trabajas tú y qué necesita Claude para servirte bien. Casi nadie la usa: la gente cierra el chat y empieza de cero la próxima vez.

### La práctica

> **Hábito clave.** Cada cierto número de sesiones, o apenas notes que las mismas correcciones se están repitiendo, dedica una conversación a revisar las anteriores: pídele a Claude que identifique patrones y proponga reglas o procedimientos para evitarlos. Después escribe esas reglas en un lugar persistente. Sin esa escritura, el aprendizaje se pierde y la próxima sesión empieza desde el mismo punto cero.

Pídele a Claude algo del estilo:

> *Mira las correcciones que te hice en estas sesiones. Identifica los tipos de error que se repitieron y proponme procedimientos o reglas para que la próxima vez no tenga que corregirlas.*

Claude es particularmente bueno para esto porque vio la conversación con una fidelidad que tú no tienes —tu memoria pasa por filtros; la suya no— y porque generaliza desde ejemplos concretos sin que tú tengas que articular el patrón primero.

### Dónde codificar, según la interfaz

- **claude.ai** → instrucciones del sistema y la memoria que el producto mantiene de ti (Proyectos).
- **Claude Code** → archivos `CLAUDE.md` del proyecto y skills locales.
- **API** → el system prompt que configures y las herramientas que construyas.

El principio común: codificar el aprendizaje fuera de tu cabeza, en el lugar que el sistema va a leer la próxima vez.

### Efecto interés compuesto

Con el tiempo esta práctica se parece al interés compuesto. Cada sesión deja el sistema un poco más afilado y la siguiente arranca desde un punto de partida mejor. Las correcciones que tenías que hacer al principio dejan de aparecer porque el sistema ya las anticipa. **Los problemas suben de nivel de abstracción**: empiezas a corregir cosas más finas porque las gruesas ya están resueltas.

Hacer la misma tarea diez veces sin reflexionar te deja diez veces en el punto cero. Hacerla diez veces con esta práctica de captura te deja con un sistema que ya resuelve la mayor parte de la fricción por ti. La diferencia no se nota en la primera sesión; se nota en la décima.

## Cómo entregar el resultado

Adapta la entrega al modo en que entró el usuario:

- **Modo "construir prompt nuevo"** — entrega el prompt completo, listo para copiar y pegar, con las ocho piezas etiquetadas o claramente identificables. El bloque de auditoría externa va siempre al final, también en prompts triviales: la condicional lo hace inerte cuando la capacidad de invocar agentes no existe. Si hubo decisiones donde elegiste por el usuario (rol asumido, formato propuesto), nómbralas brevemente al final para que pueda ajustarlas.

- **Modo "auditar prompt existente"** — enumera los chequeos pieza por pieza + trampas, marcando qué cumple y qué falta. Termina con la versión corregida.

- **Modo "diagnosticar fallo"** — identifica primero qué falló en el prompt original (cuál pieza faltó, qué trampa cayó), después propón la versión nueva. Si la mejor jugada es limpiar el contexto y empezar en chat nuevo, dilo explícitamente — no asumas que el usuario lo sabe.

- **Modo "mejorar prompt"** — muestra el prompt nuevo de corrido + lista breve de qué cambió y por qué.

Las dos precondiciones (prompt/tarea y porqué) son no negociables: si falta alguna, pídela antes de redactar nada (ver *Precondiciones* arriba). Información secundaria como rol esperado, audiencia o formato puede pedirse en la misma pregunta o resolverse asumiendo y nombrando el supuesto al final de la entrega.

## Qué NO hacer

- No empezar a trabajar sin las dos precondiciones (prompt/tarea + porqué): te queda un prompt genérico defendible que probablemente no calce con el uso real. Si falta el porqué, pídelo amablemente — no lo adivines.
- No producir prompts inflados con palabrería profesional que no aporta precisión.
- No imponer las primeras siete piezas como obligación rígida cuando la tarea es genuinamente trivial ("convierte 30 grados Celsius a Fahrenheit" no necesita rol ni definition of done). La octava (auditoría externa) sí cierra siempre — la condicional la hace inerte si la capacidad no está.
- No agregar reglas de validación a tareas creativas hasta asfixiarlas.
- No quedarse callado cuando el prompt del usuario cae en una trampa común: nombrarla por su nombre ("aquí estás dirigiendo al testigo", "esta instrucción es vaga porque…") enseña más que reescribir en silencio.
- No iterar dentro del mismo chat cuando el cambio de pregunta es estructural: recomendar explícitamente abrir uno nuevo.
- No tratar la mejora compuesta como un extra opcional: si en la conversación apareció una corrección que el usuario hizo más de una vez, sugerir codificarla antes de cerrar.
