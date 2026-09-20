#!/usr/bin/env python3
"""Extract every display equation from the manuscript as raw (Word-ready) LaTeX.
Word's equation editor accepts LaTeX input: on the Equation tab set the input
mode to 'LaTeX', paste the string, then press Space / 'Convert' to render it.
Outputs:
  Equations_WordLaTeX.md    -- readable numbered listing (fenced LaTeX)
  Equations_WordLaTeX.docx  -- each equation as a paragraph (Consolas), Word-ready
"""
import re, html, zipfile

SRC = "Irreversibility_Casson_Hybrid_Squeezing_Paper.md"

def extract():
    t = open(SRC, encoding="utf-8").read()
    blocks = re.findall(r'\$\$(.+?)\$\$', t, flags=re.DOTALL)
    eqs = []
    for b in blocks:
        m = re.search(r'\\tag\{(\d+)\}', b)
        num = int(m.group(1)) if m else None
        latex = re.sub(r'\\tag\{\d+\}', '', b)
        latex = ' '.join(latex.split())          # collapse newlines/space
        latex = latex.strip()
        eqs.append((num, latex))
    # keep only tagged, order by tag
    eqs = [(n, l) for (n, l) in eqs if n is not None]
    eqs.sort(key=lambda x: x[0])
    return eqs

def write_md(eqs):
    out = ["# Equations (Word-ready LaTeX) — Irreversibility Casson Hybrid Squeezing Manuscript",
           "",
           "**How to use in Microsoft Word:** Insert → Equation (Alt+=), set the equation input mode to **LaTeX** (Equation tab → *{ }LaTeX*), paste the string for the equation you need, then press **Space** or click **Convert** to render it as a native Word equation.",
           ""]
    for n, l in eqs:
        out.append(f"**({n})**")
        out.append("```latex")
        out.append(l)
        out.append("```")
        out.append("")
    open("Equations_WordLaTeX.md", "w", encoding="utf-8").write("\n".join(out))
    return len(eqs)

# ---- minimal docx (raw LaTeX text, Consolas) --------------------------------
def esc(s): return html.escape(s, quote=False)
def write_docx(eqs):
    body = []
    def para(inner, style=None):
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
        return f'<w:p>{ppr}{inner}</w:p>'
    def run(text, bold=False, mono=False, sz=None, color=None):
        rpr = '<w:rPr>'
        if bold: rpr += '<w:b/>'
        if mono: rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
        if color: rpr += f'<w:color w:val="{color}"/>'
        if sz: rpr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
        rpr += '</w:rPr>'
        return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'
    # title + instructions
    body.append(para(run("Equations (Word-ready LaTeX)", bold=True, sz=32), style="Title"))
    body.append(para(run("Manuscript: Irreversibility Analysis of a Radiative Casson Hybrid "
                         "Nanofluid Between Squeezing Porous Plates.", sz=22)))
    body.append(para(run("How to use: Insert > Equation (Alt+=); on the Equation tab set input "
                         "mode to LaTeX; paste an equation string; press Space/Convert to render.",
                         sz=20, color="555555")))
    body.append(para(run("")))
    for n, l in eqs:
        body.append(para(run(f"({n})", bold=True, sz=22)))
        body.append(para(run(l, mono=True, sz=20)))
        body.append(para(run("")))
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                f'<w:body>{"".join(body)}'
                '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                '<w:pgMar w:top="1440" w:bottom="1440" w:left="1440" w:right="1440"/></w:sectPr>'
                '</w:body></w:document>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
              '<w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
              '<w:pPr><w:spacing w:after="80"/></w:pPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
              '<w:pPr><w:jc w:val="center"/><w:spacing w:after="200"/></w:pPr>'
              '<w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style></w:styles>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '</Relationships>')
    with zipfile.ZipFile("Equations_WordLaTeX.docx", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct)
        z.writestr('_rels/.rels', rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', styles)
        z.writestr('word/_rels/document.xml.rels', drels)

if __name__ == "__main__":
    eqs = extract()
    n = write_md(eqs)
    write_docx(eqs)
    print(f"Extracted {n} equations -> Equations_WordLaTeX.md and Equations_WordLaTeX.docx")
    print("tags:", eqs[0][0], "..", eqs[-1][0])
