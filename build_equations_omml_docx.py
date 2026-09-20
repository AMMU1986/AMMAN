#!/usr/bin/env python3
"""Convert the manuscript's 100 LaTeX equations into NATIVE Word equations (OMML)
so they render with proper stacked fractions, powers, radicals, integrals and
piecewise braces on open -- no pasting/conversion needed.

Pure standard library. Output: Equations_WordEditor.docx
Supported LaTeX subset: \\frac \\tfrac \\dfrac, ^ _ (sub/sup/subsup), \\sqrt,
\\left..\\right delimiters, \\int \\sum (n-ary), \\overline, \\hat, Greek and
common operators, \\begin{cases}..\\end{cases}."""
import re, html, zipfile

SRC = "Irreversibility_Casson_Hybrid_Squeezing_Paper.md"
OUT = "Equations_WordEditor.docx"

SYM = {
 r'\alpha':'α',r'\beta':'β',r'\gamma':'γ',r'\delta':'δ',r'\epsilon':'ε',r'\varepsilon':'ε',
 r'\zeta':'ζ',r'\eta':'η',r'\theta':'θ',r'\kappa':'κ',r'\lambda':'λ',r'\mu':'μ',r'\nu':'ν',
 r'\xi':'ξ',r'\pi':'π',r'\rho':'ρ',r'\sigma':'σ',r'\tau':'τ',r'\phi':'φ',r'\varphi':'φ',
 r'\chi':'χ',r'\psi':'ψ',r'\omega':'ω',r'\Gamma':'Γ',r'\Delta':'Δ',r'\Theta':'Θ',
 r'\Lambda':'Λ',r'\Xi':'Ξ',r'\Pi':'Π',r'\Sigma':'Σ',r'\Phi':'Φ',r'\Psi':'Ψ',r'\Omega':'Ω',
 r'\partial':'∂',r'\nabla':'∇',r'\infty':'∞',r'\times':'×',r'\cdot':'·',r'\pm':'±',
 r'\mp':'∓',r'\leq':'≤',r'\le':'≤',r'\geq':'≥',r'\ge':'≥',r'\neq':'≠',r'\approx':'≈',
 r'\equiv':'≡',r'\to':'→',r'\rightarrow':'→',r'\Rightarrow':'⇒',r'\in':'∈',
 r'\ldots':'…',r'\cdots':'⋯',r'\hbar':'ℏ',r'\ast':'∗',
}
FUNC = {r'\exp':'exp',r'\log':'log',r'\ln':'ln',r'\sin':'sin',r'\cos':'cos',r'\tan':'tan'}
SPACE = {r'\,':' ',r'\;':' ',r'\:':' ',r'\!':'',r'\quad':'  ',r'\qquad':'    ',r'\\':' '}

def esc(s): return html.escape(s, quote=False)
def mrun(t):
    return '<m:r><m:t xml:space="preserve">%s</m:t></m:r>' % esc(t) if t != '' else ''

TOKEN = re.compile(r"\\left|\\right|\\[A-Za-z]+|\\[^A-Za-z]|[{}^_]|[^\\{}^_]")

def tokenize(s): return TOKEN.findall(s)

def mapdelim(tok):
    d = {'(':'(',')':')','[':'[',']':']','\\{':'{','\\}':'}','|':'|','.':''}
    return d.get(tok, tok if tok in '()[]|' else '')

class P:
    def __init__(self, toks): self.t = toks; self.i = 0
    def peek(self): return self.t[self.i] if self.i < len(self.t) else None
    def nxt(self):
        tok = self.peek(); self.i += 1; return tok

def script(base, sub, sup):
    if sub is not None and sup is not None:
        return ('<m:sSubSup><m:e>%s</m:e><m:sub>%s</m:sub><m:sup>%s</m:sup></m:sSubSup>'
                % (base, sub, sup))
    if sup is not None:
        return '<m:sSup><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>' % (base, sup)
    if sub is not None:
        return '<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>' % (base, sub)
    return base

