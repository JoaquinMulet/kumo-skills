---
name: unslop
description: >-
  Quita del texto las marcas que delatan que lo escribió una IA, y le devuelve
  voz. Corrige relleno, vocabulario inflado, puntuación de muleta, listas con
  etiqueta que se repite a sí misma, voz pasiva, adverbios que apuntalan verbos
  débiles y metáforas abstractas que tapan la palabra concreta. Es el ÚLTIMO
  paso del pipeline documental y se aplica a todo texto que alguien más va a
  leer. Úsala al cerrar cualquier documento, skill, README, informe, carta o
  mensaje largo, y cuando el usuario diga que un texto suena a IA, suena
  robótico, suena a ChatGPT, tiene relleno, o pida unslop, limpiar el estilo,
  quitar el tono de IA, o equivalentes en cualquier idioma.
---

# Unslop. Quitar las marcas de IA y devolver la voz

Un texto puede estar completo, bien fundado y bien ordenado, y aun así delatar
en la primera línea que lo escribió una máquina. Eso no lo arregla ninguna de
las otras skills de documentos, porque las tres primeras juzgan **qué dice** el
texto y esta juzga **cómo suena**.

## Dónde va en el orden

1. `doc-completitud`. ¿está todo?
2. `doc-cadena-causal`. ¿cada cosa se sostiene sola?
3. `doc-narrativa`. ¿se lee bien?
4. `doc-prueba-de-uso`. ¿se puede actuar con esto?
5. **`unslop`, ¿suena a persona?** ← esta

**Va al final, siempre.** Las cuatro anteriores agregan texto, y todo texto que
un modelo agrega llega con sus marcas puestas. Correr unslop antes de ellas es
limpiar una casa mientras siguen entrando cajas.

Y hay una consecuencia incómoda. **Si después de unslop vuelves a editar el
documento con un modelo, hay que volver a correrlo.** No es una etapa que se
gane una vez.

## El proceso

1. Barre buscando los patrones de abajo.
2. Reescribe conservando el significado y el tono que el texto quería tener.
3. Devuelve la voz, que es la otra mitad del trabajo.
4. Auditoría propia. Pregúntate «¿qué hace que esto se vea escrito por una IA?»
   y arregla lo que quede.

El paso 4 no es decorativo. Los tres primeros son mecánicos y encuentran lo
listado. El cuarto es el único que encuentra lo que la lista todavía no tiene.

## Devolver la voz, que es la mitad del trabajo

Quitar patrones deja un texto estéril, y un texto estéril delata igual.

- **Ten una opinión.** Reacciona a los hechos en vez de listar ventajas y
  desventajas con cara de neutral.
- **Varía el ritmo.** Frases cortas. Y después una que se tome su tiempo y
  respire un poco antes de terminar. Mézclalas.
- **Reconoce lo incómodo.** «Impresionante y también un poco inquietante» dice
  más que «impresionante».
- **Usa la primera persona cuando corresponda.** No es poco profesional.
- **Deja entrar algo de desorden.** Una estructura perfecta se ve fabricada.
- **Sé específico.** No «esto preocupa», sino «hay algo raro en unos agentes
  trabajando solos a las 3 de la mañana».

## Los patrones

### Contenido

1. **Grandilocuencia.** «momento decisivo», «da testimonio de», «panorama en
   evolución», «sentando las bases para», «huella imborrable», «profundamente
   arraigado». Córtala y di qué pasó.
2. **Nombres sueltos.** Enumerar medios o autoridades sin contexto. Elige uno y
   di qué dijo.
3. **Gerundios de adorno.** «destacando…», «asegurando…», «reflejando…»,
   «fomentando…». Bórralos o conviértelos en una afirmación con fuente.
4. **Lenguaje de folleto.** «enclavado», «vibrante», «impresionante»,
   «revolucionario», «de renombre», «imperdible». Descripción neutra.
5. **Atribuciones vagas.** «Los expertos creen», «Algunos críticos sostienen».
   Nombra la fuente o borra la frase.
6. **La fórmula del desafío.** «Pese a los desafíos, sigue prosperando».
   Reemplázala por hechos concretos.

### Lenguaje

7. **Vocabulario de IA.** En inglés: additionally, crucial, delve, enhance,
   fostering, garner, interplay, intricate, landscape, pivotal, showcase,
   tapestry, testament, underscore, vibrant. En español: «adicionalmente»,
   «crucial», «profundizar en», «potenciar», «fomentar», «entramado»,
   «intrincado», «panorama», «clave» como muletilla, «subrayar», «robusto»,
   «integral», «en aras de», «cabe destacar», «no obstante». Palabra llana.
8. **Formas rebuscadas de decir «es».** «funge como», «se erige como»,
   «ostenta», «cuenta con», «se posiciona como». Di «es» o «tiene».
9. **«No solo X, sino Y».** Di el punto directo.
10. **Regla de tres.** Forzar todo a grupos de tres. Usa el número real.
11. **Rotación de sinónimos.** Protagonista, personaje principal, figura
    central y héroe en el mismo párrafo. Elige uno y repítelo.
12. **Rangos falsos.** «desde X hasta Y» cuando X e Y no están en ninguna escala
    común. Enumera y ya.

### Estilo

13. **Guion largo.** Ni uno. Y cuidado con el atajo, cambiarlo por paréntesis es
    canjear una marca por otra. Si una idea necesita separarse, termina la frase
    o usa una coma.
14. **Dos puntos.** Sirven antes de una lista o un ejemplo. No como conector a
    mitad de frase. Casi siempre tapan un conector que nadie pensó.
