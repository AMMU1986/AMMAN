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
