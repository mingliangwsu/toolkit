#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 13:56:50 2022
get strata veg ID (two stratas) for each patch 
@author: liuming
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
import os
from os.path import exists
import math
from scipy.interpolate import make_interp_spline, BSpline
from scipy.ndimage.filters import gaussian_filter1d

def q05(x):
    return x.quantile(0.05)
# 25th Percentile
def q25(x):
    return x.quantile(0.25)
# 50th Percentile
def q50(x):
    return x.quantile(0.5)

# 75th Percentile
def q75(x):
    return x.quantile(0.75)
def q95(x):
    return x.quantile(0.95)

modelresults_path = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/liudebug_output"

#get patch vegetation ID
path = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/process_data"
patch_vegid_file = path + "/patch_vegID2.txt"
patchveg = pd.read_csv(patch_vegid_file)
patchveg = patchveg.rename(columns={'patch': 'patchID'})

patch_xyz_file = path + "/patch_xyz.txt"
patch_xyz = pd.read_csv(patch_xyz_file)
patch_xyz = patch_xyz.rename(columns={'patch': 'patchID'})

#consumption_list = ["0.0", "0.1", "0.5", "1.0", "5.0", "25", "50", "100"]
#mort_list = ["0.0", "0.1", "0.2", "0.4", "0.6", "0.8", "1.0"]
consumption_list = ["0.0", "0.1", "0.5", "1.0", "5.0", "25", "50", "100"]
mort_list = ["0.1", "0.2", "0.4", "0.6", "0.8", "1.0"]
#`21223111qwconsumption_list = ["25"]
#mort_list = ["0.1"]

all_statistics_lai_annual = pd.DataFrame()
all_statistics_c_annual = pd.DataFrame()
map_lai_annual = pd.DataFrame()
map_c_annual = pd.DataFrame()

#import matplotlib.pyplot as plt
#plt.figure(figsize=(12,24)) 

for consumption in consumption_list:
    #for mort in 0.0 0.5 1.0
	#for mort in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
    
    for mort in mort_list:
        print(consumption + ":" + mort)
        #month year basinID hillID zoneID patchID leach denitrif soil_moist_deficit et psn DOC DON lai nitrif mineralized uptake theta snow area nitrate sminn burn
        pm_file = modelresults_path + "/eastern_output_fire_1990_m" + mort + "_consum_" + consumption + "_patch.monthly"    
        #year basinID hillID zoneID patchID leaf_c leaf_n plant_c plant_n litter_c soil_c litter_n soil_n nitrate sminn root_depth
        gp_file = modelresults_path + "/eastern_output_fire_1990_m" + mort + "_consum_" + consumption + "_grow_patch.yearly"
        size1 = 0
        size2 = 0
        if exists(pm_file) and exists(gp_file):
            size1 = os.path.getsize(pm_file)
            size2 = os.path.getsize(gp_file)
        if size1 > 10 and size2 > 10:
            pm_df = pd.read_csv(pm_file,delim_whitespace=True)
            gp_df = pd.read_csv(gp_file,delim_whitespace=True)
        
        
        
            #process LAI
            lai_annual = pm_df.groupby(['year','patchID']).agg(
                                                            lai_max=('lai', 'max'),
                                                            lai_mean=('lai', 'mean'),
                                                           ).reset_index()
            #lai_annual = lai_annual.rename(columns={"patchID": "patch", "B": "c"})
            lai_annual_veg = lai_annual.merge(patchveg,on="patchID",how="left")
            lai_annual_map = lai_annual.merge(patch_xyz,on="patchID",how="left")
            lai_annual_veg_curve = lai_annual_veg.groupby(['year','veg0']).agg(
                                                            lai_vegmx_min=('lai_max', 'min'),
                                                            lai_vegmx_max=('lai_max', 'max'),
                                                            lai_vegmx_mean=('lai_max', 'mean'),
                                                            lai_vegmx_median=('lai_max', 'median'),
                                                            lai_vegmx_q05=('lai_max', q05),
                                                            lai_vegmx_q25=('lai_max', q25),
                                                            lai_vegmx_q75=('lai_max', q75),
                                                            lai_vegmx_q95=('lai_max', q95)
                                                           ).reset_index()
            lai_annual_veg_curve['mort'] = float(mort)
            lai_annual_veg_curve['consumption'] = float(consumption)
            if all_statistics_lai_annual.empty:
                all_statistics_lai_annual = lai_annual_veg_curve.copy()
            else:
                all_statistics_lai_annual = all_statistics_lai_annual.append(lai_annual_veg_curve)
            
            lai_annual_map['mort'] = float(mort)
            lai_annual_map['consumption'] = float(consumption)
            if map_lai_annual.empty:
                map_lai_annual = lai_annual_map.copy()
            else:
                map_lai_annual = map_lai_annual.append(lai_annual_map)
        
        
            #process carbon
            c_annual_veg = gp_df.merge(patchveg,on="patchID",how="left")
            c_annual_map = gp_df.merge(patch_xyz,on="patchID",how="left")
            c_annual_veg_curve = c_annual_veg.groupby(['year','veg0']).agg(
                                                            leaf_c_min=('leaf_c', 'min'),
                                                            leaf_c_max=('leaf_c', 'max'),
                                                            leaf_c_mean=('leaf_c', 'mean'),
                                                            leaf_c_median=('leaf_c', 'median'),
                                                            leaf_c_q05=('leaf_c', q05),
                                                            leaf_c_q25=('leaf_c', q25),
                                                            leaf_c_q75=('leaf_c', q75),
                                                            leaf_c_q95=('leaf_c', q95),
                                                            plant_c_min=('plant_c', 'min'),
                                                            plant_c_max=('plant_c', 'max'),
                                                            plant_c_mean=('plant_c', 'mean'),
                                                            plant_c_median=('plant_c', 'median'),
                                                            plant_c_q05=('plant_c', q05),
                                                            plant_c_q25=('plant_c', q25),
                                                            plant_c_q75=('plant_c', q75),
                                                            plant_c_q95=('plant_c', q95),
                                                            litter_c_min=('litter_c', 'min'),
                                                            litter_c_max=('litter_c', 'max'),
                                                            litter_c_mean=('litter_c', 'mean'),
                                                            litter_c_median=('litter_c', 'median'),
                                                            litter_c_q05=('litter_c', q05),
                                                            litter_c_q25=('litter_c', q25),
                                                            litter_c_q75=('litter_c', q75),
                                                            litter_c_q95=('litter_c', q95),
                                                            soil_c_min=('soil_c', 'min'),
                                                            soil_c_max=('soil_c', 'max'),
                                                            soil_c_mean=('soil_c', 'mean'),
                                                            soil_c_median=('soil_c', 'median'),
                                                            soil_c_q05=('soil_c', q05),
                                                            soil_c_q25=('soil_c', q25),
                                                            soil_c_q75=('soil_c', q75),
                                                            soil_c_q95=('soil_c', q95)
                                                           ).reset_index()
            c_annual_veg_curve['mort'] = float(mort)
            c_annual_veg_curve['consumption'] = float(consumption)
            if all_statistics_c_annual.empty:
                all_statistics_c_annual = c_annual_veg_curve.copy()
            else:
                all_statistics_c_annual = all_statistics_c_annual.append(c_annual_veg_curve)
            
            c_annual_map['mort'] = float(mort)
            c_annual_map['consumption'] = float(consumption)
            if map_c_annual.empty:
                map_c_annual = c_annual_map.copy()
            else:
                map_c_annual = map_c_annual.append(c_annual_map)
