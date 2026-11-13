---
name: redaccion-narrativa-conjunta
description: "Guía la redacción conjunta de un texto narrativo largo (capítulo, introducción, ensayo o informe para divulgar) entre el usuario y Claude, párrafo por párrafo. El usuario pone la visión, el mensaje y la voz, y Claude pone las fuentes comprobadas, la estructura y las reglas de escritura. Cubre el mapa de ideas, la lectura conversada de las fuentes, el mensaje central con el plan de párrafos, la comprobación de cada cita con un script y el cierre de cada etapa. Usar cuando el usuario pide redactar juntos un capítulo, una introducción o una sección, escribir párrafo por párrafo, darle hilo conductor o columna vertebral a un texto, convertir un esqueleto narrativo en prosa, o dice «redactemos la etapa», «ayúdame a redactar», «sigamos con el párrafo siguiente»."
---

# Redacción narrativa conjunta

Esta skill resume cómo Joaquín y Claude escribieron la apertura del capítulo «Sobre los agentes» para la ACTI, el 11 de noviembre de 2026. El primer borrador resumía la fuente, el segundo partía del último dato conversado y el tercero no tenía hilo. La versión final salió de un flujo de ida y vuelta, párrafo por párrafo, y Joaquín la llamó «perfecta». Cada regla de abajo nació de una de esas correcciones.

La clave es el reparto de roles. El usuario pone la visión, el mensaje, la voz y el criterio. Claude pone las fuentes comprobadas, la estructura, la coherencia y las reglas de escritura. Cada vez que uno hizo el trabajo del otro, el texto empeoró.

Que Claude redacte solo no significa que redacte de una vez. Aunque el usuario delegue la lectura de las fuentes, las fases C y D se hacen igual, con su aprobación en cada paso.

## Antes de empezar

- Carga la skill de escritura del proyecto si existe (por ejemplo `writing`) y aplica sus reglas. La más importante es que nada se nombra antes de presentarse.
- Lee las reglas de prosa del usuario (su `CLAUDE.md` y su memoria). Para Joaquín, sin raya, sin dos puntos como conector, sin el patrón que niega primero y afirma después, y prosa narrativa formal en los entregables.
- Pregunta para quién es el texto. Si se divulga ampliamente, no lleva escenas internas, como una reunión de la organización que lo encarga.

## Fase A. Preparar el material

1. Todas las ideas del texto viven en un mapa de ideas, cada una con su código, su origen y su fuente. Las ideas del usuario llevan su frase original.
2. Un esqueleto narrativo dice, por etapa, qué cuenta, qué ideas lleva y qué fuentes leer. Un programa comprueba que toda idea marcada para incluir tenga su lugar.

## Fase B. Leer y conversar

3. El usuario lee las fuentes clave. Si una fuente es de dominio público y está en otro idioma, Claude la pega traducida en el chat, párrafo por párrafo, con espacio para sus opiniones. Si está protegida, Claude da en el primer mensaje los enlaces de un traductor de documentos y un resumen de sus ideas.
4. El usuario comenta. Claude responde con observaciones que salen de la fuente, como un matiz, una frase que no se había usado o un contraste con lo que se sabe hoy, y comprueba cada una antes de decirla.
5. Las ideas nuevas que nacen de la conversación se anotan en el mapa y se mandan a la etapa donde corresponden. No todas entran a la etapa que se está escribiendo.

## Fase C. La columna vertebral

6. Antes de escribir, relee el esqueleto entero, el encargo y las ideas del usuario. El punto de partida es el problema del lector, nunca el último dato que se conversó.
7. Propón el mensaje central en pocas frases. Son las preguntas que la etapa responde y la tesis que las une.
8. Propón el plan de párrafos. Cada párrafo lleva la pregunta que responde y una frase que dice por qué viene después del anterior. Si un párrafo no tiene esa frase, está mal ubicado.
9. Revisa el plan con la skill de escritura. Ningún párrafo usa un concepto que se presenta después, y ninguno promete que algo «se explicará más adelante».
10. El usuario aprueba, corrige o reencuadra. Si cambia el mensaje central, se rehace el plan antes de escribir una línea. Un cambio de estructura se explica antes de hacerlo.

