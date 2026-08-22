"""
Generate professional DOCX for the book chapter:
"Machine Learning and AI for Smart Antenna and RIS Optimization"

Features:
- Embedded PNG figures (jpg/png format)
- Numbered references [1]-[43] in square brackets
- Formatted tables with styling
- Professional typography
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import re
import os


def set_cell_shading(cell, color):
    """Set background color for a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def add_body_paragraph(doc, text):
    """Add a body paragraph with proper formatting and citation highlighting."""
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(8)
    para.paragraph_format.first_line_indent = Cm(1.27)
    para.paragraph_format.line_spacing = 1.5

    # Split by citation brackets [N] to format them
    parts = re.split(r'(\[\d+\])', text)
    for part in parts:
        if re.match(r'\[\d+\]', part):
            run = para.add_run(part)
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0, 0, 139)  # Dark blue for citations
        else:
            run = para.add_run(part)
            run.font.size = Pt(11)
    return para


def add_figure(doc, image_path, figure_num, caption):
    """Add a figure with embedded image and caption."""
    # Space before figure
    doc.add_paragraph().paragraph_format.space_before = Pt(12)

    # Image paragraph (centered)
    img_para = doc.add_paragraph()
    img_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = img_para.add_run()
    if os.path.exists(image_path):
        run.add_picture(image_path, width=Inches(5.5))
    else:
        run.add_text(f'[Image not found: {image_path}]')
        run.font.color.rgb = RGBColor(255, 0, 0)

    # Caption paragraph
    cap_para = doc.add_paragraph()
    cap_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap_para.paragraph_format.space_after = Pt(12)
    cap_para.paragraph_format.space_before = Pt(6)
    run = cap_para.add_run(f'Figure {figure_num}. ')
    run.bold = True
    run.font.size = Pt(10)
    run = cap_para.add_run(caption)
    run.font.size = Pt(10)


def add_table_to_doc(doc, table_num, caption, headers, rows):
    """Add a formatted table with numbered caption."""
    # Caption above table
    cap_para = doc.add_paragraph()
    cap_para.paragraph_format.space_before = Pt(14)
    cap_para.paragraph_format.space_after = Pt(8)
    run = cap_para.add_run(f'Table {table_num}. ')
    run.bold = True
    run.font.size = Pt(10)
    run = cap_para.add_run(caption)
    run.italic = True
    run.font.size = Pt(10)

    # Create table
    num_cols = len(headers)
    num_rows = len(rows) + 1
    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    # Header row
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        para = cell.paragraphs[0]
        run = para.add_run(header)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, "1B3A5C")

    # Data rows
    for row_idx, row_data in enumerate(rows):
        for col_idx, cell_text in enumerate(row_data):
            cell = table.rows[row_idx + 1].cells[col_idx]
            cell.text = ''
            para = cell.paragraphs[0]
            run = para.add_run(cell_text)
            run.font.size = Pt(8.5)
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if row_idx % 2 == 0:
                set_cell_shading(cell, "EDF2F7")

    # Space after table
    doc.add_paragraph().paragraph_format.space_after = Pt(8)


