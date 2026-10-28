#!/usr/bin/env python3
"""
Generate 4 figure images (PNG, 300 dpi) for the chapter

    "Explainable and Federated Artificial Intelligence for Secure Clinical
     Decision Support in Next-Generation Healthcare Systems"

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py so
it runs without any third-party dependencies in the sandbox. PNGCanvas is
subclassed here to embed a pHYs chunk declaring 300 dpi, and all figures are
rendered at high pixel resolution so that the physical print size is ~6 inches
wide at 300 dpi.

Figures:
  Figure 1 - Evolution of AI in clinical decision support
  Figure 2 - Federated learning architecture for privacy-preserving healthcare
  Figure 3 - Taxonomy of explainable AI techniques for clinical predictions
  Figure 4 - Integrated explainable-federated AI (XFL) framework for
             trustworthy clinical decision support
"""

import os
import struct
import zlib

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

OUTPUT_DIR = '/projects/sandbox/AMMAN/xfl_figures'
DPI = 300
TEAL = (38, 132, 132)
LIGHT_TEAL = (196, 228, 228)


class HiResCanvas(PNGCanvas):
    """PNGCanvas that writes a pHYs chunk so the PNG declares 300 dpi."""

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            offset = y * self.w * 3
            raw.extend(self.data[offset:offset + self.w * 3])
        compressed = zlib.compress(bytes(raw), 9)

        def chunk(ctype, data):
            c = ctype + data
            crc = zlib.crc32(c) & 0xffffffff
            return struct.pack('>I', len(data)) + c + struct.pack('>I', crc)

        ppm = int(round(DPI / 0.0254))  # pixels per metre
        phys = struct.pack('>IIB', ppm, ppm, 1)

        with open(path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.write(chunk(b'IHDR',
                          struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0)))
            f.write(chunk(b'pHYs', phys))
            f.write(chunk(b'IDAT', compressed))
            f.write(chunk(b'IEND', b''))


