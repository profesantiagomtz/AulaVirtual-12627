"""Fondo ilustrado del tema Acción de Gracias (dibujo propio, sin emojis).

Misma composición que los fondos de Halloween, Día de Muertos y Navidad: guirnalda de hojas arriba,
escena grande a la derecha (cuerno de la abundancia, calabazas y pavito) y una esquina adornada abajo
a la izquierda. Genera public/theme-assets/gracias-fiesta.png (1536×1024, fondo transparente).

Correr:  python3 scripts/theme-art/gracias_fiesta.py
"""
import math
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'public/theme-assets'
W, H = 1536, 1024
rnd = random.Random(7)
INK = '#4a2a14'
LEAF = ['#d9481e', '#e8902a', '#f2b81f', '#b8321c', '#c9772f', '#8a9a3a']

defs = '''
<radialGradient id="pump" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#ffc06b"/><stop offset=".5" stop-color="#f08a24"/><stop offset="1" stop-color="#b8560f"/></radialGradient>
<radialGradient id="pumpW" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#fffaf0"/><stop offset=".6" stop-color="#f1e6d2"/><stop offset="1" stop-color="#c9b896"/></radialGradient>
<radialGradient id="apple" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ff9a8a"/><stop offset=".4" stop-color="#d93c3c"/><stop offset="1" stop-color="#8e1414"/></radialGradient>
<radialGradient id="grape" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#c9a4f0"/><stop offset=".45" stop-color="#7b3fb0"/><stop offset="1" stop-color="#3e1a63"/></radialGradient>
<linearGradient id="horn" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e3b56b"/><stop offset=".6" stop-color="#b9813e"/><stop offset="1" stop-color="#7a4a20"/></linearGradient>
<linearGradient id="hay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d27a"/><stop offset="1" stop-color="#c99a3a"/></linearGradient>
<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6e2c2"/><stop offset="1" stop-color="#e8c896"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a5a32"/><stop offset=".5" stop-color="#b07a48"/><stop offset="1" stop-color="#7a4a24"/></linearGradient>
<radialGradient id="sky" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fde7c4"/><stop offset=".7" stop-color="#fdf1de" stop-opacity=".7"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
<filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="7" stdDeviation="7" flood-color="#5a2e17" flood-opacity=".28"/></filter>
<filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>
'''


def maple(x, y, s, c, rot=0):
    d = 'M0 -40 L8 -22 L20 -28 L17 -12 L34 -15 L26 -3 L38 6 L20 9 L23 20 L4 14 L2 34 L-2 34 L-4 14 L-23 20 L-20 9 L-38 6 L-26 -3 L-34 -15 L-17 -12 L-20 -28 L-8 -22z'
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.0f}) scale({s:.2f})"><path d="{d}" fill="{c}" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<path d="M0 34 V-30 M0 0 L22 -10 M0 0 L-22 -10 M0 12 L16 16 M0 12 L-16 16" stroke="{INK}" stroke-width="1.6" opacity=".55" fill="none"/></g>')


def oak(x, y, s, c, rot=0):
    d = 'M0 -40 C8 -36 4 -28 12 -26 C20 -24 18 -14 12 -10 C22 -8 22 2 14 4 C22 8 18 18 8 16 C10 24 4 30 0 34 C-4 30 -10 24 -8 16 C-18 18 -22 8 -14 4 C-22 2 -22 -8 -12 -10 C-18 -14 -20 -24 -12 -26 C-4 -28 -8 -36 0 -40z'
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.0f}) scale({s:.2f})"><path d="{d}" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
            f'<path d="M0 40 V-32 M0 -10 L10 -16 M0 4 L-10 -2 M0 16 L8 12" stroke="{INK}" stroke-width="1.6" opacity=".55" fill="none"/></g>')


def leaf(x, y, s=1.0, rot=None, c=None):
    rot = rnd.uniform(-60, 60) if rot is None else rot
    c = c or rnd.choice(LEAF)
    return (maple if rnd.random() < .55 else oak)(x, y, s, c, rot)


