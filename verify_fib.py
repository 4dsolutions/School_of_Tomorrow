#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 07:07:28 2024

@author: kirbyurner

Verify a claim about the Fibonacci Numbers 
visually proved by Ghee Beom Kim.

https://flic.kr/p/2qCuqqR

William Scheid provided a proof by mathematical 
induction for n >= 2 in the comments.
"""

def fibs():  
    "generate the next fib"
    last = 1
    before_last = 0
    while True:
        yield last
        before_last, last = last, before_last + last
        
def verify():
    genfib = fibs()
    next(genfib)           # 1, n=1
    fibnext = next(genfib) # 1, n=2
    the_sum = 2  # 1**2 + 1**2 == 1 * 2 check
    for n in range(3, 101):
        the_product = fibnext * (fibnext := next(genfib))
        assert the_sum == the_product # crash if not
        the_sum = the_sum + fibnext ** 2
    print("Good as Gold!")
   
if __name__ == "__main__":
    verify()
    