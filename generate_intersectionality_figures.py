#!/usr/bin/env python3
"""
Figures for the chapter "Intersectionality, Climate Vulnerability, and Community
Resilience" (written as code).

    python3 generate_intersectionality_figures.py

Figure 1 - The intersectional matrix of compounded climate vulnerability
Figure 2 - Comparative vulnerability profiles of differently positioned women
           (illustrative composite levels, as in the chapter's narrative synthesis)
Figure 3 - Pillars of community resilience and the community-based adaptation cycle
Figure 4 - Integrated framework for intersectional, community-centred climate action
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
from svgfig import Figure, Axes, col  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'intersectionality_figures')


def fig1():
    f = Figure(1500, 900, title='The Intersectional Matrix of Compounded Climate Vulnerability',
               subtitle='Overlapping social positions converge to intensify climate risk and narrow adaptation pathways')
    cx, cy = 750, 470
    axes = [('Gender', 'rose'), ('Caste / race /<br>ethnicity', 'orange'), ('Class &amp;<br>poverty', 'amber'),
            ('Indigeneity &amp;<br>land rights', 'emerald'), ('Age &amp;<br>disability', 'blue'),
            ('Migration &amp;<br>displacement', 'violet')]
    n = len(axes)
    R, r = 120, 150
    for i, (name, c) in enumerate(axes):
        a = -math.pi / 2 + i * 2 * math.pi / n
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        f.circle(x, y, r, fill=col(c), opacity=0.30)
        f.circle(x, y, r, fill='none', stroke=col(c), sw=2.5)
        lx, ly = cx + (R + 95) * math.cos(a), cy + (R + 95) * math.sin(a)
        f.html(lx - 80, ly - 32, 160, 64, name, size=16, weight=800, color=col(c, 2))
    f.circle(cx, cy, 74, fill=f.radgrad('#FCA5A5', '#991B1B'), shadow=True)
    f.html(cx - 70, cy - 55, 140, 110, '<div style="color:#fff;font-weight:800;font-size:15px">COMPOUNDED<br/>'
           'VULNERABILITY</div><div style="color:#FEE2E2;font-size:12px;margin-top:4px">least visible ·<br/>least served</div>')
    # hazards
    hz = [('Floods', 'sky'), ('Droughts', 'amber'), ('Heatwaves', 'red'), ('Cyclones &amp; storms', 'indigo'),
          ('Sea-level rise &amp; salinity', 'cyan')]
    f.text(165, 150, 'CLIMATE HAZARDS', size=16, weight=800, color=col('sky', 2), spacing=1.5)
    for i, (h, c) in enumerate(hz):
        y = 175 + i * 120
        f.tile(50, y, 230, 76, h, color=c, size=16)
        f.arrow(284, y + 38, 450, cy - 80 + i * 40, color=c, sw=3)
    # outcomes
    oc = [('↑ Exposure', 'Unsafe housing, hazard-prone land, outdoor and informal work', 'red'),
          ('↑ Sensitivity', 'Poor health, food insecurity, dependence on climate-sensitive livelihoods', 'orange'),
          ('↓ Adaptive capacity', 'Limited land, credit, information, mobility, voice in decisions', 'violet'),
          ('↓ Visibility', 'Missing from aggregate data and mainstream planning instruments', 'slate')]
    f.text(1300, 150, 'OUTCOMES', size=16, weight=800, color=col('red', 2), spacing=1.5)
    for i, (t, d, c) in enumerate(oc):
        y = 175 + i * 150
        f.card(1150, y, 310, 125, t, d, color=c, title_size=16, body_size=13.5, header_h=36)
        f.arrow(1050, cy - 60 + i * 40, 1146, y + 62, color=c, sw=3)
    # bottom strip
    g = f.lingrad(col('rose'), col('violet'), horizontal=True)
    f.rect(330, 790, 840, 70, fill=g, rx=35, shadow=True)
    f.html(330, 790, 840, 70, '<div style="color:#fff;font-weight:700;font-size:17px">Effects multiply rather than '
           'simply add: risk is shaped by the <i>configuration</i> of positions, not by any single axis</div>')
    f.save(os.path.join(OUT, 'Figure_1_Intersectional_Matrix.png'))


def fig2():
    f = Figure(1500, 900, title='Comparative Vulnerability Profiles of Differently Positioned Women',
               subtitle='Illustrative composite profiles: aggregate "women" averages conceal those at greatest risk')
    dims = ['Exposure', 'Sensitivity', 'Low adaptive capacity']
    profiles = [
        ('Landowning woman,<br>dominant social group', [30, 30, 25], 'emerald'),
        ('Landless woman,<br>marginalised caste', [70, 72, 78], 'amber'),
        ('Indigenous woman,<br>dispossessed territory', [78, 70, 82], 'violet'),
        ('Widowed / displaced woman,<br>in poverty', [85, 88, 90], 'rose'),
    ]
    avg = [round(sum(p[1][d] for p in profiles) / 4) for d in range(3)]
    rows = profiles + [('"Women" as one category<br>(aggregate average)', avg, 'slate')]
    ax = Axes(f, 360, 130, 1060, 600, (0, 100), (0, 5), xlabel='Relative level of climate risk (illustrative scale, 0–100)',
              yticks=[], xticks=[0, 25, 50, 75, 100], xticklabels=['0 · low', '25', '50 · medium', '75', '100 · high'],
              grid=False)
    for t in (25, 50, 75):
        f.line(ax.px(t), ax.y, ax.px(t), ax.y + ax.h, color='#E2E8F0', sw=1.2)
    dcol = ['sky', 'orange', 'purple']
    for pi, (name, vals, c) in enumerate(rows):
        yc = 4.5 - pi
        gy = ax.py(yc)
        f.rect(40, gy - 54, 300, 108, fill=f.grad_for(c), stroke=col(c), sw=2, rx=14,
               dash='8,5' if c == 'slate' else None)
        f.html(40, gy - 54, 300, 108, name, size=15.5, weight=700, color=col(c, 2))
        for di, v in enumerate(vals):
            y = yc + 0.26 - di * 0.26
            ax.hbar(y, 0, v, 26, color=dcol[di], label='%d' % v, label_size=13.5,
                    opacity=0.45 if c == 'slate' else 1)
    f.line(ax.x, ax.py(1), ax.x + ax.w, ax.py(1), color='#94A3B8', sw=2, dash='6,5')
    f.html(ax.px(72.5), ax.py(0.5) - 40, 300, 80, '<div style="text-align:left">Averaging hides the 55–65-point gap between '
           'the most and least advantaged profiles</div>', size=13.5, color='#475569', italic=True, align='left')
    f.legend(470, 800, [(d, dcol[i]) for i, d in enumerate(dims)], cols=3, col_w=300, size=15)
    f.footnote('Values are illustrative relative levels synthesising the chapter\'s narrative evidence [5, 7]; '
               'they are not survey measurements. Higher bars indicate greater risk.', y=860)
    f.save(os.path.join(OUT, 'Figure_2_Vulnerability_Profiles.png'))


def fig3():
    f = Figure(1500, 920, title='Pillars of Community Resilience and the Community-Based Adaptation Cycle',
               subtitle='Resilience as a dynamic, iterative and locally owned process, not a fixed endpoint')
    # temple: roof
    f.polygon([(60, 250), (420, 120), (780, 250)], fill=f.lingrad(col('indigo'), col('violet')), shadow=True)
    f.text(420, 215, 'COMMUNITY RESILIENCE', size=21, weight=800, color='#FFFFFF')
    f.rect(70, 255, 700, 22, fill=col('indigo', 2), rx=4, shadow=False)
    pillars = [('Diversified &amp; secure livelihoods', 'emerald'), ('Robust, inclusive collective institutions', 'blue'),
               ('Access to &amp; control over resources', 'amber'), ('Social cohesion &amp; mutual support', 'rose'),
               ('Voice in decisions that affect community life', 'violet')]
    pw = 118
    for i, (p, c) in enumerate(pillars):
        x = 85 + i * 138
        f.rect(x, 285, pw, 420, fill=f.vivid_for(c), rx=10, shadow=True)
        f.rect(x - 6, 285, pw + 12, 16, fill=col(c, 2), rx=4, shadow=False)
        f.rect(x - 6, 690, pw + 12, 16, fill=col(c, 2), rx=4, shadow=False)
        f.html(x + 2, 305, pw - 4, 380, '<div style="color:#fff;font-weight:700;font-size:16px">%s</div>' % p)
    f.rect(55, 712, 730, 50, fill=f.lingrad('#475569', '#1E293B'), rx=8, shadow=True)
    f.html(55, 712, 730, 50, 'Foundation: equitable power relations across gender, caste, class and indigeneity',
           size=14.5, color='#FFFFFF', weight=700)
    f.html(55, 770, 730, 70, '<i>Read intersectionally, each pillar is an arena of contestation: whose livelihoods, '
           'whose institutions, whose voice?</i>', size=14, color='#475569')
    # CBA cycle
    cx, cy, R = 1135, 500, 215
    stages = [('Participatory<br>assessment', 'Who is vulnerable, to what, and why?', 'rose'),
              ('Inclusive<br>planning', 'Priorities set with marginalised members', 'amber'),
              ('Locally led<br>action', 'Implement, resource and adapt', 'emerald'),
              ('Shared<br>learning', 'Monitor, reflect, adjust', 'blue')]
    f.circle(cx, cy, R, fill='none', stroke='#E2E8F0', sw=30)
    for i in range(4):
        a1 = -math.pi / 2 + (i + 0.2) * math.pi / 2
        a2 = -math.pi / 2 + (i + 0.8) * math.pi / 2
        f.path('M%.1f,%.1f A%d,%d 0 0 1 %.1f,%.1f' % (cx + R * math.cos(a1), cy + R * math.sin(a1), R, R,
                                                     cx + R * math.cos(a2), cy + R * math.sin(a2)),
               stroke=stages[(i + 1) % 4][2], sw=8, arrow=True)
    for i, (t, d, c) in enumerate(stages):
        a = -math.pi / 2 + i * math.pi / 2
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        f.card(x - 105, y - 62, 210, 124, t, d, color=c, title_size=15, header_h=50, body_size=13)
    f.circle(cx, cy, 95, fill=f.radgrad('#C4B5FD', '#5B21B6'), shadow=True)
    f.html(cx - 90, cy - 60, 180, 120, '<div style="color:#fff;font-weight:800;font-size:17px">LOCAL<br/>OWNERSHIP</div>'
           '<div style="color:#EDE9FE;font-size:12.5px;margin-top:4px">inclusive at every stage</div>')
    f.text(cx, 150, 'Community-Based Adaptation Cycle', size=19, weight=800, color=col('violet', 2))
    f.html(800, 780, 680, 80, 'The cycle is transformative only when assessment, planning, action and learning '
           'deliberately draw in the knowledge and priorities of marginalised members.', size=14, color='#475569',
           italic=True)
    f.save(os.path.join(OUT, 'Figure_3_Resilience_Pillars_Cycle.png'))


def fig4():
    f = Figure(1500, 760, title='An Integrated Framework for Intersectional, Community-Centred Climate Action',
               subtitle='Linking analysis of compounded vulnerability to inclusive governance and transformative outcomes')
    cols_ = [
        ('1 · ANALYSE', 'rose', 'Intersectional vulnerability assessment',
         ['Disaggregate data by gender, caste, class, age, disability, indigeneity', 'Map power and access to resources',
          'Participatory and community-led methods', 'Recognise local and indigenous knowledge']),
        ('2 · GOVERN', 'violet', 'Inclusive, accountable governance',
         ['Meaningful participation and representation', 'Recognition of rights and identities',
          'Redistribution of resources and finance', 'Accountability to the most marginalised']),
        ('3 · ACT', 'blue', 'Community-centred adaptation',
         ['Locally led, adequately financed action', 'Secure land, livelihoods and social protection',
          'Avoid maladaptation and elite capture', 'Strengthen collective institutions']),
        ('4 · TRANSFORM', 'emerald', 'Transformative, just outcomes',
         ['Reduced compounded vulnerability', 'Expanded capabilities and agency',
          'Shifted power relations', 'Durable, equitable resilience']),
    ]
    w, gap = 320, 40
    for i, (h, c, sub, items) in enumerate(cols_):
        x = 50 + i * (w + gap)
        body = ('<div style="text-align:left"><div style="font-weight:800;font-size:15.5px;margin-bottom:8px;'
                'color:%s">%s</div>' % (col(c, 2), sub) +
                ''.join('<div style="font-size:14.5px;line-height:1.45;margin-bottom:5px">• %s</div>' % t for t in items) +
                '</div>')
        f.card(x, 125, w, 320, h, body, color=c, title_size=19, header_h=56, valign='top')
        if i < 3:
            f.arrow(x + w + 4, 285, x + w + gap - 4, 285, color=c, sw=6)
    cc = [('Feminist lens', 'pink', 'gendered labour, care, devalued knowledge'),
          ('Decolonial lens', 'amber', 'histories of extraction; self-determination'),
          ('Justice lens', 'teal', 'distributive, procedural and recognitional')]
    f.text(750, 483, 'CROSS-CUTTING COMMITMENTS (apply at every stage)', size=15.5, weight=800, color='#334155', spacing=1.2)
    for i, (t, c, d) in enumerate(cc):
        x = 80 + i * 455
        f.soft(x, 500, 430, 84, '<div><b style="font-size:17px">%s</b><div style="font-size:14px;margin-top:4px;'
               'font-weight:500">%s</div></div>' % (t, d), color=c)
    f.path('M1452,330 C1490,420 1490,650 1300,650 L200,650 C10,650 10,420 48,330', stroke='indigo', sw=4,
           dash='12,7', arrow=True)
    f.pill(750, 650, 'Monitoring, evaluation & learning with communities: feeds back into analysis', color='indigo',
           size=14.5)
    f.html(100, 680, 1300, 60, 'Outcomes are judged by whether those at the densest intersections of disadvantage '
           'gain resources, rights and voice, not by aggregate community averages.', size=14.5, color='#475569',
           italic=True)
    f.save(os.path.join(OUT, 'Figure_4_Integrated_Framework.png'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    fig1()
    fig2()
    fig3()
    fig4()
