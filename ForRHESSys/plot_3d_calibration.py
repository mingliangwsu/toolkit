#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 15:30:38 2022

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


from mpl_toolkits import mplot3d


datafile = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/test.txt"
pf = pd.read_csv(datafile,delimiter=" ",header=0)

ax = plt.axes(projection='3d')
surf = ax.plot_trisurf(pf['cal0'], pf['cal1'], pf['likelyhood'], linewidth=0, antialiased=False)
#ax.plot_surface(pf['cal0'], pf['cal1'], pf['likelyhood'], rstride=1, cstride=1,
#                cmap='viridis', edgecolor='none')
ax.set_title('surface');