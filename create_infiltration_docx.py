#!/usr/bin/env python3
"""
Build a Word (.docx) manuscript for
"Coupled Effects of Vegetation, Soil Properties, and Antecedent Moisture on
 Infiltration in Permeable Channels".

- Reads Vegetated_Permeable_Channel_Infiltration.md
- Embeds the 7 PNG figures (from infiltration_figures/) after the paragraph in
  which each figure is first cited
- Inserts 4 real Word tables (with data) after the paragraph in which each
  table is first cited
- Uses ONLY the Python standard library (zipfile, struct, zlib, re).
"""

import zipfile
import os
import struct
import re

BASE = '/projects/sandbox/AMMAN'
MD = os.path.join(BASE, 'Vegetated_Permeable_Channel_Infiltration.md')
FIGDIR = os.path.join(BASE, 'infiltration_figures')
OUT = os.path.join(BASE, 'Vegetated_Permeable_Channel_Infiltration.docx')

EMU_PER_PX = 9525  # 1 px @ 96 dpi
MAX_W_PX = 600     # target on-page width in px (~6.25 in)

FIGURES = {
    1: ('Figure_1_Conceptual_Framework.png',
        'Figure 1. Coupled conceptual framework and recirculating flume with cell-resolved infiltration collection.'),
    2: ('Figure_2_Vegetation_Configurations.png',
        'Figure 2. Tested vegetation configurations at fixed stem geometry; frontal-area density increases from bare to high.'),
    3: ('Figure_3_Infiltration_Rate_Density.png',
        'Figure 3. Instantaneous infiltration rate f(t) for four vegetation densities under dry and wet antecedent states.'),
    4: ('Figure_4_Cumulative_Soil_Discharge.png',
        'Figure 4. Cumulative infiltration F(t) for three bed materials across four discharges.'),
    5: ('Figure_5_Spatial_Distribution.png',
        'Figure 5. Along-channel infiltration profile f_x(x) for three vegetation densities, showing a localized hotspot.'),
    6: ('Figure_6_Dimensionless_Collapse.png',
        'Figure 6. Dimensionless collapse of normalized infiltration I* = f/K_s across three bed materials.'),
    7: ('Figure_7_Observed_vs_Predicted.png',
        'Figure 7. Independent-validation parity plot and Nash-Sutcliffe efficiency for the competing models.'),
}

