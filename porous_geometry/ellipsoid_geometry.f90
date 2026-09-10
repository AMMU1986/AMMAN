!==============================================================================
!  ellipsoid_geometry.f90
!
!  Generation of 3-D random packed-ELLIPSOID porous geometries.  This is the
!  ellipsoidal counterpart of porous_geometry.f90: instead of spheres, each
!  pore is a randomly-oriented ellipsoid with three independent semi-axes
!  (a, b, c) and an orientation given by three Euler angles.
!
!  Two generation methods (mirroring the sphere flowcharts):
!
!    Method 1 : Constant ellipsoid shape/size
!               - fixed semi-axes (A1, B1, C1), random orientation
!               - random-sequential placement with a rejection test
!                 (conservative bounding-sphere distance check on centres)
!               - voxelize on a regular grid  (inside ellipsoid = 0 = solid,
!                                               outside          = 1 = pore)
!               - "grid averaging by some factor"
!
!    Method 2 : Specified porosity + variable ellipsoid size
!               - semi-axes a,b,c each random in [AXMIN,AXMAX], random
!                 orientation, allowed overlap o in [OMIN,OMAX]
!               - keep adding ellipsoids (rejecting those whose bounding
!                 spheres are closer than r_i + r_j - o) until the solid
!                 volume reaches the required fraction (target porosity)
!               - voxelize + coarse-grain
!
!  Inside/outside test for an ellipsoid centred at p0 with orientation matrix
!  R (columns = principal axes) and semi-axes (a,b,c):
!        let d = p - p0 ,  u = R^T d           (rotate into body frame)
!        inside  <=>  (u_x/a)^2 + (u_y/b)^2 + (u_z/c)^2 <= 1
!
!  Output for each method:
!     *.vtk      legacy VTK STRUCTURED_POINTS scalar field (0 = solid, 1 = pore)
!     *.dat      one line per ellipsoid:  x y z  a b c  phi theta psi
!     printed    achieved porosity, ellipsoid count, timing
!
!  Build :   gfortran -O2 -o ellipsoid_geometry ellipsoid_geometry.f90
!  Run   :   ./ellipsoid_geometry
!
!==============================================================================
module ell_params
   implicit none
   integer,  parameter :: wp = selected_real_kind(15, 307)   ! double precision

   real(wp), parameter :: PI = acos(-1.0_wp)

   !--- Physical domain (cube 0..LDOM) ----------------------------------------
   real(wp), parameter :: LDOM = 25.0_wp

   !--- Grid ------------------------------------------------------------------
   integer,  parameter :: NG   = 150            ! fine grid points per side
   integer,  parameter :: AVGF = 3              ! grid-averaging factor
                                                ! (NG must be divisible by AVGF)

   !--- Method 1 (constant ellipsoid) -----------------------------------------
   integer,  parameter :: NELL1 = 70            ! number of ellipsoids to place
   real(wp), parameter :: A1 = 2.4_wp           ! fixed semi-axes
   real(wp), parameter :: B1 = 1.5_wp
   real(wp), parameter :: C1 = 1.1_wp
   integer,  parameter :: MAXTRY1 = 800000      ! attempts before giving up

   !--- Method 2 (variable ellipsoid, target porosity) ------------------------
   real(wp), parameter :: AXMIN = 0.9_wp        ! min semi-axis
   real(wp), parameter :: AXMAX = 2.8_wp        ! max semi-axis
   real(wp), parameter :: OMIN  = 0.0_wp        ! min allowed overlap
   real(wp), parameter :: OMAX  = 1.2_wp        ! max allowed overlap
   real(wp), parameter :: TARGET_POROSITY = 0.55_wp   ! desired void fraction
   integer,  parameter :: MAXTRY2 = 8000000     ! attempts before giving up
   integer,  parameter :: MAXELL2 = 40000       ! storage cap
end module ell_params
!==============================================================================


!------------------------------------------------------------------------------
! Utilities: RNG, random rotation matrix, VTK writer.
!------------------------------------------------------------------------------
module ell_utils
   use ell_params
   implicit none
