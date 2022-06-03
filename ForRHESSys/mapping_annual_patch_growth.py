#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 01:45:46 2018

@author: liuming
"""

import numpy as np
import pandas as pd
import datetime
import sys 
import os
import math
from os import path
import statistics 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import cm

def to_date_column(year,mon,day):
    return datetime.date(int(year),int(mon),int(day))

indir = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/liudebug_output/"
prefix = "liutest_output_fire_1990"
scale = "grow_patch"
timestep = "yearly"
annual_outfile = indir + prefix + "_" + scale + "." + timestep

patch_location_file = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/auxdata/patch_location.csv"

patch_location = pd.read_csv(patch_location_file, sep=',')
growth_patch_annual = pd.read_csv(annual_outfile, sep=r"\s+")
pgrowth__with_location = growth_patch_annual.join(patch_location.set_index('patchID'), on='patchID')

year_list = pgrowth__with_location.year.unique().tolist()
map_vars = ['plant_c', 'plant_n', 'litter_c', 'soil_c', 'litter_n', 'soil_n', 'nitrate', 'sminn', 'root_depth']

max_values = dict()
min_values = dict()
for var in map_vars:
    print(var)
    maxvalue = 0.0   
    minvalue = 10000.0
    maxtemp = pgrowth__with_location[var].max()
    mintemp = pgrowth__with_location[var].min()
    if maxtemp > maxvalue:
        maxvalue = maxtemp
    if mintemp < minvalue:
        minvalue = mintemp
    if minvalue <= 0:
        minvalue = 0.000001
    #print(minvalue)
    digits_max = math.floor(math.log10(maxvalue))
    digits_min = math.floor(math.log10(minvalue))
    setymax = (int(maxvalue / (10 ** digits_max)) + 1) * (10**digits_max)
    setymin = int(minvalue / (10 ** digits_min)) * (10**digits_min)
    if (setymin <= 5 and setymax > 10) or (setymin < 0.00001):
        setymin = 0
    max_values[var] = setymax
    min_values[var] = setymin
    print("max:"+str(max_values[var])+" min:"+str(min_values[var]))
for year in year_list:
    t = pgrowth__with_location[pgrowth__with_location['year'] == year]
    for var in map_vars:
        #ax = t.plot.scatter(x='col',
        #                    y='row_bot_to_top',
        #                    c=var,
        #                    marker='s',
        #                    colormap='viridis',
        #                    linewidths=0,
        #                    s=1,
        #                    figsize=(9,8),
        #                    #xlabel='col',
        #                    #ylabel='row',
        #                    title=var+' '+str(year)
        #                    )
        #ax.set_xlabel("Col")
        #ax.set_ylabel("Row")
        
        fig, ax = plt.subplots()
        t.plot(kind='scatter', 
               x='col', 
               y='row_bot_to_top', 
               s=1, 
               c=var, 
               cmap='YlGnBu',
               vmin=min_values[var],
               vmax=max_values[var],
               #zlim=(min_values[var],max_values[var]),
               ax=ax)
        ax.set_title(str(year) + " " + var)        
        ax.set_xlabel("Col")
        ax.set_ylabel("Row")

        #plt.scatter(t['col'],t['row_bot_to_top'],t[var],cmap='jet')
        #plt.plot(t['col'],t['row_bot_to_top'],t[var])
        #plt.show()
    

print("Done!")