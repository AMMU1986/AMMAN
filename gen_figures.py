#!/usr/bin/env python3
"""Generate 4 figures for the GenAI chapter using only standard library."""
import struct
import zlib
import os

OUTPUT_DIR = "/projects/sandbox/AMMAN/genai_figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_png(width, height, pixels_func, filename):
    """Create a PNG file from pixel data. pixels_func(x,y) returns (r,g,b)."""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = zlib.crc32(chunk) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)

    # PNG signature
    sig = b'\x89PNG\r\n\x1a\n'
    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)
    # IDAT
    raw = b''
    for y in range(height):
        raw += b'\x00'  # filter byte
        for x in range(width):
            r, g, b = pixels_func(x, y)
            raw += struct.pack('BBB', r, g, b)
    compressed = zlib.compress(raw)
    idat = make_chunk(b'IDAT', compressed)
    # IEND
    iend = make_chunk(b'IEND', b'')

    with open(filename, 'wb') as f:
        f.write(sig + ihdr + idat + iend)



def draw_text_on_grid(grid, text, x0, y0, color, scale=1):
    """Simple 3x5 font renderer for labels."""
    font = {
        'A': ['010','101','111','101','101'], 'B': ['110','101','110','101','110'],
        'C': ['011','100','100','100','011'], 'D': ['110','101','101','101','110'],
        'E': ['111','100','110','100','111'], 'F': ['111','100','110','100','100'],
        'G': ['011','100','101','101','011'], 'H': ['101','101','111','101','101'],
        'I': ['111','010','010','010','111'], 'J': ['001','001','001','101','010'],
        'K': ['101','110','100','110','101'], 'L': ['100','100','100','100','111'],
        'M': ['101','111','111','101','101'], 'N': ['101','111','111','111','101'],
        'O': ['010','101','101','101','010'], 'P': ['110','101','110','100','100'],
        'Q': ['010','101','101','111','011'], 'R': ['110','101','110','101','101'],
        'S': ['011','100','010','001','110'], 'T': ['111','010','010','010','010'],
        'U': ['101','101','101','101','011'], 'V': ['101','101','101','010','010'],
        'W': ['101','101','111','111','101'], 'X': ['101','101','010','101','101'],
        'Y': ['101','101','010','010','010'], 'Z': ['111','001','010','100','111'],
        '0': ['010','101','101','101','010'], '1': ['010','110','010','010','111'],
        '2': ['110','001','010','100','111'], '3': ['110','001','010','001','110'],
        '4': ['101','101','111','001','001'], '5': ['111','100','110','001','110'],
        '6': ['011','100','110','101','010'], '7': ['111','001','010','010','010'],
        '8': ['010','101','010','101','010'], '9': ['010','101','011','001','110'],
        ' ': ['000','000','000','000','000'], '.': ['000','000','000','000','010'],
        '-': ['000','000','111','000','000'], '%': ['101','001','010','100','101'],
        '/': ['001','001','010','100','100'], ':': ['000','010','000','010','000'],
        ',': ['000','000','000','010','100'], '(': ['001','010','010','010','001'],
        ')': ['100','010','010','010','100'], '+': ['000','010','111','010','000'],
        '&': ['010','101','010','101','011'],
    }
    cx = x0
    for ch in text.upper():
        glyph = font.get(ch, ['000','000','000','000','000'])
        for row_i, row in enumerate(glyph):
            for col_i, bit in enumerate(row):
                if bit == '1':
                    for sy in range(scale):
                        for sx in range(scale):
                            py = y0 + row_i * scale + sy
                            px = cx + col_i * scale + sx
                            if 0 <= py < len(grid) and 0 <= px < len(grid[0]):
                                grid[py][px] = color
        cx += (len(glyph[0]) + 1) * scale



def fill_rect(grid, x, y, w, h, color):
    """Fill a rectangle on the grid."""
    for dy in range(h):
        for dx in range(w):
            py, px = y + dy, x + dx
            if 0 <= py < len(grid) and 0 <= px < len(grid[0]):
                grid[py][px] = color


