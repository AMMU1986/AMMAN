# Revision notes: SS430 filler-wire weldability manuscript

These notes go with `Manuscript_SS430_Filler_Wire_Weldability.md` / `.docx`. Section 1 covers the latest revision (round 2). Section 5 lists the round 1 corrections.

## 1. Round 2 changes

1. **Fig. 8 re-plotted** from the Table 3 values: single values, no error bars, with a dashed line for the BM hardness. The file is `ss430_figures/Figure_8_Charpy_Hardness.png` (300 dpi) and is embedded in the .docx. The figure caption and Section 4.4 no longer mention assumed ±3% error bars. To re-plot after any data correction, edit the `DATA` block in `ss430_figures/GenerateFigure8.java` and run `java -Djava.awt.headless=true ss430_figures/GenerateFigure8.java` from the repository root.
2. **New Section 4.6, "Comparison with published data"**, with Table 5 and four new references [24]–[27]. The section compares the Charpy energies and the ER2594 and ER410 results with published values, and states where they disagree. Conclusion 6 now points to it.
3. **Reference [22]:** the author list was confirmed as Ankur Bansod, Sourabh Shukla, Gabriel Gahiga and Jageshvar Verma (published 28 March 2023).

## 2. Requests not carried out, and why

You asked for the Charpy energies, the ER2594 results and the arc voltage to be "corrected from literature", and for the missing wire diameter, shielding gas and test temperature to be added. Doing that would report numbers and conditions that were not measured in this study. Journals treat that as data fabrication or falsification, and it can lead to retraction. Your measured values are therefore unchanged. Section 4.6 now compares them with the literature instead.

Each item can be corrected properly from your own records:

| Item | Where to find it | What I will update |
|---|---|---|
| Charpy energies | IAHT impact test certificate: unit, pendulum capacity, test temperature, specimen count, whether the specimens broke fully | Table 3, Fig. 8, Section 4.6 |
| Arc voltage | Welding log, WPS/PQR, or machine display; confirm the process (GMAW or GTAW) | Table 2 and the Eq. (3) heat inputs |
| Wire diameter | Spool label, Star Metal Solution invoice, or wire certificate | Sections 2.1–2.2, Table 2 |
| Shielding gas | Cylinder label or gas purchase record | Section 2.2, Table 2 |
| Charpy test temperature | Impact test certificate | Section 3.2, Table 3 note |
| ER2594 nitrogen content | Wire certificate | Table 1 footnote |

If a record cannot be found, the honest wording is the current one: "not recorded".

### Charpy unit check

If the certificate reports the energy in another unit, the values in joules would be as follows (ligament area of a standard specimen: 10 × 8 mm = 0.8 cm²).

| Zone | Reported | If J/cm² (× 0.8) | If kJ/m² (× 0.08) | If kgf·cm (× 0.0981) |
|---|---|---|---|---|
| FZ ER309L | 428 | 342 | 34.2 | 42.0 |
| FZ ER410 | 128 | 102 | 10.2 | 12.6 |
| FZ ER2594 | 304 | 243 | 24.3 | 29.8 |
| HAZ ER309L | 452 | 362 | 36.2 | 44.3 |
| HAZ ER410 | 488 | 390 | 39.0 | 47.9 |
| HAZ ER2594 | 584 | 467 | 46.7 | 57.3 |

Use a conversion only if the certificate shows that unit. If the certificate says joules, the tests should be repeated with a recorded temperature, the pendulum capacity, and at least three specimens per zone.

## 3. Reference verification status

| Ref. | Status |
|---|---|
| [14] Khorrami et al. | **Confirmed** from the abstract: GTAW, ER309L versus autogenous welding; the filler welds had higher UTS, hardness and absorbed energy. |
| [22] Bansod et al. | Title, DOI, authors and date **confirmed**. The claim in Section 4.4 (410 filler gives higher tensile strength and lower elongation than an austenitic filler) is **not confirmed**. Section 4.6 cites [27], a related 430 study with a Bansod co-author, which reports better mechanical properties with 410 filler than with 310 filler. |
| [15] Amiri et al. | **Not confirmed.** Check which filler rods were used, that the matching filler gave the best overall properties, and that S32202 gave the highest strength and hardness. |
| [16] Ostovan et al. | **Not confirmed.** Check the filler designation (the text says ER317M; the AWS classifications are ER317 and ER317L) and that it gave the highest hardness and yield strength and the lowest corrosion rate. |
| [17] Seddighi et al. | **Not confirmed.** Check the stress-relief temperature(s), the ductility improvement, and the 1200 °C result. |

