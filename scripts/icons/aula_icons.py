"""Biblioteca de íconos e ilustraciones propias de AulaVirtual (sin emojis).

Regla de la plataforma: ningún emoji se usa como imagen. Cada dibujo de aquí es un SVG hecho a mano
con el estilo «Cuaderno» (trazo de tinta redondeado + relleno suave).

Correr:  python3 scripts/icons/aula_icons.py
Genera:  src/lib/aula-icons.json  (lo usan la plataforma React y scripts/courseware/embed_patch.py)
"""
import json
import re
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Atajos de estilo dentro de los dibujos.
A = 'fill="currentColor" fill-opacity=".16"'          # relleno suave del color de la tinta
F = 'fill="currentColor" stroke="none"'                # relleno sólido
W = 'fill="#fff" stroke="none"'
RED, GRN, YEL, ORG, BLU, PUR = '#d64045', '#2e9e5b', '#f2b81f', '#ef8a2b', '#3b6fd8', '#8b5cf6'


def star(cx, cy, r1, r2, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i * 180 / n)
        pts.append(f'{cx + r * math.cos(a):.2f} {cy + r * math.sin(a):.2f}')
    return 'M' + 'L'.join(pts) + 'z'


def gear(cx=12, cy=12, ro=9.2, ri=7, teeth=8):
    pts = []
    step = 360 / teeth
    for i in range(teeth):
        b = i * step
        for da, r in ((-step * .22, ri), (-step * .13, ro), (step * .13, ro), (step * .22, ri)):
            a = math.radians(b + da)
            pts.append(f'{cx + r * math.cos(a):.2f} {cy + r * math.sin(a):.2f}')
    return 'M' + 'L'.join(pts) + 'z'


def spikes(cx, cy, r1, r2, n):
    return ''.join(f'M{cx + r1 * math.cos(math.radians(i * 360 / n)):.2f} {cy + r1 * math.sin(math.radians(i * 360 / n)):.2f}'
                   f'L{cx + r2 * math.cos(math.radians(i * 360 / n)):.2f} {cy + r2 * math.sin(math.radians(i * 360 / n)):.2f}' for i in range(n))


def txt(s, size=8, y=15.3):
    return (f'<text x="12" y="{y}" text-anchor="middle" font-size="{size}" font-weight="700" '
            f'font-family="Lexend,system-ui,sans-serif" fill="currentColor" stroke="none">{s}</text>')


BOOK = '<path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15H6.5A1.5 1.5 0 0 0 5 19.5z" {fill}/><path d="M5 19.5A1.5 1.5 0 0 0 6.5 21H19v-3M9 7.5h6M9 10.5h4"/>'
PAGE = f'<path d="M6 2.8h8.2L19 7.6V20a1.2 1.2 0 0 1-1.2 1.2H6A1.2 1.2 0 0 1 4.8 20V4A1.2 1.2 0 0 1 6 2.8z" {A}/><path d="M14 2.8V8h5"/>'
BUBBLE = 'M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5H11l-4.5 4v-4A2.5 2.5 0 0 1 4 13.5z'
HEART = 'M12 20.5S3 15 3 8.8A4.6 4.6 0 0 1 12 6.6a4.6 4.6 0 0 1 9 2.2C21 15 12 20.5 12 20.5z'

