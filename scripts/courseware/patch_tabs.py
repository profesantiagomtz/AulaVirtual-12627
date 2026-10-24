"""Agrega al motor las tres pestañas Aprende / Diagnostica / Construye.

Se aplica una sola vez a las plantillas ya generadas (asin-ra12 y msii-ra12); el resto de los
materiales la heredan al construirse con build.py. Es idempotente.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
JS = (HERE / 'tabs_engine.js').read_text(encoding='utf8').strip()
CSS = (HERE / 'tabs_engine.css').read_text(encoding='utf8').strip()


def patch(path):
    html = path.read_text(encoding='utf8')
    if '/*TABS3*/' in html:
        print(f'{path.name}: ya tiene las pestañas')
        return
    old = 'go((ST.pos&&ST.pos[id])||0)}'
    if html.count(old) != 1:
        raise SystemExit(f'{path.name}: no se encontró el arranque de sec()')
    html = html.replace(old, 'go(SECI!=null&&ids.indexOf(SECI)>-1?ids.indexOf(SECI):((ST.pos&&ST.pos[id])||0))}')
    if html.count('\nhome();sv();\n') != 1:
        raise SystemExit(f'{path.name}: no se encontró el arranque del motor')
    html = html.replace('\nhome();sv();\n', '\n' + JS + '\nhome();sv();\n')
    html = html.replace('</style>', CSS + '</style>', 1)
    path.write_text(html, encoding='utf8')
    print(f'{path.name}: pestañas agregadas')


if __name__ == '__main__':
    for name in sys.argv[1:] or ['asin-ra12-material.html', 'msii-ra12-material.html']:
        patch(ROOT / 'public/courses' / name)
