# Revision notes: SS430 filler-wire weldability manuscript

These notes go with `Manuscript_SS430_Filler_Wire_Weldability.md` and `.docx`. Part A lists the changes made to the text. Part B lists problems that need the original data or an author decision. A reviewer is likely to raise each item in Part B.

## A. Corrections made

### Numerical and technical errors

1. **Table 1, SS430 Cr<sub>eq</sub>:** changed from 16.82 to **16.84** (16.3 + 0 + 1.5 × 0.36). All other Cr<sub>eq</sub>/Ni<sub>eq</sub> values, both heat inputs (1.120 and 0.972 kJ/mm), the 4.036 kJ/mm sum, the Faraday factor (1.17016 × 10<sup>4</sup>), and all four penetration rates were recalculated and are correct.
2. **Tensile cross-section:** changed from 78.571 mm² (π taken as 22/7) to **78.54 mm²** (π × 5²). The 0.04% difference has no effect on the stresses.
3. **Standards wording:** "in accordance with ASTM G5 and ASTM G59" was inaccurate. G5 uses 1 N H<sub>2</sub>SO<sub>4</sub> and a 0.6 V/h scan, and G59 is a ±30 mV polarization-resistance method. The text now says the procedure was *based on* these standards and that the electrolyte, scan range, and scan rate differed. ASTM G102 is now cited to explain why the Fe-based equivalent weight was used.
4. **Table 1 asterisk:** the asterisk on 10.06 had no footnote. A footnote now states that N was not analyzed, and that ER2594 is N-alloyed (0.20–0.30 wt% N in AWS A5.9; see the [Washington Alloy 2594 datasheet](https://www.washingtonalloy.com/wp-content/uploads/2020/12/e2594-16.pdf)). The "–" entry for Mo is also explained.
5. **Equations:** all four displayed equations are now numbered (Schaeffler Cr<sub>eq</sub>/Ni<sub>eq</sub> = Eqs. 1–2, heat input = Eq. 3, Faraday = Eq. 4). The text states that the Schaeffler 0.5Nb term was omitted. *I*<sub>corr</sub> (a current) was renamed *i*<sub>corr</sub>, because the quantity is a current density.
6. **ER2594 is described as super-duplex.** It is the AWS filler that matches 2507/S32750.
7. The **cumulative 4.036 kJ/mm** is now labeled as a reference value only, because the HAZ thermal cycle depends on the per-pass heat input.
8. **XRD:** mentions of "amorphous content" and "percentage of crystallinity" were removed. They do not apply to steel welds, and reviewers would query them.

### Presentation of uncertainty

9. **"±" values were removed from the abstract, results text, Table 3, and conclusions.** They were an assumed ±3% of each value, not measured scatter. In those places a "±" would be read as a measured SD. Fig. 8 still shows the assumed error bars, so its caption and one sentence in Section 4.4 still state what they are. **Recommendation:** re-plot Fig. 8 without error bars and delete those two sentences. I can generate the replacement figure from Table 3 if you want.

### Notes to self removed from the paper body

10. These sentences were removed or rewritten as plain statements: "should be reconciled with the original polarization-fitting outputs", "should not be recalculated from the resized image", "obtain the root face from the original fabrication drawing", "Values retain the source graph-series labels", and "after excluding the unlabeled impact bar". Where a fact was involved, it is now stated directly (e.g., "the root-face dimension was not recorded").

### Structure, consistency, and language

11. Section 2 is now split into 2.1 Materials and 2.2 Welding procedure. Two repeated sentences about Table 1 were merged. The out-of-place sentence about tensile extraction labels was moved to Section 3.3. Table 2 was rebuilt as a two-column table, with the arc efficiency added.
12. Filler labels are now consistent. The text had ER309L, F309, and FW 309L for the same filler; it now uses ER309L, ER410, and ER2594 throughout. The Fig. 6 and Fig. 10 captions explain the F309/F410/F2594 legend labels.
13. Spelling is American throughout ("centred" and "millimetres" were the exceptions). Units use slash notation (kJ/mm, A/cm², mm/y). Minus signs, en-dash ranges, and HV0.5 are used consistently.
14. **References:** diacritics in [13] (Şenol, Çam), en dashes in the page ranges of [12] and [14], issue number (3) for [22], consistent volume (issue) (year) format, and the "(no DOI assigned)" remarks removed.

### Additions (delete if you disagree)

15. **Section 4.4:** one sentence on notch sampling. In a single-V groove, a HAZ notch also samples FZ and BM along its front. This is offered as one possible reason why the HAZ energies are high even though the HAZ fractographs show cleavage features.
16. **Section 4.5:** one sentence noting that the *i*<sub>corr</sub> ranking follows the Cr content of the starting materials in Table 1.
17. **Abstract:** a one-sentence closing conclusion. It states that the filler ranking differs between the FZ and the HAZ, which the Table 3 data show.

## B. Issues that need your data or decision (not changed)

1. **Charpy energies of 428–584 J are the most serious problem.** These values are far above what full-size (10 × 10 mm) CVN specimens of ferritic or martensitic stainless weld zones normally absorb. They also exceed what common 300–450 J pendulums can validly measure. ASTM E23 treats energies above 80% of the machine capacity as outside the valid range ([Instron, ASTM E23](https://www.instron.com/en/testing-solutions/astm-standards/astm-e23-sub-size/)), and ISO 148-1 has a similar "exceeding machine capacity" clause. Under that rule, 584 J would need a pendulum of at least 730 J. A HAZ with cleavage facets and river patterns that also absorbs the highest energy is a further inconsistency. Please check:
   - the unit (J, J/cm², kJ/m², or kgf·m);
   - the machine capacity;
   - the specimen size;
   - whether the specimens broke completely.

   If the values are energy per unit area, convert them or label them correctly.
2. **The arc voltage is low for GMAW.** At 135–150 A, GMAW normally runs at about 18–24 V, whereas 12–14 V is typical of GTAW. DCEP polarity and η = 0.8 do point to GMAW. Please check whether the voltage was measured at the arc or at the power source, or whether the process was in fact GTAW. If it was GTAW, η = 0.6 (EN 1011-1) and all heat inputs would change.
3. **The ER2594 results look atypical.** Super-duplex deposits are normally stronger and harder than 309L deposits; for example, ER2594 is specified with a yield strength of at least 550 MPa ([ER2594 datasheet](https://www.weldingandwelder.com/wp-content/uploads/2024/06/TDS.ER2594.GTAW_rev2.pdf)). Here the ER2594 FZ has the lowest hardness (176.8 HV0.5) and the lowest tensile response. Since the filler-to-specimen mapping is already uncertain, check for swapped labels.
4. **Austenite reflections in the ER410 FZ** would be unusual for an almost Ni-free deposit. Please recheck the peak indexing.
5. **Base-metal Charpy result:** Section 3.2 says BM specimens were tested, but no BM energy is reported. Either report it or delete that sentence. If the excluded unassigned result is the BM, say so.
6. **No tensile values are reported.** The paper gives no yield strength, UTS, elongation, or fracture location. Reviewers will expect a table of these values.
7. **Missing experimental details:**
   - wire diameter and shielding gas;
   - root face and preheat;
   - OM, SEM, and potentiostat models;
   - Ag/AgCl filling solution and Tafel fitting range;
   - Charpy test temperature and number of specimens per condition.
8. **Figures:**
   - Remove the provisional "eutectic" and other phase labels from Figs. 4–5; the caveats in Sections 4.1–4.2 can then be shortened.
   - Add a scale bar to Fig. 2a.
   - Re-plot Fig. 8 without the assumed error bars.
9. **Citations checked only partly.** I confirmed that [14] used GTAW with ER309L versus autogenous welding and that the filler welds had higher mechanical properties, which matches the text. I confirmed the title and DOI of [22]. I could not reach the full texts behind the specific claims attributed to [15]–[17] and the tensile claim attributed to [22]. Please check them, including the "ER317M" designation in [16] (the AWS classifications are ER317 and ER317L).
10. **Optional reference:** Shanmugasundar et al., *Materials* 16 (2023) 1590 compared 310 and 410 fillers on TIG-welded 430 and found better mechanical properties with 410 ([MDPI](https://www.mdpi.com/1996-1944/16/4/1590)). It supports the comparison in Section 4.4.
