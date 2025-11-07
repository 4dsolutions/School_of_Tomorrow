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
from mpmath import radians

from itertools import permutations
g = permutations((2,1,1,0))
UNIQUE = {p for p in g}  # set comprehension

IVM_DIRS = {Qvector(x) for x in UNIQUE}

Svol = (PHI **-5)/2  
Evol = (rt2(2)/8) * (PHI ** -3)

sfactor = Svol/Evol

CLOSEUP = \
"""
   
// perspective (default) camera
camera {
  location  <3, 0.1, 0.2>
  rotate    <90, 0, 47.0>
  look_at   <0.0, 0.0,  0.0>
  right     x*image_width/image_height
}

"""

def test1():

    brown  = "rgb <{}, {}, {}>".format(102/255, 51/255, 0)
    green  = "rgb <0, 1, 0>"
    blue   = "rgb <0, 0, 1>"
 
    with open("rotate.pov", "w") as T:
        T.write(pov_header)

        tip = Qvector((0,1,1,2))
        x_spoke = Qvector((1,0,0,0))
        draw_edge(Edge(ORIGIN, x_spoke), blue, 0.03, T)

        for degrees in range(360):
            newtip = tip.qrotA(degrees)
            edge = Edge(ORIGIN, newtip)
            draw_edge(edge, brown, 0.03, T)
            draw_vert(newtip, c=green , r=0.03, t=T)

def test2():

    tet    = Tetrahedron()
    invtet = InvTetrahedron()
    cube   = Cube()
    octa   = Octahedron()
    rd     = RD()         # hug ball
    cubocta= Cuboctahedron()
    icosa  = Icosahedron()
    pd     = PD()
    rt     = RT() * (1/PHI) # hug ball

    thickness: float = 0.03    
    for shape in tet, invtet, cube, octa, rd, cubocta, icosa, pd, rt:
        shape.edge_radius = thickness
    
    with open("nh00.pov", "w") as T:
        "just ivm ball"
        T.write(pov_header)
        T.write(CLOSEUP)
        
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)
        
    with open("nh01.pov", "w") as T:
        "orange tet"
        T.write(pov_header)
        T.write(CLOSEUP)

        draw_poly(tet, T)        

    with open("nh02.pov", "w") as T:
        "orange + black tet"
        T.write(pov_header) 
        T.write(CLOSEUP)

        draw_poly(tet, T)
        draw_poly(invtet, T)
        
    with open("nh03.pov", "w") as T:
        "orange + black tet + green_cube"
        T.write(pov_header) 
        T.write(CLOSEUP)

        draw_poly(tet, T)
        draw_poly(invtet, T)
        draw_poly(cube, T)
        
    with open("nh04.pov", "w") as T:
        "orange + black tet + green_cube + red_oct"
        T.write(pov_header)
        T.write(CLOSEUP)

        draw_poly(tet, T)
        draw_poly(invtet, T)
        draw_poly(cube, T)
        draw_poly(octa, T)
        
    with open("nh05.pov", "w") as T:
        "orange + black tet + green_cube + red_oct + blue_RD"
        T.write(pov_header)        
        T.write(CLOSEUP)

        draw_poly(tet, T)
        draw_poly(invtet, T)
        draw_poly(cube, T)
        draw_poly(octa, T)
        draw_poly(rd, T)
        
    with open("nh06.pov", "w") as T:
        "orange + black tet + green_cube + red_oct + blue_RD + yellow_CO"
        T.write(pov_header)
        T.write(CLOSEUP)

        draw_poly(tet, T)
        draw_poly(invtet, T)
        draw_poly(cube, T)
        draw_poly(octa, T)
        draw_poly(rd, T)
        draw_poly(cubocta, T)
        
    with open("nh07.pov", "w") as T:
        "yellow_CO + cyan_icosa"
        T.write(pov_header)
        T.write(CLOSEUP)

        draw_poly(cubocta, T)
        draw_poly(icosa, T)
        
    with open("nh08.pov", "w") as T:
        "yellow_CO + cyan_icosa + brown_PD"
        T.write(pov_header) 
        T.write(CLOSEUP)

        draw_poly(cubocta, T)
        draw_poly(icosa, T)
        draw_poly(pd, T)
        
    with open("nh09.pov", "w") as T:
        "yellow_CO + cyan_icosa + brown_PD + purple_RT"
        T.write(pov_header)
        T.write(CLOSEUP)

        draw_poly(cubocta, T)
        draw_poly(icosa, T)
        draw_poly(pd, T)
        draw_poly(rt, T)     
        
    with open("nh10.pov", "w") as T:
        "purple_RT + ball"
        T.write(pov_header)
        T.write(CLOSEUP)

        draw_poly(rt, T) 
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)        

    with open("nh11.pov", "w") as T:
        "just ivm ball"
        T.write(pov_header)
        T.write(CLOSEUP)
        
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)


