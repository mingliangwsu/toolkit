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

def sortkey(x): 
    return int(x)



#state_file_name = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/br_cali_true.state.Y1985M1D1H1.state"
#state_file_name = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/br_veg_spun_and_stable.state"
#outpath = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/process_data"
#outpatch_vegid_file = outpath + "/patch_vegID2.txt"
#outpatch_vegid_file = outpath + "/patch_vegID2_04272022.txt"

#state_file_name = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/cedar_world_final_fire.txt"
#outpath = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar"
state_file_name = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/br_veg_spun_and_stable.state"
outpath = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979"
outpatch_vegid_file = outpath + "/patch_stratum_vegid.txt"


patch_vegID_lib = dict()

with open(state_file_name) as f:
    for line in f:
        a = line.rstrip().split()
        if "patch_ID" in a:
            patch = a[0]
            if patch not in patch_vegID_lib:
                patch_vegID_lib[patch] = dict()
        if "canopy_strata_ID" in a:                                                    #85393 patch_ID
            strata = a[0]
        if "veg_parm_ID" in a:                                                 #5 veg_parm_ID
            veg = a[0]
            if strata not in patch_vegID_lib[patch]:
                patch_vegID_lib[patch][strata] = veg

with open(outpatch_vegid_file,'w') as fout:
    fout.write("patch_ID,strata_ID,veg_parm_ID\n")
    for patch in sorted(patch_vegID_lib, key=sortkey, reverse=False):
        for strata in sorted(patch_vegID_lib[patch], key=sortkey, reverse=False):
            fout.write(str(patch) + ',' + strata + ',' + patch_vegID_lib[patch][strata] + '\n')
            
print("Done!")                    
        