## Fase D. Párrafo por párrafo

11. Escribe un solo párrafo por mensaje. **Siempre, antes de escribir o corregir cualquier párrafo, por chico que sea el cambio, lee la etapa entera con Read, desde su primer párrafo hasta el último.** Leer solo el párrafo anterior y el siguiente no basta. Joaquín lo dijo el 12 de noviembre de 2026, después de 3 repeticiones seguidas de cosas ya explicadas, una frase que cerraba en mitad de la etapa y un estudio presentado como «de los primeros»: «tu problema está en no estar leyendo toda la etapa… y los intentas parchear con herramientas que construyes para tapar el error que nació ahora, pero no el que cometerás después». Y agregó: «no lo hagas solo ahora, hazlo siempre». Un error de lectura no se tapa con un script nuevo. Se corrige leyendo.
12. Antes de mostrarlo, corre el script de comprobación sobre el borrador y sus fuentes.

    ```
    uv run --with pymupdf python scripts/comprobar_parrafo.py BORRADOR.md FUENTE [FUENTE ...]
    ```

    El script busca cada cita de las notas al pie en el texto de las fuentes, y marca los dos puntos como conector, las rayas, las frases que abren negando y las frases de índice. Si falla, se arregla antes de mostrar. Una cifra o un hecho sin cita también se busca en su fuente antes de escribirlo.
13. Un defecto que uno mismo nota se corrige antes de mostrar el párrafo. Nunca se muestra con un aviso de «lo corrijo en la próxima pasada». El 12 de noviembre de 2026 mostré una frase con «además» repetido avisando que lo arreglaría después, y Joaquín tuvo que pedirlo igual. Muestra el párrafo entero en el chat, en prosa, y después explica en pocas líneas qué cambió y por qué, qué hace el párrafo y cómo enlaza con el siguiente. Termina con una sola pregunta, qué cambiaría el usuario.
14. El usuario corrige la voz, las palabras, el foco o el mensaje. Aplica sus correcciones con sus palabras. Si una idea suya choca con una fuente o la precisa, explica qué dice de verdad la fuente, con su mecanismo concreto, y propone cómo unir las 2 cosas.
15. Cuando el usuario aprueba el párrafo, guárdalo en git y pasa al siguiente.
    El título de una obra y el nombre de quien la publicó van en la nota y en la bibliografía, no en la prosa. La prosa nombra a una persona o a una institución solo cuando eso aporta al relato, y el título solo cuando el título mismo dice algo, como «Still Waters, Rapid Currents». El 12 de noviembre de 2026 el párrafo 1 abría con «Según recuerda *Buenas Prácticas…*, el libro de la Mesa de IA de la ACTI», y Joaquín pidió sacarlo: «eso va en las referencias, no aquí».
    Un producto se nombra por lo que es, no por la etiqueta que le puso su empresa. El 12 de noviembre de 2026 el párrafo 2 decía que ChatGPT era «un modelo que conversaba con las personas», como lo presentó OpenAI, y Joaquín corrigió que es una aplicación que permite a las personas chatear con los modelos. Antes de escribir qué es algo, se separa el modelo de la aplicación o del arnés que lo rodea. Y la palabra del usuario se conserva. En esa misma corrección quité «aplicación» porque la frase ya abría con «La primera aplicación masiva», y Joaquín tuvo que escribir «te falta aplicación que permitía». Si su palabra choca con otra de la frase, cambia la mía.
    Un fenómeno que el lector no conoce se nombra junto con lo que es y con por qué importa, en la misma frase o en la siguiente. El 12 de noviembre de 2026 el párrafo de la fragilidad de METR decía «las trampas de los modelos también mueven la cifra», y Joaquín preguntó qué trampas y por qué mueven la cifra. La versión aprobada dice qué cuenta METR como trampa, en qué modelo la vio y cómo cambia el horizonte según se cuente.
    Una pregunta abierta va en su propia frase, corta y dicha como pregunta del lector. 2 preguntas nunca se cuelgan de un mismo «sigue abierto» con «y además». El 12 de noviembre de 2026 Joaquín encontró «Si los laboratorios lograrán reducir esas fallas, y en cuánto tiempo, sigue abierto, y para las personas, las empresas y los gobiernos importa además cuánto de ese avance llega ya a su trabajo», que llevaba todo el día en el borrador: «está pésima, no se entiende, está muy larga, no son claras las preguntas». Un defecto que sobrevive varias aprobaciones sigue siendo un defecto. Al releer la etapa entera, las frases de cierre de cada párrafo se miran con la misma vara que las nuevas.
    Antes de mostrar un párrafo con una fuente nueva, cada afirmación se pone al lado de la frase oficial que la respalda, y las cautelas de la fuente pasan al texto («appeared to roughly correspond» no es «equivalía», «has advanced» no es «avanza»). Lo que la fuente dice en general no se le atribuye a un caso que ella no nombra. El 12 de noviembre de 2026 Joaquín pidió validar el párrafo del ECI contra Epoch, y aparecieron 3 diferencias: una saturación atribuida a GDPval y METR sin fuente, un «equivalía» donde Epoch dice «parecía corresponder» y un presente donde Epoch dice «ha avanzado».
    Lo que el usuario todavía no aprueba vive en una lista, `por_aprobar.md` junto al borrador, y el documento que él lee lo muestra en amarillo. Una línea marca un párrafo entero por su comienzo o una frase exacta. Cada texto nuevo o cambiado entra a la lista, y sale cuando él lo aprueba. El 12 de noviembre de 2026 Joaquín pidió «resáltame en amarillo las cosas que debo aprobar y no he aprobado formalmente», porque los cambios y las aprobaciones se habían mezclado en la conversación.
    Si el cambio agregó contenido nuevo al párrafo, antes de mostrarlo se relee el párrafo siguiente buscando lo que ahora repite, y se propone su ajuste en el mismo mensaje. El 12 de noviembre de 2026 el párrafo 3 pasó a contar las herramientas de Claude Code, y el 4 seguía definiendo al agente por «usar herramientas y ejecutar acciones». Joaquín lo notó después de aprobar el 3.
