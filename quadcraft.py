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

def test6():
    """
    Layered CCP packing
    """
    
    nucleus = tuple([Qvector((0,0,0,0))])
    
    cubocta = tuple(IVM_DIRS)
    rd = RD()
    rd.edge_radius = 0.02
    
    with open("ccp0.pov", "w") as T:  
        T.write(pov_header)
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)
        draw_poly(rd, T)

    def next_layer(curr_layer, prev_layer):
        """
        generates a next layer of FCC spheres by trying 12-around-1 
        for each in the current layer (curr_layer) but without keeping
        any duplicates i.e. discarding redundant sphere centers.
        """
        next_layer = set()
        for qv in curr_layer:
            for bv in cubocta:
                v_sum = qv + bv
                if (not v_sum in curr_layer 
                    and not v_sum in prev_layer):
                    next_layer.add(v_sum)
        return sorted(list(next_layer))
    
    def frame(balls):
        for ball in balls:
            draw_vert(ball, "T_Stone18", half, T, texture=True) 
            draw_poly(rd + ball, T)              

    with open("ccp1.pov", "w") as T:  
        T.write(pov_header)            
        nl   = next_layer(nucleus, nucleus) # 1-freq
        frame(nl)

    with open("ccp2.pov", "w") as T:  
        T.write(pov_header)    
        nnl  = next_layer(nl, nucleus)      # 2-freq
        frame(nl)
        frame(nnl)

    with open("ccp3.pov", "w") as T:  
        T.write(pov_header)    
        nnnl = next_layer(nnl, nl)          # 3-freq
        frame(nl)
        frame(nnl)
        frame(nnnl)

    with open("ccp4.pov", "w") as T:  
        T.write(pov_header)    
        nnnnl= next_layer(nnnl, nnl)        # 4-freq
        frame(nl)
        frame(nnl)
        frame(nnnl)
        frame(nnnnl)  
    
    print("Number of balls in successive layers:")
    print(len(nl))     # 12 around 1
    print(len(nnl))    # should be 42 unique balls
    print(len(nnnl))   # expecting 92 unique balls
    print(len(nnnnl))  # the next next next next layer


