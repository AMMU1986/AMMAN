#!/usr/bin/env python3
"""Generate the 4 figures for the Bio-Integrated Urban Tourism chapter."""

import os
from bittourism_pnglib import Canvas

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "biotourism_figures")
os.makedirs(OUT, exist_ok=True)

# Palette
GREEN = (46, 125, 50)
LGREEN = (129, 199, 132)
BLUE = (25, 118, 210)
LBLUE = (144, 202, 249)
TEAL = (0, 137, 123)
ORANGE = (239, 108, 0)
GREY = (117, 117, 117)
DARK = (33, 33, 33)
BG = (255, 255, 255)
AXIS = (60, 60, 60)


def fig1_ecosystem_services():
    """Bar chart: ecological co-benefits of urban green tourism infrastructure."""
    c = Canvas(900, 600, BG)
    c.text_center(450, 20, "ECOLOGICAL CO-BENEFITS OF GREEN TOURISM INFRASTRUCTURE", DARK, 2)
    # plot area
    x0, y0, x1, y1 = 110, 90, 850, 500
    c.line(x0, y0, x0, y1, AXIS, 2)
    c.line(x0, y1, x1, y1, AXIS, 2)
    labels = ["COOLING", "AIR QUAL", "STORMWTR", "CARBON", "BIODIV", "WELLBEING"]
    vals = [78, 64, 71, 55, 83, 89]
    colors = [BLUE, TEAL, LBLUE, GREEN, LGREEN, ORANGE]
    n = len(vals)
    slot = (x1 - x0) / n
    bw = slot * 0.55
    maxv = 100
    # gridlines
    for g in range(0, 101, 20):
        gy = y1 - (y1 - y0) * g / maxv
        c.line(x0, gy, x1, gy, (220, 220, 220), 1)
        c.text(x0 - 45, gy - 7, str(g), GREY, 1)
    c.line(x0, y0, x0, y1, AXIS, 2)
    c.line(x0, y1, x1, y1, AXIS, 2)
    for i, v in enumerate(vals):
        bx = x0 + slot * i + (slot - bw) / 2
        bh = (y1 - y0) * v / maxv
        c.rect(bx, y1 - bh, bx + bw, y1 - 1, colors[i])
        c.text_center(bx + bw / 2, y1 - bh - 22, str(v), DARK, 2)
        c.text_center(bx + bw / 2, y1 + 12, labels[i], DARK, 1)
    c.text(20, 250, "INDEX", GREY, 1)
    c.text_center(450, 545, "PERFORMANCE INDEX (0-100, RELATIVE BENEFIT)", GREY, 1)
    c.save(os.path.join(OUT, "Figure_1_Ecosystem_Cobenefits.png"))


def fig2_framework():
    """Conceptual framework: transition to nature-positive tourism."""
    c = Canvas(900, 620, BG)
    c.text_center(450, 20, "FRAMEWORK FOR BIO-INTEGRATED URBAN TOURISM", DARK, 2)

    def box(cx, cy, w, h, color, title, sub=None):
        c.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, color)
        c.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, DARK, fill=False)
        c.text_center(cx, cy - (12 if sub else 6), title, (255, 255, 255), 2)
        if sub:
            c.text_center(cx, cy + 10, sub, (255, 255, 255), 1)

    # Three input pillars
    box(180, 130, 240, 70, GREEN, "LIVING", "SYSTEMS")
    box(450, 130, 240, 70, BLUE, "COMPUTATIONAL", "INNOVATION")
    box(720, 130, 240, 70, ORANGE, "COMMUNITY &", "GOVERNANCE")
    # arrows down to core
    for cx in (180, 450, 720):
        c.line(cx, 165, 450, 265, GREY, 2)
    # core
    box(450, 300, 360, 80, TEAL, "BIO-INTEGRATED", "GREEN INFRASTRUCTURE")
    c.line(450, 340, 450, 400, GREY, 2)
    # outcomes row
    box(200, 450, 260, 70, LGREEN, "REGENERATIVE", "DESTINATIONS")
    box(450, 450, 220, 70, LGREEN, "RESILIENCE", None)
    box(700, 450, 260, 70, LGREEN, "VISITOR", "WELLBEING")
    for cx in (200, 450, 700):
        c.line(450, 400, cx, 415, GREY, 2)
    # feedback loop
    box(450, 560, 520, 60, GREY, "MONITORING - CERTIFICATION - FEEDBACK", None)
    c.line(700, 485, 700, 530, DARK, 2)
    c.line(200, 530, 200, 485, DARK, 2)
    c.save(os.path.join(OUT, "Figure_2_Conceptual_Framework.png"))