contains

   function uran(a, b) result(x)
      real(wp), intent(in) :: a, b
      real(wp)             :: x, u
      call random_number(u)
      x = a + (b - a)*u
   end function uran

   subroutine seed_rng(seed_val)
      integer, intent(in) :: seed_val
      integer :: n, i, j
      integer, allocatable :: s(:)
      call random_seed(size = n)
      allocate(s(n))
      if (seed_val > 0) then
         do i = 1, n
            s(i) = seed_val + 37*i
         end do
      else
         call system_clock(count = i)
         do j = 1, n
            s(j) = i + 41*j
         end do
      end if
      call random_seed(put = s)
      deallocate(s)
   end subroutine seed_rng

   !--- random ZXZ Euler angles (phi about z, theta about x', psi about z'') --
   subroutine random_euler(phi, theta, psi)
      real(wp), intent(out) :: phi, theta, psi
      real(wp) :: u
      phi = uran(0.0_wp, 2.0_wp*PI)
      call random_number(u)                 ! cos(theta) uniform -> uniform axis
      theta = acos(2.0_wp*u - 1.0_wp)
      psi = uran(0.0_wp, 2.0_wp*PI)
   end subroutine random_euler

   !--- rotation matrix R (body -> world) from ZXZ Euler angles --------------
   !    columns of R are the ellipsoid principal axes expressed in world coords
   subroutine euler_matrix(phi, theta, psi, R)
      real(wp), intent(in)  :: phi, theta, psi
      real(wp), intent(out) :: R(3,3)
      real(wp) :: c1, s1, c2, s2, c3, s3
      c1 = cos(phi);   s1 = sin(phi)
      c2 = cos(theta); s2 = sin(theta)
      c3 = cos(psi);   s3 = sin(psi)
      ! R = Rz(phi) Rx(theta) Rz(psi)
      R(1,1) =  c1*c3 - s1*c2*s3
      R(1,2) = -c1*s3 - s1*c2*c3
      R(1,3) =  s1*s2
      R(2,1) =  s1*c3 + c1*c2*s3
      R(2,2) = -s1*s3 + c1*c2*c3
      R(2,3) = -c1*s2
      R(3,1) =  s2*s3
      R(3,2) =  s2*c3
      R(3,3) =  c2
   end subroutine euler_matrix

   subroutine write_vtk(fname, nx, ny, nz, h, vol)
      character(len=*), intent(in) :: fname
      integer,          intent(in) :: nx, ny, nz
      real(wp),         intent(in) :: h
      real(wp),         intent(in) :: vol(nx, ny, nz)
      integer :: u, i, j, k
      open(newunit=u, file=fname, status='replace', action='write')
      write(u,'(A)') '# vtk DataFile Version 3.0'
      write(u,'(A)') 'random packed-ellipsoid porous geometry'
      write(u,'(A)') 'ASCII'
      write(u,'(A)') 'DATASET STRUCTURED_POINTS'
      write(u,'(A,3(1x,I0))') 'DIMENSIONS', nx, ny, nz
      write(u,'(A,3(1x,F0.6))') 'ORIGIN', 0.0_wp, 0.0_wp, 0.0_wp
      write(u,'(A,3(1x,F0.6))') 'SPACING', h, h, h
      write(u,'(A,1x,I0)') 'POINT_DATA', nx*ny*nz
      write(u,'(A)') 'SCALARS phase float 1'
      write(u,'(A)') 'LOOKUP_TABLE default'
      do k = 1, nz
         do j = 1, ny
            do i = 1, nx
               write(u,'(F0.6)') vol(i,j,k)
            end do
         end do
      end do
      close(u)
   end subroutine write_vtk

end module ell_utils
!==============================================================================


!------------------------------------------------------------------------------
! Voxelization + averaging for ellipsoids.
!------------------------------------------------------------------------------
module ell_voxel
   use ell_params
   use ell_utils, only : euler_matrix
   implicit none
contains

   !----------------------------------------------------------------------
   ! Voxelize a set of oriented ellipsoids onto the fine NGxNGxNG grid.
   !   grid = 0.0 -> inside an ellipsoid (solid)
   !   grid = 1.0 -> pore space (void)
   ! The scan is limited to each ellipsoid's axis-aligned bounding box
   ! (half-widths = max semi-axis, a safe superset).
   !----------------------------------------------------------------------
   subroutine voxelize(nell, cx, cy, cz, sa, sb, sc, ephi, eth, epsi, h, grid)
      integer,  intent(in)  :: nell
      real(wp), intent(in)  :: cx(nell), cy(nell), cz(nell)
      real(wp), intent(in)  :: sa(nell), sb(nell), sc(nell)
      real(wp), intent(in)  :: ephi(nell), eth(nell), epsi(nell)
      real(wp), intent(in)  :: h
      real(wp), intent(out) :: grid(NG, NG, NG)
      integer  :: s, i, j, k, i0, i1, j0, j1, k0, k1
      real(wp) :: gx, gy, gz, dx, dy, dz, rmax, R(3,3)
      real(wp) :: ux, uy, uz, val

      grid = 1.0_wp

      do s = 1, nell
         call euler_matrix(ephi(s), eth(s), epsi(s), R)
         rmax = max(sa(s), sb(s), sc(s))          ! bounding-box half-width
         i0 = max(1 , int((cx(s) - rmax)/h) + 1)
         i1 = min(NG, int((cx(s) + rmax)/h) + 1)
         j0 = max(1 , int((cy(s) - rmax)/h) + 1)
         j1 = min(NG, int((cy(s) + rmax)/h) + 1)
         k0 = max(1 , int((cz(s) - rmax)/h) + 1)
         k1 = min(NG, int((cz(s) + rmax)/h) + 1)
         do k = k0, k1
            gz = (real(k,wp) - 0.5_wp)*h;  dz = gz - cz(s)
            do j = j0, j1
               gy = (real(j,wp) - 0.5_wp)*h;  dy = gy - cy(s)
               do i = i0, i1
                  gx = (real(i,wp) - 0.5_wp)*h;  dx = gx - cx(s)
                  ! rotate world offset into body frame:  u = R^T d
                  ux = R(1,1)*dx + R(2,1)*dy + R(3,1)*dz
                  uy = R(1,2)*dx + R(2,2)*dy + R(3,2)*dz
                  uz = R(1,3)*dx + R(2,3)*dy + R(3,3)*dz
                  val = (ux/sa(s))**2 + (uy/sb(s))**2 + (uz/sc(s))**2
                  if (val <= 1.0_wp) grid(i,j,k) = 0.0_wp
               end do
            end do
         end do
      end do
   end subroutine voxelize

   subroutine average_grid(grid, ncg, cgrid)
      real(wp), intent(in)  :: grid(NG, NG, NG)
      integer,  intent(out) :: ncg
      real(wp), allocatable, intent(out) :: cgrid(:,:,:)
      integer  :: ic, jc, kc, i, j, k, i0, j0, k0
      real(wp) :: acc, nvox
      ncg  = NG / AVGF
      allocate(cgrid(ncg, ncg, ncg))
      nvox = real(AVGF**3, wp)
      do kc = 1, ncg
         k0 = (kc-1)*AVGF
         do jc = 1, ncg
            j0 = (jc-1)*AVGF
            do ic = 1, ncg
               i0 = (ic-1)*AVGF
               acc = 0.0_wp
               do k = 1, AVGF
                  do j = 1, AVGF
                     do i = 1, AVGF
                        acc = acc + grid(i0+i, j0+j, k0+k)
                     end do
                  end do
               end do
               cgrid(ic,jc,kc) = acc / nvox
            end do
         end do
      end do
   end subroutine average_grid

   function porosity(grid) result(phi)
      real(wp), intent(in) :: grid(NG, NG, NG)
      real(wp) :: phi
      phi = sum(grid) / real(NG*NG*NG, wp)
   end function porosity

end module ell_voxel
!==============================================================================


!------------------------------------------------------------------------------
! Method 1 : constant ellipsoid shape, random orientation.
!------------------------------------------------------------------------------
module ell_method1
   use ell_params
   use ell_utils
   use ell_voxel
   implicit none
contains
   subroutine run_method1()
      real(wp) :: cx(NELL1), cy(NELL1), cz(NELL1)
      real(wp) :: sa(NELL1), sb(NELL1), sc(NELL1)
      real(wp) :: ep(NELL1), et(NELL1), es(NELL1)
      real(wp) :: grid(NG, NG, NG)
      real(wp), allocatable :: cgrid(:,:,:)
      real(wp) :: h, x, y, z, phi, theta, psi
      real(wp) :: dx, dy, dz, d2, rb, dmin, t0, t1
      integer  :: cnt, tries, s, ncg, u
      logical  :: ok

      write(*,'(/,A)') '============================================================'
      write(*,'(A)')   '  METHOD 1 : constant ellipsoid shape/size'
      write(*,'(A)')   '============================================================'

      call cpu_time(t0)
      h    = LDOM / real(NG, wp)
      rb   = max(A1, B1, C1)          ! bounding-sphere radius of one ellipsoid
      dmin = 2.0_wp*rb                ! conservative non-overlap on centres
      cnt  = 0
      tries = 0

      do while (cnt < NELL1 .and. tries < MAXTRY1)
         tries = tries + 1
         x = uran(rb, LDOM - rb)
         y = uran(rb, LDOM - rb)
         z = uran(rb, LDOM - rb)
         ok = .true.
         do s = 1, cnt
            dx = x - cx(s); dy = y - cy(s); dz = z - cz(s)
            d2 = dx*dx + dy*dy + dz*dz
            if (d2 < dmin*dmin) then
               ok = .false.; exit
            end if
         end do
         if (ok) then
            cnt = cnt + 1
            call random_euler(phi, theta, psi)
            cx(cnt)=x; cy(cnt)=y; cz(cnt)=z
            sa(cnt)=A1; sb(cnt)=B1; sc(cnt)=C1
            ep(cnt)=phi; et(cnt)=theta; es(cnt)=psi
         end if
      end do

      write(*,'(A,I0,A,I0,A)') '  placed ', cnt, ' ellipsoids in ', tries, ' attempts'
      if (cnt < NELL1) write(*,'(A)') &
         '  (packing limit reached before target count - lower NELL1 or axes)'

      call voxelize(cnt, cx, cy, cz, sa, sb, sc, ep, et, es, h, grid)
      call average_grid(grid, ncg, cgrid)

      write(*,'(A,F7.4)') '  achieved porosity (void fraction) = ', porosity(grid)
      write(*,'(A,I0,A,I0)') '  fine grid = ', NG, '^3 , coarse grid = ', ncg

      call write_vtk('ell_method1_geometry.vtk', NG, NG, NG, h, grid)
      open(newunit=u, file='ell_method1_ellipsoids.dat', status='replace', action='write')
      write(u,'(A)') '#     x           y           z           a           b           c          phi        theta        psi'
      do s = 1, cnt
         write(u,'(9(1x,F11.6))') cx(s),cy(s),cz(s), sa(s),sb(s),sc(s), ep(s),et(s),es(s)
      end do
      close(u)

      call cpu_time(t1)
      write(*,'(A,F8.3,A)') '  cpu time = ', t1 - t0, ' s'
      write(*,'(A)') '  wrote ell_method1_geometry.vtk , ell_method1_ellipsoids.dat'
      deallocate(cgrid)
   end subroutine run_method1
end module ell_method1
!==============================================================================


!------------------------------------------------------------------------------
! Method 2 : variable ellipsoid size, driven to a target porosity.
!------------------------------------------------------------------------------
module ell_method2
   use ell_params
   use ell_utils
   use ell_voxel
   implicit none
contains
   subroutine run_method2()
      real(wp), allocatable :: cx(:), cy(:), cz(:)
      real(wp), allocatable :: sa(:), sb(:), sc(:)
      real(wp), allocatable :: ep(:), et(:), es(:), rbnd(:), ovl(:)
      real(wp) :: grid(NG, NG, NG)
      real(wp), allocatable :: cgrid(:,:,:)
      real(wp) :: h, x, y, z, a, b, cc, o, phi, theta, psi
      real(wp) :: dx, dy, dz, d2, dallow, rb
      real(wp) :: vbox, vsolid, vtarget, t0, t1
      integer  :: cnt, tries, s, ncg, u
      logical  :: ok

      write(*,'(/,A)') '============================================================'
      write(*,'(A)')   '  METHOD 2 : variable ellipsoid size + specified porosity'
      write(*,'(A)')   '============================================================'

      call cpu_time(t0)
      h       = LDOM / real(NG, wp)
      vbox    = LDOM**3
      vtarget = (1.0_wp - TARGET_POROSITY) * vbox    ! required SOLID volume
      cnt = 0; tries = 0; vsolid = 0.0_wp

      allocate(cx(MAXELL2), cy(MAXELL2), cz(MAXELL2))
      allocate(sa(MAXELL2), sb(MAXELL2), sc(MAXELL2))
      allocate(ep(MAXELL2), et(MAXELL2), es(MAXELL2), rbnd(MAXELL2), ovl(MAXELL2))

      do while (vsolid < vtarget .and. tries < MAXTRY2 .and. cnt < MAXELL2)
         tries = tries + 1
         a  = uran(AXMIN, AXMAX)
         b  = uran(AXMIN, AXMAX)
         cc = uran(AXMIN, AXMAX)
         o  = uran(OMIN, OMAX)
         rb = max(a, b, cc)                    ! bounding-sphere radius
         x = uran(rb, LDOM - rb)
         y = uran(rb, LDOM - rb)
         z = uran(rb, LDOM - rb)

         ! rejection based on bounding spheres (fast, conservative)
         ok = .true.
         do s = 1, cnt
            dx = x - cx(s); dy = y - cy(s); dz = z - cz(s)
            d2 = dx*dx + dy*dy + dz*dz
            dallow = rb + rbnd(s) - min(o, ovl(s))
            if (dallow < 0.0_wp) dallow = 0.0_wp
            if (d2 < dallow*dallow) then
               ok = .false.; exit
            end if
         end do

         if (ok) then
            cnt = cnt + 1
            call random_euler(phi, theta, psi)
            cx(cnt)=x; cy(cnt)=y; cz(cnt)=z
            sa(cnt)=a; sb(cnt)=b; sc(cnt)=cc
            ep(cnt)=phi; et(cnt)=theta; es(cnt)=psi
            rbnd(cnt)=rb; ovl(cnt)=o
            vsolid = vsolid + (4.0_wp/3.0_wp)*PI*a*b*cc   ! ellipsoid volume
         end if
      end do

      write(*,'(A,I0,A,I0,A)') '  placed ', cnt, ' ellipsoids in ', tries, ' attempts'
      write(*,'(A,F7.4)') '  requested porosity                 = ', TARGET_POROSITY

      call voxelize(cnt, cx, cy, cz, sa, sb, sc, ep, et, es, h, grid)
      call average_grid(grid, ncg, cgrid)

      write(*,'(A,F7.4)') '  achieved porosity (void fraction)  = ', porosity(grid)
      write(*,'(A,I0,A,I0)') '  fine grid = ', NG, '^3 , coarse grid = ', ncg

      call write_vtk('ell_method2_geometry.vtk', NG, NG, NG, h, grid)
      open(newunit=u, file='ell_method2_ellipsoids.dat', status='replace', action='write')
      write(u,'(A)') '#     x           y           z           a           b           c          phi        theta        psi'
      do s = 1, cnt
         write(u,'(9(1x,F11.6))') cx(s),cy(s),cz(s), sa(s),sb(s),sc(s), ep(s),et(s),es(s)
      end do
      close(u)

      call cpu_time(t1)
      write(*,'(A,F8.3,A)') '  cpu time = ', t1 - t0, ' s'
      write(*,'(A)') '  wrote ell_method2_geometry.vtk , ell_method2_ellipsoids.dat'
      deallocate(cx,cy,cz,sa,sb,sc,ep,et,es,rbnd,ovl,cgrid)
   end subroutine run_method2
end module ell_method2
!==============================================================================


program ellipsoid_geometry
   use ell_utils,   only : seed_rng
   use ell_method1, only : run_method1
   use ell_method2, only : run_method2
   implicit none

   call seed_rng(12345)          ! fixed seed -> reproducible; <=0 for random

   call run_method1()
   call run_method2()

   write(*,'(/,A)') 'Done. Open the .vtk files in ParaView/VisIt to view the 3-D geometry.'
end program ellipsoid_geometry
!==============================================================================
