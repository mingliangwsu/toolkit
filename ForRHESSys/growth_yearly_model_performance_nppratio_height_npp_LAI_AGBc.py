#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 1 2022
Calculate model performance on NPP/GPP ratio
@author: liuming
"""

#import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
import sys 
#import os
#from os.path import exists
#import math
import scipy.stats

#from scipy.interpolate import make_interp_spline, BSpline
#from scipy.ndimage.filters import gaussian_filter1d

if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<growth_year_file> <valid_start_year> <valid_end_year> <valid_veg_id> <patch_stratum_vegid_file> <target1> <target_stddev1> ... <outdist_file> <out_record_file>\n")
    sys.exit(0)
print(f'leng_args:{len(sys.argv)}')    
#target0:npp/gpp ratio  
#target1:height (m)
#target2:npp  (kgC/year)
#target3:LAI  (m2/m2)
#target4:ABGc  (kgC)
    
numtargets =  int((len(sys.argv) - 8) / 2)
outdist = sys.argv[len(sys.argv)-2]
outrecords = sys.argv[len(sys.argv)-1]
outflog = open(outrecords, "a")
outflog.write("numtargets :" + str(numtargets) + "\n")   
#print(sys.argv)
 
growth_year = sys.argv[1] 
#"/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/Outputs/spinup_fire__grow_stratum.yearly"
valid_start_year = int(sys.argv[2]) 
# = 1990
valid_end_year = int(sys.argv[3]) 
# = 2018
valid_veg_id = int(sys.argv[4]) 
patch_stata_veg = sys.argv[5] 
# = 1
target = dict()
target_stddev = dict()

for t in range(numtargets):
    idx = 6 + t * 2
    target[t] = float(sys.argv[idx]) 
    target_stddev[t] = float(sys.argv[idx+1])
    #print("targets :" + str(t) + " target:" + str(target[t]) + " std_dev:" + str(target_stddev[t]))   
    
# = 0.5


#"/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/Outputs/dist_npp_gpp_ratio.txt"


#patch_stata_veg = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/patch_stratum_vegid.txt"

patch_strata = pd.read_csv(patch_stata_veg,delimiter=",",header=0)
growth = pd.read_csv(growth_year,delimiter=" ",header=0)
growth['gpp'] = growth['psn_net'] + growth['mr'] + growth['gr']
growth['npp_gpp_ratio'] = growth['psn_net'] / growth['gpp']

growth = pd.merge(growth, patch_strata, left_on=  ['patchID', 'stratumID'],right_on= ['patch_ID', 'strata_ID'], how = 'left')

avg = dict()
dist = dict()
tdist = 1.0
for t in range(numtargets):
    if t == 0:
        avg[t] = growth[(growth['veg_parm_ID'] == valid_veg_id) & (growth['year'] >= valid_start_year) & (growth['year'] <= valid_end_year)]['npp_gpp_ratio'].mean()
    elif t == 1:
        avg[t] = growth[(growth['veg_parm_ID'] == valid_veg_id) & (growth['year'] >= valid_start_year) & (growth['year'] <= valid_end_year)]['height'].mean()
    elif t == 2:
        avg[t] = growth[(growth['veg_parm_ID'] == valid_veg_id) & (growth['year'] >= valid_start_year) & (growth['year'] <= valid_end_year)]['psn_net'].mean()
    elif t == 3:
        avg[t] = growth[(growth['veg_parm_ID'] == valid_veg_id) & (growth['year'] >= valid_start_year) & (growth['year'] <= valid_end_year)]['LAI'].mean()
    elif t == 4:
        avg[t] = growth[(growth['veg_parm_ID'] == valid_veg_id) & (growth['year'] >= valid_start_year) & (growth['year'] <= valid_end_year)]['AGBc'].mean()
    #likelyhood
    #mean ratio 0.5 95%:0.4-0.6    stddev=0.051
    
    dist[t] = scipy.stats.norm.pdf(avg[t],loc=target[t],scale=target_stddev[t])
    tdist = tdist * dist[t]
    #print("targets:" + str(t) + " avg:" + str(avg[t]) + " target_value:" + str(target[t]) + " std_dev:" + str(target_stddev[t]) + " dist:" + str(dist[t]) + " tdist:" + str(tdist))
    outflog.write("targets:" + str(t) + " avg:" + str('%.4f' % avg[t]) + " target_value:" + str('%.4f' % target[t]) + " std_dev:" + str('%.4f' % target_stddev[t]) + " dist:" + str('%.4f' % dist[t]) + " tdist:" + str('%.4f' % tdist) + "\n")   

with open(outdist, 'w') as fh:
    #fh.write(str('%.12f' % tdist) + '\n')
    fh.write(str("{0:.2E}".format(tdist)) + '\n')
