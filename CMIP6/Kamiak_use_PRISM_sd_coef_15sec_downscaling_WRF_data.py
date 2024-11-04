#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 17:57:02 2024

export the coefficient for next round aggregation

@author: liuming
"""

import xarray as xr
#import matplotlib.pyplot as plt
#import subprocess
import os
#from wrf import getvar, latlon_coords
import pandas as pd
import math
from scipy.interpolate import griddata
import numpy as np
#from mpl_toolkits.axes_grid1 import make_axes_locatable

import xarray as xr
#import rasterio
import numpy as np
#import gc
import sys

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15
vectorized_kelvin_to_celsius = np.vectorize(kelvin_to_celsius)

def get_decimal_part(value):
    return value - int(value)

def get_centers_from_corner(ll,counts,cellsize):
    return np.linspace(ll + 0.5 * cellsize, ll + counts * cellsize - 0.5 * cellsize, counts)

def snap_to_nearest_fraction(value, fraction=1/8, less=True):
    t = round(round(value / fraction) * fraction,5)
    if t > value and less == True:
        t -= round(fraction,5)
    if t < value and less == False:
        t += round(fraction,5)
    return t

def is_leap_year(year):
    """Check if a year is a leap year."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def get_points_from_nc(ncfile):
    pfile = f"{prism_coef_path}/CRB_PRISM_15sec_ceof_tmean_month_1_focal_{source_data_resolution:0.5f}.nc"
    nc = xr.open_dataset(pfile)
    plat_list = nc['lat'].values
    plon_list = nc['lon'].values
    new_lat2d, new_lon2d = np.meshgrid(plat_list, plon_list, indexing="ij")
    target_points = np.column_stack((new_lat2d.ravel(), new_lon2d.ravel()))
    return target_points, new_lat2d, new_lon2d, plat_list, plon_list

def convert_360_to_gregorian_simplify(date_360):
    """Convert a single 360-day date to Gregorian by accounting for months of different lengths."""
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # Gregorian month lengths
    # Initialize with January 1st of the year
    year = int(date_360[0:4])
    month = int(date_360[4:6])
    day = int(date_360[6:8])
    if is_leap_year(year):
        days_per_month[1] = 29
    # Adjust the day number by how many days exceed the actual Gregorian month's days
    if day > days_per_month[month-1]:
        return None
    else:
        return pd.Timestamp(year=year, month=month, day=day)

v_convert_360_to_gregorian_simplify = np.vectorize(convert_360_to_gregorian_simplify)
# Function to read ESRI ASCII grid file

if len(sys.argv) < 2:
    print("Usage: python script.py <WRF_GCMmodel_name> ...")
    sys.exit(1)

#outpath = '/home/mingliang/Projects/cmip6'
prism_coef_path = '/weka/data/project/agaid/mingliang.liu/CMIP6/PRISM800mSDCoef'
dpath = '/weka/data/project/agaid/mingliang.liu/CMIP6/WRF_Alex_Hall'
outncpath = '/weka/data/project/agaid/mingliang.liu/CMIP6/WRF_Alex_Hall_SD_16thDD'
nc_cord = '/weka/data/project/agaid/mingliang.liu/CMIP6/PRISM800mSDCoef/wrfinput_d02_coord.nc'
ds_nc_cord = xr.open_dataset(nc_cord)


diff_choice = {'ppt': 'fraction', 'tmin': 'diff', 'tmax': 'diff', 
               'tmean': 'diff', 'vpdmin': 'fraction', 
               'vpdmax': 'fraction', 'soltotal': 'fraction'}
mnumber = {'ppt': '4', 'tmin': '5', 'tmax': '5', 'tmean': '5', 
           'vpdmin': '5', 'vpdmax': '5', 'soltotal': '3'}
#prism_path = '/home/mingliang/Projects/cmip6/PRISM800m'
prism_vars = ['ppt','tmax','tmin','tmean','vpdmax','vpdmin','soltotal']
spatial_downscaling_source = 'WRF'
spatial_downscaling_target = 'VIC'
#target_resolution = 30 / 3600 #1/16
target_resolution = 1/16

agg_factor = int(target_resolution / (15/3600))  #hard coded.The PRISM coef is 15 second resolution

#snapcell = 1/8 #snap to 2-times of VIC gridcell 1/16th
source_data_resolution = 1/12

