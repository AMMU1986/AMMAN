#!/usr/bin/env python3
"""
Generate 4 original conceptual figures (PNG) for the chapter
"Sustainable Land Management to Achieve a Land Degradation Neutral World".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Drivers, processes, and cascading impacts of land degradation
             under a changing climate
  Figure 2 - The LDN response hierarchy (avoid-reduce-reverse) and the
             neutrality counterbalancing mechanism
  Figure 3 - Digital workflow for land-degradation assessment and LDN
             monitoring, from data to decision support
  Figure 4 - Participatory watershed management in Sukhomajri: interventions
             and their biophysical and socio-economic outcomes
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/slm_figures'


def gen_fig1():
    """Figure 1: Drivers -> processes -> impacts cascade with climate multiplier."""
    c = PNGCanvas(840, 520)
    c.text_c(420, 10, "Drivers, Processes, and Cascading Impacts of Land Degradation", BLACK, 2)

    # Climate-change threat-multiplier band across the top
    c.rect(40, 40, 800, 72, RED, LIGHT_RED)
    c.text_c(420, 50, "CLIMATE CHANGE  -  threat multiplier across every stage", BLACK, 1)

    col_top = 110
    box_h = 36
    gap = 10

    # Column 1: Drivers
    c.text_c(150, 90, "DRIVERS", BLACK, 1)
    drivers = [
        ("Unsustainable cultivation", MED_BLUE, LIGHT_BLUE),
        ("Overgrazing", MED_BLUE, LIGHT_BLUE),
        ("Deforestation", MED_BLUE, LIGHT_BLUE),
        ("Improper irrigation", MED_BLUE, LIGHT_BLUE),
        ("Urban expansion", MED_BLUE, LIGHT_BLUE),
    ]
    for i, (lbl, col, fill) in enumerate(drivers):
        y = col_top + i * (box_h + gap)
        c.rect(50, y, 250, y + box_h, col, fill)
        c.text_c(150, y + box_h // 2 - 4, lbl, BLACK, 1)

    # Column 2: Processes
    c.text_c(420, 90, "PROCESSES", BLACK, 1)
    procs = [
        ("Soil erosion", DARK_GREEN, LIGHT_GREEN),
        ("Loss of soil organic carbon", DARK_GREEN, LIGHT_GREEN),
        ("Salinization & compaction", DARK_GREEN, LIGHT_GREEN),
        ("Vegetation & biodiversity loss", DARK_GREEN, LIGHT_GREEN),
    ]
    for i, (lbl, col, fill) in enumerate(procs):
        y = col_top + i * (box_h + gap) + 20
        c.rect(320, y, 520, y + box_h, col, fill)
        c.text_c(420, y + box_h // 2 - 4, lbl, BLACK, 1)

    # Column 3: Impacts
    c.text_c(690, 90, "IMPACTS", BLACK, 1)
    impacts = [
        ("Food insecurity &", "yield decline", ORANGE, LIGHT_ORANGE),
        ("Water-cycle disruption", "(drought & floods)", ORANGE, LIGHT_ORANGE),
        ("Biodiversity &", "ecosystem-service loss", ORANGE, LIGHT_ORANGE),
        ("Poverty, displacement", "& migration", ORANGE, LIGHT_ORANGE),
    ]
    for i, (l1, l2, col, fill) in enumerate(impacts):
        y = col_top + i * (box_h + gap) + 20
        c.rect(590, y, 800, y + box_h, col, fill)
        c.text_c(695, y + 8, l1, BLACK, 1)
        c.text_c(695, y + 22, l2, BLACK, 1)

    # Arrows between columns
    c.arrow(252, 210, 318, 210, GRAY, 3, 11)
    c.arrow(522, 210, 588, 210, GRAY, 3, 11)

    # Feedback loop: impacts -> climate band -> drivers (vicious cycle)
    c.line(695, col_top + 20, 695, 350, PURPLE, 2)
    c.line(150, 350, 695, 350, PURPLE, 2)
    c.line(150, 350, 150, col_top, PURPLE, 2)
    # mark the loop with arrowheads
    c.arrow(697, 352, 695, 342, PURPLE, 2, 9)
    c.arrow(150, 300, 150, col_top, PURPLE, 2, 9)
    c.text_c(420, 356, "Reinforcing feedback: degraded land accelerates emissions and erodes resilience", PURPLE, 1)

    # Interpretive footer
    c.rect(40, 440, 800, 492, GRAY, (250, 250, 250))
    c.text_c(420, 452, "Biophysical degradation and human vulnerability are mutually reinforcing, not separable", BLACK, 1)
    c.text_c(420, 470, "Prevention (avoiding degradation) interrupts the cascade earliest and most cheaply", GRAY, 1)

    c.text(40, 504, "Figure 1: The land-degradation cascade and its climate feedbacks", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Degradation_Cascade.png'))
    print("  Figure_1_Degradation_Cascade.png done")


def gen_fig2():
    """Figure 2: LDN response hierarchy + counterbalancing (losses vs gains)."""
    c = PNGCanvas(840, 500)
    c.text_c(420, 10, "LDN Response Hierarchy and the Neutrality Counterbalancing Mechanism", BLACK, 2)

    # (a) Avoid / Reduce / Reverse hierarchy as stacked tiers
    c.text(95, 46, "(a) Response hierarchy", BLACK, 1)
    tiers = [
        ("AVOID", "responsible land-use planning; protect intact land", DARK_GREEN, LIGHT_GREEN, 70, 360),
        ("REDUCE", "sustainable management of land in use", GOLD, LIGHT_GOLD, 110, 320),
        ("REVERSE", "restoration & rehabilitation of degraded land", ORANGE, LIGHT_ORANGE, 150, 280),
    ]
    base_y = 250
    tier_h = 46
    for i, (name, sub, col, fill, x1, x2) in enumerate(tiers):
        y = base_y - i * (tier_h + 8)
        c.rect(x1, y, x2, y + tier_h, col, fill)
        c.text_c((x1 + x2) // 2, y + 10, name, BLACK, 1)
        c.text_c((x1 + x2) // 2, y + 28, sub, GRAY, 1)

    # priority arrow (top = highest priority)
    c.arrow(45, 250, 45, 72, DARK_BLUE, 3, 11)
    c.text(54, 150, "Priority", DARK_BLUE, 1)
    c.text(70, 312, "Larger area / lower cost at the base; restoration is the last resort", GRAY, 1)

    # (b) Counterbalancing: losses offset by gains -> no net loss
    c.text(440, 46, "(b) Counterbalancing within a land type", BLACK, 1)
    axis_x = 470
    zero_y = 230
    c.hline(axis_x, 800, zero_y, BLACK)   # zero line
    c.vline(axis_x, 90, 360, BLACK)       # value axis
    c.text(axis_x - 40, 150, "gain", DARK_GREEN, 1)
    c.text(axis_x - 40, 300, "loss", RED, 1)

    # losses (down bars)
    losses = [("New", 70), ("Ongoing", 50)]
    bx = axis_x + 30
    for lbl, v in losses:
        c.rect(bx, zero_y, bx + 50, zero_y + v, RED, LIGHT_RED)
        c.text_c(bx + 25, zero_y + v + 6, lbl, BLACK, 1)
        bx += 80
    c.text_c(axis_x + 95, zero_y + 92, "LOSSES", RED, 1)

    # gains (up bars)
    gains = [("Reduced", 55), ("Restored", 65)]
    bx = axis_x + 200
    for lbl, v in gains:
        c.rect(bx, zero_y - v, bx + 50, zero_y, DARK_GREEN, LIGHT_GREEN)
        c.text_c(bx + 25, zero_y - v - 12, lbl, BLACK, 1)
        bx += 80
    c.text_c(axis_x + 265, zero_y + 20, "GAINS", DARK_GREEN, 1)

    # net = zero
    c.arrow(axis_x + 150, zero_y + 110, axis_x + 240, zero_y + 110, GRAY, 2, 9)
    c.rect(axis_x + 150, 300, axis_x + 330, 340, DARK_BLUE, PALE_BLUE)
    c.text_c(axis_x + 240, 312, "NET = ZERO", BLACK, 1)
    c.text_c(axis_x + 240, 328, "no net loss (neutrality)", GRAY, 1)

    # footer
    c.rect(40, 400, 800, 452, GRAY, (250, 250, 250))
    c.text_c(420, 412, "Anticipated losses in land-based natural capital are offset by equivalent gains of the same land type", BLACK, 1)
    c.text_c(420, 430, "so that the quality and quantity of land resources remain stable or increase", GRAY, 1)

    c.text(40, 480, "Figure 2: Prioritising avoidance, then reduction, then reversal, within a neutrality accounting framework", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_LDN_Hierarchy.png'))
    print("  Figure_2_LDN_Hierarchy.png done")


def gen_fig3():
    """Figure 3: Digital monitoring workflow (methodology flowchart)."""
    c = PNGCanvas(920, 470)
    c.text_c(460, 10, "Digital Workflow for Land-Degradation Assessment and LDN Monitoring", BLACK, 2)

    # Stage boxes left-to-right
    stages = [
        ("DATA\nACQUISITION", ["Satellite imagery", "Field sampling", "Climate & terrain"], DARK_BLUE, PALE_BLUE),
        ("GIS\nINTEGRATION", ["Pre-processing", "Layer overlay", "Harmonisation"], MED_BLUE, LIGHT_BLUE),
        ("AI\nANALYSIS", ["Classification", "Change detection", "Early warning"], PURPLE, LIGHT_PURPLE),
        ("LDN\nINDICATORS", ["Land cover", "Productivity", "Soil organic C"], DARK_GREEN, LIGHT_GREEN),
        ("DECISION\nSUPPORT", ["Target hotspots", "SDG 15.3.1 report", "Plan & finance"], ORANGE, LIGHT_ORANGE),
    ]
    bw, bh = 150, 130
    top = 90
    x0 = 20
    step = 180
    centers = []
    for i, (title, items, col, fill) in enumerate(stages):
        x = x0 + i * step
        c.rect(x, top, x + bw, top + bh, col, fill)
        # title (two lines)
        t1, t2 = title.split("\n")
        c.text_c(x + bw // 2, top + 8, t1, BLACK, 1)
        c.text_c(x + bw // 2, top + 22, t2, BLACK, 1)
        c.hline(x + 12, x + bw - 12, top + 40, col)
        for j, it in enumerate(items):
            c.text_c(x + bw // 2, top + 54 + j * 20, it, GRAY, 1)
        centers.append((x + bw // 2, top + bh // 2))
        if i < len(stages) - 1:
            c.arrow(x + bw + 2, top + bh // 2, x + bw + step - bw - 2, top + bh // 2, GRAY, 3, 11)

    # Feedback loop from decision support back to data acquisition
    y_fb = top + bh + 60
    c.line(centers[-1][0], top + bh, centers[-1][0], y_fb, MED_GREEN, 2)
    c.line(centers[0][0], y_fb, centers[-1][0], y_fb, MED_GREEN, 2)
    c.arrow(centers[0][0], y_fb, centers[0][0], top + bh, MED_GREEN, 2, 10)
    c.text_c(460, y_fb + 8, "Iterative monitoring & verification feedback (track progress toward neutrality)", MED_GREEN, 1)

    # footer
    c.rect(20, 380, 900, 432, GRAY, (250, 250, 250))
    c.text_c(460, 392, "Remote sensing supplies synoptic coverage; field data and GIS add ground truth; AI scales the analysis;", BLACK, 1)
    c.text_c(460, 410, "the three globally agreed indicators convert observations into comparable, decision-relevant information", GRAY, 1)

    c.text(20, 452, "Figure 3: From raw Earth observation to actionable LDN indicators and land-use decisions", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Monitoring_Workflow.png'))
    print("  Figure_3_Monitoring_Workflow.png done")


def gen_fig4():
    """Figure 4: Sukhomajri interventions + before/after outcomes."""
    c = PNGCanvas(860, 500)
    c.text_c(430, 10, "Sukhomajri: Participatory Watershed Management and Its Outcomes", BLACK, 2)

    # (a) Schematic of the watershed interventions
    c.text(30, 42, "(a) Watershed interventions (Shivalik foothills)", BLACK, 1)

    # degraded-to-restored hill slope
    # slope line
    c.line(40, 230, 300, 90, DARK_GREEN, 2)
    c.line(40, 230, 40, 300, GRAY, 2)
    c.hline(40, 420, 300, GRAY)
    # regenerated trees on the hill (social fencing -> regeneration)
    for i, tx in enumerate(range(90, 300, 34)):
        ty = 230 - (tx - 40) * (140.0 / 260)
        c.circle(tx, int(ty) - 10, 7, DARK_GREEN, LIGHT_GREEN)
        c.vline(tx, int(ty) - 3, int(ty) + 6, (120, 80, 40))
    c.text(70, 70, "Social fencing + stall-feeding", DARK_GREEN, 1)
    c.text(70, 84, "-> forest regeneration", GRAY, 1)

    # check dams on the stream
    for i, dx in enumerate([120, 190, 260]):
        dy = 230 - (dx - 40) * (140.0 / 260)
        c.rect(dx - 6, int(dy), dx + 6, int(dy) + 22, MED_BLUE, LIGHT_BLUE)
    c.text(60, 232, "Check dams harvest runoff & trap silt", MED_BLUE, 1)

    # village + farmland in valley
    c.rect(60, 250, 110, 290, ORANGE, LIGHT_ORANGE)
    c.text_c(85, 266, "Village", BLACK, 1)
    c.fill_rect(130, 270, 300, 298, LIGHT_GREEN)
    c.text(140, 278, "Irrigated farmland (182 ha)", BLACK, 1)

    # downstream reservoir (Sukhna Lake)
    c.fill_rect(320, 250, 420, 300, LIGHT_BLUE)
    c.rect(320, 250, 420, 300, MED_BLUE)
    c.text_c(370, 262, "Sukhna Lake", BLACK, 1)
    c.text_c(370, 278, "(less silting)", GRAY, 1)
    c.arrow(300, 285, 318, 285, MED_BLUE, 2, 8)

    # institution label
    c.rect(30, 320, 420, 352, PURPLE, LIGHT_PURPLE)
    c.text_c(225, 330, "Hill Resource Management Societies: equitable water rights incl. landless", BLACK, 1)

    # (b) Before/after outcomes (relative index bars)
    c.text(460, 42, "(b) Reported outcomes (before vs after)", BLACK, 1)
    ind = [
        ("Tree density", 4, 98, "13 -> ~1,270 /ha"),
        ("Water for irrigation", 8, 85, "rainfed -> stored"),
        ("Household income", 20, 80, "subsistence -> higher"),
        ("Sediment to lake", 95, 30, "very high -> reduced"),
    ]
    bx0 = 470
    top = 70
    row_h = 78
    max_w = 300
    for i, (name, before, after, note) in enumerate(ind):
        y = top + i * row_h
        c.text(bx0, y, name, BLACK, 1)
        # before bar
        c.rect(bx0, y + 14, bx0 + int(before / 100.0 * max_w), y + 30, RED, LIGHT_RED)
        c.text(bx0 + int(before / 100.0 * max_w) + 4, y + 17, "before", GRAY, 1)
        # after bar
        c.rect(bx0, y + 34, bx0 + int(after / 100.0 * max_w), y + 50, DARK_GREEN, LIGHT_GREEN)
        c.text(bx0 + int(after / 100.0 * max_w) + 4, y + 37, "after", GRAY, 1)
        c.text(bx0, y + 54, note, GRAY, 1)

    # durability caveat
    c.rect(460, 392, 830, 440, GOLD, LIGHT_GOLD)
    c.text_c(645, 402, "Caveat: gains later eroded where dam maintenance", BLACK, 1)
    c.text_c(645, 418, "and community institutions weakened over time", GRAY, 1)

    c.text(30, 372, "Sediment bar is inverted in meaning: a shorter 'after' bar is the desired outcome", GRAY, 1)
    c.text(30, 478, "Figure 4: Integrated interventions reversed degradation across soil, water, vegetation, and livelihoods", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_Sukhomajri.png'))
    print("  Figure_4_Sukhomajri.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating SLM / LDN chapter figures...")
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
