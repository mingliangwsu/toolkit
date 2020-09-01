#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June. 23, 2020, LIU
List VIC grid id from weather data file
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

#if len(sys.argv) <= 1:
#    print("Usage:" + sys.argv[0] + "<weather_data_file_path_with_backslash> <VIC_soil_filename> <output_gridcell_id_list>\n")
#    sys.exit(0)

#PNW_Klamath
#weatherdir = sys.argv[1]
#vic_soil = sys.argv[2]
#out_vic_list = sys.argv[3]
    
weatherdir = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Weather"
vic_soil = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Parameters_for_Linux_site_testrun/parameters/Database/Soil/all_calibrated_plus_uncalibrated_soil.txt"
out_vic_list = weatherdir + "/vic_list.txt"

#printout
outfile = open(out_vic_list, "w")

for filename in os.listdir(weatherdir):
  if 'data' in filename: 
      names = filename.rstrip().split("_")
      lat = names[1]
      lon = names[2]
      with open(vic_soil) as fvic:
          for line in fvic:
              a = line.rstrip().split()
              if lat == a[2] and lon == a[3]:
                  outfile.write(a[1] + " " + lat + " " + lon + "\n")
      print(names)
outfile.close()
      
      
#for grid in sorted(vic_neighbor, key=sortkey, reverse=False):
#    out = ""
#    for index in range(0,16,1):
#        out += vic_out_soil[grid][index] + " "
#    out += "\n"
#    outfile.write(out)


#read fraction file and write to vegetation parameter file:
print("Done\n")