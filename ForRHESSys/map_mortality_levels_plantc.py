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
#all_statistics_lai_annual = pd.read_csv(path + "/all_statistics_lai_annual.csv")
#all_statistics_c_annual = pd.read_csv(path + "/all_statistics_c_annual.csv")



#map_lai_annual = pd.read_csv(path + "/map_lai_annual.csv")


#map_c_annual = pd.read_csv(path + "/map_c_annual.csv")

#average 1985-1989
map_annual_1985_1989 = map_c_annual[(map_c_annual.year >= 1985) & (map_c_annual.year <= 1989)].groupby(['patchID']).agg(
        avgv=('plant_c', 'mean'),
        x=('x', 'mean'),
        y=('y', 'mean'),
        z=('z', 'mean')).reset_index()

fig = plt.figure(figsize=(20,16)) 
#plt.ylabel('y', fontsize=18)
#plt.yticks(fontsize=16)
#plt.xlabel('x', fontsize=18)
#plt.xticks(fontsize=16)            

#p1 = plt.scatter(map_lai_annual_1985_1989.x, map_lai_annual_1985_1989.y,
#            c=map_lai_annual_1985_1989.lai_max_avg,vmin=0, vmax=6,cmap='YlGn',s=30,marker='s')
p1 = plt.scatter(map_annual_1985_1989.x, map_annual_1985_1989.y,
            c=map_annual_1985_1989.avgv,cmap='YlGn',vmin=0, vmax=50,s=30,marker='s')
fig.colorbar(p1, label='Plant C')

plt.title("Mean Plant C 1985-1989",fontsize=18)
plt.savefig(path + "/mean_plantc_1985_1989.png")
plt.close()

#plt.legend()
#consumption_list = ["0.0", "0.1", "0.5", "1.0", "5.0", "25", "50", "100"]
#mort_list = ["0.0", "0.1", "0.2", "0.4", "0.6", "0.8", "1.0"]
consumption_list = ["0.0", "0.1", "0.5", "1.0", "5.0", "25", "50", "100"]
mort_list = ["0.1", "0.2", "0.4", "0.6", "0.8", "1.0"]

#consumption_list = ["1.0"]
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
for year in range(1990,2016,1):
    for consumption in consumption_list:
        for mort in mort_list:
            t =  map_c_annual[(map_c_annual.year == year) & (map_c_annual.consumption == float(consumption)) & (map_c_annual.mort == float(mort))]
            if len(t) > 0:
                print(consumption + " " + mort + " " + str(year))
                fig = plt.figure(figsize=(20,16)) 
                p1 = plt.scatter(t.x, t.y,
                                 c=t.plant_c,cmap='YlGn',vmin=0, vmax=50,s=30,marker='s')
                fig.colorbar(p1, label='Plant C')

                plt.title("Plant C " + str(year) + "    Mort:" + mort + "    Consumption Coef:" + consumption,fontsize=18)
                plt.savefig(path + "/map_plantc_"+ str(year) + "_Mort_" + mort + "_Consumption_" + consumption + ".png")
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