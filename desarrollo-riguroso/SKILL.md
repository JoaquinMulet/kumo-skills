---
name: desarrollo-riguroso
description: El estándar de desarrollo de software de Kumo — la forma rigurosa de escribir, testear y corregir código en CUALQUIER proyecto de la empresa, independiente del stack o el dominio. Aplica TDD, verificación contra datos reales, prevención sistémica de bugs, observabilidad y honestidad. Usa esta skill al partir un proyecto nuevo, al sembrar o revisar su CLAUDE.md, al escribir o corregir código, al diseñar el flujo de testing, o cuando el usuario menciona cómo desarrollar, disciplina o estándar de desarrollo, TDD, test-first, arreglar un bug, calidad de código, o cómo hacer las cosas bien. También aplica en frases como "cómo lo desarrollamos", "cuál es nuestro estándar", "haz esto con rigor", "escribe el test primero", "test-driven", o equivalentes en cualquier idioma.
---

# Desarrollo riguroso. El estándar de Kumo

Kumo desarrolla proyectos de todo tipo (ERPs, integraciones, herramientas, servicios). Esta skill es lo que **NO cambia entre proyectos**: la forma de desarrollar. Lo que SÍ cambia, stack, comandos, invariantes de dominio, cuál es el "oráculo de verdad", vive en el `CLAUDE.md` de cada proyecto, que se **siembra** desde estos principios y se **endurece** con la skill `retrospectiva-de-sesion` tras cada sesión de código.

Los ejemplos marcados *(ej. …)* vienen de proyectos reales. Son ilustración, no la norma.

## Principio rector: un test verde puede validar código incorrecto

Un test que pasa NO prueba que el código esté bien, prueba que el código hace lo que el test dice, que puede ser lo incorrecto. El TDD te da correctitud contra los ejemplos que **imaginaste**. Los datos reales te dan correctitud contra los que **no**. Por eso todo lo demás gira alrededor de una postura: **no des nada por bueno hasta confrontarlo con la realidad** (datos reales, la implementación de referencia, el comportamiento observable). *(ej. un detector pasó 2 tests sintéticos y produjo 16 falsos positivos contra datos de producción.)*

La forma más pura del test que miente: **un guard DEFINIDO y unit-testeado en verde que NINGÚN call site llama**. El test certifica *la función*, no *su uso*, y da falsa confianza precisamente donde creías estar protegido. Al escribir un invariante-guard: ponlo en el **chokepoint** por donde pasa toda escritura, testea que **la ruta real lo respeta** (no solo que la función lanza), `grep` sus call sites (una función exportada sin caller de producción es un smell), y **dale su operación inversa**, un guard sin escape hatch explícito no protege: bloquea. *(ej. `assertEditable` existía, documentado y verde, mientras el motor idempotente borraba y reposteaba los asientos de meses "congelados" en cada cierre. Y su mensaje prometía una "reapertura explícita" que nadie había implementado.)*

Hay una segunda ceguera, complementaria: **el AUTOR no ve los huecos de su propio fix**. Antes de integrar un lote de cambios al trunk, y antes de compoundear sus lecciones, pásalo por **verificación adversarial de contexto fresco**: uno o más escépticos que leen SOLO el diff, sin tu contexto, con el mandato de *romperlo* (ghost-discipline), no de confirmarlo. Caza lo que tú, que lo escribiste, no puedes ver. Es a la revisión de código lo que VERIFY-REAL es a los datos. *(ej. un auditor fresco cazó que un filtro de exclusión del deploy vivía en el empaquetador y no en el `.dockerignore` que el build realmente lee, el autor lo había dado por resuelto.)*

La misma ceguera alcanza a toda **PROPUESTA** que produces, una arquitectura, un plan de fix, una decisión con tradeoffs, no solo al código. El primer borrador lleva tus errores adentro tanto como un diff, y el dueño del proyecto merece la versión ya endurecida, no tu borrador con la crítica pendiente. Antes de exponerle una propuesta al operador, sométela a un crítico de contexto fresco con mandato de romperla, que lea la propuesta Y el sistema real (código, datos, costos), no tu razonamiento, e itera hasta que sobreviva. Recién entonces preséntala. El gate del código es el trunk. El de una propuesta es el operador, ninguno se cruza sin pasar la aduana adversarial. *(ej. real: una propuesta de arquitectura de caching afirmaba −61% de ahorro y pedía una sonda pagada para "medirlo". Un crítico fresco mostró que el −61% era imposible, le cobraba a un dato único la tarifa de uno compartido, el real era ~−20%, y que ese dato el sistema ya lo emitía gratis a CloudWatch. Los dos errores habrían llegado al operador sin la aduana.)*

## Pilar 1. TDD: rojo → verde → refactor (no negociable)

Todo bug y toda feature empieza por el test que **falla**. Nunca escribir el fix antes del test. El loop:

1. **IDENTIFY.** Nombrar la función/línea/condición que rompe en una frase.
2. **REPLICATE (con la forma de los datos REALES).** Reproducir usando la forma de los datos de producción (todos los casos borde del dominio: multimoneda, valores vacíos/cero/nulos como tres estados distintos, unicode, límites), NO un caso de juguete. Si no puedes reproducir, no entiendes el bug.
3. **FAILING TEST.** El test debe fallar contra el código actual, **por la razón correcta**. Confírmalo: borrar cualquier cláusula portante del fix debe romper al menos un test. Un test que pasa con y sin el fix no prueba nada.
4. **FIX.** Cambio mínimo y quirúrgico. Sin scaffolding defensivo ni refactors oportunistas.
5. **CONFIRM.** El test del paso 3 pasa. La suite completa y el **preflight** (los checks pre-commit que ningún commit saltea: formato, lint, tipos, tests, build) quedan verdes.
6. **VERIFY-REAL.** Para cualquier cosa que compare contra una fuente de verdad o emita señales (detectores, reconciliadores, reportes), **verde no basta**: confrontar contra datos reales ANTES de desplegar, nunca después. El chequeo empírico va antes del deploy. Desplegar y "ver qué pasa" es un anti-patrón.

El **refactor** del ciclo es culpable hasta probar que preserva comportamiento: diff del comportamiento viejo completo (side effects, polaridad de condiciones, defaults) antes de tocar.

## Pilar 2. Arreglar la CLASE, no el caso

Arreglar el bug en la **capa que es dueña del invariante violado**, no donde aparece el síntoma. Si un helper compartido produce salida incorrecta, se arregla el helper, no un call site. Antes de cerrar, `grep` de cada sitio hermano que comparte el patrón (ramas paralelas, gemelos sync/async, fast/slow path, cada caller del helper cambiado) y arreglarlos en el mismo cambio, o decir explícitamente cuál se excluye y por qué.

## Pilar 3. Observabilidad: entender cada cosa, o gritar

El objetivo no es cero errores, es **cero errores INVISIBLES**. Postura de fiscalizador: ningún estado/movimiento se acepta sin entender su contraparte. Si no se entiende, se levanta la alarma y se investiga de inmediato. Reglas duras:

