#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 19:51:51 2024

@author: liuming
"""
import os
import pandas as pd
dpath = '/media/liuming/Elements/CMIP6_usb_wrf'
#GCMS = ['bcc-csm1-1']
cmip6 = pd.DataFrame()
for root, dirs, files in os.walk(dpath):
    for file in files:
        file_path = os.path.join(root, file)
        print(file)
        items = file.split('_')
        varname = items[1]
        print(varname)
        if varname in ['t2','prec']:
            df = pd.read_csv(file_path)
            df['month'] = df['month'].astype(int)
            