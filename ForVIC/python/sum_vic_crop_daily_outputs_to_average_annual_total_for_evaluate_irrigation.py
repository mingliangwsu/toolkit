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
#clm_list = ['Livneh']
#rot_list = ['norotation','rotation']
#rot_list = ['norotation']

irri_list = ['DEFAULT_CENTER_PIVOT','DEFAULT_BIG_GUN','DEFAULT_SOLID_SET','DEFAULT_MOVING_WHEEL','DEFAULT_DRIP','DEFAULT_FLOOD','DEFAULT_RILL','DEFAULT_FURROW','IrrigTP_CP_impact_14VH_RainBird','IrrigTP_CP_impact_M20VH_PM_RainBird','IrrigTP_CP_impact_65PJ_RainBird','IrrigTP_CP_impact_30FH_30FWH_RainBird','IrrigTP_CP_impact_L36H_L36AH_RainBird_1','IrrigTP_CP_impact_L36H_L36AH_RainBird_2','IrrigTP_CP_impact_85EHD_RainBird_1','IrrigTP_CP_impact_85EHD_RainBird_2','IrrigTP_CP_impact_85EHD_RainBird_3','IrrigTP_CP_impact_85EHD_LA_RainBird_1','IrrigTP_CP_impact_85EHD_LA_RainBird_2','IrrigTP_CP_impact_85EHD_LA_RainBird_3','IrrigTP_CP_spray_S3000_Nelson','IrrigTP_CP_spray_O3000_Nelson','IrrigTP_CP_spray_R3000_Nelson_1','IrrigTP_CP_spray_R3000_Nelson_2','IrrigTP_CP_spray_A3000_Nelson_1','IrrigTP_CP_spray_A3000_Nelson_2','IrrigTP_Big_Gun_75TR_Nelson_1','IrrigTP_Big_Gun_75TR_Nelson_2','IrrigTP_Big_Gun_75TR_Nelson_3','IrrigTP_Big_Gun_150TB_Nelson_1','IrrigTP_Big_Gun_150TB_Nelson_2','IrrigTP_Big_Gun_150TB_Nelson_3','IrrigTP_Big_Gun_200TB_Nelson_1','IrrigTP_Big_Gun_200TB_Nelson_2','IrrigTP_Big_Gun_200TB_Nelson_3','IrrigTP_Solid_set_R5_POP_UP_Nelson','IrrigTP_Solid_set_R2000WF_6_Nelson_1','IrrigTP_Solid_set_R2000WF_6_Nelson_2','IrrigTP_Solid_set_R2000WF_6_Nelson_3','IrrigTP_Solid_set_R33_Nelson','IrrigTP_Moving_wheel_R2000WF_6_Nelson_1','IrrigTP_Moving_wheel_R2000WF_6_Nelson_2','IrrigTP_Moving_wheel_R2000WF_6_Nelson_3','IrrigTP_drip_0_0','IrrigTP_Sub_surf_drip_0_0','IrrigTP_flood_0_0','IrrigTP_rill_0_0','IrrigTP_furrow_0_0','Noirrigation']
irri_model_list = ['Mech','Predefined']

#irri_list = ['DEFAULT_CENTER_PIVOT']
#irri_model_list = ['Mech']


cell_loc = '45.84375_-119.09375'

#User output
outdir = "/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Scenarios/Liu_Linux_309119_irrigation_evaluation/VIC_output"

target_var_list = ['Yield_kg_m2','irrig_netdemand_mm','irrig_total_mm','irrig_evap_mm','irrig_runoff_mm','water_stress_index','Runoff','Baseflow','Soil_E_mm','Crop_Canopy_E_mm','Act_Transp_mm','ET_mm','VIC_PET_shortgrass_mm','CropSyst_Pot_Transp_mm','PPT']
#key_list = ['Year','CroppingSyst_code','Crop_code']
#key_list_annual = ['Year','CroppingSyst_code']
key_list = ['Year']

all_var_list = key_list + target_var_list
os.chdir(outdir)

avglist = target_var_list + ['Model','Irrig']
avgdata = pd.DataFrame(columns=target_var_list)

for model in irri_model_list:
    print(model)
    for irri in irri_list:
        print("    " + irri)
        #vic_crop_outputs = "crop4001_cp_45.84375_-119.09375.asc"
        #vic_crop_outputs = "crop_Livneh_norotation_45.84375_-119.09375.asc"
        if (model == 'Predefined'):
            vic_crop_outputs = "CROP_" + irri + "_" + cell_loc + ".asc"
        else:
            vic_crop_outputs = model + "_CROP_" + irri + "_" + cell_loc + ".asc"
            
        vic_crop = pd.read_csv(vic_crop_outputs,sep=',',index_col=False)
        #print(key_list)
        temp = vic_crop[all_var_list]
        vic_select = temp.loc[temp['Year'] >= 1986]
        #vic_select = vic_select.drop('Crop_code', 1)

        vic_annual = vic_select.groupby(key_list,as_index=False)[target_var_list].sum()
        #vic_avg_annual = vic_annual.mean(index=False,axis=0)
        vic_annual['Year'] = 1
        vic_avg_annual = vic_annual.groupby(key_list,as_index=False)[target_var_list].mean()
        vic_avg_annual = vic_avg_annual.drop('Year', axis=1)
        vic_avg_annual['Model'] = model
        vic_avg_annual['Irrig'] = irri
        avgdata = avgdata.append(vic_avg_annual)
avgdata.to_csv("irrigation_efficiencies.txt", index=False)        
