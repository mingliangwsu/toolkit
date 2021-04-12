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

def find_plant_dic_key(plantdic,crop_name_with_zone):
    for crop in plantdic:
        #print("crop:" + crop + " in " + crop_name_with_zone + "?")
        if crop in crop_name_with_zone:
            #print("crop:" + crop + " in " + crop_name_with_zone)
            return crop
    return "NA"

#datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Library/"
#veg_file = datapath + "pnw_veg_parameter_filledzero.txt"
#veglib_file = datapath + "veglib_20200506_ext_Forecast2020.txt"
#outlist_file = datapath + "allveglist.txt"
#outveglib_file = datapath + "veglib_20200506_ext_Forecast2020_final.txt"
#fout_veglib = open(outveglib_file,"w")

rotation_path = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Rotation/"
crop_parameter_path = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Crop/Name/"
management_path = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Management/Name/"
out_rotation_file_path = rotation_path + "Name/"
rotation_mode = rotation_path + "mode.CS_rotation"
rotation_crop_state_info = rotation_path + "new_rotation_crop_state_name_list.txt"
planting_date = rotation_path + "planting_dates.txt"

veglib = dict()   #[veg_code] list of parameters

management_file_dict = {
    "2411" : "AutoIrrigHarvest_hops",       #"Hops_colder",
    "2412" : "AutoIrrigHarvest_hops",       #"Hops_warmer",
    "2417" : "AutoIrrigHarvest_onions",     #"Onion_bulb_colder",
    "2418" : "AutoIrrigHarvest_onions",     #"Onion_bulb_warmer",
    "2421" : "AutoIrrigHarvest_Grass",      #"Sod_seed_grass_colder",
    "2422" : "AutoIrrigHarvest_Grass",      #"Sod_seed_grass_warmer",
    "701"  : "AutoIrrigHarvest_Alfalfa",     #"Alfalfa_Hay",
    "708"  : "AutoIrrigHarvest_Clover",      #"CloverHay",
    "713"  : "AutoIrrigHarvest_Grass",       #"GrassHay",
    "807"  : "AutoIrrigHarvest_mint",        #"Mint",
    "1814" : "AutoIrrigHarvest_sweet_corn", #"Corn_Sweet",
}
default_management = "AutoIrrigHarvest_annual"

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
    
    "701"  : "Alfalfa_Hay",
    "708"  : "CloverHay",
    "713"  : "GrassHay",
    "807"  : "Mint",
    "1814" : "Corn_Sweet",
    "1824" : "Pea_Dry",
    "1839" : "Radish"
}

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

#planting date
#Planting_Date,WA,OR,ID,MT,NE,UT,WY,CAN
#Barley_spring,105,112,111,123,120,101,103,123
planting_date_dic = dict() #[rotation_broader_name][state]
with open(planting_date) as f:
    for line in f:
        a = line.rstrip().split(',')
        if len(a) > 0:
            if "Planting_Date" in a:
                phead = a.copy()
            else:
                if a[0] not in planting_date_dic:
                    planting_date_dic[a[0]] = dict()
                    for index,state in enumerate(phead):
                        if state != "Planting_Date":
                            if state not in planting_date_dic[a[0]]:
                                planting_date_dic[a[0]][state] = a[index]
print("reading planting date done!")            

with open(rotation_mode) as f:
    rot_mode = f.read()

#get new rotation list
with open(rotation_crop_state_info) as f:
    #9401,2401,WA,Barley_spring_colder
    for line in f:
        a = line.rstrip().split(',')
        if len(a) > 1:
            print(a[0])
            rotation_name = "CT_" + a[2] + "_" + a[3] + "_single_crop"
            rotation_name_filename = out_rotation_file_path + rotation_name + ".rot"
            pdate_key = find_plant_dic_key(planting_date_dic,a[3])
            pdate = "0" + planting_date_dic[pdate_key][a[2]]
            cropfilename = crop_parameter_path + a[3] + ".crp"
            if a[1] in management_file_dict:
                management = management_file_dict[a[1]]
            else:
                management = default_management
            management_filename = management_path + management + ".mgt"
            #replace information from mode
            outrot = str(rot_mode)
            outrot = outrot.replace("REPLACE_DESCRIPTION",rotation_name)
            outrot = outrot.replace("REPLACE_DATE",pdate)
            outrot = outrot.replace("REPLASE_CROP",cropfilename)
            outrot = outrot.replace("REPLASE_MANAGEMENT",management_filename)
            with open(rotation_name_filename,"w") as ofile:
                ofile.write(outrot)
        

"""           
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
"""
print('Done.\n')

    
    
        