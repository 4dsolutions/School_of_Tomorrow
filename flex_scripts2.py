#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thurs Feb 13 2025

@author: K. Urner

Apr  8: make this 2nd of 2 files, flex_scripts1.py being the first
Feb 19: import PHI as sympy object vs using math.sqrt  
"""

from flextegrity import pov_header, Cuboctahedron, Cube, Octahedron, RT
from flextegrity import Tetrahedron, InvTetrahedron, RD, PD, Icosahedron, Mite
from flextegrity import Edge, draw_edge, draw_poly, draw_vert, half, ORIGIN, PHI
from qrays import Qvector, Vector, A, B, C, D

import numpy as np
import sympy as sy
from sympy import sqrt as rt2

from itertools import permutations
g = permutations((2,1,1,0))
UNIQUE = {p for p in g}  # set comprehension

IVM_DIRS = {Qvector(x) for x in UNIQUE}

Svol = (PHI **-5)/2  
Evol = (rt2(2)/8) * (PHI ** -3)

sfactor = Svol/Evol

BRYG = \
"""

// perspective (default) camera
camera {
  location  <0.1, 0.2, 4.5>
  rotate    <20, 30, 180>
  //rotate    <35, 55, 20.0>
  look_at   <0.0, 0.0,  0.0>
  right     x*image_width/image_height
}

"""

CLOSEUP = \
"""
   
// perspective (default) camera
camera {
  location  <2, 0.1, 0.2>
  rotate    <35, 35, 10.0>
  look_at   <0.0, 0.0,  0.0>
  right     x*image_width/image_height
}

