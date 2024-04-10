#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 11:50:00 2020

@author: mac
"""
from flextegrity import pov_header, Cuboctahedron, Cube, Octahedron
from flextegrity import Tetrahedron, InvTetrahedron, RD, Icosahedron, Struts
from flextegrity import twelve_around_one, draw_poly, draw_vert
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

Svol = (PHI **-5)/2  
Evol = (math.sqrt(2)/8) * (PHI ** -3)

sfactor = Svol/Evol

def ch():
    with open("concentric_hierarchy.pov", "w") as target:
        target.write(pov_header)
        ico = Icosahedron() * 2
        cubo = Cuboctahedron() * 2
        cub  = Cube() * 2
        rd = RD() * 2
        tet = Tetrahedron() * 2
        octa = Octahedron() * 2
        draw_poly(ico, target)
        draw_poly(cubo, target)
        draw_poly(rd, target)
        draw_poly(cub, target)
        draw_poly(tet, target)
        draw_poly(octa, target)

def iw():
    with open("icosa_within.pov", "w") as target:
        target.write(pov_header)
        ico = 2 * Icosahedron() * 0.8
        cubo = 2 * Cuboctahedron() * 0.8
        octa = 2 * Octahedron() * 0.8
        draw_poly(ico, target)
        draw_poly(cubo, target)
        draw_poly(octa, target)
        
def jitterbug():
    with open("cubo_icosa.pov", "w") as target:
        target.write(pov_header)
        ico = Icosahedron()
        # cubo = Cuboctahedron()
        # draw_poly(cubo, target)
        draw_poly(ico, target)
        
def logo():
    with open("logo.pov", "w") as target:
        target.write(pov_header)
        t  = Tetrahedron()
        it = InvTetrahedron()
        draw_poly(t, target)
        draw_poly(it, target)
        
def cubocta_in_cube_lattice():
    with open("cubocta.pov", "w") as target:
        target.write(pov_header) 
        cubocta = Cuboctahedron()
        cube = Cube()
        draw_poly(cubocta, target)
        for c in twelve_around_one(cube):
            draw_poly(c, target)
            
def sphere_packing():
    with open("sphere_pack2.pov", "w") as target:
        target.write(pov_header)
        cube = Cube()
        rd   = RD()
        octa    = Octahedron()
        cubocta = Cuboctahedron()
        draw_poly(cube, target)
        draw_poly(octa, target)
        draw_poly(rd, target)
        for p in twelve_around_one(cube):
            draw_poly(p, target)
        for p in twelve_around_one(rd):
            draw_poly(p, target)
        for p in twelve_around_one(octa):
            draw_poly(p, target)
        cubocta.vert_radius = Qvector((2,1,1,0)).length()/2 # grow the balls
        cubocta.vert_color = "rgb <1,0,0>"
        draw_poly(cubocta, target, v=True, e=False)
        draw_vert(Qvector((0,0,0,0)), c=cubocta.vert_color, 
                  r=cubocta.vert_radius, t=target)

def spheres_bulging():
    with open("sphere_pack2.pov", "w") as target:
        target.write(pov_header)
        cube = Cube()
        rd   = RD()
        octa    = Octahedron()
        cubocta = Cuboctahedron()
        draw_poly(cube, target)
        draw_poly(octa, target)
        draw_poly(rd, target)
        for p in twelve_around_one(cube):
            draw_poly(p, target)
        for p in twelve_around_one(rd):
            draw_poly(p, target)
        for p in twelve_around_one(octa):
            draw_poly(p, target)
        cubocta.vert_radius = Qvector((2,1,1,0)).length()/2 # grow the balls
        cubocta.vert_color = "rgb <1,0,0>"
        draw_poly(cubocta, target, v=True, e=False)
        draw_vert(Qvector((0,0,0,0)), c=cubocta.vert_color, 
                  r=cubocta.vert_radius, t=target)
 
def animation(targdir="anim2"):
    
    path = os.path.join(".",targdir)
    if not os.path.isdir(targdir):
        os.mkdir(targdir)
    
    radii = np.linspace(0, 0.5, 8).tolist()
    radii += reversed(radii[1:-1])
    for frame_id, radius in enumerate(radii, start=1):
        filename = f"balls{frame_id:03}.pov"

        with open(os.path.join(path,filename), "w") as target:
            target.write(pov_header) 
            cubocta             = Cuboctahedron()
            cubocta.vert_radius = radius
            cubocta.vert_color  = "rgb <1,0,0>"
            draw_poly(cubocta, target, v=True, e=False)
            draw_vert(Qvector((0,0,0,0)), c=cubocta.vert_color, 
                      r=cubocta.vert_radius, t=target)
            
            if frame_id < 9:
                rd   = RD()
                draw_poly(rd, target)
                for p in twelve_around_one(rd):
                    draw_poly(p, target)
            
            draw_poly(Cuboctahedron(), target, v=True, e=True)

def animation2(targdir="anim2"):
    
    path = os.path.join(".",targdir)
    if not os.path.isdir(targdir):
        os.mkdir(targdir)
    
    radii = np.linspace(0, 0.5, 8).tolist()
    radii += reversed(radii[1:-1])
    for frame_id, radius in enumerate(radii, start=1):
        filename = f"balls{frame_id:03}.pov"

        with open(os.path.join(path,filename), "w") as target:
            target.write(pov_header) 
            cubocta             = Cuboctahedron()
            cubocta.vert_radius = radius
            cubocta.vert_color  = "rgb <1,0,0>"
            draw_poly(cubocta, target, v=True, e=False)
            draw_vert(Qvector((0,0,0,0)), c=cubocta.vert_color, 
                      r=cubocta.vert_radius, t=target)
            
            if frame_id < 9:
                rd   = RD()
                draw_poly(rd, target)
                for p in twelve_around_one(rd):
                    draw_poly(p, target)
            
            draw_poly(Cuboctahedron(), target, v=True, e=True)

def animation3(targdir="anim3"):
    
    targdir = os.path.join(".",targdir)
    if not os.path.isdir(targdir):
        os.mkdir(targdir)
    
    radii = np.linspace(0, 0.5, 8).tolist()
    radii += reversed(radii[1:-1])
    for frame_id, radius in enumerate(radii, start=1):
        filename = f"balls{frame_id:03}.pov"

        with open(os.path.join(targdir,filename), "w") as target:
            target.write(pov_header) 
            cubocta             = Cuboctahedron()
            cubocta.vert_radius = radius
            cubocta.vert_color  = "rgb <1,0,0>"
            if frame_id <= 9:
                draw_poly(cubocta, target, v=True, e=False)
                draw_vert(Qvector((0,0,0,0)), c=cubocta.vert_color, 
                          r=cubocta.vert_radius, t=target)
                                
            if frame_id > 9:
                cube = Cube()
                ico  = Icosahedron() * (1/PHI * math.sqrt(2)/2) * 1.2 * radius 
                st   = Struts(cube, ico)
                draw_poly(ico, target)
                draw_poly(st, target)
                # draw_poly(cube, target)
                for ik in twelve_around_one(ico):
                    draw_poly(ik, target)
                # for c in twelve_around_one(cube):
                    # draw_poly(c, target)
                for s in twelve_around_one(st):
                    draw_poly(s, target)
            
def animation4(targdir="anim4"):
    
    targdir = os.path.join(".",targdir)
    if not os.path.isdir(targdir):
        os.mkdir(targdir)
    
    radii = np.linspace(0.6, 1.3, 8).tolist()
    radii += reversed(radii[1:-1])
    for frame_id, radius in enumerate(radii, start=1):
        filename = f"balls{frame_id:03}.pov"
        
        with open(os.path.join(targdir,filename), "w") as target:
            target.write(pov_header) 
            ico = Icosahedron() * radius
            cube= Cube() * PHI * 1.5
            s   = Struts(cube, ico)
            draw_poly(ico, target)
            draw_poly(cube, target)
            draw_poly(s, target)
            
def one_hop_away(thirteen_balls):
    the_ball, *twelve_balls = thirteen_balls
    newlist = [the_ball]
    while True:
        for idx, ball in enumerate(twelve_balls):
            if (the_ball - ball).length() == 1.0:
                newlist.append(ball)
                the_ball = ball
                break
        del twelve_balls[idx]
        if not twelve_balls:
            break
    return newlist
    
def animation5(targdir="anim5"):
    targdir = os.path.join(".",targdir)
    if not os.path.isdir(targdir):
        os.mkdir(targdir)

    thirteen_balls = [Qvector((0,0,0,0))] + list(IVM_DIRS)
     
    neighbors = one_hop_away(thirteen_balls)
    
    for frame_id in range(13):
        filename = f"balls{frame_id:03}.pov"
            
        with open(os.path.join(targdir,filename), "w") as target:
            target.write(pov_header) 
            rd = RD()
            draw_poly(rd, target)

            for idx, p in enumerate(twelve_around_one(rd)):
                if idx == frame_id:
                    draw_vert(neighbors[idx], 
                              c="rgb <1,0,0>", 
                              r=0.5, t=target)
                draw_poly(p, target)
                
            if 12 == frame_id:
                draw_vert(neighbors[12], 
                          c="rgb <1,0,0>", 
                          r=0.5, t=target)

def animation10(targdir="anim10"):
    targdir = os.path.join(".",targdir)
    if not os.path.isdir(targdir):
        os.mkdir(targdir)

    thirteen_balls = [Qvector((0,0,0,0))] + list(IVM_DIRS)
     
    neighbors = one_hop_away(thirteen_balls)
    
    for frame_id in range(13):
        filename = f"balls{frame_id:03}.pov"
            
        with open(os.path.join(targdir,filename), "w") as target:
            target.write(pov_header) 
            rd = RD()
            draw_poly(rd, target)

            for idx, p in enumerate(twelve_around_one(rd)):
                if idx <= frame_id:
                    draw_vert(neighbors[idx], 
                              c="rgb <1,0,0>", 
                              r=0.5, t=target)
                draw_poly(p, target)
                
            if 12 == frame_id:
                draw_vert(neighbors[12], 
                          c="rgb <1,0,0>", 
                          r=0.5, t=target)
 
def animation11(targdir="anim11"):
    targdir = os.path.join(".",targdir)
    if not os.path.isdir(targdir):
        os.mkdir(targdir)

    thirteen_balls = [Qvector((0,0,0,0))] + list(IVM_DIRS)
     
    neighbors = one_hop_away(thirteen_balls)
    
    colors = cycle(["rgb <1,0,0>", "rgb <.8,0,.2>", "rgb <.6,0,.4>", 
                    "rgb <.4,0,.6>", "rgb <.2,0,.8>", "rgb <0,.5,.2>", 
                    "rgb <0,.7,.2>"])
    
    rainbow = [next(colors) for _ in range(13)]
    
    for frame_id in range(13):
        filename = f"balls{frame_id:03}.pov"
            
        with open(os.path.join(targdir,filename), "w") as target:
            target.write(pov_header) 
            rd = RD()
            draw_poly(rd, target)

            for idx, p in enumerate(twelve_around_one(rd)):
                if idx <= frame_id:
                    draw_vert(neighbors[idx], 
                              rainbow[idx],
                              r=0.4, t=target)
                draw_poly(p, target)
                
            if 12 == frame_id:
                draw_vert(neighbors[12],
                          rainbow[12],
                          r=0.4, t=target)
if __name__ == "__main__":
    # animation5()
    # sphere_packing()
    # jitterbug()
    # animation()
    # animation10()
    # animation11()
    # logo()
    iw()
    