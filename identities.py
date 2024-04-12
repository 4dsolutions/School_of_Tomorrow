#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 11:09:23 2019

@author: Kirby Urner
"""

"""
From David Koski's paper:

Revisiting R.B. Fuller's S & E Modules

--------
The concentric hierarchy can be described in terms of 
phi-scaled S modules: 

Tetrahedron:  21S +  5s3 =  5S3 + 1S = 1S6 + 1S3 
Cube       :  72S + 15s3 = 15S3 + 3S = 3S6 + 3S3 
Octahedron :  84S + 20s3 = 20S3 + 4S = 4S6 + 4S3 
Rh Triac   : 105S + 25s3 = 25S3 + 5S = 5S6 + 5S3 (volume = 5) 
Rh Dodec   : 126S + 30s3 = 30S3 + 6S = 6S6 + 6S3
Pent Dodeca: 348E + 84e3
Icosahedron: 100E3 + 20E
VE         : 20
SuperRT    : 20 * S3
--------

On-line:  http://coffeeshopsnet.blogspot.com/2017/06/koski-paper.html
"""
from math import sqrt as rt2

import pandas as pd
import numpy as np

shapes = pd.Series(
    np.array(["SuperRT",
              "Cubocta",
              "Icosa",
              "P Dodeca",
              "Rh Dodeca",
              "RT5+",
              "RT5",
              "Octa",
              "Cube",
              "Sm Icosa",
              "Sm VE",
              "Tetra",
              "Emod3",
              "Emod",
              "emod3",
              "Tmod",
              "Amod",
              "Bmod",
              "Smod3",
              "Smod",
              "smod3"], dtype=np.unicode_),
    name="Shapes")

zeros         = pd.Series(np.zeros((21,)), dtype=np.float64)
volumes_table = pd.DataFrame({"Volumes" : zeros,
                              "Comments": pd.Series(['']*21, 
                                            dtype=np.unicode_)
                             })
volumes_table.index = shapes
#%%

φ  = (rt2(5)+1)/2      # golden ratio
S3 = rt2(9/8)          # not to be confused with Smod

Smod = (φ **-5)/2      # home base Smod
smod3 = Smod  * φ**-3  # small s, phi down
Smod3 = Smod  * φ**3   # capital s, phi up
Smod6 = Smod3 * φ**3   # phi up yet again

cubocta = 20
SuperRT = S3 * cubocta

Octa = 4

Emod3 = SuperRT / 120          # Emod phi up
Emod = (rt2(2)/8) * (φ ** -3)  # home base Emod
emod3 = Emod * φ ** -3         # Emod phi down

S_factor = Smod / Emod
T_factor = pow(3/2, 1/3) * rt2(2)/φ

SmallVE = 20 * 1/8  # half D edges (=R)
SkewIcosa = SmallVE * S_factor * S_factor
Smod_check = (Octa - SkewIcosa)/24
assert round(Smod,8) == round(Smod_check,8)

volumes_table.loc['SuperRT',    "Volumes"]  = SuperRT
volumes_table.loc['SuperRT',   "Comments"]  = "Emods RT phi-up, (Icosa, P Dodeca)"
volumes_table.loc['Cubocta',    "Volumes"]  = cubocta
volumes_table.loc['Cubocta',   "Comments"]  = "12 balls around 1"
volumes_table.loc['Icosa',      "Volumes"]  = 100*Emod3 + 20*Emod
volumes_table.loc['Icosa',     "Comments"]  = "Jitterbug first stop"
volumes_table.loc['P Dodeca',   "Volumes"]  = 348*Emod  + 84*emod3
volumes_table.loc['P Dodeca',  "Comments"]  = "Icosahedron Dual"
volumes_table.loc['Rh Dodeca',  "Volumes"]  = 6*Smod6 + 6*Smod3
volumes_table.loc['Rh Dodeca', "Comments"]  = "Space-filler, ball domain, (Cube, Octa)"
volumes_table.loc['RT5+',       "Volumes"]  = 120*Emod
volumes_table.loc['RT5+',      "Comments"]  = "Radius = 1.0000"
volumes_table.loc['RT5',        "Volumes"]  = 5*Smod6 + 5*Smod3
volumes_table.loc['RT5',       "Comments"]  = "Radius = 0.9994"
volumes_table.loc['Octa',       "Volumes"]  = 4*Smod6 + 4*Smod3
volumes_table.loc['Octa',      "Comments"]  = "Jitterbug 2nd stop, Cube dual"
volumes_table.loc['Cube',       "Volumes"]  = 3*Smod6 + 3*Smod3
volumes_table.loc['Cube',      "Comments"]  = "Duo-tet cube, Octa dual"
volumes_table.loc['Sm Icosa',   "Volumes"]  = SmallVE * S_factor * S_factor
volumes_table.loc['Sm Icosa',  "Comments"]  = "Faces flush with Octa"
volumes_table.loc['Sm VE',      "Volumes"]  = SmallVE
volumes_table.loc['Sm VE',     "Comments"]  = "Faces flush with Octa"
volumes_table.loc['Tetra',      "Volumes"]  = 5*Smod3 + Smod
volumes_table.loc['Tetra',     "Comments"]  = "Unit Volume"
volumes_table.loc['Emod3',      "Volumes"]  = Emod3
volumes_table.loc['Emod3',     "Comments"]  = "Emod phi up"
volumes_table.loc['Emod',       "Volumes"]  = Emod
volumes_table.loc['Emod',      "Comments"]  = "1/120th RT5+"
volumes_table.loc['emod3',      "Volumes"]  = emod3
volumes_table.loc['emod3',     "Comments"]  = "Emod phi down"
volumes_table.loc['Tmod',       "Volumes"]  = Emod * 1/T_factor**3 # 1/24
volumes_table.loc['Tmod',      "Comments"]  = "1/120th RT5"
volumes_table.loc['Amod',       "Volumes"]  = 1/24
volumes_table.loc['Amod',      "Comments"]  = "12 left + 12 right = Tetra"
volumes_table.loc['Bmod',       "Volumes"]  = 1/24
volumes_table.loc['Bmod',      "Comments"]  = "48A + 48B = Octa"
volumes_table.loc['Smod3',      "Volumes"]  = Smod3
volumes_table.loc['Smod3',     "Comments"]  = "Smod phi up"
volumes_table.loc['Smod',      "Volumes" ]  = Smod
volumes_table.loc['Smod',     "Comments" ]  = "Sm Icosa + 24 Smods = Octa"
volumes_table.loc['smod3',      "Volumes"]  = smod3
volumes_table.loc['smod3',     "Comments"]  = "Smod phi down"

def print_table():
    print("Five VEs      : {:10.6f}".format(480*Smod + 280*smod3))
    print("SuperRT       : {:10.6f}".format(SuperRT))
    print("Cubocta       : {:10.6f}".format(cubocta))
    # print("Volume of Icosa   : {:10.6f}".format(20 * 1/S_factor))
    # print("Volume of Icosa   : {:10.6f}".format(420 * Emod + 100 * emod3))
    print("Icosa         : {:10.6f}".format(100*Emod3 + 20*Emod))
    print("P Dodeca      : {:10.6f}".format(348*Emod  + 84*emod3))
    print("Rh Dodeca (RD): {:10.6f}".format(6*Smod6 + 6*Smod3))
    print("RT5+          : {:10.6f}".format(120*Emod))
    print("RT5           : {:10.6f}".format(5*Smod6 + 5*Smod3))
    print("Octa          : {:10.6f}".format(4*Smod6 + 4*Smod3))
    print("Cube          : {:10.6f}".format(3*Smod6 + 3*Smod3))
    print("Skew Icosa    : {:10.6f}".format(SmallVE * S_factor * S_factor))
    print("Small VE      : {:10.6f}".format(SmallVE))
    print("Tetra         : {:10.6f}".format(5*Smod3 + Smod))
    print("-" * 20)
    print("Emod3         : {:10.6f}".format(Emod3)) 
    print("Emod          : {:10.6f}".format(Emod)) 
    print("emod3         : {:10.6f}".format(emod3)) 
    print("Tmod          : {:10.6f}".format(Emod*1/T_factor**3)) 
    print("Smod6         : {:10.6f}".format(Smod6))
    print("Smod3         : {:10.6f}".format(Smod3))
    print("Smod          : {:10.6f}".format(Smod))
    print("Smod (check)  : {:10.6f}".format(Smod_check))
    print("smod3         : {:10.6f}".format(smod3))

if __name__ == "__main__":
    print_table()
    