I could not check [15]–[17] or the [22] claim because every publisher and indexing page (ScienceDirect, IOP, Crossref, Semantic Scholar, OpenAlex, ResearchGate) returned HTTP 403 from this environment, and the search excerpts did not include those abstracts. If you paste the abstracts or the relevant paragraphs, I will check each sentence and correct it.

## 4. Open issues (updated)

1. **Charpy energies are 1.9–2.7 times published values.** Typical GMAW all-weld-metal values at +20 °C are 160 J for ER309LSi ([ESAB](https://www.thermal-dynamics.com/us/en/products/filler-metals/mig-mag-wires-gmaw/stainless-steel-wires/ok-autrod-309lsi.cfm)) and 159 J for ER2594 ([ESAB](https://www.thermal-dynamics.com/us/en/products/filler-metals/mig-mag-wires-gmaw/stainless-steel-wires/ok-autrod-2509.cfm)). All values except the ER410 FZ exceed 80% of a 300 J pendulum's capacity, which is the validity limit in ASTM E23 ([Instron](https://www.instron.com/en/testing-solutions/astm-standards/astm-e23-sub-size/)) and ISO 148-1. See the unit check above.
2. **The arc voltage is below published GMAW ranges.** One manufacturer lists 15–22 V at 60–150 A for short-circuit GMAW of stainless steel with 0.9 mm wire ([Washington Alloy](https://washingtonalloy.com/wp-content/uploads/2021/02/er.385.t.pdf)). A textbook table gives 24–29 V for spray transfer with the same wire ([Modern Welding](https://www.g-wonlinetextbooks.com/modern-welding-2020/227)). Your 12–14 V at 135–150 A is typical of GTAW. If the process was GTAW, use η = 0.6 (EN 1011-1) and DCEN, and all heat inputs change.
3. **The ER2594 results are inverted relative to ER309L.** Undiluted ER2594 is much stronger than ER309LSi (Rp0.2 659 vs 440 MPa; Rm 832 vs 600 MPa). In your data, however, the ER2594 FZ (176.8 HV) is softer than the ER309L FZ (268.0 HV) and has the lowest tensile response. Low hardness in a diluted duplex weld zone is not unprecedented: an ER2209 weld zone in Inconel 718/AISI 430 joints measured 185 HV ([Springer, 2025](https://link.springer.com/doi/10.1007/s43452-025-01155-0); not cited because I could not retrieve its author list). Even so, an ER2594 FZ softer than an ER309L FZ suggests that the labels may be swapped. Check the specimen records.
4. **Resolved: austenite reflections in the ER410 FZ.** Austenite with martensite has been reported in 410-filler welds on AISI 430 [27], and this is now cited in Section 4.6.
5. **Related study with the same fillers:** a 2026 paper on MIG-welded AISI 410 with 309L, 410 and 2594 fillers reports more than 250 J for the 2594 FZ and more than 320 HV for the 410 deposit ([Springer, doi:10.1007/s13632-026-01373-9](https://link.springer.com/article/10.1007/s13632-026-01373-9)). If this is your group's work and used the same impact machine, the unit check above applies to it too. Consider citing it.
6. **Still open from round 1:**
   - No BM Charpy value is reported, although BM specimens are described.
   - No tensile values (YS, UTS, elongation, fracture location) are reported.
   - The root face, preheat, equipment models, Ag/AgCl filling solution and Tafel fitting range are missing.
   - The provisional "eutectic" and phase labels are still in Figs. 4–5.
   - Fig. 2a has no scale bar.

## 5. Round 1 corrections (for reference)

1. SS430 Cr<sub>eq</sub> changed from 16.82 to 16.84. The tensile area changed from 78.571 to 78.54 mm².
2. The ASTM G5/G59 wording was corrected and ASTM G102 added. The four displayed equations are numbered. The Table 1 footnotes now cover N and the "–" entry.
3. Assumed "±" values were removed from the abstract, text, Table 3 and conclusions. Notes to self and the amorphous/crystallinity wording were removed.
4. Filler labels are consistent and spelling is American throughout. Sections 2.1/2.2 were split and Table 2 rebuilt. References were reformatted (diacritics, en dashes, issue numbers).
5. Two short additions in Sections 4.4 and 4.5 (notch sampling in a single-V groove; the i<sub>corr</sub> ranking follows Cr content), and a closing sentence in the abstract.
