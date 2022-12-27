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
from pathlib import Path


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
patch_location = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/process_data/patch_init_state.txt"
#simlist_file = path + "/simulation_list_brw.txt"
simlist_file = path + "/simulation_list_brw_nosim0.txt"
patch_veg_file = path + "/patch_vegID2_04272022.txt"

sims = pd.read_csv(simlist_file,delimiter=r"\s+",header=None)
columns = ['SimID', 'BurnYear', 'Pspread', 'OverMortR', 'UnderMortR', 'KUMort', 'KCons', 'KoMort1', 'KoMort2']
sims.columns = columns

patch_veg = pd.read_csv(patch_veg_file,delimiter=",",header=0)
patch_loc = pd.read_csv(patch_location,delimiter=",",header=0)
patch_loc = patch_loc[['patch','x','y','z']]
patch_loc = patch_loc.rename({"patch" : "patchID"}, axis='columns')

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

#target_files = {"year_patch_pool" : "year_patchID_veg0_from_out_grow_patch.yearly_simid_",
#                "year_stratum_lai_height" : "year_patchID_veg_parm_ID_from_out_stratum.monthly_simid_"}

target_files = {"year_patch_pool" : "year_patchID_veg0_from_out_grow_patch.yearly_simid_"}

data = dict()
#Time series data

#year_hillID_veg0_from_out_grow_patch.yearly_simid_
#year,hillID,veg0,leaf_c,leaf_n,plant_c,plant_n,litter_c,soil_c,litter_n,soil_n,nitrate,sminn,root_depth,simid,year_aftb

#year_month_hillID_veg0_from_out_patch.monthly_simid_
#year,month,hillID,veg0,leach,denitrif,soil_moist_deficit,et,psn,DOC,DON,lai,nitrif,mineralized,uptake,theta,snow,nitrate,sminn,simid,year_aftb

#year_month_hillID_veg_parm_ID_from_out_stratum.monthly_simid_
#year,month,hillID,veg_parm_ID,above_plantc,cover_fraction,height,all_lai,proj_lai,simid,year_aftb

#year_patchID_veg0_from_out_grow_patch.yearly_simid_
#year,patchID,veg0,leaf_c,leaf_n,plant_c,plant_n,litter_c,soil_c,litter_n,soil_n,nitrate,sminn,root_depth,denitrif,simid,year_aftb

#year_patchID_veg_parm_ID_from_out_stratum.monthly_simid_
#year,patchID,veg_parm_ID,above_plantc,cover_fraction,height,all_lai,proj_lai,simid,year_aftb

"""
target_vars = {"plant_c" : "kgC/m2", 
               "litter_c" : "kgC/m2", 
               "soil_c" : "kgC/m2",
               "nitrate" : "kgN/m2",
               "sminn" : "kgN/m2",
               "psn" : "gC/m2/month",
               "et" : "mm/month",
               "lai" : "m2/m2", 
               "proj_lai" : "m2/m2",
               "height" : "m",
               "above_plantc" : "kgC/m2",
               "root_depth" : "m"}
"""
target_vars = {"plant_c" : "kgC/m2"}
keys = ['patchID','veg0','veg_parm_ID','year_aftb','simid']

for target in target_files:
    data[target] = pd.DataFrame()
    for index, row in sims.iterrows():
      if index <= 2:
        #print(row)
        simid = int(row['SimID'])
        tgroup = sim_to_simgroup(simid)
        print("sim:" + str(simid) + " group:" + str(tgroup))
        simoutput = statpath + target_files[target] + str(simid) + ".csv"
        if Path(simoutput).is_file():
            t = pd.read_csv(simoutput,delimiter=",")
            
            #only select target vars or keys
            for var in t:
                if (var not in keys) and (var not in target_vars):
                    t = t.drop(columns=[var])
            
            t["sim_group"] = tgroup
            if data[target].empty:
                data[target] = t.copy()
            else:
                data[target] = data[target].append(t)
    data[target] = data[target][(data[target]['year_aftb'] >= -5) & (data[target]["year_aftb"] <= 15)]    

    if "veg_parm_ID" in data[target].columns:
        data[target] = data[target].rename({"veg_parm_ID" : "veg0"}, axis='columns')
    if "month" in data[target].columns:
        data[target]["month_aftb"] = data[target]["year_aftb"] * 12 + data[target]["month"] - 5
        timestep = "month_aftb"
    else:
        timestep = "year_aftb"
    
    #always output annual 
    timestep = "year_aftb"
    t = data[target].groupby(["simid",timestep,"patchID","veg0"]).mean().reset_index()
    
    #plot for each land cover and variable
    figindex = 1
    for veg in veglib:
        tsub = t[t["veg0"] == veg]  
        for var in target_vars:
            if var in tsub.columns:
                print("veg:" + str(veg) + " var:" + var)
                drange = tsub.groupby(['sim_group',timestep,'patchID']).agg(
                        #x_min=(var, 'min'),
                        #x_max=(var, 'max'),
                        #x_mean=(var, 'mean'),
                        x_median=(var, 'median'),
                        #x_q05=(var, q05),
                        #x_q25=(var, q25),
                        #x_q75=(var, q75),
                        #x_q95=(var, q95)
                        ).reset_index()
                
                drange_with_xyz = drange.merge(patch_loc,on=['patchID'],how='left')
                fig = plt.figure(figsize=(30,16)) 
                p1 = plt.scatter(drange_with_xyz.x, drange_with_xyz.y,c=drange_with_xyz.x_median,cmap='YlGn',vmin=0, vmax=30,s=30)
                #cbar = fig.colorbar(p1, label='x_median')
                #plt.colorbar(p1)
                #cbar = fig.colorbar(p1, label='LAI')
                #for tic in cbar.ax.get_yticklabels():
                #    tic.set_fontsize(16)
                plt.title(var,fontsize=18)
                #plt.colorbar(p1)
                #plt.savefig(path + "/map_LAI_"+ str(year) + "_ps_" + mort + ".png")
                plt.close()
                #plt.plot(xnew, power_smooth_md, linewidth=3, label=consumption,color=consumption_code[consumption])
                #plt.legend(loc="upper left",fontsize=12)
                #plt.legend(fontsize=12)
                 #export fig
                #figname = path + "/map_lai_veg_" + veglib[veg] + "_mort_" + mort + ".png"
                #plt.savefig(figname)
                #plt.close()
                



















