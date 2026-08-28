#!/usr/bin/env python3
"""Generate 4 PNG figures for the Industry 5.0 workforce chapter."""

import os
from wf5_draw import Canvas

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wf5_figures")
os.makedirs(OUT, exist_ok=True)

# Palette
BLUE = (37, 99, 175)
TEAL = (23, 145, 145)
GREEN = (46, 139, 87)
ORANGE = (222, 130, 40)
PURPLE = (120, 80, 170)
GREY = (110, 110, 110)
LGREY = (225, 225, 225)
DARK = (40, 40, 40)
WHITE = (255, 255, 255)


def fig1():
    """Conceptual framework: Industry 4.0 -> 5.0 with AI enabling DEI + SDGs."""
    c = Canvas(1040, 730)
    c.text_center(520, 24, "Figure 1  AI-Enabled Inclusive Workforce Development Framework", DARK, 2)
    c.line(60, 60, 980, 60, BLUE, 2)

    # Three input pillars
    pillars = [
        ("Organizational", "Leadership, DEI policy,", "culture, governance", BLUE, 70),
        ("Technological", "AI, cobots, IoT,", "digital twins, analytics", TEAL, 400),
        ("Human", "Skills, well-being,", "trust, participation", GREEN, 730),
    ]
    for title, l1, l2, col, x in pillars:
        c.rect(x, 100, x + 300, 230, col)
        c.rect_outline(x, 100, x + 300, 230, DARK, 2)
        c.text_center(x + 150, 122, title, WHITE, 2)
        c.text_center(x + 150, 160, l1, WHITE, 2)
        c.text_center(x + 150, 190, l2, WHITE, 2)
        c.line(x + 150, 230, 520, 300, GREY, 2)

    # Central AI engine
    c.rect(250, 300, 790, 400, ORANGE)
    c.rect_outline(250, 300, 790, 400, DARK, 2)
    c.text_center(520, 322, "AI-Enabled Intelligent Manufacturing", WHITE, 2)
    c.text_center(520, 358, "Recruit  Upskill  Cobots  Well-being  Fairness", WHITE, 2)

    # Arrow down
    c.line(520, 400, 520, 450, DARK, 3)
    c.line(520, 450, 510, 435, DARK, 3)
    c.line(520, 450, 530, 435, DARK, 3)

    # DEI outcomes
    dei = [("Diversity", 110), ("Equity", 435), ("Inclusion", 760)]
    for label, x in dei:
        c.rect(x, 460, x + 260, 530, PURPLE)
        c.rect_outline(x, 460, x + 260, 530, DARK, 2)
        c.text_center(x + 130, 486, label, WHITE, 2)

    # Arrow down to SDGs
    c.line(520, 530, 520, 575, DARK, 3)
    c.line(520, 575, 510, 560, DARK, 3)
    c.line(520, 575, 530, 560, DARK, 3)

    # SDG bar
    c.rect(110, 585, 910, 660, GREEN)
    c.rect_outline(110, 585, 910, 660, DARK, 2)
    c.text_center(510, 600, "Sustainable Development Goals", WHITE, 2)
    c.text_center(510, 632, "SDG 5   SDG 8   SDG 9   SDG 10", WHITE, 2)

    c.text(60, 695, "Source: authors, adapted from cited literature", GREY, 2)
    c.save(os.path.join(OUT, "Figure_1_Framework.png"))


def fig2():
    """Grouped bar chart: DEI/workforce metrics before vs after AI adoption."""
    c = Canvas(1000, 640)
    c.text_center(500, 20, "Figure 2  Workforce DEI Indicators Before and After AI Adoption", DARK, 2)

    # Axes
    ox, oy = 120, 520
    top = 90
    c.line(ox, oy, 920, oy, DARK, 2)         # x axis
    c.line(ox, oy, ox, top, DARK, 2)          # y axis
    # y gridlines 0..100
    for v in range(0, 101, 20):
        y = oy - (oy - top) * v / 100
        c.line(ox, y, 920, y, LGREY, 1)
        c.text(ox - 55, y - 7, f"{v}", GREY, 2)
    c.text(30, 250, "%", GREY, 2)

    cats = [
        ("Gender\nbalance", 32, 47),
        ("Older-worker\nretention", 55, 78),
        ("Disability\ninclusion", 18, 41),
        ("Reskilling\ncompletion", 44, 82),
        ("Pay-equity\nindex", 61, 85),
    ]
    n = len(cats)
    span = (920 - ox) / n
    bw = 46
    for i, (lab, before, after) in enumerate(cats):
        cx = ox + span * i + span / 2
        # before
        h1 = (oy - top) * before / 100
        c.rect(cx - bw - 4, oy - h1, cx - 4, oy, GREY)
        c.rect_outline(cx - bw - 4, oy - h1, cx - 4, oy, DARK, 1)
        c.text_center(cx - bw / 2 - 4, oy - h1 - 22, f"{before}", DARK, 2)
        # after
        h2 = (oy - top) * after / 100
        c.rect(cx + 4, oy - h2, cx + bw + 4, oy, BLUE)
        c.rect_outline(cx + 4, oy - h2, cx + bw + 4, oy, DARK, 1)
        c.text_center(cx + bw / 2 + 4, oy - h2 - 22, f"{after}", DARK, 2)
        # label (2 lines)
        parts = lab.split("\n")
        c.text_center(cx, oy + 12, parts[0], DARK, 2)
        if len(parts) > 1:
            c.text_center(cx, oy + 34, parts[1], DARK, 2)

    # legend
    c.rect(640, top - 5, 660, top + 12, GREY)
    c.text(668, top - 5, "Before AI", DARK, 2)
    c.rect(780, top - 5, 800, top + 12, BLUE)
    c.text(808, top - 5, "After AI", DARK, 2)
    c.text(120, 610, "Illustrative composite values from cited case evidence", GREY, 2)
    c.save(os.path.join(OUT, "Figure_2_Indicators.png"))