- **Explicar, nunca silenciar.** Los falsos positivos de una alarma se resuelven creando un MÉTODO que EXPLIQUE el caso (categorizarlo), jamás relajando o escondiendo el detector. Relajar la observabilidad para bajar ruido la vuelve inútil.
- **Un check nuevo nace verde y SIN excepciones.** Si al integrar un test/gate/validador nuevo este detecta un problema PREEXISTENTE, primero se arregla el bug (con su loop completo) y después se integra el check, jamás se mergea con allowlists, `xfail`, `skip` o exclusiones "temporales" para convivir con el bug: las exclusiones se olvidan y el sistema de seguridad nace mintiendo (cobertura aparente sin cobertura real). Si el fix espera una decisión, el check espera junto al fix, un check que documenta un bug en vez de prevenirlo es teatro. *(ej. un walker estricto anti-drift de contrato iba a nacer con una exclusión para un campo interno que ya se filtraba al cliente. Lo correcto fue sanitizar el campo primero y mergear el walker sin excepciones.)*
- **Cada fix suma su observabilidad.** Todo bug fix pregunta: ¿qué señal habría gritado esto ANTES? Si la respuesta es "ninguna", el fix incluye esa señal, no solo corrige el síntoma.
- Ante la duda, el sistema **levanta la alarma para que un humano valide**, en vez de adivinar en silencio.

## Pilar 4. Hacer imposibles los estados inválidos

Los errores del compilador son mejor feedback que una guía de estilo (o que un test). Prefiere que el **tipo** impida el estado inválido antes que un test que lo cace. *(ej. dar a "monto" su moneda en el tipo → sumar CLP+EUR pasa a ser error de compilación, no un pool silencioso.)* El test verde puede mentir. El tipo no.

## Pilar 5. Una sola fuente de verdad

Un dato vive en un solo lugar. Los consumidores se derivan de él y se actualizan **atómicamente**. Nunca copiar un helper, constante o tabla entre módulos (ni entre el lado que escribe y el que lee un formato), compartir o derivar. Un cambio de firma/enum/campo obliga a auditar cada switch, constructor y serializador que lo toca (los call sites viejos compilan y fallan en silencio).

**Si el dato VARÍA EN EL TIEMPO** (una tarifa, un precio, una tasa, un parámetro de cálculo), esa única fuente debe ser **effective-dated**: un cambio se agrega como una versión NUEVA con su vigencia, y **jamás se pisa el valor anterior**. Editar el valor viejo **reescribe el pasado**: todo lo ya calculado con él, costos, márgenes, cierres validados contra un tercero, cambia solo y en silencio. Es la misma falla que mutar un período ya cerrado, pero por la vía de la CONFIGURACIÓN, y por eso se escapa de los guards que solo miran el libro. *(ej. un proveedor subió su tarifa 10%: pisar la constante habría re-costeado meses ya cuadrados al peso con el contador.)* Regla práctica: si un valor alimenta un cálculo histórico, pregúntate "¿qué pasa con lo ya calculado si lo edito?", si la respuesta es "cambia", necesita vigencia, no edición.

## Pilar 6. Honestidad brutal

Nunca sobre-vender lo hecho. Si algo no se verificó, decirlo. Si un paso se saltó, decirlo. Si un deploy falló, exponerlo. "Verificado a mano", "tests existentes" sin nombrar, y "debería funcionar" no cuentan. El contrato de confianza depende del reporte preciso, vale más un "no sé si esto está bien" que un verde falso.

**Y el informe se escribe para quien DECIDE, no para lucir el análisis.** Un reporte que el lector no entiende **no está entregado**, por riguroso que sea por dentro. Señal inequívoca de fallo: que te digan *"no entiendo nada"* o *"me hablas críptico"*, ahí el error es tuyo, no del lector. Antes de entregar: ¿la conclusión está en la PRIMERA línea y en palabras del negocio (no del stack)? ¿sacaste la jerga, los IDs, los ARNs y las tablas que el lector no necesita para decidir? ¿queda claro **qué pasa, por qué importa y qué hacer**, sin descifrar nada? **Densidad no es rigor:** el rigor va en el trabajo, la claridad va en la entrega. El detalle técnico se ofrece aparte, para quien lo pida.

Dos casos de la misma regla que muerden distinto: (a) **una CONFIRMACIÓN** («¿está listo?», «¿está desplegado?») se responde con el sí/no en una frase más **pruebas que el lector pueda verificar por sí mismo** (una URL que puede abrir, un escáner público que puede correr), no con la tabla de checks del que verificó. La señal de fallo es que **repitan la pregunta recién respondida**, la respuesta anterior no respondió en su idioma. (b) **Si el usuario trae un checklist con validador ejecutable** (un escáner con API, una suite, un oráculo externo), la respuesta es la salida REAL de ese validador ítem por ítem (pass/fail/no-aplica), nunca un resumen narrativo propio. *(ej. real: tres escaladas de la misma pregunta en una sesión, «¿está en mi web?», «¿está desplegado?», y la tercera con el checklist del escáner pegado, hasta que la respuesta fue la salida del escáner mismo.)*

## Jamás botar trabajo hecho

Cuando un proceso se detiene, se relanza o se corrige a mitad de camino (política de modelo equivocada, config mala, entorno incorrecto, run interrumpido), **lo ya generado se cosecha y se reutiliza, solo lo nuevo se rehace bajo la política corregida**. Antes de relanzar desde cero, preguntarse siempre: ¿qué produjo el run anterior que siga siendo válido? Los artefactos parciales (journals, logs, outputs intermedios, borradores) son trabajo pagado: se extraen, se marcan con su procedencia/nivel de verificación, y entran como insumo de la síntesis. Botar output válido para "empezar limpio" es el mismo pecado que el rewrite innecesario de código que funciona. *(ej. un run de investigación se detuvo por correr en el modelo no autorizado. El journal ya tenía 102 afirmaciones extraídas de 21 fuentes y 12 veredictos, se cosecharon del `journal.jsonl` y se fusionaron con el run corregido en vez de descartarse.)*

## Antes de BORRAR en infraestructura compartida

Una operación destructiva sobre infraestructura no se juzga por el nombre del recurso sino por
**quién depende de él**. En una cuenta/cluster/VPC compartida, lo normal en una consultora o un
proyecto multi-cliente, el nombre y las etiquetas son una **PISTA, no una prueba**: un recurso
puede llamarse como tu proyecto y estar sirviendo a otro, o no tener etiqueta alguna.

**Regla:** antes de borrar, detener o modificar, (a) identifica POSITIVAMENTE al dueño y (b)
verifica que **nada lo referencia**, quién apunta a él, qué lo usa, a qué está adjunto. La
prueba es la referencia real, no la convención de nombres. Ante la mínima duda: **no se toca, se
pregunta.** El costo de preguntar es un minuto. El de borrar el recurso de otro cliente es su
producción caída y tu credibilidad.

**Y verifica DESPUÉS**, no solo antes: busca las referencias colgando (rutas en `blackhole`,
montajes muertos, dependencias rotas). Una limpieza sin chequeo posterior no está terminada.
*(ej. real: se limpió una cuenta AWS asumida como dedicada filtrando por prefijo de nombre;
resultó ser multi-cliente con producción de terceros. La limpieza estuvo bien acotada, pero el
método, confiar en el nombre, habría fallado con un solo recurso mal etiquetado.)*

## Una operación que persiste MEDIA VERDAD no es atómica

Cuando una operación recibe un hecho y lo escribe en un modelo que **no puede expresarlo
entero**, la parte que no cabe **se pierde por construcción**, y como el resto sí se
grabó, nada falla y nadie se entera. Es el bug silencioso más caro: no hay excepción, no
hay test rojo, solo un dato que no está.