def test3():

    tet    = Tetrahedron()
    invtet = InvTetrahedron()

    thickness: float = 0.03    
    for shape in tet, invtet:
        shape.edge_radius = thickness
        
    with open("test_shot.pov", "w") as T:
        "orange + black tet"
        T.write(pov_header) 
        T.write(CLOSEUP)

        draw_poly(tet, T)
        draw_poly(invtet, T)

def test4():
    """
    [(0, 'sin', 'cos', 0),
     ('sin', 0, 'cos', 0),
     (0, 'sin', 0, 'cos'),
     ('sin', 'cos', 0, 0),
     ('sin', 0, 0, 'cos'),
     (0, 0, 'sin', 'cos')]
    """

    green   = "rgb <0, 1, 0>"
    orange  = "rgb <{}, {}, {}>".format(1, 128/255, 0)
    black   = "rgb <0, 0, 0>"
    red     = "rgb <1, 0, 0>"
    blue    = "rgb <0, 0, 1>"
    yellow  = "rgb <1, 1, 0>"
    brown   = "rgb <{}, {}, {}>".format(102/255, 51/255, 0)
    magenta = "rgb <{}, {}, {}>".format(1, 0, 1)
    purple  = "rgb <{}, {}, {}>".format(0, 128/255, 128/255)
    cyan    =  "rgb <{}, {}, {}>".format(0, 1, 1)
    pink    =  "rgb <{}, {}, {}>".format(1, 105/255, 180/255)
    
    cu = Cube()
    cu.edge_radius = 0.03
    
    oc = Octahedron()
    oc.edge_radius = 0.03
    
    with open("trig_test.pov", "w") as T:
        T.write(pov_header)
        # T.write(CLOSEUP)
        
        #draw_edge(Edge(ORIGIN, A), black, 0.03, T)
        #draw_edge(Edge(ORIGIN, B), black, 0.03, T)
        #draw_edge(Edge(ORIGIN, C), black, 0.03, T)
        #draw_edge(Edge(ORIGIN, D), black, 0.03, T)

        #draw_edge(Edge(ORIGIN, -A), black, 0.03, T)
        #draw_edge(Edge(ORIGIN, -B), black, 0.03, T)
        #draw_edge(Edge(ORIGIN, -C), black, 0.03, T)
        #draw_edge(Edge(ORIGIN, -D), black, 0.03, T)
        
        draw_vert(ORIGIN, orange, 0.05, T)
        draw_poly(cu, T)
        draw_poly(oc, T)
        
        for i in range(360):
            r = radians(i)
            p0 = Qvector((0, sy.sin(r), sy.cos(r), 0)) # (0, 'sin', 'cos', 0)
            p1 = Qvector((sy.sin(r), 0, sy.cos(r), 0)) # ('sin', 0, 'cos', 0)
            p2 = Qvector((0, sy.sin(r), 0, sy.cos(r))) # (0, 'sin', 0, 'cos')
            p3 = Qvector((sy.sin(r), sy.cos(r), 0, 0)) # ('sin', 'cos', 0, 0)
            p4 = Qvector((sy.sin(r), 0, 0, sy.cos(r))) # ('sin', 0, 0, 'cos')          
            p5 = Qvector((0, 0, sy.sin(r), sy.cos(r))) # (0, 0, 'sin', 'cos')
            
            draw_vert(p0, magenta, 0.03, T)
            draw_vert(p1, blue, 0.03, T)
            draw_vert(p2, purple, 0.03, T)
            draw_vert(p3, yellow, 0.03, T)
            draw_vert(p4, brown, 0.03, T)
            draw_vert(p5, cyan, 0.03, T)
            
if __name__ == "__main__":
    test4()
                        
