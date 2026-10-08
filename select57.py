#!/usr/bin/env python3
"""
Select exactly 57 essential equations from the full 130-equation OMML set and
expose them in presentation order under a new sequential key (1..57) WITHOUT any
displayed numbering. Also provides, for each, the markdown anchor phrase after
which the equation should be inserted in the rewritten manuscript.
"""

from build_equations_docx import E as E130

# (original_number, anchor_phrase_fragment_in_text)
# Chosen to retain: geometry (gap, field), CF operator + variable order,
# all governing balances, Cattaneo flux + energy, radiation, concentration,
# both boundary-condition groups, all property correlations (viscosity shape
# trio collapsed representation kept), similarity transforms, the three reduced
# ODEs + memory kernel, wall-quantity definitions, and the core algorithm
# (L1 weights, collocation node, residual trio, Newton update). Dropped: limit
# identities (6,7), scalar group definitions (45-60 kept as text), intermediate
# algorithm scalars and duplicate limits.
SELECTION = [
    (2,  "interspace between the two disks"),      # gap h(t)
    (4,  "magnetic field acts normal"),            # B(t)
    (5,  "the constant-order CF derivative is"),   # CF derivative
    (10, "A convenient and physically motivated"), # variable order alpha
    (11, "A symmetric mid-gap-weighted choice"),   # Lambda(eta)
    (12, "Mass conservation for the axisymmetric"),# continuity
    (13, "the Lorentz force, and the Darcy"),      # radial momentum
    (14, "second-grade differential operator acting on the velocity"), # L_u
    (15, "The axial momentum balance is"),         # axial momentum
    (16, "companion second-grade operator"),       # L_w
    (17, "so that the flux lags the gradient"),    # Cattaneo flux
    (18, "the energy balance reads"),              # energy eq
    (20, "expansion of T"),                        # radiative flux linearised
    (22, "a first-order homogeneous chemical reaction"), # concentration
    (23, "while the upper disk squeezes"),         # lower BC
    (24, "convectively cooled"),                   # upper BC
    (25, "shape-weighted combination"),            # mu_thnf
    (29, "The effective density is"),              # rho_thnf
    (30, "The effective volumetric heat capacity"),# rhoCp_thnf
    (31, "The first embeds gold in blood"),        # sigma step 1
    (32, "the second embeds titania"),             # sigma step 2
    (33, "the third embeds silver"),               # sigma step 3
    (34, "summed over the three species"),         # kappa_thnf
    (35, "each shape-specific contribution"),      # kappa_nf1
    (38, "property ratios are abbreviated"),       # A1..A5
    (39, "the similarity variable and the dimensionless"), # eta
    (40, "u ="),                                   # u
    (41, "w ="),                                   # w
    (42, "theta(eta)"),                            # theta
    (43, "Phi(eta)"),                              # Phi
    (44, "temperature-ratio linearisation"),       # T linearisation
    (61, "the radial momentum equation becomes"),  # reduced momentum
    (63, "The reduced memory kernel"),             # N_mem
    (64, "reduces to"),                            # reduced energy
    (65, "The concentration equation reduces to"), # reduced concentration
    (66, "The similarity forms of"),               # reduced lower BC
    (67, "at eta = 1"),                            # reduced upper BC (same line grp)
    (68, "The radial skin-friction coefficient"),  # Cf
    (69, "the second-grade shear stress"),         # tau_rz
    (70, "the lower and upper disks become"),      # Cf1
    (71, "Cf2"),                                   # Cf2
    (73, "the Nusselt number, which"),             # Nu
    (74, "the Sherwood number"),                   # Sh
    (77, "Writing the kernel decay rate"),         # lambda_n
    (78, "the weighted sum of backward differences"), # L1 sum
    (79, "the exactly integrated exponential weights"), # weights
    (80, "isolate the implicit diagonal"),         # w_nn
    (84, "mapped to the Chebyshev"),               # eta_j nodes
    (85, "scaled for the half-interval"),          # derivative scaling
    (89, "the unknown vector concatenates"),       # U vector
    (90, "incorporates the implicit CF diagonal"), # R^f
    (91, "The energy residual is"),                # R^theta
    (92, "The concentration residual is"),         # R^Phi
    (93, "Newton's method updates the solution"),  # Newton update
    (119, "mean square of the discrete residual"), # E_f residual error
    (124, "reproduces the analytical CF derivative"), # CF test
    (127, "reduces to the viscous squeezing problem"), # beta->0 limit
]

assert len(SELECTION) == 57, f"have {len(SELECTION)} not 57"

# Build the renumbered (but UN-numbered when displayed) OMML list in order.
EQ57 = [E130[orig] for (orig, _anchor) in SELECTION]
ANCHORS = [anchor for (_o, anchor) in SELECTION]
ORIG = [o for (o, _a) in SELECTION]

if __name__ == "__main__":
    print("Selected", len(SELECTION), "equations:")
    for i, (o, a) in enumerate(SELECTION, 1):
        print(f"  {i:2d}  (was {o:3d})  anchor: {a}")