El olfato: **¿algún campo del input NO aparece en lo que se persiste?** Si la operación
deriva su salida re-leyendo lo que acaba de escribir (reconstruir B desde A), todo lo que
A no sepa expresar desaparece. *(ej. real: una factura en EUR se convertía a CLP para el
asiento contable. La cuenta por pagar se re-derivaba DESDE el asiento, y una partida doble
solo sabe de pesos → el monto original en euros se evaporaba, y había que parchearlo a
mano después.)*

Las cuatro preguntas, prestadas de ACID, que endurecen cualquier operación de escritura:

- **Atomicidad.** ¿se graba el hecho COMPLETO o no se graba nada? Dos escrituras separadas
  donde la segunda puede quedar corta son media verdad esperando a ocurrir.
- **Consistencia.** ¿el estado inválido es siquiera REPRESENTABLE? Si el esquema permite
  "monto en divisa sin su divisa", va a existir. Prohibirlo (constraint/tipo/guard) es más
  barato que detectarlo (ver Pilar 4).
- **Aislamiento.** ¿un reintento COMPLETA o no hace nada en silencio? Un `onConflictDoNothing`
  sobre una fila incompleta la deja incompleta para siempre.
- **Durabilidad.** ¿el hecho y su respaldo (documento, evidencia) nacen juntos, o el segundo
  queda "para después"? Lo que queda para después queda.

Y para lo que ya se coló: un **detector que lo reporte** (nunca silenciarlo), y la reparación
leyendo la **fuente original** (el documento real), no estimando.

## Manejo de errores

Nunca tragar una falla ni señalar éxito sobre una (`catch {}`, defaults silenciosos, retornos de I/O descartados convierten errores diagnosticables en corrupción silenciosa). Toda falla alcanzable desde input de usuario, red, disco o args es un **error recuperable y tipado**, nunca un panic ni un sentinel mágico. Mensajes accionables: qué recurso falló, qué restricción se violó (con el valor rechazado), y un remedio concreto.

Caso especial legítimo: la falla tragada **a propósito** (un write best-effort que jamás debe romper la lectura que lo dispara). Ahí el response deja de ser señal, el 200 no dice nada, y la verificación se desplaza al **efecto persistido**: el smoke post-deploy LEE el registro/estado que la operación debía dejar, no el status code. Ojo además con el doble ciego de entorno: **los mocks no emulan permisos** (IAM, ACLs), la clase "operación sin permiso" pasa toda la suite en verde y solo existe en el ambiente real. *(ej. un lazy-repair con `update_item` en un handler históricamente read-only: AccessDenied tragado por el catch best-effort, suite con mocks verde, y el bug solo apareció leyendo la base post-deploy.)*

## Verificar la semántica empíricamente, nunca por nombres

Leer la implementación de cada helper, macro o constante de la que dependes, no confiar en su nombre. Al **reusar** código "confiable", fijar en un test EL SUPUESTO que importas: sobre todo (a) en qué unidad/moneda/tipo compara, y (b) si usa el valor del período o el acumulado. Código confiable trae bugs latentes que se activan con una forma de dato nueva. *(ej. una función reusada comparaba un monto en EUR contra un pool en CLP y escondió el bug.)* Para código portado, la implementación de referencia ES la spec: diferenciar el flujo contra ella antes de "corregir" un bug aparente.

**Los datos de texto no son el texto que crees.** Todo parser de texto plano propio tolera CRLF (`split(/\r?\n/)`), BOM y espacios de cola desde que nace: son invisibles en el editor y rompen el match en silencio. Al diagnosticar «el archivo está bien y no funciona», mira los BYTES del archivo ANTES que la lógica, un dump cuesta un segundo. Teorizar sobre el parser cuesta la sesión. Y la otra cara, al ESCRIBIR: una herramienta puede agregar lo invisible (`Out-File -Encoding utf8` de PowerShell 5.1 antepone BOM), un archivo que otro programa va a leer se escribe con encoding explícito sin BOM. *(ej. real, dos mordidas en una sesión: un `.env` con CRLF dejó al dev server sin NINGUNA clave, `(.*)$` no matcheaba ninguna línea, y un settings.json escrito con BOM quedó para su lector como config inválida.)*

## El anti-cargo-cult: adopta el principio, re-deriva el mecanismo

La regla más importante al importar prácticas de una referencia de la industria que admires: para CADA práctica preguntar **"¿qué invariante protege, y este proyecto lo tiene?"**

- **Sí** → adoptar el *principio* y **re-derivar el mecanismo** para tu stack y tu escala.
- **No** (protege un invariante que este proyecto no tiene, seguridad de memoria en código nativo, performance en hot paths, gatekeeping de miles de contribuidores) → **descartar**.

Nunca importes un mecanismo sin su invariante. *(ej. fuzzing 24/7 y sanitizers de memoria son la respuesta de dominio de un runtime en C++/Rust. Un servicio en un lenguaje con GC y un solo dev no los sostiene ni los necesita.)* Corolario: **usa el mecanismo más simple que los invariantes permitan**, y descarta todo lo que no sobreviva tres meses sin que alguien lo cuide (snapshots que se pudren, tests flaky, ceremonia). Right-size siempre al proyecto real, no al proyecto que admiras.

**Y antes de recomendar una feature PAGADA de un proveedor: (1) verifica en la doc viva de qué plan y de qué eje de facturación cuelga** (los proveedores cobran por ejes independientes, en Cloudflare, plan de CUENTA vs plan de ZONA por dominio. Tener uno no da acceso al otro), **(2) pregúntate si la infraestructura que ya controlas da el mismo resultado gratis, y (3) la compra no se propone hasta agotar la vía gratis.** *(ej. real: se recomendó activar «Markdown for Agents» sin decir que exige zona Pro (US$240/año). El usuario frenó la compra preguntando por qué pagar más si ya pagaba Workers, y el origen propio servía el mismo `text/markdown` con un middleware de 30 líneas, costo cero.)*

## El oráculo de verdad varía por proyecto. Identifícalo

VERIFY-REAL confronta contra "la verdad", pero la verdad no es igual en todos lados:

- **Oráculo DURO** (un test suite de referencia, un estándar bit-exacto, una spec): espejar fiel, no "corrijas" la referencia. Una desviación es tu bug.
- **Oráculo BLANDO** (un humano, un sistema legado que se atrasa o se equivoca, un proceso manual): espejar para cuadrar, PERO cuando la realidad difiere del oráculo (llegó plata que él aún no registró), **no espejes su error: nombra el residual** y déjalo visible hasta reconciliar. Sobre-indexar en "la referencia es la spec" con un oráculo blando te vuelve *menos* correcto.

**Convergencia contra el oráculo = auditar el oráculo.** Cuando varios sistemas INDEPENDIENTES (modelos distintos, implementaciones distintas, personas distintas) convergen en la misma respuesta "incorrecta" según tu oráculo, la probabilidad se invierte: deja de depurar los sistemas y ve a la fuente primaria que el oráculo dice resumir. Lo típico que encuentras: la fuente admite DOS lecturas válidas y el oráculo capturó solo una, el fix es una decisión de convención explícita del dueño del dominio, no un parche. *(Caso real: dos LLMs distintos convergían en un valor "errado" contra el ground truth. El documento fuente tenía dos configuraciones legítimas y el GT había fijado la otra.)*

Identificar cuál tiene el proyecto es parte de sembrar su `CLAUDE.md`.

## Branching y deploy: el trunk es lo que se despliega

El **trunk es la rama que se despliega**, nómbralo explícitamente y **deploya SIEMPRE desde él**:

