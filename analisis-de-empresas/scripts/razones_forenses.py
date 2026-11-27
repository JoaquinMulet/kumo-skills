"""Calcula las razones de la revisión forense y avisa qué pruebas mirar primero.

Qué espera. Un CSV con una fila por concepto y una columna por período, del más antiguo al más
nuevo. La primera columna se llama `concepto`. Las cifras van con punto decimal y sin separador de
miles, todas en la misma unidad. Los períodos tienen que ser comparables entre sí (años completos,
o el mismo trimestre de cada año, porque comparar un trimestre con el anterior mezcla la temporada).

Conceptos que entiende. Solo se calculan las razones cuyos conceptos están. Si la empresa no tiene
un concepto, la fila no va o la celda queda vacía. No se pone 0.
  dias                          días del período, 365 si falta (91.25 en un trimestre)
  ingresos, costo_ventas, utilidad_operacional, utilidad_neta
  utilidad_antes_impuestos, impuestos   el gasto por impuestos, en positivo
  flujo_operacional, capex, adquisiciones
  dividendos                    solo los pagados en efectivo
  cuentas_por_cobrar            saldo del balance, neto de provisión
  cuentas_por_cobrar_vendidas   vendidas o cedidas que siguen pendientes al cierre
  documentos_por_cobrar         pagarés y letras recibidos de clientes
  provision_incobrables         en positivo
  inventario, inventario_largo_plazo, cuentas_por_pagar
  ingreso_diferido, pasivos_blandos, activos_blandos
  cartera_morosa, provision_cartera, cartera_repactada

Qué devuelve. Una tabla con las razones por período y una lista de avisos. Un aviso compara 2
períodos seguidos y nombra las pruebas del paso forense que hay que abrir. No usa umbrales. Dice la
dirección y el tamaño del cambio, y el juicio queda para quien lee la nota. Un aviso no es un
hallazgo. Sale con 0 si pudo calcular y con 2 si el archivo o una cifra están mal.

Uso.
  uv run python -I scripts/razones_forenses.py analisis/cifras.csv
"""

import csv
import sys
from pathlib import Path

DIAS_DE_UN_ANO = 365.0
CONCEPTOS = {
    "dias", "ingresos", "costo_ventas", "utilidad_operacional", "utilidad_neta",
    "utilidad_antes_impuestos", "impuestos",
    "flujo_operacional", "capex", "adquisiciones", "dividendos",
    "cuentas_por_cobrar", "cuentas_por_cobrar_vendidas", "documentos_por_cobrar",
    "provision_incobrables", "inventario", "inventario_largo_plazo", "cuentas_por_pagar",
    "ingreso_diferido", "pasivos_blandos", "activos_blandos", "cartera_morosa", "provision_cartera",
    "cartera_repactada",
}


def numero(valor, decimales=0):
    if valor is None:
        return ""
    texto = f"{valor:,.{decimales}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def leer(ruta):
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        filas = [f for f in csv.reader(archivo) if f and any(c.strip() for c in f)]
    if len(filas) < 2 or len(filas[0]) < 2:
        raise ValueError("El CSV necesita una fila de encabezado con los períodos y al menos un concepto.")
    periodos = [p.strip() for p in filas[0][1:]]
    datos, desconocidos = {}, []
    for fila in filas[1:]:
        concepto = fila[0].strip().lower()
        if concepto not in CONCEPTOS:
            desconocidos.append(concepto)
            continue
        valores = []
        for periodo, celda in zip(periodos, fila[1:] + [""] * len(periodos)):
            celda = celda.strip()
            if not celda:
                valores.append(None)
                continue
            try:
                valores.append(float(celda))
            except ValueError:
                raise ValueError(
                    f"En «{concepto}», período {periodo}, «{celda}» no es un número. "
                    "Usa punto decimal y ningún separador de miles."
                )
        datos[concepto] = valores
    return periodos, datos, desconocidos


def serie(datos, n, calculo, *conceptos):
    if any(c not in datos for c in conceptos):
        return None
    salida = []
    for i in range(n):
        valores = [datos[c][i] for c in conceptos]
        try:
            salida.append(None if any(v is None for v in valores) else calculo(i, *valores))
        except ZeroDivisionError:
            salida.append(None)
    return salida


def suma_opcional(datos, i, *conceptos):
    return sum(datos[c][i] or 0 for c in conceptos if c in datos)


