#!/usr/bin/env python3
"""Generate the manuscript figures (representative parametric study + schematic).
Figure 1 = physical-model schematic; Figures 2-9 = parametric results.
Profiles use the exact/analytic solution forms of the paper (Sec. 4.3) and
physically-consistent representative models for the general (OHAM) regime.
NOTE: illustrative curves for the draft; camera-ready figures should be
regenerated from the authors' converged OHAM/BVPh data."""
import math, os
from png_plot import Plot, Heatmap, Canvas

OUT = "irreversibility_figures"
os.makedirs(OUT, exist_ok=True)
N = 121
ETA = [i/(N-1) for i in range(N)]

# ---- building blocks -------------------------------------------------------
def hermite(l, e): return l*(1 - 3*e*e + 2*e*e*e)
def vel(e, l=1.0, amp=0.0): return hermite(l, e) + amp*math.sin(math.pi*e)
def theta_exact(e, Pi):
    if abs(Pi) < 1e-6: return e
    return (1 - math.exp(-Pi*e))/(1 - math.exp(-Pi))
def dtheta_exact(e, Pi):
    if abs(Pi) < 1e-6: return 1.0
    return Pi*math.exp(-Pi*e)/(1 - math.exp(-Pi))
def phi_exact(e, Sc=1.0, fc=1.0, K=1.0):
    disc = math.sqrt(Sc*Sc*fc*fc + 4*Sc*K); r1=(-Sc*fc+disc)/2; r2=(-Sc*fc-disc)/2
    return (math.exp(r1*e)-math.exp(r2*e))/(math.exp(r1)-math.exp(r2))
def dphi_exact(e, Sc=1.0, fc=1.0, K=1.0):
    disc = math.sqrt(Sc*Sc*fc*fc + 4*Sc*K); r1=(-Sc*fc+disc)/2; r2=(-Sc*fc-disc)/2
    return (r1*math.exp(r1*e)-r2*math.exp(r2*e))/(math.exp(r1)-math.exp(r2))
def deriv(fun, e, h=1e-3):
    return (fun(min(e+h,1))-fun(max(e-h,0)))/(min(e+h,1)-max(e-h,0))

A1,A3,A4,A5=1.12,1.15,1.18,1.05
BETA=1.0;KP=1.0;LAM=1.0;ZETA=1.0;OM=1.0
def NG_point(e, Br=1.0, M=1.0, Rd=1.0, Pi=1.2, amp=0.15, K=1.0):
    fp=vel(e,1.0,amp); fpp=deriv(lambda z:vel(z,1.0,amp),e)
    th=dtheta_exact(e,Pi); ph=dphi_exact(e,1.0,1.0,K)
    NH=A4*(1+4/3*Rd)*th*th
    NF=(Br/OM)*(A1*(1+1/BETA)*(fpp*fpp+KP*fp*fp)+A3*M*fp*fp)
    ND=LAM*(ZETA*ZETA/(OM*OM))*ph*ph+LAM*(ZETA/OM)*th*ph
    return NH,NF,ND

# ============================================================ FIGURE 1 (schematic)
def arrow(c,x0,y0,x1,y1,col,head=7,th=2):
    c.line(x0,y0,x1,y1,col,th)
    ang=math.atan2(y1-y0,x1-x0)
    for da in (math.radians(150),math.radians(-150)):
        hx=x1+head*math.cos(ang+da); hy=y1+head*math.sin(ang+da)
        c.line(x1,y1,hx,hy,col,th)
def ring(c,cx,cy,r,col):
    for a in range(0,360,25):
        c.px(int(cx+r*math.cos(math.radians(a))),int(cy+r*math.sin(math.radians(a))),col)

def schematic():
    W,H=760,480; c=Canvas(W,H)
    BLACK=(0,0,0); GREY=(110,110,110); BLUE=(31,119,180); RED=(214,39,40)
    GREEN=(44,160,44); LGREY=(180,180,180)
    xl,xr=140,620; yt,yb=95,340
    # channel background
    c.fill_rect(xl,yt,xr,yb,(238,242,248))
    # porous medium rings + hybrid nanoparticles (two colours)
    for ix in range(xl+15,xr-5,34):
        for iy in range(yt+16,yb-5,30):
            ring(c,ix,iy,6,LGREY)
    for k,(ix,iy) in enumerate([(xl+30+((i*47)%(xr-xl-40)),yt+24+((i*53)%(yb-yt-40))) for i in range(26)]):
        col=BLUE if k%2==0 else RED
        c.fill_rect(ix,iy,ix+5,iy+5,col)
    # plates
    c.fill_rect(xl,yt-12,xr,yt,GREY)          # upper plate
    c.fill_rect(xl,yb,xr,yb+12,GREY)          # lower plate
    for hx in range(xl,xr,12):                # hatching
        c.line(hx,yt-12,hx+8,yt,(70,70,70),1)
        c.line(hx,yb,hx+8,yb+12,(70,70,70),1)
    # labels for plates
    c.text(xl,yt-30,"UPPER PLATE (SQUEEZING)  Y = H(T)",BLACK,1)
    c.text(xl,yb+18,"LOWER PLATE (STRETCHING, PERMEABLE)  Y = 0",BLACK,1)
    # squeezing arrow (upper plate moving down)
    arrow(c,380,yt+18,380,yt+56,RED,8,2); c.text(388,yt+30,"VH = DH/DT",RED,1)
    # stretching arrows on lower plate
    arrow(c,360,yb-8,250,yb-8,GREEN,8,2)
    arrow(c,400,yb-8,510,yb-8,GREEN,8,2); c.text(520,yb-14,"UW",GREEN,1)
    # suction/injection arrows through lower plate
    for sx in (200,300,470,560):
        arrow(c,sx,yb-22,sx,yb+10,(150,90,30),6,2)
    c.text(300,yb+30,"VW (SUCTION / INJECTION)",(150,90,30),1)
    # magnetic field arrows (transverse, y-direction)
    for bx in (120,120):
        arrow(c,118,yb,118,yt,(90,60,150),8,2)
    c.text(96,yt-26,"B(T)",(90,60,150),1)
    # coordinate axes
    ax,ay=650,420
    arrow(c,ax,ay,ax+70,ay,BLACK,7,2); c.text(ax+74,ay-4,"X",BLACK,1)
    arrow(c,ax,ay,ax,ay-70,BLACK,7,2); c.text(ax-4,ay-86,"Y",BLACK,1)
    # legend for particles
    c.fill_rect(xl,yb+40,xl+6,yb+46,BLUE); c.text(xl+12,yb+40,"AL2O3",BLACK,1)
    c.fill_rect(xl+90,yb+40,xl+96,yb+46,RED); c.text(xl+102,yb+40,"CU",BLACK,1)
    ring(c,xl+165,yb+43,5,LGREY); c.text(xl+178,yb+40,"POROUS MATRIX",BLACK,1)
    c.text_center(W/2,20,"FIG 1  PHYSICAL MODEL OF THE SQUEEZING CHANNEL",BLACK,2)
    c.save(OUT+"/Figure_1.png")

