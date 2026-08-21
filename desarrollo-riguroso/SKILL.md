---
name: desarrollo-riguroso
description: El estándar de desarrollo de software de Kumo — la forma rigurosa de escribir, testear y corregir código en CUALQUIER proyecto de la empresa, independiente del stack o el dominio. Aplica TDD, verificación contra datos reales, prevención sistémica de bugs, observabilidad y honestidad. Usa esta skill al partir un proyecto nuevo, al sembrar o revisar su CLAUDE.md, al escribir o corregir código, al diseñar el flujo de testing, o cuando el usuario menciona cómo desarrollar, disciplina o estándar de desarrollo, TDD, test-first, arreglar un bug, calidad de código, o cómo hacer las cosas bien. También aplica en frases como "cómo lo desarrollamos", "cuál es nuestro estándar", "haz esto con rigor", "escribe el test primero", "test-driven", o equivalentes en cualquier idioma.
---

# Desarrollo riguroso — el estándar de Kumo

Kumo desarrolla proyectos de todo tipo (ERPs, integraciones, herramientas, servicios). Esta skill es lo que **NO cambia entre proyectos**: la forma de desarrollar. Lo que SÍ cambia —stack, comandos, invariantes de dominio, cuál es el "oráculo de verdad"— vive en el `CLAUDE.md` de cada proyecto, que se **siembra** desde estos principios y se **endurece** con la skill `retrospectiva-de-sesion` tras cada sesión de código.

Los ejemplos marcados *(ej. …)* vienen de proyectos reales; son ilustración, no la norma.

## Principio rector: un test verde puede validar código incorrecto

Un test que pasa NO prueba que el código esté bien — prueba que el código hace lo que el test dice, que puede ser lo incorrecto. El TDD te da correctitud contra los ejemplos que **imaginaste**; los datos reales te dan correctitud contra los que **no**. Por eso todo lo demás gira alrededor de una postura: **no des nada por bueno hasta confrontarlo con la realidad** (datos reales, la implementación de referencia, el comportamiento observable). *(ej. un detector pasó 2 tests sintéticos y produjo 16 falsos positivos contra datos de producción.)*

La forma más pura del test que miente: **un guard DEFINIDO y unit-testeado en verde que NINGÚN call site llama**. El test certifica *la función*, no *su uso* — y da falsa confianza precisamente donde creías estar protegido. Al escribir un invariante-guard: ponlo en el **chokepoint** por donde pasa toda escritura, testea que **la ruta real lo respeta** (no solo que la función lanza), `grep` sus call sites (una función exportada sin caller de producción es un smell), y **dale su operación inversa** — un guard sin escape hatch explícito no protege: bloquea. *(ej. `assertEditable` existía, documentado y verde, mientras el motor idempotente borraba y reposteaba los asientos de meses "congelados" en cada cierre; y su mensaje prometía una "reapertura explícita" que nadie había implementado.)*

Hay una segunda ceguera, complementaria: **el AUTOR no ve los huecos de su propio fix**. Antes de integrar un lote de cambios al trunk —y antes de compoundear sus lecciones— pásalo por **verificación adversarial de contexto fresco**: uno o más escépticos que leen SOLO el diff, sin tu contexto, con el mandato de *romperlo* (ghost-discipline), no de confirmarlo. Caza lo que tú, que lo escribiste, no puedes ver. Es a la revisión de código lo que VERIFY-REAL es a los datos. *(ej. un auditor fresco cazó que un filtro de exclusión del deploy vivía en el empaquetador y no en el `.dockerignore` que el build realmente lee — el autor lo había dado por resuelto.)*

La misma ceguera alcanza a toda **PROPUESTA** que produces —una arquitectura, un plan de fix, una decisión con tradeoffs—, no solo al código. El primer borrador lleva tus errores adentro tanto como un diff, y el dueño del proyecto merece la versión ya endurecida, no tu borrador con la crítica pendiente. Antes de exponerle una propuesta al operador, sométela a un crítico de contexto fresco con mandato de romperla —que lea la propuesta Y el sistema real (código, datos, costos), no tu razonamiento— e itera hasta que sobreviva; recién entonces preséntala. El gate del código es el trunk; el de una propuesta es el operador — ninguno se cruza sin pasar la aduana adversarial. *(ej. real: una propuesta de arquitectura de caching afirmaba −61% de ahorro y pedía una sonda pagada para "medirlo"; un crítico fresco mostró que el −61% era imposible —le cobraba a un dato único la tarifa de uno compartido, el real era ~−20%— y que ese dato el sistema ya lo emitía gratis a CloudWatch. Los dos errores habrían llegado al operador sin la aduana.)*

## Pilar 1 — TDD: rojo → verde → refactor (no negociable)

Todo bug y toda feature empieza por el test que **falla**. Nunca escribir el fix antes del test. El loop:

1. **IDENTIFY** — nombrar la función/línea/condición que rompe en una frase.
2. **REPLICATE (con la forma de los datos REALES)** — reproducir usando la forma de los datos de producción (todos los casos borde del dominio: multimoneda, valores vacíos/cero/nulos como tres estados distintos, unicode, límites), NO un caso de juguete. Si no puedes reproducir, no entiendes el bug.
3. **FAILING TEST** — el test debe fallar contra el código actual, **por la razón correcta**. Confírmalo: borrar cualquier cláusula portante del fix debe romper al menos un test. Un test que pasa con y sin el fix no prueba nada.
4. **FIX** — cambio mínimo y quirúrgico. Sin scaffolding defensivo ni refactors oportunistas.
5. **CONFIRM** — el test del paso 3 pasa; la suite completa y el **preflight** (los checks pre-commit que ningún commit saltea: formato, lint, tipos, tests, build) quedan verdes.
6. **VERIFY-REAL** — para cualquier cosa que compare contra una fuente de verdad o emita señales (detectores, reconciliadores, reportes), **verde no basta**: confrontar contra datos reales ANTES de desplegar, nunca después. El chequeo empírico va antes del deploy; desplegar y "ver qué pasa" es un anti-patrón.

El **refactor** del ciclo es culpable hasta probar que preserva comportamiento: diff del comportamiento viejo completo (side effects, polaridad de condiciones, defaults) antes de tocar.

## Pilar 2 — Arreglar la CLASE, no el caso

Arreglar el bug en la **capa que es dueña del invariante violado**, no donde aparece el síntoma. Si un helper compartido produce salida incorrecta, se arregla el helper, no un call site. Antes de cerrar, `grep` de cada sitio hermano que comparte el patrón (ramas paralelas, gemelos sync/async, fast/slow path, cada caller del helper cambiado) y arreglarlos en el mismo cambio — o decir explícitamente cuál se excluye y por qué.

## Pilar 3 — Observabilidad: entender cada cosa, o gritar

El objetivo no es cero errores, es **cero errores INVISIBLES**. Postura de fiscalizador: ningún estado/movimiento se acepta sin entender su contraparte; si no se entiende, se levanta la alarma y se investiga de inmediato. Reglas duras:

