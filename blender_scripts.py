#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 11:50:00 2020

@author: mac
"""
import polys_blender
from polys_blender import Cuboctahedron, Cube, Octahedron
from polys_blender import Tetrahedron, InvTetrahedron, RD, Icosahedron, Struts
from polys_blender import twelve_around_one, draw_poly, draw_vert
from qrays import Qvector
from itertools import cycle

import os
import numpy as np
import math

from itertools import permutations
g = permutations((2,1,1,0))
UNIQUE = {p for p in g}  # set comprehension

IVM_DIRS = {Qvector(x) for x in UNIQUE}
PHI = (1 + math.sqrt(5))/2

def ch():
    ico = Icosahedron() * 2
    cubo = Cuboctahedron() * 2
    cub  = Cube() * 2
    rd = RD() * 2
    tet = Tetrahedron() * 2
    octa = Octahedron() * 2
    draw_poly(ico)
    draw_poly(cubo)
    draw_poly(rd)
    draw_poly(cub)
    draw_poly(tet)
    draw_poly(octa)
        
def jitterbug():
    ico = Icosahedron()
    cubo = Cuboctahedron()
    draw_poly(cubo)
    draw_poly(ico)
        
def logo():
    t  = Tetrahedron()
    it = InvTetrahedron()
    draw_poly(t)
    draw_poly(it)
        
def cubocta_in_cube_lattice():
    cubocta = Cuboctahedron()
    cube = Cube()
    draw_poly(cubocta)
    for c in twelve_around_one(cube):
        draw_poly(c)
            
def sphere_packing():
    cube = Cube()
    rd   = RD()
    octa    = Octahedron()
    cubocta = Cuboctahedron()
    draw_poly(cube)
    draw_poly(octa)
    draw_poly(rd)
    for p in twelve_around_one(cube):
        draw_poly(p)
    for p in twelve_around_one(rd):
        draw_poly(p)
    for p in twelve_around_one(octa):
        draw_poly(p)
    cubocta.vert_radius = Qvector((2,1,1,0)).length()/2 # grow the balls
    cubocta.vert_color = (1,0,0)
    draw_poly(cubocta, v=True, e=False)
    draw_vert(Qvector((0,0,0,0)), c=cubocta.vert_color, 
              r=cubocta.vert_radius)

def struts():
    IVM = {}
    IVM[0] = [Qvector((0,0,0,0))]
    IVM[1] = list(IVM_DIRS)
    print(IVM)
    polys_blender.IVM = IVM
    radius = 0.5
    cube = Cube()
    ico  = Icosahedron() * (1/PHI * math.sqrt(2)/2) * 1.2 * radius 
    st   = Struts(cube, ico, True)
    draw_poly(ico)
    draw_poly(st)
    # draw_poly(cube, target)
    for ik in twelve_around_one(ico):
        draw_poly(ik)
    # for c in twelve_around_one(cube):
        # draw_poly(c, target)
    for s in twelve_around_one(st):
        draw_poly(s, v=False)    