# -*- coding: utf-8 -*-
import math
from nums import V, OM, OP, OF, OS, C
import model
from cb import *

RG = model.RGAS
TUM = model.tumour_arrhenius()
HM = model.HM
LC = model.layer_coeffs(model.TISSUE["tumour"]), model.layer_coeffs(model.TISSUE["normal"])
LS = model.laser_shape()


def f1(x): return "%.1f" % x
def f2(x): return "%.2f" % x
def f3(x): return "%.3f" % x
def f4(x): return "%.4f" % x
def k0(x): return "%.0f" % x
def sci(x, n=2):
    m, e = ("%." + str(n) + "e") % x
    return x


def sc(x, n=2):
    s_ = ("%." + str(n) + "e") % x
    m, e = s_.split("e")
    return "$%s\\times10^{%d}$" % (m, int(e))


def tdam(arr, Tc):
    """time (s) for Omega = 1 at constant temperature Tc (deg C)"""
    return 1.0 / (arr["A"] * math.exp(-arr["Ea"] / (RG * (273.15 + Tc))))


def B1(name, sc_="S1"):
    return OM[sc_ + "_" + name]["best"]


def pct(x, n=2): return ("%." + str(n) + "g") % (100 * x)


def e_(x, n=1):
    s_ = ("%." + str(n) + "e") % x
    m, e = s_.split("e")
    return "%s\\times10^{%d}" % (m, int(e))


base = B1("MGL")
bm = base["m"]
bd = base["des"]
pen = B1("Pennes")
pm = pen["m"]
pd_ = pen["des"]
FN_h = 1 - math.exp(-bm["OmN_h"])
