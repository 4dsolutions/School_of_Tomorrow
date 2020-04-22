#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 15:07:45 2020

@author: Kirby Urner in conversation with David Koski

"""
import mpmath
from mpmath import mpf

mpmath.mp.dps = 50

three = mpf(3)
four  = mpf(4)
five  = mpf(5)
six   = mpf(6)
two   = mpf(2)
eight = mpf(8)
root2 = two.sqrt()
root5 = five.sqrt()

φ  = (root5+1)/two
Smod = (φ **-five)/two
smod3 = Smod * φ **-three
smod6 = Smod * φ **-six

Emod  = (root2/eight) * (φ ** -3)
emod3 = Emod * (φ ** -3)
emod6 = Emod * (φ ** -6)

T_factor = mpf("3/2")**mpf("1/3") * root2/φ
Tmod = Emod*1/T_factor**3
# FAKE PI
PhiPi = (six/five) * φ**2

S_factor = Smod/Emod
print(φ)
print(Smod)
print(Emod)
print(PhiPi)

RTplus = 120 * Emod
print(f"{RTplus}")

PhiPiRT = PhiPi * two.sqrt()
#print(f"PhiPiBall {PhiPiBall}")

# EXACTLY = RTPLUS IN VOLUME
print(PhiPiRT * 25*Smod)

k = mpmath.mpf('52.8')
r = mpmath.mpf('19.2')

# ALGEBRAIC IDENTITY
print(RTplus - PhiPiRT)
print(k * emod3 + r * emod6)

special_mod = PhiPiRT/120
print(500 * special_mod)
print(20 * Emod/Smod)

print(126*Smod + 30*smod3)
print(f"E_mod: {Emod}")
print(f"T_mod: {Tmod}")
print(f"Special_mod: {special_mod}")

cubocta = mpf('2.5')
print("CO2.5:", mpf('52.5')*Smod + mpf('12.5')*smod3)
print("Myst:", 60*emod3 + 20*emod6)
InterMediate = cubocta * S_factor
print("Intermediate:", InterMediate)
print(InterMediate * PhiPiRT)
IcosaWithin = cubocta * S_factor ** 2
print("IcoWithin:", IcosaWithin)
print("Octa:", IcosaWithin + 24 * Smod)

print(InterMediate * PhiPiRT)