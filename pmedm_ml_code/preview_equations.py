#!/usr/bin/env python3
"""Render the manuscript's 45 equations through the same parse tree used for OMML, emitted
as MathML, in headless Chromium. Used to check the LaTeX-to-Word conversion visually."""

import os
import re
import subprocess
import sys
import tempfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from latex2omml import Parser  # noqa: E402
from svgplot import CHROME_CANDIDATES  # noqa: E402

ROOT = os.path.dirname(HERE)


def mml(nodes, style=None):
    return "".join(node(n, style) for n in nodes)


def tok(text, style):
    if not text:
        return ""
    if text.isdigit() or re.fullmatch(r"[0-9.]+", text):
        return "<mn>%s</mn>" % escape(text)
    if style in ("p", "text"):
        return '<mi mathvariant="normal">%s</mi>' % escape(text) if len(text) == 1 else "<mi>%s</mi>" % escape(text)
    if style == "b":
        return '<mi mathvariant="bold">%s</mi>' % escape(text)
    if style == "bi":
        return '<mi mathvariant="bold-italic">%s</mi>' % escape(text)
    if style == "script":
        return '<mi mathvariant="script">%s</mi>' % escape(text)
    if style == "double-struck":
        return '<mi mathvariant="double-struck">%s</mi>' % escape(text)
    if text.isalpha():
        return "<mi>%s</mi>" % escape(text)
    return "<mo>%s</mo>" % escape(text)


def node(n, style=None):
    k = n.kind
    if k == "char":
        return tok(n.text, style)
    if k == "text":
        return tok(n.text, n.style)
    if k == "styled":
        return mml(n.items, n.style)
    if k == "group":
        return "<mrow>%s</mrow>" % mml(n.items, style)
    if k == "frac":
        return "<mfrac><mrow>%s</mrow><mrow>%s</mrow></mfrac>" % (mml(n.num, style), mml(n.den, style))
    if k == "rad":
        return "<msqrt>%s</msqrt>" % mml(n.arg, style)
    if k == "delim":
        return ('<mrow><mo stretchy="true">%s</mo>%s<mo stretchy="true">%s</mo></mrow>'
                % (escape(n.open), mml(n.items, style), escape(n.close)))
    if k == "cases":
        rows = "".join("<mtr>%s</mtr>" % "".join("<mtd>%s</mtd>" % mml(c, style) for c in r) for r in n.rows)
        return '<mrow><mo stretchy="true">{</mo><mtable columnalign="left">%s</mtable></mrow>' % rows
    if k == "acc":
        return '<mover accent="true"><mrow>%s</mrow><mo>%s</mo></mover>' % (
            mml(n.arg, style), {"\u0302": "^", "\u0305": "¯", "\u0303": "~"}.get(n.chr, n.chr))
    if k == "script":
        b = node(n.base, style)
        if n.sub is not None and n.sup is not None:
            return "<msubsup><mrow>%s</mrow><mrow>%s</mrow><mrow>%s</mrow></msubsup>" % (
                b, mml(n.sub, style), mml(n.sup, style))
        if n.sub is not None:
            return "<msub><mrow>%s</mrow><mrow>%s</mrow></msub>" % (b, mml(n.sub, style))
        return "<msup><mrow>%s</mrow><mrow>%s</mrow></msup>" % (b, mml(n.sup, style))
    if k == "nary":
        op = '<mo largeop="true" movablelimits="false">%s</mo>' % n.chr
        sub, sup = mml(n.sub or [], style), mml(n.sup or [], style)
        if n.sub is not None and n.sup is not None:
            o = "<munderover>%s<mrow>%s</mrow><mrow>%s</mrow></munderover>" % (op, sub, sup)
        elif n.sub is not None:
            o = "<munder>%s<mrow>%s</mrow></munder>" % (op, sub)
        else:
            o = op
        # mark the operand with a light box so its extent can be checked visually
        return '<mrow>%s<mrow style="background:#eef4ff">%s</mrow></mrow>' % (o, mml(n.body, style))
    if k == "limfunc":
        if n.sub is None:
            return "<mi>%s</mi>" % n.name
        return "<munder><mi>%s</mi><mrow>%s</mrow></munder>" % (n.name, mml(n.sub, style))
    raise ValueError(k)


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="eq_preview_")
    os.makedirs(out_dir, exist_ok=True)
    md = open(os.path.join(ROOT, "Manuscript_PMEDM_ML_Reanalysis.md"), encoding="utf-8").read()
    eqs = re.findall(r"\$\$(.*?)\$\$", md, flags=re.S)
    rows = []
    for e in eqs:
        p = Parser(e)
        tree = p.parse()
        rows.append('<tr><td style="padding:6px 14px;font:14px sans-serif">(%s)</td><td><math display="block">%s</math></td></tr>'
                    % (p.tag, mml(tree)))
    html = ('<html><head><meta charset="utf-8"><style>body{margin:10px;background:white}math{font-size:19px}'
            '</style></head><body><table>%s</table></body></html>' % "".join(rows))
    path = os.path.join(out_dir, "eq_preview.html")
    with open(path, "w") as fh:
        fh.write(html)
    chrome = next(c for c in CHROME_CANDIDATES if os.path.exists(c))
    for part, (a, b) in enumerate(((0, 15), (15, 30), (30, 45))):
        sub = ('<html><head><meta charset="utf-8"><style>body{margin:10px;background:white}math{font-size:19px}'
               '</style></head><body><table>%s</table></body></html>' % "".join(rows[a:b]))
        sp = os.path.join(out_dir, "eq_preview_%d.html" % part)
        with open(sp, "w") as fh:
            fh.write(sub)
        out = os.path.join(out_dir, "eq_preview_%d.png" % part)
        subprocess.run([chrome, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1300,1500", "--screenshot=" + out, "file://" + sp],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        print(out)


if __name__ == "__main__":
    main()
