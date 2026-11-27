# Síntesis de la revisión forense

Parte del anexo de 15 veredictos ya validado por `scripts/validar_forense.py`. Junta los hallazgos,
calcula cuánto mueven entre todos, escribe las preguntas para el gerente de finanzas y deja listos
los ajustes del paso 5. Si el anexo no tiene hallazgos, esta síntesis es una sola frase que lo dice,
con el puntaje y las pruebas que quedaron sin dato.

## 1. La tabla resumen

Una fila por hallazgo, con el efecto sobre las 3 cifras que el resto del análisis usa. Las pruebas
limpias no van. Las que quedaron sin dato van al final, con lo que falta.

```markdown
| Prueba | Veredicto | Qué se encontró | Utilidad neta | Flujo operacional | Patrimonio |
|---|---|---|---|---|---|
| EM 3 | ALTA | Beneficio tributario por un aporte entre empresas del grupo | 102.243 menos | Sin efecto | Sin efecto |
| CF 3 | BAJA | Cuentas por pagar crecieron más que las ventas | Sin efecto | 77.910 que no se repiten | Sin efecto |
```

## 2. La matriz de cruce

Los hallazgos se suman y se muestran las cifras como quedarían sin ellos. Cada resta lleva su
prueba al lado.

```markdown
| Cifra | Reportada | Ajuste | Ajustada | De qué prueba sale |
|---|---|---|---|---|
| Utilidad neta | 191.396 | 102.243 menos | 89.153 | EM 3 |
| Flujo operacional | 905.930 | 77.910 menos | 828.020 | CF 3 |
| Patrimonio | 1.943.297 | Sin ajuste | 1.943.297 | |
```

Después se marcan los hallazgos que se explican entre sí. Un ingreso adelantado (EM 1) suele venir
con cuentas por cobrar vendidas (CF 1) y con un DSO que baja de golpe (KM 2). Una compra de empresas
(AA 1) suele venir con reservas que después se liberan (EM 5 o EM 7). 3 hallazgos que cuentan la
misma historia pesan más que 3 sueltos, y la síntesis lo dice.

## 3. Qué estaría tapando

Una frase, en palabras del negocio. Es la lección del libro que más se olvida. Detrás de un problema
contable hay que preguntar qué problema del negocio estaba escondido. La frase nombra el deterioro
(ventas que se frenan, margen que cae, caja que no alcanza, una compra que salió mal) y la cifra que
lo muestra una vez hechos los ajustes.

## 4. Las preguntas para el gerente de finanzas

Va una pregunta por cada hallazgo de veredicto MEDIA o mayor. Cada pregunta usa las cifras del
propio informe de la empresa, con su nota, para que no se pueda contestar con «ese dato está mal».

```markdown
### Pregunta 1. Beneficio tributario de 2025 (EM 3, ALTA)

| Dato | Valor | Dónde está |
|---|---|---|
| Beneficio tributario reconocido | 102.243 | Nota 15, página 42 |
| Utilidad antes de impuestos | 89.153 | Estado de resultados |
| Utilidad neta | 191.396 | Estado de resultados |

La empresa reconoció un beneficio tributario de 102.243 por un aporte entre sociedades del grupo.
Es 53 por ciento de la utilidad neta y no trajo caja. ¿Cuál fue el propósito del aporte fuera del
efecto tributario, y cuánto de ese beneficio se repite en 2026?

Si la respuesta es «es el tratamiento que corresponde», la pregunta que sigue es cuánta de la
utilidad de 2026 espera la empresa sin este beneficio.
```

Las preguntas se ordenan por tamaño del efecto, después por veredicto, y al final por si el problema
se puede revertir o no. Son para quien analiza. No se le envían a la empresa sin que Joaquín vise
el texto.

## 5. Lo que pasa a los pasos siguientes

| Hacia | Qué pasa |
|---|---|
| Paso 5, owner earnings | La utilidad ajustada de la matriz es el punto de partida. Salen las ganancias de una vez (EM 3), las reservas liberadas (EM 5 y EM 7) y los ingresos adelantados o sin sustancia (EM 1 y EM 2). Los costos activados de más (EM 4) se suman al capex de mantenimiento |
| Paso 5, prueba de caja | El flujo operacional ajustado reemplaza al reportado. Se le restan las cuentas por cobrar vendidas (CF 1), las salidas clasificadas fuera de la operación (CF 2) y la mejora de capital de trabajo que no se repite (CF 3) |
| Paso 6, tasa de descuento | El puntaje, con la tabla de [`forense-procedimiento.md`](forense-procedimiento.md) |
| Paso 6, puente a la acción | La deuda y los compromisos fuera de balance encontrados en EM 5 y KM 2 se restan como deuda |
| Paso 7, riesgo | Cada prueba sin dato y cada hallazgo de veredicto ALTA o CRÍTICA entran como riesgo nombrado |
| Paso 8, veredicto | La pregunta 4 se aprueba con el puntaje en el tramo «Limpio» o «Dudas» y sin ningún hallazgo crítico |
