---
name: desarrollo-riguroso
description: La portada del estándar de desarrollo de Kumo. Dice qué skill de pstack leer en cada situación de código (bug, test, diseño de datos, verificación, revisión de un cambio, corrección del usuario) y agrega las reglas propias de Kumo que pstack no trae. Usa esta skill al partir un proyecto nuevo, al sembrar o revisar su CLAUDE.md, al escribir o corregir código, al diseñar el testing, o cuando el usuario menciona cómo desarrollar, estándar de desarrollo, TDD, test-first, arreglar un bug, calidad de código, verificar que algo funciona, o hacer las cosas bien. USO OBLIGATORIO. Se lee COMPLETA, termina en el marcador FIN-DESARROLLO-RIGUROSO, y si no lo viste sigue leyendo con Read antes de actuar. Su sección «Higiene continua del repo» se aplica siempre.
---

# Desarrollo riguroso. La portada de Kumo sobre pstack

Desde el 3 de noviembre de 2026 los principios de ingeniería de Kumo son los de pstack, de Lauren
Tan (licencia MIT, copiados a este repo). Esta skill ya no los repite. Dice cuál leer en cada
situación y agrega lo que pstack no trae. La decisión de Joaquín que la ordena es una sola. Un
trabajo queda bien hecho cuando una comprobación automática lo demuestra, no cuando otro agente
opina que está bien.

## Cómo se lee una skill de pstack aquí

Las skills de pstack no se cargan solas, porque llevan `disable-model-invocation: true`. Se leen con
`Read`, desde la carpeta hermana de esta skill (`../<nombre>/SKILL.md`), cuando la tabla de abajo lo
pide. Están escritas para Cursor. Antes de seguir una que nombre `Task`, `readonly`, un modelo `grok`
o una ruta `.cursor/`, lee [`reference/pstack-en-claude-code.md`](reference/pstack-en-claude-code.md),
que traduce cada nombre a Claude Code.

## Qué leer en cada situación

| Situación | Lee antes de actuar |
|---|---|
| Vas a diseñar o construir algo que no es solo apariencia o texto | `especificar-antes-de-construir`, que se carga con la herramienta Skill y va antes que cualquier otra fila. Su ficha aprobada es el contrato del cambio |
| Vas a escribir código con estado, o el código ramifica mucho | `principle-model-the-domain`, `principle-type-system-discipline` |
| Validas datos que entran, manejas errores o adaptas un framework | `principle-boundary-discipline` |
| Un comando o un proceso puede correr 2 veces o cortarse a la mitad | `principle-make-operations-idempotent` |
| Arreglas un bug | `tdd`, `principle-fix-root-causes` |
| 2 arreglos con la misma premisa fallaron | `principle-attack-the-premise` |
| Escribes, cambias o conservas un test | `principle-test-behavior-not-implementation` |
| El trabajo no es trivial (varias ediciones, una migración, un análisis) | `principle-build-the-lever`, `principle-sequence-verifiable-units` |
| Vas a agregar algo a un sistema que existe | `principle-subtract-before-you-add` |
| Vas a decir «listo» | `principle-prove-it-works` |
| Mediste un número (tiempo, conteo, cuadre) y vas a reportarlo | `principle-explain-the-number` |
| El proyecto no tiene un script que maneje la app real y junte evidencia | `create-verification-skill`, y después `maintain-verification-skill` |
| Hay código donde un error cuesta caro y los tests no llegan (dinero, concurrencia, estados) | `create-formal-verification-skill`, `statechart`, `maintain-formal-verification-skill` |
| Quieres saber qué puede romper un cambio fuera del diff | `blast-radius` |
| Un cambio o un diseño importante va a entrar al trunk | `interrogate` |
| El usuario te corrigió, o repetiste un error | `correct`, `principle-encode-lessons-in-structure` |
| Escribes un documento, un README o un mensaje de commit | `technical-writing`, y al final `unslop` |
| Trabajo largo o sin supervisión que alguien revisa después | `show-me-your-work` |

## Ajustes de Kumo a pstack

Mandan sobre lo que diga la skill de pstack.

- Un subagente corre sus comandos en primer plano, con `timeout`. pstack dice segundo plano. El
  29 de octubre de 2026 un subagente quedó esperando su aviso y el sistema lo cortó a los 10 minutos.
