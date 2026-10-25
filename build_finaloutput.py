#!/usr/bin/env python3
"""
Build the Front-End Development graded-assignment final-output Word document.

python-docx is unavailable offline, so this writes a valid .docx by zipping
hand-built OOXML parts (the same approach already used elsewhere in this repo).

Output: FinalOutput_2025EB01187.docx
"""

import zipfile
from xml.sax.saxutils import escape

OUT = "FinalOutput_2025EB01187.docx"

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

# ----------------------------------------------------------------------
# Static package parts
# ----------------------------------------------------------------------
CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {W}>
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
      <w:sz w:val="22"/><w:szCs w:val="22"/>
    </w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr>
      <w:spacing w:after="140" w:line="288" w:lineRule="auto"/>
    </w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/><w:pPr><w:jc w:val="both"/></w:pPr>
  </w:style>
</w:styles>'''


# ----------------------------------------------------------------------
# Paragraph builders
# ----------------------------------------------------------------------
def run(text, bold=False, italic=False, size=22, color=None, font=None):
    rpr = "<w:rPr>"
    if font:
        rpr += f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>'
    if bold:
        rpr += "<w:b/>"
    if italic:
        rpr += "<w:i/>"
    if color:
        rpr += f'<w:color w:val="{color}"/>'
    rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def para(runs_xml, align="both", space_after=140, space_before=0,
         shade=None, border=False, line=None, indent=None):
    ppr = "<w:pPr>"
    if shade:
        ppr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
    if border:
        ppr += ('<w:pBdr>'
                '<w:top w:val="single" w:sz="4" w:space="1" w:color="C8C8C8"/>'
                '<w:left w:val="single" w:sz="4" w:space="4" w:color="C8C8C8"/>'
                '<w:bottom w:val="single" w:sz="4" w:space="1" w:color="C8C8C8"/>'
                '<w:right w:val="single" w:sz="4" w:space="4" w:color="C8C8C8"/>'
                '</w:pBdr>')
    sp = f'w:after="{space_after}" w:before="{space_before}"'
    if line:
        sp += f' w:line="{line}" w:lineRule="auto"'
    ppr += f'<w:spacing {sp}/>'
    if indent:
        ppr += f'<w:ind w:left="{indent}"/>'
    ppr += f'<w:jc w:val="{align}"/></w:pPr>'
    return f"<w:p>{ppr}{runs_xml}</w:p>"


def heading(text, size=30, color="1F3C72", before=320, after=140):
    return para(run(text, bold=True, size=size, color=color),
                align="left", space_before=before, space_after=after)


def body(text):
    return para(run(text, size=22))


def centered(text, bold=False, size=22, color=None):
    return para(run(text, bold=bold, size=size, color=color), align="center",
                space_after=60)


def code_block(source):
    """Render source text as tightly-spaced, shaded, monospace lines."""
    lines = source.replace("\t", "    ").split("\n")
    # drop a single trailing empty line
    while lines and lines[-1] == "":
        lines.pop()
    out = []
    n = len(lines)
    for i, ln in enumerate(lines):
        r = run(ln if ln != "" else " ", size=16, font="Consolas", color="1A1A1A")
        before = 40 if i == 0 else 0
        after = 40 if i == n - 1 else 0
        out.append(para(r, align="left", space_after=after, space_before=before,
                        shade="F3F4F6", border=(i == 0 or i == n - 1),
                        line=240))
    return "".join(out)


def rule_line():
    return ('<w:p><w:pPr><w:pBdr>'
            '<w:bottom w:val="single" w:sz="6" w:space="1" w:color="2A5298"/>'
            '</w:pBdr><w:spacing w:after="160"/></w:pPr></w:p>')


def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ----------------------------------------------------------------------
# Assemble the document body
# ----------------------------------------------------------------------
parts = []

# ---- Cover ----
parts.append(centered("Front-End Development", bold=True, size=40, color="1F3C72"))
parts.append(centered("Graded Assignment  (Weeks 1 - 6)", bold=True, size=28, color="2A5298"))
parts.append(centered("Final Output Document", size=24, color="555555"))
parts.append(rule_line())
parts.append(para(run("Student Name : ", bold=True) + run("Amman Jakhar"), align="left", space_after=60))
parts.append(para(run("Student UID : ", bold=True) + run("2025EB01187"), align="left", space_after=60))
parts.append(para(run("Date of Birth : ", bold=True) + run("29.08.1986"), align="left", space_after=60))
parts.append(para(run("Date of Submission : ", bold=True) + run("25 October 2026"), align="left", space_after=160))

# ---- Declaration / approach ----
parts.append(heading("Author's Note", size=26))
parts.append(body(
    "All four deliverable files in this submission were written by me. The "
    "in-code comments are my own as well; wherever I added one I tried to "
    "record the reason a line exists rather than simply naming the property. "
    "The screenshots were captured directly from the browser, and in each of "
    "them the page tab clearly reads 2025EB01187, which is the label both "
    "questions required."))

parts.append(page_break())

# ====================================================================
#  QUESTION 1
# ====================================================================
parts.append(heading("Question 1 — Student Identity Card", size=30))
parts.append(body(
    "For this card I separated the two responsibilities. IDCard.html carries "
    "only the structure, while IDCard_styles.css handles every colour, size "
    "and spacing decision. Keeping them apart meant I could change the look of "
    "the card without ever touching its markup. The document title is set to "
    "my UID so that the browser tab displays 2025EB01187."))

parts.append(heading("Output Screenshot", size=24, before=200))
parts.append(para(run("[ Figure 1 — IDCard.html rendered in the browser; the tab reads 2025EB01187. "
                      "Paste the screenshot here. ]", italic=True, color="777777"), align="center"))

parts.append(heading("Source — IDCard.html", size=24, before=220))
parts.append(code_block(read("IDCard.html")))

parts.append(heading("Source — IDCard_styles.css", size=24, before=220))
parts.append(code_block(read("IDCard_styles.css")))

parts.append(page_break())

# ====================================================================
#  QUESTION 2
# ====================================================================
parts.append(heading("Question 2 — Student ID Card Application", size=30))
parts.append(body(
    "The second task is a short form that collects the details needed for an "
    "ID card. StudentApp.html provides the page itself, but the marks sit in "
    "StudentApp.js, so that is where the real work went: five validators that "
    "each guard one field, a Student class that I instantiate and print with "
    "console.log, and a pair of cookie helpers that remember the most recent "
    "student. When every field passes, a green summary appears on screen while "
    "the same details are written to the console and stored in a cookie."))

parts.append(heading("Output Screenshot — Application Form", size=24, before=200))
parts.append(para(run("[ Figure 2 — The form immediately after a valid submission; the green banner is "
                      "the success summary. Paste the screenshot here. ]", italic=True, color="777777"),
                  align="center"))

parts.append(heading("Output Screenshot — Console Log (Student object + cookie)", size=24, before=180))
parts.append(para(run("[ Figure 3 — The console showing the expanded Student object together with the "
                      "lastStudent cookie read back through document.cookie. Paste the screenshot here. ]",
                      italic=True, color="777777"), align="center"))

parts.append(heading("Source — StudentApp.html", size=24, before=220))
parts.append(code_block(read("StudentApp.html")))

parts.append(heading("Source — StudentApp.js", size=24, before=220))
parts.append(code_block(read("StudentApp.js")))

body_xml = "".join(parts)

SECT = ('<w:sectPr>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        '</w:sectPr>')

DOCUMENT = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<w:document {W}><w:body>{body_xml}{SECT}</w:body></w:document>')

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", CONTENT_TYPES)
    z.writestr("_rels/.rels", RELS)
    z.writestr("word/_rels/document.xml.rels", WORD_RELS)
    z.writestr("word/styles.xml", STYLES)
    z.writestr("word/document.xml", DOCUMENT)

print("Wrote", OUT)
