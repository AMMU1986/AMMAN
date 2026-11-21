#!/usr/bin/env node
/*
 * Runs every numerical experiment used in the three articles and writes the
 * results to results/*.json. Usage: node run_experiments.js [a1|a2|a3|all]
 */
'use strict';
const fs = require('fs');
const path = require('path');
const runAll = require('./pool');
const { run } = require('./melanoma_sim');

const RES = path.join(__dirname, 'results');
fs.mkdirSync(RES, { recursive: true });
const save = (name, obj) => { fs.writeFileSync(path.join(RES, name + '.json'), JSON.stringify(obj)); console.log('saved', name); };
const range = (a, b, h) => { const o = []; for (let x = a; x <= b + 1e-9; x += h) o.push(+x.toFixed(6)); return o; };

const DET = 0.1;          // detectable satellite mass (dimensionless)
const T_SURG = 540;       // surgery 18 months after tumour initiation
const SEED_T = 180;       // satellite seeded at 6 months
const BASE_SAT = { T: 1500, fixed_seeds: [{ t: SEED_T, r: 2.0 }], t_surg: T_SURG, margin: 0.5 };

// ---------------------------------------------------------------- Article 1
async function a1() {
  // A1.1 baseline time courses
  const prof = [530, 545, 570, 600, 700];
  const surg = run(Object.assign({}, BASE_SAT, { profiles_at: prof }));
  const nos = run(Object.assign({}, BASE_SAT, { t_surg: null, profiles_at: prof }));
  const noImm = run(Object.assign({}, BASE_SAT, { Q: 0 }));
  save('a1_timecourse', { surg, nos, noImm });

  // A1.2 satellite fate vs seed distance and excision margin
  const rs = range(1.0, 4.0, 0.1), ms = range(0, 3, 0.25);
  const cfgs = [];
  for (const r of rs) for (const mg of ms) cfgs.push(Object.assign({}, BASE_SAT, { fixed_seeds: [{ t: SEED_T, r }], margin: mg }));
  const fate = await runAll(cfgs, function (o, cfg) {
    let trec = null; for (let k = 540; k < o.Ms.length; k++) if (o.Ms[k] > 0.1) { trec = k - 540; break; }
    return { r: cfg.fixed_seeds[0].r, margin: cfg.margin, preMs: o.Ms[539], finalMs: o.Ms[o.Ms.length - 1], trec, Rex: o.events.length ? o.events[0].Rex : null, primFinal: o.Mp[539] };
  });
  save('a1_fatemap', { rs, ms, fate });

  // A1.3 timing of perioperative immunomodulation
  const offs = range(-240, 360, 20);
  const arms = [
    { key: 'Q_boost', F: 1.5, D: 60 }, { key: 'Q_boost', F: 2, D: 60 }, { key: 'Q_boost', F: 3, D: 60 },
    { key: 'Q_boost', F: 5, D: 60 }, { key: 'Q_boost', F: 3, D: 120 }, { key: 'Q_boost', F: 3, D: 30 },
    { key: 'betaK_block', F: 0.25, D: 60 }, { key: 'betaK_block', F: 0.1, D: 120 },
  ];
  const tc = [];
  for (const a of arms) for (const off of offs) { const c = Object.assign({}, BASE_SAT); c[a.key] = [{ start: T_SURG + off, end: T_SURG + off + a.D, factor: a.F }]; c._arm = a; c._off = off; tc.push(c); }
  const timing = await runAll(tc, function (o, cfg) {
    let peak = 0; for (let k = 540; k < o.Ms.length; k++) peak = Math.max(peak, o.Ms[k]);
    const s0 = cfg._off + 540; const msStart = o.Ms[Math.max(0, Math.min(o.Ms.length - 1, Math.round(s0)))];
    return { arm: cfg._arm, off: cfg._off, finalMs: o.Ms[o.Ms.length - 1], peak, msAtStart: msStart };
  });
  // continuous adjuvant from surgery onward (Q x F until end)
  const cont = await runAll([1.25, 1.5, 2, 3].map(F => Object.assign({}, BASE_SAT, { Q_boost: [{ start: 540, end: 1e9, factor: F }], _F: F })),
    function (o, cfg) { return { F: cfg._F, finalMs: o.Ms[o.Ms.length - 1], Ms: o.Ms.filter((_, k) => k % 5 === 0) }; });
  // time courses for representative schedules
  const reps = [['none', {}], ['boost day 0', { Q_boost: [{ start: 540, end: 600, factor: 3 }] }],
    ['boost day +120', { Q_boost: [{ start: 660, end: 720, factor: 3 }] }], ['boost day -120', { Q_boost: [{ start: 420, end: 480, factor: 3 }] }]];
  const repTC = reps.map(([n, x]) => { const o = run(Object.assign({}, BASE_SAT, x)); return { name: n, t: o.t, Ms: o.Ms, Mm: o.Mm }; });
  save('a1_timing', { offs, arms, timing, cont, repTC });

  // A1.4 robustness of the three headline outcomes
  const variants = [['baseline', {}], ['ext_thresh 1e-6', { ext_thresh: 1e-6 }], ['ext_thresh 1e-7', { ext_thresh: 1e-7 }],
    ['r_c 0.25', { r_c: 0.25 }], ['r_c 0.35', { r_c: 0.35 }], ['D_m 0.005', { Dm: 0.005 }], ['D_m 0.02', { Dm: 0.02 }],
    ['chi 0.15', { chi: 0.15 }], ['chi 0.35', { chi: 0.35 }], ['beta_K 0.4', { beta_K: 0.4 }], ['beta_K 0.6', { beta_K: 0.6 }],
    ['dt 0.025', { dt: 0.025 }], ['dr 0.05 mm', { N: 240 }]];
  const sc = [];
  for (const [n, v] of variants) {
    sc.push(Object.assign({}, BASE_SAT, v, { t_surg: null, _n: n, _k: 'nosurg' }));
    sc.push(Object.assign({}, BASE_SAT, v, { _n: n, _k: 'surg' }));
    sc.push(Object.assign({}, BASE_SAT, v, { Q_boost: [{ start: 540, end: 600, factor: 3 }], _n: n, _k: 'boost0' }));
    sc.push(Object.assign({}, BASE_SAT, v, { Q_boost: [{ start: 660, end: 720, factor: 3 }], _n: n, _k: 'boost120' }));
  }
  const sens = await runAll(sc, function (o, cfg) {
    let trec = null; for (let k = 540; k < o.Ms.length; k++) if (o.Ms[k] > 0.1) { trec = k - 540; break; }
    return { name: cfg._n, kind: cfg._k, preMs: o.Ms[539], finalMs: o.Ms[o.Ms.length - 1], primMs: o.Mp[539], trec };
  });
  save('a1_sens', { variants: variants.map(v => v[0]), sens });
}

