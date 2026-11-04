#!/usr/bin/env python3
"""
Figures for the chapter "Economic Analysis of Smart Hybrid Renewable Energy
Systems (HRES)" (written as code).  Every plotted number is taken from the
chapter's own tables; ranges are plotted directly and point values use the
midpoint of the reported range.

    python3 generate_hres_figures.py

Figure 1 - LCOE comparison across seven HRES configurations (Table 1)
Figure 2 - Revenue stacking, smart HRES vs alternatives (Table 2, range midpoints)
Figure 3 - Technology cost trajectories 2025-2035, indexed 2025 = 100 (Table 4 midpoints)
Figure 4 - Smart HRES market integration framework (conceptual)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
from svgfig import Figure, Axes, col  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'HRES_figures')

# ---------------------------------------------------------------- data
# Table 1: (configuration, LCOE low, LCOE high, optimal LCOE, RE fraction, ELCC)
TABLE1 = [
    ('PV/Wind (no storage)', 30, 60, 33, '70–85%', '15–30%'),
    ('PV/Wind/Li-ion Battery', 40, 65, 42, '90–99%', '50–75%'),
    ('PV/Wind/Pumped Hydro', 38, 60, 38.45, '95–100%', '70–90%'),
    ('PV/Wind/Battery/H₂', 45, 80, 58, '95–100%', '65–85%'),
    ('Solar + Storage (firm)', 54, 82, 54, '90–99%', '55–80%'),
    ('Offshore Wind/Battery', 65, 110, 72, '95–100%', '55–75%'),
    ('PV/Wind/Flow Battery', 45, 75, 48, '90–99%', '45–70%'),
]
# Table 2 revenue ranges (USD/MWh): stream -> [solar, wind, HRES w/o AI, smart HRES]
TABLE2 = [
    ('Day-ahead energy sales', 'blue', [(30, 45), (35, 50), (35, 55), (40, 65)]),
    ('Real-time balancing', 'violet', [(0, 3), (0, 5), (3, 10), (8, 20)]),
    ('Frequency regulation', 'emerald', [(0, 2), (0, 3), (5, 12), (10, 25)]),
    ('Spinning/non-spinning reserves', 'orange', [(0, 0), (0, 0), (2, 5), (5, 12)]),
    ('Capacity payments', 'red', [(3, 8), (5, 12), (8, 18), (12, 25)]),
    ('REC / green premiums', 'sky', [(2, 10), (2, 10), (3, 12), (4, 15)]),
    ('Demand response', 'teal', [(0, 0), (0, 0), (2, 8), (5, 15)]),
]
CONFIGS2 = ['Standalone Solar', 'Standalone Wind', 'HRES without AI', 'Smart HRES with AI']
# Table 4 cost ranges at 2025, 2028, 2030, 2035
YEARS = [2025, 2028, 2030, 2035]
TABLE4 = [
    ('Solar PV installed', 'orange', [(600, 900), (450, 700), (380, 550), (280, 420)]),
    ('Li-ion battery pack', 'emerald', [(150, 250), (100, 170), (70, 130), (45, 90)]),
    ('Onshore wind installed', 'blue', [(1100, 1500), (950, 1300), (850, 1150), (700, 1000)]),
    ('PEM electrolyzer', 'violet', [(800, 1400), (500, 900), (300, 600), (200, 400)]),
    ('AI / EMS software', 'red', [(15, 40), (10, 28), (8, 20), (5, 14)]),
]


def mid(r):
    return (r[0] + r[1]) / 2.0


def fig1():
    f = Figure(1500, 840, title='Levelized Cost of Energy across HRES Configurations (2025)',
               subtitle='Solid bar = optimal achievable LCOE · light band = full reported range · data: Table 1')
    rows = sorted(TABLE1, key=lambda r: r[3])
    ax = Axes(f, 380, 120, 1000, 630, (0, 120), (0, len(rows)), xlabel='LCOE (USD/MWh)', yticks=[],
              xticks=list(range(0, 121, 20)), grid=False)
    for t in range(20, 121, 20):
        f.line(ax.px(t), ax.y, ax.px(t), ax.y + ax.h, color='#E2E8F0', sw=1)
    palette = ['emerald', 'teal', 'cyan', 'blue', 'violet', 'amber', 'rose']
    for i, (name, lo, hi, opt, re_, elcc) in enumerate(rows):
        yc = len(rows) - i - 0.5
        c = palette[i]
        ax.hbar(yc, lo, hi, 46, color=col(c, 1), vivid=False, rx=8)
        f.rect(ax.px(lo), ax.py(yc) - 23, ax.px(hi) - ax.px(lo), 46, fill='none', stroke=col(c), sw=1.5,
               rx=8, shadow=False, dash='5,4')
        ax.hbar(yc, 0, opt, 26, color=c)
        f.text(ax.px(opt) - 8, ax.py(yc) + 5, ('%g' % opt), size=13.5, weight=800, color='#FFFFFF', anchor='end')
        f.text(ax.px(hi) + 10, ax.py(yc) + 5, '%d–%d' % (lo, hi), size=13.5, weight=700, color=col(c, 2),
               anchor='start')
        f.html(30, ax.py(yc) - 40, 340, 80, '<div style="text-align:right"><b style="font-size:16px">%s</b>'
               '<div style="font-size:12.5px;color:#475569;margin-top:2px">RE %s · ELCC %s</div></div>'
               % (name, re_, elcc), align='right', size=15)
    best = min((r for r in TABLE1 if r[4].startswith('95')), key=lambda r: r[3])
    f.soft(985, 118, 390, 96, '<div style="text-align:left"><b>Lowest overall:</b> PV/Wind without storage, '
           'USD 33/MWh (but ELCC only 15–30%%).<br/><b>Lowest at ≥95%% RE:</b> %s, USD %g/MWh.</div>'
           % (best[0], best[3]), color='amber', size=13.5, weight=500, align='left')
    f.save(os.path.join(OUT, 'figure1_lcoe_comparison.png'))


def fig2():
    f = Figure(1500, 860, title='Revenue Stacking: Smart HRES versus Alternatives',
               subtitle='Midpoints of the revenue ranges in Table 2 (USD/MWh), stacked by market revenue stream')
    totals = [sum(mid(s[2][k]) for s in TABLE2) for k in range(4)]
    ax = Axes(f, 140, 140, 820, 620, (0, 4), (0, 140), ylabel='Revenue (USD/MWh, range midpoints)',
              yticks=list(range(0, 141, 20)), xticks=[0.5, 1.5, 2.5, 3.5], xticklabels=CONFIGS2)
    for k in range(4):
        base = 0
        for name, c, vals in TABLE2:
            v = mid(vals[k])
            if v <= 0:
                continue
            ax.bar(k + 0.5, base + v, 120, color=c, base=base, rx=3)
            if v >= 6:
                f.text(ax.px(k + 0.5), (ax.py(base) + ax.py(base + v)) / 2 + 5, '%g' % v, size=12.5,
                       weight=700, color='#FFFFFF')
            base += v
        f.pill(ax.px(k + 0.5), ax.py(base) - 24, 'USD %.1f' % base, color='indigo', size=14)
    f.arrow(ax.px(0.5) + 70, ax.py(totals[0]) - 30, ax.px(3.5) - 80, ax.py(totals[3]) - 10, color='rose', sw=3,
            dash='8,6', curve=-40)
    f.pill(ax.px(1.05), ax.py(122), '+%.0f%% vs standalone solar' % ((totals[3] / totals[0] - 1) * 100),
           color='rose', size=14)
    f.text(1215, 160, 'Revenue streams', size=17, weight=800, color='#334155')
    f.legend(1030, 200, [(n, c) for n, c, _ in reversed(TABLE2)], size=14.5, gap=36)
    f.soft(1020, 500, 440, 170, '<div style="text-align:left;font-size:14px;line-height:1.5"><b>How to read:</b> '
           'each segment is the midpoint of the reported range for that stream. Table 2\'s total rows are '
           'reported separately (USD 35–65, 42–75, 53–108 and 73–153/MWh) because streams are co-optimized and '
           'cannot all peak at once; midpoint stacks therefore differ slightly from range totals.</div>',
           color='slate', weight=500, align='left')
    f.save(os.path.join(OUT, 'figure2_revenue_stacking.png'))


def fig3():
    f = Figure(1500, 880, title='HRES Technology Cost Trajectories, 2025–2035',
               subtitle='Index of range-midpoint costs, 2025 = 100 · data: Table 4')
    ax = Axes(f, 130, 130, 900, 600, (2024.5, 2035.5), (0, 110), xlabel='Year', ylabel='Cost index (2025 = 100)',
              yticks=list(range(0, 111, 20)), xticks=YEARS, xticklabels=[str(y) for y in YEARS])
    ends = []
    for name, c, rng in TABLE4:
        m = [mid(r) for r in rng]
        idx = [v / m[0] * 100 for v in m]
        lo = [r[0] / m[0] * 100 for r in rng]
        hi = [r[1] / m[0] * 100 for r in rng]
        ax.line(YEARS, idx, color=c, sw=3.5, smooth=False)
        ends.append((idx[-1], name, c))
    # labels at right
    prev = -1e9
    for i, (v, name, c) in enumerate(sorted(ends, key=lambda e: -e[0])):
        y = max(ax.py(v), prev + 18)
        prev = y
        f.text(ax.px(2035) + 14, y + 5, '%.0f' % v, size=14, weight=800, color=col(c, 2), anchor='start')
    f.text(1250, 150, '2035 vs 2025', size=17, weight=800, color='#334155')
    for i, (v, name, c) in enumerate(sorted(ends, key=lambda e: e[0])):
        y = 185 + i * 92
        f.rect(1080, y, 380, 76, fill=f.grad_for(c), stroke=col(c), sw=2, rx=12)
        f.text(1100, y + 31, name, size=15.5, weight=700, color=col(c, 2), anchor='start')
        f.text(1440, y + 56, '−%.0f%%' % (100 - v), size=22, weight=800, color=col(c, 2), anchor='end')
        f.text(1100, y + 56, 'index %.0f in 2035' % v, size=13, color='#475569', anchor='start')
    f.footnote('Each line indexes the midpoint of the Table 4 cost range for that year to its 2025 midpoint. '
               'Learning rates (Table 4): PV 24%, Li-ion 20%, PEM 18%, wind 17%, AI/EMS 25%.', y=845)
    f.save(os.path.join(OUT, 'figure3_cost_trajectories.png'))


def fig4():
    f = Figure(1500, 1000, title='Smart HRES Market Integration Framework',
               subtitle='AI/ML-enabled energy management connects generation and storage assets to six market products')
    # generation
    f.text(170, 140, 'GENERATION', size=16, weight=800, color=col('amber', 2), spacing=1.5)
    for i, (t, c) in enumerate([('☀ Solar PV', 'amber'), ('Wind', 'sky'), ('Backup / dispatchable', 'slate')]):
        f.tile(50, 160 + i * 105, 240, 80, t.replace('☀ ', ''), color=c, size=17)
        f.arrow(292, 200 + i * 105, 540, 360, color=c, sw=3)
    f.text(170, 515, 'STORAGE', size=16, weight=800, color=col('emerald', 2), spacing=1.5)
    for i, (t, c) in enumerate([('Battery (Li-ion / flow)', 'emerald'), ('Hydrogen (electrolyzer + tank)', 'teal')]):
        f.tile(50, 535 + i * 105, 240, 80, t, color=c, size=16)
        f.arrow(292, 575 + i * 105, 540, 470, color=c, sw=3, both=True)
    # EMS core
    f.rect(545, 250, 410, 330, fill=f.lingrad('#4F46E5', '#7C3AED'), rx=28, shadow=True)
    f.html(545, 262, 410, 70, '<div style="color:#fff;font-size:22px;font-weight:800">AI / ML ENERGY<br/>MANAGEMENT SYSTEM</div>')
    for i, t in enumerate(['Forecast generation, load and prices', 'Co-optimize dispatch and bids',
                           'Schedule charge / discharge', 'Manage risk and degradation']):
        f.rect(575, 345 + i * 55, 350, 44, fill='#FFFFFF', opacity=0.16, rx=10, shadow=False)
        f.text(750, 373 + i * 55, t, size=15, weight=600, color='#FFFFFF')
    # markets
    mk = [('Wholesale energy', 'blue', 'day-ahead · intraday · real-time'),
          ('Ancillary services', 'violet', 'frequency regulation · reserves'),
          ('Capacity market', 'red', 'firm capacity (ELCC)'),
          ('P2P trading', 'pink', 'local / community markets'),
          ('REC market', 'lime', 'certificates · green premiums'),
          ('Hydrogen market', 'teal', 'industry · mobility · export')]
    f.text(1250, 140, 'MARKET PRODUCTS', size=16, weight=800, color=col('blue', 2), spacing=1.5)
    for i, (t, c, d) in enumerate(mk):
        y = 160 + i * 112
        f.soft(1100, y, 350, 92, '<div><b style="font-size:17px">%s</b><div style="font-size:13.5px;'
               'font-weight:500;margin-top:4px">%s</div></div>' % (t, d), color=c)
        f.arrow(957, 415, 1097, y + 46, color=c, sw=3, both=True)
    # intelligence layer
    g = f.lingrad(col('cyan'), col('indigo'), horizontal=True)
    f.rect(330, 820, 1120, 130, fill=g, rx=22, shadow=True)
    f.text(890, 852, 'INTELLIGENCE LAYER', size=17, weight=800, color='#FFFFFF', spacing=2)
    for i, t in enumerate(['Forecasting', 'Optimization', 'Blockchain settlement', 'Digital twin']):
        f.rect(355 + i * 272, 870, 252, 56, fill='#FFFFFF', opacity=0.2, rx=12, shadow=False)
        f.text(481 + i * 272, 905, t, size=16, weight=700, color='#FFFFFF')
    f.arrow(750, 585, 750, 815, color='indigo', sw=4, both=True)
    f.soft(40, 800, 270, 150, '<div><b style="font-size:15px">Revenue potential</b><div style="font-size:26px;'
           'font-weight:800;margin:4px 0">USD 73–153/MWh</div><div style="font-size:13px">15–35% uplift from AI '
           'optimization</div></div>', color='amber', weight=600)
    f.save(os.path.join(OUT, 'figure4_market_framework.png'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    fig1()
    fig2()
    fig3()
    fig4()
