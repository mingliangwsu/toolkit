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
              fout.write(out)
          elif len(a) == 2:
              if a[0] == selected:
                  find = True
                  out = line
                  fout.write(out)
              else:
                  find = False
          elif len(a) > 2:
              if find:
                  out = line
                  fout.write(out)
print("Done!")                    
        
