# Higiene continua del repo. Los principios

Este anexo es la antigua sección «Higiene continua del repo» de `SKILL.md`, movida tal cual el 3 de noviembre de 2026 cuando la skill pasó a ser la portada de Kumo sobre pstack. El anexo operativo, con los 7 pasos de instalación, está en [`higiene-continua.md`](higiene-continua.md).

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

Cuatro formas distintas del mismo engaño, medidas en carne propia.

- **El código de salida de un trabajo dice si la herramienta CORRIÓ, no si encontró algo.**
  Un análisis de seguridad terminó en verde con 30 alertas abiertas, seis de severidad alta.
  Reportarlo como «pasó» fue falso en sustancia. Se lee el **conteo de hallazgos**, no el estado.
- **Un control puede no estar mirando el cambio.** Dos de las cinco comprobaciones verdes
  de cada propuesta apuntaban a la instancia **ya desplegada**, no al código propuesto, así
  que pasaban con cualquier contenido. Antes de contar una capa, verifica **contra qué
  artefacto corre**.
- **Una función puede estar a medio encender.** El archivo de actualizaciones automáticas
  generaba propuestas con las **alertas** de esa función apagadas en el repositorio. Escribir
  el archivo no es habilitar la función. Se comprueba **pidiéndole su resultado por su interfaz**.
- **Un push que termina en 0 no es una CI verde.** El push dice que el commit LLEGÓ, no
  que el remoto lo aprobó. El veredicto se lee en la CI, después. Detalle y caso en el anexo.

Las cuatro se engloban en una regla. **Prueba el efecto, no la presencia.**

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
  suite completa, las comprobaciones de clase y los instrumentos. En un lenguaje sin
  compilador, «compilar» es lo que sea que caiga antes de ejecutar nada, o sea el
  verificador de tipos y el análisis estático.
- **Antes de cada envío**, todo lo anterior más lo que necesita red. Verificación contra
  los servicios reales y el trinquete. Esta etapa corre **exactamente lo que corre la
  integración continua**, sin recortes. Si tu portón local corre **menos** que ella, tu
  verde es de otro color. La paridad se vigila con una **comprobación de clase** que lee la
  CI con su parser real y falla si un comando de ella no está en un hook (ver el anexo).
- **Después de empujar y antes de desplegar**, la conclusión de la CI remota del commit,
  como paso previo del deploy que se niega si está roja. No es un recordatorio (anexo).
- **Después de desplegar**, lo que solo existe desplegado. Protocolo y cliente real contra
  la instancia viva. Una pieza que ES un borde solo se prueba cruzándolo.
- **Programado**, lo que depende del mundo y no del código. Vulnerabilidades publicadas
  después del último commit. Y toda **acción agendada re-deriva sus precondiciones de la fuente autoritativa AL DISPARAR**, con falla cerrada si no puede leerla: el estado que dejó la sesión que la agendó es caché, nunca autoridad — entre agendar y disparar el mundo cambia y el agente puede no existir. *(ej. real: un recordatorio «a quien no haya respondido» dependía de un flag a mano en un JSON; la cura fue releer el buzón real al correr, probada en rojo con el conteo esperado conocido de antemano.)*
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

El anexo operativo vive en [`reference/higiene-continua.md`](higiene-continua.md)
y lleva lo que se consulta mientras ejecutas. **La receta de 5 pasos para escribir una
comprobación de clase**, que es la pieza que de verdad encuentra defectos, **el núcleo del
trinquete y del informe**, porque los 2 se escriben y no se instalan, **la tabla de
equivalencias por lenguaje**, **el procedimiento de 7 pasos para instalar esto en un repo
que no lo tiene**, cómo leer la salida de una herramienta sin que te mienta, cómo acotar
una medición antes de creerle, cuál es la unidad sobre la que se decide, y qué herramientas
de catálogo NO hacen falta todavía. **Ábrelo al entrar a un repo nuevo**, que es cuando los
7 pasos son la tarea.

