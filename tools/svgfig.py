#!/usr/bin/env python3
"""
svgfig - a small, dependency-free toolkit for writing colourful publication
figures as code.

Figures are composed in Python as SVG (gradients, drop shadows, rounded cards,
wrapped rich text, coloured arrows, chart axes) and rasterised to
high-resolution PNG with the headless Chromium shipped in the sandbox, so the
result has real anti-aliased typography (Noto Sans) instead of bitmap fonts.

    from svgfig import Figure, Axes, C
    f = Figure(1200, 700, title="My figure", subtitle="optional")
    f.card(60, 120, 300, 160, "Title", "Body text", color="blue")
    f.arrow(360, 200, 460, 200, color="slate")
    f.save("out/figure.png")

The SVG source can be kept alongside the PNG with save(..., keep_svg=True).
"""
import html as _html
import math
import os
import re
import shutil
import subprocess
import tempfile

# --------------------------------------------------------------------------
# Palette: vivid base colours with light / dark companions
# --------------------------------------------------------------------------
C = {
    'blue':    ('#2563EB', '#DBEAFE', '#1E3A8A'),
    'sky':     ('#0EA5E9', '#E0F2FE', '#075985'),
    'cyan':    ('#06B6D4', '#CFFAFE', '#155E75'),
    'teal':    ('#14B8A6', '#CCFBF1', '#115E59'),
    'emerald': ('#10B981', '#D1FAE5', '#065F46'),
    'green':   ('#22C55E', '#DCFCE7', '#166534'),
    'lime':    ('#84CC16', '#ECFCCB', '#3F6212'),
    'yellow':  ('#EAB308', '#FEF9C3', '#854D0E'),
    'amber':   ('#F59E0B', '#FEF3C7', '#92400E'),
    'orange':  ('#F97316', '#FFEDD5', '#9A3412'),
    'red':     ('#EF4444', '#FEE2E2', '#991B1B'),
    'rose':    ('#F43F5E', '#FFE4E6', '#9F1239'),
    'pink':    ('#EC4899', '#FCE7F3', '#9D174D'),
    'fuchsia': ('#D946EF', '#FAE8FF', '#86198F'),
    'purple':  ('#A855F7', '#F3E8FF', '#6B21A8'),
    'violet':  ('#8B5CF6', '#EDE9FE', '#5B21B6'),
    'indigo':  ('#6366F1', '#E0E7FF', '#3730A3'),
    'slate':   ('#64748B', '#F1F5F9', '#1E293B'),
    'gray':    ('#9CA3AF', '#F3F4F6', '#374151'),
}
# A good categorical sequence for charts
SERIES = ['blue', 'orange', 'emerald', 'rose', 'violet', 'amber', 'cyan',
          'pink', 'lime', 'indigo', 'teal', 'red']
INK = '#0F172A'
MUTED = '#475569'
FONT = "'Noto Sans', 'DejaVu Sans', Arial, sans-serif"

HEADLESS = ('/inner_container/opt/playwright/chromium_headless_shell-1232/'
            'chrome-headless-shell-linux64/chrome-headless-shell')


def col(name, shade=0):
    """Resolve a palette name (or pass through '#hex'). shade 0=base,1=light,2=dark."""
    if name in C:
        return C[name][shade]
    return name


def lerp_hex(a, b, t):
    a, b = a.lstrip('#'), b.lstrip('#')
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return '#%02X%02X%02X' % tuple(round(x + (y - x) * t) for x, y in zip(ca, cb))


_ALLOWED = ('b', 'i', 'sub', 'sup', 'br', 'u', 'small', 'span')


def rich(s):
    """Escape text but keep a few inline tags (<b>, <i>, <sub>, <sup>, <br>)."""
    s = _html.escape(_html.unescape(s), quote=False)
    for t in _ALLOWED:
        s = re.sub(r'&lt;(/?)%s(\s[^&]*?)?(/?)&gt;' % t,
                   lambda m: '<%s%s%s%s>' % (m.group(1), t,
                                              (m.group(2) or '').replace('&quot;', '"'),
                                              m.group(3)), s)
    s = s.replace('<br>', '<br/>')
    return s


def esc(s):
    return _html.escape(str(s), quote=True)


