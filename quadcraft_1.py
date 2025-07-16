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
   location  <-2.5, 0.1, -0.4>
   rotate    <90.0, 0, -100>
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

colors = [orange, red, green, blue, yellow, magenta, black, purple, cyan, pink, brown, salmon, grey]
names  = ['orange', 'red', 'green', 'blue', 'yellow', 'magenta', 'black', 
          'purple', 'cyan', 'pink', 'brown', 'salmon', 'grey']

colordict = {n:c for n,c in zip(names, colors)} 
ivm_colors = {n:v for v,n in zip(IVM_DIRS, names[1:])}
ivm_colors['orange'] = ORIGIN

def colorkey():
    for n,v in ivm_colors.items():
        print("{:10}: {}".format(n, v))
        
def test0():
    out = open("qc_0.pov", "w")
    out.write(pov_header)
    
    draw_vert(ORIGIN, orange, half, out)
    for v, c in zip(IVM_DIRS, colors[1:]):
        draw_vert(v, c, half, out)  
        
def test1():
    out = open("qc_1.pov", "w")
    out.write(pov_header) 
    zero = sy.Integer(0)
    one  = sy.Integer(1)
    
    origin = Vector((zero,zero,zero))
    v1 = Vector((one,zero,zero))
    v2 = Vector((zero,one,zero))
    v3 = Vector((one,one,zero))
    v4 = Vector((half, half, rt2(2)/2))
    
    draw_vert(origin, orange, half, out)
    draw_vert(v1, magenta, half, out)
    draw_vert(v2, red, half, out)
    draw_vert(v3, grey, half, out)
    draw_vert(v4, yellow, half, out)
    
    color_key = {n:v for n,v in 
                 zip(('orange','magenta', 
                      'red', 'grey', 'yellow'),
                     (origin, v1, v2, v3, v4))}
    
    for c, v in color_key.items():
        print("{:8}: {}".format(c, v))
    
    print()
    
    for c, v in color_key.items():
        print("{:8}: {}".format(c, v.quadray())) 
    
    out.close()


def test2():
    out = open("qc_2.pov", "w")
    out.write(pov_header) 
    
    origin = ivm_colors['orange']
    v1 = ivm_colors['magenta']
    v2 = ivm_colors['red']
    v3 = ivm_colors['grey']
    v4 = ivm_colors['yellow']
    
    draw_vert(origin, orange, half, out)
    draw_vert(v1, magenta, half, out)
    draw_vert(v2, red, half, out)
    draw_vert(v3, grey, half, out)
    draw_vert(v4, yellow, half, out)
    
    color_key = {n:v for n,v in 
                 zip(('orange','magenta', 
                      'red', 'grey', 'yellow'),
                     (origin, v1, v2, v3, v4))}
    
    for c, v in color_key.items():
        print("{:8}: {}".format(c, v))
        
    print()
    
    for c, v in color_key.items():
        print("{:8}: {}".format(c, v.xyz))    

def test3():
    """
    OctaPacking
    """

    # texture = "T_Wood20"
    # texture = "T_Stone18"
    # texture = "T_Silver_4D"
    # texture = "T_Brass_5A"
    
    camera = \
"""
// perspective (default) camera
camera {
  location  <0.1, 0.2, 10>
  rotate    <20, 30, 180>
  //rotate    <35, 55, 20.0>
  look_at   <0.0, 0.0,  0.0>
  right     x*image_width/image_height
}
"""

    BALLNUMBER  = 1
    balldict    = {}
    rad = half
    # rad = 0.12
    
    origin = ivm_colors['orange']
    v1 = ivm_colors['magenta']
    v2 = ivm_colors['red']
    v3 = ivm_colors['grey']
    v4 = ivm_colors['yellow']
  
    paths = [v1, v2, v3, v4]

    rd = RD()
    
    def next_layer(layer):
        nonlocal BALLNUMBER
        nextlayer = list()
        for ball in layer:
            for path in paths:
                candidate = ball + path
                # print(candidate)
                if candidate not in nextlayer:
                    BALLNUMBER += 1
                    nextlayer.append(candidate)
                    balldict[BALLNUMBER] = candidate
        return nextlayer
        
    balldict[1] = origin
    l0 = [origin]
    l1 = next_layer(l0)
    l2 = next_layer(l1)
    l3 = next_layer(l2)
    l4 = next_layer(l3)
    l5 = next_layer(l4)
    l6 = next_layer(l5)
    
    def get_texture(b):
        return "T_Wood20"
        if b in l0:
            return "T_Stone18"
        if b in l1:
            return "T_Silver_4D"
        if b in l2:
            return "T_Brass_5A"
        if b in l3:
            return "T_Wood20"
        if b in l4:
            return "T_Stone18"
        if b in l5:
            return "T_Silver_4D"
        
    with open("ocpack_1.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera)       

        for ball in l0:
            texture = get_texture(ball)
            draw_vert(ball, texture, rad, T, texture=True)
            draw_poly(rd + ball, T)
            
    with open("ocpack_2.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        
        for ball in l0 + l1:
            texture = get_texture(ball)
            draw_vert(ball, texture, rad, T, texture=True)        
            draw_poly(rd + ball, T)
            
    with open("ocpack_3.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        
        for ball in l0 + l1 + l2:
            texture = get_texture(ball)
            draw_vert(ball, texture, rad, T, texture=True)
            draw_poly(rd + ball, T)
            
    with open("ocpack_4.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        
        for ball in l0 + l1 + l2 + l3:
            texture = get_texture(ball)
            draw_vert(ball, texture, rad, T, texture=True)
            draw_poly(rd + ball, T)
            
    with open("ocpack_5.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        
        for ball in l0 + l1 + l2 + l3 + l4:
            texture = get_texture(ball)
            draw_vert(ball, texture, rad, T, texture=True)
            draw_poly(rd + ball, T)
            
    with open("ocpack_6.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        
        for ball in l0 + l1 + l2 + l3 + l4 + l5:
            texture = get_texture(ball)
            draw_vert(ball, texture, rad, T, texture=True)
            draw_poly(rd + ball, T)
            
    with open("ocpack_7.pov", "w") as T:  
        T.write(pov_header)
        T.write(camera) 
        
        for ball in l0 + l1 + l2 + l3 + l4 + l5 + l6:
            texture = get_texture(ball)
            draw_vert(ball, texture, rad, T, texture=True)
            draw_poly(rd + ball, T)            

    return balldict
    
def main():
    test3()
    
if __name__ == "__main__":
    main()