- **Explicar, nunca silenciar.** Los falsos positivos de una alarma se resuelven creando un MÉTODO que EXPLIQUE el caso (categorizarlo), jamás relajando o escondiendo el detector. Relajar la observabilidad para bajar ruido la vuelve inútil.
- **Un check nuevo nace verde y SIN excepciones.** Si al integrar un test/gate/validador nuevo este detecta un problema PREEXISTENTE, primero se arregla el bug (con su loop completo) y después se integra el check — jamás se mergea con allowlists, `xfail`, `skip` o exclusiones "temporales" para convivir con el bug: las exclusiones se olvidan y el sistema de seguridad nace mintiendo (cobertura aparente sin cobertura real). Si el fix espera una decisión, el check espera junto al fix — un check que documenta un bug en vez de prevenirlo es teatro. *(ej. un walker estricto anti-drift de contrato iba a nacer con una exclusión para un campo interno que ya se filtraba al cliente; lo correcto fue sanitizar el campo primero y mergear el walker sin excepciones.)*
- **Cada fix suma su observabilidad.** Todo bug fix pregunta: ¿qué señal habría gritado esto ANTES? Si la respuesta es "ninguna", el fix incluye esa señal — no solo corrige el síntoma.
- Ante la duda, el sistema **levanta la alarma para que un humano valide**, en vez de adivinar en silencio.

## Pilar 4 — Hacer imposibles los estados inválidos

Los errores del compilador son mejor feedback que una guía de estilo (o que un test). Prefiere que el **tipo** impida el estado inválido antes que un test que lo cace. *(ej. dar a "monto" su moneda en el tipo → sumar CLP+EUR pasa a ser error de compilación, no un pool silencioso.)* El test verde puede mentir; el tipo no.

## Pilar 5 — Una sola fuente de verdad

Un dato vive en un solo lugar; los consumidores se derivan de él y se actualizan **atómicamente**. Nunca copiar un helper, constante o tabla entre módulos (ni entre el lado que escribe y el que lee un formato) — compartir o derivar. Un cambio de firma/enum/campo obliga a auditar cada switch, constructor y serializador que lo toca (los call sites viejos compilan y fallan en silencio).

**Si el dato VARÍA EN EL TIEMPO** (una tarifa, un precio, una tasa, un parámetro de cálculo), esa única fuente debe ser **effective-dated**: un cambio se agrega como una versión NUEVA con su vigencia, y **jamás se pisa el valor anterior**. Editar el valor viejo **reescribe el pasado**: todo lo ya calculado con él —costos, márgenes, cierres validados contra un tercero— cambia solo y en silencio. Es la misma falla que mutar un período ya cerrado, pero por la vía de la CONFIGURACIÓN, y por eso se escapa de los guards que solo miran el libro. *(ej. un proveedor subió su tarifa 10%: pisar la constante habría re-costeado meses ya cuadrados al peso con el contador.)* Regla práctica: si un valor alimenta un cálculo histórico, pregúntate "¿qué pasa con lo ya calculado si lo edito?" — si la respuesta es "cambia", necesita vigencia, no edición.

## Pilar 6 — Honestidad brutal

Nunca sobre-vender lo hecho. Si algo no se verificó, decirlo. Si un paso se saltó, decirlo. Si un deploy falló, exponerlo. "Verificado a mano", "tests existentes" sin nombrar, y "debería funcionar" no cuentan. El contrato de confianza depende del reporte preciso — vale más un "no sé si esto está bien" que un verde falso.

**Y el informe se escribe para quien DECIDE, no para lucir el análisis.** Un reporte que el lector no entiende **no está entregado**, por riguroso que sea por dentro. Señal inequívoca de fallo: que te digan *"no entiendo nada"* o *"me hablas críptico"* — ahí el error es tuyo, no del lector. Antes de entregar: ¿la conclusión está en la PRIMERA línea y en palabras del negocio (no del stack)? ¿sacaste la jerga, los IDs, los ARNs y las tablas que el lector no necesita para decidir? ¿queda claro **qué pasa, por qué importa y qué hacer**, sin descifrar nada? **Densidad no es rigor:** el rigor va en el trabajo, la claridad va en la entrega. El detalle técnico se ofrece aparte, para quien lo pida.

Dos casos de la misma regla que muerden distinto: (a) **una CONFIRMACIÓN** («¿está listo?», «¿está desplegado?») se responde con el sí/no en una frase más **pruebas que el lector pueda verificar por sí mismo** (una URL que puede abrir, un escáner público que puede correr), no con la tabla de checks del que verificó; la señal de fallo es que **repitan la pregunta recién respondida** — la respuesta anterior no respondió en su idioma. (b) **Si el usuario trae un checklist con validador ejecutable** (un escáner con API, una suite, un oráculo externo), la respuesta es la salida REAL de ese validador ítem por ítem (pass/fail/no-aplica), nunca un resumen narrativo propio. *(ej. real: tres escaladas de la misma pregunta en una sesión — «¿está en mi web?», «¿está desplegado?», y la tercera con el checklist del escáner pegado — hasta que la respuesta fue la salida del escáner mismo.)*

## Jamás botar trabajo hecho

Cuando un proceso se detiene, se relanza o se corrige a mitad de camino (política de modelo equivocada, config mala, entorno incorrecto, run interrumpido), **lo ya generado se cosecha y se reutiliza — solo lo nuevo se rehace bajo la política corregida**. Antes de relanzar desde cero, preguntarse siempre: ¿qué produjo el run anterior que siga siendo válido? Los artefactos parciales (journals, logs, outputs intermedios, borradores) son trabajo pagado: se extraen, se marcan con su procedencia/nivel de verificación, y entran como insumo de la síntesis. Botar output válido para "empezar limpio" es el mismo pecado que el rewrite innecesario de código que funciona. *(ej. un run de investigación se detuvo por correr en el modelo no autorizado; el journal ya tenía 102 afirmaciones extraídas de 21 fuentes y 12 veredictos — se cosecharon del `journal.jsonl` y se fusionaron con el run corregido en vez de descartarse.)*

## Antes de BORRAR en infraestructura compartida

Una operación destructiva sobre infraestructura no se juzga por el nombre del recurso sino por
**quién depende de él**. En una cuenta/cluster/VPC compartida —lo normal en una consultora o un
proyecto multi-cliente— el nombre y las etiquetas son una **PISTA, no una prueba**: un recurso
puede llamarse como tu proyecto y estar sirviendo a otro, o no tener etiqueta alguna.

**Regla:** antes de borrar, detener o modificar, (a) identifica POSITIVAMENTE al dueño y (b)
verifica que **nada lo referencia** — quién apunta a él, qué lo usa, a qué está adjunto. La
prueba es la referencia real, no la convención de nombres. Ante la mínima duda: **no se toca, se
pregunta.** El costo de preguntar es un minuto; el de borrar el recurso de otro cliente es su
producción caída y tu credibilidad.

**Y verifica DESPUÉS**, no solo antes: busca las referencias colgando (rutas en `blackhole`,
montajes muertos, dependencias rotas). Una limpieza sin chequeo posterior no está terminada.
*(ej. real: se limpió una cuenta AWS asumida como dedicada filtrando por prefijo de nombre;
resultó ser multi-cliente con producción de terceros. La limpieza estuvo bien acotada, pero el
método —confiar en el nombre— habría fallado con un solo recurso mal etiquetado.)*