def calcular(periodos, datos):
    n = len(periodos)
    dias = [d if d else DIAS_DE_UN_ANO for d in datos.get("dias", [None] * n)]
    razones = {}

    def poner(nombre, decimales, valores):
        if valores is not None:
            razones[nombre] = (decimales, valores)

    poner("DSO, días de venta por cobrar", 0, serie(datos, n, lambda i, c, v: c / v * dias[i], "cuentas_por_cobrar", "ingresos"))
    if "cuentas_por_cobrar_vendidas" in datos or "documentos_por_cobrar" in datos:
        poner(
            "DSO ajustado, con vendidas y documentos", 0,
            serie(datos, n, lambda i, c, v: (c + suma_opcional(datos, i, "cuentas_por_cobrar_vendidas", "documentos_por_cobrar")) / v * dias[i], "cuentas_por_cobrar", "ingresos"),
        )
    poner("DSI, días de inventario", 0, serie(datos, n, lambda i, inv, c: (inv + suma_opcional(datos, i, "inventario_largo_plazo")) / c * dias[i], "inventario", "costo_ventas"))
    poner("DPO, días de cuentas por pagar", 0, serie(datos, n, lambda i, p, c: p / c * dias[i], "cuentas_por_pagar", "costo_ventas"))
    poner("Flujo operacional menos utilidad neta", 0, serie(datos, n, lambda i, f, u: f - u, "flujo_operacional", "utilidad_neta"))
    poner("Flujo de caja libre", 0, serie(datos, n, lambda i, f, c: f - c, "flujo_operacional", "capex"))
    poner("Flujo de caja libre tras adquisiciones", 0, serie(datos, n, lambda i, f, c, a: f - c - a, "flujo_operacional", "capex", "adquisiciones"))
    poner("Margen neto, por ciento", 1, serie(datos, n, lambda i, u, v: u / v * 100, "utilidad_neta", "ingresos"))
    poner("Tasa efectiva de impuestos, por ciento", 1, serie(datos, n, lambda i, t, a: t / a * 100, "impuestos", "utilidad_antes_impuestos"))
    poner("Capex sobre ingresos, por ciento", 1, serie(datos, n, lambda i, c, v: c / v * 100, "capex", "ingresos"))
    poner("Provisión sobre cuentas por cobrar brutas, por ciento", 1, serie(datos, n, lambda i, p, c: p / (c + p) * 100, "provision_incobrables", "cuentas_por_cobrar"))
    poner("Provisión de cartera sobre cartera morosa, por ciento", 1, serie(datos, n, lambda i, p, m: p / m * 100, "provision_cartera", "cartera_morosa"))
    poner("Cartera morosa sobre cuentas por cobrar, por ciento", 1, serie(datos, n, lambda i, m, c: m / c * 100, "cartera_morosa", "cuentas_por_cobrar"))
    poner("Cartera repactada sobre cuentas por cobrar, por ciento", 1, serie(datos, n, lambda i, r, c: r / c * 100, "cartera_repactada", "cuentas_por_cobrar"))
    poner("Ingreso diferido sobre ingresos, por ciento", 1, serie(datos, n, lambda i, d, v: d / v * 100, "ingreso_diferido", "ingresos"))
    poner("Pasivos blandos sobre ingresos, por ciento", 1, serie(datos, n, lambda i, p, v: p / v * 100, "pasivos_blandos", "ingresos"))
    poner("Activos blandos sobre ingresos, por ciento", 1, serie(datos, n, lambda i, a, v: a / v * 100, "activos_blandos", "ingresos"))
    return razones


def variacion(datos, concepto, i):
    if concepto not in datos:
        return None
    antes, ahora = datos[concepto][i - 1], datos[concepto][i]
    if antes is None or ahora is None or antes <= 0:
        return None
    return (ahora / antes - 1) * 100


