#!/usr/bin/env python3
"""
Build Fractional_TriHybrid_Disks_Equations.docx: every one of the 130 equations
rendered as a native Word Equation-Editor (OMML) object, numbered, with section
headings. Each equation is a real editable m:oMath element -- click into it in
Word and it opens in the equation editor; copy/paste works as an equation.

Stdlib only.
"""

import zipfile
from omml import (run as R, txt, frac, sup, sub, subsup, rad, delim, nary,
                  nary_nolim, lim_lower, group as GP, G)

# convenient shorthands
def it(s): return R(s)          # italic variable
def up(s): return txt(s)        # upright text
def op(s): return R(s, 'p')     # operator/symbol upright

PLUS = op('+'); MINUS = op('&#8722;'); EQ = op('='); CDOT = op(G['cdot'])
LP = op('('); RP = op(')')

# frequently used tokens
def d_(): return R(G['partial'])            # partial symbol
def al(): return R(G['alpha'])
def et(): return R(G['eta'])
def th(): return R(G['theta'])
def mu(): return R(G['mu'])
def nu(): return R(G['nu'])
def rho(): return R(G['rho'])
def sig(): return R(G['sigma'])
def kap(): return R(G['kappa'])
def lam(): return R(G['lambda'])
def phi(): return R(G['phi'])
def Phi(): return R(G['Phi'])
def bet(): return R(G['beta'])
def gam(): return R(G['gamma'])
def Lam(): return R(G['Lambda'])

# partial derivative d f / d x  (upright partials)
def pd(f, x, order=1):
    if order == 1:
        return frac(d_() + f, d_() + x)
    return frac(sup(d_(), op(str(order))) + f, d_() + sup(x, op(str(order))))

def dd(f, x, order=1):
    # ordinary derivative
    if order == 1:
        return frac(R('d') + f, R('d') + x)
    return frac(sup(R('d'), op(str(order))) + f, R('d') + sup(x, op(str(order))))

# CF derivative operator symbol: {}^{CF}D_t^{alpha}
def CFD(order_inner=None):
    pre = sup(R(''), up('CF'))  # leading superscript CF (approx via small sup)
    base = sub(R('D'), R('t'))
    a = order_inner if order_inner else al()
    return up('CF') + sup(base, a)

# ---- Build each equation body ----
E = {}

E[1] = (it('V') + EQ + delim(it('u') + delim(R('r,z,t')) + op(',') + op('0') + op(',') +
        it('w') + delim(R('r,z,t'))))

E[2] = (it('h') + delim(it('t')) + EQ + it('H') +
        sup(delim(op('1') + MINUS + it('b') + it('t')), frac(op('1'), op('2'))))

E[3] = (frac(R('d') + it('h'), R('d') + it('t')) + EQ + MINUS + frac(op('1'), op('2')) +
        it('b') + it('H') + sup(delim(op('1') + MINUS + it('b') + it('t')),
                                 MINUS + frac(op('1'), op('2'))))

E[4] = (it('B') + delim(it('t')) + EQ + sub(it('B'), op('0')) +
        sup(delim(op('1') + MINUS + it('b') + it('t')), MINUS + frac(op('1'), op('2'))))

E[5] = (CFD() + it('g') + delim(it('t')) + EQ +
        frac(it('M') + delim(al()), op('1') + MINUS + al()) +
        nary(G['integral'], op('0'), it('t'),
             sup(it('g'), R(G['prime'])) + delim(it('s')) +
             txt('exp') + delim(MINUS + frac(al() + delim(it('t') + MINUS + it('s')),
                                             op('1') + MINUS + al()), '[', ']') +
             R('d') + it('s')))

E[6] = (lim_lower(txt('lim'), al() + op(G['to']) + op('1')) + CFD() + it('g') +
        delim(it('t')) + EQ + sup(it('g'), R(G['prime'])) + delim(it('t')))

E[7] = (lim_lower(txt('lim'), al() + op(G['to']) + op('0')) + CFD() + it('g') +
        delim(it('t')) + EQ + it('g') + delim(it('t')) + MINUS + it('g') + delim(op('0')))

E[8] = (al() + EQ + al() + delim(et() + op(',') + it('t')) + op(',') +
        op('0') + op('&lt;') + sub(al(), up('min')) + op(G['leq']) +
        al() + delim(et() + op(',') + it('t')) + op(G['leq']) + op('1'))

E[9] = (sup(sub(R('D'), R('t')), al() + delim(et() + op(',') + it('t'))) + it('g') + EQ +
        frac(op('1'), op('1') + MINUS + al() + delim(et() + op(',') + it('t'))) +
        nary(G['integral'], op('0'), it('t'),
             sup(it('g'), R(G['prime'])) + delim(it('s')) +
             txt('exp') + delim(MINUS + frac(al() + delim(et() + op(',') + it('t')) +
                                             delim(it('t') + MINUS + it('s')),
                                             op('1') + MINUS + al() + delim(et() + op(',') + it('t'))),
                                '[', ']') + R('d') + it('s')))

E[10] = (al() + delim(et() + op(',') + it('t')) + EQ + op('1') + MINUS +
         delim(op('1') + MINUS + sub(al(), op('0'))) +
         sup(delim(op('1') + MINUS + it('b') + it('t')), frac(op('1'), op('2'))) +
         Lam() + delim(et()))

E[11] = (Lam() + delim(et()) + EQ + op('4') + et() + delim(op('1') + MINUS + et()))

E[12] = (pd(it('u'), it('r')) + PLUS + frac(it('u'), it('r')) + PLUS +
         pd(it('w'), it('z')) + EQ + op('0'))

# momentum (13) -- write compactly but complete
E[13] = (pd(it('u'), it('t')) + PLUS + it('u') + pd(it('u'), it('r')) + PLUS +
         it('w') + pd(it('u'), it('z')) + EQ +
         MINUS + frac(op('1'), sub(rho(), up('thnf'))) + pd(it('p'), it('r')) + PLUS +
         frac(sub(mu(), up('thnf')), sub(rho(), up('thnf'))) +
         delim(pd(it('u'), it('z'), 2) + frac(op('1'), it('r')) + pd(it('u'), it('r')) +
               PLUS + pd(it('u'), it('r'), 2) + MINUS + frac(it('u'), sup(it('r'), op('2'))), '[', ']') +
         MINUS + frac(sub(sig(), up('thnf')), sub(rho(), up('thnf'))) +
         sup(it('B'), op('2')) + it('u') + MINUS +
         frac(sub(mu(), up('thnf')), sub(rho(), up('thnf'))) +
         frac(it('u'), sub(sup(it('K'), op('*')), it('p'))) + MINUS +
         frac(sub(it('C'), it('b')), rad(sub(sup(it('K'), op('*')), it('p')))) + sup(it('u'), op('2')) +
         PLUS + frac(sub(R(G['delta']), op('1')), sub(rho(), up('thnf'))) +
         sup(sub(R('D'), R('t')), al()) + sub(it('L'), it('u')))

