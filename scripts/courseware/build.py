"""Genera materiales integrados con el mismo motor que los de R.A. 1.2.

Toma public/courses/asin-ra12-material.html como plantilla (estilos, navegación,
actividades autocorregibles, prácticas PC/celular y evaluación desbloqueable) y
sustituye solo los datos del curso. Uso:

    python3 scripts/courseware/build.py asin_ra21 msii_ra21
"""
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / 'public/courses/asin-ra12-material.html'
HERE = Path(__file__).resolve().parent


def js(value):
    return json.dumps(value, ensure_ascii=False).replace('</', '<\\/')


def evaluation_page(e):
    """Página de la actividad de evaluación (se muestra desbloqueada dentro del material)."""
    tpl = TEMPLATE.read_text(encoding='utf8')
    first = tpl[tpl.index('<script>var EV=') + len('<script>var EV='):]
    ev = json.loads(first[:first.index('\n')].rstrip(';'))
    head = ev[:ev.index('</style>') + len('</style>')].replace('R.A. 1.2 · Actividad de evaluación', f"{e['ra']} · Actividad de evaluación")
    script = ev[ev.index('<script>'):]
    steps, n = [], 0
    for group, items in e['steps']:
        steps.append(f'<h3>{group}</h3>')
        for item in items:
            n += 1
            steps.append(f'<label class="st"><input type="checkbox"><span><b>{n}.</b> {item}</span></label>')
    rubric = ''.join(f'<tr><td>{c}</td><td>{p}</td></tr>' for c, p in e['rubric'])
    total = sum(p for _, p in e['rubric'])
    data = ''.join(f'<div><b>{k}</b>{v}</div>' for k, v in e['data'])
    deliver = ''.join(f'<li>{x}</li>' for x in e['deliver'])
    return (head + '</head><body><main>\n'
            f'<div class="top"><small>{e["course"]}</small><h1>{e["ra"]} · {e["title"]}</h1></div>\n'
            f'<section><h2>Datos de la actividad</h2><div class="dl">{data}</div></section>\n'
            f'<section><h2>Situación</h2><p>{e["situation"]}</p><div class="hint">💡 {e["hint"]}</div></section>\n'
            '<div class="pr"><span id="pt">0 de 0 pasos</span><i id="pb"></i></div>\n'
            f'<section><h2>Instrucciones</h2>{"".join(steps)}</section>\n'
            f'<section><h2>Lista de cotejo</h2><table><tr><th>Criterio</th><th>Pts</th></tr>{rubric}<tr><th>Total</th><th>{total}</th></tr></table></section>\n'
            f'<section><h2>Entrega</h2><ul>{deliver}</ul></section>\n'
            '</main>' + script)


