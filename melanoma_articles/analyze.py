#!/usr/bin/env python3
"""Print the summary statistics quoted in the three articles."""
import json, os, math
from collections import defaultdict

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
L = lambda n: json.load(open(os.path.join(R, n + '.json')))
DET = 0.1


def a1():
    print('=== A1 time course ===')
    d = L('a1_timecourse')
    s, n, q = d['surg'], d['nos'], d['noImm']
    for k in (179, 300, 539, 541, 560, 580, 600, 650, 700, 1000, 1500):
        print(f"t={k:5d} Mp={s['Mp'][k]:.3e} Ms={s['Ms'][k]:.3e} Mm={s['Mm'][k]:.3e} | noSurg Ms={n['Ms'][k]:.3e} Mm={n['Mm'][k]:.3e}")
    tdet = next((k - 540 for k in range(540, len(s['Ms'])) if s['Ms'][k] > DET), None)
    tpr = next((k - 540 for k in range(540, len(s['Ms'])) if s['Ms'][k] > s['Mp'][539]), None)
    print('primary steady mass', s['Mp'][539], 'edge', s['edge_p'][539], 'Rex', s['events'])
    print('detect after surgery', tdet, 'exceed primary', tpr, 'final ratio', s['Ms'][-1] / s['Mp'][539])
    print('immune mass drop', s['Mm'][539], '->', s['Mm'][541])
    print('no immune: Mp at 539', q['Mp'][539], 'Ms', q['Ms'][539], 'final', q['Mp'][-1], q['Ms'][-1])
    # growth rates (doubling time) post-surgery
    import math as m
    k1 = next(k for k in range(541, 1500) if s['Ms'][k] > 1e-3)
    k2 = next(k for k in range(541, 1500) if s['Ms'][k] > 1e-1)
    print('doubling time satellite post-op (1e-3->1e-1)', (k2 - k1) * m.log(2) / m.log(s['Ms'][k2] / s['Ms'][k1]))
    print('=== A1 fate map ===')
    f = L('a1_fatemap')
    by = defaultdict(dict)
    for x in f['fate']:
        by[x['margin']][round(x['r'], 2)] = x
    for mg in f['ms']:
        row = by[mg]
        cls = ''
        for r in f['rs']:
            x = row[round(r, 2)]
            if x['preMs'] > DET: c = 'P'  # escaped before surgery
            elif x['finalMs'] > DET: c = 'R'
            elif x['finalMs'] > 0: c = 'd'
            else: c = '.'
            cls += c
        print(f"margin {mg:4.2f} Rex {row[1.0]['Rex']:.2f} {cls}")
    print('rs', f['rs'][0], f['rs'][-1])
    trs = [x['trec'] for x in f['fate'] if x['trec'] is not None and x['preMs'] < DET]
    print('trec range among recurrences', min(trs), max(trs), 'n', len(trs))
    print('=== A1 timing ===')
    t = L('a1_timing')
    rows = defaultdict(list)
    for x in t['timing']:
        a = x['arm']; rows[(a['key'], a['F'], a['D'])].append(x)
    for k, v in rows.items():
        v.sort(key=lambda x: x['off'])
        print(k, ' '.join(f"{x['off']}:{'E' if x['finalMs'] < 1e-3 else ('%.1f' % x['finalMs'])}" for x in v))
        er = [x['off'] for x in v if x['finalMs'] < 1e-3]
        print('   eradication offsets', (min(er), max(er)) if er else None, 'Ms at start of first eradicating', [ '%.3g' % x['msAtStart'] for x in v if x['finalMs'] < 1e-3][:2])
    for x in t['cont']:
        print('continuous F', x['F'], 'final', x['finalMs'])
    print('=== A1 sens ===')
    s = L('a1_sens')
    g = defaultdict(dict)
    for x in s['sens']:
        g[x['name']][x['kind']] = x
    for n in s['variants']:
        r = g[n]
        print(f"{n:18s} dormantPre={r['nosurg']['preMs']:.2e} nosurgFinal={r['nosurg']['finalMs']:.2e} surgFinal={r['surg']['finalMs']:.2f} trec={r['surg']['trec']} boost0={r['boost0']['finalMs']:.2f} boost120={r['boost120']['finalMs']:.2e}")


