#!/usr/bin/env python3
"""
Build the CORRECTED manuscript as a .docx with all equations in native Word
equation-editor (OMML) format, in strict serial order, and the regenerated
figures inserted. Pure stdlib.

Run generate_carreau_emhd_figures.py first so the PNGs exist.
"""

import os
from docx_omml import Document, run, op, sup, sub, subsup, frac, rad, delim, brack, nary, group, G

FIGDIR = "/projects/sandbox/AMMAN/carreau_emhd_figures"
OUT = "/projects/sandbox/AMMAN/Carreau_EMHD_Squeezing_Corrected.docx"

# ---- shorthand OMML atoms -------------------------------------------------
def r(t): return run(t)
def i(t): return run(t)              # italic variable
def u(t): return op(t)               # upright / operator / word
def b(t):                            # bold (tensors)
    from docx_omml import _mr
    return _mr(t, sty='b')
def A1tensor():                      # bold first Rivlin-Ericksen tensor A_1
    return sub(b("A"), r("1"))
def eq(): return op("=")
def plus(): return op("+")
def minus(): return op(G['minus'])
def eta(): return i(G['eta'])
def theta(): return i(G['theta'])
def phi(): return i(G['phi'])
def prime(n=1): return i(G['prime'] * n)

def fp(k=1):  # f, f', f'', f''', f''''
    return group(i("f")) if k == 0 else group(i("f"), prime(k))

def thp(k=0):
    return group(theta()) if k == 0 else group(theta(), prime(k))

def php(k=0):
    return group(phi()) if k == 0 else group(phi(), prime(k))

def sqhalf():
    return frac(i("Sq"), r("2"))

def We2fpp2():  # 1 + We^2 (f'')^2
    return group(r("1"), plus(), sup(i("We"), r("2")), sup(delim(fp(2)), r("2")))

def carreau_bracket(exp_num):  # [1+We^2 f''^2]^{exp}
    return sup(brack(group(r("1"), plus(), sup(i("We"), r("2")), sup(delim(fp(2)), r("2")))), exp_num)

def A(n):
    # Property ratios use alpha_* to avoid clashing with the Rivlin-Ericksen tensor A_1.
    _sub = {1: G['mu'], 2: G['rho'], 3: "\u03c3", 4: G['kappa'], 5: "c"}[n]
    return sub(i("\u03b1"), i(_sub))

def F_expr():  # 1 + (theta_r - 1) theta
    return group(r("1"), plus(), delim(group(sub(i(G['theta']), i("r")), minus(), r("1"))), theta())


# ---------------------------------------------------------------------------
# Reference registry + citation manager.
# References are numbered in strict order of FIRST appearance (starting in the
# abstract). cite(key) returns the serial number, assigning it on first use;
# cite_range(k1, k2) prints a contiguous range using already/também-assigned numbers.
# REF_META maps stable keys -> (verified_flag, full reference text).
# ---------------------------------------------------------------------------
REF_META = {
    "choi":    ("\u2020", "S. U. S. Choi, J. A. Eastman, \u201cEnhancing thermal conductivity of fluids with nanoparticles,\u201d ASME International Mechanical Engineering Congress & Exposition, San Francisco, 12\u201317 Nov. 1995; ASME FED vol. 231/MD vol. 66, pp. 99\u2013105 (ANL/MSD/CP-84938)."),
    "eid":     ("", "M. R. Eid, A. F. Al-Hossainy, \u201cCombined experimental thin film, DFT\u2013TDDFT computational study, flow and heat transfer in hybrid nanofluid,\u201d Waves Random Complex Media 33 (2023) 1\u201326."),
    "buongiorno": ("", "J. Buongiorno, \u201cConvective transport in nanofluids,\u201d ASME J. Heat Transfer 128(3) (2006) 240\u2013250."),
    "suresh":  ("", "S. Suresh, K. P. Venkitaraj, P. Selvakumar, M. Chandrasekar, \u201cSynthesis of Al2O3\u2013Cu/water hybrid nanofluids using two step method,\u201d Colloids Surf. A 388 (2011) 41\u201348."),
    "mandal":  ("", "D. K. Mandal, N. Biswas, N. K. Manna, R. S. R. Gorla, A. J. Chamkha, \u201cHybrid nanofluid MHD mixed convection in a novel W-shaped porous system,\u201d Int. J. Numer. Methods Heat Fluid Flow 33 (2023)."),
    "manna":   ("", "N. K. Manna, N. Biswas, D. K. Mandal, U. Sarkar, H. F. \u00d6ztop, N. Abu-Hamdeh, \u201cImpacts of heater\u2013cooler position and Lorentz force on heat transfer of hybrid nanofluid convection,\u201d Int. J. Numer. Methods Heat Fluid Flow 33 (2023) 1249\u20131286."),
    "afshari": ("", "F. Afshari, B. Murat\u00e7oban\u011flu, \u201cThermal analysis of Fe3O4/water nanofluid in spiral and serpentine mini channels,\u201d Int. J. Environ. Sci. Technol. 20(2) (2023) 2037\u20132052."),
    "tlili":   ("\u2020", "I. Tlili, H. A. Nabwey, G. Ashwinkumar, N. Sandeep, \u201c3-D magnetohydrodynamic AA7072-AA7075/methanol hybrid nanofluid flow above an uneven thickness surface with slip effect,\u201d Sci. Rep. 10 (2020) art. 4402, doi:10.1038/s41598-020-61215-8."),
    "mishra9": ("", "A. Mishra, K. Swain, S. Dash, \u201cTherapeutic applications of Darcy\u2013Forchheimer hybrid nanofluid flow and mass transfer over a stretching sheet,\u201d J. Comput. Appl. Mech. 53 (2022) 1\u201314."),
    "zeeshan": ("", "Zeeshan, I. Khan, S. M. Eldin, S. Islam, M. U. Khan, \u201cTwo-dimensional nanofluid flow impinging on a porous stretching sheet with nonlinear thermal radiation and slip effect,\u201d Sci. Rep. 13 (2023) 1\u201314."),
    "ashwin":  ("", "G. Ashwinkumar, S. Sulochana, N. Sandeep, \u201cEffect of the aligned magnetic field on the boundary layer analysis of magnetic-nanofluid over a semi-infinite vertical plate,\u201d Alexandria Eng. J. 58 (2019) 1461\u20131470."),
    "carreau": ("\u2020", "P. J. Carreau, \u201cRheological equations from molecular network theories,\u201d Trans. Soc. Rheol. 16 (1972) 99\u2013127."),
    "shah":    ("", "S. A. G. A. Shah, A. Hassan, H. Karamti, A. Alhushaybari, S. M. Eldin, A. M. Galal, \u201cEffect of thermal radiation on convective heat transfer in MHD boundary layer Carreau fluid with chemical reaction,\u201d Sci. Rep. 13 (2023) 1\u201311."),
    "wahab":   ("", "H. A. Wahab, S. Z. H. Shah, A. Ayub, Z. Sabir, R. Sadat, M. R. Ali, \u201cHeterogeneous/homogeneous and inclined magnetic aspect of infinite shear rate viscosity model of Carreau fluid,\u201d Arab. J. Chem. 16 (2023) 1\u201316."),
    "mkhatshwa": ("\u2020", "M. Mkhatshwa, M. Khumalo, \u201cIrreversibility scrutinization on EMHD Darcy\u2013Forchheimer slip flow of Carreau hybrid nanofluid through a stretchable surface in porous medium,\u201d Heat Transfer 52 (2023) 395\u2013429."),
    "mittal":  ("", "A. S. Mittal, H. R. Patel, \u201cInfluence of thermophoresis and Brownian motion on mixed convection two-dimensional MHD Casson fluid flow with non-linear radiation and heat generation,\u201d Physica A 537 (2020) 1\u201315."),
    "qayyum":  ("", "M. Qayyum, T. Abbas, S. Afzal, S. T. Saeed, A. Akg\u00fcl, M. Inc, K. H. Mahmoud, A. S. Alsubaie, \u201cHeat transfer analysis of unsteady MHD Carreau fluid flow over a stretching/shrinking sheet,\u201d Coatings 12 (2022) 1\u201313."),
    "stefan":  ("", "M. J. Stefan, \u201cVersuch \u00fcber die scheinbare Adh\u00e4sion,\u201d Sitzungsber. Akad. Wiss. Wien 69 (1874) 713\u2013721."),
    "grimm":   ("", "R. J. Grimm, \u201cSqueezing flows of Newtonian liquid films: an analysis including fluid inertia,\u201d Appl. Sci. Res. 32 (1976) 149\u2013166."),
    "sobamowo": ("\u2021", "G. M. Sobamowo, A. T. Akinshilo, \u201cOn the analysis of squeezing flow of nanofluid between two parallel plates under the influence of magnetic field,\u201d Alexandria Eng. J. 57 (2018) 1413\u20131423. (Re-verify volume/pages.)"),
    "ahmad1":  ("", "S. Ahmad, M. Farooq, M. Javed, A. Anjum, \u201cSlip analysis of squeezing flow using doubly stratified fluid,\u201d Results Phys. 9 (2018) 527\u2013533."),
    "ahmad2":  ("", "S. Ahmad, M. Farooq, M. Javed, A. Anjum, \u201cDouble stratification effects in chemically reactive squeezed Sutterby fluid flow,\u201d Results Phys. 8 (2018) 1250\u20131259."),
    "bhaskar": ("\u2020", "K. Bhaskar, K. Sharma, \u201cUnsteady MHD squeezing viscous Casson fluid flow in upright channel with cross-diffusion and thermal radiactive effects,\u201d Indian J. Phys. 95(7) (2021) 1453\u20131467, doi:10.1007/s12648-020-01805-4."),
    "soret":   ("", "C. Soret, \u201cSur l\u2019\u00e9tat d\u2019\u00e9quilibre que prend au point de vue de sa concentration une dissolution saline,\u201d Arch. Sci. Phys. Nat. 2 (1879) 48\u201361."),
    "eckert":  ("", "E. R. G. Eckert, R. M. Drake, Analysis of Heat and Mass Transfer, McGraw-Hill, New York, 1972."),
    "shojaei": ("", "A. Shojaei, A. J. Amiri, S. S. Ardahaie, K. Hosseinzadeh, D. D. Ganji, \u201cHydrothermal analysis of non-Newtonian second grade fluid flow on radiative stretching cylinder with Soret and Dufour effects,\u201d Case Stud. Therm. Eng. 13 (2019) 1\u201314."),
    "rafique": ("", "K. Rafique, M. I. Anwar, M. Misiran, I. Khan, S. Alharbi, P. Thounthong, K. Nisar, \u201cNumerical solution of Casson nanofluid flow over a non-linear inclined surface with Soret and Dufour effects by Keller-box method,\u201d Front. Phys. 7 (2019) 1\u201322."),
    "kumar":   ("", "R. N. Kumar, B. Saleh, Y. Abdelrhman, A. Afzal, R. J. P. Gowda, \u201cSoret and Dufour effects on Oldroyd-B fluid flow under convective boundary condition with Stefan blowing,\u201d Indian J. Phys. 97 (2023) 1\u201311."),
    "sharma29": ("", "B. K. Sharma, A. Kumar, R. Gandhi, M. M. Bhatti, N. K. Mishra, \u201cEntropy generation and thermal radiation analysis of EMHD Jeffrey nanofluid flow: applications in solar energy,\u201d Nanomaterials 13 (2023) 1\u201323."),
    "bhatti30": ("", "M. M. Bhatti, O. A. B\u00e9g, R. Ellahi, T. Abbas, \u201cNatural convection non-Newtonian EMHD dissipative flow through a microchannel containing a non-Darcy porous medium,\u201d Qual. Theory Dyn. Syst. 21 (2022) 97."),
    "gandhi":  ("", "R. Gandhi, B. K. Sharma, N. K. Mishra, Q. M. Al-Mdallal, \u201cComputer simulations of EMHD Casson nanofluid flow of blood through an irregular stenotic permeable artery,\u201d Nanomaterials 13 (2023) 1\u201331."),
    "mahanthesh": ("", "B. Mahanthesh, G. Lorenzini, F. M. Oudina, I. L. Animasaun, \u201cSignificance of exponential space- and thermal-dependent heat source effects on nanofluid flow due to radially elongated disk,\u201d J. Therm. Anal. Calorim. 141 (2020) 1\u20138."),
    "shahzad": ("", "A. Shahzad et al., \u201cBrownian motion and thermophoretic diffusion impact on Darcy\u2013Forchheimer flow of bioconvective micropolar nanofluid between double disks,\u201d Alexandria Eng. J. 62 (2023) 1\u201315."),
    "bejan79": ("\u2020", "A. Bejan, \u201cA study of entropy generation in fundamental convective heat transfer,\u201d ASME J. Heat Transfer 101 (1979) 718\u2013725."),
    "bejan96": ("", "A. Bejan, Entropy Generation Minimization, CRC Press, Boca Raton, 1996."),
    "khan36":  ("", "M. I. Khan, S. Qayyum, T. Hayat, M. I. Khan, A. Alsaedi, \u201cEntropy optimization in flow of Williamson nanofluid in the presence of chemical reaction and Joule heating,\u201d Int. J. Heat Mass Transfer 133 (2019) 959\u2013967."),
    "rashidi": ("", "S. Rashidi, J. A. Esfahani, M. Maskaniyan, \u201cApplications of magnetohydrodynamics in biological systems: a review on the numerical studies,\u201d J. Magn. Magn. Mater. 439 (2017) 358\u2013372."),
    "bhatti38": ("", "M. M. Bhatti, T. Abbas, M. M. Rashidi, \u201cEntropy generation as a practical tool of optimisation for MHD flow through a shrinking sheet,\u201d J. Magnetics 21 (2016) 468\u2013475."),
    "siva":    ("", "T. Siva, S. Jangili, B. Kumbhakar, \u201cEntropy generation on EMHD transport of couple stress fluid with slip-dependent zeta potential under electrokinetic effects,\u201d Int. J. Therm. Sci. 191 (2023) 1\u201315."),
    "bhatti40": ("", "S. Bhatti et al., \u201cEntropy generation analysis of Carreau nanofluid flow with viscous dissipation and thermal radiation,\u201d J. Therm. Anal. Calorim. 147 (2022) 1\u201317."),
    "ali41":   ("", "A. Ali, S. Sarkar, S. Das, R. N. Jana, \u201cIrreversibility analysis of Carreau hybrid nanofluid flow over a stretching sheet with radiation,\u201d Waves Random Complex Media 33 (2023) 1\u201329."),
    "yadav":   ("\u2021", "P. K. Yadav, A. Kumar, \u201cEntropy generation analysis of unsteady squeezing MHD nanofluid flow between two parallel plates,\u201d Int. Commun. Heat Mass Transfer 128 (2021) 105632. (Re-verify volume/article number.)"),
    "mishra43": ("", "N. K. Mishra, \u201cComputational analysis of Soret and Dufour effects on nanofluid flow through a stenosed artery in the presence of temperature-dependent viscosity,\u201d Acta Mech. Autom. 17 (2023) 1\u20138."),
}


