#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 2022
Process fire results
@author: liuming
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
from pathlib import Path
import os
from os.path import exists
import math
#from scipy.interpolate import make_interp_spline, BSpline
#from scipy.ndimage.filters import gaussian_filter1d
from pyDOE import *

#0-1 to 0.01 - 100
def f_to_k(d0_1):
    return math.pow(10,(d0_1 - 0.5) * 4)
def f_to_year(d0_1):
    return int(1990 + round(d0_1 * (2000 - 1990)))

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

veglib = {1:"evergreen",
          2:"deciduous",
          5:"shrub"}
consumption_code = {"0.0":'gainsboro', 
                    "0.1":'lightgray', 
                    "0.5":'darkgrey', 
                    "1.0":'grey', 
                    "5.0":'gray', 
                    "25":'dimgrey', 
                    "50":'dimgray', 
                    "100":'black'}

path = "/home/liuming/mnt/hydronas2/Projects/FireEarth/BullRun"
simlist_file = path + "/simulation_list.txt"
patch_veg_file = path + "/patch_vegID2_04272022.txt"

sims = pd.read_csv(simlist_file,delimiter=r"\s+",header=None)
columns = ['SimID', 'BurnYear', 'Pspread', 'OverMortR', 'UnderMortR', 'KUMort', 'KCons', 'KoMort1', 'KoMort2']
sims.columns = columns

patch_veg = pd.read_csv(patch_veg_file,delimiter=",",header=0)

outpath = path + "/stat"

if not os.path.isdir(outpath):
    os.mkdir(outpath)

#v0=[1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000] #fire_year
#v1=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]            #fire_pspread
#v2=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]            #fire_overstory_mortality_rate
#v3=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]            #fire_understory_mortality_rate
#v4=[0.01, 0.1, 0.25, 0.5, 1, 2, 5, 10, 25, 50, 100]                   #fire_pc_ku_mort
#v5=[0.01, 0.1, 0.25, 0.5, 1, 2, 5, 10, 25, 50, 100]                   #fire_pc_kcons
#v6=[-10]                                                    #fire_pc_ko_mort1
#v7=[1]                                                      #fire_pc_ko_mort2




for index, row in sims.iterrows():
    #print(row)
    simid = int(row['SimID'])
    
    #process out_patch.monthly
    #month year basinID hillID zoneID patchID leach denitrif soil_moist_deficit et 
    #psn DOC DON lai nitrif mineralized uptake theta snow area nitrate sminn burn
    simoutput = path + "/simid_" + str(simid) + "/out_patch.monthly"
    if Path(simoutput).is_file():
       #tp = pd.read_csv(patch_monthly,delimiter=r"\s+")
       print("Reading " + simoutput)
       tp = pd.read_csv(simoutput,delimiter=r"\s+")
       tpveg = tp.merge(patch_veg,left_on='patchID',right_on='patch',how='left')
       #time_series
       temp = tpveg.groupby(['year','month','hillID','veg0']).mean().reset_index()
       temp = temp.drop(columns=['basinID', 'zoneID', 'patchID', 'area', 'burn', 'patch', 'veg1'])
       
       temp['simid'] = simid
       temp['year_aftb'] = temp['year'] - row['BurnYear']
       
       output = outpath + "/year_month_hillID_veg0_from_out_patch.monthly_simid_" + str(simid) + ".csv"
       temp.to_csv(output,index=False)
       
       #patch annual mean
       temp = tpveg.groupby(['year','patchID']).mean().reset_index()
       temp = temp.drop(columns=['month', 'basinID', 'hillID', 'zoneID', 'area', 'burn', 'patch', 'veg0', 'veg1'])
       
       temp['simid'] = simid
       temp['year_aftb'] = temp['year'] - row['BurnYear']
       output = outpath + "/year_patchID_from_out_patch.monthly_simid_" + str(simid) + ".csv"
       temp.to_csv(output,index=False)
       
    #process out_stratum.monthly
    #'month', 'year', 'basinID', 'hillID', 'zoneID', 'patchID', 'stratumID', 'veg_parm_ID', 'above_plantc',
    #'cover_fraction',  'height', 'all_lai', 'proj_lai'
    simoutput = path + "/simid_" + str(simid) + "/out_stratum.monthly"
    if Path(simoutput).is_file():
       #tp = pd.read_csv(patch_monthly,delimiter=r"\s+")
       print("Reading " + simoutput)
       tp = pd.read_csv(simoutput,delimiter=r"\s+")
       #tpveg = tp.merge(patch_veg,left_on='patchID',right_on='patch',how='left')
       #time_series
       temp = tp.groupby(['year','month','hillID','veg_parm_ID']).mean().reset_index()
       temp = temp.drop(columns=['basinID', 'zoneID', 'patchID', 'stratumID'])
       
       temp['simid'] = simid
       temp['year_aftb'] = temp['year'] - row['BurnYear']
       
       output = outpath + "/year_month_hillID_veg_parm_ID_from_out_stratum.monthly_simid_" + str(simid) + ".csv"
       temp.to_csv(output,index=False)
       
       #patch annual mean
       temp = tp.groupby(['year','patchID','veg_parm_ID']).mean().reset_index()
       temp = temp.drop(columns=['month', 'basinID', 'hillID', 'zoneID', 'stratumID'])
       
       temp['simid'] = simid
       temp['year_aftb'] = temp['year'] - row['BurnYear']
       output = outpath + "/year_patchID_veg_parm_ID_from_out_stratum.monthly_simid_" + str(simid) + ".csv"
       temp.to_csv(output,index=False)
       
    #process out_grow_patch.yearly
    #'year', 'basinID', 'hillID', 'zoneID', 'patchID', 'leaf_c', 'leaf_n', 'plant_c',
    # 'plant_n', 'litter_c', 'soil_c', 'litter_n', 'soil_n', 'nitrate', 'sminn', 'root_depth'
    simoutput = path + "/simid_" + str(simid) + "/out_grow_patch.yearly"
    if Path(simoutput).is_file():
       #tp = pd.read_csv(patch_monthly,delimiter=r"\s+")
       print("Reading " + simoutput)
       tp = pd.read_csv(simoutput,delimiter=r"\s+")
       tp = tp.merge(patch_veg,left_on='patchID',right_on='patch',how='left')
       #time_series
       temp = tp.groupby(['year','hillID','veg0']).mean().reset_index()
       temp = temp.drop(columns=['basinID', 'zoneID', 'patchID', 'patch', 'veg1'])
       
       temp['simid'] = simid
       temp['year_aftb'] = temp['year'] - row['BurnYear']
       
       output = outpath + "/year_hillID_veg0_from_out_grow_patch.yearly_simid_" + str(simid) + ".csv"
       temp.to_csv(output,index=False)
       
       #patch annual mean
       temp = tp.groupby(['year','patchID','veg0']).mean().reset_index()
       temp = temp.drop(columns=['basinID', 'hillID', 'zoneID', 'patch', 'veg1'])
       
       temp['simid'] = simid
       temp['year_aftb'] = temp['year'] - row['BurnYear']
       output = outpath + "/year_patchID_veg0_from_out_grow_patch.yearly_simid_" + str(simid) + ".csv"
       temp.to_csv(output,index=False)


       
    
