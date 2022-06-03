#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 15:41:38 2022

@author: liuming
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
import os
from os.path import exists
import math
from scipy.interpolate import make_interp_spline, BSpline
from scipy.ndimage.filters import gaussian_filter1d

path = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/Outputs"
zone_month_file = path + "/test_output_zone.monthly"
outf = path + "/zone_132001_month.csv"
outallregion = path + "/zone_month_198507.csv"

zone = pd.read_csv(zone_month_file, delim_whitespace=True)
t = zone[zone["zoneID"] == 132001]
oneday = zone[(zone["year"] == 1985) & (zone["month"] == 7)]
t.to_csv(outf)
oneday.to_csv(outallregion)