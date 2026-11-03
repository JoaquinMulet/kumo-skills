# -*- coding: utf-8 -*-
"""
Verifica que el curso NO tenga referencias hacia adelante.

Lee un CONTRATO DE VOCABULARIO (termino -> capitulo donde se introduce) y
comprueba, para cada termino, que su PRIMERA aparicion en el HTML caiga en ese
capitulo o despues. Si aparece antes, es deuda: el lector lo lee sin tenerlo.

Existe porque el defecto estructural del curso v3 era exactamente ese, medido en
22 lecciones-concepto de deuda acumulada, y no habia forma de detectarlo salvo
que un lector se trabara.

    uv run python verificar_vocabulario.py
"""
import io, re, sys, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

AQUI = os.path.dirname(os.path.abspath(__file__))
from objetivo import objetivo
CURSO = objetivo()
CONTRATO = os.path.join(AQUI, 'contrato_vocabulario.json')


def mapa_secciones(t):
    """offset -> id de seccion, incluyendo el <script> final."""
    sec = [(m.start(), m.group(1))
           for m in re.finditer(r'<section id="([a-z0-9-]+)"', t)]
    js = t.find('<script>')
    if js > 0:
        sec.append((js, 'JS'))
    sec.sort()
    return sec


EXENTAS = ('indice',)

def neutraliza_navegacion(t):
    """Reemplaza por espacios el encabezado y las secciones exentas, para que
    su texto no cuente como primera aparicion de un termino."""
    fin_hero = t.find('<section id=')
    if fin_hero > 0:
        t = ' ' * fin_hero + t[fin_hero:]
    for sid in EXENTAS:
        i = t.find('<section id="%s"' % sid)
        if i < 0:
            continue
        j = t.find('</section>', i)
        # se conserva la etiqueta de apertura para no mover los offsets de seccion
        k = t.find('>', i) + 1
        t = t[:k] + ' ' * (j - k) + t[j:]
    return t


def seccion_de(sec, off):
    nom = '(antes de toda seccion)'
    for o, s in sec:
        if o <= off:
            nom = s
        else:
            break
    return nom


def indice_de(sec_ids, nom):
    """Posicion ordinal de una seccion en el documento."""
    try:
        return sec_ids.index(nom)
    except ValueError:
        return -1


def main():
    if not os.path.exists(CONTRATO):
        print('No existe %s' % CONTRATO)
        print('Debe contener {"termino": {"patron": "regex", "capitulo": "l4"}, ...}')
        sys.exit(2)

    t = open(CURSO, encoding='utf-8').read()
    # El indice y el encabezado son NAVEGACION, no exposicion: nombrar un
    # capitulo por su titulo no es usar el concepto antes de explicarlo.
    # El contrato lo declaraba en su comentario, pero el verificador nunca lo
    # implemento — y por eso reportaba deuda donde no la hay.
    t = neutraliza_navegacion(t)
    contrato = json.load(open(CONTRATO, encoding='utf-8'))
    sec = mapa_secciones(t)
    sec_ids = [s for _, s in sec]

    print('%-26s %-22s %-12s %s' % ('TERMINO', '1a APARICION', 'CONTRATO', 'VEREDICTO'))
    print('-' * 84)
    deuda, sin_uso = [], []
    for termino, spec in contrato.items():
        if termino.startswith('_'):    # claves de metadatos, no terminos
            continue
        pat = spec.get('patron') or re.escape(termino)
        cap = spec['capitulo']
        m = re.search(pat, t)
        if not m:
            sin_uso.append(termino)
            print('%-26s %-22s %-12s %s' % (termino, '(no aparece)', cap, 'revisar: se perdio?'))
            continue
        donde = seccion_de(sec, m.start())
        i_real, i_contrato = indice_de(sec_ids, donde), indice_de(sec_ids, cap)
        if i_real < i_contrato:
            deuda.append((termino, donde, cap, i_contrato - i_real))
            ver = 'DEUDA de %d secciones' % (i_contrato - i_real)
        else:
            ver = 'ok'
        print('%-26s %-22s %-12s %s' % (termino, donde, cap, ver))

    print()
    print('=' * 84)
    if deuda:
        print('REFERENCIAS HACIA ADELANTE: %d' % len(deuda))
        deuda.sort(key=lambda x: -x[3])
        for termino, donde, cap, d in deuda:
            print('  %2d  %-26s se usa en %-10s pero se introduce en %s' % (d, termino, donde, cap))
        print('\nDeuda total: %d secciones-concepto' % sum(d[3] for d in deuda))
        sys.exit(1)
    print('DEUDA CERO — ningun termino se usa antes de su capitulo (%d verificados).'
          % (len(contrato) - len(sin_uso)))
    if sin_uso:
        print('Ojo: %d terminos del contrato no aparecen en el curso: %s'
              % (len(sin_uso), ', '.join(sin_uso)))


if __name__ == '__main__':
    main()
