#!/usr/bin/env python3
"""
COMPLETE MANUSCRIPT GENERATOR
Chapter: "Accreditation as Accountability, Learning, and Institutional Renewal"
Book: Higher Education Beyond Boundaries: Dynamics, Change, Challenges and Opportunities

Generates a single .docx file with:
- Full 7000+ word text
- 3 Tables (one per section)
- 3 Figures (one per section)
- 52 numbered references in strict serial order
- Times New Roman 12pt, double-spaced
- APA 7th Edition style

Uses only Python standard library (zipfile, xml, struct, zlib, math).
"""

import zipfile
import os
import struct
import zlib
import math
from xml.etree.ElementTree import Element, SubElement, tostring

# ===========================================================================
# SECTION A: PNG FIGURE GENERATION (Pure Python)
# ===========================================================================

def create_png(width, height, pixels):
    """Create PNG from pixel data: list of rows, each row = list of (R,G,B)."""
    def chunk(ctype, data):
        c = ctype + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    raw = b''
    for row in pixels:
        raw += b'\x00'
        for r, g, b in row:
            raw += struct.pack('BBB', r, g, b)
    idat = chunk(b'IDAT', zlib.compress(raw))
    iend = chunk(b'IEND', b'')
    return sig + ihdr + idat + iend

def draw_filled_rect(px, x1, y1, x2, y2, color):
    H, W = len(px), len(px[0])
    for y in range(max(0,y1), min(H,y2)):
        for x in range(max(0,x1), min(W,x2)):
            px[y][x] = color

def draw_rect_border(px, x1, y1, x2, y2, color, t=2):
    H, W = len(px), len(px[0])
    for i in range(t):
        for x in range(max(0,x1), min(W,x2)):
            if 0 <= y1+i < H: px[y1+i][x] = color
            if 0 <= y2-1-i < H: px[y2-1-i][x] = color
        for y in range(max(0,y1), min(H,y2)):
            if 0 <= x1+i < W: px[y][x1+i] = color
            if 0 <= x2-1-i < W: px[y][x2-1-i] = color

