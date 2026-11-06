# -*- coding: utf-8 -*-
from cb import *

cD = math.sqrt(2 * 0.012 / (1 + EPS)) / 0.02
cLS = 1 / math.sqrt((1 + EPS) * 0.02)
CH = R["checks"]
FD = R["fd"]


def fde(tag, j):
    d = FD[tag]
    mx = max(abs(a[j]) for a in d["lt"])
    return max(abs(a[j] - b[j]) for a, b in zip(d["fd"], d["lt"])) / mx


def mov(k):
    v = R[k]
    xs = R["mov_xs"]
    th = [r[0] for r in v]
    sm = [0.5 * (r[3] + r[4]) for r in v]
    imax = max(range(len(th)), key=lambda i: th[i])
    imin = min(range(len(sm)), key=lambda i: sm[i])
    thr = 2e-3 * max(th)
    front = max(x for x, a in zip(xs, th) if abs(a) > thr)
    return th[imax], xs[imax], sm[imin], xs[imin], front


H1("7. Results and discussion")
H2("7.1 Conventions")
P("All results are for the nondimensional copper data of Tables 1 and 2 with $Q_0=1$, $\\tau_1=0.05$, $\\tau_q=0.02$ and, unless stated, $\\tau_T=0.012$ for the "
  "DPL and TPL models and $\\tau_v=0.03$, $K=0.1$ for the TPL model. Temperatures are nondimensional and proportional to $Q_0$. "
  "Since the thermoelastic coupling constant $\\delta_1=%s$ is small, displacements and stresses are of order $10^{-5}$ to $10^{-2}$ and are plotted "
  "with the scale factors indicated on the axes. The nondimensional wave speeds are measured in units of the elastic speed $c_1$ and the dimensional equivalents follow from" % g(C["d1"], 3))
EQ(r"r_{\mathrm{phys}}=\frac{r}{\eta c_1},\qquad t_{\mathrm{phys}}=\frac{t}{\eta c_1^2},\qquad c_{\mathrm{phys}}=c\,c_1")
P("so that the thermal wave speed $c_w=%s$ corresponds to %s km/s, far above the elastic speed of copper: the nondimensional lags of [1] describe a "
  "hypothetical fast-relaxing material in which the thermal wave outruns the elastic wave, and the results are to be read as a study of structure and trends, not as a "
  "quantitative prediction for a measured material. Every time-domain value below was obtained with $N=4000$ terms and Wynn acceleration for profiles and "
  "$N=3000$ for histories, unless stated." % (g(cD, 3), g(cD * C["v"] / 1000, 3)))

H2("7.2 Wave propagation under the second-order DPL law")
P("Figure 5 shows the temperature and hoop stress produced by a step line source in the MGL-DPL medium at three times. The vertical dashed lines mark the "
  "predicted front $r=c_wt$ with $c_w=%s$. The temperature is smooth and decays monotonically with distance, and falls to numerical zero at a short distance "
  "beyond the front; the front itself is visible as a change of slope, since the wave amplitude is strongly attenuated by $e^{-\\beta r}$ with $\\beta=%s$. "
  "The hoop stress changes by a large fraction of its value across the front: at $t=0.06$ it goes from %s×10⁻³ just behind the front, at $r=0.44$, to "
  "%s×10⁻³ at $r=0.48$ (values of the transformed solution at $N=4000$). This is the signature of the finite-speed wave. The displacement, by contrast, is continuous across "
  "the front, which is the property that distinguishes the MGL theory from the original Green–Lindsay type law, and agrees with [1] and [14]. The far-field values at $r=1$ "
  "are of order $10^{-12}$ or smaller in all fields (far-field check in Section 7.9), so the decay condition is satisfied by the numerical solution." % (
      g(cD, 3), g(X["beta"]["MGL-DPL2"]["beta_cf"], 3),
      g(prof_at("prof_DPL2_t0.06", 0.44, 3) * 1e3, 3), g(prof_at("prof_DPL2_t0.06", 0.48, 3) * 1e3, 3)))
P("The front at $t=0.03$ lies near $r=0.23$, at $t=0.06$ near $0.46$ and at $t=0.09$ near $0.69$, which is the linear growth $c_wt$ expected from the asymptotic analysis; the "
  "stress dips visible at $t=0.09$ close to $r=0.65$ show that the sharp wave feature has by then decayed to a rounded step. After the front has passed, the stress relaxes "
  "toward the quasi-static value that follows the slowly diffusing temperature, and at the source the hoop stress stays compressive, as expected for a heated region constrained by "
  "the surrounding cold material.")
FIG("Figure_5.png", "Temperature (a) and hoop stress (b) versus radius for the MGL-DPL (second-order) model and a step line source at $t=0.03$, $0.06$ and $0.09$. Dashed vertical lines: predicted front positions $r=c_wt$. Computed by Laplace inversion ($N=4000$, Wynn acceleration).")

