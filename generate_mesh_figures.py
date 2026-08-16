#!/usr/bin/env python3
"""
Generate CFD mesh visualization TIFF images for slotted blade configurations.
Uses only Python standard library (no external dependencies).

Mesh Parameters (Fine level - used for visualization):
- Total Elements: 10,24,000
- Boundary Layer Elements: 3,10,000
- Inflation Layers: 20
- First Layer Thickness: 0.005 mm
- Growth Ratio: 1.15
- ΔP_reverse: 6,195 Pa (reference)
"""

import struct
import math
import os

# ============================================================================
# TIFF WRITER (Pure Python)
# ============================================================================

def write_tiff(filename, pixels, width, height):
    """Write a grayscale TIFF file from pixel data (list of 0-255 values)."""
    # TIFF Header
    byte_order = b'II'  # Little endian
    magic = struct.pack('<H', 42)
    ifd_offset = struct.pack('<I', 8)  # IFD starts right after header
    
    # Image data offset (after header + IFD)
    # IFD: 2 bytes (count) + entries + 4 bytes (next IFD = 0)
    num_tags = 11
    ifd_size = 2 + num_tags * 12 + 4
    strips_offset = 8 + ifd_size + 8  # +8 for resolution rational values
    
    # Resolution values (72 DPI as rational)
    res_offset = 8 + ifd_size
    
    def make_tag(tag_id, type_id, count, value):
        """Create a 12-byte IFD entry."""
        return struct.pack('<HHI', tag_id, type_id, count) + struct.pack('<I', value)
    
    row_bytes = width
    strip_size = row_bytes * height
    
    tags = [
        make_tag(256, 3, 1, width),          # ImageWidth
        make_tag(257, 3, 1, height),         # ImageLength
        make_tag(258, 3, 1, 8),              # BitsPerSample
        make_tag(259, 3, 1, 1),              # Compression (None)
        make_tag(262, 3, 1, 1),              # PhotometricInterpretation (BlackIsZero)
        make_tag(273, 3, 1, strips_offset),  # StripOffsets
        make_tag(277, 3, 1, 1),              # SamplesPerPixel
        make_tag(278, 3, 1, height),         # RowsPerStrip
        make_tag(279, 4, 1, strip_size),     # StripByteCounts
        make_tag(282, 5, 1, res_offset),     # XResolution
        make_tag(283, 5, 1, res_offset),     # YResolution
    ]
    
    with open(filename, 'wb') as f:
        # Header
        f.write(byte_order + magic + ifd_offset)
        # IFD
        f.write(struct.pack('<H', num_tags))
        for tag in tags:
            f.write(tag)
        f.write(struct.pack('<I', 0))  # Next IFD offset (none)
        # Resolution rational (72/1)
        f.write(struct.pack('<II', 72, 1))
        # Pixel data
        f.write(bytes(pixels))


# ============================================================================
# DRAWING PRIMITIVES
# ============================================================================

