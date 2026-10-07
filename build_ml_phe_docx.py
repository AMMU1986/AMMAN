#!/usr/bin/env python3
"""
Build the ML / TiO2-Al2O3 PHE manuscript as a .docx (pure stdlib).

Features:
  - Markdown body -> Word paragraphs/headings
  - Native Word tables (5 tables)
  - Embedded PNG figures (7 figures) with captions
  - 18 governing equations rendered as centered, numbered, word-form statements
Markers inside the markdown:
  [[FIGUREn]] [[TABLEn]] [[EQn]]
"""

import os
import re
import struct
import zipfile

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


def runs_from_inline(text):
    """Convert **bold** markup into runs; return run XML."""
    out = []
    for i, seg in enumerate(re.split(r'(\*\*[^*]+\*\*)', text)):
        if not seg:
            continue
        if seg.startswith('**') and seg.endswith('**'):
            inner = esc(seg[2:-2])
            out.append('<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % inner)
        else:
            out.append('<w:r><w:t xml:space="preserve">%s</w:t></w:r>' % esc(seg))
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
    return ('<w:p>%s<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (ppr, rpr, esc(text)))


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


# ---------------------------------------------------------------------------
# Equations (word form, centered + numbered)
# ---------------------------------------------------------------------------
EQUATIONS = {
    'EQ1': ('rho_nf  =  (1 - phi_1 - phi_2) * rho_bf  +  phi_1 * rho_p1  +  phi_2 * rho_p2',
            'mixture density equals base-fluid volume fraction times base-fluid density, '
            'plus each particle volume fraction times its solid density', 1),
    'EQ2': ('(rho * c_p)_nf  =  (1 - phi_1 - phi_2)(rho * c_p)_bf  +  phi_1 (rho * c_p)_p1  +  phi_2 (rho * c_p)_p2',
            'the product of mixture density and specific heat equals the volume-weighted sum of '
            'the density-specific-heat products of base fluid and particles', 2),
    'EQ3': ('Re  =  (G * D_h) / mu_nf',
            'Reynolds number equals channel mass flux times hydraulic diameter divided by dynamic viscosity', 3),
    'EQ4': ('Pr  =  (mu_nf * c_p,nf) / k_nf',
            'Prandtl number equals dynamic viscosity times specific heat divided by thermal conductivity', 4),
    'EQ5': ('Q  =  m-dot * c_p * (T_in - T_out)',
            'heat duty equals mass flow rate times specific heat times the inlet-to-outlet temperature difference', 5),
    'EQ6': ('U  =  Q / (A * LMTD)',
            'overall heat-transfer coefficient equals heat duty divided by the product of area and '
            'log-mean temperature difference', 6),
    'EQ7': ('LMTD  =  (dT_1 - dT_2) / ln(dT_1 / dT_2)',
            'log-mean temperature difference equals the difference of the terminal temperature differences '
            'divided by the natural logarithm of their ratio', 7),
    'EQ8': ('1 / (U * A)  =  1 / (h_h * A)  +  t_w / (k_w * A)  +  1 / (h_c * A)',
            'overall thermal resistance equals the hot-side convective resistance plus the plate-wall '
            'conduction resistance plus the cold-side convective resistance', 8),
    'EQ9': ('Nu  =  (h * D_h) / k_nf',
            'Nusselt number equals the convective coefficient times hydraulic diameter divided by '
            'nanofluid thermal conductivity', 9),
    'EQ10': ('f  =  (dP * D_h * 2 * rho) / (L * G^2)',
             'Darcy friction factor equals pressure drop times hydraulic diameter times twice the density, '
             'divided by channel length times the square of the mass flux', 10),
    'EQ11': ('eta  =  (h_nf / h_w) / (f_nf / f_w)^(1/3)',
             'thermal performance factor equals the convective-coefficient ratio divided by the cube root '
             'of the friction-factor ratio', 11),
    'EQ12': ('keep x  if  Q1 - 1.5*IQR  <=  x  <=  Q3 + 1.5*IQR',
             'an observation is retained only if it lies within 1.5 interquartile ranges of the first and '
             'third quartiles', 12),
    'EQ13': ('x_norm  =  (x - x_min) / (x_max - x_min)',
             'the normalised feature equals the raw value minus its minimum divided by the span between '
             'its maximum and minimum', 13),
    'EQ14': ('F(w)  =  beta * sum(e_i^2)  +  alpha * sum(w_j^2)',
             'the Bayesian-regularised objective equals a weighted sum of squared errors plus a weighted '
             'sum of squared network weights', 14),
    'EQ15': ('y_RF  =  (1 / B) * sum over b of  T_b(x)',
             'the random-forest prediction equals the arithmetic mean of the outputs of the B bootstrap trees', 15),
    'EQ16': ('F_m(x)  =  F_(m-1)(x)  +  nu * h_m(x),   h_m fit to the negative gradient of the regularised loss',
             'each boosting stage adds a shrunk tree fitted to the negative gradient of a '
             'complexity-penalised loss', 16),
    'EQ17': ('minimise  (1/2)||w||^2 + C * sum(xi_i + xi_i*)   subject to the epsilon-insensitive tube',
             'support-vector regression minimises model complexity plus a penalty on deviations that '
             'exceed the epsilon-insensitive tube', 17),
    'EQ18': ('R^2  =  1 - ( sum(y_i - y_hat_i)^2 / sum(y_i - y_bar)^2 )',
             'the coefficient of determination equals one minus the residual sum of squares divided by '
             'the total sum of squares', 18),
}


def equation_xml(key):
    formula, words, num = EQUATIONS[key]
    # centered symbolic line in italic, with right-aligned equation number via tab
    sym = ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="20"/></w:pPr>'
           '<w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>'
           '<w:r><w:tab/><w:t xml:space="preserve">(%d)</w:t></w:r></w:p>'
           % (esc(formula), num))
    wf = ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="140"/></w:pPr>'
          '<w:r><w:rPr><w:sz w:val="20"/></w:rPr>'
          '<w:t xml:space="preserve">In words: %s.</w:t></w:r></w:p>'
          % esc(words[0].upper() + words[1:]))
    return sym + wf


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
            elif key in EQUATIONS:
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
