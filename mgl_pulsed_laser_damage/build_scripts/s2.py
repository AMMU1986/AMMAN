# -*- coding: utf-8 -*-
from vals import *

H1("2. Governing equations")
H2("2.1 Geometry, thermoelastic balance laws and constitutive relations")
P("The domain is the slab $0<x<L$ with $L=20$ mm. The tumour layer ($i=1$) occupies $0<x<h$ with $h=4$ mm and the normal tissue ($i=2$) occupies $h<x<L$. Fields carry the index $i$ of the layer. "
  "The laser enters at $x=0$. The displacement is $u_i(x,t)$, the temperature increment above the reference temperature $T_0=310$ K is $\\theta_i(x,t)$, and the absolute temperature is $T=T_0+\\theta$. "
  "The balance of linear momentum with the stress $\\sigma_i$ is")
EQ("\\rho_i\\,\\partial_t^2u_i=\\partial_x\\sigma_i", "mom")
P("The constitutive law of the modified Green–Lindsay theory applies the operator $1+\\tau_1\\partial_t$, with the strain-rate lag $\\tau_1$, to both the elastic and the thermal part of the stress,")
EQ("\\sigma_i=\\left(1+\\tau_1\\partial_t\\right)\\left[c_{11,i}\\,\\partial_xu_i-\\beta_i\\theta_i\\right],\\qquad c_{11,i}=\\lambda_i+2\\mu_i", "const")
P("with the thermoelastic modulus")
EQ("\\beta_i=\\left(3\\lambda_i+2\\mu_i\\right)\\alpha_{T,i}", "beta")
P("For the data of [13], $\\lambda_1=2.481\\times10^{7}$ Pa, $\\mu_1=1.034\\times10^{6}$ Pa, $\\lambda_2=8.27\\times10^{7}$ Pa and $\\mu_2=3.446\\times10^{6}$ Pa, and $\\alpha_T=10^{-4}$ K$^{-1}$ in both layers. "
  "The source lists these values in kg/(m s²), which is the unit of the pascal. They correspond to a Young modulus of " + f2(3.06) + " MPa in the tumour and " + f1(10.2) + " MPa in the normal tissue with a Poisson ratio of 0.48, which is in the range of soft tissue and is adopted without change. "
  "The resulting thermoelastic moduli are $\\beta_1=" + k0(LC[0]["beta"]) + "$ and $\\beta_2=" + k0(LC[1]["beta"]) + "$ Pa/K, and the longitudinal wave speeds are " + k0(LC[0]["cwave"]) + " and " + k0(LC[1]["cwave"]) + " m/s.")
H2("2.2 Energy equation for the four conduction models")
P("The energy balance contains the heat capacity, the thermoelastic coupling term, the perfusion sink and the laser source $Q$. The unified form used for all four models is")
EQ("\\left(1+\\tau_q\\partial_t\\right)\\left[\\rho_ic_{v,i}\\partial_t\\theta_i+T_0\\beta_i\\partial_t\\partial_xu_i+\\omega_i\\theta_i-Q\\right]+\\tau_0\\,\\partial_t\\left[\\rho_ic_{v,i}\\partial_t\\theta_i+T_0\\beta_i\\partial_t\\partial_xu_i\\right]=\\partial_x\\left(k_i\\partial_x\\theta_i\\right)+k_i^{*}\\partial_x^2v_i", "energy")
P("with the thermal displacement $v_i$ defined by")
EQ("\\partial_tv_i=\\theta_i", "vdef")
P("The four models are obtained by choosing the parameters. Pennes theory has $\\tau_q=\\tau_0=0$ and $k^*=0$. The Cattaneo–Vernotte (CV) model has $\\tau_q>0$, $\\tau_0=0$ and $k^*=0$. The Moore–Gibson–Thompson type model (MGT) has $\\tau_q>0$ and $k^*>0$, which after one time integration reproduces the third-order equation of [13]. "
  "The modified Green–Lindsay model (MGL) has $\\tau_q=0$ and $\\tau_0>0$, so that the temperature-rate lag acts on the storage and coupling terms only, and the strain-rate lag $\\tau_1$ appears in Eq. (@const@). "
  "The base values of the illustrative relaxation times are $\\tau_q=\\tau_0=2$ s and $\\tau_1=1$ s. The coefficient $\\omega_i$ is the perfusion coefficient")