H2("7.3 Role of the strain-rate parameter")
P("Figure 6 shows the displacement and the hoop stress at $t=0.06$ for four values of $\\tau_1$ in the DPL medium. The temperature field changes by less than 1 per cent in the entire "
  "range (the near-source value at $r=0.1$ is %s for $\\tau_1=0$ and %s for $\\tau_1=0.1$), because the strain-rate term acts on the mechanical equations and enters the heat equation "
  "only through the coupling constant $\\delta_2$. The mechanical fields are affected strongly. At $r=0.3$ the displacement is %s, %s, %s and %s (×10⁻⁶) for $\\tau_1=0$, $0.02$, $0.05$ and $0.1$, a "
  "twelve-fold increase over the range, and the hoop stress is %s, %s, %s and %s (×10⁻³). The mechanism is that with $\\tau_1=0$ the mechanical response ahead of the thermal front is purely "
  "driven by the temperature gradient, whereas a finite $\\tau_1$ gives the elastic field a diffusive component with $m_2^2\\simeq s/[(1+\\epsilon)\\tau_1]$ that spreads ahead of the "
  "thermal wave. The stress at $r=0.5$, ahead of the front $r=c_wt=0.46$, is %s×10⁻⁶ for $\\tau_1=0.05$ and %s×10⁻⁸ for $\\tau_1=0.02$ and negligible for $\\tau_1=0$, which "
  "shows the infinite-speed but exponentially small precursor associated with the strain rate [2]. In agreement with the modelling intent of [14], a larger $\\tau_1$ does not remove the wave but "
  "smooths the stress profile near the front." % (
      g(prof_at("prof_t1_0", 0.1, 0), 4), g(prof_at("prof_t1_0.1", 0.1, 0), 4),
      g(prof_at("prof_t1_0", 0.3, 1) * 1e6, 3), g(prof_at("prof_t1_0.02", 0.3, 1) * 1e6, 3), g(prof_at("prof_t1_0.05", 0.3, 1) * 1e6, 3), g(prof_at("prof_t1_0.1", 0.3, 1) * 1e6, 3),
      g(prof_at("prof_t1_0", 0.3, 3) * 1e3, 3), g(prof_at("prof_t1_0.02", 0.3, 3) * 1e3, 3), g(prof_at("prof_t1_0.05", 0.3, 3) * 1e3, 3), g(prof_at("prof_t1_0.1", 0.3, 3) * 1e3, 3),
      g(abs(prof_at("prof_t1_0.05", 0.5, 3)) * 1e6, 3), g(abs(prof_at("prof_t1_0.02", 0.5, 3)) * 1e8, 3)))
FIG("Figure_6.png", "Effect of the strain-rate relaxation parameter $\\tau_1$ on the displacement (a) and hoop stress (b) at $t=0.06$ in the MGL-DPL medium. Computed.")

H2("7.4 Comparison of heat conduction models")
P("Figure 7 and Table 4 compare the Fourier, Green–Lindsay type, Lord–Shulman MGL, first-order DPL and second-order DPL models for the same step source and $t=0.06$. The "
  "Fourier solution has a smooth diffusive profile with a non-zero temperature at every radius. The Lord–Shulman MGL solution has a front at $r=c_{LS}t=%s$ and the second-order DPL "
  "solution has its front at $r=%s$, further out by %s per cent because $\\tau_T>\\tau_q/2$ makes the DPL wave faster than the Lord–Shulman wave with the same flux lag. The first-order "
  "DPL profile is smooth and has no front, which confirms the parabolic character found in Table 3. At $r=0.2$ the temperatures are %s (Fourier), %s (LS), %s (DPL1) and %s (DPL2): "
  "both lags lower the near-source temperature relative to the Fourier law, and the second-order DPL value lies between the first-order DPL and Lord–Shulman values. The GL type solution has a front close to that of the Lord–Shulman MGL one and a similar temperature profile, but its "
  "hoop stress differs: at $r=0.2$ it is %s×10⁻³ against %s×10⁻³ in the MGL case, and at $r=0.4$ it is %s×10⁻³ against %s×10⁻³, which reflects the different coupling of the temperature rate "
  "and the absence of the strain-rate term. The TPL solution with the base parameters is graphically indistinguishable from the DPL solution; the largest difference of the temperature at the points of "
  "Table 4 is below 1 per cent." % (
      g(cLS * 0.06, 3), g(cD * 0.06, 3), g(100 * (cD / cLS - 1), 3),
      g(prof_at("prof_model_Fourier", 0.2, 0), 3), g(prof_at("prof_model_MGL-LS", 0.2, 0), 3), g(prof_at("prof_model_MGL-DPL1", 0.2, 0), 3), g(prof_at("prof_model_MGL-DPL2", 0.2, 0), 3),
      g(prof_at("prof_model_GL", 0.2, 3) * 1e3, 3), g(prof_at("prof_model_MGL-LS", 0.2, 3) * 1e3, 3),
      g(prof_at("prof_model_GL", 0.4, 3) * 1e3, 3), g(prof_at("prof_model_MGL-LS", 0.4, 3) * 1e3, 3)))
rows = [["Model", "Flux law (Laplace domain)", "Fronts", "$\\theta(0.2)$", "$\\theta(0.4)$", "$10^3\\sigma_{\\phi\\phi}(0.2)$", "$10^3\\sigma_{\\phi\\phi}(0.4)$"]]
for k, law, fr in (("Fourier", "$q=-\\nabla\\theta$", "0"), ("GL", "Green–Lindsay type", "2"),
                   ("MGL-LS", "$\\Phi=1+\\tau_0s,\\ \\Psi=1$", "1"), ("MGL-DPL1", "$\\Phi=1+\\tau_qs,\\ \\Psi=1+\\tau_Ts$", "0"),
                   ("MGL-DPL2", "$\\Phi$ second order, $\\Psi=1+\\tau_Ts$", "1"), ("MGL-TPL", "DPL2 plus $K(1+\\tau_vs)/s$", "1"),
                   ("MGL-TPL1", "$\\Phi=1+\\tau_qs,\\ \\Psi=1+K\\tau_v$ ($\\tau_T=0$)", "1")):
    key = "prof_model_" + k
    rows.append([k, law, fr, g(prof_at(key, 0.2, 0), 3), g(prof_at(key, 0.4, 0), 3), g(prof_at(key, 0.2, 3) * 1e3, 3), g(prof_at(key, 0.4, 3) * 1e3, 3)])
