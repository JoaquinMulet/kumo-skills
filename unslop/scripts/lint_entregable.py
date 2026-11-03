"""Revisa un entregable contra las reglas de Joaquín que se pueden comprobar sin leer el sentido.

Qué espera. Una o más rutas de archivos de texto (.md, .txt, .tex, .html).

Qué marca, con archivo y línea.
  - Una estimación de esfuerzo por tarea (jornadas, horas de trabajo, días-persona). Regla del
    6 de septiembre de 2026. Un plan lleva tareas, orden y precondiciones, sin horas.
  - Una instrucción de no contarle algo a alguien («no hay que decirle»). Regla del 6 de
    septiembre de 2026. Se elige cómo se dice un dato, nunca si se dice.
  - «pagado por» o «pagador» sin decir a quién se le paga. Regla del 31 de octubre de 2026. Toda
    frase de dinero nombra a quién paga y a quién le paga.
  - Una duda narrada en vez de resuelta («conviene confirmarlo», «lo confirmé»). Regla del 29 de
    octubre de 2026. Si la fuente está a mano, va la cifra con su cita.

Las 2 últimas a veces son correctas, porque dependen del sentido. El script las marca para que
alguien las lea, y la salida dice cuáles son de revisión.

Salida. Sale con 0 si no hay marcas, 1 si hay alguna, 2 si un archivo no existe.

Uso.
  uv run python -I scripts/lint_entregable.py informe.md plan.md
"""

import re
import sys
from pathlib import Path

REGLAS = [
    (
        "esfuerzo",
        "estimación de esfuerzo por tarea. Un plan lleva tareas, orden y precondiciones, sin horas",
        re.compile(
            r"\b\d+(?:[.,]\d+)?\s*(?:a\s*\d+\s*)?(?:jornadas?|horas[- ](?:hombre|persona)|horas de (?:trabajo|desarrollo|esfuerzo)"
            r"|d[ií]as[- ](?:hombre|persona)|semanas[- ](?:hombre|persona)|story points?|puntos de historia)\b"
            r"|\besfuerzo estimado\b",
            re.I,
        ),
    ),
    (
        "no decir",
        "instrucción de no contarle algo a alguien. Se elige cómo se dice, nunca si se dice",
        re.compile(
            r"\bno\s+(?:hay\s+que|conviene|es\s+necesario|debemos|deber[ií]amos)\s+(?:dec[ií]rle|contarle|mencion[aá]rle|avis[aá]rle|inform[aá]rle)"
            r"|\bno\s+(?:le\s+)?(?:digas|cuentes|menciones|avises)\b|\bsin\s+(?:dec[ií]rle|contarle)\b|\bpara\s+no\s+alarmar(?:lo|la|los)?\b",
            re.I,
        ),
    ),
    (
        "quién paga (revisar)",
        "frase de dinero sin destinatario. Escribe «X le paga a Y», con los 2 nombres",
        re.compile(r"\bpagad[oa]s?\s+por\b|\bpagador(?:a|es)?\b", re.I),
    ),
    (
        "duda narrada (revisar)",
        "duda narrada en vez de resuelta. Va la cifra con su cita, o se atribuye a quien la dijo",
        re.compile(
            r"\bconviene\s+confirmar(?:lo|la)?\b|\bpor\s+confirmar\b|\blo\s+confirm[eé]\b|\bfalta\s+verificar\b|\bno\s+verificad[oa]\b|\bpendiente\s+de\s+confirmar\b",
            re.I,
        ),
    ),
]


def lineas_sin_codigo(texto):
    """Devuelve (número de línea, texto) fuera de los bloques de código delimitados con 3 acentos graves."""
    en_codigo = False
    for n, linea in enumerate(texto.splitlines(), 1):
        if linea.lstrip().startswith("```"):
            en_codigo = not en_codigo
            continue
        if not en_codigo:
            yield n, re.sub(r"`[^`]*`", " ", linea)


def main(argv):
    for flujo in (sys.stdout, sys.stderr):
        flujo.reconfigure(encoding="utf-8", errors="replace")
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    marcas = 0
    for arg in argv[1:]:
        ruta = Path(arg)
        if not ruta.is_file():
            print(f"No existe {ruta}.", file=sys.stderr)
            return 2
        texto = ruta.read_bytes().decode("utf-8-sig", errors="replace")
        for n, linea in lineas_sin_codigo(texto):
            for nombre, explicacion, patron in REGLAS:
                m = patron.search(linea)
                if m:
                    marcas += 1
                    print(f"{ruta}:{n}  [{nombre}] «{m.group(0)}». {explicacion}.")
    print(f"\n{marcas} marcas." if marcas else "VERDE. Sin marcas.")
    return 1 if marcas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