def draw_line(px, x1, y1, x2, y2, color, t=2):
    dx, dy = abs(x2-x1), abs(y2-y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    H, W = len(px), len(px[0])
    while True:
        for i in range(-t//2, t//2+1):
            if dx > dy:
                py = y1+i
                if 0<=py<H and 0<=x1<W: px[py][x1] = color
            else:
                pxx = x1+i
                if 0<=y1<H and 0<=pxx<W: px[y1][pxx] = color
        if x1==x2 and y1==y2: break
        e2 = 2*err
        if e2 > -dy: err -= dy; x1 += sx
        if e2 < dx: err += dx; y1 += sy

def draw_arrow(px, x1, y1, x2, y2, color, t=2):
    draw_line(px, x1, y1, x2, y2, color, t)
    angle = math.atan2(y2-y1, x2-x1)
    for a in [angle+2.5, angle-2.5]:
        ax, ay = int(x2+12*math.cos(a)), int(y2+12*math.sin(a))
        draw_line(px, x2, y2, ax, ay, color, t)

def draw_filled_circle(px, cx, cy, r, color):
    H, W = len(px), len(px[0])
    for y in range(cy-r, cy+r+1):
        for x in range(cx-r, cx+r+1):
            if (x-cx)**2+(y-cy)**2 <= r**2:
                if 0<=y<H and 0<=x<W: px[y][x] = color

def draw_circle(px, cx, cy, r, color, t=2):
    H, W = len(px), len(px[0])
    for deg in range(360):
        a = math.radians(deg)
        for i in range(t):
            x = int(cx+(r-i)*math.cos(a))
            y = int(cy+(r-i)*math.sin(a))
            if 0<=y<H and 0<=x<W: px[y][x] = color

# Bitmap font 5x7
FONT = {
    'A':['01110','10001','10001','11111','10001','10001','10001'],
    'B':['11110','10001','10001','11110','10001','10001','11110'],
    'C':['01110','10001','10000','10000','10000','10001','01110'],
    'D':['11110','10001','10001','10001','10001','10001','11110'],
    'E':['11111','10000','10000','11110','10000','10000','11111'],
    'F':['11111','10000','10000','11110','10000','10000','10000'],
    'G':['01110','10001','10000','10111','10001','10001','01110'],
    'H':['10001','10001','10001','11111','10001','10001','10001'],
    'I':['01110','00100','00100','00100','00100','00100','01110'],
    'J':['00111','00010','00010','00010','00010','10010','01100'],
    'K':['10001','10010','10100','11000','10100','10010','10001'],
    'L':['10000','10000','10000','10000','10000','10000','11111'],
    'M':['10001','11011','10101','10101','10001','10001','10001'],
    'N':['10001','11001','10101','10011','10001','10001','10001'],
    'O':['01110','10001','10001','10001','10001','10001','01110'],
    'P':['11110','10001','10001','11110','10000','10000','10000'],
    'Q':['01110','10001','10001','10001','10101','10010','01101'],
    'R':['11110','10001','10001','11110','10100','10010','10001'],
    'S':['01110','10001','10000','01110','00001','10001','01110'],
    'T':['11111','00100','00100','00100','00100','00100','00100'],
    'U':['10001','10001','10001','10001','10001','10001','01110'],
    'V':['10001','10001','10001','10001','01010','01010','00100'],
    'W':['10001','10001','10001','10101','10101','10101','01010'],
    'X':['10001','10001','01010','00100','01010','10001','10001'],
    'Y':['10001','10001','01010','00100','00100','00100','00100'],
    'Z':['11111','00001','00010','00100','01000','10000','11111'],
    '0':['01110','10001','10011','10101','11001','10001','01110'],
    '1':['00100','01100','00100','00100','00100','00100','01110'],
    '2':['01110','10001','00001','00110','01000','10000','11111'],
    '3':['01110','10001','00001','00110','00001','10001','01110'],
    '4':['00010','00110','01010','10010','11111','00010','00010'],
    '5':['11111','10000','11110','00001','00001','10001','01110'],
    '6':['01110','10001','10000','11110','10001','10001','01110'],
    '7':['11111','00001','00010','00100','01000','01000','01000'],
    '8':['01110','10001','10001','01110','10001','10001','01110'],
    '9':['01110','10001','10001','01111','00001','10001','01110'],
    ' ':['00000','00000','00000','00000','00000','00000','00000'],
    '.':['00000','00000','00000','00000','00000','00000','00100'],
    ',':['00000','00000','00000','00000','00000','00100','01000'],
    ':':['00000','00000','00100','00000','00000','00100','00000'],
    '-':['00000','00000','00000','11111','00000','00000','00000'],
    '/':['00001','00010','00010','00100','01000','01000','10000'],
    '(':['00010','00100','01000','01000','01000','00100','00010'],
    ')':['01000','00100','00010','00010','00010','00100','01000'],
    '&':['01100','10010','10100','01000','10101','10010','01101'],
    '+':['00000','00100','00100','11111','00100','00100','00000'],
    '[':['01110','01000','01000','01000','01000','01000','01110'],
    ']':['01110','00010','00010','00010','00010','00010','01110'],
    '>':['10000','01000','00100','00010','00100','01000','10000'],
    '<':['00010','00100','01000','10000','01000','00100','00010'],
}

def draw_text(px, x, y, text, color, scale=2):
    cx = x
    for ch in text.upper():
        bm = FONT.get(ch)
        if bm:
            for ri, row in enumerate(bm):
                for ci, bit in enumerate(row):
                    if bit == '1':
                        for sy in range(scale):
                            for sx in range(scale):
                                pxx = cx + ci*scale + sx
                                pyy = y + ri*scale + sy
                                if 0<=pyy<len(px) and 0<=pxx<len(px[0]):
                                    px[pyy][pxx] = color
        cx += 6*scale

def tw(text, scale=2):
    return len(text)*6*scale



def make_figure1():
    """Stakeholder Accountability Framework"""
    W, H = 800, 500
    px = [[(255,255,255) for _ in range(W)] for _ in range(H)]
    DB=(25,60,120); MB=(50,100,170); LB=(200,220,245)
    GD=(180,140,30); LGD=(255,240,200); GR=(30,120,60); LGR=(210,240,210)
    RD=(160,40,40); LRD=(255,220,220); BK=(0,0,0); GY=(100,100,100)

    draw_text(px,(W-tw("STAKEHOLDER ACCOUNTABILITY FRAMEWORK"))//2,12,"STAKEHOLDER ACCOUNTABILITY FRAMEWORK",DB,2)
    # Center
    cx,cy=400,260; bw,bh=160,60
    draw_filled_rect(px,cx-bw//2,cy-bh//2,cx+bw//2,cy+bh//2,LB)
    draw_rect_border(px,cx-bw//2,cy-bh//2,cx+bw//2,cy+bh//2,DB,3)
    draw_text(px,cx-tw("ACCREDITATION")//2,cy-7,"ACCREDITATION",DB,2)
    # Stakeholders
    boxes=[(130,100,"STUDENTS",LGD,GD),(400,75,"EMPLOYERS",LGR,GR),(670,100,"GOVERNMENT",LRD,RD),
           (130,420,"FACULTY",LB,MB),(670,420,"PUBLIC",LGR,GR)]
    for bx,by,lbl,fill,brd in boxes:
        draw_filled_rect(px,bx-70,by-25,bx+70,by+25,fill)
        draw_rect_border(px,bx-70,by-25,bx+70,by+25,brd,2)
        draw_text(px,bx-tw(lbl,1)//2,by-5,lbl,brd,1)
    # Arrows
    for bx,by,_,_,_ in boxes:
        tx=cx-bw//2 if bx<cx else (cx+bw//2 if bx>cx else cx)
        ty=cy-bh//2 if by<cy else (cy+bh//2 if by>cy else cy)
        draw_arrow(px,bx,by+(25 if by<cy else -25),tx,ty,GY,2)
    # Caption
    cap="FIGURE 1. STAKEHOLDER ACCOUNTABILITY FRAMEWORK"
    draw_text(px,(W-tw(cap,1))//2,H-22,cap,BK,1)
    return create_png(W,H,px)

def make_figure2():
    """Organizational Learning Cycle"""
    W, H = 800, 500
    px = [[(255,255,255) for _ in range(W)] for _ in range(H)]
    DB=(25,60,120); MB=(50,100,170); LB=(210,225,245)
    PR=(90,40,130); LP=(230,215,245); TL=(20,120,120); LT=(200,240,240)
    OR=(180,90,20); LO=(255,230,200); BK=(0,0,0); GY=(80,80,80)

    draw_text(px,(W-tw("ORGANIZATIONAL LEARNING CYCLE"))//2,12,"ORGANIZATIONAL LEARNING CYCLE",DB,2)
    cx,cy=400,270; bw,bh=140,55
    nodes=[(cx,cy-145,"SELF-STUDY",LB,MB),(cx+180,cy,"DATA ANALYSIS",LT,TL),
           (cx,cy+145,"PEER REVIEW",LP,PR),(cx-180,cy,"ACTION PLAN",LO,OR)]
    for nx,ny,lbl,fill,brd in nodes:
        draw_filled_rect(px,nx-bw//2,ny-bh//2,nx+bw//2,ny+bh//2,fill)
        draw_rect_border(px,nx-bw//2,ny-bh//2,nx+bw//2,ny+bh//2,brd,2)
        draw_text(px,nx-tw(lbl,1)//2,ny-5,lbl,brd,1)
    # Arrows clockwise
    draw_arrow(px,cx+bw//2,cy-145+10,cx+180-bw//2,cy-bh//2+5,GY,2)
    draw_arrow(px,cx+180-10,cy+bh//2,cx+bw//2,cy+145-10,GY,2)
    draw_arrow(px,cx-bw//2,cy+145-10,cx-180+bw//2,cy+bh//2-5,GY,2)
    draw_arrow(px,cx-180+10,cy-bh//2,cx-bw//2,cy-145+10,GY,2)
    # Center
    draw_text(px,cx-tw("CONTINUOUS",1)//2,cy-8,"CONTINUOUS",DB,1)
    draw_text(px,cx-tw("LEARNING",1)//2,cy+6,"LEARNING",DB,1)
    cap="FIGURE 2. THE ORGANIZATIONAL LEARNING CYCLE"
    draw_text(px,(W-tw(cap,1))//2,H-22,cap,BK,1)
    return create_png(W,H,px)

def make_figure3():
    """Virtuous Cycle: Accountability, Learning, Renewal"""
    W, H = 800, 520
    px = [[(255,255,255) for _ in range(W)] for _ in range(H)]
    DB=(25,60,120); BL=(40,90,160); LB=(210,225,245)
    GR=(30,120,50); LGR=(210,240,210); PR=(100,40,130); LP=(235,215,250)
    BK=(0,0,0); GY=(80,80,80); GD=(170,130,20)

    draw_text(px,(W-tw("THE VIRTUOUS CYCLE"))//2,12,"THE VIRTUOUS CYCLE",DB,2)
    draw_text(px,(W-tw("ACCOUNTABILITY - LEARNING - RENEWAL"))//2,34,"ACCOUNTABILITY - LEARNING - RENEWAL",DB,2)
    # Triangle nodes
    ax,ay=400,130; lx,ly=200,390; rx,ry=600,390
    nw,nh=150,60
    for nx,ny,lbl,fill,brd in [(ax,ay,"ACCOUNTABILITY",LB,BL),(lx,ly,"LEARNING",LGR,GR),(rx,ry,"RENEWAL",LP,PR)]:
        draw_filled_rect(px,nx-nw//2,ny-nh//2,nx+nw//2,ny+nh//2,fill)
        draw_rect_border(px,nx-nw//2,ny-nh//2,nx+nw//2,ny+nh//2,brd,3)
        draw_text(px,nx-tw(lbl,1)//2,ny-5,lbl,brd,1)
    # Arrows
    draw_arrow(px,ax-40,ay+nh//2,lx+40,ly-nh//2,GY,2)
    draw_arrow(px,lx+nw//2,ly,rx-nw//2,ry,GY,2)
    draw_arrow(px,rx-40,ry-nh//2,ax+40,ay+nh//2,GY,2)
    # Center CQI
    draw_filled_circle(px,400,300,32,(255,245,220))
    draw_circle(px,400,300,32,GD,2)
    draw_text(px,400-tw("CQI",1)//2,295,"CQI",GD,1)
    cap="FIGURE 3. THE VIRTUOUS CYCLE OF CONTINUOUS IMPROVEMENT"
    draw_text(px,(W-tw(cap,1))//2,H-22,cap,BK,1)
    return create_png(W,H,px)



# ===========================================================================
# SECTION B: DOCX XML HELPERS
# ===========================================================================

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
}

def n(prefix, tag):
    return f'{{{NS[prefix]}}}{tag}'

def para(text='', bold=False, italic=False, indent=False, center=False, style=None, sz=24):
    """Create a paragraph element."""
    p = Element(n('w','p'))
    pPr = SubElement(p, n('w','pPr'))
    if style:
        ps = SubElement(pPr, n('w','pStyle')); ps.set(n('w','val'), style)
    sp = SubElement(pPr, n('w','spacing'))
    sp.set(n('w','line'),'480'); sp.set(n('w','lineRule'),'auto')
    if indent:
        ind = SubElement(pPr, n('w','ind')); ind.set(n('w','firstLine'),'720')
    if center:
        jc = SubElement(pPr, n('w','jc')); jc.set(n('w','val'),'center')
    if text:
        r = SubElement(p, n('w','r'))
        rPr = SubElement(r, n('w','rPr'))
        rf = SubElement(rPr, n('w','rFonts'))
        rf.set(n('w','ascii'),'Times New Roman'); rf.set(n('w','hAnsi'),'Times New Roman'); rf.set(n('w','cs'),'Times New Roman')
        s = SubElement(rPr, n('w','sz')); s.set(n('w','val'),str(sz))
        sc = SubElement(rPr, n('w','szCs')); sc.set(n('w','val'),str(sz))
        if bold: SubElement(rPr, n('w','b'))
        if italic: SubElement(rPr, n('w','i'))
        t = SubElement(r, n('w','t'))
        t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
        t.text = text
    return p

def ref_para(text):
    """Reference paragraph with hanging indent."""
    p = Element(n('w','p'))
    pPr = SubElement(p, n('w','pPr'))
    sp = SubElement(pPr, n('w','spacing'))
    sp.set(n('w','line'),'480'); sp.set(n('w','lineRule'),'auto'); sp.set(n('w','after'),'0')
    ind = SubElement(pPr, n('w','ind')); ind.set(n('w','left'),'720'); ind.set(n('w','hanging'),'720')
    if text:
        r = SubElement(p, n('w','r'))
        rPr = SubElement(r, n('w','rPr'))
        rf = SubElement(rPr, n('w','rFonts'))
        rf.set(n('w','ascii'),'Times New Roman'); rf.set(n('w','hAnsi'),'Times New Roman'); rf.set(n('w','cs'),'Times New Roman')
        s = SubElement(rPr, n('w','sz')); s.set(n('w','val'),'24')
        sc = SubElement(rPr, n('w','szCs')); sc.set(n('w','val'),'24')
        t = SubElement(r, n('w','t'))
        t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
        t.text = text
    return p

def table(headers, rows):
    """Create a Word table with borders and header shading."""
    tbl = Element(n('w','tbl'))
    tblPr = SubElement(tbl, n('w','tblPr'))
    tw_el = SubElement(tblPr, n('w','tblW')); tw_el.set(n('w','w'),'9360'); tw_el.set(n('w','type'),'dxa')
    brd = SubElement(tblPr, n('w','tblBorders'))
    for bn in ['top','left','bottom','right','insideH','insideV']:
        b = SubElement(brd, n('w',bn)); b.set(n('w','val'),'single'); b.set(n('w','sz'),'4'); b.set(n('w','space'),'0'); b.set(n('w','color'),'000000')
    nc = len(headers); cw = 9360//nc
    grid = SubElement(tbl, n('w','tblGrid'))
    for _ in range(nc): gc = SubElement(grid, n('w','gridCol')); gc.set(n('w','w'),str(cw))
    # Header
    tr = SubElement(tbl, n('w','tr'))
    for h in headers:
        tc = SubElement(tr, n('w','tc'))
        tcPr = SubElement(tc, n('w','tcPr'))
        tcW = SubElement(tcPr, n('w','tcW')); tcW.set(n('w','w'),str(cw)); tcW.set(n('w','type'),'dxa')
        shd = SubElement(tcPr, n('w','shd')); shd.set(n('w','val'),'clear'); shd.set(n('w','color'),'auto'); shd.set(n('w','fill'),'D9E2F3')
        tc.append(para(h, bold=True, center=True, sz=20))
    # Rows
    for row in rows:
        tr = SubElement(tbl, n('w','tr'))
        for cell in row:
            tc = SubElement(tr, n('w','tc'))
            tcPr = SubElement(tc, n('w','tcPr'))
            tcW = SubElement(tcPr, n('w','tcW')); tcW.set(n('w','w'),str(cw)); tcW.set(n('w','type'),'dxa')
            tc.append(para(cell, sz=20))
    return tbl

def img_para(rid, w_emu, h_emu, name='Figure'):
    """Paragraph with inline image."""
    p = Element(n('w','p'))
    pPr = SubElement(p, n('w','pPr'))
    jc = SubElement(pPr, n('w','jc')); jc.set(n('w','val'),'center')
    sp = SubElement(pPr, n('w','spacing')); sp.set(n('w','line'),'480'); sp.set(n('w','lineRule'),'auto')
    r = SubElement(p, n('w','r'))
    dr = SubElement(r, n('w','drawing'))
    inl = SubElement(dr, n('wp','inline'))
    inl.set('distT','0'); inl.set('distB','0'); inl.set('distL','0'); inl.set('distR','0')
    ext = SubElement(inl, n('wp','extent')); ext.set('cx',str(w_emu)); ext.set('cy',str(h_emu))
    dp = SubElement(inl, n('wp','docPr')); dp.set('id','1'); dp.set('name',name)
    gr = SubElement(inl, n('a','graphic'))
    gd = SubElement(gr, n('a','graphicData')); gd.set('uri','http://schemas.openxmlformats.org/drawingml/2006/picture')
    pic = SubElement(gd, n('pic','pic'))
    nvp = SubElement(pic, n('pic','nvPicPr'))
    cnvp = SubElement(nvp, n('pic','cNvPr')); cnvp.set('id','0'); cnvp.set('name',name)
    SubElement(nvp, n('pic','cNvPicPr'))
    bf = SubElement(pic, n('pic','blipFill'))
    blip = SubElement(bf, n('a','blip')); blip.set(n('r','embed'),rid)
    st = SubElement(bf, n('a','stretch')); SubElement(st, n('a','fillRect'))
    spPr = SubElement(pic, n('pic','spPr'))
    xfrm = SubElement(spPr, n('a','xfrm'))
    off = SubElement(xfrm, n('a','off')); off.set('x','0'); off.set('y','0')
    ex2 = SubElement(xfrm, n('a','ext')); ex2.set('cx',str(w_emu)); ex2.set('cy',str(h_emu))
    pg = SubElement(spPr, n('a','prstGeom')); pg.set('prst','rect')
    return p



# ===========================================================================
# SECTION C: FULL MANUSCRIPT CONTENT (~7000 words)
# ===========================================================================

def build_manuscript():
    """Build the entire manuscript as a list of XML paragraph/table elements."""
    P = []  # paragraph list
    B = lambda: P.append(para())  # blank line
    H1 = lambda t: P.append(para(t, style='Heading1', bold=True))
    H2 = lambda t: P.append(para(t, style='Heading2', bold=True))
    T = lambda t: P.append(para(t, indent=True))  # body text with first-line indent
    C = lambda t, **kw: P.append(para(t, center=True, **kw))  # centered

    # ===== TITLE =====
    B(); B()
    H1('Accreditation as Accountability, Learning, and Institutional Renewal')
    B()
    H2('Author Information')
    B()
    P.append(para('[Author Name]'))
    P.append(para('ORCID: [0000-0000-0000-0000]'))
    P.append(para('Affiliation: [Department, Institution, City, Country]'))
    P.append(para('Email: [author.email@institution.edu]'))
    B()
    T('Bio: [Author Name] is a [title/position] at [Institution]. With over [X] years of experience in higher education policy and accreditation, [he/she/they] has published extensively on quality assurance, institutional effectiveness, and organizational learning in post-secondary education. [His/Her/Their] research focuses on the intersection of accountability frameworks and institutional transformation in a globalized higher education landscape. [He/She/They] has served on multiple accreditation review teams and advisory boards.')
    B(); B()

    # ===== ABSTRACT =====
    H2('Abstract')
    B()
    T('This chapter examines the multifaceted role of accreditation in contemporary higher education, arguing that its true power lies not in any single function but in the dynamic interplay among three essential dimensions: accountability, learning, and institutional renewal. In an era marked by unprecedented skepticism toward the value of higher education, escalating costs, and rapid technological disruption, accreditation has evolved from a collegial peer-review process into a high-stakes mechanism for demonstrating institutional legitimacy. This chapter moves beyond the conventional view of accreditation as merely a compliance exercise. Drawing on organizational learning theory, institutional theory, and quality improvement frameworks, it demonstrates how a strategically approached accreditation process can serve as a powerful catalyst for self-discovery, evidence-based decision-making, and transformative institutional change. The chapter is structured around three interconnected sections: the accountability imperative that establishes the non-negotiable baseline of quality assurance; the learning dimension that repositions the process as a framework for organizational intelligence; and the renewal function that translates self-knowledge into strategic foresight and cultural transformation. The analysis concludes by proposing that institutions that embrace this holistic, cyclical view of accreditation can transform what is often perceived as a bureaucratic burden into their most powerful instrument for thriving in the boundaryless landscape of twenty-first-century higher education.')
    B()
    P.append(para('Keywords: accreditation, accountability, institutional learning, quality assurance, continuous improvement, higher education, organizational renewal, self-study, peer review'))
    B(); B()

    # ===== INTRODUCTION =====
    H1('Introduction')
    B()
    T('The landscape of higher education is undergoing a period of profound transformation. Traditional boundaries\u2014between disciplines, between institutions, between nations, and between the academy and the world of work\u2014are dissolving at an accelerating pace. In this environment of radical change, the question of how institutions demonstrate their quality, relevance, and fitness for purpose has become one of the most consequential debates in educational policy [1]. At the center of this debate stands accreditation: a process that is simultaneously ancient in its collegial principles and urgently modern in its demands.')
    B()
    T('Accreditation in higher education has long functioned as the primary mechanism through which institutions voluntarily submit to external review to demonstrate that they meet established standards of quality [2]. Yet the perception and purpose of this process have shifted dramatically over the past three decades. What was once a largely private conversation among academic peers has become a public instrument of accountability, scrutinized by legislators, journalists, and an increasingly skeptical public demanding evidence that the substantial investment in higher education yields meaningful returns [3, 4].')
    B()
    T('This chapter advances a central argument: that accreditation, when approached with intentionality and strategic vision, functions not as a single activity but as a dynamic cycle comprising three interconnected dimensions\u2014accountability, learning, and renewal. Accountability represents the non-negotiable baseline: the demonstration to external stakeholders that an institution is financially viable, ethically governed, and educationally effective. Learning represents the transformative middle ground: the use of systematic self-examination and peer review to build organizational intelligence and foster a culture of evidence-based inquiry. Renewal represents the ultimate aspiration: the translation of institutional self-knowledge into strategic action, adaptive capacity, and cultural transformation that positions the institution for long-term flourishing.')
    B()
    T('These three dimensions are not sequential phases but rather simultaneous and mutually reinforcing aspects of a single, virtuous cycle. Accountability without learning becomes mere bureaucratic compliance; learning without renewal is intellectual exercise without consequence; renewal without accountability is unsustainable aspiration without foundation. This chapter explores each dimension in turn, drawing on theoretical frameworks from organizational learning [5, 6], institutional theory [7], and quality management [8], while grounding the analysis in the practical realities of accreditation as experienced by institutions navigating the boundaryless landscape of contemporary higher education.')
    B()
    T('The significance of this argument extends beyond the procedural mechanics of accreditation to address fundamental questions about the nature and purpose of quality assurance in post-secondary education. As institutions face existential challenges\u2014demographic shifts that threaten enrollment stability, technological disruptions that challenge traditional pedagogical models, and legitimacy crises that erode public support\u2014the capacity to learn and adapt becomes not merely desirable but essential for institutional survival. Accreditation, reconceived as a catalyst for this adaptive capacity, offers institutions a structured pathway from compliance to transformation\u2014a pathway that honors the legitimate demands of accountability while simultaneously cultivating the organizational intelligence necessary for strategic renewal [9].')
    B()
    T('The structure of this chapter reflects the interconnected nature of its argument. Section 1 examines the accountability dimension, exploring how shifting stakeholder expectations have transformed accreditation into a high-stakes mechanism for demonstrating institutional value, while also acknowledging the pathologies that can emerge from an overemphasis on compliance. Section 2 repositions accreditation as a framework for organizational learning, examining how the self-study process, evidence-based inquiry, and peer review create unique opportunities for institutional self-discovery. Section 3 explores the renewal dimension, demonstrating how accreditation can serve as a catalyst for strategic transformation, institutional agility, and the development of a permanent culture of continuous quality improvement. The conclusion synthesizes these three dimensions into an integrated model and offers recommendations for institutional leaders, faculty, and accreditors seeking to realize accreditation\u2019s full transformative potential.')
    B(); B()

    # ===== SECTION 1 =====
    H1('Section 1: The Face of Accountability: Demonstrating Value in a Skeptical Era')
    B()
    H2('1.1 The Stakeholder Mandate: From Public Trust to Public Proof')
    B()
    T('The social contract between higher education and the public has undergone a fundamental renegotiation. For much of the twentieth century, institutions of higher learning operated under a regime of presumptive trust. Society granted universities considerable autonomy\u2014intellectual, financial, and operational\u2014in exchange for the broadly understood social goods of research, teaching, and community service [10]. Accreditation, in this context, functioned primarily as a form of self-regulation among peers, a collegial handshake affirming that a fellow institution met basic standards of respectability.')
    B()
    T('That era of presumptive trust has ended. In its place has emerged what might be termed a regime of demonstrable proof [11]. Multiple forces have driven this transformation. The exponential growth of tuition costs has converted higher education from a broadly accessible public good into what many families experience as a high-stakes financial investment demanding quantifiable returns [4]. The proliferation of post-secondary providers\u2014including for-profit institutions, online platforms, and international competitors\u2014has created a marketplace in which the traditional signals of quality (institutional age, reputation, selectivity) are no longer sufficient differentiators. Simultaneously, a series of high-profile institutional failures and predatory practices has eroded public confidence in the capacity of higher education to police itself [12].')
    B()
    T('The cost-value equation has become the dominant frame through which students and families assess educational options. In a globalized market with thousands of providers, accreditation serves as the primary quality benchmark\u2014a credible signal that an institution has been externally validated against recognized standards [13]. For prospective students weighing the return on investment of a degree, accreditation status provides a minimum threshold of assurance that their credits will transfer, their credentials will be recognized, and their educational experience will meet baseline expectations of rigor and relevance.')
    B()
    T('From the employer\u2019s perspective, accreditation functions as a risk-reduction mechanism. In an era of credential inflation and competency-based hiring, employers rely on accreditation as a signal that graduates from a particular institution possess a baseline of knowledge, skills, and professional competencies [14]. This is particularly consequential in fields with professional licensure requirements, where graduation from an accredited program is a prerequisite for practice. The employer\u2019s lens thus transforms accreditation from an academic exercise into an economic imperative with direct workforce implications.')
    B()
    T('The governmental dimension of this stakeholder mandate is perhaps the most consequential. In the United States, institutional accreditation serves as the gateway to federal financial aid\u2014a mechanism that channels over $150 billion annually to students and, through them, to institutions [15]. This linkage between accreditation status and access to public funding has transformed what was once a voluntary professional process into an effective governmental requirement, dramatically raising the stakes of accreditation decisions and intensifying demands for transparency and public accountability. State governments, too, have increasingly linked appropriations and performance-based funding models to accreditation-related metrics such as graduation rates, employment outcomes, and student loan default rates.')
    B()
    T('Internationally, this governmental interest in accreditation has intensified as nations recognize the economic implications of higher education quality. The Bologna Process in Europe, the establishment of national quality assurance agencies across Asia and Africa, and the growth of cross-border quality assurance networks all reflect a global convergence toward more systematic accountability mechanisms [16]. In this international context, accreditation serves not only as a domestic quality signal but as a mechanism for international credential recognition, student mobility, and institutional reputation\u2014functions that are increasingly consequential in a globalized labor market where graduates compete across national boundaries. The convergence of these domestic and international forces has created a stakeholder environment in which accountability is no longer optional but existential\u2014institutions that cannot demonstrate their value risk not merely reputational damage but loss of the financial resources upon which their operations depend.')
    B(); B()

    # ---- TABLE 1 ----
    C('Table 1', bold=True); C('Stakeholder Expectations and Accreditation Responses', italic=True); B()
    P.append(table(
        ['Stakeholder', 'Primary Expectation', 'Accreditation Response', 'Key Metric'],
        [['Students/Families', 'ROI; credential portability', 'Quality benchmarking; transfer assurance', 'Graduation/employment rates'],
         ['Employers', 'Graduate competency', 'Program outcomes; professional standards', 'Licensure pass rates'],
         ['Government', 'Responsible use of public funds', 'Financial viability; compliance review', 'Default/completion rates'],
         ['Faculty/Staff', 'Academic freedom; development', 'Governance; faculty qualification standards', 'Faculty retention rates'],
         ['Public/Society', 'Institutional integrity', 'Mission fidelity; transparency', 'Community engagement indices']]
    ))
    B(); B()

    H2('1.2 Compliance and Standards: The Baseline of Quality Assurance')
    B()
    T('If the stakeholder mandate establishes the why of accountability, accreditation standards establish the what. Standards represent the codified expectations against which institutional quality is measured\u2014the \u201chygiene factors\u201d (to borrow from Herzberg\u2019s motivational theory) whose absence signals fundamental deficiency but whose presence alone does not guarantee excellence [17]. These standards address the foundational requirements that ensure institutional stability, integrity, and basic educational effectiveness.')
    B()
    T('Financial viability constitutes a primary domain of accreditation standards. Institutions must demonstrate sound fiscal management, sustainable revenue models, and adequate reserves to fulfill their commitments to enrolled students and employed staff [18]. The financial scrutiny embedded in accreditation review serves a critical protective function, identifying institutions at risk of sudden closure\u2014a scenario whose human costs have been vividly demonstrated by the abrupt shuttering of institutions that left students mid-degree with non-transferable credits and substantial debt [19].')
    B()
    T('Student protection represents another essential dimension of compliance standards. Accreditation requires institutions to maintain transparent admissions policies, fair grading practices, accessible grievance procedures, and accurate representations of programs and outcomes [20]. Mission fidelity represents a distinctive dimension: most regional accrediting bodies evaluate institutions against their own stated missions [21], respecting institutional diversity while establishing accountability for alignment between stated purposes and actual operations.')
    B()
    T('Beyond these specific domains, accreditation standards collectively establish what might be termed the infrastructure of educational integrity. They require institutions to maintain qualified faculty, adequate physical and technological resources, coherent curricula, effective governance structures, and systematic processes for assessing student learning [18]. Their codification creates explicit expectations against which institutional performance can be measured, communicated, and sanctioned.')
    B(); B()

    H2('1.3 Navigating the \u201cAudit Culture\u201d: The Pitfalls and Potentials')
    B()
    T('While accountability serves essential purposes, an honest examination of accreditation must acknowledge the pathologies that can emerge when accountability becomes an end in itself rather than a means toward improvement. The concept of \u201caudit culture\u201d [22] provides a useful critical lens for understanding these dynamics. When institutions experience accreditation primarily as a surveillance mechanism\u2014a threat to be managed rather than an opportunity to be embraced\u2014predictable dysfunctions emerge.')
    B()
    T('The \u201cbox-checking\u201d mentality represents perhaps the most pervasive pathology. When institutional actors perceive accreditation primarily as a compliance exercise with high-stakes consequences for failure, their rational response is to focus energy on satisfying the letter of the standards while minimizing disruption to existing practices [16]. This results in performative compliance: the production of documentation that presents an institution favorably without necessarily reflecting genuine engagement with quality questions.')
    B()
    T('Mission creep represents a subtler pathology. When accreditation standards are perceived as reflecting a singular model of institutional quality, institutions with distinctive missions may feel pressure to conform to expectations that do not align with their unique purposes [23]. The homogenizing pressure of standardized accountability can stifle the institutional diversity that is one of higher education\u2019s greatest strengths. The burden of evidence constitutes a practical challenge: comprehensive self-study preparation requires substantial investments of staff time, faculty energy, and financial resources [24]. The challenge is to develop systems for efficient and integrated data management that serve both accountability and improvement purposes simultaneously.')
    B(); B()

    # ---- FIGURE 1 ----
    P.append(img_para('rId3', 6096000, 3810000, 'Figure 1'))
    B()
    C('Figure 1. Stakeholder Accountability Framework showing multiple stakeholders', italic=True)
    C('converging on accreditation as the mechanism for demonstrable proof of quality.', italic=True)
    B(); B()

    return P



def build_section2(P):
    """Section 2 content."""
    B = lambda: P.append(para())
    H1 = lambda t: P.append(para(t, style='Heading1', bold=True))
    H2 = lambda t: P.append(para(t, style='Heading2', bold=True))
    T = lambda t: P.append(para(t, indent=True))
    C = lambda t, **kw: P.append(para(t, center=True, **kw))

    H1('Section 2: The Pedagogy of Organizations: Accreditation as a Framework for Learning')
    B()
    H2('2.1 The Self-Study as a Diagnostic Tool: Uncovering Tacit Knowledge')
    B()
    T('If Section 1 addressed the compliance dimension of accreditation\u2014the non-negotiable baseline of quality assurance\u2014this section repositions the accreditation process as a rich opportunity for institutional self-discovery and organizational learning. The theoretical foundation for this repositioning draws on the concept of the \u201clearning organization\u201d [5]: an entity that continuously enhances its capacity to create its desired future through systematic processes of inquiry, reflection, and adaptive action.')
    B()
    T('The self-study\u2014the comprehensive institutional examination that forms the centerpiece of most accreditation processes\u2014is far more than a report to be produced. When approached with genuine intellectual curiosity and organizational commitment, it functions as a powerful diagnostic tool: a structured occasion for an institution to systematically examine its own assumptions, practices, and outcomes [25]. In the language of organizational learning theory, the self-study creates the conditions for both single-loop learning (detecting and correcting errors within existing frames) and double-loop learning (questioning and revising the frames themselves) [6].')
    B()
    T('A well-facilitated self-study creates what organizational theorists term a \u201clearning space\u201d\u2014a psychologically safe environment in which difficult questions can be asked, uncomfortable data can be examined, and honest assessments can be offered without fear of retribution [26]. This is no small achievement in academic organizations, which are often characterized by disciplinary silos, hierarchical governance structures, and cultural norms that reward individual expertise over collective inquiry. The accreditation self-study, by virtue of its institutional legitimacy and external mandate, provides permission to ask questions that might otherwise be deemed threatening or inappropriate: Are our students actually learning what we claim to teach? Are our support services reaching those who need them most? Are our resource allocation decisions aligned with our stated priorities? Are we achieving equitable outcomes across different student populations?')
    B()
    T('The self-study\u2019s requirement to examine the entire institution\u2014from governance and finance to curriculum and student support\u2014forces departments and divisions to communicate across traditional boundaries. Academic affairs must engage with student affairs; enrollment management must dialogue with academic departments; information technology must connect its resource planning to institutional learning goals [27]. This cross-functional engagement is particularly valuable in institutions where organizational silos have calcified over time, creating fragmented understanding of the student experience. The accreditation self-study thus serves as one of the few occasions in institutional life when the entire organization is required to examine itself as an integrated system rather than a collection of independent units.')
    B()
    T('Perhaps most importantly, a genuine self-study process can reveal the \u201cunknown unknowns\u201d\u2014gaps in institutional knowledge that are not normally on the organizational radar [28]. Through systematic data collection and cross-functional dialogue, institutions may discover that retention rates diverge dramatically across demographic groups; that students in certain programs consistently report lower satisfaction despite high academic performance; that substantial resources are being allocated to activities whose contribution to the institutional mission is unclear. These discoveries\u2014often uncomfortable but invariably valuable\u2014constitute the raw material of organizational learning. The temporal dimension also merits attention: concentrated examination of five or ten years of data reveals longitudinal patterns obscured in annual reporting cycles, providing the empirical foundation for strategic projection [29]. The self-study thus functions not merely as a snapshot but as a time-lapse photograph that reveals trajectories of change and provides the basis for evidence-informed planning.')
    B(); B()

    # ---- TABLE 2 ----
    C('Table 2', bold=True); C('Self-Study Components and Institutional Learning Outcomes', italic=True); B()
    P.append(table(
        ['Self-Study Component', 'Learning Process', 'Organizational Outcome', 'Theory Base'],
        [['Institutional data collection', 'Single-loop: error detection', 'Performance gap identification', 'Argyris & Schon [6]'],
         ['Cross-functional dialogue', 'Bridging organizational silos', 'Holistic student experience view', 'Senge [5]'],
         ['Mission alignment review', 'Double-loop: frame questioning', 'Strategic clarity and renewal', 'Argyris & Schon [6]'],
         ['Stakeholder surveys', 'Environmental scanning', 'Market responsiveness', 'Volkwein et al. [30]'],
         ['Outcomes assessment', 'Evidence-based inquiry', 'Pedagogical improvement', 'Banta & Palomba [33]'],
         ['Resource analysis', 'Systems thinking', 'Efficient allocation', 'Senge [5]']]
    ))
    B(); B()

    H2('2.2 Data, Evidence, and the Culture of Inquiry: Building Organizational Intelligence')
    B()
    T('The shift from \u201cdata for compliance\u201d to \u201cdata for understanding\u201d represents one of the most significant conceptual advances in contemporary accreditation practice. This shift parallels broader developments in organizational management, where the movement from \u201cbusiness intelligence\u201d to \u201corganizational intelligence\u201d reflects a recognition that data\u2019s value lies not in its collection but in its capacity to inform action and generate insight [30].')
    B()
    T('The accreditation process mandates the use of systematic evidence, which can serve as a powerful antidote to the anecdotal reasoning that often characterizes academic decision-making. Faculty frequently hold strong beliefs about what constitutes effective pedagogy, which students are \u201cprepared\u201d for college-level work, and which programs are \u201cexcellent\u201d\u2014beliefs that may be grounded in individual experience but are not always supported by systematic evidence [31]. The requirement to produce evidence of student learning outcomes, retention and completion rates, and graduate employment can challenge these assumptions, replacing intuition with information and opinion with evidence.')
    B()
    T('The development of sophisticated learning analytics represents an emerging frontier in accreditation-driven data use. Rather than merely reporting historical outcomes, institutions are increasingly using the data infrastructure built for accreditation purposes to develop predictive models for student success [32]. By analyzing patterns in student engagement, course performance, and utilization of support services, institutions can identify students at risk of departure early enough to intervene effectively. This predictive capacity transforms the institution from a passive recorder of outcomes to an active agent in student success\u2014a shift that directly serves both accountability and improvement purposes and represents the kind of data-driven institutional intelligence that the most forward-thinking accrediting bodies now expect.')
    B()
    T('The concept of \u201cclosing the assessment loop\u201d represents the critical step that distinguishes genuine organizational learning from mere data collection [33]. This concept requires institutions not merely to measure outcomes but to use those measurements to implement changes, and then to re-assess to determine whether the changes produced the intended improvements. This iterative cycle\u2014plan, implement, assess, improve\u2014constitutes the engine of institutional learning. When assessment reveals that students in a particular program are not achieving expected learning outcomes, the institution must demonstrate that it has investigated root causes, implemented targeted interventions, and measured the effects of those interventions. This requirement transforms accreditation from a snapshot assessment into a longitudinal narrative of improvement. The cultural shift required to move from data collection to genuine evidence-based decision-making should not be underestimated; academic institutions have historically been characterized by a culture of autonomous professional judgment [34], and institutions must frame assessment as professional enhancement rather than surveillance to navigate this transition successfully.')
    B(); B()

    H2('2.3 Peer Review: The Transformative Power of External Perspectives')
    B()
    T('The peer review visit\u2014in which a team of experienced academics and administrators from other institutions conducts an on-site evaluation\u2014represents one of accreditation\u2019s most distinctive and valuable features. Unlike governmental inspection regimes or commercial auditing processes, peer review operates on the principle that institutions are best evaluated by those who share their fundamental purposes and understand their operational complexities [1]. This collegial foundation distinguishes accreditation from other forms of external accountability and creates unique opportunities for organizational learning.')
    B()
    T('The capacity to challenge organizational groupthink represents one of peer review\u2019s most important functions. Every organization develops internal narratives\u2014stories it tells itself about its strengths, its challenges, and its identity\u2014that over time can become so deeply embedded that they are no longer subject to critical examination [35]. External reviewers, precisely because they do not share these narratives, can identify blind spots that are invisible to insiders. They may observe that an institution\u2019s self-description as \u201cstudent-centered\u201d is contradicted by policies that privilege administrative convenience over student access; that claims of \u201cshared governance\u201d coexist with decision-making processes that are opaque and exclusionary; or that assertions of \u201cinnovation\u201d mask a fundamental resistance to pedagogical change. These observations, delivered with the credibility of external expertise, can catalyze conversations that internal critics have been unable to initiate.')
    B()
    T('The peer review visit also functions as a mechanism for best practice exchange. Visiting team members bring knowledge of effective practices at their own institutions, while the host institution\u2019s innovations may inspire visitors to implement changes upon their return [36]. This bidirectional knowledge transfer represents a form of structured, non-competitive intelligence gathering that has few parallels in other sectors. Unlike commercial competitors who guard proprietary processes, academic institutions participating in peer review engage in open sharing of effective practices\u2014a manifestation of the academic values of openness and collective advancement of knowledge.')
    B()
    T('The legitimacy and validation that peer review provides should not be underestimated as a factor in organizational motivation and morale [37]. When respected colleagues from peer institutions affirm that an institution\u2019s efforts are producing meaningful results\u2014that its innovations are working, that its faculty are dedicated, that its students are thriving\u2014the psychological and institutional effects are significant. This validation can energize faculty and staff, reinforce institutional identity, and provide political capital for continued investment in quality improvement initiatives. Moreover, the preparation for peer review itself catalyzes reflection and collective sense-making that extends well beyond the formal evaluation period [38]. Faculty and staff who participate in presentations to visiting teams often report that the process deepens their own understanding of their work and its connection to broader institutional purposes.')
    B(); B()

    # ---- FIGURE 2 ----
    P.append(img_para('rId4', 6096000, 3810000, 'Figure 2'))
    B()
    C('Figure 2. The Organizational Learning Cycle showing how accreditation creates', italic=True)
    C('a continuous cycle of self-study, data analysis, peer review, and action.', italic=True)
    B(); B()

    return P



def build_section3(P):
    """Section 3 content."""
    B = lambda: P.append(para())
    H1 = lambda t: P.append(para(t, style='Heading1', bold=True))
    H2 = lambda t: P.append(para(t, style='Heading2', bold=True))
    T = lambda t: P.append(para(t, indent=True))
    C = lambda t, **kw: P.append(para(t, center=True, **kw))

    H1('Section 3: The Catalyst for Renewal: Reimagining the Institution for the Future')
    B()
    H2('3.1 Strategic Foresight: Aligning Accreditation with Institutional Strategy')
    B()
    T('The transition from learning to renewal marks the point at which institutional self-knowledge is translated into strategic action. This section argues that the most effective institutions approach accreditation not as an isolated compliance activity but as an integral component of their strategic planning process\u2014using the rhythms of the accreditation cycle to structure and energize long-term institutional transformation [39].')
    B()
    T('The concept of the \u201crhythm of renewal\u201d offers a powerful reframing of the accreditation cycle. Rather than experiencing the ten-year reaffirmation cycle as a periodic disruption\u2014a frantic scramble of documentation and preparation that interrupts normal operations\u2014institutions can reconceive this rhythm as a structured timeline for strategic implementation [40]. The first years following reaffirmation become a period for bold strategic planning informed by the self-study\u2019s findings; the middle years become a period of implementation and piloting; the final years before the next review become a period of assessment and course correction. This alignment transforms accreditation from an external imposition into an internal strategic tool.')
    B()
    T('Mission serves as the compass in this strategic alignment. The self-study process\u2014if genuinely conducted\u2014forces institutions to critically evaluate whether their current strategic direction remains aligned with their foundational purposes and with evolving market realities [23]. In a rapidly changing environment, yesterday\u2019s strategic plan may no longer be responsive to today\u2019s challenges. An institution whose mission emphasizes preparation for the workforce must continuously evaluate whether its programs align with emerging employment needs. A liberal arts college committed to developing critical thinking must assess whether its pedagogical approaches remain effective for current student populations. The self-study provides a structured occasion for this essential strategic reflection.')
    B()
    T('Resource allocation represents a critical bridge between strategic insight and institutional action. The findings from a thorough self-study provide an evidence base for difficult resource decisions that might otherwise be made on the basis of political power, historical precedent, or institutional inertia [41]. When accreditation findings demonstrate that a program is producing excellent outcomes with minimal resources, or conversely that substantial investment in another area is yielding disappointing results, institutional leaders gain both the information and the political legitimacy to advocate for strategic reallocation. The strategic alignment of accreditation with institutional planning also creates opportunities for building institutional capacity\u2014investing in data systems, assessment expertise, and communication structures as strategic assets rather than mere accreditation expenses [42].')
    B(); B()

    H2('3.2 Enhancing Agility and Responsiveness: Adapting to a Boundaryless World')
    B()
    T('The theme of this volume\u2014\u201chigher education beyond boundaries\u201d\u2014invites direct consideration of how accreditation can facilitate rather than impede institutional agility in a rapidly evolving landscape. Critics have long argued that accreditation\u2019s emphasis on stability and standardization can function as a conservative force, slowing institutional adaptation to changing realities [43]. This criticism contains an element of truth: accreditation standards developed for traditional residential institutions may not adequately address the realities of online learning, competency-based education, or international partnerships. Yet this tension also creates an opportunity for accrediting bodies and institutions to collaboratively reimagine the relationship between quality assurance and innovation.')
    B()
    T('The concept of \u201cinnovation sandboxes\u201d offers a promising framework for reconciling quality assurance with experimental pedagogy. Several accrediting bodies have begun developing mechanisms that allow institutions to pilot new approaches\u2014micro-credentials, stackable certificates, competency-based progressions, employer-embedded learning experiences\u2014within a framework of enhanced monitoring rather than standard compliance [44]. These sandbox approaches acknowledge that innovation necessarily involves uncertainty and that rigid adherence to traditional standards can prevent institutions from developing the new models that the future of higher education demands. The most forward-thinking accrediting bodies are moving toward a model in which demonstrated capacity for self-assessment and self-correction is weighted as heavily as current compliance with specific standards\u2014an approach that rewards institutional maturity and learning capacity rather than merely documenting conformity.')
    B()
    T('Responding to workforce shifts represents an increasingly urgent dimension of institutional agility. The acceleration of technological change, the emergence of new industries, and the obsolescence of traditional occupations create constant pressure on institutions to update curricula, develop new programs, and create flexible pathways to employment [14]. Accreditation can support this responsiveness by requiring institutions to demonstrate active engagement with employer feedback, alumni outcomes data, and labor market intelligence\u2014not as a one-time compliance exercise but as an ongoing practice of environmental scanning and curricular adaptation. Serving non-traditional students\u2014adult learners, first-generation students, working professionals, and internationally mobile learners\u2014requires models that differ fundamentally from the traditional full-time residential paradigm [45]. Accreditation standards must evolve to accommodate these diverse learner profiles, recognizing that quality may manifest differently across different delivery modalities and student populations [46].')
    B(); B()

    # ---- TABLE 3 ----
    C('Table 3', bold=True); C('From Compliance Event to Continuous Quality Improvement Culture', italic=True); B()
    P.append(table(
        ['Dimension', 'Traditional (Event)', 'CQI Approach (Process)', 'Enabling Factor'],
        [['Timing', 'Decennial preparation', 'Ongoing annual cycles', 'Embedded data systems'],
         ['Leadership', 'Top-down mandate', 'Distributed ownership', 'Faculty empowerment'],
         ['Data Use', 'Retrospective reporting', 'Real-time analytics', 'Learning analytics platforms'],
         ['Culture', 'Fear-based compliance', 'Curiosity-driven improvement', 'Psychological safety'],
         ['Scope', 'Document production', 'Systemic organizational learning', 'Cross-functional teams'],
         ['Outcome', 'Status reaffirmation', 'Institutional transformation', 'Strategic alignment']]
    ))
    B(); B()

    H2('3.3 Fostering a Culture of Continuous Quality Improvement')
    B()
    T('The ultimate aspiration of accreditation as renewal is the institutionalization of a culture of continuous quality improvement (CQI)\u2014a state in which the practices of systematic inquiry, evidence-based decision-making, and adaptive action become permanent features of institutional life rather than episodic responses to external review [47]. This aspiration draws on the quality management traditions pioneered in manufacturing by Deming [8] and Juran [48] and subsequently adapted to educational contexts by scholars including Seymour [49] and Freed et al. [50].')
    B()
    T('The transformation from \u201cevent\u201d to \u201cprocess\u201d is fundamental to achieving a CQI culture. When institutions experience accreditation primarily as a decennial event\u2014a project with a beginning, middle, and end\u2014the work of quality improvement tends to surge during preparation periods and dissipate once the site visit concludes [40]. The alternative model institutionalizes the core practices of the self-study on an ongoing, cyclical basis. Annual assessment cycles, regular program reviews, periodic environmental scans, and systematic tracking of key performance indicators create a continuous feedback system that maintains institutional attention on quality regardless of the accreditation calendar. This perpetual engagement with evidence and improvement eliminates the destructive pattern of neglect followed by panic that characterizes many institutions\u2019 relationship with accreditation.')
    B()
    T('Faculty and staff empowerment constitutes a critical success factor in building a CQI culture. The traditional approach to accreditation is predominantly top-down: administrators identify standards, assign report-writing tasks, and manage site visit logistics, while faculty and staff experience the process as an administrative burden imposed upon their \u201creal work\u201d [39]. The CQI alternative inverts this dynamic, positioning faculty and staff as the primary agents of quality improvement. When instructors are engaged as genuine partners in assessment\u2014participating in designing learning outcomes, selecting methods, analyzing results, and implementing improvements\u2014they develop ownership of the quality improvement process.')
    B()
    T('The concept of the \u201clearning organization\u201d [5] provides the theoretical capstone for this discussion. A learning organization is one that has developed the systemic capacity to continuously transform itself through five interrelated disciplines: personal mastery, shared mental models, team learning, systems thinking, and shared vision. An institution that has achieved a genuine CQI culture embodies these disciplines: its members are committed to professional growth; its shared assumptions are regularly examined and updated; its teams engage in genuine dialogue rather than mere discussion; its leaders think systemically about the interconnections among institutional functions; and its community shares a compelling vision of quality that motivates and guides collective effort.')
    B()
    T('Achieving this organizational state requires attention to both structural and cultural dimensions. Structurally, institutions must develop the infrastructure for continuous improvement: regular assessment cycles, functioning program review processes, accessible data dashboards, and governance mechanisms that ensure assessment findings inform decision-making [30]. Culturally, institutions must cultivate values of curiosity, humility, and collective responsibility\u2014values that make it acceptable to acknowledge challenges, learn from failures, and celebrate improvement rather than merely defending the status quo [51]. Leadership plays a critical role in modeling these values: when presidents, provosts, and deans publicly engage with institutional data, acknowledge areas needing improvement, and celebrate evidence of progress, they signal that quality improvement is a shared institutional commitment rather than a peripheral administrative function.')
    B()
    T('The integration of technology into continuous quality improvement processes represents an emerging dimension of institutional capacity. Contemporary institutions can leverage data analytics platforms, automated assessment tools, learning management system data, and integrated planning software to create real-time feedback systems that dramatically reduce the delay between evidence generation and responsive action [32, 52]. Rather than waiting for annual assessment reports or decennial self-studies, institutions can develop the capacity for continuous monitoring and rapid response\u2014adapting pedagogical approaches when early warning indicators suggest student difficulties, adjusting resource allocation when utilization data reveals inefficiencies, and piloting innovations when environmental scanning identifies emerging opportunities.')
    B(); B()

    # ---- FIGURE 3 ----
    P.append(img_para('rId5', 6096000, 3962400, 'Figure 3'))
    B()
    C('Figure 3. The Virtuous Cycle: Accountability, Learning, and Renewal form an', italic=True)
    C('interconnected system with Continuous Quality Improvement (CQI) at the center.', italic=True)
    B(); B()

    return P



def build_conclusion(P):
    """Conclusion and References."""
    B = lambda: P.append(para())
    H1 = lambda t: P.append(para(t, style='Heading1', bold=True))
    T = lambda t: P.append(para(t, indent=True))

    H1('Conclusion')
    B()
    T('This chapter has argued that accreditation in higher education is most powerfully understood not as a single function but as a dynamic cycle of three interconnected dimensions: accountability, learning, and institutional renewal. Each dimension is essential, and each depends upon the others for its full realization. Accountability provides the foundation of legitimacy and public trust upon which all else rests. Learning transforms accountability from a defensive posture into a genuine inquiry into institutional effectiveness. Renewal translates that learning into strategic action, adaptive capacity, and cultural transformation. When these three dimensions operate in concert, accreditation becomes far more than a regulatory mechanism\u2014it becomes a dynamic engine of institutional excellence.')
    B()
    T('The virtuous cycle that connects these dimensions can be simply stated: Accountability without learning is bureaucratic; learning without renewal is academic; renewal without accountability is unsustainable. An institution that merely documents its compliance without seeking to understand its performance is engaged in a hollow exercise. An institution that understands its strengths and weaknesses but fails to act on that understanding wastes the knowledge it has generated. And an institution that implements bold changes without grounding them in evidence and subjecting them to ongoing scrutiny builds on sand.')
    B()
    T('Achieving this ideal is neither simple nor automatic. It requires institutional leadership that values genuine inquiry over comfortable narratives, that creates psychological safety for honest self-assessment, and that demonstrates the courage to act on difficult findings. It requires a culture of trust in which faculty, staff, and administrators view quality improvement as a shared professional responsibility rather than an externally imposed burden. It requires accrediting bodies that balance their gatekeeping function with genuine commitment to institutional development, that resist the temptation to create ever-more-complex compliance requirements, and that evolve their own processes to remain relevant in a rapidly changing landscape.')
    B()
    T('Looking forward, the future of accreditation itself must evolve to better serve the renewal function in an era of boundaryless higher education. Accrediting bodies face their own imperative for transformation: they must develop standards and processes flexible enough to accommodate radical innovation while maintaining the public trust that is their fundamental asset. They must embrace technology-enhanced review processes that reduce burden while increasing insight. They must internationalize their perspectives to remain relevant in a global education marketplace. And they must build genuine partnerships with institutions\u2014relationships characterized by mutual respect and shared commitment to improvement rather than by the dynamics of surveillance and compliance. The evolution of accreditation must mirror the evolution it seeks to catalyze in institutions: moving from rigidity to agility, from standardization to contextualization, and from retrospective judgment to prospective partnership. This evolution is already underway, as several accrediting bodies experiment with risk-based review cycles, technology-mediated peer review, and competency-based standards that focus on demonstrated institutional capacity rather than input measures.')
    B()
    T('The opportunity before higher education is significant. By consciously elevating accreditation beyond compliance\u2014by embracing it as a framework for organizational learning and a catalyst for institutional renewal\u2014colleges and universities can transform what has often been experienced as a dreaded chore into their most powerful tool for thriving in a world of constant change. In doing so, they fulfill not only their obligations to external stakeholders but their deeper commitment to their own missions, their students, and the societies they serve.')
    B()
    T('The call to action is directed at all participants in the accreditation enterprise. Institutional leaders must champion a vision of accreditation that transcends compliance and embraces transformation. Faculty must engage as genuine partners in inquiry rather than reluctant participants in bureaucratic exercises. Accreditors must continue evolving their standards and processes to reward genuine improvement rather than merely policing minimum thresholds. And policymakers must recognize that the most productive accountability frameworks are those that simultaneously demand evidence of quality and create space for innovation, experimentation, and institutional self-determination. Together, these actors can realize accreditation\u2019s full potential as the powerful instrument of institutional renewal that higher education\u2019s boundaryless future demands.')
    B()
    T('Ultimately, the measure of accreditation\u2019s success is not whether institutions produce impressive self-study reports or survive site visits without sanctions. The measure is whether the process\u2014in its totality\u2014contributes to the creation of institutions that are more effective, more responsive, more equitable, and more capable of serving the diverse learners and complex societies that depend upon them. When accreditation achieves this aspiration, it fulfills its deepest purpose: not as a gatekeeper of minimum standards, but as a catalyst for the continuous pursuit of excellence in service to the public good. In the boundaryless landscape of twenty-first-century higher education, this catalytic function has never been more important, nor has the opportunity to realize it been greater. The institutions that will thrive in this new landscape are those that have internalized the disciplines of accountability, learning, and renewal\u2014not as separate obligations but as an integrated way of being that enables continuous adaptation and enduring excellence.')
    B(); B()

    # ===== REFERENCES =====
    H1('References')
    B()
    refs = [
        '[1] Eaton, J. S. (2015). An overview of U.S. accreditation. Council for Higher Education Accreditation.',
        '[2] Brittingham, B. (2009). Accreditation in the United States: How did we get to where we are? New Directions for Higher Education, 2009(145), 7\u201327. https://doi.org/10.1002/he.331',
        '[3] Spellings Commission. (2006). A test of leadership: Charting the future of U.S. higher education. U.S. Department of Education.',
        '[4] Kelchen, R. (2018). Higher education accountability. Johns Hopkins University Press.',
        '[5] Senge, P. M. (2006). The fifth discipline: The art and practice of the learning organization (Rev. ed.). Doubleday.',
        '[6] Argyris, C., & Sch\u00f6n, D. A. (1996). Organizational learning II: Theory, method, and practice. Addison-Wesley.',
        '[7] DiMaggio, P. J., & Powell, W. W. (1983). The iron cage revisited: Institutional isomorphism and collective rationality in organizational fields. American Sociological Review, 48(2), 147\u2013160. https://doi.org/10.2307/2095101',
        '[8] Deming, W. E. (1993). The new economics for industry, government, education. MIT Press.',
        '[9] Kezar, A. (2018). How colleges change: Understanding, leading, and enacting change (2nd ed.). Routledge.',
        '[10] Trow, M. (1996). Trust, markets, and accountability in higher education: A comparative perspective. Higher Education Policy, 9(4), 309\u2013324. https://doi.org/10.1016/S0952-8733(96)00029-3',
        '[11] Ewell, P. T. (2009). Assessment, accountability, and improvement: Revisiting the tension (NILOA Occasional Paper No. 1). National Institute for Learning Outcomes Assessment.',
        '[12] U.S. Government Accountability Office. (2010). For-profit colleges: Undercover testing finds colleges encouraged fraud and engaged in deceptive and questionable marketing practices (GAO-10-948T). U.S. GAO.',
        '[13] Hazelkorn, E. (2015). Rankings and the reshaping of higher education: The battle for world-class excellence (2nd ed.). Palgrave Macmillan.',
        '[14] Carnevale, A. P., Cheah, B., & Wenzinger, E. (2020). The college payoff: More education doesn\u2019t always mean more earnings. Georgetown University Center on Education and the Workforce.',
        '[15] U.S. Department of Education. (2022). Federal student aid annual report. https://studentaid.gov/data-center/student/portfolio',
        '[16] Stensaker, B., & Harvey, L. (2011). Accountability in higher education: Global perspectives on trust and power. Routledge.',
        '[17] Herzberg, F. (1966). Work and the nature of man. World Publishing Company.',
        '[18] Middle States Commission on Higher Education. (2015). Standards for accreditation and requirements of affiliation (13th ed.). MSCHE.',
        '[19] Cochrane, D., & Szabo-Kubitz, L. (2016). On the verge: Costs and tradeoffs facing community college students. The Institute for College Access & Success.',
        '[20] Council for Higher Education Accreditation. (2019). CHEA at a glance. https://www.chea.org/chea-glance',
        '[21] Higher Learning Commission. (2020). Criteria for accreditation. https://www.hlcommission.org/Policies/criteria-and-core-components.html',
        '[22] Power, M. (1997). The audit society: Rituals of verification. Oxford University Press.',
        '[23] Morphew, C. C., & Hartley, M. (2006). Mission statements: A thematic analysis of rhetoric across institutional type. The Journal of Higher Education, 77(3), 456\u2013471. https://doi.org/10.1353/jhe.2006.0023',
        '[24] Lubinescu, E. S., Ratcliff, J. L., & Gaffney, M. A. (2001). Two continuums collide: Accreditation and assessment. New Directions for Higher Education, 2001(113), 5\u201321. https://doi.org/10.1002/he.1',
        '[25] Kells, H. R. (1995). Self-study processes: A guide to self-evaluation in higher education (4th ed.). American Council on Education/Oryx Press.',
        '[26] Edmondson, A. (1999). Psychological safety and learning behavior in work teams. Administrative Science Quarterly, 44(2), 350\u2013383. https://doi.org/10.2307/2666999',
        '[27] Bresciani, M. J., Gardner, M. M., & Hickmott, J. (2009). Demonstrating student success: A practical guide to outcomes-based assessment of learning and development in student affairs. Stylus Publishing.',
        '[28] Schein, E. H. (2010). Organizational culture and leadership (4th ed.). Jossey-Bass.',
        '[29] Swing, R. L., & Ross, L. E. (2016). A new vision for institutional research. Change: The Magazine of Higher Learning, 48(2), 6\u201313. https://doi.org/10.1080/00091383.2016.1163132',
        '[30] Volkwein, J. F., Liu, Y., & Woodell, J. (2012). The structure and functions of institutional research offices. In R. D. Howard, G. W. McLaughlin, & W. E. Knight (Eds.), The handbook of institutional research (pp. 22\u201339). Jossey-Bass.',
        '[31] Suskie, L. (2018). Assessing student learning: A common sense guide (3rd ed.). Jossey-Bass.',
        '[32] Siemens, G., & Long, P. (2011). Penetrating the fog: Analytics in learning and education. EDUCAUSE Review, 46(5), 30\u201332.',
        '[33] Banta, T. W., & Palomba, C. A. (2015). Assessment essentials: Planning, implementing, and improving assessment in higher education (2nd ed.). Jossey-Bass.',
        '[34] Kezar, A., & Eckel, P. D. (2002). The effect of institutional culture on change strategies in higher education: Universal principles or culturally responsive concepts? The Journal of Higher Education, 73(4), 435\u2013460. https://doi.org/10.1353/jhe.2002.0038',
        '[35] Janis, I. L. (1982). Groupthink: Psychological studies of policy decisions and fiascoes (2nd ed.). Houghton Mifflin.',
        '[36] Kis, V. (2005). Quality assurance in tertiary education: Current practices in OECD countries and a literature review on potential effects. OECD Thematic Review of Tertiary Education.',
        '[37] Harvey, L. (2004). The power of accreditation: Views of academics. Journal of Higher Education Policy and Management, 26(2), 207\u2013223. https://doi.org/10.1080/1360080042000218267',
        '[38] Kinzie, J. (2010). Perspectives from campus leaders on the current state of student learning outcomes assessment. Assessment Update, 22(5), 1\u201315. https://doi.org/10.1002/au.225',
        '[39] Welsh, J. F., & Metcalf, J. (2003). Faculty and administrative support for institutional effectiveness activities: A bridge across the chasm? The Journal of Higher Education, 74(4), 445\u2013468. https://doi.org/10.1353/jhe.2003.0032',
        '[40] Baker, R. L. (2004). Keystones of regional accreditation: Intentions, outcomes, and sustainability. In P. Hernon, R. E. Dugan, & C. Schwartz (Eds.), Revisiting outcomes assessment in higher education (pp. 1\u201325). Libraries Unlimited.',
        '[41] Dickeson, R. C. (2010). Prioritizing academic programs and services: Reallocating resources to achieve strategic balance (2nd ed.). Jossey-Bass.',
        '[42] Terenzini, P. T. (2013). \u201cOn the nature of institutional research\u201d revisited: Plus \u00e7a change...? Research in Higher Education, 54(2), 137\u2013148. https://doi.org/10.1007/s11162-012-9274-3',
        '[43] Carey, K. (2012). A future of competency-based higher education. EDUCAUSE Review, 47(5), 68\u201369.',
        '[44] Laitinen, A. (2012). Cracking the credit hour. New America Foundation.',
        '[45] Pusser, B., Breneman, D. W., Gansneder, B. M., Kohl, K. J., Levin, J. S., Milam, J. H., & Turner, S. E. (2007). Returning to learning: Adults\u2019 success in college is key to America\u2019s future. Lumina Foundation.',
        '[46] Baum, S., Ma, J., & Payea, K. (2013). Education pays 2013: The benefits of higher education for individuals and society. The College Board.',
        '[47] Dill, D. D. (1999). Academic accountability and university adaptation: The architecture of an academic learning organization. Higher Education, 38(2), 127\u2013154. https://doi.org/10.1023/A:1003762420723',
        '[48] Juran, J. M. (1989). Juran on leadership for quality: An executive handbook. Free Press.',
        '[49] Seymour, D. T. (1992). On Q: Causing quality in higher education. Macmillan.',
        '[50] Freed, J. E., Klugman, M. R., & Fife, J. D. (1997). A culture for academic excellence: Implementing the quality principles in higher education. ASHE-ERIC Higher Education Report, 25(1). ERIC Clearinghouse on Higher Education.',
        '[51] Birnbaum, R. (1988). How colleges work: The cybernetics of academic organization and leadership. Jossey-Bass.',
        '[52] Norris, D. M., & Baer, L. L. (2013). Building organizational capacity for analytics. EDUCAUSE.',
    ]
    for r in refs:
        P.append(ref_para(r))

    return P



# ===========================================================================
# SECTION D: DOCX ASSEMBLY AND OUTPUT
# ===========================================================================

def assemble_and_save(output_path):
    """Assemble complete manuscript .docx with figures, tables, and text."""
    print("Generating figures...")
    fig1 = make_figure1()
    fig2 = make_figure2()
    fig3 = make_figure3()

    print("Building manuscript text...")
    P = build_manuscript()
    build_section2(P)
    build_section3(P)
    build_conclusion(P)

    # Count words
    word_count = 0
    for el in P:
        for t_el in el.iter(n('w','t')):
            if t_el.text:
                word_count += len(t_el.text.split())
    print(f"Word count: {word_count}")

    # Build document.xml
    root = Element(n('w','document'))
    root.set('xmlns:w', NS['w']); root.set('xmlns:r', NS['r'])
    root.set('xmlns:wp', NS['wp']); root.set('xmlns:a', NS['a']); root.set('xmlns:pic', NS['pic'])
    body = SubElement(root, n('w','body'))
    for p in P:
        body.append(p)
    sectPr = SubElement(body, n('w','sectPr'))
    pgSz = SubElement(sectPr, n('w','pgSz')); pgSz.set(n('w','w'),'12240'); pgSz.set(n('w','h'),'15840')
    pgMar = SubElement(sectPr, n('w','pgMar'))
    pgMar.set(n('w','top'),'1440'); pgMar.set(n('w','right'),'1440')
    pgMar.set(n('w','bottom'),'1440'); pgMar.set(n('w','left'),'1440')
    pgMar.set(n('w','header'),'720'); pgMar.set(n('w','footer'),'720')
    doc_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(root, encoding='unicode')

    # Content Types
    ct = Element('Types'); ct.set('xmlns','http://schemas.openxmlformats.org/package/2006/content-types')
    for ext, ctype in [('rels','application/vnd.openxmlformats-package.relationships+xml'),('xml','application/xml'),('png','image/png')]:
        d = SubElement(ct,'Default'); d.set('Extension',ext); d.set('ContentType',ctype)
    for pn, ctype in [('/word/document.xml','application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'),
                      ('/word/styles.xml','application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml'),
                      ('/word/settings.xml','application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml')]:
        o = SubElement(ct,'Override'); o.set('PartName',pn); o.set('ContentType',ctype)
    ct_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(ct, encoding='unicode')

    # _rels/.rels
    rels = Element('Relationships'); rels.set('xmlns','http://schemas.openxmlformats.org/package/2006/relationships')
    r1 = SubElement(rels,'Relationship'); r1.set('Id','rId1'); r1.set('Type','http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument'); r1.set('Target','word/document.xml')
    rels_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(rels, encoding='unicode')

    # word/_rels/document.xml.rels
    wrels = Element('Relationships'); wrels.set('xmlns','http://schemas.openxmlformats.org/package/2006/relationships')
    for rid, rtype, target in [
        ('rId1','http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles','styles.xml'),
        ('rId2','http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings','settings.xml'),
        ('rId3','http://schemas.openxmlformats.org/officeDocument/2006/relationships/image','media/figure1.png'),
        ('rId4','http://schemas.openxmlformats.org/officeDocument/2006/relationships/image','media/figure2.png'),
        ('rId5','http://schemas.openxmlformats.org/officeDocument/2006/relationships/image','media/figure3.png'),
    ]:
        r = SubElement(wrels,'Relationship'); r.set('Id',rid); r.set('Type',rtype); r.set('Target',target)
    wrels_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(wrels, encoding='unicode')

    # Styles
    sty = Element(n('w','styles')); sty.set('xmlns:w',NS['w']); sty.set('xmlns:r',NS['r'])
    dd = SubElement(sty, n('w','docDefaults'))
    rpd = SubElement(dd, n('w','rPrDefault')); rpr = SubElement(rpd, n('w','rPr'))
    rf = SubElement(rpr, n('w','rFonts')); rf.set(n('w','ascii'),'Times New Roman'); rf.set(n('w','hAnsi'),'Times New Roman'); rf.set(n('w','cs'),'Times New Roman')
    sz = SubElement(rpr, n('w','sz')); sz.set(n('w','val'),'24')
    szc = SubElement(rpr, n('w','szCs')); szc.set(n('w','val'),'24')
    ppd = SubElement(dd, n('w','pPrDefault')); ppr = SubElement(ppd, n('w','pPr'))
    sp = SubElement(ppr, n('w','spacing')); sp.set(n('w','line'),'480'); sp.set(n('w','lineRule'),'auto')
    for sid, sname, is_bold, szv, ctr in [('Normal','Normal',False,'24',False),('Heading1','heading 1',True,'28',True),('Heading2','heading 2',True,'24',False)]:
        s = SubElement(sty, n('w','style')); s.set(n('w','type'),'paragraph'); s.set(n('w','styleId'),sid)
        nm = SubElement(s, n('w','name')); nm.set(n('w','val'),sname)
        if ctr:
            sppr = SubElement(s, n('w','pPr')); jc = SubElement(sppr, n('w','jc')); jc.set(n('w','val'),'center')
        if is_bold:
            srpr = SubElement(s, n('w','rPr')); SubElement(srpr, n('w','b'))
            ssz = SubElement(srpr, n('w','sz')); ssz.set(n('w','val'),szv)
            sszc = SubElement(srpr, n('w','szCs')); sszc.set(n('w','val'),szv)
    sty_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(sty, encoding='unicode')

    # Settings
    settings = Element(n('w','settings')); settings.set('xmlns:w',NS['w']); settings.set('xmlns:r',NS['r'])
    set_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + tostring(settings, encoding='unicode')

    # Write .docx
    print("Writing .docx...")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', ct_xml)
        zf.writestr('_rels/.rels', rels_xml)
        zf.writestr('word/_rels/document.xml.rels', wrels_xml)
        zf.writestr('word/document.xml', doc_xml)
        zf.writestr('word/styles.xml', sty_xml)
        zf.writestr('word/settings.xml', set_xml)
        zf.writestr('word/media/figure1.png', fig1)
        zf.writestr('word/media/figure2.png', fig2)
        zf.writestr('word/media/figure3.png', fig3)

    size = os.path.getsize(output_path)
    print(f"\n{'='*60}")
    print(f"MANUSCRIPT GENERATED SUCCESSFULLY")
    print(f"{'='*60}")
    print(f"File: {output_path}")
    print(f"Size: {size:,} bytes")
    print(f"Word count: ~{word_count} words")
    print(f"References: 52 (numbered [1]-[52] in serial order)")
    print(f"Tables: 3 (one per section)")
    print(f"Figures: 3 (one per section, embedded PNG)")
    print(f"Format: Times New Roman 12pt, double-spaced")
    print(f"{'='*60}")


if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'Chapter_Accreditation_Accountability_Learning_Renewal.docx')
    assemble_and_save(out)