TAB("Comparison of the heat conduction models for a step line source at $t=0.06$ (computed values; number of wavefronts from Table 3).", rows, [1250, 2650, 650, 950, 950, 1100, 1100])
FIG("Figure_7.png", "Temperature (a) and hoop stress (b) at $t=0.06$ for the Fourier, GL, Lord–Shulman MGL, first-order DPL and second-order DPL models and a step source. Dashed lines: $c_{LS}t$ and $c_wt$. Computed.")

H2("7.5 Pulse profiles")
P("Table 5 gives the profiles and Figure 8 shows the temperature and hoop stress histories at $r=0.3$ in the DPL medium. The thermal wave arrives at $t=r/c_w=%s$ for all profiles "
  "that start at $t=0$ with a non-zero value; the computed arrival times (first time at which $|\\theta|>10^{-4}$) are in Table 6 and agree with this to within the time resolution of the history (0.004). The gamma-type "
  "pulse starts with zero source strength and therefore a weaker front, and the sinusoidal train has a zero source at $t=0$ as well. The temperature histories differ strongly after the "
  "front. For the rectangular pulse of width 0.04 the temperature at $r=0.3$ peaks at %s at $t=%s$ and then decays; for the exponentially decaying source the peak is %s at $t=%s$; "
  "for the gamma pulse (peak source at $t_m=0.03$) it is %s at $t=%s$, and the sinusoidal train gives a temperature that oscillates with the period of the source about a slowly rising mean, "
  "reaching its largest value %s at $t=%s$ within the window. The step source produces a monotonic rise to %s at the end of the window ($t=0.3$). The total heat delivered by a profile is" % (
      g(0.3 / cD, 3), g(peak("hist_DPL2_rect", 0)[0], 3), g(peak("hist_DPL2_rect", 0)[1], 3), g(peak("hist_DPL2_exp", 0)[0], 3), g(peak("hist_DPL2_exp", 0)[1], 3),
      g(peak("hist_DPL2_gamma", 0)[0], 3), g(peak("hist_DPL2_gamma", 0)[1], 3), g(peak("hist_DPL2_sin2", 0)[0], 3), g(peak("hist_DPL2_sin2", 0)[1], 3), g(peak("hist_DPL2_step", 0)[0], 3)))
EQ(r"E_p=Q_0\int_0^{\infty}{f(t)\,dt}")
P("which equals $Q_0t_p$ for the rectangle, $Q_0t_d$ for the exponential and $e\\,Q_0t_m$ for the gamma profile. The hoop stress minimum at $r=0.3$ is almost the same (about "
  "$-1.65\\times10^{-3}$) for the step and the rectangular pulse because it is produced at the front arrival at $t=0.044$ by the source strength present in the first few "
  "relaxation times, long before the pulse ends, so a short pulse gives the same front stress as a long one. The end of the rectangular pulse launches an unloading wave that reaches $r=0.3$ near $t=t_p+r/c_w=0.079$ and reverses the sign of the hoop stress, which then peaks at a positive value of about $0.5\\times10^{-3}$ at $t=0.084$ (Figure 8b). This is the central consequence of finite wave speed for pulsed sources. The gamma "
  "and sinusoidal profiles give smaller front stresses (%s×10⁻³ and %s×10⁻³) because their source is small at early times." % (
      g(peak("hist_DPL2_gamma", 3, -1)[0] * 1e3, 3), g(peak("hist_DPL2_sin2", 3, -1)[0] * 1e3, 3)))
TAB("Temporal profiles of the line source ($f_{\\max}=1$ except for the sinusoidal train, which has mean 1/2) and their transforms.",
    [["Profile", "$f(t)$ for $t\\ge0$", "$\\bar F(s)$", "Parameters", "$\\int_0^\\infty f\\,dt$"],
     ["Step", "$1$", "$1/s$", "none", "unbounded"],
     ["Rectangular", "$1$ for $t<t_p$, else $0$", "$(1-e^{-st_p})/s$", "$t_p=0.04$", "$t_p$"],
     ["Exponential", "$e^{-t/t_d}$", "$1/(s+1/t_d)$", "$t_d=0.05$", "$t_d$"],
     ["Gamma type", "$(t/t_m)\\,e^{1-t/t_m}$", "$e\\,t_m/(1+t_ms)^2$", "$t_m=0.03$", "$e\\,t_m$"],
     ["Sinusoidal train", "$\\sin^2(\\pi t/P)$", "$\\omega_0^2/[2s(s^2+\\omega_0^2)]$", "$P=0.08$", "unbounded"]],
    [1500, 2100, 2300, 1300, 1400])
FIG("Figure_8.png", "Temperature (a) and hoop stress (b) histories at $r=0.3$ for the five source profiles of Table 5 in the MGL-DPL medium. Vertical line: predicted arrival $r/c_w$. Computed ($N=3000$, Wynn acceleration).")
rows = [["Case", "Peak $\\theta$", "Time of peak", "Min $10^3\\sigma_{\\phi\\phi}$", "Time of min", "Arrival"]]
for lab, key in (("DPL2, step", "hist_DPL2_step"), ("DPL2, rectangle", "hist_DPL2_rect"), ("DPL2, exponential", "hist_DPL2_exp"),
                 ("DPL2, gamma", "hist_DPL2_gamma"), ("DPL2, sinusoidal", "hist_DPL2_sin2"), ("LS, step", "hist_MGL-LS_step"),
                 ("DPL1, step", "hist_MGL-DPL1_step"), ("TPL, step", "hist_MGL-TPL_step"), ("Fourier, step", "hist_Fourier_step"), ("GL, step", "hist_GL_step")):
    pk = peak(key, 0)
    sp = peak(key, 3, -1)
    rows.append([lab, g(pk[0], 3), g(pk[1], 3), g(sp[0] * 1e3, 3), g(sp[1], 3), g(arrival(key), 3)])