def a2():
    print('=== A2 time courses ===')
    d = L('a2_timecourse')
    for tc in d['tcs']:
        te = next((k for k, e in enumerate(tc['Me']) if e > 1), None)
        print('g', tc['g'], 'tesc', te, 'Mp', [round(tc['Mp'][k], 3) for k in (100, 300, 400, 600, 1000, 2000)], 'Mm', [round(tc['Mm'][k], 2) for k in (300, 600, 2000)])
    for p in d['prof']:
        print('profile t', p['t'], 'vmax', round(max(p['v']), 3), 'emax', round(max(p['e']), 3), 'pmax', round(max(p['p']), 3), 'mmax', round(max(p['m']), 3))
    print('=== A2 dormancy ===')
    d = L('a2_dormancy')
    print('gc in', d['lo'], d['hi'])
    xs, ys = [], []
    for x in d['esc']:
        print(x)
        if x['tesc'] is not None:
            xs.append(math.log(x['g'] - d['gc'])); ys.append(math.log(x['tesc']))
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    b = sum((a - mx) * (c - my) for a, c in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)
    print('log-log slope all', b)
    xs2, ys2 = xs[:6], ys[:6]
    mx = sum(xs2) / 6; my = sum(ys2) / 6
    b2 = sum((a - mx) * (c - my) for a, c in zip(xs2, ys2)) / sum((a - mx) ** 2 for a in xs2)
    print('log-log slope near gc (first 6)', b2, 'intercept', math.exp(my - b2 * mx))
    print('=== A2 phase ===')
    p = L('a2_phase')
    for key in ('phase', 'phase2'):
        print(key)
        m = {(round(x['Q'], 3), x['g']): x for x in p[key]}
        for g in reversed(p['Gs']):
            row = ''
            for Q in p['Qs']:
                x = m[(round(Q, 3), g)]
                row += cls2(x)
            print(f"{int(g):5d} {row}")
        print('      ' + ''.join(str(int(round(Q * 100)) % 10) for Q in p['Qs']))
    print('=== A2 anti-VEGF ===')
    a = L('a2_antivegf')
    for x in a['anti']:
        print(f"g={x['g']} f={x['f']} {x['sched']:28s} te0={x['te0']} tesc={x['tesc']} Mp1000={x['Mp1000']:.2f} Mp2000={x['Mp']:.2f} Me={x['Me']:.1f}")


def cls2(x):
    if x['Mp'] < 1e-3: return '.'      # eradicated
    if x['tesc'] is None: return 'c' if x['Mp'] < 2 else 'A'   # controlled / avascular escape
    return 'V' if x['Mp'] < 2 else 'X'  # vascularised but controlled / angiogenic escape


def a3():
    print('=== A3 halo ===')
    h = L('a3_halo')
    m = {(round(x['Q'], 3), round(x['r'], 2)): x for x in h['halo']}
    ms = {(round(x['Q'], 3), round(x['r'], 2)): x for x in h['haloS']}
    for Q in h['Qs']:
        row = ''; row2 = ''
        for r in h['rs']:
            x = m[(round(Q, 3), round(r, 2))]
            row += '.' if x['Ms'] == 0 else ('d' if x['Ms'] < DET else 'E')
            y = ms[(round(Q, 3), round(r, 2))]
            row2 += '.' if y['Ms'] == 0 else ('d' if y['Ms'] < DET else ('P' if y['pre'] > DET else 'R'))
        edge = m[(round(Q, 3), 1.0)]['edge']
        dr = [round(r, 2) for r in h['rs'] if m[(round(Q, 3), round(r, 2))]['Ms'] > 0 and m[(round(Q, 3), round(r, 2))]['Ms'] < DET]
        print(f"Q={Q:.2f} edge={edge:.2f} {row}  dormant band {dr[0] if dr else None}-{dr[-1] if dr else None}")
        print(f"      surg      {row2}")
    print('=== A3 MC ===')
    d = L('a3_mc')
    g = defaultdict(list)
    for x in d['mcr']:
        g[(x['ld'], x['ls'])].append(x)
    for ld in d['LD']:
        for ls in d['LS']:
            v = g[(ld, ls)]
            n = len(v)
            pre = sum(x['pre'] > DET for x in v) / n
            rec = sum(x['fin'] > DET for x in v) / n
            recOnly = sum((x['fin'] > DET and x['pre'] <= DET) for x in v) / n
            ns = sum(x['nseed'] for x in v) / n
            mm = sum(x['meanMm'] for x in v) / n
            pk = sum(x['primPre'] < 1e-3 for x in v) / n
            trs = [x['trec'] for x in v if x['trec'] is not None and x['pre'] <= DET]
            print(f"ld={ld} ls={ls:6} seeds={ns:7.1f} Ppre={pre:.3f} Prec={rec:.3f} PrecFromDormant={recOnly:.3f} meanMm={mm:.2f} primaryLost={pk:.2f} trec_med={sorted(trs)[len(trs)//2] if trs else None}")
    print('=== A3 margin ===')
    d = L('a3_margin')
    g = defaultdict(list)
    for x in d['mgr']:
        g[(x['ld'], x['ls'], x['mg'])].append(x)
    for ld in (2, 4, 8):
        for ls in (0.03, 0.3):
            print(f"ld={ld} ls={ls}", ' '.join(f"m{mg}:{sum(x['fin'] > DET for x in g[(ld, ls, mg)]) / len(g[(ld, ls, mg)]):.2f}" for mg in d['MG']),
                  ' pre:', sum(x['pre'] > DET for x in g[(ld, ls, 0)]) / len(g[(ld, ls, 0)]))
    e = L('a3_example')
    print('example seeds', e['n_seeds'], 'events', e['events'], 'Ms539', e['Ms'][539], 'final', e['Ms'][-1])
    trec = next((k - 540 for k in range(540, len(e['Ms'])) if e['Ms'][k] > DET), None)
    print('example trec', trec)


if __name__ == '__main__':
    a1(); a2(); a3()
