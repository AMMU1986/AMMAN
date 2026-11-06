# -*- coding: utf-8 -*-
from cb import *
# Reference list: ONLY the 15 DOIs taken from the reference list of the base paper [1].
# Pre-2013 classics (Lord-Shulman, Green-Lindsay, Tzou, Roychoudhuri, Chandrasekharaiah, Quintanilla-Racke)
# are named in the prose without numbers or DOIs; add them only if pre-2013 sources are wanted.
H1("References")
REFS = [
 ("R. V. Singh and S. Mukhopadhyay, \"Mathematical significance of strain rate and temperature rate on heat conduction in thermoelastic material due to line heat source,\" J. Therm. Stresses, vol. 46, no. 11, pp. 1164–1179, 2023.", "10.1080/01495739.2023.2246523"),
 ("R. V. Singh and S. Mukhopadhyay, \"An investigation on strain and temperature rate-dependent thermoelasticity and its infinite speed behavior,\" J. Therm. Stresses, vol. 43, no. 3, pp. 269–283, 2020.", "10.1080/01495739.2019.1680333"),
 ("B. Singh, M. Gupta and S. Mukhopadhyay, \"On the fundamental solutions for the strain and temperature rate-dependent generalized thermoelasticity theory,\" J. Therm. Stresses, vol. 43, no. 5, pp. 650–664, 2020.", "10.1080/01495739.2020.1736967"),
 ("M. Gupta and S. Mukhopadhyay, \"Galerkin-type solution for the theory of strain and temperature rate-dependent thermoelasticity,\" Acta Mech., vol. 230, no. 10, pp. 3633–3643, 2019.", "10.1007/s00707-019-02482-z"),
 ("O. N. Shivay and S. Mukhopadhyay, \"A complete Galerkin's type approach of finite element for the solution of a problem on modified Green–Lindsay thermoelasticity for a functionally graded hollow disk,\" Eur. J. Mech. A/Solids, vol. 80, p. 103914, 2020.", "10.1016/j.euromechsol.2019.103914"),
 ("I. M. Tayel and K. Lotfy, \"Photothermal effects in semiconductors induced by surface absorption of a uniform laser radiation under modified Green–Lindsay theory,\" Eur. Phys. J. Plus, vol. 136, no. 9, pp. 1–17, 2021.", "10.1140/epjp/s13360-021-01941-8"),
 ("R. V. Singh and S. Mukhopadhyay, \"Study of wave propagation in an infinite solid due to a line heat source under Moore–Gibson–Thompson thermoelasticity,\" Acta Mech., vol. 232, no. 12, pp. 4747–4760, 2021.", "10.1007/s00707-021-03073-7"),
 ("A. E. Abouelregal, I. E. Ahmed, M. E. Nasr, K. M. Khalil, A. Zakria and F. A. Mohammed, \"Thermoelastic processes by a continuous heat source line in an infinite solid via Moore–Gibson–Thompson thermoelasticity,\" Materials, vol. 13, no. 19, p. 4463, 2020.", "10.3390/ma13194463"),
 ("F. Shakeriaski, M. Ghodrat, J. Escobedo-Diaz and M. Behnia, \"Recent advances in generalized thermoelasticity theory and the modified models: a review,\" J. Comput. Des. Eng., vol. 8, no. 1, pp. 15–35, 2021.", "10.1093/jcde/qwaa082"),
 ("A. Krysko, J. Awrejcewicz, S. Pavlov, K. Bodyagina and V. Krysko, \"Topological optimization of thermoelastic composites with maximized stiffness and heat transfer,\" Compos. Part B: Eng., vol. 158, pp. 319–327, 2019.", "10.1016/j.compositesb.2018.09.047"),
 ("A. Babaee and J. Jelovica, \"Nonlinear transient thermoelastic response of FGM plate under sudden cryogenic cooling,\" Ocean Eng., vol. 226, p. 108875, 2021.", "10.1016/j.oceaneng.2021.108875"),
 ("A. Babaee and J. Jelovica, \"Large amplitude vibration of annular and circular functionally graded composite plates under cooling thermal shocks,\" Thin-Walled Struct., vol. 182, p. 110142, 2023.", "10.1016/j.tws.2022.110142"),
 ("A. Babaee, M. Sadighi, A. Nikbakht and S. Alimirzaei, \"Generalized differential quadrature nonlinear buckling analysis of smart SMA/FG laminated beam resting on nonlinear elastic medium under thermal loading,\" J. Therm. Stresses, vol. 41, no. 5, pp. 583–607, 2018.", "10.1080/01495739.2017.1408048"),
 ("Y. J. Yu, Z. N. Xue and X. G. Tian, \"A modified Green–Lindsay thermoelasticity with strain rate to eliminate the discontinuity,\" Meccanica, vol. 53, no. 10, pp. 2543–2554, 2018.", "10.1007/s11012-018-0843-1"),
 ("R. Quintanilla, \"Some qualitative results for a modification of the Green–Lindsay thermoelasticity,\" Meccanica, vol. 53, no. 14, pp. 3607–3613, 2018.", "10.1007/s11012-018-0889-0"),
]
for i, (t, d) in enumerate(REFS, 1):
    add(("ref", "[%d] %s DOI: " % (i, t), d))
add(("note", "NOTE (not a reference): the manuscript requires 34 references from 2013 to 2026, each with its DOI. Only 15 verified references are listed above (DOIs taken from the reference list of the base paper [1]). 19 more verified references (2013–2026) must be added to reach 34. No DOI was invented, because there was no network access to verify any additional one."))