EQ("\\omega_i=w_{b,i}\\rho_bc_b\\,g_i\\!\\left(\\theta_i,\\Omega_i\\right)", "omega")
P("where $w_{b,i}$ is the basal perfusion rate (0.009 s$^{-1}$ in the tumour and 0.00018 s$^{-1}$ in the normal tissue), $\\rho_b=1060$ kg/m³ and $c_b=3770$ J/(kg K) are the blood density and specific heat, so that the basal sink coefficients are $\\omega_{0,1}=" + sc(LC[0]["om0"], 3) + "$ and $\\omega_{0,2}=" + sc(LC[1]["om0"], 3) + "$ W/(m³ K). "
  "The regulation function $g_i$ combines vasodilation, vascular shutdown at high temperature and, optionally, shutdown after damage,")
EQ("g_i=\\left(1+c_{w,i}\\frac{\\theta}{10\\,\\mathrm{K}}\\right)\\frac{S_i(\\theta)}{S_i(0)}\\,e^{-\\kappa_v\\Omega_i}", "g")
EQ("S_i(\\theta)=\\frac{1}{2}\\left[1-\\tanh\\frac{\\theta-\\theta_{c,i}}{\\Delta\\theta}\\right]", "S")
P("The illustrative parameters are $c_{w,1}=0.5$, $\\theta_{c,1}=6$ K for the tumour, whose vessels dilate poorly and fail early, and $c_{w,2}=3$, $\\theta_{c,2}=9$ K for the normal tissue, with $\\Delta\\theta=2$ K. These values are not taken from a measurement. The shutdown coefficient $\\kappa_v$ is zero in the base case.")
P("The source of [13], with the units clarified, uses $k^{*}=17$ W/(m K s) for the tumour and 16 for the normal tissue. The unit of $k^*$ follows from Eq. (@energy@): since $v$ has the unit K s, $k^*\\partial_x^2v$ is a power density only if $k^*$ is in W/(m K s). "
  "The unit is therefore consistent. The difficulty is not in the unit but in the stability of the MGT equation when the relaxation time is of the order of seconds, which is discussed in Section 2.5.")
H2("2.3 Laser source and boundary conditions")
P("The volumetric source is the Gardner-type profile of [13] multiplied by the pulse-train function,")
EQ("Q(x,t)=I_0\\mu_a\\,G(x)\\,f(t),\\qquad G(x)=B_1e^{-l_1x/\\delta}-B_2e^{-l_2x/\\delta}", "Q")
EQ("\\delta=\\frac{1}{\\sqrt{3\\mu_a\\left[\\mu_a+(1-g)\\mu_s\\right]}}", "delta")
P("with $g=0.9$, $\\mu_s=12000$ m$^{-1}$ and $\\mu_a=40$ m$^{-1}$, giving the optical depth $\\delta=" + f2(LS["delta"] * 1e3) + "$ mm. The diffuse reflectance $R_d=0.05$ enters through the coefficients")
EQ("B_1=3.09+5.44R_d-2.12e^{-21.5R_d},\\qquad B_2=2.09-1.47R_d-2.12e^{-21.5R_d}", "B")
EQ("l_1=1-\\left(1-\\frac{1}{\\sqrt{3}}\\right)e^{-20.1R_d},\\qquad l_2=1.63\\,e^{3.4R_d}", "ll")
P("which give $B_1=" + f3(LS["B1"]) + "$, $B_2=" + f3(LS["B2"]) + "$, $l_1=" + f3(LS["l1"]) + "$ and $l_2=" + f3(LS["l2"]) + "$. The profile $G$ has the surface value $G(0)=" + f3(LS["B1"] - LS["B2"]) + "$ and decays to " + f2((LS["B1"] * math.exp(-LS["l1"] * 0.004 / LS["delta"]) - LS["B2"] * math.exp(-LS["l2"] * 0.004 / LS["delta"])) / (LS["B1"] - LS["B2"])) + " of the surface value at the tumour edge $x=h$. "
  "A reference intensity of $I_0=3\\times10^{5}$ W/m² gives a surface source of " + sc(3e5 * 40 * (LS["B1"] - LS["B2"]), 2) + " W/m³. The pulse train is a sum of rectangular pulses of width $t_p$ and period $P$,")
