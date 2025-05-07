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
from qrays import Qvector, Vector, A, B, C, D

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
        
    for idx, v in enumerate(UNIQUE):
        Aspoke = A * v[0]
        Bspoke = B * v[1]
        Cspoke = C * v[2]
        Dspoke = D * v[3]
        
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
        
        # break # just testing first iteration
        
if __name__ == "__main__":
    test2()
    