#!/usr/bin/env python3
"""
Figures for the chapter "Agentic AI and Autonomous Systems" (written as code).

    python3 generate_agentic_figures.py

Figure 1 - Evolutionary trajectory: rule-based -> ML -> generative -> agentic AI
Figure 2 - Reference architecture of an autonomous AI agent
Figure 3 - Layered interoperability framework for heterogeneous multi-agent systems
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
from svgfig import Figure, col  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agentic_figures')


def bullets(items, size=15, lh=1.65):
    return ('<div style="text-align:left;font-size:%spx;line-height:%s">' % (size, lh) +
            ''.join('<div>• %s</div>' % b for b in items) + '</div>')


def fig1():
    f = Figure(1500, 800, title='Evolution of Artificial Intelligence toward Agentic Systems',
               subtitle='From hand-coded rules to goal-directed agents that plan, use tools and act')
    stages = [
        ('Rule-Based<br>Expert Systems', '1970s – 1980s', 'blue',
         ['Hand-coded if–then rules', 'Symbolic inference engines', 'Narrow and brittle'], 'Reasoning'),
        ('Statistical<br>Machine Learning', '1990s – 2010s', 'teal',
         ['Patterns learned from data', 'Deep neural networks', 'Reactive prediction'], '+ Perception'),
        ('Generative AI &<br>Foundation Models', '2018 – 2022', 'violet',
         ['Large pre-trained models', 'Text, image and code generation', 'Mostly single-turn'], '+ Generation'),
        ('Agentic AI', '2023 – present', 'orange',
         ['Goal-directed planning', 'Memory and tool use', 'Multi-step autonomous action'], '+ Planning & Action'),
    ]
    ramp = f.lingrad('#DBEAFE', '#FED7AA', horizontal=True)
    f.polygon([(60, 640), (1440, 640), (1440, 200), (60, 520)], fill=ramp, opacity=0.6)
    bw, bh, gap, x0 = 300, 255, 50, 75
    tops = [330, 280, 230, 180]
    for i, (name, era, c, bl, cap) in enumerate(stages):
        x, y = x0 + i * (bw + gap), tops[i]
        f.card(x, y, bw, bh, name, bullets(bl), color=c, title_size=19, header_h=78, valign='top')
        f.pill(x + bw / 2, y + bh - 34, era, color=c, size=14)
        f.pill(x + bw / 2, y - 24, cap, color=c, size=14, solid=False)
        if i:
            f.arrow(x - gap + 8, y + bh / 2 + 45, x - 8, y + bh / 2 + 20, color=c, sw=5)
        f.text(x + bw / 2, 680, ['Level 1 · Assistive', 'Level 2 · Predictive', 'Level 3 · Generative',
                                 'Level 4 · Autonomous'][i], size=16, weight=700, color=col(c, 2))
    g = f.lingrad(col('blue'), col('orange'), horizontal=True)
    f.path('M90,715 L1395,715', stroke=None)
    f.rect(90, 707, 1300, 16, fill=g, rx=8, shadow='softshadow')
    f.polygon([(1385, 695), (1420, 715), (1385, 735)], fill=col('orange'))
    f.text(750, 752, 'Increasing autonomy, scope of action and need for governance', size=15.5,
           weight=700, color='#334155')
    f.footnote('Each stage subsumes the capabilities of the previous one; agentic systems add persistent goals, '
               'planning, memory and the ability to act on their environment.', y=785)
    f.save(os.path.join(OUT, 'Figure_1_Evolution_of_Agentic_AI.png'))


def fig2():
    f = Figure(1500, 1010, title='Reference Architecture of an Autonomous AI Agent',
               subtitle='Perception → memory-augmented reasoning → tool use → action, closed by environmental feedback')
    f.soft(30, 100, 1440, 860, None, color='sky', dash='12,8', shadow=False, rx=30)
    f.pill(215, 124, 'ENVIRONMENT  ·  digital and/or physical', color='sky', size=14)
    # agent boundary
    f.rect(290, 165, 920, 720, fill=f.lingrad('#FFFFFF', '#F5F3FF'), stroke=col('indigo'), sw=2.5, rx=28)
    f.pill(750, 165, 'AUTONOMOUS AGENT', color='indigo', size=15)
    # inputs / effects
    ins = [('User goals &amp; instructions', 'blue'), ('Sensors &amp; telemetry', 'cyan'),
           ('Data streams &amp; documents', 'teal'), ('Messages from other agents', 'violet')]
    outs = [('Digital systems &amp; APIs', 'orange'), ('Physical actuators &amp; robots', 'red'),
            ('Other agents', 'violet'), ('Humans (reports, requests)', 'pink')]
    f.text(155, 300, 'INPUTS', size=15, weight=800, color=col('blue', 2), spacing=2)
    f.text(1345, 300, 'EFFECTS', size=15, weight=800, color=col('orange', 2), spacing=2)
    for i, (s, c) in enumerate(ins):
        y = 320 + i * 95
        f.soft(55, y, 200, 70, s, color=c, size=14)
        f.arrow(257, y + 35, 320, 495, color=c, sw=2.2, dash='1,0')
    for i, (s, c) in enumerate(outs):
        y = 320 + i * 95
        f.soft(1245, y, 200, 70, s, color=c, size=14)
    # perception
    f.card(320, 410, 240, 170, 'PERCEPTION', 'Parse, ground and filter observations into a structured state',
           color='blue', title_size=17, body_size=14.5)
    # memory
    f.card(590, 205, 320, 130, 'MEMORY', 'Working context · episodic log · long-term vector store with retrieval',
           color='violet', title_size=17, body_size=14.5)
    # tools
    f.card(940, 410, 240, 170, 'TOOLS & APIs', 'Search, code execution, databases, enterprise systems, actuators',
           color='orange', title_size=17, body_size=14.5)
    # action
    f.card(590, 650, 320, 125, 'ACTION', 'Execute selected step and change the state of the environment',
           color='red', title_size=17, body_size=14.5)
    # core
    cx, cy = 750, 495
    f.circle(cx, cy, 128, fill=f.radgrad('#6EE7B7', '#047857'), shadow=True)
    f.circle(cx, cy, 108, fill='none', stroke='#FFFFFF', sw=2, opacity=0.7)
    f.html(cx - 105, cy - 90, 210, 180,
           '<div style="color:#fff"><div style="font-size:20px;font-weight:800">REASONING CORE</div>'
           '<div style="font-size:14.5px;margin-top:4px">LLM-based planner</div>'
           '<div style="font-size:13.5px;margin-top:8px">Reason → Plan → Act<br>→ Observe → Reflect</div></div>')
    # internal arrows
    f.arrow(562, 495, 618, 495, color='blue', sw=4, label='state', label_dy=-14)
    f.arrow(720, 337, 720, 368, color='violet', sw=4)
    f.arrow(780, 368, 780, 337, color='violet', sw=4)
    f.text(855, 360, 'read / write', size=13.5, weight=700, color=col('violet', 2))
    f.arrow(880, 470, 938, 470, color='orange', sw=4, label='invoke', label_dy=-14)
    f.arrow(938, 525, 880, 525, color='slate', sw=3, label='results', label_dy=26)
    f.arrow(750, 625, 750, 648, color='red', sw=4)
    # action -> effects
    f.path('M912,712 L1226,712', stroke='red', sw=3.2)
    f.path('M1226,355 L1226,712', stroke='red', sw=3.2)
    for i in range(4):
        f.arrow(1226, 355 + i * 95, 1241, 355 + i * 95, color='red', sw=3.2)
    f.circle(1226, 712, 5, fill=col('red'))
    # guardrails bar
    g = f.lingrad(col('amber'), col('rose'), horizontal=True)
    f.rect(320, 800, 860, 58, fill=g, rx=14, shadow='softshadow')
    f.html(320, 800, 860, 58, '🛡 &nbsp;Guardrails &amp; human oversight: permissions · policy checks · '
           'audit logging · escalation to a human', size=15.5, color='#FFFFFF', weight=700)
    # feedback loop
    f.path('M1345,705 C1345,935 1200,935 750,935 C300,935 155,935 155,705', stroke='emerald', sw=4,
           arrow=True, dash='12,7')
    f.pill(750, 935, 'Observation & feedback loop: outcomes become new inputs', color='emerald', size=14)
    f.save(os.path.join(OUT, 'Figure_2_Agent_Architecture.png'))


def fig3():
    f = Figure(1500, 1000, title='Layered Interoperability for Heterogeneous Multi-Agent Systems',
               subtitle='Agents built by different organisations on different models collaborate only if every layer aligns')
    layers = [
        ('Coordination & Policy', 'purple', 'Roles, norms, negotiation, task allocation, workflow orchestration',
         'contract-net · auctions · voting · shared plans'),
        ('Semantic', 'emerald', 'Shared ontologies, vocabularies and intent, so that messages mean the same thing',
         'ontologies · knowledge graphs · capability descriptions'),
        ('Message Format', 'orange', 'Communicative acts and structured, validated schemas',
         'request · inform · propose · JSON schema'),
        ('Transport', 'blue', 'Networks, protocols, addressing, security and delivery guarantees',
         'HTTP/gRPC · message queues · pub/sub · TLS'),
    ]
    top, lh, gap = 205, 122, 30
    ax, bx, sw_ = 70, 1150, 280
    f.tile(ax, 115, sw_, 70, '<b>Agent A</b><br><span style="font-size:13px">Organisation 1 · Model X</span>',
           color='indigo', size=17)
    f.tile(bx, 115, sw_, 70, '<b>Agent B</b><br><span style="font-size:13px">Organisation 2 · Model Y</span>',
           color='rose', size=17)
    f.text(750, 145, 'Peer protocols: each layer talks to its counterpart', size=17, weight=700, color='#334155')
    f.text(750, 172, 'and relies on the layer beneath it', size=15, color='#64748B', italic=True)
    for i, (name, c, desc, ex) in enumerate(layers):
        y = top + i * (lh + gap)
        for x in (ax, bx):
            f.tile(x, y, sw_, lh, '<div style="font-size:19px;font-weight:800">%s</div>'
                   '<div style="font-size:13px;font-weight:500;margin-top:6px;opacity:.95">Layer %d</div>'
                   % (name.replace('&', '&amp;'), 4 - i), color=c)
        f.soft(400, y + 10, 700, lh - 20,
               '<div style="font-size:15.5px;font-weight:700">%s</div>'
               '<div style="font-size:13.5px;font-weight:500;margin-top:8px;font-style:italic">e.g. %s</div>'
               % (desc, ex), color=c, shadow=False)
        f.arrow(ax + sw_ + 4, y + lh / 2, 398, y + lh / 2, color=c, sw=3, dash='8,6')
        f.arrow(1102, y + lh / 2, bx - 4, y + lh / 2, color=c, sw=3, dash='8,6')
        if i < 3:
            for x in (ax, bx):
                f.arrow(x + sw_ / 2, y + lh + 3, x + sw_ / 2, y + lh + gap - 3, color='slate', sw=3, both=True)
    yb = top + 4 * (lh + gap) - 4
    g = f.lingrad(col('blue'), col('cyan'), horizontal=True)
    f.rect(ax, yb, bx + sw_ - ax, 42, fill=g, rx=12, shadow='softshadow')
    f.text(750, yb + 27, 'Shared network infrastructure (physical exchange of bytes)', size=15.5, weight=700,
           color='#FFFFFF')
    f.soft(70, yb + 62, 1360, 92,
           '<div><b>Peer-to-peer alignment is required at every layer.</b> A message can be delivered '
           '(transport) and parsed (format) yet still be misunderstood (semantics) or conflict with the '
           'other agent\'s commitments (coordination), producing silent coordination failures.</div>',
           color='amber', size=15, weight=500, align='left')
    f.save(os.path.join(OUT, 'Figure_3_Interoperability_Framework.png'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    fig1()
    fig2()
    fig3()
