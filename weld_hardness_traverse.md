# Vickers Microhardness Traverse Across the Weld (VHN / HV0.5)

**Filler wire:** E6018  |  **Load:** HV0.5  |  **Temperature:** ~23 C (room)  |  ISO 6507-1

**Traverse:** x = -8.0 mm to +8.0 mm at 0.1 mm interval (161 points per weld)  |  **Replicates:** n = 3 per point (Mean +/- sample StdDev).

**Fusion-line interfaces:** x = -5 mm and x = +5 mm.

> These are representative, literature-consistent (synthetic) values, not measured laboratory results.

## Zone boundary definitions

| Zone | Position (distance from centerline, mm) |
|---|---|
| Fusion Zone / Weld Metal (E6018) | |x| < 3.8 |
| Heat-Affected Zone (HAZ) | 3.8 <= |x| < 5.0 (1.2 mm band inside each fusion line) |
| Base Metal | 5.0 <= |x| <= 8.0 |

## Peak / plateau summary per weld

| Weld Type | Left Base (HV) | Left HAZ peak (HV) | Weld Metal (HV) | Right HAZ peak (HV) | Right Base (HV) |
|---|---|---|---|---|---|
| X70-X70 | 215 | 252 | 194 | 252 | 215 |
| S355-S355 | 165 | 206 | 186 | 206 | 165 |
| X70-S355 | 215 | 249 | 192 | 202 | 164 |

The X70-S355 dissimilar weld is **asymmetric**: the higher X70 base/HAZ appears on the left (x < 0) and the softer S355 base/HAZ on the right (x > 0).

## Condensed profile: X70-X70 (every 0.5 mm)

| x (mm) | Mean (HV) | StdDev (HV) | Zone |
|---|---|---|---|
| -8.0 | 218.1 | 2.3 | Base Metal - X70 |
| -7.5 | 214.6 | 2.4 | Base Metal - X70 |
| -7.0 | 212.7 | 4.4 | Base Metal - X70 |
| -6.5 | 220.7 | 6.0 | Base Metal - X70 |
| -6.0 | 219.2 | 2.4 | Base Metal - X70 |
| -5.5 | 220.2 | 5.5 | Base Metal - X70 |
| -5.0 | 218.7 | 2.5 | Base Metal - X70 |
| -4.5 | 250.9 | 2.5 | HAZ - X70 |
| -4.0 | 208.1 | 4.4 | HAZ - X70 |
| -3.5 | 189.7 | 2.2 | Fusion Zone (E6018) |
| -3.0 | 194.6 | 13.1 | Fusion Zone (E6018) |
| -2.5 | 193.7 | 7.8 | Fusion Zone (E6018) |
| -2.0 | 187.5 | 4.9 | Fusion Zone (E6018) |
| -1.5 | 190.2 | 6.9 | Fusion Zone (E6018) |
| -1.0 | 197.6 | 1.6 | Fusion Zone (E6018) |
| -0.5 | 196.1 | 3.1 | Fusion Zone (E6018) |
| 0.0 | 191.8 | 5.7 | Fusion Zone (E6018) |
| 0.5 | 186.6 | 4.1 | Fusion Zone (E6018) |
| 1.0 | 190.0 | 9.9 | Fusion Zone (E6018) |
| 1.5 | 189.4 | 2.5 | Fusion Zone (E6018) |
| 2.0 | 193.0 | 6.3 | Fusion Zone (E6018) |
| 2.5 | 190.7 | 1.0 | Fusion Zone (E6018) |
| 3.0 | 193.8 | 11.2 | Fusion Zone (E6018) |
| 3.5 | 192.0 | 8.4 | Fusion Zone (E6018) |
| 4.0 | 198.2 | 3.7 | HAZ - X70 |
| 4.5 | 247.2 | 3.8 | HAZ - X70 |
| 5.0 | 220.4 | 6.5 | Base Metal - X70 |
| 5.5 | 218.7 | 2.7 | Base Metal - X70 |
| 6.0 | 222.8 | 2.6 | Base Metal - X70 |
| 6.5 | 223.4 | 6.1 | Base Metal - X70 |
| 7.0 | 216.5 | 4.8 | Base Metal - X70 |
| 7.5 | 212.6 | 2.6 | Base Metal - X70 |
| 8.0 | 216.2 | 3.9 | Base Metal - X70 |

_Full 161-point profile at 0.1 mm resolution is in `weld_hardness_traverse.csv`._

## Condensed profile: S355-S355 (every 0.5 mm)

