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
#from wrf import getvar, latlon_coords
import pandas as pd
import math
from scipy.interpolate import griddata
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

import xarray as xr
import rasterio
import numpy as np

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
        nodata = header['NODATA_value']
        
        # Read the grid data
        data = np.loadtxt(f)
        data[data == nodata] = np.nan

    # Create coordinate arrays (x, y)
    x = get_centers_from_corner(xllcorner,ncols,cellsize)
    y = get_centers_from_corner(yllcorner,nrows,cellsize)
    y = y[::-1]
    
    # Create a meshgrid of x, y coordinates
    xx, yy = np.meshgrid(x, y)
    
    return xx, yy, data, cellsize, ncols, nrows, xllcorner, yllcorner, nodata

def read_esri_ascii_grid_and_snap_to_VIC_grid(filename):
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
        nodata = header['NODATA_value']
        
        # Read the grid data
        data = np.loadtxt(f)
        data[data == nodata] = np.nan

    # Create coordinate arrays (x, y)
    x = get_centers_from_corner(xllcorner,ncols,cellsize)
    y = get_centers_from_corner(yllcorner,nrows,cellsize)
    y = y[::-1]
    
    # Create a meshgrid of x, y coordinates
    xx, yy = np.meshgrid(x, y)
    
    x_flat = xx.flatten()
    y_flat = yy.flatten()
    z_flat = data.flatten()
    
    # Mask out the NoData values
    mask = z_flat != nodata
    x_interp = x_flat[mask]
    y_interp = y_flat[mask]
    z_interp = z_flat[mask]
    
    newxllcorner = snap_to_nearest_fraction(xllcorner,1/8,True)
    newyllcorner = snap_to_nearest_fraction(yllcorner,1/8,True)
    newxurcorner = snap_to_nearest_fraction(xllcorner + ncols * cellsize,1/8,False)
    newyurcorner = snap_to_nearest_fraction(yllcorner + nrows * cellsize,1/8,False)
    new_ncols = int(round((newxurcorner - newxllcorner) / cellsize,0))
    new_nrows = int(round((newyurcorner - newyllcorner) / cellsize,0))
    new_x = get_centers_from_corner(newxllcorner,new_ncols,cellsize)
    new_y = get_centers_from_corner(newyllcorner,new_nrows,cellsize)
    new_y = new_y[::-1]
    new_x_grid, new_y_grid = np.meshgrid(new_x, new_y)
    
    # Interpolate the data onto the new grid
    new_z_grid = griddata((x_interp, y_interp), z_interp, (new_x_grid, new_y_grid), method='nearest')
    
    return new_x_grid, new_y_grid, new_z_grid, cellsize, new_ncols, new_nrows, newxllcorner, newyllcorner, nodata

# Function to read ESRI ASCII file into xarray.DataArray
def read_ascii_to_xarray(filepath):
    with rasterio.open(filepath) as src:
        # Read the data
        data = src.read(1)  # Read the first (and usually only) band
        # Get the coordinates from the metadata
        transform = src.transform
        nodata_value = src.nodata
        # Create the coordinate arrays (assuming a regular grid)
        x = np.arange(src.width) * transform[0] + transform[2]  # Longitude (x)
        y = np.arange(src.height) * transform[4] + transform[5]  # Latitude (y)
        # Create an xarray DataArray
        da = xr.DataArray(data, dims=("lat", "lon"), coords={"lat": y, "lon": x}, name="values")
        # Mask no data values if nodata_value exists
        if nodata_value is not None:
            da = da.where(da != nodata_value)
    return da

