!==============================================================================
!  pcm_geometry_all.f90
!
!  Generates ALL EIGHT capsule arrangements of Fig. 14 of
!
!    V. Athawale, A. Bhattacharya, P. Rath,
!    "Prediction of melting characteristics of encapsulated phase change
!     material energy storage systems",
!    Int. J. Heat and Mass Transfer 181 (2021) 121872.
!
!      (a) straight   3x3      (e) alternate  3x3
!      (b) straight   4x4      (f) alternate  4x4
!      (c) straight   5x5      (g) alternate  5x5
!      (d) straight   6x6      (h) alternate  6x6
!
!  The total PCM volume (area, in 2-D) is kept constant across all cases:
!  a 6x6 array uses r = 3 mm, so for an n x n array
!
!          N * pi * r_n^2 = const   =>   r_n = r_ref * (n_ref / n)
!
!  giving r = 6.0, 4.5, 3.6, 3.0 mm for n = 3,4,5,6 (cf. Table 3).
!
!  For every arrangement the PCM volume fraction phi is built on the coarse
!  finite-volume mesh with the fine -> coarse mapping technique of Section 2.1
!  (phi = 1 inside a capsule, 0 in the HTF, 0<phi<1 at the interface).
!
!  Output: eight data files  geom_a.dat ... geom_h.dat  (columns: x  y  phi),
!  all on the same 8 cm x 8 cm domain and 200 x 200 mesh, plus a screen summary.
!
!  Build : gfortran -O2 -o pcm_geometry_all pcm_geometry_all.f90
!  Run   : ./pcm_geometry_all
!==============================================================================
program pcm_geometry_all
   implicit none
   integer, parameter :: dp = selected_real_kind(15, 307)

   !--------------------------------------------------------------------------
   !  Fixed problem parameters (common to all 8 arrangements)
   !--------------------------------------------------------------------------
   real(dp), parameter :: Lx     = 0.08_dp    ! domain length in x [m] (8 cm)
   real(dp), parameter :: Ly     = 0.08_dp    ! domain length in y [m] (8 cm)
   integer,  parameter :: n_ref  = 6          ! reference array size
   real(dp), parameter :: r_ref  = 0.003_dp   ! reference radius at 6x6 [m] (3 mm)
   integer,  parameter :: ncx    = 200        ! coarse cells in x (0.40 mm)
   integer,  parameter :: ncy    = 200        ! coarse cells in y (0.40 mm)
   integer,  parameter :: refine = 8          ! fine samples per cell per dir
   real(dp), parameter :: pi     = 3.141592653589793_dp

   ! The eight cases: n = 3,4,5,6 straight, then 3,4,5,6 alternate
   integer,  parameter :: ncase = 8
   integer,          dimension(ncase) :: narr    = (/3,4,5,6,3,4,5,6/)
   logical,          dimension(ncase) :: stag    = (/.false.,.false.,.false.,.false., &
                                                      .true. ,.true. ,.true. ,.true./)
   character(len=1), dimension(ncase) :: tag     = (/'a','b','c','d','e','f','g','h'/)

   real(dp), allocatable :: phi(:,:), xc(:), yc(:)
   real(dp), allocatable :: capx(:), capy(:), capr(:)
   real(dp) :: dxc, dyc, cell_area, rN, pcm_area, phi_area
   integer  :: i, j, ic, n, ncap
   character(len=32) :: fname

   allocate(phi(ncx,ncy), xc(ncx), yc(ncy))
   dxc = Lx / real(ncx, dp)
   dyc = Ly / real(ncy, dp)
   cell_area = dxc * dyc
   do i = 1, ncx
      xc(i) = (real(i, dp) - 0.5_dp) * dxc
   end do
   do j = 1, ncy
      yc(j) = (real(j, dp) - 0.5_dp) * dyc
   end do

   write(*,'(a)') '================================================================='
   write(*,'(a)') ' Encapsulated-PCM geometry: all 8 arrangements (Fig. 14)'
   write(*,'(a)') ' Domain 8 cm x 8 cm,  mesh 200 x 200 (0.40 mm),  const. PCM vol.'
   write(*,'(a)') '================================================================='
   write(*,'(a)') ' case  arrangement   n x n   radius(mm)   PCM area(cm^2)   map err%'
   write(*,'(a)') '-----------------------------------------------------------------'

   do ic = 1, ncase
      n    = narr(ic)
      ncap = n * n
      rN   = r_ref * real(n_ref, dp) / real(n, dp)   ! constant-volume radius

      allocate(capx(ncap), capy(ncap), capr(ncap))
      call build_capsules(capx, capy, capr, n, Lx, Ly, rN, stag(ic))
      call map_phi(phi, xc, yc, dxc, dyc, ncx, ncy, refine, capx, capy, capr, ncap)

      pcm_area = real(ncap, dp) * pi * rN*rN
      phi_area = sum(phi) * cell_area

      write(fname,'(a,a,a)') 'geom_', tag(ic), '.dat'
      call write_phi_field(trim(fname), phi, xc, yc, ncx, ncy)

      write(*,'(3x,a1,4x,a,4x,i1,a,i1,6x,f5.2,7x,f8.4,8x,f6.3)') &
           tag(ic), merge('ALTERNATE','STRAIGHT ', stag(ic)), n, 'x', n, &
           rN*1000.0_dp, phi_area*1.0e4_dp, &
           100.0_dp*abs(phi_area-pcm_area)/pcm_area

      deallocate(capx, capy, capr)
   end do

   write(*,'(a)') '-----------------------------------------------------------------'
   write(*,'(a)') ' Wrote geom_a.dat ... geom_h.dat'

   deallocate(phi, xc, yc)

