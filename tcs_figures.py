#!/usr/bin/env python3
"""Build SVG figures for the TCS misuse research article from tcs_results.json.
Standard library only."""
import json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tcs_figures")
os.makedirs(OUT, exist_ok=True)
R = json.load(open(os.path.join(HERE, "tcs_results.json")))

C = dict(sm="#c0504d", pr="#4f81bd", axis="#333", grid="#dddddd",
         text="#222", muted="#666", pt="#2c3e50", ci="#7f8c8d")

def head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="Helvetica,Arial,sans-serif">\n'
            f'<rect width="{w}" height="{h}" fill="white"/>\n')

# ---------- Figure 1: adverse-effect rate by group ----------
def fig1():
    w, h = 640, 420
    pl, pt, pb, pr_ = 70, 70, 70, 30
    ph = h - pt - pb; pw = w - pl - pr_
    p = R["primary_ae"]
    groups = [("Self-medicated", p["self_med_ae_pct"], C["sm"]),
              ("Prescribed", p["prescribed_ae_pct"], C["pr"])]
    vmax = 100
    s = head(w, h)
    s += f'<text x="20" y="28" font-size="16" font-weight="bold" fill="{C["text"]}">Figure 1. Adverse-effect rate by source of topical corticosteroid</text>\n'
    for g in range(0, 6):
        gy = pt + ph*(1-g/5); gv = vmax*g/5
        s += f'<line x1="{pl}" y1="{gy:.1f}" x2="{w-pr_}" y2="{gy:.1f}" stroke="{C["grid"]}"/>\n'
        s += f'<text x="{pl-8}" y="{gy+4:.1f}" font-size="11" fill="{C["muted"]}" text-anchor="end">{gv:.0f}%</text>\n'
    bw = pw/ (len(groups)*2)
    for i,(lab,val,col) in enumerate(groups):
        x = pl + pw*(i+0.5)/len(groups) - bw/2
        bh = ph*val/vmax; y = pt+ph-bh
        s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{col}" rx="2"/>\n'
        s += f'<text x="{x+bw/2:.1f}" y="{y-8:.1f}" font-size="14" font-weight="bold" fill="{C["text"]}" text-anchor="middle">{val}%</text>\n'
        s += f'<text x="{x+bw/2:.1f}" y="{pt+ph+22:.1f}" font-size="13" fill="{C["text"]}" text-anchor="middle">{lab}</text>\n'
    s += f'<line x1="{pl}" y1="{pt+ph}" x2="{w-pr_}" y2="{pt+ph}" stroke="{C["axis"]}"/>\n'
    s += f'<line x1="{pl}" y1="{pt}" x2="{pl}" y2="{pt+ph}" stroke="{C["axis"]}"/>\n'
    ann = f'OR = {p["OR"]} (95% CI {p["OR_lo"]}\u2013{p["OR_hi"]}); \u03c7\u00b2 = {p["chi2"]}, p < 0.001'
    s += f'<text x="{w/2:.0f}" y="{h-18}" font-size="12" fill="{C["muted"]}" text-anchor="middle">{ann}</text>\n'
    s += "</svg>\n"
    open(os.path.join(OUT,"fig1_ae_rate.svg"),"w").write(s)

# ---------- Figure 2: forest plot of adjusted ORs ----------
def fig2():
    rows = [r for r in R["logit"] if r["var"] != "Intercept"]
    w = 720; row_h = 46; pt = 70; pb = 60
    h = pt + len(rows)*row_h + pb
    pl = 210; pr_ = 90; pw = w - pl - pr_
    # log scale x-axis
    lo = min(r["aOR_lo"] for r in rows); hi = max(r["aOR_hi"] for r in rows)
    xmin, xmax = math.log(min(lo,0.9)*0.9), math.log(hi*1.1)
    def X(v): return pl + pw*(math.log(v)-xmin)/(xmax-xmin)
    s = head(w, h)
    s += f'<text x="20" y="28" font-size="16" font-weight="bold" fill="{C["text"]}">Figure 2. Adjusted odds ratios for any adverse effect (multivariable logistic regression)</text>\n'
    for tick in [0.5,1,2,4,8]:
        if xmin <= math.log(tick) <= xmax:
            gx = X(tick)
            s += f'<line x1="{gx:.1f}" y1="{pt-10}" x2="{gx:.1f}" y2="{pt+len(rows)*row_h}" stroke="{C["grid"]}"/>\n'
            s += f'<text x="{gx:.1f}" y="{pt+len(rows)*row_h+20:.1f}" font-size="11" fill="{C["muted"]}" text-anchor="middle">{tick}</text>\n'
    x1 = X(1.0)
    s += f'<line x1="{x1:.1f}" y1="{pt-10}" x2="{x1:.1f}" y2="{pt+len(rows)*row_h}" stroke="{C["axis"]}" stroke-dasharray="4,3"/>\n'
    for i,r in enumerate(rows):
        y = pt + i*row_h + row_h/2
        xlo, xhi, xor = X(r["aOR_lo"]), X(r["aOR_hi"]), X(r["aOR"])
        s += f'<text x="{pl-12}" y="{y+4:.1f}" font-size="13" fill="{C["text"]}" text-anchor="end">{r["var"]}</text>\n'
        s += f'<line x1="{xlo:.1f}" y1="{y:.1f}" x2="{xhi:.1f}" y2="{y:.1f}" stroke="{C["ci"]}" stroke-width="2"/>\n'
        for xe in (xlo,xhi):
            s += f'<line x1="{xe:.1f}" y1="{y-5:.1f}" x2="{xe:.1f}" y2="{y+5:.1f}" stroke="{C["ci"]}" stroke-width="2"/>\n'
        s += f'<rect x="{xor-5:.1f}" y="{y-5:.1f}" width="10" height="10" fill="{C["pt"]}"/>\n'
        s += f'<text x="{w-pr_+8}" y="{y+4:.1f}" font-size="11.5" fill="{C["text"]}">{r["aOR"]} ({r["aOR_lo"]}\u2013{r["aOR_hi"]})</text>\n'
    s += f'<text x="{pl+pw/2:.0f}" y="{h-16}" font-size="12" fill="{C["muted"]}" text-anchor="middle">Adjusted odds ratio (log scale)</text>\n'
    s += "</svg>\n"
    open(os.path.join(OUT,"fig2_forest.svg"),"w").write(s)

