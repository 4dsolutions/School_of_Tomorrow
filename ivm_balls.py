import bpy
import sys

sys.path.append("C:\\Users\\Kirby\\School_of_Tomorrow")
from qrays import Qvector


from functools import partial
from itertools import permutations

g = permutations((2,1,1,0))

ORIGIN_IVM = Qvector((0,0,0,0))
# set comprehension in list comprehension
SPOKES_IVM = [Qvector(v) for v in {p for p in g}] 
nucleus = tuple([ORIGIN_IVM])

def next_layer(curr_layer, prev_layer):
    """
    generates a next layer of FCC spheres by trying 12-around-1 
    for each in the current layer (curr_layer) but without keeping
    any duplicates i.e. discarding redundant sphere centers.
    """
    next_layer = set()
    for qv in curr_layer:
        for bv in SPOKES_IVM:
            v_sum = qv + bv
            if (not v_sum in curr_layer 
                and not v_sum in prev_layer):
                next_layer.add(v_sum)
    return sorted(list(next_layer))

nl   = next_layer(nucleus, nucleus) # 1-freq
nnl  = next_layer(nl, nucleus)      # 2-freq
nnnl = next_layer(nnl, nl)          # 3-freq
nnnnl= next_layer(nnnl, nnl)        # 4-freq

def get_xyz(qvectors):
    xyz_vectors = []
    for qv in qvectors:
        xyz_vectors.append(qv.xyz())
    return xyz_vectors

# c6xty_ball = bpy.ops.mesh.primitive_ico_sphere_add
c6xty_ball = partial(bpy.ops.mesh.primitive_ico_sphere_add, subdivisions=1, radius=0.5, enter_editmode=False)


for ball in get_xyz(nl):
    c6xty_ball(location=ball.xyz)

for ball in get_xyz(nnl):
    c6xty_ball(location=ball.xyz)
    
for ball in get_xyz(nnnl):
    c6xty_ball(location=ball.xyz)

for ball in get_xyz(nnnnl):
    c6xty_ball(location=ball.xyz)