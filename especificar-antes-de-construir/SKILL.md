---
name: especificar-antes-de-construir
description: "Lleva el procedimiento de Kumo que se responde antes de especificar y construir algo que no es trivial. Son 8 fases y 23 preguntas, ordenadas con las 4 reglas de Descartes y con la inversión del problema. Producen una ficha que Joaquín aprueba como contrato del cambio, y de esa ficha parte el flujo de verificación formal. Usar antes de diseñar o construir una funcionalidad, un servicio, una máquina de estados, una integración o cualquier cambio que toca datos, dinero, seguridad, disponibilidad o mensajes hacia afuera. También cuando el usuario dice especificación, requisitos, diseño, qué vamos a construir, antes de programar, lista de chequeo, o pide pensar un problema con Descartes o invirtiéndolo. No aplica a cambios de apariencia o de texto."
---

# Especificar antes de construir

Las demostraciones ya no son lo caro. Lo caro es decidir qué se demuestra. El artículo de Google DeepMind sobre
AlphaProof Code, del 10 de noviembre de 2026, lo dice así: la mayor parte del trabajo humano está ahora en la
especificación. Esta skill es el procedimiento de Kumo para hacer ese trabajo de la misma forma cada vez, como una lista
de chequeo de cabina.

El resultado es una ficha por cambio. Joaquín la aprueba, y desde ese momento es el contrato. El modelo, el código y las
pruebas se escriben desde la ficha, nunca al revés.

## Fase 0. ¿Aplica esta lista?

| Condición | Respuesta |
|---|---|
| El cambio toca datos, dinero, seguridad, disponibilidad, estados de un sistema o mensajes hacia afuera | APLICA. Se corre la lista completa |
| El cambio es solo de apariencia o de texto | NO APLICA. Se anota en 1 línea por qué, en el mensaje de cierre |
| Hay duda | APLICA |

## Cómo se corre

1. El agente arma un borrador de la ficha con `reference/ficha.md`. Responde cada pregunta con evidencia propia: lee el
   código, mide, abre la fuente. No responde de memoria.
2. Cada respuesta lleva 1 de 3 marcas. HECHO, con su fuente. SUPUESTO, con quién lo garantiza. DECISIÓN, cuando le toca a
   Joaquín.
3. Las decisiones se le plantean a Joaquín de a 1 por mensaje, con lo encontrado y una recomendación.
4. La ficha aprobada se guarda en el repo del proyecto, en `docs/fichas/AAAA-MM-DD-tema.md`. Su commit es la línea base
   del contrato.

## La lista

### Fase 1. Evidencia

Regla 1 de Descartes: no aceptar nada como verdadero sin saber con evidencia que lo es. Evita la prisa y el prejuicio.

1. ¿Qué problema se resuelve, y con qué evidencia medida? Una respuesta aceptable trae un número, un registro o un caso
   real con fecha. «Se cree que» no basta.
2. ¿Qué es hecho y qué es supuesto? Cada hecho lleva su fuente: archivo y línea, registro, medición o documento.
3. ¿Quién decide, y quién carga la consecuencia si sale mal? La información es de quien carga la consecuencia.

### Fase 2. Propósito

4. ¿Qué daño evita, dicho en palabras del negocio? Si nadie puede nombrar el daño, el cambio no se justifica todavía.
5. ¿Cómo se sabrá en producción que funcionó? Es una medida concreta que se va a revisar después de instalar.

### Fase 3. Inversión

Invertir el problema da otro punto de vista. La máxima es del matemático Carl Jacobi, «invertir, siempre invertir», y la
hizo conocida Charlie Munger.

6. Si esto fracasó dentro de 1 año, ¿cómo fracasó? Se escriben al menos 3 formas distintas.
7. ¿Qué no debe pasar nunca? Cada respuesta será una regla de seguridad en la fase 6.
8. ¿Qué error ya ocurrió en algo parecido, en Kumo o fuera? Se buscan los pendientes, las skills de verificación del
   repo y la memoria de los proyectos.
9. ¿Qué haría que la verificación salga verde con el sistema roto? Por ejemplo, una regla copiada del código o un
   modelo que le regala al sistema un dato que no tiene.

### Fase 4. El mundo y el sistema

10. ¿Qué actores, estados y eventos existen?
11. ¿Qué observa el sistema, y de qué línea de código sale cada dato? Un dato sin línea de código es un dato del mundo.
    El sistema no lo puede usar.
