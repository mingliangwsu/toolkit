#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 13:56:50 2022
get strata veg ID (two stratas) for each patch 
@author: liuming
"""

import numpy as np
import pandas as pd
import sys 
import os
import math

path = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/process_data"
patch_vegid_file = path + "/patch_vegID2.txt"

patchveg = pd.read_csv(patch_vegid_file)

print("Done!")                    