"""
Generate 4 figures for the Signal Processing for Condition Monitoring chapter.
Uses pure Python with struct/zlib to create PNG files - optimized for speed.
"""
import struct
import zlib
import os
import math

def create_png_from_buffer(width, height, buffer, filename):
    """Create PNG from flat bytearray buffer (RGB, row-major)."""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = zlib.crc32(chunk) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)
    
    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)
    
    # Build raw data with filter bytes
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)  # filter none
        raw.extend(buffer[y * stride:(y + 1) * stride])
    
    compressed = zlib.compress(bytes(raw), 6)
    idat = make_chunk(b'IDAT', compressed)
    iend = make_chunk(b'IEND', b'')
    
    with open(filename, 'wb') as f:
        f.write(signature + ihdr + idat + iend)

def set_pixel(buf, width, x, y, r, g, b):
    if 0 <= x < width and 0 <= y:
        idx = (y * width + x) * 3
        if idx + 2 < len(buf):
            buf[idx] = r
            buf[idx+1] = g
            buf[idx+2] = b

def fill_rect(buf, width, height, x1, y1, x2, y2, r, g, b):
    x1, x2 = max(0, x1), min(width, x2)
    y1, y2 = max(0, y1), min(height, y2)
    stride = width * 3
    row_segment = bytes([r, g, b]) * (x2 - x1)
    for y in range(y1, y2):
        start = y * stride + x1 * 3
        buf[start:start + len(row_segment)] = row_segment

def draw_hline(buf, width, height, x1, x2, y, r, g, b, thickness=1):
    for t in range(thickness):
        yy = y + t
        if 0 <= yy < height:
            x1c, x2c = max(0, x1), min(width, x2)
            stride = width * 3
            start = yy * stride + x1c * 3
            segment = bytes([r, g, b]) * (x2c - x1c)
            buf[start:start + len(segment)] = segment

def draw_vline(buf, width, height, x, y1, y2, r, g, b, thickness=1):
    for t in range(thickness):
        xx = x + t
        if 0 <= xx < width:
            for yy in range(max(0, y1), min(height, y2)):
                idx = (yy * width + xx) * 3
                buf[idx] = r
                buf[idx+1] = g
                buf[idx+2] = b

def draw_box(buf, width, height, x1, y1, x2, y2, fill_r, fill_g, fill_b, border_r=0, border_g=0, border_b=0):
    fill_rect(buf, width, height, x1, y1, x2, y2, fill_r, fill_g, fill_b)
    draw_hline(buf, width, height, x1, x2, y1, border_r, border_g, border_b, 2)
    draw_hline(buf, width, height, x1, x2, y2-2, border_r, border_g, border_b, 2)
    draw_vline(buf, width, height, x1, y1, y2, border_r, border_g, border_b, 2)
    draw_vline(buf, width, height, x2-2, y1, y2, border_r, border_g, border_b, 2)