- **Nombra el trunk en el `CLAUDE.md`.** Si no está escrito cuál es la rama viva, cada agente arranca en frío sin saberlo y el trabajo deriva a la rama activa por default. *(ej. real: un `feature/*` juntó 60 commits y se volvió el trunk de facto sin que ningún doc lo dijera. El script de deploy zippeaba el working tree de esa rama → prod == donde estabas parado, incluso sin commitear.)*
- **Ramas cortas: días, no semanas.** Una feature merge al trunk apenas está lista + preflight verde. Si una rama junta decenas de commits sin mergear, dejó de ser una feature branch: es un fork, y el trunk nominal se vuelve ficción.
- **La dependencia se mergea primero.** Si B depende de A, mergea A al trunk y branchea B desde ahí, nunca apiles B sobre un A sin mergear. Si no, "aislar B" es solo la etiqueta (arrastra todo A).
- **Un solo trunk vivo** para un equipo chico. Un modelo multi-rama (feature→dev→main) sin CI que lo *enforce* se abandona en días y produce justo este drift, no lo declares como vigente si no hay quien lo haga cumplir.

## Estilo que se hace cumplir

- **Cambios quirúrgicos.** Tocar solo lo que la tarea pide. Dead code o smells no relacionados se **flaggean, no se borran** en el mismo cambio.
- **El código y los datos son ground truth. El .md solo lleva lo que NO es derivable.** Test de derivabilidad: si una línea se puede VERIFICAR leyendo el código, corriendo una query o mirando `git`, **no va escrita a mano.** Se deriva, se enlaza, o se omite. Rota especialmente rápido (NUNCA a mano): **status/progreso** ("hecho", "✓", "validado"), **"implementado en X"**, **conteos**, **valores actuales**, la trampa de "los docs describen el ESTADO ACTUAL" es justo esa (el estado derivable se pudre). Sí van a mano, porque el código no los expresa: decisiones + su PORQUÉ, convenciones, invariantes, cuál es el oráculo, gotchas, lessons, comandos exactos. *(ej. un `CLAUDE.md` afirmaba "RCV en TS, validado vs enero" mientras el RCV vivo era shell-out a Python. El doc quedó atrás del código Y de su propia regla "no narres el código".)*
- **No le preguntes al usuario lo que el sistema ya sabe** (corolario operacional del test de derivabilidad). Antes de pedir un dato de negocio, *"¿a qué tarifa se facturó?"*, *"¿cuándo cambió esto?"*, pregúntate si está en la base, en los documentos ya cargados o en el código. Si está, **se deriva**: preguntar traslada al usuario un trabajo que es tuyo, y encima con peor precisión (él recuerda, la base SABE). Pregunta solo lo que no existe en ningún artefacto: una decisión futura, una intención, un hecho externo nunca registrado. Señal inequívoca de fallo: que te respondan *"¿no puedes revisarlo tú mismo?"*.
- **Comentarios solo con contenido durable no obvio:** invariantes, contratos de ownership/lifetime, deviaciones deliberadas. No narrar lo que el código hace. Eso va en el mensaje del commit.
- **Grep el helper antes de escribir uno nuevo.** Ser el único archivo que toca un primitivo crudo es una señal de alerta.
- **La forma más simple y honesta;** deduplicar dentro del propio diff (la segunda vez que aparece un bloque, extraer un helper y usarlo en cada sitio paralelo).

## Sembrar el CLAUDE.md de un proyecto nuevo

El `CLAUDE.md` es el **manual operativo** del proyecto, comandos densos y accionables, no un ensayo. **No improvises su estructura: usa el esqueleto probado en [`reference/plantilla-claude-md.md`](reference/plantilla-claude-md.md)**, que trae las secciones en orden (qué es → build & comandos → ramas y deploy → arquitectura → invariantes y oráculo → bug-fix workflow → testing → patterns → lessons → gotchas → deploy) + las reglas de densidad y un ejemplo trabajado.

Lo esencial al rellenarlo:

- **Comandos EXACTOS del stack**, pegar-y-correr, con su gotcha (`# NUNCA X`), no "corre los tests".
- **Nombres reales** (rutas, funciones, tablas), no "el módulo de datos".
- Los **invariantes de dominio** + **cuál es el oráculo de verdad** (duro/blando).
- **Marca lo inventado** con `⚠️ confirmar`, un puerto o un default asumido no es verdad hasta confirmarlo.
- **Lessons Learned arranca casi vacía** (semilla). La llena `retrospectiva-de-sesion` sesión a sesión.
- **Déjalo CRECER (efecto compounding), pero léelo completo.** El CLAUDE.md se enriquece con cada `retrospectiva-de-sesion`. **NO lo limites por tamaño.** Recortar el contenido mata el aprendizaje acumulado, que es justo el punto. El riesgo no es el largo, es leer solo una página parcial: por eso la **PRIMERA LÍNEA del CLAUDE.md ordena explícitamente** *"si tu Read se trunca, sigue paginando hasta el final antes de actuar, este doc crece con cada sesión"*. Además, pon los anclas operacionales críticos (trunk, deploy, comandos) ARRIBA, para que hasta un lector apurado los capte. *(ej. real: un CLAUDE.md de 730 líneas se cortó en la 601 y la sección de deploy quedó sin leer, el fix es la directiva de paginar, jamás achicar el doc.)*
- **Nada aspiracional en presente.** Un flujo FUTURO escrito en imperativo presente, aunque lo califiques "(modelo objetivo)", engaña: el lector no sabe si aplica YA. Si el CI o el flujo no existen aún, documenta el flujo MANUAL real (desde qué rama se despliega hoy), no el automatizado que viene. Es la misma regla "estado ACTUAL, no historia", y su violación más común.

Los principios de esta skill son el default. El `CLAUDE.md` los **aterriza y adapta** con lo propio del proyecto, nunca los contradice sin dejarlo dicho. La filosofía general vive acá. El `CLAUDE.md` no la repite, la concreta.

## Los documentos también se testean

Un `CLAUDE.md`, una skill o un spec son artefactos de información, y como el código, **pueden "leerse bien" y ser inútiles**. "Un test verde puede mentir" aplica a la prosa: un doc que pasa un control de coherencia todavía puede fallar en su propósito. Kumo los endurece con un pipeline de tres skills **en orden**:

`doc-completitud` (que no falte nada) → `doc-narrativa` (que se lea como relato) → **`doc-prueba-de-uso`** (que un lector frío débil pueda EJECUTAR la tarea que el doc habilita).

La prueba de uso es a la prosa lo que **VERIFY-REAL es al código**: se le pasa el documento a un modelo débil con una tarea real y se mira si puede hacerla. Lo que tuvo que adivinar es lo que falta concretar. **Explicar ≠ poder hacer.** Antes de dar por bueno un CLAUDE.md o una skill, pásalos por la prueba de uso, es el equivalente documental de no desplegar sin confrontar datos reales.

Un eje distinto y complementario: **verificar los CLAIMS contra el código**. La prueba de uso mide si un lector puede EJECUTAR. Esto mide si lo que el doc AFIRMA es CIERTO hoy. Un lector FRÍO extrae cada afirmación verificable del doc (rutas `/api/*`, nombres de funciones, "X está en TS", conteos, "validado", status de un roadmap) y la cruza contra el código/tests/DB/`git`, es la superficie "docs vs realidad" de `auditoria-de-realidad` apuntada al propio `CLAUDE.md`. Hazlo rutina (parte de la retro, o antes de confiar en un doc heredado), no por suerte: el status derivable se pudre en silencio y el autor es ciego a su propio drift. La cura de raíz es no escribirlo a mano (test de derivabilidad, arriba). Este gate caza lo que ya se coló.

