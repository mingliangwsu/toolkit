#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 11:01:02 2020

@author: liuming
"""

import pandas as pd
import pysal as ps
import numpy as np

def sortkey(x): 
    return int(x)

basins = ["EMBOR","BBNTA","FURNA","JURUM","NVPTE","TQRCU"]

dpath = "/home/liuming/mnt/hydronas1/Projects/ForJocerito"

for basin in basins:
    txtfile = dpath + "/" + basin + ".obs.day"
    outfile = dpath + "/" + basin + ".obs.month"
    daily_data = pd.read_csv(txtfile, sep='\t', names=["Year", "Month", "Day", "cfs"], header = None)
    monthly_data = daily_data.groupby(by = ['Year','Month']).mean().reset_index()
    del monthly_data['Day']
    monthly_data.to_csv(outfile, header=None, index=None, sep='\t')