FONT = {
    'A': ['01110','10001','10001','11111','10001','10001','10001'],
    'B': ['11110','10001','10001','11110','10001','10001','11110'],
    'C': ['01110','10001','10000','10000','10000','10001','01110'],
    'D': ['11110','10001','10001','10001','10001','10001','11110'],
    'E': ['11111','10000','10000','11110','10000','10000','11111'],
    'F': ['11111','10000','10000','11110','10000','10000','10000'],
    'G': ['01110','10001','10000','10111','10001','10001','01110'],
    'H': ['10001','10001','10001','11111','10001','10001','10001'],
    'I': ['01110','00100','00100','00100','00100','00100','01110'],
    'J': ['00111','00010','00010','00010','00010','10010','01100'],
    'K': ['10001','10010','10100','11000','10100','10010','10001'],
    'L': ['10000','10000','10000','10000','10000','10000','11111'],
    'M': ['10001','11011','10101','10101','10001','10001','10001'],
    'N': ['10001','11001','10101','10011','10001','10001','10001'],
    'O': ['01110','10001','10001','10001','10001','10001','01110'],
    'P': ['11110','10001','10001','11110','10000','10000','10000'],
    'Q': ['01110','10001','10001','10001','10101','10010','01101'],
    'R': ['11110','10001','10001','11110','10100','10010','10001'],
    'S': ['01110','10001','10000','01110','00001','10001','01110'],
    'T': ['11111','00100','00100','00100','00100','00100','00100'],
    'U': ['10001','10001','10001','10001','10001','10001','01110'],
    'V': ['10001','10001','10001','10001','01010','01010','00100'],
    'W': ['10001','10001','10001','10101','10101','10101','01010'],
    'X': ['10001','10001','01010','00100','01010','10001','10001'],
    'Y': ['10001','10001','01010','00100','00100','00100','00100'],
    'Z': ['11111','00001','00010','00100','01000','10000','11111'],
    '0': ['01110','10001','10011','10101','11001','10001','01110'],
    '1': ['00100','01100','00100','00100','00100','00100','01110'],
    '2': ['01110','10001','00001','00110','01000','10000','11111'],
    '3': ['01110','10001','00001','00110','00001','10001','01110'],
    '4': ['00010','00110','01010','10010','11111','00010','00010'],
    '5': ['11111','10000','11110','00001','00001','10001','01110'],
    '6': ['01110','10001','10000','11110','10001','10001','01110'],
    '7': ['11111','00001','00010','00100','01000','01000','01000'],
    '8': ['01110','10001','10001','01110','10001','10001','01110'],
    '9': ['01110','10001','10001','01111','00001','10001','01110'],
    ' ': ['00000','00000','00000','00000','00000','00000','00000'],
    '-': ['00000','00000','00000','11111','00000','00000','00000'],
    '.': ['00000','00000','00000','00000','00000','01100','01100'],
    ',': ['00000','00000','00000','00000','00000','00100','01000'],
    '(': ['00010','00100','01000','01000','01000','00100','00010'],
    ')': ['01000','00100','00010','00010','00010','00100','01000'],
    '/': ['00001','00010','00010','00100','01000','01000','10000'],
    ':': ['00000','01100','01100','00000','01100','01100','00000'],
    '%': ['11001','11010','00010','00100','01000','01011','10011'],
    '+': ['00000','00100','00100','11111','00100','00100','00000'],
    '=': ['00000','00000','11111','00000','11111','00000','00000'],
}

def draw_text(buf, width, height, text, x, y, r, g, b, scale=1):
    cx = x
    for ch in text.upper():
        if ch in FONT:
            bitmap = FONT[ch]
            for row_idx, row_bits in enumerate(bitmap):
                for col_idx, bit in enumerate(row_bits):
                    if bit == '1':
                        px_base = cx + col_idx * scale
                        py_base = y + row_idx * scale
                        for sy in range(scale):
                            for sx in range(scale):
                                px = px_base + sx
                                py = py_base + sy
                                if 0 <= px < width and 0 <= py < height:
                                    idx = (py * width + px) * 3
                                    buf[idx] = r
                                    buf[idx+1] = g
                                    buf[idx+2] = b
        cx += 6 * scale

