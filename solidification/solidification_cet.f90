!==============================================================================
!  solidification_cet.f90
!
!  2-D Cellular Automaton (CA) simulation of solidification microstructure
!  showing the COLUMNAR-to-EQUIAXED TRANSITION (CET):
!
!     * Heat is extracted through the four cold mould walls.
!     * Grains NUCLEATE ON THE WALLS and grow INWARD  -> COLUMNAR grains
!       (elongated, aligned roughly normal to the wall).
!     * The melt in the CENTRE cools more slowly, becomes undercooled and
!       nucleates in the bulk -> EQUIAXED DENDRITIC grains that block the
!       advancing columnar front (the CET).
!
!  Physics captured (in dimensionless CA units, chosen for a fast demo):
!     - Transient heat conduction (explicit FTCS) with cold Dirichlet walls
!       plus a uniform volumetric cooling rate.
!     - Latent heat released (recalescence) when a cell solidifies.
!     - Surface (heterogeneous) nucleation on the walls at small undercooling.
!     - Continuous bulk nucleation using a Gaussian distribution of critical
!       undercoolings (Rappaz/Oldfield continuous-nucleation model).
!     - Dendrite-envelope growth by a decentered-square capture rule; the
!       four square corners represent the <10> primary dendrite arms, so the
!       growth is crystallographically oriented (each grain has a random
!       orientation theta in [0,90deg)). Oriented growth naturally produces
!       columnar texture selection near the walls.
!
!  Output:
!     - grains_XXXX.ppm : colour map, one random colour per grain (frames)
!     - zones.ppm       : blue = columnar grains, red = equiaxed grains
!     - grain_id.dat    : final grain-id field (ASCII, nx columns x ny rows)
!     - an ASCII map + statistics printed to the terminal.
!
!  Build : gfortran -O2 -o cet solidification_cet.f90
!  Run   : ./cet
!
!  Author: Kiro demo.  All parameters are grouped in module params for tuning.
!==============================================================================

module params
   implicit none
   ! ---- grid -------------------------------------------------------------
   integer, parameter :: nx = 240          ! cells in x (incl. mould walls)
   integer, parameter :: ny = 240          ! cells in y (incl. mould walls)
   integer, parameter :: nsteps = 1500     ! number of time steps
   integer, parameter :: nout   = 250      ! write a frame every nout steps

   ! ---- thermal (dimensionless CA units) --------------------------------
   real, parameter :: TL    = 10.0         ! liquidus temperature
   real, parameter :: T0    = 12.0         ! initial melt temp (superheated)
   real, parameter :: Twall = -10.0        ! cold mould-wall temperature
   real, parameter :: Ddiff = 0.15         ! thermal diffusion coeff (<0.25 stable)
   real, parameter :: Qcool = 0.012        ! uniform cooling per step
   real, parameter :: Lheat = 6.0          ! latent-heat recalescence per cell

   ! ---- growth kinetics --------------------------------------------------
   real, parameter :: mu   = 0.02          ! growth coeff:  v = mu * dT^2
   real, parameter :: vmax = 0.5           ! cap on interface speed (cells/step)

   ! ---- nucleation -------------------------------------------------------
   real, parameter :: pWall   = 0.35       ! prob. of a wall-layer cell seeding
   real, parameter :: siteFrac = 0.006     ! fraction of bulk cells that are sites
   real, parameter :: dTnMean = 5.0        ! mean critical undercooling (bulk)
   real, parameter :: dTnSig  = 1.2        ! std dev of critical undercooling
   integer, parameter :: nucEvery = 5      ! test bulk nucleation every N steps

   ! ---- cell states ------------------------------------------------------
   integer, parameter :: LIQUID  = 0
   integer, parameter :: GROWING = 1       ! interface cell (has a growing square)
   integer, parameter :: SOLID   = 2       ! interior solid (no liquid neighbours)
   integer, parameter :: FRESH   = 3       ! captured this step (temp marker)
   integer, parameter :: WALL    = 4       ! mould wall (never solidifies)

   ! ---- grain types ------------------------------------------------------
   integer, parameter :: COLUMNAR = 1
   integer, parameter :: EQUIAXED = 2

   real, parameter :: PI = 3.14159265358979
