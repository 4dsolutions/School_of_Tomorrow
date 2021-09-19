#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 11:40:54 2020

@author: Kirby Urner

Sept 19, 2021:  altered to work with new qray.py 
                wherein Qvector.xyz is a property
"""

class Polyhedron:
    """
    Designed to be subclassed, not used directly
    """
    
    def scale(self, scalefactor):
        if hasattr(self, "volume"):
            self.volume = scalefactor ** 3
        newverts = {}
        for v in self.vertexes:
            newverts[v] = self.vertexes[v] * scalefactor
        newme = type(self)()
        newme.vertexes = newverts      # substitutes new guts
        newme.edges = newme._distill() # update edges to use new verts

        return newme

    __mul__ = __rmul__ = scale

    def translate(self, vector):
        newverts = {}
        for v in self.vertexes:
            newverts[v] = self.vertexes[v] + vector
        newme = type(self)()
        newme.vertexes = newverts      # substitutes new tent stakes
        if hasattr(self, "center"):    # shift center before suppress!
            newme.center = self.center + vector
        if hasattr(self, "suppress"):
            newme.suppress = self.suppress
            if newme.suppress:
                newme.faces = newme._suppress()
        newme.edges = newme._distill() # update edges to use new verts          
        return newme

    __add__ = __radd__ = translate
    
    def _distill(self):

        edges = []
        unique = set()
        
        for f in self.faces:
            for pair in zip(f , f[1:] + (f[0],)):
                unique.add( tuple(sorted(pair)) )
        
        for edge in unique:
            edges.append( Edge(self.vertexes[edge[0]],
                               self.vertexes[edge[1]]) )

        return edges 

class Edge:

    """
    Edges are defined by two Vectors (above) and express as cylinder via draw().
    """

    def __init__(self, v0, v1):
        self.v0 = v0  # actual coordinates, not a letter label
        self.v1 = v1
             
    def __repr__(self):
        return 'Edge from %s to %s' % (self.v0, self.v1)

def draw_vert(v, c, r, t): 
    v = v.xyz
    x,y,z = v.x, v.y, v.z
    data = "< %s, %s, %s >" % (x,y,z), r, c
    template = ("sphere { %s, %s texture "
                "{ pigment { color %s } } no_shadow }")
    print(template % data, file=t)
    
def draw_face(f, c, t): pass

def draw_edge(e, c, r, t):
    v = e.v0.xyz
    v0 = "< %s, %s, %s >" % (v.x, v.y, v.z)
    v = e.v1.xyz
    v1 = "< %s, %s, %s >" % (v.x, v.y, v.z)
    data = (v0, v1, r, c)
    template = ("cylinder { %s, %s, %s texture "
                        "{pigment { color %s } } no_shadow }")
    print(template % data, file=t)
    

def draw_poly(p, the_file, v=True, f=False, e=True):
    
    ec = p.edge_color
    er = p.edge_radius
    vc = p.vert_color
    vr = p.vert_radius
    fc = p.face_color
    
    if v:
        for v in p.vertexes.values():
            draw_vert(v, vc, vr, the_file)

    if f:
        for f in p.faces:
            draw_face(f, fc, the_file)

    if e:
        for e in p.edges:
            draw_edge(e, ec, er, the_file)
     
import math
from qrays import Qvector, Vector
PHI = (1 + math.sqrt(5))/2.0

ORIGIN = Qvector((0,0,0,0))
A = Qvector((1,0,0,0))
B = Qvector((0,1,0,0))
C = Qvector((0,0,1,0))
D = Qvector((0,0,0,1))

E,F,G,H     = B+C+D, A+C+D, A+B+D, A+B+C
I,J,K,L,M,N = A+B, A+C, A+D, B+C, B+D, C+D
O,P,Q,R,S,T = I+J, I+K, I+L, I+M, N+J, N+K
U,V,W,X,Y,Z = N+L, N+M, J+L, L+M, M+K, K+J

# OPPOSITE DIAGONALS
# ZY WX
# RV OS
# TU PQ
control = (Z - T).length()

midface = (Z + Y)
gold    = 0.5 * PHI * midface/midface.length()
Zi = gold + J/J.length() * control/2
Yi = gold + M/M.length() * control/2

midface = (W + X)
gold    = 0.5 * PHI * midface/midface.length()
Wi = gold + J/J.length() * control/2
Xi = gold + M/M.length() * control/2

midface = (R + V)
gold    = 0.5 * PHI * midface/midface.length()
Ri = gold + I/I.length() * control/2
Vi = gold + N/N.length() * control/2

midface = (O + S)
gold    = 0.5 * PHI * midface/midface.length()
Oi = gold + I/I.length() * control/2
Si = gold + N/N.length() * control/2

midface = (T + U)
gold    = 0.5 * PHI * midface/midface.length()
Ti = gold + K/K.length() * control/2
Ui = gold + L/L.length() * control/2

midface = (P + Q)
gold    = 0.5 * PHI * midface/midface.length()
Pi = gold + K/K.length() * control/2
Qi = gold + L/L.length() * control/2

class Tetrahedron(Polyhedron):
    """
    Tetrahedron
    """
    
    def __init__(self):
        # POV-Ray
        self.edge_color = "rgb <{}, {}, {}>".format(1, 165/255, 0) # orange
        self.edge_radius= 0.03
        self.vert_color = "rgb <{}, {}, {}>".format(1, 165/255, 0) # orange
        self.vert_radius= 0.03
        self.face_color = "rgb <0, 0, 0>" # not used 
        
        verts = dict(a = Qvector((1,0,0,0)), #A
                     b = Qvector((0,1,0,0)), #B
                     c = Qvector((0,0,1,0)), #C
                     d = Qvector((0,0,0,1))) #D
        
        self.name = "Tetrahedron"
        self.volume = 1  # per Concentric Hierarchy
        self.center = ORIGIN

        # 4 vertices
        self.vertexes = verts
        
        # 4 faces
        self.faces = (('a','b','c'),('a','c','d'),
                      ('a','d','b'),('b','d','c'))

        self.edges = self._distill()

class InvTetrahedron(Polyhedron):
    """
    Inverse Tetrahedron
    """
    
    def __init__(self):
        # POV-Ray
        self.edge_color = "rgb <{}, {}, {}>".format(0, 0, 0) # black
        self.edge_radius= 0.03
        self.vert_color = "rgb <{}, {}, {}>".format(0, 0, 0) # black
        self.vert_radius= 0.03
        self.face_color = "rgb <0, 0, 0>" # not used 
        
        verts = dict(e = -Qvector((1,0,0,0)), #E
                     f = -Qvector((0,1,0,0)), #F
                     g = -Qvector((0,0,1,0)), #G
                     h = -Qvector((0,0,0,1))) #H
        
        self.name = "InvTetrahedron"
        self.volume = 1  # per Concentric Hierarchy
        self.center = ORIGIN
        
        # 4 vertices
        self.vertexes = verts
        
        # 4 faces
        self.faces = (('e','f','g'),('e','g','h'),
                      ('e','h','f'),('f','h','g'))

        self.edges = self._distill()
        
class Cube (Polyhedron):
    """
    Cube
    """

    def __init__(self):
        # POV-Ray
        self.edge_color = "rgb <0, 1, 0>"
        self.edge_radius= 0.03
        self.vert_color = "rgb <0, 1, 0>"
        self.vert_radius= 0.03
        self.face_color = "rgb <0, 0, 0>"

        verts = {}
        for vert_label in "abcdefgh":
            # keep the uppercase A-Z universe (namespace) unobstructed
            verts[vert_label] = eval(vert_label.upper())
                
        self.name = "Cube"
        self.volume = 3  # per Concentric Hierarchy
        self.center = ORIGIN
        
        # 8 vertices
        self.vertexes = verts
        
        # 6 faces
        self.faces = (('a','f','c','h'),('h','c','e','b'),
                      ('b','e','d','g'),('g','d','f','a'),
                      ('c','f','d','e'),('a','h','b','g'))

        self.edges = self._distill()
        
class Cuboid (Polyhedron):
    """
    Cuboid with height, width, depth = sqrt(1), sqrt(2), sqrt(4)
    """

    def __init__(self):
        # POV-Ray
        self.edge_color = "rgb <255/255, 20/255, 147/255>"
        self.edge_radius= 0.03
        self.vert_color = "rgb <255/255, 20/255, 147/255>"
        self.vert_radius= 0.03
        self.face_color = "rgb <0, 0, 0>"

        verts = {}
        verts['A'] = Vector(( 1,  0.5,  math.sqrt(2)/2))
        verts['B'] = Vector(( 1, -0.5,  math.sqrt(2)/2))       
        verts['C'] = Vector(( 1, -0.5, -math.sqrt(2)/2))        
        verts['D'] = Vector(( 1,  0.5, -math.sqrt(2)/2))
        verts['E'] = Vector((-1,  0.5,  math.sqrt(2)/2))
        verts['F'] = Vector((-1, -0.5,  math.sqrt(2)/2))
        verts['G'] = Vector((-1, -0.5, -math.sqrt(2)/2))
        verts['H'] = Vector((-1,  0.5, -math.sqrt(2)/2))
                
        self.name = "Cuboid"
        self.volume = 8  # per Concentric Hierarchy
        self.center = ORIGIN
        
        # 8 vertices
        self.vertexes = verts
        
        # 6 faces
        self.faces = (('A','B','C','D'),('E','F','G','H'),
                      ('A','E','F','B'),('D','H','G','C'),
                      ('A','E','H','D'),('B','F','G','C'))

        self.edges = self._distill()
        
class Octahedron (Polyhedron):
    """
    Octahedron
    """

    def __init__(self):
        # POV-Ray
        self.edge_color = "rgb <1, 0, 0>"
        self.edge_radius= 0.03
        self.vert_color = "rgb <1, 0, 0>"
        self.vert_radius= 0.03
        self.face_color = "rgb <0, 0, 0>"
        
        verts = {}
        for vert_label in "ijklmn":
            # keep the uppercase A-Z universe unobstructed
            verts[vert_label] = eval(vert_label.upper())

        self.name = "Octahedron"
        self.volume = 4  # per Concentric Hierarchy
        self.center = ORIGIN
        
        # 6 vertices
        self.vertexes = verts

        # 8 faces
        self.faces = (('j','k','i'),('j','i','l'),('j','l','n'),('j','n','k'),                      
                      ('m','k','i'),('m','i','l'),('m','l','n'),('m','n','k'))

        self.edges = self._distill()
        
class RD (Polyhedron):
        """
        Rhombic Dodecahedron
        """

        def __init__(self):
            self.edge_color = "rgb <0, 0, 1>"
            self.edge_radius= 0.03
            self.vert_color = "rgb <0, 0, 1>"
            self.vert_radius= 0.03
            self.face_color = "rgb <0, 0, 0>"

            verts = {}
            for vert_label in "abcdefghijklmn":
                # keep the uppercase A-Z universe unobstructed
                verts[vert_label] = eval(vert_label.upper())
                
            self.name = "RD"
            self.volume = 6  # per Concentric Hierarchy
            self.center = ORIGIN
            
            # 14 vertices
            self.vertexes = verts

            # 12 faces
            # I,J,K,L,M,N = A+B, A+C, A+D, B+C, B+D, C+D
            self.faces = (('j','f','k','a'),('j','f','n','c'),('j','c','l','h'),('j','h','i','a'),
                          ('m','d','k','g'),('m','d','n','e'),('m','e','l','b'),('m','b','i','g'),
                          ('k','d','n','f'),('n','c','l','e'),('l','h','i','b'),('i','a','k','g'))

            self.edges = self._distill()

class Icosahedron (Polyhedron):

    def __init__(self):
        # 8 vertices
        self.edge_color = "rgb <0, 1, 1>"
        self.edge_radius= 0.03
        self.vert_color = "rgb <0, 1, 1>"
        self.vert_radius= 0.03
        self.face_color = "rgb <0, 0, 0>"

        self.vertexes = dict(o =  Oi,
                             p =  Pi,
                             q =  Qi,
                             r =  Ri,
                             s =  Si,
                             t =  Ti,
                             u =  Ui,
                             v =  Vi,
                             w =  Wi,
                             x =  Xi,
                             y =  Yi,
                             z =  Zi)
        
        self.name = "Icosahedron"
        self.volume = 18.51
        self.center = ORIGIN
        # 20 faces
        # OPPOSITE DIAGONALS of cubocta
        # ZY WX
        # RV OS
        # TU PQ
        self.faces = (('o','w','s'),('o','z','s'),
                      ('z','p','y'),('z','t','y'),
                      ('t','v','u'),('t','s','u'),
                      ('w','q','x'),('w','u','x'),
                      ('p','o','q'),('p','r','q'),
                      ('r','y','v'),('r','x','v'),
                      ('z','s','t'),('t','y','v'),
                      ('y','p','r'),('r','q','x'),
                      ('x','u','v'),('u','s','w'),
                      ('w','q','o'),('o','z','p'))

        self.edges = self._distill()

class Cuboctahedron (Polyhedron):

    def __init__(self):
        # 8 vertices
        self.edge_color = "rgb <1, 1, 0>"
        self.edge_radius= 0.03
        self.vert_color = "rgb <1, 1, 0>"
        self.vert_radius= 0.03
        self.face_color = "rgb <0, 0, 0>"

        self.vertexes = dict(o =  O,
                             p =  P,
                             q =  Q,
                             r =  R,
                             s =  S,
                             t =  T,
                             u =  U,
                             v =  V,
                             w =  W,
                             x =  X,
                             y =  Y,
                             z =  Z)
        self.name = "Cuboctahedron"
        self.volume = 20
        self.center = ORIGIN
        
        # 6 faces
        self.faces = (('o','w','s','z'),('z','p','y','t'),
                      ('t','v','u','s'),('w','q','x','u'),
                      ('o','p','r','q'),('r','y','v','x'),
                      ('z','s','t'),('t','y','v'),
                      ('y','p','r'),('r','q','x'),
                      ('x','u','v'),('u','s','w'),
                      ('w','q','o'),('o','z','p'))

        self.edges = self._distill()
        
class Struts(Polyhedron):
    
    def __init__(self, c=None, ico=None, suppress=False):

        self.edge_color = "rgb <1, 0, 0>"
        self.edge_radius= 0.02
        self.vert_color = "rgb <1, 0, 0>"
        self.vert_radius= 0.02
        self.face_color = "rgb <0, 0, 0>"
        self.suppress = suppress
        
        if not c and not ico:
            c = Cube()
            ico = Icosahedron()
        
        self.vertexes = dict(
            # cube mid-edges
            af = (c.vertexes['a'] + c.vertexes['f'])/2,
            ag = (c.vertexes['a'] + c.vertexes['g'])/2,
            ah = (c.vertexes['a'] + c.vertexes['h'])/2,
            be = (c.vertexes['b'] + c.vertexes['e'])/2,
            bh = (c.vertexes['b'] + c.vertexes['h'])/2,
            bg = (c.vertexes['b'] + c.vertexes['g'])/2,
            ce = (c.vertexes['c'] + c.vertexes['e'])/2,
            cf = (c.vertexes['c'] + c.vertexes['f'])/2,
            ch = (c.vertexes['c'] + c.vertexes['h'])/2,
            de = (c.vertexes['d'] + c.vertexes['e'])/2,
            df = (c.vertexes['d'] + c.vertexes['f'])/2,
            dg = (c.vertexes['d'] + c.vertexes['g'])/2,
            # icosa mid-edges
            # OPPOSITE DIAGONALS of cubocta
            # ZY WX
            # RV OS
            # TU PQ
            os = (ico.vertexes['o'] + ico.vertexes['s'])/2,
            pq = (ico.vertexes['p'] + ico.vertexes['q'])/2,
            rv = (ico.vertexes['r'] + ico.vertexes['v'])/2,
            tu = (ico.vertexes['t'] + ico.vertexes['u'])/2,
            wx = (ico.vertexes['w'] + ico.vertexes['x'])/2,
            yz = (ico.vertexes['y'] + ico.vertexes['z'])/2
        )

        self.name  = 'struts'
        self.center = ico.center
            
        self.faces = (('os', 'af'), ('os', 'ch'),
                      ('rv', 'be'), ('rv', 'dg'), 
                      ('tu', 'cf'), ('tu', 'de'),
                      ('pq', 'ah'), ('pq', 'bg'),
                      ('yz', 'ag'), ('yz', 'df'),
                      ('wx', 'bh'), ('wx', 'ce'))   

        if self.suppress:
            self.faces = self._suppress()
        
        self.edges = self._distill()
        
    def _suppress(self):
        """
        A global IVM of integral Qray positions is expected for 
        the suppress feature to work. This could be an n-frequency
        cuboctahedron or perhaps a layered tetrahedron of half-
        octahedron of balls.
        """
        global IVM
        keep = []
        # print("Suppressing disconnected edges")
        for f in self.faces:
            # print(f, self.center)
            neighbor = self.center + eval(f[1][0].upper()) + eval(f[1][1].upper())
            # print("Neighbor=", neighbor)
            for layer in IVM:
                if neighbor in IVM[layer]:
                    # print("Bing!")
                    keep.append(f)
                    break
            else:
                pass
                # print("Not found")
        return keep     
        
from itertools import permutations
g = permutations((2,1,1,0))
unique = {p for p in g}  # set comprehension

def twelve_around_one(p):
    twelve = [ ]
    for v in unique:
        trans_vector = Qvector(v)
        twelve.append(p + trans_vector)
    return twelve

pov_header = \
"""
// Persistence of Vision Ray Tracer Scene Description File
// File: xyz.pov
// Vers: 3.6
// Desc: test file
// Date: Sat Sep  7 09:49:33 2019
// Auth: me
// ==== Standard POV-Ray Includes ====
#include "colors.inc"     // Standard Color definitions
// include "textures.inc"   // Standard Texture definitions
// include "functions.inc"  // internal functions usable in user defined functions