# Noto Sans (the only font in the sandbox) lacks arrows, check marks and a
# few maths symbols.  They are drawn as tiny inline vector glyphs instead.
def _ig(path, w=1.0, fill=False, sw=2.2, vb='0 0 20 20', dy='-0.12em'):
    if fill:
        p = '<path d="%s" fill="currentColor"/>' % path
    else:
        p = ('<path d="%s" fill="none" stroke="currentColor" stroke-width="%s" '
             'stroke-linecap="round" stroke-linejoin="round"/>' % (path, sw))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" style="width:%sem;height:0.95em;'
            'vertical-align:middle;margin:0 0.08em;position:relative;top:%s">%s</svg>' % (vb, w, dy, p))


GLYPHS = {
    '→': _ig('M2,10 H17 M11,4 L17,10 L11,16', 1.05),
    '←': _ig('M18,10 H3 M9,4 L3,10 L9,16', 1.05),
    '↑': _ig('M10,18 V3 M4,9 L10,3 L16,9', 0.8),
    '↓': _ig('M10,2 V17 M4,11 L10,17 L16,11', 0.8),
    '↔': _ig('M3,10 H17 M7,5 L2,10 L7,15 M13,5 L18,10 L13,15', 1.1),
    '⇄': _ig('M2,7 H17 M13,3 L17,7 L13,11 M18,13 H3 M7,9 L3,13 L7,17', 1.1),
    '⇒': _ig('M2,7 H14 M2,13 H14 M11,3 L18,10 L11,17', 1.05),
    '✓': _ig('M3,11 L8,16 L17,4', 0.9, sw=2.8),
    '✗': _ig('M4,4 L16,16 M16,4 L4,16', 0.85, sw=2.8),
    '●': _ig('M10,3 a7,7 0 1,0 0.01,0 z', 0.75, fill=True),
    '◆': _ig('M10,2 L18,10 L10,18 L2,10 z', 0.75, fill=True),
    '★': _ig('M10,1.5 L12.6,7.4 L19,7.9 L14.1,12 L15.6,18.3 L10,15 L4.4,18.3 L5.9,12 L1,7.9 L7.4,7.4 z',
             0.85, fill=True),
    '▲': _ig('M10,3 L18,17 L2,17 z', 0.75, fill=True),
    '▼': _ig('M10,17 L18,3 L2,3 z', 0.75, fill=True),
    '≥': _ig('M4,3 L16,8 L4,13 M4,17 H16', 0.8, sw=2),
    '≤': _ig('M16,3 L4,8 L16,13 M4,17 H16', 0.8, sw=2),
    '≈': _ig('M3,8 C6,5 9,5 10,8 C11,11 14,11 17,8 M3,14 C6,11 9,11 10,14 C11,17 14,17 17,14', 0.85, sw=1.9),
    '∞': _ig('M10,10 C7,5 2,5 2,10 C2,15 7,15 10,10 C13,5 18,5 18,10 C18,15 13,15 10,10 z', 1.0, sw=1.9),
    '🛡': _ig('M10,2 L17,5 V10 C17,14.5 14,17 10,18.5 C6,17 3,14.5 3,10 V5 z', 0.9, fill=True),
}
_SUBST = {'∆': 'Δ', '⋅': '·', '\u2009': ' '}
_NEEDS = set(GLYPHS)


def _glyphify(s):
    for k, v in _SUBST.items():
        s = s.replace(k, v)
    for k, v in GLYPHS.items():
        s = s.replace(k, v)
    return s


def _xhtml(s):
    """Make hand-written HTML fragments XML-safe for foreignObject."""
    s = re.sub(r'<br\s*>', '<br/>', s)
    s = s.replace('&nbsp;', '&#160;')
    s = re.sub(r'&(?!#?\w+;)', '&amp;', s)
    return s