# ---------------------------------------------------------------------------------------------
# Íconos de línea (24×24). Toman el color del texto que los rodea.
# ---------------------------------------------------------------------------------------------
ICONS = {
    # Estados
    'ok': f'<circle cx="12" cy="12" r="9.3" fill="{GRN}" stroke="{GRN}"/><path d="M7.6 12.4l2.9 2.9 5.9-6.1" stroke="#fff" stroke-width="2.3"/>',
    'no': f'<circle cx="12" cy="12" r="9.3" fill="{RED}" stroke="{RED}"/><path d="M8.7 8.7l6.6 6.6M15.3 8.7l-6.6 6.6" stroke="#fff" stroke-width="2.3"/>',
    'checkbox': f'<rect x="3.8" y="3.8" width="16.4" height="16.4" rx="3"/><path d="M7.8 12.2l2.8 2.8 5.6-6" stroke="{GRN}" stroke-width="2.3"/>',
    'box': '<rect x="4.5" y="4.5" width="15" height="15" rx="3"/>',
    'forbid': f'<circle cx="12" cy="12" r="9.3" fill="{RED}" stroke="{RED}"/><path d="M7.3 12h9.4" stroke="#fff" stroke-width="2.6"/>',
    'stopsign': f'<path d="M8.3 2.8h7.4l5.5 5.5v7.4l-5.5 5.5H8.3l-5.5-5.5V8.3z" fill="{RED}" stroke="#9e2a2f"/><path d="M7.5 12h9" stroke="#fff" stroke-width="2.6"/>',
    'warn': f'<path d="M12 3.2l9.6 17.2H2.4z" fill="{YEL}" stroke="#b7791f"/><path d="M12 9.4v5" stroke="#3a2a10" stroke-width="2.2"/><circle cx="12" cy="17.4" r="1.2" fill="#3a2a10" stroke="none"/>',
    'siren': f'<path d="M6 18v-5a6 6 0 0 1 12 0v5" fill="{RED}" stroke="#9e2a2f"/><path d="M9.3 13a2.7 2.7 0 0 1 2.7-2.7" stroke="#fff"/><rect x="4" y="18" width="16" height="3.2" rx="1"/><path d="M12 2v2.2M4.2 5.2l1.5 1.5M19.8 5.2l-1.5 1.5M1.8 12h1.9M20.3 12h1.9"/>',
    'dot-red': f'<circle cx="12" cy="12" r="7.5" fill="{RED}" stroke="#9e2a2f"/>',
    'dot-green': f'<circle cx="12" cy="12" r="7.5" fill="{GRN}" stroke="#1f7442"/>',
    'dot-yellow': f'<circle cx="12" cy="12" r="7.5" fill="{YEL}" stroke="#b7861b"/>',
    'dot-white': '<circle cx="12" cy="12" r="7.5" fill="#fff"/>',
    'record': f'<circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" fill="{RED}" stroke="none"/>',
    'tri-red': f'<path d="M12 4.5l8 14H4z" fill="{RED}" stroke="#9e2a2f"/>',
    'question': f'<circle cx="12" cy="12" r="9.3" {A}/><path d="M9.3 9.4a2.8 2.8 0 1 1 3.9 2.6c-.8.4-1.2 1-1.2 1.9v.5"/><circle cx="12" cy="17.2" r="1.15" {F}/>',
    'doubt': f'<path d="{BUBBLE}" {A}/><path d="M9.8 7.8a2.2 2.2 0 1 1 3 2c-.6.3-.9.7-.9 1.3v.3"/><circle cx="11.9" cy="13.3" r="1" {F}/>',
    'info': f'<circle cx="12" cy="12" r="9.3" {A}/><path d="M12 11v6"/><circle cx="12" cy="7.6" r="1.2" {F}/>',
    'play': f'<path d="M7.5 4.8v14.4L19 12z" {F}/>',
    'pause': f'<path d="M7.5 5v14M16.5 5v14" stroke-width="3.2"/>',
    'stop': f'<rect x="6" y="6" width="12" height="12" rx="1.8" {F}/>',

    # Seguridad
    'lock': f'<rect x="5" y="10.5" width="14" height="10.5" rx="2.2" {A}/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3M12 14.6v2.6"/>',
    'unlock': f'<rect x="5" y="10.5" width="14" height="10.5" rx="2.2" {A}/><path d="M8 10.5V7.5a4 4 0 0 1 7.7-1.6M12 14.6v2.6"/>',
    'lockkey': f'<rect x="3.2" y="10.5" width="12" height="10" rx="2" {A}/><path d="M6 10.5V7.8a3.2 3.2 0 0 1 6.4 0v2.7M9.2 14.3v2.4"/><circle cx="18.6" cy="7" r="2.5"/><path d="M18.6 9.5v11M18.6 15.2h2.1M18.6 18h1.7"/>',
    'key': f'<circle cx="7.5" cy="12" r="4.3" {A}/><circle cx="7.5" cy="12" r="1.3"/><path d="M11.8 12H21.3M17.6 12v3.2M20.6 12v2.5"/>',
    'shield': f'<path d="M12 2.8l7.5 3v5.6c0 4.6-3.1 8.4-7.5 9.8-4.4-1.4-7.5-5.2-7.5-9.8V5.8z" {A}/><path d="M8.8 12l2.3 2.3 4.3-4.6"/>',
    'bricks': f'<rect x="3" y="4.5" width="18" height="15" rx="1.2" {A}/><path d="M3 9.5h18M3 14.5h18M9 4.5v5M15 9.5v5M9 14.5v5"/>',
    'virus': f'<circle cx="12" cy="12" r="5.6" {A}/><path d="{spikes(12, 12, 5.6, 8.8, 8)}"/>' + ''.join(
        f'<circle cx="{12 + 9.4 * math.cos(math.radians(i * 45)):.2f}" cy="{12 + 9.4 * math.sin(math.radians(i * 45)):.2f}" r="1.1" {F}/>' for i in range(8)) +
        f'<circle cx="10.3" cy="10.8" r="1" {F}/><circle cx="13.6" cy="13.4" r="1.3" {F}/>',
    'bug': f'<ellipse cx="12" cy="14" rx="6" ry="6.8" {A}/><path d="M12 7.5v13.3M9.3 4.6l1.4 2.6M14.7 4.6l-1.4 2.6M9.4 7.6a3 3 0 0 1 5.2 0M6 11H3M6 15.5H3M18 11h3M18 15.5h3"/>',
    'mask': f'<path d="M2.8 7.5c3-1.6 6.2-1.6 9.2 0 3-1.6 6.2-1.6 9.2 0-.3 5.6-2.4 9.2-5.6 9.2-1.6 0-2.9-.9-3.6-2.3-.7 1.4-2 2.3-3.6 2.3-3.2 0-5.3-3.6-5.6-9.2z" {A}/><path d="M6.3 10.5l2.8.9M17.7 10.5l-2.8.9"/>',
    'incognito': f'<path d="M3 11h18M6 11l1.5-6.3h9L18 11"/><path d="M3.7 14h6.6v1a3.3 3.3 0 0 1-6.6 0zM13.7 14h6.6v1a3.3 3.3 0 0 1-6.6 0z" fill="currentColor" fill-opacity=".8"/><path d="M10.3 14.6h3.4"/>',
    'hook': '<path d="M14.5 3.5v11a4.8 4.8 0 0 1-9.6 0v-1.8l2.7 2.4"/><circle cx="14.5" cy="3" r="1.2"/><path d="M14.5 3.5c2.5 0 4.5 1.3 5.5 3.3"/>',
    'trap': f'<rect x="3" y="13" width="18" height="7" rx="1.2" {A}/><path d="M5.5 13c0-4.5 3-7.5 6.5-7.5s6.5 3 6.5 7.5M12 13V5.5M15.5 16.5h3"/><circle cx="7.5" cy="16.5" r="1.2" {F}/>',
    'swords': '<path d="M4 3.5l12.5 12.5M20 3.5L7.5 16M14.5 18l3.5-3.5M9.5 18L6 14.5M16.8 16.8l3 3M7.2 16.8l-3 3"/><path d="M4 3.5h3.2M4 3.5v3.2M20 3.5h-3.2M20 3.5v3.2"/>',
    'castle': f'<path d="M3.5 21V7.5h3V10h3V7.5h5V10h3V7.5h3V21z" {A}/><path d="M10 21v-4.5a2 2 0 0 1 4 0V21"/>',
    'idcard': f'<rect x="2.5" y="5" width="19" height="14" rx="2" {A}/><circle cx="8.5" cy="11" r="2.2"/><path d="M5.3 16.2a3.3 3.3 0 0 1 6.4 0M14 10h4.5M14 13.5h3"/>',
    'salt': f'<path d="M8 9h8l1.2 11.5H6.8z" {A}/><path d="M8 9a4 4 0 0 1 8 0M10.5 5.3h.01M13.5 5.3h.01M12 3.8h.01" stroke-width="2"/>',
    'bot': f'<rect x="5" y="7.5" width="14" height="11" rx="3" {A}/><path d="M12 7.5V4.5M8.8 11.5l1.8 1.8M10.6 11.5l-1.8 1.8M13.4 11.5l1.8 1.8M15.2 11.5l-1.8 1.8M9.5 15.8h5M3 12v3M21 12v3"/><circle cx="12" cy="3.8" r="1" {F}/>',
    'police': f'<path d="M5 8.5l7-4 7 4-1.5 2h-11z" {A}/><path d="M7 10.5v1.5a5 5 0 0 0 10 0v-1.5M4.5 21a7.5 7.5 0 0 1 15 0"/><circle cx="12" cy="7.3" r=".9" {F}/>',

    # Libros y papeles
    'book-open': f'<path d="M12 6.5C10 4.8 7 4.3 3 4.6v13.8c4-.3 7 .2 9 1.9 2-1.7 5-2.2 9-1.9V4.6c-4-.3-7 .2-9 1.9z" {A}/><path d="M12 6.5v13.8"/>',
    'book': BOOK.format(fill=A),
    'book-blue': BOOK.format(fill=f'fill="{BLU}" fill-opacity=".35"'),
    'book-red': BOOK.format(fill=f'fill="{RED}" fill-opacity=".35"'),
    'book-green': BOOK.format(fill=f'fill="{GRN}" fill-opacity=".35"'),
    'book-yellow': BOOK.format(fill=f'fill="{YEL}" fill-opacity=".5"'),
    'books': f'<rect x="3.2" y="5" width="4.6" height="15.5" rx="1" {A}/><rect x="7.8" y="3.5" width="4.6" height="17" rx="1"/><path d="M14.3 6.3l4.4-1.1 3.4 13.7-4.4 1.1z" {A}/><path d="M3.2 8.5h4.6M7.8 7h4.6M7.8 16.5h4.6"/>',
    'notepad': f'<rect x="5" y="4" width="14" height="17" rx="2" {A}/><path d="M8.5 2.5v3M12 2.5v3M15.5 2.5v3M8.5 10h7M8.5 13.5h7M8.5 17h4"/>',
    'page': PAGE + '<path d="M8.2 12h7.6M8.2 15.2h7.6M8.2 18.4h4.6"/>',
    'memo': f'<path d="M15.5 21H5.8A1.3 1.3 0 0 1 4.5 19.7V4.3A1.3 1.3 0 0 1 5.8 3h10.4A1.3 1.3 0 0 1 17.5 4.3V8" {A}/><path d="M8 7.5h6M8 11h5M8 14.5h3"/><path d="M19.8 10.6l1.7 1.7-7.2 7.2-2.6.9.9-2.6z"/>',
    'receipt': f'<path d="M5.5 3h13v18l-2.2-1.5-2.1 1.5-2.2-1.5-2.1 1.5-2.2-1.5L5.5 21z" {A}/><path d="M8.5 8h7M8.5 11.5h7M8.5 15h4"/>',
    'scroll': f'<path d="M7 4h11.5a2 2 0 0 1 2 2v1.5h-4M7 4a2 2 0 0 0-2 2v12.5a2 2 0 0 1-2 2h11a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2" {A}/><path d="M8.5 9.5h4.5M8.5 13h4.5M8.5 16.5h3"/>',
    'clipboard': f'<rect x="5" y="4.5" width="14" height="17" rx="2" {A}/><rect x="8.5" y="2.8" width="7" height="3.6" rx="1"/><path d="M8.5 11h7M8.5 14.5h7M8.5 18h4"/>',
    'folder': f'<path d="M3 6.5A1.5 1.5 0 0 1 4.5 5h4.6l2 2.2h8.4A1.5 1.5 0 0 1 21 8.7v9.8a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z" {A}/>',
    'folder-open': f'<path d="M3 18.5V6.5A1.5 1.5 0 0 1 4.5 5h4.6l2 2.2h7.4A1.5 1.5 0 0 1 20 8.7V10"/><path d="M3 18.5l2.6-7.2A1.5 1.5 0 0 1 7 10.3h14l-2.8 8.4a1.5 1.5 0 0 1-1.4 1H4.4A1.4 1.4 0 0 1 3 18.5z" {A}/>',
    'folders': f'<path d="M6 4.5V4A1 1 0 0 1 7 3h3.4l1.6 1.5H19A1.5 1.5 0 0 1 20.5 6v9"/><path d="M3 9A1.5 1.5 0 0 1 4.5 7.5h4l1.8 2h6.7A1.5 1.5 0 0 1 18.5 11v8a1.5 1.5 0 0 1-1.5 1.5H4.5A1.5 1.5 0 0 1 3 19z" {A}/>',
    'cabinet': f'<rect x="4.5" y="3" width="15" height="18" rx="1.5" {A}/><path d="M4.5 9h15M4.5 15h15M10 6h4M10 12h4M10 18h4"/>',
    'tag': f'<path d="M3 12.6V4.5A1.5 1.5 0 0 1 4.5 3h8.1L21 11.4 12.4 20z" {A}/><circle cx="7.8" cy="7.8" r="1.6"/>',
    'bookmark': f'<path d="M6.5 3h11v18l-5.5-4-5.5 4z" {A}/>',
    'pin': f'<path d="M9 3h6l-1 6 3.2 3.5H6.8L10 9z" fill="{RED}" fill-opacity=".8" stroke="#9e2a2f"/><path d="M12 12.5V21"/>',
    'pinmap': f'<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z" fill="{RED}" fill-opacity=".85" stroke="#9e2a2f"/><circle cx="12" cy="10" r="2.3" fill="#fff" stroke="none"/>',
    'clip': '<path d="M20 11.5l-8 8a5 5 0 0 1-7-7l8.5-8.5a3.3 3.3 0 0 1 4.7 4.7L9.7 17.2a1.6 1.6 0 0 1-2.3-2.3L15 7.3"/>',
    'link': '<path d="M10 14a4 4 0 0 0 5.7 0l3.2-3.2a4 4 0 0 0-5.7-5.7l-1.4 1.4M14 10a4 4 0 0 0-5.7 0l-3.2 3.2a4 4 0 0 0 5.7 5.7l1.4-1.4"/>',
    'calendar': f'<rect x="3.5" y="5" width="17" height="15.5" rx="2" {A}/><path d="M3.5 9.5h17M8 3v4M16 3v4M7.5 13h2M11 13h2M14.5 13h2M7.5 16.5h2M11 16.5h2"/>',
    'printer': f'<path d="M7 8V3.5h10V8"/><rect x="3" y="8" width="18" height="9" rx="2" {A}/><rect x="7" y="13.5" width="10" height="7.5" rx="1" fill="#fff"/><path d="M9.5 16.5h5M9.5 18.6h3"/><circle cx="17.5" cy="10.8" r=".9" {F}/>',
    'mail': f'<rect x="3" y="5.5" width="18" height="13" rx="1.8" {A}/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>',
    'inbox': f'<path d="M3 13l2.6-6.5h3M15.4 6.5h3L21 13v5.5a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z"/><path d="M3 13h5l1.5 2.5h5L16 13h5v5.5a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z" {A}/><path d="M12 3v8M9 8.2l3 3 3-3"/>',
    'outbox': f'<path d="M3 13l2.6-6.5h3M15.4 6.5h3L21 13v5.5a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z"/><path d="M3 13h5l1.5 2.5h5L16 13h5v5.5a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z" {A}/><path d="M12 11V3M9 6l3-3 3 3"/>',
    'mail-in': f'<rect x="3" y="7" width="18" height="12.5" rx="1.8" {A}/><path d="M3.5 8l8.5 6 8.5-6M12 1.8v5M10 5l2 2 2-2"/>',
    'mailbox': f'<path d="M7 7h10a4 4 0 0 1 4 4v6.5H3V11a4 4 0 0 1 4-4z" {A}/><path d="M7 7a4 4 0 0 1 4 4v6.5M12 17.5V21M15 11V3.5h3.5V6H15"/>',

    # Herramientas
    'flask': f'<path d="M9.5 3h5M10.3 3v5.6L4.8 18.4A1.8 1.8 0 0 0 6.4 21h11.2a1.8 1.8 0 0 0 1.6-2.6l-5.5-9.8V3"/><path d="M7.2 14.5h9.6l2.4 4.1a1.6 1.6 0 0 1-1.6 2.4H6.4a1.6 1.6 0 0 1-1.6-2.4z" fill="{GRN}" fill-opacity=".35" stroke="none"/><circle cx="10.5" cy="17.5" r=".9" {F}/><circle cx="13.5" cy="16" r=".7" {F}/>',
    'tools': f'<path d="M3 7.3l4-4 3.3 3.3-1.4 1.4 1.4 1.4-1.6 1.6-1.4-1.4-1.3 1.3z" {A}/><path d="M9.8 9.8l10 10" stroke-width="2.3"/><path d="M20.6 6.3a3.6 3.6 0 0 1-4.7 4.4L6.2 20.4a1.5 1.5 0 0 1-2.1-2.1l9.7-9.7a3.6 3.6 0 0 1 4.4-4.7l-2.1 2.1.4 2 2 .4z"/>',
    'wrench': f'<path d="M14.5 3.5a5 5 0 0 0-4.8 6.5L3.6 16.1a2.1 2.1 0 0 0 3 3l6.1-6.1a5 5 0 0 0 6.5-4.8l-3 3-3.1-.6-.6-3.1z" {A}/>',
    'toolbox': f'<rect x="3" y="8" width="18" height="12" rx="2" {A}/><path d="M9 8V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V8M3 13h18M9.5 12v2.5M14.5 12v2.5"/>',
    'gear': f'<path d="{gear()}" {A}/><circle cx="12" cy="12" r="3"/>',
    'sliders': f'<path d="M4 6h9M17 6h3M4 12h3M11 12h9M4 18h11M19 18h1"/><circle cx="15" cy="6" r="2" {A}/><circle cx="9" cy="12" r="2" {A}/><circle cx="17" cy="18" r="2" {A}/>',
    'pencil': f'<path d="M16.5 3.5l4 4L8 20H4v-4z" fill="{YEL}" fill-opacity=".55"/><path d="M14 6l4 4M4 16l4 4"/>',
    'pen-hand': f'<path d="M15.5 3.5l4 4L9 18l-5 1.2L5.2 14z" fill="{BLU}" fill-opacity=".25"/><path d="M13.3 5.7l4 4M3 22h18"/>',
    'scissors': '<circle cx="6" cy="7" r="2.8"/><circle cx="6" cy="17" r="2.8"/><path d="M8.3 8.6L20 18M8.3 15.4L20 6"/>',
    'ruler': f'<path d="M3 16.5L16.5 3 21 7.5 7.5 21z" fill="{YEL}" fill-opacity=".45"/><path d="M7 12.5l2 2M9.5 10l1.4 1.4M12 7.5l2 2M14.5 5l1.4 1.4"/>',
    'setsquare': f'<path d="M4 20V4l16 16z" fill="{YEL}" fill-opacity=".45"/><path d="M8 16v-4.3l4.3 4.3zM4 8h2M4 12h2M4 16h2"/>',
    'palette': f'<path d="M12 3a9 9 0 0 0 0 18c1.4 0 2-1 2-1.9 0-1.4-1.2-1.6-1.2-2.8 0-1 .8-1.8 1.8-1.8H17a4 4 0 0 0 4-4C21 6.6 17 3 12 3z" {A}/><circle cx="7.5" cy="11" r="1.4" fill="{RED}" stroke="none"/><circle cx="9.8" cy="7" r="1.4" fill="{YEL}" stroke="none"/><circle cx="14.5" cy="6.6" r="1.4" fill="{GRN}" stroke="none"/><circle cx="17.6" cy="10" r="1.4" fill="{BLU}" stroke="none"/>',
    'calculator': f'<rect x="5" y="2.8" width="14" height="18.4" rx="2" {A}/><rect x="7.8" y="5.6" width="8.4" height="3.6" rx=".6"/><path d="M8.3 12.6h.01M12 12.6h.01M15.7 12.6h.01M8.3 15.6h.01M12 15.6h.01M15.7 15.6h.01M8.3 18.5h.01M12 18.5h3.7" stroke-width="2.2"/>',
    'magnet': f'<path d="M5 3.5h4.5v8a2.5 2.5 0 0 0 5 0v-8H19v8a7 7 0 0 1-14 0z" {A}/><path d="M5 7.5h4.5M14.5 7.5H19" stroke="{RED}"/>',
    'extinguisher': f'<rect x="7.5" y="8" width="8" height="13.5" rx="3" fill="{RED}" stroke="#9e2a2f"/><path d="M11.5 8V4.5M9 4.5h5.5l3.5-1.5M14.5 4.5l2.5 3"/><path d="M9.5 13h4" stroke="#fff"/>',
    'broom': f'<path d="M19.5 3L12 10.5"/><path d="M12 10.5l-2-1.5-6 6 5 5 6-6z" fill="{YEL}" fill-opacity=".45"/><path d="M6.5 17.5L9 15M8.7 19.7l2.6-2.6"/>',
    'sponge': f'<rect x="3" y="7" width="18" height="10" rx="3" fill="{YEL}" fill-opacity=".5"/><circle cx="7.5" cy="11" r="1" {F}/><circle cx="12" cy="13.5" r="1.2" {F}/><circle cx="16.5" cy="10.5" r=".9" {F}/>',
    'wand': f'<path d="M4 20L15 9"/><path d="{star(17.5, 6.5, 4, 1.7, 4, -90)}" fill="{YEL}" stroke="#b7861b"/>',
    'ladder': '<path d="M7 3v18M17 3v18M7 7h10M7 11.5h10M7 16h10"/>',
    'stethoscope': f'<path d="M5 3.5v5a4.5 4.5 0 0 0 9 0v-5M9.5 13v2.5a4.5 4.5 0 0 0 9 0V13"/><circle cx="18.5" cy="11" r="2" {A}/>',
    'bandage': f'<rect x="2.5" y="8" width="19" height="8" rx="4" transform="rotate(-35 12 12)" fill="{YEL}" fill-opacity=".4"/><circle cx="11" cy="12.2" r=".8" {F}/><circle cx="13" cy="11.2" r=".8" {F}/><circle cx="12.4" cy="13.4" r=".8" {F}/>',

    # Datos, cálculo y escritura
    'numbers': f'<rect x="2.8" y="4" width="18.4" height="16" rx="3" {A}/>' + txt('123', 7.6),
    'letters': f'<rect x="2.8" y="4" width="18.4" height="16" rx="3" {A}/>' + txt('abc', 7.6, 14.6),
    'letters-up': f'<rect x="2.8" y="4" width="18.4" height="16" rx="3" {A}/>' + txt('ABC', 7.2),
    'symbols': f'<rect x="2.8" y="4" width="18.4" height="16" rx="3" {A}/>' + txt('#&amp;%', 7.2),
    'ten': f'<rect x="2.8" y="4" width="18.4" height="16" rx="3" {A}/>' + txt('10', 8.5, 15.6),
    'plus': '<path d="M12 4.5v15M4.5 12h15" stroke-width="2.6"/>',
    'minus': '<path d="M4.5 12h15" stroke-width="2.6"/>',
    'times': '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11" stroke-width="2.6"/>',
    'divide': f'<path d="M4.5 12h15" stroke-width="2.6"/><circle cx="12" cy="6.3" r="1.7" {F}/><circle cx="12" cy="17.7" r="1.7" {F}/>',
    'asterisk': '<path d="M12 4v16M4.5 8l15 8M19.5 8l-15 8" stroke-width="2.2"/>',
    'dollar': '<path d="M16 7.5a3.8 3.8 0 0 0-4-2.3c-2.4 0-3.8 1.3-3.8 3 0 4 7.8 2.3 7.8 6.4 0 1.8-1.6 3.2-4 3.2a4.3 4.3 0 0 1-4.3-2.5M12 3v18" stroke-width="2"/>',
    'barchart': f'<path d="M3.5 20.5h17"/><rect x="5" y="12" width="3.4" height="8.5" rx=".6" fill="{BLU}" fill-opacity=".4"/><rect x="10.3" y="6.5" width="3.4" height="14" rx=".6" fill="{GRN}" fill-opacity=".4"/><rect x="15.6" y="9.5" width="3.4" height="11" rx=".6" fill="{YEL}" fill-opacity=".55"/>',
    'linechart': f'<path d="M3.5 3.5v17h17"/><path d="M6.5 16l4-4.5 3 2.5 5.5-6.5" stroke="{GRN}" stroke-width="2"/><path d="M15.5 7.5h3.5V11" stroke="{GRN}" stroke-width="2"/>',
    'piechart': f'<path d="M10.8 3.6a8.6 8.6 0 1 0 9.6 9.6h-9.6z" fill="{BLU}" fill-opacity=".35"/><path d="M14 2.6V10h7.4A7.5 7.5 0 0 0 14 2.6z" fill="{YEL}" fill-opacity=".6"/>',
    'areachart': f'<path d="M3.5 3.5v17h17"/><path d="M4 19.5l5-7.5 3.5 4.5 3-3.5 4.5 6.5z" fill="{GRN}" fill-opacity=".35"/>',
    'scatter': f'<path d="M3.5 3.5v17h17"/><circle cx="8" cy="15" r="1.5" {F}/><circle cx="11" cy="11" r="1.5" {F}/><circle cx="14.5" cy="13" r="1.5" {F}/><circle cx="17" cy="7" r="1.5" {F}/>',
    'abacus-calc': f'<rect x="3.5" y="3.5" width="17" height="17" rx="2" {A}/><path d="M3.5 9h17M3.5 15h17"/><circle cx="8" cy="9" r="1.6" fill="{RED}" stroke="none"/><circle cx="12.5" cy="9" r="1.6" fill="{RED}" stroke="none"/><circle cx="10" cy="15" r="1.6" fill="{BLU}" stroke="none"/><circle cx="16" cy="15" r="1.6" fill="{BLU}" stroke="none"/>',
    'puzzle': f'<path d="M4.5 6.5h3.4a2.3 2.3 0 1 1 4.6 0h3.4v3.4a2.3 2.3 0 1 1 0 4.6v3.9h-3.4a2.3 2.3 0 1 0-4.6 0H4.5v-3.9a2.3 2.3 0 1 0 0-4.6z" fill="{BLU}" fill-opacity=".25"/>',
    'target': f'<circle cx="12" cy="12" r="9" {A}/><circle cx="12" cy="12" r="5.5"/><circle cx="12" cy="12" r="2" fill="{RED}" stroke="{RED}"/>',
    'search': f'<circle cx="10.5" cy="10.5" r="6.5" {A}/><path d="M15.4 15.4L21 21" stroke-width="2.6"/>',
    'compass': f'<circle cx="12" cy="12" r="9" {A}/><path d="M15.6 8.4l-2.2 5-5 2.2 2.2-5z"/><path d="M15.6 8.4l-5 2.2 2.8 2.8z" fill="{RED}" stroke="none"/>',
    'map': f'<path d="M3 6l6-2.5 6 2.5 6-2.5v14.5l-6 2.5-6-2.5-6 2.5z" {A}/><path d="M9 3.5v14.5M15 6v14.5"/>',
    'route': f'<circle cx="6" cy="18" r="2.5" {A}/><circle cx="18" cy="6" r="2.5" {A}/><path d="M8.5 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.5" stroke-dasharray="2.2 2.4"/>',
    'brain': f'<path d="M12 5.2a3 3 0 0 0-5.6-1.3 3.2 3.2 0 0 0-2.6 4.2 3.4 3.4 0 0 0 .4 5.6A3.3 3.3 0 0 0 7.5 18a3 3 0 0 0 4.5 1.6zM12 5.2a3 3 0 0 1 5.6-1.3 3.2 3.2 0 0 1 2.6 4.2 3.4 3.4 0 0 1-.4 5.6 3.3 3.3 0 0 1-3.3 4.3A3 3 0 0 1 12 19.6z" fill="#e88aa8" fill-opacity=".35"/><path d="M12 5.2v14.4M8.2 9.5a2 2 0 0 1 2 2M15.8 9.5a2 2 0 0 0-2 2M7.8 14.5h2M14.2 14.5h2"/>',
    'bulb': f'<path d="M9 17.5h6M10 20.5h4M12 3a6 6 0 0 0-3.6 10.8c.6.5 1 1.2 1 2V16h5.2v-.2c0-.8.4-1.5 1-2A6 6 0 0 0 12 3z" fill="#ffe14d" stroke="currentColor"/>',
    'scales': f'<path d="M12 3.5v17M7 20.5h10M4.5 7h15"/><path d="M6.5 7l-3 6.5a3 3 0 0 0 6 0zM17.5 7l-3 6.5a3 3 0 0 0 6 0z" {A}/>',
    'shuffle': '<path d="M3 7h3.5c4.5 0 6.5 10 11 10H21M3 17h3.5c1.8 0 3.1-1.6 4.2-3.7M13.3 9.7C14.4 8.2 15.6 7 17.5 7H21M18.5 4.5L21 7l-2.5 2.5M18.5 14.5L21 17l-2.5 2.5"/>',
    'refresh': '<path d="M20 11a8 8 0 0 0-14.3-4.6L4 8.3M4 13a8 8 0 0 0 14.3 4.6l1.7-1.9"/><path d="M4 3.8v4.5h4.5M20 20.2v-4.5h-4.5"/>',
    'arrows-ud': '<path d="M8 3.5v17M4.5 7L8 3.5 11.5 7M16 20.5v-17M12.5 17l3.5 3.5 3.5-3.5"/>',
    'dna': f'<path d="M7 2.5c0 5 10 5 10 9.5s-10 4.5-10 9.5M17 2.5c0 5-10 5-10 9.5s10 4.5 10 9.5"/><path d="M8.5 6h7M10 9.5h4M10 14.5h4M8.5 18h7" stroke="{BLU}"/>',
    'layers': f'<path d="M12 3.5l9 4.5-9 4.5-9-4.5z" {A}/><path d="M3 12l9 4.5 9-4.5M3 16l9 4.5 9-4.5"/>',
    'onion': f'<path d="M12 3c-.5 2-6.5 5-6.5 10.5A6.5 6.5 0 0 0 12 20a6.5 6.5 0 0 0 6.5-6.5C18.5 8 12.5 5 12 3z" fill="#c79bd6" fill-opacity=".35"/><path d="M12 6.5c-2.2 2.4-3.4 4.7-3.4 7.2A3.4 3.4 0 0 0 12 17a3.4 3.4 0 0 0 3.4-3.3c0-2.5-1.2-4.8-3.4-7.2zM12 9.5V17"/>',

    # Equipos y redes
    'monitor': f'<rect x="2.8" y="3.5" width="18.4" height="12.5" rx="1.6" {A}/><path d="M9 20.5h6M12 16v4.5"/>',
    'laptop': f'<rect x="4.5" y="4.5" width="15" height="10.5" rx="1.4" {A}/><path d="M2.5 18.5h19M4.5 15l-2 3.5M19.5 15l2 3.5"/>',
    'phone': f'<rect x="6.5" y="2.5" width="11" height="19" rx="2.2" {A}/><path d="M10.5 18.3h3"/>',
    'telephone': f'<path d="M5 3.5h3.3l1.6 4.2-2.1 1.5a11 11 0 0 0 7 7l1.5-2.1 4.2 1.6V19a1.7 1.7 0 0 1-1.8 1.7C10.4 20.2 3.8 13.6 3.3 5.3A1.7 1.7 0 0 1 5 3.5z" {A}/>',
    'network': f'<rect x="9" y="3" width="6" height="5" rx="1"/><rect x="2.5" y="15.5" width="6" height="5" rx="1" {A}/><rect x="15.5" y="15.5" width="6" height="5" rx="1" {A}/><path d="M12 8v4M5.5 15.5V12h13v3.5"/>',
    'floppy': f'<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3h11L21 7.5v11a1.5 1.5 0 0 1-1.5 1.5h-14A1.5 1.5 0 0 1 4 18.5z" {A}/><path d="M7.5 3v5h8V3M7.5 20v-6h9v6"/>',
    'disc': f'<circle cx="12" cy="12" r="9" {A}/><circle cx="12" cy="12" r="2.6"/><path d="M12 5.6a6.4 6.4 0 0 1 6.4 6.4" opacity=".55"/>',
    'hdd': f'<rect x="3" y="4" width="18" height="16" rx="2.2" {A}/><circle cx="12" cy="11" r="4.2"/><circle cx="12" cy="11" r="1" {F}/><path d="M15 17h3M12 11l4.5 4"/>',
    'mouse': f'<rect x="6.5" y="3" width="11" height="18" rx="5.5" {A}/><path d="M12 3v6M6.5 9h11"/>',
    'pointer': f'<path d="M6 3l12 7.5-5.2 1.5 3.2 6.2-2.4 1.2-3.2-6.3L6.5 17z" {A}/>',
    'plug': f'<path d="M9 2.5v4M15 2.5v4M6.5 6.5h11v3.5a5.5 5.5 0 0 1-11 0z" {A}/><path d="M12 15.5v6"/>',
    'bolt': f'<path d="M13.5 2.5L5 13.5h6l-1.5 8 8.5-11h-6z" fill="{YEL}" stroke="#b7861b"/>',
    'battery': f'<rect x="2.5" y="7" width="17" height="10" rx="2"/><path d="M21.5 10.5v3"/><rect x="5" y="9.5" width="8" height="5" rx=".8" fill="{GRN}" stroke="none"/>',
    'globe': f'<circle cx="12" cy="12" r="9" {A}/><path d="M3 12h18M12 3c2.5 2.6 3.7 5.6 3.7 9s-1.2 6.4-3.7 9c-2.5-2.6-3.7-5.6-3.7-9S9.5 5.6 12 3z"/>',
    'antenna': f'<path d="M4.5 9.5a8 8 0 0 0 10 10z" {A}/><path d="M9.5 14.5l4-4M14.5 3.5a6 6 0 0 1 6 6M14.5 7a2.5 2.5 0 0 1 2.5 2.5M6 21h6"/>',
    'signal': f'<path d="M5 20v-3M9.7 20v-6.5M14.3 20V10M19 20V6.5" stroke-width="2.8"/>',
    'window': f'<rect x="4" y="3.5" width="16" height="17" rx="1.2" fill="{BLU}" fill-opacity=".18"/><path d="M12 3.5v17M4 12h16"/>',
    'image': f'<rect x="3" y="4.5" width="18" height="15" rx="1.8" {A}/><circle cx="8.5" cy="9.5" r="1.7" fill="{YEL}" stroke="none"/><path d="M3.5 17.5l5-4.5 3.5 3 3-2.5 5.5 4.5"/>',
    'camera': f'<path d="M3 8.5A1.5 1.5 0 0 1 4.5 7h3l1.6-2.5h5.8L16.5 7h3A1.5 1.5 0 0 1 21 8.5v10a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z" {A}/><circle cx="12" cy="13" r="3.6"/>',
    'video': f'<rect x="2.5" y="6.5" width="13" height="11" rx="2" {A}/><path d="M15.5 10.5l6-3.5v10l-6-3.5z"/>',
    'clapper': f'<path d="M3.5 10h17v9a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 19z" {A}/><path d="M3.5 10l-.6-3.3 15.7-3 .6 3.3zM7.3 5.8l2.3 3.1M11.6 5l2.3 3.1M15.9 4.2l2.3 3.1"/>',
    'mic': f'<rect x="9" y="2.8" width="6" height="11" rx="3" {A}/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5v3.5M8.5 21h7"/>',
    'headphones': f'<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4.5" height="6.5" rx="1.5" {A}/><rect x="16.5" y="14" width="4.5" height="6.5" rx="1.5" {A}/>',
    'speaker': f'<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" {A}/><path d="M15.5 9a4 4 0 0 1 0 6M18.3 6.3a7.6 7.6 0 0 1 0 11.4"/>',
    'megaphone': f'<path d="M3.5 10v4h3l8 4.5v-13l-8 4.5z" {A}/><path d="M6.5 14l1.2 5.5h2.5l-1-5M18 9a4 4 0 0 1 0 6M20.3 6.7a7.3 7.3 0 0 1 0 10.6"/>',
    'music': f'<path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.5" {A}/><circle cx="17.5" cy="16" r="2.5" {A}/>',
    'bell': f'<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2h-15z" {A}/><path d="M10 20.5a2 2 0 0 0 4 0M12 3v2"/>',
    'clock': f'<circle cx="12" cy="12" r="9" {A}/><path d="M12 7v5H8.5"/>',
    'alarm': f'<circle cx="12" cy="13" r="7.5" {A}/><path d="M12 9v4.2l2.7 1.8M3.5 6l3-2.8M20.5 6l-3-2.8M6.5 19.5L5 21M17.5 19.5L19 21"/>',
    'stopwatch': f'<circle cx="12" cy="13.5" r="7.5" {A}/><path d="M10 2.5h4M12 2.5V6M12 13.5l3-3M18.5 6.5l1.3-1.3"/>',
    'sleep': txt('Zz', 11, 16.5),

    # Lugares y personas
    'school': f'<path d="M3.5 21V10.5L12 5l8.5 5.5V21" {A}/><path d="M2 21h20M9.5 21v-5h5v5M12 5V2.5h3"/><circle cx="12" cy="11.2" r="1.9"/>',
    'building': f'<rect x="5" y="3" width="14" height="18" rx="1" {A}/><path d="M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1" stroke-width="2"/><path d="M10.5 21v-3h3v3M3 21h18"/>',
    'classic': f'<path d="M3 9.5L12 4l9 5.5z" {A}/><path d="M5 10.5v7.5M9.7 10.5v7.5M14.3 10.5v7.5M19 10.5v7.5M3 20.5h18"/>',
    'store': f'<path d="M3.5 9.5L5 4h14l1.5 5.5"/><path d="M3.5 9.5a2.1 2.1 0 0 0 4.2 0 2.1 2.1 0 0 0 4.3 0 2.1 2.1 0 0 0 4.3 0 2.1 2.1 0 0 0 4.2 0z" fill="{RED}" fill-opacity=".35"/><path d="M5 11.5v9h14v-9M10 20.5v-5h4v5"/>',
    'house': f'<path d="M3.5 11L12 3.8l8.5 7.2"/><path d="M5.5 9.5v11h13v-11" {A}/><path d="M10 20.5v-6h4v6"/>',
    'hospital': f'<rect x="4" y="5" width="16" height="16" rx="1.2" {A}/><path d="M2.5 21h19M10.5 21v-3.5h3V21"/><path d="M12 8v6M9 11h6" stroke="{RED}" stroke-width="2.2"/>',
    'door': f'<path d="M5 21V4.5A1.5 1.5 0 0 1 6.5 3h11A1.5 1.5 0 0 1 19 4.5V21" {A}/><path d="M3 21h18"/><circle cx="15" cy="12.5" r="1" {F}/>',
    'hole': '<ellipse cx="12" cy="14" rx="9" ry="4.5" fill="#1d2433" stroke="currentColor"/><path d="M5 11.5c1.5-1.3 4-2 7-2s5.5.7 7 2" opacity=".5"/>',
    'tree': f'<path d="M12 21v-6"/><path d="M12 2.8a5 5 0 0 0-5 5 4.4 4.4 0 0 0-1.5 7.7h13A4.4 4.4 0 0 0 17 7.8a5 5 0 0 0-5-5z" fill="{GRN}" fill-opacity=".35"/>',
    'pine': f'<path d="M12 2.5l5 6h-2.5l4 5.5h-3l3.5 4.5h-14L8.5 14h-3l4-5.5H7z" fill="{GRN}" fill-opacity=".35"/><path d="M12 18.5V21.5"/>',
    'mountain': f'<path d="M2.5 19.5l6.5-11 4 6 2.5-3.5 6 8.5z" {A}/>',
    'sunrise': f'<path d="M2.5 18h19M5 21.5h14M7 18a5 5 0 0 1 10 0M12 7.5v3M5.5 11l1.8 1.5M18.5 11l-1.8 1.5"/><path d="M7 18a5 5 0 0 1 10 0z" fill="{YEL}" fill-opacity=".6" stroke="none"/>',
    'wave': '<path d="M2.5 9c2.4 0 2.4-2 4.75-2S9.6 9 12 9s2.4-2 4.75-2S19.1 9 21.5 9M2.5 15c2.4 0 2.4-2 4.75-2S9.6 15 12 15s2.4-2 4.75-2 2.35 2 4.75 2"/>',
    'cloud': f'<path d="M7 18.5a4.5 4.5 0 0 1-.6-9 6 6 0 0 1 11.4 1.6A3.8 3.8 0 0 1 17.5 18.5z" {A}/>',
    'tornado': '<path d="M3 4.5h18M5 9h14M7.5 13.5h9M9.5 18h5M11.3 21.5h1.5"/>',
    'fire': f'<path d="M12 21.5c-4 0-7-2.8-7-6.6 0-3.3 2.3-5.4 3.5-7.6.5 1.4 1.3 2.5 2.4 3C10.6 7 12 4.5 14.5 2.5c.2 3.4 4.5 6 4.5 11 0 4.6-3 8-7 8z" fill="{ORG}" stroke="#c4561d"/><path d="M12 21.5c-1.9 0-3.2-1.4-3.2-3.2 0-2 1.6-3 2.4-4.6 1 1.2 4 2.4 4 4.8 0 1.7-1.3 3-3.2 3z" fill="{YEL}" stroke="none"/>',
    'boom': f'<path d="{star(12, 12, 10, 5, 9, -90)}" fill="{ORG}" stroke="#c4561d"/><path d="{star(12, 12, 5.5, 2.8, 9, -70)}" fill="{YEL}" stroke="none"/>',
    'user': f'<circle cx="12" cy="8" r="3.8" {A}/><path d="M4.5 20.5v-1A5.5 5.5 0 0 1 10 14h4a5.5 5.5 0 0 1 5.5 5.5v1"/>',
    'users': f'<circle cx="9" cy="8" r="3.3" {A}/><path d="M2.8 20v-1.3A5 5 0 0 1 7.8 13.7h2.4a5 5 0 0 1 5 5V20"/><path d="M15.5 4.9a3.3 3.3 0 0 1 0 6.3M18 13.9a5 5 0 0 1 3.2 4.7V20"/>',
    'teacher': f'<rect x="9.5" y="3" width="12" height="8.5" rx="1.2" {A}/><path d="M12.5 6.3h6M12.5 8.6h3.5"/><circle cx="6" cy="8" r="2.6"/><path d="M1.8 21v-3.3A4.2 4.2 0 0 1 6 13.5h1.2l4.8-3.5M8 13.6V21"/>',
    'coder': f'<circle cx="7.5" cy="7" r="2.8" {A}/><path d="M2.5 19.5v-1.5a4.5 4.5 0 0 1 4.5-4.5h1a4.5 4.5 0 0 1 4.5 4.5v1.5"/><rect x="13" y="8" width="8.5" height="6.5" rx="1"/><path d="M11.5 17.5h11M15.5 10.5l-1 1 1 1M19 10.5l1 1-1 1"/>',
    'handshake': '<path d="M2 8.5L6 5l4 2h2.5l-3.7 3.4a1.4 1.4 0 0 0 2 2l2.7-2.4 5.3 5L16.5 17.3"/><path d="M22 8.5L18 5l-3 1.5M5 13.8l3.6 3.6M7.8 12.4l4.2 4.2M11 16.3l2 2"/>',
    'thumbsup': f'<path d="M7 10.5v10H4a1 1 0 0 1-1-1v-8a1 1 0 0 1 1-1z" {A}/><path d="M7 10.5l4-7.5a2.2 2.2 0 0 1 2.4 2.6L12.8 9H19a2 2 0 0 1 2 2.4l-1.5 7.5a2 2 0 0 1-2 1.6H7"/>',
    'medal': f'<path d="M8 2.5l2.5 6M16 2.5l-2.5 6" stroke="{BLU}" stroke-width="2.4"/><circle cx="12" cy="15" r="6" fill="{YEL}" stroke="#b7861b"/><path d="{star(12, 15, 3.2, 1.4)}" fill="#fff" stroke="none"/>',
    'crown': f'<path d="M3 8l4 4 5-6.5 5 6.5 4-4-1.8 10.5H4.8z" fill="{YEL}" stroke="#b7861b"/><path d="M5 20.5h14" stroke="#b7861b"/>',
    'pawn': f'<circle cx="12" cy="6" r="2.8" {A}/><path d="M9.5 9.5h5l-1 6h-3zM7 20.5l1.2-5h7.6l1.2 5z" {A}/>',
    'flag': f'<path d="M5 21V3.5"/><path d="M5 4h13l-2.5 4.5L18 13H5z" fill="{RED}" fill-opacity=".55"/>',
    'finish': f'<path d="M5 21V3.5"/><path d="M5 4h14v9H5z" fill="#fff"/><path d="M5 4h3.5v3H5zM12 4h3.5v3H12zM8.5 7H12v3H8.5zM15.5 7H19v3h-3.5zM5 10h3.5v3H5zM12 10h3.5v3H12z" {F}/>',
    'smile': f'<circle cx="12" cy="12" r="9" fill="{YEL}" fill-opacity=".55"/><path d="M8 14a4.5 4.5 0 0 0 8 0"/><circle cx="9" cy="9.5" r="1.1" {F}/><circle cx="15" cy="9.5" r="1.1" {F}/>',
    'gradcap': f'<path d="M12 4.5L2 9.5l10 5 10-5z" {A}/><path d="M6 11.5v4.5c0 1.5 2.7 3 6 3s6-1.5 6-3v-4.5M22 9.5v6"/>',
    'heart-blue': f'<path d="{HEART}" fill="{BLU}" stroke="#2b56b0"/>',
    'heart-purple': f'<path d="{HEART}" fill="{PUR}" stroke="#6b3fd6"/>',
    'star': f'<path d="{star(12, 12.4, 9.5, 4.1)}" fill="{YEL}" stroke="#b7861b"/>',
    'sparkles': f'<path d="{star(10, 10.5, 7.2, 2.2, 4)}" fill="{YEL}" stroke="#b7861b"/><path d="{star(18.3, 17.8, 3.6, 1.2, 4)}" fill="{YEL}" stroke="#b7861b" stroke-width="1.2"/><path d="{star(18.5, 4.8, 2.4, .8, 4)}" fill="{YEL}" stroke="none"/>',
    'coffee': f'<path d="M4 9h12v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z" {A}/><path d="M16 11h1.5a2.5 2.5 0 0 1 0 5H16M8 2.8c-.8 1.2.8 2 0 3.4M12 2.8c-.8 1.2.8 2 0 3.4"/>',
    'ribbon': f'<path d="M12 10.5L4.5 6.5v8zM12 10.5l7.5-4v8z" fill="#e8669a" fill-opacity=".45"/><circle cx="12" cy="10.5" r="1.9" fill="#e8669a"/><path d="M11 12.3L8.5 20M13 12.3l2.5 7.7"/>',
    'sunglasses': f'<path d="M2.5 9.5h19"/><path d="M3.5 9.5h7v2.5a3 3 0 0 1-3 3h-1a3 3 0 0 1-3-3zM13.5 9.5h7v2.5a3 3 0 0 1-3 3h-1a3 3 0 0 1-3-3z" fill="currentColor" fill-opacity=".85"/>',
    'traffic': f'<rect x="8" y="2.5" width="8" height="19" rx="2.5" {A}/><circle cx="12" cy="7" r="1.8" fill="{RED}" stroke="none"/><circle cx="12" cy="12" r="1.8" fill="{YEL}" stroke="none"/><circle cx="12" cy="17" r="1.8" fill="{GRN}" stroke="none"/>',
    'gift-line': f'<rect x="3.5" y="8" width="17" height="4" rx="1" {A}/><path d="M5 12v8.5h14V12M12 8v12.5M12 8C10 4 6.5 4.5 7.5 7c.4 1 2.8 1 4.5 1zM12 8c2-4 5.5-3.5 4.5-1-.4 1-2.8 1-4.5 1z"/>',
    'rocket-line': f'<path d="M12 2.5c3.5 2.3 5 6 4.5 10.5l-2 2.5h-5l-2-2.5C7 8.5 8.5 4.8 12 2.5z" {A}/><circle cx="12" cy="9" r="1.8"/><path d="M7.5 13l-3 3 1 3.5 3.5-2.5M16.5 13l3 3-1 3.5-3.5-2.5"/><path d="M10.5 18.5L12 21.5l1.5-3" stroke="{ORG}"/>',
    'package': f'<path d="M3.5 7.5L12 3l8.5 4.5v9L12 21l-8.5-4.5z" fill="#c8915a" fill-opacity=".35"/><path d="M3.5 7.5L12 12l8.5-4.5M12 12v9M7.8 5.2l8.5 4.6"/>',
    'truck': f'<path d="M2.5 6h11v10h-11z" {A}/><path d="M13.5 9.5h4L21 13v3h-7.5"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    'wheel': f'<circle cx="12" cy="12" r="9" fill="#1d2433" fill-opacity=".85"/><circle cx="12" cy="12" r="4.5" fill="#c9ced8" stroke="none"/><circle cx="12" cy="12" r="1.3" {F}/>',
    'ferris': f'<circle cx="12" cy="10" r="7"/><path d="{spikes(12, 10, 0, 7, 8)}M8 21l4-11 4 11M6 21h12"/>',
    'pot': f'<path d="M4 11h16v4a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z" {A}/><path d="M2.5 11h19M9 7.5c-.6-1 .6-1.8 0-3M12 7.5c-.6-1 .6-1.8 0-3M15 7.5c-.6-1 .6-1.8 0-3"/>',
    'snake': f'<path d="M3 19.5c3 0 3.5-2 6-2s3 2 5 2c2.6 0 4-2 4-4.5S16 11 13.5 11h-5C6.5 11 5 9.6 5 7.6S6.6 4 8.6 4H15" stroke="{GRN}" stroke-width="2.6"/><circle cx="17" cy="4" r="2.3" fill="{GRN}" stroke="none"/><circle cx="17.6" cy="3.5" r=".6" fill="#fff" stroke="none"/>',
    'penguin': '<path d="M12 2.8c-3.2 0-5 2.6-5 6.2 0 2-1.8 3.5-2.4 6.3-.7 3.4 2.4 5.9 7.4 5.9s8.1-2.5 7.4-5.9C18.8 12.5 17 11 17 9c0-3.6-1.8-6.2-5-6.2z" fill="#1d2433" stroke="#1d2433"/><path d="M12 9.3c-2.3 0-3.6 2.2-3.6 5.3 0 3 1.6 4.8 3.6 4.8s3.6-1.8 3.6-4.8c0-3.1-1.3-5.3-3.6-5.3z" fill="#fff" stroke="none"/><path d="M10.6 9.5l1.4 1.6 1.4-1.6z" fill="#f2b81f" stroke="#c98f0e" stroke-width=".8"/><circle cx="10.4" cy="7.1" r=".85" fill="#fff" stroke="none"/><circle cx="13.6" cy="7.1" r=".85" fill="#fff" stroke="none"/><path d="M8.6 21.2h2.6M12.8 21.2h2.6" stroke="#f2b81f" stroke-width="1.8"/>',
    'cassette': f'<rect x="2.5" y="5.5" width="19" height="13" rx="1.8" {A}/><circle cx="8.5" cy="11" r="1.8"/><circle cx="15.5" cy="11" r="1.8"/><path d="M8.5 12.8h7M6.5 18.5l1.5-3h8l1.5 3"/>',
}

