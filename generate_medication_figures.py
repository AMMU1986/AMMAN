#!/usr/bin/env python3
"""
Figures for the manuscript "AI-assisted medication-safety education for caregivers of
children with neurodevelopmental disorders" (manuscript_with_references.md), written as code.

    python3 generate_medication_figures.py          # all figures
    python3 generate_medication_figures.py 1 3      # selected figures

Figure 1 - Medication-safety practice (routine name/dose checking, Table 3)
Figure 2 - ADR / medication-error recognition (Table 3) and domain knowledge scores (Table 2)
Figure 3 - Caregiver confidence (3A, Table 3) and knowledge gain / retention (3B, text)
Figure 4 - Predictors of knowledge improvement (exploratory multivariable analysis)

Data policy: only values reported in the manuscript are plotted.  Storage and schedule
practices were reported as "improved" without numbers, and the multivariable analysis
reports the direction of association only, so these are drawn as labelled conceptual
elements with no invented values.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
from svgfig import Figure, Axes, col  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'medication_figures')

TIMES = ['Baseline', '4 weeks', '3 months']
NS = ['n = 170', 'n = 162', 'n = 157']
TCOL = ['slate', 'violet', 'teal']


def panel(f, x, y, w, h, letter, title, color):
    f.rect(x, y, w, h, fill='#FFFFFF', stroke=col(color, 1), sw=2, rx=16)
    f.panel_label(x + 14, y + 12, letter, color=color)
    f.text(x + 58, y + 32, title, size=16.5, weight=700, color=col(color, 2), anchor='start')


def time_ticks(ax, f, xs, with_n=True):
    for i, x in enumerate(xs):
        f.text(ax.px(x), ax.y + ax.h + 22, TIMES[i], size=13.5, weight=700, color='#334155')
        if with_n:
            f.text(ax.px(x), ax.y + ax.h + 40, NS[i], size=11.5, color='#64748B')


# --------------------------------------------------------------------------- Figure 1
def fig1():
    f = Figure(1400, 640, title='Medication-Safety Practices Before and After AI-Assisted Education',
               subtitle='Caregivers who routinely check the medication name and dose (Table 3)')
    panel(f, 20, 95, 820, 500, 'A', 'Routinely checks medication name and dose', 'violet')
    ax = Axes(f, 110, 160, 700, 350, (-0.6, 2.6), (0, 100), ylabel='Caregivers (%)',
              yticks=[0, 20, 40, 60, 80, 100])
    vals = [61.8, 89.5, 85.4]
    for i, v in enumerate(vals):
        ax.bar(i, v, 120, color=TCOL[i], label='%.1f%%' % v, label_size=15)
    time_ticks(ax, f, range(3))
    # change annotations
    f.pill(ax.px(0.5), ax.py(101) - 6, '+27.7 points', color='violet', size=12.5)
    f.pill(ax.px(1.5), ax.py(101) - 6, '−4.1 points', color='slate', size=12.5)

    panel(f, 860, 95, 520, 500, 'B', 'Other practices reported', 'teal')
    f.card(890, 160, 460, 120, 'Appropriate medication storage',
           'Reported as improved after the intervention; no percentages were reported.',
           color='teal', title_size=15, body_size=13.5, header_h=38)
    f.card(890, 300, 460, 120, 'Keeping to the medication schedule',
           'Reported as improved after the intervention; no percentages were reported.',
           color='sky', title_size=15, body_size=13.5, header_h=38)
    f.soft(890, 440, 460, 130,
           '<div style="text-align:left"><b>Reading the chart.</b> Percentages use the caregivers assessed at '
           'each time point as the denominator. The 3-month value stays 23.6 points above baseline.</div>',
           color='violet', size=13.5, weight=500, align='left')
    f.footnote('Only the name-and-dose item was quantified in the study; no values are drawn for storage or '
               'schedule practices.', y=620)
    f.save(os.path.join(OUT, 'Figure_1_Medication_Safety_Practices.png'))


# --------------------------------------------------------------------------- Figure 2
def fig2():
    f = Figure(1500, 680, title='Recognition of Medication Problems and Domain Knowledge Over Time',
               subtitle='Categorical recognition outcomes (Table 3) and domain knowledge scores, mean ± SD (Table 2)')
    panel(f, 20, 95, 720, 540, 'A', 'Recognition of medication problems (%)', 'rose')
    ax = Axes(f, 100, 250, 610, 300, (-0.6, 2.6), (0, 100), ylabel='Caregivers (%)',
              yticks=[0, 20, 40, 60, 80, 100])
    adr = [42.4, 85.8, 80.3]
    err = [48.8, 87.0, 82.8]
    for i in range(3):
        ax.bar(i - 0.17, adr[i], 64, color='rose', label='%.1f' % adr[i], label_size=12.5)
        ax.bar(i + 0.17, err[i], 64, color='amber', label='%.1f' % err[i], label_size=12.5)
    time_ticks(ax, f, range(3))
    f.legend(120, 172, [('Adequate ADR recognition (72/170, 139/162, 126/157)', 'rose'),
                        ('Medication-error recognition', 'amber')], cols=1, size=13, gap=22)

    panel(f, 760, 95, 720, 540, 'B', 'Domain knowledge scores (% correct)', 'blue')
    ax2 = Axes(f, 850, 250, 600, 300, (-0.3, 2.3), (25, 95), ylabel='Score (%, mean ± SD)',
               yticks=[30, 40, 50, 60, 70, 80, 90])
    series = [('ADR recognition', 'rose', [45.7, 75.4, 70.9], [16.3, 13.0, 13.7], -0.06),
              ('Medication-error prevention', 'amber', [53.6, 80.1, 76.3], [15.1, 11.8, 12.5], 0.0),
              ('Adherence and storage', 'teal', [54.9, 77.8, 73.6], [14.2, 11.5, 12.4], 0.06)]
    for name, c, m, sd, dx in series:
        xs = [i + dx for i in range(3)]
        for x, mv, s in zip(xs, m, sd):
            ax2.errorbar(x, max(25, mv - s), min(95, mv + s), color=col(c), cap=5, sw=1.6)
        ax2.line(xs, m, color=c, sw=3, r=6)
    time_ticks(ax2, f, range(3))
    f.legend(880, 160, [(s[0], s[1], 'line') for s in series], cols=1, size=13, gap=21)
    f.footnote('Error bars show ±1 SD. All domains rise to 4 weeks and '
               'fall slightly by 3 months while remaining above baseline.', y=662)
    f.save(os.path.join(OUT, 'Figure_2_ADR_Error_Adherence_Knowledge.png'))


# --------------------------------------------------------------------------- Figure 3
def fig3():
    f = Figure(1500, 660, title='Caregiver Confidence and Knowledge Retention',
               subtitle='Confidence on a 0–10 scale (Table 3) and overall knowledge gain relative to baseline (Table 2)')
    panel(f, 20, 95, 600, 520, '3A', 'Caregiver confidence (0–10)', 'indigo')
    ax = Axes(f, 100, 170, 490, 350, (-0.6, 2.6), (0, 10), ylabel='Confidence score (mean ± SD)',
              yticks=[0, 2, 4, 6, 8, 10])
    m, sd = [5.6, 8.1, 7.7], [1.8, 1.2, 1.4]
    for i in range(3):
        ax.bar(i, m[i], 96, color=TCOL[i] if i else 'slate')
        ax.errorbar(i, m[i] - sd[i], min(10, m[i] + sd[i]), color='#0F172A', cap=8, sw=2)
        f.text(ax.px(i), ax.py(0) - 18, '%.1f' % m[i], size=17, weight=800, color='#FFFFFF')
    time_ticks(ax, f, range(3))
    f.pill(ax.x + 70, ax.y + 18, 'P < 0.001', color='indigo', size=13)

    panel(f, 640, 95, 840, 520, '3B', 'Knowledge gain and retention', 'emerald')
    ax2 = Axes(f, 720, 170, 400, 350, (-0.6, 1.6), (0, 30), ylabel='Gain over baseline (points)',
               yticks=[0, 5, 10, 15, 20, 25, 30], xticks=None)
    gains = [26.8, 22.4]
    for i, g in enumerate(gains):
        ax2.bar(i, g, 120, color=['violet', 'teal'][i], label='+%.1f' % g, label_size=15)
    for i, (lab, sub) in enumerate([('4 weeks', '51.8 → 78.6%'), ('3 months', '51.8 → 74.2%')]):
        f.text(ax2.px(i), ax2.y + ax2.h + 22, lab, size=13.5, weight=700, color='#334155')
        f.text(ax2.px(i), ax2.y + ax2.h + 40, sub, size=11.5, color='#64748B')
    # retention ring
    cx, cy, r = 1300, 330, 105
    import math
    frac = 0.836
    f.circle(cx, cy, r, fill='none', stroke='#E2E8F0', sw=26)
    a0 = -math.pi / 2
    a1 = a0 + 2 * math.pi * frac
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    f.path('M%.1f,%.1f A%d,%d 0 1 1 %.1f,%.1f' % (x0, y0, r, r, x1, y1), stroke='emerald', sw=26)
    f.text(cx, cy + 4, '83.6%', size=30, weight=800, color=col('emerald', 2))
    f.text(cx, cy + 30, 'of the gain retained', size=13, weight=600, color='#334155')
    f.html(1170, 455, 260, 70, '<b>Retention</b> = 3-month gain ÷ 4-week gain = 22.4 ÷ 26.8',
           size=13, color='#334155')
    f.footnote('Knowledge values are overall scores (% correct): 51.8 ± 11.4 at baseline, 78.6 ± 9.8 at 4 weeks '
               'and 74.2 ± 10.3 at 3 months.', y=640)
    f.save(os.path.join(OUT, 'Figure_3_Confidence_and_Retention.png'))


# --------------------------------------------------------------------------- Figure 4
def fig4():
    f = Figure(1400, 650, title='Predictors of Improvement in Medication-Safety Knowledge',
               subtitle='Exploratory multivariable analysis: factors associated with a greater knowledge gain')
    preds = [
        ('Higher educational level', 'blue',
         'Graduate / postgraduate caregivers: 76 of 170 (44.7%)', '+'),
        ('Previous medication counselling', 'violet',
         'Prior medication-safety education: 58 of 170 (34.1%)', '+'),
        ('Baseline knowledge score', 'amber',
         'Baseline overall score 51.8 ± 11.4%; more room to improve', '−'),
    ]
    y = 105
    for name, c, body, sign in preds:
        f.card(60, y, 470, 130, name, body, color=c, title_size=16, body_size=13.5, header_h=42)
        f.badge(560, y + 65, sign, color=c, r=20, size=20)
        f.arrow(585, y + 65, 830, 330, color=col(c), sw=3.2, curve=0)
        y += 165
    f.rect(840, 220, 500, 220, fill=f.lingrad(col('emerald', 1), '#FFFFFF'), stroke=col('emerald'), sw=2.5, rx=22)
    f.text(1090, 285, 'Greater improvement in', size=20, weight=800, color=col('emerald', 2))
    f.text(1090, 315, 'medication-safety knowledge', size=20, weight=800, color=col('emerald', 2))
    f.html(870, 345, 440, 80, 'Outcome: change in overall knowledge score from baseline (mean gain 26.8 points '
           'at 4 weeks, 22.4 points at 3 months)', size=13.5, color='#334155')
    f.soft(860, 470, 460, 80, '<div style="text-align:left;padding-left:14px"><b>+</b>&#160; a higher level of the factor goes with a '
           'larger gain<br/><b>&#8722;</b>&#160; a lower level of the factor goes with a larger gain</div>',
           color='slate', size=13.5, weight=500, align='left')
    f.footnote('Direction of association only. Regression coefficients, confidence intervals and P values were not '
               'reported, so no effect sizes are drawn. Percentages describe the cohort (Table 1).', y=628)
    f.save(os.path.join(OUT, 'Figure_4_Predictors_of_Improvement.png'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:] or ['1', '2', '3', '4']
    for w in which:
        globals()['fig' + w]()