def pumpkin(x, y, w, h, white=False, stem='#5b7a2a'):
    g = 'pumpW' if white else 'pump'
    o = [f'<g filter="url(#shadow)" stroke="{INK}" stroke-width="3">']
    for f in (-.32, .32, -.16, .16, 0):
        o.append(f'<ellipse cx="{x + w * f:.1f}" cy="{y}" rx="{w * (.34 if f else .3):.1f}" ry="{h / 2:.1f}" fill="url(#{g})"/>')
    o.append(f'<path d="M{x - 6} {y - h / 2 + 4} C{x - 8} {y - h / 2 - 18} {x + 4} {y - h / 2 - 26} {x + 14} {y - h / 2 - 22}" stroke="{stem}" stroke-width="{max(7, w * .07):.0f}" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M{x + 10} {y - h / 2 - 14} c18 -14 30 -4 38 -14" stroke="#6fae4b" stroke-width="3" fill="none"/></g>')
    o.append(f'<ellipse cx="{x - w * .22:.1f}" cy="{y - h * .2:.1f}" rx="{w * .06:.1f}" ry="{h * .16:.1f}" fill="#fff" opacity=".45"/>')
    return ''.join(o)


def apple(x, y, r=26):
    return (f'<g filter="url(#shadow)"><circle cx="{x}" cy="{y}" r="{r}" fill="url(#apple)" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M{x} {y - r + 4} q2 -14 8 -18" stroke="{INK}" stroke-width="3" fill="none"/><path d="M{x + 4} {y - r - 6} c12 -10 24 -6 26 0 c-10 6 -20 6 -26 0z" fill="#6fae4b" stroke="{INK}" stroke-width="2"/>'
            f'<ellipse cx="{x - r * .4:.1f}" cy="{y - r * .35:.1f}" rx="{r * .18:.1f}" ry="{r * .1:.1f}" fill="#fff" opacity=".7" transform="rotate(-35 {x - r * .4:.1f} {y - r * .35:.1f})"/></g>')


def grapes(x, y, s=1.0):
    pts = [(0, 0), (-16, -4), (16, -4), (-8, 14), (8, 14), (0, 28), (-24, 10), (24, 10), (-14, 28), (14, 28), (0, 44), (-6, 58), (8, 58)]
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#shadow)"><path d="M0 -6 q4 -18 -6 -26" stroke="{INK}" stroke-width="3" fill="none"/>'
            f'<path d="M0 -14 c20 -18 40 -6 42 4 c-16 6 -30 4 -42 -4z" fill="#8a9a3a" stroke="{INK}" stroke-width="2"/>'
            + ''.join(f'<circle cx="{px}" cy="{py}" r="11" fill="url(#grape)" stroke="{INK}" stroke-width="1.8"/>' for px, py in pts) + '</g>')