| x (mm) | Mean (HV) | StdDev (HV) | Zone |
|---|---|---|---|
| -8.0 | 163.8 | 7.6 | Base Metal - S355 |
| -7.5 | 162.4 | 9.0 | Base Metal - S355 |
| -7.0 | 170.9 | 4.5 | Base Metal - S355 |
| -6.5 | 169.5 | 7.0 | Base Metal - S355 |
| -6.0 | 169.7 | 2.7 | Base Metal - S355 |
| -5.5 | 174.6 | 2.1 | Base Metal - S355 |
| -5.0 | 175.8 | 5.7 | Base Metal - S355 |
| -4.5 | 205.7 | 1.5 | HAZ - S355 |
| -4.0 | 193.7 | 7.8 | HAZ - S355 |
| -3.5 | 188.8 | 2.4 | Fusion Zone (E6018) |
| -3.0 | 183.7 | 5.9 | Fusion Zone (E6018) |
| -2.5 | 184.0 | 2.1 | Fusion Zone (E6018) |
| -2.0 | 186.1 | 2.3 | Fusion Zone (E6018) |
| -1.5 | 181.8 | 3.0 | Fusion Zone (E6018) |
| -1.0 | 181.9 | 6.7 | Fusion Zone (E6018) |
| -0.5 | 184.4 | 0.5 | Fusion Zone (E6018) |
| 0.0 | 185.6 | 6.5 | Fusion Zone (E6018) |
| 0.5 | 182.6 | 7.8 | Fusion Zone (E6018) |
| 1.0 | 183.8 | 4.0 | Fusion Zone (E6018) |
| 1.5 | 179.7 | 10.3 | Fusion Zone (E6018) |
| 2.0 | 187.2 | 2.8 | Fusion Zone (E6018) |
| 2.5 | 182.3 | 9.6 | Fusion Zone (E6018) |
| 3.0 | 181.0 | 3.4 | Fusion Zone (E6018) |
| 3.5 | 184.0 | 1.6 | Fusion Zone (E6018) |
| 4.0 | 191.2 | 9.0 | HAZ - S355 |
| 4.5 | 205.3 | 2.8 | HAZ - S355 |
| 5.0 | 169.7 | 7.2 | Base Metal - S355 |
| 5.5 | 172.8 | 1.9 | Base Metal - S355 |
| 6.0 | 166.5 | 3.9 | Base Metal - S355 |
| 6.5 | 170.2 | 5.2 | Base Metal - S355 |
| 7.0 | 173.6 | 6.8 | Base Metal - S355 |
| 7.5 | 164.7 | 7.9 | Base Metal - S355 |
| 8.0 | 166.0 | 6.8 | Base Metal - S355 |

_Full 161-point profile at 0.1 mm resolution is in `weld_hardness_traverse.csv`._

## Condensed profile: X70-S355 (every 0.5 mm)

| x (mm) | Mean (HV) | StdDev (HV) | Zone |
|---|---|---|---|
| -8.0 | 214.0 | 1.5 | Base Metal - X70 side |
| -7.5 | 217.6 | 6.6 | Base Metal - X70 side |
| -7.0 | 216.1 | 1.5 | Base Metal - X70 side |
| -6.5 | 210.0 | 4.1 | Base Metal - X70 side |
| -6.0 | 213.9 | 3.7 | Base Metal - X70 side |
| -5.5 | 221.3 | 10.3 | Base Metal - X70 side |
| -5.0 | 222.6 | 5.4 | Base Metal - X70 side |
| -4.5 | 247.9 | 7.2 | HAZ - X70 side |
| -4.0 | 199.8 | 4.2 | HAZ - X70 side |
| -3.5 | 192.9 | 6.3 | Fusion Zone (E6018) |
| -3.0 | 187.2 | 7.1 | Fusion Zone (E6018) |
| -2.5 | 183.6 | 2.8 | Fusion Zone (E6018) |
| -2.0 | 182.3 | 0.7 | Fusion Zone (E6018) |
| -1.5 | 187.8 | 1.7 | Fusion Zone (E6018) |
| -1.0 | 190.2 | 3.7 | Fusion Zone (E6018) |
| -0.5 | 188.6 | 2.8 | Fusion Zone (E6018) |
| 0.0 | 189.7 | 5.8 | Fusion Zone (E6018) |
| 0.5 | 186.9 | 3.8 | Fusion Zone (E6018) |
| 1.0 | 194.8 | 7.5 | Fusion Zone (E6018) |
| 1.5 | 191.6 | 5.7 | Fusion Zone (E6018) |
| 2.0 | 192.5 | 4.7 | Fusion Zone (E6018) |
| 2.5 | 191.1 | 7.9 | Fusion Zone (E6018) |
| 3.0 | 193.4 | 3.5 | Fusion Zone (E6018) |
| 3.5 | 188.4 | 7.7 | Fusion Zone (E6018) |
| 4.0 | 193.7 | 8.1 | HAZ - S355 side |
| 4.5 | 199.4 | 3.2 | HAZ - S355 side |
| 5.0 | 169.5 | 3.8 | Base Metal - S355 side |
| 5.5 | 167.5 | 3.4 | Base Metal - S355 side |
| 6.0 | 169.8 | 7.4 | Base Metal - S355 side |
| 6.5 | 168.7 | 4.5 | Base Metal - S355 side |
| 7.0 | 163.7 | 3.9 | Base Metal - S355 side |
| 7.5 | 162.5 | 6.4 | Base Metal - S355 side |
| 8.0 | 165.5 | 6.5 | Base Metal - S355 side |

_Full 161-point profile at 0.1 mm resolution is in `weld_hardness_traverse.csv`._
