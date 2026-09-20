#!/usr/bin/env python3
"""Convert the manuscript's 100 LaTeX equations to Word UnicodeMath (linear format).
These strings are pasted DIRECTLY into a Word equation field (Alt+=, default
UnicodeMath mode); pressing Space builds them up into formatted equations.
Outputs: Equations_UnicodeMath.md and Equations_UnicodeMath.docx"""
import re, html, zipfile

SRC = "Irreversibility_Casson_Hybrid_Squeezing_Paper.md"

GREEK = {
 r'\alpha':'α',r'\beta':'β',r'\gamma':'γ',r'\delta':'δ',r'\epsilon':'ε',r'\varepsilon':'ε',
 r'\zeta':'ζ',r'\eta':'η',r'\theta':'θ',r'\kappa':'κ',r'\lambda':'λ',r'\mu':'μ',r'\nu':'ν',
 r'\xi':'ξ',r'\pi':'π',r'\rho':'ρ',r'\sigma':'σ',r'\tau':'τ',r'\phi':'φ',r'\varphi':'φ',
 r'\chi':'χ',r'\psi':'ψ',r'\omega':'ω',r'\Gamma':'Γ',r'\Delta':'Δ',r'\Theta':'Θ',
 r'\Lambda':'Λ',r'\Xi':'Ξ',r'\Pi':'Π',r'\Sigma':'Σ',r'\Phi':'Φ',r'\Psi':'Ψ',r'\Omega':'Ω',
}
SYM = {
 r'\partial':'∂',r'\nabla':'∇',r'\infty':'∞',r'\times':'×',r'\cdot':'⋅',r'\pm':'±',
 r'\mp':'∓',r'\leq':'≤',r'\le':'≤',r'\geq':'≥',r'\ge':'≥',r'\neq':'≠',r'\approx':'≈',
 r'\equiv':'≡',r'\to':'→',r'\rightarrow':'→',r'\Rightarrow':'⇒',r'\in':'∈',
 r'\ldots':'…',r'\cdots':'⋯',r'\hbar':'ℏ',r'\int':'∫',r'\oint':'∮',r'\sum':'∑',r'\prod':'∏',
}
DROP = [r'\left',r'\right',r'\!',r'\bigl',r'\bigr',r'\Big',r'\big']
SPACE = {r'\,':' ',r'\;':' ',r'\:':' ',r'\quad':'  ',r'\qquad':'   ',r'\\':' '}
MARK = 'ĈASĒ'

def _iter(pat, repl, s):
    for _ in range(8):
        ns = re.sub(pat, repl, s)
        if ns == s: return ns
        s = ns
    return s

def convline(s):
    for d in DROP: s = s.replace(d, '')
    s = s.replace('\\ ', ' ')                    # LaTeX control space
    for k, v in SPACE.items(): s = s.replace(k, v)
    # font commands (\mathcal{L} -> L) rendered transparent
    s = _iter(r'\\(?:mathcal|mathbf|mathrm|mathbb|mathsf|mathit|boldsymbol|operatorname|text|mathfrak)\{([^{}]*)\}', r'\1', s)
    # subscripts/superscripts braces -> parentheses (innermost first)
    s = _iter(r'\^\{([^{}]*)\}', r'^(\1)', s)
    s = _iter(r'_\{([^{}]*)\}', r'_(\1)', s)
    # radicals & accents FIRST so their braces vanish before fraction matching
    s = _iter(r'\\sqrt\{([^{}]*)\}', r'√(\1)', s)
    s = _iter(r'\\overline\{([^{}]*)\}', lambda m: '(' + m.group(1) + ')\u0304', s)
    s = _iter(r'\\hat\{([^{}]*)\}', lambda m: '(' + m.group(1) + ')\u0302', s)
    # fractions (braces now free of nested {}) innermost first
    s = _iter(r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}', r'(\1)/(\2)', s)
    s = _iter(r'\\[dt]?frac(\w)(\w)', r'(\1)/(\2)', s)
    # functions
    for fn in ('exp','log','ln','sin','cos','tan'):
        s = s.replace('\\'+fn, fn)
    # greek + symbols
    for k, v in sorted(GREEK.items(), key=lambda x:-len(x[0])): s = s.replace(k, v)
    for k, v in sorted(SYM.items(), key=lambda x:-len(x[0])):   s = s.replace(k, v)
    s = s.replace(r'\beta^*', 'β^∗').replace('^*', '^∗')
    # leftover single-char scripts already fine (A_1, y^2). Drop remaining commands.
    s = re.sub(r'\\(bar|hat)', lambda m: '\u0304' if m.group(1)=='bar' else '\u0302', s)
    s = re.sub(r'\\[A-Za-z]+', lambda m: m.group(0)[1:], s)  # unknown cmd -> its name
    s = s.replace('{', '(').replace('}', ')')
    s = re.sub(r'[ \t]{2,}', ' ', s)
    return s.strip()

