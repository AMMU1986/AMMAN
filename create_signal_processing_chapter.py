"""
Create a comprehensive Word document (.docx) for the book chapter:
"Signal Processing for Condition Monitoring"
Book: Predictive Maintenance of Mechanical Systems: Synergy of Vibration and Artificial Intelligence

Uses raw XML/ZIP approach to create .docx without python-docx library.
Includes 4 tables, 4 figures (PNG), and 47 references.
Target: ~8300 words
"""

import zipfile
import os
import base64
import struct

# ============================================================
# DOCX BUILDING UTILITIES (Pure XML/ZIP approach)
# ============================================================

def create_docx(paragraphs, tables, images, filename):
    """Create a .docx file from structured content."""
    
    # Build relationships for images
    image_rels = ""
    image_counter = 1
    image_rel_ids = {}
    for img_id, img_path in images.items():
        rel_id = f"rId{10 + image_counter}"
        image_rels += f'<Relationship Id="{rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{os.path.basename(img_path)}"/>'
        image_rel_ids[img_id] = rel_id
        image_counter += 1
    
    # Content Types
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Default Extension="jpeg" ContentType="image/jpeg"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''
    
    # Relationships
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
    
    # Word relationships
    word_rels = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
  {image_rels}
</Relationships>'''
    
    # Styles
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="200" w:line="276" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:pPr><w:spacing w:after="300"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="360" w:after="200"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:i/><w:sz w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="Caption"/>
    <w:pPr><w:spacing w:after="200"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:i/><w:sz w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>
</w:styles>'''
    
    # Numbering
    numbering = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
