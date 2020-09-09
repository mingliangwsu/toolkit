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



vic_grid_list_path = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/gis/"
#datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/irrigation/"
datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Veg/"
veg_file = datapath + "pnw_veg_parameter_filledzero.txt"
updated_veg_file = datapath + "pnw_veg_parameter_filledzero_state_reclassified.txt"

irrigation_path = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Management/"
irrigation_file = irrigation_path + "pnw_irrigation.txt"
updated_irrigation_file = irrigation_path + "pnw_irrigation_state_reclassified.txt"

state_zone_rotation_file_list = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Rotation/new_rotation_crop_state_name_list.txt"

#crop list to be reclassified
crop_to_reclassify = {
        "4004" : "Potato_colder",
        "4005" : "Winter_wheat_colder",
        "4006" : "Spring_wheat_colder",
        "4007" : "Corn_grain_colder",
        "4008" : "Corn_Sweet",
        "4010" : "Dry_beans_colder",
        "4011" : "Barley_spring_colder",
        "4100" : "Onion_bulb_colder", 
        "4101" : "Canola_colder",
        "7206" : "Oats_colder",
        "7701" : "Alfalfa_Hay",
        "7708" : "CloverHay",
        "7806" : "Hops_colder",
        "7807" : "Mint",
        "8205" : "GrassHay",
        "8704" : "Sod_seed_grass_colder",
        "8819" : "Lentils_colder",
        "8824" : "Pea_Dry",
        "8839" : "Radish",
        "9209" : "Triticale_spring_colder"
        }

state_list = ["wa", "can", "mt", "id", "ne", "ut", "wy", "or"]
#state_list = ["wy"]

#get vic cell list
large_vic_list = dict()
for state in state_list:
    large_vic_list[state] = list()
    #reading vic list from files
    viclistfile = vic_grid_list_path + "vic" + state + ".txt"
    with open(viclistfile) as f:
        for line in f:
            a = line.rstrip().split(',')
            if "FID" not in a:
                grid = a[-1]
                if grid not in large_vic_list[state]:
                    large_vic_list[state].append(grid)

oldcode_state_to_newcode = dict() #[old_cropcode][state]
newcropname_state_newcode = dict() #[cropname][state]

with open(state_zone_rotation_file_list) as f:
    for line in f:
        a = line.rstrip().split(',')
        if a[3] not in newcropname_state_newcode:
            newcropname_state_newcode[a[3]] = dict()
        state = a[2].lower()
        if state not in newcropname_state_newcode[a[3]]:
            newcropname_state_newcode[a[3]][state] = a[0]
for oldcropcode in crop_to_reclassify:
    if oldcropcode not in oldcode_state_to_newcode:
        oldcode_state_to_newcode[oldcropcode] = dict()
    for state in newcropname_state_newcode[crop_to_reclassify[oldcropcode]]:
        oldcode_state_to_newcode[oldcropcode][state] = newcropname_state_newcode[crop_to_reclassify[oldcropcode]][state]


#croplist = list()
def get_state(vicid):
    for state in state_list:
        if vicid in large_vic_list[state]:
            return state;
    return "or"

#vegetation parameter
with open(updated_veg_file,"w") as fout:
    with open(veg_file) as f:
        for line in f:
            a = line.rstrip().split()
            if len(a) == 2:
                state = get_state(a[0])
            if len(a) == 8:
                longcode = False
                cropcodeint = int(a[0])
                newcode = a[0]
                if cropcodeint > 10000:
                    cropcodeint -= 10000
                    longcode = True
                if str(cropcodeint) in oldcode_state_to_newcode:
                    newcode = oldcode_state_to_newcode[str(cropcodeint)][state]
                    if longcode:
                        newcode = str(int(newcode) + 10000)
                outline = "   " + newcode
                for index in range(1,8):
                    outline += " " + a[index]
                outline += "\n"
                fout.write(outline)
            else:
                fout.write(line)

#irrigation parameter
with open(updated_irrigation_file,"w") as fout:
    with open(irrigation_file) as f:
        for line in f:
            a = line.rstrip().split()
            if a[1].isdigit():
                state = get_state(a[0])
                fout.write(line)
            else:
                oldcode = a[0]
                if oldcode in oldcode_state_to_newcode:
                    newcode = oldcode_state_to_newcode[oldcode][state]
                    outline = "    " + newcode + " " + a[1] + "\n"
                    fout.write(outline)
                else:
                    fout.write(line)


#            if a[0] not in croplist:
#                croplist.append(a[0])
#fout = open(outlist_file,"w")
#croplist.sort(key = int)
#for crop in croplist:
#    fout.write(crop + "\n")

#fout.close()
print('Done.\n')

    
    
        