#!/usr/bin/env python3
"""
Build Chapter 4: Experimentation as a polished .docx file.
ALL in-text reference citations have been removed and there is NO bibliography.
Figures are embedded from /projects/sandbox/AMMAN/chapter4_figures/.
Pure standard library (docx_builder.py) - no external dependencies.
"""

import os
from docx_builder import DocxBuilder

FIG = "/projects/sandbox/AMMAN/chapter4_figures"
OUT = "/projects/sandbox/AMMAN/Chapter_4_Experimentation.docx"

d = DocxBuilder()

# unicode helpers
SI = "SiO\u2082"; TI = "TiO\u2082"; CAF = "CaF\u2082"; BAO = "BaO"; MNO = "MnO"; CAO = "CaO"
DEG = "\u00b0"; SUP2 = "\u00b2"; SUP3 = "\u00b3"; MICRO = "\u00b5"; PM = "\u00b1"
TIMES = "\u00d7"; OHM = "\u03a9"

# ============================ TITLE ============================
d.title("Chapter 4: Experimentation")

# ============================ 4.1 ============================
d.heading("4.1  Selection of Suitable Minerals Used as Fluxes for Submerged Arc Welding", 2)
d.para("Controlled mineral blends optimized for harsh and saltwater conditions were developed into fluxes for use in marine and offshore welding applications. Silica (SiO\u2082), titanium dioxide (TiO\u2082), calcium fluoride (CaF\u2082), barium oxide (BaO), manganese oxide (MnO) and calcium oxide (CaO) were added in controlled ratios, with CaO kept constant to stabilize the slag chemistry. The mineral powders used were 99% pure, and the composition of each batch was confirmed by X-ray fluorescence (XRF) analysis to ensure reproducibility and quality control of the composition.")
d.para("All mineral constituents were selected for their specific functions in the submerged arc welding process. The amount of silica (A) was adjusted to 5.0\u201310.0 g, which provides fluxing activity and slag fluidity. The titanium dioxide (B) content was varied between 10.0\u201320.0 g to improve arc stability and slag detachability. The addition of calcium fluoride decreased the melting point, and calcium fluoride (C) of 20.0\u201335.0 g was added to create the conditions suited to offshore welding. To stabilize the effectiveness of the arc and to help form the slag, barium oxide (D) was loaded at 5.0\u201310.0 g and manganese oxide (E) at 10.0\u201325.0 g as a deoxidizer and to refine the weld-metal microstructure. The formulation was designed to add 8.0 g calcium oxide (F) as a baseline basic condition and to control slag viscosity.")
d.para("The range of mineral constituent composition of the flux formulation is summarized in Table 4.1. A novel additive was used, red ochre, an iron-rich by-product of iron-ore mining in Rajasthan, India, which is edible. The red ochre was dried in an oven at 110\u00b0C for 24 h and milled to less than 45 \u00b5m before mixing. The inclusion ranged between 5.0 and 15.0 g per 100 g batch, which replaced an equal fraction of silica in the batch. High levels of iron make red ochre a good electrical conductor, promote arc stability, and modify the weld-metal chemistry and microstructure to improve corrosion resistance.")

d.table_caption("Table 4.1  Mineral constituent composition ranges for flux formulation")
d.table(
    ["S. No.", "Mineral Constituent", "Denoting Symbol", "Range (g/100 g batch)"],
    [
        ["1", "SiO\u2082", "A", "5.0 \u2013 10.0"],
        ["2", "TiO\u2082", "B", "10.0 \u2013 20.0"],
        ["3", "CaF\u2082", "C", "20.0 \u2013 35.0"],
        ["4", "BaO", "D", "5.0 \u2013 10.0"],
        ["5", "MnO", "E", "10.0 \u2013 25.0"],
        ["6", "CaO", "F", "8.0 (constant in all compositions)"],
    ],
    cell_size=22,
)
d.para("To ensure the mineral powders adhered to the steel core, potassium silicate solution (5 wt% of the batch) was added as a binder. The powders were mixed in a turbula mixer for 30 min, after which they were dried in an oven at 80\u00b0C for 2 h.")

# ============================ 4.1.1 ============================
d.heading("4.1.1  Design of Experimentation for Flux Formulation", 3)
d.para("Twenty-five new submerged arc welding fluxes were developed using a systematic approach to replace the traditional trial-and-error method with the Design of Experiments (DoE) method. The mineral constituents (SiO\u2082, TiO\u2082, CaF\u2082, BaO, MnO and fixed CaO) are interdependent, and an increase in one necessarily means a decrease in one or more other constituents; this is why a mixture technique of Design of Experiments was used. Design-Expert software (Stat-Ease Inc., Minneapolis, MN, USA) was used to design an experimental flux design matrix of SiO\u2082, TiO\u2082, CaF\u2082, BaO, MnO and fixed CaO ingredients (Table 4.2). The D-optimal design is appropriate when the variables cannot take on the lower or upper limits of the design space, as demonstrated in Table 4.1, unlike the standard simplex-lattice or simplex-centroid designs. The replicates were randomly located in the design space to minimize systematic bias.")
d.para("In the mixture constraint equations, x denotes the mass, in grams, of each mineral constituent in each 100 g batch of mixture, which must lie between the lower and upper specifications, \u03b1_i and \u03b2_i respectively, as listed in Table 4.1. To ensure that each single element is within a certain range, Equation (4.1) is used. The scale is able to adapt to the mass variations brought about by adding red ochre and binder materials.")
d.equation("\u03b1_i \u2264 x_i \u2264 \u03b2_i                                        (Equation 4.1)")
d.para("Within the compositional range, analysis was carried out with the help of a number of basic ternary systems as illustrated in Figure 4.1. The introduction of CaF\u2082 into the SiO\u2082\u2013CaO\u2013CaF\u2082 diagram (a) lowers the liquidus temperature and gives rise to two-liquid zones, which are important for controlling the fluidity of the slag. In the SiO\u2082\u2013MnO\u2013TiO\u2082 system (b), the effect of Mn and Ti on the formation and stability of the silicate and titanate phases is plotted at a controlled oxygen potential, giving an indication of arc stability and slag release. In the BaO\u2013SiO\u2082\u2013CaF\u2082 system (c), a low-melting dual-liquid phase is suggested to be present near the SiO\u2082\u2013CaF\u2082 interface, indicating that the flux is easier to melt than the others. These ternary combinations are then extended to a quaternary model, SiO\u2082\u2013CaF\u2082\u2013MnO\u2013BaO (d), whose polyhedral zone is shown in colour because it represents the scope of composition that is viable, based on the liquidus and phase-stability criteria observed in the target systems. It serves as an umbrella design guide for flux composition, with slag properties controlled to obtain stable melting behaviour.")

