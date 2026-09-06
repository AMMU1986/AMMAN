!==============================================================================
!  dendritic_cet.f90
!
!  2-D interface-resolved DENDRITIC cellular automaton for the
!  columnar-to-equiaxed transition (CET) -- an upgrade of the grain-envelope
!  model in solidification_cet.f90 that produces REAL dendrites with
!  PRIMARY, SECONDARY and TERTIARY branches.
!
!  Why this version branches and the envelope one does not
!  -------------------------------------------------------
!  Side-branching is a morphological (Mullins-Sekerka) instability.  It only
!  appears when three ingredients act together:
!     1. DIFFUSION-LIMITED growth: a solid cell releases latent heat
!        (recalescence) into a thermal field U that diffuses.  Heat piles up
!        in the concave grooves between arms and starves them, while tips
!        that poke into the cold undercooled melt keep growing.
!     2. CRYSTALLOGRAPHIC ANISOTROPY: growth is fastest along the grain's
!        four <10> directions (4-fold), so the instability organises into
!        oriented primary arms rather than a random fractal.
!     3. NOISE: small stochastic perturbations of the interface seed the
!        side-branches that the instability then amplifies.
!
!  Geometry (same CET set-up as before):
!     * Cold mould walls (Dirichlet, strongly undercooled) -> columnar
!       dendrites nucleate on the walls and grow inward.
!     * The centre cools more slowly; when it is undercooled enough, bulk
!       (equiaxed) dendrites nucleate and branch freely.
!
!  Model (dimensionless units)
!     U ............ thermal field.  U = 0 is the equilibrium (liquidus);
!                    melt is undercooled (U < 0).  Solidification releases
!                    latent heat, raising U locally.
!     state ........ LIQUID / SOLID / WALL  (sharp interface, no mushy fs)
!     Growth rule .. a liquid cell adjacent to solid freezes with a
!                    probability  P = krate * undercooling * anisotropy,
!                    updated synchronously so there is no scan-order bias.
!
!  Output:
!     dend_XXXX.ppm  colour-per-grain frames (branches shown vs black melt)
!     zones.ppm      blue = columnar dendrites, red = equiaxed dendrites
!     field.ppm      thermal field U (blue cold -> red hot) at the end
!     + ASCII map and statistics to the terminal.
!
!  Build : gfortran -O2 -o dend dendritic_cet.f90
!  Run   : ./dend      (convert *.ppm with the included ppm2png.py)
!==============================================================================

module params
   implicit none
   ! ---- grid / time ------------------------------------------------------
   integer, parameter :: nx = 300, ny = 300
   integer, parameter :: nsteps = 24000
   integer, parameter :: nout   = 3000

   ! ---- thermal field ----------------------------------------------------
   real, parameter :: Ddiff = 0.08     ! LOW diffusion -> latent heat stays local
   real, parameter :: U0    = -0.20     ! mild initial melt undercooling
   real, parameter :: Uwall = -0.55     ! cold-wall undercooling (drives columnar)
   real, parameter :: Lheat = 2.00      ! STRONG recalescence -> grooves stall
   real, parameter :: Qcool = 0.00015   ! slow uniform cooling per step

   ! ---- growth kinetics --------------------------------------------------
   real, parameter :: krate  = 0.12     ! SLOW freezing -> diffusion keeps up
   real, parameter :: Aaniso = 0.90     ! strong 4-fold anisotropy (0..1)
   real, parameter :: pAniso = 6.0      ! sharp <10> arm lobes
   real, parameter :: noise  = 0.40     ! stochastic noise seeds side-branches

   ! ---- nucleation -------------------------------------------------------
   integer, parameter :: wallStep = 42  ! spacing of columnar seeds on walls
   real, parameter :: bulkSiteFrac = 0.00004 ! fraction of cells = bulk sites
   real, parameter :: dTnMean = 0.50    ! mean bulk critical undercooling
   real, parameter :: dTnSig  = 0.08
   integer, parameter :: nucEvery = 12

   ! ---- states -----------------------------------------------------------
   integer, parameter :: LIQUID = 0, SOLID = 1, WALL = 4
   integer, parameter :: COLUMNAR = 1, EQUIAXED = 2
   real, parameter :: PI = 3.14159265358979
end module params

