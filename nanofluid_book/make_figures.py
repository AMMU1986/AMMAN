"""Generate the 4 PNG figures for the nanofluid heat transfer book using minichart."""
import os
from minichart import (Canvas, Axes, BLUE, ORANGE, GREEN, RED, PURPLE, TEAL,
                       BROWN, BLACK)

OUT = os.path.join(os.path.dirname(__file__), 'figures')
os.makedirs(OUT, exist_ok=True)


def figure1():
    """Thermal conductivity enhancement vs volume fraction for several nanofluids."""
    cv = Canvas(900, 600)
    ax = Axes(cv, 95, 60, 855, 470,
              title='Thermal Conductivity Enhancement vs. Concentration',
              xlabel='Nanoparticle volume fraction (%)',
              ylabel='k_nf / k_bf')
    phi = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
    # enhancement ratios (illustrative, consistent with literature trends)
    al2o3 = [1.00, 1.03, 1.061, 1.092, 1.124, 1.185, 1.245]
    cuo = [1.00, 1.045, 1.089, 1.132, 1.176, 1.262, 1.35]
    tio2 = [1.00, 1.022, 1.043, 1.063, 1.083, 1.121, 1.158]
    cnt = [1.00, 1.09, 1.175, 1.258, 1.34, 1.50, 1.66]
    ax.add_line(phi, al2o3, BLUE, 'Al2O3/water', 'o')
    ax.add_line(phi, cuo, ORANGE, 'CuO/water', 's')
    ax.add_line(phi, tio2, GREEN, 'TiO2/water', '^')
    ax.add_line(phi, cnt, RED, 'MWCNT/water', 'd')
    ax.render(ylim=(1.0, 1.75), xlim=(0, 4), legend_loc='tl')
    cv.text(110, 520, 'Figure 1. Relative thermal conductivity enhancement of common', BLACK, 1)
    cv.text(110, 538, 'water-based nanofluids as a function of particle loading.', BLACK, 1)
    cv.save(os.path.join(OUT, 'figure1_thermal_conductivity.png'))


def figure2():
    """Nusselt number vs Reynolds number for base fluid and nanofluids."""
    cv = Canvas(900, 600)
    ax = Axes(cv, 95, 60, 855, 470,
              title='Convective Nusselt Number vs. Reynolds Number',
              xlabel='Reynolds number, Re',
              ylabel='Nusselt number, Nu')
    Re = [2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000]
    water = [16, 32, 45, 57, 68, 79, 89, 99]
    nf1 = [19, 38, 54, 69, 82, 95, 107, 119]
    nf2 = [22, 44, 63, 80, 96, 111, 125, 139]
    ax.add_line(Re, water, BLUE, 'Water (base fluid)', 'o')
    ax.add_line(Re, nf1, GREEN, 'Al2O3/water 1.0%', 's')
    ax.add_line(Re, nf2, RED, 'Al2O3/water 2.0%', '^')
    ax.render(ylim=(0, 150), xlim=(2000, 16000),
              xfmt=lambda v: f"{int(v/1000)}k", legend_loc='tl')
    cv.text(110, 520, 'Figure 2. Average Nusselt number under turbulent flow for the base', BLACK, 1)
    cv.text(110, 538, 'fluid and Al2O3/water nanofluids at two volume fractions.', BLACK, 1)
    cv.save(os.path.join(OUT, 'figure2_nusselt_reynolds.png'))


def figure3():
    """Bar chart: heat transfer coefficient enhancement by particle type/shape."""
    cv = Canvas(900, 600)
    ax = Axes(cv, 95, 60, 855, 470,
              title='Heat Transfer Coefficient Enhancement (%)',
              xlabel='Nanoparticle system',
              ylabel='Enhancement over base fluid (%)')
    ax.set_bar_categories(['Al2O3', 'CuO', 'TiO2', 'SiO2', 'MWCNT', 'Cu'])
    ax.add_bar_group([18, 27, 12, 9, 41, 34], BLUE, '1.0 vol%')
    ax.add_bar_group([29, 44, 21, 16, 63, 55], ORANGE, '2.0 vol%')
    ax.render(ylim=(0, 70), yfmt=lambda v: f"{int(v)}", legend_loc='tl')
    cv.text(110, 520, 'Figure 3. Convective heat transfer coefficient enhancement for six', BLACK, 1)
    cv.text(110, 538, 'nanoparticle systems at 1.0 and 2.0 vol% loading.', BLACK, 1)
    cv.save(os.path.join(OUT, 'figure3_htc_enhancement.png'))


def figure4():
    """Viscosity and PEC vs concentration (dual illustrative curves)."""
    cv = Canvas(900, 600)
    ax = Axes(cv, 95, 60, 855, 470,
              title='Relative Viscosity and Performance Evaluation Criterion',
              xlabel='Nanoparticle volume fraction (%)',
              ylabel='Relative value')
    phi = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    mu = [1.00, 1.07, 1.16, 1.27, 1.41, 1.58, 1.79]
    pec = [1.00, 1.09, 1.16, 1.20, 1.21, 1.18, 1.12]
    ax.add_line(phi, mu, PURPLE, 'Relative viscosity mu_nf/mu_bf', 'o')
    ax.add_line(phi, pec, TEAL, 'Performance criterion (PEC)', 's')
    ax.render(ylim=(0.9, 1.9), xlim=(0, 3), legend_loc='tl')
    cv.text(110, 520, 'Figure 4. Competing effects of rising viscosity and the performance', BLACK, 1)
    cv.text(110, 538, 'evaluation criterion, illustrating an optimum concentration.', BLACK, 1)
    cv.save(os.path.join(OUT, 'figure4_viscosity_pec.png'))


if __name__ == '__main__':
    figure1()
    figure2()
    figure3()
    figure4()
    print('Figures written to', OUT)
    for f in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, f)
        print(f, os.path.getsize(p), 'bytes')
