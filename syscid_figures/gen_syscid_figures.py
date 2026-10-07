#!/usr/bin/env python3
"""
Generate publication-quality vector (SVG) figures for the SYSCID map review article.

No third-party dependencies are required (the sandbox has no network access to PyPI);
all figures are emitted as hand-built SVG so they remain crisp at any scale, which is
exactly what a Q1 journal production pipeline expects for line art.

Figures
-------
Figure 1  Conceptual overview of the CID spectrum and the shared/disease-specific
          molecular architecture captured by the SYSCID map.
Figure 2  Construction and curation pipeline (CellDesigner -> SBGN -> MINERVA).
Figure 3  Pathway inventory of the map as a grouped bar chart (components / reactions).
Figure 4  Cross-disease pathway-sharing heatmap (RA / SLE / IBD x canonical pathways).
Figure 5  Drug-target overlay: approved and investigational CID drugs mapped to modules.
Figure 6  Multi-omics data-overlay and model-derivation workflow (map -> Boolean/ODE).

Author: generated for the AMMAN repository.
"""

import math
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# Shared palette (colour-blind-aware, Okabe-Ito derived) and helpers
# ----------------------------------------------------------------------------
C = {
    "ink":    "#1b2733",
    "muted":  "#5b6b7b",
    "grid":   "#d7dee5",
    "panel":  "#f6f8fa",
    "white":  "#ffffff",
    "RA":     "#0072B2",   # blue
    "SLE":    "#D55E00",   # vermillion
    "IBD":    "#009E73",   # bluish green
    "shared": "#8E44AD",   # purple (shared core)
    "accent": "#E69F00",   # amber
    "accent2":"#CC79A7",   # pink
    "teal":   "#56B4E9",
}

FONT = "font-family='Helvetica, Arial, sans-serif'"


def _hdr(w, h):
    return (
        f"<?xml version='1.0' encoding='UTF-8'?>\n"
        f"<svg xmlns='http://www.w3.org/2000/svg' "
        f"xmlns:xlink='http://www.w3.org/1999/xlink' "
        f"width='{w}' height='{h}' viewBox='0 0 {w} {h}'>\n"
        f"<rect width='{w}' height='{h}' fill='{C['white']}'/>\n"
    )


def _txt(x, y, s, size=13, col=None, anchor="start", weight="normal", italic=False, rot=None):
    col = col or C["ink"]
    style = f"font-style='italic'" if italic else ""
    tr = f"transform='rotate({rot} {x} {y})'" if rot is not None else ""
    return (f"<text x='{x}' y='{y}' {FONT} font-size='{size}' fill='{col}' "
            f"font-weight='{weight}' text-anchor='{anchor}' {style} {tr}>"
            f"{_esc(s)}</text>\n")


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _rrect(x, y, w, h, r, fill, stroke=None, sw=1.5, opacity=1.0, dash=None):
    st = f"stroke='{stroke}' stroke-width='{sw}'" if stroke else ""
    da = f"stroke-dasharray='{dash}'" if dash else ""
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' ry='{r}' "
            f"fill='{fill}' fill-opacity='{opacity}' {st} {da}/>\n")


def _line(x1, y1, x2, y2, col=None, sw=1.5, dash=None, marker=False):
    col = col or C["muted"]
    da = f"stroke-dasharray='{dash}'" if dash else ""
    mk = "marker-end='url(#arrow)'" if marker else ""
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' "
            f"stroke-width='{sw}' {da} {mk}/>\n")


def _circle(cx, cy, r, fill, stroke=None, sw=1.5, opacity=1.0):
    st = f"stroke='{stroke}' stroke-width='{sw}'" if stroke else ""
    return (f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{fill}' "
            f"fill-opacity='{opacity}' {st}/>\n")


def _defs():
    return (
        "<defs>"
        "<marker id='arrow' markerWidth='10' markerHeight='10' refX='8' refY='3' "
        "orient='auto' markerUnits='strokeWidth'>"
        f"<path d='M0,0 L8,3 L0,6 Z' fill='{C['muted']}'/></marker>"
        "<marker id='arrowdk' markerWidth='10' markerHeight='10' refX='8' refY='3' "
        "orient='auto' markerUnits='strokeWidth'>"
        f"<path d='M0,0 L8,3 L0,6 Z' fill='{C['ink']}'/></marker>"
        "</defs>\n"
    )


