#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 17:57:02 2024

@author: liuming
"""

import xarray as xr
import matplotlib.pyplot as plt
#import subprocess
import os
from wrf import getvar, latlon_coords
import pandas as pd
import math
from scipy.interpolate import griddata
import numpy as np


# Function to read ESRI ASCII grid file
def read_esri_ascii_grid(filename):
    with open(filename, 'r') as f:
        # Read header
        header = {}
        for _ in range(6):
            line = f.readline().strip().split()
            header[line[0]] = float(line[1])
        
        # Extract metadata
        ncols = int(header['ncols'])
        nrows = int(header['nrows'])
        xllcorner = header['xllcorner']
        yllcorner = header['yllcorner']
        cellsize = header['cellsize']
        
        # Read the grid data
        data = np.loadtxt(f)
        data[data == -9999] = np.nan

    # Create coordinate arrays (x, y)
    x = np.linspace(xllcorner, xllcorner + (ncols - 1) * cellsize, ncols)
    y = np.linspace(yllcorner, yllcorner + (nrows - 1) * cellsize, nrows)
    
    # Create a meshgrid of x, y coordinates
    xx, yy = np.meshgrid(x, y)
    
    return xx, yy, data


prism_path = '/home/liuming/Projects/CMIP6data'
prism_vars = ['ppt','tmax','tmin','tmean','vpdmax','vpdmin','soltotal']

pvar = 'ppt'
month = 1
pfile = f'{prism_path}/PRISM_{pvar}_30yr_normal_800mM4_all_asc/PRISM_{pvar}_30yr_normal_800mM4_{month:02}_asc.asc'

# Read the ESRI ASCII grid
xx, yy, z = read_esri_ascii_grid(pfile)
# Flatten the arrays to use them in griddata
points = np.c_[xx.ravel(), yy.ravel()]
values = z.ravel()

# Plot the original data and interpolated data
plt.subplot(1, 2, 1)
plt.imshow(z, extent=(xx.min(), xx.max(), yy.min(), yy.max()), origin='lower')
plt.title('Original Data')
plt.colorbar()

plt.tight_layout()
plt.show()
