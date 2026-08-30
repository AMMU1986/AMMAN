# -*- coding: utf-8 -*-
"""
Chapter 2 content for "Soil Pollution in the Anthropocene".
Structured as a list of blocks consumed by build_docx.py.

Block types:
  ("title", text)
  ("subtitle", text)
  ("h1", text)          chapter / major heading
  ("h2", text)          section heading
  ("h3", text)          subsection heading
  ("abstract_h", text)  abstract heading (styled)
  ("p", text)           body paragraph (may contain [n] citations, keywords)
  ("fig", (imgfile, number, caption))
  ("table", (number, caption, headers[list], rows[list of lists]))
  ("refs_h", text)
  ("ref", text)         a single reference (already numbered)
"""

BOOK_TITLE = "Soil Pollution in the Anthropocene"
BOOK_SUBTITLE = "From Molecular Diagnostics to Global Remediation"
CHAPTER_TITLE = ("Chapter 2  Soil Pollution on a Global Scale: "
                 "Maps, Trends, and Hotspots")

ABSTRACT = (
    "Soil is a finite, slowly renewable resource that underpins food security, "
    "water regulation, carbon storage, and terrestrial biodiversity, yet it is "
    "increasingly compromised by the accumulation of chemical contaminants at a "
    "planetary scale. This chapter synthesizes the global picture of soil "
    "pollution during the Anthropocene, integrating the geographic distribution "
    "of major pollutant classes, the construction and interpretation of global "
    "soil contamination maps, and the socio-economic drivers that concentrate "
    "contamination in identifiable hotspots. We examine how heavy metals, "
    "pesticides, hydrocarbons, and persistent organic pollutants are distributed "
    "across agricultural, industrial, urban, and mining landscapes, and how "
    "natural geochemical backgrounds are increasingly overwritten by anthropogenic "
    "loading. The chapter reviews advances in remote sensing, geographic "
    "information systems, geostatistical interpolation, and machine learning that "
    "together enable predictive mapping of contamination and the ranking of "
    "high-risk regions. We further consider the temporal evolution of soil "
    "pollution, the biogeochemical processes governing pollutant fate and "
    "bioavailability, and the cascading ecological, agricultural, and human-health "
    "consequences of contaminated land. Finally, we discuss monitoring "
    "technologies, harmonized global standards, and risk-based frameworks for "
    "prioritizing remediation. By linking spatial evidence with mechanistic "
    "understanding and governance, the chapter provides a foundation for the "
    "molecular diagnostic and remediation strategies developed in later chapters, "
    "and argues that a coordinated, data-driven, and equity-aware approach is "
    "essential for safeguarding soils as a shared global resource."
)

# Body is defined as a sequence of (kind, payload) tuples in build order.
