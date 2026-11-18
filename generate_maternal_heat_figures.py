#!/usr/bin/env python3
"""
Generate the four figures (300 dpi PNG) for the chapter
"Cooling the Cradle: Integrating Maternal and Newborn Heat Protection into
Climate-Ready Preventive Health Systems".

Figures
  Figure 1 - Pathways linking heat exposure to maternal, fetal and neonatal harm
  Figure 2 - Visibility of mothers and newborns in heat-health action plans and
             in the intervention literature (redrawn from published data)
  Figure 3 - Integrated preventive model across the maternal-newborn continuum
  Figure 4 - Multilevel governance and monitoring framework

Usage:
    python3 generate_maternal_heat_figures.py
"""

import math
import os

from maternal_heat_figlib import Canvas, hex2rgb as H

OUT = '/projects/sandbox/AMMAN/maternal_heat_figures'

NAVY = H('1F4E79'); NAVY_L = H('DCEBF7')
TEAL = H('0F766E'); TEAL_L = H('D5F0EC')
ORANGE = H('C55A11'); ORANGE_L = H('FBE5D6')
RED = H('A50F15'); RED_L = H('FADBD8')
GREEN = H('38761D'); GREEN_L = H('E2F0D9')
PURPLE = H('5B3A8E'); PURPLE_L = H('E8E0F3')
GOLD = H('9C6500'); GOLD_L = H('FFF2CC')
GRAY = H('595959'); GRAY_L = H('F2F2F2'); MID = H('A6A6A6')
INK = H('1A1A1A'); WHITE = (255, 255, 255)


def box(c, x1, y1, x2, y2, text, fill, edge, size=34, title=None,
        title_fill=None, r=22, pad=22):
    c.round_rect(x1, y1, x2, y2, r, fill=fill, outline=edge, width=4)
    top = y1
    if title:
        th = size * 1.9
        c.round_rect(x1, y1, x2, y1 + th, r, fill=title_fill or edge)
        c.fill_rect(x1, y1 + th - r, x2, y1 + th, title_fill or edge)
        c.text_box_centered((x1 + x2) / 2, y1 + th / 2, title, size * 1.05,
                            x2 - x1 - 2 * pad, WHITE, bold=True)
        top = y1 + th
    if text:
        c.text_box_centered((x1 + x2) / 2, (top + y2) / 2, text, size,
                            x2 - x1 - 2 * pad, INK)


def bullets(c, x, y, items, size, max_w, color=INK, gap=14):
    for it in items:
        c.circle(x + 10, y + size * 0.62, 7, fill=color)
        h = c.text_block(x + 32, y, it, size, max_w - 32, INK)
        y += h + gap
    return y


