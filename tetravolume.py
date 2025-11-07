"""
tetravolume.py
Kirby Urner (c) MIT License

Jan    1, 2024: Tetrahedron unit tests all passing, I need to revisit Triangle
Dec   31, 2024: DIAM=1; RAD=1/2 and DIAM=2; RAD=1 need to both work equally well
May    6, 2024: dihedral angles
April  1, 2024: wire up all three volume-from-edges algorithms as options 
April  1, 2024: add A, B subclasses of Tetrahedron, completing BEAST set

March 30, 2024: tighten the unittests to rely more on sympy
March 30, 2024: save edges and angles when initializing the Tetrahedron
March 30, 2024: make_tet now returns Tetrahedon (not volumes tuple)

The tetravolume.py methods make_tet and make_tri 
assume that volume and area use R-edge cubes and 
triangles for XYZ units respectively, and D-edge 
tetrahedrons and triangles for IVM units of volume 
and area (D = 2R).

The tetrahedron of edges DIAM has sqrt(8/9) the 
volume of a cube of edges RAD, yet each is unit in
its respective matrix.

The triangle of edges DIAM has an XYZ area of sqrt(3)
i.e. an equilateral triangle of edges 2 in R-square
units.  The IVM area of the same triangle is simply 1.

The cube of edges sqrt(2) in RAD units, has volume 
sqrt(2) to the 3rd power.  One third of that volume
is our unit tetrahedron of edges D (cube face diagonals).

See:
https://coda.io/d/Math4Wisdom_d0SvdI3KSto/ivm-xyz_suqdu#_luR7B
for explanation of quadrays, used for some unit tests

https://flic.kr/p/2pGmvWD (labeling system)

https://github.com/4dsolutions/School_of_Tomorrow/blob/master/VolumeTalk.ipynb
for background on adapting volume formulas and/or using GdJ's

https://github.com/4dsolutions/School_of_Tomorrow/blob/master/Qvolume.ipynb
for background on computing a tet volume from 4 quadrays

A goal for this version of tetravolume.py + qrays.py
is to keep computations symbolic, with precision 
open-ended. A work in progress.  Mar 5, 2024.

Another goal as of March-April 2024 is to flesh out
the Tetrahedron instance with more specific info as
to which segments are what length.

Apex A goes to base B, C, D, creating edges:
    a: AB
    b: AC
    c: AD
    d: BC
    e: CD
    f: BD
(alphabetized pairs)
    
And faces: 
    ABC ACD ADB BCD (in terms of verts)
or (in terms of lengths): 
    (a, d, b), (b, e, c), (c, f, a), (d, e, f)
    [ tuples any order, elements may cycle ]
    
Therefore we have three angles from each vertex:
A: BAC CAD BAD
B: ABC CBD ABD
C: ACB ACD BCD
D: ADC BDC ADB
(middle letter is vertex angle, left and right letters alphabetized)

When we get the six lengths as inputs, lets 
assign them to edge names and compute the 
twelve angles.

Example resource:
https://www.omnicalculator.com/math/triangle-angle
"""

from sympy import Rational, Integer, Matrix, acos, cos, sin, deg, N, Eq
from sympy import sqrt as rt2
from qrays import Qvector, Vector, RAD, DIAM, one, two
import sys

# ============[ GLOBAL CONSTANTS ]=================== 

R = Rational(1,2)
D = Integer(1)

Syn3   = rt2(Rational(9, 8))
root2  = rt2(2)
root3  = rt2(3)
root5  = rt2(5)
root6  = rt2(6)
root10 = rt2(10)

PHI = (1 + root5)/2

Svol = (PHI **-5)/2  
Evol = (root2/8) * (PHI ** -3)
Avol = Bvol = Tvol = Rational(1,24)

sfactor = Svol/Evol  # = (2*root2 / PHI**2) = (3*root2 - root10)

# ============[ TETRAHEDRON CLASS ]=================== 