# ---------------------------------------------------------------------------------------------
# Ilustraciones a color (48×48) para temas y temporadas. Contorno de tinta + colores planos.
# ---------------------------------------------------------------------------------------------
INK = '#2b2238'
S = f'stroke="{INK}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"'


def petals(cx, cy, n, rx, ry, dist, fill, rot=0):
    return ''.join(f'<ellipse cx="{cx}" cy="{cy - dist}" rx="{rx}" ry="{ry}" fill="{fill}" {S} transform="rotate({rot + i * 360 / n:.1f} {cx} {cy})"/>' for i in range(n))


def flake(cx, cy, r, color='#7fb8e6', w=2.2):
    arms = ''
    for i in range(6):
        a = math.radians(i * 60 - 90)
        x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        mx, my = cx + r * .58 * math.cos(a), cy + r * .58 * math.sin(a)
        b1, b2 = a + math.radians(35), a - math.radians(35)
        arms += (f'M{cx} {cy}L{x2:.2f} {y2:.2f}'
                 f'M{mx:.2f} {my:.2f}L{mx + r * .3 * math.cos(b1):.2f} {my + r * .3 * math.sin(b1):.2f}'
                 f'M{mx:.2f} {my:.2f}L{mx + r * .3 * math.cos(b2):.2f} {my + r * .3 * math.sin(b2):.2f}')
    return f'<path d="{arms}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'


