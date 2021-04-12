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
datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Veg/"
veg_file = datapath + "pnw_veg_parameter_filledzero_state_reclassified.txt"

irrigation_path = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Management/"
irrigation_file = irrigation_path + "pnw_irrigation_state_reclassified.txt"


out_irrigated = datapath + "irrigated_gridcells.txt"
out_cropall = datapath + "all_crops_gridcells.txt"

allcrop_grid = list()
#vegetation parameter
with open(veg_file) as f:
    for line in f:
        a = line.rstrip().split()
        if len(a) == 2:
            grid = a[0]
        if len(a) == 8:
            cropcodeint = int(a[0])
            if cropcodeint > 20:
                if grid not in allcrop_grid:
                    allcrop_grid.append(grid)
with open(out_cropall,"w") as fout:
    for grid in allcrop_grid:
        outline = grid + "\n"
        fout.write(outline)
#irrigation parameter
with open(out_irrigated,"w") as fout:
    with open(irrigation_file) as f:
        for line in f:
            a = line.rstrip().split()
            if a[1].isdigit():
                if int(a[1]) >= 1:
                    outline = a[0] + "\n"
                    fout.write(outline)
print('Done.\n')

    
    
        