def cases_unicode(body):
    rows = re.split(r'\\\\', body)
    parts = []
    for r in rows:
        r = re.sub(r'^\s*\[[^\]]*\]', '', r)
        if r.strip() == '': continue
        cells = [convline(c) for c in r.split('&')]
        parts.append('&'.join(cells) if len(cells) > 1 else cells[0])
    return '{█(' + '@'.join(parts) + ')┤'

def conv(latex):
    latex = latex.strip().rstrip(',').rstrip('.')
    store = {}
    def grab(m):
        key = MARK + str(len(store)) + MARK
        store[key] = cases_unicode(m.group(1))
        return key
    latex = re.sub(r'\\begin\{cases\}(.*?)\\end\{cases\}', grab, latex, flags=re.DOTALL)
    out = convline(latex)
    for k, v in store.items(): out = out.replace(convline(k), v).replace(k, v)
    return out

def extract():
    t = open(SRC, encoding='utf-8').read()
    blocks = re.findall(r'\$\$(.+?)\$\$', t, flags=re.DOTALL)
    eqs = []
    for b in blocks:
        mm = re.search(r'\\tag\{(\d+)\}', b)
        if not mm: continue
        latex = re.sub(r'\\tag\{\d+\}', '', b)
        eqs.append((int(mm.group(1)), ' '.join(latex.split())))
    eqs.sort(key=lambda x: x[0])
    return eqs

def write_md(eqs):
    o = ["# Equations — Word UnicodeMath (linear) form",
         "",
         "**Direct paste into Word:** press **Alt + =** to open an equation field (keep the "
         "default *UnicodeMath* input mode — NOT LaTeX), paste one line below, then press "
         "**Space** (or Enter) to build it up into a formatted equation.",
         ""]
    for n, l in eqs:
        o.append(f"**({n})**")
        o.append("```")
        o.append(conv(l))
        o.append("```")
        o.append("")
    open("Equations_UnicodeMath.md", "w", encoding="utf-8").write("\n".join(o))

def esc(s): return html.escape(s, quote=False)
def write_docx(eqs):
    body = []
    def para(inner, style=None):
        p = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
        return f'<w:p>{p}{inner}</w:p>'
    def run(t, bold=False, mono=False, sz=None, color=None):
        rpr = '<w:rPr>'
        if bold: rpr += '<w:b/>'
        if mono: rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
        if color: rpr += f'<w:color w:val="{color}"/>'
        if sz: rpr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
        rpr += '</w:rPr>'
        return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(t)}</w:t></w:r>'
    body.append(para(run("Equations — Word UnicodeMath (linear) form", bold=True, sz=30), style="Title"))
    body.append(para(run("Manuscript: Irreversibility Analysis of a Radiative Casson Hybrid "
                         "Nanofluid Between Squeezing Porous Plates.", sz=22)))
    body.append(para(run("Direct paste: Alt+= to open an equation field (keep default UnicodeMath "
                         "mode, not LaTeX); paste a line; press Space to build up.", sz=20, color="555555")))
    body.append(para(run("")))
    for n, l in eqs:
        body.append(para(run(f"({n})", bold=True, sz=22)))
        body.append(para(run(conv(l), mono=True, sz=20)))
        body.append(para(run("")))
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                f'<w:body>{"".join(body)}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                '<w:pgMar w:top="1440" w:bottom="1440" w:left="1440" w:right="1440"/></w:sectPr>'
                '</w:body></w:document>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
              '<w:pPr><w:spacing w:after="60"/></w:pPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
              '<w:pPr><w:jc w:val="center"/><w:spacing w:after="200"/></w:pPr>'
              '<w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:style></w:styles>')
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
    with zipfile.ZipFile("Equations_UnicodeMath.docx", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct); z.writestr('_rels/.rels', rels)
        z.writestr('word/document.xml', document); z.writestr('word/styles.xml', styles)
        z.writestr('word/_rels/document.xml.rels', drels)

if __name__ == "__main__":
    eqs = extract()
    write_md(eqs); write_docx(eqs)
    print("Wrote Equations_UnicodeMath.md/.docx with", len(eqs), "equations")
    for n in (6, 13, 63, 99, 100):
        l = dict(eqs)[n]; print(f"({n})", conv(l))