#get points for interpolation
target_points, new_lat2d, new_lon2d, plat_list, plon_list = get_points_from_nc(f'{prism_coef_path}/CRB_PRISM_15sec_ceof_soltotal_month_12_focal_{source_data_resolution:0.5f}.nc')  #all RAW will be interpolated to 15 second at first


#target_latmin,target_latmax = 40.0,50.0
target_latmin,target_latmax = 40.0,53.0      #include Canada BC
target_lonmin,target_lonmax = -126.0,-109.0

#target_latmin,target_latmax = 44.0,46.0      #include Canada BC
#target_lonmin,target_lonmax = -119.0,-115.0

#WRF data


WRF_PRISM_vars = {'t2':'tmean','t2max':'tmax','t2min':'tmin','prec':'ppt','sw_dwn':'soltotal'}



#WRF_var = 't2'
#pvar = WRF_PRISM_vars[WRF_var]
testoneday = True

coef = dict() #PRISM 15second coordinations
#new_lat2d = None #PRISM 15second coordinations
#new_lon2d = None #PRISM 15second coordinations
#target_points = None #PRISM 15second coordinations
#plat_list = None
#plon_list = None
#agg_factor = None
mask = None
agg_lat,agg_lon = None,None

print('Start...')
for dirpath, dirnames, filenames in os.walk(dpath):
    for dirname in dirnames:
        model = dirname.split('_')[0]
        if dirname == sys.argv[1]:
            ddir = f'{dpath}/{dirname}'
            outdir = f'{outncpath}/{dirname}'
            if not os.path.exists(outdir):
                os.makedirs(outdir, exist_ok=True)
            print(ddir) # Full path of the subdirectory
            for filename in os.listdir(ddir):
                ffile = f'{ddir}/{filename}'
                if filename[-3:] == '.nc' and not os.path.exists(f'{outdir}/{filename}'):
                    #if filename[-3:] == '.nc' and filename.split('.')[0] == 'q2':
                    WRF_var = filename.split('.')[0]
                    if WRF_var in WRF_PRISM_vars:
                        pvar = WRF_PRISM_vars[WRF_var] #PRISM var name
                        print(f'{ffile} var: {WRF_var}')
                    else:
                        pvar = 'None'
    
                    ds = xr.open_dataset(ffile)
                    first_date = str(int(ds['day'][0].item()))
                    end_date = str(int(ds['day'][-1].item()))
                    time_size = ds.sizes['day']
                    if time_size == 360:
                        ds['day'] = ds['day'].astype(int).astype(str)
                        #print(ds['day'][0].item())
                        #ds['day'] = v_convert_360_to_gregorian(ds['day'])
                        ds['day'] = v_convert_360_to_gregorian_simplify(ds['day'])
                        #print(ds['day'][0].item())
                    else:
                        if len(first_date) != 8:  #some model has day format as "days since 1850-01-01"
                            #ds['day'] = ds['day'].apply(get_yyyymmdd_from_days_since1850)
                            date_np = np.datetime64(ds['day'][0].item(), 'ns')
                            first_date = np.datetime_as_string(date_np, unit='D').replace('-', '')
                        else:
                            ds['day'] = pd.to_datetime(ds['day'].astype(int).astype(str), format='%Y%m%d')
                    
                    ds = ds.rename_dims({
                        "lat2d": "lat",
                        "lon2d": "lon"
                    })
                    ds['lat2d'] = ds_nc_cord['lat2d']
                    ds['lon2d'] = ds_nc_cord['lon2d']
    
                    tmpday = []
                    # Code to analyze memory
                    interpolated_data = []
                    for day in ds.day:
                        #print(f'var:{pvar} month:{month}')
                        #month = 7
                        month = day.values.astype('datetime64[M]').astype(int) % 12 + 1
                        tmpday.append(day.values)
                        print(day.values)
                        pvmon = f'{pvar}{month}'
                        if pvmon not in coef and WRF_var in WRF_PRISM_vars:
                            #PRISM_15sec_ceof_{pvar}_month_{month}_focal_{target_resolution:0.5f}.nc
                            pfile = f"{prism_coef_path}/CRB_PRISM_15sec_ceof_{pvar}_month_{month}_focal_{source_data_resolution:0.5f}.nc"
                            coef[pvmon] = xr.open_dataset(pfile)
                            # Rename the variables
                            coef[pvmon] = coef[pvmon].rename({list(coef[pvmon].data_vars)[0]: pvar})
                            
                            if diff_choice[pvar] == 'fraction':
                                coef[pvmon] = coef[pvmon].fillna(1)
                            elif diff_choice[pvar] == 'diff':
                                coef[pvmon] = coef[pvmon].fillna(0)
                        
                        temp_day = ds[WRF_var].sel(day=day).values
                        if WRF_var in ['t2','t2min','t2max']:
                            temp_day = vectorized_kelvin_to_celsius(temp_day)
                        # Flatten lat2d, lon2d, and temperature for griddata
                        points = np.column_stack((ds["lat2d"].values.ravel(), ds["lon2d"].values.ravel()))
                        values = temp_day.ravel()
                        valid_points = points[~np.isnan(values)]
                        valid_values = values[~np.isnan(values)]
                        # Perform interpolation
                        interp_values = griddata(valid_points, valid_values, target_points, method="linear")
                        interp_values = interp_values.reshape(new_lat2d.shape)
                        #interpolated_data.append(interp_values.reshape(new_lat2d.shape))
                        
                        da = xr.DataArray(
                            interp_values,
                            dims=['lat', 'lon'],
                            coords={'lat': plat_list, 'lon': plon_list}  # New coordinates for 1 km grid
                        )
                        
                        da_mean = da.rolling(lat=agg_factor, lon=agg_factor, center=True).mean()
                        
                        if pvmon in coef: #if PRISM coef exist
                            if diff_choice[pvar] == 'fraction':
                                sdds = da_mean * coef[pvmon]
                            elif diff_choice[pvar] == 'diff':
                                sdds = da_mean + coef[pvmon]
                            sdds = sdds.rename({pvar: WRF_var})
                            #print(f'{pvmon} exist and do SD')
                        else: #none spatial downscaling adjustedment, just rescaling
                            sdds = da_mean.to_dataset(name=WRF_var)
                            #sdds.name = WRF_var
                            
                        
        
                        sdds = sdds.coarsen(lat=agg_factor, lon=agg_factor, boundary='pad').mean()
                        
                        #target_latmin,target_latmax = 40.0,50.0
                        #target_lonmin,target_lonmax = -126.0,-109.0
                        
                        if mask is None:
                            mask = (sdds.lat >= target_latmin) & (sdds.lat <= target_latmax) & \
                                   (sdds.lon >= target_lonmin) & (sdds.lon <= target_lonmax)
                               
                        sdds = sdds.where(mask, drop=True)
                        if agg_lat is None and agg_lon is None:
                            agg_lat = sdds['lat'].values
                            agg_lon = sdds['lon'].values
                            
                        interpolated_data.append(sdds[WRF_var])
                        
                        
                        '''
                        #testoneday = False
                        plt.figure(figsize=(10, 6))
                        
                        #test only!
                        damask = (da.lat >= target_latmin) & (da.lat <= target_latmax) & \
                                   (da.lon >= target_lonmin) & (da.lon <= target_lonmax)
                        da = da.where(damask, drop=True)
                        
                        coef_fig = da.plot(cmap='viridis', add_colorbar=False)  # Disable automatic colorbar
                        plt.title(f'original {WRF_var} {day.values}')
                        plt.colorbar(coef_fig, label='Value')
                        plt.tight_layout()
                        plt.show()
                        
                        plt.figure(figsize=(10, 6))
                        coef_fig = sdds[WRF_var].plot(cmap='viridis', add_colorbar=False)  # Disable automatic colorbar
                        plt.title(f'spatial downscaled {WRF_var} {day.values}')
                        plt.colorbar(coef_fig, label='Value')
                        plt.tight_layout()
                        plt.show()
                        
                        coefda = coef[pvmon].where(damask, drop=True)
                        plt.figure(figsize=(10, 6))
                        coef_fig = coefda[pvar].plot(cmap='viridis', add_colorbar=False)  # Disable automatic colorbar
                        plt.title(f'spatial downscaled {WRF_var} {day.values}')
                        plt.colorbar(coef_fig, label='Value')
                        plt.tight_layout()
                        plt.show()
                        '''
        
                        
                        
                                    
                    # Convert interpolated results to an xarray DataArray
                    interpolated_array = xr.DataArray(
                        np.stack(interpolated_data),
                        dims=["day", "lat", "lon"],
                        coords={"day": tmpday, "lat": agg_lat, "lon": agg_lon},
                        name=WRF_var
                    )
                    
                    interpolated_array.to_netcdf(f'{outdir}/{filename}')

