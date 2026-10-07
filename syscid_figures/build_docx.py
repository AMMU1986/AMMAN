#!/usr/bin/env python3
"""
Pure-standard-library Markdown -> DOCX converter tailored to
SYSCID_Map_Review_Article.md.

A .docx is an OPC (Open Packaging Conventions) ZIP of XML parts.  We generate a
genuine Word document (not HTML masquerading as .doc) with:
  * Title / Heading 1 / Heading 2 styles
  * Justified body paragraphs with bold/italic inline runs
  * Native Word tables with header shading and thin borders
  * Embedded PNG figures (scaled to page width) with italic captions
  * Blockquote (note) styling

No third-party packages are required.
"""
import os
import re
import struct
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MD = os.path.join(ROOT, "SYSCID_Map_Review_Article.md")
OUT = os.path.join(ROOT, "SYSCID_Map_Review_Article.docx")

EMU_PER_PX = 9525          # 1 px (96 dpi) = 9525 EMU
PAGE_WIDTH_PX = 620        # usable content width target for figures


def xml_escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


# ---------------------------------------------------------------------------
# Inline formatting: **bold**, *italic*, `code` -> runs
# ---------------------------------------------------------------------------
def inline_runs(text, base_italic=False, base_bold=False, color=None):
    # tokenise on ** , * , `
    tokens = re.split(r"(\*\*|\*|`)", text)
    runs = []
    bold, ital, code = base_bold, base_italic, False
    for tok in tokens:
        if tok == "**":
            bold = not bold; continue
        if tok == "*":
            ital = not ital; continue
        if tok == "`":
            code = not code; continue
        if tok == "":
            continue
        runs.append((tok, bold, ital, code, color))
    return runs


def run_xml(text, bold, ital, code, color=None, size=None):
    rpr = "<w:rPr>"
    if bold:
        rpr += "<w:b/>"
    if ital:
        rpr += "<w:i/>"
    if code:
        rpr += "<w:rFonts w:ascii='Consolas' w:hAnsi='Consolas'/>"
    if color:
        rpr += f"<w:color w:val='{color}'/>"
    if size:
        rpr += f"<w:sz w:val='{size}'/><w:szCs w:val='{size}'/>"
    rpr += "</w:rPr>"
    # preserve spaces
    return (f"<w:r>{rpr}<w:t xml:space='preserve'>{xml_escape(text)}</w:t></w:r>")


def para(runs, style=None, align=None, spacing_after=120):
    ppr = "<w:pPr>"
    if style:
        ppr += f"<w:pStyle w:val='{style}'/>"
    if align:
        ppr += f"<w:jc w:val='{align}'/>"
    ppr += f"<w:spacing w:after='{spacing_after}'/></w:pPr>"
    body = "".join(run_xml(*r) if len(r) == 5 else run_xml(*r) for r in runs)
    return f"<w:p>{ppr}{body}</w:p>"


def heading(text, level):
    style = "Title" if level == 0 else f"Heading{level}"
    runs = inline_runs(text)
    return para(runs, style=style, spacing_after=160)


def body_para(text, align="both"):
    return para(inline_runs(text), align=align)


def caption_para(text):
    # text already includes "Figure N." etc.; italic
    return para(inline_runs(text, base_italic=True), align="both", spacing_after=200)


def note_para(text):
    runs = inline_runs(text, base_italic=True)
    ppr = ("<w:pPr><w:pBdr><w:left w:val='single' w:sz='18' w:space='8' "
           "w:color='8E44AD'/></w:pBdr><w:ind w:left='240'/>"
           "<w:spacing w:after='160'/></w:pPr>")
    body = "".join(run_xml(*r) for r in runs)
    return f"<w:p>{ppr}{body}</w:p>"


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------
def table_xml(rows):
    # rows: list of list of cell-text; first row = header
    ncol = max(len(r) for r in rows)
    borders = ("<w:tblBorders>"
               + "".join(f"<w:{e} w:val='single' w:sz='4' w:space='0' w:color='B8C2CC'/>"
                         for e in ["top", "left", "bottom", "right", "insideH", "insideV"])
               + "</w:tblBorders>")
    tblpr = ("<w:tblPr><w:tblStyle w:val='TableGrid'/>"
             "<w:tblW w:w='5000' w:type='pct'/>"
             + borders + "<w:tblLook w:firstRow='1'/></w:tblPr>")
    grid = "<w:tblGrid>" + "".join("<w:gridCol/>" for _ in range(ncol)) + "</w:tblGrid>"
    out = [f"<w:tbl>{tblpr}{grid}"]
    for ri, row in enumerate(rows):
        is_head = (ri == 0)
        cells = []
        for ci in range(ncol):
            txt = row[ci] if ci < len(row) else ""
            shade = ("<w:shd w:val='clear' w:fill='1F4E79'/>" if is_head
                     else ("<w:shd w:val='clear' w:fill='EEF3F7'/>" if ri % 2 == 0 else ""))
            tcpr = f"<w:tcPr><w:tcW w:w='0' w:type='auto'/>{shade}"\
                   "<w:vAlign w:val='center'/></w:tcPr>"
            color = "FFFFFF" if is_head else None
            runs = inline_runs(txt, base_bold=is_head, color=color)
            cpar = para(runs, align="left", spacing_after=40)
            cells.append(f"<w:tc>{tcpr}{cpar}</w:tc>")
        out.append(f"<w:tr>{''.join(cells)}</w:tr>")
    out.append("</w:tbl>")
    # trailing empty paragraph (Word requires block after table)
    out.append("<w:p><w:pPr><w:spacing w:after='120'/></w:pPr></w:p>")
    return "".join(out)


