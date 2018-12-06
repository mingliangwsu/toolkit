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
outdir = "/fastscratch/liuming/BPA_180616_nofrozensoil"
cellid_file = "/data/hydro/users/liumingdata/Projects/WSU_BPA/VIC-CropSyst/Simulation/Scenario/Aeolus_BPA_runs/cellloc_id_list.txt"

os.chdir(outdir)
generateout_dir = outdir

loc_name_list = []
loc_id_dic = {}
with open(cellid_file) as f:
    for line in f:
        records = line.split(" ")
        if len(records[0]):
            loc_name_list.append(records[0])
            loc_id_dic.update({records[0] : records[1]})
print("cell id list reading is finished.\n")
        


"""
loc_name_list = ["45.03125_-118.96875",
                 "45.09375_-119.03125"]
"""
                 
#irrigation_list = ["TRUE", "FALSE"]
irrigation_list = ["TRUE"]

"""
loc_id_dic = {"45.03125_-118.96875" : 297057,
              "45.09375_-119.03125" : 297984}
"""


print(len(loc_name_list))

for irrigation in irrigation_list:
    print("Irrigation:" + irrigation)
    avg_annual_all = pd.DataFrame()
    avg_month_all = pd.DataFrame()

    avg_annual_file_out = generateout_dir + "/" + "allgridcell_annual_irr_" + irrigation + ".txt"
    avg_month_file_out = generateout_dir + "/" + "allgridcell_month_irr_" + irrigation + ".txt"
    for loc_name in loc_name_list:
        #preprocess the output file
        vic_outputs = "vic_irr_" + irrigation + "_sd__" + loc_name
        print(loc_name)
        reformatted_vicout = open("tempvic.txt","w")
        
        target_var_list = ['OUT_PREC', 'OUT_AIR_TEMP', 'OUT_SNOWF', 'OUT_EVAP', 'OUT_RUNOFF', 'OUT_BASEFLOW', 'OUT_SWE', 'OUT_EVAP_BARE', 'OUT_EVAP_CANOP', 'OUT_TRANSP_VEG', 'OUT_CROP_IRRI_WAT', 'OUT_EVAP_FROM_IRRIG', 'OUT_RUNOFF_IRRIG', 'OUT_ET_POT_SHORT']
        key_list = ['cell_id','YEAR','MONTH']
        key_list_month = ['cell_id','YEAR','MONTH']
        key_list_annual = ['cell_id','YEAR']
        key_month = ['cell_id','MONTH']
        key_year = ['cell_id']
        all_var_list = key_list + target_var_list

        with open(vic_outputs) as f:
            for line in f:
                if "#" not in line:
                    value = line.split()
                    newline = ""
                    if len(value[0]) > 0:
                        OUT_SWE = 0
                        OUT_EVAP_BARE = 0
                        OUT_EVAP_CANOP = 0
                        OUT_TRANSP_VEG = 0
                        OUT_CROP_IRRI_WAT = 0
                        OUT_EVAP_FROM_IRRIG = 0
                        OUT_RUNOFF_IRRIG = 0
                        OUT_ET_POT_SHORT = 0
                        
                        for index in range(9):
                            newline = newline + " " + value[index]
                        index_i = 0
                        for var in varlist:
                            if "OUT_SWE" in var:
                               OUT_SWE = OUT_SWE + float(value[index_i])
                            if "OUT_EVAP_BARE" in var:
                               OUT_EVAP_BARE = OUT_EVAP_BARE + float(value[index_i])
                            if "OUT_EVAP_CANOP" in var:
                               OUT_EVAP_CANOP = OUT_EVAP_CANOP + float(value[index_i])
                            if "OUT_TRANSP_VEG" in var:
                               OUT_TRANSP_VEG = OUT_TRANSP_VEG + float(value[index_i])
                            if "OUT_CROP_IRRI_WAT" in var:
                               OUT_CROP_IRRI_WAT = OUT_CROP_IRRI_WAT + float(value[index_i])
                            if "OUT_EVAP_FROM_IRRIG" in var:
                               OUT_EVAP_FROM_IRRIG = OUT_EVAP_FROM_IRRIG + float(value[index_i])
                            if "OUT_RUNOFF_IRRIG" in var:
                               OUT_RUNOFF_IRRIG = OUT_RUNOFF_IRRIG + float(value[index_i])
                            if "OUT_ET_POT_SHORT" in var:
                               OUT_ET_POT_SHORT = OUT_ET_POT_SHORT + float(value[index_i])
                            index_i = index_i + 1
                        newline = newline + " " + str('%.2f' % OUT_SWE) + " " + str('%.2f' % OUT_EVAP_BARE) + " " + str('%.2f' % OUT_EVAP_CANOP) + " " + str('%.2f' % OUT_TRANSP_VEG)
                        newline = newline + " " + str('%.2f' % OUT_CROP_IRRI_WAT) + " " + str('%.2f' % OUT_EVAP_FROM_IRRIG) + " " + str('%.2f' % OUT_RUNOFF_IRRIG) + " " + str('%.2f' % OUT_ET_POT_SHORT) + "\n"        
                        reformatted_vicout.write(newline)
                if "YEAR" in line:
                    newline = line[2:]
                    varlist = newline.split()
                    newline = "YEAR MONTH DAY"
                    for var in target_var_list:
                        newline = newline + " " + var
                    reformatted_vicout.write(newline + "\n")
        reformatted_vicout.close()
        
        #load new vic output
        all_var_list = key_list + target_var_list
  
        gridid = loc_id_dic[loc_name]
        output_annual_mean = generateout_dir + "Total_annual_" + irrigation + "_" + loc_name + ".asc" 
        output_month_mean = generateout_dir + "Total_month_" + irrigation + "_" + loc_name + ".asc" 
        avgoutput_annual_mean = generateout_dir + "avg_Total_annual_" + irrigation + "_" + loc_name + ".asc" 
        avgoutput_month_mean = generateout_dir + "avg_Total_monnth_" + irrigation + "_" + loc_name + ".asc" 
            

        vic_crop = pd.read_csv("tempvic.txt",sep = "\s+|\t+|\s+\t+|\t+\s+",index_col=False, engine='python')
            #print(key_list)
        vic_crop['cell_id'] = int(gridid)
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

    avg_annual_all.to_csv(avg_annual_file_out, index=False, float_format='%.3f')
    avg_month_all.to_csv(avg_month_file_out, index=False, float_format='%.3f')

print("Done!")
