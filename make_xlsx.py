#!/usr/bin/env python3
"""
Build hardness_profile.xlsx from hardness_profile_data.csv using only the
Python standard library (an .xlsx is a ZIP of XML parts). Two worksheets:
  1) "Hardness Data" : full 321-row traverse (-8..+8 mm, 0.05 mm step)
  2) "Summary"       : zone statistics + metadata + literature sources
"""
import csv, zipfile, datetime

CSV = "hardness_profile_data.csv"
OUT = "hardness_profile.xlsx"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def col_letter(n):           # 1 -> A
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def cell(ref, value, is_num, style=0):
    s = f' s="{style}"' if style else ""
    if is_num:
        return f'<c r="{ref}"{s}><v>{value}</v></c>'
    return f'<c r="{ref}"{s} t="inlineStr"><is><t xml:space="preserve">{esc(value)}</t></is></c>'


def sheet_xml(rows):
    """rows: list of list of (value, is_num, style)."""
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
           '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
           '<sheetData>']
    for ri, row in enumerate(rows, start=1):
        cells = "".join(cell(f"{col_letter(ci)}{ri}", v, num, st)
                        for ci, (v, num, st) in enumerate(row, start=1))
        out.append(f'<row r="{ri}">{cells}</row>')
    out.append('</sheetData></worksheet>')
    return "".join(out)


# ---- read data ----
rows = []
with open(CSV) as f:
    r = csv.reader(f)
    header = next(r)
    for row in r:
        rows.append(row)

# ---- Sheet 1: data (with SD = 5% of each HV value) ----
hdr = ["Position_mm", "E6018_HV", "E6018_SD", "E7018_HV", "E7018_SD",
       "E9018_HV", "E9018_SD", "Zone"]
data_rows = [[(h, False, 1) for h in hdr]]
for row in rows:
    x, e6, e7, e9, zone = row
    e6, e7, e9 = float(e6), float(e7), float(e9)
    data_rows.append([(float(x), True, 0),
                      (e6, True, 0), (round(0.02 * e6, 2), True, 0),
                      (e7, True, 0), (round(0.02 * e7, 2), True, 0),
                      (e9, True, 0), (round(0.02 * e9, 2), True, 0),
                      (zone, False, 0)])

# ---- zone statistics ----
def stats(col_idx, zone):
    vals = [float(row[col_idx]) for row in rows if row[4] == zone]
    return (round(sum(vals) / len(vals), 1), min(vals), max(vals)) if vals else (0, 0, 0)

# CGHAZ peak = max over HAZ
def peak(col_idx):
    return max(float(row[col_idx]) for row in rows if row[4] == "HAZ")

electrodes = [("E6018", 1), ("E7018", 2), ("E9018", 3)]

# ---- Sheet 2: summary ----
S = []
def srow(*cells):  # cells: list of (val, is_num, style)
    S.append(list(cells))

srow(("Microhardness Traverse — API X70 SMAW Weld Joints", False, 1))
srow(("Generated", False, 0), (datetime.date.today().isoformat(), False, 0))
srow(("Traverse", False, 0), ("-8 mm to +8 mm, step 0.05 mm (321 points/curve)", False, 0))
srow(("Fusion line", False, 0), ("|x| = 5 mm; HAZ 5-7 mm; Base metal |x| > 7 mm", False, 0))
srow(("Error bars", False, 0), ("SD = 2% of each HV value (see *_SD columns on Hardness Data)", False, 0))
srow()
srow(("Zone statistics (HV0.1): mean / min / max", False, 1))
srow(("Electrode", False, 1), ("Region", False, 1), ("Mean", False, 1),
     ("Min", False, 1), ("Max", False, 1))
for name, ci in electrodes:
    for zone, label in [("BM", "Base metal"), ("HAZ", "HAZ"), ("FZ", "Fusion zone")]:
        m, lo, hi = stats(ci, zone)
        srow((name, False, 0), (label, False, 0), (m, True, 0),
             (lo, True, 0), (hi, True, 0))
    srow((name, False, 0), ("CGHAZ peak", False, 0), (round(peak(ci), 1), True, 0),
         ("", False, 0), ("", False, 0))
srow()
srow(("Literature basis (ranges reported for API X70 welds)", False, 1))
srow(("X70 base metal", False, 0), ("~210-225 HV", False, 0))
srow(("CGHAZ peak", False, 0), ("up to ~234-253 HV at high cooling rate (bainitic)", False, 0))
srow(("Weld metal order", False, 0), ("E90 > E70 > E60 (rises with electrode strength)", False, 0))
srow()
srow(("Sources", False, 1))
srow(("SAW X70 hardness/tensile", False, 0),
     ("doi.org/10.1007/s00170-023-11070-4", False, 0))
srow(("X70 CGHAZ CCT & hardness", False, 0),
     ("doi.org/10.1007/s12046-021-01623-2", False, 0))
srow(("sDSS/X70 GTA HAZ sub-zones", False, 0),
     ("doi.org/10.1007/s10853-023-08723-w", False, 0))
srow(("SMAW E7018 vs E6013 weld hardness", False, 0),
     ("sapub.org 10.5923/j.materials.20190901.03", False, 0))
srow(("GMAW/FCAW X70 cap-pass hardness", False, 0),
     ("doi.org/10.1007/s00170-024-13859-3", False, 0))
srow()
srow(("Note", False, 1))
srow(("Values are a literature-grounded synthetic reconstruction of a realistic", False, 0),)
srow(("traverse (CGHAZ peak, overlapping BM/HAZ, FZ fan-out, multi-pass scatter),", False, 0),)
srow(("not raw measured indentations.", False, 0),)

# pad summary rows to uniform-ish (not required by Excel)
summary_rows = [r if r else [("", False, 0)] for r in S]

# ---- static parts ----
CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''

WORKBOOK = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets>
<sheet name="Hardness Data" sheetId="1" r:id="rId1"/>
<sheet name="Summary" sheetId="2" r:id="rId2"/>
</sheets>
</workbook>'''

WB_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>
<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs>
</styleSheet>'''

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", CONTENT_TYPES)
    z.writestr("_rels/.rels", RELS)
    z.writestr("xl/workbook.xml", WORKBOOK)
    z.writestr("xl/_rels/workbook.xml.rels", WB_RELS)
    z.writestr("xl/styles.xml", STYLES)
    z.writestr("xl/worksheets/sheet1.xml", sheet_xml(data_rows))
    z.writestr("xl/worksheets/sheet2.xml", sheet_xml(summary_rows))

print(f"wrote {OUT}: {len(data_rows)} data rows + summary sheet")
