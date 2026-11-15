# PM-EDM reanalysis dataset

Source: Singh, J. (2022). Multi-objective optimization of powder-mixed EDM parameters using hybrid
Grey-ANFIS artificial intelligence technique. *International Journal on Interactive Design and
Manufacturing*, 16, 1533–1549. https://doi.org/10.1007/s12008-022-00866-5

| File | Content | Source in the paper |
|---|---|---|
| `singh2022_l27_pmedm_wc.csv` | 27 L27 runs: factor settings, measured MRR and TWR, and the reported normalised values, grey relational coefficients, GRG, G-ANFIS grade and ranks | Tables 2 and 3 |
| `singh2022_confirmation_runs.csv` | Three confirmation replicates at A2B3C1D3 | Table 12 |

Transcription notes

- Factor symbols follow the paper: A = pulse-off time (µs), B = pulse-on time (µs), C = abrasive, D = current (A).
- `powder = none` is the "Simple oil (−)" level.
- Run 26 TWR is printed as 1.1248 in Table 2. It is kept as printed; its reported normalised value (0.490) is consistent with 1.125.
- Workpiece: WC-based alloy (reported composition W 65.50, Ti 15.47, Co 10.07, Nb 4.69, Cu 3.66; units not stated in the source), copper tool, 15 g/l powder, 10 min per run.
