#!/usr/bin/env python3
"""
Build a self-contained Word .docx of the stroke article WITH figures embedded.
Each figure is inserted as a modern-Office SVG image (crisp vector) plus a
data-driven PNG fallback (for older viewers). Standard library only.
"""
import zipfile, os, re, html, json, zlib, struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "Sex_Differences_Stroke_Research_Article.md")
OUT  = os.path.join(HERE, "Sex_Differences_Stroke_Research_Article.docx")
R    = json.load(open(os.path.join(HERE, "stroke_results.json")))
BAND = [(46,125,50),(155,187,89),(240,173,78),(224,123,57),(176,65,62)]

# ------------------------------------------------------------------ PNG
def write_png(path, pix, w, h):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        row = pix[y]
        for x in range(w):
            r,g,b = row[x]; raw += bytes((r,g,b))
    comp = zlib.compress(bytes(raw), 9)
    def chunk(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)))
        f.write(chunk(b"IDAT", comp))
        f.write(chunk(b"IEND", b""))

def canvas(w, h, bg=(255,255,255)):
    return [[list(bg) for _ in range(w)] for _ in range(h)]

def rect(px, x0, y0, x1, y1, col, W, H):
    x0=max(0,int(x0)); y0=max(0,int(y0)); x1=min(W,int(x1)); y1=min(H,int(y1))
    for y in range(y0, y1):
        row = px[y]
        for x in range(x0, x1):
            row[x] = list(col)

# ------------------------------------------------------------------ figure PNGs (data-driven, no text)
def png_fig1(path):
    W,H=760,300; px=canvas(W,H); pl=90; top=70; barh=52; gap=52; pw=W-pl-30
    for bi,dist in enumerate([R["mrs_dist"]["women"], R["mrs_dist"]["men"]]):
        y=top+bi*(barh+gap); x=pl
        for i,val in enumerate(dist):
            seg=pw*val/100.0; rect(px,x,y,x+seg,y+barh,BAND[i],W,H); x+=seg
        rect(px,pl,y,pl+2,y+barh,(80,80,80),W,H)
    write_png(path,px,W,H); return W,H

def png_fig2(path):
    import math
    rows=[r for r in R["logit"] if r["var"]!="Intercept"]
    W=760; row_h=46; top=60; H=top+len(rows)*row_h+40; pl=230; pr=110; pw=W-pl-pr
    lo=min(r["aOR_lo"] for r in rows); hi=max(r["aOR_hi"] for r in rows)
    xmin,xmax=math.log(min(lo,0.55)*0.9),math.log(hi*1.1)
    def X(v): return pl+pw*(math.log(v)-xmin)/(xmax-xmin)
    px=canvas(W,H)
    x1=X(1.0); rect(px,x1,top-6,x1+2,top+len(rows)*row_h,(120,120,120),W,H)
    for i,r in enumerate(rows):
        y=top+i*row_h+row_h//2
        xlo,xhi,xor=X(r["aOR_lo"]),X(r["aOR_hi"]),X(r["aOR"])
        col=(192,80,77) if r["var"]=="Female sex" else (44,62,80)
        rect(px,xlo,y-1,xhi,y+1,(127,140,141),W,H)
        rect(px,xlo,y-6,xlo+2,y+6,(127,140,141),W,H); rect(px,xhi-2,y-6,xhi,y+6,(127,140,141),W,H)
        rect(px,xor-6,y-6,xor+6,y+6,col,W,H)
    write_png(path,px,W,H); return W,H

def png_fig3(path):
    W,H=720,380; px=canvas(W,H); pl=70; top=50; pb=70; ph=H-top-pb; pw=W-pl-30
    pg=R["primary_good"]; sec=R["secondary"]; vmax=70
    women=[pg["women_pct"],sec["death"]["women_pct"],sec["home"]["women_pct"]]
    men=[pg["men_pct"],sec["death"]["men_pct"],sec["home"]["men_pct"]]
    series=[(women,(192,80,77)),(men,(79,129,189))]; ng=3; gw=pw/ng; bw=gw*0.7/2
    for gi in range(ng):
        gx0=pl+gi*gw+gw*0.15
        for si,(vals,col) in enumerate(series):
            v=vals[gi]; bh=ph*v/vmax; bx=gx0+si*bw; by=top+ph-bh
            rect(px,bx,by,bx+bw-4,top+ph,col,W,H)
    rect(px,pl,top+ph,W-30,top+ph+2,(80,80,80),W,H)
    write_png(path,px,W,H); return W,H

