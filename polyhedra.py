"""
Kirby Urner
4D Solutions
First published: Apr 29 2007

Suitable for spatial geometry and/or synergetics students.

Update May 10:  I'd forgotten 8 of the 20 Icosahedron triangles!  Added.
Update May 13:  Added Octahedron, Mite, Coupler

"""
import sys
sys.path.append("/Users/mac/Documents/Python5")

import qrays
from math import sqrt

phi = (sqrt(5) + 1)/2.0

class Vector(qrays.Vector):
    
    radius = 0.02
    
    def __init__(self, xyz, color=(0,0,1)):
        super().__init__(xyz)
        self.color = color
        self.cyl = None

class Qvector(qrays.Qvector):
    
    radius = 0.02
    
    def __init__(self, xyz, color=(0,0,1)):
        super().__init__(xyz)
        self.color = color
        self.cyl = None
        
    @property
    def xyz(self):
        v = super().xyz()
        return v.xyz

class color:
    orange = "orange"
    green  = "green"
    red = "red"
    cyan = "cyan"
    
class Polyhedron:

    # defaults may be overridden
    showfaces      = True
    showedges      = True
    showvertices   = True
    # default POV-Ray textures
    face_texture   = 'T_Stone14'   # from stones.inc
    vertex_texture = 'T_Silver_1A' # from metals.inc
    edge_texture   = 'T_Copper_4A' # from metals.inc
    
    def scale(self, scalefactor):
        newverts = {}
        for v in self.vertices:
            newverts[v] = self.vertices[v] * scalefactor
        return self.__class__(newverts)

    __mul__ = __rmul__ = scale

    def translate(self, vector):
        newverts = {}
        for v in self.vertices:
            newverts[v] = self.vertices[v] + vector
        return self.__class__(newverts)

    __add__ = __radd__ = translate
    
    def _distill(self):

        edges = []
        unique = set()
        
        for f in self.faces:
            for pair in zip(f , f[1:] + (f[0],)):
                unique.add( tuple(sorted(pair)) )

        for edge in unique:
            edges.append( Edge(self.vertices[edge[0]],self.vertices[edge[1]]) )

        return edges            

    def draw(self):
        # VPython wireframe view, native to stickworks.py
        for e in self.edges:
            e.draw()
 
class Edge:

    """
    Edges are defined by two Vectors (above) and express as cylinder via draw().
    """

    radius = 0.02
    color = (1,0,0)

    def __init__(self, v0, v1, color=None):
        if not color==None:
            self.color = color
        self.v0 = v0
        self.v1 = v1
        self.cyl = None        
        
    def __repr__(self):
        return 'Edge from %s to %s' % (self.v0, self.v1)
          
    def draw(self):
        pass
    
class Amodule (Polyhedron) :
    pass

class Bmodule (Polyhedron) :
    pass

class Mite (Polyhedron) :

    def __init__(self,
                 name   = "Mite",
                 verts  = dict(j = Vector(( 0,  1, 0)),
                               o = Vector(( 0,  0, 0)),
                               r = Vector(( 1,  0, 1)),
                               s = Vector(( 1,  0,-1)))):
         
        self.name = name
        # 4 vertices
        self.vertices = verts

        # 4 faces
        self.faces = (('j','o','r'),('j','r','s'),('j','s','o'),('o','r','s'))

        self.edges = self._distill()
        
class Smite (Polyhedron) :
    pass

class Coupler (Polyhedron) :
    
    def __init__(self,
                 name = "Coupler",
                 verts  = dict(j = Vector(( 0,  1, 0)),
                               l = Vector(( 0, -1, 0)),
                               q = Vector((-1,  0, 1)),
                               r = Vector(( 1,  0, 1)),
                               s = Vector(( 1,  0,-1)),
                               t = Vector((-1,  0,-1)))):
        
        self.name = name
        # 6 vertices
        self.vertices = verts

        # 8 faces
        self.faces = (('j','q','r'),('j','r','s'),('j','s','t'),('j','t','q'),
                      ('l','q','r'),('l','r','s'),('l','s','t'),('l','t','q'))

        self.edges = self._distill()

