import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
def objetivo(defecto='curso_v4_wip.html'):
    """Archivo a verificar. Argumento > variable de entorno > el v4 en curso."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    return os.path.join(AQUI, '..', os.environ.get('CURSO_HTML', defecto))
