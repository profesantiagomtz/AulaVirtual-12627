"""Fondo ilustrado del tema Navidad (dibujo propio, sin emojis).

Genera public/theme-assets/navidad-fiesta.svg y, con Playwright, navidad-fiesta.png (1536×1024),
con la misma composición que los fondos de Halloween y Día de Muertos: guirnalda arriba,
escena grande a la derecha (pino con regalos) y una esquina adornada abajo a la izquierda.

Correr:  python3 scripts/theme-art/navidad_fiesta.py
"""
import math
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'public/theme-assets'
W, H = 1536, 1024
rnd = random.Random(12)
INK = '#1d3b2a'
BALLS = ['ballR', 'ballG', 'ballB', 'ballY', 'ballP']
LIGHTS = ['#ffd166', '#ff6b6b', '#7fd1ff', '#9cff8a', '#ffb3e6']

defs = f'''
<radialGradient id="ballR" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#ffb3b3"/><stop offset=".35" stop-color="#e53935"/><stop offset="1" stop-color="#8e1414"/></radialGradient>
<radialGradient id="ballG" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#fff2b0"/><stop offset=".35" stop-color="#f2b81f"/><stop offset="1" stop-color="#a86b05"/></radialGradient>
<radialGradient id="ballB" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#cfe9ff"/><stop offset=".35" stop-color="#3b82f6"/><stop offset="1" stop-color="#1e3a8a"/></radialGradient>
<radialGradient id="ballY" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#ffffff"/><stop offset=".4" stop-color="#d9dde6"/><stop offset="1" stop-color="#8b93a6"/></radialGradient>
<radialGradient id="ballP" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#ffd1f0"/><stop offset=".35" stop-color="#c2408f"/><stop offset="1" stop-color="#6d1650"/></radialGradient>
<linearGradient id="tier" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3fae6a"/><stop offset=".55" stop-color="#1f7a46"/><stop offset="1" stop-color="#0f4d2b"/></linearGradient>
<linearGradient id="tierDark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c6b3d"/><stop offset="1" stop-color="#0d3f23"/></linearGradient>
<linearGradient id="snow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#dbe8f3"/></linearGradient>
<linearGradient id="trunk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5b3419"/><stop offset=".5" stop-color="#8a5a32"/><stop offset="1" stop-color="#4a2a14"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#fff6c8" stop-opacity=".95"/><stop offset=".4" stop-color="#ffd166" stop-opacity=".45"/><stop offset="1" stop-color="#ffd166" stop-opacity="0"/></radialGradient>
<radialGradient id="sky" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#dcecf8"/><stop offset=".7" stop-color="#eef6fc" stop-opacity=".7"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<linearGradient id="ribbonGold" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c98f0e"/><stop offset=".5" stop-color="#ffe08a"/><stop offset="1" stop-color="#c98f0e"/></linearGradient>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#0b2a18" flood-opacity=".28"/></filter>
'''


def ball(x, y, r, g=None):
    g = g or rnd.choice(BALLS)
    return (f'<line x1="{x}" y1="{y - r - 10}" x2="{x}" y2="{y - r}" stroke="#c9a227" stroke-width="2"/>'
            f'<rect x="{x - r * .35:.1f}" y="{y - r - 5:.1f}" width="{r * .7:.1f}" height="{r * .35 + 3:.1f}" rx="2" fill="url(#ballG)" stroke="{INK}" stroke-width="1.5"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{g})" stroke="{INK}" stroke-width="2"/>'
            f'<ellipse cx="{x - r * .35:.1f}" cy="{y - r * .38:.1f}" rx="{r * .25:.1f}" ry="{r * .15:.1f}" fill="#fff" opacity=".75" transform="rotate(-30 {x - r * .35:.1f} {y - r * .38:.1f})"/>')


