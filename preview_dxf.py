#!/usr/bin/env python3
"""Render the hand-written DXF to a PNG for visual verification (stdlib only)."""
import zlib, struct, math
from generate_ckd_figures import FONT

DXF = '/projects/sandbox/AMMAN/Welding_Specimen_Extraction.dxf'
PNG = '/projects/sandbox/AMMAN/_dxf_preview.png'

ACI = {1:(220,0,0),2:(210,210,0),3:(0,170,70),4:(0,175,215),5:(20,40,210),
       6:(200,0,160),7:(10,10,10),8:(120,120,120),30:(240,140,0),214:(140,55,175)}

def parse(path):
    lines=open(path).read().split('\n')
    i=0; ents=[]
    # jump to ENTITIES
    while i<len(lines) and not(lines[i]=='2' and i+1<len(lines) and lines[i+1]=='ENTITIES'):
        i+=1
    pairs=[]
    i+=2
    while i+1<len(lines):
        pairs.append((lines[i], lines[i+1])); i+=2
    # split into entities on code 0
    cur=None
    for code,val in pairs:
        if code=='0':
            if cur: ents.append(cur)
            cur={'type':val}
            if val in ('ENDSEC','EOF'): cur=None
        elif cur is not None:
            cur.setdefault(code,[]).append(val)
    return ents

class C:
    def __init__(s,w,h): s.w=w;s.h=h;s.px=bytearray(b'\xff'*w*h*3)
    def pt(s,x,y,c):
        x=int(x);y=int(y)
        if 0<=x<s.w and 0<=y<s.h:
            i=(y*s.w+x)*3; s.px[i:i+3]=bytes(c)
    def line(s,x0,y0,x1,y1,c,t=1):
        x0,y0,x1,y1=int(x0),int(y0),int(x1),int(y1)
        dx=abs(x1-x0);dy=-abs(y1-y0);sx=1 if x0<x1 else -1;sy=1 if y0<y1 else -1;e=dx+dy
        while True:
            for ox in range(t):
                for oy in range(t): s.pt(x0+ox,y0+oy,c)
            if x0==x1 and y0==y1:break
            e2=2*e
            if e2>=dy:e+=dy;x0+=sx
            if e2<=dx:e+=dx;y0+=sy
    def fillpoly(s,pts,c):
        ys=[p[1] for p in pts]; y0=int(min(ys));y1=int(max(ys))
        for y in range(y0,y1+1):
            xs=[]
            for j in range(len(pts)):
                ax,ay=pts[j];bx,by=pts[(j+1)%len(pts)]
                if (ay<=y<by) or (by<=y<ay):
                    xs.append(ax+(bx-ax)*(y-ay)/(by-ay))
            xs.sort()
            for k in range(0,len(xs)-1,2):
                for x in range(int(xs[k]),int(xs[k+1])+1): s.pt(x,y,c)
    def ch(s,x,y,g,c,sc):
        for ry,row in enumerate(g):
            for rx,b in enumerate(row):
                if b=='1':
                    for a in range(sc):
                        for d in range(sc): s.pt(x+rx*sc+a,y+ry*sc+d,c)
    def text(s,x,y,sstr,c,sc,center,rot):
        sstr=sstr.upper().replace('%%D','DEG')
        cw=(5+1)*sc
        if rot==90:
            tot=len(sstr)*cw
            yy=y+tot//2
            for chx in sstr:
                s.ch(x- (7*sc)//2, yy-cw, FONT.get(chx,FONT[' ']), c, sc); yy-=cw
            return
        tot=len(sstr)*cw
        xx=x-tot//2 if center else x
        for chx in sstr:
            s.ch(xx, y-(7*sc)//2, FONT.get(chx,FONT[' ']), c, sc); xx+=cw
    def save(s,p):
        raw=bytearray()
        for y in range(s.h):
            raw.append(0); raw+=s.px[y*s.w*3:(y+1)*s.w*3]
        def ck(t,d):
            cc=t+d; return struct.pack('>I',len(d))+cc+struct.pack('>I',zlib.crc32(cc)&0xffffffff)
        png=b'\x89PNG\r\n\x1a\n'+ck(b'IHDR',struct.pack('>IIBBBBB',s.w,s.h,8,2,0,0,0))
        png+=ck(b'IDAT',zlib.compress(bytes(raw),9))+ck(b'IEND',b'')
        open(p,'wb').write(png)

ents=parse(DXF)
xmin,ymin,xmax,ymax=-45,-125,325,405
sc=2.0; marg=20
W=int((xmax-xmin)*sc)+2*marg; H=int((ymax-ymin)*sc)+2*marg
cv=C(W,H)
def mx(x): return (float(x)-xmin)*sc+marg
def my(y): return H-((float(y)-ymin)*sc+marg)
for e in ents:
    t=e.get('type'); col=ACI.get(int(e.get('62',['7'])[0]),(0,0,0))
    if t=='LINE':
        cv.line(mx(e['10'][0]),my(e['20'][0]),mx(e['11'][0]),my(e['21'][0]),col,1)
    elif t=='SOLID':
        p=[(mx(e['10'][0]),my(e['20'][0])),(mx(e['11'][0]),my(e['21'][0])),
           (mx(e['13'][0]),my(e['23'][0])),(mx(e['12'][0]),my(e['22'][0]))]
        cv.fillpoly(p,col)
    elif t=='ARC':
        cxp=float(e['10'][0]);cyp=float(e['20'][0]);r=float(e['40'][0])
        a0=math.radians(float(e['50'][0]));a1=math.radians(float(e['51'][0]))
        steps=24;prev=None
        for s_ in range(steps+1):
            a=a0+(a1-a0)*s_/steps; pxx=mx(cxp+r*math.cos(a));pyy=my(cyp+r*math.sin(a))
            if prev: cv.line(prev[0],prev[1],pxx,pyy,col,1)
            prev=(pxx,pyy)
    elif t=='TEXT':
        h=float(e['40'][0]); s_=e['1'][0]; rot=int(float(e.get('50',['0'])[0]))
        center=e.get('72',['0'])[0]=='1'
        scl=max(1,int(h*sc/7))
        cv.text(mx(e['10'][0]),my(e['20'][0]),s_,col,scl,center,rot)
cv.save(PNG)
print('wrote',PNG,W,'x',H)
