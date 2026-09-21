#!/usr/bin/env python3
"""
Convert TCS_Misuse_Research_Article.md into a Word .docx using ONLY the
Python standard library (zipfile). Supports: #/##/### headings, paragraphs,
**bold**, *italic*, blockquotes, horizontal rules, and GitHub pipe tables.
"""
import zipfile, os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "TCS_Misuse_Research_Article.md")
OUT = os.path.join(HERE, "TCS_Misuse_Research_Article.docx")

def esc(t): return html.escape(t, quote=False)

def runs(text):
    """Convert inline **bold**/*italic* into w:r runs."""
    out = []
    # tokenize on ** and *
    pattern = re.compile(r'(\*\*.+?\*\*|\*.+?\*)')
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            out.append(("", text[pos:m.start()]))
        tok = m.group(0)
        if tok.startswith("**"):
            out.append(("b", tok[2:-2]))
        else:
            out.append(("i", tok[1:-1]))
        pos = m.end()
    if pos < len(text):
        out.append(("", text[pos:]))
    xml = ""
    for style, chunk in out:
        rpr = ""
        if style == "b": rpr = "<w:rPr><w:b/></w:rPr>"
        elif style == "i": rpr = "<w:rPr><w:i/></w:rPr>"
        xml += f'<w:r>{rpr}<w:t xml:space="preserve">{esc(chunk)}</w:t></w:r>'
    return xml or '<w:r><w:t/></w:r>'

def para(text, style=None, size=None, bold=False, align=None, color=None, spacing_before=120, spacing_after=120):
    ppr = "<w:pPr>"
    ppr += f'<w:spacing w:before="{spacing_before}" w:after="{spacing_after}"/>'
    if align: ppr += f'<w:jc w:val="{align}"/>'
    ppr += "</w:pPr>"
    r = runs(text)
    if bold or size or color:
        # wrap: rebuild runs with rPr additions is complex; use simple single run
        rpr = "<w:rPr>"
        if bold: rpr += "<w:b/>"
        if size: rpr += f'<w:sz w:val="{size*2}"/><w:szCs w:val="{size*2}"/>'
        if color: rpr += f'<w:color w:val="{color}"/>'
        rpr += "</w:rPr>"
        r = f'<w:r>{rpr}<w:t xml:space="preserve">{esc(re.sub(r"[*]", "", text))}</w:t></w:r>'
    return f"<w:p>{ppr}{r}</w:p>"

def heading(text, level):
    sizes = {1: 20, 2: 15, 3: 13}
    return para(text, bold=True, size=sizes.get(level, 12), color="1F3864" if level<=2 else "2E5496",
                spacing_before=240 if level==1 else 200, spacing_after=120)

def table(rows):
    # rows: list of list of cell strings; first row = header
    borders = ('<w:tblBorders>' + ''.join(
        f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        for e in ["top","left","bottom","right","insideH","insideV"]) + '</w:tblBorders>')
    tblpr = f'<w:tblPr><w:tblW w:w="5000" w:type="pct"/>{borders}<w:tblLook w:val="04A0"/></w:tblPr>'
    xml = f"<w:tbl>{tblpr}"
    for i, row in enumerate(rows):
        xml += "<w:tr>"
        for cell in row:
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if i == 0 else ""
            cpr = f'<w:tcPr>{shd}</w:tcPr>'
            r = runs(("**"+cell+"**") if i == 0 else cell)
            xml += f'<w:tc>{cpr}<w:p><w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>{r}</w:p></w:tc>'
        xml += "</w:tr>"
    xml += "</w:tbl>"
    # trailing empty paragraph so tables don't merge
    return xml + "<w:p/>"

def md_to_body(md):
    lines = md.split("\n")
    body = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1; continue
        # table detection
        if line.lstrip().startswith("|") and i+1 < len(lines) and re.match(r'^\s*\|?[\s:|-]+\|?\s*$', lines[i+1]):
            tbl = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                if re.match(r'^\s*\|?[\s:|-]+\|?\s*$', lines[i]):
                    i += 1; continue
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                tbl.append(cells)
                i += 1
            body.append(table(tbl))
            continue
        if line.startswith("### "):
            body.append(heading(line[4:], 3))
        elif line.startswith("## "):
            body.append(heading(line[3:], 2))
        elif line.startswith("# "):
            body.append(heading(line[2:], 1))
        elif line.strip() in ("---", "***", "___"):
            body.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="999999"/></w:pBdr></w:pPr></w:p>')
        elif line.startswith(">"):
            body.append(para(line.lstrip("> ").strip(), color="555555", spacing_before=80, spacing_after=80))
        elif re.match(r'^\s*[-*] ', line):
            body.append(para("\u2022 " + re.sub(r'^\s*[-*] ', '', line), spacing_before=40, spacing_after=40))
        elif re.match(r'^\s*\d+\. ', line):
            body.append(para(re.sub(r'^\s*(\d+)\. ', r'\1. ', line), spacing_before=40, spacing_after=40))
        else:
            body.append(para(line))
        i += 1
    return "".join(body)

def build():
    md = open(SRC, encoding="utf-8").read()
    body = md_to_body(md)
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:body>{body}'
        '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
        '</w:sectPr></w:body></w:document>')
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '</Types>')
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", document)
    print("Wrote", OUT, f"({os.path.getsize(OUT)} bytes)")

if __name__ == "__main__":
    build()