EQ("f(t)=\\sum_{m=0}^{N_p-1}\\left[H(t-mP)-H(t-mP-t_p)\\right]", "f")
P("with the Heaviside function $H$ and $N_p$ pulses. The treatment time is $t_{\\mathrm{treat}}=N_pP$. At the irradiated surface the stress and the heat flux vanish, and the far face is clamped and held at body temperature,")
EQ("\\sigma_1(0,t)=0,\\qquad k_1\\partial_x\\theta_1(0,t)+k_1^{*}\\partial_xv_1(0,t)=0", "bc0")
EQ("u_2(L,t)=0,\\qquad\\theta_2(L,t)=0", "bcL")
P("At the interface, the displacement, the stress, the temperature and the heat flux are continuous,")
EQ("\\left[u\\right]=\\left[\\sigma\\right]=\\left[\\theta\\right]=\\left[k\\partial_x\\theta+k^{*}\\partial_xv\\right]=0\\quad\\text{at }x=h", "interf")
P("and the medium is at rest at $t=0$,")
EQ("u_i=\\partial_tu_i=\\theta_i=\\partial_t\\theta_i=v_i=0\\quad\\text{at }t=0", "ic")
H2("2.4 Quasi-static reduction and the in-plane stress")
P("The time scale of the heating is seconds, while the elastic transit time of the slab is")
EQ("t_w=\\frac{h}{c_1}+\\frac{L-h}{c_2},\\qquad c_i=\\sqrt{\\frac{c_{11,i}}{\\rho_i}}", "tw")
P("which is " + sc(V["qs"]["twave"], 2) + " s for the present data. The ratio of the inertial term to the elastic term in Eq. (@mom@) scales with")
EQ("\\varepsilon_{\\mathrm{in}}=\\left(\\frac{t_w}{t_c}\\right)^2\\sim\\frac{\\rho L^2}{c_{11}t_c^2}", "epsin")
P("where $t_c$ is the shortest time scale of the loading. For $t_c=1$ s this ratio is of order $10^{-8}$. Dropping the inertia term gives $\\partial_x\\sigma=0$, and with the traction-free surface Eq. (@bc0@) this means that the axial stress vanishes everywhere, and that the axial strain follows the temperature,")
EQ("\\sigma_{xx}\\equiv0\\;\\Rightarrow\\;\\partial_xu_i=\\frac{\\beta_i}{c_{11,i}}\\,\\theta_i", "qs")
P("This is an important structural fact: in a one-dimensional traction-free slab there is no quasi-static axial thermal stress. The strain compatibility with the surrounding tissue in the lateral directions does produce stress. "
  "If the lateral strains are held at zero by the surrounding tissue, the in-plane stress is $\\sigma_{yy}=\\sigma_{zz}=(1+\\tau_1\\partial_t)[\\lambda_i\\partial_xu_i-\\beta_i\\theta_i]$, and Eq. (@qs@) gives")
EQ("\\sigma_{\\parallel,i}=-s_i\\left(1+\\tau_1\\partial_t\\right)\\theta_i,\\qquad s_i=\\frac{2\\mu_i\\beta_i}{c_{11,i}}", "sig")
P("with $s_1=" + f1(LC[0]["sl"]) + "$ Pa/K and $s_2=" + f1(LC[1]["sl"]) + "$ Pa/K. The stress is compressive during heating, and it can become tensile during rapid cooling if $\\tau_1\\partial_t\\theta$ exceeds $\\theta$. The stress jumps at the interface because of the difference of $s_i$. "
  "Substituting Eq. (@qs@) into the coupling term of Eq. (@energy@) replaces the heat capacity by the effective capacity")