E[14] = (sub(it('L'), it('u')) + delim(it('u') + op(',') + it('w')) + EQ +
         pd(it('u'), it('z'), 2) + PLUS + frac(op('1'), it('r')) + pd(it('u'), it('r')) +
         PLUS + pd(it('u'), it('r'), 2) + MINUS + frac(it('u'), sup(it('r'), op('2'))) +
         PLUS + it('u') + frac(R('d'), R('d') + it('r')) + delim(pd(it('u'), it('z'), 2)) +
         PLUS + it('w') + frac(R('d'), R('d') + it('z')) + delim(pd(it('u'), it('z'), 2)))

E[15] = (pd(it('w'), it('t')) + PLUS + it('u') + pd(it('w'), it('r')) + PLUS +
         it('w') + pd(it('w'), it('z')) + EQ + MINUS +
         frac(op('1'), sub(rho(), up('thnf'))) + pd(it('p'), it('z')) + PLUS +
         frac(sub(mu(), up('thnf')), sub(rho(), up('thnf'))) +
         delim(pd(it('w'), it('z'), 2) + frac(op('1'), it('r')) + pd(it('w'), it('r')) +
               PLUS + pd(it('w'), it('r'), 2), '[', ']') + MINUS +
         frac(sub(mu(), up('thnf')), sub(rho(), up('thnf'))) +
         frac(it('w'), sub(sup(it('K'), op('*')), it('p'))) + MINUS +
         frac(sub(it('C'), it('b')), rad(sub(sup(it('K'), op('*')), it('p')))) + sup(it('w'), op('2')) +
         PLUS + frac(sub(R(G['delta']), op('1')), sub(rho(), up('thnf'))) +
         sup(sub(R('D'), R('t')), al()) + sub(it('L'), it('w')))

E[16] = (sub(it('L'), it('w')) + delim(it('u') + op(',') + it('w')) + EQ +
         pd(it('w'), it('z'), 2) + PLUS + frac(op('1'), it('r')) + pd(it('w'), it('r')) +
         PLUS + pd(it('w'), it('r'), 2) + PLUS + it('u') + frac(R('d'), R('d') + it('r')) +
         delim(pd(it('w'), it('z'), 2)) + PLUS + it('w') + frac(R('d'), R('d') + it('z')) +
         delim(pd(it('w'), it('z'), 2)))

E[17] = (it('q') + PLUS + sub(lam(), it('T')) + sup(sub(R('D'), R('t')), al()) + it('q') +
         EQ + MINUS + sub(kap(), up('thnf')) + R(G['nabla']) + it('T'))

E[18] = (delim(op('1') + PLUS + sub(lam(), it('T')) + sup(sub(R('D'), R('t')), al())) +
         delim(pd(it('T'), it('t')) + it('u') + pd(it('T'), it('r')) + PLUS + it('w') +
               pd(it('T'), it('z')), '[', ']') + EQ +
         frac(sub(kap(), up('thnf')), sub(delim(rho() + sub(it('C'), it('p'))), up('thnf'))) +
         delim(pd(it('T'), it('r'), 2) + frac(op('1'), it('r')) + pd(it('T'), it('r')) + PLUS +
               pd(it('T'), it('z'), 2), '[', ']') + MINUS +
         frac(op('1'), sub(delim(rho() + sub(it('C'), it('p'))), up('thnf'))) +
         pd(sub(it('q'), it('r')), it('z')) + PLUS +
         frac(sub(sig(), up('thnf')), sub(delim(rho() + sub(it('C'), it('p'))), up('thnf'))) +
         sup(it('B'), op('2')) + sup(it('u'), op('2')) + MINUS +
         frac(sub(it('Q'), op('0')), sub(delim(rho() + sub(it('C'), it('p'))), up('thnf'))) +
         delim(it('T') + MINUS + sub(it('T'), op('2'))))

E[19] = (sub(it('q'), it('r')) + EQ + MINUS +
         frac(op('4') + sup(sig(), op('*')), op('3') + sup(it('k'), op('*'))) +
         pd(sup(it('T'), op('4')), it('z')))

E[20] = (sub(it('q'), it('r')) + EQ + MINUS +
         frac(op('16') + sup(sig(), op('*')), op('3') + sup(it('k'), op('*'))) +
         sup(it('T'), op('3')) + pd(it('T'), it('z')))

E[21] = (sup(it('T'), op('4')) + op(G['approx']) + op('4') + sub(sup(it('T'), op('3')), op('2')) +
         it('T') + MINUS + op('3') + sub(sup(it('T'), op('4')), op('2')))

E[22] = (pd(it('C'), it('t')) + PLUS + it('u') + pd(it('C'), it('r')) + PLUS + it('w') +
         pd(it('C'), it('z')) + EQ + it('D') +
         delim(pd(it('C'), it('r'), 2) + frac(op('1'), it('r')) + pd(it('C'), it('r')) + PLUS +
               pd(it('C'), it('z'), 2), '[', ']') + PLUS +
         frac(it('D') + sub(it('K'), it('T')), sub(it('T'), it('m'))) +
         delim(pd(it('T'), it('r'), 2) + frac(op('1'), it('r')) + pd(it('T'), it('r')) + PLUS +
               pd(it('T'), it('z'), 2), '[', ']') + MINUS + sub(it('k'), op('1')) +
         delim(it('C') + MINUS + sub(it('C'), op('2'))))

E[23] = (it('u') + EQ + sub(it('L'), op('1')) + sub(mu(), up('thnf')) + pd(it('u'), it('z')) +
         op(',') + op('&#160;') + it('w') + EQ + MINUS +
         frac(sub(it('w'), op('0')), rad(op('1') + MINUS + it('b') + it('t'))) + PLUS +
         sub(it('L'), op('1')) + sub(mu(), up('thnf')) + pd(it('w'), it('z')) + op(',') +
         op('&#160;') + sub(kap(), up('thnf')) + pd(it('T'), it('z')) + EQ +
         sub(it('h'), up('f1')) + delim(it('T') + MINUS + sub(it('T'), op('1'))) + op(',') +
         op('&#160;') + it('C') + EQ + sub(it('C'), op('1')) + PLUS + sub(it('L'), it('c')) +
         pd(it('C'), it('z')) + op('&#160;&#160;') + up('at') + op('&#160;') + it('z') + EQ + op('0'))

E[24] = (it('u') + EQ + op('0') + op(',') + op('&#160;') + it('w') + EQ +
         frac(R('d') + it('h'), R('d') + it('t')) + op(',') + op('&#160;') +
         sub(kap(), up('thnf')) + pd(it('T'), it('z')) + EQ + MINUS + sub(it('h'), up('f2')) +
         delim(it('T') + MINUS + sub(it('T'), op('2'))) + op(',') + op('&#160;') + it('C') + EQ +
         sub(it('C'), op('2')) + op('&#160;&#160;') + up('at') + op('&#160;') + it('z') + EQ +
         it('h') + delim(it('t')))

