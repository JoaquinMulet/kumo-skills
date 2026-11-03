# Prompts de orquestación multi-agente

Las ocho piezas del `SKILL.md` gobiernan el prompt que un agente ejecuta. Este documento cubre otra especie: el **prompt de orquestación** — el que recibe un agente raíz que va a dirigir un enjambre de sub-agentes en una búsqueda persistente (demostrar algo difícil, cazar una causa raíz esquiva, agotar un espacio de diseño). Aquí el prompt no describe una tarea: describe una **política de búsqueda** — cómo gestionar el portafolio de enfoques, cuándo insistir, y qué cuenta exactamente como terminado.

**Cuándo aplica.** El problema no se resuelve en una pasada, existen múltiples enfoques incompatibles posibles, y el riesgo dominante es doble: que el sistema declare victoria sobre un resultado parcial, o que todos los agentes converjan prematuramente al mismo enfoque atractivo pero incompleto.

## Las nueve piezas de un prompt de orquestación

Lista completa primero; al final, un ejemplo que las aplica todas.

### 1. Contrato de resultado con definición negativa

Definir "hecho" en positivo no basta: hay que enumerar explícitamente qué **NO** cuenta como éxito. Casos especiales, reducción a otro problema igual de no-resuelto, verificación computacional parcial, candidato sin certificado completo — cada uno nombrado. El atajo favorito de un sistema bajo presión es vestir progreso parcial de resultado final; la lista negativa se lo cierra por nombre, uno por uno.

### 2. Cierre de salidas-escape

Además de lo que no cuenta como éxito, nombrar las **respuestas cómodas prohibidas**: "no retornes solo porque los enfoques actuales fallaron", "no respondas que el problema está abierto", "no entregues un resumen de mejor esfuerzo ni una explicación de por qué es difícil". Cada escape que no nombres es exactamente el que el sistema tomará cuando la búsqueda se ponga cuesta arriba.

### 3. Premisa operativa fijada

"Asume para efectos de esta tarea que existe una solución completa" quita del tablero dos fugas: litigar la premisa y rendirse temprano. Peligro real: la premisa presiona a **fabricar** una solución que no existe. Solo es legítima acompañada de una auditoría adversarial con poder de veto (pieza 7): la premisa empuja a seguir buscando; la auditoría impide inventar. Nunca la una sin la otra.

### 4. Política de portafolio por heurísticas, no topología fija

No "N agentes para la estrategia X". En su lugar, reglas de gestión que el orquestador aplica ronda a ronda: partir con un portafolio genuinamente diverso de formulaciones; mantener un **registro explícito de familias de enfoque**, agrupadas por el mecanismo de fondo y no por la redacción superficial; redirigir agentes hacia formulaciones subexploradas cuando una familia se satura. La topología fija muere con el primer plan; la política sobrevive a cualquier plan.

### 5. Independencia epistémica y polinización diferida

No contarle a la mayoría de los agentes cuál es el enfoque favorito del momento. En rondas tempranas la independencia vale más que la coordinación, porque evita que todos converjan a la misma reducción atractiva. Mantener vivas varias rutas incompatibles durante varias rondas, y cruzar ideas entre ellas **solo después** de que cada una se desarrolló lo suficiente para exponer sus fuerzas y huecos reales. Polinizar temprano homogeneiza; polinizar tarde combina.

### 6. Economía de rutas: bloqueo, reapertura y anti-elegancia

Cuando una ruta se estanca en un lema faltante de fuerza equivalente al problema original, se marca **bloqueada**; solo se le reasignan agentes si alguien propone un mecanismo, invariante o construcción genuinamente nuevos — el entusiasmo renovado no cuenta. Y la regla anti-seducción: no dejar que un enfoque domine solo porque produce reducciones elegantes. Una reducción que termina en algo tan difícil como el problema original no es progreso, por linda que sea.

### 7. Moneda concreta y adversarial continuo

Exigir que cada agente devuelva **artefactos juzgables** — lemas probados, construcciones, ecuaciones, contraejemplos a sublemas propuestos — y rechazar explícitamente reportes de estado, optimismo vago y el clásico "el paso restante es rutinario". Todo candidato a solución pasa por agentes adversariales **durante toda la corrida**, no solo al final. La imparcialidad de esos auditores sigue las reglas de la pieza 8 del `SKILL.md`: contexto limpio, ven solo lo juzgable.

### 8. Permisos de herramientas con carve-out

Cuando una herramienta sirve para el trabajo pero también puede invalidarlo, autorizar el mecanismo y prohibir el uso tóxico en la misma oración: "puedes buscar en la web para background matemático ordinario o teoremas estándar con nombre; no para buscar la solución de este problema exacto ni para determinar si está abierto". Un permiso binario (todo o nada) o amputa capacidad útil o contamina el resultado; el carve-out conserva ambas cosas.

### 9. Presupuesto y criterio de parada honesto