class Qrays(Polyhedron):
    
    def __init__(self):
        self.name = "qrays"
        
        self.vertices = dict(a = Qvector((1,0,0,0)),
                             b = Qvector((0,1,0,0)),
                             c = Qvector((0,0,1,0)),
                             d = Qvector((0,0,0,1)),
                             o = Qvector((0,0,0,0)))
        
        self.faces = (('o','a'),('o','b'),('o','c'),('o','d'))
        
        self.edges = self._distill()

class InvQrays(Polyhedron):
    
    def __init__(self):
        self.name = "inv_qrays"
        
        self.vertices = dict(e = -Qvector((1,0,0,0)),
                             f = -Qvector((0,1,0,0)),
                             g = -Qvector((0,0,1,0)),
                             h = -Qvector((0,0,0,1)),
                             o = Qvector((0,0,0,0)))
        
        self.faces = (('o','e'),('o','f'),('o','g'),('o','h'))
        
        self.edges = self._distill()

class XYZ(Polyhedron):
    
    def __init__(self):
        self.name = "XYZ_coords"
        
        self.vertices = dict(x  = Vector((1,0,0)),
                             y  = Vector((0,1,0)),
                             z  = Vector((0,0,1)),
                             nx = Vector((-1,0,0)),
                             ny = Vector((0,-1,0)),
                             nz = Vector((0,0,-1)),
                             o  = Vector((0,0,0)))
        
        self.faces = (('o','x'),('o','y'),('o','z'),
                      ('o','nx'), ('o','ny'), ('o','nz'))
        
        self.edges = self._distill()
        
class Tetrahedron (Polyhedron) :

    def __init__(self,
                 name   = "Tetrahedron",
                 verts  = dict(a = Vector((-1, -1, 1)),
                               b = Vector((-1,  1, -1)),
                               c = Vector((1, 1, 1)),
                               d = Vector((1, -1, -1)))):
        """
        Imagine a cube centered at the origin and with
        a positive octant vertex at (1,1,1).  Inscribe
        a regular tetrahedron as six face diagonals therein.
        """
        self.name = name
        # 4 vertices
        self.vertices = verts

        # 4 faces
        self.faces = (('a','b','c'),('a','c','d'),
                      ('a','d','b'),('b','d','c'))

        self.edges = self._distill()

class Qtet(Polyhedron):
    
    def __init__(self):
        self.name = "Qtet"
        
        self.vertices = dict(a = Qvector((1,0,0,0)),
                             b = Qvector((0,1,0,0)),
                             c = Qvector((0,0,1,0)),
                             d = Qvector((0,0,0,1)))
        
        # 4 faces
        self.faces = (('a','b','c'),('a','c','d'),
                      ('a','d','b'),('b','d','c'))

        self.edges = self._distill()
 
class InvQtet(Polyhedron):
    
    def __init__(self):
        self.name = "InvQtet"
        
        self.vertices = dict(e = -Qvector((1,0,0,0)),
                             f = -Qvector((0,1,0,0)),
                             g = -Qvector((0,0,1,0)),
                             h = -Qvector((0,0,0,1)))
        
        # 4 faces
        self.faces = (('e','f','g'),('e','g','h'),
                      ('e','h','f'),('f','h','g'))

        self.edges = self._distill()
        
class Cube (Polyhedron):

    def __init__(self, 
                 name = "Cube",
                 verts = dict( a = Vector((-1, -1, 1)),
                                     b = Vector((-1,  1, -1)),
                                     c = Vector((1, 1, 1)),
                                     d = Vector((1, -1, -1)),
                                     e = Vector((1,  1, -1)),
                                     f = Vector((1, -1,  1)),
                                     g = Vector((-1, -1, -1)),
                                     h = Vector((-1, 1, 1)))):
        self.name = name
        # 8 vertices
        self.vertices = verts

        # 6 faces
        self.faces = (('a','f','c','h'),('h','c','e','b'),
                      ('b','e','d','g'),('g','d','f','a'),
                      ('c','f','d','e'),('a','h','b','g'))

        self.edges = self._distill()

