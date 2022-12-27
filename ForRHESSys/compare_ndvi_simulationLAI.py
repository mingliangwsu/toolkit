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
    g = 0
    if sim == 0:
        g = 0
    elif sim > 0 and sim <= 50:
        g = 1
    elif sim >= 51 and sim <= 110:
        g = 2
    elif sim > 111 and sim <= 160:
        g = 3
    return g


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

#veglib = {1:"evergreen",
#          2:"deciduous",
#          3:"grass",
#          5:"shrub"}

sim_clr = {0:"k",1:"b",2:"g",3:"r"}
sim_stl = { 0:"-",1:'--',2:':',3:'-.'}
outpath = "/home/liuming/mnt/hydronas3/Projects/FireEarth/Landsat_post_fire"
ndvi = "/home/liuming/mnt/hydronas3/Projects/FireEarth/Landsat_post_fire/NDVI.csv"
lai = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/figures_12072022/laievergreen.csv"
dndvi = pd.read_csv(ndvi,delimiter=",",header=0)
dlai = pd.read_csv(lai,delimiter=",",header=0)

"""


t = [data1,data2]

dataall = pd.concat(t)

data = dataall.sort_values(by=['Fire_ID','year','doy'])

datamax = data.groupby(["Fire_ID","year_aftb"]).max().reset_index()
vars = ['NDVI','EVI']
figindex = 1
for var in vars:
    drange = datamax.groupby(['year_aftb']).agg(x_min=(var, 'min'),
                        x_max=(var, 'max'),
                        x_mean=(var, 'mean'),
                        x_median=(var, 'median'),
                        x_q05=(var, q05),
                        x_q25=(var, q25),
                        x_q75=(var, q75),
                        x_q95=(var, q95)
                        ).reset_index()
    plt.figure(num=figindex,figsize=(10,5)) 
    plt.title(var, fontsize=18)
    plt.ylabel(var, fontsize=18)
    plt.yticks(fontsize=16)
    plt.xlabel('After Burn', fontsize=18)
    plt.xticks(fontsize=16)            
    plt.figure(figindex)    
    print("figindex:" + str(figindex))
    xnew = drange
    plt.plot(xnew['year_aftb'], xnew["x_median"], linewidth=2, label="median",linestyle=sim_stl[0],color=sim_clr[0])
    #plt.plot(xnew, tgrp["x_median"], linewidth=2, label=simgroups[group] + str(hill),color=sim_clr[group])
    plt.fill_between(xnew['year_aftb'], xnew["x_q25"], xnew["x_q75"], color=sim_clr[0], alpha=.3)
    plt.fill_between(xnew['year_aftb'], xnew["x_q05"], xnew["x_q95"], color=sim_clr[0], alpha=.1)
    plt.legend(fontsize=10)
    figname = outpath + "/" + var + ".png"
    plt.savefig(figname)
    drange.to_csv(outpath + "/" + var + ".csv")
    #plt.close()
    figindex += 1

"""
"""
veglib = {1:"evergreen"}

#series 1: define pspread (burn intensity), i.e. change byear + pspread + fire_pc_ku_mort + fire_pc_kcons  
#series 2: define mortality, i.e. change byear + fire_overstory_mortality_rate + fire_understory_mortality_rate + fire_pc_kcons  
#series 3: define fire_understory_mortality_rate, i.e. change byear + fire_understory_mortality_rate + fire_pc_kcons  

#simgroups = {0:"w/o Fire", 1:"v_pspread", 2:"v_mortality", 3:"v_ud_mortality"}
simgroups = {1:"v_pspread", 2:"v_mortality", 3:"v_ud_mortality"}

#simgroups = {1:"v_pspread"}
sim_clr = {0:"k",1:"b",2:"g",3:"r"}
sim_stl = { 0:"-",1:'--',2:':',3:'-.'}

path = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min"
statpath = "/home/liuming/mnt/hydronas3/Projects/FireEarth/stat_12072022/"
#simlist_file = path + "/simulation_list_brw.txt"
simlist_file = path + "/simulation_list_brw_nosim0.txt"
patch_veg_file = path + "/patch_vegID2_04272022.txt"

sims = pd.read_csv(simlist_file,delimiter=r"\s+",header=None)
columns = ['SimID', 'BurnYear', 'Pspread', 'OverMortR', 'UnderMortR', 'KUMort', 'KCons', 'KoMort1', 'KoMort2']
sims.columns = columns

patch_veg = pd.read_csv(patch_veg_file,delimiter=",",header=0)

outpath = path + "/figures_12072022"

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
#target_files = {"year_hill_pool" : "year_hillID_veg0_from_out_grow_patch.yearly_simid_",
#                "month_hill_lai_fluxes " : "year_month_hillID_veg0_from_out_patch.monthly_simid_",
#                "month_hill_plant ": "year_month_hillID_veg_parm_ID_from_out_stratum.monthly_simid_"}

target_files = {"year_hill_pool" : "year_hillID_veg0_from_out_grow_patch.yearly_simid_"}
hills = [310,356,370]

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
  lw = 0
  for hill in hills:
    lw += 1
    data[target] = pd.DataFrame()
    for index, row in sims.iterrows():
        #print(row)
        simid = int(row['SimID'])
        tgroup = sim_to_simgroup(simid)
        #print("sim:" + str(simid) + " group:" + str(group))
        simoutput = statpath + target_files[target] + str(simid) + ".csv"
        if Path(simoutput).is_file():
            t = pd.read_csv(simoutput,delimiter=",")
            t["sim_group"] = tgroup
            if data[target].empty:
                data[target] = t.copy()
            else:
                data[target] = data[target].append(t)
    data[target] = data[target][(data[target]['year'] <= 2017) & (data[target]['year_aftb'] >= -5) & (data[target]["year_aftb"] <= 15) & (data[target]["hillID"] == hill)]    

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
                print("figindex:" + str(figindex))
                for group in simgroups:
                    tgrp = drange[(drange["sim_group"] == group) & (drange["veg0"] == veg)]
                    xnew = tgrp[timestep]
                    plt.plot(xnew, tgrp["x_median"], linewidth=lw, label="h " + str(hill) + " " + simgroups[group],linestyle=sim_stl[group],color=sim_clr[group])
                    #plt.plot(xnew, tgrp["x_median"], linewidth=2, label=simgroups[group] + str(hill),color=sim_clr[group])
                    plt.fill_between(xnew, tgrp["x_q25"], tgrp["x_q75"], color=sim_clr[group], alpha=.3)
                    #plt.fill_between(xnew, tgrp["x_q05"], tgrp["x_q95"], color=sim_clr[group], alpha=.1)
                plt.legend(fontsize=10)
                figname = outpath + "/" + var + "_" + veglib[veg] + "_hill_" + str(hill) + ".png"
                plt.savefig(figname)
                #plt.close()
            figindex += 1

       
"""    
