import java.io.*;
import java.lang.reflect.Field;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;

/**
 * Planar, depth-averaged reaction-diffusion-advection model of melanoma in-transit recurrence after wide local
 * excision, coupling surgical wound healing, macrophage polarisation, interstitial fluid flow and lymphatic
 * regeneration. Companion code for "Lymphatic Rerouting at the Scar".
 *
 * Units: length mm, time day. Tumour densities in cells mm^-2 (depth-integrated over the dermis); immune/stromal
 * cells, cytokines, vessels and lymphatics are normalised (dimensionless). Pressures in mmHg.
 *
 * Usage: java LymphaticScarModel <mode> [threads]   mode = test | all
 */
public class LymphaticScarModel {

    // ------------------------------------------------------------------ grid
    static final int NX = 160, NY = 160, NC = NX * NY;
    static final double H = 1.0, XMIN = -80.0, YMIN = -80.0, DA = H * H;

    static double xc(int i) { return XMIN + (i + 0.5) * H; }
    static double yc(int j) { return YMIN + (j + 0.5) * H; }
    static int fx(int i, int j) { return j * (NX + 1) + i; }   // x-face between (i-1,j) and (i,j)
    static int fy(int i, int j) { return j * NX + i; }         // y-face between (i,j-1) and (i,j)

    // ------------------------------------------------------------------ parameters
    public static class P implements Cloneable {
        // geometry and surgery
        public double r0 = 3.0, aspect = 3.0, ws = 2.0, epsU = 0.5, epsBU = 0.3, epsQ = 0.05, q0 = 1.0, tauQ = 1.0;
        public double uA = 2.0, uB = 10.0;              // undermining width l_u = uA*B + uB
        public double bS = 0.2, kapS = 0.3;            // residual vessels / collagen at the incision line
        public double tPre = 180.0, tPost = 730.0;
        // interstitial fluid and lymph
        public double K0 = 2.0, xiE = 1.0, xiK = 2.0, PhiV = 0.1, zetaA = 4.0, pV = 0.0, PhiL = 0.2;
        public double Kl = 500.0, epsL = 0.002, Lmin = 0.2, pN = -8.0, G0 = 16.0, epsS = 0.6, tauS = 30.0;
        public double Vref = 4.0, chiA = 0.5, uStar = 0.5;
        // tumour cells
        public double KC = 3.75e5, CpFrac = 0.6, lamSh = 1e-6, Dt = 8.0, delT = 0.05;
        public double lam0 = 0.15, lam1 = 2.0, Vstar = 2.0, lamE = 0.5, delD = 0.002;
        public double om0 = 0.002, omV = 6.0, omM = 6.0, KM = 1.0, omNET = 30.0, KN = 1.0, omE = 2.0;
        public double Dc = 0.005, alphaC = 0.35, theta1 = 7.5, delC = 0.02, kE = 0.56, k1 = 0.05, lamC = 2e4;
        public double nu0 = 0.05, lamIv = 1e-3, sigV = 60.0, rb = 1.4, nuC = 1.0, sAlpha = 0.6, Nvis = 1e7;
        public double sG = 1.5, sM = 0.5, sI = 0.6, AI = 1000.0;
        // chemokine (immune-attracting factor)
        public double Da = 1.5, betaA = 4.0, gA0 = 0.4, gAq = 20.0, gAn = 0.5, gA1 = 0.05, gAe = 0.5, gAc = 4.0;
        // neutrophils
        public double Dn = 0.2, chiN = 0.3, rhoN = 6.0, Kn = 1.0, delN = 1.0, etaN = 0.3;
        // macrophages
        public double DM = 0.1, chiM = 0.2, rhoM = 4.0, delM = 0.25, k12 = 0.3, k21 = 0.05, omN = 0.5, omC = 1.0,
                KcM = 0.1, etaML = 0.05;
        // cytotoxic lymphocytes and systemic priming
        public double DE = 0.07, chiE = 0.1, epsE = 0.5, delE = 0.1, etaPi = 0.5, betaK = 0.2, lamM = 0.5;
        public double rPi = 0.1, delPi = 0.02, KA = 1e6;
        // TGF-beta
        public double Dg = 0.5, betaG = 2.0, gG0 = 0.5, gGq = 8.0, gG2 = 0.3, gGf = 0.1, gGc = 1.0, clG = 0.5;
        // fibroblasts and matrix
        public double Df = 0.05, chiF = 0.1, rF = 0.6, fMax = 5.0, delF = 0.1, Kgf = 1.0, Ke = 0.2;
        public double gEq = 2.0, gEf = 0.05, muE = 0.1, gK = 0.01, etaG = 8.0, kapMax = 2.5;
        // VEGF-A and blood microvessels
        public double Dv = 0.5, betaV = 2.0, gV0 = 0.1, gVq = 1.5, gV1 = 0.05, gV2 = 0.3, gVf = 0.05, hV = 6.0,
                thetaH = 10.0, gVc = 2.0, muV = 0.5, clV = 0.5;
        public double Db = 0.05, chiB = 0.2, alphaB = 0.5, bMax = 3.0;
        // VEGF-C and lymphatics
        public double Dw = 0.5, betaW = 1.0, gW0 = 0.1, gW1 = 0.05, gW2 = 0.4, gWc = 2.0, muW = 0.2, clW = 0.5;
        public double DL = 0.05, chiU = 1.0, alphaL = 1.0, LMax = 2.0, sLg = 2.0, sLk = 2.0, Lseed = 0.02;
        // treatment efficacies
        public double effNsaidRecruit = 0.5, effNsaidVEGFC = 0.5, effNsaidVEGFA = 0.3;
        public double effBetaVEGFA = 0.4, effBetaVEGFC = 0.4, effBetaRecruit = 0.25;
        public double effAntiVEGFA = 0.7, effAntiVEGFR3 = 0.8;
        // derived at homeostasis (computed)
        public double betaB, betaL, muK, rhoE, upsT, g0, M1b, M2b, ab, vb, wb, nb;

        P copy() {
            try { return (P) super.clone(); } catch (CloneNotSupportedException e) { throw new RuntimeException(e); }
        }
    }

    // ------------------------------------------------------------------ scenario definition
    static class Scenario {
        String name;
        double margin = 10.0, theta = 0.0;
        boolean immuneLoss = true, wound = true, reroute = true;
        double tSLNB = Double.NaN;                    // days relative to surgery, NaN = none
        double[][] drug = new double[4][];             // {start, duration} relative to surgery; 0 NSAID,1 beta,2 aVEGFA,3 aVEGFR3
        Map<String, Double> mult = new LinkedHashMap<>();
        double[] snapDays = null;                      // post-operative snapshot days
        Scenario(String n) { name = n; }
        Scenario m(double v) { margin = v; return this; }
        Scenario th(double v) { theta = v; return this; }
        Scenario sw(boolean il, boolean wo, boolean rr) { immuneLoss = il; wound = wo; reroute = rr; return this; }
        Scenario slnb(double t) { tSLNB = t; return this; }
        Scenario drug(int k, double s, double d) { drug[k] = new double[]{s, d}; return this; }
        Scenario mul(String p, double f) { mult.put(p, f); return this; }
        Scenario snaps(double... d) { snapDays = d; return this; }
    }