E[25] = (sub(mu(), up('thnf')) + EQ +
         frac(sub(mu(), up('nf1')) + sub(phi(), op('1')) + PLUS + sub(mu(), up('nf2')) +
              sub(phi(), op('2')) + PLUS + sub(mu(), up('nf3')) + sub(phi(), op('3')), phi()) +
         op(',') + op('&#160;') + phi() + EQ + sub(phi(), op('1')) + PLUS + sub(phi(), op('2')) +
         PLUS + sub(phi(), op('3')))

E[26] = (sub(mu(), up('nf1')) + EQ + sub(mu(), it('f')) +
         delim(op('1') + PLUS + op('1.9') + phi() + PLUS + op('471.4') + sup(phi(), op('2'))))

E[27] = (sub(mu(), up('nf2')) + EQ + sub(mu(), it('f')) +
         delim(op('1') + PLUS + op('14.6') + phi() + PLUS + op('123.3') + sup(phi(), op('2'))))

E[28] = (sub(mu(), up('nf3')) + EQ + sub(mu(), it('f')) +
         delim(op('1') + PLUS + op('37.1') + phi() + PLUS + op('612.6') + sup(phi(), op('2'))))

E[29] = (sub(rho(), up('thnf')) + EQ + sub(phi(), op('1')) + sub(rho(), up('s1')) + PLUS +
         sub(phi(), op('2')) + sub(rho(), up('s2')) + PLUS + sub(phi(), op('3')) +
         sub(rho(), up('s3')) + PLUS +
         delim(op('1') + MINUS + sub(phi(), op('1')) + MINUS + sub(phi(), op('2')) + MINUS +
               sub(phi(), op('3'))) + sub(rho(), it('f')))

def rCp(sfx): return sub(delim(rho() + sub(it('C'), it('p'))), sfx)
E[30] = (rCp(up('thnf')) + EQ + sub(phi(), op('1')) + rCp(up('s1')) + PLUS + sub(phi(), op('2')) +
         rCp(up('s2')) + PLUS + sub(phi(), op('3')) + rCp(up('s3')) + PLUS +
         delim(op('1') + MINUS + sub(phi(), op('1')) + MINUS + sub(phi(), op('2')) + MINUS +
               sub(phi(), op('3'))) + rCp(it('f')))

def maxwell(sig_in, sig_s, p):
    num = sig_s + delim(op('1') + PLUS + op('2') + p) + PLUS + op('2') + sig_in + delim(op('1') + MINUS + p)
    den = sig_s + delim(op('1') + MINUS + p) + PLUS + sig_in + delim(op('2') + PLUS + p)
    return frac(num, den)

E[31] = (sub(sig(), up('bf')) + EQ + sub(sig(), it('f')) +
         delim(maxwell(sub(sig(), it('f')), sub(sig(), up('s1')), sub(phi(), op('1'))), '[', ']'))
E[32] = (sub(sig(), up('hnf')) + EQ + sub(sig(), up('bf')) +
         delim(maxwell(sub(sig(), up('bf')), sub(sig(), up('s2')), sub(phi(), op('2'))), '[', ']'))
E[33] = (sub(sig(), up('thnf')) + EQ + sub(sig(), up('hnf')) +
         delim(maxwell(sub(sig(), up('hnf')), sub(sig(), up('s3')), sub(phi(), op('3'))), '[', ']'))

E[34] = (sub(kap(), up('thnf')) + EQ +
         frac(sub(phi(), op('1')) + sub(kap(), up('nf1')) + PLUS + sub(phi(), op('2')) +
              sub(kap(), up('nf2')) + PLUS + sub(phi(), op('3')) + sub(kap(), up('nf3')), phi()))

def hc(ks):
    num = ks + delim(it('m') + MINUS + op('1')) + sub(kap(), it('f')) + MINUS + \
          delim(it('m') + MINUS + op('1')) + phi() + delim(sub(kap(), it('f')) + MINUS + ks)
    den = ks + delim(it('m') + MINUS + op('1')) + sub(kap(), it('f')) + PLUS + \
          phi() + delim(sub(kap(), it('f')) + MINUS + ks)
    return frac(num, den)

E[35] = (sub(kap(), up('nf1')) + EQ + sub(kap(), it('f')) + delim(hc(sub(kap(), up('s1'))), '[', ']') +
         op(',') + op('&#160;') + it('m') + EQ + op('3.7'))
E[36] = (sub(kap(), up('nf2')) + EQ + sub(kap(), it('f')) + delim(hc(sub(kap(), up('s2'))), '[', ']') +
         op(',') + op('&#160;') + it('m') + EQ + op('8.6'))
E[37] = (sub(kap(), up('nf3')) + EQ + sub(kap(), it('f')) + delim(hc(sub(kap(), up('s3'))), '[', ']') +
         op(',') + op('&#160;') + it('m') + EQ + op('5.7'))

E[38] = (sub(it('A'), op('1')) + EQ + frac(sub(mu(), up('thnf')), sub(mu(), it('f'))) + op(',') +
         op('&#160;') + sub(it('A'), op('2')) + EQ + frac(sub(rho(), up('thnf')), sub(rho(), it('f'))) +
         op(',') + op('&#160;') + sub(it('A'), op('3')) + EQ +
         frac(sub(sig(), up('thnf')), sub(sig(), it('f'))) + op(',') + op('&#160;') +
         sub(it('A'), op('4')) + EQ + frac(sub(kap(), up('thnf')), sub(kap(), it('f'))) + op(',') +
         op('&#160;') + sub(it('A'), op('5')) + EQ + frac(rCp(up('thnf')), rCp(it('f'))))

E[39] = (et() + EQ + frac(it('z'), it('H') + rad(op('1') + MINUS + it('b') + it('t'))))
E[40] = (it('u') + EQ + frac(it('b') + it('r'), op('2') + delim(op('1') + MINUS + it('b') + it('t'))) +
         sup(it('f'), R(G['prime'])) + delim(et()))
E[41] = (it('w') + EQ + MINUS + frac(it('b') + it('H'), rad(op('1') + MINUS + it('b') + it('t'))) +
         it('f') + delim(et()))
E[42] = (th() + delim(et()) + EQ + frac(it('T') + MINUS + sub(it('T'), op('2')),
                                        sub(it('T'), op('1')) + MINUS + sub(it('T'), op('2'))))
E[43] = (Phi() + delim(et()) + EQ + frac(it('C') + MINUS + sub(it('C'), op('2')),
                                         sub(it('C'), op('1')) + MINUS + sub(it('C'), op('2'))))
