#!/usr/bin/env python3
"""
Generate simple PNG figures for the Digital Transformation in Marine Biotechnology chapter.
Uses pure Python (struct + zlib) to create PNG files without external dependencies.
"""
import struct
import zlib
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chapter_figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class SimplePNG:
    """Minimal PNG writer using pure Python."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # RGBA pixels
        self.pixels = [[(255, 255, 255, 255)] * width for _ in range(height)]

    def set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color

    def fill_rect(self, x, y, w, h, color):
        for dy in range(h):
            for dx in range(w):
                self.set_pixel(x + dx, y + dy, color)

    def draw_rect(self, x, y, w, h, color, thickness=2):
        for t in range(thickness):
            for dx in range(w):
                self.set_pixel(x + dx, y + t, color)
                self.set_pixel(x + dx, y + h - 1 - t, color)
            for dy in range(h):
                self.set_pixel(x + t, y + dy, color)
                self.set_pixel(x + w - 1 - t, y + dy, color)

    def draw_rounded_rect(self, x, y, w, h, color, thickness=2):
        self.draw_rect(x, y, w, h, color, thickness)

    def fill_rounded_rect(self, x, y, w, h, color):
        self.fill_rect(x, y, w, h, color)

    def draw_line(self, x1, y1, x2, y2, color, thickness=2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            for t in range(-(thickness // 2), (thickness + 1) // 2):
                if dx >= dy:
                    self.set_pixel(x1, y1 + t, color)
                else:
                    self.set_pixel(x1 + t, y1, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_arrow(self, x1, y1, x2, y2, color, thickness=2):
        self.draw_line(x1, y1, x2, y2, color, thickness)
        # Arrowhead
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 10
        for i in range(2):
            a = angle + math.pi + (0.4 if i == 0 else -0.4)
            ax = int(x2 + arrow_len * math.cos(a))
            ay = int(y2 + arrow_len * math.sin(a))
            self.draw_line(x2, y2, ax, ay, color, thickness)

    def draw_text_block(self, x, y, w, h, text, bg_color, border_color, text_color=(0, 0, 0, 255)):
        """Draw a labeled box (text is simulated as a filled region with label indicator)."""
        self.fill_rounded_rect(x, y, w, h, bg_color)
        self.draw_rounded_rect(x, y, w, h, border_color, 2)
        # Draw a simple text indicator (horizontal lines to simulate text)
        text_y = y + h // 2 - 2
        line_w = min(w - 20, len(text) * 5)
        start_x = x + (w - line_w) // 2
        for i in range(min(3, max(1, len(text) // 10))):
            lw = line_w if i == 0 else line_w * 2 // 3
            lx = x + (w - lw) // 2
            self.draw_line(lx, text_y + i * 6, lx + lw, text_y + i * 6, text_color, 2)

    def draw_circle(self, cx, cy, r, color, thickness=2):
        import math
        for angle in range(360):
            rad = math.radians(angle)
            for t in range(thickness):
                x = int(cx + (r - t) * math.cos(rad))
                y = int(cy + (r - t) * math.sin(rad))
                self.set_pixel(x, y, color)

    def fill_circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r:
                    self.set_pixel(cx + dx, cy + dy, color)

    def save(self, filename):
        raw_data = b""
        for row in self.pixels:
            raw_data += b"\x00"  # filter byte
            for r, g, b, a in row:
                raw_data += struct.pack("BBBB", r, g, b, a)

        def make_chunk(chunk_type, data):
            chunk = chunk_type + data
            return struct.pack(">I", len(data)) + chunk + struct.pack(">I", zlib.crc32(chunk) & 0xFFFFFFFF)

        png = b"\x89PNG\r\n\x1a\n"
        png += make_chunk(b"IHDR", struct.pack(">IIBBBBB", self.width, self.height, 8, 6, 0, 0, 0))
        compressed = zlib.compress(raw_data)
        png += make_chunk(b"IDAT", compressed)
        png += make_chunk(b"IEND", b"")

        with open(filename, "wb") as f:
            f.write(png)


# Color palette
BLUE = (70, 130, 180, 255)
LIGHT_BLUE = (173, 216, 230, 255)
GREEN = (60, 179, 113, 255)
LIGHT_GREEN = (200, 240, 200, 255)
ORANGE = (255, 165, 0, 255)
LIGHT_ORANGE = (255, 228, 181, 255)
PURPLE = (128, 0, 128, 255)
LIGHT_PURPLE = (220, 200, 240, 255)
RED = (220, 60, 60, 255)
LIGHT_RED = (255, 200, 200, 255)
DARK = (40, 40, 40, 255)
GRAY = (150, 150, 150, 255)
LIGHT_GRAY = (230, 230, 230, 255)
TEAL = (0, 128, 128, 255)
LIGHT_TEAL = (200, 235, 235, 255)
YELLOW = (200, 180, 0, 255)
LIGHT_YELLOW = (255, 255, 200, 255)


def figure_1():
    """Industry 5.0 framework - five pillars around central hub."""
    img = SimplePNG(600, 400)
    img.fill_rect(0, 0, 600, 400, (245, 245, 255, 255))

    # Central hub - Digital Infrastructure
    img.fill_circle(300, 200, 50, LIGHT_BLUE)
    img.draw_circle(300, 200, 50, BLUE, 3)
    # Label lines inside
    img.draw_line(275, 195, 325, 195, DARK, 2)
    img.draw_line(280, 205, 320, 205, DARK, 2)

    # Five pillars around the center
    positions = [(300, 50), (500, 140), (440, 330), (160, 330), (100, 140)]
    colors_bg = [LIGHT_GREEN, LIGHT_ORANGE, LIGHT_PURPLE, LIGHT_TEAL, LIGHT_YELLOW]
    colors_border = [GREEN, ORANGE, PURPLE, TEAL, YELLOW]

    for i, (px, py) in enumerate(positions):
        img.fill_rounded_rect(px - 55, py - 25, 110, 50, colors_bg[i])
        img.draw_rounded_rect(px - 55, py - 25, 110, 50, colors_border[i], 2)
        # Text indicator
        img.draw_line(px - 30, py - 3, px + 30, py - 3, DARK, 2)
        img.draw_line(px - 20, py + 7, px + 20, py + 7, DARK, 1)
        # Connection line to center
        img.draw_line(px, py, 300, 200, GRAY, 1)

    img.save(os.path.join(OUTPUT_DIR, "Figure_1_Industry5_Framework.png"))
    print("Figure 1 saved.")


def figure_2():
    """AI/ML pipeline - linear flow with feedback loop."""
    img = SimplePNG(700, 300)
    img.fill_rect(0, 0, 700, 300, (250, 250, 255, 255))

    # Pipeline stages
    stages = [
        (50, 120, "Data Acq.", LIGHT_BLUE, BLUE),
        (190, 120, "Preprocess", LIGHT_GREEN, GREEN),
        (330, 120, "Model Train", LIGHT_ORANGE, ORANGE),
        (470, 120, "Deploy", LIGHT_PURPLE, PURPLE),
        (610, 120, "Output", LIGHT_TEAL, TEAL),
    ]

    for x, y, label, bg, border in stages:
        img.fill_rounded_rect(x, y, 100, 50, bg)
        img.draw_rounded_rect(x, y, 100, 50, border, 2)
        img.draw_line(x + 20, y + 23, x + 80, y + 23, DARK, 2)
        img.draw_line(x + 25, y + 33, x + 70, y + 33, DARK, 1)

    # Arrows between stages
    for i in range(4):
        x1 = stages[i][0] + 100
        x2 = stages[i + 1][0]
        img.draw_arrow(x1 + 5, 145, x2 - 5, 145, DARK, 2)

    # Feedback loop (curved - simplified as lines)
    img.draw_line(560, 170, 560, 240, RED, 2)
    img.draw_line(560, 240, 140, 240, RED, 2)
    img.draw_arrow(140, 240, 140, 175, RED, 2)
    # Label for feedback
    img.draw_line(320, 235, 380, 235, RED, 1)

    img.save(os.path.join(OUTPUT_DIR, "Figure_2_AI_ML_Pipeline.png"))
    print("Figure 2 saved.")


def figure_3():
    """Three-layer IoT architecture."""
    img = SimplePNG(600, 400)
    img.fill_rect(0, 0, 600, 400, (248, 252, 255, 255))

    # Three layers stacked
    # Application layer (top)
    img.fill_rounded_rect(50, 30, 500, 80, LIGHT_PURPLE)
    img.draw_rounded_rect(50, 30, 500, 80, PURPLE, 2)
    img.draw_line(230, 60, 370, 60, DARK, 2)
    img.draw_line(250, 72, 350, 72, DARK, 1)

    # Network layer (middle)
    img.fill_rounded_rect(50, 150, 500, 80, LIGHT_ORANGE)
    img.draw_rounded_rect(50, 150, 500, 80, ORANGE, 2)
    img.draw_line(230, 180, 370, 180, DARK, 2)
    img.draw_line(250, 192, 350, 192, DARK, 1)

    # Perception layer (bottom)
    img.fill_rounded_rect(50, 270, 500, 80, LIGHT_BLUE)
    img.draw_rounded_rect(50, 270, 500, 80, BLUE, 2)
    img.draw_line(230, 300, 370, 300, DARK, 2)
    img.draw_line(250, 312, 350, 312, DARK, 1)

    # Arrows between layers
    img.draw_arrow(300, 270, 300, 235, DARK, 2)
    img.draw_arrow(300, 150, 300, 115, DARK, 2)

    # Sensor icons at bottom
    for x in [120, 220, 320, 420]:
        img.fill_circle(x, 360, 10, LIGHT_TEAL)
        img.draw_circle(x, 360, 10, TEAL, 2)

    img.save(os.path.join(OUTPUT_DIR, "Figure_3_IoT_Architecture.png"))
    print("Figure 3 saved.")


def figure_4():
    """Digital twin architecture - physical and digital domains with bidirectional flow."""
    img = SimplePNG(650, 350)
    img.fill_rect(0, 0, 650, 350, (250, 252, 248, 255))

    # Physical domain (left)
    img.fill_rounded_rect(30, 50, 250, 250, LIGHT_BLUE)
    img.draw_rounded_rect(30, 50, 250, 250, BLUE, 3)
    img.draw_line(100, 80, 220, 80, BLUE, 2)
    # Sub-elements
    img.fill_rounded_rect(55, 110, 200, 40, (220, 235, 250, 255))
    img.draw_rounded_rect(55, 110, 200, 40, BLUE, 1)
    img.draw_line(100, 128, 200, 128, DARK, 1)

    img.fill_rounded_rect(55, 170, 200, 40, (220, 235, 250, 255))
    img.draw_rounded_rect(55, 170, 200, 40, BLUE, 1)
    img.draw_line(100, 188, 200, 188, DARK, 1)

    img.fill_rounded_rect(55, 230, 200, 40, (220, 235, 250, 255))
    img.draw_rounded_rect(55, 230, 200, 40, BLUE, 1)
    img.draw_line(100, 248, 200, 248, DARK, 1)

    # Digital domain (right)
    img.fill_rounded_rect(370, 50, 250, 250, LIGHT_GREEN)
    img.draw_rounded_rect(370, 50, 250, 250, GREEN, 3)
    img.draw_line(440, 80, 560, 80, GREEN, 2)
    # Sub-elements
    img.fill_rounded_rect(395, 110, 200, 40, (220, 250, 220, 255))
    img.draw_rounded_rect(395, 110, 200, 40, GREEN, 1)
    img.draw_line(440, 128, 540, 128, DARK, 1)

    img.fill_rounded_rect(395, 170, 200, 40, (220, 250, 220, 255))
    img.draw_rounded_rect(395, 170, 200, 40, GREEN, 1)
    img.draw_line(440, 188, 540, 188, DARK, 1)

    img.fill_rounded_rect(395, 230, 200, 40, (220, 250, 220, 255))
    img.draw_rounded_rect(395, 230, 200, 40, GREEN, 1)
    img.draw_line(440, 248, 540, 248, DARK, 1)

    # Bidirectional arrows
    img.draw_arrow(280, 155, 370, 155, ORANGE, 3)
    img.draw_arrow(370, 195, 280, 195, PURPLE, 3)

    img.save(os.path.join(OUTPUT_DIR, "Figure_4_Digital_Twin.png"))
    print("Figure 4 saved.")


def figure_5():
    """Intelligent biorefinery process flow."""
    img = SimplePNG(700, 350)
    img.fill_rect(0, 0, 700, 350, (255, 252, 248, 255))

    # AI Control layer at top
    img.fill_rounded_rect(100, 20, 500, 50, LIGHT_PURPLE)
    img.draw_rounded_rect(100, 20, 500, 50, PURPLE, 2)
    img.draw_line(280, 40, 420, 40, DARK, 2)
    img.draw_line(300, 52, 400, 52, DARK, 1)

    # Process stages
    stages_x = [50, 200, 350, 500]
    labels = ["Pre-treat", "Extract", "Separate", "Purify"]
    for i, x in enumerate(stages_x):
        img.fill_rounded_rect(x, 120, 120, 60, LIGHT_ORANGE)
        img.draw_rounded_rect(x, 120, 120, 60, ORANGE, 2)
        img.draw_line(x + 25, 148, x + 95, 148, DARK, 2)

    # Arrows between process stages
    for i in range(3):
        img.draw_arrow(stages_x[i] + 120, 150, stages_x[i + 1], 150, DARK, 2)

    # Feedback arrows from AI layer down
    for x in stages_x:
        img.draw_line(x + 60, 70, x + 60, 120, GRAY, 1)

    # Output streams at bottom
    outputs_x = [80, 230, 380, 530]
    for x in outputs_x:
        img.fill_rounded_rect(x, 250, 100, 45, LIGHT_GREEN)
        img.draw_rounded_rect(x, 250, 100, 45, GREEN, 2)
        img.draw_line(x + 20, 270, x + 80, 270, DARK, 1)
        # Arrow from process
        img.draw_arrow(x + 50, 180, x + 50, 250, GREEN, 1)

    img.save(os.path.join(OUTPUT_DIR, "Figure_5_Biorefinery_Flow.png"))
    print("Figure 5 saved.")


def figure_6():
    """Blockchain-enabled supply chain."""
    img = SimplePNG(700, 300)
    img.fill_rect(0, 0, 700, 300, (248, 250, 255, 255))

    # Chain of blocks
    block_x = [30, 160, 290, 420, 550]
    block_labels = ["Farm", "Process", "Distribute", "Retail", "Consumer"]
    for i, x in enumerate(block_x):
        img.fill_rounded_rect(x, 80, 110, 70, LIGHT_BLUE)
        img.draw_rounded_rect(x, 80, 110, 70, BLUE, 2)
        # Inner lines (block data)
        img.draw_line(x + 15, 100, x + 95, 100, DARK, 1)
        img.draw_line(x + 15, 112, x + 80, 112, DARK, 1)
        img.draw_line(x + 15, 124, x + 70, 124, GRAY, 1)
        # Hash link visualization
        img.fill_rect(x + 20, 135, 70, 8, LIGHT_ORANGE)
        img.draw_rect(x + 20, 135, 70, 8, ORANGE, 1)

    # Chain links (arrows)
    for i in range(4):
        img.draw_arrow(block_x[i] + 110, 115, block_x[i + 1], 115, DARK, 2)

    # Smart contract indicator at bottom
    img.fill_rounded_rect(200, 200, 300, 50, LIGHT_GREEN)
    img.draw_rounded_rect(200, 200, 300, 50, GREEN, 2)
    img.draw_line(280, 220, 420, 220, DARK, 2)
    img.draw_line(300, 232, 400, 232, DARK, 1)

    # Connection lines from blocks to smart contract
    img.draw_line(300, 150, 300, 200, GRAY, 1)
    img.draw_line(400, 150, 400, 200, GRAY, 1)

    img.save(os.path.join(OUTPUT_DIR, "Figure_6_Blockchain_Supply_Chain.png"))
    print("Figure 6 saved.")


def figure_7():
    """Technology roadmap - near, mid, long term."""
    img = SimplePNG(700, 350)
    img.fill_rect(0, 0, 700, 350, (252, 250, 248, 255))

    # Timeline arrow at bottom
    img.draw_arrow(50, 300, 650, 300, DARK, 3)

    # Three time periods
    # Near-term
    img.fill_rounded_rect(60, 60, 170, 200, LIGHT_BLUE)
    img.draw_rounded_rect(60, 60, 170, 200, BLUE, 2)
    img.draw_line(100, 85, 190, 85, BLUE, 2)
    # Items inside
    for j in range(3):
        img.fill_rounded_rect(80, 110 + j * 45, 130, 30, (230, 240, 255, 255))
        img.draw_rounded_rect(80, 110 + j * 45, 130, 30, BLUE, 1)
        img.draw_line(95, 123 + j * 45, 180, 123 + j * 45, DARK, 1)

    # Mid-term
    img.fill_rounded_rect(265, 60, 170, 200, LIGHT_ORANGE)
    img.draw_rounded_rect(265, 60, 170, 200, ORANGE, 2)
    img.draw_line(305, 85, 395, 85, ORANGE, 2)
    for j in range(3):
        img.fill_rounded_rect(285, 110 + j * 45, 130, 30, (255, 240, 220, 255))
        img.draw_rounded_rect(285, 110 + j * 45, 130, 30, ORANGE, 1)
        img.draw_line(300, 123 + j * 45, 385, 123 + j * 45, DARK, 1)

    # Long-term
    img.fill_rounded_rect(470, 60, 170, 200, LIGHT_GREEN)
    img.draw_rounded_rect(470, 60, 170, 200, GREEN, 2)
    img.draw_line(510, 85, 600, 85, GREEN, 2)
    for j in range(3):
        img.fill_rounded_rect(490, 110 + j * 45, 130, 30, (220, 255, 220, 255))
        img.draw_rounded_rect(490, 110 + j * 45, 130, 30, GREEN, 1)
        img.draw_line(505, 123 + j * 45, 590, 123 + j * 45, DARK, 1)

    # Progression arrows
    img.draw_arrow(230, 160, 265, 160, DARK, 2)
    img.draw_arrow(435, 160, 470, 160, DARK, 2)

    # Time markers on timeline
    for x, label in [(145, "Near"), (350, "Mid"), (555, "Long")]:
        img.fill_circle(x, 300, 6, DARK)

    img.save(os.path.join(OUTPUT_DIR, "Figure_7_Technology_Roadmap.png"))
    print("Figure 7 saved.")


if __name__ == "__main__":
    print("Generating chapter figures...")
    figure_1()
    figure_2()
    figure_3()
    figure_4()
    figure_5()
    figure_6()
    figure_7()
    print(f"\nAll 7 figures saved to: {OUTPUT_DIR}")