def draw_line(grid, x1, y1, x2, y2, color):
    """Draw a line using Bresenham's algorithm."""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        if 0 <= y1 < len(grid) and 0 <= x1 < len(grid[0]):
            grid[y1][x1] = color
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def generate_figure1():
    """Figure 1: GenAI Adoption Rates in Business Intelligence (Bar Chart)."""
    W, H = 640, 400
    bg = (255, 255, 255)
    grid = [[bg for _ in range(W)] for _ in range(H)]

    # Title
    draw_text_on_grid(grid, "FIGURE 1: GENAI ADOPTION IN BUSINESS INTELLIGENCE", 80, 15, (0, 0, 0), 2)

    # Data: sectors and adoption %
    sectors = ["FINANCE", "HEALTH", "RETAIL", "MANUFAC", "ENERGY"]
    values = [72, 58, 65, 45, 38]
    colors = [(41, 128, 185), (39, 174, 96), (192, 57, 43), (142, 68, 173), (243, 156, 18)]

    # Axes
    ox, oy = 100, 350  # origin
    draw_line(grid, ox, 50, ox, oy, (0, 0, 0))
    draw_line(grid, ox, oy, 600, oy, (0, 0, 0))

    # Y-axis labels
    for val in range(0, 101, 20):
        yp = oy - int(val * 2.8)
        draw_text_on_grid(grid, str(val), ox - 35, yp - 3, (80, 80, 80), 1)
        draw_line(grid, ox, yp, ox + 5, yp, (80, 80, 80))

    # Bars
    bar_w = 70
    gap = 20
    for i, (sec, val, col) in enumerate(zip(sectors, values, colors)):
        x = ox + gap + i * (bar_w + gap)
        bar_h = int(val * 2.8)
        fill_rect(grid, x, oy - bar_h, bar_w, bar_h, col)
        draw_text_on_grid(grid, sec, x + 5, oy + 8, (0, 0, 0), 1)
        draw_text_on_grid(grid, str(val) + "%", x + 20, oy - bar_h - 12, col, 1)

    # Y-axis label
    draw_text_on_grid(grid, "ADOPTION RATE %", 10, 180, (0, 0, 0), 1)

    filepath = os.path.join(OUTPUT_DIR, "Figure_1_GenAI_Adoption_BI.png")
    create_png(W, H, lambda x, y: grid[y][x], filepath)
    print(f"Created: {filepath}")



def generate_figure2():
    """Figure 2: Framework for AI-Driven Sustainable Human Capital (Flowchart)."""
    W, H = 640, 480
    bg = (245, 248, 250)
    grid = [[bg for _ in range(W)] for _ in range(H)]

    # Title
    draw_text_on_grid(grid, "FIGURE 2: AI-DRIVEN SUSTAINABLE", 130, 10, (0, 0, 0), 2)
    draw_text_on_grid(grid, "HUMAN CAPITAL FRAMEWORK", 160, 35, (0, 0, 0), 2)

    # Boxes
    boxes = [
        (220, 70, 200, 40, "GENERATIVE AI ENGINE", (41, 128, 185)),
        (60, 160, 180, 35, "WORKFORCE ANALYTICS", (39, 174, 96)),
        (400, 160, 180, 35, "TALENT INTELLIGENCE", (142, 68, 173)),
        (60, 240, 180, 35, "PERSONALIZED LEARNING", (192, 57, 43)),
        (400, 240, 180, 35, "SKILL DEVELOPMENT", (243, 156, 18)),
        (140, 330, 180, 35, "SUSTAINABILITY METRICS", (22, 160, 133)),
        (320, 330, 180, 35, "BUSINESS INTELLIGENCE", (41, 128, 185)),
        (220, 410, 200, 40, "SUSTAINABLE ENTERPRISE", (39, 174, 96)),
    ]

    for (bx, by, bw, bh, label, col) in boxes:
        fill_rect(grid, bx, by, bw, bh, col)
        # Border
        draw_line(grid, bx, by, bx + bw, by, (0, 0, 0))
        draw_line(grid, bx, by + bh, bx + bw, by + bh, (0, 0, 0))
        draw_line(grid, bx, by, bx, by + bh, (0, 0, 0))
        draw_line(grid, bx + bw, by, bx + bw, by + bh, (0, 0, 0))
        draw_text_on_grid(grid, label, bx + 10, by + 14, (255, 255, 255), 1)

    # Arrows (simple vertical/horizontal lines)
    arrow_col = (100, 100, 100)
    # From GenAI Engine down to Workforce Analytics and Talent Intelligence
    draw_line(grid, 320, 110, 150, 160, arrow_col)
    draw_line(grid, 320, 110, 490, 160, arrow_col)
    # Down to next level
    draw_line(grid, 150, 195, 150, 240, arrow_col)
    draw_line(grid, 490, 195, 490, 240, arrow_col)
    # Converge to sustainability
    draw_line(grid, 150, 275, 230, 330, arrow_col)
    draw_line(grid, 490, 275, 410, 330, arrow_col)
    # Down to sustainable enterprise
    draw_line(grid, 230, 365, 320, 410, arrow_col)
    draw_line(grid, 410, 365, 320, 410, arrow_col)

    filepath = os.path.join(OUTPUT_DIR, "Figure_2_AI_Human_Capital_Framework.png")
    create_png(W, H, lambda x, y: grid[y][x], filepath)
    print(f"Created: {filepath}")



