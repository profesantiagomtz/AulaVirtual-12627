"""Ayudantes para escribir el contenido de un material en Python.

Cada función devuelve el código JS que llama al motor (pL, pA, sp, bk…), con
los textos escapados por json.dumps. Las explicaciones de cada respuesta de pA
se registran en EXP automáticamente.
"""
import json
import re


def j(v):
    return json.dumps(v, ensure_ascii=False)


def call(name, *args):
    while args and args[-1] is None:
        args = args[:-1]
    return f'{name}(' + ','.join(a.code if isinstance(a, Js) else j(a) for a in args) + ')'


class Js:
    """Código JS ya escrito (un cuerpo armado con sp/bk/ex…)."""

    def __init__(self, code):
        self.code = code

    def __add__(self, other):
        return Js(self.code + '+' + other.code)


def sp(h, p):
    return Js(call('sp', h, p))


def ex(h, p):
    return Js(call('ex', h, p))


def ana(h, p):
    return Js(call('ana', h, p))


def bk(h, p, c=''):
    return Js(call('bk', h, p, c))


def warn(h, p):
    return bk(h, p, 'wn')


def r3(items):
    return Js(call('r3', [[f"<div style='font-size:24px'>{e}</div>", t, d] for e, t, d in items]))


def px(t, steps):
    return Js(call('px', t, steps))


def html(s):
    return Js(j(s))


def body(*parts):
    out = parts[0]
    for p in parts[1:]:
        out = out + p
    return out


class Course:
    def __init__(self):
        self.pages = []
        self.exp = {}

    def _add(self, code):
        self.pages.append(code)
        return len(self.pages) - 1

    def L(self, ic, t, inf, content, h=None):
        return self._add(call('pL', ic, t, inf, content, h))

    def A(self, ic, t, inf, rows, h=None, opts=None):
        """rows: [texto, respuesta, explicación]."""
        for text, _, why in rows:
            key = re.sub(r'<[^>]*>', '', text).strip()
            if key in self.exp and self.exp[key] != why:
                raise SystemExit(f'Explicación repetida con otro texto: {key}')
            self.exp[key] = why
        return self._add(call('pA', ic, t, inf, [[r[0], r[1]] for r in rows], h, opts))

    def O(self, ic, t, inf, items, h=None):
        return self._add(call('pO', ic, t, inf, items, h))

    def Z(self, ic, t, inf, tpl, blanks, h=None):
        for answer, options in blanks:
            assert answer in options, answer
        return self._add(call('pZ', ic, t, inf, tpl, blanks, h))

    def W(self, ic, t, inf, prompt, crit, h=None, ph=None):
        for _, rule in crit:
            if not rule.startswith('palabras:'):
                re.compile(rule)
        return self._add(call('pW', ic, t, inf, prompt, crit, h, ph))

    def T(self, ic, t, inf, rows, h=None, mode=None):
        return self._add(call('pT', ic, t, inf, rows, h, mode))

    def raw(self, code):
        return self._add(code)

    def mark(self):
        return len(self.pages)

    def js_pages(self):
        return ',\n'.join(self.pages)
