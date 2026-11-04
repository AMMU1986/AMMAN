#!/usr/bin/env python3
"""
One-off migration: convert every document's figure placeholders into the
unified convention understood by tools/build_docx.py:

    ![Figure N](figure_dir/Figure_N_name.png)

    **Figure N.** Caption text ...

The image line is placed exactly where the figure belongs in the text.
"""
import re
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rw(name, fn):
    p = os.path.join(ROOT, name)
    s = open(p, encoding='utf8').read()
    s2 = fn(s)
    open(p, 'w', encoding='utf8').write(s2)
    print('normalized', name)


# ---- Agentic / Intersectionality / Design Thinking: "[Insert Figure N here]\nFigure N. Title"
def insert_style(figdir, files):
    def fn(s):
        def rep(m):
            n = int(m.group(1))
            title = m.group(2).strip()
            return f'![Figure {n}]({figdir}/{files[n]})\n\n**Figure {n}.** {title}'
        return re.sub(r'\[Insert Figure (\d+) here\]\s*\nFigure \d+\.\s*(.+)', rep, s)
    return fn


rw('Chapter_Agentic_AI_Autonomous_Systems.md', insert_style('agentic_figures', {
    1: 'Figure_1_Evolution_of_Agentic_AI.png',
    2: 'Figure_2_Agent_Architecture.png',
    3: 'Figure_3_Interoperability_Framework.png'}))

rw('Chapter_Intersectionality_Climate_Resilience.md', insert_style('intersectionality_figures', {
    1: 'Figure_1_Intersectional_Matrix.png',
    2: 'Figure_2_Vulnerability_Profiles.png',
    3: 'Figure_3_Resilience_Pillars_Cycle.png',
    4: 'Figure_4_Integrated_Framework.png'}))

rw('Chapter_Design_Thinking_Business_Functions.md', insert_style('design_thinking_figures', {
    1: 'Figure_1_Design_Thinking_Process.png',
    2: 'Figure_2_Customer_Experience_Framework.png',
    3: 'Figure_3_Business_Model_Innovation.png',
    4: 'Figure_4_Organizational_Readiness.png'}))


# ---- HRES: fix broken figure paths (figures/ belongs to Chapter 16)
rw('Chapter_Economic_Analysis_HRES.md',
   lambda s: s.replace('](figures/figure', '](HRES_figures/figure'))


# ---- Chapter 16: "[FIGURE N - See Figure_N.png]" + "Figure N: caption"
def ch16(s):
    s = re.sub(r'\[FIGURE (\d+) - See Figure_\d+\.png\]',
               lambda m: f'![Figure {m.group(1)}](figures/Figure_{m.group(1)}.png)', s)
    s = re.sub(r'^Figure (\d+): ', r'**Figure \1.** ', s, flags=re.M)
    return s


rw('Chapter_16_AI_Assisted_Design_of_Nanomaterials.md', ch16)

# ---- Chapter 4: "**Figure 4.N: caption**" -> image + caption
CH4 = {1: 'Figure_4_1_Ternary_Phase_Diagrams.png',
       2: 'Figure_4_2_SAW_Bead_Plate.png',
       3: 'Figure_4_3_Thermophysical_Properties.png',
       4: 'Figure_4_4_XRD_Patterns.png',
       5: 'Figure_4_5_FTIR_Spectra.png'}


def ch4(s):
    def rep(m):
        n = int(m.group(1))
        return f'![Figure 4.{n}](chapter4_figures/{CH4[n]})\n\n**Figure 4.{n}.** {m.group(2).strip()}'
    return re.sub(r'^\*\*Figure 4\.(\d+): (.+?)\*\*\s*$', rep, s, flags=re.M)


rw('Chapter_4_Experimentation.md', ch4)

# ---- Medication manuscript: "**Figure N:** caption"
MED = {1: 'Figure_1_Medication_Safety_Practices.png',
       2: 'Figure_2_ADR_Error_Adherence_Knowledge.png',
       3: 'Figure_3_Confidence_and_Retention.png',
       4: 'Figure_4_Predictors_of_Improvement.png'}


def med(s):
    def rep(m):
        n = int(m.group(1))
        return f'![Figure {n}](medication_figures/{MED[n]})\n\n**Figure {n}.** {m.group(2).strip()}'
    return re.sub(r'^\*\*Figure (\d+):\*\* (.+)$', rep, s, flags=re.M)


rw('manuscript_with_references.md', med)

# ---- Ionic-liquid manuscript: captions are listed at the end; move each
#      figure + caption to just after the paragraph that first cites it.
IL = {1: 'Figure_1_Experimental_Setup.png',
      2: 'Figure_2_FD_Model_Discretization.png',
      3: 'Figure_3_Machining_Forces.png',
      4: 'Figure_4_Temperature_Estimates.png',
      5: 'Figure_5_EDS_Surface.png'}


def il(s):
    caps = {}
    m = re.search(r'\n## Figure Captions\n(.*?)\n---\n', s, re.S)
    if not m:
        return s
    for cm in re.finditer(r'^\*\*Fig\. (\d+)\.\*\* (.+)$', m.group(1), re.M):
        caps[int(cm.group(1))] = cm.group(2).strip()
    s = s[:m.start()] + '\n' + s[m.end():]
    paras = s.split('\n\n')
    placed = set()
    out = []
    for p in paras:
        out.append(p)
        if p.startswith('#') or p.startswith('|'):
            continue
        for n in sorted(caps):
            if n in placed:
                continue
            if re.search(r'Fig(?:s?\.|ure)\s*%d\b' % n, p) or (n == 1 and 'experimental setup' in p.lower()):
                out.append(f'![Fig. {n}](manuscript_figures/{IL[n]})')
                out.append(f'**Fig. {n}.** {caps[n]}')
                placed.add(n)
    missing = set(caps) - placed
    if missing:
        print('  WARNING: IL figures not placed:', missing)
    return '\n\n'.join(out)


rw('Manuscript_Ionic_Liquids_MQL_Machining.md', il)
