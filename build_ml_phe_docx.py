#!/usr/bin/env python3
"""
Build the ML / TiO2-Al2O3 PHE manuscript as a .docx (pure stdlib).

Features:
  - Markdown body -> Word paragraphs/headings
  - Native Word tables (5 tables)
  - Embedded PNG figures (7 figures) with captions
  - 18 governing equations rendered as native Word equation-editor objects
    (OMML / Office Math), numbered, each followed by a word-form statement
  - Chemical formulas (TiO2, Al2O3, H2O, ...) with real subscripts in text
  - Inline symbols wrapped in $...$ emitted as inline OMML equation objects
Markers inside the markdown:
  [[FIGUREn]] [[TABLEn]] [[EQn]]  ;  inline math via $...$
"""

import os
import re
import struct
import zipfile

import omml as o
from equations_omml import EQUATIONS as OMML_EQUATIONS

ROOT = '/projects/sandbox/AMMAN'
MD = os.path.join(ROOT, 'ML_Hybrid_Nanofluid_PHE_Manuscript.md')
FIGDIR = os.path.join(ROOT, 'ml_phe_figures')
OUT = os.path.join(ROOT, 'ML_Hybrid_Nanofluid_PHE_Manuscript.docx')

EMU_PER_PX = 9525  # at 96 dpi


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------
def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


# chemical formulas that must get proper subscripts in running text.
# order matters: longer / combined tokens first.
CHEM_PATTERN = re.compile(
    r'(TiO2|Al2O3|SiO2|Fe3O4|CuO|ZnO|H2O|CO2)'
)


def _chem_runs(token, bold=False):
    """Render a chemical formula as Word runs with real subscripts for digits."""
    runs = []
    b = '<w:b/>' if bold else ''
    for ch in token:
        if ch.isdigit():
            runs.append('<w:r><w:rPr>%s<w:vertAlign w:val="subscript"/></w:rPr>'
                        '<w:t xml:space="preserve">%s</w:t></w:r>' % (b, ch))
        else:
            rpr = '<w:rPr>%s</w:rPr>' % b if b else ''
            runs.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
                        % (rpr, esc(ch)))
    return ''.join(runs)


def _text_runs_with_chem(text, bold=False):
    """Split plain text on chemical formulas; emit subscripted chem + normal runs."""
    out = []
    pos = 0
    b = '<w:b/>' if bold else ''
    for m in CHEM_PATTERN.finditer(text):
        if m.start() > pos:
            seg = text[pos:m.start()]
            rpr = '<w:rPr>%s</w:rPr>' % b if b else ''
            out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
                       % (rpr, esc(seg)))
        out.append(_chem_runs(m.group(0), bold=bold))
        pos = m.end()
    if pos < len(text):
        rpr = '<w:rPr>%s</w:rPr>' % b if b else ''
        out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
                   % (rpr, esc(text[pos:])))
    return ''.join(out)


def _inline_math(expr):
    """Return an inline <m:oMath> object for a $...$ span."""
    return o.omml_inline(expr)


def runs_from_inline(text):
    """Convert markup into Word runs.
    Handles: **bold**, $inline math$, and chemical-formula subscripts.
    """
    out = []
    # split on bold first, keeping delimiters
    for seg in re.split(r'(\*\*[^*]+\*\*)', text):
        if not seg:
            continue
        bold = seg.startswith('**') and seg.endswith('**')
        content = seg[2:-2] if bold else seg
        # within each (bold or normal) chunk, split on $...$ math spans
        for piece in re.split(r'(\$[^$]+\$)', content):
            if not piece:
                continue
            if piece.startswith('$') and piece.endswith('$'):
                out.append(_inline_math(piece[1:-1]))
            else:
                out.append(_text_runs_with_chem(piece, bold=bold))
    return ''.join(out)


