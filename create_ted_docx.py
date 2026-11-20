#!/usr/bin/env python3
"""
Build Manuscript_TED_Single_Delay_Microbeams.docx from the Markdown source.

Standard library only. Features:
  * headings, paragraphs with **bold**, *italic*, inline $math$
  * display equations $$ ... \\tag{n} $$ converted to native Word (OMML)
    equations with right-aligned numbers
  * pipe tables, embedded PNG figures with captions, numbered references
The LaTeX -> OMML converter supports the subset used in the manuscript.
"""

import os
import re
import struct
import zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Manuscript_TED_Single_Delay_Microbeams.md")
OUT = os.path.join(HERE, "Manuscript_TED_Single_Delay_Microbeams.docx")

# ---------------------------------------------------------------------------
# LaTeX subset -> OMML
# ---------------------------------------------------------------------------
SYMBOLS = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ϵ", "varepsilon": "ε",
    "theta": "θ", "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ", "pi": "π", "rho": "ρ",
    "sigma": "σ", "tau": "τ", "upsilon": "υ", "phi": "φ", "chi": "χ", "psi": "ψ", "omega": "ω",
    "kappa": "κ", "Delta": "Δ", "Theta": "Θ", "Omega": "Ω", "Phi": "Φ", "Gamma": "Γ",
    "nabla": "∇", "partial": "∂", "int": "∫", "pm": "±", "approx": "≈", "ll": "≪", "gg": "≫",
    "le": "≤", "ge": "≥", "leq": "≤", "geq": "≥", "cdot": "·", "times": "×", "infty": "∞",
    "to": "→", "propto": "∝", "dots": "…", "ldots": "…", "gtrsim": "≳", "lesssim": "≲",
    "langle": "⟨", "rangle": "⟩", "neq": "≠", "sim": "∼",
}
FUNCS = {"sin", "cos", "tan", "sinh", "cosh", "tanh", "exp", "ln", "log", "max", "min", "Re", "Im"}
SPACES = {",": "\u2009", ";": "\u2005", "quad": "\u2003", "qquad": "\u2003\u2003", " ": " ", "!": ""}
ACCENTS = {"dot": "\u0307", "ddot": "\u0308", "hat": "\u0302", "bar": "\u0305", "tilde": "\u0303"}


def tokenize(s):
    toks, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+)", s[i:])
            if m:
                toks.append(("cmd", m.group(1)))
                i += len(m.group(0))
                continue
            toks.append(("cmd", s[i + 1]))
            i += 2
            continue
        if c in "{}^_":
            toks.append((c, c))
        elif c.isspace():
            pass
        else:
            toks.append(("ch", c))
        i += 1
    return toks


class P:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self):
        tok = self.peek()
        self.i += 1
        return tok

    def group(self):
        """Parse a {...} group or a single atom; return OMML string."""
        k, v = self.peek()
        if k == "{":
            self.take()
            out = self.expr(stop="}")
            self.take()
            return out
        return self.atom()

    def raw_text_group(self):
        k, v = self.take()
        if k != "{":
            return v or ""
        depth, out = 1, []
        while True:
            k, v = self.take()
            if k is None:
                break
            if k == "{":
                depth += 1
            elif k == "}":
                depth -= 1
                if depth == 0:
                    break
            if k == "cmd":
                out.append(SYMBOLS.get(v, SPACES.get(v, v)))
            else:
                out.append(v)
        return "".join(out)

    def expr(self, stop=None):
        parts = []
        while True:
            k, v = self.peek()
            if k is None or (stop and k == stop):
                break
            if k == "cmd" and v == "right":
                break
            parts.append(self.script())
        return "".join(parts)

    def script(self):
        base = self.atom()
        sub = sup = None
        while True:
            k, v = self.peek()
            if k == "^" and sup is None:
                self.take()
                sup = self.group()
            elif k == "_" and sub is None:
                self.take()
                sub = self.group()
            else:
                break
        if sub is not None and sup is not None:
            return "<m:sSubSup><m:e>%s</m:e><m:sub>%s</m:sub><m:sup>%s</m:sup></m:sSubSup>" % (base, sub, sup)
        if sup is not None:
            return "<m:sSup><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>" % (base, sup)
        if sub is not None:
            return "<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>" % (base, sub)
        return base

    def atom(self):
        k, v = self.take()
        if k is None:
            return ""
        if k == "{":
            out = self.expr(stop="}")
            self.take()
            return out
        if k == "ch":
            return run("\u2212" if v == "-" else v)
        if k in ("^", "_"):
            return ""
        # commands
        if v == "frac":
            a = self.group()
            b = self.group()
            return "<m:f><m:num>%s</m:num><m:den>%s</m:den></m:f>" % (a, b)
        if v == "sqrt":
            a = self.group()
            return "<m:rad><m:radPr><m:degHide m:val=\"1\"/></m:radPr><m:deg/><m:e>%s</m:e></m:rad>" % a
        if v in ACCENTS:
            a = self.group()
            return "<m:acc><m:accPr><m:chr m:val=\"%s\"/></m:accPr><m:e>%s</m:e></m:acc>" % (ACCENTS[v], a)
        if v in ("mathrm", "text", "operatorname", "mathbf"):
            txt = self.raw_text_group()
            return run(txt, upright=True, bold=(v == "mathbf"))
        if v == "left":
            k2, opener = self.take()
            opener = SYMBOLS.get(opener, opener) if k2 == "cmd" else opener
            inner = self.expr()
            self.take()  # \right
            k3, closer = self.take()
            closer = SYMBOLS.get(closer, closer) if k3 == "cmd" else closer
            if opener == ".":
                opener = ""
            if closer == ".":
                closer = ""
            return ("<m:d><m:dPr><m:begChr m:val=\"%s\"/><m:endChr m:val=\"%s\"/></m:dPr><m:e>%s</m:e></m:d>"
                    % (escape(opener), escape(closer), inner))
        if v in FUNCS:
            return run(v, upright=True)
        if v in SYMBOLS:
            return run(SYMBOLS[v])
        if v in SPACES:
            return run(SPACES[v]) if SPACES[v] else ""
        if v in ("{", "}", "|", "%", "&", "#", "$"):
            return run(v)
        return run(v)


