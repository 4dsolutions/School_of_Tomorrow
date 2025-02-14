#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 11:40:54 2020

@author: Kirby Urner

The qrays.py module provides more context.

This implementation of Matryoskah doll polys
(nested) is yet another iteration of what I do:
output in POV-Ray scene description language
plus others: VRML, VPython, Blender, over the
years. The overall schema is from Synergetics
(R. B. Fuller), including the volumes table.

The polys rely on an index of Qvectors, which
inherit from Vectors in qrays.py, but for a 
poly one needs face tuples, connecting 
surface points into polygons. From the faces
data structure e.g.

# 4 faces
self.faces = (('a','b','c'),('a','c','d'),
              ('a','d','b'),('b','d','c'))

the Polyhedron superclass is able to distill
the edges (vector pairs, connecting endpoints).

self.edges = self._distill()

Jan  22, 2025:  rethink deriving icosa from cubocta vectors
Jan  21, 2025:  adding new "scapes" (poly vistas)
Oct  13, 2024:  write new tests, rewrite test6, simplify constants
Oct  06, 2024:  test16 for 7-frame animated GIF
Oct  05, 2024:  test15 for 9-frame animated GIF 
Sept-Oct,2024:  keep adding new tests (scenarios) to make povs
Sept 21, 2024:  added PD, RT, implemented faces as polygons
Sept 19, 2021:  altered to work with new qray.py 
                wherein Qvector.xyz is a property
