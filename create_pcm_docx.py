#!/usr/bin/env python3
"""
Create a DOCX file for the PCM chapter from scratch using zipfile.
DOCX is an Open XML format - essentially a ZIP of XML files.
No external dependencies required.
"""
import zipfile
import os
import base64
import struct
import zlib

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "Chapter_Phase_Change_Thermal_Energy_Storage.docx")
FIGURES_DIR = os.path.join(SCRIPT_DIR, "pcm_figures")

# XML namespace declarations used throughout
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
}



def escape_xml(text):
    """Escape XML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')


def make_paragraph(text, style=None, bold=False, italic=False, font_size=None, alignment=None):
    """Create a paragraph XML element."""
    ppr = '<w:pPr>'
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if alignment:
        ppr += f'<w:jc w:val="{alignment}"/>'
    ppr += '</w:pPr>'
    
    rpr = '<w:rPr>'
    if bold:
        rpr += '<w:b/>'
    if italic:
        rpr += '<w:i/>'
    if font_size:
        rpr += f'<w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/>'
    rpr += '</w:rPr>'
    
    escaped = escape_xml(text)
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{escaped}</w:t></w:r></w:p>'


def make_heading(text, level=1):
    """Create a heading paragraph."""
    style = f'Heading{level}'
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r></w:p>'



def make_image_paragraph(rid, width_emu, height_emu, caption=""):
    """Create an inline image paragraph."""
    img_xml = f'''<w:p>
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{width_emu}" cy="{height_emu}"/>
        <wp:docPr id="1" name="Picture"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="Picture"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rid}"/>
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
        img_xml += make_paragraph(caption, italic=True, alignment="center", font_size="20")
    return img_xml



def make_table(headers, rows, caption=""):
    """Create a table XML element."""
    xml = ''
    if caption:
        xml += make_paragraph(caption, bold=True, alignment="center", font_size="20")
    
    col_count = len(headers)
    col_width = 9000 // col_count  # distribute across page width
    
    xml += '<w:tbl>'
    xml += '<w:tblPr>'
    xml += '<w:tblStyle w:val="TableGrid"/>'
    xml += f'<w:tblW w:w="9000" w:type="dxa"/>'
    xml += '<w:tblBorders>'
    xml += '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '</w:tblBorders>'
    xml += '</w:tblPr>'
    
    # Grid definition
    xml += '<w:tblGrid>'
    for _ in range(col_count):
        xml += f'<w:gridCol w:w="{col_width}"/>'
    xml += '</w:tblGrid>'
    
    # Header row
    xml += '<w:tr>'
    for h in headers:
        xml += f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="1B3C78"/></w:tcPr>'
        xml += f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">{escape_xml(h)}</w:t></w:r></w:p></w:tc>'
    xml += '</w:tr>'
    
    # Data rows
    for row in rows:
        xml += '<w:tr>'
        for cell in row:
            xml += f'<w:tc><w:p><w:pPr><w:jc w:val="left"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">{escape_xml(str(cell))}</w:t></w:r></w:p></w:tc>'
        xml += '</w:tr>'
    
    xml += '</w:tbl>'
    xml += '<w:p/>'  # Empty paragraph after table
    return xml



def generate_document_body(image_rids):
    """Generate the full document body XML content."""
    body = ''
    
    # Title
    body += make_heading('Phase Change and Thermal Energy Storage Materials', 1)
    body += make_paragraph('Book: Emerging Materials and Technologies for Sustainable Development and Clean Energy', italic=True, alignment="center", font_size="22")
    body += '<w:p/>'
    
    # Abstract
    body += make_heading('Abstract', 2)
    body += make_paragraph(
        'Thermal energy storage (TES) technologies have emerged as a cornerstone in the global transition toward sustainable energy systems. '
        'Among TES approaches, phase change materials (PCMs) offer unparalleled advantages in storing and releasing thermal energy at nearly '
        'constant temperatures, providing high energy density per unit volume. This chapter provides a comprehensive overview of PCM science, '
        'engineering, and applications within the context of sustainable development and clean energy. Beginning with the fundamental principles '
        'of thermal energy storage and the classification of PCMs, the discussion progresses through the key challenges limiting PCM performance '
        'and the advanced strategies developed to overcome them, including thermal conductivity enhancement, encapsulation, and computational '
        'modeling. The chapter then examines critical applications spanning building energy management, renewable energy integration, battery '
        'thermal management, and industrial systems. Finally, a forward-looking analysis addresses life cycle assessment, emerging smart '
        'technologies, and the policy landscape necessary to accelerate PCM deployment in the global energy transition.'
    )
    body += '<w:p/>'
    body += make_paragraph('Keywords: Phase change materials, thermal energy storage, latent heat, sustainability, energy efficiency, encapsulation, renewable energy integration', bold=True, font_size="20")
    body += '<w:p/>'
    
    return body



def generate_section1(image_rids):
    """Generate Section 1 content."""
    body = ''
    body += make_heading('Section 1: Fundamentals of Thermal Energy Storage and Phase Change Materials', 1)
    body += make_heading('1.1 The Role of Thermal Energy Storage in Sustainable Energy Systems', 2)
    
    body += make_paragraph(
        'The twenty-first century presents an unprecedented challenge in reconciling growing global energy demand with the imperative '
        'to decarbonize energy systems [6]. Renewable energy sources, particularly solar and wind power, have experienced remarkable '
        'growth over the past two decades, driven by dramatic cost reductions and supportive policy frameworks [7]. However, the inherent '
        'intermittency of these resources remains a fundamental obstacle to their widespread integration into energy grids [8]. Solar energy '
        'is available only during daylight hours and is subject to cloud cover, while wind energy fluctuates with atmospheric conditions. '
        'This temporal mismatch between energy supply and demand necessitates effective energy storage solutions capable of bridging the '
        'gap between generation and consumption [9].'
    )
    
    body += make_paragraph(
        'Thermal energy storage (TES) represents one of the most promising and cost-effective approaches to addressing this intermittency '
        'challenge [10]. Unlike electrochemical storage systems such as batteries, TES systems store energy in the form of heat or cold, '
        'which can subsequently be retrieved for heating, cooling, or power generation purposes [11]. The fundamental operating principle '
        'of any TES system involves three distinct phases: charging, during which thermal energy is absorbed and stored; storing, during '
        'which the energy is maintained with minimal losses over the required duration; and discharging, during which the stored energy '
        'is released to meet demand [12].'
    )
    
    # Figure 6
    body += '<w:p/>'
    body += make_image_paragraph(image_rids['fig6'], 5400000, 3037500, 
        'Figure 6: Schematic of Thermal Energy Storage System - Operating Principle')
    body += '<w:p/>'
    
    body += make_paragraph(
        'TES technologies are broadly classified into three categories based on the mechanism of energy storage [13]. Sensible heat storage '
        'involves raising or lowering the temperature of a storage medium without any phase change occurring. Common sensible heat storage '
        'materials include water, rocks, concrete, and molten salts. The energy stored is proportional to the mass of the material, its '
        'specific heat capacity, and the temperature difference achieved [14]. While conceptually simple and widely deployed, sensible heat '
        'storage systems typically require large volumes of material and operate over broad temperature ranges, which can limit system efficiency.'
    )
    
    body += make_paragraph(
        'Latent heat storage, the primary focus of this chapter, exploits the energy absorbed or released during a phase transition, most '
        'commonly the solid-to-liquid transition [15]. Phase change materials (PCMs) can store significantly more energy per unit mass or '
        'volume compared to sensible heat storage materials, because the latent heat of fusion is typically much larger than the sensible '
        'heat stored over a practical temperature range [16]. Furthermore, the phase transition occurs at a nearly constant temperature, '
        'providing isothermal or near-isothermal operation that is highly advantageous for temperature-sensitive applications.'
    )
    
    body += make_paragraph(
        'Thermochemical storage represents the third category, utilizing reversible chemical reactions to store and release thermal energy [17]. '
        'While thermochemical systems offer the highest theoretical energy densities and can store energy indefinitely without thermal losses, '
        'they remain largely in the research and development stage due to challenges related to reaction kinetics, system complexity, and '
        'material degradation.'
    )
    
    return body



def generate_table1():
    """Table 1: Comparison of Thermal Energy Storage Methods."""
    headers = ['Parameter', 'Sensible Heat Storage', 'Latent Heat Storage (PCM)', 'Thermochemical Storage']
    rows = [
        ['Storage mechanism', 'Temperature change', 'Phase transition', 'Reversible chemical reaction'],
        ['Energy density (kJ/m3)', '50-150', '150-400', '500-3000'],
        ['Temperature range', 'Wide (DT dependent)', 'Narrow (isothermal)', 'Application-specific'],
        ['Storage duration', 'Hours to days', 'Hours to days', 'Days to months'],
        ['Maturity level', 'Commercial', 'Commercial/Demo', 'Research/Pilot'],
        ['Typical materials', 'Water, rock, concrete', 'Paraffins, salt hydrates', 'Metal hydrides, zeolites'],
        ['Advantages', 'Simple, low cost', 'High density, isothermal', 'Highest density, no losses'],
        ['Disadvantages', 'Large volume, heat loss', 'Low conductivity, leakage', 'Complex, slow kinetics'],
    ]
    return make_table(headers, rows, 'Table 1: Comparison of Thermal Energy Storage Methods')


def generate_section1_continued(image_rids):
    """Continue Section 1 after Table 1."""
    body = ''
    
    body += generate_table1()
    
    body += make_paragraph(
        'TES systems can also be categorized as active or passive based on their operational characteristics [18]. Active TES systems '
        'employ forced convection mechanisms, such as pumps or fans, to circulate the storage medium or heat transfer fluid through the '
        'system. These systems offer greater control over charging and discharging rates but require external energy input and more complex '
        'infrastructure. Passive TES systems, by contrast, rely on natural heat transfer mechanisms such as conduction and natural '
        'convection [19]. In passive systems, the PCM is typically integrated directly into the application environment, such as within '
        'building walls or around heat-generating equipment, and absorbs or releases heat in response to ambient temperature fluctuations '
        'without any mechanical intervention.'
    )
    
    body += make_paragraph(
        'The strategic importance of TES in sustainable energy systems extends beyond simple energy storage. By enabling load shifting, '
        'peak shaving, and demand-side management, TES technologies can reduce the strain on electrical grids, decrease the need for '
        'peaking power plants (which are often fossil fuel-based), and improve the overall efficiency of energy systems [20]. In the context '
        'of heating and cooling, which accounts for approximately 50% of global final energy consumption, TES offers particular promise '
        'for reducing carbon emissions and enhancing energy security [21].'
    )
    
    # Section 1.2
    body += make_heading('1.2 Phase Change Materials: Fundamentals and Classification', 2)
    
    body += make_paragraph(
        'The science of phase change materials is rooted in the thermodynamic principles governing phase transitions [22]. When a substance '
        'undergoes a phase change from solid to liquid (melting), it absorbs a quantity of energy known as the latent heat of fusion at a '
        'characteristic temperature (the melting point) without any change in temperature until the transition is complete. Conversely, '
        'during solidification (freezing), the material releases this stored energy at the same characteristic temperature [23]. This '
        'isothermal energy absorption and release mechanism is what distinguishes latent heat storage from sensible heat storage and '
        'provides PCMs with their unique advantages.'
    )
    
    # Figure 3
    body += '<w:p/>'
    body += make_image_paragraph(image_rids['fig3'], 5400000, 3375000,
        'Figure 3: Temperature Profile During PCM Charging and Discharging')
    body += '<w:p/>'
    
    return body



def generate_section1_classification(image_rids):
    """Section 1.2 continued - classification."""
    body = ''
    
    body += make_paragraph(
        'The phase transition process in a solid-liquid PCM can be understood at the molecular level. In the solid state, molecules are '
        'held in fixed positions within a crystalline or amorphous lattice by intermolecular forces. As heat is supplied, the molecular '
        'kinetic energy increases until it overcomes these binding forces, allowing molecules to move freely and form a liquid [24]. The '
        'energy required to break these intermolecular bonds constitutes the latent heat.'
    )
    
    body += make_paragraph(
        'PCMs are classified into three broad categories: organic, inorganic, and eutectic mixtures [25]. Each category encompasses a wide '
        'range of materials with distinct properties, advantages, and limitations. Figure 1 presents the complete classification hierarchy of PCMs.'
    )
    
    # Figure 1
    body += '<w:p/>'
    body += make_image_paragraph(image_rids['fig1'], 5400000, 3375000,
        'Figure 1: Classification of Phase Change Materials (PCMs)')
    body += '<w:p/>'
    
    body += make_paragraph(
        'Organic PCMs include paraffin waxes, fatty acids, esters, alcohols, and glycols [26]. Paraffin waxes (alkanes with the general '
        'formula CnH2n+2) are among the most widely studied and commercially available organic PCMs. They offer a broad range of melting '
        'temperatures (from approximately -5 degrees C to over 100 degrees C) that can be tuned by selecting paraffins with different chain '
        'lengths [27]. Key advantages of organic PCMs include excellent chemical stability, non-corrosiveness, self-nucleating behavior, '
        'congruent melting, and good compatibility with conventional encapsulation materials. However, organic PCMs suffer from relatively '
        'low thermal conductivity (typically 0.15-0.30 W/m.K), moderate latent heat values (150-250 kJ/kg for paraffins), flammability, '
        'and relatively high cost for pure compounds [28].'
    )
    
    body += make_paragraph(
        'Non-paraffin organic PCMs, including fatty acids (such as capric acid, lauric acid, palmitic acid, and stearic acid), offer sharper '
        'melting transitions and higher latent heat values compared to paraffin waxes but tend to be more expensive and mildly corrosive [29]. '
        'Polyethylene glycols (PEGs) represent another subclass of organic PCMs with tunable melting points and good biocompatibility [30].'
    )
    
    body += make_paragraph(
        'Inorganic PCMs primarily comprise salt hydrates and metallics [31]. Salt hydrates (general formula AB.nH2O) are crystalline salts '
        'that incorporate water molecules within their crystal structure [32]. Salt hydrates offer several compelling advantages: high '
        'volumetric latent heat storage capacity (typically 200-400 kJ/kg), relatively high thermal conductivity (0.5-1.0 W/m.K), low '
        'cost, non-flammability, and availability. However, they are plagued by significant challenges including incongruent melting, '
        'subcooling, and corrosiveness toward metals [33].'
    )
    
    body += make_paragraph(
        'Molten salts, such as mixtures of sodium nitrate and potassium nitrate, operate at much higher temperatures (200-600 degrees C) '
        'and are primarily used in concentrated solar power plants for high-temperature thermal storage [34].'
    )
    
    body += make_paragraph(
        'Eutectic PCMs are minimum-melting-point mixtures of two or more components [35]. The eutectic composition melts and freezes '
        'congruently at a single, sharp temperature, which is lower than the melting points of the individual components. The selection '
        'of an appropriate PCM for a given application requires careful consideration of multiple criteria [36].'
    )
    
    return body



def generate_table2():
    """Table 2: Thermophysical Properties of Representative PCMs."""
    headers = ['PCM Type', 'Example', 'Melting T (C)', 'Latent Heat (kJ/kg)', 'Thermal Cond. (W/m.K)', 'Density (kg/m3)', 'Key Advantage', 'Key Limitation']
    rows = [
        ['Paraffin', 'n-Octadecane', '28', '244', '0.15', '814', 'Stable, no subcooling', 'Low conductivity'],
        ['Paraffin', 'RT-42', '42', '174', '0.20', '880', 'Commercial availability', 'Flammable'],
        ['Fatty acid', 'Capric acid', '32', '153', '0.15', '886', 'Sharp melting point', 'Mildly corrosive'],
        ['Fatty acid', 'Palmitic acid', '64', '185', '0.16', '850', 'High latent heat', 'Higher cost'],
        ['PEG', 'PEG-6000', '66', '190', '0.19', '1085', 'Biocompatible', 'Hygroscopic'],
        ['Salt hydrate', 'CaCl2.6H2O', '29', '190', '0.54', '1710', 'Low cost, non-flammable', 'Subcooling'],
        ['Salt hydrate', 'Na2SO4.10H2O', '32', '254', '0.55', '1485', 'High latent heat', 'Incongruent melting'],
        ['Molten salt', 'NaNO3', '306', '172', '0.50', '2260', 'High-temp storage', 'Corrosive at high T'],
        ['Eutectic', 'Capric-Lauric', '21', '143', '0.14', '880', 'Tailored melting T', 'Limited cycle data'],
        ['Metallic', 'Gallium', '30', '80', '29.4', '5907', 'Very high conductivity', 'Very expensive'],
    ]
    return make_table(headers, rows, 'Table 2: Thermophysical Properties of Representative Phase Change Materials')


def generate_section1_challenges():
    """Section 1.3 - Key Challenges."""
    body = ''
    body += make_heading('1.3 Key Challenges and Performance Limitations of PCMs', 2)
    
    body += make_paragraph(
        'Despite their considerable promise, PCMs face several significant challenges that have historically limited their widespread '
        'adoption in commercial systems [37]. Understanding these limitations is essential for developing effective mitigation strategies, '
        'which are explored in subsequent sections.'
    )
    
    body += make_paragraph(
        'Low Thermal Conductivity represents the single most critical challenge facing PCM systems [38]. The vast majority of PCMs, '
        'particularly organic materials, exhibit thermal conductivities in the range of 0.1-0.5 W/m.K, which is one to three orders of '
        'magnitude lower than that of common metals [39]. This low thermal conductivity creates substantial thermal resistance between '
        'the heat source/sink and the PCM bulk, severely limiting the rate at which energy can be stored during charging and retrieved '
        'during discharging.'
    )
    
    body += make_paragraph(
        'Incongruent Melting is a phenomenon predominantly affecting salt hydrate PCMs [40]. When a salt hydrate melts incongruently, '
        'the anhydrous salt does not completely dissolve in the released water of crystallization at the melting temperature, resulting in '
        'progressive and irreversible degradation of the storage capacity with each thermal cycle [41].'
    )
    
    body += make_paragraph(
        'Subcooling (Supercooling) refers to the phenomenon where a PCM must be cooled significantly below its melting point before '
        'crystallization nucleation occurs and solidification commences [42]. The degree of subcooling can range from a few degrees to '
        'more than 20 degrees C in severe cases. Leakage during the liquid phase is an inherent challenge for solid-liquid PCMs [43]. '
        'Volume changes accompanying the solid-liquid transition (typically 5-15% expansion upon melting) exacerbate leakage issues by '
        'creating mechanical stress on containers.'
    )
    
    body += make_paragraph(
        'Poor Long-Term Cycling Stability encompasses the gradual degradation of PCM properties over repeated melting and solidification '
        'cycles [44]. The implications of these challenges for system performance are substantial [45]. Addressing these challenges through '
        'material engineering and system design is therefore essential for realizing the full potential of PCM-based thermal energy storage.'
    )
    
    return body



def generate_table3():
    """Table 3: Key Challenges of PCMs."""
    headers = ['Challenge', 'Affected PCM Type', 'Severity', 'Impact on Performance', 'Mitigation Strategy']
    rows = [
        ['Low thermal conductivity', 'All (especially organic)', 'Critical', 'Slow charge/discharge rates', 'Metal foams, nanoparticles, fins'],
        ['Incongruent melting', 'Salt hydrates', 'High', 'Capacity loss (20-50%)', 'Thickening agents, stirring'],
        ['Subcooling', 'Salt hydrates, some organic', 'Moderate-High', 'Delayed heat release', 'Nucleating agents, cold finger'],
        ['Leakage', 'All solid-liquid', 'Moderate', 'Material loss, contamination', 'Encapsulation, shape stabilization'],
        ['Volume change', 'All', 'Moderate', 'Container stress, seal failure', 'Void space design, flexible containers'],
        ['Cycling degradation', 'All', 'High (long-term)', 'Reduced lifetime', 'Material purification, encapsulation'],
        ['Flammability', 'Organic PCMs', 'Moderate', 'Safety hazard', 'Fire retardants, inorganic shells'],
        ['Corrosion', 'Salt hydrates', 'Moderate', 'Container degradation', 'Compatible materials, coatings'],
    ]
    return make_table(headers, rows, 'Table 3: Key Challenges of PCMs and Their Impact on System Performance')


def generate_section2(image_rids):
    """Generate Section 2 content."""
    body = ''
    body += make_heading('Section 2: Enhancing PCM Performance for Advanced Applications', 1)
    body += make_heading('2.1 Thermal Conductivity Enhancement Techniques', 2)
    
    body += make_paragraph(
        'The low intrinsic thermal conductivity of most PCMs constitutes the primary bottleneck limiting the practical performance of '
        'latent heat storage systems [46]. Consequently, extensive research over the past three decades has focused on developing '
        'strategies to enhance the effective thermal conductivity of PCM composites without significantly compromising their latent '
        'heat storage capacity [47].'
    )
    
    body += make_paragraph(
        'Metallic Foams and Porous Matrices represent one of the most effective approaches for thermal conductivity enhancement [48]. '
        'Open-cell metal foams, typically fabricated from aluminum or copper with porosities ranging from 85% to 97%, provide a continuous, '
        'highly conductive network throughout the PCM volume. Studies have demonstrated that incorporating aluminum foam with 95% porosity '
        'can increase the effective thermal conductivity of paraffin-based systems by a factor of 20-40, reducing melting times by 50-80% '
        'compared to pure PCM systems [49].'
    )
    
    body += make_paragraph(
        'Nanoparticle Additives offer another strategy for enhancing PCM thermal conductivity [50]. High-conductivity nanoparticles are '
        'dispersed within the PCM to create nano-enhanced PCMs (NePCMs). The nanoparticles can increase the effective thermal conductivity '
        'by 10-100%, depending on particle type, size, concentration, and dispersion quality [51]. Typical nanoparticle loading fractions '
        'range from 1% to 10% by weight [52].'
    )
    
    body += make_paragraph(
        'Carbon-Based Materials have emerged as particularly promising thermal conductivity enhancers [53]. Expanded graphite composites '
        'can achieve effective thermal conductivities of 5-50 W/m.K while retaining 80-90% of the original PCM latent heat capacity [54]. '
        'Carbon nanotubes (CNTs) and graphene nanoplatelets offer similar benefits [55].'
    )
    
    body += make_paragraph(
        'Finned Heat Exchanger Surfaces represent a system-level approach to addressing the thermal conductivity limitation [56]. Advanced '
        'fin designs inspired by fractal geometry or topology optimization algorithms can achieve superior heat transfer enhancement [57]. '
        'In practice, hybrid approaches combining multiple enhancement techniques can achieve synergistic performance improvements [58].'
    )
    
    # Figure 2
    body += '<w:p/>'
    body += make_image_paragraph(image_rids['fig2'], 5400000, 3375000,
        'Figure 2: Thermal Conductivity Enhancement of PCMs - Comparison of Techniques')
    body += '<w:p/>'
    
    return body



def generate_table4():
    """Table 4: Thermal Conductivity Enhancement Techniques."""
    headers = ['Enhancement Method', 'Additive/Structure', 'Conductivity (W/m.K)', 'Enhancement Factor', 'Latent Heat Retention (%)', 'Key Trade-off']
    rows = [
        ['Pure Paraffin (baseline)', 'None', '0.15-0.25', '1x', '100', '-'],
        ['Nanoparticles (1-5 wt%)', 'Al2O3, CuO, TiO2', '0.3-0.5', '1.5-2.5x', '90-98', 'Viscosity increase, sedimentation'],
        ['Carbon nanotubes (1-5 wt%)', 'MWCNT, SWCNT', '0.4-1.0', '2-5x', '85-95', 'Dispersion difficulty, cost'],
        ['Graphene nanoplatelets', 'GNP (1-10 wt%)', '0.5-2.0', '3-10x', '85-95', 'Agglomeration'],
        ['Expanded graphite', 'EG (5-20 wt%)', '5-50', '25-250x', '75-90', 'Reduces PCM volume'],
        ['Metal foam (Al/Cu)', '85-97% porosity', '3-25', '15-125x', '80-95', 'Weight, cost, volume loss'],
        ['Metallic fins', 'Al, Cu fins', 'System-dependent', '5-20x (effective)', '70-90', 'Volume displacement'],
        ['Hybrid (EG + fins)', 'Combined', '10-60', '50-300x', '70-85', 'Complexity, cost'],
    ]
    return make_table(headers, rows, 'Table 4: Thermal Conductivity Enhancement Techniques for PCMs')


def generate_section2_encapsulation(image_rids):
    """Section 2.2 - Encapsulation."""
    body = ''
    body += make_heading('2.2 Encapsulation and Shape Stabilization', 2)
    
    body += make_paragraph(
        'The transition from solid to liquid phase during PCM melting introduces critical challenges related to material containment, '
        'leakage prevention, and volume change accommodation [59]. Encapsulation and shape stabilization technologies address these '
        'challenges by confining the PCM within protective structures or supporting matrices that maintain structural integrity throughout '
        'repeated phase change cycles.'
    )
    
    body += make_paragraph(
        'Macroencapsulation involves containing PCM volumes typically ranging from milliliters to liters within rigid or semi-rigid '
        'containers or modules [60]. Common macroencapsulation geometries include cylindrical tubes, flat panels or pouches, spherical '
        'nodules, and rectangular containers [61].'
    )
    
    body += make_paragraph(
        'Microencapsulation (capsule diameters of 1-1000 micrometers) and nanoencapsulation (capsule diameters below 1 micrometer) involve '
        'enclosing individual PCM droplets within thin shells of polymer or inorganic material [62]. Microencapsulation is typically achieved '
        'through techniques such as complex coacervation, interfacial polymerization, in-situ polymerization, spray drying, or sol-gel '
        'processes [63]. Micro/nanoencapsulated PCMs (MEPCMs) offer several significant advantages including dramatically improved heat '
        'transfer rates and prevention of leakage [64]. However, microencapsulation introduces challenges including shell rupture, reduced '
        'effective latent heat, and significantly higher cost [65].'
    )
    
    body += make_paragraph(
        'Shape-Stabilized PCMs (ss-PCMs) represent an alternative containment strategy in which the PCM is dispersed within or absorbed '
        'into a supporting matrix material [66]. Shape-stabilized composites are typically prepared by vacuum impregnation, melt blending, '
        'or solution intercalation methods [67].'
    )
    
    # Figure 4
    body += '<w:p/>'
    body += make_image_paragraph(image_rids['fig4'], 5400000, 3375000,
        'Figure 4: PCM Encapsulation Methods - Macro, Micro, and Shape-Stabilized')
    body += '<w:p/>'
    
    return body



def generate_table5():
    """Table 5: Comparison of PCM Encapsulation Techniques."""
    headers = ['Parameter', 'Macroencapsulation', 'Microencapsulation', 'Shape-Stabilized']
    rows = [
        ['Capsule size', '1 mm - 10 cm', '1 um - 1000 um', 'Bulk composite'],
        ['Shell/matrix material', 'Steel, HDPE, Al', 'MF, UF, PMMA, SiO2', 'EG, HDPE, diatomite'],
        ['PCM loading (wt%)', '80-95', '60-85', '50-85'],
        ['Thermal conductivity', 'Low (shell limits)', 'Moderate (high SA/V)', 'Can be high (EG matrix)'],
        ['Leakage prevention', 'Good (sealed)', 'Excellent', 'Good (capillary forces)'],
        ['Heat transfer rate', 'Low (large volume)', 'High', 'Medium-High'],
        ['Cycling stability', 'Good', 'Moderate (shell wear)', 'Good'],
        ['Cost', 'Low-Moderate', 'High', 'Moderate'],
        ['Integration ease', 'Modular', 'Mixable into materials', 'Direct structural use'],
        ['Best applications', 'Storage tanks, panels', 'Building materials, slurries', 'Composites, direct contact'],
    ]
    return make_table(headers, rows, 'Table 5: Comparison of PCM Encapsulation Techniques')


def generate_section2_modeling():
    """Section 2.3 - Modeling."""
    body = ''
    body += make_heading('2.3 Modeling and Optimization of Thermal Systems', 2)
    
    body += make_paragraph(
        'The design and optimization of PCM-based thermal energy storage systems require sophisticated mathematical modeling and '
        'computational simulation tools [68]. Unlike single-phase heat transfer problems, the melting and solidification of PCMs involve '
        'moving solid-liquid interfaces, latent heat absorption/release, natural convection in the liquid phase, and potentially non-linear '
        'material properties [69].'
    )
    
    body += make_paragraph(
        'The Stefan Problem and Analytical Solutions form the classical mathematical foundation for modeling phase change [70]. '
        'Computational Fluid Dynamics (CFD) Modeling has become the primary tool for simulating PCM behavior in complex, realistic system '
        'configurations [71]. The most widely employed numerical approach is the enthalpy-porosity method, which treats the mushy zone as '
        'a porous medium with porosity equal to the liquid fraction [72]. This approach eliminates the need to explicitly track the moving '
        'solid-liquid interface, greatly simplifying the numerical implementation while providing accurate results for engineering applications.'
    )
    
    body += make_paragraph(
        'Optimization Techniques including topology optimization and genetic algorithms are employed to maximize the thermal performance '
        'of PCM systems [73]. System-level optimization includes the selection and layering of multiple PCMs with cascaded melting '
        'temperatures to maintain more uniform temperature driving forces and improve overall exergetic efficiency [74].'
    )
    
    return body



def generate_section3(image_rids):
    """Generate Section 3 content."""
    body = ''
    body += make_heading('Section 3: Applications of PCMs in Sustainable Development and Clean Energy', 1)
    body += make_heading('3.1 PCMs for Building Energy Management and Energy Efficiency', 2)
    
    body += make_paragraph(
        'The building sector accounts for approximately 40% of global energy consumption and nearly one-third of energy-related carbon '
        'dioxide emissions [75]. The integration of phase change materials into building envelopes and HVAC systems offers a compelling '
        'strategy for reducing building energy consumption and improving occupant thermal comfort [76].'
    )
    
    body += make_paragraph(
        'Integration into Building Envelopes involves incorporating PCMs into the structural or finishing elements that form the thermal '
        'boundary of a building [5]. PCM-enhanced wallboards with melting temperatures of 21-26 degrees C are blended into gypsum '
        'plasterboard during manufacture [9]. Experimental studies have shown that PCM-enhanced building envelopes can reduce peak indoor '
        'temperatures by 2-4 degrees C and reduce daily cooling energy consumption by 15-30% [19].'
    )
    
    body += make_paragraph(
        'Peak Load Shifting and Demand Management represent key economic and grid-level benefits of PCM integration in buildings [20]. '
        'Building-integrated PCMs serve a dual function: improving individual building energy performance while providing grid-level '
        'services through reduced peak demand and improved load factors [21].'
    )
    
    body += make_paragraph(
        'Free Cooling Systems exploit the diurnal temperature variation between day and night. During nighttime hours when ambient '
        'temperatures fall below the PCM melting point, outdoor air is circulated through a PCM heat exchanger to solidify the material '
        'and store coolness. During daytime hours, warm indoor air is passed through the solidified PCM, which absorbs heat and provides '
        'cooling without mechanical refrigeration, achieving energy savings of 30-50% for cooling with minimal electrical energy input [18, 12].'
    )
    
    body += make_heading('3.2 Renewable Energy Integration: Solar Thermal and Battery Thermal Management', 2)
    
    body += make_paragraph(
        'The integration of PCMs with renewable energy systems addresses the fundamental challenge of temporal mismatch between energy '
        'generation and demand [2]. Two applications of particular strategic importance are solar thermal energy storage and battery '
        'thermal management for electric vehicles.'
    )
    
    body += make_paragraph(
        'Solar Water Heating and Domestic Hot Water Systems represent one of the most mature applications of PCMs in renewable energy [34]. '
        'By integrating PCMs with melting temperatures of 45-60 degrees C into solar thermal storage tanks, the storage capacity per unit '
        'volume can be increased by a factor of 2-4 compared to sensible-heat-only water tanks [11]. This enhanced storage capacity '
        'extends the availability of hot water well beyond sunset hours. Field studies have demonstrated solar fractions of 60-80% in '
        'temperate climates with PCM-enhanced systems [15].'
    )
    
    body += make_paragraph(
        'Concentrated Solar Power (CSP) Plants require large-scale, high-temperature thermal energy storage to enable dispatchable '
        'electricity generation during periods without direct solar radiation [34]. The incorporation of latent heat storage using '
        'high-temperature PCMs such as sodium nitrate (melting point 306 degrees C) and eutectic salt mixtures can reduce storage '
        'costs by 20-40% compared to conventional two-tank molten salt systems [14]. Cascaded PCM systems employing multiple PCMs '
        'with progressively lower melting temperatures maintain a more uniform temperature driving force throughout the discharge '
        'process, improving heat transfer rates and thermal efficiency [74].'
    )
    
    return body



def generate_section3_continued(image_rids):
    """Section 3 continued - BTM and specialized apps."""
    body = ''
    
    body += make_paragraph(
        'Battery Thermal Management (BTM) for Electric Vehicles represents a rapidly growing application area for PCMs [4]. Lithium-ion '
        'batteries exhibit optimal performance within a narrow operating temperature window of 15-35 degrees C [10]. Temperatures above '
        'this range accelerate degradation mechanisms, reduce cycle life, and in extreme cases can trigger thermal runaway. PCM-based BTM '
        'systems passively absorb heat generated by the battery during charging and discharging, maintaining cell temperatures near the '
        'PCM melting point without requiring active cooling systems [58]. Paraffin-based composites with expanded graphite are among the '
        'most commonly employed formulations, offering a favorable combination of appropriate melting temperature, adequate thermal '
        'conductivity, and form stability [54].'
    )
    
    body += make_heading('3.3 Industrial, Electronic, and Specialized Applications', 2)
    
    body += make_paragraph(
        'Beyond building energy management and renewable energy systems, PCMs find application across diverse industrial and specialized '
        'domains [3].'
    )
    
    body += make_paragraph(
        'Thermal Management of Electronics is increasingly critical as electronic devices continue to increase in power density while '
        'simultaneously decreasing in physical size [10]. PCM-based solutions are particularly advantageous for transient or pulsed '
        'thermal loads characteristic of portable electronics, telecommunications equipment, and power electronics [50, 55].'
    )
    
    body += make_paragraph(
        'Temperature-Controlled Transport and Logistics represents a commercially significant application of PCMs [60]. The pharmaceutical '
        'industry requires strict temperature control (typically 2-8 degrees C for vaccines and biologics, or 15-25 degrees C for many '
        'medications) throughout the cold chain from manufacturer to patient [35]. PCM-based packaging solutions provide passive thermal '
        'protection for 24-120 hours without requiring electrical power, making them ideal for last-mile delivery and remote locations [43].'
    )
    
    body += make_paragraph(
        'Smart Textiles and Personal Thermal Comfort applications incorporate microencapsulated PCMs into clothing fibers, providing '
        'dynamic thermal buffering that absorbs excess body heat during activity and releases it during rest periods [62, 64].'
    )
    
    body += make_paragraph(
        'Aerospace Thermal Protection Systems employ PCMs to manage the extreme thermal environments experienced by spacecraft and '
        'satellites, where surfaces alternately face direct solar radiation and deep space cold during orbital cycles [17].'
    )
    
    # Figure 5
    body += '<w:p/>'
    body += make_image_paragraph(image_rids['fig5'], 5400000, 3712500,
        'Figure 5: Applications of PCMs in Sustainable Development and Clean Energy')
    body += '<w:p/>'
    
    return body



def generate_table6():
    """Table 6: Summary of PCM Applications."""
    headers = ['Application', 'PCM Type', 'Melting Range (C)', 'Key Benefit', 'Energy Savings', 'Status']
    rows = [
        ['Building walls/ceilings', 'Microencapsulated paraffin', '21-26', 'Reduced peak temperatures', '15-30% cooling', 'Commercial'],
        ['Free cooling systems', 'Salt hydrates, paraffins', '18-24', 'Eliminates daytime AC', '30-50% cooling', 'Demo/Commercial'],
        ['Solar water heating', 'Paraffins, fatty acids', '45-60', 'Increased storage capacity', '20-40% higher solar fraction', 'Commercial'],
        ['Concentrated solar power', 'Molten salts, NaNO3', '250-550', 'Dispatchable power', '20-40% cost reduction', 'Pilot/Demo'],
        ['Battery thermal mgmt', 'Paraffin/EG composites', '35-45', 'Temperature uniformity', 'Extended battery life', 'R&D/Demo'],
        ['Electronics cooling', 'Paraffin, gallium', '40-70', 'Absorbs heat spikes', 'Prevents throttling', 'Commercial'],
        ['Cold chain logistics', 'Eutectic salts, organics', '2-8 / 15-25', 'Passive temperature control', 'Eliminates active cooling', 'Commercial'],
        ['Smart textiles', 'Microencapsulated paraffin', '28-33', 'Dynamic thermal comfort', 'Personal energy savings', 'Commercial'],
        ['Aerospace', 'Metallic PCMs, salts', 'Wide range', 'Temperature moderation', 'Protects equipment', 'Specialized'],
    ]
    return make_table(headers, rows, 'Table 6: Summary of PCM Applications, Operating Conditions, and Benefits')


def generate_section4():
    """Generate Section 4 content."""
    body = ''
    body += make_heading('Section 4: Environmental Impact, Life Cycle Assessment, and Future Directions', 1)
    body += make_heading('4.1 Life Cycle Assessment and Sustainability of PCMs', 2)
    
    body += make_paragraph(
        'As PCM technologies transition from laboratory research to large-scale commercial deployment, a comprehensive understanding of '
        'their environmental footprint becomes essential [1]. Life cycle assessment (LCA) provides a systematic framework for evaluating '
        'environmental impacts across all stages of a product life, from raw material extraction through manufacturing, use, and '
        'end-of-life disposal or recycling [6].'
    )
    
    body += make_paragraph(
        'Environmental Impact Across the Life Cycle varies significantly depending on the PCM type, production method, and application '
        'context [28, 26, 31]. Petroleum-derived paraffin waxes carry embodied energy of 50-80 MJ/kg and carbon footprints of 2.5-4.0 kg '
        'CO2/kg, reflecting the energy-intensive refining processes involved in their production. Bio-based organic PCMs derived from '
        'renewable feedstocks such as coconut oil, palm oil derivatives, or waste cooking oils offer substantially lower environmental '
        'impacts, with embodied energies of 20-40 MJ/kg [29, 30]. Inorganic salt hydrates generally have the lowest production-phase '
        'environmental impact due to the abundance and minimal processing requirements of their constituent materials [33].'
    )
    
    body += make_paragraph(
        'For building-integrated PCMs, studies have demonstrated net energy savings of 15-40% for heating and cooling over building '
        'lifetimes of 20-50 years [75, 76]. The payback period for the environmental investment in PCM production is typically 2-5 years, '
        'after which the system provides net environmental benefits for the remainder of its operational life [19].'
    )
    
    body += make_paragraph(
        'Economic Feasibility and Cost-Benefit Analysis are inextricably linked to environmental sustainability [36]. Pure organic PCMs '
        'cost 5-50 USD/kg, salt hydrates 1-10 USD/kg, and microencapsulated PCMs 20-100 USD/kg [33, 65]. The total system cost including '
        'containment, heat exchangers, and integration represents 2-5 times the raw material cost.'
    )
    
    body += make_paragraph(
        'Contribution to Sustainable Development Goals - PCMs contribute directly to SDG 7 (Affordable and Clean Energy) by enabling '
        'more efficient use of renewable energy sources, SDG 13 (Climate Action) through reduced greenhouse gas emissions from buildings '
        'and industry, SDG 11 (Sustainable Cities) by improving urban energy infrastructure, and SDG 9 (Industry, Innovation and '
        'Infrastructure) through advanced material development [7, 8, 9, 21].'
    )
    
    body += make_paragraph(
        'Bio-Based and Recycled PCMs derived from renewable feedstocks offer reduced petroleum dependence and improved environmental '
        'profiles [29, 30, 44]. Research into waste-derived PCMs, including those from used cooking oils, industrial by-products, and '
        'agricultural residues, represents a promising pathway toward circular economy integration.'
    )
    
    return body



def generate_table7():
    """Table 7: Life Cycle Comparison of PCM Categories."""
    headers = ['Assessment Criterion', 'Organic (Paraffin)', 'Organic (Bio-based)', 'Inorganic (Salt Hydrate)', 'Eutectic']
    rows = [
        ['Raw material source', 'Petroleum-derived', 'Renewable biomass', 'Mineral mining', 'Mixed sources'],
        ['Embodied energy (MJ/kg)', '50-80', '20-40', '10-30', '30-60'],
        ['CO2 footprint (kg CO2/kg)', '2.5-4.0', '0.5-1.5', '0.8-2.0', '1.5-3.0'],
        ['Recyclability', 'Moderate', 'Good', 'Limited', 'Limited'],
        ['Toxicity', 'Low', 'Very low', 'Low-Moderate', 'Variable'],
        ['Cycling life (cycles)', '1000-5000', '500-2000', '500-2000*', '500-3000'],
        ['Cost (USD/kg)', '5-50', '3-20', '1-10', '5-30'],
        ['Payback period (years)', '2-5', '2-4', '1-3', '3-5'],
    ]
    return make_table(headers, rows, 'Table 7: Life Cycle Comparison of PCM Categories')


def generate_section4_emerging():
    """Section 4.2 - Emerging Technologies."""
    body = ''
    body += make_heading('4.2 Emerging Technologies and Smart Integration', 2)
    
    body += make_paragraph(
        'The field of phase change materials is experiencing rapid innovation driven by advances in nanotechnology, materials science, '
        'and digital technologies [47].'
    )
    
    body += make_paragraph(
        'Biomimetic PCMs draw inspiration from biological systems that have evolved sophisticated thermal regulation mechanisms over '
        'millions of years [66, 67]. Researchers are developing PCMs that mimic the hierarchical porous structures found in natural '
        'materials, achieving improved thermal transport and mechanical stability.'
    )
    
    body += make_paragraph(
        'Flexible and Conformable PCMs address the growing demand for thermal management solutions in non-rigid applications such as '
        'wearable electronics, flexible displays, and soft robotics [62, 64]. These materials combine the energy storage capability of '
        'PCMs with the mechanical flexibility required for integration into deformable substrates.'
    )
    
    body += make_paragraph(
        'Photo-Switchable and Triggerable PCMs represent an exciting frontier in which the energy release from PCMs can be controlled '
        'on-demand rather than being solely temperature-driven [53, 55]. These materials incorporate molecular switches that can be '
        'activated by light, electrical signals, or mechanical stimuli to trigger crystallization and heat release at predetermined times.'
    )
    
    body += make_paragraph(
        'Integration with IoT and Smart Building Management Systems enables intelligent, predictive control of PCM charging and '
        'discharging cycles based on weather forecasts, occupancy patterns, and energy price signals [71, 72, 73]. Machine learning '
        'algorithms optimize PCM system operation in real-time, maximizing energy savings and thermal comfort.'
    )
    
    body += make_paragraph(
        '3D-Printed PCM Structures leverage additive manufacturing to create optimized geometries that maximize heat transfer surface '
        'area while minimizing material usage [68, 69, 70]. Topology-optimized lattice structures and functionally graded composites '
        'can be produced that would be impossible to manufacture using conventional techniques.'
    )
    
    return body



def generate_conclusion():
    """Section 4.3 - Conclusion."""
    body = ''
    body += make_heading('4.3 Conclusion: Challenges, Policy, and the Path Forward', 2)
    
    body += make_paragraph(
        'Phase change materials and thermal energy storage technologies offer transformative potential for advancing sustainable '
        'development and accelerating the global clean energy transition [1, 3]. The research community has made remarkable progress '
        'in addressing the fundamental limitations of PCMs through innovative material engineering, advanced encapsulation techniques, '
        'and sophisticated computational design tools.'
    )
    
    body += make_paragraph(
        'Remaining Technical Challenges include the need for PCMs that simultaneously offer high latent heat, adequate thermal '
        'conductivity, long-term stability, and low cost [37, 46]. While individual solutions exist for each of these requirements, '
        'achieving all objectives simultaneously in a single material system remains elusive. Multi-functional composite PCMs that '
        'integrate thermal conductivity enhancement, shape stabilization, and fire retardancy within a single formulation represent '
        'a promising research direction.'
    )
    
    body += make_paragraph(
        'Economic Barriers and Scalable Manufacturing represent significant obstacles to widespread deployment [36, 65, 61]. The '
        'transition from laboratory-scale synthesis to industrial production must maintain material quality and consistency while '
        'achieving cost targets competitive with conventional energy storage and thermal management solutions.'
    )
    
    body += make_paragraph(
        'Regulatory Frameworks and Standards play a crucial role in supporting PCM technology deployment [45, 76, 75]. The development '
        'of standardized testing protocols, performance metrics, and safety certifications is essential for building industry confidence '
        'and enabling fair comparison between competing products and technologies.'
    )
    
    body += make_paragraph(
        'Policy Support and Incentives can significantly accelerate PCM deployment [7, 8, 20]. Building energy codes that recognize '
        'the thermal storage contribution of PCMs, carbon pricing mechanisms that properly value the emissions reductions achieved, and '
        'research funding programs that support scale-up activities can all catalyze market development.'
    )
    
    body += make_paragraph(
        'Interdisciplinary Research and Collaboration will be essential for realizing the full potential of PCM technologies [6, 73, 47]. '
        'The convergence of materials science, thermal engineering, architecture, electrical engineering, and data science creates '
        'opportunities for breakthrough innovations that no single discipline could achieve independently.'
    )
    
    body += make_paragraph(
        'Strategic Foresight and the Global Energy Transition - the convergence of PCM technology with digital technologies, advanced '
        'manufacturing, and circular economy principles positions the field for continued innovation and growing impact on global energy '
        'systems [72, 74, 21]. As the world accelerates its transition away from fossil fuels, the ability to store and manage thermal '
        'energy efficiently will become increasingly critical, ensuring that PCMs remain at the forefront of sustainable energy technology '
        'development for decades to come.'
    )
    
    return body



def generate_references():
    """Generate the references section."""
    refs = [
        '[1] Sharma, A., Tyagi, V. V., Chen, C. R., & Buddhi, D. (2009). Review on thermal energy storage with phase change materials and applications. Renewable and Sustainable Energy Reviews, 13(2), 318-345.',
        '[2] Kenisarin, M., & Mahkamov, K. (2007). Solar energy storage using phase change materials. Renewable and Sustainable Energy Reviews, 11(9), 1913-1965.',
        '[3] Zalba, B., Marin, J. M., Cabeza, L. F., & Mehling, H. (2003). Review on thermal energy storage with phase change: Materials, heat transfer analysis and applications. Applied Thermal Engineering, 23(3), 251-283.',
        '[4] Ling, Z., Zhang, Z., Shi, G., Fang, X., Wang, L., Gao, X., et al. (2014). Review on thermal management systems using PCMs for electronic components, Li-ion batteries and photovoltaic modules. Renewable and Sustainable Energy Reviews, 31, 427-438.',
        '[5] Cabeza, L. F., Castell, A., Barreneche, C., de Gracia, A., & Fernandez, A. I. (2011). Materials used as PCM in thermal energy storage in buildings: A review. Renewable and Sustainable Energy Reviews, 15(3), 1675-1695.',
        '[6] Dincer, I., & Rosen, M. A. (2011). Thermal energy storage: Systems and applications (2nd ed.). John Wiley & Sons.',
        '[7] International Energy Agency. (2014). Technology roadmap: Energy storage. IEA Publications.',
        '[8] Mahlia, T. M. I., Saktisahdan, T. J., Jannifar, A., Hasan, M. H., & Matseelar, H. S. C. (2014). A review of available methods and development on energy storage: Technology update. Renewable and Sustainable Energy Reviews, 33, 532-545.',
        '[9] Kuznik, F., David, D., Johannes, K., & Roux, J. J. (2011). A review on phase change materials integrated in building walls. Renewable and Sustainable Energy Reviews, 15(1), 379-391.',
        '[10] Agyenim, F., Hewitt, N., Eames, P., & Smyth, M. (2010). A review of materials, heat transfer and phase change problem formulation for LHTESS. Renewable and Sustainable Energy Reviews, 14(2), 615-628.',
    ]
    refs += [
        '[11] Gil, A., Medrano, M., Martorell, I., Lazaro, A., Dolado, P., Zalba, B., & Cabeza, L. F. (2010). State of the art on high temperature thermal energy storage for power generation. Part 1. Renewable and Sustainable Energy Reviews, 14(1), 31-55.',
        '[12] Osterman, E., Tyagi, V. V., Butala, V., Rahim, N. A., & Stritih, U. (2012). Review of PCM based cooling technologies for buildings. Energy and Buildings, 49, 37-49.',
        '[13] Hasnain, S. M. (1998). Review on sustainable thermal energy storage technologies. Energy Conversion and Management, 39(11), 1127-1138.',
        '[14] Medrano, M., Gil, A., Martorell, I., Potau, X., & Cabeza, L. F. (2010). State of the art on high-temperature thermal energy storage for power generation. Part 2. Renewable and Sustainable Energy Reviews, 14(1), 56-72.',
        '[15] Farid, M. M., Khudhair, A. M., Razack, S. A. K., & Al-Hallaj, S. (2004). A review on phase change energy storage: Materials and applications. Energy Conversion and Management, 45(9-10), 1597-1615.',
        '[16] Pielichowska, K., & Pielichowski, K. (2014). Phase change materials for thermal energy storage. Progress in Materials Science, 65, 67-123.',
        '[17] Cot-Gores, J., Castell, A., & Cabeza, L. F. (2012). Thermochemical energy storage and conversion: A state-of-the-art review. Renewable and Sustainable Energy Reviews, 16(7), 5207-5224.',
        '[18] Lazaro, A., Dolado, P., Marin, J. M., & Zalba, B. (2009). PCM-air heat exchangers for free-cooling applications in buildings. Energy Conversion and Management, 50(3), 439-443.',
        '[19] Soares, N., Costa, J. J., Gaspar, A. R., & Santos, P. (2013). Review of passive PCM latent heat thermal energy storage systems towards buildings energy efficiency. Energy and Buildings, 59, 82-103.',
        '[20] Navarro, L., de Gracia, A., Niall, D., Castell, A., et al. (2016). Thermal energy storage in building integrated thermal systems: A review. Part 2. Renewable Energy, 85, 1334-1356.',
    ]
    refs += [
        '[21] de Gracia, A., & Cabeza, L. F. (2015). Phase change materials and thermal energy storage for buildings. Energy and Buildings, 103, 414-419.',
        '[22] Abhat, A. (1983). Low temperature latent heat thermal energy storage: Heat storage materials. Solar Energy, 30(4), 313-332.',
        '[23] Lane, G. A. (1983). Solar heat storage: Latent heat materials (Vol. 1). CRC Press.',
        '[24] Mehling, H., & Cabeza, L. F. (2008). Heat and cold storage with PCM: An up to date introduction into basics and applications. Springer.',
        '[25] Akeiber, H., Nejat, P., Majid, M. Z. A., et al. (2016). A review on PCM for sustainable passive cooling in building envelopes. Renewable and Sustainable Energy Reviews, 60, 1470-1497.',
        '[26] Himran, S., Suwono, A., & Mansoori, G. A. (1994). Characterization of alkanes and paraffin waxes for application as PCM. Energy Sources, 16(1), 117-128.',
        '[27] Dimaano, M. N. R., & Watanabe, T. (2002). The capric-lauric acid and pentadecane combination as PCM for cooling applications. Applied Thermal Engineering, 22(4), 365-377.',
        '[28] Sari, A. (2003). Thermal reliability test of some fatty acids as PCMs for solar thermal latent heat storage. Energy Conversion and Management, 44(14), 2277-2287.',
        '[29] Yuan, Y., Zhang, N., Tao, W., Cao, X., & He, Y. (2014). Fatty acids as phase change materials: A review. Renewable and Sustainable Energy Reviews, 29, 482-498.',
        '[30] Karaman, S., Karaipekli, A., Sari, A., & Bicer, A. (2011). PEG/diatomite composite as a novel form-stable PCM for thermal energy storage. Solar Energy Materials and Solar Cells, 95(7), 1647-1653.',
    ]
    return refs



def generate_references_continued():
    """Generate remaining references."""
    refs = [
        '[31] Tyagi, V. V., & Buddhi, D. (2007). PCM thermal storage in buildings: A state of art. Renewable and Sustainable Energy Reviews, 11(6), 1146-1166.',
        '[32] Oro, E., de Gracia, A., Castell, A., Farid, M. M., & Cabeza, L. F. (2012). Review on PCMs for cold thermal energy storage applications. Applied Energy, 99, 513-533.',
        '[33] Mohamed, S. A., Al-Sulaiman, F. A., Ibrahim, N. I., et al. (2017). A review on current status and challenges of inorganic PCMs for TES systems. Renewable and Sustainable Energy Reviews, 70, 1072-1089.',
        '[34] Liu, M., Saman, W., & Bruno, F. (2012). Review on storage materials and thermal performance enhancement for high temperature PCM storage. Renewable and Sustainable Energy Reviews, 16(4), 2118-2132.',
        '[35] Sharma, R. K., Ganesan, P., Tyagi, V. V., et al. (2015). Developments in organic solid-liquid PCMs and their applications in TES. Energy Conversion and Management, 95, 193-228.',
        '[36] Kousksou, T., Bruel, P., Jamil, A., El Rhafiki, T., & Zeraouli, Y. (2014). Energy storage: Applications and challenges. Solar Energy Materials and Solar Cells, 120, 59-80.',
        '[37] Lin, Y., Jia, Y., Alva, G., & Fang, G. (2018). Review on thermal conductivity enhancement of PCMs in thermal energy storage. Renewable and Sustainable Energy Reviews, 82, 2730-2742.',
        '[38] Fan, L., & Khodadadi, J. M. (2011). Thermal conductivity enhancement of PCMs for thermal energy storage: A review. Renewable and Sustainable Energy Reviews, 15(1), 24-46.',
        '[39] Dhaidan, N. S., & Khodadadi, J. M. (2015). Melting and convection of PCMs in different shape containers: A review. Renewable and Sustainable Energy Reviews, 43, 449-477.',
        '[40] Rathod, M. K., & Banerjee, J. (2013). Thermal stability of PCMs used in latent heat energy storage systems: A review. Renewable and Sustainable Energy Reviews, 18, 246-258.',
        '[41] Cabeza, L. F., Castellon, C., Nogues, M., et al. (2007). Use of microencapsulated PCM in concrete walls for energy savings. Energy and Buildings, 39(2), 113-119.',
        '[42] Gunther, E., Hiebler, S., Mehling, H., & Redlich, R. (2009). Enthalpy of PCMs as a function of temperature. International Journal of Thermophysics, 30(4), 1257-1269.',
        '[43] Sari, A., & Karaipekli, A. (2007). Thermal conductivity and latent heat characteristics of paraffin/expanded graphite composite PCM. Applied Thermal Engineering, 27(8-9), 1271-1277.',
        '[44] Alva, G., Lin, Y., & Fang, G. (2018). An overview of thermal energy storage systems. Energy, 144, 341-378.',
        '[45] Pandey, A. K., Hossain, M. S., Tyagi, V. V., et al. (2018). Novel approaches and recent developments on potential applications of PCMs in solar energy. Renewable and Sustainable Energy Reviews, 82, 281-323.',
        '[46] Huang, X., Alva, G., Jia, Y., & Fang, G. (2017). Morphological characterization and applications of PCMs in thermal energy storage: A review. Renewable and Sustainable Energy Reviews, 72, 128-145.',
        '[47] Milian, Y. E., Gutierrez, A., Grageda, M., & Ushak, S. (2017). A review on encapsulation techniques for inorganic PCMs. Renewable and Sustainable Energy Reviews, 73, 983-999.',
        '[48] Zhao, C. Y., & Wu, Z. G. (2011). Heat transfer enhancement of high temperature TES using metal foams and expanded graphite. Solar Energy Materials and Solar Cells, 95(2), 636-643.',
        '[49] Xiao, X., Zhang, P., & Li, M. (2013). Preparation and thermal characterization of paraffin/metal foam composite PCM. Applied Energy, 112, 1357-1366.',
        '[50] Khodadadi, J. M., & Hosseinizadeh, S. F. (2007). Nanoparticle-enhanced PCMs (NEPCM) with great potential for improved TES. International Communications in Heat and Mass Transfer, 34(5), 534-543.',
    ]
    refs += [
        '[51] Leong, K. Y., Abdul Rahman, M. R., & Gurunathan, B. A. (2019). Nano-enhanced PCMs: A review of thermo-physical properties and challenges. Journal of Energy Storage, 21, 18-31.',
        '[52] Wu, S., Zhu, D., Zhang, X., & Huang, J. (2010). Preparation and melting/freezing characteristics of Cu/paraffin nanofluid as PCM. Energy & Fuels, 24(3), 1894-1898.',
        '[53] Zhang, P., Xiao, X., & Ma, Z. W. (2016). A review of the composite PCMs: Fabrication, characterization, mathematical modeling and application. Applied Energy, 165, 472-510.',
        '[54] Sari, A., & Karaipekli, A. (2009). Preparation and thermal reliability of palmitic acid/expanded graphite composite as form-stable PCM. Solar Energy Materials and Solar Cells, 93(5), 571-576.',
        '[55] Shi, J. N., Ger, M. D., Liu, Y. M., et al. (2013). Improving thermal conductivity and shape-stabilization of PCMs using nanographite. Carbon, 51, 365-372.',
        '[56] Agyenim, F., Eames, P., & Smyth, M. (2009). Heat transfer enhancement in a medium temperature TES heat exchanger using fins. Solar Energy, 83(9), 1509-1520.',
        '[57] Mat, S., Al-Abidi, A. A., Sopian, K., et al. (2013). Enhance heat transfer for PCM melting in triplex tube with internal-external fins. Energy Conversion and Management, 74, 223-236.',
        '[58] Javani, N., Dincer, I., Naterer, G. F., & Yilbas, B. S. (2014). Heat transfer and thermal management with PCMs in Li-ion battery cells for EVs. International Journal of Heat and Mass Transfer, 72, 690-703.',
        '[59] Jamekhorshid, A., Sadrameli, S. M., & Farid, M. (2014). A review of microencapsulation methods of PCMs as TES medium. Renewable and Sustainable Energy Reviews, 31, 531-542.',
        '[60] Regin, A. F., Solanki, S. C., & Saini, J. S. (2008). Heat transfer characteristics of TES system using PCM capsules: A review. Renewable and Sustainable Energy Reviews, 12(9), 2438-2458.',
        '[61] Salunkhe, P. B., & Shembekar, P. S. (2012). A review on effect of PCM encapsulation on the thermal performance of a system. Renewable and Sustainable Energy Reviews, 16(8), 5603-5616.',
        '[62] Mondal, S. (2008). Phase change materials for smart textiles - An overview. Applied Thermal Engineering, 28(11-12), 1536-1550.',
        '[63] Zhao, C. Y., & Zhang, G. H. (2011). Review on microencapsulated PCMs: Fabrication, characterization and applications. Renewable and Sustainable Energy Reviews, 15(8), 3813-3832.',
        '[64] Sarier, N., & Onder, E. (2012). Organic PCMs and their textile applications: An overview. Thermochimica Acta, 540, 7-60.',
        '[65] Tyagi, V. V., Kaushik, S. C., Tyagi, S. K., & Akiyama, T. (2011). Development of PCM based microencapsulated technology for buildings: A review. Renewable and Sustainable Energy Reviews, 15(2), 1373-1391.',
        '[66] Khadiran, T., Hussein, M. Z., Zainal, Z., & Rusli, R. (2016). Shape-stabilised n-octadecane/activated carbon nanocomposite PCM. Journal of the Taiwan Institute of Chemical Engineers, 55, 26-34.',
        '[67] Wen, R., Zhang, X., Huang, Z., et al. (2017). Preparation and thermal properties of fatty acid/diatomite form-stable composite PCM. Solar Energy Materials and Solar Cells, 178, 273-279.',
        '[68] Al-Abidi, A. A., Mat, S., Sopian, K., et al. (2013). Numerical study of PCM solidification in a triplex tube heat exchanger. International Journal of Heat and Mass Transfer, 61, 684-695.',
        '[69] Voller, V. R., & Prakash, C. (1987). A fixed grid numerical modelling methodology for phase-change problems. International Journal of Heat and Mass Transfer, 30(8), 1709-1719.',
        '[70] Dutil, Y., Rousse, D. R., Salah, N. B., et al. (2011). A review on PCMs: Mathematical modeling and simulations. Renewable and Sustainable Energy Reviews, 15(1), 112-130.',
    ]
    refs += [
        '[71] Jegadheeswaran, S., & Pohekar, S. D. (2009). Performance enhancement in latent heat thermal storage system: A review. Renewable and Sustainable Energy Reviews, 13(9), 2225-2244.',
        '[72] Khudhair, A. M., & Farid, M. M. (2004). A review on energy conservation in building applications with thermal storage using PCMs. Energy Conversion and Management, 45(2), 263-275.',
        '[73] Baetens, R., Jelle, B. P., & Gustavsen, A. (2010). Phase change materials for building applications: A state-of-the-art review. Energy and Buildings, 42(9), 1361-1368.',
        '[74] Xu, H. J., Zhao, C. Y., & Liang, D. (2019). Analytical considerations of thermal storage and interface evolution of a PCM with/without porous media. Int. J. Numerical Methods for Heat & Fluid Flow, 30(1), 373-400.',
        '[75] Bland, A., Khzouz, M., Statheros, T., & Gkanas, E. I. (2017). PCMs for residential building applications: A short review. Buildings, 7(3), 78.',
        '[76] Souayfane, F., Fardoun, F., & Biwole, P. H. (2016). Phase change materials (PCM) for cooling applications in buildings: A review. Energy and Buildings, 129, 396-431.',
    ]
    return refs



def get_content_types_xml(image_count):
    """Generate [Content_Types].xml."""
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    xml += '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    xml += '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    xml += '<Default Extension="xml" ContentType="application/xml"/>'
    xml += '<Default Extension="png" ContentType="image/png"/>'
    xml += '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    xml += '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    xml += '</Types>'
    return xml


def get_rels_xml():
    """Generate _rels/.rels."""
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    xml += '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    xml += '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    xml += '</Relationships>'
    return xml


def get_word_rels_xml(image_rids):
    """Generate word/_rels/document.xml.rels."""
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    xml += '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    xml += '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    
    rid_num = 2
    for key, rid in image_rids.items():
        filename = {
            'fig1': 'Figure_1_PCM_Classification.png',
            'fig2': 'Figure_2_Thermal_Conductivity_Enhancement.png',
            'fig3': 'Figure_3_Temperature_Profile.png',
            'fig4': 'Figure_4_Encapsulation_Methods.png',
            'fig5': 'Figure_5_PCM_Applications.png',
            'fig6': 'Figure_6_TES_Schematic.png',
        }[key]
        xml += f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{filename}"/>'
        rid_num += 1
    
    xml += '</Relationships>'
    return xml



def get_styles_xml():
    """Generate word/styles.xml with heading styles."""
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    xml += '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    
    # Default style
    xml += '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    xml += '<w:name w:val="Normal"/>'
    xml += '<w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>'
    xml += '<w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
    xml += '</w:style>'
    
    # Heading 1
    xml += '<w:style w:type="paragraph" w:styleId="Heading1">'
    xml += '<w:name w:val="heading 1"/>'
    xml += '<w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr>'
    xml += '<w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="1B3C78"/></w:rPr>'
    xml += '</w:style>'
    
    # Heading 2
    xml += '<w:style w:type="paragraph" w:styleId="Heading2">'
    xml += '<w:name w:val="heading 2"/>'
    xml += '<w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>'
    xml += '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="2E5090"/></w:rPr>'
    xml += '</w:style>'
    
    # Table style
    xml += '<w:style w:type="table" w:styleId="TableGrid">'
    xml += '<w:name w:val="Table Grid"/>'
    xml += '<w:tblPr><w:tblBorders>'
    xml += '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    xml += '</w:tblBorders></w:tblPr>'
    xml += '</w:style>'
    
    xml += '</w:styles>'
    return xml



def build_docx():
    """Assemble and write the complete DOCX file."""
    print("Building DOCX file...")
    
    # Image relationship IDs
    image_rids = {
        'fig1': 'rId10',
        'fig2': 'rId11',
        'fig3': 'rId12',
        'fig4': 'rId13',
        'fig5': 'rId14',
        'fig6': 'rId15',
    }
    
    # Build document body
    body_content = ''
    body_content += generate_document_body(image_rids)
    body_content += generate_section1(image_rids)
    body_content += generate_section1_continued(image_rids)
    body_content += generate_section1_classification(image_rids)
    body_content += generate_table2()
    body_content += generate_section1_challenges()
    body_content += generate_table3()
    body_content += generate_section2(image_rids)
    body_content += generate_table4()
    body_content += generate_section2_encapsulation(image_rids)
    body_content += generate_table5()
    body_content += generate_section2_modeling()
    body_content += generate_section3(image_rids)
    body_content += generate_section3_continued(image_rids)
    body_content += generate_table6()
    body_content += generate_section4()
    body_content += generate_table7()
    body_content += generate_section4_emerging()
    body_content += generate_conclusion()
    
    # References
    body_content += make_heading('References', 1)
    all_refs = generate_references() + generate_references_continued()
    for ref in all_refs:
        body_content += make_paragraph(ref, font_size="20")
    
    # Wrap in document XML
    doc_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    doc_xml += '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    doc_xml += 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    doc_xml += 'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    doc_xml += 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    doc_xml += 'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    doc_xml += '<w:body>'
    doc_xml += body_content
    doc_xml += '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
    doc_xml += '</w:body></w:document>'
    
    # Create the DOCX ZIP file
    with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', get_content_types_xml(6))
        zf.writestr('_rels/.rels', get_rels_xml())
        zf.writestr('word/_rels/document.xml.rels', get_word_rels_xml(image_rids))
        zf.writestr('word/document.xml', doc_xml)
        zf.writestr('word/styles.xml', get_styles_xml())
        
        # Add image files
        image_files = {
            'Figure_1_PCM_Classification.png': os.path.join(FIGURES_DIR, 'Figure_1_PCM_Classification.png'),
            'Figure_2_Thermal_Conductivity_Enhancement.png': os.path.join(FIGURES_DIR, 'Figure_2_Thermal_Conductivity_Enhancement.png'),
            'Figure_3_Temperature_Profile.png': os.path.join(FIGURES_DIR, 'Figure_3_Temperature_Profile.png'),
            'Figure_4_Encapsulation_Methods.png': os.path.join(FIGURES_DIR, 'Figure_4_Encapsulation_Methods.png'),
            'Figure_5_PCM_Applications.png': os.path.join(FIGURES_DIR, 'Figure_5_PCM_Applications.png'),
            'Figure_6_TES_Schematic.png': os.path.join(FIGURES_DIR, 'Figure_6_TES_Schematic.png'),
        }
        
        for filename, filepath in image_files.items():
            zf.write(filepath, f'word/media/{filename}')
    
    print(f"DOCX file created: {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE)} bytes")


if __name__ == '__main__':
    build_docx()