def bulb(x, y, c, s=1.0, rot=0):
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.0f}) scale({s})">'
            f'<circle r="16" fill="url(#glow)"/><rect x="-4" y="-12" width="8" height="6" rx="1.5" fill="#3a4a3f"/>'
            f'<path d="M0 -7 C7 -7 8 3 0 10 C-8 3 -7 -7 0 -7z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
            f'<ellipse cx="-2" cy="-1" rx="1.6" ry="3" fill="#fff" opacity=".8"/></g>')


def star(cx, cy, r1, r2, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i * 180 / n)
        pts.append(f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}')
    return 'M' + ' L'.join(pts) + 'z'


def flake(cx, cy, r, op=.9, w=2.2, color='#9cc9ec'):
    d = ''
    for i in range(6):
        a = math.radians(i * 60 - 90)
        x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        mx, my = cx + r * .55 * math.cos(a), cy + r * .55 * math.sin(a)
        for s in (1, -1):
            b = a + s * math.radians(38)
            d += f'M{mx:.1f} {my:.1f}L{mx + r * .32 * math.cos(b):.1f} {my + r * .32 * math.sin(b):.1f}'
        d += f'M{cx:.1f} {cy:.1f}L{x2:.1f} {y2:.1f}'
    return f'<path d="{d}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" fill="none" opacity="{op}"/>'


def needles(x1, y1, x2, y2, n, size, fill='url(#tier)'):
    """Rama de pino: hileras de agujas a lo largo de una línea."""
    out = []
    for i in range(n):
        t = i / (n - 1)
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        s = size * (0.75 + 0.5 * math.sin(math.pi * t))
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        for side in (1, -1):
            out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{s:.1f}" ry="{s * .28:.1f}" fill="{fill}" stroke="{INK}" stroke-width="1.2" '
                       f'transform="rotate({ang + side * 48:.1f} {x:.1f} {y:.1f}) translate({s * .8:.1f} 0)"/>')
    return ''.join(out)


def bow(x, y, s=1.0, c='#d62e3a'):
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="2" stroke-linejoin="round">'
            f'<path d="M0 0 C-14 -16 -34 -12 -30 2 C-27 12 -10 8 0 0z" fill="{c}"/><path d="M0 0 C14 -16 34 -12 30 2 C27 12 10 8 0 0z" fill="{c}"/>'
            f'<path d="M-3 2 L-12 26 L-4 22 L0 30 L3 4z" fill="{c}"/><path d="M3 2 L12 26 L4 22 L0 30z" fill="{c}"/>'
            f'<circle r="6" fill="{c}"/><path d="M-22 -4 C-16 -8 -10 -6 -6 -2" stroke="#fff" stroke-width="2" fill="none" opacity=".6"/></g>')


def gift(x, y, w, h, body, lid, rib='url(#ribbonGold)', bowc='#ffd166', pattern=None):
    o = [f'<g filter="url(#shadow)" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{body}"/>']
    if pattern == 'dots':
        o += [f'<circle cx="{x + w * fx:.1f}" cy="{y + h * fy:.1f}" r="{min(w, h) * .05:.1f}" fill="#fff" opacity=".75" stroke="none"/>' for fx in (.18, .42, .66, .86) for fy in (.25, .55, .85)]
    if pattern == 'stripes':
        o.append(f'<clipPath id="c{x}{y}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/></clipPath>')
        o.append(f'<g clip-path="url(#c{x}{y})" stroke="none" fill="#fff" opacity=".35">' + ''.join(f'<rect x="{x - h + i * 26}" y="{y}" width="11" height="{h * 2}" transform="rotate(35 {x + i * 26} {y})"/>' for i in range(int((w + h) / 26) + 2)) + '</g>')
    o += [f'<rect x="{x - 6}" y="{y - 18}" width="{w + 12}" height="24" rx="5" fill="{lid}"/>',
          f'<rect x="{x + w / 2 - 9:.1f}" y="{y - 18}" width="18" height="{h + 18}" fill="{rib}"/>',
          f'<rect x="{x}" y="{y + h * .45:.1f}" width="{w}" height="14" fill="{rib}" opacity=".0"/></g>',
          bow(x + w / 2, y - 18, min(w, 140) / 110, bowc)]
    return ''.join(o)