def corn(x, y, s=1.0, rot=0):
    o = [f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#shadow)" stroke="{INK}" stroke-width="2.4">',
         '<path d="M0 -80 C22 -80 30 -40 30 0 C30 40 20 70 0 70 C-20 70 -30 40 -30 0 C-30 -40 -22 -80 0 -80z" fill="#f7c948"/>']
    o += [f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="#e6a817" stroke-width="1"/>' for cy in range(-62, 64, 13) for cx in (-14, 0, 14) if abs(cx) < 22 - abs(cy) * .12]
    o += ['<path d="M0 70 C-30 60 -50 20 -44 -40 C-30 -10 -20 30 0 70z" fill="#c9a24a"/><path d="M0 70 C30 60 50 20 44 -40 C30 -10 20 30 0 70z" fill="#b8913a"/>',
          '<path d="M0 70 C-6 40 -20 10 -26 -20 M0 70 C6 40 20 10 26 -20" stroke-width="1.4" fill="none" opacity=".6"/></g>']
    return ''.join(o)


def wheat(x, y, s=1.0, rot=0):
    o = [f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="{INK}" stroke-width="1.8">']
    for k, a in enumerate((-18, -8, 0, 8, 18)):
        o.append(f'<g transform="rotate({a})"><path d="M0 0 V-150" stroke="#c99a3a" stroke-width="3"/>' +
                 ''.join(f'<ellipse cx="{sx * 7}" cy="{-150 + i * 13}" rx="5" ry="10" fill="#e6b24a" transform="rotate({sx * 28} {sx * 7} {-150 + i * 13})"/>' for i in range(5) for sx in (-1, 1)) +
                 '<ellipse cx="0" cy="-158" rx="5" ry="10" fill="#e6b24a"/></g>')
    o.append('<path d="M-14 -40 h28" stroke="#b8321c" stroke-width="7"/></g>')
    return ''.join(o)


def sunflower(x, y, r=46, stem=140):
    o = [f'<path d="M{x} {y} V{y + stem}" stroke="#4c7a2a" stroke-width="7"/>',
         f'<path d="M{x} {y + stem * .55} c26 -26 52 -20 60 -8 c-24 12 -44 14 -60 8z" fill="#6fae4b" stroke="{INK}" stroke-width="2"/>']
    for i in range(18):
        a = i * 20
        o.append(f'<ellipse cx="{x}" cy="{y - r * .78:.1f}" rx="{r * .2:.1f}" ry="{r * .42:.1f}" fill="{"#f7c948" if i % 2 else "#f2b81f"}" stroke="{INK}" stroke-width="2" transform="rotate({a} {x} {y})"/>')
    o.append(f'<circle cx="{x}" cy="{y}" r="{r * .48:.1f}" fill="#6b3a1c" stroke="{INK}" stroke-width="2.5"/>')
    o += [f'<circle cx="{x + r * .3 * math.cos(a):.1f}" cy="{y + r * .3 * math.sin(a):.1f}" r="2.4" fill="#c8915a"/>' for a in [i * .9 for i in range(7)]]
    return ''.join(o)


def hay(x, y, w, h):
    o = [f'<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="url(#hay)" stroke="{INK}" stroke-width="3"/>']
    o += [f'<path d="M{x + 10 + i * 9} {y + 6} l{rnd.uniform(-4, 4):.1f} {h - 12}" stroke="#b8862a" stroke-width="2" opacity=".6"/>' for i in range(int((w - 20) / 9))]
    o += [f'<path d="M{x} {y + h * f:.0f} h{w}" stroke="#8a5a20" stroke-width="5"/>' for f in (.3, .7)]
    o += [f'<path d="M{x + rnd.uniform(0, w):.0f} {y} l{rnd.uniform(-8, 8):.0f} -12" stroke="#d9a83a" stroke-width="2"/>' for _ in range(14)]
    return ''.join(o) + '</g>'


def turkey(x, y, s=1.0):
    feathers = ['#b8321c', '#e8902a', '#8a4a22', '#f2b81f', '#5f7f3a', '#e8902a', '#b8321c', '#c9772f', '#f2b81f']
    o = [f'<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="3" filter="url(#shadow)">']
    for i, c in enumerate(feathers):
        a = -80 + i * 20
        o.append(f'<ellipse cx="0" cy="-110" rx="26" ry="78" fill="{c}" transform="rotate({a} 0 -40)"/>')
        o.append(f'<ellipse cx="0" cy="-170" rx="10" ry="14" fill="#fff4dc" stroke-width="1.5" opacity=".85" transform="rotate({a} 0 -40)"/>')
    o += ['<ellipse cx="0" cy="-30" rx="62" ry="66" fill="#8a5a3b"/>',
          '<path d="M-40 -40 q40 34 80 0 M-46 -14 q46 34 92 0" stroke="#6b4228" stroke-width="3" fill="none"/>',
          '<path d="M-58 -36 c-24 10 -24 40 0 52 M58 -36 c24 10 24 40 0 52" fill="#7a4a2a"/>',
          '<circle cx="0" cy="-104" r="34" fill="#a8714a"/>',
          '<circle cx="-12" cy="-110" r="7" fill="#fff"/><circle cx="12" cy="-110" r="7" fill="#fff"/><circle cx="-11" cy="-109" r="3.6" fill="#2b1a10" stroke="none"/><circle cx="13" cy="-109" r="3.6" fill="#2b1a10" stroke="none"/>',
          '<path d="M-8 -96 L8 -96 L0 -82z" fill="#f2b81f"/>',
          '<path d="M3 -86 c12 6 10 24 -2 28 c-6 -8 -6 -20 2 -28z" fill="#d93c3c"/>',
          '<circle cx="-22" cy="-94" r="6" fill="#ff9aa8" stroke="none" opacity=".8"/><circle cx="22" cy="-94" r="6" fill="#ff9aa8" stroke="none" opacity=".8"/>',
          '<path d="M-20 34 v28 M20 34 v28 M-34 64 h28 M6 64 h28" stroke="#e8902a" stroke-width="6" stroke-linecap="round"/>',
          '<path d="M-14 -142 l-6 -18 M0 -140 v-20 M14 -142 l6 -18" stroke-width="3" opacity=".0"/>',
          '</g>']
    return ''.join(o)


def cornucopia(x, y, s=1.0):
    o = [f'<g transform="translate({x} {y}) scale({s})">',
         f'<path d="M260 -40 C200 -150 40 -170 -40 -110 C-90 -70 -100 10 -60 60 C-20 100 60 90 120 40 C170 0 230 -10 260 -40z" fill="url(#horn)" stroke="{INK}" stroke-width="4" filter="url(#shadow)"/>']
    for i in range(7):
        t = i / 6
        o.append(f'<path d="M{250 - t * 290:.0f} {-44 - math.sin(t * math.pi) * 90:.0f} C{230 - t * 300:.0f} {-10 - math.sin(t * math.pi) * 60:.0f} {200 - t * 260:.0f} {30 + math.sin(t * math.pi) * 20:.0f} {150 - t * 230:.0f} {40 + math.sin(t * math.pi) * 40:.0f}" stroke="#8a5a20" stroke-width="3" fill="none" opacity=".55"/>')
    o.append(f'<path d="M260 -40 c40 -40 70 -30 80 -70 c6 -24 -10 -36 -24 -24" stroke="{INK}" stroke-width="18" fill="none" stroke-linecap="round"/><path d="M260 -40 c40 -40 70 -30 80 -70 c6 -24 -10 -36 -24 -24" stroke="#c9914a" stroke-width="12" fill="none" stroke-linecap="round"/>')
    o.append(f'<ellipse cx="-60" cy="-20" rx="60" ry="86" fill="#5a3418" stroke="{INK}" stroke-width="4" transform="rotate(-18 -60 -20)"/>')
    # frutas que se derraman
    o += [grapes(-90, -80, 1.2), corn(-140, 30, .9, -70), apple(-40, 40, 30), pumpkin(-130, 110, 120, 90), apple(-210, 110, 28),
          pumpkin(-260, 70, 90, 70, True), grapes(-220, 0, .9), apple(-10, 110, 26), leaf(-170, -60, 1.2), leaf(10, -60, 1.0)]
    o.append('</g>')
    return ''.join(o)


def garland_top():
    o = []
    pts = [(-20, 30), (300, 96), (620, 40), (940, 100), (1260, 42), (1560, 92)]
    path = f'M{pts[0][0]} {pts[0][1]} ' + ' '.join(f'Q{(a[0] + b[0]) / 2} {max(a[1], b[1]) + 44} {b[0]} {b[1]}' for a, b in zip(pts, pts[1:]))
    o.append(f'<path d="{path}" stroke="#a87a3a" stroke-width="5" fill="none"/>')
    for a, b in zip(pts, pts[1:]):
        mx, my = (a[0] + b[0]) / 2, max(a[1], b[1]) + 44
        for s in range(13):
            t = s / 12
            x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * mx + t ** 2 * b[0]
            y = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * my + t ** 2 * b[1]
            o.append(leaf(x, y + 14, rnd.uniform(.8, 1.1), rnd.uniform(130, 230)))
        # bellotas colgando
        for t in (.3, .7):
            x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * mx + t ** 2 * b[0]
            y = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * my + t ** 2 * b[1] + 30
            o.append(f'<line x1="{x:.0f}" y1="{y - 14:.0f}" x2="{x:.0f}" y2="{y + 8:.0f}" stroke="#a87a3a" stroke-width="2"/>'
                     f'<ellipse cx="{x:.0f}" cy="{y + 26:.0f}" rx="13" ry="17" fill="#b07a48" stroke="{INK}" stroke-width="2"/>'
                     f'<path d="M{x - 15:.0f} {y + 16:.0f} q15 -16 30 0z" fill="#6b4228" stroke="{INK}" stroke-width="2"/>')
        o.append(f'<line x1="{mx}" y1="{(a[1] + b[1]) / 4 + my / 2 + 6:.0f}" x2="{mx}" y2="{(a[1] + b[1]) / 4 + my / 2 + 40:.0f}" stroke="#a87a3a" stroke-width="2.5"/>'
                 + pumpkin(mx, (a[1] + b[1]) / 4 + my / 2 + 74, 70, 54))
    for x, y in pts[1:-1]:
        o.append(wheat(x, y + 40, .45, 180))
    return ''.join(o)


def corner_tl():
    o = [wheat(40, 230, .9, 140), wheat(10, 200, .8, 120)]
    o += [leaf(40 + rnd.uniform(-30, 170), 40 + rnd.uniform(-30, 120), rnd.uniform(1.1, 1.6)) for _ in range(12)]
    o += [sunflower(170, 70, 40, 0), apple(80, 150, 24)]
    return ''.join(o)


def corner_bl():
    o = [f'<path d="M-20 1040 C40 920 200 900 320 950 C400 980 460 1000 540 1040z" fill="url(#ground)" stroke="#d9b37a" stroke-width="3"/>']
    o += [hay(30, 900, 200, 110), pumpkin(150, 880, 120, 92), pumpkin(290, 960, 90, 70, True), pumpkin(60, 990, 80, 60)]
    o += [leaf(rnd.uniform(0, 460), rnd.uniform(960, 1020), rnd.uniform(.9, 1.3)) for _ in range(12)]
    o += [corn(380, 960, .7, 60), wheat(20, 930, .8, -20)]
    return ''.join(o)


def scene_right():
    o = ['<path d="M760 880 C880 800 1020 780 1120 800 C1220 760 1380 740 1560 770 V1040 H760z" fill="#f3d9b0" opacity=".8"/>',
         '<path d="M820 900 C960 840 1100 840 1200 860 C1320 830 1450 830 1560 850 V1040 H820z" fill="#ecc890" opacity=".8"/>']
    # árboles otoñales lejanos
    for x, y, s in ((880, 820, .8), (980, 800, .65), (1460, 780, .9), (1380, 790, .6), (1530, 800, .7)):
        o.append(f'<g transform="translate({x} {y}) scale({s})" opacity=".75"><rect x="-6" y="-20" width="12" height="60" fill="#b07a48"/>'
                 f'<circle cx="0" cy="-60" r="52" fill="{rnd.choice(["#f2b06a", "#e89a5a", "#f3c26b"])}"/><circle cx="-30" cy="-40" r="30" fill="#e8a25a"/><circle cx="30" cy="-40" r="32" fill="#f0b86a"/></g>')
    # cerca de madera
    o.append('<g stroke="#4a2a14" stroke-width="3">' + ''.join(f'<rect x="{x}" y="760" width="22" height="150" rx="4" fill="url(#wood)"/>' for x in range(860, 1560, 90))
             + '<rect x="840" y="790" width="740" height="16" rx="5" fill="url(#wood)"/><rect x="840" y="850" width="740" height="16" rx="5" fill="url(#wood)"/></g>')
    o += [sunflower(1440, 640, 52, 200), sunflower(1510, 700, 44, 160), sunflower(900, 690, 40, 150)]
    o.append(f'<path d="M780 1040 C880 940 1060 910 1240 925 C1380 935 1480 910 1560 895 V1040z" fill="url(#ground)" stroke="#d9b37a" stroke-width="3"/>')
    o.append(hay(1300, 830, 220, 120))
    o.append(cornucopia(1060, 900, 1.15))
    o.append(turkey(1430, 990, 1.0))
    o += [pumpkin(1180, 990, 130, 96), pumpkin(1320, 1000, 90, 66, True), pumpkin(960, 1000, 100, 76), corn(860, 980, .8, -30), apple(1060, 1010, 26)]
    o += [leaf(rnd.uniform(800, 1530), rnd.uniform(990, 1024), rnd.uniform(.8, 1.2)) for _ in range(14)]
    return ''.join(o)


def big_tree():
    """Árbol otoñal grande a la derecha, con la copa llena de hojas."""
    o = [f'<path d="M1440 1000 C1450 820 1430 640 1460 470 C1470 420 1500 380 1540 350 L1560 360 C1540 420 1530 520 1536 640 L1560 1000z" fill="url(#wood)" stroke="{INK}" stroke-width="4"/>',
         f'<path d="M1458 560 C1400 500 1340 470 1260 470 M1452 470 C1420 400 1380 350 1320 330 M1470 640 C1420 610 1380 600 1330 610" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round"/>'
         f'<path d="M1458 560 C1400 500 1340 470 1260 470 M1452 470 C1420 400 1380 350 1320 330 M1470 640 C1420 610 1380 600 1330 610" stroke="#9a6a3c" stroke-width="15" fill="none" stroke-linecap="round"/>']
    for cx, cy, r, c in ((1300, 300, 150, '#e8902a'), (1460, 250, 170, '#d9481e'), (1200, 420, 120, '#f2b81f'), (1380, 420, 140, '#c9772f'), (1520, 440, 120, '#e8902a'), (1280, 560, 100, '#d9481e')):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r * .82:.0f}" fill="{c}" opacity=".55" filter="url(#soft)"/>')
    for _ in range(190):
        a, d = rnd.uniform(0, 6.28), rnd.uniform(0, 1) ** .6
        x, y = 1370 + math.cos(a) * 240 * d, 370 + math.sin(a) * 210 * d
        o.append(leaf(x, y, rnd.uniform(.8, 1.2)))
    return ''.join(o)


def falling():
    o = []
    for _ in range(46):
        x, y = rnd.uniform(0, W), rnd.uniform(160, H - 120)
        if 420 < x < 900 and 220 < y < 760:   # centro despejado para el contenido
            continue
        o.append(leaf(x, y, rnd.uniform(.5, .9)))
    return ''.join(o)


svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs>{defs}</defs>'
       + '<ellipse cx="1240" cy="620" rx="540" ry="560" fill="url(#sky)"/>' + big_tree() + falling() + scene_right() + corner_bl() + corner_tl() + garland_top() + '</svg>')
src = OUT / 'gracias-fiesta.svg'
src.write_text(svg, encoding='utf8')
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:{W},height:{H}}}}});
await p.goto('file://{src}');await p.screenshot({{path:'{OUT / 'gracias-fiesta.png'}',omitBackground:true}});await b.close()}})()"""
subprocess.run(['node', '-e', js], check=True, cwd='/tmp')
src.unlink()
print('Fondo de Acción de Gracias → public/theme-assets/gracias-fiesta.png')
