#!/usr/bin/env python3
"""
Statistical engine for the research article:
"Sex Differences in Early Functional Outcomes After Acute Stroke"

Generates a literature-calibrated SYNTHETIC cohort of acute ischaemic stroke
patients and computes genuine inferential statistics using ONLY the Python
standard library. Results -> stroke_results.json.

Calibration anchors (published literature):
  - Women older at onset (~75 vs ~69 y) and higher baseline NIHSS
  - Women: more atrial fibrillation, hypertension, higher prestroke disability
  - Men: more coronary disease, smoking, diabetes
  - Good outcome (mRS 0-2) less frequent in women (~53% vs ~71%)
  - Female sex independently associated with poor early outcome (aOR ~1.3)
This is a MODELLED dataset for methodological illustration, not real patients.
"""
import random, math, json, os

SEED = 20260923
random.seed(SEED)
N = 2000

# ---------------- stats helpers (stdlib only) ----------------
def norm_cdf(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def norm_sf(x): return 1.0-norm_cdf(x)
def z_p(z): return 2.0*norm_sf(abs(z))
def chi2_p_df1(x): return math.erfc(math.sqrt(x/2.0))

def chi2_2x2(a,b,c,d):
    n=a+b+c+d; r1,r2=a+b,c+d; c1,c2=a+c,b+d
    obs=[a,b,c,d]; exp=[r1*c1/n,r1*c2/n,r2*c1/n,r2*c2/n]
    chi2=sum((abs(o-e)-0.5)**2/e for o,e in zip(obs,exp))
    return chi2, chi2_p_df1(chi2)

def odds_ratio_ci(a,b,c,d):
    if 0 in (a,b,c,d): a+=0.5;b+=0.5;c+=0.5;d+=0.5
    orr=(a*d)/(b*c); se=math.sqrt(1/a+1/b+1/c+1/d)
    return orr, math.exp(math.log(orr)-1.96*se), math.exp(math.log(orr)+1.96*se)

def welch_t(x,y):
    nx,ny=len(x),len(y); mx,my=sum(x)/nx,sum(y)/ny
    vx=sum((v-mx)**2 for v in x)/(nx-1); vy=sum((v-my)**2 for v in y)/(ny-1)
    se=math.sqrt(vx/nx+vy/ny); t=(mx-my)/se
    return mx,my,math.sqrt(vx),math.sqrt(vy),t,z_p(t)

def mean_sd(x):
    n=len(x); m=sum(x)/n; sd=math.sqrt(sum((v-m)**2 for v in x)/(n-1)) if n>1 else 0
    return m,sd

def mat_inv(M):
    n=len(M); A=[row[:]+[1.0 if i==j else 0.0 for j in range(n)] for i,row in enumerate(M)]
    for col in range(n):
        piv=max(range(col,n),key=lambda r:abs(A[r][col])); A[col],A[piv]=A[piv],A[col]
        pv=A[col][col]; A[col]=[v/pv for v in A[col]]
        for r in range(n):
            if r!=col:
                f=A[r][col]; A[r]=[a-f*b for a,b in zip(A[r],A[col])]
    return [row[n:] for row in A]

def logistic_regression(X,y,iters=60):
    n,k=len(X),len(X[0]); beta=[0.0]*k
    for _ in range(iters):
        grad=[0.0]*k; H=[[0.0]*k for _ in range(k)]
        for i in range(n):
            eta=max(-30,min(30,sum(beta[j]*X[i][j] for j in range(k))))
            p=1.0/(1.0+math.exp(-eta)); w=p*(1-p); r=y[i]-p
            for a in range(k):
                grad[a]+=X[i][a]*r
                for b in range(k): H[a][b]+=X[i][a]*X[i][b]*w
        Hinv=mat_inv(H); step=[sum(Hinv[a][b]*grad[b] for b in range(k)) for a in range(k)]
        beta=[beta[a]+step[a] for a in range(k)]
        if max(abs(s) for s in step)<1e-9: break
    cov=mat_inv(H); se=[math.sqrt(cov[a][a]) for a in range(k)]
    return beta,se

def logit(p): return math.log(p/(1-p))

# ---------------- simulate cohort ----------------
R=[]
for _ in range(N):
    female = 1 if random.random() < 0.52 else 0
    age = random.gauss(75 if female else 69, 13)
    age = max(30, min(98, age))
    af  = 1 if random.random() < (0.24 if female else 0.17) else 0
    htn = 1 if random.random() < (0.70 if female else 0.63) else 0
    dm  = 1 if random.random() < (0.20 if female else 0.27) else 0
    smoke = 1 if random.random() < (0.12 if female else 0.28) else 0
    cad = 1 if random.random() < (0.14 if female else 0.24) else 0
    prestroke_dis = 1 if random.random() < (0.30 if female else 0.19) else 0  # mRS>=2 before
    # baseline NIHSS (higher in women)
    nih = random.gauss(9.0 if female else 7.5, 6.0)
    nihss = int(max(0, min(42, round(nih))))
    # thrombolysis (slightly lower in women; more likely with moderate severity)
    ltpa = -1.75 - 0.28*female + 0.03*(nihss-8) - 0.010*(age-72)
    tpa = 1 if random.random() < 1/(1+math.exp(-ltpa)) else 0
    # poor EARLY functional outcome at discharge (mRS 3-6)
    lp = (logit(0.35) + 0.045*(age-72) + 0.16*(nihss-8) + 0.80*prestroke_dis
          + 0.50*af + 0.42*female - 0.55*tpa)
    poor = 1 if random.random() < 1/(1+math.exp(-max(-30,min(30,lp)))) else 0
    # ordinal-ish mRS band at discharge
    if not poor:
        mrs_band = 0 if random.random()<0.55 else 1  # 0=mRS0-1, 1=mRS2
    else:
        r=random.random()
        mrs_band = 2 if r<0.5 else (3 if r<0.85 else 4)  # 2=mRS3-4,3=mRS5,4=death(6)
    # in-hospital mortality
    ld = -3.0 + 0.055*(age-72) + 0.14*(nihss-8) + 0.45*af + 0.15*female
    death = 1 if (mrs_band==4 or random.random() < 1/(1+math.exp(-ld))) else 0
    if death: mrs_band = 4
    home = 1 if ((not poor and random.random()<0.9) or (poor and not death and random.random()<0.15)) else 0
    los = max(1, round(random.lognormvariate(math.log(6 + 0.15*nihss + 2*poor), 0.5)))
    R.append(dict(female=female, age=age, af=af, htn=htn, dm=dm, smoke=smoke, cad=cad,
                  prestroke_dis=prestroke_dis, nihss=nihss, tpa=tpa, poor=poor,
                  good=1-poor, mrs_band=mrs_band, death=death, home=home, los=los))

W=[r for r in R if r["female"]==1]
M=[r for r in R if r["female"]==0]
out={"meta":{"seed":SEED,"N":N,"n_women":len(W),"n_men":len(M),
             "pct_women":round(100*len(W)/N,1)}}

def prop(g,k): 
    n=len(g); x=sum(r[k] for r in g); return x,round(100*x/n,1)

# ---------- Table 1: baseline characteristics ----------
t1={}
# continuous: age, nihss, los
for key in ["age","nihss","los"]:
    mw,mm,sw,sm,t,p=welch_t([r[key] for r in W],[r[key] for r in M])
    t1[key]={"women_mean":round(mw,1),"women_sd":round(sw,1),
             "men_mean":round(mm,1),"men_sd":round(sm,1),"t":round(t,2),"p":p}
# categorical
for key in ["af","htn","dm","smoke","cad","prestroke_dis","tpa"]:
    xw,pw=prop(W,key); xm,pm=prop(M,key)
    chi2,p=chi2_2x2(xw,len(W)-xw,xm,len(M)-xm)
    orr,lo,hi=odds_ratio_ci(xw,len(W)-xw,xm,len(M)-xm)
    t1[key]={"women_pct":pw,"men_pct":pm,"chi2":round(chi2,2),"p":p,
             "OR":round(orr,2),"OR_lo":round(lo,2),"OR_hi":round(hi,2)}
out["table1"]=t1

# ---------- Primary outcome: good functional outcome (mRS 0-2) ----------
gw=sum(r["good"] for r in W); gm=sum(r["good"] for r in M)
chi2,p=chi2_2x2(gw,len(W)-gw,gm,len(M)-gm)
orr,lo,hi=odds_ratio_ci(gw,len(W)-gw,gm,len(M)-gm)  # OR of GOOD outcome for women vs men
out["primary_good"]={"women_pct":round(100*gw/len(W),1),"men_pct":round(100*gm/len(M),1),
    "chi2":round(chi2,2),"p":p,"OR_good_women":round(orr,2),"OR_lo":round(lo,2),"OR_hi":round(hi,2)}
# also crude OR of POOR outcome for women
pw_=len(W)-gw; pm_=len(M)-gm
orp,lop,hip=odds_ratio_ci(pw_,gw,pm_,gm)
out["primary_poor"]={"women_pct":round(100*pw_/len(W),1),"men_pct":round(100*pm_/len(M),1),
    "OR_poor_women":round(orp,2),"OR_lo":round(lop,2),"OR_hi":round(hip,2)}

# ---------- Secondary outcomes ----------
sec={}
for key,label in [("death","In-hospital mortality"),("home","Discharge to home")]:
    xw,pw=prop(W,key); xm,pm=prop(M,key)
    chi2,p=chi2_2x2(xw,len(W)-xw,xm,len(M)-xm)
    orr,lo,hi=odds_ratio_ci(xw,len(W)-xw,xm,len(M)-xm)
    sec[key]={"label":label,"women_pct":pw,"men_pct":pm,"chi2":round(chi2,2),"p":p,
              "OR":round(orr,2),"OR_lo":round(lo,2),"OR_hi":round(hi,2)}
out["secondary"]=sec

# ---------- mRS distribution by sex (for stacked figure) ----------
def band_dist(g):
    n=len(g); d=[0,0,0,0,0]
    for r in g: d[r["mrs_band"]]+=1
    return [round(100*x/n,1) for x in d]
out["mrs_dist"]={"women":band_dist(W),"men":band_dist(M),
                 "labels":["mRS 0-1","mRS 2","mRS 3-4","mRS 5","mRS 6 (death)"]}

# ---------- Multivariable logistic regression: POOR outcome (mRS 3-6) ----------
ages=[r["age"] for r in R]; nihs=[r["nihss"] for r in R]
ma,sa=mean_sd(ages); mn,sn=mean_sd(nihs)
X=[[1.0, r["female"], (r["age"]-ma)/sa, (r["nihss"]-mn)/sn, r["prestroke_dis"],
    r["af"], r["tpa"]] for r in R]
Y=[r["poor"] for r in R]
beta,se=logistic_regression(X,Y)
names=["Intercept","Female sex","Age (per SD)","Baseline NIHSS (per SD)",
       "Prestroke disability","Atrial fibrillation","Thrombolysis (IV tPA)"]
out["logit"]=[]
for nm,b,s in zip(names,beta,se):
    z=b/s
    out["logit"].append({"var":nm,"beta":round(b,3),"aOR":round(math.exp(b),2),
        "aOR_lo":round(math.exp(b-1.96*s),2),"aOR_hi":round(math.exp(b+1.96*s),2),
        "z":round(z,2),"p":z_p(z)})

here=os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here,"stroke_results.json"),"w"), indent=2)

