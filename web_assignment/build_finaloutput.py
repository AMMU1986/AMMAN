#!/usr/bin/env python3
"""
Build finaloutput.doc (a valid .docx Word document) from scratch using only
the Python standard library (zipfile + xml). The document contains:
  - Student details
  - Direct downloadable links (GitHub raw URLs) for each source file
  - The full source code of all four deliverables
  - Labeled placeholders where the output screenshots should be pasted
"""

import os
import zipfile
from xml.sax.saxutils import escape

BRANCH = "web-assignment-idcard"
RAW_BASE = "https://raw.githubusercontent.com/AMMU1986/AMMAN/{}/web_assignment".format(BRANCH)
BLOB_BASE = "https://github.com/AMMU1986/AMMAN/blob/{}/web_assignment".format(BRANCH)

HERE = os.path.dirname(os.path.abspath(__file__))

FILES = ["IDCard.html", "IDCard_styles.css", "StudentApp.html", "StudentApp.js"]

# Collected hyperlink relationships: list of (rId, url)
rels = []
_rid_counter = [0]


def new_rid(url):
    _rid_counter[0] += 1
    rid = "rId{}".format(100 + _rid_counter[0])
    rels.append((rid, url))
    return rid


# ---- paragraph builders (produce word/document.xml body fragments) ----

def para(text, bold=False, size=22, color="000000", spacing_after=120):
    """A normal paragraph of text. size is in half-points (22 = 11pt)."""
    b = '<w:b/>' if bold else ''
    return (
        '<w:p><w:pPr><w:spacing w:after="{sp}"/></w:pPr>'
        '<w:r><w:rPr>{b}<w:color w:val="{c}"/><w:sz w:val="{s}"/></w:rPr>'
        '<w:t xml:space="preserve">{t}</w:t></w:r></w:p>'
    ).format(sp=spacing_after, b=b, c=color, s=size, t=escape(text))


def heading(text, size=32, color="1E3C72"):
    return (
        '<w:p><w:pPr><w:spacing w:before="200" w:after="120"/></w:pPr>'
        '<w:r><w:rPr><w:b/><w:color w:val="{c}"/><w:sz w:val="{s}"/></w:rPr>'
        '<w:t xml:space="preserve">{t}</w:t></w:r></w:p>'
    ).format(c=color, s=size, t=escape(text))


def link_para(label, url):
    """A paragraph with a bold label followed by a clickable hyperlink."""
    rid = new_rid(url)
    return (
        '<w:p><w:pPr><w:spacing w:after="80"/></w:pPr>'
        '<w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr>'
        '<w:t xml:space="preserve">{label}  </w:t></w:r>'
        '<w:hyperlink r:id="{rid}" w:history="1">'
        '<w:r><w:rPr><w:color w:val="0563C1"/><w:u w:val="single"/><w:sz w:val="20"/></w:rPr>'
        '<w:t xml:space="preserve">{url}</w:t></w:r></w:hyperlink></w:p>'
    ).format(label=escape(label), rid=rid, url=escape(url))


def code_block(code):
    """Render source code as monospaced, line-by-line paragraphs on a light bg."""
    out = []
    for line in code.split("\n"):
        line = line.replace("\t", "    ")
        tmpl = (
            '<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>'
            '<w:shd w:val="clear" w:fill="F4F4F4"/></w:pPr>'
            '<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
            '<w:sz w:val="16"/></w:rPr>'
            '<w:t xml:space="preserve">{t}</w:t></w:r></w:p>'
        )
        out.append(tmpl.format(t=escape(line) if line else " "))
    return "".join(out)


