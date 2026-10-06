#!/usr/bin/env python3
"""
Generate 7 real figures from the pure-Python Carreau-EMHD solver.
No matplotlib: curves are rasterised directly to PNG via zlib/struct.
Outputs carreau_figures/fig1..fig7.png
"""
import os, struct, zlib, math
from carreau_solver import params, properties, solve

OUTDIR = "carreau_figures"
os.makedirs(OUTDIR, exist_ok=True)

W, H = 760, 520          # image size
L, Rm, T, Bm = 90, 30, 54, 60   # margins (left,right,top,bottom)
PW, PH = W - L - Rm, H - T - Bm  # plot area

WHITE=(255,255,255); BLACK=(20,20,20); GREY=(170,170,170); LGREY=(225,225,225)
PALETTE=[(31,119,180),(214,39,40),(44,160,44),(148,103,189),(255,127,14),(23,190,207)]

def blank():
    return [[WHITE[:] for _ in range(W)] for _ in range(H)]

def setpx(img,x,y,c):
    x=int(x); y=int(y)
    if 0<=x<W and 0<=y<H: img[y][x]=c

def line(img,x0,y0,x1,y1,c,wd=2):
    x0,y0,x1,y1=int(round(x0)),int(round(y0)),int(round(x1)),int(round(y1))
    dx=abs(x1-x0); dy=-abs(y1-y0); sx=1 if x0<x1 else -1; sy=1 if y0<y1 else -1
    err=dx+dy
    while True:
        for ox in range(-(wd//2),wd//2+1):
            for oy in range(-(wd//2),wd//2+1):
                setpx(img,x0+ox,y0+oy,c)
        if x0==x1 and y0==y1: break
        e2=2*err
        if e2>=dy: err+=dy; x0+=sx
        if e2<=dx: err+=dx; y0+=sy

# minimal 5x7 bitmap font (upper, digits, few symbols)
FONT={
 '0':["01110","10001","10011","10101","11001","10001","01110"],
 '1':["00100","01100","00100","00100","00100","00100","01110"],
 '2':["01110","10001","00001","00010","00100","01000","11111"],
 '3':["11111","00010","00100","00010","00001","10001","01110"],
 '4':["00010","00110","01010","10010","11111","00010","00010"],
 '5':["11111","10000","11110","00001","00001","10001","01110"],
 '6':["00110","01000","10000","11110","10001","10001","01110"],
 '7':["11111","00001","00010","00100","01000","01000","01000"],
 '8':["01110","10001","10001","01110","10001","10001","01110"],
 '9':["01110","10001","10001","01111","00001","00010","01100"],
 '.':["00000","00000","00000","00000","00000","00110","00110"],
 '-':["00000","00000","00000","11111","00000","00000","00000"],
 '=':["00000","00000","11111","00000","11111","00000","00000"],
 ' ':["00000"]*7,
 'f':["00110","01001","01000","11100","01000","01000","01000"],
 "'":["00100","00100","00100","00000","00000","00000","00000"],
 '(':["00010","00100","01000","01000","01000","00100","00010"],
 ')':["01000","00100","00010","00010","00010","00100","01000"],
 'n':["00000","00000","10110","11001","10001","10001","10001"],
 'N':["10001","11001","10101","10011","10001","10001","10001"],
 's':["01111","10000","10000","01110","00001","00001","11110"],
 'B':["11110","10001","10001","11110","10001","10001","11110"],
 'e':["01110","10001","10001","11111","10000","10001","01110"],
 'S':["01111","10000","10000","01110","00001","00001","11110"],
 'q':["01111","10001","10001","01111","00001","00001","00001"],
 'W':["10001","10001","10001","10101","10101","11011","10001"],
 'M':["10001","11011","10101","10101","10001","10001","10001"],
 'R':["11110","10001","10001","11110","10100","10010","10001"],
 'd':["00001","00001","01101","10011","10001","10001","01111"],
 'E':["11111","10000","10000","11110","10000","10000","11111"],
 'c':["01110","10001","10000","10000","10000","10001","01110"],
 'r':["00000","00000","10110","11001","10000","10000","10000"],
 'C':["01110","10001","10000","10000","10000","10001","01110"],
 'h':["10000","10000","10110","11001","10001","10001","10001"],
 'i':["00100","00000","01100","00100","00100","00100","01110"],
 't':["01000","01000","11110","01000","01000","01001","00110"],
 'a':["00000","00000","01110","00001","01111","10001","01111"],
 'p':["00000","00000","11110","10001","11110","10000","10000"],
 'o':["00000","00000","01110","10001","10001","10001","01110"],
 'l':["01100","00100","00100","00100","00100","00100","01110"],
 'u':["00000","00000","10001","10001","10001","10011","01101"],
 'm':["00000","00000","11010","10101","10101","10101","10101"],
 'b':["10000","10000","10110","11001","10001","10001","11110"],
 'g':["00000","01111","10001","10001","01111","00001","01110"],
 'A':["01110","10001","10001","11111","10001","10001","10001"],
 'x':["00000","00000","10001","01010","00100","01010","10001"],
 'Q':["01110","10001","10001","10001","10101","10010","01101"],
 'T':["11111","00100","00100","00100","00100","00100","00100"],
 'P':["11110","10001","10001","11110","10000","10000","10000"],
 'U':["10001","10001","10001","10001","10001","10001","01110"],
 'v':["00000","00000","10001","10001","10001","01010","00100"],
 'w':["00000","00000","10001","10001","10101","10101","01010"],
 'y':["00000","10001","10001","01111","00001","00001","01110"],
 'z':["00000","00000","11111","00010","00100","01000","11111"],
 '/':["00001","00010","00100","00100","01000","10000","10000"],
 ',':["00000","00000","00000","00000","00110","00110","01100"],
}
def text(img,x,y,s,c=BLACK,sc=2):
    cx=x
    for ch in s:
        g=FONT.get(ch,FONT[' '])
        for row in range(7):
            bits=g[row] if row<len(g) else "00000"
            for col in range(len(bits)):
                if bits[col]=='1':
                    for dx in range(sc):
                        for dy in range(sc):
                            setpx(img,cx+col*sc+dx,y+row*sc+dy,c)
        cx += (len(g[0]) if g else 5)*sc + sc
    return cx

def fmt(v):
    s=("%.2f"%v).rstrip('0').rstrip('.')
    return s if s not in ('','-0') else '0'

def plot(fname, series, xlabel, ylabel, title, xr=(0,1), yr=None, legend_title=None):
    img=blank()
    xs_all=[p[0] for s in series for p in s['pts']]
    ys_all=[p[1] for s in series for p in s['pts']]
    x0,x1=xr
    if yr is None:
        ymin,ymax=min(ys_all),max(ys_all); pad=0.08*((ymax-ymin) or 1); yr=(ymin-pad,ymax+pad)
    y0,y1=yr
    def X(v): return L+ (v-x0)/(x1-x0)*PW
    def Y(v): return T+ (1-(v-y0)/(y1-y0))*PH
    # grid + ticks
    for i in range(6):
        gx=L+PW*i/5
        line(img,gx,T,gx,T+PH,LGREY,1)
        text(img,gx-10,T+PH+8,fmt(x0+(x1-x0)*i/5),BLACK,2)
    for i in range(6):
        gy=T+PH*i/5
        line(img,L,gy,L+PW,gy,LGREY,1)
        text(img,8,gy-6,fmt(y1-(y1-y0)*i/5),BLACK,2)
    # axes
    line(img,L,T,L,T+PH,BLACK,2); line(img,L,T+PH,L+PW,T+PH,BLACK,2)
    # curves
    for k,s in enumerate(series):
        c=PALETTE[k%len(PALETTE)]
        pts=s['pts']
        for j in range(len(pts)-1):
            line(img,X(pts[j][0]),Y(pts[j][1]),X(pts[j+1][0]),Y(pts[j+1][1]),c,2)
    # title & labels
    text(img,L,16,title,BLACK,2)
    text(img,L+PW//2-40,T+PH+30,xlabel,BLACK,2)
    # ylabel (vertical-ish: just put at top-left of axis)
    text(img,10,T-18,ylabel,BLACK,2)
    # legend
    ly=T+10
    if legend_title: text(img,L+PW-150,ly,legend_title,BLACK,2); ly+=20
    for k,s in enumerate(series):
        c=PALETTE[k%len(PALETTE)]
        line(img,L+PW-150,ly+6,L+PW-120,ly+6,c,3)
        text(img,L+PW-112,ly,s['label'],BLACK,2); ly+=20
    write_png(os.path.join(OUTDIR,fname),img)
    print("wrote",fname)

def write_png(path,img):
    raw=b''
    for row in img:
        raw+=b'\x00'+b''.join(struct.pack('BBB',*px) for px in row)
    def chunk(t,d):
        c=t+d; return struct.pack('>I',len(d))+c+struct.pack('>I',zlib.crc32(c)&0xffffffff)
    sig=b'\x89PNG\r\n\x1a\n'
    ihdr=chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))
    idat=chunk(b'IDAT',zlib.compress(raw,9))
    iend=chunk(b'IEND',b'')
    with open(path,'wb') as fp: fp.write(sig+ihdr+idat+iend)

def profile(ov, idx):
    """return list of (eta, y[idx]) using N=200 trajectory."""
    P=params(**ov); pr=properties(P['phi1'],P['phi2'])
    s,traj,nrm=solve(P,pr,N=200)
    return [(e, y[idx]) for e,y in traj]

def Ns_profile(ov):
    """compute Ns(eta) from trajectory using Eq.(48)."""
    P=params(**ov); pr=properties(P['phi1'],P['phi2'])
    s,traj,nrm=solve(P,pr,N=200)
    a_mu,a_sig,a_k=pr['a_mu'],pr['a_sig'],pr['a_k']
    Br,Om,M,Ee=1.0,1.0,P['M'],P['Ee']
    Lam,zeta,We,n,Rd,thr=0.5,1.0,P['We'],P['n'],P['Rd'],P['thr']
    out=[]; 
    for e,y in traj:
        fp,fpp,th,thp,php=y[1],y[2],y[4],y[5],y[7]
        F=1+(thr-1)*th
        NHT=(a_k+4/3*Rd*F**3)*thp*thp
        NFF=(a_mu*Br/Om)*fpp*fpp*(1+We*We*fpp*fpp)**((n-1)/2)
        NJ =(a_sig*Br*M/Om)*(fp-Ee)**2
        NDD=Lam*(zeta/Om)**2*php*php+Lam*(zeta/Om)*thp*php
        Ns=NHT+NFF+NJ+NDD
        Be=(NHT+NDD)/Ns if Ns>0 else 0
        out.append((e,Ns,Be))
    return out

# ---------- Figure 1: schematic ----------
def fig1():
    img=blank()
    # two plates
    line(img,120,120,640,120,BLACK,4)   # upper plate
    line(img,120,400,640,400,BLACK,4)   # lower plate
    text(img,150,96,"Upper plate moves down vh = Sq/2 (squeezing)",BLACK,2)
    text(img,150,410,"Lower plate stretches Ue = ax/(1-gamma t)",BLACK,2)
    # gap arrows
    for xx in range(170,641,80):
        line(img,xx,130,xx,160,PALETTE[1],2)  # down arrows (squeeze)
        line(img,xx-4,152,xx,160,PALETTE[1],2); line(img,xx+4,152,xx,160,PALETTE[1],2)
    # stretch arrows at lower plate
    for xx in range(170,641,80):
        line(img,xx,390,xx+28,390,PALETTE[2],2)
        line(img,xx+20,386,xx+28,390,PALETTE[2],2); line(img,xx+20,394,xx+28,390,PALETTE[2],2)
    # fields
    text(img,150,230,"B(t) transverse (+y)   E(t) aligned (+z)",PALETTE[3],2)
    text(img,150,260,"Carreau hybrid nanofluid AA7072-AA7075 / methanol",PALETTE[0],2)
    text(img,150,290,"Darcy-Forchheimer porous channel",BLACK,2)
    # h(t)
    line(img,100,120,100,400,PALETTE[5],2); text(img,60,250,"h(t)",PALETTE[5],2)
    # eta axis
    line(img,660,120,660,400,BLACK,2)
    text(img,676,118,"eta=1",BLACK,2); text(img,676,392,"eta=0",BLACK,2)
    text(img,150,52,"Figure 1  Schematic of EMHD squeezing flow",BLACK,2)
    write_png(os.path.join(OUTDIR,"fig1.png"),img); print("wrote fig1.png")

fig1()

# ---------- Figure 2: f'(eta) vs Sq ----------
s2=[{'label':"Sq="+fmt(Sq),'pts':profile(dict(Sq=Sq),1)} for Sq in (0.2,0.4,0.6,0.8)]
plot("fig2.png",s2,"eta","f'(eta)","Figure 2  Velocity f'(eta) vs squeezing Sq",legend_title=None)

# ---------- Figure 3: f'(eta) vs We (and M) ----------
s3=[{'label':"We="+fmt(We),'pts':profile(dict(We=We),1)} for We in (0.5,1.0,2.0)]
s3+=[{'label':"M="+fmt(M),'pts':profile(dict(M=M),1)} for M in (2.0,)]
plot("fig3.png",s3,"eta","f'(eta)","Figure 3  Velocity f'(eta) vs We and M")

# ---------- Figure 4: theta(eta) vs Rd & Ec ----------
s4=[{'label':"Rd="+fmt(Rd),'pts':profile(dict(Rd=Rd),4)} for Rd in (0.2,0.5,1.0)]
s4+=[{'label':"Ec="+fmt(Ec),'pts':profile(dict(Ec=Ec),4)} for Ec in (0.6,)]
plot("fig4.png",s4,"eta","theta(eta)","Figure 4  Temperature theta(eta) vs Rd and Ec")

# ---------- Figure 5: Ns(eta) vs Br & M ----------
s5=[]
for Br in (0.5,1.0,1.5):
    pts=[(e,ns) for (e,ns,be) in Ns_profile(dict())]  # Br scales linearly in Ns; recompute properly
# recompute with Br in formula
def Ns_with(ov, Br):
    P=params(**ov); pr=properties(P['phi1'],P['phi2'])
    s,traj,nrm=solve(P,pr,N=200)
    a_mu,a_sig,a_k=pr['a_mu'],pr['a_sig'],pr['a_k']
    Om,M,Ee=1.0,P['M'],P['Ee']; Lam,zeta,We,n,Rd,thr=0.5,1.0,P['We'],P['n'],P['Rd'],P['thr']
    out=[]
    for e,y in traj:
        fp,fpp,th,thp,php=y[1],y[2],y[4],y[5],y[7]; F=1+(thr-1)*th
        NHT=(a_k+4/3*Rd*F**3)*thp*thp
        NFF=(a_mu*Br/Om)*fpp*fpp*(1+We*We*fpp*fpp)**((n-1)/2)
        NJ=(a_sig*Br*M/Om)*(fp-Ee)**2
        NDD=Lam*(zeta/Om)**2*php*php+Lam*(zeta/Om)*thp*php
        Ns=NHT+NFF+NJ+NDD; Be=(NHT+NDD)/Ns if Ns>0 else 0
        out.append((e,Ns,Be))
    return out
s5=[{'label':"Br="+fmt(Br),'pts':[(e,ns) for e,ns,_ in Ns_with(dict(),Br)]} for Br in (0.5,1.0,1.5)]
s5+=[{'label':"M=2",'pts':[(e,ns) for e,ns,_ in Ns_with(dict(M=2.0),1.0)]}]
plot("fig5.png",s5,"eta","Ns(eta)","Figure 5  Entropy number Ns(eta) vs Br and M")

# ---------- Figure 6: Be(eta) vs Rd & Br ----------
s6=[{'label':"Rd="+fmt(Rd),'pts':[(e,be) for e,ns,be in Ns_with(dict(Rd=Rd),1.0)]} for Rd in (0.2,0.5,1.0)]
s6+=[{'label':"Br=1.5",'pts':[(e,be) for e,ns,be in Ns_with(dict(),1.5)]}]
plot("fig6.png",s6,"eta","Be(eta)","Figure 6  Bejan number Be(eta) vs Rd and Br",yr=(0,1))

# ---------- Figure 7: Cf, Nu, Sh vs phi ----------
phis=[0.0,0.01,0.02,0.03,0.04,0.05]
cf=[];nu=[];sh=[]
for p in phis:
    P=params(phi1=p,phi2=p); pr=properties(p,p)
    s,traj,nrm=solve(P,pr,N=200); y=traj[-1][1]
    F=1+(P['thr']-1)*y[4]
    Cf=pr['a_mu']*y[2]*(1+P['We']**2*y[2]**2)**((P['n']-1)/2)
    Nu=-(pr['a_k']+4/3*P['Rd']*F**3)*y[5]
    Sh=-y[7]
    cf.append((p,Cf)); nu.append((p,Nu)); sh.append((p,Sh))
s7=[{'label':"Re^.5 Cf",'pts':cf},{'label':"Re^-.5 Nu",'pts':nu},{'label':"Re^-.5 Sh",'pts':sh}]
plot("fig7.png",s7,"phi","quantity","Figure 7  Cf, Nu, Sh vs volume fraction phi",xr=(0,0.05))

print("ALL FIGURES DONE")
