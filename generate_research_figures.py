#!/usr/bin/env python3
"""Generate 4 publication-style figures for the AI-Driven Research Support
chapter, using the pure-Python purepng toolkit (no matplotlib / Pillow)."""

import os
from purepng import Canvas

OUT = '/projects/sandbox/AMMAN/research_figures'
os.makedirs(OUT, exist_ok=True)

# palette
NAVY = (27, 54, 93)
BLUE = (46, 117, 182)
LBLUE = (189, 215, 238)
TEAL = (56, 142, 142)
GREEN = (84, 158, 96)
ORANGE = (221, 132, 58)
AMBER = (233, 179, 60)
RED = (192, 80, 77)
PURPLE = (112, 88, 168)
GREY = (110, 110, 118)
LGREY = (232, 234, 238)
DARK = (35, 40, 52)
WHITE = (255, 255, 255)


# ============================================================ FIGURE 1
def figure1():
    """Research lifecycle augmented by AI (circular / staged pipeline)."""
    W, H = 1500, 900
    c = Canvas(W, H, WHITE)
    c.text_center(W // 2, 34, "AI Augmentation Across the Research Lifecycle",
                  NAVY, scale=4)
    c.line(220, 108, W - 220, 108, BLUE, 3)

    stages = [
        ("Problem &", "Hypothesis", BLUE),
        ("Literature", "Discovery", TEAL),
        ("Design &", "Planning", GREEN),
        ("Data", "Management", AMBER),
        ("Analysis &", "Interpretation", ORANGE),
        ("Writing &", "Dissemination", PURPLE),
    ]
    n = len(stages)
    box_w, box_h = 190, 96
    gap = (W - 2 * 70 - n * box_w) / (n - 1)
    y = 175
    centers = []
    for i, (l1, l2, col) in enumerate(stages):
        x0 = 70 + i * (box_w + gap)
        c.round_panel(x0, y, x0 + box_w, y + box_h, col, r=14)
        cx = x0 + box_w / 2
        c.text_center(cx, y + 26, l1, WHITE, scale=2)
        c.text_center(cx, y + 52, l2, WHITE, scale=2)
        c.text_center(cx, y - 26, "0" + str(i + 1), col, scale=3)
        centers.append((cx, y + box_h))
        if i < n - 1:
            c.arrow(x0 + box_w + 4, y + box_h / 2,
                    x0 + box_w + gap - 4, y + box_h / 2, GREY, 3, 12)

    # AI capability band beneath, connecting to each stage
    band_y = 430
    c.round_panel(70, band_y, W - 70, band_y + 60, NAVY, r=16)
    c.text_center(W // 2, band_y + 20, "Cross-Cutting AI Capabilities Layer",
                  WHITE, scale=3)
    for cx, by in centers:
        c.arrow(cx, by + 4, cx, band_y - 4, GREY, 2, 9)

    caps = [
        ("NLP &", "Language Models", TEAL),
        ("Machine", "Learning", GREEN),
        ("Knowledge", "Graphs", AMBER),
        ("Retrieval &", "Search", ORANGE),
        ("Predictive", "Analytics", PURPLE),
        ("Automation &", "Agents", BLUE),
    ]
    cy = 560
    cbw = 205
    cgap = (W - 140 - len(caps) * cbw) / (len(caps) - 1)
    for i, (l1, l2, col) in enumerate(caps):
        x0 = 70 + i * (cbw + cgap)
        c.round_panel(x0, cy, x0 + cbw, cy + 92, LBLUE, r=12, border=col, bt=3)
        cx = x0 + cbw / 2
        c.arrow(cx, band_y + 60 + 2, cx, cy - 4, GREY, 2, 9)
        c.text_center(cx, cy + 26, l1, DARK, scale=2)
        c.text_center(cx, cy + 52, l2, DARK, scale=2)

    # outcomes bar
    oy = 720
    c.round_panel(70, oy, W - 70, oy + 78, LGREY, r=14, border=NAVY, bt=2)
    c.text_center(W // 2, oy + 14, "Outcomes: Efficiency  +  Reproducibility  +  Scholarly Impact",
                  NAVY, scale=3)
    c.text_center(W // 2, oy + 46,
                  "Human oversight and responsible use span the entire cycle",
                  GREY, scale=2)
    c.rect_outline(8, 8, W - 8, H - 8, LGREY, 3)
    c.save(os.path.join(OUT, "Figure_1_Research_Lifecycle.png"))