end module params

!------------------------------------------------------------------------------
module state
   use params
   implicit none
   integer :: st(nx,ny)        ! cell state
   integer :: gid(nx,ny)       ! grain id (0 = none)
   real    :: gx(nx,ny)        ! growing-square centre x (cell units)
   real    :: gy(nx,ny)        ! growing-square centre y
   real    :: Lh(nx,ny)        ! square half-diagonal (grows over time)
   real    :: T(nx,ny)         ! temperature
   real    :: Tb(nx,ny)        ! temperature buffer
   real    :: dTc(nx,ny)       ! critical undercooling for bulk nucleation

   integer, parameter :: maxg = nx*ny
   real    :: gtheta(maxg)     ! per-grain crystallographic orientation
   integer :: gtype(maxg)      ! per-grain type (COLUMNAR / EQUIAXED)
   integer :: ngrain           ! number of grains created
end module state

!==============================================================================
program solidification_cet
   use params
   use state
   implicit none
   integer :: step
   integer :: seed_size
   integer, allocatable :: seed(:)

   ! reproducible random numbers
   call random_seed(size=seed_size)
   allocate(seed(seed_size))
   seed = 20260906
   call random_seed(put=seed)

   call init_domain()
   call seed_walls()          ! surface nucleation -> columnar grains

   print '(A)', '=============================================================='
   print '(A)', '  CA solidification: columnar (walls) + equiaxed (centre)'
   print '(A)', '=============================================================='
   print '(A,I0,A,I0)', '  grid            : ', nx, ' x ', ny
   print '(A,I0)',       '  steps           : ', nsteps
   print '(A,I0)',       '  wall nuclei     : ', ngrain
   print '(A)', '--------------------------------------------------------------'
   print '(A)', '   step   %solid   #columnar   #equiaxed   Tcentre'

   do step = 1, nsteps
      call heat_step()                          ! conduction + cooling
      if (mod(step,nucEvery) == 0) call bulk_nucleation()
      call grow_and_capture()                   ! dendrite-envelope growth

      if (mod(step,nout) == 0 .or. step == nsteps) then
         call report(step)
         call write_ppm_grains(step)
      end if
   end do

   print '(A)', '--------------------------------------------------------------'
   call ascii_map()
   call write_ppm_zones()
   call write_grain_id()
   print '(A)', '=============================================================='
   print '(A)', '  Done.  Output: grains_XXXX.ppm, zones.ppm, grain_id.dat'
   print '(A)', '=============================================================='

end program solidification_cet

!==============================================================================
subroutine init_domain()
   use params
   use state
   implicit none
   integer :: i, j
   real    :: r
   real, external :: gauss

   ngrain = 0
   st  = LIQUID
   gid = 0
   gx  = 0.0; gy = 0.0; Lh = 0.0
   T   = T0

   ! mould walls (outer ring) -----------------------------------------------
   do i = 1, nx
      st(i,1)  = WALL;  st(i,ny) = WALL
      T(i,1)   = Twall; T(i,ny)  = Twall
   end do
   do j = 1, ny
      st(1,j)  = WALL;  st(nx,j) = WALL
      T(1,j)   = Twall; T(nx,j)  = Twall
   end do

   ! assign per-cell critical undercooling for bulk nucleation --------------
   ! Only a fraction of interior cells are potential nucleation sites; the
   ! rest get a huge threshold so they never nucleate on their own.
   dTc = 1.0e6
   do j = 2, ny-1
      do i = 2, nx-1
         call random_number(r)
         if (r < siteFrac) dTc(i,j) = max(0.5, gauss(dTnMean, dTnSig))
      end do
   end do
end subroutine init_domain