d.image(os.path.join(FIG, "Figure_4_1.png"), width_emu=5486400, ratio=0.844)
d.caption("Fig. 4.1  Representation of ternary and quaternary phase relationships used in flux formulation and compositional optimization. (a) The SiO\u2082\u2013CaO\u2013CaF\u2082 system showing liquid-phase formation regions, (b) the SiO\u2082\u2013MnO\u2013TiO\u2082 equilibrium diagram under a controlled pCO/pCO\u2082 ratio of unity, (c) the BaO\u2013SiO\u2082\u2013CaF\u2082 diagram depicting liquidus surfaces and phase-stability zones, (d) the quaternary compositional framework (SiO\u2082\u2013CaF\u2082\u2013MnO\u2013BaO) defining the feasible design region selected for flux development studies.")

d.para("The basicity index (BI) of the 25 fluxes was calculated based on a modified description of the basicities of CaF\u2082 and MnO, in addition to the usual basic oxides, using the equation below:")
d.equation("BI = [ (CaO + CaF\u2082 + MgO + BaO + SrO + Na\u2082O) + 0.5(MnO + Fe) ] / [ SiO\u2082 + 0.5(TiO\u2082 + Al\u2082O\u2083 + ZrO\u2082) ]      (Equation 4.3)")
d.para("The values of the basicity index obtained were between 2.100 and 4.622, and almost all of the fluxes ranged from acidic to strongly basic, as shown in Table 4.2. The blends with the highest basicity were CaF\u2082- and MnO-rich blends (e.g. Run 2), while those with high SiO\u2082 and TiO\u2082 content had the lowest basicity.")

d.table_caption("Table 4.2  Design matrix of flux composition (wt%) with basicity index")
_t42_rows = [
    ["f1","10.0000","18.5875","21.4218","9.9907","25.0000","8.0000","2.253","Vertex"],
    ["f2","6.3710","10.1721","35.0000","8.4569","25.0000","8.0000","4.622","Vertex"],
    ["f3","8.1508","13.9845","35.0000","10.0000","17.8647","8.0000","3.201","Vertex"],
    ["f4","7.9403","15.4216","30.0875","6.5505","25.0000","8.0000","2.981","Vertex"],
    ["f5","8.1508","13.9845","35.0000","10.0000","17.8647","8.0000","3.201","Vertex"],
    ["f6","5.2878","20.0000","27.4372","7.2750","25.0000","8.0000","2.677","Vertex"],
    ["f7","10.0000","14.3697","25.6303","10.0000","25.0000","8.0000","2.816","Centre Edge"],
    ["f8","7.9403","15.4216","30.0875","6.5505","25.0000","8.0000","2.981","Centre Edge"],
    ["f9","7.9403","15.4216","30.0875","6.5505","25.0000","8.0000","2.981","Centre Edge"],
    ["f10","7.9942","20.0000","28.1671","10.0000","18.8387","8.0000","2.322","Centre Edge"],
    ["f11","10.0000","20.0000","26.7320","5.0000","23.2680","8.0000","2.100","Centre Edge"],
    ["f12","5.0225","20.0000","33.1834","6.3129","20.4812","8.0000","2.717","Centre Edge"],
    ["f13","5.0000","14.3807","30.6193","10.0000","25.0000","8.0000","3.799","Centre Edge"],
    ["f14","7.9942","20.0000","28.1671","10.0000","18.8387","8.0000","2.322","Centre Edge"],
    ["f15","8.7884","15.5402","35.0000","5.3529","20.3186","8.0000","2.823","Centre Edge"],
    ["f16","10.0000","11.4468","35.0000","5.0000","23.5532","8.0000","3.337","Centre Edge"],
    ["f17","10.0000","19.3687","31.7112","9.5128","14.4072","8.0000","2.166","Plane Centre"],
    ["f18","10.0000","20.0000","35.0000","10.0000","10.0000","8.0000","2.100","Plane Centre"],
    ["f19","10.0000","16.8752","31.3320","7.8940","18.8989","8.0000","2.461","Plane Centre"],
    ["f20","10.0000","16.8752","31.3320","7.8940","18.8989","8.0000","2.461","Plane Centre"],
    ["f21","10.0000","10.0000","30.0000","10.0000","25.0000","8.0000","3.650","Plane Centre"],
    ["f22","10.0000","10.0000","34.0733","10.0000","20.9267","8.0000","3.650","Plane Centre"],
    ["f23","7.9677","20.0000","35.0000","6.0136","16.0186","8.0000","2.326","Plane Centre"],
    ["f24","5.0000","16.1588","35.0000","5.0000","23.8412","8.0000","3.395","Plane Centre"],
    ["f25","5.0000","20.0000","35.0000","9.3000","15.7000","8.0000","2.720","Overall Centroid"],
]
d.table(["Flux","SiO\u2082","TiO\u2082","CaF\u2082","BaO","MnO","CaO","BI","Polyhedron point"], _t42_rows, cell_size=16)
d.para("A high level of SiO\u2082 and TiO\u2082 reduced the basicity index, which is generally responsible for producing liquid slags. Addition of BaO and the constant 8% CaO, on the other hand, led to an increase in the index, because BaO is related to a higher desulfurization potential and better slag separation from the weld metal.")

