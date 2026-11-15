"""Load the anchor dataset (Singh 2022, Tables 2, 3 and 12)."""

import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(HERE), "pmedm_ml_data")
POWDER_CODE = {"graphite": 0, "alumina": 1, "none": 2}


def load_runs():
    path = os.path.join(DATA_DIR, "singh2022_l27_pmedm_wc.csv")
    rows = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            rows.append({
                "run": int(r["run"]),
                "x": (float(r["toff_us"]), float(r["ton_us"]), float(r["current_A"]),
                      POWDER_CODE[r["powder"]]),
                "powder": r["powder"],
                "mrr": float(r["mrr_mm3_min"]),
                "twr": float(r["twr_mm3_min"]),
                "rep": {k: float(r[k]) for k in ("mrr_norm_reported", "twr_norm_reported",
                                                 "grc_mrr_reported", "grc_twr_reported",
                                                 "grg_reported", "ganfis_reported")},
                "rank_grg": int(r["rank_grg_reported"]),
                "rank_ganfis": int(r["rank_ganfis_reported"]),
            })
    return rows


def load_confirmation():
    path = os.path.join(DATA_DIR, "singh2022_confirmation_runs.csv")
    out = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            out.append({"x": (float(r["toff_us"]), float(r["ton_us"]), float(r["current_A"]),
                              POWDER_CODE[r["powder"]]),
                        "mrr": float(r["mrr_mm3_min"]), "twr": float(r["twr_mm3_min"])})
    return out


def design_label(x):
    lv = [(10.0, 50.0, 75.0), (15.0, 50.0, 100.0), (3.0, 6.0, 9.0)]

    def lev(v, j):
        return 1 + min(range(3), key=lambda k: abs(lv[j][k] - v))

    return "A%dB%dC%dD%d" % (lev(x[0], 0), lev(x[1], 1), x[3] + 1, lev(x[2], 2))


def log_targets(rows, key):
    return [math.log(r[key]) for r in rows]
