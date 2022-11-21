#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 13:56:50 2022
get strata veg ID (two stratas) for each patch from state file
@author: liuming
"""

#import numpy as np
import pandas as pd
#import sys 
#import os
#import math
from os.path import exists
import copy
import matplotlib.pyplot as plt

datadir_root = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979"
#output_dir_name = "liudebug_init"
#state_file_name = "br_veg_spun_and_stable.state.Y2015M1D1H1.state.Y2015M1D1H1.state"
#state_file_name = "br_veg_spun_and_stable.state.Y2015M1D1H1.state"
state_file_name = "br_veg_spun_and_stable.state.Y2015M1D1H1.state.Y2015M1D1H1.state.11072022"
outpath = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/process_data"
outpatch_vegid_file = outpath + "/patch_init_state.txt"
fullpath_state_file_name = datadir_root + "/" + state_file_name

overwrite = True
#state_file_name = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/cedar_world_final_fire.txt"
#outpath = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar"
#outpatch_vegid_file = outpath + "/patch_xyz_zone_hillslope.txt"

patch_vegID_lib_x = dict()
patch_vegID_lib_y = dict()
patch_vegID_lib_z = dict()

patch_zone = dict()
patch_hillslope = dict()
patch_target = dict()
patch_strata_target = dict()

target_patch_vars = ["litter_cs.litr1c", "litter_ns.litr1n", "litter_cs.litr2c", "litter_cs.litr3c", 
               "litter_cs.litr4c", "soil_cs.soil1c", "soil_cs.soil2c", 
               "soil_cs.soil3c", "soil_cs.soil4c", "soil_ns.sminn", "soil_ns.nitrate", 
               "rz_storage","unsat_storage","sat_deficit","snowpack.water_equivalent_depth"]
target_strata_vars = ["cs.cpool", "cs.leafc", 
               "cs.live_stemc","cs.dead_stemc", "cs.live_crootc", 
               "cs.dead_crootc", "cs.frootc", "cs.cwdc"]
stratas = ["over","under"]

for var in target_patch_vars:
    patch_target[var] = dict()
for var in target_strata_vars:    
    patch_strata_target[var] = dict()
    for strata in stratas:
        patch_strata_target[var][strata] = dict()

if overwrite or not exists(outpatch_vegid_file):
  with open(fullpath_state_file_name) as f:
    patch = "-9999"
    readpatch = False
    readStrata = False
    for line in f:
        a = line.rstrip().split()
        if "zone_ID" in a:
            readpatch = False
            zone = a[0]
        if "hillslope_ID" in a:
            hillslope = a[0]
        if "patch_ID" in a:   
            strata_index = -1
            readpatch = True
            readStrata = False
            patch = a[0]
            if patch != "-9999":
                if patch not in patch_zone:
                    patch_zone[patch] = zone
                if patch not in patch_hillslope:
                    patch_hillslope[patch] = hillslope
                for var in target_patch_vars:
                    if patch not in patch_target[var]:
                        patch_target[var][patch] = 0.0
                for var in target_strata_vars:    
                    for strata in stratas:
                        if patch not in patch_strata_target[var][strata]:
                            patch_strata_target[var][strata][patch] = 0.0
        if "canopy_strata_ID" in a:
            strata_ID = a[0]
            readStrata = True
            strata_index += 1
        if "veg_parm_ID" in a:
            int_veg_ID = int(a[0])
        if readpatch and patch != "-9999" and "x" in a:
            patch_vegID_lib_x[patch] = a[0]
        if readpatch and patch != "-9999" and "y" in a:
            patch_vegID_lib_y[patch] = a[0]
        if readpatch and patch != "-9999" and "z" in a:
            patch_vegID_lib_z[patch] = a[0]
        if readpatch and patch != "-9999" and a[1] in target_patch_vars:
            patch_target[a[1]][patch] += float(a[0])
        if readStrata and patch != "-9999" and a[1] in target_strata_vars:
            patch_strata_target[a[1]][stratas[strata_index]][patch] += float(a[0])
            
  with open(outpatch_vegid_file,'w') as fout:
    t = "patch,x,y,z,zone,hillslope"
    for var in target_patch_vars:
        t += "," + var
    for var in target_strata_vars:
        for strata in stratas:
            t += "," + strata + "_" + var
    t += "\n"
    fout.write(t)
    
    for patch in patch_vegID_lib_x:
        if patch in patch_vegID_lib_y and patch in patch_vegID_lib_z:
            t = patch + "," + patch_vegID_lib_x[patch] + "," + patch_vegID_lib_y[patch] + "," + patch_vegID_lib_z[patch] + "," + patch_zone[patch] + "," + patch_hillslope[patch]
            for var in target_patch_vars:
                t += "," + str('%.2f' % patch_target[var][patch])
            for var in target_strata_vars:
                for strata in stratas:
                    t += "," + str('%.2f' % patch_strata_target[var][strata][patch])
            t += "\n"
            
            
            fout.write(t)
            
            
outvars = copy.deepcopy(target_patch_vars)
for var in target_strata_vars:    
    for strata in stratas:
        outvars.append(strata + "_" + var)
        
        
t = pd.read_csv(outpatch_vegid_file)
for var in outvars:
  fig = plt.figure(figsize=(20,10)) 
  #p1 = plt.scatter(t.x, t.y,c=t[var],cmap='YlGn',vmin=0, vmax=50,s=30,marker='s')
  p1 = plt.scatter(t.x, t.y,c=t[var],cmap='YlGn',s=8,marker='s')
  fig.colorbar(p1, label=var)
  plt.title(var,fontsize=18)
  #plt.close()
  plt.savefig(outpath + "/map_" + var + ".png")


print("Done!")                    
        