# ---------------------------------------------------------------------------
def fig1():
    c = Canvas(2400, 1560)
    cols = [(40, 560, 'Heat exposure'), (660, 1560, 'Physiological pathways'),
            (1660, 2360, 'Adverse outcomes')]
    for x1, x2, t in cols:
        c.text((x1 + x2) / 2, 30, t, 46, NAVY, bold=True, anchor='c')
        c.line(x1, 100, x2, 100, NAVY, 4)

    exp = ['Ambient and humid heat (heatwaves, high wet-bulb temperature)',
           'Indoor heat (poorly ventilated housing, no power for fans)',
           'Occupational heat (farming, brick kilns, domestic and market work)',
           'Heat inside health facilities (uncooled antenatal, labour and postnatal wards)']
    y = 130
    for t in exp:
        box(c, 40, y, 560, y + 245, t, ORANGE_L, ORANGE, 33)
        y += 270

    mat = ['Higher metabolic heat production and fetal heat load narrow the margin for heat loss',
           'Dehydration and reduced circulating plasma volume',
           'Blood diverted to the skin, reducing uteroplacental perfusion',
           'Inflammatory and stress-hormone responses that may trigger early labour',
           'Cardiovascular strain and raised blood pressure']
    c.text(1110, 122, 'Pregnant woman and fetus', 34, RED, bold=True, anchor='c')
    y = 172
    for t in mat:
        box(c, 660, y, 1560, y + 138, t, RED_L, RED, 31)
        y += 152
    c.text(1110, 940, 'Newborn', 34, TEAL, bold=True, anchor='c')
    box(c, 660, 990, 1560, 1200,
        'Immature thermoregulation, high surface-area-to-mass ratio, limited '
        'sweating capacity, rapid fluid loss and full dependence on caregivers '
        'for cooling, feeding and shade', TEAL_L, TEAL, 31)

    outs = [('Maternal', 'Heat exhaustion and heat stroke, hypertensive disorders, '
             'fatigue, poor sleep, psychological distress', RED, RED_L),
            ('Fetal and birth', 'Miscarriage, preterm birth, stillbirth, low birth '
             'weight, growth restriction, congenital anomalies', PURPLE, PURPLE_L),
            ('Neonatal', 'Dehydration, hyperthermia, feeding difficulty, '
             'neonatal hospital admission and death', TEAL, TEAL_L)]
    y = 130
    for t, body, e, f in outs:
        box(c, 1660, y, 2360, y + 330, body, f, e, 33, title=t)
        y += 357

    # flow arrows
    for yy in (330, 640, 940):
        c.block_arrow(575, yy, 650, 70, MID)
    c.block_arrow(575, 1095, 650, 70, MID)
    for yy in (300, 680):
        c.block_arrow(1575, yy, 1650, 70, MID)
    c.block_arrow(1575, 1095, 1650, 70, MID)

    # modifiers band
    c.round_rect(40, 1290, 2360, 1530, 22, fill=GOLD_L, outline=GOLD, width=4)
    c.text(1200, 1312, 'Effect modifiers that amplify risk', 38, GOLD, bold=True, anchor='c')
    c.text_box_centered(1200, 1435,
                        'Poverty  |  informal outdoor work  |  crowded, poorly ventilated housing  |  '
                        'unreliable water and electricity  |  distance to care  |  '
                        'gender norms that limit rest  |  chronic hypertension, diabetes, adolescence',
                        33, 2200, INK)
    for xx in (300, 1110, 2010):
        c.arrow(xx, 1285, xx, 1215, GOLD, 6, 26)
    c.save(os.path.join(OUT, 'Figure_1_Heat_Pathways.png'))


# ---------------------------------------------------------------------------
def hbar_panel(c, x0, y0, w, title, data, color, unit, vmax, label_w=430,
               bar_h=78, gap=46, size=34):
    c.text_block(x0, y0, title, 38, w, NAVY, bold=True)
    top = y0 + 140
    ax0 = x0 + label_w
    aw = w - label_w - 120
    n = len(data)
    bottom = top + n * (bar_h + gap)
    for k in range(0, 6):
        v = vmax * k / 5
        gx = ax0 + aw * k / 5
        c.line(gx, top - 16, gx, bottom - gap + 16, H('D9D9D9'), 2)
        lab = ('%d' % v) + (unit if unit == '%' else '')
        c.text(gx, bottom - gap + 28, lab, 30, GRAY, anchor='c')
    for i, (lab, v, col) in enumerate(data):
        yy = top + i * (bar_h + gap)
        lines = c.wrap(lab, size, label_w - 30)
        th = len(lines) * size * 1.25
        for j, ln in enumerate(lines):
            c.text(ax0 - 24, yy + bar_h / 2 - th / 2 + j * size * 1.25, ln, size,
                   INK, anchor='r')
        bw = aw * v / vmax
        c.rect(ax0, yy, ax0 + bw, yy + bar_h, fill=col or color)
        txt = ('%d%%' % v) if unit == '%' else ('%d' % v)
        c.text(ax0 + bw + 16, yy + bar_h / 2 - 20, txt, 36, INK, bold=True)
    c.line(ax0, top - 16, ax0, bottom - gap + 16, INK, 3)
    return bottom