def build(name):
    c = importlib.import_module(name)
    lines = TEMPLATE.read_text(encoding='utf8').replace('<script>var EV=', '\n<script>var EV=', 1).split('\n')
    script_start = next(i for i, l in enumerate(lines) if l.startswith('<script>var EV='))
    head, body = lines[:script_start], lines[script_start:]
    idx = {key: next(i for i, l in enumerate(body) if l.startswith(prefix)) for key, prefix in {
        'exp': 'var EXP={', 'esc': 'function esc(', 'ill': 'var ILL={};', 'grid3': 'function grid3(',
        'pL': 'function pL(', 'exh': 'var EXH={};', 'exhcap': 'function exw(', 'p': 'var P=[', 'sec': 'var SEC=',
        'pr': 'var PR=', 'flags': 'var SIMUL=', 'sid': 'var SID=', 'sv': 'function sv(', 'mkcode': 'function mkcode(',
        'checkPage': 'function checkPage(', 'initW': 'function initW(', 'end': '</script>'}.items()}

    def until(start, stop_prefixes):
        return next(i for i in range(start, len(body)) if any(body[i].startswith(p) for p in stop_prefixes))

    lessons = {json.loads(t) for t in re.findall(r'pL\("(?:[^"\\]|\\.)*",("(?:[^"\\]|\\.)*")', c.P)}
    for title in re.findall(r'^ILL\["(.+?)"\]', c.ILL, re.M):
        if title not in lessons:
            raise SystemExit(f'Ilustración sin lección: {title}')
    exh = set(re.findall(r'^EXH\.(\w+)=', c.EXH, re.M))
    for p in c.PR:
        for mode in p['modes'].values():
            for s in mode['steps']:
                if isinstance(s, list) and s[1] not in exh:
                    raise SystemExit(f'Falta EXH.{s[1]} ({p["id"]})')

    out = []
    out.append('<script>var EV=' + js(evaluation_page(c.EVALUATION)) + ';')
    out.append('var EXP=' + js(c.EXP) + ';')
    out.append('var EXP2={};')
    # Motor sin cambios hasta las ilustraciones.
    out += body[idx['esc']:idx['ill'] + 1]
    out += c.ILL.strip().split('\n')
    out.append(body[idx['grid3']])
    out.append('')
    out += body[idx['pL']:idx['exhcap'] + 1]
    out += c.EXH.strip().split('\n')
    out.append('')
    out.append(getattr(c, 'EXTRA_JS', '').strip())
    out.append('var P=[')
    out += [l.rstrip() for l in c.P.strip().split('\n')]
    out.append('];')
    out.append('var SEC=' + js(c.SEC) + ';')
    out.append('var CH={')
    out += c.CH.strip().split('\n')
    out.append('};')
    out.append('var ORDER=' + js(c.ORDER) + ';')
    out.append('var PR=' + js(c.PR) + ';')
    out += body[idx['flags']:idx['end'] + 1]
    out += body[idx['end'] + 1:]
    html = '\n'.join(head + out)

    code, short = c.CODE, c.CODE.lower().replace('-ra-', '-ra').replace('.', '')
    replacements = [
        ('KEY="asin-ra12-avance-"', f'KEY="{short}-avance-"'),
        ('source:"ASIN-RA-1.2"', f'source:"{code}"'),
        ('m:"asin-ra12"', f'm:"{short}"'),
        ('return "ASIN1."', f'return "{c.CODE_PREFIX}."'),
        ('<title>ASIN-20 · R.A. 1.2 · Plan de seguridad</title>', f'<title>{c.TITLE_TAG}</title>'),
        ('<b>ASIN-20 · Seguridad informática</b><span>R.A. 1.2 · Plan de seguridad en cómputo</span>', f'<b>{c.BRAND}</b><span>{c.BRAND_SUB}</span>'),
        ('<small>ASIN-20 · R.A. 1.2</small><h1>Plan de seguridad en cómputo</h1><p>Aprende los modelos, los estándares y cómo armar un plan con sus políticas y métricas.</p>', f'<small>{c.HERO_KICK}</small><h1>{c.HERO_TITLE}</h1><p>{c.HERO_TEXT}</p>'),
        ('"elabora tu plan y tus políticas de seguridad."', js(c.EV_SHORT)),
        ('"Desbloqueada: elabora tu plan y tus políticas de seguridad."', js('Desbloqueada: ' + c.EV_SHORT)),
        ('<span><b>Plan y políticas</b><small>', f'<span><b>{c.EV_CARD}</b><small>'),
        ('<iframe title="Actividad de evaluación R.A. 1.2">', f'<iframe title="Actividad de evaluación {c.RA}">'),
        ('placeholder="Grupo (ej. 310)"', f'placeholder="Grupo (ej. {c.GROUP})"'),
    ]
    for old, new in replacements:
        if old not in html:
            raise SystemExit(f'No se encontró en la plantilla: {old[:60]}')
        html = html.replace(old, new)
    tabs = {'a': ['Aprende', 'Teoría, esquemas y ejercicios'], 'd': ['Diagnostica', 'Herramientas y simulador'], 'c': ['Construye', 'Prácticas guiadas']}
    tabs.update(getattr(c, 'TABS', {}))
    html, n = re.subn(r'/\*TABL\*/\{[^}]*\}', lambda m: '/*TABL*/' + js(tabs), html, count=1)
    if n != 1:
        raise SystemExit('La plantilla no tiene las pestañas: ejecuta patch_tabs.py')
    for old, new in getattr(c, 'ENGINE_PATCHES', []):
        if html.count(old) != 1:
            raise SystemExit(f'Parche ambiguo o ausente: {old[:60]}')
        html = html.replace(old, new)
    target = ROOT / 'public/courses' / c.FILE
    target.write_text(html, encoding='utf8')
    print(f'{target.relative_to(ROOT)}: {len(html):,} bytes, {c.P.count(chr(10)) + 1} páginas')


if __name__ == '__main__':
    sys.path.insert(0, str(HERE))
    for module in sys.argv[1:] or ['asin_ra21', 'msii_ra21']:
        build(module)