# ---- Table data ----------------------------------------------------------
TABLES = {
    1: {
        'caption': 'Table 1. Physical properties of the three bed materials and geometric characteristics of the vegetation elements.',
        'headers': ['Property', 'Coarse sand', 'Medium sand', 'Sand-gravel'],
        'rows': [
            ['Saturated conductivity Ks (mm/min)', '18.5', '6.2', '24.1'],
            ['Porosity n (-)', '0.41', '0.38', '0.36'],
            ['Bulk density (g/cm3)', '1.56', '1.63', '1.71'],
            ['d10 (mm)', '0.42', '0.18', '0.55'],
            ['d50 (mm)', '0.95', '0.42', '2.35'],
            ['d60 (mm)', '1.15', '0.52', '3.10'],
            ['Uniformity coefficient Cu (-)', '2.74', '2.89', '5.64'],
            ['Saturated water content th_s (-)', '0.41', '0.38', '0.36'],
            ['Residual water content th_r (-)', '0.045', '0.061', '0.038'],
            ['--- Vegetation (rigid cylinders) ---', '', '', ''],
            ['Stem diameter d_v (mm)', '6.0', '6.0', '6.0'],
            ['Stem height H_v (mm)', '120', '120', '120'],
            ['Arrangement', 'Staggered', 'Staggered', 'Staggered'],
        ],
    },
    2: {
        'caption': 'Table 2. Experimental parameters, factor levels, and ranges (Stage I factorial design).',
        'headers': ['Factor', 'Symbol', 'Levels', 'Range / values'],
        'rows': [
            ['Vegetation density', 'lambda', '4', '0, 0.6, 1.3, 2.4 % (bare/low/med/high)'],
            ['Discharge', 'Q', '4', '3.0 - 12.0 L/s'],
            ['Bed material', 'Ks', '3', 'coarse / medium / sand-gravel'],
            ['Antecedent saturation', 'S_i', '3', '0.2, 0.5, 0.8'],
            ['Bed slope (primary)', 'S', '1', '0.0025 (supplementary: 0.001-0.005)'],
            ['Flow depth', 'h', 'derived', '35 - 145 mm'],
            ['Depth-averaged velocity', 'U', 'derived', '0.12 - 0.48 m/s'],
            ['Stem diameter (secondary expt.)', 'd_v', '3', '4, 6, 8 mm'],
            ['Nominal Stage I conditions', '-', '-', '4x4x3x3 = 144'],
            ['Run duration', 't', '-', '60 min'],
        ],
    },
    3: {
        'caption': 'Table 3. Dimensionless variables and their physical interpretation.',
        'headers': ['Group', 'Definition', 'Physical interpretation'],
        'rows': [
            ['Reynolds number Re', 'U h / nu', 'Bulk flow regime / turbulence level'],
            ['Froude number Fr', 'U / sqrt(g h)', 'Sub- vs super-critical; depth response to drag'],
            ['Permeability Reynolds Re_k', 'U k / (nu h)', 'Bed permeability relative to the flow'],
            ['Vegetation density lambda', 'N d_v H_v / A_b', 'Canopy frontal-area forcing'],
            ['Relative submergence', 'H_v / h', 'Emergent vs submerged canopy condition'],
            ['Initial saturation ratio S_i', '(th_i - th_r)/(th_s - th_r)', 'Antecedent moisture state / initial gradient'],
            ['Normalized infiltration I*', 'f / K_s', 'Infiltration scaled by bed conductivity (response)'],
        ],
    },
    4: {
        'caption': 'Table 4. Model performance on the reserved independent validation conditions (best value per column in each metric).',
        'headers': ['Model', 'R2', 'RMSE', 'MAE', 'NSE', 'MAPE (%)', 'd'],
        'rows': [
            ['Green-Ampt benchmark', '0.61', '0.041', '0.033', '0.48', '19.4', '0.79'],
            ['Horton empirical', '0.66', '0.038', '0.030', '0.55', '17.1', '0.83'],
            ['Multiple nonlinear regression', '0.80', '0.026', '0.020', '0.74', '11.8', '0.91'],
            ['Random forest', '0.85', '0.023', '0.018', '0.81', '9.6', '0.94'],
            ['Physical power law', '0.90', '0.019', '0.015', '0.88', '7.9', '0.96'],
            ['Hybrid (physical + ML residual)', '0.97', '0.011', '0.008', '0.96', '4.7', '0.99'],
            ['--- Reserved validation set ---', '', '', '', '', '', ''],
            ['No. of reserved conditions', '32', '(~22% of Stage I)', '', '', '', ''],
            ['Coverage', 'independent lambda x Q x Ks x S_i combinations withheld from calibration', '', '', '', '', ''],
        ],
    },
}


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(26)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('not a png: ' + path)
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def para(text, style=None, bold=False, italic=False, size=None, align=None):
    runs_rpr = ''
    props = ''
    if bold:
        props += '<w:b/>'
    if italic:
        props += '<w:i/>'
    if size:
        props += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size)
    if props:
        runs_rpr = '<w:rPr>%s</w:rPr>' % props
    ppr = ''
    inner = ''
    if style:
        inner += '<w:pStyle w:val="%s"/>' % style
    if align:
        inner += '<w:jc w:val="%s"/>' % align
    if inner:
        ppr = '<w:pPr>%s</w:pPr>' % inner
    return ('<w:p>%s<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (ppr, runs_rpr, esc(text)))


def empty_para():
    return '<w:p/>'


def image_para(rid, w_px, h_px):
    scale = min(1.0, MAX_W_PX / float(w_px))
    cx = int(w_px * scale * EMU_PER_PX)
    cy = int(h_px * scale * EMU_PER_PX)
    return (
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0">'
        '<wp:extent cx="%d" cy="%d"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="%d" name="Picture%d"/>'
        '<wp:cNvGraphicFramePr>'
        '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr><pic:cNvPr id="%d" name="Picture%d"/><pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
        % (cx, cy, rid, rid, rid, rid, rid, cx, cy)
    )


def cell(text, bold=False, width=None):
    props = '<w:b/>' if bold else ''
    rpr = '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/>%s</w:rPr>' % props
    tcpr = '<w:tcW w:w="%d" w:type="dxa"/>' % width if width else ''
    return ('<w:tc><w:tcPr>%s'
            '<w:tcBorders>'
            '<w:top w:val="single" w:sz="4" w:color="808080"/>'
            '<w:bottom w:val="single" w:sz="4" w:color="808080"/>'
            '<w:left w:val="single" w:sz="4" w:color="808080"/>'
            '<w:right w:val="single" w:sz="4" w:color="808080"/>'
            '</w:tcBorders></w:tcPr>'
            '<w:p><w:pPr><w:spacing w:after="20"/></w:pPr>'
            '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p></w:tc>'
            % (tcpr, rpr, esc(text)))


def build_table(tdef):
    headers = tdef['headers']
    rows = tdef['rows']
    ncol = len(headers)
    total = 9360
    cw = total // ncol
    out = ['<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/>'
           '<w:tblLayout w:type="fixed"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:color="808080"/>'
           '<w:bottom w:val="single" w:sz="4" w:color="808080"/>'
           '<w:left w:val="single" w:sz="4" w:color="808080"/>'
           '<w:right w:val="single" w:sz="4" w:color="808080"/>'
           '<w:insideH w:val="single" w:sz="4" w:color="808080"/>'
           '<w:insideV w:val="single" w:sz="4" w:color="808080"/>'
           '</w:tblBorders></w:tblPr>' % total]
    out.append('<w:tblGrid>' + ('<w:gridCol w:w="%d"/>' % cw) * ncol + '</w:tblGrid>')
    # header row
    out.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
    for hcell in headers:
        out.append(cell(hcell, bold=True, width=cw))
    out.append('</w:tr>')
    # data rows
    for r in rows:
        out.append('<w:tr>')
        cells = list(r) + [''] * (ncol - len(r))
        for i, val in enumerate(cells[:ncol]):
            out.append(cell(val, width=cw))
        out.append('</w:tr>')
    out.append('</w:tbl>')
    return ''.join(out)


# =========================================================================
# Minimal LaTeX -> OMML (Word equation) converter
# Handles the constructs used in this manuscript:
#   \frac, \tfrac, subscripts _, superscripts ^, \sqrt, \int, \sum,
#   \left \right delimiters, Greek letters, \text{}, \overline, spacing.
# =========================================================================
M_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

GREEK = {
    'alpha': '\u03b1', 'beta': '\u03b2', 'gamma': '\u03b3', 'delta': '\u03b4',
    'Delta': '\u0394', 'theta': '\u03b8', 'Theta': '\u0398', 'lambda': '\u03bb',
    'mu': '\u03bc', 'nu': '\u03bd', 'pi': '\u03c0', 'rho': '\u03c1',
    'sigma': '\u03c3', 'tau': '\u03c4', 'phi': '\u03c6', 'Phi': '\u03a6',
    'psi': '\u03c8', 'Psi': '\u03a8', 'omega': '\u03c9',
}
SYMS = {
    'times': '\u00d7', 'cdot': '\u00b7', 'approx': '\u2248', 'partial': '\u2202',
    'infty': '\u221e', 'le': '\u2264', 'ge': '\u2265', 'pm': '\u00b1',
    'qquad': '\u2003\u2003', 'quad': '\u2003',
}


def _mtxt(s):
    return '<m:r><m:t xml:space="preserve">%s</m:t></m:r>' % esc(s)


def _tokenize(s):
    """Split a LaTeX string into tokens (commands, braces, chars)."""
    toks = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == '\\':
            j = i + 1
            if j < n and not s[j].isalpha():
                toks.append(('cmd', s[j])); i = j + 1; continue
            k = j
            while k < n and s[k].isalpha():
                k += 1
            toks.append(('cmd', s[j:k])); i = k; continue
        elif c in '{}^_&':
            toks.append((c, c)); i += 1; continue
        elif c.isspace():
            i += 1; continue
        else:
            toks.append(('chr', c)); i += 1; continue
    return toks


def _parse_group(toks, i):
    """Parse a { ... } group starting at token i (which is '{'); return (nodes, next_i)."""
    assert toks[i][0] == '{'
    i += 1
    nodes, i = _parse_seq(toks, i, stop='}')
    return nodes, i + 1  # skip closing brace


def _parse_atom(toks, i):
    """Parse a single atom -> (omml_string, next_i)."""
    typ, val = toks[i]
    if typ == '{':
        nodes, ni = _parse_group(toks, i)
        return ''.join(nodes), ni
    if typ == 'cmd':
        if val in ('frac', 'tfrac'):
            num, i2 = _parse_atom(toks, i + 1)
            den, i3 = _parse_atom(toks, i2)
            frac = ('<m:f><m:fPr><m:type m:val="bar"/></m:fPr>'
                    '<m:num>%s</m:num><m:den>%s</m:den></m:f>' % (num, den))
            return frac, i3
        if val == 'sqrt':
            rad, i2 = _parse_atom(toks, i + 1)
            return '<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>%s</m:e></m:rad>' % rad, i2
        if val == 'overline':
            arg, i2 = _parse_atom(toks, i + 1)
            return '<m:bar><m:barPr><m:pos m:val="top"/></m:barPr><m:e>%s</m:e></m:bar>' % arg, i2
        if val == 'text':
            arg_nodes, i2 = _parse_group(toks, i + 1)
            # flatten text group into plain string
            return arg_nodes if isinstance(arg_nodes, str) else ''.join(arg_nodes), i2
        if val in ('left', 'right'):
            # delimiter marker handled in sequence; emit the following char literally
            return '', i + 1
        if val == 'int':
            return '<m:nary><m:naryPr><m:chr m:val="\u222b"/><m:limLoc m:val="subSup"/></m:naryPr>%s</m:nary>', i + 1
        if val == 'sum':
            return '<m:nary><m:naryPr><m:chr m:val="\u2211"/><m:limLoc m:val="undOvr"/></m:naryPr>%s</m:nary>', i + 1
        if val in GREEK:
            return _mtxt(GREEK[val]), i + 1
        if val in SYMS:
            return _mtxt(SYMS[val]), i + 1
        # unknown command: emit its name
        return _mtxt(val), i + 1
    if typ == 'chr':
        return _mtxt(val), i + 1
    # stray brace or operator
    return _mtxt(val), i + 1


def _parse_seq(toks, i, stop=None):
    """Parse a sequence, honoring _ and ^; return (list_of_omml, next_i)."""
    out = []
    n = len(toks)
    while i < n:
        typ, val = toks[i]
        if stop is not None and typ == stop:
            return out, i
        if typ == '^' or typ == '_':
            base = out.pop() if out else _mtxt('')
            script, i2 = _parse_atom(toks, i + 1)
            # check for the other script immediately following (sub+sup)
            if i2 < n and toks[i2][0] in ('^', '_') and toks[i2][0] != typ:
                other, i3 = _parse_atom(toks, i2 + 1)
                if typ == '_':
                    sub, sup = script, other
                else:
                    sub, sup = other, script
                node = ('<m:sSubSup><m:e>%s</m:e><m:sub>%s</m:sub><m:sup>%s</m:sup></m:sSubSup>'
                        % (base, sub, sup))
                out.append(node); i = i3; continue
            if typ == '_':
                node = '<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>' % (base, script)
            else:
                node = '<m:sSup><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>' % (base, script)
            out.append(node); i = i2; continue
        if typ == 'cmd' and val in ('int', 'sum'):
            nary, i2 = _parse_atom(toks, i)
            # optional _ and ^ for limits
            sub = sup = ''
            if i2 < n and toks[i2][0] == '_':
                sub, i2 = _parse_atom(toks, i2 + 1)
            if i2 < n and toks[i2][0] == '^':
                sup, i2 = _parse_atom(toks, i2 + 1)
            # the integrand: next atom
            integ, i3 = _parse_atom(toks, i2) if i2 < n else ('', i2)
            sub_xml = '<m:sub>%s</m:sub>' % sub if sub else '<m:sub/>'
            sup_xml = '<m:sup>%s</m:sup>' % sup if sup else '<m:sup/>'
            filled = nary.replace('</m:naryPr>', '</m:naryPr>%s%s<m:e>%s</m:e>' % (sub_xml, sup_xml, integ))
            out.append(filled); i = i3; continue
        atom, i2 = _parse_atom(toks, i)
        if atom:
            out.append(atom)
        i = i2
    return out, i


def latex_to_omml(latex):
    """Convert a (single) LaTeX expression to an OMML oMath fragment."""
    # strip \tag and \! (negative thin space) and \, \; spacing to visible spaces
    latex = re.sub(r'\\tag\{[^}]*\}', '', latex)
    latex = latex.replace('\\!', '').replace('\\,', ' ').replace('\\;', ' ')
    latex = latex.replace('\\big', '').replace('\\Big', '')
    toks = _tokenize(latex)
    nodes, _ = _parse_seq(toks, 0)
    return ''.join(nodes)


def equation_para(latex, tag):
    """Return a paragraph containing a centered OMML equation with a right-aligned tag."""
    omml_body = latex_to_omml(latex)
    tag_run = _mtxt('     (%s)' % tag) if tag else ''
    return (
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
        '<m:oMathPara xmlns:m="%s"><m:oMath>%s%s</m:oMath></m:oMathPara>'
        '</w:p>' % (M_NS, omml_body, tag_run)
    )


def parse_markdown(md):
    """Yield content tuples, grouping $$...$$ blocks into ('eq', latex)."""
    lines = md.split('\n')
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i].rstrip()
        line = raw
        stripped = line.strip()
        # equation block: starts with $$ (possibly whole eq on one line)
        if stripped.startswith('$$'):
            # collect until closing $$
            buf = [stripped]
            # single-line $$ ... $$
            if stripped.count('$$') >= 2:
                content = stripped.strip('$').strip()
                yield ('eq', content)
                i += 1
                continue
            i += 1
            while i < n and '$$' not in lines[i]:
                buf.append(lines[i].strip())
                i += 1
            if i < n:
                buf.append(lines[i].strip())
                i += 1
            joined = ' '.join(buf).replace('$$', ' ').strip()
            yield ('eq', joined)
            continue
        if not line:
            yield ('blank', '')
        elif line.startswith('### '):
            yield ('h3', line[4:].strip())
        elif line.startswith('## '):
            yield ('h2', line[3:].strip())
        elif line.startswith('# '):
            yield ('title', line[2:].strip())
        else:
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            clean = re.sub(r'\*([^*]+)\*', r'\1', clean)
            yield ('p', clean)
        i += 1