16. Si un párrafo crece en varios, cambia de lugar o se suma uno que el plan no tenía, se detiene la escritura y se rehace el plan del bloque, con sus mensajes de fondo y la pregunta de cada párrafo, antes del párrafo siguiente. El 12 de noviembre de 2026 la parte de mediciones pasó de 1 párrafo a 8 sin rehacer el plan, y los párrafos siguientes repitieron definiciones, cerraron a mitad de etapa y afirmaron que un estudio de 2026 era de los primeros. Joaquín: «perdimos totalmente el hilo narrativo».

## Fase E. Cerrar la etapa

16. Marca la versión como aprobada y pon al día el esqueleto, el mapa y la lista de pendientes.
17. Cada corrección del usuario que sirve para las etapas siguientes va a la memoria, y la que sirve para cualquier texto va a esta skill.

## Lo que hace bien un párrafo

- Tiene a lo más 3 ideas. Si tiene más, se separa en 2 párrafos, aunque el plan aprobado tuviera uno. Joaquín lo pidió por legibilidad.
- Abstrae la fuente para hoy. Un autor clásico entra como una historia corta con 1 o 2 citas, y el texto parte y termina en el presente.
- Atribuye a cada autor solo lo que dijo, con sus palabras y su cita. Una pregunta «de Ricardo» va con la frase de Ricardo.
- Explica la idea de un autor con el mecanismo concreto que describe, no con su frase más abstracta.
- La lectura tiene que ser predecible. La primera frase de un párrafo le dice al lector qué viene, la pregunta o el tema, sin adelantar la conclusión y sin lanzarlo de golpe a un dato. Joaquín, el 12 de noviembre de 2026, primero sobre una apertura con la conclusión («no partas con la conclusión») y después sobre una que partía directo con la fecha del estudio («eso no es placentero de leer, la lectura debe ser predecible»). Bien: «Otra forma de anticipar el impacto es preguntarle a la gente qué espera de la inteligencia artificial, y comparar a quienes trabajan más cerca de los agentes con el resto».
- Un autor se cita por lo que aporta al argumento del texto, no por la parte de su obra que mira otro tema. Y la opinión de un modelo de IA que un autor cita no es evidencia. Joaquín, el 12 de noviembre de 2026, sobre Howard Marks: lo que vale es que se hace «las preguntas correctas», y su escala de previsibilidad pedida a Claude y su mirada de inversionista «no es lo relevante aquí».
- Un estudio se cuenta con sus detalles, nunca como titular. Antes de escribir su cifra, se lee entero, incluidas sus figuras, y se responden las preguntas que importan. Qué preguntó exactamente y a quién. Qué mide y qué no mide, por ejemplo capacidad o uso. En qué coinciden los grupos y dónde se separan. Qué matiza la cifra principal. El 12 de noviembre de 2026 escribí «el 75 % contra el 28 %» y «7 de 8 tareas» sin saber cuáles eran las tareas, que solo estaban en la figura 1. Joaquín: «el diablo está en los detalles, no hables como títulos de periodismo… haz las preguntas que importan».
- Un ejemplo que respalda una tesis sale de la evidencia más seria que hay a mano, un paper, un informe técnico del laboratorio o un estudio con método, y cuenta qué se hizo y qué pasó. Una anécdota suelta o un detalle pintoresco (el editor de video de un programador, una regla que bloquea un borrado) no basta. Joaquín, el 12 de noviembre de 2026: «no me gustan tus ejemplos… son banales, simplistas, coloquiales. Seamos serios, tenemos papers e información de primera».
- Contrasta el supuesto de un clásico con lo que se sabe hoy, antes de usarlo como argumento.
- No repite lo que queda entre líneas ni lo que dijo un párrafo anterior. Un concepto ya explicado se nombra y nada más, sin aposición que lo vuelva a definir («los agentes, sus modelos con sus arneses»).
- Un párrafo de mediciones parte por el objetivo que se mide y por quién lo mide, y recién después da las cifras con su evolución. Tres cifras en fila, sin ese marco, no cuentan una historia. Joaquín lo pidió así para el párrafo de capacidades.
- Prohibido el contraste retórico, en cualquier lugar de la frase. Es negar una idea para afirmar otra, como «no es X, es Y», «X, y no Y», «distinto de», «no da lo mismo», «un horizonte que se duplica no duplica la automatización» o «es la parte que no es inteligencia artificial. Es software tradicional». Joaquín lo pidió así el 12 de noviembre de 2026, cansado de verlo («basta de usar esa forma retórica»). Se dice solo lo que es, con su mecanismo («la automatización crece menos que el horizonte», «es software tradicional»). La negación de un hecho medido sí vale («ninguno usa un marco general»). El script lista las candidatas con la marca «CONTRASTE?».
- Prohibidas las frases sin contenido. Cada frase cuenta un hecho, un dato o una idea que no estaba antes. Lo que no informa es relleno y se borra, porque el texto busca ser acotado, con buen flujo y la mayor información posible por frase. La forma más común del relleno es la frase catafórica o bisagra. Es corta, tiene por sujeto una abstracción que el texto acaba de nombrar («esas dos direcciones», «las dos mediciones») y solo anuncia o resume lo que cuentan las frases vecinas («Cada una de esas dos direcciones tiene hoy quien la mida», «Las dos mediciones muestran un avance rápido»). Suena a sentencia y corta la historia, porque nadie hace nada en ella. Las otras formas son el resumen de lo recién dicho, la frase de índice y el anuncio de lo que viene. Si el párrafo necesita pasar de un tema a otro, el paso lo hace una frase que ya trae un hecho, con alguien que actúa, cuándo y para qué («Mientras tanto, METR se propuso medir cuánto tiempo puede trabajar solo un agente»). La prueba es borrar la frase. Si no se pierde ningún hecho, se elimina. El script de la fase D lista las candidatas con la marca «BORRAR?», y cada una pasa la prueba antes de mostrar el párrafo.
- No encadena «y». Una frase con una enumeración unida por «y» más otras cláusulas unidas por «y» se lee pesada. Se parte en frases cortas y la enumeración usa comas, con una sola conjunción al final. Joaquín, el 12 de noviembre de 2026, sobre «puede buscar y leer el código…, escribir y correr pruebas y usar las herramientas…, y con ella se abrió…»: «esto está pésimo, lleno de y».
- Termina con la intención o la consecuencia, nunca con un índice de lo que viene.
- Un párrafo de cierre deja la idea final y baja a tierra lo que significa para el lector. Los detalles técnicos que matizan (un límite de la prueba, una fecha de actualización) van en los párrafos anteriores o salen. Joaquín lo pidió así para el cierre de las advertencias de METR, «debe dejar la idea final, no seguir entrampándose con detalles».
- No abre con un demostrativo suelto («Esa experiencia», «Esto», «Ese cambio»). La primera frase de un párrafo nombra de qué habla, porque el lector puede haber olvidado el párrafo anterior. Joaquín preguntó «¿cuál experiencia?».
- Una enumeración sigue el orden que anuncia la frase que la presenta, y todos sus elementos tienen la misma forma. Si dice «cada laboratorio ofrece su arnés para sus modelos», cada elemento va laboratorio, arnés y modelos, en ese orden.
- No anuncia cómo va a nombrar algo («de aquí en adelante, los llamamos…»). Lo nombra y sigue.
- Una tesis propia va con «creemos» o «probablemente». Un dato va con su fuente. Pero el capítulo no da opiniones donde la evidencia muestra lo que hacen los actores. Ahí se dice el hecho («por eso la industria ha puesto sus fichas también en el arnés y en el entorno»), y el «creemos» queda para las pocas tesis de los autores que no tienen otra fuente. Joaquín: «aquí no estamos dando opiniones».
- Usa las palabras que eligió el usuario para su mensaje, aunque haya sinónimos.
- Nombra una obra por su título exacto, entre comillas, la primera vez, nunca con una descripción propia.