E[44] = (it('T') + EQ + sub(it('T'), op('1')) + delim(th() + delim(sub(R(G['theta']), it('r')) +
         MINUS + op('1')) + PLUS + op('1')) + op(',') + op('&#160;') +
         sub(R(G['theta']), it('r')) + EQ + frac(sub(it('T'), op('1')), sub(it('T'), op('2'))))

E[45] = (up('Sq') + EQ + frac(it('b') + sup(it('H'), op('2')), op('2') + sub(nu(), it('f'))))
E[46] = (bet() + EQ + frac(sub(R(G['delta']), op('1')) + it('b'),
                           op('2') + delim(op('1') + MINUS + it('b') + it('t')) + sub(mu(), it('f'))))
E[47] = (up('Fr') + EQ + frac(sub(it('C'), it('b')) + it('r'), rad(sub(sup(it('K'), op('*')), it('p')))))
E[48] = (up('Kp') + EQ + frac(sup(it('H'), op('2')) + delim(op('1') + MINUS + it('b') + it('t')),
                              sub(sup(it('K'), op('*')), it('p'))))
E[49] = (it('M') + EQ + frac(sub(sig(), it('f')) + sub(sup(it('B'), op('2')), op('0')) +
         sup(it('H'), op('2')), sub(mu(), it('f'))))
E[50] = (up('Pr') + EQ + frac(sub(mu(), it('f')) + sub(delim(sub(it('C'), it('p'))), it('f')),
                              sub(kap(), it('f'))))
E[51] = (up('Ec') + EQ + frac(sup(it('b'), op('2')) + sup(it('r'), op('2')),
         op('4') + sup(delim(op('1') + MINUS + it('b') + it('t')), op('2')) +
         sub(delim(sub(it('C'), it('p'))), it('f')) + delim(sub(it('T'), op('1')) + MINUS +
         sub(it('T'), op('2')))))
E[52] = (up('Hs') + EQ + frac(op('2') + sub(it('Q'), op('0')) + delim(op('1') + MINUS + it('b') + it('t')),
         it('b') + rCp(it('f'))))
E[53] = (up('Rd') + EQ + frac(op('4') + sup(sig(), op('*')) + sub(sup(it('T'), op('3')), op('2')),
         sup(it('k'), op('*')) + sub(kap(), it('f'))))
E[54] = (up('Df') + EQ + frac(it('D') + sub(it('K'), it('T')) + delim(sub(it('C'), op('1')) + MINUS +
         sub(it('C'), op('2'))), sub(it('C'), it('s')) + sub(delim(sub(it('C'), it('p'))), it('f')) +
         sub(nu(), it('f')) + delim(sub(it('T'), op('1')) + MINUS + sub(it('T'), op('2')))))
E[55] = (up('Sc') + EQ + frac(sub(nu(), it('f')), it('D')))
E[56] = (up('Sr') + EQ + frac(it('D') + sub(it('K'), it('T')) + delim(sub(it('T'), op('1')) + MINUS +
         sub(it('T'), op('2'))), sub(it('T'), it('m')) + sub(nu(), it('f')) +
         delim(sub(it('C'), op('1')) + MINUS + sub(it('C'), op('2')))))
E[57] = (it('K') + EQ + frac(sub(it('k'), op('1')) + delim(op('1') + MINUS + it('b') + it('t')) +
         sup(it('H'), op('2')), sub(nu(), it('f'))))
E[58] = (sub(gam(), it('T')) + EQ + frac(sub(lam(), it('T')) + it('b'),
         op('2') + delim(op('1') + MINUS + it('b') + it('t'))))
E[59] = (sub(up('Bi'), op('1')) + EQ + frac(sub(it('h'), up('f1')) + it('H') +
         rad(op('1') + MINUS + it('b') + it('t')), sub(kap(), it('f'))) + op(',') + op('&#160;') +
         sub(up('Bi'), op('2')) + EQ + frac(sub(it('h'), up('f2')) + it('H') +
         rad(op('1') + MINUS + it('b') + it('t')), sub(kap(), it('f'))))
E[60] = (it('S') + EQ + frac(sub(it('w'), op('0')), it('b') + it('H')))

# ---- Reduced ODE system ----
def fp(n=1):
    return sup(it('f'), R(G['prime']*0) + ("".join([G['prime']]*n)))
# simpler primes
def fprime(k):
    return it('f') + R(G['prime']*k) if False else sup(it('f'), op("".join(["&#8242;"]*k)))

E[61] = (frac(sub(it('A'), op('1')), sub(it('A'), op('2'))) + fprime(4) + MINUS + up('Sq') +
         delim(op('3') + fprime(2) + MINUS + op('2') + it('f') + fprime(3) + PLUS + et() + fprime(3)) +
         PLUS + frac(bet(), op('2') + sub(it('A'), op('2'))) + sup(sub(R('D'), R('t')), al()) +
         delim(op('5') + fprime(4) + MINUS + op('2') + it('f') + fprime(5) + PLUS + et() + fprime(5), '[', ']') +
         MINUS + op('2') + up('Fr') + up('Sq') + fprime(1) + fprime(2) + MINUS +
         frac(sub(it('A'), op('1')), sub(it('A'), op('2'))) + up('Kp') + fprime(2) + MINUS +
         frac(sub(it('A'), op('3')), sub(it('A'), op('2'))) + it('M') + fprime(2) + EQ + op('0'))

E[62] = (sup(sub(R('D'), R('t')), al()) + delim(it('G') + delim(et()) + R(G['tau']) + delim(it('t')), '[', ']') +
         EQ + it('G') + delim(et()) + sup(sub(R('D'), R('t')), al()) + R(G['tau']) + delim(it('t')))

E[63] = (sub(it('N'), up('mem')) + delim(et() + op(',') + it('t')) + EQ +
         frac(op('1'), op('1') + MINUS + al() + delim(et() + op(',') + it('t'))) +
         nary(G['integral'], op('0'), it('t'),
              sup(R(G['tau']), R(G['prime'])) + delim(it('s')) +
              txt('exp') + delim(MINUS + frac(al() + delim(et() + op(',') + it('t')) +
                                              delim(it('t') + MINUS + it('s')),
                                              op('1') + MINUS + al() + delim(et() + op(',') + it('t'))), '[', ']') +
              R('d') + it('s')))