def run(text, upright=False, bold=False):
    if not text:
        return ""
    rpr = ""
    if upright or bold:
        rpr = "<m:rPr><m:sty m:val=\"%s\"/></m:rPr>" % ("b" if bold else "p")
    return "<m:r>%s<w:rPr><w:rFonts w:ascii=\"Cambria Math\" w:hAnsi=\"Cambria Math\"/></w:rPr><m:t xml:space=\"preserve\">%s</m:t></m:r>" % (rpr, escape(text))


def latex_to_omml(tex):
    return "<m:oMath>%s</m:oMath>" % P(tokenize(tex)).expr()


# ---------------------------------------------------------------------------
# Inline text -> runs (bold, italic, inline math)
# ---------------------------------------------------------------------------
def wrun(text, bold=False, italic=False, size=None, sup=False, color=None):
    rpr = []
    if bold:
        rpr.append("<w:b/>")
    if italic:
        rpr.append("<w:i/>")
    if color:
        rpr.append("<w:color w:val=\"%s\"/>" % color)
    if size:
        rpr.append("<w:sz w:val=\"%d\"/><w:szCs w:val=\"%d\"/>" % (size, size))
    if sup:
        rpr.append("<w:vertAlign w:val=\"superscript\"/>")
    return "<w:r><w:rPr>%s</w:rPr><w:t xml:space=\"preserve\">%s</w:t></w:r>" % ("".join(rpr), escape(text))


def inline(text, size=None, base_bold=False, base_italic=False):
    out = []
    # split on inline math first
    for i, seg in enumerate(re.split(r"(\$[^$]+\$)", text)):
        if not seg:
            continue
        if seg.startswith("$") and seg.endswith("$") and len(seg) > 1:
            out.append(latex_to_omml(seg[1:-1]))
            continue
        for part in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)", seg):
            if not part:
                continue
            if part.startswith("**") and part.endswith("**"):
                out.append(_md_inner(part[2:-2], size, True, base_italic))
            elif part.startswith("*") and part.endswith("*") and len(part) > 2:
                out.append(_md_inner(part[1:-1], size, base_bold, True))
            elif part.startswith("`") and part.endswith("`"):
                out.append("<w:r><w:rPr><w:rFonts w:ascii=\"Consolas\" w:hAnsi=\"Consolas\"/>%s</w:rPr><w:t xml:space=\"preserve\">%s</w:t></w:r>"
                           % (("<w:sz w:val=\"%d\"/>" % size) if size else "", escape(part[1:-1])))
            else:
                out.append(_unicode_scripts(part, size, base_bold, base_italic))
    return "".join(out)


def _md_inner(text, size, bold, italic):
    # inner text may still contain inline math (handled by caller split) -> plain
    return _unicode_scripts(text, size, bold, italic)


def _unicode_scripts(text, size, bold, italic):
    return wrun(text, bold, italic, size)


