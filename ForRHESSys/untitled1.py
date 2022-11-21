#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 1 2022
Calculate model performance on NPP/GPP ratio
@author: liuming
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
import os
from os.path import exists
import math
import scipy.stats

#from scipy.interpolate import make_interp_spline, BSpline
#from scipy.ndimage.filters import gaussian_filter1d

if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<growth_year_file> <valid_start_year> <valid_end_year> <valid_veg_id> <patch_stratum_vegid_file> <target1> <target_stddev1> ... <outdist_file>\n")
    sys.exit(0)
print("DOne")