def avisar(periodos, datos, razones):
    avisos = []

    def valor(nombre, i):
        return razones[nombre][1][i] if nombre in razones else None

    def par(nombre, i):
        a, b = valor(nombre, i - 1), valor(nombre, i)
        return (a, b) if a is not None and b is not None else None

    def dato(concepto, i):
        return datos[concepto][i] if concepto in datos else None

    for i in range(1, len(periodos)):
        tramo = f"{periodos[i]} contra {periodos[i - 1]}"

        def poner(texto, pruebas):
            avisos.append(f"{tramo}. {texto} Mirar {pruebas}.")

        v_ing = variacion(datos, "ingresos", i)
        v_cxc = variacion(datos, "cuentas_por_cobrar", i)
        v_inv = variacion(datos, "inventario", i)
        v_op = variacion(datos, "utilidad_operacional", i)
        v_blandos = variacion(datos, "activos_blandos", i)

        if v_cxc is not None and v_ing is not None and v_cxc > v_ing and round(v_cxc) > round(v_ing):
            poner(f"Las cuentas por cobrar crecieron más que los ingresos ({numero(v_cxc)} contra {numero(v_ing)} por ciento).", "EM 1 y EM 2")
        dso = par("DSO ajustado, con vendidas y documentos", i) or par("DSO, días de venta por cobrar", i)
        if dso and i >= 2:
            previo = valor("DSO, días de venta por cobrar", i - 2)
            anterior = valor("DSO, días de venta por cobrar", i - 1)
            actual = valor("DSO, días de venta por cobrar", i)
            if None not in (previo, anterior, actual) and round(anterior) > round(previo) and round(actual) < round(anterior):
                poner(f"El DSO bajó de {numero(anterior)} a {numero(actual)} días después de haber subido.", "KM 2 y CF 1")
        dsi = par("DSI, días de inventario", i)
        if dsi and round(dsi[1]) > round(dsi[0]):
            poner(f"El DSI subió de {numero(dsi[0])} a {numero(dsi[1])} días.", "EM 4")
        dpo = par("DPO, días de cuentas por pagar", i)
        if dpo and round(dpo[1]) > round(dpo[0]):
            poner(f"El DPO subió de {numero(dpo[0])} a {numero(dpo[1])} días.", "CF 3")
        if v_op is not None and v_ing is not None and round(v_op) > round(v_ing):
            poner(f"La utilidad operacional creció más que los ingresos ({numero(v_op)} contra {numero(v_ing)} por ciento).", "EM 3, EM 4 y EM 5")

        v_neta = variacion(datos, "utilidad_neta", i)
        v_antes = variacion(datos, "utilidad_antes_impuestos", i)
        tasa = par("Tasa efectiva de impuestos, por ciento", i)
        if v_neta is not None and v_antes is not None and round(v_neta) > round(v_antes) and tasa and round(tasa[1], 1) < round(tasa[0], 1):
            poner(
                f"La utilidad neta creció más que la utilidad antes de impuestos ({numero(v_neta)} contra {numero(v_antes)} por ciento), "
                f"con una tasa de impuestos que bajó de {numero(tasa[0], 1)} a {numero(tasa[1], 1)} por ciento.",
                "EM 3",
            )

        u0, u1 = dato("utilidad_neta", i - 1), dato("utilidad_neta", i)
        f0, f1 = dato("flujo_operacional", i - 1), dato("flujo_operacional", i)
        if None not in (u0, u1, f0, f1):
            if u1 > u0 and f1 < f0:
                poner("La utilidad neta subió y el flujo operacional bajó.", "EM 1 a EM 5")
            if u1 < u0 and f1 > f0:
                poner("La utilidad neta bajó y el flujo operacional subió.", "CF 1, CF 2 y CF 3")
        libre = par("Flujo de caja libre", i)
        if libre and f0 is not None and f1 is not None and f1 > f0 and libre[1] < libre[0]:
            poner("El flujo operacional subió y el flujo de caja libre bajó.", "EM 4 y CF 2")
        margen = par("Margen neto, por ciento", i)
        if margen and v_ing is not None and v_ing > 0 and round(margen[1], 1) < round(margen[0], 1):
            poner(f"Los ingresos crecieron {numero(v_ing)} por ciento y el margen neto bajó de {numero(margen[0], 1)} a {numero(margen[1], 1)} por ciento.", "EM 2")
        provision = par("Provisión sobre cuentas por cobrar brutas, por ciento", i)
        if provision and v_cxc is not None and v_cxc > 0 and round(provision[1], 1) < round(provision[0], 1):
            poner(f"Las cuentas por cobrar subieron y su provisión bajó de {numero(provision[0], 1)} a {numero(provision[1], 1)} por ciento.", "EM 4")
        cartera = par("Provisión de cartera sobre cartera morosa, por ciento", i)
        if cartera and round(cartera[1], 1) < round(cartera[0], 1):
            poner(f"La provisión de cartera bajó de {numero(cartera[0], 1)} a {numero(cartera[1], 1)} por ciento de la cartera morosa.", "EM 4 y KM 2")
        v_morosa = variacion(datos, "cartera_morosa", i)
        if v_morosa is not None and v_cxc is not None and v_morosa < 0 < v_cxc:
            poner(f"La cartera morosa bajó {numero(-v_morosa)} por ciento mientras las cuentas por cobrar subían {numero(v_cxc)}.", "EM 4 y KM 2")
        v_repactada = variacion(datos, "cartera_repactada", i)
        if v_repactada is not None and v_cxc is not None and round(v_repactada) > round(v_cxc):
            poner(f"La cartera repactada creció más que las cuentas por cobrar ({numero(v_repactada)} contra {numero(v_cxc)} por ciento).", "EM 4 y KM 2")
        blandos_pasivo = par("Pasivos blandos sobre ingresos, por ciento", i)
        if blandos_pasivo and round(blandos_pasivo[1], 1) < round(blandos_pasivo[0], 1):
            poner(f"Los pasivos blandos bajaron de {numero(blandos_pasivo[0], 1)} a {numero(blandos_pasivo[1], 1)} por ciento de los ingresos.", "EM 5")
        diferido = par("Ingreso diferido sobre ingresos, por ciento", i)
        if diferido and round(diferido[1], 1) < round(diferido[0], 1):
            poner(f"El ingreso diferido bajó de {numero(diferido[0], 1)} a {numero(diferido[1], 1)} por ciento de los ingresos.", "EM 6")
        if v_blandos is not None and v_ing is not None and round(v_blandos) > round(v_ing):
            poner(f"Los activos blandos crecieron más que los ingresos ({numero(v_blandos)} contra {numero(v_ing)} por ciento).", "EM 4 y CF 2")
        capex = par("Capex sobre ingresos, por ciento", i)
        if capex and round(capex[1], 1) > round(capex[0], 1):
            poner(f"El capex subió de {numero(capex[0], 1)} a {numero(capex[1], 1)} por ciento de los ingresos.", "EM 4 y CF 2")
        if v_inv is not None and v_ing is not None and v_inv < 0 < v_ing:
            poner(f"El inventario bajó {numero(-v_inv)} por ciento mientras los ingresos subían.", "CF 3 y EM 7")

    for i in range(len(periodos)):
        libre_adq = valor("Flujo de caja libre tras adquisiciones", i)
        flujo = dato("flujo_operacional", i)
        compras = dato("adquisiciones", i)
        if libre_adq is not None and flujo is not None and compras and flujo > 0 and libre_adq < 0:
            avisos.append(f"{periodos[i]}. El flujo operacional es positivo y el flujo de caja libre tras adquisiciones es negativo. Mirar AA 2.")
        libre = valor("Flujo de caja libre", i)
        dividendos = dato("dividendos", i)
        if libre is not None and dividendos and dividendos > libre:
            avisos.append(f"{periodos[i]}. Los dividendos ({numero(dividendos)}) superan al flujo de caja libre ({numero(libre)}). Mirar KM 1.")
    return avisos