def test7():
    """
    Blues Radio
    """
    blue   = "rgb <0, 0, 1>"
    red    = "rgb <1, 0, 0>"
    green  = "rgb <0, 1, 0>"
    yellow = "rgb <1, 1, 0>"

    Blue   = C
    Green  = B
    Red    = A
    Yellow = D
  
    camera = """

    // perspective (default) camera
    camera {
      location  <0.1, 0.2, 2.5>
      rotate    <20, 30, 180>
      //rotate    <35, 55, 20.0>
      look_at   <0.0, 0.0,  0.0>
      right     x*image_width/image_height
    }

    """

    def q_spokes():
        draw_edge(Edge(ORIGIN, Blue),   c=blue,   r=0.03, t=T) # home base
        draw_edge(Edge(ORIGIN, Green),  c=green,  r=0.03, t=T) # tip apex
        draw_edge(Edge(ORIGIN, Red),    c=red,    r=0.03, t=T) # base
        draw_edge(Edge(ORIGIN, Yellow), c=yellow, r=0.03, t=T) # base
       
        draw_vert(Blue,   c=blue,  r=0.1, t=T)  # home base
        draw_vert(Green,  c=green, r=0.1, t=T)  # tip apex
        draw_vert(Red,    c=red,   r=0.1, t=T)  # base
        draw_vert(Yellow, c=yellow,r=0.1, t=T)  # base
        
    with open("tripod_1.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera)      
        q_spokes()

    with open("tripod_2.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        draw_vert(Blue, c=blue, r=half, t=T )
        q_spokes()
        
    with open("tripod_3.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        draw_vert(Blue, c=blue, r=half, t=T )
        draw_vert(Blue + 2 * Yellow + Red + Green, c=yellow, r=half, t=T )       
        q_spokes()
              
    with open("tripod_4.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        draw_vert(Blue, c=blue, r=half, t=T )
        draw_vert(Blue + 2 * Yellow + Red + Green, c=yellow, r=half, t=T )       
        draw_vert(Blue + 2 * Green + Red + Yellow,  c=green,  r=half, t=T )
        q_spokes()
        
    with open("tripod_5.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        draw_vert(Blue, c=blue, r=half, t=T )
        draw_vert(Blue + 2 * Yellow + Red + Green, c=yellow, r=half, t=T )       
        draw_vert(Blue + 2 * Green + Red + Yellow, c=green,  r=half, t=T )
        draw_vert(Blue + 2 * Red + Green + Yellow, c=red,    r=half, t=T )
        q_spokes()
 
def test8():
    """
    Blues Radio
    """
    blue   = "rgb <0, 0, 1>"
    red    = "rgb <1, 0, 0>"
    green  = "rgb <0, 1, 0>"
    yellow = "rgb <1, 1, 0>"

    Blue   = C
    Green  = B
    Red    = A
    Yellow = D
  
    camera = """

    // perspective (default) camera
    camera {
      location  <0.1, 0.2, 2.5>
      rotate    <20, 30, 180>
      //rotate    <35, 55, 20.0>
      look_at   <0.0, 0.0,  0.0>
      right     x*image_width/image_height
    }

    """

    def q_spokes():
        draw_edge(Edge(ORIGIN, Blue),   c=blue,   r=0.03, t=T) # home base
        draw_edge(Edge(ORIGIN, Green),  c=green,  r=0.03, t=T) # tip apex
        draw_edge(Edge(ORIGIN, Red),    c=red,    r=0.03, t=T) # base
        draw_edge(Edge(ORIGIN, Yellow), c=yellow, r=0.03, t=T) # base
       
        draw_vert(Blue,   c=blue,  r=0.1, t=T)  # home base
        draw_vert(Green,  c=green, r=0.1, t=T)  # tip apex
        draw_vert(Red,    c=red,   r=0.1, t=T)  # base
        draw_vert(Yellow, c=yellow,r=0.1, t=T)  # base
        
    with open("vector_add_1.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera)      
        q_spokes()
        
        draw_edge(Edge(Blue, Blue + Yellow), c=yellow, r=0.02, t=T)
        start = Blue + Yellow
        draw_vert(start, c=yellow, r=0.03, t=T)
        
        draw_edge(Edge(start, start + Yellow), c=yellow, r=0.02, t=T)
        start = start + Yellow
        draw_vert(start, c=yellow, r=0.03, t=T)
        
        draw_edge(Edge(start, start + Red), c=red, r=0.02, t=T)
        start = start + Red 
        draw_vert(start, c=red, r=0.03, t=T)
        
        draw_edge(Edge(start, start + Green), c=green, r=0.02, t=T)
        start = start + Green
        draw_vert(start, c=green, r=0.03, t=T)        

    with open("vector_add_2.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera)      
        q_spokes()
        
        draw_edge(Edge(Blue, Blue + Green), c=green, r=0.02, t=T)
        start = Blue + Green
        draw_vert(start, c=green, r=0.03, t=T)
        
        draw_edge(Edge(start, start + Green), c=green, r=0.02, t=T)
        start = start + Green
        draw_vert(start, c=green, r=0.03, t=T)
        
        draw_edge(Edge(start, start + Red), c=red, r=0.02, t=T)
        start = start + Red 
        draw_vert(start, c=red, r=0.03, t=T)
        
        draw_edge(Edge(start, start + Yellow), c=yellow, r=0.02, t=T)
        start = start + Yellow
        draw_vert(start, c=yellow, r=0.03, t=T)        

    with open("vector_add_3.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera)      
        q_spokes()
        
        draw_edge(Edge(Blue, Blue + Red), c=red, r=0.02, t=T)
        start = Blue + Red
        draw_vert(start, c=red, r=0.03, t=T)
        
        draw_edge(Edge(start, start + Red), c=red, r=0.02, t=T)
        start = start + Red
        draw_vert(start, c=red, r=0.03, t=T)
        
        draw_edge(Edge(start, start + Green), c=green, r=0.02, t=T)
        start = start + Green
        draw_vert(start, c=green, r=0.03, t=T)
        
        draw_edge(Edge(start, start + Yellow), c=yellow, r=0.02, t=T)
        start = start + Yellow
        draw_vert(start, c=yellow, r=0.03, t=T)        

def test9():
    """
    TetraPacking
    """
    blue   = "rgb <0, 0, 1>"
    red    = "rgb <1, 0, 0>"
    green  = "rgb <0, 1, 0>"
    yellow = "rgb <1, 1, 0>"

    Blue   = C
    Green  = B
    Red    = A
    Yellow = D
  
    paths = [2 * Red + Green + Yellow,
             2 * Green + Red + Yellow,
             2 * Yellow + Red + Green]
    
    texture = "T_Wood20"
    # texture = "T_Stone18"
    # texture = "T_Silver_4D"
    # texture = "T_Brass_5A"
    
    camera = """

    // perspective (default) camera
    camera {
      location  <0.1, 0.2, 12.5>
      rotate    <20, 30, 180>
      //rotate    <35, 55, 20.0>
      look_at   <0.0, 0.0,  0.0>
      right     x*image_width/image_height
    }

    """  

    def q_spokes():
        draw_edge(Edge(ORIGIN, Blue),   c=blue,   r=0.03, t=T) # home base
        draw_edge(Edge(ORIGIN, Green),  c=green,  r=0.03, t=T) # tip apex
        draw_edge(Edge(ORIGIN, Red),    c=red,    r=0.03, t=T) # base
        draw_edge(Edge(ORIGIN, Yellow), c=yellow, r=0.03, t=T) # base
       
        draw_vert(Blue,   c=blue,  r=0.1, t=T)  # home base
        draw_vert(Green,  c=green, r=0.1, t=T)  # tip apex
        draw_vert(Red,    c=red,   r=0.1, t=T)  # base
        draw_vert(Yellow, c=yellow,r=0.1, t=T)  # base
        
    def next_layer(layer):
        nextlayer = set()
        for ball in layer:
            for path in paths:
                nextlayer.add(ball + path)
        return list(nextlayer)

    l0 = [Blue]
    l1 = next_layer(l0)
    l2 = next_layer(l1)
    l3 = next_layer(l2)
    l4 = next_layer(l3)
    l5 = next_layer(l4)
 
    with open("tetrapack_0.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        q_spokes()
        
    with open("tetrapack_1.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera)       
        q_spokes()
        
        for ball in l0:
            draw_vert(ball, texture, half, T, texture=True)

    with open("tetrapack_2.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        
        for ball in l0 + l1:
            draw_vert(ball, texture, half, T, texture=True)        

    with open("tetrapack_3.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        
        for ball in l0 + l1 + l2:
            draw_vert(ball, texture, half, T, texture=True)
    
    with open("tetrapack_4.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        
        for ball in l0 + l1 + l2 + l3:
            draw_vert(ball, texture, half, T, texture=True)

    with open("tetrapack_5.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        
        for ball in l0 + l1 + l2 + l3 + l4:
            draw_vert(ball, texture, half, T, texture=True)
            
    with open("tetrapack_6.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        
        for ball in l0 + l1 + l2 + l3 + l4 + l5:
            draw_vert(ball, texture, half, T, texture=True)
            
if __name__ == "__main__":
    test9()
    