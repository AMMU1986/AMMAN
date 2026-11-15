import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.List;

/**
 * Renders the eight manuscript figures from the simulation outputs of LymphaticScarModel using Java2D only.
 * Usage: java LymphaticFigures <resultsDir> <figureDir>
 */
public class LymphaticFigures {

    static Path RES, OUT;
    static final String FONT = "Noto Sans";
    static final Color[] PAL = {new Color(0, 0, 0), new Color(230, 159, 0), new Color(86, 180, 233), new Color(0, 158, 115),
            new Color(213, 94, 0), new Color(0, 114, 178), new Color(204, 121, 167), new Color(120, 120, 120), new Color(240, 200, 30)};
    static double CAL = 1.0;     // converts expected lesions at the reference shedding rate to the calibrated scale
    static final double TARGET_P = 0.10;

    // ================================================================== data helpers
    static Map<String, String> summary(String sc) throws IOException {
        Map<String, String> m = new LinkedHashMap<>();
        for (String ln : Files.readAllLines(RES.resolve(sc).resolve("summary.csv"))) {
            if (ln.startsWith("key,")) continue;
            int c = ln.indexOf(','); m.put(ln.substring(0, c), ln.substring(c + 1));
        }
        return m;
    }
    static double sv(String sc, String k) throws IOException { return Double.parseDouble(summary(sc).get(k)); }
    static Map<String, double[]> csv(Path p) throws IOException {
        List<String> lines = Files.readAllLines(p);
        String[] hd = lines.get(0).split(",");
        Map<String, double[]> m = new LinkedHashMap<>();
        int n = lines.size() - 1;
        for (String h : hd) m.put(h, new double[n]);
        for (int r = 0; r < n; r++) {
            String[] f = lines.get(r + 1).split(",");
            for (int c = 0; c < hd.length; c++) {
                double v;
                try { v = Double.parseDouble(f[c]); } catch (Exception e) { v = f[c].equals("post") ? 1 : 0; }
                m.get(hd[c])[r] = v;
            }
        }
        return m;
    }
    static Map<String, double[]> ts(String sc) throws IOException { return csv(RES.resolve(sc).resolve("timeseries.csv")); }
    /** Cumulative probability of a visible recurrence by post-operative day (calibrated). */
    static double[] cumP(String sc) throws IOException {
        Map<String, double[]> v = csv(RES.resolve(sc).resolve("visibility.csv"));
        double[] b = v.get("vis_bin"), out = new double[b.length];
        double s = 0;
        for (int i = 0; i < b.length; i++) { s += b[i]; out[i] = 1 - Math.exp(-CAL * s); }
        return out;
    }
    static double P2(String sc) throws IOException { return 1 - Math.exp(-CAL * sv(sc, "Nvis_730")); }
    static double P1(String sc) throws IOException { return 1 - Math.exp(-CAL * sv(sc, "Nvis_365")); }
    static double Ploc(String sc) throws IOException { return 1 - Math.exp(-CAL * sv(sc, "Nvis_local_730")); }
    static double Ptr(String sc) throws IOException { return 1 - Math.exp(-CAL * (sv(sc, "Nvis_730") - sv(sc, "Nvis_local_730"))); }
    static boolean exists(String sc) { return Files.exists(RES.resolve(sc).resolve("summary.csv")); }

    static class Snap { int nx, ny; Map<String, float[]> f = new HashMap<>(); }
    static Snap snap(String sc, String tag) throws IOException {
        Snap s = new Snap();
        try (DataInputStream in = new DataInputStream(new BufferedInputStream(Files.newInputStream(RES.resolve(sc).resolve("snap").resolve(tag + ".bin"))))) {
            int n = in.readInt(); s.nx = in.readInt(); s.ny = in.readInt();
            for (int q = 0; q < n; q++) {
                String nm = in.readUTF(); float[] a = new float[s.nx * s.ny];
                for (int k = 0; k < a.length; k++) a[k] = in.readFloat();
                s.f.put(nm, a);
            }
        }
        return s;
    }