def main():
    md = open(MD, encoding='utf-8').read()

    body = []
    rels = []
    media = {}  # arcname -> bytes
    rid_counter = [100]

    figs_done = set()
    tabs_done = set()

    def add_figure(num):
        fname, caption = FIGURES[num]
        path = os.path.join(FIGDIR, fname)
        w, h = png_size(path)
        rid_counter[0] += 1
        rid = 'rId%d' % rid_counter[0]
        arc = 'word/media/%s' % fname
        media[arc] = open(path, 'rb').read()
        rels.append((rid, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', 'media/%s' % fname))
        body.append(empty_para())
        body.append(image_para(rid_counter[0], w, h))
        body.append(para(caption, italic=True, size=18, align='center'))
        body.append(empty_para())

    def add_table(num):
        tdef = TABLES[num]
        body.append(empty_para())
        body.append(para(tdef['caption'], bold=True, size=18))
        body.append(build_table(tdef))
        body.append(empty_para())

    for kind, text in parse_markdown(md):
        if kind == 'title':
            body.append(para(text, style='Title', bold=True, size=32))
        elif kind == 'h2':
            body.append(para(text, style='Heading1', bold=True, size=28))
        elif kind == 'h3':
            body.append(para(text, style='Heading2', bold=True, size=24))
        elif kind == 'blank':
            pass  # spacing handled by styles
        elif kind == 'eq':
            m = re.search(r'\\tag\{(\d+)\}', text)
            tag = m.group(1) if m else ''
            body.append(equation_para(text, tag))
        else:
            body.append(para(text))
            # after adding a paragraph, check for first figure/table citations
            for num in sorted(FIGURES):
                if num not in figs_done and re.search(r'\bFigure %d\b' % num, text):
                    figs_done.add(num)
                    add_figure(num)
            for num in sorted(TABLES):
                if num not in tabs_done and re.search(r'\bTable %d\b' % num, text):
                    tabs_done.add(num)
                    add_table(num)

    # any figures/tables not yet placed (safety) -> append at end
    for num in sorted(FIGURES):
        if num not in figs_done:
            add_figure(num)
    for num in sorted(TABLES):
        if num not in tabs_done:
            add_table(num)

    body_xml = '\n'.join(body)

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<w:body>' + body_xml +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        '</w:sectPr></w:body></w:document>'
    )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '</Types>'
    )

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>'
    )

    rels_xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, rtype, target in rels:
        rels_xml.append('<Relationship Id="%s" Type="%s" Target="%s"/>' % (rid, rtype, target))
    rels_xml.append('</Relationships>')
    word_rels = ''.join(rels_xml)

    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
        '<w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
        '<w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
        '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
        '<w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
        '<w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr></w:style>'
        '</w:styles>'
    )

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', root_rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)
        for arc, data in media.items():
            zf.writestr(arc, data)

    print('Created %s' % OUT)
    print('Figures embedded: %s' % sorted(figs_done))
    print('Tables embedded:  %s' % sorted(tabs_done))


if __name__ == '__main__':
    main()
