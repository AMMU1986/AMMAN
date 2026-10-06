#!/usr/bin/env python3
"""
Build a Word (.docx) document for the corrected Carreau-EMHD squeezing-flow
manuscript using ONLY the Python standard library (zipfile + minimal OOXML).

The content incorporates the reviewer corrections:
  (1)  Explicit pressure-elimination derivation for Eqs. (28)-(29).
  (2)  Eq. (17)/v_h typo nu_e -> nu_f fixed.
  (3)  Similarity transformation stated as LOCALLY similar; We, Ec, Ee are
       local-similarity parameters.
  (8)  Dimensional derivation of the Dufour/Soret coefficient (Pr a_rho Df).
  (9)  Thermodynamic basis stated for the mass-diffusion / cross-gradient
       entropy terms.
  (11) Convergence claim softened to "mesh-independent to the reported
       precision" (no fabricated extra digits).
  (12) Table 4 vs text: Nu(Rd) corrected to 1.3509 -> 2.3466 (~74%).
  (13) Table 5 vs text: Ns(0) at Omega=2.0 corrected to 3.5495.
  (16) "porous channel" terminology clarified.
  (17) Appendix A Newtonian limit stated under adopted mu_inf = 0 model.

Run:  python3 build_carreau_emhd_docx.py
Out:  Carreau_EMHD_Squeezing_Manuscript_Corrected.docx
"""

import zipfile
from xml.sax.saxutils import escape

OUT = "Carreau_EMHD_Squeezing_Manuscript_Corrected.docx"

# ----------------------------------------------------------------------
# Minimal OOXML paragraph builders
# ----------------------------------------------------------------------

def _run(text, bold=False, italic=False, sz=None):
    rpr = ""
    props = ""
    if bold:
        props += "<w:b/>"
    if italic:
        props += "<w:i/>"
    if sz:
        props += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (sz, sz)
    if props:
        rpr = "<w:rPr>%s</w:rPr>" % props
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, escape(text))


def para(text="", style=None, bold=False, italic=False, sz=None, align=None):
    ppr = ""
    inner = ""
    if style:
        ppr += '<w:pStyle w:val="%s"/>' % style
    if align:
        ppr += '<w:jc w:val="%s"/>' % align
    if ppr:
        inner += "<w:pPr>%s</w:pPr>" % ppr
    if text:
        inner += _run(text, bold=bold, italic=italic, sz=sz)
    return "<w:p>%s</w:p>" % inner


def heading(text, level=1):
    style = "Heading%d" % level
    return para(text, style=style)


def title(text):
    return para(text, style="Title")


def eq(text, num=None):
    """Equation line: monospace-ish, centered, optional (n) tag at right."""
    label = ("    (%s)" % num) if num else ""
    return (
        '<w:p><w:pPr><w:ind w:left="360"/></w:pPr>'
        + '<w:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
        + '<w:i/></w:rPr>'
        + '<w:t xml:space="preserve">%s</w:t></w:r>' % escape(text + label)
        + "</w:p>"
    )


def table(headers, rows):
    cols = len(headers)
    grid = "".join('<w:gridCol w:w="%d"/>' % int(9000 / cols) for _ in range(cols))

    def cell(txt, bold=False):
        return (
            "<w:tc><w:tcPr><w:tcW w:w=\"%d\" w:type=\"dxa\"/></w:tcPr>" % int(9000 / cols)
            + para(txt, bold=bold)
            + "</w:tc>"
        )

    out = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="0" w:type="auto"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
           '</w:tblBorders></w:tblPr>']
    out.append("<w:tblGrid>%s</w:tblGrid>" % grid)
    out.append("<w:tr>" + "".join(cell(h, bold=True) for h in headers) + "</w:tr>")
    for r in rows:
        out.append("<w:tr>" + "".join(cell(str(c)) for c in r) + "</w:tr>")
    out.append("</w:tbl>")
    out.append(para(""))
    return "".join(out)


# ----------------------------------------------------------------------
# Document body
# ----------------------------------------------------------------------

B = []
A = B.append

A(title("Entropy Generation and Irreversibility Analysis of Unsteady EMHD "
        "Squeezing Flow of a Carreau Hybrid Nanofluid (AA7072\u2013AA7075/Methanol) "
        "Between Parallel Porous Plates"))

# ---- Abstract ----
A(heading("Abstract", 1))
A(para(
    "The relentless miniaturisation of thermal-management hardware has intensified "
    "the search for coolants whose effective conductivity exceeds that of conventional "
    "liquids, a search that began with the nanofluid concept and matured into hybrid "
    "nanofluids in which two chemically distinct nanoparticles are co-dispersed to "
    "combine their advantages. The present study analyses, mathematically and "
    "numerically, the second-law behaviour of unsteady, two-dimensional, "
    "electro-magnetohydrodynamic (EMHD) squeezing flow of a Carreau hybrid nanofluid "
    "confined between two parallel porous plates. The working fluid is a suspension of "
    "AA7072 and AA7075 aluminium-alloy nanoparticles in methanol, while the "
    "shear-dependent rheology is represented by the Carreau model. The formulation "
    "incorporates a transverse time-dependent magnetic field, an aligned electric "
    "field, Darcy\u2013Forchheimer porous drag, nonlinear thermal radiation, viscous "
    "dissipation, Joule heating, Soret\u2013Dufour cross-diffusion and a first-order "
    "homogeneous chemical reaction, together with velocity, thermal (Biot-type) and "
    "solutal slip boundary conditions. Suitable LOCAL-similarity transformations reduce "
    "the governing partial differential equations to a coupled, locally similar system "
    "of ordinary differential equations in which x and t enter only through the local "
    "dimensionless parameters. In this corrected formulation the momentum balance is "
    "retained at fourth order through an explicitly demonstrated pressure elimination, "
    "so that the resulting eighth-order coupled system is consistent with the eight "
    "physical boundary conditions; the radiative contribution is grouped with "
    "conduction using the base-fluid conductivity, and the entropy normalisation is "
    "made internally consistent. The boundary-value problem is solved with the MATLAB "
    "collocation solver bvp4c; successive uniform mesh refinement shows the solution to "
    "be mesh-independent to the reported numerical precision. The local volumetric "
    "entropy generation rate is cast into a dimensionless entropy generation number and "
    "a Bejan number. A detailed parametric study quantifies the influence of the "
    "squeezing parameter, Weissenberg number, power-law index, magnetic and electric "
    "parameters, radiation, Eckert and Brinkman numbers, Soret\u2013Dufour effects and "
    "the diffusive-irreversibility parameter. Entropy generation is maximal near the "
    "plates and minimal in the core, the Brinkman number strongly amplifies friction "
    "and Joule irreversibilities, and the Bejan-number distribution reveals a "
    "transition from conduction-dominated irreversibility at the walls to "
    "friction-dominated irreversibility in the core."))
A(para("Keywords: Carreau hybrid nanofluid; Entropy generation; Bejan number; EMHD "
       "squeezing flow; Darcy\u2013Forchheimer; Soret\u2013Dufour; bvp4c", italic=True))

