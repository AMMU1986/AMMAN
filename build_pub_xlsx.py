#!/usr/bin/env python3
"""
Parse pubs_raw.txt (a Google-Scholar style publication dump) into a structured
Excel workbook (.xlsx) with a DOI column + a one-click Crossref DOI-lookup link.

Pure standard library: writes the .xlsx (a zip of XML parts) directly.
"""

import re
import zipfile
import html
from urllib.parse import quote

RAW = '/projects/sandbox/AMMAN/pubs_raw.txt'
OUT = '/projects/sandbox/AMMAN/Mukhopadhyay_Publications.xlsx'

# ---- verified DOIs (filled from literature search; keyed by lowercase title prefix) ----
VERIFIED = {}


def key(title):
    return re.sub(r'[^a-z0-9]', '', title.lower())[:45]


def add_doi(title, doi):
    VERIFIED[key(title)] = doi


# ------------------------------- parse ----------------------------------------
TERM = re.compile(r'^\s*(?:(\d+)\*?\s*\t?\s*)?((?:19|20)\d{2})\s*$')

lines = [l.rstrip() for l in open(RAW, encoding='utf-8').read().split('\n')]
lines = [l for l in lines if l.strip()]

records = []
block = []
for ln in lines:
    m = TERM.match(ln)
    if m and block:                       # terminator -> close record
        cites = m.group(1) or ''
        year = m.group(2)
        title = block[0]
        authors = block[1] if len(block) > 1 else ''
        source = ' '.join(block[2:]) if len(block) > 2 else ''
        records.append({'title': title, 'authors': authors, 'source': source,
                        'cites': cites, 'year': year})
        block = []
    else:
        block.append(ln)

print(f'parsed {len(records)} publications')

# ------------------------------- xlsx helpers ---------------------------------
HEADERS = ['No', 'Year', 'Citations', 'Title', 'Authors',
           'Source (journal, vol, issue, pages)', 'DOI', 'DOI URL',
           'Crossref DOI lookup']


def col(n):
    s = ''
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def esc(t):
    return html.escape(str(t), quote=True)


def cell(cref, val, style=None, numeric=False):
    s = f' s="{style}"' if style is not None else ''
    if numeric and val != '':
        return f'<c r="{cref}"{s}><v>{val}</v></c>'
    if val == '':
        return f'<c r="{cref}"{s}/>'
    return f'<c r="{cref}" t="inlineStr"{s}><is><t xml:space="preserve">{esc(val)}</t></is></c>'


def build_sheet():
    rows = []
    # header row
    hc = ''.join(cell(f'{col(i)}1', h, style=1) for i, h in enumerate(HEADERS))
    rows.append(f'<row r="1">{hc}</row>')
    for idx, rec in enumerate(records, start=1):
        r = idx + 1
        doi = VERIFIED.get(key(rec['title']), '')
        doi_url = f'https://doi.org/{doi}' if doi else ''
        lookup = 'https://search.crossref.org/?q=' + quote(rec['title']) + '&from_ui=yes'
        cells = [
            cell(f'A{r}', idx, numeric=True),
            cell(f'B{r}', rec['year'], numeric=True),
            cell(f'C{r}', rec['cites'], numeric=bool(rec['cites'])),
            cell(f'D{r}', rec['title'], style=2),
            cell(f'E{r}', rec['authors'], style=2),
            cell(f'F{r}', rec['source'], style=2),
            cell(f'G{r}', doi, style=2),
            cell(f'H{r}', doi_url, style=2),
            cell(f'I{r}', lookup, style=2),
        ]
        rows.append(f'<row r="{r}">{"".join(cells)}</row>')
    dim = f'A1:{col(len(HEADERS) - 1)}{len(records) + 1}'
    cols = (
        '<cols>'
        '<col min="1" max="1" width="5"/>'
        '<col min="2" max="3" width="9"/>'
        '<col min="4" max="4" width="60"/>'
        '<col min="5" max="5" width="26"/>'
        '<col min="6" max="6" width="40"/>'
        '<col min="7" max="7" width="24"/>'
        '<col min="8" max="9" width="40"/>'
        '</cols>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="{dim}"/>'
        '<sheetViews><sheetView workbookViewId="0">'
        '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
        '</sheetView></sheetViews>'
        '<sheetFormatPr defaultRowHeight="15"/>'
        f'{cols}<sheetData>{"".join(rows)}</sheetData></worksheet>')


