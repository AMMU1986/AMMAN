#!/usr/bin/env python3
"""
Build the final Chapter 5 with numbered square-bracket citations.

- In-text APA citations are mapped to the USER'S authoritative master list
  ([1]-[65]) rather than order-of-appearance.
- 26 new, verified references ([66]-[91]) are inserted at anchor sentences.
- The reference list is emitted as [1]-[91] (master list first, then new refs).

APA-style entries, square-bracket numbering.
"""

import re
import os

BASE = '/projects/sandbox/AMMAN/Chapter_5_APA_base.md'
OUT = '/projects/sandbox/AMMAN/Chapter_5_Results_and_Discussion.md'


# ---------------------------------------------------------------------------
# 1.  Author-token normaliser (first surname only) + year -> KEY
# ---------------------------------------------------------------------------
INITIALS = set('abcdefghijklmnopqrstuvwxyz')


def first_surname(auth):
    a = auth.lower().replace('&', ' ')
    a = re.sub(r'\bet al\.?', ' ', a)
    a = a.split(',')[0]
    a = re.sub(r'[^a-zà-ÿ \-]', ' ', a)   # keep hyphen (e.g. Paniagua-Mercado)
    toks = [t for t in a.split() if len(t) > 1 and t not in ('and', 'the')]
    return toks[0] if toks else ''


def key(auth, year):
    return f'{first_surname(auth)}|{year}'


