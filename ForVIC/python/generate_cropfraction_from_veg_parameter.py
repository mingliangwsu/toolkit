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
if len(sys.argv) < 2:
    print("Usage:" + sys.argv[0] + "<original_veg_file> <output_fraction_file> \n")
    sys.exit(0)
    
invegfile = sys.argv[1]
outvegfile = sys.argv[2]

#reading original vegetation parameter                

orig_veg = dict() #[grid][crop] list: fraction + vegparameter(list) + lai(list)  crop:1-20000
  
with open(invegfile) as f:   
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
                if vegcode not in orig_veg[grid]:
                    orig_veg[grid][vegcode] = list()
                    orig_veg[grid][vegcode].append(a[1])
                    orig_veg[grid][vegcode].append(a[2:])
            elif len(a) == 12:
                orig_veg[grid][vegcode].append(a)
        current_line += 1
print("Finished reading veg!")

veg_list = list()

for grid in orig_veg:
    for crop in orig_veg[grid]:
        if crop not in veg_list:
            veg_list.append(crop)
            
with open(outvegfile,"w") as fout:
    fout.write("gridid,lat,lon")
    for crop in sorted(veg_list, key=sortkey, reverse=False):     
        fout.write(',' + crop)
    fout.write('\n')
    for grid in sorted(orig_veg, key=sortkey, reverse=False): 
        fout.write(grid + "," + str('%.5f' % lat_from_id(int(grid))) + "," + str('%.5f' % lon_from_id(int(grid))))
        for crop in sorted(veg_list, key=sortkey, reverse=False):
            fraction = "0.0"
            if crop in orig_veg[grid]:
                fraction = orig_veg[grid][crop][0]
            fout.write("," + fraction)
        fout.write('\n')
print("Finished!\n")

""" 
    #merge
    for grid in all_veg[region]:
        if grid in grid_list[region] and grid not in merged_veg:
            merged_veg[grid] = all_veg[region][grid]
    for grid in all_irr[region]:
        if grid in grid_list[region] and grid not in merged_irr:
            merged_irr[grid] = all_irr[region][grid]
    print('Finish merging!')

print('Start writing...')
fout_veg = open(out_veg_file,"w")
fout_irr = open(out_irr_file,"w")
for grid in sorted(merged_veg, key=sortkey, reverse=False):
    fout_veg.write(merged_veg[grid])
for grid in sorted(merged_irr, key=sortkey, reverse=False):
    fout_irr.write(merged_irr[grid])
fout_veg.close()
fout_irr.close()
"""
print('Done.\n')

    
    
        