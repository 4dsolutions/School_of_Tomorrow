import bpy
from qrays import Qvector
import sys

sys.path.append("C:\\Users\\Kirby\\School_of_Tomorrow")
from itertools import permutations
g = permutations((2,1,1,0))

ORIGIN_IVM = Qvector((0,0,0,0))
# set comprehension in list comprehension
SPOKES_IVM = [Qvector(v) for v in {p for p in g}] 
ORIGIN_XYZ = ORIGIN_IVM.xyz().xyz # (0,0,0)

c6xty_ball = bpy.ops.mesh.primitive_ico_sphere_add
c6xty_ball(radius=0.5, enter_editmode=False, location=ORIGIN_XYZ)
bpy.ops.object.shade_smooth()

for qv in SPOKES_IVM:
    xyz = qv.xyz().xyz
    c6xty_ball(radius=0.5, enter_editmode=False, location=xyz)
    # bpy.ops.object.shade_smooth()