!------------------------------------------------------------------------------
! Surface (heterogeneous) nucleation: seed the material layer adjacent to the
! mould walls with densely spaced nuclei of random orientation.  These grow
! inward and compete -> columnar zone.
!------------------------------------------------------------------------------
subroutine seed_walls()
   use params
   use state
   implicit none
   integer :: i, j

   do i = 2, nx-1
      call try_seed(i, 2,    COLUMNAR)
      call try_seed(i, ny-1, COLUMNAR)
   end do
   do j = 2, ny-1
      call try_seed(2,    j, COLUMNAR)
      call try_seed(nx-1, j, COLUMNAR)
   end do
end subroutine seed_walls

subroutine try_seed(i, j, gtyp)
   use params
   use state
   implicit none
   integer, intent(in) :: i, j, gtyp
   real :: r, th
   if (st(i,j) /= LIQUID) return
   call random_number(r)
   if (r > pWall) return
   call random_number(th)
   call new_grain(i, j, th*0.5*PI, gtyp)
end subroutine try_seed

!------------------------------------------------------------------------------
! Continuous bulk nucleation in the undercooled melt -> equiaxed grains.
!------------------------------------------------------------------------------
subroutine bulk_nucleation()
   use params
   use state
   implicit none
   integer :: i, j
   real :: dT, th

   do j = 2, ny-1
      do i = 2, nx-1
         if (st(i,j) /= LIQUID) cycle
         dT = TL - T(i,j)
         if (dT >= dTc(i,j)) then
            call random_number(th)
            call new_grain(i, j, th*0.5*PI, EQUIAXED)
         end if
      end do
   end do
end subroutine bulk_nucleation

!------------------------------------------------------------------------------
! Create a new grain at cell (i,j): a growing square of size ~1 centred on the
! cell.  Also releases latent heat (recalescence).
!------------------------------------------------------------------------------
subroutine new_grain(i, j, th, gtyp)
   use params
   use state
   implicit none
   integer, intent(in) :: i, j, gtyp
   real,    intent(in) :: th

   ngrain = ngrain + 1
   gtheta(ngrain) = th
   gtype(ngrain)  = gtyp

   st(i,j)  = GROWING
   gid(i,j) = ngrain
   gx(i,j)  = real(i)
   gy(i,j)  = real(j)
   Lh(i,j)  = 0.7          ! small initial half-diagonal
   T(i,j)   = T(i,j) + Lheat
end subroutine new_grain

!==============================================================================
! Explicit heat conduction (FTCS) + uniform cooling.  Walls held at Twall.
!==============================================================================
subroutine heat_step()
   use params
   use state
   implicit none
   integer :: i, j

   Tb = T
   do j = 2, ny-1
      do i = 2, nx-1
         Tb(i,j) = T(i,j) + Ddiff*( T(i+1,j) + T(i-1,j) + T(i,j+1) + T(i,j-1) &
                                    - 4.0*T(i,j) ) - Qcool
      end do
   end do
   ! copy back, keep walls cold
   do j = 2, ny-1
      do i = 2, nx-1
         T(i,j) = Tb(i,j)
      end do
   end do
   do i = 1, nx
      T(i,1) = Twall; T(i,ny) = Twall
   end do
   do j = 1, ny
      T(1,j) = Twall; T(nx,j) = Twall
   end do
end subroutine heat_step