def screenshot_placeholder(text):
    """A bordered empty box telling the student where to paste a screenshot."""
    return (
        '<w:p><w:pPr><w:spacing w:before="120" w:after="120"/>'
        '<w:pBdr>'
        '<w:top w:val="dashed" w:sz="12" w:space="6" w:color="999999"/>'
        '<w:left w:val="dashed" w:sz="12" w:space="6" w:color="999999"/>'
        '<w:bottom w:val="dashed" w:sz="12" w:space="6" w:color="999999"/>'
        '<w:right w:val="dashed" w:sz="12" w:space="6" w:color="999999"/>'
        '</w:pBdr><w:jc w:val="center"/></w:pPr>'
        '<w:r><w:rPr><w:i/><w:color w:val="888888"/><w:sz w:val="22"/></w:rPr>'
        '<w:t xml:space="preserve">{t}</w:t></w:r></w:p>'
        # a couple of blank lines to give the box some height
        '<w:p><w:pPr><w:pBdr>'
        '<w:left w:val="dashed" w:sz="12" w:space="6" w:color="999999"/>'
        '<w:right w:val="dashed" w:sz="12" w:space="6" w:color="999999"/>'
        '<w:bottom w:val="dashed" w:sz="12" w:space="6" w:color="999999"/>'
        '</w:pBdr></w:pPr><w:r><w:rPr><w:sz w:val="22"/></w:rPr>'
        '<w:t xml:space="preserve"> </w:t></w:r></w:p>'
    ).format(t=escape(text))


# ---- assemble the document body ----

body = []
body.append(heading("Front-End Development  -  Graded Assignment (Weeks 1-6)", size=36))
body.append(para("Final Output Document (finaloutput.doc)", bold=True, size=26, color="555555"))
body.append(para("Student Name : AMMAN JAKHAR", bold=True))
body.append(para("Student UID  : 2025EB01187", bold=True))
body.append(para("Date of Birth: 29.08.1986", bold=True))

body.append(heading("Direct Download Links (source code)", size=28))
body.append(para("Click any link below to download the raw source file directly:", size=20, color="555555"))
for f in FILES:
    body.append(link_para("Download " + f + ":", RAW_BASE + "/" + f))
body.append(para("Browse all files on GitHub:", bold=True))
body.append(link_para("Repository folder:", BLOB_BASE))
body.append(link_para("Pull request:", "https://github.com/AMMU1986/AMMAN/pull/216"))

# ---------- QUESTION 1 ----------
body.append(heading("Question 1 - Student ID Card", size=30))
body.append(para("Output screenshot (paste the browser view of IDCard.html below - "
                 "ensure the 2025EB01187 title tab is visible):", bold=True))
body.append(screenshot_placeholder("[ Paste Question 1 output screenshot here ]"))

for f in ["IDCard.html", "IDCard_styles.css"]:
    body.append(heading("Source: " + f, size=24, color="2A5298"))
    with open(os.path.join(HERE, f), "r", encoding="utf-8") as fh:
        body.append(code_block(fh.read()))

# ---------- QUESTION 2 ----------
body.append(heading("Question 2 - Student ID Card Application", size=30))
body.append(para("Output screenshot (paste the form view AND the browser console "
                 "showing the logged Student object / cookie below):", bold=True))
body.append(screenshot_placeholder("[ Paste Question 2 form output screenshot here ]"))
body.append(screenshot_placeholder("[ Paste Question 2 console log (Student object + cookie) screenshot here ]"))

for f in ["StudentApp.html", "StudentApp.js"]:
    body.append(heading("Source: " + f, size=24, color="2A5298"))
    with open(os.path.join(HERE, f), "r", encoding="utf-8") as fh:
        body.append(code_block(fh.read()))

body_xml = "".join(body)

# ---- full document.xml ----
document_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document '
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<w:body>'
    + body_xml +
    '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
    '</w:sectPr>'
    '</w:body></w:document>'
)

# ---- document relationships (hyperlinks) ----
rel_entries = "".join(
    '<Relationship Id="{rid}" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
    'Target="{url}" TargetMode="External"/>'.format(rid=rid, url=escape(url))
    for rid, url in rels
)
document_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    + rel_entries +
    '</Relationships>'
)

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '</Types>'
)

root_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
    'Target="word/document.xml"/>'
    '</Relationships>'
)

out_path = os.path.join(HERE, "finaloutput.doc")
with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", root_rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/_rels/document.xml.rels", document_rels)

print("Wrote", out_path)
print("Hyperlinks embedded:", len(rels))