def candy_cane(x, y, s=1.0, rot=0):
    d = 'M0 0 V-120 A28 28 0 0 1 56 -120 V-108'
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" fill="none" stroke-linecap="round">'
            f'<path d="{d}" stroke="{INK}" stroke-width="22"/><path d="{d}" stroke="#fff" stroke-width="16"/>'
            f'<path d="{d}" stroke="#e53935" stroke-width="16" stroke-dasharray="12 12"/></g>')


def holly(x, y, s=1.0, rot=0):
    leaf = 'M0 0 C10 -6 14 -18 30 -22 C26 -16 30 -10 38 -10 C32 -4 34 4 40 6 C28 8 20 4 0 0z'
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="{INK}" stroke-width="2">'
            f'<path d="{leaf}" fill="#2a8f55"/><path d="{leaf}" fill="#1f7a46" transform="scale(-1 1)"/><path d="{leaf}" fill="#35a463" transform="rotate(-70)"/>'
            f'<circle cx="-6" cy="4" r="8" fill="url(#ballR)"/><circle cx="7" cy="6" r="8" fill="url(#ballR)"/><circle cx="1" cy="-6" r="8" fill="url(#ballR)"/></g>')


def poinsettia(x, y, s=1.0):
    p = []
    for i in range(10):
        a = i * 36 + (18 if i % 2 else 0)
        L = 46 if i % 2 == 0 else 34
        p.append(f'<path d="M0 0 C10 -{L * .4:.0f} 8 -{L * .8:.0f} 0 -{L} C-8 -{L * .8:.0f} -10 -{L * .4:.0f} 0 0z" fill="{"#d62e3a" if i % 2 == 0 else "#b51f2b"}" stroke="{INK}" stroke-width="1.8" transform="rotate({a})"/>')
    p += [f'<circle cx="{4 * math.cos(i):.1f}" cy="{4 * math.sin(i):.1f}" r="3.2" fill="#ffd166" stroke="{INK}" stroke-width="1"/>' for i in range(6)]
    return f'<g transform="translate({x} {y}) scale({s})">{"".join(p)}</g>'


def snowman(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="3" filter="url(#shadow)">'
            f'<circle cx="0" cy="-60" r="62" fill="url(#snow)"/><circle cx="0" cy="-160" r="46" fill="url(#snow)"/><circle cx="0" cy="-236" r="34" fill="url(#snow)"/>'
            f'<path d="M-46 -268 h92 M-30 -268 v-46 h60 v46" fill="#1f2433"/><rect x="-30" y="-284" width="60" height="10" fill="#d62e3a" stroke="none"/>'
            f'<circle cx="-12" cy="-242" r="4" fill="{INK}"/><circle cx="12" cy="-242" r="4" fill="{INK}"/><path d="M0 -232 L34 -226 L0 -222z" fill="#f08a24" stroke-width="2"/>'
            f'<path d="M-14 -216 q14 9 28 0" fill="none" stroke-width="2.5"/>'
            f'<path d="M-44 -200 q44 20 88 0 l2 16 q-46 22 -92 0z" fill="#d62e3a"/><path d="M26 -190 l14 52 l-18 2 l-8 -46z" fill="#d62e3a"/>'
            f'<path d="M-30 -196 l-10 0 M-14 -190 l-4 6 M6 -188 l2 6 M26 -194 l6 4" stroke="#fff" stroke-width="3"/>'
            + ''.join(f'<circle cx="0" cy="{cy}" r="5" fill="{INK}"/>' for cy in (-176, -152, -128, -88, -60))
            + f'<path d="M-44 -170 L-104 -214 M-84 -200 l-14 -2 M-84 -200 l-4 -14 M44 -170 L102 -206 M84 -194 l12 -10 M84 -194 l14 2" stroke="#6b4423" stroke-width="5" fill="none" stroke-linecap="round"/></g>')