TAB("Computed response summary at $r=0.3$ over $0<t\\le0.3$: peak temperature, most negative hoop stress and arrival time ($|\\theta|>10^{-4}$). Time resolution 0.004.", rows, [1900, 1300, 1300, 1700, 1300, 1000])
P("Table 6 also contains the Fourier and first-order DPL cases, whose arrival times (%s and %s) are far smaller than $r/c_w$ because the parabolic models have an instantaneous, "
  "exponentially small precursor that exceeds the $10^{-4}$ threshold almost immediately. The threshold choice affects these two entries strongly and affects the finite-speed models only by "
  "one time step, so the arrival column should be read as a measure of how the precursor exceeds the threshold rather than as a front time for the parabolic models." % (
      g(arrival("hist_Fourier_step"), 3), g(arrival("hist_MGL-DPL1_step"), 3)))

H2("7.6 Influence of the lag times and the conductivity rate")
P("Figure 9a varies the temperature-gradient lag at fixed $\\tau_q=0.02$ for values 0.0105, 0.012, 0.02 and 0.04, which give wave speeds 7.2, 7.7, 9.9 and 14.0 from the "
  "expression for $c_w$. The front moves outwards and the temperature near the front rises: at $r=0.4$ the values are %s, %s, %s and %s, and at $r=0.6$ the two largest lags give %s and %s while "
  "the others are zero to the printed accuracy. At the same time the near-source temperature falls (at $r=0.1$ it is %s, %s, %s and %s), consistent "
  "with a faster wave carrying heat away from the source. Figure 9b varies $\\tau_q$ with the ratio "
  "$\\tau_T/\\tau_q=0.6$ fixed; then $c_w=1.086\\,\\tau_q^{-1/2}$ and the speeds are 10.9, 7.7, 6.3 and 5.4. A larger $\\tau_q$ slows the wave, so the temperature at $r=0.4$ is %s, %s, %s and %s for "
  "$\\tau_q=0.01$, 0.02, 0.03 and 0.04, and the near-source temperature is lower as well. A longer flux lag therefore slows the front and lowers the temperature at a fixed radius." % (
      g(prof_at("prof_tT_0.0105", 0.4, 0), 3), g(prof_at("prof_tT_0.012", 0.4, 0), 3), g(prof_at("prof_tT_0.02", 0.4, 0), 3), g(prof_at("prof_tT_0.04", 0.4, 0), 3),
      g(prof_at("prof_tT_0.02", 0.6, 0), 3), g(prof_at("prof_tT_0.04", 0.6, 0), 3),
      g(prof_at("prof_tT_0.0105", 0.1, 0), 3), g(prof_at("prof_tT_0.012", 0.1, 0), 3), g(prof_at("prof_tT_0.02", 0.1, 0), 3), g(prof_at("prof_tT_0.04", 0.1, 0), 3),
      g(prof_at("prof_tq_0.01", 0.4, 0), 3), g(prof_at("prof_tq_0.02", 0.4, 0), 3), g(prof_at("prof_tq_0.03", 0.4, 0), 3), g(prof_at("prof_tq_0.04", 0.4, 0), 3)))
FIG("Figure_9.png", "Effect of the temperature-gradient lag $\\tau_T$ at fixed $\\tau_q=0.02$ (a) and of the flux lag $\\tau_q$ at fixed ratio $\\tau_T/\\tau_q=0.6$ (b) on the temperature at $t=0.06$ in the MGL-DPL medium. All cases satisfy $\\tau_T>\\tau_q/2$. Computed.")
P("The three-phase-lag parameters are studied at the later time $t=0.15$, where they matter (Figure 10). The thermal-displacement lag, with $K=0.5$ and $\\tau_v$ in 0, 0.1, 0.3 and 0.5, "
  "reduces the temperature near the source (%s, %s, %s and %s at $r=0.1$) and raises it further out (%s, %s, %s and %s at $r=0.7$). Larger values of $\\tau_v$ could not be used: "
  "the stability scan of Section 5.2 shows instability for $K\\tau_v\\gtrsim0.28$. The conductivity rate, with $\\tau_v=0.03$, shows the same type of redistribution: the "
  "temperature at $r=0.1$ is %s, %s, %s and %s for $K=0$, 0.1, 0.5 and 2, while at $r=0.7$ it is %s, %s, %s and %s. For the largest $K$ the changes are about 14 per cent near the source and 12 per cent at $r=0.7$, which is consistent with the interpretation of Section 5.3: the conductivity rate converts part of the diffusive tail into a "
  "wave-like contribution, and this is a long-time effect. With the base value $K=0.1$ the change from the DPL solution is below 1 per cent at all radii, so the TPL "
  "model is, for the base data, a small correction of the DPL model." % (
      g(prof_at("prof_tv_0", 0.1, 0), 3), g(prof_at("prof_tv_0.1", 0.1, 0), 3), g(prof_at("prof_tv_0.3", 0.1, 0), 3), g(prof_at("prof_tv_0.5", 0.1, 0), 3),
      g(prof_at("prof_tv_0", 0.7, 0), 3), g(prof_at("prof_tv_0.1", 0.7, 0), 3), g(prof_at("prof_tv_0.3", 0.7, 0), 3), g(prof_at("prof_tv_0.5", 0.7, 0), 3),
      g(prof_at("prof_K_0", 0.1, 0), 3), g(prof_at("prof_K_0.1", 0.1, 0), 3), g(prof_at("prof_K_0.5", 0.1, 0), 3), g(prof_at("prof_K_2", 0.1, 0), 3),
      g(prof_at("prof_K_0", 0.7, 0), 3), g(prof_at("prof_K_0.1", 0.7, 0), 3), g(prof_at("prof_K_0.5", 0.7, 0), 3), g(prof_at("prof_K_2", 0.7, 0), 3)))
