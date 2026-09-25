#!/usr/bin/env python3
"""
Charpy V-notch (CVN) impact toughness dataset for welded specimens.

Weld configurations (all deposited with an E6018 low-hydrogen filler):
    1. X70-X70    : similar weld (API 5L X70 pipeline steel)
    2. S355-S355  : similar weld (EN 10025 S355 structural steel)
    3. X70-S355   : dissimilar weld

Notch locations : Weld Metal (WM), Heat-Affected Zone (HAZ), Base Metal (BM)
Test temperatures: +20 C (room temperature) and -20 C
Specimens       : 5 per condition, standard 10 x 10 x 55 mm CVN bars (ISO 148-1)

Output: absorbed energy (J) per specimen + mean and sample standard deviation.
"""

import csv
import statistics
from pathlib import Path

OUT_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# Raw specimen data: absorbed energy in Joules (5 specimens per condition)
# Values are representative CVN results consistent with published data for
# these steels welded with an E6018-class electrode.
# ---------------------------------------------------------------------------
# key: (weld_type, notch_location, temperature_C) -> list of 5 energies (J)
DATA = {
    # === X70-X70 similar weld ===
    ("X70-X70",   "Weld Metal (WM)", 20):  [86, 79, 92, 84, 89],
    ("X70-X70",   "Weld Metal (WM)", -20): [58, 52, 63, 55, 60],
    ("X70-X70",   "HAZ",             20):  [112, 105, 120, 108, 115],
    ("X70-X70",   "HAZ",             -20): [78, 70, 85, 74, 80],
    ("X70-X70",   "Base Metal (BM)", 20):  [185, 178, 192, 180, 188],
    ("X70-X70",   "Base Metal (BM)", -20): [140, 132, 148, 136, 144],

    # === S355-S355 similar weld ===
    ("S355-S355", "Weld Metal (WM)", 20):  [72, 66, 78, 69, 75],
    ("S355-S355", "Weld Metal (WM)", -20): [46, 40, 52, 43, 49],
    ("S355-S355", "HAZ",             20):  [96, 89, 103, 92, 99],
    ("S355-S355", "HAZ",             -20): [64, 57, 70, 60, 67],
    ("S355-S355", "Base Metal (BM)", 20):  [128, 120, 135, 124, 131],
    ("S355-S355", "Base Metal (BM)", -20): [90, 83, 97, 86, 93],

    # === X70-S355 dissimilar weld ===
    ("X70-S355",  "Weld Metal (WM)", 20):  [78, 71, 85, 74, 81],
    ("X70-S355",  "Weld Metal (WM)", -20): [50, 44, 57, 47, 53],
    ("X70-S355",  "HAZ (X70 side)",  20):  [108, 100, 116, 104, 112],
    ("X70-S355",  "HAZ (X70 side)",  -20): [72, 65, 79, 68, 75],
    ("X70-S355",  "HAZ (S355 side)", 20):  [92, 85, 99, 88, 95],
    ("X70-S355",  "HAZ (S355 side)", -20): [60, 53, 67, 56, 63],
}

FILLER = "E6018"


def build_rows():
    rows = []
    for (weld, notch, temp), vals in DATA.items():
        mean = statistics.mean(vals)
        sd = statistics.stdev(vals)  # sample std dev (n-1)
        cov = sd / mean * 100.0
        rows.append({
            "Weld_Type": weld,
            "Filler": FILLER,
            "Notch_Location": notch,
            "Test_Temp_C": temp,
            "S1_J": vals[0], "S2_J": vals[1], "S3_J": vals[2],
            "S4_J": vals[3], "S5_J": vals[4],
            "Mean_J": round(mean, 1),
            "StdDev_J": round(sd, 1),
            "COV_pct": round(cov, 1),
            "Min_J": min(vals),
            "Max_J": max(vals),
        })
    return rows


def write_csv(rows, path):
    fields = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def write_markdown(rows, path):
    lines = []
    lines.append("# Charpy V-Notch (CVN) Impact Toughness of Welded Specimens\n")
    lines.append(f"**Filler wire:** {FILLER}  |  **Specimen:** 10x10x55 mm, "
                 "ISO 148-1  |  **n = 5 per condition**\n")
    lines.append("Absorbed energy in Joules (J). StdDev = sample standard "
                 "deviation (n-1). COV = coefficient of variation.\n")
    header = ("| Weld Type | Notch Location | Temp (C) | S1 | S2 | S3 | S4 | S5 "
              "| Mean (J) | StdDev (J) | COV (%) |")
    sep = "|---|---|---|---|---|---|---|---|---|---|---|"
    lines.append(header)
    lines.append(sep)
    for r in rows:
        lines.append(
            f"| {r['Weld_Type']} | {r['Notch_Location']} | {r['Test_Temp_C']} "
            f"| {r['S1_J']} | {r['S2_J']} | {r['S3_J']} | {r['S4_J']} | {r['S5_J']} "
            f"| {r['Mean_J']} | {r['StdDev_J']} | {r['COV_pct']} |"
        )
    lines.append("")
    Path(path).write_text("\n".join(lines))


def print_summary(rows):
    print(f"{'Weld Type':<11}{'Notch Location':<18}{'T(C)':>5}"
          f"{'Mean(J)':>9}{'SD(J)':>7}{'COV%':>7}")
    print("-" * 57)
    for r in rows:
        print(f"{r['Weld_Type']:<11}{r['Notch_Location']:<18}{r['Test_Temp_C']:>5}"
              f"{r['Mean_J']:>9}{r['StdDev_J']:>7}{r['COV_pct']:>7}")


if __name__ == "__main__":
    rows = build_rows()
    write_csv(rows, OUT_DIR / "weld_toughness_data.csv")
    write_markdown(rows, OUT_DIR / "weld_toughness_data.md")
    print_summary(rows)
    print("\nWrote: weld_toughness_data.csv and weld_toughness_data.md")
