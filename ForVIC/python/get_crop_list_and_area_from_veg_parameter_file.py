#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan. 22, LIU
Convert crop fractions into VIC veg files (irrigation is processed for next step)
Note: the calibration does not need the irrigation information so the irrigation file can be generated late
@author: liuming


Use original vegetation parameter (for Forecast project) as natural vegetation
"""

import pandas as pd
import sys 
import os

def sortkey(x): 
    return int(x)

#input lists:
#monthly LAI
#always ture!!!
use_old_veg_parameter_lai = True
vic_area = "/mnt/hydronas/Projects/BPA_CRB/GIS/boundary/vicid_areakm2_list.txt"

veg_parameters = {
        "old_nat_veg" : "/home/liuming/temp/temp/CRB_vegetation_parameter_use_oldnatveg.txt",
        "new_nat_veg" : "/home/liuming/temp/temp/CRB_vegetation_parameter.txt"
        }

outfiles = {
        "old_nat_veg" : "/home/liuming/temp/temp/CRB_vegetation_parameter_use_oldnatveg_veglist_and_area(total_km2).txt",
        "new_nat_veg" : "/home/liuming/temp/temp/CRB_vegetation_parameter_veglist_and_area(total_km2).txt"
        }

#get vic area for each grid
vic_area_dic = dict()
with open(vic_area) as f:
    for line in f:
        a = line.split()
        if len(a) > 0:
            if a[0] not in vic_area_dic:
                vic_area_dic[a[0]] = float(a[1])
print("vic area done!")

for pf in veg_parameters:
    fout = open(outfiles[pf],"w")
    fract = dict()
    with open(veg_parameters[pf]) as f:
        for line in f:
            a = line.split()
            if len(a) == 2:
                if a[0] in vic_area_dic:
                    cellarea_km2 = vic_area_dic[a[0]]
                else:
                    cellarea_km2 = 36.3
            elif len(a) == 8:
                if a[0] not in fract:
                    fract[a[0]] = float(a[1]) * cellarea_km2
                else:
                    fract[a[0]] += float(a[1]) * cellarea_km2
    for veg in sorted(fract, key=sortkey, reverse=False):
        fout.write(veg + " " + str('%.3f' % fract[veg]) + "\n")
    print(pf + " done")
    fout.close()
print("All done!")