class Canvas:
    """Simple drawing canvas for mesh visualization."""
    
    def __init__(self, width, height, bg=255):
        self.width = width
        self.height = height
        self.pixels = [bg] * (width * height)
    
    def set_pixel(self, x, y, val):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y * self.width + x] = max(0, min(255, val))
    
    def get_pixel(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y * self.width + x]
        return 255
    
    def draw_line(self, x0, y0, x1, y1, val=0, thickness=1):
        """Bresenham's line algorithm with thickness."""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            for t in range(-(thickness//2), (thickness+1)//2):
                if dx > dy:
                    self.set_pixel(x0, y0 + t, val)
                else:
                    self.set_pixel(x0 + t, y0, val)
            
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
    
    def draw_circle(self, cx, cy, r, val=0, thickness=1):
        """Draw circle outline."""
        for angle in range(360 * 4):
            a = math.radians(angle / 4.0)
            x = int(cx + r * math.cos(a))
            y = int(cy + r * math.sin(a))
            for t in range(-(thickness//2), (thickness+1)//2):
                self.set_pixel(x + t, y, val)
                self.set_pixel(x, y + t, val)
    
    def draw_arc(self, cx, cy, r, start_deg, end_deg, val=0, thickness=1):
        """Draw arc from start_deg to end_deg."""
        steps = max(100, int(abs(end_deg - start_deg) * 2))
        for i in range(steps + 1):
            a = math.radians(start_deg + (end_deg - start_deg) * i / steps)
            x = int(cx + r * math.cos(a))
            y = int(cy + r * math.sin(a))
            for t in range(-(thickness//2), (thickness+1)//2):
                self.set_pixel(x + t, y, val)
                self.set_pixel(x, y + t, val)
    
    def draw_ellipse(self, cx, cy, rx, ry, val=0, thickness=1, rotation=0):
        """Draw ellipse outline with optional rotation."""
        steps = max(200, int((rx + ry) * 4))
        cos_r = math.cos(rotation)
        sin_r = math.sin(rotation)
        for i in range(steps):
            a = 2 * math.pi * i / steps
            px = rx * math.cos(a)
            py = ry * math.sin(a)
            x = int(cx + px * cos_r - py * sin_r)
            y = int(cy + px * sin_r + py * cos_r)
            for t in range(-(thickness//2), (thickness+1)//2):
                self.set_pixel(x + t, y, val)
                self.set_pixel(x, y + t, val)
    
    def draw_bezier(self, points, val=0, thickness=1, steps=200):
        """Draw cubic bezier curve."""
        prev_x, prev_y = None, None
        for i in range(steps + 1):
            t = i / steps
            t2 = t * t
            t3 = t2 * t
            mt = 1 - t
            mt2 = mt * mt
            mt3 = mt2 * mt
            
            x = int(mt3 * points[0][0] + 3 * mt2 * t * points[1][0] + 
                    3 * mt * t2 * points[2][0] + t3 * points[3][0])
            y = int(mt3 * points[0][1] + 3 * mt2 * t * points[1][1] + 
                    3 * mt * t2 * points[2][1] + t3 * points[3][1])
            
            if prev_x is not None:
                self.draw_line(prev_x, prev_y, x, y, val, thickness)
            prev_x, prev_y = x, y
    
    def draw_text(self, x, y, text, val=0, scale=1):
        """Draw simple bitmap text (basic font)."""
        # Simple 5x7 font for basic characters
        font = {
            'A': ['01110', '10001', '10001', '11111', '10001', '10001', '10001'],
            'B': ['11110', '10001', '10001', '11110', '10001', '10001', '11110'],
            'C': ['01110', '10001', '10000', '10000', '10000', '10001', '01110'],
            'D': ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
            'E': ['11111', '10000', '10000', '11110', '10000', '10000', '11111'],
            'F': ['11111', '10000', '10000', '11110', '10000', '10000', '10000'],
            'G': ['01110', '10001', '10000', '10111', '10001', '10001', '01110'],
            'H': ['10001', '10001', '10001', '11111', '10001', '10001', '10001'],
            'I': ['01110', '00100', '00100', '00100', '00100', '00100', '01110'],
            'L': ['10000', '10000', '10000', '10000', '10000', '10000', '11111'],
            'M': ['10001', '11011', '10101', '10101', '10001', '10001', '10001'],
            'N': ['10001', '11001', '10101', '10011', '10001', '10001', '10001'],
            'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'],
            'P': ['11110', '10001', '10001', '11110', '10000', '10000', '10000'],
            'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
            'S': ['01110', '10001', '10000', '01110', '00001', '10001', '01110'],
            'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
            'U': ['10001', '10001', '10001', '10001', '10001', '10001', '01110'],
            'V': ['10001', '10001', '10001', '10001', '01010', '01010', '00100'],
            'W': ['10001', '10001', '10001', '10101', '10101', '11011', '10001'],
            'X': ['10001', '10001', '01010', '00100', '01010', '10001', '10001'],
            'Y': ['10001', '10001', '01010', '00100', '00100', '00100', '00100'],
            'Z': ['11111', '00001', '00010', '00100', '01000', '10000', '11111'],
            '0': ['01110', '10001', '10011', '10101', '11001', '10001', '01110'],
            '1': ['00100', '01100', '00100', '00100', '00100', '00100', '01110'],
            '2': ['01110', '10001', '00001', '00110', '01000', '10000', '11111'],
            '3': ['01110', '10001', '00001', '00110', '00001', '10001', '01110'],
            '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'],
            '5': ['11111', '10000', '11110', '00001', '00001', '10001', '01110'],
            ' ': ['00000', '00000', '00000', '00000', '00000', '00000', '00000'],
            '-': ['00000', '00000', '00000', '11111', '00000', '00000', '00000'],
            ':': ['00000', '00100', '00100', '00000', '00100', '00100', '00000'],
            '.': ['00000', '00000', '00000', '00000', '00000', '01100', '01100'],
            '(': ['00010', '00100', '01000', '01000', '01000', '00100', '00010'],
            ')': ['01000', '00100', '00010', '00010', '00010', '00100', '01000'],
            ',': ['00000', '00000', '00000', '00000', '00000', '00100', '01000'],
        }
        
        cx = x
        for ch in text.upper():
            if ch in font:
                for row_idx, row in enumerate(font[ch]):
                    for col_idx, bit in enumerate(row):
                        if bit == '1':
                            for sy in range(scale):
                                for sx in range(scale):
                                    self.set_pixel(cx + col_idx * scale + sx, 
                                                   y + row_idx * scale + sy, val)
            cx += 6 * scale
    
    def fill_rect(self, x0, y0, x1, y1, val):
        """Fill a rectangle."""
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                self.set_pixel(x, y, val)
    
    def draw_rect(self, x0, y0, x1, y1, val=0, thickness=1):
        """Draw rectangle outline."""
        self.draw_line(x0, y0, x1, y0, val, thickness)
        self.draw_line(x1, y0, x1, y1, val, thickness)
        self.draw_line(x1, y1, x0, y1, val, thickness)
        self.draw_line(x0, y1, x0, y0, val, thickness)


# ============================================================================
# MESH GENERATION FUNCTIONS
# ============================================================================

def generate_boundary_layer_lines(canvas, profile_points, num_layers, first_layer, 
                                   growth_ratio, normal_dir='outward', val=180):
    """Generate boundary layer mesh lines along a profile."""
    for layer in range(num_layers):
        thickness = first_layer * (growth_ratio ** layer)
        offset = sum(first_layer * (growth_ratio ** k) for k in range(layer + 1))
        
        # Draw offset curve
        for i in range(len(profile_points) - 1):
            x0, y0 = profile_points[i]
            x1, y1 = profile_points[i + 1]
            
            # Calculate normal
            dx = x1 - x0
            dy = y1 - y0
            length = math.sqrt(dx*dx + dy*dy)
            if length < 0.1:
                continue
            
            if normal_dir == 'outward':
                nx = -dy / length
                ny = dx / length
            else:
                nx = dy / length
                ny = -dx / length
            
            ox0 = int(x0 + nx * offset)
            oy0 = int(y0 + ny * offset)
            ox1 = int(x1 + nx * offset)
            oy1 = int(y1 + ny * offset)
            
            # Lighter lines for boundary layer
            line_val = 180 + min(60, layer * 3)
            canvas.draw_line(ox0, oy0, ox1, oy1, line_val, 1)


def draw_triangular_mesh(canvas, x0, y0, x1, y1, density=20, val=200):
    """Draw triangular mesh pattern in a rectangular region."""
    dx = (x1 - x0) / density
    dy = (y1 - y0) / density
    
    for i in range(density + 1):
        for j in range(density + 1):
            px = int(x0 + i * dx)
            py = int(y0 + j * dy)
            
            # Draw cell edges (triangular)
            if i < density and j < density:
                px2 = int(x0 + (i+1) * dx)
                py2 = int(y0 + (j+1) * dy)
                canvas.draw_line(px, py, px2, py, val, 1)
                canvas.draw_line(px, py, px, py2, val, 1)
                canvas.draw_line(px, py, px2, py2, val, 1)
            
            if i < density:
                px2 = int(x0 + (i+1) * dx)
                canvas.draw_line(px, py, px2, py, val, 1)
            if j < density:
                py2 = int(y0 + (j+1) * dy)
                canvas.draw_line(px, py, px, py2, val, 1)


def draw_structured_quad_mesh(canvas, profile_points, num_layers, first_layer,
                               growth_ratio, normal_dir='outward', mesh_color=190):
    """Draw structured quadrilateral boundary layer mesh."""
    # Generate layer offsets
    offsets = []
    for layer in range(num_layers + 1):
        if layer == 0:
            offsets.append(0)
        else:
            offsets.append(sum(first_layer * (growth_ratio ** k) for k in range(layer)))
    
    # Draw radial lines (connecting layers)
    step = max(1, len(profile_points) // 40)
    for i in range(0, len(profile_points) - 1, step):
        x0, y0 = profile_points[i]
        x1, y1 = profile_points[min(i+1, len(profile_points)-1)]
        
        dx = x1 - x0
        dy = y1 - y0
        length = math.sqrt(dx*dx + dy*dy)
        if length < 0.1:
            continue
        
        if normal_dir == 'outward':
            nx = -dy / length
            ny = dx / length
        else:
            nx = dy / length
            ny = -dx / length
        
        # Draw radial line from surface to outer boundary layer
        sx = int(x0)
        sy = int(y0)
        ex = int(x0 + nx * offsets[-1])
        ey = int(y0 + ny * offsets[-1])
        canvas.draw_line(sx, sy, ex, ey, mesh_color, 1)
    
    # Draw circumferential lines (layer boundaries)
    for layer in range(num_layers + 1):
        offset = offsets[layer]
        for i in range(len(profile_points) - 1):
            x0, y0 = profile_points[i]
            x1, y1 = profile_points[i + 1]
            
            dx = x1 - x0
            dy = y1 - y0
            length = math.sqrt(dx*dx + dy*dy)
            if length < 0.1:
                continue
            
            if normal_dir == 'outward':
                nx0 = -dy / length
                ny0 = dx / length
            else:
                nx0 = dy / length
                ny0 = -dx / length
            
            ox0 = int(x0 + nx0 * offset)
            oy0 = int(y0 + ny0 * offset)
            ox1 = int(x1 + nx0 * offset)
            oy1 = int(y1 + ny0 * offset)
            
            # Inner layers are darker (finer mesh)
            line_val = mesh_color - min(40, layer * 2)
            canvas.draw_line(ox0, oy0, ox1, oy1, line_val, 1)


# ============================================================================
# AIRFOIL/BLADE PROFILE GENERATION
# ============================================================================

def generate_airfoil_points(cx, cy, chord, thickness_ratio=0.12, num_points=200, angle=0):
    """Generate NACA-like airfoil profile points."""
    points_upper = []
    points_lower = []
    
    cos_a = math.cos(math.radians(angle))
    sin_a = math.sin(math.radians(angle))
    
    for i in range(num_points + 1):
        t = i / num_points
        x = t * chord
        
        # NACA 4-digit thickness distribution
        yt = 5 * thickness_ratio * chord * (
            0.2969 * math.sqrt(t + 1e-10) - 0.1260 * t - 
            0.3516 * t**2 + 0.2843 * t**3 - 0.1015 * t**4
        )
        
        # Apply rotation
        xu = x * cos_a - yt * sin_a + cx
        yu = x * sin_a + yt * cos_a + cy
        xl = x * cos_a + yt * sin_a + cx
        yl = x * sin_a - yt * cos_a + cy
        
        points_upper.append((xu, yu))
        points_lower.append((xl, yl))
    
    # Combine: upper surface forward, lower surface backward
    return points_upper + points_lower[::-1]


def generate_slot_profile(cx, cy, slot_width, slot_height, slot_type='A'):
    """Generate slot geometry points for different configurations."""
    points = []
    
    if slot_type == 'A':
        # Straight slot (perpendicular)
        hw = slot_width / 2
        points = [
            (cx - hw, cy - slot_height/2),
            (cx - hw, cy + slot_height/2),
            (cx + hw, cy + slot_height/2),
            (cx + hw, cy - slot_height/2),
        ]
    elif slot_type == 'B':
        # Angled slot (30 degrees)
        angle = math.radians(30)
        hw = slot_width / 2
        dx = slot_height * math.sin(angle)
        points = [
            (cx - hw, cy - slot_height/2),
            (cx - hw + dx, cy + slot_height/2),
            (cx + hw + dx, cy + slot_height/2),
            (cx + hw, cy - slot_height/2),
        ]
    elif slot_type == 'C':
        # Curved slot (S-shape)
        for i in range(50):
            t = i / 49
            x = cx - slot_width/2 + slot_width * math.sin(t * math.pi * 0.3)
            y = cy - slot_height/2 + t * slot_height
            points.append((x, y))
        for i in range(50):
            t = i / 49
            x = cx + slot_width/2 + slot_width * math.sin(t * math.pi * 0.3)
            y = cy + slot_height/2 - t * slot_height
            points.append((x, y))
    elif slot_type == 'D':
        # Teardrop/converging slot
        for i in range(100):
            t = i / 99
            angle = 2 * math.pi * t
            rx = slot_width / 2 * (1 + 0.3 * math.cos(angle))
            ry = slot_height / 2
            x = cx + rx * math.cos(angle)
            y = cy + ry * math.sin(angle)
            points.append((x, y))
    
    return points


# ============================================================================
# FIGURE GENERATION
# ============================================================================

def create_figure1_leading_edge_mesh(output_dir):
    """Figure 1: Enlarged view of mesh near leading edge."""
    W, H = 1200, 900
    canvas = Canvas(W, H)
    
    # Title
    canvas.draw_text(20, 15, "LEADING EDGE - REFINED MESH DETAIL", 0, 2)
    canvas.draw_text(20, 45, "FINE MESH: 20 INFLATION LAYERS, FIRST LAYER 0.005MM, GR 1.15", 0, 1)
    
    # Draw leading edge circle (large scale view)
    le_cx, le_cy = 400, 450
    le_radius = 80
    
    # Draw airfoil leading edge region (enlarged)
    upper_points = []
    lower_points = []
    for i in range(150):
        angle = math.radians(-90 + 180 * i / 149)
        x = le_cx + le_radius * math.cos(angle)
        y = le_cy - le_radius * math.sin(angle)
        upper_points.append((x, y))
    
    for i in range(150):
        angle = math.radians(-90 + 180 * i / 149)
        x = le_cx + le_radius * math.cos(angle)
        y = le_cy + le_radius * math.sin(angle)
        lower_points.append((x, y))
    
    # Draw airfoil surface (thick line)
    for i in range(len(upper_points) - 1):
        canvas.draw_line(int(upper_points[i][0]), int(upper_points[i][1]),
                        int(upper_points[i+1][0]), int(upper_points[i+1][1]), 0, 3)
    for i in range(len(lower_points) - 1):
        canvas.draw_line(int(lower_points[i][0]), int(lower_points[i][1]),
                        int(lower_points[i+1][0]), int(lower_points[i+1][1]), 0, 3)
    
    # Draw boundary layer mesh (structured quad cells)
    num_layers = 20
    first_layer = 3.0  # pixels (representing 0.005mm scaled)
    growth_ratio = 1.15
    
    # Draw inflation layers around leading edge
    for layer in range(num_layers):
        offset = sum(first_layer * (growth_ratio ** k) for k in range(layer + 1))
        layer_color = 150 + min(80, layer * 4)
        
        # Upper surface layers
        for i in range(len(upper_points) - 1):
            x0, y0 = upper_points[i]
            x1, y1 = upper_points[i + 1]
            dx = x1 - x0
            dy = y1 - y0
            length = math.sqrt(dx*dx + dy*dy)
            if length < 0.5:
                continue
            nx = -dy / length
            ny = dx / length
            
            ox0 = int(x0 + nx * offset)
            oy0 = int(y0 + ny * offset)
            ox1 = int(x1 + nx * offset)
            oy1 = int(y1 + ny * offset)
            canvas.draw_line(ox0, oy0, ox1, oy1, layer_color, 1)
        
        # Lower surface layers
        for i in range(len(lower_points) - 1):
            x0, y0 = lower_points[i]
            x1, y1 = lower_points[i + 1]
            dx = x1 - x0
            dy = y1 - y0
            length = math.sqrt(dx*dx + dy*dy)
            if length < 0.5:
                continue
            nx = dy / length
            ny = -dx / length
            
            ox0 = int(x0 + nx * offset)
            oy0 = int(y0 + ny * offset)
            ox1 = int(x1 + nx * offset)
            oy1 = int(y1 + ny * offset)
            canvas.draw_line(ox0, oy0, ox1, oy1, layer_color, 1)
    
    # Draw radial lines (cell divisions)
    step = 5
    for i in range(0, len(upper_points) - 1, step):
        x0, y0 = upper_points[i]
        x1, y1 = upper_points[min(i+1, len(upper_points)-1)]
        dx = x1 - x0
        dy = y1 - y0
        length = math.sqrt(dx*dx + dy*dy)
        if length < 0.5:
            continue
        nx = -dy / length
        ny = dx / length
        total_offset = sum(first_layer * (growth_ratio ** k) for k in range(num_layers))
        canvas.draw_line(int(x0), int(y0), int(x0 + nx * total_offset), 
                        int(y0 + ny * total_offset), 180, 1)
    
    for i in range(0, len(lower_points) - 1, step):
        x0, y0 = lower_points[i]
        x1, y1 = lower_points[min(i+1, len(lower_points)-1)]
        dx = x1 - x0
        dy = y1 - y0
        length = math.sqrt(dx*dx + dy*dy)
        if length < 0.5:
            continue
        nx = dy / length
        ny = -dx / length
        total_offset = sum(first_layer * (growth_ratio ** k) for k in range(num_layers))
        canvas.draw_line(int(x0), int(y0), int(x0 + nx * total_offset),
                        int(y0 + ny * total_offset), 180, 1)
    
    # Unstructured mesh in far field (right side)
    draw_triangular_mesh(canvas, 700, 100, 1150, 850, density=15, val=210)
    
    # Add annotation
    canvas.draw_text(700, 870, "UNSTRUCTURED FAR-FIELD", 0, 1)
    canvas.draw_text(200, 870, "STRUCTURED BL MESH", 0, 1)
    
    # Draw zoom indicator box
    canvas.draw_rect(50, 80, 650, 860, 0, 2)
    canvas.draw_text(55, 65, "ENLARGED VIEW", 0, 1)
    
    write_tiff(os.path.join(output_dir, "Figure_Mesh_1_Leading_Edge.tiff"), 
               canvas.pixels, W, H)
    print("  Created: Figure_Mesh_1_Leading_Edge.tiff")


def create_figure2_trailing_edge_mesh(output_dir):
    """Figure 2: Enlarged view of mesh near trailing edge."""
    W, H = 1200, 900
    canvas = Canvas(W, H)
    
    canvas.draw_text(20, 15, "TRAILING EDGE - REFINED MESH DETAIL", 0, 2)
    canvas.draw_text(20, 45, "FINE MESH: 20 INFLATION LAYERS, FIRST LAYER 0.005MM, GR 1.15", 0, 1)
    
    # Trailing edge (sharp, thin profile converging)
    te_x = 900
    te_y = 450
    
    # Upper and lower surfaces converging to trailing edge
    upper_points = []
    lower_points = []
    
    for i in range(200):
        t = i / 199
        x = 100 + t * 800
        # Thickness decreases toward trailing edge
        half_thick = 120 * (1 - t) ** 0.6 * (1 + 0.2 * t)
        if t > 0.8:
            half_thick *= (1 - t) / 0.2  # Sharp close at TE
        upper_points.append((x, te_y - half_thick))
        lower_points.append((x, te_y + half_thick))
    
    # Draw surfaces
    for i in range(len(upper_points) - 1):
        canvas.draw_line(int(upper_points[i][0]), int(upper_points[i][1]),
                        int(upper_points[i+1][0]), int(upper_points[i+1][1]), 0, 3)
    for i in range(len(lower_points) - 1):
        canvas.draw_line(int(lower_points[i][0]), int(lower_points[i][1]),
                        int(lower_points[i+1][0]), int(lower_points[i+1][1]), 0, 3)
    
    # Draw structured boundary layer mesh near TE
    num_layers = 20
    first_layer = 2.5
    growth_ratio = 1.15
    
    # Focus on trailing edge region (last 40% of chord)
    start_idx = 120
    
    for layer in range(num_layers):
        offset = sum(first_layer * (growth_ratio ** k) for k in range(layer + 1))
        layer_color = 150 + min(80, layer * 4)
        
        for i in range(start_idx, len(upper_points) - 1):
            x0, y0 = upper_points[i]
            x1, y1 = upper_points[i + 1]
            dx = x1 - x0
            dy = y1 - y0
            length = math.sqrt(dx*dx + dy*dy)
            if length < 0.3:
                continue
            nx = -dy / length
            ny = dx / length
            ox0 = int(x0 + nx * offset)
            oy0 = int(y0 + ny * offset)
            ox1 = int(x1 + nx * offset)
            oy1 = int(y1 + ny * offset)
            canvas.draw_line(ox0, oy0, ox1, oy1, layer_color, 1)
        
        for i in range(start_idx, len(lower_points) - 1):
            x0, y0 = lower_points[i]
            x1, y1 = lower_points[i + 1]
            dx = x1 - x0
            dy = y1 - y0
            length = math.sqrt(dx*dx + dy*dy)
            if length < 0.3:
                continue
            nx = dy / length
            ny = -dx / length
            ox0 = int(x0 + nx * offset)
            oy0 = int(y0 + ny * offset)
            ox1 = int(x1 + nx * offset)
            oy1 = int(y1 + ny * offset)
            canvas.draw_line(ox0, oy0, ox1, oy1, layer_color, 1)
    
    # Radial lines
    step = 8
    total_offset = sum(first_layer * (growth_ratio ** k) for k in range(num_layers))
    for i in range(start_idx, len(upper_points) - 1, step):
        x0, y0 = upper_points[i]
        x1, y1 = upper_points[min(i+1, len(upper_points)-1)]
        dx = x1 - x0
        dy = y1 - y0
        length = math.sqrt(dx*dx + dy*dy)
        if length < 0.3:
            continue
        nx = -dy / length
        ny = dx / length
        canvas.draw_line(int(x0), int(y0), int(x0 + nx * total_offset),
                        int(y0 + ny * total_offset), 180, 1)
    
    for i in range(start_idx, len(lower_points) - 1, step):
        x0, y0 = lower_points[i]
        x1, y1 = lower_points[min(i+1, len(lower_points)-1)]
        dx = x1 - x0
        dy = y1 - y0
        length = math.sqrt(dx*dx + dy*dy)
        if length < 0.3:
            continue
        nx = dy / length
        ny = -dx / length
        canvas.draw_line(int(x0), int(y0), int(x0 + nx * total_offset),
                        int(y0 + ny * total_offset), 180, 1)
    
    # Wake region mesh (downstream of TE)
    for i in range(20):
        x = te_x + i * 15
        y_spread = 5 + i * 4
        canvas.draw_line(x, te_y - y_spread, x, te_y + y_spread, 200, 1)
    for i in range(10):
        y = te_y - 80 + i * 16
        canvas.draw_line(te_x, y, te_x + 280, y, 200, 1)
    
    canvas.draw_text(920, 870, "WAKE REGION", 0, 1)
    canvas.draw_text(400, 870, "TRAILING EDGE BL REFINEMENT", 0, 1)
    canvas.draw_rect(50, 80, 1150, 860, 0, 2)
    
    write_tiff(os.path.join(output_dir, "Figure_Mesh_2_Trailing_Edge.tiff"),
               canvas.pixels, W, H)
    print("  Created: Figure_Mesh_2_Trailing_Edge.tiff")


def create_figure3_slot_edge_mesh(output_dir):
    """Figure 3: Mesh refinement around slot edges."""
    W, H = 1400, 1000
    canvas = Canvas(W, H)
    
    canvas.draw_text(20, 15, "SLOT EDGE MESH REFINEMENT - ALL CONFIGURATIONS", 0, 2)
    canvas.draw_text(20, 45, "FINE MESH: 20 INFLATION LAYERS, GROWTH RATIO 1.15", 0, 1)
    
    # Four quadrants for Slots A-D
    configs = [
        ('SLOT A - STRAIGHT', 350, 300),
        ('SLOT B - ANGLED 30DEG', 1050, 300),
        ('SLOT C - CURVED', 350, 700),
        ('SLOT D - CONVERGING', 1050, 700),
    ]
    
    for idx, (label, cx, cy) in enumerate(configs):
        # Draw slot opening with mesh
        slot_w = 30
        slot_h = 150
        
        canvas.draw_text(cx - 150, cy - 220, label, 0, 2)
        
        if idx == 0:  # Straight slot
            # Draw slot walls
            canvas.draw_line(cx - slot_w, cy - slot_h//2, cx - slot_w, cy + slot_h//2, 0, 3)
            canvas.draw_line(cx + slot_w, cy - slot_h//2, cx + slot_w, cy + slot_h//2, 0, 3)
            # Rounded edges
            canvas.draw_arc(cx - slot_w, cy - slot_h//2, 10, 90, 270, 0, 2)
            canvas.draw_arc(cx + slot_w, cy - slot_h//2, 10, 270, 450, 0, 2)
            canvas.draw_arc(cx - slot_w, cy + slot_h//2, 10, 90, 270, 0, 2)
            canvas.draw_arc(cx + slot_w, cy + slot_h//2, 10, 270, 450, 0, 2)
            
            # BL mesh inside slot
            num_layers = 15
            first_layer = 1.5
            gr = 1.15
            for layer in range(num_layers):
                offset = sum(first_layer * (gr ** k) for k in range(layer + 1))
                if offset > slot_w - 2:
                    break
                lc = 160 + min(70, layer * 5)
                # Left wall
                canvas.draw_line(int(cx - slot_w + offset), cy - slot_h//2,
                               int(cx - slot_w + offset), cy + slot_h//2, lc, 1)
                # Right wall
                canvas.draw_line(int(cx + slot_w - offset), cy - slot_h//2,
                               int(cx + slot_w - offset), cy + slot_h//2, lc, 1)
            
            # Horizontal lines (cell divisions)
            for j in range(0, slot_h, 8):
                canvas.draw_line(cx - slot_w, cy - slot_h//2 + j,
                               cx + slot_w, cy - slot_h//2 + j, 200, 1)
        
        elif idx == 1:  # Angled slot
            angle = math.radians(30)
            dx = slot_h * math.sin(angle) / 2
            # Draw angled slot walls
            points_l = [(cx - slot_w - dx, cy - slot_h//2), (cx - slot_w + dx, cy + slot_h//2)]
            points_r = [(cx + slot_w - dx, cy - slot_h//2), (cx + slot_w + dx, cy + slot_h//2)]
            canvas.draw_line(int(points_l[0][0]), int(points_l[0][1]),
                           int(points_l[1][0]), int(points_l[1][1]), 0, 3)
            canvas.draw_line(int(points_r[0][0]), int(points_r[0][1]),
                           int(points_r[1][0]), int(points_r[1][1]), 0, 3)
            
            # BL mesh along angled walls
            num_layers = 15
            first_layer = 1.5
            gr = 1.15
            cos_a = math.cos(angle)
            for layer in range(num_layers):
                offset = sum(first_layer * (gr ** k) for k in range(layer + 1))
                if offset > slot_w - 2:
                    break
                lc = 160 + min(70, layer * 5)
                # Offset lines parallel to walls
                canvas.draw_line(int(points_l[0][0] + offset * cos_a), int(points_l[0][1]),
                               int(points_l[1][0] + offset * cos_a), int(points_l[1][1]), lc, 1)
                canvas.draw_line(int(points_r[0][0] - offset * cos_a), int(points_r[0][1]),
                               int(points_r[1][0] - offset * cos_a), int(points_r[1][1]), lc, 1)
            
            # Cross lines
            for j in range(0, slot_h, 8):
                t = j / slot_h
                lx = points_l[0][0] + t * (points_l[1][0] - points_l[0][0])
                ly = points_l[0][1] + t * (points_l[1][1] - points_l[0][1])
                rx = points_r[0][0] + t * (points_r[1][0] - points_r[0][0])
                ry = points_r[0][1] + t * (points_r[1][1] - points_r[0][1])
                canvas.draw_line(int(lx), int(ly), int(rx), int(ry), 200, 1)
        
        elif idx == 2:  # Curved slot
            # S-shaped slot
            slot_points_l = []
            slot_points_r = []
            for i in range(100):
                t = i / 99
                curve_x = 25 * math.sin(t * math.pi)
                y = cy - slot_h//2 + t * slot_h
                slot_points_l.append((cx - slot_w + curve_x, y))
                slot_points_r.append((cx + slot_w + curve_x, y))
            
            for i in range(len(slot_points_l) - 1):
                canvas.draw_line(int(slot_points_l[i][0]), int(slot_points_l[i][1]),
                               int(slot_points_l[i+1][0]), int(slot_points_l[i+1][1]), 0, 3)
                canvas.draw_line(int(slot_points_r[i][0]), int(slot_points_r[i][1]),
                               int(slot_points_r[i+1][0]), int(slot_points_r[i+1][1]), 0, 3)
            
            # BL mesh
            num_layers = 12
            first_layer = 1.5
            gr = 1.15
            for layer in range(num_layers):
                offset = sum(first_layer * (gr ** k) for k in range(layer + 1))
                if offset > slot_w - 3:
                    break
                lc = 160 + min(70, layer * 5)
                for i in range(0, len(slot_points_l) - 1, 2):
                    x0, y0 = slot_points_l[i]
                    x1, y1 = slot_points_l[min(i+1, len(slot_points_l)-1)]
                    canvas.draw_line(int(x0 + offset), int(y0), int(x1 + offset), int(y1), lc, 1)
                    
                    x0, y0 = slot_points_r[i]
                    x1, y1 = slot_points_r[min(i+1, len(slot_points_r)-1)]
                    canvas.draw_line(int(x0 - offset), int(y0), int(x1 - offset), int(y1), lc, 1)
            
            # Cross lines
            for i in range(0, 100, 5):
                canvas.draw_line(int(slot_points_l[i][0]), int(slot_points_l[i][1]),
                               int(slot_points_r[i][0]), int(slot_points_r[i][1]), 200, 1)
        
        elif idx == 3:  # Converging/teardrop slot
            # Teardrop shape
            td_points = []
            for i in range(200):
                t = 2 * math.pi * i / 199
                # Teardrop parametric
                rx = slot_w * (1 + 0.5 * math.cos(t))
                ry = slot_h // 2
                x = cx + rx * math.cos(t)
                y = cy + ry * math.sin(t) * 0.8
                td_points.append((x, y))
            
            for i in range(len(td_points) - 1):
                canvas.draw_line(int(td_points[i][0]), int(td_points[i][1]),
                               int(td_points[i+1][0]), int(td_points[i+1][1]), 0, 3)
            
            # BL mesh around teardrop
            num_layers = 15
            first_layer = 1.5
            gr = 1.15
            for layer in range(num_layers):
                offset = sum(first_layer * (gr ** k) for k in range(layer + 1))
                lc = 160 + min(70, layer * 5)
                for i in range(len(td_points) - 1):
                    x0, y0 = td_points[i]
                    x1, y1 = td_points[min(i+1, len(td_points)-1)]
                    dx = x1 - x0
                    dy = y1 - y0
                    length = math.sqrt(dx*dx + dy*dy)
                    if length < 0.3:
                        continue
                    nx = -dy / length
                    ny = dx / length
                    ox0 = int(x0 + nx * offset)
                    oy0 = int(y0 + ny * offset)
                    ox1 = int(x1 + nx * offset)
                    oy1 = int(y1 + ny * offset)
                    canvas.draw_line(ox0, oy0, ox1, oy1, lc, 1)
            
            # Radial lines
            total_offset = sum(first_layer * (gr ** k) for k in range(num_layers))
            for i in range(0, len(td_points) - 1, 10):
                x0, y0 = td_points[i]
                x1, y1 = td_points[min(i+1, len(td_points)-1)]
                dx = x1 - x0
                dy = y1 - y0
                length = math.sqrt(dx*dx + dy*dy)
                if length < 0.3:
                    continue
                nx = -dy / length
                ny = dx / length
                canvas.draw_line(int(x0), int(y0), int(x0 + nx * total_offset),
                               int(y0 + ny * total_offset), 190, 1)
    
    # Draw separator lines
    canvas.draw_line(700, 80, 700, 950, 0, 1)
    canvas.draw_line(50, 500, 1350, 500, 0, 1)
    canvas.draw_rect(50, 80, 1350, 950, 0, 2)
    
    write_tiff(os.path.join(output_dir, "Figure_Mesh_3_Slot_Edge_Refinement.tiff"),
               canvas.pixels, W, H)
    print("  Created: Figure_Mesh_3_Slot_Edge_Refinement.tiff")


def create_figure4_blade_tip_mesh(output_dir):
    """Figure 4: Mesh near blade tip with tip clearance."""
    W, H = 1200, 900
    canvas = Canvas(W, H)
    
    canvas.draw_text(20, 15, "BLADE TIP - MESH REFINEMENT", 0, 2)
    canvas.draw_text(20, 45, "TIP CLEARANCE REGION WITH INFLATION LAYERS", 0, 1)
    
    # Draw blade tip cross-section
    tip_y = 500
    blade_top = 300
    blade_bot = 700
    casing_y = 250  # Casing wall above tip
    
    # Blade body
    canvas.fill_rect(200, blade_top, 800, blade_bot, 240)
    canvas.draw_rect(200, blade_top, 800, blade_bot, 0, 3)
    
    # Rounded tip
    canvas.draw_arc(500, blade_top, 300, 0, 180, 0, 3)
    
    # Casing wall
    canvas.draw_line(50, casing_y, 1150, casing_y, 0, 3)
    canvas.draw_text(50, 230, "CASING WALL", 0, 1)
    
    # Tip clearance gap mesh
    gap = blade_top - casing_y  # pixels
    num_layers = 15
    first_layer = 1.2
    gr = 1.15
    
    # BL on casing wall (downward)
    for layer in range(num_layers):
        offset = sum(first_layer * (gr ** k) for k in range(layer + 1))
        if offset > gap * 0.4:
            break
        lc = 160 + min(70, layer * 5)
        canvas.draw_line(200, int(casing_y + offset), 800, int(casing_y + offset), lc, 1)
    
    # BL on blade tip (upward from blade surface)
    for layer in range(num_layers):
        offset = sum(first_layer * (gr ** k) for k in range(layer + 1))
        if offset > gap * 0.4:
            break
        lc = 160 + min(70, layer * 5)
        # Flat part of tip
        canvas.draw_line(200, int(blade_top - offset), 800, int(blade_top - offset), lc, 1)
    
    # Vertical cell divisions in gap
    for x in range(200, 800, 15):
        canvas.draw_line(x, casing_y, x, blade_top, 200, 1)
    
    # Mesh on blade sides
    num_layers_side = 20
    for layer in range(num_layers_side):
        offset = sum(first_layer * (gr ** k) for k in range(layer + 1))
        if offset > 150:
            break
        lc = 160 + min(70, layer * 4)
        # Left side
        canvas.draw_line(int(200 - offset), blade_top, int(200 - offset), blade_bot, lc, 1)
        # Right side  
        canvas.draw_line(int(800 + offset), blade_top, int(800 + offset), blade_bot, lc, 1)
    
    # Horizontal lines on sides
    for y in range(blade_top, blade_bot, 12):
        total_offset = sum(first_layer * (gr ** k) for k in range(min(num_layers_side, 20)))
        canvas.draw_line(int(200 - total_offset), y, 200, y, 200, 1)
        canvas.draw_line(800, y, int(800 + total_offset), y, 200, 1)
    
    # Annotations
    canvas.draw_text(850, 270, "TIP CLEARANCE GAP", 0, 1)
    canvas.draw_line(840, 275, 810, int((casing_y + blade_top)/2), 0, 1)
    
    canvas.draw_text(850, 500, "BLADE BODY", 0, 2)
    canvas.draw_text(50, 400, "BL MESH", 0, 1)
    
    # Draw dimension arrow for gap
    canvas.draw_line(180, casing_y, 180, blade_top, 0, 1)
    canvas.draw_line(175, casing_y, 185, casing_y, 0, 2)
    canvas.draw_line(175, blade_top, 185, blade_top, 0, 2)
    
    canvas.draw_rect(50, 80, 1150, 860, 0, 2)
    
    write_tiff(os.path.join(output_dir, "Figure_Mesh_4_Blade_Tip.tiff"),
               canvas.pixels, W, H)
    print("  Created: Figure_Mesh_4_Blade_Tip.tiff")


def create_figure5_slot_configs(output_dir):
    """Figure 5: Representative mesh for each slot configuration (A-D) 
    showing the full blade profile with slot."""
    W, H = 1600, 1200
    canvas = Canvas(W, H)
    
    canvas.draw_text(20, 15, "REPRESENTATIVE MESH - SLOTTED BLADE CONFIGURATIONS A-D", 0, 2)
    canvas.draw_text(20, 45, "FINE MESH: 1024000 ELEMENTS, 310000 BL ELEMENTS, 20 LAYERS", 0, 1)
    
    configs = [
        ('(A) STRAIGHT SLOT', 400, 300),
        ('(B) ANGLED SLOT', 1200, 300),
        ('(C) CURVED SLOT', 400, 900),
        ('(D) CONVERGING SLOT', 1200, 900),
    ]
    
    for idx, (label, cx, cy) in enumerate(configs):
        canvas.draw_text(cx - 180, cy - 260, label, 0, 2)
        
        # Draw airfoil profile
        chord = 300
        airfoil_points = generate_airfoil_points(cx - chord//2, cy, chord, 0.15, 150)
        
        # Draw airfoil outline
        for i in range(len(airfoil_points) - 1):
            canvas.draw_line(int(airfoil_points[i][0]), int(airfoil_points[i][1]),
                           int(airfoil_points[i+1][0]), int(airfoil_points[i+1][1]), 0, 2)
        
        # Draw boundary layer mesh around airfoil
        num_layers = 12
        first_layer = 2.0
        gr = 1.15
        
        # Simplified BL visualization (every other point for performance)
        step = 4
        for layer in range(num_layers):
            offset = sum(first_layer * (gr ** k) for k in range(layer + 1))
            lc = 160 + min(70, layer * 5)
            
            for i in range(0, len(airfoil_points) - 1, step):
                x0, y0 = airfoil_points[i]
                x1, y1 = airfoil_points[min(i + step, len(airfoil_points) - 1)]
                dx = x1 - x0
                dy = y1 - y0
                length = math.sqrt(dx*dx + dy*dy)
                if length < 0.5:
                    continue
                nx = -dy / length
                ny = dx / length
                ox0 = int(x0 + nx * offset)
                oy0 = int(y0 + ny * offset)
                ox1 = int(x1 + nx * offset)
                oy1 = int(y1 + ny * offset)
                canvas.draw_line(ox0, oy0, ox1, oy1, lc, 1)
        
        # Draw slot on airfoil (at ~40% chord)
        slot_x = cx - chord//2 + int(0.4 * chord)
        slot_w = 8
        slot_h = 40
        
        if idx == 0:  # Straight
            canvas.draw_line(slot_x - slot_w, cy - slot_h, slot_x - slot_w, cy + slot_h, 40, 2)
            canvas.draw_line(slot_x + slot_w, cy - slot_h, slot_x + slot_w, cy + slot_h, 40, 2)
            # Mesh inside slot
            for layer in range(8):
                off = 1 + layer * 1.0
                if off > slot_w - 1:
                    break
                canvas.draw_line(int(slot_x - slot_w + off), cy - slot_h,
                               int(slot_x - slot_w + off), cy + slot_h, 180, 1)
                canvas.draw_line(int(slot_x + slot_w - off), cy - slot_h,
                               int(slot_x + slot_w - off), cy + slot_h, 180, 1)
            for j in range(-slot_h, slot_h, 5):
                canvas.draw_line(slot_x - slot_w, cy + j, slot_x + slot_w, cy + j, 200, 1)
                
        elif idx == 1:  # Angled
            angle = math.radians(30)
            dx_off = slot_h * math.sin(angle)
            canvas.draw_line(int(slot_x - slot_w), cy - slot_h,
                           int(slot_x - slot_w + dx_off), cy + slot_h, 40, 2)
            canvas.draw_line(int(slot_x + slot_w), cy - slot_h,
                           int(slot_x + slot_w + dx_off), cy + slot_h, 40, 2)
            for layer in range(8):
                off = 1 + layer * 0.9
                if off > slot_w - 1:
                    break
                canvas.draw_line(int(slot_x - slot_w + off), cy - slot_h,
                               int(slot_x - slot_w + dx_off + off), cy + slot_h, 180, 1)
                canvas.draw_line(int(slot_x + slot_w - off), cy - slot_h,
                               int(slot_x + slot_w + dx_off - off), cy + slot_h, 180, 1)
            for j in range(-slot_h, slot_h, 5):
                t = (j + slot_h) / (2 * slot_h)
                x_shift = t * dx_off
                canvas.draw_line(int(slot_x - slot_w + x_shift), cy + j,
                               int(slot_x + slot_w + x_shift), cy + j, 200, 1)
                
        elif idx == 2:  # Curved
            for i in range(80):
                t = i / 79
                curve = 10 * math.sin(t * math.pi)
                y_pos = cy - slot_h + t * 2 * slot_h
                canvas.draw_line(int(slot_x - slot_w + curve), int(y_pos),
                               int(slot_x - slot_w + curve), int(y_pos + 1), 40, 2)
                canvas.draw_line(int(slot_x + slot_w + curve), int(y_pos),
                               int(slot_x + slot_w + curve), int(y_pos + 1), 40, 2)
            # Mesh lines
            for j in range(-slot_h, slot_h, 5):
                t = (j + slot_h) / (2 * slot_h)
                curve = 10 * math.sin(t * math.pi)
                canvas.draw_line(int(slot_x - slot_w + curve), cy + j,
                               int(slot_x + slot_w + curve), cy + j, 200, 1)
                
        elif idx == 3:  # Converging
            # Wider at entry, narrower at exit
            for i in range(80):
                t = i / 79
                w = slot_w * (1.5 - 0.7 * t)
                y_pos = cy - slot_h + t * 2 * slot_h
                canvas.set_pixel(int(slot_x - w), int(y_pos), 40)
                canvas.set_pixel(int(slot_x + w), int(y_pos), 40)
                if i > 0:
                    canvas.draw_line(int(slot_x - w), int(y_pos - 1),
                                   int(slot_x - w), int(y_pos), 40, 2)
                    canvas.draw_line(int(slot_x + w), int(y_pos - 1),
                                   int(slot_x + w), int(y_pos), 40, 2)
            for j in range(-slot_h, slot_h, 5):
                t = (j + slot_h) / (2 * slot_h)
                w = slot_w * (1.5 - 0.7 * t)
                canvas.draw_line(int(slot_x - w), cy + j, int(slot_x + w), cy + j, 200, 1)
    
    # Separator lines
    canvas.draw_line(800, 80, 800, 1150, 0, 1)
    canvas.draw_line(50, 600, 1550, 600, 0, 1)
    canvas.draw_rect(50, 80, 1550, 1150, 0, 2)
    
    write_tiff(os.path.join(output_dir, "Figure_Mesh_5_Slot_Configurations_AD.tiff"),
               canvas.pixels, W, H)
    print("  Created: Figure_Mesh_5_Slot_Configurations_AD.tiff")


def create_figure6_overall_mesh(output_dir):
    """Figure 6: Overall computational domain mesh showing refinement zones."""
    W, H = 1400, 1000
    canvas = Canvas(W, H)
    
    canvas.draw_text(20, 15, "OVERALL COMPUTATIONAL DOMAIN - MESH DISTRIBUTION", 0, 2)
    canvas.draw_text(20, 45, "TOTAL ELEMENTS: 1024000, BL ELEMENTS: 310000", 0, 1)
    
    # Draw outer domain boundary
    canvas.draw_rect(100, 100, 1300, 900, 0, 2)
    
    # Coarse far-field mesh
    far_spacing = 50
    for x in range(100, 1300, far_spacing):
        canvas.draw_line(x, 100, x, 900, 230, 1)
    for y in range(100, 900, far_spacing):
        canvas.draw_line(100, y, 1300, y, 230, 1)
    
    # Medium refinement zone
    canvas.draw_rect(300, 300, 1100, 700, 100, 2)
    med_spacing = 25
    for x in range(300, 1100, med_spacing):
        canvas.draw_line(x, 300, x, 700, 210, 1)
    for y in range(300, 700, med_spacing):
        canvas.draw_line(300, y, 1100, y, 210, 1)
    
    # Fine refinement zone around blade
    canvas.draw_rect(400, 400, 1000, 600, 80, 2)
    fine_spacing = 10
    for x in range(400, 1000, fine_spacing):
        canvas.draw_line(x, 400, x, 600, 190, 1)
    for y in range(400, 600, fine_spacing):
        canvas.draw_line(400, y, 1000, y, 190, 1)
    
    # Draw blade profile in center
    blade_cx, blade_cy = 700, 500
    chord = 350
    airfoil = generate_airfoil_points(blade_cx - chord//2, blade_cy, chord, 0.12, 100)
    for i in range(len(airfoil) - 1):
        canvas.draw_line(int(airfoil[i][0]), int(airfoil[i][1]),
                        int(airfoil[i+1][0]), int(airfoil[i+1][1]), 0, 3)
    
    # Draw BL around blade (simplified)
    for layer in range(10):
        offset = (layer + 1) * 3
        lc = 140 + layer * 8
        for i in range(0, len(airfoil) - 1, 3):
            x0, y0 = airfoil[i]
            x1, y1 = airfoil[min(i+3, len(airfoil)-1)]
            dx = x1 - x0
            dy = y1 - y0
            length = math.sqrt(dx*dx + dy*dy)
            if length < 0.5:
                continue
            nx = -dy / length
            ny = dx / length
            canvas.draw_line(int(x0 + nx * offset), int(y0 + ny * offset),
                           int(x1 + nx * offset), int(y1 + ny * offset), lc, 1)
    
    # Annotations
    canvas.draw_text(110, 110, "FAR-FIELD COARSE MESH", 0, 1)
    canvas.draw_text(310, 310, "MEDIUM REFINEMENT ZONE", 0, 1)
    canvas.draw_text(410, 385, "FINE REFINEMENT ZONE", 0, 1)
    canvas.draw_text(600, 540, "BLADE PROFILE", 0, 1)
    
    # Mesh statistics box
    canvas.fill_rect(950, 750, 1280, 890, 255)
    canvas.draw_rect(950, 750, 1280, 890, 0, 2)
    canvas.draw_text(960, 760, "MESH STATISTICS:", 0, 1)
    canvas.draw_text(960, 780, "TOTAL: 1024000 ELEM", 0, 1)
    canvas.draw_text(960, 795, "BL: 310000 ELEM", 0, 1)
    canvas.draw_text(960, 810, "LAYERS: 20", 0, 1)
    canvas.draw_text(960, 825, "FIRST LAYER: 0.005MM", 0, 1)
    canvas.draw_text(960, 840, "GROWTH: 1.15", 0, 1)
    canvas.draw_text(960, 855, "Y PLUS: LESS 1", 0, 1)
    
    write_tiff(os.path.join(output_dir, "Figure_Mesh_6_Overall_Domain.tiff"),
               canvas.pixels, W, H)
    print("  Created: Figure_Mesh_6_Overall_Domain.tiff")


# ============================================================================
# MAIN
# ============================================================================

def main():
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mesh_figures")
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("GENERATING CFD MESH VISUALIZATION FIGURES (TIFF FORMAT)")
    print("=" * 60)
    print(f"\nOutput directory: {output_dir}")
    print(f"\nMesh Parameters (Fine level):")
    print(f"  Total Elements:     10,24,000")
    print(f"  BL Elements:        3,10,000")
    print(f"  Inflation Layers:   20")
    print(f"  First Layer:        0.005 mm")
    print(f"  Growth Ratio:       1.15")
    print(f"  ΔP_reverse:         6,195 Pa (reference)")
    print()
    
    print("Generating figures...")
    print()
    
    print("[1/6] Leading Edge Mesh Detail...")
    create_figure1_leading_edge_mesh(output_dir)
    
    print("[2/6] Trailing Edge Mesh Detail...")
    create_figure2_trailing_edge_mesh(output_dir)
    
    print("[3/6] Slot Edge Mesh Refinement (A-D)...")
    create_figure3_slot_edge_mesh(output_dir)
    
    print("[4/6] Blade Tip Mesh...")
    create_figure4_blade_tip_mesh(output_dir)
    
    print("[5/6] Slot Configurations A-D (Full Blade)...")
    create_figure5_slot_configs(output_dir)
    
    print("[6/6] Overall Computational Domain...")
    create_figure6_overall_mesh(output_dir)
    
    print()
    print("=" * 60)
    print("ALL FIGURES GENERATED SUCCESSFULLY")
    print("=" * 60)
    print(f"\nFiles saved in: {output_dir}/")
    print("  1. Figure_Mesh_1_Leading_Edge.tiff")
    print("  2. Figure_Mesh_2_Trailing_Edge.tiff")
    print("  3. Figure_Mesh_3_Slot_Edge_Refinement.tiff")
    print("  4. Figure_Mesh_4_Blade_Tip.tiff")
    print("  5. Figure_Mesh_5_Slot_Configurations_AD.tiff")
    print("  6. Figure_Mesh_6_Overall_Domain.tiff")


if __name__ == "__main__":
    main()
