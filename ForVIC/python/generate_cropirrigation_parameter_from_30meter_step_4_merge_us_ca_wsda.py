#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 09:12:25 2020
Merge Canada, US, and WSDA vegetation and irrigation parameter
Output: VIC vegetation and irrigation parameter

@author: liuming
"""

# this block of code copied from https://gist.github.com/ryan-hill/f90b1c68f60d12baea81 
import pandas as pd
import pysal as ps
import numpy as np

def sortkey(x): 
    return int(x)

datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/irrigation/"
out_veg_file = datapath + "pnw_veg_parameter.txt"
out_irr_file = datapath + "pnw_irrigation.txt"

regions = ['wsda','us','ca']
all_veg = dict() #[region][grid]
all_irr = dict() #[region][grid]
grid_list = dict() #[region]

merged_veg = dict() #[grid]
merged_irr = dict() #[grid]

for region in regions:
    print(region)
    all_veg[region] = dict()
    all_irr[region] = dict()
    grid_list[region] = list()
    
    vegfile = datapath + region + "_veg_parameter.txt"  
    irrfile = datapath + region + "_irrigation.txt"
    gridfile = datapath + "vic_in_" + region + ".csv" 
    
    #read grid list
    with open(gridfile) as f:
        for line in f:
            a = line.rstrip().split()
            if len(a) > 0:
                grid_list[region].append(a[0])
    print('Done grid list.\n')
    
    
    #read veg information
    with open(vegfile) as f:   
        current_line = 0
        nextgrid_line = 0
        for line in f:
            a = line.rstrip().split()
            if current_line == nextgrid_line:
                grid = a[0]
                nextgrid_line += int(a[1]) * 2 + 1
                if grid not in all_veg[region]:
                    all_veg[region][grid] = ""
                all_veg[region][grid] += line
            else:
                all_veg[region][grid] += line
            current_line += 1
    print("finished reading veg!")
    
    #read irri information
    with open(irrfile) as f:   
        current_line = 0
        nextgrid_line = 0
        for line in f:
            a = line.rstrip().split()
            if current_line == nextgrid_line:
                grid = a[0]
                nextgrid_line += int(a[1]) + 1
                if grid not in all_irr[region]:
                    all_irr[region][grid] = ""
                all_irr[region][grid] += line
            else:
                all_irr[region][grid] += line
            current_line += 1
    print("finished reading irr!")
    
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

print('Done.\n')

    
    
        