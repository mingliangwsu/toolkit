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

def to_date_column(year,mon,day):
    return datetime.date(int(year),int(mon),int(day))

indir = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/liudebug_output/"
prefix = "liutest_output_fire_1990"
annual_mean_outfile = indir + "Annual_mean_from_daily_all_patches_grow_patch.txt"
patch_raster_file =  

#modelout_file = indir + prefix + '_' + output
#flowtable = indir + '/br_cali_true.flow'
#outfile = indir + "/flow_patchinfo.txt"
#fout = open(outfile,"w")
#fout.write("patch_ID zone_ID hill_ID x y z area area drainage_type gamma num_neighbours\n")
#with open(flowtable) as f:
#    for line in f:
#        vars = line.rstrip().split(' ')
#        if len(vars) == 11:
#            fout.write(line)

annual_data = pd.read_csv(annual_mean_outfile, sep=',')
#outdata['date'] = outdata.apply(lambda x: to_date_column(x.year,x.month,x.day), axis=1)
#outdata['literc'] = outdata['litr1c'] + outdata['litr2c'] + outdata['litr3c'] + outdata['litr4c']
#outdata['litern'] = outdata['litr1n'] + outdata['litr2n'] + outdata['litr3n'] + outdata['litr4n']
#outdata['soilc'] = outdata['soil1c'] + outdata['soil2c'] + outdata['soil3c'] + outdata['soil4c']
#outdata['soiln'] = outdata['soil1n'] + outdata['soil2n'] + outdata['soil3n'] + outdata['soil4n']
#outdata['soil_DIN'] = outdata['soilNO3'] + outdata['soilNH4']
#outdata['totc'] = outdata['plantc'] + outdata['literc'] + outdata['soilc']
#outdata['totorgn'] = outdata['plantn'] + outdata['litern'] + outdata['soiln']

#outdata_annual = outdata.groupby(['year','patchID'],as_index=False).mean()
#outdata_annual['date'] = outdata_annual.apply(lambda x: to_date_column(x.year,x.month,x.day), axis=1)
#outdata_annual.to_csv(annual_mean_outfile, index=False)

#del outdata
print("Done!")