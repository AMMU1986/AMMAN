import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.*;
import java.util.List;
import javax.imageio.ImageIO;

/**
 * Renders a high-resolution PNG microhardness profile across API X70 SMAW
 * weld joints (E6018, E7018, E9018) from hardness_profile_data.csv.
 * Uses only the JDK (Graphics2D + ImageIO) — no external libraries.
 */
public class HardnessPlot {

    // ---- plot geometry (high-res for print embedding) ----
    static final int W = 2000, H = 1200;
    static final int ML = 150, MR = 410, MT = 120, MB = 150;
    static final int PW = W - ML - MR, PH = H - MT - MB;
    static final double X_MIN = -8, X_MAX = 8, Y_MIN = 215, Y_MAX = 275;
    static final double FZ = 5, HAZ = 7, BM = 245;

    static double sx(double x) { return ML + (x - X_MIN) / (X_MAX - X_MIN) * PW; }
    static double sy(double y) { return MT + (Y_MAX - y) / (Y_MAX - Y_MIN) * PH; }

    public static void main(String[] args) throws Exception {
        // ---- read CSV ----
        List<double[]> rows = new ArrayList<>(); // x, e6018, e7018, e9018
        try (BufferedReader br = new BufferedReader(new FileReader("hardness_profile_data.csv"))) {
            String line = br.readLine(); // header
            while ((line = br.readLine()) != null) {
                if (line.isBlank()) continue;
                String[] p = line.split(",");
                rows.add(new double[]{
                    Double.parseDouble(p[0]), Double.parseDouble(p[1]),
                    Double.parseDouble(p[2]), Double.parseDouble(p[3])});
            }
        }

        BufferedImage img = new BufferedImage(W, H, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);
        g.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE);

        g.setColor(Color.WHITE);
        g.fillRect(0, 0, W, H);

        // ---- zone bands ----
        band(g, X_MIN, -HAZ, new Color(127,127,127), 46);
        band(g, -HAZ, -FZ, new Color(255,127,14), 46);
        band(g, -FZ, FZ, new Color(31,119,180), 46);
        band(g, FZ, HAZ, new Color(255,127,14), 46);
        band(g, HAZ, X_MAX, new Color(127,127,127), 46);

        // zone labels
        g.setColor(new Color(60,60,60));
        g.setFont(new Font("SansSerif", Font.BOLD, 26));
        center(g, "Fusion Zone (Weld)", sx(0), MT + 36);
        center(g, "HAZ", sx(-6), MT + 36);
        center(g, "HAZ", sx(6), MT + 36);
        center(g, "BM", sx(-7.5), MT + 36);
        center(g, "BM", sx(7.5), MT + 36);

        // centreline
        g.setColor(new Color(150,150,150));
        g.setStroke(dashed(2f, 8f, 8f));
        g.draw(new Line2D.Double(sx(0), MT, sx(0), MT + PH));

        // ---- grid + ticks ----
        g.setFont(new Font("SansSerif", Font.PLAIN, 22));
        for (int y = 215; y <= 275; y += 5) {
            double yp = sy(y);
            g.setColor(new Color(224,224,224));
            g.setStroke(new BasicStroke(1.2f));
            g.draw(new Line2D.Double(ML, yp, ML + PW, yp));
            g.setColor(new Color(40,40,40));
            right(g, Integer.toString(y), ML - 14, yp + 8);
        }
        for (int xt = -8; xt <= 8; xt++) {
            double xp = sx(xt);
            g.setColor(new Color(238,238,238));
            g.setStroke(new BasicStroke(1.2f));
            g.draw(new Line2D.Double(xp, MT, xp, MT + PH));
            g.setColor(new Color(40,40,40));
            center(g, Integer.toString(xt), xp, MT + PH + 36);
        }

        // base-metal reference line
        g.setColor(new Color(85,85,85));
        g.setStroke(dashed(2f, 9f, 7f));
        g.draw(new Line2D.Double(ML, sy(BM), ML + PW, sy(BM)));