def frac(n, d):
    return '<m:f><m:num>%s</m:num><m:den>%s</m:den></m:f>' % (n, d)
def sqrt(e):
    return '<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>%s</m:e></m:rad>' % e
def bar(e):
    return '<m:bar><m:barPr><m:pos m:val="top"/></m:barPr><m:e>%s</m:e></m:bar>' % e
def acc(e, ch='&#770;'):
    return '<m:acc><m:accPr><m:chr m:val="%s"/></m:accPr><m:e>%s</m:e></m:acc>' % (ch, e)
def delim(inner, b, e):
    return ('<m:d><m:dPr><m:begChr m:val="%s"/><m:endChr m:val="%s"/></m:dPr>'
            '<m:e>%s</m:e></m:d>' % (esc(b), esc(e), inner))
def nary(ch, sub, sup, limloc):
    subhide = '0' if sub else '1'; suphide = '0' if sup else '1'
    return ('<m:nary><m:naryPr><m:chr m:val="%s"/><m:limLoc m:val="%s"/>'
            '<m:subHide m:val="%s"/><m:supHide m:val="%s"/></m:naryPr>'
            '<m:sub>%s</m:sub><m:sup>%s</m:sup><m:e></m:e></m:nary>'
            % (ch, limloc, subhide, suphide, sub or '', sup or ''))

def parse_atom(p):
    """Return OMML for a single argument/atom."""
    tok = p.peek()
    if tok == '{':
        p.nxt(); inner = parse_seq(p, stop='}')
        if p.peek() == '}': p.nxt()
        return inner
    if tok in (r'\frac', r'\tfrac', r'\dfrac'):
        p.nxt(); return frac(parse_atom(p), parse_atom(p))
    if tok == r'\sqrt':
        p.nxt(); return sqrt(parse_atom(p))
    if tok == r'\overline':
        p.nxt(); return bar(parse_atom(p))
    if tok == r'\hat':
        p.nxt(); return acc(parse_atom(p))
    if tok is not None and tok.startswith('\\'):
        p.nxt()
        if tok in SYM: return mrun(SYM[tok])
        if tok in FUNC: return mrun(FUNC[tok])
        if tok in SPACE: return mrun(SPACE[tok])
        return mrun(tok[1:])
    if tok is None: return ''
    p.nxt(); return mrun(tok)

def parse_seq(p, stop=None):
    elems = []; buf = ''
    def flush():
        nonlocal buf
        if buf != '': elems.append(mrun(buf)); buf = ''
    while True:
        tok = p.peek()
        if tok is None: break
        if stop is not None and tok == stop: break
        if tok in ('^', '_'):
            flush()
            base = elems.pop() if elems else mrun('')
            sub = sup = None
            while p.peek() in ('^', '_'):
                s = p.nxt(); arg = parse_atom(p)
                if s == '^': sup = arg
                else: sub = arg
            elems.append(script(base, sub, sup)); continue
        if tok == '{':
            p.nxt(); inner = parse_seq(p, stop='}')
            if p.peek() == '}': p.nxt()
            flush(); elems.append(inner); continue
        if tok in (r'\frac', r'\tfrac', r'\dfrac'):
            p.nxt(); flush(); elems.append(frac(parse_atom(p), parse_atom(p))); continue
        if tok == r'\sqrt':
            p.nxt(); flush(); elems.append(sqrt(parse_atom(p))); continue
        if tok == r'\overline':
            p.nxt(); flush(); elems.append(bar(parse_atom(p))); continue
        if tok == r'\hat':
            p.nxt(); flush(); elems.append(acc(parse_atom(p))); continue
        if tok == r'\left':
            p.nxt(); dopen = p.nxt(); inner = parse_seq(p, stop=r'\right')
            if p.peek() == r'\right': p.nxt(); dclose = p.nxt()
            else: dclose = ')'
            flush(); elems.append(delim(inner, mapdelim(dopen), mapdelim(dclose))); continue
        if tok in (r'\int', r'\oint', r'\sum', r'\prod'):
            p.nxt(); flush()
            sub = sup = None
            while p.peek() in ('^', '_'):
                s = p.nxt(); arg = parse_atom(p)
                if s == '^': sup = arg
                else: sub = arg
            ch = {'\\int':'∫','\\oint':'∮','\\sum':'∑','\\prod':'∏'}[tok]
            limloc = 'subSup' if tok in (r'\int', r'\oint') else 'undOvr'
            elems.append(nary(ch, sub, sup, limloc)); continue
        if tok.startswith('\\'):
            p.nxt()
            if tok in SYM: buf += SYM[tok]
            elif tok in FUNC: buf += FUNC[tok]
            elif tok in SPACE: buf += SPACE[tok]
            else: buf += tok[1:]
            continue
        # ordinary char
        p.nxt(); buf += tok
    flush()
    return ''.join(elems)

