#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:07:18 2020

@author: liuming
"""

import xarray
import pandas as pd
import numpy as np

datapath = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/prepostprocess"
delta_nc = "deltas_PRISM_v_PNNLWRF.nc"

delta = xarray.open_dataset(datapath + "/" + delta_nc)

alldic = dict()
var_list = ["LAT","LON","PRCP_ratio","TMIN_diff","TMAX_diff"]
for var in var_list:
    alldic[var] = list()
    for a in delta[var]:
        for b in a.values:
            alldic[var].append(b)
print("Done!")

for var in var_list:
    if var != "LAT" and var != "LON":
        outfile = datapath + "/delta_" + var + ".csv"
        with open(outfile,"w") as f:
            for idx,val in enumerate(alldic[var]):
                if not np.isnan(val):  
                    f.write(str(int(val*100)) + "," + str(alldic["LON"][idx]) + "," + str(alldic["LAT"][idx]) + "\n")