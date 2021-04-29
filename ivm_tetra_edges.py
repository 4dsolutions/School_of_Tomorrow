#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
See:
https://oeis.org/A007531
Number of contact points between equal spheres 
arranged in a tetrahedron with n - 1 spheres 
in each edge. - Ignacio Larrosa Cañestro, Jan 07 2013

https://oeis.org/A035006
Number of contact points between equal spheres 
arranged in a half octahedron with n - 1 spheres 
in each edge. - Kirby Urner, Apr 27 2021

https://oeis.org/A300758
Number of contact points between equal spheres 
arranged in an octahedron with n - 1 spheres 
in each edge. - Kirby Urner, Apr 27 2021

With thanks to
https://www.instagram.com/struppipohl/
who derived the tet_edges result as well.

>>> [tet_edges(n) for n in range(1, 100)] 
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
    
def sqr(n : int) -> int:
    "Square number n"
    return n**2

def tet_edges(f : int) -> int:
    """
    Each layer of tri(N) balls 3, 10, 15...
    spawns N tetrahedrons of 6 edges each, accumulating 
    to give a next layer of tri(N+1) balls, and so on.
    f = frequency (number of intervals along each edge)
    """
    cumm = 0
    for layer in range(1, f+1):
        if layer == 1:  # initial frequency
            cumm = 6
        else:
            cumm = cumm + tri(layer)*6
    return cumm    

def half_oct_edges(f : int) -> int:
    """
    Each layer of sqr(N) balls 4, 9, 16...
    spawns N half-octahedrons, with 4*N edges
    to the next layer of N+1 balls per edge, 
    plus (layer+1)*layer*2 layer edges.
    """
    cumm = 0
    for layer in range(1, f+1):
        if layer == 1:  # initial frequency
            cumm = 8
        else:
            cumm =  cumm + \
                    sqr(layer)*4 + \
                    (layer+1)*layer*2
    return cumm 

def oct_edges(f : int) -> int:
    """
    Two half-octas minus the layer they have in common
    """
    return 2*half_oct_edges(f) - (f+1)*f*2

def make_table(n:int, nm:str = "edges_table.txt", s:str = "tetra") -> None:
    """
    n:   up to max frequency
    nm:  name of output file
    s:   shape used for accumulating 
         ("tetra", "hocta", "octa")
    
    prints a file as a side effect, using either 
    tetra or half-octa edge accumulator as f:Callable = global function
    """
    template = "{:3}. {:10d}"
    if s=="tetra":
        f = tet_edges
    elif s=="hocta":
        f = half_oct_edges # globals 
    elif s=="octa":
        f = oct_edges    
    with open(nm, "w") as output:
        print("Freq      Edges", file=output)
        print("---------------", file=output)
        for i in range(n):
            print(template.format(i, f(i)), file=output)

            
def a007531(n):
    "tetra edges (ball contacts)"
    return n*(n+1)*(n+2)

def a035006(n):
    "half octa edges (ball contacts)"
    return n*2*(n+1)**2

def a300758(n):
    "octa edges (ball contacts)"
    return 2*n*(n+1)*(2*n+1)