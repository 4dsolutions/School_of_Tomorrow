#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 11:22:53 2020

Generate Mersenne Primes using both brute force and
Miller-Rabin probable primes tester.

Mostly I raided my old Python 2.x stash here:
    http://4dsolutions.net/ocn/python/primes.py
    (Oregon Curriculum Network)
    
Thanks to calcpage for the inspiration.
Doing it in Java:  https://youtu.be/-Snd7a55FrE

@author: Kirby Urner
"""

import random

_primes = [2]    # global list of primes

def iseven(n):
   """Return true if n is even."""
   return n%2==0

def isodd(n):
   """Return true if n is odd."""   
   return not iseven(n)


def divtrial(n):
   """
   Trial by division check whether a number is prime."""
   verdict = 1      # default is "yes, add to list"
   cutoff  = n**0.5 # 2nd root of n
   
   for i in _primes:
        if not n%i:      # if no remainder
           verdict = 0   # then we _don't_ want to add
           break
        if i >= cutoff:  # stop trying to divide by
           break         # lower primes when p**2 > n

   return verdict

def isprime(n):
   """
   Divide by primes until n proves composite or prime.

   Brute force algorithm, will wimp out for humongous n
   return 0 if n is divisible
   return 1 if n is prime"""
   
   rtnval = 1

   if n == 2: return 1
   if n < 2 or iseven(n): return 0
   
   maxnb = n ** 0.5 # 2nd root of n

   # if n < largest prime on file, check for n in list   
   if n <= _primes[-1]: rtnval = (n in _primes)

   # if primes up to root(n) on file, run divtrial (a prime test)
   elif maxnb <= _primes[-1]: rtnval = divtrial(n)
   
   else:
      rtnval = divtrial(n)   # check divisibility by primes so far

      if rtnval==1:       # now, if still tentatively prime...
         # start with highest prime so far
         i = _primes[-1]
         # and add...
         i = i + 1 + isodd(i)*1     # next odd number
         while i <= maxnb:
            if divtrial(i):         # test of primehood
                _primes.append(i)    # append to list if prime
                if not n%i:         # if n divisible by latest prime
                   rtnval = 0       # then we're done
                   break
            i=i+2                   # next odd number

   return rtnval

def pptest(n):
    """
    Simple implementation of Miller-Rabin test for
    determining probable primehood.
    """
    bases  = [random.randrange(2,50000) for _ in range(90)]

    # if any of the primes is a factor, we're done
    if n<=1: return 0
    
    for b in bases:
        if n%b==0: return 0
        
    tests,s  = 0,0
    m        = n-1

    # turning (n-1) into (2**s) * m
    while not m&1:  # while m is even
        m >>= 1
        s += 1
    for b in bases:
        tests += 1
        isprob = algP(m,s,b,n)
        if not isprob: break
            
    if isprob: return (1-(1./(4**tests)))
    else:      return 0
    
def algP(m,s,b,n):
    """
    based on Algorithm P in Donald Knuth's 'Art of
    Computer Programming' v.2 pg. 395 
    """
    result = 0
    y = pow(b,m,n)    
    for j in range(s):
       if (y==1 and j==0) or (y==n-1):
          result = 1
          break
       y = pow(y,2,n)       
    return result

m = 1
for n in range(650):
    candidate = 2**n - 1
    if len(str(candidate)) < 10:
        if isprime(candidate):
            print(f"M{m} = 2**{n}-1 = {candidate}")            
            m += 1
    else: 
        if pptest(2**n-1):
            print(f"M{m} = 2**{n}-1 = {candidate}")
            m += 1