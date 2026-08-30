#!/usr/bin/env python3
"""
Generate 4 scientific figure images (PNG) for Chapter 16
"Wearable, Implantable, and Intelligent Therapeutic Systems".

Reuses the pure-standard-library PNGCanvas from generate_figures.py so no
third-party imaging libraries are required.
"""

import os
import math
import importlib.util

# ─── Import PNGCanvas and colors from the existing figure module ───
_SPEC = importlib.util.spec_from_file_location(
    "genfig", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "generate_figures.py"))
_genfig = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_genfig)

PNGCanvas = _genfig.PNGCanvas
DARK_BLUE = _genfig.DARK_BLUE
MED_BLUE = _genfig.MED_BLUE
LIGHT_BLUE = _genfig.LIGHT_BLUE
PALE_BLUE = _genfig.PALE_BLUE
DARK_GREEN = _genfig.DARK_GREEN
MED_GREEN = _genfig.MED_GREEN
LIGHT_GREEN = _genfig.LIGHT_GREEN
ORANGE = _genfig.ORANGE
LIGHT_ORANGE = _genfig.LIGHT_ORANGE
RED = _genfig.RED
LIGHT_RED = _genfig.LIGHT_RED
PURPLE = _genfig.PURPLE
LIGHT_PURPLE = _genfig.LIGHT_PURPLE
GOLD = _genfig.GOLD
LIGHT_GOLD = _genfig.LIGHT_GOLD
GRAY = _genfig.GRAY
LIGHT_GRAY = _genfig.LIGHT_GRAY
BLACK = _genfig.BLACK
WHITE = _genfig.WHITE

OUTPUT_DIR = '/projects/sandbox/AMMAN/wearable_figures'


