!===============================================================================
! gyroid_png.f90
!
! Renders a Gyroid TPMS isosurface to a PNG image -- NO external libraries.
!
!   * Ray-marches the implicit surface  F(x,y,z) = sin x cos y + sin y cos z
!     + sin z cos x = iso  inside a cubic block of "ncell" unit cells.
!   * Diffuse + head-light shading gives the 3D look; open channels (tunnels)
!     appear as the characteristic round "holes" when viewed near an axis.
!   * Writes a real PNG using uncompressed DEFLATE ("stored") blocks with a
!     correct zlib header, Adler-32 checksum and per-chunk CRC-32.
!
!   Requires only stream I/O (Fortran 2003).  Build & run:
!       gfortran -O2 -o gyroid_png gyroid_png.f90
!       ./gyroid_png            ->  writes gyroid.png
!===============================================================================
program gyroid_png
    implicit none
    integer, parameter :: dp = selected_real_kind(15, 307)
    integer, parameter :: i1 = selected_int_kind(2)   ! 1-byte integer

    ! ----- Image / scene parameters -----------------------------------------
    integer,  parameter :: w = 720, h = 720          ! image size (pixels)
    integer,  parameter :: ncell = 3                 ! unit cells per axis
    real(dp), parameter :: iso = 0.0_dp              ! isovalue of the surface
    real(dp), parameter :: pi  = 3.141592653589793_dp
    real(dp), parameter :: fov_deg = 42.0_dp         ! camera field of view

    ! ----- Derived scene geometry -------------------------------------------
    real(dp), parameter :: L = real(ncell, dp) * 2.0_dp * pi   ! block size
    real(dp) :: cen(3), eye(3), fwd(3), rgt(3), upv(3), up0(3)
    real(dp) :: ldir(3), dist, tanf, aspect

    ! ----- Byte buffers ------------------------------------------------------
    integer, parameter :: rowstride = 1 + 3*w
    integer, parameter :: nraw = h * rowstride
    integer(i1), allocatable :: raw(:), zlib(:)
    integer, allocatable :: crctab(:)
    integer :: zlen

    ! ----- Misc --------------------------------------------------------------
    integer  :: px, py, base, r, g, b
    real(dp) :: u, v, dir(3), col(3)

    ! ----- Build CRC table ---------------------------------------------------
    allocate(crctab(0:255))
    call build_crc_table(crctab)

    ! ----- Camera setup (look near the +y axis with a slight tilt) ----------
    cen = (/ 0.5_dp*L, 0.5_dp*L, 0.5_dp*L /)
    fwd = normalize((/ 0.16_dp, 1.0_dp, 0.11_dp /))   ! view direction
    dist = 2.6_dp * L
    eye  = cen - dist * fwd
    up0  = (/ 0.0_dp, 0.0_dp, 1.0_dp /)
    rgt  = normalize(cross(fwd, up0))
    upv  = cross(rgt, fwd)
    ldir = normalize((/ -0.35_dp, -0.75_dp, 0.55_dp /))  ! direction TO light
    tanf = tan(0.5_dp * fov_deg * pi / 180.0_dp)
    aspect = real(w, dp) / real(h, dp)

    ! ----- Render into the raw scanline buffer ------------------------------
    allocate(raw(nraw))
    raw = 0_i1
    do py = 0, h-1
        raw(py*rowstride + 1) = 0_i1                  ! PNG filter byte = None
        v = (1.0_dp - 2.0_dp*(real(py, dp)+0.5_dp)/real(h, dp)) * tanf
        do px = 0, w-1
            u = (2.0_dp*(real(px, dp)+0.5_dp)/real(w, dp) - 1.0_dp) * tanf * aspect
            dir = normalize(fwd + u*rgt + v*upv)
            call shade_pixel(eye, dir, ldir, col)
            r = clamp255(col(1)); g = clamp255(col(2)); b = clamp255(col(3))
            base = py*rowstride + 1 + 3*px + 1
            raw(base)   = to_byte(r)
            raw(base+1) = to_byte(g)
            raw(base+2) = to_byte(b)
        end do
    end do

    ! ----- Wrap raw data in a zlib stream (stored blocks) -------------------
    call build_zlib(raw, nraw, zlib, zlen)

    ! ----- Write the PNG file ------------------------------------------------
    call write_png("gyroid.png", zlib, zlen, crctab)

    write(*,'(A)')          "Wrote gyroid.png"
    write(*,'(A,I0,A,I0)')  "Image size : ", w, " x ", h
    write(*,'(A,I0)')       "Unit cells : ", ncell

