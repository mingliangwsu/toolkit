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
#from wrf import getvar, latlon_coords
import pandas as pd
import math
import numpy as np
from datetime import datetime, timedelta
reference_date = datetime(1850, 1, 1)

def get_yyyymmdd_from_days_since1850(days_since):
    new_date = reference_date + timedelta(days=days_since)
    # Convert the date to the desired format YYYYMMDD
    formatted_date = new_date.strftime('%Y%m%d')
    return formatted_date

def convert_to_degrees_east(longitude):
    if longitude < 0:
        return longitude + 360
    return longitude

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def row_col_index_to_gridid(row,col,digits):
    return (row + 1)*digits + (col + 1)

def set_year_from_month(month,first_date):
    year = int(first_date[:4])
    if month >= 9:
        return year
    else:
        return year + 1

#relative path to the data folder
#datapath = "/home/liuming/mnt/hydronas3/Projects/Forecast2026/Data/CMIP6/cesm2.1.5"

dpath = '/home/liuming/Projects/CMIP6data/WRF_Alex_Hall'

regions = ['WA','CRB','CRB_USA']
#regions = ['CRB_USA']

#generate the mask array
nc_cord = f'{dpath}/wrfinput_d02_coord.nc'
#coordinate_nc = '/home/liuming/Projects/CMIP6data/WRF_Alex_Hall/wrfinput_d02_coord.nc'
#selected_wrf_grid_file = '/home/liuming/Projects/CMIP6data/WRF_Alex_Hall/WRF_WA.csv'

selected_gridids = dict()
for region in regions:
    selected_wrf_grid_file = f'{dpath}/{region}_WRF_Grids.csv'
    selected_wrf_grid = pd.read_csv(selected_wrf_grid_file)
    selected_gridids[region] = selected_wrf_grid['gridid'].tolist()


dcord = xr.open_dataset(nc_cord)
first_element = dcord
rows = first_element.sizes['lat']
cols = first_element.sizes['lon']

selected_mask = dict()
for region in regions:
    new_data = np.zeros(first_element['lat2d'].shape, dtype=int)
    first_element[region] = (['lat', 'lon'], new_data)
    for i in range(rows):  # Loop over the first dimension (x)
        for j in range(cols):  # Loop over the second dimension (y)
            gridid = row_col_index_to_gridid(i,j,1000)
            if gridid in selected_gridids[region]:
                first_element[region][i,j] = 1
    selected_mask[region] = (first_element[region] == 1)
    selected_mask[region] = selected_mask[region].rename({'lat': 'lat2d','lon': 'lon2d'})


#Get mean


vars = ['lw_dwn','t2','prec','t2max','q2','t2min','rh','wspd10mean','sw_dwn']
#vars = ['lw_dwn']
for var in vars:
    alldata = pd.DataFrame()
    outfile = f'{dpath}/{var}.yearmonth.mean.csv'
    ddpath = '/home/liuming/Projects/CMIP6data/WRF_Alex_Hall/RAW'
    for dirpath, dirnames, filenames in os.walk(ddpath):
        for dirname in dirnames:
            #print(os.path.join(dirpath, dirname))  # Full path of the subdirectory
            
            model = dirname.split('_')[0]
            ddir = f'{ddpath}/{dirname}'
            if dirname[-3:] == '_bc':
                bc = 'NonBC'
            else:
                bc = 'BC'
            #print(ddir) # Full path of the subdirectory
            
            #loop all files
            for filename in os.listdir(ddir):
                ffile = f'{ddir}/{filename}'
                if filename[-3:] == '.nc' and filename.split('.')[0] == var:
                    print(filename)

                    #var = 't2'
                    ncfile_name = ffile
                    ds = xr.open_dataset(ncfile_name)
                    #ds['temp_celsius'] = kelvin_to_celsius(ds['t2'])
                    first_date = str(int(ds['day'][0].item()))
                    end_date = str(int(ds['day'][-1].item()))
                    if len(first_date) != 8:  #some model has day format as "days since 1850-01-01"
                        #ds['day'] = ds['day'].apply(get_yyyymmdd_from_days_since1850)
                        date_np = np.datetime64(ds['day'][0].item(), 'ns')
                        first_date = np.datetime_as_string(date_np, unit='D').replace('-', '')
                    else:
                        ds['day'] = pd.to_datetime(ds['day'].astype(int).astype(str), format='%Y%m%d')
                    monthly_mean = ds.groupby('day.month').mean()
                    ds = monthly_mean
                    selmean_timeseries = dict()
                    for region in regions:
                        selected_data = ds[var].where(selected_mask[region])
                        selmean_timeseries[region] = selected_data.mean(dim=['lat2d','lon2d'])
                        df = selmean_timeseries[region].to_dataframe().reset_index()
                        
                        df['region'] = region
                        df['year'] = df['month'].apply(set_year_from_month,args=(first_date,))
                        df['model'] = model
                        df['bc'] = bc
                        if alldata.empty:
                            alldata = df.copy()
                        else:
                            alldata = pd.concat([alldata, df], ignore_index=True)
                        
                    
                    allmean_timeseries = ds[var].mean(dim=['lat2d','lon2d'])
                    df = allmean_timeseries.to_dataframe().reset_index()
                    df['region'] = 'WRFDOMAIN'
                    df['year'] = df['month'].apply(set_year_from_month,args=(first_date,))
                    df['model'] = model
                    df['bc'] = bc
                    if alldata.empty:
                        alldata = df.copy()
                    else:
                        alldata = pd.concat([alldata, df], ignore_index=True)
                    
                    
    if not alldata.empty:
        alldata.to_csv(outfile, index=False)


# Plot the 1D array data
plt.figure(figsize=(10, 5))
plt.plot(allmean_timeseries, marker='o', color='blue', label='Entire domain')
for region in regions:
    if region == 'WA': scolor = 'red'
    if region in ['CRB','CRB_USA']: scolor = 'black'
    plt.plot(selmean_timeseries[region], marker='.', color=scolor, label=region)
# Customize the plot
plt.title(var)
plt.xlabel('Time')
plt.ylabel(var)
plt.legend()
plt.grid()
plt.show()

#first_element['mask'].plot(figsize=(12, 13))
#plt.show()
