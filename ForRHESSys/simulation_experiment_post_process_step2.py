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
from scipy.interpolate import make_interp_spline, BSpline
from scipy.ndimage.filters import gaussian_filter1d
#from pyDOE import *

#0-1 to 0.01 - 100
def f_to_k(d0_1):
    return math.pow(10,(d0_1 - 0.5) * 4)
def f_to_year(d0_1):
    return int(1990 + round(d0_1 * (2000 - 1990)))
def sim_to_simgroup(sim):
    return sim // 40 + 1


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

#veglib = {1:"evergreen",
#          2:"deciduous",
#          3:"grass",
#          4:"nonveg",
#          5:"shrub",
#          6:"water"}

veglib = {1:"evergreen",
          2:"deciduous",
          3:"grass",
          5:"shrub"}

#series 1: define pspread (burn intensity), i.e. change byear + pspread + fire_pc_ku_mort + fire_pc_kcons  
#series 2: define mortality, i.e. change byear + fire_overstory_mortality_rate + fire_understory_mortality_rate + fire_pc_kcons  
#series 3: define fire_understory_mortality_rate, i.e. change byear + fire_understory_mortality_rate + fire_pc_kcons  

simgroups = {1:"v_pspread", 
             2:"v_mortality", 
             3:"v_ud_mortality"}

#simgroups = {1:"v_pspread"}
sim_clr = {1:"k", 
             2:"g", 
             3:"r"}
sim_stl = {1:'-', 
             2:':', 
             3:'-.'}

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
#patch_veg_file = path + "/patch_vegID2_04272022.txt"

sims = pd.read_csv(simlist_file,delimiter=r"\s+",header=None)
columns = ['SimID', 'BurnYear', 'Pspread', 'OverMortR', 'UnderMortR', 'KUMort', 'KCons', 'KoMort1', 'KoMort2']
sims.columns = columns

patch_veg = pd.read_csv(patch_veg_file,delimiter=",",header=0)

outpath = path + "/figures"

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

#target_files = {"month_hill_plant ": "year_month_hillID_veg_parm_ID_from_out_stratum.monthly_simid_"}
target_files = {"year_hill_pool" : "year_hillID_veg0_from_out_grow_patch.yearly_simid_",
                "month_hill_lai_fluxes " : "year_month_hillID_veg0_from_out_patch.monthly_simid_",
                "month_hill_plant ": "year_month_hillID_veg_parm_ID_from_out_stratum.monthly_simid_"}

data = dict()
#Time series data

#year_hillID_veg0_from_out_grow_patch.yearly_simid_
#year,hillID,veg0,leaf_c,leaf_n,plant_c,plant_n,litter_c,soil_c,litter_n,soil_n,nitrate,sminn,root_depth,simid,year_aftb

#year_month_hillID_veg0_from_out_patch.monthly_simid_
#year,month,hillID,veg0,leach,denitrif,soil_moist_deficit,et,psn,DOC,DON,lai,nitrif,mineralized,uptake,theta,snow,nitrate,sminn,simid,year_aftb

#year_month_hillID_veg_parm_ID_from_out_stratum.monthly_simid_
#year,month,hillID,veg_parm_ID,above_plantc,cover_fraction,height,all_lai,proj_lai,simid,year_aftb
target_vars = {"plant_c" : "kgC/m2", 
               "litter_c" : "kgC/m2", 
               "soil_c" : "kgC/m2",
               "nitrate" : "kgN/m2",
               "sminn" : "kgN/m2",
               "psn" : "gC/m2/month",
               "et" : "mm/month",
               "lai" : "m2/m2", 
               "proj_lai" : "m2/m2",
               "height" : "m"}

for target in target_files:
    data[target] = pd.DataFrame()
    for index, row in sims.iterrows():
        #print(row)
        simid = int(row['SimID'])
        group = sim_to_simgroup(simid)
        #print("sim:" + str(simid) + " group:" + str(group))
        simoutput = path + "/stat/" + target_files[target] + str(simid) + ".csv"
        if Path(simoutput).is_file():
            t = pd.read_csv(simoutput,delimiter=",")
            t["sim_group"] = group
            if data[target].empty:
                data[target] = t.copy()
            else:
                data[target] = data[target].append(t)
    data[target] = data[target][(data[target]['year'] <= 2017) & (data[target]['year_aftb'] >= -5) & (data[target]["year_aftb"] <= 15)]    

    if "veg_parm_ID" in data[target].columns:
        data[target] = data[target].rename({"veg_parm_ID" : "veg0"}, axis='columns')
    if "month" in data[target].columns:
        data[target]["month_aftb"] = data[target]["year_aftb"] * 12 + data[target]["month"] - 5
        timestep = "month_aftb"
    else:
        timestep = "year_aftb"
    
    #always output annual 
    timestep = "year_aftb"
    t = data[target].groupby(["simid",timestep,"veg0"]).mean().reset_index()
    
    #plot for each land cover and variable
    figindex = 1
    for veg in veglib:
        for var in target_vars:
            if var in data[target].columns:
                drange = t.groupby(['sim_group',timestep,'veg0']).agg(
                        x_min=(var, 'min'),
                        x_max=(var, 'max'),
                        x_mean=(var, 'mean'),
                        x_median=(var, 'median'),
                        x_q05=(var, q05),
                        x_q25=(var, q25),
                        x_q75=(var, q75),
                        x_q95=(var, q95)
                        ).reset_index()
                
                #plot
                plt.figure(num=figindex,figsize=(10,5)) 
                plt.title(veglib[veg], fontsize=18)
                plt.ylabel(var + " (" + target_vars[var] + ")", fontsize=18)
                plt.yticks(fontsize=16)
                plt.xlabel('After Burn', fontsize=18)
                plt.xticks(fontsize=16)            
                plt.figure(figindex)    
                for group in simgroups:
                    tgrp = drange[(drange["sim_group"] == group) & (drange["veg0"] == veg)]
                    xnew = tgrp[timestep]
                    plt.plot(xnew, tgrp["x_median"], linewidth=2, label=simgroups[group],linestyle=sim_stl[group],color=sim_clr[group])
                    plt.fill_between(xnew, tgrp["x_q25"], tgrp["x_q75"], color=sim_clr[group], alpha=.2)
                    #plt.fill_between(xnew, tgrp["x_q05"], tgrp["x_q95"], color=sim_clr[group], alpha=.1)
                plt.legend(fontsize=12)
                figname = outpath + "/" + var + "_" + veglib[veg] + ".png"
                plt.savefig(figname)
            figindex += 1

       
    
