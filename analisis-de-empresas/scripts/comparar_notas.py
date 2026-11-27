"""Muestra qué frases cambiaron entre el informe del período anterior y el de este período.

Qué espera. 2 archivos ya bajados al disco, primero el anterior y después el actual (.txt, .md,
.html, .htm, .xml o .pdf). Pueden ser el informe completo o una nota copiada a un archivo.

Qué devuelve. 3 listas. Las frases que CAMBIARON, con las palabras que entraron entre [+ +] y las
que salieron entre [- -]. Las frases NUEVAS, que no tienen pareja en el informe anterior. Las
frases que DESAPARECIERON. Una frase que solo cambió sus cifras o sus fechas no se reporta, porque
las cifras cambian todos los años y taparían lo que importa. Sale con 0 si pudo comparar y con 2 si
el uso o un archivo están mal.

Sin opciones muestra solo las frases que tocan temas contables (ingresos, provisiones, estimaciones,
cuentas por cobrar, inventario, reservas, reclasificaciones), y dice cuántas dejó fuera.

Opciones.
  --contiene TÉRMINO   deja solo las frases que traen ese término. Se puede repetir.
  --todo               muestra todas las frases, también las que no tocan temas contables.
  --max N              frases que se muestran por lista. 40 si falta.

Uso.
  uv run python -I scripts/comparar_notas.py fuente/10k-2015.txt fuente/10k-2016.txt
  uv run python -I scripts/comparar_notas.py memoria-2023.pdf memoria-2024.pdf --contiene ingresos --contiene "se reconoce"
  Con un PDF, corre con: uv run --with pymupdf python -I scripts/comparar_notas.py ...

Por qué existe. La técnica que el libro de Schilit más recomienda es comparar cada informe con el
anterior, porque una empresa solo cambia la redacción de una nota cuando algo cambió. Leer 2
informes de 200 páginas buscando la frase distinta no lo hace nadie.
"""

import difflib
import html
import re
import sys
from collections import Counter
from pathlib import Path

LARGO_MINIMO_DE_FRASE = 40
PARECIDO_MINIMO_PARA_SER_LA_MISMA_FRASE = 0.6
CANDIDATAS_POR_FRASE = 6
LARGO_MINIMO_DE_PALABRA_QUE_IDENTIFICA = 5
MAXIMO_POR_LISTA = 40
# Sin filtro, un informe entero entrega cientos de frases y lo primero que sale es la portada y la
# descripción del negocio. Pasó en la prueba de campo del 27 de noviembre de 2026 (482 frases en
# Sanmina). Por eso, si no se pide otra cosa, se muestran solo las frases que traen uno de estos
# trozos de palabra, en inglés y en español.
TERMINOS_CONTABLES = (
    "recogni", "revenue", "receivable", "allowance", "reserve", "accrual", "accrued", "estimate",
    "useful li", "capitaliz", "deferred", "recourse", "factoring", "securitiz", "impairment",
    "write-down", "written down", "restructuring", "inventor", "payable", "payment terms",
    "related part", "reclassif", "restate", "material weakness", "change in accounting",
    "days sales", "non-gaap", "contingent consideration", "pension", "discount rate", "warrant",
    "consignment", "bill-and-hold", "percentage-of-completion", "hedg", "off-balance",
    "recorded", "netted", "expensed", "amortiz", "depreciat", "classified", "incentive", "rebate",
    "returns", "fair value", "accounting", "income statement", "balance sheet", "cash flow",
    "se registra", "contabiliz", "depreciaci", "clasific", "descuento", "devoluci", "valor razonable",
    "contable", "estado de resultados", "flujo de efectivo",
    "se reconoce", "reconocimiento", "ingresos ordinarios", "por cobrar", "deudores comerciales",
    "provisi", "deterioro", "estimaci", "vida útil", "vidas útiles", "activad", "diferid",
    "securitiza", "cesión", "reestructuraci", "inventario", "por pagar", "confirming", "relacionad",
    "reclasific", "reexpres", "política contable", "cambio contable", "contraprestación contingente",
    "tasa de descuento", "garantía", "consignación", "grado de avance", "cobertura", "fuera de balance",
)
CORTE_DE_FRASE = re.compile(r"(?<=[.;:!?])\s+(?=[A-ZÁÉÍÓÚÑ«\"“(\[])")
ESPACIO_EN_NUMERO = re.compile(r"(?<=#) (?=#)")


def leer(ruta):
    if ruta.suffix.lower() == ".pdf":
        try:
            import pymupdf
        except ImportError:
            print("Para leer un PDF corre el script con: uv run --with pymupdf python -I ...", file=sys.stderr)
            sys.exit(2)
        with pymupdf.open(ruta) as doc:
            texto = " ".join(pagina.get_text() for pagina in doc)
    else:
        texto = ruta.read_bytes().decode("utf-8-sig", errors="replace")
        if ruta.suffix.lower() in (".html", ".htm", ".xml"):
            texto = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", texto)
            texto = re.sub(r"<[^>]+>", " ", texto)
    return " ".join(html.unescape(texto).split())


def frases(texto):
    return [f.strip() for f in CORTE_DE_FRASE.split(texto) if len(f.strip()) >= LARGO_MINIMO_DE_FRASE]


def clave(frase):
    sin_cifras = re.sub(r"\d[\d.,/]*", "#", frase.casefold())
    return ESPACIO_EN_NUMERO.sub("", " ".join(re.sub(r"[^\w#]+", " ", sin_cifras).split()))