schematic()

# ============================================================ FIGURE 2  velocity vs M
p=Plot(title="FIG 2  VELOCITY vs M",xlabel="ETA",ylabel="F'(ETA)")
for M,amp in zip([1,3,5,7],[0.18,0.10,0.02,-0.08]):
    p.add(ETA,[vel(e,1.0,amp) for e in ETA],"M="+str(M))
p.render((0,1),(0,1.1),OUT+"/Figure_2.png")

# ============================================================ FIGURE 3  velocity vs Sq
p=Plot(title="FIG 3  VELOCITY vs SQ",xlabel="ETA",ylabel="F'(ETA)")
for Sq,amp in zip([-0.3,0.0,0.3,0.6],[-0.28,0.0,0.28,0.52]):
    p.add(ETA,[vel(e,1.0,amp) for e in ETA],"Sq="+str(Sq))
p.render((0,1),(-0.4,1.4),OUT+"/Figure_3.png")

# ============================================================ FIGURE 4  temperature vs Rd
p=Plot(title="FIG 4  TEMPERATURE vs RD",xlabel="ETA",ylabel="THETA(ETA)")
for Rd,Pi in zip([0.5,1,2,4],[1.6,1.33,1.0,0.667]):
    p.add(ETA,[theta_exact(e,Pi) for e in ETA],"Rd="+str(Rd))
p.render((0,1),(0,1.0),OUT+"/Figure_4.png")

# ============================================================ FIGURE 5  concentration vs K
p=Plot(title="FIG 5  CONCENTRATION vs K",xlabel="ETA",ylabel="PHI(ETA)")
for K in [0.5,1.0,1.5,2.0]:
    p.add(ETA,[phi_exact(e,1.0,1.0,K) for e in ETA],"K="+str(K))
p.render((0,1),(0,1.0),OUT+"/Figure_5.png")

# ============================================================ FIGURE 6  N_G vs Br
p=Plot(title="FIG 6  ENTROPY NG vs BR",xlabel="ETA",ylabel="NG"); mx=0
for Br in [0.5,1.0,2.0,3.0]:
    ys=[sum(NG_point(e,Br=Br)) for e in ETA]; mx=max(mx,max(ys))
    p.add(ETA,ys,"Br="+str(Br))
p.render((0,1),(0,math.ceil(mx)),OUT+"/Figure_6.png")

# ============================================================ FIGURE 7  Be vs M
p=Plot(title="FIG 7  BEJAN vs M",xlabel="ETA",ylabel="BE")
for M in [0.5,1.0,3.0,5.0]:
    ys=[]
    for e in ETA:
        NH,NF,ND=NG_point(e,M=M); tot=NH+NF+ND; ys.append((NH+ND)/tot if tot>0 else 0)
    p.add(ETA,ys,"M="+str(M))
p.render((0,1),(0,1.0),OUT+"/Figure_7.png")

# ============================================================ FIGURE 8  contour N_G(eta,M)
hm=Heatmap(title="FIG 8  NG (ETA, M)",xlabel="M",ylabel="ETA")
hm.render((0.2,6.0),(0,1),lambda M,e:sum(NG_point(e,M=M,amp=0.15)),OUT+"/Figure_8.png",zlabel="NG")

# ============================================================ FIGURE 9  avg N_G vs Sq
p=Plot(title="FIG 9  AVG NG vs SQ",xlabel="SQ",ylabel="NG AVG")
SQ=[0.05*i for i in range(1,25)]
for beta,kf in zip([0.5,1.0,5.0],[3.0,2.0,1.2]):
    ys=[kf*(0.3+0.6*sq**1.5)+1.7/(1+1.2*sq) for sq in SQ]
    p.add(SQ,ys,"beta="+str(beta))
p.render((0,1.2),(1.0,5.0),OUT+"/Figure_9.png")

print("Figures written to",OUT)
for i in range(1,10):
    fn=OUT+"/Figure_%d.png"%i; print(fn, os.path.getsize(fn),"bytes")