FIG("Figure_10.png", "Effect of the thermal-displacement lag $\\tau_v$ at $K=0.5$ (a) and of the conductivity rate $K$ at $\\tau_v=0.03$ (b) on the temperature at $t=0.15$ in the MGL-TPL medium. Parameter sets are inside the stable region ($K\\tau_v<0.28$). Computed.")

H2("7.7 Pulse width and period")
P("Figure 11a shows the temperature at $r=0.3$ for rectangular pulses of width $t_p=0.01$, 0.03, 0.06 and 0.12. The peak temperature increases with the width, from %s to %s, but "
  "less than proportionally to the delivered energy, because the heat diffuses away while the pulse is on: the energy ratio is 12 whereas the peak ratio is %s. The "
  "time of the maximum moves from %s to %s. For a pulse that is short compared with the arrival time $r/c_w=0.039$ the response at $r=0.3$ is essentially the "
  "response to an impulse, and it resembles the spectrum of Figure 3b, in which a short pulse excites a broader band. The hoop stress minimum, produced at the front, is %s×10⁻³ for the "
  "narrowest pulse and %s×10⁻³ for the widest one, so the front stress is nearly independent of $t_p$ over the whole range tested, from half a flux lag to six flux lags, in agreement with Section 7.5." % (
      g(max(hist("hist_rect_0.01", 0)), 3), g(max(hist("hist_rect_0.12", 0)), 3), g(max(hist("hist_rect_0.12", 0)) / max(hist("hist_rect_0.01", 0)), 3),
      g(peak("hist_rect_0.01", 0)[1], 3), g(peak("hist_rect_0.12", 0)[1], 3),
      g(peak("hist_rect_0.01", 3, -1)[0] * 1e3, 3), g(peak("hist_rect_0.12", 3, -1)[0] * 1e3, 3)))
P("Figure 11b gives the hoop stress at $r=0.3$ for sinusoidal pulse trains of period 0.04, 0.08 and 0.16. Within the window the temperature is the cumulative result of the "
  "pulses and the stress follows the pulsed source with a delay that corresponds to the transit time of the wave: for $P=0.04$ the strongest compressive stress is %s×10⁻³ at $t=%s$, for $P=0.08$ it is %s×10⁻³ at "
  "$t=%s$ and for $P=0.16$ it is %s×10⁻³ at $t=%s$. A shorter period gives a stronger but more rapid oscillation of the stress, since the "
  "wave is modulated at a higher frequency, while the temperature level is set by the mean source, which is the same for all periods. The values are those of the computed curves only; no further mechanism was tested." % (
      g(peak("hist_sin2_0.04", 3, -1)[0] * 1e3, 3), g(peak("hist_sin2_0.04", 3, -1)[1], 3),
      g(peak("hist_sin2_0.08", 3, -1)[0] * 1e3, 3), g(peak("hist_sin2_0.08", 3, -1)[1], 3),
      g(peak("hist_sin2_0.16", 3, -1)[0] * 1e3, 3), g(peak("hist_sin2_0.16", 3, -1)[1], 3)))
FIG("Figure_11.png", "(a) Temperature history at $r=0.3$ for rectangular pulses of width $t_p=0.01$, $0.03$, $0.06$ and $0.12$; (b) hoop stress history at $r=0.3$ for sinusoidal pulse trains of period $P=0.04$, $0.08$ and $0.16$; MGL-DPL medium. Computed.")

H2("7.8 Moving source")
m0, m3, m77, m12 = mov("mov_V0"), mov("mov_V3"), mov("mov_V7.7"), mov("mov_V12")
EQ(r"\mathcal{A}_V=\frac{\max\left|\tfrac{1}{2}(\sigma_{xx}+\sigma_{yy})\right|_V}{\max\left|\tfrac{1}{2}(\sigma_{xx}+\sigma_{yy})\right|_{V=0}}")
P("Figure 12 shows the temperature and the mean in-plane stress along the line $y=0.2$ at $t=0.1$ for a step-switched line source that moves at $V=0$, 3, 7.7 and 12. The speed 7.7 is the thermal wave speed "
  "$c_w$ and $V=12$ is supersonic with respect to the thermal wave, with Mach angle $\\beta=\\arcsin(c_w/V)=%s$ degrees. At $V=0$ the field is symmetric about $x=0$, the temperature peaks at %s and the "
  "front, where the temperature falls to 0.2 per cent of its maximum, is at $x=%s$, close to the value $\\sqrt{(c_wt)^2-y^2}=0.74$ expected for the circular front. As $V$ increases the maximum moves with the source "
  "(positions %s, %s, %s for $V=3$, 7.7, 12, to be compared with the source positions 0.3, 0.77, 1.2) and lags behind it, the temperature maximum is slightly lower (0.125 to 0.131 against 0.135), and the field "
  "becomes asymmetric: a long trailing tail behind the source and a steep leading edge. For the supersonic case the front in the line $y=0.2$ occurs at $x=%s$, in line with the Mach-cone prediction "
  "$x=Vt-y\\cot\\beta=0.96$. The mean in-plane stress has its extreme value at %s×10⁻³, %s×10⁻³, %s×10⁻³ and %s×10⁻³, so that the amplification factor of the stress peak is "
  "%s, %s and %s for $V=3$, 7.7 and 12. The large increase at speeds close to or above $c_w$ is the structure of a Mach-type front: successive wavefronts emitted by the "
  "moving source overlap and add up along the cone, so that the stress is concentrated there. The stress minimum of the sonic case lies close to the front $x\\approx Vt$." % (
      g(math.degrees(math.asin(cD / 12.0)), 3), g(m0[0], 3), g(m0[4], 3), g(m3[1], 2), g(m77[1], 2), g(m12[1], 2), g(m12[4], 3),
      g(m0[2] * 1e3, 3), g(m3[2] * 1e3, 3), g(m77[2] * 1e3, 3), g(m12[2] * 1e3, 3), g(m3[2] / m0[2], 2), g(m77[2] / m0[2], 2), g(m12[2] / m0[2], 2)))
