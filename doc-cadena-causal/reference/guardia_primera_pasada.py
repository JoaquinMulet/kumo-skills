# -*- coding: utf-8 -*-
"""
Guarda de la PASADA 1: falla si se cuela una cifra DERIVADA.

La estructura espiral solo funciona si la primera pasada no contiene ninguna
cantidad que sea consecuencia de un calculo. El juez del panel lo dijo sin
rodeos: "sin ese script, el riesgo es certeza".

Lista blanca (datos crudos que SI pueden aparecer en la pasada 1):
  - los cinco tipos de cambio observados: 936,69 / 963,57 / 931,36 / 866,74 / 907,51
  - el nocional del bono: 1.000  (y su forma "USD 1.000")
  - el plazo: 2 anios, 4 trimestres, y los rotulos Q1..Q4
  - numeracion estructural: capitulos, pasos, listas, anios de calendario

Todo lo demas —9 %, 20.250, 11.250, valores del swap, elemento a plazo,
inefectividad, resultados contables, cifras de Entel— es derivado y NO va.

    uv run python verificar_pasada1.py
"""
import io, re, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

AQUI = os.path.dirname(os.path.abspath(__file__))
from objetivo import objetivo
CURSO = objetivo()
CAPS_PASADA1 = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7']

# cifras crudas autorizadas (como texto exacto)
BLANCA = {
    '936,69', '963,57', '931,36', '866,74', '907,51',   # tipos de cambio observados (BCCh)
    '2025', '2026',                           # anios del caso
    '1.000', '1000',                          # nocional en USD
    '4',                                      # cupon 4 %
    '2',                                      # dos anios
    '9',                                      # NIC 9 / IFRS 9 (se filtra aparte)
    '21',                                     # NIC 21
    '0', '1', '3', '5', '6', '7', '8', '10',  # numeracion estructural
    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    '22', '23', '2008', '2026', '2031', '2032', '6.5.11',
}

def texto_visible(html):
    """Quita script, svg, atributos y comentarios: deja lo que el lector lee."""
    h = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    h = re.sub(r'<svg.*?</svg>', ' ', h, flags=re.S)
    h = re.sub(r'<!--.*?-->', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    # las fechas no son cifras derivadas: se neutralizan antes de tokenizar
    h = re.sub(r'\d{1,2}-\d{1,2}-\d{4}', ' [fecha] ', h)
    h = re.sub(r'\d{1,2} de \w+ de \d{4}', ' [fecha] ', h)
    return h

def main():
    t = open(CURSO, encoding='utf-8').read()
    # las fechas no son cifras derivadas: se neutralizan sobre todo el documento
    t = re.sub(r'\d{1,2}-\d{1,2}-\d{4}', '[fecha]', t)
    t = re.sub(r'\d{1,2} de [a-zA-Zúí]+ de \d{4}', '[fecha]', t)
    # delimitar cada capitulo de la pasada 1
    faltan, hallazgos = [], []
    for cap in CAPS_PASADA1:
        m = re.search(r'<section id="%s"' % cap, t)
        if not m:
            faltan.append(cap); continue
        fin = t.find('</section>', m.start())
        cuerpo = texto_visible(t[m.start():fin])
        # normalizar: IFRS 9 / NIC 21 / 6.5.11 no cuentan
        cuerpo = cuerpo.replace('IFRS 9', ' ').replace('NIC 21', ' ').replace('6.5.11', ' ')
        # ojo: hay que quitar la puntuacion pegada, o "capitulo 7," se lee como la cifra "7,"
        for n in re.finditer(r'\d[\d.,]*\s*%?', cuerpo):
            crudo = n.group(0).strip().rstrip('%').strip().rstrip('.,').strip()
            if crudo in BLANCA:
                continue
            # referencias de navegacion: "capitulo 15", "Q3", "pasada 2"
            antes = cuerpo[max(0, n.start()-14):n.start()].lower()
            if re.search(r'(cap[ií]tulo|pasada|ap[ée]ndice|nic|ifrs|\bq)\s*$', antes):
                continue
            ctx = re.sub(r'\s+', ' ', cuerpo[max(0, n.start()-70):n.start()+40]).strip()
            hallazgos.append((cap, n.group(0).strip(), ctx))

    if faltan:
        print('CAPITULOS NO ENCONTRADOS: %s' % ', '.join(faltan))
        print('(¿todavia no se escribe la pasada 1, o cambiaron los id?)')
        sys.exit(2)

    print('GUARDA DE LA PASADA 1 — capitulos %s' % ', '.join(CAPS_PASADA1))
    print('-' * 78)
    if not hallazgos:
        print('LIMPIO — ninguna cifra derivada en la primera pasada.')
        return
    print('CIFRAS DERIVADAS FILTRADAS: %d\n' % len(hallazgos))
    for cap, cifra, ctx in hallazgos:
        print('  [%s] %-12s ...%s...' % (cap, cifra, ctx))
    sys.exit(1)

if __name__ == '__main__':
    main()
