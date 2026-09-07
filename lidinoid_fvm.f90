!==============================================================================
! lidinoid_fvm.f90
!
! Finite-Volume steady-state heat-conduction solver on a Lidinoid triply-
! periodic minimal surface (TPMS) porous solid, with a user-controllable
! POROSITY parameter.
!
! Physics
! -------
!   Solves   div( k(x) grad T ) = 0   on a cubic domain [0,L]^3
!   using a cell-centred finite-volume discretisation.
!
!   Each cell is classified SOLID or VOID from the Lidinoid implicit
!   function evaluated at the cell centre:
!        solid  if  |F(x,y,z)| <= t
!        void   otherwise
!   The half-thickness t is calibrated (by bisection) so that the void
!   volume fraction equals the requested POROSITY.
!
!   Conductivities:  k_solid for solid cells, k_void for void cells.
!   Face conductivity = harmonic mean of the two neighbouring cells
!   (correct FV treatment of a discontinuous coefficient).
!
!   Boundary conditions:
!        x = 0   : T = T_hot   (Dirichlet)
!        x = L   : T = T_cold  (Dirichlet)
!        y,z faces: adiabatic   (zero flux)
!
!   The linear system is solved by point SOR (Gauss-Seidel + relaxation).
!   The effective conductivity is recovered from the net heat flux:
!        k_eff = Q * L / ( A * (T_hot - T_cold) )
!
! Usage
! -----
!   ./lidinoid_fvm [porosity] [n] [n_cells]
!     porosity : void fraction in (0,1)      (default 0.95)
!     n        : cells per unit cell edge     (default 40)
!     n_cells  : number of unit cells / edge  (default 1)
!
! Build
! -----
!   gfortran -O2 -o lidinoid_fvm lidinoid_fvm.f90
!
! Note on resolution vs porosity
! ------------------------------
!   TPMS sheet walls get thinner as porosity -> 1.  At very high porosity
!   (e.g. 0.95) the walls are sub-grid unless n is large enough, so the solid
!   fails to percolate and k_eff collapses toward k_void.  Refine the grid for
!   high-porosity cases, e.g. (porosity 0.95):
!        n = 48 -> k_eff/k_solid ~ 1.3e-4   (walls under-resolved)
!        n = 64 -> k_eff/k_solid ~ 2.8e-3
!        n = 96 -> k_eff/k_solid ~ 5.7e-3   (walls resolved, percolating)
!   Moderate porosities (0.5-0.85) are well resolved already at n = 40-48.
!==============================================================================
module fvm_params
  implicit none
  integer,  parameter :: dp = selected_real_kind(15, 307)
  real(dp), parameter :: PI = 3.141592653589793238462643_dp

  ! --- physical / numerical settings (edit as needed) ---------------------
  real(dp), parameter :: L        = 1.0_dp      ! total domain edge length
  real(dp), parameter :: k_solid  = 1.0_dp      ! solid-phase conductivity
  real(dp), parameter :: k_void   = 1.0e-4_dp   ! void-phase conductivity (~air)
  real(dp), parameter :: T_hot    = 1.0_dp      ! Dirichlet at x=0
  real(dp), parameter :: T_cold   = 0.0_dp      ! Dirichlet at x=L
  real(dp), parameter :: omega    = 1.7_dp      ! SOR relaxation factor
  real(dp), parameter :: tol      = 1.0e-7_dp   ! convergence tolerance
  integer,  parameter :: max_iter = 50000       ! iteration cap
contains

  !--- Lidinoid implicit function; period = 1 per unit cell -----------------
  pure real(dp) function lidinoid(x, y, z, ncells) result(f)
    real(dp), intent(in) :: x, y, z
    integer,  intent(in) :: ncells
    real(dp) :: X2, Y2, Z2
    X2 = 2.0_dp*PI*ncells*x
    Y2 = 2.0_dp*PI*ncells*y
    Z2 = 2.0_dp*PI*ncells*z
    f = 0.5_dp*( sin(2*X2)*cos(Y2)*sin(Z2)   &
               + sin(2*Y2)*cos(Z2)*sin(X2)   &
               + sin(2*Z2)*cos(X2)*sin(Y2) ) &
      - 0.5_dp*( cos(2*X2)*cos(2*Y2)         &
               + cos(2*Y2)*cos(2*Z2)         &
               + cos(2*Z2)*cos(2*X2) )       &
      + 0.15_dp
  end function lidinoid

