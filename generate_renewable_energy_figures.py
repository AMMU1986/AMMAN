#!/usr/bin/env python3
"""
Generate 5 figure images (PNG) for the chapter
"Renewable Energy Integration and Forecasting".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py
so it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Architecture of an AI-enabled smart grid
  Figure 2 - LSTM cell structure for time-series forecasting
  Figure 3 - Data flow: sensing -> fusion -> forecasting -> control
  Figure 4 - Closed-loop AI-enabled energy management
  Figure 5 - Federated learning across decentralized energy participants
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/renewable_figures'


def gen_fig1():
    """Figure 1: Architecture of an AI-enabled smart grid."""
    c = PNGCanvas(760, 480)
    c.text_c(380, 10, "AI-Enabled Smart Grid Architecture", BLACK, 2)

    # Central grid / control bus
    bus_y = 250
    c.fill_rect(60, bus_y - 3, 700, bus_y + 3, DARK_BLUE)
    c.text_c(380, bus_y + 10, "Smart Grid Network (bidirectional power + data)", GRAY, 1)

    # Generation sources (top left)
    gens = [
        ("Solar PV", 90, MED_BLUE, LIGHT_BLUE),
        ("Wind", 230, MED_GREEN, LIGHT_GREEN),
        ("Hybrid", 370, PURPLE, LIGHT_PURPLE),
    ]
    for lab, x, co, fi in gens:
        c.rect(x - 55, 60, x + 55, 110, co, fi)
        c.text_c(x, 80, lab, BLACK, 1)
        c.arrow(x, 110, x, bus_y - 4, co, 2, 8)

    # Storage (top right)
    c.rect(500, 60, 610, 110, ORANGE, LIGHT_ORANGE)
    c.text_c(555, 78, "Storage", BLACK, 1)
    c.text_c(555, 94, "(battery)", GRAY, 1)
    c.arrow(555, 110, 555, bus_y - 4, ORANGE, 2, 8)
    # bidirectional
    c.arrow(545, bus_y - 4, 545, 110, GRAY, 1, 6)

    # Distributed resources (far right)
    c.rect(635, 60, 720, 110, GOLD, LIGHT_GOLD)
    c.text_c(677, 78, "DER /", BLACK, 1)
    c.text_c(677, 94, "EV", BLACK, 1)
    c.arrow(677, 110, 677, bus_y - 4, GOLD, 2, 8)

    # Loads (bottom)
    loads = [
        ("Residential", 120, MED_BLUE, LIGHT_BLUE),
        ("Commercial", 290, MED_GREEN, LIGHT_GREEN),
        ("Industrial", 460, PURPLE, LIGHT_PURPLE),
        ("Flexible loads", 630, RED, LIGHT_RED),
    ]
    for lab, x, co, fi in loads:
        c.rect(x - 60, 330, x + 60, 380, co, fi)
        c.text_c(x, 350, lab, BLACK, 1)
        c.arrow(x, bus_y + 4, x, 330, co, 2, 8)

    # AI control center
    c.rect(250, 410, 510, 465, DARK_GREEN, LIGHT_GREEN)
    c.text_c(380, 425, "AI CONTROL CENTER", BLACK, 1)
    c.text_c(380, 445, "forecast - optimize - dispatch - balance", GRAY, 1)
    # data links (dashed-look) from control to bus
    c.line(380, 410, 380, 388, DARK_GREEN, 1)
    c.arrow(380, 388, 380, 384, DARK_GREEN, 1, 6)

    c.text(40, 472, "Figure 1: Variable generation, storage, flexible loads, and AI control within one system", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Smart_Grid_Architecture.png'))
    print("  Figure_1_Smart_Grid_Architecture.png done")


def gen_fig2():
    """Figure 2: LSTM cell structure for time-series forecasting."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "LSTM Cell for Renewable Energy Time-Series Forecasting", BLACK, 2)

    # Cell boundary
    c.rect(150, 90, 610, 300, DARK_BLUE, (245, 248, 255))
    c.text_c(380, 100, "LSTM memory cell", GRAY, 1)

    # Cell state line (top, horizontal)
    c.fill_rect(170, 135, 590, 139, DARK_GREEN)
    c.text(175, 120, "Cell state  C(t-1) -> C(t)", DARK_GREEN, 1)

    # Gates
    gates = [
        ("Forget", 230, RED, LIGHT_RED),
        ("Input", 330, ORANGE, LIGHT_ORANGE),
        ("Candidate", 430, PURPLE, LIGHT_PURPLE),
        ("Output", 530, MED_GREEN, LIGHT_GREEN),
    ]
    for lab, x, co, fi in gates:
        c.rect(x - 40, 200, x + 40, 250, co, fi)
        c.text_c(x, 220, lab, BLACK, 1)
        c.text_c(x, 234, "gate", BLACK, 1)
        # gate acts on cell state
        c.arrow(x, 200, x, 141, co, 2, 7)

    # hidden state in/out
    c.rect(40, 200, 130, 250, MED_BLUE, LIGHT_BLUE)
    c.text_c(85, 218, "h(t-1)", BLACK, 1)
    c.text_c(85, 234, "input x(t)", BLACK, 1)
    c.arrow(130, 225, 150, 225, GRAY, 2, 8)
    c.rect(630, 200, 720, 250, MED_BLUE, LIGHT_BLUE)
    c.text_c(675, 218, "h(t)", BLACK, 1)
    c.text_c(675, 234, "output", BLACK, 1)
    c.arrow(610, 225, 630, 225, GRAY, 2, 8)

    # Application strip: time series -> forecast
    c.text(40, 330, "Application: learn long-range temporal dependence", BLACK, 1)
    # draw a wiggly generation series
    ax, ay = 60, 420
    c.hline(ax, 560, ay, BLACK)
    c.vline(ax, 350, ay, BLACK)
    c.text(10, 380, "Power", BLACK, 1)
    import math as m
    prev = None
    for x in range(ax + 2, 420):
        t = (x - ax) / 60.0
        y = int(ay - 45 - 25 * m.sin(t) - 12 * m.sin(3 * t + 1))
        if prev:
            c.line(prev[0], prev[1], x, y, MED_GREEN, 2)
        prev = (x, y)
    # forecast continuation (dashed look, different color)
    for x in range(420, 560, 4):
        t = (x - ax) / 60.0
        y = int(ay - 45 - 25 * m.sin(t) - 12 * m.sin(3 * t + 1))
        c.pixel(x, y, ORANGE); c.pixel(x, y + 1, ORANGE)
    c.line(420, 355, 420, ay, GRAY, 1)
    c.text(300, 352, "history", MED_GREEN, 1)
    c.text(470, 352, "forecast", ORANGE, 1)

    # legend box
    c.rect(590, 350, 730, 430, LIGHT_GRAY, (250, 250, 250))
    c.text(600, 360, "Gates control:", BLACK, 1)
    c.text(600, 380, "- what to forget", RED, 1)
    c.text(600, 396, "- what to store", ORANGE, 1)
    c.text(600, 412, "- what to output", MED_GREEN, 1)

    c.text(40, 458, "Figure 2: Gated memory cell captures long-range temporal patterns in energy data", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_LSTM_Cell.png'))
    print("  Figure_2_LSTM_Cell.png done")


def gen_fig3():
    """Figure 3: Data flow from sensing to control."""
    c = PNGCanvas(760, 460)
    c.text_c(380, 10, "Data Flow in an AI-Enabled Smart Grid", BLACK, 2)

    # Layer 1: sensing sources (left column)
    srcs = [
        ("Smart meters", MED_BLUE, LIGHT_BLUE),
        ("IoT sensors", MED_GREEN, LIGHT_GREEN),
        ("Weather service", ORANGE, LIGHT_ORANGE),
        ("Sky/satellite imagery", PURPLE, LIGHT_PURPLE),
    ]
    sx1, sx2 = 30, 210
    top = 55
    bh = 60
    gap = 18
    src_centers = []
    for i, (lab, co, fi) in enumerate(srcs):
        y1 = top + i * (bh + gap)
        c.rect(sx1, y1, sx2, y1 + bh, co, fi)
        c.text_c((sx1 + sx2) // 2, y1 + bh // 2 - 4, lab, BLACK, 1)
        src_centers.append((sx2, y1 + bh // 2))

    # Layer 2: data fusion / cleaning
    fx1, fx2 = 270, 420
    fy1, fy2 = 120, 300
    c.rect(fx1, fy1, fx2, fy2, GOLD, LIGHT_GOLD)
    c.text_c((fx1 + fx2) // 2, fy1 + 30, "DATA FUSION", BLACK, 1)
    c.text_c((fx1 + fx2) // 2, fy1 + 55, "& QUALITY", BLACK, 1)
    c.text_c((fx1 + fx2) // 2, fy1 + 80, "CONTROL", BLACK, 1)
    c.text_c((fx1 + fx2) // 2, fy1 + 110, "clean, sync,", GRAY, 1)
    c.text_c((fx1 + fx2) // 2, fy1 + 126, "impute, align", GRAY, 1)
    for (ex, ey) in src_centers:
        c.arrow(ex + 2, ey, fx1 - 2, (fy1 + fy2) // 2, GRAY, 2, 7)

    # Layer 3: analytics / forecasting
    ax1, ax2 = 470, 620
    ay1, ay2 = 90, 200
    c.rect(ax1, ay1, ax2, ay2, MED_GREEN, LIGHT_GREEN)
    c.text_c((ax1 + ax2) // 2, ay1 + 26, "AI ANALYTICS", BLACK, 1)
    c.text_c((ax1 + ax2) // 2, ay1 + 48, "forecasting,", GRAY, 1)
    c.text_c((ax1 + ax2) // 2, ay1 + 64, "anomaly detection", GRAY, 1)
    c.arrow(fx2 + 2, (fy1 + fy2) // 2 - 40, ax1 - 2, (ay1 + ay2) // 2, GRAY, 2, 8)

    # Layer 4: decision / control
    dx1, dx2 = 470, 620
    dy1, dy2 = 230, 340
    c.rect(dx1, dy1, dx2, dy2, RED, LIGHT_RED)
    c.text_c((dx1 + dx2) // 2, dy1 + 26, "DECISION &", BLACK, 1)
    c.text_c((dx1 + dx2) // 2, dy1 + 44, "CONTROL", BLACK, 1)
    c.text_c((dx1 + dx2) // 2, dy1 + 66, "dispatch, storage,", GRAY, 1)
    c.text_c((dx1 + dx2) // 2, dy1 + 82, "demand response", GRAY, 1)
    c.arrow(fx2 + 2, (fy1 + fy2) // 2 + 40, dx1 - 2, (dy1 + dy2) // 2, GRAY, 2, 8)
    c.arrow((ax1 + ax2) // 2, ay2 + 2, (dx1 + dx2) // 2, dy1 - 2, GRAY, 2, 7)

    # Grid box
    c.rect(650, 160, 740, 270, DARK_BLUE, PALE_BLUE)
    c.text_c(695, 200, "GRID", BLACK, 1)
    c.text_c(695, 220, "(physical", GRAY, 1)
    c.text_c(695, 234, "system)", GRAY, 1)
    c.arrow(dx2 + 2, (dy1 + dy2) // 2, 650 - 2, 230, RED, 2, 8)
    # feedback loop grid -> sensing
    c.line(695, 270, 695, 400, GRAY, 1)
    c.line(695, 400, 120, 400, GRAY, 1)
    c.arrow(120, 400, 120, top + 4 * (bh + gap) - 10, GRAY, 1, 7)
    c.text(300, 404, "feedback: new measurements", GRAY, 1)

    c.text(40, 440, "Figure 3: Distributed sensing and weather fusion feed forecasting, decision, and control", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Data_Flow.png'))
    print("  Figure_3_Data_Flow.png done")


def gen_fig4():
    """Figure 4: Closed-loop AI-enabled energy management."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Closed-Loop AI-Enabled Energy Management", BLACK, 2)

    # four stages around a loop
    stages = [
        ("FORECAST", "generation, demand, price", 380, 70, MED_BLUE, LIGHT_BLUE),
        ("OPTIMIZE", "storage + demand response", 600, 230, ORANGE, LIGHT_ORANGE),
        ("ACT", "dispatch, charge/discharge", 380, 390, RED, LIGHT_RED),
        ("MEASURE", "grid state via sensors", 160, 230, MED_GREEN, LIGHT_GREEN),
    ]
    bw, bh = 170, 70
    centers = []
    for title, sub, cx, cy, co, fi in stages:
        c.rect(cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2, co, fi)
        c.text_c(cx, cy - 10, title, BLACK, 1)
        c.text_c(cx, cy + 10, sub, GRAY, 1)
        centers.append((cx, cy))

    # clockwise arrows
    def loop_arrow(a, b):
        ax, ay = centers[a]; bx, by = centers[b]
        dx, dy = bx - ax, by - ay
        d = math.hypot(dx, dy)
        ox, oy = dx / d, dy / d
        sx, sy = int(ax + ox * 95), int(ay + oy * 50)
        ex, ey = int(bx - ox * 95), int(by - oy * 50)
        c.arrow(sx, sy, ex, ey, GRAY, 3, 10)

    loop_arrow(0, 1); loop_arrow(1, 2); loop_arrow(2, 3); loop_arrow(3, 0)

    # center hub
    c.circle(380, 230, 46, GOLD, LIGHT_GOLD)
    c.text_c(380, 218, "PREDICTIVE", BLACK, 1)
    c.text_c(380, 234, "CONTROL", BLACK, 1)
    c.text_c(380, 250, "(MPC / RL)", GRAY, 1)

    # note
    c.text_c(380, 438, "Forecast quality sets the ceiling on every downstream decision", DARK_GREEN, 1)

    c.text(40, 460, "Figure 4: Continuous loop coordinating forecasting, demand response, storage, and balancing", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Energy_Management_Loop.png'))
    print("  Figure_4_Energy_Management_Loop.png done")


def gen_fig5():
    """Figure 5: Federated learning across decentralized participants."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Federated Learning Across Decentralized Energy Participants", BLACK, 2)

    # Central aggregation server
    c.rect(300, 60, 460, 130, DARK_GREEN, LIGHT_GREEN)
    c.text_c(380, 80, "AGGREGATION SERVER", BLACK, 1)
    c.text_c(380, 100, "global model", BLACK, 1)
    c.text_c(380, 114, "(averages updates)", GRAY, 1)

    # Participants
    parts = [
        ("Utility A", 90, 300, MED_BLUE, LIGHT_BLUE),
        ("Aggregator B", 290, 340, ORANGE, LIGHT_ORANGE),
        ("Prosumer C", 490, 340, PURPLE, LIGHT_PURPLE),
        ("Microgrid D", 660, 300, RED, LIGHT_RED),
    ]
    for lab, cx, cy, co, fi in parts:
        c.rect(cx - 70, cy, cx + 70, cy + 55, co, fi)
        c.text_c(cx, cy + 16, lab, BLACK, 1)
        c.text_c(cx, cy + 34, "local model", GRAY, 1)
        # local private data store
        c.rect(cx - 45, cy + 62, cx + 45, cy + 92, LIGHT_GRAY, (248, 248, 248))
        c.text_c(cx, cy + 70, "local data", BLACK, 1)
        c.text_c(cx, cy + 84, "(never shared)", GRAY, 1)
        # up arrow: send model update
        c.arrow(cx - 12, cy - 2, 350, 132, MED_GREEN, 2, 7)
        # down arrow: receive global model
        c.arrow(410, 132, cx + 12, cy - 2, DARK_BLUE, 2, 7)

    # legend of arrows
    c.rect(300, 150, 460, 215, LIGHT_GRAY, (250, 250, 250))
    c.text(312, 160, "Up (green): model updates", MED_GREEN, 1)
    c.text(312, 178, "Down (blue): global model", DARK_BLUE, 1)
    c.text(312, 196, "Raw data stays local", RED, 1)

    c.text(40, 452, "Figure 5: Participants train collaboratively while raw consumption data remains private", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_5_Federated_Learning.png'))
    print("  Figure_5_Federated_Learning.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating renewable-energy chapter figures...")
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
