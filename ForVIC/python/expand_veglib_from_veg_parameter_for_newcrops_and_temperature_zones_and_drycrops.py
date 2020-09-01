#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jun. 23, 2020
Add missing veg lib for crops (keep all original crops in veg lib)

@author: liuming
"""

# this block of code copied from https://gist.github.com/ryan-hill/f90b1c68f60d12baea81 
import pandas as pd
import pysal as ps
import numpy as np

def sortkey(x): 
    return int(x)

datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Library/"
#veg_file = datapath + "pnw_veg_parameter_filledzero.txt"
veglib_file = datapath + "veglib_20200506_ext_Forecast2020.txt"
#outlist_file = datapath + "allveglist.txt"
outveglib_file = datapath + "veglib_20200506_ext_Forecast2020_final.txt"

fout_veglib = open(outveglib_file,"w")

veglib = dict()   #[veg_code] list of parameters

new_crops = {  #new crops need various planting dates
    "2401" : "Barley_spring_colder",
    "2402" : "Barley_spring_medium",
    "2403" : "Barley_spring_warmer",
    "2404" : "Canola_colder",
    "2405" : "Canola_warmer",
    "2406" : "Corn_grain_colder",
    "2407" : "Corn_grain_medium",
    "2408" : "Corn_grain_warmer",
    "2409" : "Dry_beans_colder",
    "2410" : "Dry_beans_warmer",
    "2411" : "Hops_colder",
    "2412" : "Hops_warmer",
    "2413" : "Lentils_colder",
    "2414" : "Lentils_warmer",
    "2415" : "Oats_colder",
    "2416" : "Oats_warmer",
    "2417" : "Onion_bulb_colder",
    "2418" : "Onion_bulb_warmer",
    "2419" : "Potato_colder",
    "2420" : "Potato_warmer",
    "2421" : "Sod_seed_grass_colder",
    "2422" : "Sod_seed_grass_warmer",
    "2423" : "Spring_wheat_colder",
    "2424" : "Spring_wheat_warmer",
    "2425" : "Triticale_spring_colder",
    "2426" : "Triticale_spring_warmer",
    "2427" : "Winter_wheat_colder",
    "2428" : "Winter_wheat_warmer",
    
    "701" : "Alfalfa_Hay",
    "708" : "CloverHay",
    "713" : "GrassHay",
    "807" : "Mint",
    "1814" : "Corn_Sweet",
    "1824" : "Pea_Dry",
    "1839" : "Radish"
}

"""
ocnsb = { #other_crops_need_state_boundary
    "701" : "Alfalfa_Hay",
    "708" : "CloverHay",
    "713" : "GrassHay",
    "807" : "Mint",
    "1814" : "Corn_Sweet",
    "1824" : "Pea_Dry",
    "1839" : "Radish"
}
"""

state_zones = {
    "WA" : "1",
    "OR" : "2",
    "ID" : "3",
    "MT" : "4",
    "NE" : "5",
    "UT" : "6",
    "WY" : "7",
    "CAN" : "8"
}

#veglib file
with open(veglib_file) as f:
    for line in f:
        a = line.rstrip().split('\t')
        if "COMMENT" not in a:
            if a[0] not in veglib:
                veglib[a[0]] = a
        else:
            fout_veglib.write(line)
            
#add single rotation types for newcrops
start_code = 9401   #9401-9999 can be used the veg library
newrotation = start_code
for crop in new_crops:
    for state in state_zones:
        irr_rotation = str(newrotation)
        nonirr_rotation = str(10000 + int(irr_rotation))
        rot_name = state + "_" + new_crops[crop] + "_single_crop"
        nonirr_rot_name = "Nonirr_" + rot_name
        print(irr_rotation + " : " + crop + " : " + state + " : " + new_crops[crop])
        #irrigated rotation
        if irr_rotation not in veglib:
            veglib[irr_rotation] = veglib[crop].copy()
            veglib[irr_rotation][0] = irr_rotation
            veglib[irr_rotation][-1] = rot_name
        #nonirrigated rotation
        if nonirr_rotation not in veglib:
            veglib[nonirr_rotation] = veglib[crop].copy()
            veglib[nonirr_rotation][0] = nonirr_rotation
            veglib[nonirr_rotation][-1] = nonirr_rot_name
            
        newrotation += 1
            
#write new library file
for crop in sorted(veglib,key=sortkey, reverse=False):
        index = 0
        for col in veglib[crop]:
            if index > 0:
                fout_veglib.write('\t')
            fout_veglib.write(col)
            index += 1
        fout_veglib.write('\n')

fout_veglib.close()
print('Done.\n')

    
    
        