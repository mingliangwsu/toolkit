#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: liuming

Create a subset of soil parameter file from cell list
"""

import pandas as pd
import sys 
import os

if len(sys.argv) == 0:
    print("Usage:" + sys.argv[0] + "<original_big_file> <xmin> <ymin> <xmax> <ymax> <out_new_file>\n")
    sys.exit(0)

orig_file = sys.argv[1]
xmin = float(sys.argv[2])
ymin = float(sys.argv[3])
xmax = float(sys.argv[4])
ymax = float(sys.argv[5])
new_file = sys.argv[6]

if xmin > xmax:
    t = xmin
    xmin = xmax
    xmax = t
if ymin > ymax:
    t = ymin
    ymin = ymax
    ymax = t

outfile_soil = open(new_file,"w")


#read soil parameter to create location dictionary
with open(orig_file) as f:
    for line in f:
        #cell = line.rstrip()
        cell = line.split()
        if "x" in cell:
            outfile_soil.write(line)
        else:
            if float(cell[0]) >= xmin and float(cell[0]) <= xmax and float(cell[1]) >= ymin and float(cell[1]) <= ymax:
                outfile_soil.write(line)
outfile_soil.close()
print("Getting subset done!")