class Tetrahedron:
    """
    Takes six edges of tetrahedron with faces
    (a,b,d)(b,c,e)(c,a,f)(d,e,f) -- returns volume
    in ivm tvs and xyz cubic units, Syn3 ratio.
    
        Apex A goes to base B, C, D, creating edges:
            a: AB
            b: AC
            c: AD
            d: BC
            e: CD
            f: DB  
            
    https://flic.kr/p/2pGmvWD (labeling system)
    """

    def __init__(self, a, b, c, d, e, f):
        self.a, self.a2 = a, a**2
        self.b, self.b2 = b, b**2
        self.c, self.c2 = c, c**2
        self.d, self.d2 = d, d**2
        self.e, self.e2 = e, e**2
        self.f, self.f2 = f, f**2
   
        # 2-letter edge labels
        self.AB = a
        self.AC = b
        self.AD = c
        self.BC = d
        self.CD = e
        self.BD = f
        
        # 3-letter face angles
        a2,b2,c2,d2,e2,f2 = self.a2, self.b2, self.c2, self.d2, self.e2, self.f2

        self.BAC = acos( (a2 + b2 - d2)/(2 * a * b) )
        self.CAD = acos( (b2 + c2 - e2)/(2 * b * c) )
        self.BAD = acos( (a2 + c2 - f2)/(2 * a * c) )
        
        self.ABC = acos( (a2 + d2 - b2)/(2 * a * d) )
        self.CBD = acos( (d2 + f2 - e2)/(2 * d * f) )
        self.ABD = acos( (a2 + f2 - c2)/(2 * a * f) )
        
        self.ACB = acos( (b2 + d2 - a2)/(2 * b * d) )
        self.ACD = acos( (b2 + e2 - c2)/(2 * b * e) ) 
        self.BCD = acos( (d2 + e2 - f2)/(2 * d * e) )
        
        self.ADC = acos( (c2 + e2 - b2)/(2 * c * e) ) 
        self.BDC = acos( (e2 + f2 - d2)/(2 * e * f) ) 
        self.ADB = acos( (c2 + f2 - a2)/(2 * c * f) )
        
    def dihedral(self, edge):
        if   edge == 'AB': 
            r = (cos(self.CBD) - cos(self.ABD) * cos(self.ABC))/(sin(self.ABD) * sin(self.ABC))
        elif edge == 'AC': 
            r = (cos(self.BCD) - cos(self.ACD) * cos(self.ACB))/(sin(self.ACD) * sin(self.ACB))
        elif edge == 'AD': 
            r = (cos(self.BDC) - cos(self.ADB) * cos(self.ADC))/(sin(self.ADB) * sin(self.ADC))
        elif edge == 'BC': 
            r = (cos(self.ACD) - cos(self.BCD) * cos(self.ACB))/(sin(self.BCD) * sin(self.ACB))
        elif edge == 'CD': 
            r = (cos(self.ADB) - cos(self.ADC) * cos(self.BDC))/(sin(self.ADC) * sin(self.BDC))
        elif edge == 'BD': 
            r = (cos(self.ADC) - cos(self.BDC) * cos(self.ADB))/(sin(self.BDC) * sin(self.ADB))
        return acos(r)
    
    def dihedrals(self, values=False, degrees=False, prec=15):
        """
            a: AB
            b: AC
            c: AD
            d: BC
            e: CD
            f: BD 
        """
        if values:
            the_dict = {
                "AB": N(self.dihedral('AB'), prec),
                "AC": N(self.dihedral('AC'), prec),
                "AD": N(self.dihedral('AD'), prec),
                "BC": N(self.dihedral('BC'), prec),
                "CD": N(self.dihedral('CD'), prec),
                "BD": N(self.dihedral('BD'), prec),
                }
        else:
            the_dict = {
                "AB": self.dihedral('AB'),
                "AC": self.dihedral('AC'),
                "AD": self.dihedral('AD'),
                "BC": self.dihedral('BC'),
                "CD": self.dihedral('CD'),
                "BD": self.dihedral('BD'),
                }    
        
        if degrees:
        
            output = {}  # empty dict
            
            if values:
                for k,v in the_dict.items():
                    output[k] = N(deg(v), prec) 
            else:
                for k,v in the_dict.items():
                    output[k] = deg(v)
        
        else:
            
            output = the_dict  # radians or expressions
                
        return output
        
    def dump(self):
        return self.a2, self.b2, self.c2
    
    def __mul__(self, other):
        a = self.a * other
        b = self.b * other
        c = self.c * other
        d = self.d * other
        e = self.e * other
        f = self.f * other
        return Tetrahedron(a,b,c,d,e,f)
        
    __rmul__ = __mul__
        
    def edges(self, values=False, prec=15):
        """
            a: AB
            b: AC
            c: AD
            d: BC
            e: CD
            f: BD 
        """
        if values:
            return {
                "AB": N(self.a, prec),
                "AC": N(self.b, prec),
                "AD": N(self.c, prec),
                "BC": N(self.d, prec),
                "CD": N(self.e, prec),
                "BD": N(self.f, prec),
                }
        else:
            return {
                "AB": self.a,
                "AC": self.b,
                "AD": self.c,
                "BC": self.d,
                "CD": self.e,
                "BD": self.f,
                }            
        
    def angles(self, values=False, prec=15):
        """
        Three angles from each vertex:
        A: BAC CAD BAD
        B: ABC CBD ABD
        C: ACB ACD BCD
        D: ADC BDC ADB
        (middle letter is vertex angle, left and right letters alphabetized)
        """
        if values:
            return {
                "BAC": N(self.BAC, prec),
                "CAD": N(self.CAD, prec),
                "BAD": N(self.BAD, prec),
                "ABC": N(self.ABC, prec),
                "CBD": N(self.CBD, prec),
                "ABD": N(self.ABD, prec),
                "ACB": N(self.ACB, prec),
                "ACD": N(self.ACD, prec),
                "BCD": N(self.BCD, prec),
                "ADC": N(self.ADC, prec),
                "BDC": N(self.BDC, prec),
                "ADB": N(self.ADB, prec),
                }            
        else:
            return {
                "BAC": self.BAC,
                "CAD": self.CAD,
                "BAD": self.BAD,
                "ABC": self.ABC,
                "CBD": self.CBD,
                "ABD": self.ABD,
                "ACB": self.ACB,
                "ACD": self.ACD,
                "BCD": self.BCD,
                "ADC": self.ADC,
                "BDC": self.BDC,
                "ADB": self.ADB
                }

    def degrees(self, values=False, prec=15):
        output = {}
        if values:
            for k,v in self.angles().items():
                output[k] = N(deg(v), prec) 
        else:
            for k,v in self.angles().items():
                output[k] = deg(v)
        return output
            
    def ivm_volume(self, value=False, prec=50):
        """
        Three options to compute volume from edges...
        GdJ: Gerald de Jong, similar to Euler's, lost his notes, works
        PdF: Piero della Francesca, modified by Syn3 (XYZ->IVM constant)
        CM : Caley-Menger, modified by Syn3 (XYZ->IVM constant) 
        """
        
        ivmvol = GdJ(self.a, self.b, self.c, self.d, self.e, self.f)
        # ivmvol = PdF(self.a, self.b, self.c, self.d, self.e, self.f)
        # ivmvol = CM(self.a, self.b, self.c, self.d, self.e, self.f)
        
        return ivmvol if not value else N(ivmvol, prec)

    def xyz_volume(self, value=False, prec=50):
        xyzvol = (1/Syn3) * self.ivm_volume()
        return xyzvol if not value else N(xyzvol, prec)

