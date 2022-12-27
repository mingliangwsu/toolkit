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



print("Done!")                    