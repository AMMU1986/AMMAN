#!/usr/bin/env node
/*
 * Reduced radially symmetric tumour-immune model of melanoma, adapted from
 * Eikenberry, Thalhauser & Kuang (2009) PLoS Comput Biol 5(4): e1000362.
 *
 * State variables on 0 <= r <= R (mm), densities scaled by the tumour-cell
 * carrying capacity K_C (dimensionless), time in days:
 *   p  primary-tumour cells          s  satellite-metastasis cells
 *   m  cytotoxic immune cells        e  tumour vasculature (0..1)
 *   a  immune-attracting factor (IAF, quasi-steady)
 *   v  tumour angiogenic factor (TAF, quasi-steady)
 *
 * Usage:  node melanoma_sim.js '<json config>'   (or config on stdin)
 * Prints a JSON object with time series and (optionally) final profiles.
 */
'use strict';

const DEFAULTS = {
  // geometry / numerics
  R: 12.0, N: 120, dt: 0.05, T: 1500, out_every: 1.0, seed: 1,
  // tumour cells
  r_c: 0.30, Dc: 0.01, K0: 0.25, K_sat: 0.5,
  // immune cells
  Dm: 0.01, chi: 0.25, Q: 0.05, phi_a: 0.02, beta_m: 0.02,
  beta_K: 0.5, lambda_m: 0.01,
  tau_c0: 0.02, tau_cA: 2.027, lambda_c: 0.01, xi: 0.1,
  // IAF
  Da: 2.0, beta_a: 8.0, g_ac: 1.0, g_am: 1.0,
  // TAF and vasculature
  Dv: 0.5, beta_v: 20.0, g_v: 20.0, g_vm: 0.0, V_T: 0.5, V_w: 0.05,
  alpha_e: 0.05, De: 0.002,
  // initial primary tumour
  p0: 0.2, r0: 0.5,
  ext_thresh: 1e-5,          // densities below ~1 cell per grid ring are set to zero
  // metastatic seeding (Poisson process)
  lambda_seed: 0.0, lambda_dist: 1.0, seed_start: 180, seed_amp: 0.002,
  fixed_seeds: [],           // [{t, r, amp}] deterministic seeds
  // surgery
  t_surg: null, margin: 1.0, edge_thresh: 0.01,
  // therapies: lists of {start, end, factor}
  Q_boost: [],      // multiply immune influx Q
  betaK_block: [],  // multiply beta_K (checkpoint-like relief of suppression)
  anti_vegf: [],    // multiply TAF by factor (fraction of TAF left bioavailable)
  profiles_at: [],  // times at which radial profiles are recorded
};

function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function windowFactor(list, t, base) {
  let f = base;
  for (const w of list) if (t >= w.start && t < w.end) f *= w.factor;
  return f;
}