def generate_figure1():
    """Figure 1: Vibration Signal Processing Framework"""
    w, h = 800, 500
    buf = bytearray([255, 255, 255] * w * h)
    
    # Header bar
    fill_rect(buf, w, h, 0, 0, 800, 40, 40, 60, 120)
    draw_text(buf, w, h, "VIBRATION SIGNAL PROCESSING FRAMEWORK", 130, 12, 255, 255, 255, 2)
    
    # Stage boxes
    boxes = [
        (40, 60, 200, 120, "SENSOR SYSTEM", 180, 220, 255),
        (40, 140, 200, 200, "DATA ACQUISITION", 180, 220, 255),
        (260, 60, 460, 120, "TIME DOMAIN", 200, 255, 200),
        (260, 140, 460, 200, "FREQUENCY DOMAIN", 200, 255, 200),
        (260, 220, 460, 280, "TIME-FREQ DOMAIN", 200, 255, 200),
        (530, 60, 730, 120, "ML CLASSIFICATION", 255, 230, 200),
        (530, 140, 730, 200, "FAULT DIAGNOSIS", 255, 230, 200),
        (530, 220, 730, 280, "RUL PREDICTION", 255, 230, 200),
    ]
    for x1, y1, x2, y2, label, fr, fg, fb in boxes:
        draw_box(buf, w, h, x1, y1, x2, y2, fr, fg, fb)
        tx = x1 + (x2 - x1 - len(label)*6)//2
        ty = y1 + (y2 - y1 - 7)//2
        draw_text(buf, w, h, label, tx, ty, 0, 0, 0, 1)
    
    # Arrows (horizontal bars)
    fill_rect(buf, w, h, 200, 88, 260, 92, 0, 0, 150)
    fill_rect(buf, w, h, 200, 168, 260, 172, 0, 0, 150)
    fill_rect(buf, w, h, 460, 88, 530, 92, 0, 0, 150)
    fill_rect(buf, w, h, 460, 168, 530, 172, 0, 0, 150)
    fill_rect(buf, w, h, 460, 248, 530, 252, 0, 0, 150)
    
    # Vertical connectors
    fill_rect(buf, w, h, 118, 120, 122, 140, 0, 0, 150)
    fill_rect(buf, w, h, 358, 120, 362, 140, 0, 0, 150)
    fill_rect(buf, w, h, 358, 200, 362, 220, 0, 0, 150)
    fill_rect(buf, w, h, 628, 120, 632, 140, 0, 0, 150)
    fill_rect(buf, w, h, 628, 200, 632, 220, 0, 0, 150)
    
    # Vibration waveform at bottom
    draw_text(buf, w, h, "SAMPLE VIBRATION SIGNAL", 270, 310, 0, 60, 120, 2)
    baseline_y = 400
    fill_rect(buf, w, h, 50, baseline_y, 750, baseline_y+1, 180, 180, 180)
    
    for x in range(50, 750):
        t = (x - 50) / 80.0
        val = int(30*math.sin(2*math.pi*t) + 12*math.sin(7*math.pi*t) + 6*math.sin(15*math.pi*t))
        py = baseline_y - val
        if 0 <= py < h:
            set_pixel(buf, w, x, py, 0, 80, 180)
            if py+1 < h:
                set_pixel(buf, w, x, py+1, 0, 80, 180)
    
    draw_text(buf, w, h, "TIME", 380, baseline_y + 10, 100, 100, 100, 1)
    draw_text(buf, w, h, "AMPLITUDE", 10, baseline_y - 30, 100, 100, 100, 1)
    
    # Stage headers
    draw_text(buf, w, h, "ACQUISITION", 80, 48, 0, 0, 120, 1)
    draw_text(buf, w, h, "SIGNAL PROCESSING", 300, 48, 0, 100, 0, 1)
    draw_text(buf, w, h, "AI ANALYTICS", 590, 48, 150, 60, 0, 1)
    
    create_png_from_buffer(w, h, buf, '/projects/sandbox/AMMAN/signal_figures/Figure_1_Signal_Processing_Framework.png')
    print("Figure 1 generated.")

