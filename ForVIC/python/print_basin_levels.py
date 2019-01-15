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
basin_contain_file = '/mnt/hydronas/Projects/BPA_CRB/GIS/calibration_subbasins_spatial_relationships.txt'
outlevel_file = '/home/liuming/temp/temp/basin_levels.txt'
basin_contains_file = '/home/liuming/temp/temp/basin_containing_subbasins.txt'

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
print("reading basins done!")

basin_sublist= dict()
#create all subbasin list for each subbasins
for outlet in subbasins:
    temp = list()
    basin_sublist[outlet] = temp

#get basin contain information
#left = list()
#right = list()
with open(basin_contain_file) as f:
    for line in f:
        a = line.split(' ')
        if len(a) > 0:
            #left.append(a[0])
            #right.append(a[2])
            cell = a[2].rstrip()
            if a[0] not in basin_sublist[cell]:
                basin_sublist[cell].append(a[0])
            #print("viccell:" + a[2])
            #print(location + ':' + cellid)
print("reading basin contain info done!")

outfile = open(outlevel_file,"w")

#get level 0 at first
#subbasins = ['360182','311055']
alllevel = dict()
temp = list()
leveled_cells = list()
for outlet in subbasins:
    if len(basin_sublist[outlet]) == 0:
        temp.append(outlet)
        leveled_cells.append(outlet)
        print(outlet + ' is 0 level')
        outfile.write('0:' + outlet + '\n')
print('level 0 is done')

#iterate to generate all levels
alllevel[0] = temp
level = 1
MAX = 50
uplevel = list()
while level < MAX:
    uplevel.extend(alllevel[level-1])
    alllevel[level] = list()
    for outlet in subbasins:
        this_level = True
        for sub in basin_sublist[outlet]:
            if sub not in uplevel:
                this_level = False
                break
        if this_level == True and len(basin_sublist[outlet]) > 0 and outlet not in leveled_cells:
            alllevel[level].append(outlet)
            leveled_cells.append(outlet)
            print(outlet + ' is ' + str(level) + ' level')
            outfile.write(str(level) + ':' + outlet + '\n')
    level += 1

#output basin and subbasin contain info
outfile_basinsub = open(basin_contains_file,"w")
for basin in basin_sublist:
    outfile_basinsub.write(basin + ":")
    if len(basin_sublist[basin]) > 0:
        outfile_basinsub.write(" ")
        for cell in basin_sublist[basin]:
            outfile_basinsub.write(cell + " ")
    outfile_basinsub.write("\n")

print('Done!\n')
outfile.close()
outfile_basinsub.close()
