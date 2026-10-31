#!/usr/bin/env python3
"""
Convert the generated .docx into a Word-openable .doc (RTF payload).

Word, WordPad and Google Docs all open an RTF file saved with a .doc
extension. This reads the OOXML we built and emits RTF with:
  - headings, justified body text, bold/italic runs
  - the 4 tables (native RTF tables with borders + shaded headers)
  - the 7 figures (PNG embedded via \\pngblip)
  - the 34 equations rendered as formatted text (real super/subscripts,
    fractions, radicals and summation signs)
Pure standard library only.
"""

import zipfile
import struct
import xml.etree.ElementTree as ET

SRC = '/projects/sandbox/AMMAN/RAC_Ensemble_TreeBased_ML_Paper.docx'
OUT = '/projects/sandbox/AMMAN/RAC_Ensemble_TreeBased_ML_Paper.doc'

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'

def w(t): return f'{{{W}}}{t}'
def m(t): return f'{{{M}}}{t}'

zf = zipfile.ZipFile(SRC)
rel_xml = zf.read('word/_rels/document.xml.rels').decode('utf-8')
rel_root = ET.fromstring(rel_xml)
REL = {}
for rel in rel_root:
    REL[rel.get('Id')] = rel.get('Target')


# ---------------- RTF escaping ----------------
def esc(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == '\\':
            out.append('\\\\')
        elif ch == '{':
            out.append('\\{')
        elif ch == '}':
            out.append('\\}')
        elif o < 128:
            out.append(ch)
        else:
            v = o if o < 32768 else o - 65536
            out.append('\\u%d?' % v)
    return ''.join(out)


# ---------------- OMML -> formatted RTF text ----------------
def conv_math(el):
    tag = el.tag.split('}')[-1]
    if tag == 't':
        return esc(el.text or '')
    if tag in ('oMath', 'oMathPara', 'e', 'num', 'den', 'sup', 'sub',
               'deg', 'radicand'):
        return ''.join(conv_math(c) for c in el)
    if tag == 'r':
        return ''.join(conv_math(c) for c in el)
    if tag == 'f':
        num = el.find(m('num')); den = el.find(m('den'))
        return '(' + conv_math(num) + ')/(' + conv_math(den) + ')'
    if tag == 'sSup':
        e = el.find(m('e')); sup = el.find(m('sup'))
        return conv_math(e) + '{\\super ' + conv_math(sup) + '}'
    if tag == 'sSub':
        e = el.find(m('e')); sub = el.find(m('sub'))
        return conv_math(e) + '{\\sub ' + conv_math(sub) + '}'
    if tag == 'sSubSup':
        e = el.find(m('e')); sub = el.find(m('sub')); sup = el.find(m('sup'))
        return (conv_math(e) + '{\\sub ' + conv_math(sub) + '}'
                + '{\\super ' + conv_math(sup) + '}')
    if tag == 'rad':
        rad = el.find(m('radicand'))
        return '\\u8730?(' + conv_math(rad) + ')'
    if tag == 'nary':
        pr = el.find(m('naryPr'))
        ch = '\\u8721?'
        if pr is not None:
            c = pr.find(m('chr'))
            if c is not None and c.get(f'{{{M}}}val'):
                ch = esc(c.get(f'{{{M}}}val'))
        sub = el.find(m('sub')); sup = el.find(m('sup')); e = el.find(m('e'))
        s = ch
        if sub is not None and list(sub):
            s += '{\\sub ' + conv_math(sub) + '}'
        if sup is not None and list(sup):
            s += '{\\super ' + conv_math(sup) + '}'
        s += ' ' + conv_math(e)
        return s
    if tag == 'd':
        pr = el.find(m('dPr'))
        beg, end = '(', ')'
        if pr is not None:
            b = pr.find(m('begChr')); en = pr.find(m('endChr'))
            if b is not None and b.get(f'{{{M}}}val') is not None:
                beg = b.get(f'{{{M}}}val')
            if en is not None and en.get(f'{{{M}}}val') is not None:
                end = en.get(f'{{{M}}}val')
        inner = ''.join(conv_math(c) for c in el if c.tag == m('e'))
        return esc(beg) + inner + esc(end)
    if tag == 'acc':
        e = el.find(m('e'))
        return conv_math(e) + '\\u772?'   # combining macron (bar)
    # default: recurse
    return ''.join(conv_math(c) for c in el)


# ---------------- image embedding ----------------
def png_size(data):
    wpx, hpx = struct.unpack('>II', data[16:24])
    return wpx, hpx

def image_rtf(rid):
    target = REL.get(rid)
    if not target:
        return ''
    data = zf.read('word/' + target)
    wpx, hpx = png_size(data)
    goal_w = 8640  # 6 inches in twips
    goal_h = int(hpx * (goal_w / wpx))
    return ('{\\pict\\pngblip\\picwgoal%d\\pichgoal%d\n%s}'
            % (goal_w, goal_h, data.hex()))


# ---------------- run / paragraph handling ----------------
def conv_run(r):
    rpr = r.find(w('rPr'))
    bold = italic = False
    sz = None
    if rpr is not None:
        bold = rpr.find(w('b')) is not None
        italic = rpr.find(w('i')) is not None
        szel = rpr.find(w('sz'))
        if szel is not None:
            sz = szel.get(f'{{{W}}}val')
    chunk = ''
    for c in r:
        lt = c.tag.split('}')[-1]
        if lt == 't':
            chunk += esc(c.text or '')
        elif lt == 'tab':
            chunk += '\\tab '
        elif lt == 'br':
            chunk += '\\line '
        elif lt == 'drawing':
            blip = None
            for d in c.iter(f'{{{A}}}blip'):
                blip = d; break
            if blip is not None:
                rid = blip.get(f'{{{R}}}embed')
                chunk += image_rtf(rid)
    pre, post = '', ''
    if sz:
        pre += '\\fs%s ' % sz; post = '\\fs24 ' + post
    if bold:
        pre += '\\b '; post = '\\b0 ' + post
    if italic:
        pre += '\\i '; post = '\\i0 ' + post
    if pre:
        return '{' + pre + chunk + '}'
    return chunk


def para_style(p):
    ppr = p.find(w('pPr'))
    style = None
    jc = None
    if ppr is not None:
        st = ppr.find(w('pStyle'))
        if st is not None:
            style = st.get(f'{{{W}}}val')
        j = ppr.find(w('jc'))
        if j is not None:
            jc = j.get(f'{{{W}}}val')
    return style, jc


def conv_paragraph(p):
    style, jc = para_style(p)
    # gather inline content (runs + inline math) in document order
    body = ''
    for c in p:
        lt = c.tag.split('}')[-1]
        if lt == 'r':
            body += conv_run(c)
        elif lt == 'oMath':
            body += conv_math(c)
        elif lt == 'oMathPara':
            for mm in c.findall(m('oMath')):
                body += conv_math(mm)
    # styling
    if style == 'Title':
        return '\\pard\\qc\\sb120\\sa200{\\b\\fs36 ' + body + '}\\par\n'
    if style == 'Heading1':
        return '\\pard\\sb320\\sa120{\\b\\fs28 ' + body + '}\\par\n'
    if style == 'Heading2':
        return '\\pard\\sb200\\sa100{\\b\\fs26 ' + body + '}\\par\n'
    align = {'center': '\\qc', 'left': '\\ql', 'right': '\\qr',
             'both': '\\qj'}.get(jc, '\\qj')
    return '\\pard' + align + '\\sa120\\sl276\\slmult1 ' + body + '\\par\n'


def conv_table(tbl):
    grid = tbl.find(w('tblGrid'))
    widths = [int(gc.get(f'{{{W}}}w')) for gc in grid.findall(w('gridCol'))]
    # cumulative right edges
    edges = []
    acc = 0
    for wd in widths:
        acc += wd
        edges.append(acc)
    out = []
    for tr in tbl.findall(w('tr')):
        trpr = tr.find(w('trPr'))
        header = trpr is not None and trpr.find(w('tblHeader')) is not None
        row = '\\trowd\\trgaph108\\trleft0\n'
        for i, _edge in enumerate(edges):
            bdr = ('\\clbrdrt\\brdrs\\brdrw10\\clbrdrl\\brdrs\\brdrw10'
                   '\\clbrdrb\\brdrs\\brdrw10\\clbrdrr\\brdrs\\brdrw10')
            shade = '\\clcbpat2' if header else ''
            row += bdr + shade + ('\\cellx%d\n' % edges[i])
        cells = tr.findall(w('tc'))
        for i, tc in enumerate(cells):
            text = ''
            for p in tc.findall(w('p')):
                for r in p.findall(w('r')):
                    text += conv_run(r)
            al = '\\qc' if i > 0 else '\\ql'
            bld = '\\b ' if header else ''
            out_cell = ('\\pard\\intbl' + al + '\\fs18 ' + bld + text
                        + ('\\b0' if header else '') + '\\cell\n')
            row += out_cell
        row += '\\row\n'
        out.append(row)
    return '\\pard\n' + ''.join(out) + '\\pard\\sa120\n'


def main():
    doc = ET.fromstring(zf.read('word/document.xml'))
    bodyel = doc.find(w('body'))
    parts = []
    for child in bodyel:
        lt = child.tag.split('}')[-1]
        if lt == 'p':
            parts.append(conv_paragraph(child))
        elif lt == 'tbl':
            parts.append(conv_table(child))
        elif lt == 'sectPr':
            pass
    header = (r'{\rtf1\ansi\ansicpg1252\deff0\deflang1033'
              r'{\fonttbl{\f0\froman Times New Roman;}}'
              r'{\colortbl ;\red217\green226\blue243;}'
              '\n\\paperw12240\\paperh15840'
              '\\margl1440\\margr1440\\margt1440\\margb1440\n'
              '\\fs24\n')
    rtf = header + ''.join(parts) + '}'
    with open(OUT, 'w', encoding='latin-1', errors='replace') as f:
        f.write(rtf)
    import os
    print('Created', OUT)
    print('Size: %.1f KB' % (os.path.getsize(OUT) / 1024))


if __name__ == '__main__':
    main()