## Una operación que persiste MEDIA VERDAD no es atómica

Cuando una operación recibe un hecho y lo escribe en un modelo que **no puede expresarlo
entero**, la parte que no cabe **se pierde por construcción** — y como el resto sí se
grabó, nada falla y nadie se entera. Es el bug silencioso más caro: no hay excepción, no
hay test rojo, solo un dato que no está.

El olfato: **¿algún campo del input NO aparece en lo que se persiste?** Si la operación
deriva su salida re-leyendo lo que acaba de escribir (reconstruir B desde A), todo lo que
A no sepa expresar desaparece. *(ej. real: una factura en EUR se convertía a CLP para el
asiento contable; la cuenta por pagar se re-derivaba DESDE el asiento, y una partida doble
solo sabe de pesos → el monto original en euros se evaporaba, y había que parchearlo a
mano después.)*

Las cuatro preguntas, prestadas de ACID, que endurecen cualquier operación de escritura:

- **Atomicidad** — ¿se graba el hecho COMPLETO o no se graba nada? Dos escrituras separadas
  donde la segunda puede quedar corta son media verdad esperando a ocurrir.
- **Consistencia** — ¿el estado inválido es siquiera REPRESENTABLE? Si el esquema permite
  "monto en divisa sin su divisa", va a existir. Prohibirlo (constraint/tipo/guard) es más
  barato que detectarlo (ver Pilar 4).
- **Aislamiento** — ¿un reintento COMPLETA o no hace nada en silencio? Un `onConflictDoNothing`
  sobre una fila incompleta la deja incompleta para siempre.
- **Durabilidad** — ¿el hecho y su respaldo (documento, evidencia) nacen juntos, o el segundo
  queda "para después"? Lo que queda para después queda.

Y para lo que ya se coló: un **detector que lo reporte** (nunca silenciarlo), y la reparación
leyendo la **fuente original** (el documento real), no estimando.

## Manejo de errores

Nunca tragar una falla ni señalar éxito sobre una (`catch {}`, defaults silenciosos, retornos de I/O descartados convierten errores diagnosticables en corrupción silenciosa). Toda falla alcanzable desde input de usuario, red, disco o args es un **error recuperable y tipado**, nunca un panic ni un sentinel mágico. Mensajes accionables: qué recurso falló, qué restricción se violó (con el valor rechazado), y un remedio concreto.

Caso especial legítimo: la falla tragada **a propósito** (un write best-effort que jamás debe romper la lectura que lo dispara). Ahí el response deja de ser señal — el 200 no dice nada — y la verificación se desplaza al **efecto persistido**: el smoke post-deploy LEE el registro/estado que la operación debía dejar, no el status code. Ojo además con el doble ciego de entorno: **los mocks no emulan permisos** (IAM, ACLs) — la clase "operación sin permiso" pasa toda la suite en verde y solo existe en el ambiente real. *(ej. un lazy-repair con `update_item` en un handler históricamente read-only: AccessDenied tragado por el catch best-effort, suite con mocks verde, y el bug solo apareció leyendo la base post-deploy.)*

## Verificar la semántica empíricamente, nunca por nombres

Leer la implementación de cada helper, macro o constante de la que dependes — no confiar en su nombre. Al **reusar** código "confiable", fijar en un test EL SUPUESTO que importas: sobre todo (a) en qué unidad/moneda/tipo compara, y (b) si usa el valor del período o el acumulado. Código confiable trae bugs latentes que se activan con una forma de dato nueva. *(ej. una función reusada comparaba un monto en EUR contra un pool en CLP y escondió el bug.)* Para código portado, la implementación de referencia ES la spec: diferenciar el flujo contra ella antes de "corregir" un bug aparente.

**Los datos de texto no son el texto que crees.** Todo parser de texto plano propio tolera CRLF (`split(/\r?\n/)`), BOM y espacios de cola desde que nace: son invisibles en el editor y rompen el match en silencio. Al diagnosticar «el archivo está bien y no funciona», mira los BYTES del archivo ANTES que la lógica — un dump cuesta un segundo; teorizar sobre el parser cuesta la sesión. Y la otra cara, al ESCRIBIR: una herramienta puede agregar lo invisible (`Out-File -Encoding utf8` de PowerShell 5.1 antepone BOM) — un archivo que otro programa va a leer se escribe con encoding explícito sin BOM. *(ej. real, dos mordidas en una sesión: un `.env` con CRLF dejó al dev server sin NINGUNA clave —`(.*)$` no matcheaba ninguna línea—, y un settings.json escrito con BOM quedó para su lector como config inválida.)*

## El anti-cargo-cult: adopta el principio, re-deriva el mecanismo

La regla más importante al importar prácticas de una referencia de la industria que admires: para CADA práctica preguntar **"¿qué invariante protege, y este proyecto lo tiene?"**

- **Sí** → adoptar el *principio* y **re-derivar el mecanismo** para tu stack y tu escala.
- **No** (protege un invariante que este proyecto no tiene — seguridad de memoria en código nativo, performance en hot paths, gatekeeping de miles de contribuidores) → **descartar**.

Nunca importes un mecanismo sin su invariante. *(ej. fuzzing 24/7 y sanitizers de memoria son la respuesta de dominio de un runtime en C++/Rust; un servicio en un lenguaje con GC y un solo dev no los sostiene ni los necesita.)* Corolario: **usa el mecanismo más simple que los invariantes permitan**, y descarta todo lo que no sobreviva tres meses sin que alguien lo cuide (snapshots que se pudren, tests flaky, ceremonia). Right-size siempre al proyecto real, no al proyecto que admiras.

**Y antes de recomendar una feature PAGADA de un proveedor: (1) verifica en la doc viva de qué plan y de qué eje de facturación cuelga** (los proveedores cobran por ejes independientes — en Cloudflare, plan de CUENTA vs plan de ZONA por dominio; tener uno no da acceso al otro), **(2) pregúntate si la infraestructura que ya controlas da el mismo resultado gratis, y (3) la compra no se propone hasta agotar la vía gratis.** *(ej. real: se recomendó activar «Markdown for Agents» sin decir que exige zona Pro (US$240/año); el usuario frenó la compra preguntando por qué pagar más si ya pagaba Workers — y el origen propio servía el mismo `text/markdown` con un middleware de 30 líneas, costo cero.)*

## El oráculo de verdad varía por proyecto — identifícalo

VERIFY-REAL confronta contra "la verdad", pero la verdad no es igual en todos lados:

- **Oráculo DURO** (un test suite de referencia, un estándar bit-exacto, una spec): espejar fiel — no "corrijas" la referencia; una desviación es tu bug.
- **Oráculo BLANDO** (un humano, un sistema legado que se atrasa o se equivoca, un proceso manual): espejar para cuadrar, PERO cuando la realidad difiere del oráculo (llegó plata que él aún no registró), **no espejes su error: nombra el residual** y déjalo visible hasta reconciliar. Sobre-indexar en "la referencia es la spec" con un oráculo blando te vuelve *menos* correcto.