Dos defectos frecuentes en prompts de orquestación agresivos, que no hay que copiar:

- **Condiciones de término contradictorias** — un párrafo permite reportar "el derivado parcial más fuerte y su hueco exacto" y otro prohíbe retornar sin la solución completa. El orquestador queda con dos contratos incompatibles y elige uno al azar bajo presión.
- **Persistencia sin cota** — "no retornes nunca hasta lograrlo" sin presupuesto es un loop infinito con factura.

La forma correcta: **una** condición de retorno por éxito, sin ambigüedad ("retorna solo cuando la solución sobreviva la auditoría adversarial"), más **una** válvula por presupuesto ("si agotas ~X rondas o ~Y tokens sin solución auditada, retorna el derivado más fuerte rigurosamente probado y su hueco exacto, etiquetado como PARCIAL"). La válvula no debilita la persistencia — la vuelve gobernable.

## Relación con las ocho piezas base

Estas nueve no reemplazan a las ocho del `SKILL.md`: se apilan encima. El contrato de resultado (1–2) es la *definition of done* (pieza #6) endurecida con lista negativa; el adversarial continuo (7) generaliza la auditoría externa (pieza #8) de un cierre puntual a una función permanente; los permisos con carve-out (8) son restricciones explícitas (pieza #7) aplicadas a herramientas. Lo genuinamente nuevo es la capa de política (4–6): solo existe cuando el destinatario del prompt dirige a otros agentes, porque gobierna un portafolio, no una ejecución.

## Ejemplo completo

Encargo: encontrar la causa raíz de una corrupción de datos intermitente en un pipeline, con varias hipótesis incompatibles posibles y alto riesgo de "diagnóstico plausible pero equivocado".

> **[Contrato de resultado]** Una solución completa identifica la causa raíz con un mecanismo reproducible: condición de disparo + secuencia de eventos + demostración de que produce exactamente la corrupción observada. NO cuentan como solución: una correlación sin mecanismo, una hipótesis que explica solo parte de los casos observados, una lista de sospechosos ordenada por plausibilidad, ni un fix que hace desaparecer el síntoma sin explicar por qué.
>
> **[Salidas-escape]** No retornes solo porque las hipótesis actuales fallaron. No respondas que el bug "no es reproducible". No entregues un resumen de mejor esfuerzo ni una explicación de por qué el sistema es difícil de diagnosticar.
>
> **[Premisa operativa]** Asume para efectos de esta tarea que la causa raíz existe y es determinable con la evidencia disponible o generable.
>
> **[Política de portafolio]** Gestiona la búsqueda dinámicamente, sin asignación fija de agentes por hipótesis. Parte con un portafolio diverso: condiciones de carrera, corrupción en serialización, fallas de infraestructura, errores de lógica de negocio, interacción entre versiones. Mantén un registro de familias de hipótesis agrupadas por mecanismo de fondo; si muchas convergen a una familia, redirige agentes a las subexploradas.
>
> **[Independencia]** No les digas a la mayoría de los agentes cuál hipótesis va ganando. Mantén varias rutas incompatibles vivas durante varias rondas; cruza evidencia entre ellas solo cuando cada una haya producido hechos verificados propios.
>
> **[Economía de rutas]** Si una hipótesis se estanca en una condición que no puedes observar ni reproducir, márcala bloqueada; reábrela solo ante evidencia o instrumentación genuinamente nueva. No dejes que una hipótesis domine solo porque produce la narrativa más elegante.
>
> **[Moneda concreta + adversarial]** Cada agente retorna artefactos verificables: logs específicos con timestamps, reproducciones, diffs, trazas. Rechaza reportes de estado y afirmaciones de que un paso no verificado es "seguramente lo que pasa". Todo candidato a causa raíz debe sobrevivir a un agente adversarial con contexto limpio que intente refutarlo con la misma evidencia.
>
> **[Permisos con carve-out]** Puedes buscar documentación de las tecnologías involucradas y bugs conocidos de las versiones exactas en uso; no busques "diagnósticos típicos" para adoptarlos sin evidencia local.
>
> **[Presupuesto y parada]** Retorna cuando un candidato sobreviva la auditoría adversarial. Si agotas 6 rondas sin candidato superviviente, retorna la hipótesis mejor soportada, su evidencia exacta, y qué observación específica falta para confirmarla — etiquetada como PARCIAL.

## Cuándo NO usar esta capa

- Tarea de una pasada o fan-out simple y paralelo (revisar N archivos, resumir M documentos): bastan las ocho piezas base y, si hay que medir consistencia, el anexo de estabilidad del `SKILL.md`.
- Y rige siempre la puerta de la casa: un fan-out pesado de agentes **no se lanza sin confirmación explícita** de la persona a cargo, con la aritmética de agentes y rondas a la vista. Este documento enseña a escribir la política; no autoriza a ejecutarla.