# ============================================================ FIGURE 2
def figure2():
    """Grouped bar chart: adoption of AI tools across research stages."""
    W, H = 1500, 900
    c = Canvas(W, H, WHITE)
    c.text_center(W // 2, 30, "Reported Adoption of AI Tools Across Research Stages",
                  NAVY, scale=4)
    c.text_center(W // 2, 82, "Illustrative survey data (percentage of researchers)",
                  GREY, scale=2)

    ox, oy = 150, 720           # origin (bottom-left of plot)
    pw, ph = W - 260, 560       # plot area
    top = oy - ph
    # axes
    c.line(ox, oy, ox + pw, oy, DARK, 3)
    c.line(ox, oy, ox, top, DARK, 3)
    # gridlines + y labels
    for v in range(0, 101, 20):
        yy = oy - ph * v / 100
        c.line(ox, yy, ox + pw, yy, LGREY, 1)
        c.text(ox - 70, yy - 8, str(v) + "%", GREY, 2)

    groups = ["Lit.\nReview", "Data\nMgmt", "Analysis", "Writing", "Dissem."]
    # two series: Current use vs Planned use
    current = [71, 44, 52, 63, 38]
    planned = [88, 69, 74, 81, 66]
    gw = pw / len(groups)
    bw = 62
    for i in range(len(groups)):
        gx = ox + i * gw + gw / 2
        # current
        h1 = ph * current[i] / 100
        c.rect(gx - bw - 6, oy - h1, gx - 6, oy, BLUE)
        c.text_center(gx - bw / 2 - 6, oy - h1 - 26, str(current[i]) + "%", BLUE, 2)
        # planned
        h2 = ph * planned[i] / 100
        c.rect(gx + 6, oy - h2, gx + bw + 6, oy, ORANGE)
        c.text_center(gx + bw / 2 + 6, oy - h2 - 26, str(planned[i]) + "%", ORANGE, 2)
        # x label (two lines)
        parts = groups[i].split("\n")
        c.text_center(gx, oy + 16, parts[0], DARK, 2)
        if len(parts) > 1:
            c.text_center(gx, oy + 40, parts[1], DARK, 2)

    # legend
    lx, ly = ox + pw - 300, top + 10
    c.rect(lx, ly, lx + 26, ly + 26, BLUE)
    c.text(lx + 36, ly + 4, "Current use", DARK, 2)
    c.rect(lx, ly + 40, lx + 26, ly + 66, ORANGE)
    c.text(lx + 36, ly + 44, "Planned within 2 yrs", DARK, 2)
    c.text(ox - 100, top - 30, "Adoption", GREY, 2)
    c.rect_outline(8, 8, W - 8, H - 8, LGREY, 3)
    c.save(os.path.join(OUT, "Figure_2_Adoption_Bar.png"))