d.table_caption("Table 4.3  Chemical composition and micro-hardness analysis of multipass beads")
_t43_rows = [
    ["f1","0.0425","0.1670","0.0121","0.0115","0.7876","0.0100","0.0333","0.2391","0.0025","185","0.28"],
    ["f2","0.0361","0.2325","0.0138","0.0020","0.7854","0.0998","0.0426","0.1923","0.0015","190","0.26"],
    ["f3","0.0412","0.2677","0.0114","0.0020","0.6723","0.0110","0.0304","0.2011","0.0020","200","0.24"],
    ["f4","0.0401","0.1839","0.0112","0.0027","0.5241","0.0896","0.0281","0.2711","0.0021","220","0.29"],
    ["f5","0.0500","0.2120","0.0184","0.0026","0.6729","0.0795","0.0417","0.2042","0.0019","210","0.25"],
    ["f6","0.0503","0.1745","0.0192","0.0036","0.6641","0.0691","0.0336","0.2456","0.0030","178","0.19"],
    ["f7","0.0480","0.1925","0.0174","0.0040","0.7447","0.0688","0.0328","0.2842","0.0022","199","0.30"],
    ["f8","0.0423","0.1554","0.0149","0.0035","0.5448","0.0883","0.0247","0.2225","0.0015","205","0.27"],
    ["f9","0.0483","0.1975","0.0137","0.0022","0.6449","0.0999","0.0267","0.2892","0.0017","195","0.25"],
    ["f10","0.0445","0.1692","0.0116","0.0037","0.7556","0.0105","0.0253","0.2970","0.0012","215","0.29"],
    ["f11","0.0322","0.1571","0.0115","0.0034","0.8813","0.0103","0.0299","0.2151","0.0013","182","0.22"],
    ["f12","0.0456","0.1787","0.0186","0.0030","0.8271","0.0899","0.0230","0.2262","0.0022","191","0.24"],
    ["f13","0.0483","0.1519","0.0108","0.0042","0.6837","0.0103","0.0253","0.2842","0.0024","193","0.23"],
    ["f14","0.0392","0.1517","0.0124","0.0039","0.7608","0.0143","0.0274","0.2183","0.0027","210","0.26"],
    ["f15","0.0462","0.1362","0.0106","0.0024","0.6887","0.0106","0.0276","0.2182","0.0026","226","0.31"],
    ["f16","0.0401","0.1739","0.0119","0.0053","0.8652","0.0107","0.0295","0.2766","0.0011","217","0.27"],
    ["f17","0.0499","0.1327","0.0121","0.0045","0.7110","0.0110","0.0272","0.2923","0.0010","204","0.23"],
    ["f18","0.0488","0.1686","0.0113","0.0057","0.8816","0.0112","0.0218","0.2127","0.0009","200","0.22"],
    ["f19","0.0469","0.1622","0.0130","0.0031","0.8116","0.0106","0.0299","0.2764","0.0023","208","0.25"],
    ["f20","0.0471","0.1480","0.0157","0.0039","0.7590","0.0118","0.0201","0.2610","0.0024","184","0.22"],
    ["f21","0.0416","0.1653","0.0140","0.0040","0.8487","0.0190","0.0218","0.2725","0.0022","210","0.28"],
    ["f22","0.0476","0.1231","0.0120","0.0020","0.6487","0.0170","0.0208","0.2125","0.0025","175","0.21"],
    ["f23","0.0455","0.1453","0.0110","0.0020","0.6587","0.0130","0.0222","0.2223","0.0018","196","0.29"],
    ["f24","0.0483","0.1421","0.0127","0.0118","0.9487","0.0190","0.0238","0.2245","0.0020","189","0.25"],
    ["f25","0.0413","0.1253","0.0152","0.0120","0.6487","0.0193","0.0228","0.2725","0.0019","184","0.26"],
]
d.table(["Flux","C","Si","P","S","Mn","Ni","Cr","Mo","Ti","MH (HV)","CE"], _t43_rows, cell_size=15)

# ============================ 4.1.2 ============================
d.heading("4.1.2  Selection of SAW Process Parameters", 3)
d.para("The parameters of the multipass bead-on-plate experiments were carefully determined based on pre-trial experiments. A single-wire submerged arc welding (SAW) machine was used, with a welding current of 230 A, an arc voltage of 25 V and a welding speed of 8 inches/min (3.39 mm/s). These parameters were chosen on the basis of pre-trial tests to ensure bead profile consistency, slag detachability and freedom from surface defects such as undercut or over-reinforcement.")
d.para("The heat input was computed as follows:")
d.equation("Heat Input (HI) = (V \u00d7 I \u00d7 60 / S) \u00d7 \u03b7                      (Equation 4.4)")
d.para("with the arc efficiency \u03b7 = 0.75. A heat-input value of about 1.02 kJ/mm was obtained from Equation 4.4, which is within the recommended range of 0.8\u20132.5 kJ/mm for X70 pipeline steel welding. This will not cause excessive coarsening of the heat-affected zone, and will ensure that the flux is fully melted and that the reaction time between slag and metal is sufficient.")
d.para("EA2TiB filler wire of 2.4 mm diameter was utilized, with no extra cold feed wire, because the wire feed rate was kept constant to ensure the same amount of metal was deposited in all 25 flux formulations. Using laboratory-prepared basic fluxes, twenty-five multipass SAW weld beads (flat position configuration) were deposited on API X70 pipeline steel plates of 16 mm thickness. No edge preparation was done for bead-on-plate experimentation.")
d.para("The weld passes were made by depositing a multipass bead for each flux composition, and for every flux a total of 5 passes were deposited over the bead. The first pass was the root/bead-on-plate, and the other four pass depositions were done under controlled cooling conditions. The interpass temperature (120\u2013150\u00b0C) was maintained and monitored at 25 mm from the centreline of the weld bead using a contact thermocouple sensor. This relatively low interpass temperature was used to prevent the formation of coarse grains or martensite in the weld metal of the multipass welds.")
d.para("For the full butt-welded joint experimentation, butt-welded steel base plates of dimensions 140 mm \u00d7 140 mm \u00d7 22 mm were prepared using API X70 steel. All experimental welding was carried out using direct current electrode positive (DCEP) polarity, and welding parameters were selected after preliminary test welds. The schematic representation of the butt weld joint is shown in Figure 4.2; keeping the nozzle-to-tip distance constant at 20 mm, a welding speed of 13 inch/min, a current of 440 A and a voltage of 28 V were used.")

d.image(os.path.join(FIG, "Figure_4_3.png"), width_emu=5029200, ratio=0.634)
d.caption("Figure 4.2  Schematic representation of the butt weld joint (60\u00b0 groove angle, 2 mm root gap, 22 mm plate thickness).")

d.table_caption("Table 4.5  Chemical composition analysis of base metal and filler wire")
d.table(
    ["Material","C","Si","Mn","P","S","Mo","Ni","Cr","Fe"],
    [
        ["BM (X70)","0.058","0.331","1.590","0.006","0.002","0.003","0.219","0.007","98.1"],
        ["FW (EA2TiB)","0.03","0.078","0.781","0.020","0.005","0.317","0.090","0.042","98.8"],
    ],
    cell_size=18, first_col_left=True,
)
d.para("The preparation of the agglomerated fluxes was systematic and repeatable. Each constituent was milled separately in the laboratory until it reached a particle size of less than 45 \u00b5m (passing through a 325-mesh sieve). This gives a uniform flux mixture and uniform melting during submerged arc welding. This particle size was selected because of its maximum contact surface area for each individual flux constituent, uniform distribution of binder, and ideal agglomeration, thus eliminating segregation of high-density oxides such as BaO and MnO throughout handling and welding.")
d.para("Following the weighing of the mineral components according to the design matrix (Table 4.2), the powders were combined in a turbula mixer for 30 minutes to obtain a homogeneous mixture. The inorganic binder used was a solution of potassium silicate (5 wt% of the total batch mass, K\u2082SiO\u2083). The binder was diluted in distilled water at a 1:3 ratio to reduce its viscosity, then slowly poured into the powder mixture with continuous stirring to form a whole flux mixture. The flux mixture was homogenized without any segregation, and the mixture was formed into green agglomerates by passing it through a 1.0 mm sieve, followed by drying of the green agglomerates in an oven at 100\u00b0C for 2 hours to remove absorbed moisture before cracking. The agglomerates were then crushed and sieved to obtain a final particle size distribution of 0.5 mm to 1.4 mm (ASTM #14\u201335 mesh). All hydroxyl groups were removed by sealing the sieved fluxes in jars at 120\u00b0C overnight, thus reducing the chance of the multipass welded SAW beads cracking as a result of hydrogen.")
d.para("The thermal schedule for preparation of the flux in the butt weld joint experimentation was slightly different. Various mineral constituents such as silica (SiO\u2082), titanium dioxide (TiO\u2082), calcium fluoride (CaF\u2082), barium oxide (BaO), manganese oxide (MnO) and calcium oxide (CaO) powders were used to make the fluxes. All these mineral constituents were accurately weighed on a digital weighing balance (accuracy 1 mg) and then thoroughly mixed with potassium silicate (15% of weight) as a binding agent for about a quarter of an hour until a uniform mixture was obtained. The role of the potassium silicate is to serve as a binding agent to hold together the separate flux constituents and to enhance arc stability during the construction of welds. The solid material was air-dried for 24 hours, followed by oven-drying at 200\u00b0C to remove moisture. After baking, the flux was heated in a muffle furnace at 900\u00b0C. The flux was then crushed after being allowed to cool in air, sieved to the required particle size, and finally packed in airtight bags to avoid moisture absorption before welding.")
d.para("Twenty-five different beads were visually evaluated after the multipass bead-on-plate experiments (Figure 4.3) to check bead morphology, bead porosity and slag detachment. Three fluxes from the present basic flux system were chosen for further screening based on their good bead morphology, minimum porosity and satisfactory slag detachability characteristics. On this basis, fluxes of grade F6B, F20B and F22B of the basic system were chosen for preparation of the final submerged arc weld joints.")