def tree(cx, base, height, width):
    """Pino grande de tres pisos con ramas de agujas, guirnaldas, esferas y foquitos."""
    o = [f'<ellipse cx="{cx}" cy="{base + 4}" rx="{width * .62:.0f}" ry="30" fill="#0b2a18" opacity=".18" filter="url(#soft)"/>',
         f'<rect x="{cx - 34}" y="{base - 80}" width="68" height="90" rx="8" fill="url(#trunk)" stroke="{INK}" stroke-width="3"/>']
    top = base - height
    ornaments, lights, garlands = [], [], []
    # pisos de abajo hacia arriba
    for (yt, yb, wf) in [(0.30, 0.94, 1.0), (0.16, 0.66, .78), (0.02, 0.40, .55)]:
        y_top, y_bot = top + height * yt, top + height * yb
        half = width / 2 * wf
        # silueta con borde ondulado
        n = 9
        o.append(f'<path d="M{cx} {y_top:.1f} C{cx + half * .3:.1f} {y_top + (y_bot - y_top) * .45:.1f} {cx + half * .8:.1f} {y_bot - 30:.1f} {cx + half:.1f} {y_bot:.1f} '
                 f'L{cx - half:.1f} {y_bot:.1f} C{cx - half * .8:.1f} {y_bot - 30:.1f} {cx - half * .3:.1f} {y_top + (y_bot - y_top) * .45:.1f} {cx} {y_top:.1f}z" fill="url(#tier)" stroke="{INK}" stroke-width="3.5"/>')
        o.append(f'<path d="M{cx - half:.1f} {y_bot:.1f} ' + ' '.join(f'Q{cx - half + (i + .5) * 2 * half / n:.1f} {y_bot + 28:.1f} {cx - half + (i + 1) * 2 * half / n:.1f} {y_bot:.1f}' for i in range(n)) + f'" fill="url(#tierDark)" stroke="{INK}" stroke-width="3.5"/>')
        # sombras de ramas
        for i in range(7):
            fx = -0.75 + i * .25
            o.append(f'<path d="M{cx + fx * half * .5:.1f} {y_top + (y_bot - y_top) * .35:.1f} Q{cx + fx * half * .85:.1f} {y_bot - 40:.1f} {cx + fx * half * 1.0:.1f} {y_bot + 6:.1f}" stroke="#0f4d2b" stroke-width="3" fill="none" opacity=".45"/>')
        # nieve sobre las puntas
        o.append(f'<path d="M{cx - half * .92:.1f} {y_bot - 4:.1f} ' + ' '.join(f'q{half / n * .9:.1f} -{12 + (i % 3) * 4} {2 * half / n:.1f} 2' for i in range(n - 1)) + f'" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" opacity=".95"/>')
        # guirnalda dorada en curva
        garlands.append(f'<path d="M{cx - half * .72:.1f} {y_top + (y_bot - y_top) * .55:.1f} Q{cx:.1f} {y_top + (y_bot - y_top) * .85:.1f} {cx + half * .78:.1f} {y_top + (y_bot - y_top) * .45:.1f}" stroke="url(#ribbonGold)" stroke-width="9" fill="none" stroke-linecap="round" stroke-dasharray="1 0"/>')
        # cadena de foquitos
        m = 9
        for i in range(m):
            t = (i + .5) / m
            x = cx - half * .9 + t * half * 1.8
            yy = y_top + (y_bot - y_top) * (.25 + .5 * (4 * t * (1 - t)) * .6 + .35)
            if abs(x - cx) < (yy - y_top) / (y_bot - y_top) * half * .95:
                lights.append(bulb(x, yy, LIGHTS[(i + len(lights)) % 5], 1.1, (t - .5) * 50))
        for i in range(6):
            fy = rnd.uniform(.35, .85)
            yy = y_top + (y_bot - y_top) * fy
            lim = half * fy * .85
            ornaments.append(ball(cx + rnd.uniform(-lim, lim), yy, rnd.choice([13, 15, 17, 19])))
    o += garlands + ornaments + lights
    # estrella con halo
    o.append(f'<circle cx="{cx}" cy="{top - 6}" r="90" fill="url(#glow)"/>')
    o.append(f'<path d="{star(cx, top - 6, 52, 22)}" fill="url(#ballG)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    o.append(f'<path d="{star(cx, top - 6, 24, 10)}" fill="#fff6c8" opacity=".75"/>')
    return ''.join(o)


def garland_top():
    o = []
    # cuerda que cuelga en ondas a lo largo de arriba
    pts = [(-20, 40), (300, 110), (620, 50), (940, 112), (1260, 52), (1560, 104)]
    path = f'M{pts[0][0]} {pts[0][1]} ' + ' '.join(f'Q{(a[0] + b[0]) / 2} {max(a[1], b[1]) + 46} {b[0]} {b[1]}' for a, b in zip(pts, pts[1:]))
    o.append(f'<path d="{path}" stroke="#0f4d2b" stroke-width="10" fill="none"/>')
    # agujas a lo largo
    for (a, b) in zip(pts, pts[1:]):
        mx, my = (a[0] + b[0]) / 2, max(a[1], b[1]) + 46
        for s in range(18):
            t = s / 17
            x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * mx + t ** 2 * b[0]
            y = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * my + t ** 2 * b[1]
            for k in range(3):
                ang = rnd.uniform(0, 360)
                L = rnd.uniform(16, 26)
                o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{L:.1f}" ry="{L * .25:.1f}" fill="{rnd.choice(["#2a8f55", "#1f7a46", "#35a463"])}" stroke="{INK}" stroke-width="1" transform="rotate({ang:.0f} {x:.1f} {y:.1f}) translate({L * .7:.1f} 0)"/>')
        # foquitos y esferas colgando
        for s in range(1, 6):
            t = s / 6
            x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * mx + t ** 2 * b[0]
            y = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * my + t ** 2 * b[1]
            o.append(bulb(x, y + 16, LIGHTS[(s + int(a[0])) % 5], 1.25))
        x = mx
        y = (a[1] + b[1]) / 4 + my / 2
        o.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + 46}" stroke="#c9a227" stroke-width="2.5"/>' + ball(x, y + 70, 22))
    for (x, y) in pts[1:-1]:
        o.append(bow(x, y + 4, 1.25))
    return ''.join(o)