## Citas y notas

Toda fuente va en una nota al pie numerada, nunca entre paréntesis dentro del texto. Joaquín lo pidió así para un trabajo formal («soy piloto, soy cuadrado»), y la regla vale para todo el documento.

- La llamada va antes del signo de puntuación, como pide la RAE: «inteligentes[^1].».
- Las notas siguen el estilo Chicago de notas y bibliografía, en su forma corta, porque el texto lleva bibliografía completa al final. Cada nota dice autor, título corto y página: `Barbaste y otros, «Harness Engineering», 6.` Los títulos de libros e informes van en cursiva y los de artículos y páginas web entre comillas angulares. Joaquín eligió Chicago el 12 de noviembre de 2026, al preguntar cuál era el formato más formal.
- La frase original va en la nota solo cuando el texto traduce una cita textual: `Ricardo, *On the Principles…*, cap. 31, párr. 3. «the substitution of machinery…».`
- Las frases que respaldan cada dato viven en un archivo de comprobación aparte, con el mismo número de nota, que no se publica. En la ACTI está en `6_informe/fuentes/sobre_los_agentes_comprobacion_<etapa>.md`. El script de la fase D se corre sobre ese archivo para comprobar las citas, y sobre el borrador para las reglas de la prosa.
- Al final del texto va la sección «Bibliografía», en estilo Chicago, ordenada por autor.
- La numeración sigue el orden de aparición en todo el texto, sin saltos.
- El script de la fase D marca las citas entre paréntesis que queden en la prosa.