def read_ascii_to_xarray_and_snap_to_VIC_1_16th_grid(filepath):
    #read 30 second 30-year normal PRISM data
    with rasterio.open(pfile) as src:
        data = src.read(1)  # Read the first band (assuming single-band)
        transform = src.transform  # Get affine transform (coordinates)
        nodata = src.nodata  # No-data value
        bounds = src.bounds  # Bounds of the data (min_x, min_y, max_x, max_y)
        res = src.res  # Resolution (cell size)
        
    # Step 2: Convert raster data to xarray DataArray
    # Create coordinate arrays for the x and y axes
    nrows, ncols = data.shape
    
    if abs(res[0] - 0.00833) < 0.0001:   #HARD CODDED!
        cellsize = round(30/3600,12)
    else:
        cellsize = res[0]
    #print(f'cellsize:{cellsize}')
    x_coords = np.linspace(bounds.left + res[0] * 0.5, bounds.right - cellsize * 0.5, ncols)
    y_coords = np.linspace(bounds.top - res[1] * 0.5, bounds.bottom + cellsize * 0.5, nrows)
    
    # Convert to xarray DataArray
    da = xr.DataArray(
        data, 
        dims=["lat", "lon"], 
        coords={"lon": x_coords, "lat": y_coords},
        attrs={"nodata": nodata, "transform": transform}
    )
    
    da = da.where(da != nodata, other=np.nan)
    
    newleft = snap_to_nearest_fraction(bounds.left,1/8,True)
    newbottom = snap_to_nearest_fraction(bounds.bottom,1/8,True)
    newright = snap_to_nearest_fraction(bounds.right,1/8,False)
    newtop = snap_to_nearest_fraction(bounds.top,1/8,False)
    new_ncols = int(round((newright - newleft) / cellsize,0))
    new_nrows = int(round((newtop - newbottom) / cellsize,0))
    # Step 3: Snap to new grid (assuming new grid is regular)
    # Define new grid resolution and coordinates (you can adjust these based on your new grid)
    new_x_coords = np.linspace(newleft + cellsize * 0.5, newright - cellsize * 0.5, new_ncols)  # Example: coarsen the grid
    new_y_coords = np.linspace(newtop - cellsize * 0.5, newbottom + cellsize * 0.5, new_nrows)
    
    print(f'{newleft} {newbottom} {newright} {newtop} ncol:{new_ncols} nrow:{new_nrows} cell:{cellsize:.12f}')
    print(f'{new_x_coords}\n{new_y_coords}\n')
    
    new_grid = xr.DataArray(
        np.empty((len(new_y_coords), len(new_x_coords))),  # Empty grid (can be NaNs)
        dims=["lat", "lon"], 
        coords={"lon": new_x_coords, "lat": new_y_coords}
    )
    snapped_data = da.reindex_like(new_grid, method="nearest")
    return snapped_data

def disaggregate_to_15second_calc_fract_or_shift_from_big_grid(
        da,bfract,target_resolution):
    #da: row 30 second xarray
    #bfract: True get the fraction of sum
    #agg_factor: the aggregation factor from 15 second degree data
    
    #output: 
    #outda:fraction or shift
    #outagg: sum or mean of PRISM at big grid resolution
    
    latitudes = da.coords['lat'].values
    longitudes = da.coords['lon'].values
    
    
    
    new_latitudes = np.linspace(latitudes.max(), latitudes.min(), len(latitudes) * 2) #15 seconds
    new_longitudes = np.linspace(longitudes.min(), longitudes.max(), len(longitudes) * 2) #15 seconds
    #resample to 15 second
    da_15second = xr.DataArray(
        np.repeat(np.repeat(da.values, 2, axis=0), 2, axis=1),
        dims=['lat', 'lon'],
        coords={'lat': new_latitudes, 'lon': new_longitudes}  # New coordinates for 1 km grid
    )
    
    
    agg_factor = int(target_resolution / (da_15second.lat[1] - da_15second.lat[2]))
    print(f"{da.coords['lon'].values.min()} {da.coords['lat'].values.min()} {da.coords['lon'].values.max()} {da.coords['lat'].values.max()} ncols:{da_15second.shape[0]} nrowss:{da_15second.shape[1]} {latitudes[1] - latitudes[0]} agg_factor:{agg_factor}" )
    
    if bfract == True:
        da_agg_sum = da_15second.coarsen(lat=agg_factor, lon=agg_factor, boundary='pad').sum()
        da_15second_sum = xr.DataArray(
            np.repeat(np.repeat(da_agg_sum.values, agg_factor, axis=0), agg_factor, axis=1),
            dims=['lat', 'lon'],
            coords={'lat': new_latitudes, 'lon': new_longitudes}  # New coordinates for 1 km grid
        )
        outda = da_15second / da_15second_sum   #fraction of precipitation of this pixel to 1/16th grid cell
        outagg = da_15second_sum
    else:
        da_agg_mean = da_15second.coarsen(lat=agg_factor, lon=agg_factor, boundary='pad').mean()
        # Resample the 1x1 grid back to 6x6 grid (repeating the value)
        da_15second_mean = xr.DataArray(
            np.repeat(np.repeat(da_agg_mean.values, agg_factor, axis=0), agg_factor, axis=1),
            dims=['lat', 'lon'],
            coords={'lat': new_latitudes, 'lon': new_longitudes}  # New coordinates for 1 km grid
        )
        outda = da_15second - da_15second_mean
        outagg = da_15second_mean
    return outda,outagg