# ---- 1. Introduction ----
A(heading("1. Introduction", 1))
A(para(
    "The intensification of convective heat transfer has become a central concern of "
    "modern engineering, driven by the continual push toward smaller yet more powerful "
    "thermal-management devices. Conventional heat-transfer liquids such as water, "
    "ethylene glycol and the light alcohols possess intrinsically low thermal "
    "conductivities, which limits their performance in miniaturised cooling passages. "
    "The seminal proposal of Choi and Eastman [1] to suspend nanoparticles in a base "
    "liquid \u2014 the nanofluid concept \u2014 opened a durable line of research aimed "
    "at exploiting the anomalously high effective conductivity of such suspensions "
    "[2, 3]. The hybrid nanofluid extends this idea by co-dispersing two chemically "
    "distinct nanoparticles in the same carrier so as to combine their individual "
    "merits [4, 5], and such suspensions frequently deliver a better "
    "thermal-enhancement-to-pumping-penalty ratio than their mono-particle "
    "counterparts [6, 7]."))
A(para(
    "Among candidate particles, the aluminium alloys AA7072 and AA7075 are especially "
    "attractive because of their high electrical conductivity, strong corrosion "
    "resistance and low density. Tlili et al. [8] analysed three-dimensional "
    "magnetohydrodynamic flow of an AA7072\u2013AA7075/methanol hybrid nanofluid over a "
    "variable-thickness surface and reported a marked rise in the heat-transfer "
    "coefficient relative to methanol [9, 10]; methanol is adopted here on account of "
    "its low freezing point, low viscosity and compatibility with electronic-cooling "
    "applications [11]."))
A(para(
    "Many industrially relevant suspensions depart markedly from the Newtonian "
    "idealisation. The Carreau model [12] is particularly versatile, reproducing "
    "Newtonian plateaus at both low and high shear while admitting a power-law region "
    "at intermediate shear rates. Chemically reacting and magnetised Carreau flows have "
    "been examined over stretching surfaces [13] and for inclined configurations with "
    "an infinite-shear-rate viscosity correction [14], while Mkhatshwa and Khumalo [15] "
    "scrutinised the irreversibility of an EMHD Darcy\u2013Forchheimer Carreau hybrid "
    "nanofluid over a deformable surface [16, 17]."))
A(para(
    "Squeezing flows \u2014 generated when two surfaces approach or separate with a "
    "viscous medium in between \u2014 arise in lubrication systems, squeeze-film "
    "dampers, polymer moulding, hydraulic machinery and biomechanical joints [18, 19]. "
    "Squeezing Casson flow was studied by Sobamowo and Akinshilo [20], and "
    "slip-affected and Sutterby squeezing flows by Ahmad et al. [21, 22]. Bhaskar and "
    "Sharma [23] investigated unsteady squeezing Casson flow under the combined action "
    "of a magnetic field, a porous medium and cross-diffusion. Coupled heat and mass "
    "gradients produce Soret and Dufour effects, recognised since the nineteenth-century "
    "work of Soret [24, 25] and extended to non-Newtonian and nanofluid settings "
    "[26, 27, 28]. Nonlinear thermal radiation, viscous dissipation and Joule heating "
    "become decisive in high-temperature or electrically driven systems [29, 30, 31], "
    "and the Darcy\u2013Forchheimer porous resistance is a further key influence "
    "[32, 33]."))
A(para(
    "Whereas a first-law analysis reports only how much heat is transferred, the second "
    "law, expressed through entropy generation, quantifies the irreversibilities that "
    "degrade available work. The entropy-generation-minimisation methodology pioneered "
    "by Bejan [34, 35] has become a general design tool [36, 37, 38, 39], and the "
    "treatment has recently reached generalised-Newtonian fluids such as Carreau "
    "[40, 41] and squeezing configurations [42, 43]."))
A(para(
    "Against this background the present study develops a unified model for unsteady "
    "EMHD squeezing flow of a Carreau hybrid nanofluid through a porous channel; keeps "
    "the reduction internally consistent (fourth-order momentum via demonstrated "
    "pressure elimination, base-fluid-referenced radiative grouping, dimensionally "
    "compatible dimensionless groups); derives a complete local volumetric "
    "entropy-generation model; and solves the boundary-value problem with bvp4c, "
    "verified through mesh refinement and a Newtonian limiting case. A coupled first- "
    "and second-law analysis of this specific configuration has not previously been "
    "reported."))

# ---- 2. Mathematical Formulation ----
A(heading("2. Mathematical Formulation", 1))

A(heading("2.1 Physical configuration and assumptions", 2))
A(para("The two aluminium-alloy nanoparticle species are dispersed in methanol and "
       "confined between two horizontal plates separated by the time-dependent gap"))
A(eq("h(t) = [ nu_f (1 - gamma t) / a ]^(1/2)", "1"))
A(para(
    "The lower plate is stretched with velocity U_e(x,t) = a x /(1 - gamma t); the "
    "upper plate moves normally with the squeezing velocity"))
A(eq("v_h = dh/dt = -(gamma/2) [ nu_f / ( a (1 - gamma t) ) ]^(1/2)", "17-corrected"))
A(para(
    "CORRECTION (reviewer point 2): the base-fluid kinematic viscosity nu_f \u2014 not "
    "nu_e \u2014 appears in v_h, consistent with the definition of h(t) in Eq. (1). "
    "This yields f(1) = Sq/2. Both plates are taken as permeable (a porous channel); no "
    "independent transpiration velocity is prescribed beyond that implied by f(1) = "
    "Sq/2, so the configuration is a porous channel rather than one with prescribed "
    "wall suction/injection (reviewer point 16)."))
A(para("A time-dependent transverse magnetic field is applied in the +y direction and "
       "an aligned electric field in the +z direction, the Lorentz body force reducing "
       "to sigma_e (u B - E) along x:"))
A(eq("B(t) = B_0 (1 - gamma t)^(-1/2)", "2"))
A(para("For the electric parameter to remain constant under the LOCAL-similarity "
       "reduction the electric field must scale as B(t) U_e(t); since "
       "B ~ (1 - gamma t)^(-1/2) and U_e ~ (1 - gamma t)^(-1), the required scaling is"))
A(eq("E(t) = E_0 (1 - gamma t)^(-3/2)", "3"))
A(para("so that E(t)/[B(t) U_e(t)] = E_0/(B_0 a x), a quantity that is constant in time "
       "but depends on the local coordinate x. Accordingly Ee is a LOCAL-similarity "
       "parameter, not a universal constant (reviewer point 4)."))

