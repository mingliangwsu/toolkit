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

def match_y_to_x(x,y):
    t = 1
    for idx,yi in enumerate(y):
       if idx < len(x):
           if yi == x[idx]:
               t *= 1
           else:
               t = 0
    return (t == 1)

#state_file_name = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/br_cali_true.state.Y1985M1D1H1.state"
#state_file_name = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/br_veg_spun_and_stable.state"
#outpath = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/process_data"
#outpatch_vegid_file = outpath + "/patch_vegID2.txt"
#outpatch_vegid_file = outpath + "/patch_vegID2_04272022.txt"
    
import sys 
import random
import copy

if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1flow_filename> <2out_subset> <hillslope_ID>\n")
    sys.exit(0)

in_file = sys.argv[1]
out_file = sys.argv[2]
selected = sys.argv[3]
find = False
with open(in_file) as f,open(out_file,'w') as fout:
    for line in f:
        a = line.rstrip().split()
        out = ""
        if len(a) > 0:
          #print("line:",line)
          #print("0 torig:",torig)
          #print("0 tnew:",tnew)
          if len(a) == 1:
              out = "1\n"
          elif len(a) == 2:
              if a[0] == selected:
                  find = True
                  out = line
          elif len(a) > 2:
              if a[2] == selected:
                  out = line
        if out != "":
                    #print(out)
            fout.write(out)
          #print("2 torig:",torig)
          #print("2 tnew:",tnew)
"""                
            if a[0] == sys.argv[3]:
                fout.write(line)
        if ("num_basins" in a) and inlevel == 1:
            if numlevels["basin_ID"] == 1:
                out = "1" + whitespace + "num_basins" + "\n"
            else:
                out = line
            fout.write(out)
        if "basin_ID" in a:
            inlevel = 2
            if a[0] == sys.argv[4]:
                fout.write(line)
        if inlevel == 2:
            if "num_hillslopes" not in a:
                fout.write(line)
            else:
                if numlevels["hillslope_ID"] == 1:
                    out = "   1" + whitespace + "num_hillslopes" + "\n"
                else:
                    out = line
                fout.write(out)
        if "hillslope_ID" in a:
            inlevel = 3
            
                
                
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
"""            
print("Done!")                    
        