    // ================================================================== drawing toolkit
    static class Fig {
        BufferedImage img; Graphics2D g; int W, H;
        Fig(int w, int h) {
            W = w; H = h; img = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB); g = img.createGraphics();
            g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
            g.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE);
            g.setRenderingHint(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);
            g.setColor(Color.WHITE); g.fillRect(0, 0, w, h);
        }
        void save(String name) throws IOException { Files.createDirectories(OUT); ImageIO.write(img, "png", OUT.resolve(name).toFile()); System.out.println("wrote " + name); }
        void panelLabel(String s, double x, double y) { text(s, x, y, 46, true, Color.BLACK, -1); }
        /** Rich text: '_' subscript, '^' superscript (single char or {group}). align -1 left, 0 centre, 1 right. */
        double text(String s, double x, double y, float size, boolean bold, Color c, int align) {
            double w = textWidth(s, size, bold);
            double x0 = align < 0 ? x : align == 0 ? x - w / 2 : x - w;
            drawRich(s, x0, y, size, bold, c, true);
            return w;
        }
        double textWidth(String s, float size, boolean bold) { return drawRich(s, 0, 0, size, bold, Color.BLACK, false); }
        double drawRich(String s, double x, double y, float size, boolean bold, Color c, boolean draw) {
            double cx = x; int i = 0;
            Font base = new Font(FONT, bold ? Font.BOLD : Font.PLAIN, Math.round(size));
            Font small = new Font(FONT, bold ? Font.BOLD : Font.PLAIN, Math.round(size * 0.68f));
            g.setColor(c);
            while (i < s.length()) {
                char ch = s.charAt(i);
                if ((ch == '_' || ch == '^') && i + 1 < s.length()) {
                    String grp; int j;
                    if (s.charAt(i + 1) == '{') { j = s.indexOf('}', i + 2); grp = s.substring(i + 2, j); i = j + 1; }
                    else { grp = s.substring(i + 1, i + 2); i += 2; }
                    g.setFont(small);
                    double dy = ch == '_' ? size * 0.25 : -size * 0.42;
                    if (draw) g.drawString(grp, (float) cx, (float) (y + dy));
                    cx += g.getFontMetrics().stringWidth(grp);
                } else {
                    int j = i; while (j < s.length() && s.charAt(j) != '_' && s.charAt(j) != '^') j++;
                    String seg = s.substring(i, j); g.setFont(base);
                    if (draw) g.drawString(seg, (float) cx, (float) y);
                    cx += g.getFontMetrics().stringWidth(seg); i = j;
                }
            }
            return cx - x;
        }
        void vtext(String s, double x, double y, float size, Color c) {   // rotated -90, centred at (x,y)
            AffineTransform old = g.getTransform();
            g.translate(x, y); g.rotate(-Math.PI / 2);
            double w = textWidth(s, size, false);
            drawRich(s, -w / 2, 0, size, false, c, true);
            g.setTransform(old);
        }
    }

    static class Axes {
        Fig f; double X, Y, Wd, Ht; double x0, x1, y0, y1; boolean logy = false, logx = false;
        float fs = 30f;
        Axes(Fig f, double X, double Y, double W, double H) { this.f = f; this.X = X; this.Y = Y; this.Wd = W; this.Ht = H; }
        Axes lim(double a, double b, double c, double d) { x0 = a; x1 = b; y0 = c; y1 = d; return this; }
        double px(double x) { return logx ? X + Wd * (Math.log10(x) - Math.log10(x0)) / (Math.log10(x1) - Math.log10(x0)) : X + Wd * (x - x0) / (x1 - x0); }
        double py(double y) { return logy ? Y + Ht - Ht * (Math.log10(y) - Math.log10(y0)) / (Math.log10(y1) - Math.log10(y0)) : Y + Ht - Ht * (y - y0) / (y1 - y0); }
        void frame() {
            f.g.setColor(Color.BLACK); f.g.setStroke(new BasicStroke(2.2f));
            f.g.draw(new Rectangle2D.Double(X, Y, Wd, Ht));
        }
        void clip(boolean on) { if (on) f.g.setClip(new Rectangle2D.Double(X, Y, Wd, Ht)); else f.g.setClip(null); }
        void xticks(double[] t, String fmt) {
            f.g.setStroke(new BasicStroke(2f));
            for (double v : t) {
                double x = px(v); f.g.setColor(Color.BLACK);
                f.g.draw(new Line2D.Double(x, Y + Ht, x, Y + Ht + 10));
                f.text(fmtv(v, fmt), x, Y + Ht + 12 + fs, fs, false, Color.BLACK, 0);
            }
        }
        void yticks(double[] t, String fmt) {
            f.g.setStroke(new BasicStroke(2f));
            for (double v : t) {
                double y = py(v); f.g.setColor(Color.BLACK);
                f.g.draw(new Line2D.Double(X - 10, y, X, y));
                f.text(fmtv(v, fmt), X - 16, y + fs * 0.35, fs, false, Color.BLACK, 1);
            }
        }
        void grid(double[] ty) {
            f.g.setStroke(new BasicStroke(1.2f)); f.g.setColor(new Color(225, 225, 225));
            for (double v : ty) f.g.draw(new Line2D.Double(X, py(v), X + Wd, py(v)));
        }
        static String fmtv(double v, String fmt) {
            if (fmt.equals("pow")) { int e = (int) Math.round(Math.log10(v)); return e == 0 ? "1" : e == 1 ? "10" : "10^{" + e + "}"; }
            if (fmt.equals("pct")) return String.format(Locale.ROOT, "%.0f%%", 100 * v);
            return String.format(Locale.ROOT, fmt, v);
        }
        void xlabel(String s) { f.text(s, X + Wd / 2, Y + Ht + 2.4 * fs + 22, fs * 1.08f, false, Color.BLACK, 0); }
        void ylabel(String s) { f.vtext(s, X - 3.1 * fs - 8, Y + Ht / 2, fs * 1.08f, Color.BLACK); }
        void title(String s) { f.text(s, X + Wd / 2, Y - 18, fs * 1.08f, true, Color.BLACK, 0); }
        void line(double[] xs, double[] ys, Color c, float w, float[] dash) {
            Path2D.Double p = new Path2D.Double(); boolean st = false;
            for (int i = 0; i < xs.length; i++) {
                if (Double.isNaN(ys[i]) || (logy && ys[i] <= 0)) { st = false; continue; }
                double x = px(xs[i]), y = py(ys[i]);
                if (!st) { p.moveTo(x, y); st = true; } else p.lineTo(x, y);
            }
            f.g.setColor(c);
            f.g.setStroke(dash == null ? new BasicStroke(w, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) : new BasicStroke(w, BasicStroke.CAP_BUTT, BasicStroke.JOIN_ROUND, 10f, dash, 0f));
            clip(true); f.g.draw(p); clip(false);
        }
        void markers(double[] xs, double[] ys, Color c, double r) {
            for (int i = 0; i < xs.length; i++) {
                double x = px(xs[i]), y = py(ys[i]);
                f.g.setColor(Color.WHITE); f.g.fill(new Ellipse2D.Double(x - r, y - r, 2 * r, 2 * r));
                f.g.setColor(c); f.g.setStroke(new BasicStroke(3f)); f.g.draw(new Ellipse2D.Double(x - r, y - r, 2 * r, 2 * r));
                f.g.fill(new Ellipse2D.Double(x - r * 0.55, y - r * 0.55, 1.1 * r, 1.1 * r));
            }
        }
        void vspan(double a, double b, Color c) { f.g.setColor(c); double xa = px(a), xb = px(b); clip(true); f.g.fill(new Rectangle2D.Double(xa, Y, xb - xa, Ht)); clip(false); }
        void legend(String[] lab, Color[] col, float[][] dash, double lx, double ly, float size) {
            double y = ly;
            for (int i = 0; i < lab.length; i++) {
                f.g.setColor(col[i]);
                f.g.setStroke(dash == null || dash[i] == null ? new BasicStroke(5f) : new BasicStroke(5f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_ROUND, 10f, dash[i], 0f));
                f.g.draw(new Line2D.Double(lx, y - size * 0.32, lx + 60, y - size * 0.32));
                f.text(lab[i], lx + 74, y, size, false, Color.BLACK, -1);
                y += size * 1.35;
            }
        }
    }

    // ------------------------------------------------------------------ colour maps
    static final int[][] VIRIDIS = {{68, 1, 84}, {72, 40, 120}, {62, 74, 137}, {49, 104, 142}, {38, 130, 142}, {31, 158, 137}, {53, 183, 121}, {109, 205, 89}, {180, 222, 44}, {253, 231, 37}};
    static final int[][] MAGMA = {{0, 0, 4}, {28, 16, 68}, {79, 18, 123}, {129, 37, 129}, {181, 54, 122}, {229, 80, 100}, {251, 135, 97}, {254, 194, 135}, {252, 253, 191}};
    static final int[][] RDBU = {{5, 48, 97}, {33, 102, 172}, {67, 147, 195}, {146, 197, 222}, {209, 229, 240}, {247, 247, 247}, {253, 219, 199}, {244, 165, 130}, {214, 96, 77}, {178, 24, 43}, {103, 0, 31}};
    static Color cmap(int[][] m, double t) {
        t = Math.max(0, Math.min(1, t)); double s = t * (m.length - 1); int i = (int) Math.floor(s); if (i >= m.length - 1) i = m.length - 2;
        double fr = s - i;
        return new Color((int) Math.round(m[i][0] + fr * (m[i + 1][0] - m[i][0])), (int) Math.round(m[i][1] + fr * (m[i + 1][1] - m[i][1])), (int) Math.round(m[i][2] + fr * (m[i + 1][2] - m[i][2])));
    }

    /** Heat map of a 160x160 field (cell-centred, domain [-80,80]^2) inside axes limits. */
    static void heat(Axes ax, float[] fld, int nx, int ny, int[][] cm, double vmin, double vmax, boolean log) {
        int pw = (int) Math.round(ax.Wd), ph = (int) Math.round(ax.Ht);
        BufferedImage im = new BufferedImage(pw, ph, BufferedImage.TYPE_INT_RGB);
        for (int py = 0; py < ph; py++) for (int pxl = 0; pxl < pw; pxl++) {
            double x = ax.x0 + (pxl + 0.5) / pw * (ax.x1 - ax.x0), y = ax.y1 - (py + 0.5) / ph * (ax.y1 - ax.y0);
            double gx = (x + 80) - 0.5, gy = (y + 80) - 0.5;
            gx = Math.max(0, Math.min(nx - 1.0001, gx)); gy = Math.max(0, Math.min(ny - 1.0001, gy));
            int i = (int) gx, j = (int) gy; double a = gx - i, b = gy - j; int k = j * nx + i;
            double v = (1 - a) * (1 - b) * fld[k] + a * (1 - b) * fld[k + 1] + (1 - a) * b * fld[k + nx] + a * b * fld[k + nx + 1];
            double t = log ? (Math.log10(Math.max(v, vmin)) - Math.log10(vmin)) / (Math.log10(vmax) - Math.log10(vmin)) : (v - vmin) / (vmax - vmin);
            im.setRGB(pxl, py, cmap(cm, t).getRGB());
        }
        ax.f.g.drawImage(im, (int) Math.round(ax.X), (int) Math.round(ax.Y), null);
    }
    static void colorbar(Fig f, double X, double Y, double W, double H, int[][] cm, double vmin, double vmax, boolean log, double[] ticks, String fmt, String label) {
        for (int i = 0; i < (int) H; i++) { f.g.setColor(cmap(cm, 1 - i / H)); f.g.fillRect((int) X, (int) (Y + i), (int) W, 1); }
        f.g.setColor(Color.BLACK); f.g.setStroke(new BasicStroke(1.6f)); f.g.draw(new Rectangle2D.Double(X, Y, W, H));
        for (double tv : ticks) {
            double t = log ? (Math.log10(tv) - Math.log10(vmin)) / (Math.log10(vmax) - Math.log10(vmin)) : (tv - vmin) / (vmax - vmin);
            double y = Y + H - t * H;
            f.g.draw(new Line2D.Double(X + W, y, X + W + 7, y));
            f.text(Axes.fmtv(tv, fmt), X + W + 11, y + 9, 25, false, Color.BLACK, -1);
        }
        f.vtext(label, X + W + 112, Y + H / 2, 25, Color.BLACK);
    }
    static void ellipse(Axes ax, double A, double B, double thetaDeg, Color c, float w, float[] dash) {
        Graphics2D g = ax.f.g; AffineTransform old = g.getTransform();
        double sx = ax.Wd / (ax.x1 - ax.x0), sy = ax.Ht / (ax.y1 - ax.y0);
        g.translate(ax.px(0), ax.py(0)); g.scale(sx, -sy); g.rotate(Math.toRadians(thetaDeg));
        g.setColor(c);
        g.setStroke(dash == null ? new BasicStroke((float) (w / sx)) : new BasicStroke((float) (w / sx), BasicStroke.CAP_BUTT, BasicStroke.JOIN_ROUND, 10f, scale(dash, 1 / sx), 0f));
        g.setTransform(old);
        g.setClip(new Rectangle2D.Double(ax.X, ax.Y, ax.Wd, ax.Ht));
        g.translate(ax.px(0), ax.py(0)); g.scale(sx, -sy); g.rotate(Math.toRadians(thetaDeg));
        g.draw(new Ellipse2D.Double(-A, -B, 2 * A, 2 * B));
        g.setTransform(old); g.setClip(null);
    }
    static void scarLine(Axes ax, double A, double thetaDeg, Color c, float w) {
        double th = Math.toRadians(thetaDeg);
        ax.f.g.setColor(c); ax.f.g.setStroke(new BasicStroke(w, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        ax.f.g.draw(new Line2D.Double(ax.px(-A * Math.cos(th)), ax.py(-A * Math.sin(th)), ax.px(A * Math.cos(th)), ax.py(A * Math.sin(th))));
    }
    static float[] scale(float[] d, double s) { float[] o = new float[d.length]; for (int i = 0; i < d.length; i++) o[i] = (float) (d[i] * s); return o; }

    /** Streamlines of the emboli velocity field derived from lymph pressure and lymphatic density. */
    static void streamlines(Axes ax, Snap s, Color c) {
        float[] pl = s.f.get("pl"), L = s.f.get("L");
        int nx = s.nx;
        Graphics2D g = ax.f.g; g.setColor(c); g.setStroke(new BasicStroke(2.2f));
        ax.clip(true);
        for (double y0 = ax.y0 + 4; y0 < ax.y1; y0 += 8) {
            double x = ax.x0 + 1, y = y0; Path2D.Double p = new Path2D.Double(); p.moveTo(ax.px(x), ax.py(y));
            int arrowAt = 40, st = 0;
            for (int it = 0; it < 400; it++) {
                double[] v = vel(pl, L, nx, x, y);
                double sp = Math.hypot(v[0], v[1]); if (sp < 1e-6) break;
                double ds = 0.5; x += ds * v[0] / sp; y += ds * v[1] / sp;
                if (x < ax.x0 || x > ax.x1 || y < ax.y0 || y > ax.y1) break;
                p.lineTo(ax.px(x), ax.py(y)); st++;
                if (st == arrowAt) { arrow(g, ax.px(x), ax.py(y), v[0], -v[1]); arrowAt += 70; }
            }
            g.draw(p);
        }
        ax.clip(false);
    }
    static double[] vel(float[] pl, float[] L, int nx, double x, double y) {
        double gx = x + 80 - 0.5, gy = y + 80 - 0.5; int i = (int) Math.max(1, Math.min(nx - 2, Math.round(gx))), j = (int) Math.max(1, Math.min(nx - 2, Math.round(gy)));
        int k = j * nx + i;
        double fac = (L[k] + 0.002) / (L[k] + 0.2);
        return new double[]{-fac * (pl[k + 1] - pl[k - 1]) / 2, -fac * (pl[k + nx] - pl[k - nx]) / 2};
    }
    static void arrow(Graphics2D g, double x, double y, double vx, double vy) {
        double a = Math.atan2(vy, vx), L = 16;
        Path2D.Double p = new Path2D.Double();
        p.moveTo(x, y); p.lineTo(x - L * Math.cos(a - 0.45), y - L * Math.sin(a - 0.45));
        p.lineTo(x - L * Math.cos(a + 0.45), y - L * Math.sin(a + 0.45)); p.closePath(); g.fill(p);
    }

    static double[] seq(int n) { double[] d = new double[n]; for (int i = 0; i < n; i++) d[i] = i; return d; }
    static double[] div(double[] a, double s) { double[] o = a.clone(); for (int i = 0; i < o.length; i++) o[i] /= s; return o; }
    static double[][] postWindow(Map<String, double[]> t, String col, double tmax) {
        List<Double> xs = new ArrayList<>(), ys = new ArrayList<>();
        double[] tt = t.get("t"), ph = t.get("phase"), c = t.get(col);
        for (int i = 0; i < tt.length; i++) if (ph[i] > 0.5 && tt[i] <= tmax) { xs.add(tt[i]); ys.add(c[i]); }
        double[][] o = new double[2][xs.size()];
        for (int i = 0; i < xs.size(); i++) { o[0][i] = xs.get(i); o[1][i] = ys.get(i); }
        return o;
    }

    // ================================================================== Figure 1: schematic
    static void fig1() throws IOException {
        Fig f = new Fig(2400, 1560);
        Graphics2D g = f.g;
        // Panel A: dermal sheet before surgery
        f.panelLabel("A", 30, 70);
        f.text("Dermal sheet before excision", 600, 70, 34, true, Color.BLACK, 0);
        double ax = 90, ay = 110, aw = 1060, ah = 600;
        g.setColor(new Color(252, 236, 222)); g.fill(new RoundRectangle2D.Double(ax, ay, aw, ah, 30, 30));
        g.setColor(new Color(150, 120, 100)); g.setStroke(new BasicStroke(2.5f)); g.draw(new RoundRectangle2D.Double(ax, ay, aw, ah, 30, 30));
        Random rnd = new Random(7);
        g.setColor(new Color(60, 140, 200)); g.setStroke(new BasicStroke(3.2f));
        for (int k = 0; k < 9; k++) {
            double y = ay + 50 + k * 62; Path2D.Double p = new Path2D.Double(); p.moveTo(ax + 20, y);
            for (double x = ax + 20; x <= ax + aw - 20; x += 20) p.lineTo(x, y + 9 * Math.sin(x / 55.0 + k) + (k - 4) * (x - ax) * -0.035);
            g.draw(p);
        }
        double cx = ax + 330, cy = ay + ah / 2;
        g.setColor(new Color(40, 25, 20)); g.fill(new Ellipse2D.Double(cx - 34, cy - 34, 68, 68));
        f.text("primary", cx, cy - 52, 27, true, Color.BLACK, 0);
        for (int k = 0; k < 70; k++) {
            double x = cx + 40 + Math.abs(rnd.nextGaussian()) * 230, y = cy + rnd.nextGaussian() * (35 + 0.18 * (x - cx));
            if (x > ax + aw - 25) continue;
            g.setColor(new Color(200, 30, 60)); g.fill(new Ellipse2D.Double(x - 6, y - 6, 12, 12));
        }
        for (int k = 0; k < 18; k++) {
            double x = cx + 60 + rnd.nextDouble() * 600, y = cy + rnd.nextGaussian() * 60;
            g.setColor(new Color(120, 40, 160)); g.fill(new Ellipse2D.Double(x - 8, y - 8, 16, 16));
            g.setColor(Color.WHITE); g.fill(new Ellipse2D.Double(x - 3, y - 3, 6, 6));
        }
        g.setColor(Color.BLACK); g.setStroke(new BasicStroke(5f));
        g.draw(new Line2D.Double(ax + aw - 160, ay + ah + 45, ax + aw + 40, ay + ah + 45)); arrow(g, ax + aw + 40, ay + ah + 45, 1, 0);
        f.text("lymph drainage to regional node basin (+x)", ax + aw - 170, ay + ah + 55, 27, false, Color.BLACK, 1);
        // legend A
        double lx = ax + 20, ly = ay + ah + 110;
        g.setColor(new Color(60, 140, 200)); g.setStroke(new BasicStroke(4f)); g.draw(new Line2D.Double(lx, ly - 9, lx + 50, ly - 9));
        f.text("dermal lymphatic plexus, L", lx + 60, ly, 26, false, Color.BLACK, -1);
        g.setColor(new Color(200, 30, 60)); g.fill(new Ellipse2D.Double(lx + 420, ly - 15, 12, 12));
        f.text("in-transit emboli, c_t", lx + 440, ly, 26, false, Color.BLACK, -1);
        g.setColor(new Color(120, 40, 160)); g.fill(new Ellipse2D.Double(lx + 720, ly - 17, 16, 16));
        f.text("dormant lodged cells, c_d", lx + 744, ly, 26, false, Color.BLACK, -1);

        // Panel B: excision, closure, undermining
        f.panelLabel("B", 1240, 70);
        f.text("Excision geometry and primary closure", 1810, 70, 34, true, Color.BLACK, 0);
        double bx = 1300, by = 120, bw = 1040, bh = 590;
        g.setColor(new Color(252, 236, 222)); g.fill(new RoundRectangle2D.Double(bx, by, bw, bh, 30, 30));
        g.setColor(new Color(150, 120, 100)); g.setStroke(new BasicStroke(2.5f)); g.draw(new RoundRectangle2D.Double(bx, by, bw, bh, 30, 30));
        double ex = bx + 300, ey = by + bh / 2, B = 70, A = 210, Bu = 170;
        g.setColor(new Color(255, 214, 160)); g.fill(new Ellipse2D.Double(ex - A, ey - Bu, 2 * A, 2 * Bu));
        g.setColor(new Color(235, 150, 70)); g.setStroke(new BasicStroke(2.5f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_ROUND, 10f, new float[]{12, 8}, 0)); g.draw(new Ellipse2D.Double(ex - A, ey - Bu, 2 * A, 2 * Bu));
        g.setColor(Color.WHITE); g.fill(new Ellipse2D.Double(ex - A, ey - B, 2 * A, 2 * B));
        g.setColor(Color.BLACK); g.setStroke(new BasicStroke(3f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_ROUND, 10f, new float[]{16, 10}, 0)); g.draw(new Ellipse2D.Double(ex - A, ey - B, 2 * A, 2 * B));
        g.setColor(new Color(40, 25, 20)); g.fill(new Ellipse2D.Double(ex - 20, ey - 20, 40, 40));
        g.setStroke(new BasicStroke(2.5f)); g.setColor(Color.BLACK);
        g.draw(new Line2D.Double(ex, ey, ex, ey - B)); f.text("B = r_0 + m", ex + 12, ey - B / 2 + 8, 25, false, Color.BLACK, -1);
        g.draw(new Line2D.Double(ex, ey + 4, ex + A, ey + 4)); f.text("A = 3B", ex + A / 2, ey + 34, 25, false, Color.BLACK, 0);
        f.text("undermined zone U (B_u = 3B + 10 mm)", ex, ey - Bu - 14, 25, false, new Color(170, 90, 20), 0);
        // after closure
        double cx2 = bx + 800;
        g.setColor(new Color(255, 214, 160)); g.fill(new Ellipse2D.Double(cx2 - 150, ey - Bu, 300, 2 * Bu));
        g.setColor(new Color(235, 150, 70)); g.setStroke(new BasicStroke(2.5f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_ROUND, 10f, new float[]{12, 8}, 0)); g.draw(new Ellipse2D.Double(cx2 - 150, ey - Bu, 300, 2 * Bu));
        g.setColor(new Color(170, 30, 30)); g.setStroke(new BasicStroke(10f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        g.draw(new Line2D.Double(cx2 - 150, ey, cx2 + 150, ey));
        g.setColor(Color.BLACK); g.setStroke(new BasicStroke(3f));
        for (int s = -1; s <= 1; s += 2) for (int k = -1; k <= 1; k++) {
            double x = cx2 + k * 70; g.draw(new Line2D.Double(x, ey + s * 120, x, ey + s * 30)); arrow(g, x, ey + s * 30, 0, -s);
        }
        f.text("scar band S (|y'| < 2 mm)", cx2, ey + Bu + 36, 25, false, new Color(170, 30, 30), 0);
        g.setStroke(new BasicStroke(4f)); g.setColor(Color.BLACK); g.draw(new Line2D.Double(bx + 545, ey, bx + 615, ey)); arrow(g, bx + 615, ey, 1, 0);
        f.text("closure", bx + 580, ey - 18, 25, false, Color.BLACK, 0);
        f.text("rotation angle \u03b8 of the long axis relative to the drainage axis", bx + bw / 2, by + bh + 50, 26, false, Color.BLACK, 0);

        // Panel C: mechanisms
        f.panelLabel("C", 30, 920);
        f.text("Three post-excision mechanisms acting on dormant cells", 1200, 920, 34, true, Color.BLACK, 0);
        g.translate(0, 60);
        String[][] boxes = {
                {"Loss of the primary antigen source", "systemic priming \u03a0(t) decays", "fewer cytotoxic lymphocytes E"},
                {"Wound-healing cascade", "platelets, neutrophils, M1, then M2 and TGF-\u03b2", "suppressed E_{eff}; VEGF-A and NETs wake cells"},
                {"Lymphatic transection and regrowth", "stasis and lodging of in-transit emboli", "impaired clearance; flow-guided regrowth"}};
        Color[] bc = {new Color(222, 235, 247), new Color(253, 226, 210), new Color(214, 239, 225)};
        for (int i = 0; i < 3; i++) {
            double x = 90 + i * 760, y = 910;
            g.setColor(bc[i]); g.fill(new RoundRectangle2D.Double(x, y, 700, 230, 30, 30));
            g.setColor(new Color(90, 90, 90)); g.setStroke(new BasicStroke(2.5f)); g.draw(new RoundRectangle2D.Double(x, y, 700, 230, 30, 30));
            f.text(boxes[i][0], x + 350, y + 55, 29, true, Color.BLACK, 0);
            f.text(boxes[i][1], x + 350, y + 115, 26, false, Color.BLACK, 0);
            f.text(boxes[i][2], x + 350, y + 170, 26, false, Color.BLACK, 0);
            g.setColor(Color.BLACK); g.setStroke(new BasicStroke(4f));
            g.draw(new Line2D.Double(x + 350, y + 232, 1200, 1270)); arrow(g, 1200, 1270, 1200 - (x + 350), 1270 - (y + 232));
        }
        g.setColor(new Color(245, 245, 245)); g.fill(new RoundRectangle2D.Double(560, 1275, 1280, 190, 30, 30));
        g.setColor(new Color(90, 90, 90)); g.setStroke(new BasicStroke(2.5f)); g.draw(new RoundRectangle2D.Double(560, 1275, 1280, 190, 30, 30));
        f.text("Dormant lodged cells c_d exit dormancy at rate \u03c9 and escape with probability \u03c0(\u03b1, \u03bc)", 1200, 1335, 27, false, Color.BLACK, 0);
        f.text("giving a visible satellite (within 2 cm of scar) or in-transit recurrence after a delay \u03c4_{vis}", 1200, 1395, 27, false, Color.BLACK, 0);
        f.text("cumulative risk P(t) = 1 - exp[-N(t)]", 1200, 1450, 27, true, Color.BLACK, 0);
        f.save("Figure_1_Model_Schematic.png");
    }

    // ================================================================== Figure 2: wound-healing time courses
    static void fig2() throws IOException {
        Map<String, double[]> t = ts("baseline");
        Map<String, String> s = summary("baseline");
        double M1b = Double.parseDouble(s.get("baseline_M1")), M2b = Double.parseDouble(s.get("baseline_M2")), gb = Double.parseDouble(s.get("baseline_g"));
        double vb = Double.parseDouble(s.get("baseline_v")), wb = Double.parseDouble(s.get("baseline_w")), ab = Double.parseDouble(s.get("baseline_a"));
        Fig f = new Fig(2400, 1750);
        double[][] pos = {{230, 120}, {1440, 120}, {230, 960}, {1440, 960}};
        String[] lab = {"A", "B", "C", "D"};
        String[] ttl = {"Inflammatory cells (scar band)", "Matrix remodelling (scar band)", "Vascular and lymphatic remodelling", "Immune effector suppression"};
        for (int p = 0; p < 4; p++) {
            Axes a = new Axes(f, pos[p][0], pos[p][1], 900, 560);
            if (p < 3) { a.logy = true; a.lim(0, 60, 0.02, 40); } else a.lim(0, 60, 0, 1.6);
            if (p == 0) { a.vspan(1, 2, new Color(255, 230, 230)); a.vspan(3, 7, new Color(230, 240, 255)); }
            if (p == 1) a.vspan(5, 14, new Color(235, 245, 225));
            if (p == 2) a.vspan(14, 56, new Color(230, 245, 250));
            if (p == 3) a.vspan(0, 14, new Color(255, 240, 225));
            double[] yt = p == 3 ? new double[]{0, 0.4, 0.8, 1.2, 1.6} : new double[]{0.1, 1, 10};
            a.grid(yt);
            String[] cols; double[] norm; String[] names;
            if (p == 0) { cols = new String[]{"band_n", "band_M1", "band_M2", "band_a"}; norm = new double[]{1, M1b, M2b, ab}; names = new String[]{"neutrophils n (normalised)", "M1 macrophages (fold)", "M2 macrophages (fold)", "chemokine a (fold)"}; }
            else if (p == 1) { cols = new String[]{"band_g", "band_f", "band_e", "band_kap"}; norm = new double[]{gb, 1, 1, 1}; names = new String[]{"TGF-\u03b2 g (fold)", "fibroblasts f (fold)", "provisional matrix e", "collagen \u03ba (fold)"}; }
            else if (p == 2) { cols = new String[]{"band_v", "band_b", "band_w", "band_L"}; norm = new double[]{vb, 1, wb, 1}; names = new String[]{"VEGF-A v (fold)", "microvessels b (fold)", "VEGF-C w (fold)", "lymphatics L (fold)"}; }
            else { cols = new String[]{"band_Eeff", "Eeff_far"}; norm = new double[]{1, 1}; names = new String[]{"E_{eff} in scar band", "E_{eff} > 40 mm from scar"}; }
            for (int q = 0; q < cols.length; q++) {
                double[][] d = postWindow(t, cols[q], 60);
                a.line(d[0], div(d[1], norm[q]), PAL[q == 0 ? 0 : q == 1 ? 4 : q == 2 ? 5 : 3], 4.5f, null);
            }
            if (p == 3) {
                double[][] d = postWindow(t, "band_pi", 60);
                double[] sc = d[1].clone(); for (int i = 0; i < sc.length; i++) sc[i] = sc[i] * 10;
                a.line(d[0], sc, PAL[1], 4.5f, new float[]{14, 9});
                names = new String[]{"E_{eff} in scar band", "E_{eff} > 40 mm from scar", "escape probability \u03c0 \u00d7 10 (band)"};
            }
            a.frame(); a.xticks(new double[]{0, 10, 20, 30, 40, 50, 60}, "%.0f"); a.yticks(yt, p == 3 ? "%.1f" : "%.1f");
            a.xlabel("days after excision"); a.ylabel(p == 3 ? "relative level" : "level relative to homeostasis");
            a.title(ttl[p]);
            Color[] lc = p == 3 ? new Color[]{PAL[0], PAL[4], PAL[1]} : new Color[]{PAL[0], PAL[4], PAL[5], PAL[3]};
            float[][] ld = p == 3 ? new float[][]{null, null, {14, 9}} : null;
            if (p == 3) a.legend(names, lc, ld, a.X + a.Wd - 560, a.Y + a.Ht - 150, 26); else a.legend(names, lc, ld, a.X + a.Wd - 560, a.Y + 50, 26);
            f.panelLabel(lab[p], pos[p][0] - 200, pos[p][1] - 20);
        }
        f.text("shaded: reported windows for neutrophil (days 1-2) and macrophage (days 3-7) peaks, fibroblast proliferation (days 5-14), lymphatic regeneration (weeks 2-8)", 1200, 1735, 26, false, new Color(80, 80, 80), 0);
        f.save("Figure_2_Wound_Healing_Dynamics.png");
    }

    // ================================================================== Figure 3: spatial maps (baseline)
    static void fig3() throws IOException {
        String sc = "baseline";
        double A = sv(sc, "A_mm"), B = sv(sc, "B_mm"), Bu = sv(sc, "Bu_mm");
        Snap pre = snap(sc, "pre"), d3 = snap(sc, "d3"), d7 = snap(sc, "d7"), d21 = snap(sc, "d21"), d730 = snap(sc, "d730");
        Fig f = new Fig(2400, 1330);
        double W = 470, Hh = 359;
        double[][] pos = {{140, 110}, {940, 110}, {1740, 110}, {140, 760}, {940, 760}, {1740, 760}};
        String[] ttl = {"Dormant cells c_d before excision", "In-transit cells c_t and lymph paths", "Effector activity E_{eff}, day 3",
                "Emboli speed |V_t|, day 7", "Lymphatic density L, day 21", "Origin of escaping lineages, 2 y"};
        Snap[] sn = {pre, pre, d3, d7, d21, d730};
        String[] fld = {"cd", "ct", "Eeff", "Vabs", "L", "escMap"};
        int[][][] cms = {MAGMA, MAGMA, VIRIDIS, VIRIDIS, VIRIDIS, MAGMA};
        double[][] rng = {{1e-3, 1}, {1e-3, 1}, {0.3, 1.7}, {0, 8}, {0, 1.6}, {1e-3, 1}};
        boolean[] lg = {true, true, false, false, false, true};
        boolean[] rel = {true, true, false, false, false, true};
        String[] cbl = {"relative density", "relative density", "relative to homeostasis", "mm day^{-1}", "relative to homeostasis", "relative density"};
        double[][] tks = {{1e-3, 1e-2, 1e-1, 1}, {1e-3, 1e-2, 1e-1, 1}, {0.3, 1.0, 1.7}, {0, 4, 8}, {0, 0.8, 1.6}, {1e-3, 1e-2, 1e-1, 1}};
        for (int p = 0; p < 6; p++) {
            Axes a = new Axes(f, pos[p][0], pos[p][1], W, Hh);
            a.lim(-30, 80, -40, 44);
            float[] data = sn[p].f.get(fld[p]);
            if (rel[p]) { double mx = max(data); float[] d2 = new float[data.length]; for (int k = 0; k < data.length; k++) d2[k] = (float) (data[k] / mx); data = d2; }
            heat(a, data, sn[p].nx, sn[p].ny, cms[p], rng[p][0], rng[p][1], lg[p]);
            if (p == 1) streamlines(a, pre, new Color(255, 255, 255, 170));
            if (p < 2) { ellipse(a, A, B, 0, Color.WHITE, 3.5f, new float[]{12, 8}); ellipse(a, A, Bu, 0, new Color(255, 200, 120), 3f, new float[]{4, 6}); }
            else scarLine(a, A, 0, p == 2 ? Color.BLACK : Color.WHITE, 3f);
            a.frame(); a.fs = 25f;
            a.xticks(new double[]{-20, 0, 20, 40, 60, 80}, "%.0f"); a.yticks(new double[]{-40, -20, 0, 20, 40}, "%.0f");
            a.xlabel("x (mm), toward node basin"); a.ylabel("y (mm)");
            f.text(ttl[p], a.X + a.Wd / 2, a.Y - 20, 28, true, Color.BLACK, 0);
            colorbar(f, a.X + a.Wd + 18, a.Y, 24, a.Ht, cms[p], rng[p][0], rng[p][1], lg[p], tks[p], lg[p] ? "%.3g" : "%.1f", cbl[p]);
            f.panelLabel("ABCDEF".substring(p, p + 1), a.X - 125, a.Y - 18);
        }
        f.text("dashed white: excision ellipse (m = 10 mm, \u03b8 = 0\u00b0); dotted orange: undermined zone; solid line: closed scar", 1200, 1310, 25, false, new Color(70, 70, 70), 0);
        f.save("Figure_3_Spatial_Dynamics_Baseline.png");
    }
    static double max(float[] a) { double m = 0; for (float v : a) m = Math.max(m, v); return m; }

    // ================================================================== Figure 4: mechanism decomposition
    static void fig4() throws IOException {
        Fig f = new Fig(2400, 1100);
        Axes a = new Axes(f, 210, 110, 960, 760).lim(0, 730, 0, 0.12);
        double[] yt = {0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12};
        a.grid(yt);
        String[] codes = {"111", "011", "101", "110", "100", "010", "001", "000"};
        String[] lbl = {"all mechanisms (baseline)", "no immune loss", "no wound response", "no lymphatic disruption", "immune loss only", "wound only", "lymphatic only", "removal only"};
        float[][] dashes = {null, null, null, null, {14, 9}, {14, 9}, {14, 9}, {5, 6}};
        Color[] cl = {PAL[0], PAL[5], PAL[4], PAL[3], PAL[5], PAL[4], PAL[3], PAL[7]};
        for (int i = 0; i < codes.length; i++) {
            String sc = codes[i].equals("111") ? "baseline" : "fact_I" + codes[i].charAt(0) + "W" + codes[i].charAt(1) + "R" + codes[i].charAt(2);
            double[] cp = cumP(sc);
            a.line(seq(cp.length), cp, cl[i], i == 0 ? 6f : 4f, dashes[i]);
        }
        a.frame(); a.xticks(new double[]{0, 180, 365, 545, 730}, "%.0f"); a.yticks(yt, "pct");
        a.xlabel("days after excision"); a.ylabel("cumulative probability of visible recurrence");
        a.title("Factorial removal of mechanisms (m = 10 mm, \u03b8 = 0\u00b0)");
        a.legend(lbl, cl, dashes, a.X + 30, a.Y + 45, 25);
        f.panelLabel("A", 20, 80);
        // B: main effects as relative risk (geometric mean over the other factors), both orientations
        Axes b = new Axes(f, 1440, 110, 880, 760).lim(0, 3, 1, 3.0);
        double[] yt2 = {1, 1.5, 2, 2.5, 3};
        b.grid(yt2);
        String[] mech = {"immune loss", "wound response", "lymphatic disruption"};
        for (int o = 0; o < 2; o++) {
            String pre = o == 0 ? "fact_" : "fact90_";
            String base = o == 0 ? "baseline" : "margin_10.0_th90";
            for (int m = 0; m < 3; m++) {
                double sl = 0; int c = 0;
                for (int x1 = 0; x1 < 2; x1++) for (int x2 = 0; x2 < 2; x2++) {
                    int[] on = new int[3], off = new int[3];
                    int[] others = {x1, x2}; int q = 0;
                    for (int k = 0; k < 3; k++) { if (k == m) { on[k] = 1; off[k] = 0; } else { on[k] = others[q]; off[k] = others[q]; q++; } }
                    String son = name(pre, on, base), soff = name(pre, off, base);
                    sl += Math.log(P2(son) / P2(soff)); c++;
                }
                double rr = Math.exp(sl / c);
                double x = m + 0.18 + o * 0.34, w = 0.3;
                f.g.setColor(o == 0 ? PAL[5] : PAL[1]);
                f.g.fill(new Rectangle2D.Double(b.px(x), b.py(rr), b.px(x + w) - b.px(x), b.py(1) - b.py(rr)));
                f.text(String.format(Locale.ROOT, "%.2f", rr), b.px(x + w / 2), b.py(rr) - 10, 25, false, Color.BLACK, 0);
            }
        }
        b.frame(); b.yticks(yt2, "%.1f");
        for (int m = 0; m < 3; m++) f.text(mech[m], b.px(m + 0.5), b.Y + b.Ht + 45, 27, false, Color.BLACK, 0);
        b.ylabel("relative risk, mechanism on vs off");
        b.title("Main effects, geometric mean over other factors");
        b.legend(new String[]{"long axis parallel to drainage (\u03b8 = 0\u00b0)", "perpendicular (\u03b8 = 90\u00b0)"}, new Color[]{PAL[5], PAL[1]}, null, b.X + 30, b.Y + 50, 25);
        f.panelLabel("B", 1250, 80);
        f.save("Figure_4_Mechanism_Decomposition.png");
    }
    static String name(String pre, int[] s, String base) {
        if (s[0] == 1 && s[1] == 1 && s[2] == 1) return base;
        return pre + "I" + s[0] + "W" + s[1] + "R" + s[2];
    }

    // ================================================================== Figure 5: margin sweep
    static void fig5() throws IOException {
        double[] ms = {2, 5, 7.5, 10, 12.5, 15, 20};
        double[] p0 = new double[ms.length], p90 = new double[ms.length], pr = new double[ms.length], l0 = new double[ms.length], t0 = new double[ms.length], l90 = new double[ms.length], t90 = new double[ms.length];
        double[] ex0 = new double[ms.length], ex90 = new double[ms.length], pen = new double[ms.length];
        for (int i = 0; i < ms.length; i++) {
            String s0 = ms[i] == 10 ? "baseline" : "margin_" + ms[i] + "_th0", s90 = "margin_" + ms[i] + "_th90", sr = "removal_" + ms[i];
            p0[i] = P2(s0); p90[i] = P2(s90); pr[i] = P2(sr);
            l0[i] = Ploc(s0); t0[i] = Ptr(s0); l90[i] = Ploc(s90); t90[i] = Ptr(s90);
            ex0[i] = sv(s0, "excised_cd_frac"); ex90[i] = sv(s90, "excised_cd_frac");
            pen[i] = sv(s0, "Nvis_730") / sv(sr, "Nvis_730");
        }
        Fig f = new Fig(2400, 1050);
        Axes a = new Axes(f, 200, 110, 600, 700).lim(0, 21, 0, 0.30);
        double[] yt = {0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30};
        a.grid(yt);
        a.line(ms, p0, PAL[5], 5f, null); a.markers(ms, p0, PAL[5], 10);
        a.line(ms, p90, PAL[1], 5f, null); a.markers(ms, p90, PAL[1], 10);
        a.line(ms, pr, PAL[7], 4f, new float[]{14, 9}); a.markers(ms, pr, PAL[7], 8);
        a.frame(); a.xticks(new double[]{0, 5, 10, 15, 20}, "%.0f"); a.yticks(yt, "pct");
        a.xlabel("radial margin m (mm)"); a.ylabel("2-year probability of recurrence");
        a.title("Margin width");
        a.legend(new String[]{"\u03b8 = 0\u00b0 (along drainage)", "\u03b8 = 90\u00b0 (across drainage)", "\u03b8 = 0\u00b0, removal only"}, new Color[]{PAL[5], PAL[1], PAL[7]}, new float[][]{null, null, {14, 9}}, a.X + 150, a.Y + 45, 24);
        f.panelLabel("A", 20, 80);
        Axes b = new Axes(f, 1000, 110, 600, 700).lim(0, 21, 0, 0.20);
        double[] yt2 = {0, 0.05, 0.10, 0.15, 0.20};
        b.grid(yt2);
        b.line(ms, l0, PAL[5], 5f, null); b.markers(ms, l0, PAL[5], 9);
        b.line(ms, t0, PAL[5], 4f, new float[]{14, 9});
        b.line(ms, l90, PAL[1], 5f, null); b.markers(ms, l90, PAL[1], 9);
        b.line(ms, t90, PAL[1], 4f, new float[]{14, 9});
        b.frame(); b.xticks(new double[]{0, 5, 10, 15, 20}, "%.0f"); b.yticks(yt2, "pct");
        b.xlabel("radial margin m (mm)"); b.ylabel("2-year probability");
        b.title("Satellite (<= 2 cm) vs in-transit (> 2 cm)");
        b.legend(new String[]{"satellite, \u03b8 = 0\u00b0", "in-transit, \u03b8 = 0\u00b0", "satellite, \u03b8 = 90\u00b0", "in-transit, \u03b8 = 90\u00b0"}, new Color[]{PAL[5], PAL[5], PAL[1], PAL[1]}, new float[][]{null, {14, 9}, null, {14, 9}}, b.X + 200, b.Y + 45, 24);
        f.panelLabel("B", 820, 80);
        Axes c = new Axes(f, 1800, 110, 560, 700).lim(0, 21, 0, 1.0);
        double[] yt3 = {0, 0.2, 0.4, 0.6, 0.8, 1.0};
        c.grid(yt3);
        c.line(ms, ex0, PAL[5], 5f, null); c.markers(ms, ex0, PAL[5], 9);
        c.line(ms, ex90, PAL[1], 5f, null); c.markers(ms, ex90, PAL[1], 9);
        double[] penS = new double[ms.length]; for (int i = 0; i < ms.length; i++) penS[i] = (pen[i] - 1);
        c.line(ms, penS, PAL[4], 4f, new float[]{14, 9}); c.markers(ms, penS, PAL[4], 8);
        c.frame(); c.xticks(new double[]{0, 5, 10, 15, 20}, "%.0f"); c.yticks(yt3, "%.1f");
        c.xlabel("radial margin m (mm)"); c.ylabel("fraction");
        c.title("Removal and excess risk");
        c.legend(new String[]{"dormant cells excised, \u03b8 = 0\u00b0", "dormant cells excised, \u03b8 = 90\u00b0", "relative excess from wound + lymphatics (\u03b8 = 0\u00b0)"}, new Color[]{PAL[5], PAL[1], PAL[4]}, new float[][]{null, null, {14, 9}}, c.X + 20, c.Y + 40, 22);
        f.panelLabel("C", 1640, 80);
        f.save("Figure_5_Margin_Width.png");
    }

    // ================================================================== Figure 6: orientation
    static void fig6() throws IOException {
        double[] th = {0, 22.5, 45, 67.5, 90};
        double[] P = new double[th.length], Pl = new double[th.length];
        for (int i = 0; i < th.length; i++) {
            String s = th[i] == 0 ? "baseline" : th[i] == 90 ? "margin_10.0_th90" : "orient_" + th[i];
            P[i] = P2(s); Pl[i] = Ploc(s);
        }
        Fig f = new Fig(2400, 1500);
        Axes a = new Axes(f, 200, 120, 560, 480).lim(-5, 95, 0, 0.20);
        double[] yt = {0, 0.05, 0.10, 0.15, 0.20};
        a.grid(yt);
        a.line(th, P, PAL[0], 5f, null); a.markers(th, P, PAL[0], 10);
        a.line(th, Pl, PAL[4], 4f, new float[]{14, 9}); a.markers(th, Pl, PAL[4], 8);
        a.frame(); a.fs = 26f; a.xticks(new double[]{0, 22.5, 45, 67.5, 90}, "%.1f"); a.yticks(yt, "pct");
        a.xlabel("angle \u03b8 of long axis to drainage axis (\u00b0)"); a.ylabel("2-year probability");
        a.title("Excision orientation (m = 10 mm)");
        a.legend(new String[]{"all recurrences", "satellite (within 2 cm of scar)"}, new Color[]{PAL[0], PAL[4]}, new float[][]{null, {14, 9}}, a.X + 25, a.Y + 45, 24);
        f.panelLabel("A", 20, 90);
        // B: polar distribution of escape origins
        double cx = 1210, cy = 390, R = 245;
        f.text("Direction of escape origins", cx, 92, 30, true, Color.BLACK, 0);
        String[] scs = {"baseline", "margin_10.0_th90"}; Color[] cc = {new Color(0, 114, 178, 150), new Color(230, 159, 0, 150)};
        double gmax = 0; double[][] dist = new double[2][36];
        for (int o = 0; o < 2; o++) {
            Map<String, double[]> an = csv(RES.resolve(scs[o]).resolve("angular.csv"));
            double tot = 0;
            for (int q = 0; q < 36; q++) { dist[o][q] = an.get("d0_5")[q] + an.get("d5_10")[q] + an.get("d10_20")[q] + an.get("d20_40")[q]; tot += dist[o][q]; }
            for (int q = 0; q < 36; q++) { dist[o][q] /= tot; gmax = Math.max(gmax, dist[o][q]); }
        }
        f.g.setStroke(new BasicStroke(1.5f)); f.g.setColor(new Color(200, 200, 200));
        for (int r = 1; r <= 4; r++) f.g.draw(new Ellipse2D.Double(cx - R * r / 4.0, cy - R * r / 4.0, R * r / 2.0, R * r / 2.0));
        for (int q = 0; q < 8; q++) f.g.draw(new Line2D.Double(cx, cy, cx + R * Math.cos(q * Math.PI / 4), cy - R * Math.sin(q * Math.PI / 4)));
        for (int o = 0; o < 2; o++) for (int q = 0; q < 36; q++) {
            double r = R * Math.sqrt(dist[o][q] / gmax);
            f.g.setColor(cc[o]);
            f.g.fill(new Arc2D.Double(cx - r, cy - r, 2 * r, 2 * r, q * 10, 10, Arc2D.PIE));
        }
        f.text("0\u00b0", cx + R + 10, cy + 9, 24, false, Color.BLACK, -1);
        f.text("(node basin)", cx + R + 10, cy + 40, 22, false, Color.BLACK, -1);
        f.text("180\u00b0", cx - R - 10, cy + 9, 24, false, Color.BLACK, 1);
        f.text("90\u00b0", cx, cy - R - 10, 24, false, Color.BLACK, 0);
        f.text("270\u00b0", cx, cy + R + 32, 24, false, Color.BLACK, 0);
        f.g.setColor(cc[0]); f.g.fillRect((int) (cx - 230), 690, 40, 26); f.text("\u03b8 = 0\u00b0", cx - 180, 713, 24, false, Color.BLACK, -1);
        f.g.setColor(cc[1]); f.g.fillRect((int) (cx + 50), 690, 40, 26); f.text("\u03b8 = 90\u00b0", cx + 100, 713, 24, false, Color.BLACK, -1);
        f.panelLabel("B", 880, 90);
        // C, D: emboli speed maps, day 7; F: escape origins for theta = 90
        String[] snaps = {"baseline", "margin_10.0_th90"}; double[] ang = {0, 90};
        double[][] mpos = {{1660, 120}, {200, 880}};
        for (int o = 0; o < 2; o++) {
            Snap s = snap(snaps[o], "d7");
            Axes m = new Axes(f, mpos[o][0], mpos[o][1], 480, 480).lim(-50, 70, -60, 60);
            heat(m, s.f.get("Vabs"), s.nx, s.ny, VIRIDIS, 0, 8, false);
            streamlines(m, s, new Color(255, 255, 255, 150));
            scarLine(m, sv(snaps[o], "A_mm"), ang[o], new Color(255, 80, 80), 5f);
            m.frame(); m.fs = 24f; m.xticks(new double[]{-40, -20, 0, 20, 40, 60}, "%.0f"); m.yticks(new double[]{-60, -30, 0, 30, 60}, "%.0f");
            m.xlabel("x (mm)"); m.ylabel("y (mm)");
            f.text(o == 0 ? "Emboli speed, day 7, \u03b8 = 0\u00b0" : "Emboli speed, day 7, \u03b8 = 90\u00b0", m.X + m.Wd / 2, m.Y - 20, 27, true, Color.BLACK, 0);
            f.panelLabel(o == 0 ? "C" : "D", m.X - 130, m.Y - 20);
            colorbar(f, m.X + m.Wd + 16, m.Y, 22, m.Ht, VIRIDIS, 0, 8, false, new double[]{0, 4, 8}, "%.0f", "|V_t| (mm day^{-1})");
        }
        Snap s90 = snap("margin_10.0_th90", "d730");
        Axes fm = new Axes(f, 1660, 880, 480, 480).lim(-50, 70, -60, 60);
        float[] es = s90.f.get("escMap"); double mx = max(es); float[] esn = new float[es.length]; for (int k = 0; k < es.length; k++) esn[k] = (float) (es[k] / mx);
        heat(fm, esn, s90.nx, s90.ny, MAGMA, 1e-3, 1, true);
        scarLine(fm, sv("margin_10.0_th90", "A_mm"), 90, Color.WHITE, 4f);
        fm.frame(); fm.fs = 24f; fm.xticks(new double[]{-40, -20, 0, 20, 40, 60}, "%.0f"); fm.yticks(new double[]{-60, -30, 0, 30, 60}, "%.0f");
        fm.xlabel("x (mm)"); fm.ylabel("y (mm)");
        f.text("Escape origins, 2 y, \u03b8 = 90\u00b0", fm.X + fm.Wd / 2, fm.Y - 20, 27, true, Color.BLACK, 0);
        f.panelLabel("F", fm.X - 130, fm.Y - 20);
        colorbar(f, fm.X + fm.Wd + 16, fm.Y, 22, fm.Ht, MAGMA, 1e-3, 1, true, new double[]{1e-3, 1e-2, 1e-1, 1}, "%.3g", "relative density");
        // E: clearance of residual in-transit cells
        Axes e = new Axes(f, 1000, 880, 460, 480).lim(0, 30, 0, 1.0);
        double[] yt3 = {0, 0.25, 0.5, 0.75, 1.0}; e.grid(yt3);
        for (int o = 0; o < 2; o++) {
            Map<String, double[]> t = ts(snaps[o]);
            double[][] d = postWindow(t, "ct_tot", 30);
            e.line(d[0], div(d[1], d[1][0]), o == 0 ? PAL[5] : PAL[1], 5f, null);
        }
        e.frame(); e.fs = 24f; e.xticks(new double[]{0, 10, 20, 30}, "%.0f"); e.yticks(yt3, "%.2f");
        e.xlabel("days after excision"); e.ylabel("in-transit cells remaining");
        e.title("Residual in-transit cells");
        double r0 = sv("baseline", "lodged_post_wound_zone"), r90 = sv("margin_10.0_th90", "lodged_post_wound_zone");
        e.legend(new String[]{"\u03b8 = 0\u00b0", String.format(Locale.ROOT, "\u03b8 = 90\u00b0 (%.1f\u00d7 lodging near scar)", r90 / r0)}, new Color[]{PAL[5], PAL[1]}, null, e.X + 20, e.Y + 50, 22);
        f.panelLabel("E", 880, 860);
        f.save("Figure_6_Excision_Orientation.png");
    }
    // ================================================================== Figure 7: SLNB timing
    static void fig7() throws IOException {
        String[] sc = {"baseline", "slnb_prior", "slnb_simult", "slnb_delayed"};
        String[] lb = {"no SLNB", "SLNB 4 weeks before excision", "SLNB at excision", "SLNB 6 weeks after excision"};
        Color[] cl = {PAL[0], PAL[3], PAL[4], PAL[5]};
        Fig f = new Fig(2400, 1000);
        Axes a = new Axes(f, 200, 110, 900, 680).lim(0, 730, 0, 0.12);
        double[] yt = {0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12};
        a.grid(yt);
        for (int i = 0; i < sc.length; i++) a.line(seq(731), cumP(sc[i]), cl[i], i == 0 ? 6f : 4.5f, i == 0 ? null : new float[]{16, 8});
        a.frame(); a.xticks(new double[]{0, 180, 365, 545, 730}, "%.0f"); a.yticks(yt, "pct");
        a.xlabel("days after excision"); a.ylabel("cumulative probability of visible recurrence");
        a.title("Sentinel lymph node biopsy timing");
        a.legend(lb, cl, new float[][]{null, {16, 8}, {16, 8}, {16, 8}}, a.X + 30, a.Y + 45, 25);
        f.panelLabel("A", 20, 80);
        Axes b = new Axes(f, 1400, 110, 900, 680).lim(0, 4, 0, 1.4);
        double[] yt2 = {0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4}; b.grid(yt2);
        double base = P2("baseline"), baseL = sv("baseline", "lodged_post");
        for (int i = 0; i < sc.length; i++) {
            double rr = P2(sc[i]) / base, lr = sv(sc[i], "lodged_post") / baseL;
            f.g.setColor(PAL[5]); f.g.fill(new Rectangle2D.Double(b.px(i + 0.15), b.py(rr), b.px(i + 0.48) - b.px(i + 0.15), b.py(0) - b.py(rr)));
            f.g.setColor(PAL[1]); f.g.fill(new Rectangle2D.Double(b.px(i + 0.52), b.py(lr), b.px(i + 0.85) - b.px(i + 0.52), b.py(0) - b.py(lr)));
            f.text(String.format(Locale.ROOT, "%.2f", rr), b.px(i + 0.315), b.py(rr) - 10, 23, false, Color.BLACK, 0);
            f.text(String.format(Locale.ROOT, "%.2f", lr), b.px(i + 0.685), b.py(lr) - 10, 23, false, Color.BLACK, 0);
            String[] two = lb[i].split(" (?=\\d|at|before|after)", 2);
            f.text(i == 0 ? "no SLNB" : i == 1 ? "4 wk before" : i == 2 ? "at excision" : "6 wk after", b.px(i + 0.5), b.Y + b.Ht + 42, 26, false, Color.BLACK, 0);
        }
        b.frame(); b.yticks(yt2, "%.1f"); b.ylabel("relative to no SLNB");
        b.title("2-year risk and post-operative lodging");
        b.legend(new String[]{"2-year recurrence probability", "in-transit cells lodged after excision"}, new Color[]{PAL[5], PAL[1]}, null, b.X + 30, b.Y + 45, 25);
        f.panelLabel("B", 1220, 80);
        f.save("Figure_7_SLNB_Timing.png");
    }

    // ================================================================== Figure 8: perioperative therapy and sensitivity
    static void fig8() throws IOException {
        Fig f = new Fig(2400, 1650);
        String[] sc = {"drug_nsaid_d0_7", "drug_nsaid_d7_14", "drug_beta_dm2_28", "drug_antiVEGFA_d0_28", "drug_antiVEGFR3_d3_24", "drug_nsaid_beta"};
        String[] lb = {"NSAID d0-7", "NSAID d7-14", "\u03b2-blocker d-2 to 28", "anti-VEGF-A d0-28", "anti-VEGFR-3 d3-24", "NSAID + \u03b2-blocker"};
        double base = P2("baseline");
        Axes a = new Axes(f, 330, 110, 760, 640).lim(0.90, 1.20, 0, sc.length);
        double[] xt = {0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20};
        f.g.setColor(new Color(225, 225, 225)); for (double x : xt) f.g.draw(new Line2D.Double(a.px(x), a.Y, a.px(x), a.Y + a.Ht));
        for (int i = 0; i < sc.length; i++) {
            double rr = P2(sc[i]) / base;
            double y0 = a.py(sc.length - i - 0.2), y1 = a.py(sc.length - i - 0.8);
            f.g.setColor(rr < 1 ? PAL[3] : PAL[4]);
            f.g.fill(new Rectangle2D.Double(Math.min(a.px(1), a.px(rr)), y0, Math.abs(a.px(rr) - a.px(1)), y1 - y0));
            f.text(lb[i], a.X - 14, (y0 + y1) / 2 + 9, 25, false, Color.BLACK, 1);
            f.text(String.format(Locale.ROOT, "%.3f", rr), rr < 1 ? a.px(rr) - 8 : a.px(rr) + 8, (y0 + y1) / 2 + 9, 23, false, Color.BLACK, rr < 1 ? 1 : -1);
        }
        f.g.setColor(Color.BLACK); f.g.setStroke(new BasicStroke(2.5f)); f.g.draw(new Line2D.Double(a.px(1), a.Y, a.px(1), a.Y + a.Ht));
        a.frame(); a.xticks(xt, "%.2f"); a.xlabel("relative risk of 2-year recurrence vs. no drug");
        a.title("Perioperative regimens");
        f.panelLabel("A", 20, 80);
        // B: NSAID window heat map
        double[] st = {0, 3, 7, 14}, du = {3, 7, 14, 28};
        double[][] rr = new double[4][4]; double mn = 1, mx = 1;
        for (int i = 0; i < 4; i++) for (int j = 0; j < 4; j++) {
            rr[i][j] = P2("win_nsaid_s" + (int) st[i] + "_d" + (int) du[j]) / base; mn = Math.min(mn, rr[i][j]); mx = Math.max(mx, rr[i][j]);
        }
        double hx = 1520, hy = 150, cs = 150;
        f.text("NSAID window: relative risk", hx + 2 * cs, 100, 31, true, Color.BLACK, 0);
        double lo = Math.floor(mn * 100) / 100.0, hi = 1.0;
        for (int i = 0; i < 4; i++) for (int j = 0; j < 4; j++) {
            double t = (rr[i][j] - lo) / (hi - lo + 1e-9);
            f.g.setColor(cmap(VIRIDIS, t)); f.g.fill(new Rectangle2D.Double(hx + j * cs, hy + i * cs, cs - 4, cs - 4));
            f.text(String.format(Locale.ROOT, "%.3f", rr[i][j]), hx + j * cs + cs / 2, hy + i * cs + cs / 2 + 10, 27, true, t > 0.6 ? Color.BLACK : Color.WHITE, 0);
        }
        for (int j = 0; j < 4; j++) f.text(String.format(Locale.ROOT, "%.0f d", du[j]), hx + j * cs + cs / 2, hy + 4 * cs + 34, 26, false, Color.BLACK, 0);
        for (int i = 0; i < 4; i++) f.text(String.format(Locale.ROOT, "day %.0f", st[i]), hx - 14, hy + i * cs + cs / 2 + 10, 26, false, Color.BLACK, 1);
        f.text("duration", hx + 2 * cs, hy + 4 * cs + 80, 28, false, Color.BLACK, 0);
        f.vtext("start after excision", hx - 165, hy + 2 * cs, 28, Color.BLACK);
        colorbar(f, hx + 4 * cs + 20, hy, 26, 4 * cs - 4, VIRIDIS, lo, hi, false, new double[]{lo, (lo + hi) / 2, hi}, "%.3f", "relative risk");
        f.panelLabel("B", 1250, 80);
        // C: tornado sensitivity
        String[] ps = {"lam1", "lam0", "sG", "sM", "omV", "omNET", "etaPi", "delPi", "epsU", "epsQ", "Vref", "clG", "sAlpha", "kE", "sI"};
        String[] pl = {"\u03bb_1 stasis lodging", "\u03bb_0 basal lodging", "s_g TGF-\u03b2 suppression", "s_M M2 suppression", "\u03c9_v VEGF awakening", "\u03c9_N NET awakening", "\u03b7_\u03a0 priming gain", "\u03b4_\u03a0 priming decay",
                "\u03b5_u undermining cut", "\u03b5_q undermining injury", "V_{ref} emboli speed", "\u03ba_g TGF-\u03b2 lymph clearance", "s_\u03b1 clonal heterogeneity", "k_E CTL killing", "s_I systemic suppression"};
        double[][] ch = new double[ps.length][2]; Integer[] ord = new Integer[ps.length];
        for (int i = 0; i < ps.length; i++) {
            ch[i][0] = Math.log(P2("sens_" + ps[i] + "_lo") / base) / Math.log(2); ch[i][1] = Math.log(P2("sens_" + ps[i] + "_hi") / base) / Math.log(2); ord[i] = i;
        }
        Arrays.sort(ord, (x, y) -> Double.compare(Math.max(Math.abs(ch[y][0]), Math.abs(ch[y][1])), Math.max(Math.abs(ch[x][0]), Math.abs(ch[x][1]))));
        double span = 5;
        Axes c = new Axes(f, 600, 930, 1460, 620).lim(-span, span, 0, ps.length);
        f.g.setColor(new Color(225, 225, 225));
        for (double x = -span; x <= span + 1e-9; x += 1) f.g.draw(new Line2D.Double(c.px(x), c.Y, c.px(x), c.Y + c.Ht));
        for (int r = 0; r < ps.length; r++) {
            int i = ord[r];
            double y0 = c.py(ps.length - r - 0.12), y1 = c.py(ps.length - r - 0.88);
            for (int s2 = 0; s2 < 2; s2++) {
                double v = ch[i][s2]; f.g.setColor(s2 == 0 ? PAL[5] : PAL[1]);
                double ya = s2 == 0 ? y0 : (y0 + y1) / 2, yb = s2 == 0 ? (y0 + y1) / 2 : y1;
                f.g.fill(new Rectangle2D.Double(Math.min(c.px(0), c.px(v)), ya, Math.abs(c.px(v) - c.px(0)), yb - ya));
                double rrv = Math.pow(2, v);
                f.text(String.format(Locale.ROOT, "%.2f", rrv), v >= 0 ? c.px(v) + 8 : c.px(v) - 8, yb - 3, 19, false, new Color(60, 60, 60), v >= 0 ? -1 : 1);
            }
            f.text(pl[i], c.X - 14, (y0 + y1) / 2 + 9, 23, false, Color.BLACK, 1);
        }
        f.g.setColor(Color.BLACK); f.g.setStroke(new BasicStroke(2.5f)); f.g.draw(new Line2D.Double(c.px(0), c.Y, c.px(0), c.Y + c.Ht));
        c.frame(); c.fs = 25f;
        double[] tx = {-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5};
        for (double tv : tx) {
            f.g.setColor(Color.BLACK); f.g.draw(new Line2D.Double(c.px(tv), c.Y + c.Ht, c.px(tv), c.Y + c.Ht + 10));
            String lb2 = tv >= 0 ? String.format(Locale.ROOT, "%.0f", Math.pow(2, tv)) : "1/" + String.format(Locale.ROOT, "%.0f", Math.pow(2, -tv));
            f.text(lb2, c.px(tv), c.Y + c.Ht + 40, 24, false, Color.BLACK, 0);
        }
        c.xlabel("relative risk of 2-year recurrence vs baseline (log scale)");
        c.title("One-at-a-time sensitivity (parameter \u00d7 0.5 and \u00d7 1.5)");
        c.legend(new String[]{"parameter \u00d7 0.5", "parameter \u00d7 1.5"}, new Color[]{PAL[5], PAL[1]}, null, c.X + c.Wd - 330, c.Y + c.Ht - 70, 24);
        f.panelLabel("C", 20, 900);
        f.save("Figure_8_Therapy_and_Sensitivity.png");
    }

    // ================================================================== tables and numbers for the manuscript
    static void numbers() throws IOException {
        StringBuilder sb = new StringBuilder("scenario,P1y,P2y,P2y_satellite,P2y_intransit,local_frac,N2y_cal,excised_cd_frac,lodged_post,lodged_post_wound_zone,peak_band_VEGFA_fold,band_L50_day,N_pre_cal\n");
        List<String> names = new ArrayList<>();
        try (DirectoryStream<Path> ds = Files.newDirectoryStream(RES)) { for (Path p : ds) if (Files.exists(p.resolve("summary.csv"))) names.add(p.getFileName().toString()); }
        Collections.sort(names);
        for (String s : names) {
            Map<String, String> m = summary(s);
            double N = Double.parseDouble(m.get("Nvis_730")), Nl = Double.parseDouble(m.get("Nvis_local_730"));
            sb.append(String.format(Locale.ROOT, "%s,%.5f,%.5f,%.5f,%.5f,%.4f,%.5f,%.4f,%.4f,%.4f,%.3f,%s,%.5f%n", s, P1(s), P2(s), Ploc(s), Ptr(s), Nl / N, CAL * N,
                    Double.parseDouble(m.get("excised_cd_frac")), Double.parseDouble(m.get("lodged_post")), Double.parseDouble(m.get("lodged_post_wound_zone")),
                    Double.parseDouble(m.get("peak_band_VEGFA")) / Double.parseDouble(m.get("baseline_v")), m.get("band_L_recovery50_day"), CAL * Double.parseDouble(m.get("N_pre"))));
        }
        Files.writeString(RES.resolve("scenario_outcomes.csv"), sb.toString());
        System.out.println("wrote scenario_outcomes.csv (" + names.size() + " scenarios), calibration factor " + CAL);
    }

    public static void main(String[] args) throws Exception {
        RES = Paths.get(args.length > 0 ? args[0] : "results");
        OUT = Paths.get(args.length > 1 ? args[1] : "../lymphatic_figures");
        System.setProperty("java.awt.headless", "true");
        CAL = -Math.log(1 - TARGET_P) / sv("baseline", "Nvis_730");
        String which = args.length > 2 ? args[2] : "all";
        if (which.equals("all") || which.contains("n")) numbers();
        if (which.equals("all") || which.contains("1")) fig1();
        if (which.equals("all") || which.contains("2")) fig2();
        if (which.equals("all") || which.contains("3")) fig3();
        if (which.equals("all") || which.contains("4")) fig4();
        if (which.equals("all") || which.contains("5")) fig5();
        if (which.equals("all") || which.contains("6")) fig6();
        if (which.equals("all") || which.contains("7")) fig7();
        if (which.equals("all") || which.contains("8")) fig8();
    }
}
