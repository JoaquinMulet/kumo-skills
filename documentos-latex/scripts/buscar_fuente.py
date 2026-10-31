"""Busca frases o cifras en el texto de una fuente primaria y dice en qué página están.

Uso:
  uv run python -I -X utf8 scripts/buscar_fuente.py fuente.txt "texto a buscar" ["otro texto" ...]

Lee un texto plano sacado de la fuente (por ejemplo un prospecto S-1 de la SEC). Las páginas se
reconocen por su número, escrito solo en una línea al pie de la página y seguido de la línea
«Table of Contents», que es como los presenta la SEC. Una línea pertenece a la página cuyo número
aparece DESPUÉS de ella. Los estados financieros se numeran F-1, F-2 y así.
Si tu fuente marca las páginas de otra forma, cambia PIE y SIGUIENTE y prueba con 3 páginas que
conozcas antes de confiar en el resultado.

La búsqueda no distingue mayúsculas y normaliza los espacios, porque el texto extraído trae saltos
de línea dentro de las frases. Muestra hasta 6 coincidencias por consulta y el total.
"""

import re
import sys
from pathlib import Path

PIE = re.compile(r"^(F-)?\d{1,3}$|^[ivx]{1,5}$")  # número de página arábigo, F-n o romano
SIGUIENTE = "Table of Contents"
VENTANA = 4  # líneas que se juntan para encontrar una frase partida en varias líneas
MAXIMO = 6


def paginas(lineas):
    """Devuelve, para cada línea, el número de página al que pertenece."""
    pies = [(i, lineas[i].strip()) for i in range(len(lineas) - 1)
            if PIE.match(lineas[i].strip()) and lineas[i + 1].strip() == SIGUIENTE]
    asignada, k = [], 0
    for i in range(len(lineas)):
        while k < len(pies) and pies[k][0] < i:
            k += 1
        asignada.append(pies[k][1] if k < len(pies) else "?")
    return asignada, len(pies)


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    ruta = Path(sys.argv[1])
    if not ruta.exists():
        print(f"No existe {ruta}", file=sys.stderr)
        sys.exit(2)
    lineas = ruta.read_text(encoding="utf-8").split("\n")
    pag, n_pies = paginas(lineas)
    if n_pies == 0:
        print("No encontré ningún pie de página. Ajusta PIE y SIGUIENTE para esta fuente.", file=sys.stderr)
    plano = [" ".join(l.split()) for l in lineas]
    for consulta in sys.argv[2:]:
        q = " ".join(consulta.split()).lower()
        hallados = 0
        for i in range(len(plano)):
            ventana = " ".join(plano[i:i + VENTANA]).lower()
            pos = ventana.find(q)
            # la coincidencia cuenta en la línea donde empieza, para no repetirla en las siguientes
            if pos >= 0 and pos < len(plano[i]) + 1:
                hallados += 1
                if hallados <= MAXIMO:
                    print(f"[{consulta}] p. {pag[i]} (línea {i + 1}): {' '.join(plano[i:i + 3])[:240]}")
        print(f"[{consulta}] {hallados} coincidencias\n")


if __name__ == "__main__":
    main()
