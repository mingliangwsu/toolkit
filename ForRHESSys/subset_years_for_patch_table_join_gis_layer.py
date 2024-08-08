#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 01:45:46 2018

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
import subprocess

indir = "/home/liuming/mnt/hydronas3/Projects/WWS_Oregon/GateCreek_RHESSys_output/agg_sts_outputs/"
nlcds = ['2001','2021']
for nlcd in nlcds:
    datafile = f'{indir}agg_annual_max_patch_from_grow_patch.daily_{nlcd}.txt'
    allyears_data = pd.read_csv(datafile)
    for selected_year in range(2001,2022):
        sel_data = allyears_data[allyears_data['year'] == selected_year]
        outputf = f'{indir}_nlcd{nlcd}_{selected_year}.txt'
        sel_data.to_csv(outputf, index=False)



print("Done!")