"""

from qrays import Qvector, Vector
import sympy as sy  
from sympy import sqrt as rt2

two  = sy.Integer(2)
one  = sy.Integer(1)
half = sy.Rational(1, 2)
zero = sy.Integer(0)

PHI = (one + rt2(5))/two

ORIGIN = Qvector((zero, zero, zero, zero))
A = Qvector((one, zero, zero, zero))
B = Qvector((zero, one, zero, zero))
C = Qvector((zero, zero, one, zero))
D = Qvector((zero, zero, zero ,one))

# from Wikipedia (Quadray Coordinates)
E,F,G,H     = B+C+D, A+C+D, A+B+D, A+B+C
I,J,K,L,M,N = A+B, A+C, A+D, B+C, B+D, C+D
O,P,Q,R,S,T = I+J, I+K, I+L, I+M, N+J, N+K
U,V,W,X,Y,Z = N+L, N+M, J+L, L+M, M+K, K+J

sfactor = 20/(5 * rt2(2) * PHI**2) # VE/icosa vol ratio
half = sy.Rational(1,2)

# OPPOSITE DIAGONALS
# ZY WX
# RV OS
# TU PQ
control = (Z - T).length() # surface edge of Cubocta

def phi_rect(v0, v1):
    """
    develop 3 phi-rectangles from cubocta face diagonals
    takes a pair of points from square faces, returns a pair 
    """
    gold    = (v0+v1).unit_vector() * (control*PHI)/two
    offset  = (v0-v1).unit_vector()
    return (gold + (offset * control/two),
            gold - (offset * control/two))

# icosahedral points
Zi, Yi = phi_rect(Z, Y)
Wi, Xi = phi_rect(W, X)
Ri, Vi = phi_rect(R, V)
Oi, Si = phi_rect(O, S)
Ti, Ui = phi_rect(T, U)
Pi, Qi = phi_rect(P, Q)

class Polyhedron:
    """
    Designed to be subclassed, not used directly
    """
    
    def scale(self, scalefactor):
        if hasattr(self, "volume"):
            new_volume = self.volume * scalefactor ** 3
        newverts = {}
        for v in self.vertexes:
            newverts[v] = self.vertexes[v] * scalefactor
        newme = type(self)()
        newme.volume   = new_volume       # new volume
        newme.vertexes = newverts         # substitutes new guts
        newme.edges    = newme._distill() # update edges to use new verts

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
            
        self.unique = unique # hack to keep edges as symbolic pairs
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

#=== DRAW ROUTINES ===

def draw_vert(v, c, r, t, *, texture = False): 
    v = v.xyz
    x,y,z = float(v.x), float(v.y), float(v.z)
    data = "< %s, %s, %s >" % (x,y,z), float(r), c
    if not texture:
        template = ("sphere { %s, %s texture "
                    "{ pigment { color %s } } no_shadow }")
    else:
        template = ("sphere { %s, %s texture "
                    "{ %s } no_shadow }")    
    print(template % data, file=t)    
    
def draw_face(p, f, c, t, *, texture = False):
    """
    POLYGON:
    polygon
    {
        Number_Of_Points, <Point_1> <Point_2>... <Point_n>
        [OBJECT_MODIFIER...]
    }
    
    Parameters
    ----------
    f : tuple of tuples
        vertexes around a face
    f : tuple of strings
        labels of verts around a face
    c : string
        color info
    t : file object

    Returns
    -------
    None.

    """
    data = ""
    num_points = len(f)
    for v in f:
        coords = p.vertexes[v].xyz
        x,y,z = float(coords.x), float(coords.y), float(coords.z)
        data += "< %s, %s, %s > " % (x, y, z)
    
    if not texture:
        template = ("polygon { %s, %s texture "
                    "{ pigment { color %s } } no_shadow }")  
        print(template % (num_points, data, c), file=t)
    else: 
        template = ("polygon { %s, %s texture "
                    "{ %s } no_shadow }")      
    print(template % (num_points, data, c), file=t)        

def draw_edge(e, c, r, t, *, texture=False):
    v = e.v0.xyz
    v0 = "< %s, %s, %s >" % (float(v.x), float(v.y), float(v.z))
    v = e.v1.xyz
    v1 = "< %s, %s, %s >" % (float(v.x), float(v.y), float(v.z))
    data = (v0, v1, float(r), c)
    if not texture:
        template = ("cylinder { %s, %s, %s texture "
                            "{pigment { color %s } } no_shadow }")
    else:
        template = ("cylinder { %s, %s, %s texture "
                            "{ %s } no_shadow }")        
    print(template % data, file=t)
    

def draw_poly(p, the_file, v=True, f=False, e=True, *, texture=False):
    
    ec = p.edge_color
    er = p.edge_radius
    vc = p.vert_color
    vr = p.vert_radius
    fc = p.face_color
    
    if v:
        alt_color  = "rgb <{}, {}, {}>".format(1, 0, 0) # red
        alt_radius = 0.05
        for label, v in p.vertexes.items():
            if label == None: # replace None with exceptional v e.g. 'z'
                draw_vert(v, alt_color, alt_radius, the_file, texture=texture)
            else:
                draw_vert(v, vc, vr, the_file, texture=texture)

    if f:
        for f in p.faces:
            draw_face(p, f, fc, the_file, texture=texture)

    if e:
        for e in p.edges:
            draw_edge(e, ec, er, the_file, texture=texture)
     
#=== REPORTS ===

def edge_lengths(shape):
    return [(e.v0 - e.v1).length().evalf() 
            for e in shape.edges]

def globals():
    print(\
f"""\
A  : {A.length().evalf()}
B  : {B.length().evalf()}
C  : {C.length().evalf()}
D  : {D.length().evalf()}
E  : {E.length().evalf()}
F  : {F.length().evalf()}
G  : {G.length().evalf()}
H  : {H.length().evalf()}
I  : {I.length().evalf()}
J  : {J.length().evalf()}
K  : {K.length().evalf()}
L  : {L.length().evalf()}
M  : {M.length().evalf()}
N  : {N.length().evalf()}
O  : {O.length().evalf()}
P  : {P.length().evalf()}
Q  : {Q.length().evalf()}
R  : {R.length().evalf()}
S  : {S.length().evalf()}
T  : {T.length().evalf()}
U  : {U.length().evalf()} 
V  : {V.length().evalf()}
W  : {W.length().evalf()}
X  : {X.length().evalf()}
Y  : {Y.length().evalf()}
Z  : {Z.length().evalf()}
Oi : {Oi.length().evalf()}
Pi : {Pi.length().evalf()}
Qi : {Qi.length().evalf()}
Ri : {Ri.length().evalf()}
Si : {Si.length().evalf()}
Ti : {Ti.length().evalf()}
Ui : {Ui.length().evalf()}
Vi : {Vi.length().evalf()}
Wi : {Wi.length().evalf()}
Zi : {Zi.length().evalf()}
""")
    
#=== POLYS ===

class Tetrahedron(Polyhedron):
    """
    Tetrahedron
    """
    
    def __init__(self):
        # POV-Ray
        self.edge_color = "rgb <{}, {}, {}>".format(1, 140/255, 0) # orange
        self.edge_radius= 0.03
        self.vert_color = "rgb <{}, {}, {}>".format(1, 140/255, 0) # orange
        self.vert_radius= 0.03
        self.face_color = self.edge_color # often not used 
        
        verts = {}
        for vert_label in "abcd":
            # keep the uppercase A-Z universe (namespace) unobstructed
            verts[vert_label] = eval(vert_label.upper())
        
        self.name = "Tetrahedron"
        self.nick = "Tet"
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
        self.edge_color = "rgb <{}, {}, {}>".format(67/255, 70/255, 75/255) # black
        self.edge_radius= 0.03
        self.vert_color = self.edge_color
        self.vert_radius= 0.03
        self.face_color = "rgb <0, 0, 0>" # not used 
        self.face_color = self.edge_color # often not used 
        
        verts = {}
        for vert_label in "efgh":
            # keep the uppercase A-Z universe (namespace) unobstructed
            verts[vert_label] = eval(vert_label.upper())
        
        self.name = "Inverse Tetrahedron"
        self.nick = "~Tet"
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
        self.face_color = self.edge_color 

        verts = {}
        for vert_label in "abcdefgh":
            # keep the uppercase A-Z universe (namespace) unobstructed
            verts[vert_label] = eval(vert_label.upper())
                
        self.name = "Cube"
        self.nick = "Cube"
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
        self.face_color = "rgb <255/255, 20/255, 147/255>"

        verts = {}
        verts['A'] = Vector(( one,  half,  rt2(2)/2))
        verts['B'] = Vector(( one, -half,  rt2(2)/2))       
        verts['C'] = Vector(( one, -half, -rt2(2)/2))        
        verts['D'] = Vector(( one,  half, -rt2(2)/2))
        verts['E'] = Vector((-one,  half,  rt2(2)/2))
        verts['F'] = Vector((-one, -half,  rt2(2)/2))
        verts['G'] = Vector((-one, -half, -rt2(2)/2))
        verts['H'] = Vector((-one,  half, -rt2(2)/2))
                
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
        self.face_color = "rgb <1, 0, 0>"
        
        verts = {}
        for vert_label in "ijklmn":
            # keep the uppercase A-Z universe unobstructed
            verts[vert_label] = eval(vert_label.upper())

        self.name = "Octahedron"
        self.nick = "Oct"
        self.volume = 4  # per Concentric Hierarchy (84S + 20S)
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
            self.face_color = self.edge_color 

            verts = {}
            for vert_label in "abcdefghijklmn":
                # keep the uppercase A-Z universe unobstructed
                verts[vert_label] = eval(vert_label.upper())

            self.name = "Rhombic Dodecahedron"
            self.nick = "RD"
            self.volume = 6  # per Concentric Hierarchy
            self.center = ORIGIN
            
            # 14 vertices
            self.vertexes = verts

            # 12 faces
            # I,J,K,L,M,N = A+B, A+C, A+D, B+C, B+D, C+D
            self.faces = (('j','f','k','a'),('j','f','n','c'),('j','c','l','h'),
                          ('j','h','i','a'),('m','d','k','g'),('m','d','n','e'),
                          ('m','e','l','b'),('m','b','i','g'),('k','d','n','f'),
                          ('n','c','l','e'),('l','h','i','b'),('i','a','k','g'))

            self.edges = self._distill()

class Icosahedron (Polyhedron):

    def __init__(self):
        # 20 vertices
        self.edge_color = "rgb <0, 1, 1>"
        self.edge_radius= 0.03
        self.vert_color = "rgb <0, 1, 1>"
        self.vert_radius= 0.03
        self.face_color = self.edge_color 

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
        self.nick = "Ico"
        self.volume = 5 * rt2(2) * PHI**2
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

class PD (Polyhedron):  
# Pentagonal Dodecahedron

    def __init__(self):
        # Sienna Brown rgb(160,82,45)
        self.edge_color = "rgb <%s, %s, %s>" % (160/255, 82/255, 45/255)
        self.edge_radius= 0.03
        self.vert_color = self.edge_color
        self.vert_radius= 0.03
        self.face_color = self.edge_color 
        
        # 20 vertexes
        # V + F = E + 2; 20 + 12 = 30 + 2
        icosa_midedge = ((Wi + Qi)/two).length()
        cross_wise = control/PHI * half
        sk = rt2(icosa_midedge**2 + cross_wise**2) # scale factor
        self.vertexes = dict(osw = sk * (Oi + Wi + Si).unit_vector(),
                             osz = sk * (Oi + Zi + Si).unit_vector(),
                             pyz = sk * (Zi + Pi + Yi).unit_vector(),
                             tyz = sk * (Zi + Ti + Yi).unit_vector(),
                             tuv = sk * (Ti + Vi + Ui).unit_vector(),
                             stu = sk * (Ti + Si + Ui).unit_vector(),
                             qwx = sk * (Wi + Qi + Xi).unit_vector(),
                             uwx = sk * (Wi + Ui + Xi).unit_vector(),
                             opq = sk * (Pi + Oi + Qi).unit_vector(),
                             pqr = sk * (Pi + Ri + Qi).unit_vector(),
                             rvy = sk * (Ri + Yi + Vi).unit_vector(),
                             rvx = sk * (Ri + Xi + Vi).unit_vector(),
                             stz = sk * (Zi + Si + Ti).unit_vector(),
                             tvy = sk * (Ti + Yi + Vi).unit_vector(),
                             pry = sk * (Yi + Pi + Ri).unit_vector(),
                             qrx = sk * (Ri + Qi + Xi).unit_vector(),
                             uvx = sk * (Xi + Ui + Vi).unit_vector(),
                             suw = sk * (Ui + Si + Wi).unit_vector(),
                             oqw = sk * (Wi + Qi + Oi).unit_vector(),
                             opz = sk * (Oi + Zi + Pi).unit_vector())
        
        self.name = "Pentagonal Dodecahedron"            
        self.nick = "PD"
        self.volume = 3 * rt2(2) * (PHI**2 + 1)
        self.center = ORIGIN
        # 12 faces
        self.faces = (('oqw', 'opq', 'opz', 'osz', 'osw'), # o
                      ('opq', 'pqr', 'pry', 'pyz', 'opz'), # p
                      ('opq', 'pqr', 'qrx', 'qwx', 'oqw'), # q
                      ('qrx', 'pqr', 'pry', 'rvy', 'rvx'), # r
                      ('stu', 'suw', 'osw', 'osz', 'stz'), # s
                      ('stu', 'stz', 'tyz', 'tvy', 'tuv'), # t
                      ('suw', 'uwx', 'uvx', 'tuv', 'stu'), # u
                      ('tvy', 'tuv', 'uvx', 'rvx', 'rvy'), # v
                      ('osw', 'oqw', 'qwx', 'uwx', 'suw'), # w  
                      ('uwx', 'qwx', 'qrx', 'rvx', 'uvx'), # x
                      ('pyz', 'pry', 'rvy', 'tvy', 'tyz'), # y
                      ('osz', 'opz', 'pyz', 'tyz', 'stz'), # z
                      )
        

        self.edges = self._distill()

class RT (Polyhedron):
    # Rhombic Triacontahedron

    def __init__(self):
        # Purple Heart rgb(105,53,156)
        self.edge_color = "rgb <%s, %s, %s>" % (105/255, 53/255, 156/255)
        self.edge_radius= 0.03
        self.vert_color = self.edge_color
        self.vert_radius= 0.03
        self.face_color = self.edge_color
        
        # 32 vertexes
        # V + F = E + 2; 32 + 30 = 60 + 2
        icosa_midedge = ((Wi + Qi)/two).length()
        cross_wise = control/PHI * half
        sk = rt2(icosa_midedge**2 + cross_wise**2) # scale factor
        self.vertexes = dict(osw = sk * (Oi + Wi + Si).unit_vector(),
                             osz = sk * (Oi + Zi + Si).unit_vector(),
                             pyz = sk * (Zi + Pi + Yi).unit_vector(),
                             tyz = sk * (Zi + Ti + Yi).unit_vector(),
                             tuv = sk * (Ti + Vi + Ui).unit_vector(),
                             stu = sk * (Ti + Si + Ui).unit_vector(),
                             qwx = sk * (Wi + Qi + Xi).unit_vector(),
                             uwx = sk * (Wi + Ui + Xi).unit_vector(),
                             opq = sk * (Pi + Oi + Qi).unit_vector(),
                             pqr = sk * (Pi + Ri + Qi).unit_vector(),
                             rvy = sk * (Ri + Yi + Vi).unit_vector(),
                             rvx = sk * (Ri + Xi + Vi).unit_vector(),
                             stz = sk * (Zi + Si + Ti).unit_vector(),
                             tvy = sk * (Ti + Yi + Vi).unit_vector(),
                             pry = sk * (Yi + Pi + Ri).unit_vector(),
                             qrx = sk * (Ri + Qi + Xi).unit_vector(),
                             uvx = sk * (Xi + Ui + Vi).unit_vector(),
                             suw = sk * (Ui + Si + Wi).unit_vector(),
                             oqw = sk * (Wi + Qi + Oi).unit_vector(),
                             opz = sk * (Oi + Zi + Pi).unit_vector())
        
        self.vertexes.update(dict(
                             o =  Oi,
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
                             z =  Zi))                    
        self.name = "Rhombic Triacontahedron"
        self.nick = "RT"
        self.volume = 20 * rt2(sy.Rational(9, 8))
        self.center = ORIGIN
        # 30 faces
        self.faces = (('s', 'stz', 'z', 'osz'),
                      ('s', 'osz', 'o', 'osw'),
                      ('s', 'suw', 'w', 'osw'),
                      ('s', 'suw', 'u', 'stu'),
                      ('s', 'stu', 't', 'stz'),
                      ('r', 'qrx', 'q', 'pqr'),
                      ('r', 'pry', 'p', 'pqr'),
                      ('r', 'pry', 'y', 'rvy'),
                      ('r', 'rvx', 'v', 'rvy'),
                      ('r', 'qrx', 'x', 'rvx'),
                      ('v', 'tuv', 't', 'tvy'),
                      ('t', 'tyz', 'y', 'tvy'),
                      ('y', 'tyz', 'z', 'pyz'),
                      ('z', 'pyz', 'p', 'opz'),
                      ('p', 'opz', 'o', 'opq'),
                      ('o', 'oqw', 'q', 'opq'),
                      ('q', 'oqw', 'w', 'qwx'),
                      ('w', 'uwx', 'x', 'qwx'),
                      ('x', 'uwx', 'u', 'uvx'),
                      ('u', 'tuv', 'v', 'uvx'),
                      ('v', 'tvy', 'y', 'rvy'),
                      ('y', 'pry', 'p', 'pyz'),
                      ('p', 'pqr', 'q', 'opq'),
                      ('q', 'qwx', 'x', 'qrx'),
                      ('x', 'uvx', 'v', 'rvx'),
                      ('t', 'stz', 'z', 'tyz'),
                      ('z', 'osz', 'o', 'opz'),
                      ('o', 'osw', 'w', 'oqw'),
                      ('w', 'suw', 'u', 'uwx'),
                      ('u', 'stu', 't', 'tuv'),
                      )
        
        self.edges = self._distill()

class Cuboctahedron (Polyhedron):

    def __init__(self):
        # 8 vertices
        self.edge_color = "rgb <1, 1, 0>"
        self.edge_radius= 0.03
        self.vert_color = "rgb <1, 1, 0>"
        self.vert_radius= 0.03
        self.face_color = self.edge_color 

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
        self.nick = "CO"
        self.volume = sy.Integer(20)
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
#include "skies.inc"      // Ready defined sky spheres
// include "stars.inc"      // Some star fields
// include "strings.inc"    // macros for generating and manipulating text strings

// --- textures ---
// include "finish.inc"     // Some basic finishes
#include "glass.inc"      // Glass textures/interiors
// include "golds.inc"      // Gold textures
#include "metals.inc"     // Metallic pigments, finishes, and textures
#include "stones.inc"     // Binding include-file for STONES1 and STONES2
// include "stones1.inc"    // Great stone-textures created by Mike Miller
// include "stones2.inc"    // More, done by Dan Farmer and Paul Novak
// include "woodmaps.inc"   // Basic wooden colormaps
// include "woods.inc"      // Great wooden textures created by Dan Farmer and Paul Novak

global_settings {assumed_gamma 1.0}
global_settings {ambient_light rgb<1, 1, 1> }

// perspective (default) camera
camera {
  location  <2.5, 0.1, 0.2>
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

sky_sphere { S_Cloud2 scale 2 translate -1}

background { color rgb <1.0, 1.0, 1.0> }
"""