def create_chapter_docx():
    """Create the complete DOCX document with embedded figures."""

    # Read the markdown source
    with open('Chapter_ML_AI_Smart_Antenna_RIS_Optimization.md', 'r') as f:
        md_content = f.read()

    body_part = md_content.split('## References\n\n')[0]
    refs_part = md_content.split('## References\n\n')[1]

    doc = Document()

    # Configure styles
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)

    # Margins
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    # ==================== TITLE ====================
    title_para = doc.add_paragraph()
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_para.paragraph_format.space_after = Pt(6)
    run = title_para.add_run('Machine Learning and AI for Smart Antenna\nand RIS Optimization')
    run.bold = True
    run.font.size = Pt(18)
    run.font.color.rgb = RGBColor(0, 51, 102)

    # Separator line
    sep = doc.add_paragraph()
    sep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sep.paragraph_format.space_after = Pt(18)
    run = sep.add_run('─' * 60)
    run.font.color.rgb = RGBColor(150, 150, 150)

    # ==================== ABSTRACT ====================
    ah = doc.add_paragraph()
    ah.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ah.paragraph_format.space_after = Pt(8)
    run = ah.add_run('Abstract')
    run.bold = True
    run.font.size = Pt(13)

    abstract_text = (
        "The rapid evolution of wireless communication systems toward sixth-generation (6G) and beyond has "
        "necessitated the development of intelligent, adaptive antenna systems and reconfigurable intelligent "
        "surfaces (RIS) capable of meeting unprecedented demands for data throughput, spectral efficiency, and "
        "energy performance. This chapter presents a comprehensive examination of machine learning (ML) and "
        "artificial intelligence (AI) techniques applied to the optimization of smart antenna systems and RIS "
        "configurations. Beginning with foundational concepts of smart antennas, beamforming, and RIS architectures, "
        "the chapter systematically explores AI-driven design frameworks, data-driven antenna modeling, adaptive "
        "beamforming optimization, terahertz antenna design, RIS phase configuration, deep reinforcement learning "
        "for dynamic RIS control, and joint optimization of communication resources. Emerging applications in 6G "
        "networks, challenges in implementation, and future research directions involving federated learning, "
        "explainable AI, and intelligent metasurfaces are discussed. The integration of AI methodologies into "
        "antenna and RIS design represents a paradigm shift from conventional optimization approaches, enabling "
        "real-time adaptation, enhanced network performance, and intelligent wireless environments for "
        "next-generation communication systems."
    )
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(8)
    para.paragraph_format.line_spacing = 1.5
    run = para.add_run(abstract_text)
    run.font.size = Pt(11)

    # Keywords
    kw_para = doc.add_paragraph()
    kw_para.paragraph_format.space_after = Pt(20)
    run = kw_para.add_run('Keywords: ')
    run.bold = True
    run.font.size = Pt(11)
    run = kw_para.add_run(
        'Smart antennas, reconfigurable intelligent surfaces, machine learning, deep learning, '
        'beamforming, 6G communications, reinforcement learning, terahertz antennas, phase optimization, '
        'intelligent wireless environments'
    )
    run.font.size = Pt(11)
    run.italic = True

    # ==================== PROCESS BODY ====================
    # Parse the markdown content into paragraphs
    paragraphs = body_part.split('\n\n')

    # Figure details
    figure_files = {
        1: ('chapter_figures/Figure_1_RIS_Architecture.png',
            'Architecture of a RIS-assisted smart antenna communication system showing the base station '
            'with adaptive antenna array, RIS panel with configurable reflecting elements, and multiple '
            'user equipment in a multi-path propagation environment.'),
        2: ('chapter_figures/Figure_2_Beamforming_Architecture.png',
            'AI-based adaptive beamforming architecture showing input channel measurements, neural network '
            'processing pipeline (feature extraction CNN, temporal modeling LSTM, beam weight prediction '
            'fully-connected layers), and output beamforming weight vectors applied to the antenna array elements.'),
        3: ('chapter_figures/Figure_3_RIS_ML_Framework.png',
            'Machine learning framework for RIS phase optimization showing the complete pipeline: '
            '(a) channel measurement acquisition, (b) feature extraction and preprocessing, (c) deep neural '
            'network prediction of optimal phase configurations, (d) RIS controller implementing predicted '
            'phase shifts, and (e) feedback loop for online model refinement.'),
        4: ('chapter_figures/Figure_4_6G_Applications.png',
            'Application scenarios for AI-driven RIS-assisted THz networks in 6G environments: '
            '(a) indoor high-speed communications, (b) smart factory with distributed RIS, '
            '(c) vehicular network with roadside RIS, and (d) aerial network with UAV-mounted RIS.'),
    }

    # Table data
    table_data = {
        1: ('Machine Learning Categories and Applications in Smart Antenna and RIS Optimization',
            ['ML Category', 'Key Algorithms', 'Antenna Applications', 'RIS Applications'],
            [
                ['Supervised Learning', 'Neural Networks, SVM,\nRandom Forest, GP',
                 'Parameter prediction,\nradiation pattern modeling,\nimpedance matching',
                 'Phase shift prediction,\nchannel estimation,\nbeam direction classification'],
                ['Unsupervised Learning', 'K-means, PCA,\nAutoencoders, DBSCAN',
                 'Design space exploration,\nchannel clustering,\nfeature extraction',
                 'RIS element grouping,\nenvironmental classification,\nanomaly detection'],
                ['Reinforcement Learning', 'Q-learning, DQN,\nPPO, A3C',
                 'Adaptive beamforming,\nbeam tracking,\npower control',
                 'Dynamic phase configuration,\nuser association,\nresource allocation'],
                ['Deep Learning', 'CNN, RNN, GAN,\nTransformer',
                 'Near-field pattern prediction,\narray synthesis,\nmutual coupling compensation',
                 'Large-scale RIS optimization,\nchannel prediction,\ngenerative channel modeling'],
            ]),
        2: ('Comparison of Machine Learning Techniques for Antenna Performance Prediction',
            ['ML Technique', 'Prediction\nAccuracy', 'Training Data\nRequired', 'Inference\nCost',
             'High-Dim\nHandling', 'Uncertainty\nQuantification'],
            [
                ['Artificial Neural Networks', 'High (RMSE<2%)', 'Moderate\n(500–5000)', 'Very Low (ms)', 'Excellent', 'Limited'],
                ['Gaussian Process Regression', 'Very High (RMSE<1%)', 'Low\n(100–500)', 'Moderate (N³)', 'Poor', 'Excellent'],
                ['Support Vector Regression', 'High (RMSE<3%)', 'Moderate\n(200–2000)', 'Low (ms)', 'Good', 'Limited'],
                ['Random Forest', 'Moderate (RMSE<5%)', 'Low\n(100–1000)', 'Low (ms)', 'Good', 'Moderate'],
                ['Deep Learning (CNN/DNN)', 'Very High (RMSE<1%)', 'High\n(5000–50000)', 'Very Low (ms)', 'Excellent', 'Limited'],
            ]),
        3: ('Comparative Analysis of Deep Reinforcement Learning Algorithms for Dynamic RIS Control',
            ['DRL Algorithm', 'Action Space', 'Scalability\n(Elements)', 'Convergence\nSpeed',
             'Sample\nEfficiency', 'Performance\nvs. Optimal'],
            [
                ['DQN', 'Discrete', 'Limited (<64)', 'Moderate', 'Low', '90–95%'],
                ['Double DQN', 'Discrete', 'Limited (<64)', 'Moderate', 'Moderate', '92–96%'],
                ['PPO', 'Cont./Discrete', 'Good (<256)', 'Fast', 'Moderate', '93–97%'],
                ['A3C', 'Cont./Discrete', 'Good (<256)', 'Fast', 'Moderate', '92–96%'],
                ['SAC', 'Continuous', 'Excellent (<1024)', 'Moderate', 'High', '95–98%'],
                ['Multi-Agent DRL', 'Cont./Discrete', 'Excellent (>1024)', 'Slow', 'Low', '90–95%'],
            ]),
        4: ('Key Challenges and Mitigation Approaches in AI-Based Antenna and RIS Optimization',
            ['Challenge', 'Performance\nImpact', 'Mitigation\nApproaches', 'Effectiveness',
             'Open Research\nGaps'],
            [
                ['Channel Estimation\nErrors', '15–40%\nthroughput loss', 'Robust optimization,\nBayesian methods',
                 'Moderate\n(60–75% recovery)', 'Ultra-fast estimation\nfor mobile scenarios'],
                ['Computational\nComplexity', 'Real-time\nconstraints violated', 'Model compression,\nedge computing',
                 'Good\n(10× speedup, <5% loss)', 'Sub-ms inference\nfor THz systems'],
                ['Training Data\nScarcity', 'Suboptimal\ngeneralization', 'Transfer learning,\ndata augmentation',
                 'Moderate\n(70–85% performance)', 'Zero-shot\ngeneralization'],
                ['Hardware\nImpairments', '5–20%\nperformance loss', 'Hardware-aware\ntraining, calibration',
                 'Good\n(80–90% of ideal)', 'Joint HW-algorithm\nco-design'],
                ['Energy\nConsumption', 'Sustainability\nconcerns', 'Green AI,\nsleep modes',
                 'Limited\n(30–50% reduction)', 'Near-zero energy\nRIS optimization'],
                ['Model\nGeneralization', 'Performance collapse\nin new scenarios', 'Meta-learning,\nensemble methods',
                 'Moderate\n(75–85% cross-domain)', 'Lifelong learning\nfor evolving networks'],
            ]),
    }

    table_inserted = {1: False, 2: False, 3: False, 4: False}
    figure_inserted = {1: False, 2: False, 3: False, 4: False}

    for para_text in paragraphs:
        para_text = para_text.strip()
        if not para_text:
            continue

        # Skip already handled
        if para_text.startswith('# Machine Learning') or para_text.startswith('## Abstract'):
            continue
        if 'The rapid evolution of wireless' in para_text and 'Abstract' not in para_text:
            continue
        if para_text.startswith('**Keywords:'):
            continue
        if para_text == '---':
            continue

        # Section headings
        if para_text.startswith('## Section 1:'):
            doc.add_page_break()
            h = doc.add_heading(para_text[3:], level=1)
            for run in h.runs:
                run.font.color.rgb = RGBColor(0, 51, 102)
            continue
        if para_text.startswith('## Section 2:'):
            doc.add_page_break()
            h = doc.add_heading(para_text[3:], level=1)
            for run in h.runs:
                run.font.color.rgb = RGBColor(0, 51, 102)
            continue
        if para_text.startswith('## Section 3:'):
            doc.add_page_break()
            h = doc.add_heading(para_text[3:], level=1)
            for run in h.runs:
                run.font.color.rgb = RGBColor(0, 51, 102)
            continue
        if para_text.startswith('## Section 4:'):
            doc.add_page_break()
            h = doc.add_heading(para_text[3:], level=1)
            for run in h.runs:
                run.font.color.rgb = RGBColor(0, 51, 102)
            continue
        if para_text.startswith('## Conclusion'):
            doc.add_page_break()
            h = doc.add_heading('Conclusion', level=1)
            for run in h.runs:
                run.font.color.rgb = RGBColor(0, 51, 102)
            continue

        # Subsection headings
        if para_text.startswith('### '):
            doc.add_heading(para_text[4:], level=2)
            continue

        # Figure placeholders - insert actual images
        if para_text.startswith('**[Figure'):
            fig_match = re.match(r'\*\*\[Figure (\d+):', para_text)
            if fig_match:
                fig_num = int(fig_match.group(1))
                if fig_num in figure_files and not figure_inserted[fig_num]:
                    img_path, caption = figure_files[fig_num]
                    add_figure(doc, img_path, fig_num, caption)
                    figure_inserted[fig_num] = True
            continue

        # Table placeholders - insert formatted tables
        if para_text.startswith('**[Table'):
            continue

        # Markdown table headers trigger table insertion
        if para_text.startswith('| ML Category') and not table_inserted[1]:
            cap, headers, rows = table_data[1]
            add_table_to_doc(doc, 1, cap, headers, rows)
            table_inserted[1] = True
            continue
        if para_text.startswith('| ML Technique') and not table_inserted[2]:
            cap, headers, rows = table_data[2]
            add_table_to_doc(doc, 2, cap, headers, rows)
            table_inserted[2] = True
            continue
        if para_text.startswith('| DRL Algorithm') and not table_inserted[3]:
            cap, headers, rows = table_data[3]
            add_table_to_doc(doc, 3, cap, headers, rows)
            table_inserted[3] = True
            continue
        if para_text.startswith('| Challenge') and not table_inserted[4]:
            cap, headers, rows = table_data[4]
            add_table_to_doc(doc, 4, cap, headers, rows)
            table_inserted[4] = True
            continue

        # Skip remaining markdown table rows
        if para_text.startswith('|'):
            continue

        # Regular body paragraphs
        if len(para_text) > 50 and not para_text.startswith('#'):
            clean_text = para_text.replace('**', '').replace('*', '')
            add_body_paragraph(doc, clean_text)

    # ==================== REFERENCES ====================
    doc.add_page_break()
    h = doc.add_heading('References', level=1)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0, 51, 102)

    ref_entries = [r.strip() for r in refs_part.strip().split('\n\n') if r.strip()]
    for ref in ref_entries:
        clean_ref = ref.replace('*', '')
        para = doc.add_paragraph()
        para.paragraph_format.left_indent = Cm(1.0)
        para.paragraph_format.first_line_indent = Cm(-1.0)
        para.paragraph_format.space_after = Pt(4)
        para.paragraph_format.line_spacing = 1.15

        # Format the [N] number in bold
        num_match = re.match(r'(\[\d+\])\s*(.*)', clean_ref)
        if num_match:
            run = para.add_run(num_match.group(1) + ' ')
            run.bold = True
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(0, 0, 139)
            run = para.add_run(num_match.group(2))
            run.font.size = Pt(10)
        else:
            run = para.add_run(clean_ref)
            run.font.size = Pt(10)

    # Save
    output_path = 'Chapter_ML_AI_Smart_Antenna_RIS_Optimization.docx'
    doc.save(output_path)
    return output_path, doc


