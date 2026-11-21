# Follow-on modelling articles to Eikenberry, Thalhauser & Kuang (2009)

These are three research articles that extend the tumour–immune melanoma model of Eikenberry S, Thalhauser C, Kuang Y, *PLoS Comput Biol* 5(4):e1000362 (2009). All results come from simulations run with the code in this folder.

| Article | Question | Files |
|---|---|---|
| 1 | Which satellites does surgery release, and when does immune stimulation prevent recurrence? | `Article_1_Surgery_Triggered_Recurrence.{md,docx}`, `article1_figures/` |
| 2 | How does immune-derived angiogenic factor set dormancy duration, and how does anti-VEGF scheduling interact with it? | `Article_2_Immune_Angiogenic_Switch.{md,docx}`, `article2_figures/` |
| 3 | How far does tumour-directed immunity reach, and what does that imply for stochastic seeding and excision margins? | `Article_3_Immune_Halo_Stochastic_Seeding.{md,docx}`, `article3_figures/` |

## Model

`melanoma_sim.js` implements a reduced, radially symmetric version of the original model. It tracks primary tumour cells, satellite cells, immune cells, vasculature, and quasi-steady IAF/TAF fields. The scheme is finite-volume with explicit Euler time stepping and tridiagonal solves for the quasi-steady fields. Parameters and simplifications are documented in Section 2 of Article 1. Several parameters were calibrated rather than measured, and masses are dimensionless.

## Reproducing

Requirements: Node.js 18 or later and Python 3.8 or later. Only standard libraries are used.

```
node run_experiments.js all   # about 13 min on 8 cores; writes results/*.json
python3 analyze.py            # prints every number quoted in the articles
python3 make_figures.py       # renders article*_figures/*.png
python3 build_docx.py         # builds the three .docx files
```

Run a single article's experiments with `node run_experiments.js a1|a2|a3`.

## Status

These are drafts. The author names and affiliations are placeholders, and the manuscripts have not been peer reviewed.
