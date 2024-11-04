#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10/15/2024 for
@author: liuming
"""

import xarray as xr
import matplotlib.pyplot as plt
#import subprocess
import os
from wrf import getvar, latlon_coords
import pandas as pd
import math

#relative path to the data folder
#datapath = "/home/liuming/mnt/hydronas3/Projects/Forecast2026/Data/CMIP6/cesm2.1.5"

coordinate_nc = '/home/liuming/Projects/CMIP6data/WRF_Alex_Hall/wrfinput_d02_coord.nc'
outf = '/home/liuming/Projects/CMIP6data/WRF_Alex_Hall/wrf_gridid_coord.csv'

cordf = pd.DataFrame({
    'gridid': pd.Series(dtype='int'),
    'lat': pd.Series(dtype='float'),
    'lon': pd.Series(dtype='float')
})

cords = xr.open_dataset(coordinate_nc)

rows = cords.sizes['lat']
cols = cords.sizes['lon']
shift = int(math.pow(10, len(str(cols))))

for row in range(rows): #rows):
    for col in range(cols):
        lat = cords['lat2d'].isel(lat=row,lon=col).item()
        lon = cords['lon2d'].isel(lat=row,lon=col).item()
        #print(f'row:{row} col:{col} lat:{lat} lon:{lon}')
        pid = (row + 1) * shift + (col + 1)
        new_row = pd.DataFrame({'gridid': [pid], 'lat':[lat], 'lon':[lon]})
        #cordf = cordf.append(new_row, ignore_index=True)
        cordf = pd.concat([cordf, new_row], ignore_index=True)

cordf.to_csv(outf,index=False)

