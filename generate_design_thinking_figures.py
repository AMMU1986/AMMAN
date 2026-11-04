#!/usr/bin/env python3
"""
Figures for the chapter "Design Thinking across Business Functions" (written as code).

    python3 generate_design_thinking_figures.py

Figure 1 - The design thinking process model (five iterative stages)
Figure 2 - Design thinking-enabled customer experience framework
Figure 3 - Design thinking-enabled business model innovation process
Figure 4 - Organizational readiness framework for design thinking implementation
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
from svgfig import Figure, col  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'design_thinking_figures')


def ul(items, size=14, lh=1.55):
    return ('<div style="text-align:left;font-size:%spx;line-height:%s">' % (size, lh) +
            ''.join('<div>• %s</div>' % i for i in items) + '</div>')


def fig1():
    f = Figure(1500, 950, title='The Design Thinking Process Model',
               subtitle='Five interconnected, iterative stages of human-centred innovation')
    stages = [
        ('1', 'EMPATHIZE', 'rose', ['Observe and interview users', 'Immerse in context',
                                     'Uncover latent needs']),
        ('2', 'DEFINE', 'orange', ['Synthesize research', 'Frame a point of view',
                                    '"How might we…?" questions']),
        ('3', 'IDEATE', 'amber', ['Diverge: many ideas', 'Defer judgement',
                                   'Converge on concepts']),
        ('4', 'PROTOTYPE', 'emerald', ['Make ideas tangible', 'Low fidelity first',
                                        'Build to learn']),
        ('5', 'TEST', 'blue', ['Validate with real users', 'Measure and observe',
                                'Refine or pivot']),
    ]
    r, cy = 100, 395
    xs = [160 + i * 295 for i in range(5)]
    # iteration arcs above the circles (from TEST back to earlier stages)
    loops = [(3, 'emerald', 0, 'refine prototype'), (1, 'orange', 18, 're-define the problem'),
             (0, 'rose', 36, 'return to users')]
    labels = []
    for tgt, c, off, lab in loops:
        x1, x2 = xs[4] - 10 - off, xs[tgt] + 10 + off * 0.3
        top = cy - r - 14
        h = 34 + (xs[4] - xs[tgt]) * 0.075
        f.path('M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (x1, top, x1, top - h * 1.3, x2, top - h * 1.3, x2, top),
               stroke=c, sw=3.5, dash='9,6', arrow=True)
        labels.append(((x1 + x2) / 2, top - h * 0.98, lab, c))
    for lx, ly, lab, c in labels:
        f.pill(lx, ly, lab, color=c, size=13)
    for i, (n, name, c, items) in enumerate(stages):
        x = xs[i]
        f.circle(x, cy, r + 10, fill=col(c, 1), shadow=False)
        f.circle(x, cy, r, fill=f.radgrad(f_l(c), col(c)), shadow=True)
        f.html(x - r, cy - r + 10, 2 * r, 2 * r - 20,
               '<div style="color:#fff"><div style="font-size:38px;font-weight:800;line-height:1">%s</div>'
               '<div style="font-size:18px;font-weight:800;letter-spacing:1px;margin-top:6px">%s</div></div>'
               % (n, name))
        f.card(x - 128, 540, 256, 150, name.title(), ul(items), color=c, title_size=16, header_h=36,
               valign='top')
        f.line(x, cy + r + 10, x, 539, color=c, sw=2, dash='4,4')
        if i < 4:
            f.arrow(x + r + 12, cy, xs[i + 1] - r - 14, cy, color=c, sw=5)
    f.soft(32, 705, 696, 44, 'PROBLEM SPACE · understand the right problem', color='rose', size=15,
           shadow=False, weight=700)
    f.soft(772, 705, 696, 44, 'SOLUTION SPACE · build the right solution', color='blue', size=15,
           shadow=False, weight=700)
    g = f.lingrad(col('rose'), col('blue'), horizontal=True)
    f.rect(60, 772, 1380, 60, fill=g, rx=30, shadow=True)
    f.html(60, 772, 1380, 60, 'Human-centred  ·  Collaborative and cross-functional  ·  Bias toward action  ·  '
           'Comfort with ambiguity  ·  Learning through iteration', size=17, color='#FFFFFF', weight=700)
    f.html(100, 845, 1300, 80, 'Divergent thinking (Empathize, Ideate) alternates with convergent thinking '
           '(Define, Prototype, Test). In practice the stages overlap and repeat: a failed test may send a '
           'team back to re-define the problem rather than merely re-build the prototype.',
           size=14.5, color='#475569', italic=True)
    f.save(os.path.join(OUT, 'Figure_1_Design_Thinking_Process.png'))


def f_l(c):
    from svgfig import lerp_hex
    return lerp_hex(col(c), '#FFFFFF', 0.35)


def fig2():
    f = Figure(1500, 880, title='Design Thinking-Enabled Customer Experience Framework',
               subtitle='From empathetic research to integrated, continuously refined experience delivery')
    # stage 1: empathy research
    f.card(50, 175, 300, 450, 'EMPATHY & RESEARCH', ul([
        'Ethnographic observation', 'Customer interviews', 'Personas and empathy maps',
        'Journey mapping of moments that matter', 'Voice-of-customer and behavioural data',
        'Co-creation workshops with customers', 'Pain-point and emotion analysis',
        'Frontline employee insight']),
        color='rose', title_size=17, valign='top', body_size=16)
    # stage 2: experience strategy
    f.card(410, 175, 300, 450, 'EXPERIENCE STRATEGY', ul([
        'Experience vision and principles', 'Prioritised pain points and opportunities',
        'Target emotions at each touchpoint', 'Service blueprint (front- and back-stage)',
        'Moments-of-truth design', 'Omnichannel consistency rules',
        'Experience KPIs (NPS, CES, retention)']), color='violet', title_size=17, valign='top', body_size=16)
    for x in (352, 712):
        f.arrow(x, 400, x + 54, 400, color='slate', sw=5)
    # functional lanes
    lanes = [('Marketing', 'pink', 'Brand promise, communication, personalised engagement'),
             ('Operations', 'amber', 'Processes, service delivery, fulfilment and recovery'),
             ('Technology', 'cyan', 'Digital touchpoints, data platforms, self-service tools'),
             ('Human Resources', 'emerald', 'Frontline capability, culture, empowered employees')]
    f.text(1010, 140, 'CROSS-FUNCTIONAL CO-DELIVERY', size=15, weight=800, color='#334155', spacing=1.5)
    for i, (n, c, d) in enumerate(lanes):
        y = 160 + i * 132
        f.soft(770, y, 480, 112, '<div><div style="font-size:18px;font-weight:800">%s</div>'
               '<div style="font-size:14px;font-weight:500;margin-top:6px">%s</div></div>' % (n, d),
               color=c)
        f.arrow(1252, y + 56, 1288, 400 + (i - 1.5) * 40, color=c, sw=3)
    # integrated experience
    f.circle(1375, 400, 92, fill=f.radgrad('#93C5FD', '#1D4ED8'), shadow=True)
    f.html(1283, 330, 184, 140, '<div style="color:#fff;font-weight:800;font-size:17px">INTEGRATED<br/>CUSTOMER<br/>'
           'EXPERIENCE</div>')
    # touchpoint journey strip
    tps = [('Aware', 'rose'), ('Consider', 'orange'), ('Purchase', 'amber'), ('Use', 'emerald'),
           ('Support', 'cyan'), ('Loyalty & advocacy', 'violet')]
    f.text(750, 718, 'Customer journey touchpoints', size=15, weight=700, color='#334155')
    for i, (t, c) in enumerate(tps):
        x = 90 + i * 225
        f.tile(x, 735, 195, 52, t, color=c, size=15)
        if i < 5:
            f.arrow(x + 197, 761, x + 223, 761, color='slate', sw=2.5)
    # feedback loop
    f.path('M1440,465 C1500,560 1495,835 1320,835 L210,835 C90,835 70,720 150,628', stroke='emerald', sw=4,
           dash='12,7', arrow=True)
    f.pill(750, 835, 'Continuous feedback: test, measure, learn and refine', color='emerald', size=14.5)
    f.save(os.path.join(OUT, 'Figure_2_Customer_Experience_Framework.png'))


def fig3():
    f = Figure(1500, 900, title='Design Thinking-Enabled Business Model Innovation Process',
               subtitle='Empathetic research, creative ideation and iterative prototyping of value creation, delivery and capture')
    cx, cy, R = 520, 500, 300
    steps = [
        ('Empathetic market research', 'Unmet needs, jobs-to-be-done, ecosystem actors', 'rose'),
        ('Value proposition design', 'Gains, pains, differentiated offer', 'orange'),
        ('Business model ideation', 'Alternative canvases and revenue logics', 'amber'),
        ('Prototype the model', 'Mock-ups, pilots, minimum viable offers', 'emerald'),
        ('Market validation', 'Test assumptions with real customers', 'cyan'),
        ('Refine, scale or pivot', 'Evidence-based decision and roll-out', 'violet'),
    ]
    f.circle(cx, cy, R + 34, fill='none', stroke='#E2E8F0', sw=26)
    n = len(steps)
    pos = []
    for i in range(n):
        a = -math.pi / 2 + i * 2 * math.pi / n
        pos.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    for i in range(n):
        a1 = -math.pi / 2 + (i + 0.22) * 2 * math.pi / n
        a2 = -math.pi / 2 + (i + 0.78) * 2 * math.pi / n
        x1, y1 = cx + (R + 34) * math.cos(a1), cy + (R + 34) * math.sin(a1)
        x2, y2 = cx + (R + 34) * math.cos(a2), cy + (R + 34) * math.sin(a2)
        f.path('M%.1f,%.1f A%d,%d 0 0 1 %.1f,%.1f' % (x1, y1, R + 34, R + 34, x2, y2),
               stroke=steps[i][2], sw=7, arrow=True)
    for i, ((t, d, c), (x, y)) in enumerate(zip(steps, pos)):
        f.card(x - 120, y - 62, 240, 124, '%d · %s' % (i + 1, t), d, color=c, title_size=14.5,
               header_h=48, body_size=13.5)
    f.circle(cx, cy, 125, fill=f.radgrad('#C4B5FD', '#6D28D9'), shadow=True)
    f.html(cx - 115, cy - 80, 230, 160, '<div style="color:#fff"><div style="font-size:19px;font-weight:800">'
           'SUSTAINABLE<br/>BUSINESS MODEL</div><div style="font-size:13.5px;margin-top:8px">'
           'grounded in genuine human need</div></div>')
    # canvas panel
    f.text(1205, 130, 'Business Model Canvas', size=18, weight=800, color=col('indigo', 2))
    f.text(1205, 152, 'blocks iterated in every cycle', size=13.5, color='#64748B', italic=True)
    blocks = [('Key<br>partners', 'teal', 0, 0, 1, 2), ('Key<br>activities', 'cyan', 1, 0, 1, 1),
              ('Key<br>resources', 'sky', 1, 1, 1, 1), ('Value<br>propo-<br>sitions', 'rose', 2, 0, 1, 2),
              ('Customer<br>relation-<br>ships', 'pink', 3, 0, 1, 1), ('Channels', 'fuchsia', 3, 1, 1, 1),
              ('Customer<br>segments', 'purple', 4, 0, 1, 2)]
    X0, Y0, cw, chh = 960, 172, 98, 150
    for name, c, gx, gy, w, h in blocks:
        f.tile(X0 + gx * cw, Y0 + gy * chh, w * cw - 6, h * chh - 6, name, color=c, size=13, rx=8,
               shadow=False)
    f.tile(X0, Y0 + 2 * chh, 2.5 * cw - 6, 80, 'Cost structure', color='slate', size=14, rx=8, shadow=False)
    f.tile(X0 + 2.5 * cw, Y0 + 2 * chh, 2.5 * cw - 6, 80, 'Revenue streams', color='emerald', size=14,
           rx=8, shadow=False)
    f.arrow(900, 300, 952, 300, color='indigo', sw=3, dash='6,5')
    # assumption tests
    f.card(960, 600, 484, 235, 'Assumption testing at each loop', ul([
        '<b>Desirability</b> – do customers want it?', '<b>Feasibility</b> – can we deliver it?',
        '<b>Viability</b> – does it create and capture value?',
        '<b>Responsibility</b> – is it sustainable and fair?',
        'Kill, pivot or persevere using evidence, not opinion']), color='indigo', title_size=16,
        valign='top', body_size=14.5)
    f.save(os.path.join(OUT, 'Figure_3_Business_Model_Innovation.png'))


def fig4():
    f = Figure(1500, 1000, title='Organizational Readiness Framework for Design Thinking Implementation',
               subtitle='Diagnose barriers across four dimensions, then build capability through targeted enablers')
    dims = [
        ('CULTURAL', 'rose', 'Risk aversion · fear of failure · preference for analysis over experimentation',
         'Psychological safety · leadership role-modelling · celebrate learning from failure'),
        ('STRUCTURAL', 'orange', 'Functional silos · hierarchical approvals · misaligned incentives',
         'Cross-functional teams · delegated decision rights · team-based incentives'),
        ('CAPABILITY', 'emerald', 'Limited design skills · weak facilitation · little user-research know-how',
         'Training and coaching · design champions · toolkits and playbooks'),
        ('RESOURCE & MEASUREMENT', 'blue', 'No time or budget for exploration · ROI hard to show',
         'Protected innovation time · staged funding · learning and impact metrics'),
    ]
    f.text(330, 135, 'BARRIERS (diagnose)', size=16, weight=800, color=col('red', 2), spacing=1.5)
    f.text(1170, 135, 'ENABLERS (act)', size=16, weight=800, color=col('emerald', 2), spacing=1.5)
    for i, (d, c, bar, en) in enumerate(dims):
        y = 160 + i * 150
        f.soft(60, y, 520, 125, '<div style="text-align:left"><div style="font-size:13px;font-weight:800;'
               'color:#991B1B">✗ BARRIERS</div><div style="font-size:15px;font-weight:500;margin-top:6px">%s</div></div>'
               % bar, color='red', size=15, align='left')
        f.tile(625, y + 12, 250, 100, d, color=c, size=17)
        f.soft(920, y, 520, 125, '<div style="text-align:left"><div style="font-size:13px;font-weight:800;'
               'color:#065F46">✓ ENABLERS</div><div style="font-size:15px;font-weight:500;margin-top:6px">%s</div></div>'
               % en, color='emerald', size=15, align='left')
        f.arrow(582, y + 62, 622, y + 62, color='red', sw=3)
        f.arrow(877, y + 62, 917, y + 62, color='emerald', sw=3)
    # maturity ladder
    y0 = 790
    f.text(750, y0 - 12, 'Readiness / maturity levels', size=16, weight=800, color='#334155')
    lv = [('1 · Unaware', 'gray'), ('2 · Experimenting', 'amber'), ('3 · Projects', 'orange'),
          ('4 · Integrated', 'violet'), ('5 · Strategic & embedded', 'indigo')]
    for i, (t, c) in enumerate(lv):
        h = 50 + i * 22
        x = 80 + i * 272
        f.tile(x, y0 + 130 - h, 255, h, t, color=c, size=15)
    f.arrow(80, y0 + 152, 1420, y0 + 152, color='indigo', sw=4)
    f.text(750, y0 + 182, 'Assess current level on each dimension → prioritise the weakest → re-assess',
           size=14.5, color='#475569', italic=True)
    f.save(os.path.join(OUT, 'Figure_4_Organizational_Readiness.png'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    fig1()
    fig2()
    fig3()
    fig4()