def fig3():
    """Human-robot collaboration continuum / inclusive work design layers."""
    c = Canvas(1000, 600)
    c.text_center(500, 20, "Figure 3  Human-Robot Collaboration Continuum in Inclusive Work Design", DARK, 2)

    stages = [
        ("Coexistence", "Separate zones", GREY),
        ("Cooperation", "Shared space,\nsequential tasks", TEAL),
        ("Collaboration", "Shared task,\nsimultaneous", BLUE),
        ("Augmentation", "AI-guided,\nadaptive support", PURPLE),
    ]
    x = 70
    w = 200
    gap = 20
    y0 = 120
    for i, (t, d, col) in enumerate(stages):
        c.rect(x, y0, x + w, y0 + 150, col)
        c.rect_outline(x, y0, x + w, y0 + 150, DARK, 2)
        c.text_center(x + w / 2, y0 + 20, t, WHITE, 2)
        for j, ln in enumerate(d.split("\n")):
            c.text_center(x + w / 2, y0 + 70 + j * 24, ln, WHITE, 2)
        if i < 3:
            ax = x + w
            c.line(ax, y0 + 75, ax + gap, y0 + 75, DARK, 3)
            c.line(ax + gap, y0 + 75, ax + gap - 12, y0 + 67, DARK, 3)
            c.line(ax + gap, y0 + 75, ax + gap - 12, y0 + 83, DARK, 3)
        x += w + gap

    c.text_center(500, 300, "Increasing human-centricity and adaptive AI support", DARK, 2)
    c.line(70, 322, 930, 322, ORANGE, 2)
    c.line(930, 322, 916, 314, ORANGE, 3)
    c.line(930, 322, 916, 330, ORANGE, 3)

    # inclusive design benefits row
    c.text_center(500, 360, "Inclusive Design Benefits", DARK, 2)
    benefits = [
        ("Ergonomics", GREEN, 60),
        ("Older workers", BLUE, 290),
        ("Disability access", PURPLE, 520),
        ("Cognitive aid", ORANGE, 750),
    ]
    for lab, col, bx in benefits:
        c.rect(bx, 400, bx + 220, 470, col)
        c.rect_outline(bx, 400, bx + 220, 470, DARK, 2)
        c.text_center(bx + 110, 428, lab, WHITE, 2)
    c.text(70, 520, "Source: authors, based on cited human-robot interaction studies", GREY, 2)
    c.save(os.path.join(OUT, "Figure_3_HRC.png"))


def fig4():
    """Line chart: reskilling completion & inclusion index trajectory 2021-2027."""
    c = Canvas(1000, 620)
    c.text_center(500, 20, "Figure 4  Projected Reskilling and Inclusion Trajectories", DARK, 2)

    ox, oy = 110, 500
    top = 80
    right = 920
    c.line(ox, oy, right, oy, DARK, 2)
    c.line(ox, oy, ox, top, DARK, 2)
    for v in range(0, 101, 20):
        y = oy - (oy - top) * v / 100
        c.line(ox, y, right, y, LGREY, 1)
        c.text(ox - 50, y - 7, f"{v}", GREY, 2)
    c.text(24, 250, "Index", GREY, 2)

    years = ["2021", "2022", "2023", "2024", "2025", "2026", "2027"]
    n = len(years)
    for i, yr in enumerate(years):
        x = ox + (right - ox) * i / (n - 1)
        c.text_center(x, oy + 14, yr, DARK, 2)

    def plot(series, col):
        pts = []
        for i, v in enumerate(series):
            x = ox + (right - ox) * i / (n - 1)
            y = oy - (oy - top) * v / 100
            pts.append((x, y))
        for i in range(len(pts) - 1):
            c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], col, 3)
        for (x, y) in pts:
            c.circle(int(x), int(y), 5, col)
        return pts

    reskill = [30, 41, 52, 63, 72, 80, 88]
    inclusion = [38, 44, 50, 58, 66, 73, 81]
    greenjobs = [12, 20, 29, 40, 52, 63, 74]
    plot(reskill, BLUE)
    plot(inclusion, GREEN)
    plot(greenjobs, ORANGE)

    # legend
    lx, ly = 620, 90
    c.line(lx, ly, lx + 30, ly, BLUE, 3); c.text(lx + 40, ly - 7, "Reskilling completion", DARK, 2)
    c.line(lx, ly + 30, lx + 30, ly + 30, GREEN, 3); c.text(lx + 40, ly + 23, "Inclusion index", DARK, 2)
    c.line(lx, ly + 60, lx + 30, ly + 60, ORANGE, 3); c.text(lx + 40, ly + 53, "Green-job share", DARK, 2)

    c.text(110, 560, "Illustrative projections synthesised from cited workforce data", GREY, 2)
    c.save(os.path.join(OUT, "Figure_4_Trajectories.png"))


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4()
    for f in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, f)
        print(f, os.path.getsize(p), "bytes")
