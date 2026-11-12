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

11. Escribe un solo párrafo por mensaje. Al editar, toca un párrafo a la vez y relee el anterior y el siguiente.
12. Antes de mostrarlo, corre el script de comprobación sobre el borrador y sus fuentes.

    ```
    uv run --with pymupdf python scripts/comprobar_parrafo.py BORRADOR.md FUENTE [FUENTE ...]
    ```

    El script busca cada cita de las notas al pie en el texto de las fuentes, y marca los dos puntos como conector, las rayas, las frases que abren negando y las frases de índice. Si falla, se arregla antes de mostrar. Una cifra o un hecho sin cita también se busca en su fuente antes de escribirlo.
13. Muestra el párrafo entero en el chat, en prosa, y después explica en pocas líneas qué cambió y por qué, qué hace el párrafo y cómo enlaza con el siguiente. Termina con una sola pregunta, qué cambiaría el usuario.
14. El usuario corrige la voz, las palabras, el foco o el mensaje. Aplica sus correcciones con sus palabras. Si una idea suya choca con una fuente o la precisa, explica qué dice de verdad la fuente, con su mecanismo concreto, y propone cómo unir las 2 cosas.
15. Cuando el usuario aprueba el párrafo, guárdalo en git y pasa al siguiente.

## Fase E. Cerrar la etapa

16. Marca la versión como aprobada y pon al día el esqueleto, el mapa y la lista de pendientes.
17. Cada corrección del usuario que sirve para las etapas siguientes va a la memoria, y la que sirve para cualquier texto va a esta skill.

## Lo que hace bien un párrafo

- Tiene a lo más 3 ideas. Si tiene más, se separa en 2 párrafos, aunque el plan aprobado tuviera uno. Joaquín lo pidió por legibilidad.
- Abstrae la fuente para hoy. Un autor clásico entra como una historia corta con 1 o 2 citas, y el texto parte y termina en el presente.
- Atribuye a cada autor solo lo que dijo, con sus palabras y su cita. Una pregunta «de Ricardo» va con la frase de Ricardo.
- Explica la idea de un autor con el mecanismo concreto que describe, no con su frase más abstracta.
- Contrasta el supuesto de un clásico con lo que se sabe hoy, antes de usarlo como argumento.
- No repite lo que queda entre líneas ni lo que dijo un párrafo anterior. Un concepto ya explicado se nombra y nada más, sin aposición que lo vuelva a definir («los agentes, sus modelos con sus arneses»).
- Un párrafo de mediciones parte por el objetivo que se mide y por quién lo mide, y recién después da las cifras con su evolución. Tres cifras en fila, sin ese marco, no cuentan una historia. Joaquín lo pidió así para el párrafo de capacidades.
- Termina con la intención o la consecuencia, nunca con un índice de lo que viene.
- No abre con un demostrativo suelto («Esa experiencia», «Esto», «Ese cambio»). La primera frase de un párrafo nombra de qué habla, porque el lector puede haber olvidado el párrafo anterior. Joaquín preguntó «¿cuál experiencia?».
- Una enumeración sigue el orden que anuncia la frase que la presenta, y todos sus elementos tienen la misma forma. Si dice «cada laboratorio ofrece su arnés para sus modelos», cada elemento va laboratorio, arnés y modelos, en ese orden.
- No anuncia cómo va a nombrar algo («de aquí en adelante, los llamamos…»). Lo nombra y sigue.
- Una tesis propia va con «creemos» o «probablemente». Un dato va con su fuente.
- Usa las palabras que eligió el usuario para su mensaje, aunque haya sinónimos.
- Nombra una obra por su título exacto, entre comillas, la primera vez, nunca con una descripción propia.

## Citas y notas

Toda fuente va en una nota al pie numerada, nunca entre paréntesis dentro del texto. Joaquín lo pidió así para un trabajo formal («soy piloto, soy cuadrado»), y la regla vale para todo el documento.

- La llamada va antes del signo de puntuación, como pide la RAE: «inteligentes[^1].».
- Cada nota dice autor, año y página, y si hay cita textual, la frase original después: `Ricardo, 1821, cap. 31, párr. 3. «the substitution of machinery…».`
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
| Un párrafo con varias ideas sin hilo | El cierre mezclaba empleo, fotos con fecha, Ricardo y Acemoglu | Que cada frase salga de la anterior |
