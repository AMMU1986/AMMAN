!==============================================================================
!  porous_geometry.f90
!
!  Generation of 3-D random packed-sphere porous geometries, implementing the
!  two algorithms shown in the "Geometry creation algorithm" flowcharts:
!
!    Method 1 : Constant sphere size
!               - randomly place N non-overlapping spheres of a fixed radius
!               - voxelize on a regular grid  (inside sphere = 0 = solid,
!                                               outside      = 1 = pore/void)
!               - coarse-grain ("grid averaging by some factor")
!
!    Method 2 : Specified porosity + variable sphere size
!               - randomly generate spheres with variable radius r in [rmin,rmax]
!                 and an allowed overlap o in [omin,omax]
!               - keep adding spheres (rejecting those that violate the
!                 minimum centre distance  d_ij >= r_i + r_j - o) until the
!                 solid volume fraction reaches the required value
!                 (i.e. the target porosity is met)
!               - voxelize + coarse-grain
!
!  Output for each method:
!     *.vtk      legacy VTK STRUCTURED_POINTS scalar field  (0 = solid sphere,
!                1 = pore) -> open in ParaView / VisIt for the 3-D view
!     *.dat      list of sphere centres and radii             (x y z r)
!     printed    achieved porosity, sphere count, timing
!
!  Build :   gfortran -O2 -o porous_geometry porous_geometry.f90
!  Run   :   ./porous_geometry
!
!==============================================================================
module geom_params
   implicit none
   integer,  parameter :: wp = selected_real_kind(15, 307)   ! double precision

   !--- Physical domain (a cube, axes 0..LDOM as in the reference figure) -----
   real(wp), parameter :: LDOM = 25.0_wp        ! domain edge length

   !--- Grid ------------------------------------------------------------------
   integer,  parameter :: NG   = 150            ! fine grid points per side
   integer,  parameter :: AVGF = 3              ! grid-averaging factor
                                                ! (NG must be divisible by AVGF)

   !--- Method 1 (constant radius) --------------------------------------------
   integer,  parameter :: NSPH1 = 250           ! number of spheres to place
   real(wp), parameter :: RAD1  = 1.6_wp        ! constant sphere radius
   integer,  parameter :: MAXTRY1 = 500000      ! attempts before giving up

   !--- Method 2 (variable radius, target porosity) ---------------------------
   real(wp), parameter :: RMIN = 0.8_wp         ! min sphere (pore) radius
   real(wp), parameter :: RMAX = 2.6_wp         ! max sphere (pore) radius
   real(wp), parameter :: OMIN = 0.0_wp         ! min allowed overlap
   real(wp), parameter :: OMAX = 1.2_wp         ! max allowed overlap
   real(wp), parameter :: TARGET_POROSITY = 0.55_wp  ! desired void fraction
   integer,  parameter :: MAXTRY2 = 5000000     ! attempts before giving up
   integer,  parameter :: MAXSPH2 = 20000       ! storage cap for spheres
end module geom_params
!==============================================================================


!------------------------------------------------------------------------------
! Small utility module: RNG helpers and VTK writer.
!------------------------------------------------------------------------------
module geom_utils
   use geom_params
   implicit none
contains

   !--- uniform random real in [a,b] ----------------------------------------
   function uran(a, b) result(x)
      real(wp), intent(in) :: a, b
      real(wp)             :: x, u
      call random_number(u)
      x = a + (b - a)*u
   end function uran

   !--- seed the RNG (reproducible if seed_val > 0, random otherwise) --------
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

   !--- write a legacy VTK STRUCTURED_POINTS scalar volume -------------------
   subroutine write_vtk(fname, nx, ny, nz, h, vol)
      character(len=*), intent(in) :: fname
      integer,          intent(in) :: nx, ny, nz
      real(wp),         intent(in) :: h                 ! cell spacing
      real(wp),         intent(in) :: vol(nx, ny, nz)   ! scalar field
      integer :: u, i, j, k
      open(newunit=u, file=fname, status='replace', action='write')
      write(u,'(A)') '# vtk DataFile Version 3.0'
      write(u,'(A)') 'random packed-sphere porous geometry'
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

end module geom_utils
!==============================================================================


!------------------------------------------------------------------------------
! Core voxelization + averaging (shared by both methods).
!------------------------------------------------------------------------------
module geom_voxel
   use geom_params
   implicit none