def para(text, style=None, bold=False, size=None, jc=None, italic=False):
    rpr = ''
    inner = '<w:b/>' if bold else ''
    if italic:
        inner += '<w:i/>'
    if size:
        inner += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size)
    if inner:
        rpr = '<w:rPr>%s</w:rPr>' % inner
    ppr_parts = []
    if style:
        ppr_parts.append('<w:pStyle w:val="%s"/>' % style)
    if jc:
        ppr_parts.append('<w:jc w:val="%s"/>' % jc)
    ppr = '<w:pPr>%s</w:pPr>' % ''.join(ppr_parts) if ppr_parts else ''
    # route text through chem-aware runs so TiO2/Al2O3 etc. get subscripts,
    # carrying the paragraph's run properties (bold/size/italic) onto each run.
    rbody = _runs_with_props(text, rpr)
    return '<w:p>%s%s</w:p>' % (ppr, rbody)


def _runs_with_props(text, rpr):
    """Emit chem-aware runs that all share the given <w:rPr> block."""
    runs = []
    pos = 0
    for m in CHEM_PATTERN.finditer(text):
        if m.start() > pos:
            runs.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
                        % (rpr, esc(text[pos:m.start()])))
        for ch in m.group(0):
            if ch.isdigit():
                # merge subscript flag into existing rPr
                sub_rpr = _merge_rpr(rpr, '<w:vertAlign w:val="subscript"/>')
                runs.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
                            % (sub_rpr, ch))
            else:
                runs.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
                            % (rpr, esc(ch)))
        pos = m.end()
    if pos < len(text):
        runs.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
                    % (rpr, esc(text[pos:])))
    return ''.join(runs)


def _merge_rpr(rpr, extra):
    if not rpr:
        return '<w:rPr>%s</w:rPr>' % extra
    return rpr.replace('</w:rPr>', extra + '</w:rPr>')


def para_runs(text, jc='both'):
    ppr = '<w:pPr><w:jc w:val="%s"/></w:pPr>' % jc
    return '<w:p>%s%s</w:p>' % (ppr, runs_from_inline(text))


def empty_para():
    return '<w:p/>'


# ---------------------------------------------------------------------------
# PNG size
# ---------------------------------------------------------------------------
def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(26)
    assert head[:8] == b'\x89PNG\r\n\x1a\n'
    w, h = struct.unpack('>II', head[16:24])
    return w, h


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
FIGURES = {
    'FIGURE1': ('Figure_1_Workflow.png',
                'Figure 1. Methodology workflow of the proposed ML-based multi-target '
                'predictive framework for the TiO2-Al2O3/water hybrid nanofluid in a PHE.'),
    'FIGURE2': ('Figure_2_h_vs_Re.png',
                'Figure 2. Variation of the convection coefficient h with Reynolds number '
                'for the five TiO2:Al2O3 ratios at a total loading of 0.10 vol.%.'),
    'FIGURE3': ('Figure_3_loading.png',
                'Figure 3. (a) Convection coefficient versus Reynolds number for the 0:5 '
                'ratio at loadings of 0.01-0.20 vol.%. (b) Percentage enhancement of h '
                'relative to water versus total loading for the five mixture ratios (Re = 1200).'),
    'FIGURE4': ('Figure_4_friction_tpf.png',
                'Figure 4. (a) Friction factor versus Reynolds number for water and for the '
                '0:5 composition at three loadings. (b) Thermal performance factor versus '
                'loading for the five mixture ratios (Re = 1200); the dotted line marks eta = 1.'),
    'FIGURE5': ('Figure_5_parity.png',
                'Figure 5. Parity plots of predicted versus experimental values for h, Nu and '
                'f using the XGBoost multi-target model (test set, n = 75). Red dashed lines '
                'denote the +/-10% error bands.'),
    'FIGURE6': ('Figure_6_model_compare.png',
                'Figure 6. (a) Coefficient of determination and (b) normalised RMSE of the '
                'four benchmarked models for the three prediction targets.'),
    'FIGURE7': ('Figure_7_importance_benchmark.png',
                'Figure 7. (a) Permutation importance (mean decrease in R-squared) of the five '
                'input features for each target; negative values clipped to zero. (b) Predictive '
                'accuracy of classical correlations versus the proposed XGBoost framework.'),
}