def corner_tl():
    o = [needles(0, 170, 210, 30, 14, 44), needles(0, 60, 150, 0, 10, 34), needles(30, 260, 120, 120, 9, 30)]
    o += [ball(150, 140, 24, 'ballR'), ball(90, 205, 20, 'ballG'), ball(215, 85, 18, 'ballB')]
    o += [holly(60, 110, 1.4, 20), poinsettia(170, 45, 1.2)]
    return ''.join(o)


def corner_bl():
    o = [f'<path d="M-20 1040 C40 900 180 880 300 930 C380 960 440 990 520 1040z" fill="url(#snow)" stroke="#c7d9e8" stroke-width="3"/>']
    o += [needles(-10, 900, 220, 1000, 14, 40), needles(-10, 820, 120, 980, 10, 34)]
    o += [gift(70, 900, 120, 92, '#3b6fd8', '#5a8ae8', '#fff', '#ffffff', 'dots'), gift(210, 935, 90, 70, '#d62e3a', '#e85a5a', pattern='stripes')]
    o += [candy_cane(330, 1000, 1.0, 12), holly(40, 860, 1.5, -20), poinsettia(330, 960, .9)]
    o += [ball(160, 860, 20, 'ballP')]
    return ''.join(o)


def scene_right():
    o = [f'<path d="M820 1040 C900 940 1080 900 1240 920 C1380 935 1480 900 1560 880 V1040z" fill="url(#snow)" stroke="#c7d9e8" stroke-width="3"/>']
    o.append(tree(1240, 900, 690, 520))
    o.append(snowman(1452, 985, .66))
    # montón de regalos al pie
    o += [gift(1040, 880, 140, 100, '#d62e3a', '#e85a5a', pattern='dots'),
          gift(1190, 900, 110, 82, '#2f9e5b', '#3fbf72', '#d62e3a', '#d62e3a', 'stripes'),
          gift(1310, 870, 150, 112, '#3b6fd8', '#5a8ae8', '#fff', '#ffffff', 'dots'),
          gift(960, 930, 90, 68, '#f2b81f', '#ffd166', '#d62e3a', '#d62e3a'),
          gift(1110, 950, 120, 70, '#c2408f', '#e05ab0', 'url(#ribbonGold)', '#ffd166', 'stripes'),
          gift(1250, 960, 96, 62, '#ffffff', '#f0f4f8', '#d62e3a', '#d62e3a', 'stripes')]
    o += [candy_cane(920, 1010, 1.15, -10), candy_cane(1520, 1010, .9, 8), poinsettia(870, 990, 1.0)]
    return ''.join(o)


