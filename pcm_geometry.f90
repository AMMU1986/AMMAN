!==============================================================================
!  pcm_geometry.f90
!
!  Generation of the encapsulated-PCM geometry shown in Fig. 1 of
!
!    V. Athawale, A. Bhattacharya, P. Rath,
!    "Prediction of melting characteristics of encapsulated phase change
!     material energy storage systems",
!    Int. J. Heat and Mass Transfer 181 (2021) 121872.
!
!  A square domain contains a structured array of circular PCM capsules.
!  Following Section 2.1 ("Geometry model") of the paper, a PCM volume
!  fraction phi is defined for every control volume of the (coarse) finite
!  volume mesh:
!
!        phi = 1  -> control volume lies completely inside a capsule (PCM)
!        phi = 0  -> control volume lies completely in the HTF region
!        0<phi<1  -> control volume straddles a capsule interface
!
!  phi is obtained with the fine-grid / coarse-grid mapping technique
!  described in the paper: the domain is first covered by a very fine grid
!  of sample points, each flagged 0/1 (outside/inside a capsule); phi for
!  each coarse control volume is then the average of the fine sample points
!  falling inside it.
!
!  The program supports:
!     * straight (aligned) or alternate (staggered) capsule arrangements
!     * an optional per-row percentage reduction of capsule radius along the
!       flow (x) direction, with the first-row radius rescaled so that the
!       total PCM area (volume, in 2-D) is preserved (the "graded" design of
!       Section 3.5).
!
!  Outputs
!     phi_field.dat        phi on the coarse mesh  (x  y  phi)  [gnuplot/tecplot]
!     capsules.dat         capsule centres and radii (xc yc r)
!     screen               a compact ASCII map + summary
!
!  Build : gfortran -O2 -o pcm_geometry pcm_geometry.f90
!  Run   : ./pcm_geometry
!==============================================================================
program pcm_geometry
   implicit none
   integer, parameter :: dp = selected_real_kind(15, 307)

   !--------------------------------------------------------------------------
   !  User-configurable problem parameters
   !--------------------------------------------------------------------------
   real(dp), parameter :: Lx      = 0.08_dp   ! domain length in x  [m]
   real(dp), parameter :: Ly      = 0.08_dp   ! domain length in y  [m]
   integer,  parameter :: ncap_x  = 6         ! number of capsule columns
   integer,  parameter :: ncap_y  = 6         ! number of capsule rows
   real(dp), parameter :: r_base  = 0.003_dp  ! base capsule radius [m] (3 mm)

   ! Coarse finite-volume mesh (control volumes) -> paper uses 0.40 mm spacing
   integer,  parameter :: ncx     = 200       ! coarse cells in x
   integer,  parameter :: ncy     = 200       ! coarse cells in y

   ! Fine sampling grid used only for the phi mapping (much finer than coarse)
   integer,  parameter :: refine  = 8         ! fine points per coarse cell / dir

   ! Arrangement: .false. = straight,  .true. = alternate (staggered) rows
   logical,  parameter :: alternate = .false.

   ! Graded design: percentage radius reduction from one column to the next
   ! along the flow (x) direction.  0.0 reproduces the equal-size Fig. 1 layout.
   real(dp), parameter :: pct_reduction = 0.0_dp   ! e.g. 12.0_dp for optimum
   !--------------------------------------------------------------------------

   real(dp), allocatable :: phi(:,:)          ! PCM volume fraction on coarse mesh
   real(dp), allocatable :: xc(:), yc(:)      ! coarse cell-centre coordinates
   real(dp), allocatable :: capx(:), capy(:), capr(:)   ! capsule geometry
   integer  :: ncap
   real(dp) :: dxc, dyc, cell_area
   real(dp) :: pcm_area, phi_area
   integer  :: i, j

   ncap = ncap_x * ncap_y
   allocate(phi(ncx,ncy), xc(ncx), yc(ncy))
   allocate(capx(ncap), capy(ncap), capr(ncap))

   dxc = Lx / real(ncx, dp)
   dyc = Ly / real(ncy, dp)
   cell_area = dxc * dyc

   ! Coarse cell-centre coordinates
   do i = 1, ncx
      xc(i) = (real(i, dp) - 0.5_dp) * dxc
   end do
   do j = 1, ncy
      yc(j) = (real(j, dp) - 0.5_dp) * dyc
   end do

   !--------------------------------------------------------------------------
   !  1. Build the capsule array (centres + radii)
   !--------------------------------------------------------------------------
   call build_capsules(capx, capy, capr, ncap_x, ncap_y, &
                        Lx, Ly, r_base, alternate, pct_reduction, pcm_area)

   !--------------------------------------------------------------------------
   !  2. Map capsule geometry onto phi using the fine/coarse technique
   !--------------------------------------------------------------------------
   call map_phi(phi, xc, yc, dxc, dyc, ncx, ncy, refine, &
                capx, capy, capr, ncap)

   !--------------------------------------------------------------------------
   !  3. Report + write output files
   !--------------------------------------------------------------------------
   phi_area = sum(phi) * cell_area          ! PCM area recovered from phi field

   write(*,'(a)')        '======================================================'
   write(*,'(a)')        ' Encapsulated PCM geometry generator (Athawale 2021)'
   write(*,'(a)')        '======================================================'
   write(*,'(a,f8.4,a,f8.4,a)') ' Domain (Lx x Ly)     : ', Lx, ' x ', Ly, ' m'
   write(*,'(a,i0,a,i0)')       ' Coarse mesh (ncx x ncy): ', ncx, ' x ', ncy
   write(*,'(a,f8.5,a,f8.5,a)') ' Cell size (dx x dy)  : ', dxc, ' x ', dyc, ' m'
   write(*,'(a,i0,a,i0,a,i0)')  ' Capsule array        : ', ncap_x, ' x ', &
                                 ncap_y, '  (total ', ncap, ')'
   write(*,'(a,f8.5,a)')        ' Base capsule radius  : ', r_base, ' m'
   if (alternate) then
      write(*,'(a)')            ' Arrangement          : ALTERNATE (staggered)'
   else
      write(*,'(a)')            ' Arrangement          : STRAIGHT (aligned)'
   end if
   write(*,'(a,f6.2,a)')        ' Per-row size grading : ', pct_reduction, ' %'
   write(*,'(a)')        '------------------------------------------------------'
   write(*,'(a,es13.6,a)') ' Target PCM area (exact circles) : ', pcm_area, ' m^2'
   write(*,'(a,es13.6,a)') ' PCM area from phi field         : ', phi_area, ' m^2'
   write(*,'(a,f7.3,a)')   ' Mapping error                   : ', &
                             100.0_dp*abs(phi_area-pcm_area)/pcm_area, ' %'
   write(*,'(a,f7.3,a)')   ' PCM volume (area) fraction      : ', &
                             100.0_dp*phi_area/(Lx*Ly), ' %'
   write(*,'(a)')        '======================================================'

   call write_phi_field(phi, xc, yc, ncx, ncy)
   call write_capsules(capx, capy, capr, ncap)
   call ascii_map(phi, ncx, ncy)

   write(*,'(a)') ' Wrote: phi_field.dat, capsules.dat'

   deallocate(phi, xc, yc, capx, capy, capr)

