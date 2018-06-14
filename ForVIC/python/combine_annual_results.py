#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 08:50:46 2018
Convert excel annual daily averaged VIC-CropSyst (hydro- and 
irrigation-related variables)


@author: liuming
"""

import pandas as pd
import os


indir = "/home/liuming/data/BPA_output/crop4001"
outdir = "/home/liuming/data/BPA_output/crop4001_processed"
output_file = "irrigation_annual_daymean.csv"
os.chdir(indir)
columns_name = ['cell_id', 'lon', 'lat', 'Year', 'Month', 'Day', 'DOY', 'Dist', 'Band', 'Cell_fract', 'CroppingSyst_code', 'Crop_code', 'Crop_name', 'Accum_DD', 'Grow_Stage', 'VIC_LAI', 'LAI', 'GAI', 'Total_Canopy_Cover', 'Biomass_kg_m2', 'Yield_kg_m2', 'Root_depth_mm', 'VIC_PET_shortgrass_mm', 'CropSyst_Pot_Transp_mm', 'Act_Transp_mm', 'irrig_netdemand_mm', 'irrig_total_mm', 'irrig_evap_mm', 'irrig_runoff_mm', 'irrig_intcpt_mm', 'Soil_E_mm', 'Canopy_E_mm', 'ET_mm', 'water_stress_index', 'Runoff', 'Baseflow', 'PPT', 'Tair_avg', 'Tmax', 'Tmin', 'SWRAD_w_m2', 'VP_kPa', 'SPH_kg_kg', 'RHUM_avg_%', 'RHUM_max_%', 'RHUM_min_%', 'Snow_dep_mm', 'Crop_Biomass_kg_m2', 'Surface_Residue_C_kg_m2', 'Soil_Residue_C_kg_m2', 'Soil_SOM_C_kg_m2', 'Canopy_Biomass_N_kg_m2', 'Surface_Residue_N_kg_m2', 'Soil_Residue_N_kg_m2', 'Soil_SOM_N_kg_m2', 'Soil_NO3_N_kg_m2', 'Soil_NH4_N_kg_m2', 'NPP_C_kg_m2', 'CO2_C_loss_Residue_kg_m2', 'CO2_C_loss_SOM_kg_m2', 'N_applied_inorg_kg_m2', 'N_applied_org_kg_m2', 'volatilization_loss_NH3_kg_m2', 'volatilization_total_kg_m2', 'N_uptake_kg_m2', 'N_stress_index', 'Nitrification_N_kg_m2', 'DeNitrification_N_kg_m2', 'Nitrification_N2O_N_kg_m2', 'DeNitrification_N2O_N_kg_m2', 'Profile_soil_liquid_water_mm']
#tdf = pd.DataFrame([0,0,0,0,0,0,0], columns=columns_name)

for irrig in range(49):
    #print(irrig)
    sheet_name = "ann_irrig_" + str(irrig)
    exl_name = sheet_name + ".xlsx"
    print(exl_name)
    df = pd.read_excel(exl_name, sheetname=sheet_name)                         #DataFrame
    
    subdf = df[df.Year >= 1922]
   
    if irrig == 0:
        avgdata = pd.DataFrame(columns=columns_name)
        loct = 0
    t0 = irrig
    t1 = df['irrig_total'].mean()
    t2 = df['irrig_evap'].mean()
    t3 = df['irrig_ro'].mean()
    t4 = df['vic_ro_noirrig'].mean()
    t5 = df['avg_baseflow'].mean()
    avgdata = avgdata.append({'Irrig' : t0, 'irrig_total' : t1,'irrig_evap' : t2,'irrig_ro' : t3,'vic_ro_noirrig' : t4,'avg_baseflow' : t5},ignore_index=True)
    
avgdata.to_csv(output_file,sep=',')
