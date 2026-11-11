/*
 * Fig. 8 of the SS430 filler-wire manuscript: (a) Charpy absorbed energy and
 * (b) Vickers microhardness of the FZ and HAZ for ER309L, ER410 and ER2594.
 *
 * The values are the single values reported in Table 3 of the manuscript.
 * No error bars are drawn, because replicate data were not available.
 * If the original test records change any value (for example, after the
 * Charpy unit is confirmed), edit the DATA block below and re-run:
 *
 *     java -Djava.awt.headless=true ss430_figures/GenerateFigure8.java
 *
 * Output: ss430_figures/Figure_8_Charpy_Hardness.png (2400 x 1050 px, 300 dpi)
 * Requires only a JDK (11+); no third-party libraries.
 */

import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.Locale;
import javax.imageio.*;
import javax.imageio.metadata.*;
import javax.imageio.stream.ImageOutputStream;

public class GenerateFigure8 {

    // ---------------- DATA (Table 3) ----------------
    static final String[] FILLERS = {"ER309L", "ER410", "ER2594"};
    static final double[] FZ_KV  = {428, 128, 304};
    static final double[] HAZ_KV = {452, 488, 584};
    static final String KV_UNIT = "J";
    static final double[] FZ_HV  = {268.0, 313.8, 176.8};
    static final double[] HAZ_HV = {148.4, 147.1, 141.1};
    static final double BM_HV = 156.0;
    // -------------------------------------------------

    static final int W = 2400, H = 1050, DPI = 300;
    static final Color FZ_COLOR = new Color(31, 78, 121);
    static final Color HAZ_COLOR = new Color(166, 196, 228);
    static final Color AXIS = Color.BLACK;
    static final String FONT = "Noto Sans";

