#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 13:56:50 2022
get strata veg ID (two stratas) for each patch from state file
@author: liuming
"""
from pyproj import Proj, transform
import sys 

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
inProj = Proj(init='epsg:4326')
outProj = Proj(init='epsg:32610')    

if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1old_base_filename> <2new_base>\n")
    sys.exit(0)

with open(sys.argv[1]) as f,open(sys.argv[2],'w') as fout:
    for line in f:
        a = line.rstrip().split()
        if len(a) > 0:
          #print("line:",line)
          #print("0 torig:",torig)
          #print("0 tnew:",tnew)
          if "x_coordinate" in a:
              lon = float(a[0])
          elif "y_coordinate" in a:
              lat = float(a[0])
              x2,y2 = transform(inProj,outProj,lon,lat)
              out = str('%.1f' % x2) + " x_coordinate\n"
              fout.write(out)
              out = str('%.1f' % y2) + " y_coordinate\n"
              fout.write(out)
          else:
              fout.write(line)
print("Done!")                    
        