def test1():
    """
    minimalist, uses default Icosahedron and PD
    no fidling with attributes, no rescaling.
    """
    f = open("testing123.pov", "w")
    f.write(pov_header)
    ico = Icosahedron()
    pd = PD()
    draw_poly(ico, f)
    draw_poly(pd, f)
    f.close()
    
def test2():
    """
    same as test1 but adding a Rhombic Triacontahedron
    ico and pd are duals of each other, sized by default
    to criss-cross at mid-edges thereby forming verts
    of the correspondingly sized RT
    """    
    f = open("testing123.pov", "w")
    f.write(pov_header)
    ico = Icosahedron()
    pd = PD()
    rt = RT()
    draw_poly(ico, f)
    draw_poly(pd, f)
    draw_poly(rt, f)
    f.close()
    
def test3():
    """
    Remember you can edit these by turning shapes on and off.
    You have control over the filename if you wish to stop
    overwriting the same testing123 over and over
    """
    f = open("testing123.pov", "w")
    f.write(pov_header)
    # ico = Icosahedron()
    rt = RT()
    draw_poly(rt, f)
    # draw_poly(ico, f)
    f.close()
    
def test4():
    """
    Taking default Icosahedron to have R=1 edges (vs D=1),
    such scaling by sfactor gives IcosaWithin (IW), which,
    when further scaled up by PHI, becomes faces flush 
    with 2F SuperCube. 4 * Cube() because everything's 
    doubled when R=1 vs 0.5.
    """
    f = open("testing123.pov", "w")
    f.write(pov_header)
    octa = 2 * Octahedron()
    co = Cuboctahedron()
    ico = Icosahedron() * sfactor
    #rt = RT() * sfactor * PHI
    #cu = 4 * Cube()
    draw_poly(ico, f)
    draw_poly(octa, f)
    draw_poly(co, f)
    #draw_poly(cu, f)
    #draw_poly(rt, f)
    f.close()
    
