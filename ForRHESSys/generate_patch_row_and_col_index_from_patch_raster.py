#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
col: from left to right, starting from 1
row: from top to bottom, starting from 1
row_bot_to_top: from bottom to top, starting from 1

@author: liuming
"""

import numpy as np
import pandas as pd
import datetime
import sys 
import os
import math
from os import path
import statistics 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import cm

#wdir = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/auxdata/"
wdir = "/home/liuming/mnt/hydronas1/Projects/FireEarth/run_RHESSysPreprocessing/BRW/Input/rasters/"
#patch_raster = wdir + "patchgrid.txt"
patch_raster = wdir + "patch_100m_nohead.asc"
outfile = wdir + "patch_location_100m.csv"

rows = 0
with open(patch_raster,"r") as f:
    for line in f:
        t = line.rstrip().split(' ')
        if len(t) > 0:
            rows += 1
        if rows == 1:
            cols = len(t)
print("rows:" + str(rows) + " cols:" + str(cols))

row_index = 0
fout = open(outfile,'w')
fout.write("patchID,row,col,row_bot_to_top\n")
with open(patch_raster,"r") as f:
    for line in f:
        t = line.rstrip().split(' ')
        if len(t) > 0:
            row_index += 1
        row_from_bottom_to_top = rows - row_index + 1
        col_index = 1
        for patch_id in t:
            if patch_id != "-9999":
                fout.write(patch_id + "," + str(row_index) + "," + str(col_index) + "," + str(row_from_bottom_to_top) + "\n")
            col_index += 1
fout.close()
print("Done!")