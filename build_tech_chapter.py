"""
Build a complete Word document (.docx) for the book chapter:
"Technology-Driven Strategies for Competitive Advantage in Modern Business"

This script creates a DOCX file from scratch using Python's zipfile and XML,
without requiring python-docx or any external libraries.

Features:
- ~8300 words of academic content
- 43 references in square brackets [1]-[43] spread throughout
- 4 tables
- 4 figures (PNG images embedded)
- Professional formatting with headings, paragraphs, and styles
"""

import zipfile
import os
import base64
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring

# ============================================================
# DOCX Structure Builder
# ============================================================

class DocxBuilder:
    """Builds a .docx file from scratch using XML."""
    
    def __init__(self):
        self.body_elements = []
        self.images = {}  # rId -> (filename, data)
        self.image_counter = 0
        self.rel_counter = 10  # start relationship IDs at 10
        
    def add_heading(self, text, level=1):
        """Add a heading paragraph."""
        self.body_elements.append(('heading', text, level))
    
    def add_paragraph(self, text, bold=False, italic=False, style=None):
        """Add a normal paragraph."""
        self.body_elements.append(('paragraph', text, bold, italic, style))
    
    def add_image(self, filepath, caption="", width_emu=5400000, height_emu=3600000):
        """Add an image with caption."""
        self.image_counter += 1
        self.rel_counter += 1
        rid = f"rId{self.rel_counter}"
        img_filename = f"image{self.image_counter}.png"
        
        with open(filepath, 'rb') as f:
            img_data = f.read()
        
        self.images[rid] = (img_filename, img_data)
        self.body_elements.append(('image', rid, img_filename, width_emu, height_emu))
        if caption:
            self.body_elements.append(('paragraph', caption, False, True, 'caption'))
    
    def add_table(self, headers, rows, caption=""):
        """Add a table with headers and rows."""
        if caption:
            self.body_elements.append(('paragraph', caption, True, False, 'table_caption'))
        self.body_elements.append(('table', headers, rows))
    
    def add_page_break(self):
        """Add a page break."""
        self.body_elements.append(('pagebreak',))
    
    def _build_document_xml(self):
        """Build the main document.xml content."""
        
        # Namespace declarations
        nsmap = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
            'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
            'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
        }
        
        lines = []
        lines.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
        lines.append('<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                     'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                     'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
                     'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
                     'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">')
        lines.append('<w:body>')
        
        for elem in self.body_elements:
            if elem[0] == 'heading':
                _, text, level = elem
                style_map = {1: 'Heading1', 2: 'Heading2', 3: 'Heading3'}
                style = style_map.get(level, 'Heading1')
                lines.append(f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>')
                lines.append(f'<w:r><w:t xml:space="preserve">{self._escape(text)}</w:t></w:r></w:p>')
                
            elif elem[0] == 'paragraph':
                _, text, bold, italic, style = elem
                lines.append('<w:p>')
                if style == 'caption':
                    lines.append('<w:pPr><w:jc w:val="center"/></w:pPr>')
                elif style == 'table_caption':
                    lines.append('<w:pPr><w:jc w:val="center"/><w:spacing w:before="240" w:after="120"/></w:pPr>')
                else:
                    lines.append('<w:pPr><w:jc w:val="both"/><w:spacing w:after="120" w:line="360" w:lineRule="auto"/></w:pPr>')
                
                rpr = ''
                if bold or italic:
                    rpr = '<w:rPr>'
                    if bold:
                        rpr += '<w:b/>'
                    if italic:
                        rpr += '<w:i/>'
                    rpr += '</w:rPr>'
                
                # Split text on newlines
                parts = text.split('\n')
                for i, part in enumerate(parts):
                    lines.append(f'<w:r>{rpr}<w:t xml:space="preserve">{self._escape(part)}</w:t></w:r>')
                    if i < len(parts) - 1:
                        lines.append('<w:r><w:br/></w:r>')
                
                lines.append('</w:p>')
                
            elif elem[0] == 'image':
                _, rid, filename, w_emu, h_emu = elem
                lines.append('<w:p><w:pPr><w:jc w:val="center"/></w:pPr>')
                lines.append('<w:r><w:drawing>')
                lines.append(f'<wp:inline distT="0" distB="0" distL="0" distR="0">')
                lines.append(f'<wp:extent cx="{w_emu}" cy="{h_emu}"/>')
                lines.append('<wp:docPr id="1" name="Picture"/>')
                lines.append('<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">')
                lines.append(f'<pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="{filename}"/><pic:cNvPicPr/></pic:nvPicPr>')
                lines.append(f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>')
                lines.append(f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>')
                lines.append('<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>')
                lines.append('</pic:pic></a:graphicData></a:graphic>')
                lines.append('</wp:inline></w:drawing></w:r></w:p>')
                
            elif elem[0] == 'table':
                _, headers, rows = elem
                num_cols = len(headers)
                col_width = 9000 // num_cols  # distribute width
                
                lines.append('<w:tbl>')
                lines.append('<w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9000" w:type="dxa"/>')
                lines.append('<w:tblBorders>')
                for border in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                    lines.append(f'<w:{border} w:val="single" w:sz="4" w:space="0" w:color="000000"/>')
                lines.append('</w:tblBorders></w:tblPr>')
                
                # Grid
                lines.append('<w:tblGrid>')
                for _ in range(num_cols):
                    lines.append(f'<w:gridCol w:w="{col_width}"/>')
                lines.append('</w:tblGrid>')
                
                # Header row
                lines.append('<w:tr>')
                for h in headers:
                    lines.append(f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="1B3A6D"/></w:tcPr>')
                    lines.append(f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr>')
                    lines.append(f'<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/></w:rPr>')
                    lines.append(f'<w:t xml:space="preserve">{self._escape(h)}</w:t></w:r></w:p></w:tc>')
                lines.append('</w:tr>')
                
                # Data rows
                for row in rows:
                    lines.append('<w:tr>')
                    for cell in row:
                        lines.append(f'<w:tc><w:p><w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>')
                        lines.append(f'<w:r><w:t xml:space="preserve">{self._escape(str(cell))}</w:t></w:r></w:p></w:tc>')
                    lines.append('</w:tr>')
                
                lines.append('</w:tbl>')
                # Space after table
                lines.append('<w:p><w:pPr><w:spacing w:after="200"/></w:pPr></w:p>')
                
            elif elem[0] == 'pagebreak':
                lines.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
        
        # Section properties (A4, margins)
        lines.append('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>')
        lines.append('<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
                     'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>')
        lines.append('</w:body></w:document>')
        
        return '\n'.join(lines)
    
    def _escape(self, text):
        """Escape XML special characters."""
        return (text.replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
                    .replace('"', '&quot;')
                    .replace("'", '&apos;'))
    
    def save(self, filepath):
        """Save the complete .docx file."""
        
        # Content Types
        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Default Extension="jpeg" ContentType="image/jpeg"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''
        
        # Root relationships
        root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
        
        # Word relationships
        word_rels_lines = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                          '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
                          '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
        
        for rid, (img_filename, _) in self.images.items():
            word_rels_lines.append(
                f'  <Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{img_filename}"/>')
        
        word_rels_lines.append('</Relationships>')
        word_rels = '\n'.join(word_rels_lines)
        
        # Styles
        styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:color w:val="1B3A6D"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="1"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:color w:val="2962A8"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="200" w:after="80"/><w:outlineLvl w:val="2"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="24"/><w:color w:val="34495E"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr><w:tblBorders>
      <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
    </w:tblBorders></w:tblPr>
  </w:style>
</w:styles>'''
        
        # Build document XML
        document_xml = self._build_document_xml()
        
        # Write ZIP
        with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('[Content_Types].xml', content_types)
            zf.writestr('_rels/.rels', root_rels)
            zf.writestr('word/_rels/document.xml.rels', word_rels)
            zf.writestr('word/document.xml', document_xml)
            zf.writestr('word/styles.xml', styles)
            
            # Add images
            for rid, (img_filename, img_data) in self.images.items():
                zf.writestr(f'word/media/{img_filename}', img_data)
        
        print(f"Document saved: {filepath} ({os.path.getsize(filepath):,} bytes)")


# ============================================================
# CHAPTER CONTENT
# ============================================================

def build_chapter():
    doc = DocxBuilder()
    
    # ---- TITLE PAGE ----
    doc.add_heading("Technology-Driven Strategies for Competitive Advantage in Modern Business", 1)
    doc.add_paragraph("")
    doc.add_paragraph("Chapter Authors: [Author Names]", bold=True)
    doc.add_paragraph("Affiliation: [University/Institution Name]")
    doc.add_paragraph("")
    
    # ---- ABSTRACT ----
    doc.add_heading("Abstract", 1)
    doc.add_paragraph(
        "The contemporary business landscape is undergoing unprecedented transformation driven by rapid technological "
        "advancements that fundamentally alter competitive dynamics across industries. This chapter examines the strategic "
        "role of emerging technologies, including artificial intelligence, machine learning, Internet of Things, cloud "
        "computing, blockchain, and digital platforms, in creating and sustaining competitive advantage for modern "
        "organizations. Through a comprehensive analysis of technology-driven business strategies, this work explores "
        "how firms can leverage digital transformation initiatives to achieve operational excellence, enhance customer "
        "experiences, and develop innovative business models. The chapter presents a structured framework for understanding "
        "organizational readiness, technology adoption lifecycles, and strategic alignment between technological capabilities "
        "and business objectives. Furthermore, it addresses critical challenges including cybersecurity risks, ethical "
        "considerations, workforce development, and sustainability imperatives that organizations must navigate in their "
        "digital transformation journeys. The chapter concludes with a strategic roadmap for building future-ready "
        "organizations capable of sustained competitive advantage in an increasingly digital global economy. Four key "
        "frameworks are presented through detailed figures and tables that synthesize current knowledge and provide "
        "actionable guidance for practitioners and scholars alike. The analysis draws upon extensive academic literature "
        "and industry research to provide evidence-based insights that bridge theoretical foundations with practical "
        "applications, offering a comprehensive guide for organizational leaders navigating the complex intersection "
        "of technology strategy and competitive positioning."
    )
    doc.add_paragraph("")
    doc.add_paragraph("Keywords: Digital transformation, competitive advantage, artificial intelligence, emerging technologies, business strategy, Industry 4.0, innovation management, sustainable growth", italic=True)
    
    doc.add_page_break()
    
    # ============================================================
    # SECTION 1
    # ============================================================
    doc.add_heading("1. The Changing Competitive Landscape and the Role of Technology", 1)
    
    # 1.1
    doc.add_heading("1.1 Emerging Trends Shaping Modern Business", 2)
    
    doc.add_paragraph(
        "The global business environment is experiencing a period of extraordinary change, characterized by the convergence "
        "of multiple disruptive forces that are reshaping industries, markets, and competitive dynamics [1]. Digital "
        "transformation has emerged as perhaps the most significant driver of organizational change in the twenty-first "
        "century, fundamentally altering how businesses create, deliver, and capture value [2]. The pace of technological "
        "advancement has accelerated dramatically, with innovations in artificial intelligence, cloud computing, Internet "
        "of Things, and blockchain technology creating new possibilities for business model innovation and operational "
        "transformation [3]. Research indicates that more than 70 percent of organizations globally have either initiated "
        "or are planning significant digital transformation programs, representing collective investment exceeding one "
        "trillion dollars annually across all industries and geographies."
    )
    
    doc.add_paragraph(
        "Globalization continues to expand market boundaries while simultaneously intensifying competition, requiring "
        "organizations to develop capabilities that enable them to compete effectively across diverse geographic and "
        "cultural contexts [4]. The interconnectedness of global markets means that competitive threats can emerge from "
        "unexpected sources, with technology-native firms from emerging economies challenging established incumbents in "
        "developed markets. Customer expectations have evolved significantly, driven by digital experiences that "
        "establish new benchmarks for convenience, personalization, and responsiveness [5]. Modern consumers demand "
        "seamless omnichannel experiences, instant gratification, and personalized interactions that anticipate their "
        "needs and preferences. This shift has created both opportunities and challenges for organizations seeking to "
        "maintain relevance in an increasingly demanding marketplace. The democratization of information through digital "
        "channels has empowered customers with unprecedented access to comparative data, reviews, and alternatives, "
        "fundamentally shifting the balance of power in buyer-seller relationships."
    )
    
    doc.add_paragraph(
        "Market volatility has become a defining characteristic of the contemporary business environment, with "
        "disruptions occurring more frequently and with greater intensity than ever before [6]. The COVID-19 pandemic "
        "demonstrated how rapidly external shocks can transform competitive landscapes, accelerating digital adoption "
        "by several years and fundamentally changing work patterns, consumer behavior, and industry structures [7]. "
        "Organizations that had invested in digital capabilities prior to the pandemic were significantly better "
        "positioned to adapt and thrive, while those with limited digital maturity faced existential challenges. "
        "The pandemic catalyzed remote work adoption, e-commerce acceleration, telemedicine deployment, and "
        "digital entertainment consumption at rates that fundamentally altered the trajectory of multiple industries. "
        "Supply chain disruptions further highlighted the vulnerability of traditional, linear supply networks and "
        "accelerated the adoption of digital supply chain technologies including real-time visibility platforms, "
        "predictive analytics, and autonomous logistics systems."
    )
    
    doc.add_paragraph(
        "Industry 4.0 represents the fourth industrial revolution, characterized by the fusion of physical and digital "
        "systems through cyber-physical systems, Internet of Things, cloud computing, and cognitive computing [8]. This "
        "evolution toward intelligent enterprises involves the integration of smart technologies into manufacturing "
        "processes, supply chains, and business operations, creating interconnected ecosystems that generate and leverage "
        "vast quantities of data for decision-making and optimization. The convergence of operational technology with "
        "information technology creates new possibilities for real-time monitoring, predictive maintenance, and "
        "autonomous optimization that fundamentally transform industrial processes. The emergence of Industry 5.0 "
        "further emphasizes human-machine collaboration, sustainability, and resilience as core principles guiding "
        "technological advancement [9]. This evolution recognizes that technology must serve human needs and societal "
        "welfare rather than simply maximizing efficiency and productivity metrics. As illustrated in Figure 1, the "
        "digital transformation framework encompasses multiple interconnected technology domains that collectively "
        "enable organizational transformation across strategic, operational, and innovation dimensions."
    )
    
    # Insert Figure 1
    doc.add_image(
        '/projects/sandbox/AMMAN/chapter_figures/Figure_1_Digital_Transformation_Framework.png',
        caption="Figure 1. Digital Transformation Framework: Interconnected Technology Domains Enabling Business Transformation",
        width_emu=5000000,
        height_emu=4000000
    )
    
    # 1.2
    doc.add_heading("1.2 Technology as a Source of Competitive Advantage", 2)
    
    doc.add_paragraph(
        "The strategic importance of technological innovation as a source of competitive advantage has been widely "
        "recognized in both academic literature and business practice [10]. Building on Porter's foundational work "
        "on competitive strategy, contemporary researchers have demonstrated that technology-driven differentiation "
        "can create sustainable competitive positions that are difficult for rivals to replicate [11]. Unlike "
        "traditional sources of advantage such as location or natural resources, technological capabilities can "
        "be continuously developed and refined, providing dynamic competitive advantages that evolve with market "
        "conditions. The relationship between technology investment and competitive performance has been empirically "
        "validated across multiple industries, with firms that invest strategically in technology consistently "
        "demonstrating superior financial performance, market share growth, and organizational resilience."
    )
    
    doc.add_paragraph(
        "Technology-driven differentiation manifests in multiple forms, including superior product features, enhanced "
        "service delivery, operational efficiency, and innovative business models [12]. Organizations that effectively "
        "leverage technology can create value propositions that are both distinctive and difficult to imitate, "
        "establishing competitive moats that protect market positions over time. The concept of digital capabilities "
        "as strategic assets has gained prominence, with research demonstrating that firms with superior digital "
        "capabilities consistently outperform their peers across multiple financial metrics [13]. These digital "
        "capabilities encompass not only technical infrastructure and tools but also the organizational routines, "
        "processes, and knowledge systems that enable effective technology utilization. The notion of technological "
        "complementarity is particularly important, as the value of individual technology investments is significantly "
        "enhanced when combined with complementary assets including skilled personnel, supportive organizational "
        "structures, and aligned business processes."
    )
    
    doc.add_paragraph(
        "Building sustainable competitive advantage through digital capabilities requires a holistic approach that "
        "integrates technology investments with organizational strategy, culture, and human capital development [14]. "
        "The resource-based view of the firm suggests that competitive advantage stems from valuable, rare, inimitable, "
        "and non-substitutable resources. In the digital context, these resources include proprietary algorithms, "
        "unique data assets, specialized technical talent, and organizational capabilities for innovation and adaptation. "
        "The dynamic capabilities framework further emphasizes the importance of sensing opportunities, seizing them "
        "through strategic investments, and transforming organizational structures and processes to sustain advantage [15]. "
        "Organizations must develop sensing capabilities that enable them to identify emerging technological opportunities "
        "before competitors, seizing capabilities that allow them to make timely and appropriate investments, and "
        "transforming capabilities that enable them to reconfigure resources and processes as technologies and markets "
        "evolve. This tripartite framework provides a comprehensive lens for understanding how technology creates "
        "sustainable competitive advantage in dynamic environments."
    )
    
    # Table 1
    doc.add_table(
        headers=["Technology Domain", "Competitive Advantage Mechanism", "Strategic Impact", "Implementation Timeline"],
        rows=[
            ["Artificial Intelligence", "Predictive analytics and decision automation", "High - transforms decision-making processes", "12-24 months"],
            ["Cloud Computing", "Scalable infrastructure and cost optimization", "High - enables agility and flexibility", "6-12 months"],
            ["Internet of Things", "Real-time monitoring and data-driven operations", "Medium-High - enhances operational visibility", "12-36 months"],
            ["Blockchain", "Trust, transparency, and process automation", "Medium - disrupts intermediary-based models", "18-36 months"],
            ["Big Data Analytics", "Market intelligence and customer insights", "High - enables evidence-based strategy", "6-18 months"],
            ["Digital Platforms", "Network effects and ecosystem orchestration", "Very High - creates winner-take-all dynamics", "12-36 months"],
            ["Robotic Process Automation", "Process efficiency and error reduction", "Medium - reduces operational costs", "3-12 months"],
            ["Edge Computing", "Low-latency processing and distributed intelligence", "Medium-High - enables real-time applications", "12-24 months"],
        ],
        caption="Table 1. Technology Domains and Their Competitive Advantage Mechanisms"
    )
    
    doc.add_paragraph(
        "Table 1 presents a comprehensive mapping of key technology domains to their respective competitive advantage "
        "mechanisms, strategic impact levels, and typical implementation timelines. This framework provides practitioners "
        "with a structured approach for prioritizing technology investments based on organizational needs and strategic "
        "objectives. The varying implementation timelines highlight the importance of phased technology adoption strategies "
        "that balance quick wins with longer-term transformational initiatives [16]. Organizations should use this "
        "framework as a starting point for technology portfolio management, recognizing that the specific impact and "
        "timeline for any given technology will vary based on industry context, organizational maturity, and strategic "
        "alignment. The interrelationships between these technology domains are equally important, as investments in "
        "foundational technologies such as cloud computing and big data analytics create enabling platforms that "
        "accelerate the deployment and enhance the value of more advanced technologies including artificial intelligence "
        "and blockchain applications. A portfolio approach that combines quick-return investments in robotic process "
        "automation and cloud migration with longer-term strategic investments in AI and platform development provides "
        "the optimal balance of near-term value creation and long-term competitive positioning."
    )
    
    # 1.3
    doc.add_heading("1.3 Organizational Readiness for Technological Change", 2)
    
    doc.add_paragraph(
        "Assessing organizational readiness for technological change is a critical prerequisite for successful digital "
        "transformation initiatives [17]. Technological maturity assessments evaluate an organization's current state "
        "across multiple dimensions, including infrastructure capabilities, data management practices, digital skills, "
        "and innovation processes. Research indicates that organizations with higher levels of technological maturity "
        "are significantly more likely to achieve positive outcomes from digital transformation investments [18]. "
        "Maturity models typically define progressive levels from initial ad-hoc technology use through managed, "
        "defined, and optimized stages, with each level characterized by specific capabilities, processes, and "
        "outcomes. Organizations must conduct honest self-assessments of their current maturity levels to develop "
        "realistic transformation roadmaps that account for existing capabilities and gaps."
    )
    
    doc.add_paragraph(
        "Developing a culture of innovation and adaptability is essential for organizations seeking to leverage "
        "technology for competitive advantage. Innovation culture encompasses organizational values, norms, and "
        "practices that encourage experimentation, tolerate failure, and reward creative problem-solving [19]. "
        "Organizations with strong innovation cultures are better equipped to identify and capitalize on technological "
        "opportunities, adapt to changing market conditions, and sustain competitive advantages over time. The "
        "relationship between organizational culture and technology adoption success has been extensively documented, "
        "with studies consistently showing that cultural factors are among the strongest predictors of digital "
        "transformation outcomes [20]. Cultural transformation often represents the most challenging aspect of "
        "digital transformation, requiring sustained leadership attention, consistent messaging, aligned incentive "
        "systems, and visible commitment to new ways of working. Organizations that treat digital transformation "
        "as purely a technology initiative without addressing cultural dimensions consistently underperform those "
        "that adopt holistic transformation approaches encompassing people, processes, and technology simultaneously."
    )
    
    doc.add_paragraph(
        "Leadership plays a pivotal role in driving technological change, with senior executives responsible for "
        "articulating digital vision, allocating resources, and creating conditions that enable innovation [21]. "
        "The concept of digital leadership has emerged as a distinct competency domain, encompassing skills such as "
        "technology literacy, data-driven decision-making, agile management, and ecosystem thinking. Effective "
        "digital leaders must balance multiple tensions: maintaining operational stability while driving transformation, "
        "investing for the long term while delivering short-term results, and promoting standardization while "
        "enabling experimentation. Employee skills and change management strategies are equally critical, as the "
        "success of technology implementations ultimately depends on the ability of people to adopt and effectively "
        "utilize new tools and processes. Comprehensive change management approaches that combine communication, "
        "training, support, and reinforcement are essential for achieving the adoption rates necessary to realize "
        "the full value of technology investments. The digital transformation framework illustrated in Figure 1 "
        "demonstrates how leadership, culture, and capabilities must align with technological investments to "
        "achieve strategic objectives across all organizational dimensions."
    )
    
    doc.add_page_break()
    
    # ============================================================
    # SECTION 2
    # ============================================================
    doc.add_heading("2. Harnessing Emerging Technologies for Business Transformation", 1)
    
    # 2.1
    doc.add_heading("2.1 Artificial Intelligence, Machine Learning, and Intelligent Automation", 2)
    
    doc.add_paragraph(
        "Artificial intelligence has rapidly evolved from a theoretical concept to a practical business tool that "
        "is transforming industries across the global economy [22]. AI-enabled decision-making leverages machine "
        "learning algorithms, natural language processing, and computer vision to augment human judgment, automate "
        "complex analyses, and generate insights that would be impossible to derive through traditional analytical "
        "methods. Predictive analytics, powered by advanced machine learning models, enables organizations to "
        "anticipate market trends, customer behaviors, and operational disruptions with unprecedented accuracy [23]. "
        "The economic impact of AI is substantial and growing, with estimates suggesting that AI could contribute "
        "up to 15.7 trillion dollars to the global economy by 2030, encompassing both productivity improvements "
        "and consumption-side effects. Organizations across sectors including healthcare, finance, manufacturing, "
        "retail, and logistics are deploying AI systems to enhance decision quality, reduce costs, and create "
        "entirely new value propositions that differentiate their offerings from competitors."
    )
    
    doc.add_paragraph(
        "Intelligent process automation represents the convergence of artificial intelligence with robotic process "
        "automation, creating systems capable of handling complex, unstructured tasks that previously required human "
        "cognitive abilities [24]. Unlike traditional automation that follows rigid rule-based processes, intelligent "
        "automation can learn from experience, adapt to changing conditions, and handle exceptions autonomously. "
        "This capability has profound implications for operational efficiency, enabling organizations to reduce costs, "
        "improve quality, and accelerate process execution while freeing human workers to focus on higher-value "
        "creative and strategic activities. The integration of computer vision, natural language understanding, "
        "and machine learning with process automation creates cognitive automation capabilities that can process "
        "invoices, analyze contracts, classify documents, respond to customer inquiries, and perform complex "
        "compliance checks with minimal human intervention. Industry research suggests that intelligent automation "
        "can reduce process costs by 40 to 75 percent while simultaneously improving accuracy rates and processing "
        "speeds, representing one of the highest-return technology investments available to modern organizations."
    )
    
    doc.add_paragraph(
        "Generative AI represents the latest frontier in artificial intelligence, with large language models and "
        "multimodal AI systems opening entirely new possibilities for business innovation [25]. These systems can "
        "generate text, code, images, and other creative outputs that were previously the exclusive domain of human "
        "intelligence. The business applications of generative AI span content creation, software development, "
        "product design, customer service, and strategic planning, with early adopters reporting significant "
        "productivity improvements and cost reductions. The rapid advancement of generative AI capabilities has "
        "created both excitement and concern across industries, with organizations racing to identify and capture "
        "value from these technologies while managing associated risks including accuracy, bias, intellectual "
        "property, and workforce displacement. As shown in Figure 2, the technology adoption lifecycle "
        "demonstrates how AI technologies progress through distinct phases of maturity, with corresponding "
        "implications for competitive advantage timing and strategic positioning."
    )
    
    # Insert Figure 2
    doc.add_image(
        '/projects/sandbox/AMMAN/chapter_figures/Figure_2_Technology_Adoption_Maturity.png',
        caption="Figure 2. Technology Adoption S-Curve and Competitive Advantage Window: The relationship between technology maturity and competitive differentiation potential",
        width_emu=5000000,
        height_emu=3800000
    )
    
    doc.add_paragraph(
        "Figure 2 illustrates the technology adoption S-curve alongside the competitive advantage window, demonstrating "
        "that maximum competitive differentiation occurs during the growth phase when early adopters gain advantages "
        "before technology becomes commoditized. This insight has significant implications for technology investment "
        "timing and strategic positioning [26]. Organizations that invest too early may bear excessive costs and risks "
        "associated with immature technologies, while those that invest too late find that the technology has become "
        "widely available and no longer provides differentiation. The strategic window for competitive advantage "
        "is relatively narrow for each technology wave, requiring organizations to develop sophisticated capabilities "
        "for timing their investments to maximize competitive impact. Understanding where specific technologies "
        "sit on the adoption curve enables more informed investment decisions and helps organizations allocate "
        "resources between proven technologies for near-term value and emerging technologies for future positioning."
    )
    
    # 2.2
    doc.add_heading("2.2 Internet of Things, Cloud Computing, and Big Data", 2)
    
    doc.add_paragraph(
        "The Internet of Things ecosystem encompasses billions of connected devices generating continuous streams "
        "of data that provide unprecedented visibility into physical processes, customer behaviors, and environmental "
        "conditions [27]. Connected products transform traditional offerings into intelligent systems capable of "
        "self-monitoring, predictive maintenance, and adaptive optimization. Smart operations leverage IoT sensor "
        "data to optimize manufacturing processes, logistics networks, and facility management in real-time, "
        "creating significant operational efficiencies and competitive advantages. The proliferation of IoT devices "
        "is creating what some researchers term the physical internet, a network of interconnected physical objects "
        "that communicate, collaborate, and coordinate autonomously. By 2025, an estimated 75 billion IoT devices "
        "will be deployed globally, generating data volumes that dwarf current capabilities and creating unprecedented "
        "opportunities for data-driven optimization and innovation across virtually every industry sector. The "
        "strategic implications of IoT extend well beyond operational efficiency to encompass entirely new business "
        "models based on outcome-based pricing, predictive services, and autonomous optimization that fundamentally "
        "redefine the relationship between products, services, and customer value."
    )
    
    doc.add_paragraph(
        "Cloud computing has fundamentally transformed the economics of IT infrastructure, enabling organizations "
        "of all sizes to access enterprise-grade computing resources on a pay-as-you-go basis [28]. Cloud platforms "
        "provide the scalable foundation upon which digital transformation initiatives are built, offering computing "
        "power, storage, networking, and specialized services including AI/ML platforms, database management, and "
        "analytics tools. The shift from capital expenditure to operational expenditure models has democratized "
        "access to advanced technology capabilities, enabling startups and small enterprises to compete with "
        "established incumbents on more equal footing [29]. Multi-cloud and hybrid cloud strategies have emerged "
        "as dominant approaches, enabling organizations to leverage best-of-breed capabilities from multiple "
        "providers while maintaining control over sensitive workloads and ensuring regulatory compliance. The "
        "cloud-native development paradigm, incorporating microservices, containers, and serverless computing, "
        "has fundamentally changed how applications are designed, deployed, and scaled, enabling unprecedented "
        "levels of agility and resilience in software delivery."
    )
    
    doc.add_paragraph(
        "Big data analytics represents the analytical backbone of digital transformation, transforming raw data "
        "into actionable intelligence that drives strategic decision-making [30]. The combination of IoT-generated "
        "data, cloud computing infrastructure, and advanced analytics algorithms creates powerful capabilities for "
        "market intelligence, customer insights, and operational optimization. Organizations that effectively "
        "harness big data analytics can identify patterns, predict outcomes, and optimize processes at scales and "
        "speeds that were previously unattainable, creating significant competitive advantages in data-rich "
        "industries. The evolution from descriptive analytics through diagnostic and predictive to prescriptive "
        "analytics represents a maturation journey that progressively increases the strategic value of data assets. "
        "Advanced analytics techniques including deep learning, reinforcement learning, and graph analytics enable "
        "organizations to extract insights from complex, multi-dimensional datasets that resist traditional "
        "analytical approaches, opening new frontiers for competitive intelligence and strategic decision-making."
    )
    
    # Table 2
    doc.add_table(
        headers=["Technology", "Key Business Applications", "Data Volume Impact", "ROI Timeline"],
        rows=[
            ["IoT Sensors", "Predictive maintenance, asset tracking, quality control", "Generates 2.5 quintillion bytes/day globally", "12-18 months"],
            ["Cloud Platforms (IaaS)", "Scalable computing, disaster recovery, global deployment", "Enables processing of petabyte-scale datasets", "3-6 months"],
            ["Cloud Platforms (PaaS)", "Application development, AI/ML services, DevOps", "Accelerates development cycles by 40-60%", "6-12 months"],
            ["Big Data Analytics", "Customer segmentation, fraud detection, supply chain optimization", "Processes structured and unstructured data at scale", "6-18 months"],
            ["Edge Computing", "Real-time processing, autonomous vehicles, AR/VR", "Reduces latency to sub-millisecond levels", "12-24 months"],
            ["Data Lakes", "Centralized data storage, cross-functional analytics", "Consolidates enterprise data from disparate sources", "6-12 months"],
        ],
        caption="Table 2. IoT, Cloud Computing, and Big Data: Business Applications and Impact Assessment"
    )
    
    # 2.3
    doc.add_heading("2.3 Blockchain, Digital Platforms, and Advanced Technologies", 2)
    
    doc.add_paragraph(
        "Blockchain technology offers transformative potential for business processes that require trust, transparency, "
        "and security without reliance on centralized intermediaries [31]. Distributed ledger technology enables "
        "tamper-proof record-keeping, automated contract execution through smart contracts, and decentralized "
        "governance mechanisms that can revolutionize supply chain management, financial services, healthcare, "
        "and numerous other sectors. The immutability and transparency of blockchain records create new possibilities "
        "for compliance, auditing, and stakeholder trust that address longstanding challenges in multi-party "
        "business transactions. Enterprise blockchain applications have moved beyond initial cryptocurrency "
        "applications to encompass supply chain provenance tracking, cross-border payments, digital identity "
        "management, intellectual property protection, and decentralized autonomous organizations that operate "
        "without traditional hierarchical governance structures. The tokenization of real-world assets including "
        "real estate, art, intellectual property, and carbon credits represents an emerging application of "
        "blockchain technology that could fundamentally reshape capital markets and ownership structures."
    )
    
    doc.add_paragraph(
        "Digital platforms have emerged as dominant business models in the modern economy, creating value through "
        "the orchestration of multi-sided ecosystems that connect producers and consumers [32]. Platform-based "
        "competition operates according to fundamentally different dynamics than traditional pipeline businesses, "
        "with network effects, data accumulation, and ecosystem lock-in creating powerful competitive advantages "
        "for platform leaders. The platform economy has produced some of the most valuable companies in history, "
        "demonstrating the enormous value creation potential of ecosystem-based business models [33]. Platform "
        "strategies enable organizations to scale rapidly by leveraging external resources and capabilities, "
        "creating virtuous cycles where increased participation generates greater value for all ecosystem members. "
        "The distinction between innovation platforms, transaction platforms, and hybrid platforms provides a "
        "useful typology for understanding different approaches to platform-based competition and the specific "
        "strategic considerations each entails. Successful platform strategies require careful attention to "
        "governance mechanisms that balance openness with quality control, pricing structures that attract both "
        "sides of the market, and trust-building mechanisms that encourage participation and reduce transaction "
        "friction across the ecosystem."
    )
    
    doc.add_paragraph(
        "Beyond these established technologies, a new wave of emerging innovations promises to further transform "
        "competitive dynamics in the coming decade. Quantum computing offers the potential for exponential increases "
        "in computational power for specific problem classes, with implications for optimization, cryptography, "
        "and drug discovery [34]. Extended reality technologies, including virtual reality, augmented reality, "
        "and mixed reality, are creating new channels for customer engagement, training, and collaboration. "
        "Biotechnology and nanotechnology advances are expanding the boundaries of what is possible in healthcare, "
        "materials science, and manufacturing, creating entirely new industry categories and competitive arenas. "
        "The convergence of these technologies with artificial intelligence creates multiplicative effects, as "
        "AI enhances the capabilities of other technologies while those technologies generate the data and "
        "computational substrates that advance AI capabilities. The emerging technologies ecosystem depicted "
        "in Figure 3 illustrates how these technologies integrate across three layers to create business "
        "capabilities that ultimately drive strategic outcomes for organizations."
    )
    
    # Insert Figure 3
    doc.add_image(
        '/projects/sandbox/AMMAN/chapter_figures/Figure_3_Emerging_Tech_Ecosystem.png',
        caption="Figure 3. AI and Emerging Technologies Business Integration Ecosystem: Three-layer model showing technology foundations, business capabilities, and strategic outcomes",
        width_emu=5000000,
        height_emu=4200000
    )
    
    doc.add_page_break()
    
    # ============================================================
    # SECTION 3
    # ============================================================
    doc.add_heading("3. Technology-Driven Strategies for Sustainable Competitive Advantage", 1)
    
    # 3.1
    doc.add_heading("3.1 Digital Innovation and Business Model Transformation", 2)
    
    doc.add_paragraph(
        "Digital innovation encompasses the development of technology-enabled products, services, and processes "
        "that create new value for customers and stakeholders [35]. Unlike incremental improvements to existing "
        "offerings, digital innovation often involves fundamental rethinking of value propositions, customer "
        "interactions, and revenue models. The most successful digital innovators combine deep technological "
        "expertise with customer empathy and business acumen, creating solutions that address unmet needs in "
        "ways that were previously impossible or impractical. The distinction between sustaining and disruptive "
        "digital innovation is particularly relevant for strategic planning, as sustaining innovations improve "
        "existing products along established performance trajectories while disruptive innovations create entirely "
        "new value networks that eventually displace established approaches. Innovation ecosystems that connect "
        "startups, corporations, universities, and government agencies are increasingly important for generating "
        "breakthrough innovations that no single actor could achieve independently, creating collaborative "
        "networks that accelerate the pace of technology-driven value creation."
    )
    
    doc.add_paragraph(
        "Digital business models represent a paradigm shift from traditional approaches to value creation and "
        "capture. Subscription-based models, freemium strategies, marketplace models, and data-driven business "
        "models have disrupted established industries and created entirely new market categories [36]. Platform-based "
        "competition has proven particularly powerful, with network effects enabling rapid scaling and creating "
        "winner-take-most dynamics in many digital markets. Organizations that successfully transition to digital "
        "business models often achieve superior growth rates, customer retention, and profitability compared to "
        "those relying on traditional approaches. The economics of digital business models differ fundamentally "
        "from physical business models, with near-zero marginal costs, rapid scalability, and data-driven "
        "learning effects creating powerful advantages for firms that achieve critical mass. Business model "
        "experimentation, enabled by digital tools and lean methodologies, allows organizations to test multiple "
        "value propositions simultaneously and rapidly iterate toward optimal configurations. The transition from "
        "product-centric to service-centric and experience-centric business models, often facilitated by IoT "
        "connectivity and data analytics, represents one of the most significant strategic shifts enabled by "
        "digital technologies, transforming one-time transactions into ongoing relationships that generate "
        "recurring revenue streams and deeper customer engagement."
    )
    
    doc.add_paragraph(
        "Continuous innovation and organizational agility are essential for sustaining competitive advantage in "
        "rapidly evolving digital markets [37]. Agile methodologies, design thinking, and lean startup approaches "
        "provide frameworks for rapid experimentation, iterative development, and customer-centric innovation that "
        "enable organizations to respond quickly to changing market conditions and emerging opportunities. The "
        "integration of these approaches with advanced technologies such as AI-driven market intelligence and "
        "automated testing creates powerful innovation capabilities that accelerate time-to-market and reduce "
        "the costs of experimentation. Organizations that cultivate innovation agility can explore multiple "
        "strategic options simultaneously, learn rapidly from market feedback, and pivot effectively when "
        "initial approaches prove suboptimal. The concept of innovation portfolios, which balance investments "
        "across core innovation, adjacent innovation, and transformational innovation, provides a structured "
        "approach for managing risk while pursuing breakthrough opportunities. The three-layer ecosystem model "
        "shown in Figure 3 demonstrates how technology foundations enable business capabilities that ultimately "
        "drive strategic outcomes including competitive advantage, operational excellence, and sustainable growth."
    )
    
    # 3.2
    doc.add_heading("3.2 Customer-Centric Digital Transformation", 2)
    
    doc.add_paragraph(
        "Personalization through data and AI represents one of the most impactful applications of emerging "
        "technologies for competitive advantage. Advanced machine learning algorithms can analyze vast quantities "
        "of customer data to generate individualized recommendations, communications, and experiences that "
        "significantly improve engagement, conversion, and loyalty [38]. The sophistication of personalization "
        "capabilities has advanced rapidly, moving from simple rule-based segmentation to real-time, context-aware "
        "experiences that adapt dynamically to individual behaviors and preferences. Hyper-personalization "
        "leverages real-time behavioral data, contextual signals, and predictive models to deliver experiences "
        "that are tailored not just to customer segments but to individual moments within the customer journey. "
        "Research demonstrates that organizations deploying advanced personalization achieve revenue increases of "
        "10 to 30 percent compared to those using basic segmentation approaches, representing a significant "
        "competitive advantage in customer-facing industries."
    )
    
    doc.add_paragraph(
        "Digital customer experience encompasses all interactions between customers and organizations across "
        "digital channels, including websites, mobile applications, social media, chatbots, and emerging "
        "interfaces such as voice assistants and augmented reality [39]. Creating superior digital customer "
        "experiences requires deep understanding of customer journeys, pain points, and preferences, combined "
        "with the technical capability to deliver seamless, intuitive, and emotionally engaging interactions "
        "across all touchpoints. Organizations that excel in digital customer experience consistently achieve "
        "higher customer satisfaction, Net Promoter Scores, and lifetime value metrics compared to industry peers. "
        "The design of digital experiences must account for the full spectrum of customer needs including "
        "functional requirements, emotional needs, and social dimensions, creating holistic experiences that "
        "build deep emotional connections between customers and brands. Customer journey orchestration platforms "
        "that coordinate interactions across channels in real-time represent a significant advancement over "
        "traditional multi-channel approaches, enabling truly seamless experiences regardless of how customers "
        "choose to interact with an organization."
    )
    
    doc.add_paragraph(
        "Technology-enabled marketing and relationship management leverage AI, big data analytics, and marketing "
        "automation platforms to optimize customer acquisition, retention, and growth [40]. Predictive customer "
        "analytics enables proactive engagement strategies that anticipate customer needs and prevent churn, while "
        "AI-powered content generation and optimization improve marketing effectiveness at scale. The integration "
        "of customer data platforms with AI-driven decision engines creates closed-loop systems that continuously "
        "learn and improve, delivering compounding returns on customer relationship investments over time. "
        "Attribution modeling powered by machine learning enables organizations to understand the true impact "
        "of marketing investments across complex multi-touch customer journeys, optimizing resource allocation "
        "for maximum return. The convergence of marketing technology with customer experience technology is "
        "creating unified platforms that manage the entire customer lifecycle from awareness through advocacy, "
        "enabling organizations to deliver consistent, personalized value at every stage of the relationship."
    )
    
    # Table 3
    doc.add_table(
        headers=["Strategy", "Technology Enablers", "Customer Impact", "Competitive Differentiation"],
        rows=[
            ["Hyper-personalization", "AI/ML, real-time analytics, customer data platforms", "35-40% increase in engagement", "High - creates unique customer experiences"],
            ["Omnichannel integration", "Cloud platforms, APIs, microservices", "25% improvement in satisfaction", "Medium-High - reduces friction across channels"],
            ["Predictive service", "Machine learning, IoT sensors, digital twins", "50% reduction in service issues", "High - shifts from reactive to proactive"],
            ["Conversational AI", "NLP, large language models, knowledge graphs", "60% faster resolution times", "Medium - becoming table stakes"],
            ["Immersive experiences", "AR/VR, 3D modeling, spatial computing", "2x engagement duration", "High - creates memorable interactions"],
            ["Voice commerce", "Speech recognition, NLU, smart speakers", "15-20% new channel revenue", "Medium - growing adoption"],
            ["Emotion AI", "Computer vision, sentiment analysis, biometrics", "30% improvement in empathy scores", "High - deeply personalizes interactions"],
        ],
        caption="Table 3. Customer-Centric Digital Strategies: Technology Enablers and Impact Metrics"
    )
    
    # 3.3
    doc.add_heading("3.3 Operational Excellence and Sustainable Growth", 2)
    
    doc.add_paragraph(
        "Smart manufacturing represents the application of Industry 4.0 principles to production processes, "
        "creating intelligent, connected, and adaptive manufacturing systems that optimize performance across "
        "multiple dimensions simultaneously [41]. Digital twins, which create virtual replicas of physical "
        "assets and processes, enable predictive maintenance, process simulation, and continuous optimization "
        "that significantly reduce downtime, waste, and quality defects. The integration of AI with manufacturing "
        "execution systems creates autonomous production environments capable of self-optimization and adaptive "
        "quality control. Advanced manufacturing technologies including additive manufacturing, collaborative "
        "robotics, and autonomous guided vehicles are further transforming production capabilities, enabling "
        "mass customization, distributed manufacturing, and flexible production systems that can rapidly adapt "
        "to changing demand patterns. The concept of lights-out manufacturing, where production facilities "
        "operate autonomously with minimal human intervention, is becoming increasingly feasible as AI and "
        "robotics technologies mature. The integration of digital thread technologies that connect design, "
        "engineering, production, and service data creates unprecedented traceability and enables optimization "
        "across the entire product lifecycle from concept through end-of-life recycling and disposal."
    )
    
    doc.add_paragraph(
        "Intelligent supply chains leverage IoT, AI, and blockchain technologies to create end-to-end visibility, "
        "predictive capabilities, and automated decision-making across complex global supply networks. Technology-enabled "
        "resource optimization extends beyond manufacturing to encompass energy management, workforce planning, "
        "financial resource allocation, and environmental impact minimization. As outlined in Table 2, the convergence "
        "of IoT sensors, cloud platforms, and big data analytics provides the technological foundation for these "
        "intelligent supply chain capabilities. Organizations that achieve operational "
        "excellence through technology integration typically realize 20 to 40 percent improvements in efficiency "
        "metrics while simultaneously enhancing quality, flexibility, and sustainability performance. Supply chain "
        "digital twins enable scenario planning and risk assessment that significantly improve organizational "
        "resilience, allowing firms to simulate disruptions and develop contingency plans before events occur. "
        "The integration of demand sensing algorithms with supply planning systems enables organizations to "
        "respond to market changes in near real-time, reducing inventory costs while improving service levels. "
        "Autonomous logistics systems incorporating self-driving vehicles, drone delivery, and robotic warehousing "
        "are poised to transform the economics and speed of physical distribution, creating new competitive "
        "advantages for organizations that successfully deploy these technologies at scale."
    )
    
    doc.add_paragraph(
        "Green technologies and sustainability-oriented innovation represent an increasingly important dimension "
        "of technology-driven competitive advantage [42]. As stakeholder expectations regarding environmental "
        "and social responsibility intensify, organizations that leverage technology to reduce environmental "
        "impact, improve resource efficiency, and contribute to sustainability goals are gaining competitive "
        "advantages in talent attraction, customer loyalty, regulatory compliance, and access to capital. "
        "The convergence of digital transformation and sustainability creates powerful synergies, with "
        "technologies such as AI-optimized energy management, IoT-enabled circular economy systems, and "
        "blockchain-verified sustainability credentials simultaneously improving business performance and "
        "environmental outcomes. Carbon footprint tracking powered by IoT and analytics enables organizations "
        "to measure, report, and reduce emissions across their value chains with unprecedented precision. "
        "Sustainable technology strategies are increasingly viewed not merely as compliance requirements but "
        "as sources of innovation and competitive differentiation that create long-term value for shareholders "
        "while contributing to broader societal welfare and environmental stewardship."
    )
    
    doc.add_page_break()
    
    # ============================================================
    # SECTION 4
    # ============================================================
    doc.add_heading("4. Future Readiness, Challenges, and Strategic Perspectives", 1)
    
    # 4.1
    doc.add_heading("4.1 Managing Risks and Challenges of Technological Adoption", 2)
    
    doc.add_paragraph(
        "Cybersecurity threats represent one of the most significant risks associated with digital transformation "
        "and technology adoption. As organizations become more digitally connected and data-dependent, their "
        "attack surfaces expand correspondingly, creating vulnerabilities that can be exploited by increasingly "
        "sophisticated threat actors [43]. The global cost of cybercrime is projected to exceed ten trillion "
        "dollars annually by 2025, encompassing data breaches, ransomware attacks, intellectual property theft, "
        "and business disruption. Effective cybersecurity requires a comprehensive approach that combines "
        "technological controls, governance frameworks, employee awareness, and incident response capabilities. "
        "The increasing sophistication of cyber threats, including AI-powered attacks, supply chain compromises, "
        "and nation-state sponsored operations, demands continuous evolution of defensive capabilities and "
        "proactive threat intelligence. Zero-trust security architectures that verify every access request "
        "regardless of source location are replacing traditional perimeter-based approaches that are inadequate "
        "for cloud-native, distributed computing environments. The integration of cybersecurity considerations "
        "into technology strategy from the outset, rather than treating security as an afterthought, is essential "
        "for building systems that are both innovative and resilient against evolving threat landscapes."
    )
    
    doc.add_paragraph(
        "Privacy and data governance have become critical concerns as organizations collect, process, and leverage "
        "increasingly vast quantities of personal and sensitive data. Regulatory frameworks such as the General "
        "Data Protection Regulation (GDPR), California Consumer Privacy Act (CCPA), and emerging regulations "
        "globally impose significant obligations on organizations regarding data collection, processing, storage, "
        "and sharing. Organizations must develop robust data governance frameworks that ensure compliance while "
        "enabling the analytical capabilities necessary for competitive advantage. The tension between data "
        "utilization for business value and privacy protection requires careful balancing through privacy-by-design "
        "principles, data minimization, and transparent consent mechanisms. Data ethics has emerged as a distinct "
        "discipline that goes beyond legal compliance to address broader questions of fairness, transparency, and "
        "societal impact. Organizations that proactively adopt ethical data practices can build trust advantages "
        "that differentiate them in markets where consumers are increasingly concerned about how their personal "
        "information is collected, used, and protected. The emergence of privacy-enhancing technologies including "
        "federated learning, differential privacy, homomorphic encryption, and secure multi-party computation "
        "offers promising approaches for enabling data-driven analytics while preserving individual privacy rights, "
        "potentially resolving the tension between data utilization and privacy protection that has challenged "
        "organizations since the advent of large-scale data collection."
    )
    
    doc.add_paragraph(
        "Ethical issues surrounding emerging technologies have gained prominence as AI systems, surveillance "
        "technologies, and automated decision-making increasingly impact individuals and communities. Algorithmic "
        "bias, transparency, accountability, and fairness are critical considerations that organizations must "
        "address in their technology deployments. The responsible use of AI and other emerging technologies "
        "requires ethical frameworks, governance structures, and oversight mechanisms that ensure technology "
        "serves human welfare and societal benefit rather than causing harm or perpetuating inequalities. "
        "Financial, technological, and organizational barriers to adoption further complicate the landscape, "
        "with many organizations struggling to justify the significant investments required for digital "
        "transformation while managing the organizational change and talent development challenges that "
        "accompany technology adoption. The digital divide between organizations with resources to invest "
        "in advanced technologies and those without creates growing competitive asymmetries that policy makers "
        "and industry leaders must address to ensure broad-based economic participation and prosperity. "
        "Organizations that proactively establish responsible AI governance frameworks, including ethics review "
        "boards, algorithmic audit processes, and stakeholder engagement mechanisms, can build reputational "
        "advantages while mitigating the growing regulatory and legal risks associated with AI deployment "
        "in sensitive domains."
    )
    
    # 4.2
    doc.add_heading("4.2 Building Future-Ready Organizations", 2)
    
    doc.add_paragraph(
        "Developing digital competencies and workforce capabilities is essential for organizations seeking to "
        "sustain competitive advantage in an increasingly technology-driven economy. The skills gap between "
        "organizational needs and available talent represents a significant constraint on digital transformation "
        "progress, with research indicating that over 70 percent of organizations cite talent shortages as a "
        "primary barrier to achieving digital transformation objectives. Addressing this challenge requires "
        "comprehensive approaches that combine recruitment of specialized talent, upskilling of existing workforces, "
        "and organizational learning systems that continuously develop capabilities aligned with evolving technology "
        "landscapes. Digital literacy must extend beyond technical specialists to encompass all organizational "
        "members, with differentiated competency frameworks that define appropriate skill levels for different "
        "roles and functions. The concept of continuous learning organizations, where skill development is "
        "embedded in daily work rather than confined to periodic training events, is increasingly recognized "
        "as essential for keeping pace with the rate of technological change. T-shaped skill profiles that "
        "combine deep expertise in one domain with broad understanding across multiple technology and business "
        "areas are increasingly valued as they enable effective collaboration across functional boundaries "
        "and facilitate the integration of diverse perspectives necessary for complex technology-driven innovation."
    )
    
    doc.add_paragraph(
        "Agile leadership and innovation-oriented organizational culture are foundational elements of future-ready "
        "organizations. Leaders must cultivate environments that embrace experimentation, tolerate productive "
        "failure, and empower distributed decision-making while maintaining strategic coherence and operational "
        "discipline. The balance between exploration of new opportunities and exploitation of existing capabilities "
        "is particularly challenging in rapidly changing technological environments, requiring ambidextrous "
        "organizational designs that simultaneously pursue incremental improvement and breakthrough innovation. "
        "Organizational structures are evolving from traditional hierarchies toward network-based, team-centric "
        "designs that enable faster decision-making, cross-functional collaboration, and adaptive resource "
        "allocation. As demonstrated in Table 3, customer-centric digital strategies require organizations to "
        "develop capabilities spanning hyper-personalization, omnichannel integration, and conversational AI, "
        "all of which demand agile leadership approaches that can coordinate cross-functional technology "
        "deployment at pace. The role of middle management is being transformed from supervisory and coordinative functions "
        "toward coaching, facilitation, and innovation sponsorship as organizations flatten hierarchies and "
        "distribute authority closer to the point of value creation and customer interaction. Psychological safety, "
        "where team members feel comfortable taking interpersonal risks without fear of punishment or humiliation, "
        "has been identified as a critical enabler of innovation and learning in technology-driven organizations, "
        "as it encourages the experimentation and knowledge sharing that drive continuous improvement and "
        "breakthrough discoveries."
    )
    
    doc.add_paragraph(
        "Strategic partnerships, ecosystems, and continuous learning represent critical enablers of future "
        "readiness. No single organization possesses all the capabilities, technologies, and resources necessary "
        "to compete effectively across all dimensions of digital transformation. Ecosystem strategies enable "
        "organizations to access complementary capabilities through partnerships, alliances, and platform "
        "participation, creating collective advantages that exceed what any individual firm could achieve alone. "
        "Open innovation approaches that leverage external knowledge sources, startup partnerships, and academic "
        "collaborations accelerate the pace of innovation while reducing the costs and risks associated with "
        "internal research and development. Corporate venture capital programs enable established firms to "
        "participate in emerging technology developments while maintaining strategic optionality. Innovation "
        "hubs, accelerator programs, and technology sandboxes provide structured environments for exploring "
        "emerging technologies in controlled settings before committing to full-scale deployment. As depicted "
        "in the technology adoption maturity model in Figure 2, organizations must continuously monitor the "
        "technology landscape and adjust their strategies as technologies progress through different lifecycle "
        "stages, ensuring that investment timing aligns with strategic objectives and market readiness."
    )
    
    # Table 4
    doc.add_table(
        headers=["Dimension", "Current State (Typical)", "Future-Ready Target", "Key Actions Required"],
        rows=[
            ["Digital Skills", "Basic digital literacy in 40% of workforce", "Advanced digital capabilities in 80%+ of workforce", "Continuous learning programs, digital academies, skill assessments"],
            ["Innovation Culture", "Risk-averse, hierarchical decision-making", "Experimentation-friendly, distributed innovation", "Leadership modeling, incentive alignment, failure tolerance"],
            ["Technology Infrastructure", "Legacy systems with limited integration", "Cloud-native, API-first, composable architecture", "Phased modernization, technical debt reduction, platform investments"],
            ["Data Capabilities", "Siloed data, limited analytics", "Unified data fabric, AI-augmented insights", "Data governance frameworks, analytics platforms, data democratization"],
            ["Ecosystem Engagement", "Transactional supplier relationships", "Strategic ecosystem partnerships and co-creation", "Partnership programs, open innovation, platform participation"],
            ["Sustainability Integration", "Compliance-focused environmental reporting", "Technology-enabled sustainability embedded in operations", "Green IT initiatives, circular economy systems, ESG-integrated strategy"],
        ],
        caption="Table 4. Future-Ready Organization Assessment Framework: Dimensions, Targets, and Actions"
    )
    
    doc.add_paragraph(
        "Table 4 presents a comprehensive framework for assessing organizational future-readiness across six "
        "critical dimensions. This assessment tool enables organizations to identify gaps between their current "
        "state and the capabilities required for sustained competitive advantage in an increasingly digital and "
        "sustainability-conscious business environment. The framework emphasizes that future-readiness is not "
        "solely about technology adoption but encompasses cultural, organizational, and strategic dimensions "
        "that must evolve in concert with technological capabilities. Organizations can use this framework for "
        "periodic self-assessment, tracking progress along each dimension and identifying areas where accelerated "
        "investment or attention is needed. The interdependencies between dimensions are particularly important "
        "to recognize: digital skills development enables technology infrastructure modernization, which in turn "
        "supports data capability advancement, creating reinforcing cycles that accelerate overall transformation "
        "when properly coordinated. Conversely, weaknesses in any single dimension can constrain progress across "
        "all others, highlighting the importance of balanced investment across the full spectrum of future-readiness "
        "capabilities."
    )
    
    # 4.3
    doc.add_heading("4.3 Future Directions and Strategic Roadmap", 2)
    
    doc.add_paragraph(
        "Anticipating technological disruptions and market shifts requires organizations to develop systematic "
        "capabilities for environmental scanning, trend analysis, and scenario planning. The accelerating pace "
        "of technological change means that organizations must look further ahead while simultaneously maintaining "
        "the flexibility to adapt as futures unfold differently than anticipated. Technologies currently in "
        "early development stages, including quantum computing, brain-computer interfaces, autonomous systems, "
        "and molecular nanotechnology, have the potential to create entirely new competitive landscapes within "
        "the next decade, requiring organizations to develop adaptive strategies that can accommodate multiple "
        "possible futures. Horizon scanning methodologies that systematically monitor scientific publications, "
        "patent filings, startup activity, and research funding patterns can provide early warning of emerging "
        "technologies with disruptive potential, enabling proactive strategic positioning rather than reactive "
        "adaptation after disruption occurs. The development of technology foresight capabilities, including "
        "war-gaming exercises, technology scouting programs, and scenario planning workshops, enables organizations "
        "to build shared understanding of possible futures and develop robust strategies that perform adequately "
        "across a range of potential outcomes rather than optimizing for a single predicted future that may "
        "not materialize."
    )
    
    doc.add_paragraph(
        "Designing long-term technology adoption roadmaps provides organizations with structured approaches for "
        "sequencing technology investments, building capabilities, and managing the organizational change required "
        "for successful transformation. Effective roadmaps balance short-term value delivery with long-term "
        "capability building, ensure alignment between technology investments and business strategy, and "
        "incorporate flexibility mechanisms that enable adaptation as conditions change. The strategic roadmap "
        "for technology-driven growth illustrated in Figure 4 presents a four-phase approach that guides "
        "organizations from initial assessment through full innovation integration. Roadmap governance "
        "mechanisms including periodic reviews, milestone assessments, and adaptive planning cycles ensure "
        "that technology strategies remain relevant and effective as both internal capabilities and external "
        "conditions evolve over time. The integration of financial planning with technology roadmapping enables "
        "organizations to optimize investment timing, manage cash flow implications of major technology "
        "programs, and demonstrate return on investment to stakeholders who require evidence of value creation "
        "from significant technology expenditures."
    )
    
    # Insert Figure 4
    doc.add_image(
        '/projects/sandbox/AMMAN/chapter_figures/Figure_4_Strategic_Roadmap.png',
        caption="Figure 4. Strategic Roadmap for Technology-Driven Sustainable Growth: Four-phase approach from assessment to innovation leadership",
        width_emu=5000000,
        height_emu=3800000
    )
    
    doc.add_paragraph(
        "Figure 4 illustrates the strategic roadmap comprising four sequential phases: Assessment, Implementation, "
        "Optimization, and Innovation. Each phase includes specific activities, key performance indicators, and "
        "milestones that guide organizational progress toward technology-driven competitive advantage. The roadmap "
        "emphasizes the iterative nature of technology adoption, with continuous feedback loops enabling learning "
        "and adaptation throughout the transformation journey. Organizations should view this roadmap not as a "
        "rigid prescription but as an adaptive framework that can be customized to specific organizational "
        "contexts, industry dynamics, and strategic priorities."
    )
    
    doc.add_paragraph(
        "Harnessing technology for resilience, competitiveness, and sustainable growth requires organizations "
        "to adopt integrated approaches that simultaneously address operational efficiency, customer value, "
        "innovation capability, and societal responsibility. The convergence of digital transformation with "
        "sustainability imperatives creates opportunities for organizations to build competitive advantages "
        "that are both economically viable and socially responsible. As the business environment continues "
        "to evolve at an unprecedented pace, organizations that successfully integrate emerging technologies "
        "into their strategic fabric will be best positioned to thrive in the face of uncertainty, create "
        "lasting value for stakeholders, and contribute to a more sustainable and prosperous global economy. "
        "The transition from viewing technology as a functional enabler to recognizing it as a strategic "
        "imperative represents a fundamental shift in organizational thinking that distinguishes future-ready "
        "firms from those at risk of disruption and decline. The most successful organizations will be those "
        "that develop what may be termed technological ambidexterity: the simultaneous ability to exploit "
        "current technologies for maximum operational value while exploring emerging technologies for "
        "future competitive positioning, maintaining balance between efficiency and innovation across "
        "their entire technology portfolio."
    )
    
    doc.add_paragraph(
        "In conclusion, the strategic deployment of emerging technologies represents both the greatest opportunity "
        "and the most significant challenge facing modern organizations. Success requires not only technological "
        "sophistication but also organizational wisdom: the ability to align technology investments with strategic "
        "objectives, develop human capabilities alongside technical ones, manage risks responsibly, and maintain "
        "a long-term perspective amidst short-term pressures. Organizations that master this complex balancing "
        "act will emerge as the competitive leaders of the digital age, while those that fail to adapt will "
        "find themselves increasingly marginalized in an unforgiving global marketplace. The frameworks, analyses, "
        "and strategic guidance presented in this chapter provide a foundation for informed decision-making and "
        "effective action in the pursuit of technology-driven competitive advantage. The journey toward digital "
        "leadership is neither simple nor linear, but organizations that approach it with clarity of purpose, "
        "commitment to learning, and willingness to transform will find abundant opportunities to create "
        "enduring value in an increasingly technology-mediated world. Ultimately, the organizations that will "
        "thrive are those that view technology not merely as a tool for efficiency but as a fundamental enabler "
        "of new forms of value creation, stakeholder engagement, and societal contribution that define "
        "competitive excellence in the twenty-first century."
    )
    
    doc.add_page_break()
    
    # ============================================================
    # REFERENCES
    # ============================================================
    doc.add_heading("References", 1)
    
    references = [
        "[1] Schwab, K. (2017). The Fourth Industrial Revolution. Crown Publishing Group, New York.",
        "[2] Vial, G. (2019). Understanding digital transformation: A review and a research agenda. Journal of Strategic Information Systems, 28(2), 118-144.",
        "[3] Bharadwaj, A., El Sawy, O. A., Pavlou, P. A., & Venkatraman, N. (2013). Digital business strategy: Toward a next generation of insights. MIS Quarterly, 37(2), 471-482.",
        "[4] Ghemawat, P. (2018). The New Global Road Map: Enduring Strategies for Turbulent Times. Harvard Business Review Press.",
        "[5] Lemon, K. N., & Verhoef, P. C. (2016). Understanding customer experience throughout the customer journey. Journal of Marketing, 80(6), 69-96.",
        "[6] Teece, D. J. (2018). Business models and dynamic capabilities. Long Range Planning, 51(1), 40-49.",
        "[7] McKinsey & Company (2021). The next normal: Digitizing at speed and scale. McKinsey Global Institute Report.",
        "[8] Lasi, H., Fettke, P., Kemper, H. G., Feld, T., & Hoffmann, M. (2014). Industry 4.0. Business & Information Systems Engineering, 6(4), 239-242.",
        "[9] Xu, X., Lu, Y., Vogel-Heuser, B., & Wang, L. (2021). Industry 4.0 and Industry 5.0: Inception, conception and perception. Journal of Manufacturing Systems, 61, 530-535.",
        "[10] Porter, M. E., & Heppelmann, J. E. (2014). How smart, connected products are transforming competition. Harvard Business Review, 92(11), 64-88.",
        "[11] Teece, D. J. (2018). Profiting from innovation in the digital economy: Enabling technologies, standards, and licensing models. Research Policy, 47(8), 1367-1387.",
        "[12] Nambisan, S., Wright, M., & Feldman, M. (2019). The digital transformation of innovation and entrepreneurship: Progress, challenges and key themes. Research Policy, 48(8), 103773.",
        "[13] Westerman, G., Bonnet, D., & McAfee, A. (2014). Leading Digital: Turning Technology into Business Transformation. Harvard Business Review Press.",
        "[14] Matt, C., Hess, T., & Benlian, A. (2015). Digital transformation strategies. Business & Information Systems Engineering, 57(5), 339-343.",
        "[15] Teece, D. J. (2007). Explicating dynamic capabilities: The nature and microfoundations of (sustainable) enterprise performance. Strategic Management Journal, 28(13), 1319-1350.",
        "[16] Rogers, E. M. (2003). Diffusion of Innovations (5th ed.). Free Press, New York.",
        "[17] Lokuge, S., Sedera, D., Grover, V., & Dongming, X. (2019). Organizational readiness for digital innovation. Information & Management, 56(6), 103146.",
        "[18] Kane, G. C., Palmer, D., Phillips, A. N., Kiron, D., & Buckley, N. (2019). Accelerating digital innovation inside and out. MIT Sloan Management Review Research Report.",
        "[19] Pisano, G. P. (2019). The hard truth about innovative cultures. Harvard Business Review, 97(1), 62-71.",
        "[20] Fitzgerald, M., Kruschwitz, N., Bonnet, D., & Welch, M. (2014). Embracing digital technology: A new strategic imperative. MIT Sloan Management Review, 55(2), 1-12.",
        "[21] Li, L., Su, F., Zhang, W., & Mao, J. Y. (2018). Digital transformation by SME entrepreneurs: A capability perspective. Information Systems Journal, 28(6), 1129-1157.",
        "[22] Davenport, T. H., & Ronanki, R. (2018). Artificial intelligence for the real world. Harvard Business Review, 96(1), 108-116.",
        "[23] Agrawal, A., Gans, J., & Goldfarb, A. (2018). Prediction Machines: The Simple Economics of Artificial Intelligence. Harvard Business Review Press.",
        "[24] Lacity, M. C., & Willcocks, L. P. (2021). Becoming strategic with intelligent automation. MIS Quarterly Executive, 20(1), 1-14.",
        "[25] Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2023). GPTs are GPTs: An early look at the labor market impact potential of large language models. arXiv preprint arXiv:2303.10130.",
        "[26] Christensen, C. M., McDonald, R., Altman, E. J., & Palmer, J. E. (2018). Disruptive innovation: An intellectual history and directions for future research. Journal of Management Studies, 55(7), 1043-1078.",
        "[27] Atzori, L., Iera, A., & Morabito, G. (2017). Understanding the Internet of Things: Definition, potentials, and societal role of a fast-evolving paradigm. Ad Hoc Networks, 56, 122-140.",
        "[28] Armbrust, M., Fox, A., Griffith, R., et al. (2010). A view of cloud computing. Communications of the ACM, 53(4), 50-58.",
        "[29] Iansiti, M., & Lakhani, K. R. (2020). Competing in the Age of AI: Strategy and Leadership When Algorithms and Networks Run the World. Harvard Business Review Press.",
        "[30] McAfee, A., & Brynjolfsson, E. (2017). Machine, Platform, Crowd: Harnessing Our Digital Future. W. W. Norton & Company.",
        "[31] Iansiti, M., & Lakhani, K. R. (2017). The truth about blockchain. Harvard Business Review, 95(1), 118-127.",
        "[32] Parker, G. G., Van Alstyne, M. W., & Choudary, S. P. (2016). Platform Revolution: How Networked Markets Are Transforming the Economy. W. W. Norton & Company.",
        "[33] Cusumano, M. A., Gawer, A., & Yoffie, D. B. (2019). The Business of Platforms: Strategy in the Age of Digital Competition, Innovation, and Power. Harper Business.",
        "[34] Arute, F., Arya, K., Babbush, R., et al. (2019). Quantum supremacy using a programmable superconducting processor. Nature, 574(7779), 505-510.",
        "[35] Nambisan, S., Lyytinen, K., Majchrzak, A., & Song, M. (2017). Digital innovation management: Reinventing innovation management research in a digital world. MIS Quarterly, 41(1), 223-238.",
        "[36] Osterwalder, A., Pigneur, Y., Bernarda, G., & Smith, A. (2014). Value Proposition Design. John Wiley & Sons.",
        "[37] Rigby, D. K., Sutherland, J., & Noble, A. (2018). Agile at scale. Harvard Business Review, 96(3), 88-96.",
        "[38] Huang, M. H., & Rust, R. T. (2021). A strategic framework for artificial intelligence in marketing. Journal of the Academy of Marketing Science, 49(1), 30-50.",
        "[39] Bolton, R. N., McColl-Kennedy, J. R., Cheung, L., et al. (2018). Customer experience challenges: Bringing together digital, physical and social realms. Journal of Service Management, 29(5), 776-808.",
        "[40] Kumar, V., Rajan, B., Venkatesan, R., & Lecinski, J. (2019). Understanding the role of artificial intelligence in personalized engagement marketing. California Management Review, 61(4), 135-155.",
        "[41] Zheng, T., Ardolino, M., Bacchetti, A., & Perona, M. (2021). The applications of Industry 4.0 technologies in manufacturing context: A systematic literature review. International Journal of Production Research, 59(6), 1922-1954.",
        "[42] George, G., Merrill, R. K., & Schillebeeckx, S. J. (2021). Digital sustainability and entrepreneurship: How digital innovations are helping tackle climate change and sustainable development. Entrepreneurship Theory and Practice, 45(5), 999-1027.",
        "[43] Kshetri, N. (2021). Cybersecurity management: An organizational and strategic approach. University of Toronto Press.",
    ]
    
    for ref in references:
        doc.add_paragraph(ref)
    
    # Save document
    output_path = '/projects/sandbox/AMMAN/Chapter_Technology_Competitive_Advantage.docx'
    doc.save(output_path)
    
    # Count approximate words
    word_count = 0
    for elem in doc.body_elements:
        if elem[0] in ('paragraph', 'heading'):
            text = elem[1]
            word_count += len(text.split())
        elif elem[0] == 'table':
            for row in elem[2]:
                for cell in row:
                    word_count += len(str(cell).split())
            for h in elem[1]:
                word_count += len(h.split())
    
    print(f"\nApproximate word count: {word_count}")
    print(f"Number of references: {len(references)}")
    print(f"Number of tables: 4")
    print(f"Number of figures: 4")
    print(f"Output: {output_path}")
    

if __name__ == "__main__":
    build_chapter()
