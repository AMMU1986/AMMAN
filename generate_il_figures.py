#!/usr/bin/env python3
"""
Figures for the manuscript "Ionic liquids as MQL additives in interrupted machining"
(Manuscript_Ionic_Liquids_MQL_Machining.md), written as code.

    python3 generate_il_figures.py          # all figures
    python3 generate_il_figures.py 3 4      # selected figures

Fig. 1 - Experimental set-up (schematic, instruments and settings from Section 2)
Fig. 2 - Heat-generation zones (a) and FD domain with boundary conditions (b), to scale
Fig. 3 - Machining forces: reported best-performing fluids per regime (Section 4, Table 5)
Fig. 4 - Estimated temperatures: stated thresholds vs. Table 1 decomposition temperatures
Fig. 5 - EDS / surface / SEM evidence (schematic illustrations)

Data policy: the manuscript does not tabulate per-condition force or temperature values,
and the original micrographs are not part of the repository.  Figures 3 and 4 therefore
show only what the text states (rankings, the 28 % reduction, temperature thresholds and the
Table 1 decomposition temperatures); Figure 5 is an explicitly labelled schematic.  No
values are invented.
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
from svgfig import Figure, Axes, col  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'manuscript_figures')


def panel(f, x, y, w, h, letter, title, color):
    f.rect(x, y, w, h, fill='#FFFFFF', stroke=col(color, 1), sw=2, rx=16)
    f.panel_label(x + 14, y + 12, letter, color=color)
    f.text(x + 58, y + 32, title, size=16, weight=700, color=col(color, 2), anchor='start')


# --------------------------------------------------------------------------- Fig. 1
def fig1():
    f = Figure(1400, 760, title='Interrupted Orthogonal Machining Set-up',
               subtitle='Peripheral down milling on a CNC vertical machining centre with MQL, force and '
                        'temperature measurement (Section 2)')
    # ---- machine area
    f.rect(30, 95, 860, 610, fill=f.lingrad('#FFFFFF', '#F1F5F9'), stroke='#CBD5E1', sw=1.5, rx=18)
    f.text(460, 125, 'BFW Surya VF30 CNC vertical machining centre (FANUC control)', size=14.5, weight=700,
           color=col('slate', 2))
    # spindle
    f.rect(350, 140, 120, 120, fill=f.lingrad('#94A3B8', '#475569'), rx=10)
    f.text(410, 205, 'Spindle', size=14, weight=700, color='#FFFFFF')
    f.rect(395, 260, 30, 50, fill='#64748B', rx=4, shadow=False)
    # cutter (50 mm diameter, single insert)
    cx, cy, r = 410, 375, 75
    f.circle(cx, cy, r, fill=f.radgrad('#E2E8F0', '#94A3B8'), stroke='#475569', sw=2.5, shadow=True)
    f.circle(cx, cy, 14, fill='#334155', stroke=None)
    f.polygon([(cx - 8, cy + r - 4), (cx + 16, cy + r - 4), (cx + 10, cy + r + 14), (cx - 8, cy + r + 10)],
              fill='amber', stroke=col('amber', 2), sw=1.5)
    f.text(cx - 95, cy - 10, 'Side & face', size=12.5, weight=700, color='#334155', anchor='end')
    f.text(cx - 95, cy + 8, 'milling cutter, Ø 50 mm', size=12.5, color='#334155', anchor='end')
    f.text(cx - 95, cy + 26, 'rake angle +5°', size=12.5, color='#334155', anchor='end')
    f.arrow(cx + 50, cy - 95, cx + 100, cy - 40, color='indigo', sw=3, curve=30)
    f.text(cx + 112, cy - 70, 'rotation', size=12.5, weight=700, color=col('indigo', 2), anchor='start')
    f.html(cx - 310, cy + 40, 210, 46, '<b>Single carbide insert</b><br/>TPUN 160308, P30, uncoated',
           size=12, color=col('amber', 2), align='right')
    f.line(cx - 98, cy + 66, cx - 12, cy + r + 4, color=col('amber', 2), sw=1.5, dash='4,3')
    # workpiece
    wy = 468
    f.rect(250, wy, 360, 52, fill=f.lingrad('#93C5FD', '#3B82F6'), stroke=col('blue', 2), sw=2, rx=4)
    f.text(430, wy + 32, 'Workpiece: medium carbon steel, 190 BHN, 48 × 14 × 6 mm', size=12, weight=700,
           color='#FFFFFF')
    f.arrow(640, wy + 26, 720, wy + 26, color='blue', sw=3)
    f.text(680, wy + 14, 'feed', size=12.5, weight=700, color=col('blue', 2))
    # fixture with thermocouples
    f.rect(230, wy + 52, 400, 48, fill=f.lingrad('#CBD5E1', '#94A3B8'), stroke='#475569', sw=1.5, rx=4)
    f.text(430, wy + 82, 'Fixture', size=13, weight=700, color='#1E293B')
    for tx in (300, 360, 500, 560):
        f.circle(tx, wy + 60, 6, fill='red', stroke='#FFFFFF', sw=1.5)
    f.line(300, wy + 60, 300, wy + 150, color='red', sw=2)
    f.line(300, wy + 150, 690, wy + 150, color='red', sw=2)
    # dynamometer
    f.rect(210, wy + 100, 440, 40, fill=f.lingrad('#A78BFA', '#7C3AED'), stroke=col('violet', 2), sw=1.5, rx=6)
    f.text(430, wy + 126, 'Kistler 5210 dynamometer', size=13.5, weight=700, color='#FFFFFF')
    f.line(430, wy + 140, 430, wy + 175, color='violet', sw=2.5)
    f.line(430, wy + 175, 690, wy + 175, color='violet', sw=2.5)
    # MQL nozzle
    f.polygon([(640, 300), (720, 260), (730, 280), (655, 320)], fill='teal', stroke=col('teal', 2), sw=1.5)
    f.rect(720, 230, 150, 70, fill=f.lingrad('#5EEAD4', '#0D9488'), rx=10)
    f.html(720, 230, 150, 70, '<b>MQL unit</b><br/>Botti Lubrostar GLS-1', size=12, color='#FFFFFF')
    rnd = random.Random(7)
    for _ in range(26):
        t = rnd.random()
        px = 640 - t * 140 + rnd.uniform(-10, 10)
        py = 315 + t * 120 + rnd.uniform(-12, 12)
        f.circle(px, py, rnd.uniform(2, 4.5), fill='teal', stroke=None, opacity=0.55)
    f.html(700, 318, 180, 44, '39 mL/h · air 5 kgf/cm² (≈ 0.49 MPa)', size=11.5, color=col('teal', 2), align='left')
    f.text(565, 455, 'tool–workpiece contact', size=11.5, color='#475569', anchor='middle', italic=True)

    # ---- acquisition chain
    f.card(690, 610, 190, 82, 'Force channel', 'Kistler 5070 amplifier → Dynoware, 15 kHz',
           color='violet', title_size=13, body_size=11.5, header_h=28)
    f.card(690, 505, 190, 92, 'Temperature', 'K-type, Ø 0.25 mm → NI cDAQ-9188 → LabVIEW',
           color='red', title_size=13, body_size=11.5, header_h=28)
    f.line(690, wy + 150, 690, 560, color='red', sw=2)
    f.line(690, wy + 175, 690, 640, color='violet', sw=2.5)

    # ---- right-hand information cards
    f.card(910, 95, 460, 165, 'Cutting conditions', '<div style="text-align:left">'
           '<b>Light:</b> f = 0.1 mm/tooth, radial depth 0.3 mm<br/>'
           '<b>Heavy:</b> f = 0.3 mm/tooth, radial depth 0.8 mm<br/>'
           '<b>Speeds:</b> Vc = 150, 200 and 250 m/min<br/>'
           'Three replicates per condition; fresh edge per test</div>',
           color='blue', title_size=15, body_size=13, header_h=36)
    f.card(910, 278, 460, 175, 'MWF application conditions', '<div style="text-align:left">'
           'DRY · OIL (canola) · OIL + IL1 · OIL + IL308 (1%) · OIL + IL308 (0.5%) · PEG · PEG + IL1<br/>'
           'Also: oil + BMIM PF6 / BF4 / TFSI, flood cooling, compressed air jet</div>',
           color='teal', title_size=15, body_size=13, header_h=36)
    f.card(910, 471, 460, 150, 'Post-process analysis', '<div style="text-align:left">'
           'Surface roughness Ra: Zeiss Surfcom 500<br/>'
           'SEM: JEOL JSM-6610LV · EDS: Oxford INCA X<br/>'
           'Fluids: Lovis 2000M, DMA 35, TGA/DSC 1, DSC1</div>',
           color='amber', title_size=15, body_size=13, header_h=36)
    f.legend(930, 655, [('Thermocouple (in fixture)', 'red', 'dot'), ('MQL mist', 'teal', 'dot')],
             cols=2, col_w=230, size=13)
    f.footnote('Schematic, not to scale. Instruments and settings are those given in Section 2.', y=738)
    f.save(os.path.join(OUT, 'Figure_1_Experimental_Setup.png'))


# --------------------------------------------------------------------------- Fig. 2
def fig2():
    f = Figure(1400, 700, title='Heat Generation and the Finite-Difference Model Domain',
               subtitle='(a) Heat-generation zones in orthogonal cutting   ·   (b) 30 mm × 8 mm FD domain '
                        'with boundary conditions, drawn to scale')
    panel(f, 20, 95, 520, 560, 'a', 'Heat-generation zones', 'orange')
    # workpiece
    f.polygon([(50, 430), (300, 430), (300, 400), (520, 400), (520, 630), (50, 630)],
              fill=f.lingrad('#BFDBFE', '#60A5FA'), stroke=col('blue', 2), sw=2)
    f.text(410, 600, 'Workpiece', size=14, weight=700, color=col('blue', 2))
    # chip
    f.polygon([(300, 400), (300, 430), (270, 300), (230, 180), (275, 170), (330, 290)],
              fill=f.lingrad('#FDBA74', '#EA580C'), stroke=col('orange', 2), sw=2)
    f.text(220, 160, 'Chip', size=14, weight=700, color=col('orange', 2), anchor='end')
    # tool
    f.polygon([(330, 290), (300, 420), (330, 425), (500, 360), (500, 170), (300, 170)],
              fill=f.lingrad('#CBD5E1', '#64748B'), stroke='#334155', sw=2)
    f.polygon([(300, 170), (330, 290), (275, 170)], fill='#FFFFFF', stroke=None)
    f.text(430, 250, 'Tool', size=15, weight=700, color='#FFFFFF')
    f.line(300, 430, 270, 330, color='red', sw=3, dash='6,4')
    f.text(250, 360, 'shear plane', size=12, color=col('red', 2), anchor='end', italic=True)
    # zones
    for (zx, zy, lab, c) in [(288, 385, '1', 'red'), (322, 330, '2', 'orange'), (322, 432, '3', 'amber')]:
        f.circle(zx, zy, 24, fill=c, stroke='#FFFFFF', sw=2.5, opacity=0.9, shadow=True)
        f.text(zx, zy + 6, lab, size=17, weight=700, color='#FFFFFF')
    f.arrow(120, 415, 240, 415, color='blue', sw=3)
    f.text(130, 405, 'cutting direction', size=12, color=col('blue', 2), anchor='start')
    f.rect(60, 490, 280, 100, fill='#FFFFFF', stroke=col('orange', 1), sw=1.5, rx=12, opacity=0.95)
    f.html(66, 490, 270, 100, '<div style="text-align:left"><b style="color:#B91C1C">1</b> primary shear zone<br/>'
           '<b style="color:#C2410C">2</b> secondary zone (rake face)<br/>'
           '<b style="color:#B45309">3</b> tertiary zone (flank)</div>', size=13, color='#1E293B',
           align='left')

    panel(f, 560, 95, 820, 560, 'b', 'FD discretisation and boundary conditions', 'indigo')
    sx = 23.0                      # px per mm
    x0, y0 = 610, 250
    W, H = 30 * sx, 8 * sx
    f.rect(x0, y0, W, H, fill=f.lingrad('#E0E7FF', '#C7D2FE'), stroke=col('indigo', 2), sw=2.5, rx=0)
    for i in range(1, 30):
        f.line(x0 + i * sx, y0, x0 + i * sx, y0 + H, color='#A5B4FC', sw=0.8)
    for j in range(1, 8):
        f.line(x0, y0 + j * sx, x0 + W, y0 + j * sx, color='#A5B4FC', sw=0.8)
    for i in range(31):
        for j in range(9):
            f.circle(x0 + i * sx, y0 + j * sx, 1.8, fill='indigo', stroke=None)
    # heat source on top
    hx = x0 + 17 * sx
    for k in range(5):
        f.arrow(hx + k * 10 - 20, y0 - 50, hx + k * 10 - 20, y0 - 4, color='red', sw=2.5)
    f.text(hx, y0 - 60, 'moving heat flux q̇ (tool contact)', size=13, weight=700, color=col('red', 2))
    f.arrow(hx + 50, y0 - 30, hx + 120, y0 - 30, color='orange', sw=3)
    f.text(hx + 130, y0 - 26, 'feed', size=12.5, weight=700, color=col('orange', 2), anchor='start')
    # convection at top
    for k in range(4):
        bx = x0 + 40 + k * 70
        f.path('M%d,%d c -10,-14 10,-22 0,-36' % (bx, y0 - 6), stroke='sky', sw=2.5)
    f.text(x0 + 140, y0 - 50, 'convection: h, T∞', size=13, weight=700, color=col('sky', 2))
    # Dirichlet boundaries
    f.line(x0, y0, x0, y0 + H, color='emerald', sw=6)
    f.line(x0 + W, y0, x0 + W, y0 + H, color='emerald', sw=6)
    f.line(x0, y0 + H, x0 + W, y0 + H, color='emerald', sw=6)
    f.text(x0 - 10, y0 + H / 2, 'T = T∞', size=13, weight=700, color=col('emerald', 2), anchor='end')
    f.text(x0 + W + 4, y0 + H + 26, 'T = T∞', size=13, weight=700, color=col('emerald', 2), anchor='end')
    f.text(x0 + W / 2, y0 + H + 26, 'bottom: T = T∞', size=13, weight=700, color=col('emerald', 2))
    # thermocouple 11 mm from left, 3 mm below top
    tx, ty = x0 + 11 * sx, y0 + 3 * sx
    f.circle(tx, ty, 9, fill='red', stroke='#FFFFFF', sw=2.5, shadow=True)
    f.line(x0, ty, tx - 10, ty, color=col('red', 2), sw=1.5, dash='4,3')
    f.line(tx, y0, tx, ty - 10, color=col('red', 2), sw=1.5, dash='4,3')
    f.text(x0 + 5.5 * sx, ty - 6, '11 mm', size=12, weight=700, color=col('red', 2))
    f.text(tx + 8, y0 + 1.5 * sx + 4, '3 mm', size=12, weight=700, color=col('red', 2), anchor='start')
    f.text(tx + 16, ty + 22, 'thermocouple', size=12.5, weight=700, color=col('red', 2), anchor='start')
    # dimensions
    f.arrow(x0, y0 + H + 52, x0 + W, y0 + H + 52, color='slate', sw=2, both=True)
    f.text(x0 + W / 2, y0 + H + 72, '30 mm', size=13, weight=700, color='#334155')
    f.arrow(x0 + W + 30, y0, x0 + W + 30, y0 + H, color='slate', sw=2, both=True)
    f.text(x0 + W + 40, y0 + H / 2 + 4, '8 mm', size=13, weight=700, color='#334155', anchor='start')
    f.html(590, 500, 770, 80, '<div style="text-align:left"><b>Explicit scheme:</b> interior nodes use Eq. (2), '
           'stable for Fo ≤ 1/4; convective top-surface nodes use Eq. (4), stable for Fo(2 + Bi) ≤ 1/2. '
           'The flux q̇ is fitted inversely to the measured thermocouple history.</div>',
           size=13, color='#1E293B', align='left')
    f.footnote('Grid drawn at 1 mm spacing for illustration only; this is not the spacing used in the study.',
               y=680)
    f.save(os.path.join(OUT, 'Figure_2_FD_Model_Discretization.png'))


# --------------------------------------------------------------------------- Fig. 3
FLUIDS = ['DRY', 'OIL', 'IL1', 'IL308 1%', 'IL308 0.5%', 'PEG', 'PEG+IL1']
FCOL = ['slate', 'amber', 'red', 'violet', 'purple', 'teal', 'cyan']


def ranking_panel(f, x, y, w, h, letter, title, color, best, mech, mech_color, note):
    panel(f, x, y, w, h, letter, title, color)
    f.pill(x + w - 110, y + 27, mech, color=mech_color, size=12.5)
    tw, gap = (w - 40 - 6 * 8) / 7.0, 8
    ty = y + 70
    for i, fl in enumerate(FLUIDS):
        tx = x + 20 + i * (tw + gap)
        if fl in best:
            f.rect(tx, ty, tw, 92, fill=f.vivid_for(FCOL[i]), rx=12)
            f.html(tx, ty + 6, tw, 50, fl, size=13, color='#FFFFFF', weight=700)
            f.badge(tx + tw / 2, ty + 70, '★', color='yellow', r=14, size=15)
        else:
            f.rect(tx, ty, tw, 92, fill='#F8FAFC', stroke='#E2E8F0', sw=1.5, rx=12, shadow=False)
            f.html(tx, ty + 6, tw, 50, fl, size=12.5, color='#94A3B8', weight=600)
    f.html(x + 20, ty + 100, w - 40, 60, note, size=13, color='#334155', align='left', valign='top')


def fig3():
    f = Figure(1400, 780, title='Machining Forces under Different MWF Application Conditions',
               subtitle='Fluids reported to give the lowest machining forces in each regime (Section 4.3 and Table 5)')
    pw, ph = 670, 315
    ranking_panel(f, 20, 95, pw, ph, 'a', 'Light machining, Vc = 150 m/min', 'teal',
                  ['PEG', 'IL308 1%'], 'Physical: viscosity', 'teal',
                  'Temperatures stay below all decomposition temperatures, so the higher-viscosity fluids '
                  '(PEG 97.43 and IL308 1% 139.34 mPa·s, Table 1) give the lowest forces.')
    # 28 % inset in panel a
    ax = Axes(f, 60, 345, 420, 55, (0, 100), (-0.6, 1.6), yticks=[], grid=False, bg=False)
    ax.hbar(1, 0, 100, 22, color='slate', label='Dry = 100')
    ax.hbar(0, 0, 72, 22, color='teal', label='BMIM PF6 oil ≈ 72')
    f.text(60, 337, 'Force relative to dry (28% reduction, Table 5)', size=12, weight=700,
           color=col('teal', 2), anchor='start')

    ranking_panel(f, 710, 95, pw, ph, 'b', 'Light machining, Vc = 250 m/min', 'sky',
                  ['IL1'], 'Chemical: F release', 'rose',
                  'Lubricants begin to decompose at the higher speed (Table 5); the fluorine-containing IL1 '
                  'gives the lowest forces.')
    ranking_panel(f, 20, 425, pw, ph, 'c', 'Heavy machining, Vc = 150 m/min', 'orange',
                  ['IL1', 'PEG+IL1'], 'Chemical: F release', 'rose',
                  'Temperatures exceed the decomposition temperatures of the fluids; IL1 and PEG+IL1 give the '
                  'lowest forces and temperatures. At 200 m/min IL308 (1%) performed best (Table 5).')
    ranking_panel(f, 710, 425, pw, ph, 'd', 'Heavy machining, Vc = 250 m/min', 'red',
                  ['OIL', 'IL1', 'IL308 0.5%'], 'Not resolved', 'slate',
                  'Neat vegetable oil matches or outperforms the ionic-liquid fluids; the base-oil film '
                  '(decomposition 380 °C) becomes increasingly important.')
    f.legend(30, 764, [('Reported lowest-force fluid', 'yellow', 'dot')], size=12.5)
    f.footnote('Per-condition force magnitudes are not tabulated in the manuscript, so the panels show the '
               'reported ranking only; the inset uses the stated 28% reduction.', y=768)
    f.save(os.path.join(OUT, 'Figure_3_Machining_Forces.png'))


# --------------------------------------------------------------------------- Fig. 4
DECOMP = [(380, 'Oil 380 °C', 'amber'), (341, 'Oil + IL1 341 °C', 'red'), (279, 'PEG 279 °C', 'teal')]


def temp_panel(f, x, y, w, h, letter, title, color, cols):
    """cols: dict speed_index -> (lo, hi, label, colour, kind) ; kind 'above'|'below'|'range'."""
    panel(f, x, y, w, h, letter, title, color)
    ax = Axes(f, x + 80, y + 60, w - 230, h - 120, (-0.6, 2.6), (0, 600), ylabel='Temperature (°C)',
              yticks=[0, 100, 200, 300, 400, 500, 600], xticks=[0, 1, 2],
              xticklabels=['150 m/min', '200 m/min', '250 m/min'])
    for i, spec in cols.items():
        if spec is None:
            f.text(ax.px(i), ax.py(150), 'not stated', size=12, color='#94A3B8', italic=True)
            continue
        lo, hi, lab, c, kind = spec
        bw = 92
        x0 = ax.px(i) - bw / 2
        if kind == 'above':
            grad = f.lingrad(col(c), '#FFFFFF')
            grad = f.lingrad('#FFFFFF', col(c))
            f.rect(x0, ax.py(hi), bw, ax.py(lo) - ax.py(hi), fill=grad, rx=8, opacity=0.85)
            f.arrow(ax.px(i), ax.py(lo) - 10, ax.px(i), ax.py(hi) + 8, color=col(c, 2), sw=3)
            f.pill(ax.px(i), ax.py(lo) + 16, lab, color=c, size=12)
        elif kind == 'below':
            f.rect(x0, ax.py(hi), bw, ax.py(lo) - ax.py(hi), fill=f.lingrad(col(c), '#FFFFFF'), rx=8, opacity=0.8)
            f.arrow(ax.px(i), ax.py(hi) + 14, ax.px(i), ax.py(lo + 20), color=col(c, 2), sw=3)
            f.pill(ax.px(i), ax.py(hi) - 16, lab, color=c, size=12)
        else:
            f.rect(x0, ax.py(hi), bw, ax.py(lo) - ax.py(hi), fill=col(c, 1), stroke=col(c), sw=2, rx=8,
                   dash='6,4', shadow=False)
            f.html(x0 - 20, ax.py(hi) - 46, bw + 40, 40, lab, size=11.5, color=col(c, 2), weight=700)
    for v, lab, c in DECOMP:
        ax.hline(v, color=c, sw=2, dash='8,5')
        f.text(ax.x + ax.w + 8, ax.py(v) + 4.5, lab, size=11.5, weight=700, color=col(c, 2), anchor='start')
    return ax


def fig4():
    f = Figure(1400, 1015, title='Estimated Temperatures from the FD Thermal Model',
               subtitle='Temperature levels stated in Section 4.4 compared with the lubricant decomposition '
                        'temperatures of Table 1 (dashed)')
    pw, ph = 670, 430
    temp_panel(f, 20, 95, pw, ph, 'a', 'Shear zone, light machining', 'teal',
               {0: (25, 272, 'below all (< 272 °C)', 'teal', 'below'), 1: None,
                2: (272, 380, 'begin to decompose (zone not specified)', 'rose', 'range')})
    temp_panel(f, 710, 95, pw, ph, 'b', 'Rake face, light machining', 'sky',
               {0: None, 1: None,
                2: (272, 380, 'begin to decompose (zone not specified)', 'rose', 'range')})
    temp_panel(f, 20, 540, pw, ph, 'c', 'Shear zone, heavy machining', 'orange',
               {0: (350, 600, '> 350 °C', 'orange', 'above'), 1: (350, 600, '> 350 °C', 'orange', 'above'),
                2: (350, 600, '> 350 °C', 'orange', 'above')})
    temp_panel(f, 710, 540, pw, ph, 'd', 'Rake face, heavy machining', 'red',
               {0: (400, 600, '> 400 °C', 'red', 'above'), 1: (400, 600, '> 400 °C', 'red', 'above'),
                2: (500, 600, '> 500 °C', 'fuchsia', 'above')})
    f.footnote('Bars show lower bounds or ranges stated in the text, not individual model estimates, which are '
               'not tabulated in the manuscript. Also in Table 1: IL308 1% 337, IL308 0.5% 366, PEG + IL1 272 °C.',
               y=1000)
    f.save(os.path.join(OUT, 'Figure_4_Temperature_Estimates.png'))


# --------------------------------------------------------------------------- Fig. 5
def dot_map(f, x, y, w, h, color, seed, deposits, density, bg_density, label):
    f.rect(x, y, w, h, fill='#0F172A', rx=10, shadow=True)
    rnd = random.Random(seed)
    # cutting edge
    f.line(x + 14, y + h - 30, x + w - 14, y + h - 30, color='#E2E8F0', sw=2, dash='5,4')
    for _ in range(bg_density):
        f.circle(x + rnd.uniform(6, w - 6), y + rnd.uniform(6, h - 6), 1.3, fill=color, stroke=None, opacity=0.5)
    for (dx, dy, rr) in deposits:
        for _ in range(density):
            a = rnd.uniform(0, 6.283)
            d = rr * (rnd.random() ** 0.6)
            import math
            f.circle(x + dx + d * math.cos(a), y + dy + d * math.sin(a) * 0.7, 1.6, fill=color, stroke=None,
                     opacity=0.9)
    f.text(x + 18, y + 26, label, size=16, weight=800, color=col(color), anchor='start')
    f.text(x + w - 12, y + h - 10, 'cutting edge', size=10.5, color='#CBD5E1', anchor='end', italic=True)


def surface(f, x, y, w, h, seed, amp, scars, title, color):
    rnd = random.Random(seed)
    f.rect(x, y, w, h, fill=f.lingrad('#E5E7EB', '#9CA3AF'), rx=10)
    for k in range(int(h / 6)):
        yy = y + 4 + k * 6
        pts = []
        for i in range(0, int(w) + 1, 10):
            pts.append((x + i, yy + rnd.uniform(-amp, amp)))
        f.polyline(pts, stroke='#6B7280', sw=1, opacity=0.6)
    for _ in range(scars):
        sx = x + rnd.uniform(10, w - 80)
        sy = y + rnd.uniform(10, h - 10)
        f.path('M%.1f,%.1f q %.1f,%.1f %.1f,%.1f' % (sx, sy, 30, rnd.uniform(-6, 6), rnd.uniform(50, 80),
                                                    rnd.uniform(-3, 3)), stroke='#374151', sw=3.5, opacity=0.8)
    f.text(x + w / 2, y + h + 22, title, size=13, weight=700, color=col(color, 2))


def fig5():
    f = Figure(1400, 760, title='Tool-Chip Interface Evidence for Fluorine-Assisted Anti-Adhesion',
               subtitle='Schematic illustration of the EDS, optical and SEM observations described in Section 4.5')
    panel(f, 20, 95, 560, 600, 'a', 'EDS element dot maps near the cutting edge', 'indigo')
    deposits = [(70, 120, 40), (170, 90, 32), (130, 160, 30), (205, 150, 22)]
    dot_map(f, 40, 145, 255, 230, 'orange', 3, deposits, 110, 60, 'Fe')
    dot_map(f, 305, 145, 255, 230, 'lime', 5, deposits, 60, 25, 'F')
    f.html(40, 390, 520, 120, '<div style="text-align:left"><b>Reading:</b> fluorine (F) is densest where iron '
           '(Fe) has been deposited from the workpiece, i.e. the two maps are co-localised. S and P appear '
           'only in trace amounts.</div>', size=13.5, color='#1E293B', align='left')
    f.soft(40, 520, 520, 150, '<div style="text-align:left"><b>Interpretation (Section 5):</b> at the interface '
           'temperature the ionic liquid decomposes and releases fluorine, which may form a low-shear iron '
           'fluoride layer. EDS is semi-quantitative and does not identify the compound.</div>',
           color='indigo', size=13, weight=500)

    panel(f, 600, 95, 780, 340, 'b', 'Machined surfaces, optical microscope (×100)', 'teal')
    surface(f, 625, 150, 350, 220, 11, 1.6, 9, 'Neat vegetable oil MQL: aggressive scouring', 'red')
    surface(f, 1005, 150, 350, 220, 12, 0.5, 1, 'Oil + BMIM PF6 MQL: smoother surface', 'teal')

    panel(f, 600, 455, 780, 240, 'c', 'Tool cutting edge (SEM)', 'orange')
    f.polygon([(640, 660), (900, 660), (1000, 520), (640, 520)], fill=f.lingrad('#D1D5DB', '#6B7280'),
              stroke='#374151', sw=2)
    f.text(760, 600, 'carbide insert', size=13, weight=700, color='#FFFFFF')
    f.path('M905,655 C930,630 950,610 985,540 L1000,520 C1010,560 975,630 930,665 Z',
           fill=f.lingrad('#FDBA74', '#C2410C'), stroke=col('orange', 2), sw=1.5)
    f.arrow(1060, 560, 975, 585, color='orange', sw=3)
    f.html(1065, 520, 300, 120, '<div style="text-align:left"><b>Adhered workpiece material</b> near the '
           'cutting edge, consistent with an adhesion-controlled process.</div>', size=13,
           color=col('orange', 2), align='left')
    f.footnote('Schematic illustrations only, not measured data. Replace with the original EDS maps, '
               'optical micrographs and SEM image for publication.', y=735)
    f.save(os.path.join(OUT, 'Figure_5_EDS_Surface.png'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:] or ['1', '2', '3', '4', '5']
    for w in which:
        globals()['fig' + w]()
