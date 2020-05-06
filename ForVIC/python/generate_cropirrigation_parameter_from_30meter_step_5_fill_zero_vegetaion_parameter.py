#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 09:12:25 2020
Find grid cell without vegetation parameter by filling zero

@author: liuming
"""

# this block of code copied from https://gist.github.com/ryan-hill/f90b1c68f60d12baea81 
import pandas as pd
import pysal as ps
import numpy as np

def sortkey(x): 
    return int(x)

datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/irrigation/"
inveg_file = datapath + "pnw_veg_parameter.txt"
outveg_file = datapath + "pnw_veg_parameter_filledzero.txt"
viclist_file = datapath + "viclist.txt"


fout = open(outveg_file,"w")
gridlist = list()
veglist = list()

with open(viclist_file) as f:
    for line in f:
        a = line.rstrip().split()
        if len(a) > 0:
            if a[0] not in gridlist:
                gridlist.append(a[0])
with open(inveg_file) as f:
    for line in f:
        a = line.rstrip().split()
        if len(a) > 0:
            if len(a) == 2:
                if a[0] not in veglist:
                    veglist.append(a[0])
            fout.write(line)
for grid in gridlist:
    if grid not in veglist:
        fout.write(grid + " 0\n")

fout.close()
print('Done.\n')

    
    
        