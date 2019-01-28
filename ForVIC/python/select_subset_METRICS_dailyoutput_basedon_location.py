#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: liuming

Create a subset of soil parameter file from cell list
"""

import pandas as pd
import sys 
import os

if len(sys.argv) != 5:
    print("Usage:" + sys.argv[0] + "<original_big_file> <x> <y> <out_new_file>\n")
    sys.exit(0)

orig_file = sys.argv[1]
x = float(sys.argv[2])
y = float(sys.argv[3])
new_file = sys.argv[4]

outfile_soil = open(new_file,"w")


#read soil parameter to create location dictionary
with open(orig_file) as f:
    for line in f:
        #cell = line.rstrip()
        cell = line.split()
        if "row" in cell:
            outfile_soil.write(line)
        else:
            if abs(float(cell[2]) - x) <= 15 and abs(float(cell[3]) - y) <= 15:
                outfile_soil.write(line)
outfile_soil.close()
print("Getting subset done!")

