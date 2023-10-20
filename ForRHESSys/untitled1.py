#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 09:00:40 2023

@author: liuming
"""

#import numpy as np
#import pandas as pd
#import datetime
#import sys 
#import os
lon = [-105.8917, -105.85, -105.8083, -105.7667, -105.725, -105.6833, -105.6417, -105.6, -105.5583, -105.5167, -105.475, -105.4333];
    
lat = [40.56667, 40.525, 40.48333, 40.44167, 40.4, 40.35833, 40.31667, 40.275, 40.23333];

outcsv = "/home/liuming/mnt/hydronas3/Projects/Colorado_MZ/Rind_CO/gridmet_centroid.csv"

with open(outcsv,'w') as f:
    f.write("id,lon,lat\n")
    id = 0
    for ilon in lon:
        for ilat in lat:
            outline = str(id) + ',' + str(ilon) + ',' + str(ilat) + '\n'
            f.write(outline)
            id += 1
            