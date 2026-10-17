#!/usr/bin/env python3
"""
Build a self-contained Excel workbook (.xlsx) for the API X70 SMAW weldment
microhardness traverse (with and without hydrogen charging).

Pure Python (zipfile + XML) -- no openpyxl / pandas required.

Output: hardness_profile.xlsx
  Sheet "Data" : x_mm, region, hardness_uncharged_HV, hardness_charged_HV
  Sheet "Chart": a line chart of the two hardness curves vs. distance.
"""

import csv
import os
import zipfile

CSV_IN = "hardness_profile_data.csv"
XLSX_OUT = "hardness_profile.xlsx"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
rows = []
with open(CSV_IN, newline="") as f:
    r = csv.reader(f)
    header = next(r)
    for line in r:
        rows.append(line)  # [x, region, unch, chg]

N = len(rows)
last = N + 1  # last worksheet row (1-based, incl. header)

# ---------------------------------------------------------------------------
# sheet1 (Data)
# ---------------------------------------------------------------------------
sb = []
sb.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
sb.append('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
sb.append(f'<dimension ref="A1:D{last}"/>')
sb.append('<sheetData>')
# header row (inline strings)
sb.append('<row r="1">'
          '<c r="A1" t="inlineStr"><is><t>x_mm</t></is></c>'
          '<c r="B1" t="inlineStr"><is><t>region</t></is></c>'
          '<c r="C1" t="inlineStr"><is><t>hardness_uncharged_HV</t></is></c>'
          '<c r="D1" t="inlineStr"><is><t>hardness_charged_HV</t></is></c>'
          '</row>')
for i, (x, region, unch, chg) in enumerate(rows):
    rr = i + 2
    sb.append(
        f'<row r="{rr}">'
        f'<c r="A{rr}"><v>{x}</v></c>'
        f'<c r="B{rr}" t="inlineStr"><is><t>{esc(region)}</t></is></c>'
        f'<c r="C{rr}"><v>{unch}</v></c>'
        f'<c r="D{rr}"><v>{chg}</v></c>'
        f'</row>')
sb.append('</sheetData>')
sb.append('</worksheet>')
sheet1 = "\n".join(sb)

# ---------------------------------------------------------------------------
# sheet2 (Chart host) + drawing + chart
# ---------------------------------------------------------------------------
sheet2 = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          '<dimension ref="A1"/><sheetData/>'
          '<drawing r:id="rId1"/></worksheet>')

drawing = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" '
           'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
           'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
           '<xdr:twoCellAnchor>'
           '<xdr:from><xdr:col>1</xdr:col><xdr:colOff>0</xdr:colOff>'
           '<xdr:row>1</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:from>'
           '<xdr:to><xdr:col>14</xdr:col><xdr:colOff>0</xdr:colOff>'
           '<xdr:row>34</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:to>'
           '<xdr:graphicFrame macro="">'
           '<xdr:nvGraphicFramePr>'
           '<xdr:cNvPr id="2" name="HardnessChart"/><xdr:cNvGraphicFramePr/>'
           '</xdr:nvGraphicFramePr>'
           '<xdr:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/></xdr:xfrm>'
           '<a:graphic><a:graphicData '
           'uri="http://schemas.openxmlformats.org/drawingml/2006/chart">'
           '<c:chart xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
           'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
           'r:id="rId1"/></a:graphicData></a:graphic>'
           '</xdr:graphicFrame><xdr:clientData/></xdr:twoCellAnchor></xdr:wsDr>')

cat_ref = f"Data!$A$2:$A${last}"
unch_ref = f"Data!$C$2:$C${last}"
chg_ref = f"Data!$D$2:$D${last}"

