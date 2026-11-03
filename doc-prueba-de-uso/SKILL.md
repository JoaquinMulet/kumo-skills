---
name: doc-prueba-de-uso
description: >-
  Valida un documento con la PRUEBA DE USO. Un lector frío (un modelo débil, sin contexto, que lee
  SOLO la sección) tiene que EJECUTAR la tarea que esa sección existe para habilitar (armar la base
  de datos desde el anexo de esquema, rehacer el modelo financiero desde el capítulo financiero), y
  su resultado se califica contra una pauta escrita ANTES. Trae además un script que falla si un
  término se usa antes de la sección que lo explica. Úsala antes de entregar un documento a quien
  debe actuar con él, cuando el usuario diga "no se entiende nada", "con esto no se puede construir",
  "pruébalo con la tarea real", "pásaselo a haiku y que lo haga", "está desordenado", o cuando un
  documento completo y bien escrito igual no le sirve a nadie.
---

# Prueba de uso. Un documento se prueba haciendo la tarea

Un informe de Aero360 pasó 2 revisiones con lectores que debían explicar cada sección, y Joaquín
abrió el anexo de datos y dijo «no se entiende nada». Nombraba 28 tablas sin un solo atributo. La
prueba que sirvió fue la que él propuso: «pásale el anexo a Haiku y pídele que te arme la base de
datos». Resumir exige lo que está. Ejecutar exige lo que falta.

## El procedimiento

1. Por cada sección, completa la frase «después de leer solo esto, el lector debe poder ___». Eso
   define el rol del lector (DBA, CFO, abogado) y su tarea. Una sección sin tarea queda fuera.
2. Escribe la pauta ANTES de lanzar al lector, con los criterios críticos y los importantes. Para
   un esquema, las llaves y las restricciones. Para un método, inventa casos con números que no estén
   en el documento y calcula tú las respuestas.
3. Copia la sección sola a un archivo de la carpeta de borradores. El lector recibe solo ese archivo.
4. Lanza el lector con `Agent`, modelo `haiku`, comandos en primer plano. Su encargo tiene 4 partes.
   - El rol y la tarea, con la ruta exacta del archivo.
   - 2 o 3 preguntas que exigen haber leído (citar una línea, nombrar un elemento). Un lector que
     no leyó inventa, y esto lo delata.
   - El resultado completo, no un resumen.
   - Todo lo que tuvo que adivinar, y dónde lo buscó. Un dato que la sección manda a otra («ver
     §5.3») no es un vacío.
5. Califica el resultado contra la pauta. Busca con `grep` cada vacío que el lector reclama antes
   de creerle. En el caso del anexo, 10 de 12 hallazgos de una ronda eran falsos. Revisa también tu
   propio enunciado del caso, porque una duda puede nacer ahí y no en el documento.
6. Corrige tú, con el parche más chico que desbloquea la tarea. Nunca le pides al lector que arregle
   el documento.
7. Repite con un lector nuevo hasta que pase los criterios críticos y no reporte vacíos reales.
   Suelen bastar 2 o 3 rondas, y a veces 1.

Un modelo débil mide si la información alcanza. Un modelo fuerte mide si el texto admite una sola
lectura, y cuando entiende mal, el defecto es del documento. Usa el fuerte en la última ronda de un
documento que otro va a ejecutar al pie de la letra.

## El orden de los términos, con un script

Un término que se usa antes de explicarse no lo marca ningún lector, porque al final del documento
sí está explicado. Escribe un contrato con cada término y la sección que lo explica, y córrelo.

```
uv run python -I scripts/verificar_orden.py documento.md contrato.json
```

El contrato es un JSON con esta forma.

```json
{"swap": {"patron": "(?i)\\bswap\\b", "seccion": "Qué es un swap"}}
```

Sale con 1 si algún término se adelanta, si una sección del contrato no existe o si un término
desapareció. Lee títulos `#` de Markdown, `<section id>` de HTML y `\section` de LaTeX.

## Que los arreglos sobrevivan

Cada arreglo vive en una redacción, y la próxima reescritura lo borra sin que se note. Antes de
cerrar, convierte cada arreglo en un centinela. Es una frase corta y distintiva dentro de una prueba
que falla si la frase desaparece, como `scripts/centinelas.py` del repo kumo-skills. El contrato de
orden también se queda junto al documento y se vuelve a correr después de cada edición.