# ---------------------------------------------------------------------------
# PNG dimension reader
# ---------------------------------------------------------------------------
def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def figure_xml(img_rel_path, rid, abspath):
    w, h = png_size(abspath)
    disp_w = PAGE_WIDTH_PX
    disp_h = int(h * disp_w / w)
    cx = disp_w * EMU_PER_PX
    cy = disp_h * EMU_PER_PX
    drawing = f"""<w:p><w:pPr><w:jc w:val='center'/><w:spacing w:before='120' w:after='60'/></w:pPr><w:r><w:drawing>
<wp:inline distT='0' distB='0' distL='0' distR='0' xmlns:wp='http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'>
<wp:extent cx='{cx}' cy='{cy}'/>
<wp:docPr id='{rid}' name='Figure{rid}'/>
<a:graphic xmlns:a='http://schemas.openxmlformats.org/drawingml/2006/main'>
<a:graphicData uri='http://schemas.openxmlformats.org/drawingml/2006/picture'>
<pic:pic xmlns:pic='http://schemas.openxmlformats.org/drawingml/2006/picture'>
<pic:nvPicPr><pic:cNvPr id='{rid}' name='Figure{rid}'/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed='rId{rid}' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships'/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x='0' y='0'/><a:ext cx='{cx}' cy='{cy}'/></a:xfrm>
<a:prstGeom prst='rect'><a:avLst/></a:prstGeom></pic:spPr></pic:pic>
</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>"""
    return drawing


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------
def parse_markdown(md):
    """Yield body-XML strings and collect image references."""
    lines = md.split("\n")
    blocks = []
    images = []  # (relpath, abspath)
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        s = ln.strip()
        if s == "" or s == "---":
            i += 1
            continue
        # image: ![alt](path)
        m = re.match(r"!\[[^\]]*\]\(([^)]+)\)", s)
        if m:
            rel = m.group(1)
            ab = os.path.join(ROOT, rel)
            # swap .svg -> .png
            if ab.endswith(".svg"):
                ab = ab[:-4] + ".png"
                rel = rel[:-4] + ".png"
            if os.path.exists(ab):
                rid = len(images) + 100
                images.append((rel, ab, rid))
                blocks.append(("fig", rel, ab, rid))
            i += 1
            continue
        # headings
        hm = re.match(r"^(#{1,6})\s+(.*)$", s)
        if hm:
            level = len(hm.group(1))
            blocks.append(("h", min(level, 3), hm.group(2)))
            i += 1
            continue
        # table block
        if s.startswith("|"):
            tbl = []
            while i < n and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                # skip separator row |---|---|
                if re.match(r"^\|[\s:|-]+\|?$", row.replace("--", "-")):
                    i += 1
                    continue
                cells = [c.strip() for c in row.strip("|").split("|")]
                tbl.append(cells)
                i += 1
            blocks.append(("table", tbl))
            continue
        # caption: ***Figure / ***Table ...  (whole paragraph italic/bold)
        if s.startswith("***"):
            # gather until blank
            buf = [s]
            i += 1
            while i < n and lines[i].strip() != "":
                buf.append(lines[i].strip())
                i += 1
            text = " ".join(buf)
            text = text.replace("***", "")  # strip the triple markers; keep inner
            blocks.append(("caption", text))
            continue
        # blockquote note
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            blocks.append(("note", " ".join(buf)))
            continue
        # list item
        if s.startswith("- ") or re.match(r"^\d+\.\s", s):
            buf = []
            while i < n and (lines[i].strip().startswith("- ")
                             or re.match(r"^\d+\.\s", lines[i].strip())):
                item = re.sub(r"^(- |\d+\.\s)", "", lines[i].strip())
                buf.append(item)
                i += 1
            blocks.append(("list", buf))
            continue
        # default paragraph (gather until blank)
        buf = [s]
        i += 1
        while i < n and lines[i].strip() != "" and not lines[i].strip().startswith(("#", "|", "!", "***", ">", "- ")):
            buf.append(lines[i].strip())
            i += 1
        blocks.append(("p", " ".join(buf)))
    return blocks, images


