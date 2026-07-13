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

## Pilar 6 — Honestidad brutal

Nunca sobre-vender lo hecho. Si algo no se verificó, decirlo. Si un paso se saltó, decirlo. Si un deploy falló, exponerlo. "Verificado a mano", "tests existentes" sin nombrar, y "debería funcionar" no cuentan. El contrato de confianza depende del reporte preciso — vale más un "no sé si esto está bien" que un verde falso.

## Manejo de errores

Nunca tragar una falla ni señalar éxito sobre una (`catch {}`, defaults silenciosos, retornos de I/O descartados convierten errores diagnosticables en corrupción silenciosa). Toda falla alcanzable desde input de usuario, red, disco o args es un **error recuperable y tipado**, nunca un panic ni un sentinel mágico. Mensajes accionables: qué recurso falló, qué restricción se violó (con el valor rechazado), y un remedio concreto.

Caso especial legítimo: la falla tragada **a propósito** (un write best-effort que jamás debe romper la lectura que lo dispara). Ahí el response deja de ser señal — el 200 no dice nada — y la verificación se desplaza al **efecto persistido**: el smoke post-deploy LEE el registro/estado que la operación debía dejar, no el status code. Ojo además con el doble ciego de entorno: **los mocks no emulan permisos** (IAM, ACLs) — la clase "operación sin permiso" pasa toda la suite en verde y solo existe en el ambiente real. *(ej. un lazy-repair con `update_item` en un handler históricamente read-only: AccessDenied tragado por el catch best-effort, suite con mocks verde, y el bug solo apareció leyendo la base post-deploy.)*

## Verificar la semántica empíricamente, nunca por nombres

Leer la implementación de cada helper, macro o constante de la que dependes — no confiar en su nombre. Al **reusar** código "confiable", fijar en un test EL SUPUESTO que importas: sobre todo (a) en qué unidad/moneda/tipo compara, y (b) si usa el valor del período o el acumulado. Código confiable trae bugs latentes que se activan con una forma de dato nueva. *(ej. una función reusada comparaba un monto en EUR contra un pool en CLP y escondió el bug.)* Para código portado, la implementación de referencia ES la spec: diferenciar el flujo contra ella antes de "corregir" un bug aparente.

## El anti-cargo-cult: adopta el principio, re-deriva el mecanismo

La regla más importante al importar prácticas de una referencia de la industria que admires: para CADA práctica preguntar **"¿qué invariante protege, y este proyecto lo tiene?"**

- **Sí** → adoptar el *principio* y **re-derivar el mecanismo** para tu stack y tu escala.
- **No** (protege un invariante que este proyecto no tiene — seguridad de memoria en código nativo, performance en hot paths, gatekeeping de miles de contribuidores) → **descartar**.

Nunca importes un mecanismo sin su invariante. *(ej. fuzzing 24/7 y sanitizers de memoria son la respuesta de dominio de un runtime en C++/Rust; un servicio en un lenguaje con GC y un solo dev no los sostiene ni los necesita.)* Corolario: **usa el mecanismo más simple que los invariantes permitan**, y descarta todo lo que no sobreviva tres meses sin que alguien lo cuide (snapshots que se pudren, tests flaky, ceremonia). Right-size siempre al proyecto real, no al proyecto que admiras.

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
- **Comentarios solo con contenido durable no obvio:** invariantes, contratos de ownership/lifetime, deviaciones deliberadas. No narrar lo que el código hace; eso va en el mensaje del commit.
- **Grep el helper antes de escribir uno nuevo.** Ser el único archivo que toca un primitivo crudo es una señal de alerta.
- **La forma más simple y honesta;** deduplicar dentro del propio diff (la segunda vez que aparece un bloque, extraer un helper y usarlo en cada sitio paralelo).

## Sembrar el CLAUDE.md de un proyecto nuevo

El `CLAUDE.md` es el **manual operativo** del proyecto — comandos densos y accionables, no un ensayo. **No improvises su estructura: usa el esqueleto probado en [`reference/plantilla-claude-md.md`](reference/plantilla-claude-md.md)**, que trae las secciones en orden (qué es → build & comandos → arquitectura → invariantes y oráculo → bug-fix workflow → testing → patterns → lessons → gotchas → deploy) + las reglas de densidad y un ejemplo trabajado.

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
- **Un verificador debe demostrar que ejerció el objeto (prueba de trabajo).** Un auditor que puede devolver "sin hallazgos" sin haber leído nada es un lazo cerrado más: cumple el contrato de salida (el schema, el formato) midiendo el vacío — y el output estructurado *enmascara* el fallo aguas arriba, porque el agente rellena el schema obedientemente en vez de gritar. Exige en el output una prueba de lectura/ejecución (el título real del objeto, una línea textual, el conteo de lo procesado) y trata el **cero hallazgos de la primera pasada como sospecha de instrumento roto**, no como éxito. *(ej. real: dos rondas de lectores ciegos devolvieron "SIN_VACIOS" schema-perfecto sobre un capítulo… porque un bug de argumentos les pasó una lista de archivos VACÍA; la ronda con ruta incrustada y campo obligatorio "resumen_leido" encontró un bloqueante y un error matemático real que el autor no había visto.)*
- **Un ritual sin enforcement es teatro.** VERIFY-REAL y la retrospectiva derivan si dependen de que alguien se acuerde. Conviértelos en GATES automáticos (un hook, un deploy que se niega fuera del trunk, un check del harness). Lo hace cumplir el harness, no la buena voluntad.
- **Cierra toda sesión con la pregunta adversarial-contra-la-realidad:** *"¿qué problema real y grave es invisible para mi aparato AHORA?"* — sobre el repo/prod real, no un fixture. **Encontrar un error por suerte (porque un humano lo señaló) NO cuenta como que el sistema funciona.**