# ============================================================ FIGURE 3
def figure3():
    """FAIR-aligned AI research data management architecture (layered)."""
    W, H = 1560, 950
    c = Canvas(W, H, WHITE)
    c.text_center(W // 2, 32, "AI-Enabled, FAIR-Aligned Research Data Architecture",
                  NAVY, scale=4)
    c.line(230, 106, W - 230, 106, BLUE, 3)

    layers = [
        ("SOURCES", "Instruments  |  Surveys  |  Simulations  |  Repositories  |  Text Corpora", GREY),
        ("INGESTION & CURATION", "AI classification  |  Auto metadata  |  Cleaning  |  Harmonization", TEAL),
        ("QUALITY & VALIDATION", "Anomaly detection  |  Missing-value imputation  |  Consistency checks", GREEN),
        ("STORAGE & DISCOVERY", "FAIR repositories  |  Semantic search  |  Knowledge organization", AMBER),
        ("GOVERNANCE & SECURITY", "Access control  |  Encryption  |  Privacy-preserving analytics", RED),
    ]
    x0, x1 = 90, W - 260
    y = 140
    lh = 118
    gap = 22
    layer_centers = []
    for name, sub, col in layers:
        c.round_panel(x0, y, x1, y + lh, LBLUE, r=16, border=col, bt=4)
        c.rect(x0, y + 14, x0 + 14, y + lh - 14, col)
        c.text(x0 + 40, y + 30, name, col, 3)
        c.text(x0 + 40, y + 72, sub, DARK, 2)
        layer_centers.append(y + lh / 2)
        if len(layer_centers) > 1:
            midx = (x0 + x1) / 2
            c.arrow(midx, layer_centers[-2] + lh / 2 - 2,
                    midx, y - 4, GREY, 2, 9)
        y += lh + gap

    # FAIR badges on the right, aligned to the layers
    bx = x1 + 55
    c.round_panel(bx - 20, 140, W - 40, y - gap, LGREY, r=16, border=BLUE, bt=3)
    c.text_center((bx - 20 + W - 40) / 2, 152, "FAIR", NAVY, 3)
    labels = [("F", "Findable"), ("A", "Accessible"),
              ("I", "Interoperable"), ("R", "Reusable")]
    ry = 210
    for letter, word in labels:
        badge_cx = (bx - 20 + W - 40) / 2
        c.circle(badge_cx, ry + 22, 24, BLUE, fill=True)
        c.text_center(badge_cx, ry + 10, letter, WHITE, 3)
        c.text_center(badge_cx, ry + 58, word, DARK, 2)
        ry += 150
    c.rect_outline(8, 8, W - 8, H - 8, LGREY, 3)
    c.save(os.path.join(OUT, "Figure_3_Data_Architecture.png"))


# ============================================================ FIGURE 4
def figure4():
    """Line chart: growth of AI-assisted research outputs / time savings."""
    W, H = 1500, 900
    c = Canvas(W, H, WHITE)
    c.text_center(W // 2, 30, "Trends in AI-Assisted Research Productivity",
                  NAVY, scale=4)
    c.text_center(W // 2, 82, "Illustrative index, 2019 = baseline (100)", GREY, 2)

    ox, oy = 160, 730
    pw, ph = W - 300, 560
    top = oy - ph
    c.line(ox, oy, ox + pw, oy, DARK, 3)
    c.line(ox, oy, ox, top, DARK, 3)

    ymin, ymax = 80, 320
    for v in range(80, 321, 40):
        yy = oy - ph * (v - ymin) / (ymax - ymin)
        c.line(ox, yy, ox + pw, yy, LGREY, 1)
        c.text(ox - 80, yy - 8, str(v), GREY, 2)

    years = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
    lit = [100, 118, 140, 172, 210, 248, 282, 305]      # literature discovery
    analysis = [100, 110, 126, 150, 178, 205, 232, 258]  # analysis automation
    writing = [100, 106, 120, 148, 190, 232, 268, 296]   # writing assistance

    def X(i):
        return ox + pw * i / (len(years) - 1)

    def Y(v):
        return oy - ph * (v - ymin) / (ymax - ymin)

    series = [("Literature discovery", lit, BLUE),
              ("Analysis automation", analysis, GREEN),
              ("Writing assistance", writing, ORANGE)]
    for name, data, col in series:
        for i in range(len(data) - 1):
            c.line(X(i), Y(data[i]), X(i + 1), Y(data[i + 1]), col, 4)
        for i, v in enumerate(data):
            c.circle(X(i), Y(v), 6, col, fill=True)

    for i, yr in enumerate(years):
        c.text_center(X(i), oy + 16, str(yr), DARK, 2)

    # legend
    lx, ly = ox + 20, top + 6
    for name, data, col in series:
        c.rect(lx, ly, lx + 26, ly + 12, col)
        c.text(lx + 36, ly - 4, name, DARK, 2)
        ly += 34
    c.text(ox - 120, top - 28, "Index", GREY, 2)
    c.rect_outline(8, 8, W - 8, H - 8, LGREY, 3)
    c.save(os.path.join(OUT, "Figure_4_Productivity_Trends.png"))


if __name__ == '__main__':
    figure1()
    figure2()
    figure3()
    figure4()
    for f in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, f)
        print(f"{f:45s} {os.path.getsize(p)/1024:7.1f} KB")
