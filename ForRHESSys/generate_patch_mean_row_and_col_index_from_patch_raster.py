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
patch_raster = wdir + "patch_100m.asc"
outfile = wdir + "test_patch_location.csv"

rows = 0
with open(patch_raster,"r") as f:
    for line in f:
        t = line.rstrip().split()
        if len(t) > 2:   #Assume cols > 2
            rows += 1
            if rows == 1:
                cols = len(t)
print("rows:" + str(rows) + " cols:" + str(cols))

Colums = {
    "patchID": "int32",
    "row": "int32",
    "col": "int32",
    "row_bot_to_top": "int32"
    }
patchdf = pd.DataFrame({col: pd.Series(dtype=dt) for col, dt in Colums.items()})

row_index = 0
with open(patch_raster,"r") as f:
    for line in f:
        t = line.rstrip().split()
        if len(t) > 2:
            row_index += 1
            row_from_bottom_to_top = rows - row_index + 1
            col_index = 1
            for patch_id in t:
                if patch_id != "-9999":
                    #fout.write(patch_id + "," + str(row_index) + "," + str(col_index) + "," + str(row_from_bottom_to_top) + "\n")
                    Row = {
                        "patchID": patch_id,
                        "row": row_index,
                        "col": col_index,
                        "row_bot_to_top": row_from_bottom_to_top
                    }
                    patchdf.loc[len(patchdf)] = Row
                col_index += 1

#get the average of location for each patch
grouped_mean = patchdf.groupby('patchID', as_index = False).mean()
grouped_mean['row'] = grouped_mean['row'].round(0).astype(int)
grouped_mean['col'] = grouped_mean['col'].round(0).astype(int)
grouped_mean['row_bot_to_top'] = grouped_mean['row_bot_to_top'].round(0).astype(int)
grouped_mean.to_csv(outfile,index = False)

print("Done!")