end module fvm_params

!==============================================================================
program lidinoid_fvm
  use fvm_params
  implicit none

  integer  :: n, ncells
  real(dp) :: porosity
  real(dp) :: t_half, achieved_por
  real(dp) :: h, area, keff, qtot
  integer  :: i, j, k, iter
  logical,  allocatable :: solid(:,:,:)
  real(dp), allocatable :: kc(:,:,:)      ! cell conductivity
  real(dp), allocatable :: T(:,:,:)       ! temperature field

  ! -------- read command-line arguments --------
  call read_args(porosity, n, ncells)

  write(*,'(A)') '=============================================================='
  write(*,'(A)') ' Lidinoid TPMS  --  Finite-Volume heat-conduction solver'
  write(*,'(A)') '=============================================================='
  write(*,'(A,F8.4)')  ' Requested porosity      : ', porosity
  write(*,'(A,I0)')    ' Grid cells per edge     : ', n
  write(*,'(A,I0)')    ' Unit cells per edge     : ', ncells
  write(*,'(A,ES10.3,A,ES10.3)') ' k_solid / k_void        : ', k_solid, ' / ', k_void

  allocate(solid(n,n,n), kc(n,n,n), T(0:n+1,0:n+1,0:n+1))
  h    = L / real(n, dp)          ! cell size
  area = L * L                    ! cross-section area normal to x

  ! -------- calibrate half-thickness t for target porosity --------
  call calibrate(porosity, n, ncells, h, t_half, achieved_por)
  write(*,'(A,F10.6)') ' Calibrated half-thick t : ', t_half
  write(*,'(A,F8.4,A)') ' Achieved porosity       : ', achieved_por*100.0_dp, ' %'

  ! -------- build geometry & conductivity field --------
  do k = 1, n
     do j = 1, n
        do i = 1, n
           solid(i,j,k) = ( abs( lidinoid( (i-0.5_dp)*h, (j-0.5_dp)*h, &
                                           (k-0.5_dp)*h, ncells) ) <= t_half )
           if (solid(i,j,k)) then
              kc(i,j,k) = k_solid
           else
              kc(i,j,k) = k_void
           end if
        end do
     end do
  end do

  ! -------- initialise temperature (linear guess) --------
  T = 0.0_dp
  do i = 0, n+1
     T(i,:,:) = T_hot + (T_cold - T_hot) * (real(i,dp)-0.5_dp)/real(n,dp)
  end do

  ! -------- solve by SOR --------
  call solve_sor(n, h, kc, T, iter)

  ! -------- effective conductivity from net x-flux --------
  qtot = heat_flux_x(n, h, kc, T)
  keff = qtot * L / ( area * (T_hot - T_cold) )

  write(*,'(A)') '--------------------------------------------------------------'
  write(*,'(A,I0)')      ' SOR iterations          : ', iter
  write(*,'(A,ES13.6)')  ' Net heat flow Q (x)     : ', qtot
  write(*,'(A,ES13.6)')  ' Effective conductivity  : ', keff
  write(*,'(A,ES13.6)')  ' k_eff / k_solid         : ', keff / k_solid
  write(*,'(A)') '=============================================================='

  ! -------- write a mid-plane temperature slice (z = n/2) for plotting --------
  call write_slice(n, h, T, solid, porosity)

  deallocate(solid, kc, T)