def test5():
    """
    Same as above, but once RT is faces flush with 
    containing cube, enlarge is very slightly to 
    force its diamond faces to protrude and show 
    up clearly against the 2F cube faces background
    """
    f = open("marble_polys.pov", "w")
    f.write(pov_header)
    rt = RT() * sfactor * PHI * 1.01 # push out faces a bit more
    rt.face_color = "T_Stone18"
    cu = 4 * Cube()
    cu.face_color = "T_Stone17"
    draw_poly(rt, f, v=False, e=False, f=True, texture=True)
    draw_poly(cu, f, v=False, e=False, f=True, texture=True)
    f.close()

def test6():
    """
    Back to D=1. Shrink initial D edge Icosa by half then
    scale up by sfactor, known to be edges of the icosa
    inscribing in the corresponding Octa. Include the 
    2F Cube with faces-flush RT in addition to IW faces
    flush with Octa.
    """
    out = open("iw_rt_123.pov", "w")
    out.write(pov_header)
    # Icosa with edges sfactor = S/E
    icosaWithin = Icosahedron() * half * sfactor # D=1 (volume 60S + 20s3)
    octa = Octahedron()              # corresponding octa edges D
    rt = RT() * half * sfactor * PHI  # blow up corresponding RT by PHI
    cu_2F = Cube() * 2               # 2F Cube
    draw_poly(icosaWithin, out)
    draw_poly(octa, out)
    draw_poly(cu_2F, out)
    draw_poly(rt, out)
    out.close()