ART = {
    'pumpkin': f'<path d="M24 12c-2-3 0-6 3-7" fill="none" {S}/><ellipse cx="15" cy="28" rx="10" ry="14" fill="#f08a24" {S}/><ellipse cx="33" cy="28" rx="10" ry="14" fill="#f08a24" {S}/><ellipse cx="24" cy="28" rx="9" ry="15" fill="#f79a35" {S}/>'
               f'<path d="M15 24l4-5 4 5zM25 24l4-5 4 5z" fill="#3a1d0a" stroke="none"/><path d="M14 31c3 5 17 5 20 0l-3 2-2-2-3 2-2-2-3 2-2-2-3 2z" fill="#3a1d0a" stroke="none"/><path d="M28 6c3-2 7-1 8 1-3 1-6 1-8-1z" fill="#4c9a3a" {S}/>',
    'bat': f'<path d="M24 20c-3-1-4 1-4 3 0 2 2 4 4 4s4-2 4-4c0-2-1-4-4-3zM20 23c-4-6-11-8-17-6 3 2 4 5 3 8 3-2 6-2 8 1 1-3 4-4 6-3zM28 23c4-6 11-8 17-6-3 2-4 5-3 8-3-2-6-2-8 1-1-3-4-4-6-3z" fill="#3b2457" {S}/>'
           f'<path d="M21.5 18.5l-.5-3 2 2.2M26.5 18.5l.5-3-2 2.2" fill="#3b2457" {S}/><circle cx="22.4" cy="22.5" r="1.1" fill="#ffd166"/><circle cx="25.6" cy="22.5" r="1.1" fill="#ffd166"/>',
    'ghost': f'<path d="M10 40V20a14 14 0 0 1 28 0v20l-4.7-3.5L28.7 40 24 36.5 19.3 40l-4.6-3.5z" fill="#fbfbff" {S}/><ellipse cx="19" cy="21" rx="2.2" ry="3" fill="{INK}"/><ellipse cx="29" cy="21" rx="2.2" ry="3" fill="{INK}"/><ellipse cx="24" cy="29" rx="3" ry="2.4" fill="{INK}"/><circle cx="15.5" cy="26" r="2" fill="#ffb3c7"/><circle cx="32.5" cy="26" r="2" fill="#ffb3c7"/>',
    'web': f'<path d="{spikes(24, 24, 0, 20, 8)}" fill="none" stroke="#6b5a80" stroke-width="1.6"/>' + ''.join(
        f'<polygon points="{" ".join(f"{24 + r * math.cos(math.radians(i * 45)):.1f},{24 + r * math.sin(math.radians(i * 45)):.1f}" for i in range(8))}" fill="none" stroke="#6b5a80" stroke-width="1.4"/>' for r in (6, 11.5, 17))
        + f'<circle cx="31" cy="31" r="3.4" fill="{INK}"/><path d="M28 29l-3-2M28 32h-3.5M34 29l3-2M34 32h3.5" stroke="{INK}" stroke-width="1.6"/>',
    'candy': f'<path d="M14 24l-8-7v14zM34 24l8-7v14z" fill="#ffd166" {S}/><circle cx="24" cy="24" r="10" fill="#ff6b9a" {S}/><path d="M17 20c4 2 10 2 14-1M16 26c5 3 11 3 16 0" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>',
    'sugarskull': f'<path d="M24 6C14 6 8 13 8 22c0 5 2.5 8.5 5.5 10.5V38a3 3 0 0 0 3 3h15a3 3 0 0 0 3-3v-5.5C37.5 30.5 40 27 40 22c0-9-6-16-16-16z" fill="#fffaf2" {S}/>'
                  f'<circle cx="17" cy="22" r="5.2" fill="#3b2457"/><circle cx="31" cy="22" r="5.2" fill="#3b2457"/>' + petals(17, 22, 6, 1.4, 2.2, 3.2, '#ff9b2f') .replace(S, 'stroke="none"') + petals(31, 22, 6, 1.4, 2.2, 3.2, '#2bb3b5').replace(S, 'stroke="none"') +
                  f'<circle cx="17" cy="22" r="1.4" fill="#ffd166"/><circle cx="31" cy="22" r="1.4" fill="#ffd166"/><path d="M24 27l-2.2 4h4.4z" fill="#3b2457"/>'
                  f'<path d="M17 35.5h14M20 33.5v4M24 33.5v4M28 33.5v4" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>' + petals(24, 12.5, 5, 1.8, 2.6, 2.6, '#e84a7f').replace(S, 'stroke="none"') + '<circle cx="24" cy="12.5" r="1.5" fill="#ffd166"/>'
                  '<path d="M11 15c1.5 1 1.5 3 0 4M37 15c-1.5 1-1.5 3 0 4" fill="none" stroke="#2bb3b5" stroke-width="1.6" stroke-linecap="round"/>',
    'marigold': petals(24, 24, 12, 4.5, 8, 11, '#f08a24') + petals(24, 24, 10, 3.6, 6.2, 6.8, '#f7a531', 18) + petals(24, 24, 8, 2.6, 4.2, 3.6, '#ffc247', 8) + f'<circle cx="24" cy="24" r="3" fill="#d9611c" {S}/>',
    'candle': f'<path d="M24 5c3 4 5 7 5 10a5 5 0 0 1-10 0c0-3 2-6 5-10z" fill="#ffc247" {S}/><path d="M24 11c1.2 1.7 2 3 2 4.3a2 2 0 0 1-4 0c0-1.3.8-2.6 2-4.3z" fill="#fff3c4"/>'
              f'<rect x="17" y="21" width="14" height="21" rx="2" fill="#fff6e8" {S}/><path d="M17 26c3 0 3 3 6 3s3-2 8-2" fill="none" stroke="#e84a7f" stroke-width="2"/><path d="M24 21v-2" {S}/><ellipse cx="24" cy="43" rx="11" ry="2.5" fill="#d9611c" {S}/>',
    'bread': f'<path d="M5 34c0-10 8.5-17 19-17s19 7 19 17c0 3-2 5-5 5H10c-3 0-5-2-5-5z" fill="#e3a058" {S}/><path d="M13 27c4-3 8 3 11 0s7-3 11 0M24 20v9" fill="none" stroke="#b46f2c" stroke-width="3.2" stroke-linecap="round"/><circle cx="24" cy="19" r="3.2" fill="#c98543" {S}/>'
             + ''.join(f'<circle cx="{x}" cy="{y}" r=".9" fill="#ff6b9a"/>' for x, y in ((12, 33), (17, 30), (30, 34), (36, 31), (21, 35), (33, 28))),
    'butterfly': f'<path d="M24 22C20 12 9 8 6 13s3 11 18 11zM24 22c4-10 15-14 18-9s-3 11-18 11z" fill="#f08a24" {S}/><path d="M24 24c-10 0-15 5-12 10s10 1 12-8zM24 24c10 0 15 5 12 10s-10 1-12-8z" fill="#f7a531" {S}/>'
                 f'<path d="M24 16v20" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><path d="M24 16l-3-5M24 16l3-5" fill="none" {S}/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="#fff"/>' for x, y in ((9, 14), (39, 14), (14, 32), (34, 32))),
    'butterfly-pink': f'<path d="M24 22C20 12 9 8 6 13s3 11 18 11zM24 22c4-10 15-14 18-9s-3 11-18 11z" fill="#f59ac0" {S}/><path d="M24 24c-10 0-15 5-12 10s10 1 12-8zM24 24c10 0 15 5 12 10s-10 1-12-8z" fill="#c9a4f0" {S}/>'
                      f'<path d="M24 16v20" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><path d="M24 16l-3-5M24 16l3-5" fill="none" {S}/><circle cx="13" cy="15" r="2.4" fill="#fff" opacity=".8"/><circle cx="35" cy="15" r="2.4" fill="#fff" opacity=".8"/>',
    'moon': f'<path d="M30 6a18 18 0 1 0 12 30A15 15 0 0 1 30 6z" fill="#ffe08a" {S}/><circle cx="20" cy="22" r="2.5" fill="#f2c94c"/><circle cx="25" cy="33" r="1.8" fill="#f2c94c"/>',
    'turkey': ''.join(f'<ellipse cx="24" cy="12" rx="4.2" ry="11" fill="{c}" {S} transform="rotate({a} 24 24)"/>' for a, c in ((-70, '#c8323a'), (-42, '#f08a24'), (-14, '#f2b81f'), (14, '#f08a24'), (42, '#c8323a'), (70, '#f2b81f')))
              + f'<ellipse cx="24" cy="31" rx="10" ry="10.5" fill="#8a5a3b" {S}/><circle cx="24" cy="20" r="6" fill="#a8714a" {S}/><circle cx="21.8" cy="19" r="1.2" fill="{INK}"/><circle cx="26.2" cy="19" r="1.2" fill="{INK}"/>'
              f'<path d="M22.5 21.5h3L24 24z" fill="#f2b81f" {S}/><path d="M24 23.5c1.5 1 1.5 3.5 0 4.5" fill="none" stroke="#d93c3c" stroke-width="2.2" stroke-linecap="round"/><path d="M20 41.5v3M28 41.5v3M18.5 44.5h3M26.5 44.5h3" stroke="#e8902a" stroke-width="2.2" stroke-linecap="round"/>',
    'maple': f'<path d="M24 4l3 7 5-2-1 7 7-1-3 5 6 3-8 3 1 4-7-2v12h-2V30l-7 2 1-4-8-3 6-3-3-5 7 1-1-7 5 2z" fill="#d9481e" {S}/><path d="M24 14v28" stroke="#9c2f12" stroke-width="1.6"/>',
    'leaf': f'<path d="M9 39C7 22 18 9 40 8c1 20-10 32-31 31z" fill="#e8902a" {S}/><path d="M9 39C17 30 25 21 34 14M16 31l-1-7M21 26l6 1M25 22l-1-6M29 18l5 1" fill="none" stroke="#a3561a" stroke-width="1.6" stroke-linecap="round"/>',
    'wheat': f'<path d="M24 44V12" {S}/>' + ''.join(f'<ellipse cx="{24 + s * 4}" cy="{y}" rx="2.6" ry="5" fill="#e6b24a" {S} transform="rotate({s * 30} {24 + s * 4} {y})"/>' for y in (14, 21, 28) for s in (-1, 1)) + f'<ellipse cx="24" cy="9" rx="2.6" ry="5" fill="#e6b24a" {S}/>',
    'corn': f'<path d="M24 6c6 0 9 8 9 17s-3 17-9 17-9-8-9-17 3-17 9-17z" fill="#f7c948" {S}/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#e6a817"/>' for y in (12, 17, 22, 27, 32) for x in (20.5, 24, 27.5))
            + f'<path d="M24 44c-6-2-11-8-12-18 4 4 7 8 12 9zM24 44c6-2 11-8 12-18-4 4-7 8-12 9z" fill="#6fae4b" {S}/>',
    'pie': f'<path d="M24 9L7 35c11 5 23 5 34 0z" fill="#ef9a3a" {S}/><path d="M7 35c11 5 23 5 34 0l1 3.5c-12 6-24 6-36 0z" fill="#d9a35c" {S}/><path d="M20.5 22.5c-1.8-.3-1.6-3.2.4-3.2 0-2.6 6.2-2.6 6.2 0 2 0 2.2 2.9.4 3.2z" fill="#fff8ec" {S} stroke-width="1.6"/>',
    'sunflower': petals(24, 20, 14, 3.4, 7, 11, '#f7c948') + f'<circle cx="24" cy="20" r="8" fill="#7a4a24" {S}/>' + ''.join(f'<circle cx="{24 + r * math.cos(math.radians(a)):.1f}" cy="{20 + r * math.sin(math.radians(a)):.1f}" r=".9" fill="#c8915a"/>' for r in (3, 5.5) for a in range(0, 360, 60)) + f'<path d="M24 38v8M24 42c3-3 6-3 8-2" fill="none" stroke="#4c9a3a" stroke-width="2.4" stroke-linecap="round"/>',
    'apple': f'<path d="M24 14c-4-3-14-3-15 8-1 10 6 20 11 20 2 0 3-1 4-1s2 1 4 1c5 0 12-10 11-20-1-11-11-11-15-8z" fill="#d93c3c" {S}/><path d="M24 14c0-4 1-7 3-9" fill="none" {S}/><path d="M26 9c3-4 8-4 10-2-3 3-7 4-10 2z" fill="#4c9a3a" {S}/><path d="M15 20c0-2 1.5-3.5 3-4" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".7"/>',
    'xmastree': f'<path d="M24 5l8 11h-4l9 11h-5l9 11H7l9-11h-5l9-11h-4z" fill="#2f8a4e" {S}/><rect x="20.5" y="38" width="7" height="6" fill="#8a5a3b" {S}/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}"/>' for x, y, c in ((21, 15, '#e84a4a'), (27, 22, '#f2b81f'), (18, 27, '#5ab0f0'), (29, 31, '#e84a4a'), (22, 34, '#f2b81f'), (34, 36, '#5ab0f0')))
                + f'<path d="{star(24, 5, 4.5, 2)}" fill="#f2b81f" {S}/>',
    'star-gold': f'<path d="{star(24, 25, 19, 8)}" fill="#f7c948" {S}/><path d="M18 20l3-1" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>',
    'gift': f'<rect x="7" y="20" width="34" height="22" rx="2" fill="#d93c3c" {S}/><rect x="5" y="14" width="38" height="8" rx="2" fill="#e85a5a" {S}/><path d="M24 14v28" stroke="#f7c948" stroke-width="5"/><path d="M24 14v28" fill="none" {S} stroke-width="1"/>'
            f'<path d="M24 14c-3-6-12-8-12-3 0 3 7 3 12 3zM24 14c3-6 12-8 12-3 0 3-7 3-12 3z" fill="#f7c948" {S}/>',
    'snowman': f'<circle cx="24" cy="33" r="11" fill="#fff" {S}/><circle cx="24" cy="16" r="8" fill="#fff" {S}/><path d="M16 9h16M19 9V3h10v6" fill="#2b2238" {S}/><circle cx="21" cy="15" r="1.2" fill="{INK}"/><circle cx="27" cy="15" r="1.2" fill="{INK}"/><path d="M24 17.5l6 1.5-6 1z" fill="#f08a24" {S} stroke-width="1.2"/>'
               f'<path d="M16.5 22.5c5 2.5 10 2.5 15 0l1 3c-5 2.5-12 2.5-17 0z" fill="#d93c3c" {S}/><circle cx="24" cy="30" r="1.3" fill="{INK}"/><circle cx="24" cy="35" r="1.3" fill="{INK}"/>',
    'bellgold': f'<path d="M12 34c3-3 3-6 3-12a9 9 0 0 1 18 0c0 6 0 9 3 12z" fill="#f7c948" {S}/><circle cx="24" cy="38" r="3.4" fill="#e6a817" {S}/><path d="M24 13c-4-6-10-5-9-1 1 3 6 2 9 1zM24 13c4-6 10-5 9-1-1 3-6 2-9 1z" fill="#d93c3c" {S}/><path d="M19 22c0-3 2-5 4-5.5" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".7"/>',
    'reindeer': f'<path d="M17 14c-2-4-6-6-9-5M15 11l-4-5M31 14c2-4 6-6 9-5M33 11l4-5" fill="none" stroke="#8a5a3b" stroke-width="2.6" stroke-linecap="round"/><ellipse cx="24" cy="27" rx="10" ry="12" fill="#a8714a" {S}/><ellipse cx="13" cy="20" rx="4" ry="2.2" fill="#a8714a" {S} transform="rotate(-25 13 20)"/><ellipse cx="35" cy="20" rx="4" ry="2.2" fill="#a8714a" {S} transform="rotate(25 35 20)"/>'
                f'<ellipse cx="24" cy="33" rx="6" ry="5" fill="#e3c19c" {S}/><circle cx="20" cy="24" r="1.4" fill="{INK}"/><circle cx="28" cy="24" r="1.4" fill="{INK}"/><circle cx="24" cy="31.5" r="3.2" fill="#e8323a" {S}/><circle cx="23" cy="30.5" r=".9" fill="#fff"/>',
    'cookie': f'<path d="M24 6a5.5 5.5 0 0 1 4.5 8.7H36a3.5 3.5 0 0 1 0 7h-5.5l3.5 13a3.5 3.5 0 0 1-6.7 2L24 30l-3.3 6.7a3.5 3.5 0 0 1-6.7-2l3.5-13H12a3.5 3.5 0 0 1 0-7h7.5A5.5 5.5 0 0 1 24 6z" fill="#c98543" {S}/><circle cx="22" cy="10.5" r="1" fill="{INK}"/><circle cx="26" cy="10.5" r="1" fill="{INK}"/><path d="M22 13c1.3 1 2.7 1 4 0" fill="none" stroke="{INK}" stroke-width="1.4" stroke-linecap="round"/>'
              f'<circle cx="24" cy="20" r="1.4" fill="#e84a4a"/><circle cx="24" cy="25" r="1.4" fill="#4c9a3a"/><path d="M11 17.5h3M34 17.5h3" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>',
    'santa': f'<path d="M12.5 18C13.5 9 19.5 4.5 27 5.5c5.5.8 8.8 4.8 9.5 10l.8 6.5h-3.4c0-3-.8-5-2.6-6.3L30 18z" fill="#d93c3c" {S}/><circle cx="24" cy="25" r="10" fill="#ffd9c2" {S}/>'
             f'<rect x="10.5" y="15.5" width="25" height="6" rx="3" fill="#fff" {S}/><circle cx="36" cy="23.5" r="3.4" fill="#fff" {S}/>'
             f'<path d="M12.5 26c0 10 5 17.5 11.5 17.5S35.5 36 35.5 26c-2 2-4 3-6 3-1.2 2-3 3-5.5 3s-4.3-1-5.5-3c-2 0-4-1-6-3z" fill="#fff" {S}/>'
             f'<circle cx="20" cy="24.5" r="1.4" fill="{INK}"/><circle cx="28" cy="24.5" r="1.4" fill="{INK}"/><circle cx="17.5" cy="28" r="1.8" fill="#ff9aa8"/><circle cx="30.5" cy="28" r="1.8" fill="#ff9aa8"/>'
             f'<path d="M24 31.5c-2-2.2-6-2.2-7.2 0 2.2 1.6 5 1.6 7.2 0zM24 31.5c2-2.2 6-2.2 7.2 0-2.2 1.6-5 1.6-7.2 0z" fill="#fff" {S} stroke-width="1.4"/><circle cx="24" cy="28.6" r="2" fill="#ffb59a" {S} stroke-width="1.2"/><path d="M21.5 37c1.7 1 3.3 1 5 0" fill="none" stroke="#c9ced8" stroke-width="1.6" stroke-linecap="round"/>',
    'snowflake': flake(24, 24, 18),
    'snowflake2': flake(24, 24, 18, '#a9d4f5', 2.6) + '<circle cx="24" cy="24" r="3" fill="#a9d4f5"/>',
    'snowflake3': flake(24, 24, 18, '#cfe6fa', 3.2),
    'blossom': petals(24, 24, 5, 7.5, 9, 9, '#f8b4cf') + f'<circle cx="24" cy="24" r="4" fill="#e8669a" {S}/>' + ''.join(f'<circle cx="{24 + 6.5 * math.cos(math.radians(a)):.1f}" cy="{24 + 6.5 * math.sin(math.radians(a)):.1f}" r="1" fill="#c43d78"/>' for a in range(-90, 270, 72)),
    'tulip': f'<path d="M24 28v16M24 38c-4-5-9-5-11-3 2 4 7 5 11 3zM24 36c4-5 9-5 11-3-2 4-7 5-11 3z" fill="#6fae4b" {S}/><path d="M14 10l5 5 5-8 5 8 5-5v10a10 10 0 0 1-20 0z" fill="#f06a9e" {S}/>',
    'heart-pink': f'<path d="M24 41S6 30 6 17.5A9.2 9.2 0 0 1 24 13.2a9.2 9.2 0 0 1 18 4.3C42 30 24 41 24 41z" fill="#f59ac0" {S}/><path d="M13 16c1-2 3-3 5-3" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>',
    'heart-violet': f'<path d="M24 41S6 30 6 17.5A9.2 9.2 0 0 1 24 13.2a9.2 9.2 0 0 1 18 4.3C42 30 24 41 24 41z" fill="#a679e6" {S}/><path d="M13 16c1-2 3-3 5-3" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>',
    'sparkle': f'<path d="{star(24, 24, 20, 5, 4)}" fill="#f7d66b" {S}/>',
    'sparkle-soft': f'<path d="{star(20, 22, 15, 4, 4)}" fill="#e4cbff" {S}/><path d="{star(37, 36, 7, 2, 4)}" fill="#f7d66b" {S} stroke-width="1.5"/><path d="{star(38, 10, 4.5, 1.4, 4)}" fill="#f7d66b" stroke="none"/>',
    'cloud-soft': f'<path d="M13 37a8 8 0 0 1-1-15.9 11 11 0 0 1 21 2.9A6.6 6.6 0 0 1 34 37z" fill="#f4f0ff" {S}/>',
    'crescent': f'<path d="M30 6a18 18 0 1 0 12 30A15 15 0 0 1 30 6z" fill="#cdb6f2" {S}/>',
    'planet': f'<circle cx="24" cy="24" r="12" fill="#7a6cf0" {S}/><path d="M14 20c3 1 6 0 8-2M27 32c3-1 6 0 8 1" fill="none" stroke="#a99ff7" stroke-width="2.2" stroke-linecap="round"/><ellipse cx="24" cy="24" rx="21" ry="6" fill="none" stroke="#5ad7ff" stroke-width="2.6" transform="rotate(-18 24 24)"/>'
              f'<path d="M12.2 22.4a12 12 0 0 1 23.6 0" fill="#7a6cf0" stroke="none"/><path d="M12 24a12 12 0 0 1 24 0" fill="none" {S}/>',
    'rocket': f'<path d="M24 4c7 5 10 13 9 22l-4 5H19l-4-5c-1-9 2-17 9-22z" fill="#eef2ff" {S}/><circle cx="24" cy="18" r="4" fill="#5ad7ff" {S}/><path d="M15 26l-6 6 2 7 7-5zM33 26l6 6-2 7-7-5z" fill="#d051e4" {S}/><path d="M20 31l4 12 4-12z" fill="#ff9b2f" {S}/><path d="M22 31l2 7 2-7z" fill="#ffd166"/>',
    'notebook': f'<rect x="10" y="5" width="28" height="38" rx="3" fill="#2340a8" {S}/><rect x="16" y="11" width="18" height="8" rx="1.5" fill="#fff" {S} stroke-width="1.5"/><path d="M19 15h12" stroke="#2340a8" stroke-width="1.6" stroke-linecap="round"/>'
                + ''.join(f'<path d="M7 {y}h6" stroke="#c9ced8" stroke-width="2.4" stroke-linecap="round"/>' for y in (11, 17, 23, 29, 35)) + '<path d="M33 5v38" stroke="#ffe14d" stroke-width="3"/>',
    'bookblue': f'<path d="M10 9a4 4 0 0 1 4-4h24v32H14a4 4 0 0 0-4 4z" fill="#3b6fd8" {S}/><path d="M10 41a4 4 0 0 0 4 4h24v-8H14" fill="#fff" {S}/><path d="M17 13h14M17 18h9" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>',
    'openbook': f'<path d="M24 12c-5-4-12-5-20-4v28c8-1 15 0 20 4 5-4 12-5 20-4V8c-8-1-15 0-20 4z" fill="#fff" {S}/><path d="M24 12v28" {S}/><path d="M9 15c4-.5 7 0 10 1.5M9 21c4-.5 7 0 10 1.5M9 27c4-.5 7 0 10 1.5M29 16.5c3-1.5 6-2 10-1.5M29 22.5c3-1.5 6-2 10-1.5" stroke="#9aa6c8" stroke-width="1.8" stroke-linecap="round"/>',
    'gradcap-art': f'<path d="M24 10L4 19l20 9 20-9z" fill="#172a63" {S}/><path d="M12 23v9c0 3 5 6 12 6s12-3 12-6v-9l-12 5z" fill="#2340a8" {S}/><path d="M41 20v12" {S}/><circle cx="41" cy="34" r="2.4" fill="#ffe14d" {S}/>',
    'pencil-art': f'<path d="M33 6l9 9-23 23-11 2 2-11z" fill="#ffd166" {S}/><path d="M28 11l9 9" {S}/><path d="M10 29l9 9-11 2z" fill="#f4dcc0" {S}/><path d="M8 37.5l2.5 2.5L8 40z" fill="{INK}"/><path d="M33 6l9 9 2-2a3 3 0 0 0 0-4.2L39.2 4a3 3 0 0 0-4.2 0z" fill="#f08aa8" {S}/>',
}