!------------------------------------------------------------------------------
module state
   use params
   implicit none
   integer :: st(nx,ny)      ! LIQUID / SOLID / WALL
   integer :: gid(nx,ny)     ! grain id (0 = none)
   integer :: claim(nx,ny)   ! grain that will freeze a cell this step (0=none)
   real    :: U(nx,ny)       ! thermal field
   real    :: Un(nx,ny)      ! buffer

   integer, parameter :: maxg = nx*ny
   real    :: gtheta(maxg)   ! per-grain orientation
   integer :: gtype(maxg)    ! COLUMNAR / EQUIAXED
   integer :: ngrain

   ! neighbour offsets (8) and the outward-growth angle from neighbour to cell
   integer :: offi(8), offj(8)
   real    :: offang(8)
end module state

!==============================================================================
program dendritic_cet
   use params
   use state
   implicit none
   integer :: step, seed_size
   integer, allocatable :: seed(:)

   call random_seed(size=seed_size)
   allocate(seed(seed_size));  seed = 20260906;  call random_seed(put=seed)

   call init_domain()
   call seed_walls()

   print '(A)', '=================================================================='
   print '(A)', '  Dendritic CA: branched columnar (walls) + equiaxed (centre)'
   print '(A)', '=================================================================='
   print '(A,I0,A,I0,A,I0)', '  grid ', nx, ' x ', ny, ',  steps ', nsteps
   print '(A,I0)', '  columnar wall nuclei : ', ngrain
   print '(A)', '------------------------------------------------------------------'
   print '(A)', '    step   %solid   #columnar   #equiaxed    Ucentre'

   do step = 1, nsteps
      call diffuse_field()
      if (mod(step,nucEvery) == 0) call bulk_nucleation()
      call grow_step()
      if (mod(step,nout) == 0 .or. step == nsteps) then
         call report(step)
         call write_ppm_grains(step)
      end if
   end do

   print '(A)', '------------------------------------------------------------------'
   call grain_counts()
   call ascii_map()
   call write_ppm_zones()
   call write_ppm_field()
   print '(A)', '  Done.  Output: dend_XXXX.ppm, zones.ppm, field.ppm'
   print '(A)', '=================================================================='
end program dendritic_cet

!==============================================================================
subroutine init_domain()
   use params
   use state
   implicit none
   integer :: i, j, k

   ngrain = 0
   st = LIQUID;  gid = 0;  claim = 0;  U = U0

   ! mould walls (outer ring): cold heat sink
   do i = 1, nx
      st(i,1) = WALL;  st(i,ny) = WALL;  U(i,1) = Uwall;  U(i,ny) = Uwall
   end do
   do j = 1, ny
      st(1,j) = WALL;  st(nx,j) = WALL;  U(1,j) = Uwall;  U(nx,j) = Uwall
   end do

   ! 8-neighbour offsets and the outward angle (neighbour -> cell)
   k = 0
   do j = -1, 1
      do i = -1, 1
         if (i == 0 .and. j == 0) cycle
         k = k + 1
         offi(k) = i;  offj(k) = j
         offang(k) = atan2(real(-j), real(-i))   ! direction from neighbour to cell
      end do
   end do
end subroutine init_domain

!------------------------------------------------------------------------------
! Columnar seeds: evenly spaced on the wall-adjacent layer, random orientation.
!------------------------------------------------------------------------------
subroutine seed_walls()
   use params
   use state
   implicit none
   integer :: i, j

   do i = 2+wallStep/2, nx-1, wallStep
      call put_seed(i, 2,    COLUMNAR)
      call put_seed(i, ny-1, COLUMNAR)
   end do
   do j = 2+wallStep/2, ny-1, wallStep
      call put_seed(2,    j, COLUMNAR)
      call put_seed(nx-1, j, COLUMNAR)
   end do
end subroutine seed_walls

subroutine put_seed(i, j, gtyp)
   use params
   use state
   implicit none
   integer, intent(in) :: i, j, gtyp
   real :: th
   if (st(i,j) /= LIQUID) return
   call random_number(th)
   ngrain = ngrain + 1
   gtheta(ngrain) = th*0.5*PI          ! 0..90 deg (4-fold symmetry)
   gtype(ngrain)  = gtyp
   st(i,j)  = SOLID
   gid(i,j) = ngrain
   U(i,j)   = U(i,j) + Lheat
end subroutine put_seed

