"""Integra los materiales a la plataforma: toma los colores de la skin activa y limpia el encabezado.

Inserta (o actualiza) embed.css y embed.js en un material ya construido. Es idempotente y lo llama build.py.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CSS = (HERE / 'embed.css').read_text(encoding='utf8').strip()
JS = (HERE / 'embed.js').read_text(encoding='utf8').strip()


def apply(html):
    html = re.sub(r'<style id="aula-embed">.*?</style>', '', html, flags=re.S)
    html = re.sub(r'<script id="aula-embed-js">.*?</script>', '', html, flags=re.S)
    if html.count('</head>') != 1 or html.count('</body>') != 1:
        raise SystemExit('El material no tiene head o body únicos')
    html = html.replace('</head>', f'<style id="aula-embed">{CSS}</style></head>', 1)
    return html.replace('</body>', f'<script id="aula-embed-js">{JS}</script></body>', 1)


if __name__ == '__main__':
    names = sys.argv[1:] or sorted(p.name for p in (ROOT / 'public/courses').glob('*-material.html'))
    for name in names:
        path = ROOT / 'public/courses' / name
        path.write_text(apply(path.read_text(encoding='utf8')), encoding='utf8')
        print(f'{name}: integrado a la plataforma')