E[64] = (delim(sub(it('A'), op('4')) + frac(op('4'), op('3')) + up('Rd') +
         sup(delim(op('1') + PLUS + th() + delim(sub(R(G['theta']), it('r')) + MINUS + op('1'))), op('3'))) +
         sup(th(), op('&#8242;&#8242;')) + PLUS + up('Pr') +
         delim(sub(it('A'), op('3')) + it('M') + up('Ec') + sup(fprime(1), op('2')) + PLUS + up('Df') +
               sub(it('A'), op('2')) + sup(Phi(), op('&#8242;&#8242;')) + MINUS + up('Sq') + up('Hs') + th()) +
         PLUS + sub(it('A'), op('5')) + up('Sq') + up('Pr') +
         delim(op('2') + it('f') + sup(th(), op('&#8242;')) + MINUS + et() + sup(th(), op('&#8242;'))) +
         PLUS + op('4') + up('Rd') +
         sup(delim(op('1') + PLUS + th() + delim(sub(R(G['theta']), it('r')) + MINUS + op('1'))), op('2')) +
         delim(sub(R(G['theta']), it('r')) + MINUS + op('1')) + sup(th(), op('&#8242;2')) + MINUS +
         sub(gam(), it('T')) + sub(it('N'), up('mem')) + up('Pr') + sub(it('A'), op('5')) +
         sup(delim(up('Sq') + delim(op('2') + it('f') + sup(th(), op('&#8242;')) + MINUS + et() +
             sup(th(), op('&#8242;')))), op('&#8242;')) + EQ + op('0'))

E[65] = (sup(Phi(), op('&#8242;&#8242;')) + PLUS + up('Sr') + up('Sc') + sup(th(), op('&#8242;&#8242;')) +
         MINUS + it('K') + up('Sc') + Phi() + PLUS + up('Sc') + up('Sq') +
         delim(op('2') + it('f') + sup(Phi(), op('&#8242;')) + MINUS + et() + sup(Phi(), op('&#8242;'))) +
         EQ + op('0'))

E[66] = (fprime(1) + EQ + sub(it('A'), op('1')) + sub(it('H'), it('f')) + fprime(2) + op(',') +
         op('&#160;') + it('f') + EQ + it('S') + PLUS + sub(it('A'), op('1')) + sub(it('H'), it('f')) +
         fprime(1) + op(',') + op('&#160;') + sub(it('A'), op('4')) + sup(th(), op('&#8242;')) + EQ +
         sub(up('Bi'), op('1')) + delim(th() + MINUS + op('1')) + op(',') + op('&#160;') + Phi() + EQ +
         op('1') + PLUS + sub(it('H'), it('c')) + sup(Phi(), op('&#8242;')) + op('&#160;&#160;') +
         up('at') + op('&#160;') + et() + EQ + op('0'))

E[67] = (fprime(1) + EQ + op('0') + op(',') + op('&#160;') + it('f') + EQ + frac(op('1'), op('2')) +
         op(',') + op('&#160;') + sub(it('A'), op('4')) + sup(th(), op('&#8242;')) + EQ + MINUS +
         sub(up('Bi'), op('2')) + th() + op(',') + op('&#160;') + Phi() + EQ + op('0') +
         op('&#160;&#160;') + up('at') + op('&#160;') + et() + EQ + op('1'))

# ---- Engineering quantities ----
E[68] = (sub(it('C'), it('f')) + EQ +
         frac(sub(R(G['tau']), up('rz')),
              sub(rho(), it('f')) + sup(delim(MINUS + frac(it('b') + it('H'),
                  op('2') + rad(op('1') + MINUS + it('b') + it('t')))), op('2'))))
E[69] = (sub(R(G['tau']), up('rz')) + EQ + sub(mu(), up('thnf')) +
         delim(pd(it('u'), it('z')) + pd(it('w'), it('r'))) + PLUS + sub(R(G['delta']), op('1')) +
         sup(sub(R('D'), R('t')), al()) +
         delim(frac(sup(d_(), op('2')) + it('u'), d_() + it('z') + d_() + it('t')) + it('u') +
               frac(sup(d_(), op('2')) + it('u'), d_() + it('r') + d_() + it('z')) + PLUS + it('w') +
               pd(it('u'), it('z'), 2), '[', ']'))
E[70] = (sub(it('C'), up('f1')) + frac(sup(it('H'), op('2')), sup(it('r'), op('2'))) + up('Re') + EQ +
         delim(sub(it('A'), op('1')) + frac(op('3'), op('2')) + bet() + sub(it('N'), up('mem'))) +
         fprime(2) + delim(op('0')) + MINUS + bet() + sub(it('N'), up('mem')) + it('S') + fprime(3) +
         delim(op('0')))
E[71] = (sub(it('C'), up('f2')) + frac(sup(it('H'), op('2')), sup(it('r'), op('2'))) + up('Re') + EQ +
         delim(sub(it('A'), op('1')) + frac(op('3'), op('2')) + bet() + sub(it('N'), up('mem'))) +
         fprime(2) + delim(op('1')))
E[72] = (up('Re') + EQ + frac(it('b') + it('r') + it('H'),
         op('2') + sub(nu(), it('f')) + rad(op('1') + MINUS + it('b') + it('t'))))
E[73] = (up('Nu') + rad(op('1') + MINUS + it('b') + it('t')) + EQ + MINUS +
         delim(sub(it('A'), op('4')) + frac(op('4'), op('3')) + up('Rd') +
               sup(delim(op('1') + PLUS + th() + delim(sub(R(G['theta']), it('r')) + MINUS + op('1'))), op('3'))) +
         sup(th(), op('&#8242;')) + delim(et()))
E[74] = (up('Sh') + rad(op('1') + MINUS + it('b') + it('t')) + EQ + MINUS +
         sup(Phi(), op('&#8242;')) + delim(et()))
E[75] = (sub(it('q'), it('w')) + EQ + MINUS + sub(kap(), up('thnf')) + delim(pd(it('T'), it('z'))) +
         PLUS + sub(it('q'), it('r')))
E[76] = (sub(it('q'), it('m')) + EQ + MINUS + it('D') + delim(pd(it('C'), it('z'))))

# ---- Algorithm ----
E[77] = (sub(lam(), it('n')) + EQ + frac(sub(al(), it('n')), op('1') + MINUS + sub(al(), it('n'))))
E[78] = (sup(sub(R('D'), R('t')), sub(al(), it('n'))) + it('g') + op('|') + sub(R(''), sub(it('t'), it('n'))) +
         EQ + nary(G['sum'], R('k=1'), it('n'),
                   sub(it('w'), up('n,k')) +
                   frac(delim(it('g') + delim(sub(it('t'), it('k'))) + MINUS + it('g') +
                        delim(sub(it('t'), up('k-1')))), R('d') + it('t'))))
E[79] = (sub(it('w'), up('n,k')) + EQ + frac(op('1'), op('1') + MINUS + sub(al(), it('n'))) +
         nary(G['integral'], sub(it('t'), up('k-1')), sub(it('t'), it('k')),
              txt('exp') + delim(MINUS + sub(lam(), it('n')) + delim(sub(it('t'), it('n')) + MINUS + it('s')), '[', ']') +
              R('d') + it('s')) + EQ + frac(op('1'), sub(al(), it('n'))) +
         delim(txt('exp') + delim(MINUS + sub(lam(), it('n')) + delim(sub(it('t'), it('n')) + MINUS +
               sub(it('t'), it('k')))) + MINUS + txt('exp') + delim(MINUS + sub(lam(), it('n')) +
               delim(sub(it('t'), it('n')) + MINUS + sub(it('t'), up('k-1')))), '[', ']'))
