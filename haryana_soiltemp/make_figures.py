#!/usr/bin/env python3
"""Draw the six paper figures from results.json / series.csv (pure stdlib)."""

import csv
import json
import os
import sys

sys.path.insert(0, '/projects/sandbox/AMMAN')
from generate_figures import (PNGCanvas, DARK_BLUE, MED_BLUE, LIGHT_BLUE, PALE_BLUE,
                              DARK_GREEN, MED_GREEN, LIGHT_GREEN, ORANGE, LIGHT_ORANGE,
                              RED, LIGHT_RED, PURPLE, LIGHT_PURPLE, GOLD, LIGHT_GOLD,
                              GRAY, LIGHT_GRAY, BLACK)

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figures')
WHITE = (255, 255, 255)
R = json.load(open(os.path.join(HERE, 'results.json')))


def box(c, x1, y1, x2, y2, col, fill, title, lines=(), lh=13):
    c.rect(x1, y1, x2, y2, col, fill)
    cx = (x1 + x2) // 2
    c.text_c(cx, y1 + 7, title, BLACK, 1)
    for i, ln in enumerate(lines):
        c.text_c(cx, y1 + 24 + i * lh, ln, BLACK, 1)


class Axes:
    def __init__(self, c, x0, y0, x1, y1, xr, yr):
        self.c, self.x0, self.y0, self.x1, self.y1, self.xr, self.yr = c, x0, y0, x1, y1, xr, yr
        c.rect(x0, y0, x1, y1, BLACK)

    def px(self, x):
        return int(self.x0 + (x - self.xr[0]) / (self.xr[1] - self.xr[0]) * (self.x1 - self.x0))

    def py(self, y):
        return int(self.y1 - (y - self.yr[0]) / (self.yr[1] - self.yr[0]) * (self.y1 - self.y0))

    def yticks(self, vals, fmt='{:g}'):
        for v in vals:
            y = self.py(v)
            self.c.hline(self.x0 - 4, self.x0, y, BLACK)
            self.c.hline(self.x0 + 1, self.x1 - 1, y, (235, 235, 235))
            s = fmt.format(v)
            self.c.text(self.x0 - 8 - 6 * len(s), y - 3, s, BLACK, 1)

    def xticks(self, vals, labels=None):
        for i, v in enumerate(vals):
            x = self.px(v)
            self.c.vline(x, self.y1, self.y1 + 4, BLACK)
            s = labels[i] if labels else '{:g}'.format(v)
            self.c.text_c(x, self.y1 + 8, s, BLACK, 1)

    def polyline(self, xs, ys, col, thick=1):
        for i in range(1, len(xs)):
            self.c.line(self.px(xs[i - 1]), self.py(ys[i - 1]), self.px(xs[i]), self.py(ys[i]), col, thick)