**Convergencia contra el oráculo = auditar el oráculo.** Cuando varios sistemas INDEPENDIENTES (modelos distintos, implementaciones distintas, personas distintas) convergen en la misma respuesta "incorrecta" según tu oráculo, la probabilidad se invierte: deja de depurar los sistemas y ve a la fuente primaria que el oráculo dice resumir. Lo típico que encuentras: la fuente admite DOS lecturas válidas y el oráculo capturó solo una — el fix es una decisión de convención explícita del dueño del dominio, no un parche. *(Caso real: dos LLMs distintos convergían en un valor "errado" contra el ground truth; el documento fuente tenía dos configuraciones legítimas y el GT había fijado la otra.)*

Identificar cuál tiene el proyecto es parte de sembrar su `CLAUDE.md`.

## Branching y deploy: el trunk es lo que se despliega

El **trunk es la rama que se despliega** — nómbralo explícitamente y **deploya SIEMPRE desde él**:

- **Nombra el trunk en el `CLAUDE.md`.** Si no está escrito cuál es la rama viva, cada agente arranca en frío sin saberlo y el trabajo deriva a la rama activa por default. *(ej. real: un `feature/*` juntó 60 commits y se volvió el trunk de facto sin que ningún doc lo dijera; el script de deploy zippeaba el working tree de esa rama → prod == donde estabas parado, incluso sin commitear.)*
- **Ramas cortas: días, no semanas.** Una feature merge al trunk apenas está lista + preflight verde. Si una rama junta decenas de commits sin mergear, dejó de ser una feature branch: es un fork, y el trunk nominal se vuelve ficción.
- **La dependencia se mergea primero.** Si B depende de A, mergea A al trunk y branchea B desde ahí — nunca apiles B sobre un A sin mergear; si no, "aislar B" es solo la etiqueta (arrastra todo A).
- **Un solo trunk vivo** para un equipo chico. Un modelo multi-rama (feature→dev→main) sin CI que lo *enforce* se abandona en días y produce justo este drift — no lo declares como vigente si no hay quien lo haga cumplir.

## Estilo que se hace cumplir

- **Cambios quirúrgicos.** Tocar solo lo que la tarea pide. Dead code o smells no relacionados se **flaggean, no se borran** en el mismo cambio.
- **El código y los datos son ground truth; el .md solo lleva lo que NO es derivable.** Test de derivabilidad: si una línea se puede VERIFICAR leyendo el código, corriendo una query o mirando `git`, **no va escrita a mano** — se deriva, se enlaza, o se omite. Rota especialmente rápido (NUNCA a mano): **status/progreso** ("hecho", "✓", "validado"), **"implementado en X"**, **conteos**, **valores actuales** — la trampa de "los docs describen el ESTADO ACTUAL" es justo esa (el estado derivable se pudre). Sí van a mano, porque el código no los expresa: decisiones + su PORQUÉ, convenciones, invariantes, cuál es el oráculo, gotchas, lessons, comandos exactos. *(ej. un `CLAUDE.md` afirmaba "RCV en TS, validado vs enero" mientras el RCV vivo era shell-out a Python; el doc quedó atrás del código Y de su propia regla "no narres el código".)*
- **No le preguntes al usuario lo que el sistema ya sabe** (corolario operacional del test de derivabilidad). Antes de pedir un dato de negocio —*"¿a qué tarifa se facturó?"*, *"¿cuándo cambió esto?"*— pregúntate si está en la base, en los documentos ya cargados o en el código. Si está, **se deriva**: preguntar traslada al usuario un trabajo que es tuyo, y encima con peor precisión (él recuerda, la base SABE). Pregunta solo lo que no existe en ningún artefacto: una decisión futura, una intención, un hecho externo nunca registrado. Señal inequívoca de fallo: que te respondan *"¿no puedes revisarlo tú mismo?"*.
- **Comentarios solo con contenido durable no obvio:** invariantes, contratos de ownership/lifetime, deviaciones deliberadas. No narrar lo que el código hace; eso va en el mensaje del commit.
- **Grep el helper antes de escribir uno nuevo.** Ser el único archivo que toca un primitivo crudo es una señal de alerta.
- **La forma más simple y honesta;** deduplicar dentro del propio diff (la segunda vez que aparece un bloque, extraer un helper y usarlo en cada sitio paralelo).

## Sembrar el CLAUDE.md de un proyecto nuevo

El `CLAUDE.md` es el **manual operativo** del proyecto — comandos densos y accionables, no un ensayo. **No improvises su estructura: usa el esqueleto probado en [`reference/plantilla-claude-md.md`](reference/plantilla-claude-md.md)**, que trae las secciones en orden (qué es → build & comandos → ramas y deploy → arquitectura → invariantes y oráculo → bug-fix workflow → testing → patterns → lessons → gotchas → deploy) + las reglas de densidad y un ejemplo trabajado.

Lo esencial al rellenarlo:

- **Comandos EXACTOS del stack**, pegar-y-correr, con su gotcha (`# NUNCA X`) — no "corre los tests".
- **Nombres reales** (rutas, funciones, tablas), no "el módulo de datos".
- Los **invariantes de dominio** + **cuál es el oráculo de verdad** (duro/blando).
- **Marca lo inventado** con `⚠️ confirmar` — un puerto o un default asumido no es verdad hasta confirmarlo.
- **Lessons Learned arranca casi vacía** (semilla); la llena `retrospectiva-de-sesion` sesión a sesión.
- **Déjalo CRECER (efecto compounding), pero léelo completo.** El CLAUDE.md se enriquece con cada `retrospectiva-de-sesion`; **NO lo limites por tamaño** — recortar el contenido mata el aprendizaje acumulado, que es justo el punto. El riesgo no es el largo, es leer solo una página parcial: por eso la **PRIMERA LÍNEA del CLAUDE.md ordena explícitamente** *"si tu Read se trunca, sigue paginando hasta el final antes de actuar — este doc crece con cada sesión"*. Además, pon los anclas operacionales críticos (trunk, deploy, comandos) ARRIBA, para que hasta un lector apurado los capte. *(ej. real: un CLAUDE.md de 730 líneas se cortó en la 601 y la sección de deploy quedó sin leer — el fix es la directiva de paginar, jamás achicar el doc.)*
- **Nada aspiracional en presente.** Un flujo FUTURO escrito en imperativo presente —aunque lo califiques "(modelo objetivo)"— engaña: el lector no sabe si aplica YA. Si el CI o el flujo no existen aún, documenta el flujo MANUAL real (desde qué rama se despliega hoy), no el automatizado que viene. Es la misma regla "estado ACTUAL, no historia" — y su violación más común.

Los principios de esta skill son el default; el `CLAUDE.md` los **aterriza y adapta** con lo propio del proyecto — nunca los contradice sin dejarlo dicho. La filosofía general vive acá; el `CLAUDE.md` no la repite, la concreta.

## Los documentos también se testean

Un `CLAUDE.md`, una skill o un spec son artefactos de información — y como el código, **pueden "leerse bien" y ser inútiles**. "Un test verde puede mentir" aplica a la prosa: un doc que pasa un control de coherencia todavía puede fallar en su propósito. Kumo los endurece con un pipeline de tres skills **en orden**:

