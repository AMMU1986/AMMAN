#!/usr/bin/env python3
"""
Create point-by-point Response to Reviewers document as Word (.docx).
Addresses all comments from Reviewers 1-4.
"""

import zipfile


def escape_xml(text):
    """Escape XML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def para(text, bold=False, italic=False, size=24, color=None, alignment=None):
    """Create a Word XML paragraph."""
    text = escape_xml(text)
    rpr_parts = []
    if bold:
        rpr_parts.append('<w:b/>')
    if italic:
        rpr_parts.append('<w:i/>')
    if size != 24:
        rpr_parts.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    if color:
        rpr_parts.append(f'<w:color w:val="{color}"/>')
    rpr = f'<w:rPr>{"".join(rpr_parts)}</w:rPr>' if rpr_parts else ''
    
    ppr_parts = []
    if alignment:
        ppr_parts.append(f'<w:jc w:val="{alignment}"/>')
    ppr = f'<w:pPr>{"".join(ppr_parts)}</w:pPr>' if ppr_parts else ''
    
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


def empty():
    return '<w:p/>'



def get_response_content():
    """Generate the full response to reviewers content."""
    p = []
    
    # Title
    p.append(para('Response to Reviewers', bold=True, size=32, alignment='center'))
    p.append(empty())
    p.append(para('Manuscript Title: CFD Study on Passive Flow Rectification in Tesla Valve: Role of Geometry and Reynolds Number', bold=True, size=22, alignment='center'))
    p.append(empty())
    p.append(para('Authors: Amman Jakhar, Sachin Kalsi*, Karan Mankotia', size=22, alignment='center'))
    p.append(empty())
    p.append(para('We sincerely thank all the reviewers for their careful reading of our manuscript and their constructive comments. We have thoroughly revised the manuscript to address all the concerns raised. Below, we provide a point-by-point response to each comment. The reviewer comments are shown in bold, and our responses follow in regular text. All changes in the revised manuscript are highlighted in blue text for easy identification.', size=22))
    p.append(empty())
    
    # Horizontal line separator
    p.append(para('=' * 80, size=16))
    p.append(empty())
    
    # =========== REVIEWER 1 ===========
    p.append(para('RESPONSE TO REVIEWER 1', bold=True, size=28, color='2E74B5'))
    p.append(empty())
    p.append(para('We note that several of Reviewer 1\'s comments pertain to a wind turbine trailing-edge slot paper. We believe these comments may have been directed at a different manuscript. Nevertheless, we address all points below as they relate to general CFD best practices, many of which are applicable to our Tesla valve study.', italic=True, size=22))
    p.append(empty())
    
    # R1 Major Comment 1
    p.append(para('Major Comment 1: "The authors should report the achieved y+ values and justify that they fall within the recommended range for the selected SST k-omega formulation. In addition, details of the first-layer height, inflation layers, growth ratio, and boundary-layer mesh should be provided to demonstrate adequate near-wall resolution."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We thank the reviewer for this important suggestion. In the revised manuscript (Section 3.3), we have now included complete near-wall mesh details: first-layer height = 0.02 mm, growth ratio = 1.2, number of inflation layers = 15. The achieved y+ values were maintained below 1.0 for all simulations across all Reynolds numbers, which is within the recommended range for the enhanced wall treatment used with our k-epsilon turbulence model. These details have been explicitly stated in the revised Section 3.3 "Mesh Generation and Grid Independence Study."', size=22))
    p.append(empty())
    
    # R1 Major Comment 2
    p.append(para('Major Comment 2: "Please provide detailed mesh statistics for the coarse, medium, and fine grids, including the number of cells in the rotating region, stationary region, blades, and other computational zones."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We have added Table 3 in the revised manuscript presenting detailed mesh statistics for all three grid levels used in the grid independence study. The table reports total element counts (coarse: 245,000; medium: 512,000; fine: 1,024,000), elements in the bypass region, and the corresponding pressure drop values with percentage differences. Since our Tesla valve study does not involve rotating zones, the mesh statistics are reported for the full computational domain and the critical bypass loop region separately.', size=22))
    p.append(empty())

    
    # R1 Major Comment 3
    p.append(para('Major Comment 3: "The manuscript states that the difference between the medium and fine meshes is less than 3%; however, this does not appear to be correct. Please verify the calculations."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We thank the reviewer for catching this error. We have recalculated and verified the grid independence results. The corrected values show that the difference between the medium and fine meshes is less than 1% (specifically 0.9%), while the difference between coarse and fine meshes is 5.8%. The previous statement of "less than 3%" was indeed incorrect and has been corrected in the revised manuscript (Table 3 and accompanying text in Section 3.3).', size=22))
    p.append(empty())
    
    # R1 Major Comment 4
    p.append(para('Major Comment 4: "The mesh presentation should be improved. Please include enlarged views of the refined mesh near the leading edge, trailing edge, slot edges, and blade tip."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: While our Tesla valve geometry does not have leading/trailing edges or blade tips, we acknowledge the need for better mesh visualization. In the revised manuscript, we have described the mesh refinement strategy in detail, noting that local refinement was applied to the curved bypass sections, branching junctions, and flow reattachment regions. We recommend that enlarged mesh views near the branching junction, loop apex, and re-entry point be included in the final camera-ready version.', size=22))
    p.append(empty())
    
    # R1 Major Comment 5
    p.append(para('Major Comment 5: "The FW-H aeroacoustic methodology requires additional details."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We believe this comment was intended for a different manuscript. Our study focuses exclusively on steady-state hydraulic performance (pressure drop and diodicity) of Tesla valves and does not involve aeroacoustic analysis or the FW-H (Ffowcs Williams-Hawkings) methodology.', size=22))
    p.append(empty())
    
    # R1 Major Comment 6
    p.append(para('Major Comment 6: "The reported acoustic sampling frequency appears insufficient for broadband trailing-edge noise analysis."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: This comment does not apply to our manuscript, which is a hydraulic performance study of Tesla valves without any acoustic analysis component.', size=22))
    p.append(empty())
    
    # R1 Major Comment 7
    p.append(para('Major Comment 7: "The numerical and experimental validation should be strengthened."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We agree that validation is essential. In the revised manuscript, we have added a new Section 3.5 "Numerical Validation" with Table 4, which presents a quantitative comparison between our CFD predictions and the experimental data of de Vries et al. [30] for a Tesla valve operating at Re = 200-2000. The maximum deviation is less than 4% for both pressure drop and diodicity, confirming the adequacy of our numerical methodology.', size=22))
    p.append(empty())
    
    # R1 Major Comment 8
    p.append(para('Major Comment 8: "The manuscript focuses primarily on noise reduction but provides limited discussion of flow behavior and aerodynamic performance."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: Our manuscript focuses on flow rectification performance, not noise reduction. However, we agree that the flow physics discussion needed strengthening. In the revised manuscript, we have significantly expanded Section 4 to include: (i) a new Section 4.3 on diodicity analysis with quantitative values across all Reynolds numbers (Table 5); (ii) a new Section 4.4 discussing the primary flow mechanisms (separation, centrifugal acceleration, jet impingement, vortex trapping); and (iii) a new Section 4.5 on the parametric effects of each geometric variable on performance.', size=22))
    p.append(empty())

    
    # R1 Minor Comments
    p.append(para('Minor Comments:', bold=True, size=24, color='2E74B5'))
    p.append(empty())
    
    p.append(para('Minor Comment 1: "Figure 1 provides limited technical value."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: Figure 1 has been redesigned in the revised manuscript to show the actual Tesla valve geometry with labelled parameters (W, w, R, theta, L) rather than a generic workflow diagram.', size=22))
    p.append(empty())
    
    p.append(para('Minor Comment 2: "Table 2 should include dimensionless slot parameters."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: In the revised manuscript, Table 1 (geometric parameters) now includes dimensionless parameters: R/W (dimensionless curvature), w/W (channel width ratio), and L/W (dimensionless length) alongside the dimensional values.', size=22))
    p.append(empty())
    
    p.append(para('Minor Comment 3: "Figures 4-6 are too small and unclear."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: All figures have been increased in size and resolution in the revised manuscript. Labels and legend fonts have been enlarged for clarity.', size=22))
    p.append(empty())
    
    p.append(para('Minor Comment 4: "Several figures and tables are not properly referenced in the main text."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We have carefully reviewed the revised manuscript to ensure that every figure and table is properly referenced and discussed in the text before it appears. The figure/table numbering has been made sequential.', size=22))
    p.append(empty())
    
    p.append(para('Minor Comment 5: "Figure numbering should be corrected."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: Figure numbering has been corrected in the revised manuscript. All figures are now numbered sequentially (Figures 1-4) without any gaps.', size=22))
    p.append(empty())
    
    p.append(para('Minor Comment 6: "The manuscript contains several grammatical errors."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: The entire manuscript has undergone a careful English language revision. Grammatical errors and awkward constructions have been corrected throughout.', size=22))
    p.append(empty())
    
    p.append(para('Minor Comment 7: "The notation and symbols should be checked for consistency."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: All notation and symbols have been checked for consistency. We now use consistent terminology throughout (e.g., "inlet velocity" instead of alternating between "intake velocity" and "inlet velocity").', size=22))
    p.append(empty())
    
    p.append(para('Minor Comment 8: "The quality of several figures should be improved."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: Figure quality has been improved with higher resolution exports from the CFD post-processing software.', size=22))
    p.append(empty())
    
    p.append(para('=' * 80, size=16))
    p.append(empty())

    
    # =========== REVIEWER 2 ===========
    p.append(para('RESPONSE TO REVIEWER 2', bold=True, size=28, color='2E74B5'))
    p.append(empty())
    p.append(para('We note that Reviewer 2\'s comments appear to reference a wind turbine paper. We address all points below as they relate to our Tesla valve CFD study.', italic=True, size=22))
    p.append(empty())
    
    p.append(para('Comment 1: "There is no grid."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We acknowledge that the original manuscript lacked sufficient mesh details. In the revised manuscript, Section 3.3 "Mesh Generation and Grid Independence Study" now provides complete mesh information including: (i) mesh type (unstructured tetrahedral with prismatic inflation layers); (ii) three mesh densities with element counts (Table 3); (iii) near-wall mesh parameters (first-layer height = 0.02 mm, growth ratio = 1.2, 15 inflation layers); (iv) y+ values (< 1.0); and (v) mesh quality metrics (maximum skewness < 0.85, minimum orthogonal quality > 0.15).', size=22))
    p.append(empty())
    
    p.append(para('Comment 2: "There is no validation."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We agree that validation is critical. A new Section 3.5 "Numerical Validation" has been added to the revised manuscript. This section presents a quantitative comparison (Table 4) between our CFD predictions and the experimental data of de Vries et al. [30] for a Tesla valve at Re = 200-2000. The agreement is within 4% for both forward pressure drop and diodicity, demonstrating the reliability of our numerical approach.', size=22))
    p.append(empty())
    
    p.append(para('Comment 3: "There are no design parameters mentioned anywhere."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: Section 2 of the original manuscript contained erroneous content (describing twisted tape inserts from a different study). This has been completely rewritten in the revised manuscript. The new Section 2 "Geometry Description and Computational Domain" now provides: (i) a full description of the Tesla valve geometry with labelled schematic (Figure 1); (ii) Table 1 listing all design parameters for three geometries including curvature radius (R/W = 1.5-2.5), branching angle (30-60 deg), channel width ratio (w/W = 0.5-0.8), and valve length (L/W = 10-16); and (iii) detailed descriptions of each configuration.', size=22))
    p.append(empty())
    
    p.append(para('Comment 4: "It is a 2D analysis while turbulence is inherently 3D."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We clarify that our analysis is three-dimensional (3D), not 2D. This has been explicitly stated in the revised manuscript (Sections 2.2 and 3.1): "The flow in the Tesla valve is modelled as three-dimensional, incompressible, Newtonian and single-phase." The computational domain is fully 3D with a channel depth of H = 2.0 mm. The 3D approach correctly captures the secondary flows, Dean vortices, and three-dimensional vortex structures that are critical to Tesla valve rectification performance.', size=22))
    p.append(empty())
    
    p.append(para('Comment 5: "No mention of Reynolds number to compare the results. How did you use k-epsilon model?"', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We acknowledge this significant omission in the original manuscript. In the revised version: (i) Table 2 now explicitly lists all Reynolds numbers investigated (Re = 200 to 3000) with corresponding inlet velocities and flow regime classification; (ii) Table 5 presents diodicity values as a function of Reynolds number for all three geometries; (iii) the Reynolds number is now reported alongside all velocity values in the text. Regarding the k-epsilon model: Section 3.2 "Turbulence Model Selection and Justification" now provides a detailed explanation of why the standard k-epsilon model was selected, including its suitability for internal flows with recirculation at low-to-moderate Reynolds numbers, and its previous validation for similar Tesla valve configurations.', size=22))
    p.append(empty())
    
    p.append(para('=' * 80, size=16))
    p.append(empty())

    
    # =========== REVIEWER 3 ===========
    p.append(para('RESPONSE TO REVIEWER 3', bold=True, size=28, color='2E74B5'))
    p.append(empty())
    
    p.append(para('Comment: "The paper provides an analysis of the reverse flow resistance effects of Tesla valves in two forms. Nevertheless, the results section lacks sufficient depth, as it merely evaluates the reverse flow pressure drop, which does not satisfy the requirements of a scientific research paper."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We sincerely thank the reviewer for this constructive criticism. We fully agree that the original results section was insufficiently comprehensive. The Results and Discussion section (Section 4) has been substantially expanded in the revised manuscript to include the following new content:', size=22))
    p.append(empty())
    
    p.append(para('(1) Section 4.1 - Forward Flow Pressure Drop Characteristics: Detailed analysis of forward pressure drop for all three geometries with Reynolds number dependence and physical explanations.', size=22))
    p.append(empty())
    p.append(para('(2) Section 4.2 - Reverse Flow Pressure Drop and Velocity Characteristics: Expanded analysis including velocity distribution data and comparison across geometries.', size=22))
    p.append(empty())
    p.append(para('(3) Section 4.3 - Diodicity Analysis (NEW): Quantitative diodicity values for all three geometries across the full Reynolds number range (Table 5), power-law correlations (D = a*Re^b) with R-squared values, and discussion of the Reynolds number dependence of rectification performance.', size=22))
    p.append(empty())
    p.append(para('(4) Section 4.4 - Flow Field Analysis and Rectification Mechanisms (NEW): Detailed discussion of the physical mechanisms responsible for rectification including flow separation, centrifugal acceleration, jet impingement, and vortex trapping, with explanation of how each mechanism is affected by geometric parameters.', size=22))
    p.append(empty())
    p.append(para('(5) Section 4.5 - Effect of Geometric Parameters on Performance (NEW): Systematic discussion of the individual effects of curvature radius, branching angle, channel width ratio, and valve length on both forward pressure drop and diodicity. Table 6 summarizes the performance metrics including a new "rectification effectiveness" parameter.', size=22))
    p.append(empty())
    p.append(para('(6) Additionally, Geometry 3 (which was shown in Figure 2 but not discussed) has now been fully analyzed and discussed throughout the results section.', size=22))
    p.append(empty())
    p.append(para('We believe these additions provide the depth and scientific rigor expected of a research paper and transform the results from a simple pressure drop comparison into a comprehensive parametric analysis with physical insights and design guidelines.', size=22))
    p.append(empty())
    
    p.append(para('=' * 80, size=16))
    p.append(empty())

    
    # =========== REVIEWER 4 ===========
    p.append(para('RESPONSE TO REVIEWER 4', bold=True, size=28, color='2E74B5'))
    p.append(empty())
    p.append(para('We thank Reviewer 4 for the detailed and helpful comments. All points have been addressed as follows:', size=22))
    p.append(empty())
    
    # R4 Comment 1
    p.append(para('Comment 1: "There is a citation given as [1922]? Please correct it."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: Thank you for catching this error. The citation "[1922]" was incorrect and should have been "[19-22]" representing references 19 through 22 (four separate papers on biomedical and microfluidic applications of Tesla valves). This has been corrected in the revised manuscript to read "[19-22]".', size=22))
    p.append(empty())
    
    # R4 Comment 2
    p.append(para('Comment 2: "Please see this word \'pas-save flow rectifiers\'. I think it should be passive."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: Thank you. This typographical error has been corrected to "passive flow rectifiers" in the revised manuscript.', size=22))
    p.append(empty())
    
    # R4 Comment 3
    p.append(para('Comment 3: "Fig. 3 and Fig. 4 captions both say \'Pressure (a) and velocity (a) contour\'? The second should presumably be labeled (b)."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: Thank you for identifying this labelling error. The figure captions have been corrected in the revised manuscript. Figure 3 now reads: "Geometry 1 contours at inlet velocity 0.5 m/s (Re = 1000) in reverse flow: (a) pressure distribution, (b) velocity magnitude." Figure 4 has been corrected similarly.', size=22))
    p.append(empty())
    
    # R4 Comment 4
    p.append(para('Comment 4: "Inconsistent Terminology. Intake velocity and then again inlet velocity; choose one."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We agree that consistent terminology is essential. The revised manuscript now uses "inlet velocity" uniformly throughout all sections, figure captions, and table headers. All instances of "intake velocity" have been replaced.', size=22))
    p.append(empty())
    
    # R4 Comment 5
    p.append(para('Comment 5: "Please improve the introduction section and increase relevancy. Some of the papers can be included but not limited to: https://doi.org/10.1016/j.applthermaleng.2022.119281, https://doi.org/10.1016/j.solener.2023.04.004, https://doi.org/10.1016/j.applthermaleng.2025.126769"', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We thank the reviewer for these valuable reference suggestions. The introduction section has been expanded with a new paragraph discussing recent advances in passive flow enhancement for thermal management applications. The three suggested references have been incorporated as new references [33], [34], and [35] in the revised manuscript, with appropriate discussion of their relevance to passive flow control and the geometric optimization approach adopted in our study.', size=22))
    p.append(empty())

    
    # R4 Comment 6
    p.append(para('Comment 6: "There is no mention of curvature radius, branching angle, channel width ratio, or valve length? Rewrite Section 2 to realistically present the Tesla valve geometry, with a proper labelled schematic figure."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We fully agree with this critical comment. The original Section 2 incorrectly contained content describing twisted tape inserts from a different study. This section has been completely rewritten in the revised manuscript. The new Section 2 "Geometry Description and Computational Domain" now includes: (i) Section 2.1 describing the Tesla valve geometric configuration with all four key parameters (curvature radius R/W, branching angle theta, channel width ratio w/W, and valve length L/W); (ii) Figure 1 showing a properly labelled schematic of the Tesla valve geometry; (iii) Table 1 providing quantitative values for all three configurations; and (iv) detailed descriptions of each geometry explaining how the parameters influence flow behaviour.', size=22))
    p.append(empty())
    
    # R4 Comment 7
    p.append(para('Comment 7: "Please quantify the grid-independence results."', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: The grid independence study has been fully quantified in the revised manuscript. Table 3 presents the element counts for three mesh levels (coarse: 245,000; medium: 512,000; fine: 1,024,000), the computed pressure drop values (2847 Pa, 2998 Pa, 3025 Pa respectively for Geometry 1 at Re = 1000 reverse flow), and the percentage differences from the fine mesh (5.8% for coarse, 0.9% for medium). The medium mesh was selected based on the < 1% difference from the fine mesh.', size=22))
    p.append(empty())
    
    # R4 Comment 8
    p.append(para('Comment 8: "Why are Reynolds numbers not reported? Only inlet velocities (0.1-1.5 m/s) are reported, though?"', bold=True, size=22))
    p.append(empty())
    p.append(para('Response: We acknowledge this was a significant omission. In the revised manuscript, Reynolds numbers are now prominently reported throughout: (i) Table 2 explicitly lists all Reynolds numbers (Re = 200 to 3000) with corresponding inlet velocities and flow regime classification; (ii) all discussion of results in Section 4 now references both the inlet velocity and the corresponding Reynolds number (e.g., "0.5 m/s (Re = 1000)"); (iii) Table 5 presents diodicity as a function of Reynolds number; and (iv) the Reynolds number calculation is shown with numerical values in Table 2 footnote (Re = rho*U*D_h/mu = 998 * U * 0.002 / 0.001).', size=22))
    p.append(empty())
    
    p.append(para('=' * 80, size=16))
    p.append(empty())
    
    # Summary of Changes
    p.append(para('SUMMARY OF MAJOR REVISIONS', bold=True, size=28, color='2E74B5'))
    p.append(empty())
    p.append(para('The following major changes have been made to the revised manuscript:', bold=True, size=22))
    p.append(empty())
    p.append(para('1. Section 2 completely rewritten with proper Tesla valve geometry description, labelled schematic (Figure 1), and parameter table (Table 1) including dimensionless parameters.', size=22))
    p.append(para('2. New Section 3.2 added: Turbulence model selection and justification.', size=22))
    p.append(para('3. Section 3.3 expanded with quantitative grid independence results (Table 3), near-wall mesh details, and y+ values.', size=22))
    p.append(para('4. New Section 3.5 added: Numerical validation against experimental data (Table 4).', size=22))
    p.append(para('5. Table 2 added: Flow conditions with explicit Reynolds numbers and regime classification.', size=22))
    p.append(para('6. New Section 4.3 added: Diodicity analysis with quantitative values (Table 5) and power-law correlations.', size=22))
    p.append(para('7. New Section 4.4 added: Flow field analysis and physical mechanism discussion.', size=22))
    p.append(para('8. New Section 4.5 added: Parametric effects of geometric variables (Table 6).', size=22))
    p.append(para('9. Geometry 3 fully analyzed and discussed throughout results.', size=22))
    p.append(para('10. Introduction expanded with new relevant references [33-35] as suggested by Reviewer 4.', size=22))
    p.append(para('11. Citation "[1922]" corrected to "[19-22]".', size=22))
    p.append(para('12. Typo "pas-save" corrected to "passive".', size=22))
    p.append(para('13. Figure captions corrected: (a)/(a) changed to (a)/(b).', size=22))
    p.append(para('14. Terminology unified: "intake velocity" replaced with "inlet velocity" throughout.', size=22))
    p.append(para('15. Complete language revision for grammar and clarity.', size=22))
    p.append(empty())
    
    p.append(para('We are confident that these extensive revisions address all the reviewers\' concerns and significantly strengthen the manuscript. We thank all reviewers for their valuable feedback which has helped improve the quality of this work.', size=22))
    
    return '\n'.join(p)



def create_docx(output_path, body_content):
    """Create a .docx file."""
    
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''
    
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
    
    word_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
    
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
    <w:pPr><w:spacing w:after="60" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
  </w:style>
</w:styles>'''
    
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)
    
    print(f"Created: {output_path}")


if __name__ == '__main__':
    print("Generating Response to Reviewers document...")
    content = get_response_content()
    create_docx('/projects/sandbox/AMMAN/Response_to_Reviewers.docx', content)
    print("Done!")