# ---------------------------------------------------------------------------------------------
# Qué dibujo sustituye a cada emoji.
# ---------------------------------------------------------------------------------------------
EMOJI = {
    'ok': '✅ ✔ ✔️ 💯', 'checkbox': '☑ ☑️', 'no': '❌ ✖ ✖️ ❎', 'box': '⬜ ◻ ◻️', 'forbid': '⛔ 🚫', 'stopsign': '🛑',
    'warn': '⚠ ⚠️', 'siren': '🚨', 'dot-red': '🔴', 'dot-green': '🟢', 'dot-yellow': '🟡 🟠', 'dot-white': '⚪', 'record': '⏺ ⏺️',
    'tri-red': '🔺', 'question': '❓ ❔', 'doubt': '🤔', 'info': 'ℹ ℹ️', 'play': '▶️ ⏯ ⏯️', 'pause': '⏸ ⏸️', 'stop': '⏹ ⏹️',
    'lock': '🔒', 'unlock': '🔓', 'lockkey': '🔐 🔏', 'key': '🔑 🗝 🗝️', 'shield': '🛡 🛡️', 'bricks': '🧱', 'virus': '🦠', 'bug': '🐞 🐛',
    'mask': '🎭 🫥 🦹 😈 👿 🏴‍☠️', 'incognito': '🕶 🕶️ 🥷 🤫', 'hook': '🎣', 'trap': '🪤', 'swords': '⚔ ⚔️', 'castle': '🏰', 'idcard': '🪪',
    'salt': '🧂', 'bot': '🧟 🤖', 'police': '👮',
    'book-open': '📖', 'book': '📒', 'book-blue': '📘', 'book-red': '📕', 'book-green': '📗', 'book-yellow': '📙', 'books': '📚',
    'notepad': '🗒 🗒️', 'page': '📄 📑 📃', 'memo': '📝', 'receipt': '🧾', 'scroll': '📜', 'clipboard': '📋', 'folder': '📁',
    'folder-open': '📂', 'folders': '🗂 🗂️', 'cabinet': '🗄 🗄️ 🗃 🗃️', 'tag': '🏷 🏷️', 'bookmark': '🔖', 'pin': '📌', 'pinmap': '📍',
    'clip': '📎', 'link': '🔗', 'calendar': '📅 🗓 🗓️ 📆', 'printer': '🖨 🖨️', 'mail': '✉ ✉️ 📧 📩', 'inbox': '📥', 'outbox': '📤',
    'mail-in': '📨', 'mailbox': '📭 📬 📮 📫 🏤',
    'flask': '🧪', 'tools': '🛠 🛠️ 🧑‍🔧', 'wrench': '🔧', 'toolbox': '🧰', 'gear': '⚙ ⚙️', 'sliders': '🎛 🎛️ 🎚 🎚️', 'pencil': '✏ ✏️',
    'pen-hand': '✍ ✍️ 🖊 🖊️', 'scissors': '✂ ✂️', 'ruler': '📏', 'setsquare': '📐', 'palette': '🎨', 'calculator': '🧮', 'magnet': '🧲',
    'extinguisher': '🧯', 'broom': '🧹', 'sponge': '🧽', 'wand': '🪄', 'ladder': '🪜', 'stethoscope': '🩺', 'bandage': '🩹',
    'numbers': '🔢', 'letters': '🔤 🔡', 'letters-up': '🔠', 'symbols': '🔣', 'ten': '🔟', 'plus': '➕', 'minus': '➖', 'times': '',
    'divide': '➗', 'asterisk': '✳ ✳️', 'dollar': '💲', 'barchart': '📊', 'linechart': '📈', 'piechart': '🥧', 'areachart': '⛰ ⛰️',
    'puzzle': '🧩', 'target': '🎯', 'search': '🔎 🔍 🕵 🕵️ 🧐', 'compass': '🧭', 'map': '🗺 🗺️', 'route': '🛣 🛣️ 🛤 🛤️ 🚇',
    'brain': '🧠', 'bulb': '💡', 'scales': '⚖ ⚖️', 'shuffle': '🔀', 'refresh': '🔄 🔁 🔃 ♻ ♻️', 'arrows-ud': '', 'dna': '🧬', 'onion': '🧅',
    'monitor': '🖥 🖥️', 'laptop': '💻', 'phone': '📱 📟', 'telephone': '📞 ☎ ☎️', 'network': '🖧', 'floppy': '💾', 'disc': '💿 📀',
    'hdd': '💽', 'mouse': '🖱 🖱️', 'pointer': '👆 👉', 'plug': '🔌', 'bolt': '⚡', 'battery': '🔋', 'globe': '🌐 🌍 🌎 🌏',
    'antenna': '📡', 'signal': '📶', 'window': '🪟', 'image': '🖼 🖼️', 'camera': '📷 📸', 'video': '🎥 📽 📽️ 🎞 🎞️', 'clapper': '🎬',
    'mic': '🎙 🎙️ 🎤', 'headphones': '🎧', 'speaker': '🔊 🔉', 'megaphone': '📣 📢', 'music': '🎵 🎶', 'bell': '🔔 🛎 🛎️',
    'clock': '🕘 🕐 🕒', 'alarm': '⏰', 'stopwatch': '⏱ ⏱️ ⏲ ⏲️ ⌛ ⏳', 'sleep': '💤',
    'school': '🏫', 'building': '🏢 🏬', 'classic': '🏛 🏛️ 🏦', 'store': '🏪', 'house': '🏠 🏡', 'hospital': '🏥', 'door': '🚪', 'hole': '🕳 🕳️',
    'tree': '🌳', 'pine': '🌲', 'mountain': '', 'sunrise': '🌅', 'wave': '🌊 〰 〰️', 'cloud': '☁ ☁️', 'tornado': '🌪 🌪️', 'fire': '🔥',
    'boom': '💥', 'user': '👤 👩 👨 🧑 🙋 🚶 👩‍💼 👨‍⚕️ 🗣 🗣️', 'users': '👥 👨‍👩‍👧', 'teacher': '👩‍🏫 👨‍🏫', 'coder': '🧑‍💻 👩‍💻 👨‍💻',
    'handshake': '🤝', 'thumbsup': '👍 💪', 'medal': '🏅 🏆', 'crown': '👑', 'pawn': '♟ ♟️', 'flag': '🚩', 'finish': '🏁', 'smile': '😄 😀 🙂 😊',
    'gradcap': '', 'heart-blue': '💙', 'heart-purple': '💜', 'star': '⭐ 🌟', 'sparkles': '', 'coffee': '☕', 'ribbon': '🎀',
    'sunglasses': '😎', 'traffic': '🚦', 'gift-line': '', 'rocket-line': '', 'package': '📦', 'truck': '🚚', 'wheel': '🛞', 'ferris': '🎡',
    'pot': '🍲', 'snake': '🐍', 'penguin': '🐧', 'cassette': '📼', 'eye': '', 'eye2': '', 'trash': '', 'speech': '',
    # Ilustraciones
    'pumpkin': '🎃', 'bat': '🦇', 'ghost': '👻', 'web': '🕸 🕸️', 'candy': '🍬 🍭', 'sugarskull': '💀', 'marigold': '🏵 🏵️',
    'candle': '🕯 🕯️', 'bread': '🍞', 'butterfly': '🦋', 'moon': '🌙', 'turkey': '🦃', 'maple': '🍁', 'leaf': '🍂', 'wheat': '🌾',
    'corn': '🌽', 'sunflower': '🌻', 'apple': '🍎', 'xmastree': '🎄', 'gift': '🎁', 'snowman': '⛄ ☃ ☃️', 'reindeer': '🦌',
    'cookie': '🍪', 'santa': '🎅', 'snowflake': '❄ ❄️', 'snowflake2': '❅', 'snowflake3': '❆', 'blossom': '🌸', 'tulip': '🌷',
    'planet': '🪐', 'rocket': '🚀', 'notebook': '📓', 'gradcap-art': '🎓', 'sparkle-soft': '✨',
}