def para(inner, style=None, align=None, space_after=120, keep_next=False, indent=None):
    ppr = []
    if style:
        ppr.append("<w:pStyle w:val=\"%s\"/>" % style)
    if keep_next:
        ppr.append("<w:keepNext/>")
    ppr.append("<w:spacing w:after=\"%d\" w:line=\"300\" w:lineRule=\"auto\"/>" % space_after)
    if indent:
        ppr.append(indent)
    if align:
        ppr.append("<w:jc w:val=\"%s\"/>" % align)
    return "<w:p><w:pPr>%s</w:pPr>%s</w:p>" % ("".join(ppr), inner)


def equation_par(tex, num):
    omml = latex_to_omml(tex)
    return ("<w:p><w:pPr><w:tabs><w:tab w:val=\"center\" w:pos=\"4680\"/><w:tab w:val=\"right\" w:pos=\"9360\"/></w:tabs>"
            "<w:spacing w:before=\"60\" w:after=\"120\"/></w:pPr><w:r><w:tab/></w:r>%s<w:r><w:tab/><w:t>(%s)</w:t></w:r></w:p>"
            % (omml, num))


# ---------------------------------------------------------------------------
# Tables and images
# ---------------------------------------------------------------------------
def table_xml(rows):
    ncol = len(rows[0])
    width = 9360 // ncol
    out = ["<w:tbl><w:tblPr><w:tblStyle w:val=\"TableGrid\"/><w:tblW w:w=\"5000\" w:type=\"pct\"/>"
           "<w:tblBorders><w:top w:val=\"single\" w:sz=\"8\" w:color=\"000000\"/><w:bottom w:val=\"single\" w:sz=\"8\" w:color=\"000000\"/>"
           "<w:insideH w:val=\"single\" w:sz=\"2\" w:color=\"BFBFBF\"/></w:tblBorders>"
           "<w:tblCellMar><w:left w:w=\"60\" w:type=\"dxa\"/><w:right w:w=\"60\" w:type=\"dxa\"/></w:tblCellMar></w:tblPr><w:tblGrid>"]
    out.append("".join("<w:gridCol w:w=\"%d\"/>" % width for _ in range(ncol)))
    out.append("</w:tblGrid>")
    for r, row in enumerate(rows):
        out.append("<w:tr>%s" % ("<w:trPr><w:tblHeader/></w:trPr>" if r == 0 else ""))
        for cell in row:
            shade = "<w:shd w:val=\"clear\" w:color=\"auto\" w:fill=\"DEEAF6\"/>" if r == 0 else ""
            out.append("<w:tc><w:tcPr><w:tcW w:w=\"%d\" w:type=\"dxa\"/>%s</w:tcPr>%s</w:tc>"
                       % (width, shade, para(inline(cell.strip(), size=17, base_bold=(r == 0)), align="center", space_after=20)))
        out.append("</w:tr>")
    out.append("</w:tbl>")
    return "".join(out)


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    w, h = struct.unpack(">II", head[16:24])
    return w, h


class Media:
    def __init__(self):
        self.items = []

    def add(self, path):
        rid = "rIdImg%d" % (len(self.items) + 1)
        name = "image%d.png" % (len(self.items) + 1)
        self.items.append((rid, name, path))
        return rid, len(self.items)


def image_xml(rid, idx, path, max_w_in=6.3):
    w, h = png_size(path)
    cx = int(max_w_in * 914400)
    cy = int(cx * h / w)
    if cy > int(7.5 * 914400):
        cy = int(7.5 * 914400)
        cx = int(cy * w / h)
    return ("<w:r><w:drawing><wp:inline distT=\"0\" distB=\"0\" distL=\"0\" distR=\"0\"><wp:extent cx=\"%d\" cy=\"%d\"/>"
            "<wp:docPr id=\"%d\" name=\"Figure %d\"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect=\"1\"/></wp:cNvGraphicFramePr>"
            "<a:graphic><a:graphicData uri=\"http://schemas.openxmlformats.org/drawingml/2006/picture\"><pic:pic>"
            "<pic:nvPicPr><pic:cNvPr id=\"%d\" name=\"image%d.png\"/><pic:cNvPicPr/></pic:nvPicPr>"
            "<pic:blipFill><a:blip r:embed=\"%s\"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>"
            "<pic:spPr><a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"%d\" cy=\"%d\"/></a:xfrm><a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom></pic:spPr>"
            "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>" % (cx, cy, idx, idx, idx, idx, rid, cx, cy))


