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
    print("Usage:" + sys.argv[0] + "<1flow_filename> <2error_report>\n")
    sys.exit(0)

in_file = sys.argv[1]
out_file = sys.argv[2]
with open(in_file) as f,open(out_file,'w') as fout:
    for line in f:
        a = line.rstrip().split()
        out = ""
        if len(a) == 2:
            phill = a[0]
        if len(a) > 5:
          patch = a[0]
          zone = a[1]
          hill = a[2]
        elif len(a) == 4:
          tp = a[0]
          tz = a[1]
          th = a[2]
          if (phill != hill or phill != th or hill != th):
              out = "patch:" + patch + " of hill " + hill + " contains outside neighbors: " + tp + " of hill " + th 
              fout.write(out)
          #print("2 torig:",torig)
          #print("2 tnew:",tnew)

print("Done!")                    
        