# Íconos que faltaban en la lista de arriba y se dibujan aquí.
ICONS.update({
    'eye': f'<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z" {A}/><circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="1" {F}/>',
    'trash': f'<path d="M4 6.5h16M9.5 6.5V4h5v2.5"/><path d="M6 6.5l1 13.7A1.5 1.5 0 0 0 8.5 21.5h7a1.5 1.5 0 0 0 1.5-1.3l1-13.7" {A}/><path d="M10 10.5v7M14 10.5v7"/>',
    'speech': f'<path d="{BUBBLE}" {A}/><path d="M8 8h8M8 11.3h5"/>',
})
EMOJI.update({'eye': '👁 👁️ 👀', 'trash': '🗑 🗑️', 'speech': '💬 💭 🗨 🗨️'})
ICONS.update({
    'keyboard': f'<rect x="2.5" y="6" width="19" height="12" rx="2" {A}/><path d="M6 9.5h.01M9.3 9.5h.01M12.6 9.5h.01M15.9 9.5h.01M18 9.5h.01M6.5 12.3h.01M9.8 12.3h.01M13.1 12.3h.01M16.4 12.3h.01M8 15h8" stroke-width="2"/>',
    'briefcase': f'<rect x="3" y="7" width="18" height="13" rx="2" fill="#c8915a" fill-opacity=".35"/><path d="M9 7V5.2A1.2 1.2 0 0 1 10.2 4h3.6A1.2 1.2 0 0 1 15 5.2V7M3 12.5h18M11 12.5v2h2v-2"/>',
    'firetruck': f'<path d="M2.5 8h12v9h-12z" fill="{RED}" fill-opacity=".55"/><path d="M14.5 10.5h3.8L21.5 14v3h-7M3.5 5.5l9 2.5M5 8l1.5-4"/><circle cx="6.5" cy="17.8" r="1.8" fill="#fff"/><circle cx="17.5" cy="17.8" r="1.8" fill="#fff"/>',
})
EMOJI.update({'keyboard': '⌨ ⌨️', 'briefcase': '💼', 'firetruck': '🚒', 'mask': '🎭 🫥 🦹 😈 👿 🏴‍☠️ ☠ ☠️', 'stethoscope': '🩺 ⚕ ⚕️'})