!==============================================================================
! Growth of dendrite envelopes + decentered-square capture.
!
!  Each GROWING cell owns a square (centre gx,gy, half-diagonal Lh) rotated by
!  the grain orientation theta.  The four corners are the <10> dendrite arms.
!  A liquid neighbour whose centre falls inside the square is captured; it is
!  given a NEW square of the same orientation, DECENTERED onto the nearest
!  crystallographic axis so that the neighbour sits exactly on the new square's
!  edge.  This keeps growth aligned to <10> and reduces grid anisotropy.
!==============================================================================
subroutine grow_and_capture()
   use params
   use state
   implicit none
   integer :: i, j, di, dj, ni, nj, g
   real :: th, c, s, dT, v
   real :: rx, ry, a, b, la, lb, Ln, cnx, cny
   logical :: hasLiquid

   do j = 2, ny-1
      do i = 2, nx-1
         if (st(i,j) /= GROWING) cycle
         g  = gid(i,j)
         th = gtheta(g)
         c  = cos(th);  s = sin(th)

         ! ---- grow the square (only into undercooled melt) ----------------
         dT = TL - T(i,j)
         if (dT > 0.0) then
            v = mu*dT*dT
            if (v > vmax) v = vmax
            Lh(i,j) = Lh(i,j) + v
         end if

         ! ---- attempt to capture liquid neighbours (Moore, 8) -------------
         hasLiquid = .false.
         do dj = -1, 1
            do di = -1, 1
               if (di == 0 .and. dj == 0) cycle
               ni = i + di;  nj = j + dj
               if (st(ni,nj) /= LIQUID) cycle

               rx = real(ni) - gx(i,j)
               ry = real(nj) - gy(i,j)
               a  =  rx*c + ry*s        ! local coord along crystal axis 1
               b  = -rx*s + ry*c        ! local coord along crystal axis 2

               if (abs(a) + abs(b) <= Lh(i,j)) then
                  ! ---- capture: build decentered square for (ni,nj) -------
                  if (abs(a) >= abs(b)) then
                     la = a;   lb = 0.0;  Ln = abs(b)   ! primary along axis 1
                  else
                     la = 0.0; lb = b;    Ln = abs(a)   ! primary along axis 2
                  end if
                  cnx = gx(i,j) + (la*c - lb*s)
                  cny = gy(i,j) + (la*s + lb*c)

                  st(ni,nj)  = FRESH
                  gid(ni,nj) = g
                  gx(ni,nj)  = cnx
                  gy(ni,nj)  = cny
                  Lh(ni,nj)  = Ln
                  T(ni,nj)   = T(ni,nj) + Lheat   ! recalescence
               else
                  hasLiquid = .true.
               end if
            end do
         end do

         if (.not. hasLiquid) st(i,j) = SOLID   ! fully surrounded
      end do
   end do

   ! promote freshly captured cells to growing interface cells
   do j = 2, ny-1
      do i = 2, nx-1
         if (st(i,j) == FRESH) st(i,j) = GROWING
      end do
   end do
end subroutine grow_and_capture

!==============================================================================
!  Utility / diagnostics
!==============================================================================
real function gauss(mean, sig)
   use params, only: PI
   implicit none
   real, intent(in) :: mean, sig
   real :: u1, u2
   call random_number(u1)
   call random_number(u2)
   if (u1 < 1.0e-12) u1 = 1.0e-12
   gauss = mean + sig*sqrt(-2.0*log(u1))*cos(2.0*PI*u2)
end function gauss

subroutine report(step)
   use params
   use state
   implicit none
   integer, intent(in) :: step
   integer :: i, j, nsol, ncol, neqx
   real :: fsolid, Tc

   nsol = 0; ncol = 0; neqx = 0
   do j = 2, ny-1
      do i = 2, nx-1
         if (st(i,j) == GROWING .or. st(i,j) == SOLID) then
            nsol = nsol + 1
            if (gtype(gid(i,j)) == COLUMNAR) then
               ncol = ncol + 1
            else
               neqx = neqx + 1
            end if
         end if
      end do
   end do
   fsolid = 100.0*real(nsol)/real((nx-2)*(ny-2))
   Tc = T(nx/2, ny/2)
   print '(I7,F9.1,I12,I12,F10.2)', step, fsolid, ncol, neqx, Tc
end subroutine report