contains

    !===========================================================================
    ! Gyroid implicit function.
    !===========================================================================
    function fgyr(p) result(val)
        real(dp), intent(in) :: p(3)
        real(dp) :: val
        val = sin(p(1))*cos(p(2)) + sin(p(2))*cos(p(3)) + sin(p(3))*cos(p(1)) - iso
    end function fgyr

    !===========================================================================
    ! Shade one pixel by ray-marching to the first surface crossing.
    !===========================================================================
    subroutine shade_pixel(o, d, lgt, col)
        real(dp), intent(in)  :: o(3), d(3), lgt(3)
        real(dp), intent(out) :: col(3)
        real(dp), parameter :: bg(3) = (/ 0.96_dp, 0.97_dp, 0.98_dp /)  ! background
        real(dp), parameter :: base(3) = (/ 0.27_dp, 0.72_dp, 0.80_dp /)! cyan
        real(dp) :: t0, t1, ds, ta, tb, fa, fb, tm, fm, p(3), nrm(3)
        real(dp) :: diff, head, shade
        integer  :: it, nstep

        col = bg
        if (.not. box_hit(o, d, 0.0_dp, L, t0, t1)) return
        t0 = max(t0, 0.0_dp) + 1.0e-4_dp

        ds = 0.05_dp
        ta = t0
        fa = fgyr(o + ta*d)
        nstep = int((t1 - t0)/ds) + 1
        do it = 1, nstep
            tb = min(ta + ds, t1)
            fb = fgyr(o + tb*d)
            if (fa*fb <= 0.0_dp) then
                ! ----- bisection refine to the crossing -----
                do while (tb - ta > 1.0e-5_dp)
                    tm = 0.5_dp*(ta+tb)
                    fm = fgyr(o + tm*d)
                    if (fa*fm <= 0.0_dp) then
                        tb = tm; fb = fm
                    else
                        ta = tm; fa = fm
                    end if
                end do
                p = o + 0.5_dp*(ta+tb)*d
                nrm = surf_normal(p)
                if (dot(nrm, d) > 0.0_dp) nrm = -nrm      ! face the camera
                diff = max(0.0_dp, dot(nrm, lgt))
                head = max(0.0_dp, dot(nrm, -d))          ! head-light rim
                shade = 0.22_dp + 0.68_dp*diff + 0.18_dp*head
                if (shade > 1.0_dp) shade = 1.0_dp
                col = base * shade
                return
            end if
            ta = tb; fa = fb
            if (tb >= t1) exit
        end do
    end subroutine shade_pixel

    !===========================================================================
    ! Surface normal via central differences of F.
    !===========================================================================
    function surf_normal(p) result(nrm)
        real(dp), intent(in) :: p(3)
        real(dp) :: nrm(3), e
        e = 1.0e-3_dp
        nrm(1) = fgyr(p+(/e,0.0_dp,0.0_dp/)) - fgyr(p-(/e,0.0_dp,0.0_dp/))
        nrm(2) = fgyr(p+(/0.0_dp,e,0.0_dp/)) - fgyr(p-(/0.0_dp,e,0.0_dp/))
        nrm(3) = fgyr(p+(/0.0_dp,0.0_dp,e/)) - fgyr(p-(/0.0_dp,0.0_dp,e/))
        nrm = normalize(nrm)
    end function surf_normal

    !===========================================================================
    ! Ray/axis-aligned-box intersection (slab method). Box = [bmin,bmax]^3.
    !===========================================================================
    logical function box_hit(o, d, bmin, bmax, tenter, texit)
        real(dp), intent(in)  :: o(3), d(3), bmin, bmax
        real(dp), intent(out) :: tenter, texit
        real(dp) :: t0, t1, lo, hi, tmp
        integer  :: k
        tenter = -1.0e30_dp
        texit  =  1.0e30_dp
        do k = 1, 3
            if (abs(d(k)) < 1.0e-12_dp) then
                if (o(k) < bmin .or. o(k) > bmax) then
                    box_hit = .false.; return
                end if
            else
                t0 = (bmin - o(k)) / d(k)
                t1 = (bmax - o(k)) / d(k)
                lo = min(t0, t1); hi = max(t0, t1)
                if (lo > tenter) tenter = lo
                if (hi < texit)  texit  = hi
            end if
        end do
        box_hit = (tenter < texit) .and. (texit > 0.0_dp)
        tmp = tmp  ! silence unused (never reached)
    end function box_hit

    !===========================================================================
    ! Vector helpers.
    !===========================================================================
    function cross(a, b) result(c)
        real(dp), intent(in) :: a(3), b(3)
        real(dp) :: c(3)
        c(1) = a(2)*b(3) - a(3)*b(2)
        c(2) = a(3)*b(1) - a(1)*b(3)
        c(3) = a(1)*b(2) - a(2)*b(1)
    end function cross

    function dot(a, b) result(s)
        real(dp), intent(in) :: a(3), b(3)
        real(dp) :: s
        s = a(1)*b(1) + a(2)*b(2) + a(3)*b(3)
    end function dot

    function normalize(a) result(u)
        real(dp), intent(in) :: a(3)
        real(dp) :: u(3), m
        m = sqrt(a(1)*a(1) + a(2)*a(2) + a(3)*a(3))
        if (m < 1.0e-30_dp) m = 1.0_dp
        u = a / m
    end function normalize

    integer function clamp255(x)
        real(dp), intent(in) :: x
        real(dp) :: y
        y = x
        if (y < 0.0_dp) y = 0.0_dp
        if (y > 1.0_dp) y = 1.0_dp
        clamp255 = nint(y * 255.0_dp)
    end function clamp255

    !===========================================================================
    ! Convert a 0..255 integer into a signed 1-byte integer.
    !===========================================================================
    function to_byte(v) result(b)
        integer, intent(in) :: v
        integer(i1) :: b
        if (v > 127) then
            b = int(v - 256, i1)
        else
            b = int(v, i1)
        end if
    end function to_byte

    !===========================================================================
    ! Build a zlib stream from raw data using uncompressed DEFLATE blocks.
    !===========================================================================
    subroutine build_zlib(src, n, out, outlen)
        integer(i1), intent(in)  :: src(:)
        integer,     intent(in)  :: n
        integer(i1), allocatable, intent(out) :: out(:)
        integer,     intent(out) :: outlen
        integer, parameter :: mx = 65535
        integer :: nblk, cap, pos, off, blen, s1, s2, k, bv
        nblk = (n + mx - 1) / mx
        if (nblk == 0) nblk = 1
        cap = 2 + nblk*5 + n + 4
        allocate(out(cap))
        out(1) = to_byte(120)      ! CMF = 0x78
        out(2) = to_byte(1)        ! FLG = 0x01  (0x7801 divisible by 31)
        pos = 3
        off = 1
        do
            blen = min(mx, n - off + 1)
            if (off - 1 + blen >= n) then
                out(pos) = to_byte(1)          ! BFINAL=1, BTYPE=00
            else
                out(pos) = to_byte(0)          ! BFINAL=0, BTYPE=00
            end if
            pos = pos + 1
            out(pos)   = to_byte(iand(blen,255));                pos = pos + 1
            out(pos)   = to_byte(iand(ishft(blen,-8),255));      pos = pos + 1
            out(pos)   = to_byte(iand(ieor(blen,65535),255));    pos = pos + 1
            out(pos)   = to_byte(iand(ishft(ieor(blen,65535),-8),255)); pos = pos + 1
            out(pos:pos+blen-1) = src(off:off+blen-1)
            pos = pos + blen
            off = off + blen
            if (off > n) exit
        end do
        ! ----- Adler-32 over the raw data -----
        s1 = 1; s2 = 0
        do k = 1, n
            bv = iand(int(src(k)), 255)
            s1 = mod(s1 + bv, 65521)
            s2 = mod(s2 + s1, 65521)
        end do
        out(pos)   = to_byte(iand(ishft(s2,-8),255)); pos = pos + 1
        out(pos)   = to_byte(iand(s2,255));           pos = pos + 1
        out(pos)   = to_byte(iand(ishft(s1,-8),255)); pos = pos + 1
        out(pos)   = to_byte(iand(s1,255));           pos = pos + 1
        outlen = pos - 1
    end subroutine build_zlib

    !===========================================================================
    ! CRC-32 (PNG polynomial) table and helpers.
    !===========================================================================
    subroutine build_crc_table(tab)
        integer, intent(out) :: tab(0:255)
        integer :: nn, kk, c, poly
        poly = int(z'EDB88320')
        do nn = 0, 255
            c = nn
            do kk = 1, 8
                if (iand(c,1) /= 0) then
                    c = ieor(ishft(c,-1), poly)
                else
                    c = ishft(c,-1)
                end if
            end do
            tab(nn) = c
        end do
    end subroutine build_crc_table

    subroutine crc_accum(crc, bytes, n, tab)
        integer,     intent(inout) :: crc
        integer(i1), intent(in)    :: bytes(:)
        integer,     intent(in)    :: n, tab(0:255)
        integer :: k, bv, idx
        do k = 1, n
            bv  = iand(int(bytes(k)), 255)
            idx = iand(ieor(crc, bv), 255)
            crc = ieor(ishft(crc,-8), tab(idx))
        end do
    end subroutine crc_accum

    !===========================================================================
    ! Write a PNG chunk: length | type | data | CRC  (CRC over type+data).
    !===========================================================================
    subroutine write_chunk(unit, ctype, data, ndata, tab)
        integer,          intent(in) :: unit, ndata, tab(0:255)
        character(len=4), intent(in) :: ctype
        integer(i1),      intent(in) :: data(:)
        integer(i1) :: len4(4), typ(4), crc4(4)
        integer :: crc, k
        len4(1) = to_byte(iand(ishft(ndata,-24),255))
        len4(2) = to_byte(iand(ishft(ndata,-16),255))
        len4(3) = to_byte(iand(ishft(ndata,-8),255))
        len4(4) = to_byte(iand(ndata,255))
        do k = 1, 4
            typ(k) = to_byte(iachar(ctype(k:k)))
        end do
        crc = -1                                   ! 0xFFFFFFFF
        call crc_accum(crc, typ, 4, tab)
        if (ndata > 0) call crc_accum(crc, data, ndata, tab)
        crc = ieor(crc, -1)                        ! final XOR 0xFFFFFFFF
        crc4(1) = to_byte(iand(ishft(crc,-24),255))
        crc4(2) = to_byte(iand(ishft(crc,-16),255))
        crc4(3) = to_byte(iand(ishft(crc,-8),255))
        crc4(4) = to_byte(iand(crc,255))
        write(unit) len4
        write(unit) typ
        if (ndata > 0) write(unit) data(1:ndata)
        write(unit) crc4
    end subroutine write_chunk

    !===========================================================================
    ! Assemble and write the whole PNG file.
    !===========================================================================
    subroutine write_png(fname, idat, idlen, tab)
        character(len=*), intent(in) :: fname
        integer(i1),      intent(in) :: idat(:)
        integer,          intent(in) :: idlen, tab(0:255)
        integer, parameter :: u = 20
        integer(i1) :: sig(8), ihdr(13), empty(1)
        sig = (/ to_byte(137), to_byte(80), to_byte(78), to_byte(71), &
                 to_byte(13),  to_byte(10), to_byte(26), to_byte(10) /)
        ! IHDR
        ihdr(1)  = to_byte(iand(ishft(w,-24),255))
        ihdr(2)  = to_byte(iand(ishft(w,-16),255))
        ihdr(3)  = to_byte(iand(ishft(w,-8),255))
        ihdr(4)  = to_byte(iand(w,255))
        ihdr(5)  = to_byte(iand(ishft(h,-24),255))
        ihdr(6)  = to_byte(iand(ishft(h,-16),255))
        ihdr(7)  = to_byte(iand(ishft(h,-8),255))
        ihdr(8)  = to_byte(iand(h,255))
        ihdr(9)  = to_byte(8)     ! bit depth
        ihdr(10) = to_byte(2)     ! color type 2 = truecolor RGB
        ihdr(11) = to_byte(0)     ! compression
        ihdr(12) = to_byte(0)     ! filter method
        ihdr(13) = to_byte(0)     ! interlace
        empty(1) = 0_i1
        open(unit=u, file=fname, access='stream', form='unformatted', status='replace')
        write(u) sig
        call write_chunk(u, "IHDR", ihdr, 13, tab)
        call write_chunk(u, "IDAT", idat, idlen, tab)
        call write_chunk(u, "IEND", empty, 0, tab)
        close(u)
    end subroutine write_png

end program gyroid_png
