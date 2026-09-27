"""Trace a city skyline from a photo into the POLY array used by index.html.

Usage:
  python3 trace_skyline.py photo.jpg SKY_Y FG_Y WATERLINE_Y > poly.json

  SKY_Y        a row (in photo pixels) above the tallest building: everything above is sky
  FG_Y         a row that is solidly buildings all the way across
  WATERLINE_Y  the row where buildings meet the water or ground

Best photos: your own, shot level from across water at blue hour, no zoom.
Needs: pip install opencv-python-headless numpy scipy
"""
import sys, json
import cv2, numpy as np
from scipy.ndimage import median_filter

f, sky_y, fg_y, wl = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
S = 3
im = cv2.resize(cv2.imread(f), None, fx=S, fy=S, interpolation=cv2.INTER_CUBIC)
H, W = im.shape[:2]

# 1. Separate sky from city with GrabCut, seeded by the three rows above
m = np.full((H, W), cv2.GC_PR_BGD, np.uint8)
m[:sky_y*S] = cv2.GC_BGD
m[fg_y*S:wl*S] = cv2.GC_FGD
m[wl*S:] = cv2.GC_BGD
bg = np.zeros((1, 65)); fg = np.zeros((1, 65))
cv2.grabCut(im, m, None, bg, fg, 6, cv2.GC_INIT_WITH_MASK)
mask = ((m == 1) | (m == 3)).astype(np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
n, lab = cv2.connectedComponents(mask)
mask = np.isin(lab, list(set(lab[fg_y*S+2, :]) - {0})).astype(np.uint8)

# 2. Top edge of the city in every column
base = wl - 6
top = np.array([np.argmax(mask[:wl*S, x]) if mask[:wl*S, x].any() else wl*S for x in range(W)]) / S
top = median_filter(np.minimum(top, base), size=7, mode='nearest')

# 3. Staircase -> simplified polygon, snapped to verticals and horizontals
pts = [(0, float(base))]
for i, y in enumerate(top):
    xx = i / S
    if pts[-1][1] != y:
        pts += [(xx, pts[-1][1]), (xx, float(y))]
pts += [(W / S, pts[-1][1]), (W / S, float(base))]
A = cv2.approxPolyDP(np.array(pts, np.float32).reshape(-1, 1, 2), 0.9, False).reshape(-1, 2).tolist()
out = [A[0]]
for px, py in A[1:]:
    qx, qy = out[-1]
    if abs(px - qx) <= abs(py - qy) * 0.3: px = qx
    elif abs(py - qy) <= abs(px - qx) * 0.18: py = qy
    if abs(px - qx) > 1e-3 or abs(py - qy) > 1e-3: out.append([px, py])
json.dump([[round(a, 2), round(b, 2)] for a, b in out], sys.stdout)
print(f"\n# photo width {W//S}, base row {base}", file=sys.stderr)