STYLES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
    '<fonts count="2">'
    '<font><sz val="11"/><name val="Calibri"/></font>'
    '<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>'
    '</fonts>'
    '<fills count="3">'
    '<fill><patternFill patternType="none"/></fill>'
    '<fill><patternFill patternType="gray125"/></fill>'
    '<fill><patternFill patternType="solid"><fgColor rgb="FF2E5496"/><bgColor indexed="64"/></patternFill></fill>'
    '</fills>'
    '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
    '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
    '<cellXfs count="3">'
    '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
    '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1">'
    '<alignment horizontal="center" vertical="center" wrapText="1"/></xf>'
    '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1">'
    '<alignment vertical="top" wrapText="1"/></xf>'
    '</cellXfs>'
    '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
    '</styleSheet>')

CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
    '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
    '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
    '</Types>')

RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
    '</Relationships>')

WORKBOOK = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<sheets><sheet name="Publications" sheetId="1" r:id="rId1"/></sheets></workbook>')

WB_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '</Relationships>')


def save():
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS)
        z.writestr('xl/workbook.xml', WORKBOOK)
        z.writestr('xl/_rels/workbook.xml.rels', WB_RELS)
        z.writestr('xl/styles.xml', STYLES)
        z.writestr('xl/worksheets/sheet1.xml', build_sheet())
    print('written', OUT, '| DOIs filled:', len(VERIFIED))


# also a CSV mirror
def save_csv():
    import csv
    with open('/projects/sandbox/AMMAN/Mukhopadhyay_Publications.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        for idx, rec in enumerate(records, 1):
            doi = VERIFIED.get(key(rec['title']), '')
            w.writerow([idx, rec['year'], rec['cites'], rec['title'], rec['authors'],
                        rec['source'], doi, f'https://doi.org/{doi}' if doi else '',
                        'https://search.crossref.org/?q=' + quote(rec['title']) + '&from_ui=yes'])


# ---- verified DOIs (confirmed via literature search; exact-title matches) ----
add_doi('Thermoelastic damping analysis in microbeam resonators based on Moore–Gibson–Thompson generalized thermoelasticity theory', '10.1007/s00707-020-02688-6')
add_doi('A domain of influence theorem under MGT thermoelasticity theory', '10.1177/1081286520946820')
add_doi('Galerkin-type solution for the Moore–Gibson–Thompson thermoelasticity theory', '10.1007/s00707-020-02915-0')
add_doi('A domain of influence theorem for a natural stress–heat-flux problem in the Moore–Gibson–Thompson thermoelasticity theory', '10.1007/s00707-020-02833-1')
add_doi('Study of wave propagation in an infinite solid due to a line heat source under Moore–Gibson–Thompson thermoelasticity', '10.1007/s00707-021-03073-7')
add_doi('On fundamental solution of Moore–Gibson–Thompson (MGT) thermoelasticity theory', '10.1007/s00033-023-01996-w')
add_doi('Galerkin-type solution for the theory of strain and temperature rate-dependent thermoelasticity', '10.1007/s00707-019-02482-z')
add_doi('Thermoelastic wave propagation and reflection in biological tissue under nonlocal elasticity and Moore–Gibson–Thompson heat conduction: modeling and analysis', '10.1007/s00033-024-02414-5')
add_doi('Thermoelastic damping analysis for a piezothermoelastic nanobeam resonator using DPL model under modified couple stress theory', '10.1007/s00033-024-02275-y')
add_doi('Vibration analysis of a transversely isotropic piezothermoelastic beam resonators under nonlocal strain gradient theory with DPL model', '10.1007/s00707-024-04198-1')
add_doi('On the representation of solutions for the theory of generalized thermoelasticity with three phase-lags', '10.1007/s00707-010-0291-z')
add_doi("Size-dependent thermoelastic damping analysis in nanobeam resonators based on Eringen's nonlocal elasticity and modified couple stress theories", '10.1177/10775463211064689')

if __name__ == '__main__':
    save()
    save_csv()