# ============[ VOLUME FORMULAE ]=================== 

def GdJ(a, b, c, d, e, f):
    "Gerald de Jong"
    A,B,C,D,E,F = [x**2 for x in (a, b, c, d, e, f)] # 2nd power us

    _open   = sum((A * B * E, A * B * F, A * C * D,  
                   A * C * E, A * D * E, A * E * F,
                   B * C * D, B * C * F, B * D * F, 
                   B * E * F, C * D * E, C * D * F))
    
    _closed = sum((A * B * D, 
                   A * C * F, 
                   B * C * E, 
                   D * E * F))

    _oppo   = sum((A * E * (A + E),
                   B * F * (B + F),
                   C * D * (C + D)))
    
    return rt2((_open - _closed - _oppo)/2) * (1/DIAM**3) # D = 1D or 2R

def PdF(a,b,c,d,e,f):
    """
    Piero della Francesca
    https://www.mathpages.com/home/kmath424/kmath424.htm
    """
    
    def adapter(a, e, c, d, f, b):
        "unscramble input's to match GdJ order"
        return a, b, c, d, e, f

    A,B,C,D,E,F = [x**2 for x in 
                   adapter(2*a,2*b,2*c,2*d,2*e,2*f)] 
    
    comp_chunk =  ((A * F) * (-A + B + C + D + E - F)
                 + (B * E) * ( A - B + C + D - E + F)
                 + (C * D) * ( A + B - C - D + E + F)
                 - (A + F) * (B + E) * (C + D)/2
                 - (A - F) * (B - E) * (C - D)/2 )
    
    return (rt2(2 * comp_chunk) / 16) * (1/DIAM**3) # D = 1D or 2R; Syn3 is blended in here

