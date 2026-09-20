#!/usr/bin/env python3
"""
Build a Word (.docx) version of the manuscript
'Irreversibility_Casson_Hybrid_Squeezing_Paper.md'
using ONLY the Python standard library (no python-docx / pandoc available offline).

A .docx is an OOXML zip package. We emit:
  [Content_Types].xml, _rels/.rels, word/document.xml, word/styles.xml.

LaTeX-ish math ($...$ and $$...$$) is converted to readable Unicode
(best-effort; not a full TeX engine). Markdown headings, bold (**..**),
and pipe-tables are rendered as native Word constructs.
"""
import re, zipfile, html, os, struct

SRC = "Irreversibility_Casson_Hybrid_Squeezing_Paper.md"
OUT = "Irreversibility_Casson_Hybrid_Squeezing_Paper.docx"

# registry of embedded images: list of (rId, arcname, filepath, w_px, h_px)
IMAGES = []
def _png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    return struct.unpack('>II', head[16:24])
def register_image(path):
    idx = len(IMAGES) + 1
    rid = 'rIdImg%d' % idx
    arc = 'word/media/image%d.png' % idx
    w, h = _png_size(path)
    IMAGES.append((rid, arc, path, w, h))
    return rid, w, h
def image_paragraph(path):
    rid, w, h = register_image(path)
    target_w = 5486400  # 6.0 in in EMU
    target_h = int(target_w * h / w)
    return (f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{target_w}" cy="{target_h}"/>'
            f'<wp:effectExtent l="0" t="0" r="0" b="0"/>'
            f'<wp:docPr id="{len(IMAGES)}" name="Picture{len(IMAGES)}"/>'
            f'<wp:cNvGraphicFramePr><a:graphicFrameLocks '
            f'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
            f'</wp:cNvGraphicFramePr>'
            f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{len(IMAGES)}" name="Picture{len(IMAGES)}"/>'
            f'<pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/>'
            f'<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
            f'<a:ext cx="{target_w}" cy="{target_h}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            f'</pic:pic></a:graphicData></a:graphic></wp:inline>'
            f'</w:drawing></w:r></w:p>')

