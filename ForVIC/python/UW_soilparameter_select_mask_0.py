#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar. 19, 2020, LIU
Update climate information and soil parameters from gNATSGO data sets.
@author: liuming
"""

original_soil_file = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/vic_soil/wa_soil_ext_neighbor_gNATSGO.txt"
out_soil_parameter_file = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/vic_soil/wa_missing_mask_0.txt"

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

def id_from_lat_lon(xlon,ylat): 
    id = ((ylat - 25 - 0.0625 / 2.0) // 0.0625) * 928 + (xlon + 125 - 0.0625 / 2.0) / 0.0625 + 1
    return id


#reading original VIC (filled missing data with neighboring cells)
vic_dic = dict()
of = open(out_soil_parameter_file,"w")
with open(original_soil_file) as f:
    for line in f:
        if "VALUE" not in line:
            a = line.rstrip().split()
            mask = int(a[0])
            if mask == 0:
                of.write("1")
                for i in range(len(a)):
                    if i >= 1:
                        of.write(" " + a[i])
                of.write("\n")
of.close()




#read fraction file and write to vegetation parameter file:
print("Done\n")