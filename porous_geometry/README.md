# Random Packed-Sphere Porous Geometry Generator (Fortran)

`porous_geometry.f90` generates 3-D random packed-sphere porous geometries and
voxelizes them onto a regular grid, implementing the two algorithms from the
*"Geometry creation algorithm"* flowcharts:

| Method | Description |
|--------|-------------|
| **Method 1** | **Constant sphere size.** Randomly place `N` non-overlapping spheres of a fixed radius (random-sequential addition with a distance-rejection test — the "array C" check), then voxelize and coarse-average. |
| **Method 2** | **Specified porosity + variable sphere size.** Randomly generate spheres with variable radius `r ∈ [rmin,rmax]` and an allowed overlap `o ∈ [omin,omax]`; keep adding spheres (rejecting any that violate the minimum centre distance `d_ij ≥ r_i + r_j − o`) until the solid volume reaches the required fraction, i.e. the **target porosity** is met. Then voxelize and coarse-average. |

## Voxelization convention

For every fine-grid point the code marks:

- `0` → point lies **inside a sphere** (solid)
- `1` → point lies in the **pore space** (void)

then performs *"grid averaging by some factor"* (`AVGF`) to produce a coarse
volume-fraction field. Only grid points within the local bounding box of each
sphere are visited ("localized volume around the selected sphere") for speed.

## Build & run

```sh
gfortran -O2 -o porous_geometry porous_geometry.f90
./porous_geometry
```

## Output

| File | Contents |
|------|----------|
| `method1_geometry.vtk`, `method2_geometry.vtk` | Legacy VTK `STRUCTURED_POINTS` scalar volume (`0`=solid, `1`=pore). Open in **ParaView** / **VisIt**; threshold or iso-surface at `0.5` to see the packed spheres in 3-D. |
| `method1_spheres.dat`, `method2_spheres.dat` | List of sphere centres and radii (`x y z r [overlap]`) — useful for plotting spheres directly (e.g. MATLAB/Python). |

The program also prints the sphere count, the achieved porosity, grid sizes and timing.

## Key parameters (edit the `geom_params` module at the top of the file)

```
LDOM             domain edge length (cube)
NG               fine grid points per side
AVGF             grid-averaging factor (NG must be divisible by AVGF)

NSPH1, RAD1      Method 1: sphere count and constant radius
RMIN, RMAX       Method 2: variable radius range
OMIN, OMAX       Method 2: allowed overlap range
TARGET_POROSITY  Method 2: desired void fraction
```

The RNG is seeded with a fixed value (`seed_rng(12345)`) for reproducible
geometries; pass a value `<= 0` for a time-based random seed.


---

## Ellipsoidal geometries

`ellipsoid_geometry.f90` is the ellipsoidal counterpart of the sphere
generator. Each pore is a **randomly-oriented ellipsoid** with three
independent semi-axes `(a, b, c)` and an orientation given by ZXZ Euler angles
`(phi, theta, psi)`.

| Method | Description |
|--------|-------------|
| **Method 1** | **Constant ellipsoid shape/size.** Fixed semi-axes `(A1,B1,C1)`, random orientation; random-sequential placement with a conservative bounding-sphere rejection test; voxelize + coarse-average. |
| **Method 2** | **Specified porosity + variable ellipsoid size.** Semi-axes each random in `[AXMIN,AXMAX]`, random orientation, allowed overlap `o ∈ [OMIN,OMAX]`; keep adding until the solid volume reaches the required fraction (target porosity); voxelize + coarse-average. |

**Inside/outside test.** For an ellipsoid centred at `p0` with rotation matrix
`R` (columns = principal axes) and semi-axes `(a,b,c)`, rotate the offset into
the body frame `u = Rᵀ(p − p0)` and test
`(u_x/a)² + (u_y/b)² + (u_z/c)² ≤ 1`.

### Build & run

```sh
gfortran -O2 -o ellipsoid_geometry ellipsoid_geometry.f90
./ellipsoid_geometry
```

### Output

| File | Contents |
|------|----------|
| `ell_method1_geometry.vtk`, `ell_method2_geometry.vtk` | Legacy VTK `STRUCTURED_POINTS` volume (`0`=solid, `1`=pore) for ParaView/VisIt. |
| `ell_method1_ellipsoids.dat`, `ell_method2_ellipsoids.dat` | One line per ellipsoid: `x y z  a b c  phi theta psi`. |

### Rendering

`render_ellipsoids.py` (pure stdlib, no numpy/matplotlib/PIL) ray-traces the
oriented ellipsoids to a PNG, coloured by height:

```sh
python3 render_ellipsoids.py ell_method1_ellipsoids.dat ell_method1_render.png
python3 render_ellipsoids.py ell_method2_ellipsoids.dat ell_method2_render.png
```

> Note: Method 1's non-overlap test uses each ellipsoid's *bounding sphere*, so
> for elongated axes it saturates at a modest count — lower `NELL1` (or the
> semi-axes) if the target count is not reached. Method 2 allows controlled
> overlap and packs the domain to the requested porosity.