def fig3_trends():
    """Line chart: microclimate & performance trends across greening intensity."""
    c = Canvas(900, 600, BG)
    c.text_center(450, 20, "PERFORMANCE VS GREENING INTENSITY", DARK, 2)
    x0, y0, x1, y1 = 110, 90, 850, 500
    c.line(x0, y0, x0, y1, AXIS, 2)
    c.line(x0, y1, x1, y1, AXIS, 2)
    for g in range(0, 101, 20):
        gy = y1 - (y1 - y0) * g / 100
        c.line(x0, gy, x1, gy, (225, 225, 225), 1)
        c.text(x0 - 45, gy - 7, str(g), GREY, 1)
    xs = [0, 20, 40, 60, 80, 100]
    for xv in xs:
        gx = x0 + (x1 - x0) * xv / 100
        c.text_center(gx, y1 + 12, str(xv), GREY, 1)

    def series(vals, color):
        pts = []
        for i, xv in enumerate(xs):
            gx = x0 + (x1 - x0) * xv / 100
            gy = y1 - (y1 - y0) * vals[i] / 100
            pts.append((gx, gy))
        c.polyline(pts, color, 3)
        for p in pts:
            c.circle(int(p[0]), int(p[1]), 5, color)

    cooling = [20, 34, 48, 62, 74, 82]
    biodiv = [15, 28, 45, 60, 76, 88]
    wellbeing = [30, 42, 55, 66, 77, 85]
    series(cooling, BLUE)
    series(biodiv, GREEN)
    series(wellbeing, ORANGE)
    # legend
    lx, ly = 620, 110
    c.rect(lx, ly, lx + 18, ly + 12, BLUE); c.text(lx + 26, ly, "COOLING", DARK, 1)
    c.rect(lx, ly + 24, lx + 18, ly + 36, GREEN); c.text(lx + 26, ly + 24, "BIODIVERSITY", DARK, 1)
    c.rect(lx, ly + 48, lx + 18, ly + 60, ORANGE); c.text(lx + 26, ly + 48, "WELLBEING", DARK, 1)
    c.text_center(450, 545, "GREEN COVER RATIO (%)", GREY, 1)
    c.text(15, 250, "BENEFIT INDEX", GREY, 1)
    c.save(os.path.join(OUT, "Figure_3_Greening_Trends.png"))


def fig4_smart_stack():
    """Layered diagram: smart green infrastructure technology stack."""
    c = Canvas(900, 600, BG)
    c.text_center(450, 20, "SMART GREEN INFRASTRUCTURE TECHNOLOGY STACK", DARK, 2)
    layers = [
        ("SENSING LAYER  -  IOT AIR, WATER, SOIL, MICROCLIMATE SENSORS", TEAL),
        ("DATA LAYER  -  REAL-TIME ECOLOGICAL & TOURISM DATA PLATFORMS", BLUE),
        ("INTELLIGENCE LAYER  -  AI OPTIMIZATION & PREDICTIVE ANALYTICS", GREEN),
        ("MODELING LAYER  -  DIGITAL TWINS & GIS SPATIAL PLANNING", ORANGE),
        ("DECISION LAYER  -  GOVERNANCE, POLICY & VISITOR MANAGEMENT", GREY),
    ]
    top = 80
    h = 78
    gap = 14
    for i, (txt, col) in enumerate(layers):
        y = top + i * (h + gap)
        c.rect(120, y, 780, y + h, col)
        c.rect(120, y, 780, y + h, DARK, fill=False)
        c.text_center(450, y + h / 2 - 7, txt, (255, 255, 255), 1)
        if i < len(layers) - 1:
            midy = y + h + gap / 2
            c.line(450, y + h, 450, y + h + gap, DARK, 2)
    c.save(os.path.join(OUT, "Figure_4_Smart_Green_Stack.png"))


if __name__ == "__main__":
    fig1_ecosystem_services()
    fig2_framework()
    fig3_trends()
    fig4_smart_stack()
    print("Figures written to", OUT)
    for f in sorted(os.listdir(OUT)):
        print(" -", f, os.path.getsize(os.path.join(OUT, f)), "bytes")
