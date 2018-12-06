#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sum VIC-CropSyst crop daily outputs to annuam mean.

@author: liuming
"""

import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import os

#clm_list = ['Livneh','Abatzoglou']
clm_list = ['Livneh']
#rot_list = ['norotation','rotation']
rot_list = ['norotation']

#irrigation = "noirrig_"
irrigation = ""

start_year = 1915

#User output
#outdir = "/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Scenarios/BPA_Umatilla/VIC_output"
#outdir = "/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Scenario/Testruns/Output_180617_crops18"
outdir = "/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Scenario/Testruns/Output"
#outdir = "/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Scenario/Testruns/Output_local_180617_Alfalfa"

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
                 "45.53125_-119.65625",
                 
                 "46.15625_-119.09375",
                 "45.84375_-119.03125"]
"""


loc_name_list = ["45.09375_-120.21875"]


loc_crop_dic = {"45.84375_-119.09375" : "Potato", 
                "45.78125_-118.46875" : "WinWheat", 
                "45.71875_-119.59375" : "SprWheat", 
                "45.96875_-119.15625" : "Corn", 
                "45.84375_-119.34375" : "Alfafa", 
                "46.03125_-119.28125" : "SweetCorn",
                "45.78125_-118.59375" : "Peas",
                "45.78125_-119.84375" : "Onion",
                "45.78125_-119.40625" : "Canola",
                "45.90625_-119.71875" : "Carrots",
                "45.71875_-119.28125" : "DryBeans",
                "45.28125_-119.78125" : "Barley",
                "46.21875_-118.84375" : "Apple",
                "45.71875_-119.34375" : "GrassSeed",
                "45.78125_-119.21875" : "Mint",
                "45.78125_-119.53125" : "Cherry",
                "45.78125_-119.28125" : "GENERIC_Hay",
                "45.53125_-119.65625" : "Camelina",
                
                "46.15625_-119.09375" : "MixedCrops",
                "46.15625_-119.09375" : "MixedCrops",
                "45.09375_-120.21875" : "MixedCrops"}

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

avg_annual_all = pd.DataFrame()
avg_month_all = pd.DataFrame()


print("Irrigation:" + irrigation)

avg_annual_out = irrigation + "all_annual_avg.txt"
avg_month_out = irrigation + "all_month_avg.txt"

print(len(loc_name_list))