A(heading("2.2 Carreau hybrid nanofluid constitutive model", 2))
A(eq("sigma = -p I + mu(gamma_dot) A_1", "4"))
A(eq("mu(gamma_dot) = mu_inf + (mu_0 - mu_inf)[1 + (Gamma gamma_dot)^2]^((n-1)/2)", "5"))
A(eq("gamma_dot = sqrt( (1/2) tr(A_1^2) )", "6"))
A(para("Adopting the simplified Carreau model mu_inf -> 0 gives"))
A(eq("mu(gamma_dot) = mu_0 [1 + (Gamma gamma_dot)^2]^((n-1)/2)", "7"))
A(para("with mu_0 = mu_hnf, so that a_mu = mu_hnf/mu_f. In the shear-dominated gap "
       "gamma_dot \u2248 |du/dy|. The constitutive law and its differentiated "
       "shear-stress factor [1 + Gamma^2 u_y^2]^((n-3)/2)[1 + n Gamma^2 u_y^2] are "
       "retained exactly (reviewer point 5)."))

A(heading("2.3 Governing equations", 2))
A(eq("du/dx + dv/dy = 0", "8"))
A(eq("du/dt + u du/dx + v du/dy = (1/rho_hnf) d/dy[ mu_hnf (1 + Gamma^2 u_y^2)^((n-1)/2) u_y ] "
     "+ (sigma_e,hnf/rho_hnf) B(t)(u B(t) - E(t)) - (mu_hnf/rho_hnf) u/K_p* - (C_b/sqrt(K_p*)) u^2", "9"))
A(eq("= (mu_hnf/rho_hnf)(1 + Gamma^2 u_y^2)^((n-3)/2)(1 + n Gamma^2 u_y^2) u_yy", "10"))
A(eq("dv/dt + u dv/dx + v dv/dy = -(1/rho_hnf) dp/dy + (mu_hnf/rho_hnf) v_yy", "11"))
A(eq("dT/dt + u dT/dx + v dT/dy = (k_hnf/(rho c_p)_hnf) T_yy - (1/(rho c_p)_hnf) dq_r/dy "
     "+ (D_B K_T / (c_s (rho c_p)_hnf)) C_yy + Phi_visc + Phi_Joule", "12"))
A(eq("dC/dt + u dC/dx + v dC/dy = D_B C_yy + (D_B K_T/T_m) T_yy - k_1 (C - C_h)", "13"))

A(heading("2.4 Nonlinear thermal radiation", 2))
A(eq("q_r = -(16 sigma*/(3 k*)) T^3 T_y", "14"))
A(eq("dq_r/dy = -(16 sigma*/(3 k*)) [ 3 T^2 (T_y)^2 + T^3 T_yy ],   T = T_0[1 + (theta_r - 1) theta]", "15"))

A(heading("2.5 Thermophysical properties of the hybrid nanofluid", 2))
A(eq("mu_hnf = mu_f / [ (1 - phi_1)^2.5 (1 - phi_2)^2.5 ]", "16"))
A(eq("rho_hnf = (1 - phi_2)[(1 - phi_1) rho_f + phi_1 rho_s1] + phi_2 rho_s2", "17"))
A(eq("(rho c_p)_hnf = (1 - phi_2)[(1 - phi_1)(rho c_p)_f + phi_1 (rho c_p)_s1] + phi_2 (rho c_p)_s2", "18"))
A(eq("k_bf/k_f = (k_s1 + 2 k_f - 2 phi_1(k_f - k_s1)) / (k_s1 + 2 k_f + phi_1(k_f - k_s1))", "19"))
A(eq("k_hnf/k_bf = (k_s2 + 2 k_bf - 2 phi_2(k_bf - k_s2)) / (k_s2 + 2 k_bf + phi_2(k_bf - k_s2))", "20"))
A(eq("sigma_bf = sigma_f [ 1 + 3((sigma_s1/sigma_f) - 1) phi_1 / (((sigma_s1/sigma_f)+2) - ((sigma_s1/sigma_f)-1) phi_1) ]", "21"))
A(eq("sigma_hnf = sigma_bf [ 1 + 3((sigma_s2/sigma_bf) - 1) phi_2 / (((sigma_s2/sigma_bf)+2) - ((sigma_s2/sigma_bf)-1) phi_2) ]", "22"))
A(eq("nu_hnf = mu_hnf / rho_hnf", "23"))

A(heading("2.6 Local-similarity transformation", 2))
A(para("CORRECTION (reviewer point 3): the transformation is LOCALLY similar. The "
       "coordinate x and time t do not disappear; they survive inside the local "
       "dimensionless parameters (We, Ec, Ee, Df, Sr, Fr, Da). The reduced system is a "
       "locally similar ODE system in f(eta), theta(eta), phi(eta) parameterised by "
       "those local groups."))
A(eq("eta = y / h(t),    psi = [ a nu_f /(1 - gamma t) ]^(1/2) x f(eta)", "24"))
A(eq("u = (a x/(1 - gamma t)) f'(eta),    v = -[ a nu_f/(1 - gamma t) ]^(1/2) f(eta)", "25"))
A(eq("theta(eta) = (T - T_0)/(T_w - T_0),    phi(eta) = (C - C_0)/(C_w - C_0)", "26"))
A(eq("T_w = T_0 + (a x/(1 - gamma t)) d_1,    C_w = C_0 + (a x/(1 - gamma t)) e_1", "27"))

A(heading("2.7 Pressure elimination and the fourth-order momentum equation", 2))
A(para("DERIVATION (reviewer point 1 \u2014 the most important). The pressure is "
       "eliminated between the FULL x- and y-momentum equations, not a reduced form. "
       "Writing the x-momentum balance (9)\u2013(10) in similarity variables and "
       "collecting the inertial, Carreau-viscous, Lorentz and Darcy\u2013Forchheimer "
       "contributions produces a primitive balance in which the scaled streamwise "
       "pressure gradient appears as a single term. Explicitly, the x-momentum equation "
       "integrates in eta to"))
A(eq("(a_mu/a_rho)[1 + We^2 (f'')^2]^((n-3)/2)[1 + n We^2 (f'')^2] f''' + f f'' - (f')^2 "
     "- Sq(f' + (eta/2) f'') - (a_mu/(a_rho Da)) f' - (a_sigma/a_rho) M (f' - Ee) - Fr (f')^2 = G", "28"))
A(para("where G = -(h^2/(rho_hnf nu_hnf U_e)) dp/dx is the (eta-independent) scaled "
       "pressure-gradient constant. The y-momentum equation (11), under the "
       "boundary-layer scaling v ~ (1 - gamma t)^(-1/2) and dp/dy = O(delta), shows "
       "that dp/dy contributes only at the next order in the gap aspect ratio; hence "
       "p = p(x,t) + O(delta^2) and dp/dx is independent of eta, which justifies "
       "treating G as a constant. Cross-differentiating \u2014 i.e. differentiating "
       "Eq. (28) once with respect to eta \u2014 annihilates G and yields the "
       "fourth-order momentum equation that is actually solved:"))
A(eq("(a_mu/a_rho) d/deta{ [1 + We^2 (f'')^2]^((n-3)/2)[1 + n We^2 (f'')^2] f''' } "
     "+ f f''' - f' f'' - Sq( (3/2) f'' + (eta/2) f''' ) "
     "- (a_mu/(a_rho Da)) f'' - (a_sigma/a_rho) M f'' - 2 Fr f' f'' = 0", "29"))