## La trampa del validador autorreferencial

El error más peligroso no es el bug, es **creer que lo validaste**. Correr tu aparato de validación sobre datos SINTÉTICOS (proyectos inventados, fixtures de juguete, tests diseñados para pasar) se *siente* como rigor y es un lazo cerrado: mide *"¿la herramienta funciona?"*, no *"¿mi realidad es correcta?"*. Un validador validado contra sí mismo nunca toca el mundo. *(ej. real: se validó un set de skills con discovery + prueba de uso SINTÉTICOS, "15/15, 5/5", mientras un drift de 62 commits en el repo real, visible con un solo `git rev-list --count`, quedó invisible a todo el aparato y lo encontró el usuario, no el sistema.)*

- **Corre tus tests sobre tus artefactos REALES de alto riesgo, no sobre juguetes.** La prueba de uso, sobre el CLAUDE.md que de verdad usas. VERIFY-REAL, contra el prod que de verdad tienes.
- **Invoca el sistema real, no lo aproximes.** Un validador que RASPA lo que debería PARSEAR (una regex sobre el YAML en vez del parser YAML. Un check de strings en vez del compilador) comparte el punto ciego de quien lo escribió: valida el modelo que tienes en la cabeza, no lo que ejecuta producción. Corre el parser/compilador/loader real que usa prod y valida sobre SU salida. *(ej. real: el gate de skills medía largo/voseo con regex propia y aprobó una `description` con `: ` sin comillas que el cargador YAML real rechazó, "mapping values are not allowed",. La cura fue parsear el YAML de verdad, no remendar la regex.)*
- **Un entorno opaco es un oráculo no consultado, instruméntalo ANTES de teorizar.** Cuando lo que falla es un runtime remoto u opaco que no puedes inspeccionar directamente, el primer movimiento NO es hipotetizar la causa ni aplicar un fix especulativo: es hacerlo observable, un diagnóstico seguro corrido DENTRO de ese runtime que devuelva el artefacto primario (estado real de credenciales/config, resolución de binarios, nombres de env vars, presencia, nunca el VALOR de un secreto a la transcripción). Teorizar contra un entorno invisible es adivinar. Y heredar el auto-diagnóstico causal del subsistema que falló (tomar su mensaje de error como la causa) propaga su error. Peor: la cirugía invasiva a ciegas sobre un recurso compartido (reemplazar un binario, pisar un symlink) puede empeorar el fallo en vez de arreglarlo. *(ej. real: varias rondas teorizando por qué un routine remoto daba `InvalidClientTokenId`, ¿key rotada? ¿token expirado? ¿IP?, hasta que UN diagnóstico in-situ mostró la causa de una: el runtime inyectaba una env var placeholder que tapaba el archivo de credenciales. Y encima, un wrapper "clever" aplicado a ciegas sobre el binario `aws` lo dejó colgado.)*
- **Un verificador debe demostrar que ejerció el objeto (prueba de trabajo).** Un auditor que puede devolver "sin hallazgos" sin haber leído nada es un lazo cerrado más: cumple el contrato de salida (el schema, el formato) midiendo el vacío, y el output estructurado *enmascara* el fallo aguas arriba, porque el agente rellena el schema obedientemente en vez de gritar. Exige en el output una prueba de lectura/ejecución (el título real del objeto, una línea textual, el conteo de lo procesado) y trata el **cero hallazgos de la primera pasada como sospecha de instrumento roto**, no como éxito. *(ej. real: dos rondas de lectores ciegos devolvieron "SIN_VACIOS" schema-perfecto sobre un capítulo… porque un bug de argumentos les pasó una lista de archivos VACÍA. La ronda con ruta incrustada y campo obligatorio "resumen_leido" encontró un bloqueante y un error matemático real que el autor no había visto.)*
- **Un verde debe poder ponerse rojo, y el verificador debe decir sobre QUÉ opinó.** La prueba de trabajo del punto anterior contesta *"¿leyó algo?"*. Falta contestar *"¿leyó lo correcto?"* y *"¿este verde es capaz de ser rojo?"*. Un verificador que apunta al archivo equivocado no da error: da **verde**, que es el peor resultado posible porque se parece al éxito. Dos reglas baratas: (1) el objetivo **nunca** se escribe a mano en cada instrumento, se resuelve en un solo lugar compartido y el reporte **imprime la ruta que leyó**. (2) antes de creerle a un verde, aliméntalo con una entrada que DEBE fallar y comprueba que falla. Hermano del *«una medición que acusa necesita un control»*: **una que absuelve, también**. *(ejs. reales, misma sesión: un verificador de vocabulario informó "DEUDA CERO, 58 términos" mientras leía la versión ANTERIOR del documento, porque su ruta estaba hardcodeada y había divergido de la de sus dos hermanos. Y un guardia de idempotencia que preguntaba `if 'sobrevivir' in texto` para no duplicar una sección se dio por satisfecho con una frase no relacionada y se saltó el archivo.)*
- **El veredicto viaja por un canal, y el canal también miente.** Los dos puntos anteriores endurecen al verificador. Falta el cable por el que llega su respuesta. El caso barato y universal: en un shell, `$?` después de una tubería es el código del ÚLTIMO comando de la tubería, no el del verificador, `cmd | tail` convierte todo fallo en éxito aparente, y `cmd > archivo` o `cmd | tee` hacen lo mismo. La regla: **el instrumento se corre solo y su código de salida se lee sin intermediarios**. Si necesitas su salida filtrada, captúrala primero y filtra después, o usa `set -o pipefail`. Vale más allá del shell: un `try/except` que envuelve al verificador, un runner que reporta "completado" en vez del veredicto, un schema que solo tiene campo de resultado y no de error, todos son el mismo cable que colorea de verde lo que llegó rojo. Prueba de un segundo: `sh -c "exit 1" | tail; echo $?` debe darte 1 y te da 0. **El caso que más se repite en la práctica es consultar un CI**, porque la salida es larga y la tentación de filtrarla es inmediata. `gh run watch <id> --exit-status | tail` reporta 0 aunque el CI esté rojo. El veredicto se lee del campo, no del texto: `gh run view <id> --json conclusion`. **Y una tarea en segundo plano reporta el codigo del ULTIMO comando de la secuencia**, asi que `git push; echo; tail` avisa "exit code 0" con el push rechazado. El codigo de cada comando se lee al lado del comando, no al final del grupo. *(ej. real: esta misma regla quedó redactada acá y menos de una hora después la rompí así. Una regla abstracta no se reconoce en el momento en que aplica, por eso va con el comando exacto al lado.)* *(ej. real: el test que verifica un parche de privacidad sobre un bot público se corrió con `| tail` y el comando reportó `EXIT=0` mientras el test imprimía "el parche NO está aplicado". El mensaje era explícito y por eso no hubo daño, pero un fallo más callado se habría leído como canal protegido.)*
- **Un ritual sin enforcement es teatro.** VERIFY-REAL y la retrospectiva derivan si dependen de que alguien se acuerde. Conviértelos en GATES automáticos (un hook, un deploy que se niega fuera del trunk, un check del harness). Lo hace cumplir el harness, no la buena voluntad.
- **Cierra toda sesión con la pregunta adversarial-contra-la-realidad:** *"¿qué problema real y grave es invisible para mi aparato AHORA?"*, sobre el repo/prod real, no un fixture. **Encontrar un error por suerte (porque un humano lo señaló) NO cuenta como que el sistema funciona.**