# ---------------------------------------------------------------------------
# Markdown -> document body
# ---------------------------------------------------------------------------
def build_body(md, media):
    lines = md.split("\n")
    out = []
    i = 0
    in_refs = False
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s or s == "---":
            i += 1
            continue
        # display equation (single or multi line)
        if s.startswith("$$"):
            buf = s[2:]
            while not buf.rstrip().endswith("$$"):
                i += 1
                buf += " " + lines[i].strip()
            tex = buf.rstrip()[:-2].strip()
            m = re.search(r"\\tag\{([^}]*)\}", tex)
            num = m.group(1) if m else ""
            tex = re.sub(r"\\tag\{[^}]*\}", "", tex).strip()
            if num:
                out.append(equation_par(tex, num))
            else:
                out.append("<w:p><w:pPr><w:jc w:val=\"center\"/><w:spacing w:after=\"120\"/></w:pPr>%s</w:p>" % latex_to_omml(tex))
            i += 1
            continue
        if s.startswith("#"):
            level = len(s) - len(s.lstrip("#"))
            text = s.lstrip("#").strip()
            if level == 1:
                out.append(para(inline(text, size=34, base_bold=True), align="center", space_after=240))
            else:
                out.append(para(inline(text), style="Heading%d" % (level - 1), keep_next=True))
            in_refs = text.lower().startswith("references")
            i += 1
            continue
        if s.startswith("!["):
            m = re.match(r"!\[(.*)\]\((.*)\)", s)
            cap, path = m.group(1), os.path.join(HERE, m.group(2))
            rid, idx = media.add(path)
            out.append(para(image_xml(rid, idx, path), align="center", space_after=60, keep_next=True))
            mm = re.match(r"(Figure \d+\.)\s*(.*)", cap)
            out.append(para(wrun(mm.group(1) + " ", bold=True, size=20) + wrun(mm.group(2), size=20), align="both", space_after=240))
            i += 1
            continue
        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"\s*:?-{3,}:?\s*", c) for c in cells):
                    rows.append(cells)
                i += 1
            out.append(table_xml(rows))
            out.append(para("", space_after=120))
            continue
        if re.match(r"^\d+\.\s", s):
            if in_refs:
                n, rest = s.split(".", 1)
                out.append(para(wrun("[%s] " % n, size=20) + inline(rest.strip(), size=20), align="both", space_after=60,
                                indent="<w:ind w:left=\"440\" w:hanging=\"440\"/>"))
            else:
                n, rest = s.split(".", 1)
                out.append(para(wrun(n + ". ") + inline(rest.strip()), align="both", space_after=80,
                                indent="<w:ind w:left=\"360\" w:hanging=\"360\"/>"))
            i += 1
            continue
        if s.startswith("- "):
            out.append(para(wrun("\u2022 ") + inline(s[2:]), align="both", space_after=80,
                            indent="<w:ind w:left=\"360\" w:hanging=\"360\"/>"))
            i += 1
            continue
        if s.startswith("**Table"):
            out.append(para(inline(s, size=20), align="both", space_after=80, keep_next=True))
            i += 1
            continue
        # normal paragraph (join soft-wrapped lines)
        buf = s
        while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^(#|\||!\[|\$\$|- |\d+\.\s|---|\*\*Table)", lines[i + 1].strip()):
            i += 1
            buf += " " + lines[i].strip()
        out.append(para(inline(buf), align="both"))
        i += 1
    return "".join(out)


NS = ('xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
      'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"')

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-GB"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="300" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="360" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/><w:color w:val="1F4E79"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:color w:val="1F4E79"/></w:rPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:color="000000"/><w:bottom w:val="single" w:sz="4" w:color="000000"/></w:tblBorders></w:tblPr></w:style>
</w:styles>"""


def build():
    md = open(SRC, encoding="utf-8").read()
    media = Media()
    body = build_body(md, media)
    sect = ("<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/><w:pgMar w:top=\"1440\" w:right=\"1273\" w:bottom=\"1440\" "
            "w:left=\"1273\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr>")
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:document %s><w:body>%s%s</w:body></w:document>'
                % (NS, body, sect))
    rels = ['<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, name, _ in media.items:
        rels.append('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/%s"/>' % (rid, name))
    doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>'
                % "".join(rels))
    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                     '<Default Extension="xml" ContentType="application/xml"/>'
                     '<Default Extension="png" ContentType="image/png"/>'
                     '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                     '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                     '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
                     '</Types>')
    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                 '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                 '</Relationships>')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>Thermoelastic damping and quality factor of micro/nano-beam resonators under an exact single-delay heat conduction model</dc:title>'
            '</cp:coreProperties>')
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("docProps/core.xml", core)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        for rid, name, path in media.items:
            z.write(path, "word/media/" + name)
    print("wrote", OUT, "| figures:", len(media.items))


if __name__ == "__main__":
    build()