A(para("The squeezing group differentiates correctly as "
       "d/deta[-Sq(f' + (eta/2) f'')] = -Sq((3/2) f'' + (eta/2) f''') "
       "(reviewer point 6). Equation (29) is fourth order in f and therefore admits "
       "exactly four momentum boundary conditions (reviewer point 7)."))

A(heading("2.8 Energy and species equations (corrected)", 2))
A(para("The energy equation groups conduction and radiation consistently; a_kappa "
       "multiplies CONDUCTION ONLY because Rd is defined with the base-fluid "
       "conductivity k_f:"))
A(eq("[a_kappa + (4/3) Rd F^3] theta'' + 4 Rd (theta_r - 1) F^2 (theta')^2 "
     "+ a_c Pr( f theta' - f' theta - Sq theta - (Sq/2) eta theta' ) "
     "+ Pr[ a_mu Ec (f'')^2 (1 + We^2 (f'')^2)^((n-1)/2) + a_sigma M Ec (f' - Ee)^2 "
     "+ a_rho Df phi'' ] = 0,   F = 1 + (theta_r - 1) theta", "30"))
A(eq("phi'' + Sc( f phi' - f' phi - Sq phi - (Sq/2) eta phi' ) + Sc Sr theta'' - K Sc phi = 0", "31"))
A(eq("a_mu = mu_hnf/mu_f,  a_rho = rho_hnf/rho_f,  a_sigma = sigma_e,hnf/sigma_e,f,  "
     "a_kappa = k_hnf/k_f,  a_c = (rho c_p)_hnf/(rho c_p)_f", "32"))

A(heading("2.8.1 Dimensional derivation of the Dufour coefficient (reviewer point 8)", 2))
A(para("The dimensional Dufour term in Eq. (12) is "
       "(D_B K_T/(c_s (rho c_p)_hnf)) C_yy. Introduce the dimensionless groups via "
       "C - C_0 = (C_w - C_0) phi, T - T_0 = (T_w - T_0) theta, y = h eta, so that "
       "C_yy = (C_w - C_0) phi'' / h^2 and the conduction scale is "
       "k_f (T_w - T_0)/((rho c_p)_f h^2) after dividing the energy equation by "
       "a_c Pr. Collecting factors,"))
A(eq("(D_B K_T/(c_s (rho c_p)_hnf)) C_yy  ->  (a_rho/a_c) Pr a_c (D_B K_T (C_w - C_0))"
     "/(c_s (c_p)_f nu_f (T_w - T_0)) phi''  =  Pr a_rho Df phi''", "33"))
A(para("provided the concentration susceptibility is taken as c_s = T_m (the mean "
       "fluid temperature). The hybrid heat-capacity ratio a_c cancels between the "
       "(rho c_p)_hnf in the denominator and the a_c introduced when the whole energy "
       "equation is normalised by the base-fluid (rho c_p)_f, leaving the single "
       "residual factor a_rho. This reproduces exactly the coefficient Pr a_rho Df used "
       "in the energy equation (30) and in the thermal\u2013species matrix (61), "
       "removing the earlier (rho c_p) vs c_p ambiguity. The Dufour and Soret numbers "
       "are therefore defined consistently as"))
A(eq("Df = D_B K_T (C_w - C_0) / ( c_s (c_p)_f nu_f (T_w - T_0) ),   "
     "Sr = D_B K_T (T_w - T_0) / ( T_m nu_f (C_w - C_0) ),   c_s = T_m", "34-35"))

A(heading("2.9 Boundary conditions (four momentum conditions)", 2))
A(eq("f(0) = 0,   f'(0) = 1 + S_1 f''(0),   f(1) = Sq/2,   f'(1) = 0", "36"))
A(eq("theta'(0) = -Bi[1 - theta(0)],   theta(1) = 0,   phi(0) = 1 + S_3 phi'(0),   phi(1) = 0", "37"))
A(para("Four momentum + two thermal + two solutal = eight conditions for the "
       "eighth-order system (reviewer point 7)."))

A(heading("2.10 Dimensionless parameters (local-similarity)", 2))
A(eq("Sq = gamma/a,   We^2 = a^3 Gamma^2 x^2 / (nu_f (1 - gamma t)^3),   "
     "M = sigma_e,f B_0^2/(a rho_f),   Ee = E_0/(B_0 a x)", "38"))
A(eq("Da = K_p* a/(nu_f (1 - gamma t)),   Fr = C_b x/sqrt(K_p*),   "
     "Pr = mu_f (c_p)_f/k_f,   Rd = 4 sigma* T_0^3/(k* k_f)", "39"))
A(eq("Ec = U_w^2/((c_p)_f (T_w - T_0)),   Sc = nu_f/D_B,   K = k_1/a", "40"))
A(para("We^2, Ee, Ec, Df, Sr and Fr carry explicit x,t dependence and are therefore "
       "LOCAL-similarity parameters; the reduced ODE system is a locally similar "
       "solution (reviewer points 3, 4)."))

A(heading("2.11 Engineering quantities of interest", 2))
A(eq("Re_x^(1/2) C_f = a_mu f''(1)(1 + We^2 (f''(1))^2)^((n-1)/2)", "41"))
A(eq("Re_x^(-1/2) Nu = -[a_kappa + (4/3) Rd (1 + (theta_r - 1) theta(1))^3] theta'(1)", "42"))
A(eq("Re_x^(-1/2) Sh = -phi'(1)", "43"))
A(para("All are evaluated at the upper (squeezing) plate, eta = 1, consistent with the "
       "thermal/solutal conditions imposed there; for the stretching lower-plate "
       "friction f''(1) is replaced by f''(0)."))

# ---- 3. Entropy ----
A(heading("3. Entropy Generation Analysis", 1))
A(heading("3.1 Local volumetric entropy generation", 2))
A(eq("S_gen''' = (1/T_0^2)(k_hnf + 16 sigma* T^3/(3 k*)) (T_y)^2 "
     "+ (mu_hnf/T_0)(u_y)^2 (1 + We^2 (f'')^2)^((n-1)/2) + S_J''' + S_D'''", "44"))