E[80] = (sub(it('w'), up('n,n')) + EQ + frac(op('1'), sub(al(), it('n'))) +
         delim(op('1') + MINUS + txt('exp') + delim(MINUS + sub(lam(), it('n')) + R('d') + it('t')), '[', ']'))
E[81] = (sup(sub(R('D'), R('t')), sub(al(), it('n'))) + it('g') + op('|') + sub(R(''), sub(it('t'), it('n'))) +
         EQ + sub(it('w'), up('n,n')) + frac(delim(it('g') + delim(sub(it('t'), it('n'))) + MINUS +
         it('g') + delim(sub(it('t'), up('n-1')))), R('d') + it('t')) + PLUS +
         sub(it('H'), it('n')) + delim(it('g'), '[', ']'))
E[82] = (sub(it('H'), it('n')) + delim(it('g'), '[', ']') + EQ +
         nary(G['sum'], R('k=1'), R('n-1'), sub(it('w'), up('n,k')) +
              frac(delim(it('g') + delim(sub(it('t'), it('k'))) + MINUS + it('g') +
                   delim(sub(it('t'), up('k-1')))), R('d') + it('t'))))
E[83] = (sub(it('H'), it('n')) + delim(it('g'), '[', ']') + EQ +
         txt('exp') + delim(MINUS + sub(lam(), it('n')) + R('d') + it('t')) + sub(it('H'), up('n-1')) +
         delim(it('g'), '[', ']') + PLUS + up('correction'))
E[84] = (sub(et(), it('j')) + EQ + frac(op('1'), op('2')) +
         delim(op('1') + MINUS + txt('cos') + delim(frac(it('j') + R(G['pi']), sub(it('N'), it('x'))))) +
         op(',') + op('&#160;') + it('j') + EQ + op('0,1,') + op('&#8230;') + op(',') + sub(it('N'), it('x')))
E[85] = (frac(R('d'), R('d') + et()) + op('&#8594;') + op('2') + it('D') + op(',') + op('&#160;') +
         frac(sup(R('d'), op('2')), R('d') + sup(et(), op('2'))) + op('&#8594;') +
         sup(delim(op('2') + it('D')), op('2')) + op(',') + op('&#160;') +
         frac(sup(R('d'), op('4')), R('d') + sup(et(), op('4'))) + op('&#8594;') +
         sup(delim(op('2') + it('D')), op('4')))
E[86] = (sub(it('D'), up('00')) + EQ + frac(op('2') + sub(sup(it('N'), op('2')), it('x')) + PLUS + op('1'), op('6')) +
         op(',') + op('&#160;') + sub(it('D'), up('NxNx')) + EQ + MINUS +
         frac(op('2') + sub(sup(it('N'), op('2')), it('x')) + PLUS + op('1'), op('6')))
E[87] = (sub(it('D'), up('jj')) + EQ + MINUS + frac(sub(it('x'), it('j')),
         op('2') + delim(op('1') + MINUS + sub(sup(it('x'), op('2')), it('j')))))
E[88] = (sub(it('D'), up('ij')) + EQ + frac(sub(it('c'), it('i')), sub(it('c'), it('j'))) +
         frac(sup(delim(MINUS + op('1')), up('i+j')), sub(it('x'), it('i')) + MINUS + sub(it('x'), it('j'))) +
         op(',') + op('&#160;') + it('i') + op('&#8800;') + it('j'))
E[89] = (it('U') + EQ + delim(sub(it('f'), op('0')) + op(',') + op('&#8230;') + op(',') +
         sub(it('f'), sub(it('N'), it('x'))) + op(',') + sub(th(), op('0')) + op(',') + op('&#8230;') +
         op(',') + sub(th(), sub(it('N'), it('x'))) + op(',') + sub(Phi(), op('0')) + op(',') +
         op('&#8230;') + op(',') + sub(Phi(), sub(it('N'), it('x')))) + sup(R(''), it('T')))
# 90-92 residuals (compact)
E[90] = (sub(sup(it('R'), it('f')), it('j')) + EQ + frac(sub(it('A'), op('1')), sub(it('A'), op('2'))) +
         sup(delim(op('2') + it('D')), op('4')) + it('f') + MINUS + up('Sq') +
         delim(op('3') + fprime(2) + MINUS + op('2') + it('f') + fprime(3) + PLUS + et() + fprime(3)) +
         PLUS + up('elastic') + MINUS + op('2') + up('Fr') + up('Sq') + fprime(1) + fprime(2) + MINUS +
         frac(sub(it('A'), op('1')), sub(it('A'), op('2'))) + up('Kp') + fprime(2) + MINUS +
         frac(sub(it('A'), op('3')), sub(it('A'), op('2'))) + it('M') + fprime(2))
E[91] = (sub(sup(it('R'), R(G['theta'])), it('j')) + EQ +
         delim(sub(it('A'), op('4')) + frac(op('4'), op('3')) + up('Rd') +
               sup(delim(op('1') + PLUS + th() + delim(sub(R(G['theta']), it('r')) + MINUS + op('1'))), op('3'))) +
         sup(delim(op('2') + it('D')), op('2')) + th() + PLUS + up('Pr') +
         delim(sub(it('A'), op('3')) + it('M') + up('Ec') + sup(fprime(1), op('2')) + PLUS + up('Df') +
               sub(it('A'), op('2')) + sup(delim(op('2') + it('D')), op('2')) + Phi() + MINUS + up('Sq') +
               up('Hs') + th()) + PLUS + up('Cattaneo'))
E[92] = (sub(sup(it('R'), R(G['Phi'])), it('j')) + EQ + sup(delim(op('2') + it('D')), op('2')) + Phi() +
         PLUS + up('Sr') + up('Sc') + sup(delim(op('2') + it('D')), op('2')) + th() + MINUS + it('K') +
         up('Sc') + Phi() + PLUS + up('Sc') + up('Sq') +
         delim(op('2') + it('f') + delim(op('2') + it('D')) + Phi() + MINUS + et() + delim(op('2') + it('D')) + Phi()))
E[93] = (it('J') + delim(sup(it('U'), up('(s)'))) + R(G['delta']) + it('U') + EQ + MINUS + it('R') +
         delim(sup(it('U'), up('(s)'))) + op(',') + op('&#160;&#160;') + sup(it('U'), up('(s+1)')) + EQ +
         sup(it('U'), up('(s)')) + PLUS + R(G['delta']) + it('U'))
E[94] = (it('J') + EQ + frac(R('d') + it('R'), R('d') + it('U')))
E[95] = (frac(R('d'), R('d') + it('f')) + delim(it('f') + sup(delim(op('2') + it('D')), op('3')) + it('f'), '[', ']') +
         EQ + up('diag') + delim(sup(delim(op('2') + it('D')), op('3')) + it('f')) + PLUS +
         up('diag') + delim(it('f')) + sup(delim(op('2') + it('D')), op('3')))
