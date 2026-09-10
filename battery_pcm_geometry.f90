!=======================================================================
!  battery_pcm_geometry.f90
!
!  Generates the geometry of a Phase-Change-Material (PCM) battery pack:
!    * A rectangular PCM block  (Lx x Ly x Lz)
!    * An N x N array of vertical cylindrical batteries (full height in Z)
!      embedded in the PCM  (reproduces the 4x4 / 92 x 92 x 65 mm layout).
!
!  The program can work in two modes:
!    MODE = 1 : radius of each cell is given  -> metal (battery) fraction
!               is COMPUTED.
!    MODE = 2 : a TARGET metal fraction is given -> the cell radius needed
!               to achieve it is SOLVED analytically.
!
!  Metal (battery) volume fraction:
!        phi = N_cells * pi * r^2 * Lz / (Lx * Ly * Lz)
!            = N_cells * pi * r^2      / (Lx * Ly)
!  (the Lz cancels because the cells span the full block height).
!
!  Outputs
!    * screen summary (dimensions, radius, pitch, fraction, volumes)
!    * battery_centres.dat : x,y coordinates of every cell centre
!    * battery_pcm.vtk      : STRUCTURED_POINTS voxel model
!                             (0 = PCM, 1 = battery) for ParaView / VisIt.
!
!  Build:  gfortran -O2 battery_pcm_geometry.f90 -o battery_pcm
!  Run  :  ./battery_pcm
!=======================================================================
program battery_pcm_geometry
   implicit none

   integer,  parameter :: dp = selected_real_kind(15,307)
   real(dp), parameter :: pi = 3.141592653589793_dp

   !------------------------------------------------------------------
   !  USER INPUT  (edit these to match your case)
   !------------------------------------------------------------------
   real(dp) :: Lx = 92.0_dp        ! block length in X  (mm)
   real(dp) :: Ly = 92.0_dp        ! block length in Y  (mm)
   real(dp) :: Lz = 65.0_dp        ! block height in Z  (mm)
   integer  :: nx = 4              ! number of cells along X
   integer  :: ny = 4              ! number of cells along Y

   integer  :: mode = 1            ! 1 = radius given, 2 = target fraction given
   real(dp) :: r_cell   = 9.0_dp   ! cell radius (mm)  -> used when mode = 1
   real(dp) :: phi_target = 0.45_dp! target metal fraction -> used when mode = 2

   ! voxel resolution for the VTK model
   integer  :: res = 120           ! voxels along the longest horizontal edge
   !------------------------------------------------------------------

   integer  :: ncells
   real(dp) :: phi, pitch_x, pitch_y
   real(dp) :: Vbatt, Vpcm, Vtot
   real(dp), allocatable :: xc(:), yc(:)

   ncells  = nx*ny
   pitch_x = Lx/real(nx,dp)        ! centre-to-centre spacing (uniform cells)
   pitch_y = Ly/real(ny,dp)

   !------------------------------------------------------------------
   !  Determine the cell radius / metal fraction
   !------------------------------------------------------------------
   if (mode == 2) then
      ! solve  phi = ncells*pi*r^2/(Lx*Ly)  for r
      r_cell = sqrt( phi_target*Lx*Ly/(real(ncells,dp)*pi) )
      phi    = phi_target
   else
      phi    = real(ncells,dp)*pi*r_cell**2/(Lx*Ly)
   end if

   ! geometric sanity check: cells must fit inside their pitch
   if (2.0_dp*r_cell > min(pitch_x,pitch_y)) then
      write(*,'(a)') 'WARNING: cells overlap (2*r > pitch). Reduce r or phi.'
   end if

   !------------------------------------------------------------------
   !  Volumes
   !------------------------------------------------------------------
   Vtot  = Lx*Ly*Lz
   Vbatt = real(ncells,dp)*pi*r_cell**2*Lz
   Vpcm  = Vtot - Vbatt

   !------------------------------------------------------------------
   !  Cell-centre coordinates (centred in each pitch cell)
   !------------------------------------------------------------------
   call build_centres(nx,ny,pitch_x,pitch_y,xc,yc)

   !------------------------------------------------------------------
   !  Report
   !------------------------------------------------------------------
   call report(Lx,Ly,Lz,nx,ny,ncells,r_cell,pitch_x,pitch_y, &
               phi,Vtot,Vbatt,Vpcm)

   call write_centres(xc,yc,ncells,r_cell,Lz)
   call write_vtk(Lx,Ly,Lz,res,xc,yc,r_cell,ncells)

   write(*,'(/,a)') 'Done.  Files written: battery_centres.dat, battery_pcm.vtk'

