#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 7 2025

@author: K.Urner

May 7: initialized to make renderings relevant to the QuadCraft Project
"""

from flextegrity import pov_header, Cuboctahedron, Cube, Octahedron, RT
from flextegrity import Tetrahedron, InvTetrahedron, RD, PD, Icosahedron, Mite
from flextegrity import Edge, draw_edge, draw_poly, draw_vert, half, ORIGIN, PHI
from qrays import Qvector, Vector
from flextegrity import A, B, C, D, E, F, G, H, I, J, K, L, M, N

import numpy as np
import sympy as sy
from math import sqrt as rt2

from itertools import permutations
g = permutations((2,1,1,0))
UNIQUE = {p for p in g}  # set comprehension

IVM_DIRS = {Qvector(x) for x in UNIQUE}

Svol = (PHI **-5)/2  
Evol = (rt2(2)/8) * (PHI ** -3)

sfactor = Svol/Evol

       
def test1():
    """
    sandbox for testing text output
    """
    
    with open("qc1.pov", "w") as T:
        T.write(pov_header)

        T.write("""
                // perspective (default) camera
                camera {
                  location  <7.5, 0.1, 0.2>
                  rotate    <0, 90, 0>
                  look_at   <0.0, 0.0,  0.0>
                  right     x*image_width/image_height
                }
                """)
                
        # test text writing
        T.write("""
            text {
            ttf "timrom.ttf" "Welcome to QuadCraft" .25, 0 
            pigment { Blue }
            translate -4.7*x
            translate -2*y
            }
            """)
                        
        cu = Cuboctahedron()
        
        draw_poly(cu, T)

def test2():
    """
    Daniel's': quadpod thrusters display (see Hop's) 
    but limited to 12 thrust patterns + no net thrust"
    Show corresponding destination as a cuboctahedron vertex
    
    https://flic.kr/p/2r3ir1k (Hop's Quadpod)
    """

    red = "rgb <{}, {}, {}>".format(1, 0, 0)    
    orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
    black = "rgb <{}, {}, {}>".format(0, 0, 0)
    
    offset = 3 * Qvector((1,1,0,0))
    t = Tetrahedron() 
    cu = Cuboctahedron() + offset
    
    t.edge_radius = 0.02
    t.edge_color  = black
    t.vert_color  = black
    
    # one permutation per frame    
    for idx, v in enumerate(UNIQUE):
        Aspoke = A * v[0]
        Bspoke = B * v[1]
        Cspoke = C * v[2]
        Dspoke = D * v[3]
        
        # for each frame of the animated GIF...
        with open(f"thrust{idx}.pov", "w") as T:
            T.write(pov_header)

            T.write(
"""
// perspective (default) camera
camera {
  location  <3.5, 0.1, 0.2>
  rotate    <0, 25, 10.0>								
  look_at   <-10, -2.0,  2.5>
  right     x*image_width/image_height
}
""")
                
            if v[0] > 0:
                draw_edge(Edge(ORIGIN, Aspoke), orange, 0.02, T)
            if v[1] > 0:
                draw_edge(Edge(ORIGIN, Bspoke), orange, 0.02, T)
            if v[2] > 0:
                draw_edge(Edge(ORIGIN, Cspoke), orange, 0.02, T)
            if v[3] > 0:
                draw_edge(Edge(ORIGIN, Dspoke), orange, 0.02, T)  
            
            draw_vert(Qvector(v) + offset, red, 0.1, T)
            draw_poly(t, T)          
            draw_poly(cu, T)
        
def test3():
    """
    cubes world
    """

    orange = "rgb <{}, {}, {}>".format(1, 128/255, 0)
    black = "rgb <{}, {}, {}>".format(0, 0, 0)   
    
    with open("qc8.pov", "w") as T:
        T.write(pov_header)

        # draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)

        def spokes(offset):
            draw_edge(Edge(ORIGIN + offset, E + offset), black, 0.02, T)
            draw_edge(Edge(ORIGIN + offset, F + offset), black, 0.02, T)
            draw_edge(Edge(ORIGIN + offset, G + offset), black, 0.02, T)
            draw_edge(Edge(ORIGIN + offset, H + offset), black, 0.02, T)         
                    
        for offset in [ORIGIN, E+F, E+G, E+H, F+G, G+H, H+F]:
            
            cu = Cube() + offset
            cu.edge_radius = 0.02
            draw_poly(cu, T)
            spokes(offset)

        for offset in IVM_DIRS:
            
            cu = Cube() + offset
            cu.edge_radius = 0.02
            draw_poly(cu, T)
            spokes(offset)
            # draw_vert(ORIGIN + offset, "T_Stone18", half, T, texture=True)
            
        rd = RD()
        rd.edge_radius = 0.02
        # draw_poly(rd, T)
        
        oc = Octahedron()
        oc.edge_radius = 0.02
        # draw_poly(oc, T)

def test4():
    """
    Animated GIF: tet, balls, invtet, balls, both tets, cube, octa, RD
    """
    
    tet = Tetrahedron()
    tet.edge_radius = 0.02
    
    invtet = InvTetrahedron()
    invtet.edge_radius = 0.02
    
    cu = Cube()
    cu.edge_radius = 0.02
    
    octa = Octahedron()
    octa.edge_radius = 0.02
    
    rd = RD()    
    rd.edge_radius = 0.02
    
    with open("qctest4_1.pov", "w") as T:
        T.write(pov_header)    
        draw_poly(tet, T)

    with open("qctest4_2.pov", "w") as T:
        T.write(pov_header)
        for qv in A,B,C,D:
            draw_vert(ORIGIN + qv, "T_Stone18", half, T, texture=True)
        
    with open("qctest4_3.pov", "w") as T:
        T.write(pov_header)
        draw_poly(tet, T)
        draw_poly(invtet, T)
        
    with open("qctest4_4.pov", "w") as T:
        T.write(pov_header)
        for qv in E,F,G,H:
            draw_vert(ORIGIN + qv, "T_Stone18", half, T, texture=True)
            
    with open("qctest4_5.pov", "w") as T:
        T.write(pov_header)
        draw_poly(tet, T)
        draw_poly(invtet, T)
        draw_poly(cu, T)
        
    with open("qctest4_6.pov", "w") as T:
        T.write(pov_header)
        T.write(pov_header)
        draw_poly(cu, T)
        
    with open("qctest4_7.pov", "w") as T:
        T.write(pov_header)
        draw_poly(cu, T)
        draw_poly(octa, T)  

    with open("qctest4_8.pov", "w") as T:
        T.write(pov_header)
        draw_poly(cu, T)
        draw_poly(octa, T)
        for qv in I, J, K, L, M, N:
            draw_vert(ORIGIN + qv, "T_Stone18", half, T, texture=True)

    with open("qctest4_9.pov", "w") as T:
        T.write(pov_header)
        draw_poly(cu, T)
        draw_poly(octa, T)
        for qv in I, J, K, L, M, N:
            draw_vert(ORIGIN + qv, "T_Stone18", half, T, texture=True)
            newrd = rd + qv
            newrd.edge_radius = 0.02
            draw_poly(newrd, T)
            
    with open("qctest4_10.pov", "w") as T:
        T.write(pov_header)
        draw_poly(cu, T)
        draw_poly(octa, T)  
        draw_poly(rd, T)

    with open("qctest4_11.pov", "w") as T:
        T.write(pov_header)  
        draw_poly(rd, T)
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)        

def test5():
    """
    Lakota Tetrapod
    """
    
    red    = "rgb <1, 0, 0>"
    white  = "rgb <1, 1, 1>"
    yellow = "rgb <1, 1, 0>"
    black  = "rgb <0, 0, 0>"
    
    with open("lakota_tetra.pov", "w") as T:  
        T.write(pov_header)
        for qv, c in zip([A,B,C,D],[red, white, yellow, black]):
            draw_vert(ORIGIN + qv, c, half, T)        
    
if __name__ == "__main__":
    test5()
    