def fp(p): return "<0.001" if p<0.001 else f"{p:.3f}"
print(f"Cohort N={N} | women={len(W)} ({out['meta']['pct_women']}%), men={len(M)}")
print(f"\nAge: women {t1['age']['women_mean']} vs men {t1['age']['men_mean']}, p={fp(t1['age']['p'])}")
print(f"NIHSS: women {t1['nihss']['women_mean']} vs men {t1['nihss']['men_mean']}, p={fp(t1['nihss']['p'])}")
print(f"AF: {t1['af']['women_pct']}% vs {t1['af']['men_pct']}%  | tPA: {t1['tpa']['women_pct']}% vs {t1['tpa']['men_pct']}%")
pg=out["primary_good"]
print(f"\nGood outcome (mRS 0-2): women {pg['women_pct']}% vs men {pg['men_pct']}%")
print(f"  crude OR(good, women)={pg['OR_good_women']} ({pg['OR_lo']}-{pg['OR_hi']}), chi2={pg['chi2']}, p={fp(pg['p'])}")
print(f"  crude OR(poor, women)={out['primary_poor']['OR_poor_women']} ({out['primary_poor']['OR_lo']}-{out['primary_poor']['OR_hi']})")
print(f"Mortality: women {sec['death']['women_pct']}% vs men {sec['death']['men_pct']}%, OR={sec['death']['OR']}")
print("\nAdjusted logistic regression (poor outcome, mRS 3-6):")
for row in out["logit"]:
    if row["var"]=="Intercept": continue
    print(f"  {row['var']:<26} aOR={row['aOR']:>5} ({row['aOR_lo']}-{row['aOR_hi']}), p={fp(row['p'])}")
print("\nWrote stroke_results.json")
