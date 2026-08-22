"""Barrido mecanico de la puntuacion que el proyecto prohibe.

Cubre solo lo que se puede decidir SIN contexto. el guion largo y el
punto y coma. Los dos puntos a mitad de frase NO se tocan aca, porque a
veces introducen una enumeracion legitima y esa distincion necesita
leer, no contar.

Que NO toca, y esto manda sobre todo lo demas.
  - El frontmatter YAML entre --- y ---.
  - Los bloques de codigo delimitados por acentos graves triples.
  - Todo lo que este dentro de acentos graves simples.
  - Las tablas markdown, porque el guion largo suele ser el simbolo de
    «no aplica» en una celda y ahi significa algo.
  - Las flechas ->, que a veces se escriben con guion largo pegado.

Uso.
  python scripts/unslop_puntuacion.py --listar          cuenta, no escribe
  python scripts/unslop_puntuacion.py archivo.md        escribe ese archivo
  python scripts/unslop_puntuacion.py --todos           escribe todos
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Las reglas -------------------------------------------------------

# 1. Par de guiones sin espacio por dentro. «texto —aclaracion— sigue».
#    Es un inciso, y en espanol el inciso va entre comas.
INCISO_PEGADO = re.compile(r'\s—(?=\S)(.+?)(?<=\S)—')

# 2. Guion largo suelto rodeado de espacios, o pegado a la palabra
#    anterior. Se vuelve coma.
SUELTO = re.compile(r'\s*—\s*')

# 3. Punto y coma. Se vuelve punto, y la siguiente letra sube a
#    mayuscula. Siempre es gramatical, a diferencia de la coma, que
#    entre dos oraciones independientes seria un empalme.
PUNTO_Y_COMA = re.compile(r';\s+(\S)')


def _mayus(t):
    return t[:1].upper() + t[1:] if t else t


# Titulo markdown. «## Pilar 1 — TDD» -> «## Pilar 1. TDD».
TITULO = re.compile(r'^(#{1,6} .*?)\s*—\s*(\S)')

# Etiqueta en negrita o en codigo al inicio de una vineta o de un paso
# numerado. «- **IDENTIFY** — nombrar» -> «- **IDENTIFY.** Nombrar».
# Es la forma que la regla 16 del propio unslop declara correcta.
ETIQUETA_NEGRITA = re.compile(r'^(\s*(?:[-*+]|\d+\.)\s+)\*\*(.+?)\*\*\s*—\s*(\S)')
ETIQUETA_CODIGO = re.compile(r'^(\s*(?:[-*+]|\d+\.)\s+)(`[^`]+`)\s*—\s*(\S)')


def transformar_linea(linea):
    """Aplica las reglas a una linea de PROSA. Devuelve (nueva, cambios)."""
    antes_todo = linea

    # Las 2 excepciones corren PRIMERO, sobre la linea entera, porque
    # dependen de donde empieza la linea y la regla generica no lo sabe.
    linea = TITULO.sub(lambda m: m.group(1) + '. ' + m.group(2).upper(), linea)
    linea = ETIQUETA_NEGRITA.sub(
        lambda m: m.group(1) + '**' + m.group(2) + '.** ' + m.group(3).upper(), linea)
    linea = ETIQUETA_CODIGO.sub(
        lambda m: m.group(1) + m.group(2) + '. ' + m.group(3).upper(), linea)

    # Los tramos entre acentos graves simples se apartan y vuelven intactos.
    trozos = re.split(r'(`[^`]*`)', linea)
    for i, t in enumerate(trozos):
        if t.startswith('`'):
            continue
        t = INCISO_PEGADO.sub(lambda m: ', ' + m.group(1) + ',', t)
        t = SUELTO.sub(', ', t)
        t = PUNTO_Y_COMA.sub(lambda m: '. ' + _mayus(m.group(1)), t)
        trozos[i] = t
    salida = ''.join(trozos)

    # Limpieza de los destrozos que dejan las reglas, sobre la linea YA
    # rearmada. Medido en la primera corrida sobre un archivo de prueba.
    # la regla del inciso choca con la coma que ya seguia al cierre y
    # produce «,,», y un guion al final de linea deja una coma colgando
    # con un espacio detras.
    salida = re.sub(r',(\s*,)+', ',', salida)
    salida = re.sub(r',\s+([.,;:)])', r'\1', salida)
    salida = re.sub(r',[ \t]+$', ',', salida)
    return salida, (1 if salida != antes_todo else 0)


def procesar(texto):
    lineas = texto.split('\n')
    en_yaml = False
    en_bloque = False
    cambios = 0
    for i, l in enumerate(lineas):
        if i == 0 and l.strip() == '---':
            en_yaml = True
            continue
        if en_yaml:
            if l.strip() == '---':
                en_yaml = False
            continue
        if l.strip().startswith('```'):
            en_bloque = not en_bloque
            continue
        if en_bloque:
            continue
        # Las tablas quedan fuera. un guion largo en una celda suele ser
        # el simbolo de «no aplica».
        if l.lstrip().startswith('|'):
            continue
        nueva, n = transformar_linea(l)
        if n:
            lineas[i] = nueva
            cambios += n
    return '\n'.join(lineas), cambios


def archivos():
    salida = []
    for d in sorted(os.listdir(RAIZ)):
        p = os.path.join(RAIZ, d, 'SKILL.md')
        if os.path.isdir(os.path.join(RAIZ, d)) and os.path.exists(p):
            salida.append(p)
    salida.append(os.path.join(RAIZ, 'README.md'))
    return salida


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    solo_listar = '--listar' in sys.argv
    objetivo = archivos() if ('--todos' in sys.argv or solo_listar) else [
        os.path.join(RAIZ, a) for a in args]
    if not objetivo:
        print(__doc__)
        return 2

    total = 0
    for ruta in objetivo:
        texto = io.open(ruta, encoding='utf-8').read()
        nuevo, n = procesar(texto)
        total += n
        if n:
            rel = os.path.relpath(ruta, RAIZ).replace('\\', '/')
            print(f"  {n:>4} sitios  {rel}")
            if not solo_listar:
                io.open(ruta, 'w', encoding='utf-8', newline='\n').write(nuevo)
    print(f"TOTAL {total} sitios" + ("  (modo listar, no se escribio nada)" if solo_listar else "  reescritos"))
    return 0


if __name__ == '__main__':
    sys.exit(main())
