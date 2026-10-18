#!/usr/bin/env python3
"""
Build an Excel workbook (.xlsx) for the API X70 SMAW hydrogen-charged
microhardness study, with native in-cell charts.

No third-party libraries (openpyxl/xlsxwriter unavailable, no network).
An .xlsx is a ZIP of XML parts, which we assemble by hand.

Sheets:
  1. Interpolated_0.1mm  - 161-row traverse (uncharged + charged + SD) with a
                           scatter/line chart (uncharged vs charged vs position)
  2. Region_Summary      - manuscript Table 1 values with a clustered-column
                           chart (uncharged vs charged per region)

Output: microhardness_hydrogen_charging.xlsx
"""

import os
import zipfile

from hydrogen_charged_microhardness import (
    build_grid, region_stats, REGION_NAME, REGION_ORDER,
)

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'microhardness_hydrogen_charging.xlsx')

A = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'


def col(n):
    """0-based column index -> letter(s)."""
    s = ''
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def cell(c, r, value, is_num, style=None):
    ref = f'{c}{r}'
    s = f' s="{style}"' if style is not None else ''
    if is_num:
        return f'<c r="{ref}"{s}><v>{value}</v></c>'
    return f'<c r="{ref}"{s} t="inlineStr"><is><t>{esc(value)}</t></is></c>'


def sheet_xml(header, rows, numeric_cols, drawing_rid='rId1'):
    """header: list[str]; rows: list[list]; numeric_cols: set of col idx that are numbers."""
    out = [A,
           '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
           'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
           '<sheetData>']
    # header
    hc = ''.join(cell(col(i), 1, h, False, style=1) for i, h in enumerate(header))
    out.append(f'<row r="1">{hc}</row>')
    for ri, row in enumerate(rows, start=2):
        cc = ''.join(cell(col(i), ri, v, (i in numeric_cols)) for i, v in enumerate(row))
        out.append(f'<row r="{ri}">{cc}</row>')
    out.append('</sheetData>')
    out.append(f'<drawing r:id="{drawing_rid}"/>')
    out.append('</worksheet>')
    return ''.join(out)


# ---- static parts ---------------------------------------------------------
CONTENT_TYPES = A + (
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
    '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
    '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
    '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
    '<Override PartName="/xl/drawings/drawing1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/>'
    '<Override PartName="/xl/drawings/drawing2.xml" ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/>'
    '<Override PartName="/xl/charts/chart1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.chart+xml"/>'
    '<Override PartName="/xl/charts/chart2.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.chart+xml"/>'
    '</Types>')

ROOT_RELS = A + (
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
    '</Relationships>')

WORKBOOK = A + (
    '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<sheets>'
    '<sheet name="Interpolated_0.1mm" sheetId="1" r:id="rId1"/>'
    '<sheet name="Region_Summary" sheetId="2" r:id="rId2"/>'
    '</sheets></workbook>')

WORKBOOK_RELS = A + (
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '</Relationships>')

STYLES = A + (
    '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
    '<fonts count="2">'
    '<font><sz val="11"/><name val="Calibri"/></font>'
    '<font><b/><sz val="11"/><name val="Calibri"/></font>'
    '</fonts>'
    '<fills count="2"><fill><patternFill patternType="none"/></fill>'
    '<fill><patternFill patternType="gray125"/></fill></fills>'
    '<borders count="1"><border/></borders>'
    '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
    '<cellXfs count="2">'
    '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
    '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>'
    '</cellXfs></styleSheet>')


def drawing_xml(name):
    return A + (
        '<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<xdr:twoCellAnchor>'
        '<xdr:from><xdr:col>8</xdr:col><xdr:colOff>0</xdr:colOff><xdr:row>1</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:from>'
        '<xdr:to><xdr:col>22</xdr:col><xdr:colOff>0</xdr:colOff><xdr:row>30</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:to>'
        '<xdr:graphicFrame macro="">'
        '<xdr:nvGraphicFramePr><xdr:cNvPr id="2" name="' + name + '"/>'
        '<xdr:cNvGraphicFramePr/></xdr:nvGraphicFramePr>'
        '<xdr:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/></xdr:xfrm>'
        '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/chart">'
        '<c:chart xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="rId1"/>'
        '</a:graphicData></a:graphic></xdr:graphicFrame>'
        '<xdr:clientData/></xdr:twoCellAnchor></xdr:wsDr>')