# ---------------------------------------------------------------------------
# 2.  USER MASTER LIST  ([1]-[65]) -> (number, full APA text)
#     Keyed by first-surname|year(+letter).  Disambiguation letters (a-e)
#     match those used in the chapter body.
# ---------------------------------------------------------------------------
MASTER = [
    # (num, key, full APA text)
    (1,  'kumar|2022',        "Kumar, A., & Chhibber, R. (2022). Investigation of the wetting behavior of formulated SMAW electrode coating fluxes with regression and ANN model. *Metallurgical and Materials Transactions B.*"),
    (2,  'kumar|2023',        "Kumar, A., Sharma, L., & Chhibber, R. (2023). Wettability studies of formulated SMAW electrode coating fluxes with regression analysis and neural network approach. *Ceramics International, 49*(7), 10224–10237."),
    (3,  'kumar|2024a',       "Kumar, A., & Chhibber, R. (2024). Thermal property characterization and modeling of SMAW electrode coating flux using ANN and regression analysis. *Proceedings of the Institution of Mechanical Engineers, Part B: Journal of Engineering Manufacture.*"),
    (4,  'kumar|2023b',       "Kumar, A., Sharma, L., & Chhibber, R. (2023). Investigation and modeling of the SMAW coating flux thermal properties using neural network and regression analysis. *Ceramics International, 49*(11), 17753–17765."),
    (5,  'kumar|2024b',       "Kumar, A., & Chhibber, R. (2024). Element transfer, microhardness and metallurgical analysis of weld-bead using CaF₂–CaO–Al₂O₃–BaO fluxes. *Materials Science and Technology, 40*(18), 1377–1391."),
    (6,  'sharma|2019a',      "Sharma, L., & Chhibber, R. (2019). Investigating the physicochemical and thermophysical properties of submerged arc welding fluxes designed using TiO₂–SiO₂–MgO and SiO₂–MgO–Al₂O₃ flux systems for linepipe steels. *Ceramics International, 45*(2), 1569–1587."),
    (7,  'sharma|2019b',      "Sharma, L., & Chhibber, R. (2019). Design and development of submerged arc welding fluxes using TiO₂–SiO₂–CaO and SiO₂–CaO–Al₂O₃ flux systems. *Proceedings of the Institution of Mechanical Engineers, Part E: Journal of Process Mechanical Engineering, 233*(4), 739–762."),
    (8,  'sharma|2019c',      "Sharma, L., & Chhibber, R. (2019). Design of CaO–SiO₂–CaF₂ and CaO–SiO₂–Al₂O₃ based submerged arc fluxes for a series of bead-on-plate pipeline steel welds: Effect on carbon and manganese content, grain size and microhardness. *Journal of Pressure Vessel Technology, 141*(1), 011404."),
    (9,  'sharma|2019f',      "Sharma, L., Kumar, J., & Chhibber, R. (2019). Experimental investigation on high-temperature wettability and structural behaviour of SAW fluxes using MgO–TiO₂–SiO₂ and Al₂O₃–MgO–SiO₂ flux systems. *Ceramics International, 45*(17), 22142–22155."),
    (10, 'sharma|2019d',      "Sharma, L., & Chhibber, R. (2019). Design and development of submerged arc welding slags using CaO–SiO₂–CaF₂ and CaO–SiO₂–Al₂O₃ systems. *Silicon, 12*(9), 2179–2190."),
    (11, 'sharma|2019e',      "Sharma, L., & Chhibber, R. (2019). Effect of heat treatment on mechanical properties and corrosion behaviour of API X70 linepipe steel in different environments. *Transactions of the Indian Institute of Metals, 72*(1), 93–110."),
    (12, 'sharma|2018',       "Sharma, L., & Chhibber, R. (2018). Mechanical properties and hydrogen induced cracking behaviour of API X70 SAW weldments. *International Journal of Pressure Vessels and Piping, 165*, 193–207."),
    (13, 'arya|2018',         "Arya, H. K., Singh, K., & Saxena, R. K. (2018). Effect of weld cooling rates on mechanical and metallurgical properties of submerged arc welded pressure vessel steel. *Journal of Pressure Vessel Technology, 140*(4), 041406."),
    (14, 'arora|2018',        "Arora, K. S., Pandu, R. S., Shajan, N., Pathak, P., & Shome, M. (2018). Microstructure and impact toughness of reheated coarse-grain heat-affected zones of API X65 and API X80 linepipe steels. *International Journal of Pressure Vessels and Piping, 167*, 37–47."),
    (15, 'beidokhti|2009',    "Beidokhti, B., Koukabi, A. H., & Dolati, A. (2009). Effect of titanium addition on the microstructure and inclusion formation in submerged arc welded HSLA pipeline steel. *Journal of Materials Processing Technology, 209*(8), 4027–4035."),
    (16, 'houldcroft|1989',   "Houldcroft, P. T. (1989). *Submerged-arc welding.* Abington Publishing."),
    (17, 'kou|2003',          "Kou, S. (2003). *Welding metallurgy* (2nd ed.). John Wiley & Sons."),
    (18, 'davis|1977',        "Davis, M. L. E., & Coe, F. R. (1977). *The chemistry of submerged arc welding fluxes* (Welding Institute Research Report No. 39/1977/M). The Welding Institute."),
    (19, 'kanjilal|2006',     "Kanjilal, P., Pal, T. K., & Majumdar, S. K. (2006). Combined effect of flux and welding parameters on chemical composition and mechanical properties of submerged arc weld metal. *Journal of Materials Processing Technology, 171*(2), 223–231."),
    (20, 'bang|2009',         "Bang, K., Park, C., Jung, H., & Lee, J. (2009). Effects of flux composition on the element transfer and mechanical properties of weld metal in submerged arc welding. *Metals and Materials International, 15*(3), 471–477."),
    (21, 'kanjilal|2005',     "Kanjilal, P., Majumdar, S. K., & Pal, T. K. (2005). Prediction of acicular ferrite in C–Mn steel weld metals. *ISIJ International, 45*(6), 876–885."),
    (22, 'davis|1991',        "Davis, M. L. E., & Bailey, N. (1991). Evidence of inclusion chemistry for element transfer in submerged arc welding. *Welding Journal Research Supplement, 70*(2), 58–65."),
    (23, 'north|1978',        "North, T. H., Bell, H. B., Nowicki, A., & Craig, I. (1978). Slag/metal interaction, oxygen and toughness in submerged arc welding. *Welding Journal Research Supplement, 57*(3), 63S–75S."),
    (24, 'datta|2008',        "Datta, S., Bandyopadhyay, A., & Pal, P. K. (2008). Application of Taguchi philosophy for parametric optimization of bead geometry and HAZ width in submerged arc welding using a mixture of fresh flux and fused flux. *International Journal of Advanced Manufacturing Technology, 36*(7–8), 689–698."),
    (25, 'palm|1972',         "Palm, J. H. (1972). How fluxes determine the metallurgical properties of submerged arc welds. *Welding Journal,* 358S–360S."),
    (26, 'crespo|2007',       "Crespo, A. C., Puchol, R. Q., Gonzalez, L. P., Sanchez, L. G., Gomez Perez, C. R., Cedre, E. D., Mendez, T. O., & Pozol, J. A. (2007). Obtaining a submerged arc welding flux of the MnO–SiO₂–CaO–Al₂O₃–CaF₂ system by fusion. *Welding International, 21*(7), 502–511."),
    (27, 'campbell|1957',     "Campbell, H. C., & Johnson, W. C. (1957). Bonded fluxes for submerged arc welding of alloy steels. *Welding Journal.*"),
    (28, 'golovko|2011',      "Golovko, V. V., & Potapov, N. N. (2011). Special features of agglomerated (ceramic) fluxes in welding. *Welding International, 25*(11), 889–893."),
    (29, 'singh|2013',        "Singh, B., Khan, Z. A., & Siddiquee, A. N. (2013). Review on effect of flux composition on its behavior and bead geometry in submerged arc welding. *Journal of Mechanical Engineering Research, 5*(7), 123–127."),
    (30, 'paniagua-mercado|2005', "Paniagua-Mercado, A. M., Lopez-Hirata, V. M., & Saucedo-Munoz, M. L. (2005). Influence of the chemical composition of flux on the microstructure and tensile properties of submerged-arc welds. *Journal of Materials Processing Technology, 169*(3), 346–351."),
    (31, 'adeyeye|2008',      "Adeyeye, A. D., & Oyawale, F. A. (2008). Mixture experiments and their applications in welding flux design. *Journal of the Brazilian Society of Mechanical Sciences and Engineering, 30*(4), 319–326."),
    (32, 'jackson|1973',      "Jackson, C. E. (1973). *Fluxes and slags in welding* (Welding Research Council Bulletin No. 190). Welding Research Council."),
    (33, 'chai|1982',         "Chai, C. S., & Eagar, T. W. (1982). Slag-metal reactions in binary CaF₂–metal oxide welding fluxes. *Welding Journal, 61*(7), 229–232."),
    (34, 'kanjilal|2007',     "Kanjilal, P., Pal, T. K., & Majumdar, S. K. (2007). Prediction of element transfer in submerged arc welding. *Welding Journal, 86*(4), 135S–146S."),
    (35, 'schwemer|1979',     "Schwemer, D. D., Olson, D. L., & Williamson, D. L. (1979). Relationship of weld penetration to the welding flux. *Welding Research Supplement,* 153S–160S."),
    (36, 'dallam|1985',       "Dallam, C. B., Liu, S., & Olson, D. L. (1985). Flux composition dependence of microstructure and toughness of submerged arc HSLA weldments. *Welding Research Supplement,* 140S–152S."),
    (37, 'fox|1996',          "Fox, A. G., Eakes, M. W., & Franke, G. I. (1996). The effect of small changes in flux basicity on the acicular ferrite content and mechanical properties of submerged arc weld metal. *Welding Research Supplement,* 330S–342S."),
    (38, 'plessis|2007',      "Plessis, J. D., Toit, M. D., & Pistorius, P. C. (2007). Control of diffusible weld metal hydrogen through flux chemistry modification. *Welding Journal, 86*, 273–280."),
    (39, 'houldcroft|1977',   "Houldcroft, P. T. (1977). *Welding process technology.* Cambridge University Press."),
    (40, 'jung|2012',         "Jung, E. J., & Min, D. J. (2012). Effect of Al₂O₃ and MgO on interfacial tension between calcium silicate-based melts and a solid steel substrate. *Steel Research International, 83*(7), 705–711."),
    (41, 'jung|2010',         "Jung, E. J., Kim, W., Sohn, I., & Min, D. J. (2010). A study on the interfacial tension between solid iron and CaO–SiO₂–MO system. *Journal of Materials Science, 45*, 2023–2029."),
    (42, 'sharma|2019g',      "Sharma, L., & Chhibber, R. (2019). Design of TiO₂–SiO₂–MgO and SiO₂–MgO–Al₂O₃ based submerged arc fluxes for multi-pass bead-on-plate linepipe steel welds. *Journal of Pressure Vessel Technology, 141*(1), 011403."),
    (43, 'kim|2015',          "Kim, J. B., Choi, J. K., Han, I. W., & Sohn, I. (2015). High-temperature wettability and structure of the TiO₂–MnO–SiO₂–Al₂O₃ welding flux system. *Journal of Non-Crystalline Solids.*"),
    (44, 'quintana|2003',     "Quintana, R., Cruz, A., Perdomo, L., Castellanos, G., García, L. L., Formoso, A., & Cores, A. (2003). Study of the transfer efficiency of alloyed elements in fluxes during the submerged arc welding process. *Welding International, 17*(12), 958–965."),
    (45, 'jindal|2013a',      "Jindal, S., Chhibber, R., & Mehta, N. P. (2013). Investigation on flux design for submerged arc welding of high-strength low-alloy steel. *Proceedings of the Institution of Mechanical Engineers, Part B: Journal of Engineering Manufacture, 227*(3), 383–395."),
    (46, 'baune|2000',        "Baune, E., Bonnet, C., & Liu, S. (2000). Reconsidering the basicity of a FCAW consumable—Part 1: Solidified slag composition of a FCAW consumable as a basicity indicator. *Welding Journal, 79*(3), 57S–65S."),
    (47, 'jindal|2013b',      "Jindal, S., Chhibber, R., & Mehta, N. P. (2013). Effect of flux constituents and basicity index on mechanical properties and microstructural evolution of submerged arc welded high-strength low-alloy steel. *Materials Science Forum, 738–739*, 242–246."),
    (48, 'zhang|2022a',       "Zhang, J., Wang, X., Zhao, Y., & Liu, C. (2022). A review on parallel development of flux design and welding metallurgy in submerged arc welding. *Processes, 10*(11), 2305."),
    (49, 'astm|2023a',        "ASTM International. (2023). *ASTM E8/E8M: Standard test methods for tension testing of metallic materials.* ASTM International."),
    (50, 'adeyeye|2009',      "Adeyeye, A. D., & Oyawale, F. A. (2009). Weld-metal property optimization from flux ingredients through mixture experiments and mathematical programming approach. *Materials Research, 12*(3), 339–343."),
    (51, 'astm|2023b',        "ASTM International. (2023). *ASTM E23: Standard test methods for notched bar impact testing of metallic materials.* ASTM International."),
    (52, 'callister|2020',    "Callister, W. D., & Rethwisch, D. G. (2020). *Materials science and engineering: An introduction* (10th ed.). John Wiley & Sons."),
    (53, 'zhang|2022b',       "Zhang, J., Wang, X., Zhao, Y., & Liu, C. (2022). A review on parallel development of flux design and welding metallurgy in submerged arc welding. *Processes, 10*(11), 2305. https://doi.org/10.3390/pr10112305"),
    (54, 'kumar|2024c',       "Kumar, A., & Chhibber, R. (2024). Microhardness and element transfer investigation of weld bead using formulated SiO₂–CaO–CaF₂–BaO SMAW electrode coatings. *Proceedings of the Institution of Mechanical Engineers, Part C: Journal of Mechanical Engineering Science.*"),
    (55, 'bhadeshia|2001',    "Bhadeshia, H. K. D. H. (2001). *Bainite in steels: Transformations, microstructure and properties* (2nd ed.). Institute of Materials."),
    (56, 'lancaster|1999',    "Lancaster, J. F. (1999). *The metallurgy of welding* (6th ed.). Woodhead Publishing."),
    (57, 'easterling|1992',   "Easterling, K. (1992). *Introduction to the physical metallurgy of welding.* Butterworth-Heinemann."),
    (58, 'svensson|1994',     "Svensson, L. E. (1994). *Control of microstructures and properties in steel arc welds.* CRC Press."),
    (59, 'thewlis|1994',      "Thewlis, G. (1994). Classification and quantification of microstructures in steels. *Materials Science and Technology, 10*(2), 110–125."),
    (60, 'olson|1986',        "Olson, D. L. (1986). Prediction of acicular ferrite formation in C–Mn steel weld metal. *Welding Journal Research Supplement,* 97S–106S."),
    (61, 'montgomery|2019',   "Montgomery, D. C. (2019). *Design and analysis of experiments* (10th ed.). John Wiley & Sons."),
    (62, 'cornell|2011',      "Cornell, J. A. (2011). *Experiments with mixtures: Designs, models, and the analysis of mixture data* (3rd ed.). Wiley."),
    (63, 'myers|2016',        "Myers, R. H., Montgomery, D. C., & Anderson-Cook, C. M. (2016). *Response surface methodology* (4th ed.). Wiley."),
    (64, 'fisher|1935',       "Fisher, R. A. (1935). *The design of experiments.* Oliver & Boyd."),
    (65, 'piepel|1988',       "Piepel, G. F. (1988). Programs for generating extreme vertices and centroid designs for mixture experiments. *Journal of Quality Technology, 20*(2), 125–139."),
]

