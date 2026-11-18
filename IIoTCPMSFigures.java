/*
 * Generates the four figures for the chapter
 * "Industrial Internet of Things and Cyber-Physical Manufacturing Systems:
 *  Foundations, Architectures and Pathways for Industry 5.0".
 *
 * JDK only (Java2D + ImageIO); matplotlib/PIL are not available in this sandbox.
 * Figures are drawn in point units and rendered at 300 dpi with a 300 dpi pHYs chunk.
 *
 * Usage (JDK 11+):  java IIoTCPMSFigures.java
 */

import javax.imageio.*;
import javax.imageio.metadata.*;
import javax.imageio.stream.ImageOutputStream;
import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.io.File;

public class IIoTCPMSFigures {

    static final String OUT_DIR = "/projects/sandbox/AMMAN/iiot_cpms_figures";
    static final double DPI = 300.0;
    static final double S = DPI / 72.0;
    static final String FONT = "Noto Sans";

    static final Color C1 = new Color(0x1B4F72);   // dark blue
    static final Color C2 = new Color(0x2471A3);   // blue
    static final Color C3 = new Color(0x17A589);   // teal
    static final Color C4 = new Color(0xD68910);   // amber
    static final Color C5 = new Color(0xC0392B);   // red
    static final Color C6 = new Color(0x7D3C98);   // purple
    static final Color GREY = new Color(0x566573);

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
        return new Color((int) (255 - (255 - c.getRed()) * a), (int) (255 - (255 - c.getGreen()) * a),
                (int) (255 - (255 - c.getBlue()) * a));
    }

    /** Multi-line text; align -1 left, 0 centre, 1 right; y is the vertical centre. */
    static void text(String s, double x, double y, float size, int style, Color c, int align) {
        g.setFont(new Font(FONT, style, 1).deriveFont(size));
        g.setColor(c);
        FontMetrics fm = g.getFontMetrics();
        String[] lines = s.split("\n");
        double lh = size * 1.22, top = y - lh * lines.length / 2.0;
        for (int i = 0; i < lines.length; i++) {
            double w = fm.getStringBounds(lines[i], g).getWidth();
            double xx = align == 0 ? x - w / 2 : (align > 0 ? x - w : x);
            double base = top + lh * i + lh / 2 + fm.getAscent() / 2.0 - fm.getDescent() / 2.0;
            g.drawString(lines[i], (float) xx, (float) base);
        }
    }

    static void rbox(double x, double y, double w, double h, Color c, double fillA) {
        RoundRectangle2D r = new RoundRectangle2D.Double(x, y, w, h, 7, 7);
        g.setColor(tint(c, fillA));
        g.fill(r);
        g.setColor(c);
        g.setStroke(new BasicStroke(1.0f));
        g.draw(r);
    }

    static void box(double x, double y, double w, double h, Color c, String s, float size) {
        rbox(x, y, w, h, c, 0.15);
        text(s, x + w / 2, y + h / 2, size, Font.PLAIN, Color.BLACK, 0);
    }

    static void arrowHead(double x1, double y1, double x2, double y2, Color c) {
        double a = Math.atan2(y2 - y1, x2 - x1), len = 6, wid = 3;
        Path2D p = new Path2D.Double();
        p.moveTo(x2, y2);
        p.lineTo(x2 - len * Math.cos(a) + wid * Math.sin(a), y2 - len * Math.sin(a) - wid * Math.cos(a));
        p.lineTo(x2 - len * Math.cos(a) - wid * Math.sin(a), y2 - len * Math.sin(a) + wid * Math.cos(a));
        p.closePath();
        g.setColor(c);
        g.fill(p);
    }

    static void arrow(double x1, double y1, double x2, double y2, Color c, boolean both) {
        g.setColor(c);
        g.setStroke(new BasicStroke(1.1f));
        double a = Math.atan2(y2 - y1, x2 - x1);
        double sx = both ? x1 + 5 * Math.cos(a) : x1, sy = both ? y1 + 5 * Math.sin(a) : y1;
        g.draw(new Line2D.Double(sx, sy, x2 - 5 * Math.cos(a), y2 - 5 * Math.sin(a)));
        arrowHead(x1, y1, x2, y2, c);
        if (both) arrowHead(x2, y2, x1, y1, c);
    }

    static void save(BufferedImage img, String name) throws Exception {
        g.dispose();
        File f = new File(OUT_DIR, name);
        ImageWriter w = ImageIO.getImageWritersByFormatName("png").next();
        ImageWriteParam p = w.getDefaultWriteParam();
        IIOMetadata meta = w.getDefaultImageMetadata(ImageTypeSpecifier.createFromRenderedImage(img), p);
        String mm = Double.toString(25.4 / DPI);
        IIOMetadataNode h = new IIOMetadataNode("HorizontalPixelSize");
        h.setAttribute("value", mm);
        IIOMetadataNode v = new IIOMetadataNode("VerticalPixelSize");
        v.setAttribute("value", mm);
        IIOMetadataNode dim = new IIOMetadataNode("Dimension");
        dim.appendChild(h);
        dim.appendChild(v);
        IIOMetadataNode root = new IIOMetadataNode("javax_imageio_1.0");
        root.appendChild(dim);
        meta.mergeTree("javax_imageio_1.0", root);
        try (ImageOutputStream ios = ImageIO.createImageOutputStream(f)) {
            w.setOutput(ios);
            w.write(null, new IIOImage(img, null, meta), p);
        }
        w.dispose();
        System.out.printf("Saved %s (%d x %d px, 300 dpi)%n", f.getPath(), img.getWidth(), img.getHeight());
    }

    // ------------------------------------------------------------------ figures

    /** Figure 1: the 5C architecture as a pyramid with functions and outputs. */
    static void figure1() throws Exception {
        double W = 540, H = 330;
        BufferedImage img = canvas(W, H);
        text("The 5C architecture for cyber-physical manufacturing systems", W / 2, 14, 10.5f,
                Font.BOLD, Color.BLACK, 0);
        String[] lvl = {"V. Configuration", "IV. Cognition", "III. Cyber", "II. Conversion", "I. Connection"};
        String[] fn = {
                "Self-configuration, self-adjustment and self-optimisation;\nsupervisory control feeds decisions back to machines",
                "Integrated simulation and synthesis; diagnosis and\ndecision support presented to human operators",
                "Digital twin of each component and machine; fleet-level\ncomparison, clustering and similarity analysis",
                "Signal processing and feature extraction; degradation\nand health-value estimation (data to information)",
                "Plug-and-play acquisition from sensors, controllers and\nenterprise systems; tether-free, reliable communication"};
        Color[] col = {C6, C5, C4, C3, C2};
        double cx = 165, top = 40, lh = 52, baseW = 250, topW = 70;
        for (int i = 0; i < 5; i++) {
            double y0 = top + i * lh, y1 = y0 + lh - 4;
            double w0 = topW + (baseW - topW) * i / 5.0, w1 = topW + (baseW - topW) * (i + 1) / 5.0;
            Path2D p = new Path2D.Double();
            p.moveTo(cx - w0 / 2, y0);
            p.lineTo(cx + w0 / 2, y0);
            p.lineTo(cx + w1 / 2, y1);
            p.lineTo(cx - w1 / 2, y1);
            p.closePath();
            g.setColor(col[i]);
            g.fill(p);
            text(lvl[i], cx, (y0 + y1) / 2, 8.6f, Font.BOLD, Color.WHITE, 0);
            rbox(306, y0 + 2, 228, lh - 8, col[i], 0.12);
            text(fn[i], 312, (y0 + y1) / 2, 7.6f, Font.PLAIN, Color.BLACK, -1);
            g.setColor(col[i]);
            g.setStroke(new BasicStroke(0.8f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER, 10f,
                    new float[]{2f, 2f}, 0f));
            g.draw(new Line2D.Double(cx + w1 / 2 + 4, (y0 + y1) / 2, 304, (y0 + y1) / 2));
        }
        // Side arrows: data flow up, control flow down
        double ax = 18;
        arrow(ax, top + 5 * lh - 6, ax, top + 4, C1, false);
        AffineTransform old = g.getTransform();
        g.translate(ax - 9, top + 5 * lh / 2.0);
        g.rotate(-Math.PI / 2);
        text("Data and information flow (upward); decisions flow back down", 0, 0, 7.2f, Font.ITALIC, C1, 0);
        g.setTransform(old);
        text("Value: from raw signals (I) to\nresilient, self-adapting production (V)", W / 2,
                top + 5 * lh + 14, 7.6f, Font.ITALIC, GREY, 0);
        save(img, "Figure_1_5C_Architecture.png");
    }

    /** Figure 2: layered IIoT network architecture across the edge-cloud continuum. */
    static void figure2() throws Exception {
        double W = 540, H = 350;
        BufferedImage img = canvas(W, H);
        text("Layered IIoT architecture across the edge-cloud continuum", W / 2, 14, 10.5f, Font.BOLD,
                Color.BLACK, 0);
        String[] layer = {"Cloud", "Fog / plant\n(on-premises)", "Edge", "Field level"};
        String[][] items = {
                {"Enterprise analytics\nand model training", "ERP, supply chain\nand fleet twins", "Long-term data\nlake and archive"},
                {"MES and\nscheduling", "Plant historian and\ntime-series store", "Site-level\ndigital twin"},
                {"Industrial edge\ngateways", "Stream processing\nand ML inference", "Protocol translation\nand security zone"},
                {"Sensors and\nactuators", "PLCs, drives\nand robots", "Wearables and\nAR devices"}};
        String[] lat = {"seconds to\nhours", "100 ms to\nseconds", "1 to 100 ms", "under 1 ms\n(deterministic)"};
        String[] proto = {"HTTPS, AMQP, MQTT", "OPC UA, MQTT, ISA-95 interfaces",
                "OPC UA, MQTT, 5G URLLC", "EtherCAT, PROFINET, TSN, Modbus, IO-Link"};
        Color[] col = {C6, C4, C3, C2};
        double top = 34, lh = 72, x0 = 78, x1 = 452;
        for (int i = 0; i < 4; i++) {
            double y = top + i * lh;
            rbox(x0, y, x1 - x0, lh - 8, col[i], 0.08);
            text(layer[i], 40, y + (lh - 8) / 2, 8.6f, Font.BOLD, col[i], 0);
            double bw = 110, gap = ((x1 - x0) - 3 * bw - 16) / 2.0;
            for (int j = 0; j < 3; j++) {
                box(x0 + 8 + j * (bw + gap), y + 6, bw, 36, col[i], items[i][j], 7.4f);
            }
            text(proto[i], (x0 + x1) / 2, y + 53, 7.0f, Font.ITALIC, GREY, 0);
            text(lat[i], 497, y + (lh - 8) / 2, 7.6f, Font.PLAIN, Color.BLACK, 0);
        }
        text("Typical\nlatency", 497, top - 6, 7.6f, Font.BOLD, Color.BLACK, 0);
        // Vertical trade-off arrow
        double ax = 530;
        arrow(ax, top + 4 * lh - 10, ax, top + 6, GREY, false);
        text("Upward: more compute, storage and context.  Downward: lower latency, higher determinism, data locality",
                W / 2, top + 4 * lh + 4, 7.2f, Font.ITALIC, GREY, 0);
        save(img, "Figure_2_Edge_Cloud_Architecture.png");
    }

    /** Figure 3: human-centric adaptive CPMS control loop. */
    static void figure3() throws Exception {
        double W = 540, H = 360;
        BufferedImage img = canvas(W, H);
        text("Human-centric adaptive manufacturing loop enabled by IIoT", W / 2, 14, 10.5f, Font.BOLD,
                Color.BLACK, 0);
        double cx = 270, cy = 182, R = 118;
        // central twin
        Ellipse2D core = new Ellipse2D.Double(cx - 70, cy - 36, 140, 72);
        g.setColor(tint(C1, 0.15));
        g.fill(core);
        g.setColor(C1);
        g.setStroke(new BasicStroke(1.2f));
        g.draw(core);
        text("Digital twin and\nCPMS decision layer", cx, cy - 6, 8.6f, Font.BOLD, C1, 0);
        text("synchronised model of\nassets, process and people", cx, cy + 18, 7.0f, Font.ITALIC, GREY, 0);

        String[] node = {
                "SENSE\nIIoT sensors, machine\ncontrollers, vision",
                "ANALYSE\nedge analytics, anomaly\ndetection, quality prediction",
                "DECIDE\nscheduling, re-planning,\nprocess optimisation",
                "ACT\nadaptive machines, cobots,\nAGVs, reconfiguration",
                "HUMAN OPERATOR\nAR guidance, wearables,\nexoskeletons, feedback"};
        Color[] col = {C2, C3, C4, C5, C6};
        double[] ang = {-90, -18, 54, 126, 198};
        double bw = 136, bh = 50;
        double[][] pos = new double[5][2];
        for (int i = 0; i < 5; i++) {
            double a = Math.toRadians(ang[i]);
            pos[i][0] = cx + R * 1.45 * Math.cos(a);
            pos[i][1] = cy + R * Math.sin(a);
        }
        for (int i = 0; i < 5; i++) {
            int j = (i + 1) % 5;
            double dx = pos[j][0] - pos[i][0], dy = pos[j][1] - pos[i][1], d = Math.hypot(dx, dy);
            double ux = dx / d, uy = dy / d;
            double t = Math.min((bw / 2 + 4) / Math.max(Math.abs(ux), 1e-6), (bh / 2 + 4) / Math.max(Math.abs(uy), 1e-6));
            double sx = pos[i][0] + ux * t, sy = pos[i][1] + uy * t;
            double ex = pos[j][0] - ux * t, ey = pos[j][1] - uy * t;
            arrow(sx, sy, ex, ey, GREY, false);
            // spoke to centre
            g.setColor(tint(GREY, 0.6));
            g.setStroke(new BasicStroke(0.8f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER, 10f,
                    new float[]{3f, 2f}, 0f));
            double ddx = cx - pos[i][0], ddy = cy - pos[i][1], dd = Math.hypot(ddx, ddy);
            g.draw(new Line2D.Double(pos[i][0] + ddx / dd * 30, pos[i][1] + ddy / dd * 26,
                    cx - ddx / dd * 74, cy - ddy / dd * 40));
        }
        for (int i = 0; i < 5; i++) {
            rbox(pos[i][0] - bw / 2, pos[i][1] - bh / 2, bw, bh, col[i], 0.15);
            String[] parts = node[i].split("\n", 2);
            text(parts[0], pos[i][0], pos[i][1] - 15, 8.0f, Font.BOLD, col[i], 0);
            text(parts[1], pos[i][0], pos[i][1] + 7, 7.2f, Font.PLAIN, Color.BLACK, 0);
        }
        // Wellbeing monitoring note
        rbox(18, 318, 504, 30, GREY, 0.06);
        text("Cross-cutting: worker safety and wellbeing monitoring (fatigue, ergonomics, cognitive load), "
                + "cybersecurity zones and\nfunctional-safety interlocks constrain every transition in the loop",
                W / 2, 333, 7.4f, Font.PLAIN, Color.BLACK, 0);
        save(img, "Figure_3_Human_Centric_Loop.png");
    }

    /** Figure 4: phased implementation roadmap aligned with acatech maturity stages. */
    static void figure4() throws Exception {
        double W = 540, H = 300;
        BufferedImage img = canvas(W, H);
        text("Phased IIoT-CPMS implementation roadmap aligned with maturity stages", W / 2, 14, 10.5f,
                Font.BOLD, Color.BLACK, 0);
        String[] stage = {"1 Computer-\nisation", "2 Connec-\ntivity", "3 Visibility", "4 Trans-\nparency",
                "5 Predictive\ncapacity", "6 Adapt-\nability"};
        String[] q = {"", "", "What is\nhappening?", "Why is it\nhappening?", "What will\nhappen?",
                "How can the system\nrespond autonomously?"};
        Color[] col = {tint(C2, 0.45), tint(C2, 0.65), C2, C3, C4, C5};
        double x0 = 14, cw = 86, ch = 46, y = 56;
        for (int i = 0; i < 6; i++) {
            double x = x0 + i * (cw - 2);
            Path2D p = new Path2D.Double();
            p.moveTo(x, y);
            p.lineTo(x + cw - 12, y);
            p.lineTo(x + cw, y + ch / 2);
            p.lineTo(x + cw - 12, y + ch);
            p.lineTo(x, y + ch);
            if (i > 0) p.lineTo(x + 12, y + ch / 2);
            p.closePath();
            g.setColor(col[i]);
            g.fill(p);
            g.setColor(Color.WHITE);
            g.setStroke(new BasicStroke(1.5f));
            g.draw(p);
            text(stage[i], x + cw / 2 + 2, y + ch / 2, 7.6f, Font.BOLD, Color.WHITE, 0);
            if (!q[i].isEmpty()) text(q[i], x + cw / 2 + 2, y + ch + 16, 7.0f, Font.ITALIC, GREY, 0);
        }
        text("acatech Industrie 4.0 Maturity Index stages", W / 2, 40, 8.2f, Font.BOLD, C1, 0);
        text("Foundations of digitalisation", x0 + cw - 2, y - 7, 7.0f, Font.ITALIC, GREY, 0);

        // Roadmap phases under the stages
        String[] ph = {"Phase A: Assess", "Phase B: Pilot", "Phase C: Integrate", "Phase D: Scale and adapt"};
        String[] act = {
                "Maturity audit (IMPULS,\nacatech); value-case and\nuse-case prioritisation;\nOT asset and risk inventory",
                "Retrofit sensors and edge\ngateways on one line;\nOPC UA/MQTT data model;\nIEC 62443 zones and conduits",
                "MES/ERP integration via\nISA-95; plant historian;\ndigital twin (ISO 23247);\nworkforce upskilling",
                "Multi-site rollout; closed-loop\nand self-optimising control;\nhuman-robot collaboration;\nsustainability KPIs"};
        Color[] pc = {C1, C3, C4, C5};
        double py = 150, pw = 124, gap = (W - 28 - 4 * pw) / 3.0;
        for (int i = 0; i < 4; i++) {
            double x = 14 + i * (pw + gap);
            rbox(x, py, pw, 22, pc[i], 1.0);
            text(ph[i], x + pw / 2, py + 11, 8.0f, Font.BOLD, Color.WHITE, 0);
            rbox(x, py + 26, pw, 62, pc[i], 0.10);
            text(act[i], x + 6, py + 57, 7.1f, Font.PLAIN, Color.BLACK, -1);
            if (i < 3) arrow(x + pw + 1, py + 11, x + pw + gap - 1, py + 11, GREY, false);
        }
        g.setColor(GREY);
        g.setStroke(new BasicStroke(1.0f));
        arrow(14, 258, W - 14, 258, GREY, false);
        text("Increasing integration, data value and autonomy; human oversight retained at every phase",
                W / 2, 272, 7.6f, Font.ITALIC, GREY, 0);
        save(img, "Figure_4_Implementation_Roadmap.png");
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