## Errores que ya ocurrieron

| Error | Cómo se vio | Arreglo |
|---|---|---|
| Resumir la fuente en su propio orden | El primer borrador recorría a Ricardo párrafo por párrafo, con 5 citas | Escribir la tesis propia en 1 frase antes de planificar |
| Partir del último dato conversado | El segundo borrador abría con una cifra de Anthropic que se acababa de revisar | Releer el esqueleto entero y partir del problema del lector |
| Frases funcionales o de índice | «Para mirar lo que ocurre con los agentes», «este capítulo se ocupa de ellas en el orden en que se presentan» | Escribir la idea, no el camino hacia ella |
| Paráfrasis atribuida a un autor | «La pregunta de Ricardo, quién gana» | Citar su frase real, con su párrafo |
| La frase más abstracta de un autor | «Nada en el avance de la técnica obligaba…», que el usuario no entendió | Citar el mecanismo, como las tareas nuevas, el voto y los sindicatos |
| Afirmar sin fuente | «La mayoría de las empresas» | Cambiar a lo que se puede respaldar, o buscar la fuente |
| Escena interna en un texto público | El texto abría con «en la mesa de la ACTI» | Un escenario general que incluya a todos los lectores |
| Un clásico como prueba de hoy | Ricardo «ya anticipó» que la IA se abarata, sin los fosos defensivos | Presentarlo como su supuesto y contrastarlo |
| Una subordinada metida entre el verbo y su complemento | «define la inteligencia artificial general que busca como «…»», que se lee «busca como» | Separar en 2 verbos con su complemento al lado, «dice que busca desarrollar una inteligencia artificial general, y la define como «…»» |
| «Los distintos X» sin dueño | «medir esas dos capacidades en los distintos agentes» se leyó como si los agentes fueran los laboratorios | Decir de quién son, «de sus agentes» |
| Narrar el propósito de un autor con palabras propias | «METR se propuso medir cuánto tiempo puede trabajar solo un agente», y el autor de METR escribió que el horizonte no es eso | Al narrar qué buscó o qué mide un autor, copiar el sentido de su definición, y leer sus advertencias antes de escribir la cifra |
| Una medida técnica definida en una sola frase | «definió el horizonte de tiempo como el tiempo que una persona experta tarda en las tareas que el modelo completa la mitad de las veces», que Joaquín no entendió | Contar el procedimiento en pasos (qué se midió primero, qué después) y cerrar con un ejemplo con números («si un agente resuelve la mitad de las tareas de una hora, su horizonte es de una hora») |
| Traducir al pie de la letra una expresión técnica | «a factor of ~2 in each direction» quedó «el doble hacia arriba y hacia abajo», y Joaquín preguntó qué significaba | Decir qué significa con un caso con números («entre la mitad y el doble, un horizonte de 4 horas puede ser de 2 o de 8») |
| Contrastar el todo con una de sus partes | «Las fallas de los agentes nacen de los modelos… El arnés, en cambio, es determinista», como si el arnés no fuera parte del agente | Al contrastar, nombrar las 2 partes del mismo todo («el modelo… el arnés que lo rodea») y decir qué hace cada una por el todo |
| Calcar un término genérico de la fuente | «production systems» quedó «los sistemas en uso», que no nombra a nadie | Nombrar a quién o qué se refiere la fuente («las empresas que construyen agentes») |
| Un párrafo que no retoma al anterior | El párrafo 10 terminaba en las fallas de los agentes y el 11 abría con «El modelo de lenguaje…», y Joaquín lo sintió desanclado | La primera frase toma el último concepto del párrafo anterior por su nombre y su autor («Las fallas que describe Kwa tienen su origen en…») |
| Cerrar en mitad de la etapa | El párrafo 13 terminaba con las preguntas abiertas como cierre, y la etapa seguía con 2 bloques más | Antes de escribir un párrafo, ubicarlo en el hilo de la etapa. Si no es el último, pasa a la pregunta del bloque siguiente en vez de cerrar |
| Frase catafórica sin contenido | «Cada una de esas dos direcciones tiene hoy quien la mida», que Joaquín llamó relleno | Borrarla, o cambiarla por una frase que narre un hecho con alguien que actúa |
| Un párrafo con varias ideas sin hilo | El cierre mezclaba empleo, fotos con fecha, Ricardo y Acemoglu | Que cada frase salga de la anterior |
