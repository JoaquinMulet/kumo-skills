---
name: verificacion-adversarial
description: >-
  Comprueba las cifras, citas y afirmaciones de un texto YA ESCRITO contra su fuente primaria bajada
  al disco, con un script que confirma que cada cita existe en el archivo y cuenta términos para
  probar ausencias. El producto es un veredicto por afirmación (aparece, no aparece, falta abrir la
  fuente) con la corrección exacta, nunca un informe nuevo. Usar cuando un texto que afirma hechos va
  a publicarse o enviarse (informe a cliente, artículo, tesis de inversión, peritaje) y el usuario
  pide comprobar si es cierto, contrastar cifras contra su fuente, verificar citas, auditar las
  fuentes, o dice "verifica estas cifras", "esto se publica", "refuta esto", "qué de esto es verdad".
  NO usar para una pregunta abierta sin afirmaciones previas (eso es investigar) ni para juzgar si un
  texto se entiende (doc-prueba-de-uso).
---

# Verificación adversarial. Cada cita se prueba en el archivo

Desde el 3 de noviembre de 2026 esta skill no lanza refutadores. La prueba de una afirmación es
abrir la fuente primaria, bajarla al disco y encontrar ahí la frase o la cifra con un script. Otro
agente que no logra refutarla no prueba nada. El 17 de agosto de 2026 un agente entregó citas de la
OCDE con página y texto entre comillas que nunca había abierto, y el archivo en disco zanjó el caso
en un minuto.

## El procedimiento

1. Lista las afirmaciones del texto que cargan la conclusión, cada una con la fuente que la
   respalda. Esa lista se escribe antes de buscar nada.
2. Baja cada fuente primaria a una carpeta nueva de la carpeta de borradores. Un resumen, una nota
   de prensa o una cita de otro autor no son la fuente. Si hay muro de pago o un 403, anota qué rutas
   probaste (el sitio del emisor, Internet Archive, un repositorio académico) y respeta el robots.txt
   y las condiciones de uso de cada sitio.
3. Corre el script por cada afirmación.

   ```
   uv run --with pymupdf python -I scripts/buscar_en_fuente.py fuente.pdf --cita "texto exacto"
   ```

   Para probar que algo no está, usa `--contar` con el término y con una 2.ª formulación.
   `--sin-acentos` compara sin tildes. Sale con 1 si una cita no aparece.
4. Lee el párrafo entero alrededor de cada coincidencia. El script encuentra la frase, pero una cita
   cortada justo antes de la cláusula que invierte su sentido también aparece.
5. Revisa la medición con tu propio juicio. La cifra tiene que medir el período, el perímetro y la
   unidad que el texto le atribuye. Los errores de categoría más comunes son mezclar lo generado con
   lo almacenado o lo cobrado, lo comprometido con lo ejecutado, y una medición local con una nacional.
6. Entrega una tabla con 3 columnas, la afirmación, el veredicto y la corrección exacta. El veredicto
   es uno de 3.
   - Aparece, con el archivo y la página.
   - No aparece, con la búsqueda que corriste.
   - Falta abrir la fuente, con las rutas que probaste.

## Lo que el script no ve

- Una frase partida entre 2 páginas de un PDF. Si no aparece, busca la mitad de la frase.
- Un PDF escaneado sin texto. El script lo avisa y sale con 2.
- Si la conclusión se sigue de la evidencia. Eso es juicio tuyo.

## Reglas que costaron un error real

- «No lo encuentro» no es «no existe». Una cifra se descartó por «no rastreable» y estaba en el
  artículo original, de un reportero con nombre y fecha. Un negativo vale solo con la fuente abierta
  y la búsqueda corrida.
- 3 fuentes que coinciden pueden venir de 1 sola. Antes de contar una confirmación, comprueba que las
  fuentes no citen al mismo autor.
- Revisa con más dureza lo que conviene a la tesis. En una corrida, 7 de 9 errores graves estaban en
  afirmaciones a favor.
- Si el dato no existe en ninguna fuente pública, eso es un hallazgo que se publica, con la búsqueda
  que lo prueba. No se rellena con una secundaria.
- Si el documento todavía no se envió, el error se corrige en el texto y no queda rastro de él.