EQ("C_{\\mathrm{eff},i}=\\rho_ic_{v,i}+\\frac{T_0\\beta_i^2}{c_{11,i}}", "ceff")
P("The thermoelastic increment is " + f1(LC[0]["cpl"]) + " J/(m³ K) in the tumour and " + f1(LC[1]["cpl"]) + " J/(m³ K) in the normal tissue, that is " + sc(LC[0]["cpl"] / LC[0]["C0"], 1) + " and " + sc(LC[1]["cpl"] / LC[1]["C0"], 1) + " of $\\rho c_v$. Thermoelastic coupling is therefore a negligible effect on the heat balance here. The reduced energy equation is")
EQ("\\left(1+\\tau_q\\partial_t\\right)\\left[C_{\\mathrm{eff}}\\partial_t\\theta+\\omega\\theta-Q\\right]+\\tau_0C_{\\mathrm{eff}}\\partial_t^2\\theta=\\partial_x\\left(k\\partial_x\\theta\\right)+k^{*}\\partial_x^2v", "red")
H2("2.5 Stability of the Moore–Gibson–Thompson type model")
P("Seeking solutions of the homogeneous form of Eq. (@red@) with $\\tau_0=\\omega=0$ in the form $e^{\\lambda t+\\mathrm{i}\\kappa x}$ gives the characteristic cubic")
EQ("\\tau_qC\\lambda^3+C\\lambda^2+k\\kappa^2\\lambda+k^{*}\\kappa^2=0", "cubic")
P("The Routh–Hurwitz conditions for roots with negative real parts reduce to the single condition $\\tau_qk^*<k$. For the data of [13] this means $\\tau_q<k/k^*=" + f3(model.TISSUE["tumour"]["k"] / 17.0) + "$ s in the tumour and " + f3(model.TISSUE["normal"]["k"] / 16.0) + " s in the normal tissue. "
  "With relaxation times of seconds, the literal values of $k^*$ give a growing mode: the largest real part of the roots is " + sc(V["mgt"]["literal"][1][0], 2) + " s$^{-1}$ at $\\kappa=100$ m$^{-1}$ and " + f2(V["mgt"]["literal"][3][0]) + " s$^{-1}$ at $\\kappa=10^4$ m$^{-1}$. "
  "This is a result of the present study, and it indicates that the MGT parameters of [13] are tied to its nondimensional time scale. To keep the model well posed with relaxation times of seconds, the MGT variant uses")
EQ("k^{*}_i=\\eta\\,\\frac{k_i}{\\tau_q},\\qquad0<\\eta<1", "eta")
P("with $\\eta=0.5$ in the base case. With this choice the largest real part of the roots is negative for all wave numbers examined (" + sc(V["mgt"]["eta0.5"][3][0], 2) + " s$^{-1}$ at $\\kappa=10^4$ m$^{-1}$).")
H2("2.6 Arrhenius damage")
P("Irreversible thermal damage is described by the burn integral")
EQ("\\Omega(x,t)=\\int_0^tA\\exp\\!\\left(-\\frac{E_a}{R\\left[T_0+\\theta(x,s)\\right]}\\right)\\mathrm{d}s", "arr")
P("where $R=8.314$ J/(mol K) is the gas constant, $A$ is the frequency factor and $E_a$ the activation energy. The fraction of damaged tissue is")
EQ("F=1-e^{-\\Omega}", "F")
P("This is the same as a two-state kinetic model in which the viable fraction $U$ decays irreversibly with the temperature-dependent rate constant $k_d(T)=A\\exp(-E_a/RT)$,")
EQ("\\frac{\\mathrm{d}U}{\\mathrm{d}t}=-k_d(T)\\,U,\\qquad U=e^{-\\Omega}", "twostate")
P("At constant temperature the integral is exactly $\\Omega=A\\,t\\,e^{-E_a/RT}$, which is used as a verification case. "
  "Two parameter sets are used and both are illustrative. For the normal tissue the classical Henriques–Moritz skin-burn values $A=3.1\\times10^{98}$ s$^{-1}$ and $E_a=6.28\\times10^{5}$ J/mol are taken as a conservative healthy-tissue proxy; they were derived for skin and are not claimed to be valid for deeper tissue. "
  "For the tumour a lower activation energy $E_a=5.5\\times10^{5}$ J/mol is used, with the frequency factor $A=" + sc(TUM["A"], 3) + "$ s$^{-1}$ fixed so that $\\Omega=1$ after one hour at 43 °C, a thermal-dose anchor. "
  "The time to reach $\\Omega=1$ at constant temperature is then " + f1(tdam(TUM, 50)) + " s at 50 °C, " + f2(tdam(TUM, 55)) + " s at 55 °C and " + f3(tdam(TUM, 60)) + " s at 60 °C for the tumour set, against " + k0(tdam(HM, 50)) + " s, " + f1(tdam(HM, 55)) + " s and " + f2(tdam(HM, 60)) + " s for the Henriques–Moritz set. The tumour is therefore more heat sensitive, and the selectivity ratio of the rates is")