`doc-completitud` (que no falte nada) → `doc-narrativa` (que se lea como relato) → **`doc-prueba-de-uso`** (que un lector frío débil pueda EJECUTAR la tarea que el doc habilita).

La prueba de uso es a la prosa lo que **VERIFY-REAL es al código**: se le pasa el documento a un modelo débil con una tarea real y se mira si puede hacerla; lo que tuvo que adivinar es lo que falta concretar. **Explicar ≠ poder hacer.** Antes de dar por bueno un CLAUDE.md o una skill, pásalos por la prueba de uso — es el equivalente documental de no desplegar sin confrontar datos reales.

Un eje distinto y complementario: **verificar los CLAIMS contra el código**. La prueba de uso mide si un lector puede EJECUTAR; esto mide si lo que el doc AFIRMA es CIERTO hoy. Un lector FRÍO extrae cada afirmación verificable del doc (rutas `/api/*`, nombres de funciones, "X está en TS", conteos, "validado", status de un roadmap) y la cruza contra el código/tests/DB/`git` — es la superficie "docs vs realidad" de `auditoria-de-realidad` apuntada al propio `CLAUDE.md`. Hazlo rutina (parte de la retro, o antes de confiar en un doc heredado), no por suerte: el status derivable se pudre en silencio y el autor es ciego a su propio drift. La cura de raíz es no escribirlo a mano (test de derivabilidad, arriba); este gate caza lo que ya se coló.

## La trampa del validador autorreferencial

El error más peligroso no es el bug — es **creer que lo validaste**. Correr tu aparato de validación sobre datos SINTÉTICOS (proyectos inventados, fixtures de juguete, tests diseñados para pasar) se *siente* como rigor y es un lazo cerrado: mide *"¿la herramienta funciona?"*, no *"¿mi realidad es correcta?"*. Un validador validado contra sí mismo nunca toca el mundo. *(ej. real: se validó un set de skills con discovery + prueba de uso SINTÉTICOS —"15/15, 5/5"— mientras un drift de 62 commits en el repo real, visible con un solo `git rev-list --count`, quedó invisible a todo el aparato y lo encontró el usuario, no el sistema.)*

- **Corre tus tests sobre tus artefactos REALES de alto riesgo, no sobre juguetes.** La prueba de uso, sobre el CLAUDE.md que de verdad usas; VERIFY-REAL, contra el prod que de verdad tienes.
- **Invoca el sistema real, no lo aproximes.** Un validador que RASPA lo que debería PARSEAR (una regex sobre el YAML en vez del parser YAML; un check de strings en vez del compilador) comparte el punto ciego de quien lo escribió: valida el modelo que tienes en la cabeza, no lo que ejecuta producción. Corre el parser/compilador/loader real que usa prod y valida sobre SU salida. *(ej. real: el gate de skills medía largo/voseo con regex propia y aprobó una `description` con `: ` sin comillas que el cargador YAML real rechazó —"mapping values are not allowed"—; la cura fue parsear el YAML de verdad, no remendar la regex.)*
- **Un entorno opaco es un oráculo no consultado — instruméntalo ANTES de teorizar.** Cuando lo que falla es un runtime remoto u opaco que no puedes inspeccionar directamente, el primer movimiento NO es hipotetizar la causa ni aplicar un fix especulativo: es hacerlo observable — un diagnóstico seguro corrido DENTRO de ese runtime que devuelva el artefacto primario (estado real de credenciales/config, resolución de binarios, nombres de env vars — presencia, nunca el VALOR de un secreto a la transcripción). Teorizar contra un entorno invisible es adivinar; y heredar el auto-diagnóstico causal del subsistema que falló (tomar su mensaje de error como la causa) propaga su error. Peor: la cirugía invasiva a ciegas sobre un recurso compartido (reemplazar un binario, pisar un symlink) puede empeorar el fallo en vez de arreglarlo. *(ej. real: varias rondas teorizando por qué un routine remoto daba `InvalidClientTokenId` —¿key rotada? ¿token expirado? ¿IP?— hasta que UN diagnóstico in-situ mostró la causa de una: el runtime inyectaba una env var placeholder que tapaba el archivo de credenciales; y encima, un wrapper "clever" aplicado a ciegas sobre el binario `aws` lo dejó colgado.)*
- **Un verificador debe demostrar que ejerció el objeto (prueba de trabajo).** Un auditor que puede devolver "sin hallazgos" sin haber leído nada es un lazo cerrado más: cumple el contrato de salida (el schema, el formato) midiendo el vacío — y el output estructurado *enmascara* el fallo aguas arriba, porque el agente rellena el schema obedientemente en vez de gritar. Exige en el output una prueba de lectura/ejecución (el título real del objeto, una línea textual, el conteo de lo procesado) y trata el **cero hallazgos de la primera pasada como sospecha de instrumento roto**, no como éxito. *(ej. real: dos rondas de lectores ciegos devolvieron "SIN_VACIOS" schema-perfecto sobre un capítulo… porque un bug de argumentos les pasó una lista de archivos VACÍA; la ronda con ruta incrustada y campo obligatorio "resumen_leido" encontró un bloqueante y un error matemático real que el autor no había visto.)*
- **Un verde debe poder ponerse rojo, y el verificador debe decir sobre QUÉ opinó.** La prueba de trabajo del punto anterior contesta *"¿leyó algo?"*; falta contestar *"¿leyó lo correcto?"* y *"¿este verde es capaz de ser rojo?"*. Un verificador que apunta al archivo equivocado no da error: da **verde**, que es el peor resultado posible porque se parece al éxito. Dos reglas baratas: (1) el objetivo **nunca** se escribe a mano en cada instrumento — se resuelve en un solo lugar compartido y el reporte **imprime la ruta que leyó**; (2) antes de creerle a un verde, aliméntalo con una entrada que DEBE fallar y comprueba que falla. Hermano del *«una medición que acusa necesita un control»*: **una que absuelve, también**. *(ejs. reales, misma sesión: un verificador de vocabulario informó "DEUDA CERO — 58 términos" mientras leía la versión ANTERIOR del documento, porque su ruta estaba hardcodeada y había divergido de la de sus dos hermanos; y un guardia de idempotencia que preguntaba `if 'sobrevivir' in texto` para no duplicar una sección se dio por satisfecho con una frase no relacionada y se saltó el archivo.)*
- **El veredicto viaja por un canal, y el canal también miente.** Los dos puntos anteriores endurecen al verificador; falta el cable por el que llega su respuesta. El caso barato y universal: en un shell, `$?` después de una tubería es el código del ÚLTIMO comando de la tubería, no el del verificador — `cmd | tail` convierte todo fallo en éxito aparente, y `cmd > archivo` o `cmd | tee` hacen lo mismo. La regla: **el instrumento se corre solo y su código de salida se lee sin intermediarios**; si necesitas su salida filtrada, captúrala primero y filtra después, o usa `set -o pipefail`. Vale más allá del shell: un `try/except` que envuelve al verificador, un runner que reporta "completado" en vez del veredicto, un schema que solo tiene campo de resultado y no de error — todos son el mismo cable que colorea de verde lo que llegó rojo. Prueba de un segundo: `sh -c "exit 1" | tail; echo $?` debe darte 1 y te da 0. *(ej. real: el test que verifica un parche de privacidad sobre un bot público se corrió con `| tail` y el comando reportó `EXIT=0` mientras el test imprimía "el parche NO está aplicado"; el mensaje era explícito y por eso no hubo daño, pero un fallo más callado se habría leído como canal protegido.)*
- **Un ritual sin enforcement es teatro.** VERIFY-REAL y la retrospectiva derivan si dependen de que alguien se acuerde. Conviértelos en GATES automáticos (un hook, un deploy que se niega fuera del trunk, un check del harness). Lo hace cumplir el harness, no la buena voluntad.
- **Cierra toda sesión con la pregunta adversarial-contra-la-realidad:** *"¿qué problema real y grave es invisible para mi aparato AHORA?"* — sobre el repo/prod real, no un fixture. **Encontrar un error por suerte (porque un humano lo señaló) NO cuenta como que el sistema funciona.**

