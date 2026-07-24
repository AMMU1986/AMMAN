#!/usr/bin/env python3
"""
Generate 4 publication-quality figures for the Academic Identity chapter.
Uses only standard library (struct, zlib) to create PNG images.
Includes a bitmap font renderer for clear, readable text.
"""
import struct
import zlib
import os

# =============================================================
# Bitmap font - 5x7 pixel characters (uppercase, lowercase, digits, punctuation)
# =============================================================
FONT = {}

def _parse_font():
    """Define a compact 5x7 bitmap font for readable text rendering."""
    chars = {

        'A': ["01110","10001","10001","11111","10001","10001","10001"],
        'B': ["11110","10001","10001","11110","10001","10001","11110"],
        'C': ["01110","10001","10000","10000","10000","10001","01110"],
        'D': ["11100","10010","10001","10001","10001","10010","11100"],
        'E': ["11111","10000","10000","11110","10000","10000","11111"],
        'F': ["11111","10000","10000","11110","10000","10000","10000"],
        'G': ["01110","10001","10000","10111","10001","10001","01110"],
        'H': ["10001","10001","10001","11111","10001","10001","10001"],
        'I': ["01110","00100","00100","00100","00100","00100","01110"],
        'J': ["00111","00010","00010","00010","00010","10010","01100"],
        'K': ["10001","10010","10100","11000","10100","10010","10001"],
        'L': ["10000","10000","10000","10000","10000","10000","11111"],
        'M': ["10001","11011","10101","10101","10001","10001","10001"],
        'N': ["10001","10001","11001","10101","10011","10001","10001"],
        'O': ["01110","10001","10001","10001","10001","10001","01110"],
        'P': ["11110","10001","10001","11110","10000","10000","10000"],
        'Q': ["01110","10001","10001","10001","10101","10010","01101"],
        'R': ["11110","10001","10001","11110","10100","10010","10001"],
        'S': ["01110","10001","10000","01110","00001","10001","01110"],
        'T': ["11111","00100","00100","00100","00100","00100","00100"],
        'U': ["10001","10001","10001","10001","10001","10001","01110"],
        'V': ["10001","10001","10001","10001","10001","01010","00100"],
        'W': ["10001","10001","10001","10101","10101","10101","01010"],
        'X': ["10001","10001","01010","00100","01010","10001","10001"],
        'Y': ["10001","10001","01010","00100","00100","00100","00100"],
        'Z': ["11111","00001","00010","00100","01000","10000","11111"],

        'a': ["00000","00000","01110","00001","01111","10001","01111"],
        'b': ["10000","10000","10110","11001","10001","10001","11110"],
        'c': ["00000","00000","01110","10000","10000","10001","01110"],
        'd': ["00001","00001","01101","10011","10001","10001","01111"],
        'e': ["00000","00000","01110","10001","11111","10000","01110"],
        'f': ["00110","01001","01000","11100","01000","01000","01000"],
        'g': ["00000","01111","10001","10001","01111","00001","01110"],
        'h': ["10000","10000","10110","11001","10001","10001","10001"],
        'i': ["00100","00000","01100","00100","00100","00100","01110"],
        'j': ["00010","00000","00110","00010","00010","10010","01100"],
        'k': ["10000","10000","10010","10100","11000","10100","10010"],
        'l': ["01100","00100","00100","00100","00100","00100","01110"],
        'm': ["00000","00000","11010","10101","10101","10001","10001"],
        'n': ["00000","00000","10110","11001","10001","10001","10001"],
        'o': ["00000","00000","01110","10001","10001","10001","01110"],
        'p': ["00000","00000","11110","10001","11110","10000","10000"],
        'q': ["00000","00000","01101","10011","01111","00001","00001"],
        'r': ["00000","00000","10110","11001","10000","10000","10000"],
        's': ["00000","00000","01110","10000","01110","00001","11110"],
        't': ["01000","01000","11100","01000","01000","01001","00110"],
        'u': ["00000","00000","10001","10001","10001","10011","01101"],
        'v': ["00000","00000","10001","10001","10001","01010","00100"],
        'w': ["00000","00000","10001","10001","10101","10101","01010"],
        'x': ["00000","00000","10001","01010","00100","01010","10001"],
        'y': ["00000","00000","10001","10001","01111","00001","01110"],
        'z': ["00000","00000","11111","00010","00100","01000","11111"],

        '0': ["01110","10001","10011","10101","11001","10001","01110"],
        '1': ["00100","01100","00100","00100","00100","00100","01110"],
        '2': ["01110","10001","00001","00010","00100","01000","11111"],
        '3': ["11111","00010","00100","00010","00001","10001","01110"],
        '4': ["00010","00110","01010","10010","11111","00010","00010"],
        '5': ["11111","10000","11110","00001","00001","10001","01110"],
        '6': ["00110","01000","10000","11110","10001","10001","01110"],
        '7': ["11111","00001","00010","00100","01000","01000","01000"],
        '8': ["01110","10001","10001","01110","10001","10001","01110"],
        '9': ["01110","10001","10001","01111","00001","00010","01100"],
        ' ': ["00000","00000","00000","00000","00000","00000","00000"],
        '.': ["00000","00000","00000","00000","00000","00000","00100"],
        ',': ["00000","00000","00000","00000","00000","00100","01000"],
        ':': ["00000","00000","00100","00000","00000","00100","00000"],
        ';': ["00000","00000","00100","00000","00000","00100","01000"],
        '-': ["00000","00000","00000","11111","00000","00000","00000"],
        '+': ["00000","00100","00100","11111","00100","00100","00000"],
        '/': ["00001","00010","00010","00100","01000","01000","10000"],
        '(': ["00010","00100","01000","01000","01000","00100","00010"],
        ')': ["01000","00100","00010","00010","00010","00100","01000"],
        '&': ["01100","10010","10100","01000","10101","10010","01101"],
        '"': ["01010","01010","01010","00000","00000","00000","00000"],
        "'": ["00100","00100","00100","00000","00000","00000","00000"],
        '?': ["01110","10001","00001","00010","00100","00000","00100"],
        '!': ["00100","00100","00100","00100","00100","00000","00100"],
        '[': ["01110","01000","01000","01000","01000","01000","01110"],
        ']': ["01110","00010","00010","00010","00010","00010","01110"],
        '%': ["11001","11010","00010","00100","01000","01011","10011"],
    }
    for ch, rows in chars.items():
        FONT[ch] = [[int(b) for b in row] for row in rows]

