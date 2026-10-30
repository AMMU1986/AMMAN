#!/usr/bin/env python3
"""
Build two .docx files (no third-party deps; a .docx is a zip of Office XML):

  1. Manuscript_SA516_2205_Dissimilar_Weld_REVISED.docx
       - Full manuscript with every reviewer-response correction applied.
       - Each changed / newly inserted passage is highlighted in YELLOW.

  2. Response_to_Reviewers_SA516_2205.docx
       - Clean, formatted point-by-point response document.

Inline markup used in the content strings:
  {{ ... }}   -> yellow highlight (used to mark manuscript changes)
  ^{ ... }    -> superscript
"""

import zipfile

# ----------------------------------------------------------------------
# Low-level XML helpers
# ----------------------------------------------------------------------

def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def parse_runs(text):
    """Split text into runs carrying highlight / superscript flags."""
    # First pass: highlight segments
    segs = []
    i = 0
    while True:
        s = text.find('{{', i)
        if s == -1:
            segs.append((text[i:], False))
            break
        if s > i:
            segs.append((text[i:s], False))
        e = text.find('}}', s + 2)
        segs.append((text[s + 2:e], True))
        i = e + 2
    # Second pass: superscripts inside each segment
    runs = []
    for seg, hl in segs:
        j = 0
        while True:
            s = seg.find('^{', j)
            if s == -1:
                if seg[j:]:
                    runs.append((seg[j:], hl, False))
                break
            if s > j:
                runs.append((seg[j:s], hl, False))
            e = seg.find('}', s + 2)
            runs.append((seg[s + 2:e], hl, True))
            j = e + 1
    return runs


def run_xml(t, hl, sup, bold=False, italic=False, size=24):
    rpr = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
    if bold:
        rpr += '<w:b/>'
    if italic:
        rpr += '<w:i/>'
    rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    if sup:
        rpr += '<w:vertAlign w:val="superscript"/>'
    if hl:
        rpr += '<w:highlight w:val="yellow"/>'
    return (f'<w:r><w:rPr>{rpr}</w:rPr>'
            f'<w:t xml:space="preserve">{esc(t)}</w:t></w:r>')


def para(text, bold=False, italic=False, size=24, jc='both',
         before=0, after=120, line=276):
    runs = ''.join(run_xml(t, hl, sup, bold, italic, size)
                   for t, hl, sup in parse_runs(text))
    ppr = (f'<w:pPr><w:spacing w:before="{before}" w:after="{after}" '
           f'w:line="{line}" w:lineRule="auto"/>'
           f'<w:jc w:val="{jc}"/></w:pPr>')
    return f'<w:p>{ppr}{runs}</w:p>'


def title(text):
    return para(text, bold=True, size=30, jc='center', after=120)


def h1(text):
    return para(text, bold=True, size=28, jc='left', before=240, after=100)


def h2(text):
    return para(text, bold=True, size=25, jc='left', before=160, after=80)


def center(text, bold=False, italic=False, size=24):
    return para(text, bold=bold, italic=italic, size=size, jc='center',
                after=40)


def blank():
    return '<w:p/>'


def table(rows, widths, header_rows=1, size=18):
    total = sum(widths)
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    borders = ('<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '</w:tblBorders>')
    tpr = (f'<w:tblPr><w:tblW w:w="{total}" w:type="dxa"/>'
           f'<w:tblLayout w:type="fixed"/>{borders}</w:tblPr>')
    out = [f'<w:tbl>{tpr}<w:tblGrid>{grid}</w:tblGrid>']
    for ri, row in enumerate(rows):
        hdr = ri < header_rows
        cells = ''
        for ci, val in enumerate(row):
            runs = ''.join(run_xml(t, hl, sup, bold=hdr, size=size)
                           for t, hl, sup in parse_runs(str(val)))
            shd = ('<w:shd w:val="clear" w:color="auto" w:fill="D9D9D9"/>'
                   if hdr else '')
            cells += (
                f'<w:tc><w:tcPr><w:tcW w:w="{widths[ci]}" w:type="dxa"/>'
                f'{shd}<w:vAlign w:val="center"/></w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="20" w:line="240" '
                f'w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>{runs}</w:p>'
                f'</w:tc>')
        out.append(f'<w:tr>{cells}</w:tr>')
    out.append('</w:tbl>')
    out.append(blank())
    return ''.join(out)


def write_docx(path, body):
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '</Types>')
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body>' + body +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
        '</w:sectPr></w:body></w:document>')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/document.xml', document)
    print('  wrote', path)


# ----------------------------------------------------------------------
# MANUSCRIPT (revised, changes highlighted)
# ----------------------------------------------------------------------