def CM(a, b, c, d, e, f):
    """
    Caley-Menger
    https://en.wikipedia.org/wiki/Cayley%E2%80%93Menger_determinant
    """
    A,B,C,D,E,F = [(2*x)**2 for x in (a,b,c,d,e,f)]
    
    # Construct a 5x5 matrix per Caley-Menger
    M = Matrix(
        [[0, 1, 1, 1, 1],
         [1, 0, A, B, C],
         [1, A, 0, D, F],
         [1, B, D, 0, E],
         [1, C, F, E, 0]])
    return (rt2(M.det())/16) * (1/DIAM**3) # D = 1D or 2R 

def make_tet(v0,v1,v2):
    """
    three edges from any corner, remaining three edges computed
    """
    return Tetrahedron(v0.length(), v1.length(), v2.length(), 
                      (v0-v1).length(), (v1-v2).length(), (v2-v0).length())

def qvolume(q0, q1, q2, q3):
    """
    Construct a 5x5 matrix per Tom Ace
    """
    M = Matrix([
        q0.coords + (1,),
        q1.coords + (1,),
        q2.coords + (1,),
        q3.coords + (1,),
        [1,1,1,1,0]])
    return (abs(M.det())/4) # that's it!

# ============[ BEAST Modules ]=================== 
        
class A(Tetrahedron):
    """
    Developed using Qvectors
    """
    
    def __init__(self):
        
        one = Integer(1)
        two = Integer(2)
        three = Integer(3)
        a = Qvector((one,0,0,0))
        b = Qvector((0,one,0,0))
        c = Qvector((0,0,one,0))
        d = Qvector((0,0,0,one))
        
        # vertexes
        # amod_E  = Qvector((0,0,0,0))  # origin = center of home base tetrahedron
        amod_C  = b                     # to vertex (C), choose Qvector b
        amod_D  = (b + c)/two           # to mid-edge D of CC on tetra base 
        amod_F  = (b + c + d)/three     # to face-center of base F
        
        # apex E to base F, C, D
        amod_EF = amod_F
        amod_CE = b
        amod_DE = amod_D
        
        # around the base, C, D, E
        amod_CF = amod_C - amod_F
        amod_CD = amod_C - amod_D
        amod_DF = amod_D - amod_F
        
        a,b,c,d,e,f = [v.length() for v in (amod_EF, amod_CE, amod_DE, 
                                            amod_CF, amod_CD, amod_DF)]
        
        super().__init__(a,b,c,d,e,f) 
        
    def fig986_421(self, value = False, prec = 15):
        """
        http://rwgrayprojects.com/synergetics/s09/figs/f86421.html
        """
        a = DIAM
        figdata = {
            "BF" : a * root3/3,
            "BE" : a * root6/4,
            "BG" : a/2,
            "EF" : a * root6/12,
            "EG" : a * root2/4,
            "FG" : a * root3/6,}
        if value:
            return { edge: N(expr, prec) for (edge, expr) in figdata.items() }
        else:
            return figdata

    def fig913_01(self, value = False, prec = 15):
        """
        http://rwgrayprojects.com/synergetics/s09/figs/f1301.html
        """
        a = DIAM
        figdata = {
            "CE" : a * root6/4,
            "CF" : a * root3/3,
            "CD" : a/2,
            "EF" : a * root6/12,
            "DF" : a * root3/6,
            "DE" : a * root2/4,}
        if value:
            return { edge: N(expr, prec) for (edge, expr) in figdata.items() }
        else:
            return figdata