## Cuando la verificación es un grafo de agentes

Si vas a montar un fan-out de verificación, o a convertir un flujo lineal en grafo, **lee
[`reference/esqueleto-de-verificacion.md`](reference/esqueleto-de-verificacion.md) antes de
escribir el script**: trae la forma canónica (ancla → lentes independientes → síntesis →
verificación contra el ancla → decisión del orquestador) y los modos de fallo que cada
skill de Kumo pagó por separado (el ancla que se puede argumentar, el nodo que audita el
vacío, el proponedor sin tope, el juez con sangre contaminada). No lo re-derives ni lo
recuentes en tu skill: instánciala y apunta ahí. La regla de fondo es el Pilar 5 aplicado
al conocimiento, cada skill que recontaba el mismo gotcha era una copia esperando a
divergir, y la quinta se escribió sin heredar ninguna de las cuatro advertencias previas.

**El test de dependencia se le aplica también al PLAN**, no solo al trabajo que el plan
ordena. Sobre cada flecha que dibujes, pregunta *¿el paso B lee la salida de A?*, si no,
es una **arista falsa** y los dos pasos son ramas paralelas. Distingue además la
dependencia de la **compuerta**: «esto va primero porque hay riesgo de pérdida» es una
compuerta, y si se traba no bloquea nada aguas abajo. Dibujar una cadena donde hay ramas
te hace creer que estás bloqueado cuando no lo estás. *(ej. real: un plan de refactor de
skills se escribió 0→1→2→3→4→5. De las cinco flechas, cuatro eran falsas, y el paso puesto
al final era el único que podía arrancar de inmediato.)*

**Si mides ANTES y DESPUÉS, el instrumento no se toca.** Un número «antes» y un número «después»
solo se pueden comparar si los produjo la MISMA medición: el mismo patrón de `grep`, el mismo
prompt, la misma rúbrica, el mismo modelo. Cambiar el instrumento entre las dos tomas produce una
comparación que parece evidencia y no lo es, y el sentido del cambio es arbitrario, así que puede
mostrar una mejora inexistente o una regresión inexistente sobre un artefacto que objetivamente
mejoró. Si tocaste el instrumento, **la única salida honesta es volver a medir el antes con el
instrumento nuevo**. No se compara ni se reporta la diferencia hasta entonces. *(ej. real, dos
veces en una sola sesión: un conteo de duplicados «bajó de 7 a 3» porque el segundo `grep` usaba
otro patrón. Y una calificación de diagramas «empeoró» de 3 a 2 porque el segundo prompt del juez
pedía severidad y explicaba más contexto que el primero.)*

Y el corolario, al re-medir bien: **una nota que no se mueve puede ser insensibilidad del
instrumento, no ausencia de mejora.** Si la rúbrica de un juez incluye un criterio
**inalcanzable** («¿el dibujo sin texto cuenta toda la historia?», «¿el documento no necesita
ningún contexto?»), ese criterio domina la nota, la aplasta contra el piso y la vuelve ciega a
cualquier cambio real. La señal está entonces en los MOTIVOS, no en el escalar: si antes decía
«no hay ninguna pista de que esto sea una decisión» y ahora dice «la forma indica que hay una
decisión», el arreglo funcionó aunque el número sea idéntico. Regla: **lee los motivos del juez
antes que su nota**, y sospecha de toda rúbrica cuyo puntaje máximo nadie puede alcanzar.

**Todo refactor de consolidación necesita su propia ancla,** y el gate de higiene no lo es:
que el linter pase y los disparadores sigan vivos no responde la afirmación que el refactor
está haciendo («ahora se hereda en vez de duplicar»). Dos anclas baratas: una **mecánica y
contable** (`grep` de lo duplicado, que debe quedar en uno) y la **prueba de uso** del
artefacto reusable, un lector frío, con ese archivo como única fuente, ejecutando la tarea
que el archivo existe para habilitar. Validar un artefacto reusable releyéndolo es la forma
más débil de verificación que existe.

## Higiene continua del repo, capas con agujeros en distintos lugares

Las pruebas responden «¿funciona?». No responden «¿está creciendo mal?» ni «¿lo que
entrego dice la verdad?». Esta sección es el aparato para esas dos preguntas.

**El encuadre que ordena todo, y que es fácil de perder. Quien lee, entiende y modifica el
código eres tú (el agente). Ninguna herramienta refactoriza nada, solo apuntan dónde
mirar.** De ahí sale el criterio para elegirlas. Sirve la que entrega una lista corta,
ordenada por lo que se gana, con ruta y línea para ir a leer. No sirve la que entrega un
puntaje, un porcentaje o un tablero. **Un número no dice qué hacer.** Y para elegirlas bien
hay que entender primero cómo un defecto las esquiva.

### El modelo de las láminas de queso, y el peligro de olvidar los agujeros

Piensa en cada control como una lámina de queso suizo. La lámina es la capa que revisa el
código, un linter, la suite, un revisor. Los agujeros son los casos que esa capa no mira, y
los tiene siempre, porque toda capa se construye prediciendo qué defecto va a aparecer y
ninguna predicción cubre lo que su autor no imaginó. **El agujero no es un descuido, es la
forma que tiene esa capa de haber elegido qué mira.**

Apiladas, cada lámina tapa los agujeros de las vecinas, y el defecto pasa solo cuando
encuentra un agujero alineado en todas. De ahí que la conclusión ingenua sea «pon más
capas», y de ahí que sea falsa. **Más capas solo ayudan si sus agujeros están en lugares
distintos.** Una lámina fotocopiada agrega trabajo y no tapa nada, porque sus agujeros caen
exactamente donde los de la original.

Un caso real que lo mide. Un servidor tenía 72 comprobaciones sobre una pieza y cuatro
revisores adversariales (agentes frescos, sin el contexto del autor, cuyo encargo
no es revisar sino **refutar**), con una lente distinta cada uno, encontraron tres defectos
graves en veinte minutos. Las 72 eran la misma lámina fotocopiada 72 veces. Los tres
hallazgos salieron de tres revisores distintos.

De ahí las dos preguntas al agregar un control. **¿Qué clase de defecto atrapa esta capa
que ninguna otra atrapa?** y **si el sistema fallara ahora mismo, ¿esta capa diría algo?**
Si la respuesta a la segunda es no, la capa es decorativa por más verde que se vea.

Y no se responden discutiendo, se responden **midiendo**. Mete un defecto de esa clase a
propósito, corre todas las capas, y anota cuáles hablaron. Si dos hablan siempre juntas,
una de las dos es redundante. Si una no habla nunca, sobra. *(Caso real. Al encender un
análisis de camino de datos, sus primeros hallazgos incluyeron seis declaraciones sin usar
que el linter y el detector de código muerto locales no veían, porque la regla que las
cubre era otra que nadie había encendido. Esa capa se ganó su lugar el primer día, y se
supo porque se comparó lo que dijo cada una sobre el mismo código.)*

### Herramientas de catálogo contra comprobaciones propias

Las herramientas de catálogo miden **forma**. Complejidad, duplicación, código muerto y
estilo. Son baratas, valen la pena, y en un día completo de uso no encontraron ni un solo
defecto de comportamiento.

El defecto grave lo encontró una **comprobación de clase**. Es una prueba corriente, en tu
suite de siempre, que en vez de ejercitar una función **lee el código fuente entero como
texto** y falla si encuentra un patrón que ya causó daño una vez. No mira un caso, mira
la clase, así que también atrapa el código que nadie ha escrito todavía. Ninguna herramienta genérica podía encontrarlo, porque el patrón no es feo
ni complejo ni duplicado, es correcto en forma y mentiroso en contenido.

