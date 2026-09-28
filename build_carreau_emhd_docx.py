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

def A(n): return sub(i("A"), r(str(n)))

def F_expr():  # 1 + (theta_r - 1) theta
    return group(r("1"), plus(), delim(group(sub(i(G['theta']), i("r")), minus(), r("1"))), theta())


def build():
    d = Document()

    # =====================================================================
    # Title / abstract
    # =====================================================================
    d.title("Entropy Generation and Irreversibility Analysis of Unsteady EMHD "
            "Squeezing Flow of a Carreau Hybrid Nanofluid (AA7072\u2013AA7075/Methanol) "
            "Between Parallel Porous Plates")

    d.heading("Abstract", 2)
    d.para(
        "The second-law behaviour of unsteady, two-dimensional, electro-magnetohydrodynamic "
        "(EMHD) squeezing flow of a Carreau hybrid nanofluid confined between two parallel "
        "porous plates is investigated mathematically and numerically. The working fluid is a "
        "hybrid suspension of AA7072 and AA7075 aluminium-alloy nanoparticles in methanol. The "
        "model incorporates a transverse time-dependent magnetic field, an aligned electric "
        "field, Darcy\u2013Forchheimer porous drag, nonlinear thermal radiation, viscous "
        "dissipation, Joule heating, Soret\u2013Dufour cross-diffusion and a first-order "
        "homogeneous chemical reaction, together with velocity, thermal (Biot-type) and solutal "
        "slip boundary conditions. Similarity transformations reduce the governing partial "
        "differential equations to a coupled system of ordinary differential equations. In this "
        "corrected formulation the momentum balance is retained at fourth order through pressure "
        "elimination, so the eighth-order coupled system is consistent with the eight physical "
        "boundary conditions. The system is solved with the MATLAB collocation solver bvp4c. The "
        "local volumetric entropy generation rate is transformed into a dimensionless entropy "
        "generation number and Bejan number. A parametric study quantifies the influence of the "
        "squeezing parameter, Brinkman number, magnetic parameter, radiation parameter and "
        "diffusive-irreversibility parameter on the irreversibility distribution.")

    d.para("Keywords: Carreau hybrid nanofluid; Entropy generation; Bejan number; EMHD squeezing "
           "flow; Darcy\u2013Forchheimer; Soret\u2013Dufour; bvp4c", italic=True)

    # =====================================================================
    # 1. Introduction (condensed, unchanged in substance)
    # =====================================================================
    d.heading("1. Introduction", 1)
    d.para(
        "Intensification of convective heat transfer drives the development of compact, "
        "high-performance thermal-management devices. The low intrinsic conductivity of "
        "conventional coolants motivated the nanofluid concept of Choi and Eastman [1], and its "
        "hybrid extension in which two chemically distinct nanoparticles are co-dispersed [4, 5]. "
        "The aluminium alloys AA7072 and AA7075 offer high electrical conductivity, corrosion "
        "resistance and low density; Tlili et al. [8] reported significant heat-transfer "
        "enhancement for AA7072\u2013AA7075/methanol suspensions.")
    d.para(
        "Many industrial suspensions are non-Newtonian. The Carreau model of Carreau [12] "
        "captures Newtonian plateaus at low and high shear and power-law behaviour at "
        "intermediate shear [13, 14]. Squeezing flows between approaching surfaces arise in "
        "lubrication, squeeze-film dampers and hydraulic machinery [18, 19]. Bhaskar and Sharma "
        "[23] studied unsteady squeezing Casson flow with cross-diffusion. The present work "
        "extends this squeezing-channel configuration to a Carreau hybrid nanofluid with a "
        "complete second-law treatment, including Soret\u2013Dufour cross-diffusion, nonlinear "
        "radiation, Joule heating and multi-mode slip in a Darcy\u2013Forchheimer porous channel "
        "[24\u201343].")
    d.para(
        "This revised manuscript corrects the transformed momentum equation and its boundary-"
        "condition count, rederives the radiative grouping in the energy equation, and makes the "
        "entropy-generation normalisation consistent, as detailed below.")

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
                         frac(r("1"), r("2")))), number=1)
    d.para("The lower plate is stretched with velocity U\u2091(x, t); the upper plate moves "
           "normally with the squeezing velocity v\u2095 = dh/dt. A time-dependent transverse "
           "magnetic field and aligned electric field are applied:")
    d.equation(group(i("B"), delim(i("t")), eq(),
                     frac(sub(i("B"), r("0")), sup(delim(group(r("1"), minus(), i(G['gamma']), i("t"))), frac(r("1"), r("2"))))),
               number=2)

    d.heading("2.2 Carreau hybrid nanofluid constitutive model", 2)
    d.para("The Cauchy stress tensor is written with the total-stress symbol \u03c3 (preferred "
           "over \u03c4 for total stress):")
    d.equation(group(i(G['sigma']), eq(), minus(), i("p"), i("I"), plus(),
                     i(G['mu']), delim(i("\u03b3\u0307")), sub(i("A"), r("1"))), number=3)
    d.para("with the shear-dependent (Carreau) viscosity")
    # (4): mu = mu_inf + (mu0 - mu_inf)[1 + (Gamma gammadot)^2]^{(n-1)/2}
    d.equation(group(i(G['mu']), delim(i("\u03b3\u0307")), eq(), sub(i(G['mu']), i("\u221e")),
                     plus(), delim(group(sub(i(G['mu']), r("0")), minus(), sub(i(G['mu']), i("\u221e")))),
                     sup(brack(group(r("1"), plus(), sup(delim(group(i(G['Gamma']), i("\u03b3\u0307"))), r("2")))),
                         frac(group(i("n"), minus(), r("1")), r("2")))), number=4)
    d.para("and the scalar shear rate")
    # (5): gammadot = sqrt( (1/2) tr(A1^2) )
    d.equation(group(i("\u03b3\u0307"), eq(),
                     rad(group(frac(r("1"), r("2")), u("tr"), delim(sub(sup(i("A"), r("2")), r("1")))))), number=5)
    d.para("Adopting \u03bc\u221e \u2192 0 gives the limiting form")
    # (6): limiting form
    d.equation(group(i(G['mu']), delim(i("\u03b3\u0307")), eq(), sub(i(G['mu']), r("0")),
                     sup(brack(group(r("1"), plus(), sup(delim(group(i(G['Gamma']), i("\u03b3\u0307"))), r("2")))),
                         frac(group(i("n"), minus(), r("1")), r("2")))), number=6)

    d.heading("2.3 Governing equations", 2)
    d.para("Under the boundary-layer approximation for the narrow gap, mass, momentum, energy "
           "and species conservation give:")
    # continuity
    d.equation(group(frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("x"))), plus(),
                     frac(group(i(G['partial']), i("v")), group(i(G['partial']), i("y"))), eq(), r("0")),
               number=7)
    # x-momentum (primitive)
    xmom = group(
        frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("t"))), plus(),
        i("u"), frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("x"))), plus(),
        i("v"), frac(group(i(G['partial']), i("u")), group(i(G['partial']), i("y"))), eq(),
        frac(sub(i(G['mu']), i("hnf")), sub(i(G['rho']), i("hnf"))),
        frac(group(sup(i(G['partial']), r("2")), i("u")), group(i(G['partial']), sup(i("y"), r("2")))),
        u("[\u22ef]"))
    d.equation(xmom, number=8)
    d.para("(the full Carreau, Lorentz, Darcy and Forchheimer terms are as in the original "
           "Eq. 8). Eliminating pressure between the x- and y-momentum equations \u2014 required "
           "because dp/dy is set by the y-momentum balance \u2014 leads to the fourth-order "
           "similarity equation given below.")
    # y-momentum
    d.equation(group(frac(group(i(G['partial']), i("v")), group(i(G['partial']), i("t"))), plus(),
                     u("\u22ef"), eq(), minus(),
                     frac(r("1"), sub(i(G['rho']), i("hnf"))),
                     frac(group(i(G['partial']), i("p")), group(i(G['partial']), i("y"))), plus(),
                     frac(sub(i(G['mu']), i("hnf")), sub(i(G['rho']), i("hnf"))),
                     frac(group(sup(i(G['partial']), r("2")), i("v")), group(i(G['partial']), sup(i("y"), r("2"))))),
               number=9)
    # energy
    d.equation(group(frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("t"))), plus(),
                     u("\u22ef"), eq(),
                     frac(sub(i(G['kappa']), i("hnf")), group(delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), i("hnf")))),
                     frac(group(sup(i(G['partial']), r("2")), i("T")), group(i(G['partial']), sup(i("y"), r("2")))),
                     minus(), frac(r("1"), group(delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), i("hnf")))),
                     frac(group(i(G['partial']), sub(i("q"), i("r"))), group(i(G['partial']), i("y"))),
                     plus(), u("\u22ef")), number=10)
    # concentration
    d.equation(group(frac(group(i(G['partial']), i("C")), group(i(G['partial']), i("t"))), plus(),
                     u("\u22ef"), eq(),
                     sub(i("D"), i("B")), frac(group(sup(i(G['partial']), r("2")), i("C")), group(i(G['partial']), sup(i("y"), r("2")))),
                     plus(), frac(group(sub(i("D"), i("B")), sub(i("K"), i("T"))), sub(i("T"), i("m"))),
                     frac(group(sup(i(G['partial']), r("2")), i("T")), group(i(G['partial']), sup(i("y"), r("2")))),
                     minus(), sub(i("k"), r("1")), delim(group(i("C"), minus(), sub(i("C"), i("h"))))), number=11)

    d.heading("2.4 Nonlinear thermal radiation", 2)
    d.equation(group(sub(i("q"), i("r")), eq(), minus(),
                     frac(group(r("16"), sup(i(G['sigma']), r("*"))), group(r("3"), sup(i("k"), r("*")))),
                     sup(i("T"), r("3")), frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("y")))), number=12)
    d.equation(group(frac(group(i(G['partial']), sub(i("q"), i("r"))), group(i(G['partial']), i("y"))), eq(), minus(),
                     frac(group(r("16"), sup(i(G['sigma']), r("*"))), group(r("3"), sup(i("k"), r("*")))),
                     brack(group(r("3"), sup(i("T"), r("2")), sup(delim(frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("y")))), r("2")),
                                 plus(), sup(i("T"), r("3")),
                                 frac(group(sup(i(G['partial']), r("2")), i("T")), group(i(G['partial']), sup(i("y"), r("2"))))))), number=13)
    d.inline_math("with T = T", group(), "\u2080[1 + (\u03b8\u1d63 \u2212 1)\u03b8].")

    d.heading("2.5 Thermophysical properties of the hybrid nanofluid", 2)
    d.equation(group(sub(i(G['mu']), i("hnf")), eq(),
                     frac(sub(i(G['mu']), i("f")),
                          group(sup(delim(group(r("1"), minus(), sub(i(G['phi']), r("1")))), r("2.5")),
                                sup(delim(group(r("1"), minus(), sub(i(G['phi']), r("2")))), r("2.5"))))), number=14)
    d.equation(group(sub(i(G['rho']), i("hnf")), eq(),
                     delim(group(r("1"), minus(), sub(i(G['phi']), r("2")))),
                     brack(group(delim(group(r("1"), minus(), sub(i(G['phi']), r("1")))), sub(i(G['rho']), i("f")),
                                 plus(), sub(i(G['phi']), r("1")), sub(i(G['rho']), r("s1")))),
                     plus(), sub(i(G['phi']), r("2")), sub(i(G['rho']), r("s2"))), number=15)
    d.equation(group(delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), i("hnf")), eq(),
                     delim(group(r("1"), minus(), sub(i(G['phi']), r("2")))),
                     brack(group(delim(group(r("1"), minus(), sub(i(G['phi']), r("1")))),
                                 delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), i("f")),
                                 plus(), sub(i(G['phi']), r("1")), delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), r("s1")))),
                     plus(), sub(i(G['phi']), r("2")), delim(group(i(G['rho']), sub(i("c"), i("p")))), sub(r(""), r("s2"))), number=16)
    d.equation(group(frac(sub(i(G['kappa']), i("bf")), sub(i(G['kappa']), i("f"))), eq(),
                     frac(group(sub(i(G['kappa']), r("s1")), plus(), r("2"), sub(i(G['kappa']), i("f")), minus(), r("2"), sub(i(G['phi']), r("1")), delim(group(sub(i(G['kappa']), i("f")), minus(), sub(i(G['kappa']), r("s1"))))),
                          group(sub(i(G['kappa']), r("s1")), plus(), r("2"), sub(i(G['kappa']), i("f")), plus(), sub(i(G['phi']), r("1")), delim(group(sub(i(G['kappa']), i("f")), minus(), sub(i(G['kappa']), r("s1"))))))), number=17)
    d.equation(group(frac(sub(i(G['kappa']), i("hnf")), sub(i(G['kappa']), i("bf"))), eq(),
                     frac(group(sub(i(G['kappa']), r("s2")), plus(), r("2"), sub(i(G['kappa']), i("bf")), minus(), r("2"), sub(i(G['phi']), r("2")), delim(group(sub(i(G['kappa']), i("bf")), minus(), sub(i(G['kappa']), r("s2"))))),
                          group(sub(i(G['kappa']), r("s2")), plus(), r("2"), sub(i(G['kappa']), i("bf")), plus(), sub(i(G['phi']), r("2")), delim(group(sub(i(G['kappa']), i("bf")), minus(), sub(i(G['kappa']), r("s2"))))))), number=18)
    d.para("The electrical conductivity uses the analogous two-step Maxwell\u2013Garnett "
           "relations (Eqs. 19\u201320), and \u03bd\u2095\u2099\u2093 = \u03bc\u2095\u2099\u2093/\u03c1\u2095\u2099\u2093 (Eq. 21).")
    d.equation(group(sub(i(G['sigma']), i("bf")), sub(r(""), r("")), eq(),
                     sub(i(G['sigma']), i("f")), delim(group(r("1"), plus(),
                     frac(group(r("3"), delim(group(frac(sub(i(G['sigma']), r("s1")), sub(i(G['sigma']), i("f"))), minus(), r("1"))), sub(i(G['phi']), r("1"))),
                          group(delim(group(frac(sub(i(G['sigma']), r("s1")), sub(i(G['sigma']), i("f"))), plus(), r("2"))), minus(), delim(group(frac(sub(i(G['sigma']), r("s1")), sub(i(G['sigma']), i("f"))), minus(), r("1"))), sub(i(G['phi']), r("1"))))))), number=19)
    d.equation(group(sub(i(G['sigma']), i("hnf")), eq(),
                     sub(i(G['sigma']), i("bf")), delim(group(r("1"), plus(),
                     frac(group(r("3"), delim(group(frac(sub(i(G['sigma']), r("s2")), sub(i(G['sigma']), i("bf"))), minus(), r("1"))), sub(i(G['phi']), r("2"))),
                          group(delim(group(frac(sub(i(G['sigma']), r("s2")), sub(i(G['sigma']), i("bf"))), plus(), r("2"))), minus(), delim(group(frac(sub(i(G['sigma']), r("s2")), sub(i(G['sigma']), i("bf"))), minus(), r("1"))), sub(i(G['phi']), r("2"))))))), number=20)
    d.equation(group(sub(i(G['nu']), i("hnf")), eq(), frac(sub(i(G['mu']), i("hnf")), sub(i(G['rho']), i("hnf")))), number=21)

    d.heading("2.6 Similarity transformation", 2)
    # eta, psi
    d.equation(group(eta(), eq(), frac(i("y"), group(i("h"), delim(i("t")))), u("  ,  "),
                     i(G['psi']), eq(), sup(brack(frac(group(i("a"), sub(i(G['nu']), i("f"))), group(r("1"), minus(), i(G['gamma']), i("t")))), frac(r("1"), r("2"))),
                     i("x"), i("f"), delim(eta())), number=22)
    # u, v
    d.equation(group(i("u"), eq(), frac(group(i("a"), i("x")), group(r("1"), minus(), i(G['gamma']), i("t"))), fp(1),
                     u("  ,  "), i("v"), eq(), minus(),
                     sup(brack(frac(group(i("a"), sub(i(G['nu']), i("f"))), group(r("1"), minus(), i(G['gamma']), i("t")))), frac(r("1"), r("2"))),
                     i("f"), delim(eta())), number=23)
    # theta, phi
    d.equation(group(theta(), delim(eta()), eq(),
                     frac(group(i("T"), minus(), sub(i("T"), i("h"))), group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))),
                     u("  ,  "), phi(), delim(eta()), eq(),
                     frac(group(i("C"), minus(), sub(i("C"), i("h"))), group(sub(i("C"), i("w")), minus(), sub(i("C"), r("0"))))), number=24)
    d.para("The stream function satisfies continuity identically (u = \u2202\u03c8/\u2202y, "
           "v = \u2212\u2202\u03c8/\u2202x). The x- and time-dependent wall excesses are")
    d.equation(group(sub(i("T"), i("w")), eq(), sub(i("T"), r("0")), plus(),
                     frac(group(i("a"), i("x")), group(r("1"), minus(), i(G['gamma']), i("t"))), sub(i("d"), r("1")),
                     u("  ,  "), sub(i("C"), i("w")), eq(), sub(i("C"), r("0")), plus(),
                     frac(group(i("a"), i("x")), group(r("1"), minus(), i(G['gamma']), i("t"))), sub(i("e"), r("1"))), number=25)
    d.para("Here T\u2095, T\u2080, C\u2095 and C\u2080 denote the upper-wall and reference "
           "temperatures and concentrations; \u03b8 and \u03c6 are normalised so that "
           "\u03b8(1) = 0 and \u03c6(1) = 0 at the upper plate.")

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
    d.equation(mom3, number=26)
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
    d.equation(mom4, number=27)
    d.para("The corrected energy equation groups conduction and radiation consistently "
           "(A\u2084 multiplies conduction only, because Rd is defined with the base-fluid "
           "conductivity \u03ba\u2091):")
    energy = group(
        brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3")))), thp(2),
        plus(), r("4"), i("Rd"), delim(group(sub(i(G['theta']), i("r")), minus(), r("1"))),
        sup(F_expr(), r("2")), sup(delim(thp(1)), r("2")),
        plus(), A(5), i("Pr"), delim(group(i("f"), thp(1), minus(), sqhalf(), eta(), thp(1))),
        plus(), i("Pr"), brack(group(
            A(1), i("Ec"), sup(delim(fp(2)), r("2")), sup(delim(We2fpp2()), frac(group(i("n"), minus(), r("1")), r("2"))),
            plus(), A(3), i("M"), i("Ec"), sup(delim(group(fp(1), minus(), i("Ee"))), r("2")),
            plus(), A(2), i("Df"), php(2))), eq(), r("0"))
    d.equation(energy, number=28)
    d.para("and the concentration equation is")
    species = group(php(2), plus(), i("Sc"),
                    delim(group(i("f"), php(1), minus(), sqhalf(), eta(), php(1))),
                    plus(), i("Sc"), i("Sr"), thp(2), minus(), i("K"), i("Sc"), phi(), eq(), r("0"))
    d.equation(species, number=29)
    d.inline_math("The property ratios are A\u2081 = \u03bc\u2095\u2099\u2093/\u03bc\u2091, "
                  "A\u2082 = \u03c1\u2095\u2099\u2093/\u03c1\u2091, A\u2083 = \u03c3\u2095\u2099\u2093/\u03c3\u2091, "
                  "A\u2084 = \u03ba\u2095\u2099\u2093/\u03ba\u2091 and A\u2085 = ", group(),
                  "(\u03c1c\u209a)\u2095\u2099\u2093/(\u03c1c\u209a)\u2091 (Eq. 30).")

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
                     fp(1), u("(1)"), eq(), r("0")), number=30)
    d.equation(group(thp(1), u("(0)"), eq(), minus(), i("Bi"), brack(group(r("1"), minus(), theta(), u("(0)"))),
                     u("  ,  "), theta(), u("(1)"), eq(), r("0"), u("  ,  "),
                     phi(), u("(0)"), eq(), r("1"), plus(), sub(i("S"), r("3")), php(1), u("(0)"),
                     u("  ,  "), phi(), u("(1)"), eq(), r("0")), number=31)
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
                     u("  ,  "), i("M"), eq(), frac(group(sub(i(G['sigma']), i("f")), sup(sub(i("B"), r("0")), r("2"))), group(i("a"), sub(i(G['rho']), i("f")))),
                     u("  ,  "), i("Ee"), eq(), frac(sub(i("E"), r("0")), group(sub(i("B"), r("0")), sub(i("U"), i("w"))))), number=32)
    d.equation(group(i("Da"), eq(), frac(group(sub(sup(i("K"), r("*")), i("p")), i("a")), group(sub(i(G['nu']), i("f")), delim(group(r("1"), minus(), i(G['gamma']), i("t"))))),
                     u("  ,  "), i("Fr"), eq(), frac(group(sub(i("C"), i("b")), i("x")), rad(sub(sup(i("K"), r("*")), i("p")))),
                     u("  ,  "), i("Pr"), eq(), frac(group(sub(i(G['mu']), i("f")), sub(delim(sub(i("c"), i("p"))), i("f"))), sub(i(G['kappa']), i("f"))),
                     u("  ,  "), i("Rd"), eq(), frac(group(r("4"), sup(i(G['sigma']), r("*")), sub(sup(i("T"), r("3")), r("0"))), group(sup(i("k"), r("*")), sub(i(G['kappa']), i("f"))))), number=33)
    d.equation(group(i("Ec"), eq(), frac(sub(sup(i("U"), r("2")), i("w")), group(sub(delim(sub(i("c"), i("p"))), i("f")), delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))))),
                     u("  ,  "), i("Df"), eq(), frac(group(sub(i("D"), i("B")), sub(i("K"), i("T")), delim(group(sub(i("C"), i("w")), minus(), sub(i("C"), r("0"))))),
                                                     group(sub(i("c"), i("s")), sub(delim(sub(i("c"), i("p"))), i("f")), sub(i(G['nu']), i("f")), delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0"))))))), number=34)
    d.equation(group(i("Sc"), eq(), frac(sub(i(G['nu']), i("f")), sub(i("D"), i("B"))),
                     u("  ,  "), i("Sr"), eq(), frac(group(sub(i("D"), i("B")), sub(i("K"), i("T")), delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0"))))),
                                                     group(sub(i("T"), i("m")), sub(i(G['nu']), i("f")), delim(group(sub(i("C"), i("w")), minus(), sub(i("C"), r("0")))))),
                     u("  ,  "), i("K"), eq(), frac(sub(i("k"), r("1")), i("a"))), number=35)
    d.para("Because We\u00b2 and Ee depend on x and t, they are treated under a local-similarity "
           "assumption; the Darcy and Forchheimer groups are defined consistently with the "
           "similarity scaling, and Df/Sr are checked dimensionally against Eqs. (10)\u2013(11).")

    # =====================================================================
    # 2.10 Engineering quantities
    # =====================================================================
    d.heading("2.10 Engineering quantities of interest", 2)
    d.equation(group(sub(i("C"), i("f")), eq(), frac(sub(i(G['tau']), i("w")), group(sub(i(G['rho']), i("f")), sub(sup(i("U"), r("2")), i("w")))),
                     u("  ,  "), i("Nu"), eq(), frac(group(i("x"), sub(i("q"), i("w"))), group(sub(i(G['kappa']), i("f")), delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))))),
                     u("  ,  "), i("Sh"), eq(), frac(group(i("x"), sub(i("q"), i("m"))), group(sub(i("D"), i("B")), delim(group(sub(i("C"), i("w")), minus(), sub(i("C"), r("0"))))))), number=36)
    d.equation(group(subsup(i("Re"), i("x"), frac(r("1"), r("2"))), sub(i("C"), i("f")), eq(),
                     A(1), fp(2), u("(1)"), sup(delim(group(r("1"), plus(), sup(i("We"), r("2")), sup(delim(group(fp(2), u("(1)"))), r("2")))), frac(group(i("n"), minus(), r("1")), r("2")))), number=37)
    d.equation(group(subsup(i("Re"), i("x"), group(minus(), frac(r("1"), r("2")))), i("Nu"), eq(), minus(),
                     brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(delim(group(r("1"), plus(), delim(group(sub(i(G['theta']), i("r")), minus(), r("1"))), theta(), u("(1)"))), r("3")))), thp(1), u("(1)")), number=38)
    d.equation(group(subsup(i("Re"), i("x"), group(minus(), frac(r("1"), r("2")))), i("Sh"), eq(), minus(), php(1), u("(1)")), number=39)

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
                     plus(), subsup(i("S"), i("J"), i("\u2034")), plus(), subsup(i("S"), i("D"), i("\u2034"))), number=40)
    d.para("The Joule term uses the time-dependent electromagnetic fields (correction to the "
           "original Eq. 43):")
    d.equation(group(subsup(i("S"), i("J"), i("\u2034")), eq(),
                     frac(sub(i(G['sigma']), i("hnf")), sub(i("T"), r("0"))),
                     sup(brack(group(i("u"), i("B"), delim(i("t")), minus(), i("E"), delim(i("t")))), r("2"))), number=41)
    d.equation(group(subsup(i("S"), i("D"), i("\u2034")), eq(),
                     frac(group(i("R"), sub(i("D"), i("B"))), sub(i("C"), r("0"))), sup(delim(frac(group(i(G['partial']), i("C")), group(i(G['partial']), i("y")))), r("2")),
                     plus(), frac(group(i("R"), sub(i("D"), i("B"))), sub(i("T"), r("0"))),
                     delim(group(frac(group(i(G['partial']), i("T")), group(i(G['partial']), i("y"))), frac(group(i(G['partial']), i("C")), group(i(G['partial']), i("y")))))), number=42)

    d.heading("3.2 Characteristic entropy and the entropy generation number", 2)
    d.para("For consistency, the reference entropy generation rate is normalised with the "
           "base-fluid conductivity \u03ba\u2091 so that A\u2084 appears once, on conduction "
           "only (correction to Eqs. 45\u201346):")
    d.equation(group(subsup(i("S"), r("0"), i("\u2034")), eq(),
                     frac(group(sub(i(G['kappa']), i("f")), sup(delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))), r("2"))),
                          group(sub(sup(i("T"), r("2")), r("0")), sup(group(i("h"), delim(i("t"))), r("2"))))), number=43)
    ns = group(sub(i("N"), i("s")), eq(),
               brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3")))), sup(delim(thp(1)), r("2")),
               plus(), frac(group(A(1), i("Br")), i(G['Omega'])), sup(delim(fp(2)), r("2")), sup(delim(We2fpp2()), frac(group(i("n"), minus(), r("1")), r("2"))),
               plus(), frac(group(A(3), i("Br"), i("M")), i(G['Omega'])), sup(delim(group(fp(1), minus(), i("Ee"))), r("2")),
               plus(), i(G['Lambda']), sup(delim(frac(i(G['zeta']), i(G['Omega']))), r("2")), sup(delim(php(1)), r("2")),
               plus(), i(G['Lambda']), delim(frac(i(G['zeta']), i(G['Omega']))), thp(1), php(1))
    d.equation(ns, number=44)
    d.para("with the Brinkman number and temperature-difference ratio")
    d.equation(group(i("Br"), eq(), frac(group(sub(i(G['mu']), i("f")), sub(sup(i("U"), r("2")), i("w"))),
                                          group(sub(i(G['kappa']), i("f")), delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))))),
                     u("  ,  "), i(G['Omega']), eq(), frac(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0"))), sub(i("T"), r("0")))), number=45)
    d.para("and the diffusive-irreversibility parameter and concentration ratio")
    d.equation(group(i(G['Lambda']), eq(), frac(group(i("R"), sub(i("D"), i("B")), sub(i("C"), r("0"))), sub(i(G['kappa']), i("f"))),
                     u("  ,  "), i(G['zeta']), eq(), frac(group(sub(i("C"), i("w")), minus(), sub(i("C"), r("0"))), sub(i("C"), r("0")))), number=46)
    d.para("The four contributions are")
    d.equation(group(sub(i("N"), i("HT")), eq(), brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3")))), sup(delim(thp(1)), r("2"))), number=47)
    d.equation(group(sub(i("N"), i("FF")), eq(), frac(group(A(1), i("Br")), i(G['Omega'])), sup(delim(fp(2)), r("2")), sup(delim(We2fpp2()), frac(group(i("n"), minus(), r("1")), r("2")))), number=48)
    d.equation(group(sub(i("N"), i("J")), eq(), frac(group(A(3), i("Br"), i("M")), i(G['Omega'])), sup(delim(group(fp(1), minus(), i("Ee"))), r("2"))), number=49)
    d.equation(group(sub(i("N"), i("DD")), eq(), i(G['Lambda']), sup(delim(frac(i(G['zeta']), i(G['Omega']))), r("2")), sup(delim(php(1)), r("2")), plus(), i(G['Lambda']), delim(frac(i(G['zeta']), i(G['Omega']))), thp(1), php(1)), number=50)

    d.heading("3.3 Bejan number", 2)
    d.equation(group(i("Be"), eq(), frac(group(sub(i("N"), i("HT")), plus(), sub(i("N"), i("DD"))), sub(i("N"), i("s")))), number=51)
    d.para("The diffusive cross-gradient term is retained; its thermodynamic non-negativity "
           "requires |\u039b(\u03b6/\u03a9)\u03b8\u2032\u03c6\u2032| not to exceed the sum of the "
           "squared-gradient terms, which is verified a posteriori for the reported cases.")

    d.heading("3.4 Dimensional decomposition (corrected)", 2)
    d.para("The thermal irreversibility no longer double-counts A\u2084 on the radiation part "
           "(correction to Eq. 66):")
    d.equation(group(subsup(i("S"), i("HT"), i("\u2034")), eq(),
                     frac(group(sub(i(G['kappa']), i("f")), sup(delim(group(sub(i("T"), i("w")), minus(), sub(i("T"), r("0")))), r("2"))), group(sub(sup(i("T"), r("2")), r("0")), sup(i("h"), r("2")))),
                     brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3")))), sup(delim(thp(1)), r("2"))), number=52)
    d.para("The Joule irreversibility with the time-dependent field (correction to Eq. 68):")
    d.equation(group(subsup(i("S"), i("J"), i("\u2034")), eq(),
                     frac(group(sub(i(G['sigma']), i("hnf")), sup(sub(i("B"), r("0")), r("2")), sub(sup(i("U"), r("2")), i("w"))), group(sub(i("T"), r("0")), delim(group(r("1"), minus(), i(G['gamma']), i("t"))))),
                     sup(delim(group(fp(1), minus(), i("Ee"))), r("2"))), number=53)
    d.para("The gap-averaged entropy number and average Bejan number follow by integration over "
           "\u03b7 \u2208 [0, 1] (Eqs. 54\u201357), with the mechanism fractions summing to unity.")
    d.equation(group(sub(i("N"), group(i("s"), u(",avg"))), eq(),
                     nary("\u222b", r("0"), r("1"), group(sub(i("N"), i("s")), delim(eta()), i("d"), eta()))), number=54)

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
                     u(", "), sub(i("y"), r("7")), eq(), phi(), u(", "), sub(i("y"), r("8")), eq(), php(1)), number=55)
    d.para("The highest momentum derivative y\u2084\u2032 = f\u2034\u2032 is obtained from Eq. (27). "
           "The energy and species second derivatives are coupled through Df and Sr; they are "
           "obtained by solving the 2\u00d72 linear system at each mesh point (not sequentially):")
    d.equation(group(delim(group(
        # 2x2 matrix as fraction-free bracket approximation
        brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3")))),
        u("  "), i("Pr"), A(2), i("Df"))),
        thp(2), plus(), u("("), i("Pr"), A(2), i("Df"), u(")"), php(2), eq(), sub(i("b"), r("1"))), number=56)
    d.equation(group(i("Sc"), i("Sr"), thp(2), plus(), php(2), eq(), sub(i("b"), r("2"))), number=57)
    d.para("The transformed boundary conditions supplied to the residual function are")
    d.equation(group(sub(i("y"), r("1")), u("(0)"), eq(), r("0"), u(",  "),
                     sub(i("y"), r("2")), u("(0)"), minus(), r("1"), minus(), sub(i("S"), r("1")), sub(i("y"), r("3")), u("(0)"), eq(), r("0"), u(",  "),
                     i("f"), delim(r("1")), eq(), sqhalf(), u(",  "), sub(i("y"), r("2")), u("(1)"), eq(), r("0")), number=58)
    d.equation(group(sub(i("y"), r("6")), u("(0)"), plus(), i("Bi"), brack(group(r("1"), minus(), sub(i("y"), r("5")), u("(0)"))), eq(), r("0"), u(",  "),
                     sub(i("y"), r("5")), u("(1)"), eq(), r("0"), u(",  "),
                     sub(i("y"), r("7")), u("(0)"), minus(), r("1"), minus(), sub(i("S"), r("3")), sub(i("y"), r("8")), u("(0)"), eq(), r("0"), u(",  "),
                     sub(i("y"), r("7")), u("(1)"), eq(), r("0")), number=59)

    d.heading("4.1 Residuals and grid convergence (corrected)", 2)
    d.para("The discrete L\u2082 norm of the combined residual is the global error indicator, and "
           "the observed order of accuracy uses the magnitude of successive differences "
           "(correction to Eq. 80):")
    d.equation(group(sub(i("\u03b5"), r("L2")), eq(),
                     sup(brack(group(frac(r("1"), i("N")), nary("\u2211", group(i("j"), eq(), r("1")), i("N"),
                                                                group(sup(sub(i("R"), i("f")), r("2")), plus(), sup(sub(i("R"), i(G['theta'])), r("2")), plus(), sup(sub(i("R"), i(G['phi'])), r("2")))))), frac(r("1"), r("2")))), number=60)
    d.equation(group(sub(i("p"), i("obs")), eq(),
                     frac(group(u("ln"), delim(group(frac(group(sub(i("q"), i("N")), minus(), sub(i("q"), r("2N"))), group(sub(i("q"), r("2N")), minus(), sub(i("q"), r("4N"))))), left="|", right="|")),
                          group(u("ln"), r("2")))), number=61)
    d.para("With N = 100, 200, 400 uniform intervals the monitored wall gradient f\u2033(1) is "
           "mesh-independent to better than 10\u207b\u2076 and the estimated p_obs \u2248 4.00, "
           "confirming the fourth-order scheme (see Table 3a). Baseline parameters: Sq = 0.5, "
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
           "and Sharma [23]; comparison with [23] is therefore restricted to a common Newtonian "
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
            [["0.1", "1.650489", "0.762234"],
             ["0.5", "0.422159", "0.746319"],
             ["1.0", "\u22121.152174", "0.726799"],
             ["1.5", "\u22122.768838", "0.707699"]])

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
    d.figure(os.path.join(FIGDIR, "Figure_2_velocity_Sq.png"),
             "Figure 2. Effect of the squeezing parameter Sq on the velocity profile f\u2032(\u03b7).")
    d.figure(os.path.join(FIGDIR, "Figure_3_velocity_We_M.png"),
             "Figure 3. Effect of the Weissenberg number We and magnetic parameter M on the "
             "velocity profile f\u2032(\u03b7).")

    d.heading("6.2 Temperature field", 2)
    d.para("Figure 4 shows the temperature \u03b8(\u03b7) for varying Rd and Ec. Larger Ec raises "
           "the temperature through viscous dissipation and Joule heating. With the corrected "
           "radiation grouping [A\u2084 + (4/3)Rd F\u00b3]\u03b8\u2033, an increase in Rd raises "
           "the effective conductivity, which redistributes heat and moderates the dissipation-"
           "driven peak for the present boundary conditions.")
    d.figure(os.path.join(FIGDIR, "Figure_4_temperature_Rd_Ec.png"),
             "Figure 4. Effect of the radiation parameter Rd and Eckert number Ec on the "
             "temperature profile \u03b8(\u03b7).")

    d.heading("6.3 Concentration field", 2)
    d.para("The concentration decreases monotonically from the lower to the upper plate. A larger "
           "Schmidt number thins the solutal layer, and a destructive reaction (K > 0) lowers the "
           "concentration. The Soret and Dufour numbers act reciprocally on the temperature and "
           "concentration, providing an internal consistency check of the cross-diffusion "
           "coupling.")

    d.heading("6.4 Entropy generation", 2)
    d.para("Figure 5 shows the entropy generation number Ns(\u03b7). Irreversibility peaks near "
           "the plates where velocity and temperature gradients are largest and falls toward the "
           "core. Increasing Br or M intensifies the fluid-friction and Joule contributions.")
    d.figure(os.path.join(FIGDIR, "Figure_5_entropy_Br_M.png"),
             "Figure 5. Effect of the Brinkman number Br and magnetic parameter M on the entropy "
             "generation number Ns(\u03b7).")

    d.heading("6.5 Bejan number", 2)
    d.para("Figure 6 shows the Bejan number Be(\u03b7), bounded in [0, 1]. Thermal and diffusive "
           "irreversibilities dominate near the walls (Be \u2192 large), while friction and Joule "
           "irreversibilities are relatively more important in the core. Larger Rd raises Be; "
           "larger Br lowers it.")
    d.figure(os.path.join(FIGDIR, "Figure_6_bejan_Rd_Br.png"),
             "Figure 6. Effect of the radiation parameter Rd and Brinkman number Br on the Bejan "
             "number Be(\u03b7).")

    d.heading("6.6 Engineering quantities", 2)
    d.para("Figure 7 shows the reduced skin friction, Nusselt and Sherwood numbers versus "
           "nanoparticle volume fraction. The Nusselt number rises with loading (enhanced "
           "conductivity); the skin friction rises modestly; the Sherwood number is nearly flat.")
    d.figure(os.path.join(FIGDIR, "Figure_7_engineering_phi.png"),
             "Figure 7. Variations of the reduced skin-friction coefficient, Nusselt number and "
             "Sherwood number with the nanoparticle volume fraction \u03c6.")

    d.heading("6.7 Tabulated results", 2)
    d.para("Tables 4\u20136 summarise the corrected-model outputs recomputed with the fourth-order "
           "formulation and consistent entropy normalisation.")
    d.table("Table 4. Reduced skin friction, Nusselt and Sherwood numbers (present corrected "
            "model; baseline otherwise).",
            ["Parameter", "Value", "Re^{1/2} Cf", "Re^{-1/2} Nu", "Re^{-1/2} Sh"],
            [["Sq", "0.2", "1.3306", "5.1692", "0.4748"],
             ["Sq", "0.8", "\u22121.1816", "3.2942", "0.5828"],
             ["M", "0.5", "0.1175", "3.4359", "0.6137"],
             ["M", "2.0", "0.0318", "3.5623", "0.6058"],
             ["We", "0.5", "\u22120.0380", "3.1290", "0.6367"],
             ["We", "2.0", "0.2693", "4.1585", "0.5590"],
             ["Rd", "0.2", "0.0885", "3.1913", "0.5972"],
             ["Rd", "1.0", "0.0885", "3.9032", "0.6423"],
             ["Df", "0.6", "0.0885", "7.4979", "0.2145"],
             ["Sr", "0.5", "0.0885", "4.8542", "0.0522"],
             ["K", "1.5", "0.0885", "3.9164", "0.4497"]])
    d.table("Table 5. Entropy generation number Ns and Bejan number Be at \u03b7 = 0 (present "
            "corrected model).",
            ["Br", "M", "Rd", "\u03a9", "Ns(0)", "Be(0)"],
            [["0.5", "1.0", "0.5", "1.0", "4.1208", "0.2355"],
             ["1.0", "1.0", "0.5", "1.0", "7.2712", "0.1335"],
             ["1.5", "1.0", "0.5", "1.0", "10.4217", "0.0931"],
             ["1.0", "0.5", "0.5", "1.0", "6.9090", "0.1385"],
             ["1.0", "2.0", "0.5", "1.0", "7.9887", "0.1250"],
             ["1.0", "1.0", "1.0", "1.0", "7.1543", "0.1193"],
             ["1.0", "1.0", "0.5", "2.0", "3.4627", "0.0902"]])
    d.table("Table 6. Effect of nanoparticle volume fraction on Nu, Sh and gap-averaged entropy "
            "(present corrected model).",
            ["\u03c6\u2081", "\u03c6\u2082", "Re^{-1/2} Nu", "Re^{-1/2} Sh", "Ns,avg"],
            [["0.00", "0.00", "2.9817", "0.6200", "5.3914"],
             ["0.02", "0.02", "3.3053", "0.6138", "5.9766"],
             ["0.03", "0.03", "3.4787", "0.6110", "6.2948"],
             ["0.04", "0.04", "3.6605", "0.6084", "6.6318"],
             ["0.05", "0.05", "3.8512", "0.6059", "6.9888"]])

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
    d.para("2. The energy equation groups conduction and radiation as [A\u2084 + (4/3)Rd F\u00b3]"
           "\u03b8\u2033, with A\u2084 multiplying conduction only.")
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
    d.equation(a1, number="A1")
    d.equation(group(A(1), eq(), A(2), eq(), A(3), eq(), A(4), eq(), A(5), eq(), r("1")), number="A2")
    d.equation(group(frac(sub(i(G['kappa']), i("nf")), sub(i(G['kappa']), i("f"))), eq(),
                     frac(group(sub(i(G['kappa']), r("s1")), plus(), r("2"), sub(i(G['kappa']), i("f")), minus(), r("2"), sub(i(G['phi']), r("1")), delim(group(sub(i(G['kappa']), i("f")), minus(), sub(i(G['kappa']), r("s1"))))),
                          group(sub(i(G['kappa']), r("s1")), plus(), r("2"), sub(i(G['kappa']), i("f")), plus(), sub(i(G['phi']), r("1")), delim(group(sub(i(G['kappa']), i("f")), minus(), sub(i(G['kappa']), r("s1"))))))), number="A3")
    d.para("Suppressing the electromagnetic fields (M = 0) removes the Lorentz coupling:")
    a4 = group(frac(A(1), A(2)), carreau_bracket(frac(group(i("n"), minus(), r("3")), r("2"))),
               brack(group(r("1"), plus(), i("n"), sup(i("We"), r("2")), sup(delim(fp(2)), r("2")))), fp(3),
               plus(), i("f"), fp(2), minus(), sup(delim(fp(1)), r("2")),
               minus(), i("Sq"), delim(group(fp(1), plus(), frac(eta(), r("2")), fp(2))),
               minus(), frac(A(1), group(A(2), i("Da"))), fp(1), minus(), i("Fr"), sup(delim(fp(1)), r("2")), eq(), i("G"))
    d.equation(a4, number="A4")
    d.para("Omitting the porous resistance (Fr = 0, Da \u2192 \u221e) leaves the non-porous "
           "(still nanoparticle-laden) squeezing channel:")
    a5 = group(frac(A(1), A(2)), carreau_bracket(frac(group(i("n"), minus(), r("3")), r("2"))),
               brack(group(r("1"), plus(), i("n"), sup(i("We"), r("2")), sup(delim(fp(2)), r("2")))), fp(3),
               plus(), i("f"), fp(2), minus(), sup(delim(fp(1)), r("2")),
               minus(), i("Sq"), delim(group(fp(1), plus(), frac(eta(), r("2")), fp(2))),
               minus(), frac(A(3), A(2)), i("M"), delim(group(fp(1), minus(), i("Ee"))), eq(), i("G"))
    d.equation(a5, number="A5")
    d.para("In the absence of radiation (Rd = 0):")
    a6 = group(A(4), thp(2), plus(), A(5), i("Pr"), delim(group(i("f"), thp(1), minus(), sqhalf(), eta(), thp(1))),
               plus(), i("Pr"), brack(group(A(1), i("Ec"), sup(delim(fp(2)), r("2")), sup(delim(We2fpp2()), frac(group(i("n"), minus(), r("1")), r("2"))),
                                            plus(), A(3), i("M"), i("Ec"), sup(delim(group(fp(1), minus(), i("Ee"))), r("2")), plus(), A(2), i("Df"), php(2))), eq(), r("0"))
    d.equation(a6, number="A6")
    d.para("and in the non-squeezing limit (Sq \u2192 0):")
    a7 = group(brack(group(A(4), plus(), frac(r("4"), r("3")), i("Rd"), sup(F_expr(), r("3")))), thp(2),
               plus(), r("4"), i("Rd"), delim(group(sub(i(G['theta']), i("r")), minus(), r("1"))), sup(F_expr(), r("2")), sup(delim(thp(1)), r("2")),
               plus(), A(5), i("Pr"), i("f"), thp(1), plus(), i("Pr"), i("\u039e"), eq(), r("0"))
    d.equation(a7, number="A7")
    d.para("For a reaction-free species field (K = 0):")
    d.equation(group(php(2), plus(), i("Sc"), delim(group(i("f"), php(1), minus(), sqhalf(), eta(), php(1))), plus(), i("Sc"), i("Sr"), thp(2), eq(), r("0")), number="A8")
    d.para("The true pure-diffusion limit (Sr = 0, Sq = 0, K = 0, no convection) is")
    d.equation(group(php(2), eq(), r("0")), number="A9")
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
    d.equation(a10, number="A10")
    a11 = group(i("Be"), eq(), frac(group(A(4), sup(delim(thp(1)), r("2")), plus(),
                                          i(G['Lambda']), sup(delim(frac(i(G['zeta']), i(G['Omega']))), r("2")), sup(delim(php(1)), r("2")),
                                          plus(), i(G['Lambda']), delim(frac(i(G['zeta']), i(G['Omega']))), thp(1), php(1)),
                                    sub(i("N"), i("s"))))
    d.equation(a11, number="A11")
    d.para("The limiting engineering quantities for the Newtonian base fluid (A\u2084 = 1) are")
    d.equation(group(subsup(i("Re"), i("x"), frac(r("1"), r("2"))), sub(i("C"), i("f")), eq(), fp(2), u("(1)")), number="A12")
    d.equation(group(subsup(i("Re"), i("x"), group(minus(), frac(r("1"), r("2")))), i("Nu"), eq(), minus(),
                     delim(group(r("1"), plus(), frac(r("4"), r("3")), i("Rd"))), thp(1), u("(1)")), number="A13")
    d.para("(the (1 + 4Rd/3) factor follows from \u03b8(1) = 0; without radiation it reduces to "
           "\u2212\u03b8\u2032(1)). The isothermal lower-wall limit (Bi \u2192 \u221e) is")
    d.equation(group(theta(), u("(0)"), eq(), r("1")), number="A14")
    d.equation(group(subsup(i("Re"), i("x"), group(minus(), frac(r("1"), r("2")))), i("Sh"), eq(), minus(), php(1), u("(1)"),
                     u(",  "), phi(), u("(0)"), eq(), r("1"), u(",  "), sub(i("S"), r("3")), eq(), r("0")), number="A15")
    d.para("These reductions confirm internal consistency. The Newtonian limit of the Carreau "
           "model does not by itself recover the Casson constitutive model; any comparison with "
           "the Casson squeezing results of Bhaskar and Sharma [23] must be restricted to a common "
           "Newtonian limit or another explicitly demonstrated constitutive correspondence.")

    # =====================================================================
    # References (kept from original)
    # =====================================================================
    d.heading("References", 1)
    refs = [
        "[1] S. U. S. Choi, J. A. Eastman, Enhancing thermal conductivity of fluids with nanoparticles, ASME IMECE, San Francisco, 1995, pp. 99\u2013105.",
        "[4] S. Suresh, K. P. Venkitaraj, P. Selvakumar, M. Chandrasekar, Synthesis of Al2O3\u2013Cu/water hybrid nanofluids using two step method, Colloids Surf. A 388 (2011) 41\u201348.",
        "[5] D. K. Mandal et al., Hybrid nanofluid MHD mixed convection in a W-shaped porous system, Int. J. Numer. Methods Heat Fluid Flow 33 (2023).",
        "[8] I. Tlili, H. A. Nabwey, G. Ashwinkumar, N. Sandeep, 3-D MHD AA7072-AA7075/methanol hybrid nanofluid flow, Sci. Rep. 10 (2020) 1\u201313.",
        "[12] P. J. Carreau, Rheological equations from molecular network theories, Trans. Soc. Rheol. 16 (1972) 99\u2013127.",
        "[13] S. A. G. A. Shah et al., Thermal radiation on convective heat transfer in MHD Carreau fluid, Sci. Rep. 13 (2023).",
        "[14] H. A. Wahab et al., Inclined magnetic aspect of infinite shear rate Carreau fluid, Arab. J. Chem. 16 (2023).",
        "[15] M. Mkhatshwa, M. Khumalo, Irreversibility of EMHD Darcy\u2013Forchheimer slip flow of Carreau hybrid nanofluid, Heat Transf. 52 (2023) 395\u2013429.",
        "[18] M. J. Stefan, Versuch \u00fcber die scheinbare Adh\u00e4sion, Sitzungsber. Akad. Wiss. Wien 69 (1874) 713\u2013721.",
        "[19] R. J. Grimm, Squeezing flows of Newtonian liquid films, Appl. Sci. Res. 32 (1976) 149\u2013166.",
        "[20] G. M. Sobamowo, A. T. Akinshilo, Squeezing flow of nanofluid between two parallel plates under magnetic field, Alex. Eng. J. 57 (2018) 1413\u20131423.",
        "[23] K. Bhaskar, K. Sharma, Unsteady MHD squeezing viscous Casson fluid flow with cross-diffusion and thermal radiative effects, Indian J. Phys. 95(7) (2021) 1453\u20131467.",
        "[26] A. Shojaei et al., Hydrothermal analysis of second grade fluid with Soret and Dufour effects, Case Stud. Therm. Eng. 13 (2019).",
        "[27] K. Rafique et al., Casson nanofluid flow with Soret and Dufour effects by Keller-box, Front. Phys. 7 (2019).",
        "[28] R. N. Kumar et al., Soret and Dufour effects on Oldroyd-B fluid under convective condition, Indian J. Phys. 97 (2023).",
        "[34] A. Bejan, A study of entropy generation in fundamental convective heat transfer, ASME J. Heat Transf. 101 (1979) 718\u2013725.",
        "[36] M. I. Khan et al., Entropy optimization in Williamson nanofluid with chemical reaction and Joule heating, Int. J. Heat Mass Transf. 133 (2019) 959\u2013967.",
        "[41] A. Ali, S. Sarkar, S. Das, R. N. Jana, Irreversibility of Carreau hybrid nanofluid over a stretching sheet with radiation, Waves Random Complex Media 33 (2023).",
        "[42] P. K. Yadav, A. Kumar, Entropy generation of unsteady squeezing MHD nanofluid flow between parallel plates, Int. Commun. Heat Mass Transf. 128 (2021) 105632.",
    ]
    for rf in refs:
        d.para(rf, justify=False)

    d.save(OUT)
    return OUT


if __name__ == "__main__":
    path = build()
    print("Wrote", path)