## Cuando la verificación es un grafo de agentes

Si vas a montar un fan-out de verificación —o a convertir un flujo lineal en grafo—, **lee
[`reference/esqueleto-de-verificacion.md`](reference/esqueleto-de-verificacion.md) antes de
escribir el script**: trae la forma canónica (ancla → lentes independientes → síntesis →
verificación contra el ancla → decisión del orquestador) y los modos de fallo que cada
skill de Kumo pagó por separado (el ancla que se puede argumentar, el nodo que audita el
vacío, el proponedor sin tope, el juez con sangre contaminada). No lo re-derives ni lo
recuentes en tu skill: instánciala y apunta ahí. La regla de fondo es el Pilar 5 aplicado
al conocimiento — cada skill que recontaba el mismo gotcha era una copia esperando a
divergir, y la quinta se escribió sin heredar ninguna de las cuatro advertencias previas.

**El test de dependencia se le aplica también al PLAN**, no solo al trabajo que el plan
ordena. Sobre cada flecha que dibujes, pregunta *¿el paso B lee la salida de A?* — si no,
es una **arista falsa** y los dos pasos son ramas paralelas. Distingue además la
dependencia de la **compuerta**: «esto va primero porque hay riesgo de pérdida» es una
compuerta, y si se traba no bloquea nada aguas abajo. Dibujar una cadena donde hay ramas
te hace creer que estás bloqueado cuando no lo estás. *(ej. real: un plan de refactor de
skills se escribió 0→1→2→3→4→5; de las cinco flechas, cuatro eran falsas, y el paso puesto
al final era el único que podía arrancar de inmediato.)*

