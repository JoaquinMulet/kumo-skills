"""Prueba los 3 scripts del paso forense contra cifras conocidas.

Qué espera. Nada. Arma sus archivos en una carpeta temporal y la borra al terminar.

Qué comprueba. Que `razones_forenses.py` reproduce las cifras de las tablas de Financial Shenanigans
(Trex 3-3, WorldCom 6-1, Tyco 16-2, Sunbeam 9-2, Linn 13-5), que `comparar_notas.py` encuentra el
cambio de la nota de ingresos de Keurig entre 2007 y 2008, y que `validar_forense.py` acepta un
anexo completo y rechaza cada hueco. Los valores esperados se leyeron de las tablas del libro el
27 de noviembre de 2026.

Sale con 0 si todo pasa y con 1 si algo falla.

Uso.
  uv run python -I scripts/probar_forense.py
"""

import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FALLAS = []


def correr(script, *args):
    r = subprocess.run(
        [sys.executable, "-I", "-X", "utf8", str(AQUI / script), *map(str, args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    return r.returncode, r.stdout + r.stderr


def comprobar(nombre, condicion, detalle=""):
    print(("  pasa   " if condicion else "  FALLA  ") + nombre)
    if not condicion:
        FALLAS.append(nombre)
        if detalle:
            print("         " + detalle[-900:].replace("\n", "\n         "))


def escribir(ruta, texto):
    ruta.write_bytes(texto.encode("utf-8"))
    return ruta


def probar_razones(tmp):
    print("razones_forenses.py")
    trex = escribir(
        tmp / "trex.csv",
        "concepto,T1 2003,T1 2004,T1 2005\n"
        "dias,91.25,91.25,91.25\n"
        "ingresos,68.7,76.3,89.9\n"
        "cuentas_por_cobrar,13.9,31.9,68.8\n",
    )
    codigo, salida = correr("razones_forenses.py", trex)
    comprobar("Trex. DSO de 18, 38 y 70 días", codigo == 0 and "| 18 | 38 | 70 |" in salida, salida)
    comprobar("Trex. Avisa que las cuentas por cobrar crecen más que los ingresos", "crecieron más que los ingresos" in salida, salida)
    comprobar("Trex. El aviso nombra EM 1", "EM 1" in salida, salida)

    worldcom = escribir(
        tmp / "worldcom.csv",
        "concepto,1999,2000\nflujo_operacional,11005,7666\ncapex,8716,11484\n",
    )
    codigo, salida = correr("razones_forenses.py", worldcom)
    comprobar("WorldCom. Flujo de caja libre de 2.289 y -3.818", "| 2.289 | -3.818 |" in salida, salida)

    tyco = escribir(
        tmp / "tyco.csv",
        "concepto,1999,2000,2001,2002\n"
        "flujo_operacional,3550,5275,6926,5696\n"
        "capex,1632,1815,4046,2855\n"
        "adquisiciones,5135,4791,11851,3709\n",
    )
    codigo, salida = correr("razones_forenses.py", tyco)
    comprobar("Tyco. Flujo libre tras adquisiciones de -3.217, -1.331, -8.971 y -868", "| -3.217 | -1.331 | -8.971 | -868 |" in salida, salida)
    comprobar("Tyco. Avisa AA 2 por flujo operacional positivo y flujo tras adquisiciones negativo", "AA 2" in salida, salida)

    sunbeam = escribir(
        tmp / "sunbeam.csv",
        "concepto,9M 1996,9M 1997\n"
        "ingresos,715.4,830.1\n"
        "utilidad_operacional,4.0,132.6\n"
        "cuentas_por_cobrar,194.6,309.1\n"
        "flujo_operacional,-18.8,-60.8\n",
    )
    codigo, salida = correr("razones_forenses.py", sunbeam)
    comprobar("Sunbeam. Cuentas por cobrar suben 59 por ciento contra 16 de los ingresos", "59" in salida and "16" in salida, salida)
    comprobar("Sunbeam. Avisa que la utilidad operacional crece más que los ingresos", "utilidad operacional creció más que los ingresos" in salida, salida)

    linn = escribir(
        tmp / "linn.csv",
        "concepto,2011,2012\n"
        "flujo_operacional,518710,350907\n"
        "capex,629864,1045079\n"
        "dividendos,590224,679275\n",
    )
    codigo, salida = correr("razones_forenses.py", linn)
    comprobar("Linn. Flujo de caja libre de -111.154 y -694.172", "| -111.154 | -694.172 |" in salida, salida)
    comprobar("Linn. Avisa KM 1 porque los dividendos superan al flujo de caja libre", "KM 1" in salida, salida)

    scholastic = escribir(
        tmp / "scholastic.csv",
        "concepto,2001,2002\ncuentas_por_cobrar,75.9,83.58\nprovision_incobrables,24.1,21.42\n",
    )
    codigo, salida = correr("razones_forenses.py", scholastic)
    comprobar("Provisión sobre cuentas por cobrar brutas de 24,1 y 20,4 por ciento", "| 24,1 | 20,4 |" in salida, salida)
    comprobar("Avisa EM 4 cuando la provisión baja y las cuentas por cobrar suben", "EM 4" in salida, salida)

    limpio = escribir(
        tmp / "limpio.csv",
        "concepto,2019,2020\n"
        "ingresos,100,110\nutilidad_neta,10,11\nflujo_operacional,12,13.2\ncapex,3,3.3\n"
        "cuentas_por_cobrar,20,22\ncosto_ventas,60,66\ninventario,15,16.5\ncuentas_por_pagar,10,11\n",
    )
    codigo, salida = correr("razones_forenses.py", limpio)
    comprobar("Una empresa que crece pareja no produce avisos", codigo == 0 and "Sin avisos" in salida, salida)

    codigo, salida = correr("razones_forenses.py", tmp / "no-existe.csv")
    comprobar("Un archivo que no existe sale con 2", codigo == 2, salida)
    malo = escribir(tmp / "malo.csv", "concepto,2019,2020\ningresos,cien,110\n")
    codigo, salida = correr("razones_forenses.py", malo)
    comprobar("Una cifra que no es número sale con 2 y dice cuál", codigo == 2 and "cien" in salida, salida)
    raro = escribir(tmp / "raro.csv", "concepto,2019,2020\ningresos,100,110\nventas_netas,100,110\n")
    codigo, salida = correr("razones_forenses.py", raro)
    comprobar("Un concepto desconocido se avisa por su nombre", "ventas_netas" in salida, salida)


NOTA_2007 = (
    "Revenue from wholesale and consumer direct sales is recognized upon product delivery. "
    "In addition, the Company's customers can earn certain incentives, which are netted against sales "
    "in the consolidated income statements. "
    "The Company had 1,220 employees at September 29, 2007 and operates in two segments. "
    "Inventories are stated at the lower of cost or market, with cost determined by the first-in first-out method. "
)
NOTA_2008 = (
    "Revenue from wholesale and consumer direct sales is recognized upon product delivery, and in some "
    "cases upon product shipment. "
    "In addition, the Company's customers can earn certain incentives, which are netted against sales "
    "or recorded in operating and selling expenses in the consolidated income statements. "
    "The Company had 1,490 employees at September 27, 2008 and operates in two segments. "
    "Inventories are stated at the lower of cost or market, with cost determined by the first-in first-out method. "
    "The Company may at times market certain client receivable balances without recourse. "
)


def probar_notas(tmp):
    print("comparar_notas.py")
    antes = escribir(tmp / "nota-2007.txt", NOTA_2007)
    ahora = escribir(tmp / "nota-2008.txt", NOTA_2008)
    codigo, salida = correr("comparar_notas.py", antes, ahora)
    comprobar("Keurig. Marca como agregado «in some cases upon product shipment»", codigo == 0 and "in some cases upon product shipment" in salida, salida)
    comprobar("Keurig. Marca como agregado «or recorded in operating and selling expenses»", "or recorded in operating and selling expenses" in salida, salida)
    comprobar("Una frase que solo cambió sus cifras no se reporta", "employees" not in salida, salida)
    comprobar("Una frase idéntica no se reporta", "first-in first-out" not in salida, salida)
    comprobar("Una frase nueva sin pareja se lista como nueva", "NUEVA" in salida and "without recourse" in salida, salida)
    codigo, salida = correr("comparar_notas.py", antes, ahora, "--contiene", "recourse")
    comprobar("Con --contiene solo quedan las frases con ese término", "without recourse" in salida and "product shipment" not in salida, salida)
    codigo, salida = correr("comparar_notas.py", antes, antes)
    comprobar("2 archivos iguales no reportan cambios", codigo == 0 and "Sin cambios" in salida, salida)
    codigo, salida = correr("comparar_notas.py", antes, tmp / "no-existe.txt")
    comprobar("Un archivo que no existe sale con 2", codigo == 2, salida)


CODIGOS = ["EM 1", "EM 2", "EM 3", "EM 4", "EM 5", "EM 6", "EM 7", "CF 1", "CF 2", "CF 3", "KM 1", "KM 2", "AA 1", "AA 2", "AA 3"]


def seccion(codigo, veredicto="LIMPIO", extra=""):
    return (
        f"## {codigo}. Prueba\n\n| Campo | Contenido |\n|---|---|\n| Veredicto | {veredicto} |\n"
        "| Qué se revisó | DSO de 41, 42 y 40 días en 3 años y la nota 2 comparada con la del año anterior |\n"
        f"{extra}\n"
    )


def anexo(cambios=None, omitir=()):
    cambios = cambios or {}
    return "# Anexo forense\n\n" + "".join(cambios.get(c, seccion(c)) for c in CODIGOS if c not in omitir)


def probar_validador(tmp):
    print("validar_forense.py")
    escribir(tmp / "fuente.txt", NOTA_2008)
    codigo, salida = correr("validar_forense.py", escribir(tmp / "limpio.md", anexo()))
    comprobar("Un anexo con las 15 pruebas limpias queda verde con 0 puntos", codigo == 0 and "0 puntos" in salida, salida)

    codigo, salida = correr("validar_forense.py", escribir(tmp / "falta.md", anexo(omitir=("AA 3",))))
    comprobar("Si falta AA 3 queda rojo y la nombra", codigo == 1 and "AA 3" in salida, salida)

    sin_cita = {"EM 1": seccion("EM 1", "ALTA", "| Efecto | Adelanta ingresos |")}
    codigo, salida = correr("validar_forense.py", escribir(tmp / "sin-cita.md", anexo(sin_cita)))
    comprobar("Un hallazgo sin cita queda rojo", codigo == 1 and "EM 1" in salida and "cita" in salida.lower(), salida)

    falsa = {"EM 1": seccion("EM 1", "ALTA", "| Efecto | Adelanta ingresos |\n| Cita | «recognized upon signing of the contract» en fuente.txt |")}
    codigo, salida = correr("validar_forense.py", escribir(tmp / "cita-falsa.md", anexo(falsa)))
    comprobar("Una cita que no está en la fuente queda rojo", codigo == 1 and "no aparece" in salida, salida)

    buena = {
        "EM 1": seccion("EM 1", "ALTA", "| Efecto | Adelanta ingresos |\n| Cita | «and in some cases upon product shipment» en fuente.txt |"),
        "CF 1": seccion("CF 1", "BAJA", "| Efecto | Menor |\n| Cita | «market certain client receivable balances without recourse» en fuente.txt |"),
    }
    codigo, salida = correr("validar_forense.py", escribir(tmp / "bueno.md", anexo(buena)))
    comprobar("Con las citas presentes queda verde", codigo == 0, salida)
    comprobar("ALTA más BAJA suman 4 puntos", "4 puntos" in salida, salida)

    sin_efecto = {"EM 1": seccion("EM 1", "MEDIA", "| Cita | «and in some cases upon product shipment» en fuente.txt |")}
    codigo, salida = correr("validar_forense.py", escribir(tmp / "sin-efecto.md", anexo(sin_efecto)))
    comprobar("Un hallazgo sin la fila Efecto queda rojo", codigo == 1 and "Efecto" in salida, salida)

    critica = {"EM 2": seccion("EM 2", "CRÍTICA", "| Efecto | Ingresos sin sustancia |\n| Cita | «without recourse» en fuente.txt |")}
    codigo, salida = correr("validar_forense.py", escribir(tmp / "critica.md", anexo(critica)))
    comprobar("Un hallazgo crítico se anuncia aparte del puntaje", codigo == 0 and "crítico" in salida.lower(), salida)

    sin_dato = {"KM 2": "## KM 2. Prueba\n\n| Campo | Contenido |\n|---|---|\n| Veredicto | SIN DATO |\n| Qué falta | La nota de provisiones de 2015 |\n\n"}
    codigo, salida = correr("validar_forense.py", escribir(tmp / "sin-dato.md", anexo(sin_dato)))
    comprobar("SIN DATO con lo que falta queda verde y se cuenta aparte", codigo == 0 and "1 sin dato" in salida.lower(), salida)

    inventado = {"EM 3": seccion("EM 3", "GRAVE")}
    codigo, salida = correr("validar_forense.py", escribir(tmp / "inventado.md", anexo(inventado)))
    comprobar("Un veredicto que no existe queda rojo", codigo == 1 and "GRAVE" in salida, salida)

    vacio = {"EM 4": "## EM 4. Prueba\n\n| Campo | Contenido |\n|---|---|\n| Veredicto | LIMPIO |\n| Qué se revisó | Todo bien |\n\n"}
    codigo, salida = correr("validar_forense.py", escribir(tmp / "vacio.md", anexo(vacio)))
    comprobar("Un LIMPIO que no dice qué cifra o nota miró queda rojo", codigo == 1 and "EM 4" in salida, salida)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    with tempfile.TemporaryDirectory() as carpeta:
        tmp = Path(carpeta)
        probar_razones(tmp)
        probar_notas(tmp)
        probar_validador(tmp)
    if FALLAS:
        print(f"\nROJO. Fallaron {len(FALLAS)} comprobaciones.")
        return 1
    print("\nVERDE. Los 3 scripts del paso forense se comportan como dice su cabecera.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
