#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 17:48:56 2020

@author: Kirby Urner

Verifying a Ramanujan Identity
https://flic.kr/p/2j9NcAd

Keywords:  recursion, number theory, arbitrary precision

School of Tomorrow
https://medium.com/@kirbyurner/calculator-of-tomorrow-using-arbitrary-precision-8f219b0092d9
https://repl.it/@kurner/RamanujanIdentity01
"""

import mpmath
from mpmath import e, pi
print(mpmath.libmp.BACKEND)
mpmath.mp.dps = 100
two   = mpmath.mpf('2')
five  = mpmath.mpf('5')
root5 = mpmath.mpf('5').sqrt()
phi = (1 + root5)/2

term = "(1 + (e ** (-2*{} * pi))/{})"

def cont_frac(n, c=1):
    """
    Recursively build the continued fraction, 
    as a string, to level of depth n
    """
    if n==0:
        return "1"
    else:    
        return "(1 + ((e ** (-2*{} * pi)/{})))".format(c, cont_frac(n-1, c+1))

print(eval(cont_frac(10))) # evaluate the continued fraction
print(1/(((phi * root5).sqrt() - phi) * e ** (two/five * pi))) # left side of the equation
print("Ta daa!")