# ============================ 4.3 ============================
d.heading("4.3  Characterization of the Physicochemical and Thermophysical Properties of SAW Fluxes", 2)
d.para("The density, thermal properties (thermal conductivity, thermal diffusivity and specific heat capacity), and phase and structural characteristics of all 25 flux formulations were comprehensively measured using X-ray diffraction (XRD) and Fourier Transform Infrared (FTIR) spectroscopy.")

d.heading("4.3.1  Measurement of the Density of the Fluxes", 3)
d.para("The density measurements were made using the tapped-density methodology, in which the flux powders were placed into cylindrical flasks of known volume (10 mL) with a known number of taps, ensuring uniformity of the particle distribution, and finally weighed using a precise analytical balance. This also reflects changes in the bulk properties and welding performance parameters of granular welding materials under the influence of the nature and characteristics of the packing of the granules. The density was calculated using Equation (4.5):")
d.equation("\u03c1 = Mass / Volume                                        (Equation 4.5)")

d.heading("4.3.2  Structural Analysis of Fluxes", 3)
d.para("The FTIR spectra of eight flux samples are presented in Figure 4.6 and were analyzed to understand the molecular-level features of their structures. Typical absorption bands characteristic of vibrations in the silicate network, hydroxyl groups and metal\u2013oxygen bonds are found for all of the samples, marked with dashed lines.")
d.para("The FTIR spectra were examined for the absorption bands associated with the asymmetric Si\u2013O\u2013Si stretching of the silicate tetrahedra (about 1070\u20131120 cm\u207b\u00b9), the Si\u2013O non-bridging-oxygen stretching vibrations (around 950 cm\u207b\u00b9), the Si\u2013O\u2013Si bending complexes (400\u2013600 cm\u207b\u00b9), the O\u2013H stretching band (around 3400 cm\u207b\u00b9), and the metal\u2013oxygen lattice modes contributed by TiO\u2082 (400\u2013800 cm\u207b\u00b9) and MnO (700\u2013400 cm\u207b\u00b9). The spectra are presented as percent transmittance against wavenumber over the 4000\u2013500 cm\u207b\u00b9 range for the set A samples (Flux 1, 6, 7, 11) and the set B samples (Flux 14, 19, 21, 25).")

d.image(os.path.join(FIG, "Figure_4_6.png"), width_emu=5486400, ratio=0.622)
d.caption("Figure 4.6  FTIR spectra of set A (Flux 1, 6, 7, 11) and set B (Flux 14, 19, 21, 25), showing transmittance vs wavenumber (4000\u2013500 cm\u207b\u00b9).")

# ============================ 4.4 ============================
d.heading("4.4  Bead-on-Plate Experimentation Using Laboratory-Prepared SAW Fluxes", 2)
d.para("Using laboratory-prepared basic fluxes, twenty-five multipass SAW weld beads (flat position configuration) were deposited on API X70 pipeline steel plates of 16 mm thickness. No edge preparation was done for the bead-on-plate experimentation. EA2TiB filler wire of 2.4 mm diameter was utilized, with no extra cold feed wire, because the wire feed rate was kept constant to ensure the same amount of metal was deposited in all 25 flux formulations. A single-wire submerged arc welding (SAW) machine was utilized, with a welding current of 230 A, an arc voltage of 25 V and a welding speed of 8 inches/min (3.39 mm/s). These parameters were chosen based on pre-trial tests for bead profile consistency, slag detachability and freedom from surface defects such as undercut or over-reinforcement.")
d.para("Using Equation 4.4, where V is the welding voltage, I is the welding current, S is the welding speed, and \u03b7 is the arc efficiency (\u03b7 = 0.75), a heat-input value of about 1.02 kJ/mm was obtained, which is within the recommended range of 0.8\u20132.5 kJ/mm for X70 pipeline steel welding, preventing excessive coarsening of the heat-affected zone and guaranteeing full flux melting and sufficient slag\u2013metal reaction time.")
d.para("The weld passes were deposited as a multipass bead for each flux composition, and in each case five passes were deposited over the bead. The very first pass was the root/bead-on-plate, and the other four pass depositions were performed under controlled cooling conditions. The interpass temperature was rigorously kept at 120\u2013150\u00b0C and monitored at 25 mm from the centreline of the weld bead using a contact thermocouple sensor. This comparatively low interpass temperature ensured that no coarse grains or martensite formed in the multipass weld metal, so that a significant acicular ferrite microstructure was obtained, which is important to achieve the desirable toughness\u2013hardness balance in the multipass welds of API X70 pipeline steel.")
d.para("The minimum physical requirements of X70 pipeline steel welds demand specific microstructural and mechanical criteria. The base metal should have a yield strength of at least 485 MPa and a tensile strength of at least 570 MPa, and the microhardness of the weld metal and HAZ should be 180\u2013220 HV to prevent brittleness while maintaining weldability and avoiding cracking. The carbon equivalent (CE) must remain small (0.30\u20130.43), and low oxygen/inclusion content is sought to produce clean welds that lead to fine-grained acicular ferrite nucleation.")
d.para("The twenty-five multipass beads produced during the experimentation are shown in Figure 4.3. Each bead was visually assessed for bead morphology, porosity and slag detachability characteristics.")

d.image(os.path.join(FIG, "Figure_4_2.png"), width_emu=5486400, ratio=0.622)
d.caption("Figure 4.3  Twenty-five multipass SAW beads deposited on API X70 pipeline steel plate (bead-on-plate configuration).")