- En Claude Code no hay Grok. Un panel «de varios modelos» queda en un solo modelo. Por eso en
  `interrogate` solo vale el hallazgo que trae su comando y la salida de ese comando.
- Un fan-out de más de 6 agentes se propone a Joaquín antes de lanzarlo.
- Un mensaje a un tercero sale solo con el texto visado por Joaquín. pstack lo dice también.
- No se usa `poteto-mode`. Cuando una skill de pstack nombra su sección Subagents, aplica esta tabla y
  estos ajustes.
- En `create-formal-verification-skill`, cada dato que usa el sistema dentro del modelo lleva una fila con el archivo y
  la línea del código que lo lee. Un dato sin fila es un dato del mundo, y el modelo no puede dárselo al sistema. El
  11 y el 13 de noviembre de 2026 el modelo de la subida de AeroStratus le dio al agente 2 datos que el router no ve.
- Las reglas que se verifican sobre el código salen del modelo o de la ficha aprobada, nunca del código. El 13 de
  noviembre de 2026 una regla de Kani copiada del código demostró solo que el código cumple consigo mismo.

## Reglas de Kumo que pstack no trae

1. Un valor que cambia en el tiempo (una tarifa, un precio, una tasa) se guarda con vigencia. El
   cambio entra como versión nueva y el valor viejo no se pisa. Pisarlo recalcula en silencio lo ya
   cerrado. Un proveedor subió su tarifa un 10 por ciento, y pisar la constante habría recosteado
   meses ya cuadrados al peso con el contador.
2. Una escritura que no puede guardar el hecho entero pierde la parte que no cabe, y nada falla. Una
   factura en euros se convirtió a pesos para el asiento, la cuenta por pagar se rearmó desde el
   asiento, y el monto en euros desapareció. Antes de escribir pregunta si algún campo del dato de
   entrada no queda guardado.
3. La verdad contra la que se compara puede ser dura (una spec, un estándar) o blanda (una persona,
   un sistema que se atrasa). Con la dura se copia fiel. Con la blanda se cuadra y la diferencia
   queda nombrada a la vista. Si varios sistemas independientes coinciden en una respuesta que la
   referencia marca como errada, se revisa la referencia.
4. Antes de borrar o detener un recurso en una cuenta compartida, se prueba quién lo usa por sus
   referencias, nunca por su nombre o su etiqueta. Después del borrado se buscan referencias rotas.
5. El informe se escribe para quien decide. La conclusión va en la primera línea, en palabras del
   negocio. Si el lector dice «no entiendo», el error es del informe.

## Higiene continua del repo

Se aplica siempre. Un repo sin su aparato de higiene no puede commitear, y el hook
`hooks/exigir-higiene.mjs` lo impide. Los principios están en
[`reference/higiene-principios.md`](reference/higiene-principios.md). La receta de 5 pasos para
escribir una comprobación de clase, el trinquete que se calcula y los 7 pasos para instalar el
aparato en un repo que no lo tiene están en [`reference/higiene-continua.md`](reference/higiene-continua.md).
Ábrelos al entrar a un repo nuevo.

## El CLAUDE.md de cada proyecto

- Su primera línea ordena seguir paginando si la lectura se corta.
- Arriba van la rama que se despliega, el comando de deploy y los comandos de test.
- Lleva la tabla de `correct`, que empareja cada regla con lo que la hace cumplir. Una regla sin
  comprobación queda marcada como pendiente.
- No lleva nada que se pueda leer del código, de una consulta o de `git`.

## La paranoia del compounding

Cada corrección del usuario se arregla en el mismo turno con `correct`. El orden es arquitectura,
después tipos, después lint o hook, después test, y el texto queda solo para lo que necesita juicio.
La comprobación nueva se prueba contra el error real que la originó y tiene que ponerse roja. Si el
usuario tuvo que pedir el aprendizaje, el reflejo ya falló. El hook `UserPromptSubmit` de
`~/.claude/settings.json` lo recuerda en cada mensaje.

Esta skill vive en el repo `kumo-skills`. Para editarla se sigue la sección «Cuando Claude edite una
skill INSTALADA» del `CLAUDE.md` de ese repo.
<!-- FIN-DESARROLLO-RIGUROSO -->