# ------------------------------------------------------------------ markdown -> wml (reused helpers)
def esc(t): return html.escape(t, quote=False)
def runs(text):
    out=[]; pat=re.compile(r'(\*\*.+?\*\*|\*.+?\*)'); pos=0
    for m in pat.finditer(text):
        if m.start()>pos: out.append(("",text[pos:m.start()]))
        tok=m.group(0)
        out.append(("b",tok[2:-2]) if tok.startswith("**") else ("i",tok[1:-1]))
        pos=m.end()
    if pos<len(text): out.append(("",text[pos:]))
    xml=""
    for st,ch in out:
        rpr="<w:rPr><w:b/></w:rPr>" if st=="b" else ("<w:rPr><w:i/></w:rPr>" if st=="i" else "")
        xml+=f'<w:r>{rpr}<w:t xml:space="preserve">{esc(ch)}</w:t></w:r>'
    return xml or '<w:r><w:t/></w:r>'
def para(text, size=None, bold=False, color=None, align=None, before=120, after=120):
    ppr=f'<w:pPr><w:spacing w:before="{before}" w:after="{after}"/>'+(f'<w:jc w:val="{align}"/>' if align else "")+"</w:pPr>"
    if bold or size or color:
        rpr="<w:rPr>"+("<w:b/>" if bold else "")+(f'<w:sz w:val="{size*2}"/><w:szCs w:val="{size*2}"/>' if size else "")+(f'<w:color w:val="{color}"/>' if color else "")+"</w:rPr>"
        r=f'<w:r>{rpr}<w:t xml:space="preserve">{esc(re.sub(r"[*]","",text))}</w:t></w:r>'
    else:
        r=runs(text)
    return f"<w:p>{ppr}{r}</w:p>"
def heading(text, level):
    sizes={1:20,2:15,3:13}
    return para(text,bold=True,size=sizes.get(level,12),color="1F3864" if level<=2 else "2E5496",
                before=240 if level==1 else 200, after=120)
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

def image_para(pid, W, H, rid_png, rid_svg):
    disp_w_in=min(6.0, W/96.0); scale=disp_w_in/(W/96.0)
    cx=int(disp_w_in*914400); cy=int((H/96.0)*scale*914400)
    return (f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="60"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
            f'<wp:docPr id="{pid}" name="Figure{pid}"/><wp:cNvGraphicFramePr/>'
            f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{pid}" name="Figure{pid}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid_png}">'
            f'<a:extLst><a:ext uri="{{96DAC541-7B7A-43D3-8B79-37D633B846F1}}">'
            f'<asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" r:embed="{rid_svg}"/>'
            f'</a:ext></a:extLst></a:blip><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
            f'</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')

def build():
    # render PNG fallbacks
    media=[]  # (svg_abs, png_abs, W, H)
    figmap={
        "fig1_mrs.svg": png_fig1,
        "fig2_forest.svg": png_fig2,
        "fig3_outcomes.svg": png_fig3,
    }
    dims={}
    for name,fn in figmap.items():
        png_path=os.path.join(HERE,"stroke_figures",name.replace(".svg",".png"))
        W,H=fn(png_path); dims[name]=(W,H)

    md=open(SRC,encoding="utf-8").read()
    lines=md.split("\n")
    body=[]; rels=[]; ct_defaults=set(); imgparts=[]; i=0; pid=1; rid=1
    fig_re=re.compile(r'^\*Figure\s*\d+\s*[—-].*`([^`]+\.svg)`.*\*$')
    while i<len(lines):
        line=lines[i].rstrip()
        if not line.strip(): i+=1; continue
        mfig=fig_re.match(line.strip())
        if mfig:
            svgrel=mfig.group(1); name=os.path.basename(svgrel)
            body.append(para(line.strip(), color="555555", align="center", before=40, after=40))
            if name in dims:
                W,H=dims[name]
                rid_png=f"rId{rid}"; rid_svg=f"rId{rid+1}"; rid+=2
                pngmedia=f"image{pid}.png"; svgmedia=f"image{pid}.svg"
                imgparts.append((os.path.join(HERE,"stroke_figures",name.replace('.svg','.png')),"word/media/"+pngmedia))
                imgparts.append((os.path.join(HERE,"stroke_figures",name),"word/media/"+svgmedia))
                rels.append((rid_png,"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image","media/"+pngmedia))
                rels.append((rid_svg,"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image","media/"+svgmedia))
                ct_defaults.add(("png","image/png")); ct_defaults.add(("svg","image/svg+xml"))
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
        f'<w:body>{"".join(body)}'
        '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
        '</w:sectPr></w:body></w:document>')
    ct=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        + "".join(f'<Default Extension="{e}" ContentType="{c}"/>' for e,c in sorted(ct_defaults)) +
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '</Types>')
    pkg_rels=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')
    doc_rels=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(f'<Relationship Id="{i}" Type="{t}" Target="{tg}"/>' for i,t,tg in rels) +
        '</Relationships>')
    with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",ct)
        z.writestr("_rels/.rels",pkg_rels)
        z.writestr("word/document.xml",document)
        z.writestr("word/_rels/document.xml.rels",doc_rels)
        for srcp,arc in imgparts:
            z.write(srcp,arc)
    print("Wrote",OUT,f"({os.path.getsize(OUT)} bytes)")
    print("Embedded figures:",pid-1,"| media parts:",len(imgparts))

if __name__=="__main__":
    build()