def fig1():
    c = PNGCanvas(860, 500)
    c.text_c(430, 10, "Architecture of the IoT-Edge Soil Temperature Forecasting System", BLACK, 2)
    # field layer
    c.rect(20, 55, 300, 440, DARK_GREEN, (240, 248, 236))
    c.text_c(160, 63, "FIELD LAYER (Karnal, Hisar)", DARK_GREEN, 1)
    for i, (lab, prac) in enumerate([("Node K1", "CT plot"), ("Node K2", "ZT-R plot"), ("Node H1", "CT plot")]):
        y = 85 + i * 115
        box(c, 40, y, 280, y + 95, MED_GREEN, LIGHT_GREEN, lab + " - " + prac,
            ["ESP32 + 4 x DS18B20", "5, 10, 20, 50 cm", "Air T, RH, light, moisture", "int8 MLP on-device"])
    # gateway
    box(c, 340, 170, 500, 290, ORANGE, LIGHT_ORANGE, "LoRa GATEWAY",
        ["SX1302 concentrator", "865-867 MHz (IN865)", "4G/Wi-Fi backhaul", "Solar powered"])
    for y in (132, 247, 362):
        c.arrow(282, y, 338, 230, ORANGE, 2, 8)
    c.text(298, 300, "LoRa uplink", ORANGE, 1)
    c.text(298, 312, "every 15 min", ORANGE, 1)
    # cloud
    box(c, 545, 70, 840, 230, MED_BLUE, LIGHT_BLUE, "CLOUD LAYER",
        ["Time-series database", "Quality control, gap filling", "Retraining: MLR, RF, GBT, MLP",
         "Model update pushed to nodes", "Dashboard and API"], 15)
    c.arrow(502, 215, 543, 160, MED_BLUE, 3, 10)
    c.arrow(543, 185, 502, 245, GRAY, 2, 8)
    c.text(505, 255, "OTA weights", GRAY, 1)
    # advisory
    box(c, 545, 280, 840, 420, PURPLE, LIGHT_PURPLE, "ADVISORY LAYER",
        ["1-, 3-, 7-day soil T forecasts", "Wheat sowing window", "Heat and cold alerts",
         "SMS / app in Hindi", "KVK extension staff"], 15)
    c.arrow(692, 232, 692, 278, PURPLE, 3, 10)
    c.text(30, 470, "Edge path: forecast computed on node and sent with data (works if backhaul fails).", BLACK, 1)
    c.text(30, 485, "Figure 1: Three-tier IoT-edge architecture of the proposed network", BLACK, 1)
    c.save(os.path.join(FIG, 'Figure_1_System_Architecture.png'))


def fig2():
    c = PNGCanvas(860, 520)
    c.text_c(430, 10, "Low-Cost Sensor Node: Block Diagram and Probe Installation", BLACK, 2)
    box(c, 260, 180, 430, 280, DARK_BLUE, PALE_BLUE, "ESP32-WROOM-32",
        ["240 MHz dual core", "520 KB SRAM, 4 MB flash", "Deep sleep 15 min", "int8 MLP inference"])
    parts = [
        (20, 60, "4 x DS18B20 (1-Wire)", ["Soil T at 4 depths", "0.0625 C resolution"], MED_GREEN, LIGHT_GREEN, (180, 120), (260, 200)),
        (20, 160, "BME280 (I2C)", ["Air T, RH, pressure"], MED_GREEN, LIGHT_GREEN, (180, 190), (260, 215)),
        (20, 240, "BH1750 (I2C)", ["Illuminance -> Rs proxy"], MED_GREEN, LIGHT_GREEN, (180, 270), (260, 240)),
        (20, 320, "Capacitive moisture", ["0-10 cm, ADC input"], MED_GREEN, LIGHT_GREEN, (180, 350), (260, 265)),
        (500, 60, "SX1276 LoRa (SPI)", ["865 MHz, SF7-SF10"], ORANGE, LIGHT_ORANGE, (500, 90), (430, 200)),
        (500, 160, "Tipping-bucket gauge", ["Rainfall, 1 site"], ORANGE, LIGHT_ORANGE, (500, 190), (430, 225)),
    ]
    for x, y, t, ls, col, fill, a, b in parts:
        box(c, x, y, x + 160, y + 55, col, fill, t, ls, 12)
        c.arrow(a[0], a[1], b[0], b[1], GRAY, 2, 7)
    box(c, 500, 260, 660, 360, RED, LIGHT_RED, "POWER",
        ["6 W solar panel", "CN3791 MPPT charger", "2 x 18650, 6000 mAh", "Low-Iq LDO 3.3 V"], 14)
    c.arrow(500, 300, 432, 262, RED, 2, 7)
    # soil profile
    c.fill_rect(690, 70, 840, 80, (120, 180, 90))
    c.fill_rect(690, 80, 840, 450, (205, 170, 125))
    c.text_c(765, 56, "Soil profile", BLACK, 1)
    for d, lab in [(5, "5 cm"), (10, "10 cm"), (20, "20 cm"), (50, "50 cm")]:
        y = 80 + int(d * 7.2)
        c.fill_rect(745, y - 3, 785, y + 3, (60, 60, 60))
        c.text(790, y - 3, lab, BLACK, 1)
    c.vline(765, 60, 80, BLACK)
    c.text(30, 470, "Indicative node cost: about Rs 5,000 (see Table 1).", BLACK, 1)
    c.text(30, 490, "Figure 2: Sensor node hardware and installation depths of the soil temperature probes", BLACK, 1)
    c.save(os.path.join(FIG, 'Figure_2_Sensor_Node.png'))