class Figure:
    def __init__(self, w, h, title=None, subtitle=None, bg='#FFFFFF',
                 header_color='indigo', header=True):
        self.w, self.h = w, h
        self.defs = []
        self.body = []
        self._ids = set()
        self._gid = 0
        self.defs.append(
            '<filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">'
            '<feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.16"/>'
            '</filter>'
            '<filter id="softshadow" x="-20%" y="-20%" width="140%" height="150%">'
            '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.12"/>'
            '</filter>')
        self.rect(0, 0, w, h, fill=bg, rx=0, shadow=False)
        self.top = 20
        if title and header:
            hc = col(header_color)
            g = self.lingrad(lerp_hex(hc, '#000000', 0.15), lerp_hex(hc, '#EC4899', 0.45), horizontal=True)
            hh = 74 if subtitle else 58
            self.rect(0, 0, w, hh, fill=g, rx=0, shadow=False)
            self.text(w / 2, 38, title, size=25, weight=700, color='#FFFFFF')
            if subtitle:
                self.text(w / 2, 62, subtitle, size=15, color='#E0E7FF', italic=True)
            self.top = hh + 18

    # ---------------------------------------------------------------- defs
    def _id(self, prefix):
        self._gid += 1
        return '%s%d' % (prefix, self._gid)

    def lingrad(self, c1, c2, horizontal=False, stops=None):
        gid = self._id('g')
        x2, y2 = ('1', '0') if horizontal else ('0', '1')
        if stops is None:
            stops = [(0, c1), (1, c2)]
        st = ''.join('<stop offset="%s" stop-color="%s"/>' % (o, c) for o, c in stops)
        self.defs.append('<linearGradient id="%s" x1="0" y1="0" x2="%s" y2="%s">%s</linearGradient>'
                         % (gid, x2, y2, st))
        return 'url(#%s)' % gid

    def radgrad(self, c1, c2):
        gid = self._id('r')
        self.defs.append('<radialGradient id="%s" cx="50%%" cy="40%%" r="65%%">'
                         '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
                         '</radialGradient>' % (gid, c1, c2))
        return 'url(#%s)' % gid

    def marker(self, color):
        mid = 'm' + color.lstrip('#')
        if mid not in self._ids:
            self._ids.add(mid)
            self.defs.append(
                '<marker id="%s" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" '
                'markerHeight="5.5" orient="auto-start-reverse">'
                '<path d="M0,0 L10,5 L0,10 L2.5,5 z" fill="%s"/></marker>' % (mid, color))
        return 'url(#%s)' % mid

    def grad_for(self, name, vertical=True):
        """Pleasant light->base gradient for a palette colour."""
        base, light, _ = C.get(name, (name, '#FFFFFF', name))
        return self.lingrad(lerp_hex(light, '#FFFFFF', 0.3), lerp_hex(base, light, 0.55),
                            horizontal=not vertical)

    def vivid_for(self, name):
        base, light, dark = C.get(name, (name, name, name))
        return self.lingrad(lerp_hex(base, '#FFFFFF', 0.12), lerp_hex(base, dark, 0.25))

    # ------------------------------------------------------------- shapes
    def raw(self, s):
        self.body.append(s)

    def rect(self, x, y, w, h, fill='#FFFFFF', stroke=None, sw=2, rx=12,
             shadow=True, opacity=1, dash=None):
        a = ['x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s"' % (x, y, w, h, rx),
             'fill="%s"' % col(fill)]
        if stroke:
            a.append('stroke="%s" stroke-width="%s"' % (col(stroke), sw))
        if dash:
            a.append('stroke-dasharray="%s"' % dash)
        if opacity != 1:
            a.append('opacity="%s"' % opacity)
        if shadow:
            a.append('filter="url(#%s)"' % ('shadow' if shadow is True else shadow))
        self.body.append('<rect %s/>' % ' '.join(a))

    def circle(self, cx, cy, r, fill='#FFFFFF', stroke=None, sw=2, shadow=False, opacity=1):
        a = 'cx="%.1f" cy="%.1f" r="%.1f" fill="%s"' % (cx, cy, r, col(fill))
        if stroke:
            a += ' stroke="%s" stroke-width="%s"' % (col(stroke), sw)
        if shadow:
            a += ' filter="url(#softshadow)"'
        if opacity != 1:
            a += ' opacity="%s"' % opacity
        self.body.append('<circle %s/>' % a)

    def ellipse(self, cx, cy, rx, ry, fill='#FFFFFF', stroke=None, sw=2, opacity=1, shadow=False):
        a = 'cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"' % (cx, cy, rx, ry, col(fill))
        if stroke:
            a += ' stroke="%s" stroke-width="%s"' % (col(stroke), sw)
        if opacity != 1:
            a += ' opacity="%s"' % opacity
        if shadow:
            a += ' filter="url(#softshadow)"'
        self.body.append('<ellipse %s/>' % a)

    def path(self, d, fill='none', stroke='slate', sw=2, opacity=1, dash=None,
             arrow=False, arrow_start=False, cap='round', shadow=False):
        sc = col(stroke) if stroke else 'none'
        a = 'd="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"' % (
            d, col(fill), sc, sw, cap)
        if opacity != 1:
            a += ' opacity="%s"' % opacity
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        if arrow:
            a += ' marker-end="%s"' % self.marker(sc)
        if arrow_start:
            a += ' marker-start="%s"' % self.marker(sc)
        if shadow:
            a += ' filter="url(#softshadow)"'
        self.body.append('<path %s/>' % a)

    def polygon(self, pts, fill='blue', stroke=None, sw=2, opacity=1, shadow=False):
        p = ' '.join('%.1f,%.1f' % xy for xy in pts)
        a = 'points="%s" fill="%s"' % (p, col(fill))
        if stroke:
            a += ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (col(stroke), sw)
        if opacity != 1:
            a += ' opacity="%s"' % opacity
        if shadow:
            a += ' filter="url(#softshadow)"'
        self.body.append('<polygon %s/>' % a)

    def polyline(self, pts, stroke='blue', sw=3, dash=None, opacity=1, arrow=False):
        d = 'M' + ' L'.join('%.1f,%.1f' % xy for xy in pts)
        self.path(d, stroke=stroke, sw=sw, dash=dash, opacity=opacity, arrow=arrow)

    def line(self, x1, y1, x2, y2, color='slate', sw=2, dash=None, opacity=1):
        self.path('M%.1f,%.1f L%.1f,%.1f' % (x1, y1, x2, y2), stroke=color, sw=sw,
                  dash=dash, opacity=opacity)

    def arrow(self, x1, y1, x2, y2, color='slate', sw=3, dash=None, both=False, curve=0,
              label=None, label_color=None, label_size=13, label_dy=-8):
        """Straight (curve=0) or curved arrow. curve = perpendicular bulge in px."""
        if curve:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            L = math.hypot(dx, dy) or 1
            cx, cy = mx - dy / L * curve, my + dx / L * curve
            d = 'M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f' % (x1, y1, cx, cy, x2, y2)
            lx, ly = (mx + cx) / 2, (my + cy) / 2
        else:
            d = 'M%.1f,%.1f L%.1f,%.1f' % (x1, y1, x2, y2)
            lx, ly = (x1 + x2) / 2, (y1 + y2) / 2
        self.path(d, stroke=color, sw=sw, dash=dash, arrow=True, arrow_start=both)
        if label:
            self.pill(lx, ly + label_dy, label, color=label_color or color, size=label_size)

    def polyarrow(self, pts, color='slate', sw=3, dash=None, both=False):
        d = 'M' + ' L'.join('%.1f,%.1f' % xy for xy in pts)
        self.path(d, stroke=color, sw=sw, dash=dash, arrow=True, arrow_start=both)

    # -------------------------------------------------------------- text
    def text(self, x, y, s, size=15, color=INK, weight=400, anchor='middle',
             italic=False, rotate=None, opacity=1, family=None, spacing=None):
        s = str(s)
        for k, v in _SUBST.items():
            s = s.replace(k, v)
        if any(ch in _NEEDS for ch in s):
            # route through HTML so that vector glyphs can be inlined
            W = 2400
            left = {'middle': x - W / 2, 'start': x, 'end': x - W}[anchor]
            top = y - size * 1.08
            tr = ' transform="rotate(%s %.1f %.1f)"' % (rotate, x, y) if rotate is not None else ''
            style = ('width:%dpx;height:%spx;text-align:%s;white-space:nowrap;font-family:%s;'
                     'font-size:%spx;line-height:1.3;color:%s;font-weight:%s;%s%s' % (
                         W, size * 1.6, {'middle': 'center', 'start': 'left', 'end': 'right'}[anchor],
                         FONT.replace('"', "'"), size, col(color), weight,
                         'font-style:italic;' if italic else '',
                         'letter-spacing:%spx;' % spacing if spacing else ''))
            self.body.append(
                '<foreignObject x="%.1f" y="%.1f" width="%d" height="%.1f"%s%s>'
                '<div xmlns="http://www.w3.org/1999/xhtml" style="%s">%s</div></foreignObject>'
                % (left, top, W, size * 1.6, tr, ' opacity="%s"' % opacity if opacity != 1 else '',
                   style, _glyphify(rich(s))))
            return
        a = ['x="%.1f" y="%.1f"' % (x, y), 'font-size="%s"' % size,
             'font-family="%s"' % (family or FONT).replace('"', "'"),
             'fill="%s"' % col(color), 'text-anchor="%s"' % anchor,
             'font-weight="%s"' % weight]
        if italic:
            a.append('font-style="italic"')
        if rotate is not None:
            a.append('transform="rotate(%s %.1f %.1f)"' % (rotate, x, y))
        if opacity != 1:
            a.append('opacity="%s"' % opacity)
        if spacing:
            a.append('letter-spacing="%s"' % spacing)
        content = rich(s)
        content = content.replace('<sub>', '<tspan baseline-shift="sub" font-size="70%">') \
                         .replace('</sub>', '</tspan>') \
                         .replace('<sup>', '<tspan baseline-shift="super" font-size="70%">') \
                         .replace('</sup>', '</tspan>') \
                         .replace('<b>', '<tspan font-weight="700">').replace('</b>', '</tspan>') \
                         .replace('<i>', '<tspan font-style="italic">').replace('</i>', '</tspan>')
        self.body.append('<text %s>%s</text>' % (' '.join(a), content))

    def html(self, x, y, w, h, content, size=14, color=INK, align='center',
             valign='center', weight=400, line=1.25, pad=6, italic=False):
        """Wrapped rich text inside a box (foreignObject)."""
        jc = {'center': 'center', 'top': 'flex-start', 'bottom': 'flex-end'}[valign]
        style = ('width:%dpx;height:%dpx;box-sizing:border-box;padding:%dpx;display:flex;'
                 'flex-direction:column;justify-content:%s;text-align:%s;font-family:%s;'
                 'font-size:%spx;line-height:%s;color:%s;font-weight:%s;%s'
                 'overflow:hidden;word-wrap:break-word;' % (
                     w, h, pad, jc, align, FONT.replace('"', "'"), size, line, col(color),
                     weight, 'font-style:italic;' if italic else ''))
        self.body.append(
            '<foreignObject x="%.1f" y="%.1f" width="%.1f" height="%.1f">'
            '<div xmlns="http://www.w3.org/1999/xhtml" style="%s">%s</div></foreignObject>'
            % (x, y, w, h, style,
               '<div>%s</div>' % _glyphify(_xhtml(content) if content.lstrip().startswith('<div')
                                           else rich(content))))

    def pill(self, cx, cy, s, color='indigo', size=13, fg='#FFFFFF', pad=10, solid=True):
        plain = _html.unescape(re.sub(r'<[^>]+>', '', s))
        units = sum(0.72 if ch.isupper() else 0.3 if ch in ' ·.,:;il|' else 0.58 for ch in plain)
        w = max(24, units * size + 2 * pad)
        h = size + 12
        if solid:
            self.rect(cx - w / 2, cy - h / 2, w, h, fill=col(color), rx=h / 2, shadow='softshadow')
            self.text(cx, cy + size * 0.36, s, size=size, color=fg, weight=700)
        else:
            self.rect(cx - w / 2, cy - h / 2, w, h, fill=col(color, 1), stroke=col(color), sw=1.5,
                      rx=h / 2, shadow=False)
            self.text(cx, cy + size * 0.36, s, size=size, color=col(color, 2), weight=700)
        return w

    def badge(self, cx, cy, s, color='indigo', r=17, size=15):
        self.circle(cx, cy, r, fill=self.vivid_for(color), shadow=True)
        self.text(cx, cy + size * 0.36, s, size=size, color='#FFFFFF', weight=700)

    def panel_label(self, x, y, s, color='indigo'):
        self.rect(x, y, 34, 28, fill=self.vivid_for(color), rx=8, shadow='softshadow')
        self.text(x + 17, y + 19.5, s, size=15, color='#FFFFFF', weight=700)

    # -------------------------------------------------------------- cards
    def card(self, x, y, w, h, title, body=None, color='blue', title_size=16,
             body_size=13.5, header_h=None, icon=None, align='center', rx=14, solid_header=True,
             body_color=None, valign='center'):
        """Rounded card with a vivid gradient header and wrapped body text."""
        base, light, dark = C.get(color, (color, '#FFFFFF', color))
        self.rect(x, y, w, h, fill=self.lingrad('#FFFFFF', lerp_hex(light, '#FFFFFF', 0.25)),
                  stroke=lerp_hex(base, '#FFFFFF', 0.35), sw=1.5, rx=rx)
        if body is None:
            # whole card is a vivid tile
            self.rect(x, y, w, h, fill=self.vivid_for(color), rx=rx, shadow=False)
            self.html(x, y, w, h, ('%s ' % icon if icon else '') + title, size=title_size,
                      color='#FFFFFF', weight=700)
            return
        hh = header_h or max(34, title_size * 2.3)
        if solid_header:
            self.path('M%.1f,%.1f a%s,%s 0 0 1 %s,-%s h%.1f a%s,%s 0 0 1 %s,%s v%.1f h-%.1f z' % (
                x, y + rx, rx, rx, rx, rx, w - 2 * rx, rx, rx, rx, rx, hh - rx, w),
                fill=self.vivid_for(color), stroke=None)
            self.html(x, y, w, hh, ('%s ' % icon if icon else '') + title, size=title_size,
                      color='#FFFFFF', weight=700, pad=4)
        else:
            self.html(x, y, w, hh, title, size=title_size, color=dark, weight=700, pad=4)
        self.html(x + 4, y + hh, w - 8, h - hh - 2, body, size=body_size,
                  color=body_color or '#1E293B', align=align, pad=10, valign=valign)

    def tile(self, x, y, w, h, s, color='blue', size=15, rx=14, fg='#FFFFFF', weight=700, shadow=True):
        self.rect(x, y, w, h, fill=self.vivid_for(color), rx=rx, shadow=shadow)
        self.html(x, y, w, h, s, size=size, color=fg, weight=weight)

    def soft(self, x, y, w, h, s=None, color='blue', size=14, rx=14, weight=600, stroke=True,
             dash=None, shadow=True, align='center', valign='center', text_color=None):
        base, light, dark = C.get(color, (color, color, color))
        self.rect(x, y, w, h, fill=self.grad_for(color), stroke=base if stroke else None, sw=2,
                  rx=rx, shadow=shadow, dash=dash)
        if s:
            self.html(x, y, w, h, s, size=size, color=text_color or dark, weight=weight,
                      align=align, valign=valign)

    def legend(self, x, y, items, size=14, swatch='rect', gap=26, cols=1, col_w=200):
        """items: list of (label, colour[, style]) ; style 'rect'|'line'|'dot'|'dash'."""
        for i, it in enumerate(items):
            label, colour = it[0], it[1]
            style = it[2] if len(it) > 2 else swatch
            cx = x + (i % cols) * col_w
            cy = y + (i // cols) * gap
            c = col(colour)
            if style == 'rect':
                self.rect(cx, cy - 11, 22, 15, fill=c, rx=4, shadow=False)
            elif style == 'dot':
                self.circle(cx + 11, cy - 4, 7, fill=c, stroke='#FFFFFF', sw=2)
            elif style in ('line', 'dash'):
                self.line(cx, cy - 4, cx + 26, cy - 4, color=c, sw=4,
                          dash='7,5' if style == 'dash' else None)
                self.circle(cx + 13, cy - 4, 4.5, fill=c, stroke='#FFFFFF', sw=1.5)
            self.text(cx + 32, cy + 1, label, size=size, anchor='start', color=INK)

    def footnote(self, s, size=12.5, color=MUTED, y=None):
        self.text(self.w / 2, y or self.h - 14, s, size=size, color=color, italic=True)

    # -------------------------------------------------------------- output
    def svg(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
                '<defs>%s</defs>%s</svg>' % (self.w, self.h, self.w, self.h,
                                             ''.join(self.defs), '\n'.join(self.body)))

    def save(self, png_path, scale=2, keep_svg=False):
        png_path = os.path.abspath(png_path)
        os.makedirs(os.path.dirname(png_path), exist_ok=True)
        work = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.render_tmp')
        os.makedirs(work, exist_ok=True)
        svg_path = os.path.join(work, os.path.basename(png_path)[:-4] + '.svg')
        with open(svg_path, 'w', encoding='utf8') as f:
            f.write(self.svg())
        out_tmp = os.path.join(work, os.path.basename(png_path))
        if os.path.exists(out_tmp):
            os.remove(out_tmp)
        cmd = [HEADLESS, '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
               '--force-device-scale-factor=%s' % scale,
               '--user-data-dir=%s' % os.path.join(work, 'profile'),
               '--default-background-color=FFFFFFFF',
               '--screenshot=%s' % out_tmp, '--window-size=%d,%d' % (self.w, self.h),
               'file://' + svg_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
        if not os.path.exists(out_tmp):
            raise RuntimeError('render failed for ' + png_path)
        shutil.move(out_tmp, png_path)
        if keep_svg:
            shutil.copy(svg_path, png_path[:-4] + '.svg')
        print('  wrote %s (%d KB)' % (os.path.relpath(png_path), os.path.getsize(png_path) // 1024))


class Axes:
    """Minimal cartesian axes for bar / line / band charts."""

    def __init__(self, fig, x, y, w, h, xlim, ylim, xlabel=None, ylabel=None, title=None,
                 yticks=None, xticks=None, xticklabels=None, grid=True, ytickfmt='{:g}',
                 bg=True, title_color='indigo', tick_size=13, label_size=14, xtick_rotate=None):
        self.f, self.x, self.y, self.w, self.h = fig, x, y, w, h
        self.x0, self.x1 = xlim
        self.y0, self.y1 = ylim
        if bg:
            fig.rect(x, y, w, h, fill=fig.lingrad('#FFFFFF', '#F8FAFC'), stroke='#E2E8F0', sw=1,
                     rx=6, shadow=False)
        if title:
            fig.text(x + w / 2, y - 14, title, size=15.5, weight=700, color=col(title_color, 2))
        if yticks is None:
            yticks = self._nice(self.y0, self.y1)
        for t in yticks:
            py = self.py(t)
            if grid:
                fig.line(x, py, x + w, py, color='#E2E8F0', sw=1)
            fig.text(x - 8, py + 4.5, ytickfmt.format(t), size=tick_size, anchor='end', color=MUTED)
        if xticks is not None:
            for i, t in enumerate(xticks):
                px = self.px(t)
                lab = xticklabels[i] if xticklabels else '{:g}'.format(t)
                if xtick_rotate:
                    fig.text(px, y + h + 16, lab, size=tick_size, anchor='end', color=MUTED,
                             rotate=xtick_rotate)
                else:
                    fig.text(px, y + h + 20, lab, size=tick_size, color=MUTED)
        fig.line(x, y + h, x + w, y + h, color='#334155', sw=1.6)
        fig.line(x, y, x, y + h, color='#334155', sw=1.6)
        if xlabel:
            fig.text(x + w / 2, y + h + (46 if not xtick_rotate else 70), xlabel, size=label_size,
                     weight=600, color='#334155')
        if ylabel:
            fig.text(x - 52, y + h / 2, ylabel, size=label_size, weight=600, color='#334155',
                     rotate=-90)

    @staticmethod
    def _nice(a, b, n=5):
        span = b - a
        raw = span / n
        mag = 10 ** math.floor(math.log10(raw))
        step = min([1, 2, 2.5, 5, 10], key=lambda s: abs(s * mag - raw)) * mag
        t = math.ceil(a / step) * step
        out = []
        while t <= b + 1e-9:
            out.append(round(t, 10))
            t += step
        return out

    def px(self, v):
        return self.x + (v - self.x0) / (self.x1 - self.x0) * self.w

    def py(self, v):
        return self.y + self.h - (v - self.y0) / (self.y1 - self.y0) * self.h

    def bar(self, xc, value, width, color='blue', base=None, label=None, label_fmt='{:g}',
            label_size=12.5, vivid=True, rx=4, label_color=INK, opacity=1, stroke=None):
        b = self.y0 if base is None else base
        y1, y2 = self.py(max(value, b)), self.py(min(value, b))
        x = self.px(xc) - width / 2
        fill = self.f.vivid_for(color) if vivid else col(color)
        self.f.rect(x, y1, width, max(0.5, y2 - y1), fill=fill, rx=rx, shadow='softshadow',
                    opacity=opacity, stroke=stroke, sw=1.5)
        if label is not None:
            s = label if isinstance(label, str) else label_fmt.format(value)
            self.f.text(self.px(xc), y1 - 7, s, size=label_size, weight=700, color=label_color)

    def hbar(self, yc, v0, v1, height, color='blue', vivid=True, rx=5, opacity=1, label=None,
             label_size=12.5):
        x1, x2 = self.px(v0), self.px(v1)
        fill = self.f.vivid_for(color) if vivid else col(color)
        self.f.rect(x1, self.py(yc) - height / 2, x2 - x1, height, fill=fill, rx=rx,
                    shadow='softshadow', opacity=opacity)
        if label:
            self.f.text(x2 + 6, self.py(yc) + 4.5, label, size=label_size, anchor='start',
                        weight=700, color=col(color, 2))

    def line(self, xs, ys, color='blue', sw=3.2, marker=True, dash=None, r=5.5, smooth=False,
             labels=None, label_fmt='{:g}', label_dy=-12, label_size=12.5):
        pts = [(self.px(a), self.py(b)) for a, b in zip(xs, ys)]
        if smooth and len(pts) > 2:
            d = 'M%.1f,%.1f' % pts[0]
            for i in range(1, len(pts)):
                p0 = pts[i - 2] if i > 1 else pts[i - 1]
                p1, p2 = pts[i - 1], pts[i]
                p3 = pts[i + 1] if i + 1 < len(pts) else p2
                c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
                c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
                d += ' C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (c1 + c2 + p2)
            self.f.path(d, stroke=color, sw=sw, dash=dash)
        else:
            self.f.polyline(pts, stroke=color, sw=sw, dash=dash)
        if marker:
            for i, (a, b) in enumerate(pts):
                self.f.circle(a, b, r, fill=col(color), stroke='#FFFFFF', sw=2, shadow=True)
        if labels:
            for (a, b), v in zip(pts, ys):
                self.f.text(a, b + label_dy, label_fmt.format(v), size=label_size, weight=700,
                            color=col(color, 2))

    def area(self, xs, ys_lo, ys_hi, color='blue', opacity=0.25):
        top = [(self.px(a), self.py(b)) for a, b in zip(xs, ys_hi)]
        bot = [(self.px(a), self.py(b)) for a, b in zip(xs, ys_lo)][::-1]
        self.f.polygon(top + bot, fill=col(color), opacity=opacity)

    def errorbar(self, xc, lo, hi, color='slate', cap=7, sw=2):
        x = self.px(xc)
        self.f.line(x, self.py(lo), x, self.py(hi), color=color, sw=sw)
        for v in (lo, hi):
            self.f.line(x - cap, self.py(v), x + cap, self.py(v), color=color, sw=sw)

    def hline(self, v, color='rose', sw=2, dash='7,5', label=None, label_side='right', size=12.5):
        y = self.py(v)
        self.f.line(self.x, y, self.x + self.w, y, color=color, sw=sw, dash=dash)
        if label:
            if label_side == 'right':
                self.f.text(self.x + self.w - 6, y - 7, label, size=size, anchor='end',
                            weight=700, color=col(color, 2))
            else:
                self.f.text(self.x + 6, y - 7, label, size=size, anchor='start', weight=700,
                            color=col(color, 2))

    def band(self, v0, v1, color='amber', opacity=0.18, label=None, size=12.5):
        y1, y2 = self.py(v1), self.py(v0)
        self.f.rect(self.x, y1, self.w, y2 - y1, fill=col(color), opacity=opacity, rx=0, shadow=False)
        if label:
            self.f.text(self.x + self.w - 8, y1 + 16, label, size=size, anchor='end', weight=700,
                        color=col(color, 2))
