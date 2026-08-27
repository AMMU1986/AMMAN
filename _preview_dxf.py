"""Quick pure-Python DXF (R12) validator + SVG preview generator.

Reads LINE / CIRCLE / ARC / TEXT entities and writes an SVG so the drawing
can be eyeballed without any CAD software or third-party libraries.
"""
import math
import sys


def read_groups(path):
    with open(path) as f:
        toks = f.read().split("\n")
    i = 0
    pairs = []
    while i + 1 < len(toks):
        code = toks[i].strip()
        val = toks[i + 1]
        if code == "":
            i += 2
            continue
        pairs.append((int(code), val))
        i += 2
    return pairs


def parse_entities(pairs):
    ents = []
    cur = None
    in_entities = False
    for code, val in pairs:
        if code == 0:
            if val == "SECTION":
                pass
            if val in ("LINE", "CIRCLE", "ARC", "TEXT"):
                if cur:
                    ents.append(cur)
                cur = {"type": val}
                continue
            else:
                if cur:
                    ents.append(cur)
                    cur = None
        if cur is None:
            continue
        cur[code] = val
    return ents


def main(path):
    pairs = read_groups(path)
    ents = parse_entities(pairs)
    counts = {}
    for e in ents:
        counts[e["type"]] = counts.get(e["type"], 0) + 1
    print("Entity counts:", counts)

    # collect bounds
    xs, ys = [], []
    segs = []
    circs = []
    texts = []
    for e in ents:
        t = e["type"]
        if t == "LINE":
            x1, y1 = float(e[10]), float(e[20])
            x2, y2 = float(e[11]), float(e[21])
            segs.append((x1, y1, x2, y2))
            xs += [x1, x2]; ys += [y1, y2]
        elif t in ("CIRCLE", "ARC"):
            cx, cy, r = float(e[10]), float(e[20]), float(e[40])
            a0 = float(e.get(50, 0)); a1 = float(e.get(51, 360))
            circs.append((cx, cy, r, a0, a1, t))
            xs += [cx - r, cx + r]; ys += [cy - r, cy + r]
        elif t == "TEXT":
            x, y, h = float(e[10]), float(e[20]), float(e[40])
            texts.append((x, y, h, e.get(1, "")))
            xs.append(x); ys.append(y)

    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    pad = 10
    W = (maxx - minx) + 2 * pad
    H = (maxy - miny) + 2 * pad

    def tx(x): return x - minx + pad
    def ty(y): return maxy - y + pad   # flip Y for screen coords

    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="{:.0f}" height="{:.0f}" '
           'viewBox="0 0 {:.0f} {:.0f}">'.format(W * 3, H * 3, W, H)]
    out.append('<rect width="100%" height="100%" fill="white"/>')
    for x1, y1, x2, y2 in segs:
        out.append('<line x1="{:.2f}" y1="{:.2f}" x2="{:.2f}" y2="{:.2f}" '
                   'stroke="black" stroke-width="0.3"/>'.format(tx(x1), ty(y1), tx(x2), ty(y2)))
    for cx, cy, r, a0, a1, t in circs:
        if t == "CIRCLE":
            out.append('<circle cx="{:.2f}" cy="{:.2f}" r="{:.2f}" fill="none" '
                       'stroke="black" stroke-width="0.3"/>'.format(tx(cx), ty(cy), r))
        else:
            pts = []
            steps = 24
            for k in range(steps + 1):
                a = math.radians(a0 + (a1 - a0) * k / steps)
                pts.append("{:.2f},{:.2f}".format(tx(cx + r * math.cos(a)), ty(cy + r * math.sin(a))))
            out.append('<polyline points="{}" fill="none" stroke="black" '
                       'stroke-width="0.3"/>'.format(" ".join(pts)))
    for x, y, h, s in texts:
        out.append('<text x="{:.2f}" y="{:.2f}" font-size="{:.1f}" fill="green">{}</text>'
                   .format(tx(x), ty(y), h, s.replace("&", "&amp;").replace("<", "&lt;")))
    out.append("</svg>")
    svg_path = path.rsplit(".", 1)[0] + "_preview.svg"
    with open(svg_path, "w") as f:
        f.write("\n".join(out))
    print("Preview written:", svg_path)
    print("Bounds: x[{:.1f},{:.1f}] y[{:.1f},{:.1f}]".format(minx, maxx, miny, maxy))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Specimen_Layout_Drawing.dxf")
