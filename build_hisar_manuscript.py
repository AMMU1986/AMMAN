#!/usr/bin/env python3
"""
Assemble the Hisar infiltration manuscript.

  1. Reads hisar_manuscript_draft.md (text with {citation-keys} and
     {TABLE1}..{TABLE4} placeholders) and hisar_data/results.json.
  2. Builds Tables 1-4 from the analysis results, so the tables always match
     the data.
  3. Converts citation keys to Vancouver-style numbers in order of first
     citation and writes the reference list.
  4. Writes Manuscript_Hisar_Infiltration_Models.md and, using the raw-OOXML
     writer in create_intersectionality_docx.py, the .docx with the four
     figures embedded.

Run order:
    python3 hisar_infiltration_analysis.py
    python3 hisar_figures.py
    python3 build_hisar_manuscript.py
"""

import json
import os
import re

import create_intersectionality_docx as docx_writer

ROOT = os.path.dirname(os.path.abspath(__file__))
DRAFT = os.path.join(ROOT, 'hisar_manuscript_draft.md')
RES = os.path.join(ROOT, 'hisar_data', 'results.json')
OUT_MD = os.path.join(ROOT, 'Manuscript_Hisar_Infiltration_Models.md')
OUT_DOCX = os.path.join(ROOT, 'Manuscript_Hisar_Infiltration_Models.docx')

REFS = {
    'hillel': 'Hillel D. Introduction to Environmental Soil Physics. Amsterdam: Elsevier Academic Press; 2004.',
    'mishra': 'Mishra SK, Tyagi JV, Singh VP. Comparison of infiltration models. Hydrol Process. 2003;17(13):2629–52. doi:10.1002/hyp.1257',
    'chahinian': 'Chahinian N, Moussa R, Andrieux P, Voltz M. Comparison of infiltration models to simulate flood events at the field scale. J Hydrol. 2005;306(1–4):191–214. doi:10.1016/j.jhydrol.2004.09.009',
    'haghighi': 'Haghighi F, Gorji M, Shorafa M, Sarmadian F, Mohammadi MH. Evaluation of some infiltration models and hydraulic parameters. Span J Agric Res. 2010;8(1):210–7. doi:10.5424/sjar/2010081-1160',
    'bouwer': 'Bouwer H. Intake rate: cylinder infiltrometer. In: Klute A, editor. Methods of Soil Analysis, Part 1: Physical and Mineralogical Methods. 2nd ed. Madison (WI): ASA–SSSA; 1986. p. 825–44.',
    'astm': 'ASTM International. ASTM D3385: Standard test method for infiltration rate of soils in field using double-ring infiltrometer. West Conshohocken (PA): ASTM International.',
    'machiwal': 'Machiwal D, Jha MK, Mal BC. Modelling infiltration and quantifying spatial soil variability in a wasteland of Kharagpur, India. Biosyst Eng. 2006;95(4):569–82. doi:10.1016/j.biosystemseng.2006.08.007',
    'wosten': 'Wösten JHM, Pachepsky YA, Rawls WJ. Pedotransfer functions: bridging the gap between available basic soil data and missing soil hydraulic characteristics. J Hydrol. 2001;251(3–4):123–50. doi:10.1016/S0022-1694(01)00464-4',
    'sihag_gpr': 'Sihag P, Tiwari NK, Ranjan S. Modelling of infiltration of sandy soil using Gaussian process regression. Model Earth Syst Environ. 2017;3(3):1091–100. doi:10.1007/s40808-017-0357-1',
    'singh_rf': 'Singh B, Sihag P, Singh K. Modelling of impact of water quality on infiltration rate of soil by random forest regression. Model Earth Syst Environ. 2017;3(3):999–1004. doi:10.1007/s40808-017-0347-3',
    'vand': 'Vand AS, Sihag P, Singh B, Zand M. Comparative evaluation of infiltration models. KSCE J Civ Eng. 2018;22(10):4173–84. doi:10.1007/s12205-018-1347-1',
    'angelaki': 'Angelaki A, Singh Nain S, Singh V, Sihag P. Estimation of models for cumulative infiltration of soil using machine learning methods. ISH J Hydraul Eng. 2021;27(2):162–9. doi:10.1080/09715010.2018.1531274',
    'greenampt': 'Green WH, Ampt GA. Studies on soil physics, 1. The flow of air and water through soils. J Agric Sci. 1911;4(1):1–24.',
    'philip': 'Philip JR. The theory of infiltration: 4. Sorptivity and algebraic infiltration equations. Soil Sci. 1957;84(3):257–64.',
    'richards': 'Richards LA. Capillary conduction of liquids through porous mediums. Physics. 1931;1(5):318–33.',
    'kostiakov': 'Kostiakov AN. On the dynamics of the coefficient of water-percolation in soils and on the necessity for studying it from a dynamic point of view for purposes of amelioration. Trans 6th Comm Int Soc Soil Sci. 1932;Part A:17–21.',
    'horton': 'Horton RE. An approach toward a physical interpretation of infiltration-capacity. Soil Sci Soc Am Proc. 1941;5:399–417.',
    'turner': 'Turner ER. Comparison of infiltration equations and their field validation with rainfall simulation [MSc thesis]. College Park (MD): University of Maryland; 2006.',
    'sihag2017': 'Sihag P, Tiwari NK, Ranjan S. Estimation and inter-comparison of infiltration models. Water Sci. 2017;31(1):34–43. doi:10.1016/j.wsj.2017.03.001',
    'rasmussen': 'Rasmussen CE, Williams CKI. Gaussian Processes for Machine Learning. Cambridge (MA): MIT Press; 2006.',
    'breiman': 'Breiman L. Random forests. Mach Learn. 2001;45(1):5–32. doi:10.1023/A:1010933404324',
    'haykin': 'Haykin S. Neural Networks: A Comprehensive Foundation. 2nd ed. Upper Saddle River (NJ): Prentice Hall; 1999.',
    'roberts': 'Roberts DR, Bahn V, Ciuti S, Boyce MS, Elith J, Guillera-Arroita G, et al. Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography. 2017;40(8):913–29. doi:10.1111/ecog.02881',
    'bouyoucos': 'Bouyoucos GJ. Hydrometer method improved for making particle size analyses of soils. Agron J. 1962;54(5):464–5.',
    'blake': 'Blake GR, Hartge KH. Bulk density. In: Klute A, editor. Methods of Soil Analysis, Part 1: Physical and Mineralogical Methods. 2nd ed. Madison (WI): ASA–SSSA; 1986. p. 363–75.',
    'walkley': 'Walkley A, Black IA. An examination of the Degtjareff method for determining soil organic matter, and a proposed modification of the chromic acid titration method. Soil Sci. 1934;37(1):29–38.',
    'marquardt': 'Marquardt DW. An algorithm for least-squares estimation of nonlinear parameters. J Soc Ind Appl Math. 1963;11(2):431–41.',
    'kingma': 'Kingma DP, Ba J. Adam: a method for stochastic optimization. arXiv:1412.6980 [Preprint]. 2014.',
    'nash': 'Nash JE, Sutcliffe JV. River flow forecasting through conceptual models part I – a discussion of principles. J Hydrol. 1970;10(3):282–90. doi:10.1016/0022-1694(70)90255-6',
    'moriasi': 'Moriasi DN, Arnold JG, Van Liew MW, Bingner RL, Harmel RD, Veith TL. Model evaluation guidelines for systematic quantification of accuracy in watershed simulations. Trans ASABE. 2007;50(3):885–900.',
}

