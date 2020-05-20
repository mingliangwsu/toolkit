#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 17:41:19 2020

@author: liuming
"""

import xarray
import matplotlib.pyplot as plt
import matplotlib.colors
cmap = matplotlib.colors.ListedColormap(["limegreen", "gold", "crimson"])
#fname = 'http://thredds.ucar.edu/thredds/dodsC/grib/NCEP/GFS/Global_onedeg/Best'  # Remote OPeNDAP Dataset 
#fname = '/home/liuming/mnt/hydronas1/Projects/USDA_Water_Ag/METRIC/GIS/Franklin_x1_y1.nc_2017-03-01_2017-10-31.nc'   # Local NetCDF file
#fname = '/home/liuming/mnt/hydronas1/Projects/USDA_Water_Ag/METRIC/GIS/Franklin_x1_y1.nc'   # Local NetCDF file
fname = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/Gridded_runoff/9228176/GRUN_v1_GSWP3_WGS84_05_1902_2014.nc"

ds = xarray.open_dataset(fname)

#dsloc = ds.sel(x=334452,y=5132481.0,method='nearest')
#dsloc = ds.sel(x=334327,y=5131703.0,method='nearest')

ncstart_year = 1902
ncend_year = 2014
target_start_year = 1985
target_end_year = 2014

nc_start_X = -179.75
nc_start_Y = -89.75
target_start_X = -125
target_end_X = -115
target_start_Y = 45
target_end_Y = 50

sel_time_start_index = (target_start_year - ncstart_year) * 12
sel_time_end_index = (target_end_year - ncstart_year) * 12 - 1

sel_X_start_index = int((target_start_X - nc_start_X) / 0.5)
sel_X_end_index = int((target_end_X - nc_start_X) / 0.5)
sel_Y_start_index = int((target_start_Y - nc_start_Y) / 0.5)
sel_Y_end_index = int((target_end_Y - nc_start_Y) / 0.5)



dsloc_growingseason = ds.isel(time=slice(sel_time_start_index,sel_time_end_index), \
                              X=slice(sel_X_start_index,sel_X_end_index), \
                              Y=slice(sel_Y_start_index,sel_Y_end_index))
#dsloc_growingseason_pt = dsloc_growingseason.sel(x=334327,y=5131703.0,method='nearest')

t_sptial_mean=dsloc_growingseason.sum(dim='time')
t_time_mean=dsloc_growingseason.mean(dim=['X','Y'])
#t_sptial_mean=ds.sum(dim='time')
#t_time_mean=ds.mean(dim=['X','Y'])

#dsloc = ds.sel(x=slice(331681,332078),y=slice(5130449,5129830))
#dsloc = ds.sel(CDL=1)

#dsloc['ET'].plot();
#dsloc['ETR'].plot(color='red');
#dsloc['ETRF'].plot(color='green');
norm = matplotlib.colors.BoundaryNorm([0,50,100,200,350,500,700,900,1100,1300,1500], 10)
#norm = matplotlib.colors.BoundaryNorm([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5], 10)
plt.figure(0)
t_sptial_mean['Runoff'].plot(cmap='YlGn',norm=norm)
plt.figure(1)
t_time_mean['Runoff'].plot()
#dsloc_growingseason_pt['ET'].plot();
plt.figure(2)
#dsloc_growingseason_pt['ETR'].plot(color='red');
plt.figure(3)
#dsloc_growingseason_pt['ETRF'].plot(color='green');