def gen_fig1():
    """Figure 16.1: Wearable data pipeline from transduction to decision support."""
    c = PNGCanvas(760, 430)
    c.text_c(380, 10, "Wearable Data Pipeline: Sensor to Decision Support", BLACK, 2)

    stages = [
        ("Transduction", 30, DARK_BLUE, PALE_BLUE, ["PPG / ECG", "Motion", "Biochem"]),
        ("Preprocessing", 175, MED_BLUE, LIGHT_BLUE, ["Filtering", "Artifact", "removal"]),
        ("Feature Extract", 320, DARK_GREEN, LIGHT_GREEN, ["Time/Freq", "Fusion"]),
        ("Inference", 465, ORANGE, LIGHT_ORANGE, ["ML / DL", "Uncertainty"]),
        ("Decision Support", 610, RED, LIGHT_RED, ["Alerts", "Trends", "Clinician"]),
    ]
    bw, bh = 125, 90
    by = 90
    centers = []
    for label, bx, col, fill, items in stages:
        c.rect(bx, by, bx + bw, by + bh, col, fill)
        c.text_c(bx + bw // 2, by + 8, label, BLACK, 1)
        for k, it in enumerate(items):
            c.text_c(bx + bw // 2, by + 30 + k * 16, it, GRAY, 1)
        centers.append((bx + bw, by + bh // 2, bx, by))
    # Arrows between stages
    for i in range(len(stages) - 1):
        x1 = centers[i][0]
        y = centers[i][1]
        x2 = centers[i + 1][2]
        c.arrow(x1 + 2, y, x2 - 2, y, GRAY, 2, 7)

    # Edge vs cloud annotation band
    c.rect(30, 210, 460, 245, MED_GREEN, (235, 250, 235))
    c.text_c(245, 220, "On-device / Edge Processing", DARK_GREEN, 1)
    c.rect(465, 210, 735, 245, MED_BLUE, (235, 240, 252))
    c.text_c(600, 220, "Gateway / Cloud Analytics", DARK_BLUE, 1)

    # Feedback (personalization) loop
    c.line(672, 180, 672, 275, PURPLE, 2)
    c.line(672, 275, 92, 275, PURPLE, 2)
    c.arrow(92, 275, 92, 182, PURPLE, 2, 7)
    c.text_c(380, 285, "Personalization / model update feedback", PURPLE, 1)

    # Example waveform panel
    c.rect(30, 315, 735, 405, LIGHT_GRAY, (250, 250, 250))
    c.text(40, 322, "Raw signal (noisy) vs cleaned:", BLACK, 1)
    for x in range(60, 400):
        t = (x - 60) / 30.0
        y = int(370 + 18 * math.sin(t) + 6 * math.sin(t * 7))
        c.pixel(x, y, RED)
    for x in range(410, 725):
        t = (x - 410) / 30.0
        y = int(370 + 18 * math.sin(t))
        c.pixel(x, y, DARK_GREEN)
        c.pixel(x, y + 1, DARK_GREEN)
    c.text(150, 388, "noisy PPG", RED, 1)
    c.text(520, 388, "filtered", DARK_GREEN, 1)

    c.text(30, 415, "Figure 16.1: Canonical wearable pipeline from transduction to decision support", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_16_1_Wearable_Pipeline.png'))
    print("  Figure_16_1 done")


def gen_fig2():
    """Figure 16.2: Smart drug-delivery architectures."""
    c = PNGCanvas(760, 430)
    c.text_c(380, 10, "Smart Drug-Delivery Architectures", BLACK, 2)

    # (a) Passive matrix diffusion
    c.text_c(140, 45, "(a) Passive Matrix", BLACK, 1)
    c.rect(50, 65, 230, 210, DARK_GREEN, LIGHT_GREEN)
    import random
    random.seed(1)
    for _ in range(60):
        px = random.randint(58, 222)
        py = random.randint(73, 202)
        c.circle(px, py, 2, DARK_GREEN, DARK_GREEN)
    for k in range(5):
        c.arrow(232, 90 + k * 25, 262, 90 + k * 25, ORANGE, 2, 6)
    c.text_c(140, 218, "diffusion-controlled release", GRAY, 1)

    # (b) Active micropump reservoir
    c.text_c(390, 45, "(b) Active Micropump Reservoirs", BLACK, 1)
    c.rect(285, 65, 495, 210, MED_BLUE, LIGHT_BLUE)
    for row in range(2):
        for col in range(4):
            rx = 300 + col * 45
            ry = 80 + row * 55
            filled = (row * 4 + col) % 3 != 0
            c.rect(rx, ry, rx + 32, ry + 38, DARK_BLUE,
                   LIGHT_ORANGE if filled else WHITE)
    c.rect(300, 175, 480, 200, GOLD, LIGHT_GOLD)
    c.text_c(390, 182, "Controller + micropump", BLACK, 1)
    c.text_c(390, 218, "dose-on-command reservoirs", GRAY, 1)

    # (c) Stimuli-responsive nanocarriers
    c.text_c(640, 45, "(c) Responsive Nanocarriers", BLACK, 1)
    c.rect(545, 65, 730, 210, PURPLE, LIGHT_PURPLE)
    for i in range(4):
        cx = 575 + i * 40
        c.circle(cx, 110, 14, PURPLE, WHITE)
        c.circle(cx, 110, 5, PURPLE, PURPLE)
    c.text_c(640, 135, "stable in circulation", GRAY, 1)
    c.arrow(637, 145, 637, 165, RED, 2, 6)
    c.text_c(640, 170, "trigger: pH / enzyme / light", RED, 1)
    for i in range(4):
        cx = 575 + i * 40
        for a in range(6):
            ang = math.radians(60 * a)
            c.pixel(int(cx + 12 * math.cos(ang)), int(195 + 12 * math.sin(ang)), RED)
        c.circle(cx, 195, 3, RED, RED)
    c.text_c(640, 218, "payload released at target", GRAY, 1)

    # Bottom: release-profile comparison
    c.rect(50, 250, 730, 405, LIGHT_GRAY, (250, 250, 250))
    c.text(60, 258, "Plasma concentration vs time:", BLACK, 1)
    c.vline(90, 275, 390, BLACK)
    c.hline(90, 710, 390, BLACK)
    c.text(60, 275, "C", BLACK, 1)
    c.text(660, 393, "time", BLACK, 1)
    # therapeutic window band
    c.fill_rect(91, 300, 709, 340, (225, 240, 225))
    c.text(600, 305, "therapeutic window", DARK_GREEN, 1)
    # conventional (spiky)
    for x in range(95, 705):
        t = (x - 95) / 55.0
        y = int(365 - 120 * abs(math.sin(t)) * math.exp(-((t % 3.14) - 1.5) ** 2))
        c.pixel(x, y, RED)
    # controlled (steady in window)
    for x in range(95, 705):
        t = (x - 95) / 610.0
        y = int(320 - 5 * math.sin(t * 6))
        c.pixel(x, y, MED_BLUE)
        c.pixel(x, y + 1, MED_BLUE)
    c.hline(560, 590, 360, RED); c.text(595, 357, "conventional", BLACK, 1)
    c.hline(560, 590, 375, MED_BLUE); c.text(595, 372, "controlled", BLACK, 1)

    c.text(30, 415, "Figure 16.2: Passive, active, and responsive smart drug-delivery architectures", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_16_2_Drug_Delivery.png'))
    print("  Figure_16_2 done")


def gen_fig3():
    """Figure 16.3: Generic closed-loop therapeutic control architecture."""
    c = PNGCanvas(760, 430)
    c.text_c(380, 10, "Closed-Loop Therapeutic Control Architecture", BLACK, 2)

    # Patient / body
    c.rect(300, 50, 460, 105, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 65, "PATIENT / BODY", BLACK, 2)
    c.text_c(380, 88, "physiological state", GRAY, 1)

    # Sensor
    c.rect(560, 130, 710, 185, MED_GREEN, LIGHT_GREEN)
    c.text_c(635, 143, "SENSOR", BLACK, 1)
    c.text_c(635, 162, "wearable / implant", GRAY, 1)

    # Estimator
    c.rect(560, 220, 710, 275, MED_BLUE, LIGHT_BLUE)
    c.text_c(635, 233, "STATE ESTIMATION", BLACK, 1)
    c.text_c(635, 252, "filter / calibration", GRAY, 1)

    # Controller
    c.rect(300, 300, 460, 380, ORANGE, LIGHT_ORANGE)
    c.text_c(380, 315, "CONTROLLER", BLACK, 2)
    c.text_c(380, 340, "PID / MPC / RL", BLACK, 1)
    c.text_c(380, 358, "learned policy", GRAY, 1)

    # Safety supervisor
    c.rect(300, 220, 460, 275, RED, LIGHT_RED)
    c.text_c(380, 233, "SAFETY SUPERVISOR", BLACK, 1)
    c.text_c(380, 252, "constraint enforcement", GRAY, 1)

    # Actuator
    c.rect(50, 130, 200, 185, PURPLE, LIGHT_PURPLE)
    c.text_c(125, 143, "ACTUATOR", BLACK, 1)
    c.text_c(125, 162, "pump / stimulator", GRAY, 1)

    # Arrows forming the loop
    c.arrow(460, 78, 635, 128, MED_GREEN, 2, 7); c.text(475, 92, "measure", MED_GREEN, 1)
    c.arrow(635, 185, 635, 218, GRAY, 2, 7)
    c.arrow(635, 275, 460, 320, MED_BLUE, 2, 7); c.text(490, 300, "estimate", MED_BLUE, 1)
    c.arrow(380, 300, 380, 277, RED, 2, 7)
    c.arrow(300, 340, 125, 187, ORANGE, 2, 7); c.text(150, 300, "command", ORANGE, 1)
    c.arrow(125, 130, 300, 80, PURPLE, 2, 7); c.text(150, 95, "deliver therapy", PURPLE, 1)

    # Reference / target
    c.rect(40, 300, 200, 355, GOLD, LIGHT_GOLD)
    c.text_c(120, 315, "TARGET / SETPOINT", BLACK, 1)
    c.text_c(120, 335, "clinical goal", GRAY, 1)
    c.arrow(200, 327, 300, 340, GOLD, 2, 7)

    c.text(30, 415, "Figure 16.3: Generic closed-loop architecture with safety supervision", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_16_3_Closed_Loop.png'))
    print("  Figure_16_3 done")


def gen_fig4():
    """Figure 16.4: Convergence of the three pillars."""
    c = PNGCanvas(760, 440)
    c.text_c(380, 10, "Convergence into Closed-Loop Therapeutic Systems", BLACK, 2)

    # Three pillar circles (Venn-like)
    c.circle(250, 190, 130, MED_BLUE, (232, 240, 252))
    c.circle(510, 190, 130, MED_GREEN, (234, 250, 234))
    c.circle(380, 300, 130, ORANGE, (255, 244, 232))

    c.text_c(200, 120, "SENSING", DARK_BLUE, 2)
    c.text_c(200, 145, "wearable +", GRAY, 1)
    c.text_c(200, 160, "implantable", GRAY, 1)

    c.text_c(560, 120, "ACTUATION", DARK_GREEN, 2)
    c.text_c(560, 145, "controllable", GRAY, 1)
    c.text_c(560, 160, "delivery", GRAY, 1)

    c.text_c(380, 355, "COMPUTATION", ORANGE, 2)
    c.text_c(380, 380, "edge AI + control", GRAY, 1)

    # Center intersection
    c.text_c(380, 210, "CLOSED-LOOP", BLACK, 1)
    c.text_c(380, 228, "THERAPY", BLACK, 1)

    # Enabling-technology callouts
    c.rect(20, 260, 190, 340, MED_BLUE, LIGHT_BLUE)
    c.text_c(105, 268, "Enabling: Sensing", BLACK, 1)
    c.text(28, 285, "- flexible", DARK_BLUE, 1)
    c.text(28, 300, "  bioelectronics", DARK_BLUE, 1)
    c.text(28, 315, "- biocompatible", DARK_BLUE, 1)
    c.text(28, 328, "  implants", DARK_BLUE, 1)

    c.rect(570, 260, 745, 340, MED_GREEN, LIGHT_GREEN)
    c.text_c(657, 268, "Enabling: Actuation", BLACK, 1)
    c.text(578, 285, "- micropumps", DARK_GREEN, 1)
    c.text(578, 300, "- stimulators", DARK_GREEN, 1)
    c.text(578, 315, "- responsive", DARK_GREEN, 1)
    c.text(578, 328, "  materials", DARK_GREEN, 1)

    c.rect(285, 400, 480, 432, ORANGE, LIGHT_ORANGE)
    c.text_c(382, 408, "Enabling: edge intelligence,", BLACK, 1)
    c.text_c(382, 421, "safety supervision, personalization", BLACK, 1)

    c.text(30, 428, "Figure 16.4: Convergence of sensing, actuation, and computation", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_16_4_Convergence.png'))
    print("  Figure_16_4 done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Chapter 16 figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print(f"\nAll 4 figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz/1024:.1f} KB")


if __name__ == '__main__':
    main()