def generate_figure3():
    """Figure 3: Risk Assessment Matrix for AI Implementation."""
    W, H = 640, 440
    bg = (255, 255, 255)
    grid = [[bg for _ in range(W)] for _ in range(H)]

    # Title
    draw_text_on_grid(grid, "FIGURE 3: RISK ASSESSMENT MATRIX", 140, 10, (0, 0, 0), 2)
    draw_text_on_grid(grid, "FOR AI IMPLEMENTATION", 180, 35, (0, 0, 0), 2)

    # Grid for matrix (5x5)
    ox, oy = 120, 80
    cell_w, cell_h = 90, 60
    rows, cols = 5, 5

    # Color coding: green(low), yellow(med), orange(high), red(critical)
    risk_colors = [
        [(144,238,144),(144,238,144),(255,255,150),(255,255,150),(255,200,100)],
        [(144,238,144),(255,255,150),(255,255,150),(255,200,100),(255,200,100)],
        [(255,255,150),(255,255,150),(255,200,100),(255,200,100),(255,100,100)],
        [(255,255,150),(255,200,100),(255,200,100),(255,100,100),(255,100,100)],
        [(255,200,100),(255,200,100),(255,100,100),(255,100,100),(200,50,50)],
    ]

    # Draw grid
    for r in range(rows):
        for c in range(cols):
            x = ox + c * cell_w
            y = oy + r * cell_h
            fill_rect(grid, x, y, cell_w - 2, cell_h - 2, risk_colors[r][c])
            draw_line(grid, x, y, x + cell_w - 2, y, (80, 80, 80))
            draw_line(grid, x, y + cell_h - 2, x + cell_w - 2, y + cell_h - 2, (80, 80, 80))
            draw_line(grid, x, y, x, y + cell_h - 2, (80, 80, 80))
            draw_line(grid, x + cell_w - 2, y, x + cell_w - 2, y + cell_h - 2, (80, 80, 80))

    # Axis labels
    x_labels = ["VERY LOW", "LOW", "MEDIUM", "HIGH", "VERY HIGH"]
    y_labels = ["VERY LOW", "LOW", "MEDIUM", "HIGH", "VERY HIGH"]
    for i, lbl in enumerate(x_labels):
        draw_text_on_grid(grid, lbl, ox + i * cell_w + 10, oy + rows * cell_h + 10, (0, 0, 0), 1)
    for i, lbl in enumerate(y_labels):
        draw_text_on_grid(grid, lbl, ox - 80, oy + i * cell_h + 25, (0, 0, 0), 1)

    draw_text_on_grid(grid, "LIKELIHOOD", ox + 180, oy + rows * cell_h + 30, (0, 0, 0), 2)
    draw_text_on_grid(grid, "IMPACT", 20, oy + 130, (0, 0, 0), 2)

    # Legend
    legend_y = 400
    fill_rect(grid, 120, legend_y, 20, 15, (144, 238, 144))
    draw_text_on_grid(grid, "LOW", 145, legend_y + 3, (0, 0, 0), 1)
    fill_rect(grid, 220, legend_y, 20, 15, (255, 255, 150))
    draw_text_on_grid(grid, "MEDIUM", 245, legend_y + 3, (0, 0, 0), 1)
    fill_rect(grid, 340, legend_y, 20, 15, (255, 200, 100))
    draw_text_on_grid(grid, "HIGH", 365, legend_y + 3, (0, 0, 0), 1)
    fill_rect(grid, 440, legend_y, 20, 15, (255, 100, 100))
    draw_text_on_grid(grid, "CRITICAL", 465, legend_y + 3, (0, 0, 0), 1)

    filepath = os.path.join(OUTPUT_DIR, "Figure_3_Risk_Assessment_Matrix.png")
    create_png(W, H, lambda x, y: grid[y][x], filepath)
    print(f"Created: {filepath}")



