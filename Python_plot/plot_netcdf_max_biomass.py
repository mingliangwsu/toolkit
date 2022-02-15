#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 17:41:19 2020

@author: liuming
"""

import xarray
import matplotlib.pyplot as plt
import matplotlib.colors
cmap = matplotlib.colors.ListedColormap(["limegreen", "gold", "crimson"])
test = ""
if test != "kamiak":
    fname = '/home/liuming/mnt/hydronas3/LiuNas3/Project/USDA_Hydro/outnc.nc'
else:
    fname = '/home/liuming/mnt/hydronas3/LiuNas3/Project/USDA_Hydro/outnc_kamiak.nc'

outdir = "/home/liuming/mnt/hydronas3/LiuNas3/Project/USDA_Hydro"
#fname = '/home/liuming/mnt/hydronas1/Projects/USDA_Water_Ag/METRIC/METRIC_output/LIT_STJ_2018_x1_y1.nc'
norm_ET = matplotlib.colors.BoundaryNorm([0,50,100,200,350,500,700,900,1100,1300,1500], 10)
norm_NDVI = matplotlib.colors.BoundaryNorm([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0], 10)

cdls = {1 : "Corn",
        24 : "WinWheat",
        36 : "Alfalfa",
        43 : "Potatoes",
        9999 : "All (Corn, WinWheat,Alfalfa,and Potatos)"}
#cdls = {36 : "Alfalfa"}

ds = xarray.open_dataset(fname)
ds = ds.where(ds.CS_DAE >= 1, other=0)

#calculate mean over time dim
#ds_timeseries = ds.mean(dim=['x','y'])
#ds_avg_map = ds.mean(dim=['time'])

plt.close('all')


vars = ["CS_BIOMASS"]
#vars = ["ETRF"]
for var in vars:
    for cdl in cdls:
        fig, axes = plt.subplots(ncols=2,figsize=(18,7))
        fig.suptitle(var + " (" + cdls[cdl] + ")",fontsize=18)
        #cdl_ds = ds.where(ds.CS_DAE >= 1 and ds.CDL == cdl,drop = True)  
        #cdl_ds = ds.where(ds.CS_DAE >= 1 and int(ds.CDL) == cdl)
        if cdl != 9999:
            cdl_ds = ds.where(ds.CDL == float(cdl))
        else:
            cdl_ds = ds
        ds_timeseries = cdl_ds.mean(dim=['x','y'])
        ds_avg_map = cdl_ds.max(dim=['time'])    
    
        ds_timeseries[var].plot(ax=axes[0])
        #ds_avg_map[var].plot(ax=axes[1],norm=norm_NDVI,cmap='YlGn')
        ds_avg_map[var].plot(ax=axes[1],cmap='YlGn')
        if test != "kamiak":
            outimage = outdir + "/fig_max_" + cdls[cdl] + "_" + var + ".png"
        else:
            outimage = outdir + "/kamiak_fig_max_" + cdls[cdl] + "_" + var + ".png"
        plt.savefig(outimage)


plt.close('all')