class B(Tetrahedron):
    """
    Developed from Fig 916.01
    http://rwgrayprojects.com/synergetics/s09/figs/f1601.html
    """
    
    def __init__(self):
        a = DIAM
        BA = a * root2/2
        BE = a * root6/4
        BG = a/2
        AE = a * root6/12
        EG = a * root2/4
        AG = a/2
        super().__init__(BA, BE, BG, AE, EG, AG)
        
    def fig986_421(self, value = False, prec = 15):
        """
        http://rwgrayprojects.com/synergetics/s09/figs/f86421.html
        """
        a = DIAM
        figdata = {
            "BA" : a * root2/2,
            "BE" : a * root6/4,
            "BG" : a/2,
            "AE" : a * root6/12,
            "EG" : a * root2/4,
            "AG" : a/2,}
        if value:
            return { edge: N(expr, prec) for (edge, expr) in figdata.items() }
        else:
            return figdata
        
    def fig916_01(self, value = False, prec = 15):
        """
        http://rwgrayprojects.com/synergetics/s09/figs/f1601.html
        """
        a = DIAM
        figdata = {
            "AB" : a * root6/4,
            "AC" : a/2,
            "AE" : a * root2/2,
            "BC" : a * root2/4,
            "CE" : a/2,
            "BE" : a * root6/12}
        if value:
            return { edge: N(expr, prec) for (edge, expr) in figdata.items() }
        else:
            return figdata

class S(Tetrahedron):
    
    def __init__(self):
        a  = DIAM
        e0 = 1/PHI
        e1 = sfactor/2
        e2 = root3 * e1/2
        e3 = (3 - root5)/2
        e4 = e1/2
        e5 = e4
        super().__init__(a*e0, a*e1, a*e2, a*e3, a*e4, a*e5)  

    def fig988_13(self, value = False, prec = 15):
        a = DIAM
        figdata = {
            "GH" : (a/2) * rt2(7 - 3*root5),
            "EG" : (a/2) * rt2(7 - 3*root5),
            "EH" : (a/2) * (3 - root5),
            "FG" : (a/2) * root3 * rt2(7 - 3*root5),
            "FE" : a * rt2(7 - 3*root5),
            "FH" : (a/2) * (root5 - 1),}
        if value:
            return { edge: N(expr, prec) for (edge, expr) in figdata.items() }
        else:
            return figdata
        
class T(Tetrahedron):
    
    def __init__(self):
        E2T = (Rational(1,24) / E().ivm_volume()).simplify()
        h = E2T ** Rational(1,3)
        a  = DIAM/2
        e0 = a
        e1 = a * root3 * PHI**-1
        e2 = a * rt2((5 - root5)/2)
        e3 = a * (3 - root5)/2
        e4 = a * rt2(5 - 2*root5)
        e5 = a * 1/PHI
        
        e0 *= h
        e1 *= h
        e2 *= h
        e3 *= h
        e4 *= h
        e5 *= h
 
        super().__init__(e0, e1, e2, e3, e4, e5)        

    def fig986_411(self, value = False, prec = 15):
        E2T = (Rational(1,24) / E().ivm_volume()).simplify()
        h = RAD * (E2T ** Rational(1,3))       
        figdata = {
            "CA" : (h/2) * (3 - root5),
            "CB" : (h/2) * (root5 - 1),
            "CO" : h,
            "AB" : h * rt2(5 - 2 * root5),
            "AO" : h * rt2((5 - root5)/2),
            "BO" : h * rt2((9 - 3 * root5)/2),}
        if value:
            return { edge: N(expr, prec) for (edge, expr) in figdata.items() }
        else:
            return figdata
        