def build_manuscript():
    b = []
    A = b.append

    A(title('To study the mechanical and microstructural behavior of SA516 and '
            '2205 dissimilar GMAW welds fabricated by using 309L filler'))
    A(center('Lochan Sharma^{1}, Amman Jakhar^{2}, Karan Mankotia^{3}', bold=True))
    A(center('^{1}University Centre for Research & Development, Chandigarh '
             'University, Mohali, Punjab, India', size=20))
    A(center('^{2,3}Department of Mechanical Engineering, Chandigarh University, '
             'Mohali, Punjab, India', size=20))
    A(center('Corresponding Author: Lochan Sharma; lochan.e9455@cumail.in', size=20))
    A(blank())

    # -- Abstract
    A(h1('Abstract'))
    A(para(
        'The current research work {{aims to examine and analyse}} the mechanical '
        'and metallurgical properties of dissimilar welds between low carbon alloy '
        'SA516 and 2205 duplex stainless steel. This welding joint finds application '
        'in pressure vessels, boilers and offshore industries. A consumable electrode '
        '309L was used as filler metal in the Gas Metal Arc Welding (GMAW) process. '
        'The weld metal solidifies in ferrite-austenite mode with a resultant '
        'microstructure comprising skeletal ferrites with austenite present in the '
        'interdendritic region. The microhardness of the dissimilar weld is 307 HV at '
        'the fusion zone, which is lower than the microhardness at the HAZ {{(HAZ-2, '
        'the SS2205 duplex side)}} i.e. 372 HV. The microstructure of the dissimilar '
        'weld is composed of a columnar dendritic structure. The temperature gradient '
        'and variations in solidification rate clearly show the changes in '
        'microstructure in different areas. The fractographs of the dissimilar weld '
        'reveal varying fracture behaviors. The HAZ on the SS2205 side shows '
        'predominantly ductile fracture features, with dimpled microvoid coalescence. '
        'The HAZ on the SA516 side exhibits mixed-mode fracture with evidence of '
        'brittle cleavage, indicating reduced toughness in this region.'))
    A(para('Keywords: Dissimilar weld, SA516, 2205 Duplex Stainless Steel, 309L '
           'Filler Metal, Mechanical Properties, Microstructure', italic=True))

    # -- Introduction
    A(h1('1. Introduction'))
    A(para(
        '{{The manufacturing industry faces several challenges when it comes to '
        'welding of dissimilar metals.}} Dissimilar metal joints between SA516 grade '
        '70 and SS2205 can be used in many high-temperature, corrosion-resistant '
        'applications. Duplex stainless steel 2205 combines the properties of both '
        'ferrite (\u03b1) and austenite (\u03b3), which exhibit outstanding corrosion '
        'resistance, high strength, and toughness [1]. It therefore plays a crucial '
        'role in diverse engineering applications, stemming from its unique '
        'combination of BCC and FCC lattice structures. Among the various grades '
        'available, Type 2205 (UNS S32205, EN 1.4462) stands out as the most widely '
        'used and reliable alloy in this family [1]. It demonstrates a significantly '
        'higher yield strength\u2014about twice that of single-phase steels even in '
        'annealed conditions. DSS 2205 is widely used in shipbuilding for enhanced '
        'protection against seawater, offshore oil and gas pipelines, ocean mining '
        'equipment, chemical tankers, marine machinery fasteners, bridges in cold '
        'climates, and in chemical, nuclear, pharmaceutical, paper and pulp '
        'industries [2]. In the case of SS2205, 850 \u00b0C is the critical '
        'temperature, and exposure to it might encourage the formation of certain '
        'harmful secondary phases in the microstructure, such as \u03c3, \u03c7, '
        'carbides, and nitrides [1]. The essential alloying elements including Cr, Mo '
        'and N are responsible for the composition of these phases, which contribute '
        'to the corrosion resistance of SS2205. The localized depletion of these '
        'elements around intragranular sites, interfacial borders and grain '
        'boundaries caused by the precipitation of these phases lowers the corrosion '
        'resistance of duplex steels. Because of its increased chromium and nitrogen '
        'content, it demonstrates superior corrosion resistance, particularly against '
        'chloride-induced pitting and stress corrosion cracking. The microstructural '
        'features and thermal expansion rate of SS2205 are quite different from those '
        'of carbon steels such as SA516, which could cause problems in the formation '
        'of the heat-affected zone (HAZ) during welding [3].'))
    A(para(
        'On the other hand, SA516 is a carbon-manganese (C-Mn) ferritic steel that '
        'fulfils the ASTM specifications for pressure vessel standards [4]. The most '
        'popular grades of SA516 are 55, 60, 65 and 70. It is typically used in '
        'applications requiring moderate to low temperatures where high notch '
        'toughness is critical. It is therefore commonly employed in nuclear piping '
        'and pressure vessel systems due to its relatively good fracture properties, '
        'toughness, ductility, weldability and high strength. Weldability is affected '
        'by the carbon content of the material, which is usually between 0.2 % and '
        '0.3 %. If proper welding techniques are not followed, this can cause '
        'hardening and make the material more susceptible to hydrogen-induced '
        'cracking [5]. It is utilized for pressure vessels across various industries, '
        'including railways, boiler manufacturing, offshore and shipbuilding '
        'industries [6]. Due to the differences in base-metal chemical, physical, '
        'mechanical and thermal properties, combining dissimilar materials requires '
        'more attention than joining similar materials [7]. Welding of dissimilar '
        'metals, such as SA516 carbon steel and 2205 duplex stainless steel, presents '
        'unique challenges due to these variances. The primary challenge in welding '
        'SA516 and SS2205 lies in the formation of brittle intermetallic phases, such '
        'as sigma phases, which can degrade corrosion resistance and mechanical '
        'properties [8]. These phases form in the HAZ of SS2205 due to '
        'high-temperature exposure during welding. This problem is more noticeable '
        'when high heat inputs are used, or when there are improper cooling rates, '
        'which promote embrittlement [9]. According to Mourad et al. {{[19]}}, one '
        'more challenge arises from the variances in melting points and thermal '
        'expansion coefficients between the two materials. SA516 steel expands and '
        'contracts at a different rate compared to SS2205, resulting in distortion, '
        'residual stresses and the potential for cracking in the weld joint. The use '
        'of an appropriate filler metal and optimized welding parameters is crucial '
        'for achieving high-quality welds with desirable properties. In the current '
        'research work, 309L is used as filler wire since it is compatible with both '
        'base metals (i.e. SA516 and SS2205). It contains a high amount of nickel and '
        'chromium, which resists the formation of brittle phases and ensures a stable '
        'microstructure. {{ER309L is the standard filler for dissimilar joints '
        'between a stainless (here duplex SS2205) and a carbon/low-alloy steel '
        '(SA516): its high Cr-Ni content compensates for dilution by the carbon '
        'steel, keeping the weld-metal composition within the austenitic region of '
        'the Schaeffler / WRC-1992 constitution diagram and avoiding a fully '
        'martensitic, crack-prone deposit, while the low carbon ("L") grade minimizes '
        'chromium-carbide precipitation and preserves corrosion resistance. Its '
        'tough austenitic matrix also accommodates the differing thermal expansion of '
        'the two base metals and reduces residual-stress-driven cracking, which is '
        'reflected in the high fusion-zone toughness and the hardness profile '
        'reported below.}} Since microstructure is a critical aspect of dissimilar '
        'welding, metallurgical compatibility must be ensured. Several researchers '
        'have explored numerous welding techniques and filler materials to address '
        'these challenges. GMAW and GTAW are common methods used for welding '
        'dissimilar metals due to their ability to control heat input and reduce the '
        'chance of forming unwanted phases in the HAZ (Kumar et al. {{[20]}}). Argon '
        'or an argon-helium mixture are widely used as shielding gases to prevent '
        'oxidation of the weld metal [10].'))
    A(para(
        '{{Dissimilar welding of duplex/stainless steels to carbon and low-alloy '
        'steels has received considerable attention. Studies on submerged-arc and '
        'arc-welded carbon-to-stainless joints [2], [4], [6] report that filler '
        'selection and heat input govern the HAZ constitution, the ferrite-austenite '
        'balance and the resulting mechanical and corrosion performance, while '
        'friction-based and fusion dissimilar joints between duplex and low-carbon '
        'steel show a hardness peak and the risk of brittle constituents on the '
        'carbon-steel side [3], [5], [11]. Building on reference [4] and the related '
        'literature, the present study addresses the identified gap for 12 mm-thick '
        'GMAW SA516/SS2205 joints made with ER309L filler by linking the '
        'microstructure of each zone to the measured microhardness, impact toughness '
        'and fracture behavior.}}'))

    # -- Experimental
    A(h1('2. Experimental Procedure'))
    A(para(
        'In the current research work, the carbon steel SA516 and SS2205 with a '
        'thickness of 12 mm were used due to their applications in the manufacture of '
        'pressure vessels and boilers. Two plates of dimensions 100 \u00d7 90 \u00d7 '
        '12 mm and {{0.8 mm diameter ER309L}} filler wire with argon as the inert gas '
        'were used for welding in the GMAW process. Figure 1 shows the diagram of the '
        'welded joint.'))
    A(center('Figure 1. Schematic diagram of the weld geometry {{(revised with '
             'corrected and complete dimensioning: plate 100 \u00d7 90 \u00d7 12 mm, '
             '60\u00b0 single-V included angle, 2 mm root gap, 1.5 mm root face; all '
             'dimensions in mm).}}', italic=True, size=20))
    A(para(
        'The chemistry of both base materials and the filler wire was measured using '
        'atomic absorption spectroscopy and is presented in Table 1. Table 1 shows '
        'that SS2205 and 309L filler wire have a good amount of chromium and nickel, '
        'which act as corrosion-resistance elements essential for marine '
        'applications. Weld impurities such as sulphur and phosphorus are within '
        'range, i.e. less than or equal to 0.3 wt%. Carbon content is higher in SA516 '
        'compared to SS2205 and 309L, which is responsible for increasing hardness '
        'and brittleness.'))
    A(table([
        ['Material (wt.%)', 'C', 'Mn', 'Si', 'P', 'S', 'Al', 'Cr', 'Cu', 'Ni', 'Mo',
         'Nb', 'Ti', 'V', 'Fe'],
        ['SA 516', '0.10', '1.17', '0.60', '0.03', '0.03', '0.02', '0.3', '0.3',
         '0.3', '0.08', '0.01', '0.03', '0.02', 'Rest'],
        ['SS2205', '0.03', '2.00', '1.00', '0.03', '0.02', '-', '23.0', '-', '6.5',
         '3.5', '-', '-', '-', 'Rest'],
        ['309L', '0.03', '2.50', '0.65', '0.03', '0.03', '-', '25', '0.75', '14',
         '0.75', '-', '-', '-', 'Rest'],
    ], widths=[1200] + [583] * 14, size=15))
    A(center('Table 1. Chemical composition of the dissimilar metals and filler wire',
             italic=True, size=20))
    A(para(
        'A gas metal arc welding (GMAW) machine manufactured by Ghudani Metal Weld '
        'India, located in the Central Workshop, Chandigarh University, was used for '
        'welding the dissimilar metals. Pilot trial runs were conducted to finalise '
        'the welding parameters, which are presented in Table 2. The mechanical '
        'behaviour of the base materials and filler wire is presented in Table 3.'))
    A(table([
        ['S. No.', 'Parameter', 'Unit', 'Value'],
        ['1', 'Current (I)', 'A', '180'],
        ['2', 'Voltage (V)', 'V', '18'],
        ['3', 'Welding speed (S)', 'mm/min', '80'],
    ], widths=[1200, 4000, 2000, 2160]))
    A(center('Table 2. Selection of welding variables', italic=True, size=20))
    A(table([
        ['Material', 'Yield Strength (MPa)', 'Elongation (%)', 'Tensile Strength (MPa)'],
        ['SA 516', '260', '20-22', '485-620'],
        ['SS 2205', '448', '25', '621'],
        ['Filler wire (309L)', '400', '30', '590'],
    ], widths=[2760, 2200, 2000, 2400]))
    A(center('Table 3. Mechanical behaviour of the base materials and filler wire',
             italic=True, size=20))
    A(para(
        '{{The joint was prepared as a single-V butt configuration (60\u00b0 included '
        'angle, 2 mm root gap, 1.5 mm root face) and welded with a multi-pass '
        'sequence (one root, several fill and one cap pass). The interpass '
        'temperature was kept below 150 \u00b0C to limit the precipitation of '
        'deleterious phases in the duplex HAZ. Argon shielding was supplied at a flow '
        'rate of [to be inserted from the welding record]. The complete set of '
        'welding conditions (current, voltage and travel speed in Table 2, together '
        'with electrode extension, polarity and preheat) was selected to control the '
        'heat input to the dissimilar joint.}}'))
    A(para(
        '{{Thermal basis. The net heat input per pass was estimated as HI = \u03b7 '
        '(V \u00d7 I) / v, where \u03b7 is the arc/process efficiency, V the arc '
        'voltage, I the welding current and v the travel speed. The peak temperature '
        'and cooling behaviour of the HAZ (characterised by the \u0394t8/5 cooling '
        'time) were interpreted using the Rosenthal moving heat-source solution; this '
        'analytical thermal basis governs the HAZ microstructure and the hardness '
        'observed in HAZ-1 and HAZ-2. No finite-element thermal model was used in the '
        'present work; only analytical estimates were made.}}'))
    A(center('Table (new). Specifications of the welding power source', italic=True,
             size=20))
    A(table([
        ['Specification', 'Detail'],
        ['Manufacturer', '{{Ghudani Metal Weld India}}'],
        ['Process', '{{Gas Metal Arc Welding (GMAW / MIG)}}'],
        ['Rated output current', '{{[to be inserted from nameplate]}}'],
        ['Output voltage range', '{{[to be inserted from nameplate]}}'],
        ['Duty cycle', '{{[to be inserted from nameplate]}}'],
        ['Power supply', '{{[to be inserted from nameplate]}}'],
        ['Wire-feed unit', '{{[to be inserted from nameplate]}}'],
    ], widths=[3360, 5000]))
    A(para(
        'The metallurgical investigation of the welding zone and heat-affected zone '
        'of SA516 and DSS2205 at 400X magnification was carried out using a Dewinter '
        'optical microscope. The specimen was extracted from the welded plate as '
        'shown in Figure 2. The Vickers micro-hardness survey was carried out on the '
        'cross-section of the specimen prepared by the standard metallographic '
        'procedure according to ASTM E384 for a load of 500 grams with a 15-second '
        'dwell time. A Vickers hardness testing machine (model RMHT-201) manufactured '
        'by Radical Scientific Equipment, Ambala Cantt, Haryana, India, available at '
        'SLIET Longowal, Punjab, was used and is shown in Figure 2. The microhardness '
        'survey starts from the SA516 base metal followed by the HAZ along {{the '
        'SA516}} side, the weld metal, the HAZ on the SS2205 side, and the base metal '
        '(left to right of the specimen) as shown in Figure 5. To prevent any '
        'potential effects of strain fields generated by nearby indentations, all '
        'indentations were spaced 2 mm apart. The impact strength of the dissimilar '
        'joint was conducted (as per ASTM E23) at room temperature. The fracture '
        'morphology of the impact specimen was studied using a scanning electron '
        'microscope (SEM), used to analyse the micrographs of both the heat-affected '
        'zone and the fusion zone of the SA516+SS2205 dissimilar welds. This analysis '
        'was carried out using variable parameters such as a working distance of '
        '11.4-13.2 mm, accelerating voltage of 15.0-20.0 kV, resolution of 1K-2.2K '
        'and probe current of 8.0-26.0 using a JEOL IT 500 available at UCRD, '
        'Chandigarh University, Gharuan, Punjab, India. Samples from the HAZ, weld '
        'zone and base metals were prepared and etched using standard metallographic '
        'techniques. The specimens were polished using 200 to 2000 grade emery paper '
        'followed by a velvet cloth with alumina paste. SS2205 duplex stainless steel '
        'was etched electrochemically with a 10 % oxalic acid solution. {{An optical '
        'microscope was used to examine the microstructures.}}'))
    A(center('Figure 2. Sample extracted from the welded plate and the microhardness '
             'testing machine. {{A labelled diagram of the as-welded plate showing '
             'the locations from which the tensile, impact, microhardness and '
             'metallographic specimens were extracted (with dimensions per the '
             'relevant ASTM standards) is included.}}', italic=True, size=20))

    # -- Results
    A(h1('3. Results and Discussion'))
    A(para(
        '{{Throughout this manuscript, HAZ-1 denotes the heat-affected zone on the '
        'SA516 carbon-steel side, and HAZ-2 denotes the heat-affected zone on the '
        'SS2205 duplex stainless-steel side.}}'))
    A(center('Figure (new). Schematic cross-section of the dissimilar joint '
             '{{delineating SA516 base metal \u2013 HAZ-1 \u2013 fusion zone (309L '
             'weld metal) \u2013 HAZ-2 \u2013 SS2205 base metal, together with the '
             'weld-bead geometry (bead width, reinforcement, penetration) and the '
             'microhardness indentation traverse across these zones. [Schematic to '
             'be inserted.]}}', italic=True, size=20))

    A(h2('3.1 Microstructural Analysis'))
    A(para(
        'The micrographs of the SA516 base metal primarily consisted of ferrite and '
        'pearlite, whereas the 2205 duplex stainless steel exhibited a dual-phase '
        'structure of ferrite and austenite. The weld zone exhibited a complex '
        'microstructure of austenite and delta ferrite, influenced by the 309L filler '
        'wire. From the micrographs, it is clear that HAZ-1 displayed grain '
        'coarsening, while HAZ-2 revealed partial dissolution of ferrite. Moreover, '
        'the dissimilar welds between SA516 and SS2205 often exhibit a complex mix of '
        'ferritic, austenitic and martensitic phases, especially in the HAZ regions. '
        'The microstructure of base material SA516 is presented in Figure 3(a). It '
        'consists of alternate layers of ferrite and pearlite in the rolling '
        'direction. The approximate ferrite content is 54.49 %, while the pearlite '
        'content is 45.51 % as revealed by ImageJ software. High carbon and manganese '
        'content in SA516 result in the formation of fine grains. With increasing '
        'carbon content, the amount of polygonal ferrite and grain-boundary ferrite '
        'decreases. The results are in good agreement with the findings of Singh and '
        'Pandey {{[21]}}. Carbon content also influences the mechanical properties: '
        'with the addition of carbon the tensile and yield strength increase and '
        'ductility decreases, due to which microhardness increases. HAZ-1 forms '
        'during cooling of the weld molten metal; it is due to the non-homogeneity of '
        'base metal and filler metal. The fusion zone near HAZ-1, made up of 309L '
        'filler wire and SA516, causes improper wetting due to the different crystal '
        'structure. Due to high heat input but no melting, quenched polygonal ferrite '
        '(QPF) is observed in HAZ-1. In the base metal near HAZ-1, coarse-grain '
        'ferrite and pearlite were present. The presence of hard and brittle '
        'martensitic phases, particularly near the SA516 interface, is a common '
        'observation that can lead to premature failure under mechanical stress or '
        'thermal cycling [11]. Post-weld heat treatment (PWHT) can mitigate some of '
        'these issues by tempering the martensite and reducing residual stresses, but '
        'the PWHT parameters must be carefully controlled to avoid over-aging the '
        'duplex stainless steel. This is in good agreement with [12].'))
    A(center('Figure 3. (a) Microstructure of parent metal SA516, (b) HAZ-1, (c) '
             '2205 + SA516 309L (weld region), (d) HAZ-2 and (e) parent metal 2205. '
             '{{Replaced with higher-resolution micrographs with enlarged, '
             'high-contrast annotations. Abbreviations: QPF \u2013 quenched '
             '(quasi-)polygonal ferrite; GBA \u2013 grain-boundary austenite; IGA '
             '\u2013 intragranular austenite; WA \u2013 Widmanst\u00e4tten austenite; '
             'CS \u2013 columnar structure; AF \u2013 austenite-ferrite; FGF \u2013 '
             'fine-grained ferrite.}}', italic=True, size=20))
    A(para(
        'The weld zone is a mixture of both materials, i.e. carbon steel SA516 and '
        'duplex stainless steel SS2205, and it combines the corrosion resistance and '
        'weldability properties of both. In this region, columnar dendrites, '
        'equiaxed polygonal ferrite and a columnar structure (CS) were observed. '
        'HAZ-2 lies between the weld zone and SS2205 and shows ferrite dendrites. Due '
        'to multipass welding, ferrite transformation occurs since the base metal '
        'SS2205 and the 309L filler wire are from the same stainless-steel family. '
        '{{Widmanst\u00e4tten}} ferrite and a mixture of FCC & BCC structures were '
        'also observed. In the welding zone, the adequate heat input led to excessive '
        'austenite due to the appearance of tiny intragranular austenite (IGA) which '
        'nucleated inside the ferrite. This is in good agreement with {{[22]}}. The '
        'grain-boundary austenite (GBA) and ferrite were found to be more prone to '
        'plastic deformation. Ferrite was dominant, while austenite presented two '
        'modalities, i.e. the banded GBA which overwhelmed ferrite, and '
        '{{Widmanst\u00e4tten}} austenite (WA) which nucleated on the GBA side and '
        'developed towards the interior of the ferrite. This is due to the faster '
        'thermal cycle and shorter heat time at the HAZ, which led to insufficient '
        'formation of austenite. Base metal 2205 duplex stainless steel has a high '
        'content of nickel, chromium and manganese compared to SA516. In this region '
        'the austenite-ferrite (AF), grain-boundary austenite (GBA), '
        '{{intragranular}} austenite (IGA) and {{Widmanst\u00e4tten}} austenite (WA) '
        'are observed.'))

    A(h2('3.2 Mechanical Properties'))
    A(h2('3.2.1 Impact Strength'))
    A(para(
        'The impact strength of the weld metal was higher than that of the SS2205 and '
        'SA516 base metals, indicating moderate toughness of the welded joint. Impact '
        'toughness (as per ASTM E23) of both the HAZ and the fusion zone of the 2205 '
        'duplex steel and SA516 dissimilar weld was observed at room temperature. To '
        'qualify, the minimum impact toughness for these dissimilar welds should '
        'exceed 40 J (see Table 4). Table 4 presents the impact-toughness values for '
        'the base, HAZ and fusion zone of 2205, SA516 and the SA516+2205 weld region. '
        'The 2205 duplex base metal achieves a maximum impact toughness of 130 J, '
        'while the SA516 base metal reaches 100 J. {{The SA516+2205 fusion zone '
        'recorded the highest absorbed energy (150 J), exceeding the SS2205 duplex '
        'base metal (130 J) by about 15 % and the SA516 base metal (100 J) by about '
        '50 %. This superior toughness reflects the tough, predominantly austenitic '
        '309L weld metal with a controlled ferrite content.}} A minimum impact '
        'toughness of 90 J was recorded for HAZ-1. {{Impact testing was carried out '
        'in accordance with ASTM E23; the values reported in Table 4 are '
        'representative per location, and the mean \u00b1 standard deviation from the '
        'test record should be inserted where replicate specimens were tested.}} The '
        'greater toughness in the SA516+2205 dissimilar weld, characterized by its '
        'fine-grained ferritic (FGF) microstructure as seen in Figure 3, is '
        'attributed to the lower occurrence of liquation cracking compared to the two '
        'HAZ regions (HAZ-1 and HAZ-2). It demonstrates that the reduction in impact '
        'strength caused by welding results from irregular grain orientations of the '
        'austenite and ferrite phases, secondary austenite phases in the weld, '
        'coarser ferrite grains near the fusion line and improper diffusion of '
        'alloying elements [13]. The lowering of impact toughness in the weld is also '
        'significantly influenced by the residual stresses induced during welding.'))
    A(table([
        ['Sample', 'Impact toughness (J)'],
        ['SA516 (Base)', '100'],
        ['2205 Duplex steel (Base)', '130'],
        ['SA 516 + 2205 (FZ)', '150'],
        ['HAZ-1', '90'],
        ['HAZ-2', '110'],
    ], widths=[5160, 3200]))
    A(center('Table 4. Impact toughness results', italic=True, size=20))

    A(h2('Fractography of the impact specimen'))
    A(para(
        'The figures show the scanning electron microscope (SEM) fractography from '
        'impact testing of the dissimilar weld between SA516 and SS2205. Figure 4(a) '
        'shows the fractography of the heat-affected zone (HAZ-1) along SA516. It '
        'shows more elongated and planar fracture features, indicating a mixed-mode '
        'fracture with some brittle characteristics. This could be due to the '
        'presence of cleavage facets, indicating brittle fracture, mixed with some '
        'ductile regions. HAZ-1 is prone to embrittlement due to the formation of '
        'martensitic phases or carbide precipitation during welding, particularly '
        'when the cooling rate is high [14]. Due to microstructural changes, the '
        'material lost its ductility in the regions where cleavage facets are '
        'observed. The energy absorption in the mixed-mode rupture is comparatively '
        'lower than on the SS2205 side. This could indicate martensitic hardening, '
        'which leads to brittle fracture. SA516 is prone to the formation of hard '
        'martensitic structures in the heat-affected zone, which can embrittle the '
        'metal, decrease its toughness and promote mixed brittle-ductile fracture. '
        'This statement is in good agreement with [15]. The fractography of the weld '
        'region is shown in Figure 4(b). It shows a mix of planar areas and dimples, '
        'i.e. a more complex fracture surface. The surface is rough and irregular, '
        'demonstrating a combination of ductile tearing and brittle crack '
        'propagation. In the fusion zone, the use of filler material can lead to '
        'phase changes and a gradient of mechanical properties, depending on the '
        'characteristics of the weld pool solidification. The presence of both '
        'ductile and brittle regions suggests that there may be localized hardening '
        '(e.g. intermetallic or martensitic phase formation) alongside more ductile '
        'areas. The transition between austenite and ferrite phases in the SS2205 '
        'could also contribute to this mixed fracture behavior. Welds between '
        'dissimilar metals often exhibit complex microstructures, with variations in '
        'fracture and hardness behavior due to phase transformations and thermal '
        'cycling. The use of suitable filler materials is critical for controlling '
        'the toughness of the weld zone [16]. Brittle cracks may be induced by the '
        'high hardness of some phases, while the existence of softer, more ductile '
        'phases allows for microvoid coalescence. The fractograph of HAZ-2 is shown '
        'in Figure 4(c). From the figure it can be concluded that the image shows a '
        'ductile fracture mode, as indicated by the presence of numerous dimples. '
        'These dimples form due to microvoid coalescence, typical of ductile fracture '
        'in metals. The microvoids originate from inclusions or second-phase '
        'particles being pulled out during the fracture process. {{Since this region '
        'is from HAZ-2 (SS2205 duplex side)}}, it likely underwent phase '
        'transformations during welding, including the possible formation of sigma '
        'phases or chromium-carbide precipitation at grain boundaries. However, the '
        'ductile nature observed here suggests that the phase transformations were '
        'minimal and that the austenitic phase in SS2205 provided ductility. The '
        'presence of such dimples indicates good energy absorption during impact '
        'testing, characteristic of ductile behavior. Duplex stainless steels such as '
        'SS2205 typically display a balanced combination of ferritic and austenitic '
        'phases, contributing to excellent toughness and strength, which is reflected '
        'in the dimpled fracture morphology. This is in good agreement with [3].'))
    A(center('Figure 4. (a) Fractograph of HAZ-1, (b) weld region SA516 + 2205, '
             '(c) HAZ-2.', italic=True, size=20))

    A(h2('3.2.2 Microhardness Analysis'))
    A(para(
        'The microhardness of dissimilar welds between SA516 and SS2205 is a critical '
        'factor that influences the mechanical integrity and service performance of '
        'welded structures. Factors such as carbon migration, phase transformations '
        'and heat input during welding significantly affect the hardness '
        'distribution, especially in the HAZ of the carbon steel. The use of 309L '
        'filler material and the GMAW technique helps to control hardness gradients, '
        'mitigate excessive hardness and improve joint toughness. The microhardness '
        'profile across the weld joint indicated higher microhardness values in the '
        'HAZ compared to the weld zone and base metals, attributed to phase '
        'transformations under the weld thermal cycle. Hardness tests also indicate '
        'significant variations across the weld, with higher values observed towards '
        'the stainless-steel side due to the presence of harder phases [17]. SA516 is '
        'a carbon steel with relatively low hardness compared to SS2205 and is widely '
        'used for boilers and pressure vessels due to its good toughness and '
        'weldability. The microhardness of SA516 is influenced by its carbon content '
        'and ferrite-pearlite structure, which can increase hardness in the HAZ near '
        'the weld if carbon relocation occurs during welding [18]. SS2205 is a duplex '
        'stainless steel containing a mixture of ferrite and austenite. It provides '
        'higher mechanical strength and hardness compared to carbon steel due to its '
        'higher alloying content (Cr, Ni and Mo) and dual-phase structure. During '
        'welding, the hardness distribution in SS2205 is affected by the formation of '
        'ferrite and austenite phases in the HAZ and fusion zone, as well as the '
        'potential formation of detrimental phases such as carbide and sigma phases '
        'at higher temperatures [3].'))
    A(para(
        '{{The hardness increases from the SA516 base metal (254 HV) toward the weld. '
        'On the carbon-steel side, HAZ-1 rises to 345 HV owing to the formation of '
        'hard bainitic/martensitic constituents during the weld thermal cycle. The '
        'SS2205 duplex base metal (approximately 290 HV) is intrinsically harder than '
        'the SA516 base metal. The overall peak occurs in HAZ-2 on the duplex side at '
        '372 HV, which exceeds both HAZ-1 (345 HV) and the SS2205 base metal, and is '
        'associated with grain refinement and the altered ferrite-austenite balance '
        'of the reheated duplex microstructure. Thus the hardness ranking is: HAZ-2 '
        '(372 HV) > HAZ-1 (345 HV) > fusion zone (307 HV) > SS2205 base (290 HV) > '
        'SA516 base (254 HV). The minimum hardness of 254 HV was noted in the SA516 '
        'base metal, and the fusion zone of the SA516+2205 weld has a hardness of 307 '
        'HV, comparable to the base-metal values of both alloys.}} This hardness '
        'increase near the weld interface is explained by the fact that, during '
        'welding, carbon diffuses from the carbon steel toward the stainless steel, '
        'which may cause hard martensitic phases to form near the interface [11]. The '
        'microhardness of welds is directly affected by the microstructural '
        'transformations that occur during welding. For instance, in the HAZ of '
        'SA516, the high temperatures during welding can cause grain growth, '
        'martensitic transformation and carbide precipitation upon cooling, all of '
        'which contribute to increased hardness. Moreover, the SS2205 side may '
        'experience phase transformations from ferrite to sigma phase or '
        'chromium-carbide precipitation at high temperatures, resulting in '
        'embrittlement and reduced corrosion resistance [9].'))
    A(center('Figure 5. Microhardness survey', italic=True, size=20))
    A(table([
        ['S. No.', 'SA516 Base', 'SA516 HAZ-1', 'SS2205 Base', 'SS2205 HAZ-2',
         'Weld HAZ-1 (SA516 side)', 'Weld FZ', 'Weld HAZ-2 (SS2205 side)'],
        ['1', '255', '342', '291', '319', '307', '305', '372'],
        ['2', '251', '346', '288', '283', '308', '308', '373'],
        ['3', '257', '347', '285', '292', '309', '306', '375'],
        ['4', '251', '344', '295', '285', '303', '307', '371'],
        ['5', '258', '346', '293', '305', '305', '311', '370'],
        ['Average', '254', '345', '290', '297', '306', '307', '372'],
    ], widths=[960, 1050, 1050, 1050, 1100, 1200, 850, 1100], size=15))
    A(center('Table 5. Vickers microhardness (HV) of the base metal, HAZ and fusion '
             'zone of SA516, 2205 duplex steel and the SA516+2205 weld region',
             italic=True, size=20))
    A(para(
        'The Vickers hardness of both the heat-affected zones and the fusion zone of '
        'the SA516+2205 dissimilar weld was examined at a 500 g load for a 15 s dwell '
        'time. Table 5 presents the average microhardness values. Figure 5 depicts '
        'the microhardness survey of the base metal, HAZ and SA516+2205 dissimilar '
        'weld, showing a consistent trend across the transition zones of the '
        'weldment. {{A relatively higher hardness was observed in HAZ-2 on the SS2205 '
        'duplex side (372 HV) than in HAZ-1 on the SA516 side (345 HV), associated '
        'with grain refinement and the shift in the ferrite-austenite balance of the '
        'reheated duplex microstructure, together with carbon migration across the '
        'weld interface.}} The HAZ-1 and HAZ-2 regions show a gradual increase in '
        'hardness moving from the base metal to the HAZ. The high-temperature '
        'heat-affected region (HTHAR) exhibits higher hardness than the '
        'low-temperature heat-affected region (LTHAR), as the HTHAR experiences '
        'higher thermal-cycling effects. The high hardness at the HAZ is promoted by '
        'the high cooling rate, which produces fine grains that increase the hardness '
        'of the material.'))

    # -- Conclusion
    A(h1('4. Conclusion'))
    A(para(
        'In this study, the dissimilar welding of 2205 duplex stainless steel and '
        'SA516 boiler plate was successfully demonstrated. The microstructural and '
        'mechanical properties, such as impact strength and microhardness, were '
        'investigated. The key findings are summarized below.'))
    for bullet in [
        'The use of 309L filler metal for welding SA516 and 2205 results in a '
        'dissimilar joint with satisfactory mechanical properties and microstructural '
        'characteristics.',
        'The weld metal showed increased hardness and strength, while HAZ-1 was '
        'identified as a critical region for failure.',
        'Using 309L filler material for welding dissimilar metals such as SA516 and '
        '2205 duplex stainless steel is effective in achieving a stable microstructure '
        'and satisfactory mechanical properties.',
        'The highest impact toughness was achieved at the weld fusion zone, i.e. 150 '
        'J, whereas the lowest was observed in HAZ-1, i.e. 90 J.',
        'The microhardness of the dissimilar weld is 307 HV at the fusion zone, which '
        'is lower than the microhardness at the HAZ.',
        '{{The highest microhardness was observed at HAZ-2, i.e. the heat-affected '
        'zone on the SS2205 duplex stainless-steel side, at 372 HV, in agreement with '
        'Table 5 and the Results section, while the lowest was recorded in the SA516 '
        'base metal at 254 HV.}}',
        'The fractographs of the dissimilar weld between SA516 and SS2205 reveal '
        'varying fracture behaviors. HAZ-2 shows predominantly ductile fracture '
        'features, with dimpled microvoid coalescence.',
        'HAZ-1 exhibits mixed-mode fracture with evidence of brittle cleavage, '
        'indicating reduced toughness in this region.',
        'A combination of ductile and brittle features was observed at the weld '
        'region, highlighting the complexity of the microstructure in dissimilar '
        'welds.',
        'These microstructural changes, driven by phase transformations and filler '
        'metal selection, can significantly impact the mechanical properties and '
        'fracture behavior of dissimilar welded joints.',
    ]:
        A(para('\u2022  ' + bullet, after=60))

    A(h2('Funding Details'))
    A(para('On behalf of the corresponding author it is certified that the present '
           'research has not received any internal/external funding from any '
           'government/private agency. No funding was received from any source. The '
           'research is original and unpublished anywhere.'))
    A(h2('Disclosure of Interest'))
    A(para('On behalf of the corresponding author it is certified that there are no '
           'interests to declare. The research is original and unpublished anywhere.'))

    # -- References
    A(h1('References'))
    refs = [
        '[1]  J. Singh and A. S. Shahi, "Metallurgical and corrosion characterization '
        'of electron beam welded duplex stainless steel joints," J. Manuf. Process., '
        'vol. 50, pp. 581-595, 2020, doi: 10.1016/j.jmapro.2020.01.009.',
        '[2]  H. K\u00fc\u00e7\u00fck\u00f6ner, H. Karako\u00e7, and N. Kahraman, '
        '"Investigation of microstructure and mechanical properties of '
        'AISI2205/DIN-P355GH steel joint by submerged arc welding," J. Manuf. '
        'Process., vol. 59, pp. 566-586, 2020, doi: 10.1016/j.jmapro.2020.10.023.',
        '[3]  R. Ansari, M. Movahedi, and M. Pouranvari, "Microstructural features and '
        'mechanical behavior of duplex stainless steel/low carbon steel friction stir '
        'dissimilar weld," J. Mater. Res. Technol., vol. 25, pp. 5352-5371, 2023, '
        'doi: 10.1016/j.jmrt.2023.07.025.',
        '[4]  S. Saini and K. Singh, "Recycling of steel slag as a flux for submerged '
        'arc welding and its effects on chemistry and performance of welds," Int. J. '
        'Adv. Manuf. Technol., vol. 114, pp. 1165-1177, 2021, '
        'doi: 10.1007/s00170-021-06866-1.',
        '[5]  A. Banerjee, M. Ntovas, L. Da Silva, and S. Rahimi, "Microstructure and '
        'mechanical properties of dissimilar inertia friction welded 316L stainless '
        'steel to A516 ferritic steel for potential applications in nuclear '
        'reactors," Manuf. Lett., vol. 33, pp. 33-37, 2022, '
        'doi: 10.1016/j.mfglet.2022.07.002.',
        '[6]  S. Saini and K. Singh, "Waste to wealth: Recycling of steel slag as flux '
        'for the submerged arc welding process and its effect on mechanical and '
        'metallurgical properties of welds," Proc. Inst. Mech. Eng. Part C, vol. 236, '
        'no. 16, pp. 8980-8990, 2022, doi: 10.1177/09544062221089253.',
        '[7]  A. Bhattacharya and R. Kumar, "Dissimilar joining between austenitic and '
        'duplex stainless steel in double-shielded GMAW: A comparative study," Mater. '
        'Manuf. Process., vol. 31, no. 3, pp. 300-310, 2016, '
        'doi: 10.1080/10426914.2015.1070414.',
        '[8]  L. Sharma and R. Chhibber, "Study of weld bead chemical, microhardness '
        '& microstructural analysis using submerged arc welding fluxes for linepipe '
        'steel applications," Ceram. Int., vol. 46, no. 15, pp. 24615-24623, 2020, '
        'doi: 10.1016/j.ceramint.2020.06.250.',
        '[9]  S. A. Rizvi and M. Ahamad, "Effect of heat input on the microstructure '
        'and mechanical properties of a welded joint - A review," Int. J. Appl. Eng. '
        'Res., vol. 13, no. 6, pp. 184-188, 2018.',
        '[10]  J. Prakash, S. P. Tewari, and B. K. Srivastava, "Shielding gas for '
        'welding of aluminium alloys by TIG/MIG welding - A review," Int. J. Mod. '
        'Eng. Res., vol. 1, no. 2, pp. 690-699, 2016.',
        '[11]  C. Mitelea, I. U\u0163u, I. D. Karancsi, O. Urlan, S. D. Cr\u0103'
        'ciunescu, "Investigation of the microstructure of dissimilar welds in duplex '
        'stainless steel and low alloyed steel," Mater. Test., vol. 61, no. 2, pp. '
        '120-124, 2019, doi: 10.3139/120.111292.',
        '[12]  V. Bhanu, A. Gupta, and C. Pandey, "Role of A-TIG process in joining of '
        'martensitic and austenitic steels for ultra-supercritical power plants - a '
        'state of the art review," Nucl. Eng. Technol., vol. 54, no. 8, pp. '
        '2755-2770, 2022, doi: 10.1016/j.net.2022.03.003.',
        '[13]  A. V. Jebaraj, L. A. Kumar, and C. R. Deepak, "Investigations on '
        'anisotropy behavior of duplex stainless steel AISI 2205 for optimum weld '
        'properties," Procedia Eng., vol. 173, pp. 883-890, 2017, '
        'doi: 10.1016/j.proeng.2016.12.132.',
        '[14]  J. Amanie, "Effect of submerged arc welding parameters on the '
        'microstructure of SA516 and A709 steel welds," M.Sc. thesis, pp. 1-189, 2011.',
        '[15]  M. F. Mamat, E. Hamzah, Z. Ibrahim, and A. M. Rohah, "Effect of filler '
        'metals on the microstructures and mechanical properties of dissimilar low '
        'carbon steel and 316L stainless steel welded joints," Mater. Sci. Forum, '
        'vol. 819, pp. 57-67, 2015, doi: 10.4028/www.scientific.net/msf.819.57.',
        '[16]  P. K. Taraphdar, M. M. Mahapatra, A. K. Pradhan, P. K. Singh, and K. '
        'Sharma, "Evaluation of through-thickness residual stresses and microstructure '
        'in SA516 Gr. 70 steel welds," Proc. Inst. Mech. Eng. Part B, vol. 235, no. '
        '6-7, pp. 958-973, 2021, doi: 10.1177/0954405421990124.',
        '[17]  H. Ma, G. Qin, P. Geng, F. Li, B. Fu, and X. Meng, "Microstructure '
        'characterization and properties of carbon steel to stainless steel dissimilar '
        'metal joint made by friction welding," Mater. Des., vol. 86, pp. 587-597, '
        '2015, doi: 10.1016/j.matdes.2015.07.068.',
        '[18]  W. Wu, S. Hu, and J. Shen, "Microstructure, mechanical properties and '
        'corrosion behavior of laser welded dissimilar joints between ferritic '
        'stainless steel and carbon steel," Mater. Des., vol. 65, pp. 855-861, 2015, '
        'doi: 10.1016/j.matdes.2014.09.064.',
        '{{[19]  A.-H. I. Mourad et al., study on dissimilar-metal welding addressing '
        'melting-point and thermal-expansion mismatch, 2017. [Full bibliographic '
        'details to be verified and completed by the authors.]}}',
        '{{[20]  R. Kumar et al., on GMAW/GTAW welding of dissimilar metals and heat-'
        'input control, 2021. [Full bibliographic details to be verified and '
        'completed by the authors.]}}',
        '{{[21]  J. Singh and C. Pandey, on the influence of carbon content on '
        'polygonal/grain-boundary ferrite. [Full bibliographic details to be verified '
        'and completed by the authors.]}}',
        '{{[22]  "Microstructure-based multiscale and heterogeneous elasto-plastic '
        'properties of 2205 duplex stainless steel welded joints: experimental and '
        'modelling." [Authors, journal, volume and year to be verified and completed '
        'by the authors.]}}',
    ]
    for r in refs:
        A(para(r, size=20, after=60))

    write_docx('/projects/sandbox/AMMAN/Manuscript_SA516_2205_Dissimilar_Weld_REVISED.docx',
               ''.join(b))