def drawing_rels(chart_target):
    return A + (
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart" Target="{chart_target}"/>'
        '</Relationships>')


def sheet_rels(drawing_target):
    return A + (
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing" Target="{drawing_target}"/>'
        '</Relationships>')


CHART_NS = ('xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')


def title(txt):
    return ('<c:title><c:tx><c:rich><a:bodyPr/><a:lstStyle/>'
            f'<a:p><a:r><a:t>{esc(txt)}</a:t></a:r></a:p></c:rich></c:tx>'
            '<c:overlay val="0"/></c:title>')


def axis_title(txt):
    return ('<c:title><c:tx><c:rich><a:bodyPr/><a:lstStyle/>'
            f'<a:p><a:r><a:t>{esc(txt)}</a:t></a:r></a:p></c:rich></c:tx>'
            '<c:overlay val="0"/></c:title>')


def scatter_chart(sheet, nrows):
    last = nrows + 1  # data rows 2..last

    def ser(idx, name_cell, name, ycolL, color):
        return (
            '<c:ser>'
            f'<c:idx val="{idx}"/><c:order val="{idx}"/>'
            f'<c:tx><c:strRef><c:f>{sheet}!${name_cell}$1</c:f>'
            f'<c:strCache><c:ptCount val="1"/><c:pt idx="0"><c:v>{name}</c:v></c:pt></c:strCache></c:strRef></c:tx>'
            f'<c:spPr><a:ln w="19050"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln></c:spPr>'
            '<c:marker><c:symbol val="none"/></c:marker>'
            f'<c:xVal><c:numRef><c:f>{sheet}!$A$2:$A${last}</c:f></c:numRef></c:xVal>'
            f'<c:yVal><c:numRef><c:f>{sheet}!${ycolL}$2:${ycolL}${last}</c:f></c:numRef></c:yVal>'
            '<c:smooth val="0"/></c:ser>')

    return A + (
        f'<c:chartSpace {CHART_NS}><c:chart>'
        + title('API X70 SMAW Microhardness: Uncharged vs H-Charged')
        + '<c:autoTitleDeleted val="0"/><c:plotArea><c:layout/>'
        '<c:scatterChart><c:scatterStyle val="lineMarker"/><c:varyColors val="0"/>'
        + ser(0, 'C', 'HV_uncharged', 'C', '1F4E79')
        + ser(1, 'E', 'HV_charged', 'E', 'C00000')
        + '<c:axId val="111111111"/><c:axId val="222222222"/></c:scatterChart>'
        '<c:valAx><c:axId val="111111111"/><c:scaling><c:orientation val="minMax"/></c:scaling>'
        '<c:delete val="0"/><c:axPos val="b"/>'
        + axis_title('Distance from weld centreline (mm)')
        + '<c:crossAx val="222222222"/></c:valAx>'
        '<c:valAx><c:axId val="222222222"/><c:scaling><c:orientation val="minMax"/></c:scaling>'
        '<c:delete val="0"/><c:axPos val="l"/>'
        + axis_title('Vickers hardness (HV0.5)')
        + '<c:crossAx val="111111111"/></c:valAx>'
        '</c:plotArea><c:legend><c:legendPos val="t"/><c:overlay val="0"/></c:legend>'
        '<c:plotVisOnly val="1"/><c:dispBlanksAs val="gap"/></c:chart></c:chartSpace>')