def generate_figure2():
    """Figure 2: Time-Frequency Analysis Comparison"""
    w, h = 800, 500
    buf = bytearray([255, 255, 255] * w * h)
    
    # Title
    fill_rect(buf, w, h, 0, 0, 800, 35, 40, 80, 40)
    draw_text(buf, w, h, "TIME-FREQUENCY ANALYSIS METHODS COMPARISON", 110, 8, 255, 255, 255, 2)
    
    # Left panel - STFT
    draw_text(buf, w, h, "STFT SPECTROGRAM", 110, 45, 0, 0, 100, 1)
    px1, py1, pw, ph = 50, 60, 320, 170
    draw_box(buf, w, h, px1, py1, px1+pw, py1+ph, 240, 240, 255)
    
    # Simulated spectrogram tiles
    for tx in range(32):
        for fy in range(17):
            bx = px1 + 2 + tx * 10
            by = py1 + 2 + fy * 10
            t = tx / 32.0
            f = fy / 17.0
            energy = math.exp(-((t-0.3)**2 + (f-0.4)**2)*8) + math.exp(-((t-0.7)**2 + (f-0.7)**2)*8)
            intensity = int(min(255, energy * 255))
            fill_rect(buf, w, h, bx, by, bx+9, by+9, 255-intensity, 255-intensity, 255)
    
    draw_text(buf, w, h, "TIME", 180, py1+ph+5, 0, 0, 0, 1)
    draw_text(buf, w, h, "FREQ", 25, py1+80, 0, 0, 0, 1)
    
    # Right panel - Wavelet
    draw_text(buf, w, h, "WAVELET SCALOGRAM", 520, 45, 100, 0, 0, 1)
    px2 = 430
    draw_box(buf, w, h, px2, py1, px2+pw, py1+ph, 255, 240, 240)
    
    for tx in range(64):
        for fy in range(17):
            bx = px2 + 2 + tx * 5
            by = py1 + 2 + fy * 10
            t = tx / 64.0
            f = fy / 17.0
            sf = 1.0 + 2.0 * f
            energy = math.exp(-((t-0.3)**2*sf + (f-0.4)**2)*10) + math.exp(-((t-0.7)**2*sf + (f-0.7)**2)*10)
            intensity = int(min(255, energy * 255))
            fill_rect(buf, w, h, bx, by, bx+4, by+9, 255, 255-intensity, 255-intensity)
    
    draw_text(buf, w, h, "TIME", 560, py1+ph+5, 0, 0, 0, 1)
    draw_text(buf, w, h, "SCALE", 400, py1+80, 0, 0, 0, 1)
    
    # Bottom - EMD
    fill_rect(buf, w, h, 0, 255, 800, 275, 40, 40, 100)
    draw_text(buf, w, h, "EMPIRICAL MODE DECOMPOSITION", 200, 258, 255, 255, 255, 2)
    
    labels = ["ORIGINAL", "IMF 1", "IMF 2", "RESIDUE"]
    colors = [(0,0,0), (200,0,0), (0,150,0), (0,0,200)]
    for idx, (label, clr) in enumerate(zip(labels, colors)):
        yc = 310 + idx * 45
        draw_text(buf, w, h, label, 60, yc-3, 0, 0, 0, 1)
        fill_rect(buf, w, h, 150, yc, 700, yc+1, 220, 220, 220)
        for x in range(150, 700):
            t = (x - 150) / 80.0
            if idx == 0:
                val = int(12*math.sin(2*math.pi*t) + 7*math.sin(6*math.pi*t) + 3*math.sin(14*math.pi*t))
            elif idx == 1:
                val = int(3*math.sin(14*math.pi*t)*max(0, 1-t*0.15))
            elif idx == 2:
                val = int(7*math.sin(6*math.pi*t))
            else:
                val = int(12*math.sin(2*math.pi*t))
            py = yc - val
            if 0 <= py < h:
                set_pixel(buf, w, x, py, clr[0], clr[1], clr[2])
    
    create_png_from_buffer(w, h, buf, '/projects/sandbox/AMMAN/signal_figures/Figure_2_Time_Frequency_Analysis.png')
    print("Figure 2 generated.")