def fig2():
    c = Canvas(2400, 900)
    b1 = hbar_panel(c, 40, 30, 1160,
                    'A. Population groups named as at risk in heat-health action plans',
                    [('Children', 83, H('8FAADC')),
                     ('Pregnant individuals', 52, RED),
                     ('Newborns', 39, TEAL),
                     ('Postpartum and breastfeeding individuals', 14, PURPLE)],
                    NAVY, '%', 100, label_w=440)
    c.text(40 + 440 + 300, b1 + 20, 'Share of plans', 32, GRAY, anchor='c')
    b2 = hbar_panel(c, 1260, 30, 1100,
                    'B. Focus of interventions mapped for maternal, newborn and child health (n = 76)',
                    [('Air pollution', 57, H('8C8C8C')),
                     ('Extreme heat', 18, ORANGE),
                     ('Both exposures', 1, GOLD)],
                    NAVY, 'n', 60, label_w=330)
    c.text(1260 + 330 + 325, b2 + 20, 'Number of items', 32, GRAY, anchor='c')
    c.line(40, 770, 2360, 770, H('D9D9D9'), 2)
    c.text_block(40, 792,
                 'Panel A redrawn from data reported by Czerniewska et al. (2025). Panel B redrawn '
                 'from data reported by Strong et al. (2025). Both are open-access articles in the '
                 'Journal of Global Health.',
                 31, 2320, GRAY)
    c.save(os.path.join(OUT, 'Figure_2_MNCH_Visibility.png'))


# ---------------------------------------------------------------------------
def fig3():
    c = Canvas(2400, 1460)
    c.round_rect(40, 30, 2360, 190, 26, fill=NAVY)
    c.text(1200, 52, 'Heat-health early warning system', 44, WHITE, bold=True, anchor='c')
    c.text(1200, 118, 'Forecast  >  locally set health threshold  >  alert routed to MNCH services, '
           'community health workers and registered pregnant women', 33, WHITE, anchor='c')
    stages = [
        ('Antenatal care', RED, RED_L,
         ['Heat-risk screening at every contact', 'Counselling on fluids, rest, cooling and warning signs',
          'Phone numbers added to alert lists', 'Flag hypertension, diabetes, outdoor work, adolescence']),
        ('Community and household', ORANGE, ORANGE_L,
         ['CHW home visits to high-risk women on alert days', 'Check water, shade, fan and power access',
          'Arrange referral and transport', 'Engage spouses and mothers-in-law']),
        ('Labour and delivery', PURPLE, PURPLE_L,
         ['Cooled, ventilated labour rooms with drinking water',
          'Maternal temperature and hydration monitoring',
          'Obstetric heat-illness and rapid-cooling protocol', 'Ambulances equipped for cooling']),
        ('Postnatal and newborn care', TEAL, TEAL_L,
         ['Newborn temperature and hydration checks', 'Support frequent breastfeeding',
          'Advise against over-wrapping; safe cooling', 'Extra postnatal contacts during alerts']),
    ]
    x = 40
    w = 535
    step = 595
    for i, (t, e, f, items) in enumerate(stages):
        x1 = x + i * step
        c.arrow(x1 + w / 2, 195, x1 + w / 2, 290, NAVY, 7, 30)
        c.round_rect(x1, 300, x1 + w, 900, 24, fill=f, outline=e, width=4)
        c.round_rect(x1, 300, x1 + w, 410, 24, fill=e)
        c.fill_rect(x1, 380, x1 + w, 410, e)
        c.text_box_centered(x1 + w / 2, 355, t, 37, w - 40, WHITE, bold=True)
        bullets(c, x1 + 26, 440, items, 32, w - 50, e, gap=30)
        if i < 3:
            c.block_arrow(x1 + w + 6, 600, x1 + step - 6, 64, MID)
    c.text(1200, 925, 'Continuum of care: the same woman and newborn are followed across contact points',
           32, GRAY, anchor='c')
    c.round_rect(40, 1005, 2360, 1430, 26, fill=GRAY_L, outline=GRAY, width=3)
    c.text(1200, 1025, 'Health-system enablers', 40, INK, bold=True, anchor='c')
    en = [('Trained workforce', 'Heat modules for midwives, nurses, ASHAs and other CHWs', NAVY, NAVY_L),
          ('Heat-resilient facilities', 'Passive cooling, shading, water, back-up power', GREEN, GREEN_L),
          ('Data and surveillance', 'Heat-linked fields in ANC, delivery and HMIS records', PURPLE, PURPLE_L),
          ('Financing and protection', 'Budget lines, cash transfers, heat insurance, transport', GOLD, GOLD_L)]
    for i, (t, d, e, f) in enumerate(en):
        x1 = 80 + i * 575
        box(c, x1, 1100, x1 + 535, 1400, d, f, e, 31, title=t)
    c.save(os.path.join(OUT, 'Figure_3_Integrated_Preventive_Model.png'))


