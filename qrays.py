# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 09:07:22 2016

qrays.py is an implementation of Quadray Coordinates,
per Wikipedia.[1] I have a few versions across repos.
This copy is from:
    
https://github.com/4dsolutions/School_of_Tomorrow

My context for quadrays is in a philosophy of mathematics
investigation ala Wittgenstein, wherein an invented 
language game is used to probe the more accepted, 
status quo language games, such as XYZ i.e. "Cartesian
Coodinates". What do we mean by "basis vector" 
and "reflection" and even "dimension"? IVM coodinates
give us something to bounce off, for contrast.

Synergetics as initially published in two volumes
by Macmillan, provided a critique of the orthonormal
orthodoxy, whereby perpendicularity is the hallmark
"dimension seperator", but it proposed no alternative
lattice-based apparatus along the lines of XYZ. 

When I first learned of the "caltrop" approach, 
with four basis vectors forming a "beacon", with
coordinates (1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1)
I was drawn in to explore the ramifications. We 
were a small company of co-researchers.

Our method of normalization, such that every point
has only the one canonical representation, is part 
of the overall design. To normalize any (a,b,c,d),
find m=min(a,b,c,d) and rewrite as (a-m,b-m,c-m,d-m).
At least one of the four slots will now be 0.

Of core relevance is a way to map qrays to ordinary
xyz vectors, with two-way conversion. Design decisions,
aesthetically based, as well as practical considerations,
entered the process, along with a choice of computer 
language.

I think a simple 3ray xyz vector type in an object 
oriented language makes a great beginning. The 4ray 
ivm vector type defines the home base tetrahedron
of unit edges, defined by four close-packed IVM 
balls of unit radius, in juxtaposition with the
XYZ cube. The tetrahedron's edges D (D for 
diameter) are twice those of a ball with radius R.

In keeping with Fuller's emphasis on S3 -- 2nd root
of 9/8 -- as a volumetric conversion factor, my 
R-edged cube is designated the "unit volume" in 
XYZ, whereas the D-edged tetrahedron is the "unit
volume" of our alternative accounting system. The
conversion constant is S3, the unit-to-unit ratio.
In IVM tetravolumes, the XYZ cube of edges R has 
volume S3. That's unorthodox to say the least: a 
unit-edge cube with a not-unit volume. Our philo-
sophical investigation continues...

On the practical side, the left-handedness inherits 
from POV-Ray (povray.org),a ray-tracer and targeted 
application. Alternative juxtapositions of the D-edged 
IVM tetrahedron and the R-edge XYZ cube might be 
imagined, such as a right-handed version.

Per the slides [2], we introduce a human figure
with arms outstreched, and legs striding a line
perpendicular to the hand-to-hand one. The figure's
left hand is in the all-positive (+ + +) octant of 
the Cartesian system and has coordinates: 
    
>>> A
ivm_vector(a=1, b=0, c=0, d=0)

>>> A.xyz
xyz_vector(x=sqrt(2)/4, y=sqrt(2)/4, z=sqrt(2)/4)

>>> A.length() # DIAM = 1
sqrt(6)/4