def main(argv):
    for flujo in (sys.stdout, sys.stderr):
        flujo.reconfigure(encoding="utf-8", errors="replace")
    if len(argv) != 2 or argv[1].startswith("--"):
        print(__doc__, file=sys.stderr)
        return 2
    ruta = Path(argv[1])
    if not ruta.is_file():
        print(f"No existe {ruta}. Arma primero el CSV de cifras del paso 3.", file=sys.stderr)
        return 2
    try:
        periodos, datos, desconocidos = leer(ruta)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    if desconocidos:
        print(
            "No conozco estos conceptos y los salté: " + ", ".join(desconocidos)
            + ". Los que entiendo están en la cabecera del script.",
            file=sys.stderr,
        )
    razones = calcular(periodos, datos)
    if not razones:
        print("Con estos conceptos no puedo calcular ninguna razón. Revisa la cabecera del script.", file=sys.stderr)
        return 2

    print(f"Razones forenses de {ruta.name}\n")
    print("| Razón | " + " | ".join(periodos) + " |")
    print("|---|" + "---|" * len(periodos))
    for nombre, (decimales, valores) in razones.items():
        print(f"| {nombre} | " + " | ".join(numero(v, decimales) for v in valores) + " |")
    avisos = avisar(periodos, datos, razones)
    print("\nAvisos")
    if not avisos:
        print("Sin avisos. Las 15 pruebas se corren igual, porque esta tabla no ve las notas.")
    for aviso in avisos:
        print("- " + aviso)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
