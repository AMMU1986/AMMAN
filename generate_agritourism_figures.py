#!/usr/bin/env python3
"""
Generate 4 high-quality SVG figures for the Agricultural Tourism
and Regenerative Farming Landscapes chapter.
"""
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agritourism_figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)



def figure1_conceptual_framework():
    """Figure 1: Conceptual Framework - Integration of Agricultural Tourism
    and Regenerative Farming (Venn Diagram style)"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 650" width="900" height="650">
  <defs>
    <style>
      .title { font: bold 20px 'Segoe UI', Arial, sans-serif; fill: #1a1a1a; }
      .subtitle { font: 14px 'Segoe UI', Arial, sans-serif; fill: #444; }
      .label { font: bold 14px 'Segoe UI', Arial, sans-serif; fill: #1a1a1a; }
      .item { font: 12px 'Segoe UI', Arial, sans-serif; fill: #333; }
      .overlap-item { font: bold 12px 'Segoe UI', Arial, sans-serif; fill: #1a1a1a; }
      .note { font: italic 11px 'Segoe UI', Arial, sans-serif; fill: #666; }
    </style>
  </defs>
  <!-- Background -->
  <rect width="900" height="650" fill="#fafbfc" rx="8"/>
  <!-- Title -->
  <text x="450" y="35" text-anchor="middle" class="title">Figure 1. Conceptual Framework: Integration of Agricultural Tourism</text>
  <text x="450" y="57" text-anchor="middle" class="title">and Regenerative Farming Landscapes</text>
  <!-- Left circle - Agricultural Tourism -->
  <circle cx="320" cy="320" r="190" fill="#4a90d9" fill-opacity="0.2" stroke="#4a90d9" stroke-width="2.5"/>
  <!-- Right circle - Regenerative Farming -->
  <circle cx="580" cy="320" r="190" fill="#27ae60" fill-opacity="0.2" stroke="#27ae60" stroke-width="2.5"/>
  <!-- Labels -->
  <text x="220" y="160" text-anchor="middle" class="label" fill="#2c5f9e">AGRICULTURAL</text>
  <text x="220" y="180" text-anchor="middle" class="label" fill="#2c5f9e">TOURISM</text>
  <text x="680" y="160" text-anchor="middle" class="label" fill="#1e7a42">REGENERATIVE</text>
  <text x="680" y="180" text-anchor="middle" class="label" fill="#1e7a42">FARMING</text>
  <!-- Left items -->
  <text x="210" y="230" text-anchor="middle" class="item">• Visitor experiences</text>
  <text x="210" y="255" text-anchor="middle" class="item">• Farm stays &amp; eco-lodges</text>
  <text x="210" y="280" text-anchor="middle" class="item">• Culinary tourism</text>
  <text x="210" y="305" text-anchor="middle" class="item">• Educational programmes</text>
  <text x="210" y="330" text-anchor="middle" class="item">• Cultural heritage</text>
  <text x="210" y="355" text-anchor="middle" class="item">• Income diversification</text>
  <text x="210" y="380" text-anchor="middle" class="item">• Rural employment</text>
  <text x="210" y="405" text-anchor="middle" class="item">• Community engagement</text>
  <!-- Right items -->
  <text x="690" y="230" text-anchor="middle" class="item">• Soil health restoration</text>
  <text x="690" y="255" text-anchor="middle" class="item">• Carbon sequestration</text>
  <text x="690" y="280" text-anchor="middle" class="item">• Biodiversity conservation</text>
  <text x="690" y="305" text-anchor="middle" class="item">• Water cycle improvement</text>
  <text x="690" y="330" text-anchor="middle" class="item">• Minimal tillage</text>
  <text x="690" y="355" text-anchor="middle" class="item">• Cover cropping</text>
  <text x="690" y="380" text-anchor="middle" class="item">• Integrated livestock</text>
  <text x="690" y="405" text-anchor="middle" class="item">• Ecosystem services</text>
  <!-- Overlap items -->
  <text x="450" y="260" text-anchor="middle" class="overlap-item">Sustainability</text>
  <text x="450" y="285" text-anchor="middle" class="overlap-item">Multifunctionality</text>
  <text x="450" y="310" text-anchor="middle" class="overlap-item">Rural resilience</text>
  <text x="450" y="335" text-anchor="middle" class="overlap-item">Landscape aesthetics</text>
  <text x="450" y="360" text-anchor="middle" class="overlap-item">Knowledge transfer</text>
  <text x="450" y="385" text-anchor="middle" class="overlap-item">Climate mitigation</text>
  <!-- Bottom outcome box -->
  <rect x="200" y="530" width="500" height="70" fill="#f39c12" fill-opacity="0.15" stroke="#f39c12" stroke-width="2" rx="8"/>
  <text x="450" y="555" text-anchor="middle" class="label" fill="#d68910">INTEGRATED OUTCOMES</text>
  <text x="450" y="578" text-anchor="middle" class="item">Resilient rural landscapes | Carbon-neutral tourism | Thriving communities</text>
  <text x="450" y="593" text-anchor="middle" class="item">Enhanced ecosystem services | Sustainable livelihoods | Food security</text>
  <!-- Arrows to outcome -->
  <path d="M350 480 L380 530" stroke="#4a90d9" stroke-width="2" fill="none" marker-end="url(#arrow-blue)"/>
  <path d="M550 480 L520 530" stroke="#27ae60" stroke-width="2" fill="none" marker-end="url(#arrow-green)"/>
  <defs>
    <marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#4a90d9"/>
    </marker>
    <marker id="arrow-green" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#27ae60"/>
    </marker>
  </defs>
  <!-- Source note -->
  <text x="450" y="635" text-anchor="middle" class="note">Source: Author's compilation based on literature review (2024)</text>
</svg>'''
    with open(os.path.join(OUTPUT_DIR, "Figure_1_Conceptual_Framework.svg"), "w") as f:
        f.write(svg)
    print("Figure 1 generated: Conceptual Framework")



def figure2_ecosystem_services():
    """Figure 2: Ecosystem Services Provided by Regenerative Agri-Tourism Landscapes
    (Radar/Spider chart style using SVG polygon)"""
    import math
    # Data: scale 0-10 for each service, comparing Conventional vs Regenerative
    categories = [
        "Carbon\nSequestration", "Biodiversity", "Water\nRetention",
        "Pollination", "Soil Health", "Aesthetic\nValue",
        "Cultural\nServices", "Food\nProduction"
    ]
    conventional = [2, 3, 3, 3, 3, 2, 2, 8]
    regenerative = [8, 8, 8, 7, 9, 8, 7, 7]

    cx, cy = 450, 340
    max_r = 180
    n = len(categories)
    angles = [i * 2 * math.pi / n - math.pi/2 for i in range(n)]

    def get_points(values, scale=10):
        pts = []
        for i, v in enumerate(values):
            r = (v / scale) * max_r
            x = cx + r * math.cos(angles[i])
            y = cy + r * math.sin(angles[i])
            pts.append(f"{x:.1f},{y:.1f}")
        return " ".join(pts)

    grid_lines = ""
    for level in [2, 4, 6, 8, 10]:
        r = (level / 10) * max_r
        pts = " ".join([f"{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}" for a in angles])
        grid_lines += f'  <polygon points="{pts}" fill="none" stroke="#ddd" stroke-width="1"/>\n'

    axis_lines = ""
    for i, a in enumerate(angles):
        x2 = cx + max_r * math.cos(a)
        y2 = cy + max_r * math.sin(a)
        axis_lines += f'  <line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#ccc" stroke-width="1"/>\n'

    labels_svg = ""
    label_texts = ["Carbon Sequestration", "Biodiversity", "Water Retention",
                   "Pollination", "Soil Health", "Aesthetic Value",
                   "Cultural Services", "Food Production"]
    for i, a in enumerate(angles):
        lx = cx + (max_r + 35) * math.cos(a)
        ly = cy + (max_r + 35) * math.sin(a)
        anchor = "middle"
        if math.cos(a) > 0.3: anchor = "start"
        elif math.cos(a) < -0.3: anchor = "end"
        labels_svg += f'  <text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" class="axis-label">{label_texts[i]}</text>\n'

    conv_pts = get_points(conventional)
    regen_pts = get_points(regenerative)

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 650" width="900" height="650">
  <defs>
    <style>
      .title {{ font: bold 18px 'Segoe UI', Arial, sans-serif; fill: #1a1a1a; }}
      .axis-label {{ font: 12px 'Segoe UI', Arial, sans-serif; fill: #333; }}
      .legend {{ font: 13px 'Segoe UI', Arial, sans-serif; fill: #333; }}
      .note {{ font: italic 11px 'Segoe UI', Arial, sans-serif; fill: #666; }}
      .scale {{ font: 10px 'Segoe UI', Arial, sans-serif; fill: #999; }}
    </style>
  </defs>
  <rect width="900" height="650" fill="#fafbfc" rx="8"/>
  <text x="450" y="35" text-anchor="middle" class="title">Figure 2. Ecosystem Services Comparison: Conventional vs. Regenerative</text>
  <text x="450" y="58" text-anchor="middle" class="title">Agri-Tourism Landscapes (Scale: 0–10)</text>
  <!-- Grid -->
{grid_lines}
  <!-- Axes -->
{axis_lines}
  <!-- Scale labels -->
  <text x="{cx+5}" y="{cy - (2/10)*max_r}" class="scale">2</text>
  <text x="{cx+5}" y="{cy - (4/10)*max_r}" class="scale">4</text>
  <text x="{cx+5}" y="{cy - (6/10)*max_r}" class="scale">6</text>
  <text x="{cx+5}" y="{cy - (8/10)*max_r}" class="scale">8</text>
  <text x="{cx+5}" y="{cy - (10/10)*max_r}" class="scale">10</text>
  <!-- Conventional polygon -->
  <polygon points="{conv_pts}" fill="#e74c3c" fill-opacity="0.15" stroke="#e74c3c" stroke-width="2.5"/>
  <!-- Regenerative polygon -->
  <polygon points="{regen_pts}" fill="#27ae60" fill-opacity="0.2" stroke="#27ae60" stroke-width="2.5"/>
  <!-- Labels -->
{labels_svg}
  <!-- Legend -->
  <rect x="320" y="575" width="20" height="14" fill="#e74c3c" fill-opacity="0.4" stroke="#e74c3c" stroke-width="1.5" rx="2"/>
  <text x="348" y="587" class="legend">Conventional Agriculture</text>
  <rect x="530" y="575" width="20" height="14" fill="#27ae60" fill-opacity="0.4" stroke="#27ae60" stroke-width="1.5" rx="2"/>
  <text x="558" y="587" class="legend">Regenerative Agri-Tourism</text>
  <!-- Source -->
  <text x="450" y="635" text-anchor="middle" class="note">Source: Adapted from Lal (2020), Kremen and Merenlender (2018), and field data compilation</text>
</svg>'''
    with open(os.path.join(OUTPUT_DIR, "Figure_2_Ecosystem_Services_Comparison.svg"), "w") as f:
        f.write(svg)
    print("Figure 2 generated: Ecosystem Services Comparison")



def figure3_visitor_experience_model():
    """Figure 3: Visitor Experience Design Model for Regenerative Farm Tourism
    (Flowchart/process diagram)"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 700" width="900" height="700">
  <defs>
    <style>
      .title { font: bold 18px 'Segoe UI', Arial, sans-serif; fill: #1a1a1a; }
      .box-title { font: bold 13px 'Segoe UI', Arial, sans-serif; fill: #fff; }
      .box-item { font: 11.5px 'Segoe UI', Arial, sans-serif; fill: #333; }
      .phase { font: bold 15px 'Segoe UI', Arial, sans-serif; fill: #555; }
      .note { font: italic 11px 'Segoe UI', Arial, sans-serif; fill: #666; }
      .outcome { font: bold 12px 'Segoe UI', Arial, sans-serif; fill: #1a1a1a; }
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <rect width="900" height="700" fill="#fafbfc" rx="8"/>
  <text x="450" y="35" text-anchor="middle" class="title">Figure 3. Visitor Experience Design Model for Regenerative Farm Tourism</text>

  <!-- Phase 1: Pre-Visit -->
  <text x="450" y="75" text-anchor="middle" class="phase">PHASE 1: PRE-VISIT ENGAGEMENT</text>
  <rect x="60" y="90" width="180" height="80" rx="6" fill="#fff" stroke="#3498db" stroke-width="2"/>
  <rect x="60" y="90" width="180" height="25" rx="6" fill="#3498db"/>
  <text x="150" y="107" text-anchor="middle" class="box-title">Digital Discovery</text>
  <text x="70" y="130" class="box-item">• Social media storytelling</text>
  <text x="70" y="147" class="box-item">• Virtual farm tours</text>
  <text x="70" y="164" class="box-item">• Online booking</text>

  <rect x="280" y="90" width="180" height="80" rx="6" fill="#fff" stroke="#3498db" stroke-width="2"/>
  <rect x="280" y="90" width="180" height="25" rx="6" fill="#3498db"/>
  <text x="370" y="107" text-anchor="middle" class="box-title">Expectation Setting</text>
  <text x="290" y="130" class="box-item">• Seasonal calendar</text>
  <text x="290" y="147" class="box-item">• Activity options</text>
  <text x="290" y="164" class="box-item">• Sustainability ethos</text>

  <rect x="500" y="90" width="180" height="80" rx="6" fill="#fff" stroke="#3498db" stroke-width="2"/>
  <rect x="500" y="90" width="180" height="25" rx="6" fill="#3498db"/>
  <text x="590" y="107" text-anchor="middle" class="box-title">Preparation</text>
  <text x="510" y="130" class="box-item">• Travel planning</text>
  <text x="510" y="147" class="box-item">• Skill matching</text>
  <text x="510" y="164" class="box-item">• Pre-visit learning</text>

  <!-- Arrow Phase 1 to 2 -->
  <line x1="450" y1="175" x2="450" y2="205" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Phase 2: On-Farm Experience -->
  <text x="450" y="225" text-anchor="middle" class="phase">PHASE 2: ON-FARM EXPERIENCE</text>
  <rect x="60" y="240" width="180" height="110" rx="6" fill="#fff" stroke="#27ae60" stroke-width="2"/>
  <rect x="60" y="240" width="180" height="25" rx="6" fill="#27ae60"/>
  <text x="150" y="257" text-anchor="middle" class="box-title">Immersive Stay</text>
  <text x="70" y="280" class="box-item">• Eco-lodge accommodation</text>
  <text x="70" y="297" class="box-item">• Farm rhythms integration</text>
  <text x="70" y="314" class="box-item">• Nature observation</text>
  <text x="70" y="331" class="box-item">• Quiet reflection spaces</text>

  <rect x="280" y="240" width="180" height="110" rx="6" fill="#fff" stroke="#27ae60" stroke-width="2"/>
  <rect x="280" y="240" width="180" height="25" rx="6" fill="#27ae60"/>
  <text x="370" y="257" text-anchor="middle" class="box-title">Active Participation</text>
  <text x="290" y="280" class="box-item">• Hands-on farming</text>
  <text x="290" y="297" class="box-item">• Soil health workshops</text>
  <text x="290" y="314" class="box-item">• Harvest activities</text>
  <text x="290" y="331" class="box-item">• Conservation tasks</text>

  <rect x="500" y="240" width="180" height="110" rx="6" fill="#fff" stroke="#27ae60" stroke-width="2"/>
  <rect x="500" y="240" width="180" height="25" rx="6" fill="#27ae60"/>
  <text x="590" y="257" text-anchor="middle" class="box-title">Culinary Experience</text>
  <text x="510" y="280" class="box-item">• Farm-to-table dining</text>
  <text x="510" y="297" class="box-item">• Cooking classes</text>
  <text x="510" y="314" class="box-item">• Food preservation</text>
  <text x="510" y="331" class="box-item">• Foraging walks</text>

  <rect x="720" y="240" width="160" height="110" rx="6" fill="#fff" stroke="#27ae60" stroke-width="2"/>
  <rect x="720" y="240" width="160" height="25" rx="6" fill="#27ae60"/>
  <text x="800" y="257" text-anchor="middle" class="box-title">Interpretation</text>
  <text x="730" y="280" class="box-item">• Guided walks</text>
  <text x="730" y="297" class="box-item">• Soil microscopy</text>
  <text x="730" y="314" class="box-item">• Wildlife ID</text>
  <text x="730" y="331" class="box-item">• Signage trails</text>

  <!-- Arrow Phase 2 to 3 -->
  <line x1="450" y1="355" x2="450" y2="385" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Phase 3: Post-Visit -->
  <text x="450" y="405" text-anchor="middle" class="phase">PHASE 3: POST-VISIT CONNECTION</text>
  <rect x="120" y="420" width="200" height="80" rx="6" fill="#fff" stroke="#8e44ad" stroke-width="2"/>
  <rect x="120" y="420" width="200" height="25" rx="6" fill="#8e44ad"/>
  <text x="220" y="437" text-anchor="middle" class="box-title">Continued Engagement</text>
  <text x="130" y="460" class="box-item">• Product subscriptions (CSA)</text>
  <text x="130" y="477" class="box-item">• Social media community</text>
  <text x="130" y="494" class="box-item">• Return visit incentives</text>

  <rect x="380" y="420" width="200" height="80" rx="6" fill="#fff" stroke="#8e44ad" stroke-width="2"/>
  <rect x="380" y="420" width="200" height="25" rx="6" fill="#8e44ad"/>
  <text x="480" y="437" text-anchor="middle" class="box-title">Behavioural Change</text>
  <text x="390" y="460" class="box-item">• Sustainable food choices</text>
  <text x="390" y="477" class="box-item">• Environmental advocacy</text>
  <text x="390" y="494" class="box-item">• Knowledge sharing</text>

  <rect x="640" y="420" width="200" height="80" rx="6" fill="#fff" stroke="#8e44ad" stroke-width="2"/>
  <rect x="640" y="420" width="200" height="25" rx="6" fill="#8e44ad"/>
  <text x="740" y="437" text-anchor="middle" class="box-title">Impact Measurement</text>
  <text x="650" y="460" class="box-item">• Visitor satisfaction surveys</text>
  <text x="650" y="477" class="box-item">• Carbon offset tracking</text>
  <text x="650" y="494" class="box-item">• Repeat visit rates</text>

  <!-- Arrow to Outcomes -->
  <line x1="450" y1="505" x2="450" y2="535" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Outcomes Box -->
  <rect x="150" y="540" width="600" height="90" rx="8" fill="#f39c12" fill-opacity="0.12" stroke="#f39c12" stroke-width="2"/>
  <text x="450" y="565" text-anchor="middle" class="phase" fill="#d68910">INTEGRATED OUTCOMES</text>
  <text x="200" y="590" class="outcome">• Enhanced visitor satisfaction</text>
  <text x="200" y="610" class="outcome">• Increased farm revenue</text>
  <text x="500" y="590" class="outcome">• Environmental education impact</text>
  <text x="500" y="610" class="outcome">• Community empowerment</text>

  <!-- Feedback loop arrow -->
  <path d="M760 580 Q 830 580, 830 400 Q 830 100, 750 90" fill="none" stroke="#999" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowhead)"/>
  <text x="850" y="340" class="box-item" fill="#999" transform="rotate(90, 850, 340)">Feedback Loop</text>

  <text x="450" y="685" text-anchor="middle" class="note">Source: Author's design based on Tew and Barbieri (2012) and Ham (2013)</text>
</svg>'''
    with open(os.path.join(OUTPUT_DIR, "Figure_3_Visitor_Experience_Model.svg"), "w") as f:
        f.write(svg)
    print("Figure 3 generated: Visitor Experience Design Model")



def figure4_future_technology_roadmap():
    """Figure 4: Technology Integration Roadmap for Regenerative Agri-Tourism
    (Timeline/roadmap style)"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 650" width="900" height="650">
  <defs>
    <style>
      .title { font: bold 18px 'Segoe UI', Arial, sans-serif; fill: #1a1a1a; }
      .era { font: bold 14px 'Segoe UI', Arial, sans-serif; fill: #fff; }
      .tech-label { font: bold 12px 'Segoe UI', Arial, sans-serif; fill: #1a1a1a; }
      .tech-item { font: 11px 'Segoe UI', Arial, sans-serif; fill: #444; }
      .layer-label { font: bold 13px 'Segoe UI', Arial, sans-serif; fill: #555; }
      .note { font: italic 11px 'Segoe UI', Arial, sans-serif; fill: #666; }
    </style>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#666"/>
    </marker>
  </defs>
  <rect width="900" height="650" fill="#fafbfc" rx="8"/>
  <text x="450" y="35" text-anchor="middle" class="title">Figure 4. Technology Integration Roadmap for Regenerative Agri-Tourism (2024–2035)</text>

  <!-- Timeline arrow -->
  <line x1="80" y1="80" x2="840" y2="80" stroke="#666" stroke-width="3" marker-end="url(#arr)"/>
  <!-- Era markers -->
  <rect x="100" y="65" width="180" height="30" rx="4" fill="#3498db"/>
  <text x="190" y="85" text-anchor="middle" class="era">2024–2026: Foundation</text>
  <rect x="310" y="65" width="180" height="30" rx="4" fill="#27ae60"/>
  <text x="400" y="85" text-anchor="middle" class="era">2027–2029: Growth</text>
  <rect x="520" y="65" width="180" height="30" rx="4" fill="#8e44ad"/>
  <text x="610" y="85" text-anchor="middle" class="era">2030–2032: Maturity</text>
  <rect x="730" y="65" width="100" height="30" rx="4" fill="#e67e22"/>
  <text x="780" y="85" text-anchor="middle" class="era">2033+</text>

  <!-- Layer 1: Precision Agriculture -->
  <text x="40" y="140" class="layer-label" transform="rotate(-90, 40, 200)">Precision Ag</text>
  <rect x="100" y="115" width="170" height="90" rx="5" fill="#3498db" fill-opacity="0.1" stroke="#3498db" stroke-width="1.5"/>
  <text x="110" y="135" class="tech-label">GPS-guided equipment</text>
  <text x="110" y="152" class="tech-item">• Variable-rate seeding</text>
  <text x="110" y="167" class="tech-item">• Soil mapping</text>
  <text x="110" y="182" class="tech-item">• Yield monitoring</text>
  <text x="110" y="197" class="tech-item">• Drone scouting</text>

  <rect x="310" y="115" width="170" height="90" rx="5" fill="#27ae60" fill-opacity="0.1" stroke="#27ae60" stroke-width="1.5"/>
  <text x="320" y="135" class="tech-label">Advanced sensing</text>
  <text x="320" y="152" class="tech-item">• Hyperspectral imaging</text>
  <text x="320" y="167" class="tech-item">• Real-time soil biology</text>
  <text x="320" y="182" class="tech-item">• Automated cover crops</text>
  <text x="320" y="197" class="tech-item">• Precision grazing</text>

  <rect x="520" y="115" width="170" height="90" rx="5" fill="#8e44ad" fill-opacity="0.1" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="530" y="135" class="tech-label">Autonomous systems</text>
  <text x="530" y="152" class="tech-item">• Robot weeding</text>
  <text x="530" y="167" class="tech-item">• AI-driven rotation</text>
  <text x="530" y="182" class="tech-item">• Predictive ecology</text>
  <text x="530" y="197" class="tech-item">• Carbon auto-reporting</text>

  <!-- Layer 2: AI & IoT -->
  <text x="40" y="275" class="layer-label" transform="rotate(-90, 40, 335)">AI &amp; IoT</text>
  <rect x="100" y="225" width="170" height="90" rx="5" fill="#3498db" fill-opacity="0.1" stroke="#3498db" stroke-width="1.5"/>
  <text x="110" y="245" class="tech-label">Sensor networks</text>
  <text x="110" y="262" class="tech-item">• Soil moisture IoT</text>
  <text x="110" y="277" class="tech-item">• Weather stations</text>
  <text x="110" y="292" class="tech-item">• Livestock GPS</text>
  <text x="110" y="307" class="tech-item">• Water quality monitors</text>

  <rect x="310" y="225" width="170" height="90" rx="5" fill="#27ae60" fill-opacity="0.1" stroke="#27ae60" stroke-width="1.5"/>
  <text x="320" y="245" class="tech-label">AI analytics</text>
  <text x="320" y="262" class="tech-item">• Biodiversity AI ID</text>
  <text x="320" y="277" class="tech-item">• Predictive pest models</text>
  <text x="320" y="292" class="tech-item">• Visitor flow AI</text>
  <text x="320" y="307" class="tech-item">• NLP farm chatbots</text>

  <rect x="520" y="225" width="170" height="90" rx="5" fill="#8e44ad" fill-opacity="0.1" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="530" y="245" class="tech-label">Digital twins</text>
  <text x="530" y="262" class="tech-item">• Farm ecosystem twins</text>
  <text x="530" y="277" class="tech-item">• Carbon cycle models</text>
  <text x="530" y="292" class="tech-item">• Regeneration forecasts</text>
  <text x="530" y="307" class="tech-item">• Virtual visitor access</text>

  <!-- Layer 3: GIS & Remote Sensing -->
  <text x="40" y="385" class="layer-label" transform="rotate(-90, 40, 445)">GIS &amp; RS</text>
  <rect x="100" y="335" width="170" height="90" rx="5" fill="#3498db" fill-opacity="0.1" stroke="#3498db" stroke-width="1.5"/>
  <text x="110" y="355" class="tech-label">Baseline mapping</text>
  <text x="110" y="372" class="tech-item">• Satellite NDVI</text>
  <text x="110" y="387" class="tech-item">• LiDAR terrain</text>
  <text x="110" y="402" class="tech-item">• Soil carbon maps</text>
  <text x="110" y="417" class="tech-item">• Trail GIS planning</text>

  <rect x="310" y="335" width="170" height="90" rx="5" fill="#27ae60" fill-opacity="0.1" stroke="#27ae60" stroke-width="1.5"/>
  <text x="320" y="355" class="tech-label">Change detection</text>
  <text x="320" y="372" class="tech-item">• Multi-temporal analysis</text>
  <text x="320" y="387" class="tech-item">• Vegetation recovery</text>
  <text x="320" y="402" class="tech-item">• Erosion monitoring</text>
  <text x="320" y="417" class="tech-item">• Habitat connectivity</text>

  <rect x="520" y="335" width="170" height="90" rx="5" fill="#8e44ad" fill-opacity="0.1" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="530" y="355" class="tech-label">Landscape intelligence</text>
  <text x="530" y="372" class="tech-item">• Real-time dashboards</text>
  <text x="530" y="387" class="tech-item">• AR landscape overlays</text>
  <text x="530" y="402" class="tech-item">• Ecosystem health index</text>
  <text x="530" y="417" class="tech-item">• Public data portals</text>

  <!-- Layer 4: Digital Tourism Platforms -->
  <text x="40" y="495" class="layer-label" transform="rotate(-90, 40, 555)">Digital Tourism</text>
  <rect x="100" y="445" width="170" height="90" rx="5" fill="#3498db" fill-opacity="0.1" stroke="#3498db" stroke-width="1.5"/>
  <text x="110" y="465" class="tech-label">Basic platforms</text>
  <text x="110" y="482" class="tech-item">• Online booking</text>
  <text x="110" y="497" class="tech-item">• QR interpretation</text>
  <text x="110" y="512" class="tech-item">• Social media</text>
  <text x="110" y="527" class="tech-item">• Review platforms</text>

  <rect x="310" y="445" width="170" height="90" rx="5" fill="#27ae60" fill-opacity="0.1" stroke="#27ae60" stroke-width="1.5"/>
  <text x="320" y="465" class="tech-label">Smart experiences</text>
  <text x="320" y="482" class="tech-item">• Mobile farm apps</text>
  <text x="320" y="497" class="tech-item">• Live data dashboards</text>
  <text x="320" y="512" class="tech-item">• Impact certificates</text>
  <text x="320" y="527" class="tech-item">• Personalised itineraries</text>

  <rect x="520" y="445" width="170" height="90" rx="5" fill="#8e44ad" fill-opacity="0.1" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="530" y="465" class="tech-label">Immersive platforms</text>
  <text x="530" y="482" class="tech-item">• VR farm experiences</text>
  <text x="530" y="497" class="tech-item">• Metaverse farming</text>
  <text x="530" y="512" class="tech-item">• Blockchain traceability</text>
  <text x="530" y="527" class="tech-item">• Token-based rewards</text>

  <!-- Vision box -->
  <rect x="730" y="225" width="140" height="310" rx="6" fill="#e67e22" fill-opacity="0.1" stroke="#e67e22" stroke-width="2"/>
  <text x="800" y="250" text-anchor="middle" class="tech-label" fill="#d35400">2033+ Vision:</text>
  <text x="740" y="275" class="tech-item">Fully integrated</text>
  <text x="740" y="295" class="tech-item">regenerative</text>
  <text x="740" y="315" class="tech-item">smart farms</text>
  <text x="740" y="345" class="tech-item">Carbon-negative</text>
  <text x="740" y="365" class="tech-item">tourism verified</text>
  <text x="740" y="385" class="tech-item">by real-time</text>
  <text x="740" y="405" class="tech-item">digital twins</text>
  <text x="740" y="435" class="tech-item">Autonomous</text>
  <text x="740" y="455" class="tech-item">ecosystem</text>
  <text x="740" y="475" class="tech-item">management</text>
  <text x="740" y="505" class="tech-item">Global regen</text>
  <text x="740" y="525" class="tech-item">tourism network</text>

  <!-- Source -->
  <text x="450" y="635" text-anchor="middle" class="note">Source: Author's projection based on current technology trajectories and industry analysis</text>
</svg>'''
    with open(os.path.join(OUTPUT_DIR, "Figure_4_Technology_Roadmap.svg"), "w") as f:
        f.write(svg)
    print("Figure 4 generated: Technology Integration Roadmap")



if __name__ == "__main__":
    print("Generating figures for Agricultural Tourism chapter...")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 50)
    figure1_conceptual_framework()
    figure2_ecosystem_services()
    figure3_visitor_experience_model()
    figure4_future_technology_roadmap()
    print("=" * 50)
    print("All 4 figures generated successfully!")
    print(f"Files saved to: {OUTPUT_DIR}/")