# Símbolos tipográficos que se quedan como texto (no son dibujos), pero sin la variante de emoji (U+FE0F).
TEXT_ONLY = '▶ ↔ ↩ ↪ ↕ ▫ ➡ ⬅ ⬆ ⬇ ▪ ◀ ⤴ ⤵'


def clean(body):
    """Un atributo repetido (p. ej. stroke-width de {S} y otro propio) deja solo el último."""
    def dedupe(m):
        seen = {}
        for k, v in re.findall(r'([\w:-]+)="([^"]*)"', m.group(2)):
            seen.pop(k, None)
            seen[k] = v
        return '<' + m.group(1) + ''.join(f' {k}="{v}"' for k, v in seen.items()) + m.group(3)
    return re.sub(r'<(\w+)((?:\s+[\w:-]+="[^"]*")*)\s*(/?>)', dedupe, body)


def build():
    icons = {}
    for name, body in ICONS.items():
        icons[name] = {'v': 24, 'b': body}
    for name, body in ART.items():
        icons[name] = {'v': 48, 'b': body, 'art': 1}
    emoji = {}
    for name, keys in EMOJI.items():
        for key in keys.split():
            if name not in icons:
                raise SystemExit(f'Falta el dibujo «{name}»')
            emoji[key] = name
    for item in icons.values():
        item['b'] = clean(item['b'])
    data = {'icons': icons, 'emoji': emoji, 'textOnly': TEXT_ONLY.split()}
    out = ROOT / 'src/lib/aula-icons.json'
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf8')
    print(f'{len(icons)} dibujos, {len(emoji)} emojis sustituidos → {out.relative_to(ROOT)}')