contains

   !----------------------------------------------------------------------
   ! Voxelize a set of spheres onto the fine NGxNGxNG grid.
   !   grid value = 0.0  -> point lies inside a sphere (solid)
   !   grid value = 1.0  -> point lies in the pore space (void)
   !
   ! Only grid points inside the local bounding box of each sphere are
   ! visited ("localized volume around the selected sphere").
   !----------------------------------------------------------------------
   subroutine voxelize(nsph, cx, cy, cz, rad, h, grid)
      integer,  intent(in)  :: nsph
      real(wp), intent(in)  :: cx(nsph), cy(nsph), cz(nsph), rad(nsph)
      real(wp), intent(in)  :: h
      real(wp), intent(out) :: grid(NG, NG, NG)
      integer  :: s, i, j, k, i0, i1, j0, j1, k0, k1
      real(wp) :: gx, gy, gz, r2, dx, dy, dz

      grid = 1.0_wp                       ! start as all pore

      do s = 1, nsph
         r2 = rad(s)*rad(s)
         ! local bounding box (grid index range) around this sphere
         i0 = max(1 , int((cx(s) - rad(s))/h) + 1)
         i1 = min(NG, int((cx(s) + rad(s))/h) + 1)
         j0 = max(1 , int((cy(s) - rad(s))/h) + 1)
         j1 = min(NG, int((cy(s) + rad(s))/h) + 1)
         k0 = max(1 , int((cz(s) - rad(s))/h) + 1)
         k1 = min(NG, int((cz(s) + rad(s))/h) + 1)
         do k = k0, k1
            gz = (real(k,wp) - 0.5_wp)*h
            dz = gz - cz(s)
            do j = j0, j1
               gy = (real(j,wp) - 0.5_wp)*h
               dy = gy - cy(s)
               do i = i0, i1
                  gx = (real(i,wp) - 0.5_wp)*h
                  dx = gx - cx(s)
                  if (dx*dx + dy*dy + dz*dz <= r2) grid(i,j,k) = 0.0_wp
               end do
            end do
         end do
      end do
   end subroutine voxelize

   !----------------------------------------------------------------------
   ! "Grid averaging by some factor": block-average the fine grid by AVGF
   ! into a coarse grid holding the local solid/pore volume fraction.
   !----------------------------------------------------------------------
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

   !--- porosity = fraction of pore (value 1) voxels on the fine grid -------
   function porosity(grid) result(phi)
      real(wp), intent(in) :: grid(NG, NG, NG)
      real(wp) :: phi
      phi = sum(grid) / real(NG*NG*NG, wp)
   end function porosity

end module geom_voxel
!==============================================================================


!------------------------------------------------------------------------------
! Method 1 : constant sphere size (non-overlapping random packing).
!------------------------------------------------------------------------------
module method1
   use geom_params
   use geom_utils
   use geom_voxel
   implicit none
contains
   subroutine run_method1()
      real(wp) :: cx(NSPH1), cy(NSPH1), cz(NSPH1), rad(NSPH1)
      real(wp) :: grid(NG, NG, NG)
      real(wp), allocatable :: cgrid(:,:,:)
      real(wp) :: h, x, y, z, dmin, dx, dy, dz, d2, t0, t1
      integer  :: count, tries, s, ncg, u
      logical  :: ok

      write(*,'(/,A)') '============================================================'
      write(*,'(A)')   '  METHOD 1 : constant sphere size'
      write(*,'(A)')   '============================================================'

      call cpu_time(t0)
      h     = LDOM / real(NG, wp)
      dmin  = 2.0_wp*RAD1               ! non-overlap: centres >= 2R apart
      count = 0
      tries = 0

      ! --- random sequential placement with distance rejection (array C) ----
      do while (count < NSPH1 .and. tries < MAXTRY1)
         tries = tries + 1
         ! keep centres at least one radius inside the box
         x = uran(RAD1, LDOM - RAD1)
         y = uran(RAD1, LDOM - RAD1)
         z = uran(RAD1, LDOM - RAD1)
         ok = .true.
         do s = 1, count
            dx = x - cx(s);  dy = y - cy(s);  dz = z - cz(s)
            d2 = dx*dx + dy*dy + dz*dz
            if (d2 < dmin*dmin) then       ! too close -> reject
               ok = .false.
               exit
            end if
         end do
         if (ok) then
            count      = count + 1
            cx(count)  = x
            cy(count)  = y
            cz(count)  = z
            rad(count) = RAD1
         end if
      end do

      write(*,'(A,I0,A,I0,A)') '  placed ', count, ' spheres in ', tries, ' attempts'
      if (count < NSPH1) write(*,'(A)') &
         '  (packing limit reached before target count - lower NSPH1 or RAD1)'

      ! --- voxelize + average ------------------------------------------------
      call voxelize(count, cx, cy, cz, rad, h, grid)
      call average_grid(grid, ncg, cgrid)

      write(*,'(A,F7.4)') '  achieved porosity (void fraction) = ', porosity(grid)
      write(*,'(A,I0,A,I0)') '  fine grid = ', NG, '^3 , coarse grid = ', ncg

      ! --- output ------------------------------------------------------------
      call write_vtk('method1_geometry.vtk', NG, NG, NG, h, grid)
      open(newunit=u, file='method1_spheres.dat', status='replace', action='write')
      write(u,'(A)') '#        x            y            z            r'
      do s = 1, count
         write(u,'(4(1x,F12.6))') cx(s), cy(s), cz(s), rad(s)
      end do
      close(u)

      call cpu_time(t1)
      write(*,'(A,F8.3,A)') '  wall/cpu time = ', t1 - t0, ' s'
      write(*,'(A)') '  wrote method1_geometry.vtk , method1_spheres.dat'
      deallocate(cgrid)
   end subroutine run_method1
