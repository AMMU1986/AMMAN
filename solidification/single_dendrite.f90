!==============================================================================
!  single_dendrite.f90
!
!  A single FREE dendrite grown from one seed in an undercooled melt, using the
!  same diffusion-limited anisotropic growth engine as dendritic_cet.f90.
!  Its purpose is to show the branch hierarchy clearly:
!       PRIMARY arms  along the four <10> directions,
!       SECONDARY arms budding off the primaries,
!       TERTIARY  arms budding off the secondaries.
!
!  Mechanism: latent heat released on freezing (recalescence) diffuses slowly,
!  so it accumulates in the grooves between arms and stalls them, while the
!  tips advance into the cold melt.  4-fold anisotropy orients the arms and
!  stochastic noise seeds the side-branches.  Walls are insulated (zero-flux)
!  so the dendrite grows freely and symmetrically.
!
!  Build : gfortran -O2 -o single single_dendrite.f90
!  Run   : ./single      (then convert single_XXXX.ppm with ppm2png.py)
!==============================================================================
module pm
   implicit none
   integer, parameter :: nx = 401, ny = 401
   integer, parameter :: nsteps = 9000, nout = 1500
   real, parameter :: Ddiff = 0.10      ! low diffusion -> heat stays local
   real, parameter :: U0    = -0.45     ! uniform melt undercooling
   real, parameter :: Lheat = 2.00      ! recalescence
   real, parameter :: krate = 0.10      ! slow, diffusion-limited growth
   real, parameter :: Aan   = 0.92      ! 4-fold anisotropy strength
   real, parameter :: pAn   = 6.0       ! sharpness of <10> lobes
   real, parameter :: noise = 0.35      ! seeds side-branches
   real, parameter :: theta = 0.0       ! crystal orientation (0 -> arms on x/y)
   integer, parameter :: LIQUID = 0, SOLID = 1
end module pm

module sm
   use pm
   implicit none
   integer :: st(nx,ny), claim(nx,ny)
   real    :: U(nx,ny), Un(nx,ny)
   integer :: offi(8), offj(8)
   real    :: offang(8)
end module sm

program single_dendrite
   use pm; use sm
   implicit none
   integer :: step, k, i, j, ss
   integer, allocatable :: seed(:)

   call random_seed(size=ss); allocate(seed(ss)); seed = 12345; call random_seed(put=seed)

   st = LIQUID; claim = 0; U = U0
   k = 0
   do j = -1, 1
      do i = -1, 1
         if (i==0 .and. j==0) cycle
         k = k+1; offi(k)=i; offj(k)=j; offang(k)=atan2(real(-j),real(-i))
      end do
   end do
   ! central seed (a small 2x2 nucleus)
   st(nx/2,   ny/2  ) = SOLID; U(nx/2,   ny/2  ) = U0 + Lheat
   st(nx/2+1, ny/2  ) = SOLID; U(nx/2+1, ny/2  ) = U0 + Lheat
   st(nx/2,   ny/2+1) = SOLID; U(nx/2,   ny/2+1) = U0 + Lheat
   st(nx/2+1, ny/2+1) = SOLID; U(nx/2+1, ny/2+1) = U0 + Lheat

   print '(A)', '  Single free dendrite (primary/secondary/tertiary arms)'
   print '(A)', '    step    %solid'
   do step = 1, nsteps
      call diffuse()
      call grow()
      if (mod(step,nout)==0 .or. step==nsteps) then
         call report(step)
         call dump(step)
      end if
   end do
   print '(A)', '  Done.  Output: single_XXXX.ppm'
end program single_dendrite

subroutine diffuse()
   use pm; use sm
   implicit none
   integer :: i, j
   do j = 2, ny-1
      do i = 2, nx-1
         Un(i,j) = U(i,j) + Ddiff*(U(i+1,j)+U(i-1,j)+U(i,j+1)+U(i,j-1)-4.0*U(i,j))
      end do
   end do
   do j = 2, ny-1
      do i = 2, nx-1
         U(i,j) = Un(i,j)
      end do
   end do
   ! insulated (zero-flux) walls
   do i = 1, nx
      U(i,1) = U(i,2); U(i,ny) = U(i,ny-1)
   end do
   do j = 1, ny
      U(1,j) = U(2,j); U(nx,j) = U(nx-1,j)
   end do
end subroutine diffuse

subroutine grow()
   use pm; use sm
   implicit none
   integer :: i, j, k, ni, nj
   real :: driving, fbest, f, cang, P, r, rn
   claim = 0
   do j = 2, ny-1
      do i = 2, nx-1
         if (st(i,j) /= LIQUID) cycle
         driving = -U(i,j)
         if (driving <= 0.0) cycle
         fbest = -1.0
         do k = 1, 8
            ni = i+offi(k); nj = j+offj(k)
            if (st(ni,nj) /= SOLID) cycle
            cang = cos(4.0*(offang(k) - theta))
            f = (0.5*(1.0+cang))**pAn
            f = (1.0-Aan) + Aan*f
            if (f > fbest) fbest = f
         end do
         if (fbest < 0.0) cycle
         call random_number(rn)
         P = krate*driving*fbest*(1.0 - noise + noise*rn)
         if (P > 1.0) P = 1.0
         call random_number(r)
         if (r < P) claim(i,j) = 1
      end do
   end do
   do j = 2, ny-1
      do i = 2, nx-1
         if (claim(i,j) == 1) then
            st(i,j) = SOLID; U(i,j) = U(i,j) + Lheat
         end if
      end do
   end do
end subroutine grow

subroutine report(step)
   use pm; use sm
   implicit none
   integer, intent(in) :: step
   integer :: i, j, n
   n = 0
   do j = 1, ny
      do i = 1, nx
         if (st(i,j) == SOLID) n = n+1
      end do
   end do
   print '(I8,F10.2)', step, 100.0*real(n)/real(nx*ny)
end subroutine report

subroutine dump(step)
   use pm; use sm
   implicit none
   integer, intent(in) :: step
   character(len=64) :: fn
   character(len=1), parameter :: nl = char(10)
   character(len=32) :: dims
   integer :: i, j, u2, ir, ig, ib
   real :: t
   write(fn,'(A,I4.4,A)') 'single_', step, '.ppm'
   open(newunit=u2, file=trim(fn), access='stream', form='unformatted', status='replace')
   write(dims,'(I0,1X,I0)') nx, ny
   write(u2) 'P6', nl; write(u2) trim(dims), nl; write(u2) '255', nl
   do j = ny, 1, -1
      do i = 1, nx
         if (st(i,j) == SOLID) then
            t = (U(i,j) + 0.5)/2.0            ! recalescence shading
            if (t < 0.0) t = 0.0
            if (t > 1.0) t = 1.0
            ir = 210 + int(45.0*t); ig = 120 + int(110.0*t); ib = 30 + int(60.0*t)
         else
            ir = 6; ig = 12; ib = 30           ! undercooled melt (dark navy)
         end if
         write(u2) char(min(255,ir)), char(min(255,ig)), char(min(255,ib))
      end do
   end do
   close(u2)
end subroutine dump