**Las de catálogo miden la forma. Solo las que nacen de un fallo tuyo miden la verdad de
tu dominio.** Por eso el orden correcto al entrar a un repo es instalar esas herramientas
de catálogo primero, porque son baratas, y entender que **el trabajo real empieza cuando
escribes la primera comprobación derivada de un fallo que ya pasó**.

Corolario que cuesta aceptar. La mayor parte del tiempo de una jornada de higiene no se
va arreglando código, se va **arreglando la medición**. Vale la pena igual, porque una
medición equivocada no es neutra, hace creer que el sistema está sano.

### Las tres piezas, y por qué son tres y no una

Confundirlas es el error habitual, porque las tres «miden calidad» y hacen cosas opuestas.
Diagnóstico, valla y lista de trabajo, en ese orden.

1. **Instrumentos.** Miden y no opinan. Se configuran una vez y los corres tú, en el
   portón de antes de cada commit junto con la suite, y a mano cuando quieras ver cómo está
   una carpeta. Por sí solos no bloquean nada, solo imprimen.
2. **Trinquete.** Es un portón. Falla solo si una métrica **empeoró**. No pide mejorar el
   número histórico, así que una base con deuda vieja se puede seguir trabajando sin una
   limpieza previa imposible.
3. **Informe de oportunidades.** No es portón. Es la lista de trabajo, ordenada por lo
   que se gana. Nunca falla y nunca bloquea, y el porqué importa. Un informe lista todo lo
   que se podría mejorar, o sea casi siempre algo, y si además frena el trabajo te obliga a
   elegir entre atender deuda vieja y avanzar. Esa elección se resuelve una sola vez,
   apagándolo, y ahí pierdes la lista entera por haberla querido obligatoria.

### El trinquete se COMPUTA, jamás se guarda en un archivo

La forma habitual del trinquete es un umbral versionado. **Eso no sirve cuando el
mantenedor es un agente de IA**, porque al ver rojo puede subir el número en el mismo
commit que lo rompe, y nadie se entera. Un número que el mantenedor puede editar no es un
trinquete, es un comentario.

La línea base se calcula. Se mide el árbol de trabajo, se mide el árbol del commit que
devuelve `git merge-base <rama-por-defecto-del-remoto> HEAD`, y se comparan. Esa rama se
resuelve con git y nunca se escribe a mano, porque un `origin/main` clavado revienta en
silencio en un repo cuya rama es `master` (los 2 comandos exactos están en el anexo). Para
aflojar la base habría que reescribir la historia del remoto. Y como el portón corre antes
de empujar, un número peor nunca llega al remoto, así que solo puede quedarse igual o
mejorar. **El trinquete se sostiene solo.**

Dos trampas medidas en carne propia. Las dos mediciones usan la MISMA vara, la del árbol
actual, o estrenar una regla se lee como «el código empeoró de 0 a 40» y quitarla como una
mejora. Y toda métrica va en el mismo sentido, menos es mejor, porque recordar el sentido
de cada una es justo el momento en que alguien se equivoca.

### Verde no significa limpio, y es el error más caro de esta sección

Tres formas distintas del mismo engaño, las tres medidas en un solo día.

- **El código de salida de un trabajo dice si la herramienta CORRIÓ, no si encontró algo.**
  Un análisis de seguridad terminó en verde con 30 alertas abiertas, seis de severidad
  alta. Reportarlo como «pasó» fue falso en sustancia aunque cierto en estado. Lo que se
  lee es el **conteo de hallazgos**, no el estado del trabajo.
- **Un control puede no estar mirando el cambio.** Dos de las cinco comprobaciones verdes
  de cada propuesta apuntaban a la instancia **ya desplegada**, no al código propuesto, así
  que pasaban con cualquier contenido. Antes de contar una capa, verifica **contra qué
  artefacto corre**.
- **Una función puede estar a medio encender.** El archivo de actualizaciones automáticas
  generaba propuestas mientras las **alertas** de esa misma función estaban apagadas en la
  configuración del repositorio. Escribir el archivo no es habilitar la función. Se
  comprueba **pidiéndole su resultado por su interfaz**, y ahí la API contestó «están
  deshabilitadas para este repositorio» con el archivo perfecto y versionado.

Las tres se engloban en una regla. **Prueba el efecto, no la presencia.**

### Qué corre en cada etapa, y por qué la duración NO decide

**Jamás limites lo que se ejecuta por lo que tarda.** Los costos no son comparables. Un
portón lento cuesta minutos, y un defecto que se escapa cuesta un entregable equivocado,
una ronda perdida con quien confía en el resultado, y la confianza en todo el aparato.
Comparar «4 minutos» con «publiqué un dato falso» es comparar unidades distintas.

El criterio correcto para repartir el trabajo entre etapas no es la velocidad, es **qué
información existe recién en esa etapa**. No puedes verificar un despliegue antes de
desplegar. Todo lo demás corre lo antes posible y corre COMPLETO.

- **Al editar**, en el editor. Formato y estilo, que es lo único que de verdad necesita ser
  instantáneo porque corre en cada tecla.
- **Antes de cada commit**, todo lo que se puede saber sin red ni despliegue. Compilar, la
  suite completa, las comprobaciones de clase y los instrumentos.
- **Antes de cada envío**, todo lo anterior más lo que necesita red. Verificación contra
  los servicios reales y el trinquete. Esta etapa corre **exactamente lo que corre la
  integración continua**, sin recortes. Si tu portón local corre **menos** que ella, tu
  verde es de otro color. Abre su archivo de configuración y compara comando por comando.
- **Después de desplegar**, lo que solo existe desplegado. Protocolo y cliente real contra
  la instancia viva. Una pieza que ES un borde solo se prueba cruzándolo.
- **Programado**, lo que depende del mundo y no del código. Vulnerabilidades publicadas
  después del último commit.
- **Cuando toca refactorizar**, a mano. El informe de oportunidades.

Si un portón se vuelve tan lento que estorba, la respuesta es **hacerlo más rápido**
(caché, paralelismo, incremental), nunca ejecutar menos. Recortar la cobertura para ganar
minutos es cambiar una molestia visible por un riesgo invisible.


### Reglas de commit que se siguen de todo esto

- **Cada arreglo en su propio commit.** Mezclar una limpieza con un cambio de conducta hace
  que ninguna de las dos se pueda revisar ni revertir. La excepción legítima es un ayudante
  y su adopción, porque un ayudante que nadie llama es código muerto y el propio detector
  lo marcaría. Cuando uses la excepción, dila en el mensaje.
- **El repo se entrega más limpio de lo que estaba.** Antes de escribir el mensaje, revisa
  qué dejó de usarse con este cambio, qué número o texto quedó repetido en dos lugares, y
  qué comentario describe cómo era antes.
- **El commit de formato masivo va solo**, y su identificador (el SHA del commit) se anota en
  `.git-blame-ignore-revs`, que se activa con
  `git config blame.ignoreRevsFile .git-blame-ignore-revs`. Sin eso, un solo commit se come el historial de todo
  el repo.
- **Quien envía mira el resultado.** Y si no va a mirarlo, el portón tiene que correr antes
  del envío.

### Un portón que nadie probó cerrar no es un portón

Introduce a propósito el defecto que el portón existe para atrapar, confirma que se pone
rojo y que sale con código distinto de cero, y **después** revierte. Vale para el
trinquete, para cada comprobación de clase y para cada regla nueva. Una prueba que no puede
fallar da confianza falsa, y es peor que no tenerla.


