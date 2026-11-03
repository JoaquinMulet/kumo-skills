"""Valida el anexo de las 70 preguntas del checklist de estados financieros.

Qué espera. La ruta del anexo en Markdown o texto. Cada respuesta empieza en su propia línea con su
número y un punto («23.» o «**23.**»), y sigue hasta la respuesta siguiente.

Qué comprueba. Que estén las 70 respuestas y que cada una traiga evidencia (una cifra, un documento,
una nota o un módulo del modelo, como pide la regla del 14 de agosto de 2026) o la marca [SIN DATO].
Un checklist con huecos silenciosos es peor que ninguno. Si las respuestas vienen fuera de orden, solo
cuenta la 1.ª secuencia creciente, porque una lista numerada dentro de una respuesta reinicia en 1.

Sale con 0 si el anexo está completo, 1 si falta algo, 2 si el archivo no existe.

Uso.
  uv run python -I scripts/validar_anexo.py anexo.md
"""

import re
import sys
from pathlib import Path

TOTAL = 70  # preguntas del checklist v2 en reference/checklist-lehman.md
# Sin sangría. Una línea con sangría que empieza con una cifra («    47. La diferencia…») es la
# continuación de una respuesta, no una respuesta nueva. Pasó en el anexo real de Cencosud.
INICIO = re.compile(r"^[>*_]*[ \t]?\**(\d{1,2})\.\**[ \t]", re.M)
# La regla de la casa (14 de agosto de 2026) acepta como evidencia una cifra, un documento, una
# página o un módulo del modelo. Una cifra basta, y por eso cualquier dígito cuenta.
EVIDENCIA = re.compile(
    r"\[SIN DATO\]|\d|\bmódulo\b|\bmemoria\b|\bnota\b|\binforme\b|\bestados?\b",
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
    # Una lista numerada dentro de una respuesta («1. la primera señal», «2. …») reinicia la
    # numeración. Solo cuenta como respuesta nueva un número mayor que el último aceptado.
    # Lo que queda debajo se suma a la respuesta anterior.
    marcas = []
    for m in INICIO.finditer(texto):
        if not marcas or int(m.group(1)) > int(marcas[-1].group(1)):
            marcas.append(m)
    respuestas = {}
    for k, m in enumerate(marcas):
        fin = marcas[k + 1].start() if k + 1 < len(marcas) else len(texto)
        respuestas[int(m.group(1))] = texto[m.end():fin]

    faltan = [n for n in range(1, TOTAL + 1) if n not in respuestas]
    sin_evidencia = [n for n in range(1, TOTAL + 1) if n in respuestas and not EVIDENCIA.search(respuestas[n])]
    print(f"Leí {ruta}. Encontré {len([n for n in respuestas if 1 <= n <= TOTAL])} de {TOTAL} respuestas.")
    if faltan:
        print(f"  Faltan las preguntas {', '.join(map(str, faltan))}.")
    if sin_evidencia:
        print(f"  Sin cifra, documento, módulo ni [SIN DATO]: {', '.join(map(str, sin_evidencia))}.")
    if faltan or sin_evidencia:
        print("ROJO. El anexo tiene huecos.")
        return 1
    print("VERDE. Las 70 preguntas tienen evidencia o la marca [SIN DATO].")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
