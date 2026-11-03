#!/usr/bin/env python3
"""
Generate 5 figure images (PNG) for the chapter
"Emerging Trends and Future Perspectives"
(AI and Digital Twin-Driven Smart Grids).

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py
so it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Layered convergence of the smart grid
  Figure 2 - Digital twin architecture
  Figure 3 - Digital twin-driven monitoring pipeline (IoT/edge/cloud)
  Figure 4 - AI-driven energy management loop
  Figure 5 - Digital twin applications across smart grid domains
"""

import os
import math

from generate_figures import (
    PNGCanvas,
    DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
    DARK_GREEN, MED_GREEN, LIGHT_GREEN,
    ORANGE, LIGHT_ORANGE,
    RED, LIGHT_RED,
    PURPLE, LIGHT_PURPLE,
    GOLD, LIGHT_GOLD,
    GRAY, LIGHT_GRAY,
    BLACK, WHITE,
)

OUTPUT_DIR = '/projects/sandbox/AMMAN/emerging_figures'


def gen_fig1():
    """Figure 1: Layered convergence of the smart grid."""
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "Layered Convergence in the Smart Grid", BLACK, 2)

    layers = [
        ("Intelligence Layer", "AI / ML + Digital Twins: forecast, diagnose, optimize, control",
         PURPLE, LIGHT_PURPLE),
        ("Data & Analytics Layer", "Big data platforms, edge and cloud computing",
         DARK_GREEN, LIGHT_GREEN),
        ("Sensing & Communication Layer", "IoT devices, smart meters, PMUs, real-time networks",
         ORANGE, LIGHT_ORANGE),
        ("Physical Power Layer", "Generation, renewables, DER, transmission, distribution, loads",
         MED_BLUE, LIGHT_BLUE),
    ]
    lx1, lx2 = 90, 670
    top = 60
    lh = 72
    gap = 14
    for i, (title, sub, col, fill) in enumerate(layers):
        y1 = top + i * (lh + gap)
        y2 = y1 + lh
        c.rect(lx1, y1, lx2, y2, col, fill)
        c.text_c((lx1 + lx2) // 2, y1 + 22, title, BLACK, 1)
        c.text_c((lx1 + lx2) // 2, y1 + 44, sub, GRAY, 1)
        if i < len(layers) - 1:
            midx = (lx1 + lx2) // 2
            # data flows up, control flows down
            c.arrow(midx - 60, y2 + gap, midx - 60, y2 + 2, DARK_GREEN, 2, 7)
            c.arrow(midx + 60, y2 + 2, midx + 60, y2 + gap, RED, 2, 7)

    # side labels for the two flows
    c.text(690, top + 120, "data up", DARK_GREEN, 1)
    c.text(690, top + 140, "control", RED, 1)
    c.text(690, top + 154, "down", RED, 1)

    c.text(40, 444, "Figure 1: Physical, sensing, data, and intelligence layers converge in the smart grid", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Layered_Convergence.png'))
    print("  Figure_1_Layered_Convergence.png done")


def gen_fig2():
    """Figure 2: Digital twin architecture."""
    c = PNGCanvas(760, 450)
    c.text_c(380, 10, "Digital Twin Architecture", BLACK, 2)

    # Physical entity (left)
    c.rect(40, 120, 250, 300, MED_BLUE, LIGHT_BLUE)
    c.text_c(145, 140, "PHYSICAL ENTITY", BLACK, 1)
    c.text_c(145, 170, "Grid asset / system", BLACK, 1)
    c.text_c(145, 190, "(transformer, line,", GRAY, 1)
    c.text_c(145, 204, "plant, microgrid)", GRAY, 1)
    # little sensor dots
    for i in range(4):
        c.circle(70 + i * 45, 250, 6, RED, LIGHT_RED)
    c.text_c(145, 272, "IoT sensors", RED, 1)

    # Virtual model (right)
    c.rect(510, 120, 720, 300, MED_GREEN, LIGHT_GREEN)
    c.text_c(615, 140, "VIRTUAL MODEL", BLACK, 1)
    c.text_c(615, 170, "Continuously updated", BLACK, 1)
    c.text_c(615, 190, "physics + data model", GRAY, 1)
    c.text_c(615, 210, "mirrors real state", GRAY, 1)
    # mesh look
    for i in range(3):
        c.rect(545 + i * 50, 240, 575 + i * 50, 270, DARK_GREEN, (210, 235, 205))

    # Data synchronization (center, bidirectional)
    c.rect(300, 150, 460, 270, GOLD, LIGHT_GOLD)
    c.text_c(380, 168, "DATA SYNC", BLACK, 1)
    c.text_c(380, 188, "real-time", GRAY, 1)
    c.text_c(380, 202, "connection", GRAY, 1)
    c.arrow(250, 190, 300, 190, DARK_GREEN, 3, 10)
    c.text(252, 172, "measurements", DARK_GREEN, 1)
    c.arrow(460, 230, 510, 230, GRAY, 3, 10)
    c.arrow(510, 250, 460, 250, PURPLE, 2, 8)
    c.text(300, 300, "state update <-> insight", GRAY, 1)

    # Services layer (bottom)
    c.rect(130, 330, 630, 400, PURPLE, LIGHT_PURPLE)
    c.text_c(380, 344, "ANALYTIC SERVICES", BLACK, 1)
    c.text_c(380, 366, "monitoring - simulation - prediction - optimization - visualization", GRAY, 1)
    c.arrow(380, 300, 380, 330, PURPLE, 2, 8)
    # control back to physical
    c.line(130, 365, 60, 365, RED, 1)
    c.line(60, 365, 60, 300, RED, 1)
    c.arrow(60, 300, 60, 300, RED, 1, 6)
    c.text(70, 340, "control action", RED, 1)

    c.text(40, 434, "Figure 2: Physical entity, virtual model, data synchronization, and analytic services", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Digital_Twin_Architecture.png'))
    print("  Figure_2_Digital_Twin_Architecture.png done")


def gen_fig3():
    """Figure 3: Digital twin-driven monitoring pipeline."""
    c = PNGCanvas(760, 450)
    c.text_c(380, 10, "Digital Twin-Driven Monitoring Pipeline", BLACK, 2)

    stages = [
        ("IoT SENSING", "assets instrumented", 110, MED_BLUE, LIGHT_BLUE),
        ("EDGE COMPUTING", "low-latency processing", 310, ORANGE, LIGHT_ORANGE),
        ("CLOUD PLATFORM", "training, aggregation", 540, DARK_GREEN, LIGHT_GREEN),
    ]
    bw, bh = 180, 70
    top = 70
    centers = []
    for title, sub, cx, co, fi in stages:
        c.rect(cx - bw // 2, top, cx + bw // 2, top + bh, co, fi)
        c.text_c(cx, top + 24, title, BLACK, 1)
        c.text_c(cx, top + 46, sub, GRAY, 1)
        centers.append((cx, top + bh // 2))
    c.arrow(centers[0][0] + bw // 2 + 2, centers[0][1], centers[1][0] - bw // 2 - 2, centers[1][1], GRAY, 3, 9)
    c.arrow(centers[1][0] + bw // 2 + 2, centers[1][1], centers[2][0] - bw // 2 - 2, centers[2][1], GRAY, 3, 9)

    # Digital twin virtual model (center)
    c.rect(230, 200, 530, 290, PURPLE, LIGHT_PURPLE)
    c.text_c(380, 220, "DIGITAL TWIN VIRTUAL MODEL", BLACK, 1)
    c.text_c(380, 244, "continuously synchronized state", GRAY, 1)
    c.text_c(380, 262, "+ simulation engine", GRAY, 1)
    c.arrow(310, 140, 330, 200, MED_BLUE, 2, 8)
    c.arrow(540, 140, 470, 200, DARK_GREEN, 2, 8)

    # Outputs (bottom)
    outs = [
        ("Real-time monitoring", 115, 78, MED_GREEN, LIGHT_GREEN),
        ("Scenario simulation", 300, 78, GOLD, LIGHT_GOLD),
        ("Asset management", 485, 75, RED, LIGHT_RED),
        ("Reliability", 650, 55, MED_BLUE, LIGHT_BLUE),
    ]
    oy = 330
    for lab, cx, hw, co, fi in outs:
        c.rect(cx - hw, oy, cx + hw, oy + 50, co, fi)
        c.text_c(cx, oy + 25, lab, BLACK, 1)
        c.arrow(380, 290, cx, oy - 2, GRAY, 1, 7)

    c.text(40, 434, "Figure 3: Sensing, edge-cloud computation, and simulation support reliability and asset management", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Monitoring_Pipeline.png'))
    print("  Figure_3_Monitoring_Pipeline.png done")


def gen_fig4():
    """Figure 4: AI-driven energy management loop."""
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "AI-Driven Energy Management Loop", BLACK, 2)

    stages = [
        ("FORECAST", "load + renewable generation", 380, 70, MED_BLUE, LIGHT_BLUE),
        ("OPTIMIZE (RL)", "storage, DER, dispatch", 590, 225, ORANGE, LIGHT_ORANGE),
        ("DEMAND-SIDE CONTROL", "shift flexible loads", 380, 380, RED, LIGHT_RED),
        ("MONITOR", "grid stability, state", 170, 225, MED_GREEN, LIGHT_GREEN),
    ]
    bw, bh = 190, 70
    centers = []
    for title, sub, cx, cy, co, fi in stages:
        c.rect(cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2, co, fi)
        c.text_c(cx, cy - 8, title, BLACK, 1)
        c.text_c(cx, cy + 12, sub, GRAY, 1)
        centers.append((cx, cy))

    def loop_arrow(a, b):
        ax, ay = centers[a]; bx, by = centers[b]
        dx, dy = bx - ax, by - ay
        d = math.hypot(dx, dy)
        ox, oy = dx / d, dy / d
        c.arrow(int(ax + ox * 105), int(ay + oy * 50),
                int(bx - ox * 105), int(by - oy * 50), GRAY, 3, 10)

    loop_arrow(0, 1); loop_arrow(1, 2); loop_arrow(2, 3); loop_arrow(3, 0)

    # center hub
    c.circle(380, 225, 48, GOLD, LIGHT_GOLD)
    c.text_c(380, 213, "ADAPTIVE", BLACK, 1)
    c.text_c(380, 229, "ENERGY MGMT", BLACK, 1)
    c.text_c(380, 245, "efficiency+stability", GRAY, 1)

    c.text(40, 444, "Figure 4: Forecasting, RL optimization, and demand-side control interact continuously", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Energy_Management_Loop.png'))
    print("  Figure_4_Energy_Management_Loop.png done")


def gen_fig5():
    """Figure 5: Digital twin applications across smart grid domains."""
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "Digital Twin Applications Across Smart Grid Domains", BLACK, 2)

    # Central integrated digital twin
    c.circle(380, 230, 60, PURPLE, LIGHT_PURPLE)
    c.text_c(380, 215, "INTEGRATED", BLACK, 1)
    c.text_c(380, 231, "DIGITAL TWIN", BLACK, 1)
    c.text_c(380, 247, "+ AI", GRAY, 1)

    domains = [
        ("Photovoltaic", "performance, fault detect", 380, 70, MED_BLUE, LIGHT_BLUE),
        ("Wind energy", "condition, maintenance", 620, 150, MED_GREEN, LIGHT_GREEN),
        ("Battery storage", "SoC/SoH, safety", 650, 320, ORANGE, LIGHT_ORANGE),
        ("Electric vehicles", "charging, V2G", 380, 395, RED, LIGHT_RED),
        ("Microgrids / DER", "balance, coordination", 110, 320, GOLD, LIGHT_GOLD),
        ("Distribution", "state estimation", 110, 150, DARK_GREEN, LIGHT_GREEN),
    ]
    for lab, sub, cx, cy, co, fi in domains:
        c.rect(cx - 90, cy - 30, cx + 90, cy + 30, co, fi)
        c.text_c(cx, cy - 8, lab, BLACK, 1)
        c.text_c(cx, cy + 10, sub, GRAY, 1)
        # connect to center
        dx, dy = 380 - cx, 230 - cy
        d = math.hypot(dx, dy)
        ox, oy = dx / d, dy / d
        sx, sy = int(cx + ox * 92), int(cy + oy * 32)
        ex, ey = int(380 - ox * 62), int(230 - oy * 62)
        c.line(sx, sy, ex, ey, GRAY, 2)

    c.text(40, 444, "Figure 5: A common twin framework spans generation, storage, EVs, and microgrids", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_Domain_Applications.png'))
    print("  Figure_5_Domain_Applications.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating emerging-trends chapter figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    gen_fig5()
    print(f"\nAll figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz / 1024:.1f} KB")


if __name__ == '__main__':
    main()