class E(Tetrahedron):
    
    def __init__(self):
        a  = DIAM/2
        e0 = a
        e1 = a * root3 * PHI**-1
        e2 = a * rt2((5 - root5)/2)
        e3 = a * (3 - root5)/2
        e4 = a * rt2(5 - 2*root5)
        e5 = a * 1/PHI        
        super().__init__(e0, e1, e2, e3, e4, e5)
        
    def fig986_411(self, value = False, prec = 15):
        h = Rational(1,2) 
        figdata = {
            "CA" : (h/2) * (3 - root5),
            "CB" : (h/2) * (root5 - 1),
            "CO" : h,
            "AB" : h * rt2(5 - 2 * root5),
            "AO" : h * rt2((5 - root5)/2),
            "BO" : h * rt2((9 - 3 * root5)/2),}
        if value:
            return { edge: N(expr, prec) for (edge, expr) in figdata.items() }
        else:
            return figdata

class K(Tetrahedron):
    
    def __init__(self):
        E2K = (Rational(1,16) / E().ivm_volume()).simplify()
        h = E2K ** Rational(1,3)
        a  = DIAM/2
        e0 = a
        e1 = a * root3 * PHI**-1
        e2 = a * rt2((5 - root5)/2)
        e3 = a * (3 - root5)/2
        e4 = a * rt2(5 - 2*root5)
        e5 = a * 1/PHI
        
        e0 *= h
        e1 *= h
        e2 *= h
        e3 *= h
        e4 *= h
        e5 *= h
 
        super().__init__(e0, e1, e2, e3, e4, e5)        

    def fig986_411(self, value = False, prec = 15):
        E2T = (Rational(1,24) / E().ivm_volume()).simplify()
        h = RAD * (E2T ** Rational(1,3))       
        figdata = {
            "CA" : (h/2) * (3 - root5),
            "CB" : (h/2) * (root5 - 1),
            "CO" : h,
            "AB" : h * rt2(5 - 2 * root5),
            "AO" : h * rt2((5 - root5)/2),
            "BO" : h * rt2((9 - 3 * root5)/2),}
        if value:
            return { edge: N(expr, prec) for (edge, expr) in figdata.items() }
        else:
            return figdata
        
# ============[ TRIANGLE CLASS ]===================

class Triangle:
    
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c  

    def ivm_area(self):
        ivmarea = self.xyz_area() * 1/rt2(3)
        return ivmarea

    def xyz_area(self):
        """
        Heron's Formula, without the 1/4
        """
        a,b,c = self.a, self.b, self.c
        xyzarea = rt2((a+b+c) * (-a+b+c) * (a-b+c) * (a+b-c))
        return xyzarea * (1/DIAM ** 2)
    
def make_tri(v0,v1):
    """
    input two edge vectors from a common corner, 3rd computed
    """
    tri = Triangle(v0.length(), v1.length(), (v1-v0).length())
    return tri

# ============[ TESTS ]===================        
import unittest