// ==== Additional Includes ====
// Don't have all of the following included at once, it'll cost memory and time
// to parse!
// --- general include files ---
// include "chars.inc"      // A complete library of character objects, by Ken Maeno
// include "skies.inc"      // Ready defined sky spheres
// include "stars.inc"      // Some star fields
// include "strings.inc"    // macros for generating and manipulating text strings

// --- textures ---
// include "finish.inc"     // Some basic finishes
// include "glass.inc"      // Glass textures/interiors
// include "golds.inc"      // Gold textures
// include "metals.inc"     // Metallic pigments, finishes, and textures
// include "stones.inc"     // Binding include-file for STONES1 and STONES2
// include "stones1.inc"    // Great stone-textures created by Mike Miller
// include "stones2.inc"    // More, done by Dan Farmer and Paul Novak
// include "woodmaps.inc"   // Basic wooden colormaps
// include "woods.inc"      // Great wooden textures created by Dan Farmer and Paul Novak

global_settings {assumed_gamma 1.0}
global_settings {ambient_light rgb<1, 1, 1> }

// perspective (default) camera
camera {
  location  <4, 0.1, 0.2>
  rotate    <35, 35, 10.0>
  look_at   <0.0, 0.0,  0.0>
  right     x*image_width/image_height
}

// create a regular point light source
light_source {
  0*x                  // light's position (translated below)
  color rgb <1,1,1>    // light's color
  translate <-20, 15, 10>
}

// create a regular point light source
light_source {
  0*x                  // light's position (translated below)
  color rgb <1,1,1>    // light's color
  translate <20, -15, -10>
}

background { color rgb <1.0, 1.0, 1.0> }
"""