def blocks_to_xml(blocks):
    out = []
    for b in blocks:
        kind = b[0]
        if kind == "h":
            out.append(heading(b[2], b[1]))
        elif kind == "p":
            out.append(body_para(b[1]))
        elif kind == "caption":
            out.append(caption_para(b[1]))
        elif kind == "note":
            out.append(note_para(b[1]))
        elif kind == "table":
            out.append(table_xml(b[1]))
        elif kind == "fig":
            out.append(figure_xml(b[1], b[3], b[2]))
        elif kind == "list":
            for item in b[1]:
                p = para(inline_runs(item), align="both", spacing_after=60)
                # add bullet via indentation + char
                p = p.replace("<w:pPr>", "<w:pPr><w:ind w:left='360' w:hanging='180'/>")
                out.append(para([("•  " + item if False else "", False, False, False, None)]) if False else
                           para(inline_runs("•  " + item), align="both", spacing_after=60))
        else:
            out.append(body_para(str(b)))
    return "".join(out)


# ---------------------------------------------------------------------------
# DOCX packaging
# ---------------------------------------------------------------------------
STYLES = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<w:styles xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii='Calibri' w:hAnsi='Calibri'/><w:sz w:val='21'/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type='paragraph' w:default='1' w:styleId='Normal'><w:name w:val='Normal'/></w:style>
<w:style w:type='paragraph' w:styleId='Title'><w:name w:val='Title'/><w:pPr><w:jc w:val='center'/><w:spacing w:after='240'/></w:pPr><w:rPr><w:b/><w:color w:val='1F4E79'/><w:sz w:val='36'/></w:rPr></w:style>
<w:style w:type='paragraph' w:styleId='Heading1'><w:name w:val='heading 1'/><w:basedOn w:val='Normal'/><w:pPr><w:keepNext/><w:spacing w:before='240' w:after='120'/></w:pPr><w:rPr><w:b/><w:color w:val='1F4E79'/><w:sz w:val='28'/></w:rPr></w:style>
<w:style w:type='paragraph' w:styleId='Heading2'><w:name w:val='heading 2'/><w:basedOn w:val='Normal'/><w:pPr><w:keepNext/><w:spacing w:before='200' w:after='100'/></w:pPr><w:rPr><w:b/><w:color w:val='2E6CA4'/><w:sz w:val='24'/></w:rPr></w:style>
<w:style w:type='paragraph' w:styleId='Heading3'><w:name w:val='heading 3'/><w:basedOn w:val='Normal'/><w:pPr><w:keepNext/><w:spacing w:before='160' w:after='80'/></w:pPr><w:rPr><w:b/><w:color w:val='5B6B7B'/><w:sz w:val='22'/></w:rPr></w:style>
<w:style w:type='table' w:styleId='TableGrid'><w:name w:val='Table Grid'/><w:tblPr><w:tblBorders><w:top w:val='single' w:sz='4' w:color='B8C2CC'/><w:left w:val='single' w:sz='4' w:color='B8C2CC'/><w:bottom w:val='single' w:sz='4' w:color='B8C2CC'/><w:right w:val='single' w:sz='4' w:color='B8C2CC'/><w:insideH w:val='single' w:sz='4' w:color='B8C2CC'/><w:insideV w:val='single' w:sz='4' w:color='B8C2CC'/></w:tblBorders></w:tblPr></w:style>
</w:styles>"""

CONTENT_TYPES_HEAD = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<Types xmlns='http://schemas.openxmlformats.org/package/2006/content-types'>
<Default Extension='rels' ContentType='application/vnd.openxmlformats-package.relationships+xml'/>
<Default Extension='xml' ContentType='application/xml'/>
<Default Extension='png' ContentType='image/png'/>
<Override PartName='/word/document.xml' ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'/>
<Override PartName='/word/styles.xml' ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml'/>
</Types>"""

ROOT_RELS = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'>
<Relationship Id='rId1' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument' Target='word/document.xml'/>
</Relationships>"""


def build():
    with open(MD) as f:
        md = f.read()
    blocks, images = parse_markdown(md)
    body = blocks_to_xml(blocks)

    sectpr = ("<w:sectPr><w:pgSz w:w='11906' w:h='16838'/>"
              "<w:pgMar w:top='1440' w:right='1440' w:bottom='1440' w:left='1440' "
              "w:header='720' w:footer='720' w:gutter='0'/></w:sectPr>")
    document = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
        "<w:document xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main' "
        "xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships'>"
        f"<w:body>{body}{sectpr}</w:body></w:document>"
    )

    # document rels (image embeds)
    rels = ["<?xml version='1.0' encoding='UTF-8' standalone='yes'?>",
            "<Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'>",
            "<Relationship Id='rIdStyles' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles' Target='styles.xml'/>"]
    media = []
    for rel, ab, rid in images:
        name = os.path.basename(ab)
        rels.append(f"<Relationship Id='rId{rid}' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/image' Target='media/{name}'/>")
        media.append((name, ab))
    rels.append("</Relationships>")
    document_rels = "".join(rels)

    # fix styles relationship id reference in document.xml: Word expects styles via rels
    # (we referenced rIdStyles; ensure styles part declared in content types already)

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES_HEAD)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/_rels/document.xml.rels", document_rels)
        for name, ab in media:
            with open(ab, "rb") as f:
                z.writestr(f"word/media/{name}", f.read())
    print("wrote", OUT, f"({os.path.getsize(OUT)} bytes, {len(media)} figures)")


if __name__ == "__main__":
    build()
