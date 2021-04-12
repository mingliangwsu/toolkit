#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 10:30:45 2020

@author: liuming
"""

import pandas as pd
import sys 
import os
import math
import re
from os import path
import matplotlib
import matplotlib.pyplot as plt



#from copy import deepcopy

def sortkey(x): 
    return int(x)

modes = ["daily","hourly"]
vic_path = dict()
vic_path["daily"] = "/home/liuming/mnt/hydronas2_ftp/data/UW_culvert_project/VIC_results/vic20200820"
vic_path["hourly"] = "/home/liuming/mnt/hydronas2/Projects/UW_subcontract/daily/pnnl_historical"
outfig_path = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/results/compare_3hour_daily/compare_figures"

simindex = 4
filename = "flux_47.59375_-121.53125"

daily_columns = ["YEAR","MONTH","DAY","OUT_PREC","OUT_WIND","OUT_REL_HUMID","OUT_VP", \
                 "OUT_AIR_TEMP","OUT_SHORTWAVE","OUT_PET_SHORT","OUT_RAINF","OUT_SNOWF",
                 "OUT_SNOW_DEPTH","OUT_SWE","OUT_DELSWE","OUT_SNOW_MELT","OUT_SUB_SNOW", \
                 "OUT_EVAP","OUT_RUNOFF","OUT_BASEFLOW","OUT_SOIL_MOIST_0","OUT_SOIL_MOIST_1","OUT_SOIL_MOIST_2"]
data = dict()
year_month = dict()
month = dict()
index = 0
for mode in modes:
    plt.figure(index)
    
    for simindex in range(0,40):
        dfile = vic_path[mode] + "/sim" + str(simindex) + "/" + filename
        if mode == "daily":
            data[mode] = pd.read_csv(dfile,sep="\t",skiprows=6,names=daily_columns,header=None)
            titlemessage = "daily simulation"
        else:
            data[mode] = pd.read_csv(dfile,header=0,sep="\t")
            titlemessage = "3-hour simulation"
        data[mode]["tot_runoff"] = data[mode]["OUT_RUNOFF"] + data[mode]["OUT_BASEFLOW"]
        year_month[mode] = data[mode][data[mode]["YEAR"] >= 1983].groupby(["YEAR","MONTH"]).sum().reset_index()
        year_month[mode] = year_month[mode].drop(columns=["DAY"])

        month[mode] = year_month[mode].groupby(["MONTH"]).mean().reset_index()
        month[mode] = month[mode].drop(columns=["YEAR"])
    
    
    
    #plt.ylim=[0,3.5]

        ax = month[mode]["OUT_EVAP"].plot(color="blue")
        ax.set_ylim(0, 120)
        ax.set(xlabel="Month",ylabel="ET (mm/month)",title=titlemessage)

        ax2 = month[mode]["tot_runoff"].plot(secondary_y=True,color="orange")
        ax2.set_ylim(0, 1000)
        ax2.set(ylabel="tot_runoff (mm/month)")
    #ax2.set_ylable("tot_runoff")
    #fig = ax.get_figure()
    #plt.show()
    index += 1