if __name__ == '__main__':
    output_path, doc = create_chapter_docx()
    print(f"✅ Document saved: {output_path}")
    print(f"   File size: {os.path.getsize(output_path)/1024:.1f} KB")

    # Verification
    print("\n📋 VERIFICATION:")
    print(f"   Tables: {len(doc.tables)}")

    # Count embedded images
    img_count = 0
    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            img_count += 1
    print(f"   Embedded images: {img_count}")

    # Count references
    in_refs = False
    ref_count = 0
    for p in doc.paragraphs:
        if p.text.strip() == 'References':
            in_refs = True
            continue
        if in_refs and p.text.strip() and p.text.strip().startswith('['):
            ref_count += 1
    print(f"   References: {ref_count}")

    # Verify citations in body
    citation_nums = set()
    in_refs = False
    for p in doc.paragraphs:
        if p.text.strip() == 'References':
            break
        for m in re.finditer(r'\[(\d+)\]', p.text):
            citation_nums.add(int(m.group(1)))
    print(f"   Unique citations in text: {len(citation_nums)}")
    print(f"   Citation range: [{min(citation_nums)}] to [{max(citation_nums)}]")

    # Check no refs in intro (Section 1.1) or conclusion
    in_intro = False
    in_conclusion = False
    intro_cites = []
    concl_cites = []
    for p in doc.paragraphs:
        if '1.1 Smart Antenna Systems' in p.text:
            in_intro = True
            continue
        if '1.2 Machine Learning' in p.text:
            in_intro = False
        if p.text.strip() == 'Conclusion':
            in_conclusion = True
            continue
        if p.text.strip() == 'References':
            in_conclusion = False

        if in_intro:
            cites = re.findall(r'\[\d+\]', p.text)
            intro_cites.extend(cites)
        if in_conclusion:
            cites = re.findall(r'\[\d+\]', p.text)
            concl_cites.extend(cites)

    print(f"   Refs in Section 1.1 (intro): {len(intro_cites)} {'✓' if len(intro_cites)==0 else '✗'}")
    print(f"   Refs in Conclusion: {len(concl_cites)} {'✓' if len(concl_cites)==0 else '✗'}")