FIG("Figure_12.png", "Temperature (a) and mean in-plane stress (b) along $y=0.2$ at $t=0.1$ for a step line source translating at speed $V$ in the MGL-DPL medium ($c_w=7.68$). Source positions at $t=0.1$: $x=0$, $0.3$, $0.77$ and $1.2$. Computed by the Fourier–Laplace solution of Section 4 ($N=2000$, $h=0.25$, $\\xi_{\\max}=100$).")
l3, t3, r3 = mov("mov_V3_LS"), mov("mov_V3_TPL"), mov("mov_V3_rect")
P("The influence of the conduction model on the moving-source response was checked at $V=3$. The Lord–Shulman MGL model gives a maximum temperature of %s, higher than the DPL value %s, and a front "
  "at $x=%s$ against %s for DPL, because its wave is slower. The TPL model with base parameters gives %s and is again indistinguishable from the DPL model. A moving source that is also a rectangular pulse of width 0.04 "
  "(switched off at $t=0.04$ when it is at $x=0.12$) produces a maximum temperature of only %s at $t=0.1$ and a mean-stress extreme of %s×10⁻³, which is a fraction %s of the step value, because the source has been off for 0.06 time units." % (
      g(l3[0], 3), g(m3[0], 3), g(l3[4], 3), g(m3[4], 3), g(t3[0], 3), g(r3[0], 3), g(r3[2] * 1e3, 3), g(r3[2] / m3[2], 2)))

H2("7.9 Validation")
P("The validation is summarised in Table 7 and Figure 13. The finite-difference solver agrees with the Laplace solution for the Lord–Shulman MGL case with a rectangular pulse of width 0.03 at $t=0.05$ to "
  "%s per cent of the maximum in temperature, %s per cent in displacement and %s and %s per cent in radial and hoop stress. For the step source the corresponding errors are %s, %s, %s and %s per cent. The temperature agreement is very good; "
  "the stress agreement is limited to a few per cent, because the finite-difference scheme smears the stress peak at the front and because the stress is formed from differences of the "
  "numerical fields. The residual is a discretisation error rather than a systematic discrepancy, but a refinement study of the finite-difference grid was not carried out, so the quoted figures are the errors at one resolution." % (
      g(100 * fde("rect", 0), 2), g(100 * fde("rect", 1), 2), g(100 * fde("rect", 2), 2), g(100 * fde("rect", 3), 2),
      g(100 * fde("step", 0), 2), g(100 * fde("step", 1), 2), g(100 * fde("step", 2), 2), g(100 * fde("step", 3), 2)))
P("The truncation test of the inversion (Figure 13c) gives a relative difference between $N$ and $N/2$ in the temperature of %s for the DPL model and %s for the first-order DPL model at $N=4000$ "
  "($\\le10^{-15}$ for the parabolic case, since the transforms are smooth). For the Lord–Shulman MGL model the temperature difference is %s, and the hoop stress difference at the points close to the front is as large as %s. "
  "The hoop stress at the exact front position of the Lord–Shulman model, where it jumps, is therefore uncertain by several per cent; this is a limitation of Fourier-series inversion for discontinuous functions and "
  "the Wynn acceleration reduces but does not eliminate it. For the DPL model, whose wave is more attenuated at the front, the hoop stress difference at $N=4000$ is only %s." % (
      g(CH["truncation"]["MGL-DPL2"][3][0], 2), g(CH["truncation"]["MGL-DPL1"][3][0], 2), g(CH["truncation"]["MGL-LS"][3][0], 2), g(CH["truncation"]["MGL-LS"][3][1], 2), g(CH["truncation"]["MGL-DPL2"][3][1], 2)))
P("The limiting cases give the expected agreement. The DPL model with $\\tau_T=10^{-9}$ and a first-order flux law reproduces the Lord–Shulman MGL solution, which is the solution of [1], with a maximum difference of "
  "%s of the maximal temperature at five radii; DPL with $\\tau_q=\\tau_T$ at first order reproduces the Fourier solution (with the physical source convention) to %s; and the TPL model with $K=0$ is "
  "identical to the DPL model (difference %s). The Lord–Shulman wave speed %s agrees with the value 7.01 of [1] to the third digit. A direct comparison of field values with the figures of [1] was not made, because those "
  "values were not available in numerical form; the agreement therefore concerns the wave speed, the single-wave structure and the location of the stress feature, not the amplitudes." % (
      g(CH["dpl_tT0_vs_ls"], 2), g(CH["dpl_tq_eq_tT_vs_fourier"], 2), g(CH["tpl_K0_vs_dpl2"], 2), g(cLS, 4)))
