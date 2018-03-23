#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 13:37:50 2017

Read VIC-CropSyst crop daily outputs.

@author: liuming
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re

#vicdir = "/home/liuming/data/vic_out/VIC_his_vic_fluxes"
vicdir = "/media/liuming/Elements/VIC_outputs/VIC_his_vic_fluxes"
os.chdir(vicdir)

outmergedhis = "/home/liuming/data/vic_out/merged_his_met.csv"
#allhis = pd.DataFrame(columns=['lat','lon','# YEAR','MONTH','DAY','OUT_PREC',' OUT_AIR_TEMP'])
index=0
for root, dirs, filenames in os.walk(vicdir):
    for f in filenames:
        vic_crop = pd.read_csv(f,skiprows=5,sep='\t')
        t = re.findall(r"[-+]?\d*\.\d+|\d+",f)
        vic_crop['lat'] = t[0]
        vic_crop['lon'] = t[1]
        vic_crop_tp = vic_crop[['lat','lon','# YEAR','MONTH','DAY','OUT_PREC',' OUT_AIR_TEMP']]
        if index == 0: 
            allhis = vic_crop_tp
        else:    
            allhis = allhis.append(vic_crop_tp,ignore_index=True)
        #allhis = allhis.append(vic_crop_tp,ignore_index=True)
        #print(f)
        print(index)
        index = index + 1
allhis.to_csv(outmergedhis,index=False)
print("Finished!")