### Cuando el portón te bloquea por deuda que no es tuya

El trinquete no es el que bloquea acá, y conviene decirlo porque suena a contradicción. Él
solo compara contra la línea base, así que la deuda vieja le da igual mientras no crezca.
Los que bloquean son los otros portones, el linter, el compilador y las comprobaciones de
clase, que miran el archivo entero y no distinguen qué línea escribiste tú. Tocas un
archivo con deuda de hace un año y se ponen rojos por algo que no hiciste. La reacción
correcta no es saltarse el portón, es **arreglar esa deuda en su propio commit** y después
seguir. Un portón que se salta una vez se salta siempre, y la deuda que bloquea a uno
bloquea a todos.

### Dónde está el resto

El anexo operativo vive en [`reference/higiene-continua.md`](reference/higiene-continua.md)
y lleva lo que se consulta mientras ejecutas. **La receta de 5 pasos para escribir una
comprobación de clase**, que es la pieza que de verdad encuentra defectos, **el núcleo del
trinquete y del informe**, porque los 2 se escriben y no se instalan, **la tabla de
equivalencias por lenguaje**, **el procedimiento de 7 pasos para instalar esto en un repo
que no lo tiene**, cómo leer la salida de una herramienta sin que te mienta, cómo acotar
una medición antes de creerle, cuál es la unidad sobre la que se decide, y qué herramientas
de catálogo NO hacen falta todavía. **Ábrelo al entrar a un repo nuevo**, que es cuando los
7 pasos son la tarea.

## Cómo crece este estándar. La paranoia del compounding

Este estándar no es estático. Tras cada sesión de código sustantiva, correr `retrospectiva-de-sesion`: destila las correcciones del usuario y los descubrimientos, y decide qué es **específico del proyecto** (va a su `CLAUDE.md`) y qué es **universal** (vuelve acá, endureciendo el estándar de toda la empresa).

Pero la retro es el ritual de COSECHA, no el momento en que se aprende. Debajo hay una base más profunda, descubierta a los golpes: **un sistema de conocimiento se escribe como BIBLIOTECA (contenido correcto, completo, bien redactado) pero lo que opera es una MÁQUINA (qué se carga, qué se copia, qué se dispara, qué se sincroniza)**. Todo fallo de proceso repetido es un punto donde la biblioteca asumió que la máquina la ejecutaría sola, y la deriva es sistemática, no mala suerte: escribir es barato y mecanizar es caro, así que el gradiente de mínimo esfuerzo produce doctrina sin disparadores, y si el corpus crece más rápido que su mecánica, la fracción de letra muerta tiende a 1.

De ahí la ley: **nada existe hasta que algo lo dispara.** Toda regla nueva necesita tres cosas, no una: el contenido, su **mecanismo de activación no-textual** (un ancla en algo que siempre se carga, un hook, un gate, un guard que revienta ruidosamente, un campo obligatorio de schema) y **la evidencia de su primer disparo real**. Test de activación: «¿qué hace que esto opere cuando nadie está mirando?», si la respuesta es «la memoria del próximo agente», no está compoundeado: está *declarado*, y se registra como deuda declarada, no como cobertura. El corte del regreso infinito (¿quién vigila al hook?) no es otra capa: es instrumentos que fallan ruidosamente + el humano como oráculo de última instancia, el diseño correcto lo tiene de ÚLTIMO eslabón, nunca de primero.

La actitud que se sigue de la base es la **paranoia por el compounding**: todo caso es sospechoso de ser una clase, y todo aprendizaje no escrito se está perdiendo AHORA. Cinco reflejos, casos de la misma pregunta generadora, en loop constante durante la sesión, no solo al cierre:

1. Ante un fix → **¿caso o clase?** `grep` de los hermanos que comparten el patrón antes de cerrar (Pilar 2).
2. Ante una corrección del usuario → **¿qué principio hay detrás y dónde vive?** El micro-ciclo se dispara EN EL MOMENTO, como parte del mismo fix: arreglar el caso → destilar el principio (la prueba de fuego de la retro) → escribirlo donde vive (el `CLAUDE.md` del proyecto, esta skill, o la skill afectada) → verificar lo escrito. La retro del cierre verifica y completa lo acumulado, no debe ser la primera vez que el aprendizaje se piensa. **Ojo con el alcance angosto:** si la corrección obliga a releer una fuente de verdad (spec, ficha, doc heredado), el principio a destilar no es solo el dato puntual preguntado, re-verifica TODAS las afirmaciones del artefacto en curso contra esa fuente, no solo la corregida. Un documento que contradice tu borrador en un punto es candidato a contradecirlo en otros que no estabas buscando. *(ej. real: una corrección de alcance geográfico mandó a releer una ficha de negocio completa. El dato pedido se extrajo bien, pero una frase a dos líneas de distancia en el mismo documento, que contradecía otra afirmación ya escrita sobre qué ES la empresa, no se corrigió hasta que el usuario señaló el error una segunda vez.)*
3. Ante un resultado limpio → **¿el instrumento midió algo?** (la prueba de trabajo, arriba).
4. Ante una regla o referencia escrita → **¿alguien la sigue?** Un puntero que nadie sigue, una regla que nada dispara, es letra muerta certificable como completa.
5. Ante un «listo» → **¿qué es invisible para mi aparato AHORA?** (la pregunta adversarial, arriba).

**El disparador mecánico del reflejo 2, instalación por máquina.** El reflejo de compounding no puede depender de la memoria del agente (violaría la propia ley del disparador). Se mecaniza con un hook `UserPromptSubmit` en `~/.claude/settings.json`, que inyecta el check en CADA mensaje del usuario:

```json
"hooks": { "UserPromptSubmit": [ { "hooks": [ { "type": "command", "timeout": 10,
  "command": "echo \"[check-compounding] Si este mensaje del usuario contiene una correccion, una preferencia o una friccion: compoundeala EN ESTE TURNO como parte del mismo fix (caso->clase, principio en una frase, escribirlo donde vive) - ver desarrollo-riguroso, seccion 'paranoia del compounding'. Si el usuario tuvo que repetir algo o pedir el aprendizaje, el reflejo ya fallo.\"" } ] } ] }
```

Sin este hook (u otro disparador equivalente), el reflejo 2 corre como **deuda declarada** en esa máquina, decláralo al sembrar un entorno nuevo. Refuerzo opcional: la misma postura en dos líneas en el `~/.claude/CLAUDE.md` global del usuario.

**Señal inequívoca de que la paranoia falló:** el usuario encontró el problema, o tuvo que pedir el aprendizaje («¿qué aprendimos?», «¿cómo compoundeamos esto?»). Cada vez que pase, el hallazgo N.º 1 de la cosecha es por qué el reflejo no disparó. *(Caso real: en la MISMA sesión en que se endureció todo este aparato, una corrección del usuario se arregló como bug puntual y el principio quedó sin escribir hasta que el usuario lo exigió, el aparato existía. El reflejo que lo dispara es lo que faltaba.)*

Y "acá" significa **el repo `kumo-skills`**, no la copia instalada en `~/.claude/skills/`: la mecánica completa de editar una skill (diff previo, merge del drift, gate, resync, push) vive en el `CLAUDE.md` de ese repo, sección «Cuando Claude edite una skill INSTALADA». Este archivo que estás leyendo puede SER una copia instalada, edítalo en el repo y re-distribuye.
