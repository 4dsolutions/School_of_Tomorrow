#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 09:28:28 2025

@author: kirbyurner

A School of Tomorrow approach to learning Python includes:
(a) learning to use Jupyter Notebooks
(b) learning to use an IDE (vs a Notebook as an IDE)
(c) practicing using Python as a calulator with Nested Hierarchy i.e. BASKET

https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator

https://mail.python.org/archives/list/edu-sig@python.org/message/6IVIMHQLBN5UVJHKKM7JJEVLXI7O35WQ/

https://docs.google.com/presentation/d/13QLfgKo6kyX0j0K0RJ7W0uisB0ZyeBiK-_qbzytipck/edit?usp=sharing

OUTPUT:
    
phi: 1/2 + sqrt(5)/2
phi: 1.61803398874989
----
Smod: 1/(2*(1/2 + sqrt(5)/2)**5)
Smod: 0.0450849718747371
----
Emod: sqrt(2)/(8*(1/2 + sqrt(5)/2)**3)
Emod: 0.0417313169277737
----
sfactor: 2*sqrt(2)/(1/2 + sqrt(5)/2)**2
sfactor: 1.08036302695091
----
IW: 20/(1/2 + sqrt(5)/2)**4
IW: 2.91796067500631
--- calcs ---
1/((1/2 + sqrt(5)/2)**3 + (1/2 + sqrt(5)/2)**6)
11 + 5*sqrt(5)
1/(11 + 5*sqrt(5))
0.0450849718747371
Equal Smod?: True
----
Octa: 4
Octa: 4.00000000000000

"""
import sympy
from sympy import sqrt as rt2

root2 = rt2(2)
root5 = rt2(5)
phi = (1 + root5)/2
print("phi:", phi)
print("phi:", phi.evalf())
print("----")

Smod = 1/(2 * phi ** 5) 
print("Smod:",Smod)
print("Smod:",Smod.evalf())
print("----")

Emod = (root2/8)*(phi**-3)
print("Emod:",Emod)
print("Emod:",Emod.evalf())
print("----")

sfactor = Smod/Emod
print("sfactor:",sfactor)
print("sfactor:",sfactor.evalf())
print("----")

# Icosa Within (volume = cubocta of 2.5 * sfactor * sfactor)
IW = sympy.Rational(5,2) * sfactor**2
print("IW:", IW)
print("IW:", IW.evalf())
print("--- calcs ---")

print(1/(phi**3 + phi**6))
print((phi**3 + phi**6).simplify())
print(1/(11 + 5*root5))
print((1/(11 + 5*root5)).evalf())
print("Equal Smod?:",sympy.Eq(1/(11 + 5*root5), Smod))
print("----")

# IW + 24S modules = 4 exactly
print("Octa:",((24 * Smod) + IW).simplify())
print("Octa:",((24 * Smod) + IW).evalf())

