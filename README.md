# AMMAN

Book chapters and manuscripts. Every document has a single Markdown source, figures generated from code, and a Word file built from the two.

## Documents

| Markdown source | Word output | Figure generator | Figure folder |
|---|---|---|---|
| `Chapter_Agentic_AI_Autonomous_Systems.md` | `Chapter_Agentic_AI_Autonomous_Systems.docx` | `generate_agentic_figures.py` | `agentic_figures/` |
| `Chapter_Design_Thinking_Business_Functions.md` | `Chapter_Design_Thinking_Business_Functions.docx` | `generate_design_thinking_figures.py` | `design_thinking_figures/` |
| `Chapter_Economic_Analysis_HRES.md` | `HRES_Economic_Analysis_Chapter.docx` | `generate_hres_figures.py` | `HRES_figures/` |
| `Chapter_Intersectionality_Climate_Resilience.md` | `Chapter_Intersectionality_Climate_Resilience.docx` | `generate_intersectionality_figures.py` | `intersectionality_figures/` |
| `Manuscript_Ionic_Liquids_MQL_Machining.md` | `Manuscript_Ionic_Liquids_MQL_Machining.docx` | `generate_il_figures.py` | `manuscript_figures/` |
| `Chapter_16_AI_Assisted_Design_of_Nanomaterials.md` | `Chapter_16_AI_Assisted_Design_of_Nanomaterials.docx` | `generate_ch16_figures.py` | `figures/` |
| `Chapter_4_Experimentation.md` | `Chapter_4_Experimentation.docx` | `generate_chapter4_figures.py` | `chapter4_figures/` |
| `manuscript_with_references.md` | `AI_Medication_Safety_Education_with_references.docx` | `generate_medication_figures.py` | `medication_figures/` |

`create_mechanical_drawing.py` produces `Mechanical_Part_Drawing.dxf` and is independent of the documents.

## Rebuilding

```bash
# 1. figures (each script accepts figure numbers, e.g. `python3 generate_il_figures.py 3 4`)
for g in generate_*_figures.py; do python3 "$g"; done

# 2. Word documents (all eight, figures embedded in place)
python3 tools/build_docx.py
# or a single document
python3 tools/build_docx.py Chapter_4_Experimentation.md Chapter_4_Experimentation.docx
```

The scripts need only the Python 3 standard library.

- Figures are written as SVG by `tools/svgfig.py`.
- The SVG is rasterised to 2× PNG with a headless Chromium (`chrome-headless-shell`). To use a different binary, set the `HEADLESS` path at the top of `tools/svgfig.py`.
- `tools/build_docx.py` writes the OOXML directly.

## Conventions

- **Figures.** A figure is a line `![Figure N](folder/file.png)` placed where it belongs in the text, followed by a caption paragraph starting with `**Figure N.**` (the Ionic Liquids manuscript uses `**Fig. N.**` instead).
- **Tables.** A table is preceded by a `**Table N.**` caption.
- **Data policy for figures.** Figures plot only values stated in the documents. Some figures are conceptual or illustrative, for example where per-condition data or the original micrographs are not part of the repository. These are labelled as such on the figure itself. The schematic EDS, optical and SEM panels in the Ionic Liquids Fig. 5 should be replaced with the original images before publication.
- `tools/docx_to_md.py` and `tools/normalize_figures.py` are one-off helpers. They were used to extract the Markdown sources for Chapter 4 and Chapter 16 from the earlier Word files.