KEY2NUM = {k: n for (n, k, _t) in MASTER}

# Some body citations use forms not perfectly matching the master letter; map them.
ALIAS = {
    'kumar|2023': 2,          # Kumar et al. 2023 (narrative & paren)
    'sharma|2019': 6,         # bare "Sharma & Chhibber (2019)" -> default 6
    'zhang|2022': 48,
    'jung&kim|2010': 41,
    'jung&min|2012': 40,
}


def num_for(auth, year):
    k = key(auth, year)
    if k in KEY2NUM:
        return KEY2NUM[k]
    if k in ALIAS:
        return ALIAS[k]
    # try same surname + 4-digit year ignoring letter
    fs = first_surname(auth)
    base = year[:4]
    # prefer exact-letter matches already handled; now relaxed
    for (n, mk, _t) in MASTER:
        mfs, my = mk.split('|')
        if mfs == fs and my[:4] == base:
            return n
    return None


# ---------------------------------------------------------------------------
# 3.  NEW REFERENCES [66]-[91]  (verified metadata) + placement anchors.
#     Each: (num, apa_text, anchor_regex, insert_kind)
#       insert_kind 'after_sentence': append " [n]" before the period that ends
#       the sentence containing the FIRST match of anchor_regex.
# ---------------------------------------------------------------------------
NEWREFS = [
    (66, "Gao, J., Wen, G., Huang, T., Bai, B., Tang, P., & Liu, Q. (2022). Probing viscosity and structural variations in CaF₂–SiO₂–MnO welding fluxes. *Metallurgical and Materials Transactions B, 53*(4), 2814–2823. https://doi.org/10.1007/s11663-022-02566-7",
     r"corroborating the structural trend reported by Kim et al\."),
    (67, "Zhang, Y., Coetsee, T., & Wang, C. (2022). Evaluation of the flux basicity concept geared toward estimation of oxygen content in submerged arc welded metal. *Metals, 12*(9), 1530. https://doi.org/10.3390/met12091530",
     r"varied inversely with the basicity index"),
    (68, "Zhang, Y., Liu, H., Coetsee, T., Wang, Z., & Wang, C. (2023). Identifying oxygen transfer pathways during high-heat-input submerged arc welding: A case study into CaF₂–SiO₂–CaO–TiO₂ fluxes. *Metallurgical and Materials Transactions B, 54*(6), 2875–2880. https://doi.org/10.1007/s11663-023-02922-1",
     r"greater retention of crystalline titania"),
    (69, "Coetsee, T., & De Bruin, F. (2022). Element transfer behaviour for a CaF₂–Na₂O–SiO₂ agglomerated flux subject to the submerged arc welding process. *Processes, 10*(9), 1847. https://doi.org/10.3390/pr10091847",
     r"the well-documented desulfurizing action of the basic oxides"),
    (70, "Wang, Q., Wang, X., & Luo, X. (2020). Effect of basicity on the structure, viscosity and crystallization of CaO–SiO₂–B₂O₃-based mold fluxes. *Metals, 10*(9), 1240. https://doi.org/10.3390/met10091240",
     r"more effectively \[52\]"),
    (71, "Coetsee, T. (2024). Recycling welding fluxes: A case study into the manganese-silicate system. *Metallurgical and Materials Transactions B, 55*(6), 4045–4056. https://doi.org/10.1007/s11663-024-03252-6",
     r"higher configurational entropy than polymerized networks"),
    (72, "Kumar, V. (2011). Modeling of weld bead geometry and shape relationships in submerged arc welding using developed fluxes. *Jordan Journal of Mechanical and Industrial Engineering, 5*(5), 461–470.",
     r"obviating trial-and-error experimentation"),
    (73, "Chowdhury, S., Yadaiah, N., Prakash, S., Kumar, S., & Nirsanametla, Y. (2023). Effect of physico-chemical properties of submerged arc welding fluxes on pipeline steel: A brief review. *Archives of Metallurgy and Materials, 68*(1), 5–14.",
     r"reproducing the basicity–detachability relationship reported by Sharma and Chhibber \[8\]"),
    (74, "Kumar, S., & Nadkarni, S. V. (2022). Application of response surface methodology for optimization of submerged arc welding process parameters. In *Advances in materials and manufacturing engineering* (pp. 51–61). Springer.",
     r"single-response treatments \[63\]"),
    (75, "Adeyeye, A. D., & Oyawale, F. A. (2021). Current trends in welding flux development. *Nigerian Journal of Technology, 40*(4), 622–631.",
     r"the non-linear composition–property relationships that govern the final weld properties"),
    (76, "Giarola, J. M., Calderón-Hernández, J. W., Conde, F. F., Marcomini, J. B., de Melo, H. G., Avila, J. A., & Bose Filho, W. W. (2021). Corrosion behavior and microstructural characterization of friction stir welded API X70 steel. *Journal of Materials Engineering and Performance, 30*(8), 5953–5961. https://doi.org/10.1007/s11665-021-05640-4",
     r"exerts over weld-metal chemistry and inclusion morphology"),
    (77, "Ahmed, M., Hamdy, S., & El-Sayed, A. (2025). Microstructural evolution, mechanical properties, and corrosion resistance of welded X70 pipeline steel: Effects of thermal welding cycles on cap and root regions. *International Journal of Advanced Manufacturing Technology, 139*, 2965–2975. https://doi.org/10.1007/s00170-025-16052-2",
     r"reproduce the aggressive marine and offshore service environment"),
    (78, "Vieira, L. G., de Souza, G. A., Ventrella, V. A., & Gallego, J. (2023). Optimization of submerged arc welding parameters to improve corrosion resistance and hardness in API 5L X70 steel joints using support vector regression and a multi-objective genetic algorithm. *International Journal of Advanced Manufacturing Technology, 126*, 3735–3748. https://doi.org/10.1007/s00170-023-11070-4",
     r"the control that flux composition exerts over"),
    (79, "Kim, S.-J., Kim, K.-Y., & Yang, W.-S. (2018). Molybdenum effects on pitting corrosion resistance of FeCrMnMoNC austenitic stainless steels. *Metals, 8*(8), 653. https://doi.org/10.3390/met8080653",
     r"enhancing pitting resistance relative to molybdenum-free fluxes"),
    (80, "Wang, Z., Zhang, L., Zhang, Z., Marcus, P., & Maurice, V. (2023). Molybdenum effects on the stability of passive films unraveled at the nanometer and atomic scales. *npj Materials Degradation, 7*, 4. https://doi.org/10.1038/s41529-023-00418-6",
     r"resist breakdown in chloride environments"),
    (81, "Loable, C., Ryl, J., Kokot, A., Zielinski, A., & Ryl, J. (2024). Combined role of molybdenum and nitrogen in limiting corrosion and pitting of super austenitic stainless steel. *Heliyon, 10*(4), e26372. https://doi.org/10.1016/j.heliyon.2024.e26372",
     r"resist breakdown in chloride environments"),
    (82, "Zhang, B., Wang, J., Wu, B., Guo, X. W., Wang, Y. J., Chen, D., Zhang, Y. C., Du, K., Oguzie, E. E., & Ma, X. L. (2018). Unmasking chloride attack on the passive film of metals. *Nature Communications, 9*, 2559. https://doi.org/10.1038/s41467-018-04942-x",
     r"nucleate micro-pits \[23\]"),
    (83, "Ünsal, T., Cao, Y., Wang, Z., Bettge, D., & Ozcan, O. (2022). Operando electrochemical TEM, ex-situ SEM and atomistic modeling studies of MnS dissolution and its role in triggering pitting corrosion in 304L stainless steel. *Corrosion Science, 201*, 110268. https://doi.org/10.1016/j.corsci.2022.110268",
     r"serve as preferential pit-initiation sites"),
    (84, "Zhao, Y., Zhang, T., & Wang, F. (2025). Understanding the non-steady electrochemical mechanisms of the stress corrosion cracking of X70 pipeline steel in a marine environment. *Materials, 18*(9), 2073. https://doi.org/10.3390/ma18092073",
     r"supporting the systematic flux-design strategy advanced for marine and offshore pipeline applications"),
    (85, "Fu, C., Li, X., Li, H., Han, T., Han, B., & Wang, Y. (2022). Influence of ICCGHAZ on the low-temperature toughness in the HAZ of heavy-wall X80 pipeline steel. *Metals, 12*(6), 907. https://doi.org/10.3390/met12060907",
     r"coarse prior-austenite grains \[14, 54\]|coarse prior-austenite grains"),
    (86, "Li, X., Fan, Y., Ma, X., Subramanian, S. V., & Shang, C. (2019). Effect of heat input on the M-A constituent and toughness of the coarse-grained heat-affected zone in an X100 pipeline steel. *Journal of Materials Engineering and Performance, 28*(4), 1932–1940. https://doi.org/10.1007/s11665-019-03921-7",
     r"the modest increase in coarse-grained-HAZ hardness \[55\]"),
    (87, "Han, Y., Zhang, C., & Wang, J. (2026). Nitrogen content effects on microstructural evolution and low-temperature impact toughness in the coarse-grained heat-affected zone of welded X70 pipeline steel. *Metals, 16*(3), 331. https://doi.org/10.3390/met16030331",
     r"developed predominantly bainite and acicular ferrite for all fluxes"),
    (88, "Wan, X. L., Wu, K. M., Cheng, L., & Wei, R. (2018). Effect of Ti addition on the microstructure and mechanical properties of weld metals in HSLA steels. *Journal of Materials Engineering and Performance, 27*(11), 5946–5956. https://doi.org/10.1007/s11665-018-3686-y",
     r"a modest reduction in carbon equivalent \[15\]"),
    (89, "Zhu, Z., Han, J., & Li, H. (2022). Evaluation of the mechanical properties and microstructure of X70 pipeline steel with strain-based design. *Metals, 12*(10), 1616. https://doi.org/10.3390/met12101616",
     r"micro-alloyed with Mn, Mo, Ti, Cr, Nb, and Ni"),
    (90, "Wang, H.-H., Li, G.-Q., Lei, T.-C., & Zhao, Y. (2015). Structure–property–fracture mechanism correlation in the heat-affected zone of X100 ferrite–bainite pipeline steel. *Metallurgical and Materials Transactions E, 1*(1), 40–53. https://doi.org/10.1007/s40553-014-0036-3",
     r"signifying lower fracture resistance in accordance with the microstructure–toughness relationship of Thewlis \[59\]"),
    (91, "Yang, J., Xin, L., Wang, X., & Wang, C. (2009). Microstructure and toughness of weld metals of pipeline steels welded by four-wire submerged arc welding. *International Journal of Minerals, Metallurgy and Materials, 16*(4), 425–429. https://doi.org/10.1016/S1674-4799(09)60011-X",
     r"sustain toughness to sub-zero temperatures \[21, 59\]"),
]


