"""
Create AutoCAD DXF drawing reproducing the mechanical part from the reference image.

Features:
- Upper semicircular body with R96 outer arc
- Three Ø30 holes at 60° spacing on R64 radius
- Central Ø50 circle with R20 inner bore
- Lower extension with R36, R35, R54 arcs
- Four R9 holes (Ø18) in lower section
- Ø40 circle at bottom
- 60° TYP angular features
- R20 fillets
- Dimension annotations
- Centerlines
"""

import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
import math

# Create a new DXF document (R2010 format - widely compatible with AutoCAD)
doc = ezdxf.new('R2010')
doc.units = units.MM

# Setup layers
doc.layers.add('OUTLINE', color=7, lineweight=50)        # White/Black - main outline
doc.layers.add('HIDDEN', color=1, linetype='DASHED')      # Red - hidden lines
doc.layers.add('CENTER', color=2, linetype='CENTER')      # Yellow - centerlines
doc.layers.add('DIMENSION', color=3)                      # Green - dimensions
doc.layers.add('CONSTRUCTION', color=8)                   # Gray - construction
doc.layers.add('HATCH', color=4)                          # Cyan - hatch/fill areas

# Add linetypes
doc.linetypes.add('DASHED', pattern=[0.5, 0.25, -0.25])
doc.linetypes.add('CENTER', pattern=[1.25, 0.5, -0.25, 0.25, -0.25])

msp = doc.modelspace()

# ============================================================
# GEOMETRIC PARAMETERS (from the drawing, origin at center)
# ============================================================
# All dimensions in mm

# Main body
R96 = 96        # Outer arc radius of upper body
R64 = 64        # Radius to center of 3 bolt holes
R50_d = 50      # Diameter of holes on R64 → actually Ø30 holes
D30 = 30        # Diameter of 3 holes (Ø30)
R30 = D30 / 2   # Radius of 3 holes = 15

D50 = 50        # Central circle diameter
R50 = D50 / 2   # Central circle radius = 25

R20_bore = 20   # Central bore radius (R20)

# Lower body features
R36 = 36        # Arc radius for lower body transition
R35 = 35        # Arc radius in lower section
R54 = 54        # Arc radius for lower outer contour
R20_fillet = 20 # Fillet radius

D40 = 40        # Bottom circle diameter
R40 = D40 / 2   # Bottom circle radius = 20

R9 = 9          # Radius of 4 small holes (R9 - 4X)

# Positions
# Upper 3 holes at 60° spacing centered around top (90°, 150°, 30° from horizontal)
# Actually from the drawing: holes at 30°, 90°, 150° from horizontal (top half)
hole_angles_deg = [30, 90, 150]  # Degrees from positive X-axis

# Lower body center (below main center)
lower_center_y = -80  # 80mm dimension shown on drawing

# ============================================================
# DRAW CENTERLINES
# ============================================================
# Horizontal centerline
msp.add_line((-120, 0), (120, 0), dxfattribs={'layer': 'CENTER'})
# Vertical centerline
msp.add_line((0, 110), (0, -130), dxfattribs={'layer': 'CENTER'})

# 30° angle lines from center (for upper holes)
for angle in [30, 150]:
    rad = math.radians(angle)
    x = 80 * math.cos(rad)
    y = 80 * math.sin(rad)
    msp.add_line((-x, -y), (x, y), dxfattribs={'layer': 'CENTER'})

# 60° construction lines
for angle in [60, 120]:
    rad = math.radians(angle)
    x = 100 * math.cos(rad)
    y = 100 * math.sin(rad)
    msp.add_line((0, 0), (x, y), dxfattribs={'layer': 'CENTER'})

# ============================================================
# DRAW MAIN OUTLINE - UPPER BODY
# ============================================================

# Outer arc R96 (upper semicircle from about 15° to 165°)
# The upper body is a large arc
msp.add_arc(
    center=(0, 0),
    radius=R96,
    start_angle=20,
    end_angle=160,
    dxfattribs={'layer': 'OUTLINE'}
)

# ============================================================
# DRAW THREE Ø30 HOLES ON R64 RADIUS
# ============================================================
for angle_deg in hole_angles_deg:
    rad = math.radians(angle_deg)
    cx = R64 * math.cos(rad)
    cy = R64 * math.sin(rad)
    # Draw circle (Ø30 = R15)
    msp.add_circle(
        center=(cx, cy),
        radius=R30,
        dxfattribs={'layer': 'OUTLINE'}
    )
    # Small centerline cross
    msp.add_line((cx - 20, cy), (cx + 20, cy), dxfattribs={'layer': 'CENTER'})
    msp.add_line((cx, cy - 20), (cx, cy + 20), dxfattribs={'layer': 'CENTER'})