# relationship ids assigned per figure
FIG_ORDER = ['FIGURE1', 'FIGURE2', 'FIGURE3', 'FIGURE4', 'FIGURE5', 'FIGURE6', 'FIGURE7']


def figure_xml(key, rid, max_w_px=600):
    fname, caption = FIGURES[key]
    path = os.path.join(FIGDIR, fname)
    w, h = png_size(path)
    if w > max_w_px:
        scale = max_w_px / w
        w2, h2 = int(w * scale), int(h * scale)
    else:
        w2, h2 = w, h
    cx, cy = w2 * EMU_PER_PX, h2 * EMU_PER_PX
    drawing = (
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0">'
        '<wp:extent cx="%d" cy="%d"/>'
        '<wp:docPr id="%d" name="%s"/>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
        % (cx, cy, FIG_ORDER.index(key) + 1, fname,
           FIG_ORDER.index(key) + 1, fname, rid, cx, cy)
    )
    cap = ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="200"/></w:pPr>'
           '<w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p>'
           % esc(caption))
    return empty_para() + drawing + cap


# ---------------------------------------------------------------------------
# Tables (native Word tables)
# ---------------------------------------------------------------------------
def tbl(headers, rows, caption, widths=None):
    ncol = len(headers)
    if widths is None:
        widths = [int(9360 / ncol)] * ncol
    grid = ''.join('<w:gridCol w:w="%d"/>' % w for w in widths)

    def cell(text, w, bold=False, shade=None):
        rpr = '<w:rPr><w:b/><w:sz w:val="20"/></w:rPr>' if bold else '<w:rPr><w:sz w:val="20"/></w:rPr>'
        tcpr = '<w:tcW w:w="%d" w:type="dxa"/>' % w
        if shade:
            tcpr += '<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade
        tcpr += '<w:vAlign w:val="center"/>'
        return ('<w:tc><w:tcPr>%s</w:tcPr><w:p><w:pPr><w:spacing w:after="0"/></w:pPr>'
                '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p></w:tc>'
                % (tcpr, rpr, esc(str(text))))

    head_cells = ''.join(cell(h, widths[i], bold=True, shade='D9E2F3') for i, h in enumerate(headers))
    head_row = '<w:tr><w:trPr><w:tblHeader/></w:trPr>%s</w:tr>' % head_cells
    body = ''
    for r in rows:
        cells = ''.join(cell(v, widths[i]) for i, v in enumerate(r))
        body += '<w:tr>%s</w:tr>' % cells
    borders = ('<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '</w:tblBorders>')
    tblpr = '<w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:jc w:val="center"/>%s</w:tblPr>' % borders
    table = ('<w:tbl>%s<w:tblGrid>%s</w:tblGrid>%s%s</w:tbl>'
             % (tblpr, grid, head_row, body))
    cap = ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="160" w:after="60"/></w:pPr>'
           '<w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p>'
           % esc(caption))
    return cap + table + empty_para()