E[96] = (frac(R('d'), R('d') + it('f')) + delim(it('f') + delim(op('2') + it('D')) + th(), '[', ']') +
         EQ + up('diag') + delim(delim(op('2') + it('D')) + th()))
E[97] = (frac(R('d'), R('d') + th()) + delim(it('f') + delim(op('2') + it('D')) + th(), '[', ']') + EQ +
         up('diag') + delim(it('f')) + delim(op('2') + it('D')))
E[98] = (frac(R('d'), R('d') + Phi()) + delim(it('f') + delim(op('2') + it('D')) + Phi(), '[', ']') + EQ +
         up('diag') + delim(it('f')) + delim(op('2') + it('D')))
E[99] = (frac(R('d'), R('d') + th()) + delim(delim(sub(it('A'), op('4')) + frac(op('4'), op('3')) + up('Rd') +
         sup(delim(op('1') + PLUS + th() + delim(sub(R(G['theta']), it('r')) + MINUS + op('1'))), op('3'))) +
         sup(delim(op('2') + it('D')), op('2')) + th(), '[', ']') + EQ +
         delim(sub(it('A'), op('4')) + frac(op('4'), op('3')) + up('Rd') +
               sup(delim(op('1') + PLUS + th() + delim(sub(R(G['theta']), it('r')) + MINUS + op('1'))), op('3'))) +
         sup(delim(op('2') + it('D')), op('2')) + PLUS + op('4') + up('Rd') +
         delim(sub(R(G['theta']), it('r')) + MINUS + op('1')) + up('diag') +
         delim(sup(delim(op('1') + PLUS + th() + delim(sub(R(G['theta']), it('r')) + MINUS + op('1'))), op('2'))) +
         up('diag') + delim(sup(delim(op('2') + it('D')), op('2')) + th()))

E[100] = (delim(op('2') + it('D')) + it('f') + op('|') + sub(R(''), op('0')) + MINUS + sub(it('A'), op('1')) +
          sub(it('H'), it('f')) + sup(delim(op('2') + it('D')), op('2')) + it('f') + op('|') +
          sub(R(''), op('0')) + EQ + op('0'))
E[101] = (sub(it('f'), op('0')) + MINUS + it('S') + MINUS + sub(it('A'), op('1')) + sub(it('H'), it('f')) +
          delim(op('2') + it('D')) + it('f') + op('|') + sub(R(''), op('0')) + EQ + op('0'))
E[102] = (sub(it('A'), op('4')) + delim(op('2') + it('D')) + th() + op('|') + sub(R(''), op('0')) + MINUS +
          sub(up('Bi'), op('1')) + delim(sub(th(), op('0')) + MINUS + op('1')) + EQ + op('0'))
E[103] = (sub(Phi(), op('0')) + MINUS + op('1') + MINUS + sub(it('H'), it('c')) + delim(op('2') + it('D')) +
          Phi() + op('|') + sub(R(''), op('0')) + EQ + op('0'))
E[104] = (delim(op('2') + it('D')) + it('f') + op('|') + sub(R(''), sub(it('N'), it('x'))) + EQ + op('0'))
E[105] = (sub(it('f'), sub(it('N'), it('x'))) + MINUS + frac(op('1'), op('2')) + EQ + op('0'))
E[106] = (sub(it('A'), op('4')) + delim(op('2') + it('D')) + th() + op('|') + sub(R(''), sub(it('N'), it('x'))) +
          PLUS + sub(up('Bi'), op('2')) + sub(th(), sub(it('N'), it('x'))) + EQ + op('0'))
E[107] = (sub(Phi(), sub(it('N'), it('x'))) + EQ + op('0'))

# 108-118 algorithm steps (as short math/text lines)
E[108] = (up('Initialise ') + sup(it('U'), op('0')) + up(' at ') + sub(it('t'), op('0')) +
          up(' from OHAM benchmark.'))
E[109] = (up('Set frozen orders ') + sub(al(), it('n')) + delim(sub(et(), it('j'))) + up(' from (10)-(11).'))
E[110] = (up('Evaluate ') + sub(it('w'), up('n,n')) + up(' from (80) and history ') + sub(it('H'), it('n')) +
          up(' from (82)-(83).'))
E[111] = (sup(it('U'), up('(0)')) + EQ + sup(it('U'), up('n-1')))
E[112] = (up('Assemble ') + it('R') + delim(sup(it('U'), up('(s)'))) + up(' from (90)-(92).'))
E[113] = (up('Assemble ') + it('J') + up(' from (94)-(99).'))
E[114] = (up('Solve ') + it('J') + R(G['delta']) + it('U') + EQ + MINUS + it('R') + up(' by LU.'))
E[115] = (sup(it('U'), up('(s+1)')) + EQ + sup(it('U'), up('(s)')) + PLUS + R(G['delta']) + it('U'))
E[116] = (up('Test ') + op('&#8214;') + R(G['delta']) + it('U') + op('&#8214;') + op('&#8734;') + up(' convergence.'))
E[117] = (op('&#8214;') + R(G['delta']) + it('U') + op('&#8214;') + sub(R(''), op('&#8734;')) + op('&lt;') +
          sub(R(G['epsilon']) if 'epsilon' in G else R('&#949;'), it('N')) + op(',') + op('&#160;') +
          sub(R('&#949;'), it('N')) + EQ + sup(op('10'), MINUS + op('10')))
E[118] = (up('Store ') + sup(it('U'), it('n')) + up(', update ') + sub(it('H'), it('n')) + op('&#8594;') +
          sub(it('H'), up('n+1')) + up(', advance.'))

E[119] = (sub(it('E'), it('f')) + EQ + frac(op('1'), sub(it('N'), it('x')) + MINUS + op('1')) +
          nary(G['sum'], R('j=1'), R('Nx-1'), sup(delim(sub(sup(it('R'), it('f')), it('j'))), op('2'))))
E[120] = (sub(it('E'), R(G['theta'])) + EQ + frac(op('1'), sub(it('N'), it('x')) + MINUS + op('1')) +
          nary(G['sum'], R('j=1'), R('Nx-1'), sup(delim(sub(sup(it('R'), R(G['theta'])), it('j'))), op('2'))))
E[121] = (sub(it('E'), R(G['Phi'])) + EQ + frac(op('1'), sub(it('N'), it('x')) + MINUS + op('1')) +
          nary(G['sum'], R('j=1'), R('Nx-1'), sup(delim(sub(sup(it('R'), R(G['Phi'])), it('j'))), op('2'))))
E[122] = (op('|') + fprime(2) + delim(op('0')) + op('|') + sub(R(''), sub(it('N'), it('x'))) + MINUS +
          fprime(2) + delim(op('0')) + op('|') + sub(R(''), up('Nx/2')) + op('|') + op('&lt;') +
          sub(R('&#949;'), it('S')) + op(',') + op('&#160;') + sub(R('&#949;'), it('S')) + EQ +
          sup(op('10'), MINUS + op('8')))