def bar_chart(sheet):
    def ser(idx, name_cell, name, valcolL, color):
        return (
            '<c:ser>'
            f'<c:idx val="{idx}"/><c:order val="{idx}"/>'
            f'<c:tx><c:strRef><c:f>{sheet}!${name_cell}$1</c:f>'
            f'<c:strCache><c:ptCount val="1"/><c:pt idx="0"><c:v>{name}</c:v></c:pt></c:strCache></c:strRef></c:tx>'
            f'<c:spPr><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></c:spPr>'
            f'<c:cat><c:strRef><c:f>{sheet}!$A$2:$A$4</c:f></c:strRef></c:cat>'
            f'<c:val><c:numRef><c:f>{sheet}!${valcolL}$2:${valcolL}$4</c:f></c:numRef></c:val>'
            '</c:ser>')

    return A + (
        f'<c:chartSpace {CHART_NS}><c:chart>'
        + title('Representative microhardness by region (Table 1)')
        + '<c:autoTitleDeleted val="0"/><c:plotArea><c:layout/>'
        '<c:barChart><c:barDir val="col"/><c:grouping val="clustered"/><c:varyColors val="0"/>'
        + ser(0, 'B', 'HV_uncharged', 'B', '1F4E79')
        + ser(1, 'D', 'HV_charged', 'D', 'C00000')
        + '<c:axId val="333333333"/><c:axId val="444444444"/></c:barChart>'
        '<c:catAx><c:axId val="333333333"/><c:scaling><c:orientation val="minMax"/></c:scaling>'
        '<c:delete val="0"/><c:axPos val="b"/><c:crossAx val="444444444"/></c:catAx>'
        '<c:valAx><c:axId val="444444444"/><c:scaling><c:orientation val="minMax"/></c:scaling>'
        '<c:delete val="0"/><c:axPos val="l"/>'
        + axis_title('Vickers hardness (HV0.5)')
        + '<c:crossAx val="333333333"/></c:valAx>'
        '</c:plotArea><c:legend><c:legendPos val="t"/><c:overlay val="0"/></c:legend>'
        '<c:plotVisOnly val="1"/></c:chart></c:chartSpace>')


def main():
    rows = build_grid()

    # Sheet 1: interpolated traverse
    s1_header = ['Position_mm', 'Region', 'HV_uncharged', 'SD_uncharged',
                 'HV_charged', 'SD_charged_1.5pct', 'Delta_HV']
    s1_rows = [[r['pos'], r['region'], r['hv_uncharged'], r['sd_uncharged'],
                r['hv_charged'], r['sd_charged'], r['delta_hv']] for r in rows]
    s1_numeric = {0, 2, 3, 4, 5, 6}
    sheet1 = sheet_xml(s1_header, s1_rows, s1_numeric)

    # Sheet 2: region summary (user-defined weld geometry, computed from data)
    s2_header = ['Region', 'HV_uncharged', 'SD_uncharged', 'HV_charged',
                 'SD_charged', 'Delta_HV', 'Increase_pct']
    st = region_stats(rows)
    s2_rows = []
    for reg in REGION_ORDER:
        s = st[reg]
        if not s:
            continue
        s2_rows.append([REGION_NAME[reg], round(s['mu'], 1), round(s['sdu'], 1),
                        round(s['mc'], 1), round(s['sdc'], 1),
                        round(s['mc'] - s['mu'], 1),
                        round((s['mc'] / s['mu'] - 1) * 100, 1)])
    s2_numeric = {1, 2, 3, 4, 5, 6}
    sheet2 = sheet_xml(s2_header, s2_rows, s2_numeric)

    parts = {
        '[Content_Types].xml': CONTENT_TYPES,
        '_rels/.rels': ROOT_RELS,
        'xl/workbook.xml': WORKBOOK,
        'xl/_rels/workbook.xml.rels': WORKBOOK_RELS,
        'xl/styles.xml': STYLES,
        'xl/worksheets/sheet1.xml': sheet1,
        'xl/worksheets/sheet2.xml': sheet2,
        'xl/worksheets/_rels/sheet1.xml.rels': sheet_rels('../drawings/drawing1.xml'),
        'xl/worksheets/_rels/sheet2.xml.rels': sheet_rels('../drawings/drawing2.xml'),
        'xl/drawings/drawing1.xml': drawing_xml('Chart 1'),
        'xl/drawings/drawing2.xml': drawing_xml('Chart 2'),
        'xl/drawings/_rels/drawing1.xml.rels': drawing_rels('../charts/chart1.xml'),
        'xl/drawings/_rels/drawing2.xml.rels': drawing_rels('../charts/chart2.xml'),
        'xl/charts/chart1.xml': scatter_chart('Interpolated_0.1mm', len(s1_rows)),
        'xl/charts/chart2.xml': bar_chart('Region_Summary'),
    }

    with zipfile.ZipFile(XLSX, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)

    print(f"XLSX -> {XLSX}")
    print(f"  Sheet 'Interpolated_0.1mm': {len(s1_rows)} data rows + scatter/line chart")
    print(f"  Sheet 'Region_Summary'    : {len(s2_rows)} rows (Table 1) + column chart")


if __name__ == '__main__':
    main()
