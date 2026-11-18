/*
 * Generates the four figures for the chapter
 * "The Price of Delay: Health, Labour and Macroeconomic Costs of Climate Inaction".
 *
 * Uses only the JDK (Java2D + ImageIO), because matplotlib/PIL are not available
 * in this sandbox. Each figure is drawn in point units and rendered at 300 dpi;
 * the PNG pHYs chunk is set to 300 dpi so Word and publishers read the correct size.
 *
 * All numbers come from the sources cited in the captions of
 * Chapter_Climate_Inaction_Economics.md.
 *
 * Usage (single-file source launch, JDK 11+):
 *     java ClimateInactionFigures.java
 */

import javax.imageio.*;
import javax.imageio.metadata.*;
import javax.imageio.stream.ImageOutputStream;
import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.io.File;
import org.w3c.dom.Node;

public class ClimateInactionFigures {

    static final String OUT_DIR = "/projects/sandbox/AMMAN/climate_inaction_figures";
    static final double DPI = 300.0;
    static final double S = DPI / 72.0;           // points -> pixels
    static final String FONT = "Noto Sans";

    static final Color HAZ = new Color(0xC0392B);
    static final Color HEALTH = new Color(0xE67E22);
    static final Color ECON = new Color(0x2471A3);
    static final Color MACRO = new Color(0x1E8449);
    static final Color GREY = new Color(0x566573);
    static final Color LIGHT_GRID = new Color(0xD5D8DC);

    // ------------------------------------------------------------------ helpers

    static Graphics2D g;

