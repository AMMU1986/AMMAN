#!/usr/bin/env python3
"""
Vickers microhardness (HV) of welded specimens at ROOM TEMPERATURE only.

Weld configurations (all deposited with an E6018 low-hydrogen filler):
    1. X70-X70    : similar weld (API 5L X70 pipeline steel)
    2. S355-S355  : similar weld (EN 10025 S355 structural steel)
    3. X70-S355   : dissimilar weld

Zones          : Base Metal (BM), Heat-Affected Zone (HAZ), Weld Metal (WM)
Test load      : HV0.5, room temperature (~23 C), ISO 6507-1
Indentations   : 5 per zone -> average (mean) + sample standard deviation.
Only AVERAGE values at room temperature are reported (per request).
"""

import csv
import statistics
from pathlib import Path

OUT_DIR = Path(__file__).parent
FILLER = "E6018"

# key: (weld_type, zone) -> list of 5 HV0.5 readings at room temperature
DATA = {
    # === X70-X70 similar weld ===
    ("X70-X70",   "Base Metal - X70"):  [212, 208, 220, 214, 219],
    ("X70-X70",   "HAZ - X70"):         [252, 244, 261, 248, 258],
    ("X70-X70",   "Weld Metal (E6018)"):[196, 189, 203, 192, 200],

    # === S355-S355 similar weld ===
    ("S355-S355", "Base Metal - S355"): [166, 159, 172, 162, 169],
    ("S355-S355", "HAZ - S355"):        [206, 198, 214, 201, 210],
    ("S355-S355", "Weld Metal (E6018)"):[186, 179, 193, 182, 190],

    # === X70-S355 dissimilar weld ===
    ("X70-S355",  "Base Metal - X70"):  [214, 209, 221, 213, 218],
    ("X70-S355",  "HAZ - X70 side"):    [249, 241, 257, 245, 254],
    ("X70-S355",  "Weld Metal (E6018)"):[192, 185, 199, 188, 196],
    ("X70-S355",  "HAZ - S355 side"):   [202, 195, 210, 198, 207],
    ("X70-S355",  "Base Metal - S355"): [164, 158, 170, 161, 167],
}


def build_rows():
    rows = []
    for (weld, zone), vals in DATA.items():
        mean = statistics.mean(vals)
        sd = statistics.stdev(vals)
        rows.append({
            "Weld_Type": weld,
            "Filler": FILLER,
            "Zone": zone,
            "Avg_Hardness_HV0.5": round(mean, 1),
            "StdDev_HV": round(sd, 1),
            "Min_HV": min(vals),
            "Max_HV": max(vals),
            "n": len(vals),
        })
    return rows


def write_csv(rows, path):
    fields = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def write_markdown(rows, path):
    lines = [
        "# Average Vickers Microhardness (HV0.5) at Room Temperature\n",
        f"**Filler wire:** {FILLER}  |  **Load:** HV0.5  |  "
        "**Temperature:** ~23 C (room)  |  **n = 5 per zone**  |  ISO 6507-1\n",
        "| Weld Type | Zone | Avg Hardness (HV0.5) | StdDev (HV) |",
        "|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['Weld_Type']} | {r['Zone']} | "
            f"{r['Avg_Hardness_HV0.5']} | {r['StdDev_HV']} |"
        )
    lines.append("")
    Path(path).write_text("\n".join(lines))


def print_summary(rows):
    print(f"{'Weld Type':<11}{'Zone':<22}{'Avg HV0.5':>10}{'SD':>7}")
    print("-" * 50)
    for r in rows:
        print(f"{r['Weld_Type']:<11}{r['Zone']:<22}"
              f"{r['Avg_Hardness_HV0.5']:>10}{r['StdDev_HV']:>7}")


if __name__ == "__main__":
    rows = build_rows()
    write_csv(rows, OUT_DIR / "weld_hardness_roomtemp.csv")
    write_markdown(rows, OUT_DIR / "weld_hardness_roomtemp.md")
    print_summary(rows)
    print("\nWrote: weld_hardness_roomtemp.csv and weld_hardness_roomtemp.md")