"""
    
def test11():
    out = open("rt_spokes.pov", "w")
    out.write(pov_header) 
    
    rt_t = RT() * (1/(3*rt2(2)))**(1/3)  # RT_T
    for face in rt_t.faces:
        spoke = ORIGIN
        for i in range(4):
            spoke += rt_t.vertexes[face[i]] 
        spoke = spoke * 0.25
        edge = Edge(ORIGIN, spoke)
        draw_edge(edge, "rgb <0, 0, 1>", 0.02, out)
    rt_t.edge_radius = 0.01
    draw_poly(rt_t, out, v=False, e=True, f=False)

    rt_e = RT() * (1/PHI)   # RT_E
    for face in rt_e.faces:
        spoke = ORIGIN
        for i in range(4):
            spoke += rt_e.vertexes[face[i]] 
        spoke = spoke * 0.25
        edge = Edge(ORIGIN, spoke)
        draw_edge(edge, "rgb <1, 0, 0>", 0.01, out)
    rt_t.face_color = "T_Stone17"
    draw_poly(rt_t, out, v=False, e=False, f=True, texture=True)
    
    out.close()

def test12():
    out = open("stella_octangula.pov", "w")
    out.write(pov_header)
    tet = Tetrahedron()
    tet.edge_radius = 0.01
    invtet = InvTetrahedron()
    invtet.edge_radius = 0.01
    octa = Octahedron() * (1/2)
    octa.vert_radius = 0.01
    octa.edge_radius = 0.01
    cu = Cube()
    cu.vert_radius = 0.01
    cu.edge_radius = 0.01
    draw_poly(tet, out, v=False, e=True, f=False)
    draw_poly(invtet, out, v=False, e=True, f=False)
    draw_poly(octa, out, v=True, e=True, f=False)
    draw_poly(cu,   out, v=True, e=True, f=False)
    out.close()
    
def test13():
    out = open("stella_octangula_2.pov", "w")
    out.write(pov_header)
    tet = Tetrahedron()
    tet.edge_radius = 0.01
    invtet = InvTetrahedron()
    invtet.edge_radius = 0.01
    cu = Cube()
    cu.vert_radius = 0.01
    cu.edge_radius = 0.01
    draw_poly(tet, out, v=False, e=True, f=True)
    draw_poly(invtet, out, v=False, e=True, f=True)
    draw_poly(cu,   out, v=True, e=True, f=False)
    out.close()

def test14():
    out = open("tet_cu_octa_dodeca.pov", "w")
    out.write(pov_header)
    tet = Tetrahedron()
    tet.edge_radius = 0.01
    invtet = InvTetrahedron()
    invtet.edge_radius = 0.01
    octa = Octahedron()
    octa.vert_radius = 0.01
    octa.edge_radius = 0.01
    cu = Cube()
    cu.vert_radius = 0.01
    cu.edge_radius = 0.01
    rd = RD()
    rd.vert_radius = 0.02
    rd.edge_radius = 0.02
    # draw_poly(tet, out, v=False, e=True, f=False)
    # draw_poly(invtet, out, v=False, e=True, f=False)
    draw_poly(octa, out, v=True, e=True, f=False)
    draw_poly(cu,   out, v=True, e=True, f=False)
    draw_poly(rd,   out, v=True, e=True, f=False)
    out.close()

def test15():
    out = open("gif1.pov", "w")
    out.write(pov_header)
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    out.close()
    
    out = open("gif2.pov", "w") 
    out.write(pov_header)   
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    tet = Tetrahedron()
    tet.vert_radius = tet.edge_radius
    invtet = InvTetrahedron()
    invtet.vert_radius = invtet.edge_radius
    draw_poly(tet, out, v=True, e=True, f=False)
    draw_poly(invtet, out, v=True, e=True, f=False)
    out.close()    

    out = open("gif3.pov", "w") 
    out.write(pov_header) 
    tet = Tetrahedron()
    tet.vert_radius = tet.edge_radius
    invtet = InvTetrahedron()
    invtet.vert_radius = invtet.edge_radius
    draw_poly(tet, out, v=True, e=True, f=False)
    draw_poly(invtet, out, v=True, e=True, f=False)
    
    out = open("gif4.pov", "w")
    out.write(pov_header)   
    tet = Tetrahedron()
    tet.vert_radius = tet.edge_radius
    invtet = InvTetrahedron()
    invtet.vert_radius = invtet.edge_radius
    cu = Cube()
    cu.vert_radius = cu.edge_radius
    draw_poly(tet, out, v=True, e=True, f=False)
    draw_poly(invtet, out, v=True, e=True, f=False)
    draw_poly(cu,   out, v=True, e=True, f=False)
    out.close()
    
    out = open("gif5.pov", "w")
    out.write(pov_header)   
    cu = Cube()
    cu.vert_radius = cu.edge_radius
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius
    draw_poly(cu,   out, v=True, e=True, f=False)
    draw_poly(octa,   out, v=True, e=True, f=False)
    out.close()
    
    out = open("gif6.pov", "w")
    out.write(pov_header)  
    cu = Cube()
    cu.vert_radius = cu.edge_radius
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius
    rd = RD()
    rd.vert_radius = rd.edge_radius
    draw_poly(cu,   out, v=True, e=True, f=False)
    draw_poly(octa,   out, v=True, e=True, f=False)
    draw_poly(rd,   out, v=True, e=True, f=False)
    out.close()
    
    out = open("gif7.pov", "w")
    out.write(pov_header)   
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    rd = RD()
    rd.vert_radius = rd.edge_radius
    draw_poly(rd,   out, v=True, e=True, f=False)
    out.close()
    
    out = open("gif8.pov", "w")
    out.write(pov_header)   
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    rd = RD()
    rd.vert_radius = rd.edge_radius
    rt = RT() * (1/rt2(2)) # 7.5 RT
    rt.vert_radius = rt.edge_radius
    draw_poly(rd,   out, v=True, e=True, f=False)
    draw_poly(rt,   out, v=True, e=True, f=False)
    out.close()

    out = open("gif9.pov", "w")
    out.write(pov_header)   
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    rt = RT() * (1/PHI)
    rt.vert_radius = rt.edge_radius
    draw_poly(rt,   out, v=True, e=True, f=False)
    out.close()

def test16():
    out = open("gif1.pov", "w")
    out.write(pov_header)
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    out.close()

    out = open("gif2.pov", "w") 
    out.write(pov_header)   
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    co = Cuboctahedron() * half
    co.vert_radius = co.edge_radius
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius
    draw_poly(co, out, v=True, e=True, f=False)
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()  
    
    out = open("gif3.pov", "w") 
    out.write(pov_header)   
    co = Cuboctahedron() * half
    co.vert_radius = co.edge_radius
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius
    draw_poly(co, out, v=True, e=True, f=False)
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close() 
    
    out = open("gif4.pov", "w") 
    out.write(pov_header)   
    co = Cuboctahedron() * half
    co.vert_radius = co.edge_radius
    # Icosa with edges sfactor = S/E
    iw = Icosahedron() * half * sfactor # edges 1.08R... (volume 60S + 20s3)
    iw.vert_radius = iw.edge_radius
    draw_poly(co, out, v=True, e=True, f=False)
    draw_poly(iw, out, v=True, e=True, f=False)
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()  
    
    out = open("gif5.pov", "w") 
    out.write(pov_header)   
    # Icosa with edges sfactor = S/E
    iw = Icosahedron() * half * sfactor # edges 1.08R... (volume 60S + 20s3)
    iw.vert_radius = iw.edge_radius
    draw_poly(iw, out, v=True, e=True, f=False)
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()
    
    out = open("gif6.pov", "w") 
    out.write(pov_header)   
    ic = Icosahedron() 
    ic.vert_radius = ic.edge_radius
    draw_poly(ic, out, v=True, e=True, f=False)
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()
    
    out = open("gif7.pov", "w") 
    out.write(pov_header)   
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    ic = Icosahedron() 
    ic.vert_radius = ic.edge_radius
    draw_poly(ic, out, v=True, e=True, f=False)
    co = Cuboctahedron() 
    co.vert_radius = co.edge_radius
    draw_poly(co, out, v=True, e=True, f=False)
    out.close()

def test17():
    out = open("gif1.pov", "w")
    out.write(pov_header)
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    out.close()

    out = open("gif2.pov", "w") 
    out.write(pov_header) 
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius = 0.01
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()  
    
    out = open("gif3.pov", "w") 
    out.write(pov_header)   
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius = 0.01
    iw = Icosahedron() * half * sfactor # edges 1.08R... (volume 60S + 20s3)
    iw.vert_radius = iw.edge_radius = 0.01
    draw_poly(iw, out, v=True, e=True, f=True)
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()  
    
    out = open("gif4.pov", "w") 
    out.write(pov_header)   
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    iw = Icosahedron() * half * sfactor # edges 1.08R... (volume 60S + 20s3)
    iw.vert_radius = iw.edge_radius = 0.01
    pd = PD() * half * sfactor # edges 1.08R... (volume 60S + 20s3)
    pd.vert_radius = pd.edge_radius = 0.01
    rt = RT() * half * sfactor
    rt.vert_radius = rt.edge_radius = 0.01
    draw_poly(iw, out, v=True, e=True, f=True)
    draw_poly(pd, out, v=True, e=True, f=False)
    draw_poly(rt, out, v=True, e=True, f=False)
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close() 
    
    out = open("gif5.pov", "w") 
    out.write(pov_header)   
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    iw = Icosahedron() * half * sfactor # edges 1.08R... (volume 60S + 20s3)
    iw.vert_radius = iw.edge_radius = 0.01
    pd = PD() * half * sfactor # edges 1.08R... (volume 60S + 20s3)
    pd.vert_radius = pd.edge_radius = 0.01
    rt = RT() * half * sfactor
    rt.vert_radius = rt.edge_radius = 0.01
    draw_poly(iw, out, v=True, e=True, f=False)
    draw_poly(pd, out, v=True, e=True, f=True)
    draw_poly(octa, out, v=True, e=True, f=True)
    draw_poly(rt, out, v=True, e=True, f=False)
    out.close() 
    
    out = open("gif6.pov", "w") 
    out.write(pov_header)      
    rd = RD() * (2/PHI**2) 
    rd.vert_radius = rd.edge_radius = 0.01
    rt = RT() * half * sfactor
    rt.vert_radius = rt.edge_radius = 0.01
    draw_poly(rt, out, v=True, e=True, f=False)
    draw_poly(rd, out, v=True, e=True, f=False)
    out.close()
    
    out = open("gif7.pov", "w") 
    out.write(pov_header)      
    rd = RD() * (2/PHI**2) 
    rd.vert_radius = rd.edge_radius = 0.01
    cu = Cube() * (2/PHI**2)
    cu.vert_radius = cu.edge_radius = 0.01
    pd = PD() * half * sfactor # edges 1.08R... (volume 60S + 20s3)
    pd.vert_radius = pd.edge_radius = 0.01
    draw_poly(cu, out, v=True, e=True, f=True)
    draw_poly(pd, out, v=True, e=True, f=False)
    draw_poly(rd, out, v=True, e=True, f=False)
    out.close()

    out = open("gif8.pov", "w") 
    out.write(pov_header) 
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)     
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    rd = RD()
    rd.vert_radius = rd.edge_radius = 0.01
    rt = RT() * (1/rt2(2)) # 7.5 RT
    rt.vert_radius = rt.edge_radius = 0.01
    draw_poly(rd, out, v=True, e=True, f=False)
    draw_poly(octa, out, v=True, e=True, f=False)
    draw_poly(rt, out, v=True, e=True, f=False)
    out.close()

    out = open("gif9.pov", "w") 
    out.write(pov_header) 
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)     
    rd = RD()
    rd.vert_radius = rd.edge_radius = 0.01
    rt = RT() * (1/rt2(2)) # 7.5 RT
    rt.vert_radius = rt.edge_radius = 0.01
    draw_poly(rd, out, v=True, e=True, f=False)
    draw_poly(rt, out, v=True, e=True, f=False)
    out.close()
    
def test18():
    global S_1, S_2, S_3, S_6, s_1, s_2, s_3, s_6
    global RT_, IW_, RD_, PD_, OC_, CU_, TT_
    
    PHI  = sy.Symbol("PHI")
    
    S_1  = (PHI **-5)/2  
    S_3  = S_1 * PHI**3
    S_6  = S_3 * PHI**3
    s_1  = S_1
    s_3  = s_1 * PHI**-3
    s_6  = s_3 * PHI**-3
    
    RT_ =  60 * (  S_1 + s_3)
    IW_ =  20 * (3*S_1 + s_3)
    RD_ =  48 * (  S_1 + s_3)
    PD_ =  24 * (2*S_1 + s_3)
    OC_ =  32 * (  S_1 + s_3)
    CU_ =  24 * (  S_1 + s_3)
    TT_ =   8 * (  S_1 + s_3) 
    print(f"RT = {RT_} = {RT_.evalf(subs={PHI: (1+rt2(5))/2})}")
    print(f"IW = {IW_} = {IW_.evalf(subs={PHI: (1+rt2(5))/2})}")
    print(f"RD = {RD_} = {RD_.evalf(subs={PHI: (1+rt2(5))/2})}")
    print(f"PD = {PD_} = {PD_.evalf(subs={PHI: (1+rt2(5))/2})}")
    print(f"OC = {OC_} = {OC_.evalf(subs={PHI: (1+rt2(5))/2})}")
    print(f"CU = {CU_} = {CU_.evalf(subs={PHI: (1+rt2(5))/2})}")
    print(f"TT =  {TT_}  = {TT_.evalf(subs={PHI: (1+rt2(5))/2})}")

def test19():
    out = open("little_ch.pov", "w") 
    out.write(pov_header) 
    rt = RT() * half * sfactor 
    rt.edge_radius = 0.01
    rt.vert_radius = 0.01
    pd = PD() * half * sfactor
    pd.edge_radius = 0.01
    pd.vert_radius = 0.01
    iw = Icosahedron()  * half * sfactor
    iw.edge_radius = 0.01
    iw.vert_radius = 0.01
    octa = Octahedron()
    octa.edge_radius = 0.01
    octa.vert_radius = 0.01
    cu = Cube() * (2/(PHI**2))
    cu.edge_radius = 0.01
    cu.vert_radius = 0.01
    rd = RD() * (2/(PHI**2))
    rd.edge_radius = 0.01
    rd.vert_radius = 0.01
    tt = Tetrahedron() * (2/(PHI**2))
    tt.edge_radius = 0.01
    tt.vert_radius = 0.01
    draw_poly(rt, out, v=True, e=True, f=False)
    draw_poly(pd, out, v=True, e=True, f=True)
    #draw_poly(iw, out, v=True, e=True, f=False)
    # draw_poly(rd, out, v=True, e=True, f=False)
    #draw_poly(octa, out, v=True, e=True, f=True)
    draw_poly(cu, out, v=True, e=True, f=False)
    #draw_poly(tt, out, v=True, e=True, f=False)
    out.close()
    
def test20():
    out = open("gif1.pov", "w")
    out.write(pov_header)
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()
     
    out = open("gif2.pov", "w")
    out.write(pov_header)
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    rt = RT() # SuperRT
    rt.vert_radius = rt.edge_radius = 0.01
    draw_poly(rt, out, v=True, e=True, f=False)
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()

    out = open("gif3.pov", "w")
    out.write(pov_header)
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    rt = RT() * (1/PHI)
    rt.vert_radius = rt.edge_radius = 0.01
    draw_poly(rt, out, v=True, e=True, f=False)
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()    
    
    out = open("gif4.pov", "w")
    out.write(pov_header)
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    rt_t = RT() * (1/(3*rt2(2)))**(1/3)  # RT_T
    rt_t.vert_radius = rt_t.edge_radius = 0.01
    draw_poly(rt_t, out, v=True, e=True, f=False)
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()
    
    out = open("gif5.pov", "w")
    out.write(pov_header)
    rt_iw = RT() * half * sfactor  # RT_IW
    rt_iw.vert_radius = rt_iw.edge_radius = 0.01
    iw = Icosahedron() * half * sfactor # edges 1.08R... (volume 60S + 20s3)
    iw.vert_radius = iw.edge_radius = 0.01
    draw_poly(rt_iw, out, v=True, e=True, f=False)
    draw_poly(iw, out, v=True, e=True, f=True)
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()

    out = open("gif6.pov", "w")
    out.write(pov_header)
    rt =  RT() * (1/rt2(2)) # 7.5 RT
    rt.vert_radius = rt.edge_radius = 0.01
    rd = RD()
    rd.vert_radius = rd.edge_radius = 0.01
    draw_poly(rt, out, v=True, e=True, f=False)
    draw_poly(rd, out, v=True, e=True, f=False)
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    draw_poly(octa, out, v=True, e=True, f=True)
    out.close()

    out = open("gif7.pov", "w")
    out.write(pov_header)
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    rt =  RT() 
    rt.vert_radius = rt.edge_radius = 0.01
    icosa = Icosahedron()
    icosa.vert_radius = icosa.edge_radius = 0.01
    pd = PD()
    pd.vert_radius = pd.edge_radius = 0.01
    draw_poly(rt, out, v=True, e=True, f=False)
    draw_poly(icosa, out, v=True, e=True, f=False)
    draw_poly(pd, out, v=True, e=True, f=False)
    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    draw_poly(octa, out, v=True, e=True, f=False)
    out.close()

def test21():
    f = open("ivm_xyz_cube.pov", "w")
    f.write(pov_header)
    cu  = Cube() * 2
    tet = Tetrahedron() * 2
    cu2 = Cube() * rt2(2)
    cu2.edge_color = brown = "rgb <{}, {}, {}>".format(102/255, 51/255, 0)
    orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
    
    #origin = ORIGIN
    r_edge_cube = {
    'big_yellow'   : Vector((0,0,0)),
    'small_yellow' : Vector((1,1,1)),
    'small_blue'   : Vector((1,0,0)),
    'big_blue'     : Vector((0,1,1)),
    'small_green'  : Vector((0,1,0)),
    'big_green'    : Vector((1,0,1)),
    'small_red'    : Vector((0,0,1)),
    'big_red'      : Vector((1,1,0)),
    }  

    edge = Edge(r_edge_cube['big_yellow'], r_edge_cube['small_green'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['big_yellow'], r_edge_cube['small_blue'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['big_yellow'], r_edge_cube['small_red'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_yellow'], r_edge_cube['big_red'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_yellow'], r_edge_cube['big_blue'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_yellow'], r_edge_cube['big_green'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_red'], r_edge_cube['big_blue'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_red'], r_edge_cube['big_green'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_green'], r_edge_cube['big_red'])
    draw_edge(edge, brown, 0.01, f)    

    edge = Edge(r_edge_cube['small_green'], r_edge_cube['big_blue'])
    draw_edge(edge, brown, 0.01, f)  

    edge = Edge(r_edge_cube['small_blue'], r_edge_cube['big_green'])
    draw_edge(edge, brown, 0.01, f)    

    edge = Edge(r_edge_cube['small_blue'], r_edge_cube['big_red'])
    draw_edge(edge, brown, 0.01, f)  
    
    draw_vert(r_edge_cube['big_yellow'], c=' rgb <1,1,0>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_yellow'], c=' rgb <1,1,0>' , r=0.07, t=f)

    draw_vert(r_edge_cube['big_green'], c=' rgb <0,1,0>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_green'], c=' rgb <0,1,0>' , r=0.07, t=f)

    draw_vert(r_edge_cube['big_blue'], c=' rgb <0,0,1>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_blue'], c=' rgb <0,0,1>' , r=0.07, t=f)

    draw_vert(r_edge_cube['big_red'], c=' rgb <1,0,0>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_red'], c=' rgb <1,0,0>' , r=0.07, t=f)

    draw_vert(2*A, c = orange, r = 0.14, t=f) 
    draw_vert(2*B, c = orange, r = 0.14, t=f) 
    draw_vert(2*C, c = orange, r = 0.14, t=f) 
    draw_vert(2*D, c = orange, r = 0.14, t=f) 
    
    draw_poly(cu, f)
    draw_poly(tet, f)
    # draw_poly(cu2, f)
    f.close()

def test22():
    f = open("test22.pov", "w")
    f.write(pov_header)
    cu  = Cube() * 2
    tet = Tetrahedron() * 2
    orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
    brown = "rgb <{}, {}, {}>".format(102/255, 51/255, 0)
    
    #origin = ORIGIN
    r_edge_cube = {
    'big_yellow'   : Vector((0,0,0)),
    'small_yellow' : Vector((1,1,1)),
    'small_blue'   : Vector((1,0,0)),
    'big_blue'     : Vector((0,1,1)),
    'small_green'  : Vector((0,1,0)),
    'big_green'    : Vector((1,0,1)),
    'small_red'    : Vector((0,0,1)),
    'big_red'      : Vector((1,1,0)),
    }  

    edge = Edge(r_edge_cube['big_yellow'], r_edge_cube['small_green'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['big_yellow'], r_edge_cube['small_blue'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['big_yellow'], r_edge_cube['small_red'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_yellow'], r_edge_cube['big_red'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_yellow'], r_edge_cube['big_blue'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_yellow'], r_edge_cube['big_green'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_red'], r_edge_cube['big_blue'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_red'], r_edge_cube['big_green'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_green'], r_edge_cube['big_red'])
    draw_edge(edge, brown, 0.01, f)    

    edge = Edge(r_edge_cube['small_green'], r_edge_cube['big_blue'])
    draw_edge(edge, brown, 0.01, f)  

    edge = Edge(r_edge_cube['small_blue'], r_edge_cube['big_green'])
    draw_edge(edge, brown, 0.01, f)    

    edge = Edge(r_edge_cube['small_blue'], r_edge_cube['big_red'])
    draw_edge(edge, brown, 0.01, f)  
    
    draw_vert(r_edge_cube['big_yellow'], c=' rgb <1,1,0>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_yellow'], c=' rgb <1,1,0>' , r=0.07, t=f)

    draw_vert(r_edge_cube['big_green'], c=' rgb <0,1,0>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_green'], c=' rgb <0,1,0>' , r=0.07, t=f)

    draw_vert(r_edge_cube['big_blue'], c=' rgb <0,0,1>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_blue'], c=' rgb <0,0,1>' , r=0.07, t=f)

    draw_vert(r_edge_cube['big_red'], c=' rgb <1,0,0>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_red'], c=' rgb <1,0,0>' , r=0.07, t=f)

    #texture1 = "pigment { Col_Glass_Bluish }"
    #texture2 = "pigment { Col_Glass_Dark_Green }"
    #texture3 = "pigment { Col_Glass_Yellow }"
    #texture4 = "pigment { Col_Glass_Ruby }"

    draw_vert(2*A, c = orange, r = 0.14, t=f) 
    draw_vert(2*B, c = orange, r = 0.14, t=f) 
    draw_vert(2*C, c = orange, r = 0.14, t=f) 
    draw_vert(2*D, c = orange, r = 0.14, t=f)
    
    #draw_vert(2*A, texture1, r = 1, t=f, texture = True) 
    #draw_vert(2*B, texture2, r = 1, t=f, texture = True) 
    #draw_vert(2*C, texture3, r = 1, t=f, texture = True) 
    #draw_vert(2*D, texture4, r = 1, t=f, texture = True) 
    
    draw_poly(cu, f)
    draw_poly(tet, f)
    # draw_poly(cu2, f)
    f.close()

def test24():
    f = open("test_24.pov", "w")
    f.write(pov_header)
    oc  = Octahedron() * 2
    cu  = Cube() * 2
    tet = Tetrahedron() * 2
    rd = RD() * 2
    
    orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
    #brown = "rgb <{}, {}, {}>".format(102/255, 51/255, 0)

    #texture1 = "T_Copper_1A"
    texture2 = "T_Stone18"
    #texture2 = "pigment { Col_Glass_Dark_Green }"
    #texture3 = "pigment { Col_Glass_Yellow }"
    #texture4 = "pigment { Col_Glass_Ruby }"

    draw_vert(2*A, c = orange, r = 0.14, t=f) 
    draw_vert(2*B, c = orange, r = 0.14, t=f) 
    draw_vert(2*C, c = orange, r = 0.14, t=f) 
    draw_vert(2*D, c = orange, r = 0.14, t=f)
    
    draw_vert(ORIGIN, texture2, r = 1, t=f, texture = True) 
    #draw_vert(2*A, texture1, r = 1, t=f, texture = True)
    #draw_vert(2*B, texture2, r = 1, t=f, texture = True) 
    #draw_vert(2*C, texture1, r = 1, t=f, texture = True) 
    #draw_vert(2*D, texture2, r = 1, t=f, texture = True) 
    
    draw_poly(cu, f)
    draw_poly(tet, f)
    draw_poly(oc, f)
    draw_poly(rd, f)
    # draw_poly(cu2, f)
    f.close()

def test25():
    f = open("testing25.pov", "w")
    f.write(pov_header)

    # black = "rgb <{0}, {0}, {0}>".format(0)
    white = "rgb <{0}, {0}, {0}>".format(220/255)
    green = "rgb <0, 1, 0>"
    red   = "rgb <1, 0, 0>"
    blue  = "rgb <0, 0, 1>"
    yellow= "rgb <1, 1, 0>"
    tet = Tetrahedron()
    cu  = Cube()
    oc  = Octahedron() * (1/2)
    oc2 = Octahedron()
    rd  = RD()
    co  = Cuboctahedron()
    
    
    oc.edge_color = white
    oc.vert_color = white
    oc.vert_radius = 0.07
    
    # draw_vert(ORIGIN, c = black, r=0.07, t=f)
    draw_vert(ORIGIN, "T_Stone18", half, f, texture=True)
    
    draw_poly(cu, f)
    draw_poly(tet, f)
    draw_poly(oc, f)
    draw_poly(oc2, f)
    draw_poly(rd, f)
    draw_poly(co, f)

    draw_vert(A, c = green, r = 0.07, t=f) 
    draw_vert(B, c = blue, r = 0.07, t=f) 
    draw_vert(C, c = red, r = 0.07, t=f) 
    draw_vert(D, c = yellow, r = 0.07, t=f)
    f.close()

def test26():
    """
    // perspective (default) camera
    camera {
      location  <-2.5, 0.1, -0.4>
      rotate    <90.0, 0, -100>
      look_at   <0.0, 0.0,  0.0>
      right     x*image_width/image_height
    }
    """
    f = open("testing26.pov", "w")
    f.write(pov_header)

    #black = "rgb <{0}, {0}, {0}>".format(0)
    white = "rgb <{0}, {0}, {0}>".format(220/255)
    #green = "rgb <0, 1, 0>"
    red   = "rgb <1, 0, 0>"
    blue  = "rgb <0, 0, 1>"
    yellow= "rgb <1, 1, 0>"
    orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
    brown = "rgb <{}, {}, {}>".format(102/255, 51/255, 0)
    
    #tet = Tetrahedron() * 2
    cu  = Cube() * 2
    draw_poly(cu, f)
    # draw_poly(tet, f)
    
    rad = 0.01
    
    draw_edge(Edge(ORIGIN, Vector((1,0,0))), red, rad, t=f)
    draw_vert(Vector((1,0,0)), c=orange, r=0.07, t=f)
    draw_edge(Edge(ORIGIN, Vector((-1,0,0))), red, rad, t=f)
    
    draw_edge(Edge(ORIGIN, Vector((0,1,0))), blue, rad,  t=f)
    draw_vert(Vector((0,1,0)), c = orange, r=0.07, t=f)
    draw_edge(Edge(ORIGIN, Vector((0,-1,0))), blue, rad,  t=f)
    
    draw_edge(Edge(ORIGIN, Vector((0,0,1))), yellow, rad, t=f)
    draw_vert(Vector((0,0,1)), c = orange, r=0.07, t=f)    
    draw_edge(Edge(ORIGIN, Vector((0,0,-1))), yellow, rad, t=f)
    
    draw_edge(Edge(ORIGIN, 2 * Qvector((1,0,0,0))), red, rad,  t=f)
    draw_edge(Edge(ORIGIN, 2 * Qvector((0,1,0,0))), blue, rad,  t=f)
    draw_edge(Edge(ORIGIN, 2 * Qvector((0,0,1,0))), yellow, rad,  t=f)
    draw_edge(Edge(ORIGIN, 2 * Qvector((0,0,0,1))), white, rad, t=f)

    r_edge_cube = {
    'big_yellow'   : Vector((0,0,0)),
    'small_yellow' : Vector((1,1,1)),
    'small_blue'   : Vector((1,0,0)),
    'big_blue'     : Vector((0,1,1)),
    'small_green'  : Vector((0,1,0)),
    'big_green'    : Vector((1,0,1)),
    'small_red'    : Vector((0,0,1)),
    'big_red'      : Vector((1,1,0)),
    }  

    edge = Edge(r_edge_cube['big_yellow'], r_edge_cube['small_green'])
    #draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['big_yellow'], r_edge_cube['small_blue'])
    #draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['big_yellow'], r_edge_cube['small_red'])
    #draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_yellow'], r_edge_cube['big_red'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_yellow'], r_edge_cube['big_blue'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_yellow'], r_edge_cube['big_green'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_red'], r_edge_cube['big_blue'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_red'], r_edge_cube['big_green'])
    draw_edge(edge, brown, 0.01, f)

    edge = Edge(r_edge_cube['small_green'], r_edge_cube['big_red'])
    draw_edge(edge, brown, 0.01, f)    

    edge = Edge(r_edge_cube['small_green'], r_edge_cube['big_blue'])
    draw_edge(edge, brown, 0.01, f)  

    edge = Edge(r_edge_cube['small_blue'], r_edge_cube['big_green'])
    draw_edge(edge, brown, 0.01, f)    

    edge = Edge(r_edge_cube['small_blue'], r_edge_cube['big_red'])
    draw_edge(edge, brown, 0.01, f) 

    draw_vert(r_edge_cube['big_yellow'], c=' rgb <1,1,0>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_yellow'], c=' rgb <1,1,0>' , r=0.07, t=f)

    draw_vert(r_edge_cube['big_green'], c=' rgb <0,1,0>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_green'], c=' rgb <0,1,0>' , r=0.07, t=f)

    draw_vert(r_edge_cube['big_blue'], c=' rgb <0,0,1>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_blue'], c=' rgb <0,0,1>' , r=0.07, t=f)

    draw_vert(r_edge_cube['big_red'], c=' rgb <1,0,0>' , r=0.14, t=f)
    draw_vert(r_edge_cube['small_red'], c=' rgb <1,0,0>' , r=0.07, t=f)

    f.close()

def test27():
    f = open("testing27.pov", "w")
    f.write(pov_header)

    tet    = Tetrahedron()
    cu     = Cube()
    xyz_cu = Cube() * (1/rt2(2))
    cu2    = Cube() * 2

    draw_poly(tet, f)
    draw_poly(xyz_cu, f)
    draw_poly(cu, f)
    draw_poly(cu2, f)

def test28():
    f = open("testing28.pov", "w")
    f.write(pov_header)

    rt   = RT() * (1/PHI)
    rt.edge_radius = 0.02
    rt75 = RT() * (1/PHI) * 0.9994 * (3/2)**(1/3) # 7.5 RT_K
    rt75.edge_color = "rgb <{}, {}, {}>".format(1, 105/255, 180/255)
    rt75.edge_radius = 0.02
    rd    = RD()
    rd.edge_radius = 0.02
    
    draw_vert(ORIGIN, "T_Stone18", half, f, texture=True)
    draw_poly(rt, f)
    draw_poly(rt75, f)
    draw_poly(rd, f)
    
def test29():
    f = open("testing29.pov", "w")
    f.write(pov_header)

    rt   = RT()
    rt.edge_radius = 0.02
    ic   =  Icosahedron()
    ic.edge_radius = 0.02
    rd    = RD()
    rd.edge_radius = 0.02
    cu = Cuboctahedron()
    cu.edge_radius = 0.02
    pd    = PD()
    pd.edge_radius = 0.02
    
    draw_vert(ORIGIN, "T_Stone18", half, f, texture=True)
    draw_poly(rt, f)
    draw_poly(ic, f)
    # draw_poly(rd, f)
    # draw_poly(cu, f)
    draw_poly(pd, f)

def test30():
    f = open("testing30a.pov", "w")
    f.write(pov_header)

    #black = "rgb <{0}, {0}, {0}>".format(0)
    white = "rgb <{0}, {0}, {0}>".format(220/255)
    green = "rgb <0, 1, 0>"
    red   = "rgb <1, 0, 0>"
    blue  = "rgb <0, 0, 1>"
    yellow= "rgb <1, 1, 0>"
    orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
    brown = "rgb <{}, {}, {}>".format(102/255, 51/255, 0)

    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    octa.edge_radius = octa.edge_radius= 0.01
    draw_poly(octa, f, v=True, e=True, f=False)

    # draw_vert(octa.vertexes['i'], red, 0.05, f, texture=False)
    # draw_vert(octa.vertexes['j'], green, 0.05, f, texture=False)
    # draw_vert(octa.vertexes['k'], blue, 0.05, f, texture=False)
    # draw_vert(octa.vertexes['l'], yellow, 0.05, f, texture=False)
    # draw_vert(octa.vertexes['m'], orange, 0.05, f, texture=False)
    # draw_vert(octa.vertexes['n'], brown, 0.05, f, texture=False)
    
#                      ('z','s','t'),('t','y','v'),
#                      ('y','p','r'),('r','q','x'),
#                      ('x','u','v'),('u','s','w'),
#                      ('w','q','o'),('o','z','p'))    

    n = 0.2

    # ('z','s','t')
    # (o p q r s* t* u v w x y z*)
    
    co = Cuboctahedron() * (1/2)
    co.vert_radius = octa.edge_radius= 0.01
    co.edge_radius = octa.edge_radius= 0.01
    draw_poly(co, f, v=True, e=True, f=False) 

    # draw_vert(co.vertexes['z'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['s'], green, 0.05, f, texture=False)
    # draw_vert(co.vertexes['t'], blue, 0.05, f, texture=False)

    co.vertexes['z'] = co.vertexes['z'] + n * (co.vertexes['z'] - octa.vertexes['j'])
    co.vertexes['s'] = co.vertexes['s'] + n * (co.vertexes['s'] - octa.vertexes['n'])
    co.vertexes['t'] = co.vertexes['t'] + n * (co.vertexes['t'] - octa.vertexes['k'])

    # draw_poly(co, f, v=True, e=True, f=False)

    # draw_vert(co.vertexes['z'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['s'], green, 0.05, f, texture=False)
    # draw_vert(co.vertexes['t'], blue, 0.05, f, texture=False)

    # ('t','y','v')
    # (o p q r s* t* u v* w x y* z*)
    
    # draw_vert(co.vertexes['t'], blue, 0.05, f, texture=False)
    # draw_vert(co.vertexes['y'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['v'], green, 0.05, f, texture=False)

    # co.vertexes['t'] = co.vertexes['t'] + n * (co.vertexes['t'] - octa.vertexes['k'])
    co.vertexes['y'] = co.vertexes['y'] + n * (co.vertexes['y'] - octa.vertexes['m'])
    co.vertexes['v'] = co.vertexes['v'] + n * (co.vertexes['v'] - octa.vertexes['n'])

    # draw_vert(co.vertexes['t'], blue, 0.05, f, texture=False)
    # draw_vert(co.vertexes['y'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['v'], green, 0.05, f, texture=False)

    # ('o','z','p')
    # (o* p* q r s* t* u v* w x y* z*)

    # draw_vert(co.vertexes['o'], green, 0.05, f, texture=False)
    # draw_vert(co.vertexes['z'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['p'], blue, 0.05, f, texture=False)

    co.vertexes['o'] = co.vertexes['o'] + n * (co.vertexes['o'] - octa.vertexes['i'])
    # co.vertexes['z'] = co.vertexes['z'] + n * (co.vertexes['z'] - octa.vertexes['m'])
    co.vertexes['p'] = co.vertexes['p'] + n * (co.vertexes['p'] - octa.vertexes['k'])

    # draw_vert(co.vertexes['o'], green, 0.05, f, texture=False)
    # draw_vert(co.vertexes['z'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['p'], blue, 0.05, f, texture=False)

    # ('u','s','w')
    # (o* p* q r s* t* u* v* w* x y* z*)
    
    # draw_vert(co.vertexes['s'], green, 0.05, f, texture=False)
    # draw_vert(co.vertexes['u'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['w'], blue, 0.05, f, texture=False)

    # co.vertexes['s'] = co.vertexes['s'] + n * (co.vertexes['s'] - octa.vertexes['n'])
    co.vertexes['u'] = co.vertexes['u'] + n * (co.vertexes['u'] - octa.vertexes['l'])
    co.vertexes['w'] = co.vertexes['w'] + n * (co.vertexes['w'] - octa.vertexes['j'])

    # draw_vert(co.vertexes['s'], green, 0.05, f, texture=False)
    # draw_vert(co.vertexes['u'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['w'], blue, 0.05, f, texture=False)

    # ('x','u','v')
    # (o* p* q r s* t* u* v* w* x y* z*)
    
    # draw_vert(co.vertexes['x'], blue, 0.05, f, texture=False)
    # draw_vert(co.vertexes['u'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['v'], green, 0.05, f, texture=False)

    # co.vertexes['x'] = co.vertexes['x'] + n * (co.vertexes['x'] - octa.vertexes['m'])
    # co.vertexes['u'] = co.vertexes['u'] + n * (co.vertexes['u'] - octa.vertexes['l'])
    # co.vertexes['v'] = co.vertexes['v'] + n * (co.vertexes['v'] - octa.vertexes['j'])

    # draw_vert(co.vertexes['x'], blue, 0.05, f, texture=False)
    # draw_vert(co.vertexes['u'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['v'], blue, 0.05, f, texture=False)

    # ('r','q','x')
    # (o* p* q* r* s* t* u* v* w* x* y* z*)
    
    # draw_vert(co.vertexes['x'], blue, 0.05, f, texture=False)
    # draw_vert(co.vertexes['r'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['q'], green, 0.05, f, texture=False)

    co.vertexes['x'] = co.vertexes['x'] + n * (co.vertexes['x'] - octa.vertexes['m'])
    co.vertexes['r'] = co.vertexes['r'] + n * (co.vertexes['r'] - octa.vertexes['i'])
    co.vertexes['q'] = co.vertexes['q'] + n * (co.vertexes['q'] - octa.vertexes['l'])

    # draw_vert(co.vertexes['x'], blue, 0.05, f, texture=False)
    # draw_vert(co.vertexes['r'], red, 0.05, f, texture=False)
    # draw_vert(co.vertexes['q'], green, 0.05, f, texture=False)

    f = open("testing30b.pov", "w")
    f.write(pov_header)
    co.edges = co._distill()

    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    octa.edge_radius = octa.edge_radius= 0.01
    draw_poly(octa, f, v=True, e=True, f=False)

    draw_poly(co, f, v=True, e=True, f=False) 
    f.close()

    f = open("testing30c.pov", "w")
    f.write(pov_header)
    co.edges = co._distill()

    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    octa.edge_radius = octa.edge_radius= 0.01
    draw_poly(octa, f, v=True, e=True, f=False)

    ic = Icosahedron() * half * sfactor # D=1 (volume 60S + 20s3)
    ic.vert_radius = octa.edge_radius= 0.01
    ic.edge_radius = octa.edge_radius= 0.01
    
    draw_poly(ic, f, v=True, e=True, f=False) 
    f.close()

def test31():
    #black = "rgb <{0}, {0}, {0}>".format(0)
    white = "rgb <{0}, {0}, {0}>".format(220/255)
    green = "rgb <0, 1, 0>"
    red   = "rgb <1, 0, 0>"
    blue  = "rgb <0, 0, 1>"
    yellow= "rgb <1, 1, 0>"
    orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
    brown = "rgb <{}, {}, {}>".format(102/255, 51/255, 0)
    
    f = open("testing31_0.pov", "w")
    f.write(pov_header)

    octa = Octahedron()
    octa.vert_radius = octa.edge_radius= 0.01
    octa.edge_radius = octa.edge_radius= 0.01
    draw_poly(octa, f, v=True, e=True, f=False)

    co = Cuboctahedron() * (1/2)
    co.vert_radius = octa.edge_radius= 0.01
    co.edge_radius = octa.edge_radius= 0.01
    draw_poly(co, f, v=True, e=True, f=False) 

    #  ('z','s','t'),('t','y','v'),
    #  ('y','p','r'),('r','q','x'),
    #  ('x','u','v'),('u','s','w'),
    #  ('w','q','o'),('o','z','p'))    

    # ('z','s','t')
    # (o p q r s* t* u v w x y z*)
    for idx, n in enumerate(np.arange(0, 1.1, 0.1), 1):

        if idx > 3:
            idx += 1
            
        f = open(f"testing31_{idx}.pov", "w")
        f.write(pov_header)

        co = Cuboctahedron() * (1/2)
        co.vert_radius = octa.edge_radius= 0.01
        co.edge_radius = octa.edge_radius= 0.01
   
        co.vertexes['z'] = co.vertexes['z'] + n * (co.vertexes['z'] - octa.vertexes['j'])
        co.vertexes['s'] = co.vertexes['s'] + n * (co.vertexes['s'] - octa.vertexes['n'])
        co.vertexes['t'] = co.vertexes['t'] + n * (co.vertexes['t'] - octa.vertexes['k'])
        co.vertexes['y'] = co.vertexes['y'] + n * (co.vertexes['y'] - octa.vertexes['m'])
        co.vertexes['v'] = co.vertexes['v'] + n * (co.vertexes['v'] - octa.vertexes['n'])
        co.vertexes['o'] = co.vertexes['o'] + n * (co.vertexes['o'] - octa.vertexes['i'])
        co.vertexes['p'] = co.vertexes['p'] + n * (co.vertexes['p'] - octa.vertexes['k'])
        co.vertexes['u'] = co.vertexes['u'] + n * (co.vertexes['u'] - octa.vertexes['l'])
        co.vertexes['w'] = co.vertexes['w'] + n * (co.vertexes['w'] - octa.vertexes['j'])
        co.vertexes['x'] = co.vertexes['x'] + n * (co.vertexes['x'] - octa.vertexes['m'])
        co.vertexes['r'] = co.vertexes['r'] + n * (co.vertexes['r'] - octa.vertexes['i'])
        co.vertexes['q'] = co.vertexes['q'] + n * (co.vertexes['q'] - octa.vertexes['l'])
        
        co.edges = co._distill()

        octa = Octahedron()
        octa.vert_radius = octa.edge_radius= 0.01
        octa.edge_radius = octa.edge_radius= 0.01
        draw_poly(octa, f, v=True, e=True, f=False)
        
        if idx == 3:
            ic = Icosahedron() * half * sfactor # D=1 (volume 60S + 20s3)
            ic.vert_radius = octa.edge_radius= 0.01
            ic.edge_radius = octa.edge_radius= 0.01
            draw_poly(ic, f, v=True, e=True, f=False) 
        else:
            draw_poly(co, f, v=True, e=True, f=False) 
        
        f.close()

def test32():
    with open("testing32.pov", "w") as f:
        f.write(pov_header)
    
        cu      = Cube()
        cu.vert_radius = 0.01
        cu.edge_radius = 0.01
        
        octa    = Octahedron() * (3/4) 
        octa.vert_radius = 0.01
        octa.edge_radius = 0.01
    
        draw_poly(cu, f)
        draw_poly(octa, f, f=True)
    
def test33():
    with open("testing33.pov", "w") as f:
        f.write(pov_header)
    
        rt      = RT()
        rt.vert_radius = 0.01
        rt.edge_radius = 0.01
        red   = "rgb <1, 0, 0>"
        
        for face in rt.faces:
            face_center = (  rt.vertexes[face[0]] 
                           + rt.vertexes[face[1]] 
                           + rt.vertexes[face[2]] 
                           + rt.vertexes[face[3]]) / 4 
            tentpole = face_center * 1.05 #just a little longer
            for i in range(len(face)):
                draw_edge(Edge(tentpole, rt.vertexes[face[i]]), 
                          red, rt.edge_radius, f)
        
        draw_poly(rt, f, f=True) # the whole rt
        
def test34():
    """
    verbose comments for practice...
    """ 
    # we're gonna use this as our output textfile
    # which'll be something povray can eat and make
    # a PNG out of.
    with open("testing34.pov", "w") as f:
        f.write(pov_header)        # boilerplate povray, lotsa lines
    
        cu3 = Cube()               # birth a cube in the Matryoshka context
        cu3.vert_radius = 0.01     # override default vertex radius
        cu3.edge_radius = 0.01     # override edge cylinder radius
        
        cu24 = Cube() * 2          # birth a cube but scale up all edges x2
        cu24.vert_radius = 0.01    # ergo volume is boosted 8-fold from
        cu24.edge_radius = 0.01    # 3 to 24 (cu3 vs cu24 refers to volume)
        
        octa = Octahedron()        # red by default, dual of cu3
        octa.vert_radius = 0.01
        octa.edge_radius = 0.01
        
        tet = Tetrahedron()        # orange by default, inverse tet is black
        tet.vert_radius = 0.01     # appears as face diagonals of cu3
        tet.edge_radius = 0.01

        # here is where we actually commit the polys to the open textfile
        draw_poly(cu3, f, f=False)
        draw_poly(cu24, f, f=False)        
        draw_poly(octa, f, f=False)
        draw_poly(tet, f, f=True)  # the only one with filled-in faces     
       
    # output file is closed automatically here, as
    # indentation block is finished
        
def test35():
    with open("testing35.pov", "w") as f:
        f.write(pov_header)
    
        draw_vert(ORIGIN, "T_Stone18", half, f, texture=True)
        
        cu3 = Cube()
        cu3.vert_radius = 0.01
        cu3.edge_radius = 0.01
        
        cu24 = Cube() * 2
        cu24.vert_radius = 0.01
        cu24.edge_radius = 0.01
        
        octa = Octahedron()  # red
        octa.vert_radius = 0.01
        octa.edge_radius = 0.01
        
        draw_poly(cu3, f, f=False)
        draw_poly(cu24, f, f=False)        
        draw_poly(octa, f, f=False)
 

def test36():
    with open("testing36.pov", "w") as f:
        f.write(pov_header)
    
        draw_vert(ORIGIN, "T_Stone18", half, f, texture=True)
        
        cu3 = Cube()
        cu3.vert_radius = 0.01
        cu3.edge_radius = 0.01
        
        cu24 = Cube() * 2
        cu24.vert_radius = 0.01
        cu24.edge_radius = 0.01
        
        rd = RD()  # red
        rd.vert_radius = 0.01
        rd.edge_radius = 0.01
        
        draw_poly(cu3, f, f=False)
        draw_poly(cu24, f, f=False)        
        draw_poly(rd, f, f=False)
        
def test37():
    with open("testing37.pov", "w") as f:
        f.write(pov_header)
        
        cu = Cube()
        cu.vert_radius = 0.01
        cu.edge_radius = 0.01
        
        orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
        
        draw_edge(Edge(ORIGIN, A), r=0.01, c=orange, t=f)
        draw_edge(Edge(ORIGIN, B), r=0.01, c=orange, t=f)
        draw_edge(Edge(ORIGIN, C), r=0.01, c=orange, t=f)
        draw_edge(Edge(ORIGIN, D), r=0.01, c=orange, t=f)
        
        draw_poly(cu, f)

def test38():
    with open("testing38.pov", "w") as f:
        f.write(pov_header)       
        cu = Cube()
        cu.vert_radius = 0.01
        cu.edge_radius = 0.01   
        tet = Tetrahedron()
        tet.vert_radius = 0.01
        tet.edge_radius = 0.01 
        rd = RD()
        rd.vert_radius = 0.01
        rd.edge_radius = 0.01 
        ve = Cuboctahedron()
        ve.vert_radius = 0.01
        ve.edge_radius = 0.01  
        oc = Octahedron()
        oc.vert_radius = 0.01
        oc.edge_radius = 0.01
        orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
        cubes = []
        spherics = []
        
        draw_vert(ORIGIN, "T_Stone18", half, f, texture=True)
        for v in IVM_DIRS:
            # draw_edge(Edge(ORIGIN, v), r=0.01, c=orange, t=f)           
            cube = Cube() + v
            cube.vert_radius = 0.01
            cube.edge_radius = 0.01            
            spheric = RD() + v
            spheric.vert_radius = 0.01
            spheric.edge_radius = 0.01
            
            cubes.append(cube)
            spherics.append(spheric)
            
            # draw_vert(v, "T_Stone18", half/4, f, texture=True)
        
        draw_poly(cu, f)
        #for cube in cubes:
        #    draw_poly(cube, f) 
        # draw_poly(tet, f, f=True, e=True)
        draw_poly(ve, f)
        draw_poly(oc, f) 
        draw_poly(rd, f)
        #for spheric in spherics:
        #    draw_poly(spheric, f)

def test39():
    with open("testing39.pov", "w") as f:
        f.write(pov_header)
        cu = Cube()
        cu.vert_radius = 0.01
        cu.edge_radius = 0.01
        cu2 = Cube() + (A+B)
        cu2.vert_radius = 0.01
        cu2.edge_radius = 0.01
        orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
        rd = RD() + (A+B)
        rd.vert_radius = 0.05
        rd.edge_radius = 0.02  
        rd.edge_color = "T_Silver_3A"
        rd.vert_color = 'T_Copper_1A'
        
        m = Mite()
        m.vert_radius = 0.01
        m.edge_radius = 0.03
        # m.face_color = "T_Stone18"
        m.edge_color = orange
        # m.vert_color = 'T_Copper_1A'

        draw_poly(cu, f)
        draw_poly(cu2, f)
        draw_poly(m, f)
        draw_poly(rd, f, texture=True)
        
def test40():
    with open("testing40.pov", "w") as f:
        f.write(pov_header)
        cu = Cube()
        cu.vert_radius = 0.01
        cu.edge_radius = 0.01
        cu2 = Cube() * 2
        cu2.vert_radius = 0.01
        cu2.edge_radius = 0.01
        rd = RD()
        rd.vert_radius = 0.01
        rd.edge_radius = 0.01  
        
        rds = []
        for k, v in cu2.vertexes.items():
            newrd = RD() + v
            newrd.vert_radius = 0.01
            newrd.edge_radius = 0.01            
            rds.append(newrd)
            
        draw_poly(cu, f)
        draw_poly(cu2, f)
        draw_poly(rd, f)        
        #for rd in rds:
        #    draw_poly(rd, f) 
        draw_poly(rds[0], f)           

def test41():
    with open("testing41.pov", "w") as f:
        f.write(pov_header)
        cu = Cube()
        cu.vert_radius = 0.01
        cu.edge_radius = 0.01
        cu2 = Cube() * 2
        cu2.vert_radius = 0.01
        cu2.edge_radius = 0.01
        oc = Octahedron() 
        oc.vert_radius = 0.01
        oc.edge_radius = 0.01
        
        orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
        brown  = "rgb <{}, {}, {}>".format(102/255, 51/255, 0)
        yellow = "rgb <1, 1, 0>"   
        red    = "rgb <1, 0, 0>"
        green  = "rgb <0, 1, 0>"
        blue   = "rgb <0, 0, 1>"
        
        # +X +Y +Z
        X = Edge(ORIGIN, Vector((1,0,0)))
        Y = Edge(ORIGIN, Vector((0,1,0)))
        Z = Edge(ORIGIN, Vector((0,0,1)))

        draw_edge(X, orange, 0.01, f)
        draw_edge(Y, orange, 0.01, f)
        draw_edge(Z, orange, 0.01, f)  
        
        draw_vert(Vector((1,0,0)), red,   0.03, f)
        draw_vert(Vector((0,1,0)), green, 0.03, f)
        draw_vert(Vector((0,0,1)), blue,  0.03, f)
        
        # -X -Y -Z
        X = Edge(ORIGIN, Vector((-1,0,0)))
        Y = Edge(ORIGIN, Vector((0,-1,0)))
        Z = Edge(ORIGIN, Vector((0,0,-1)))

        draw_edge(X, yellow, 0.01, f)
        draw_edge(Y, yellow, 0.01, f)
        draw_edge(Z, yellow, 0.01, f)
        
        # four quadrays
        a = Edge(ORIGIN, Qvector((1,0,0,0)))
        b = Edge(ORIGIN, Qvector((0,1,0,0)))
        c = Edge(ORIGIN, Qvector((0,0,1,0)))
        d = Edge(ORIGIN, Qvector((0,0,0,1)))

        draw_vert(Qvector((1,0,0,0)), red,     0.03, f)
        draw_vert(Qvector((0,1,0,0)), green,   0.03, f)
        draw_vert(Qvector((0,0,1,0)), blue,    0.03, f)
        draw_vert(Qvector((0,0,0,1)), yellow,  0.03, f)
        
        draw_edge(a, brown, 0.02, f)
        draw_edge(b, brown, 0.02, f)
        draw_edge(c, brown, 0.02, f)
        draw_edge(d, brown, 0.02, f)

        draw_poly(cu, f)
        draw_poly(cu2, f)
        # draw_poly(oc, f)

def test42():
    from random import choice
    from tetravolume import Tetrahedron
    
    with open("testing42.pov", "w") as T:
        T.write(pov_header)
        twelve_directions = list(IVM_DIRS)
        
        # orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
        brown  = "rgb <{}, {}, {}>".format(102/255, 51/255, 0)
        yellow = "rgb <1, 1, 0>"   
        red    = "rgb <1, 0, 0>"
        green  = "rgb <0, 1, 0>"
        blue   = "rgb <0, 0, 1>"
        
        # define the four turtles at their common origin
        turtles = [RD(), RD(), RD(), RD()]
        turtles[0].edge_color = red
        turtles[1].edge_color = green
        turtles[2].edge_color = blue
        turtles[3].edge_color = yellow
        
        # draw the turtles in their initial position
        for t in turtles:
            draw_poly(t, T)
        
        # wander off, choosing randomly from 12 directions
        for _ in range(10):
            for idx in range(len(turtles)):
                t = turtles[idx]
                keep_color = t.edge_color
                turtles[idx] = t + choice(twelve_directions)
                turtles[idx].edge_color = keep_color
                # draw_poly(turtles[idx], T)

        # draw the turtles in their final positions
        for t in turtles:
            draw_poly(t, T)
                            
        # connect the final positions of the four turtles into a tet
        a = Edge(turtles[0].center, turtles[1].center)
        b = Edge(turtles[0].center, turtles[2].center)
        c = Edge(turtles[0].center, turtles[3].center)
        d = Edge(turtles[1].center, turtles[2].center)
        e = Edge(turtles[2].center, turtles[3].center)
        f = Edge(turtles[3].center, turtles[1].center)
        
        # draw the tet
        draw_edge(a, brown, 0.05, T)
        draw_edge(b, brown, 0.05, T)
        draw_edge(c, brown, 0.05, T)
        draw_edge(d, brown, 0.05, T)
        draw_edge(e, brown, 0.05, T)
        draw_edge(f, brown, 0.05, T)
        
        # compute the volume of the tet
        tet = Tetrahedron(a.length(), 
                          b.length(), 
                          c.length(), 
                          d.length(), 
                          e.length(), 
                          f.length())
        
        # report the volume
        print("Tet volume:", tet.ivm_volume())             

def test43():
    with open("testing43.pov", "w") as T:
        T.write(pov_header)
        
        rd = RD()
        co = Cuboctahedron() * half
        
        draw_poly(rd, T)
        draw_poly(co, T)
        
def test45():
    with open("testing45.pov", "w") as T:
        T.write(pov_header)
        
        rd = RD()
        rt_e = RT() * (1/PHI)   # RT_E
        # rt_75 = RT() * (1/(3*rt2(2)))**(1/3) * (3/2)**(1/3) # RT 7.5

        rd.vert_radius = 0.01
        rd.edge_radius = 0.01
        
        rt_e.vert_radius = 0.01
        rt_e.edge_radius = 0.01
        
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)        
        draw_poly(rd, T)
        draw_poly(rt_e, T)

def test46():
    """
    S3 + S6 = RegTet (tvs)
    
    Where would we slice the Regtet parallel to a face
    such that apex volume = S3, fustrum volume = S6 
    or.. apex volume = S6 and fustrum volume = S3?
    
    After computing these two slice locations, make 
    the corresponding POV-ray renderings.
    
    """
    print("Svol:", Svol)
    S3 = Svol * PHI**3
    apex_edge_S3 = S3 ** sy.Rational(1,3)
    print("S3 apex tet edges:", apex_edge_S3.evalf())
    
    S6 = Svol * PHI**6
    apex_edge_S6 = S6 ** sy.Rational(1,3)
    print("S6 apex tet edges:", apex_edge_S6.evalf())
    
    with open("testing46a.pov", "w") as T:
        T.write(pov_header)
        T.write(CLOSEUP)
        
        RegTet = Tetrahedron() 
        RegTet.face_color = "T_Stone17"
        RegTet.edge_color = "T_Copper_1A"
        RegTet.edge_radius = 0.01
        
        # S3 is apex tet, leaving a fat fustrum for the bigger volume S6
        S3_tet = Tetrahedron() * apex_edge_S3
        print("S3_tet volume:", S3_tet.volume.evalf())
        print("S3:", S3.evalf())

        shift = RegTet.vertexes['a'] - S3_tet.vertexes['a']
        S3_tet = S3_tet + shift # align apex vertexes of both tets
        S3_tet = S3_tet * 1.005 # inflate very slightly so texture will appear
        
        S3_tet.face_color = "T_Stone18"
        S3_tet.edge_color = "T_Copper_1A"
        S3_tet.edge_radius = 0.01
        
        draw_poly(S3_tet, T, v=False, e=False, f=True, texture=True) 
        draw_poly(RegTet, T, v=False, e=True, f=True, texture=True) 

    with open("testing46b.pov", "w") as T:
        T.write(pov_header)
        T.write(CLOSEUP)
        
        RegTet = Tetrahedron()
        RegTet.face_color = "T_Stone18"
        RegTet.edge_color = "T_Copper_1A"
        RegTet.edge_radius = 0.01
        
        # S6 is apex tet, leaving a thin fustrum for the smaller volume S3
        S6_tet = Tetrahedron() * apex_edge_S6
        print("S6_tet volume:", S6_tet.volume.evalf())
        print("S6:", S6.evalf())

        shift = RegTet.vertexes['a'] - S6_tet.vertexes['a']
        S6_tet = S6_tet + shift
        S6_tet = S6_tet * 1.005 
        
        S6_tet.face_color = "T_Stone17"
        S6_tet.edge_color = "T_Copper_1A"
        S6_tet.edge_radius = 0.01
        
        draw_poly(S6_tet, T, v=False, e=False, f=True, texture=True) 
        draw_poly(RegTet, T, v=False, e=True, f=True, texture=True) 

        print("S3 + S6:", S3.evalf() + S6.evalf())

def test47():
    """
    S3 + S6 = RegTet (tvs)
    
    Here we're partitioning a regular tet into two
    tets each with 60-60-60 degree angles. We'll put a 
    sliding point on a shared edge such that computing 
    tetravolume requires simply multiplying the three 
    edges stemming from those angles.
    
    """
    orange  = "rgb <{}, {}, {}>".format(1, 165/255, 0)
    red     = "rgb <{}, {}, {}>".format(1, 0, 0)
    green   = "rgb <{}, {}, {}>".format(0, 1, 0) 
    blue    = "rgb <{}, {}, {}>".format(0, 0, 1)
    yellow  = "rgb <{}, {}, {}>".format(1, 1, 0)
    magenta = "rgb <{}, {}, {}>".format(1, 0, 1)
    black   = "rgb <{}, {}, {}>".format(0, 0, 0)
    purple  = "rgb <{}, {}, {}>".format(0, 128/255, 128/255)
    cyan    =  "rgb <{}, {}, {}>".format(0, 1, 1)
    pink    =  "rgb <{}, {}, {}>".format(1, 105/255, 180/255)
    brown   =  "rgb <{}, {}, {}>".format(160/255, 82/255, 45/255)
    salmon  =  "rgb <{}, {}, {}>".format(1, 140/255, 105/255)
    grey    =  "rgb <{}, {}, {}>".format(128/255, 128/255, 128/255)  
        
    # S6 length
    ps6 = A - (A-B) * Svol * PHI**6
    e1_s6 = Edge(A, D) # 1
    e2_s6 = Edge(A, C) # 1
    e3_s6 = Edge(A, ps6) # volume of S6
    e4_s6 = Edge(D, ps6)
    e5_s6 = Edge(C, ps6)
    e6_s6 = Edge(C, D) # 1
    
    S6vol = e1_s6.length() * e2_s6.length() * e3_s6.length()
    print("S6vol:", S6vol.simplify())
    print("S6vol:", S6vol.evalf())
    print("AD:", e1_s6.length())
    print("AC:", e2_s6.length())
    print("Ap:", e3_s6.length().evalf())
    print("Dp:", e4_s6.length())
    print("Cp:", e5_s6.length())
    print("CD:", e6_s6.length())

    # S3 lengths
    ps3 = B - (B-A) * Svol * PHI**3
    e1_s3 = Edge(B, D) # 1
    e2_s3 = Edge(B, C)
    e3_s3 = Edge(B, ps3) # volume of S3
    e4_s3 = Edge(C, ps3) 
    e5_s3 = Edge(D, ps3) 
    e6_s3 = Edge(C, D)
    
    S3vol = e1_s3.length() * e2_s3.length() * e3_s3.length()
    print("S3vol:", S3vol.simplify())
    print("S3vol:", S3vol.evalf())
    print("BD:", e1_s3.length())
    print("BC:", e2_s3.length())
    print("Bp:", e3_s3.length().evalf())
    
    print()
    
    print("Total volume:", (S3vol + S6vol).evalf())
    
    with open("testing47.pov", "w") as T:
        T.write(pov_header)
        T.write(BRYG)
       
        def regtet():
            draw_vert(A, red, 0.03, T)
            draw_vert(B, green, 0.03, T)
            draw_vert(C, blue, 0.03, T)
            draw_vert(D, yellow, 0.03, T)
        
            draw_edge(Edge(A,B), green, 0.01, T)
            draw_edge(Edge(A,C), green, 0.01, T)
            draw_edge(Edge(A,D), green, 0.01, T)
            draw_edge(Edge(B,C), green, 0.01, T)
            draw_edge(Edge(C,D), green, 0.01, T)
            draw_edge(Edge(D,B), green, 0.01, T)        
            draw_vert(ps6, magenta, 0.03, T)
            draw_vert(ps3, magenta, 0.03, T)
            
        def draw_S6():
            #draw_edge(e1_s6, orange, 0.02, T)
            #draw_edge(e2_s6, orange, 0.02, T)
            #draw_edge(e3_s6, orange, 0.02, T)
            #draw_vert(ps6, blue, 0.03, T)
            draw_edge(e4_s6, orange, 0.01, T)
            draw_edge(e5_s6, orange, 0.01, T)
            draw_edge(e6_s6, orange, 0.01, T)

        def draw_S3():
            draw_edge(e1_s3, red, 0.01, T)
            draw_edge(e2_s3, red, 0.01, T)
            draw_edge(e3_s3, red, 0.01, T)
            draw_vert(ps3, blue, 0.03, T)
            draw_edge(e4_s3, red, 0.01, T)
            draw_edge(e5_s3, red, 0.01, T)
            draw_edge(e6_s3, red, 0.01, T)
        
        regtet()
        draw_S6()
        # draw_S3()
        
if __name__ == "__main__":
    test47()