    public static void main(String[] args) throws Exception {
        BufferedImage img = new BufferedImage(W, H, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_FRACTIONALMETRICS, RenderingHints.VALUE_FRACTIONALMETRICS_ON);
        g.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE);
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, W, H);

        int panelW = W / 2;
        drawPanel(g, 0, 0, panelW, H, "(a)", "Charpy absorbed energy (" + KV_UNIT + ")",
                  700, 100, FZ_KV, HAZ_KV, "%.0f", Double.NaN, null);
        drawPanel(g, panelW, 0, panelW, H, "(b)", "Microhardness (HV0.5)",
                  350, 50, FZ_HV, HAZ_HV, "%.1f", BM_HV,
                  String.format(Locale.ROOT, "BM %.1f HV0.5", BM_HV));
        g.dispose();

        // Run from the repository root (or from inside ss430_figures/).
        File dir = new File("ss430_figures").isDirectory() ? new File("ss430_figures") : new File(".");
        File out = new File(dir, "Figure_8_Charpy_Hardness.png");
        writePng(img, out);
        System.out.println("Wrote " + out.getPath() + " (" + W + " x " + H + " px, " + DPI + " dpi)");
    }

    static void drawPanel(Graphics2D g, int x0, int y0, int w, int h, String label, String yLabel,
                          double yMax, double yStep, double[] fz, double[] haz, String fmt,
                          double refValue, String refLabel) {
        int left = x0 + 210, right = x0 + w - 50, top = y0 + 150, bottom = y0 + h - 130;
        int plotH = bottom - top, plotW = right - left;

        Font tick = new Font(FONT, Font.PLAIN, 34);
        Font axisFont = new Font(FONT, Font.PLAIN, 38);
        Font valueFont = new Font(FONT, Font.PLAIN, 28);
        Font panelFont = new Font(FONT, Font.BOLD, 42);

        // Panel label
        g.setColor(AXIS);
        g.setFont(panelFont);
        g.drawString(label, x0 + 30, y0 + 70);

        // Y axis: ticks and labels
        g.setStroke(new BasicStroke(3f));
        g.setFont(tick);
        FontMetrics tfm = g.getFontMetrics();
        for (double v = 0; v <= yMax + 1e-9; v += yStep) {
            int y = (int) Math.round(bottom - v / yMax * plotH);
            g.draw(new Line2D.Double(left - 14, y, left, y));
            String s = String.format(Locale.ROOT, "%.0f", v);
            g.drawString(s, left - 22 - tfm.stringWidth(s), y + tfm.getAscent() / 2 - 4);
        }
        g.draw(new Line2D.Double(left, top, left, bottom));
        g.draw(new Line2D.Double(left, bottom, right, bottom));

        // Y-axis title (rotated)
        g.setFont(axisFont);
        FontMetrics afm = g.getFontMetrics();
        AffineTransform saved = g.getTransform();
        g.translate(x0 + 62, top + plotH / 2.0 + afm.stringWidth(yLabel) / 2.0);
        g.rotate(-Math.PI / 2);
        g.drawString(yLabel, 0, 0);
        g.setTransform(saved);

        // Reference line (BM hardness), drawn behind the bars; labelled in the legend
        if (!Double.isNaN(refValue)) {
            double y = bottom - refValue / yMax * plotH;
            g.setColor(REF_COLOR);
            g.setStroke(DASH);
            g.draw(new Line2D.Double(left, y, right, y));
            g.setStroke(new BasicStroke(3f));
        }

        // Bars
        int n = FILLERS.length;
        double groupW = plotW / (double) n;
        double barW = groupW * 0.30, gap = 10;
        g.setFont(valueFont);
        FontMetrics vfm = g.getFontMetrics();
        for (int i = 0; i < n; i++) {
            double cx = left + groupW * (i + 0.5);
            drawBar(g, cx - gap / 2 - barW, barW, bottom, plotH, yMax, fz[i], FZ_COLOR, fmt, vfm);
            drawBar(g, cx + gap / 2, barW, bottom, plotH, yMax, haz[i], HAZ_COLOR, fmt, vfm);
            g.setFont(tick);
            FontMetrics fm = g.getFontMetrics();
            g.setColor(AXIS);
            g.drawString(FILLERS[i], (float) (cx - fm.stringWidth(FILLERS[i]) / 2.0), bottom + 56);
            g.setFont(valueFont);
        }

        // Legend (above the plot area)
        g.setFont(tick);
        FontMetrics lfm = g.getFontMetrics();
        int lx = left + 30, ly = top - 70, box = 30;
        legendItem(g, lx, ly, box, FZ_COLOR, "FZ", lfm);
        legendItem(g, lx + 150, ly, box, HAZ_COLOR, "HAZ", lfm);
        if (refLabel != null) {
            int sx = lx + 330, sy = ly + box / 2;
            g.setColor(REF_COLOR);
            g.setStroke(DASH);
            g.draw(new Line2D.Double(sx, sy, sx + 70, sy));
            g.setStroke(new BasicStroke(3f));
            g.setColor(AXIS);
            g.drawString(refLabel, sx + 84, sy + lfm.getAscent() / 2 - 4);
        }
    }

    static final Color REF_COLOR = new Color(192, 0, 0);
    static final BasicStroke DASH = new BasicStroke(3f, BasicStroke.CAP_BUTT,
            BasicStroke.JOIN_MITER, 10f, new float[]{18f, 12f}, 0f);

    static void drawBar(Graphics2D g, double x, double bw, int bottom, int plotH, double yMax,
                        double v, Color c, String fmt, FontMetrics vfm) {
        double bh = v / yMax * plotH;
        Rectangle2D r = new Rectangle2D.Double(x, bottom - bh, bw, bh);
        g.setColor(c);
        g.fill(r);
        g.setColor(AXIS);
        g.setStroke(new BasicStroke(2f));
        g.draw(r);
        // Value label inside the top of the bar: white on dark bars, black on light bars
        String s = String.format(Locale.ROOT, fmt, v);
        double lum = 0.299 * c.getRed() + 0.587 * c.getGreen() + 0.114 * c.getBlue();
        g.setColor(lum < 128 ? Color.WHITE : AXIS);
        g.drawString(s, (float) (x + bw / 2 - vfm.stringWidth(s) / 2.0),
                     (float) (bottom - bh + vfm.getAscent() + 10));
        g.setColor(AXIS);
    }

    static void legendItem(Graphics2D g, int x, int y, int box, Color c, String text, FontMetrics fm) {
        Rectangle2D r = new Rectangle2D.Double(x, y, box, box);
        g.setColor(c);
        g.fill(r);
        g.setColor(AXIS);
        g.setStroke(new BasicStroke(2f));
        g.draw(r);
        g.drawString(text, x + box + 14, y + box / 2 + fm.getAscent() / 2 - 4);
    }

    static void writePng(BufferedImage img, File out) throws Exception {
        ImageWriter writer = ImageIO.getImageWritersByFormatName("png").next();
        ImageWriteParam param = writer.getDefaultWriteParam();
        IIOMetadata meta = writer.getDefaultImageMetadata(
                ImageTypeSpecifier.createFromRenderedImage(img), param);
        IIOMetadataNode root = new IIOMetadataNode("javax_imageio_png_1.0");
        IIOMetadataNode phys = new IIOMetadataNode("pHYs");
        String ppm = Integer.toString((int) Math.round(DPI / 0.0254));
        phys.setAttribute("pixelsPerUnitXAxis", ppm);
        phys.setAttribute("pixelsPerUnitYAxis", ppm);
        phys.setAttribute("unitSpecifier", "meter");
        root.appendChild(phys);
        meta.mergeTree("javax_imageio_png_1.0", root);
        try (ImageOutputStream ios = ImageIO.createImageOutputStream(out)) {
            writer.setOutput(ios);
            writer.write(null, new IIOImage(img, null, meta), param);
        }
        writer.dispose();
    }
}
