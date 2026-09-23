#!/usr/bin/env python3
"""SVG figures for the stroke sex-differences article. Reads stroke_results.json.
Standard library only."""
import json, os, math

HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,"stroke_figures"); os.makedirs(OUT,exist_ok=True)
R=json.load(open(os.path.join(HERE,"stroke_results.json")))

C=dict(women="#c0504d",men="#4f81bd",axis="#333",grid="#dddddd",text="#222",
       muted="#666",pt="#2c3e50",ci="#7f8c8d")
# mRS band colours: 0-1 good -> green shades to red for death
BAND=["#2e7d32","#9bbb59","#f0ad4e","#e07b39","#b0413e"]

def head(w,h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="Helvetica,Arial,sans-serif">\n'
            f'<rect width="{w}" height="{h}" fill="white"/>\n')

# ---------- Figure 1: mRS distribution by sex (stacked "Grotta" bars) ----------
def fig1():
    w,h=760,340; pl=90; pr=30; pt=70; barh=54; gap=46
    pw=w-pl-pr
    labels=R["mrs_dist"]["labels"]
    rows=[("Women",R["mrs_dist"]["women"]),("Men",R["mrs_dist"]["men"])]
    s=head(w,h)
    s+=f'<text x="20" y="28" font-size="16" font-weight="bold" fill="{C["text"]}">Figure 1. Distribution of modified Rankin Scale at discharge, by sex</text>\n'
    y=pt
    for name,dist in rows:
        x=pl
        s+=f'<text x="{pl-12}" y="{y+barh/2+5:.0f}" font-size="14" fill="{C["text"]}" text-anchor="end">{name}</text>\n'
        for i,val in enumerate(dist):
            seg=pw*val/100.0
            s+=f'<rect x="{x:.1f}" y="{y}" width="{seg:.1f}" height="{barh}" fill="{BAND[i]}"/>\n'
            if seg>28:
                s+=f'<text x="{x+seg/2:.1f}" y="{y+barh/2+5:.0f}" font-size="12" fill="white" text-anchor="middle">{val:.0f}%</text>\n'
            x+=seg
        y+=barh+gap
    # legend
    lx=pl; ly=h-34
    for i,lab in enumerate(labels):
        s+=f'<rect x="{lx}" y="{ly-11}" width="14" height="14" fill="{BAND[i]}"/>\n'
        s+=f'<text x="{lx+19}" y="{ly}" font-size="12" fill="{C["text"]}">{lab}</text>\n'
        lx+=28+len(lab)*7.6
    s+=f'<text x="{pl+pw/2:.0f}" y="{pt+2*barh+gap+14:.0f}" font-size="12" fill="{C["muted"]}" text-anchor="middle">Ordinal shift toward worse outcomes in women (good outcome mRS 0\u20132: {R["primary_good"]["women_pct"]}% vs {R["primary_good"]["men_pct"]}%, p &lt; 0.001)</text>\n'
    s+="</svg>\n"; open(os.path.join(OUT,"fig1_mrs.svg"),"w").write(s)

# ---------- Figure 2: forest plot of adjusted ORs ----------
def fig2():
    rows=[r for r in R["logit"] if r["var"]!="Intercept"]
    w=760; row_h=48; pt=70; pb=60; h=pt+len(rows)*row_h+pb
    pl=230; pr=110; pw=w-pl-pr
    lo=min(r["aOR_lo"] for r in rows); hi=max(r["aOR_hi"] for r in rows)
    xmin,xmax=math.log(min(lo,0.55)*0.9),math.log(hi*1.1)
    def X(v): return pl+pw*(math.log(v)-xmin)/(xmax-xmin)
    s=head(w,h)
    s+=f'<text x="20" y="28" font-size="16" font-weight="bold" fill="{C["text"]}">Figure 2. Adjusted odds ratios for poor early outcome (mRS 3\u20136)</text>\n'
    for tick in [0.5,0.7,1,1.5,2,2.5,3]:
        if xmin<=math.log(tick)<=xmax:
            gx=X(tick)
            s+=f'<line x1="{gx:.1f}" y1="{pt-10}" x2="{gx:.1f}" y2="{pt+len(rows)*row_h}" stroke="{C["grid"]}"/>\n'
            s+=f'<text x="{gx:.1f}" y="{pt+len(rows)*row_h+20:.1f}" font-size="11" fill="{C["muted"]}" text-anchor="middle">{tick}</text>\n'
    x1=X(1.0)
    s+=f'<line x1="{x1:.1f}" y1="{pt-10}" x2="{x1:.1f}" y2="{pt+len(rows)*row_h}" stroke="{C["axis"]}" stroke-dasharray="4,3"/>\n'
    for i,r in enumerate(rows):
        y=pt+i*row_h+row_h/2
        xlo,xhi,xor=X(r["aOR_lo"]),X(r["aOR_hi"]),X(r["aOR"])
        col=C["women"] if r["var"]=="Female sex" else C["pt"]
        s+=f'<text x="{pl-12}" y="{y+4:.1f}" font-size="12.5" fill="{C["text"]}" text-anchor="end">{r["var"]}</text>\n'
        s+=f'<line x1="{xlo:.1f}" y1="{y:.1f}" x2="{xhi:.1f}" y2="{y:.1f}" stroke="{C["ci"]}" stroke-width="2"/>\n'
        for xe in (xlo,xhi):
            s+=f'<line x1="{xe:.1f}" y1="{y-5:.1f}" x2="{xe:.1f}" y2="{y+5:.1f}" stroke="{C["ci"]}" stroke-width="2"/>\n'
        s+=f'<rect x="{xor-5:.1f}" y="{y-5:.1f}" width="10" height="10" fill="{col}"/>\n'
        star=" *" if r["p"]<0.05 else ""
        s+=f'<text x="{w-pr+8}" y="{y+4:.1f}" font-size="11.5" fill="{C["text"]}">{r["aOR"]} ({r["aOR_lo"]}\u2013{r["aOR_hi"]}){star}</text>\n'
    s+=f'<text x="{pl+pw/2:.0f}" y="{h-16}" font-size="12" fill="{C["muted"]}" text-anchor="middle">Adjusted odds ratio (log scale) \u2014 * p &lt; 0.05</text>\n'
    s+="</svg>\n"; open(os.path.join(OUT,"fig2_forest.svg"),"w").write(s)