# ---------- Figure 3: duration & cost grouped bars ----------
def fig3():
    w,h = 700,430; pl,pt,pb,pr_=70,70,90,30
    ph=h-pt-pb; pw=w-pl-pr_
    dur=R["duration"]; cost=R["cost"]
    groups=["Mean duration (weeks)","Mean direct cost (USD)"]
    series=[("Self-medicated",[dur["self_med_mean"],cost["self_med_mean"]],C["sm"]),
            ("Prescribed",[dur["prescribed_mean"],cost["prescribed_mean"]],C["pr"])]
    vmax=max(cost["self_med_mean"],dur["self_med_mean"])*1.2
    s=head(w,h)
    s+=f'<text x="20" y="28" font-size="16" font-weight="bold" fill="{C["text"]}">Figure 3. Duration of use and direct cost of care by group</text>\n'
    for g in range(0,6):
        gy=pt+ph*(1-g/5); gv=vmax*g/5
        s+=f'<line x1="{pl}" y1="{gy:.1f}" x2="{w-pr_}" y2="{gy:.1f}" stroke="{C["grid"]}"/>\n'
        s+=f'<text x="{pl-8}" y="{gy+4:.1f}" font-size="11" fill="{C["muted"]}" text-anchor="end">{gv:.0f}</text>\n'
    ng=len(groups); gw=pw/ng; bw=gw*0.7/len(series)
    for gi,gname in enumerate(groups):
        gx0=pl+gi*gw+gw*0.15
        for si,(sname,vals,col) in enumerate(series):
            v=vals[gi]; bh=ph*v/vmax; bx=gx0+si*bw; by=pt+ph-bh
            s+=f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw-4:.1f}" height="{bh:.1f}" fill="{col}" rx="2"/>\n'
            s+=f'<text x="{bx+(bw-4)/2:.1f}" y="{by-6:.1f}" font-size="12" font-weight="bold" fill="{C["text"]}" text-anchor="middle">{v}</text>\n'
        s+=f'<text x="{pl+gi*gw+gw/2:.1f}" y="{pt+ph+24:.1f}" font-size="12.5" fill="{C["text"]}" text-anchor="middle">{gname}</text>\n'
    s+=f'<line x1="{pl}" y1="{pt+ph}" x2="{w-pr_}" y2="{pt+ph}" stroke="{C["axis"]}"/>\n'
    s+=f'<line x1="{pl}" y1="{pt}" x2="{pl}" y2="{pt+ph}" stroke="{C["axis"]}"/>\n'
    lx=pl; ly=h-28
    for sname,_,col in series:
        s+=f'<rect x="{lx}" y="{ly-10}" width="14" height="14" fill="{col}"/>\n'
        s+=f'<text x="{lx+20}" y="{ly+1}" font-size="12" fill="{C["text"]}">{sname}</text>\n'
        lx+=40+len(sname)*7.5
    s+=f'<text x="{w-pr_}" y="{h-12}" font-size="11" fill="{C["muted"]}" text-anchor="end">cost ratio {cost["cost_ratio"]}\u00d7; both p &lt; 0.001</text>\n'
    s+="</svg>\n"
    open(os.path.join(OUT,"fig3_dur_cost.svg"),"w").write(s)

fig1(); fig2(); fig3()
print("Figures written to", OUT)
for f in sorted(os.listdir(OUT)): print(" -", f)
