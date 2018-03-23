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

indir = "/media/liuming/LIU/BPA_VIC_CropSyst_simulation_results"
outdir = indir
output_file = "irrigation_annual_daymean.csv"
os.chdir(indir)

for irrig in range(1):
    #print(irrig)
    sheet_name = "ann_irrig_" + str(irrig)
    exl_name = sheet_name + ".xlsx"
    print(irrig_exl)
    df = pd.read_excel(irrig_exl, sheetname=sheet_name)
    if irrig == 0:
        all_df = df[['Year','avg_ppt','tair']]
    newinfo = df[['irrig_total','irrig_evap','irrig_ro','vic_ro_noirrig','avg_baseflow']]
    irrig_name = 'irr' + str(irrig)
    newinfo.columns = [irrig_name + '_ir', irrig_name + '_irevap', irrig_name + '_irro', irrig_name + '_vicro', irrig_name + '_bf']
    test = newinfo[irrig_name + '_irro'] + newinfo[irrig_name + '_vicro']
    newinfo.merge(test.to_frame(),left_index=True, right_index=True)
    
    
    #newinfo[irrig_name + '_ro'] = test
    #newinfo.assign(irrig_name + '_ro' = newinfo[irrig_name + '_irro'])
    #newinfo[irrig_name + '_ro'] = newinfo[irrig_name + '_irro'] + newinfo[irrig_name + '_vicro'] 
    
    
    all_df.join(df[['irrig_total','irrig_evap','irrig_ro','vic_ro_noirrig','avg_baseflow']])
