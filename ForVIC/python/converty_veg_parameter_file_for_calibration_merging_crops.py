#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aggregate crop types into "corn type"
@author: liuming


Use original vegetation parameter (for Forecast project) as natural vegetation
"""

import pandas as pd
import sys 
import os

def sortkey(x): 
    return int(x)

MIN_FRACTION = 0.0001
#input lists:
#monthly LAI
#always ture!!!


veg_parameters = {
        "old_nat_veg" : "/home/liuming/temp/temp/CRB_vegetation_parameter_use_oldnatveg.txt",
        "new_nat_veg" : "/home/liuming/temp/temp/CRB_vegetation_parameter.txt"
        }

outfiles = {
        "old_nat_veg" : "/home/liuming/temp/temp/CRB_vegetation_parameter_use_oldnatveg_calibration.txt",
        "new_nat_veg" : "/home/liuming/temp/temp/CRB_vegetation_parameter_calibration.txt"
        }

fruit_list = ["102","103","104","107","198","401","402","403","804"
              ,"1401","1402","1403","1404","1405","1407","1409","1410","1411","2502"]

corn = "11"
fruit = "4"

lai_dic_default = {
            "1"    : "3.4 3.4 3.5 3.7 4 4.4 4.4 4.3 4.2 3.7 3.5 3.4",
            "2"    : "3.4 3.4 3.5 3.7 4 4.4 4.4 4.3 4.2 3.7 3.5 3.4",
            "3"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "4"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "5"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "6"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "7"    : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "8"    : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "9"    : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "10"   : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "11"   : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "12"   : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "13"   : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2"}
lai_default_missed = "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5"

paramter_dic = {"1"  : "0.1 0.05 1 0.45 5 0.5",
                "2"  : "0.1 0.05 1 0.45 5 0.5",
                "3"  : "0.1 0.05 1 0.45 5 0.5",
                "4"  : "0.1 0.05 1 0.45 5 0.5",
                "5"  : "0.1 0.05 1 0.45 5 0.5",
                "6"  : "0.1 0.1 1 0.65 1 0.25",
                "7"  : "0.1 0.1 1 0.65 1 0.25",
                "8"  : "0.1 0.1 1 0.65 0.5 0.25",
                "9"  : "0.1 0.1 1 0.65 0.5 0.25",
                "10" : "0.1 0.1 1 0.7 0.5 0.2",
                "11" : "0.1 0.1 0.75 0.6 0.5 0.3",
                "12" : "0.1 0.1 0.75 0.6 0.5 0.3",
                "13" : "0.1 0.1 0.75 0.6 0.5 0.3"}
default_veg_parameter = "0.1 0.1 0.75 0.6 0.5 0.3"


for pf in veg_parameters:
    allcells_fract = dict()
    all_cells_lai = dict()
    all_cells_param = dict()
    fout = open(outfiles[pf],"w")
    with open(veg_parameters[pf]) as f:
        for line in f:
            a = line.split()
            if len(a) == 2:
                cellid = a[0]
                if cellid not in allcells_fract:
                    allcells_fract[cellid] = dict()
                if cellid not in all_cells_lai:
                    all_cells_lai[cellid] = dict()
                if cellid not in all_cells_param:
                    all_cells_param[cellid] = dict()
            elif len(a) == 8:
                vegid = a[0]
                if vegid in fruit_list:
                    if fruit not in allcells_fract[cellid]:
                        allcells_fract[cellid][fruit] = float(a[1])
                    else:
                        allcells_fract[cellid][fruit] += float(a[1])
                elif int(vegid) > 100:
                    if corn not in allcells_fract[cellid]:
                        allcells_fract[cellid][corn] = float(a[1])
                    else:
                        allcells_fract[cellid][corn] += float(a[1])
                else:
                    if vegid not in allcells_fract[cellid]:
                        allcells_fract[cellid][vegid] = float(a[1])
                    else:
                        allcells_fract[cellid][vegid] += float(a[1])
                if vegid not in all_cells_param[cellid]:
                    all_cells_param[cellid][vegid] = a[2] + " " + a[3] + " " + a[4] + " " + a[5] + " " + a[6] + " " + a[7]
            elif len(a) == 12:
                if vegid not in all_cells_lai[cellid]:
                    all_cells_lai[cellid][vegid] = line
    
    for cell in sorted(allcells_fract, key=sortkey, reverse=False):
        types = 0
        for veg in allcells_fract[cell]:
            if allcells_fract[cell][veg] >= MIN_FRACTION:
                types += 1
        fout.write(cell + " " + str(types) + "\n")
        for veg in sorted(allcells_fract[cell], key=sortkey, reverse=False):
            if allcells_fract[cell][veg] >= MIN_FRACTION:
                if veg not in all_cells_param[cell]:
                    param = paramter_dic[veg]
                else:
                    param = all_cells_param[cell][veg]
                fout.write("    " + veg + " " + str('%.4f' % allcells_fract[cell][veg]) + " " + param + "\n")
                if veg not in all_cells_lai[cell]:
                    if veg in lai_dic_default:
                        lai = "      " + lai_dic_default[veg] + "\n"
                    else:
                        lai = "      " + lai_default_missed + "\n"
                else:
                    lai = all_cells_lai[cell][veg]
                fout.write(lai)
    fout.close()
print("All done!")