def conv(latex):
    latex = latex.strip().rstrip(',').rstrip('.')
    return parse_seq(P(tokenize(latex)))

def cases_omml(body):
    rows = re.split(r'\\\\', body)
    row_xml = []
    for r in rows:
        if r.strip() == '': continue
        cells = r.split('&')
        cell_xml = conv(cells[0])
        if len(cells) > 1:
            cell_xml += '<m:r><m:t xml:space="preserve">   </m:t></m:r>' + conv(cells[1])
        row_xml.append('<m:e>%s</m:e>' % cell_xml)
    arr = '<m:eqArr>%s</m:eqArr>' % ''.join(row_xml)
    return ('<m:d><m:dPr><m:begChr m:val="{"/><m:endChr m:val=""/>'
            '<m:grow m:val="1"/></m:dPr><m:e>%s</m:e></m:d>' % arr)

def latex_to_omml(latex):
    m = re.search(r'(.*?)\\begin\{cases\}(.*?)\\end\{cases\}(.*)', latex, re.DOTALL)
    if m:
        pre, body, post = m.group(1), m.group(2), m.group(3)
        return conv(pre) + cases_omml(body) + conv(post)
    return conv(latex)

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

def build(eqs):
    body = []
    body.append('<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
                '<w:r><w:rPr><w:b/><w:sz w:val="30"/></w:rPr>'
                '<w:t>Equations (native Word equation objects)</w:t></w:r></w:p>')
    body.append('<w:p><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="555555"/></w:rPr>'
                '<w:t xml:space="preserve">Manuscript: Irreversibility Analysis of a Radiative '
                'Casson Hybrid Nanofluid Between Squeezing Porous Plates. Each equation below is a '
                'live Word equation (Insert &gt; Equation) with book-style fractions, powers and radicals.'
                '</w:t></w:r></w:p>')
    for n, l in eqs:
        omml = latex_to_omml(l)
        # equation left, number right (right tab stop)
        para = ('<w:p><w:pPr><w:tabs><w:tab w:val="right" w:pos="9360"/></w:tabs>'
                '<w:spacing w:before="80" w:after="80"/></w:pPr>'
                '<m:oMath>%s</m:oMath>'
                '<w:r><w:tab/><w:t>(%d)</w:t></w:r></w:p>' % (omml, n))
        body.append(para)
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<w:body>' + ''.join(body) +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:bottom="1440" w:left="1440" w:right="1440"/></w:sectPr>'
        '</w:body></w:document>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:docDefaults><w:rPrDefault><w:rPr>'
              '<w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
              '<w:sz w:val="24"/></w:rPr></w:rPrDefault></w:docDefaults></w:styles>')
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
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct)
        z.writestr('_rels/.rels', rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', styles)
        z.writestr('word/_rels/document.xml.rels', drels)

if __name__ == '__main__':
    eqs = extract()
    build(eqs)
    print('Wrote', OUT, 'with', len(eqs), 'native equations (tags', eqs[0][0], '..', eqs[-1][0], ')')