def palabras_que_identifican(frase):
    return {p for p in clave(frase).split() if len(p) >= LARGO_MINIMO_DE_PALABRA_QUE_IDENTIFICA}


def sin_tipografia(palabra):
    return palabra.replace(chr(0x2019), "'").replace(chr(0x2018), "'").replace(chr(0x201C), '"').replace(chr(0x201D), '"')


def marcar(antes, ahora):
    a, b = antes.split(), ahora.split()
    partes = []
    iguales = difflib.SequenceMatcher(None, [sin_tipografia(p) for p in a], [sin_tipografia(p) for p in b], autojunk=False)
    for op, i1, i2, j1, j2 in iguales.get_opcodes():
        if op == "equal":
            partes.append(" ".join(b[j1:j2]))
        if op in ("delete", "replace"):
            partes.append("[- " + " ".join(a[i1:i2]) + " -]")
        if op in ("insert", "replace"):
            partes.append("[+ " + " ".join(b[j1:j2]) + " +]")
    return " ".join(partes)


def comparar(texto_antes, texto_ahora):
    antes, ahora = frases(texto_antes), frases(texto_ahora)
    claves_antes, claves_ahora = {clave(f) for f in antes}, {clave(f) for f in ahora}
    solo_antes = [f for f in dict.fromkeys(antes) if clave(f) not in claves_ahora]
    solo_ahora = [f for f in dict.fromkeys(ahora) if clave(f) not in claves_antes]

    indice = {}
    for n, frase in enumerate(solo_antes):
        for palabra in palabras_que_identifican(frase):
            indice.setdefault(palabra, []).append(n)

    cambiadas, nuevas, usadas = [], [], set()
    for frase in solo_ahora:
        votos = Counter()
        for palabra in palabras_que_identifican(frase):
            for n in indice.get(palabra, ()):
                if n not in usadas:
                    votos[n] += 1
        mejor, parecido = None, 0.0
        for n, _ in votos.most_common(CANDIDATAS_POR_FRASE):
            r = difflib.SequenceMatcher(None, clave(solo_antes[n]).split(), clave(frase).split(), autojunk=False).ratio()
            if r > parecido:
                mejor, parecido = n, r
        if mejor is not None and parecido >= PARECIDO_MINIMO_PARA_SER_LA_MISMA_FRASE:
            usadas.add(mejor)
            cambiadas.append((solo_antes[mejor], frase))
        else:
            nuevas.append(frase)
    desaparecidas = [f for n, f in enumerate(solo_antes) if n not in usadas]
    return cambiadas, nuevas, desaparecidas


def main(argv):
    for flujo in (sys.stdout, sys.stderr):
        flujo.reconfigure(encoding="utf-8", errors="replace")
    rutas, terminos, maximo, todo, i = [], [], MAXIMO_POR_LISTA, False, 1
    while i < len(argv):
        if argv[i] == "--contiene" and i + 1 < len(argv):
            terminos.append(argv[i + 1].casefold())
            i += 2
        elif argv[i] == "--max" and i + 1 < len(argv) and argv[i + 1].isdigit():
            maximo = int(argv[i + 1])
            i += 2
        elif argv[i] == "--todo":
            todo = True
            i += 1
        elif argv[i].startswith("--"):
            print(f"No entiendo «{argv[i]}». Usa --contiene, --todo o --max.", file=sys.stderr)
            return 2
        else:
            rutas.append(Path(argv[i]))
            i += 1
    if len(rutas) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    for ruta in rutas:
        if not ruta.is_file():
            print(f"No existe {ruta}. Baja primero los 2 informes al disco.", file=sys.stderr)
            return 2
    textos = [leer(r) for r in rutas]
    for ruta, texto in zip(rutas, textos):
        if not texto:
            print(f"{ruta} no tiene texto. Un PDF escaneado necesita OCR antes de comparar.", file=sys.stderr)
            return 2

    cambiadas, nuevas, desaparecidas = comparar(*textos)
    print(f"Comparé {rutas[0].name} (anterior) con {rutas[1].name} (actual).")
    print(f"Cambiaron {len(cambiadas)} frases, hay {len(nuevas)} nuevas y desaparecieron {len(desaparecidas)}.")
    if not (cambiadas or nuevas or desaparecidas):
        print("Sin cambios de redacción fuera de cifras y fechas.")
        return 0

    filtro = terminos or (None if todo else TERMINOS_CONTABLES)

    def trae(frase):
        return filtro is None or any(t in frase.casefold() for t in filtro)

    listas = (
        ("CAMBIÓ", [marcar(a, b) for a, b in cambiadas if trae(a) or trae(b)], len(cambiadas)),
        ("NUEVA", [f for f in nuevas if trae(f)], len(nuevas)),
        ("DESAPARECIÓ", [f for f in desaparecidas if trae(f)], len(desaparecidas)),
    )
    if terminos:
        print("Muestro solo las frases que traen: " + ", ".join(terminos) + ".")
    elif not todo:
        print("Muestro solo las frases que tocan temas contables (ingresos, provisiones, estimaciones,")
        print("cuentas por cobrar, inventario, reservas, reclasificaciones). Con --todo se ven todas.")
    for titulo, lista, total in listas:
        if not total:
            continue
        resto = total - len(lista)
        aparte = f", y otras {resto} que no se muestran" if resto else ""
        print(f"\n{titulo} ({len(lista)}{aparte})")
        for frase in lista[:maximo]:
            print(f"- {frase}")
        if len(lista) > maximo:
            print(f"  y {len(lista) - maximo} más. Acota con --contiene o sube --max.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