contains

   !---------------------------------------------------------------------------
   !  Build capsule centres and radii for a structured ncap_x by ncap_y array.
   !
   !  Columns are indexed along the flow (x) direction.  For the graded design
   !  every column's radius is reduced by pct_reduction % relative to the
   !  previous column; the first-column radius is then rescaled so that the
   !  total PCM area equals that of an equal-size array of radius r_base.
   !---------------------------------------------------------------------------
   subroutine build_capsules(cx, cy, cr, nx, ny, Lx, Ly, rbase, &
                             stagger, pct, total_area)
      real(dp), intent(out) :: cx(:), cy(:), cr(:)
      integer,  intent(in)  :: nx, ny
      real(dp), intent(in)  :: Lx, Ly, rbase, pct
      logical,  intent(in)  :: stagger
      real(dp), intent(out) :: total_area

      real(dp) :: sx, sy          ! centre-to-centre spacing in x and y
      real(dp) :: factor, sumfac2, r1, rj, yshift
      real(dp), parameter :: pi = 3.141592653589793_dp
      integer  :: ix, iy, k

      ! Uniform spacing with a half-cell margin from the walls
      sx = Lx / real(nx, dp)
      sy = Ly / real(ny, dp)

      factor = 1.0_dp - pct/100.0_dp     ! geometric reduction ratio per column

      ! Determine first-column radius r1 that preserves total PCM area.
      ! Column j radius = r1 * factor**(j-1).  Every row in a column shares it.
      ! Total area = ny * pi * r1^2 * sum_j factor**(2(j-1))  (must equal
      !              nx*ny*pi*rbase^2).
      sumfac2 = 0.0_dp
      do ix = 1, nx
         sumfac2 = sumfac2 + factor**(2*(ix-1))
      end do
      r1 = rbase * sqrt( real(nx, dp) / sumfac2 )

      k = 0
      total_area = 0.0_dp
      do ix = 1, nx                       ! columns (x, flow direction)
         rj = r1 * factor**(ix-1)
         do iy = 1, ny                     ! rows (y)
            k = k + 1
            cx(k) = (real(ix, dp) - 0.5_dp) * sx
            cy(k) = (real(iy, dp) - 0.5_dp) * sy
            cr(k) = rj
            total_area = total_area + pi * rj*rj
         end do
      end do

      ! Alternate (staggered) arrangement: shift every second column in y by
      ! half the vertical spacing to create the zig-zag pattern of the paper.
      if (stagger) then
         yshift = 0.5_dp * sy
         k = 0
         do ix = 1, nx
            do iy = 1, ny
               k = k + 1
               if (mod(ix,2) == 0) then
                  cy(k) = cy(k) + yshift
                  if (cy(k) > Ly - cr(k)) cy(k) = cy(k) - sy   ! keep inside
               end if
            end do
         end do
      end if
   end subroutine build_capsules

   !---------------------------------------------------------------------------
   !  Fine/coarse mapping of the PCM volume fraction phi.
   !
   !  Each coarse control volume is sub-sampled by refine x refine fine points.
   !  A fine point is flagged 1 if it lies inside ANY capsule, else 0.
   !  phi of the coarse cell is the mean of its fine-point flags.
   !---------------------------------------------------------------------------
   subroutine map_phi(phi, xc, yc, dx, dy, nx, ny, ref, cx, cy, cr, ncap)
      real(dp), intent(out) :: phi(:,:)
      real(dp), intent(in)  :: xc(:), yc(:), dx, dy, cx(:), cy(:), cr(:)
      integer,  intent(in)  :: nx, ny, ref, ncap

      integer  :: i, j, p, q, kc, inside
      real(dp) :: x0, y0, fx, fy, xf, yf
      real(dp) :: dxf, dyf
      real(dp) :: cr2

      dxf = dx / real(ref, dp)
      dyf = dy / real(ref, dp)

      do j = 1, ny
         do i = 1, nx
            x0 = xc(i) - 0.5_dp*dx        ! lower-left corner of the coarse cell
            y0 = yc(j) - 0.5_dp*dy
            inside = 0
            do q = 1, ref
               yf = y0 + (real(q, dp) - 0.5_dp) * dyf
               do p = 1, ref
                  xf = x0 + (real(p, dp) - 0.5_dp) * dxf
                  ! Is (xf,yf) inside any capsule?
                  do kc = 1, ncap
                     fx = xf - cx(kc)
                     fy = yf - cy(kc)
                     cr2 = cr(kc)*cr(kc)
                     if (fx*fx + fy*fy <= cr2) then
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
   !  Write phi(x,y) as a 3-column ascii file (blank line between x-scans so
   !  gnuplot "splot 'phi_field.dat' with pm3d" renders it directly).
   !---------------------------------------------------------------------------
   subroutine write_phi_field(phi, xc, yc, nx, ny)
      real(dp), intent(in) :: phi(:,:), xc(:), yc(:)
      integer,  intent(in) :: nx, ny
      integer :: i, j, u
      open(newunit=u, file='phi_field.dat', status='replace', action='write')
      write(u,'(a)') '# x            y            phi'
      do i = 1, nx
         do j = 1, ny
            write(u,'(3es15.6)') xc(i), yc(j), phi(i,j)
         end do
         write(u,*)                      ! blank line -> new gnuplot scan line
      end do
      close(u)
   end subroutine write_phi_field

   !---------------------------------------------------------------------------
   !  Write the capsule centres and radii.
   !---------------------------------------------------------------------------
   subroutine write_capsules(cx, cy, cr, n)
      real(dp), intent(in) :: cx(:), cy(:), cr(:)
      integer,  intent(in) :: n
      integer :: k, u
      open(newunit=u, file='capsules.dat', status='replace', action='write')
      write(u,'(a)') '# xc            yc            r'
      do k = 1, n
         write(u,'(3es15.6)') cx(k), cy(k), cr(k)
      end do
      close(u)
   end subroutine write_capsules

   !---------------------------------------------------------------------------
   !  Compact ASCII visualisation of the phi field (down-sampled to ~60 cols).
   !---------------------------------------------------------------------------
   subroutine ascii_map(phi, nx, ny)
      real(dp), intent(in) :: phi(:,:)
      integer,  intent(in) :: nx, ny
      integer, parameter :: cols = 60, rows = 30
      integer :: i, j, ii, jj
      real(dp) :: v
      character(len=1) :: ch

      write(*,'(a)') ' PCM volume-fraction map (# = PCM, : = interface, blank = HTF)'
      write(*,'(a)') ' +' // repeat('-', cols) // '+'
      do jj = rows, 1, -1               ! top row first so y points up
         write(*,'(a)', advance='no') ' |'
         j = 1 + int( (real(jj,dp)-0.5_dp)/real(rows,dp) * real(ny,dp) )
         do ii = 1, cols
            i = 1 + int( (real(ii,dp)-0.5_dp)/real(cols,dp) * real(nx,dp) )
            v = phi(min(i,nx), min(j,ny))
            if (v > 0.75_dp) then
               ch = '#'
            else if (v > 0.05_dp) then
               ch = ':'
            else
               ch = ' '
            end if
            write(*,'(a)', advance='no') ch
         end do
         write(*,'(a)') '|'
      end do
      write(*,'(a)') ' +' // repeat('-', cols) // '+'
   end subroutine ascii_map

end program pcm_geometry