# ---------- Figure 3: outcome rates by sex ----------
def fig3():
    w,h=720,440; pl,pt,pb,pr=70,70,90,30; ph=h-pt-pb; pw=w-pl-pr
    pg=R["primary_good"]; sec=R["secondary"]
    groups=["Good outcome\n(mRS 0-2)","In-hospital\nmortality","Discharge\nto home"]
    women=[pg["women_pct"],sec["death"]["women_pct"],sec["home"]["women_pct"]]
    men=[pg["men_pct"],sec["death"]["men_pct"],sec["home"]["men_pct"]]
    series=[("Women",women,C["women"]),("Men",men,C["men"])]
    vmax=70
    s=head(w,h)
    s+=f'<text x="20" y="28" font-size="16" font-weight="bold" fill="{C["text"]}">Figure 3. Early clinical outcomes by sex</text>\n'
    for g in range(0,6):
        gy=pt+ph*(1-g/5); gv=vmax*g/5
        s+=f'<line x1="{pl}" y1="{gy:.1f}" x2="{w-pr}" y2="{gy:.1f}" stroke="{C["grid"]}"/>\n'
        s+=f'<text x="{pl-8}" y="{gy+4:.1f}" font-size="11" fill="{C["muted"]}" text-anchor="end">{gv:.0f}%</text>\n'
    ng=len(groups); gw=pw/ng; bw=gw*0.7/len(series)
    for gi,gname in enumerate(groups):
        gx0=pl+gi*gw+gw*0.15
        for si,(sname,vals,col) in enumerate(series):
            v=vals[gi]; bh=ph*v/vmax; bx=gx0+si*bw; by=pt+ph-bh
            s+=f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw-4:.1f}" height="{bh:.1f}" fill="{col}" rx="2"/>\n'
            s+=f'<text x="{bx+(bw-4)/2:.1f}" y="{by-6:.1f}" font-size="12" font-weight="bold" fill="{C["text"]}" text-anchor="middle">{v}</text>\n'
        for li,part in enumerate(gname.split("\n")):
            s+=f'<text x="{pl+gi*gw+gw/2:.1f}" y="{pt+ph+20+li*15:.1f}" font-size="12" fill="{C["text"]}" text-anchor="middle">{part}</text>\n'
    s+=f'<line x1="{pl}" y1="{pt+ph}" x2="{w-pr}" y2="{pt+ph}" stroke="{C["axis"]}"/>\n'
    s+=f'<line x1="{pl}" y1="{pt}" x2="{pl}" y2="{pt+ph}" stroke="{C["axis"]}"/>\n'
    lx=pl; ly=h-24
    for sname,_,col in series:
        s+=f'<rect x="{lx}" y="{ly-11}" width="14" height="14" fill="{col}"/>\n'
        s+=f'<text x="{lx+19}" y="{ly}" font-size="12" fill="{C["text"]}">{sname}</text>\n'; lx+=70
    s+="</svg>\n"; open(os.path.join(OUT,"fig3_outcomes.svg"),"w").write(s)

fig1(); fig2(); fig3()
print("Figures written to", OUT)
for f in sorted(os.listdir(OUT)): print(" -", f)