contains

  !--------------------------------------------------------------------------
  subroutine read_args(por, ncell_grid, ncells_uc)
    real(dp), intent(out) :: por
    integer,  intent(out) :: ncell_grid, ncells_uc
    character(len=64) :: arg
    integer :: nargs, ios
    por = 0.95_dp;  ncell_grid = 40;  ncells_uc = 1
    nargs = command_argument_count()
    if (nargs >= 1) then
       call get_command_argument(1, arg); read(arg,*,iostat=ios) por
       if (ios /= 0 .or. por <= 0.0_dp .or. por >= 1.0_dp) por = 0.95_dp
    end if
    if (nargs >= 2) then
       call get_command_argument(2, arg); read(arg,*,iostat=ios) ncell_grid
       if (ios /= 0 .or. ncell_grid < 4) ncell_grid = 40
    end if
    if (nargs >= 3) then
       call get_command_argument(3, arg); read(arg,*,iostat=ios) ncells_uc
       if (ios /= 0 .or. ncells_uc < 1) ncells_uc = 1
    end if
  end subroutine read_args

  !--------------------------------------------------------------------------
  ! Bisection on the half-thickness t so that void fraction == target porosity
  subroutine calibrate(target_por, n, ncells, h, t_out, por_out)
    real(dp), intent(in)  :: target_por, h
    integer,  intent(in)  :: n, ncells
    real(dp), intent(out) :: t_out, por_out
    real(dp) :: lo, hi, tm, solidfrac
    integer  :: it
    lo = 0.0_dp;  hi = 2.0_dp
    do it = 1, 60
       tm = 0.5_dp*(lo+hi)
       solidfrac = solid_fraction(tm, n, ncells, h)
       ! porosity = 1 - solidfrac ; increase t -> more solid -> less porosity
       if ( (1.0_dp - solidfrac) > target_por ) then
          lo = tm          ! too porous, need thicker walls
       else
          hi = tm
       end if
    end do
    t_out   = 0.5_dp*(lo+hi)
    por_out = 1.0_dp - solid_fraction(t_out, n, ncells, h)
  end subroutine calibrate

  !--------------------------------------------------------------------------
  real(dp) function solid_fraction(t, n, ncells, h) result(frac)
    real(dp), intent(in) :: t, h
    integer,  intent(in) :: n, ncells
    integer :: i, j, k
    integer(kind=8) :: cnt
    cnt = 0
    do k = 1, n
       do j = 1, n
          do i = 1, n
             if ( abs( lidinoid((i-0.5_dp)*h,(j-0.5_dp)*h,(k-0.5_dp)*h,ncells) ) <= t ) &
                  cnt = cnt + 1
          end do
       end do
    end do
    frac = real(cnt,dp) / real(int(n,8)**3, dp)
  end function solid_fraction

  !--------------------------------------------------------------------------
  ! Harmonic-mean face conductivity between two cells
  pure real(dp) function kface(ka, kb) result(kf)
    real(dp), intent(in) :: ka, kb
    kf = 2.0_dp*ka*kb / (ka + kb)
  end function kface

  !--------------------------------------------------------------------------
  ! Point SOR sweep to steady state.  x-faces Dirichlet via ghost mirror,
  ! y/z faces adiabatic (zero-flux -> face conductivity = 0).
  subroutine solve_sor(n, h, kc, T, iter)
    integer,  intent(in)    :: n
    real(dp), intent(in)    :: h
    real(dp), intent(in)    :: kc(n,n,n)
    real(dp), intent(inout) :: T(0:n+1,0:n+1,0:n+1)
    integer,  intent(out)   :: iter
    integer  :: i, j, k
    real(dp) :: aw, ae, as, an, ab, at, ap, rhs, Tnew, resid, denom
    real(dp) :: bsrc

    ! Dirichlet on x-faces is applied IMPLICITLY (folded into ap and the
    ! source term) so the update stays diagonally dominant and SOR is stable
    ! for 0 < omega < 2.  y/z faces are adiabatic (zero-flux).
    do iter = 1, max_iter
       resid = 0.0_dp
       denom = 0.0_dp
       do k = 1, n
          do j = 1, n
             do i = 1, n
                bsrc = 0.0_dp
                ! --- west face (x-) ---
                if (i == 1) then
                   aw   = 2.0_dp*kc(i,j,k)      ! wall at half-cell distance
                   bsrc = bsrc + aw*T_hot        ! fixed hot wall
                else
                   aw = kface(kc(i,j,k), kc(i-1,j,k))
                end if
                ! --- east face (x+) ---
                if (i == n) then
                   ae   = 2.0_dp*kc(i,j,k)      ! wall at half-cell distance
                   bsrc = bsrc + ae*T_cold       ! fixed cold wall
                else
                   ae = kface(kc(i,j,k), kc(i+1,j,k))
                end if
                ! --- south/north (y): adiabatic on domain boundary ---
                if (j == 1) then
                   as = 0.0_dp
                else
                   as = kface(kc(i,j,k), kc(i,j-1,k))
                end if
                if (j == n) then
                   an = 0.0_dp
                else
                   an = kface(kc(i,j,k), kc(i,j+1,k))
                end if
                ! --- bottom/top (z): adiabatic on domain boundary ---
                if (k == 1) then
                   ab = 0.0_dp
                else
                   ab = kface(kc(i,j,k), kc(i,j,k-1))
                end if
                if (k == n) then
                   at = 0.0_dp
                else
                   at = kface(kc(i,j,k), kc(i,j,k+1))
                end if

                ap = aw + ae + as + an + ab + at
                if (ap <= 0.0_dp) cycle
                ! interior-neighbour contributions (wall terms already in bsrc)
                rhs = bsrc
                if (i > 1) rhs = rhs + aw*T(i-1,j,k)
                if (i < n) rhs = rhs + ae*T(i+1,j,k)
                rhs = rhs + as*T(i,j-1,k) + an*T(i,j+1,k) &
                          + ab*T(i,j,k-1) + at*T(i,j,k+1)
                Tnew = rhs / ap
                resid = resid + abs(Tnew - T(i,j,k))
                denom = denom + abs(Tnew)
                T(i,j,k) = T(i,j,k) + omega*(Tnew - T(i,j,k))
             end do
          end do
       end do

       if (denom > 0.0_dp) then
          if (resid/denom < tol) exit
       else if (resid < tol) then
          exit
       end if
    end do
    if (iter > max_iter) iter = max_iter
  end subroutine solve_sor

  !--------------------------------------------------------------------------
  ! Net heat flow in +x direction, evaluated at the mid x-plane (i.e. sum of
  ! face fluxes between column i and i+1), averaged over interior planes.
  real(dp) function heat_flux_x(n, h, kc, T) result(qavg)
    integer,  intent(in) :: n
    real(dp), intent(in) :: h
    real(dp), intent(in) :: kc(n,n,n)
    real(dp), intent(in) :: T(0:n+1,0:n+1,0:n+1)
    integer  :: i, j, k
    real(dp) :: qplane, kf, qsum
    qsum = 0.0_dp
    do i = 1, n-1
       qplane = 0.0_dp
       do k = 1, n
          do j = 1, n
             kf = kface(kc(i,j,k), kc(i+1,j,k))
             ! flux through face (area h*h), q = -k*dT/dx * A
             qplane = qplane + kf * (T(i,j,k) - T(i+1,j,k)) / h * (h*h)
          end do
       end do
       qsum = qsum + qplane
    end do
    qavg = qsum / real(n-1, dp)
  end function heat_flux_x

  !--------------------------------------------------------------------------
  subroutine write_slice(n, h, T, solid, por)
    integer,  intent(in) :: n
    real(dp), intent(in) :: h, por
    real(dp), intent(in) :: T(0:n+1,0:n+1,0:n+1)
    logical,  intent(in) :: solid(n,n,n)
    integer :: i, j, kmid, u
    character(len=80) :: fname
    kmid = n/2
    write(fname,'(A,I0,A)') 'lidinoid_output/fvm_Tslice_por', nint(por*100), '.csv'
    open(newunit=u, file=trim(fname), status='replace', action='write')
    write(u,'(A)') 'i,j,x,y,T,phase'
    do j = 1, n
       do i = 1, n
          write(u,'(I0,",",I0,",",F8.5,",",F8.5,",",ES13.6,",",I0)') &
               i, j, (i-0.5_dp)*h, (j-0.5_dp)*h, T(i,j,kmid), merge(1,0,solid(i,j,kmid))
       end do
    end do
    close(u)
    write(*,'(A,A)') ' Mid-plane slice written : ', trim(fname)
  end subroutine write_slice

end program lidinoid_fvm