contains

   !--------------------------------------------------------------
   subroutine build_centres(nx,ny,px,py,xc,yc)
      integer,  intent(in)  :: nx, ny
      real(dp), intent(in)  :: px, py
      real(dp), allocatable, intent(out) :: xc(:), yc(:)
      integer :: i, j, k
      allocate(xc(nx*ny), yc(nx*ny))
      k = 0
      do j = 1, ny
         do i = 1, nx
            k = k + 1
            xc(k) = (real(i,dp)-0.5_dp)*px
            yc(k) = (real(j,dp)-0.5_dp)*py
         end do
      end do
   end subroutine build_centres

   !--------------------------------------------------------------
   subroutine report(Lx,Ly,Lz,nx,ny,nc,r,px,py,phi,Vt,Vb,Vp)
      real(dp), intent(in) :: Lx,Ly,Lz,r,px,py,phi,Vt,Vb,Vp
      integer,  intent(in) :: nx,ny,nc
      write(*,'(a)') '======================================================'
      write(*,'(a)') '   BATTERY / PCM PACK GEOMETRY'
      write(*,'(a)') '======================================================'
      write(*,'(a,3(f8.2),a)') ' Block (Lx,Ly,Lz)    : ',Lx,Ly,Lz,'  mm'
      write(*,'(a,i0,a,i0,a,i0)') ' Cell array          : ',nx,' x ',ny,' = ',nc
      write(*,'(a,f8.3,a)')  ' Cell radius   r     : ',r,'  mm'
      write(*,'(a,f8.3,a)')  ' Cell diameter 2r    : ',2.0_dp*r,'  mm'
      write(*,'(a,2(f8.3),a)') ' Pitch (px,py)       : ',px,py,'  mm'
      write(*,'(a,f8.4)')    ' Metal (battery) frac: ',phi
      write(*,'(a,f8.4)')    ' PCM fraction        : ',1.0_dp-phi
      write(*,'(a)') '------------------------------------------------------'
      write(*,'(a,es12.5,a)') ' Total volume        : ',Vt,'  mm^3'
      write(*,'(a,es12.5,a)') ' Battery volume      : ',Vb,'  mm^3'
      write(*,'(a,es12.5,a)') ' PCM volume          : ',Vp,'  mm^3'
      write(*,'(a)') '======================================================'
   end subroutine report

   !--------------------------------------------------------------
   subroutine write_centres(xc,yc,nc,r,Lz)
      real(dp), intent(in) :: xc(:), yc(:), r, Lz
      integer,  intent(in) :: nc
      integer :: u, k
      open(newunit=u, file='battery_centres.dat', status='replace', action='write')
      write(u,'(a)') '# id      xc(mm)      yc(mm)      r(mm)     z0(mm)    z1(mm)'
      do k = 1, nc
         write(u,'(i4,5(1x,f11.4))') k, xc(k), yc(k), r, 0.0_dp, Lz
      end do
      close(u)
   end subroutine write_centres

   !--------------------------------------------------------------
   !  Structured-points voxel model.  A voxel is tagged "battery" (1)
   !  if its centre lies inside any cylinder, otherwise "PCM" (0).
   !--------------------------------------------------------------
   subroutine write_vtk(Lx,Ly,Lz,res,xc,yc,r,nc)
      real(dp), intent(in) :: Lx,Ly,Lz,xc(:),yc(:),r
      integer,  intent(in) :: res, nc
      integer  :: nX, nY, nZ, i, j, k, m, u, tag
      real(dp) :: h, x, y, dx, dy, r2

      h  = max(Lx,Ly)/real(res,dp)      ! isotropic voxel size
      nX = max(1, nint(Lx/h))
      nY = max(1, nint(Ly/h))
      nZ = max(1, nint(Lz/h))
      r2 = r*r

      open(newunit=u, file='battery_pcm.vtk', status='replace', action='write')
      write(u,'(a)') '# vtk DataFile Version 3.0'
      write(u,'(a)') 'Battery-PCM pack (0=PCM, 1=battery)'
      write(u,'(a)') 'ASCII'
      write(u,'(a)') 'DATASET STRUCTURED_POINTS'
      write(u,'(a,3(1x,i0))')  'DIMENSIONS', nX, nY, nZ
      write(u,'(a,3(1x,f10.5))') 'ORIGIN', 0.5_dp*h, 0.5_dp*h, 0.5_dp*h
      write(u,'(a,3(1x,f10.5))') 'SPACING', h, h, h
      write(u,'(a,1x,i0)') 'POINT_DATA', nX*nY*nZ
      write(u,'(a)') 'SCALARS material int 1'
      write(u,'(a)') 'LOOKUP_TABLE default'

      do k = 1, nZ
         do j = 1, nY
            y = (real(j,dp)-0.5_dp)*h
            do i = 1, nX
               x = (real(i,dp)-0.5_dp)*h
               tag = 0
               do m = 1, nc
                  dx = x - xc(m)
                  dy = y - yc(m)
                  if (dx*dx + dy*dy <= r2) then
                     tag = 1
                     exit
                  end if
               end do
               write(u,'(i0)') tag
            end do
         end do
      end do
      close(u)
   end subroutine write_vtk

end program battery_pcm_geometry
