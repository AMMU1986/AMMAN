#!/usr/bin/env python3
"""
Generate 4 high-quality SVG figures for Chapter 1: Introduction to Rehabilitation Robots.

Figure 1: Classification and Taxonomy of Rehabilitation Robots
Figure 2: Historical Timeline of Rehabilitation Robotics Development (1960s-Present)
Figure 3: Technology Architecture of Modern Rehabilitation Robot Systems
Figure 4: Clinical Applications Framework for Physical and Cognitive Rehabilitation
"""

import os

OUTPUT_DIR = "/projects/sandbox/AMMAN/chapter1_figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_figure_1():
    """Figure 1: Classification and Taxonomy of Rehabilitation Robots"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">
  <defs>
    <style>

      .title { font: bold 24px 'Arial', sans-serif; fill: #1a1a2e; }
      .subtitle { font: 16px 'Arial', sans-serif; fill: #4a4a6a; }
      .category-title { font: bold 16px 'Arial', sans-serif; fill: #ffffff; }
      .item-text { font: 13px 'Arial', sans-serif; fill: #2d2d44; }
      .item-text-sm { font: 11px 'Arial', sans-serif; fill: #4a4a6a; }
      .connector { stroke: #6c63ff; stroke-width: 2; fill: none; }
      .box-shadow { filter: drop-shadow(2px 3px 4px rgba(0,0,0,0.15)); }
    </style>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f093fb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f5576c;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4facfe;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#00f2fe;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#43e97b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#38f9d7;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#fa709a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#fee140;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="1200" height="800" fill="#fafbff" rx="8"/>
  <rect x="20" y="20" width="1160" height="760" fill="white" rx="6" stroke="#e8e8f0" stroke-width="1"/>
  
  <!-- Title -->
  <text x="600" y="60" class="title" text-anchor="middle">Classification and Taxonomy of Rehabilitation Robots</text>
  <text x="600" y="85" class="subtitle" text-anchor="middle">Hierarchical organization by function, structure, and deployment setting</text>
  
  <!-- Central Node -->
  <rect x="450" y="110" width="300" height="50" rx="25" fill="url(#grad1)" class="box-shadow"/>
  <text x="600" y="141" class="category-title" text-anchor="middle">REHABILITATION ROBOTS</text>
  

  <!-- Connectors from center -->
  <line x1="500" y1="160" x2="200" y2="210" class="connector"/>
  <line x1="600" y1="160" x2="600" y2="210" class="connector"/>
  <line x1="700" y1="160" x2="1000" y2="210" class="connector"/>
  
  <!-- Category 1: By Function -->
  <rect x="60" y="210" width="280" height="40" rx="20" fill="url(#grad2)" class="box-shadow"/>
  <text x="200" y="236" class="category-title" text-anchor="middle">BY FUNCTION</text>
  
  <!-- Therapeutic Robots -->
  <rect x="30" y="270" width="150" height="180" rx="8" fill="#fff5f7" stroke="#f5576c" stroke-width="1.5"/>
  <text x="105" y="295" font-size="13" font-weight="bold" fill="#f5576c" text-anchor="middle">Therapeutic</text>
  <line x1="50" y1="305" x2="160" y2="305" stroke="#f5576c" stroke-width="0.5"/>
  <text x="105" y="325" class="item-text-sm" text-anchor="middle">Motor recovery</text>
  <text x="105" y="345" class="item-text-sm" text-anchor="middle">Neuroplasticity</text>
  <text x="105" y="365" class="item-text-sm" text-anchor="middle">Task-specific training</text>
  <text x="105" y="385" class="item-text-sm" text-anchor="middle">Assist-as-needed</text>
  <text x="105" y="405" class="item-text-sm" text-anchor="middle">Intensive repetition</text>
  <text x="105" y="430" class="item-text-sm" text-anchor="middle" font-style="italic">e.g., MIT-Manus</text>
  
  <!-- Assistive Robots -->
  <rect x="200" y="270" width="150" height="180" rx="8" fill="#fff5f7" stroke="#f5576c" stroke-width="1.5"/>
  <text x="275" y="295" font-size="13" font-weight="bold" fill="#f5576c" text-anchor="middle">Assistive</text>
  <line x1="220" y1="305" x2="330" y2="305" stroke="#f5576c" stroke-width="0.5"/>
  <text x="275" y="325" class="item-text-sm" text-anchor="middle">Compensate function</text>
  <text x="275" y="345" class="item-text-sm" text-anchor="middle">Daily living support</text>
  <text x="275" y="365" class="item-text-sm" text-anchor="middle">Long-term use</text>
  <text x="275" y="385" class="item-text-sm" text-anchor="middle">Independence</text>
  <text x="275" y="405" class="item-text-sm" text-anchor="middle">Mobility aid</text>
  <text x="275" y="430" class="item-text-sm" text-anchor="middle" font-style="italic">e.g., Smart wheelchair</text>
  
  <!-- Category 2: By Structure -->
  <rect x="460" y="210" width="280" height="40" rx="20" fill="url(#grad3)" class="box-shadow"/>
  <text x="600" y="236" class="category-title" text-anchor="middle">BY STRUCTURE</text>
  

  <!-- End-Effector -->
  <rect x="430" y="270" width="160" height="180" rx="8" fill="#f0f9ff" stroke="#4facfe" stroke-width="1.5"/>
  <text x="510" y="295" font-size="13" font-weight="bold" fill="#4facfe" text-anchor="middle">End-Effector</text>
  <line x1="450" y1="305" x2="570" y2="305" stroke="#4facfe" stroke-width="0.5"/>
  <text x="510" y="325" class="item-text-sm" text-anchor="middle">Single contact point</text>
  <text x="510" y="345" class="item-text-sm" text-anchor="middle">Simple design</text>
  <text x="510" y="365" class="item-text-sm" text-anchor="middle">Easy setup</text>
  <text x="510" y="385" class="item-text-sm" text-anchor="middle">Limited joint control</text>
  <text x="510" y="405" class="item-text-sm" text-anchor="middle">Planar movements</text>
  <text x="510" y="430" class="item-text-sm" text-anchor="middle" font-style="italic">e.g., InMotion ARM</text>
  
  <!-- Exoskeleton -->
  <rect x="610" y="270" width="160" height="180" rx="8" fill="#f0f9ff" stroke="#4facfe" stroke-width="1.5"/>
  <text x="690" y="295" font-size="13" font-weight="bold" fill="#4facfe" text-anchor="middle">Exoskeleton</text>
  <line x1="630" y1="305" x2="750" y2="305" stroke="#4facfe" stroke-width="0.5"/>
  <text x="690" y="325" class="item-text-sm" text-anchor="middle">Joint alignment</text>
  <text x="690" y="345" class="item-text-sm" text-anchor="middle">Full kinematic chain</text>
  <text x="690" y="365" class="item-text-sm" text-anchor="middle">Precise joint control</text>
  <text x="690" y="385" class="item-text-sm" text-anchor="middle">Complex design</text>
  <text x="690" y="405" class="item-text-sm" text-anchor="middle">Multi-DOF support</text>
  <text x="690" y="430" class="item-text-sm" text-anchor="middle" font-style="italic">e.g., Lokomat, HAL</text>
  
  <!-- Category 3: By Setting -->
  <rect x="860" y="210" width="280" height="40" rx="20" fill="url(#grad4)" class="box-shadow"/>
  <text x="1000" y="236" class="category-title" text-anchor="middle">BY SETTING</text>
  
  <!-- Clinic-Based -->
  <rect x="840" y="270" width="150" height="180" rx="8" fill="#f0fff4" stroke="#43e97b" stroke-width="1.5"/>
  <text x="915" y="295" font-size="13" font-weight="bold" fill="#2d8a4e" text-anchor="middle">Clinic-Based</text>
  <line x1="860" y1="305" x2="970" y2="305" stroke="#43e97b" stroke-width="0.5"/>
  <text x="915" y="325" class="item-text-sm" text-anchor="middle">Stationary systems</text>
  <text x="915" y="345" class="item-text-sm" text-anchor="middle">Therapist supervised</text>
  <text x="915" y="365" class="item-text-sm" text-anchor="middle">High precision</text>
  <text x="915" y="385" class="item-text-sm" text-anchor="middle">Complex setups</text>
  <text x="915" y="405" class="item-text-sm" text-anchor="middle">Controlled environ.</text>
  <text x="915" y="430" class="item-text-sm" text-anchor="middle" font-style="italic">e.g., ARMEO Power</text>
  
  <!-- Home/Wearable -->
  <rect x="1010" y="270" width="150" height="180" rx="8" fill="#f0fff4" stroke="#43e97b" stroke-width="1.5"/>
  <text x="1085" y="295" font-size="13" font-weight="bold" fill="#2d8a4e" text-anchor="middle">Home/Wearable</text>
  <line x1="1030" y1="305" x2="1140" y2="305" stroke="#43e97b" stroke-width="0.5"/>
  <text x="1085" y="325" class="item-text-sm" text-anchor="middle">Portable systems</text>
  <text x="1085" y="345" class="item-text-sm" text-anchor="middle">Self-directed use</text>
  <text x="1085" y="365" class="item-text-sm" text-anchor="middle">Soft robotics</text>
  <text x="1085" y="385" class="item-text-sm" text-anchor="middle">Daily integration</text>
  <text x="1085" y="405" class="item-text-sm" text-anchor="middle">Tele-monitored</text>
  <text x="1085" y="430" class="item-text-sm" text-anchor="middle" font-style="italic">e.g., Soft exosuit</text>
  

  <!-- Bottom section: Target Applications -->
  <rect x="60" y="490" width="1080" height="40" rx="20" fill="url(#grad5)" class="box-shadow"/>
  <text x="600" y="516" class="category-title" text-anchor="middle">TARGET APPLICATIONS</text>
  
  <!-- Application boxes -->
  <rect x="60" y="550" width="210" height="120" rx="8" fill="#fffbf0" stroke="#fa709a" stroke-width="1.5"/>
  <text x="165" y="575" font-size="13" font-weight="bold" fill="#d63384" text-anchor="middle">Upper Limb</text>
  <line x1="80" y1="585" x2="250" y2="585" stroke="#fa709a" stroke-width="0.5"/>
  <text x="165" y="605" class="item-text-sm" text-anchor="middle">Shoulder/Elbow/Wrist</text>
  <text x="165" y="625" class="item-text-sm" text-anchor="middle">Hand/Finger dexterity</text>
  <text x="165" y="645" class="item-text-sm" text-anchor="middle">Reaching &amp; grasping</text>
  
  <rect x="290" y="550" width="210" height="120" rx="8" fill="#fffbf0" stroke="#fa709a" stroke-width="1.5"/>
  <text x="395" y="575" font-size="13" font-weight="bold" fill="#d63384" text-anchor="middle">Lower Limb</text>
  <line x1="310" y1="585" x2="480" y2="585" stroke="#fa709a" stroke-width="0.5"/>
  <text x="395" y="605" class="item-text-sm" text-anchor="middle">Gait training</text>
  <text x="395" y="625" class="item-text-sm" text-anchor="middle">Balance &amp; posture</text>
  <text x="395" y="645" class="item-text-sm" text-anchor="middle">Sit-to-stand transfer</text>
  
  <rect x="520" y="550" width="210" height="120" rx="8" fill="#fffbf0" stroke="#fa709a" stroke-width="1.5"/>
  <text x="625" y="575" font-size="13" font-weight="bold" fill="#d63384" text-anchor="middle">Cognitive</text>
  <line x1="540" y1="585" x2="710" y2="585" stroke="#fa709a" stroke-width="0.5"/>
  <text x="625" y="605" class="item-text-sm" text-anchor="middle">Memory training</text>
  <text x="625" y="625" class="item-text-sm" text-anchor="middle">Social interaction</text>
  <text x="625" y="645" class="item-text-sm" text-anchor="middle">Attention &amp; exec. function</text>
  
  <rect x="750" y="550" width="210" height="120" rx="8" fill="#fffbf0" stroke="#fa709a" stroke-width="1.5"/>
  <text x="855" y="575" font-size="13" font-weight="bold" fill="#d63384" text-anchor="middle">Neurological</text>
  <line x1="770" y1="585" x2="940" y2="585" stroke="#fa709a" stroke-width="0.5"/>
  <text x="855" y="605" class="item-text-sm" text-anchor="middle">Stroke recovery</text>
  <text x="855" y="625" class="item-text-sm" text-anchor="middle">Spinal cord injury</text>
  <text x="855" y="645" class="item-text-sm" text-anchor="middle">TBI &amp; Parkinson's</text>
  
  <!-- Connectors to applications -->
  <line x1="200" y1="450" x2="165" y2="550" class="connector" stroke-dasharray="4,3"/>
  <line x1="600" y1="450" x2="395" y2="550" class="connector" stroke-dasharray="4,3"/>
  <line x1="600" y1="450" x2="625" y2="550" class="connector" stroke-dasharray="4,3"/>
  <line x1="1000" y1="450" x2="855" y2="550" class="connector" stroke-dasharray="4,3"/>
  
  <!-- Legend/Note -->
  <text x="600" y="720" font-size="11" fill="#6a6a8a" text-anchor="middle" font-style="italic">
    Note: Many systems span multiple categories (e.g., wearable therapeutic exoskeletons for gait training)
  </text>
  <text x="600" y="755" font-size="12" fill="#4a4a6a" text-anchor="middle">
    Figure 1. Classification and taxonomy of rehabilitation robots organized by function, structure, and deployment setting.
  </text>
</svg>'''
    
    with open(os.path.join(OUTPUT_DIR, "Figure_1_Classification_Taxonomy.svg"), "w") as f:
        f.write(svg)
    print("Figure 1 generated: Classification and Taxonomy")



def generate_figure_2():
    """Figure 2: Historical Timeline of Rehabilitation Robotics Development"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" width="1200" height="750">
  <defs>
    <style>
      .title { font: bold 22px 'Arial', sans-serif; fill: #1a1a2e; }
      .subtitle { font: 14px 'Arial', sans-serif; fill: #4a4a6a; }
      .era-label { font: bold 15px 'Arial', sans-serif; fill: #ffffff; }
      .year-label { font: bold 13px 'Arial', sans-serif; fill: #333; }
      .event-text { font: 12px 'Arial', sans-serif; fill: #2d2d44; }
      .milestone { font: bold 12px 'Arial', sans-serif; fill: #1a1a2e; }
    </style>
    <linearGradient id="tl1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#ffa07a;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="tl2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#4ecdc4;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#44bba4;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="tl3" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="tl4" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#f093fb;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#f5576c;stop-opacity:1"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="1200" height="750" fill="#fafbff" rx="8"/>
  <rect x="20" y="20" width="1160" height="710" fill="white" rx="6" stroke="#e8e8f0" stroke-width="1"/>
  
  <!-- Title -->
  <text x="600" y="55" class="title" text-anchor="middle">Historical Timeline of Rehabilitation Robotics Development</text>
  <text x="600" y="78" class="subtitle" text-anchor="middle">Key milestones, systems, and paradigm shifts from 1960s to present</text>
  
  <!-- Main timeline arrow -->
  <rect x="80" y="365" width="1040" height="6" rx="3" fill="#ddd"/>
  <polygon points="1120,368 1130,362 1130,374" fill="#888"/>
  

  <!-- Era 1: 1960s-1990s -->
  <rect x="80" y="100" width="260" height="35" rx="17" fill="url(#tl1)"/>
  <text x="210" y="123" class="era-label" text-anchor="middle">ERA 1: Foundations (1960s-1990s)</text>
  
  <!-- Era 1 milestones -->
  <circle cx="130" cy="368" r="8" fill="#ff6b6b" stroke="white" stroke-width="2"/>
  <line x1="130" y1="360" x2="130" y2="150" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="3,2"/>
  <rect x="80" y="150" width="180" height="65" rx="6" fill="#fff5f5" stroke="#ff6b6b" stroke-width="1"/>
  <text x="170" y="170" class="year-label" text-anchor="middle">1963</text>
  <text x="170" y="187" class="event-text" text-anchor="middle">Rancho Arm developed</text>
  <text x="170" y="203" class="event-text" text-anchor="middle">First powered orthosis</text>
  
  <circle cx="220" cy="368" r="8" fill="#ff6b6b" stroke="white" stroke-width="2"/>
  <line x1="220" y1="376" x2="220" y2="420" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="3,2"/>
  <rect x="145" y="420" width="180" height="65" rx="6" fill="#fff5f5" stroke="#ff6b6b" stroke-width="1"/>
  <text x="235" y="440" class="year-label" text-anchor="middle">1970s</text>
  <text x="235" y="457" class="event-text" text-anchor="middle">CPM machines &amp; FES</text>
  <text x="235" y="473" class="event-text" text-anchor="middle">Electromechanical devices</text>
  
  <circle cx="310" cy="368" r="10" fill="#ff6b6b" stroke="#ff4444" stroke-width="2"/>
  <line x1="310" y1="360" x2="310" y2="240" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="3,2"/>
  <rect x="240" y="235" width="200" height="80" rx="6" fill="#fff0f0" stroke="#ff4444" stroke-width="1.5"/>
  <text x="340" y="257" class="year-label" text-anchor="middle">1991 ★</text>
  <text x="340" y="275" class="milestone" text-anchor="middle">MIT-Manus developed</text>
  <text x="340" y="292" class="event-text" text-anchor="middle">Paradigm shift: assistive</text>
  <text x="340" y="307" class="event-text" text-anchor="middle">→ therapeutic robotics</text>
  
  <!-- Era 2: 2000s -->
  <rect x="400" y="100" width="260" height="35" rx="17" fill="url(#tl2)"/>
  <text x="530" y="123" class="era-label" text-anchor="middle">ERA 2: Expansion (2000s)</text>
  
  <circle cx="450" cy="368" r="8" fill="#4ecdc4" stroke="white" stroke-width="2"/>
  <line x1="450" y1="376" x2="450" y2="420" stroke="#4ecdc4" stroke-width="1.5" stroke-dasharray="3,2"/>
  <rect x="380" y="420" width="180" height="80" rx="6" fill="#f0fffd" stroke="#4ecdc4" stroke-width="1"/>
  <text x="470" y="440" class="year-label" text-anchor="middle">1998-2001</text>
  <text x="470" y="457" class="event-text" text-anchor="middle">Lokomat (gait training)</text>
  <text x="470" y="473" class="event-text" text-anchor="middle">ReWalk (overground)</text>
  <text x="470" y="489" class="event-text" text-anchor="middle">HAL (EMG-controlled)</text>
  
  <circle cx="560" cy="368" r="8" fill="#4ecdc4" stroke="white" stroke-width="2"/>
  <line x1="560" y1="360" x2="560" y2="150" stroke="#4ecdc4" stroke-width="1.5" stroke-dasharray="3,2"/>
  <rect x="480" y="150" width="195" height="80" rx="6" fill="#f0fffd" stroke="#4ecdc4" stroke-width="1"/>
  <text x="578" y="170" class="year-label" text-anchor="middle">2004-2008</text>
  <text x="578" y="187" class="event-text" text-anchor="middle">VR integration with robots</text>
  <text x="578" y="203" class="event-text" text-anchor="middle">Clinical trials (VA ROBOTICS)</text>
  <text x="578" y="219" class="event-text" text-anchor="middle">First commercial systems</text>
  

  <!-- Era 3: 2010s -->
  <rect x="700" y="100" width="260" height="35" rx="17" fill="url(#tl3)"/>
  <text x="830" y="123" class="era-label" text-anchor="middle">ERA 3: Intelligence (2010s)</text>
  
  <circle cx="740" cy="368" r="8" fill="#667eea" stroke="white" stroke-width="2"/>
  <line x1="740" y1="360" x2="740" y2="150" stroke="#667eea" stroke-width="1.5" stroke-dasharray="3,2"/>
  <rect x="680" y="150" width="185" height="80" rx="6" fill="#f5f3ff" stroke="#667eea" stroke-width="1"/>
  <text x="773" y="170" class="year-label" text-anchor="middle">2011-2014</text>
  <text x="773" y="187" class="event-text" text-anchor="middle">FDA-cleared exoskeletons</text>
  <text x="773" y="203" class="event-text" text-anchor="middle">Ekso, Indego, ReWalk</text>
  <text x="773" y="219" class="event-text" text-anchor="middle">Wearable rehabilitation</text>
  
  <circle cx="850" cy="368" r="8" fill="#667eea" stroke="white" stroke-width="2"/>
  <line x1="850" y1="376" x2="850" y2="420" stroke="#667eea" stroke-width="1.5" stroke-dasharray="3,2"/>
  <rect x="775" y="420" width="185" height="80" rx="6" fill="#f5f3ff" stroke="#667eea" stroke-width="1"/>
  <text x="868" y="440" class="year-label" text-anchor="middle">2015-2018</text>
  <text x="868" y="457" class="event-text" text-anchor="middle">Soft exosuits (Harvard)</text>
  <text x="868" y="473" class="event-text" text-anchor="middle">Machine learning control</text>
  <text x="868" y="489" class="event-text" text-anchor="middle">BCI-robot integration</text>
  
  <!-- Era 4: 2020s-Present -->
  <rect x="990" y="100" width="140" height="35" rx="17" fill="url(#tl4)"/>
  <text x="1060" y="123" class="era-label" text-anchor="middle">ERA 4: AI (2020s+)</text>
  
  <circle cx="1050" cy="368" r="10" fill="#f093fb" stroke="#f5576c" stroke-width="2"/>
  <line x1="1050" y1="360" x2="1050" y2="150" stroke="#f093fb" stroke-width="1.5" stroke-dasharray="3,2"/>
  <rect x="970" y="150" width="185" height="95" rx="6" fill="#fef5ff" stroke="#f093fb" stroke-width="1.5"/>
  <text x="1063" y="170" class="year-label" text-anchor="middle">2020-Present ★</text>
  <text x="1063" y="188" class="milestone" text-anchor="middle">AI-driven rehabilitation</text>
  <text x="1063" y="205" class="event-text" text-anchor="middle">Tele-rehabilitation boom</text>
  <text x="1063" y="222" class="event-text" text-anchor="middle">Cloud-connected systems</text>
  <text x="1063" y="239" class="event-text" text-anchor="middle">Digital twins &amp; VR/AR</text>
  
  <!-- Technology Progression Bar -->
  <text x="600" y="570" font-size="14" font-weight="bold" fill="#333" text-anchor="middle">Technology Progression</text>
  
  <rect x="100" y="585" width="200" height="25" rx="5" fill="#ffe0e0"/>
  <text x="200" y="603" font-size="11" fill="#cc3333" text-anchor="middle">Rigid Mechanisms</text>
  
  <rect x="320" y="585" width="200" height="25" rx="5" fill="#e0fff8"/>
  <text x="420" y="603" font-size="11" fill="#2d8a7a" text-anchor="middle">Sensors + VR Integration</text>
  
  <rect x="540" y="585" width="200" height="25" rx="5" fill="#e8e0ff"/>
  <text x="640" y="603" font-size="11" fill="#5533aa" text-anchor="middle">ML + Soft Robotics</text>
  
  <rect x="760" y="585" width="220" height="25" rx="5" fill="#ffe0f5"/>
  <text x="870" y="603" font-size="11" fill="#aa3377" text-anchor="middle">AI + BCI + Cloud + Digital Twin</text>
  
  <!-- Arrows between progression -->
  <polygon points="305,597 315,592 315,603" fill="#999"/>
  <polygon points="525,597 535,592 535,603" fill="#999"/>
  <polygon points="745,597 755,592 755,603" fill="#999"/>
  
  <!-- Key metrics -->
  <text x="600" y="650" font-size="13" fill="#555" text-anchor="middle">
    Global installations: ~50 (1990s) → ~5,000 (2010s) → ~25,000+ (2020s)
  </text>
  
  <!-- Caption -->
  <text x="600" y="700" font-size="12" fill="#4a4a6a" text-anchor="middle">
    Figure 2. Historical timeline of rehabilitation robotics development showing key milestones,
  </text>
  <text x="600" y="718" font-size="12" fill="#4a4a6a" text-anchor="middle">
    systems, and the evolution of underlying technologies from the 1960s to present.
  </text>
</svg>'''
    
    with open(os.path.join(OUTPUT_DIR, "Figure_2_Historical_Timeline.svg"), "w") as f:
        f.write(svg)
    print("Figure 2 generated: Historical Timeline")



def generate_figure_3():
    """Figure 3: Technology Architecture of Modern Rehabilitation Robot Systems"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 850" width="1200" height="850">
  <defs>
    <style>
      .title { font: bold 22px 'Arial', sans-serif; fill: #1a1a2e; }
      .subtitle { font: 14px 'Arial', sans-serif; fill: #4a4a6a; }
      .layer-title { font: bold 15px 'Arial', sans-serif; fill: #ffffff; }
      .comp-title { font: bold 12px 'Arial', sans-serif; fill: #1a1a2e; }
      .comp-text { font: 11px 'Arial', sans-serif; fill: #4a4a6a; }
      .arrow-text { font: italic 10px 'Arial', sans-serif; fill: #6a6a8a; }
    </style>
  </defs>
  
  <!-- Background -->
  <rect width="1200" height="850" fill="#fafbff" rx="8"/>
  <rect x="20" y="20" width="1160" height="810" fill="white" rx="6" stroke="#e8e8f0" stroke-width="1"/>
  
  <!-- Title -->
  <text x="600" y="55" class="title" text-anchor="middle">Technology Architecture of Modern Rehabilitation Robot Systems</text>
  <text x="600" y="78" class="subtitle" text-anchor="middle">Multi-layered system architecture integrating hardware, software, AI, and clinical components</text>
  
  <!-- Layer 1: Physical/Hardware Layer -->
  <rect x="60" y="100" width="1080" height="140" rx="8" fill="#fff0f0" stroke="#e74c3c" stroke-width="2"/>
  <rect x="60" y="100" width="1080" height="32" rx="8" fill="#e74c3c"/>
  <rect x="60" y="120" width="1080" height="12" fill="#e74c3c"/>
  <text x="600" y="120" class="layer-title" text-anchor="middle">LAYER 1: PHYSICAL HARDWARE &amp; ACTUATION</text>
  
  <!-- Hardware components -->
  <rect x="85" y="145" width="165" height="80" rx="6" fill="white" stroke="#e74c3c" stroke-width="1"/>
  <text x="168" y="165" class="comp-title" text-anchor="middle">Actuators</text>
  <text x="168" y="182" class="comp-text" text-anchor="middle">Electric motors (DC/BLDC)</text>
  <text x="168" y="197" class="comp-text" text-anchor="middle">Series elastic actuators</text>
  <text x="168" y="212" class="comp-text" text-anchor="middle">Pneumatic/hydraulic</text>
  
  <rect x="270" y="145" width="165" height="80" rx="6" fill="white" stroke="#e74c3c" stroke-width="1"/>
  <text x="353" y="165" class="comp-title" text-anchor="middle">Sensors</text>
  <text x="353" y="182" class="comp-text" text-anchor="middle">Force/torque sensors</text>
  <text x="353" y="197" class="comp-text" text-anchor="middle">IMUs, encoders</text>
  <text x="353" y="212" class="comp-text" text-anchor="middle">EMG/EEG electrodes</text>
  
  <rect x="455" y="145" width="165" height="80" rx="6" fill="white" stroke="#e74c3c" stroke-width="1"/>
  <text x="538" y="165" class="comp-title" text-anchor="middle">Mechanical Structure</text>
  <text x="538" y="182" class="comp-text" text-anchor="middle">Rigid/soft exoskeleton</text>
  <text x="538" y="197" class="comp-text" text-anchor="middle">End-effector linkage</text>
  <text x="538" y="212" class="comp-text" text-anchor="middle">Body weight support</text>
  
  <rect x="640" y="145" width="165" height="80" rx="6" fill="white" stroke="#e74c3c" stroke-width="1"/>
  <text x="723" y="165" class="comp-title" text-anchor="middle">Safety Systems</text>
  <text x="723" y="182" class="comp-text" text-anchor="middle">Emergency stops</text>
  <text x="723" y="197" class="comp-text" text-anchor="middle">Force limiters</text>
  <text x="723" y="212" class="comp-text" text-anchor="middle">Mechanical compliance</text>
  
  <rect x="825" y="145" width="165" height="80" rx="6" fill="white" stroke="#e74c3c" stroke-width="1"/>
  <text x="908" y="165" class="comp-title" text-anchor="middle">Power &amp; Electronics</text>
  <text x="908" y="182" class="comp-text" text-anchor="middle">Motor drivers</text>
  <text x="908" y="197" class="comp-text" text-anchor="middle">Signal conditioning</text>
  <text x="908" y="212" class="comp-text" text-anchor="middle">Battery/power supply</text>
  
  <!-- Arrow between layers -->
  <polygon points="580,245 600,260 620,245" fill="#aaa"/>
  <polygon points="580,260 600,245 620,260" fill="#aaa"/>
  <text x="650" y="255" class="arrow-text">Bidirectional data flow</text>
  

  <!-- Layer 2: Control & Signal Processing -->
  <rect x="60" y="270" width="1080" height="140" rx="8" fill="#f0f5ff" stroke="#3498db" stroke-width="2"/>
  <rect x="60" y="270" width="1080" height="32" rx="8" fill="#3498db"/>
  <rect x="60" y="290" width="1080" height="12" fill="#3498db"/>
  <text x="600" y="290" class="layer-title" text-anchor="middle">LAYER 2: CONTROL &amp; SIGNAL PROCESSING</text>
  
  <rect x="85" y="315" width="200" height="80" rx="6" fill="white" stroke="#3498db" stroke-width="1"/>
  <text x="185" y="335" class="comp-title" text-anchor="middle">Motion Control</text>
  <text x="185" y="352" class="comp-text" text-anchor="middle">Impedance/admittance control</text>
  <text x="185" y="367" class="comp-text" text-anchor="middle">Position/force control</text>
  <text x="185" y="382" class="comp-text" text-anchor="middle">Assist-as-needed algorithms</text>
  
  <rect x="310" y="315" width="200" height="80" rx="6" fill="white" stroke="#3498db" stroke-width="1"/>
  <text x="410" y="335" class="comp-title" text-anchor="middle">Signal Processing</text>
  <text x="410" y="352" class="comp-text" text-anchor="middle">EMG/EEG decoding</text>
  <text x="410" y="367" class="comp-text" text-anchor="middle">Motion intention detection</text>
  <text x="410" y="382" class="comp-text" text-anchor="middle">Real-time filtering</text>
  
  <rect x="535" y="315" width="200" height="80" rx="6" fill="white" stroke="#3498db" stroke-width="1"/>
  <text x="635" y="335" class="comp-title" text-anchor="middle">Adaptive Algorithms</text>
  <text x="635" y="352" class="comp-text" text-anchor="middle">Model-predictive control</text>
  <text x="635" y="367" class="comp-text" text-anchor="middle">Variable impedance</text>
  <text x="635" y="382" class="comp-text" text-anchor="middle">Performance-based tuning</text>
  
  <rect x="760" y="315" width="200" height="80" rx="6" fill="white" stroke="#3498db" stroke-width="1"/>
  <text x="860" y="335" class="comp-title" text-anchor="middle">Safety Monitoring</text>
  <text x="860" y="352" class="comp-text" text-anchor="middle">Real-time limit checking</text>
  <text x="860" y="367" class="comp-text" text-anchor="middle">Collision detection</text>
  <text x="860" y="382" class="comp-text" text-anchor="middle">Patient state estimation</text>
  
  <!-- Arrow between layers -->
  <polygon points="580,415 600,430 620,415" fill="#aaa"/>
  <polygon points="580,430 600,415 620,430" fill="#aaa"/>
  <text x="650" y="425" class="arrow-text">Intelligence integration</text>
  
  <!-- Layer 3: AI & Intelligence -->
  <rect x="60" y="440" width="1080" height="140" rx="8" fill="#f5f0ff" stroke="#9b59b6" stroke-width="2"/>
  <rect x="60" y="440" width="1080" height="32" rx="8" fill="#9b59b6"/>
  <rect x="60" y="460" width="1080" height="12" fill="#9b59b6"/>
  <text x="600" y="460" class="layer-title" text-anchor="middle">LAYER 3: ARTIFICIAL INTELLIGENCE &amp; MACHINE LEARNING</text>
  
  <rect x="85" y="485" width="200" height="80" rx="6" fill="white" stroke="#9b59b6" stroke-width="1"/>
  <text x="185" y="505" class="comp-title" text-anchor="middle">Patient Modeling</text>
  <text x="185" y="522" class="comp-text" text-anchor="middle">Recovery trajectory prediction</text>
  <text x="185" y="537" class="comp-text" text-anchor="middle">Impairment classification</text>
  <text x="185" y="552" class="comp-text" text-anchor="middle">Outcome prediction</text>
  
  <rect x="310" y="485" width="200" height="80" rx="6" fill="white" stroke="#9b59b6" stroke-width="1"/>
  <text x="410" y="505" class="comp-title" text-anchor="middle">Therapy Optimization</text>
  <text x="410" y="522" class="comp-text" text-anchor="middle">Reinforcement learning</text>
  <text x="410" y="537" class="comp-text" text-anchor="middle">Parameter adaptation</text>
  <text x="410" y="552" class="comp-text" text-anchor="middle">Personalized protocols</text>
  
  <rect x="535" y="485" width="200" height="80" rx="6" fill="white" stroke="#9b59b6" stroke-width="1"/>
  <text x="635" y="505" class="comp-title" text-anchor="middle">Natural Interaction</text>
  <text x="635" y="522" class="comp-text" text-anchor="middle">Speech/language processing</text>
  <text x="635" y="537" class="comp-text" text-anchor="middle">Emotion recognition</text>
  <text x="635" y="552" class="comp-text" text-anchor="middle">Motivation strategies</text>
  
  <rect x="760" y="485" width="200" height="80" rx="6" fill="white" stroke="#9b59b6" stroke-width="1"/>
  <text x="860" y="505" class="comp-title" text-anchor="middle">Data Analytics</text>
  <text x="860" y="522" class="comp-text" text-anchor="middle">Progress visualization</text>
  <text x="860" y="537" class="comp-text" text-anchor="middle">Pattern recognition</text>
  <text x="860" y="552" class="comp-text" text-anchor="middle">Clinical decision support</text>
  

  <!-- Arrow between layers -->
  <polygon points="580,585 600,600 620,585" fill="#aaa"/>
  <polygon points="580,600 600,585 620,600" fill="#aaa"/>
  <text x="650" y="595" class="arrow-text">Clinical workflow</text>
  
  <!-- Layer 4: Clinical Interface & Connectivity -->
  <rect x="60" y="610" width="1080" height="140" rx="8" fill="#f0fff5" stroke="#27ae60" stroke-width="2"/>
  <rect x="60" y="610" width="1080" height="32" rx="8" fill="#27ae60"/>
  <rect x="60" y="630" width="1080" height="12" fill="#27ae60"/>
  <text x="600" y="630" class="layer-title" text-anchor="middle">LAYER 4: CLINICAL INTERFACE &amp; CONNECTIVITY</text>
  
  <rect x="85" y="655" width="200" height="80" rx="6" fill="white" stroke="#27ae60" stroke-width="1"/>
  <text x="185" y="675" class="comp-title" text-anchor="middle">Therapist Interface</text>
  <text x="185" y="692" class="comp-text" text-anchor="middle">Therapy configuration</text>
  <text x="185" y="707" class="comp-text" text-anchor="middle">Progress dashboards</text>
  <text x="185" y="722" class="comp-text" text-anchor="middle">Remote monitoring</text>
  
  <rect x="310" y="655" width="200" height="80" rx="6" fill="white" stroke="#27ae60" stroke-width="1"/>
  <text x="410" y="675" class="comp-title" text-anchor="middle">Patient Experience</text>
  <text x="410" y="692" class="comp-text" text-anchor="middle">VR/AR environments</text>
  <text x="410" y="707" class="comp-text" text-anchor="middle">Gamification &amp; feedback</text>
  <text x="410" y="722" class="comp-text" text-anchor="middle">Goal tracking</text>
  
  <rect x="535" y="655" width="200" height="80" rx="6" fill="white" stroke="#27ae60" stroke-width="1"/>
  <text x="635" y="675" class="comp-title" text-anchor="middle">Cloud &amp; IoT</text>
  <text x="635" y="692" class="comp-text" text-anchor="middle">Data aggregation</text>
  <text x="635" y="707" class="comp-text" text-anchor="middle">Tele-rehabilitation</text>
  <text x="635" y="722" class="comp-text" text-anchor="middle">Multi-site analytics</text>
  
  <rect x="760" y="655" width="200" height="80" rx="6" fill="white" stroke="#27ae60" stroke-width="1"/>
  <text x="860" y="675" class="comp-title" text-anchor="middle">Integration</text>
  <text x="860" y="692" class="comp-text" text-anchor="middle">EHR connectivity</text>
  <text x="860" y="707" class="comp-text" text-anchor="middle">Outcome reporting</text>
  <text x="860" y="722" class="comp-text" text-anchor="middle">Regulatory compliance</text>
  
  <!-- Right side: Cross-cutting concerns -->
  <rect x="1000" y="115" width="125" height="620" rx="6" fill="#fff8e0" stroke="#f39c12" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="1063" y="390" font-size="13" font-weight="bold" fill="#d68910" text-anchor="middle" transform="rotate(-90, 1063, 390)">CROSS-CUTTING: Safety • Ethics • Standards • Regulation</text>

  <!-- Caption -->
  <text x="600" y="790" font-size="12" fill="#4a4a6a" text-anchor="middle">
    Figure 3. Multi-layered technology architecture of modern rehabilitation robot systems showing the integration
  </text>
  <text x="600" y="808" font-size="12" fill="#4a4a6a" text-anchor="middle">
    of physical hardware, control systems, artificial intelligence, and clinical interface layers.
  </text>
</svg>'''
    
    with open(os.path.join(OUTPUT_DIR, "Figure_3_Technology_Architecture.svg"), "w") as f:
        f.write(svg)
    print("Figure 3 generated: Technology Architecture")



def generate_figure_4():
    """Figure 4: Future Directions and Convergent Technologies in Rehabilitation Robotics"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">
  <defs>
    <style>
      .title { font: bold 22px 'Arial', sans-serif; fill: #1a1a2e; }
      .subtitle { font: 14px 'Arial', sans-serif; fill: #4a4a6a; }
      .center-title { font: bold 16px 'Arial', sans-serif; fill: #ffffff; }
      .spoke-title { font: bold 14px 'Arial', sans-serif; fill: #1a1a2e; }
      .spoke-text { font: 11px 'Arial', sans-serif; fill: #4a4a6a; }
      .impact-text { font: bold 11px 'Arial', sans-serif; fill: #2d8a4e; }
    </style>
    <radialGradient id="rg1" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1"/>
    </radialGradient>
  </defs>
  
  <!-- Background -->
  <rect width="1200" height="800" fill="#fafbff" rx="8"/>
  <rect x="20" y="20" width="1160" height="760" fill="white" rx="6" stroke="#e8e8f0" stroke-width="1"/>
  
  <!-- Title -->
  <text x="600" y="55" class="title" text-anchor="middle">Future Directions and Convergent Technologies</text>
  <text x="600" y="78" class="subtitle" text-anchor="middle">Emerging technologies converging toward next-generation rehabilitation robotics</text>
  
  <!-- Central hub -->
  <circle cx="600" cy="380" r="75" fill="url(#rg1)" stroke="#4a3f9f" stroke-width="2"/>
  <text x="600" y="370" class="center-title" text-anchor="middle">NEXT-GEN</text>
  <text x="600" y="392" class="center-title" text-anchor="middle">REHABILITATION</text>
  <text x="600" y="414" font-size="12" fill="#ddd" text-anchor="middle">ROBOTICS</text>
  
  <!-- Spoke connectors -->
  <line x1="535" y1="340" x2="340" y2="200" stroke="#667eea" stroke-width="2" opacity="0.6"/>
  <line x1="665" y1="340" x2="860" y2="200" stroke="#e74c3c" stroke-width="2" opacity="0.6"/>
  <line x1="525" y1="380" x2="220" y2="400" stroke="#3498db" stroke-width="2" opacity="0.6"/>
  <line x1="675" y1="380" x2="980" y2="400" stroke="#27ae60" stroke-width="2" opacity="0.6"/>
  <line x1="535" y1="430" x2="320" y2="590" stroke="#f39c12" stroke-width="2" opacity="0.6"/>
  <line x1="665" y1="430" x2="880" y2="590" stroke="#9b59b6" stroke-width="2" opacity="0.6"/>
  

  <!-- Spoke 1: Brain-Computer Interfaces (top-left) -->
  <rect x="180" y="130" width="240" height="130" rx="10" fill="#f5f3ff" stroke="#667eea" stroke-width="2"/>
  <circle cx="210" cy="155" r="15" fill="#667eea"/>
  <text x="210" y="160" font-size="14" fill="white" text-anchor="middle">1</text>
  <text x="320" y="158" class="spoke-title" text-anchor="middle">Brain-Computer Interfaces</text>
  <line x1="200" y1="170" x2="400" y2="170" stroke="#667eea" stroke-width="0.5"/>
  <text x="300" y="190" class="spoke-text" text-anchor="middle">• EEG-based motor imagery decoding</text>
  <text x="300" y="207" class="spoke-text" text-anchor="middle">• Invasive neural interfaces</text>
  <text x="300" y="224" class="spoke-text" text-anchor="middle">• Closed-loop neuromodulation</text>
  <text x="300" y="245" class="impact-text" text-anchor="middle">→ Direct neural control of robots</text>
  
  <!-- Spoke 2: Artificial Intelligence (top-right) -->
  <rect x="780" y="130" width="240" height="130" rx="10" fill="#fff0f0" stroke="#e74c3c" stroke-width="2"/>
  <circle cx="810" cy="155" r="15" fill="#e74c3c"/>
  <text x="810" y="160" font-size="14" fill="white" text-anchor="middle">2</text>
  <text x="920" y="158" class="spoke-title" text-anchor="middle">Artificial Intelligence</text>
  <line x1="800" y1="170" x2="1000" y2="170" stroke="#e74c3c" stroke-width="0.5"/>
  <text x="900" y="190" class="spoke-text" text-anchor="middle">• Deep reinforcement learning</text>
  <text x="900" y="207" class="spoke-text" text-anchor="middle">• Foundation models for rehab</text>
  <text x="900" y="224" class="spoke-text" text-anchor="middle">• Predictive outcome modeling</text>
  <text x="900" y="245" class="impact-text" text-anchor="middle">→ Autonomous therapy delivery</text>
  
  <!-- Spoke 3: Soft Robotics (middle-left) -->
  <rect x="60" y="340" width="240" height="130" rx="10" fill="#f0f5ff" stroke="#3498db" stroke-width="2"/>
  <circle cx="90" cy="365" r="15" fill="#3498db"/>
  <text x="90" y="370" font-size="14" fill="white" text-anchor="middle">3</text>
  <text x="200" y="368" class="spoke-title" text-anchor="middle">Soft Robotics</text>
  <line x1="80" y1="380" x2="280" y2="380" stroke="#3498db" stroke-width="0.5"/>
  <text x="180" y="400" class="spoke-text" text-anchor="middle">• Pneumatic soft actuators</text>
  <text x="180" y="417" class="spoke-text" text-anchor="middle">• Cable-driven exosuits</text>
  <text x="180" y="434" class="spoke-text" text-anchor="middle">• Bio-inspired compliance</text>
  <text x="180" y="455" class="impact-text" text-anchor="middle">→ Wearable daily-use therapy</text>
  
  <!-- Spoke 4: Digital Twins & VR/AR (middle-right) -->
  <rect x="900" y="340" width="240" height="130" rx="10" fill="#f0fff5" stroke="#27ae60" stroke-width="2"/>
  <circle cx="930" cy="365" r="15" fill="#27ae60"/>
  <text x="930" y="370" font-size="14" fill="white" text-anchor="middle">4</text>
  <text x="1040" y="368" class="spoke-title" text-anchor="middle">Digital Twins &amp; VR/AR</text>
  <line x1="920" y1="380" x2="1120" y2="380" stroke="#27ae60" stroke-width="0.5"/>
  <text x="1020" y="400" class="spoke-text" text-anchor="middle">• Patient digital models</text>
  <text x="1020" y="417" class="spoke-text" text-anchor="middle">• Immersive therapy environments</text>
  <text x="1020" y="434" class="spoke-text" text-anchor="middle">• Augmented reality guidance</text>
  <text x="1020" y="455" class="impact-text" text-anchor="middle">→ Simulation-optimized therapy</text>
  

  <!-- Spoke 5: Cloud & Tele-Rehabilitation (bottom-left) -->
  <rect x="160" y="540" width="240" height="130" rx="10" fill="#fffaf0" stroke="#f39c12" stroke-width="2"/>
  <circle cx="190" cy="565" r="15" fill="#f39c12"/>
  <text x="190" y="570" font-size="14" fill="white" text-anchor="middle">5</text>
  <text x="300" y="568" class="spoke-title" text-anchor="middle">Cloud &amp; Tele-Rehabilitation</text>
  <line x1="180" y1="580" x2="380" y2="580" stroke="#f39c12" stroke-width="0.5"/>
  <text x="280" y="600" class="spoke-text" text-anchor="middle">• Remote therapy supervision</text>
  <text x="280" y="617" class="spoke-text" text-anchor="middle">• IoT health monitoring</text>
  <text x="280" y="634" class="spoke-text" text-anchor="middle">• Federated data platforms</text>
  <text x="280" y="655" class="impact-text" text-anchor="middle">→ Global access &amp; equity</text>
  
  <!-- Spoke 6: Precision Rehabilitation (bottom-right) -->
  <rect x="760" y="540" width="240" height="130" rx="10" fill="#fef5ff" stroke="#9b59b6" stroke-width="2"/>
  <circle cx="790" cy="565" r="15" fill="#9b59b6"/>
  <text x="790" y="570" font-size="14" fill="white" text-anchor="middle">6</text>
  <text x="900" y="568" class="spoke-title" text-anchor="middle">Precision Rehabilitation</text>
  <line x1="780" y1="580" x2="980" y2="580" stroke="#9b59b6" stroke-width="0.5"/>
  <text x="880" y="600" class="spoke-text" text-anchor="middle">• Biomarker-driven therapy</text>
  <text x="880" y="617" class="spoke-text" text-anchor="middle">• Genomic/neuroimaging data</text>
  <text x="880" y="634" class="spoke-text" text-anchor="middle">• Adaptive trajectories</text>
  <text x="880" y="655" class="impact-text" text-anchor="middle">→ Right therapy, right patient</text>
  
  <!-- Vision statement at bottom -->
  <rect x="250" y="700" width="700" height="40" rx="20" fill="#f0f0ff" stroke="#667eea" stroke-width="1"/>
  <text x="600" y="725" font-size="13" font-weight="bold" fill="#4a3f9f" text-anchor="middle">
    VISION: Ambient, personalized, AI-driven rehabilitation integrated into daily life
  </text>
  
  <!-- Caption -->
  <text x="600" y="770" font-size="12" fill="#4a4a6a" text-anchor="middle">
    Figure 4. Future directions showing six convergent technologies driving next-generation rehabilitation robotics.
  </text>
</svg>'''
    
    with open(os.path.join(OUTPUT_DIR, "Figure_4_Future_Directions.svg"), "w") as f:
        f.write(svg)
    print("Figure 4 generated: Future Directions")


# Generate all figures
if __name__ == "__main__":
    generate_figure_1()
    generate_figure_2()
    generate_figure_3()
    generate_figure_4()
    print("\nAll 4 figures generated successfully in:", OUTPUT_DIR)
