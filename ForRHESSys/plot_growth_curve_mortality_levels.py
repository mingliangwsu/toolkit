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
all_statistics_lai_annual = pd.read_csv(path + "/all_statistics_lai_annual.csv")
all_statistics_c_annual = pd.read_csv(path + "/all_statistics_c_annual.csv")
#map_lai_annual = pd.read_csv(path + "/map_lai_annual.csv")
#map_c_annual = pd.read_csv(path + "/map_c_annual.csv")


#consumption_list = ["0.0", "0.1", "0.5", "1.0", "5.0", "25", "50", "100"]
#mort_list = ["0.0", "0.1", "0.2", "0.4", "0.6", "0.8", "1.0"]
consumption_list = ["0.0", "0.1", "0.5", "1.0", "5.0", "25", "50", "100"]
mort_list = ["0.1", "0.2", "0.4", "0.6", "0.8", "1.0"]
#consumption_list = ["0.1"]
mort_list = ["1.0"]
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
for veg in veglib:
    plt.figure(figsize=(16,8)) 
    plt.ylabel('LAI', fontsize=18)
    plt.yticks(fontsize=16)
    plt.xlabel('Year', fontsize=18)
    plt.xticks(fontsize=16)            
    plt.figure(figindex)

    for consumption in consumption_list:
    #for mort in 0.0 0.5 1.0
	#for mort in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
  
        for mort in mort_list:
        #print(consumption + ":" + mort)
        #plt.title("Mortality:" + mort + "    Consumption Coef:" + consumption, fontsize=18)
        #plt.title("Mortality:" + mort, fontsize=18)
            plt.title(veglib[veg] + "    Mortality:" + mort, fontsize=18)
            t = all_statistics_lai_annual[(all_statistics_lai_annual.veg0 == veg) & (all_statistics_lai_annual.mort == float(mort)) & (all_statistics_lai_annual.consumption == float(consumption))]
            
            if len(t) > 0:
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
            
            #plt.plot(xnew, power_smooth_q05, linewidth=3)
            #plt.plot(xnew, power_smooth_q25, linewidth=3)
                plt.plot(xnew, power_smooth_md, linewidth=3, label=consumption,color=consumption_code[consumption])
                #plt.legend(loc="upper left",fontsize=12)
                plt.legend(fontsize=12)
            #plt.plot(xnew, power_smooth_q75, linewidth=3)
            #plt.plot(xnew, power_smooth_q95, linewidth=3)
            
                plt.fill_between(xnew, power_smooth_q25, power_smooth_q75, color='red', alpha=.2)
                plt.fill_between(xnew, power_smooth_q05, power_smooth_q95, color='lightsalmon', alpha=.2)
                
                #export fig
                figname = path + "/lai_veg_" + veglib[veg] + "_mort_" + mort + ".png"
                plt.savefig(figname)
                #plt.close()
            
    figindex += 1
            #plt.plot(t.year, t.lai_vegmx_median, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q05, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q25, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q75, linewidth=3)
            #plt.plot(t.year, t.lai_vegmx_q95, linewidth=3)



print("Done!")                    