!------------------------------------------------------------------------------
! Downsampled ASCII map so the structure is visible in the terminal:
!   '#' columnar solid   'o' equiaxed solid   '.' liquid   ' ' wall
!------------------------------------------------------------------------------
subroutine ascii_map()
   use params
   use state
   implicit none
   integer, parameter :: W = 74
   integer :: bi, bj, i, j
   character(len=1) :: ch
   character(len=W) :: line

   print '(A)', '  ASCII microstructure map ( # columnar  o equiaxed  . liquid ):'
   do bj = 1, W
      j = 1 + int((real(bj)-0.5)/real(W)*real(ny))
      if (j < 1) j = 1
      if (j > ny) j = ny
      do bi = 1, W
         i = 1 + int((real(bi)-0.5)/real(W)*real(nx))
         if (i < 1) i = 1
         if (i > nx) i = nx
         if (st(i,j) == WALL) then
            ch = ' '
         else if (st(i,j) == GROWING .or. st(i,j) == SOLID) then
            if (gtype(gid(i,j)) == COLUMNAR) then
               ch = '#'
            else
               ch = 'o'
            end if
         else
            ch = '.'
         end if
         line(bi:bi) = ch
      end do
      print '(3X,A)', line
   end do
end subroutine ascii_map

!------------------------------------------------------------------------------
! PPM (P6) colour map: one pseudo-random colour per grain.
!------------------------------------------------------------------------------
subroutine write_ppm_grains(step)
   use params
   use state
   implicit none
   integer, intent(in) :: step
   character(len=64) :: fname
   integer :: i, j, g, u
   integer :: ir, ig, ib
   character(len=1) :: cr, cg, cb

   write(fname,'(A,I4.4,A)') 'grains_', step, '.ppm'
   open(newunit=u, file=trim(fname), access='stream', form='unformatted', &
        status='replace')
   call ppm_header(u)
   do j = ny, 1, -1
      do i = 1, nx
         if (st(i,j) == WALL) then
            ir = 40; ig = 40; ib = 40
         else if (st(i,j) == LIQUID) then
            ir = 8;  ig = 12; ib = 30
         else
            g = gid(i,j)
            ir = mod(g*97 + 30,  226) + 30
            ig = mod(g*53 + 120, 226) + 30
            ib = mod(g*29 + 200, 226) + 30
         end if
         cr = char(ir); cg = char(ig); cb = char(ib)
         write(u) cr, cg, cb
      end do
   end do
   close(u)
end subroutine write_ppm_grains

!------------------------------------------------------------------------------
! PPM (P6) zone map: BLUE = columnar grains, RED = equiaxed grains.
!------------------------------------------------------------------------------
subroutine write_ppm_zones()
   use params
   use state
   implicit none
   integer :: i, j, g, u, shade
   integer :: ir, ig, ib
   character(len=1) :: cr, cg, cb

   open(newunit=u, file='zones.ppm', access='stream', form='unformatted', &
        status='replace')
   call ppm_header(u)
   do j = ny, 1, -1
      do i = 1, nx
         if (st(i,j) == WALL) then
            ir = 30; ig = 30; ib = 30
         else if (st(i,j) == LIQUID) then
            ir = 0;  ig = 0;  ib = 0
         else
            g = gid(i,j)
            shade = mod(g*47, 90)
            if (gtype(g) == COLUMNAR) then
               ir = 40 + shade; ig = 90 + shade; ib = 255      ! blue
            else
               ir = 255; ig = 60 + shade; ib = 40 + shade      ! red/orange
            end if
         end if
         cr = char(ir); cg = char(ig); cb = char(ib)
         write(u) cr, cg, cb
      end do
   end do
   close(u)
end subroutine write_ppm_zones

subroutine ppm_header(u)
   use params
   implicit none
   integer, intent(in) :: u
   character(len=1), parameter :: nl = char(10)
   character(len=32) :: dims
   write(dims,'(I0,1X,I0)') nx, ny
   write(u) 'P6', nl
   write(u) trim(dims), nl
   write(u) '255', nl
end subroutine ppm_header

!------------------------------------------------------------------------------
! Final grain-id field as ASCII (ny rows, nx columns) for post-processing.
!------------------------------------------------------------------------------
subroutine write_grain_id()
   use params
   use state
   implicit none
   integer :: i, j, u
   open(newunit=u, file='grain_id.dat', status='replace')
   do j = ny, 1, -1
      write(u,'(*(I0,1X))') (gid(i,j), i=1,nx)
   end do
   close(u)
end subroutine write_grain_id
