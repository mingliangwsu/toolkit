#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 13:56:50 2022
get strata veg ID (two stratas) for each patch from state file
@author: liuming
"""

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
    

if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1world_state_filename> <2out_subset> <3world_id> <4basin_ID> <5hillslope_ID> <6zone_ID> <7patch_ID> <8canopy_strata_ID>\n")
    sys.exit(0)

print(sys.argv[1])

levels = {"world_id" : 0,
          "basin_ID" : 0,
          "hillslope_ID" : 0,
          "zone_ID" : 0,
          "patch_ID" : 0,
          "canopy_strata_ID" : 0}
    
numlevels = {"num_basins" : 0,
          "num_hillslopes" : 0,
          "num_zones" : 0,
          "num_patches" : 0,
          "num_canopy_strata" : 0}


#print("argv[2]:" + sys.argv[2])



if len(sys.argv) >= 4:
    levels["world_id"] = 1
if len(sys.argv) >= 5:
    levels["basin_ID"] = 1
    numlevels["num_basins"] = 1
if len(sys.argv) >= 6:
    levels["hillslope_ID"] = 1
    numlevels["num_hillslopes"] = 1
if len(sys.argv) >= 7:
    levels["zone_ID"] = 1
    numlevels["num_zones"] = 1
if len(sys.argv) >= 8:
    levels["patch_ID"] = 1
    numlevels["num_patches"] = 1
if len(sys.argv) >= 9:
    levels["canopy_strata_ID"] = 1
    numlevels["num_canopy_strata"] = 1


state_file = sys.argv[1]
out_file = sys.argv[2]

target = list()
for i in range(3,len(sys.argv)):
    target.append(sys.argv[i])

#t2 = ["1","1","356","79708","797088","1","1"]
t2 = ["1","1"]

t = match_y_to_x(target,t2)

whitespace = " " * 30

nums = ["num_basins","num_hillslopes","num_zones","num_patches","num_canopy_strata"]

torig = list()
tnew = list()

with open(state_file) as f,open(out_file,'w') as fout:
    for line in f:
        a = line.rstrip().split()
        if len(a) > 0:
          #print("line:",line)
          #print("0 torig:",torig)
          #print("0 tnew:",tnew)
          if "world_id" in a:
              t = len(torig) - 0;
              for i in range(t):
                  torig.pop()
                  
              torig.append(a[0])
          if "basin_ID" in a:
              t = len(torig) - 1;
              for i in range(t):
                  torig.pop()

              torig.append(a[0])
          if "hillslope_ID" in a:
              t = len(torig) - 2;
              for i in range(t):
                  torig.pop()

              torig.append(a[0])
          if "zone_ID" in a:
              t = len(torig) - 3;
              for i in range(t):
                  torig.pop()
              torig.append(a[0])
          if "patch_ID" in a:
              t = len(torig) - 4;
              for i in range(t):
                  torig.pop()
              torig.append(a[0])
          if "canopy_strata_ID" in a:
              t = len(torig) - 5;
              for i in range(t):
                  torig.pop()
              torig.append(a[0])  
          #print("1 torig:",torig)  
          if (match_y_to_x(target,torig)):
                #tnew = torig[:]
                if (a[1] not in nums):
                    fout.write(line)
                else:
                    if numlevels[a[1]] == 1:
                        tw = len(line) - len(line.lstrip())
                        out = " " * tw + "1" + whitespace + a[1] + "\n"
                    else:
                        out = line
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
        
