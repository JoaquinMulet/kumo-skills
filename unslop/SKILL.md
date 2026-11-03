---
name: unslop
description: >-
  Quita del texto las marcas que delatan que lo escribió una IA y le devuelve voz, en español de
  Chile y con las reglas de prosa de Joaquín. Corrige relleno, vocabulario inflado, puntuación de
  muleta (raya, dos puntos, punto y coma), listas con etiqueta que se repite, voz pasiva, adverbios
  y metáforas abstractas. Es el último paso de todo texto que alguien más va a leer. Úsala al cerrar
  cualquier documento, skill, README, informe, carta o mensaje largo, y cuando el usuario diga que un
  texto suena a IA, suena robótico, suena a ChatGPT, tiene relleno, o pida unslop o limpiar el estilo.
---

# Unslop. Quitar las marcas de IA y devolver la voz

Es la versión en español de `unslop` de pstack (Lauren Tan, MIT), con la misma numeración de
patrones y las reglas de prosa que Joaquín corrigió en 28 ocasiones hasta el 25 de agosto de 2026.
Va al final, después de cualquier otra edición. Si un modelo vuelve a editar el texto, se corre otra
vez.

## El proceso

1. Corre el barrido mecánico de la raya y el punto y coma. No toca código, frontmatter ni tablas.

   ```
   uv run python -I scripts/unslop_puntuacion.py --listar archivo.md
   ```

2. Busca a mano los patrones de abajo y reescribe conservando el significado.
3. Pregúntate qué hace que el texto todavía se vea escrito por una IA, y arregla eso.

## Las reglas de Joaquín

- Nada de «No es X. Es Y.», ni de una negación como frase de apertura, ni de 3 frases cortas de cierre.
- Nada de cierres épicos de mi cosecha. Una cadena causal simple, con «probablemente» donde corresponda.
  Los golpes de efecto de Joaquín sí se respetan.
- No se anuncia la emoción («la comparación es incómoda»). Se muestra el dato.
- Sin negrita como etiqueta al inicio de un ítem de lista.
- Voz «nosotros» con duda humana («creemos», «nos preguntamos»), y primera persona donde corresponda.
- Referentes del país del lector y sin adjetivos gratuitos («exigente», «impecable», «sofisticado»).
- No se adopta la etiqueta del adversario. Se describe la realidad específica.
- Con lectores expertos, datos e ideas con su origen, nunca instrucciones sobre su propio trabajo.
- La retórica no endurece ni ablanda lo que la fuente respalda.
- Español con «tú», nunca voseo.
- Ni raya ni guion largo. Ni dos puntos ni guion como signos de puntuación en la prosa. Se salvan el
  guion dentro de una palabra, el de rutas y comandos, y los dos puntos del saludo de una carta.

## Los patrones

Contenido.
1. Grandilocuencia («momento decisivo», «sentando las bases»). Di qué pasó.
2. Nombres sueltos de medios o autoridades. Elige uno y di qué dijo.
3. Gerundios de adorno («destacando», «asegurando»). Bórralos o vuélvelos una afirmación con fuente.
4. Lenguaje de folleto («vibrante», «revolucionario»). Descripción neutra.
5. Atribuciones vagas («los expertos creen»). Nombra la fuente o borra la frase.
6. La fórmula del desafío («pese a los desafíos, prospera»). Hechos concretos.

Lenguaje.
7. Vocabulario de IA. «adicionalmente», «crucial», «profundizar en», «potenciar», «fomentar»,
   «entramado», «panorama», «clave» como muletilla, «subrayar», «robusto», «integral», «en aras de»,
   «cabe destacar», «no obstante». Palabra llana.
8. Formas rebuscadas de «es» («funge como», «se erige como», «cuenta con»). Di «es» o «tiene».
9. «No solo X, sino Y». Di el punto directo.
10. Regla de tres forzada. Usa el número real.
11. Rotación de sinónimos. Elige un nombre y repítelo.
12. Rangos falsos («desde X hasta Y» sin escala común). Enumera.

Estilo.
13. Raya. Ni una, y tampoco cambiarla por paréntesis.
14. Dos puntos a mitad de frase. Casi siempre tapan un conector que nadie pensó.
15. Negrita de más.
16. Listas con etiqueta que repite la línea («**Rendimiento.** El rendimiento mejoró»). A prosa.
17. Títulos con mayúscula en cada palabra.
18. Emojis de adorno.
19. Comillas curvas inglesas. Rectas, o las angulares del proyecto.

Restos de conversación.
20. Frases de asistente («¡Espero que te sirva!»).
21. Descargos por falta de datos. Busca la fuente o borra la frase.
22. Adulación («¡Excelente pregunta!»).

Relleno.
23. Frases de relleno («con el fin de» es «para»).
24. Titubeo excesivo. «Puede».
25. Cierres genéricos («el futuro se ve prometedor»). El plan o el dato.

Jerga.
26. Metáforas abstractas con cara técnica (sustrato, vector, andamiaje, paradigma, trinquete). Usa la
    palabra concreta. Si la metáfora es el nombre real de un archivo o comando del repo, se queda y
    se define la primera vez.

Habla llana.
27. Di lo que hace, no lo que se siente. Un mecanismo o un número. Si la frase cabría igual en otro
    proyecto, no dice nada de este.
28. Parte las frases densas. Una idea por frase.
29. Voz activa. Nombra al actor.
30. Corta los adverbios o usa un verbo más fuerte.
31. La palabra llana («utilizar» es «usar», «facilitar» es «ayudar»).

## Lo que esta skill no rompe

- El código, los comandos, las rutas y las cifras quedan intactos.
- Una regla no se vuelve sugerencia. «Tienes que» no pasa a «conviene».
- El porqué de una regla no es relleno, aunque sea largo.
- Antes de pasar unslop por un documento ya auditado, escribe sus centinelas (ver `doc-prueba-de-uso`).