15. **Negrita de más.** No pongas en negrita cada nombre propio ni cada sigla.
16. **Listas con etiqueta que se repite.** La marca es una etiqueta en negrita
    seguida de dos puntos que dice lo mismo que la línea. «**Rendimiento.** El
    rendimiento mejoró…». Eso va en prosa. Una entrada en negrita que termina en
    punto, nombra la cosa y sigue con información nueva no es marca.
17. **Títulos con mayúscula en cada palabra.** Va mayúscula solo al inicio.
18. **Emojis de adorno** en títulos y viñetas. Fuera.
19. **Comillas curvas.** Rectas, o las angulares que use el proyecto.

### Restos de conversación

20. **Frases de asistente.** «¡Espero que te sirva!», «Avísame si…»,
    «¡Por supuesto!», «¡Encontré el problema!». Fuera.
21. **Descargos por falta de datos.** «Aunque los detalles son limitados…».
    Busca la fuente o borra la frase.
22. **Adulación.** «¡Excelente pregunta!», «¡Tienes toda la razón!». Responde y
    ya.

### Relleno

23. **Frases de relleno.** «con el fin de» se vuelve «para». «debido al hecho de
    que» se vuelve «porque». «es importante notar que» se borra entero.
24. **Titubeo excesivo.** «podría potencialmente llegar a considerarse que tal
    vez» se vuelve «puede».
25. **Cierres genéricos.** «El futuro se ve prometedor». Di el plan o el dato.

### Jerga

26. **Metáforas abstractas con cara de técnicas.** Sustrato, cuña, vector, eje,
    nexo, primitiva, arnés, superficie, cimiento, andamiaje, modalidad,
    paradigma, sobreingeniería, trinquete, evacuar (por mover código), fase
    final, norte, volante de inercia. Casi siempre hay una palabra concreta
    debajo. «Sustrato» es «base». «Vector» es «forma» o «vía». «Andamiaje» es
    «armazón» o el nombre real de la pieza.
    **Excepción que hay que respetar.** Si la metáfora se volvió el NOMBRE PROPIO
    de una cosa que existe en el repo, con su archivo y su comando, ya no es
    metáfora, es un nombre, y renombrarla rompe la referencia. La prueba es
    simple. ¿hay un archivo, un script o un comando que se llame así? Si lo hay,
    se queda, y lo que corresponde es definirlo la primera vez que aparece.

### Habla llana

27. **Di lo que hace, no lo que se siente.** «la base de datos queda a mano»,
    «SQL que se puede leer» nombran una sensación. El arreglo nombra el
    mecanismo o un número. «`.toSQL()` devuelve el texto exacto que se manda a
    la base», «renombrar una columna rompe la compilación». Pregúntate qué le
    dice esa frase al lector que haga o que sepa, y escribe eso. Si no puedes
    convertirla en una instrucción, un hecho o un número, córtala. Y una prueba
    más. si la frase podría aparecer igual en la documentación de otro proyecto,
    no dice nada del tuyo.
28. **Corta o parte las frases densas.** Si el lector tiene que volver atrás
    para entender una frase, pártela en dos. Una idea por frase.
29. **Voz activa.** Caza «se hace», «es procesado por», «fue revisado» y nombra
    al actor. «las consultas se validan» se vuelve «el compilador valida las
    consultas». La pasiva sirve solo cuando el actor no se sabe o de verdad da
    igual.
30. **Corta los adverbios, o usa un verbo más fuerte.** «corre rápidamente» se
    vuelve «es rápido» o el número. «mejora significativamente» se vuelve la
    diferencia medida. Un adverbio que apuntala un verbo débil significa que el
    verbo está mal elegido.
31. **La palabra llana.** «utilizar» es «usar», «implementar» a veces es
    «hacer», «facilitar» es «ayudar», «numerosos» es «muchos», «en el caso de
    que» es «si». El sinónimo elegante casi nunca es más claro.

## Lo que esta skill NO debe romper

Un barrido de estilo es la forma más fácil de destruir contenido sin que nadie
lo note, porque el resultado siempre se lee mejor. Tres límites duros.

- **No toques el código, los comandos, las rutas ni las cifras.** Ni sus
  comillas, ni sus mayúsculas, ni sus guiones.
- **No conviertas una regla en una sugerencia.** Cambiar «tienes que» por
  «conviene» es una edición de estilo con consecuencias de gobernanza.
- **No borres el porqué.** La regla 23 manda cortar relleno, y una explicación de
  por qué existe algo no es relleno, aunque sea larga.

Y la protección que hace que esto no dependa de la disciplina. **antes de correr
unslop sobre un documento auditado, escribe sus centinelas**, o sea una frase
corta y distintiva por cada idea que costó una auditoría, dentro de una prueba
que falle si desaparece. La doctrina completa está en
[`doc-narrativa`](../doc-narrativa/SKILL.md), sección «Antes de reescribir».

## Cómo se aplica a muchos documentos

Un barrido sobre un repositorio entero es una detección en paralelo y una
edición en serie.

1. **Un agente por documento, y solo DETECTA.** Devuelve una lista de
   `{archivo, línea, patrón, texto viejo, texto nuevo propuesto}`. No edita.
2. **Verifica antes de aplicar.** Busca cada «texto viejo» en el archivo. El
   que no aparezca literal es una alucinación y se descarta.
3. **Aplicas tú, documento por documento**, porque tienes el contexto que el
   detector no tiene, y porque el paso 2 solo sirve si alguien lo hace.
4. **Corre los centinelas después de cada archivo**, no al final de todos. Si
   algo se perdió, quieres saber cuál archivo lo perdió.

## Su punto ciego

Esta skill mide el TEXTO. Un documento puede quedar impecable de voz y seguir
sin responder la pregunta que le hicieron. Eso lo miden las cuatro anteriores, y
por eso unslop va al final y nunca en lugar de ellas.
