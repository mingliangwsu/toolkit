#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sum VIC-CropSyst VIC outputs.

@author: liuming
"""

import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import sys 
import os

start_year = 1928
outdir = "/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Scenario/Testruns/Output"
os.chdir(outdir)

generateout_dir = "/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Scenario/Testruns/stats"

"""
loc_name_list = ["45.84375_-119.09375", 
                 "45.78125_-118.46875", 
                 "45.71875_-119.59375", 
                 "45.96875_-119.15625", 
                 "45.84375_-119.34375", 
                 "46.03125_-119.28125",
                 "45.78125_-118.59375",
                 "45.78125_-119.84375",
                 "45.78125_-119.40625",
                 "45.90625_-119.71875",
                 "45.71875_-119.28125",
                 "45.28125_-119.78125",
                 "46.21875_-118.84375",
                 "45.71875_-119.34375",
                 "45.78125_-119.21875",
                 "45.78125_-119.53125",
                 "45.78125_-119.28125",
                 "45.53125_-119.65625"]
"""

loc_name_list = ["45.03125_-118.96875",
                 "45.09375_-119.03125"]
irrigation_list = ["TRUE", "FALSE"]
irrigation_list = ["TRUE"]


loc_id_dic = {"45.03125_-118.96875" : 297057,
              "45.09375_-119.03125" : 297984}

#loc_name = "45.84375_-119.09375"
#loc_name = "45.78125_-118.46875"
#loc_name = "45.71875_-119.59375"
#loc_name = "45.96875_-119.15625"
#loc_name = "45.84375_-119.34375"    #Alfalfa          (5701): 309115 45.84375 -119.34375
#loc_name = "46.03125_-119.28125"
#loc_name = "45.78125_-118.59375"
#loc_name = "45.78125_-119.84375"
#loc_name = "45.78125_-119.40625"
#loc_name = "45.90625_-119.71875"
#loc_name = "45.71875_-119.28125"
#loc_name = "46.21875_-118.84375"    #Apple

print(len(loc_name_list))

avg_annual_all = pd.DataFrame()
avg_month_all = pd.DataFrame()

avg_annual_file_out = "allgridcell_annual.txt"
avg_month_file_out = "allgridcell_month.txt"

for irrigation in irrigation_list:
    print("Irrigation:" + irrigation)
    avg_annual_all = pd.DataFrame()
    avg_month_all = pd.DataFrame()

    avg_annual_file_out = "allgridcell_annual_irr_" + irrigation + ".txt"
    avg_month_file_out = "allgridcell_month_irr_" + irrigation + ".txt"
    for loc_name in loc_name_list:
        #preprocess the output file
        vic_outputs = "vic_irr_" + irrigation + "_sd__" + loc_name
        print(loc_name)
        reformatted_vicout = open("tempvic.txt","w")
        with open(vic_outputs) as f:
            for line in f:
                if "#" not in line:
                    reformatted_vicout.write(line)
                if "YEAR" in line:
                    newline = line[2:]
                    reformatted_vicout.write(newline)
        reformatted_vicout.close()
        
        #load new vic output
        target_var_list = ['OUT_PREC', 'OUT_AIR_TEMP', 'OUT_SNOWF', 'OUT_EVAP', 'OUT_RUNOFF', 'OUT_BASEFLOW', 'OUT_SWE', 'OUT_EVAP_BARE', 'OUT_EVAP_CANOP', 'OUT_TRANSP_VEG', 'OUT_CROP_IRRI_WAT', 'OUT_EVAP_FROM_IRRIG', 'OUT_RUNOFF_IRRIG', 'OUT_ET_POT_SHORT']
        key_list = ['cell_id','YEAR','MONTH']
        key_list_month = ['cell_id','YEAR','MONTH']
        key_list_annual = ['cell_id','YEAR']
        key_month = ['cell_id','MONTH']
        key_year = ['cell_id']
        
        
        all_var_list = key_list + target_var_list
  
        gridid = loc_id_dic[loc_name]
        output_annual_mean = generateout_dir + "Total_annual_" + irrigation + "_" + loc_name + ".asc" 
        output_month_mean = generateout_dir + "Total_month_" + irrigation + "_" + loc_name + ".asc" 
        avgoutput_annual_mean = generateout_dir + "avg_Total_annual_" + irrigation + "_" + loc_name + ".asc" 
        avgoutput_month_mean = generateout_dir + "avg_Total_monnth_" + irrigation + "_" + loc_name + ".asc" 
            

        vic_crop = pd.read_csv("tempvic.txt",sep = "\s+|\t+|\s+\t+|\t+\s+",index_col=False, engine='python')
            #print(key_list)
        vic_crop['cell_id'] = gridid
        temp = vic_crop[all_var_list]
        temp = temp.loc[temp['YEAR'] >= start_year]                                                                         #all revords after start_year
        vic_select = temp
        vic_month = vic_select.groupby(key_list_month,as_index=False)[all_var_list].sum()
        #vic_month_out = vic_month.drop("OUT_AIR_TEMP", 1)
        #vic_month_out.to_csv(output_month_mean, index=False)
        
        vic_annual = temp.groupby(key_list_annual,as_index=False)[all_var_list].sum()
        #vic_annual_out = vic_annual.drop("OUT_AIR_TEMP", 1)
        #vic_annual_out = vic_annual.drop("MONTH", 1)
        #vic_annual_out.to_csv(output_annual_mean, index=False)
                
        avg_month = vic_month.groupby(key_month,as_index=False)[all_var_list].mean()
        avg_year = vic_annual.groupby(key_year,as_index=False)[all_var_list].mean()
        
        #avg_year = avg_year.drop("YEAR", 1)
        #avg_year.to_csv(avgoutput_annual_mean, index=False)
        if avg_annual_all.empty:
            avg_annual_all = avg_year
        else:
            avg_annual_all = avg_annual_all.append(avg_year, ignore_index=True)
                    
        if avg_month_all.empty:
            avg_month_all = avg_month
        else:
            avg_month_all = avg_month_all.append(avg_month, ignore_index=True)

    avg_annual_all.to_csv(avg_annual_file_out, index=False)
    avg_month_all.to_csv(avg_month_file_out, index=False)

print("Done!")