class Test_Tetrahedron(unittest.TestCase):
    
    def test_unit_volume(self):
        tet = Tetrahedron(DIAM, DIAM, DIAM, DIAM, DIAM, DIAM)
        self.assertEqual(tet.ivm_volume(), Integer(1), "Volume not 1")

    def test_B_module(self):
        tet = B()
        self.assertEqual(tet.ivm_volume(), Rational(1,24), "Volume not 1/24")

    def test_E_module(self):
        tet = E()
        self.assertTrue(Eq(tet.ivm_volume(), 
                           (root2/8) * (PHI ** -3)))
                        
    def test_A_module(self):
        tet = A()
        self.assertEqual(tet.ivm_volume(), Rational(1,24), "Volume not 1/24")

    def test_S_module(self):
        tet = S()
        self.assertTrue(Eq(tet.ivm_volume(), 
                               (PHI ** -5)/2))

    def test_T_module(self):
        tet = T()
        self.assertTrue(Eq(tet.ivm_volume(), Rational(1,24)), "Volume not 1/24")
                
    def test_unit_volume2(self):
        tet = Tetrahedron(RAD, RAD, RAD, RAD, RAD, RAD)
        self.assertEqual(tet.xyz_volume(), root2/12)

    def test_unit_volume3(self):
        tet = Tetrahedron(RAD, RAD, RAD, RAD, RAD, RAD)
        self.assertEqual(tet.ivm_volume(), Rational(1,8))
        
    def test_phi_edge_tetra(self):
        tet = Tetrahedron(DIAM, DIAM, DIAM, DIAM, DIAM, DIAM*PHI)
        self.assertTrue(Eq(tet.ivm_volume(), root2/2))

    def test_right_tetra(self):
        alt = rt2(DIAM**2 - (DIAM/2)**2) # altitude of tetrabook page
        e   = rt2(alt**2 + alt**2)       # right tetrahedron hypotenuse
        tet = Tetrahedron(DIAM, DIAM, DIAM, DIAM, DIAM, e)
        self.assertEqual(tet.xyz_volume(), Integer(1))

    def test_quadrant(self):
        one = Integer(1)
        qA = Qvector((one,0,0,0))
        qB = Qvector((0,one,0,0))
        qC = Qvector((0,0,one,0))
        tet = make_tet(qA, qB, qC) 
        self.assertEqual(tet.ivm_volume(), Rational(1,4)) 

    def test_octant(self):
        qA = Qvector((one,0,0,0))
        qB = Qvector((0,one,0,0))
        qC = Qvector((0,0,one,0))
        qD = Qvector((0,0,0,one))
        qE = Qvector((0, one, one, one))
        x = (qE - qB) * (1/rt2(two))
        y = (qE - qC) * (1/rt2(two))
        z = (qE - qD) * (1/rt2(two))
        tet = make_tet(x,y,z)
        self.assertEqual(tet.xyz_volume(), Rational(1,6))

    def test_eighth_octahedron(self):
        qA = Qvector((one,0,0,0))
        qB = Qvector((0,one,0,0))
        qC = Qvector((0,0,one,0))
        qD = Qvector((0,0,0,one))
        qE = Qvector((0, one, one, one))
        a = (qE - qB)
        b = (qE - qC) 
        c = (qE - qD) 
        tet = make_tet(a, b, c)
        self.assertEqual(tet.ivm_volume(), Rational(1, 2)) 

    def test_xyz_cube(self):
        qA = Qvector((one,0,0,0))
        qB = Qvector((0,one,0,0))
        qC = Qvector((0,0,one,0))
        qD = Qvector((0,0,0,one))
        qE = Qvector((0, one, one, one))
        x = (qE - qB) * (1/rt2(two))
        y = (qE - qC) * (1/rt2(two))
        z = (qE - qD) * (1/rt2(two)) 
        R_octa = make_tet(x,y,z)
        self.assertEqual(6 * R_octa.xyz_volume(), Integer(1)) 

    def test_s3(self):
        """
        XYZ volume of D-edge Tet * Syn3 == XYZ volume of R-edge Cube == 1
        """
        D_tet = Tetrahedron(DIAM, DIAM, DIAM, DIAM, DIAM, DIAM)
        qA = Qvector((one,0,0,0))
        qB = Qvector((0,one,0,0))
        qC = Qvector((0,0,one,0))
        qD = Qvector((0,0,0,one))
        qE = Qvector((0, one, one, one))
        a = (qE - qB) * (1/rt2(two))
        b = (qE - qC) * (1/rt2(two))
        c = (qE - qD) * (1/rt2(two))
        R_cube = 6 * make_tet(a,b,c).xyz_volume()
        self.assertEqual(D_tet.xyz_volume() * Syn3, R_cube)

    def test_martian(self):
        two = Integer(2)
        one = Integer(1)
        p = Qvector((two,one,0,one))
        q = Qvector((two,one,one,0))
        r = Qvector((two,0,one,one))
        result = make_tet(5*q, 2*p, 2*r)
        self.assertEqual(result.ivm_volume(), Integer(20))
   
    def test_phi_tet(self):
        "edges from common vertex: phi, 1/phi, 1"
        two = Integer(2)
        one = Integer(1)
        p = Qvector((two,one,0,one))
        q = Qvector((two,one,one,0))
        r = Qvector((two,0,one,one))
        result = make_tet(p * PHI, q * (1/PHI), r)
        self.assertEqual(result.ivm_volume().evalf(), one)
        
    def test_koski(self):
        a = DIAM
        b = a * PHI ** -1
        c = a * PHI ** -2
        d = a * (root2) * PHI ** -1 
        e = a * (root2) * PHI ** -2
        f = a * (root2) * PHI ** -1       
        tet = Tetrahedron(a,b,c,d,e,f)
        self.assertTrue(Eq(tet.ivm_volume(), PHI ** -3))   

    def test_qvolume(self):        
        one = Integer(1)
        two = Integer(2)
        three = Integer(3)
        # a = Qvector((one,0,0,0))
        b = Qvector((0,one,0,0))
        c = Qvector((0,0,one,0))
        d = Qvector((0,0,0,one))
        
        # vertexes of the A module as Qvectors
        amod_E  = Qvector((0,0,0,0))    # origin = center of home base tetrahedron
        amod_C  = b                     # to vertex (C), choose Qvector b
        amod_D  = (b + c)/two           # to mid-edge D of CC on tetra base 
        amod_F  = (b + c + d)/three     # to face-center of base F
        self.assertEqual(qvolume(amod_E, amod_C, amod_D, amod_F), Rational(1,24))

