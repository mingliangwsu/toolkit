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
#outpath = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/process_data"
#outpatch_vegid_file = outpath + "/patch_vegID2.txt"
#outpatch_vegid_file = outpath + "/patch_vegID2_04272022.txt"

state_file_name = "/home/liuming/mnt/hydronas3/Projects/WWS_Oregon/GateCreek_Ankit/Gatecreek_postfire/Gate_creek_postfire.world.Y2023M12D30H24.state"
outpath = "/home/liuming/mnt/hydronas3/Projects/WWS_Oregon/GateCreek_Ankit/Gatecreek_postfire"
outpatch_vegid_file = outpath + "/patch_xyz_vegid.txt"


patch_vegID_lib = dict()

with open(state_file_name) as f:
    for line in f:
        a = line.rstrip().split()
        if "patch_ID" in a:                                                    #85393 patch_ID
            patch = a[0]
            if patch not in patch_vegID_lib:
                patch_vegID_lib[patch] = list()
        if "veg_parm_ID" in a:                                                 #5 veg_parm_ID
            veg = a[0]
            patch_vegID_lib[patch].append(veg)
            if (len(patch_vegID_lib[patch]) > 2):
                print("Warning:" + str(patch) + " has more than 2 veg IDs!\n")

with open(outpatch_vegid_file,'w') as fout:
    fout.write("patch,veg0,veg1\n")
    for patch in patch_vegID_lib:
        vegs = len(patch_vegID_lib[patch])
        if vegs >= 1:
            fout.write(str(patch))
            vegindex = 0
            for veg in patch_vegID_lib[patch]:
                fout.write("," + str(veg))
            if vegs < 2:
                fout.write(",-9999")
            fout.write("\n")
print("Done!")                    
        
