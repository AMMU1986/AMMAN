# PM-EDM reanalysis code

Code for the manuscript *Cross-validated machine learning with uncertainty quantification for
multi-response prediction and optimization of powder-mixed EDM of WC-Co: a reanalysis of published
experimental data* (`../Manuscript_PMEDM_ML_Reanalysis.md` and `.docx`).

Everything uses the Python standard library (Python 3.9 or later). No NumPy or scikit-learn is needed.

## Run order

From the repository root:

```bash
python3 pmedm_ml_code/analysis.py         # audit, CV of 12 models, UQ, SHAP, PDP, NSGA-II, TOPSIS, BO  (~6 min, 8 cores)
python3 pmedm_ml_code/extra_analysis.py   # decision-weight sensitivity and learning curves            (~1 min)
python3 pmedm_ml_code/figures.py          # Figures 1-9 (needs a Chromium/Chrome headless binary to rasterise SVG)
python3 pmedm_ml_code/check_manuscript.py # word counts, 45 equations, 43 references in serial order
python3 create_pmedm_ml_docx.py           # Word file with native equations, tables and figures
```

## Files

| File | Purpose |
|---|---|
| `core.py` | Dense linear algebra, BFGS, t/F/beta distributions, rank statistics |
| `data.py` | Loads `../pmedm_ml_data/*.csv` |
| `models.py` | Mean, Taguchi main effects, physics-guided power law, RSM, GPR (Matérn-5/2 × powder kernel, optional replicate-error noise), random forest, XGBoost-type boosting, ANFIS (2 and 3 MF), MC-dropout MLP, deep ensemble |
| `decision.py` | NSGA-II, 2-D hypervolume, GRA, TOPSIS, entropy and CRITIC weights |
| `analysis.py` | Main pipeline; writes `../pmedm_ml_results/results.json` |
| `extra_analysis.py` | Writes `../pmedm_ml_results/results_extra.json` |
| `svgplot.py`, `figures.py` | SVG plotting and PNG export of the figures |
| `latex2omml.py` | LaTeX-subset to Office Math (OMML) converter used by `../create_pmedm_ml_docx.py` |
| `preview_equations.py` | Optional visual check of the equation parser (renders MathML in headless Chromium) |
| `check_manuscript.py` | Checks the manuscript against the brief |

All random seeds are fixed, so reruns reproduce the numbers in the manuscript.