# ---------------------------------------------------------------------------
# 4.  Convert in-text APA citations -> [n] against MASTER
# ---------------------------------------------------------------------------
def convert_citations(body):
    unmatched = []

    author = (r'[A-Z][A-Za-zÀ-ÿ.\'\-]+'
              r'(?:, [A-Z][A-Za-zÀ-ÿ.\'\-]+)*'
              r'(?:,? (?:&|and) [A-Z][A-Za-zÀ-ÿ.\'\-]+)?'
              r'(?: et al\.)?')
    unit_re = re.compile(r'(' + author + r'),\s*'
                         r'((?:19|20)\d{2}[a-z]?(?:\s*,\s*(?:19|20)\d{2}[a-z]?)*)')
    paren_re = re.compile(r'\(([^()]*?\b(?:19|20)\d{2}[a-z]?[^()]*?)\)')
    narr_re = re.compile(
        r'([A-Z][A-Za-zÀ-ÿ.\'\-]+'
        r'(?:,? (?:&|and) [A-Z][A-Za-zÀ-ÿ.\'\-]+|, [A-Z][A-Za-zÀ-ÿ.\'\-]+| et al\.)*)'
        r'\s\(((?:19|20)\d{2}[a-z]?(?:\s*,\s*(?:19|20)\d{2}[a-z]?)*)\)')

    def emit(nums):
        nums = sorted({n for n in nums if n})
        return '[' + ', '.join(map(str, nums)) + ']'

    matches = []
    for m in narr_re.finditer(body):
        matches.append((m.start(), m.end(), 'narr', m))
    for m in paren_re.finditer(body):
        chunks = [c.strip() for c in m.group(1).split(';')]
        cc = [c for c in chunks if unit_re.fullmatch(c)]
        if not cc:
            continue
        matches.append((m.start(), m.end(), 'paren' if len(cc) == len(chunks) else 'mixed', m))

    matches.sort(key=lambda t: (t[0], -(t[1] - t[0])))
    selected, last = [], -1
    for s, e, k, m in matches:
        if s < last:
            continue
        selected.append((s, e, k, m))
        last = e

    out, cur = [], 0
    for s, e, k, m in selected:
        out.append(body[cur:s])
        if k == 'narr':
            auth = m.group(1).strip()
            yrs = re.findall(r'(?:19|20)\d{2}[a-z]?', m.group(2))
            nums = []
            for y in yrs:
                n = num_for(auth, y)
                if not n:
                    unmatched.append(f'{auth} ({y})')
                nums.append(n)
            out.append(f'{auth} {emit(nums)}')
        elif k == 'paren':
            nums = []
            for c in (x.strip() for x in m.group(1).split(';')):
                um = unit_re.fullmatch(c)
                a = um.group(1).strip()
                for y in re.findall(r'(?:19|20)\d{2}[a-z]?', um.group(2)):
                    n = num_for(a, y)
                    if not n:
                        unmatched.append(f'{a} ({y})')
                    nums.append(n)
            out.append(emit(nums))
        else:  # mixed
            kept, nums = [], []
            for c in (x.strip() for x in m.group(1).split(';')):
                um = unit_re.fullmatch(c)
                if um:
                    a = um.group(1).strip()
                    for y in re.findall(r'(?:19|20)\d{2}[a-z]?', um.group(2)):
                        n = num_for(a, y)
                        if not n:
                            unmatched.append(f'{a} ({y})')
                        nums.append(n)
                else:
                    kept.append(c)
            out.append('(' + '; '.join(kept) + ' ' + emit(nums) + ')')
        cur = e
    out.append(body[cur:])
    return ''.join(out), unmatched