"""
        for veg in [1]:
            t = lai_annual_veg_curve[lai_annual_veg_curve.veg0 == veg]
            xnew = np.linspace(t.year.min(), t.year.max(), 300)
            
            spl_md = make_interp_spline(t.year, t.lai_vegmx_median, k=3)  # type: BSpline
            power_smooth_md = spl_md(xnew)
            spl_q05 = make_interp_spline(t.year, t.lai_vegmx_q05, k=3)  # type: BSpline
            power_smooth_q05 = spl_q05(xnew)
            spl_q25 = make_interp_spline(t.year, t.lai_vegmx_q25, k=3)  # type: BSpline
            power_smooth_q25 = spl_q25(xnew)
            spl_q75 = make_interp_spline(t.year, t.lai_vegmx_q75, k=3)  # type: BSpline
            power_smooth_q75 = spl_q75(xnew)
            spl_q95 = make_interp_spline(t.year, t.lai_vegmx_q95, k=3)  # type: BSpline
            power_smooth_q95 = spl_q95(xnew)

            plt.plot(xnew, power_smooth_q05, linewidth=3)
            plt.plot(xnew, power_smooth_q25, linewidth=3)
            plt.plot(xnew, power_smooth_md, linewidth=3, color='black')
            plt.plot(xnew, power_smooth_q75, linewidth=3)
            plt.plot(xnew, power_smooth_q95, linewidth=3)
            
            
            #plt.plot(t.year, t.lai_vegmx_median, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q05, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q25, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q75, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q95, linewidth=3)
"""

#export dataframe
all_statistics_lai_annual.to_csv(path + "/all_statistics_lai_annual.csv",index=False)
all_statistics_c_annual.to_csv(path + "/all_statistics_c_annual.csv",index=False)
map_lai_annual.to_csv(path + "/map_lai_annual.csv",index=False)
map_c_annual.to_csv(path + "/map_c_annual.csv",index=False)

print("Done!")                    