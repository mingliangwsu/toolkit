#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 09:12:25 2020
Generate Vegetation and irrigation parameter based on updated/calculated crop (and natural vegetation) fractions

@author: liuming
"""

# this block of code copied from https://gist.github.com/ryan-hill/f90b1c68f60d12baea81 
import sys
import os
import pandas as pd
import pysal as ps
import numpy as np


def sortkey(x): 
    return int(x)

def lat_from_id(x): 
    lat = (x // 928) * 0.0625 + 25 + 0.0625 / 2.0
    return lat

def lon_from_id(x): 
    lon = ((x - 207873) % 928) * 0.0625 + (-125.0 + 0.0625 / 2.0)
    return lon

def VIC_grid_km2(lat_degree):
    area_km2 = 2.0 * ( 0.0625 * 3.14159 / 180.0 ) * 6371393 * 6371393 * math.cos(lat_degree * 3.1415926 / 180.0) * math.sin(0.0625 * 3.1415926 / 360.0) / 1000000.0
    return area_km2
def lat_lon_to_id(lat,lon):    
    id = ((lat - 25 - 0.0625 / 2) // 0.0625) * 928 + (lon + 125 - 0.0625 / 2.0) / 0.0625 + 1
    return int(id)

crop_irrigation_type = {
    "102" : "DRIP",
    "103" : "SPRINKLER",
    "107" : "DRIP",
    "198" : "DRIP",
    "1401" : "SPRINKLER",
    "1402" : "SPRINKLER",
    "1403" : "SPRINKLER",
    "1407" : "SPRINKLER",
    "1409" : "SPRINKLER",
    "1410" : "SPRINKLER",
    "1411" : "SPRINKLER",
    "2001" : "SPRINKLER",
    "2002" : "SPRINKLER",
    "2207" : "CENTER_PIVOT",
    "2502" : "DRIP",
    "2504" : "SPRINKLER",
    "2505" : "DRIP",
    "4004" : "CENTER_PIVOT",
    "4005" : "CENTER_PIVOT",
    "4006" : "CENTER_PIVOT",
    "4007" : "CENTER_PIVOT",
    "4008" : "CENTER_PIVOT",
    "4009" : "CENTER_PIVOT",
    "4010" : "CENTER_PIVOT",
    "4011" : "BIG_GUN",
    "4100" : "CENTER_PIVOT",
    "4101" : "CENTER_PIVOT",
    "4102" : "CENTER_PIVOT",
    "7106" : "BIG_GUN",
    "7202" : "CENTER_PIVOT",
    "7206" : "RILL",
    "7207" : "CENTER_PIVOT",
    "7701" : "CENTER_PIVOT",
    "7708" : "BIG_GUN",
    "7720" : "BIG_GUN",
    "7801" : "CENTER_PIVOT",
    "7806" : "DRIP",
    "7807" : "CENTER_PIVOT",
    "8001" : "CENTER_PIVOT",
    "8002" : "SPRINKLER",
    "8205" : "FLOOD",
    "8518" : "SPRINKLER",
    "8704" : "CENTER_PIVOT",
    "8802" : "CENTER_PIVOT",
    "8804" : "RILL",
    "8807" : "BIG_GUN",
    "8809" : "BIG_GUN",
    "8811" : "BIG_GUN",
    "8815" : "BIG_GUN",
    "8817" : "CENTER_PIVOT",
    "8824" : "CENTER_PIVOT",
    "8826" : "CENTER_PIVOT",
    "8828" : "BIG_GUN",
    "8831" : "CENTER_PIVOT",
    "8832" : "CENTER_PIVOT",
    "8834" : "DRIP",
    "8839" : "CENTER_PIVOT",
    "8841" : "CENTER_PIVOT",
    "8904" : "CENTER_PIVOT",
    "8906" : "CENTER_PIVOT",
    "8907" : "CENTER_PIVOT",
    "9209" : "CENTER_PIVOT"
        }

default_crop_irrigation_type = "CENTER_PIVOT"


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
                "13" : "0.1 0.1 0.75 0.6 0.5 0.3",
                "14" : "0.1 0.1 1 0.7 0.5 0.2"}
default_veg_parameter = "0.1 0.1 0.75 0.6 0.5 0.3"


lai_dic = {
            "1" : "1.236 1.371 1.570 1.904 2.511 3.129 3.057 2.538 1.970 1.497 1.278 1.230",
            "2" : "1.821 2.139 2.821 3.750 4.477 4.570 3.913 3.189 2.726 2.269 1.950 1.751",
            "3" : "0.763 0.828 0.897 0.985 1.282 1.943 2.122 1.670 1.156 0.853 0.759 0.749",
            "4" : "1.168 1.312 1.636 2.417 3.719 4.731 4.433 3.601 2.588 1.735 1.317 1.198",
            "5" : "1.587 1.769 2.106 2.758 3.802 4.614 4.452 3.760 2.913 2.123 1.712 1.601",
            "6" : "0.763 0.821 0.948 1.229 1.626 1.774 1.517 1.208 0.989 0.837 0.784 0.758",
            "7" : "0.518 0.574 0.670 0.826 1.065 1.338 1.308 1.034 0.739 0.556 0.513 0.502",
            "8" : "0.603 0.644 0.736 0.915 1.193 1.381 1.261 1.019 0.812 0.678 0.631 0.608",
            "9" : "0.401 0.429 0.492 0.586 0.699 0.809 0.840 0.693 0.514 0.408 0.384 0.390",
            "10" : "0.396 0.430 0.539 0.764 1.045 1.157 0.962 0.719 0.554 0.452 0.420 0.399",
            "12" : "0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000",
            "14" : "0.123 0.125 0.136 0.167 0.197 0.190 0.179 0.157 0.135 0.123 0.116 0.115"
           }

lai_default_missed = "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5"

"""
Always_irrigation = ["102","103","107","198","1401","1402","1403","1407","1409"
                     ,"1410","1411","2002","2207","2502","2505","4004","4005"
                     ,"4007","4008","4011","4100","4101","4102","6002","7106"
                     ,"7202","7206","7207","7701","7720","7801","7806","7807"
                     ,"8001","8002","8704","8802","8807","8809","8811","8815"
                     ,"8817","8820","8826","8828","8831","8832","8834","8839"
                     ,"8841","8904","9204","9205","9208"]