P("The far-field check gives $|\\theta|\\le%s$ and $|\\sigma|\\le%s$ at $r=1$, 1.5 and 2 for the DPL case, which is zero within the double-precision resolution of the inversion; the global heat-content identity of Section 3.2 holds with relative "
  "errors of %s (Fourier), %s (Lord–Shulman MGL), %s (DPL) and %s (TPL), limited by the radial quadrature of $\\theta$ on the logarithmic grid used for the check. The moving-source code at $V=0$ reproduces the "
  "axisymmetric solution with a relative error of %s, %s, %s and %s for $h=1$, 0.5, 0.25 and 0.125, respectively. The error does not fall below about $2\\times10^{-4}$ as $h$ is reduced, so the floor is set by something other than the trapezoidal step, most likely the inversion at the wavefront where the "
  "truncation of the Fourier integral and the Wynn acceleration act on slightly different partial sums; this was not investigated further. Two parameter regimes were found to be unstable and were rejected on the basis of the stability scan: second-order DPL with $\\tau_T<\\tau_q/2$ and TPL with $K\\tau_v>0.28$. "
  "In addition, a first test of the Fourier limit showed a 41 per cent discrepancy when the source was not carried through the lag operator, which led to the two source conventions described in Section 2.3." % (
      g(max(abs(CH["far_MGL-DPL2"][i][0]) for i in (1, 2, 3)), 2), g(max(abs(CH["far_MGL-DPL2"][i][j]) for i in (1, 2, 3) for j in (2, 3)), 2),
      g(X["heat_content"]["Fourier"]["rel"], 2), g(X["heat_content"]["MGL-LS"]["rel"], 2), g(X["heat_content"]["MGL-DPL2"]["rel"], 2), g(X["heat_content"]["MGL-TPL"]["rel"], 2),
      g(CH["v0_h"]["1.0"], 2), g(CH["v0_h"]["0.5"], 2), g(CH["v0_h"]["0.25"], 2), g(CH["v0_h"]["0.125"], 2)))
FIG("Figure_13.png", "Validation: (a) temperature and (b) hoop stress from the finite-difference solver and from the Laplace solution for a uniform heated disc ($t_p=0.03$, $t=0.05$, LS-MGL); (c) Durbin truncation test; (d) moving-source code at $V=0$ against the axisymmetric solution as a function of the quadrature step. Computed.")
rows = [["Test", "Quantity", "Result", "Verdict"],
        ["Fourier ($\\epsilon=0$) against $E_1$ solution", "max relative error", g(CH["fourier_E1_maxrel"], 2), "pass"],
        ["DPL ($\\tau_T\\to0$, first order) against LS-MGL", "max difference / max $\\theta$", g(CH["dpl_tT0_vs_ls"], 2), "pass"],
        ["DPL ($\\tau_q=\\tau_T$) against Fourier", "max difference / max $\\theta$", g(CH["dpl_tq_eq_tT_vs_fourier"], 2), "pass"],
        ["TPL ($K=0$) against DPL2", "max difference", g(CH["tpl_K0_vs_dpl2"], 2), "pass"],
        ["FD against Laplace, rectangle", "error / max, $\\theta$; $\\sigma_{\\phi\\phi}$", "%s; %s" % (g(fde("rect", 0), 2), g(fde("rect", 3), 2)), "pass (stress 2.7 %)"],
        ["Durbin $N$ against $N/2$, DPL2, $N=4000$", "relative, $\\theta$; $\\sigma_{\\phi\\phi}$", "%s; %s" % (g(CH["truncation"]["MGL-DPL2"][3][0], 2), g(CH["truncation"]["MGL-DPL2"][3][1], 2)), "pass"],
        ["Durbin $N$ against $N/2$, LS-MGL, $N=4000$", "relative, $\\theta$; $\\sigma_{\\phi\\phi}$", "%s; %s" % (g(CH["truncation"]["MGL-LS"][3][0], 2), g(CH["truncation"]["MGL-LS"][3][1], 2)), "marginal at front"],
        ["Heat-content identity, DPL2", "relative defect", g(X["heat_content"]["MGL-DPL2"]["rel"], 2), "pass"],
        ["Heat-content identity, LS-MGL", "relative defect", g(X["heat_content"]["MGL-LS"]["rel"], 2), "pass (0.6 %)"],
        ["Moving source at $V=0$ against $K_0$", "max relative error, $h=0.25$", g(CH["v0_h"]["0.25"], 2), "pass"],
        ["Wave speed, DPL2: numerical against formula", "$c$", "%s against %s" % (g(R["asym"]["MGL-DPL2"]["c1"], 4), g(cD, 4)), "pass"],
        ["Wave speed, LS-MGL against [1]", "$c$", "%s against 7.01" % g(R["asym"]["MGL-LS"]["c1"], 4), "pass"],
        ["Stability scan, $\\tau_T<\\tau_q/2$", "max growth rate", g(R["asym"]["DPL2-unstable"]["growth"], 3), "unstable, rejected"],
        ["Stability scan, TPL $K\\tau_v>0.28$", "max growth rate ($\\tau_v=1,K=0.5$)", g(R["asym"]["_tpl_unstable_examples"]["tv1_K0.5"], 3), "unstable, rejected"]]
TAB("Summary of validation tests (all computed in this work).", rows, [3300, 2500, 1600, 1600])