# Example usage:
#filepath = "your_esri_ascii_file.asc"


prism_path = '/home/liuming/Projects/CMIP6data'
prism_vars = ['ppt','tmax','tmin','tmean','vpdmax','vpdmin','soltotal']

pvar = 'ppt'
month = 1
pfile = f'{prism_path}/PRISM_{pvar}_30yr_normal_800mM4_all_asc/PRISM_{pvar}_30yr_normal_800mM4_{month:02}_asc.asc'

#da = read_ascii_to_xarray(pfile)
da = read_ascii_to_xarray_and_snap_to_VIC_1_16th_grid(pfile)
target_resolution = 1/16

coef,agg = disaggregate_to_15second_calc_fract_or_shift_from_big_grid(da,True,target_resolution) #the fraction of 15*15Second, i.e. 1/16th degree

# Create a figure with two subplots
plt.figure(figsize=(20, 6))

# Plot original DataArray
plt.subplot(1, 2, 1)
mappable_original = da.plot(cmap='viridis', add_colorbar=False)  # Disable automatic colorbar
plt.title("Original DataArray (6x6 Grid)")
plt.colorbar(mappable_original, label='Value')

# Plot coarsened DataArray
#plt.subplot(1, 2, 2)
#mappable_coarse = da_1_16th.plot(cmap='viridis', add_colorbar=False)  # Disable automatic colorbar
#plt.title("Aggregated DataArray (1x1 Grid)")
#plt.colorbar(mappable_coarse, label='Value')

#plt.subplot(1, 2, 2)
#mappable_coarse = fraction.plot(cmap='viridis', add_colorbar=False)  # Disable automatic colorbar
#plt.title("Fraction")
#plt.colorbar(mappable_coarse, label='Value')

reconstructed = coef * agg
plt.subplot(1, 2, 2)
mappable_coarse = reconstructed.plot(cmap='viridis', add_colorbar=False)  # Disable automatic colorbar
plt.title("Reconstructed Precipitation")
plt.colorbar(mappable_coarse, label='Value')

# Adjust layout
plt.tight_layout()
plt.show()


'''

# Read the ESRI ASCII grid
xx, yy, z, cellsize, ncols, nrows, xllcorner, yllcorner, nodata = read_esri_ascii_grid_and_snap_to_VIC_grid(pfile)
# Flatten the arrays to pass to griddata

# Flatten the arrays to use them in griddata
points = np.c_[xx.ravel(), yy.ravel()]
values = z.ravel()

# Plot the original data and interpolated data
#fig, ax = plt.subplot(1, 2, 1)
fig, ax = plt.subplots(figsize=(10, 8))
img = ax.imshow(z, extent=(xx.min(), xx.max(), yy.min(), yy.max()), origin='upper',cmap='YlGnBu')
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)  # Adjust the size and padding of the colorbar

# Create the colorbar in the new axis and set its label
cbar = plt.colorbar(img, cax=cax)
cbar.set_label("Precipitation (mm)")
plt.show()
'''