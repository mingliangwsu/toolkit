#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on  Jan. 14, 2019
Convert crop fractions into VIC veg parametger files for running VIC-CropSyst V2 (Forecast project)
@author: liuming

Check if one subbasin is totally contained by another subbasin, if partially contained, print error; otherwise printing information showing which subbasin is contained by which watershed
Kinds of hard coded for one-time thing.

"""

import pandas as pd
import sys 
import os

basin_outlets_filename = '/mnt/hydronas/Projects/BPA_CRB/GIS/final_selected_gauges_for_calibration_info.csv'
basins_dir = '/mnt/hydronas/Projects/BPA_CRB/GIS/VIC_basins'

outinfo_file = '/home/liuming/temp/temp/calibration_subbasins_spatial_relationships.txt'

#if len(sys.argv) != 4:
#    print("Usage:" + sys.argv[0] + "<original_soil_parameter_file> <new_sub_set> <out_new_soil_parameter_file>\n")
#    sys.exit(0)

#orig_soil_parameter_file = sys.argv[1]
#subset_soil_parameter_file = sys.argv[2]
#new_orig_soil_parameter_file = sys.argv[3]

#get outlets
subbasins = list()
#read soil parameter to create location dictionary
with open(basin_outlets_filename) as f:
    for line in f:
        a = line.split(',')
        if len(a) > 0 and 'data_source' not in line:
            subbasins.append(a[2])
            #print("viccell:" + a[2])
            #print(location + ':' + cellid)
print("reading subset soil done!")

outfile = open(outinfo_file,"w")

#subbasins = ['360182','311055']
for outlet in subbasins:
    basinfile = basins_dir + '/w' + outlet + '.txt'
    print('current basin:' + basinfile)
    current_cells = list()
    with open(basinfile) as f:
        for line in f:
            a = line.split()
            if len(a) > 0:
                current_cells.append(a[0])
                #print('cell:' + a[0])
    for other_basin in subbasins:
        if outlet != other_basin:
            compbasinfile = basins_dir + '/w' + other_basin + '.txt'
            print('commpare basin:' + compbasinfile)
            target_cells = list()
            with open(compbasinfile) as f:
                for line in f:
                    a = line.split()
                    if len(a) > 0:
                        target_cells.append(a[0])
                        #print('tar_cell:' + a[2])
            #check all current cells is contained by target basin
            if len(current_cells) < len(target_cells):
                contained = True
                for ccells in current_cells:
                    if ccells not in target_cells:
                        contained = False
                        print(outlet + " not inside " + other_basin)
                        break
                if contained == True:
                    outfile.write(outlet + " inside " + other_basin + '\n')
                    print(outlet + " inside " + other_basin)
                
print('Done!\n')
outfile.close()
    
"""
outfile_soil = open(new_orig_soil_parameter_file,"w")

with open(orig_soil_parameter_file) as f:
    for line in f:
        a = line.split()
        if len(a) > 0:
            cellid = a[1]
            if cellid in subset_soil_dic:
                outline = subset_soil_dic[cellid]
            else:
                outline = line
            outfile_soil.write(outline)
outfile_soil.close()
print("Done!")
"""