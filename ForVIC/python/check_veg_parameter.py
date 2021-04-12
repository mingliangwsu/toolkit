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



#datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/irrigation/"
datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Matt_veg_parameter/"
veg_file = datapath + "vegparam.txt"
outreport = datapath + "vegparam.txt.errors"

foutreport = open(outreport,"w")

start_8 = 0
start_12 = 0
numveg = 0
grid = 0
#vegetation parameter
with open(veg_file,"r") as fout:
    with open(veg_file) as f:
        for line in f:
            a = line.rstrip().split()
            if len(a) == 2:
                
                if grid > 0 and (numveg != start_8 or numveg != start_12):
                    outline = "gridcell:" + str(grid) + " vegnum does not match records!\n"
                    foutreport.write(outline)
                grid = int(a[0])
                start_8 = 0
                start_12 = 0
                numveg = int(a[1])
            if len(a) == 8:
                start_8 += 1
            if len(a) == 12:
                start_12 += 1
                


foutreport.close()
print('Done.\n')

    
    
        