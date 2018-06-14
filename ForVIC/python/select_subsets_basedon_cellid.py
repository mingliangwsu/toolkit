#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 01:45:46 2018

@author: liuming
"""

import pandas as pd
import os
import glob
import sys

indir = "/media/liuming/8E6A81026A80E873/May2_output"

#valid_cells = [297965, 299821, 299822, 299823, 300748, 300749, 300750, 300756, 301683, 301684, 302604, 302605, 302606, 302608, 302610, 302611, 302613, 303531, 303532, 303533, 303534, 303535, 303536, 303537, 303538, 303539, 303541, 303542, 303555, 304459, 304460, 304462, 304463, 304464, 304465, 304466, 304467, 304468, 304469, 304470, 304471, 304472, 304483, 304484, 304485, 305390, 305392, 305394, 305395, 305396, 305397, 305398, 305399, 305400, 305401, 305402, 305403, 305408, 305413, 305414, 306310, 306311, 306314, 306315, 306316, 306322, 306327, 306328, 306329, 306330, 306331, 306332, 306334, 306340, 306341, 306342, 306343, 307249, 307250, 307255, 307258, 307259, 307260, 307261, 307262, 307263, 307264, 307265, 307266, 307267, 307268, 307269, 307270, 307271, 307272, 307273, 308177, 308178, 308180, 308183, 308186, 308187, 308190, 308191, 308192, 308193, 308194, 308195, 308196, 308197, 308198, 308199, 308200, 308201, 308202, 309111, 309112, 309115, 309117, 309119, 309120, 309121, 309122, 309123, 309124, 309125, 309126, 309127, 309128, 309129, 309130, 309131, 310036, 310042, 310047, 310050, 310051, 310052, 310053, 310054, 310055, 310056, 310057, 310058, 310059, 310060, 310964, 310967, 310969, 310970, 310972, 310973, 310974, 310979, 310980, 310981, 310983, 310984, 310987, 310988, 310989, 311885, 311891, 311892, 311893, 311894, 311895, 311896, 311897, 311898, 311899, 311900, 311912, 311913, 311916, 311917, 312818, 312819, 312821, 312822, 312824, 312825, 312826, 312827, 312835, 313747, 313749, 313750, 313751, 313752, 313753, 313754, 313755, 313762, 313763, 313765, 314679, 314680, 314681, 314692, 314693, 315621, 315622]
valid_cells = [306327, 307249, 307255, 308180, 309111, 309112, 309119, 310036, 310042, 310964, 310967, 310969, 310970, 310972, 310973, 310974, 311895, 311896, 311897, 311898, 311899, 311900, 312835, 313762, 313763, 314692, 314693, 315621, 315622]

os.chdir(indir)

clmscen = ("meanclm","meanclm_noirrig","transitclm","transitclm_noirrig")

columns_name = ('cell_id', 'lon', 'lat', 'Year', 'Month', 'Day', 'DOY', 'Dist', 'Band', 'Cell_fract', 'CroppingSyst_code', 'Crop_code', 'Crop_name', 'Accum_DD', 'Grow_Stage', 'VIC_LAI', 'LAI', 'GAI', 'Total_Canopy_Cover', 'Biomass_kg_m2', 'Yield_kg_m2', 'Root_depth_mm', 'VIC_PET_shortgrass_mm', 'CropSyst_Pot_Transp_mm', 'Act_Transp_mm', 'irrig_netdemand_mm', 'irrig_total_mm', 'irrig_evap_mm', 'irrig_runoff_mm', 'irrig_intcpt_mm', 'Soil_E_mm', 'Canopy_E_mm', 'ET_mm', 'water_stress_index', 'Runoff', 'Baseflow', 'PPT', 'Tair_avg', 'Tmax', 'Tmin', 'SWRAD_w_m2', 'VP_kPa', 'SPH_kg_kg', 'RHUM_avg_%', 'RHUM_max_%', 'RHUM_min_%', 'Snow_dep_mm', 'Crop_Biomass_kg_m2', 'Surface_Residue_C_kg_m2', 'Soil_Residue_C_kg_m2', 'Soil_SOM_C_kg_m2', 'Canopy_Biomass_N_kg_m2', 'Surface_Residue_N_kg_m2', 'Soil_Residue_N_kg_m2', 'Soil_SOM_N_kg_m2', 'Soil_NO3_N_kg_m2', 'Soil_NH4_N_kg_m2', 'NPP_C_kg_m2', 'CO2_C_loss_Residue_kg_m2', 'CO2_C_loss_SOM_kg_m2', 'N_applied_inorg_kg_m2', 'N_applied_org_kg_m2', 'volatilization_loss_NH3_kg_m2', 'volatilization_total_kg_m2', 'N_uptake_kg_m2', 'N_stress_index', 'Nitrification_N_kg_m2', 'DeNitrification_N_kg_m2', 'Nitrification_N2O_N_kg_m2', 'DeNitrification_N2O_N_kg_m2', 'Profile_soil_liquid_water_mm')
#crop_name = ('corn_grain-irrigated','potato-irrigated','wheat_winter-irrigated')
crop_name = ('potato-irrigated',)
#crop_name = ['potato-irrigated']
#key_list = ['cell_id', 'lon', 'lat', 'Year', 'Month','Crop_name']
key_list = ('cell_id', 'Year', 'Month')
sum_list = ( 'Yield_kg_m2','irrig_netdemand_mm', 'irrig_total_mm', 'irrig_evap_mm', 'irrig_runoff_mm', 'Runoff', 'Baseflow', 'PPT')

#tdf = pd.DataFrame([0,0,0,0,0,0,0], columns=columns_name)

#for files in glob.glob("crop4001_cp_45.46875_-119.9*.asc"):
    
for clm in clmscen:
    for crop in crop_name:
        filename = clm + crop + "_annual.csv"
        temp = pd.read_csv(filename,sep=',',header=0,low_memory=False)
        subset = temp.loc[temp['cell_id'].isin(valid_cells)]

        tempsub = subset.groupby("Year",as_index=False)[sum_list].mean()
        outfilename = "potato_sts_" + filename
        tempsub.to_csv(outfilename, index = False)