12. ¿Qué supone el sistema del mundo, y quién garantiza cada supuesto? Por ejemplo, el procedimiento del operador, un
    tercero o una medición.
13. ¿Qué falla del entorno puede ocurrir? Corte de luz, reinicio, falta de internet, disco lleno, reloj corrido y
    tercero caído, entre otras.

### Fase 5. División y orden

Reglas 2 y 3 de Descartes: dividir cada dificultad en tantas partes como haga falta, y avanzar en orden, de lo más
simple a lo más complejo.

14. ¿En qué partes se divide el cambio?
15. ¿En qué orden se construyen, de la más simple a la más compleja?
16. ¿Con qué capa se verifica cada parte? Modelo TLA+ para el diseño, contratos de código para la implementación,
    binario para el núcleo más crítico, y pruebas para el resto.

### Fase 6. Reglas

17. Las reglas de seguridad, o sea lo que nunca pasa.
18. Las reglas de vida, o sea lo que termina pasando.
19. El presupuesto de memoria, disco, procesador y disponibilidad.
20. Para cada regla, 3 respuestas. El daño que evita. Un caso real donde se cumple. El error que detecta.

### Fase 7. Recuento

Regla 4 de Descartes: hacer recuentos tan completos y revisiones tan generales que se esté seguro de no omitir nada.

21. ¿Cada fracaso de la fase 3 tiene una regla que lo impide?
22. ¿Cada dato de la fase 4 tiene su línea de código?
23. ¿Cada supuesto tiene quien lo garantice?

Si una respuesta es no, se vuelve a la fase que corresponde. La ficha no sigue con un no.

### Fase 8. Aprobación

Joaquín lee la ficha y la aprueba en el chat. El agente guarda la ficha en el repo y anota la aprobación con su fecha.
Desde ese momento la ficha es el contrato del cambio.

## Después de aprobar. El flujo formal

1. El modelo TLA+ se escribe desde la ficha, con `create-formal-verification-skill`. Cada dato del modelo lleva su fila
   de origen en el código. Cada regla lleva un testigo, o sea un estado alcanzable donde se cumple. El diseño anterior o
   roto tiene que fallar.
2. Los contratos de código se escriben desde el modelo, nunca desde el código. En Rust la herramienta es Kani, según la
   comparación de verificadores de AeroStratus del 13 de noviembre de 2026.
3. Prueba roja, después el código, después la prueba en verde, con `tdd`.
4. Las mutaciones y los errores antiguos se vuelven a meter, y la verificación tiene que detectar cada uno.
5. Un crítico de otra familia de modelos revisa la ficha, el modelo y los contratos.
6. El portón del repo decide qué está terminado. Ningún agente lo declara.
7. Solo para el núcleo más crítico, una demostración sobre el binario.
8. Se mide el efecto en producción con la medida de la pregunta 5.

## Enmiendas

Un cambio a una ficha aprobada entra solo con 3 condiciones. Trae un contraejemplo comprobado o un argumento basado en el
código. No debilita ninguna regla para que calce con el código. Si la única salida es debilitar una regla, se le presenta a
Joaquín como posible error del código. Joaquín lo aprueba. Cada enmienda queda anotada en la ficha con su fecha y su razón.

## Errores que esta lista nace para evitar

| Fecha | Qué pasó | Pregunta que lo habría atrapado |
|---|---|---|
| 11 nov 2026 | El modelo de la subida dejaba que el agente leyera si la cámara había terminado, un dato que el router no ve. El aviso de término salía falso | 11 |
| 13 nov 2026 | La regla que se demostró con Kani se copió del código. Demostraba que el código cumple consigo mismo | 9 |
| 13 nov 2026 | El modelo de la subida calcula los bytes con la generación del contador, otro dato que el código no ve | 11 y 22 |

## Fuentes

- René Descartes, «Discurso del método», 1637, segunda parte. Las 4 reglas de evidencia, análisis, orden y recuento.
- La inversión, máxima de Carl Jacobi, difundida por Charlie Munger.
- Chaudhuri y otros, «AlphaProof Code: Verifying Signal's Security at the Machine-Code Level», Google DeepMind, 10 de
  noviembre de 2026. La especificación como contrato aprobado, el portero, las enmiendas con contraejemplo, el crítico
  de otra familia y los errores reinyectados.