E[123] = (op('|') + it('Q') + op('|') + sub(R(''), R('dt')) + MINUS + it('Q') + op('|') + sub(R(''), R('2dt')) +
          op('|') + op('&lt;') + sub(R('&#949;'), it('T')) + op(',') + op('&#160;') + sub(R('&#949;'), it('T')) +
          EQ + sup(op('10'), MINUS + op('6')))
E[124] = (sup(sub(R('D'), R('t')), al()) + sup(it('t'), op('2')) + EQ +
          frac(op('2'), sup(lam(), op('2'))) + delim(lam() + it('t') + MINUS + op('1') + PLUS +
          txt('exp') + delim(MINUS + lam() + it('t')), '[', ']') + op(',') + op('&#160;') + lam() + EQ +
          frac(al(), op('1') + MINUS + al()))
E[125] = (lim_lower(txt('lim'), al() + op('&#8594;') + op('1')) + sub(it('w'), up('n,n')) + EQ + op('1') +
          op(',') + op('&#160;') + lim_lower(txt('lim'), al() + op('&#8594;') + op('1')) +
          sup(sub(R('D'), R('t')), al()) + it('g') + EQ + sup(it('g'), op('&#8242;')))
E[126] = (lim_lower(txt('lim'), sub(gam(), it('T')) + op('&#8594;') + op('0')) +
          delim(op('1') + PLUS + sub(gam(), it('T')) + sup(sub(R('D'), R('t')), al())) + EQ + op('1'))
E[127] = (lim_lower(txt('lim'), bet() + op('&#8594;') + op('0')) +
          delim(frac(sub(it('A'), op('1')), sub(it('A'), op('2'))) + fprime(4) + MINUS + up('Sq') +
                delim(op('3') + fprime(2) + MINUS + op('2') + it('f') + fprime(3) + PLUS + et() + fprime(3)) +
                MINUS + frac(sub(it('A'), op('1')), sub(it('A'), op('2'))) + up('Kp') + fprime(2) + MINUS +
                frac(sub(it('A'), op('3')), sub(it('A'), op('2'))) + it('M') + fprime(2)) + EQ + op('0'))
E[128] = (lim_lower(txt('lim'), al() + op('&#8594;') + op('1')) + sub(it('C'), up('f1')) +
          frac(sup(it('H'), op('2')), sup(it('r'), op('2'))) + up('Re') + EQ +
          delim(sub(it('A'), op('1')) + frac(op('3'), op('2')) + bet()) + fprime(2) + delim(op('0')) +
          MINUS + bet() + it('S') + fprime(3) + delim(op('0')))
E[129] = (lim_lower(txt('lim'), sub(gam(), it('T')) + op('&#8594;') + op('0')) + up('Nu') +
          rad(op('1') + MINUS + it('b') + it('t')) + EQ + MINUS +
          delim(sub(it('A'), op('4')) + frac(op('4'), op('3')) + up('Rd') +
                sup(delim(op('1') + PLUS + th() + delim(sub(R(G['theta']), it('r')) + MINUS + op('1'))), op('3'))) +
          sup(th(), op('&#8242;')) + delim(op('0')))
E[130] = (up('Sh') + rad(op('1') + MINUS + it('b') + it('t')) + EQ + MINUS + sup(Phi(), op('&#8242;')) +
          delim(op('0')))

# add epsilon to G if missing
if 'epsilon' not in G:
    G['epsilon'] = '&#949;'


# ---------- Section headers mapping ----------
SECTIONS = [
    (1, "2.1 Physical configuration"),
    (5, "2.2 Variable-order Caputo-Fabrizio operator"),
    (12, "2.3 Governing balance laws"),
    (17, "2.4 Cattaneo fractional energy equation"),
    (22, "2.5 Concentration equation"),
    (23, "2.6 Boundary conditions"),
    (25, "2.7 Thermophysical properties"),
    (39, "2.8 Similarity transformation"),
    (45, "Dimensionless groups"),
    (61, "2.9 Reduced fractional ODE system"),
    (66, "2.10 Reduced boundary conditions"),
    (68, "3. Engineering quantities"),
    (77, "4.2 Temporal discretization (L1)"),
    (84, "4.3 Chebyshev collocation"),
    (89, "4.4 Residuals and Newton linearisation"),
    (100, "4.5 Boundary-condition rows"),
    (108, "4.6 Time marching and convergence"),
    (125, "4.7 Integer-order and classical limits"),
]


def para(text, bold=False, size=22, center=False):
    t = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    rpr = '<w:rPr>' + ('<w:b/>' if bold else '') + f'<w:sz w:val="{size}"/></w:rPr>'
    jc = '<w:jc w:val="center"/>' if center else ''
    return f'<w:p><w:pPr>{jc}</w:pPr><w:r>{rpr}<w:t xml:space="preserve">{t}</w:t></w:r></w:p>'


def heading(text):
    return (f'<w:p><w:pPr><w:spacing w:before="240" w:after="80"/></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="24"/></w:rPr>'
            f'<w:t xml:space="preserve">{text}</w:t></w:r></w:p>')


def eq_para(num, body):
    """Equation with a right-aligned number via a tab. Uses a 2-cell layout:
    the oMath, then a tab, then (num)."""
    return (f'<w:p><w:pPr><w:tabs><w:tab w:val="right" w:pos="9360"/></w:tabs>'
            f'<w:jc w:val="center"/></w:pPr>'
            f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{body}</m:oMath>'
            f'<w:r><w:tab/><w:t xml:space="preserve">({num})</w:t></w:r></w:p>')


def build():
    body = []
    body.append(para("Equation set: variable-order dual-fractional tri-hybrid nanofluid model",
                     bold=True, size=30, center=True))
    body.append(para("All 130 expressions below are native Word (OMML) equation objects. "
                     "Click any equation to edit it in Word's Equation Editor; copy and paste "
                     "preserves the equation.", size=20, center=True))
    body.append('<w:p/>')

    sec = {n: h for n, h in SECTIONS}
    for i in range(1, 131):
        if i in sec:
            body.append(heading(sec[i]))
        if i in E:
            body.append(eq_para(i, E[i]))
        else:
            body.append(para(f"({i})  [equation]", size=20))

    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<w:body>' + ''.join(body) +
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
        '</w:body></w:document>')

    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')
    word_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '</Relationships>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
        '<w:rPr><w:sz w:val="22"/><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr>'
        '<w:pPr><w:spacing w:after="120"/></w:pPr></w:style></w:styles>')

    out = "/projects/sandbox/AMMAN/Fractional_TriHybrid_Disks_Equations.docx"
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('word/_rels/document.xml.rels', word_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', styles)
    print("Wrote", out)
    return document


if __name__ == "__main__":
    build()
