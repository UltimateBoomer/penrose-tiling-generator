# Reference: https://preshing.com/20110831/penrose-tiling-explained/

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.collections as mplc
import matplotlib.patheffects as mplpe
import matplotlib.style as mplstyle
import math
import cmath
from collections import deque

# Colors
COLOR1 = '#ffc300'
COLOR2 = '#c70039'
LINE_COLOR = 'black'

# Parameters
iterations = 5

phi = (1 + math.sqrt(5)) / 2

def get_color(ty):
    return COLOR2 if ty else COLOR1

def subdiv(tris: deque):
    for i in range(len(tris)):
        (ty, a, b, c) = tris.popleft()
        if ty == 0:
            p = a + (b - a) / phi
            tris.extend([(0, c, p, b), (1, p, c, a)])
        elif ty == 1:
            q = b + (a - b) / phi
            r = b + (c - b) / phi
            tris.extend([(1, r, c, a), (1, q, r, b), (0, r, q, a)])

# Initial setup
base_tris = []
# Triangle fan
for i in range(10):
    b = cmath.rect(1, (2*i - 1) * math.pi / 10)
    c = cmath.rect(1, (2*i + 1) * math.pi / 10)
    if i % 2 == 0:
        b, c = c, b
    base_tris.append((0, 0j, b, c))

# Iteration
tris = deque(base_tris)
for i in range(iterations):
    subdiv(tris)

fig = plt.figure()

base_tri_verts = []

for ty, a, b, c in base_tris:
    base_tri_verts.append(((a.real, a.imag), (b.real, b.imag), (c.real, c.imag)))

tri_verts = []
line_segs = []

for ty, a, b, c in tris:
    if ty == 0:
        tri_verts.append(((a.real, a.imag), (b.real, b.imag), (c.real, c.imag)))

    line_segs.append(((b.real, b.imag), (a.real, a.imag), (c.real, c.imag)))

# Remove duplicate lines
print(f'Tri 108: {len(tri_verts)}')
print(f'Tri 36:  {len(tris) - len(tri_verts)}')
print(f'Lines:   {len(line_segs)}')

lw = 10 / phi ** iterations

save = input('Save plot (y/n)? ').lower() == 'y'

if not save:
    exit()

qual = 15

base_tri_c = mplc.PolyCollection(base_tri_verts, color=COLOR2, linewidth=lw)
tri_c = mplc.PolyCollection(tri_verts, color=COLOR1, linewidth=lw )
line_c = mplc.LineCollection(line_segs, color=LINE_COLOR, linewidth=lw, path_effects=[mplpe.Stroke(capstyle='round')])

ax = fig.add_subplot()
ax.add_collection(base_tri_c)
ax.add_collection(tri_c)
ax.add_collection(line_c)

plt.axis('off')
plt.xlim([-1.0, 1.0])
plt.ylim([-1.0, 1.0])
ax.set_aspect('equal')

# Save graph
mplstyle.use('fast')
plt.savefig(f'penrose-{iterations}.png', dpi=max(300, qual * phi ** iterations))