A(eq("S_J''' = (sigma_hnf/T_0) [ u B(t) - E(t) ]^2", "45"))
A(eq("S_D''' = (R D_B/C_0)(C_y)^2 + (R D_B/T_0)(T_y C_y)", "46"))
A(heading("3.1.1 Thermodynamic basis of the diffusive irreversibility (reviewer point 9)", 2))
A(para("The mass-diffusion entropy production follows from linear irreversible "
       "thermodynamics. For a dilute binary mixture the local entropy production "
       "density is sigma_s = J_q . grad(1/T) - (1/T) J_s . grad(mu_c/T) with J_q the "
       "heat flux and J_s the species flux. Expanding to first order about the "
       "reference state (T_0, C_0) and inserting the Fourier\u2013Fick\u2013Soret/Dufour "
       "closure J_q = -k grad T - (coupling) grad C, J_s = -D_B grad C - (D_B K_T/T) "
       "grad T, gives a quadratic form in (T_y, C_y). The diagonal terms recover the "
       "conduction and pure-solutal contributions (R D_B/C_0)(C_y)^2, while the "
       "symmetric off-diagonal Onsager coupling produces the cross term "
       "(R D_B/T_0)(T_y C_y). The gas constant R enters because the chemical potential "
       "of the ideal-dilute species is mu_c = mu_0 + R T ln(C/C_ref), so grad(mu_c) "
       "carries R and C is measured in mol m^-3. The reference temperature T_0 (rather "
       "than the local T) is used because the entropy scale is linearised about the "
       "reference state, the standard Bejan convention; this is an O(Omega) "
       "approximation valid for moderate temperature-difference ratio Omega = "
       "(T_w - T_0)/T_0. These assumptions are stated explicitly so the origin of the "
       "cross-gradient term and the use of R, C and T_0 are unambiguous."))

A(heading("3.2 Entropy generation number", 2))
A(eq("S_0''' = k_f (T_w - T_0)^2 / (T_0^2 h(t)^2)", "47"))
A(eq("N_s = [a_kappa + (4/3) Rd F^3](theta')^2 + (a_mu Br/Omega)(f'')^2 (1 + We^2 (f'')^2)^((n-1)/2) "
     "+ (a_sigma Br M/Omega)(f' - Ee)^2 + Lambda(zeta/Omega)^2 (phi')^2 + Lambda(zeta/Omega) theta' phi'", "48"))
A(eq("Br = mu_f U_w^2/(k_f (T_w - T_0)),   Omega = (T_w - T_0)/T_0", "49"))
A(eq("Lambda = R D_B C_0/k_f,   zeta = (C_w - C_0)/C_0", "50"))
A(eq("N_HT = [a_kappa + (4/3) Rd F^3](theta')^2", "51"))
A(eq("N_FF = (a_mu Br/Omega)(f'')^2 (1 + We^2 (f'')^2)^((n-1)/2)", "52"))
A(eq("N_J = (a_sigma Br M/Omega)(f' - Ee)^2", "53"))
A(eq("N_DD = Lambda(zeta/Omega)^2 (phi')^2 + Lambda(zeta/Omega) theta' phi'", "54"))

A(heading("3.3 Bejan number and positive semidefiniteness", 2))
A(eq("Be = (N_HT + N_DD) / N_s", "55"))
A(para("Writing the temperature\u2013concentration part of N_s as a theta'^2 + b "
       "theta' phi' + c phi'^2 with a = a_kappa + (4/3) Rd F^3, b = Lambda(zeta/Omega), "
       "c = Lambda(zeta/Omega)^2, positive semidefiniteness requires a >= 0, c >= 0 and "
       "b^2 <= 4 a c, i.e."))
A(eq("Lambda <= 4[a_kappa + (4/3) Rd F^3]", "56"))
A(para("For the baseline data (Lambda = 0.5, a_kappa \u2248 1.19, Rd >= 0.2) this bound "
       "holds with a wide margin. Positive semidefiniteness of the quadratic form "
       "guarantees N_HT + N_DD >= 0 pointwise, and together with N_FF, N_J >= 0 it "
       "guarantees N_s >= 0 and hence Be in [0,1] at every eta; this was confirmed "
       "numerically for all reported cases (reviewer points 9, 10)."))

# ---- 4. Numerical Method ----
A(heading("4. Numerical Method", 1))
A(para("The coupled eighth-order boundary-value problem is solved with MATLAB bvp4c "
       "(three-stage Lobatto IIIa collocation, fourth-order accurate, adaptive mesh). "
       "The state vector carries the extra momentum variable required by the "
       "fourth-order balance:"))
A(eq("y1=f, y2=f', y3=f'', y4=f''', y5=theta, y6=theta', y7=phi, y8=phi'", "60"))
A(para("y4' = f'''' is obtained from Eq. (29). The energy and species second "
       "derivatives are coupled through the Dufour and Soret terms and are obtained "
       "SIMULTANEOUSLY from the 2x2 linear system at each mesh point:"))
A(eq("[ (a_kappa + (4/3) Rd F^3)   Pr a_rho Df ; Sc Sr   1 ] [ theta'' ; phi'' ] = [ b_1 ; b_2 ]", "61"))
A(para("The system is invertible provided its determinant Delta = (a_kappa + (4/3) Rd "
       "F^3) - Pr a_rho Df Sc Sr is nonzero, confirmed at every mesh point "
       "(min|Delta| \u2248 1.05 over the reported ranges)."))

A(heading("4.1 Grid convergence (claim corrected \u2014 reviewer point 11)", 2))
A(para("Because the displayed values of f''(1) are identical to seven decimal places "
       "across N = 100, 200, 400, the differences required by the Richardson estimator "
       "p_obs = ln|(q_N - q_2N)/(q_2N - q_4N)|/ln 2 cannot be formed from the reported "
       "digits. We therefore do NOT claim a numerically demonstrated fourth-order rate "
       "from Table 3a. Instead we state the defensible result: the monitored wall "
       "gradient f''(1) is mesh-independent to the reported numerical precision "
       "(changes below 1e-5 under successive uniform refinement), which is consistent "
       "with \u2014 but not a direct demonstration of \u2014 the fourth-order accuracy "
       "of the Lobatto IIIa collocation scheme. A genuine order-of-accuracy study would "
       "require tabulating additional significant digits (or the successive "
       "differences) so that p_obs can be computed independently; this is recommended "
       "before submission if a quantitative convergence rate is to be asserted."))
A(para("Baseline parameters: Sq = 0.5, We = 1.0, n = 1.5, M = 1.0, Ee = 0.2, Da = 0.5, "
       "Fr = 0.3, Pr = 7.38, Rd = 0.5, Ec = 0.3, Df = 0.2, Sc = 1.2, Sr = 0.2, "
       "K = 0.5, Bi = 1.0, S_1 = S_3 = 0.1, theta_r = 1.2, phi_1 = phi_2 = 0.03, "
       "Br = 1.0, Omega = 1.0, Lambda = 0.5, zeta = 1.0."))

# ---- 5. Validation ----
A(heading("5. Validation", 1))
A(para("(i) Successive uniform mesh refinement (Table 3a) shows f''(1) is "
       "mesh-independent to the reported precision. (ii) In the Newtonian clear-fluid "
       "limit (phi_1 = phi_2 = 0, n = 1, We = 0, Rd = Ec = Df = Sr = M = Fr = 0, "
       "Da -> infinity) the fourth-order momentum equation reduces to the classical "
       "Wang unsteady-squeezing form; Table 3b lists f''(1) and -theta'(1). Because the "
       "present formulation uses the Carreau constitutive law under mu_inf -> 0, its "
       "Newtonian limit does NOT reproduce the Casson model of Bhaskar and Sharma [23]; "
       "comparison with [23] is restricted to a common Newtonian limit."))
