#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 1 2022
Calculate model performance on NPP/GPP ratio
@author: liuming
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
import os
from os.path import exists
import math
import scipy.stats

#from scipy.interpolate import make_interp_spline, BSpline
#from scipy.ndimage.filters import gaussian_filter1d

if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<growth_year_file> <valid_start_year> <valid_end_year> <valid_veg_id> <target> <target_stddev> <outdist_file>\n")
    sys.exit(0)
    
growth_year = sys.argv[1] 
#"/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/Outputs/spinup_fire__grow_stratum.yearly"
valid_start_year = int(sys.argv[2]) 
# = 1990
valid_end_year = int(sys.argv[3]) 
# = 2018
valid_veg_id = int(sys.argv[4]) 
# = 1
target = float(sys.argv[5]) 
target_stddev = float(sys.argv[6]) 
# = 0.5
outdist = sys.argv[7] 
#"/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/Outputs/dist_npp_gpp_ratio.txt"


patch_stata_veg = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/patch_stratum_vegid.txt"

patch_strata = pd.read_csv(patch_stata_veg,delimiter=",",header=0)
growth = pd.read_csv(growth_year,delimiter=" ",header=0)
growth['gpp'] = growth['psn_net'] + growth['mr'] + growth['gr']
growth['npp_gpp_ratio'] = growth['psn_net'] / growth['gpp']

growth = pd.merge(growth, patch_strata, left_on=  ['patchID', 'stratumID'],right_on= ['patch_ID', 'strata_ID'], how = 'left')

avg = growth[(growth['veg_parm_ID'] == valid_veg_id) & (growth['year'] >= valid_start_year) & (growth['year'] <= valid_end_year)]['npp_gpp_ratio'].mean()
#sys.exit((avg-target)*(avg-target))
#dist = abs(avg-target)

#likelyhood
#mean ratio 0.5 95%:0.4-0.6    stddev=0.051
dist = scipy.stats.norm.pdf(avg,loc=target,scale=target_stddev)

with open(outdist, 'w') as fh:
    fh.write(str('%.6f' % dist) + '\n')