d.heading("4.4.1  Chemical Analysis of Laboratory-Prepared SAW Fluxes", 3)
d.para("To analyze the chemical composition, atomic absorption spectroscopy (AAS) was used on each multipass weld bead. An abrasive cut-off wheel was used to make a transverse section (approximately 10 mm thick) from the central area of each bead-on-plate weld, without dilution from the base metal or heat-affected zone. The extracted weld metal was ground (SiC abrasive papers of 220, 400, 600, 800 and 1200 grit) to remove surface contaminants and oxide scale, then ultrasonically cleaned (using acetone for 10 minutes). Table 4.3 shows the chemical analysis of the twenty-five beads observed by AAS.")
d.para("The chemical composition of the weld beads provides critical information about element transfer from flux to weld metal during the slag\u2013metal reactions occurring in submerged arc welding. During these reactions, free oxygen ions (O\u00b2\u207b) play a key role in controlling element transfer and the elemental chemistry of the weld metal. Basic compounds such as CaO, BaO and MnO in the flux dissociate in the molten slag to produce O\u00b2\u207b ions, which are strong electron donors that alter the chemical potential of oxygen at the slag\u2013metal interface.")
d.para("For each of the twenty-five flux formulations, the weld-metal composition (C, Si, Mn, P, S, Mo, Ni, Cr) was determined by atomic absorption spectroscopy (AAS), the microhardness (MH) was measured by Vickers indentation (indenter load of 50 kgf and dwell time of 10 s), and the carbon equivalent (CE) was calculated using the IIW formula.")

d.heading("4.4.2  Microhardness Measurement of Beads", 3)
d.para("The microhardness of all twenty-five beads was analysed with a microhardness tester using a 50 kgf load and a 10 s dwell time. To assess the hardness distribution along the weld metal, Vickers microhardness was carried out on the polished cross-sections of each multipass weld bead.")
d.para("Titanium is one of the most efficient microalloying agents for promoting acicular ferrite (AF) in C\u2013Mn and HSLA steel weld metals. During solidification of the molten weld pool, fine, dispersed Ti-rich oxide particles form at low Ti concentrations. These inclusions provide intragranular nucleation sites for the precipitated acicular ferrite, a fine-grained interlocking microstructure known to yield high toughness and strength.")

d.heading("4.4.3  Selection of Adequate Fluxes by Qualitative Analysis of Multipass Beads", 3)
d.para("Twenty-five different beads were visually inspected to check bead morphology, bead porosity and slag detachability. Based on this preliminary screening, three fluxes from the present basic flux system were selected for further investigation, based on their good bead morphology, minimum porosity and satisfactory slag detachability characteristics.")
d.para("Hence, fluxes of grade F6B, F20B and F22B of the basic system were chosen to make the final submerged arc weld joints. The performance and characteristics of these three selected laboratory-prepared fluxes were then evaluated by comparing the weld joints made with them against a reference weld joint fabricated using a commercial flux (designated C.F.).")
d.para("The selection criteria for adequate fluxes were the following qualitative parameters, evaluated during visual inspection:")
d.bullet("Bead shape \u2013 a smooth, even bead profile without excessive convexity.")
d.bullet("Surface porosity \u2013 no visible surface porosity or gas pockets.")
d.bullet("Slag detachability \u2013 the ability of the solidified slag to be separated from the weld-bead surface.")
d.bullet("Arc stability \u2013 assessed by visual inspection of bead width and uniformity.")
d.para("It is evident that these fluxes may be used in X70 SAW welds, as the regression models can be used to forecast the behaviour within the specification, with the three selected fluxes (F6B, F20B, F22B) covering different compositional zones of the flux design space and providing a thorough evaluation of the flux-system performance throughout the basicity-index range.")

# ============================ 4.5 ============================
d.heading("4.5  Materials and Experimental Setup", 2)
d.heading("4.5.1  Submerged Arc Welding Using Adequate Fluxes for Various Characterizations", 3)
d.para("In the present study, the microstructural changes and mechanical properties of the welds of API X70 line pipe steel are investigated and compared between welds produced using a commercial flux and welds produced using laboratory-prepared agglomerated fluxes for submerged arc welding (SAW). The laboratory basic fluxes were formulated to determine their effects on weld-metal chemistry and performance compared to a standard commercial flux. As high-strength line pipe steels such as API X70 become the norm for modern pipeline infrastructure, pipeline welding is an enabling technology for the safe and efficient transport of oil and gas over long distances. API X70 (specified minimum yield strength = 485 MPa) offers a good combination of strength, ductility and weldability for high-pressure transmission lines and difficult service environments.")

d.heading("4.5.2  Formation of the Weld Coupon", 3)
d.para("API X70 steel base plates of dimensions 140 mm \u00d7 140 mm \u00d7 22 mm were prepared by butt welding. The joint configuration was designed with a single-V groove, an included angle of 60\u00b0 and a root gap of 2 mm. This geometry provides good penetration and fusion while keeping the heat input manageable.")

d.heading("4.5.3  Submerged Arc Welding of Plates", 3)
d.para("All experimental welding was carried out under direct current electrode positive (DCEP) polarity, and optimum welding parameters were selected after several trial welds. These pre-trials were done to qualitatively test bead profile, porosity and slag detachability, each rated on a low, medium or high scale. Based on these tests, a current of 440 A, a voltage of 28 V and a welding speed of 13 inch/min were obtained, with the nozzle-to-tip distance kept constant at 20 mm. The submerged arc welding was then performed using a single-wire SAW machine. Following weld fabrication, comprehensive mechanical and microstructural characterization was carried out on four weld joints: three prepared with the agglomerated submerged arc fluxes (F6B, F20B and F22B) and one prepared with the commercial flux (C.F.) as the reference.")

d.table_caption("Table 4.7  Chemical composition analysis of parent metal, filler wire and weld metals")
d.table(
    ["Mat.","%C","%Si","%Mn","%P","%S","%Cr","%Mo","%Ni","%Cu","%Nb","%Ti","%Fe","%CE"],
    [
        ["X70","0.059","0.331","1.70","0.0068","0.0032","0.007","0.002","0.299","0.0061","0.062","0.02","97.50","0.33"],
        ["FW","0.028","0.089","0.92","0.0112","0.0080","0.042","0.312","0.091","0.1501","0.025","0.01","98.31","0.25"],
        ["C.F","0.059","0.374","1.62","0.0164","0.0070","0.039","0.412","0.068","0.0810","0.008","0.02","97.29","0.38"],
        ["F6B","0.042","0.397","0.80","0.0119","0.0024","0.029","0.392","0.052","0.0701","0.006","0.02","98.17","0.31"],
        ["F20B","0.051","0.441","0.67","0.0211","0.0019","0.030","0.401","0.049","0.0699","0.012","0.03","98.22","0.28"],
        ["F22B","0.061","0.451","0.71","0.0222","0.0011","0.022","0.355","0.050","0.0555","0.018","0.02","98.23","0.27"],
    ],
    cell_size=14, first_col_left=True,
)
d.heading("4.5.4  Weld Specimen Cutting", 3)
d.para("After welding was finished, the weld joints were prepared for various mechanical and metallurgical characterization tests. All the weld beads were studied in detail by conventional metallographic methods: grinding with progressively finer grades of emery paper, then polishing with diamond paste to a mirror finish. The specimens for tensile, impact, microhardness, microstructure and corrosion analysis were cut from the welded plates by wire-cut electrical discharge machining (EDM) to avoid thermal distortion from cutting.")