TABLES = {
    'TABLE1': lambda: tbl(
        ['Type', 'Variable', 'Symbol', 'Range / basis'],
        [['Input', 'Mixture ratio', 'TiO2:Al2O3', '0:5 to 4:1'],
         ['Input', 'Particle loading', 'phi (vol.%)', '0.01 to 0.20'],
         ['Input', 'Flow rate / Reynolds number', 'm-dot, Re', '500 to 2000 (5 settings)'],
         ['Input', 'Inlet temperatures', 'T_hi, T_ci', '30 to 60 C'],
         ['Input', 'Thermal conductivity', 'k_nf', 'measured (hot-wire)'],
         ['Target', 'Convection coefficient', 'h (W/m2K)', 'LMTD extraction'],
         ['Target', 'Nusselt number', 'Nu', 'h*D_h / k_nf'],
         ['Target', 'Friction factor', 'f', 'pressure-drop based']],
        'Table 1. Input features and prediction targets of the multi-target framework.',
        widths=[1200, 3400, 1900, 2860]),

    'TABLE2': lambda: tbl(
        ['Quantity', 'Relation / value used', 'Source'],
        [['Effective density', 'volume-weighted mixing rule, Eq. (1)', 'validated at low phi [9]'],
         ['Effective specific heat', 'heat-capacity balance, Eq. (2)', 'validated at low phi [9]'],
         ['Thermal conductivity', 'measured (transient hot-wire)', 'this work'],
         ['Dynamic viscosity', 'measured (rotational rheometer, 20-60 C)', 'this work'],
         ['Cold-side coefficient', 'validated water-side correlation', '[1,9]'],
         ['Wall resistance', 'plate thickness / (k_plate * A)', 'standard'],
         ['Hydraulic diameter, D_h', 'fixed chevron channel geometry', '[1,9]'],
         ['Reynolds / Prandtl number', 'Eq. (3), Eq. (4)', 'standard definitions']],
        'Table 2. Thermophysical property relations and fixed parameters used in the data reduction.',
        widths=[2600, 4300, 2460]),

    'TABLE3': lambda: tbl(
        ['Model', 'Key hyperparameters (search space)', 'Selected value'],
        [['BR-ANN', 'hidden layers {1,2}; neurons/layer {5-25}; activation tanh-sig',
          '2 layers, 10-20 neurons, Levenberg-Marquardt'],
         ['Random forest', 'trees {100-800}; max depth {4-16}; min leaf {1-5}',
          '400 trees, depth 12'],
         ['XGBoost', 'trees {200-1000}; depth {3-10}; lr {0.01-0.3}; lambda {0-5}',
          '600 trees, depth 6, lr 0.05, lambda 1'],
         ['SVR (RBF)', 'C {1-1000}; epsilon {0.001-0.1}; gamma {scale, 0.01-1}',
          'C=100, epsilon=0.01, gamma=scale']],
        'Table 3. Hyperparameter search space and values selected by five-fold cross-validation.',
        widths=[1600, 4600, 3160]),

    'TABLE4': lambda: tbl(
        ['Model', 'R2 (h)', 'R2 (Nu)', 'R2 (f)', 'RMSE (h)', 'RMSE (Nu)', 'RMSE (f)', 'MAPE h/Nu/f (%)'],
        [['XGBoost', '0.9969', '0.9969', '0.9831', '9.40', '0.0736', '0.0033', '1.37 / 1.33 / 1.95'],
         ['BR-ANN', '0.9964', '0.9964', '0.9784', '10.17', '0.0795', '0.0038', '1.50 / 1.56 / 2.04'],
         ['RF', '0.9952', '0.9952', '0.9827', '11.71', '0.0915', '0.0034', '1.74 / 1.73 / 1.83'],
         ['SVR', '0.9943', '0.9942', '0.9626', '12.73', '0.1004', '0.0050', '1.78 / 1.78 / 2.81']],
        'Table 4. Test-set performance of the benchmarked multi-target models.',
        widths=[1200, 950, 950, 950, 1050, 1150, 1050, 2060]),

    'TABLE5': lambda: tbl(
        ['Target', 'Classical correlation R2', 'XGBoost R2', 'Gain (pp)', 'XGBoost NRMSE (%)'],
        [['h', '0.913', '0.9969', '+8.4', '1.71'],
         ['Nu', '0.934', '0.9969', '+6.3', '1.70'],
         ['f', '0.872', '0.9831', '+11.1', '2.34']],
        'Table 5. Benchmark of the ML framework against classical nanofluid correlations '
        '(pp = percentage points of R-squared).',
        widths=[1500, 2600, 1800, 1500, 1960]),
}




