# Ficha de especificación

Copiar este archivo a `docs/fichas/AAAA-MM-DD-tema.md` del proyecto y llenarlo. Cada respuesta lleva 1 de 3 marcas.
HECHO, con su fuente. SUPUESTO, con quién lo garantiza. DECISIÓN, cuando le toca a Joaquín.

- Cambio:
- Proyecto y repo:
- Autor del borrador:
- Estado: borrador / aprobada el AAAA-MM-DD

## Fase 0. ¿Aplica?

Respuesta y razón en 1 línea.

## Fase 1. Evidencia

1. Problema y evidencia medida.
2. Hechos con su fuente, y supuestos.

   | Afirmación | Marca | Fuente o garante |
   |---|---|---|

3. Quién decide y quién carga la consecuencia.

## Fase 2. Propósito

4. Daño que evita, en palabras del negocio.
5. Medida en producción, y cuándo se revisa.

## Fase 3. Inversión

6. Formas en que fracasó, al menos 3.
7. Lo que no debe pasar nunca.
8. Errores parecidos que ya ocurrieron, con su fuente.
9. Cómo podría salir verde la verificación con el sistema roto.

## Fase 4. El mundo y el sistema

10. Actores, estados y eventos.
11. Datos que usa el sistema.

    | Dato | Archivo y línea donde el código lo lee |
    |---|---|

12. Supuestos del mundo.

    | Supuesto | Quién lo garantiza |
    |---|---|

13. Fallas del entorno.

## Fase 5. División y orden

14. Partes del cambio.
15. Orden de construcción, de la más simple a la más compleja.
16. Capa de verificación de cada parte.

    | Parte | Capa | Herramienta |
    |---|---|---|

## Fase 6. Reglas

17 a 20. Cada regla en una fila.

| Regla | Tipo | Daño que evita | Caso real donde se cumple | Error que detecta |
|---|---|---|---|---|

19. Presupuesto de memoria, disco, procesador y disponibilidad.

## Fase 7. Recuento

21. ¿Cada fracaso de la fase 3 tiene su regla? Sí o no. Si es no, cuál falta.
22. ¿Cada dato de la fase 4 tiene su línea de código? Sí o no. Si es no, cuál falta.
23. ¿Cada supuesto tiene garante? Sí o no. Si es no, cuál falta.

## Fase 8. Aprobación

- Aprobada por Joaquín el AAAA-MM-DD, en la conversación del mismo día.

## Enmiendas

| Fecha | Cambio | Contraejemplo o argumento | Aprobada |
|---|---|---|---|
