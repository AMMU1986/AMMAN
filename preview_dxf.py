#!/usr/bin/env python3
"""
Dependency-free DXF -> SVG previewer for sanity-checking the generated drawing.
Supports LINE, LWPOLYLINE, CIRCLE, ARC, TEXT. Maps a few ACI colors.
"""
import math, sys

ACI_HEX = {
    1: "#FF0000", 2: "#FFD400", 3: "#00B050", 4: "#00B0F0", 5: "#0000FF",
    6: "#FF00FF", 7: "#000000", 8: "#808080", 9: "#BFBFBF",
    11: "#F4A9A0", 14: "#8B0000", 30: "#FF8C00", 36: "#6B4226",
}
LAYER_COLOR = {
    "PLATE_SDSS": 11, "PLATE_X70": 36, "WELD": 2, "TENSILE": 9,
    "MICROHARD": 4, "METALLO": 8, "IMPACT": 1, "OUTLINE": 7,
    "TEXT": 7, "LABELS": 1, "BORDER": 7, "0": 7,
}
FILL_LAYERS = {"PLATE_SDSS", "PLATE_X70", "TENSILE", "MICROHARD",
               "METALLO", "IMPACT"}

def parse(path):
    toks = open(path).read().splitlines()
    pairs = [(toks[i].strip(), toks[i+1]) for i in range(0, len(toks)-1, 2)]
    ents, cur, in_ent = [], None, False
    i = 0
    while i < len(pairs):
        c, v = pairs[i]
        if c == '2' and v == 'ENTITIES':
            in_ent = True
        elif c == '2' and v == 'ENDSEC':
            in_ent = False
        if in_ent and c == '0' and v in ('LINE','LWPOLYLINE','CIRCLE','ARC','TEXT'):
            if cur: ents.append(cur)
            cur = {'type': v, 'pts': [], 'raw': {}}
        elif cur is not None and in_ent:
            cur['raw'].setdefault(c, []).append(v)
        i += 1
    if cur: ents.append(cur)
    return ents

def color_for(e):
    layer = e['raw'].get('8', ['0'])[0]
    aci = LAYER_COLOR.get(layer, 7)
    if '62' in e['raw']:
        try: aci = int(e['raw']['62'][0])
        except: pass
    return ACI_HEX.get(aci, "#000000"), layer

def main():
    ents = parse("Specimen_Extraction_Layout.dxf")
    minx, miny, maxx, maxy = 0, 0, 420, 320
    scale = 2.2
    pad = 20
    def X(x): return x*scale + pad
    def Y(y): return (maxy - y)*scale + pad   # flip Y for SVG
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{maxx*scale+2*pad:.0f}" '
           f'height="{maxy*scale+2*pad:.0f}" style="background:#fff">']
    for e in ents:
        col, layer = color_for(e)
        fill = col if layer in FILL_LAYERS else "none"
        r = e['raw']
        if e['type'] == 'LINE':
            x1=float(r['10'][0]); y1=float(r['20'][0])
            x2=float(r['11'][0]); y2=float(r['21'][0])
            svg.append(f'<line x1="{X(x1):.1f}" y1="{Y(y1):.1f}" x2="{X(x2):.1f}" '
                       f'y2="{Y(y2):.1f}" stroke="{col}" stroke-width="0.8"/>')
        elif e['type'] == 'LWPOLYLINE':
            xs=[float(v) for v in r.get('10',[])]
            ys=[float(v) for v in r.get('20',[])]
            pts=" ".join(f"{X(x):.1f},{Y(y):.1f}" for x,y in zip(xs,ys))
            closed = r.get('70',['0'])[0] == '1'
            tag = 'polygon' if closed else 'polyline'
            op = '0.75' if fill!='none' else '1'
            svg.append(f'<{tag} points="{pts}" fill="{fill}" fill-opacity="{op}" '
                       f'stroke="{col}" stroke-width="0.7"/>')
        elif e['type'] == 'CIRCLE':
            cx=float(r['10'][0]); cy=float(r['20'][0]); rad=float(r['40'][0])
            svg.append(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{rad*scale:.1f}" '
                       f'fill="none" stroke="{col}" stroke-width="0.7"/>')
        elif e['type'] == 'TEXT':
            x=float(r['10'][0]); y=float(r['20'][0]); h=float(r['40'][0])
            s=r['1'][0]; rot=float(r.get('50',['0'])[0])
            svg.append(f'<text x="{X(x):.1f}" y="{Y(y):.1f}" font-size="{h*scale:.1f}" '
                       f'fill="{col}" font-family="Arial" transform="rotate({-rot:.1f} '
                       f'{X(x):.1f} {Y(y):.1f})">{s}</text>')
    svg.append('</svg>')
    open("Specimen_Extraction_Layout_preview.svg","w").write("\n".join(svg))
    print("Wrote Specimen_Extraction_Layout_preview.svg")

if __name__ == "__main__":
    main()