        // axis box
        g.setColor(new Color(40,40,40));
        g.setStroke(new BasicStroke(2f));
        g.draw(new Rectangle2D.Double(ML, MT, PW, PH));

        // ---- data polylines ----
        Color[] colors = { new Color(214,39,40), new Color(31,119,180), new Color(44,160,44) };
        g.setStroke(new BasicStroke(3f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        for (int c = 0; c < 3; c++) {
            GeneralPath path = new GeneralPath();
            boolean first = true;
            for (double[] r : rows) {
                double px = sx(r[0]), py = sy(r[c + 1]);
                if (first) { path.moveTo(px, py); first = false; }
                else path.lineTo(px, py);
            }
            g.setColor(colors[c]);
            g.draw(path);
        }

        // ---- titles ----
        g.setColor(Color.BLACK);
        g.setFont(new Font("SansSerif", Font.BOLD, 34));
        center(g, "Microhardness Profile across API X70 SMAW Weld Joints", ML + PW / 2.0, 58);

        g.setFont(new Font("SansSerif", Font.BOLD, 26));
        center(g, "Distance from Weld Centreline (mm)", ML + PW / 2.0, H - 40);

        // y-axis title (rotated)
        AffineTransform old = g.getTransform();
        g.translate(46, MT + PH / 2.0);
        g.rotate(-Math.PI / 2);
        center(g, "Vickers Microhardness (HV0.1)", 0, 0);
        g.setTransform(old);

        // ---- legend ----
        int lx = ML + PW + 40, ly = MT + 40;
        g.setFont(new Font("SansSerif", Font.BOLD, 24));
        g.setColor(Color.BLACK);
        g.drawString("Electrode", lx, ly - 14);
        String[] names = {
            "E6018  (FZ 238 / HAZ 225)",
            "E7018  (FZ 252 / HAZ 232)",
            "E9018  (FZ 268 / HAZ 241)" };
        g.setFont(new Font("SansSerif", Font.PLAIN, 23));
        g.setStroke(new BasicStroke(5f));
        for (int i = 0; i < 3; i++) {
            int yy = ly + i * 46;
            g.setColor(colors[i]);
            g.draw(new Line2D.Double(lx, yy, lx + 44, yy));
            g.setColor(Color.BLACK);
            g.drawString(names[i], lx + 56, yy + 8);
        }
        int yy = ly + 3 * 46 + 10;
        g.setColor(new Color(85,85,85));
        g.setStroke(dashed(4f, 9f, 7f));
        g.draw(new Line2D.Double(lx, yy, lx + 44, yy));
        g.setColor(Color.BLACK);
        g.drawString("Base metal 245 HV", lx + 56, yy + 8);

        g.dispose();
        ImageIO.write(img, "png", new File("hardness_profile.png"));
        System.out.println("wrote hardness_profile.png (" + W + "x" + H + ")");
    }

    static void band(Graphics2D g, double x0, double x1, Color base, int alpha) {
        g.setColor(new Color(base.getRed(), base.getGreen(), base.getBlue(), alpha));
        double a = sx(x0), b = sx(x1);
        g.fill(new Rectangle2D.Double(a, MT, b - a, PH));
    }
    static BasicStroke dashed(float w, float on, float off) {
        return new BasicStroke(w, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER, 10f,
                new float[]{on, off}, 0f);
    }
    static void center(Graphics2D g, String s, double cx, double cy) {
        FontMetrics fm = g.getFontMetrics();
        g.drawString(s, (float)(cx - fm.stringWidth(s) / 2.0), (float) cy);
    }
    static void right(Graphics2D g, String s, double rx, double ry) {
        FontMetrics fm = g.getFontMetrics();
        g.drawString(s, (float)(rx - fm.stringWidth(s)), (float) ry);
    }
}