def equation_xml(key):
    """Render a display equation as a native Word equation (OMML) with a
    right-aligned equation number, using a borderless 3-column table so the
    equation stays centred and the number sits at the right margin."""
    frag, words, num = OMML_EQUATIONS[key]
    omath = o.omath(frag)

    # borderless table: [spacer | centred equation | right number]
    cell_math = (
        '<w:tc><w:tcPr><w:tcW w:w="7800" w:type="dxa"/></w:tcPr>'
        '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="0"/></w:pPr>'
        '%s</w:p></w:tc>' % omath)
    cell_num = (
        '<w:tc><w:tcPr><w:tcW w:w="1560" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
        '<w:p><w:pPr><w:jc w:val="right"/><w:spacing w:after="0"/></w:pPr>'
        '<w:r><w:t xml:space="preserve">(%d)</w:t></w:r></w:p></w:tc>' % num)
    nobord = ('<w:tblBorders>'
              '<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
              '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
              '<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
              '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
              '<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
              '<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
              '</w:tblBorders>')
    table = (
        '<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:jc w:val="center"/>'
        '%s</w:tblPr>'
        '<w:tblGrid><w:gridCol w:w="7800"/><w:gridCol w:w="1560"/></w:tblGrid>'
        '<w:tr>%s%s</w:tr></w:tbl>' % (nobord, cell_math, cell_num))

    wf = ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="40" w:after="140"/></w:pPr>'
          '<w:r><w:rPr><w:sz w:val="20"/><w:i/></w:rPr>'
          '<w:t xml:space="preserve">In words: %s.</w:t></w:r></w:p>'
          % esc(words[0].upper() + words[1:]))
    return empty_para() + table + wf


# ---------------------------------------------------------------------------
# Markdown -> body
# ---------------------------------------------------------------------------
def build_body():
    with open(MD) as f:
        lines = f.read().split('\n')
    parts = []
    rid_map = {}  # figure key -> rId
    rid_counter = 10
    i = 0
    first_h1 = True
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()
        if not stripped:
            parts.append(empty_para())
            i += 1
            continue
        m = re.match(r'^\[\[([A-Z0-9]+)\]\]$', stripped)
        if m:
            key = m.group(1)
            if key in FIGURES:
                rid = 'rId%d' % rid_counter
                rid_map[key] = rid
                rid_counter += 1
                parts.append(figure_xml(key, rid))
            elif key in TABLES:
                parts.append(TABLES[key]())
            elif key in OMML_EQUATIONS:
                parts.append(equation_xml(key))
            i += 1
            continue
        if line.startswith('# '):
            parts.append(para(line[2:].strip(), style='Title', bold=True, size=32, jc='center'))
        elif line.startswith('## '):
            parts.append(para(line[3:].strip(), style='Heading1', bold=True, size=28))
        elif line.startswith('### '):
            parts.append(para(line[4:].strip(), style='Heading2', bold=True, size=24))
        elif stripped.startswith('**') and stripped.endswith('**') and stripped.count('**') == 2:
            parts.append(para(stripped.strip('*'), bold=True))
        elif re.match(r'^\d+\.\s', stripped):
            # numbered reference line
            parts.append(para_runs(stripped, jc='both'))
        else:
            parts.append(para_runs(stripped, jc='both'))
        i += 1
    return ''.join(parts), rid_map


# ---------------------------------------------------------------------------
# Assemble docx
# ---------------------------------------------------------------------------
def build():
    body, rid_map = build_body()

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '</Types>')

    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')

    # word/_rels: styles + one per image
    word_rel_items = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    media_files = []
    for key, rid in rid_map.items():
        fname = FIGURES[key][0]
        word_rel_items.append(
            '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/%s"/>'
            % (rid, fname))
        media_files.append(fname)
    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 + ''.join(word_rel_items) + '</Relationships>')

    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>'
        '<w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>'
        '<w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>'
        '<w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>'
        '<w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr></w:style>'
        '</w:styles>')

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<w:body>' + body +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
        '</w:body></w:document>')

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('word/_rels/document.xml.rels', word_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', styles)
        for fname in media_files:
            with open(os.path.join(FIGDIR, fname), 'rb') as f:
                z.writestr('word/media/%s' % fname, f.read())
    print('Wrote', OUT)
    print('Embedded figures:', len(media_files))


if __name__ == '__main__':
    build()