end module method1
!==============================================================================


!------------------------------------------------------------------------------
! Method 2 : variable sphere size, driven to a target porosity.
!------------------------------------------------------------------------------
module method2
   use geom_params
   use geom_utils
   use geom_voxel
   implicit none
contains
   subroutine run_method2()
      real(wp), allocatable :: cx(:), cy(:), cz(:), rad(:), ovl(:)
      real(wp) :: grid(NG, NG, NG)
      real(wp), allocatable :: cgrid(:,:,:)
      real(wp) :: h, x, y, z, r, o, dx, dy, dz, d2, dallow
      real(wp) :: vbox, vsolid, vtarget, t0, t1
      integer  :: count, tries, s, ncg, u
      logical  :: ok

      write(*,'(/,A)') '============================================================'
      write(*,'(A)')   '  METHOD 2 : variable sphere size + specified porosity'
      write(*,'(A)')   '============================================================'

      call cpu_time(t0)
      h       = LDOM / real(NG, wp)
      vbox    = LDOM**3
      vtarget = (1.0_wp - TARGET_POROSITY) * vbox   ! required SOLID volume
      count   = 0
      tries   = 0
      vsolid  = 0.0_wp

      allocate(cx(MAXSPH2), cy(MAXSPH2), cz(MAXSPH2), rad(MAXSPH2), ovl(MAXSPH2))

      ! --- add spheres until solid volume reaches the required volume --------
      do while (vsolid < vtarget .and. tries < MAXTRY2 .and. count < MAXSPH2)
         tries = tries + 1
         r = uran(RMIN, RMAX)
         o = uran(OMIN, OMAX)
         x = uran(r, LDOM - r)
         y = uran(r, LDOM - r)
         z = uran(r, LDOM - r)

         ! distance check against stored spheres using their own r and o
         ok = .true.
         do s = 1, count
            dx = x - cx(s);  dy = y - cy(s);  dz = z - cz(s)
            d2 = dx*dx + dy*dy + dz*dz
            ! allowed centre distance = r_i + r_j - overlap(min of the two)
            dallow = r + rad(s) - min(o, ovl(s))
            if (dallow < 0.0_wp) dallow = 0.0_wp
            if (d2 < dallow*dallow) then
               ok = .false.
               exit
            end if
         end do

         if (ok) then
            count      = count + 1
            cx(count)  = x
            cy(count)  = y
            cz(count)  = z
            rad(count) = r
            ovl(count) = o
            ! running estimate of solid volume (analytic sphere volume;
            ! true voxel volume is reported after voxelization below)
            vsolid = vsolid + (4.0_wp/3.0_wp)*acos(-1.0_wp)*r**3
         end if
      end do

      write(*,'(A,I0,A,I0,A)') '  placed ', count, ' spheres in ', tries, ' attempts'
      write(*,'(A,F7.4)') '  requested porosity                 = ', TARGET_POROSITY

      ! --- voxelize + average ------------------------------------------------
      call voxelize(count, cx, cy, cz, rad, h, grid)
      call average_grid(grid, ncg, cgrid)

      write(*,'(A,F7.4)') '  achieved porosity (void fraction)  = ', porosity(grid)
      write(*,'(A,I0,A,I0)') '  fine grid = ', NG, '^3 , coarse grid = ', ncg

      ! --- output ------------------------------------------------------------
      call write_vtk('method2_geometry.vtk', NG, NG, NG, h, grid)
      open(newunit=u, file='method2_spheres.dat', status='replace', action='write')
      write(u,'(A)') '#        x            y            z            r            overlap'
      do s = 1, count
         write(u,'(5(1x,F12.6))') cx(s), cy(s), cz(s), rad(s), ovl(s)
      end do
      close(u)

      call cpu_time(t1)
      write(*,'(A,F8.3,A)') '  wall/cpu time = ', t1 - t0, ' s'
      write(*,'(A)') '  wrote method2_geometry.vtk , method2_spheres.dat'
      deallocate(cx, cy, cz, rad, ovl, cgrid)
   end subroutine run_method2
end module method2
!==============================================================================


!------------------------------------------------------------------------------
! Main program.
!------------------------------------------------------------------------------
program porous_geometry
   use geom_utils, only : seed_rng
   use method1,    only : run_method1
   use method2,    only : run_method2
   implicit none

   call seed_rng(12345)          ! fixed seed -> reproducible; use <=0 for random

   call run_method1()
   call run_method2()

   write(*,'(/,A)') 'Done. Open the .vtk files in ParaView/VisIt to view the 3-D geometry.'
end program porous_geometry
!==============================================================================
