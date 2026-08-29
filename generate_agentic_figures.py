#!/usr/bin/env python3
"""
Generate 3 figure images (PNG) for the chapter
"Agentic AI and Autonomous Systems".

Reuses the pure-standard-library PNGCanvas toolkit from generate_figures.py
so it runs without any third-party dependencies in the sandbox.

Figures:
  Figure 1 - Evolutionary trajectory: rule-based -> ML -> generative -> agentic
  Figure 2 - Reference architecture of an autonomous AI agent
  Figure 3 - Layered interoperability framework for heterogeneous multi-agent
             collaboration
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

OUTPUT_DIR = '/projects/sandbox/AMMAN/agentic_figures'


def _wrapped_lines(canvas, cx, y, lines, color, scale=1, line_h=12):
    """Draw a list of centered text lines starting at y."""
    for i, ln in enumerate(lines):
        canvas.text_c(cx, y + i * line_h, ln, color, scale)


def gen_fig1():
    """Figure 1: Evolutionary trajectory of AI toward agentic systems."""
    c = PNGCanvas(760, 430)
    c.text_c(380, 10, "Evolution from Rule-Based Systems to Agentic AI", BLACK, 2)

    stages = [
        ("Rule-Based", "Expert Systems", "1970s-1980s", DARK_BLUE, PALE_BLUE,
         ["Hand-coded", "if-then rules", "Narrow, brittle"]),
        ("Machine", "Learning", "1990s-2010s", MED_BLUE, LIGHT_BLUE,
         ["Learned", "patterns", "Reactive"]),
        ("Generative", "AI", "2018-2022", MED_GREEN, LIGHT_GREEN,
         ["Foundation", "models", "Single-turn"]),
        ("Agentic", "AI", "2023-present", ORANGE, LIGHT_ORANGE,
         ["Goal-directed", "Plans & acts", "Autonomous"]),
    ]

    bw, bh = 150, 90
    top = 90
    gap = 40
    xs = []
    for i, (l1, l2, era, col, fill, bullets) in enumerate(stages):
        bx = 30 + i * (bw + gap)
        xs.append((bx, bx + bw))
        c.rect(bx, top, bx + bw, top + bh, col, fill)
        c.text_c(bx + bw // 2, top + 12, l1, BLACK, 1)
        c.text_c(bx + bw // 2, top + 26, l2, BLACK, 1)
        c.text_c(bx + bw // 2, top + 44, era, GRAY, 1)
        for j, b in enumerate(bullets):
            c.text_c(bx + bw // 2, top + 58 + j * 11, b, BLACK, 1)
        if i > 0:
            px = xs[i - 1][1]
            c.arrow(px + 4, top + bh // 2, bx - 4, top + bh // 2, GRAY, 3, 10)

    # Rising-autonomy indicator arrow spanning the bottom
    ay = top + bh + 70
    c.arrow(40, ay, 720, ay - 55, DARK_GREEN, 3, 12)
    c.text(300, ay - 20, "Increasing autonomy and scope", DARK_GREEN, 1)

    # Capability annotations under each stage
    caps = ["Reasoning", "Perception", "+ Generation", "+ Planning & Action"]
    for i, cap in enumerate(caps):
        bx = 30 + i * (bw + gap)
        c.text_c(bx + bw // 2, top + bh + 14, cap, MED_BLUE, 1)

    c.text(40, 410, "Figure 1: Evolutionary trajectory of AI toward autonomous agentic systems", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_1_Evolution_of_Agentic_AI.png'))
    print("  Figure_1_Evolution_of_Agentic_AI.png done")


def gen_fig2():
    """Figure 2: Reference architecture of an autonomous AI agent."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Reference Architecture of an Autonomous AI Agent", BLACK, 2)

    # Central reasoning core
    core_x1, core_y1, core_x2, core_y2 = 300, 150, 470, 250
    c.rect(core_x1, core_y1, core_x2, core_y2, DARK_GREEN, LIGHT_GREEN)
    c.text_c(385, 170, "REASONING CORE", BLACK, 1)
    c.text_c(385, 190, "LLM Planner", BLACK, 1)
    c.text_c(385, 210, "Reason -> Plan", GRAY, 1)
    c.text_c(385, 226, "-> Act -> Observe", GRAY, 1)

    # Perception (left, in)
    c.rect(40, 160, 190, 230, MED_BLUE, LIGHT_BLUE)
    c.text_c(115, 180, "PERCEPTION", BLACK, 1)
    c.text_c(115, 198, "Sensors,", BLACK, 1)
    c.text_c(115, 212, "data, inputs", BLACK, 1)
    c.arrow(190, 195, core_x1 - 4, 185, MED_BLUE, 3, 10)
    c.text(210, 165, "percepts", MED_BLUE, 1)

    # Memory (top)
    c.rect(300, 55, 470, 120, PURPLE, LIGHT_PURPLE)
    c.text_c(385, 68, "MEMORY", BLACK, 1)
    c.text_c(385, 84, "Short-term / Working", BLACK, 1)
    c.text_c(385, 98, "Long-term + Retrieval", BLACK, 1)
    c.arrow(385, 120, 385, core_y1 - 4, PURPLE, 3, 10)
    c.arrow(360, core_y1 - 4, 360, 120, PURPLE, 2, 8)
    c.text(475, 88, "read / write", PURPLE, 1)

    # Tools & APIs (right)
    c.rect(580, 150, 730, 250, ORANGE, LIGHT_ORANGE)
    c.text_c(655, 168, "TOOLS & APIs", BLACK, 1)
    c.text_c(655, 186, "Code, search,", BLACK, 1)
    c.text_c(655, 200, "databases,", BLACK, 1)
    c.text_c(655, 214, "actuators", BLACK, 1)
    c.arrow(core_x2 + 4, 190, 580 - 4, 190, ORANGE, 3, 10)
    c.text(490, 172, "invoke", ORANGE, 1)
    c.arrow(580 - 4, 215, core_x2 + 4, 215, GRAY, 2, 8)
    c.text(490, 222, "results", GRAY, 1)

    # Action (bottom)
    c.rect(300, 300, 470, 370, RED, LIGHT_RED)
    c.text_c(385, 318, "ACTION", BLACK, 1)
    c.text_c(385, 336, "Effect change in", BLACK, 1)
    c.text_c(385, 350, "the environment", BLACK, 1)
    c.arrow(385, core_y2 + 4, 385, 300 - 4, RED, 3, 10)
    c.text(395, 270, "act", RED, 1)

    # Environment enclosure
    c.rect(30, 400, 730, 440, DARK_BLUE, PALE_BLUE)
    c.text_c(380, 415, "ENVIRONMENT (digital and/or physical)", BLACK, 1)
    # feedback loop from action & environment back to perception
    c.line(300, 335, 115, 335, GRAY, 1)
    c.line(115, 335, 115, 230, GRAY, 1)
    c.arrow(115, 230, 115, 232, GRAY, 1, 6)
    c.text(150, 322, "feedback loop", GRAY, 1)

    c.text(40, 458, "Figure 2: Core components - perception, memory, reasoning, tools, and action", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_2_Agent_Architecture.png'))
    print("  Figure_2_Agent_Architecture.png done")


def gen_fig3():
    """Figure 3: Layered interoperability framework for multi-agent systems."""
    c = PNGCanvas(760, 470)
    c.text_c(380, 10, "Layered Interoperability for Heterogeneous Multi-Agent Systems", BLACK, 2)

    layers = [
        ("Coordination / Policy Layer", "Norms, negotiation, workflow orchestration", PURPLE, LIGHT_PURPLE),
        ("Semantic Layer", "Shared ontologies, meaning, intent", DARK_GREEN, LIGHT_GREEN),
        ("Message Format Layer", "Communication acts, structured schemas", ORANGE, LIGHT_ORANGE),
        ("Transport Layer", "Networks, protocols, routing", MED_BLUE, LIGHT_BLUE),
    ]

    lx1, lx2 = 120, 640
    top = 55
    lh = 58
    gap = 12
    for i, (title, sub, col, fill) in enumerate(layers):
        y1 = top + i * (lh + gap)
        y2 = y1 + lh
        c.rect(lx1, y1, lx2, y2, col, fill)
        c.text_c((lx1 + lx2) // 2, y1 + 16, title, BLACK, 1)
        c.text_c((lx1 + lx2) // 2, y1 + 34, sub, GRAY, 1)
        if i < len(layers) - 1:
            midx = (lx1 + lx2) // 2
            c.arrow(midx, y2 + gap, midx, y2 + 2, GRAY, 2, 7)
            c.arrow(midx + 40, y2 + 2, midx + 40, y2 + gap, GRAY, 2, 7)

    # Two heterogeneous agents on either side communicating through the stack
    c.rect(20, 150, 105, 250, DARK_BLUE, PALE_BLUE)
    _wrapped_lines(c, 62, 175, ["Agent A", "Org 1", "Model X"], BLACK, 1, 16)
    c.rect(655, 150, 740, 250, RED, LIGHT_RED)
    _wrapped_lines(c, 697, 175, ["Agent B", "Org 2", "Model Y"], BLACK, 1, 16)

    # connective arrows into the stack
    c.arrow(105, 200, lx1 - 4, 200, GRAY, 2, 8)
    c.arrow(lx2 + 4, 200, 655 - 4, 200, GRAY, 2, 8)

    # Note box
    c.rect(120, 320, 640, 390, GOLD, LIGHT_GOLD)
    c.text_c(380, 335, "Each layer must align for correct collaboration", BLACK, 1)
    c.text_c(380, 355, "Misaligned semantics -> messages valid but misunderstood", BLACK, 1)
    c.text_c(380, 372, "-> coordination failure", GRAY, 1)

    c.text(40, 458, "Figure 3: Layered interoperability framework for heterogeneous multi-agent collaboration", BLACK, 1)
    c.save(os.path.join(OUTPUT_DIR, 'Figure_3_Interoperability_Framework.png'))
    print("  Figure_3_Interoperability_Framework.png done")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating agentic AI chapter figures...")
    gen_fig1()
    gen_fig2()
    gen_fig3()
    print(f"\nAll figures saved to {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}: {sz / 1024:.1f} KB")


if __name__ == '__main__':
    main()