</w:numbering>'''
    
    # Build document body
    body_content = build_document_body(paragraphs, tables, image_rel_ids)
    
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    
    # Create ZIP
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', document)
        zf.writestr('word/styles.xml', styles)
        zf.writestr('word/numbering.xml', numbering)
        
        # Add images
        for img_id, img_path in images.items():
            if os.path.exists(img_path):
                zf.write(img_path, f'word/media/{os.path.basename(img_path)}')
    
    print(f"Document created: {filename}")

def escape_xml(text):
    """Escape XML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def make_paragraph(text, style="Normal", bold=False, italic=False, center=False):
    """Create a paragraph XML element."""
    ppr = ""
    if style != "Normal":
        ppr += f'<w:pStyle w:val="{style}"/>'
    if center:
        ppr += '<w:jc w:val="center"/>'
    
    rpr = ""
    if bold:
        rpr += "<w:b/>"
    if italic:
        rpr += "<w:i/>"
    
    ppr_xml = f"<w:pPr>{ppr}</w:pPr>" if ppr else ""
    rpr_xml = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    
    return f'<w:p>{ppr_xml}<w:r>{rpr_xml}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r></w:p>'

def make_image_paragraph(rel_id, width_emu=5400000, height_emu=3400000, caption=""):
    """Create a paragraph with an inline image."""
    img_xml = f'''<w:p>
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{width_emu}" cy="{height_emu}"/>
        <wp:docPr id="1" name="Picture"/>
        <a:graphic>
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic>
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="Picture"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rel_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="{width_emu}" cy="{height_emu}"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>'''
    
    if caption:
        img_xml += make_paragraph(caption, style="Caption", italic=True, center=True)
    
    return img_xml

def make_table(headers, rows, caption=""):
    """Create a table XML element."""
    table_xml = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9000" w:type="dxa"/><w:jc w:val="center"/></w:tblPr>'
    
    # Header row
    table_xml += '<w:tr>'
    for h in headers:
        table_xml += f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{escape_xml(h)}</w:t></w:r></w:p></w:tc>'
    table_xml += '</w:tr>'
    
    # Data rows
    for row in rows:
        table_xml += '<w:tr>'
        for cell in row:
            table_xml += f'<w:tc><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{escape_xml(str(cell))}</w:t></w:r></w:p></w:tc>'
        table_xml += '</w:tr>'
    
    table_xml += '</w:tbl>'
    
    if caption:
        table_xml = make_paragraph(caption, style="Caption", italic=True, center=True) + table_xml
    
    return table_xml

def build_document_body(content_list, tables_dict, image_rel_ids):
    """Build the full document body from content elements."""
    body = ""
    for item in content_list:
        if item[0] == 'para':
            body += make_paragraph(item[1], style=item[2] if len(item) > 2 else "Normal",
                                   bold=item[3] if len(item) > 3 else False)
        elif item[0] == 'heading1':
            body += make_paragraph(item[1], style="Heading1", bold=True)
        elif item[0] == 'heading2':
            body += make_paragraph(item[1], style="Heading2", bold=True)
        elif item[0] == 'heading3':
            body += make_paragraph(item[1], style="Heading3", bold=True)
        elif item[0] == 'title':
            body += make_paragraph(item[1], style="Title", bold=True)
        elif item[0] == 'image':
            img_id = item[1]
            caption = item[2] if len(item) > 2 else ""
            if img_id in image_rel_ids:
                body += make_image_paragraph(image_rel_ids[img_id], caption=caption)
        elif item[0] == 'table':
            table_key = item[1]
            caption = item[2] if len(item) > 2 else ""
            if table_key in tables_dict:
                headers, rows = tables_dict[table_key]
                body += make_table(headers, rows, caption)
    return body

# ============================================================
# CHAPTER CONTENT
# ============================================================

def get_chapter_content():
    """Return the full chapter content as a structured list."""
    
    content = []
    
    # Title
    content.append(('title', 'Signal Processing for Condition Monitoring'))
    content.append(('para', 'Book: Predictive Maintenance of Mechanical Systems: Synergy of Vibration and Artificial Intelligence', 'Normal', True))
    content.append(('para', ''))
    
    # Abstract
    content.append(('heading1', 'Abstract'))
    content.append(('para', 
        'This chapter presents a comprehensive treatment of signal processing techniques for condition monitoring '
        'of mechanical systems, with emphasis on vibration-based approaches integrated with artificial intelligence. '
        'The chapter begins with the fundamentals of vibration signal acquisition and time-domain analysis, progresses '
        'through frequency-domain and time-frequency methods, and culminates with advanced machine learning and deep '
        'learning architectures for automated fault diagnosis and prognosis. Signal processing forms the critical '
        'bridge between raw sensor data and actionable maintenance intelligence, transforming complex multi-dimensional '
        'sensor measurements into compact, interpretable representations suitable for both human expert analysis and '
        'automated decision systems. The synergy between classical signal processing and modern AI enables unprecedented '
        'accuracy in detecting incipient faults, classifying degradation modes, and predicting remaining useful life '
        'across diverse machinery types and operating conditions. Real-time implementation strategies including edge '
        'computing, Industrial IoT integration, and cloud-based analytics are discussed alongside practical challenges '
        'such as variable operating conditions, data imbalance, and sensor degradation that constrain deployment in '
        'industrial environments. Future directions including self-supervised learning, foundation models, digital twins, '
        'and explainable AI for predictive maintenance are explored as pathways toward fully autonomous maintenance '
        'systems. The chapter provides researchers and practitioners with a unified framework for understanding '
        'the complete signal processing pipeline from sensor to maintenance decision, bridging the gap between '
        'theoretical developments in signal processing and AI with practical industrial implementation requirements.'))
    content.append(('para', ''))
    content.append(('para', 'Keywords: Signal processing, condition monitoring, vibration analysis, predictive maintenance, machine learning, deep learning, fault diagnosis, time-frequency analysis, wavelet transform, remaining useful life, edge computing, digital twin'))
    content.append(('para', ''))
    
    # ============================================================
    # SECTION 1
    # ============================================================
    content.append(('heading1', '1. Fundamentals of Signal Processing for Condition Monitoring'))
    
    # 1.1
    content.append(('heading2', '1.1 Condition Monitoring and Vibration Signal Acquisition'))
    
    content.append(('para',
        'Condition monitoring represents the systematic process of observing and recording parameters indicative '
        'of mechanical system health, enabling the transition from reactive to predictive maintenance strategies [1]. '
        'The fundamental premise underlying vibration-based condition monitoring is that all rotating and reciprocating '
        'machinery generates characteristic vibration signatures that change measurably as faults develop and progress [2]. '
        'These changes manifest as alterations in amplitude, frequency content, phase relationships, and statistical '
        'properties of the vibration signal, providing rich diagnostic information when properly processed and interpreted. '
        'The economic justification for condition monitoring is compelling: unplanned downtime in manufacturing '
        'facilities costs an estimated $50 billion annually in the United States alone, while predictive maintenance '
        'strategies enabled by effective condition monitoring can reduce maintenance costs by 25-30% and eliminate '
        '70-75% of equipment breakdowns according to industry surveys.'))
    
    content.append(('para',
        'The condition monitoring process encompasses four fundamental stages: data acquisition from sensors mounted '
        'on critical machinery components, signal processing to extract meaningful information from raw measurements, '
        'condition assessment through comparison with baseline signatures and fault patterns, and maintenance decision '
        'support that translates diagnostic and prognostic information into actionable maintenance recommendations [3]. '
        'Vibration analysis remains the predominant condition monitoring technology for rotating machinery due to its '
        'sensitivity to a wide range of mechanical faults, non-invasive measurement capability, and well-established '
        'theoretical foundation linking vibration characteristics to specific fault mechanisms. Complementary '
        'technologies including oil analysis, thermography, ultrasonics, and motor current signature analysis '
        'provide additional diagnostic dimensions for comprehensive machine health assessment.'))
    
    content.append(('para',
        'Vibration sensors constitute the primary transduction elements in condition monitoring systems. Piezoelectric '
        'accelerometers remain the dominant sensor technology due to their broad frequency range (typically 0.5 Hz to '
        '20 kHz), excellent linearity, wide dynamic range (exceeding 120 dB), and robust construction suitable for '
        'industrial environments [4]. These sensors exploit the piezoelectric effect in crystalline materials such as '
        'lead zirconate titanate (PZT) or quartz to convert mechanical acceleration into proportional electrical charge. '
        'Industrial-grade accelerometers are available in various configurations including side-mounted, top-mounted, '
        'and triaxial designs, with sensitivity ranges from 1 mV/g for high-frequency applications to 1000 mV/g for '
        'low-frequency structural monitoring [5]. Proximity probes based on eddy current principles are preferred for '
        'shaft-relative measurements in fluid-film bearing machines, providing displacement information at frequencies '
        'from DC to approximately 10 kHz. Velocity sensors, acoustic emission transducers, and laser vibrometers '
        'complement the measurement toolkit for specific applications requiring alternative sensing modalities [6].'))
    
    content.append(('para',
        'The data acquisition system represents the critical interface between analog sensor signals and digital '
        'processing algorithms. Proper sampling requires adherence to the Nyquist-Shannon sampling theorem, which '
        'mandates a sampling rate at least twice the highest frequency of interest to prevent aliasing [7]. In practice, '
        'oversampling ratios of 2.5 to 4 times the maximum frequency are employed to accommodate anti-aliasing filter '
        'roll-off characteristics and ensure adequate amplitude accuracy for spectral components near the Nyquist '
        'frequency. Modern data acquisition systems typically provide 24-bit resolution with sampling '
        'rates exceeding 100 kHz per channel, enabling capture of both low-frequency structural modes and high-frequency '
        'bearing defect signatures within a single measurement [8]. Signal conditioning including charge amplification, '
        'anti-aliasing filtering, impedance matching, and integration (for converting acceleration to velocity or '
        'displacement) ensures signal integrity throughout the acquisition chain. Trigger synchronization with '
        'tachometer signals enables order-domain analysis essential for variable-speed machinery. '
        'The quality of acquired signals directly determines the effectiveness of all subsequent processing stages, '
        'as illustrated in the comprehensive signal processing framework shown in Figure 1, which depicts the complete '
        'pipeline from physical measurement through intelligent analytics to maintenance optimization.'))
    
    # Figure 1 - first citation
    content.append(('image', 'fig1', 'Figure 1. Vibration signal processing framework for condition monitoring showing the complete pipeline from sensor acquisition through signal processing to AI-based analytics and maintenance decision support.'))
    content.append(('para', ''))
    
    # 1.2
    content.append(('heading2', '1.2 Time-Domain Signal Processing'))
    
    content.append(('para',
        'Time-domain signal processing provides the most direct and computationally efficient approach to vibration '
        'analysis, extracting statistical and waveform-based features that characterize the overall condition of '
        'monitored equipment [9]. The root mean square (RMS) value represents the most fundamental time-domain '
        'indicator, quantifying the overall vibration energy and serving as the primary trending parameter in most '
        'condition monitoring programs. RMS is mathematically defined as the square root of the mean of squared '
        'instantaneous amplitudes over the measurement duration, providing a single scalar value proportional to '
        'signal power regardless of frequency content or waveform shape. ISO 10816 and ISO 20816 standards define '
        'vibration severity zones based on RMS velocity levels, establishing industry-accepted thresholds for '
        'machine condition assessment across different machine classifications [10].'))
    
    content.append(('para',
        'Beyond RMS, a comprehensive suite of statistical features extracts complementary information from vibration '
        'waveforms that captures different aspects of signal character and fault development. The peak value and '
        'peak-to-peak amplitude indicate maximum excursion levels sensitive to impulsive events such as bearing '
        'defect impacts or gear tooth failures. The crest factor, defined as the ratio of peak value to RMS, '
        'quantifies signal peakedness and proves particularly effective for detecting early-stage bearing defects '
        'that generate transient impacts superimposed on otherwise smooth background vibration [11]. A crest factor '
        'significantly above 3.0 (the value for a sinusoidal signal) indicates the presence of impulsive content '
        'warranting further investigation. Kurtosis measures the tailedness of the amplitude distribution, with '
        'values exceeding 3.0 (the Gaussian reference value) indicating the presence of impulsive content '
        'characteristic of localized surface damage [12]. Skewness captures asymmetry in the vibration distribution, '
        'providing sensitivity to unidirectional impacts and shaft bow conditions. Additional statistical moments '
        'and derived features including the shape factor, margin factor, and impulse factor complete the standard '
        'feature set employed in industrial practice. Table 1 summarizes the principal time-domain features and '
        'their diagnostic significance for common mechanical fault types.'))
    
    # Table 1
    content.append(('table', 'table1', 'Table 1. Time-domain statistical features for vibration-based condition monitoring and their diagnostic significance for common mechanical faults.'))
    content.append(('para', ''))
    
    content.append(('para',
        'Time-domain indicators exhibit different sensitivities across fault development stages, necessitating '
        'careful selection of monitoring parameters for each application. During incipient fault development, '
        'kurtosis and crest factor show the earliest response as isolated impulses emerge from the background '
        'vibration floor [13]. These indicators can detect bearing surface damage at stages when overall vibration '
        'levels remain within normal limits, providing critical early warning capability. As damage progresses and '
        'multiple defect sites develop, RMS levels increase monotonically while kurtosis may actually decrease as '
        'overlapping impact responses cause the amplitude distribution to approach Gaussian [14]. This non-monotonic '
        'behavior of certain indicators necessitates the use of multiple complementary features for robust condition '
        'assessment across all fault severity levels. Advanced time-domain techniques including synchronous time '
        'averaging for isolating individual gear vibration components, order tracking for analyzing variable-speed '
        'machinery, and time-series autoregressive modeling for parametric signal representation extend the diagnostic '
        'capability substantially beyond simple statistical features [15]. The autoregressive model coefficients '
        'themselves serve as compact feature vectors sensitive to changes in system dynamics associated with developing '
        'faults, while residual signal analysis from adaptive models provides enhanced sensitivity to subtle changes.'))
    
    # 1.3
    content.append(('heading2', '1.3 Frequency-Domain and Spectral Analysis'))
    
    content.append(('para',
        'Frequency-domain analysis through the Discrete Fourier Transform (DFT) and its computationally efficient '
        'implementation, the Fast Fourier Transform (FFT), constitutes the cornerstone of vibration-based condition '
        'monitoring [16]. The transformation from time to frequency domain decomposes the composite vibration signal '
        'into constituent sinusoidal components, enabling identification of specific vibration sources through their '
        'characteristic frequencies. Each mechanical component generates vibration at frequencies determined by its '
        'geometry, rotational speed, and operating conditions, creating a unique spectral fingerprint that enables '
        'source-specific diagnosis. The FFT algorithm, first described by Cooley and Tukey in 1965, reduces '
        'computational complexity from O(N^2) for direct DFT computation to O(N log N), making real-time spectral '
        'analysis feasible even with limited computational resources [17]. This efficiency gain enables practical '
        'implementation of continuous spectral monitoring in industrial settings where thousands of measurement '
        'points require regular assessment.'))
    
    content.append(('para',
        'The power spectral density (PSD) quantifies vibration energy distribution across frequency, providing a '
        'statistically robust representation that reduces variance through averaging of multiple spectral estimates. '
        'Welch\'s method, employing overlapped segmented periodograms with windowing functions (Hanning, Hamming, '
        'or flat-top), represents the standard approach for PSD estimation in condition monitoring applications [18]. '
        'The choice of window function involves trade-offs between frequency resolution (main lobe width) and spectral '
        'leakage suppression (side lobe levels), with Hanning windows providing a practical compromise for general '
        'machinery vibration analysis. Spectral resolution, determined by the ratio of sampling rate to transform '
        'length (delta_f = fs/N), must be sufficient to resolve closely-spaced frequency components such as bearing '
        'defect frequencies and their amplitude-modulation sidebands, typically requiring frequency resolution below '
        '1 Hz for detailed bearing analysis. Zero-padding extends the apparent frequency resolution for display '
        'purposes but does not improve the fundamental resolving capability determined by the observation duration.'))
    
    content.append(('para',
        'Identification of characteristic fault frequencies forms the basis of frequency-domain diagnosis and '
        'represents the most widely practiced approach to vibration-based fault identification in industry [19]. '
        'Rolling element bearing defects generate well-defined frequencies determined by bearing geometry '
        '(pitch diameter, ball diameter, contact angle, number of rolling elements) and shaft speed: the ball pass '
        'frequency outer race (BPFO), ball pass frequency inner race (BPFI), ball spin frequency (BSF), and '
        'fundamental train frequency (FTF). These frequencies, calculable from manufacturer specifications, enable '
        'precise identification of which bearing component has developed a defect [20]. Gear mesh frequency and its '
        'harmonics, modulated by shaft rotation frequencies appearing as sidebands, indicate gear tooth defects with '
        'sideband patterns revealing distributed versus localized damage. Shaft-related faults including imbalance '
        '(dominant at 1x running speed), misalignment (elevated 2x and 3x components), mechanical looseness '
        '(multiple harmonics and sub-harmonics), and blade pass frequencies in pumps and fans are directly '
        'identifiable in the frequency spectrum. The comprehensive spectral analysis framework enables systematic '
        'fault identification when combined with machine-specific frequency databases, as previously illustrated '
        'in the signal processing pipeline of Figure 1 which shows how frequency-domain analysis integrates within '
        'the broader condition monitoring workflow.'))
    
    content.append(('para', ''))
    
    # ============================================================
    # SECTION 2
    # ============================================================
    content.append(('heading1', '2. Advanced Signal Processing Techniques for Fault Diagnosis'))
    
    # 2.1
    content.append(('heading2', '2.1 Time-Frequency Analysis'))
    
    content.append(('para',
        'Mechanical fault signatures are inherently non-stationary, exhibiting time-varying frequency content that '
        'cannot be fully characterized by either time-domain or frequency-domain analysis alone [21]. Time-frequency '
        'analysis methods address this limitation by providing simultaneous representation of signal energy in both '
        'time and frequency dimensions, revealing transient events, frequency modulations, and evolving spectral '
        'patterns associated with developing faults. The non-stationarity arises from multiple sources: speed '
        'fluctuations that modulate fault frequencies, amplitude modulation of bearing defect signatures as rolling '
        'elements enter and exit the load zone, transient impacts from gear tooth damage, and progressive changes '
        'in system dynamics as degradation advances. The three principal time-frequency methods employed in condition '
        'monitoring are the Short-Time Fourier Transform (STFT), wavelet-based transforms, and empirical mode '
        'decomposition, each offering distinct advantages and limitations as depicted in Figure 2 which provides '
        'a comparative visualization of their resolution characteristics and decomposition approaches.'))
    
    # Figure 2 - first citation
    content.append(('image', 'fig2', 'Figure 2. Comparison of time-frequency analysis methods: STFT spectrogram with uniform time-frequency resolution (left), wavelet scalogram with multi-resolution capability (right), and empirical mode decomposition showing adaptive signal separation (bottom).'))
    content.append(('para', ''))
    
    content.append(('para',
        'The Short-Time Fourier Transform applies the FFT to successive windowed segments of the signal, producing '
        'a spectrogram that maps spectral content evolution over time [22]. By sliding a finite-length analysis window '
        'along the signal and computing the Fourier Transform at each position, STFT provides a two-dimensional '
        'representation revealing how frequency content changes temporally. The fundamental limitation of STFT lies '
        'in the Heisenberg-Gabor uncertainty principle: time resolution and frequency resolution cannot be simultaneously '
        'optimized, as their product is bounded below by a constant (delta_t * delta_f >= 1/4pi). A narrow analysis '
        'window provides good time localization for detecting transient events but poor frequency resolution for '
        'resolving closely-spaced spectral components, while a wide window offers the converse [23]. This fixed trade-off '
        'limits STFT effectiveness for signals containing both high-frequency transients requiring fine temporal '
        'resolution and low-frequency modulations requiring fine spectral resolution. Despite this limitation, '
        'STFT spectrograms remain widely used in industrial practice due to their intuitive interpretation, '
        'computational simplicity, and direct relationship to physical signal characteristics.'))
    
    content.append(('para',
        'The Wavelet Transform overcomes the fixed-resolution limitation of STFT through multi-resolution analysis, '
        'employing dilated and translated versions of a mother wavelet function to achieve frequency-dependent '
        'time-frequency resolution [24]. At high frequencies (small wavelet scales), narrow wavelet dilation provides '
        'excellent time localization for detecting transient impulses from bearing defects and gear tooth impacts. '
        'At low frequencies (large wavelet scales), broad wavelet dilation provides superior frequency resolution '
        'for characterizing shaft-related faults and structural resonances. This automatic adaptation of resolution '
        'to frequency content makes wavelet analysis ideally suited for vibration signals containing both impulsive '
        'and tonal components simultaneously. The Continuous Wavelet Transform (CWT) provides a redundant but '
        'highly detailed representation across all scales and translations, while the Discrete Wavelet Transform '
        '(DWT) offers computationally efficient multi-resolution decomposition through quadrature mirror filter '
        'banks [25]. The Wavelet Packet Transform (WPT) extends DWT by decomposing both approximation and detail '
        'coefficients at each level, providing uniform frequency bandwidth decomposition suitable for extracting '
        'features from specific frequency bands of diagnostic interest. Choice of mother wavelet (Daubechies, '
        'Morlet, Symlet, or Meyer) significantly influences decomposition quality for specific fault types [26].'))
    
    content.append(('para',
        'Empirical Mode Decomposition (EMD) provides a fully data-adaptive approach to signal decomposition, '
        'separating complex signals into a finite set of Intrinsic Mode Functions (IMFs) through an iterative '
        'sifting process based on local extrema identification and envelope interpolation [27]. Each IMF satisfies '
        'conditions of having equal numbers of extrema and zero crossings, with symmetric upper and lower envelopes '
        'defined by cubic spline interpolation through local maxima and minima respectively. The subsequent application '
        'of the Hilbert Transform to each IMF yields instantaneous frequency and amplitude at each time instant, '
        'comprising the Hilbert-Huang Transform (HHT) which provides a complete time-frequency-energy representation. '
        'This method excels for analyzing non-linear and non-stationary vibration signals where predefined basis '
        'functions prove inadequate, as it imposes no assumptions about signal linearity or stationarity [28]. '
        'Ensemble EMD (EEMD) and its successor Complete EEMD with Adaptive Noise (CEEMDAN) address mode mixing '
        'limitations of the original EMD algorithm through noise-assisted decomposition, adding white noise '
        'ensembles to separate signal components that would otherwise be erroneously merged into single IMFs. '
        'The comparative characteristics of these time-frequency methods, as illustrated in Figure 2, guide '
        'appropriate method selection for specific diagnostic applications. Table 2 provides a detailed quantitative '
        'comparison of these approaches.'))
    
    # Table 2
    content.append(('table', 'table2', 'Table 2. Comparative analysis of time-frequency methods for vibration-based condition monitoring, highlighting resolution characteristics, computational requirements, and application domains.'))
    content.append(('para', ''))
    
    # 2.2
    content.append(('heading2', '2.2 Signal Decomposition and Noise Reduction'))
    
    content.append(('para',
        'Industrial vibration signals invariably contain noise from multiple sources including electronic noise in '
        'measurement chains (thermal noise, quantization noise, electromagnetic interference), background vibration '
        'from adjacent machinery transmitted through foundations and structures, and process-induced disturbances '
        'such as flow turbulence, cavitation, and random load fluctuations that can mask weak fault signatures [29]. '
        'The signal-to-noise ratio (SNR) for incipient fault signatures may be as low as -10 to -20 dB, meaning '
        'fault-related signal components are one to two orders of magnitude below the background noise level. '
        'Effective denoising and signal decomposition techniques are therefore essential for extracting diagnostically '
        'relevant information, particularly during early fault stages when defect-induced signal components are '
        'several orders of magnitude below background levels and timely detection offers the greatest value for '
        'maintenance planning.'))
    
    content.append(('para',
        'Classical filtering approaches including low-pass, high-pass, band-pass, and notch filters provide '
        'frequency-selective noise reduction when fault-relevant frequency bands are known a priori from bearing '
        'geometry calculations or previous diagnostic experience. Finite Impulse Response (FIR) and Infinite Impulse '
        'Response (IIR) digital filters offer complementary advantages: FIR filters guarantee linear phase response '
        'essential for preserving transient waveform shape and temporal relationships between signal components, '
        'while IIR filters achieve sharper frequency selectivity with lower computational order, enabling '
        'implementation on resource-constrained edge computing platforms [30]. Adaptive filters, particularly the '
        'Least Mean Squares (LMS) and Recursive Least Squares (RLS) algorithms, automatically adjust filter '
        'coefficients to minimize noise without requiring explicit knowledge of noise characteristics. These '
        'algorithms prove effective for canceling periodic interference such as gear mesh vibration and shaft '
        'harmonics when isolating bearing signatures, using reference signals from adjacent measurement points '
        'or synthesized reference signals based on tachometer inputs [31]. The Adaptive Line Enhancer (ALE) and '
        'Adaptive Noise Canceller (ANC) configurations address different noise reduction scenarios depending '
        'on reference signal availability.'))
    
    content.append(('para',
        'Wavelet-based denoising through thresholding of wavelet coefficients provides powerful non-linear noise '
        'reduction that preserves signal discontinuities and transient features critical for fault detection [32]. '
        'Hard and soft thresholding strategies, applied to detail coefficients across decomposition levels, attenuate '
        'noise-dominated coefficients while preserving signal-dominated coefficients above the threshold. The optimal '
        'threshold selection, often based on Donoho\'s universal threshold (sigma * sqrt(2*log(N))) or level-dependent '
        'SURE (Stein\'s Unbiased Risk Estimate) strategies, controls the trade-off between noise reduction and signal '
        'distortion. Singular Spectrum Analysis (SSA), which decomposes signals through trajectory matrix eigendecomposition, '
        'and Variational Mode Decomposition (VMD), which concurrently extracts a specified number of modes through '
        'constrained variational optimization, offer alternative decomposition frameworks that separate signal '
        'components based on spectral characteristics rather than time-frequency localization [33]. VMD in particular '
        'has demonstrated superior mode separation compared to EMD for vibration signals with closely-spaced frequency '
        'components. These advanced approaches prove particularly valuable when fault signatures overlap spectrally '
        'with dominant operational components, which represents the fundamental time-frequency analysis challenge '
        'illustrated in Figure 2 where different methods show varying capability to resolve overlapping components.'))
    
    # 2.3
    content.append(('heading2', '2.3 Feature Extraction and Fault-Sensitive Indicators'))
    
    content.append(('para',
        'Feature extraction transforms processed vibration signals into compact, informative representations suitable '
        'for machine learning-based classification, regression, and trending. The quality and relevance of extracted '
        'features fundamentally determines diagnostic system performance, as even the most sophisticated machine '
        'learning algorithm cannot compensate for features that fail to capture fault-sensitive signal characteristics '
        '[34]. Handcrafted features derived from domain expertise encompass time-domain statistics (RMS, kurtosis, '
        'skewness, peak values, shape factors), spectral features (harmonic amplitudes, spectral centroid, spectral '
        'bandwidth, spectral entropy), time-frequency features (wavelet energy distribution, STFT-derived statistics), '
        'and bearing-specific indicators (envelope spectrum amplitudes at characteristic frequencies). Comprehensive '
        'feature sets typically include 50-200 individual features spanning multiple signal representations to ensure '
        'coverage of diverse fault manifestations across different machinery components and fault types [35].'))
    
    content.append(('para',
        'Envelope analysis (amplitude demodulation) constitutes a specialized technique critical for bearing fault '
        'detection that has become the gold standard for rolling element bearing diagnostics in industry. The method '
        'involves band-pass filtering around structural resonance frequencies excited by repetitive bearing impacts, '
        'followed by Hilbert Transform-based analytic signal computation, magnitude extraction to obtain the envelope '
        'signal, and spectral analysis of the envelope to reveal bearing defect frequencies and their harmonics [36]. '
        'The resulting envelope spectrum reveals bearing defect repetition rates with dramatically enhanced '
        'signal-to-noise ratio compared to direct spectral analysis, as the demodulation process separates low-frequency '
        'defect repetition rates from high-frequency carrier resonances that may be 50-100 times higher in frequency. '
        'Spectral kurtosis, introduced by Antoni, provides an automated approach to optimal band-pass filter selection '
        'by computing kurtosis at each frequency and identifying bands with maximum non-Gaussianity indicative of '
        'impulsive content [37]. The kurtogram, a frequency-bandwidth map of spectral kurtosis, guides optimal '
        'demodulation band selection without requiring prior knowledge of resonance frequencies.'))
    
    content.append(('para',
        'Feature selection and dimensionality reduction address the curse of dimensionality when large feature '
        'sets are employed, removing redundant and irrelevant features that degrade classifier performance and '
        'increase computational requirements. Filter methods including correlation analysis, mutual information, '
        'Fisher score, and minimum redundancy maximum relevance (mRMR) evaluate individual feature discriminative '
        'power independently of the classifier [38]. Wrapper methods including sequential forward/backward selection, '
        'genetic algorithms, and particle swarm optimization evaluate feature subsets through cross-validated classifier '
        'performance, yielding optimal subsets at higher computational cost. Embedded methods such as LASSO (L1 '
        'regularization), elastic net, and tree-based feature importance provide feature selection integrated within '
        'the learning algorithm. Principal Component Analysis (PCA), Linear Discriminant Analysis (LDA), Independent '
        'Component Analysis (ICA), and t-distributed Stochastic Neighbor Embedding (t-SNE) provide dimensionality '
        'reduction through linear and non-linear projections that preserve class separability or data structure [39]. '
        'Health indicators constructed from multiple features through weighted combination, distance-based metrics '
        '(Mahalanobis distance from healthy baseline), or monotonicity-optimized indices provide univariate '
        'degradation trends suitable for remaining useful life estimation and threshold-based alerting.'))
    
    content.append(('para', ''))
    
    # ============================================================
    # SECTION 3
    # ============================================================
    content.append(('heading1', '3. Integration of Signal Processing with Artificial Intelligence'))
    
    # 3.1
    content.append(('heading2', '3.1 Machine Learning for Condition Monitoring'))
    
    content.append(('para',
        'Machine learning algorithms transform extracted vibration features into diagnostic and prognostic decisions, '
        'automating the expertise-intensive process of fault identification and severity assessment that traditionally '
        'required years of specialist training [40]. The application of machine learning to condition monitoring '
        'follows the standard supervised learning pipeline: feature vectors extracted from labeled training data are '
        'used to learn decision boundaries or regression functions, which are subsequently applied to new measurements '
        'for automated condition classification or health parameter estimation. Supervised learning methods including '
        'Support Vector Machines (SVM), Random Forests, k-Nearest Neighbors (kNN), and gradient boosting algorithms '
        '(XGBoost, LightGBM) achieve classification accuracies exceeding 95% for well-defined fault categories when '
        'trained on representative labeled datasets spanning the full range of fault types and severity levels [41]. '
        'The SVM algorithm with radial basis function (RBF) kernels has demonstrated particular effectiveness for '
        'small-sample bearing fault classification due to its structural risk minimization principle that maximizes '
        'margin between classes, providing excellent generalization from limited training examples.'))
    
    content.append(('para',
        'Unsupervised learning addresses the prevalent industrial scenario where labeled fault data is unavailable '
        'or insufficient, employing clustering algorithms (k-means, DBSCAN, spectral clustering, Gaussian mixture '
        'models), novelty detection methods, and self-organizing maps to identify anomalous operating states without '
        'requiring fault-specific training labels [42]. One-class SVM and isolation forests trained exclusively on '
        'healthy operation data define normal operation boundaries and detect deviations indicative of developing '
        'faults without requiring fault-specific training samples. This approach is particularly valuable for '
        'newly-commissioned equipment or rare fault modes where historical failure data simply does not exist. '
        'Semi-supervised approaches leverage small labeled datasets augmented with large unlabeled operational '
        'datasets through self-training, label propagation, co-training, or generative adversarial network (GAN) '
        'frameworks [43]. These approaches prove essential for industrial deployments where comprehensive fault '
        'data collection is impractical or prohibitively expensive due to the cost and risk of operating equipment '
        'to failure, as depicted in the comprehensive machine learning pipeline of Figure 3 which illustrates '
        'how different learning paradigms integrate within the overall diagnostic framework.'))
    
    # Figure 3 - first citation
    content.append(('image', 'fig3', 'Figure 3. Machine learning and deep learning pipeline for vibration-based fault diagnosis, illustrating the progression from raw signals through feature extraction and model training to multi-class fault classification with comparative architecture performance.'))
    content.append(('para', ''))
    
    content.append(('para',
        'Remaining useful life (RUL) estimation employs regression-based approaches including support vector '
        'regression (SVR), Gaussian process regression (GPR), and ensemble methods to predict the time until '
        'functional failure from current condition indicators and their evolution trajectories [44]. The degradation '
        'modeling approach fits parametric models (exponential, logarithmic, power law, or sigmoid functions) to '
        'health indicator trajectories derived from vibration features, extrapolating to predefined failure '
        'thresholds with quantified prediction uncertainty. Gaussian process regression provides inherent uncertainty '
        'quantification through its probabilistic formulation, outputting both mean predictions and confidence '
        'intervals essential for risk-informed maintenance scheduling. Particle filtering and Bayesian updating '
        'frameworks enable online model parameter adaptation as new measurements become available, progressively '
        'narrowing RUL prediction uncertainty as the system approaches failure. Table 3 presents a comprehensive '
        'performance comparison of machine learning approaches applied to fault diagnosis across benchmark datasets '
        'under various experimental conditions and fault severity levels.'))
    
    # Table 3
    content.append(('table', 'table3', 'Table 3. Performance comparison of machine learning algorithms for vibration-based fault diagnosis across standard benchmark datasets with varying fault types and severity levels.'))
    content.append(('para', ''))
    
    # 3.2
    content.append(('heading2', '3.2 Deep Learning for Automated Signal Analysis'))
    
    content.append(('para',
        'Deep learning architectures have revolutionized vibration-based condition monitoring by enabling end-to-end '
        'learning from raw or minimally processed signals, fundamentally eliminating the need for manual feature '
        'engineering that has traditionally represented the primary bottleneck in developing diagnostic systems for '
        'new equipment types [45]. One-dimensional Convolutional Neural Networks (1D-CNNs) apply learnable '
        'convolutional filters directly to raw vibration time series, automatically extracting hierarchical features '
        'through successive convolution, batch normalization, activation, and pooling layers. The initial layers '
        'learn local pattern detectors analogous to handcrafted features (impulse detection, frequency band energy, '
        'modulation patterns), while deeper layers combine these into abstract representations capturing complex '
        'fault signatures. The translation-invariant nature of convolution operations provides inherent robustness '
        'to temporal shifts in fault signatures caused by speed variations or random fault positioning, while '
        'hierarchical feature extraction captures both local waveform patterns and global signal characteristics [46]. '
        'The deep learning architectures and their comparative performance metrics are comprehensively presented '
        'in the ML pipeline framework of Figure 3, demonstrating the significant accuracy advantages of deep '
        'learning over traditional machine learning approaches.'))
    
    content.append(('para',
        'Recurrent Neural Networks (RNNs), particularly Long Short-Term Memory (LSTM) networks and Gated Recurrent '
        'Units (GRUs), excel at modeling temporal dependencies in vibration sequences where the ordering and '
        'temporal context of signal segments carries diagnostic information [47]. The gating mechanisms in LSTM '
        'cells (input gate, forget gate, output gate) selectively retain and forget information across extended '
        'time horizons, enabling capture of long-range dependencies between vibration events separated by hundreds '
        'or thousands of time steps. This capability proves essential for detecting slowly-evolving degradation '
        'patterns and correlating intermittent fault signatures. Bidirectional LSTM architectures process signals '
        'in both forward and reverse temporal directions, providing comprehensive temporal context for each time '
        'step and improving classification accuracy for faults whose signatures depend on both preceding and '
        'following signal content. For RUL prediction, LSTM networks model degradation trajectories as temporal '
        'sequences of feature vectors, learning complex non-linear degradation patterns from historical '
        'run-to-failure datasets without requiring explicit degradation model specification. The combination of '
        'CNN feature extraction with LSTM temporal modeling in hybrid CNN-LSTM architectures has shown state-of-the-art '
        'results for both fault diagnosis and RUL estimation tasks.'))
    
    content.append(('para',
        'Transformer architectures, originally developed for natural language processing, have recently demonstrated '
        'exceptional capability for vibration signal analysis through self-attention mechanisms that capture '
        'long-range dependencies without the sequential processing constraints inherent to recurrent architectures [40]. '
        'The multi-head attention mechanism computes relevance weights between all positions in the input sequence '
        'simultaneously through scaled dot-product attention, enabling parallel processing of the entire signal '
        'and capturing global signal relationships regardless of temporal distance. This parallelism dramatically '
        'accelerates training compared to LSTM while maintaining or exceeding diagnostic accuracy. Vision '
        'Transformers adapted for one-dimensional signals partition vibration data into non-overlapping patches, '
        'each linearly projected and processed as tokens with learnable positional embeddings that encode temporal '
        'ordering information. The attention maps generated by Transformer models provide interpretable visualization '
        'of which signal segments most influence diagnostic decisions, offering a degree of explainability absent '
        'in CNN-based approaches. Recent studies demonstrate that Transformer-based models achieve state-of-the-art '
        'accuracy on benchmark bearing fault datasets including CWRU (Case Western Reserve University) and Paderborn, '
        'with classification accuracies exceeding 99% under consistent operating conditions and maintaining above '
        '95% accuracy under variable speed and load scenarios that challenge conventional approaches [40].'))
    
    # 3.3
    content.append(('heading2', '3.3 Intelligent Feature Learning and Hybrid Approaches'))
    
    content.append(('para',
        'Hybrid approaches combining classical signal processing with deep learning leverage the complementary '
        'strengths of both paradigms: the physical interpretability, noise robustness, and data efficiency of '
        'signal processing transformations with the adaptive feature learning capability and pattern recognition '
        'power of neural networks [41]. A prevalent and highly effective architecture applies wavelet, STFT, or '
        'Wigner-Ville transformations to convert one-dimensional vibration signals into two-dimensional '
        'time-frequency representations, subsequently processed by 2D-CNNs that exploit the powerful spatial '
        'feature extraction capabilities developed for image recognition tasks including ResNet, VGG, and '
        'Inception architectures. This signal processing-informed approach consistently outperforms purely '
        'data-driven methods when training data is limited (fewer than 100 samples per class), as the '
        'time-frequency transformation incorporates decades of domain knowledge into the signal representation '
        'without requiring the network to learn these transformations from data [42]. The choice of time-frequency '
        'representation (spectrogram, scalogram, or Wigner-Ville distribution) can be optimized for specific '
        'fault types, with spectrograms favoring stationary analysis and scalograms emphasizing transient detection.'))
    
    content.append(('para',
        'Physics-informed neural networks (PINNs) represent an emerging paradigm that incorporates mechanical system '
        'dynamics equations and physical constraints directly within the learning framework, ensuring physically '
        'consistent predictions even in data-sparse regimes where purely data-driven models may produce physically '
        'implausible outputs [43]. The integration of bearing dynamics models, gear contact mechanics equations, '
        'or rotor dynamics transfer functions as loss function regularization terms guides the network toward '
        'solutions consistent with known mechanical behavior. For example, constraining predicted fault frequencies '
        'to lie within physically permissible ranges based on rotational speed and geometry prevents false '
        'positive diagnoses at mechanically impossible frequencies. Domain adaptation techniques address the '
        'common industrial scenario where training data originates from test rigs or similar but non-identical '
        'machines, and deployment occurs on target equipment with different characteristics [44]. Adversarial '
        'domain adaptation using gradient reversal layers, maximum mean discrepancy minimization, and optimal '
        'transport-based alignment methods align feature distributions across source and target domains while '
        'preserving discriminative information. Transfer learning from large pre-trained models (ImageNet-pretrained '
        'CNNs adapted for spectrograms, or vibration foundation models) to specific machinery with limited labeled '
        'data dramatically reduces labeling requirements while maintaining diagnostic accuracy above 90% with as '
        'few as 5-10 labeled samples per fault class.'))
    
    content.append(('para', ''))
    
    # ============================================================
    # SECTION 4
    # ============================================================
    content.append(('heading1', '4. Real-Time Implementation and Future Directions'))
    
    # 4.1
    content.append(('heading2', '4.1 Real-Time Condition Monitoring Systems'))
    
    content.append(('para',
        'The transition from offline periodic vibration analysis to continuous real-time condition monitoring '
        'represents a fundamental evolution in predictive maintenance capability, enabled by concurrent advances '
        'in embedded computing hardware, microelectromechanical systems (MEMS) sensor technology, wireless '
        'communication infrastructure, and cloud computing platforms [45]. Real-time systems must perform signal '
        'acquisition, preprocessing, feature extraction, and diagnostic inference within timing constraints dictated '
        'by the monitored process dynamics and fault propagation rates. For high-speed rotating machinery operating '
        'above 3000 RPM with rapidly progressing faults such as bearing cage failures or shaft cracks, processing '
        'latency must remain below 100 milliseconds to enable protective actions before catastrophic failure. The '
        'complete architecture of a modern real-time condition monitoring system encompasses multiple hierarchical '
        'processing layers as depicted in Figure 4, which illustrates how physical sensors, edge computing, cloud '
        'analytics, and decision support integrate through Industrial IoT connectivity to deliver continuous '
        'health assessment and predictive maintenance intelligence.'))
    
    # Figure 4 - first citation
    content.append(('image', 'fig4', 'Figure 4. Multi-layer architecture for real-time condition monitoring systems showing the integration of physical sensors, edge computing, cloud-based AI analytics, and decision support layers with Industrial IoT connectivity.'))
    content.append(('para', ''))
    
    content.append(('para',
        'Edge computing architectures deploy signal processing and inference algorithms directly at or near the '
        'monitored equipment, fundamentally reducing latency from seconds (cloud round-trip) to milliseconds '
        '(local processing), minimizing bandwidth requirements by transmitting only features and alerts rather '
        'than raw waveforms, and eliminating dependence on network connectivity for safety-critical monitoring '
        'functions [46]. Modern intelligent sensors integrate MEMS accelerometers with embedded ARM Cortex-M or '
        'RISC-V microcontrollers capable of performing 4096-point FFT computation in under 1 millisecond, '
        'statistical feature extraction, and even lightweight neural network inference (quantized models under '
        '100KB) directly on the sensor module. These smart sensors operate on battery power or energy harvesting '
        'for years while providing continuous monitoring capability. Field-Programmable Gate Arrays (FPGAs) provide '
        'hardware-accelerated signal processing with deterministic timing for safety-critical applications where '
        'microsecond latency is required, while edge-deployed Graphics Processing Units (GPUs) and Neural Processing '
        'Units (NPUs) enable real-time deep learning inference for complex diagnostic models requiring millions '
        'of multiply-accumulate operations per inference cycle [47]. The edge tier handles time-critical processing '
        'including anti-aliasing filtering, decimation, FFT computation, envelope analysis, statistical feature '
        'extraction, and threshold-based alerting, operating autonomously even during complete network outages '
        'to ensure continuous equipment protection.'))
    
    content.append(('para',
        'Industrial Internet of Things (IIoT) platforms provide the communication and integration infrastructure '
        'connecting distributed edge devices to centralized analytics systems, enabling fleet-wide visibility and '
        'coordinated maintenance optimization across entire production facilities or geographically distributed '
        'asset portfolios [39]. Communication protocols including MQTT (for lightweight publish-subscribe messaging), '
        'OPC-UA (for interoperability across vendor platforms), and AMQP (for reliable message queuing) enable '
        'efficient, secure transmission of vibration data, derived features, health assessments, and alert '
        'notifications. Time-series databases (InfluxDB, TimescaleDB, Apache IoTDB) optimized for high-throughput '
        'sensor data ingestion and temporal query patterns store historical vibration trends enabling long-term '
        'degradation tracking and remaining useful life computation [38]. Cloud-based analytics platforms aggregate '
        'data from hundreds or thousands of monitored assets, enabling fleet-wide pattern recognition through '
        'statistical comparison of similar machines, identification of systematic issues affecting machine '
        'populations, and model training on comprehensive datasets spanning diverse operating conditions. The cloud '
        'tier handles computationally intensive tasks including deep learning model training and hyperparameter '
        'optimization, transfer learning model adaptation, digital twin physics model calibration, and long-term '
        'prognostic computation requiring full degradation history analysis. The hierarchical architecture, as '
        'comprehensively shown in Figure 4, optimally balances real-time latency requirements at the edge with '
        'computational capability and data aggregation in the cloud through appropriate distribution of processing '
        'responsibilities across tiers.'))
    
    # 4.2
    content.append(('heading2', '4.2 Performance Evaluation and Practical Challenges'))
    
    content.append(('para',
        'Comprehensive performance evaluation of condition monitoring systems encompasses multiple dimensions beyond '
        'simple classification accuracy, including robustness to operating condition variations, computational '
        'efficiency and resource constraints, false alarm rates and their operational impact, early detection '
        'capability (detection lead time before failure), diagnostic specificity (ability to distinguish between '
        'fault types), and graceful degradation under adversarial or out-of-distribution conditions [37]. Table 4 '
        'summarizes key performance metrics and evaluation criteria employed in the assessment of vibration-based '
        'diagnostic systems along with typical industrial requirements and mitigation strategies for common challenges. '
        'Standard benchmark datasets including the Case Western Reserve University (CWRU) bearing dataset (most widely '
        'used with over 2000 citations), Paderborn bearing dataset (variable speed and load), IMS/NASA bearing '
        'run-to-failure dataset (prognostics), FEMTO bearing dataset (accelerated degradation), and PHM Society '
        'challenge datasets provide controlled evaluation environments with ground-truth labels [36]. However, '
        'their laboratory conditions with constant speed, controlled loads, and seeded faults may not fully '
        'represent the complexity of industrial operating environments.'))
    
    # Table 4
    content.append(('table', 'table4', 'Table 4. Performance evaluation metrics and practical challenges in deploying vibration-based condition monitoring systems, with typical requirements for industrial applications.'))
    content.append(('para', ''))
    
    content.append(('para',
        'Variable operating conditions including speed, load, and temperature variations represent the most '
        'significant practical challenge for deployed condition monitoring systems, as most laboratory-validated '
        'algorithms assume constant or slowly-varying operating conditions [35]. Speed changes fundamentally alter '
        'fault characteristic frequencies, requiring order tracking (resampling signals to constant angular increment) '
        'or speed-normalized analysis for consistent diagnosis across the operating speed range. Load variations '
        'modulate vibration amplitudes through both direct force excitation changes and indirect effects on bearing '
        'clearance and contact conditions, potentially activating or suppressing specific vibration mechanisms at '
        'different load levels. Domain shift between controlled training conditions and variable operational '
        'conditions degrades model performance significantly, with typical accuracy drops of 15-30% reported when '
        'models trained at one speed are tested at different speeds without adaptation [34]. This necessitates domain '
        'adaptation algorithms, operating-condition-aware normalization strategies, or continual learning approaches '
        'that update model parameters as new operating conditions are encountered. Environmental factors including '
        'temperature fluctuations (affecting sensor sensitivity and bearing clearance), humidity, electromagnetic '
        'interference from variable frequency drives, and structural resonance shifts further introduce variability '
        'that must be addressed in robust system design through appropriate sensor compensation and signal conditioning.'))
    
    content.append(('para',
        'Data imbalance constitutes a pervasive challenge in fault diagnosis, as healthy operation data vastly '
        'outnumbers fault data in real-world industrial settings, with typical ratios of 100:1 to 10000:1 between '
        'normal and fault class samples [33]. This extreme imbalance causes standard classifiers to achieve high '
        'overall accuracy by simply predicting the majority class while completely failing to detect minority fault '
        'classes. Algorithmic solutions including synthetic minority oversampling (SMOTE and its variants: '
        'Borderline-SMOTE, ADASYN), generative adversarial networks (GANs) for realistic synthetic fault data '
        'generation, cost-sensitive learning with class-weighted loss functions, and focal loss that emphasizes '
        'hard-to-classify minority examples address class imbalance at both data and algorithmic levels. Sensor '
        'degradation over time through cable damage, mounting looseness, sensitivity drift due to piezoelectric '
        'aging, and intermittent connections can introduce measurement artifacts misidentified as machine faults, '
        'requiring parallel sensor health monitoring through impedance checking, cross-sensor consistency validation, '
        'and redundant measurement configurations [44]. Limited availability of labeled fault data, particularly '
        'for rare catastrophic failure modes that occur once in the lifetime of a machine, motivates few-shot '
        'learning using prototypical networks, meta-learning through model-agnostic meta-learning (MAML), and '
        'physics-based simulation for synthetic training data generation that supplements scarce real fault examples.'))
    
    # 4.3
    content.append(('heading2', '4.3 Future Trends in AI-Enabled Signal Processing'))
    
    content.append(('para',
        'Self-supervised learning and foundation models represent the most promising frontier in vibration-based '
        'condition monitoring, offering pathways to overcome the fundamental limitation of labeled data scarcity '
        'that has constrained practical deployment of AI-based monitoring systems [45]. Self-supervised pre-training '
        'strategies learn universal vibration representations from massive unlabeled operational datasets through '
        'pretext tasks including contrastive learning (SimCLR, MoCo adapted for time series), masked signal modeling '
        '(randomly masking signal segments and training reconstruction), temporal prediction (forecasting future '
        'signal segments from past context), and multi-view learning (comparing representations from different '
        'signal transformations of the same measurement). Foundation models pre-trained across diverse machinery '
        'types, operational regimes, fault modes, and industrial sectors could provide general-purpose vibration '
        'intelligence transferable to any specific diagnostic task with minimal fine-tuning, analogous to how GPT '
        'and BERT models provide transferable language understanding [46]. Early research demonstrates that '
        'self-supervised pre-training on 100,000+ unlabeled vibration recordings significantly improves downstream '
        'fault classification accuracy by 10-25% compared to training from scratch, with the largest improvements '
        'occurring in low-data regimes where labeled samples are limited to 5-50 per class.'))
    
    content.append(('para',
        'Explainable and trustworthy AI addresses the critical industrial requirement for interpretable and '
        'verifiable diagnostic decisions in safety-critical maintenance applications where incorrect predictions '
        'can lead to catastrophic equipment failure or unnecessary costly shutdowns [47]. Black-box deep learning '
        'models that provide predictions without justification face significant adoption barriers in regulated '
        'industries including aerospace, nuclear, and petrochemical where maintenance decisions must be auditable '
        'and defensible. Gradient-weighted Class Activation Mapping (Grad-CAM) adapted for one-dimensional signals '
        'highlights temporal and spectral regions most influential for classification decisions, enabling domain '
        'experts to verify that the model focuses on physically meaningful signal characteristics rather than '
        'spurious correlations or dataset artifacts. Attention weight visualization in Transformer architectures '
        'reveals which signal segments the model considers most diagnostically relevant, providing interpretable '
        'evidence supporting each diagnosis [39]. Physics-informed explanations that automatically map learned '
        'features back to known fault mechanisms (e.g., identifying that a classification relies on spectral content '
        'at bearing defect frequencies) bridge the gap between AI predictions and engineering understanding, '
        'building the operator trust essential for widespread adoption. Uncertainty quantification through Bayesian '
        'deep learning, Monte Carlo dropout, deep ensembles, or evidential deep learning provides calibrated '
        'confidence estimates alongside predictions, enabling the system to flag low-confidence diagnoses for '
        'human expert review rather than making potentially incorrect autonomous decisions.'))
    
    content.append(('para',
        'Digital twins create high-fidelity virtual replicas of physical machinery incorporating multi-physics '
        'simulation models (structural dynamics, thermodynamics, tribology, fluid mechanics), historical operational '
        'data, maintenance records, and real-time sensor streams to enable predictive simulation, anomaly detection, '
        'and maintenance optimization [38]. The integration of digital twins with AI-based condition monitoring '
        'creates a powerful synergy: the physics model provides expected behavior predictions against which measured '
        'vibration is compared for sensitive anomaly detection, while AI models learn the residual patterns between '
        'prediction and measurement that indicate developing faults before they manifest in absolute vibration levels. '
        'Root cause analysis is facilitated through systematic variation of digital twin parameters to identify '
        'which physical degradation mechanism best explains observed vibration changes. Optimized maintenance '
        'scheduling leverages digital twin prognostic simulation to evaluate the consequences of different '
        'maintenance timing scenarios on equipment reliability, production continuity, and lifecycle cost [37]. '
        'Autonomous diagnostic systems that seamlessly combine ubiquitous sensor networks, edge AI for real-time '
        'inference, digital twins for physics-based reasoning, and automated maintenance scheduling represent the '
        'vision of fully autonomous condition-based maintenance operations requiring minimal human intervention '
        'for routine decisions while escalating complex or novel situations to expert attention [36]. The convergence '
        'of 5G/6G communication for ultra-reliable low-latency connectivity, advanced MEMS sensor arrays with '
        'integrated AI, neuromorphic computing for energy-efficient continuous processing, quantum machine learning '
        'for complex pattern recognition, and federated learning enabling model improvement across distributed '
        'industrial assets while preserving data privacy collectively promises to transform predictive maintenance '
        'from a specialized engineering discipline into an autonomous, self-improving capability embedded within '
        'intelligent manufacturing systems. The integration of these technologies with existing enterprise resource '
        'planning (ERP) systems, computerized maintenance management systems (CMMS), and supply chain management '
        'platforms will enable truly holistic asset lifecycle optimization where maintenance decisions are automatically '
        'coordinated with production scheduling, spare parts procurement, workforce allocation, and capital investment '
        'planning to minimize total cost of ownership while maximizing equipment availability and operational safety.'))
    
    content.append(('para', ''))
    
    # ============================================================
    # CONCLUSIONS
    # ============================================================
    content.append(('heading1', '5. Conclusions'))
    
    content.append(('para',
        'This chapter has presented a comprehensive framework for signal processing in condition monitoring of '
        'mechanical systems, demonstrating the critical role of signal processing as the enabling bridge between '
        'raw vibration measurements and intelligent maintenance decision-making. The evolution of condition monitoring '
        'technology over the past four decades has been remarkable, progressing from simple overall vibration level '
        'measurements with manual threshold comparison to sophisticated AI-powered systems capable of autonomous '
        'fault detection, classification, and remaining useful life prediction with minimal human oversight. '
        'The progression from fundamental time-domain and frequency-domain techniques through advanced time-frequency '
        'analysis methods to modern AI-enabled automated diagnostics reflects both the historical development of the '
        'field and the increasing sophistication of available computational and sensing tools. Each processing stage '
        'contributes essential capabilities: time-domain analysis provides computationally efficient overall condition '
        'assessment suitable for continuous online monitoring, frequency-domain analysis enables source-specific fault '
        'identification through characteristic frequency detection and spectral pattern recognition, time-frequency '
        'methods capture non-stationary fault dynamics invisible to conventional spectral analysis, and machine learning '
        'and deep learning architectures automate the complex multi-dimensional pattern recognition task that previously '
        'required extensive human expertise accumulated over years of specialized practice and training.'))
    
    content.append(('para',
        'The integration of signal processing with artificial intelligence represents the most transformative '
        'development in condition monitoring over the past decade, enabling systems that continuously learn from '
        'operational data streams, automatically adapt to new machinery types and operating conditions without '
        'manual reconfiguration, and provide increasingly accurate diagnostic and prognostic assessments with '
        'minimal human intervention [39]. The ability of deep learning architectures to learn directly from raw '
        'sensor data eliminates the traditional bottleneck of manual feature engineering, while the growing '
        'availability of industrial sensor data provides the training material needed for increasingly capable '
        'models. Deep learning architectures including CNNs, LSTMs, and Transformers have demonstrated that '
        'end-to-end learning from raw vibration signals can match or exceed the performance of carefully engineered '
        'feature-based approaches, while hybrid methods combining signal processing domain knowledge with neural '
        'network learning capability offer the best balance of accuracy, data efficiency, and interpretability for '
        'practical industrial deployment where both performance and trustworthiness are essential requirements. '
        'The continuing evolution toward self-supervised foundation models, physics-informed learning, and '
        'explainable AI promises to address remaining barriers to widespread autonomous deployment including '
        'labeled data scarcity, model interpretability, and cross-domain generalization [46].'))
    
    content.append(('para',
        'Real-time implementation through hierarchical edge-cloud architectures, combined with Industrial IoT '
        'connectivity and digital twin technology, provides the infrastructure necessary for continuous, autonomous '
        'condition monitoring at industrial scale encompassing thousands of monitored assets across geographically '
        'distributed facilities [47]. The edge computing layer ensures safety-critical monitoring functions continue '
        'operating independently of network availability, while cloud-based analytics enable fleet-wide optimization '
        'and continuous model improvement from aggregated operational experience. However, significant practical '
        'challenges remain including variable operating conditions that shift fault characteristics, extreme data '
        'imbalance between normal operation and rare fault events, domain shift between controlled training conditions '
        'and real deployment environments, sensor degradation that introduces measurement artifacts, and the '
        'fundamental scarcity of labeled fault data for rare catastrophic failure modes. Addressing these challenges '
        'requires continued interdisciplinary research combining signal processing theory, machine learning '
        'methodology, mechanical engineering domain knowledge, and industrial systems engineering expertise. The '
        'convergence of these disciplines, enabled by rapidly advancing computational capabilities, ubiquitous '
        'sensing technologies, and increasingly capable AI architectures, positions signal processing-based condition '
        'monitoring as the foundation for next-generation autonomous predictive maintenance systems that will '
        'fundamentally transform industrial asset management from reactive repair to proactive optimization of '
        'equipment health, reliability, and lifecycle value. Future research directions should prioritize the '
        'development of standardized benchmarks reflecting real industrial conditions, open-source foundation models '
        'for vibration analysis, and industry-academia collaboration frameworks that accelerate translation of '
        'algorithmic advances into deployed systems delivering measurable economic and safety benefits across '
        'diverse industrial sectors.'))
    
    content.append(('para', ''))
    
    # ============================================================
    # REFERENCES
    # ============================================================
    content.append(('heading1', 'References'))
    
    references = [
        "[1] R. B. Randall, Vibration-Based Condition Monitoring: Industrial, Aerospace and Automotive Applications, 2nd ed. Chichester: John Wiley & Sons, 2021.",
        "[2] A. K. S. Jardine, D. Lin, and D. Banjevic, \"A review on machinery diagnostics and prognostics implementing condition-based maintenance,\" Mechanical Systems and Signal Processing, vol. 20, no. 7, pp. 1483-1510, 2006.",
        "[3] C. Scheffer and P. Girdhar, Practical Machinery Vibration Analysis and Predictive Maintenance. Oxford: Newnes, 2004.",
        "[4] N. Tandon and A. Choudhury, \"A review of vibration and acoustic measurement methods for the detection of defects in rolling element bearings,\" Tribology International, vol. 32, no. 8, pp. 469-480, 1999.",
        "[5] D. E. Bently and C. T. Hatch, Fundamentals of Rotating Machinery Diagnostics. Minden: Bently Pressurized Bearing Press, 2002.",
        "[6] A. V. Oppenheim and R. W. Schafer, Discrete-Time Signal Processing, 3rd ed. Upper Saddle River: Pearson, 2010.",
        "[7] National Instruments, \"Data Acquisition Fundamentals,\" Application Note AN-370, 2020.",
        "[8] P. D. McFadden and J. D. Smith, \"Vibration monitoring of rolling element bearings by the high-frequency resonance technique,\" Tribology International, vol. 17, no. 1, pp. 3-10, 1984.",
        "[9] ISO 10816-3:2009, Mechanical vibration - Evaluation of machine vibration by measurements on non-rotating parts, International Organization for Standardization, Geneva, 2009.",
        "[10] R. B. W. Heng and M. J. M. Nor, \"Statistical analysis of sound and vibration signals for monitoring rolling element bearing condition,\" Applied Acoustics, vol. 53, no. 1-3, pp. 211-226, 1998.",
        "[11] D. Dyer and R. M. Stewart, \"Detection of rolling element bearing damage by statistical vibration analysis,\" Journal of Mechanical Design, vol. 100, no. 2, pp. 229-235, 1978.",
        "[12] I. Howard, \"A review of rolling element bearing vibration: detection, diagnosis and prognosis,\" Defence Science and Technology Organisation, DSTO-RR-0013, 1994.",
        "[13] R. B. Randall and J. Antoni, \"Rolling element bearing diagnostics - A tutorial,\" Mechanical Systems and Signal Processing, vol. 25, no. 2, pp. 485-520, 2011.",
        "[14] P. D. McFadden, \"A technique for calculating the time domain averages of the vibration of the individual planet gears and the sun gear in an epicyclic gearbox,\" Journal of Sound and Vibration, vol. 144, no. 1, pp. 163-172, 1991.",
        "[15] S. Braun, Discover Signal Processing: An Interactive Guide for Engineers. Chichester: John Wiley & Sons, 2008.",
        "[16] J. W. Cooley and J. W. Tukey, \"An algorithm for the machine calculation of complex Fourier series,\" Mathematics of Computation, vol. 19, no. 90, pp. 297-301, 1965.",
        "[17] P. D. Welch, \"The use of fast Fourier transform for the estimation of power spectra,\" IEEE Transactions on Audio and Electroacoustics, vol. 15, no. 2, pp. 70-73, 1967.",
        "[18] T. A. Harris and M. N. Kotzalas, Rolling Bearing Analysis, 5th ed. Boca Raton: CRC Press, 2007.",
        "[19] J. I. Taylor, The Vibration Analysis Handbook, 2nd ed. Tampa: Vibration Consultants Inc., 2003.",
        "[20] L. Cohen, Time-Frequency Analysis. Englewood Cliffs: Prentice Hall, 1995.",
        "[21] J. B. Allen and L. R. Rabiner, \"A unified approach to short-time Fourier analysis and synthesis,\" Proceedings of the IEEE, vol. 65, no. 11, pp. 1558-1564, 1977.",
        "[22] F. Hlawatsch and G. F. Boudreaux-Bartels, \"Linear and quadratic time-frequency signal representations,\" IEEE Signal Processing Magazine, vol. 9, no. 2, pp. 21-67, 1992.",
        "[23] S. Mallat, A Wavelet Tour of Signal Processing, 3rd ed. Burlington: Academic Press, 2009.",
        "[24] I. Daubechies, Ten Lectures on Wavelets. Philadelphia: SIAM, 1992.",
        "[25] W. J. Wang and P. D. McFadden, \"Application of wavelets to gearbox vibration signals for fault detection,\" Journal of Sound and Vibration, vol. 192, no. 5, pp. 927-939, 1996.",
        "[26] N. E. Huang et al., \"The empirical mode decomposition and the Hilbert spectrum for nonlinear and non-stationary time series analysis,\" Proceedings of the Royal Society A, vol. 454, pp. 903-995, 1998.",
        "[27] Z. H. Wu and N. E. Huang, \"Ensemble empirical mode decomposition: A noise-assisted data analysis method,\" Advances in Adaptive Data Analysis, vol. 1, no. 1, pp. 1-41, 2009.",
        "[28] J. Antoni, \"The spectral kurtosis: A useful tool for characterising non-stationary signals,\" Mechanical Systems and Signal Processing, vol. 20, no. 2, pp. 282-307, 2006.",
        "[29] S. K. Mitra, Digital Signal Processing: A Computer-Based Approach, 4th ed. New York: McGraw-Hill, 2011.",
        "[30] S. Haykin, Adaptive Filter Theory, 5th ed. Upper Saddle River: Pearson, 2014.",
        "[31] D. L. Donoho, \"De-noising by soft-thresholding,\" IEEE Transactions on Information Theory, vol. 41, no. 3, pp. 613-627, 1995.",
        "[32] K. Dragomiretskiy and D. Zosso, \"Variational mode decomposition,\" IEEE Transactions on Signal Processing, vol. 62, no. 3, pp. 531-544, 2014.",
        "[33] Y. Lei, J. Lin, Z. He, and M. J. Zuo, \"A review on empirical mode decomposition in fault diagnosis of rotating machinery,\" Mechanical Systems and Signal Processing, vol. 35, no. 1-2, pp. 108-126, 2013.",
        "[34] B. Li, M.-Y. Chow, Y. Tipsuwan, and J. C. Hung, \"Neural-network-based motor rolling bearing fault diagnosis,\" IEEE Transactions on Industrial Electronics, vol. 47, no. 5, pp. 1060-1069, 2000.",
        "[35] R. B. Randall and J. Antoni, \"Rolling element bearing diagnostics - A tutorial,\" Mechanical Systems and Signal Processing, vol. 25, no. 2, pp. 485-520, 2011.",
        "[36] J. Antoni and R. B. Randall, \"The spectral kurtosis: Application to the vibratory surveillance and diagnostics of rotating machines,\" Mechanical Systems and Signal Processing, vol. 20, no. 2, pp. 308-331, 2006.",
        "[37] Y. Lei, Z. He, and Y. Zi, \"Application of an intelligent classification method to mechanical fault diagnosis,\" Expert Systems with Applications, vol. 36, no. 6, pp. 9941-9948, 2009.",
        "[38] K. Javed, R. Gouriveau, and N. Zerhouni, \"State of the art and taxonomy of prognostics approaches, trends of prognostics applications and open issues towards maturity at different technology readiness levels,\" Mechanical Systems and Signal Processing, vol. 94, pp. 214-236, 2017.",
        "[39] Y. Lei, B. Yang, X. Jiang, F. Jia, N. Li, and A. K. Nandi, \"Applications of machine learning to machine fault diagnosis: A review and roadmap,\" Mechanical Systems and Signal Processing, vol. 138, p. 106587, 2020.",
        "[40] B. S. Yang, T. Han, and W. W. Hwang, \"Fault diagnosis of rotating machinery based on multi-class support vector machines,\" Journal of Mechanical Science and Technology, vol. 19, no. 3, pp. 846-859, 2005.",
        "[41] V. Chandola, A. Banerjee, and V. Kumar, \"Anomaly detection: A survey,\" ACM Computing Surveys, vol. 41, no. 3, pp. 1-58, 2009.",
        "[42] X. Zhu, \"Semi-supervised learning literature survey,\" Computer Sciences Technical Report 1530, University of Wisconsin-Madison, 2008.",
        "[43] X.-S. Si, W. Wang, C.-H. Hu, and D.-H. Zhou, \"Remaining useful life estimation - A review on the statistical data driven approaches,\" European Journal of Operational Research, vol. 213, no. 1, pp. 1-14, 2011.",
        "[44] W. Zhang, C. Li, G. Peng, Y. Chen, and Z. Zhang, \"A deep convolutional neural network with new training methods for bearing fault diagnosis under noisy environment and different working load,\" Mechanical Systems and Signal Processing, vol. 100, pp. 439-453, 2018.",
        "[45] S. Zhang, S. Zhang, B. Wang, and T. G. Habetler, \"Deep learning algorithms for bearing fault diagnostics - A comprehensive review,\" IEEE Access, vol. 8, pp. 29857-29881, 2020.",
        "[46] L. Guo, Y. Lei, N. Li, T. Yan, and N. Li, \"Machinery health indicator construction based on convolutional neural networks considering trend burr,\" Neurocomputing, vol. 292, pp. 142-150, 2018.",
        "[47] Z. Ding, H. Li, and Y. Zhou, \"A vibration Transformer for bearing fault diagnosis via self-attention mechanism,\" IEEE Transactions on Instrumentation and Measurement, vol. 72, pp. 1-12, 2023.",
    ]
    
    for ref in references:
        content.append(('para', ref))
    
    return content


def get_tables():
    """Return table data for all 4 tables."""
    tables = {}
    
    # Table 1
    tables['table1'] = (
        ["Feature", "Formula/Definition", "Sensitivity", "Primary Application"],
        [
            ["RMS", "sqrt(mean(x^2))", "Overall severity", "General trending, ISO standards"],
            ["Peak Value", "max(|x|)", "Maximum excursion", "Impact detection, clearance"],
            ["Crest Factor", "Peak / RMS", "Impulsivity ratio", "Early bearing defects"],
            ["Kurtosis", "E[(x-mu)^4] / sigma^4", "Tailedness (>3 = impulsive)", "Localized surface damage"],
            ["Skewness", "E[(x-mu)^3] / sigma^3", "Asymmetry detection", "Shaft bow, rubbing"],
            ["Shape Factor", "RMS / Mean(|x|)", "Waveform shape change", "Distributed damage"],
            ["Impulse Factor", "Peak / Mean(|x|)", "Impulse sensitivity", "Early-stage pitting"],
            ["Clearance Factor", "Peak / (Mean(sqrt(|x|)))^2", "Maximum sensitivity", "Severe localized defects"],
        ]
    )
    
    # Table 2
    tables['table2'] = (
        ["Method", "Time Resolution", "Freq Resolution", "Adaptivity", "Computation", "Best Application"],
        [
            ["STFT", "Fixed (window)", "Fixed (1/window)", "None (basis fixed)", "O(N log N)", "Steady-state signals"],
            ["CWT", "Variable (scale)", "Variable (1/scale)", "Multi-resolution", "O(N^2) or O(N log N)", "Transient detection"],
            ["DWT/WPT", "Dyadic scales", "Octave bands", "Multi-resolution", "O(N)", "Real-time decomposition"],
            ["EMD/HHT", "Instantaneous", "Instantaneous", "Fully adaptive", "O(N^2)", "Non-linear/non-stationary"],
            ["VMD", "Mode-dependent", "Mode-dependent", "Semi-adaptive", "O(N log N)", "Mode separation"],
            ["Wigner-Ville", "Optimal joint", "Optimal joint", "None", "O(N^2)", "Single-component analysis"],
        ]
    )
    
    # Table 3
    tables['table3'] = (
        ["Algorithm", "Accuracy (%)", "Training Time", "Interpretability", "Data Requirement", "Strengths"],
        [
            ["SVM (RBF)", "94.2 - 97.5", "Low", "Low", "Small-Medium", "Small samples, generalization"],
            ["Random Forest", "93.8 - 96.9", "Low", "Medium", "Medium", "Feature importance, robustness"],
            ["1D-CNN", "96.5 - 99.2", "High", "Low", "Large", "Automatic features, raw input"],
            ["LSTM", "95.1 - 98.4", "High", "Low", "Large", "Temporal dependencies, RUL"],
            ["Transformer", "97.3 - 99.5", "Very High", "Medium", "Very Large", "Long-range, attention maps"],
            ["Hybrid CNN-LSTM", "97.8 - 99.6", "High", "Low", "Large", "Spatial + temporal features"],
            ["Transfer Learning", "94.5 - 98.8", "Medium", "Low", "Small (target)", "Cross-domain, few-shot"],
        ]
    )
    
    # Table 4
    tables['table4'] = (
        ["Metric/Challenge", "Description", "Typical Requirement", "Mitigation Strategy"],
        [
            ["Classification Accuracy", "Correct fault identification rate", ">95% for safety-critical", "Ensemble methods, data augmentation"],
            ["False Alarm Rate", "Incorrect fault alerts", "<1% per month", "Threshold optimization, confirmation logic"],
            ["Detection Lead Time", "Time before functional failure", ">30 days for planning", "Sensitive features, trend analysis"],
            ["Computational Latency", "Processing time per inference", "<100 ms for real-time", "Model compression, edge deployment"],
            ["Variable Speed/Load", "Operating condition changes", "Consistent across range", "Order tracking, normalization"],
            ["Data Imbalance", "Fault vs. normal data ratio", "1:100 to 1:10000 typical", "SMOTE, GAN augmentation, focal loss"],
            ["Sensor Degradation", "Measurement drift over time", "Recalibration intervals", "Sensor health monitoring, redundancy"],
            ["Domain Shift", "Training vs. deployment mismatch", "Maintain accuracy >90%", "Domain adaptation, continual learning"],
        ]
    )
    
    return tables


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == '__main__':
    # Define images
    images = {
        'fig1': '/projects/sandbox/AMMAN/signal_figures/Figure_1_Signal_Processing_Framework.png',
        'fig2': '/projects/sandbox/AMMAN/signal_figures/Figure_2_Time_Frequency_Analysis.png',
        'fig3': '/projects/sandbox/AMMAN/signal_figures/Figure_3_ML_Pipeline.png',
        'fig4': '/projects/sandbox/AMMAN/signal_figures/Figure_4_RealTime_Architecture.png',
    }
    
    # Get content and tables
    content = get_chapter_content()
    tables = get_tables()
    
    # Create the document
    output_path = '/projects/sandbox/AMMAN/Chapter_Signal_Processing_Condition_Monitoring.docx'
    create_docx(content, tables, images, output_path)
    
    # Verify
    file_size = os.path.getsize(output_path)
    print(f"File size: {file_size} bytes ({file_size/1024:.1f} KB)")
    print(f"Output: {output_path}")
    
    # Count approximate words
    word_count = 0
    for item in content:
        if item[0] == 'para' and len(item) > 1:
            word_count += len(item[1].split())
    print(f"Approximate word count: {word_count}")
