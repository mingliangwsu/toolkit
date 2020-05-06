#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar. 24, 2020, LIU
Process merged VIC daily outputs
@author: liuming
"""

import pandas as pd
import sys 
import os
import math
import re
from os import path


#climates = ["pnnl_historical", "delta_adjusted_pnnl_historical"]
climates = ["pnnl_historical"]
wdir = "/home/liuming/temp"

for climate in climates:
    vicfile = wdir + "/" + climate + "_merged.txt"
    new_data = list(filter(None, [re.split('\s+', i.strip('\n')) for i in open(vicfile)]))
    result = pd.DataFrame(new_data)

#elev_file = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/arcinfo/elev.csv"


