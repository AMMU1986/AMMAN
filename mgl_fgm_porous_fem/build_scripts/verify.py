import zipfile, re, xml.dom.minidom as md
from xml.etree import ElementTree as ET
P='/projects/sandbox/MGL_FGM_porous_FEM_line_source_paper.docx'
z=zipfile.ZipFile(P); print(z.testzip())
for n in z.namelist():
    if n.endswith('.xml') or n.endswith('.rels'): ET.fromstring(z.read(n))
d=z.read('word/document.xml').decode()
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
root=ET.fromstring(d)
paras=list(root.iter(W+'p'))
def text(p): return ''.join(t.text or '' for t in p.iter(W+'t'))
eqs=[];figs=[];tabs=[]
for p in paras:
    st=p.find(W+'pPr/'+W+'pStyle')
    s=st.get(W+'val') if st is not None else ''
    if s=='Equation':
        has=len(list(p.iter('{http://schemas.openxmlformats.org/officeDocument/2006/math}oMath')))
        tabsx=[t.get(W+'val') for t in p.iter(W+'tab') if t.get(W+'val')]
        eqs.append((text(p).strip(),has,tabsx))
    if s=='Caption':
        t=text(p)
        if t.startswith('Figure'): figs.append(t[:12])
        if t.startswith('Table'): tabs.append(t[:9])
nums=[int(re.search(r'\((\d+)\)$',e[0]).group(1)) for e in eqs]
print('equations',len(eqs),nums==list(range(1,57)),all(e[1]==1 for e in eqs),set(tuple(e[2]) for e in eqs))
print('figures',len(figs),figs[-1],'tables',len(tabs),tabs[-1],'real tables',d.count('<w:tbl>'),'images',len(re.findall('<pic:pic>',d)))
body=[text(p) for p in paras if (p.find(W+'pPr/'+W+'pStyle') is not None and p.find(W+'pPr/'+W+'pStyle').get(W+'val') in('BodyText','Abstract'))]
# BodyText includes the note; exclude 'NOTE'
body=[b for b in body if not b.startswith('NOTE') and not b.startswith('Keywords')]
print('body words (BodyText+Abstract paragraphs)',sum(len(b.split()) for b in body))
print('em dashes',d.count('—'), 'refs',len([p for p in paras if p.find(W+'pPr/'+W+'pStyle') is not None and p.find(W+'pPr/'+W+'pStyle').get(W+'val')=='Reference']))
print('highlight',d.count('w:highlight'))
print('unreplaced %s' , len(re.findall(r'%s|%d|\{[a-z]+\}',' '.join(text(p) for p in paras))))