"""










#modelresults_path = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/liudebug_output"

#get patch vegetation ID
path = "/home/liuming/mnt/hydronas3/Projects/FireEarth/process_data"
#all_statistics_lai_annual = pd.read_csv(path + "/all_statistics_lai_annual.csv")
#all_statistics_c_annual = pd.read_csv(path + "/all_statistics_c_annual.csv")



map_lai_annual = pd.read_csv(path + "/s1_map_lai_annual.csv")


#map_c_annual = pd.read_csv(path + "/map_c_annual.csv")

#average 1985-1989
map_lai_annual_1985_1989 = map_lai_annual[(map_lai_annual.year >= 1985) & (map_lai_annual.year <= 1989) & (map_lai_annual.ps <= 0.001)].groupby(['patchID']).agg(
        lai_max_avg=('lai_max', 'mean'),
        x=('x', 'mean'),
        y=('y', 'mean'),
        z=('z', 'mean')).reset_index()

fig = plt.figure(figsize=(30,16)) 
#plt.ylabel('y', fontsize=18)
#plt.yticks(fontsize=16)
#plt.xlabel('x', fontsize=18)
#plt.xticks(fontsize=16)            

p1 = plt.scatter(map_lai_annual_1985_1989.x, map_lai_annual_1985_1989.y,
            c=map_lai_annual_1985_1989.lai_max_avg,vmin=0, vmax=10,cmap='YlGn',s=30,marker='s')
cbar = fig.colorbar(p1, label='LAI')
#ticklabs = cbar.ax.get_yticklabels()
#cbar.ax.set_yticklabels(ticklabs, fontsize=12)
for t in cbar.ax.get_yticklabels():
    t.set_fontsize(16)
plt.title("Mean peak LAI 1985-1989",fontsize=18)
plt.savefig(path + "/mean_LAI_1985_1989.png")
plt.close()

#plt.legend()
#consumption_list = ["0.0", "0.1", "0.5", "1.0", "5.0", "25", "50", "100"]
#mort_list = ["0.0", "0.1", "0.2", "0.4", "0.6", "0.8", "1.0"]
#consumption_list = ["0.0", "0.1", "0.5", "1.0", "5.0", "25", "50", "100"]
mort_list = ["0.0","0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]

consumption_list = ["1.0"]
#mort_list = ["0.6"]

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




#for mort in mort_list:
  
figindex = 1
#for year in range(1990,2016,1):
for year in range(1985,2018,1):
    #for consumption in consumption_list:
        for mort in mort_list:
            t =  map_lai_annual[(map_lai_annual.year == year) & (map_lai_annual.ps == float(mort))]
            if len(t) > 0:
                print(" ps " + mort + " " + str(year))
                fig = plt.figure(figsize=(30,16)) 
                p1 = plt.scatter(t.x, t.y,
                                 c=t.lai_max,cmap='YlGn',vmin=0, vmax=10,s=30,marker='s')
                cbar = fig.colorbar(p1, label='LAI')
                #cbar = fig.colorbar(p1, label='LAI')
                for t in cbar.ax.get_yticklabels():
                    t.set_fontsize(16)
                #ticklabs = cbar.ax.get_yticklabels()
                #cbar.ax.set_yticklabels(ticklabs, fontsize=12)
                

                plt.title("LAI " + str(year) + "    pspread:" + mort,fontsize=18)
                plt.savefig(path + "/map_LAI_"+ str(year) + "_ps_" + mort + ".png")
                plt.close()
                #plt.plot(xnew, power_smooth_md, linewidth=3, label=consumption,color=consumption_code[consumption])
                #plt.legend(loc="upper left",fontsize=12)
                #plt.legend(fontsize=12)
                 #export fig
                #figname = path + "/map_lai_veg_" + veglib[veg] + "_mort_" + mort + ".png"
                #plt.savefig(figname)
                #plt.close()
            
    #figindex += 1
            #plt.plot(t.year, t.lai_vegmx_median, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q05, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q25, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q75, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q95, linewidth=3)

"""

print("Done!")                    