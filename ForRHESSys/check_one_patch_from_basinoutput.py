#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 13:13:51 2023

@author: liuming
"""
import pandas as pd

#grow_stratum
patchid = 8066

root = "/home/liuming/mnt/hydronas3/Projects/WWS_Oregon"

filename = root + "/" + "Hilslope_10yrs_grow_stratum.daily"
strta = pd.read_csv(filename,delimiter=' ',header=0)

strta = strta.loc[strta['patchID'] == patchid] 
strta.to_csv(f'{filename}_{patchid}')


filename = root + "/" + "Hilslope_10yrs_stratum.daily"
strta = pd.read_csv(filename,delimiter=' ',header=0)

strta = strta.loc[strta['patchID'] == patchid] 
strta.to_csv(f'{filename}_{patchid}')
