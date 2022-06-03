#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 01:45:46 2018

@author: liuming
"""

import pandas as pd
import os
import glob
import sys

#indir = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979"
#flowtable = indir + '/br_cali_true.flow'
#flowtable = indir + '/br.flow'
#outfile = indir + "/br_flow_patchinfo_04272022.txt"

indir = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar"
flowtable = indir + '/cedar_landsburg.flow'
outfile = indir + "/cedar_flow_patchinfo.txt"



fout = open(outfile,"w")
fout.write("patch_ID zone_ID hill_ID x y z area area drainage_type gamma num_neighbours\n")
with open(flowtable) as f:
    for line in f:
        vars = line.rstrip().split(' ')
        if len(vars) == 11:
            fout.write(line)
fout.close()
print("Done!")