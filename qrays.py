# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 09:07:22 2016

Vectors and Qvectors use the same metric i.e. the 
xyz vector and corresponding ivm vector always have 
the same length.

In contrast, the tetravolume.py modules in some cases 
assumes that volume and area use R-edge cubes and triangles
for XYZ units respectively, and D-edge tetrahedrons 
and triangles for IVM units of volume and area.  See
the docstring for more details.

@author:  K. Urner, 4D Solutions, (M) MIT License
 
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
import math
import sympy as sp
from operator import add, sub, mul, neg
from collections import namedtuple

XYZ = namedtuple("xyz_vector", "x y z")
IVM = namedtuple("ivm_vector", "a b c d")

root2   = sp.sqrt(2)

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
        return self.__mul__(1.0/self.length())

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
        return self.cross(v1).length()
    
    def length(self):
        """Return this vector's length"""
        return self.dot(self) ** 0.5

    def angle(self,v1):
        """
        Return angle between self and v1, in decimal degrees
        """
        costheta = self.dot(v1)/(self.length() * v1.length())
        theta = degrees(acos(costheta))
        return theta

    def rotaxis(self,vAxis,deg):
        """
        Rotate around vAxis by deg
        realign rotation axis with Z-axis, realign self accordingly,
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
        """return (a, b, c, d) quadray based on current (x, y, z)"""
        x, y, z = self.xyz
        k = root2
        x_ge_0 = 1 if x >=0 else 0
        y_ge_0 = 1 if y >=0 else 0
        z_ge_0 = 1 if z >=0 else 0
        x_lt_0 = 1 if x < 0 else 0
        y_lt_0 = 1 if y < 0 else 0
        z_lt_0 = 1 if z < 0 else 0

        a = k * (x_ge_0 *  x + y_ge_0 *  y + z_ge_0 *  z)
        b = k * (x_lt_0 * -x + y_lt_0 * -y + z_ge_0 *  z)
        c = k * (x_lt_0 * -x + y_ge_0 *  y + z_lt_0 * -z)
        d = k * (x_ge_0 *  x + y_lt_0 * -y + z_lt_0 * -z)
        return Qvector((a, b, c, d))

        
class Qvector:
    """Quadray vector"""

    def __init__(self, arg):
        """Initialize a vector at an (x,y,z)"""
        self.coords = self.norm(arg)

    def __repr__(self):
        return repr(self.coords)

    def norm(self, arg):
        """Normalize such that 4-tuple all non-negative members."""
        return IVM(*tuple(map(sub, arg, [min(arg)] * 4))) 
    
    def norm0(self):
        """Normalize such that sum of 4-tuple members = 0"""
        q = self.coords
        return IVM(*tuple(map(sub, q, [sum(q)/4.0] * 4))) 

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
        return self.__mul__(1.0/scalar)
    
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
                  
    def dot(self,v1):
        """Return the dot product of self with another vector.
        return a scalar
        
        >>> s1 = a.dot(b)/(a.length() * b.length())
        >>> degrees(acos(s1))
        109.47122063449069
        """
        return 0.5 * sum(map(mul, self.norm0(), v1.norm0()))

    def length(self):
        """Return this vector's length"""
        return self.dot(self) ** 0.5
        
    def cross(self,v1):
        """Return the cross product of self with another vector.
        return a Qvector"""
        A = type(self)((1,0,0,0))
        B = type(self)((0,1,0,0))
        C = type(self)((0,0,1,0))
        D = type(self)((0,0,0,1))
        a1,b1,c1,d1 = v1.coords
        a2,b2,c2,d2 = self.coords
        k= root2/4.0
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
        return self.cross(v1).length() * 2/(3**0.5)

    def angle(self, v1):
        return self.xyz.angle(v1.xyz)
        
    @property
    def xyz(self):
        a,b,c,d     =  self.coords
        k           =  0.5/root2
        xyz         = (k * (a - b - c + d),
                       k * (a - b + c - d),
                       k * (a + b - c - d))
        return Vector(xyz)
        
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

