#!/usr/bin/env python3
"""
Build a self-contained Word .docx of the ORIGINAL TCS misuse REVIEW paper
(/projects/sandbox/TCS_misuse_paper.md) with its 3 figures embedded
(SVG primary + data-driven PNG fallback). Standard library only.
"""
import zipfile, os, re, html, zlib, struct, shutil

ROOT = "/projects/sandbox"
SRC  = os.path.join(ROOT, "TCS_misuse_paper.md")
FIGDIR = os.path.join(ROOT, "figures")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "TCS_Misuse_Review_Paper.docx")

# ---- figure data (mirrors make_figures.py) for PNG fallbacks ----
FIGDATA = {
    "fig1_adverse_effects.svg": ("hbar", [51,49,44,30,27,15,12,10], 60, (44,110,145)),
    "fig2_market.svg": ("vbar", [[60,87,70]], 100, [(192,80,77)]),
    "fig3_cost.svg": ("vbar", [[1.6,0.3,3.1,100],[3.4,1.4,8.7,240]], 276, [(155,187,89),(192,80,77)]),
}

# ------------------------------------------------------------------ PNG
def write_png(path, pix, w, h):
    raw = bytearray()
    for y in range(h):
        raw.append(0); row = pix[y]
        for x in range(w):
            r,g,b = row[x]; raw += bytes((r,g,b))
    comp = zlib.compress(bytes(raw), 9)
    def ch(t,d): c=t+d; return struct.pack(">I",len(d))+c+struct.pack(">I",zlib.crc32(c)&0xffffffff)
    with open(path,"wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,2,0,0,0)))
        f.write(ch(b"IDAT",comp)); f.write(ch(b"IEND",b""))

def canvas(w,h,bg=(255,255,255)): return [[list(bg) for _ in range(w)] for _ in range(h)]
def rect(px,x0,y0,x1,y1,col,W,H):
    x0=max(0,int(x0));y0=max(0,int(y0));x1=min(W,int(x1));y1=min(H,int(y1))
    for y in range(y0,y1):
        row=px[y]
        for x in range(x0,x1): row[x]=list(col)

def render_png(name, path):
    kind,data,vmax,col = FIGDATA[name]
    if kind=="hbar":
        W,H=760,60+len(data)*40+40; px=canvas(W,H); pl=260; pw=W-pl-70; top=60
        for i,v in enumerate(data):
            y=top+i*40+6; bw=pw*v/vmax; rect(px,pl,y,pl+bw,y+24,col,W,H)
        rect(px,pl,top,pl+2,H-40,(60,60,60),W,H)
    else:  # vbar grouped
        W,H=720,440; px=canvas(W,H); pl=70; top=70; pb=90; ph=H-top-pb; pw=W-pl-30
        ng=len(data[0]); ns=len(data); gw=pw/ng; bw=gw*0.7/ns
        for gi in range(ng):
            gx0=pl+gi*gw+gw*0.15
            for si in range(ns):
                v=data[si][gi]; bh=ph*v/vmax; bx=gx0+si*bw; by=top+ph-bh
                rect(px,bx,by,bx+bw-4,top+ph,col[si],W,H)
        rect(px,pl,top+ph,W-30,top+ph+2,(60,60,60),W,H)
    write_png(path,px,W,H); return W,H

# ------------------------------------------------------------------ md -> wml helpers
def esc(t): return html.escape(t, quote=False)
def runs(text):
    out=[]; pat=re.compile(r'(\*\*.+?\*\*|\*.+?\*)'); pos=0
    for m in pat.finditer(text):
        if m.start()>pos: out.append(("",text[pos:m.start()]))
        tok=m.group(0); out.append(("b",tok[2:-2]) if tok.startswith("**") else ("i",tok[1:-1])); pos=m.end()
    if pos<len(text): out.append(("",text[pos:]))
    xml=""
    for st,ch in out:
        rpr="<w:rPr><w:b/></w:rPr>" if st=="b" else ("<w:rPr><w:i/></w:rPr>" if st=="i" else "")
        xml+=f'<w:r>{rpr}<w:t xml:space="preserve">{esc(ch)}</w:t></w:r>'
    return xml or '<w:r><w:t/></w:r>'
def para(text,size=None,bold=False,color=None,align=None,before=120,after=120):
    ppr=f'<w:pPr><w:spacing w:before="{before}" w:after="{after}"/>'+(f'<w:jc w:val="{align}"/>' if align else "")+"</w:pPr>"
    if bold or size or color:
        rpr="<w:rPr>"+("<w:b/>" if bold else "")+(f'<w:sz w:val="{size*2}"/><w:szCs w:val="{size*2}"/>' if size else "")+(f'<w:color w:val="{color}"/>' if color else "")+"</w:rPr>"
        r=f'<w:r>{rpr}<w:t xml:space="preserve">{esc(re.sub(r"[*]","",text))}</w:t></w:r>'
    else: r=runs(text)
    return f"<w:p>{ppr}{r}</w:p>"
def heading(text,level):
    sizes={1:20,2:15,3:13}
    return para(text,bold=True,size=sizes.get(level,12),color="1F3864" if level<=2 else "2E5496",before=240 if level==1 else 200,after=120)
def table(rows):
    borders='<w:tblBorders>'+''.join(f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="999999"/>' for e in ["top","left","bottom","right","insideH","insideV"])+'</w:tblBorders>'
    xml=f'<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/>{borders}<w:tblLook w:val="04A0"/></w:tblPr>'
    for i,row in enumerate(rows):
        xml+="<w:tr>"
        for cell in row:
            shd='<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if i==0 else ""
            xml+=f'<w:tc><w:tcPr>{shd}</w:tcPr><w:p><w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>{runs(("**"+cell+"**") if i==0 else cell)}</w:p></w:tc>'
        xml+="</w:tr>"
    return xml+"</w:tbl><w:p/>"
def image_para(pid,W,H,rid_png,rid_svg):
    disp_w=min(6.0,W/96.0); scale=disp_w/(W/96.0)
    cx=int(disp_w*914400); cy=int((H/96.0)*scale*914400)
    return (f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="120"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="{pid}" name="Figure{pid}"/><wp:cNvGraphicFramePr/>'
            f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{pid}" name="Figure{pid}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid_png}"><a:extLst><a:ext uri="{{96DAC541-7B7A-43D3-8B79-37D633B846F1}}">'
            f'<asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" r:embed="{rid_svg}"/>'
            f'</a:ext></a:extLst></a:blip><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
            f'</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')

def build():
    # render png fallbacks
    dims={}
    for name in FIGDATA:
        png=os.path.join(FIGDIR,name.replace(".svg",".png")); dims[name]=render_png(name,png)
    md=open(SRC,encoding="utf-8").read(); lines=md.split("\n")
    body=[]; rels=[]; ct=set(); imgparts=[]; i=0; pid=1; rid=1
    img_re=re.compile(r'^!\[[^\]]*\]\(([^)]+\.svg)\)\s*$')
    while i<len(lines):
        line=lines[i].rstrip()
        if not line.strip(): i+=1; continue
        mi=img_re.match(line.strip())
        if mi:
            name=os.path.basename(mi.group(1))
            if name in dims:
                W,H=dims[name]; rid_png=f"rId{rid}"; rid_svg=f"rId{rid+1}"; rid+=2
                pm=f"image{pid}.png"; sm=f"image{pid}.svg"
                imgparts.append((os.path.join(FIGDIR,name.replace('.svg','.png')),"word/media/"+pm))
                imgparts.append((os.path.join(FIGDIR,name),"word/media/"+sm))
                rels.append((rid_png,"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image","media/"+pm))
                rels.append((rid_svg,"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image","media/"+sm))
                ct.add(("png","image/png")); ct.add(("svg","image/svg+xml"))
                body.append(image_para(pid,W,H,rid_png,rid_svg)); pid+=1
            i+=1; continue
        if line.lstrip().startswith("|") and i+1<len(lines) and re.match(r'^\s*\|?[\s:|-]+\|?\s*$',lines[i+1]):
            tbl=[]
            while i<len(lines) and lines[i].lstrip().startswith("|"):
                if re.match(r'^\s*\|?[\s:|-]+\|?\s*$',lines[i]): i+=1; continue
                tbl.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i+=1
            body.append(table(tbl)); continue
        if line.startswith("### "): body.append(heading(line[4:],3))
        elif line.startswith("## "): body.append(heading(line[3:],2))
        elif line.startswith("# "): body.append(heading(line[2:],1))
        elif line.strip() in ("---","***","___"):
            body.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="999999"/></w:pBdr></w:pPr></w:p>')
        elif line.startswith(">"): body.append(para(line.lstrip("> ").strip(),color="555555",before=80,after=80))
        elif re.match(r'^\s*[-*] ',line): body.append(para("\u2022 "+re.sub(r'^\s*[-*] ','',line),before=40,after=40))
        elif re.match(r'^\s*\d+\. ',line): body.append(para(re.sub(r'^\s*(\d+)\. ',r'\1. ',line),before=40,after=40))
        else: body.append(para(line))
        i+=1
    document=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<w:body>{"".join(body)}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
        '</w:sectPr></w:body></w:document>')
    ctypes=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        + "".join(f'<Default Extension="{e}" ContentType="{c}"/>' for e,c in sorted(ct)) +
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
    pkg=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
    drels=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(f'<Relationship Id="{i}" Type="{t}" Target="{tg}"/>' for i,t,tg in rels) + '</Relationships>')
    with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",ctypes); z.writestr("_rels/.rels",pkg)
        z.writestr("word/document.xml",document); z.writestr("word/_rels/document.xml.rels",drels)
        for s,a in imgparts: z.write(s,a)
    print("Wrote",OUT,f"({os.path.getsize(OUT)} bytes) | figures embedded:",pid-1)

if __name__=="__main__":
    build()