def test6a():
    """
    MM1
    """
    out = open("test_6a.pov", "w")
    out.write(pov_header)
    tet  = Tetrahedron()
    inv  = InvTetrahedron()
    cu   = Cube()
    octa = Octahedron()              # corresponding octa edges D
    rd   = RD()
    cu_2F = Cube() * 2               # 2F Cube
    draw_poly(tet, out)
    draw_poly(inv, out)
    draw_poly(cu, out)
    draw_poly(rd, out)
    draw_poly(octa, out)
    draw_poly(rd, out)
    draw_poly(cu_2F, out)
    out.close()

def test6b():
    """
    MM2
    """
    out = open("test_6b.pov", "w")
    out.write(pov_header)
    tet  = Tetrahedron()
    inv  = InvTetrahedron()
    cu   = Cube()
    octa = Octahedron()
    rd   = RD()
    cu_2F = Cube() * 2
    
    draw_poly(tet, out)
    draw_poly(inv, out)
    draw_poly(octa, out)
    draw_poly(rd, out)
    draw_poly(cu, out)
    draw_poly(cu_2F, out)
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    out.close()
    
def test7():
    out = open("ico_pd.pov", "w")
    out.write(pov_header)
    #ico = Icosahedron()*2
    #pd = PD()*2
    rt = RT()*2
    #draw_poly(ico, out)
    #draw_poly(pd, out)
    draw_poly(rt, out)
    out.close()
    
