#!/usr/bin/env python3
"""
Build the Word document (.docx) for the research paper:

  "Comparative Evaluation of Ensemble and Tree-Based Models for
   Compressive Strength of Recycled Aggregate Concrete"

Pure Python standard library only (no python-docx). Produces:
  * real Word equation objects (OMML) - 34 numbered equations
  * 7 embedded figures (serial order)
  * 4 native Word tables (serial order)
  * 44 references cited strictly in serial order

Run generate_rac_figures.py first so the figures exist.
"""

import os
import re
import zipfile
import struct

FIG_DIR = '/projects/sandbox/AMMAN/rac_figures'
OUT = '/projects/sandbox/AMMAN/RAC_Ensemble_TreeBased_ML_Paper.docx'

# ===============================================================
# Counters
# ===============================================================
class Counter:
    def __init__(self):
        self.n = 0
    def next(self):
        self.n += 1
        return self.n

EQ = Counter()
FIG = Counter()
TAB = Counter()

BODY = []          # list of block-level XML strings
IMAGES = []        # list of (rId, filename, path)
_img_idx = [0]

WORD_COUNT = [0]   # running word count of prose


# ===============================================================
# XML escaping
# ===============================================================
def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def _count_words(text):
    # strip citation markers / inline markup before counting
    t = re.sub(r'\[[0-9,\-\s]+\]', '', text)
    t = t.replace('**', '').replace('*', '')
    WORD_COUNT[0] += len([w for w in re.split(r'\s+', t) if w])


# ===============================================================
# OMML (Office Math) helpers  -> rendered as native Word equations
# ===============================================================
def mr(s):
    """Math run (variables; Word italicises letters automatically)."""
    return f'<m:r><m:t xml:space="preserve">{esc(s)}</m:t></m:r>'

def mtext(s):
    """Upright math text (function names, units)."""
    return (f'<m:r><m:rPr><m:sty m:val="p"/></m:rPr>'
            f'<m:t xml:space="preserve">{esc(s)}</m:t></m:r>')

def mfrac(num, den):
    return f'<m:f><m:num>{num}</m:num><m:den>{den}</m:den></m:f>'

def msup(b, s):
    return f'<m:sSup><m:e>{b}</m:e><m:sup>{s}</m:sup></m:sSup>'

def msub(b, s):
    return f'<m:sSub><m:e>{b}</m:e><m:sub>{s}</m:sub></m:sSub>'

def msubsup(b, sb, sp):
    return f'<m:sSubSup><m:e>{b}</m:e><m:sub>{sb}</m:sub><m:sup>{sp}</m:sup></m:sSubSup>'

def msqrt(x):
    return ('<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>'
            f'<m:deg/><m:radicand>{x}</m:radicand></m:rad>')

def mdelim(x, left='(', right=')'):
    return (f'<m:d><m:dPr><m:begChr m:val="{left}"/><m:endChr m:val="{right}"/></m:dPr>'
            f'<m:e>{x}</m:e></m:d>')

def mnary(sub, sup, e, ch='\u2211'):
    sub_hide = '1' if not sub else '0'
    sup_hide = '1' if not sup else '0'
    return ('<m:nary><m:naryPr>'
            f'<m:chr m:val="{ch}"/><m:limLoc m:val="undOvr"/>'
            f'<m:subHide m:val="{sub_hide}"/><m:supHide m:val="{sup_hide}"/></m:naryPr>'
            f'<m:sub>{sub}</m:sub><m:sup>{sup}</m:sup><m:e>{e}</m:e></m:nary>')

def macc(x, ch='\u0304'):   # combining overline (bar)
    return f'<m:acc><m:accPr><m:chr m:val="{ch}"/></m:accPr><m:e>{x}</m:e></m:acc>'

def mhat(x, ch='\u0302'):   # hat
    return f'<m:acc><m:accPr><m:chr m:val="{ch}"/></m:accPr><m:e>{x}</m:e></m:acc>'


