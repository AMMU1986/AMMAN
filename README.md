# AMMAN

## Carreau EMHD squeezing-flow manuscript (corrected)

Corrected formulation of the paper *"Entropy Generation and Irreversibility Analysis of
Unsteady EMHD Squeezing Flow of a Carreau Hybrid Nanofluid (AA7072–AA7075/Methanol)
Between Parallel Porous Plates"*, addressing the reviewer's notes.

### What was corrected
- **Momentum equation retained at fourth order** via pressure elimination, so the coupled
  system order (8) matches the eight physical boundary conditions (fixes the BC-count
  inconsistency). Corrected unsteady group `Sq(f' + (η/2) f'')`.
- **Energy equation** radiation grouping fixed: `[A4 + (4/3) Rd F³] θ''` — `A4` multiplies
  conduction only (Rd is defined with the base-fluid conductivity).
- **Entropy generation**: Joule term uses the time-dependent fields `B(t), E(t)`; consistent
  `κ_f`-based normalisation; thermal term no longer double-counts `A4` on radiation; the
  diffusive cross-gradient term is retained in `Ns` and `Be`.
- **Grid convergence**: observed order uses magnitudes of successive differences; recomputed
  `p_obs ≈ 4.00` from three mesh resolutions.
- **Appendix A** corrections (A1, A9 = `φ''=0`, A10 keeps the cross term, A13 with `A4=1`,
  A15 requires `S3=0`, Casson-vs-Carreau caveat).

Full working derivation: `DERIVATION_NOTES_Carreau_EMHD.md`.

### Files
| File | Purpose |
|------|---------|
| `Carreau_EMHD_Squeezing_Corrected.docx` | Corrected manuscript; all equations in native Word equation-editor (OMML) format, strict serial order (1)–(61), (A1)–(A15); regenerated figures and tables inserted. |
| `DERIVATION_NOTES_Carreau_EMHD.md` | Locked derivations for every correction. |
| `carreau_emhd_solver.py` | Pure-stdlib RK4 + Newton-shooting BVP solver (8-variable system) with property ratios, entropy and engineering quantities. |
| `pyplot_stdlib.py` | Pure-stdlib PNG line-plot renderer (5×7 bitmap font, axes, ticks, grid, legend). |
| `generate_carreau_emhd_figures.py` | Generates the seven figures from computed solutions. |
| `compute_tables.py` | Computes the corrected Table 3a/3b/4/5/6 values and grid convergence. |
| `docx_omml.py` | Pure-stdlib `.docx` writer with native OMML equation builders. |
| `build_carreau_emhd_docx.py` | Assembles the corrected manuscript `.docx`. |
| `carreau_emhd_figures/` | Generated PNG figures. |

### Reproduce
No third-party packages are required (Python standard library only).

```bash
pyenv global 3.11.15
python generate_carreau_emhd_figures.py     # writes carreau_emhd_figures/*.png
python compute_tables.py                     # prints corrected table values
python build_carreau_emhd_docx.py            # writes Carreau_EMHD_Squeezing_Corrected.docx
```

The equations in the `.docx` are editable Word equation objects (Office MathML), not images.
