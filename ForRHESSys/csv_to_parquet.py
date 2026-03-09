#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 10:56:01 2026

@author: liuming
"""

import pandas as pd
import os



droot = '/home/liuming/mnt/hydronas3/Projects/NASA_Julie/RHESSys_Outputs'
os.chdir(droot)

fname = 'grow_patch_yearly.csv'
# 1. Read CSV
GPY = pd.read_csv(fname)

# 2. Save as Parquet
GPY.to_parquet(f'{fname[:-4]}.parquet', engine='pyarrow')
               