"""

#print("argv_len:" + str(len(sys.argv)))
if len(sys.argv) < 6:
    print("Usage:" + sys.argv[0] + "<new_veg_fraction_table> <original_veg_file> <original_irrigation_file> <output_veg_file> <output_irrigation_file>\n")
    sys.exit(0)
    
newfractionfile = sys.argv[1]
invegfile = sys.argv[2]
inirrfile = sys.argv[3]
outvegfile = sys.argv[4]
outirrfile = sys.argv[5]

new_fraction = dict()       #[grid][veg] total    veg: 1-99999  natualveg -> 1-14
#irrigated_fraction = dict() #[grid][veg] only irrigated

area_tolorense = 0.00001
#read new veg fractions
with open(newfractionfile,"r") as f:
    for line in f:
        a = line.rstrip().split(",")
        if len(a) > 0:
            #if "\"Lat\"" in a:
            if "CellID" in line:
                line = line.replace('"', '')
                varlist = line.split(",")
            else:
                #print(line)
                #print("a[0]" + str(a[0]) + "\n")
                #gridid = str(lat_lon_to_id(float(a[0]),float(a[1])))
                gridid = a[0]
                for idx, val in enumerate(a):
                    #if idx >= 2:
                    #print("idx:" + str(idx) + " val:" + val)
                    if varlist[idx].isnumeric():
                        fraction = float(val)
                        if fraction >= area_tolorense:
                            if gridid not in new_fraction:
                                new_fraction[gridid] = dict()
                            #if int(varlist[idx]) > 10000:
                            #    cropcode = int(varlist[idx]) - 10000
                            #    if cropcode > 100:
                            #        outveg = varlist[idx]
                            #    else:
                            #        outveg = str(cropcode)
                            #else:
                            outveg = varlist[idx]
                            if outveg not in new_fraction[gridid]:
                                new_fraction[gridid][outveg] = fraction
print("Finished reading fractions.\n")
                            
#reading original vegetation parameter                
orig_veg = dict() #[grid][crop] list: fraction + vegparameter(list) + lai(list)  crop:1-20000
with open(invegfile,"r") as f:   
    current_line = 0
    nextgrid_line = 0
    for line in f:
        a = line.rstrip().split()
        if current_line == nextgrid_line: #gridid num_veg
            grid = a[0]
            nextgrid_line += int(a[1]) * 2 + 1
            if grid not in orig_veg:
                orig_veg[grid] = dict()
        else:
            if len(a) == 8:
                vegcode = a[0] 
                if vegcode not in orig_veg[grid]:
                    orig_veg[grid][vegcode] = list()
                    orig_veg[grid][vegcode].append(a[1])
                    orig_veg[grid][vegcode].append(a[2:])
            elif len(a) == 12:
                orig_veg[grid][vegcode].append(a)
        current_line += 1
print("Finished reading veg!")

#read irri information
orig_irr = dict() #[grid][crop] irrigation type
with open(inirrfile,"r") as f:   
    current_line = 0
    nextgrid_line = 0
    for line in f:
        a = line.rstrip().split()
        if current_line == nextgrid_line:
            grid = a[0]
            nextgrid_line += int(a[1]) + 1
            if grid not in orig_irr:
                orig_irr[grid] = dict()
        else:
            if a[0] not in orig_irr[grid]:
                orig_irr[grid][a[0]] = a[1]
        current_line += 1
print("Finished reading irr!")

#Merge original veg & irr. If veg is in new_fraction, update everything for this veg; remove all other veg if it is not in the update veg list
#print new veg parameter file
with open(outvegfile,"w") as f:
    for grid in sorted(orig_veg, key=sortkey, reverse=False):
        if grid not in new_fraction:
            f.write(grid + " 0\n")
        else:
            f.write(grid + " " + str(len(new_fraction[grid])) + "\n")
            for veg in sorted(new_fraction[grid], key=sortkey, reverse=False):
                #coresponding dry or irrigated crop
                if int(veg) > 10000:
                    opp_veg = str(int(veg) - 10000)
                else:
                    opp_veg = str(int(veg) + 10000)
                    
                if veg in orig_veg[grid]:
                    vegparam = " ".join(orig_veg[grid][veg][1])
                    veglai = " ".join(orig_veg[grid][veg][2])
                elif opp_veg in orig_veg[grid]:
                    vegparam = " ".join(orig_veg[grid][opp_veg][1])
                    veglai = " ".join(orig_veg[grid][opp_veg][2])
                else:
                    if veg in paramter_dic:
                        vegparam = paramter_dic[veg]
                    else:
                        vegparam = default_veg_parameter
                        
                    if veg in lai_dic:
                        veglai = lai_dic[veg]
                    else:
                        veglai = lai_default_missed
                    
                f.write("   " + veg + " " + str('%0.5f' % new_fraction[grid][veg]) + " " + vegparam + "\n")
                f.write("      " + veglai + "\n")

#print irrigation file
with open(outirrfile,"w") as f:
    for grid in sorted(new_fraction, key=sortkey, reverse=False):
        num_irrigated = 0
        for veg in sorted(new_fraction[grid], key=sortkey, reverse=False):
            if int(veg) < 10000 and int(veg) > 15:
                num_irrigated += 1
        if num_irrigated > 0:
            f.write(grid + " " + str(num_irrigated) + "\n")
        for veg in sorted(new_fraction[grid], key=sortkey, reverse=False):
            if int(veg) < 10000 and int(veg) > 15:
                if veg in crop_irrigation_type:
                    irrig = crop_irrigation_type[veg]
                else:
                    irrig = default_crop_irrigation_type
                    
                if grid in orig_irr:
                    if veg in orig_irr[grid]:
                        irrig = orig_irr[grid][veg]
                f.write("    " + veg + " " + irrig + "\n")


print('Done.\n')

    
    
        