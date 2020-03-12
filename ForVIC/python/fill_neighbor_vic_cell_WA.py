#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Dec. 16, 2019, LIU
Fill missing VIC grid cell in Washington state with neighboring gridcell 
@author: liuming
"""

import pandas as pd
import sys 
import os
from os import path
#from simpledbf import Dbf5 
#import geopandas as gpd

def sortkey(x): 
    return int(x)

def lat_from_id(x): 
    lat = (x // 928) * 0.0625 + 25 + 0.0625 / 2.0
    return lat

def lon_from_id(x): 
    lon = ((x - 207873) % 928) * 0.0625 + (-125.0 + 0.0625 / 2.0)
    return lon

inputdir = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/vic_soil"
outputdir = "/home/liuming/temp/UW"


dem = "wavicdem10t.csv"   
#VALUE,COUNT,WAVICALL,DEM_WA_T10

neighbor = "wavicneig.csv"
#VALUE,COUNT,BIGVICPNWG,WANEIGB

#original_soil = "soil_param.0625.PNW.052108"
original_soil = "wa_soil_original_with_head.csv"
#mask,gridcel,lat,lng,b_infilt,Ds,Dsmax,Ws,c,expt1,expt2,expt3,Ksat1,Ksat2,Ksat3,phi_s1,phi_s2,phi_s3,init_moist1,init_moist2,init_moist3,elevation,depth1,depth2,depth3,avg_temp,dp,bubble1,bubble2,bubble3,quartz1,quartz2,quartz3,bulk_density1,bulk_density2,bulk_density3,soil_density1,soil_density2,soil_density3,off_gmt,Wcr_FRACT1,Wcr_FRACT2,Wcr_FRACT3,Wpwp_FRACT1,Wpwp_FRACT2,Wpwp_FRACT3,rough,snow_rough,annual_prec,resid_moist1,resid_moist2,resid_moist3,FS_ACTIVE,avgJuly_Temp

outsoil = "wa_soil_ext_neighbor.txt"

#reading dem
vic_dem = dict()
with open(inputdir + '/' + dem) as f:
    for line in f:
        if "VALUE" not in line:
            a = line.rstrip().split(',')
            grid = a[2]
            if grid not in vic_dem:
                vic_dem[grid] = float(a[3]) / 10.0

#reading dem
vic_neighbor = dict()
with open(inputdir + '/' + neighbor) as f:
    for line in f:
        if "VALUE" not in line:
            a = line.rstrip().split(',')
            grid = a[2]
            if grid not in vic_neighbor:
                vic_neighbor[grid] = a[3]

#reading soil
vic_soil = dict()
with open(inputdir + '/' + original_soil) as f:
    for line in f:
        if "mask" not in line:
            a = line.rstrip().split(',')
            grid = a[1]
            if grid not in vic_soil:
                vic_soil[grid] = list()
            for index in range(0,len(a),1):
                vic_soil[grid].append(a[index])

vic_out_soil = dict()
for grid in vic_neighbor:
    neighbor = vic_neighbor[grid]
    #if grid == neighbor and grid in vic_soil:
    if grid == neighbor:
        vic_out_soil[grid] = vic_soil[grid].copy()
    else:
        vic_out_soil[grid] = vic_soil[neighbor].copy()
        vic_out_soil[grid][1] = grid
        vic_out_soil[grid][2] = str('%.5f' % lat_from_id(int(grid)))
        vic_out_soil[grid][3] = str('%.5f' % lon_from_id(int(grid)))
        vic_out_soil[grid][21] = str('%.2f' % vic_dem[grid])
#printout
outfile = open(outputdir + "/" + outsoil, "w")
for grid in sorted(vic_neighbor, key=sortkey, reverse=False):
    out = ""
    for index in range(0,54,1):
        out += vic_out_soil[grid][index] + " "
    out += "\n"
    outfile.write(out)


outfile.close()


#read fraction file and write to vegetation parameter file:
print("Done\n")