#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
See:
https://oeis.org/A007531

Number of contact points between equal spheres 
arranged in a tetrahedron with n - 1 spheres 
in each edge. - Ignacio Larrosa Cañestro, Jan 07 2013

With thanks to
https://www.instagram.com/struppipohl/
who derived this result as well.

[edges(n) for n in range(1, 100)]
Out[21]: 
[6,
 24,
 60,
 120,
 210,
 336,
 504,
 720,
 990,
 1320,
 ...
 884640,
 912576,
 941094,
 970200,
 999900]
"""


def tri(n : int) -> int:
    "Triangular number n"
    return (n)*(n+1)//2
    
def edges(f : int) -> int:
    """
    Each layer of tri(N) balls 3, 10, 15...
    spawns N tetrahedrons of 6 edges each, accumulating 
    to give a next layer of Tri(N+1) balls, and so on.
    f = frequency (number of intervals along each edge)
    """
    cumm = 0
    for layer in range(1, f+1):
        if layer == 1:  # initial frequency
            cumm = 6
        else:
            cumm = cumm + tri(layer-1)*6
    return cumm    