def generate_figure4():
    """Figure 4: Future Trajectory of AI-Sustainability Integration (Line Chart)."""
    W, H = 640, 400
    bg = (255, 255, 255)
    grid = [[bg for _ in range(W)] for _ in range(H)]

    # Title
    draw_text_on_grid(grid, "FIGURE 4: PROJECTED AI-SUSTAINABILITY", 100, 10, (0, 0, 0), 2)
    draw_text_on_grid(grid, "INTEGRATION TRAJECTORY 2024-2035", 110, 35, (0, 0, 0), 2)

    # Axes
    ox, oy = 80, 340
    ax_w, ax_h = 500, 260
    draw_line(grid, ox, oy - ax_h, ox, oy, (0, 0, 0))
    draw_line(grid, ox, oy, ox + ax_w, oy, (0, 0, 0))

    # Data series (3 lines)
    years = list(range(2024, 2036))
    ai_adoption = [25, 32, 40, 50, 58, 65, 72, 78, 83, 87, 90, 93]
    sustainability = [15, 20, 28, 35, 43, 52, 60, 68, 75, 80, 85, 89]
    human_capital = [20, 25, 30, 38, 45, 53, 60, 66, 72, 78, 82, 86]

    colors = [(41, 128, 185), (39, 174, 96), (192, 57, 43)]
    series = [ai_adoption, sustainability, human_capital]
    labels = ["AI ADOPTION", "SUSTAINABILITY", "HUMAN CAPITAL"]

    # X-axis labels
    for i, yr in enumerate(years):
        x = ox + int(i * ax_w / (len(years) - 1))
        if i % 2 == 0:
            draw_text_on_grid(grid, str(yr), x - 10, oy + 8, (80, 80, 80), 1)

    # Y-axis labels
    for val in range(0, 101, 20):
        yp = oy - int(val * ax_h / 100)
        draw_text_on_grid(grid, str(val) + "%", ox - 40, yp - 3, (80, 80, 80), 1)
        # Grid line
        for gx in range(ox, ox + ax_w, 4):
            if 0 <= yp < H and 0 <= gx < W:
                grid[yp][gx] = (220, 220, 220)

    # Plot lines
    for s_idx, (data, col) in enumerate(zip(series, colors)):
        for i in range(len(data) - 1):
            x1 = ox + int(i * ax_w / (len(data) - 1))
            y1 = oy - int(data[i] * ax_h / 100)
            x2 = ox + int((i + 1) * ax_w / (len(data) - 1))
            y2 = oy - int(data[i + 1] * ax_h / 100)
            draw_line(grid, x1, y1, x2, y2, col)
            draw_line(grid, x1, y1 + 1, x2, y2 + 1, col)
            draw_line(grid, x1, y1 - 1, x2, y2 - 1, col)

    # Legend
    for i, (lbl, col) in enumerate(zip(labels, colors)):
        lx = 150 + i * 170
        ly = 370
        fill_rect(grid, lx, ly, 20, 8, col)
        draw_text_on_grid(grid, lbl, lx + 25, ly, (0, 0, 0), 1)

    filepath = os.path.join(OUTPUT_DIR, "Figure_4_AI_Sustainability_Trajectory.png")
    create_png(W, H, lambda x, y: grid[y][x], filepath)
    print(f"Created: {filepath}")


if __name__ == "__main__":
    generate_figure1()
    generate_figure2()
    generate_figure3()
    generate_figure4()
    print("All figures generated successfully!")
