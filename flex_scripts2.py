#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thurs Feb 13 2025

@author: mac

Feb 19: import PHI as sympy object vs using math.sqrt and dumbing it down too early
"""
from flextegrity import pov_header, Cuboctahedron, Cube, Octahedron
from flextegrity import Tetrahedron, InvTetrahedron, RD, Icosahedron, Struts
from flextegrity import twelve_around_one, draw_poly, draw_vert, half, ORIGIN, PHI
from qrays import Qvector
from itertools import cycle

import os
import numpy as np
import math

from itertools import permutations
g = permutations((2,1,1,0))
UNIQUE = {p for p in g}  # set comprehension

IVM_DIRS = {Qvector(x) for x in UNIQUE}

Svol = (PHI **-5)/2  
Evol = (math.sqrt(2)/8) * (PHI ** -3)

sfactor = Svol/Evol

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

if __name__ == "__main__":
    test31()