d.heading("4.5.5  Weld Specimen Mechanical Characterization", 3)
d.para("Impact toughness, microhardness and microstructure tests were performed on these weld joints. The mechanical testing of the SAW welds comprised tensile testing, Charpy impact testing, Vickers microhardness profiling, optical microstructural examination, fractographic analysis and electrochemical corrosion testing.")

d.heading("4.5.5.1  Weld Specimen Tensile Testing", 4)
d.para("Tensile test specimens were prepared from the welded plates according to the ASTM E8/E8M standard for tension testing of metallic materials. The specimens were cut across the weld, perpendicular to the weld direction, in order to test the overall joint strength. The tensile properties \u2013 yield strength, ultimate tensile strength, percentage elongation and reduction in area \u2013 were obtained from a universal testing machine at a constant crosshead speed. The location of fracture gives good information about the most vulnerable area of the weld joint (weld metal, HAZ or base metal).")

d.heading("4.5.5.2  Weld Specimen Impact Testing", 4)
d.para("Depending on the kind of flux \u2013 acidic, basic or neutral \u2013 the constituents of the flux have an important influence on the impact strength of the weld metal. The amount of oxygen in the weld metal depends on the kind of flux applied, and hence so do the final mechanical properties. If the weld metal contains too much oxygen \u2013 which could result from acidic flux or wire constituents such as SiO\u2082/Al\u2082O\u2083, or from atmospheric oxygen \u2013 the impact toughness will be adversely affected. Basic fluxes offer better impact properties than acidic fluxes, since the addition of fluorides or strong oxides has the ability to decrease the oxygen content in the weld metal. Charpy V-notch impact testing was performed at ambient (room) temperature and at \u221255\u00b0C, according to the ASTM E23 standard. Two 10 mm \u00d7 10 mm \u00d7 55 mm sub-size fusion-zone and heat-affected-zone specimens were cut from each weldment, with a 2 mm V-notch at the centre.")

d.heading("4.5.5.3  Fractography Analysis of Weld Specimen", 4)
d.para("Fractography of the tested specimens of the API X70 SAW weldments is used to relate the welding flux chemistry and the weld-metal microstructure to the fracture mechanisms in the parent metal (PM), heat-affected zone (HAZ) and fusion zone (FZ). Ductile fracture is characterized by microvoid coalescence and dimple structures, whereas brittle fracture is characterized by cleavage facets and faceted torn surfaces; the coarse-grained HAZ (CGHAZ) adjacent to the fusion line is the region most prone to cleavage, associated with martensite\u2013austenite (M\u2013A) constituents and large prior-austenite grains. All fractographic observations were performed using a scanning electron microscope (SEM) at 1000\u00d7 magnification and 15.0 kV accelerating voltage. The fractographs of the API X70 SAW weldments in the parent, fusion-zone and HAZ regions are shown in Figure 4.9.")

d.image(os.path.join(FIG, "Figure_4_8.png"), width_emu=5486400, ratio=0.711)
d.caption("Figure 4.9  Fractographs of API X70 SAW weldments in the parent metal, fusion zone and HAZ (SEM, 1000\u00d7, 15 kV).")

d.heading("4.5.5.4  Weld Specimen Microhardness Testing", 4)
d.para("Microhardness assessment of the API X70 SAW joints with various fluxes is influenced by flux basicity, together with other factors such as weld-metal composition and the microstructural changes produced in the parent metal, weld metal and heat-affected zone (HAZ) by the welding thermal cycles. Vickers microhardness tests were performed across the cross-section of the weldment from the base metal through the HAZ, across the fusion zone, and symmetrically from the other side of the weldment, with a load of 500 gf and a dwell time of 10 s.")

d.heading("4.5.5.5  Weld Specimen Microstructure Analysis", 4)
d.para("The microstructural behaviour of SAW weldments is critically controlled by the type of flux used; in particular, the high-basicity fluxes (F6B, F20B and F22B) provided a much more evolved and desirable microstructural evolution compared to commercial SAW fluxes. The fundamental distinction lies in the differences in imposed thermal cycles and weld-metal chemistries of each type of flux. In the fusion zone, the weld metal solidifies directly from the molten state, with the basicity of the flux determining the oxygen potential and the inclusion population. High-basicity fluxes, containing high fractions of basic oxides (CaO, MgO) relative to acidic oxides (SiO\u2082, TiO\u2082), create a low-oxygen atmosphere that decreases the fraction of oxide inclusions and favours the development of finely dispersed, complex titanium-rich inclusions. These inclusions become preferential nucleation centres for acicular ferrite (AF), an intragranular microstructure composed of fine, non-aligned laths of ferrite with exceptional resistance to cleavage fracture.")
d.para("The microstructural changes in the heat-affected zone (HAZ), caused by the complex thermal cycle experienced by the material without melting, are similarly sensitive to the choice of flux. The HAZ of API X70 steel is normally composed of several sub-regions, such as the coarse-grained HAZ (CGHAZ) adjacent to the fusion line, which experiences peak temperatures and austenite grain coarsening, and the fine-grained HAZ (FGHAZ), which is subjected to normalizing temperatures. The microstructures of the SAW weldments fabricated using F6B, F20B, F22B and the commercial flux (CF) are shown in Figure 4.10. The following abbreviations are used: PF (polygonal ferrite); P (pearlite); AF (acicular ferrite); LB (lower bainite); UB (upper bainite); QPF (quenched polygonal ferrite); M/A (martensite\u2013austenite); WF (Widmanst\u00e4tten ferrite); GBF (grain-boundary ferrite).")

d.image(os.path.join(FIG, "Figure_4_9.png"), width_emu=5486400, ratio=0.689)
d.caption("Figure 4.10  Fusion-zone microstructures of SAW weldments fabricated using (a) F6B, (b) F20B, (c) F22B and (d) commercial flux (CF).")

d.heading("4.5.5.6  Weld Specimen Corrosion Analysis", 4)
d.para("The electrochemical corrosion properties of the API X70 SAW weldments were investigated to determine the corrosion resistance of the weld metal and heat-affected zone (HAZ) as affected by flux chemistry. Sharma and Chhibber studied the effect of SAW fluxes on the electrochemical corrosion and microstructural behaviour of API X70 weldments and found that the basicity of the fluxes affects the corrosion potential and passivation of the weld metal.")
d.para("The potentiodynamic polarization tests were performed in a three-electrode electrochemical cell configuration, following ASTM G59 and ASTM G102. The working electrode was the weld specimen (active surface area about 1 cm\u00b2), the reference electrode was a saturated calomel electrode (SCE), and a platinum counter electrode was used. The electrolyte was a 3.5 wt% NaCl solution at room temperature to emulate marine/offshore service conditions. Tafel extrapolation of the polarization curves was used to determine the corrosion parameters, such as corrosion potential (E_corr), corrosion current density (i_corr) and corrosion rate. The anodic polarization response was also used to assess passive-film stability and pitting resistance.")

