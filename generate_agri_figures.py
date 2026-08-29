#!/usr/bin/env python3
"""
Generate 4 scientific figures (PNG) for the chapter
"Agricultural Data Management: Big Data Analytics, Cloud Computing, and Edge Intelligence".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py
(no matplotlib/numpy required, works offline).
"""

import os
import math

# Reuse the PNGCanvas class and colors from the existing repo script.
from generate_figures import (
    PNGCanvas, math as _m,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE, RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY, BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/agri_figures'


def box(c, x, y, w, h, outline, fill, label, scale=1, tcol=BLACK):
    c.rect(x, y, x + w, y + h, outline, fill)
    # multi-line label support via '|'
    lines = label.split('|')
    total = len(lines) * 10 * scale
    ly = y + h // 2 - total // 2
    for ln in lines:
        c.text_c(x + w // 2, ly, ln, tcol, scale)
        ly += 10 * scale


def fig1_data_ecosystem():
    """Figure 1: Agricultural data ecosystem - sources, 4Vs, and layered pipeline."""
    c = PNGCanvas(760, 520)
    c.text_c(380, 12, "Agricultural Data Ecosystem", BLACK, 2)

    # Left column: data sources
    c.text_c(130, 45, "Data Sources", DARK_BLUE, 1)
    sources = [
        ("IoT Sensors", DARK_GREEN, LIGHT_GREEN),
        ("Satellites", MED_BLUE, LIGHT_BLUE),
        ("Drones (UAV)", ORANGE, LIGHT_ORANGE),
        ("Weather Stns", PURPLE, LIGHT_PURPLE),
        ("Machinery", RED, LIGHT_RED),
        ("Markets", GOLD, LIGHT_GOLD),
    ]
    sy = 65
    src_centers = []
    for label, oc, fc in sources:
        box(c, 30, sy, 200, 42, oc, fc, label, 1)
        src_centers.append((230, sy + 21))
        sy += 62

    # Middle column: pipeline layers
    c.text_c(430, 45, "Processing Pipeline", DARK_BLUE, 1)
    layers = [
        ("Ingestion", MED_BLUE, LIGHT_BLUE),
        ("Storage (Data Lake)", DARK_BLUE, PALE_BLUE),
        ("Integration", DARK_GREEN, LIGHT_GREEN),
        ("Analytics", ORANGE, LIGHT_ORANGE),
        ("Decision Support", PURPLE, LIGHT_PURPLE),
    ]
    ly = 75
    lay_centers = []
    for label, oc, fc in layers:
        box(c, 330, ly, 200, 46, oc, fc, label, 1)
        lay_centers.append((330, ly + 23, 530, ly + 23))
        ly += 72

    # Arrows from sources to ingestion box
    ing_x, ing_y = 330, 98
    for (sx, syc) in src_centers:
        c.arrow(sx + 4, syc, ing_x - 4, ing_y, GRAY, 1, 6)

    # Vertical arrows down the pipeline
    for i in range(len(lay_centers) - 1):
        _, _, bx, by = lay_centers[i]
        x_center = 430
        c.arrow(x_center, lay_centers[i][1] + 23, x_center, lay_centers[i + 1][1] - 23, DARK_BLUE, 2, 7)

    # Right column: the 4 V's
    c.text_c(660, 45, "Characteristics (4 Vs)", DARK_BLUE, 1)
    vs = [
        ("Volume", DARK_BLUE, PALE_BLUE),
        ("Velocity", MED_GREEN, LIGHT_GREEN),
        ("Variety", ORANGE, LIGHT_ORANGE),
        ("Veracity", RED, LIGHT_RED),
    ]
    vy = 80
    for label, oc, fc in vs:
        c.circle(660, vy + 22, 26, oc, fc)
        c.text_c(660, vy + 17, label, BLACK, 1)
        vy += 78

    # Arrow from decision support outward
    c.arrow(530, lay_centers[-1][1], 600, lay_centers[-1][1], DARK_GREEN, 2, 8)
    c.text_c(660, lay_centers[-1][1] - 4, "Action", DARK_GREEN, 1)

    c.text_c(380, 500, "Raw observations are refined into decision-ready knowledge", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Data_Ecosystem.png'))


def fig2_farm_to_fork():
    """Figure 2: Farm-to-fork data flow and analytics across the supply chain."""
    c = PNGCanvas(780, 460)
    c.text_c(390, 12, "Farm-to-Fork Agricultural Data Flow", BLACK, 2)

    stages = [
        ("Production", DARK_GREEN, LIGHT_GREEN),
        ("Harvest", MED_GREEN, LIGHT_GREEN),
        ("Processing", ORANGE, LIGHT_ORANGE),
        ("Distribution", MED_BLUE, LIGHT_BLUE),
        ("Retail", PURPLE, LIGHT_PURPLE),
        ("Consumer", RED, LIGHT_RED),
    ]
    bw, bh = 110, 55
    y = 90
    gap = (780 - 40 - bw) / (len(stages) - 1)
    centers = []
    for i, (label, oc, fc) in enumerate(stages):
        x = int(20 + i * gap)
        box(c, x, y, bw, bh, oc, fc, label, 1)
        centers.append((x + bw // 2, y))
        if i > 0:
            px = centers[i - 1][0]
            c.arrow(px + bw // 2 - 8, y + bh // 2, x - 4, y + bh // 2, GRAY, 2, 8)

    # Data layer below
    c.fill_rect(20, 200, 760, 250, PALE_BLUE)
    c.rect(20, 200, 760, 250, DARK_BLUE)
    c.text_c(390, 218, "Data Layer: sensors, traceability records, quality and condition monitoring", DARK_BLUE, 1)

    # dashed upward links from stages to data layer
    for cx, cy in centers:
        c.line(cx, y + bh, cx, 200, LIGHT_GRAY, 1)

    # Analytics box below data layer
    analytics = [
        ("Demand|Forecasting", MED_BLUE, LIGHT_BLUE),
        ("Logistics|Optimization", DARK_GREEN, LIGHT_GREEN),
        ("Traceability|and Quality", ORANGE, LIGHT_ORANGE),
        ("Loss and Waste|Reduction", RED, LIGHT_RED),
    ]
    ax = 40
    aw = 160
    for label, oc, fc in analytics:
        box(c, ax, 300, aw, 60, oc, fc, label, 1)
        c.arrow(ax + aw // 2, 250, ax + aw // 2, 300, DARK_BLUE, 2, 7)
        ax += aw + 20

    c.text_c(390, 400, "Big Data Analytics for Food Security & Supply Chain Management", DARK_BLUE, 1)
    c.text_c(390, 430, "Data captured at every stage feeds analytics that optimize the food system", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Farm_to_Fork.png'))


def fig3_cloud_edge():
    """Figure 3: Layered cloud-edge architecture for digital agriculture."""
    c = PNGCanvas(720, 560)
    c.text_c(360, 12, "Cloud-Edge Architecture for Digital Agriculture", BLACK, 2)

    # Cloud tier (top)
    c.fill_rect(60, 55, 660, 155, PALE_BLUE)
    c.rect(60, 55, 660, 155, DARK_BLUE)
    c.text_c(360, 62, "CLOUD TIER", DARK_BLUE, 2)
    for i, (label) in enumerate(["Big Data Storage", "Model Training", "Cross-Farm Analytics", "Decision Support"]):
        box(c, 80 + i * 145, 95, 130, 48, MED_BLUE, LIGHT_BLUE, label, 1)

    # Edge tier (middle)
    c.fill_rect(60, 235, 660, 335, LIGHT_GOLD)
    c.rect(60, 235, 660, 335, GOLD)
    c.text_c(360, 242, "EDGE TIER", GOLD, 2)
    for i, label in enumerate(["Gateways", "Local Inference", "Real-Time Control", "Data Filtering"]):
        box(c, 80 + i * 145, 275, 130, 48, ORANGE, LIGHT_ORANGE, label, 1)

    # Field / device tier (bottom)
    c.fill_rect(60, 415, 660, 515, LIGHT_GREEN)
    c.rect(60, 415, 660, 515, DARK_GREEN)
    c.text_c(360, 422, "FIELD / DEVICE TIER", DARK_GREEN, 2)
    for i, label in enumerate(["Soil Sensors", "Cameras", "Irrigation", "Machinery"]):
        box(c, 80 + i * 145, 455, 130, 48, MED_GREEN, LIGHT_GREEN, label, 1)

    # Bidirectional arrows between tiers
    c.arrow(300, 235, 300, 158, DARK_BLUE, 2, 8)   # edge up to cloud
    c.arrow(300, 155, 300, 232, MED_BLUE, 2, 8)    # cloud down to edge
    c.text_c(210, 190, "sync / models", GRAY, 1)
    c.text_c(470, 190, "results / updates", GRAY, 1)

    c.arrow(300, 415, 300, 338, GOLD, 2, 8)        # field up to edge
    c.arrow(420, 338, 420, 412, MED_GREEN, 2, 8)   # edge down to field
    c.text_c(210, 372, "raw data", GRAY, 1)
    c.text_c(490, 372, "actuation", GRAY, 1)

    c.text_c(360, 535, "Latency decreases and locality increases toward the field", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Cloud_Edge_Architecture.png'))


def fig4_roadmap():
    """Figure 4: Roadmap toward globally connected, data-driven agriculture."""
    c = PNGCanvas(780, 480)
    c.text_c(390, 12, "Roadmap Toward Globally Connected Agriculture", BLACK, 2)

    # horizontal timeline
    c.line(60, 240, 720, 240, DARK_BLUE, 3)
    c.arrow(710, 240, 730, 240, DARK_BLUE, 3, 10)

    stages = [
        ("Connected|Sensing (IoT)", DARK_GREEN, LIGHT_GREEN, 130, -1),
        ("Cloud Data|Platforms", MED_BLUE, LIGHT_BLUE, 260, 1),
        ("Edge AI &|Analytics", ORANGE, LIGHT_ORANGE, 390, -1),
        ("Digital Twins|& Autonomy", PURPLE, LIGHT_PURPLE, 520, 1),
        ("Blockchain &|Global Networks", GOLD, LIGHT_GOLD, 650, -1),
    ]
    for label, oc, fc, x, side in stages:
        # node on timeline
        c.circle(x, 240, 10, oc, fc)
        if side < 0:
            by = 130
            box(c, x - 70, by, 140, 62, oc, fc, label, 1)
            c.line(x, 192, x, 230, GRAY, 1)
        else:
            by = 290
            box(c, x - 70, by, 140, 62, oc, fc, label, 1)
            c.line(x, 250, x, 290, GRAY, 1)

    # convergence banner
    c.fill_rect(60, 400, 720, 445, PALE_BLUE)
    c.rect(60, 400, 720, 445, DARK_BLUE)
    c.text_c(390, 415, "Integration of IoT + Cloud + Edge AI + Advanced Analytics", DARK_BLUE, 1)

    c.text_c(390, 55, "Increasing intelligence, autonomy, and connectivity", GRAY, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Roadmap.png'))


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig1_data_ecosystem()
    fig2_farm_to_fork()
    fig3_cloud_edge()
    fig4_roadmap()
    print("Generated figures in", OUTPUT_DIR)
    for f in sorted(os.listdir(OUTPUT_DIR)):
        p = os.path.join(OUTPUT_DIR, f)
        print(f"  {f}: {os.path.getsize(p)/1024:.1f} KB")