chart = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<c:chartSpace xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<c:chart>'
    '<c:title><c:tx><c:rich><a:bodyPr/><a:p><a:r>'
    '<a:t>API X70 SMAW weldment - microhardness traverse (with vs. without H charging)</a:t>'
    '</a:r></a:p></c:rich></c:tx><c:overlay val="0"/></c:title>'
    '<c:autoTitleDeleted val="0"/>'
    '<c:plotArea><c:layout/>'
    '<c:lineChart><c:grouping val="standard"/><c:varyColors val="0"/>'
    # series 1 - uncharged
    '<c:ser><c:idx val="0"/><c:order val="0"/>'
    '<c:tx><c:strRef><c:f>Data!$C$1</c:f>'
    '<c:strCache><c:ptCount val="1"/><c:pt idx="0"><c:v>Without charging</c:v></c:pt>'
    '</c:strCache></c:strRef></c:tx>'
    '<c:spPr><a:ln w="19050"><a:solidFill><a:srgbClr val="1F5FD0"/></a:solidFill></a:ln></c:spPr>'
    '<c:marker><c:symbol val="none"/></c:marker>'
    f'<c:cat><c:numRef><c:f>{cat_ref}</c:f></c:numRef></c:cat>'
    f'<c:val><c:numRef><c:f>{unch_ref}</c:f></c:numRef></c:val>'
    '<c:smooth val="0"/></c:ser>'
    # series 2 - charged
    '<c:ser><c:idx val="1"/><c:order val="1"/>'
    '<c:tx><c:strRef><c:f>Data!$D$1</c:f>'
    '<c:strCache><c:ptCount val="1"/><c:pt idx="0"><c:v>With H charging</c:v></c:pt>'
    '</c:strCache></c:strRef></c:tx>'
    '<c:spPr><a:ln w="19050"><a:solidFill><a:srgbClr val="D02020"/></a:solidFill></a:ln></c:spPr>'
    '<c:marker><c:symbol val="none"/></c:marker>'
    f'<c:cat><c:numRef><c:f>{cat_ref}</c:f></c:numRef></c:cat>'
    f'<c:val><c:numRef><c:f>{chg_ref}</c:f></c:numRef></c:val>'
    '<c:smooth val="0"/></c:ser>'
    '<c:marker val="1"/><c:axId val="111"/><c:axId val="222"/></c:lineChart>'
    # category (X) axis
    '<c:catAx><c:axId val="111"/><c:scaling><c:orientation val="minMax"/></c:scaling>'
    '<c:delete val="0"/><c:axPos val="b"/>'
    '<c:title><c:tx><c:rich><a:bodyPr/><a:p><a:r>'
    '<a:t>Distance from weld centreline (mm)</a:t></a:r></a:p></c:rich></c:tx>'
    '<c:overlay val="0"/></c:title>'
    '<c:tickLblPos val="low"/><c:crossAx val="222"/></c:catAx>'
    # value (Y) axis
    '<c:valAx><c:axId val="222"/><c:scaling><c:orientation val="minMax"/>'
    '<c:max val="295"/><c:min val="170"/></c:scaling>'
    '<c:delete val="0"/><c:axPos val="l"/>'
    '<c:majorGridlines/>'
    '<c:title><c:tx><c:rich><a:bodyPr rot="-5400000" vert="horz"/><a:p><a:r>'
    '<a:t>Vickers microhardness (HV0.5)</a:t></a:r></a:p></c:rich></c:tx>'
    '<c:overlay val="0"/></c:title>'
    '<c:tickLblPos val="nextTo"/><c:crossAx val="111"/></c:valAx>'
    '</c:plotArea>'
    '<c:legend><c:legendPos val="t"/><c:overlay val="0"/></c:legend>'
    '<c:plotVisOnly val="1"/></c:chart></c:chartSpace>')

# ---------------------------------------------------------------------------
# package scaffolding
# ---------------------------------------------------------------------------
content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/xl/workbook.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
    '<Override PartName="/xl/worksheets/sheet1.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
    '<Override PartName="/xl/worksheets/sheet2.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
    '<Override PartName="/xl/drawings/drawing1.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/>'
    '<Override PartName="/xl/charts/chart1.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.drawingml.chart+xml"/>'
    '</Types>')

root_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
    'Target="xl/workbook.xml"/></Relationships>')

workbook = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<sheets>'
    '<sheet name="Data" sheetId="1" r:id="rId1"/>'
    '<sheet name="Chart" sheetId="2" r:id="rId2"/>'
    '</sheets></workbook>')

workbook_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
    'Target="worksheets/sheet1.xml"/>'
    '<Relationship Id="rId2" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
    'Target="worksheets/sheet2.xml"/>'
    '</Relationships>')

sheet2_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing" '
    'Target="../drawings/drawing1.xml"/></Relationships>')

drawing_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart" '
    'Target="../charts/chart1.xml"/></Relationships>')

parts = {
    "[Content_Types].xml": content_types,
    "_rels/.rels": root_rels,
    "xl/workbook.xml": workbook,
    "xl/_rels/workbook.xml.rels": workbook_rels,
    "xl/worksheets/sheet1.xml": sheet1,
    "xl/worksheets/sheet2.xml": sheet2,
    "xl/worksheets/_rels/sheet2.xml.rels": sheet2_rels,
    "xl/drawings/drawing1.xml": drawing,
    "xl/drawings/_rels/drawing1.xml.rels": drawing_rels,
    "xl/charts/chart1.xml": chart,
}

if os.path.exists(XLSX_OUT):
    os.remove(XLSX_OUT)
with zipfile.ZipFile(XLSX_OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for name, data in parts.items():
        z.writestr(name, data)

print(f"Wrote {XLSX_OUT} with {N} data rows + embedded line chart.")