function run(cfg) {
  const P = Object.assign({}, DEFAULTS, cfg);
  const N = P.N, dr = P.R / N, dt = P.dt;
  const rand = mulberry32(P.seed);
  const rc = new Float64Array(N), vol = new Float64Array(N);
  const rf = new Float64Array(N + 1);
  for (let i = 0; i < N; i++) { rc[i] = (i + 0.5) * dr; vol[i] = 2 * Math.PI * rc[i] * dr; }
  for (let i = 0; i <= N; i++) rf[i] = i * dr;
  // radial Laplacian weights (zero flux at r=0 and r=R)
  const wl = new Float64Array(N), wr = new Float64Array(N);
  for (let i = 0; i < N; i++) {
    wl[i] = i > 0 ? rf[i] / (rc[i] * dr * dr) : 0;
    wr[i] = i < N - 1 ? rf[i + 1] / (rc[i] * dr * dr) : 0;
  }
  // Precomputed Thomas factorisation for  D*Lap(u) - beta*u = -S
  function makeSolver(D, beta) {
    const a = new Float64Array(N), b = new Float64Array(N), c = new Float64Array(N);
    for (let i = 0; i < N; i++) { a[i] = D * wl[i]; c[i] = D * wr[i]; b[i] = -D * (wl[i] + wr[i]) - beta; }
    const cp = new Float64Array(N), den = new Float64Array(N);
    den[0] = b[0]; cp[0] = c[0] / den[0];
    for (let i = 1; i < N; i++) { den[i] = b[i] - a[i] * cp[i - 1]; cp[i] = c[i] / den[i]; }
    const dp = new Float64Array(N);
    return function (S, out) {
      dp[0] = -S[0] / den[0];
      for (let i = 1; i < N; i++) dp[i] = (-S[i] - a[i] * dp[i - 1]) / den[i];
      out[N - 1] = dp[N - 1];
      for (let i = N - 2; i >= 0; i--) out[i] = dp[i] - cp[i] * out[i + 1];
    };
  }
  const solveA = makeSolver(P.Da, P.beta_a);
  const solveV = makeSolver(P.Dv, P.beta_v);

  const p = new Float64Array(N), s = new Float64Array(N), m = new Float64Array(N);
  const e = new Float64Array(N), A = new Float64Array(N), V = new Float64Array(N);
  const SA = new Float64Array(N), SV = new Float64Array(N), G = new Float64Array(N);
  const np = new Float64Array(N), ns = new Float64Array(N), nm = new Float64Array(N), ne = new Float64Array(N);
  for (let i = 0; i < N; i++) if (rc[i] < P.r0) p[i] = P.p0;

  const lap = (u, i) => wl[i] * ((i > 0 ? u[i - 1] : u[i]) - u[i]) + wr[i] * ((i < N - 1 ? u[i + 1] : u[i]) - u[i]);
  // density-dependent (porous-medium) diffusion  div(u grad u), as in Eikenberry et al. Eq. 1
  const nlap = (u, i) => wl[i] * (i > 0 ? 0.5 * (u[i - 1] + u[i]) * (u[i - 1] - u[i]) : 0)
    + wr[i] * (i < N - 1 ? 0.5 * (u[i + 1] + u[i]) * (u[i + 1] - u[i]) : 0);
  const mass = (u) => { let M = 0; for (let i = 0; i < N; i++) M += u[i] * vol[i]; return M; };
  const edgeOf = (u) => { let E = 0; for (let i = 0; i < N; i++) if (u[i] > P.edge_thresh) E = rf[i + 1]; return E; };

  const out = { t: [], Mp: [], Ms: [], Mm: [], Me: [], edge_p: [], n_seeds: 0, seeds: [], profiles: [], events: [] };
  const prof = P.profiles_at.slice().sort((x, y) => x - y);
  const fixed = P.fixed_seeds.slice().sort((x, y) => x.t - y.t);
  const nSteps = Math.round(P.T / dt), outStride = Math.max(1, Math.round(P.out_every / dt));
  let surgDone = false, primaryPresent = true;

  for (let n = 0; n <= nSteps; n++) {
    const t = n * dt;
    // --- quasi-steady fields ---
    const antiV = windowFactor(P.anti_vegf, t, 1.0);
    for (let i = 0; i < N; i++) {
      const T = p[i] + s[i];
      G[i] = T / (P.xi + T);
      SA[i] = P.g_ac * T + P.g_am * m[i] * G[i];
      SV[i] = P.g_v * T + P.g_vm * m[i] * G[i];
    }
    solveA(SA, A); solveV(SV, V);
    if (antiV !== 1.0) for (let i = 0; i < N; i++) V[i] *= antiV;

    // --- output ---
    if (n % outStride === 0) {
      out.t.push(+t.toFixed(4)); out.Mp.push(mass(p)); out.Ms.push(mass(s));
      out.Mm.push(mass(m)); out.Me.push(mass(e)); out.edge_p.push(edgeOf(p));
    }
    while (prof.length && t >= prof[0] - 1e-9) {
      out.profiles.push({ t: prof.shift(), r: Array.from(rc), p: Array.from(p), s: Array.from(s), m: Array.from(m), e: Array.from(e), a: Array.from(A), v: Array.from(V) });
    }
    if (n === nSteps) break;

    // --- surgery ---
    if (P.t_surg !== null && !surgDone && t >= P.t_surg) {
      const Rex = edgeOf(p) + P.margin;
      for (let i = 0; i < N; i++) if (rc[i] < Rex) { p[i] = 0; s[i] = 0; m[i] = 0; e[i] = 0; }
      surgDone = true; primaryPresent = false;
      out.events.push({ type: 'surgery', t, Rex });
      continue;
    }
    // --- metastatic seeding ---
    if (primaryPresent && t >= P.seed_start && P.lambda_seed > 0) {
      let k = 0; const lam = P.lambda_seed * dt;
      // Poisson draw (small lam per step)
      let L = Math.exp(-lam), prod = rand(); while (prod > L) { k++; prod *= rand(); }
      for (let j = 0; j < k; j++) {
        const d = -Math.log(1 - rand()) / P.lambda_dist;
        const rs = edgeOf(p) + d;
        const i = Math.floor(rs / dr);
        if (i < N) { s[i] += P.seed_amp; out.n_seeds++; if (out.seeds.length < 500) out.seeds.push([+t.toFixed(2), +rs.toFixed(3)]); }
      }
    }
    while (fixed.length && t >= fixed[0].t) {
      const f = fixed.shift(); const i = Math.floor(f.r / dr);
      if (i < N) { s[i] += (f.amp !== undefined ? f.amp : P.seed_amp); out.n_seeds++; }
    }

    // --- explicit step for cells ---
    const Qt = windowFactor(P.Q_boost, t, P.Q);
    const bK = windowFactor(P.betaK_block, t, P.beta_K);
    for (let i = 0; i < N; i++) {
      const T = p[i] + s[i];
      const Kp = P.K0 + (1 - P.K0) * e[i];
      const kill = (P.tau_c0 + P.tau_cA * G[i]) * m[i] / (P.lambda_c + T);
      np[i] = p[i] + dt * (P.Dc * nlap(p, i) + P.r_c * p[i] * (1 - T / Kp) - kill * p[i]);
      ns[i] = s[i] + dt * (P.Dc * nlap(s, i) + P.r_c * s[i] * (1 - T / P.K_sat) - kill * s[i]);
      // chemotaxis (upwind flux form)
      let chem = 0;
      if (i < N - 1) { const u = P.chi * (A[i + 1] - A[i]) / dr; chem -= rf[i + 1] * (u > 0 ? m[i] : m[i + 1]) * u; }
      if (i > 0) { const u = P.chi * (A[i] - A[i - 1]) / dr; chem += rf[i] * (u > 0 ? m[i - 1] : m[i]) * u; }
      chem /= rc[i] * dr;
      nm[i] = m[i] + dt * (P.Dm * lap(m, i) + chem + Qt * A[i] / (A[i] + P.phi_a)
        - bK * T * m[i] / (P.lambda_m + m[i]) - P.beta_m * m[i]);
      const Sg = 1 / (1 + Math.exp(-(V[i] - P.V_T) / P.V_w));
      ne[i] = e[i] + dt * (P.De * lap(e, i) + P.alpha_e * (Sg * (1 - e[i]) - (1 - Sg) * e[i]));
    }
    for (let i = 0; i < N; i++) {
      p[i] = np[i] > P.ext_thresh ? np[i] : 0; s[i] = ns[i] > P.ext_thresh ? ns[i] : 0;
      m[i] = Math.max(0, nm[i]); e[i] = Math.min(1, Math.max(0, ne[i]));
    }
  }
  return out;
}

module.exports = { run, DEFAULTS };

if (require.main === module) {
  let arg = process.argv[2];
  if (!arg) arg = require('fs').readFileSync(0, 'utf8');
  const cfg = JSON.parse(arg || '{}');
  if (Array.isArray(cfg)) process.stdout.write(JSON.stringify(cfg.map(run)));
  else process.stdout.write(JSON.stringify(run(cfg)));
}