for loc_name in loc_name_list:
    #multiyear_rotation = True
    #if loc_name == "45.84375_-119.34375" or loc_name == "45.78125_-119.21875":
    if loc_name == "XXXX":
        multiyear_rotation = True
    else:
        multiyear_rotation = False

    target_var_list = ['Yield_kg_m2','irrig_netdemand_mm','irrig_total_mm','irrig_evap_mm','irrig_runoff_mm','water_stress_index','Runoff','Baseflow','Soil_E_mm','Crop_Canopy_E_mm','Act_Transp_mm','ET_mm','VIC_PET_shortgrass_mm','CropSyst_Pot_Transp_mm','PPT']
    #key_list = ['Year','CroppingSyst_code','Crop_code']
    key_list = ['cell_id','Year','Month','CroppingSyst_code']
    key_list_month = ['cell_id','Year','Month','CroppingSyst_code']
    key_list_grseason = ['cell_id','Year','CroppingSyst_code']
    #key_list_crop = ['Year','Crop_code']
    key_list_annual = ['cell_id','Year','CroppingSyst_code']
    key_list_annual_crop = ['cell_id','Year']
    key_crop = ['cell_id','CroppingSyst_code']
    key_month_crop = ['cell_id','Month','CroppingSyst_code']


    all_var_list = key_list + target_var_list
    os.chdir(outdir)

    for clm in clm_list:
        print(clm)
        for rot in rot_list:
            print("    " + rot)
            #vic_crop_outputs = "crop4001_cp_45.84375_-119.09375.asc"
            #vic_crop_outputs = "crop_Livneh_norotation_45.84375_-119.09375.asc"
            outrot="_"
            cropname = loc_crop_dic[loc_name]
            vic_crop_outputs = irrigation + "crop_" + clm + "_" + rot + "_" + loc_name + ".asc"
            print(vic_crop_outputs)
            
            output_annual_mean = irrigation + "Total_annual_" + clm + "_" + outrot + "_" + cropname + "_" + loc_name + ".asc" 
            output_season_mean = irrigation + "Total_growseason_" + clm + "_" + outrot + "_" + cropname + "_" + loc_name + ".asc" 
            #output_month_mean = irrigation + "Total_month_" + clm + "_" + outrot + "_" + cropname + "_" + loc_name + ".asc" 
            avgoutput_annual_mean = irrigation + "avg_Total_annual_" + clm + "_" + outrot + "_" + cropname + "_" + loc_name + ".asc" 
            avgoutput_season_mean = irrigation + "avg_Total_growseason_" + clm + "_" + outrot + "_" + cropname + "_" + loc_name + ".asc" 
            #avgoutput_month_mean = irrigation + "avg_Total_monnth_" + clm + "_" + outrot + "_" + cropname + "_" + loc_name + ".asc" 

            
            if multiyear_rotation:
                output_annual_mean_allrot = "annual_mean_" + clm + "_" + outrot + "_" + cropname + "_" + loc_name + "_all_rot.asc" 
                output_season_mean_allrot = "growseason_mean_" + clm + "_" + outrot + "_" + cropname + "_" + loc_name + "_all_rot.asc" 

            vic_crop = pd.read_csv(vic_crop_outputs,sep=',',index_col=False)
            #print(key_list)
            temp = vic_crop[all_var_list + ['Crop_code'] + ['Grow_Stage']]
            temp = temp.loc[temp['Year'] >= start_year]                                                                         #all revords after start_year
            vic_select = temp[ ( temp['Crop_code'] != 0 ) & (temp['Grow_Stage'].str.contains('Dormant') == False) & ( temp['Year'] >= start_year) ]                                 #growing season for annual crops
            
            #vic_select = temp.loc[temp['Year'] >= start_year]
            vic_select = vic_select.drop('Crop_code', 1)
            vic_select = vic_select.drop('Grow_Stage', 1)
            #vic_select = temp
            #vic_month = vic_select.groupby(key_list_month,as_index=False)[all_var_list].sum()
            #vic_month_out = vic_month  #vic_month.drop('Crop_code', 1)
            #vic_month_out.to_csv(output_month_mean, index=False)
     
    
            vic_growth_season = vic_select.groupby(key_list_grseason,as_index=False)[all_var_list].sum()
            #if multiyear_rotation:
            #    vic_growth_season_allrot = vic_growth_season.groupby(key_list_crop,as_index=False)[all_var_list].mean()
            #    vic_growth_season_allrot = vic_growth_season_allrot.drop('Crop_code', 1)
            #    vic_growth_season_allrot.to_csv(output_season_mean_allrot, index=False)
                #vic_growth_season = vic_growth_season.drop('Crop_code', 1)
            #else:
            
            vic_growth_season_out = vic_growth_season.drop("Month", 1)
            vic_growth_season_out.to_csv(output_season_mean, index=False)
                
            
            vic_annual = temp.groupby(key_list_annual,as_index=False)[all_var_list].sum()
            #if multiyear_rotation:
            #    vic_annual_allrot = vic_annual.groupby(key_list_annual_crop,as_index=False)[all_var_list].mean()
            #    vic_annual = vic_annual.drop('Crop_code', 1)
            #    vic_annual_allrot.to_csv(output_annual_mean_allrot, index=False)
            #else:
            vic_annual_out = vic_annual.drop("Month", 1)
            vic_annual_out.to_csv(output_annual_mean, index=False)
                
                
            #avg_month = vic_month.groupby(key_month_crop,as_index=False)[all_var_list].mean()
            #avg_month = avg_month.drop("Year", 1)
            #avg_month = avg_month.drop("Crop_code", 1)
            #avg_month['CROP'] = cropname
            #avg_month.to_csv(avgoutput_month_mean, index=False)
            
            avg_season = vic_growth_season.groupby(key_crop,as_index=False)[all_var_list].mean()
            avg_season = avg_season.drop("Year", 1)
            #avg_season = avg_season.drop("Crop_code", 1)
            avg_season.to_csv(avgoutput_season_mean, index=False)
            
            avg_year = vic_annual.groupby(key_crop,as_index=False)[all_var_list].mean()
            avg_year = avg_year.drop("Year", 1)
            #avg_year = avg_year.drop("Crop_code", 1)
            avg_year['CROP'] = cropname
            avg_year.to_csv(avgoutput_annual_mean, index=False)
            if avg_annual_all.empty:
                avg_annual_all = avg_year
            else:
                avg_annual_all = avg_annual_all.append(avg_year, ignore_index=True)
                
            #if avg_month_all.empty:
            #    avg_month_all = avg_month
            #else:
            #    avg_month_all = avg_month_all.append(avg_month, ignore_index=True)

            
#avg_month_all.to_csv(avg_month_out, index=False, float_format='%.3f')
avg_annual_all.to_csv(avg_annual_out, index=False, float_format='%.3f')
print("Done!")