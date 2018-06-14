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

#User output
#outdir = "/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Scenarios/BPA_Umatilla/VIC_output"
start_year = 1986
outdir = "/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Scenario/Testruns/Output"
#loc_name = "45.84375_-119.09375"
#loc_name = "45.78125_-118.46875"
#loc_name = "45.71875_-119.59375"
#loc_name = "45.96875_-119.15625"
loc_name = "45.84375_-119.34375"

target_var_list = ['Yield_kg_m2','irrig_netdemand_mm','irrig_total_mm','irrig_evap_mm','irrig_runoff_mm','water_stress_index','Runoff','Baseflow','Soil_E_mm','Crop_Canopy_E_mm','Act_Transp_mm','ET_mm','VIC_PET_shortgrass_mm','CropSyst_Pot_Transp_mm','PPT']
key_list = ['Year','CroppingSyst_code','Crop_code']
key_list_crop = ['Year','Crop_code']
key_list_annual = ['Year','CroppingSyst_code']
key_list_annual_crop = ['Year']


all_var_list = key_list + target_var_list
os.chdir(outdir)

for clm in clm_list:
    print(clm)
    for rot in rot_list:
        print("    " + rot)
        #vic_crop_outputs = "crop4001_cp_45.84375_-119.09375.asc"
        #vic_crop_outputs = "crop_Livneh_norotation_45.84375_-119.09375.asc"
        vic_crop_outputs = "crop_" + clm + "_" + rot + "_" + loc_name + ".asc"
        output_annual_mean = "annual_mean_" + clm + "_" + rot + loc_name + ".asc" 
        output_season_mean = "growseason_mean_" + clm + "_" + rot + loc_name + ".asc" 
        output_annual_mean_allrot = "annual_mean_" + clm + "_" + rot + loc_name + "_all_rot.asc" 
        output_season_mean_allrot = "growseason_mean_" + clm + "_" + rot + loc_name + "_all_rot.asc" 

        vic_crop = pd.read_csv(vic_crop_outputs,sep=',',index_col=False)
        #print(key_list)
        temp = vic_crop[all_var_list]
        temp = temp.loc[temp['Year'] >= start_year]
        vic_select = temp.loc[ ( temp['Crop_code'] != 0 ) & ( temp['Year'] >= start_year) ]
        #vic_select = temp.loc[temp['Year'] >= start_year]
        #vic_select = vic_select.drop('Crop_code', 1)

        vic_growth_season = vic_select.groupby(key_list,as_index=False)[all_var_list].sum()
        vic_growth_season_allrot = vic_growth_season.groupby(key_list_crop,as_index=False)[all_var_list].mean()
        #vic_growth_season = vic_growth_season.drop('Crop_code', 1)
        vic_growth_season.to_csv(output_season_mean, index=False)
        vic_growth_season_allrot.to_csv(output_season_mean_allrot, index=False)

        vic_annual = temp.groupby(key_list_annual,as_index=False)[all_var_list].sum()
        vic_annual_allrot = vic_annual.groupby(key_list_annual_crop,as_index=False)[all_var_list].mean()
        #vic_annual = vic_annual.drop('Crop_code', 1)
        vic_annual.to_csv(output_annual_mean, index=False)
        vic_annual_allrot.to_csv(output_annual_mean_allrot, index=False)