# ---------------------------------------------------------------------------
# 5.  Insert the 26 new citations at their anchor sentences.
# ---------------------------------------------------------------------------
def insert_new_citations(body):
    """Insert each new ref at its anchor using a temporary placeholder token
    @@ORIGID@@ so we can later renumber strictly by reading order."""
    inserted = []
    for origid, _apa, anchor, *_ in NEWREFS:
        rx = re.compile(anchor)
        mm = rx.search(body)
        if not mm:
            inserted.append((origid, False))
            continue
        tail = body[mm.end():]
        pm = re.search(r'\.(?=\s|$|\))', tail)
        if not pm:
            inserted.append((origid, False))
            continue
        pos = mm.end() + pm.start()
        token = f'@@{origid}@@'
        # Merge into an existing bracket group if one ends right before the period.
        pre = body[:pos]
        mnums = re.search(r'(\[[\d,\s@]+\])\s*$', pre)
        if mnums:
            inside = mnums.group(1)[1:-1].strip()
            newtag = '[' + inside + ', ' + token + ']'
            body = pre[:mnums.start()] + newtag + body[pos:]
        else:
            body = body[:pos] + f' [{token}]' + body[pos:]
        inserted.append((origid, True))
    return body, inserted


def renumber_serial(body):
    """Assign final numbers 66.. to placeholders in strict reading order.
    Returns (body_with_final_numbers, origid->finalnum map)."""
    order = []
    for m in re.finditer(r'@@(\d+)@@', body):
        oid = int(m.group(1))
        if oid not in order:
            order.append(oid)
    mapping = {oid: 66 + i for i, oid in enumerate(order)}
    # Replace placeholders with their final numbers.
    def repl(m):
        return str(mapping[int(m.group(1))])
    body = re.sub(r'@@(\d+)@@', repl, body)
    # Normalise every bracket group: sort numbers ascending, dedupe.
    def fix_group(m):
        nums = sorted({int(x) for x in re.findall(r'\d+', m.group(0))})
        return '[' + ', '.join(map(str, nums)) + ']'
    body = re.sub(r'\[[\d,\s]+\]', fix_group, body)
    return body, mapping