_parse_font()


# =============================================================
# Image drawing primitives
# =============================================================

class Image:
    def __init__(self, width, height, bg=(255, 255, 255)):
        self.w = width
        self.h = height
        self.pixels = [[bg for _ in range(width)] for _ in range(height)]

    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.pixels[y][x] = color

    def fill_rect(self, x, y, w, h, color):
        for dy in range(h):
            for dx in range(w):
                self.set_pixel(x + dx, y + dy, color)

    def draw_rect(self, x, y, w, h, color, thickness=1):
        for t in range(thickness):
            for dx in range(w):
                self.set_pixel(x + dx, y + t, color)
                self.set_pixel(x + dx, y + h - 1 - t, color)
            for dy in range(h):
                self.set_pixel(x + t, y + dy, color)
                self.set_pixel(x + w - 1 - t, y + dy, color)

    def draw_line(self, x1, y1, x2, y2, color, thickness=1):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            for t in range(-(thickness//2), (thickness+1)//2):
                self.set_pixel(x1 + t, y1, color)
                self.set_pixel(x1, y1 + t, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy


    def draw_text(self, x, y, text, color=(0, 0, 0), scale=2):
        """Draw text using bitmap font at given scale."""
        cx = x
        for ch in text:
            glyph = FONT.get(ch, FONT.get(' '))
            if glyph is None:
                cx += 6 * scale
                continue
            for row_i, row in enumerate(glyph):
                for col_i, pixel in enumerate(row):
                    if pixel:
                        for sy in range(scale):
                            for sx in range(scale):
                                self.set_pixel(cx + col_i * scale + sx,
                                             y + row_i * scale + sy, color)
            cx += 6 * scale

    def draw_text_centered(self, cx, y, text, color=(0, 0, 0), scale=2):
        """Draw text centered horizontally at cx."""
        text_width = len(text) * 6 * scale
        self.draw_text(cx - text_width // 2, y, text, color, scale)

    def fill_circle(self, cx, cy, r, color):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx)**2 + (y - cy)**2 <= r**2:
                    self.set_pixel(x, y, color)

    def draw_circle(self, cx, cy, r, color, thickness=2):
        for y in range(cy - r - thickness, cy + r + thickness + 1):
            for x in range(cx - r - thickness, cx + r + thickness + 1):
                d = (x - cx)**2 + (y - cy)**2
                if (r - thickness)**2 <= d <= (r + thickness)**2:
                    self.set_pixel(x, y, color)

    def draw_arrow(self, x1, y1, x2, y2, color, thickness=2):
        """Draw a line with an arrowhead at the end."""
        self.draw_line(x1, y1, x2, y2, color, thickness)
        # Arrowhead
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        arr_len = 10
        for i in range(2):
            a = angle + math.pi + (0.4 if i == 0 else -0.4)
            ax = int(x2 + arr_len * math.cos(a))
            ay = int(y2 + arr_len * math.sin(a))
            self.draw_line(x2, y2, ax, ay, color, thickness)


    def draw_rounded_rect(self, x, y, w, h, color, fill=None, thickness=2):
        """Draw a rectangle with slightly rounded corners."""
        if fill:
            self.fill_rect(x + 2, y, w - 4, h, fill)
            self.fill_rect(x, y + 2, w, h - 4, fill)
            self.fill_rect(x + 1, y + 1, w - 2, h - 2, fill)
        # Borders
        self.draw_line(x + 2, y, x + w - 3, y, color, thickness)
        self.draw_line(x + 2, y + h - 1, x + w - 3, y + h - 1, color, thickness)
        self.draw_line(x, y + 2, x, y + h - 3, color, thickness)
        self.draw_line(x + w - 1, y + 2, x + w - 1, y + h - 3, color, thickness)

    def save_png(self, filename):
        """Save image as PNG file."""
        def chunk(chunk_type, data):
            c = chunk_type + data
            crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
            return struct.pack('>I', len(data)) + c + crc

        sig = b'\x89PNG\r\n\x1a\n'
        ihdr_data = struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0)
        ihdr = chunk(b'IHDR', ihdr_data)

        raw_data = b''
        for row in self.pixels:
            raw_data += b'\x00'
            for pixel in row:
                raw_data += struct.pack('BBB', *pixel)

        compressed = zlib.compress(raw_data, 9)
        idat = chunk(b'IDAT', compressed)
        iend = chunk(b'IEND', b'')

        with open(filename, 'wb') as f:
            f.write(sig + ihdr + idat + iend)
        print(f"  Saved: {filename} ({self.w}x{self.h})")


# =============================================================
# Figure 1: Conceptual Framework - Identity-Development Nexus
# =============================================================

def create_figure_1(output_dir):
    """Conceptual framework showing the relationship between
    academic identity and professional development."""
    img = Image(900, 600, bg=(255, 255, 255))

    # Title
    img.draw_text_centered(450, 15, "Figure 1: Conceptual Framework", (0, 0, 0), 3)
    img.draw_text_centered(450, 50, "The Identity-Development Nexus in Higher Education", (60, 60, 60), 2)

    # Central circle - Identity
    img.fill_circle(450, 300, 70, (220, 235, 250))
    img.draw_circle(450, 300, 70, (40, 80, 160), 3)
    img.draw_text_centered(450, 285, "ACADEMIC", (20, 50, 120), 2)
    img.draw_text_centered(450, 305, "IDENTITY", (20, 50, 120), 2)

    # Four surrounding nodes
    nodes = [
        (200, 150, "INSTITUTIONAL", "CONTEXT", (255, 235, 220), (180, 80, 30)),
        (700, 150, "DISCIPLINARY", "COMMUNITY", (220, 245, 220), (40, 120, 40)),
        (200, 450, "PROFESSIONAL", "DEVELOPMENT", (240, 220, 250), (100, 40, 140)),
        (700, 450, "PERSONAL", "VALUES", (255, 240, 220), (160, 100, 20)),
    ]
    for nx, ny, line1, line2, fill, border in nodes:
        img.fill_circle(nx, ny, 60, fill)
        img.draw_circle(nx, ny, 60, border, 2)
        img.draw_text_centered(nx, ny - 10, line1, border, 2)
        img.draw_text_centered(nx, ny + 10, line2, border, 2)

    # Arrows connecting nodes to center
    arrows = [(270, 195, 385, 260), (630, 195, 515, 260),
              (270, 405, 385, 340), (630, 405, 515, 340)]
    for x1, y1, x2, y2 in arrows:
        img.draw_arrow(x1, y1, x2, y2, (80, 80, 80), 2)
        img.draw_arrow(x2, y2, x1, y1, (80, 80, 80), 2)

    # Labels on arrows
    img.draw_text(130, 250, "Shapes", (100, 100, 100), 2)
    img.draw_text(620, 250, "Anchors", (100, 100, 100), 2)
    img.draw_text(120, 370, "Develops", (100, 100, 100), 2)
    img.draw_text(620, 370, "Motivates", (100, 100, 100), 2)

    # Bottom legend
    img.draw_text(100, 550, "Source: Adapted from Henkel (2000) and Clegg (2008)", (100,100,100), 2)
    img.draw_text(100, 575, "Note: Bidirectional arrows indicate mutually constitutive relationships", (120,120,120), 2)

    img.save_png(os.path.join(output_dir, "Figure_1_Conceptual_Framework.png"))


# =============================================================
# Figure 2: Forces of Unbundling - Triple Threat Diagram
# =============================================================

def create_figure_2(output_dir):
    """Three converging forces that unbundle academic identity."""
    img = Image(900, 600, bg=(255, 255, 255))

    # Title
    img.draw_text_centered(450, 15, "Figure 2: The Triple Threat of Unbundling", (0, 0, 0), 3)
    img.draw_text_centered(450, 50, "Forces Fragmenting the Traditional Academic Role", (60, 60, 60), 2)

    # Three force boxes at top
    boxes = [
        (50, 100, 240, 120, "ADJUNCTIFICATION", "Teaching separated", "from research", (255, 220, 220), (180, 40, 40)),
        (330, 100, 240, 120, "EDUCATIONAL", "Technology mediates", "student contact", (220, 240, 255), (40, 80, 180)),
        (610, 100, 240, 120, "ADMINISTRATIVE", "Service functions", "outsourced", (220, 255, 220), (40, 140, 40)),
    ]
    for bx, by, bw, bh, title, l1, l2, fill, border in boxes:
        img.fill_rect(bx, by, bw, bh, fill)
        img.draw_rect(bx, by, bw, bh, border, 2)
        img.draw_text_centered(bx + bw//2, by + 15, title, border, 2)
        img.draw_text_centered(bx + bw//2, by + 55, l1, (60, 60, 60), 2)
        img.draw_text_centered(bx + bw//2, by + 80, l2, (60, 60, 60), 2)

    # Arrows pointing down to center
    img.draw_arrow(170, 220, 350, 310, (180, 40, 40), 2)
    img.draw_arrow(450, 220, 450, 300, (40, 80, 180), 2)
    img.draw_arrow(730, 220, 550, 310, (40, 140, 40), 2)

    # Central impact zone
    img.fill_rect(280, 310, 340, 100, (255, 250, 230))
    img.draw_rect(280, 310, 340, 100, (160, 80, 0), 2)
    img.draw_text_centered(450, 330, "FRAGMENTED", (140, 60, 0), 2)
    img.draw_text_centered(450, 355, "ACADEMIC IDENTITY", (140, 60, 0), 2)
    img.draw_text_centered(450, 385, "Competing roles and expectations", (100, 80, 40), 2)

    # Consequences below
    img.draw_arrow(450, 410, 450, 450, (80, 80, 80), 2)

    consequences = [
        (120, 460, "Role ambiguity"),
        (320, 460, "Value conflicts"),
        (520, 460, "Precarity"),
        (700, 460, "Metric anxiety"),
    ]
    for cx, cy, label in consequences:
        img.fill_rect(cx - 10, cy, 170, 40, (245, 245, 255))
        img.draw_rect(cx - 10, cy, 170, 40, (100, 100, 160), 1)
        img.draw_text(cx + 5, cy + 12, label, (60, 60, 120), 2)

    # Source
    img.draw_text(100, 550, "Source: Based on Macfarlane (2011) and Whitchurch (2013)", (100,100,100), 2)
    img.draw_text(100, 575, "Note: Arrows indicate causal pathways from structural forces to identity fragmentation", (120,120,120), 2)

    img.save_png(os.path.join(output_dir, "Figure_2_Unbundling_Forces.png"))


# =============================================================
# Figure 3: T-Shaped Academic Development Model
# =============================================================

def create_figure_3(output_dir):
    """The T-Shaped Academic professional development model."""
    img = Image(900, 600, bg=(255, 255, 255))

    # Title
    img.draw_text_centered(450, 15, "Figure 3: The T-Shaped Academic", (0, 0, 0), 3)
    img.draw_text_centered(450, 50, "Balancing Depth and Breadth in Professional Development", (60, 60, 60), 2)

    # Draw the T shape
    # Horizontal bar (breadth)
    img.fill_rect(100, 120, 700, 80, (220, 235, 250))
    img.draw_rect(100, 120, 700, 80, (40, 80, 160), 2)
    img.draw_text_centered(450, 135, "BREADTH: Transversal Competencies", (20, 50, 120), 2)
    # Items in horizontal bar
    items_h = ["Digital Literacy", "Communication", "Leadership", "Ethics", "Networking"]
    for i, item in enumerate(items_h):
        x = 130 + i * 140
        img.draw_text(x, 168, item, (60, 80, 140), 2)

    # Vertical bar (depth)
    img.fill_rect(370, 200, 160, 320, (255, 235, 220))
    img.draw_rect(370, 200, 160, 320, (180, 80, 30), 2)
    img.draw_text_centered(450, 220, "DEPTH:", (140, 60, 0), 2)
    img.draw_text_centered(450, 245, "Disciplinary", (140, 60, 0), 2)
    img.draw_text_centered(450, 270, "Expertise", (140, 60, 0), 2)

    # Depth items
    depth_items = ["Methodology", "Theory", "Publications", "Peer Network", "Reputation"]
    for i, item in enumerate(depth_items):
        img.draw_text_centered(450, 310 + i * 35, item, (120, 60, 20), 2)

    # Career stage annotations
    img.draw_text(570, 250, "Early Career:", (80, 80, 80), 2)
    img.draw_text(570, 275, "Focus on depth", (80, 80, 80), 2)
    img.draw_arrow(560, 270, 535, 270, (80, 80, 80), 1)

    img.draw_text(570, 140, "Mid/Senior Career:", (80, 80, 80), 2)
    img.draw_text(570, 165, "Expand breadth", (80, 80, 80), 2)

    # Source
    img.draw_text(100, 555, "Source: Adapted from Barile et al. (2012)", (100,100,100), 2)
    img.draw_text(100, 578, "Note: The T-shape represents the integration of specialist and generalist competencies", (120,120,120), 2)

    img.save_png(os.path.join(output_dir, "Figure_3_T_Shaped_Academic.png"))


# =============================================================
# Figure 4: Future Academic Ecosystem
# =============================================================

def create_figure_4(output_dir):
    """The post-digital academic ecosystem showing new collegiality."""
    img = Image(900, 600, bg=(255, 255, 255))

    # Title
    img.draw_text_centered(450, 15, "Figure 4: The Post-Digital Academic Ecosystem", (0, 0, 0), 3)
    img.draw_text_centered(450, 50, "From Individual Survival to Collective Reimagination", (60, 60, 60), 2)

    # Central node: New Collegiality
    img.fill_circle(450, 310, 75, (230, 245, 230))
    img.draw_circle(450, 310, 75, (40, 120, 40), 3)
    img.draw_text_centered(450, 290, "NEW", (30, 90, 30), 2)
    img.draw_text_centered(450, 310, "COLLEGIALITY", (30, 90, 30), 2)
    img.draw_text_centered(450, 330, "(Mutualistic)", (50, 100, 50), 2)

    # Surrounding elements in a ring
    elements = [
        (200, 130, "AI Literacy", (240, 220, 255), (80, 40, 160)),
        (450, 100, "Global Citizenship", (255, 240, 220), (160, 100, 20)),
        (700, 130, "Slow Scholarship", (220, 255, 220), (40, 130, 40)),
        (150, 310, "Wellbeing", (255, 220, 220), (160, 40, 40)),
        (750, 310, "Open Science", (220, 240, 255), (40, 80, 160)),
        (200, 490, "Peer Mentoring", (255, 235, 220), (160, 100, 30)),
        (450, 520, "Shared Resources", (240, 240, 255), (80, 80, 160)),
        (700, 490, "Advocacy Networks", (230, 255, 230), (40, 120, 40)),
    ]
    for ex, ey, label, fill, border in elements:
        img.fill_circle(ex, ey, 50, fill)
        img.draw_circle(ex, ey, 50, border, 2)
        # Split label if long
        words = label.split()
        if len(words) == 1:
            img.draw_text_centered(ex, ey - 5, words[0], border, 2)
        else:
            img.draw_text_centered(ex, ey - 10, words[0], border, 2)
            img.draw_text_centered(ex, ey + 10, words[1], border, 2)

    # Connect elements to center with lines
    connections = [(200, 130), (450, 100), (700, 130), (150, 310),
                   (750, 310), (200, 490), (450, 520), (700, 490)]
    for cx, cy in connections:
        # Draw dashed-style line (just a lighter line)
        img.draw_line(cx, cy, 450, 310, (180, 200, 180), 1)

    # Source
    img.draw_text(80, 570, "Source: Synthesised from Boyer (1996), Mountz et al. (2015), Peseta et al. (2022)", (100,100,100), 2)

    img.save_png(os.path.join(output_dir, "Figure_4_Academic_Ecosystem.png"))


# =============================================================
# Main
# =============================================================

if __name__ == '__main__':
    output_dir = '/projects/sandbox/AMMAN/chapter_figures'
    os.makedirs(output_dir, exist_ok=True)

    print("Generating chapter figures...")
    create_figure_1(output_dir)
    create_figure_2(output_dir)
    create_figure_3(output_dir)
    create_figure_4(output_dir)
    print("\nAll figures generated successfully!")