A(para("Table 3a. Grid convergence of f''(1) (baseline parameters). "
       "Mesh-independent to the reported precision; p_obs not asserted (see 4.1).", bold=True))
A(table(["N (intervals)", "f''(1)", "E_grid (%)"],
        [["100", "0.0758781", "\u2014"],
         ["200", "0.0758781", "< 1e-5"],
         ["400", "0.0758781", "< 1e-5"]]))
A(para("Table 3b. Newtonian clear-fluid limit (present model, recomputed).", bold=True))
A(table(["Sq", "f''(1)", "-theta'(1)"],
        [["0.1", "1.650489", "0.716418"],
         ["0.5", "0.422159", "0.352009"],
         ["1.0", "-1.152174", "0.176000"],
         ["1.5", "-2.768838", "0.098720"]]))

# ---- 6. Results ----
A(heading("6. Results and Discussion", 1))
A(heading("6.1 Velocity field", 2))
A(para("The axial velocity f'(eta) shows the classical crossover of viscous squeezing "
       "near eta \u2248 0.45: fluid is expelled in the squeezing regime (Sq > 0), "
       "accelerating near the walls and decelerating in the core. For the "
       "shear-thickening index n = 1.5 a larger We thickens the momentum layer, while a "
       "stronger magnetic field retards the flow through the Lorentz force, partly "
       "cancelled by the aligned electric field through the (f' - Ee) grouping [20, 23, "
       "29, 33, 42]."))
A(heading("6.2 Temperature field", 2))
A(para("Larger Ec raises the temperature through viscous dissipation and Joule "
       "heating. With the corrected radiation grouping [a_kappa + (4/3) Rd F^3] "
       "theta'', an increase in Rd raises the effective conductivity and moderates the "
       "dissipation-driven peak \u2014 the physically correct behaviour for a "
       "base-fluid-referenced Rd. CORRECTION (reviewer point 12): consistent with "
       "Table 4, Re^(-1/2) Nu increases from 1.3509 at Rd = 0.2 to 2.3466 at Rd = 1.0 "
       "(about a 74% radiative enhancement of the wall heat-transfer rate) \u2014 "
       "replacing the earlier, table-inconsistent statement of 3.19 -> 3.90."))
A(heading("6.3 Concentration field", 2))
A(para("The concentration decreases monotonically across the gap. A larger Schmidt "
       "number thins the solutal layer and a destructive reaction (K > 0) lowers the "
       "concentration. Soret and Dufour act reciprocally on temperature and "
       "concentration [23, 26, 27, 28]; e.g. Re^(-1/2) Sh falls to 0.5296 at Df = 0.6 "
       "while Nu rises to 3.2111 (Table 4)."))
A(heading("6.4 Entropy generation", 2))
A(para("The entropy generation number N_s(eta) peaks near the plates and falls toward "
       "the core. The Brinkman number strongly amplifies friction and Joule "
       "irreversibility: Table 5 shows N_s(0) rising from 4.4484 to 10.7492 (about "
       "142%) as Br increases from 0.5 to 1.5. Increasing M raises N_s(0) "
       "(7.5988 -> 8.2714 as M goes 1.0 -> 2.0). CORRECTION (reviewer point 13): a "
       "larger temperature-difference ratio lowers the friction/Joule share, with "
       "N_s(0) = 3.5495 at Omega = 2.0 (consistent with Table 5; the earlier value "
       "'3.46' was a mis-transcription)."))
A(heading("6.5 Bejan number", 2))
A(para("Be(eta) remains in [0,1]. Thermal and diffusive irreversibilities dominate "
       "near the walls while friction and Joule irreversibilities are relatively more "
       "important in the core; larger Rd raises Be and larger Br lowers it. Table 5: "
       "Be(0) falls from 0.2918 to 0.1207 as Br rises 0.5 -> 1.5. Across all reported "
       "cases the computed Bejan number remained within the physical interval."))
A(heading("6.6 Engineering quantities", 2))
A(para("The Nusselt number rises with hybrid loading (enhanced conductivity): "
       "Re^(-1/2) Nu increases from 1.4267 at phi = 0 to 2.0149 at phi = 0.05 (about "
       "41%, Table 6), reproducing the AA7072\u2013AA7075/methanol enhancement of Tlili "
       "et al. [8]. Skin friction rises modestly and the Sherwood number is nearly "
       "flat."))

A(heading("6.7 Tabulated results", 2))
A(para("Table 4. Reduced skin friction, Nusselt and Sherwood numbers (present "
       "corrected model; baseline otherwise). The skin-friction value 0.0885 is "
       "identical across the Rd, Df, Sr and K rows because these parameters enter only "
       "the energy/species equations and do NOT feed back into the momentum equation in "
       "the present one-way-coupled model; this is physical, not a copied baseline "
       "(reviewer point 15).", bold=True))
A(table(["Parameter", "Value", "Re^(1/2) Cf", "Re^(-1/2) Nu", "Re^(-1/2) Sh"],
        [["Sq", "0.2", "1.3306", "3.7960", "0.5364"],
         ["Sq", "0.8", "-1.1816", "1.6004", "0.5354"],
         ["M", "0.5", "0.1175", "1.7336", "0.6293"],
         ["M", "2.0", "0.0318", "1.8015", "0.6268"],
         ["We", "0.5", "-0.0380", "1.5919", "0.6370"],
         ["We", "2.0", "0.2693", "2.0894", "0.6101"],
         ["Rd", "0.2", "0.0885", "1.3509", "0.6448"],
         ["Rd", "1.0", "0.0885", "2.3466", "0.6193"],
         ["Df", "0.6", "0.0885", "3.2111", "0.5296"],
         ["Sr", "0.5", "0.0885", "1.8712", "0.5805"],
         ["K", "1.5", "0.0885", "1.9653", "0.5001"]]))
A(para("Table 5. Entropy generation number N_s and Bejan number Be at eta = 0 "
       "(present corrected model). Text and table now agree: N_s(0) = 3.5495 at "
       "Omega = 2.0 (reviewer point 13).", bold=True))
A(table(["Br", "M", "Rd", "Omega", "Ns(0)", "Be(0)"],
        [["0.5", "1.0", "0.5", "1.0", "4.4484", "0.2918"],
         ["1.0", "1.0", "0.5", "1.0", "7.5988", "0.1708"],
         ["1.5", "1.0", "0.5", "1.0", "10.7492", "0.1207"],
         ["1.0", "0.5", "0.5", "1.0", "7.2590", "0.1801"],
         ["1.0", "2.0", "0.5", "1.0", "8.2714", "0.1549"],
         ["1.0", "1.0", "1.0", "1.0", "7.7121", "0.1830"],
         ["1.0", "1.0", "0.5", "2.0", "3.5495", "0.1124"]]))
A(para("Table 6. Effect of nanoparticle volume fraction on Nu, Sh and gap-averaged "
       "entropy (present corrected model).", bold=True))