contains

   !---------------------------------------------------------------------------
   !  Build an n x n capsule array of radius rN centred in the domain.
   !  For the alternate arrangement every second COLUMN (along the flow/x
   !  direction) is shifted in y by half the vertical spacing (zig-zag).
   !---------------------------------------------------------------------------
   subroutine build_capsules(cx, cy, cr, n, Lx, Ly, rN, stagger)
      real(dp), intent(out) :: cx(:), cy(:), cr(:)
      integer,  intent(in)  :: n
      real(dp), intent(in)  :: Lx, Ly, rN
      logical,  intent(in)  :: stagger
      real(dp) :: sx, sy, yshift
      integer  :: ix, iy, k

      sx = Lx / real(n, dp)          ! centre-to-centre spacing (with wall margin)
      sy = Ly / real(n, dp)
      yshift = 0.5_dp * sy

      k = 0
      do ix = 1, n                    ! columns (x = flow direction)
         do iy = 1, n                  ! rows (y)
            k = k + 1
            cx(k) = (real(ix, dp) - 0.5_dp) * sx
            cy(k) = (real(iy, dp) - 0.5_dp) * sy
            cr(k) = rN
            if (stagger .and. mod(ix,2) == 0) then
               cy(k) = cy(k) + yshift    ! shift even columns up by half spacing
            end if
         end do
      end do
   end subroutine build_capsules

   !---------------------------------------------------------------------------
   !  Fine/coarse mapping of the PCM volume fraction phi.
   !---------------------------------------------------------------------------
   subroutine map_phi(phi, xc, yc, dx, dy, nx, ny, ref, cx, cy, cr, ncap)
      real(dp), intent(out) :: phi(:,:)
      real(dp), intent(in)  :: xc(:), yc(:), dx, dy, cx(:), cy(:), cr(:)
      integer,  intent(in)  :: nx, ny, ref, ncap
      integer  :: i, j, p, q, kc, inside
      real(dp) :: x0, y0, fx, fy, xf, yf, dxf, dyf

      dxf = dx / real(ref, dp)
      dyf = dy / real(ref, dp)
      do j = 1, ny
         do i = 1, nx
            x0 = xc(i) - 0.5_dp*dx
            y0 = yc(j) - 0.5_dp*dy
            inside = 0
            do q = 1, ref
               yf = y0 + (real(q, dp) - 0.5_dp) * dyf
               do p = 1, ref
                  xf = x0 + (real(p, dp) - 0.5_dp) * dxf
                  do kc = 1, ncap
                     fx = xf - cx(kc)
                     fy = yf - cy(kc)
                     if (fx*fx + fy*fy <= cr(kc)*cr(kc)) then
                        inside = inside + 1
                        exit
                     end if
                  end do
               end do
            end do
            phi(i,j) = real(inside, dp) / real(ref*ref, dp)
         end do
      end do
   end subroutine map_phi

   !---------------------------------------------------------------------------
   !  Write phi(x,y) as a 3-column gnuplot-style ascii file.
   !---------------------------------------------------------------------------
   subroutine write_phi_field(path, phi, xc, yc, nx, ny)
      character(len=*), intent(in) :: path
      real(dp), intent(in) :: phi(:,:), xc(:), yc(:)
      integer,  intent(in) :: nx, ny
      integer :: i, j, u
      open(newunit=u, file=path, status='replace', action='write')
      write(u,'(a)') '# x            y            phi'
      do i = 1, nx
         do j = 1, ny
            write(u,'(3es15.6)') xc(i), yc(j), phi(i,j)
         end do
         write(u,*)
      end do
      close(u)
   end subroutine write_phi_field

end program pcm_geometry_all