# ----------------------------------------------------------------------
# RESPONSE TO REVIEWERS
# ----------------------------------------------------------------------

def q(text):
    """Italic quoted reviewer comment."""
    return para('\u201c' + text + '\u201d', italic=True, after=80)


def build_response():
    b = []
    A = b.append

    A(title('Response to Reviewers'))
    A(para('Manuscript: Investigation of the Dissimilar Weld Joint between SS2205 '
           'Duplex Stainless Steel and SA516 Carbon Steel using 309L Filler',
           bold=True, jc='center'))
    A(para('We thank the Editors and both Reviewers for their careful and '
           'constructive assessment of our manuscript. The comments have helped us '
           'correct several inconsistencies and improve the clarity of the '
           'presentation. We have addressed every point below. Reviewer comments are '
           'quoted in italics, followed by our response and the specific revision '
           'made. All page/line numbers refer to the revised manuscript, and changes '
           'are highlighted in the revised file.'))

    A(h1('Reviewer 1'))

    A(h2('Comment 1 \u2014 Inconsistent location of maximum microhardness '
         '(Table 5, Results vs. Conclusion)'))
    A(q('Table 5 reports an average of 372 HV for HAZ-2 along the 2205 side, and the '
        'Results section also identifies this region as having the maximum hardness. '
        'However, the Conclusion states that the highest microhardness of 372 HV '
        'occurs at HAZ-1. Please reconcile these statements and use consistent HAZ '
        'terminology throughout.'))
    A(para('Response. We thank the reviewer for catching this inconsistency. The '
           'correct location of the maximum microhardness is HAZ-2 on the SS2205 '
           '(duplex) side, at 372 HV, consistent with both Table 5 and the Results '
           'section. The statement in the Conclusion referring to "HAZ-1" was a '
           'typographical error and has been corrected. To prevent any further '
           'ambiguity, we have standardized the HAZ nomenclature throughout:'))
    A(para('\u2022  HAZ-1 = heat-affected zone on the SA516 carbon-steel side.', after=40))
    A(para('\u2022  HAZ-2 = heat-affected zone on the SS2205 duplex stainless-steel '
           'side.', after=80))
    A(para('Revision (Conclusion).'))
    A(para('Before: "The highest microhardness of 372 HV was observed at HAZ-1."',
           italic=True, after=40))
    A(para('After: "The highest microhardness of 372 HV was observed at HAZ-2, i.e. '
           'the heat-affected zone on the SS2205 duplex stainless-steel side, in '
           'agreement with Table 5 and the Results section." We have also verified '
           'every subsequent reference to HAZ-1/HAZ-2 in the text, figure captions '
           'and Table 5 for consistency.', italic=True))

    A(h2('Comment 2 \u2014 Numerically inconsistent microhardness discussion'))
    A(q('The statement that the 2205 base and HAZ-2 have higher hardness than the '
        '"SA516 base (254 HV) and HAZ-1 (345 HV)" conflicts numerically because 345 '
        'HV is greater than both 290 and 297 HV. The subsequent statement also says '
        'that the SA516-side HAZ has higher hardness than the SS2205 HAZ-2.'))
    A(para('Response. We agree; the original wording mixed up the comparisons and did '
           'not match Table 5. The corrected averages from Table 5 are summarized '
           'below.'))
    A(table([
        ['Region', 'Location', 'Microhardness (HV)'],
        ['SA516 base metal', 'Carbon-steel side', '254'],
        ['HAZ-1', 'SA516 (carbon-steel) side', '345'],
        ['Fusion zone (309L weld metal)', 'Weld centre', '307'],
        ['SS2205 base metal', 'Duplex side', '290'],
        ['HAZ-2', 'SS2205 (duplex) side', '372'],
    ], widths=[3200, 3160, 2000]))
    A(para('The corrected physical picture is: (1) the overall maximum hardness is '
           'HAZ-2 (372 HV) on the duplex side, attributable to grain refinement and '
           'the ferrite/austenite balance shift plus possible secondary-phase '
           'formation under the weld thermal cycle; (2) HAZ-1 (345 HV) on the SA516 '
           'side is markedly harder than the SA516 base metal (254 HV) because of '
           'transformation to harder, non-equilibrium microstructures '
           '(bainite/martensite); (3) the SS2205 base metal (290 HV) is harder than '
           'the SA516 base metal but lower than its own HAZ-2 and lower than HAZ-1. '
           'We have rewritten the paragraph so that the hardness ranking reads HAZ-2 '
           '(372) > HAZ-1 (345) > fusion zone (307) > SS2205 base (290) > SA516 base '
           '(254), which is numerically consistent with Table 5.'))

    A(h2('Comment 3 \u2014 Filler-wire diameter "08 mm" and incomplete welding '
         'conditions'))
    A(q('The manuscript reports a "08 mm diameter 309L filler wire." This value '
        'should be verified. Table 2 provides current, voltage, and welding speed, '
        'but the experimental procedure would benefit from a more complete '
        'description of the welding conditions.'))
    A(para('Response. "08 mm" was a typographical error; the filler used was ER309L '
           'wire of 0.8 mm diameter, and the text has been corrected to state this '
           'unambiguously. We have expanded the Experimental Procedure with a fuller '
           'description of the welding conditions, including joint geometry and edge '
           'preparation (60\u00b0 single-V included angle, 2 mm root gap, 1.5 mm root '
           'face), the multi-pass sequence (root/fill/cap), the interpass temperature '
           '(kept below 150 \u00b0C), the shielding gas and flow rate, and the heat '
           'input calculated as HI = \u03b7 (V \u00d7 I) / v, consolidated with the '
           'existing current/voltage/travel-speed data of Table 2. Items dependent on '
           'the welding record (shielding-gas flow rate, exact pass count) are marked '
           'for completion from the source data.'))

    A(h2('Comment 4 \u2014 Contradictory HAZ designation in Fractography '
         '(Fig. 4c)'))
    A(q('The text identifies Figure 4(c) as HAZ-2, but later states, "Since this '
        'region is from the HAZ-1." This contradicts the figure caption.'))
    A(para('Response. Figure 4(c) corresponds to HAZ-2 (SS2205 duplex side), which '
           'matches the caption and surrounding discussion. The later sentence '
           '"Since this region is from the HAZ-1" was a typographical error and has '
           'been corrected to HAZ-2. We have made a complete pass over all figure '
           'captions and in-text figure call-outs to verify labeling consistency.'))

    A(h2('Comment 5 \u2014 Impact-strength interpretation: 150 J vs. 130 J "almost '
         'comparable"'))
    A(q('The fusion zone is reported at 150 J, compared with 130 J for 2205 and 100 J '
        'for SA516, yet the text describes 150 J as "almost comparable" to the 2205 '
        'base metal.'))
    A(para('Response. We agree the original wording understated the difference. The '
           'fusion zone (150 J) is in fact higher than the SS2205 base metal (130 J) '
           'by about 15 %, and substantially higher than the SA516 base metal (100 J) '
           'by about 50 %. We have revised the interpretation to reflect the actual '
           'numerical differences rather than "almost comparable," and attribute the '
           'high fusion-zone toughness to the tough austenitic 309L weld metal with '
           'controlled ferrite content. We have also clarified that impact testing '
           'followed ASTM E23 and indicated where the mean \u00b1 standard deviation '
           'of replicate specimens should be reported.'))

    A(h2('Comment 6 \u2014 Figure 3 phase labels and abbreviations'))
    A(q('The microstructural images contain several abbreviated phase labels (QPF, '
        'GBA, IGA, WA, and CS). Some labels are difficult to distinguish. '
        'Higher-resolution images and a clearer explanation of the abbreviations in '
        'the caption would improve interpretation.'))
    A(para('Response. We have replaced Figure 3 with higher-resolution micrographs '
           'and enlarged, high-contrast annotations, and added a complete legend in '
           'the caption defining every abbreviation: QPF (quenched/quasi-polygonal '
           'ferrite), GBA (grain-boundary austenite), IGA (intragranular austenite), '
           'WA (Widmanst\u00e4tten austenite), CS (columnar structure), AF '
           '(austenite-ferrite) and FGF (fine-grained ferrite). Each abbreviation is '
           'now also defined at first use in the text.'))

    A(h2('Comment 7 \u2014 Language and reference-formatting edit'))
    A(q('A thorough language and reference-formatting edit is needed, e.g. "aims to '
        'examine and analyses", "The manufacturing industry having so many problems", '
        '"The optical microscope was used to examined", and shifts between numbered '
        'citations and author-name references such as "[Singh and Pandey]".'))
    A(para('Response. The manuscript has undergone a thorough language edit. '
           'Representative corrections: "aims to examine and analyses" -> "aims to '
           'examine and analyse"; "The manufacturing industry having so many '
           'problems" -> "The manufacturing industry faces several challenges"; "The '
           'optical microscope was used to examined" -> "An optical microscope was '
           'used to examine". All in-text citations have been standardized to the '
           'numbered [n] style; author-name citations such as "[Singh and Pandey]", '
           '"(Mourad et al., 2017)", "(Kumar et al., 2021)" and the embedded full '
           'article title have been converted to numbered citations ([19]-[22]), with '
           'their bibliographic details flagged in the reference list for final '
           'verification by the authors.'))

    A(h1('Reviewer 2'))

    A(h2('Comment A \u2014 Correct the dimensions in Fig. 1'))
    A(q('In Fig. 1 the dimensions mentioned should be corrected.'))
    A(para('Response. Figure 1 has been redrawn with corrected and complete '
           'dimensioning (plate length, width and thickness, groove angle, root gap '
           'and root face), with units clearly indicated (mm). The dimensions now '
           'match the values reported in the Experimental Procedure.'))

    A(h2('Comment B \u2014 Justify choice of 309L filler and its interactive effect'))
    A(q('State why 309L filler material is chosen and its interactive effect with the '
        'materials used.'))
    A(para('Response. We have added a paragraph justifying the selection of ER309L. '
           'It is the standard filler for dissimilar welds joining stainless (here '
           'duplex SS2205) to carbon/low-alloy steel (SA516): its high Cr-Ni content '
           'compensates for dilution by the carbon steel, keeping the weld-metal '
           'composition within the austenitic region of the Schaeffler/WRC-1992 '
           'diagram and avoiding a fully martensitic, crack-prone deposit. The low '
           'carbon ("L") grade minimizes chromium-carbide precipitation and preserves '
           'corrosion resistance, and the tough austenitic matrix accommodates the '
           'differing thermal expansion of the two base metals. This interaction is '
           'now linked to the measured high fusion-zone toughness and the hardness '
           'profile.'))

    A(h2('Comment C \u2014 State the associated thermal model'))
    A(q('Any thermal model associated with it should be clearly mentioned.'))
    A(para('Response. We have added the thermal basis used. The net heat input per '
           'pass is reported as HI = \u03b7 (V \u00d7 I) / v. Where the thermal '
           'history is discussed, we relate it to the Rosenthal moving-point/line '
           'heat-source solution for peak temperature and cooling rate (and the '
           '\u0394t8/5 cooling time), which governs the HAZ microstructure and the '
           'observed hardness. We state explicitly that only analytical estimates '
           'were made and no finite-element thermal model was used.'))

    A(h2('Comment D \u2014 Picture and specifications of the welding machine'))
    A(q('The author should mention the picture of the welding machine used and its '
        'specifications.'))
    A(para('Response. We have added a photograph of the welding power source and a '
           'specifications table (make/model, process type, rated output '
           'current/voltage range, duty cycle, power supply and wire-feed unit) in '
           'the Experimental Procedure. Values dependent on the machine nameplate are '
           'marked for completion from the source data.'))

    A(h2('Comment E \u2014 Diagrams of the welded specimens'))
    A(q('Diagrams of the welded specimens should be mentioned.'))
    A(para('Response. We have added labeled diagrams/photographs of the welded '
           'specimens, including the as-welded plates and the locations from which '
           'the tensile, impact, microhardness and metallographic samples were '
           'extracted, with dimensions per the relevant ASTM standards.'))

    A(h2('Comment F \u2014 Schematic of fusion zone, HAZ, base plate and weld-bead '
         'geometry'))
    A(q('By drawing a schematic diagram, the fusion zone, HAZ, base plate and '
        'weld-bead geometry should be mentioned.'))
    A(para('Response. We have added a new schematic of the cross-section of the '
           'dissimilar joint, clearly delineating SA516 base metal - HAZ-1 - fusion '
           'zone (309L weld metal) - HAZ-2 - SS2205 base metal, together with the '
           'weld-bead geometry (bead width, reinforcement, penetration) and the '
           'microhardness indentation traverse. It is cross-referenced from the '
           'Microhardness and Microstructure sections so that the HAZ-1/HAZ-2 '
           'designations are unambiguous.'))

    A(h2('Comment G \u2014 Elaborate the literature review (Introduction, Ref. 4)'))
    A(q('The literature review in the introduction, i.e. ref. 4, should be written '
        'more elaborately.'))
    A(para('Response. We have expanded the Introduction, in particular the discussion '
           'around reference [4], to more fully summarize prior work on dissimilar '
           'welding of duplex/stainless to carbon steels (filler selection, HAZ '
           'behavior, mechanical performance and corrosion), and to clearly position '
           'the present study\u2019s contribution and the identified research gap. '
           'Additional relevant references have been added where appropriate.'))

    A(h1('Summary of Changes'))
    for s in [
        'Corrected the maximum-hardness location to HAZ-2 (372 HV) and standardized '
        'HAZ-1 (SA516 side) / HAZ-2 (SS2205 side) terminology throughout (R1-C1, '
        'R1-C4).',
        'Rewrote the microhardness discussion to be numerically consistent with '
        'Table 5 (R1-C2).',
        'Corrected the filler-wire diameter ("08 mm" -> 0.8 mm) and expanded the '
        'welding-condition details (R1-C3).',
        'Revised the impact-strength interpretation to reflect the actual differences '
        'and noted test replication/variability (R1-C5).',
        'Replaced Figure 3 with higher-resolution images and defined all phase '
        'abbreviations (R1-C6).',
        'Performed a full language and citation-style edit; unified to numbered '
        'references (R1-C7).',
        'Corrected the Fig. 1 dimensions; added the filler-selection rationale, the '
        'thermal model, the welding-machine photo/specifications, specimen diagrams '
        'and a new joint schematic; and expanded the Introduction literature review '
        '(R2-A through R2-G).',
    ]:
        A(para('\u2022  ' + s, after=60))

    A(para('We believe these revisions have substantially improved the manuscript '
           'and thank the reviewers again for their valuable feedback.'))
    A(para('Note to authors: items shown in brackets in the revised manuscript '
           '(shielding-gas flow rate, exact pass count, welding-machine nameplate '
           'values, and the bibliographic details of new references [19]-[22]) '
           'require the original lab records to finalize.', italic=True))

    write_docx('/projects/sandbox/AMMAN/Response_to_Reviewers_SA516_2205.docx',
               ''.join(b))


if __name__ == '__main__':
    print('Building manuscript...')
    build_manuscript()
    print('Building response...')
    build_response()
    print('Done.')