**Si mides ANTES y DESPUÉS, el instrumento no se toca.** Un número «antes» y un número «después»
solo se pueden comparar si los produjo la MISMA medición: el mismo patrón de `grep`, el mismo
prompt, la misma rúbrica, el mismo modelo. Cambiar el instrumento entre las dos tomas produce una
comparación que parece evidencia y no lo es — y el sentido del cambio es arbitrario, así que puede
mostrar una mejora inexistente o una regresión inexistente sobre un artefacto que objetivamente
mejoró. Si tocaste el instrumento, **la única salida honesta es volver a medir el antes con el
instrumento nuevo**; no se compara ni se reporta la diferencia hasta entonces. *(ej. real, dos
veces en una sola sesión: un conteo de duplicados «bajó de 7 a 3» porque el segundo `grep` usaba
otro patrón; y una calificación de diagramas «empeoró» de 3 a 2 porque el segundo prompt del juez
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
artefacto reusable — un lector frío, con ese archivo como única fuente, ejecutando la tarea
que el archivo existe para habilitar. Validar un artefacto reusable releyéndolo es la forma
más débil de verificación que existe.

## Higiene continua del repo — instrumentos, trinquete e informe

Las pruebas responden «¿funciona?». No responden «¿está creciendo mal?». La complejidad,
la duplicación y el código muerto no rompen nada el día que aparecen: se acumulan hasta
que un cambio simple cuesta una tarde. **Lo que no se mide, crece.**

**El encuadre que ordena todo esto, y que es fácil de perder: quien lee, entiende y
modifica el código eres tú (el agente). Las herramientas no refactorizan nada — solo
apuntan dónde mirar.** De ahí se deduce el criterio para elegirlas: sirve la que te
entrega una lista corta, ordenada por lo que ganas, con la ruta y la línea para ir a
leer. No sirve la que te entrega un puntaje, un porcentaje o un tablero. Un número no
dice qué hacer.

### Las tres piezas, y por qué son tres y no una

Confundirlas es el error habitual, porque las tres «miden calidad» y hacen cosas
opuestas.

1. **Instrumentos.** Miden y no opinan. Se configuran una vez y se corren cuando alguien
   pregunta.
2. **Trinquete.** Es un portón. Falla si una métrica **empeoró**. No pide mejorar el
   número histórico, solo no empujarlo hacia arriba. Así una base con deuda vieja se
   puede seguir trabajando sin una limpieza previa imposible.
3. **Informe de oportunidades.** No es portón. Es la lista de trabajo para ti, ordenada
   por líneas ahorrables. Nunca falla, nunca bloquea.

### El trinquete se COMPUTA, jamás se guarda en un archivo

La forma habitual del trinquete es un umbral versionado. **Eso no sirve cuando el
mantenedor es un agente de IA**, porque al ver rojo puede subir el número en el mismo
commit que lo rompe, y nadie se entera. Un número que el mantenedor puede editar no es
un trinquete, es un comentario.

La línea base se calcula. Se mide el árbol de trabajo, se mide el árbol del
`git merge-base` contra el remoto, y se comparan. Para aflojarlo habría que reescribir la
historia del remoto. Y como el portón corre antes de empujar, un número peor nunca llega
al remoto, así que la base solo puede quedarse igual o mejorar. **El trinquete se
sostiene solo.**

Dos trampas medidas en carne propia.

- **Las dos mediciones usan la MISMA vara.** La configuración de las herramientas sale
  siempre del árbol de trabajo, nunca del árbol viejo. Sin eso, estrenar una regla nueva
  se lee como «el código empeoró de 0 a 40», y quitar una regla se lee como una mejora.
  Las dos lecturas son falsas.
- **Toda métrica va en el mismo sentido: menos es mejor.** Si una va al revés, la
  comparación deja de ser una sola y hay que recordar el sentido de cada una, que es
  justo el momento en que alguien se equivoca.

### Leer la salida de una herramienta es una fuente de defectos, no un detalle

Tres lecturas equivocadas seguidas del mismo dato, el mismo día, **y las tres
subestimaban**: una expresión regular sobre el texto con colores dio 1 de 40; leyendo
stdout, el texto de stderr venía pegado al JSON y lo reventaba, dando 0 de 40; y el
puntaje no se llamaba como yo creía, dando 0 otra vez.

Reglas que quedan.

- **Pide el informe en JSON y a un ARCHIVO**, nunca por stdout, que viene mezclado con
  stderr.
- **Una medición que falla dice DESCONOCIDA, jamás cero.** Un cero silencioso se lee como
  «está limpio», que es la conclusión contraria. En el trinquete, un fallo de lectura
  mata el portón en vez de devolver un número inventado.
- **Compara contra la herramienta cruda antes de creerle a tu lector.** Si tu informe
  dice 1 y la herramienta dice 40, el defecto es tuyo.

### Antes de medir, acota. Una medición que incluye lo que no puedes arreglar no sirve

La duplicación de un repo daba 31,92 por ciento y tapaba por completo la real, que era
4,43, porque contaba HTML capturado de un sitio externo que se guarda como evidencia de
pruebas. Y el detector de código muerto marcaba medio repositorio, porque no encontraba
el punto de entrada.

**Cuando un medidor dé una cifra escandalosa, la primera hipótesis es que está midiendo
mal, no que el código esté podrido.** Y cuando la cifra cae de 15 hallazgos a 4 al
arreglar la configuración, esos 11 eran ruido que habría hecho perder una tarde.

Causa concreta que vale la pena tener a mano: **un BOM al inicio de un archivo de
configuración**. El programa principal lo tolera y el resto de las herramientas fallan al
leerlo. Un BOM no rompe nada visible, rompe al siguiente programa que lea el archivo.

### La unidad accionable no siempre es la que reporta la herramienta

Los detectores de clones reportan **parejas**. La unidad sobre la que uno actúa es la
**familia**, o sea todos los sitios que comparten el mismo fragmento. Cuatro copias
producen seis parejas y se leen como seis problemas distintos.

El informe agrupa las parejas en familias (union-find sobre los sitios), ordena por
`(sitios - 1) x líneas`, que es lo que de verdad se ahorra, e **imprime el fragmento
compartido**, para que no haya que abrir cuatro archivos para entender de qué se trata.

Regla general que vale más allá de los clones: **antes de mostrar la salida de una
herramienta, pregúntate cuál es la unidad sobre la que se decide, y agrupa hasta llegar a
ella.**

### Otros lenguajes: se adopta la FUNCIÓN, no el nombre de la herramienta

Nada de esto es de JavaScript. Cada pieza es una **función** y en cada lenguaje hay algo
que la cumple. **Al entrar a un repo, lo primero es inventariar qué lenguajes tiene de
verdad, y buscar el equivalente de cada función para cada uno.** Un repo políglota con
instrumentos en un solo lenguaje deja el resto sin vigilancia y da una tranquilidad falsa,
que es peor que no medir.

| Función | JavaScript y TypeScript | Python | Rust | Go | Java y Kotlin | C y C++ | Multi-lenguaje |
|---|---|---|---|---|---|---|---|
| Formato y reglas de estilo | Biome | Ruff format | rustfmt | gofmt | ktlint, spotless | clang-format | pre-commit |
| Complejidad excesiva | Biome | Ruff, radon | clippy | gocyclo | detekt, PMD | clang-tidy | lizard |
| Código duplicado | jscpd | jscpd | jscpd | dupl | PMD CPD | PMD CPD | jscpd, PMD CPD |
| Exportaciones y archivos muertos | knip | vulture, deptry | cargo-udeps | deadcode | (IDE) | cppcheck | — |
| Grafo de dependencias | dependency-cruiser | pydeps | cargo-modules | go mod graph | jdeps | include-what-you-use | — |
| Vulnerabilidades en terceros | npm audit | pip-audit | cargo audit | govulncheck | OWASP DC | — | Dependabot, Snyk |
| Camino del dato (inyecciones) | CodeQL | CodeQL, bandit | cargo geiger | CodeQL | CodeQL | CodeQL | Semgrep |

Antes de dar una fila por buena, **verifica que la herramienta exista y corra hoy en ese
proyecto**, porque esta tabla envejece. La forma de verificarlo es correrla, no leer su
página.

El trinquete es agnóstico por construcción: cada métrica es una función que recibe una
carpeta y devuelve un número donde menos es mejor. Agregar un lenguaje es agregar una
entrada a esa lista, no reescribir nada.

### Seguridad: es la única capa que las pruebas no pueden cubrir

Una prueba comprueba el resultado de una función. **CodeQL sigue el camino de un dato
entre funciones**, desde donde entra hasta donde se usa, y por eso encuentra inyecciones
y fugas que ninguna prueba unitaria ve. Es gratis en repositorios públicos de GitHub, y
`Semgrep` cubre el caso de los privados.

Tres decisiones que evitan que el análisis se vuelva ruido ignorado.

- **Auditar solo las dependencias de producción.** Una vulnerabilidad en una herramienta
  de desarrollo no llega al despliegue. Mezclarlas alarga la lista, y una lista larga que
  nadie mira no protege nada.
- **Un cron semanal.** Una vulnerabilidad publicada el miércoles no espera al próximo
  commit.
- **Dependabot semanal, no diario.** Una cola de propuestas que nadie alcanza a revisar
  se vuelve ruido, y el ruido se ignora entero.

### Dónde corre cada cosa

- **Al editar**, en el editor. Formato y reglas de estilo.
- **Antes de cada commit**, unos 15 segundos. Compilar y la suite completa. Nada más: un
  portón lento se termina saltando.
- **Antes de cada push**, unos minutos. Exactamente lo que corre el CI, más el trinquete.
  Si tu portón local corre **menos** que el CI, tu verde es de otro color. Abre el archivo
  del CI y compara comando por comando.
- **En el CI**, lo lento y lo programado. Análisis de seguridad y las verificaciones
  contra servicios reales.
- **Cuando toca refactorizar**, a mano. El informe de oportunidades.

Los hooks van **versionados en el repo** con `core.hooksPath`, no en `.git/hooks`, o solo
existen en la máquina de quien los escribió.

### Reglas de commit que se siguen de todo esto

- **Cada arreglo en su propio commit.** Mezclar una limpieza con un cambio de conducta
  hace que ninguna de las dos se pueda revisar ni revertir.
- **El repo se entrega más limpio de lo que estaba.** Antes de escribir el mensaje: qué
  código dejó de usarse con este cambio, qué número o texto quedó repetido en dos
  lugares, qué comentario describe cómo era antes.
- **El commit de formato masivo va solo**, y su SHA se anota en `.git-blame-ignore-revs`
  con `git config blame.ignoreRevsFile`. Sin eso, un solo commit se come el historial de
  autoría de todo el repo.
- **Quien empuja mira el CI.** Y si no va a mirarlo, el portón tiene que correr antes del
  empujón. *(Caso real: 4 commits seguidos en rojo mientras yo declaraba verde, porque yo
  corría menos de lo que corría el CI. El usuario se enteró antes que yo.)*

### Un portón que nadie probó cerrar no es un portón

Introduce a propósito el defecto que el portón existe para atrapar, confirma que se pone
rojo y que sale con código distinto de cero, y **después** revierte. Vale para el
trinquete, para cada comprobación de clase y para cada regla nueva. Una prueba que no
puede fallar da confianza falsa, y es peor que no tenerla.

Dos detalles que muerden al revertir. `git checkout -- archivo` restaura desde el
**índice**, así que si ya hiciste `git add` te devuelve la versión mala: va
`git checkout HEAD -- archivo`. Y los scripts con escapes van a un **archivo**, nunca a un
heredoc, que se come las barras invertidas y rompe las expresiones regulares en silencio.

### Lo que NO hace falta, y por qué

La lista canónica de «herramientas para coordinar un ejército de desarrolladores»
(SonarQube, Sourcegraph, Structure101, Backstage, Snyk) resuelve un problema que casi
ningún proyecto tiene todavía: **fragmentación del conocimiento entre muchas personas y
muchos repos**. Sus funciones de calidad ya están cubiertas por instrumentos locales,
gratis y de segundos, y su regla estrella («que ningún cambio empeore el código») es
exactamente el trinquete, en una versión más débil, porque su umbral se guarda.

El criterio para adoptar una de ellas es una pregunta concreta, no el prestigio de la
herramienta: **¿hay hoy alguien que no encuentra el código que necesita?** Si la respuesta
es no, un buscador universal y un portal de servicios son infraestructura que hay que
mantener sin nadie que la use. El día que sean varios repos y varias personas, se adoptan,
y el orden correcto es primero el buscador (`Sourcegraph`) y mucho después el portal
(`Backstage`).

## Cómo crece este estándar — la paranoia del compounding

Este estándar no es estático. Tras cada sesión de código sustantiva, correr `retrospectiva-de-sesion`: destila las correcciones del usuario y los descubrimientos, y decide qué es **específico del proyecto** (va a su `CLAUDE.md`) y qué es **universal** (vuelve acá, endureciendo el estándar de toda la empresa).

Pero la retro es el ritual de COSECHA, no el momento en que se aprende. Debajo hay una base más profunda, descubierta a los golpes: **un sistema de conocimiento se escribe como BIBLIOTECA (contenido correcto, completo, bien redactado) pero lo que opera es una MÁQUINA (qué se carga, qué se copia, qué se dispara, qué se sincroniza)**. Todo fallo de proceso repetido es un punto donde la biblioteca asumió que la máquina la ejecutaría sola — y la deriva es sistemática, no mala suerte: escribir es barato y mecanizar es caro, así que el gradiente de mínimo esfuerzo produce doctrina sin disparadores, y si el corpus crece más rápido que su mecánica, la fracción de letra muerta tiende a 1.

De ahí la ley: **nada existe hasta que algo lo dispara.** Toda regla nueva necesita tres cosas, no una: el contenido, su **mecanismo de activación no-textual** (un ancla en algo que siempre se carga, un hook, un gate, un guard que revienta ruidosamente, un campo obligatorio de schema) y **la evidencia de su primer disparo real**. Test de activación: «¿qué hace que esto opere cuando nadie está mirando?» — si la respuesta es «la memoria del próximo agente», no está compoundeado: está *declarado*, y se registra como deuda declarada, no como cobertura. El corte del regreso infinito (¿quién vigila al hook?) no es otra capa: es instrumentos que fallan ruidosamente + el humano como oráculo de última instancia — el diseño correcto lo tiene de ÚLTIMO eslabón, nunca de primero.

La actitud que se sigue de la base es la **paranoia por el compounding**: todo caso es sospechoso de ser una clase, y todo aprendizaje no escrito se está perdiendo AHORA. Cinco reflejos — casos de la misma pregunta generadora — en loop constante durante la sesión, no solo al cierre:

1. Ante un fix → **¿caso o clase?** `grep` de los hermanos que comparten el patrón antes de cerrar (Pilar 2).
2. Ante una corrección del usuario → **¿qué principio hay detrás y dónde vive?** El micro-ciclo se dispara EN EL MOMENTO, como parte del mismo fix: arreglar el caso → destilar el principio (la prueba de fuego de la retro) → escribirlo donde vive (el `CLAUDE.md` del proyecto, esta skill, o la skill afectada) → verificar lo escrito. La retro del cierre verifica y completa lo acumulado — no debe ser la primera vez que el aprendizaje se piensa. **Ojo con el alcance angosto:** si la corrección obliga a releer una fuente de verdad (spec, ficha, doc heredado), el principio a destilar no es solo el dato puntual preguntado — re-verifica TODAS las afirmaciones del artefacto en curso contra esa fuente, no solo la corregida. Un documento que contradice tu borrador en un punto es candidato a contradecirlo en otros que no estabas buscando. *(ej. real: una corrección de alcance geográfico mandó a releer una ficha de negocio completa; el dato pedido se extrajo bien, pero una frase a dos líneas de distancia en el mismo documento — que contradecía otra afirmación ya escrita sobre qué ES la empresa — no se corrigió hasta que el usuario señaló el error una segunda vez.)*
3. Ante un resultado limpio → **¿el instrumento midió algo?** (la prueba de trabajo, arriba).
4. Ante una regla o referencia escrita → **¿alguien la sigue?** Un puntero que nadie sigue, una regla que nada dispara, es letra muerta certificable como completa.
5. Ante un «listo» → **¿qué es invisible para mi aparato AHORA?** (la pregunta adversarial, arriba).

**El disparador mecánico del reflejo 2 — instalación por máquina.** El reflejo de compounding no puede depender de la memoria del agente (violaría la propia ley del disparador). Se mecaniza con un hook `UserPromptSubmit` en `~/.claude/settings.json`, que inyecta el check en CADA mensaje del usuario:

```json
"hooks": { "UserPromptSubmit": [ { "hooks": [ { "type": "command", "timeout": 10,
  "command": "echo \"[check-compounding] Si este mensaje del usuario contiene una correccion, una preferencia o una friccion: compoundeala EN ESTE TURNO como parte del mismo fix (caso->clase, principio en una frase, escribirlo donde vive) - ver desarrollo-riguroso, seccion 'paranoia del compounding'. Si el usuario tuvo que repetir algo o pedir el aprendizaje, el reflejo ya fallo.\"" } ] } ] }
```

Sin este hook (u otro disparador equivalente), el reflejo 2 corre como **deuda declarada** en esa máquina — decláralo al sembrar un entorno nuevo. Refuerzo opcional: la misma postura en dos líneas en el `~/.claude/CLAUDE.md` global del usuario.

**Señal inequívoca de que la paranoia falló:** el usuario encontró el problema, o tuvo que pedir el aprendizaje («¿qué aprendimos?», «¿cómo compoundeamos esto?»). Cada vez que pase, el hallazgo N.º 1 de la cosecha es por qué el reflejo no disparó. *(Caso real: en la MISMA sesión en que se endureció todo este aparato, una corrección del usuario se arregló como bug puntual y el principio quedó sin escribir hasta que el usuario lo exigió — el aparato existía; el reflejo que lo dispara es lo que faltaba.)*

Y "acá" significa **el repo `kumo-skills`**, no la copia instalada en `~/.claude/skills/`: la mecánica completa de editar una skill (diff previo, merge del drift, gate, resync, push) vive en el `CLAUDE.md` de ese repo, sección «Cuando Claude edite una skill INSTALADA». Este archivo que estás leyendo puede SER una copia instalada — edítalo en el repo y re-distribuye.