# ---------------------------------------------------------------------------
def arc_arrow(c, cx, cy, r, a0, a1, color, width=8):
    n = 30
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
            cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
    for k in range(n - 1):
        c.line(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], color, width)
    c.arrow(pts[-3][0], pts[-3][1], pts[-1][0], pts[-1][1], color, width, 34)


def fig4():
    c = Canvas(2400, 1540)
    c.text(635, 25, 'Governance tiers', 46, NAVY, bold=True, anchor='c')
    tiers = [
        ('National', 'Pregnant and postpartum women and newborns named as priority groups in '
         'heat-health action plans; dedicated budget lines; national obstetric and neonatal heat '
         'guidance; maternal health programme seated on the climate-health task force', NAVY, NAVY_L),
        ('State / district', 'Multisectoral heat-health committees that include maternal health '
         'officers; locally calibrated alert thresholds; pre-season facility readiness audits', GREEN, GREEN_L),
        ('Health facility', 'Cooling and water standards for antenatal, labour and postnatal areas; '
         'heat-risk counselling recorded on ANC cards; surveillance of heat-linked outcomes', PURPLE, PURPLE_L),
        ('Community and household', "Community health workers, women's groups and self-help groups "
         'deliver alerts and checks; cash transfers or insurance offset the cost of cooling and transport',
         ORANGE, ORANGE_L),
    ]
    y = 110
    for t, d, e, f in tiers:
        c.round_rect(40, y, 1230, y + 255, 22, fill=f, outline=e, width=4)
        c.round_rect(40, y, 340, y + 255, 22, fill=e)
        c.fill_rect(310, y, 340, y + 255, e)
        c.text_box_centered(190, y + 128, t, 37, 270, WHITE, bold=True)
        c.text_box_centered(785, y + 128, d, 30, 840, INK)
        y += 280
    # vertical flows between tiers
    c.arrow(1272, 1195, 1272, 120, GRAY, 7, 30)
    c.arrow(1322, 120, 1322, 1195, GRAY, 7, 30)
    for i, ln in enumerate(['Data and accountability', 'flow up; guidance and', 'resources flow down']):
        c.text(1297, 1215 + i * 34, ln, 27, GRAY, anchor='c')

    cx, cy, r = 1885, 640, 330
    c.text(cx, 25, 'Monitoring and learning cycle', 46, NAVY, bold=True, anchor='c')
    c.circle(cx, cy, r + 2, fill=WHITE, outline=H('D9D9D9'), width=3)
    nodes = [(-90, 'Plan', 'Designate groups, set targets and budgets', NAVY, NAVY_L),
             (0, 'Implement', 'ANC, community and facility measures', GREEN, GREEN_L),
             (90, 'Monitor', 'Core indicators (Table 4) each season', PURPLE, PURPLE_L),
             (180, 'Review and adapt', 'Post-season review; revise the plan', ORANGE, ORANGE_L)]
    bw, bh = 380, 205
    for a0 in (-54, 22, 126, 202):
        arc_arrow(c, cx, cy, r, a0, a0 + 32, GRAY, 7)
    for ang, t, d, e, f in nodes:
        nx = cx + r * math.cos(math.radians(ang))
        ny = cy + r * math.sin(math.radians(ang))
        nx = max(1390 + bw / 2, min(2390 - bw / 2, nx))
        box(c, nx - bw / 2, ny - bh / 2, nx + bw / 2, ny + bh / 2, d, f, e, 28, title=t, r=18)
    c.text_box_centered(cx, 1135, 'Equity lens at every step: disaggregate indicators by income, '
                        'caste or ethnicity, age, and urban or rural residence', 29, 900, GRAY)
    c.round_rect(40, 1330, 2360, 1510, 22, fill=GOLD_L, outline=GOLD, width=3)
    c.text_box_centered(1200, 1420, 'Intersectoral partners: meteorological services, disaster '
                        'management, labour, women and child development, water and energy utilities, '
                        'urban planning, obstetric and paediatric professional bodies, civil society', 32, 2240, INK)
    c.save(os.path.join(OUT, 'Figure_4_Governance_Monitoring_Framework.png'))


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in (fig1, fig2, fig3, fig4):
        f()
        print(f.__name__, 'done')


if __name__ == '__main__':
    main()