def generate_figure3():
    """Figure 3: ML/DL Pipeline for Fault Diagnosis"""
    w, h = 800, 500
    buf = bytearray([248, 248, 255] * w * h)
    
    # Title
    fill_rect(buf, w, h, 0, 0, 800, 35, 100, 20, 20)
    draw_text(buf, w, h, "ML AND DL PIPELINE FOR FAULT DIAGNOSIS", 150, 8, 255, 255, 255, 2)
    
    # Pipeline boxes
    stages = [
        (30, 55, 170, 120, "RAW SIGNAL", 180, 220, 255),
        (200, 55, 340, 120, "FEATURE EXTRACT", 180, 255, 180),
        (370, 55, 510, 120, "SELECTION", 255, 255, 180),
        (540, 55, 720, 120, "ML MODEL", 255, 200, 180),
    ]
    for x1, y1, x2, y2, label, fr, fg, fb in stages:
        draw_box(buf, w, h, x1, y1, x2, y2, fr, fg, fb)
        tx = x1 + (x2-x1-len(label)*6)//2
        ty = y1 + (y2-y1-7)//2
        draw_text(buf, w, h, label, tx, ty, 0, 0, 0, 1)
    
    # Arrows
    fill_rect(buf, w, h, 170, 85, 200, 89, 0, 0, 0)
    fill_rect(buf, w, h, 340, 85, 370, 89, 0, 0, 0)
    fill_rect(buf, w, h, 510, 85, 540, 89, 0, 0, 0)
    
    # Output box
    draw_box(buf, w, h, 540, 135, 720, 185, 255, 180, 180, 150, 0, 0)
    draw_text(buf, w, h, "FAULT CLASS", 580, 155, 0, 0, 0, 1)
    fill_rect(buf, w, h, 628, 120, 632, 135, 0, 0, 0)
    
    # Deep Learning section
    fill_rect(buf, w, h, 0, 200, 800, 220, 60, 60, 120)
    draw_text(buf, w, h, "DEEP LEARNING ARCHITECTURES", 230, 203, 255, 255, 255, 2)
    
    # CNN
    draw_box(buf, w, h, 40, 235, 240, 340, 200, 200, 255, 0, 0, 100)
    draw_text(buf, w, h, "1D-CNN", 105, 245, 0, 0, 100, 1)
    draw_text(buf, w, h, "CONV LAYERS", 75, 270, 0, 0, 0, 1)
    draw_text(buf, w, h, "POOLING", 100, 290, 0, 0, 0, 1)
    draw_text(buf, w, h, "DENSE LAYERS", 70, 310, 0, 0, 0, 1)
    
    # LSTM
    draw_box(buf, w, h, 280, 235, 490, 340, 200, 255, 200, 0, 100, 0)
    draw_text(buf, w, h, "LSTM-RNN", 345, 245, 0, 100, 0, 1)
    draw_text(buf, w, h, "SEQUENCE INPUT", 310, 270, 0, 0, 0, 1)
    draw_text(buf, w, h, "HIDDEN STATES", 315, 290, 0, 0, 0, 1)
    draw_text(buf, w, h, "TEMPORAL FEAT", 315, 310, 0, 0, 0, 1)
    
    # Transformer
    draw_box(buf, w, h, 530, 235, 750, 340, 255, 220, 200, 150, 50, 0)
    draw_text(buf, w, h, "TRANSFORMER", 590, 245, 150, 50, 0, 1)
    draw_text(buf, w, h, "SELF-ATTENTION", 565, 270, 0, 0, 0, 1)
    draw_text(buf, w, h, "MULTI-HEAD", 585, 290, 0, 0, 0, 1)
    draw_text(buf, w, h, "POSITIONAL ENC", 565, 310, 0, 0, 0, 1)
    
    # Results bar chart
    draw_text(buf, w, h, "CLASSIFICATION ACCURACY COMPARISON", 200, 360, 0, 0, 0, 2)
    
    models = [("CNN", 97.2, 100, 100, 255), ("LSTM", 95.8, 100, 200, 100), 
              ("TRANS", 98.1, 255, 150, 50), ("HYBRID", 98.7, 200, 50, 200)]
    for i, (name, acc, cr, cg, cb) in enumerate(models):
        bar_x = 80 + i * 180
        bar_w = int(140 * (acc / 100.0))
        fill_rect(buf, w, h, bar_x, 395, bar_x + bar_w, 420, cr, cg, cb)
        draw_text(buf, w, h, name, bar_x, 385, 0, 0, 0, 1)
        draw_text(buf, w, h, f"{acc}%", bar_x + bar_w - 30, 425, 0, 0, 0, 1)
    
    # Output classes
    draw_text(buf, w, h, "CLASSES: NORMAL  BEARING  GEAR  MISALIGNMENT  IMBALANCE", 100, 460, 60, 60, 60, 2)
    
    create_png_from_buffer(w, h, buf, '/projects/sandbox/AMMAN/signal_figures/Figure_3_ML_Pipeline.png')
    print("Figure 3 generated.")