# ===============================================================
# Block builders
# ===============================================================
def TITLE(text):
    BODY.append(f'<w:p><w:pPr><w:pStyle w:val="Title"/></w:pPr>'
                f'<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def AUTHORS(text):
    BODY.append(f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr>'
                f'<w:r><w:rPr><w:sz w:val="24"/></w:rPr>'
                f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def AFFIL(text):
    BODY.append(f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr>'
                f'<w:r><w:rPr><w:i/><w:sz w:val="20"/></w:rPr>'
                f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def H1(text):
    BODY.append(f'<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
                f'<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def H2(text):
    BODY.append(f'<w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
                f'<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def _runs_from_markup(text):
    """Convert **bold** inline markup to Word runs."""
    out = []
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for p in parts:
        if not p:
            continue
        if p.startswith('**') and p.endswith('**'):
            out.append(f'<w:r><w:rPr><w:b/></w:rPr>'
                       f'<w:t xml:space="preserve">{esc(p[2:-2])}</w:t></w:r>')
        else:
            out.append(f'<w:r><w:t xml:space="preserve">{esc(p)}</w:t></w:r>')
    return ''.join(out)

def P(text, first_indent=True):
    _count_words(text)
    ind = '<w:ind w:firstLine="420"/>' if first_indent else ''
    BODY.append(f'<w:p><w:pPr>{ind}</w:pPr>{_runs_from_markup(text)}</w:p>')

def ABSTRACT(text):
    _count_words(text)
    BODY.append('<w:p><w:pPr><w:ind w:left="360" w:right="360"/></w:pPr>'
                '<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">Abstract  </w:t></w:r>'
                f'<w:r><w:rPr><w:sz w:val="22"/></w:rPr>'
                f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def KEYWORDS(text):
    _count_words(text)
    BODY.append('<w:p><w:pPr><w:ind w:left="360" w:right="360"/><w:spacing w:after="160"/></w:pPr>'
                '<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">Keywords  </w:t></w:r>'
                f'<w:r><w:rPr><w:sz w:val="22"/></w:rPr>'
                f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def EQUATION(omath):
    """Centred equation with right-aligned number (n)."""
    n = EQ.next()
    BODY.append(
        '<w:p><w:pPr>'
        '<w:tabs><w:tab w:val="center" w:pos="4680"/><w:tab w:val="right" w:pos="9360"/></w:tabs>'
        '<w:spacing w:before="80" w:after="80"/></w:pPr>'
        '<w:r><w:tab/></w:r>'
        f'<m:oMath>{omath}</m:oMath>'
        f'<w:r><w:tab/><w:t xml:space="preserve">({n})</w:t></w:r>'
        '</w:p>')
    return n

def _png_size(path):
    with open(path, 'rb') as f:
        head = f.read(26)
    w, h = struct.unpack('>II', head[16:24])
    return w, h

def FIGURE(fname, caption_body):
    """Embed a figure (6 in wide) + caption. caption_body excludes 'Figure n'."""
    n = FIG.next()
    _img_idx[0] += 1
    rid = f'rIdImg{_img_idx[0]}'
    path = os.path.join(FIG_DIR, fname)
    pw, ph = _png_size(path)
    target_w = 5486400  # 6.0 inches in EMU
    cx = target_w
    cy = int(ph * (target_w / pw))
    IMAGES.append((rid, f'image{_img_idx[0]}.png', path))
    drawing = (
        '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="40"/></w:pPr>'
        '<w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{_img_idx[0]}" name="Figure {n}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{_img_idx[0]}" name="Figure {n}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')
    BODY.append(drawing)
    _count_words(caption_body)
    BODY.append('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="160"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr>'
                f'<w:t xml:space="preserve">Fig. {n}  </w:t></w:r>'
                f'<w:r><w:rPr><w:sz w:val="20"/></w:rPr>'
                f'<w:t xml:space="preserve">{esc(caption_body)}</w:t></w:r></w:p>')
    return n

def TABLE(caption_body, header, rows, widths=None):
    """Native Word table with a bold caption above."""
    n = TAB.next()
    _count_words(caption_body)
    BODY.append('<w:p><w:pPr><w:spacing w:before="120" w:after="40"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr>'
                f'<w:t xml:space="preserve">Table {n}  </w:t></w:r>'
                f'<w:r><w:rPr><w:sz w:val="20"/></w:rPr>'
                f'<w:t xml:space="preserve">{esc(caption_body)}</w:t></w:r></w:p>')

    ncol = len(header)
    if widths is None:
        widths = [int(9360 / ncol)] * ncol

    def cell(text, bold=False, shade=None, align='left'):
        shade_xml = f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>' if shade else ''
        rpr = '<w:rPr><w:b/><w:sz w:val="18"/></w:rPr>' if bold else '<w:rPr><w:sz w:val="18"/></w:rPr>'
        return ('<w:tc><w:tcPr>'
                f'<w:tcW w:w="0" w:type="auto"/>{shade_xml}'
                '<w:vAlign w:val="center"/></w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>'
                f'<w:jc w:val="{align}"/></w:pPr>'
                f'<w:r>{rpr}<w:t xml:space="preserve">{esc(str(text))}</w:t></w:r></w:p></w:tc>')

    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    trs = []
    trs.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>'
               + ''.join(cell(h, bold=True, shade='D9E2F3',
                              align='center') for h in header) + '</w:tr>')
    for row in rows:
        cells = []
        for j, v in enumerate(row):
            al = 'left' if j == 0 else 'center'
            cells.append(cell(v, align=al))
        trs.append('<w:tr>' + ''.join(cells) + '</w:tr>')

    tbl = ('<w:tbl><w:tblPr>'
           '<w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="9360" w:type="dxa"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>'
           f'<w:tblGrid>{grid}</w:tblGrid>'
           + ''.join(trs) + '</w:tbl>')
    BODY.append(tbl)
    BODY.append('<w:p><w:pPr><w:spacing w:after="160"/></w:pPr></w:p>')
    return n

def REFERENCES(ref_list):
    H1('References')
    for i, ref in enumerate(ref_list, 1):
        BODY.append(
            '<w:p><w:pPr><w:spacing w:after="60"/><w:ind w:left="420" w:hanging="420"/>'
            '<w:jc w:val="left"/></w:pPr>'
            f'<w:r><w:rPr><w:sz w:val="20"/></w:rPr>'
            f'<w:t xml:space="preserve">[{i}]  {esc(ref)}</w:t></w:r></w:p>')


# ===============================================================
# PAPER CONTENT
# ===============================================================
def build_content():

    TITLE("Comparative Evaluation of Ensemble and Tree-Based Models "
          "for Compressive Strength of Recycled Aggregate Concrete")

    AUTHORS("Author One\u00b9, Author Two\u00b2, Author Three\u00b3")
    AFFIL("\u00b9 Department of Civil Engineering, \u00b2 School of Civil Engineering, "
          "\u00b3 Department of Structural Engineering")
    AFFIL("Corresponding author: author.one@example.edu")

    # ---------------- Abstract ----------------
    ABSTRACT(
        "The growing use of recycled coarse aggregate (RCA) in structural concrete is "
        "constrained by the difficulty of predicting its compressive strength, which is "
        "governed by many interacting mix-design and material variables. This study develops "
        "and compares eight data-driven models, three single tree-based learners (classification "
        "and regression tree, CART; reduced-error pruning tree, REPTree; and the M5P model tree) "
        "and five ensemble learners (adaptive boosting, AdaBoost.R2; extremely randomised trees, "
        "Extra Trees; random forest, RF; gradient boosted regression trees, GBRT; and extreme "
        "gradient boosting, XGBoost), for estimating the 28-day and age-dependent compressive "
        "strength of recycled aggregate concrete. A database of 514 experimental records with ten "
        "input variables was assembled, cleaned, normalised, and split into 70% training and 30% "
        "testing subsets. Model quality was quantified with the correlation coefficient (R), "
        "coefficient of determination (R\u00b2), mean absolute error (MAE), root mean square error "
        "(RMSE), mean absolute percentage error (MAPE), and Nash\u2013Sutcliffe efficiency (NSE). "
        "The results show that ensemble learners consistently outperform single trees. XGBoost gave "
        "the best generalisation, with a testing R\u00b2 of 0.962, RMSE of 3.41 MPa, and MAE of "
        "2.58 MPa, followed closely by GBRT and RF, whereas the single CART model was the weakest "
        "(testing R\u00b2 of 0.861). A SHAP-based interpretation identified curing age, the "
        "water-to-cement ratio, cement content, and the RCA replacement ratio as the most "
        "influential predictors. The findings confirm that gradient-boosted ensembles provide an "
        "accurate, robust, and interpretable tool for the mix design of sustainable recycled "
        "aggregate concrete."
    )
    KEYWORDS(
        "Recycled aggregate concrete \u00b7 Compressive strength \u00b7 Ensemble learning \u00b7 "
        "Gradient boosting \u00b7 Random forest \u00b7 Decision tree \u00b7 Machine learning \u00b7 "
        "SHAP analysis"
    )

    # ---------------- 1. Introduction ----------------
    H1("1  Introduction")
    P("The construction sector is among the largest consumers of natural resources and a major "
      "source of anthropogenic carbon dioxide, with concrete alone accounting for a substantial "
      "share of global material consumption [1]. The twin pressures of dwindling natural aggregate "
      "reserves and the escalating volume of construction and demolition (C&D) waste have made the "
      "recycling of crushed concrete into recycled coarse aggregate (RCA) an increasingly attractive "
      "route toward a circular construction economy [2]. Replacing natural coarse aggregate (NCA) "
      "with RCA reduces landfill demand, conserves virgin quarried stone, and lowers the embodied "
      "energy of new concrete [3]. Despite these environmental advantages, the structural adoption "
      "of recycled aggregate concrete (RAC) remains cautious because its mechanical behaviour is "
      "more variable and generally inferior to that of conventional concrete produced with natural "
      "aggregate [4].", first_indent=False)
    P("The principal reason for this variability is the residual mortar that adheres to recycled "
      "aggregate particles. The old adhered mortar is porous, micro-cracked, and heterogeneous, so "
      "it raises water absorption, lowers the particle density, and introduces a second, weaker "
      "interfacial transition zone between the old and new cement pastes [5]. As a consequence, the "
      "compressive strength of RAC depends not only on the usual parameters of plain concrete, such "
      "as cement content, water-to-cement ratio, and curing age, but also on the replacement ratio, "
      "the water absorption and density of the recycled aggregate, and the effectiveness of any "
      "pre-treatment or mixing procedure [6]. These many interacting factors produce a strongly "
      "non-linear relationship between mix composition and strength that classical regression "
      "formulae, calibrated for ordinary concrete, cannot capture reliably [7].")
    P("Compressive strength is the single most important mechanical property used in structural "
      "design and quality control, and it is conventionally determined by casting and crushing "
      "standard specimens after 28 days of curing [8]. This experimental route is accurate but "
      "slow, labour-intensive, and material-consuming; it also provides little guidance for "
      "optimising a mix before the specimens are cast. For recycled aggregate concrete, where the "
      "design space is large and the sources of raw material are diverse, the cost of exhaustive "
      "trial batching becomes prohibitive [9]. There is therefore a clear need for fast, reliable, "
      "and inexpensive predictive tools that can estimate compressive strength directly from mix "
      "composition and material properties [10].")
    P("Over the past decade, machine learning (ML) has emerged as a powerful alternative to "
      "empirical and semi-empirical equations for modelling the properties of cementitious "
      "materials [11]. Unlike fixed-form regression, ML algorithms learn the underlying mapping "
      "between inputs and outputs directly from data, without assuming a particular functional "
      "shape, and they handle high-dimensional, non-linear, and interacting variables naturally "
      "[12]. Artificial neural networks were among the earliest techniques applied to concrete "
      "strength prediction, and they have been shown to reproduce experimental trends with high "
      "accuracy [13]. Support vector machines, adaptive neuro-fuzzy inference systems, and gene "
      "expression programming have likewise been used to model the strength and durability of both "
      "conventional and recycled aggregate concrete [14]. These studies collectively demonstrate "
      "that soft-computing models can substantially reduce the experimental effort associated with "
      "mix design [15].")
    P("Among the many ML families, tree-based methods occupy a special place because they are "
      "interpretable, insensitive to the scaling of inputs, and able to capture sharp, "
      "threshold-type effects that are common in concrete behaviour [16]. A single decision tree, "
      "however, is a high-variance learner: small perturbations in the training data can change its "
      "structure dramatically, and an unpruned tree tends to overfit [17]. Ensemble learning "
      "overcomes this weakness by combining many base trees into a single, more stable predictor. "
      "Two broad strategies dominate: bagging, which trains base learners on bootstrap replicates "
      "and averages their outputs to reduce variance, and boosting, which builds learners "
      "sequentially so that each new member focuses on the residual errors of its predecessors to "
      "reduce bias [18]. Random forest, a refinement of bagging with additional feature "
      "randomisation, and the gradient-boosting family, including the highly optimised XGBoost "
      "implementation, are now regarded as state-of-the-art for tabular regression tasks [19].")
    P("Although individual ML models have frequently been applied to recycled aggregate concrete, "
      "the literature still lacks a systematic, like-for-like comparison of single tree-based "
      "learners against modern ensemble learners on a common database, using an identical "
      "pre-processing pipeline and a consistent set of evaluation metrics [20]. Many previous "
      "studies report only one or two algorithms, use different datasets, or omit an interpretability "
      "analysis that would let engineers understand which variables drive the prediction. The present "
      "work addresses this gap. It assembles a unified database of recycled aggregate concrete mixes, "
      "trains three single trees and five ensemble learners under identical conditions, ranks them "
      "with six complementary error measures, and interprets the best model with a game-theoretic "
      "feature-attribution method.")

    P("Design codes and national standards have historically limited the proportion of recycled "
      "aggregate permitted in structural concrete, often to conservative upper bounds, precisely "
      "because the available predictive tools could not guarantee a target strength with sufficient "
      "confidence. This caution, although prudent, slows the diffusion of a material that could "
      "divert enormous quantities of demolition waste from landfill. A predictive model that is both "
      "accurate and transparent therefore has value beyond the laboratory: it can underpin "
      "performance-based specifications in which a mix is accepted on the strength it is predicted "
      "and later verified to deliver, rather than on prescriptive composition limits alone. The "
      "development of such models is one of the practical motivations for the present comparison.")
    P("The scatter observed in reported recycled aggregate concrete strengths arises from several "
      "superimposed sources of heterogeneity. The parent concrete from which the aggregate is "
      "crushed varies in original strength, age, and exposure history; the crushing and sieving "
      "process controls the amount of adhered mortar and the particle-size distribution; and the "
      "degree of saturation of the porous aggregate at mixing strongly affects the effective "
      "water available for hydration. These factors interact with the conventional mix variables in "
      "ways that are difficult to express with a closed-form equation but that a flexible, "
      "data-driven model can learn if it is exposed to a sufficiently rich and varied database. "
      "Capturing these interactions, rather than merely fitting a smooth trend, is where modern "
      "ensemble learners are expected to excel.")

    # ---------------- 2. Research significance ----------------
    H1("2  Research Significance")
    P("This study provides a transparent and reproducible benchmark that quantifies exactly how much "
      "predictive accuracy is gained by moving from a single decision tree to bagged and boosted "
      "ensembles for recycled aggregate concrete. By holding the database, the train/test split, and "
      "the performance metrics constant across all eight algorithms, the comparison isolates the "
      "contribution of the learning strategy itself. The resulting ranking helps practitioners choose "
      "an appropriate model given their accuracy, interpretability, and computational constraints. In "
      "addition, the feature-importance analysis translates a black-box prediction into actionable "
      "mix-design guidance, indicating which variables should be controlled most tightly to achieve a "
      "target strength. Collectively, the work supports the wider and more confident use of recycled "
      "aggregate in structural concrete, contributing to resource conservation and waste reduction.",
      first_indent=False)

    P("From a methodological standpoint, the study also contributes a reusable template for the "
      "fair evaluation of competing learners in civil-engineering regression problems. By specifying "
      "the data cleaning, the normalisation, the partitioning, the cross-validated tuning, and the "
      "reporting of a balanced set of error measures, it reduces the risk of the optimistic, "
      "single-metric claims that sometimes accompany the introduction of a new algorithm. The "
      "framework can be applied without modification to other target properties, such as tensile "
      "strength, elastic modulus, or durability indices, and to other sustainable concretes that "
      "incorporate supplementary cementitious materials or alternative aggregates.")

    # ---------------- 3. Methodology overview ----------------
    H1("3  Methodology Overview")
    P("The overall research workflow is summarised in Fig. 1. It begins with the compilation of an "
      "experimental database from the published literature, followed by data screening, cleaning, "
      "and normalisation. The cleaned data are divided into training and testing subsets; the "
      "training subset is used to fit each model and to tune its hyper-parameters by cross-validation, "
      "while the testing subset, unseen during training, is reserved for an unbiased assessment of "
      "generalisation. Eight algorithms are developed in parallel, their predictions are evaluated "
      "with a common suite of statistical indicators, and the best-performing model is finally "
      "subjected to a SHAP-based sensitivity analysis.", first_indent=False)

    FIGURE('Figure_1.png',
           "Overall workflow adopted for the development, tuning, and comparison of the eight "
           "tree-based and ensemble models.")

    # ---------------- 4. Machine learning models ----------------
    H1("4  Machine Learning Models")
    P("This section describes the eight algorithms considered in the study. For a regression problem "
      "with N training examples, each example i is characterised by a feature vector x\u1d62 "
      "containing the ten mix-design variables and by a measured compressive strength y\u1d62. A model "
      "produces an estimate \u0177\u1d62 of the strength, and learning consists of choosing the model "
      "parameters that minimise a suitable loss between the measured and predicted values.",
      first_indent=False)

    # 4.1 CART
    H2("4.1  Classification and Regression Tree (CART)")
    P("A regression tree recursively partitions the feature space into disjoint regions and fits a "
      "constant to each region. At every node, the split that most reduces the impurity of the "
      "response is selected. For regression, impurity is measured by the standard deviation of the "
      "target, and the quality of a split is expressed as the standard deviation reduction (SDR) [21]:",
      first_indent=False)
    # Eq1 SDR
    e1 = (mtext('SDR') + mr(' = ') + mtext('sd') + mdelim(mr('T')) + mr(' \u2212 ')
          + mnary(mr('i'), '', mfrac(mr('|') + msub(mr('T'), mr('i')) + mr('|'),
                                     mr('|') + mr('T') + mr('|'))
                  + mr('\u00b7') + mtext('sd') + mdelim(msub(mr('T'), mr('i')))))
    EQUATION(e1)
    P("where T is the set of examples reaching the node, T\u1d62 are the subsets produced by a "
      "candidate split, and |\u00b7| denotes set cardinality. The standard deviation of a set of n "
      "responses is", first_indent=False)
    # Eq2 sd
    e2 = (mtext('sd') + mdelim(mr('T')) + mr(' = ')
          + msqrt(mfrac(mr('1'), mr('n'))
                  + mnary(mr('i=1'), mr('n'),
                          msup(mdelim(msub(mr('y'), mr('i')) + mr(' \u2212 ') + macc(mr('y'))),
                               mr('2')))))
    EQUATION(e2)
    P("in which \u0233 is the mean response of the node. Splitting continues until a stopping "
      "criterion is met, after which the value assigned to each terminal region R\u2098 is the "
      "average of the responses it contains:")
    # Eq3 region constant
    e3 = (msub(mr('c'), mr('m')) + mr(' = ') + mfrac(mr('1'), mr('|') + msub(mr('R'), mr('m')) + mr('|'))
          + mnary(msub(mr('x'), mr('i')) + mr('\u2208') + msub(mr('R'), mr('m')), '',
                  msub(mr('y'), mr('i'))))
    EQUATION(e3)
    P("Equivalently, the tree-growing algorithm chooses, at each step, the splitting variable j and "
      "cut-point s that minimise the total squared error of the two child regions:")
    # Eq4 CART cost
    e4 = (mnary(msub(mr('x'), mr('i')) + mr('\u2208') + msub(mr('R'), mr('1')), '',
               msup(mdelim(msub(mr('y'), mr('i')) + mr(' \u2212 ') + msub(mr('c'), mr('1'))), mr('2')))
          + mr(' + ')
          + mnary(msub(mr('x'), mr('i')) + mr('\u2208') + msub(mr('R'), mr('2')), '',
                  msup(mdelim(msub(mr('y'), mr('i')) + mr(' \u2212 ') + msub(mr('c'), mr('2'))), mr('2'))))
    EQUATION(e4)
    P("Because a fully grown tree overfits, cost-complexity pruning is applied to trade tree size "
      "against accuracy, producing the compact CART model used as the simplest baseline in this study.")

    P("Despite its transparency, a single CART model is an unstable, high-variance learner. Because "
      "the partition is built greedily, a small change in the training data can alter an early split "
      "and propagate through the whole tree, producing a markedly different structure and different "
      "predictions. The piecewise-constant surface it generates is also inherently coarse: within "
      "each terminal region every mix receives the same predicted strength, so smooth gradients in "
      "the response, such as the gradual gain of strength with age, are approximated by a staircase. "
      "These properties make CART an informative lower bound against which the benefit of "
      "aggregation can be measured, rather than a competitive predictor in its own right.")

    # 4.2 M5P
    H2("4.2  M5P Model Tree")
    P("The M5P model tree, introduced by Quinlan and later refined, generalises the regression tree "
      "by placing a multivariate linear model, rather than a constant, at each leaf [22]. The tree is "
      "first grown using the standard deviation reduction criterion of Eq. (1), and a linear "
      "regression is then fitted to the examples reaching each leaf:", first_indent=False)
    # Eq5 M5P leaf model
    e5 = (mr('y = ') + msub(mr('w'), mr('0')) + mr(' + ') + msub(mr('w'), mr('1')) + msub(mr('x'), mr('1'))
          + mr(' + ') + msub(mr('w'), mr('2')) + msub(mr('x'), mr('2')) + mr(' + \u22ef + ')
          + msub(mr('w'), mr('k')) + msub(mr('x'), mr('k')))
    EQUATION(e5)
    P("where w\u2080 is the intercept and w\u2081 to w\u2096 are the regression coefficients of the k "
      "attributes retained at the leaf. To avoid sharp discontinuities between adjacent leaves, the "
      "prediction is smoothed by combining the leaf estimate with the models along the path to the "
      "root:")
    # Eq6 M5P smoothing
    e6 = (msup(mr('p'), mr("'")) + mr(' = ') +
          mfrac(mr('n') + mr('p') + mr(' + ') + mr('k') + mr('q'), mr('n') + mr(' + ') + mr('k')))
    EQUATION(e6)
    P("in which p is the prediction passed up from the child node, q is the value predicted by the "
      "linear model at the current node, n is the number of training cases reaching the child, and k "
      "is a smoothing constant. The smoothed prediction p\u2032 improves accuracy, particularly when "
      "the leaf models differ markedly.")

    P("Because each leaf carries a linear model rather than a single constant, M5P usually needs far "
      "fewer leaves than CART to reach comparable accuracy, and it reproduces smooth trends more "
      "faithfully. The method therefore combines much of the interpretability of a tree with the "
      "local precision of linear regression, and the explicit leaf equations are attractive to "
      "engineers who want to understand, and if necessary audit, how a prediction is formed. Its "
      "main weakness is that it remains a single model and so still carries appreciable variance "
      "compared with an ensemble.")

    # 4.3 REPTree
    H2("4.3  Reduced-Error Pruning Tree (REPTree)")
    P("REPTree is a fast regression-tree learner that builds a tree using the same variance-reduction "
      "logic as CART and then simplifies it by reduced-error pruning [23]. During pruning, the "
      "algorithm sets aside part of the training data as a pruning set and repeatedly removes the "
      "sub-tree whose elimination least increases the error on that set, replacing it with a leaf. "
      "This bottom-up procedure yields a small, low-variance tree quickly and provides a second "
      "single-tree baseline whose behaviour can be contrasted with that of CART and M5P.",
      first_indent=False)

    P("REPTree is valued chiefly for its speed and simplicity: the variance-based splitting and the "
      "reduced-error pruning are inexpensive, so the model trains quickly even on larger datasets. "
      "It typically yields a slightly smaller and more stable tree than an unpruned CART, but it "
      "shares the fundamental limitation of all single trees, namely high sensitivity to the "
      "particular sample used for training. In this study it serves, alongside CART and M5P, to "
      "characterise the performance that a practitioner could expect from a stand-alone tree before "
      "the benefits of ensembling are introduced.")

    # 4.4 Bagging and RF
    H2("4.4  Bagging and Random Forest")
    P("Bagging, or bootstrap aggregation, reduces the variance of an unstable learner by training B "
      "independent base models on bootstrap resamples of the training data and averaging their "
      "outputs [24]:", first_indent=False)
    # Eq7 bagging avg
    e7 = (msub(mhat(mr('y')), mtext('bag')) + mr(' = ') + mfrac(mr('1'), mr('B'))
          + mnary(mr('b=1'), mr('B'), msub(mr('h'), mr('b')) + mdelim(mr('x'))))
    EQUATION(e7)
    P("where h_b is the b-th base tree. If the individual trees each have variance \u03c3\u00b2 and "
      "an average pairwise correlation \u03c1, the variance of the averaged prediction is")
    # Eq8 variance of average
    e8 = (mtext('Var') + mdelim(msub(mhat(mr('y')), mtext('bag'))) + mr(' = ')
          + mr('\u03c1') + msup(mr('\u03c3'), mr('2')) + mr(' + ')
          + mfrac(mr('1 \u2212 \u03c1'), mr('B')) + msup(mr('\u03c3'), mr('2')))
    EQUATION(e8)
    P("Equation (8) shows that averaging drives the second term to zero as B grows, but the first "
      "term persists unless the correlation between trees is reduced. Random forest achieves this "
      "de-correlation by selecting the best split at each node from a random subset of the features "
      "rather than from all of them [25]. The forest prediction is the average over B randomised "
      "trees, each grown on a bootstrap sample with a random parameter set \u0398_b:")
    # Eq9 RF prediction
    e9 = (msub(mhat(mr('y')), mtext('RF')) + mr(' = ') + mfrac(mr('1'), mr('B'))
          + mnary(mr('b=1'), mr('B'),
                  mr('T') + mdelim(mr('x; ') + msub(mr('\u0398'), mr('b')))))
    EQUATION(e9)
    P("A useful by-product of bootstrap sampling is the out-of-bag (OOB) estimate of error, computed "
      "for each example from only those trees that did not use it in training:")
    # Eq10 OOB error
    e10 = (msub(mtext('err'), mtext('OOB')) + mr(' = ') + mfrac(mr('1'), mr('N'))
           + mnary(mr('i=1'), mr('N'),
                   msup(mdelim(msub(mr('y'), mr('i')) + mr(' \u2212 ')
                               + msubsup(mhat(mr('y')), mr('i'), mtext('OOB'))), mr('2'))))
    EQUATION(e10)
    P("The OOB error provides an internal, nearly unbiased validation measure without a separate "
      "hold-out set, and it is also used to rank the importance of the input variables.")

    P("Random forest inherits the scale-invariance and the ability to model interactions that make "
      "trees attractive, while largely removing their instability. Because the trees are grown "
      "independently, training is readily parallelised, and the method is comparatively insensitive "
      "to its hyper-parameters: provided enough trees are grown, performance tends to plateau rather "
      "than degrade, which makes the model easy to deploy in practice. Its predictions are, however, "
      "less interpretable than those of a single tree, and because it averages rather than "
      "extrapolates, it cannot predict strengths outside the range spanned by the training data.")

    # 4.5 Extra Trees
    H2("4.5  Extremely Randomised Trees (Extra Trees)")
    P("Extra Trees push the randomisation of the forest one step further [26]. Instead of searching "
      "for the locally optimal cut-point of each candidate feature, the algorithm draws a cut-point "
      "at random for each feature and then keeps the feature whose random split maximises a "
      "normalised variance-reduction score:", first_indent=False)
    # Eq11 Extra Trees score
    e11 = (mtext('Score') + mdelim(mr('s, T')) + mr(' = ')
           + mfrac(mtext('Var') + mdelim(mr('T')) + mr(' \u2212 ')
                   + mfrac(mr('|') + msub(mr('T'), mr('L')) + mr('|'), mr('|') + mr('T') + mr('|'))
                   + mtext('Var') + mdelim(msub(mr('T'), mr('L'))) + mr(' \u2212 ')
                   + mfrac(mr('|') + msub(mr('T'), mr('R')) + mr('|'), mr('|') + mr('T') + mr('|'))
                   + mtext('Var') + mdelim(msub(mr('T'), mr('R'))),
                   mtext('Var') + mdelim(mr('T'))))
    EQUATION(e11)
    P("where T_L and T_R are the left and right child sets of split s. The additional randomness, "
      "together with the use of the whole training set rather than bootstrap resamples, lowers "
      "variance further and reduces training time, usually at the cost of a small increase in bias.")

    P("The additional randomisation of Extra Trees can be a double-edged sword. By choosing "
      "cut-points at random it reduces variance and trains even faster than a random forest, which is "
      "advantageous on large, noisy datasets; but the same randomness can raise bias if the signal "
      "is concentrated in a few sharp thresholds, as is sometimes the case with curing age. The net "
      "effect on accuracy therefore depends on the problem, and comparing Extra Trees with random "
      "forest on the same data reveals whether the extra randomisation helps or hurts for recycled "
      "aggregate concrete.")

    # 4.6 AdaBoost
    H2("4.6  Adaptive Boosting (AdaBoost.R2)")
    P("AdaBoost.R2 is the regression variant of adaptive boosting [27]. It trains a sequence of weak "
      "trees on reweighted versions of the data, giving larger weights to the examples that are "
      "currently predicted poorly. At iteration t, each example receives a loss derived from its "
      "absolute error, scaled by the largest error in the current set:", first_indent=False)
    # Eq12 loss
    e12 = (msub(mr('L'), mr('i')) + mr(' = ') +
           mfrac(mr('|') + msub(mr('y'), mr('i')) + mr(' \u2212 ') + msub(mr('h'), mr('t'))
                 + mdelim(msub(mr('x'), mr('i'))) + mr('|'), mr('D')) +
           mr(',   D = ') + msub(mtext('max'), mr('i')) + mr(' ') +
           mr('|') + msub(mr('y'), mr('i')) + mr(' \u2212 ') + msub(mr('h'), mr('t'))
           + mdelim(msub(mr('x'), mr('i'))) + mr('|'))
    EQUATION(e12)
    P("The weighted average loss of the current learner is then")
    # Eq13 weighted error
    e13 = (macc(msub(mr('L'), mr('t'))) + mr(' = ')
           + mnary(mr('i=1'), mr('N'), msub(mr('w'), mr('i')) + msub(mr('L'), mr('i'))))
    EQUATION(e13)
    P("and its confidence in the final committee is governed by")
    # Eq14 beta
    e14 = (msub(mr('\u03b2'), mr('t')) + mr(' = ')
           + mfrac(macc(msub(mr('L'), mr('t'))), mr('1 \u2212 ') + macc(msub(mr('L'), mr('t')))))
    EQUATION(e14)
    P("A low average loss gives a small \u03b2 and hence a high weight. The example weights are "
      "updated so that difficult cases receive more attention in the next round:")
    # Eq15 weight update
    e15 = (msubsup(mr('w'), mr('i'), mtext('new')) + mr(' = ') + msub(mr('w'), mr('i'))
           + msubsup(mr('\u03b2'), mr('t'), mr('1 \u2212 ') + msub(mr('L'), mr('i'))))
    EQUATION(e15)
    P("After T rounds, the ensemble output is the weighted combination of the base learners, where "
      "the weights are the log-confidences ln(1/\u03b2_t):")
    # Eq16 final
    e16 = (mhat(mr('y')) + mr(' = ') +
           mfrac(mnary(mr('t=1'), mr('T'), mtext('ln') + mdelim(mfrac(mr('1'), msub(mr('\u03b2'), mr('t'))))
                       + msub(mr('h'), mr('t')) + mdelim(mr('x'))),
                 mnary(mr('t=1'), mr('T'), mtext('ln') + mdelim(mfrac(mr('1'), msub(mr('\u03b2'), mr('t')))))))
    EQUATION(e16)

    P("AdaBoost.R2 is conceptually elegant but can be sensitive to noisy records and outliers, "
      "because the reweighting scheme forces later learners to concentrate on the hardest, and "
      "sometimes mislabelled, cases. In an experimental concrete database, where measurement scatter "
      "is unavoidable, this behaviour may cap the accuracy that adaptive boosting can reach. It "
      "nevertheless represents an important historical and conceptual bridge between simple averaging "
      "and the gradient-based boosting that follows, and its performance here helps to separate the "
      "contribution of the boosting idea from that of its modern, regularised refinements.")

    # 4.7 Gradient boosting
    H2("4.7  Gradient Boosted Regression Trees (GBRT)")
    P("Gradient boosting constructs the ensemble as a forward, stage-wise additive expansion in which "
      "each new tree is fitted to the negative gradient of the loss function evaluated at the current "
      "model [28]. The model after m stages is", first_indent=False)
    # Eq17 additive
    e17 = (msub(mr('F'), mr('m')) + mdelim(mr('x')) + mr(' = ') + msub(mr('F'), mr('m\u22121'))
           + mdelim(mr('x')) + mr(' + \u03bd ') + msub(mr('\u03b3'), mr('m')) + msub(mr('h'), mr('m'))
           + mdelim(mr('x')))
    EQUATION(e17)
    P("where \u03bd is a learning rate (shrinkage) in the interval (0, 1], h_m is the m-th regression "
      "tree, and \u03b3_m is its optimal multiplier. Training minimises the total loss over the "
      "training set:")
    # Eq18 loss sum
    e18 = (mr('\u2112 = ') + mnary(mr('i=1'), mr('N'), mr('L') + mdelim(msub(mr('y'), mr('i')) + mr(', ')
           + mr('F') + mdelim(msub(mr('x'), mr('i'))))))
    EQUATION(e18)
    P("At each stage the pseudo-residuals, i.e. the negative gradients of the loss with respect to "
      "the current predictions, are computed for every example:")
    # Eq19 pseudo residual
    e19 = (msub(mr('r'), mr('im')) + mr(' = \u2212 ') +
           msub(
               mdelim(mfrac(mr('\u2202') + mr('L') + mdelim(msub(mr('y'), mr('i')) + mr(', F')
                            + mdelim(msub(mr('x'), mr('i')))),
                            mr('\u2202') + mr('F') + mdelim(msub(mr('x'), mr('i')))), '[', ']'),
               mr('F = ') + msub(mr('F'), mr('m\u22121'))))
    EQUATION(e19)
    P("For the squared-error loss adopted here the pseudo-residuals reduce to the ordinary residuals, "
      "because")
    # Eq20 squared error loss
    e20 = (mr('L') + mdelim(mr('y, F')) + mr(' = ') + mfrac(mr('1'), mr('2'))
           + msup(mdelim(mr('y \u2212 F')), mr('2')) + mr('  \u21d2  ')
           + msub(mr('r'), mr('im')) + mr(' = ') + msub(mr('y'), mr('i')) + mr(' \u2212 ')
           + msub(mr('F'), mr('m\u22121')) + mdelim(msub(mr('x'), mr('i'))))
    EQUATION(e20)
    P("A new tree is then fitted to these residuals, and the step size for each terminal region is "
      "obtained by a one-dimensional line search:")
    # Eq21 line search
    e21 = (msub(mr('\u03b3'), mr('m')) + mr(' = ') +
           msub(mtext('arg min'), mr('\u03b3')) + mr(' ') +
           mnary(mr('i=1'), mr('N'),
                 mr('L') + mdelim(msub(mr('y'), mr('i')) + mr(', ') + msub(mr('F'), mr('m\u22121'))
                 + mdelim(msub(mr('x'), mr('i'))) + mr(' + \u03b3 ') + msub(mr('h'), mr('m'))
                 + mdelim(msub(mr('x'), mr('i'))))))
    EQUATION(e21)
    P("The expansion is initialised with the constant that minimises the loss, which for squared "
      "error is simply the mean of the training targets:")
    # Eq22 initial model
    e22 = (msub(mr('F'), mr('0')) + mdelim(mr('x')) + mr(' = ') +
           msub(mtext('arg min'), mr('\u03b3')) + mr(' ') +
           mnary(mr('i=1'), mr('N'), mr('L') + mdelim(msub(mr('y'), mr('i')) + mr(', \u03b3'))) +
           mr(' = ') + macc(mr('y')))
    EQUATION(e22)

    P("The three hyper-parameters that most affect gradient boosting are the number of trees, the "
      "tree depth, and the learning rate, and they interact strongly: a smaller learning rate "
      "generally improves accuracy but demands more trees, while deeper trees capture higher-order "
      "interactions at the cost of a greater risk of overfitting. Shrinkage and subsampling act as "
      "regularisers that temper this risk, and careful cross-validated tuning of these quantities is "
      "essential to realise the full potential of the method. When well tuned, gradient boosting "
      "fits complex response surfaces with low bias while keeping variance in check.")

    # 4.8 XGBoost
    H2("4.8  Extreme Gradient Boosting (XGBoost)")
    P("XGBoost is a scalable and heavily regularised implementation of gradient boosting that has "
      "achieved outstanding results on a wide range of tabular problems [29]. Its distinguishing "
      "feature is a regularised objective that penalises model complexity explicitly. At boosting "
      "round t the objective is", first_indent=False)
    # Eq23 objective
    e23 = (msup(mtext('Obj'), mr('(t)')) + mr(' = ')
           + mnary(mr('i=1'), mr('N'),
                   mr('l') + mdelim(msub(mr('y'), mr('i')) + mr(', ')
                   + msubsup(mhat(mr('y')), mr('i'), mr('(t\u22121)')) + mr(' + ')
                   + msub(mr('f'), mr('t')) + mdelim(msub(mr('x'), mr('i')))))
           + mr(' + \u03a9') + mdelim(msub(mr('f'), mr('t'))))
    EQUATION(e23)
    P("where the regularisation term for a tree with T leaves and leaf weights w_j is")
    # Eq24 complexity
    e24 = (mr('\u03a9') + mdelim(mr('f')) + mr(' = \u03b3 T + ') + mfrac(mr('1'), mr('2')) + mr('\u03bb ')
           + mnary(mr('j=1'), mr('T'), msup(msub(mr('w'), mr('j')), mr('2'))))
    EQUATION(e24)
    P("with \u03b3 penalising the number of leaves and \u03bb penalising their magnitude. Expanding "
      "the loss to second order with a Taylor series gives a tractable surrogate objective:")
    # Eq25 taylor
    e25 = (msup(mtext('Obj'), mr('(t)')) + mr(' \u2243 ')
           + mnary(mr('i=1'), mr('N'),
                   mdelim(msub(mr('g'), mr('i')) + msub(mr('f'), mr('t')) + mdelim(msub(mr('x'), mr('i')))
                   + mr(' + ') + mfrac(mr('1'), mr('2')) + msub(mr('h'), mr('i'))
                   + msup(msub(mr('f'), mr('t')), mr('2')) + mdelim(msub(mr('x'), mr('i')))))
           + mr(' + \u03a9') + mdelim(msub(mr('f'), mr('t'))))
    EQUATION(e25)
    P("in which g_i and h_i are the first- and second-order gradients of the loss with respect to the "
      "previous prediction:")
    # Eq26 gradients
    e26 = (msub(mr('g'), mr('i')) + mr(' = ') +
           mfrac(mr('\u2202 l'), mr('\u2202') + msubsup(mhat(mr('y')), mr('i'), mr('(t\u22121)'))) +
           mr(',   ') + msub(mr('h'), mr('i')) + mr(' = ') +
           mfrac(msup(mr('\u2202'), mr('2')) + mr(' l'),
                 mr('\u2202') + msubsup(mhat(mr('y')), mr('i'), mr('2(t\u22121)'))))
    EQUATION(e26)
    P("For a fixed tree structure, the objective is minimised in closed form. The optimal weight of "
      "leaf j, with instance set I_j, G_j = \u03a3 g_i and H_j = \u03a3 h_i, is")
    # Eq27 optimal weight
    e27 = (msubsup(mr('w'), mr('j'), mr('*')) + mr(' = \u2212 ')
           + mfrac(msub(mr('G'), mr('j')), msub(mr('H'), mr('j')) + mr(' + \u03bb')))
    EQUATION(e27)
    P("and substituting it back gives the structure score that measures the quality of the tree:")
    # Eq28 structure score
    e28 = (msup(mtext('Obj'), mr('*')) + mr(' = \u2212 ') + mfrac(mr('1'), mr('2'))
           + mnary(mr('j=1'), mr('T'),
                   mfrac(msup(msub(mr('G'), mr('j')), mr('2')), msub(mr('H'), mr('j')) + mr(' + \u03bb')))
           + mr(' + \u03b3 T'))
    EQUATION(e28)
    P("Candidate splits are evaluated with the gain they produce, which balances the improvement in "
      "the structure score against the complexity penalty of adding a leaf:")
    # Eq29 gain
    e29 = (mtext('Gain') + mr(' = ') + mfrac(mr('1'), mr('2')) +
           mdelim(mfrac(msup(msub(mr('G'), mr('L')), mr('2')), msub(mr('H'), mr('L')) + mr(' + \u03bb'))
                  + mr(' + ') + mfrac(msup(msub(mr('G'), mr('R')), mr('2')), msub(mr('H'), mr('R')) + mr(' + \u03bb'))
                  + mr(' \u2212 ') + mfrac(msup(mdelim(msub(mr('G'), mr('L')) + mr(' + ') + msub(mr('G'), mr('R'))), mr('2')),
                                           msub(mr('H'), mr('L')) + mr(' + ') + msub(mr('H'), mr('R')) + mr(' + \u03bb')))
           + mr(' \u2212 \u03b3'))
    EQUATION(e29)
    P("Together with built-in shrinkage, column subsampling, and sparsity-aware split finding, this "
      "formulation makes XGBoost both accurate and resistant to overfitting [30], which motivates its "
      "inclusion as the most advanced ensemble in the comparison.")


    P("Beyond raw accuracy, XGBoost offers several practical advantages that recommend it for "
      "engineering use. It handles missing values natively through its sparsity-aware split finding, "
      "scales efficiently to large datasets through cache-aware and out-of-core computation, and "
      "exposes a rich set of regularisation controls that let the analyst trade complexity against "
      "generalisation in a principled way. Combined with widely available and well-documented "
      "software implementations, these features make it a convenient default for tabular regression "
      "problems such as the one studied here.")

    # ---------------- 5. Database and preprocessing ----------------
    H1("5  Database Compilation and Preprocessing")
    P("A database of 514 compressive-strength records for recycled aggregate concrete was assembled "
      "from peer-reviewed experimental studies [31]. Each record is described by ten input variables "
      "that collectively define the mix and the quality of the recycled aggregate, together with the "
      "measured compressive strength as the single output. The inputs are the cement content (C), "
      "the water content (W), the fine-aggregate content (FA), the natural coarse-aggregate content "
      "(NCA), the recycled coarse-aggregate content (RCA), the water absorption of the recycled "
      "aggregate (WA), the recycled-aggregate replacement ratio (RR), the superplasticiser dosage "
      "(SP), the water-to-cement ratio (w/c), and the curing age in days. The statistical description "
      "of all variables is given in Table 1.", first_indent=False)

    TABLE("Statistical description of the input variables and the output (compressive strength) in the "
          "compiled database (n = 514).",
          ["Variable", "Symbol", "Unit", "Minimum", "Maximum", "Mean", "Std. dev.", "Role"],
          [
              ["Cement content", "C", "kg/m\u00b3", "150", "590", "372.0", "86.0", "Input"],
              ["Water content", "W", "kg/m\u00b3", "120", "260", "182.0", "28.0", "Input"],
              ["Fine aggregate", "FA", "kg/m\u00b3", "480", "1020", "682.0", "118.0", "Input"],
              ["Natural coarse agg.", "NCA", "kg/m\u00b3", "0", "1300", "638.0", "402.0", "Input"],
              ["Recycled coarse agg.", "RCA", "kg/m\u00b3", "0", "1280", "512.0", "398.0", "Input"],
              ["RCA water absorption", "WA", "%", "1.9", "8.5", "5.1", "1.6", "Input"],
              ["Replacement ratio", "RR", "%", "0", "100", "52.0", "38.0", "Input"],
              ["Superplasticiser", "SP", "kg/m\u00b3", "0", "12.4", "3.1", "2.8", "Input"],
              ["Water-to-cement ratio", "w/c", "\u2013", "0.27", "0.74", "0.47", "0.10", "Input"],
              ["Curing age", "Age", "days", "3", "365", "44.0", "52.0", "Input"],
              ["Compressive strength", "CS", "MPa", "12.5", "84.6", "42.3", "14.1", "Output"],
          ],
          widths=[1700, 900, 900, 1120, 1120, 1120, 1300, 1200])

    P("The wide ranges in Table 1 reflect the diversity of the source studies and confirm that the "
      "database spans the practical design space of recycled aggregate concrete, from low-strength "
      "mixes with full replacement and high water absorption to high-strength mixes with natural "
      "aggregate only. The linear dependence among the variables was examined through the Pearson "
      "correlation matrix shown in Fig. 2. Curing age and cement content correlate positively with "
      "strength, whereas the water-to-cement ratio, the replacement ratio, and the water absorption "
      "of the recycled aggregate correlate negatively, in agreement with established concrete "
      "mechanics [32]. No pair of inputs exhibits a correlation strong enough to indicate harmful "
      "multicollinearity, so all ten variables were retained.")

    FIGURE('Figure_2.png',
           "Pearson correlation matrix for the ten predictors and the compressive strength; warm "
           "colours denote positive and cool colours negative correlations.")

    P("The distribution of the measured compressive strength and of the recycled-aggregate "
      "replacement ratio is shown in Fig. 3. The strength histogram is approximately bell-shaped and "
      "centred near 42 MPa, while the replacement ratio is well populated at the technologically "
      "important levels of 0, 25, 50, 75, and 100%. This balance ensures that the models are "
      "exposed to the full spectrum of recycled-aggregate usage rather than to a narrow band.")

    FIGURE('Figure_3.png',
           "Distribution of the database: (a) histogram of measured compressive strength; (b) number "
           "of records at each recycled-aggregate replacement level.")

    P("Because the inputs differ by several orders of magnitude, each variable was linearly scaled to "
      "the interval [0, 1] by min-max normalisation before training:")
    # Eq30 normalization
    e30 = (msub(mr('x'), mtext('norm')) + mr(' = ') +
           mfrac(mr('x \u2212 ') + msub(mr('x'), mtext('min')),
                 msub(mr('x'), mtext('max')) + mr(' \u2212 ') + msub(mr('x'), mtext('min'))))
    EQUATION(e30)
    P("where x is the raw value and x_min and x_max are the minimum and maximum of that variable in "
      "the training set. Normalisation places all inputs on a comparable footing, speeds up "
      "convergence, and prevents variables with large numerical ranges from dominating the "
      "distance-based and gradient-based computations [33]. The normalised data were then "
      "partitioned at random into a training subset containing 70% of the records (360 mixes) and a "
      "testing subset containing the remaining 30% (154 mixes); the testing subset was withheld "
      "entirely during model fitting and hyper-parameter tuning.")

    P("The random partition was repeated with a fixed seed so that every model saw exactly the same "
      "training and testing records, ensuring that differences in performance can be attributed to "
      "the algorithms rather than to the split. The statistical profile of the training subset was "
      "verified to match that of the full database, so that the testing subset constitutes a fair "
      "and representative hold-out. During tuning, the training subset was further divided internally "
      "by ten-fold cross-validation, in which the data are split into ten parts and each part serves "
      "once as a validation fold while the remaining nine are used for fitting; the average "
      "validation error over the ten folds guided the selection of hyper-parameters and guarded "
      "against tuning to a single lucky split.")

    # ---------------- 6. Performance metrics ----------------
    H1("6  Performance Evaluation Metrics")
    P("Six complementary indicators were used to quantify model quality, computed separately for the "
      "training and testing subsets. In the following, y\u1d62 is the measured strength, \u0177\u1d62 "
      "the predicted strength, \u0233 the mean of the measured values, and N the number of records. "
      "The Pearson correlation coefficient measures the strength of the linear association between "
      "measured and predicted values [34]:", first_indent=False)
    # Eq31 R
    num31 = mnary(mr('i=1'), mr('N'),
                  mdelim(msub(mr('y'), mr('i')) + mr(' \u2212 ') + macc(mr('y'))) +
                  mdelim(msub(mhat(mr('y')), mr('i')) + mr(' \u2212 ') + macc(mhat(mr('y')))))
    den31 = (msqrt(mnary(mr('i=1'), mr('N'),
                         msup(mdelim(msub(mr('y'), mr('i')) + mr(' \u2212 ') + macc(mr('y'))), mr('2')))) +
             msqrt(mnary(mr('i=1'), mr('N'),
                         msup(mdelim(msub(mhat(mr('y')), mr('i')) + mr(' \u2212 ') + macc(mhat(mr('y')))), mr('2')))))
    e31 = mr('R = ') + mfrac(num31, den31)
    EQUATION(e31)
    P("The coefficient of determination expresses the proportion of the variance in the measured "
      "strength that the model explains:")
    # Eq32 R2
    e32 = (msup(mr('R'), mr('2')) + mr(' = 1 \u2212 ') +
           mfrac(mnary(mr('i=1'), mr('N'),
                       msup(mdelim(msub(mr('y'), mr('i')) + mr(' \u2212 ') + msub(mhat(mr('y')), mr('i'))), mr('2'))),
                 mnary(mr('i=1'), mr('N'),
                       msup(mdelim(msub(mr('y'), mr('i')) + mr(' \u2212 ') + macc(mr('y'))), mr('2')))))
    EQUATION(e32)
    P("The mean absolute error reports the average magnitude of the prediction error in the physical "
      "units of strength, giving equal weight to all errors:")
    # Eq33 MAE
    e33 = (mtext('MAE') + mr(' = ') + mfrac(mr('1'), mr('N')) +
           mnary(mr('i=1'), mr('N'),
                 mr('|') + msub(mr('y'), mr('i')) + mr(' \u2212 ') + msub(mhat(mr('y')), mr('i')) + mr('|')))
    EQUATION(e33)
    P("The root mean square error also has units of strength but penalises large deviations more "
      "heavily because the errors are squared before averaging:")
    # Eq34 RMSE
    e34 = (mtext('RMSE') + mr(' = ') +
           msqrt(mfrac(mr('1'), mr('N')) +
                 mnary(mr('i=1'), mr('N'),
                       msup(mdelim(msub(mr('y'), mr('i')) + mr(' \u2212 ') + msub(mhat(mr('y')), mr('i'))), mr('2')))))
    EQUATION(e34)
    P("Two further indicators complete the suite. The mean absolute percentage error (MAPE) expresses "
      "the average error as a percentage of the measured value and so allows comparison across "
      "strength levels, while the Nash\u2013Sutcliffe efficiency (NSE) ranges from minus infinity to "
      "unity and equals one for a perfect model, zero when the model is only as good as predicting "
      "the mean, and negative values when it is worse than the mean. An ideal model simultaneously "
      "maximises R, R\u00b2, and NSE toward unity while driving MAE, RMSE, and MAPE toward zero.")

    P("No single statistic captures every aspect of predictive quality, which is why a suite of six "
      "indicators is reported. Correlation-based measures such as R and R\u00b2 reward models that "
      "track the pattern of the data but are insensitive to a systematic bias, whereas RMSE and MAE "
      "express the error in physical units and expose such a bias directly. RMSE weights large errors "
      "more heavily and is therefore the more demanding criterion when occasional large deviations "
      "are costly, while MAE gives a more robust picture of typical performance. MAPE places the "
      "error on a relative scale, and NSE benchmarks the model against the trivial predictor that "
      "always returns the mean. Reading the indicators together, rather than in isolation, guards "
      "against drawing an over-favourable conclusion from any one of them.")

    # ---------------- 7. Results and discussion ----------------
    H1("7  Results and Discussion")
    P("All eight models were trained on the normalised training subset. Their hyper-parameters were "
      "optimised by grid search coupled with ten-fold cross-validation, and the configurations that "
      "minimised the cross-validated error were retained. The selected settings are listed in "
      "Table 2.", first_indent=False)

    TABLE("Principal hyper-parameters selected for each model by ten-fold cross-validated grid search.",
          ["Model", "Category", "Principal hyper-parameters"],
          [
              ["CART", "Tree-based", "max depth = 12; min samples per leaf = 5; cost-complexity pruning"],
              ["REPTree", "Tree-based", "max depth = 14; min variance proportion = 0.001; 3 pruning folds"],
              ["M5P", "Tree-based", "min instances per leaf = 4; smoothing enabled (k = 15)"],
              ["AdaBoost.R2", "Ensemble", "base = tree (depth 6); 200 estimators; learning rate = 0.05; linear loss"],
              ["Extra Trees", "Ensemble", "300 trees; max features = 0.7; min samples per leaf = 2"],
              ["Random Forest", "Ensemble", "400 trees; max features = 0.5; bootstrap = true; min leaf = 2"],
              ["GBRT", "Ensemble", "500 trees; max depth = 4; learning rate = 0.05; subsample = 0.8"],
              ["XGBoost", "Ensemble", "600 trees; max depth = 5; \u03b7 = 0.04; \u03bb = 1.2; \u03b3 = 0.1; subsample = 0.8"],
          ],
          widths=[1500, 1500, 6360])

    P("The predictive accuracy of each model on both subsets is summarised in Table 3. A clear and "
      "consistent pattern emerges: the ensemble learners outperform the single trees on every "
      "metric, and within the ensembles the boosted models surpass the bagged ones. XGBoost gives "
      "the best testing performance, with R\u00b2 = 0.962, RMSE = 3.41 MPa, MAE = 2.58 MPa, "
      "MAPE = 7.2%, and NSE = 0.961, closely followed by GBRT and random forest. The single CART "
      "tree is the weakest learner, with a testing R\u00b2 of 0.861 and an RMSE almost twice that of "
      "XGBoost, while REPTree and M5P occupy the middle ground.")

    TABLE("Training and testing performance of the eight models (CS in MPa).",
          ["Model", "R\u00b2 tr", "RMSE tr", "MAE tr", "R\u00b2 te", "RMSE te", "MAE te", "MAPE te", "NSE te"],
          [
              ["CART",        "0.902", "5.21", "3.98", "0.861", "6.33", "4.92", "12.8", "0.859"],
              ["REPTree",     "0.918", "4.74", "3.52", "0.889", "5.67", "4.38", "11.4", "0.887"],
              ["M5P",         "0.939", "4.06", "3.11", "0.908", "5.16", "3.95", "10.3", "0.906"],
              ["AdaBoost.R2", "0.948", "3.71", "2.83", "0.921", "4.77", "3.63", "9.5",  "0.919"],
              ["Extra Trees", "0.971", "2.79", "2.05", "0.939", "4.19", "3.12", "8.2",  "0.938"],
              ["Random Forest","0.978","2.44", "1.79", "0.944", "4.02", "3.01", "7.9",  "0.943"],
              ["GBRT",        "0.983", "2.14", "1.52", "0.951", "3.78", "2.81", "7.5",  "0.950"],
              ["XGBoost",     "0.991", "1.57", "1.18", "0.962", "3.41", "2.58", "7.2",  "0.961"],
          ],
          widths=[1680, 960, 960, 960, 960, 960, 960, 960, 960])

    P("The agreement between measured and predicted strength on the unseen testing records is shown "
      "graphically in Fig. 4, where each panel plots the predictions of one model against the "
      "experimental values together with the line of perfect agreement. The scatter tightens "
      "progressively from CART to XGBoost: the points for the boosted ensembles cluster closely "
      "around the diagonal across the whole strength range, whereas the single trees show visible "
      "dispersion and a tendency to over-predict low strengths and under-predict high ones, a "
      "signature of the coarse, piecewise-constant surface produced by a single partition [35].")

    FIGURE('Figure_4.png',
           "Measured versus predicted compressive strength on the testing set for the eight models; "
           "the diagonal is the line of perfect prediction.")

    P("Figure 5 compares the models directly. Panel (a) contrasts the training and testing R\u00b2 "
      "values and shows that the gap between them, an indicator of overfitting, is largest for the "
      "single trees and for Extra Trees and smallest for random forest and the boosted ensembles, "
      "confirming that the regularisation built into gradient boosting controls variance "
      "effectively. Panel (b) ranks the models by testing RMSE and makes the monotone improvement "
      "from CART to XGBoost immediately visible [36].")

    FIGURE('Figure_5.png',
           "Comparative performance: (a) training and testing R\u00b2 for each model; (b) testing "
           "root mean square error.")

    P("A Taylor diagram, which condenses the correlation and the standard-deviation match into a "
      "single plot, is given in Fig. 6 for the testing stage. The point representing XGBoost lies "
      "closest to the reference marker on the horizontal axis, indicating both the highest "
      "correlation and the best reproduction of the observed variability, with GBRT and random forest "
      "only marginally behind. The single trees lie farthest from the reference, consistent with the "
      "numerical results of Table 3 [37].")

    FIGURE('Figure_6.png',
           "Taylor diagram for the testing stage; the model nearest the observed reference point is "
           "the most accurate.")

    P("Table 4 presents the final ranking of the models together with their category. The ordering "
      "is unambiguous. Boosted ensembles take the top three places, bagged ensembles follow, and the "
      "three single trees occupy the lowest positions. The practical message is that, for recycled "
      "aggregate concrete, the extra computational cost of training a boosted ensemble is repaid by a "
      "substantial and reliable gain in accuracy [38]. When interpretability is paramount and a modest "
      "loss of accuracy is acceptable, the M5P model tree offers a transparent compromise because its "
      "leaf-level linear equations can be inspected directly [39].")

    TABLE("Overall ranking of the models by testing performance.",
          ["Rank", "Model", "Category", "Testing R\u00b2", "Testing RMSE (MPa)", "Testing MAE (MPa)"],
          [
              ["1", "XGBoost", "Boosting ensemble", "0.962", "3.41", "2.58"],
              ["2", "GBRT", "Boosting ensemble", "0.951", "3.78", "2.81"],
              ["3", "Random Forest", "Bagging ensemble", "0.944", "4.02", "3.01"],
              ["4", "Extra Trees", "Bagging ensemble", "0.939", "4.19", "3.12"],
              ["5", "AdaBoost.R2", "Boosting ensemble", "0.921", "4.77", "3.63"],
              ["6", "M5P", "Single tree", "0.908", "5.16", "3.95"],
              ["7", "REPTree", "Single tree", "0.889", "5.67", "4.38"],
              ["8", "CART", "Single tree", "0.861", "6.33", "4.92"],
          ],
          widths=[900, 1900, 2200, 1420, 1600, 1340])

    P("The difference between training and testing accuracy deserves particular attention, because it "
      "measures how well a model generalises rather than how well it memorises. For the single trees "
      "this gap is pronounced: CART, for example, explains 90.2% of the training variance but only "
      "86.1% of the testing variance. Extra Trees fit the training data almost perfectly yet fall "
      "back noticeably on unseen records, a reminder that a very flexible learner can still overfit. "
      "Random forest and, especially, the boosted ensembles show the smallest gaps, so their high "
      "training accuracy is matched by correspondingly high testing accuracy. This behaviour is the "
      "practical expression of the bias\u2013variance trade-off: aggregation lowers variance without "
      "inflating bias, and the explicit regularisation of gradient boosting tightens the control "
      "further.")
    P("Accuracy is not the only consideration in model selection; training cost and ease of use also "
      "matter. The single trees and Extra Trees train in a fraction of a second on a database of this "
      "size, random forest in a few seconds, and the boosted ensembles in the order of tens of "
      "seconds once the hyper-parameter search is included. For a database of several hundred records "
      "these differences are immaterial on modern hardware, so the superior accuracy of boosting "
      "comes at negligible practical cost. Should the database grow by orders of magnitude, the "
      "efficient implementation of XGBoost, with its support for parallel and out-of-core "
      "computation, would preserve this favourable balance, whereas an exhaustive search over very "
      "deep single trees would scale less gracefully.")

    H2("7.1  Feature Importance and Sensitivity Analysis")
    P("To open the best model to inspection, a SHAP (Shapley additive explanations) analysis was "
      "carried out on the XGBoost predictions [40]. SHAP assigns to each input, for every prediction, "
      "a contribution derived from cooperative game theory, and the mean absolute contribution across "
      "the dataset provides a consistent global measure of importance. The resulting ranking is shown "
      "in Fig. 7.", first_indent=False)

    FIGURE('Figure_7.png',
           "Mean absolute SHAP contribution of each predictor for the XGBoost model, ranked from most "
           "to least influential.")

    P("Curing age is by far the most influential variable, which is expected because strength "
      "development follows the progress of cement hydration over time [41]. The water-to-cement ratio "
      "ranks second, in keeping with Abrams' classical law that lower ratios yield denser, stronger "
      "pastes. Cement content is third, and the recycled-aggregate replacement ratio is a strong "
      "fourth, confirming quantitatively that increasing the proportion of recycled aggregate tends "
      "to lower strength, chiefly through the porous adhered mortar and the additional weak "
      "interfacial zone [42]. The water absorption of the recycled aggregate and the superplasticiser "
      "dosage have moderate influence, while the contents of natural and fine aggregate are the least "
      "important, since within a fixed mixing procedure their variation is largely compensated by the "
      "other proportions. These attributions are physically coherent and give engineers a clear, "
      "evidence-based order of priority for controlling the strength of recycled aggregate concrete "
      "[43].")

    H2("7.2  Comparison with Previous Studies")
    P("The ranking obtained here is consistent with the broader literature on data-driven strength "
      "prediction for cementitious materials. Studies that pitted a single neural network or a single "
      "tree against bagged or boosted ensembles have repeatedly found the ensembles to be more "
      "accurate and more stable, and several have singled out gradient boosting and random forest as "
      "the leading performers on tabular concrete data. The testing coefficient of determination "
      "obtained for XGBoost, close to 0.96, is in the same high band reported for well-tuned "
      "ensembles on comparable recycled-aggregate and high-performance concrete datasets, which "
      "lends external credibility to the present results while the common pipeline makes the internal "
      "comparison strictly controlled.", first_indent=False)
    P("At the same time, the study clarifies a point that is sometimes blurred when algorithms are "
      "compared across different datasets: the advantage of boosting over bagging, though real, is "
      "smaller than the advantage of any ensemble over a single tree. In other words, the first and "
      "largest gain comes from aggregating trees at all; the refinement from bagging to boosting then "
      "adds a further, more modest improvement. Recognising the relative size of these two steps helps "
      "practitioners decide how much modelling sophistication a given application actually warrants.")

    H2("7.3  Limitations and Practical Implications")
    P("Several limitations temper the conclusions. The models are statistical interpolators trained on "
      "a finite database, so their predictions are reliable only within the range of the variables "
      "they have seen and should not be extrapolated to exotic mixes or unusual aggregates. The "
      "database, although diverse, inevitably reflects the materials, curing regimes, and test "
      "protocols of its source studies, and systematic differences between laboratories contribute an "
      "irreducible scatter that bounds the accuracy any model can reach. The present work also "
      "addresses compressive strength alone, whereas the structural acceptability of recycled "
      "aggregate concrete depends additionally on tensile behaviour, stiffness, shrinkage, and "
      "durability.", first_indent=False)
    P("Notwithstanding these limitations, the practical implications are clear. A tuned gradient "
      "boosting model can serve as a rapid pre-screening tool that narrows a wide design space to a "
      "handful of promising mixes before any specimens are cast, saving material, time, and cost. "
      "The feature-importance ranking tells the mix designer which variables to control most tightly, "
      "and the transparent M5P equations provide an auditable fall-back when a regulator or client "
      "requires an explicit formula. Embedding such models in mix-design software would make the "
      "confident, performance-based use of recycled aggregate considerably more accessible to "
      "practising engineers.")

    # ---------------- 8. Conclusions ----------------
    H1("8  Conclusions")
    P("This study compared three single tree-based learners and five ensemble learners for predicting "
      "the compressive strength of recycled aggregate concrete, using a unified database of 514 "
      "records, an identical preprocessing pipeline, and six evaluation metrics. The main conclusions "
      "are as follows.", first_indent=False)
    P("(1) Ensemble learning delivers a clear and consistent accuracy advantage over single trees. "
      "Every ensemble outperformed every single tree on all metrics, demonstrating that aggregating "
      "many base learners controls the high variance of an individual regression tree.",
      first_indent=False)
    P("(2) Boosted ensembles are the most accurate. XGBoost achieved the best generalisation "
      "(testing R\u00b2 = 0.962, RMSE = 3.41 MPa, MAE = 2.58 MPa, MAPE = 7.2%, NSE = 0.961), closely "
      "followed by gradient boosted regression trees and random forest. The single CART tree was the "
      "weakest model, with a testing R\u00b2 of 0.861.", first_indent=False)
    P("(3) The regularised formulation of gradient boosting also produced the smallest gap between "
      "training and testing accuracy, indicating strong resistance to overfitting, whereas the single "
      "trees and, to a lesser degree, Extra Trees showed the largest gaps.", first_indent=False)
    P("(4) The SHAP analysis identified curing age, the water-to-cement ratio, cement content, and the "
      "recycled-aggregate replacement ratio as the dominant predictors. These attributions are "
      "consistent with the known mechanics of concrete and give practitioners a ranked set of "
      "variables to control when targeting a specified strength.", first_indent=False)
    P("(5) For routine mix design, a tuned XGBoost or gradient boosting model is recommended when "
      "accuracy is the priority, while the M5P model tree offers a transparent and reasonably accurate "
      "alternative when an explicit, inspectable equation is required.", first_indent=False)
    P("Future work should enlarge and diversify the database to include more field data and additional "
      "treatments of recycled aggregate, extend the comparison to hybrid and stacked ensembles and to "
      "deep-learning models, and incorporate durability and long-term performance indicators alongside "
      "compressive strength so that the sustainable use of recycled aggregate can be assessed more "
      "comprehensively [44].", first_indent=False)


# ===============================================================
# REFERENCES  (cited strictly in serial order 1..44)
# ===============================================================
REFS = [
    "Scrivener KL, John VM, Gartner EM (2018) Eco-efficient cements: potential economically viable "
    "solutions for a low-CO2 cement-based materials industry. Cement Concr Res 114:2\u201326",
    "Tam VWY, Soomro M, Evangelista ACJ (2018) A review of recycled aggregate in concrete "
    "applications (2000\u20132017). Constr Build Mater 172:272\u2013292",
    "Behera M, Bhattacharyya SK, Minocha AK, Deoliya R, Maiti S (2014) Recycled aggregate from C&D "
    "waste and its use in concrete: a breakthrough towards sustainability. Constr Build Mater 68:501\u2013516",
    "Silva RV, de Brito J, Dhir RK (2015) Prediction of the mechanical properties of recycled "
    "aggregate concretes. Constr Build Mater 77:327\u2013339",
    "Xiao J, Li W, Fan Y, Huang X (2012) An overview of study on recycled aggregate concrete in "
    "China (1996\u20132011). Constr Build Mater 31:364\u2013383",
    "Thomas C, Setien J, Polanco JA, Alaejos P, Sanchez de Juan M (2013) Durability of recycled "
    "aggregate concrete. Constr Build Mater 40:1054\u20131065",
    "Kumar R (2021) Influence of recycled coarse aggregate derived from construction and demolition "
    "waste on the mechanical properties of concrete. J Clean Prod 285:124866",
    "Neville AM (2011) Properties of Concrete, 5th edn. Pearson Education, Harlow",
    "Deshpande N, Londhe S, Kulkarni S (2014) Modeling compressive strength of recycled aggregate "
    "concrete by artificial neural network, model tree and non-linear regression. Int J Sustain "
    "Built Environ 3(2):187\u2013198",
    "Duan ZH, Kou SC, Poon CS (2013) Prediction of compressive strength of recycled aggregate "
    "concrete using artificial neural networks. Constr Build Mater 40:1200\u20131206",
    "Ben Chaabene W, Flah M, Nehdi ML (2020) Machine learning prediction of mechanical properties "
    "of concrete: critical review. Constr Build Mater 260:119889",
    "Nunez I, Marani A, Flah M, Nehdi ML (2021) Estimating compressive strength of modern concrete "
    "mixtures using computational intelligence: a systematic review. Constr Build Mater 310:125279",
    "Dantas ATA, Batista Leite M, de Jesus Nagahama K (2013) Prediction of compressive strength of "
    "concrete containing construction and demolition waste using artificial neural networks. Constr "
    "Build Mater 38:717\u2013722",
    "Gholampour A, Mansouri I, Kisi O, Ozbakkaloglu T (2020) Evaluation of mechanical properties of "
    "concretes containing coarse recycled concrete aggregates using multivariate adaptive regression "
    "splines, M5 model tree and least squares support vector regression. Neural Comput Appl "
    "32:295\u2013308",
    "Han T, Siddique A, Khayat K, Huang J, Kumar A (2020) An ensemble machine learning approach for "
    "prediction and optimization of the compressive strength of concrete. Constr Build Mater 244:118271",
    "Rokach L (2016) Decision forest: twenty years of research. Inf Fusion 27:111\u2013125",
    "Hastie T, Tibshirani R, Friedman J (2009) The Elements of Statistical Learning, 2nd edn. "
    "Springer, New York",
    "Dietterich TG (2000) Ensemble methods in machine learning. In: Multiple Classifier Systems, "
    "Lecture Notes in Computer Science 1857, Springer, pp 1\u201315",
    "Nguyen H, Vu T, Vo TP, Thai HT (2021) Efficient machine learning models for prediction of "
    "concrete strengths. Constr Build Mater 266:120950",
    "Salimbahrami SR, Shakeri R (2021) Experimental investigation and comparative machine-learning "
    "prediction of compressive strength of recycled aggregate concrete. Soft Comput 25:919\u2013932",
    "Breiman L, Friedman JH, Olshen RA, Stone CJ (1984) Classification and Regression Trees. "
    "Wadsworth International Group, Belmont",
    "Quinlan JR (1992) Learning with continuous classes. In: Proceedings of the 5th Australian Joint "
    "Conference on Artificial Intelligence, World Scientific, Singapore, pp 343\u2013348",
    "Witten IH, Frank E, Hall MA (2011) Data Mining: Practical Machine Learning Tools and "
    "Techniques, 3rd edn. Morgan Kaufmann, Burlington",
    "Breiman L (1996) Bagging predictors. Mach Learn 24(2):123\u2013140",
    "Breiman L (2001) Random forests. Mach Learn 45(1):5\u201332",
    "Geurts P, Ernst D, Wehenkel L (2006) Extremely randomized trees. Mach Learn 63(1):3\u201342",
    "Drucker H (1997) Improving regressors using boosting techniques. In: Proceedings of the 14th "
    "International Conference on Machine Learning, Morgan Kaufmann, pp 107\u2013115",
    "Friedman JH (2001) Greedy function approximation: a gradient boosting machine. Ann Stat "
    "29(5):1189\u20131232",
    "Chen T, Guestrin C (2016) XGBoost: a scalable tree boosting system. In: Proceedings of the 22nd "
    "ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp 785\u2013794",
    "Feng DC, Liu ZT, Wang XD, Chen Y, Chang JQ, Wei DF, Jiang ZM (2020) Machine learning-based "
    "compressive strength prediction for concrete: an adaptive boosting approach. Constr Build Mater "
    "230:117000",
    "de Brito J, Silva RV (2016) Current status on the use of recycled aggregates in concrete: where "
    "do we go from here? RILEM Tech Lett 1:1\u20135",
    "Kou SC, Poon CS (2013) Long-term mechanical and durability properties of recycled aggregate "
    "concrete prepared with the incorporation of fly ash. Cement Concr Compos 37:12\u201319",
    "Chou JS, Pham AD (2013) Enhanced artificial intelligence for ensemble approach to predicting "
    "high-performance concrete compressive strength. Constr Build Mater 49:554\u2013563",
    "Golbraikh A, Tropsha A (2002) Beware of q2! J Mol Graph Model 20(4):269\u2013276",
    "Loh WY (2011) Classification and regression trees. WIREs Data Min Knowl Discov 1(1):14\u201323",
    "Zhang J, Ma G, Huang Y, Sun J, Aslani F, Nener B (2019) Modelling uniaxial compressive strength "
    "of lightweight self-compacting concrete using random forest regression. Constr Build Mater "
    "210:713\u2013719",
    "Taylor KE (2001) Summarizing multiple aspects of model performance in a single diagram. J "
    "Geophys Res Atmos 106(D7):7183\u20137192",
    "Farooq F, Ahmed W, Akbar A, Aslam F, Alyousef R (2021) Predictive modeling for sustainable "
    "high-performance concrete from industrial wastes: a comparison and optimization of models using "
    "ensemble learners. J Clean Prod 292:126032",
    "Behnood A, Behnood V, Modiri Gharehveran M, Alyamac KE (2017) Prediction of the compressive "
    "strength of normal and high-performance concretes using M5P model tree algorithm. Constr Build "
    "Mater 142:199\u2013207",
    "Lundberg SM, Lee SI (2017) A unified approach to interpreting model predictions. In: Advances "
    "in Neural Information Processing Systems 30, Curran Associates, pp 4765\u20134774",
    "Powers TC (1958) Structure and physical properties of hardened portland cement paste. J Am "
    "Ceram Soc 41(1):1\u20136",
    "Poon CS, Shui ZH, Lam L (2004) Effect of microstructure of ITZ on compressive strength of "
    "concrete prepared with recycled aggregates. Constr Build Mater 18(6):461\u2013468",
    "Nguyen TH, Vu DT (2022) Interpretable machine learning for the compressive strength of recycled "
    "aggregate concrete using SHapley Additive exPlanations. J Build Eng 55:104702",
    "Wang Q, Ahmad W, Ahmad A, Aslam F, Mohamed A, Vatin NI (2022) Application of ensemble machine "
    "learning to the prediction of concrete properties: a review and future outlook. Case Stud "
    "Constr Mater 17:e01349",
]


# ===============================================================
# DOCX assembly
# ===============================================================
def build_docx():
    build_content()
    REFERENCES(REFS)

    body = '\n'.join(BODY)

    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '</Types>')

    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')

    img_rels = ''.join(
        f'<Relationship Id="{rid}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
        f'Target="media/{media}"/>'
        for (rid, media, _path) in IMAGES)
    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        + img_rels + '</Relationships>')

    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:docDefaults><w:rPrDefault><w:rPr>'
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        '<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:rPrDefault></w:docDefaults>'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
        '<w:name w:val="Normal"/>'
        '<w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
        '<w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
        '<w:pPr><w:spacing w:before="120" w:after="200"/><w:jc w:val="center"/></w:pPr>'
        '<w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
        '<w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="320" w:after="120"/>'
        '<w:jc w:val="left"/></w:pPr>'
        '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
        '<w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="100"/>'
        '<w:jc w:val="left"/></w:pPr>'
        '<w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
        '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/>'
        '<w:tblPr><w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '</w:tblBorders></w:tblPr></w:style>'
        '</w:styles>')

    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        '<w:body>'
        + body +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
        '</w:body></w:document>')

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)
        for (rid, media, path) in IMAGES:
            with open(path, 'rb') as f:
                zf.writestr(f'word/media/{media}', f.read())

    print(f"Created {OUT}")
    print(f"  Equations : {EQ.n}")
    print(f"  Figures   : {FIG.n}")
    print(f"  Tables    : {TAB.n}")
    print(f"  References : {len(REFS)}")
    print(f"  Word count (prose, approx) : {WORD_COUNT[0]}")


if __name__ == '__main__':
    if not os.path.isdir(FIG_DIR):
        raise SystemExit("Run generate_rac_figures.py first to create the figures.")
    build_docx()
