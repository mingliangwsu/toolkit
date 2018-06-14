#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 08:50:46 2018
Convert excel annual daily averaged VIC-CropSyst (hydro- and 
irrigation-related variables)

Now some code are hard coded for BPA project test outputs

@author: liuming
"""

import pandas as pd
import os
import glob
import sys

if (len(sys.argv) < 3):
    print("usage:", sys.argv[0], " [ndir] [outdir]")
    exit

#rotation_list = (400100, 400101, 400102)

indir = sys.argv[1]
outdir = sys.argv[2]
tmp = indir.rfind("/")
out_scenario = indir[tmp+1:]

os.chdir(indir)
columns_name = ('cell_id', 'lon', 'lat', 'Year', 'Month', 'Day', 'DOY', 'Dist', 'Band', 'Cell_fract', 'CroppingSyst_code', 'Crop_code', 'Crop_name', 'Accum_DD', 'Grow_Stage', 'VIC_LAI', 'LAI', 'GAI', 'Total_Canopy_Cover', 'Biomass_kg_m2', 'Yield_kg_m2', 'Root_depth_mm', 'VIC_PET_shortgrass_mm', 'CropSyst_Pot_Transp_mm', 'Act_Transp_mm', 'irrig_netdemand_mm', 'irrig_total_mm', 'irrig_evap_mm', 'irrig_runoff_mm', 'irrig_intcpt_mm', 'Soil_E_mm', 'Canopy_E_mm', 'ET_mm', 'water_stress_index', 'Runoff', 'Baseflow', 'PPT', 'Tair_avg', 'Tmax', 'Tmin', 'SWRAD_w_m2', 'VP_kPa', 'SPH_kg_kg', 'RHUM_avg_%', 'RHUM_max_%', 'RHUM_min_%', 'Snow_dep_mm', 'Crop_Biomass_kg_m2', 'Surface_Residue_C_kg_m2', 'Soil_Residue_C_kg_m2', 'Soil_SOM_C_kg_m2', 'Canopy_Biomass_N_kg_m2', 'Surface_Residue_N_kg_m2', 'Soil_Residue_N_kg_m2', 'Soil_SOM_N_kg_m2', 'Soil_NO3_N_kg_m2', 'Soil_NH4_N_kg_m2', 'NPP_C_kg_m2', 'CO2_C_loss_Residue_kg_m2', 'CO2_C_loss_SOM_kg_m2', 'N_applied_inorg_kg_m2', 'N_applied_org_kg_m2', 'volatilization_loss_NH3_kg_m2', 'volatilization_total_kg_m2', 'N_uptake_kg_m2', 'N_stress_index', 'Nitrification_N_kg_m2', 'DeNitrification_N_kg_m2', 'Nitrification_N2O_N_kg_m2', 'DeNitrification_N2O_N_kg_m2', 'Profile_soil_liquid_water_mm')
#crop_name = ('corn_grain-irrigated','potato-irrigated','wheat_winter-irrigated')
#crop_name = ['potato-irrigated']
#key_list = ['cell_id', 'lon', 'lat', 'Year', 'Month','Crop_name']
key_list = ('cell_id', 'Year', 'Month')
sum_list = ( 'Yield_kg_m2','irrig_netdemand_mm', 'irrig_total_mm', 'irrig_evap_mm', 'irrig_runoff_mm', 'Runoff', 'Baseflow', 'PPT')

key_list_all = {}
key_list_all['rotation'] = key_list + ('CroppingSyst_code',)
key_list_all['rotation_crop'] = key_list + ('CroppingSyst_code', 'Crop_name',)

avgdata = {}
for outtable in ['rotation','rotation_crop']:
    avgdata[outtable] = pd.DataFrame(columns=(key_list_all[outtable] + sum_list))
#tdf = pd.DataFrame([0,0,0,0,0,0,0], columns=columns_name)

#for files in glob.glob("crop4001_cp_45.46875_-119.9*.asc"):
for files in glob.glob("crop4001*.asc"):
    print(files)
    f = open(files)
    first = f.readline()
    f.close()
    if "cell_id" in first:
        temp = pd.read_csv(files,sep=',',header=0,low_memory=False)
    else:
        temp = pd.read_csv(files,sep=',',header=None,low_memory=False)
        temp.columns = columns_name
    for outtable in ['rotation','rotation_crop']:
        tempsub = temp.groupby(key_list_all[outtable],as_index=False)[sum_list].sum()
        avgdata[outtable] = avgdata[outtable].append(tempsub)

for outtable in ['rotation','rotation_crop']:
    avgdata[outtable].to_csv(outdir + "/" + out_scenario + "_" + outtable + ".csv", index = False)
