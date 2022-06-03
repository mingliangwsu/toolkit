#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 13:56:50 2022
get strata veg ID (two stratas) for each patch from state file
@author: liuming
"""

import numpy as np
import pandas as pd
import sys 
import os
import math

#state_file_name = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/br_cali_true.state.Y1985M1D1H1.state"
#state_file_name = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/br_veg_spun_and_stable.state"
state_file_name = "/home/liuming/mnt/hydronas2/Projects/FireEarth/BullRun/br_veg_spun_and_stable.state.Y1980M1D1H1.state"
outpath = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/process_data"
outpatch_vegid_file = outpath + "/patch_xyz_zone_hillslope_stemc_1980m1d1.txt"

#state_file_name = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/cedar_world_final_fire.txt"
#outpath = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar"
#outpatch_vegid_file = outpath + "/patch_xyz_zone_hillslope.txt"

patch_vegID_lib_x = dict()
patch_vegID_lib_y = dict()
patch_vegID_lib_z = dict()

patch_zone = dict()
patch_hillslope = dict()
patch_stemc = dict()

with open(state_file_name) as f:
    patch = "-9999"
    for line in f:
        a = line.rstrip().split()
        if "zone_ID" in a:
            zone = a[0]
        if "hillslope_ID" in a:
            hillslope = a[0]
        if "patch_ID" in a:                                                    #85393 patch_ID
            patch = a[0]
            if patch != "-9999":
                if patch not in patch_zone:
                    patch_zone[patch] = zone
                if patch not in patch_hillslope:
                    patch_hillslope[patch] = hillslope
                if patch not in patch_stemc:
                    patch_stemc[patch] = 0.0
        if patch != "-9999" and "x" in a:
            patch_vegID_lib_x[patch] = a[0]
        if patch != "-9999" and "y" in a:
            patch_vegID_lib_y[patch] = a[0]
        if patch != "-9999" and "z" in a:
            patch_vegID_lib_z[patch] = a[0]
        if patch != "-9999" and "cs.live_stemc" in a:
            patch_stemc[patch] += float(a[0])
        if patch != "-9999" and "cs.dead_stemc" in a:
            patch_stemc[patch] += float(a[0])
        

with open(outpatch_vegid_file,'w') as fout:
    fout.write("patch,x,y,z,zone,hillslope,stemc\n")
    for patch in patch_vegID_lib_x:
        if patch in patch_vegID_lib_y and patch in patch_vegID_lib_z:
            fout.write(patch + "," + patch_vegID_lib_x[patch] + "," + patch_vegID_lib_y[patch] 
            + "," + patch_vegID_lib_z[patch] + "," + patch_zone[patch] + "," + patch_hillslope[patch] + "," + str('%.2f' % patch_stemc[patch]) + "\n")
print("Done!")                    
        