EMP = ['Kostiakov', 'Modified Kostiakov', 'Philip', 'Horton', 'Novel (Sihag et al.)']
ML = ['MLR', 'ANN', 'RF', 'GPR']


def fmt_bias(v):
    return '0.00' if abs(v) < 0.005 else '%+.2f' % v


def md_table(headers, rows):
    out = ['| ' + ' | '.join(headers) + ' |',
           '|' + '|'.join(['---'] * len(headers)) + '|']
    out += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out)


def table1(r):
    rows = []
    for s in r['sites']:
        rows.append([s['site'], s['land_use'], '%g' % s['sand'], '%g' % s['silt'],
                     '%g' % s['clay'], s['texture'], '%.2f' % s['bd'], '%.1f' % s['mc'],
                     '%.2f' % s['oc'], '%.1f' % s['f_initial'], '%.1f' % s['f_final']])
    return md_table(['Site', 'Land use', 'Sand (%)', 'Silt (%)', 'Clay (%)', 'Texture',
                     'BD (g/cm³)', 'MC (%)', 'OC (%)', 'Initial f (mm/h)', 'Final f (mm/h)'], rows)


def table2(r):
    units = {'a': '–', 'b': '–', 'ic': 'mm/h', 'S': 'mm/h^½', 'A': 'mm/h',
             'f0': 'mm/h', 'fc': 'mm/h', 'k': '1/min', 'c': '–'}
    rows = []
    for n in EMP:
        e = r['empirical'][n]
        ps = list(e['params'].values())
        r2 = list(e['site_r2'].values())
        for j, pn in enumerate(e['pnames']):
            v = [p[j] for p in ps]
            m = sum(v) / len(v)
            sd = (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5
            dec = 3 if max(abs(x) for x in v) < 1 else 2
            rows.append([n if j == 0 else '–', '%s (%s)' % (pn, units[pn]),
                         ('%.*f' % (dec, min(v))), ('%.*f' % (dec, max(v))),
                         ('%.*f ± %.*f' % (dec, m, dec, sd)),
                         '%.3f' % (sum(r2) / len(r2)) if j == 0 else '–'])
    return md_table(['Model', 'Parameter (unit)', 'Minimum', 'Maximum', 'Mean ± SD',
                     'Mean R²'], rows)


def table3(r):
    rows = []
    for n in EMP + ML:
        e = r['empirical'][n] if n in r['empirical'] else r['ml'][n]
        tr, te = e['train'], e['test']
        rows.append([n, '%.3f' % tr['CC'], '%.2f' % tr['RMSE'], '%.3f' % tr['NSE'],
                     '%.3f' % te['CC'], '%.2f' % te['RMSE'], '%.2f' % te['MAE'],
                     '%.3f' % te['NSE'], fmt_bias(te['Bias']), '%.0f' % te['within20']])
    return md_table(['Model', 'CC (train)', 'RMSE (train)', 'NSE (train)', 'CC (test)',
                     'RMSE (test)', 'MAE (test)', 'NSE (test)', 'Bias (test)',
                     '±20 % (test, %)'], rows)


def table4(r):
    rows = []
    for n in ML:
        e = r['leave_sites_out'][n]
        rows.append([n, '%.3f' % e['CC'], '%.2f' % e['RMSE'], '%.2f' % e['MAE'],
                     '%.3f' % e['NSE'], fmt_bias(e['Bias']), '%.0f' % e['within20'],
                     '%.2f' % r['ml'][n]['test']['RMSE']])
    folds = '; '.join('Fold %d: %s' % (i + 1, ', '.join(f)) for i, f in enumerate(r['lso_folds']))
    return md_table(['Model', 'CC', 'RMSE (mm/h)', 'MAE (mm/h)', 'NSE', 'Bias (mm/h)',
                     '±20 % (%)', 'RMSE, random split (mm/h)'], rows) + \
        '\n\nWithheld sites per fold: ' + folds + '.'


def cite(text):
    order = []

    def repl(m):
        keys = [k.strip() for k in m.group(1).split(',')]
        if not all(k in REFS for k in keys):
            return m.group(0)
        nums = []
        for k in keys:
            if k not in order:
                order.append(k)
            nums.append(order.index(k) + 1)
        return '[' + ','.join(str(x) for x in sorted(nums)) + ']'

    body = re.sub(r'\{([a-z_0-9, ]+)\}', repl, text)
    unused = [k for k in REFS if k not in order]
    if unused:
        raise SystemExit('Unused references: %s' % unused)
    reflist = '\n\n'.join('[%d] %s' % (i + 1, REFS[k]) for i, k in enumerate(order))
    return body, reflist


def move_captions_below(text):
    """Place 'Figure N. caption' paragraphs after the image placeholder."""
    return re.sub(r'(Figure (\d+)\. [^\n]+)\n\n(\[Insert Figure \2 here\])',
                  r'\3\n\n\1', text)


def main():
    with open(RES) as fh:
        r = json.load(fh)
    with open(DRAFT, encoding='utf-8') as fh:
        text = fh.read()
    for k, fn in [('TABLE1', table1), ('TABLE2', table2), ('TABLE3', table3), ('TABLE4', table4)]:
        text = text.replace('{%s}' % k, fn(r))
    text = move_captions_below(text)
    body, refs = cite(text.replace('{REFERENCES}', '@@REFS@@'))
    final = body.replace('@@REFS@@', refs)
    with open(OUT_MD, 'w', encoding='utf-8') as fh:
        fh.write(final)

    # word count of main text (title to end of Conclusions, excluding tables)
    main_text = final.split('## Data Availability')[0]
    main_text = '\n'.join(l for l in main_text.split('\n') if not l.startswith('|'))
    print('Main-text words (excl. tables, refs): %d' % len(re.findall(r'\S+', main_text)))
    print('Total words: %d' % len(re.findall(r'\S+', final)))

    docx_writer.FIG_DIR = os.path.join(ROOT, 'hisar_figures')
    docx_writer.FIGURE_FILES = {
        1: 'Figure_1_Methodology_Flowchart.png',
        2: 'Figure_2_Empirical_Model_Fits.png',
        3: 'Figure_3_ML_Observed_vs_Predicted.png',
        4: 'Figure_4_Model_Comparison_Sensitivity.png',
    }
    docx_writer.create_docx(OUT_MD, OUT_DOCX)


if __name__ == '__main__':
    main()
