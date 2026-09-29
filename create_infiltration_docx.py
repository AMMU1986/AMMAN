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


def parse_markdown(md):
    """Yield ('h1'|'h2'|'h3'|'title'|'p'|'blank', text) tuples."""
    for raw in md.split('\n'):
        line = raw.rstrip()
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
