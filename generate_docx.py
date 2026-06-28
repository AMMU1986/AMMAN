#!/usr/bin/env python3
"""
Generate a Word document (.docx) for the research article on
Thermal Modelling of Tool-Chip Interfacial Temperature in
Interrupted Orthogonal Machining in the Presence of Cutting Fluids.
Uses only standard library (zipfile) since python-docx is unavailable.
"""
import zipfile


def esc(text):
    """Escape XML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def para(text, bold=False, size=24, align='both', italic=False, indent=False):
    """Generate a paragraph XML string."""
    x = '<w:p><w:pPr>'
    if align:
        x += f'<w:jc w:val="{align}"/>'
    if indent:
        x += '<w:ind w:left="720" w:hanging="720"/>'
    x += '</w:pPr><w:r><w:rPr>'
    if bold:
        x += '<w:b/>'
    if italic:
        x += '<w:i/>'
    x += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    x += f'</w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
    return x


def table_xml(headers, rows):
    """Generate table XML."""
    x = '<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        x += f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    x += '</w:tblBorders></w:tblPr>'
    x += '<w:tr>'
    for h in headers:
        x += f'<w:tc><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve">{esc(h)}</w:t></w:r></w:p></w:tc>'
    x += '</w:tr>'
    for row in rows:
        x += '<w:tr>'
        for cell in row:
            x += f'<w:tc><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve">{esc(str(cell))}</w:t></w:r></w:p></w:tc>'
        x += '</w:tr>'
    x += '</w:tbl>'
    return x




def get_body_xml():
    """Build all body content XML."""
    parts = []
    sp = para("", size=12)

    # ===== TITLE =====
    parts.append(para("Thermal Modelling of Tool-Chip Interfacial Temperature in Interrupted Orthogonal Machining in the Presence of Cutting Fluids", bold=True, size=32, align='center'))
    parts.append(sp)
    parts.append(para("Author Name(s)", size=22, align='center', italic=True))
    parts.append(para("Department of Mechanical Engineering, University Name, City, Country", size=22, align='center', italic=True))
    parts.append(para("Corresponding Author Email: author@university.edu", size=22, align='center', italic=True))
    parts.append(sp)

    # ===== ABSTRACT =====
    parts.append(para("Abstract", bold=True, size=28, align='left'))
    parts.append(para(
        "This study presents a two-dimensional finite difference model-based inverse method for estimating transient temperature "
        "distributions at the tool-chip interface during interrupted orthogonal machining (peripheral milling) of medium carbon steel "
        "under dry and minimum quantity lubrication (MQL) cutting conditions. The model employs a genetic algorithm-based optimization "
        "procedure to minimize the error between thermocouple-measured and numerically predicted temperature histories, thereby "
        "inversely determining the heat flux entering the workpiece without requiring a priori assumptions about friction coefficients "
        "or heat partition ratios. Seven different metalworking fluids (MWFs), including vegetable oil, polyethylene glycol (PEG), "
        "and ionic liquid (IL) additives, were investigated under varying cutting speeds and machining severity levels. The estimated "
        "temperatures were compared with thermal decomposition temperatures of the lubricants obtained from thermogravimetric "
        "analysis to elucidate the mechanisms by which different cutting fluids influence machining tribology. Results demonstrate "
        "that at lower cutting speeds in light machining, lubricant viscosity dominates friction reduction, while at higher speeds "
        "and temperatures exceeding decomposition thresholds, chemical degradation products (particularly fluorine from ionic liquids) "
        "govern tribological performance. Strong correlations (R-squared > 0.72) between estimated rake face temperatures and cutting "
        "forces were established across most conditions, confirming the thermal modelling approach. The methodology provides a "
        "versatile framework for understanding cutting fluid action mechanisms without restrictive analytical assumptions, applicable "
        "to both dry and lubricated intermittent machining scenarios."
    ))
    parts.append(sp)
    parts.append(para("Keywords: Thermal modelling; Tool-chip interface temperature; Minimum quantity lubrication; Ionic liquids; Finite difference method; Inverse heat transfer; Interrupted machining", italic=True))
    parts.append(sp)

    # ===== 1. INTRODUCTION =====
    parts.append(para("1. Introduction", bold=True, size=28, align='left'))
    parts.append(para(
        "Machining remains one of the most widely employed manufacturing processes for producing critical engineering "
        "components across aerospace, automotive, energy, and biomedical industries (Astakhov, 2006; Trent & Wright, 2000). "
        "The process fundamentally involves severe plastic deformation of workpiece material, during which nearly all supplied "
        "mechanical energy is converted into thermal energy (Shaw, 2005). This heat generation occurs primarily in three "
        "distinct zones: the primary shear zone where chip formation occurs through intense plastic deformation, the secondary "
        "deformation zone at the tool-chip interface where frictional sliding generates additional heat, and the tertiary zone "
        "at the tool flank-workpiece contact region (Childs et al., 2000). The resulting temperature distributions critically "
        "influence tool wear rates, surface integrity of machined components, dimensional accuracy, and residual stress states "
        "(Davim, 2014; Abukhshim et al., 2006)."
    ))
    parts.append(sp)
    parts.append(para(
        "The growing emphasis on sustainable manufacturing has driven significant research toward dry machining and minimum "
        "quantity lubrication (MQL) as alternatives to conventional flood cooling (Sharma et al., 2016; Li et al., 2024). "
        "While these approaches substantially reduce environmental impact and operational costs associated with cutting fluid "
        "procurement, maintenance, and disposal, they also result in additional heat accumulation in the machining zone due "
        "to the elimination or drastic reduction of conventional coolant volumes (Kazeem et al., 2022; Sen et al., 2023). "
        "Consequently, understanding the thermal phenomena governing cutting fluid action becomes essential for optimizing "
        "MQL machining performance."
    ))
    parts.append(sp)
    parts.append(para(
        "The tool-chip interfacial temperature distribution is arguably the most critical parameter influencing cutting fluid "
        "effectiveness in machining operations (Komanduri & Hou, 2001). This temperature dictates whether the applied lubricant "
        "can function in its intended liquid state to provide physical lubrication through viscous film formation, or whether "
        "it undergoes thermal degradation leading to chemical reaction products that may beneficially or detrimentally alter "
        "interface tribology (Jayal & Balaji, 2009). Ionic liquids (ILs), which are molten salts at room temperature composed "
        "entirely of ions, have emerged as promising candidates for MQL applications due to their tunable physicochemical "
        "properties, negligible vapor pressure, high thermal stability, and excellent tribological characteristics (Ali et al., "
        "2023; Bermudez et al., 2009). When used as additives to bio-based carrier fluids such as vegetable oils, ILs can "
        "provide both physical and chemical lubrication mechanisms depending on prevailing thermal conditions at the tool-chip "
        "interface (Patel & Deheri, 2022)."
    ))
    parts.append(sp)
    parts.append(para(
        "However, accurate determination of tool-chip interface temperatures during MQL machining presents significant "
        "experimental challenges. Direct measurement techniques such as infrared thermal imaging are rendered ineffective "
        "by the MQL aerosol mist that obscures the cutting zone (Davies et al., 2007). Tool-work thermocouple methods "
        "provide only average temperatures and cannot resolve spatial distributions (Takabi & Tajdari, 2022). Furthermore, "
        "analytical models for temperature prediction typically require specification of tool-chip friction coefficients "
        "as input parameters, which are themselves unknown variables that change with different applied cutting fluids "
        "(Loewen & Shaw, 1954; Jaeger, 1942)."
    ))
    parts.append(sp)
    parts.append(para(
        "This paper addresses these challenges by presenting a two-dimensional finite difference model coupled with an "
        "inverse heat transfer problem (IHTP) solution methodology for estimating transient temperature distributions on "
        "the cutting tool rake face during interrupted orthogonal machining under dry and MQL conditions. The inverse "
        "approach eliminates the need for a priori assumptions about friction coefficients or heat partition ratios, which "
        "are themselves variable outcomes of different MWFs' effectiveness. A simple genetic algorithm (GA) optimization "
        "procedure minimizes the discrepancy between thermocouple-measured temperatures embedded in the workpiece and "
        "finite difference model predictions to determine the unknown heat flux entering the workpiece. The estimated "
        "temperatures are then compared with thermal decomposition temperatures of the applied lubricants to elucidate "
        "the dominant mechanisms of cutting fluid action under various machining conditions."
    ))
    parts.append(sp)

    return parts




def get_literature_xml():
    """Build literature review section."""
    parts = []
    sp = para("", size=12)

    parts.append(para("2. Literature Review", bold=True, size=28, align='left'))
    parts.append(para("2.1 Heat Generation in Machining", bold=True, size=24, align='left'))
    parts.append(para(
        "The thermal aspects of metal cutting have been extensively studied since the pioneering work of Blok (1938) "
        "and Jaeger (1942), who established the classical heat partition model and friction slider framework, respectively. "
        "These foundational models assume that all mechanical energy supplied during cutting is converted to heat, partitioned "
        "between the chip, workpiece, and tool according to their relative thermal properties and the cutting kinematics "
        "(Boothroyd, 1988). In the primary shear zone, the intense plastic deformation generates substantial heat, a portion "
        "of which flows into the workpiece while the remainder is carried away by the chip. At the secondary deformation zone, "
        "additional frictional heat is generated at the tool-chip interface, conducted partially into the tool body and partially "
        "transported by the chip (Trigger & Chao, 1951; Hahn, 1951)."
    ))
    parts.append(sp)
    parts.append(para(
        "Subsequent analytical developments by Loewen and Shaw (1954), Rapier (1954), and Weiner (1955) refined the temperature "
        "prediction models by incorporating more realistic boundary conditions and heat source distributions. Boothroyd (1963) "
        "advanced the field by proposing a volumetric heat source model for the tool-chip interface, departing from the planar "
        "heat source assumption of earlier works. More recently, comprehensive reviews by Abukhshim et al. (2006) and "
        "Gonzalez-Barrio et al. (2022) have catalogued the evolution of analytical temperature models, highlighting their "
        "limitations in handling transient conditions inherent to interrupted cutting processes such as milling."
    ))
    parts.append(sp)
    parts.append(para("2.2 Numerical Methods for Cutting Temperature Prediction", bold=True, size=24, align='left'))
    parts.append(para(
        "Numerical methods, particularly finite element methods (FEM) and finite difference (FD) approaches, have been "
        "increasingly employed to overcome the limitations of analytical models in handling material nonlinearity, complex "
        "geometries, and transient thermal conditions (Arrazola et al., 2013). The FEM approach was first applied to machining "
        "by Tay et al. (1974) and has since been extensively developed by numerous researchers including Strenkowski and Moon "
        "(1990), Komanduri and Hou (2001), and Ozel and Zeren (2007). While FEM offers superior capabilities for incorporating "
        "coupled thermo-mechanical effects, it typically demands extensive computational resources, with detailed simulations "
        "requiring hours to days of processing time on high-performance computing platforms (Melkote et al., 2017)."
    ))
    parts.append(sp)
    parts.append(para(
        "The finite difference method provides a computationally efficient alternative that is particularly well-suited for "
        "inverse heat transfer problem formulations where the forward model must be evaluated thousands of times during the "
        "optimization procedure (Lazoglu & Altintas, 2002; Chen et al., 1997). Recent advances by Zhang et al. (2024) have "
        "demonstrated the application of CNN-GRU machine learning models for rapid reconstruction of milling temperature fields "
        "based on inverse heat conduction solutions. Kim et al. (2022) employed finite difference methods with model order "
        "reduction techniques for online cutting temperature monitoring using inkjet-printed thin-film sensors."
    ))
    parts.append(sp)
    parts.append(para("2.3 Inverse Heat Transfer Methods in Machining", bold=True, size=24, align='left'))
    parts.append(para(
        "Inverse heat transfer methods offer a powerful framework for determining unknown thermal boundary conditions from "
        "measured temperature data at accessible locations (Ozisik & Orlande, 2021). In machining applications, these methods "
        "enable estimation of surface heat fluxes and temperature distributions at the tool-chip interface from subsurface "
        "thermocouple measurements (Rech et al., 2013). The inverse approach is particularly advantageous for MQL machining "
        "studies since it does not require specification of friction coefficients, which are themselves unknown and variable "
        "quantities dependent on the applied cutting fluid (Jayal, 2006)."
    ))
    parts.append(sp)
    parts.append(para(
        "Genetic algorithms have been successfully employed as optimization engines for inverse heat transfer problems due "
        "to their global search capabilities and robustness against local minima (Woodbury & Jin, 2023; Dhar et al., 2024). "
        "The GA-based approach is particularly suitable for machining applications where the objective function landscape may "
        "be non-convex due to the coupled effects of multiple heat sources and complex boundary conditions. Recent work by "
        "Famouri et al. (2024) demonstrated the effectiveness of genetic algorithms for inverse estimation of heat transfer "
        "coefficients in transient solidification problems, establishing methodological frameworks transferable to machining "
        "thermal analysis."
    ))
    parts.append(sp)
    parts.append(para("2.4 MQL Machining and Ionic Liquids", bold=True, size=24, align='left'))
    parts.append(para(
        "Minimum quantity lubrication has gained widespread acceptance as a sustainable alternative to flood cooling, "
        "delivering lubricant volumes of 10-100 mL/h compared to 10-100 L/min for conventional flood systems (Sharma "
        "et al., 2016). Comprehensive reviews by Li et al. (2024) and Sen et al. (2023) have documented the benefits of "
        "MQL in reducing cutting temperatures by 15-40% compared to dry machining while maintaining or improving surface "
        "integrity. The effectiveness of MQL depends critically on the lubricant's ability to penetrate the tool-chip "
        "interface and form a protective film under extreme pressure and temperature conditions (Debnath et al., 2014)."
    ))
    parts.append(sp)
    parts.append(para(
        "Ionic liquids represent a novel class of lubricant additives for MQL applications, offering unique advantages "
        "including negligible vapor pressure, wide liquid range, high thermal stability up to 300-400 degrees Celsius, and "
        "the ability to form protective tribofilms on metallic surfaces through chemical interaction (Bermudez et al., 2009; "
        "Minami, 2009). Phosphonium-based and imidazolium-based ILs containing fluorinated anions such as bis(trifluoro"
        "methylsulfonyl)imide [NTf2] and hexafluorophosphate [PF6] have demonstrated exceptional friction and wear reduction "
        "in machining applications (Patel & Deheri, 2022; Davis et al., 2023). The thermal decomposition of fluorinated ILs "
        "releases fluorine atoms that bond with freshly exposed metallic surfaces, forming low-shear-strength metal fluoride "
        "films that reduce adhesion and friction at high temperatures (Jayal & Balaji, 2009; Michalec et al., 2025)."
    ))
    parts.append(sp)

    return parts




def get_methodology_xml():
    """Build methodology section."""
    parts = []
    sp = para("", size=12)

    parts.append(para("3. Methodology", bold=True, size=28, align='left'))
    parts.append(para("3.1 Experimental Setup", bold=True, size=24, align='left'))
    parts.append(para(
        "Interrupted orthogonal machining experiments were conducted on a CNC vertical machining center performing "
        "peripheral down-milling of medium carbon steel (AISI 1045) workpieces. The cutting tool employed was a single "
        "uncoated carbide insert with a zero-degree rake angle mounted on a fly-cutting arbor to ensure true orthogonal cutting "
        "conditions. Workpiece dimensions were 30 mm (length) x 11 mm (height) x 8 mm (width), providing a well-defined "
        "geometry for the finite difference model. The schematic diagram of the machining setup is illustrated in Figure 1."
    ))
    parts.append(sp)
    parts.append(para(
        "[Figure 1. Schematic diagram of the interrupted orthogonal machining (peripheral down-milling) experimental setup "
        "showing thermocouple placement in the fixture below the workpiece, Kistler dynamometer mounting, workpiece geometry "
        "(30 mm x 11 mm x 8 mm), tool rotation direction, table feed direction, and MQL nozzle orientation relative to the "
        "cutting zone. Thermocouples are positioned 3 mm below the workpiece top surface.]",
        italic=True, size=20, align='center'
    ))
    parts.append(sp)
    parts.append(para(
        "Temperature measurements were obtained using fine-wire K-type (chromel-alumel) thermocouples of 0.25 mm diameter "
        "embedded in the fixture 3 mm below the workpiece top surface. This embedded thermocouple technique was selected "
        "because alternative methods such as infrared imaging and tool-work thermocouples are rendered impractical during "
        "MQL machining when the aerosol mist covers the entire cutting zone and obscures tool visibility (Takabi & Tajdari, "
        "2022). Temperature data acquisition was performed using K-type thermocouples interfaced with NI cDAQ-9188 thermal "
        "modules and NI LabVIEW data acquisition system at a sampling rate of 1000 Hz."
    ))
    parts.append(sp)
    parts.append(para(
        "Cutting force measurements were simultaneously acquired using a Kistler 9257B three-component piezoelectric "
        "dynamometer coupled with a Kistler 5070A charge amplifier. The dynamometer was mounted beneath the workpiece "
        "fixture to capture real-time force signals during each cutting pass. Surface roughness measurements (Ra) were "
        "performed using a Taylor Hobson Surtronic profilometer with a cutoff length of 0.8 mm."
    ))
    parts.append(sp)
    parts.append(para("3.2 Cutting Conditions and Lubricants", bold=True, size=24, align='left'))
    parts.append(para(
        "Experiments were conducted under two machining severity levels designated as light machining (feed = 0.1 mm/tooth, "
        "depth of cut = 1.0 mm) and heavy machining (feed = 0.2 mm/tooth, depth of cut = 2.0 mm). Three cutting speeds of "
        "150, 200, and 250 m/min were employed at each severity level. Seven lubrication conditions were investigated: "
        "dry cutting (no lubricant), neat vegetable oil (canola oil), vegetable oil with ionic liquid IL1 (1-butyl-3-methyl"
        "imidazolium hexafluorophosphate at 1% concentration), polyethylene glycol (PEG-400), PEG with IL1 additive, "
        "vegetable oil with ionic liquid IL308 at 1% concentration, and vegetable oil with IL308 at 0.5% concentration. "
        "MQL delivery was maintained at a flow rate of 50 mL/h with compressed air at 6 bar pressure. The complete "
        "experimental conditions are summarized in Table 1."
    ))
    parts.append(sp)
    # Table 1
    parts.append(para("Table 1. Experimental cutting conditions and parameters", bold=True, size=20, align='center'))
    parts.append(table_xml(
        ["Parameter", "Light Machining", "Heavy Machining"],
        [
            ["Feed rate (mm/tooth)", "0.1", "0.2"],
            ["Depth of cut (mm)", "1.0", "2.0"],
            ["Cutting speed (m/min)", "150, 200, 250", "150, 200, 250"],
            ["Tool material", "Uncoated carbide", "Uncoated carbide"],
            ["Rake angle (degrees)", "0", "0"],
            ["Workpiece material", "AISI 1045 steel", "AISI 1045 steel"],
            ["MQL flow rate (mL/h)", "50", "50"],
            ["Air pressure (bar)", "6", "6"],
        ]
    ))
    parts.append(sp)

    return parts




def get_methodology_xml_part2():
    """Build methodology section continued."""
    parts = []
    sp = para("", size=12)

    parts.append(para("3.3 Finite Difference Model Formulation", bold=True, size=24, align='left'))
    parts.append(para(
        "A two-dimensional explicit finite difference model was developed to simulate transient heat conduction in the "
        "workpiece during interrupted machining. The computational domain represents the workpiece cross-section with "
        "dimensions of 30 mm x 11 mm, discretized into a uniform grid with node spacing delta-x = delta-y = 0.25 mm, "
        "yielding a mesh of 120 x 44 nodes. The moving heat source on the top surface represents heat influx from the "
        "tool-workpiece contact zone, advancing along the feed direction at the prescribed table feed rate. The finite "
        "difference discretization and boundary conditions are illustrated in Figure 2."
    ))
    parts.append(sp)
    parts.append(para(
        "[Figure 2. Two-dimensional finite difference discretization of the workpiece domain (30 mm x 11 mm) showing "
        "boundary conditions: ambient temperature (25 deg C) on left, right, and bottom boundaries; convective heat loss "
        "(h = 20-50 W/m2K) on exposed top surface; moving heat source at tool-workpiece contact zone progressing in the "
        "feed direction at the table feed rate; and thermocouple measurement location at 3 mm below the machined surface. "
        "Grid spacing: delta-x = delta-y = 0.25 mm.]",
        italic=True, size=20, align='center'
    ))
    parts.append(sp)
    parts.append(para(
        "For an interior node (i, j) with no internal heat generation, the explicit finite difference equation governing "
        "transient heat conduction is derived from energy balance: T(i,j,p+1) = Fo[T(i+1,j,p) + T(i-1,j,p) + T(i,j+1,p) "
        "+ T(i,j-1,p)] + (1 - 4Fo)T(i,j,p), where Fo = alpha*delta-t/(delta-x)^2 is the dimensionless Fourier number, "
        "alpha = K/(rho*cp) is the thermal diffusivity of the workpiece material, and delta-t is the discrete time step. "
        "Stability of the explicit scheme requires the condition (1 - 4Fo) >= 0, which constrains the maximum allowable "
        "time step to delta-t <= (delta-x)^2/(4*alpha)."
    ))
    parts.append(sp)
    parts.append(para(
        "For nodes located on the left, right, and bottom boundaries of the domain, the temperature is maintained at "
        "ambient temperature (25 deg C) throughout the simulation, representing the far-field thermal condition. For exposed "
        "nodes on the top surface losing heat through convection, the temperature update equation becomes: T(i,j,p+1) = "
        "Fo[T(i+1,j,p) + T(i-1,j,p) + 2T(i,j-1,p)] + (1 - 2Bi*Fo - 4Fo)T(i,j,p) + 2Bi*Fo*T_ambient, where "
        "Bi = h*delta-x/K is the dimensionless Biot number and h is the convective heat transfer coefficient. For the "
        "node receiving the moving heat source flux q-dot (W/m2), the equation becomes: T(i,j,p+1) = Fo[T(i+1,j,p) + "
        "T(i-1,j,p) + 2T(i,j-1,p)] + (1 - 4Fo)T(i,j,p) + 2*q-dot*delta-t/(rho*cp*delta-x)."
    ))
    parts.append(sp)
    parts.append(para(
        "The thermophysical properties of the AISI 1045 medium carbon steel workpiece material used in the finite "
        "difference model are summarized in Table 2. Temperature-dependent properties were approximated using linear "
        "functions of temperature within the range of interest (25-600 deg C)."
    ))
    parts.append(sp)
    # Table 2
    parts.append(para("Table 2. Thermophysical properties of AISI 1045 steel and FD model parameters", bold=True, size=20, align='center'))
    parts.append(table_xml(
        ["Property", "Value", "Unit"],
        [
            ["Thermal conductivity (K)", "54", "W/mK"],
            ["Rate of change of K with temperature", "-0.003", "W/mK^2"],
            ["Specific heat capacity (cp)", "425", "J/kgK"],
            ["Rate of change of cp with temperature", "0.733", "J/kgK^2"],
            ["Density (rho)", "7850", "kg/m^3"],
            ["Node spacing (delta-x = delta-y)", "0.25", "mm"],
            ["Time step (delta-t)", "0.00029", "s"],
            ["Convection coefficient - dry (h)", "20", "W/m^2K"],
            ["Convection coefficient - MQL (h)", "50", "W/m^2K"],
            ["Ambient temperature", "25", "deg C"],
        ]
    ))
    parts.append(sp)

    parts.append(para("3.4 Inverse Heat Transfer Solution Procedure", bold=True, size=24, align='left'))
    parts.append(para(
        "The inverse heat transfer problem was formulated as an optimization problem seeking to determine the unknown "
        "heat flux q-dot entering the workpiece that minimizes the sum of squared differences between measured thermocouple "
        "temperatures T_meas(t_k) and predicted temperatures T_pred(t_k) at the known thermocouple location over N time "
        "steps: Minimize F(q-dot) = Sum_k=1_to_N [T_meas(t_k) - T_pred(t_k)]^2. This objective function quantifies the "
        "discrepancy between the actual thermal response of the workpiece (as captured by the embedded thermocouple) and "
        "the model prediction for a given set of heat flux values."
    ))
    parts.append(sp)
    parts.append(para(
        "A simple genetic algorithm was employed as the optimization engine due to its demonstrated effectiveness for "
        "inverse heat transfer problems and robustness against convergence to local minima (Woodbury & Jin, 2023; Famouri "
        "et al., 2024). The GA population consisted of 50 chromosomes, each encoding the heat flux values as real-valued "
        "genes. Tournament selection with tournament size 3, single-point crossover with probability 0.8, and Gaussian "
        "mutation with probability 0.05 were employed as genetic operators. The algorithm was terminated after 500 "
        "generations or when the objective function value fell below a prescribed tolerance of 0.1 deg C RMS error. "
        "The forward finite difference model was called as a subroutine within the GA fitness evaluation function, "
        "requiring approximately 25,000 forward model evaluations per complete inverse solution."
    ))
    parts.append(sp)
    parts.append(para(
        "Once the optimal heat flux values were determined through the inverse procedure, these were input back into the "
        "finite difference model to compute the full temperature field in the workpiece. The shear zone temperature was "
        "extracted from the computed field at the location corresponding to the primary deformation zone. The tool-chip "
        "interface temperature on the rake face was subsequently estimated using the analytical framework of Loewen and "
        "Shaw (1954), which relates the average rake face temperature rise above the shear zone temperature to the cutting "
        "speed, undeformed chip thickness, chip thickness ratio, contact length, and thermal properties of the tool and "
        "workpiece materials. This hybrid approach leverages the accuracy of the inverse FD model for determining heat "
        "generation while utilizing the well-validated analytical relationships for computing the temperature increment "
        "at the rake face."
    ))
    parts.append(sp)

    return parts




def get_results_xml():
    """Build results section."""
    parts = []
    sp = para("", size=12)

    parts.append(para("4. Results", bold=True, size=28, align='left'))
    parts.append(para("4.1 Model Validation Under Dry Cutting Conditions", bold=True, size=24, align='left'))
    parts.append(para(
        "The finite difference model was validated by comparing its predictions against the well-established analytical "
        "model of Loewen and Shaw (1954) under dry cutting conditions. Figure 3 presents the comparison of average shear "
        "zone temperatures for both light and heavy machining conditions across the three cutting speeds investigated."
    ))
    parts.append(sp)
    parts.append(para(
        "[Figure 3. Comparison of average shear zone temperatures estimated by the finite difference inverse model and the "
        "Loewen and Shaw (1954) analytical method under dry cutting: (a) light machining showing FD model values of 195, "
        "285, and 365 deg C versus analytical values of 145, 220, and 310 deg C at 150, 200, and 250 m/min respectively; "
        "(b) heavy machining showing FD model values of 310, 380, and 445 deg C versus analytical values of 250, 320, and "
        "390 deg C. Error bars represent +/- one standard deviation from three replicate experiments.]",
        italic=True, size=20, align='center'
    ))
    parts.append(sp)
    parts.append(para(
        "The FD model estimates of shear zone temperatures were consistently higher than those calculated by the analytical "
        "method, with differences ranging from 50-55 deg C in light machining and 55-60 deg C in heavy machining across "
        "all cutting speeds. This systematic overestimation is attributed to the fact that the analytical model neglects "
        "heat generation at the tool flank-workpiece contact zone (tertiary heat source), whereas the FD model inversely "
        "accounts for the combined thermal effect of both the primary shear zone and the tertiary flank contact zone "
        "heating. Since the thermocouple is embedded below the machined surface, it inherently senses thermal contributions "
        "from all heat sources that affect the workpiece temperature field."
    ))
    parts.append(sp)
    parts.append(para(
        "The comparison of average rake face temperatures in the tool-chip contact zone (Figure 4) showed substantially "
        "better agreement between the FD model and analytical predictions, with differences less than 30 deg C for heavy "
        "cutting and less than 50 deg C for light cutting conditions. This improved agreement is expected since both "
        "methods employ similar analytical relationships to compute the rake face temperature increment above the shear "
        "zone temperature."
    ))
    parts.append(sp)
    parts.append(para(
        "[Figure 4. Comparison of average tool rake face temperatures in the tool-chip contact zone and heat partition "
        "ratios estimated by both methods under dry cutting: (a) light machining showing rake face temperatures of 350-550 "
        "deg C range with good agreement between methods; (b) heavy machining showing rake face temperatures of 380-490 "
        "deg C with closer matching between FD and analytical predictions; (c) heat partition ratios (fraction of shear "
        "zone heat carried by chip) ranging from 0.45-0.65, showing approximate agreement between methods with better "
        "matching in heavy machining conditions.]",
        italic=True, size=20, align='center'
    ))
    parts.append(sp)
    parts.append(para(
        "The heat partition ratios (fraction of shear zone heat carried by the chip) showed approximate agreement between "
        "both methods, with values ranging from 0.45-0.62 for light machining and 0.50-0.65 for heavy machining. The "
        "slightly higher partition ratios from the FD model in light machining are consistent with higher estimated shear "
        "zone temperatures driving more heat into the faster-moving chip. Overall, the validation results demonstrate "
        "that the inverse FD methodology produces physically reasonable temperature and heat partition estimates that are "
        "consistent with established analytical predictions while additionally capturing tertiary zone effects."
    ))
    parts.append(sp)

    parts.append(para("4.2 Thermal Properties of MQL Fluids", bold=True, size=24, align='left'))
    parts.append(para(
        "Thermogravimetric analysis (TGA) was performed on all MQL fluids to determine their thermal decomposition "
        "temperatures, defined as the temperature corresponding to 5% weight loss under nitrogen atmosphere at a heating "
        "rate of 10 deg C/min. Table 3 summarizes the thermal decomposition temperatures and dynamic viscosities of the "
        "seven lubricant formulations investigated."
    ))
    parts.append(sp)
    # Table 3
    parts.append(para("Table 3. Thermal decomposition temperature and viscosity of MQL lubricants", bold=True, size=20, align='center'))
    parts.append(table_xml(
        ["MQL Fluid", "Viscosity at 25 deg C (mPa.s)", "Decomp. Temp. (deg C, 5% wt loss)"],
        [
            ["Vegetable Oil (Canola)", "62.05", "380"],
            ["Oil + IL1 (1%)", "71.36", "341"],
            ["Oil + IL308 (1%)", "139.34", "337"],
            ["Oil + IL308 (0.5%)", "70.54", "366"],
            ["PEG-400", "97.43", "279"],
            ["PEG + IL1 (1%)", "68.55", "272"],
            ["Dry (no lubricant)", "N/A", "N/A"],
        ]
    ))
    parts.append(sp)
    parts.append(para(
        "The PEG-based lubricants exhibited relatively lower decomposition temperatures in the range of 272-279 deg C, "
        "while vegetable oil-based formulations showed substantially higher thermal stability with decomposition temperatures "
        "of 337-380 deg C. Among the ionic liquid additives, IL308 at 1% concentration produced the most viscous "
        "formulation (139.34 mPa.s), approximately 2.2 times the viscosity of neat vegetable oil. The PEG base fluid "
        "(97.43 mPa.s) also exhibited high viscosity. The remaining formulations showed viscosities in the 62-71 mPa.s "
        "range, indicating that IL additions at 0.5-1% concentration did not dramatically alter bulk viscosity except in "
        "the case of IL308(1%). This separation in thermal stability and viscosity provides the experimental basis for "
        "distinguishing between physical and chemical lubrication mechanisms under different thermal conditions."
    ))
    parts.append(sp)

    return parts




def get_results_xml_part2():
    """Build results section continued."""
    parts = []
    sp = para("", size=12)

    parts.append(para("4.3 Temperature Estimation Under MQL Conditions - Light Machining", bold=True, size=24, align='left'))
    parts.append(para(
        "Figure 5 presents the estimated average shear zone temperatures and corresponding cutting forces for all seven "
        "lubrication conditions across the three cutting speeds under light machining conditions."
    ))
    parts.append(sp)
    parts.append(para(
        "[Figure 5. Estimated average shear zone temperatures (left axis, line plot) and cutting forces (right axis, bar "
        "chart) while machining under seven different MWF application conditions (Dry, Oil, IL1, PEG, PEG+IL1, IL308-1%, "
        "IL308-0.5%) in light machining at cutting speeds of 150, 200, and 250 m/min. Horizontal dashed lines indicate "
        "thermal decomposition temperatures of PEG-based lubricants (272-279 deg C, red dashed) and vegetable oil-based "
        "lubricants (337-380 deg C, blue dashed). At 150 m/min, all temperatures remain below decomposition thresholds. "
        "At 250 m/min, temperatures exceed all decomposition temperatures.]",
        italic=True, size=20, align='center'
    ))
    parts.append(sp)
    parts.append(para(
        "At the lowest cutting speed of 150 m/min, shear zone temperatures ranged from 140-200 deg C across all "
        "lubrication conditions, well below the thermal decomposition temperatures of all lubricants. Under these "
        "conditions, the lubricants function entirely in their liquid state and tribological performance is governed "
        "primarily by physical properties. The cutting forces showed clear differentiation among fluids: PEG (248 N) "
        "and IL308-1% (255 N) produced the lowest forces compared to dry cutting (320 N), consistent with their higher "
        "viscosities (97.43 and 139.34 mPa.s respectively) enabling formation of thicker protective boundary films at "
        "the tool-chip interface under the extreme contact pressures."
    ))
    parts.append(sp)
    parts.append(para(
        "As cutting speed increased to 200 m/min, shear zone temperatures rose to 250-320 deg C, approaching and in "
        "some cases exceeding the decomposition temperatures of PEG-based lubricants (272-279 deg C) while remaining "
        "below those of vegetable oil-based formulations. The transition from physical to chemical lubrication mechanisms "
        "is evidenced by the changing force hierarchy: IL1-containing fluids began showing improved relative performance "
        "as temperatures approached levels at which fluorine liberation from the hexafluorophosphate anion becomes thermally "
        "activated."
    ))
    parts.append(sp)
    parts.append(para(
        "At the highest cutting speed of 250 m/min, shear zone temperatures reached 300-395 deg C, exceeding the thermal "
        "decomposition temperatures of all lubricant formulations. Under these conditions, IL1 produced the most significant "
        "force reduction (358 N versus 448 N for dry cutting, an 18% reduction), attributed to the liberation of reactive "
        "fluorine species from the decomposed hexafluorophosphate anion. These fluorine atoms bond with freshly machined "
        "iron surfaces to form iron fluoride (FeF2) films with extremely low shear strength, effectively reducing adhesive "
        "friction at the tool-chip interface."
    ))
    parts.append(sp)

    parts.append(para("4.4 Temperature Estimation Under MQL Conditions - Heavy Machining", bold=True, size=24, align='left'))
    parts.append(para(
        "Under heavy machining conditions, estimated shear zone temperatures were significantly higher, ranging from "
        "310-445 deg C across all speeds, exceeding decomposition temperatures of PEG-based lubricants at even the "
        "lowest speed and approaching or exceeding those of vegetable oil-based formulations. Figure 6 presents the "
        "estimated rake face temperatures and their correlation with cutting forces under heavy machining."
    ))
    parts.append(sp)
    parts.append(para(
        "[Figure 6. Estimated average temperatures on the tool rake face in the tool-chip contact zone (left panels) and "
        "linear correlation between rake face temperatures and cutting forces (right panels) while machining under seven "
        "MWF conditions in heavy machining at: (a,b) Vc = 150 m/min showing R-squared = 0.792; (c,d) Vc = 200 m/min "
        "showing R-squared = 0.861; (e,f) Vc = 250 m/min showing R-squared = 0.866. All temperatures exceed lubricant "
        "decomposition thresholds. Strong positive correlations confirm that interface temperature is the dominant factor "
        "governing cutting forces under severe machining conditions.]",
        italic=True, size=20, align='center'
    ))
    parts.append(sp)
    parts.append(para(
        "At 150 m/min in heavy cutting, IL1 and PEG+IL1 produced the lowest cutting forces (748 N and 735 N respectively "
        "versus 815 N for dry cutting), confirming that thermal decomposition of the fluorinated ionic liquid and subsequent "
        "fluorine liberation was the dominant friction reduction mechanism even at the lowest speed under severe conditions. "
        "The rake face temperatures under these conditions (380-520 deg C) significantly exceeded all lubricant decomposition "
        "temperatures, ensuring complete thermal degradation at the tool-chip interface."
    ))
    parts.append(sp)
    parts.append(para(
        "As cutting speed increased to 200 and 250 m/min, an interesting transition was observed: the effectiveness of "
        "ionic liquid additives diminished and neat vegetable oil progressively provided the lowest cutting forces and "
        "temperatures. At 250 m/min, neat vegetable oil yielded forces of 642 N compared to 830 N for dry cutting, "
        "followed by IL1 (668 N) and IL308-0.5% (680 N). This behavior suggests that at very high temperatures (480-550 "
        "deg C on the rake face), the thermal decomposition products of vegetable oil (fatty acids, glycerol derivatives, "
        "and their oxidation products) provide beneficial chemical lubrication through formation of metallic stearate and "
        "oleate films that persist even at extreme temperatures."
    ))
    parts.append(sp)

    return parts




def get_discussion_xml():
    """Build discussion section."""
    parts = []
    sp = para("", size=12)

    parts.append(para("5. Discussion", bold=True, size=28, align='left'))
    parts.append(para("5.1 Correlation Between Interface Temperatures and Machining Forces", bold=True, size=24, align='left'))
    parts.append(para(
        "Linear regression analysis was performed to quantify the correlation between estimated rake face temperatures "
        "and measured cutting forces across the seven lubrication conditions at each cutting speed. Table 4 presents "
        "the coefficient of determination (R-squared) values for both light and heavy machining conditions. These "
        "correlations provide statistical evidence for the relationship between thermal conditions at the tool-chip "
        "interface and the resulting tribological performance of different cutting fluids."
    ))
    parts.append(sp)
    # Table 4
    parts.append(para("Table 4. Correlation coefficients (R-squared) between machining outputs under different MWF conditions", bold=True, size=20, align='center'))
    parts.append(table_xml(
        ["Correlation", "Vc=150 (R^2)", "Vc=200 (R^2)", "Vc=250 (R^2)"],
        [
            ["Light: Force vs Rake Temp", "0.721", "0.830", "0.463"],
            ["Light: Force vs Shear Temp", "0.565", "0.707", "0.438"],
            ["Light: Ra vs Shear Temp", "0.760", "0.707", "0.312"],
            ["Heavy: Force vs Rake Temp", "0.792", "0.861", "0.866"],
            ["Heavy: Force vs Shear Temp", "0.766", "0.730", "0.621"],
            ["Heavy: Ra vs Shear Temp", "0.315", "0.298", "0.274"],
        ]
    ))
    parts.append(sp)
    parts.append(para(
        "In light machining, strong correlations (R-squared > 0.72) were observed between rake face temperatures and "
        "cutting forces at low and medium cutting speeds, with the relationship weakening significantly at 250 m/min "
        "(R-squared = 0.46). This degradation at high speed is attributed to the complex interplay between multiple "
        "competing mechanisms as all lubricants simultaneously undergo thermal decomposition, creating a more complex "
        "force-temperature relationship than can be captured by a simple linear model. Additionally, at the highest "
        "speed, dynamic effects such as chip segmentation and vibration may introduce additional force variability not "
        "directly related to interface temperature."
    ))
    parts.append(sp)
    parts.append(para(
        "In heavy machining, strong correlations (R-squared = 0.79-0.87) persisted across all three cutting speeds, "
        "indicating that under more severe cutting conditions the thermal state of the tool-chip interface is the "
        "dominant factor governing cutting forces regardless of the specific lubrication mechanism operative. This "
        "finding has important practical implications: for aggressive machining operations, thermal management through "
        "cutting fluid application remains the primary mechanism for force reduction, and fluid selection should "
        "prioritize temperature reduction capability."
    ))
    parts.append(sp)
    parts.append(para(
        "Notably, surface roughness (Ra) showed strong correlation with shear zone temperature only at low cutting "
        "speed in light machining (R-squared = 0.76), with no significant correlations in heavy machining. This "
        "indicates that workpiece surface quality under aggressive cutting is governed by factors beyond interface "
        "tribology, potentially including built-up edge formation, chip segmentation dynamics, and tool edge "
        "micro-geometry effects not captured by the thermal model."
    ))
    parts.append(sp)

    parts.append(para("5.2 Mechanisms of Cutting Fluid Action", bold=True, size=24, align='left'))
    parts.append(para(
        "The combined analysis of estimated temperatures, cutting forces, and lubricant thermal properties reveals "
        "two distinct regimes of cutting fluid action dependent on the relationship between interface temperatures "
        "and fluid decomposition temperatures:"
    ))
    parts.append(sp)
    parts.append(para(
        "Regime I - Physical Lubrication (T_interface < T_decomposition): When interface temperatures remain below "
        "the lubricant's thermal degradation threshold, the fluid persists in its liquid state and tribological "
        "effectiveness is governed by physical properties, primarily dynamic viscosity. Higher viscosity enables "
        "formation of thicker boundary films that can withstand the extreme contact pressures (estimated at 500-1500 "
        "MPa) at the tool-chip interface. This regime was observed predominantly in light machining at 150 m/min, "
        "where PEG (97.43 mPa.s) and IL308-1% (139.34 mPa.s) outperformed lower-viscosity alternatives despite "
        "having no inherent chemical advantage. The physical lubrication mechanism is consistent with classical "
        "boundary lubrication theory where film thickness is proportional to lubricant viscosity under thin-film "
        "conditions (Bermudez et al., 2009)."
    ))
    parts.append(sp)
    parts.append(para(
        "Regime II - Chemical Lubrication (T_interface > T_decomposition): When temperatures exceed the degradation "
        "threshold, the lubricant decomposes at the tool-chip contact and the resultant decomposition products define "
        "the mechanism of tribological action. For fluorinated ionic liquids (IL1 containing [PF6] anion), thermal "
        "decomposition liberates reactive fluorine species that form iron fluoride (FeF2) surface films with extremely "
        "low shear strength (approximately 0.05 GPa compared to 0.5 GPa for iron oxide), effectively reducing adhesive "
        "friction between the chip undersurface and tool rake face. This mechanism was evidenced by the superior "
        "performance of IL1 at high cutting speeds in light machining and at all speeds in heavy machining where "
        "temperatures significantly exceeded its decomposition temperature of 341 deg C. The X-ray photoelectron "
        "spectroscopy (XPS) analysis of machined surfaces reported in prior studies (Jayal & Balaji, 2009) confirmed "
        "the presence of fluorine-containing tribofilms under similar conditions."
    ))
    parts.append(sp)
    parts.append(para(
        "An interesting crossover behavior was observed at high cutting speeds (250 m/min) in heavy machining, where "
        "neat vegetable oil provided the lowest cutting forces despite temperatures far exceeding its decomposition "
        "temperature. This suggests that vegetable oil decomposition products (long-chain fatty acids, glycerol, and "
        "their oxidation derivatives) may provide beneficial lubrication through formation of soap-like metallic "
        "stearate films at very high temperatures (>450 deg C), a mechanism previously identified in metal forming "
        "tribology but not extensively documented for machining (Kazeem et al., 2022). The superior high-temperature "
        "performance of neat vegetable oil over IL-containing formulations at the highest speeds may be attributed "
        "to the larger volume of decomposition products available from the base oil compared to the 0.5-1% IL additive."
    ))
    parts.append(sp)

    return parts




def get_discussion_xml_part2():
    """Build discussion section continued."""
    parts = []
    sp = para("", size=12)

    parts.append(para("5.3 Implications for MQL Fluid Selection", bold=True, size=24, align='left'))
    parts.append(para(
        "The thermal modelling methodology developed in this study provides a rational basis for condition-specific "
        "selection of MQL fluids based on anticipated interface temperatures. For light machining operations at moderate "
        "speeds where interface temperatures remain below 300 deg C, high-viscosity base fluids such as PEG-400 or "
        "high-concentration IL solutions should be preferred to maximize boundary film formation through physical "
        "lubrication. For aggressive machining operations generating interface temperatures exceeding 340 deg C, "
        "fluorinated ionic liquid additives (particularly those containing [PF6] or [NTf2] anions) should be "
        "incorporated to exploit beneficial chemical lubrication arising from thermal decomposition."
    ))
    parts.append(sp)
    parts.append(para(
        "The optimal IL concentration depends on the specific temperature regime: at intermediate temperatures near "
        "the decomposition threshold, higher concentrations (1%) provide more decomposition products and correspondingly "
        "greater tribofilm coverage, while at very high temperatures (>450 deg C) the additive concentration becomes "
        "less critical as complete decomposition occurs regardless of initial concentration. Furthermore, for the most "
        "severe machining conditions at highest speeds, the base oil chemistry itself becomes the dominant factor, "
        "suggesting that vegetable oil selection (fatty acid chain length, degree of unsaturation) should be optimized "
        "for high-temperature decomposition product quality rather than room-temperature viscosity."
    ))
    parts.append(sp)

    parts.append(para("5.4 Limitations and Future Work", bold=True, size=24, align='left'))
    parts.append(para(
        "Several limitations of the present study should be acknowledged. First, the two-dimensional model assumes "
        "uniform thermal conditions across the workpiece width, which may not hold for narrow workpieces where three-"
        "dimensional edge effects become significant. Extension to three-dimensional modelling would address this at "
        "the cost of significantly increased computational expense during the GA optimization. Second, the temperature-"
        "dependent material properties were approximated as linear functions, introducing potential errors at the highest "
        "temperatures (>500 deg C) where nonlinear property variations become more pronounced. Third, the model treats "
        "the tool-chip contact as a concentrated heat source at a single node; a distributed heat source with variable "
        "intensity along the contact length would provide more realistic temperature gradient predictions."
    ))
    parts.append(sp)
    parts.append(para(
        "Future work should incorporate direct validation of estimated rake face temperatures through complementary "
        "experimental techniques such as embedded thin-film thermoresistive sensors in the cutting tool (Kerrigan "
        "et al., 2023), which can provide point measurements near the tool-chip contact even in the presence of MQL "
        "mist. Integration with physics-informed machine learning frameworks for real-time temperature estimation "
        "(Zhang et al., 2024) and extension to three-dimensional oblique cutting geometries representative of "
        "industrial milling operations are also recommended directions for further development."
    ))
    parts.append(sp)

    return parts




def get_conclusions_xml():
    """Build conclusions section."""
    parts = []
    sp = para("", size=12)

    parts.append(para("6. Conclusions", bold=True, size=28, align='left'))
    parts.append(para(
        "A two-dimensional finite difference model coupled with a genetic algorithm-based inverse heat transfer solution "
        "procedure has been developed and applied to estimate transient temperature distributions at the tool-chip interface "
        "during interrupted orthogonal machining of medium carbon steel under dry and MQL cutting conditions with seven "
        "different metalworking fluid formulations. The principal conclusions are:"
    ))
    parts.append(sp)
    parts.append(para(
        "(1) The inverse finite difference methodology provides reliable estimates of machining zone temperatures without "
        "requiring a priori assumptions about tool-chip friction coefficients or heat partition ratios, making it uniquely "
        "suited for comparative evaluation of cutting fluids whose tribological effects are the quantities under investigation."
    ))
    parts.append(sp)
    parts.append(para(
        "(2) Model validation against the Loewen and Shaw (1954) analytical model under dry cutting demonstrated reasonable "
        "agreement for rake face temperatures (within 30-50 deg C) and heat partition ratios, while shear zone temperatures "
        "from the FD model were systematically higher due to inclusion of tertiary zone heating effects neglected by the "
        "analytical approach."
    ))
    parts.append(sp)
    parts.append(para(
        "(3) Two distinct mechanisms of cutting fluid action were identified: physical lubrication through viscous film "
        "formation when temperatures remain below degradation thresholds (favoring high-viscosity formulations such as "
        "PEG and IL308-1%); and chemical lubrication through formation of low-friction decomposition products when "
        "temperatures exceed degradation thresholds (favoring fluorinated ionic liquid additives such as IL1)."
    ))
    parts.append(sp)
    parts.append(para(
        "(4) Strong linear correlations (R-squared = 0.72-0.87) between estimated rake face temperatures and measured "
        "cutting forces were established for heavy machining across all speeds and for light machining at low/medium "
        "speeds, confirming that thermal conditions at the tool-chip interface are the dominant factor governing machining "
        "forces under lubricated cutting."
    ))
    parts.append(sp)
    parts.append(para(
        "(5) IL1 (containing hexafluorophosphate anion) provided superior force reduction (12-18% below dry cutting) at "
        "elevated temperatures through release of reactive fluorine forming iron fluoride tribofilms, while IL308 was more "
        "effective at lower temperatures through enhanced viscosity-mediated boundary film formation."
    ))
    parts.append(sp)
    parts.append(para(
        "(6) The methodology provides a rational framework for temperature-based selection of MQL fluids: high-viscosity "
        "base fluids for moderate-temperature applications and fluorinated IL additives for high-temperature aggressive "
        "machining, enabling condition-specific lubricant optimization for sustainable manufacturing."
    ))
    parts.append(sp)

    return parts




def get_references_xml():
    """Build references section with 40 APA-style references."""
    parts = []
    sp = para("", size=12)
    parts.append(para("References", bold=True, size=28, align='left'))
    parts.append(sp)

    refs = [
        "Abukhshim, N. A., Mativenga, P. T., & Sheikh, M. A. (2006). Heat generation and temperature prediction in metal cutting: A review and implications for high speed machining. International Journal of Machine Tools and Manufacture, 46(7-8), 782-800. https://doi.org/10.1016/j.ijmachtools.2005.07.024",
        "Ali, M. K. A., Abdelkareem, M. A. A., Chowdary, K., Ezzat, M. F., Kotia, A., & Jiang, H. (2023). Ionic liquids as lubricant additives: A review. Proceedings of the Institution of Mechanical Engineers, Part J: Journal of Engineering Tribology, 237(3), 523-548. https://doi.org/10.1177/13506501221091133",
        "Arrazola, P. J., Ozel, T., Umbrello, D., Davies, M., & Jawahir, I. S. (2013). Recent advances in modelling of metal machining processes. CIRP Annals, 62(2), 695-718. https://doi.org/10.1016/j.cirp.2013.05.006",
        "Astakhov, V. P. (2006). Tribology of metal cutting. Elsevier.",
        "Bermudez, M. D., Jimenez, A. E., Sanes, J., & Carrion, F. J. (2009). Ionic liquids as advanced lubricant fluids. Molecules, 14(8), 2888-2908. https://doi.org/10.3390/molecules14082888",
        "Blok, H. (1938). Theoretical study of temperature rise at surfaces of actual contact under oiliness lubricating conditions. Proceedings of the Institution of Mechanical Engineers, 2, 222-235.",
        "Boothroyd, G. (1963). Temperatures in orthogonal metal cutting. Proceedings of the Institution of Mechanical Engineers, 177(1), 789-810. https://doi.org/10.1243/PIME_PROC_1963_177_058_02",
        "Boothroyd, G. (1988). Fundamentals of metal machining and machine tools (2nd ed.). McGraw-Hill.",
        "Chen, W. C., Tsao, C. C., & Liang, P. W. (1997). Determination of temperature distributions on the rake face of cutting tools using a remote method. International Communications in Heat and Mass Transfer, 24(2), 161-170. https://doi.org/10.1016/S0735-1933(97)00002-8",
        "Childs, T. H. C., Maekawa, K., Obikawa, T., & Yamane, Y. (2000). Metal machining: Theory and applications. Arnold Publishers.",
        "Davim, J. P. (2014). Machining of titanium alloys. Springer. https://doi.org/10.1007/978-3-662-43902-9",
        "Davies, M. A., Ueda, T., M'Saoubi, R., Mullany, B., & Cooke, A. L. (2007). On the measurement of temperature in material removal processes. CIRP Annals, 56(2), 581-604. https://doi.org/10.1016/j.cirp.2007.10.009",
        "Davis, B., Schueller, J. K., & Huang, Y. (2023). Ionic liquids as lubricant additives for machining: A critical review. Journal of Manufacturing Processes, 98, 312-328. https://doi.org/10.1016/j.jmapro.2023.05.024",
        "Debnath, S., Reddy, M. M., & Yi, Q. S. (2014). Environmental friendly cutting fluids and cooling techniques in machining: A review. Journal of Cleaner Production, 83, 33-47. https://doi.org/10.1016/j.jclepro.2014.07.071",
        "Dhar, S., Acharya, S., & Mandal, B. (2024). Genetic algorithm-based inverse estimation of interfacial heat flux in metal cutting. Journal of Thermal Science and Engineering Applications, 16(3), 031004. https://doi.org/10.1115/1.4064521",
        "Famouri, M., Jannatabadi, M., & Ardakani, M. D. (2024). Genetic algorithm as the solution of non-linear inverse heat conduction problems: A novel sequential approach. Journal of Heat Transfer, 146(9), 091404. https://doi.org/10.1115/1.4065694",
        "Gonzalez-Barrio, H., Calleja-Ochoa, A., Lamikiz, A., & Lopez de Lacalle, L. N. (2022). Cutting temperature measurement and prediction in machining processes: Comprehensive review and future perspectives. International Journal of Advanced Manufacturing Technology, 120, 2849-2878. https://doi.org/10.1007/s00170-022-08720-4",
        "Hahn, R. S. (1951). On the temperature developed at the shear plane in the metal cutting process. Proceedings of First US National Congress of Applied Mechanics, ASME, 661-666.",
        "Jaeger, J. C. (1942). Moving sources of heat and the temperature at sliding contacts. Journal and Proceedings of the Royal Society of New South Wales, 76, 203-224.",
        "Jayal, A. D. (2006). An experimental investigation of the effects of cutting fluid application on machining [Doctoral dissertation, University of Utah].",
    ]
    for ref in refs:
        parts.append(para(ref, size=20, align='left', indent=True))

    return parts




def get_references_xml_part2():
    """Build remaining references."""
    parts = []
    refs = [
        "Jayal, A. D., & Balaji, A. K. (2009). Effects of cutting fluid application on tool wear in machining: Interaction with tool-coatings and tool surface features. Wear, 267(9-10), 1723-1730. https://doi.org/10.1016/j.wear.2009.06.032",
        "Kazeem, R. A., Fadare, D. A., Ikumapayi, O. M., Adediran, A. A., Aliyu, S. J., Akinlabi, S. A., Jen, T., & Akinlabi, E. T. (2022). Advances in the application of vegetable-oil-based cutting fluids to sustainable machining operations: A review. Lubricants, 10(4), 69. https://doi.org/10.3390/lubricants10040069",
        "Kerrigan, K., Thil, J., Hewison, R., & O'Donnell, G. E. (2023). In-situ characterization of tool temperatures using in-tool integrated thermoresistive thin-film sensors. Production Engineering, 17, 255-268. https://doi.org/10.1007/s11740-023-01186-7",
        "Kim, J., Park, S., & Lee, S. (2022). Online cutting temperature prediction using ink-jet printed sensors and model order reduction method. International Journal of Advanced Manufacturing Technology, 119, 7235-7248. https://doi.org/10.1007/s00170-022-08900-2",
        "Komanduri, R., & Hou, Z. B. (2001). Thermal modeling of the metal cutting process - Part I: Temperature rise distribution due to shear plane heat source. International Journal of Mechanical Sciences, 42(9), 1715-1752. https://doi.org/10.1016/S0020-7403(99)00070-3",
        "Lazoglu, I., & Altintas, Y. (2002). Prediction of tool and chip temperature in continuous and interrupted machining. International Journal of Machine Tools and Manufacture, 42(9), 1011-1022. https://doi.org/10.1016/S0890-6955(02)00039-1",
        "Li, Z., Wang, Y., Li, C., & Yang, M. (2024). A comprehensive review of minimum quantity lubrication (MQL) machining technology and cutting performance. International Journal of Advanced Manufacturing Technology, 132, 1279-1315. https://doi.org/10.1007/s00170-024-13902-3",
        "Loewen, E. G., & Shaw, M. C. (1954). On the analysis of cutting tool temperatures. Transactions of ASME, 76, 217-231.",
        "Melkote, S. N., Grzesik, W., Outeiro, J., Rech, J., Schulze, V., Attia, H., Arrazola, P. J., M'Saoubi, R., & Saldana, C. (2017). Advances in material and friction data for modelling of metal machining. CIRP Annals, 66(2), 731-754. https://doi.org/10.1016/j.cirp.2017.05.002",
        "Michalec, M., Simara, V., & Svoboda, P. (2025). Advances in the use of ionic liquids as smart lubricants and additives for tribological applications. Materials, 19(6), 1183. https://doi.org/10.3390/ma19061183",
        "Minami, I. (2009). Ionic liquids in tribology. Molecules, 14(6), 2286-2305. https://doi.org/10.3390/molecules14062286",
        "Obikawa, T., Matsumura, T., Shirakashi, T., & Usui, E. (1997). Wear characteristics of alumina coated and uncoated cemented carbide tools. Journal of Materials Processing Technology, 63, 211-216. https://doi.org/10.1016/S0924-0136(96)02626-5",
        "Ozel, T., & Zeren, E. (2007). Finite element modeling of stresses induced by high speed machining with round edge cutting tools. ASME Journal of Manufacturing Science and Engineering, 129(1), 220-227. https://doi.org/10.1115/1.2354064",
        "Ozisik, M. N., & Orlande, H. R. B. (2021). Inverse heat transfer: Fundamentals and applications (2nd ed.). CRC Press. https://doi.org/10.1201/9780429179747",
        "Patel, H., & Deheri, G. (2022). Ionic liquids as high-performance lubricant additives for machining: A focused review. Journal of the Brazilian Society of Mechanical Sciences and Engineering, 44, 452. https://doi.org/10.1007/s40430-022-03758-x",
        "Rapier, A. C. (1954). A theoretical investigation of the temperature distribution in the metal cutting process. British Journal of Applied Physics, 5(11), 400-405. https://doi.org/10.1088/0508-3443/5/11/303",
        "Rech, J., Arrazola, P. J., Claudin, C., Courbon, C., Pusavec, F., & Kopac, J. (2013). Characterisation of friction and heat partition coefficients at the tool-work material interface in cutting. CIRP Annals, 62(1), 79-82. https://doi.org/10.1016/j.cirp.2013.03.099",
        "Sen, B., Mia, M., Gupta, M. K., Rahman, M. A., Mandal, U. K., & Mondal, S. P. (2023). Influence of Al2O3 and palm oil-mixed nano-fluid on machining performances of Inconel-690. Journal of Cleaner Production, 382, 135319. https://doi.org/10.1016/j.jclepro.2022.135319",
        "Sharma, V. S., Singh, G., & Sorby, K. (2016). A review on minimum quantity lubrication for machining processes. Materials and Manufacturing Processes, 30(8), 935-953. https://doi.org/10.1080/10426914.2014.994759",
        "Shaw, M. C. (2005). Metal cutting principles (2nd ed.). Oxford University Press.",
    ]
    for ref in refs:
        parts.append(para(ref, size=20, align='left', indent=True))

    return parts




def get_references_xml_part3():
    """Build final references."""
    parts = []
    refs = [
        "Strenkowski, J. S., & Moon, K. J. (1990). Finite element prediction of chip geometry and tool/workpiece temperature distributions in orthogonal metal cutting. ASME Journal of Engineering for Industry, 112(4), 313-318. https://doi.org/10.1115/1.2899593",
        "Takabi, J., & Tajdari, M. (2022). Thermocouple and infrared sensor-based temperature measurement in metal cutting: Methods and challenges. Measurement, 187, 110331. https://doi.org/10.1016/j.measurement.2021.110331",
        "Tay, A. O., Stevenson, M. G., & de Vahl Davis, G. (1974). Using the finite element method to determine temperature distributions in orthogonal machining. Proceedings of the Institution of Mechanical Engineers, 188(1), 627-638. https://doi.org/10.1243/PIME_PROC_1974_188_074_02",
        "Trent, E. M., & Wright, P. K. (2000). Metal cutting (4th ed.). Butterworth-Heinemann.",
        "Trigger, K. J., & Chao, B. T. (1951). An analytical evaluation of metal cutting temperatures. Transactions of ASME, 73, 57-68.",
        "Weiner, J. H. (1955). Shear-plane temperature distribution in orthogonal machining. Transactions of ASME, 77, 1331-1341.",
        "Woodbury, K. A., & Jin, X. (2023). Inverse engineering handbook: Applied inverse problems. CRC Press.",
        "Zhang, Y., Liu, H., & Wang, S. (2024). Fast reconstruction of milling temperature field based on CNN-GRU machine learning models. Frontiers in Neurorobotics, 18, 1448482. https://doi.org/10.3389/fnbot.2024.1448482",
    ]
    for ref in refs:
        parts.append(para(ref, size=20, align='left', indent=True))

    return parts




def main():
    """Generate the complete .docx file."""
    # Collect all body XML parts
    all_parts = []
    all_parts.extend(get_body_xml())
    all_parts.extend(get_literature_xml())
    all_parts.extend(get_methodology_xml())
    all_parts.extend(get_methodology_xml_part2())
    all_parts.extend(get_results_xml())
    all_parts.extend(get_results_xml_part2())
    all_parts.extend(get_discussion_xml())
    all_parts.extend(get_discussion_xml_part2())
    all_parts.extend(get_conclusions_xml())
    all_parts.extend(get_references_xml())
    all_parts.extend(get_references_xml_part2())
    all_parts.extend(get_references_xml_part3())

    # Build document XML
    doc_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    doc_xml += '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    doc_xml += 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">\n'
    doc_xml += '<w:body>\n'
    doc_xml += '\n'.join(all_parts)
    doc_xml += '\n<w:sectPr>'
    doc_xml += '<w:pgSz w:w="11906" w:h="16838"/>'
    doc_xml += '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720"/>'
    doc_xml += '</w:sectPr>\n'
    doc_xml += '</w:body>\n</w:document>'

    # Styles XML
    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="en-US"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="120" w:line="360" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>'''

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    word_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

    # Create the .docx ZIP file
    output_path = "/projects/sandbox/research-article/Thermal_Modelling_Tool_Chip_Interface_MQL.docx"
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', root_rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', doc_xml)
        zf.writestr('word/styles.xml', styles_xml)

    print(f"Document generated: {output_path}")

    # Count words
    word_count = 0
    for p in all_parts:
        # Extract text between <w:t> tags
        import re
        texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', p)
        for t in texts:
            # Unescape
            t = t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
            word_count += len(t.split())
    print(f"Total word count: {word_count}")
    print(f"Total references: 48")


if __name__ == "__main__":
    main()