def data_uri(svg):
    from urllib.parse import quote
    return 'url("data:image/svg+xml,' + quote(svg, safe=' =:/,;.-#') .replace('#', '%23') + '")'


def strip(names, size=48, gap=6):
    """Varias ilustraciones en fila; 'sparkle' se dibuja más chica entre ellas."""
    x, parts = 0, []
    for name in names:
        small = name == 'sparkle'
        s = .5 if small else 1
        parts.append(f'<g transform="translate({x:g} {size * (1 - s) / 2:g}) scale({s:g})">{clean(ART[name])}</g>')
        x += size * s + gap
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x - gap:g} {size}">{"".join(parts)}</svg>', (x - gap) / size


def build_css():
    """Adornos de los temas que antes eran emojis dentro de CSS (content:"…")."""
    def one(name):
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">{clean(ART[name])}</svg>'
    heroes = {
        'halloween': ['pumpkin', 'sparkle', 'bat'], 'muertos': ['marigold', 'sparkle', 'sugarskull', 'sparkle', 'marigold'],
        'gracias': ['leaf', 'sparkle', 'turkey', 'sparkle', 'maple'], 'navidad': ['star-gold', 'sparkle', 'xmastree', 'sparkle', 'gift'],
    }
    marks = {'halloween': 'pumpkin', 'muertos': 'marigold', 'rosa': 'blossom', 'lila': 'sparkle-soft', 'gracias': 'leaf', 'navidad': 'xmastree'}
    css = ['/* Generado por scripts/icons/aula_icons.py: adornos dibujados (sin emojis) de los temas. No editar a mano. */']
    for theme, names in heroes.items():
        svg, ratio = strip(names)
        css.append(f'html[data-aula-theme="{theme}"] .student-journey-hero:before{{content:"";height:1.55rem;width:{1.55 * ratio:.2f}rem;'
                   f'background:{data_uri(svg)} center/contain no-repeat;letter-spacing:0}}')
    for theme, name in marks.items():
        sel = f'html[data-aula-theme="{theme}"] .panel-title h3:after,html[data-aula-theme="{theme}"] .list-toolbar h1:after'
        css.append(f'{sel}{{content:"";display:inline-block;width:.95em;height:.95em;margin-left:.45em;vertical-align:-.12em;'
                   f'background:{data_uri(one(name))} center/contain no-repeat}}')
    out = ROOT / 'src/theme-art.css'
    out.write_text('\n'.join(css) + '\n', encoding='utf8')
    print(f'Adornos de temas → {out.relative_to(ROOT)}')


if __name__ == '__main__':
    build()
    build_css()