    // ------------------------------------------------------------------ math helpers
    static double erfc(double x) {   // Numerical Recipes erfcc, |rel err| < 1.2e-7
        double z = Math.abs(x), t = 1.0 / (1.0 + 0.5 * z);
        double ans = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 +
                t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 +
                t * (-0.82215223 + t * 0.17087277)))))))));
        return x >= 0 ? ans : 2.0 - ans;
    }
    static double Phi(double x) { return 0.5 * erfc(-x / Math.sqrt(2.0)); }

    /** Escape probability of an activated lineage with lognormal birth rate (median alpha, log-sd s), death mu. */
    static double escapeProb(double alpha, double mu, double s) {
        if (alpha <= 1e-12) return 0.0;
        if (mu <= 1e-12) return 1.0;
        double d = Math.log(alpha / mu) / s;
        double pi = Phi(d) - (mu / alpha) * Math.exp(0.5 * s * s) * Phi(d - s);
        return Math.max(0.0, pi);
    }
    /** Mean net growth rate of escaping clones, E[alpha | alpha > mu] - mu. */
    static double escapeRate(double alpha, double mu, double s) {
        if (alpha <= 1e-12) return 1e-3;
        double d = Math.log(alpha / Math.max(mu, 1e-12)) / s, pd = Phi(d);
        if (pd < 1e-300) return 1e-3;
        return Math.max(alpha * Math.exp(0.5 * s * s) * Phi(d + s) / pd - mu, 1e-3);
    }

    // ------------------------------------------------------------------ simulation
    static class Sim {
        final P p; final Scenario sc;
        // state fields
        double[] ct = new double[NC], cd = new double[NC], cg = new double[NC], cp = new double[NC], cpV = new double[NC];
        double[] E = new double[NC], n = new double[NC], M1 = new double[NC], M2 = new double[NC];
        double[] a = new double[NC], g = new double[NC], f = new double[NC], e = new double[NC], kap = new double[NC];
        double[] v = new double[NC], b = new double[NC], w = new double[NC], L = new double[NC];
        double[] pr = new double[NC], pl = new double[NC];
        double Pi = 0.0, Isys = 0.0, t = 0.0;
        // geometry masks after surgery: 0 none, 1 scar band, 2 undermined
        int[] zone = new int[NC];
        double tS;                     // surgery time
        boolean postOp = false;
        // scratch
        double[] gxA = new double[(NX + 1) * NY], gyA = new double[NX * (NY + 1)];
        double[] gxG = new double[(NX + 1) * NY], gyG = new double[NX * (NY + 1)];
        double[] gxV = new double[(NX + 1) * NY], gyV = new double[NX * (NY + 1)];
        double[] ux = new double[(NX + 1) * NY], uy = new double[NX * (NY + 1)];
        double[] Vx = new double[(NX + 1) * NY], Vy = new double[NX * (NY + 1)];
        double[] Dfx = new double[(NX + 1) * NY], Dfy = new double[NX * (NY + 1)];
        double[] tr = new double[NC], tmp = new double[NC];
        double[] sig = new double[NC], Eeff = new double[NC], om = new double[NC], lamb = new double[NC], uabs = new double[NC];
        double[] piEsc = new double[NC], tauV = new double[NC], Vabs = new double[NC];
        double[] nN = new double[NC], M1N = new double[NC], M2N = new double[NC], EN = new double[NC], fN = new double[NC];
        double[] bN = new double[NC], LN = new double[NC], cgN = new double[NC], cdN = new double[NC], eN = new double[NC], kN = new double[NC];
        // CG work vectors for the coupled pressure system (size 2*NC)
        double[] cgR = new double[2 * NC], cgZ = new double[2 * NC], cgP = new double[2 * NC], cgQ = new double[2 * NC], cgX = new double[2 * NC], cgD = new double[2 * NC], cgB = new double[2 * NC];
        double[] Kc = new double[NC], Cv = new double[NC], Cl = new double[NC], Rb = new double[NC];
        // risk accounting
        static final int NBIN = 731;
        double[] visBin = new double[NBIN];      // expected visible lesions by post-op day bin
        double[] visBinLocal = new double[NBIN];
        double[] escMap = new double[NC];
        double[][] angDist = new double[36][5];  // angle around scar centre x distance-to-scar class
        double Ncommit = 0, NcommitLocal = 0, NcommitProx = 0, Npre = 0, lodgedPost = 0, lodgedPostNear = 0;
        double excisedCd = 0, totalCdPre = 0, excisedCt = 0, totalCtPre = 0;
        double A_, B_, Bu_, cth, sth;
        // outputs
        StringBuilder ts = new StringBuilder();
        Path outDir;
        double peakBandV = 0, peakBandVday = 0, peakN = 0, peakNday = 0, peakM1 = 0, peakM1day = 0, peakM2 = 0, peakM2day = 0;
        double Lrec50 = Double.NaN, minBandL = 1e9;
        double cpTot = 0;

        Sim(P p, Scenario sc, Path outDir) { this.p = p; this.sc = sc; this.outDir = outDir; }

        // ---------- homeostasis (spatially uniform, local balance) ----------
        void homeostasis() {
            double aa = 0.1, nn = 0, m1 = 0.5, m2 = 0.3, gg = 0.2, vv = 0.2, ww = 0.2, dt = 0.02;
            double s0 = p.sigV * p.rb / (p.rb + 1.0);
            double hyp = 1.0 + p.hV * p.thetaH * p.thetaH / (p.thetaH * p.thetaH + s0 * s0);
            for (int it = 0; it < 400000; it++) {
                double aN = (aa + dt * (p.gA0 + p.gAn * nn + p.gA1 * m1)) / (1 + dt * p.betaA);
                double nN_ = (nn + dt * p.rhoN * aa * aa / (p.Kn * p.Kn + aa * aa)) / (1 + dt * (p.delN + p.etaN * (m1 + m2)));
                double psi = p.k12 * (gg / (1 + gg) + p.omN * nn / (1 + nn));
                double m1N = (m1 + dt * (p.rhoM * aa / (1 + aa) + p.k21 * m2)) / (1 + dt * (psi + p.delM + p.etaML));
                double m2N = (m2 + dt * psi * m1) / (1 + dt * (p.k21 + p.delM + p.etaML));
                double gN = (gg + dt * (p.gG0 + p.gG2 * m2 + p.gGf)) / (1 + dt * (p.betaG + p.clG));
                double vN = (vv + dt * (p.gV0 + (p.gV1 * m1 + p.gV2 * m2 + p.gVf) * hyp)) / (1 + dt * (p.muV / (1 + vv) + p.betaV + p.clV));
                double wN = (ww + dt * (p.gW0 + p.gW1 * m1 + p.gW2 * m2)) / (1 + dt * (p.muW / (1 + ww) + p.betaW + p.clW));
                double ch = Math.abs(aN - aa) + Math.abs(nN_ - nn) + Math.abs(m1N - m1) + Math.abs(m2N - m2) + Math.abs(gN - gg) + Math.abs(vN - vv) + Math.abs(wN - ww);
                aa = aN; nn = nN_; m1 = m1N; m2 = m2N; gg = gN; vv = vN; ww = wN;
                if (ch < 1e-13 && it > 1000) break;
            }
            p.ab = aa; p.nb = nn; p.M1b = m1; p.M2b = m2; p.g0 = gg; p.vb = vv; p.wb = ww;
            p.betaB = p.alphaB * (1 - 1 / p.bMax) * vv;
            p.betaL = p.alphaL * (1 + p.Lseed) * (1 - 1 / p.LMax) * ww;
            p.muK = p.gK * (1 - 1 / p.kapMax);
            p.rhoE = p.delE / (p.epsE + aa / (1 + aa));
            Arrays.fill(a, aa); Arrays.fill(n, nn); Arrays.fill(M1, m1); Arrays.fill(M2, m2); Arrays.fill(g, gg);
            Arrays.fill(v, vv); Arrays.fill(w, ww); Arrays.fill(E, 1.0); Arrays.fill(f, 1.0); Arrays.fill(kap, 1.0);
            Arrays.fill(b, 1.0); Arrays.fill(L, 1.0); Arrays.fill(e, 0.0);
            Arrays.fill(pr, -3.0); Arrays.fill(pl, -4.0);
            solvePressure();
            // emboli mobility from the reference speed at the primary site
            int i0 = NX / 2, j0 = NY / 2;
            double grad = Math.abs(pl[j0 * NX + i0] - pl[j0 * NX + i0 - 1]) / H;
            double fac = (1.0 + p.epsL) / (1.0 + p.Lmin);
            p.upsT = p.Vref / (fac * grad);
        }

        // ---------- helpers ----------
        double SqAt(int k, double tt) {
            if (!postOp || !sc.wound) return 0.0;
            double base = zone[k] == 1 ? 1.0 : (zone[k] == 2 ? p.epsQ : 0.0);
            return base == 0 ? 0 : p.q0 * base * Math.exp(-(tt - tS) / p.tauQ);
        }
        double drugOn(int kk, double tt) {
            double[] d = sc.drug[kk];
            if (d == null) return 0.0;
            double rel = tt - tS;
            return (rel >= d[0] && rel < d[0] + d[1]) ? 1.0 : 0.0;
        }
        double GN(double tt) {
            if (Double.isNaN(sc.tSLNB)) return p.G0;
            double tl = tS + sc.tSLNB;
            if (tt < tl) return p.G0;
            return p.G0 * (1 - p.epsS * Math.exp(-(tt - tl) / p.tauS));
        }
        static double bt(double bb) { return 1.25 * bb / (0.25 + bb); }
        boolean inExcision(int k) {
            double B = p.r0 + sc.margin, A = p.aspect * B, th = Math.toRadians(sc.theta);
            double x = xc(k % NX), y = yc(k / NX), xr = x * Math.cos(th) + y * Math.sin(th), yr = -x * Math.sin(th) + y * Math.cos(th);
            return (xr / A) * (xr / A) + (yr / B) * (yr / B) <= 1.0;
        }
        static double harm(double x, double y) { double s = x + y; return s <= 0 ? 0 : 2 * x * y / s; }

        void gradFaces(double[] s, double[] gx, double[] gy) {
            for (int j = 0; j < NY; j++) {
                gx[fx(0, j)] = 0; gx[fx(NX, j)] = 0;
                for (int i = 1; i < NX; i++) gx[fx(i, j)] = (s[j * NX + i] - s[j * NX + i - 1]) / H;
            }
            for (int i = 0; i < NX; i++) { gy[fy(i, 0)] = 0; gy[fy(i, NY)] = 0; }
            for (int j = 1; j < NY; j++) for (int i = 0; i < NX; i++) gy[fy(i, j)] = (s[j * NX + i] - s[(j - 1) * NX + i]) / H;
        }

        /** out += -coef * div(vel * q) with first-order upwinding; closed boundaries except optional right outflow. */
        static void advect(double[] q, double[] vx, double[] vy, double coef, double[] out, boolean openRight) {
            for (int j = 0; j < NY; j++) {
                int row = j * NX;
                for (int i = 1; i < NX; i++) {
                    double vel = coef * vx[fx(i, j)];
                    double F = vel > 0 ? vel * q[row + i - 1] : vel * q[row + i];
                    out[row + i - 1] -= F / H; out[row + i] += F / H;
                }
                if (openRight) {
                    double vel = coef * vx[fx(NX, j)];
                    if (vel > 0) out[row + NX - 1] -= vel * q[row + NX - 1] / H;
                }
            }
            for (int j = 1; j < NY; j++) {
                for (int i = 0; i < NX; i++) {
                    double vel = coef * vy[fy(i, j)];
                    double F = vel > 0 ? vel * q[(j - 1) * NX + i] : vel * q[j * NX + i];
                    out[(j - 1) * NX + i] -= F / H; out[j * NX + i] += F / H;
                }
            }
        }
        static void laplace(double[] q, double D, double[] out) {
            double c = D / (H * H);
            for (int j = 0; j < NY; j++) {
                int row = j * NX;
                for (int i = 0; i < NX; i++) {
                    int k = row + i;
                    double qc = q[k], s = 0;
                    if (i > 0) s += q[k - 1] - qc;
                    if (i < NX - 1) s += q[k + 1] - qc;
                    if (j > 0) s += q[k - NX] - qc;
                    if (j < NY - 1) s += q[k + NX] - qc;
                    out[k] += c * s;
                }
            }
        }
        static double maxAbs(double[] x) { double m = 0; for (double d : x) m = Math.max(m, Math.abs(d)); return m; }

        // ---------- coupled interstitial / lymph pressure (SPD system, Jacobi-PCG) ----------
        long cgIters = 0, cgCalls = 0, cgNanos = 0;
        void solvePressure() {
            long t0n = System.nanoTime(); cgCalls++;
            double G = GN(t);
            for (int k = 0; k < NC; k++) {
                double cond = p.K0 * (1 + p.xiE * e[k]) * (1 + p.xiK) / (1 + p.xiK * kap[k]);
                Kc[k] = cond;
                Cv[k] = p.PhiV * (1 + p.zetaA * a[k] / (1 + a[k])) * b[k];
                Cl[k] = p.PhiL * L[k];
            }
            Arrays.fill(Rb, 0.0);
            for (int j = 0; j < NY; j++) {
                int k = j * NX + NX - 1;
                double res = H / (2 * p.Kl * (L[k] + p.epsL)) + 1.0 / G;
                Rb[k] = 1.0 / (H * res);
            }
            // rhs, diagonal
            for (int k = 0; k < NC; k++) { cgB[k] = Cv[k] * p.pV; cgB[NC + k] = Rb[k] * p.pN; }
            for (int j = 0; j < NY; j++) for (int i = 0; i < NX; i++) {
                int k = j * NX + i; double dp = Cv[k] + Cl[k], dl = Cl[k] + Rb[k];
                if (i > 0) { dp += harm(Kc[k], Kc[k - 1]) / (H * H); dl += p.Kl * (harm(L[k], L[k - 1]) + p.epsL) / (H * H); }
                if (i < NX - 1) { dp += harm(Kc[k], Kc[k + 1]) / (H * H); dl += p.Kl * (harm(L[k], L[k + 1]) + p.epsL) / (H * H); }
                if (j > 0) { dp += harm(Kc[k], Kc[k - NX]) / (H * H); dl += p.Kl * (harm(L[k], L[k - NX]) + p.epsL) / (H * H); }
                if (j < NY - 1) { dp += harm(Kc[k], Kc[k + NX]) / (H * H); dl += p.Kl * (harm(L[k], L[k + NX]) + p.epsL) / (H * H); }
                cgD[k] = dp; cgD[NC + k] = dl;
            }
            System.arraycopy(pr, 0, cgX, 0, NC); System.arraycopy(pl, 0, cgX, NC, NC);
            applyA(cgX, cgQ);
            double bn = 0, rz = 0;
            for (int k = 0; k < 2 * NC; k++) { cgR[k] = cgB[k] - cgQ[k]; bn += cgB[k] * cgB[k]; }
            bn = Math.sqrt(bn) + 1e-30;
            for (int k = 0; k < 2 * NC; k++) { cgZ[k] = cgR[k] / cgD[k]; cgP[k] = cgZ[k]; rz += cgR[k] * cgZ[k]; }
            for (int it = 0; it < 20000; it++) {
                applyA(cgP, cgQ);
                double pq = 0; for (int k = 0; k < 2 * NC; k++) pq += cgP[k] * cgQ[k];
                double al = rz / pq, rn = 0;
                for (int k = 0; k < 2 * NC; k++) { cgX[k] += al * cgP[k]; cgR[k] -= al * cgQ[k]; rn += cgR[k] * cgR[k]; }
                cgIters++;
                if (Math.sqrt(rn) / bn < 1e-8) break;
                double rzN = 0; for (int k = 0; k < 2 * NC; k++) { cgZ[k] = cgR[k] / cgD[k]; rzN += cgR[k] * cgZ[k]; }
                double be = rzN / rz; rz = rzN;
                for (int k = 0; k < 2 * NC; k++) cgP[k] = cgZ[k] + be * cgP[k];
            }
            System.arraycopy(cgX, 0, pr, 0, NC); System.arraycopy(cgX, NC, pl, 0, NC);
            cgNanos += System.nanoTime() - t0n;
            // face velocities: interstitial Darcy u, emboli velocity V_t, emboli dispersion coefficient
            for (int j = 0; j < NY; j++) {
                ux[fx(0, j)] = 0; Vx[fx(0, j)] = 0; Dfx[fx(0, j)] = 0;
                for (int i = 1; i < NX; i++) {
                    int k = j * NX + i, km = k - 1;
                    ux[fx(i, j)] = -harm(Kc[k], Kc[km]) * (pr[k] - pr[km]) / H;
                    double Lf = harm(L[k], L[km]);
                    Vx[fx(i, j)] = -p.upsT * (Lf + p.epsL) / (Lf + p.Lmin) * (pl[k] - pl[km]) / H;
                    Dfx[fx(i, j)] = p.Dt * Lf / (Lf + p.Lmin);
                }
                int k = j * NX + NX - 1;
                ux[fx(NX, j)] = 0; Dfx[fx(NX, j)] = 0;
                double qb = Rb[k] * H * (pl[k] - p.pN);           // lymph outflow per unit boundary length
                Vx[fx(NX, j)] = Math.max(0, p.upsT * qb / (p.Kl * (L[k] + p.Lmin)));
            }
            for (int i = 0; i < NX; i++) { uy[fy(i, 0)] = uy[fy(i, NY)] = 0; Vy[fy(i, 0)] = Vy[fy(i, NY)] = 0; Dfy[fy(i, 0)] = Dfy[fy(i, NY)] = 0; }
            for (int j = 1; j < NY; j++) for (int i = 0; i < NX; i++) {
                int k = j * NX + i, km = k - NX;
                uy[fy(i, j)] = -harm(Kc[k], Kc[km]) * (pr[k] - pr[km]) / H;
                double Lf = harm(L[k], L[km]);
                Vy[fy(i, j)] = -p.upsT * (Lf + p.epsL) / (Lf + p.Lmin) * (pl[k] - pl[km]) / H;
                Dfy[fy(i, j)] = p.Dt * Lf / (Lf + p.Lmin);
            }
            for (int j = 0; j < NY; j++) for (int i = 0; i < NX; i++) {
                int k = j * NX + i;
                double uxc = 0.5 * (ux[fx(i, j)] + ux[fx(i + 1, j)]), uyc = 0.5 * (uy[fy(i, j)] + uy[fy(i, j + 1)]);
                uabs[k] = Math.hypot(uxc, uyc);
                double vxc = 0.5 * (Vx[fx(i, j)] + Vx[fx(i + 1, j)]), vyc = 0.5 * (Vy[fy(i, j)] + Vy[fy(i, j + 1)]);
                Vabs[k] = Math.hypot(vxc, vyc);
            }
        }
        void applyA(double[] x, double[] y) {
            double hh = H * H;
            for (int j = 0; j < NY; j++) for (int i = 0; i < NX; i++) {
                int k = j * NX + i;
                double xp = x[k], xl = x[NC + k];
                double yp = (Cv[k] + Cl[k]) * xp - Cl[k] * xl;
                double yl = (Cl[k] + Rb[k]) * xl - Cl[k] * xp;
                if (i > 0) { int m = k - 1; yp += harm(Kc[k], Kc[m]) / hh * (xp - x[m]); yl += p.Kl * (harm(L[k], L[m]) + p.epsL) / hh * (xl - x[NC + m]); }
                if (i < NX - 1) { int m = k + 1; yp += harm(Kc[k], Kc[m]) / hh * (xp - x[m]); yl += p.Kl * (harm(L[k], L[m]) + p.epsL) / hh * (xl - x[NC + m]); }
                if (j > 0) { int m = k - NX; yp += harm(Kc[k], Kc[m]) / hh * (xp - x[m]); yl += p.Kl * (harm(L[k], L[m]) + p.epsL) / hh * (xl - x[NC + m]); }
                if (j < NY - 1) { int m = k + NX; yp += harm(Kc[k], Kc[m]) / hh * (xp - x[m]); yl += p.Kl * (harm(L[k], L[m]) + p.epsL) / hh * (xl - x[NC + m]); }
                y[k] = yp; y[NC + k] = yl;
            }
        }

        // ---------- surgery: excision, primary closure map, wound initial conditions ----------
        void surgery() {
            double B = p.r0 + sc.margin, A = p.aspect * B, lu = p.uA * B + p.uB, Bu = B + lu, J = Bu / lu;
            A_ = A; B_ = B; Bu_ = Bu;
            double th = Math.toRadians(sc.theta); cth = Math.cos(th); sth = Math.sin(th);
            double[][] cellF = {ct, cd, cg, E, n, M1, M2};
            double[][] other = {a, g, f, e, kap, v, b, w, L};
            double[][] cellO = new double[cellF.length][], othO = new double[other.length][];
            for (int q = 0; q < cellF.length; q++) cellO[q] = cellF[q].clone();
            for (int q = 0; q < other.length; q++) othO[q] = other[q].clone();
            // excised amounts (old coordinates inside the excision ellipse)
            for (int j = 0; j < NY; j++) for (int i = 0; i < NX; i++) {
                int k = j * NX + i; double x = xc(i), y = yc(j);
                double xr = x * cth + y * sth, yr = -x * sth + y * cth;
                totalCdPre += cd[k] * DA; totalCtPre += ct[k] * DA;
                if ((xr / A) * (xr / A) + (yr / B) * (yr / B) <= 1.0) { excisedCd += cd[k] * DA; excisedCt += ct[k] * DA; }
            }
            for (int j = 0; j < NY; j++) for (int i = 0; i < NX; i++) {
                int k = j * NX + i; double x = xc(i), y = yc(j);
                double xr = x * cth + y * sth, yr = -x * sth + y * cth;
                zone[k] = 0;
                if ((xr / A) * (xr / A) + (yr / Bu) * (yr / Bu) > 1.0) continue;
                double s = Math.sqrt(Math.max(0, 1 - (xr / A) * (xr / A)));
                double beta = B * s, betaU = Bu * s;
                double sgn = yr >= 0 ? 1 : -1;
                double yo = sgn * (beta + Math.abs(yr) * (betaU - beta) / Math.max(betaU, 1e-9));
                double xo_ = xr * cth - yo * sth, yo_ = xr * sth + yo * cth;
                for (int q = 0; q < cellF.length; q++) cellF[q][k] = sample(cellO[q], xo_, yo_) / J;
                for (int q = 0; q < other.length; q++) other[q][k] = sample(othO[q], xo_, yo_);
                zone[k] = Math.abs(yr) <= p.ws ? 1 : 2;
            }
            for (int k = 0; k < NC; k++) {
                cp[k] = 0.0;
                if (!sc.immuneLoss) { /* virtual primary keeps immune stimulation */ } else cpV[k] = 0.0;
                if (zone[k] == 1) {
                    if (sc.reroute) L[k] = 0.0;
                    if (sc.wound) { b[k] = p.bS * b[k]; e[k] = 1.0; kap[k] = p.kapS; }
                } else if (zone[k] == 2) {
                    if (sc.reroute) L[k] *= (1 - p.epsU);
                    if (sc.wound) { b[k] *= (1 - p.epsBU); e[k] = Math.max(e[k], p.epsQ); }
                }
            }
            postOp = true;
        }
        static double sample(double[] fld, double x, double y) {
            double gx = (x - XMIN) / H - 0.5, gy = (y - YMIN) / H - 0.5;
            gx = Math.max(0, Math.min(NX - 1.000001, gx)); gy = Math.max(0, Math.min(NY - 1.000001, gy));
            int i = (int) gx, j = (int) gy; double fxx = gx - i, fyy = gy - j;
            int k = j * NX + i;
            return (1 - fxx) * (1 - fyy) * fld[k] + fxx * (1 - fyy) * fld[k + 1] + (1 - fxx) * fyy * fld[k + NX] + fxx * fyy * fld[k + NX + 1];
        }

        // ---------- one time step ----------
        void step(double dtNom) {
            final double nsaid = drugOn(0, t), beta = drugOn(1, t), aVA = drugOn(2, t), aVR3 = drugOn(3, t);
            final double recN = 1 - p.effNsaidRecruit * nsaid, recM = (1 - p.effNsaidRecruit * nsaid) * (1 - p.effBetaRecruit * beta);
            final double fW = (1 - p.effNsaidVEGFC * nsaid) * (1 - p.effBetaVEGFC * beta);
            final double fV = (1 - p.effNsaidVEGFA * nsaid) * (1 - p.effBetaVEGFA * beta);
            final double fVeff = 1 - p.effAntiVEGFA * aVA, fL = 1 - p.effAntiVEGFR3 * aVR3;
            // effective VEGF-A seen by vessels and dormant cells
            for (int k = 0; k < NC; k++) tmp[k] = fVeff * v[k];
            gradFaces(a, gxA, gyA); gradFaces(g, gxG, gyG); gradFaces(tmp, gxV, gyV);
            // CFL-limited time step
            double vmax = Math.max(Math.max(p.chiN, Math.max(p.chiM, p.chiE)) * Math.max(maxAbs(gxA), maxAbs(gyA)),
                    Math.max(p.chiF * Math.max(maxAbs(gxG), maxAbs(gyG)), p.chiB * Math.max(maxAbs(gxV), maxAbs(gyV))));
            vmax = Math.max(vmax, Math.max(p.chiU, p.chiA) * Math.max(maxAbs(ux), maxAbs(uy)));
            double dt = Math.min(dtNom, 0.45 * H / Math.max(vmax, 1e-9));
            final double eNorm = 1 + p.sG * p.g0 + p.sM * p.M2b;
            double Atot = 0;
            for (int k = 0; k < NC; k++) {
                double tum = cp[k] + cg[k] + cd[k];
                sig[k] = p.sigV * p.rb * b[k] / (p.rb * b[k] + 1 + p.nuC * tum / p.KC);
                Eeff[k] = E[k] * eNorm / (1 + p.sG * g[k] + p.sM * M2[k] + p.sI * Isys / (1 + Isys));
                double ve = tmp[k];
                double dn = Math.max(0, n[k] - p.nb);
                om[k] = p.om0 * (1 + p.omV * ve / (1 + ve) + p.omM * M2[k] / (p.KM + M2[k]) + p.omNET * dn / (p.KN + dn)) / (1 + p.omE * Eeff[k]);
                lamb[k] = p.lam0 * (1 + p.lam1 * Math.max(0, 1 - L[k])) * p.Vstar / (p.Vstar + Vabs[k]) + p.lamE * e[k];
                Atot += (cp[k] + cg[k]) * Math.min(L[k], 1.0) * DA;
            }
            // ---- risk accounting (uses current state) ----
            double tPostDay = t - tS;
            for (int k = 0; k < NC; k++) {
                double alpha = p.alphaC * sig[k] * sig[k] / (p.theta1 * p.theta1 + sig[k] * sig[k]) * Math.max(0, 1 - (cp[k] + cg[k] + cd[k]) / p.KC);
                double nur = p.nu0 * Eeff[k] / (1 + Eeff[k]);
                double mu = p.delC + nur + p.kE * Eeff[k] + p.k1 * M1[k];
                double pe = escapeProb(alpha, mu, p.sAlpha);
                piEsc[k] = pe;
                double flux = om[k] * cd[k] * pe * DA * dt;     // escaping lineages this step
                if (flux <= 0) { tauV[k] = 0; continue; }
                double r = escapeRate(alpha, mu, p.sAlpha);
                double tau = Math.log(p.Nvis) / r;
                tauV[k] = tau;
                if (!postOp) { if (!inExcision(k)) Npre += flux; continue; }
                Ncommit += flux;
                int i = k % NX, j = k / NX; double x = xc(i), y = yc(j);
                double xr = x * cth + y * sth, yr = -x * sth + y * cth;
                double dsc = Math.hypot(Math.max(Math.abs(xr) - A_, 0), yr);
                boolean local = dsc <= 20.0;
                if (local) NcommitLocal += flux;
                if (x > 0) NcommitProx += flux;
                escMap[k] += flux;
                int ab = (int) Math.floor((Math.toDegrees(Math.atan2(y, x)) + 360.0) % 360.0 / 10.0);
                int dc = dsc <= 5 ? 0 : dsc <= 10 ? 1 : dsc <= 20 ? 2 : dsc <= 40 ? 3 : 4;
                angDist[Math.min(ab, 35)][dc] += flux;
                int bin = (int) Math.ceil(tPostDay + tau);
                if (bin < NBIN) { visBin[bin] += flux; if (local) visBinLocal[bin] += flux; }
            }
            // ---- cells ----
            // neutrophils
            Arrays.fill(tr, 0); laplace(n, p.Dn, tr); advect(n, gxA, gyA, p.chiN, tr, false);
            for (int k = 0; k < NC; k++) {
                double gain = recN * p.rhoN * bt(b[k]) * a[k] * a[k] / (p.Kn * p.Kn + a[k] * a[k]);
                double loss = p.delN + p.etaN * (M1[k] + M2[k]);
                nN[k] = Math.max(0, (n[k] + dt * (tr[k] + gain)) / (1 + dt * loss));
            }
            // macrophages
            Arrays.fill(tr, 0); laplace(M1, p.DM, tr); advect(M1, gxA, gyA, p.chiM, tr, false);
            Arrays.fill(tmp, 0); laplace(M2, p.DM, tmp);
            for (int k = 0; k < NC; k++) {
                double tum = cp[k] + cg[k];
                double psi = p.k12 * (g[k] / (1 + g[k]) + p.omN * n[k] / (1 + n[k]) + p.omC * tum / (p.KcM * p.KC + tum));
                double rec = recM * p.rhoM * bt(b[k]) * a[k] / (1 + a[k]);
                double egress = p.etaML * Math.min(L[k], 1.5);
                M1N[k] = Math.max(0, (M1[k] + dt * (tr[k] + rec + p.k21 * M2[k])) / (1 + dt * (psi + p.delM + egress)));
                M2N[k] = Math.max(0, (M2[k] + dt * (tmp[k] + psi * M1[k])) / (1 + dt * (p.k21 + p.delM + egress)));
            }
            // cytotoxic lymphocytes
            Arrays.fill(tr, 0); laplace(E, p.DE, tr); advect(E, gxA, gyA, p.chiE, tr, false);
            for (int k = 0; k < NC; k++) {
                double rec = p.rhoE * bt(b[k]) * (1 + p.etaPi * Pi) * (p.epsE + a[k] / (1 + a[k]));
                double loss = p.delE + p.betaK * ((cp[k] + cg[k]) / p.KC) / (p.lamM + E[k]);
                EN[k] = Math.max(0, (E[k] + dt * (tr[k] + rec)) / (1 + dt * loss));
            }
            // fibroblasts
            Arrays.fill(tr, 0); laplace(f, p.Df, tr); advect(f, gxG, gyG, p.chiF, tr, false);
            for (int k = 0; k < NC; k++) {
                double dg = Math.max(0, g[k] - p.g0), Gs = dg / (p.Kgf + dg) * e[k] / (p.Ke + e[k]);
                fN[k] = Math.max(0, (f[k] + dt * (tr[k] + p.rF * f[k] * Gs + p.delF)) / (1 + dt * (p.delF + p.rF * Gs * f[k] / p.fMax)));
            }
            // blood microvessels (chemotaxis up the effective VEGF-A gradient)
            Arrays.fill(tr, 0); laplace(b, p.Db, tr); advect(b, gxV, gyV, p.chiB, tr, false);
            for (int k = 0; k < NC; k++) {
                double ve = fVeff * v[k];
                double gain = p.alphaB * b[k] * ve / (1 + ve);
                double loss = p.alphaB * ve / (1 + ve) * b[k] / p.bMax + p.betaB / (1 + ve);
                bN[k] = Math.max(0, (b[k] + dt * (tr[k] + gain)) / (1 + dt * loss));
            }
            // lymphatics: diffusion, flow-guided migration of immature lymphatics, VEGF-C driven growth
            Arrays.fill(tr, 0); laplace(L, p.DL, tr);
            for (int k = 0; k < NC; k++) tmp[k] = L[k] * Math.max(0, 1 - L[k]);
            advect(tmp, ux, uy, p.chiU, tr, false);
            for (int k = 0; k < NC; k++) {
                double xi = (1 + p.sLg * p.g0) / (1 + p.sLg * g[k]) / (1 + p.sLk * Math.max(0, kap[k] - 1));
                double ww = w[k] / (1 + w[k]);
                double gain = fL * p.alphaL * (L[k] + p.Lseed) * ww * xi;
                double loss = fL * p.alphaL * (L[k] + p.Lseed) * ww * xi / p.LMax + p.betaL / (1 + w[k]);
                LN[k] = Math.max(0, (L[k] + dt * (tr[k] + gain)) / (1 + dt * loss));
            }
            // activated (proliferating) satellite cells
            Arrays.fill(tr, 0); laplace(cg, p.Dc, tr); advect(cg, ux, uy, p.chiA, tr, false);
            for (int k = 0; k < NC; k++) {
                double alpha = p.alphaC * sig[k] * sig[k] / (p.theta1 * p.theta1 + sig[k] * sig[k]);
                double crowd = Math.max(0, 1 - (cp[k] + cg[k] + cd[k]) / p.KC);
                double nur = p.nu0 * Eeff[k] / (1 + Eeff[k]);
                double muI = (p.kE * Eeff[k] + p.k1 * M1[k]) / (1 + cg[k] / p.lamC);
                double iv = p.lamIv * L[k] * uabs[k] / (uabs[k] + p.uStar);
                cgN[k] = Math.max(0, (cg[k] + dt * (tr[k] + om[k] * cd[k] + alpha * crowd * cg[k])) / (1 + dt * (p.delC + muI + nur + iv)));
                cdN[k] = Math.max(0, (cd[k] + dt * (lamb[k] * ct[k] + nur * cg[k])) / (1 + dt * (om[k] + p.delD)));
                tmp[k] = iv * cg[k];   // intravasation source for ct
            }
            // lodging accounting (post-op)
            if (postOp) for (int k = 0; k < NC; k++) {
                double l = lamb[k] * ct[k] * DA * dt; lodgedPost += l;
                if (zone[k] != 0) lodgedPostNear += l;
            }
            // in-transit cells: sub-cycled advection-dispersion in the lymphatic network
            double vm = Math.max(maxAbs(Vx), maxAbs(Vy));
            double dmax = 0; for (double d : Dfx) dmax = Math.max(dmax, d); for (double d : Dfy) dmax = Math.max(dmax, d);
            int nsub = (int) Math.ceil(dt * (2 * vm / H + 4 * dmax / (H * H)) / 0.9);
            nsub = Math.max(nsub, 1);
            double dts = dt / nsub;
            for (int s = 0; s < nsub; s++) {
                Arrays.fill(tr, 0);
                for (int j = 0; j < NY; j++) for (int i = 1; i < NX; i++) {
                    int k = j * NX + i; double F = -Dfx[fx(i, j)] * (ct[k] - ct[k - 1]) / H;
                    tr[k - 1] -= F / H; tr[k] += F / H;
                }
                for (int j = 1; j < NY; j++) for (int i = 0; i < NX; i++) {
                    int k = j * NX + i; double F = -Dfy[fy(i, j)] * (ct[k] - ct[k - NX]) / H;
                    tr[k - NX] -= F / H; tr[k] += F / H;
                }
                advect(ct, Vx, Vy, 1.0, tr, true);
                for (int k = 0; k < NC; k++) {
                    double src = p.lamSh * L[k] * cp[k] + tmp[k];
                    ct[k] = Math.max(0, (ct[k] + dts * (tr[k] + src)) / (1 + dts * (lamb[k] + p.delT)));
                }
            }
            // ---- matrix ----
            for (int k = 0; k < NC; k++) {
                double Sq = SqAt(k, t);
                double dg = Math.max(0, g[k] - p.g0), Gs = dg / (p.Kgf + dg);
                eN[k] = Math.max(0, (e[k] + dt * (p.gEq * Sq + p.gEf * f[k] * Gs)) / (1 + dt * p.muE * (M1[k] + M2[k] + 0.2 * f[k])));
                kN[k] = Math.max(0, (kap[k] + dt * p.gK * f[k] * (1 + p.etaG * Gs)) / (1 + dt * (p.gK * f[k] * (1 + p.etaG * Gs) / p.kapMax + p.muK * f[k])));
            }
            // ---- cytokines (explicit diffusion sub-steps, implicit linear losses) ----
            double Dmax = Math.max(Math.max(p.Da, p.Dg), Math.max(p.Dv, p.Dw));
            int nc = (int) Math.ceil(dt / (0.2 * H * H / Dmax));
            double dtc = dt / nc;
            for (int s = 0; s < nc; s++) {
                double tt = t + s * dtc;
                cytokine(a, p.Da, dtc, 0, tt);
                cytokine(g, p.Dg, dtc, 1, tt);
                cytokine(v, p.Dv, dtc, 2, tt, fV);
                cytokine(w, p.Dw, dtc, 3, tt, fW);
            }
            // ---- swap ----
            System.arraycopy(nN, 0, n, 0, NC); System.arraycopy(M1N, 0, M1, 0, NC); System.arraycopy(M2N, 0, M2, 0, NC);
            System.arraycopy(EN, 0, E, 0, NC); System.arraycopy(fN, 0, f, 0, NC); System.arraycopy(bN, 0, b, 0, NC);
            System.arraycopy(LN, 0, L, 0, NC); System.arraycopy(cgN, 0, cg, 0, NC); System.arraycopy(cdN, 0, cd, 0, NC);
            System.arraycopy(eN, 0, e, 0, NC); System.arraycopy(kN, 0, kap, 0, NC);
            // ---- systemic scalars ----
            if (postOp && !sc.immuneLoss) Atot += Apre;
            if (!postOp) Apre = Atot;
            double Ainf = 0;
            for (int k = 0; k < NC; k++) if (zone[k] != 0) Ainf += Math.max(0, (n[k] - p.nb) + (M1[k] - p.M1b) + (M2[k] - p.M2b)) * DA;
            Isys = Ainf / p.AI;
            Pi = (Pi + dt * p.rPi * Atot / (Atot + p.KA)) / (1 + dt * (p.rPi * Atot / (Atot + p.KA) + p.delPi));
            t += dt;
            lastDt = dt;
        }
        double lastDt, Apre = 0;

        double[] cyN = new double[NC];
        void cytokine(double[] c, double D, double dt, int type, double tt) { cytokine(c, D, dt, type, tt, 1.0); }
        void cytokine(double[] c, double D, double dt, int type, double tt, double fac) {
            Arrays.fill(cyN, 0); laplace(c, D, cyN);
            for (int k = 0; k < NC; k++) {
                double Sq = SqAt(k, tt), prod, loss;
                double tum = cp[k] + cg[k];
                switch (type) {
                    case 0: // chemokine
                        prod = p.gA0 + p.gAq * Sq + p.gAn * n[k] + p.gA1 * M1[k] + p.gAe * e[k] + p.gAc * tum / p.KC;
                        loss = p.betaA; break;
                    case 1: // TGF-beta
                        prod = p.gG0 + p.gGq * Sq + p.gG2 * M2[k] + p.gGf * f[k] + p.gGc * tum / p.KC;
                        loss = p.betaG + p.clG * L[k]; break;
                    case 2: { // VEGF-A
                        double s2 = sig[k] * sig[k], th2 = p.thetaH * p.thetaH;
                        prod = p.gV0 + p.gVq * Sq + fac * (p.gV1 * M1[k] + p.gV2 * M2[k] + p.gVf * f[k]) * (1 + p.hV * th2 / (th2 + s2)) + p.gVc * tum / p.KC;
                        loss = p.muV * b[k] / (1 + c[k]) + p.betaV + p.clV * L[k]; break; }
                    default: // VEGF-C
                        prod = p.gW0 + fac * (p.gW1 * M1[k] + p.gW2 * M2[k]) + p.gWc * tum / p.KC;
                        loss = p.muW * L[k] / (1 + c[k]) + p.betaW + p.clW * L[k];
                }
                c[k] = Math.max(0, (c[k] + dt * (cyN[k] + prod)) / (1 + dt * loss));
            }
        }

        // ---------- driver ----------
        double bandMean(double[] q) { double s = 0; int c = 0; for (int k = 0; k < NC; k++) if (zone[k] == 1) { s += q[k]; c++; } return c == 0 ? 0 : s / c; }
        double sum(double[] q) { double s = 0; for (double d : q) s += d; return s * DA; }

        void run() throws IOException {
            tS = p.tPre;
            homeostasis();
            // prescribed primary tumour
            double Cp = p.CpFrac * p.KC;
            for (int j = 0; j < NY; j++) for (int i = 0; i < NX; i++) {
                double r = Math.hypot(xc(i), yc(j));
                cp[j * NX + i] = r <= p.r0 ? Cp : 0.0;
            }
            System.arraycopy(cp, 0, cpV, 0, NC);
            cpTot = sum(cp);
            tS = p.tPre;
            solvePressure();
            double nextP = 0, nextTs = 0;
            ts.append("t,phase,Pi,Isys,ct_tot,cd_tot,cg_tot,Ncommit,band_n,band_M1,band_M2,band_a,band_g,band_f,band_e,band_kap,band_v,band_b,band_w,band_L,band_Eeff,band_sigma,band_pi,mean_V_band,pr_band,Eeff_far\n");
            while (t < tS - 1e-9) {
                if (t >= nextP - 1e-9) { solvePressure(); nextP = t + 5.0; }
                step(Math.min(0.25, tS - t));
                if (t >= nextTs - 1e-9) { record(); nextTs = t + 5.0; }
            }
            if (sc.snapDays != null) snapshot("pre");
            surgery();
            solvePressure();
            double tEnd = tS + p.tPost; nextTs = t; nextP = t;
            int si = 0;
            while (t < tEnd - 1e-9) {
                double rel = t - tS;
                if (t >= nextP - 1e-9) { solvePressure(); nextP = t + (rel < 30 ? 1.0 : rel < 120 ? 2.0 : 10.0); }
                double dtN = rel < 3 ? 0.05 : rel < 60 ? 0.1 : 0.25;
                step(Math.min(dtN, tEnd - t));
                rel = t - tS;
                double bv = bandMean(v), bn = bandMean(n), bm1 = bandMean(M1), bm2 = bandMean(M2), bl = bandMean(L);
                if (bv > peakBandV) { peakBandV = bv; peakBandVday = rel; }
                if (bn > peakN) { peakN = bn; peakNday = rel; }
                if (bm1 > peakM1) { peakM1 = bm1; peakM1day = rel; }
                if (bm2 > peakM2) { peakM2 = bm2; peakM2day = rel; }
                if (bl < minBandL) minBandL = bl;
                if (Double.isNaN(Lrec50) && rel > 1 && bl >= 0.5) Lrec50 = rel;
                if (t >= nextTs - 1e-9) { record(); nextTs = t + (rel < 60 ? 0.5 : 2.0); }
                if (sc.snapDays != null && si < sc.snapDays.length && rel >= sc.snapDays[si] - 1e-9) { snapshot("d" + (int) Math.round(sc.snapDays[si])); si++; }
            }
            write();
        }

        void record() {
            double rel = t - tS;
            double farE = 0; int c = 0;
            for (int j = 0; j < NY; j += 4) for (int i = 0; i < NX; i += 4) {
                int k = j * NX + i; if (zone[k] == 0 && Math.hypot(xc(i), yc(j)) > 40) { farE += Eeff[k]; c++; }
            }
            double vb = 0; int cb = 0;
            for (int k = 0; k < NC; k++) if (zone[k] == 1) { vb += Vabs[k]; cb++; }
            ts.append(String.format(Locale.ROOT, "%.3f,%s,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g\n",
                    rel, postOp ? "post" : "pre", Pi, Isys, sum(ct), sum(cd), sum(cg), Ncommit,
                    bandMean(n), bandMean(M1), bandMean(M2), bandMean(a), bandMean(g), bandMean(f), bandMean(e), bandMean(kap),
                    bandMean(v), bandMean(b), bandMean(w), bandMean(L), bandMean(Eeff), bandMean(sig), bandMean(piEsc),
                    cb == 0 ? 0 : vb / cb, bandMean(pr), c == 0 ? 0 : farE / c));
        }

        void snapshot(String tag) throws IOException {
            Path dir = outDir.resolve("snap"); Files.createDirectories(dir);
            String[] names = {"ct", "cd", "cg", "L", "Vabs", "pr", "pl", "g", "v", "w", "b", "Eeff", "M2", "n", "escMap", "piEsc", "uabs", "kap"};
            double[][] arr = {ct, cd, cg, L, Vabs, pr, pl, g, v, w, b, Eeff, M2, n, escMap, piEsc, uabs, kap};
            try (DataOutputStream o = new DataOutputStream(new BufferedOutputStream(Files.newOutputStream(dir.resolve(tag + ".bin"))))) {
                o.writeInt(names.length); o.writeInt(NX); o.writeInt(NY);
                for (int q = 0; q < names.length; q++) { o.writeUTF(names[q]); for (int k = 0; k < NC; k++) o.writeFloat((float) arr[q][k]); }
            }
        }

        void write() throws IOException {
            Files.createDirectories(outDir);
            Files.writeString(outDir.resolve("timeseries.csv"), ts.toString());
            StringBuilder sb = new StringBuilder("day,vis_bin,vis_bin_local\n");
            for (int d = 0; d < NBIN; d++) sb.append(d).append(',').append(visBin[d]).append(',').append(visBinLocal[d]).append('\n');
            Files.writeString(outDir.resolve("visibility.csv"), sb.toString());
            StringBuilder ang = new StringBuilder("angle_deg,d0_5,d5_10,d10_20,d20_40,d40p\n");
            for (int q = 0; q < 36; q++) {
                ang.append(q * 10 + 5);
                for (int dc = 0; dc < 5; dc++) ang.append(',').append(angDist[q][dc]);
                ang.append('\n');
            }
            Files.writeString(outDir.resolve("angular.csv"), ang.toString());
            double v365 = 0, v730 = 0, l730 = 0;
            for (int d = 0; d < NBIN; d++) { if (d <= 365) v365 += visBin[d]; v730 += visBin[d]; l730 += visBinLocal[d]; }
            Map<String, Object> s = new LinkedHashMap<>();
            s.put("name", sc.name); s.put("margin_mm", sc.margin); s.put("theta_deg", sc.theta);
            s.put("immune_loss", sc.immuneLoss); s.put("wound", sc.wound); s.put("reroute", sc.reroute);
            s.put("t_slnb", sc.tSLNB);
            s.put("Nvis_365", v365); s.put("Nvis_730", v730); s.put("Nvis_local_730", l730);
            s.put("Ncommit_730", Ncommit); s.put("Ncommit_local", NcommitLocal); s.put("Ncommit_prox", NcommitProx); s.put("N_pre", Npre);
            s.put("excised_cd_frac", totalCdPre > 0 ? excisedCd / totalCdPre : 0); s.put("excised_ct_frac", totalCtPre > 0 ? excisedCt / totalCtPre : 0);
            s.put("cd_pre_total", totalCdPre); s.put("ct_pre_total", totalCtPre);
            s.put("lodged_post", lodgedPost); s.put("lodged_post_wound_zone", lodgedPostNear);
            s.put("peak_band_VEGFA", peakBandV); s.put("peak_band_VEGFA_day", peakBandVday);
            s.put("peak_band_n", peakN); s.put("peak_band_n_day", peakNday);
            s.put("peak_band_M1", peakM1); s.put("peak_band_M1_day", peakM1day);
            s.put("peak_band_M2", peakM2); s.put("peak_band_M2_day", peakM2day);
            s.put("band_L_recovery50_day", Lrec50); s.put("A_mm", A_); s.put("B_mm", B_); s.put("Bu_mm", Bu_);
            s.put("baseline_M1", p.M1b); s.put("baseline_M2", p.M2b); s.put("baseline_g", p.g0); s.put("baseline_v", p.vb);
            s.put("baseline_w", p.wb); s.put("baseline_a", p.ab); s.put("baseline_n", p.nb); s.put("muK", p.muK); s.put("upsT", p.upsT); s.put("betaB", p.betaB); s.put("betaL", p.betaL);
            s.put("rhoE", p.rhoE); s.put("lamSh", p.lamSh); s.put("primary_cells", cpTot);
            StringBuilder o = new StringBuilder("key,value\n");
            for (Map.Entry<String, Object> en : s.entrySet()) o.append(en.getKey()).append(',').append(en.getValue()).append('\n');
            Files.writeString(outDir.resolve("summary.csv"), o.toString());
        }
    }

    // ------------------------------------------------------------------ scenario list
    static List<Scenario> scenarios(String mode) {
        List<Scenario> L = new ArrayList<>();
        if (mode.startsWith("calib")) {
            for (String f : mode.substring(6).split(",")) {
                double fv = Double.parseDouble(f);
                for (double m : new double[]{10, 20}) L.add(new Scenario("cal_lam0x" + f + "_m" + (int) m).m(m).mul("lam0", fv));
            }
            return L;
        }
        L.add(new Scenario("baseline").snaps(1, 3, 7, 14, 21, 42, 60, 120, 365, 730));
        if (mode.equals("test")) return L;
        // factorial: immune loss x wound x rerouting
        for (int il = 0; il < 2; il++) for (int wo = 0; wo < 2; wo++) for (int rr = 0; rr < 2; rr++) {
            if (!(il == 1 && wo == 1 && rr == 1)) L.add(new Scenario("fact_I" + il + "W" + wo + "R" + rr).sw(il == 1, wo == 1, rr == 1));
            if (!(il == 1 && wo == 1 && rr == 1)) L.add(new Scenario("fact90_I" + il + "W" + wo + "R" + rr).th(90).sw(il == 1, wo == 1, rr == 1));
        }
        double[] ms = {2, 5, 7.5, 10, 12.5, 15, 20};
        for (double m : ms) {
            if (m != 10) L.add(new Scenario("margin_" + m + "_th0").m(m));
            L.add(new Scenario("margin_" + m + "_th90").m(m).th(90));
            L.add(new Scenario("removal_" + m).m(m).sw(true, false, false));
        }
        L.get(L.size() - 1);
        for (double th : new double[]{22.5, 45, 67.5}) L.add(new Scenario("orient_" + th).th(th));
        // snapshots for the perpendicular orientation at the baseline margin
        for (Scenario s : L) if (s.name.equals("margin_10.0_th90")) s.snaps(1, 3, 7, 14, 21, 42, 60, 120, 365, 730);
        L.add(new Scenario("slow_th0").mul("Vref", 0.25));
        L.add(new Scenario("slow_th0_R0").mul("Vref", 0.25).sw(true, true, false));
        L.add(new Scenario("slow_th90").th(90).mul("Vref", 0.25));
        L.add(new Scenario("slow_th90_R0").th(90).mul("Vref", 0.25).sw(true, true, false));
        L.add(new Scenario("slnb_prior").slnb(-28));
        L.add(new Scenario("slnb_simult").slnb(0));
        L.add(new Scenario("slnb_delayed").slnb(42));
        L.add(new Scenario("drug_nsaid_d0_7").drug(0, 0, 7));
        L.add(new Scenario("drug_nsaid_d7_14").drug(0, 7, 7));
        L.add(new Scenario("drug_beta_dm2_28").drug(1, -2, 30));
        L.add(new Scenario("drug_antiVEGFA_d0_28").drug(2, 0, 28));
        L.add(new Scenario("drug_antiVEGFR3_d3_24").drug(3, 3, 21));
        L.add(new Scenario("drug_nsaid_beta").drug(0, 0, 7).drug(1, -2, 30));
        for (double st : new double[]{0, 3, 7, 14}) for (double du : new double[]{3, 7, 14, 28})
            L.add(new Scenario("win_nsaid_s" + (int) st + "_d" + (int) du).drug(0, st, du));
        String[] sens = {"lam1", "lam0", "sG", "sM", "omV", "omNET", "etaPi", "delPi", "epsU", "epsQ", "Vref", "clG", "sAlpha", "kE", "sI"};
        for (String q : sens) { L.add(new Scenario("sens_" + q + "_lo").mul(q, 0.5)); L.add(new Scenario("sens_" + q + "_hi").mul(q, 1.5)); }
        return L;
    }

    public static void main(String[] args) throws Exception {
        String mode = args.length > 0 ? args[0] : "test";
        int threads = args.length > 1 ? Integer.parseInt(args[1]) : Math.max(1, Runtime.getRuntime().availableProcessors() - 1);
        Path root = Paths.get(args.length > 2 ? args[2] : "results");
        List<Scenario> list = scenarios(mode);
        if (args.length > 3) { String only = args[3]; list.removeIf(s -> !s.name.matches(only)); }
        ExecutorService ex = Executors.newFixedThreadPool(threads);
        List<Future<?>> fut = new ArrayList<>();
        long t0 = System.currentTimeMillis();
        for (Scenario sc : list) {
            fut.add(ex.submit(() -> {
                try {
                    P p = new P();
                    if (System.getProperty("tPost") != null) p.tPost = Double.parseDouble(System.getProperty("tPost"));
                    if (System.getProperty("tPre") != null) p.tPre = Double.parseDouble(System.getProperty("tPre"));
                    for (Map.Entry<String, Double> m : sc.mult.entrySet()) {
                        Field fl = P.class.getField(m.getKey()); fl.setDouble(p, fl.getDouble(p) * m.getValue());
                    }
                    long s0 = System.currentTimeMillis();
                    if (System.getProperty("snapAll") != null && sc.snapDays == null) sc.snaps(7, 60, 200, 365, 500, 730);
                    Sim sim = new Sim(p, sc, root.resolve(sc.name));
                    sim.run();
                    System.out.printf(Locale.ROOT, "%-28s done in %5.1f s  Nvis730=%.4g Ncommit=%.4g Npre=%.4g  cg calls=%d iters=%d time=%.1fs%n", sc.name,
                            (System.currentTimeMillis() - s0) / 1000.0, Arrays.stream(sim.visBin).sum(), sim.Ncommit, sim.Npre, sim.cgCalls, sim.cgIters, sim.cgNanos / 1e9);
                } catch (Exception e) { e.printStackTrace(); }
                return null;
            }));
        }
        for (Future<?> f : fut) f.get();
        ex.shutdown();
        System.out.printf("all done in %.1f s%n", (System.currentTimeMillis() - t0) / 1000.0);
    }
}
