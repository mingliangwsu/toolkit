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

#indir = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/liudebug_output/"

target_year = "1999"

#scale = "patch"
#target_var = "lai"
#timestep = "monthly"
#ccmap='YlGn'

scale = "grow_patch"
target_var = "plant_c"
timestep = "yearly"
ccmap = 'viridis_r'

figure_outdir = "/home/liuming/mnt/hydronas3/Projects/NASA_Mariana/Bullrun"

indir = "/home/liuming/mnt/hydronas2/Projects/UI_NASA_Bullrun/b" + target_year + "/"
prefix = "b" + target_year
#scale = "patch"

outfile = indir + prefix + "_" + scale + "." + timestep

#patch_location_file = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/auxdata/patch_location.csv"
patch_location_file = "/home/liuming/mnt/hydronas1/Projects/FireEarth/run_RHESSysPreprocessing/BRW/Input/rasters/patch_location_100m.csv"


patch_location = pd.read_csv(patch_location_file, sep=',')
df_raw = pd.read_csv(outfile, sep=r"\s+")


df_sts = df_raw.groupby(['year','patchID'], as_index=False).max()
sel_sts = df_sts[['patchID','year',target_var]]

#join location
df_with_location = sel_sts.join(patch_location.set_index('patchID'), on='patchID')

year_list = df_with_location.year.unique().tolist()
map_vars = [target_var]

max_values = dict()
min_values = dict()
for var in map_vars:
    print(var)
    maxvalue = 0.0   
    minvalue = 10000.0
    maxtemp = df_with_location[var].max()
    mintemp = df_with_location[var].min()
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
    t = df_with_location[df_with_location['year'] == year]
    for var in map_vars:
        if var == 'lai':
            max_values[var] = 12
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
        
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
        t.plot(kind='scatter', 
               x='col', 
               y='row_bot_to_top', 
               s=1, 
               c=var, 
               cmap=ccmap, #'YlGnBu',
               vmin=min_values[var],
               vmax=max_values[var],
               #zlim=(min_values[var],max_values[var]),
               ax=ax)
        ax.set_title(f'B{target_year} {var} ({year})')        
        ax.set_xlabel("Col")
        ax.set_ylabel("Row")
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel(None)
        ax.set_ylabel(None)

        outpng = f'{figure_outdir}/map_B{target_year}_{target_var}_{year}.png'
        plt.savefig(outpng,bbox_inches='tight', pad_inches=0.1, dpi=600)
        #plt.scatter(t['col'],t['row_bot_to_top'],t[var],cmap='jet')
        #plt.plot(t['col'],t['row_bot_to_top'],t[var])
        #plt.show()
    

print("Done!")

