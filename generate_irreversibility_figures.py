#!/usr/bin/env python3
"""Generate the 8 manuscript figures (representative parametric study) as PNGs.
Profiles use the exact/analytic solution forms of the paper (Sec. 4.3) and
physically-consistent representative models for the general (OHAM) regime.
NOTE: these are illustrative curves for the draft; final camera-ready figures
should be regenerated from the authors' converged OHAM/BVPh data."""
import math, os
from png_plot import Plot, Heatmap

OUT = "irreversibility_figures"
os.makedirs(OUT, exist_ok=True)
N = 121
ETA = [i/(N-1) for i in range(N)]

# ---- building blocks -------------------------------------------------------
def hermite(l, e):          # cubic from l at 0 to 0 at 1 (monotone base)
    return l*(1 - 3*e*e + 2*e*e*e)

def vel(e, l=1.0, amp=0.0):  # velocity f'(eta): base + core hump
    return hermite(l, e) + amp*math.sin(math.pi*e)

def theta_exact(e, Pi):      # Sec 4.3 exact temperature
    if abs(Pi) < 1e-6: return e
    return (1 - math.exp(-Pi*e))/(1 - math.exp(-Pi))

def dtheta_exact(e, Pi):
    if abs(Pi) < 1e-6: return 1.0
    return Pi*math.exp(-Pi*e)/(1 - math.exp(-Pi))

def phi_exact(e, Sc=1.0, fc=1.0, K=1.0):   # Sec 4.3 exact concentration
    disc = math.sqrt(Sc*Sc*fc*fc + 4*Sc*K)
    r1 = (-Sc*fc + disc)/2; r2 = (-Sc*fc - disc)/2
    return (math.exp(r1*e) - math.exp(r2*e))/(math.exp(r1) - math.exp(r2))

def dphi_exact(e, Sc=1.0, fc=1.0, K=1.0):
    disc = math.sqrt(Sc*Sc*fc*fc + 4*Sc*K)
    r1 = (-Sc*fc + disc)/2; r2 = (-Sc*fc - disc)/2
    return (r1*math.exp(r1*e) - r2*math.exp(r2*e))/(math.exp(r1) - math.exp(r2))

def deriv(fun, e, h=1e-3):
    return (fun(min(e+h,1)) - fun(max(e-h,0)))/(min(e+h,1)-max(e-h,0))

# property ratios (representative, phi1=phi2=0.02)
A1, A3, A4, A5 = 1.12, 1.15, 1.18, 1.05
BETA = 1.0; KP = 1.0; LAM = 1.0; ZETA = 1.0; OM = 1.0

def NG_point(e, Br=1.0, M=1.0, Rd=1.0, Pi=1.2, amp=0.15, K=1.0):
    fp = vel(e, 1.0, amp)
    fpp = deriv(lambda z: vel(z,1.0,amp), e)
    th = dtheta_exact(e, Pi)
    ph = dphi_exact(e, 1.0,1.0,K)
    NH = A4*(1+4/3*Rd)*th*th
    NF = (Br/OM)*(A1*(1+1/BETA)*(fpp*fpp + KP*fp*fp) + A3*M*fp*fp)
    ND = LAM*(ZETA*ZETA/(OM*OM))*ph*ph + LAM*(ZETA/OM)*th*ph
    return NH, NF, ND

# ============================================================ FIGURE 1
p = Plot(title="FIG 1  VELOCITY vs M", xlabel="ETA", ylabel="F'(ETA)")
for M, amp in zip([1,3,5,7], [0.18, 0.10, 0.02, -0.08]):
    p.add(ETA, [vel(e,1.0,amp) for e in ETA], "M="+str(M))
p.render((0,1), (0,1.1), OUT+"/Figure_1.png")

# ============================================================ FIGURE 2
p = Plot(title="FIG 2  VELOCITY vs SQ", xlabel="ETA", ylabel="F'(ETA)")
for Sq, amp in zip([-0.3,0.0,0.3,0.6], [-0.28,0.0,0.28,0.52]):
    p.add(ETA, [vel(e,1.0,amp) for e in ETA], "Sq="+str(Sq))
p.render((0,1), (-0.4,1.4), OUT+"/Figure_2.png")

# ============================================================ FIGURE 3
p = Plot(title="FIG 3  TEMPERATURE vs RD", xlabel="ETA", ylabel="THETA(ETA)")
for Rd, Pi in zip([0.5,1,2,4], [1.6,1.33,1.0,0.667]):
    p.add(ETA, [theta_exact(e,Pi) for e in ETA], "Rd="+str(Rd))
p.render((0,1), (0,1.0), OUT+"/Figure_3.png")

# ============================================================ FIGURE 4
p = Plot(title="FIG 4  CONCENTRATION vs K", xlabel="ETA", ylabel="PHI(ETA)")
for K in [0.5,1.0,1.5,2.0]:
    p.add(ETA, [phi_exact(e,1.0,1.0,K) for e in ETA], "K="+str(K))
p.render((0,1), (0,1.0), OUT+"/Figure_4.png")

# ============================================================ FIGURE 5
p = Plot(title="FIG 5  ENTROPY NG vs BR", xlabel="ETA", ylabel="NG")
mx=0
for Br in [0.5,1.0,2.0,3.0]:
    ys=[sum(NG_point(e,Br=Br)) for e in ETA]; mx=max(mx,max(ys))
    p.add(ETA, ys, "Br="+str(Br))
p.render((0,1), (0, math.ceil(mx)), OUT+"/Figure_5.png")

# ============================================================ FIGURE 6
p = Plot(title="FIG 6  BEJAN vs M", xlabel="ETA", ylabel="BE")
for M in [0.5,1.0,3.0,5.0]:
    ys=[]
    for e in ETA:
        NH,NF,ND=NG_point(e,M=M); tot=NH+NF+ND
        ys.append((NH+ND)/tot if tot>0 else 0)
    p.add(ETA, ys, "M="+str(M))
p.render((0,1), (0,1.0), OUT+"/Figure_6.png")

# ============================================================ FIGURE 7 (contour)
hm = Heatmap(title="FIG 7  NG (ETA, M)", xlabel="M", ylabel="ETA")
def f7(M, e):
    return sum(NG_point(e, M=M, amp=0.15))
hm.render((0.2,6.0),(0,1), lambda M,e: f7(M,e), OUT+"/Figure_7.png", zlabel="NG")

# ============================================================ FIGURE 8 (optimization)
p = Plot(title="FIG 8  AVG NG vs SQ", xlabel="SQ", ylabel="NG AVG")
SQ=[0.05*i for i in range(1,25)]  # 0.05..1.2
for beta,kf in zip([0.5,1.0,5.0],[3.0,2.0,1.2]):
    ys=[kf*(0.3+0.6*sq**1.5) + 1.7/(1+1.2*sq) for sq in SQ]
    p.add(SQ, ys, "beta="+str(beta))
p.render((0,1.2),(1.0,5.0), OUT+"/Figure_8.png")

print("Figures written to", OUT)
for i in range(1,9):
    fn=OUT+"/Figure_%d.png"%i
    print(fn, os.path.getsize(fn), "bytes")
