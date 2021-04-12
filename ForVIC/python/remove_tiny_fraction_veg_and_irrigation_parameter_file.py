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
import shutil

def sortkey(x): 
    return int(x)

orig_datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/irrigation/"

datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Veg/"
veg_file = datapath + "pnw_veg_parameter_filledzero_state_reclassified.txt"
updated_veg_file = datapath + "pnw_veg_parameter_filledzero_state_reclassified_simplified.txt"


irrigation_path = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Management/"
irrigation_file = irrigation_path + "pnw_irrigation_state_reclassified.txt"
updated_irrigation_file = irrigation_path + "pnw_irrigation_state_reclassified_simplified.txt"


#fveg = open(updated_veg_file,"w")
#firrig = open(updated_irrigation_file,"w")

removed_from_veg_parameter = dict() #[grid] list
outveg = dict() #[grid][veg] list 0: firstline 1: second line
outirrig = dict() #[grid][veg] irrigation type

tol = 0.001

#vegetation parameter
with open(updated_veg_file,"w") as fout:
    with open(veg_file) as f:
        for line in f:
            a = line.rstrip().split()
            if len(a) == 2:
                grid = a[0]
                vegnum = int(a[1])
                if grid not in outveg:
                    outveg[grid] = dict()
            if len(a) == 8:
                veg = a[0]
                fraction = float(a[1])
                remove = False
                if fraction < tol:
                    if grid not in removed_from_veg_parameter:
                        removed_from_veg_parameter[grid] = list()
                    removed_from_veg_parameter[grid].append(veg)
                    remove = True
                else:
                    if veg not in outveg[grid]:
                        outveg[grid][veg] = list()
                    outveg[grid][veg].append(line)
            if len(a) == 12:
                if not remove:
                    outveg[grid][veg].append(line)
    for grid in sorted(outveg, key=sortkey, reverse=False):
        numveg = len(outveg[grid])
        outline = grid + " " + str(numveg) + "\n"
        fout.write(outline)
        for veg in sorted(outveg[grid], key=sortkey, reverse=False):
            for line in outveg[grid][veg]:
                fout.write(line)
                
#irrigation parameter
with open(updated_irrigation_file,"w") as fout:
    with open(irrigation_file) as f:
        for line in f:
            a = line.rstrip().split()
            if a[1].isdigit():
                grid = a[0]
            else:
                veg = a[0]
                if grid in outveg:
                    if veg in outveg[grid]:
                        if grid not in outirrig:
                            outirrig[grid] = dict()
                        if veg not in outirrig[grid]:
                            outirrig[grid][veg] = a[1]
    for grid in sorted(outirrig, key=sortkey, reverse=False):
        numveg = len(outirrig[grid])
        if numveg >= 1:
            outline = grid + " " + str(numveg) + "\n"
            fout.write(outline)
        for veg in sorted(outirrig[grid], key=sortkey, reverse=False):
            outline = "    " + veg + " " + outirrig[grid][veg] + "\n"
            fout.write(outline)
print('Done.\n')

    
    
        