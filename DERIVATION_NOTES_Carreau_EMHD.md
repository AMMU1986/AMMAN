# Derivation notes — corrected formulation for the unsteady EMHD squeezing Carreau hybrid nanofluid

These notes lock the corrected equations before they are encoded into the Word document and the
figure solver. They implement the reviewer's requested corrections. Equations are numbered here
with a `C` prefix (C1, C2, ...) for the working notes; the final manuscript uses the serial (1),
(2), ... numbering.

## 1. Similarity transformation (manuscript Eqs. 1, 22, 23) — RETAINED

The plate separation, stream function and velocities are mutually consistent (reviewer's own
final correction). We keep them:

    h(t) = [ nu_f (1 - gamma t) / a ]^{1/2}
    eta  = y / h(t) = y [ a / ( nu_f (1 - gamma t) ) ]^{1/2}
    psi  = [ a nu_f / (1 - gamma t) ]^{1/2} x f(eta)
    u    =  a x / (1 - gamma t) f'(eta)
    v    = -[ a nu_f / (1 - gamma t) ]^{1/2} f(eta)

These satisfy continuity identically: u = d psi/dy, v = -d psi/dx.

## 2. Unsteady/inertial group (CORRECTION to Eq. 26)

For u = (a x /(1-gamma t)) f'(eta):

    du/dt = (a x/(1-gamma t)) (gamma/(1-gamma t)) [ f' + (eta/2) f'' ]

Non-dimensionalising the x-momentum balance by the convective scale a^2 x/(1-gamma t)^2 gives the
unsteady contribution

    Sq ( f' + (eta/2) f'' ),      Sq = gamma / a

This REPLACES the incorrect group (Sq/2)(3 f'' + eta f''').

## 3. Third-order (primitive) momentum balance

Collecting the transformed x-momentum equation (boundary-layer form, before pressure elimination)
with the corrected unsteady term:

    (A1/A2) [1 + We^2 (f'')^2]^{(n-3)/2} [1 + n We^2 (f'')^2] f'''
        + f f'' - (f')^2
        - Sq ( f' + (eta/2) f'' )
        - (A1/(A2 Da)) f'
        - (A3/A2) M (f' - Ee)
        - Fr (f')^2  =  G                                              (C-mom-3)

where G is the (constant-in-eta) scaled pressure-gradient group. Because the gap is thin and
dp/dy is eliminated between the x- and y-momentum equations, dG/deta = 0.

## 4. Fourth-order momentum equation (CORRECTION: retain 4th order, fixes the BC-count problem)

Differentiating (C-mom-3) once with respect to eta removes the pressure constant G and yields a
FOURTH-ORDER equation. Using d/deta[ f f'' - (f')^2 ] = f f''' - f' f'' :

    (A1/A2) d/deta{ [1 + We^2 (f'')^2]^{(n-3)/2} [1 + n We^2 (f'')^2] f''' }
        + f f''' - f' f''
        - Sq ( (3/2) f'' + (eta/2) f''' )
        - (A1/(A2 Da)) f''
        - (A3/A2) M f''
        - 2 Fr f' f''  =  0                                           (C-mom-4)

Notes:
 - d/deta[ Sq(f' + (eta/2) f'') ] = Sq( f'' + (1/2) f'' + (eta/2) f''' ) = Sq( (3/2) f'' + (eta/2) f''' ).
 - The Carreau bracket derivative is expanded analytically in the solver (see below). For n = 1
   (or We -> 0) the Carreau prefactor is 1 and its derivative term reduces to (A1/A2) f''''.
 - This is order 4 in f. With energy (order 2) and species (order 2) the TOTAL SYSTEM ORDER = 8,
   which now matches the EIGHT boundary conditions. The BC-count inconsistency is resolved.

### Newtonian-limit check (n = 1 or We = 0)
    (A1/A2) f'''' + f f''' - f' f''
        - Sq( (3/2) f'' + (eta/2) f''' )
        - (A1/(A2 Da)) f'' - (A3/A2) M f'' - 2 Fr f' f'' = 0
Clear-fluid, non-magnetic, non-porous limit (A_i=1, M=0, Da->inf, Fr=0):
    f'''' + f f''' - f' f'' - Sq( (3/2) f'' + (eta/2) f''' ) = 0
which is the classical Wang unsteady-squeezing fourth-order equation (up to the Sq scaling
convention), confirming the derivation.

## 5. Boundary conditions (CORRECTION to Eqs. 30-31): four momentum conditions now consistent

With a fourth-order momentum equation, four momentum BCs are appropriate:

    f(0) = 0,               (impermeable / symmetric lower reference)
    f'(0) = 1 + S1 f''(0),  (stretching + velocity slip, lower plate)
    f(1) = Sq/2,            (upper-plate normal squeezing velocity)
    f'(1) = 0.              (no tangential slip at upper plate)

Energy (2nd order):   theta'(0) = -Bi[1 - theta(0)],   theta(1) = 0.
Species (2nd order):  phi(0) = 1 + S3 phi'(0),         phi(1) = 0.

Total = 4 + 2 + 2 = 8 conditions for an order-8 system. CONSISTENT.

## 6. Energy equation (CORRECTION to Eq. 27): radiation grouping

Rd is defined with the base-fluid conductivity kappa_f, so the radiative augmentation must NOT be
multiplied by A4 = kappa_hnf/kappa_f. From Eq. (13) with F = 1 + (theta_r - 1) theta:

    [ A4 + (4/3) Rd F^3 ] theta''
      + 4 Rd (theta_r - 1) F^2 (theta')^2
      + A5 Pr ( f theta' - Sq ( (1/2) eta theta' + theta ) )        <-- see note on convective terms
      + Pr [ A1 Ec (f'')^2 (1 + We^2 (f'')^2)^{(n-1)/2}
             + A3 M Ec (f' - Ee)^2
             + A2 Df phi'' ]  = 0                                     (C-energy)

Convective-term note: because T_w = T_0 + (a x/(1-gamma t)) d1 is x- and t-dependent (Eq. 25), the
material derivative of T produces, in addition to A5 Pr f theta', an unsteady/stretching term.
Carrying the transformation through gives the group

    A5 Pr ( f theta' - (Sq/2) eta theta' )      (structure retained from the manuscript)

as the leading convective/unsteady contribution; the extra "theta" production term from the
x-linear wall excess (T_w - T_0 ~ x) cancels against the streamwise convection u dT/dx to leading
order in the local-similarity (boundary-layer) reduction used throughout. We therefore retain the
manuscript's convective structure but (i) fix the radiation grouping (A4 no longer multiplies Rd)
and (ii) keep A5 on the convective group. The corrected energy ODE used for the figures is:

    [ A4 + (4/3) Rd F^3 ] theta''
      + 4 Rd (theta_r - 1) F^2 (theta')^2
      + A5 Pr ( f theta' - (Sq/2) eta theta' )
      + Pr [ A1 Ec (f'')^2 (1 + We^2 (f'')^2)^{(n-1)/2}
             + A3 M Ec (f' - Ee)^2 + A2 Df phi'' ] = 0

## 7. Species equation (Eq. 28) — retained (radiation grouping does not affect it)

    phi'' + Sc ( f phi' - (Sq/2) eta phi' ) + Sc Sr theta'' - K Sc phi = 0

## 8. Entropy generation (CORRECTIONS)

Eq. (43) local Joule term must use time-dependent fields B(t), E(t):
    S_J''' = (sigma_hnf / T0) [ u B(t) - E(t) ]^2

Eq. (45)/(46) normalisation: the reference S0''' uses kappa_hnf. To keep A4 explicit in Ns, we
normalise consistently with kappa_f, i.e. define
    S0''' = kappa_f (T_w - T0)^2 / ( T0^2 h(t)^2 )
so that the thermal term in Ns is [ A4 + (4/3) Rd F^3 ] (theta')^2 (A4 appears once, on conduction
only; radiation not multiplied by A4).

Eq. (66) thermal irreversibility (dimensional) — remove the double A4 on the radiation part:
    S_HT''' = ( kappa_f (T_w - T0)^2 / ( T0^2 h^2 ) ) [ A4 + (4/3) Rd F^3 ] (theta')^2

Eq. (68) Joule irreversibility with time-dependent field, expressed via f' and Ee:
    S_J''' = ( sigma_hnf B0^2 U_w^2 / ( T0 (1 - gamma t) ) ) ( f' - Ee )^2,  Ee = E(t)/(B(t) U_w)

Eq. (44)/(52) diffusive irreversibility: keep the cross-gradient term but flag nonnegativity
requires |cross term| <= sum of squares; retained for Bejan number with the caveat noted.

Dimensionless entropy generation number (corrected radiation grouping):
    Ns = [ A4 + (4/3) Rd F^3 ] (theta')^2
       + (A1 Br/Omega)(f'')^2 [1 + We^2 (f'')^2]^{(n-1)/2}
       + (A3 Br M/Omega)(f' - Ee)^2
       + Lambda (zeta/Omega)^2 (phi')^2
       + Lambda (zeta/Omega) theta' phi'

## 9. Numerical state vector (CORRECTION to Eqs. 55-65): add momentum variable for 4th order

    y1=f, y2=f', y3=f'', y4=f''',  y5=theta, y6=theta', y7=phi, y8=phi'
Eight-variable first-order system (was seven). y4' = f'''' from (C-mom-4) solved for the highest
derivative. The coupling in Eq. (63)/(60)-(62) between theta' and phi'' (via Df and Sr) is solved
as a 2x2 linear system at each eta (not sequentially):
    [ (A4 + 4/3 Rd F^3)      Pr A2 Df ] [theta'']   = RHS_theta
    [ Sc Sr                  1        ] [phi''  ]   = RHS_phi

## 10. Grid convergence (CORRECTION to Eq. 80): signed successive differences
    p_obs = ln( |(q_2N - q_4N)/(q_N - q_2N)| ) / ln 2

## 11. Appendix A corrections (as per reviewer)
 - A1 (Newtonian): unsteady term -> Sq(f' + (eta/2) f''); shown at 3rd-order primitive level.
 - A9: pure-diffusion limit is phi'' = 0 (Sr=0, Sq=0, K=0, no convection). The convection-reaction
   form phi'' + Sc f phi' - K Sc phi = 0 is "steady transport without Soret", renamed.
 - A10 (was A0): keep the cross term:
     Ns = A4 (theta')^2 + (A1 Br/Omega)(f'')^2 + (A3 Br M/Omega)(f'-Ee)^2
        + Lambda(zeta/Omega)^2 (phi')^2 + Lambda(zeta/Omega) theta' phi'
 - A11: Be = [A4(theta')^2 + Lambda(zeta/Omega)^2(phi')^2 + Lambda(zeta/Omega)theta'phi'] / Ns
 - A13: Newtonian base fluid has A4 = 1 => Re^{-1/2} Nu = -theta'(1) (non-radiative);
   with radiation Re^{-1/2} Nu = -(1 + 4/3 Rd) theta'(1) since theta(1)=0.
 - A15: Re^{-1/2} Sh = -phi'(1), phi(0)=1, with S3=0 (no solutal slip); no-slip requires S1=0.
 - Concluding paragraph: Carreau Newtonian limit does NOT reproduce Casson; compare only at a
   common Newtonian limit.


## 12. Round-2 reviewer refinements (applied)

 - Electric field made explicit: E(t) = E0 / (1 - gamma t)^{3/2}, so that
   Ee = E0/(B0 U_w) is constant under local similarity (B ~ (1-gamma t)^{-1/2},
   U_w ~ (1-gamma t)^{-1}). Orientations stated: B in +y, E in +z, Lorentz force
   along x reducing to sigma(uB - E).
 - Cauchy stress written bold; electrical conductivity renamed sigma_e (sigma_e,hnf,
   sigma_e,f) to avoid clashing with total stress sigma. Stated mu0 = mu_hnf so A1 and
   the Carreau viscosity are consistently connected; gammadot ~ |du/dy| in the layer.
 - x-momentum (Eq. 9 in the revised serial numbering) written as the Carreau stress
   DIVERGENCE (1/rho) d/dy[ mu (1+Gamma^2 u_y^2)^{(n-1)/2} u_y ], with its expansion
   showing the essential (1 + n Gamma^2 u_y^2) factor. y-momentum kept complete for
   consistent pressure elimination.
 - Temperature/concentration normalisation corrected to theta = (T-T0)/(Tw-T0),
   phi = (C-C0)/(Cw-C0), with T_h = T0, C_h = C0 stated explicitly => theta(1)=phi(1)=0.
 - Dufour/Soret reconciled: energy PDE carries D_B K_T/(c_s (rho c_p)_hnf) C_yy;
   concentration PDE carries D_B K_T/T_m T_yy; set c_s == T_m; A2 in A2 Df phi'' bridges
   the base-fluid (c_p)_f normalisation of Df with the hybrid heat capacity.
 - Wall location for tau_w, q_w, q_m specified at eta = 1.
 - Entropy positive-semidefiniteness stated correctly for a theta'^2 + b theta' phi'
   + c phi'^2 with a>=0, c>=0, b^2 <= 4ac => Lambda <= 4[A4 + (4/3) Rd F^3]. Verified
   numerically: Lambda=0.5 << 4 A4 ~ 4.77; Be in [0.039, 0.999] and min|Delta| ~ 1.05
   over 54 parameter combinations.
 - Numerical coupling written as an explicit 2x2 matrix equation with determinant
   Delta = K_r - Pr A2 Df Sc Sr != 0; residual norm uses normalised residuals;
   bvp4c's own adaptive residual control noted; p_obs computed on controlled uniform
   meshes (N=100,200,400).
 - Equation numbering made continuous/auto (docx_omml Document auto-numbering); no
   duplicated numbers. Serial order 1..65 then A1..A15.


## 13. Round-3 reviewer refinements (applied)

 - Property-ratio notation changed A1..A5 -> alpha_mu, alpha_rho, alpha_sigma, alpha_kappa,
   alpha_c everywhere (resolves the collision with the Rivlin-Ericksen tensor A_1). The
   tensor A_1 and stress sigma / identity I are set in bold; electrical conductivity is
   sigma_e (sigma_e,hnf, sigma_e,f).
 - Engineering quantities: added explicit tau_w (Carreau), q_w (total conductive+radiative)
   and q_m definitions at eta=1; stated the upper-wall reporting convention and that
   f''(0) is used if the stretching lower-plate friction is wanted; Re_x = xU_w/nu_f.
 - Numbering fully continuous via auto-numbering: 1..66 then A1..A15 (no duplicates).

## 14. Reference verification (round-3 request)

Verified via literature search (bibliographic facts, not verbatim text):
 - [1] Choi & Eastman, ASME IMECE, San Francisco, Nov 12-17 1995; ASME FED 231/MD 66,
   pp. 99-105 (ANL/MSD/CP-84938). CONFIRMED.
 - [8] Tlili, Nabwey, Ashwinkumar, Sandeep, "3-D MHD AA7072-AA7075/methanol hybrid
   nanofluid flow above an uneven thickness surface with slip effect," Scientific Reports
   10, art. 4402 (2020), DOI 10.1038/s41598-020-61215-8. CONFIRMED (use article number,
   not "pp. 1-13").
 - [12] P. J. Carreau, "Rheological equations from molecular network theories," Trans.
   Soc. Rheol. 16, 99-127 (1972); ADS 1972JRheo..16...99C. CONFIRMED.
 - [15] Mkhatshwa & Khumalo, "Irreversibility ... EMHD Darcy-Forchheimer slip flow of
   Carreau hybrid nanofluid ... porous medium," Heat Transfer 52 (2023) 395-429. CONFIRMED
   (authors Musawenkhosi Mkhatshwa, Melusi Khumalo, Univ. of South Africa).
 - [23] Bhaskar & Sharma, "Unsteady MHD squeezing viscous Casson fluid flow in upright
   channel with cross-diffusion and thermal radiactive effects," Indian J. Phys. 95(7)
   (2021) 1453-1467, DOI 10.1007/s12648-020-01805-4. CONFIRMED (title's "radiactive" is the
   original spelling; first author Khushbu Bhaskar).
 - [34] A. Bejan, "A study of entropy generation in fundamental convective heat transfer,"
   ASME J. Heat Transfer 101 (1979) 718-725. CONFIRMED (classic).
COULD NOT be independently confirmed to the exact volume/page in this environment and are
flagged for the authors to re-check against the publisher record:
 - [20] Sobamowo & Akinshilo, squeezing flow of nanofluid between parallel plates under
   magnetic field, Alexandria Eng. J. 57 (2018) 1413-1423.
 - [42] Yadav & Kumar, entropy generation of unsteady squeezing MHD nanofluid flow between
   two parallel plates, Int. Commun. Heat Mass Transfer 128 (2021) 105632.


## 15. Round-4 refinements (applied)

 - Appendix A12: Newtonian base-fluid skin friction evaluated at the STRETCHING lower plate,
   Re_x^{1/2} C_f = f''(0) (was f''(1)), per reviewer; note added.
 - Notation: kept the alpha_* property-ratio notation across BOTH the main text AND
   Appendix A for internal consistency (reverting the appendix to A_1..A_5 would reintroduce
   the collision with the Rivlin-Ericksen tensor that round-3 resolved).
 - Results & Discussion expanded in EVERY results subsection (6.1-6.6), each now carrying a
   dedicated "Comparison with the literature" paragraph with quantitative figures:
     6.1 velocity: crossover eta~0.45 vs Stefan[18]/Grimm[19]/Sobamowo[20]/Bhaskar[23]/Yadav[42];
         We-thickening regime-specific vs Wahab[14]/Mkhatshwa[15]; f''(1)=0.4222 context vs [42].
     6.2 temperature: Ec/Bi heating vs Qayyum[17]/Shah[13]/Sharma[29]/Kumar[28]; corrected Rd
         grouping; Nu +22% Rd 0.2->1.0.
     6.3 concentration: Sc/K vs Rafique[27]/Shah[13]; reciprocal Soret-Dufour vs [23,26,28];
         Sh=0.052 & Nu=4.85 at Sr=0.5.
     6.4 entropy: near-wall max vs Bejan[34,35]; Ns(0) +153% with Br vs Khan[36]/Ali[41];
         M and Omega trends vs Bhatti[38]/Sharma[29]/Siva[39].
     6.5 Bejan: near-wall->core transition vs Yadav[42]/Ali[41]; Be(0) 0.236->0.093 with Br;
         Be in [0.039,0.999] verified; Br->0/large-Br limits vs [36,41].
     6.6 engineering: Nu +29% with phi vs Tlili[8]; Cf growth vs Mkhatshwa[15]/Shahzad[33].
   Section 6.8 retained as the synthesis. Added reference [17] Qayyum et al. (Coatings 12, 2022).


## 16. Round-5 refinements (applied)

 - Abstract expanded to ~368 words and now cites references (Choi&Eastman, Suresh, Mandal,
   Tlili, Carreau, Soret, Bejan, Mkhatshwa, Ali) as [1],[2],... in first-appearance order.
 - Introduction expanded to ~960 words (>= 850) with a full literature survey and an
   explicit four-point objectives/novelty paragraph.
 - Citation numbering rebuilt so references are numbered strictly in order of FIRST
   appearance starting in the abstract: citations run 1,2,3,... with NO out-of-order jumps;
   the reference list is emitted 1..43 in that same order. Implemented via a Cites() manager
   (REF_META registry + cite/one/many/rng) so numbering is automatic and cannot drift.
 - All 43 references are cited; verified programmatically that the first-appearance sequence
   equals 1..43 and the reference list is sequential 1..43.
 - The dagger/double-dagger verification markers are preserved in the regenerated list.


## 17. Round-6 refinements (applied)

 - Removed ALL citations from the Abstract and confirmed the Conclusions carry none, per
   reviewer. The abstract is now citation-free prose (~330 words).
 - First citation therefore now appears in the Introduction; the citation manager
   renumbered automatically so references remain in strict order of first appearance.
 - Reference list emitted in strictly serial format "[1] ...", "[2] ...", ... "[43] ..."
   with NO inline verification markers (dagger/double-dagger moved to a separate italic
   note after the list). Verified programmatically: abstract citations = none,
   conclusions citations = none, first-appearance sequence == 1..43, reference list
   sequential 1..43, all 43 cited.
