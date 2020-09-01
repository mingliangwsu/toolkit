#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 09:12:25 2020
Generate Vegetation and irrigation parameter based on updated/calculated crop (and natural vegetation) fractions

@author: liuming
"""

# this block of code copied from https://gist.github.com/ryan-hill/f90b1c68f60d12baea81 
import sys
import os
import pandas as pd
import pysal as ps
import numpy as np


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
def lat_lon_to_id(lat,lon):    
    id = ((lat - 25 - 0.0625 / 2) // 0.0625) * 928 + (lon + 125 - 0.0625 / 2.0) / 0.0625 + 1
    return int(id)


#print("argv_len:" + str(len(sys.argv)))
if len(sys.argv) < 3:
    print("Usage:" + sys.argv[0] + "<original_veg_file> <output_mean_LAI_file>\n")
    sys.exit(0)
    
vegfile = sys.argv[1]
outfile = sys.argv[2]

lai = dict()            #[veg][month] 
lai_count = dict()      #[veg][month] 
  
with open(invegfile,"r") as f:   
    current_line = 0
    nextgrid_line = 0
    for line in f:
        a = line.rstrip().split()
        if current_line == nextgrid_line: #gridid num_veg
            grid = a[0]
            nextgrid_line += int(a[1]) * 2 + 1
            if grid not in orig_veg:
                orig_veg[grid] = dict()
        else:
            if len(a) == 8:
                vegcode = a[0] 
            elif len(a) == 12:
                if vegcode not in lai:
                    lai[vegcode] = dict()
                    lai_count[vegcode] = dict()
                for idx, val in enumerate(a):
                    if idx not in lai[vegcode]:
                        lai[vegcode][idx] = 0.0
                        lai_count[vegcode][idx] = 0
                    lai[vegcode][idx] += float(a[idx])
                    lai_count[vegcode][idx] += 1
        current_line += 1
print("Finished reading veg!")

with open(outfile,"w") as f:
    for veg in sorted(lai, key=sortkey, reverse=False):
        f.write(veg)
        for month in range(12):
            lai_mean = lai[veg][month] / float(lai_count[veg][month])
            f.write(" " + str('%.3f' % lai_mean))
        f.write("\n")
print("Done!")



    
    
        