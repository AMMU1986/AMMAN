#!/usr/bin/env python3
"""
Generate 4 figure images (PNG) for Chapter 17
"Robotics and Autonomous Systems in Healthcare".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 17.1 - Architecture of a closed-loop drug-delivery system
  Figure 17.2 - Layered control architecture of an AI-assisted surgical system
  Figure 17.3 - Framework for human-robot collaboration in healthcare
  Figure 17.4 - Shared-autonomy spectrum: authority vs. oversight/assurance
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/healthcare_figures'


def gen_fig1():
    """Figure 17.1: Closed-loop drug-delivery system architecture."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 12, "Architecture of a Closed-Loop Drug-Delivery System", BLACK, 2)

    # Patient
    c.rect(40, 190, 190, 280, DARK_BLUE, PALE_BLUE)
    c.text_c(115, 220, "PATIENT", BLACK, 1)
    c.text_c(115, 240, "Physiological", BLACK, 1)
    c.text_c(115, 254, "state", BLACK, 1)

    # Sensor
    c.rect(250, 60, 400, 140, MED_BLUE, LIGHT_BLUE)
    c.text_c(325, 78, "SENSOR", BLACK, 1)
    c.text_c(325, 96, "Continuous", BLACK, 1)
    c.text_c(325, 110, "monitoring", BLACK, 1)
    c.text_c(325, 124, "(e.g. glucose)", GRAY, 1)

    # Controller
    c.rect(300, 190, 480, 280, DARK_GREEN, LIGHT_GREEN)
    c.text_c(390, 210, "CONTROL", BLACK, 1)
    c.text_c(390, 228, "ALGORITHM", BLACK, 1)
    c.text_c(390, 248, "Estimate ->", BLACK, 1)
    c.text_c(390, 262, "titrate dose", GRAY, 1)

    # Safety supervisor (wrapping / above controller)
    c.rect(300, 330, 480, 410, RED, LIGHT_RED)
    c.text_c(390, 348, "SAFETY SUPERVISOR", BLACK, 1)
    c.text_c(390, 366, "Hard limits, fault", BLACK, 1)
    c.text_c(390, 380, "detection, handback", BLACK, 1)
    c.text_c(390, 394, "to clinician", GRAY, 1)

    # Actuator / pump
    c.rect(590, 190, 740, 280, ORANGE, LIGHT_ORANGE)
    c.text_c(665, 220, "ACTUATOR", BLACK, 1)
    c.text_c(665, 240, "Infusion pump", BLACK, 1)
    c.text_c(665, 254, "delivers drug", GRAY, 1)

    # Clinician oversight
    c.rect(540, 60, 740, 140, PURPLE, LIGHT_PURPLE)
    c.text_c(640, 82, "CLINICIAN", BLACK, 1)
    c.text_c(640, 100, "Sets limits,", BLACK, 1)
    c.text_c(640, 114, "supervises,", BLACK, 1)
    c.text_c(640, 128, "can override", GRAY, 1)

    # Arrows: patient -> sensor
    c.arrow(115, 190, 260, 140, MED_BLUE, 3, 10)
    c.text(150, 158, "measure", MED_BLUE, 1)
    # sensor -> controller
    c.arrow(325, 140, 360, 190, GRAY, 3, 10)
    c.text(330, 162, "signal", GRAY, 1)
    # controller -> actuator
    c.arrow(480, 235, 590, 235, DARK_GREEN, 3, 10)
    c.text(505, 218, "command", DARK_GREEN, 1)
    # actuator -> patient (feedback loop, bottom)
    c.line(665, 280, 665, 440, ORANGE, 2)
    c.line(665, 440, 115, 440, ORANGE, 2)
    c.arrow(115, 440, 115, 280, ORANGE, 2, 10)
    c.text(360, 448, "drug effect (closed loop)", ORANGE, 1)
    # safety supervisor constrains controller
    c.arrow(390, 330, 390, 282, RED, 3, 10)
    c.text(398, 300, "constrains", RED, 1)
    # clinician oversees supervisor & controller
    c.arrow(640, 140, 470, 205, PURPLE, 2, 9)

    c.text(40, 458, "Figure 17.1: Closed-loop drug delivery - an optimizing controller wrapped by a conservative safety supervisor", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_17_1_Closed_Loop_Drug_Delivery.png'))
    print("  Figure_17_1_Closed_Loop_Drug_Delivery.png done")


def gen_fig2():
    """Figure 17.2: Layered control architecture of an AI-assisted surgical system."""
    c = PNGCanvas(780, 470)
    c.text_c(390, 12, "Layered Control Architecture of an AI-Assisted Surgical System", BLACK, 2)

    layers = [
        ("SURGEON (in the loop)", "Intent, judgment, supervision, override authority", PURPLE, LIGHT_PURPLE),
        ("SHARED CONTROL LAYER", "Virtual fixtures, motion scaling, cooperative steadying", DARK_GREEN, LIGHT_GREEN),
        ("PLANNING LAYER", "Task models, trajectory generation, phase recognition", MED_BLUE, LIGHT_BLUE),
        ("PERCEPTION LAYER", "Vision, force/tactile sensing, image registration", ORANGE, LIGHT_ORANGE),
        ("ROBOT / PATIENT", "Instruments acting on deformable tissue", DARK_BLUE, PALE_BLUE),
    ]

    lx1, lx2 = 90, 560
    top = 55
    lh = 56
    gap = 12
    ys = []
    for i, (title, sub, col, fill) in enumerate(layers):
        y1 = top + i * (lh + gap)
        y2 = y1 + lh
        ys.append((y1, y2))
        c.rect(lx1, y1, lx2, y2, col, fill)
        c.text_c((lx1 + lx2) // 2, y1 + 16, title, BLACK, 1)
        c.text_c((lx1 + lx2) // 2, y1 + 34, sub, GRAY, 1)
        if i < len(layers) - 1:
            midx = (lx1 + lx2) // 2
            c.arrow(midx - 60, y2 + gap, midx - 60, y2 + 2, GRAY, 2, 7)
            c.arrow(midx + 60, y2 + 2, midx + 60, y2 + gap, GRAY, 2, 7)

    # Safety layer spanning the right side (cross-cutting)
    c.rect(590, ys[0][0], 740, ys[4][1], RED, LIGHT_RED)
    c.text_c(665, (ys[0][0] + ys[4][1]) // 2 - 30, "SAFETY", BLACK, 1)
    c.text_c(665, (ys[0][0] + ys[4][1]) // 2 - 12, "LAYER", BLACK, 1)
    c.text_c(665, (ys[0][0] + ys[4][1]) // 2 + 10, "Bounds all", BLACK, 1)
    c.text_c(665, (ys[0][0] + ys[4][1]) // 2 + 24, "learned", BLACK, 1)
    c.text_c(665, (ys[0][0] + ys[4][1]) // 2 + 38, "behavior", BLACK, 1)
    for (y1, y2) in ys:
        c.arrow(590, (y1 + y2) // 2, lx2 + 2, (y1 + y2) // 2, RED, 2, 8)

    c.text(20, 445, "up = feedback / percepts   down = commands", GRAY, 1)
    c.text(40, 460, "Figure 17.2: Learning-based components operate within a structure that constrains their authority", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_17_2_Surgical_Control_Architecture.png'))
    print("  Figure_17_2_Surgical_Control_Architecture.png done")


def gen_fig3():
    """Figure 17.3: Human-robot collaboration framework in healthcare."""
    c = PNGCanvas(780, 460)
    c.text_c(390, 12, "Framework for Human-Robot Collaboration in Healthcare", BLACK, 2)

    # Clinician box (left)
    c.rect(50, 120, 230, 320, PURPLE, LIGHT_PURPLE)
    c.text_c(140, 140, "CLINICIAN", BLACK, 1)
    c.text_c(140, 162, "Goals & values", BLACK, 1)
    c.text_c(140, 180, "Judgment", BLACK, 1)
    c.text_c(140, 198, "Accountability", BLACK, 1)
    c.text_c(140, 216, "Override", BLACK, 1)

    # Robot box (right)
    c.rect(550, 120, 730, 320, DARK_GREEN, LIGHT_GREEN)
    c.text_c(640, 140, "ROBOT", BLACK, 1)
    c.text_c(640, 162, "Perception", BLACK, 1)
    c.text_c(640, 180, "Execution", BLACK, 1)
    c.text_c(640, 198, "Precision", BLACK, 1)
    c.text_c(640, 216, "Endurance", BLACK, 1)

    # Central shared ground
    c.rect(290, 90, 490, 350, MED_BLUE, PALE_BLUE)
    c.text_c(390, 104, "SHARED GROUND", BLACK, 1)

    c.rect(310, 130, 470, 175, GOLD, LIGHT_GOLD)
    c.text_c(390, 145, "Shared situational", BLACK, 1)
    c.text_c(390, 160, "awareness", BLACK, 1)

    c.rect(310, 195, 470, 240, ORANGE, LIGHT_ORANGE)
    c.text_c(390, 210, "Intent", BLACK, 1)
    c.text_c(390, 225, "communication", BLACK, 1)

    c.rect(310, 260, 470, 320, RED, LIGHT_RED)
    c.text_c(390, 276, "Control", BLACK, 1)
    c.text_c(390, 291, "arbitration", BLACK, 1)
    c.text_c(390, 307, "(who acts when)", GRAY, 1)

    # Bidirectional arrows clinician <-> shared
    c.arrow(230, 180, 288, 152, PURPLE, 3, 9)
    c.arrow(288, 218, 230, 245, GRAY, 2, 8)
    # shared <-> robot
    c.arrow(492, 152, 550, 180, DARK_GREEN, 3, 9)
    c.arrow(550, 245, 492, 218, GRAY, 2, 8)

    c.text_c(390, 375, "Bidirectional exchange builds common ground for coordinated action", GRAY, 1)
    c.text(40, 448, "Figure 17.3: Effective collaboration depends on shared awareness, intent communication, and arbitration", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_17_3_Human_Robot_Collaboration.png'))
    print("  Figure_17_3_Human_Robot_Collaboration.png done")


def gen_fig4():
    """Figure 17.4: Shared-autonomy spectrum - authority vs. oversight/assurance."""
    c = PNGCanvas(800, 450)
    c.text_c(400, 12, "The Shared-Autonomy Spectrum in Healthcare", BLACK, 2)

    stages = [
        ("Teleoperation", "Human acts", DARK_BLUE, PALE_BLUE),
        ("Assistance", "Guided/scaled", MED_BLUE, LIGHT_BLUE),
        ("Shared control", "Negotiated", DARK_GREEN, LIGHT_GREEN),
        ("Supervised\nautonomy", "Robot acts,\nhuman watches", ORANGE, LIGHT_ORANGE),
        ("High autonomy", "Rare handback", RED, LIGHT_RED),
    ]

    bw, bh = 130, 80
    top = 70
    gap = 18
    xs = []
    for i, (l1, l2, col, fill) in enumerate(stages):
        bx = 30 + i * (bw + gap)
        xs.append(bx)
        c.rect(bx, top, bx + bw, top + bh, col, fill)
        parts = l1.split("\n")
        for k, p in enumerate(parts):
            c.text_c(bx + bw // 2, top + 14 + k * 14, p, BLACK, 1)
        y2 = top + 14 + len(parts) * 14 + 4
        for k, p in enumerate(l2.split("\n")):
            c.text_c(bx + bw // 2, y2 + k * 12, p, GRAY, 1)

    # Machine authority arrow (increasing left->right)
    ay = top + bh + 40
    c.arrow(30, ay, 770, ay, DARK_GREEN, 3, 12)
    c.text(300, ay - 18, "Increasing machine authority", DARK_GREEN, 1)

    # Human oversight role (transforms, not disappears)
    oy = ay + 55
    roles = ["Operator", "Director", "Partner", "Supervisor", "Guarantor"]
    c.text(30, oy - 20, "Human role:", BLACK, 1)
    for i, r in enumerate(roles):
        bx = 30 + i * (bw + gap)
        c.text_c(bx + bw // 2, oy, r, PURPLE, 1)

    # Assurance burden arrow (rising)
    by = oy + 55
    c.arrow(30, by, 770, by - 40, RED, 3, 12)
    c.text(300, by - 10, "Rising safety-assurance burden", RED, 1)

    c.text(40, 438, "Figure 17.4: Greater machine authority transforms rather than removes the human role and raises assurance demands", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_17_4_Shared_Autonomy_Spectrum.png'))
    print("  Figure_17_4_Shared_Autonomy_Spectrum.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 17 healthcare robotics figures...")
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