class Octahedron (Polyhedron):

    def __init__(self): 

        verts = dict(i = Vector(( 0, 0, 1)),
                     j = Vector(( 0, 1, 0)),
                     k = Vector(( 0, 0,-1)),
                     l = Vector(( 0,-1, 0)),
                     m = Vector(( 1, 0, 0)),
                     n = Vector((-1, 0, 0)))

        self.name = "Octahedron"
        # 6 vertices
        self.vertices = verts
        
        # 8 faces
        self.faces = (('i','l','m'),('i','m','j'),('i','j','n'),('i','n','l'),                      
                      ('k','l','m'),('k','m','j'),('k','j','n'),('k','n','l'))
        
        self.edges = self._distill()
                                     
class Dodecahedron (Polyhedron):
    pass

class Icosahedron (Polyhedron):

    def __init__(self, 
            name = "Icosahedron",
            verts = dict(
            # 12 vertices at the corners of 3 mutually
            # orthogonal golden rectangles
            xya=Vector(( phi/2, 0.5, 0.0)), # phi rectangle in xy
            xyb=Vector(( phi/2,-0.5, 0.0)),
            xyc=Vector((-phi/2,-0.5, 0.0)),
            xyd=Vector((-phi/2, 0.5, 0.0)),
            #-----------------------------
            xza=Vector((-0.5, 0.0, phi/2)), # Phi rectangle in xz 
            xzb=Vector(( 0.5, 0.0, phi/2)),
            xzc=Vector(( 0.5, 0.0,-phi/2)),
            xzd=Vector((-0.5, 0.0,-phi/2)),
            #-----------------------------
            yza=Vector(( 0.0, phi/2, 0.5)), # Phi rectangle in yz 
            yzb=Vector(( 0.0, phi/2,-0.5)),
            yzc=Vector(( 0.0,-phi/2,-0.5)),
            yzd=Vector(( 0.0,-phi/2, 0.5)),
            )):

        self.name = name
        # 12 vertices
        self.vertices = verts

        # 20 equiangular triangles
        self.faces = (
            ('xza','xzb','yzd'),
            ('yzd','xzb','xyb'),
            ('xyb','xzb','xya'),
            ('xya','yza','xzb'),
            ('xzb','yza','xza'),

            ('xzd','xzc','yzb'),
            ('yzb','xzd','xyd'),
            ('xyd','xzd','xyc'),
            ('xyc','xzd','yzc'),
            ('yzc','xzd','xzc'),

            ('xyd','yzb','yza'),
            ('yza','yzb','xya'),
            ('xya','yzb','xzc'),
            ('xzc','xya','xyb'),
            ('xyb','xzc','yzc'),
            ('yzc','xyb','yzd'),
            ('yzd','yzc','xyc'),
            ('xyc','yzd','xza'),
            ('xza','xyc','xyd'),
            ('xyd','xza','yza')
            )
           

        self.edges = self._distill()
        
        self.rectangles = (
            ('xya','xyb','xyc','xyd'),
            ('xza','xzb','xzc','xzd'),
            ('yza','yzb','yzc','yzd'))    

    def goldrects(self):
        Edge.color = color.green
        for r in self.rectangles:
            c0,c1,c2,c3 = [self.vertices[i] for i in r]
            Edge(c0,c1).draw()
            Edge(c1,c2).draw()
            Edge(c2,c3).draw()
            Edge(c3,c0).draw()

class Cuboctahedron (Polyhedron):
    pass

def test():
    """
    The Concentric Hierarchy by R. Buckminster Fuller
    """
    Edge.color = color.orange
    tetra = Tetrahedron() * 0.5
    tetra.draw()
    
    Edge.color = color.green
    cube = Cube() * 0.5
    cube.draw()

    Edge.color = color.red
    cube = Octahedron()
    cube.draw()

    Edge.color = color.cyan
    ico = Icosahedron() * sqrt(2)
    ico.draw()

def test2():
    """
    Coupler in a Cube (canonical volumes 1 and 3 respectively)
    """

    Edge.color = color.orange
    tetra = Tetrahedron()
    tetra.draw()
    
    Edge.color = color.blue
    coupler = Mite()
    coupler.draw()

    #Edge.color = color.blue
    #coupler = Coupler()
    #coupler.draw()
    
    Edge.color = color.green
    cube = Cube()
    cube.draw()    

if __name__ == '__main__':
    test()
    # test2()