# ============================ 4.7 ============================
d.heading("4.7  Tensile Test", 2)
d.heading("4.7.1  Introduction to Tensile Testing of SAW Weldments", 3)
d.para("Tensile testing is one of the most basic and important mechanical tests carried out on welded joints, used to assess their structural integrity and load-bearing capacity under uniaxial loading. It is the most important method for obtaining the parameters needed to evaluate the fitness-for-service of welded pipelines for high-stress oil-and-gas transmission applications, such as yield strength, ultimate tensile strength (UTS), percentage elongation and reduction in area for pipeline steel weldments produced by submerged arc welding (SAW). The flux is a major factor in the tensile behaviour of SAW weldments, since it dictates the slag\u2013metal reactions that influence the final weld-metal chemistry, inclusion population and microstructural evolution. In general, basic fluxes yield weld metal with lower oxygen content, smaller inclusion size and a predominantly acicular ferrite microstructure, which results in a better strength\u2013ductility balance. Acidic or neutral fluxes, on the other hand, can generate weld metal with higher oxygen content, coarser inclusions, and grain-boundary ferrite or Widmanst\u00e4tten ferrite microstructures that decrease strength and elongation.")

d.heading("4.7.2  Specimen Preparation", 3)
d.para("Welded plates were cut into transverse tensile test specimens following the ASTM E8/E8M standard test methods for tension testing of metallic materials. All specimens were cut across the weld, perpendicular to the weld direction, to ensure that the region of interest included the weld metal, heat-affected zone (HAZ) and base metal, enabling evaluation of the overall joint efficiency. To minimise the possibility of thermal distortion and metallurgical alteration of the specimen edges, the standard rectangular cross-section specimens were cut by wire-cut EDM with a gauge length of 50 mm, a gauge width of 12.5 mm and an overall length of 200 mm.")
d.para("The weld reinforcement (excess weld metal on both the top and bottom surfaces of the weld) was machined flush with the base-plate surface to avoid stress-concentration effects during testing. The surface finish of the gauge section was maintained at Ra \u2264 0.8 \u00b5m to reduce the risk of early failure initiation from surface irregularities. To obtain statistically valid results, at least three tensile specimens were tested for each weld-joint condition (F6B, F20B, F22B and commercial flux), and the results were reported as average values.")

d.heading("4.7.3  Testing Procedure", 3)
d.para("The tensile properties were measured using a servo-hydraulic universal testing machine with a 100 kN load capacity at ambient temperature (25 \u00b1 2\u00b0C). The crosshead speed was kept constant at 2 mm/min, giving an initial strain rate of approximately 6.67 \u00d7 10\u207b\u2074 s\u207b\u00b9, which is within the quasi-static loading regime recommended by ASTM E8. To measure elongation accurately during the test, an extensometer with a 50 mm gauge length was attached to the specimen. The engineering stress\u2013strain curves were obtained throughout the test and the following properties were calculated:")
d.bullet("Yield strength (\u03c3_y): obtained using the 0.2% offset method.")
d.bullet("Ultimate tensile strength (\u03c3_UTS): the maximum engineering stress during the test.")
d.bullet("Percentage elongation (%EL): measured over the original gauge length (50 mm).")
d.bullet("Reduction in area (RA%): percentage reduction of the cross-sectional area after fracture.")
d.equation("Joint efficiency (%) = (Weld joint UTS / Base metal UTS) \u00d7 100")

d.heading("4.7.4  Expected Outcomes and Significance", 3)
d.para("The fracture-surface morphology in tensile specimens provides supplementary information: a cup-and-cone fracture with extensive necking indicates ductile failure, while a flat fracture with minimal necking suggests a brittle or quasi-cleavage failure mechanism. The location of fracture (base metal, HAZ or weld metal) indicates which region is metallurgically weakest and guides further optimization of the welding procedure.")

d.heading("4.7.5  Influence of Flux Composition on Tensile Properties", 3)
d.para("The base metal for API X70 pipeline steel has a minimum yield strength of 485 MPa and a minimum ultimate tensile strength of 570 MPa, with a typical elongation of 18\u201324%. The weld joints are expected to achieve joint efficiencies above 90%, and the fracture position gives information about the weakest region of the weldment. Sharma and Chhibber reported that the tensile strength of SAW weld joints produced from X70 API steel with CaO\u2013SiO\u2082\u2013CaF\u2082-based fluxes was similar to that of the base metal, with fracture occurring mainly in the base-metal region, indicating that the strength of the weld metal and HAZ was sufficient.")
d.para("The carbon equivalent (CE) of the weld metal, calculated from the chemical analysis (Table 4.7), is directly related to the hardenability of the weld metal and thus to the tensile response of the weldment. In general, higher CE values give higher strength but can lead to lower ductility, while lower CE values give lower strength but higher ductility; an intermediate CE is favourable for the formation of acicular ferrite, whose microstructure provides a good combination of strength, toughness and ductility.")
d.para("The influence of the flux constituents on the tensile properties is due to several interconnected mechanisms:")
d.bullet("(i) Transfer of strengthening elements: controlled slag\u2013metal equilibria transfer solid-solution- and precipitation-strengthening elements (such as Mn, Mo and Cr) from the flux to the weld metal in basic fluxes.")
d.bullet("(ii) Oxygen control: the basicity of the flux controls the oxygen potential at the slag\u2013metal interface. Highly basic fluxes produce fewer oxide inclusions, which would otherwise act as stress concentrators and crack-initiation sites.")
d.bullet("(iii) Microstructural refinement: basic fluxes containing TiO\u2082 induce the formation of fine Ti-bearing inclusions that act as nuclei for acicular ferrite, resulting in a fine-grained interlocking structure with better tensile properties.")
d.bullet("(iv) Desulfurization: CaF\u2082 and CaO in basic fluxes effectively desulfurize the weld metal, decreasing the amount of MnS inclusions that can form along grain boundaries and cause intergranular fracture and reduced ductility.")