EQ("\\varrho_{\\mathrm{sel}}(T)=\\frac{A_T}{A_N}\\exp\\!\\left[\\frac{E_{a,N}-E_{a,T}}{RT}\\right]", "sel")
P("It decreases with temperature because $E_{a,N}>E_{a,T}$, which is the mechanism that favours gentle heating. A second scenario, S2, sets the normal-tissue kinetics equal to the tumour kinetics, as a no-selectivity worst case. The base scenario is called S1.")
H2("2.7 Optimization problem")
P("The design vector collects the controllable laser parameters,")
EQ("\\mathbf{d}=\\left(I_0,\\;t_p,\\;P,\\;N_p\\right)", "d")
P("The objective is the damage inflicted on the normal tissue at the end of the evaluation horizon $t_e=120$ s. The primary measure is the thickness-integrated damage fraction")
EQ("J_F(\\mathbf{d})=\\int_h^{L}F_N(x,t_e)\\,\\mathrm{d}x", "JF")
P("which has the unit of length and equals the thickness of a fully damaged layer. For the optimization a smooth monotone transform of the integrated burn integral is minimised,")
EQ("J(\\mathbf{d})=\\ln\\!\\left[1+\\frac{1}{\\ell_0}\\int_h^{L}\\Omega_N(x,t_e)\\,\\mathrm{d}x\\right],\\qquad\\ell_0=1\\;\\mathrm{mm}", "J")
P("because it does not saturate when the tissue is destroyed. The constraints are as follows. The tumour must be killed to a damage fraction $F_c=0.99$ throughout the target depth $c\\,h$ ($c=1$ in the base case),")
EQ("\\Omega_T(x,t_e)\\ge\\Omega_c=-\\ln\\left(1-F_c\\right)=" + f3(math.log(100)) + ",\\qquad0\\le x\\le c\\,h", "kill")
P("the peak temperature must stay below the vaporization limit of 100 °C,")
EQ("\\max_{x,t}T(x,t)\\le T_{\\mathrm{vap}}=373.15\\;\\mathrm{K}", "vap")
P("the peak in-plane stress must stay below an illustrative safety limit, taken as 36 kPa,")
EQ("\\max_{x,t}\\left|\\sigma_{\\parallel}(x,t)\\right|\\le\\sigma_{\\lim}", "slim")
P("and the treatment must not last longer than 30 s,")
EQ("N_pP\\le t_{\\mathrm{treat,max}}", "ttreat")
P("The stress limit is an illustrative number. No tissue-failure data were used, and its role is to show how a stress constraint enters the design problem. "
  "The bounds on the continuous variables are $2\\times10^{4}\\le I_0\\le8\\times10^{5}$ W/m², $0.2\\le t_p\\le60$ s and a duty cycle $t_p/P$ between 0.1 and 1.")

import tables
TAB(*tables.T1())
H2("2.8 Dimensionless groups for presentation")
P("The calculations are carried out in SI units, and no nondimensionalisation is used in the numerical method. For the interpretation of the results it is useful to name a few ratios, which are formed from the data of Table 1 and are used in the discussion only. "
  "The thermal diffusion time of the tumour layer is of order one and a half minutes, and the ratio of the pulse period to this time, which is typically 0.05, decides whether individual pulses can be distinguished at the tumour edge. The optical depth of 2.6 mm is 0.65 of the tumour thickness, so that a substantial fraction of the light is absorbed beyond the interface, and this is the origin of the direct heating of the normal tissue. "
  "The ratio of the basal perfusion sink to the heat capacity, $\\omega_0/C$, is 0.0085 s$^{-1}$ in the tumour and $1.9\\times10^{-4}$ s$^{-1}$ in the normal tissue, so that over the 120 s horizon the perfusion removes an energy of the same order as the thermal storage in the tumour, but very little in the normal tissue; the nonlinear regulation changes this only at temperatures above the critical values. "
  "The ratio of the relaxation time to the diffusion time, $\\tau/t_d$, is 0.023 for $\\tau=2$ s, which is the reason why the relaxation of the heat flux has a weak effect on the tumour edge, and the Fourier number of the whole slab, $\\alpha t_e/L^2$, is 0.055, which shows that the clamped cold face at 20 mm is far enough away not to affect the result in the horizon used. "
  "The thermoelastic coupling parameter $T_0\\beta^2/(c_{11}C)$ is below $10^{-3}$ in both layers. Finally, the Arrhenius activation number $E_a/(RT)$ is about 200 to 230 for the two tissues, which is why the damage integral changes by orders of magnitude over a few kelvin and why the problem is so sensitive to the temperature at the tumour edge.")
