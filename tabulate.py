#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 20:02:12 2024

Make a pandas table of concentric hierarchy 
polys using qray coords (A, B, C, D) and 
xyz coords (X, Y, Z).

@author: kirbyurner
"""

import flextegrity as fx
import pandas as pd
import numpy as np

arrays = [
    coordsys := ["IVM", "IVM", "IVM", "IVM", "XYZ", "XYZ", "XYZ"],
    coordnms := ["A", "B", "C", "D", "X", "Y", "Z"]]
col_tuples = list(zip(*arrays))
col_tuples

def tabulate(shape, dec=False, n=8):
    vs = shape.vertexes.items()
    shape_name = shape.nick
    rows = []
    row_tuples = []

    for label, v in vs:
        xyz = v.xyz
        row_tuples.append((shape_name, label))
        if not dec:
            rows.append(dict(name = label, 
                             A=v.a, 
                             B=v.b, 
                             C=v.c, 
                             D = v.d, 
                             X = xyz.x, 
                             Y = xyz.y, 
                             Z = xyz.z))
        else:
            rows.append(dict(name = label, 
                             A = v.a.evalf(n).round(n), 
                             B = v.b.evalf(n).round(n), 
                             C = v.c.evalf(n).round(n), 
                             D = v.d.evalf(n).round(n), 
                             X = xyz.x.evalf(n).round(n), 
                             Y = xyz.y.evalf(n).round(n), 
                             Z = xyz.z.evalf(n).round(n)))  
                        
    df = pd.DataFrame.from_dict(rows)
    col_index = pd.MultiIndex.from_tuples(col_tuples, names=["System", "Coords"])
    row_index = pd.MultiIndex.from_tuples(row_tuples, names=["Shape", "Verts"])
    df.index = row_index
    df.drop(columns="name", axis=1, inplace=True)
    df.columns = col_index
    return df

def make_matrix(shape):
    the_edges = shape.unique
    labels = set()
    for verts in the_edges:
        labels.add(verts[0])
        labels.add(verts[1])
    labels = sorted(list(labels))
    face_matrix = pd.DataFrame(data=np.zeros((len(labels), len(labels)), dtype=int), 
                           index = labels,
                           columns = labels)
    for verts in the_edges:
        face_matrix.loc[verts[0], verts[1]] = 1
        face_matrix.loc[verts[1], verts[0]] = 1
    return face_matrix

if __name__ == "__main__":
    tet = tabulate(fx.Tetrahedron())
    invtet = tabulate(fx.InvTetrahedron())
    cu   = tabulate(fx.Cube())
    octa = tabulate(fx.Octahedron())
    rd   = tabulate(fx.RD())
    co   = tabulate(fx.Cuboctahedron())
    
    master_df = pd.concat((tet, invtet, cu, octa, rd, co), axis=0)
    faces_cu = make_matrix(fx.Cube())
    