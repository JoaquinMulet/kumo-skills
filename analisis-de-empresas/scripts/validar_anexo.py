"""Valida el anexo de las 70 preguntas del checklist de estados financieros.

Qué espera. La ruta del anexo en Markdown o texto. Cada respuesta empieza en su propia línea con su
número y un punto («23.» o «**23.**»), y sigue hasta la respuesta siguiente.

Qué comprueba. Que estén las 70 respuestas, una sola vez cada una, y que cada una traiga evidencia
(una página como «p. 45» o «pág. 45», una nota como «nota 12», o un módulo del modelo) o la marca
[SIN DATO]. Un checklist con huecos silenciosos es peor que ninguno.

Sale con 0 si el anexo está completo, 1 si falta algo, 2 si el archivo no existe.

Uso.
  uv run python -I scripts/validar_anexo.py anexo.md
"""

import re
import sys
from pathlib import Path

TOTAL = 70  # preguntas del checklist v2 en reference/checklist-lehman.md
INICIO = re.compile(r"^[ \t>*_-]*\**[ \t]*(\d{1,2})\.\**[ \t]", re.M)
EVIDENCIA = re.compile(
    r"\[SIN DATO\]|\bp\.\s*\d|\bpp\.\s*\d|\bpág(?:ina)?s?\.?\s*\d|\bnota\s+\d|\bmódulo\b|\bF-\d",
    re.I,
)


def main(argv):
    for flujo in (sys.stdout, sys.stderr):
        flujo.reconfigure(encoding="utf-8", errors="replace")
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    ruta = Path(argv[1])
    if not ruta.is_file():
        print(f"No existe {ruta}.", file=sys.stderr)
        return 2
    texto = ruta.read_bytes().decode("utf-8-sig")
    marcas = list(INICIO.finditer(texto))
    respuestas = {}
    repetidas = []
    for k, m in enumerate(marcas):
        n = int(m.group(1))
        fin = marcas[k + 1].start() if k + 1 < len(marcas) else len(texto)
        if n in respuestas:
            repetidas.append(n)
        respuestas[n] = texto[m.end():fin]

    faltan = [n for n in range(1, TOTAL + 1) if n not in respuestas]
    sin_evidencia = [n for n in range(1, TOTAL + 1) if n in respuestas and not EVIDENCIA.search(respuestas[n])]
    print(f"Leí {ruta}. Encontré {len([n for n in respuestas if 1 <= n <= TOTAL])} de {TOTAL} respuestas.")
    if faltan:
        print(f"  Faltan las preguntas {', '.join(map(str, faltan))}.")
    if repetidas:
        print(f"  Aparecen 2 veces las preguntas {', '.join(map(str, sorted(set(repetidas))))}.")
    if sin_evidencia:
        print(f"  Sin página, nota, módulo ni [SIN DATO]: {', '.join(map(str, sin_evidencia))}.")
    if faltan or repetidas or sin_evidencia:
        print("ROJO. El anexo tiene huecos.")
        return 1
    print("VERDE. Las 70 preguntas tienen evidencia o la marca [SIN DATO].")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
