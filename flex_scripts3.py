#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thurs Feb 13 2025

@author: K. Urner

Feb  7 2026: add A module
Feb  5 2026: new tests
Apr  8 2025: make this 2nd of 2 files, flex_scripts1.py being the first
Feb 19 2025: import PHI as sympy object vs using math.sqrt  
"""

from flextegrity import pov_header, Cuboctahedron, Cube, Octahedron, RT, Amod
from flextegrity import Tetrahedron, InvTetrahedron, RD, PD, Icosahedron, Mite
from flextegrity import Edge, draw_edge, draw_poly, draw_vert, half, ORIGIN, PHI
from qrays import Qvector, Vector, A, B, C, D

import numpy as np
import sympy as sy
from sympy import sqrt as rt2, sin, cos
from mpmath import radians

from itertools import permutations
g = permutations((2,1,1,0))
UNIQUE = {p for p in g}  # set comprehension

IVM_DIRS = {Qvector(x) for x in UNIQUE}

Svol = (PHI **-5)/2  
Evol = (rt2(2)/8) * (PHI ** -3)

sfactor = Svol/Evol

CLOSEUP1 = \
"""
   
// perspective (default) camera
camera {
  location  <3.0, 3.0, 3.1>
  rotate    <0, 0, 0>
  look_at   <0.0, 0.0,  0.2>
  right     x*image_width/image_height
}

"""

CLOSEUP2 = \
"""

// perspective (default) camera
camera {
  location  <2.0, 2.6, 2.1>
  rotate    <10, 20, 0>
  look_at   <0.0, 0.0,  0.2>
  right     x*image_width/image_height
}

"""

CLOSEUP = \
"""
// perspective (default) camera
camera {
  location  <0.1, 3.6, 0.1>
  rotate    <20, 0, 20>
  look_at   <0.0, 0.0,  0.2>
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
        
        # draw_vert(ORIGIN, orange, 0.05, T)
        
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)
        draw_poly(cu, T)  # canonical cube tv 3
        draw_poly(oc, T)  # canonical octahedron tv 4
        
        for i in range(360): # from 0 to 359 degrees
            r = radians(i)
            sinr, cosr = sin(r), cos(r)
            p0 = Qvector((0, sinr, cosr, 0)) # (0, sin, cos, 0)
            p1 = Qvector((sinr, 0, cosr, 0)) # (sin, 0, cos, 0)
            p2 = Qvector((0, sinr, 0, cosr)) # (0, sin, 0, cos)
            p3 = Qvector((sinr, cosr, 0, 0)) # (sin, cos, 0, 0)
            p4 = Qvector((sinr, 0, 0, cosr)) # (sin, 0, 0, cos)          
            p5 = Qvector((0, 0, sinr, cosr)) # (0, 0, sin, cos)
            
            draw_vert(p0, magenta, 0.03, T)
            draw_vert(p1, blue,    0.03, T)
            draw_vert(p2, orange,  0.03, T)
            draw_vert(p3, yellow,  0.03, T)
            draw_vert(p4, pink,    0.03, T)
            draw_vert(p5, cyan,    0.03, T)