def backdrop():
    """Colinas nevadas y pinitos lejanos detrás del pino grande, para dar profundidad."""
    o = ['<path d="M760 900 C860 800 980 780 1080 810 C1180 760 1330 740 1560 780 V1040 H760z" fill="#e6f0f8"/>']
    for x, y, s in ((880, 860, .9), (960, 840, .7), (1030, 830, .55), (1480, 800, .8), (1420, 790, .6), (1530, 820, .65), (820, 880, .6)):
        o.append(f'<g transform="translate({x} {y}) scale({s})" fill="#b9d3c4" opacity=".9"><path d="M0 -150 L44 -80 H24 L60 -20 H32 L70 40 H-70 L-32 -20 H-60 L-24 -80 H-44z"/>'
                 f'<path d="M-40 -84 q20 -8 40 0 q20 -8 40 0M-56 -24 q28 -8 56 0 q28 -8 56 0" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/></g>')
    return ''.join(o)


def snowfall():
    o = []
    for _ in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        if 420 < x < 900 and 220 < y < 760:   # centro despejado para el contenido
            continue
        r = rnd.choice([6, 8, 10, 14, 18])
        o.append(flake(x, y, r, rnd.uniform(.45, .9), 1.6 if r < 10 else 2.4) if r >= 10 else f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r / 2.5:.1f}" fill="#cfe4f5" opacity=".9"/>')
    for _ in range(18):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        if 420 < x < 900 and 220 < y < 760:
            continue
        o.append(f'<path d="{star(x, y, 11, 3, 4)}" fill="#ffd166" opacity=".85"/>')
    return ''.join(o)


svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs>{defs}</defs>'
       
       f'<ellipse cx="1240" cy="600" rx="520" ry="560" fill="url(#sky)"/>' + backdrop()
       + snowfall() + scene_right() + corner_bl() + corner_tl() + garland_top() + '</svg>')
OUT.joinpath('navidad-fiesta.svg').write_text(svg, encoding='utf8')
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:{W},height:{H}}}}});
await p.goto('file://{OUT / 'navidad-fiesta.svg'}');await p.screenshot({{path:'{OUT / 'navidad-fiesta.png'}',omitBackground:true}});await b.close()}})()"""
subprocess.run(['node', '-e', js], check=True, cwd='/tmp')
OUT.joinpath('navidad-fiesta.svg').unlink()
print('Fondo de Navidad → public/theme-assets/navidad-fiesta.png')