def generate_figure4():
    """Figure 4: Real-Time Condition Monitoring Architecture"""
    w, h = 800, 500
    buf = bytearray([250, 250, 255] * w * h)
    
    # Title
    fill_rect(buf, w, h, 0, 0, 800, 35, 50, 0, 100)
    draw_text(buf, w, h, "REAL-TIME CONDITION MONITORING ARCHITECTURE", 100, 8, 255, 255, 255, 2)
    
    # Layer 1 - Sensors
    draw_box(buf, w, h, 25, 45, 775, 130, 220, 235, 255, 0, 0, 150)
    draw_text(buf, w, h, "PHYSICAL LAYER: SENSORS AND DAQ", 220, 50, 0, 0, 100, 1)
    sensors = ["ACCELEROMETER", "PROXIMITY PROBE", "AE SENSOR", "TACHOMETER"]
    for i, s in enumerate(sensors):
        sx = 55 + i * 185
        fill_rect(buf, w, h, sx, 75, sx+155, 115, 180, 210, 255)
        draw_text(buf, w, h, s, sx+10, 90, 0, 0, 0, 1)
    
    # Layer 2 - Edge
    draw_box(buf, w, h, 25, 145, 775, 230, 220, 255, 220, 0, 100, 0)
    draw_text(buf, w, h, "EDGE LAYER: REAL-TIME SIGNAL PROCESSING", 190, 150, 0, 80, 0, 1)
    edge = ["PREPROCESSING", "FFT-WAVELET", "FEATURE CALC", "LOCAL ALERT"]
    for i, s in enumerate(edge):
        sx = 55 + i * 185
        fill_rect(buf, w, h, sx, 175, sx+155, 215, 180, 255, 180)
        draw_text(buf, w, h, s, sx+10, 190, 0, 0, 0, 1)
    
    # Layer 3 - Cloud AI
    draw_box(buf, w, h, 25, 245, 775, 330, 255, 235, 215, 150, 80, 0)
    draw_text(buf, w, h, "CLOUD LAYER: AI ANALYTICS AND LEARNING", 195, 250, 120, 60, 0, 1)
    cloud = ["DL MODELS", "FAULT DIAGNOS.", "PROGNOSTICS", "DIGITAL TWIN"]
    for i, s in enumerate(cloud):
        sx = 55 + i * 185
        fill_rect(buf, w, h, sx, 275, sx+155, 315, 255, 210, 180)
        draw_text(buf, w, h, s, sx+10, 290, 0, 0, 0, 1)
    
    # Layer 4 - Decision
    draw_box(buf, w, h, 25, 345, 775, 430, 235, 225, 255, 80, 0, 120)
    draw_text(buf, w, h, "DECISION LAYER: MAINTENANCE OPTIMIZATION", 180, 350, 80, 0, 100, 1)
    decision = ["SCHEDULING", "WORK ORDERS", "SPARE PARTS", "DASHBOARD"]
    for i, s in enumerate(decision):
        sx = 55 + i * 185
        fill_rect(buf, w, h, sx, 375, sx+155, 415, 210, 200, 255)
        draw_text(buf, w, h, s, sx+10, 390, 0, 0, 0, 1)
    
    # Vertical arrows between layers
    for i in range(4):
        ax = 130 + i * 185
        fill_rect(buf, w, h, ax, 130, ax+4, 145, 0, 0, 0)
        fill_rect(buf, w, h, ax, 230, ax+4, 245, 0, 0, 0)
        fill_rect(buf, w, h, ax, 330, ax+4, 345, 0, 0, 0)
    
    # Footer
    draw_text(buf, w, h, "INDUSTRIAL IOT CONNECTIVITY AND FEEDBACK LOOP", 170, 450, 80, 80, 80, 2)
    
    # Feedback arrow (simplified)
    fill_rect(buf, w, h, 775, 90, 790, 400, 150, 150, 150)
    draw_text(buf, w, h, "FEEDBACK", 760, 240, 100, 100, 100, 1)
    
    create_png_from_buffer(w, h, buf, '/projects/sandbox/AMMAN/signal_figures/Figure_4_RealTime_Architecture.png')
    print("Figure 4 generated.")

if __name__ == '__main__':
    os.makedirs('/projects/sandbox/AMMAN/signal_figures', exist_ok=True)
    generate_figure1()
    generate_figure2()
    generate_figure3()
    generate_figure4()
    print("\nAll 4 figures generated successfully in /projects/sandbox/AMMAN/signal_figures/")