def fig3():
    rows = list(csv.DictReader(open(os.path.join(HERE, 'series.csv'))))
    doy = [int(r['doy']) for r in rows]
    c = PNGCanvas(860, 470)
    c.text_c(430, 10, "Simulated Daily Temperatures at Karnal (Test Year, CT Plot)", BLACK, 2)
    ax = Axes(c, 80, 50, 830, 390, (1, 365), (0, 50))
    ax.yticks([0, 10, 20, 30, 40, 50])
    months = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    ax.xticks(months, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    series = [('ta', GRAY, 'Air temperature'), ('t5', RED, 'Soil 5 cm'), ('t20', ORANGE, 'Soil 20 cm'),
              ('t50', DARK_BLUE, 'Soil 50 cm')]
    for k, col, _ in series:
        ax.polyline(doy, [float(r[k]) for r in rows], col, 1 if k == 'ta' else 2)
    for i, (_, col, lab) in enumerate(series):
        x = 100 + i * 170
        c.fill_rect(x, 62, x + 20, 66, col)
        c.text(x + 26, 61, lab, BLACK, 1)
    c.text_c(455, 410, "Month", BLACK, 1)
    c.text(10, 215, "T (C)", BLACK, 1)
    c.text(80, 440, "Figure 3: Simulated air and soil temperatures at four depths, Karnal test year", BLACK, 1)
    c.save(os.path.join(FIG, 'Figure_3_Time_Series.png'))


def fig4():
    c = PNGCanvas(860, 470)
    c.text_c(430, 10, "Test RMSE at 5 cm Depth by Model and Forecast Horizon", BLACK, 2)
    models = ['Persistence', 'MLR', 'RF', 'GBT', 'MLP']
    cols = [GRAY, DARK_BLUE, DARK_GREEN, ORANGE, PURPLE]
    for si, site in enumerate(['Karnal', 'Hisar']):
        x0 = 70 + si * 400
        ax = Axes(c, x0, 60, x0 + 360, 380, (0, 3), (0, 4))
        ax.yticks([0, 1, 2, 3, 4])
        c.text_c(x0 + 180, 44, site, BLACK, 1)
        for hi, h in enumerate([1, 3, 7]):
            for mi, m in enumerate(models):
                v = R['perf'][f'{site}_h{h}'][m]['5']['RMSE']
                bx = ax.px(hi + 0.12) + mi * 20
                c.fill_rect(bx, ax.py(v), bx + 16, ax.py(0) - 1, cols[mi])
        ax.xticks([0.5, 1.5, 2.5], ['1 day', '3 days', '7 days'])
    for i, (m, col) in enumerate(zip(models, cols)):
        x = 120 + i * 140
        c.fill_rect(x, 405, x + 14, 415, col)
        c.text(x + 20, 406, m, BLACK, 1)
    c.text(10, 210, "RMSE", BLACK, 1)
    c.text(10, 222, "(C)", BLACK, 1)
    c.text(70, 445, "Figure 4: Test-year RMSE of soil temperature forecasts at 5 cm for both sites", BLACK, 1)
    c.save(os.path.join(FIG, 'Figure_4_RMSE_Horizons.png'))


def fig5():
    o, p = R['scatter']['obs'], R['scatter']['mlp']
    c = PNGCanvas(620, 560)
    c.text_c(310, 10, "Observed vs Forecast Soil T (5 cm, 1 day, MLP)", BLACK, 2)
    ax = Axes(c, 80, 50, 580, 480, (5, 50), (5, 50))
    ax.yticks([10, 20, 30, 40, 50])
    ax.xticks([10, 20, 30, 40, 50])
    c.line(ax.px(5), ax.py(5), ax.px(50), ax.py(50), BLACK, 1)
    for a, b in zip(o, p):
        x, y = ax.px(a), ax.py(b)
        c.rect(x - 2, y - 2, x + 2, y + 2, MED_BLUE, LIGHT_BLUE)
    m = R['perf']['Karnal_h1']['MLP']['5']
    c.text(100, 70, "Karnal, test year", BLACK, 1)
    c.text(100, 84, "RMSE = %.2f C" % m['RMSE'], BLACK, 1)
    c.text(100, 98, "NSE = %.3f" % m['NSE'], BLACK, 1)
    c.text(100, 112, "KGE = %.3f" % m['KGE'], BLACK, 1)
    c.text(470, 460, "1:1 line", BLACK, 1)
    c.text_c(330, 500, "Observed (simulated sensor) soil T (C)", BLACK, 1)
    c.text(5, 250, "Forecast", BLACK, 1)
    c.text(5, 262, "(C)", BLACK, 1)
    c.text(20, 535, "Figure 5: Agreement plot, MLP 1-day forecast at 5 cm, Karnal", BLACK, 1)
    c.save(os.path.join(FIG, 'Figure_5_Scatter.png'))


def fig6():
    names = {'ta': 'Air T (t)', 'ta_l1': 'Air T (t-1)', 'ta_l2': 'Air T (t-2)', 'rh': 'Rel. humidity',
             'ws': 'Wind speed', 'ssh': 'Sunshine hours', 'rs': 'Solar radiation', 'rain': 'Rainfall',
             'theta': 'Soil moisture', 'obs5': 'Soil T 5 cm (t)', 'obs10': 'Soil T 10 cm (t)',
             'obs20': 'Soil T 20 cm (t)', 'obs50': 'Soil T 50 cm (t)', 'obs5_l1': 'Soil T 5 cm (t-1)',
             'sin_doy': 'sin(day of year)', 'cos_doy': 'cos(day of year)'}
    imp = sorted(R['importance'].items(), key=lambda x: -x[1])
    c = PNGCanvas(820, 520)
    c.text_c(410, 10, "Permutation Importance (MLP, 5 cm, 1-day, Karnal)", BLACK, 2)
    vmax = max(v for _, v in imp)
    ax = Axes(c, 200, 45, 790, 455, (-0.1, vmax * 1.1), (0, len(imp)))
    for i, (k, v) in enumerate(imp):
        y = 50 + i * 25
        c.text(195 - 6 * len(names[k]), y + 6, names[k], BLACK, 1)
        x0, x1 = ax.px(0), ax.px(max(v, 0))
        if x1 > x0:
            c.fill_rect(x0, y + 3, x1, y + 18, DARK_GREEN if i < 5 else MED_GREEN)
        c.text(max(x1, x0) + 5, y + 7, "%.2f" % v, BLACK, 1)
    c.vline(ax.px(0), 45, 455, BLACK)
    c.text_c(495, 470, "Increase in RMSE when feature is permuted (C)", BLACK, 1)
    c.text(20, 500, "Figure 6: Permutation feature importance for the edge MLP model", BLACK, 1)
    c.save(os.path.join(FIG, 'Figure_6_Feature_Importance.png'))


if __name__ == '__main__':
    os.makedirs(FIG, exist_ok=True)
    for f in (fig1, fig2, fig3, fig4, fig5, fig6):
        f()
        print(f.__name__, 'done')
