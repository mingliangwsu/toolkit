#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sum VIC-CropSyst crop daily outputs to monthly mean.

@author: liuming
"""

import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import os

clm_list = ['Livneh','Abatzoglou']
#clm_list = ['Livneh']
rot_list = ['norotation','rotation']
#rot_list = ['norotation']

#User output
outdir = "/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Scenarios/BPA_Umatilla/VIC_output"

#target_var_list = ['Yield_kg_m2','irrig_netdemand_mm','irrig_total_mm','irrig_evap_mm','irrig_runoff_mm','water_stress_index','Runoff','Baseflow','Soil_E_mm','Crop_Canopy_E_mm','Act_Transp_mm','ET_mm','VIC_PET_shortgrass_mm','CropSyst_Pot_Transp_mm','PPT']
target_var_list_sum = ['PPT','irrig_total_mm','irrig_runoff_mm', 'Runoff','Baseflow','Soil_E_mm','Act_Transp_mm','ET_mm','CropSyst_Pot_Transp_mm','VIC_PET_shortgrass_mm']
target_var_list_mean = ['Tair_avg','Tmax','Tmin','SWRAD_w_m2','VP_kPa','water_stress_index']


#key_list = ['Year','CroppingSyst_code','Crop_code']
#key_list_annual = ['Year','CroppingSyst_code']
key_list = ['Month']
Year = ['Year']


all_var_list = key_list + target_var_list_sum + target_var_list_mean
all_var_list_mon = all_var_list + Year

os.chdir(outdir)

start_year = 1986
end_year = 2015
years = end_year - start_year + 1

for clm in clm_list:
    print(clm)
    for rot in rot_list:
        print("    " + rot)
        #vic_crop_outputs = "crop4001_cp_45.84375_-119.09375.asc"
        #vic_crop_outputs = "crop_Livneh_norotation_45.84375_-119.09375.asc"
        vic_crop_outputs = "crop_" + clm + "_" + rot + "_45.84375_-119.09375.asc"
        #output_annual_mean = "annual_mean_" + clm + "_" + rot + ".asc" 
        #output_season_mean = "growseason_mean_" + clm + "_" + rot + ".asc" 
        output_monthly_mean = "monthly_mean_" + clm + "_" + rot + ".asc" 

        vic_crop = pd.read_csv(vic_crop_outputs,sep=',',index_col=False)
        #print(key_list)
        temp = vic_crop[all_var_list_mon]
        vic_select = temp.loc[temp['Year'] >= start_year]
        vic_select = vic_select.drop('Year', 1)

        #vic_growth_season = vic_select.groupby(key_list,as_index=False)[all_var_list].sum()
        #vic_growth_season = vic_growth_season.drop('Crop_code', 1)
        #vic_growth_season.to_csv(output_season_mean, index=False)

        #vic_annual = temp.groupby(key_list_annual,as_index=False)[all_var_list].sum()
        #vic_annual = vic_annual.drop('Crop_code', 1)
        #vic_annual.to_csv(output_annual_mean, index=False)
        
        #vic_month_mean = temp.groupby(key_list,as_index=False)[all_var_list].mean()
        vic_month_mean = temp.groupby(key_list,as_index=False)[target_var_list_mean].mean()
        vic_month_sum = temp.groupby(key_list,as_index=False)[target_var_list_sum].sum()
        
        for var in target_var_list_sum:
            vic_month_sum[var] = vic_month_sum[var] / years
        
            
        tt = pd.concat([vic_month_sum,vic_month_mean], axis=1)
        tt = tt.T.drop_duplicates().T
        tt.Month = tt.Month.astype(int)
        
        tt.to_csv(output_monthly_mean, index=False)