## Cómo crece este estándar — la paranoia del compounding

Este estándar no es estático. Tras cada sesión de código sustantiva, correr `retrospectiva-de-sesion`: destila las correcciones del usuario y los descubrimientos, y decide qué es **específico del proyecto** (va a su `CLAUDE.md`) y qué es **universal** (vuelve acá, endureciendo el estándar de toda la empresa).

Pero la retro es el ritual de COSECHA, no el momento en que se aprende. Debajo hay una base más profunda, descubierta a los golpes: **un sistema de conocimiento se escribe como BIBLIOTECA (contenido correcto, completo, bien redactado) pero lo que opera es una MÁQUINA (qué se carga, qué se copia, qué se dispara, qué se sincroniza)**. Todo fallo de proceso repetido es un punto donde la biblioteca asumió que la máquina la ejecutaría sola — y la deriva es sistemática, no mala suerte: escribir es barato y mecanizar es caro, así que el gradiente de mínimo esfuerzo produce doctrina sin disparadores, y si el corpus crece más rápido que su mecánica, la fracción de letra muerta tiende a 1.

De ahí la ley: **nada existe hasta que algo lo dispara.** Toda regla nueva necesita tres cosas, no una: el contenido, su **mecanismo de activación no-textual** (un ancla en algo que siempre se carga, un hook, un gate, un guard que revienta ruidosamente, un campo obligatorio de schema) y **la evidencia de su primer disparo real**. Test de activación: «¿qué hace que esto opere cuando nadie está mirando?» — si la respuesta es «la memoria del próximo agente», no está compoundeado: está *declarado*, y se registra como deuda declarada, no como cobertura. El corte del regreso infinito (¿quién vigila al hook?) no es otra capa: es instrumentos que fallan ruidosamente + el humano como oráculo de última instancia — el diseño correcto lo tiene de ÚLTIMO eslabón, nunca de primero.

La actitud que se sigue de la base es la **paranoia por el compounding**: todo caso es sospechoso de ser una clase, y todo aprendizaje no escrito se está perdiendo AHORA. Cinco reflejos — casos de la misma pregunta generadora — en loop constante durante la sesión, no solo al cierre:

1. Ante un fix → **¿caso o clase?** `grep` de los hermanos que comparten el patrón antes de cerrar (Pilar 2).
2. Ante una corrección del usuario → **¿qué principio hay detrás y dónde vive?** El micro-ciclo se dispara EN EL MOMENTO, como parte del mismo fix: arreglar el caso → destilar el principio (la prueba de fuego de la retro) → escribirlo donde vive (el `CLAUDE.md` del proyecto, esta skill, o la skill afectada) → verificar lo escrito. La retro del cierre verifica y completa lo acumulado — no debe ser la primera vez que el aprendizaje se piensa.
3. Ante un resultado limpio → **¿el instrumento midió algo?** (la prueba de trabajo, arriba).
4. Ante una regla o referencia escrita → **¿alguien la sigue?** Un puntero que nadie sigue, una regla que nada dispara, es letra muerta certificable como completa.
5. Ante un «listo» → **¿qué es invisible para mi aparato AHORA?** (la pregunta adversarial, arriba).

**Señal inequívoca de que la paranoia falló:** el usuario encontró el problema, o tuvo que pedir el aprendizaje («¿qué aprendimos?», «¿cómo compoundeamos esto?»). Cada vez que pase, el hallazgo N.º 1 de la cosecha es por qué el reflejo no disparó. *(Caso real: en la MISMA sesión en que se endureció todo este aparato, una corrección del usuario se arregló como bug puntual y el principio quedó sin escribir hasta que el usuario lo exigió — el aparato existía; el reflejo que lo dispara es lo que faltaba.)*

Y "acá" significa **el repo `kumo-skills`**, no la copia instalada en `~/.claude/skills/`: la mecánica completa de editar una skill (diff previo, merge del drift, gate, resync, push) vive en el `CLAUDE.md` de ese repo, sección «Cuando Claude edite una skill INSTALADA». Este archivo que estás leyendo puede SER una copia instalada — edítalo en el repo y re-distribuye.