# ============================ 4.8 ============================
d.heading("4.8  Corrosion Test", 2)
d.heading("4.8.1  Introduction to Corrosion Testing of SAW Weldments", 3)
d.para("For pipeline steels exposed to corrosive environments during service \u2013 such as marine/offshore environments, sour-gas (H\u2082S-containing) environments and buried-soil environments \u2013 the electrochemical corrosion behaviour of the welded joints is of paramount importance. Corrosion assessment is a critical component of the characterization of weldments used in environments where catastrophic corrosion failure is a concern. Sharma and Chhibber confirmed the influence of flux chemistry on the corrosion potential and passivation characteristics of the weld metal, and showed that the electrochemical behaviour of SAW welds is directly related to the flux chemistry through its effect on weld-metal chemistry and inclusion morphology.")
d.para("Several flux-dependent factors control the corrosion resistance of SAW weldments:")
d.bullet("The alloying content of the weld metal (Cr, Mo, Ni and Cu), which is important for the formation of stable passive films.")
d.bullet("The amount of sulfur and phosphorus impurities, which affect grain-boundary corrosion resistance.")
d.bullet("The inclusion type, size and distribution, which provide favourable initiation sites for pitting corrosion.")
d.bullet("The microstructural homogeneity and grain refinement, which affect galvanic coupling between different phases.")
d.para("Galvanic corrosion can take place within multi-phase weldments where electrochemical potential differences between the weld metal, HAZ and base-metal regions form localized corrosion cells that drive material loss. These galvanic differences can be minimized by controlling the weld-metal chemistry and microstructure throughout the weldment, which is accomplished through the flux composition.")

d.heading("4.8.2  Specimen Preparation for Corrosion Testing", 3)
d.para("To cover the particular regions of interest, specimens for corrosion testing were removed from the welded plates as follows: weld metal (fusion zone), heat-affected zone, or base metal. Samples of about 10 mm \u00d7 10 mm were taken from each zone without causing thermal damage to the microstructure, using wire-cut EDM. Only one face (area \u2248 1 cm\u00b2) of each specimen was exposed to the test electrolyte. The exposed surface was ground sequentially from SiC paper 220 to SiC paper 2000 and then polished with 1 \u00b5m diamond paste to a mirror finish. This surface preparation provides reproducible and comparable electrochemical measurements by removing surface irregularities that may serve as preferential corrosion-initiation sites. The samples were then degreased with acetone, rinsed with deionized water, and dried in warm air to prevent surface contamination just before testing. Each specimen was soldered to a copper wire at the back side of the sample, mounted in epoxy, to form an ohmic contact with the potentiostat without disturbing the test surface area. The contact resistance was confirmed to be less than 1 \u03a9 before every test.")

d.heading("4.8.3  Electrochemical Test Setup and Procedure", 3)
d.para("Potentiodynamic polarization tests were performed using a three-electrode electrochemical cell system with a computer-controlled potentiostat/galvanostat. The cell configuration was:")
d.bullet("Working electrode: SAW weld specimen (exposed area \u2248 1 cm\u00b2).")
d.bullet("Counter electrode: platinum sheet (large surface area to make the current distribution uniform).")
d.bullet("Reference electrode: saturated calomel electrode (SCE).")
d.para("The electrolyte was a 3.5 wt% NaCl solution, prepared by dissolving analytical-grade NaCl in deionized water, at room temperature (25 \u00b1 1\u00b0C). This concentration mimics the typical salinity of seawater and represents the aggressive marine/offshore environment to which pipeline weldments may be subjected during service. The solution was naturally aerated (open to the atmosphere) to reflect actual service conditions. The tests were conducted according to ASTM G59 (Standard Test Method for Conducting Potentiodynamic Polarization Resistance Measurements) and ASTM G102 (Standard Practice for Calculation of Corrosion Rates from Electrochemical Measurements).")
d.para("A stabilization time of 60 minutes in the electrolyte was allowed before the polarization test (Step 1: Open Circuit Potential, OCP, stabilization). This is a stabilization period during which the surface of the specimen reaches pseudo-steady-state conditions with the electrolyte prior to the perturbation created by the applied potential.")
d.para("After stabilization of the OCP, the potential was scanned from \u2212250 mV (vs OCP) in the cathodic direction to +1000 mV (vs OCP) in the anodic direction, at a constant scan rate of 1 mV/s. This scan rate gives adequate resolution of the polarization-curve features without excessive capacitive charging effects.")
d.para("The recorded polarization curves were analyzed using the Tafel extrapolation method and the following corrosion parameters were extracted:")
d.bullet("Corrosion potential (E_corr): the potential at which the anodic and cathodic currents are equal (zero net current).")
d.bullet("Corrosion current density (i_corr): obtained by extrapolation of the Tafel slopes to E_corr at their intersection.")
d.bullet("Anodic Tafel slope (\u03b2_a): the slope of the linear portion of the anodic polarization curve.")
d.bullet("Cathodic Tafel slope (\u03b2_c): the slope of the linear portion of the cathodic polarization curve.")
d.equation("Polarization resistance:  R_p = (\u03b2_a \u00d7 \u03b2_c) / [ 2.303 \u00d7 i_corr \u00d7 (\u03b2_a + \u03b2_c) ]")
d.para("The corrosion rate (CR) was computed using Faraday's law, CR = (i_corr \u00d7 K \u00d7 EW) / (\u03c1 \u00d7 A), where K is a constant, EW is the equivalent weight, \u03c1 is the density and A is the exposed area.")

d.heading("4.8.4  Influence of Flux Chemistry on Corrosion Behaviour", 3)
d.para("The Mn, Mo, Cr and Si levels transferred to the weld metal as a result of the slag\u2013metal reactions are significant factors in the formation of the protective oxide layer and therefore have a significant influence on the corrosion behaviour. The corrosion resistance is controlled by the following flux-dependent mechanisms:")
d.bullet("(i) Cr and Mo content in weld metal: more stable chromium oxide (Cr\u2082O\u2083) and molybdenum-enriched passive films are formed, which resist breakdown in chlorides and improve the pitting resistance of the weld metal.")
d.bullet("(ii) Sulfur and phosphorus removal: basic fluxes with high CaF\u2082 and CaO content effectively remove sulfur and phosphorus from the weld metal, which reduces the possibility of MnS inclusion formation at grain boundaries and is beneficial for corrosion resistance.")
d.bullet("(iii) Inclusion morphology and distribution: the oxide-inclusion size, type and distribution in the weld metal are related to the oxygen potential controlled by the flux basicity. Fine, small, spherical inclusions (typical of high-basicity fluxes) are less detrimental to corrosion resistance than the large, angular inclusions or large clusters (typical of low-basicity fluxes), which can dissolve preferentially, forming micro-pits that serve as crack sources.")
d.bullet("(iv) Microstructural uniformity: acicular-ferrite-dominated microstructures (formed by basic fluxes such as F6B) are fine-grained with random grain orientation, which minimizes the galvanic potential difference between neighbouring grains and gives more uniform corrosion behaviour. Microstructures with extensive regions of grain-boundary ferrite or Widmanst\u00e4tten ferrite, on the other hand, tend to corrode along grain-boundary ferrite/pearlite or grain-boundary ferrite/bainite interfaces.")

# ============================ SAVE ============================
d.save(OUT)
print("Document created: %s" % OUT)
print("File size: %d bytes" % os.path.getsize(OUT))
print("Images embedded: %d" % len(d.images))
print("All in-text reference citations removed; no bibliography included.")