!------------------------------------------------------------------------------
! Bulk (equiaxed) nucleation in sufficiently undercooled melt.
!------------------------------------------------------------------------------
subroutine bulk_nucleation()
   use params
   use state
   implicit none
   integer :: i, j
   real :: r, th, dTc
   real, external :: gauss

   do j = 3, ny-2
      do i = 3, nx-2
         if (st(i,j) /= LIQUID) cycle
         call random_number(r)
         if (r >= bulkSiteFrac) cycle          ! only sparse sites are potent
         dTc = max(0.2, gauss(dTnMean, dTnSig))
         if (-U(i,j) >= dTc) then               ! undercooling exceeds threshold
            call random_number(th)
            ngrain = ngrain + 1
            gtheta(ngrain) = th*0.5*PI
            gtype(ngrain)  = EQUIAXED
            st(i,j)  = SOLID
            gid(i,j) = ngrain
            U(i,j)   = U(i,j) + Lheat
         end if
      end do
   end do
end subroutine bulk_nucleation

!==============================================================================
! Explicit diffusion of the thermal field + uniform cooling.  Walls fixed cold.
!==============================================================================
subroutine diffuse_field()
   use params
   use state
   implicit none
   integer :: i, j

   do j = 2, ny-1
      do i = 2, nx-1
         Un(i,j) = U(i,j) + Ddiff*( U(i+1,j)+U(i-1,j)+U(i,j+1)+U(i,j-1) &
                                    - 4.0*U(i,j) ) - Qcool
      end do
   end do
   do j = 2, ny-1
      do i = 2, nx-1
         U(i,j) = Un(i,j)
      end do
   end do
   do i = 1, nx
      U(i,1) = Uwall;  U(i,ny) = Uwall
   end do
   do j = 1, ny
      U(1,j) = Uwall;  U(nx,j) = Uwall
   end do
end subroutine diffuse_field

!==============================================================================
! One growth sweep: liquid cells adjacent to solid may freeze.
!   P = krate * undercooling * anisotropy(direction,theta) * noise
! Synchronous update via claim() so there is no scan-order bias.
!==============================================================================
subroutine grow_step()
   use params
   use state
   implicit none
   integer :: i, j, k, ni, nj, gbest, g
   real :: driving, fbest, f, cang, P, r, rn

   claim = 0
   do j = 2, ny-1
      do i = 2, nx-1
         if (st(i,j) /= LIQUID) cycle
         driving = -U(i,j)                 ! undercooling ( >0 drives freezing )
         if (driving <= 0.0) cycle

         ! best-aligned solid neighbour sets the grain and anisotropy factor
         fbest = -1.0;  gbest = 0
         do k = 1, 8
            ni = i + offi(k);  nj = j + offj(k)
            if (st(ni,nj) /= SOLID) cycle
            g = gid(ni,nj)
            cang = cos(4.0*(offang(k) - gtheta(g)))
            f = (0.5*(1.0+cang))**pAniso     ! lobe in [0,1], peaked on <10>
            f = (1.0 - Aaniso) + Aaniso*f    ! blend so grooves still fill slowly
            if (f > fbest) then
               fbest = f;  gbest = g
            end if
         end do
         if (gbest == 0) cycle              ! no solid neighbour -> cannot grow

         call random_number(rn)
         P = krate * driving * fbest * (1.0 - noise + noise*rn)
         if (P > 1.0) P = 1.0
         call random_number(r)
         if (r < P) claim(i,j) = gbest
      end do
   end do

   ! commit frozen cells + release latent heat
   do j = 2, ny-1
      do i = 2, nx-1
         if (claim(i,j) /= 0) then
            st(i,j)  = SOLID
            gid(i,j) = claim(i,j)
            U(i,j)   = U(i,j) + Lheat
         end if
      end do
   end do
end subroutine grow_step

!==============================================================================
!  Diagnostics / output
!==============================================================================
real function gauss(mean, sig)
   use params, only: PI
   implicit none
   real, intent(in) :: mean, sig
   real :: u1, u2
   call random_number(u1);  call random_number(u2)
   if (u1 < 1.0e-12) u1 = 1.0e-12
   gauss = mean + sig*sqrt(-2.0*log(u1))*cos(2.0*PI*u2)
end function gauss