def test5():
    magenta = "rgb <{}, {}, {}>".format(1, 0, 1)
    
    cu3    = Cube()            # face diagonals = D
    cu3.edge_radius = 0.03

    xyzcu  = cu3 * (1/rt2(2))  # cube edges = R
    xyzcu.edge_color = magenta
    xyzcu.edge_radius = 0.03
    xyzcu.vert_color = magenta

    rd     = RD()              # hug ball
        
    with open("learn_s3_0.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(cu3, T)
        draw_poly(xyzcu, T)
        
    with open("learn_s3_1.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(cu3, T)
        draw_poly(xyzcu, T)
        draw_poly(rd, T)

    with open("learn_s3_2.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(cu3, T)
        draw_poly(xyzcu, T)
        draw_poly(rd, T)
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)

def test6():

    big_size = 0.07
    sml_size = 0.04

    green   = "rgb <0, 1, 0>"
    blue    = "rgb <0, 0, 1>"
    yellow  = "rgb <1, 1, 0>"
    red     = "rgb <1, 0, 0>"
    
    cu3    = Cube()            # face diagonals = D
    cu3.edge_radius = 0.03

    BRYG  = Tetrahedron() 
    BRYG.edge_radius = 0.03

    bryg  = InvTetrahedron() 
    bryg.edge_radius = 0.03
    
    oc4    = Octahedron()          
    oc4.edge_radius = 0.03
    
    rd6    = RD()          
    rd6.edge_radius = 0.03

    with open("ccp_ball_1.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(cu3, T)
        draw_poly(BRYG, T)
        draw_poly(bryg, T)
        
        draw_vert(A, red, big_size, T)
        draw_vert(B, green, big_size, T)
        draw_vert(C, blue, big_size, T)
        draw_vert(D, yellow, big_size, T)

        draw_vert(-A, red, sml_size, T)
        draw_vert(-B, green, sml_size, T)
        draw_vert(-C, blue, sml_size, T)
        draw_vert(-D, yellow, sml_size, T)
           
    with open("ccp_ball_2.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(cu3, T)
        draw_poly(BRYG, T)
        draw_poly(bryg, T)
        
        draw_vert(A, red, big_size, T)
        draw_vert(B, green, big_size, T)
        draw_vert(C, blue, big_size, T)
        draw_vert(D, yellow, big_size, T)

        draw_vert(-A, red, sml_size, T)
        draw_vert(-B, green, sml_size, T)
        draw_vert(-C, blue, sml_size, T)
        draw_vert(-D, yellow, sml_size, T)
        
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)

    with open("ccp_ball_3.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(cu3, T)
        draw_poly(BRYG, T)
        draw_poly(bryg, T)
        
        draw_vert(A, red, big_size, T)
        draw_vert(B, green, big_size, T)
        draw_vert(C, blue, big_size, T)
        draw_vert(D, yellow, big_size, T)

        draw_vert(-A, red, sml_size, T)
        draw_vert(-B, green, sml_size, T)
        draw_vert(-C, blue, sml_size, T)
        draw_vert(-D, yellow, sml_size, T)
    
        draw_poly(oc4, T)
        draw_poly(rd6, T)
        
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)

    with open("ccp_ball_4.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(cu3, T)
        draw_poly(BRYG, T)
        draw_poly(bryg, T)
        
        draw_vert(A, red, big_size, T)
        draw_vert(B, green, big_size, T)
        draw_vert(C, blue, big_size, T)
        draw_vert(D, yellow, big_size, T)

        draw_vert(-A, red, sml_size, T)
        draw_vert(-B, green, sml_size, T)
        draw_vert(-C, blue, sml_size, T)
        draw_vert(-D, yellow, sml_size, T)
    
        draw_poly(oc4, T)
        draw_poly(rd6, T)

def test7():
    """
    This function gets detailed expository treatment 
    in a School of Tomorrow Jupyter Notebook:
        
    https://github.com/4dsolutions/School_of_Tomorrow/blob/master/Shapes_Framework.ipynb
    """
    
    ic    = Icosahedron()    # edges D
    ic.edge_radius = 0.03

    pd  = PD()               # Icosa's dual
    pd.edge_radius = 0.03

    rt  = RT()               # their "begot" 
    rt.edge_radius = 0.03
    
    rt_e    = rt * (1/PHI)          
    rt_e.edge_radius = 0.03
 
    with open("genesis_1.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(ic, T)
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)
     
    with open("genesis_2.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(ic, T)
        draw_poly(pd, T)
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)

    with open("genesis_3.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(ic, T)
        draw_poly(pd, T)
        draw_poly(rt, T)
        
    with open("genesis_4.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(ic, T)
        draw_poly(pd, T)
        draw_poly(rt_e, T)
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)

    with open("genesis_5.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(rt_e, T)
        draw_vert(ORIGIN, "T_Stone18", half, T, texture=True)

def test8():
    
    cu3   = Cube()
    cu3.edge_radius = 0.01
    
    hbt   = Tetrahedron()
    hbt.edge_radius = 0.01
    
    amod  = Amod()
    amod.edge_radius = 0.02

    with open("amod_in_hbt.pov", "w") as T:
        T.write(pov_header) 
        T.write(CLOSEUP)
        draw_poly(cu3, T)
        draw_poly(hbt, T)
        draw_poly(amod, T)

def test9():

    big_size = half
    sml_size = 0.04

    black   = "rgb <0, 0, 0>"
    green   = "rgb <0, 1, 0>"
    blue    = "rgb <0, 0, 1>"
    yellow  = "rgb <1, 1, 0>"
    red     = "rgb <1, 0, 0>"
    magenta = "rgb <{}, {}, {}>".format(1, 0, 1)
    orange  = "rgb <{}, {}, {}>".format(1, 128/255, 0)
    
    OX = Edge(Vector((0, 0, 0)), Vector(( 1, 0, 0)))
    Ox = Edge(Vector((0, 0, 0)), Vector((-1, 0, 0)))

    OY = Edge(Vector((0, 0, 0)), Vector(( 0, 1, 0)))
    Oy = Edge(Vector((0, 0, 0)), Vector(( 0,-1, 0)))
    
    OZ = Edge(Vector((0, 0, 0)), Vector(( 0, 0, 1)))
    Oz = Edge(Vector((0, 0, 0)), Vector(( 0, 0,-1)))

    cu3    = Cube()            # face diagonals = D
    cu3.edge_radius = 0.03

    BRYG  = Tetrahedron()      # not drawn
    BRYG.edge_radius = 0.03
    
    with open("xyz_ivm.pov", "w") as T:
        
        T.write(pov_header) 
        T.write(CLOSEUP)
        
        draw_edge(OX, magenta, 0.03, T)
        draw_edge(Ox, magenta, 0.03, T)

        draw_edge(OY, orange, 0.03, T)
        draw_edge(Oy, orange, 0.03, T)

        draw_edge(OZ, black, 0.03, T)
        draw_edge(Oz, black, 0.03, T)
        
        draw_poly(cu3, T)

        draw_vert(A, red, big_size, T)
        draw_vert(B, green, big_size, T)
        draw_vert(C, blue, big_size, T)
        draw_vert(D, yellow, big_size, T)

def test10():

    big_size = 0.10
    sml_size = 0.05
    
    black   = "rgb <0, 0, 0>"
    green   = "rgb <0, 1, 0>"
    blue    = "rgb <0, 0, 1>"
    yellow  = "rgb <1, 1, 0>"
    red     = "rgb <1, 0, 0>"
    magenta = "rgb <{}, {}, {}>".format(1, 0, 1)
    orange  = "rgb <{}, {}, {}>".format(1, 128/255, 0)
    
    OX = Edge(Vector((0, 0, 0)), Vector(( 1, 0, 0)))
    Ox = Edge(Vector((0, 0, 0)), Vector((-1, 0, 0)))

    OY = Edge(Vector((0, 0, 0)), Vector(( 0, 1, 0)))
    Oy = Edge(Vector((0, 0, 0)), Vector(( 0,-1, 0)))
    
    OZ = Edge(Vector((0, 0, 0)), Vector(( 0, 0, 1)))
    Oz = Edge(Vector((0, 0, 0)), Vector(( 0, 0,-1)))

    OA = Edge(ORIGIN, A)
    OB = Edge(ORIGIN, B)
    OC = Edge(ORIGIN, C)
    OD = Edge(ORIGIN, D)        

    cu3    = Cube()            # face diagonals = D
    cu3.edge_radius = 0.03

    with open("ivm_xyz_spokes_0.pov", "w") as T:
        
        T.write(pov_header) 
        T.write(CLOSEUP)
        
        draw_edge(OX, black, 0.03, T)
        draw_edge(Ox, black, 0.03, T)

        draw_edge(OY, black, 0.03, T)
        draw_edge(Oy, black, 0.03, T)

        draw_edge(OZ, black, 0.03, T)
        draw_edge(Oz, black, 0.03, T)
        
        draw_poly(cu3, T)

        draw_edge(OA, red, 0.03, T)
        draw_edge(OB, green, 0.03, T)
        draw_edge(OC, blue, 0.03, T)
        draw_edge(OD, yellow, 0.03, T)

        draw_vert(ORIGIN, orange, 0.10, T)   
        
        draw_vert(A, red, big_size, T)
        draw_vert(B, green, big_size, T)
        draw_vert(C, blue, big_size, T)
        draw_vert(D, yellow, big_size, T)
        
        draw_vert(-A, red, sml_size, T)
        draw_vert(-B, green, sml_size, T)
        draw_vert(-C, blue, sml_size, T)
        draw_vert(-D, yellow, sml_size, T)

    with open("ivm_xyz_spokes_1.pov", "w") as T:
        
        T.write(pov_header) 
        T.write(CLOSEUP)
        
        draw_edge(OX, black, 0.03, T)
        draw_edge(Ox, black, 0.03, T)

        draw_edge(OY, black, 0.03, T)
        draw_edge(Oy, black, 0.03, T)

        draw_edge(OZ, black, 0.03, T)
        draw_edge(Oz, black, 0.03, T)
        
        draw_poly(cu3, T)

        draw_edge(OA, red, 0.03, T)
        draw_edge(OB, green, 0.03, T)
        draw_edge(OC, blue, 0.03, T)
        draw_edge(OD, yellow, 0.03, T)

        draw_vert(ORIGIN, orange, 0.10, T)   
        
        draw_vert(A, red, half, T)
        draw_vert(B, green, half, T)
        draw_vert(C, blue, half, T)
        draw_vert(D, yellow, half, T)
        
        draw_vert(-A, red, sml_size, T)
        draw_vert(-B, green, sml_size, T)
        draw_vert(-C, blue, sml_size, T)
        draw_vert(-D, yellow, sml_size, T)

    with open("ivm_xyz_spokes_2.pov", "w") as T:
        
        T.write(pov_header) 
        T.write(CLOSEUP)
        
        draw_edge(OX, black, 0.03, T)
        draw_edge(Ox, black, 0.03, T)

        draw_edge(OY, black, 0.03, T)
        draw_edge(Oy, black, 0.03, T)

        draw_edge(OZ, black, 0.03, T)
        draw_edge(Oz, black, 0.03, T)
        
        draw_poly(cu3, T)

        draw_edge(OA, red, 0.03, T)
        draw_edge(OB, green, 0.03, T)
        draw_edge(OC, blue, 0.03, T)
        draw_edge(OD, yellow, 0.03, T)

        draw_vert(ORIGIN, orange, half, T)   
        
        draw_vert(A, red, big_size, T)
        draw_vert(B, green, big_size, T)
        draw_vert(C, blue, big_size, T)
        draw_vert(D, yellow, big_size, T)
        
        draw_vert(-A, red, sml_size, T)
        draw_vert(-B, green, sml_size, T)
        draw_vert(-C, blue, sml_size, T)
        draw_vert(-D, yellow, sml_size, T)        
    
if __name__ == "__main__":
    test10()
                        
