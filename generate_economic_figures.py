#!/usr/bin/env python3
"""
Generate 4 high-resolution figure images (PNG) for the chapter
"Counting the Cost of Delay: Economic Consequences of Climate Inaction".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies (no matplotlib / PIL / numpy) in
the sandbox. Canvases are rendered at large pixel dimensions for high
resolution suitable for print (>=300 dpi at typical figure widths).

Figures:
  Figure 1 - Taxonomy of the economic consequences of climate inaction
  Figure 2 - Realised and projected global economic losses (US$ trillion)
  Figure 3 - Inequity of the burden of climate inaction (country groups)
  Figure 4 - The economic logic of action vs. inaction, with co-benefits
"""

import os

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

OUTPUT_DIR = '/projects/sandbox/AMMAN/economic_figures'


def gen_fig1():
    """Figure 1: Taxonomy / transmission channels of climate inaction costs."""
    c = PNGCanvas(1600, 1040)
    c.text_c(800, 24, "Economic Consequences of Climate Inaction: Hazards, Cost Channels, and Impact Domains", BLACK, 3)

    def box(x1, y1, x2, y2, outline, fill, title, sub1=None, sub2=None):
        c.rect(x1, y1, x2, y2, outline, fill)
        # thicken outline
        c.rect(x1 + 1, y1 + 1, x2 - 1, y2 - 1, outline)
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        if sub1 is None and sub2 is None:
            c.text_c(cx, cy - 10, title, BLACK, 3)
        else:
            c.text_c(cx, cy - 34, title, BLACK, 3)
            if sub1:
                c.text_c(cx, cy + 4, sub1, GRAY, 2)
            if sub2:
                c.text_c(cx, cy + 32, sub2, GRAY, 2)

    # Row labels
    c.text(40, 120, "HAZARDS", MED_BLUE, 2)
    c.text(40, 420, "COST CHANNELS", MED_BLUE, 2)
    c.text(40, 720, "IMPACT DOMAINS", MED_BLUE, 2)

    # Row 1: hazards
    hz = [
        (300, "Heat and humidity", "rising wet-bulb temperatures", DARK_BLUE, PALE_BLUE),
        (720, "Extreme events", "floods, storms, wildfires", DARK_BLUE, PALE_BLUE),
        (1140, "Shifting disease ecology", "vector and water-borne spread", DARK_BLUE, PALE_BLUE),
    ]
    r1y1, r1y2 = 150, 300
    hz_centers = []
    for x, t, s, col, fill in hz:
        box(x, r1y1, x + 360, r1y2, col, fill, t, s)
        hz_centers.append(((x + x + 360) // 2, r1y2))

    # Row 2: cost channels
    cc = [
        (300, "Direct damages", "capital, crops, medical care", DARK_GREEN, LIGHT_GREEN),
        (720, "Indirect losses", "labour, output, supply chains", DARK_GREEN, LIGHT_GREEN),
        (1140, "Intangible / non-market", "mortality, well-being, ecosystems", DARK_GREEN, LIGHT_GREEN),
    ]
    r2y1, r2y2 = 450, 600
    cc_centers_top = []
    cc_centers_bot = []
    for x, t, s, col, fill in cc:
        box(x, r2y1, x + 360, r2y2, col, fill, t, s)
        cc_centers_top.append(((x + x + 360) // 2, r2y1))
        cc_centers_bot.append(((x + x + 360) // 2, r2y2))

    # Row 3: impact domains
    im = [
        (300, "Health systems", "demand up, capacity down", ORANGE, LIGHT_ORANGE),
        (720, "Labour productivity", "lost hours and output", ORANGE, LIGHT_ORANGE),
        (1140, "Macroeconomic stability", "growth, fiscal, finance", ORANGE, LIGHT_ORANGE),
    ]
    r3y1, r3y2 = 750, 900
    im_centers_top = []
    for x, t, s, col, fill in im:
        box(x, r3y1, x + 360, r3y2, col, fill, t, s)
        im_centers_top.append(((x + x + 360) // 2, r3y1))

    # Arrows hazards -> cost channels
    for (hx, hy), (cx, cy) in zip(hz_centers, cc_centers_top):
        c.arrow(hx, hy + 4, cx, cy - 4, GRAY, 3, 16)
    # cross-links (hazards each feed all channels, drawn lightly)
    c.arrow(hz_centers[0][0] + 40, r1y2 + 4, cc_centers_top[1][0] - 40, r2y1 - 4, LIGHT_GRAY, 2, 12)
    c.arrow(hz_centers[2][0] - 40, r1y2 + 4, cc_centers_top[1][0] + 40, r2y1 - 4, LIGHT_GRAY, 2, 12)

    # Arrows cost channels -> impact domains
    for (cx, cy), (ix, iy) in zip(cc_centers_bot, im_centers_top):
        c.arrow(cx, cy + 4, ix, iy - 4, GRAY, 3, 16)

    # Bottom summary bar
    c.rect(300, 950, 1500, 1010, GOLD, LIGHT_GOLD)
    c.rect(301, 951, 1499, 1009, GOLD)
    c.text_c(900, 965, "Rising, compounding, and inequitably distributed cost of inaction", BLACK, 3)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Cost_Taxonomy.png'))
    print("  Figure_1_Cost_Taxonomy.png done")


def gen_fig2():
    """Figure 2: Realised and projected global economic losses (US$ trillion)."""
    c = PNGCanvas(1600, 1000)
    c.text_c(800, 24, "Realised and Projected Global Economic Losses from Climate Inaction", BLACK, 3)
    c.text_c(800, 70, "(US$ trillion; 2024 realised vs. cumulative/annualised mid-century projections)", GRAY, 2)

    bars = [
        ("Heat labour\nloss 2024", 1.09, MED_BLUE, LIGHT_BLUE),
        ("Cross-sector\nprod. by 2050", 1.5, DARK_GREEN, LIGHT_GREEN),
        ("Healthcare\ncosts by 2050", 1.1, PURPLE, LIGHT_PURPLE),
        ("WEF cumulative\nby 2050", 12.5, ORANGE, LIGHT_ORANGE),
        ("LMIC cost\n(low) 26-50", 8.6, RED, LIGHT_RED),
        ("LMIC cost\n(high) 26-50", 20.8, RED, LIGHT_RED),
    ]

    # Axes
    ax_x = 220
    ax_y0 = 820          # baseline (value 0)
    ax_top = 150         # top of plot area
    plot_h = ax_y0 - ax_top
    vmax = 22.0
    c.line(ax_x, ax_top, ax_x, ax_y0, BLACK, 3)
    c.line(ax_x, ax_y0, 1540, ax_y0, BLACK, 3)
    c.text_c(90, (ax_top + ax_y0) // 2 - 30, "US$", BLACK, 2)
    c.text_c(90, (ax_top + ax_y0) // 2, "trillion", BLACK, 2)

    # gridlines and y labels every 4 trillion
    v = 0
    while v <= vmax:
        gy = int(ax_y0 - v / vmax * plot_h)
        c.hline(ax_x, 1540, gy, LIGHT_GRAY)
        c.text(ax_x - 80, gy - 8, f"{v:0.0f}", BLACK, 2)
        v += 4

    n = len(bars)
    slot = (1540 - ax_x - 40) // n
    bw = int(slot * 0.58)
    for i, (label, val, col, fill) in enumerate(bars):
        bx = ax_x + 40 + i * slot
        bh = int(val / vmax * plot_h)
        c.rect(bx, ax_y0 - bh, bx + bw, ax_y0, col, fill)
        c.rect(bx + 1, ax_y0 - bh + 1, bx + bw - 1, ax_y0 - 1, col)
        # value label
        c.text_c(bx + bw // 2, ax_y0 - bh - 34, f"{val:.2f}", BLACK, 2)
        # x labels (two lines)
        l1, l2 = label.split("\n")
        c.text_c(bx + bw // 2, ax_y0 + 16, l1, BLACK, 2)
        c.text_c(bx + bw // 2, ax_y0 + 44, l2, BLACK, 2)

    c.rect(240, 880, 1540, 960, GRAY, (250, 250, 250))
    c.text_c(890, 898, "The 2024 heat-productivity loss alone (~1% of global GDP) is already realised;", BLACK, 2)
    c.text_c(890, 926, "mid-century projections rise sharply and are largest for low- and middle-income countries", GRAY, 2)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Global_Cost_Trajectory.png'))
    print("  Figure_2_Global_Cost_Trajectory.png done")


def gen_fig3():
    """Figure 3: Inequity of the burden of climate inaction (grouped bars)."""
    c = PNGCanvas(1600, 1000)
    c.text_c(800, 24, "Inequity of the Burden of Climate Inaction Across Country Groups", BLACK, 3)
    c.text_c(800, 70, "(illustrative relative levels, %)", GRAY, 2)

    metrics = ["Exposure to\nhazards", "Adaptive\ncapacity", "Share of\nlosses", "Share of historical\nemissions"]
    high = [35, 85, 25, 70]
    low = [82, 28, 75, 30]

    ax_x = 180
    ax_y0 = 780
    ax_top = 150
    plot_h = ax_y0 - ax_top
    c.line(ax_x, ax_top, ax_x, ax_y0, BLACK, 3)
    c.line(ax_x, ax_y0, 1540, ax_y0, BLACK, 3)

    for v in range(0, 101, 20):
        gy = int(ax_y0 - v / 100.0 * plot_h)
        c.hline(ax_x, 1540, gy, LIGHT_GRAY)
        c.text(ax_x - 70, gy - 8, f"{v}", BLACK, 2)

    n = len(metrics)
    group_slot = (1540 - ax_x - 60) // n
    bw = int(group_slot * 0.30)
    for i, m in enumerate(metrics):
        gx = ax_x + 60 + i * group_slot
        # high income bar
        hh = int(high[i] / 100.0 * plot_h)
        c.rect(gx, ax_y0 - hh, gx + bw, ax_y0, DARK_BLUE, LIGHT_BLUE)
        c.rect(gx + 1, ax_y0 - hh + 1, gx + bw - 1, ax_y0 - 1, DARK_BLUE)
        c.text_c(gx + bw // 2, ax_y0 - hh - 30, f"{high[i]}", BLACK, 2)
        # low/middle income bar
        lx = gx + bw + 20
        lh = int(low[i] / 100.0 * plot_h)
        c.rect(lx, ax_y0 - lh, lx + bw, ax_y0, RED, LIGHT_RED)
        c.rect(lx + 1, ax_y0 - lh + 1, lx + bw - 1, ax_y0 - 1, RED)
        c.text_c(lx + bw // 2, ax_y0 - lh - 30, f"{low[i]}", BLACK, 2)
        # metric labels (two lines)
        l1, l2 = m.split("\n")
        mid = (gx + lx + bw) // 2
        c.text_c(mid, ax_y0 + 16, l1, BLACK, 2)
        c.text_c(mid, ax_y0 + 44, l2, BLACK, 2)

    # legend
    c.rect(300, 840, 340, 876, DARK_BLUE, LIGHT_BLUE)
    c.text(352, 848, "High-income countries", BLACK, 2)
    c.rect(820, 840, 860, 876, RED, LIGHT_RED)
    c.text(872, 848, "Low- and middle-income countries", BLACK, 2)
    c.text_c(800, 930, "Those least responsible for emissions bear the greatest harm with the least capacity to adapt", GRAY, 2)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Burden_Inequity.png'))
    print("  Figure_3_Burden_Inequity.png done")


def gen_fig4():
    """Figure 4: Economic logic of action vs inaction, with health co-benefits."""
    c = PNGCanvas(1600, 1000)
    c.text_c(800, 24, "The Economic Logic of Climate Action versus Inaction", BLACK, 3)
    c.text_c(800, 70, "(schematic relative magnitudes)", GRAY, 2)

    ax_x = 220
    ax_y0 = 800
    ax_top = 150
    plot_h = ax_y0 - ax_top
    c.line(ax_x, ax_top, ax_x, ax_y0, BLACK, 3)
    c.line(ax_x, ax_y0, 1540, ax_y0, BLACK, 3)
    c.text_c(110, (ax_top + ax_y0) // 2 - 30, "Relative", BLACK, 2)
    c.text_c(110, (ax_top + ax_y0) // 2, "economic", BLACK, 2)
    c.text_c(110, (ax_top + ax_y0) // 2 + 30, "magnitude", BLACK, 2)

    def bar(x, w, h, col, fill, y_base):
        c.rect(x, y_base - h, x + w, y_base, col, fill)
        c.rect(x + 1, y_base - h + 1, x + w - 1, y_base - 1, col)

    # Column 1: COST OF INACTION (tall, single damage block)
    x1 = ax_x + 120
    w = 300
    inaction_h = int(0.92 * plot_h)
    bar(x1, w, inaction_h, RED, LIGHT_RED, ax_y0)
    c.text_c(x1 + w // 2, ax_y0 - inaction_h - 36, "Accumulating", BLACK, 2)
    c.text_c(x1 + w // 2, ax_y0 - inaction_h - 10, "climate damages", BLACK, 2)
    c.text_c(x1 + w // 2, ax_y0 + 20, "COST OF", BLACK, 3)
    c.text_c(x1 + w // 2, ax_y0 + 50, "INACTION", BLACK, 3)

    # Column 2: COST OF ACTION (stacked mitigation + adaptation)
    x2 = x1 + w + 260
    mit_h = int(0.30 * plot_h)
    adp_h = int(0.16 * plot_h)
    bar(x2, w, mit_h, DARK_GREEN, LIGHT_GREEN, ax_y0)
    bar(x2, w, adp_h, MED_BLUE, LIGHT_BLUE, ax_y0 - mit_h)
    c.text_c(x2 + w // 2, ax_y0 - mit_h // 2 - 8, "Mitigation", BLACK, 2)
    c.text_c(x2 + w // 2, ax_y0 - mit_h - adp_h // 2 - 8, "Adaptation", BLACK, 2)
    c.text_c(x2 + w // 2, ax_y0 + 20, "COST OF", BLACK, 3)
    c.text_c(x2 + w // 2, ax_y0 + 50, "ACTION", BLACK, 3)

    # Co-benefits offset arrow (health + air quality) reducing net cost of action
    cob_top = ax_y0 - mit_h - adp_h
    c.rect(x2, cob_top - int(0.22 * plot_h), x2 + w, cob_top, GOLD, LIGHT_GOLD)
    c.rect(x2 + 1, cob_top - int(0.22 * plot_h) + 1, x2 + w - 1, cob_top - 1, GOLD)
    c.text_c(x2 + w // 2, cob_top - int(0.11 * plot_h) - 20, "Health &", BLACK, 2)
    c.text_c(x2 + w // 2, cob_top - int(0.11 * plot_h) + 8, "air-quality", BLACK, 2)
    c.text_c(x2 + w // 2, cob_top - int(0.11 * plot_h) + 36, "co-benefits", BLACK, 2)

    # dashed comparison line from top of inaction bar across
    top_y = ax_y0 - inaction_h
    xx = ax_x
    while xx < 1520:
        c.hline(xx, xx + 24, top_y, GRAY)
        xx += 48

    # big arrow pointing from inaction to action (the rational choice)
    c.arrow(x1 + w + 40, ax_y0 - int(0.5 * plot_h), x2 - 40, ax_y0 - int(0.5 * plot_h), DARK_GREEN, 5, 26)
    c.text_c((x1 + w + x2) // 2, ax_y0 - int(0.5 * plot_h) - 44, "the economically", DARK_GREEN, 2)
    c.text_c((x1 + w + x2) // 2, ax_y0 - int(0.5 * plot_h) - 16, "rational choice", DARK_GREEN, 2)

    c.rect(240, 880, 1540, 960, GRAY, (250, 250, 250))
    c.text_c(890, 898, "The cost of action - net of large health and air-quality co-benefits - is a fraction", BLACK, 2)
    c.text_c(890, 926, "of the accumulating cost of inaction", GRAY, 2)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Action_vs_Inaction.png'))
    print("  Figure_4_Action_vs_Inaction.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating economic-consequences chapter figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print(f"\nAll figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz / 1024:.1f} KB")


if __name__ == '__main__':
    main()