The right hand is kitty corner through the Y axis,
still above the Z plane through the origin (our 
figure's solar plexus, home tetrahedron's body 
center, the origin for both XYZ (0,0,0) and IVM
(0,0,0,0).
     
>>> B
ivm_vector(a=0, b=1, c=0, d=0)

>>> B.xyz
xyz_vector(x=-sqrt(2)/4, y=-sqrt(2)/4, z=sqrt(2)/4)
 
The reference strider's front and back feet 
correspond to vectors C, D.

The inter-angle between any two basis vectors 
A, B, C, D is 109.47... whereas in XYZ with its 
"jack" arrangement, of three basis + three non-
basis spokes, dividing space into octants, the
relationships are either 90 or 180 degrees. 

>>> A.angle(B)
109.471220634491
    
>>> X.angle(-X)
180.000000000000

Sometimes Synergetics explorers are thinking in 
terms of unit radii, such that diameter lengthed
edges get a value of 2. A 2R-edged tetrahedron 
is shown as face diagonals of a 3-volumed cube,
with edges length 2nd root of 2. As discussed in
my Quadray slides (Google deck [1]), we envision
2nd and 3rd powering differently than usual: 
with trianglar and tetrahedral models respectively.

To accommodate this propensity to switch back
and forth between D=1 and D=2 (2R) -- D for 
diameter -- I added DIAM and RAD as module globals
starting at the end of 2024. All lenghts basically
halve or double, while volumes and areas stay the
same, as it's only the length unit that's affected.
Like going from inches to half-inches, yet a cup
of water is still a cup of water.

Adding these globals made length, area and volume
computations dependent on these variables, whereas
the earlier versions assumed a fixed D=1 regime.
 
This variable approach is not inconsistent with 
Synergetics itself, wherein its basic modules 
(A, B, E, S, T) come with plane nets, that include 
the variable 'a' as a scale factor along each edge.[3]

[1] https://en.wikipedia.org/wiki/Quadray_coordinates

[2] Quadrays (Google slides):
https://docs.google.com/presentation/d/1ynde13tnMAu7EelfVuQVTFDUWGYBcRDRmtkMu4LIUFw/edit?usp=sharing

[3] http://rwgrayprojects.com/synergetics/s09/figs/f1301.html


@author:  K. Urner, 4D Solutions, (M) MIT License
 Aug 06, 2025: fix typo in Qvector
 Jan 21, 2025: rewrite the docstring
 Dec 31, 2024: DIAM=1; RAD=1/2 and DIAM=2; RAD=1 need to both work equally well
 Dec 26, 2024: simplify Qvector <-> Vector conversion algs
 Sep 21, 2022: clean up, fix unittests
 Jun 20, 2022: add sympy dependency
 Oct  8, 2021: remove gmpy2 dependency
 Sep 19, 2021: remove autoconvert to floating point when initializing Vector
 Sep 19, 2021: make xyz Vector a property of Qvector vs. a method
 Sep 06, 2019: have type(self)() instead of Qvector() return outcomes
 May 25, 2019: add area methods based on cross product
 Jun 20, 2018: make Qvectors sortable, hashable
 Jun 11, 2016: refactored to make Qvector and Vector each standalone
 Aug 29, 2000: added extra-class, class dependent methods for
    dot and cross as alternative syntax
 July 8,2000: added method for rotation around any axis vector
 May 27,2000: shortend several methods thanks to Peter Schneider-Kamp
 May 24,2000: added unit method, tweaks
 May 8, 2000: slight tweaks re rounding values
 May 7, 2000: enhanced the Qvector subclass with native
    length, dot, cross methods -- keeps coords as a 4-tuple
    -- generalized Vector methods to accommodate 4-tuples
    if Qvector subclass, plus now returns vector of whatever
    type invokes method (i.e. Qvector + Qvector = Qvector)
 Mar 23, 2000:
 added spherical coordinate subclass
 added quadray coordinate subclass
 Mar  5, 2000: added angle function
 June 6, 2020: spherical coordinates debug, working on blender integration
"""

from sympy import cos, sin, acos, sqrt, atan
from mpmath import radians, degrees
import sympy as sp
from operator import add, mul, neg
from collections import namedtuple

import unittest

XYZ = namedtuple("xyz_vector", "x y z")
IVM = namedtuple("ivm_vector", "a b c d")

root2    = sqrt(2)

zero = sp.Integer(0)
half = sp.Rational(1, 2)
one  = sp.Integer(1)
two  = sp.Rational(2)

DIAM = one # comment out if DIAM = two
# DIAM = two
RAD  = DIAM / 2

class Vector:

    def __init__(self, arg):
        """Initialize a vector at an (x,y,z)"""
        self.xyz = XYZ(*arg)

    def __repr__(self):
        return repr(self.xyz)
    
    @property
    def x(self):
        return self.xyz.x

    @property
    def y(self):
        return self.xyz.y

    @property
    def z(self):
        return self.xyz.z
        
    def __mul__(self, scalar):
        """Return vector (self) * scalar."""
        newcoords = [scalar * dim for dim in self.xyz]
        return type(self)(newcoords)

    __rmul__ = __mul__ # allow scalar * vector

    def __truediv__(self,scalar):
        """Return vector (self) * 1/scalar"""        
        return self.__mul__(1.0/scalar)
    
    def __add__(self,v1):
        """Add a vector to this vector, return a vector""" 
        newcoords = map(add, v1.xyz, self.xyz)
        return type(self)(newcoords)
        
    def __sub__(self,v1):
        """Subtract vector from this vector, return a vector"""
        return self.__add__(-v1)
    
    def __neg__(self):      
        """Return a vector, the negative of this one."""
        return type(self)(tuple(map(neg, self.xyz)))

    def unit(self):
        return self.__mul__(one/self.length())

    def dot(self,v1):
        """
        Return scalar dot product of this with another vector.
        """
        return sum(map(mul , v1.xyz, self.xyz))

    def cross(self,v1):
        """
        Return the vector cross product of this with another vector
        """
        newcoords = (self.y * v1.z - self.z * v1.y, 
                     self.z * v1.x - self.x * v1.z,
                     self.x * v1.y - self.y * v1.x )
        return type(self)(newcoords)
    
    def area(self,v1):
        """
        xyz area of a parallelogram with these edge lengths
        """
        return self.cross(v1).length() * (1/RAD)
    
    def length(self):
        """Return this vector's length in R units or D units"""
        return DIAM * sqrt(self.dot(self))
    
    def angle(self,v1):
        """
        Return angle between self and v1, in decimal degrees
        """
        costheta = self.dot(v1)/(self.length()/DIAM * v1.length()/DIAM)
        theta = degrees(acos(costheta))
        return theta.evalf()

    def rotaxis(self,vAxis,deg):
        """
        Rotate around vAxis by deg
        realign rotation axis with Z-axis, rea lign self accordingly,
        rotate by deg (counterclockwise) around Z, resume original
        orientation (undo realignment)
        """
        
        r,phi,theta = vAxis.spherical()
        newv  = self.rotz(-theta).roty(phi)
        newv  = newv.rotz(-deg)
        newv  = newv.roty(-phi).rotz(theta)
        return type(self)(newv.xyz)        

    def rotx(self, deg):
        rad    = radians(deg)
        newy   = cos(rad) * self.y - sin(rad) * self.z
        newz   = sin(rad) * self.y + cos(rad) * self.z
        newxyz = [round(p ,8) for p in (self.x , newy, newz)]
        return type(self)(newxyz)
   
    def roty(self, deg):
        rad    = radians(deg)
        newx   = cos(rad) * self.x - sin(rad) * self.z
        newz   = sin(rad) * self.x + cos(rad) * self.z
        newxyz = [round(p ,8) for p in (newx, self.y, newz)]
        return type(self)(newxyz)

    def rotz(self, deg):
        rad    = radians(deg)
        newx   = cos(rad) * self.x - sin(rad) * self.y
        newy   = sin(rad) * self.x + cos(rad) * self.y
        newxyz = [round(p ,8) for p in (newx , newy, self.z)]
        return type(self)(newxyz)
    
    def spherical(self):
        """Return (r,phi,theta) spherical coords based 
        on current (x,y,z)"""
        r = self.length()
        
        if self.x == 0:
            if   self.y ==0: theta =   0.0
            elif self.y < 0: theta = -90.0
            else:            theta =  90.0
            
        else:  
            
            theta = degrees(atan(self.y/self.x))
            if   self.x < 0 and self.y == 0:   theta = 180
            # theta is positive so turn more than 180
            elif self.x < 0 and self.y <  0:   theta = 180 + theta
            # theta is negative so turn less than 180
            elif self.x < 0 and self.y >  0:   theta = 180 + theta

        if r == 0: 
            phi=0.0
        else: 
            phi = degrees(acos(self.z/r))
        
        return (r, phi, theta)


    def quadray(self):
        """
        Return self as a quadray Vector (Vector -> Qvector)
        A linear combo of self.xyz and the xyz basis spokes as Qvectors

        Negative coefficients will create oppositely pointing Qvectors
        """ 
        return (self.x * Qvector((root2, 0, 0, root2)) + 
                self.y * Qvector((root2, 0, root2, 0)) + 
                self.z * Qvector((root2, root2, 0, 0)))
        
class Qvector:
    """Quadray vector"""

    def __init__(self, arg):
        """Initialize a vector at an (a,b,c,d)"""
        self.coords = self.norm(arg)

    def __repr__(self):
        return repr(self.coords)

    def norm(self, arg):
        """Normalize such that 4-tuple all non-negative members."""
        minarg = min(arg)
        return IVM(arg[0] - minarg, 
                   arg[1] - minarg, 
                   arg[2] - minarg, 
                   arg[3] - minarg)
    
    def norm0(self):
        """Normalize such that sum of 4-tuple members = 0"""
        q  = self.coords
        av = (q[0] + q[1] + q[2] + q[3])/4
        return IVM(q[0]-av, q[1]-av, q[2]-av, q[3]-av)
    
    def unit_vector(self):
        return self/self.length()
    
    @property
    def a(self):
        return self.coords.a

    @property
    def b(self):
        return self.coords.b

    @property
    def c(self):
        return self.coords.c

    @property
    def d(self):
        return self.coords.d
    
    def __eq__(self, other):
        return self.coords == other.coords
        
    def __lt__(self, other):
        return self.coords < other.coords

    def __gt__(self, other):
        return self.coords > other.coords
    
    def __hash__(self):
        return hash(self.coords)
    
    def __mul__(self, scalar):
        """Return vector (self) * scalar."""
        newcoords = [scalar * dim for dim in self.coords]
        return type(self)(newcoords)

    __rmul__ = __mul__ # allow scalar * vector

    def __truediv__(self,scalar):
        """Return vector (self) * 1/scalar"""        
        return self.__mul__(1/scalar)
    
    def __add__(self,v1):
        """Add a vector to this vector, return a vector""" 
        newcoords = tuple(map(add, v1.coords, self.coords))
        return type(self)(newcoords)
        
    def __sub__(self,v1):
        """Subtract vector from this vector, return a vector"""
        return self.__add__(-v1)
    
    def __neg__(self):      
        """Return a vector, the negative of this one."""
        return type(self)(tuple(map(neg, self.coords)))
                  
    def length(self):
        """
        Uses norm0
        """
        t = self.norm0()
        return DIAM * sp.sqrt(half * (t[0]**2 + t[1]**2 + t[2]**2 + t[3]**2))

    def xyzlength(self):
        return self.xyz.length()
        
    def cross(self,v1):
        """Return the cross product of self with another vector.
        return a Qvector"""
        A = type(self)((1,0,0,0))
        B = type(self)((0,1,0,0))
        C = type(self)((0,0,1,0))
        D = type(self)((0,0,0,1))
        a1,b1,c1,d1 = v1.coords
        a2,b2,c2,d2 = self.coords
        k= root2/4
        the_sum =   (A*c1*d2 - A*d1*c2 - A*b1*d2 + A*b1*c2
               + A*b2*d1 - A*b2*c1 - B*c1*d2 + B*d1*c2 
               + b1*C*d2 - b1*D*c2 - b2*C*d1 + b2*D*c1 
               + a1*B*d2 - a1*B*c2 - a1*C*d2 + a1*D*c2
               + a1*b2*C - a1*b2*D - a2*B*d1 + a2*B*c1 
               + a2*C*d1 - a2*D*c1 - a2*b1*C + a2*b1*D)
        return k * the_sum
    
    def area(self, v1):
        """
        area in unit triangles of edges D
        """
        return self.cross(v1).length() * 1/(sqrt(3)*RAD)

    def angle(self, v1):
        return self.xyz.angle(v1.xyz)
        
    @property
    def xyz(self):
        """
        Return self as an xyz Vector (Qvector -> Vector)
        A linear combo of self.coords * the four basis qrays 
        as xyz equivalents

        Note: slightly asymmetrical with Vector where v.quadray() is
        a method not an attribute i.e. method disguised with @property
        """
        return (self.a * Vector(( root2/4,  root2/4,  root2/4)) + 
                self.b * Vector((-root2/4, -root2/4,  root2/4)) + 
                self.c * Vector((-root2/4,  root2/4, -root2/4)) + 
                self.d * Vector(( root2/4, -root2/4, -root2/4)))

        
class Svector(Vector):
    """Subclass of Vector that takes spherical coordinate args."""
    
    def __init__(self,arg):
        """
        initialize a vector at an (r,phi,theta) tuple (= arg)        
        """
        # if returning from Vector calc method, spherical is true
        # arg = Vector(arg).spherical()
        r     = arg[0]
        phi   = radians(arg[1])
        theta = radians(arg[2])
        self.xyz = XYZ(
                      r * cos(theta) * sin(phi),
                      r * sin(theta) * sin(phi),
                      r * cos(phi))

    def __repr__(self):
        return "Svector " + str(self.spherical())

def dot(a,b):
    return a.dot(b)

def cross(a,b):
    """
    cross product
    """
    return a.cross(b)

def angle(a,b):
    return a.angle(b)

def length(a):
    return a.length()


A = Qvector((one, zero, zero, zero))
B = Qvector((zero, one, zero, zero))
C = Qvector((zero, zero, one, zero))
D = Qvector((zero, zero, zero, one))

X = Vector((one, zero, zero))
Y = Vector((zero, one, zero))
Z = Vector((zero, zero, one))
    
class setcontext:
    
    def __init__(self, pv):
        self.pv = pv
    
    def __enter__(self):
        global DIAM, RAD
        self._old_diam = DIAM
        self._old_rad  = RAD
        DIAM = self.pv
        RAD = DIAM / 2
        
    def __exit__(self, *oops):
        global DIAM, RAD
        DIAM = self._old_diam
        RAD = self._old_rad
        

class Test_Qvector(unittest.TestCase):
    
    def test_unit_length(self):
        self.assertEqual((A-B).length(), DIAM, "PV not DIAM")

    def test_A_length(self):
        with setcontext(one):
            self.assertEqual(A.length(), sqrt(6)/4, "PV wrong length")

    def test_A_length_2(self):
        with setcontext(two):
            self.assertEqual(A.length(), sqrt(6)/2, "PV wrong length")

    def test_2R_length(self):
        with setcontext(two):
            self.assertEqual((A-B).length(), 2, "PV not 2")

    def test_PV_length(self):
        with setcontext(one):
            self.assertEqual((A-B).length(), 1, "PV not 1")
        
    def test_convert(self):
        self.assertEqual(A.xyz.quadray(), A, "not 2-way")
        
    def test_angle(self):
        with setcontext(one):        
            self.assertAlmostEqual(float(A.angle(B).evalf()), 109.471, places=3)

    def test_angle_2(self):
        with setcontext(two):        
            self.assertAlmostEqual(A.angle(B), 109.471, places=3)

    
if __name__ == "__main__":
    unittest.main()