// ---------------------------------------------------------------- Article 2
async function a2() {
  const tcs = [0, 900, 1000, 1500].map(g => { const o = run({ T: 2000, g_vm: g }); return { g, t: o.t, Mp: o.Mp, Mm: o.Mm, Me: o.Me }; });
  const prof = run({ T: 2000, g_vm: 900, profiles_at: [300, 450, 520, 600] }).profiles;
  save('a2_timecourse', { tcs, prof });

  // escape time near the critical immune-TAF production rate
  const escT = (g) => { const o = run({ T: 4000, g_vm: g }); for (let k = 0; k < o.Me.length; k++) if (o.Me[k] > 1) return k; return null; };
  let lo = 860, hi = 900; while (hi - lo > 0.05) { const mid = 0.5 * (lo + hi); if (escT(mid) === null) lo = mid; else hi = mid; }
  const gc = 0.5 * (lo + hi);
  const gs = [0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 400].map(d => +(hi + d).toFixed(3));
  const esc = await runAll(gs.map(g => ({ T: 4000, g_vm: g })), function (o, cfg) {
    let k0 = null; for (let k = 0; k < o.Me.length; k++) if (o.Me[k] > 1) { k0 = k; break; } return { g: cfg.g_vm, tesc: k0 };
  });
  save('a2_dormancy', { gc, lo, hi, esc });

  // phase diagram: immune recruitment Q x immune TAF production g_vm
  const Qs = range(0.03, 0.15, 0.01), Gs = range(0, 1600, 100);
  const pc = []; for (const Q of Qs) for (const g of Gs) pc.push({ T: 1500, Q, g_vm: g });
  const phase = await runAll(pc, function (o, cfg) {
    let tesc = null; for (let k = 0; k < o.Me.length; k++) if (o.Me[k] > 1) { tesc = k; break; }
    const n = o.Mp.length - 1; return { Q: cfg.Q, g: cfg.g_vm, Mp: o.Mp[n], Me: o.Me[n], tesc };
  });
  // same diagram for weaker constitutive TAF (g_v = 15)
  const pc2 = pc.map(c => Object.assign({}, c, { g_v: 15 }));
  const phase2 = await runAll(pc2, function (o, cfg) {
    let tesc = null; for (let k = 0; k < o.Me.length; k++) if (o.Me[k] > 1) { tesc = k; break; }
    const n = o.Mp.length - 1; return { Q: cfg.Q, g: cfg.g_vm, Mp: o.Mp[n], Me: o.Me[n], tesc };
  });
  save('a2_phase', { Qs, Gs, phase, phase2 });

  // anti-VEGF schedules
  const scheds = [['no therapy', []], ['continuous from day 0', [{ start: 0, end: 1e9 }]],
    ['day 0-180', [{ start: 0, end: 180 }]], ['day 200-380 (dormancy)', [{ start: 200, end: 380 }]],
    ['continuous from day 200', [{ start: 200, end: 1e9 }]], ['from detection (+30 d)', 'detect']];
  const ac = [];
  for (const g of [900, 1000, 1500]) {
    const te = (() => { const o = run({ T: 2000, g_vm: g }); for (let k = 0; k < o.Me.length; k++) if (o.Me[k] > 1) return k; return 0; })();
    for (const f of [0.9, 0.7, 0.5, 0.3]) for (const [n, w] of scheds) {
      const win = w === 'detect' ? [{ start: te + 30, end: 1e9 }] : w;
      ac.push({ T: 2000, g_vm: g, anti_vegf: win.map(x => ({ start: x.start, end: x.end, factor: f })), _n: n, _f: f, _te: te });
    }
  }
  const anti = await runAll(ac, function (o, cfg) {
    let tesc = null; for (let k = 0; k < o.Me.length; k++) if (o.Me[k] > 1) { tesc = k; break; }
    const n = o.Mp.length - 1;
    return { g: cfg.g_vm, f: cfg._f, sched: cfg._n, te0: cfg._te, tesc, Mp: o.Mp[n], Me: o.Me[n], Mp1000: o.Mp[1000], series: o.Mp.filter((_, k) => k % 5 === 0) };
  });
  save('a2_antivegf', { scheds: scheds.map(s => s[0]), anti });
}