# ---------------------------------------------------------------------------
# 6.  Build reference list [1]-[91]
# ---------------------------------------------------------------------------
def build_refs(mapping):
    """mapping: origid -> final number. New refs listed in final-number order."""
    lines = ['## References', '']
    for (n, _k, t) in MASTER:
        lines.append(f'[{n}] {t}')
        lines.append('')
    # order new refs by their assigned final number
    text_by_origid = {origid: t for (origid, t, *_rest) in NEWREFS}
    for origid in sorted(mapping, key=lambda o: mapping[o]):
        n = mapping[origid]
        lines.append(f'[{n}] {text_by_origid[origid]}')
        lines.append('')
    return '\n'.join(lines).rstrip() + '\n'


def main():
    with open(BASE, encoding='utf-8') as f:
        text = f.read()
    body = text.split('## References', 1)[0]

    body, unmatched = convert_citations(body)
    body, inserted = insert_new_citations(body)
    body, mapping = renumber_serial(body)

    final = body.rstrip() + '\n\n' + build_refs(mapping)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(final)

    print('Unmatched in-text citations:', len(unmatched))
    for u in sorted(set(unmatched)):
        print('   MISS:', u)
    missing_anchor = [origid for (origid, ok) in inserted if not ok]
    print('New refs successfully placed:', sum(1 for _, ok in inserted if ok), '/', len(inserted))
    if missing_anchor:
        print('   Anchor NOT found for orig-ids:', missing_anchor)
    print('Serial mapping (orig->final):',
          {o: mapping[o] for o in sorted(mapping, key=lambda o: mapping[o])})


if __name__ == '__main__':
    main()
