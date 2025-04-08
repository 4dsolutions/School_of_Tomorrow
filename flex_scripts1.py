#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 12:27:41 2025

@author: kirbyurner

Apr 8, 2025: slice this off from the end of flextegrity.py, make standalone

"""
from flextegrity import pov_header, Cuboctahedron, Cube, Octahedron, RT
from flextegrity import Tetrahedron, InvTetrahedron, RD, PD, Icosahedron
from flextegrity import draw_poly, draw_vert, half, ORIGIN, PHI

from math import sqrt as rt2

from itertools import permutations
g = permutations((2,1,1,0))
UNIQUE = {p for p in g}  # set comprehension

# IVM_DIRS = {Qvector(x) for x in UNIQUE}

Svol = (PHI **-5)/2  
Evol = (rt2(2)/8) * (PHI ** -3)

sfactor = Svol/Evol

def test1():
    """
    minimalist, uses default Icosahedron and PD
    no fidling with attributes, no rescaling.
    """
    f = open("testing123.pov", "w")
    f.write(pov_header)
    ico = Icosahedron()
    pd = PD()
    draw_poly(ico, f)
    draw_poly(pd, f)
    f.close()
    
def test2():
    """
    same as test1 but adding a Rhombic Triacontahedron
    ico and pd are duals of each other, sized by default
    to criss-cross at mid-edges thereby forming verts
    of the correspondingly sized RT
    """    
    f = open("testing123.pov", "w")
    f.write(pov_header)
    ico = Icosahedron()
    pd = PD()
    rt = RT()
    draw_poly(ico, f)
    draw_poly(pd, f)
    draw_poly(rt, f)
    f.close()
    
def test3():
    """
    Remember you can edit these by turning shapes on and off.
    You have control over the filename if you wish to stop
    overwriting the same testing123 over and over
    """
    f = open("testing123.pov", "w")
    f.write(pov_header)
    # ico = Icosahedron()
    rt = RT()
    draw_poly(rt, f)
    # draw_poly(ico, f)
    f.close()
    
def test4():
    """
    Taking default Icosahedron to have R=1 edges (vs D=1),
    such scaling by sfactor gives IcosaWithin (IW), which,
    when further scaled up by PHI, becomes faces flush 
    with 2F SuperCube. 4 * Cube() because everything's 
    doubled when R=1 vs 0.5.
    """
    f = open("testing123.pov", "w")
    f.write(pov_header)
    octa = 2 * Octahedron()
    co = Cuboctahedron()
    ico = Icosahedron() * sfactor
    #rt = RT() * sfactor * PHI
    #cu = 4 * Cube()
    draw_poly(ico, f)
    draw_poly(octa, f)
    draw_poly(co, f)
    #draw_poly(cu, f)
    #draw_poly(rt, f)
    f.close()
    
def test5():
    """
    Same as above, but once RT is faces flush with 
    containing cube, enlarge is very slightly to 
    force its diamond faces to protrude and show 
    up clearly against the 2F cube faces background
    """
    f = open("marble_polys.pov", "w")
    f.write(pov_header)
    rt = RT() * sfactor * PHI * 1.01 # push out faces a bit more
    rt.face_color = "T_Stone18"
    cu = 4 * Cube()
    cu.face_color = "T_Stone17"
    draw_poly(rt, f, v=False, e=False, f=True, texture=True)
    draw_poly(cu, f, v=False, e=False, f=True, texture=True)
    f.close()

def test6():
    """
    Back to D=1. Shrink initial D edge Icosa by half then
    scale up by sfactor, known to be edges of the icosa
    inscribing in the corresponding Octa. Include the 
    2F Cube with faces-flush RT in addition to IW faces
    flush with Octa.
    """
    out = open("iw_rt_123.pov", "w")
    out.write(pov_header)
    # Icosa with edges sfactor = S/E
    icosaWithin = Icosahedron() * half * sfactor # D=1 (volume 60S + 20s3)
    octa = Octahedron()              # corresponding octa edges D
    rt = RT() * half * sfactor * PHI  # blow up corresponding RT by PHI
    cu_2F = Cube() * 2               # 2F Cube
    draw_poly(icosaWithin, out)
    draw_poly(octa, out)
    draw_poly(cu_2F, out)
    draw_poly(rt, out)
    out.close()

def test6a():
    """
    MM1
    """
    out = open("test_6a.pov", "w")
    out.write(pov_header)
    tet  = Tetrahedron()
    inv  = InvTetrahedron()
    cu   = Cube()
    octa = Octahedron()              # corresponding octa edges D
    rd   = RD()
    cu_2F = Cube() * 2               # 2F Cube
    draw_poly(tet, out)
    draw_poly(inv, out)
    draw_poly(cu, out)
    draw_poly(rd, out)
    draw_poly(octa, out)
    draw_poly(rd, out)
    draw_poly(cu_2F, out)
    out.close()

def test6b():
    """
    MM2
    """
    out = open("test_6b.pov", "w")
    out.write(pov_header)
    tet  = Tetrahedron()
    inv  = InvTetrahedron()
    cu   = Cube()
    octa = Octahedron()
    rd   = RD()
    cu_2F = Cube() * 2
    
    draw_poly(tet, out)
    draw_poly(inv, out)
    draw_poly(octa, out)
    draw_poly(rd, out)
    draw_poly(cu, out)
    draw_poly(cu_2F, out)
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    out.close()
    
def test7():
    out = open("ico_pd.pov", "w")
    out.write(pov_header)
    #ico = Icosahedron()*2
    #pd = PD()*2
    rt = RT()*2
    #draw_poly(ico, out)
    #draw_poly(pd, out)
    draw_poly(rt, out)
    out.close()
    
def test8():
    out = open("ball_rt.pov", "w")
    out.write(pov_header) 
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    rt = RT() * (1/PHI)  # SuperRT scaled down to wrap uniradius ball
    rt.edge_radius = 0.02
    rt.vert_radius = 0.04
    rt.vert_color = 'T_Copper_1A'
    rt.edge_color = 'T_Chrome_1A'
    draw_poly(rt, out, v=True, e=True, f=False, texture=True)
    out.close()
    
def test9():
    out = open("ball_rt_rd.pov", "w")
    out.write(pov_header) 
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    rt = RT() * (1/PHI)  # SuperRT scaled down to wrap uniradius ball
    rt.edge_radius = 0.02
    rt.vert_radius = 0.04
    rt.vert_color = 'T_Copper_1A'
    rt.edge_color = 'T_Chrome_1A'
    
    rt_2 = RT() * (1/PHI) * 0.9994 * (3/2)**(1/3) # 7.5 RT_K
    rt_2.edge_radius = 0.02
    
    rd = RD()
    rd.edge_radius = 0.02
    rd.vert_radius = 0.04
    rd.vert_color = 'T_Copper_1A'
    rd.edge_color = 'T_Silver_1A'
    
    draw_poly(rd, out, v=True, e=True, f=False, texture=True)
    draw_poly(rt, out, v=True, e=True, f=False, texture=True)
    draw_poly(rt_2, out, v=False, e=True, f=False)
    out.close()

def test10():
    out = open("ball_in_rt_t.pov", "w")
    out.write(pov_header) 
    draw_vert(ORIGIN, "rgb <1, 0, 0>", half, out)
    rt = RT() * (1/(3*rt2(2)))**(1/3)  # RT_T
    rt.face_color = "T_Stone17"
    draw_poly(rt, out, v=False, e=False, f=True, texture=True)
    out.close()

if __name__ == "__main__":
    test10()
    