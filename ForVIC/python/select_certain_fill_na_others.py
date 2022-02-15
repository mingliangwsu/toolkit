#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 01:45:46 2018

@author: liuming
"""

import pandas as pd
import os
import glob
import sys

infile = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/auxdata/patchgrid.txt"
outfile = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/auxdata/patchgrid_3patch.txt"
selected = ["55067","55459","54674"]
na = "-9999"

fout = open(outfile,"w")

with open(infile) as f:
    for line in f:
        cells = line.rstrip().split(' ')
        if len(cells) > 0:
            for cell in cells:
                if cell not in selected:
                    fout.write(na + " ")
                else:
                    fout.write(cell + " ")
        fout.write("\n")
            
        
fout.close()
print("Done!")
