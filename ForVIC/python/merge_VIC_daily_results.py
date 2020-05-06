#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar. 23, 2020, LIU
Merge daily VIC simulation results
@author: liuming
"""

import pandas as pd
import sys 
import os
import math
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

def VIC_grid_km2(lat_degree):
    area_km2 = 2.0 * ( 0.0625 * 3.14159 / 180.0 ) * 6371393 * 6371393 * math.cos(lat_degree * 3.1415926 / 180.0) * math.sin(0.0625 * 3.1415926 / 360.0) / 1000000.0
    return area_km2

if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<vic_output_dir> <output_file>\n")
    sys.exit(0)

#PNW_Klamath
vicdir = sys.argv[1]
outfile = sys.argv[2]

#areak2 = VIC_grid_km2(45.0)



#reading dem
#vic_dem = dict()
#with open(inputdir + '/' + dem) as f:
#    for line in f:
#        if "VALUE" not in line:
#            a = line.rstrip().split(',')
#            grid = a[2]
#            if grid not in vic_dem:
#                vic_dem[grid] = float(a[3]) / 10.0

        
#printout
outfile = open(outfile, "w")

for filename in os.listdir(vicdir):
  if 'flux' in filename: 
      print(filename)
      
#for grid in sorted(vic_neighbor, key=sortkey, reverse=False):
#    out = ""
#    for index in range(0,16,1):
#        out += vic_out_soil[grid][index] + " "
#    out += "\n"
#    outfile.write(out)


outfile.close()
#read fraction file and write to vegetation parameter file:
print("Done\n")