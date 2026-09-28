#!/usr/bin/env python3
"""Compute corrected table values from the corrected model."""
from carreau_emhd_solver import Params, solve, engineering, entropy_number
import math

_, BASE_U = solve(Params())

def warm(**kw):
    pr = Params(**kw); sol, u = solve(pr, u0=BASE_U); return pr, sol

print("=== Table 4: Cf, Nu, Sh vs governing parameters (baseline otherwise) ===")
rows = [("Sq",0.2),("Sq",0.8),("M",0.5),("M",2.0),("We",0.5),("We",2.0),
        ("Rd",0.2),("Rd",1.0),("Df",0.6),("Sr",0.5),("K",1.5)]
def warm_cont(k, v, steps):
    """continuation from baseline to (k=v) through intermediate steps."""
    u=BASE_U
    for s in steps+[v]:
        pr=Params(**{k:s}); sol,u=solve(pr,u0=u)
    return pr,sol
for k,v in rows:
    if k=="Df":
        pr,sol = warm_cont(k,v,[0.3,0.45])
    else:
        pr,sol = warm(**{k:v})
    Cf,Nu,Sh = engineering(sol,pr)
    print("%-3s %4s  Cf=%8.4f  Nu=%8.4f  Sh=%8.4f"%(k,v,Cf,Nu,Sh))

print()
print("=== Table 5: Ns(0), Be(0) vs irreversibility parameters ===")
rows5 = [(0.5,1.0,0.5,1.0),(1.0,1.0,0.5,1.0),(1.5,1.0,0.5,1.0),
         (1.0,0.5,0.5,1.0),(1.0,2.0,0.5,1.0),(1.0,1.0,1.0,1.0),(1.0,1.0,0.5,2.0)]
for Br,M,Rd,Om in rows5:
    pr,sol = warm(Br=Br,M=M,Rd=Rd,Omega=Om)
    Ns,Be,_ = entropy_number(0.0, sol[0][1], pr)
    print("Br=%.1f M=%.1f Rd=%.1f Om=%.1f  Ns(0)=%8.4f  Be(0)=%7.4f"%(Br,M,Rd,Om,Ns,Be))

print()
print("=== Table 6: phi effect on Nu, Sh, Ns_avg ===")
def ns_avg(pr,sol):
    # trapezoid integral of Ns over eta in [0,1]
    vals=[entropy_number(e,y,pr)[0] for e,y in sol]
    xs=[e for e,_ in sol]
    s=0.0
    for i in range(len(xs)-1):
        s+=0.5*(vals[i]+vals[i+1])*(xs[i+1]-xs[i])
    return s
u=None
for p in (0.0,0.02,0.03,0.04,0.05):
    pr=Params(phi1=p,phi2=p); sol,u=solve(pr,u0=u)
    Cf,Nu,Sh=engineering(sol,pr)
    print("phi=%.2f  Nu=%8.4f  Sh=%8.4f  Ns_avg=%8.4f"%(p,Nu,Sh,ns_avg(pr,sol)))

print()
print("=== Table 3: Newtonian clear-fluid validation, f''(1) and -theta'(1) vs Sq ===")
u=None
for Sq in (0.1,0.5,1.0,1.5):
    pr=Params(phi1=0,phi2=0,n=1.0,We=0.0,Rd=0.0,Ec=0.0,Df=0.0,Sr=0.0,
              M=0.0,Fr=0.0,Da=1e9,S1=0,S3=0,Bi=1e9,K=0.0,Sq=Sq)
    sol,u=solve(pr,u0=u)
    print("Sq=%.1f  f''(1)=%9.6f  -theta'(1)=%9.6f"%(Sq,sol[-1][1][2],-sol[-1][1][5]))

print()
print("=== Grid convergence: f''(1) at N=100,200,400 and observed order ===")
pr=Params()
vals={}
for N in (100,200,400):
    sol,u=solve(pr,N=N)
    vals[N]=sol[-1][1][2]
    print("N=%d  f''(1)=%.8f"%(N,vals[N]))
num=vals[100]-vals[200]; den=vals[200]-vals[400]
p_obs=math.log(abs(num/den))/math.log(2) if den!=0 else float('nan')
print("p_obs = ln|(qN-q2N)/(q2N-q4N)|/ln2 = %.3f"%p_obs)
Eg=abs((vals[200]-vals[400])/vals[400])*100
print("E_grid (200->400) = %.4f %%"%Eg)
