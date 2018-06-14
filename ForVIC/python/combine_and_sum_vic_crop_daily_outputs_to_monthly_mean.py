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

if (len(sys.argv) < 4):
    print("usage:", sys.argv[0], " [[ndir] [outdir] [prefix]")

rotation_list = [400100, 400101, 400102]
crop_name_list = ['wheat_winter-irrigated', 'potato-irrigated', 'corn_grain-irrigated']

indir = sys.argv[1]
outdir = sys.argv[2]
output_file_prefix = sys.argv[3]
os.chdir(indir)
columns_name = ['cell_id', 'lon', 'lat', 'Year', 'Month', 'Day', 'DOY', 'Dist', 'Band', 'Cell_fract', 'CroppingSyst_code', 'Crop_code', 'Crop_name', 'Accum_DD', 'Grow_Stage', 'VIC_LAI', 'LAI', 'GAI', 'Total_Canopy_Cover', 'Biomass_kg_m2', 'Yield_kg_m2', 'Root_depth_mm', 'VIC_PET_shortgrass_mm', 'CropSyst_Pot_Transp_mm', 'Act_Transp_mm', 'irrig_netdemand_mm', 'irrig_total_mm', 'irrig_evap_mm', 'irrig_runoff_mm', 'irrig_intcpt_mm', 'Soil_E_mm', 'Canopy_E_mm', 'ET_mm', 'water_stress_index', 'Runoff', 'Baseflow', 'PPT', 'Tair_avg', 'Tmax', 'Tmin', 'SWRAD_w_m2', 'VP_kPa', 'SPH_kg_kg', 'RHUM_avg_%', 'RHUM_max_%', 'RHUM_min_%', 'Snow_dep_mm', 'Crop_Biomass_kg_m2', 'Surface_Residue_C_kg_m2', 'Soil_Residue_C_kg_m2', 'Soil_SOM_C_kg_m2', 'Canopy_Biomass_N_kg_m2', 'Surface_Residue_N_kg_m2', 'Soil_Residue_N_kg_m2', 'Soil_SOM_N_kg_m2', 'Soil_NO3_N_kg_m2', 'Soil_NH4_N_kg_m2', 'NPP_C_kg_m2', 'CO2_C_loss_Residue_kg_m2', 'CO2_C_loss_SOM_kg_m2', 'N_applied_inorg_kg_m2', 'N_applied_org_kg_m2', 'volatilization_loss_NH3_kg_m2', 'volatilization_total_kg_m2', 'N_uptake_kg_m2', 'N_stress_index', 'Nitrification_N_kg_m2', 'DeNitrification_N_kg_m2', 'Nitrification_N2O_N_kg_m2', 'DeNitrification_N2O_N_kg_m2', 'Profile_soil_liquid_water_mm']
crop_name = ['corn_grain-irrigated','potato-irrigated','wheat_winter-irrigated']
#crop_name = ['potato-irrigated']
#key_list = ['cell_id', 'lon', 'lat', 'Year', 'Month','Crop_name']
key_list = ['cell_id', 'Year', 'Month','Crop_name']
region_key = ['Year', 'Month','Crop_name']
cell_key = ['cell_id', 'Month','Crop_name']
cell_ann_key = ['cell_id', 'Crop_name']
sum_list = [ 'Yield_kg_m2','irrig_netdemand_mm', 'irrig_total_mm', 'irrig_evap_mm', 'irrig_runoff_mm', 'irrig_intcpt_mm', 'Soil_E_mm', 'Canopy_E_mm', 'ET_mm','Runoff', 'Baseflow', 'PPT']
all_out_col = key_list + sum_list

allregion_out_col = region_key + sum_list
avgdata = {}
for crop in crop_name:
    avgdata[crop] = pd.DataFrame(columns=all_out_col)
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
    subset = {}
    vic_annual = {}
    for crop in crop_name:
        subset[crop] = temp.loc[(temp['Crop_name'] == crop) & (temp['CroppingSyst_code'] == 400100)]
        vic_annual[crop] = subset[crop].groupby(key_list,as_index=False)[sum_list].sum()
        avgdata[crop] = avgdata[crop].append(vic_annual[crop])

t = {}
region_avgdata = {}
region_avgdata_size = {}
for crop in crop_name:
    region_avgdata[crop] = avgdata[crop].groupby(region_key,as_index=False)[sum_list].mean()
    region_avgdata_size[crop] = avgdata[crop].groupby(region_key,as_index=False)[sum_list].size().reset_index(name='counts')
    #region_avgdata[crop].join(region_avgdata_size[crop],on = region_key)
    t[crop] = pd.merge(region_avgdata[crop],region_avgdata_size[crop], on = region_key)
    
    t[crop].to_csv(outdir + '/region_mean_' + crop + '.csv',index = False)
    #region_avgdata_size[crop].to_csv(outdir + '/region_mean_size_' + crop + '.csv',index = False)
    
ct = {}
cell_avgdata = {}
cell_avgdata_size = {}
cell_anntotaldata = {}
total_months = {}
nct = {}
for crop in crop_name:
    cell_avgdata[crop] = avgdata[crop].groupby(cell_key,as_index=False)[sum_list].mean()
    cell_avgdata_size[crop] = avgdata[crop].groupby(cell_key,as_index=False)[sum_list].size().reset_index(name='counts')
    #total_months[crop] = cell_avgdata_size[crop].groupby('cell_id',as_index=False)['counts'].sum()
    total_months[crop] = cell_avgdata_size[crop].groupby('cell_id',as_index=False)['counts'].max()
    total_months[crop].columns = ['cell_id','total_months']
    
    ct[crop] = pd.merge(cell_avgdata[crop],cell_avgdata_size[crop], on = cell_key)
    nct[crop] = pd.merge(ct[crop], total_months[crop], on = 'cell_id')
    #tmp = [ row.counts / row.total_months for index, row in nct[crop].iterrows() ]
    #nct[crop]['weight'] = tmp
    
    for col in sum_list:
        #for row in nct[crop].iterrows():
        #    nct[crop].loc[row,col] = nct[crop].loc[row,col] * nct[crop].loc[row,'weight']
        coln = col + '_w'
        tmp = [ row[col] * row.counts / row.total_months for index, row in nct[crop].iterrows() ]
        nct[crop][col] = tmp
    
    nct[crop].to_csv(outdir + '/cellmap_mon_mean_' + crop + '.csv',index = False)
    #cell_avgdata_size[crop].to_csv(outdir + '/cellmap_mon_mean_size_' + crop + '.csv',index = False)
    
    
    cell_anntotaldata[crop] = nct[crop].groupby(cell_ann_key,as_index=False)[sum_list].sum()
    cell_anntotaldata[crop].to_csv(outdir + '/cellmap_annual_' + crop + '.csv',index = False)
    #cellmap_mon_sum should divide the maximum of cellmap_mon_count to get monthly mean