    static BufferedImage canvas(double wPt, double hPt) {
        BufferedImage img = new BufferedImage((int) Math.round(wPt * S), (int) Math.round(hPt * S),
                BufferedImage.TYPE_INT_RGB);
        g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_FRACTIONALMETRICS, RenderingHints.VALUE_FRACTIONALMETRICS_ON);
        g.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE);
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, img.getWidth(), img.getHeight());
        g.scale(S, S);
        return img;
    }

    static Color tint(Color c, double a) {
        int r = (int) (255 - (255 - c.getRed()) * a);
        int gg = (int) (255 - (255 - c.getGreen()) * a);
        int b = (int) (255 - (255 - c.getBlue()) * a);
        return new Color(r, gg, b);
    }

    /** Draw (multi-line) text. align: -1 left, 0 centre, 1 right. y is the vertical centre. */
    static void text(String s, double x, double y, float size, int style, Color c, int align) {
        g.setFont(new Font(FONT, style, 1).deriveFont(size));
        g.setColor(c);
        FontMetrics fm = g.getFontMetrics();
        String[] lines = s.split("\n");
        double lh = size * 1.22;
        double top = y - lh * lines.length / 2.0;
        for (int i = 0; i < lines.length; i++) {
            double w = fm.getStringBounds(lines[i], g).getWidth();
            double xx = align == 0 ? x - w / 2 : (align > 0 ? x - w : x);
            double baseline = top + lh * i + lh / 2 + fm.getAscent() / 2.0 - fm.getDescent() / 2.0;
            g.drawString(lines[i], (float) xx, (float) baseline);
        }
    }

    static void rotatedText(String s, double x, double y, float size, Color c) {
        AffineTransform old = g.getTransform();
        g.translate(x, y);
        g.rotate(-Math.PI / 2);
        text(s, 0, 0, size, Font.PLAIN, c, 0);
        g.setTransform(old);
    }

    static void box(double x, double y, double w, double h, Color c, String s, float size) {
        RoundRectangle2D r = new RoundRectangle2D.Double(x, y, w, h, 7, 7);
        g.setColor(tint(c, 0.16));
        g.fill(r);
        g.setColor(c);
        g.setStroke(new BasicStroke(1.0f));
        g.draw(r);
        text(s, x + w / 2, y + h / 2, size, Font.PLAIN, Color.BLACK, 0);
    }

    static void arrowHead(double x1, double y1, double x2, double y2, Color c) {
        double ang = Math.atan2(y2 - y1, x2 - x1);
        double len = 6, wid = 3;
        Path2D p = new Path2D.Double();
        p.moveTo(x2, y2);
        p.lineTo(x2 - len * Math.cos(ang) + wid * Math.sin(ang), y2 - len * Math.sin(ang) - wid * Math.cos(ang));
        p.lineTo(x2 - len * Math.cos(ang) - wid * Math.sin(ang), y2 - len * Math.sin(ang) + wid * Math.cos(ang));
        p.closePath();
        g.setColor(c);
        g.fill(p);
    }

    static void arrow(double x1, double y1, double x2, double y2, Color c) {
        g.setColor(c);
        g.setStroke(new BasicStroke(1.1f));
        double ang = Math.atan2(y2 - y1, x2 - x1);
        g.draw(new Line2D.Double(x1, y1, x2 - 5 * Math.cos(ang), y2 - 5 * Math.sin(ang)));
        arrowHead(x1, y1, x2, y2, c);
    }

    /** Vertical-bar panel. Bars may be stacked by passing extra[] (drawn hatched on top). */
    static void barPanel(double x0, double y0, double w, double h, String title, String ylabel,
                         String[] labels, double[] vals, double[] extra, Color[] colors,
                         double ymax, double step, String[] valueLabels, String tickFmt) {
        double left = x0 + 42, right = x0 + w - 6, top = y0 + 34, bottom = y0 + h - 34;
        text(title, x0 + 4, y0 + 13, 9.5f, Font.BOLD, Color.BLACK, -1);
        g.setStroke(new BasicStroke(0.5f));
        for (double t = 0; t <= ymax + 1e-9; t += step) {
            double yy = bottom - (bottom - top) * t / ymax;
            g.setColor(LIGHT_GRID);
            g.draw(new Line2D.Double(left, yy, right, yy));
            text(String.format(tickFmt, t), left - 4, yy, 7.5f, Font.PLAIN, GREY, 1);
        }
        g.setColor(Color.BLACK);
        g.setStroke(new BasicStroke(0.8f));
        g.draw(new Line2D.Double(left, top, left, bottom));
        g.draw(new Line2D.Double(left, bottom, right, bottom));
        rotatedText(ylabel, x0 + 8, (top + bottom) / 2, 7.8f, Color.BLACK);

        int n = vals.length;
        double slot = (right - left) / n, bw = slot * 0.55;
        for (int i = 0; i < n; i++) {
            double cx = left + slot * (i + 0.5);
            double bh = (bottom - top) * vals[i] / ymax;
            Rectangle2D r = new Rectangle2D.Double(cx - bw / 2, bottom - bh, bw, bh);
            g.setColor(colors[i]);
            g.fill(r);
            g.setColor(Color.BLACK);
            g.setStroke(new BasicStroke(0.6f));
            g.draw(r);
            double topY = bottom - bh;
            if (extra != null && extra[i] > 0) {
                double eh = (bottom - top) * extra[i] / ymax;
                Rectangle2D e = new Rectangle2D.Double(cx - bw / 2, topY - eh, bw, eh);
                g.setColor(tint(colors[i], 0.4));
                g.fill(e);
                Shape oldClip = g.getClip();
                g.clip(e);
                g.setColor(colors[i]);
                g.setStroke(new BasicStroke(0.6f));
                for (double d = -eh; d < bw + eh; d += 4) {
                    g.draw(new Line2D.Double(cx - bw / 2 + d, topY, cx - bw / 2 + d + eh, topY - eh));
                }
                g.setClip(oldClip);
                g.setColor(Color.BLACK);
                g.draw(e);
                topY -= eh;
            }
            text(valueLabels[i], cx, topY - 8, 8.5f, Font.BOLD, Color.BLACK, 0);
            text(labels[i], cx, bottom + 15, 7.8f, Font.PLAIN, Color.BLACK, 0);
        }
    }

    static void save(BufferedImage img, String name) throws Exception {
        g.dispose();
        File f = new File(OUT_DIR, name);
        ImageWriter writer = ImageIO.getImageWritersByFormatName("png").next();
        ImageWriteParam param = writer.getDefaultWriteParam();
        IIOMetadata meta = writer.getDefaultImageMetadata(
                ImageTypeSpecifier.createFromRenderedImage(img), param);
        double mmPerPixel = 25.4 / DPI;
        IIOMetadataNode h = new IIOMetadataNode("HorizontalPixelSize");
        h.setAttribute("value", Double.toString(mmPerPixel));
        IIOMetadataNode v = new IIOMetadataNode("VerticalPixelSize");
        v.setAttribute("value", Double.toString(mmPerPixel));
        IIOMetadataNode dim = new IIOMetadataNode("Dimension");
        dim.appendChild(h);
        dim.appendChild(v);
        IIOMetadataNode root = new IIOMetadataNode("javax_imageio_1.0");
        root.appendChild(dim);
        meta.mergeTree("javax_imageio_1.0", root);
        try (ImageOutputStream ios = ImageIO.createImageOutputStream(f)) {
            writer.setOutput(ios);
            writer.write(null, new IIOImage(img, null, meta), param);
        }
        writer.dispose();
        System.out.printf("Saved %s (%d x %d px, 300 dpi)%n", f.getPath(), img.getWidth(), img.getHeight());
    }

    // ------------------------------------------------------------------ figures

    /** Figure 1: conceptual pathways from climate inaction to economic loss. */
    static void figure1() throws Exception {
        double W = 540, H = 340;
        BufferedImage img = canvas(W, H);
        text("Climate inaction: continued emissions and under-investment in adaptation",
                W / 2, 14, 10.5f, Font.BOLD, Color.BLACK, 0);

        String[] titles = {"Climate hazards", "Health impacts", "Economic channels", "Macroeconomic outcomes"};
        Color[] cols = {HAZ, HEALTH, ECON, MACRO};
        String[][] items = {
                {"Extreme heat and\nhumid heat", "Floods, storms\nand cyclones", "Drought and\nwildfire",
                        "Shifting vector and\npathogen ranges"},
                {"Heat illness and\nexcess mortality", "Injury, displacement\nand mental ill-health",
                        "Malnutrition and\nfood insecurity", "Vector-, water- and\nfood-borne disease"},
                {"Lost labour hours\nand presenteeism", "Rising health-care\ndemand and costs",
                        "Damaged facilities and\nsupply disruption", "Premature death and\nlost human capital"},
                {"Slower GDP growth", "Fiscal pressure and\nhigher public debt",
                        "Wider inequality and\npoverty traps", "Financial-system\nand insurance stress"}};
        double bw = 112, bh = 48, gap = (W - 20 - 4 * bw) / 3.0;
        double[] ys = {58, 118, 178, 238};
        for (int c = 0; c < 4; c++) {
            double x = 10 + c * (bw + gap);
            text(titles[c], x + bw / 2, 42, 9.5f, Font.BOLD, cols[c], 0);
            for (int r = 0; r < 4; r++) {
                box(x, ys[r], bw, bh, cols[c], items[c][r], 7.8f);
                if (c < 3) {
                    arrow(x + bw + 2, ys[r] + bh / 2, x + bw + gap - 2, ys[r] + bh / 2, GREY);
                }
            }
        }
        // Feedback loop from macro outcomes back to hazards (dashed curve)
        double xr = 10 + 3 * (bw + gap) + bw / 2, xl = 10 + bw / 2;
        g.setColor(GREY);
        g.setStroke(new BasicStroke(1.2f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_ROUND, 10f,
                new float[]{4f, 3f}, 0f));
        Path2D curve = new Path2D.Double();
        curve.moveTo(xr, 289);
        curve.curveTo(xr, 318, xl, 318, xl, 291);
        g.draw(curve);
        arrowHead(xl + 0.01, 300, xl, 289, GREY);
        text("Feedback: lost output and fiscal strain reduce the capacity to invest in mitigation and\n"
                        + "adaptation, which raises future exposure and locks in higher costs",
                W / 2, 326, 7.8f, Font.ITALIC, GREY, 0);
        save(img, "Figure_1_Pathways_Framework.png");
    }

    /** Figure 2: sector productivity losses to 2050 (a) and heat costs in 2024 (b). */
    static void figure2() throws Exception {
        double W = 540, H = 250;
        BufferedImage img = canvas(W, H);
        barPanel(0, 0, 270, H, "(a) Climate-health productivity losses by 2050",
                "Cumulative loss to 2050 (US$ billion)",
                new String[]{"Food and\nagriculture", "Built\nenvironment", "Health and\nhealthcare"},
                new double[]{740, 570, 200}, null, new Color[]{MACRO, ECON, HEALTH},
                800, 200, new String[]{"US$740 bn", "US$570 bn", "US$200 bn"}, "%.0f");
        text("Combined: at least US$1.5 trillion", 205, 52, 7.8f, Font.ITALIC, GREY, 0);

        // Panel b: horizontal bars
        double x0 = 285, left = x0 + 92, right = W - 40, top = 50, bottom = H - 40;
        text("(b) Economic costs of heat exposure in 2024", x0 + 4, 13, 9.5f, Font.BOLD, Color.BLACK, -1);
        text("640 billion potential labour hours lost", x0 + 4, 29, 7.8f, Font.ITALIC, GREY, -1);
        double xmax = 1200;
        g.setStroke(new BasicStroke(0.5f));
        for (double t = 0; t <= xmax; t += 300) {
            double xx = left + (right - left) * t / xmax;
            g.setColor(LIGHT_GRID);
            g.draw(new Line2D.Double(xx, top, xx, bottom));
            text(String.format("%,.0f", t), xx, bottom + 9, 7.5f, Font.PLAIN, GREY, 0);
        }
        g.setColor(Color.BLACK);
        g.setStroke(new BasicStroke(0.8f));
        g.draw(new Line2D.Double(left, top, left, bottom));
        g.draw(new Line2D.Double(left, bottom, right, bottom));
        text("US$ billion (2024)", (left + right) / 2, bottom + 24, 7.8f, Font.PLAIN, Color.BLACK, 0);
        String[] labs = {"Potential income lost\nfrom heat-reduced\nlabour capacity",
                "Monetised value of\nheat-related deaths\nin people over 65"};
        double[] vals = {1090, 261};
        Color[] cc = {HAZ, GREY};
        double slot = (bottom - top) / 2;
        for (int i = 0; i < 2; i++) {
            double cy = top + slot * (i + 0.5), bh = slot * 0.5;
            double bwid = (right - left) * vals[i] / xmax;
            Rectangle2D r = new Rectangle2D.Double(left, cy - bh / 2, bwid, bh);
            g.setColor(cc[i]);
            g.fill(r);
            g.setColor(Color.BLACK);
            g.setStroke(new BasicStroke(0.6f));
            g.draw(r);
            text(labs[i], left - 4, cy, 7.6f, Font.PLAIN, Color.BLACK, 1);
            String vl = String.format("US$%,.0f bn", vals[i]);
            if (i == 0) {
                text(vl, left + bwid - 4, cy, 8.5f, Font.BOLD, Color.WHITE, 1);
            } else {
                text(vl, left + bwid + 4, cy, 8.5f, Font.BOLD, Color.BLACK, -1);
            }
        }
        save(img, "Figure_2_Productivity_Losses.png");
    }

    /** Figure 3: projected climate-attributable deaths and economic costs to 2050. */
    static void figure3() throws Exception {
        double W = 540, H = 210;
        BufferedImage img = canvas(W, H);
        String[] rows = {"World Bank (2024)\n69 LMICs, 2026-2050", "WEF and Oliver Wyman\n(2024), global to 2050"};
        double[][] deaths = {{14.5, 15.6}, {14.5, 14.5}};
        double[][] costs = {{8.6, 20.8}, {12.5, 12.5}};

        rangePanel(0, 0, 270, H, "(a) Additional deaths (millions)", rows, true, deaths, 13.5, 16.5, 0.5,
                HAZ, new String[]{"14.5-15.6 million", "14.5 million"}, "%.1f");
        rangePanel(270, 0, 270, H, "(b) Economic losses (US$ trillion)", rows, false, costs, 0, 25, 5,
                ECON, new String[]{"US$8.6-20.8 tn", "US$12.5 tn, incl.\nUS$1.1 tn extra\nhealth-care costs"},
                "%.0f");
        save(img, "Figure_3_Mortality_Economic_Projections.png");
    }

    static void rangePanel(double x0, double y0, double w, double h, String title, String[] rows,
                           boolean showRowLabels, double[][] vals, double xmin, double xmax, double step,
                           Color c, String[] valueLabels, String tickFmt) {
        double left = x0 + (showRowLabels ? 96 : 14), right = x0 + w - 12, top = y0 + 30, bottom = y0 + h - 30;
        text(title, x0 + (showRowLabels ? 4 : 14), y0 + 13, 9.5f, Font.BOLD, Color.BLACK, -1);
        g.setStroke(new BasicStroke(0.5f));
        for (double t = xmin; t <= xmax + 1e-9; t += step) {
            double xx = left + (right - left) * (t - xmin) / (xmax - xmin);
            g.setColor(LIGHT_GRID);
            g.draw(new Line2D.Double(xx, top, xx, bottom));
            text(String.format(tickFmt, t), xx, bottom + 9, 7.5f, Font.PLAIN, GREY, 0);
        }
        g.setColor(Color.BLACK);
        g.setStroke(new BasicStroke(0.8f));
        g.draw(new Line2D.Double(left, bottom, right, bottom));
        double slot = (bottom - top) / rows.length;
        for (int i = 0; i < rows.length; i++) {
            double cy = top + slot * (i + 0.5);
            if (showRowLabels) text(rows[i], left - 6, cy, 7.6f, Font.PLAIN, Color.BLACK, 1);
            double xa = left + (right - left) * (vals[i][0] - xmin) / (xmax - xmin);
            double xb = left + (right - left) * (vals[i][1] - xmin) / (xmax - xmin);
            if (xb - xa > 1) {
                g.setColor(c);
                g.setStroke(new BasicStroke(9f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
                g.draw(new Line2D.Double(xa, cy, xb, cy));
            } else {
                g.setColor(c);
                g.fill(new Ellipse2D.Double(xa - 5, cy - 5, 10, 10));
            }
            boolean labelLeft = xb > right - 70;
            if (labelLeft) {
                text(valueLabels[i], xa - 9, cy - 16, 7.8f, Font.BOLD, Color.BLACK, -1);
            } else {
                text(valueLabels[i], xb + 9, cy, 7.8f, Font.BOLD, Color.BLACK, -1);
            }
        }
    }

    /** Figure 4: cost of delay versus returns to early action. */
    static void figure4() throws Exception {
        double W = 540, H = 240;
        BufferedImage img = canvas(W, H);
        barPanel(0, 0, 175, H, "(a) Transition cost by 2030", "% of global GDP",
                new String[]{"Timely\naction", "Three-year\ndelay"}, new double[]{0.5, 1.3}, null,
                new Color[]{MACRO, HAZ}, 1.5, 0.5, new String[]{"0.5%", "1.3%"}, "%.1f");
        barPanel(180, 0, 175, H, "(b) Returns to adaptation", "US$ trillion, 2020-2030",
                new String[]{"Investment", "Net\nbenefits"}, new double[]{1.8, 7.1}, null,
                new Color[]{ECON, MACRO}, 8, 2, new String[]{"US$1.8 tn", "US$7.1 tn"}, "%.0f");
        barPanel(360, 0, 180, H, "(c) Adaptation finance gap", "US$ billion per year",
                new String[]{"Public flows\n(2023)", "Need by\n2035"}, new double[]{26, 310},
                new double[]{0, 55}, new Color[]{GREY, HEALTH}, 400, 100,
                new String[]{"US$26 bn", "US$310-365 bn"}, "%.0f");
        save(img, "Figure_4_Cost_of_Delay.png");
    }

    public static void main(String[] args) throws Exception {
        System.setProperty("java.awt.headless", "true");
        new File(OUT_DIR).mkdirs();
        figure1();
        figure2();
        figure3();
        figure4();
    }
}