# ============================================================
# DRAW CENTRAL FEATURES
# ============================================================
# Central circle Ø50
msp.add_circle(
    center=(0, 0),
    radius=R50,
    dxfattribs={'layer': 'OUTLINE'}
)

# Central bore R20
msp.add_circle(
    center=(0, 0),
    radius=R20_bore,
    dxfattribs={'layer': 'OUTLINE'}
)

# ============================================================
# DRAW LOWER BODY EXTENSION
# ============================================================
# The lower body extends downward with a neck shape

# R36 arcs (transition from upper body to lower)
# Left side arc
msp.add_arc(
    center=(-16, -20),
    radius=R36,
    start_angle=250,
    end_angle=290,
    dxfattribs={'layer': 'OUTLINE'}
)

# Right side arc
msp.add_arc(
    center=(16, -20),
    radius=R36,
    start_angle=250,
    end_angle=290,
    dxfattribs={'layer': 'OUTLINE'}
)

# R20 fillet arcs connecting upper body to lower extension
# Left fillet
msp.add_arc(
    center=(-40, -10),
    radius=R20_fillet,
    start_angle=270,
    end_angle=340,
    dxfattribs={'layer': 'OUTLINE'}
)

# Right fillet
msp.add_arc(
    center=(40, -10),
    radius=R20_fillet,
    start_angle=200,
    end_angle=270,
    dxfattribs={'layer': 'OUTLINE'}
)

# Lower outer contour R54
msp.add_arc(
    center=(0, -45),
    radius=R54,
    start_angle=220,
    end_angle=320,
    dxfattribs={'layer': 'OUTLINE'}
)

# R35 arcs in lower section (inner contours)
msp.add_arc(
    center=(0, -50),
    radius=R35,
    start_angle=230,
    end_angle=310,
    dxfattribs={'layer': 'OUTLINE'}
)

# ============================================================
# DRAW LOWER FEATURES - FOUR R9 HOLES
# ============================================================
# 4 small holes (R9) arranged in pairs in the lower section
# Based on the drawing, they appear at approximately:
hole_positions_lower = [
    (-18, -50),   # Upper left
    (18, -50),    # Upper right
    (-18, -75),   # Lower left
    (18, -75),    # Lower right
]

for (hx, hy) in hole_positions_lower:
    msp.add_circle(
        center=(hx, hy),
        radius=R9,
        dxfattribs={'layer': 'OUTLINE'}
    )
    # Centerline cross for each hole
    msp.add_line((hx - 12, hy), (hx + 12, hy), dxfattribs={'layer': 'CENTER'})
    msp.add_line((hx, hy - 12), (hx, hy + 12), dxfattribs={'layer': 'CENTER'})

# ============================================================
# DRAW BOTTOM CIRCLE Ø40
# ============================================================
msp.add_circle(
    center=(0, -80),
    radius=R40,
    dxfattribs={'layer': 'OUTLINE'}
)
# Centerlines for bottom circle
msp.add_line((-25, -80), (25, -80), dxfattribs={'layer': 'CENTER'})
msp.add_line((0, -105), (0, -55), dxfattribs={'layer': 'CENTER'})

# ============================================================
# DRAW CONNECTING LINES (straight edges of the body)
# ============================================================
# Left side straight line connecting upper arc to lower section
left_upper_x = R96 * math.cos(math.radians(160))
left_upper_y = R96 * math.sin(math.radians(160))
msp.add_line(
    (left_upper_x, left_upper_y),
    (-45, -30),
    dxfattribs={'layer': 'OUTLINE'}
)

# Right side straight line
right_upper_x = R96 * math.cos(math.radians(20))
right_upper_y = R96 * math.sin(math.radians(20))
msp.add_line(
    (right_upper_x, right_upper_y),
    (45, -30),
    dxfattribs={'layer': 'OUTLINE'}
)

# Lower straight sides connecting to bottom
msp.add_line((-45, -30), (-40, -95), dxfattribs={'layer': 'OUTLINE'})
msp.add_line((45, -30), (40, -95), dxfattribs={'layer': 'OUTLINE'})

# Bottom arc connecting lower sides
msp.add_arc(
    center=(0, -85),
    radius=42,
    start_angle=200,
    end_angle=340,
    dxfattribs={'layer': 'OUTLINE'}
)

# ============================================================
# DRAW 60° ANGULAR FEATURES (V-notch at top)
# ============================================================
# 60° V-notch lines at top
notch_depth = 15
top_y = R96

# Left 60° line
angle_left = math.radians(120)
msp.add_line(
    (0, R96 + 5),
    (notch_depth * math.cos(angle_left), R96 + 5 + notch_depth * math.sin(angle_left)),
    dxfattribs={'layer': 'OUTLINE'}
)