class Test_Koski(unittest.TestCase):
        
    def test_Tetrahedron(self):
        "Tetrahedron =   S6  +    S3 # (volume = 1)"
        S6 = S() * PHI**2
        S3 = S() * PHI
        self.assertTrue(Eq(S6.ivm_volume() + S3.ivm_volume(), Integer(1)))
    
    def test_Icosahedron(self):
        "Icosahedron =100*E3 + 20*E  # (volume = ~18.51)"
        E3 = E() * PHI
        E0 = E()
        self.assertEqual(N(100*(E3.ivm_volume()) + 20*(E0.ivm_volume())), 
                         N(20 * 1/sfactor) )       

    def test_RT5(self):
        "RhTriac_T   =  5*S6 +  5*S3 # (volume = 5)"
        S6 = S() * PHI**2
        S3 = S() * PHI
        self.assertTrue(Eq(5*(S6.ivm_volume()) + 5*(S3.ivm_volume()), 5))
        
        
class Test_Triangle(unittest.TestCase):
    
    def test_unit_area1(self):
        tri = Triangle(DIAM, DIAM, DIAM)
        self.assertEqual(tri.ivm_area(), 1)
        
    def test_xyz_area1(self):
        v1 = Vector((2, 0, 0))
        v2 = Vector((0, 2, 0))
        tri = make_tri(v1, v2)
        self.assertEqual(tri.xyz_area().evalf(), 8)

    def test_xyz_area2(self):
        v1 = Vector((1, 0, 0))
        v2 = Vector((0, 1, 0))
        tri = make_tri(v1, v2)
        self.assertEqual(tri.xyz_area().evalf(), 2)

    def test_area_martian1(self):
        two = Integer(2)
        one = Integer(1)
        p = Qvector((two,one,0,one))
        q = Qvector((two,one,one,0))
        result = 3*p.area(2*q)
        self.assertEqual(result, 6)     
 
    def test_area_martian2(self):
        two = Integer(2)
        one = Integer(1)
        p = 3 * Qvector((two,one,0,one))
        q = 4 * Qvector((two,one,one,0))
        result = p.area(q)
        self.assertEqual(result, 12)

    def test_area_martian3(self):
        two = Integer(2)
        one = Integer(1)
        p = Qvector((two,one,0,one))
        q = Qvector((two,one,one,0))
        tri = make_tri(p, q)
        self.assertEqual(tri.ivm_area(), 1)

    def test_area_martian4(self):
        two = Integer(2)
        one = Integer(1)
        p = 3 * Qvector((two,one,0,one))
        q = 4 * Qvector((two,one,one,0))
        tri = make_tri(p, q)
        self.assertEqual(tri.ivm_area().evalf(), 12)
           
def command_line():
    args = sys.argv[1:]
    try:
        args = [float(x) for x in args] # floats
        t = Tetrahedron(*args)
    except TypeError:
        t = Tetrahedron(1,1,1,1,1,1)
        print("defaults used")
    print(t.ivm_volume())
    print(t.xyz_volume())
        
if __name__ == "__main__":
    if len(sys.argv)==7:
        command_line()  
    else:
        unittest.main()
