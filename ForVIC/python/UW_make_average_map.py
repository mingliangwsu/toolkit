#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 11:14:21 2020

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
import geopandas

outfig_path = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/results/compare_3hour_daily/compare_figures"



#from copy import deepcopy

def sortkey(x): 
    return int(x)

filename = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/results/compare_3hour_daily/compare_figures/allsim_mean.csv"
data = pd.read_csv(filename,header=0,sep=",")

for sim in range(0,2):
    #f, ax = plt.subplots(1)
    data_sim = data[data["SIM"] == sim]
    #data_sim
    gdf = geopandas.GeoDataFrame(data_sim, geometry=geopandas.points_from_xy(data_sim.LON, data_sim.LAT))
    titlem = "ET sim " + str(sim)
    gdf.plot(column="OUT_EVAP",legend=True,figsize=(12,8))
    fig_name = outfig_path + "/et_sim" + str(sim) + ".jpg"
    #f.suptitle('Liverpool LSOAs')
    plt.savefig(fig_name)
    #t.savefig(fig_name)
    #plt.show()
    