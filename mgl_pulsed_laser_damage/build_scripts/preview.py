import zipfile, xml.dom.minidom as md, subprocess
from plot import CHROME
d=md.parseString(zipfile.ZipFile('/projects/sandbox/MGL_pulsed_laser_damage_optimization_paper.docx').read('word/document.xml'))
def kids(n,tag=None): return [c for c in n.childNodes if c.nodeType==1 and (tag is None or c.tagName==tag)]
def one(n,tag):
    k=kids(n,tag); return k[0] if k else None
def row(n): return '<mrow>'+''.join(conv(c) for c in kids(n))+'</mrow>' if n is not None else '<mrow/>'
def conv(n):
    t=n.tagName
    if t=='m:r':
        tx=''.join(x.firstChild.data if x.firstChild else '' for x in kids(n,'m:t'))
        plain=one(n,'m:rPr') is not None
        return '<mi mathvariant="%s">%s</mi>'%('normal' if plain else 'italic',tx.replace('&','&amp;').replace('<','&lt;'))
    if t=='m:f': return '<mfrac>%s%s</mfrac>'%(row(one(n,'m:num')),row(one(n,'m:den')))
    if t=='m:sSup': return '<msup>%s%s</msup>'%(row(one(n,'m:e')),row(one(n,'m:sup')))
    if t=='m:sSub': return '<msub>%s%s</msub>'%(row(one(n,'m:e')),row(one(n,'m:sub')))
    if t=='m:sSubSup': return '<msubsup>%s%s%s</msubsup>'%(row(one(n,'m:e')),row(one(n,'m:sub')),row(one(n,'m:sup')))
    if t=='m:rad': return '<msqrt>%s</msqrt>'%row(one(n,'m:e'))
    if t=='m:acc': return '<mover>%s<mo>‾</mo></mover>'%row(one(n,'m:e'))
    if t=='m:d':
        pr=one(n,'m:dPr'); b=one(pr,'m:begChr').getAttribute('m:val'); e=one(pr,'m:endChr').getAttribute('m:val')
        return '<mrow><mo>%s</mo>%s<mo>%s</mo></mrow>'%(b,row(one(n,'m:e')),e)
    if t=='m:nary':
        pr=one(n,'m:naryPr'); ch=one(pr,'m:chr'); c=ch.getAttribute('m:val') if ch else '∫'
        return '<mrow><munderover><mo>%s</mo>%s%s</munderover>%s</mrow>'%(c,row(one(n,'m:sub')),row(one(n,'m:sup')),row(one(n,'m:e')))
    if t in ('m:oMath','m:e'): return row(n)
    return ''
html=['<html><body style="font-family:serif;font-size:18px;width:1100px">']
for p in d.getElementsByTagName('w:p'):
    st=p.getElementsByTagName('w:pStyle')
    if st and st[0].getAttribute('w:val')=='Equation':
        m=p.getElementsByTagName('m:oMath')[0]
        num=p.getElementsByTagName('w:t')[-1].firstChild.data
        html.append('<div style="display:flex;justify-content:space-between;margin:6px"><math display="block">%s</math><span>%s</span></div>'%(conv(m),num))
html.append('</body></html>')
open('preview.html','w').write(''.join(html))
subprocess.run([CHROME,'--no-sandbox','--hide-scrollbars','--screenshot=/projects/sandbox/mgl_damage_build/preview.png','--window-size=1150,7000','file:///projects/sandbox/mgl_damage_build/preview.html'],capture_output=True)