subroutine report(step)
   use params
   use state
   implicit none
   integer, intent(in) :: step
   integer :: i, j, nsol, ncol, neqx
   real :: fsolid

   nsol = 0; ncol = 0; neqx = 0
   do j = 2, ny-1
      do i = 2, nx-1
         if (st(i,j) == SOLID) then
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
   print '(I8,F9.1,I12,I12,F11.3)', step, fsolid, ncol, neqx, U(nx/2,ny/2)
end subroutine report

subroutine grain_counts()
   use params
   use state
   implicit none
   integer :: g, nc, ne
   nc = 0; ne = 0
   do g = 1, ngrain
      if (gtype(g) == COLUMNAR) then
         nc = nc + 1
      else
         ne = ne + 1
      end if
   end do
   print '(A,I0,A,I0,A,I0)', '  grains: total ', ngrain, &
         '   columnar ', nc, '   equiaxed ', ne
end subroutine grain_counts

subroutine ascii_map()
   use params
   use state
   implicit none
   integer, parameter :: W = 74
   integer :: bi, bj, i, j
   character(len=1) :: ch
   character(len=W) :: line

   print '(A)', '  ASCII map ( # columnar   o equiaxed   . liquid ):'
   do bj = 1, W
      j = 1 + int((real(bj)-0.5)/real(W)*real(ny))
      do bi = 1, W
         i = 1 + int((real(bi)-0.5)/real(W)*real(nx))
         if (st(i,j) == WALL) then
            ch = ' '
         else if (st(i,j) == SOLID) then
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

subroutine write_ppm_grains(step)
   use params
   use state
   implicit none
   integer, intent(in) :: step
   character(len=64) :: fname
   integer :: i, j, g, u2, ir, ig, ib

   write(fname,'(A,I4.4,A)') 'dend_', step, '.ppm'
   open(newunit=u2, file=trim(fname), access='stream', form='unformatted', status='replace')
   call ppm_header(u2)
   do j = ny, 1, -1
      do i = 1, nx
         if (st(i,j) == WALL) then
            ir = 45; ig = 45; ib = 45
         else if (st(i,j) == LIQUID) then
            ir = 6; ig = 10; ib = 24
         else
            g = gid(i,j)
            ir = mod(g*97 + 30, 226) + 30
            ig = mod(g*53 + 120, 226) + 30
            ib = mod(g*29 + 200, 226) + 30
         end if
         write(u2) char(ir), char(ig), char(ib)
      end do
   end do
   close(u2)
end subroutine write_ppm_grains

subroutine write_ppm_zones()
   use params
   use state
   implicit none
   integer :: i, j, g, u2, shade, ir, ig, ib

   open(newunit=u2, file='zones.ppm', access='stream', form='unformatted', status='replace')
   call ppm_header(u2)
   do j = ny, 1, -1
      do i = 1, nx
         if (st(i,j) == WALL) then
            ir = 30; ig = 30; ib = 30
         else if (st(i,j) == LIQUID) then
            ir = 0; ig = 0; ib = 0
         else
            g = gid(i,j);  shade = mod(g*47, 90)
            if (gtype(g) == COLUMNAR) then
               ir = 40+shade; ig = 90+shade; ib = 255
            else
               ir = 255; ig = 60+shade; ib = 40+shade
            end if
         end if
         write(u2) char(ir), char(ig), char(ib)
      end do
   end do
   close(u2)
end subroutine write_ppm_zones

subroutine write_ppm_field()
   use params
   use state
   implicit none
   integer :: i, j, u2, ir, ig, ib
   real :: t

   open(newunit=u2, file='field.ppm', access='stream', form='unformatted', status='replace')
   call ppm_header(u2)
   do j = ny, 1, -1
      do i = 1, nx
         t = (U(i,j) - Uwall) / (Lheat - Uwall)      ! normalise ~0..1
         if (t < 0.0) t = 0.0
         if (t > 1.0) t = 1.0
         ir = int(255.0*t)
         ig = int(120.0*(1.0-abs(2.0*t-1.0)))
         ib = int(255.0*(1.0-t))
         write(u2) char(ir), char(ig), char(ib)
      end do
   end do
   close(u2)
end subroutine write_ppm_field

subroutine ppm_header(u2)
   use params
   implicit none
   integer, intent(in) :: u2
   character(len=1), parameter :: nl = char(10)
   character(len=32) :: dims
   write(dims,'(I0,1X,I0)') nx, ny
   write(u2) 'P6', nl
   write(u2) trim(dims), nl
   write(u2) '255', nl
end subroutine ppm_header
