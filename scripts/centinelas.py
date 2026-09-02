"""CENTINELAS. Las ideas compradas con auditorias no pueden desaparecer.

Por que existe, y por que no basta con haber arreglado el texto.

Cada pasada de auditoria (completitud, cadena causal, prueba de uso)
termina en parches. Un parche vive en una redaccion concreta. Cuando el
documento se reescribe, la redaccion cambia y el parche desaparece SIN
QUE NADIE LO NOTE, porque el resultado sigue leyendose bien. El hueco no
deja hueco visible, deja un texto fluido al que le falta una respuesta.

El inventario duro (encabezados, tablas, cifras) sobrevive porque se
verifica mecanicamente. Los arreglos SEMANTICOS no sobreviven a nada.

Cada centinela apunta a la IDEA MINIMA, no a la frase larga. Una frase
larga falla con cualquier reescritura y se vuelve ruido que se ignora.

Uso.
  python scripts/centinelas.py            falla si falta alguno
  python scripts/centinelas.py --listar   solo informa
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# archivo -> { nombre del arreglo: patron de la idea minima }
CENTINELAS = {
    "desarrollo-riguroso/SKILL.md": {
        # El contrato de lectura. La declaracion vive en la description,
        # que es lo unico que llega sin truncar, y el marcador cierra el
        # archivo. Si falta uno de los 2, el contrato promete algo que no
        # se puede comprobar, que es peor que no prometerlo.
        "la description obliga a leerla completa": r"Se lee COMPLETA",
        "la description nombra el marcador": r"termina en el marcador\s+FIN-DESARROLLO-RIGUROSO",
        "la description obliga la higiene": r"Higiene continua del repo. se aplica siempre",
        "el marcador de cierre existe": r"<!-- FIN-DESARROLLO-RIGUROSO -->",
        # De doc-cadena-causal. la analogia del queso no se armaba.
        "que es una lamina": r"La lámina es la capa que revisa",
        "que es un agujero": r"agujeros son los casos que esa capa no mira",
        "por que toda capa tiene agujeros": r"ninguna predicción cubre lo que su autor no imaginó",
        "el agujero es una eleccion": r"forma que tiene esa capa de haber elegido qué mira",
        # De doc-cadena-causal. contradicciones internas.
        "el trinquete NO es el que bloquea": r"trinquete no es el que\s+(?:te\s+)?bloquea",
        "quien apaga el informe": r"apagándolo, y ahí pierdes la lista entera",
        # De doc-completitud. la definicion inline del termino central.
        "que es una comprobacion de clase": r"lee el código fuente entero como\s+texto",
        # La regla del dueno del 21 de agosto de 2026.
        "la duracion no decide": r"duración NO decide",
        "hacerlo mas rapido, no mas corto": r"hacerlo más rápido",
        # Verde no es limpio, las 4 formas.
        "el estado no es el veredicto": r"dice si la herramienta CORRIÓ, no si encontró algo",
        "un control que mira otro artefacto": r"verifica \*\*contra qué\s+artefacto corre\*\*",
        "una funcion a medio encender": r"Escribir el archivo no es habilitar la",
        "un push en 0 no es una CI verde": r"push que termina en 0 no es una CI verde",
        "la CI remota se lee antes de desplegar": r"Después de empujar y antes de desplegar",
        # El trinquete computado.
        "la linea base se computa": r"no es un\s+trinquete, es un comentario",
        "la misma vara": r"MISMA vara",
        # La leccion que ordena la eleccion de herramientas.
        "catalogo mide forma, lo tuyo mide verdad": r"miden la forma[.;]\s+[Ss]olo las que nacen de un fallo tuyo",
        # El puntero al anexo tiene que decir QUE lleva.
        "el puntero nombra la receta": r"receta de 5 pasos para escribir una\s+comprobación de",
    },
    "desarrollo-riguroso/reference/higiene-continua.md": {
        # De doc-completitud. el vacio mas grande.
        "receta de la comprobacion de clase": r"Cómo se escribe una comprobación de clase",
        "el remedio del mensaje se prueba": r"prueba que ese remedio pase el",
        "la prueba de la prueba usa la MISMA funcion": r"la misma función\*\* que usa la comprobación",
        # De doc-completitud. las 2 herramientas que no existian.
        "el trinquete y el informe se escriben": r"los escribes tú",
        "la configuracion sale del arbol actual": r"CONFIGURACION del arbol actual",
        # De doc-cadena-causal.
        "el costo de leer parejas": r"el informe parece más largo de lo que es",
        "que es un BOM": r"marca de orden de bytes",
        "el BOM lo tolera quien lo escribio": r"lo tolera y el siguiente que lo lea falla",
        # Generalizacion por lenguaje, que es el pedido del dueno.
        "inventariar los lenguajes reales": r"inventariar qué lenguajes tiene",
        "un repo poliglota a medias da falsa tranquilidad": r"tranquilidad falsa, que\s+es peor que no medir",
        # El paso que todos se saltan.
        "el paso 5 es el que atrapa": r"paso 5 es el que se salta todo el mundo",
    },
}


def main():
    solo_listar = "--listar" in sys.argv
    faltan = []
    total = 0
    for rel, mapa in CENTINELAS.items():
        ruta = os.path.join(RAIZ, rel)
        if not os.path.exists(ruta):
            faltan.append(f"{rel}: EL ARCHIVO NO EXISTE")
            continue
        # Los espacios se normalizan ANTES de buscar. El texto se reajusta
        # a 90 columnas en cada edicion, asi que una frase puede partirse
        # en otro lugar sin cambiar de idea. Sin esto, mover un salto de
        # linea se leia como una idea perdida (paso el 2 de septiembre de
        # 2026 con «Escribir el archivo no es habilitar la»), y un control
        # con falsos positivos se termina ignorando entero.
        texto = " ".join(io.open(ruta, encoding="utf-8").read().split())
        for nombre, patron in mapa.items():
            total += 1
            if re.search(patron, texto) is None:
                faltan.append(f"{rel}: se perdio «{nombre}»  (buscaba: {patron})")

    print(f"CENTINELAS. {total - len(faltan)} de {total} presentes.")
    if not faltan:
        print("VERDE. Ninguna idea comprada con auditorias se perdio.")
        return 0

    for f in faltan:
        print("  x " + f)
    if solo_listar:
        print("\nModo listar. no se falla por nada.")
        return 0
    print(
        "\nROJO. Una reescritura borro ideas que costaron una auditoria.\n"
        "Antes de dar por bueno esto, decide UNA POR UNA si cada idea esta\n"
        "REFORMULADA (entonces actualiza su patron aca) o PERDIDA (entonces\n"
        "vuelve a ponerla en el texto). Separar esas 2 cosas es justamente el\n"
        "trabajo que este control existe para obligar."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
