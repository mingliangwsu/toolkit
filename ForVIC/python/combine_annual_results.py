#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 08:50:46 2018
Convert excel annual daily averaged VIC-CropSyst (hydro- and 
irrigation-related variables)


@author: liuming
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pandas import ExcelWriter
from pandas import ExcelFile

indir = "/media/liuming/8E6A81026A80E873/BPA"
outdir = indir
output_file = "irrigation_annual_daymean.csv"
os.chdir(indir)
columns_name = ['Irrig','irrig_total','irrig_evap','irrig_ro','vic_ro_noirrig','avg_baseflow']

#tdf = pd.DataFrame([0,0,0,0,0,0,0], columns=columns_name)

for irrig in range(49):
    #print(irrig)
    sheet_name = "ann_irrig_" + str(irrig)
    exl_name = sheet_name + ".xlsx"
    print(exl_name)
    df = pd.read_excel(exl_name, sheetname=sheet_name)                         #DataFrame
    
    subdf = df[df.Year >= 1922]
   
    if irrig == 0:
        avgdata = pd.DataFrame(columns=columns_name)
        loct = 0
    t0 = irrig
    t1 = df['irrig_total'].mean()
    t2 = df['irrig_evap'].mean()
    t3 = df['irrig_ro'].mean()
    t4 = df['vic_ro_noirrig'].mean()
    t5 = df['avg_baseflow'].mean()
    avgdata = avgdata.append({'Irrig' : t0, 'irrig_total' : t1,'irrig_evap' : t2,'irrig_ro' : t3,'vic_ro_noirrig' : t4,'avg_baseflow' : t5},ignore_index=True)
    
avgdata.to_csv(output_file,sep=',')