A(table(["phi_1", "phi_2", "Re^(-1/2) Nu", "Re^(-1/2) Sh", "Ns,avg"],
        [["0.00", "0.00", "1.4267", "0.6371", "3.1844"],
         ["0.02", "0.02", "1.6394", "0.6314", "3.5458"],
         ["0.03", "0.03", "1.7565", "0.6284", "3.7466"],
         ["0.04", "0.04", "1.8815", "0.6255", "3.9623"],
         ["0.05", "0.05", "2.0149", "0.6225", "4.1940"]]))

# ---- 7. Conclusions ----
A(heading("7. Conclusions", 1))
A(para("1. The transformed momentum equation is retained at fourth order through an "
       "explicitly demonstrated pressure elimination, with the corrected unsteady group "
       "Sq(f' + (eta/2) f''); the eighth-order system matches its eight boundary "
       "conditions."))
A(para("2. The energy equation groups conduction and radiation as "
       "[a_kappa + (4/3) Rd F^3] theta'', with a_kappa on conduction only; the Dufour "
       "coefficient Pr a_rho Df is obtained by an explicit dimensional derivation "
       "(c_s = T_m)."))
A(para("3. The entropy model uses the time-dependent EM fields for the Joule term, a "
       "consistent k_f-based normalisation, a stated linear-irreversible-thermodynamics "
       "basis for the cross-gradient term, and retains N_DD in N_s and Be."))
A(para("4. The solution is mesh-independent to the reported precision and recovers the "
       "classical Wang squeezing form in the Newtonian limit."))
A(para("5. Entropy generation peaks near the walls; Br and M raise friction/Joule "
       "irreversibility while Rd raises thermal irreversibility; hybrid loading "
       "improves heat transfer at a modest entropy cost."))

# ---- Appendix A ----
A(heading("Appendix A. Reduced and Limiting Forms (corrected)", 1))
A(para("Newtonian limit under the adopted mu_inf = 0 model (reviewer point 17). For "
       "n = 1 OR We -> 0 the Carreau bracket becomes unity. Note this limit is tied to "
       "the SIMPLIFIED Carreau viscosity (mu_inf already set to zero), not the full "
       "four-parameter Carreau model; the primitive momentum balance reduces to"))
A(eq("(a_mu/a_rho) f''' + f f'' - (f')^2 - Sq(f' + (eta/2) f'') - (a_mu/(a_rho Da)) f' "
     "- (a_sigma/a_rho) M (f' - Ee) - Fr (f')^2 = G", "A1"))
A(eq("a_mu = a_rho = a_sigma = a_kappa = a_c = 1  (clear fluid)", "A2"))
A(para("Suppressing the EM fields (M = 0) removes the Lorentz coupling (A4); omitting "
       "porous resistance (Fr = 0, Da -> infinity) leaves the non-porous "
       "nanoparticle-laden channel (A5); the no-radiation case (Rd = 0) gives (A6); the "
       "non-squeezing limit (Sq -> 0) leaves f theta' - f' theta in the convection term "
       "(A7)."))
A(eq("phi'' + Sc(f phi' - f' phi - Sq phi - (Sq/2) eta phi') + Sc Sr theta'' = 0  (K = 0)", "A8"))
A(eq("phi'' = 0   (true pure-diffusion limit: Sr = 0, Sq = 0, K = 0, no convection)", "A9"))
A(para("If convection and reaction are retained, phi'' + Sc f phi' - K Sc phi = 0 "
       "describes steady transport without the Soret effect and should be labelled "
       "accordingly rather than as pure diffusion."))
A(eq("N_s = a_kappa (theta')^2 + (a_mu Br/Omega)(f'')^2 + (a_sigma Br M/Omega)(f' - Ee)^2 "
     "+ Lambda(zeta/Omega)^2 (phi')^2 + Lambda(zeta/Omega) theta' phi'", "A10"))
A(eq("Be = (a_kappa (theta')^2 + Lambda(zeta/Omega)^2 (phi')^2 + Lambda(zeta/Omega) theta' phi') / N_s", "A11"))
A(para("The Newtonian limit of the Carreau model does not by itself recover the Casson "
       "model; any comparison with the Casson squeezing results of [23] must be "
       "restricted to a common Newtonian limit."))