def box(c, x, y, w, h, outline, fill, lines, title_scale=3, body_scale=2,
        title_color=BLACK, body_color=BLACK, thick=2):
    """Draw a rounded-ish box with a title line and optional body lines."""
    for t in range(thick):
        c.rect(x + t, y + t, x + w - t, y + h - t, outline, fill if t == 0 else None)
    cy = y + 16
    if lines:
        c.text_c(x + w // 2, cy, lines[0], title_color, title_scale)
        cy += 14 * title_scale
        for ln in lines[1:]:
            c.text_c(x + w // 2, cy, ln, body_color, body_scale)
            cy += 11 * body_scale


def gen_fig1():
    """Figure 1: Evolution of AI in clinical decision support."""
    W, H = 1800, 760
    c = HiResCanvas(W, H)
    c.text_c(W // 2, 24, "Evolution of Artificial Intelligence in Clinical Decision Support",
             BLACK, 4)

    stages = [
        (DARK_BLUE, PALE_BLUE,
         ["Rule-Based", "Expert Systems", "1970s-1990s",
          "Hand-coded rules", "e.g. MYCIN", "Transparent but", "brittle, narrow"]),
        (MED_BLUE, LIGHT_BLUE,
         ["Statistical", "Machine Learning", "1990s-2010s",
          "Regression, SVM", "Feature engineering", "Data-driven,", "limited scale"]),
        (MED_GREEN, LIGHT_GREEN,
         ["Deep Learning", "", "2012-2020",
          "CNNs / RNNs", "Imaging, EHR", "High accuracy,", "opaque black box"]),
        (ORANGE, LIGHT_ORANGE,
         ["Federated and", "Explainable AI", "2020-present",
          "Privacy-preserving", "Interpretable", "Distributed and", "trustworthy"]),
    ]

    bw, bh = 360, 300
    gap = (W - 4 * bw) // 5
    top = 110
    centers = []
    for i, (col, fill, lines) in enumerate(stages):
        bx = gap + i * (bw + gap)
        box(c, bx, top, bw, bh, col, fill, lines, title_scale=3, body_scale=2, thick=3)
        centers.append((bx, bx + bw))
        if i > 0:
            px = centers[i - 1][1]
            c.arrow(px + 6, top + bh // 2, bx - 6, top + bh // 2, GRAY, 4, 22)

    # Bottom progression arrow
    ay = top + bh + 120
    c.arrow(gap, ay, W - gap, ay, DARK_GREEN, 4, 22)
    c.text_c(W // 2, ay - 40,
             "Increasing data scale, model complexity, and the need for privacy and trust",
             DARK_GREEN, 3)

    caps = ["Interpretability", "Generalization", "Representation power",
            "Privacy + Transparency"]
    for i, cap in enumerate(caps):
        bx = gap + i * (bw + gap)
        c.text_c(bx + bw // 2, ay + 24, cap, MED_BLUE, 2)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Evolution_AI_CDS.png'))
    print("  Figure_1_Evolution_AI_CDS.png done")


def gen_fig2():
    """Figure 2: Federated learning architecture for healthcare."""
    W, H = 1800, 1120
    c = HiResCanvas(W, H)
    c.text_c(W // 2, 24, "Federated Learning Architecture for Privacy-Preserving Healthcare",
             BLACK, 4)

    # Central aggregation server (top)
    sx, sy, sw, sh = W // 2 - 300, 110, 600, 150
    box(c, sx, sy, sw, sh, DARK_BLUE, PALE_BLUE,
        ["Central Aggregation Server", "Secure model aggregation (FedAvg)",
         "Global model update and broadcast"],
        title_scale=3, body_scale=2, thick=3)

    # Secure aggregation / privacy layer
    px, py, pw, ph = W // 2 - 360, 320, 720, 110
    box(c, px, py, pw, ph, PURPLE, LIGHT_PURPLE,
        ["Secure Aggregation and Privacy Layer",
         "Differential privacy  |  Homomorphic encryption  |  SMPC"],
        title_scale=3, body_scale=2, thick=3)
    c.arrow(W // 2, sy + sh + 4, W // 2, py - 6, GRAY, 4, 20)

    # Hospital clients (bottom row)
    clients = [
        (DARK_GREEN, LIGHT_GREEN, "Hospital A"),
        (TEAL, LIGHT_TEAL, "Clinic B"),
        (ORANGE, LIGHT_ORANGE, "Hospital C"),
        (RED, LIGHT_RED, "Research Lab D"),
    ]
    cw, chh = 360, 250
    cgap = (W - 4 * cw) // 5
    ctop = 760
    for i, (col, fill, name) in enumerate(clients):
        cx = cgap + i * (cw + cgap)
        box(c, cx, ctop, cw, chh, col, fill,
            [name, "Local EHR / images", "Local model training",
             "Shares encrypted", "updates only"],
            title_scale=3, body_scale=2, thick=3)
        mid = cx + cw // 2
        # Up: encrypted updates to privacy layer
        c.arrow(mid - 30, ctop - 6, px + pw // 2 - 90 + i * 60, py + ph + 6,
                MED_GREEN, 3, 16)
        # Down: global model broadcast
        c.arrow(px + pw // 2 + 90 - i * 60 + 20, py + ph + 6, mid + 30, ctop - 6,
                MED_BLUE, 3, 16)

    # Legend
    lx, ly = cgap, ctop + chh + 30
    c.line(lx, ly, lx + 60, ly, MED_GREEN, 4)
    c.text(lx + 72, ly - 8, "Encrypted local updates (uplink)", BLACK, 2)
    c.line(lx + 760, ly, lx + 820, ly, MED_BLUE, 4)
    c.text(lx + 832, ly - 8, "Global model broadcast (downlink)", BLACK, 2)
    c.text_c(W // 2, ly + 34,
             "Raw patient data never leaves the institution", RED, 2)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Federated_Architecture.png'))
    print("  Figure_2_Federated_Architecture.png done")


def gen_fig3():
    """Figure 3: Taxonomy of explainable AI techniques for clinical predictions."""
    W, H = 1800, 980
    c = HiResCanvas(W, H)
    c.text_c(W // 2, 24, "Explainable AI Techniques for Interpretable Clinical Predictions",
             BLACK, 4)

    # Input
    box(c, W // 2 - 260, 100, 520, 110, DARK_BLUE, PALE_BLUE,
        ["Clinical Inputs", "EHR, labs, vitals, medical images, genomics"],
        title_scale=3, body_scale=2, thick=3)
    # Model
    box(c, W // 2 - 260, 260, 520, 110, MED_BLUE, LIGHT_BLUE,
        ["Predictive Model", "Risk score / diagnosis / prognosis"],
        title_scale=3, body_scale=2, thick=3)
    c.arrow(W // 2, 210 + 4, W // 2, 260 - 6, GRAY, 4, 18)

    # Two branches
    by = 470
    bw, bh = 760, 220
    # Intrinsic
    ix = 120
    box(c, ix, by, bw, bh, DARK_GREEN, LIGHT_GREEN,
        ["Intrinsic (Interpretable-by-Design)",
         "Linear / logistic models", "Decision trees, rule lists",
         "Attention mechanisms", "Generalized additive models"],
        title_scale=3, body_scale=2, thick=3)
    # Post-hoc
    hx = W - 120 - bw
    box(c, hx, by, bw, bh, ORANGE, LIGHT_ORANGE,
        ["Post-hoc (Model-Agnostic / Specific)",
         "SHAP (Shapley values)", "LIME (local surrogates)",
         "Grad-CAM saliency maps", "Counterfactual explanations"],
        title_scale=3, body_scale=2, thick=3)
    c.arrow(W // 2 - 40, 370 + 4, ix + bw // 2, by - 6, GRAY, 4, 18)
    c.arrow(W // 2 + 40, 370 + 4, hx + bw // 2, by - 6, GRAY, 4, 18)

    # Output
    oy = by + bh + 70
    box(c, W // 2 - 320, oy, 640, 120, PURPLE, LIGHT_PURPLE,
        ["Human-Interpretable Explanations",
         "Feature attributions, saliency, what-if reasoning",
         "-> Clinician trust, verification and accountability"],
        title_scale=3, body_scale=2, thick=3)
    c.arrow(ix + bw // 2, by + bh + 4, W // 2 - 120, oy - 6, GRAY, 4, 18)
    c.arrow(hx + bw // 2, by + bh + 4, W // 2 + 120, oy - 6, GRAY, 4, 18)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_XAI_Taxonomy.png'))
    print("  Figure_3_XAI_Taxonomy.png done")


def gen_fig4():
    """Figure 4: Integrated explainable-federated AI framework."""
    W, H = 1800, 1060
    c = HiResCanvas(W, H)
    c.text_c(W // 2, 24,
             "Integrated Explainable-Federated AI (XFL) Framework for Trustworthy CDS",
             BLACK, 3)

    layers = [
        (DARK_GREEN, LIGHT_GREEN, "Layer 1 - Distributed Data Sources",
         "Hospitals, clinics, wearables: local EHR and imaging on-site"),
        (MED_BLUE, LIGHT_BLUE, "Layer 2 - Federated Training",
         "Local training + privacy-preserving secure aggregation (DP / HE / SMPC)"),
        (DARK_BLUE, PALE_BLUE, "Layer 3 - Global Collaborative Model",
         "Shared model generalizing across institutions without data sharing"),
        (ORANGE, LIGHT_ORANGE, "Layer 4 - Explainability Engine",
         "SHAP / LIME / attention / counterfactuals applied to global predictions"),
        (PURPLE, LIGHT_PURPLE, "Layer 5 - Clinical Decision Support",
         "Interpretable risk scores and recommendations to clinicians"),
    ]
    lx = 280
    lw = W - 2 * lx
    lh = 130
    top = 110
    vgap = 44
    centers = []
    for i, (col, fill, title, body) in enumerate(layers):
        y = top + i * (lh + vgap)
        box(c, lx, y, lw, lh, col, fill, [title, body],
            title_scale=3, body_scale=2, thick=3)
        centers.append((y, y + lh))
        if i > 0:
            c.arrow(W // 2, centers[i - 1][1] + 4, W // 2, y - 6, GRAY, 4, 20)

    # Feedback loop on the right
    rx = lx + lw + 30
    top_y = centers[0][0] + lh // 2
    bot_y = centers[-1][0] + lh // 2
    c.line(rx, top_y, rx + 80, top_y, GOLD, 4)
    c.line(rx + 80, top_y, rx + 80, bot_y, GOLD, 4)
    c.arrow(rx + 80, bot_y, rx, bot_y, GOLD, 4, 18)
    c.text(rx + 20, (top_y + bot_y) // 2 - 40, "Clinician", GOLD, 2)
    c.text(rx + 20, (top_y + bot_y) // 2 - 16, "feedback", GOLD, 2)
    c.text(rx + 20, (top_y + bot_y) // 2 + 8, "and continual", GOLD, 2)
    c.text(rx + 20, (top_y + bot_y) // 2 + 32, "learning", GOLD, 2)

    # Governance band on the left
    gx = 40
    c.rect(gx, top, gx + 180, centers[-1][1], GRAY, LIGHT_GRAY)
    c.text_c(gx + 90, top + 30, "Governance", BLACK, 2)
    c.text_c(gx + 90, top + 60, "Ethics,", GRAY, 2)
    c.text_c(gx + 90, top + 84, "regulation,", GRAY, 2)
    c.text_c(gx + 90, top + 108, "security,", GRAY, 2)
    c.text_c(gx + 90, top + 132, "auditing", GRAY, 2)

    c.save(os.path.join(OUTPUT_DIR, 'Figure_4_XFL_Framework.png'))
    print("  Figure_4_XFL_Framework.png done")


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating XFL chapter figures (300 dpi)...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    gen_fig4()
    print("All figures written to", OUTPUT_DIR)
