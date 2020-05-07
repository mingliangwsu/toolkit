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
veg_file = datapath + "pnw_veg_parameter_filledzero.txt"
outlist_file = datapath + "allcroplist.txt"


croplist = list()

with open(veg_file) as f:
    for line in f:
        a = line.rstrip().split()
        if len(a) == 8:
            if a[0] not in croplist:
                croplist.append(a[0])
fout = open(outlist_file,"w")
croplist.sort(key = int)
for crop in croplist:
    fout.write(crop + "\n")

fout.close()
print('Done.\n')

    
    
        