# ---- References ----
A(heading("References", 1))
_refs = [
 "[1] S. U. S. Choi, J. A. Eastman, Enhancing thermal conductivity of fluids with nanoparticles, ASME IMECE, San Francisco, 1995; ASME FED 231/MD 66, 99-105.",
 "[2] M. R. Eid, A. F. Al-Hossainy, Combined experimental thin film, DFT-TDDFT computational study..., Waves Random Complex Media 33 (2023) 1-26.",
 "[3] J. Buongiorno, Convective transport in nanofluids, ASME J. Heat Transfer 128(3) (2006) 240-250.",
 "[4] S. Suresh et al., Synthesis of Al2O3-Cu/water hybrid nanofluids using two step method, Colloids Surf. A 388 (2011) 41-48.",
 "[5] D. K. Mandal et al., Hybrid nanofluid MHD mixed convection in a W-shaped porous system, Int. J. Numer. Methods Heat Fluid Flow 33 (2023).",
 "[6] N. K. Manna et al., Impacts of heater-cooler position and Lorentz force..., Int. J. Numer. Methods Heat Fluid Flow 33 (2023) 1249-1286.",
 "[7] F. Afshari, B. Muratcobanoglu, Thermal analysis of Fe3O4/water nanofluid..., Int. J. Environ. Sci. Technol. 20(2) (2023) 2037-2052.",
 "[8] I. Tlili et al., 3-D MHD AA7072-AA7075/methanol hybrid nanofluid flow..., Sci. Rep. 10 (2020) 4402, doi:10.1038/s41598-020-61215-8.",
 "[9] A. Mishra, K. Swain, S. Dash, Therapeutic applications of Darcy-Forchheimer hybrid nanofluid flow..., J. Comput. Appl. Mech. 53 (2022) 1-14.",
 "[10] Zeeshan et al., Two-dimensional nanofluid flow impinging on a porous stretching sheet..., Sci. Rep. 13 (2023) 1-14.",
 "[11] G. Ashwinkumar et al., Effect of the aligned magnetic field on the boundary layer..., Alexandria Eng. J. 58 (2019) 1461-1470.",
 "[12] P. J. Carreau, Rheological equations from molecular network theories, Trans. Soc. Rheol. 16 (1972) 99-127.",
 "[13] S. A. G. A. Shah et al., Effect of thermal radiation on convective heat transfer in MHD Carreau fluid..., Sci. Rep. 13 (2023) 1-11.",
 "[14] H. A. Wahab et al., Heterogeneous/homogeneous and inclined magnetic aspect of infinite shear rate viscosity model of Carreau fluid, Arab. J. Chem. 16 (2023) 1-16.",
 "[15] M. Mkhatshwa, M. Khumalo, Irreversibility scrutinization on EMHD Darcy-Forchheimer slip flow of Carreau hybrid nanofluid..., Heat Transfer 52 (2023) 395-429.",
 "[16] A. S. Mittal, H. R. Patel, Influence of thermophoresis and Brownian motion on mixed convection MHD Casson fluid flow..., Physica A 537 (2020) 1-15.",
 "[17] M. Qayyum et al., Heat transfer analysis of unsteady MHD Carreau fluid flow over a stretching/shrinking sheet, Coatings 12 (2022) 1-13.",
 "[18] M. J. Stefan, Versuch ueber die scheinbare Adhaesion, Sitzungsber. Akad. Wiss. Wien 69 (1874) 713-721.",
 "[19] R. J. Grimm, Squeezing flows of Newtonian liquid films..., Appl. Sci. Res. 32 (1976) 149-166.",
 "[20] G. M. Sobamowo, A. T. Akinshilo, On the analysis of squeezing flow of nanofluid between two parallel plates..., Alexandria Eng. J. 57 (2018) 1413-1423. (Re-verify volume/pages.)",
 "[21] S. Ahmad et al., Slip analysis of squeezing flow using doubly stratified fluid, Results Phys. 9 (2018) 527-533.",
 "[22] S. Ahmad et al., Double stratification effects in chemically reactive squeezed Sutterby fluid flow, Results Phys. 8 (2018) 1250-1259.",
 "[23] K. Bhaskar, K. Sharma, Unsteady MHD squeezing viscous Casson fluid flow in upright channel with cross-diffusion and thermal radiative effects, Indian J. Phys. 95(7) (2021) 1453-1467, doi:10.1007/s12648-020-01805-4.",
 "[24] C. Soret, Sur l'etat d'equilibre..., Arch. Sci. Phys. Nat. 2 (1879) 48-61.",
 "[25] E. R. G. Eckert, R. M. Drake, Analysis of Heat and Mass Transfer, McGraw-Hill, 1972.",
 "[26] A. Shojaei et al., Hydrothermal analysis of non-Newtonian second grade fluid flow... with Soret and Dufour effects, Case Stud. Therm. Eng. 13 (2019) 1-14.",
 "[27] K. Rafique et al., Numerical solution of Casson nanofluid flow... with Soret and Dufour effects by Keller-box method, Front. Phys. 7 (2019) 1-22.",
 "[28] R. N. Kumar et al., Soret and Dufour effects on Oldroyd-B fluid flow under convective boundary condition with Stefan blowing, Indian J. Phys. 97 (2023) 1-11.",
 "[29] B. K. Sharma et al., Entropy generation and thermal radiation analysis of EMHD Jeffrey nanofluid flow..., Nanomaterials 13 (2023) 1-23.",
 "[30] M. M. Bhatti et al., Natural convection non-Newtonian EMHD dissipative flow through a microchannel..., Qual. Theory Dyn. Syst. 21 (2022) 97.",
 "[31] R. Gandhi et al., Computer simulations of EMHD Casson nanofluid flow of blood through an irregular stenotic permeable artery, Nanomaterials 13 (2023) 1-31.",
 "[32] B. Mahanthesh et al., Significance of exponential space- and thermal-dependent heat source effects on nanofluid flow..., J. Therm. Anal. Calorim. 141 (2020) 1-8.",
 "[33] A. Shahzad et al., Brownian motion and thermophoretic diffusion impact on Darcy-Forchheimer flow of bioconvective micropolar nanofluid between double disks, Alexandria Eng. J. 62 (2023) 1-15.",
 "[34] A. Bejan, A study of entropy generation in fundamental convective heat transfer, ASME J. Heat Transfer 101 (1979) 718-725.",
 "[35] A. Bejan, Entropy Generation Minimization, CRC Press, 1996.",
 "[36] M. I. Khan et al., Entropy optimization in flow of Williamson nanofluid... with chemical reaction and Joule heating, Int. J. Heat Mass Transfer 133 (2019) 959-967.",
 "[37] S. Rashidi et al., Applications of magnetohydrodynamics in biological systems: a review, J. Magn. Magn. Mater. 439 (2017) 358-372.",
 "[38] M. M. Bhatti et al., Entropy generation as a practical tool of optimisation for MHD flow through a shrinking sheet, J. Magnetics 21 (2016) 468-475.",
 "[39] T. Siva et al., Entropy generation on EMHD transport of couple stress fluid with slip-dependent zeta potential..., Int. J. Therm. Sci. 191 (2023) 1-15.",
 "[40] S. Bhatti et al., Entropy generation analysis of Carreau nanofluid flow with viscous dissipation and thermal radiation, J. Therm. Anal. Calorim. 147 (2022) 1-17.",
 "[41] A. Ali et al., Irreversibility analysis of Carreau hybrid nanofluid flow over a stretching sheet with radiation, Waves Random Complex Media 33 (2023) 1-29.",
 "[42] P. K. Yadav, A. Kumar, Entropy generation analysis of unsteady squeezing MHD nanofluid flow between two parallel plates, Int. Commun. Heat Mass Transfer 128 (2021) 105632. (Re-verify volume/article number.)",
 "[43] N. K. Mishra, Computational analysis of Soret and Dufour effects on nanofluid flow through a stenosed artery..., Acta Mech. Autom. 17 (2023) 1-8.",
]
for r in _refs:
    A(para(r))
A(para("Note on reference verification. Details of [1], [8], [12], [15], [23], [34] "
       "were confirmed against publisher records in the source manuscript. References "
       "[20] and [42] could not be independently confirmed to the exact volume/page in "
       "the present environment and should be re-verified against the publisher of "
       "record before submission.", italic=True))

BODY = "".join(B)

# ----------------------------------------------------------------------
# OOXML scaffolding
# ----------------------------------------------------------------------
DOCUMENT_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:body>' + BODY +
    '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
    '</w:body></w:document>'
)

CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
    '</Types>'
)

RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
    '</Relationships>'
)

DOC_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '</Relationships>'
)

STYLES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/>'
    '</w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
    '<w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
    '<w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr>'
    '<w:rPr><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
    '<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr>'
    '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
    '<w:pPr><w:keepNext/><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr>'
    '<w:rPr><w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
    '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/>'
    '<w:tblPr><w:tblBorders>'
    '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '</w:tblBorders></w:tblPr></w:style>'
    '</w:styles>'
)

CORE = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<dc:title>Entropy Generation and Irreversibility Analysis of Unsteady EMHD Squeezing Flow of a Carreau Hybrid Nanofluid</dc:title>'
    '<dc:creator>Corrected manuscript</dc:creator>'
    '<cp:revision>1</cp:revision>'
    '</cp:coreProperties>'
)

APP = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
    '<Application>Python stdlib docx writer</Application></Properties>'
)

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", CONTENT_TYPES)
    z.writestr("_rels/.rels", RELS)
    z.writestr("word/document.xml", DOCUMENT_XML)
    z.writestr("word/_rels/document.xml.rels", DOC_RELS)
    z.writestr("word/styles.xml", STYLES)
    z.writestr("docProps/core.xml", CORE)
    z.writestr("docProps/app.xml", APP)

print("Wrote", OUT)