def test8():
    out = open("ball_rt.pov", "w")
    out.write(pov_header) 
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    rt = RT() * (1/PHI)  # SuperRT scaled down to wrap uniradius ball
    rt.edge_radius = 0.02
    rt.vert_radius = 0.04
    rt.vert_color = 'T_Copper_1A'
    rt.edge_color = 'T_Chrome_1A'
    draw_poly(rt, out, v=True, e=True, f=False, texture=True)
    out.close()
    
def test9():
    out = open("ball_rt_rd.pov", "w")
    out.write(pov_header) 
    draw_vert(ORIGIN, "T_Stone18", half, out, texture=True)
    rt = RT() * (1/PHI)  # SuperRT scaled down to wrap uniradius ball
    rt.edge_radius = 0.02
    rt.vert_radius = 0.04
    rt.vert_color = 'T_Copper_1A'
    rt.edge_color = 'T_Chrome_1A'
    
    rt_2 = RT() * (1/PHI) * 0.9994 * (3/2)**(1/3) # 7.5 RT_K
    rt_2.edge_radius = 0.02
    
    rd = RD()
    rd.edge_radius = 0.02
    rd.vert_radius = 0.04
    rd.vert_color = 'T_Copper_1A'
    rd.edge_color = 'T_Silver_1A'
    
    draw_poly(rd, out, v=True, e=True, f=False, texture=True)
    draw_poly(rt, out, v=True, e=True, f=False, texture=True)
    draw_poly(rt_2, out, v=False, e=True, f=False)
    out.close()

def test10():
    out = open("ball_in_rt_t.pov", "w")
    out.write(pov_header) 
    draw_vert(ORIGIN, "rgb <1, 0, 0>", half, out)
    rt = RT() * (1/(3*rt2(2)))**(1/3)  # RT_T
    rt.face_color = "T_Stone17"
    draw_poly(rt, out, v=False, e=False, f=True, texture=True)
    out.close()

if __name__ == "__main__":
    test10()
    