# Right 60° line
angle_right = math.radians(60)
msp.add_line(
    (0, R96 + 5),
    (notch_depth * math.cos(angle_right), R96 + 5 + notch_depth * math.sin(angle_right)),
    dxfattribs={'layer': 'OUTLINE'}
)

# ============================================================
# ADD DIMENSIONS
# ============================================================
# Create a custom dimension style
doc.dimstyles.new('MECH', dxfattribs={
    'dimtxt': 3.5,        # Text height
    'dimasz': 2.5,        # Arrow size
    'dimexe': 1.5,        # Extension line extension
    'dimexo': 1.0,        # Extension line offset
    'dimgap': 1.0,        # Gap between dim line and text
    'dimtad': 1,          # Text above dimension line
    'dimdec': 0,          # Decimal places
})

# Add text annotations for dimensions (using MTEXT for flexibility)
dim_attribs = {'layer': 'DIMENSION', 'height': 3.5}

# Ø30 - 3X
msp.add_mtext(
    'Ø30 - 3X',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(45, 85))

# R96
msp.add_mtext(
    'R96',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(30, 70))

# R64
msp.add_mtext(
    'R64',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(55, 50))

# Ø50
msp.add_mtext(
    'Ø50',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(-75, 30))

# R20 (bore)
msp.add_mtext(
    'R20',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(-70, 0))

# R20 (fillet)
msp.add_mtext(
    'R20',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(50, -15))

# R36
msp.add_mtext(
    'R36',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(45, -40))

# R35
msp.add_mtext(
    'R35',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(40, -60))

# R54
msp.add_mtext(
    'R54',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(20, -100))

# Ø40
msp.add_mtext(
    'Ø40',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(35, -85))

# R9 - 4X
msp.add_mtext(
    'R9 - 4X',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(5, -110))

# 60° angle annotations
msp.add_mtext(
    '60°',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(-10, 100))

msp.add_mtext(
    '60°',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(25, 95))

# 30° angle
msp.add_mtext(
    '30°',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(75, 25))

# 60° TYP
msp.add_mtext(
    '60°\nTYP',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(-55, -35))

# 60° TYP lower
msp.add_mtext(
    '60° TYP',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(-55, -80))

# 80 dimension (vertical)
msp.add_mtext(
    '80',
    dxfattribs={'layer': 'DIMENSION', 'char_height': 3.0}
).set_location(insert=(85, -40))

# Dimension lines for 80mm
msp.add_line((80, 0), (90, 0), dxfattribs={'layer': 'DIMENSION'})
msp.add_line((80, -80), (90, -80), dxfattribs={'layer': 'DIMENSION'})
msp.add_line((87, 0), (87, -80), dxfattribs={'layer': 'DIMENSION'})
# Arrows (small lines)
msp.add_line((85, 0), (89, 0), dxfattribs={'layer': 'DIMENSION'})
msp.add_line((85, -80), (89, -80), dxfattribs={'layer': 'DIMENSION'})

# ============================================================
# ADD LEADER LINES for dimension annotations
# ============================================================
# Leader for R96
msp.add_line((28, 69), (15, 60), dxfattribs={'layer': 'DIMENSION'})

# Leader for R64
msp.add_line((53, 49), (45, 40), dxfattribs={'layer': 'DIMENSION'})

# Leader for Ø50
msp.add_line((-73, 28), (-25, 15), dxfattribs={'layer': 'DIMENSION'})

# Leader for R20 bore
msp.add_line((-68, -1), (-20, -5), dxfattribs={'layer': 'DIMENSION'})

# Leader for R36
msp.add_line((43, -41), (25, -35), dxfattribs={'layer': 'DIMENSION'})

# Leader for R35
msp.add_line((38, -61), (20, -55), dxfattribs={'layer': 'DIMENSION'})

# Leader for Ø40
msp.add_line((33, -86), (20, -80), dxfattribs={'layer': 'DIMENSION'})

# Leader for R9-4X
msp.add_line((10, -108), (18, -95), dxfattribs={'layer': 'DIMENSION'})

# ============================================================
# ADD CONSTRUCTION CIRCLES (reference circles shown dashed)
# ============================================================
# R64 bolt circle (construction/reference)
msp.add_circle(
    center=(0, 0),
    radius=R64,
    dxfattribs={'layer': 'CONSTRUCTION'}
)

# ============================================================
# SAVE THE FILE
# ============================================================
output_dxf = '/projects/sandbox/AMMAN/Mechanical_Part_Drawing.dxf'
doc.saveas(output_dxf)
print(f"DXF file saved: {output_dxf}")
print("This file can be opened directly in AutoCAD, BricsCAD, LibreCAD, or any DXF-compatible CAD software.")
print("To convert to DWG, open in AutoCAD and use 'Save As' → DWG format.")