// ---------------------------------------------------------------- Article 3
async function a3() {
  // halo map: single satellite at distance r, immune recruitment Q, no surgery
  const rs = range(1.0, 5.0, 0.1), Qs = range(0.04, 0.10, 0.01);
  const hc = []; for (const Q of Qs) for (const r of rs) hc.push({ T: 1200, Q, fixed_seeds: [{ t: SEED_T, r }] });
  const halo = await runAll(hc, function (o, cfg) {
    const n = o.Ms.length - 1; return { Q: cfg.Q, r: cfg.fixed_seeds[0].r, Ms: o.Ms[n], Mp: o.Mp[n], edge: o.edge_p[179] };
  });
  // with surgery: does the satellite recur?
  const hs = hc.map(c => Object.assign({}, c, { t_surg: T_SURG, margin: 0.5 }));
  const haloS = await runAll(hs, function (o, cfg) { const n = o.Ms.length - 1; return { Q: cfg.Q, r: cfg.fixed_seeds[0].r, Ms: o.Ms[n], pre: o.Ms[539] }; });
  save('a3_halo', { rs, Qs, halo, haloS });

  // Monte Carlo over seeding intensity and dispersal distance
  const LS = [0.003, 0.01, 0.03, 0.1, 0.3, 1, 3], LD = [2, 4, 8], REPS = 40;
  const mc = []; for (const ld of LD) for (const ls of LS) for (let s = 1; s <= REPS; s++) mc.push({ T: 1200, lambda_seed: ls, lambda_dist: ld, seed: 1000 * s + 7, t_surg: T_SURG, margin: 0.5 });
  const mcr = await runAll(mc, function (o, cfg) {
    const n = o.Ms.length - 1; let trec = null; for (let k = 540; k <= n; k++) if (o.Ms[k] > 0.1) { trec = k - 540; break; }
    let mm = 0; for (let k = 180; k < 540; k++) mm += o.Mm[k];
    return { ls: cfg.lambda_seed, ld: cfg.lambda_dist, nseed: o.n_seeds, pre: o.Ms[539], fin: o.Ms[n], primPre: o.Mp[539], trec, meanMm: mm / 360 };
  });
  save('a3_mc', { LS, LD, REPS, mcr });

  // margin study
  const MG = [0, 0.5, 1.0, 1.5, 2.0, 3.0], R2 = 30;
  const mgc = []; for (const ld of LD) for (const ls of [0.03, 0.3]) for (const mg of MG) for (let s = 1; s <= R2; s++) mgc.push({ T: 1200, lambda_seed: ls, lambda_dist: ld, seed: 1000 * s + 7, t_surg: T_SURG, margin: mg });
  const mgr = await runAll(mgc, function (o, cfg) {
    const n = o.Ms.length - 1; return { ls: cfg.lambda_seed, ld: cfg.lambda_dist, mg: cfg.margin, pre: o.Ms[539], fin: o.Ms[n] };
  });
  save('a3_margin', { MG, R2, mgr });

  // representative stochastic run
  const ex = run({ T: 1200, lambda_seed: 0.1, lambda_dist: 4, seed: 3007, t_surg: T_SURG, margin: 0.5, profiles_at: [535, 620] });
  save('a3_example', ex);
}

(async () => {
  const which = process.argv[2] || 'all';
  const t0 = Date.now();
  if (which === 'a1' || which === 'all') await a1();
  if (which === 'a2' || which === 'all') await a2();
  if (which === 'a3' || which === 'all') await a3();
  console.log('done in', ((Date.now() - t0) / 1000).toFixed(0), 's');
})();