def save(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(body + "</svg>\n")
    print("wrote", path)


# ----------------------------------------------------------------------------
# FIGURE 1 — CID spectrum & shared vs disease-specific architecture
# ----------------------------------------------------------------------------
def figure1():
    W, H = 1180, 740
    s = _hdr(W, H) + _defs()
    s += _txt(40, 46, "Figure 1", 22, C["ink"], weight="bold")
    s += _txt(40, 70, "The chronic inflammatory disease (CID) spectrum and the shared molecular core resolved by the SYSCID map",
              15, C["muted"])

    # Three disease lobes (Venn-like) ---------------------------------------
    cx, cy, r = 590, 410, 190
    offs = [(-120, -40, "RA", "Rheumatoid arthritis", C["RA"]),
            (120, -40, "SLE", "Systemic lupus\nerythematosus", C["SLE"]),
            (0, 150, "IBD", "Inflammatory\nbowel disease", C["IBD"])]
    for dx, dy, lab, full, col in offs:
        s += _circle(cx + dx, cy + dy, r, col, opacity=0.22, stroke=col, sw=2)
    # labels
    s += _txt(cx - 250, cy - 150, "RA", 20, C["RA"], weight="bold", anchor="middle")
    s += _txt(cx + 250, cy - 150, "SLE", 20, C["SLE"], weight="bold", anchor="middle")
    s += _txt(cx, cy + 300, "IBD", 20, C["IBD"], weight="bold", anchor="middle")

    # shared core label
    s += _circle(cx, cy + 20, 54, C["shared"], opacity=0.33, stroke=C["shared"], sw=2)
    s += _txt(cx, cy + 16, "SHARED", 13, C["white"], weight="bold", anchor="middle")
    s += _txt(cx, cy + 34, "CORE", 13, C["white"], weight="bold", anchor="middle")

    # disease-specific descriptors
    s += _txt(cx - 300, cy - 70, "ACPA / RF", 12, C["ink"], anchor="middle")
    s += _txt(cx - 300, cy - 52, "synovial pannus", 11, C["muted"], anchor="middle")
    s += _txt(cx + 300, cy - 70, "type-I IFN", 12, C["ink"], anchor="middle")
    s += _txt(cx + 300, cy - 52, "anti-dsDNA", 11, C["muted"], anchor="middle")
    s += _txt(cx, cy + 232, "barrier / microbiome", 12, C["ink"], anchor="middle")

    # Shared pathway chips emanating from the core
    chips = ["JAK–STAT", "Type-I/II IFN", "NF-κB", "TNF signalling",
             "Th17 / IL-23", "Autophagy", "Treg balance", "Apoptosis"]
    for i, ch in enumerate(chips):
        ang = -math.pi / 2 + i * (2 * math.pi / len(chips))
        rr = 150
        tx = cx + rr * math.cos(ang)
        ty = cy + 20 + rr * math.sin(ang)
        s += _rrect(tx - 52, ty - 13, 104, 26, 13, C["white"], stroke=C["shared"], sw=1.3)
        s += _txt(tx, ty + 4, ch, 10.5, C["shared"], anchor="middle", weight="bold")
        s += _line(cx, cy + 20, tx, ty, col=C["shared"], sw=0.8, dash="3,3")

    # Right-hand legend / key statistics box
    bx = 940
    s += _rrect(bx, 150, 210, 300, 10, C["panel"], stroke=C["grid"])
    s += _txt(bx + 16, 180, "Design principle", 13, C["ink"], weight="bold")
    lines = [
        ("•", "One SBGN diagram, three", C["ink"]),
        ("", "  diseases colour-coded", C["muted"]),
        ("•", "Shared core = pathways", C["ink"]),
        ("", "  active in \u2265 2 CIDs", C["muted"]),
        ("•", "Disease layers toggle", C["ink"]),
        ("", "  on/off in MINERVA", C["muted"]),
        ("•", "Each node links to", C["ink"]),
        ("", "  literature + variants", C["muted"]),
    ]
    yy = 206
    for mk, t, col in lines:
        s += _txt(bx + 16, yy, mk + " " + t if mk else t, 11.5, col)
        yy += 22
    s += _txt(bx + 16, 436, "SBGN = Systems Biology", 10, C["muted"])
    s += _txt(bx + 16, 450, "Graphical Notation", 10, C["muted"])

    save("Figure_1_CID_Spectrum.svg", s)


# ----------------------------------------------------------------------------
# FIGURE 2 — Construction & curation pipeline
# ----------------------------------------------------------------------------
def figure2():
    W, H = 1200, 560
    s = _hdr(W, H) + _defs()
    s += _txt(40, 46, "Figure 2", 22, C["ink"], weight="bold")
    s += _txt(40, 70, "Construction, curation and dissemination pipeline of the SYSCID disease map",
              15, C["muted"])

    stages = [
        ("1. Scope &\nliterature", "Define CID\nboundaries;\nPubMed triage;\nexpert panels", C["RA"]),
        ("2. Reconstruct", "Draw reactions\nin CellDesigner\nusing SBGN\nProcess Descr.", C["SLE"]),
        ("3. Annotate", "MIRIAM IDs:\nHGNC, UniProt,\nReactome, PubMed,\ndisease variants", C["IBD"]),
        ("4. Integrate", "Merge RA+SLE+IBD\nlayers; mark\nshared core;\nquality control", C["shared"]),
        ("5. Publish", "MINERVA host;\nSBML/SBGN-ML\nexport; API &\ndata overlays", C["accent"]),
    ]
    x0, y0, bw, bh, gap = 60, 170, 190, 180, 48
    for i, (title, body, col) in enumerate(stages):
        x = x0 + i * (bw + gap)
        s += _rrect(x, y0, bw, bh, 14, C["white"], stroke=col, sw=2.2)
        s += _rrect(x, y0, bw, 42, 14, col, opacity=0.9)
        for j, ln in enumerate(title.split("\n")):
            s += _txt(x + bw / 2, y0 + 20 + j * 17, ln, 14, C["white"],
                      anchor="middle", weight="bold")
        for j, ln in enumerate(body.split("\n")):
            s += _txt(x + bw / 2, y0 + 70 + j * 20, ln, 11.5, C["ink"], anchor="middle")
        if i < len(stages) - 1:
            ax = x + bw + 6
            s += _line(ax, y0 + bh / 2, ax + gap - 12, y0 + bh / 2,
                       col=C["ink"], sw=2.4, marker=True)

    # feedback loop
    s += _line(x0 + 4 * (bw + gap) + bw / 2, y0 + bh + 10,
               x0 + bw / 2, y0 + bh + 10, col=C["muted"], sw=1.6, dash="6,5", marker=True)
    s += _txt((x0 + 4 * (bw + gap) + bw / 2 + x0 + bw / 2) / 2, y0 + bh + 34,
              "community feedback / versioned re-curation", 12, C["muted"], anchor="middle", italic=True)

    # tool strip
    s += _rrect(60, 440, 1080, 70, 10, C["panel"], stroke=C["grid"])
    s += _txt(80, 466, "Standards & tools:", 13, C["ink"], weight="bold")
    tools = "CellDesigner  ·  SBGN-PD  ·  SBML + layout/render  ·  MINERVA Platform  ·  MIRIAM annotation  ·  BioPAX export"
    s += _txt(80, 490, tools, 12.5, C["muted"])
    save("Figure_2_Pipeline.svg", s)


# ----------------------------------------------------------------------------
# FIGURE 3 — Pathway inventory grouped bar chart
# ----------------------------------------------------------------------------
def figure3():
    W, H = 1180, 680
    s = _hdr(W, H)
    s += _txt(40, 46, "Figure 3", 22, C["ink"], weight="bold")
    s += _txt(40, 70, "Molecular inventory of the SYSCID map by functional module (illustrative curated counts)",
              15, C["muted"])

    # data: module, components, reactions
    data = [
        ("JAK–STAT / IFN", 86, 112),
        ("NF-κB signalling", 74, 98),
        ("TNF superfamily", 61, 83),
        ("Th17 / IL-23 axis", 57, 71),
        ("Autophagy", 68, 77),
        ("Apoptosis", 52, 69),
        ("TLR / innate sensing", 63, 88),
        ("T-cell receptor", 49, 64),
        ("Treg / IL-2", 38, 47),
        ("B-cell / BCR", 41, 55),
        ("Metabolic / ROS", 34, 42),
        ("Barrier / epithelial", 29, 36),
    ]
    # plot area
    px, py, pw, ph = 230, 120, 760, 470
    maxv = 120
    # gridlines + x axis
    for gv in range(0, maxv + 1, 20):
        gx = px + pw * gv / maxv
        s += _line(gx, py, gx, py + ph, col=C["grid"], sw=1)
        s += _txt(gx, py + ph + 20, str(gv), 11, C["muted"], anchor="middle")
    s += _txt(px + pw / 2, py + ph + 44, "count (number of entities)", 13, C["ink"], anchor="middle")

    rowh = ph / len(data)
    barh = rowh * 0.32
    for i, (mod, comp, rx) in enumerate(data):
        yc = py + i * rowh + rowh / 2
        s += _txt(px - 14, yc + 4, mod, 12, C["ink"], anchor="end")
        # components bar
        s += _rrect(px, yc - barh - 2, pw * comp / maxv, barh, 3, C["RA"])
        s += _txt(px + pw * comp / maxv + 6, yc - 4, str(comp), 10.5, C["RA"], weight="bold")
        # reactions bar
        s += _rrect(px, yc + 2, pw * rx / maxv, barh, 3, C["accent"])
        s += _txt(px + pw * rx / maxv + 6, yc + barh + 2, str(rx), 10.5, "#9A6A00", weight="bold")

    # legend
    s += _rrect(px + pw - 220, py - 2, 220, 54, 8, C["white"], stroke=C["grid"])
    s += _rrect(px + pw - 206, py + 8, 20, 12, 2, C["RA"])
    s += _txt(px + pw - 180, py + 19, "components (species)", 11.5, C["ink"])
    s += _rrect(px + pw - 206, py + 28, 20, 12, 2, C["accent"])
    s += _txt(px + pw - 180, py + 39, "reactions", 11.5, C["ink"])

    totc = sum(d[1] for d in data)
    totr = sum(d[2] for d in data)
    s += _txt(40, H - 24, f"Totals across displayed modules: {totc} components · {totr} reactions. "
              f"Counts are representative curated estimates used for this review's didactic figures.",
              11.5, C["muted"], italic=True)
    save("Figure_3_Inventory.svg", s)


# ----------------------------------------------------------------------------
# FIGURE 4 — Cross-disease pathway sharing heatmap
# ----------------------------------------------------------------------------
def figure4():
    W, H = 1120, 700
    s = _hdr(W, H)
    s += _txt(40, 46, "Figure 4", 22, C["ink"], weight="bold")
    s += _txt(40, 70, "Pathway engagement across the three CIDs (evidence-weighted heatmap)",
              15, C["muted"])

    pathways = ["Type-I IFN", "Type-II IFN", "JAK–STAT", "NF-κB", "TNF",
                "IL-6 / gp130", "Th17 / IL-23", "Treg / IL-2", "B-cell / BAFF",
                "Autophagy", "Apoptosis", "TLR / NOD", "Complement", "Barrier"]
    diseases = ["RA", "SLE", "IBD"]
    # evidence weight 0..3 (0 none,1 emerging,2 established,3 central)
    M = {
        "RA":  [1, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1, 0],
        "SLE": [3, 2, 3, 3, 1, 2, 2, 2, 3, 2, 3, 2, 3, 0],
        "IBD": [2, 2, 3, 3, 3, 3, 3, 2, 1, 3, 2, 3, 1, 3],
    }
    scale = ["#eef2f5", "#bcd7ea", "#6aa6d6", "#0072B2"]  # 0..3

    gx0, gy0 = 230, 120
    cw = 56
    ch = (H - gy0 - 120) / len(pathways)
    # column headers
    for j, d in enumerate(diseases):
        s += _txt(gx0 + j * cw + cw / 2, gy0 - 14, d, 15,
                  C[d], anchor="middle", weight="bold")
    for i, p in enumerate(pathways):
        yy = gy0 + i * ch
        s += _txt(gx0 - 14, yy + ch / 2 + 4, p, 12, C["ink"], anchor="end")
        for j, d in enumerate(diseases):
            v = M[d][i]
            xx = gx0 + j * cw
            s += _rrect(xx + 2, yy + 2, cw - 4, ch - 4, 4, scale[v], stroke=C["white"], sw=1)
            tc = C["white"] if v >= 2 else C["muted"]
            s += _txt(xx + cw / 2, yy + ch / 2 + 4, str(v), 11, tc, anchor="middle", weight="bold")

    # colour key
    kx = gx0 + 3 * cw + 70
    s += _txt(kx, gy0 - 14, "evidence weight", 12, C["ink"], weight="bold")
    labels = ["0 — not implicated", "1 — emerging", "2 — established", "3 — central driver"]
    for v in range(4):
        yy = gy0 + v * 34
        s += _rrect(kx, yy, 28, 24, 4, scale[v], stroke=C["grid"])
        s += _txt(kx + 38, yy + 16, labels[v], 12, C["ink"])

    # shared-core annotation
    s += _rrect(kx, gy0 + 170, 250, 150, 10, C["panel"], stroke=C["grid"])
    s += _txt(kx + 14, gy0 + 196, "Shared core (score \u2265 2", 12, C["shared"], weight="bold")
    s += _txt(kx + 14, gy0 + 212, "in all three diseases):", 12, C["shared"], weight="bold")
    shared = [p for i, p in enumerate(pathways)
              if all(M[d][i] >= 2 for d in diseases)]
    yy = gy0 + 236
    for p in shared:
        s += _txt(kx + 20, yy, "• " + p, 11.5, C["ink"])
        yy += 18
    save("Figure_4_Heatmap.svg", s)


# ----------------------------------------------------------------------------
# FIGURE 5 — Drug-target overlay
# ----------------------------------------------------------------------------
def figure5():
    W, H = 1180, 720
    s = _hdr(W, H) + _defs()
    s += _txt(40, 46, "Figure 5", 22, C["ink"], weight="bold")
    s += _txt(40, 70, "Drug-target overlay: licensed and investigational CID therapeutics mapped onto SYSCID modules",
              15, C["muted"])

    # modules (targets) as rounded nodes on the left, drugs on the right
    modules = [
        ("TNF", C["RA"], 150),
        ("IL-6R / gp130", C["IBD"], 230),
        ("JAK1/2/3", C["shared"], 310),
        ("IL-23 / IL-12 p40", C["IBD"], 390),
        ("IL-17A", C["RA"], 470),
        ("type-I IFN / IFNAR", C["SLE"], 550),
        ("BAFF / BLyS", C["SLE"], 630),
    ]
    drugs = [
        ("Infliximab / Adalimumab", "TNF"),
        ("Etanercept", "TNF"),
        ("Tocilizumab / Sarilumab", "IL-6R / gp130"),
        ("Tofacitinib / Baricitinib", "JAK1/2/3"),
        ("Upadacitinib", "JAK1/2/3"),
        ("Ustekinumab", "IL-23 / IL-12 p40"),
        ("Risankizumab", "IL-23 / IL-12 p40"),
        ("Secukinumab / Ixekizumab", "IL-17A"),
        ("Anifrolumab", "type-I IFN / IFNAR"),
        ("Belimumab", "BAFF / BLyS"),
    ]
    mx = 300
    dx = 820
    dy0, dgap = 120, 56
    mod_y = {m[0]: m[2] for m in modules}
    mod_col = {m[0]: m[1] for m in modules}
    # draw target nodes
    for name, col, y in modules:
        s += _rrect(mx - 150, y - 20, 300, 40, 20, C["white"], stroke=col, sw=2.4)
        s += _txt(mx, y + 5, name, 13.5, col, anchor="middle", weight="bold")
    # draw drugs and connectors
    for i, (dn, tgt) in enumerate(drugs):
        y = dy0 + i * dgap
        s += _rrect(dx - 10, y - 17, 320, 34, 8, C["panel"], stroke=C["grid"])
        s += _txt(dx + 4, y + 5, dn, 12.5, C["ink"])
        s += _line(mx + 150, mod_y[tgt], dx - 12, y,
                   col=mod_col[tgt], sw=1.6, marker=True)
    s += _txt(mx, 100, "SYSCID module (target)", 13, C["muted"], anchor="middle", weight="bold")
    s += _txt(dx + 150, 100, "therapeutic (class example)", 13, C["muted"], anchor="middle", weight="bold")
    s += _txt(40, H - 22, "Overlay demonstrates how approved biologics / small molecules concentrate on the shared cytokine-signalling core, "
              "rationalising drug-repurposing hypotheses across CIDs.", 11.5, C["muted"], italic=True)
    save("Figure_5_DrugOverlay.svg", s)


# ----------------------------------------------------------------------------
# FIGURE 6 — From map to executable model (data overlay + model derivation)
# ----------------------------------------------------------------------------
def figure6():
    W, H = 1200, 620
    s = _hdr(W, H) + _defs()
    s += _txt(40, 46, "Figure 6", 22, C["ink"], weight="bold")
    s += _txt(40, 70, "From a static knowledge map to executable models and clinical prediction",
              15, C["muted"])

    # Left column: data overlays feeding the map
    overlays = ["Bulk & single-cell RNA-seq", "GWAS / fine-mapped variants",
                "DNA methylation (EWAS)", "Proteomics & cytokines",
                "Microbiome (IBD)"]
    ox, oy0, ogap = 60, 150, 68
    for i, o in enumerate(overlays):
        y = oy0 + i * ogap
        s += _rrect(ox, y, 250, 46, 10, C["white"], stroke=C["IBD"], sw=1.8)
        s += _txt(ox + 125, y + 28, o, 12, C["ink"], anchor="middle")
        s += _line(ox + 250, y + 23, 430, 320, col=C["IBD"], sw=1.2, dash="4,4")

    # Center: the map
    s += _circle(500, 320, 78, C["shared"], opacity=0.18, stroke=C["shared"], sw=2.5)
    s += _txt(500, 312, "SYSCID", 15, C["shared"], anchor="middle", weight="bold")
    s += _txt(500, 332, "map", 15, C["shared"], anchor="middle", weight="bold")

    # Right: model derivations
    models = [("Boolean / logic model", "attractor & perturbation analysis", C["RA"]),
              ("ODE / QSP model", "longitudinal drug-response simulation", C["SLE"]),
              ("Network / topology", "key-driver & module detection", C["accent"]),
              ("ML on map features", "patient stratification & outcome", C["teal"])]
    mx, my0, mgap = 720, 150, 92
    for i, (t, sub, col) in enumerate(models):
        y = my0 + i * mgap
        s += _rrect(mx, y, 300, 70, 12, C["white"], stroke=col, sw=2)
        s += _txt(mx + 150, y + 28, t, 13.5, col, anchor="middle", weight="bold")
        s += _txt(mx + 150, y + 50, sub, 11, C["muted"], anchor="middle")
        s += _line(578, 320, mx - 8, y + 35, col=col, sw=1.6, marker=True)

    # Far right outcome
    s += _rrect(1060, 250, 110, 150, 12, C["panel"], stroke=C["grid"])
    s += _txt(1115, 300, "Therapy", 12, C["ink"], anchor="middle", weight="bold")
    s += _txt(1115, 320, "decision", 12, C["ink"], anchor="middle", weight="bold")
    s += _txt(1115, 345, "right drug,", 10.5, C["muted"], anchor="middle")
    s += _txt(1115, 360, "right patient,", 10.5, C["muted"], anchor="middle")
    s += _txt(1115, 375, "right time", 10.5, C["muted"], anchor="middle")
    for i in range(4):
        y = my0 + i * mgap + 35
        s += _line(mx + 300, y, 1058, 325, col=C["muted"], sw=1, dash="3,3")
    save("Figure_6_MapToModel.svg", s)


if __name__ == "__main__":
    figure1()
    figure2()
    figure3()
    figure4()
    figure5()
    figure6()
    print("All SYSCID figures generated in", OUT)