# ---------------------------------------------------------------- LaTeX -> Unicode
GREEK = {
    r'\alpha':'α', r'\beta':'β', r'\gamma':'γ', r'\delta':'δ', r'\epsilon':'ε',
    r'\zeta':'ζ', r'\eta':'η', r'\theta':'θ', r'\kappa':'κ', r'\lambda':'λ',
    r'\mu':'μ', r'\nu':'ν', r'\xi':'ξ', r'\pi':'π', r'\rho':'ρ', r'\sigma':'σ',
    r'\tau':'τ', r'\phi':'φ', r'\chi':'χ', r'\psi':'ψ', r'\omega':'ω',
    r'\Gamma':'Γ', r'\Delta':'Δ', r'\Theta':'Θ', r'\Lambda':'Λ', r'\Xi':'Ξ',
    r'\Pi':'Π', r'\Sigma':'Σ', r'\Phi':'Φ', r'\Psi':'Ψ', r'\Omega':'Ω',
}
SYM = {
    r'\partial':'∂', r'\nabla':'∇', r'\infty':'∞', r'\times':'×', r'\cdot':'·',
    r'\pm':'±', r'\mp':'∓', r'\leq':'≤', r'\le':'≤', r'\geq':'≥', r'\ge':'≥',
    r'\neq':'≠', r'\approx':'≈', r'\equiv':'≡', r'\Rightarrow':'⇒',
    r'\rightarrow':'→', r'\to':'→', r'\in':'∈', r'\int':'∫', r'\sum':'Σ',
    r'\sqrt':'√', r'\hbar':'ℏ', r'\ge1':'≥1', r'\ldots':'…', r'\cdots':'⋯',
    r'\,':' ', r'\;':' ', r'\!':'', r'\quad':'   ', r'\qquad':'      ',
    r'\left':'', r'\right':'', r'\big':'', r'\Big':'', r'\!\left':'',
}
SUP = str.maketrans('0123456789+-=()niIvxm', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱᴵᵛˣᵐ')
SUB = str.maketrans('0123456789+-=()aeoxhijklmnpst',
                    '₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₕᵢⱼₖₗₘₙₚₛₜ')

def _supsub(s):
    # ^{...} and _{...}
    def sup(m):
        t = m.group(1)
        try: return t.translate(SUP) if all(c in '0123456789+-=()niIvxm' for c in t) else '^('+t+')'
        except: return '^('+t+')'
    def sub(m):
        t = m.group(1)
        try: return t.translate(SUB) if all(c in '0123456789+-=()aeoxhijklmnpst' for c in t) else '_('+t+')'
        except: return '_('+t+')'
    s = re.sub(r'\^\{([^{}]*)\}', sup, s)
    s = re.sub(r'_\{([^{}]*)\}', sub, s)
    # single char ^2 _i
    s = re.sub(r'\^([0-9niIvxm+\-])', lambda m: m.group(1).translate(SUP), s)
    s = re.sub(r'_([0-9aeoxhijklmnpst+\-])', lambda m: m.group(1).translate(SUB), s)
    return s

def _frac(s):
    # \frac{a}{b} and \tfrac{a}{b} and \dfrac -> (a)/(b), iterate for nesting
    pat = re.compile(r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}')
    for _ in range(6):
        s2 = pat.sub(r'(\1)/(\2)', s)
        if s2 == s: break
        s = s2
    return s

def latex_to_unicode(s):
    # unwrap \text{...}/\mathrm{...} keeping inner content (avoid double braces)
    s = re.sub(r'\\(?:text|mathrm|mathbf|operatorname)\{([^{}]*)\}', r'\1', s)
    s = s.replace(r'\boxed', '')
    s = re.sub(r'\\tag\{([^{}]*)\}', r'   (\1)', s)   # equation number
    # subscripts/superscripts FIRST so brace-bearing denominators (e.g. \kappa_{hnf}) lose braces
    s = _supsub(s)
    # fractions with braces, then bare two-digit forms like \tfrac43
    s = _frac(s)
    s = re.sub(r'\\[dt]?frac(\w)(\w)', r'(\1)/(\2)', s)
    for k, v in sorted(GREEK.items(), key=lambda x:-len(x[0])): s = s.replace(k, v)
    for k, v in sorted(SYM.items(), key=lambda x:-len(x[0])):   s = s.replace(k, v)
    s = s.replace(r'\beta^*', 'β*').replace('^*', '*')
    # cleanup leftover braces / backslashes / align markers
    s = s.replace('&', ' ').replace(r'\\', '  ')
    s = re.sub(r'\\[a-zA-Z]+', '', s)      # drop unknown commands
    s = s.replace('{', '').replace('}', '').replace(r'\;', ' ').replace(r'\,', ' ')
    s = re.sub(r'[ \t]{2,}', ' ', s).strip()
    return s

# ---------------------------------------------------------------- OOXML helpers
def esc(t): return html.escape(t, quote=False)

def run(text, bold=False, italic=False, sz=None):
    rpr = ''
    if bold or italic or sz:
        rpr = '<w:rPr>'
        if bold: rpr += '<w:b/>'
        if italic: rpr += '<w:i/>'
        if sz: rpr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
        rpr += '</w:rPr>'
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

def runs_from_bold(text):
    """Split **bold** segments into runs."""
    out, i = [], 0
    for m in re.finditer(r'\*\*(.+?)\*\*', text):
        if m.start() > i: out.append(run(text[i:m.start()]))
        out.append(run(m.group(1), bold=True))
        i = m.end()
    if i < len(text): out.append(run(text[i:]))
    return ''.join(out) if out else run(text)

def para(inner, style=None, align=None, spacing_before=None):
    ppr = '<w:pPr>'
    if style: ppr += f'<w:pStyle w:val="{style}"/>'
    if align: ppr += f'<w:jc w:val="{align}"/>'
    if spacing_before: ppr += f'<w:spacing w:before="{spacing_before}"/>'
    ppr += '</w:pPr>'
    if ppr == '<w:pPr></w:pPr>': ppr = ''
    return f'<w:p>{ppr}{inner}</w:p>'

def eq_para(text):
    # centered, italic equation line rendered as Unicode text
    return para(run(text, italic=True), align='center')

# ---------------------------------------------------------------- table builder
def build_table(rows):
    header = rows[0]
    ncol = len(header)
    grid = ''.join('<w:gridCol/>' for _ in range(ncol))
    body = ''
    for ri, r in enumerate(rows):
        cells = ''
        for c in r:
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if ri == 0 else ''
            content = runs_from_bold(latex_inline(c))
            jc = '<w:jc w:val="left"/>'
            cells += (f'<w:tc><w:tcPr><w:tcBorders>'
                      f'<w:top w:val="single" w:sz="4" w:color="808080"/>'
                      f'<w:bottom w:val="single" w:sz="4" w:color="808080"/>'
                      f'<w:left w:val="single" w:sz="4" w:color="808080"/>'
                      f'<w:right w:val="single" w:sz="4" w:color="808080"/>'
                      f'</w:tcBorders>{shade}</w:tcPr>'
                      f'<w:p><w:pPr>{jc}</w:pPr>{content}</w:p></w:tc>')
        body += f'<w:tr>{cells}</w:tr>'
    return (f'<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>'
            f'<w:tblBorders>'
            f'<w:top w:val="single" w:sz="4" w:color="808080"/>'
            f'<w:bottom w:val="single" w:sz="4" w:color="808080"/>'
            f'<w:left w:val="single" w:sz="4" w:color="808080"/>'
            f'<w:right w:val="single" w:sz="4" w:color="808080"/>'
            f'<w:insideH w:val="single" w:sz="4" w:color="808080"/>'
            f'<w:insideV w:val="single" w:sz="4" w:color="808080"/>'
            f'</w:tblBorders></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>{body}</w:tbl>')

def latex_inline(text):
    """Convert inline $...$ inside a text line to unicode; leave rest."""
    def repl(m): return latex_to_unicode(m.group(1))
    return re.sub(r'\$([^$]+)\$', repl, text)

# ---------------------------------------------------------------- markdown parser
def parse(md):
    lines = md.split('\n')
    body = []
    i, n = 0, len(lines)
    in_math = False
    math_buf = []
    while i < n:
        line = lines[i]

        # block math $$ ... $$
        if line.strip().startswith('$$'):
            content = line.strip()[2:]
            if content.strip().endswith('$$') and len(content.strip()) > 2:
                inner = content.strip()[:-2]
                body.append(eq_para(latex_to_unicode(inner)))
                i += 1; continue
            in_math = True; math_buf = []
            rest = content
            if rest.strip(): math_buf.append(rest)
            i += 1
            while i < n and not lines[i].strip().endswith('$$'):
                math_buf.append(lines[i]); i += 1
            if i < n:
                last = lines[i].strip()[:-2]
                if last.strip(): math_buf.append(last)
                i += 1
            joined = ' '.join(x.strip() for x in math_buf if x.strip())
            body.append(eq_para(latex_to_unicode(joined)))
            continue

        # headings
        m = re.match(r'^(#{1,4})\s+(.*)$', line)
        if m:
            level = len(m.group(1)); txt = latex_inline(m.group(2))
            if level == 1:
                body.append(para(run(txt, bold=True, sz=32), style='Title', align='center'))
            else:
                style = {2:'Heading1', 3:'Heading2', 4:'Heading3'}[level]
                body.append(para(runs_from_bold(txt), style=style))
            i += 1; continue

        # image line ![alt](path)
        mimg = re.match(r'^!\[[^\]]*\]\(([^)]+)\)\s*$', line)
        if mimg:
            ipath = mimg.group(1)
            if os.path.exists(ipath):
                body.append(image_paragraph(ipath))
            else:
                body.append(para(run('[missing image: %s]' % ipath, italic=True), align='center'))
            i += 1; continue

        # horizontal rule
        if re.match(r'^-{3,}\s*$', line):
            body.append(para(run('')))
            i += 1; continue

        # table block
        if '|' in line and i+1 < n and re.match(r'^\s*\|?[\s:\-|]+\|?\s*$', lines[i+1]):
            tbl_rows = []
            while i < n and '|' in lines[i]:
                if re.match(r'^\s*\|?[\s:\-|]+\|?\s*$', lines[i]):
                    i += 1; continue
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                tbl_rows.append(cells)
                i += 1
            if tbl_rows: body.append(build_table(tbl_rows))
            continue

        # bullet / numbered list
        m = re.match(r'^\s*([-*]|\d+\.)\s+(.*)$', line)
        if m:
            txt = latex_inline(m.group(2))
            body.append(para(runs_from_bold(txt), style='ListParagraph'))
            i += 1; continue

        # blank
        if line.strip() == '':
            i += 1; continue

        # normal paragraph (accumulate wrapped lines until blank)
        buf = [line]
        i += 1
        while i < n and lines[i].strip() != '' and not lines[i].startswith('#') \
              and '|' not in lines[i] and not lines[i].strip().startswith('$$') \
              and not lines[i].startswith('![') \
              and not re.match(r'^\s*([-*]|\d+\.)\s+', lines[i]) \
              and not re.match(r'^-{3,}\s*$', lines[i]):
            buf.append(lines[i]); i += 1
        txt = latex_inline(' '.join(buf))
        # italicize the trailing manuscript note
        italic = txt.strip().startswith('*') and txt.strip().endswith('*')
        if italic: txt = txt.strip().strip('*')
        body.append(para(run(txt, italic=True) if italic else runs_from_bold(txt)))
    return '\n'.join(body)

# ---------------------------------------------------------------- package files
STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="1F3864"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="2E5496"/><w:sz w:val="25"/><w:szCs w:val="25"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="160" w:after="80"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:i/><w:color w:val="2E5496"/><w:sz w:val="23"/><w:szCs w:val="23"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="420"/></w:pPr></w:style>
</w:styles>'''

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

def main():
    with open(SRC, encoding='utf-8') as f:
        md = f.read()
    body = parse(md)   # populates IMAGES
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document '
                'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
                f'<w:body>{body}'
                '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                '<w:pgMar w:top="1440" w:bottom="1440" w:left="1440" w:right="1440"/></w:sectPr>'
                '</w:body></w:document>')
    # build document relationships including images
    rel_items = ['<Relationship Id="rId1" '
                 'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
                 'Target="styles.xml"/>']
    for rid, arc, path, w, h in IMAGES:
        target = arc.split('word/', 1)[1]  # relative to word/
        rel_items.append(f'<Relationship Id="{rid}" '
                         f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                         f'Target="{target}"/>')
    doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                + ''.join(rel_items) + '</Relationships>')
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', STYLES)
        for rid, arc, path, w, h in IMAGES:
            with open(path, 'rb') as imgf:
                z.writestr(arc, imgf.read())
        z.writestr('word/_rels/document.xml.rels', doc_rels)
    print('Wrote', OUT, os.path.getsize(OUT), 'bytes;', len(IMAGES), 'images embedded')

if __name__ == '__main__':
    main()