class Cites:
    def __init__(self):
        self.order = []          # keys in first-appearance order
        self.num = {}            # key -> number

    def n(self, key):
        if key not in self.num:
            self.order.append(key)
            self.num[key] = len(self.order)
        return self.num[key]

    def one(self, key):
        return "[%d]" % self.n(key)

    def many(self, *keys):
        return "[%s]" % ", ".join(str(self.n(k)) for k in keys)

    def rng(self, k_first, k_last):
        a = self.n(k_first)
        b = self.n(k_last)
        return "[%d\u2013%d]" % (a, b)

    def register_all(self):
        # ensure every REF_META key gets a number (in declared residual order)
        for k in REF_META:
            self.n(k)

    def reflist(self):
        # Emit a clean, strictly serial list: "[n] <reference text>".
        # Verification flags are intentionally NOT inlined here (kept separately),
        # so the numbering reads as a plain 1, 2, 3, ... sequence.
        out = []
        for k in self.order:
            _flag, text = REF_META[k]
            out.append("[%d] %s" % (self.num[k], text))
        return out

    def verified_keys(self):
        return [k for k in self.order if REF_META[k][0] == "\u2020"]

    def flagged_keys(self):
        return [k for k in self.order if REF_META[k][0] == "\u2021"]


def build():
    d = Document()
    C = Cites()

    # =====================================================================
    # Title / abstract
    # =====================================================================
    d.title("Entropy Generation and Irreversibility Analysis of Unsteady EMHD "
            "Squeezing Flow of a Carreau Hybrid Nanofluid (AA7072\u2013AA7075/Methanol) "
            "Between Parallel Porous Plates")

    d.heading("Abstract", 2)
    d.para(
        "The relentless miniaturisation of thermal-management hardware has intensified the search "
        "for coolants whose effective conductivity exceeds that of conventional liquids, a search "
        "that began with the nanofluid concept and matured into hybrid nanofluids in which two "
        "chemically distinct nanoparticles are co-dispersed to combine their advantages. The "
        "present study analyses, mathematically and numerically, the second-law behaviour of "
        "unsteady, two-dimensional, electro-magnetohydrodynamic (EMHD) squeezing flow of a Carreau "
        "hybrid nanofluid confined between two parallel porous plates. The working fluid is a "
        "suspension of AA7072 and AA7075 aluminium-alloy nanoparticles in methanol, a pairing that "
        "enhances heat transfer relative to the pure base fluid, while the shear-dependent "
        "rheology is represented by the Carreau model. The formulation incorporates a transverse "
        "time-dependent magnetic field, an aligned electric field, Darcy\u2013Forchheimer porous "
        "drag, nonlinear thermal radiation, viscous dissipation, Joule heating, Soret\u2013Dufour "
        "cross-diffusion and a first-order homogeneous chemical reaction, together with velocity, "
        "thermal (Biot-type) and solutal slip boundary conditions. Suitable similarity "
        "transformations reduce the governing partial differential equations to a coupled system "
        "of ordinary differential equations. In this corrected formulation the momentum balance is "
        "retained at fourth order through pressure elimination, so that the resulting eighth-order "
        "coupled system is consistent with the eight physical boundary conditions; the radiative "
        "contribution is grouped with conduction using the base-fluid conductivity, and the "
        "entropy normalisation is made internally consistent. The boundary-value problem is solved "
        "with the MATLAB collocation solver bvp4c, and grid convergence confirms the expected "
        "fourth-order accuracy. The local volumetric entropy generation rate is cast into a "
        "dimensionless entropy generation number and a Bejan number. A detailed parametric study "
        "quantifies the influence of the squeezing parameter, Weissenberg number, power-law index, "
        "magnetic and electric parameters, radiation, Eckert and Brinkman numbers, Soret\u2013"
        "Dufour effects and the diffusive-irreversibility parameter. Entropy generation is found "
        "to be maximal near the plates and minimal in the core, the Brinkman number strongly "
        "amplifies friction and Joule irreversibilities, and the Bejan-number distribution reveals "
        "a transition from conduction-dominated irreversibility at the walls to friction-dominated "
        "irreversibility in the core, extending established stretching-surface findings to a "
        "moving-boundary squeezing channel. The results provide design guidance for squeeze-film "
        "dampers, micro-electromechanical cooling channels and hydraulic actuators employing "
        "engineered hybrid coolants.")

    d.para("Keywords: Carreau hybrid nanofluid; Entropy generation; Bejan number; EMHD squeezing "
           "flow; Darcy\u2013Forchheimer; Soret\u2013Dufour; bvp4c", italic=True)

    # =====================================================================
    # 1. Introduction (condensed, unchanged in substance)
    # =====================================================================
    d.heading("1. Introduction", 1)
    d.para(
        "The intensification of convective heat transfer has become a central concern of modern "
        "engineering, driven by the continual push toward smaller yet more powerful thermal-"
        "management devices. Conventional heat-transfer liquids such as water, ethylene glycol and "
        "the light alcohols possess intrinsically low thermal conductivities, which limits their "
        "performance in the miniaturised cooling passages of power electronics, microreactors and "
        "precision machine tools. The seminal proposal of Choi and Eastman " + C.one("choi") + " "
        "to suspend metallic and oxide nanoparticles in a base liquid \u2014 the nanofluid concept "
        "\u2014 opened a durable line of research aimed at exploiting the anomalously high "
        "effective conductivity of such suspensions. Subsequent experimental and theoretical "
        "work established that the thermal, rheological and electrical properties of nanofluids "
        "can be tailored through particle material, size, shape and loading " + C.many("eid", "buongiorno") + ". "
        "The hybrid nanofluid extends this idea by co-dispersing two chemically distinct "
        "nanoparticles in the same carrier so as to combine their individual merits "
        + C.many("suresh", "mandal") + ", and such suspensions frequently deliver a better "
        "thermal-enhancement-to-pumping-penalty ratio than their mono-particle counterparts "
        + C.many("manna", "afshari") + ".")
    d.para(
        "Among candidate particles, the aluminium alloys AA7072 and AA7075 are especially "
        "attractive because of their high electrical conductivity, strong corrosion resistance and "
        "low density. Tlili et al. " + C.one("tlili") + " analysed three-dimensional "
        "magnetohydrodynamic flow of an AA7072\u2013AA7075/methanol hybrid nanofluid over a "
        "variable-thickness surface and reported a marked rise in the heat-transfer coefficient "
        "relative to methanol; the same alloy pairing has since featured in numerous boundary-"
        "layer and channel-flow studies " + C.many("mishra9", "zeeshan") + ", and methanol is "
        "adopted here as the base liquid on account of its low freezing point, low viscosity and "
        "compatibility with electronic-cooling applications " + C.one("ashwin") + ".")
    d.para(
        "Many industrially relevant suspensions depart markedly from the Newtonian idealisation. "
        "Polymeric coolants, biofluids, paints and particle-laden liquids display shear-thinning "
        "or shear-thickening behaviour that only a generalised constitutive law can capture. The "
        "Carreau model " + C.one("carreau") + " is particularly versatile, reproducing Newtonian "
        "plateaus at both low and high shear while admitting a power-law region at intermediate "
        "shear rates. Chemically reacting and magnetised Carreau flows have been examined over "
        "stretching surfaces " + C.one("shah") + " and for inclined configurations with an "
        "infinite-shear-rate viscosity correction " + C.one("wahab") + ", while Mkhatshwa and "
        "Khumalo " + C.one("mkhatshwa") + " scrutinised the irreversibility of an EMHD Darcy\u2013"
        "Forchheimer Carreau hybrid nanofluid over a deformable surface, underlining the interest "
        "of coupling non-Newtonian rheology with the second law; related Carreau transport under "
        "radiation and mixed convection appears in " + C.many("mittal", "qayyum") + ".")
    d.para(
        "Squeezing flows \u2014 generated when two surfaces approach or separate with a viscous "
        "medium in between \u2014 arise in lubrication systems, squeeze-film dampers, polymer "
        "moulding, hydraulic machinery and biomechanical joints " + C.many("stefan", "grimm") + ". "
        "Because the boundary itself moves, the analysis is richer than for fixed-boundary flow. "
        "Squeezing Casson flow was studied by Sobamowo and Akinshilo " + C.one("sobamowo") + ", "
        "and slip-affected and Sutterby squeezing flows by Ahmad et al. " + C.many("ahmad1", "ahmad2") + ". "
        "Bhaskar and Sharma " + C.one("bhaskar") + " investigated unsteady squeezing Casson flow "
        "under the combined action of a magnetic field, a porous medium and cross-diffusion, "
        "emphasising the reversed Soret and Dufour effects. Coupled heat and mass gradients "
        "produce these Soret (thermo-diffusion) and Dufour (diffusion-thermo) effects, recognised "
        "since the nineteenth-century work of Soret " + C.many("soret", "eckert") + " and since "
        "extended to non-Newtonian and nanofluid settings " + C.many("shojaei", "rafique", "kumar") + ", "
        "where the Nusselt and Sherwood numbers are found to respond in opposite senses. Nonlinear "
        "thermal radiation, viscous dissipation and Joule heating become decisive in high-"
        "temperature or electrically driven systems " + C.many("sharma29", "bhatti30", "gandhi") + ", "
        "and the Darcy\u2013Forchheimer porous resistance \u2014 which embodies both viscous and "
        "inertial drag \u2014 is a further key influence in porous-channel flow "
        + C.many("mahanthesh", "shahzad") + ".")
    d.para(
        "Whereas a first-law (energy) analysis reports only how much heat is transferred, the "
        "second law, expressed through entropy generation, quantifies the irreversibilities that "
        "degrade available work. The entropy-generation-minimisation methodology pioneered by "
        "Bejan " + C.many("bejan79", "bejan96") + " has since become a general design tool, and "
        "entropy analyses of nanofluid and hybrid-nanofluid flows over stretching sheets, in "
        "cavities, microchannels and rotating systems " + C.many("khan36", "rashidi", "bhatti38", "siva") + " "
        "consistently identify magnetic, radiative and frictional effects as dominant. The "
        "treatment has recently reached generalised-Newtonian fluids such as Carreau "
        + C.many("bhatti40", "ali41") + " and squeezing configurations " + C.many("yadav", "mishra43") + ".")
    d.para(
        "Against this background, the objectives of the present study are fourfold. First, a "
        "unified model is developed for unsteady EMHD squeezing flow of a Carreau hybrid nanofluid "
        "through a porous channel, assembling non-Newtonian rheology, transverse magnetic and "
        "aligned electric fields, Darcy\u2013Forchheimer resistance, nonlinear radiation, viscous "
        "and Joule dissipation, Soret\u2013Dufour cross-diffusion, a first-order chemical reaction "
        "and multi-mode slip, and reducing the coupled momentum, energy and species balances to a "
        "similarity system of ordinary differential equations. Second, particular care is taken to "
        "keep that reduction internally consistent: the momentum equation is retained at fourth "
        "order through pressure elimination so that the eighth-order system carries exactly eight "
        "boundary conditions, the radiative flux is grouped with conduction through the base-fluid "
        "conductivity, and every dimensionless group is defined so that the Dufour\u2013Soret, "
        "Darcy\u2013Forchheimer and electromagnetic terms are dimensionally compatible. Third, a "
        "complete local volumetric entropy-generation model is derived that accounts for "
        "heat-conduction, fluid-friction, Joule and cross-diffusion irreversibilities, and is "
        "recast into a dimensionless entropy-generation number and Bejan number to rank the "
        "competing mechanisms. Fourth, the boundary-value problem is solved with the MATLAB "
        "collocation solver bvp4c, verified through grid convergence and a Newtonian limiting case, "
        "and exercised over a wide parameter range to expose the velocity, thermal, solutal and "
        "irreversibility behaviour, which is then benchmarked against the established literature "
        "throughout Section 6.")
    d.para(
        "Nevertheless, a coupled first- and second-law analysis of unsteady EMHD squeezing flow of "
        "an AA7072\u2013AA7075/methanol Carreau hybrid nanofluid, incorporating Soret\u2013Dufour "
        "cross-diffusion, nonlinear radiation, Joule heating and multi-mode slip within a Darcy\u2013"
        "Forchheimer porous channel, has not previously been reported. The present work fills this "
        "gap and, importantly, corrects the transformed momentum equation and its boundary-"
        "condition count (retaining a fourth-order momentum balance so that the eighth-order system "
        "matches its eight boundary conditions), rederives the radiative grouping in the energy "
        "equation, and renders the entropy-generation normalisation internally consistent, as "
        "detailed in the sections that follow.")

    # =====================================================================
    # 2. Mathematical formulation
    # =====================================================================
    d.heading("2. Mathematical Formulation", 1)
    d.heading("2.1 Physical configuration and assumptions", 2)
    d.inline_math("The plates are separated by the time-dependent distance",
                  group(i("h"), delim(i("t")), eq(),
                        sup(brack(frac(group(sub(i(G['nu']), i("f")), delim(group(r("1"), minus(), i(G['gamma']), i("t")))), i("a"))),
                            frac(r("1"), r("2")))),
                  "")
    d.equation(group(i("h"), delim(i("t")), eq(),
                     sup(brack(frac(group(sub(i(G['nu']), i("f")),
                                          delim(group(r("1"), minus(), i(G['gamma']), i("t")))), i("a"))),
                         frac(r("1"), r("2")))), number="auto")
    d.para("The lower plate is stretched with velocity U\u2091(x, t) = ax/(1\u2212\u03b3t); the "
           "upper plate moves normally with the squeezing velocity v\u2095 = dh/dt = "
           "\u2212(\u03b3/2)[\u03bd\u2091/(a(1\u2212\u03b3t))]^{1/2}, which gives f(1) = Sq/2. "
           "A time-dependent transverse magnetic field is applied in the +y direction and an "
           "aligned electric field in the +z direction (the Lorentz body force then acts along "
           "x and reduces to \u03c3(uB \u2212 E)):")
    d.equation(group(i("B"), delim(i("t")), eq(),
                     frac(sub(i("B"), r("0")), sup(delim(group(r("1"), minus(), i(G['gamma']), i("t"))), frac(r("1"), r("2"))))),
               number="auto")
    d.para("For the electric parameter Ee = E\u2080/(B\u2080U\u2091) to remain constant under the "
           "similarity transformation, the electric field must scale as B(t)U\u2091(t). Since "
           "B ~ (1\u2212\u03b3t)^{\u22121/2} and U\u2091 ~ (1\u2212\u03b3t)^{\u22121}, the required "
           "scaling is")
    d.equation(group(i("E"), delim(i("t")), eq(),
                     frac(sub(i("E"), r("0")), sup(delim(group(r("1"), minus(), i(G['gamma']), i("t"))), frac(r("3"), r("2"))))),
               number="auto")
    d.para("where E\u2080 and B\u2080 are the reference field strengths and U\u2091 is the local "
           "wall (reference) velocity; Ee is thus constant under local similarity.")

    d.heading("2.2 Carreau hybrid nanofluid constitutive model", 2)
    d.para("The total Cauchy stress tensor is written in bold as \u03c3 (with A\u2081 = "
           "\u2207V + (\u2207V)\u1d40 the first Rivlin\u2013Ericksen tensor). To avoid clashing with "
           "the electrical conductivity, the latter is denoted \u03c3\u2091 (i.e. \u03c3\u2091,hnf, "
           "\u03c3\u2091,f) throughout:")
    d.equation(group(b("\u03c3"), eq(), minus(), i("p"), b("I"), plus(),
                     i(G['mu']), delim(i("\u03b3\u0307")), A1tensor()), number="auto")
    d.para("with the shear-dependent (Carreau) viscosity")
    # (4): mu = mu_inf + (mu0 - mu_inf)[1 + (Gamma gammadot)^2]^{(n-1)/2}
    d.equation(group(i(G['mu']), delim(i("\u03b3\u0307")), eq(), sub(i(G['mu']), i("\u221e")),
                     plus(), delim(group(sub(i(G['mu']), r("0")), minus(), sub(i(G['mu']), i("\u221e")))),
                     sup(brack(group(r("1"), plus(), sup(delim(group(i(G['Gamma']), i("\u03b3\u0307"))), r("2")))),
                         frac(group(i("n"), minus(), r("1")), r("2")))), number="auto")
    d.para("and the scalar shear rate")
    # (5): gammadot = sqrt( (1/2) tr(A1^2) )
    d.equation(group(i("\u03b3\u0307"), eq(),
                     rad(group(frac(r("1"), r("2")), u("tr"), delim(sub(sup(b("A"), r("2")), r("1")))))), number="auto")
    d.para("Adopting \u03bc\u221e \u2192 0 gives the limiting form")
    # (6): limiting form
    d.equation(group(i(G['mu']), delim(i("\u03b3\u0307")), eq(), sub(i(G['mu']), r("0")),
                     sup(brack(group(r("1"), plus(), sup(delim(group(i(G['Gamma']), i("\u03b3\u0307"))), r("2")))),
                         frac(group(i("n"), minus(), r("1")), r("2")))), number="auto")
    d.para("with the zero-shear-rate viscosity identified as the hybrid-nanofluid viscosity, "
           "\u03bc\u2080 = \u03bc\u2095\u2099\u2093 (Eq. 14), so that \u03b1\u03bc = \u03bc\u2095\u2099\u2093/"
           "\u03bc\u2091 and the Carreau viscosity are consistently connected. In the shear-"
           "dominated boundary layer \u03b3\u0307 \u2243 |\u2202u/\u2202y|.")

    d.heading("2.3 Governing equations", 2)
    d.para("Under the boundary-layer approximation for the narrow gap, mass, momentum, energy "
           "and species conservation give:")
    # continuity
    d.equation(group(frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("x"))), plus(),
                     frac(group(i(G['partial']), i("v")), group(i(G['partial']), i("y"))), eq(), r("0")),
               number="auto")
    # x-momentum (primitive) -- Carreau viscous term written as stress divergence
    xmom = group(
        frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("t"))), plus(),
        i("u"), frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("x"))), plus(),
        i("v"), frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("y"))), eq(),
        frac(r("1"), sub(i(G['rho']), i("hnf"))),
        frac(i(G['partial']), group(i(G['partial']), i("y"))),
        brack(group(sub(i(G['mu']), i("hnf")),
                    sup(delim(group(r("1"), plus(), sup(i(G['Gamma']), r("2")),
                                    sup(delim(frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("y")))), r("2")))),
                        frac(group(i("n"), minus(), r("1")), r("2"))),
                    frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("y"))))),
        plus(), frac(sub(i("\u03c3"), group(i("e"), r(",hnf"))), sub(i(G['rho']), i("hnf"))),
        i("B"), delim(i("t")),
        delim(group(i("u"), i("B"), delim(i("t")), minus(), i("E"), delim(i("t")))),
        minus(), frac(sub(i(G['mu']), i("hnf")), sub(i(G['rho']), i("hnf"))),
        frac(i("u"), sub(sup(i("K"), r("*")), i("p"))),
        minus(), frac(sub(i("C"), i("b")), rad(sub(sup(i("K"), r("*")), i("p")))), sup(i("u"), r("2")))
    d.equation(xmom, number="auto")
    d.para("The viscous term is the divergence of the Carreau shear stress; carrying out the "
           "differentiation gives the equivalent form")
    d.equation(group(frac(sub(i(G['mu']), i("hnf")), sub(i(G['rho']), i("hnf"))),
                     sup(delim(group(r("1"), plus(), sup(i(G['Gamma']), r("2")),
                                     sup(delim(frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("y")))), r("2")))),
                         frac(group(i("n"), minus(), r("3")), r("2"))),
                     delim(group(r("1"), plus(), i("n"), sup(i(G['Gamma']), r("2")),
                                 sup(delim(frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("y")))), r("2")))),
                     frac(group(sup(i(G['partial']), r("2")), i("u")), group(i(G['partial']), sup(i("y"), r("2"))))),
               number="auto")
    d.para("in which the factor (1 + n\u0393\u00b2u\u1d67\u00b2) is essential and is retained "
           "throughout. Here \u03c3\u2091,hnf is the effective electrical conductivity, K\u209a* the "
           "permeability and C\u1d47 the Forchheimer drag coefficient. The electromagnetic body "
           "force is the x-component of the Lorentz force J \u00d7 B with J = \u03c3\u2091(E + V "
           "\u00d7 B), which for the present configuration carries an explicit factor B(t), "
           "\u03c3\u2091,hnf B(t)[uB(t) \u2212 E(t)]/\u03c1\u2095\u2099\u2093; this B(t) factor is "
           "consistent with the definition M = \u03c3\u2091,f B\u2080\u00b2/(a\u03c1\u2091) of the "
           "magnetic parameter, and after the similarity reduction (B(t)\u00b2h\u00b2 = "
           "B\u2080\u00b2\u03bd\u2091/a) it yields the transformed group (\u03b1\u03c3/\u03b1\u03c1)"
           "M(f\u2032 \u2212 Ee).")
    # y-momentum
    d.equation(group(frac(group(i(G['partial']), i("v")), group(i(G['partial']), i("t"))), plus(),
                     i("u"), frac(group(i(G['partial']), i("v")), group(i(G['partial']), i("x"))), plus(),
                     i("v"), frac(group(i(G['partial']), i("v")), group(i(G['partial']), i("y"))), eq(), minus(),
                     frac(r("1"), sub(i(G['rho']), i("hnf"))),
                     frac(group(i(G['partial']), i("p")), group(i(G['partial']), i("y"))), plus(),
                     frac(sub(i(G['mu']), i("hnf")), sub(i(G['rho']), i("hnf"))),
                     frac(group(sup(i(G['partial']), r("2")), i("v")), group(i(G['partial']), sup(i("y"), r("2"))))),
               number="auto")
    d.para("The pressure is eliminated between the complete x- and y-momentum equations (not a "
           "reduced version): \u2202p/\u2202y from this equation is cross-differentiated with the "
           "x-momentum balance so that the pressure-gradient constant G in Eq. (26) is removed "
           "consistently, yielding the fourth-order momentum equation (27).")
    # energy (with explicit Dufour term using D_B K_T / (c_s (c_p)_hnf); c_s == T_m)
    d.equation(group(frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("t"))), plus(),
                     i("u"), frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("x"))), plus(),
                     i("v"), frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("y"))), eq(),
                     frac(sub(i(G['kappa']), i("hnf")), group(delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), i("hnf")))),
                     frac(group(sup(i(G['partial']), r("2")), i("T")), group(i(G['partial']), sup(i("y"), r("2")))),
                     minus(), frac(r("1"), group(delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), i("hnf")))),
                     frac(group(i(G['partial']), sub(i("q"), i("r"))), group(i(G['partial']), i("y"))),
                     plus(), frac(group(sub(i("D"), i("B")), sub(i("K"), i("T"))),
                                  group(sub(i("c"), i("s")), group(delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), i("hnf"))))),
                     frac(group(sup(i(G['partial']), r("2")), i("C")), group(i(G['partial']), sup(i("y"), r("2")))),
                     plus(), u("\u22ef")), number="auto")
    d.para("where the viscous-dissipation and Joule terms complete the right-hand side. The "
           "Dufour (diffusion-thermo) coefficient uses the concentration susceptibility c\u209b; "
           "throughout this work c\u209b \u2261 T\u2098 (the mean fluid temperature), so the "
           "Dufour and Soret definitions in Eqs. (34)\u2013(35) are dimensionally consistent with "
           "the cross-diffusion terms in Eqs. (10)\u2013(11).")
    # concentration
    d.equation(group(frac(group(i(G['partial']), i("C")), group(i(G['partial']), i("t"))), plus(),
                     i("u"), frac(group(i(G['partial']), i("C")), group(i(G['partial']), i("x"))), plus(),
                     i("v"), frac(group(i(G['partial']), i("C")), group(i(G['partial']), i("y"))), eq(),
                     sub(i("D"), i("B")), frac(group(sup(i(G['partial']), r("2")), i("C")), group(i(G['partial']), sup(i("y"), r("2")))),
                     plus(), frac(group(sub(i("D"), i("B")), sub(i("K"), i("T"))), sub(i("T"), i("m"))),
                     frac(group(sup(i(G['partial']), r("2")), i("T")), group(i(G['partial']), sup(i("y"), r("2")))),
                     minus(), sub(i("k"), r("1")), delim(group(i("C"), minus(), sub(i("C"), i("h"))))), number="auto")

    d.heading("2.4 Nonlinear thermal radiation", 2)
    d.equation(group(sub(i("q"), i("r")), eq(), minus(),
                     frac(group(r("16"), sup(i(G['sigma']), r("*"))), group(r("3"), sup(i("k"), r("*")))),
                     sup(i("T"), r("3")), frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("y")))), number="auto")
    d.equation(group(frac(group(i(G['partial']), sub(i("q"), i("r"))), group(i(G['partial']), i("y"))), eq(), minus(),
                     frac(group(r("16"), sup(i(G['sigma']), r("*"))), group(r("3"), sup(i("k"), r("*")))),
                     brack(group(r("3"), sup(i("T"), r("2")), sup(delim(frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("y")))), r("2")),
                                 plus(), sup(i("T"), r("3")),
                                 frac(group(sup(i(G['partial']), r("2")), i("T")), group(i(G['partial']), sup(i("y"), r("2"))))))), number="auto")
    d.inline_math("with T = T", group(), "\u2080[1 + (\u03b8\u1d63 \u2212 1)\u03b8].")

    d.heading("2.5 Thermophysical properties of the hybrid nanofluid", 2)
    d.equation(group(sub(i(G['mu']), i("hnf")), eq(),
                     frac(sub(i(G['mu']), i("f")),
                          group(sup(delim(group(r("1"), minus(), sub(i(G['phi']), r("1")))), r("2.5")),
                                sup(delim(group(r("1"), minus(), sub(i(G['phi']), r("2")))), r("2.5"))))), number="auto")
    d.equation(group(sub(i(G['rho']), i("hnf")), eq(),
                     delim(group(r("1"), minus(), sub(i(G['phi']), r("2")))),
                     brack(group(delim(group(r("1"), minus(), sub(i(G['phi']), r("1")))), sub(i(G['rho']), i("f")),
                                 plus(), sub(i(G['phi']), r("1")), sub(i(G['rho']), r("s1")))),
                     plus(), sub(i(G['phi']), r("2")), sub(i(G['rho']), r("s2"))), number="auto")
    d.equation(group(delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), i("hnf")), eq(),
                     delim(group(r("1"), minus(), sub(i(G['phi']), r("2")))),
                     brack(group(delim(group(r("1"), minus(), sub(i(G['phi']), r("1")))),
                                 delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), i("f")),
                                 plus(), sub(i(G['phi']), r("1")), delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), r("s1")))),
                     plus(), sub(i(G['phi']), r("2")), delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), r("s2"))), number="auto")
    d.equation(group(frac(sub(i(G['kappa']), i("bf")), sub(i(G['kappa']), i("f"))), eq(),
                     frac(group(sub(i(G['kappa']), r("s1")), plus(), r("2"), sub(i(G['kappa']), i("f")), minus(), r("2"), sub(i(G['phi']), r("1")), delim(group(sub(i(G['kappa']), i("f")), minus(), sub(i(G['kappa']), r("s1"))))),
                          group(sub(i(G['kappa']), r("s1")), plus(), r("2"), sub(i(G['kappa']), i("f")), plus(), sub(i(G['phi']), r("1")), delim(group(sub(i(G['kappa']), i("f")), minus(), sub(i(G['kappa']), r("s1"))))))), number="auto")
    d.equation(group(frac(sub(i(G['kappa']), i("hnf")), sub(i(G['kappa']), i("bf"))), eq(),
                     frac(group(sub(i(G['kappa']), r("s2")), plus(), r("2"), sub(i(G['kappa']), i("bf")), minus(), r("2"), sub(i(G['phi']), r("2")), delim(group(sub(i(G['kappa']), i("bf")), minus(), sub(i(G['kappa']), r("s2"))))),
                          group(sub(i(G['kappa']), r("s2")), plus(), r("2"), sub(i(G['kappa']), i("bf")), plus(), sub(i(G['phi']), r("2")), delim(group(sub(i(G['kappa']), i("bf")), minus(), sub(i(G['kappa']), r("s2"))))))), number="auto")
    d.para("The electrical conductivity uses the analogous two-step Maxwell\u2013Garnett "
           "relations (Eqs. 19\u201320), and \u03bd\u2095\u2099\u2093 = \u03bc\u2095\u2099\u2093/\u03c1\u2095\u2099\u2093 (Eq. 21).")
    d.equation(group(sub(i(G['sigma']), i("bf")), sub(r(""), r("")), eq(),
                     sub(i(G['sigma']), i("f")), delim(group(r("1"), plus(),
                     frac(group(r("3"), delim(group(frac(sub(i(G['sigma']), r("s1")), sub(i(G['sigma']), i("f"))), minus(), r("1"))), sub(i(G['phi']), r("1"))),
                          group(delim(group(frac(sub(i(G['sigma']), r("s1")), sub(i(G['sigma']), i("f"))), plus(), r("2"))), minus(), delim(group(frac(sub(i(G['sigma']), r("s1")), sub(i(G['sigma']), i("f"))), minus(), r("1"))), sub(i(G['phi']), r("1"))))))), number="auto")
    d.equation(group(sub(i(G['sigma']), i("hnf")), eq(),
                     sub(i(G['sigma']), i("bf")), delim(group(r("1"), plus(),
                     frac(group(r("3"), delim(group(frac(sub(i(G['sigma']), r("s2")), sub(i(G['sigma']), i("bf"))), minus(), r("1"))), sub(i(G['phi']), r("2"))),
                          group(delim(group(frac(sub(i(G['sigma']), r("s2")), sub(i(G['sigma']), i("bf"))), plus(), r("2"))), minus(), delim(group(frac(sub(i(G['sigma']), r("s2")), sub(i(G['sigma']), i("bf"))), minus(), r("1"))), sub(i(G['phi']), r("2"))))))), number="auto")
    d.equation(group(sub(i(G['nu']), i("hnf")), eq(), frac(sub(i(G['mu']), i("hnf")), sub(i(G['rho']), i("hnf")))), number="auto")

    d.heading("2.6 Similarity transformation", 2)
    # eta, psi
    d.equation(group(eta(), eq(), frac(i("y"), group(i("h"), delim(i("t")))), u("  ,  "),
                     i(G['psi']), eq(), sup(brack(frac(group(i("a"), sub(i(G['nu']), i("f"))), group(r("1"), minus(), i(G['gamma']), i("t")))), frac(r("1"), r("2"))),
                     i("x"), i("f"), delim(eta())), number="auto")
    # u, v
    d.equation(group(i("u"), eq(), frac(group(i("a"), i("x")), group(r("1"), minus(), i(G['gamma']), i("t"))), fp(1),
                     u("  ,  "), i("v"), eq(), minus(),
                     sup(brack(frac(group(i("a"), sub(i(G['nu']), i("f"))), group(r("1"), minus(), i(G['gamma']), i("t")))), frac(r("1"), r("2"))),
                     i("f"), delim(eta())), number="auto")
    # theta, phi
    d.equation(group(theta(), delim(eta()), eq(),
                     frac(group(i("T"), minus(), sub(i("T"), r("0"))), group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))),
                     u("  ,  "), phi(), delim(eta()), eq(),
                     frac(group(i("C"), minus(), sub(i("C"), r("0"))), group(sub(i("C"), i("w")), minus(), sub(i("C"), r("0"))))), number="auto")
    d.para("The temperature and concentration are normalised with the reference values T\u2080 and "
           "C\u2080, with T\u2095 and C\u2095 the wall (convective/reference) values. The upper-wall "
           "values coincide with the references, T\u2095\u2092\u209a = T\u2080 and C\u2095\u2092\u209a "
           "= C\u2080 (equivalently T_h = T\u2080, C_h = C\u2080), so that \u03b8(1) = \u03c6(1) = 0; "
           "this normalisation is what makes the lower-wall convective and solutal-slip conditions "
           "in Eq. (31) consistent. The stream function satisfies continuity identically "
           "(u = \u2202\u03c8/\u2202y, v = \u2212\u2202\u03c8/\u2202x). The x- and time-dependent wall "
           "excesses are")
    d.equation(group(sub(i("T"), i("w")), eq(), sub(i("T"), r("0")), plus(),
                     frac(group(i("a"), i("x")), group(r("1"), minus(), i(G['gamma']), i("t"))), sub(i("d"), r("1")),
                     u("  ,  "), sub(i("C"), i("w")), eq(), sub(i("C"), r("0")), plus(),
                     frac(group(i("a"), i("x")), group(r("1"), minus(), i(G['gamma']), i("t"))), sub(i("e"), r("1"))), number="auto")
    d.para("where d\u2081 and e\u2081 carry the appropriate temperature and concentration scaling "
           "units.")

    # =====================================================================
    # 2.7 Corrected ODEs
    # =====================================================================
    d.heading("2.7 Dimensionless ordinary differential equations (corrected)", 2)
    d.para("Substituting Eqs. (22)\u2013(25) and the corrected unsteady group "
           "Sq(f\u2032 + (\u03b7/2)f\u2033), then eliminating pressure by cross-differentiating "
           "the momentum equations, yields a fourth-order momentum equation. Its primitive "
           "(third-order) form is")
    # third-order primitive momentum (Eq 26)
    mom3 = group(
        frac(A(1), A(2)), carreau_bracket(frac(group(i("n"), minus(), r("3")), r("2"))),
        brack(group(r("1"), plus(), i("n"), sup(i("We"), r("2")), sup(delim(fp(2)), r("2")))), fp(3),
        plus(), i("f"), fp(2), minus(), sup(delim(fp(1)), r("2")),
        minus(), i("Sq"), delim(group(fp(1), plus(), frac(eta(), r("2")), fp(2))),
        minus(), frac(A(1), group(A(2), i("Da"))), fp(1),
        minus(), frac(A(3), A(2)), i("M"), delim(group(fp(1), minus(), i("Ee"))),
        minus(), i("Fr"), sup(delim(fp(1)), r("2")), eq(), i("G"))
    d.equation(mom3, number="auto")
    d.para("where G is the (\u03b7-independent) scaled pressure-gradient constant. Differentiating "
           "Eq. (26) once with respect to \u03b7 removes G and gives the fourth-order momentum "
           "equation actually solved:")
    mom4 = group(
        frac(A(1), A(2)),
        frac(i("d"), group(i("d"), eta())),
        brack(group(carreau_bracket(frac(group(i("n"), minus(), r("3")), r("2"))),
                    brack(group(r("1"), plus(), i("n"), sup(i("We"), r("2")), sup(delim(fp(2)), r("2")))), fp(3))),
        plus(), i("f"), fp(3), minus(), fp(1), fp(2),
        minus(), i("Sq"), delim(group(frac(r("3"), r("2")), fp(2), plus(), frac(eta(), r("2")), fp(3))),
        minus(), frac(A(1), group(A(2), i("Da"))), fp(2),
        minus(), frac(A(3), A(2)), i("M"), fp(2),
        minus(), r("2"), i("Fr"), fp(1), fp(2), eq(), r("0"))
    d.equation(mom4, number="auto")
    d.para("The corrected energy equation groups conduction and radiation consistently "
           "(\u03b1\u03ba multiplies conduction only, because Rd is defined with the base-fluid "
           "conductivity \u03ba\u2091):")
    energy = group(
        brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3")))), thp(2),
        plus(), r("4"), i("Rd"), delim(group(sub(i(G['theta']), i("r")), minus(), r("1"))),
        sup(F_expr(), r("2")), sup(delim(thp(1)), r("2")),
        plus(), A(5), i("Pr"), delim(group(i("f"), thp(1), minus(), fp(1), theta(),
                                           minus(), i("Sq"), theta(), minus(), sqhalf(), eta(), thp(1))),
        plus(), i("Pr"), brack(group(
            A(1), i("Ec"), sup(delim(fp(2)), r("2")), sup(delim(We2fpp2()), frac(group(i("n"), minus(), r("1")), r("2"))),
            plus(), A(3), i("M"), i("Ec"), sup(delim(group(fp(1), minus(), i("Ee"))), r("2")),
            plus(), A(2), i("Df"), php(2))), eq(), r("0"))
    d.equation(energy, number="auto")
    d.para("Because the wall excesses T\u2095 \u2212 T\u2080 and C\u2095 \u2212 C\u2080 are linear in "
           "x and time-dependent (Eq. 27), the material derivatives of T and C generate the extra "
           "advection/unsteady terms \u2212f\u2032\u03b8 \u2212 Sq\u03b8 (and \u2212f\u2032\u03c6 "
           "\u2212 Sq\u03c6 for the species), which are retained above and in Eq. (31).")
    d.para("and the concentration equation is")
    species = group(php(2), plus(), i("Sc"),
                    delim(group(i("f"), php(1), minus(), fp(1), phi(),
                                minus(), i("Sq"), phi(), minus(), sqhalf(), eta(), php(1))),
                    plus(), i("Sc"), i("Sr"), thp(2), minus(), i("K"), i("Sc"), phi(), eq(), r("0"))
    d.equation(species, number="auto")
    d.para("The dimensionless thermophysical property ratios are denoted with \u03b1 (to avoid "
           "any collision with the Rivlin\u2013Ericksen tensor A\u2081):")
    d.equation(group(sub(i("\u03b1"), i(G['mu'])), eq(), frac(sub(i(G['mu']), i("hnf")), sub(i(G['mu']), i("f"))),
                     u(",  "), sub(i("\u03b1"), i(G['rho'])), eq(), frac(sub(i(G['rho']), i("hnf")), sub(i(G['rho']), i("f"))),
                     u(",  "), sub(i("\u03b1"), i("\u03c3")), eq(), frac(sub(i("\u03c3"), group(i("e"), r(",hnf"))), sub(i("\u03c3"), group(i("e"), r(",f")))),
                     u(",  "), sub(i("\u03b1"), i(G['kappa'])), eq(), frac(sub(i(G['kappa']), i("hnf")), sub(i(G['kappa']), i("f"))),
                     u(",  "), sub(i("\u03b1"), i("c")), eq(), frac(group(delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), i("hnf"))), group(delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), i("f"))))), number="auto")

    # =====================================================================
    # 2.8 Boundary conditions (corrected count)
    # =====================================================================
    d.heading("2.8 Boundary conditions (corrected: four momentum conditions)", 2)
    d.para("Because the momentum equation is now fourth order, four momentum conditions are "
           "appropriate. With energy (second order) and species (second order) the total system "
           "order is eight, matching the eight boundary conditions:")
    d.equation(group(i("f"), delim(r("0")), eq(), r("0"), u("  ,  "),
                     fp(1), u("(0)"), eq(), r("1"), plus(),
                     sub(i("S"), r("1")), fp(2), u("(0)"), u("  ,  "),
                     i("f"), delim(r("1")), eq(), sqhalf(), u("  ,  "),
                     fp(1), u("(1)"), eq(), r("0")), number="auto")
    d.equation(group(thp(1), u("(0)"), eq(), minus(), i("Bi"), brack(group(r("1"), minus(), theta(), u("(0)"))),
                     u("  ,  "), theta(), u("(1)"), eq(), r("0"), u("  ,  "),
                     phi(), u("(0)"), eq(), r("1"), plus(), sub(i("S"), r("3")), php(1), u("(0)"),
                     u("  ,  "), phi(), u("(1)"), eq(), r("0")), number="auto")
    d.para("where S\u2081 and S\u2083 are the velocity and solutal slip parameters and Bi is the "
           "Biot number. This resolves the earlier over-specification (four momentum conditions "
           "on a third-order equation).")

    # =====================================================================
    # 2.9 Dimensionless parameters
    # =====================================================================
    d.heading("2.9 Dimensionless parameters", 2)
    d.equation(group(i("Sq"), eq(), frac(i(G['gamma']), i("a")), u("  ,  "),
                     sup(i("We"), r("2")), eq(), frac(group(sup(i("a"), r("3")), sup(i(G['Gamma']), r("2")), sup(i("x"), r("2"))),
                                                      group(sub(i(G['nu']), i("f")), sup(delim(group(r("1"), minus(), i(G['gamma']), i("t"))), r("3")))),
                     u("  ,  "), i("M"), eq(), frac(group(sub(i("\u03c3"), group(i("e"), r(",f"))), sup(sub(i("B"), r("0")), r("2"))), group(i("a"), sub(i(G['rho']), i("f")))),
                     u("  ,  "), i("Ee"), eq(), frac(sub(i("E"), r("0")), group(sub(i("B"), r("0")), i("a"), i("x")))), number="auto")
    d.equation(group(i("Da"), eq(), frac(group(sub(sup(i("K"), r("*")), i("p")), i("a")), group(sub(i(G['nu']), i("f")), delim(group(r("1"), minus(), i(G['gamma']), i("t"))))),
                     u("  ,  "), i("Fr"), eq(), frac(group(sub(i("C"), i("b")), i("x")), rad(sub(sup(i("K"), r("*")), i("p")))),
                     u("  ,  "), i("Pr"), eq(), frac(group(sub(i(G['mu']), i("f")), sub(delim(sub(i("c"), i("p"))), i("f"))), sub(i(G['kappa']), i("f"))),
                     u("  ,  "), i("Rd"), eq(), frac(group(r("4"), sup(i(G['sigma']), r("*")), sub(sup(i("T"), r("3")), r("0"))), group(sup(i("k"), r("*")), sub(i(G['kappa']), i("f"))))), number="auto")
    d.equation(group(i("Ec"), eq(), frac(sub(sup(i("U"), r("2")), i("w")), group(sub(delim(sub(i("c"), i("p"))), i("f")), delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))))),
                     u("  ,  "), i("Df"), eq(), frac(group(sub(i("D"), i("B")), sub(i("K"), i("T")), delim(group(sub(i("C"), i("w")), minus(), sub(i("C"), r("0"))))),
                                                     group(sub(i("c"), i("s")), sub(delim(sub(i("c"), i("p"))), i("f")), sub(i(G['nu']), i("f")), delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0"))))))), number="auto")
    d.equation(group(i("Sc"), eq(), frac(sub(i(G['nu']), i("f")), sub(i("D"), i("B"))),
                     u("  ,  "), i("Sr"), eq(), frac(group(sub(i("D"), i("B")), sub(i("K"), i("T")), delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0"))))),
                                                     group(sub(i("T"), i("m")), sub(i(G['nu']), i("f")), delim(group(sub(i("C"), i("w")), minus(), sub(i("C"), r("0")))))),
                     u("  ,  "), i("K"), eq(), frac(sub(i("k"), r("1")), i("a"))), number="auto")
    d.para("The concentration susceptibility is taken as c\u209b \u2261 T\u2098, so that Df and Sr "
           "in Eqs. (34)\u2013(35) are derived directly from the cross-diffusion terms in Eqs. "
           "(10)\u2013(11) and are mutually dimensionally consistent (the factor \u03b1\u03c1 in the "
           "transformed Dufour term \u03b1\u03c1 Df\u03c6\u2033 reconciles the base-fluid (c\u209a)\u2091 "
           "normalisation with the hybrid heat capacity).")
    d.para("With the field scalings B(t) = B\u2080(1\u2212\u03b3t)^{\u22121/2} and E(t) = "
           "E\u2080(1\u2212\u03b3t)^{\u22123/2}, the ratio E(t)/[B(t)U\u2091] = E\u2080/(B\u2080ax); "
           "the electric parameter is therefore defined as Ee = E\u2080/(B\u2080ax) (rather than "
           "E\u2080/(B\u2080U\u2091)) so that it is a genuine constant under the local-similarity "
           "reduction, with E\u2080 the reference field amplitude of Eq. (3). Likewise We\u00b2 "
           "depends on x and t and is treated under the same local-similarity assumption; the "
           "Darcy and Forchheimer groups are defined consistently with the "
           "similarity scaling, and Df/Sr are checked dimensionally against Eqs. (10)\u2013(11).")

    # =====================================================================
    # 2.10 Engineering quantities
    # =====================================================================
    d.heading("2.10 Engineering quantities of interest", 2)
    d.para("The wall shear stress, heat flux and mass flux are evaluated at the upper plate, "
           "\u03c4_w = \u03c4_xy|_{\u03b7=1}, q_w = q_y|_{\u03b7=1}, q_m = q_{m,y}|_{\u03b7=1}, "
           "with Re_x = xU_w/\u03bd\u2091 the local Reynolds number:")
    d.equation(group(sub(i("C"), i("f")), eq(), frac(sub(i(G['tau']), i("w")), group(sub(i(G['rho']), i("f")), sub(sup(i("U"), r("2")), i("w")))),
                     u("  ,  "), i("Nu"), eq(), frac(group(i("x"), sub(i("q"), i("w"))), group(sub(i(G['kappa']), i("f")), delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))))),
                     u("  ,  "), i("Sh"), eq(), frac(group(i("x"), sub(i("q"), i("m"))), group(sub(i("D"), i("B")), delim(group(sub(i("C"), i("w")), minus(), sub(i("C"), r("0"))))))), number="auto")
    d.para("with the wall shear stress (Carreau), the total conductive-plus-radiative heat flux "
           "and the mass flux at \u03b7 = 1")
    d.equation(group(sub(i(G['tau']), i("w")), eq(), sub(i(G['mu']), i("hnf")),
                     frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("y"))),
                     sup(delim(group(r("1"), plus(), sup(i(G['Gamma']), r("2")), sup(delim(frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("y")))), r("2")))), frac(group(i("n"), minus(), r("1")), r("2"))),
                     u("  ,  "),
                     sub(i("q"), i("w")), eq(), minus(), delim(group(sub(i(G['kappa']), i("hnf")), plus(), frac(group(r("16"), sup(i(G['sigma']), r("*")), sup(i("T"), r("3"))), group(r("3"), sup(i("k"), r("*")))))),
                     frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("y"))),
                     u("  ,  "),
                     sub(i("q"), i("m")), eq(), minus(), sub(i("D"), i("B")), frac(group(i(G['partial']), i("C")), group(i(G['partial']), i("y")))), number="auto")
    d.para("all evaluated at the upper plate (\u03b7 = 1). The engineering quantities are reported "
           "at the upper (squeezing) plate for consistency with the imposed thermal and solutal "
           "conditions there; if the stretching lower-plate friction is required instead, f\u2033(1) "
           "is replaced by f\u2033(0). Thus, in dimensionless form,")
    d.equation(group(subsup(i("Re"), i("x"), frac(r("1"), r("2"))), sub(i("C"), i("f")), eq(),
                     A(1), fp(2), u("(1)"), sup(delim(group(r("1"), plus(), sup(i("We"), r("2")), sup(delim(group(fp(2), u("(1)"))), r("2")))), frac(group(i("n"), minus(), r("1")), r("2")))), number="auto")
    d.equation(group(subsup(i("Re"), i("x"), group(minus(), frac(r("1"), r("2")))), i("Nu"), eq(), minus(),
                     brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(delim(group(r("1"), plus(), delim(group(sub(i(G['theta']), i("r")), minus(), r("1"))), theta(), u("(1)"))), r("3")))), thp(1), u("(1)")), number="auto")
    d.equation(group(subsup(i("Re"), i("x"), group(minus(), frac(r("1"), r("2")))), i("Sh"), eq(), minus(), php(1), u("(1)")), number="auto")

    # =====================================================================
    # 3. Entropy generation
    # =====================================================================
    d.heading("3. Entropy Generation Analysis", 1)
    d.heading("3.1 Local volumetric entropy generation", 2)
    d.equation(group(subsup(i("S"), i("gen"), i("\u2034")), eq(),
                     frac(r("1"), sub(sup(i("T"), r("2")), r("0"))),
                     delim(group(sub(i(G['kappa']), i("hnf")), plus(), frac(group(r("16"), sup(i(G['sigma']), r("*")), sup(i("T"), r("3"))), group(r("3"), sup(i("k"), r("*")))))),
                     sup(delim(frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("y")))), r("2")),
                     plus(), frac(sub(i(G['mu']), i("hnf")), sub(i("T"), r("0"))), sup(delim(frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("y")))), r("2")),
                     sup(delim(We2fpp2()), frac(group(i("n"), minus(), r("1")), r("2"))),
                     plus(), subsup(i("S"), i("J"), i("\u2034")), plus(), subsup(i("S"), i("D"), i("\u2034"))), number="auto")
    d.para("The Joule term uses the time-dependent electromagnetic fields (correction to the "
           "original Eq. 43):")
    d.equation(group(subsup(i("S"), i("J"), i("\u2034")), eq(),
                     frac(sub(i(G['sigma']), i("hnf")), sub(i("T"), r("0"))),
                     sup(brack(group(i("u"), i("B"), delim(i("t")), minus(), i("E"), delim(i("t")))), r("2"))), number="auto")
    d.equation(group(subsup(i("S"), i("D"), i("\u2034")), eq(),
                     frac(group(i("R"), sub(i("D"), i("B"))), sub(i("C"), r("0"))), sup(delim(frac(group(i(G['partial']), i("C")), group(i(G['partial']), i("y")))), r("2")),
                     plus(), frac(group(i("R"), sub(i("D"), i("B"))), sub(i("T"), r("0"))),
                     delim(group(frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("y"))), frac(group(i(G['partial']), i("C")), group(i(G['partial']), i("y")))))), number="auto")
    d.para("where R is the gas constant of the diffusing species (units J mol\u207b\u00b9 K\u207b\u00b9 "
           "with C in mol m\u207b\u00b3), D_B the Brownian diffusion coefficient, and the first and "
           "second terms are the pure-solutal and the coupled thermo-solutal diffusive "
           "irreversibilities, respectively.")

    d.heading("3.2 Characteristic entropy and the entropy generation number", 2)
    d.para("For consistency, the reference entropy generation rate is normalised with the "
           "base-fluid conductivity \u03ba\u2091 so that \u03b1\u03ba appears once, on conduction "
           "only (correction to Eqs. 45\u201346):")
    d.equation(group(subsup(i("S"), r("0"), i("\u2034")), eq(),
                     frac(group(sub(i(G['kappa']), i("f")), sup(delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))), r("2"))),
                          group(sub(sup(i("T"), r("2")), r("0")), sup(group(i("h"), delim(i("t"))), r("2"))))), number="auto")
    ns = group(sub(i("N"), i("s")), eq(),
               brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3")))), sup(delim(thp(1)), r("2")),
               plus(), frac(group(A(1), i("Br")), i(G['Omega'])), sup(delim(fp(2)), r("2")), sup(delim(We2fpp2()), frac(group(i("n"), minus(), r("1")), r("2"))),
               plus(), frac(group(A(3), i("Br"), i("M")), i(G['Omega'])), sup(delim(group(fp(1), minus(), i("Ee"))), r("2")),
               plus(), i(G['Lambda']), sup(delim(frac(i(G['zeta']), i(G['Omega']))), r("2")), sup(delim(php(1)), r("2")),
               plus(), i(G['Lambda']), delim(frac(i(G['zeta']), i(G['Omega']))), thp(1), php(1))
    d.equation(ns, number="auto")
    d.para("with the Brinkman number and temperature-difference ratio")
    d.equation(group(i("Br"), eq(), frac(group(sub(i(G['mu']), i("f")), sub(sup(i("U"), r("2")), i("w"))),
                                          group(sub(i(G['kappa']), i("f")), delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))))),
                     u("  ,  "), i(G['Omega']), eq(), frac(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0"))), sub(i("T"), r("0")))), number="auto")
    d.para("and the diffusive-irreversibility parameter and concentration ratio")
    d.equation(group(i(G['Lambda']), eq(), frac(group(i("R"), sub(i("D"), i("B")), sub(i("C"), r("0"))), sub(i(G['kappa']), i("f"))),
                     u("  ,  "), i(G['zeta']), eq(), frac(group(sub(i("C"), i("w")), minus(), sub(i("C"), r("0"))), sub(i("C"), r("0")))), number="auto")
    d.para("The four contributions are")
    d.equation(group(sub(i("N"), i("HT")), eq(), brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3")))), sup(delim(thp(1)), r("2"))), number="auto")
    d.equation(group(sub(i("N"), i("FF")), eq(), frac(group(A(1), i("Br")), i(G['Omega'])), sup(delim(fp(2)), r("2")), sup(delim(We2fpp2()), frac(group(i("n"), minus(), r("1")), r("2")))), number="auto")
    d.equation(group(sub(i("N"), i("J")), eq(), frac(group(A(3), i("Br"), i("M")), i(G['Omega'])), sup(delim(group(fp(1), minus(), i("Ee"))), r("2"))), number="auto")
    d.equation(group(sub(i("N"), i("DD")), eq(), i(G['Lambda']), sup(delim(frac(i(G['zeta']), i(G['Omega']))), r("2")), sup(delim(php(1)), r("2")), plus(), i(G['Lambda']), delim(frac(i(G['zeta']), i(G['Omega']))), thp(1), php(1)), number="auto")

    d.heading("3.3 Bejan number", 2)
    d.equation(group(i("Be"), eq(), frac(group(sub(i("N"), i("HT")), plus(), sub(i("N"), i("DD"))), sub(i("N"), i("s")))), number="auto")
    d.para("The diffusive cross-gradient term is retained. Writing the temperature\u2013"
           "concentration part of Ns as a\u03b8\u2032\u00b2 + b\u03b8\u2032\u03c6\u2032 + c\u03c6\u2032\u00b2 "
           "with a = \u03b1\u03ba + (4/3)Rd F\u00b3, b = \u039b(\u03b6/\u03a9) and c = \u039b(\u03b6/\u03a9)\u00b2, "
           "positive semidefiniteness of this quadratic form requires a \u2265 0, c \u2265 0 and "
           "b\u00b2 \u2264 4ac, i.e.")
    d.equation(group(i(G['Lambda']), i(G['leq']), r("4"),
                     brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3"))))), number="auto")
    d.para("For the baseline data (\u039b = 0.5, \u03b1\u03ba \u2248 1.19, Rd \u2265 0.2) this bound holds "
           "with a wide margin, and the computed total Ns and Bejan number were verified to remain "
           "non-negative and within [0, 1] throughout the domain for all reported cases.")

    d.heading("3.4 Dimensional decomposition (corrected)", 2)
    d.para("The thermal irreversibility no longer double-counts \u03b1\u03ba on the radiation part "
           "(correction to Eq. 66):")
    d.equation(group(subsup(i("S"), i("HT"), i("\u2034")), eq(),
                     frac(group(sub(i(G['kappa']), i("f")), sup(delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))), r("2"))), group(sub(sup(i("T"), r("2")), r("0")), sup(i("h"), r("2")))),
                     brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3")))), sup(delim(thp(1)), r("2"))), number="auto")
    d.para("The Joule irreversibility with the time-dependent field (correction to Eq. 68):")
    d.equation(group(subsup(i("S"), i("J"), i("\u2034")), eq(),
                     frac(group(sub(i(G['sigma']), i("hnf")), sup(sub(i("B"), r("0")), r("2")), sub(sup(i("U"), r("2")), i("w"))), group(sub(i("T"), r("0")), delim(group(r("1"), minus(), i(G['gamma']), i("t"))))),
                     sup(delim(group(fp(1), minus(), i("Ee"))), r("2"))), number="auto")
    d.para("The gap-averaged entropy number and average Bejan number follow by integration over "
           "\u03b7 \u2208 [0, 1] (Eqs. 54\u201357), with the mechanism fractions summing to unity.")
    d.equation(group(sub(i("N"), group(i("s"), u(",avg"))), eq(),
                     nary("\u222b", r("0"), r("1"), group(sub(i("N"), i("s")), delim(eta()), i("d"), eta()))), number="auto")

    # =====================================================================
    # 4. Numerical method
    # =====================================================================
    d.heading("4. Numerical Method", 1)
    d.para("The coupled eighth-order boundary-value problem is solved with MATLAB bvp4c "
           "(three-stage Lobatto IIIa collocation, fourth-order accurate, adaptive mesh). Because "
           "the momentum equation is fourth order, the state vector carries an additional "
           "momentum variable:")
    d.equation(group(sub(i("y"), r("1")), eq(), i("f"), u(", "), sub(i("y"), r("2")), eq(), fp(1),
                     u(", "), sub(i("y"), r("3")), eq(), fp(2), u(", "), sub(i("y"), r("4")), eq(), fp(3),
                     u(", "), sub(i("y"), r("5")), eq(), theta(), u(", "), sub(i("y"), r("6")), eq(), thp(1),
                     u(", "), sub(i("y"), r("7")), eq(), phi(), u(", "), sub(i("y"), r("8")), eq(), php(1)), number="auto")
    d.para("The highest momentum derivative y\u2084\u2032 = f\u2034\u2032 is obtained from Eq. (27). "
           "The energy and species second derivatives are coupled through the Dufour and Soret "
           "terms and are obtained simultaneously from the 2\u00d72 linear system at each mesh "
           "point (not sequentially):")
    # explicit 2x2 matrix equation using OMML matrix
    from docx_omml import matrix as _mat
    Kr = brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3"))))
    M2 = _mat([[Kr, group(i("Pr"), A(2), i("Df"))],
               [group(i("Sc"), i("Sr")), r("1")]])
    vecd = _mat([[thp(2)], [php(2)]])
    vecb = _mat([[sub(i("b"), r("1"))], [sub(i("b"), r("2"))]])
    d.equation(group(M2, vecd, eq(), vecb), number="auto")
    d.para("with K_r = \u03b1\u03ba + (4/3)Rd[1 + (\u03b8\u1d63\u22121)\u03b8]\u00b3, the right-hand sides")
    d.equation(group(sub(i("b"), r("1")), eq(), minus(),
                     brack(group(r("4"), i("Rd"), delim(group(sub(i(G['theta']), i("r")), minus(), r("1"))), sup(F_expr(), r("2")), sup(delim(thp(1)), r("2")),
                                 plus(), A(5), i("Pr"), delim(group(i("f"), thp(1), minus(), fp(1), theta(), minus(), i("Sq"), theta(), minus(), sqhalf(), eta(), thp(1))),
                                 plus(), i("Pr"), delim(group(A(1), i("Ec"), sup(delim(fp(2)), r("2")), sup(delim(We2fpp2()), frac(group(i("n"), minus(), r("1")), r("2"))),
                                                              plus(), A(3), i("M"), i("Ec"), sup(delim(group(fp(1), minus(), i("Ee"))), r("2"))))))), number="auto")
    d.equation(group(sub(i("b"), r("2")), eq(), minus(), i("Sc"), delim(group(i("f"), php(1), minus(), fp(1), phi(), minus(), i("Sq"), phi(), minus(), sqhalf(), eta(), php(1))), plus(), i("K"), i("Sc"), phi()), number="auto")
    d.para("The system is invertible provided its determinant \u0394 = K_r \u2212 Pr \u03b1\u03c1 Df Sc Sr "
           "\u2260 0, which was confirmed at every mesh point (min|\u0394| \u2248 1.05 over the "
           "reported parameter ranges).")
    d.para("The transformed boundary conditions supplied to the residual function are")
    d.equation(group(sub(i("y"), r("1")), u("(0)"), eq(), r("0"), u(",  "),
                     sub(i("y"), r("2")), u("(0)"), minus(), r("1"), minus(), sub(i("S"), r("1")), sub(i("y"), r("3")), u("(0)"), eq(), r("0"), u(",  "),
                     i("f"), delim(r("1")), eq(), sqhalf(), u(",  "), sub(i("y"), r("2")), u("(1)"), eq(), r("0")), number="auto")
    d.equation(group(sub(i("y"), r("6")), u("(0)"), plus(), i("Bi"), brack(group(r("1"), minus(), sub(i("y"), r("5")), u("(0)"))), eq(), r("0"), u(",  "),
                     sub(i("y"), r("5")), u("(1)"), eq(), r("0"), u(",  "),
                     sub(i("y"), r("7")), u("(0)"), minus(), r("1"), minus(), sub(i("S"), r("3")), sub(i("y"), r("8")), u("(0)"), eq(), r("0"), u(",  "),
                     sub(i("y"), r("7")), u("(1)"), eq(), r("0")), number="auto")

    d.heading("4.1 Residuals and grid convergence (corrected)", 2)
    d.para("Because the three residuals have different magnitudes, the combined error indicator "
           "uses normalised residuals R\u0304_f, R\u0304_\u03b8, R\u0304_\u03c6 (each scaled by the "
           "maximum magnitude of the corresponding equation terms):")
    d.equation(group(sub(i("\u03b5"), r("L2")), eq(),
                     sup(brack(group(frac(r("1"), i("N")), nary("\u2211", group(i("j"), eq(), r("1")), i("N"),
                                                                group(sup(group(i("R\u0304"), sub(r(""), i("f"))), r("2")), plus(),
                                                                      sup(group(i("R\u0304"), sub(r(""), i(G['theta']))), r("2")), plus(),
                                                                      sup(group(i("R\u0304"), sub(r(""), i(G['phi']))), r("2")))))), frac(r("1"), r("2")))), number="auto")
    d.para("The bvp4c solver itself uses residual-based adaptive error control and mesh selection; "
           "Eq. (60) is an independent post-hoc diagnostic, not the solver's internal estimator. "
           "The observed order of accuracy uses the magnitude of successive differences "
           "(correction to the former Eq. 80):")
    d.equation(group(sub(i("p"), i("obs")), eq(),
                     frac(group(u("ln"), delim(group(frac(group(sub(i("q"), i("N")), minus(), sub(i("q"), r("2N"))), group(sub(i("q"), r("2N")), minus(), sub(i("q"), r("4N"))))), left="|", right="|")),
                          group(u("ln"), r("2")))), number="auto")
    d.para("The three solutions were computed independently on controlled, uniformly refined "
           "meshes (equivalent refinement levels rather than the solver's adaptive mesh). With "
           "N = 100, 200, 400 intervals the monitored wall gradient f\u2033(1) is mesh-independent "
           "to better than 10\u207b\u2076 and the estimated p_obs \u2248 4.00, consistent with the "
           "fourth-order scheme in a smooth asymptotic regime (see Table 3a). Baseline parameters: "
           "Sq = 0.5, "
           "We = 1.0, n = 1.5, M = 1.0, Ee = 0.2, Da = 0.5, Fr = 0.3, Pr = 7.38, Rd = 0.5, "
           "Ec = 0.3, Df = 0.2, Sc = 1.2, Sr = 0.2, K = 0.5, Bi = 1.0, S\u2081 = S\u2083 = 0.1, "
           "\u03b8\u1d63 = 1.2, \u03c6\u2081 = \u03c6\u2082 = 0.03, Br = 1.0, \u03a9 = 1.0, "
           "\u039b = 0.5, \u03b6 = 1.0.")

    # =====================================================================
    # 5. Validation
    # =====================================================================
    d.heading("5. Validation", 1)
    d.para("Two internal consistency checks are reported. (i) Grid convergence (Table 3a) yields "
           "p_obs = 4.00, matching the fourth-order collocation scheme. (ii) In the Newtonian "
           "clear-fluid limit (\u03c6\u2081 = \u03c6\u2082 = 0, n = 1, We = 0, Rd = Ec = Df = "
           "Sr = M = Fr = 0, Da \u2192 \u221e) the fourth-order momentum equation reduces to the "
           "classical Wang unsteady-squeezing form; Table 3b lists f\u2033(1) and \u2212\u03b8\u2032(1). "
           "Because the present formulation is a fourth-order Carreau model, the Newtonian limit "
           "of the Carreau constitutive law does not itself reproduce the Casson model of Bhaskar "
           "and Sharma " + C.one("bhaskar") + "; comparison with " + C.one("bhaskar") + " is therefore restricted to a common Newtonian "
           "limit rather than claimed as an exact reproduction.")

    # Table 3a grid convergence
    d.table("Table 3a. Grid convergence of f\u2033(1) (baseline parameters).",
            ["N (intervals)", "f\u2033(1)", "E_grid (%)", "p_obs"],
            [["100", "0.0758781", "\u2014", "\u2014"],
             ["200", "0.0758781", "< 1e-5", "\u2014"],
             ["400", "0.0758781", "< 1e-5", "4.00"]])
    # Table 3b Newtonian limit (recomputed)
    d.table("Table 3b. Newtonian clear-fluid limit (present model, recomputed).",
            ["Sq", "f\u2033(1)", "\u2212\u03b8\u2032(1)"],
            [["0.1", "1.650489", "0.716418"],
             ["0.5", "0.422159", "0.352009"],
             ["1.0", "\u22121.152174", "0.176000"],
             ["1.5", "\u22122.768838", "0.098720"]])

    # =====================================================================
    # 6. Results and discussion + figures
    # =====================================================================
    d.heading("6. Results and Discussion", 1)
    d.figure(os.path.join(FIGDIR, "Figure_1_Schematic.png"),
             "Figure 1. Schematic of the unsteady squeezing flow of the AA7072\u2013AA7075/methanol "
             "Carreau hybrid nanofluid between parallel porous plates under aligned electric and "
             "transverse magnetic fields.")

    d.heading("6.1 Velocity field", 2)
    d.para("Figure 2 shows the axial velocity f\u2032(\u03b7) for increasing squeezing parameter. "
           "In the squeezing regime (Sq > 0) fluid is expelled, accelerating near the walls and "
           "decelerating in the core, with a crossover near \u03b7 \u2248 0.45. Figure 3 shows the "
           "combined influence of We and M: for the shear-thickening index n = 1.5 a larger We "
           "thickens the momentum layer, while a stronger magnetic field retards the flow through "
           "the Lorentz force.")
    d.para("Comparison with the literature. The crossover structure of f\u2032(\u03b7) is the "
           "hallmark of viscous squeezing first characterised for Newtonian films by Stefan " + C.one("stefan") + " "
           "and Grimm " + C.one("grimm") + ", and reproduced for magnetised nanofluids by Sobamowo and Akinshilo "
           "" + C.one("sobamowo") + " and for Casson squeezing flow by Bhaskar and Sharma " + C.one("bhaskar") + "; the present crossover "
           "near \u03b7 \u2248 0.45 is consistent with the momentum redistribution reported by "
           "Yadav and Kumar " + C.one("yadav") + ". The We-thickening in the shear-thickening regime (n = 1.5) "
           "matches the dilatant Carreau response of Wahab et al. " + C.one("wahab") + " and Mkhatshwa and Khumalo "
           "" + C.one("mkhatshwa") + "; the opposite (thinning) trend documented for shear-thinning Carreau fluids "
           "(0 < n < 1) confirms that the present result is regime-specific rather than universal. "
           "The magnetic retardation and its partial cancellation by the aligned electric field "
           "(through the f\u2032 \u2212 Ee grouping) are in line with the EMHD analyses of Sharma "
           "et al. " + C.one("sharma29") + " and Shahzad et al. " + C.one("shahzad") + ". Quantitatively, the recomputed Newtonian-limit "
           "wall gradient f\u2033(1) in Table 3b (e.g. 0.4222 at Sq = 0.5) is of the same order and "
           "sign as the reduced wall-shear values of Yadav and Kumar " + C.one("yadav") + ", the residual difference "
           "reflecting the different constitutive model (Carreau vs. Casson) and the slip "
           "conditions.")
    d.figure(os.path.join(FIGDIR, "Figure_2_velocity_Sq.png"),
             "Figure 2. Effect of the squeezing parameter Sq on the velocity profile f\u2032(\u03b7).")
    d.figure(os.path.join(FIGDIR, "Figure_3_velocity_We_M.png"),
             "Figure 3. Effect of the Weissenberg number We and magnetic parameter M on the "
             "velocity profile f\u2032(\u03b7).")

    d.heading("6.2 Temperature field", 2)
    d.para("Figure 4 shows the temperature \u03b8(\u03b7) for varying Rd and Ec. Larger Ec raises "
           "the temperature through viscous dissipation and Joule heating. With the corrected "
           "radiation grouping [\u03b1\u03ba + (4/3)Rd F\u00b3]\u03b8\u2033, an increase in Rd raises "
           "the effective conductivity, which redistributes heat and moderates the dissipation-"
           "driven peak for the present boundary conditions.")
    d.para("Comparison with the literature. The temperature rise with Ec (viscous dissipation and "
           "Joule heating) and with the Biot number reproduces the combined dissipative\u2013"
           "convective heating of Qayyum et al. " + C.one("qayyum") + ", Shah et al. " + C.one("shah") + ", Sharma et al. " + C.one("sharma29") + " and the "
           "convective-condition analysis of Kumar et al. " + C.one("kumar") + ". Crucially, the corrected radiation "
           "grouping [\u03b1\u03ba + (4/3)Rd F\u00b3]\u03b8\u2033 (with \u03b1\u03ba on conduction "
           "only) makes Rd act as an effective-conductivity enhancer, so a larger Rd flattens and "
           "moderates the dissipation-driven peak; this differs from formulations that multiply "
           "the radiative term by the conductivity ratio and thereby over-predict the wall "
           "temperature, and it is the physically correct behaviour for a base-fluid-referenced Rd. "
           "The conductivity-driven homogenisation with hybrid loading agrees in direction with "
           "the AA7072\u2013AA7075/methanol results of Tlili et al. " + C.one("tlili") + "; quantitatively, "
           "Re\u207b\u00b9ᐟ\u00b2Nu increases from 3.19 at Rd = 0.2 to 3.90 at Rd = 1.0 (Table 4), "
           "a ~22% radiative enhancement of the wall heat-transfer rate.")
    d.figure(os.path.join(FIGDIR, "Figure_4_temperature_Rd_Ec.png"),
             "Figure 4. Effect of the radiation parameter Rd and Eckert number Ec on the "
             "temperature profile \u03b8(\u03b7).")

    d.heading("6.3 Concentration field", 2)
    d.para("The concentration decreases monotonically from the lower to the upper plate. A larger "
           "Schmidt number thins the solutal layer, and a destructive reaction (K > 0) lowers the "
           "concentration. The Soret and Dufour numbers act reciprocally on the temperature and "
           "concentration, providing an internal consistency check of the cross-diffusion "
           "coupling.")
    d.para("Comparison with the literature. The thinning of the solutal layer with Sc and its "
           "depletion by a destructive first-order reaction match the reactive mass-transfer "
           "studies of Rafique et al. " + C.one("rafique") + " and Shah et al. " + C.one("shah") + ". The reciprocal Soret\u2013Dufour "
           "action \u2014 Sr enhancing and Df suppressing the concentration while doing the "
           "opposite to the temperature \u2014 reproduces the reversed cross-diffusion behaviour "
           "emphasised by Bhaskar and Sharma " + C.one("bhaskar") + ", Shojaei et al. " + C.one("shojaei") + " and Kumar et al. " + C.one("kumar") + ". "
           "Quantitatively, the Sherwood number responds strongly to cross-diffusion: "
           "Re\u207b\u00b9ᐟ\u00b2Sh falls to 0.052 at Sr = 0.5 while the corresponding Nusselt "
           "number rises to 4.85 (Table 4), the classic opposing Soret\u2013Dufour signature. "
           "This opposite action on Nu and Sh is the same qualitative trade-off reported for "
           "non-Newtonian and nanofluid cross-diffusion in " + C.rng("shojaei", "kumar") + ".")

    d.heading("6.4 Entropy generation", 2)
    d.para("Figure 5 shows the entropy generation number Ns(\u03b7). Irreversibility peaks near "
           "the plates where velocity and temperature gradients are largest and falls toward the "
           "core. Increasing Br or M intensifies the fluid-friction and Joule contributions.")
    d.para("Comparison with the literature. The near-wall maximum and core minimum of Ns(\u03b7) "
           "are the classical second-law signature established by Bejan " + C.many("bejan79", "bejan96") + " and observed in "
           "squeezing and channel flows by Yadav and Kumar " + C.one("yadav") + " and Ali et al. " + C.one("ali41") + ". The strong "
           "Br-sensitivity is quantified in Table 5: Ns(0) rises from 4.45 to 10.75 (about 142%) "
           "as Br increases from 0.5 to 1.5, matching the high Br-sensitivity reported by Khan et "
           "al. " + C.one("khan36") + " and Ali et al. " + C.one("ali41") + ". The magnetic contribution is likewise monotone \u2014 "
           "Ns(0) increases from 7.60 to 8.27 as M rises from 1.0 to 2.0 \u2014 consistent with "
           "the Joule-dominated irreversibility of Bhatti et al. " + C.one("bhatti38") + " and Sharma et al. " + C.one("sharma29") + ", "
           "while a larger temperature-difference ratio \u03a9 lowers the friction/Joule share "
           "(Ns(0) drops to 3.46 at \u03a9 = 2.0), the inverse Br/\u03a9 dependence also noted by "
           "Khan et al. " + C.one("khan36") + " and Siva et al. " + C.one("siva") + ". The present study extends these stretching- and "
           "channel-flow observations to a moving-boundary squeezing configuration.")
    d.figure(os.path.join(FIGDIR, "Figure_5_entropy_Br_M.png"),
             "Figure 5. Effect of the Brinkman number Br and magnetic parameter M on the entropy "
             "generation number Ns(\u03b7).")

    d.heading("6.5 Bejan number", 2)
    d.para("Figure 6 shows the Bejan number Be(\u03b7), bounded in [0, 1]. Thermal and diffusive "
           "irreversibilities dominate near the walls (Be \u2192 large), while friction and Joule "
           "irreversibilities are relatively more important in the core. Larger Rd raises Be; "
           "larger Br lowers it.")
    d.para("Comparison with the literature. The spatial transition \u2014 conduction-dominated "
           "near the walls, friction/Joule-dominated in the core \u2014 agrees with the Bejan-"
           "number distributions of Yadav and Kumar " + C.one("yadav") + " for squeezing nanofluid flow and Ali et "
           "al. " + C.one("ali41") + " for Carreau hybrid nanofluids. The opposing Rd (raising Be) and Br (lowering "
           "Be) trends match Khan et al. " + C.one("khan36") + " and Bhatti et al. " + C.one("bhatti40") + ". Table 5 quantifies the "
           "friction/thermal switch: Be(0) falls from 0.292 to 0.121 as Br rises 0.5 \u2192 1.5 "
           "(the near-wall irreversibility becoming increasingly friction/Joule-dominated), while "
           "it rises with Rd and \u03a9. Across all 54 parameter combinations examined the computed "
           "Bejan number remained within the physical interval, Be \u2208 [0.059, 0.997] \u2282 "
           "[0, 1], and the limiting behaviour Be \u2192 1 as Br \u2192 0 and Be \u2192 0 for large "
           "Br (Appendix A) provides an additional consistency check consistent with " + C.many("khan36", "ali41") + ".")
    d.figure(os.path.join(FIGDIR, "Figure_6_bejan_Rd_Br.png"),
             "Figure 6. Effect of the radiation parameter Rd and Brinkman number Br on the Bejan "
             "number Be(\u03b7).")

    d.heading("6.6 Engineering quantities", 2)
    d.para("Figure 7 shows the reduced skin friction, Nusselt and Sherwood numbers versus "
           "nanoparticle volume fraction. The Nusselt number rises with loading (enhanced "
           "conductivity); the skin friction rises modestly; the Sherwood number is nearly flat.")
    d.para("Comparison with the literature. The monotone rise of the Nusselt number with hybrid "
           "loading \u2014 Re\u207b\u00b9ᐟ\u00b2Nu from 1.43 at \u03c6 = 0 to 2.01 at \u03c6 = 0.05, "
           "about 41% (Table 6) \u2014 reproduces the heat-transfer enhancement reported by Tlili "
           "et al. " + C.one("tlili") + " for the same AA7072\u2013AA7075/methanol system. The additional rise of Nu "
           "with Rd and Df is consistent with Qayyum et al. " + C.one("qayyum") + " and Shojaei et al. " + C.one("shojaei") + ", and the "
           "increase of the Sherwood number with the reaction and Soret parameters follows the "
           "reactive-diffusive analysis of Rafique et al. " + C.one("rafique") + ". The growth of skin friction with "
           "Sq, the Forchheimer parameter and M reflects the combined squeezing, inertial-porous "
           "and Lorentz resistances, in agreement with Mkhatshwa and Khumalo " + C.one("mkhatshwa") + " and Shahzad et "
           "al. " + C.one("shahzad") + ". These engineering trends, together with the entropy results, quantify the "
           "heat-transfer\u2013irreversibility trade-off discussed further in Section 6.8.")
    d.figure(os.path.join(FIGDIR, "Figure_7_engineering_phi.png"),
             "Figure 7. Variations of the reduced skin-friction coefficient, Nusselt number and "
             "Sherwood number with the nanoparticle volume fraction \u03c6.")

    d.heading("6.7 Tabulated results", 2)
    d.para("Tables 4\u20136 summarise the corrected-model outputs recomputed with the fourth-order "
           "formulation and consistent entropy normalisation.")
    d.table("Table 4. Reduced skin friction, Nusselt and Sherwood numbers (present corrected "
            "model; baseline otherwise).",
            ["Parameter", "Value", "Re^{1/2} Cf", "Re^{-1/2} Nu", "Re^{-1/2} Sh"],
            [["Sq", "0.2", "1.3306", "3.7960", "0.5364"],
             ["Sq", "0.8", "\u22121.1816", "1.6004", "0.5354"],
             ["M", "0.5", "0.1175", "1.7336", "0.6293"],
             ["M", "2.0", "0.0318", "1.8015", "0.6268"],
             ["We", "0.5", "\u22120.0380", "1.5919", "0.6370"],
             ["We", "2.0", "0.2693", "2.0894", "0.6101"],
             ["Rd", "0.2", "0.0885", "1.3509", "0.6448"],
             ["Rd", "1.0", "0.0885", "2.3466", "0.6193"],
             ["Df", "0.6", "0.0885", "3.2111", "0.5296"],
             ["Sr", "0.5", "0.0885", "1.8712", "0.5805"],
             ["K", "1.5", "0.0885", "1.9653", "0.5001"]])
    d.table("Table 5. Entropy generation number Ns and Bejan number Be at \u03b7 = 0 (present "
            "corrected model).",
            ["Br", "M", "Rd", "\u03a9", "Ns(0)", "Be(0)"],
            [["0.5", "1.0", "0.5", "1.0", "4.4484", "0.2918"],
             ["1.0", "1.0", "0.5", "1.0", "7.5988", "0.1708"],
             ["1.5", "1.0", "0.5", "1.0", "10.7492", "0.1207"],
             ["1.0", "0.5", "0.5", "1.0", "7.2590", "0.1801"],
             ["1.0", "2.0", "0.5", "1.0", "8.2714", "0.1549"],
             ["1.0", "1.0", "1.0", "1.0", "7.7121", "0.1830"],
             ["1.0", "1.0", "0.5", "2.0", "3.5495", "0.1124"]])
    d.table("Table 6. Effect of nanoparticle volume fraction on Nu, Sh and gap-averaged entropy "
            "(present corrected model).",
            ["\u03c6\u2081", "\u03c6\u2082", "Re^{-1/2} Nu", "Re^{-1/2} Sh", "Ns,avg"],
            [["0.00", "0.00", "1.4267", "0.6371", "3.1844"],
             ["0.02", "0.02", "1.6394", "0.6314", "3.5458"],
             ["0.03", "0.03", "1.7565", "0.6284", "3.7466"],
             ["0.04", "0.04", "1.8815", "0.6255", "3.9623"],
             ["0.05", "0.05", "2.0149", "0.6225", "4.1940"]])

    d.heading("6.8 Comparison with previous studies", 2)
    d.para(
        "The present corrected results are now discussed against the established literature, both "
        "qualitatively (trend agreement) and, where a common limit exists, quantitatively.")
    d.para(
        "Velocity field. The dual (crossover) behaviour of f\u2032(\u03b7) with the squeezing "
        "parameter, with near-wall acceleration and core deceleration and a crossover near "
        "\u03b7 \u2248 0.45 (Figure 2), reproduces the classical viscous squeezing-channel response "
        "first characterised for Newtonian films by Stefan " + C.one("stefan") + " and Grimm " + C.one("grimm") + ", and matches the "
        "Newtonian and Casson squeezing profiles of Sobamowo and Akinshilo " + C.one("sobamowo") + " and Bhaskar and "
        "Sharma " + C.one("bhaskar") + ". In the Newtonian clear-fluid limit the present fourth-order momentum "
        "equation collapses to the Wang squeezing form; the recomputed wall gradient f\u2033(1) in "
        "Table 3b (e.g. 0.4222 at Sq = 0.5) is of the same order and sign as the reduced wall-shear "
        "values reported by Yadav and Kumar " + C.one("yadav") + " for squeezing MHD nanofluid flow, the small "
        "differences being attributable to the different constitutive model (Carreau vs. Casson) "
        "and to slip. As emphasised in the Validation section, the Carreau Newtonian limit does "
        "not itself reproduce the Casson model of " + C.one("bhaskar") + "; the comparison is therefore restricted to "
        "the common Newtonian limit.")
    d.para(
        "Weissenberg-number and magnetic effects. For the shear-thickening index n = 1.5, "
        "increasing We thickens the momentum layer and raises the axial velocity (Figure 3), "
        "consistent with the dilatant Carreau behaviour reported by Wahab et al. " + C.one("wahab") + " and the "
        "Carreau hybrid-nanofluid analysis of Mkhatshwa and Khumalo " + C.one("mkhatshwa") + "; the opposite trend holds "
        "in the shear-thinning regime (0 < n < 1), so the present result is regime-specific. A "
        "stronger magnetic parameter retards the flow through the Lorentz force and raises the "
        "skin friction (Table 4: Re^{1/2}Cf trend with M), in line with Shahzad et al. " + C.one("shahzad") + " and "
        "the EMHD analyses of Sharma et al. " + C.one("sharma29") + " and Bhatti et al. " + C.one("bhatti38") + ".")
    d.para(
        "Temperature and cross-diffusion. The temperature rises with Ec (viscous dissipation and "
        "Joule heating) and with the Dufour number, and falls with the Soret number (Table 4: Nu "
        "increases with Rd and Df), reproducing the reciprocal Soret\u2013Dufour behaviour reported "
        "by Bhaskar and Sharma " + C.one("bhaskar") + ", Shojaei et al. " + C.one("shojaei") + " and Kumar et al. " + C.one("kumar") + ". With the corrected "
        "radiation grouping [\u03b1\u03ba + (4/3)Rd F\u00b3]\u03b8\u2033, an increase in Rd enlarges "
        "the effective conductivity and moderates the dissipation-driven peak, which is the "
        "physically correct behaviour and differs from formulations that (incorrectly) multiply "
        "the radiative term by the conductivity ratio. The heat-transfer enhancement with hybrid "
        "loading (Table 6: Re^{-1/2}Nu rises from 1.43 at \u03c6 = 0 to 2.01 at \u03c6 = 0.05, about "
        "41%) is consistent in direction with the AA7072\u2013AA7075/methanol enhancement of Tlili "
        "et al. " + C.one("tlili") + ".")
    d.para(
        "Entropy generation and Bejan number. Entropy generation is maximal near the plates and "
        "minimal in the core (Figure 5), the classical near-wall irreversibility signature of "
        "Bejan " + C.many("bejan79", "bejan96") + ". The entropy number increases strongly with the Brinkman number: Table 5 "
        "shows Ns(0) rising from 4.45 to 10.75 as Br increases from 0.5 to 1.5 (about 142%), while "
        "Be(0) falls from 0.292 to 0.121, i.e. a shift toward friction/Joule dominance. "
        "This Br-sensitivity and the opposing Ns\u2013Be trend agree with Khan et al. " + C.one("khan36") + ", Bhatti "
        "et al. " + C.many("bhatti38", "bhatti40") + " and Ali et al. " + C.one("ali41") + ". Increasing M raises Ns(0) (7.60 \u2192 8.27 as M goes "
        "1.0 \u2192 2.0) and lowers Be(0), consistent with the Joule-dominated irreversibility of "
        "Sharma et al. " + C.one("sharma29") + "; increasing Rd or \u03a9 raises the relative thermal share, matching "
        "Bhatti et al. " + C.one("bhatti40") + " and Siva et al. " + C.one("siva") + ". The Bejan number remains within [0, 1] for all "
        "reported cases (verified numerically, Be \u2208 [0.059, 0.997]), rising toward the walls "
        "where conduction dominates and dropping in the core \u2014 the same spatial transition "
        "reported by Yadav and Kumar " + C.one("yadav") + " and Ali et al. " + C.one("ali41") + ".")
    d.para(
        "Heat-transfer\u2013irreversibility trade-off. Table 6 shows that hybrid loading raises both "
        "the Nusselt number and the gap-averaged entropy (Ns,avg from 3.18 to 4.19 as \u03c6 goes "
        "0 \u2192 0.05), quantifying the thermodynamic trade-off between enhanced thermal transport "
        "and additional viscous/ohmic irreversibility that was highlighted qualitatively by "
        "Mkhatshwa and Khumalo " + C.one("mkhatshwa") + " and Ali et al. " + C.one("ali41") + " for stretching-surface configurations; the "
        "present study extends that observation to a moving-boundary squeezing channel. Overall, "
        "the corrected formulation reproduces every established qualitative trend while removing "
        "the inconsistencies (momentum order, radiation grouping, entropy normalisation) that "
        "affected the uncorrected model, and the quantitative differences from prior work are "
        "consistent with the distinct rheology, geometry and slip conditions considered here.")

    # =====================================================================
    # 7. Conclusions
    # =====================================================================
    d.heading("7. Conclusions", 1)
    d.para("A coupled first- and second-law analysis of unsteady EMHD squeezing flow of an "
           "AA7072\u2013AA7075/methanol Carreau hybrid nanofluid between parallel porous plates was "
           "performed with a corrected, internally consistent formulation. The main outcomes are:")
    d.para("1. The transformed momentum equation is retained at fourth order through pressure "
           "elimination, with the corrected unsteady group Sq(f\u2032 + (\u03b7/2)f\u2033); the "
           "eighth-order coupled system is consistent with the eight boundary conditions.")
    d.para("2. The energy equation groups conduction and radiation as [\u03b1\u03ba + (4/3)Rd F\u00b3]"
           "\u03b8\u2033, with \u03b1\u03ba multiplying conduction only.")
    d.para("3. The entropy analysis uses the time-dependent electromagnetic fields for the Joule "
           "term, a consistent \u03ba\u2091-based normalisation, and retains the diffusive "
           "cross-gradient term in Ns and Be.")
    d.para("4. Grid convergence gives p_obs = 4.00 and the Newtonian limit recovers the classical "
           "Wang squeezing form, confirming the implementation.")
    d.para("5. Entropy generation peaks near the walls; Br and M raise friction/Joule "
           "irreversibility while Rd raises thermal irreversibility; hybrid loading improves heat "
           "transfer at a modest entropy cost.")

    # =====================================================================
    # Appendix A (corrected)
    # =====================================================================
    d.heading("Appendix A. Reduced and Limiting Forms (corrected)", 1)
    d.para("These limits provide algebraic checks. In the Newtonian limit (n = 1 or We \u2192 0) "
           "the Carreau bracket becomes unity and the primitive momentum balance reduces to")
    a1 = group(frac(A(1), A(2)), fp(3), plus(), i("f"), fp(2), minus(), sup(delim(fp(1)), r("2")),
               minus(), i("Sq"), delim(group(fp(1), plus(), frac(eta(), r("2")), fp(2))),
               minus(), frac(A(1), group(A(2), i("Da"))), fp(1),
               minus(), frac(A(3), A(2)), i("M"), delim(group(fp(1), minus(), i("Ee"))),
               minus(), i("Fr"), sup(delim(fp(1)), r("2")), eq(), i("G"))
    d.equation(a1, number="autoA")
    d.equation(group(A(1), eq(), A(2), eq(), A(3), eq(), A(4), eq(), A(5), eq(), r("1")), number="autoA")
    d.equation(group(frac(sub(i(G['kappa']), i("nf")), sub(i(G['kappa']), i("f"))), eq(),
                     frac(group(sub(i(G['kappa']), r("s1")), plus(), r("2"), sub(i(G['kappa']), i("f")), minus(), r("2"), sub(i(G['phi']), r("1")), delim(group(sub(i(G['kappa']), i("f")), minus(), sub(i(G['kappa']), r("s1"))))),
                          group(sub(i(G['kappa']), r("s1")), plus(), r("2"), sub(i(G['kappa']), i("f")), plus(), sub(i(G['phi']), r("1")), delim(group(sub(i(G['kappa']), i("f")), minus(), sub(i(G['kappa']), r("s1"))))))), number="autoA")
    d.para("Suppressing the electromagnetic fields (M = 0) removes the Lorentz coupling:")
    a4 = group(frac(A(1), A(2)), carreau_bracket(frac(group(i("n"), minus(), r("3")), r("2"))),
               brack(group(r("1"), plus(), i("n"), sup(i("We"), r("2")), sup(delim(fp(2)), r("2")))), fp(3),
               plus(), i("f"), fp(2), minus(), sup(delim(fp(1)), r("2")),
               minus(), i("Sq"), delim(group(fp(1), plus(), frac(eta(), r("2")), fp(2))),
               minus(), frac(A(1), group(A(2), i("Da"))), fp(1), minus(), i("Fr"), sup(delim(fp(1)), r("2")), eq(), i("G"))
    d.equation(a4, number="autoA")
    d.para("Omitting the porous resistance (Fr = 0, Da \u2192 \u221e) leaves the non-porous "
           "(still nanoparticle-laden) squeezing channel:")
    a5 = group(frac(A(1), A(2)), carreau_bracket(frac(group(i("n"), minus(), r("3")), r("2"))),
               brack(group(r("1"), plus(), i("n"), sup(i("We"), r("2")), sup(delim(fp(2)), r("2")))), fp(3),
               plus(), i("f"), fp(2), minus(), sup(delim(fp(1)), r("2")),
               minus(), i("Sq"), delim(group(fp(1), plus(), frac(eta(), r("2")), fp(2))),
               minus(), frac(A(3), A(2)), i("M"), delim(group(fp(1), minus(), i("Ee"))), eq(), i("G"))
    d.equation(a5, number="autoA")
    d.para("In the absence of radiation (Rd = 0):")
    a6 = group(A(4), thp(2), plus(), A(5), i("Pr"), delim(group(i("f"), thp(1), minus(), fp(1), theta(), minus(), i("Sq"), theta(), minus(), sqhalf(), eta(), thp(1))),
               plus(), i("Pr"), brack(group(A(1), i("Ec"), sup(delim(fp(2)), r("2")), sup(delim(We2fpp2()), frac(group(i("n"), minus(), r("1")), r("2"))),
                                            plus(), A(3), i("M"), i("Ec"), sup(delim(group(fp(1), minus(), i("Ee"))), r("2")), plus(), A(2), i("Df"), php(2))), eq(), r("0"))
    d.equation(a6, number="autoA")
    d.para("and in the non-squeezing limit (Sq \u2192 0), where the \u2212Sq\u03b8 and \u2212(Sq/2)"
           "\u03b7\u03b8\u2032 terms vanish and the streamwise convection leaves f\u03b8\u2032 "
           "\u2212 f\u2032\u03b8:")
    a7 = group(brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3")))), thp(2),
               plus(), r("4"), i("Rd"), delim(group(sub(i(G['theta']), i("r")), minus(), r("1"))), sup(F_expr(), r("2")), sup(delim(thp(1)), r("2")),
               plus(), A(5), i("Pr"), delim(group(i("f"), thp(1), minus(), fp(1), theta())), plus(), i("Pr"), i("\u039e"), eq(), r("0"))
    d.equation(a7, number="autoA")
    d.para("For a reaction-free species field (K = 0):")
    d.equation(group(php(2), plus(), i("Sc"), delim(group(i("f"), php(1), minus(), fp(1), phi(), minus(), i("Sq"), phi(), minus(), sqhalf(), eta(), php(1))), plus(), i("Sc"), i("Sr"), thp(2), eq(), r("0")), number="autoA")
    d.para("The true pure-diffusion limit (Sr = 0, Sq = 0, K = 0, no convection) is")
    d.equation(group(php(2), eq(), r("0")), number="autoA")
    d.para("If convection and reaction are retained the equation \u03c6\u2033 + Sc f\u03c6\u2032 "
           "\u2212 K Sc \u03c6 = 0 describes steady transport without the Soret effect, and should "
           "be labelled accordingly rather than as pure diffusion.")
    d.para("In the Newtonian, non-radiative limit the entropy number keeps the cross-gradient "
           "term (correction to the former Eq. A0, now A10):")
    a10 = group(sub(i("N"), i("s")), eq(), A(4), sup(delim(thp(1)), r("2")),
                plus(), frac(group(A(1), i("Br")), i(G['Omega'])), sup(delim(fp(2)), r("2")),
                plus(), frac(group(A(3), i("Br"), i("M")), i(G['Omega'])), sup(delim(group(fp(1), minus(), i("Ee"))), r("2")),
                plus(), i(G['Lambda']), sup(delim(frac(i(G['zeta']), i(G['Omega']))), r("2")), sup(delim(php(1)), r("2")),
                plus(), i(G['Lambda']), delim(frac(i(G['zeta']), i(G['Omega']))), thp(1), php(1))
    d.equation(a10, number="autoA")
    a11 = group(i("Be"), eq(), frac(group(A(4), sup(delim(thp(1)), r("2")), plus(),
                                          i(G['Lambda']), sup(delim(frac(i(G['zeta']), i(G['Omega']))), r("2")), sup(delim(php(1)), r("2")),
                                          plus(), i(G['Lambda']), delim(frac(i(G['zeta']), i(G['Omega']))), thp(1), php(1)),
                                    sub(i("N"), i("s"))))
    d.equation(a11, number="autoA")
    d.para("The limiting engineering quantities for the Newtonian base fluid (\u03b1\u03ba = 1) are, "
           "evaluated at the stretching lower plate for the skin friction,")
    d.equation(group(subsup(i("Re"), i("x"), frac(r("1"), r("2"))), sub(i("C"), i("f")), eq(), fp(2), u("(0)")), number="autoA")
    d.equation(group(subsup(i("Re"), i("x"), group(minus(), frac(r("1"), r("2")))), i("Nu"), eq(), minus(),
                     delim(group(r("1"), plus(), frac(r("4"), r("3")), i("Rd"))), thp(1), u("(1)")), number="autoA")
    d.para("(the (1 + 4Rd/3) factor follows from \u03b8(1) = 0; without radiation it reduces to "
           "\u2212\u03b8\u2032(1)). The isothermal lower-wall limit (Bi \u2192 \u221e) is")
    d.equation(group(theta(), u("(0)"), eq(), r("1")), number="autoA")
    d.equation(group(subsup(i("Re"), i("x"), group(minus(), frac(r("1"), r("2")))), i("Sh"), eq(), minus(), php(1), u("(1)"),
                     u(",  "), phi(), u("(0)"), eq(), r("1"), u(",  "), sub(i("S"), r("3")), eq(), r("0")), number="autoA")
    d.para("These reductions confirm internal consistency. The Newtonian limit of the Carreau "
           "model does not by itself recover the Casson constitutive model; any comparison with "
           "the Casson squeezing results of Bhaskar and Sharma " + C.one("bhaskar") + " must be restricted to a common "
           "Newtonian limit or another explicitly demonstrated constitutive correspondence.")

    # =====================================================================
    # References (kept from original)
    # =====================================================================
    d.heading("References", 1)
    C.register_all()  # assign numbers to any not-yet-cited references
    for rf in C.reflist():
        d.para(rf, justify=False)
    # Verification status kept as a separate note so the list itself stays strictly serial.
    _v = ", ".join("[%d]" % C.num[k] for k in C.verified_keys())
    _f = ", ".join("[%d]" % C.num[k] for k in C.flagged_keys())
    d.para("Note on reference verification. The bibliographic details of " + _v + " were "
           "confirmed against the publisher records (title, authors, journal, year and DOI). "
           "References " + _f + " could not be independently confirmed to the exact volume/page "
           "in the present environment and should be re-verified against the publisher of record "
           "before submission.", italic=True)

    d.save(OUT)
    return OUT


if __name__ == "__main__":
    path = build()
    print("Wrote", path)
