"""Integra los materiales a la plataforma: toma los colores de la skin activa, limpia el encabezado y agrega los apuntes imprimibles.

Inserta (o actualiza) embed.css y embed.js en un material ya construido. Es idempotente y lo llama build.py.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CSS = (HERE / 'embed.css').read_text(encoding='utf8').strip()
JS = (HERE / 'embed.js').read_text(encoding='utf8').strip()
FIT = HERE / 'print_fit.json'
# Dibujos propios en lugar de emojis (scripts/icons/aula_icons.py → src/lib/aula-icons.json).
ICON_DATA = json.loads((ROOT / 'src/lib/aula-icons.json').read_text(encoding='utf8'))
ICONS = (HERE / 'icons.js').read_text(encoding='utf8').strip().replace(
    '/*ICONS*/{}', json.dumps({'icons': ICON_DATA['icons'], 'emoji': ICON_DATA['emoji']}, ensure_ascii=False, separators=(',', ':')))
PICTO = re.compile('[\U0001F1E6-\U0001F1FF\U0001F300-\U0001FAFF]')
NOTES = (HERE / 'print_notes.js').read_text(encoding='utf8').strip().replace(
    '/*FIT*/{}', '/*FIT*/' + (json.dumps(json.loads(FIT.read_text(encoding='utf8'))) if FIT.exists() else '{}'))


def apply(html):
    html = re.sub(r'<style id="aula-embed">.*?</style>', '', html, flags=re.S)
    html = re.sub(r'<script id="aula-embed-js">.*?</script>', '', html, flags=re.S)
    html = re.sub(r'<script id="aula-apuntes">.*?</script>', '', html, flags=re.S)
    html = re.sub(r'<script id="aula-icons-js">.*?</script>', '', html, flags=re.S)
    if html.count('</head>') != 1 or html.count('</body>') != 1:
        raise SystemExit('El material no tiene head o body únicos')
    html = html.replace('</head>', f'<style id="aula-embed">{CSS}</style></head>', 1)
    # Apuntes imprimibles de «Aprende»: el script solo se activa a partir del R.A. 2.1.
    # Los emojis del material se cambian por dibujos propios al mostrarse (icons.js).
    return html.replace('</body>', f'<script id="aula-icons-js">{ICONS}</script><script id="aula-embed-js">{JS}</script><script id="aula-apuntes">{NOTES}</script></body>', 1)


def missing(html):
    """Emojis del material que todavía no tienen dibujo propio (se ocultarían)."""
    html = re.sub(r'<script id="aula-icons-js">.*?</script>', '', html, flags=re.S)
    known = ICON_DATA['emoji']
    return sorted({c for c in PICTO.findall(html) if c not in known and not any(k.startswith(c) for k in known)})


if __name__ == '__main__':
    names = sys.argv[1:] or sorted(p.name for p in (ROOT / 'public/courses').glob('*-material.html'))
    for name in names:
        path = ROOT / 'public/courses' / name
        html = apply(path.read_text(encoding='utf8'))
        path.write_text(html, encoding='utf8')
        falta = missing(html)
        print(f'{name}: integrado a la plataforma' + (f'  AVISO: emojis sin dibujo propio: {" ".join(falta)} (agrégalos en scripts/icons/aula_icons.py)' if falta else ''))
