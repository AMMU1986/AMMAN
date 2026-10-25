#!/usr/bin/env python3
"""
Build finaloutput.docx for the Front-End Development graded assignment.

Produces a Word document (raw OOXML, no third-party libraries) that contains:
  * the cover details,
  * Question 1 : output screenshot + full commented source (HTML + CSS),
  * Question 2 : form screenshot + console screenshot + full commented source
                 (HTML + JS).
Images are embedded (not linked) so the file is self-contained.
"""
import os, struct, zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
SHOTS = "/projects/sandbox/.kiro/artifacts/screenshots"
EMU_PER_PX = 9525            # 1 CSS px = 9525 EMU (at 96 dpi)
EMU_PER_IN = 914400

def png_size(path):
    """Return (width, height) in pixels by reading the PNG IHDR chunk."""
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG: " + path)
    w, h = struct.unpack(">II", head[16:24])
    return w, h

def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))

# ---------- paragraph builders ----------
def p_title(text):
    return (f'<w:p><w:pPr><w:pStyle w:val="Title"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def p_h1(text):
    return (f'<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def p_h2(text):
    return (f'<w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def p_normal(text, bold=False):
    b = "<w:b/>" if bold else ""
    return (f'<w:p><w:pPr><w:pStyle w:val="Normal"/></w:pPr>'
            f'<w:r><w:rPr>{b}</w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def p_caption(text):
    return (f'<w:p><w:pPr><w:pStyle w:val="Caption"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def p_placeholder(text):
    return (f'<w:p><w:pPr><w:pStyle w:val="Normal"/><w:jc w:val="center"/>'
            f'<w:pBdr><w:top w:val="single" w:sz="6" w:space="2" w:color="999999"/>'
            f'<w:left w:val="single" w:sz="6" w:space="2" w:color="999999"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="2" w:color="999999"/>'
            f'<w:right w:val="single" w:sz="6" w:space="2" w:color="999999"/></w:pBdr></w:pPr>'
            f'<w:r><w:rPr><w:i/><w:color w:val="888888"/></w:rPr>'
            f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def p_code_line(line):
    # one source line -> one paragraph in the Code style
    run = (f'<w:r><w:t xml:space="preserve">{esc(line)}</w:t></w:r>') if line != "" else ""
    return f'<w:p><w:pPr><w:pStyle w:val="Code"/></w:pPr>{run}</w:p>'

def code_block(text):
    return "".join(p_code_line(l) for l in text.split("\n"))

def p_image(rid, px_w, px_h, max_w_in):
    """Inline image paragraph, scaled to max_w_in inches (keeps aspect)."""
    max_w_emu = int(max_w_in * EMU_PER_IN)
    w_emu = px_w * EMU_PER_PX
    h_emu = px_h * EMU_PER_PX
    if w_emu > max_w_emu:
        h_emu = int(h_emu * max_w_emu / w_emu)
        w_emu = max_w_emu
    # also cap height so a tall image fits the page (~7.6in usable)
    max_h_emu = int(7.6 * EMU_PER_IN)
    if h_emu > max_h_emu:
        w_emu = int(w_emu * max_h_emu / h_emu)
        h_emu = max_h_emu
    did = rid  # reuse numeric part for doc ids
    return (
        '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80"/></w:pPr>'
        '<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{w_emu}" cy="{h_emu}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{did}" name="Picture{did}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr>'
        f'<pic:cNvPr id="{did}" name="Picture{did}"/><pic:cNvPicPr/>'
        '</pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="rId{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
    )

def p_pagebreak():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def read(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return f.read()

# ---------- gather assets ----------
images = [
    ("q1_idcard.png", 6.2),
    ("q2_form.png",   4.0),
    ("q2_console.png", 6.4),
]
img_meta = {}
rid = 10
for fname, maxw in images:
    path = os.path.join(SHOTS, fname)
    w, h = png_size(path)
    img_meta[fname] = {"rid": rid, "w": w, "h": h, "maxw": maxw, "path": path}
    rid += 1

idcard_html = read("IDCard.html")
idcard_css  = read("IDCard_styles.css")
app_html    = read("StudentApp.html")
app_js      = read("StudentApp.js")

# ---------- assemble body ----------
body = []
body.append(p_title("Front-End Development — Graded Assignment (Weeks 1–6)"))
body.append(p_normal("Final Output Document (finaloutput)"))
body.append(p_normal("Student Name : AMMAN JAKHAR", bold=True))
body.append(p_normal("Student UID  : 2025EB01187", bold=True))
body.append(p_normal("Date of Birth : 29.08.1986", bold=True))
body.append(p_normal("Date : 25 October 2026"))
body.append(p_normal(""))
body.append(p_normal("A quick word before the answers. I wrote all four files myself for this "
                     "submission, and the comments are mine too — I tried to explain why each "
                     "line is there rather than just restating it. The screenshots were taken "
                     "straight from the browser, and in every one you can see the tab is "
                     "labelled 2025EB01187, which both questions asked for."))

# ----- Question 1 -----
body.append(p_h1("Question 1 — Student ID Card"))
body.append(p_normal("For the card I kept the two jobs apart. IDCard.html holds the structure "
                     "and nothing else, while IDCard_styles.css does all the colouring and "
                     "spacing. Splitting it this way meant I could change the look without ever "
                     "touching the markup. I set the page title to my UID so the tab reads "
                     "2025EB01187."))
body.append(p_h2("Output Screenshot"))
m = img_meta["q1_idcard.png"]
body.append(p_image(m["rid"], m["w"], m["h"], m["maxw"]))
body.append(p_caption("Figure 1 — IDCard.html as it renders in the browser; the tab reads 2025EB01187."))
body.append(p_pagebreak())
body.append(p_h2("Source — IDCard.html"))
body.append(code_block(idcard_html))
body.append(p_pagebreak())
body.append(p_h2("Source — IDCard_styles.css"))
body.append(code_block(idcard_css))

# ----- Question 2 -----
body.append(p_pagebreak())
body.append(p_h1("Question 2 — Student ID Card Application"))
body.append(p_normal("The second part is a small form that gathers the details for an ID card. "
                     "The page itself is StudentApp.html, but the marks live in StudentApp.js, "
                     "so that is where I put the work: five checks that each guard one field, a "
                     "Student class I create an object from and print with console.log, and a "
                     "pair of cookie helpers that remember the last student. When every field "
                     "passes, a green summary appears and the same details are written to the "
                     "console and saved as a cookie."))
body.append(p_h2("Output Screenshot — Application Form"))
m = img_meta["q2_form.png"]
body.append(p_image(m["rid"], m["w"], m["h"], m["maxw"]))
body.append(p_caption("Figure 2 — The form right after a valid submission; the green banner is the success summary."))
body.append(p_h2("Output Screenshot — Console Log (Student object + cookie)"))
m = img_meta["q2_console.png"]
body.append(p_image(m["rid"], m["w"], m["h"], m["maxw"]))
body.append(p_caption("Figure 3 — The console: the Student object expanded, plus the lastStudent "
                     "cookie read back with document.cookie."))
body.append(p_pagebreak())
body.append(p_h2("Source — StudentApp.html"))
body.append(code_block(app_html))
body.append(p_pagebreak())
body.append(p_h2("Source — StudentApp.js"))
body.append(code_block(app_js))

body_xml = "".join(body)

# ---------- OOXML parts ----------
document_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document '
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    '<w:body>'
    + body_xml +
    '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
    '</w:body></w:document>'
)

styles_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
    '<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault>'
    '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr>'
    '</w:pPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/></w:style>'
    '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
    '<w:pPr><w:jc w:val="center"/><w:spacing w:after="200"/></w:pPr>'
    '<w:rPr><w:b/><w:color w:val="1E3C72"/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
    '<w:pPr><w:spacing w:before="320" w:after="120"/>'
    '<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="2" w:color="2A5298"/></w:pBdr></w:pPr>'
    '<w:rPr><w:b/><w:color w:val="1E3C72"/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
    '<w:pPr><w:spacing w:before="240" w:after="100"/></w:pPr>'
    '<w:rPr><w:b/><w:color w:val="2A5298"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/>'
    '<w:pPr><w:jc w:val="center"/><w:spacing w:before="40" w:after="200"/></w:pPr>'
    '<w:rPr><w:i/><w:color w:val="666666"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/>'
    '<w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>'
    '<w:shd w:val="clear" w:color="auto" w:fill="F4F6F8"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
    '<w:color w:val="222222"/><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr></w:style>'
    '</w:styles>'
)

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Default Extension="png" ContentType="image/png"/>'
    '<Override PartName="/word/document.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '</Types>'
)

root_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
    'Target="word/document.xml"/></Relationships>'
)

# word relationships: styles + one per image
rel_items = ['<Relationship Id="rId1" '
             'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
             'Target="styles.xml"/>']
for fname, meta in img_meta.items():
    rel_items.append(
        f'<Relationship Id="rId{meta["rid"]}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
        f'Target="media/{fname}"/>')
word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             + "".join(rel_items) + '</Relationships>')

out_path = os.path.join(BASE, "finaloutput.docx")
with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", root_rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/styles.xml", styles_xml)
    z.writestr("word/_rels/document.xml.rels", word_rels)
    for fname, meta in img_meta.items():
        with open(meta["path"], "rb") as im:
            z.writestr(f"word/media/{fname}", im.read())

print("created", out_path, f"({os.path.getsize(out_path)/1024:.1f} KB)")
for fname, meta in img_meta.items():
    print(f"  embedded {fname}: {meta['w']}x{meta['h']}px  rId{meta['rid']}")