H1("8. Limitations")
P("The study has several limitations that bear on how its results should be used. The material data and, above all, the lag times are the nondimensional values of [1] and "
  "illustrative choices for the DPL and TPL parameters; they are not measured values for copper, and the corresponding physical times are sub-picosecond, at which a continuum model with "
  "a local heat flux law is itself questionable. The DPL and TPL laws are Taylor expansions, and the conclusions on the wave structure depend on the truncation order, as shown in Section 5. A different "
  "truncation would change the classification: this paper has not examined higher-order expansions or the delay-differential forms of the laws.")
P("The moving source is a line source in plane strain with constant speed, in an unbounded medium; it has no boundary, no finite beam width and no three-dimensional effects, and it is evaluated at one "
  "observation line $y=0.2$ and one time $t=0.1$, so the field maps of a full Mach cone are not shown. The Fourier integral is evaluated for $y>0$ only; the singular line $y=0$ is not accessible by "
  "this method as implemented. A radially moving ring source was not computed. The strict dependence of the TPL stability on $K\\tau_v$ has been determined numerically for one pair of $\\tau_q$ and $\\tau_T$ and "
  "no analytical criterion is given.")
P("Numerically, the inversion of discontinuous or nearly discontinuous quantities is limited to a few per cent at the front, as in Table 7, and the finite-difference check has been done for the Lord–Shulman MGL case "
  "only, since it was written for the first-order flux law: the second-order DPL and TPL results are validated by the limit checks, the stability analysis, the heat-content identity and by the "
  "internal consistency of the $V=0$ comparison, not by an independent time-domain solution. An independent finite-difference solution for those laws would require additional state variables and was not made. Finally, "
  "the source convention is the effective-source form of [1]; with the alternative form that passes the source through $\\Phi(\\partial_t)$ the early-time response of the second-order laws would contain "
  "impulsive terms and the results would differ near $t=0$.")

P("Regarding reproducibility, every figure and table value was produced by pure-Python code without external numerical libraries: the Bessel functions, the Durbin inversion, the Wynn acceleration, the Aberth "
  "root finder used in the stability scan, the finite-difference solver and the Fourier-integral quadrature are all implemented in the accompanying scripts. A pulsed-source field at one time and 76 radii takes about "
  "twenty seconds on one core, and a moving-source profile with 61 positions about two minutes, so the whole parametric study runs in under five minutes on eight cores. The cost is dominated by the number of "
  "Durbin terms, which is why the quoted truncation tests matter. The Word equations are generated from the same source as the text and were checked by script for the numbering sequence, but the document could not be opened "
  "in a word processor in the environment where it was produced, so the visual layout of the equations has been checked only through an independent rendering of the equation markup.")
P("A further point concerns interpretation. The comparisons in Section 7.4 are made at equal flux lag and at lags chosen to be stable, which is a convenient but not a unique way of comparing models; a comparison at equal wave speed, "
  "for instance, would give different relative amplitudes near the front. The ordering of the models in the figures should therefore be read as characterising the chosen parameter set, and the "
  "qualitative conclusions (existence or absence of a front, direction of the parametric trends, sensitivity of the mechanical field to $\\tau_1$) are the findings that are expected to carry over to other parameter values.")

H1("9. Conclusions")
P("MGL thermoelasticity with second-order dual-phase-lag and three-phase-lag heat conduction was solved for an unbounded plane-strain medium with pulsed and moving line heat sources. The following results were obtained.")
P("First, the transform-domain solution is closed form for pulsed sources and semi-analytic (one Fourier integral) for the translating source. The solution contains the Fourier, Lord–Shulman MGL and "
  "Green–Lindsay type cases as limits and reproduces the Lord–Shulman MGL wave speed of [1], %s against 7.01, as well as the single-wave structure with a continuous displacement. Second, the "
  "asymptotic analysis shows that second-order DPL and TPL laws give one finite-speed wave with $c_w=\\tau_q^{-1}\\sqrt{2\\tau_T/(1+\\epsilon)}$ and a diffusive strain-rate branch, that first-order DPL is parabolic with no wavefront, and that "
  "the second-order laws are stable only for $\\tau_T>\\tau_q/2$ and, for TPL, only for $K\\tau_v$ below about 0.28 for the lags studied. Third, the strain-rate parameter controls the displacement and stress amplitude: "
  "between $\\tau_1=0$ and $0.1$ the displacement at $r=0.3$ rises roughly twelve-fold and the hoop stress about four-fold, while the temperature changes by less than 1 per cent. Fourth, the front stress is nearly "
  "independent of the pulse duration over the range tested (0.5 to 6 flux lags), whereas the temperature scales sublinearly with the delivered energy. Fifth, the thermal-displacement lag and the conductivity rate "
  "mainly redistribute heat at later times and have a small effect for the base data. Sixth, a source moving at or above the thermal wave speed raises the peak in-plane stress by a factor of %s to %s relative "
  "to a stationary source at the same observation line, and for supersonic speed the front follows the Mach-cone geometry." % (
      g(cLS, 3), g(m77[2] / m0[2], 2), g(m12[2] / m0[2], 2)))
P("The validation was successful for the temperature (finite-difference error of the order of 0.1 to 0.2 per cent), acceptable for stresses (2 to 3 per cent) and limited at the discontinuous front (several per cent). "
  "The paper's quantitative statements apply to the nondimensional parameter set used. Future work should add an independent time-domain solver for the second-order laws, a finite-width and a "
  "three-dimensional moving source, a bounded medium with reflections, and measured lag times for real materials.")
