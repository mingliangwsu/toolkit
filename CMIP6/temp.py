#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:57:19 2024

@author: liuming
"""
#import xarray as xr
#import matplotlib.pyplot as plt
#import subprocess
#import os
#from wrf import getvar, latlon_coords
import pandas as pd
#import math
#import numpy as np
#from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os,sys
from scipy.interpolate import griddata
import numpy as np

#historical period comparison: 1980/10 ~ 2005/9:1
#GCM period 2025/10 ~ 2055/9:2 and 2055/10 ~ 2085/9:3

monthdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def lat_from_id(x): 
    lat = (x // 928) * 0.0625 + 25 + 0.0625 / 2.0
    return lat

def lon_from_id(x): 
    lon = ((x - 207873) % 928) * 0.0625 + (-125.0 + 0.0625 / 2.0)
    return lon

def id_from_lat_lon(xlon,ylat): 
    id = ((ylat - 25 - 0.0625 / 2.0) // 0.0625) * 928 + (xlon + 125 - 0.0625 / 2.0) / 0.0625 + 1
    return id

def monhdays(row):
    return monthdays[int(row['month']) - 1]

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def period(row):
    year = row['year']
    month = row['month']
    period = 0
    if year > 1980 and year < 2005:
        period = 1
    elif year == 1980 and month >= 10:
        period = 1
    elif year == 2005 and month <= 9:
        period = 1
    elif year > 2025 and year < 2055:
        period = 2
    elif year == 2025 and month >= 10:
        period = 2
    elif year == 2055 and month <= 9:
        period = 2
    elif year > 2055 and year < 2085:
        period = 3
    elif year == 2055 and month >= 10:
        period = 3
    elif year == 2085 and month <= 9:
        period = 3
    return period

def wateryear(row):
    year = row['year']
    month = row['month']
    wy = year
    if month >= 10:
        wy = year + 1
    return wy

def weighted_mean(group, weight_col):
    # Multiply values by weights and sum them, then divide by the sum of the weights
    return (group.mul(group[weight_col], axis=0).sum()) / group[weight_col].sum()

#output_path = '/home/mingliang/Projects/cmip6/maps_compare_WRF_gridmet_MACA'
output_path = '/home/liuming/mnt/hydronas3/Projects/CMIP6_Data/statistics'

#gridmetmaca_path = '/media/mingliang/USB1TB/CMIP6_USB/WRC_GRIDMET_MACA_GRIDDATA_YEAR_MONTH'
gridmetmaca_path = '/media/liuming/USB1TB1/CMIP6_USB/WRC_GRIDMET_MACA_GRIDDATA_YEAR_MONTH'

gridmetmaca_path2 = '/home/liuming/mnt/hydronas3/Projects/CMIP6_Data/statistics/WRF_MACA_Gridmet_mean'

wrf_path = gridmetmaca_path



fgridmet = f'{gridmetmaca_path}/PNW_GRIDMET_VIC_GRIDMET_yearmonth_mean_grid.csv'

flivneh = f'{gridmetmaca_path2}/PNW_LIVNEH_VIC_LIVNEH_yearmonth_mean_grid.csv'

period_name = {1:'1990s',2:'2040s',3:'2070s'}

latmin,latmax = 40,53
lonmin,lonmax = -126,-109
grid_lat, grid_lon = np.mgrid[latmin:latmax:200j, lonmin:lonmax:200j]          #for interpolation


maps = ['GRIDMET','MACA','WRF','Livneh']

varss = ['TAVG','PPT']
ccmap = dict()
vvmin = dict()
vvmax = dict()
for var in varss:
    if var == 'PPT':
        ccmap[var] = 'YlGnBu'
        vvmin[var] = 0
        vvmax[var] = 2000
        #scatter = plt.scatter(df['lon'], df['lat'], c=df[var], s=16, alpha=0.6, edgecolors='w', linewidth=0.5, cmap = ccmap, vmin=0,vmax=vvmax)
    else:
        ccmap[var] = 'viridis'
        vvmin[var] = -2
        vvmax[var] = 15

tmap = 'Livneh'
if tmap in ['GRIDMET','Livneh']:
    if tmap == 'GRIDMET':
        fn = fgridmet
    elif tmap == 'Livneh':
        fn = flivneh
    
    
    gridmet = pd.read_csv(fn)
    gridmet['monthdays'] = gridmet.apply(monhdays,axis=1)
    gridmet['TAVG'] = (gridmet['TMAX'] + gridmet['TMIN']) / 2.0
    gridmet['lat'] = gridmet['GRID_CODE'].apply(lat_from_id)
    gridmet['lon'] = gridmet['GRID_CODE'].apply(lon_from_id)
    gridmet['period'] = gridmet.apply(period,axis=1)
    gridmet['wateryear'] = gridmet.apply(wateryear,axis=1)
    gridmet['PPT'] = gridmet['PPT'] * gridmet['monthdays'] #PPT is mm/month
    gridmet['TAVGsum'] = gridmet['TAVG'] * gridmet['monthdays']
    
    #precipitation & TAVG
    df = gridmet[gridmet['period'] == 1]
    df = df.groupby(['period','GRID_CODE','wateryear']).agg({'PPT': 'sum','TAVGsum':'sum','lat': 'mean','lon':'mean'}).reset_index()
    df = df.groupby(['period','GRID_CODE']).agg({'PPT': 'mean','TAVGsum':'mean','lat': 'mean','lon':'mean'}).reset_index()
    df['TAVGsum'] = df['TAVGsum']/365.0
    df = df.rename(columns={'TAVGsum': 'TAVG'})
    
    df.to_csv(f'{output_path}/map_{tmap}_1990s.csv',index=False)
    
    varss = ['TAVG','PPT']
    for var in varss:
        plt.figure(figsize=(10, 6))
        
        grid_value = griddata((df['lon'], df['lat']), df[var], (grid_lon, grid_lat), method='linear')
        #grid_value = griddata((df['lat'], df['lon']), df['value'], (grid_lon, grid_lat), method='linear')
        
        # Create a heatmap for the interpolated grid
        plt.figure(figsize=(10, 6))
        plt.imshow(grid_value, extent=(lonmin, lonmax, latmin, latmax), origin='lower', alpha=0.5, cmap=ccmap[var], vmin=vvmin[var],vmax=vvmax[var])
        plt.colorbar(label=f'{var}')
        plt.title(f'{tmap} {var} {period_name[1]}', fontsize=15)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        #plt.gca().invert_yaxis()
        plt.savefig(f'{output_path}/map_{tmap}_{var}.png',dpi=300)
    
        plt.show()
        
        
        ## Add color bar
        #plt.colorbar(scatter, label=f'{var}')
        
        ## Set titles and labels
        #plt.title(f'GridMet {var} during 1980/10 ~ 2005/9', fontsize=15)
        #plt.xlabel('Longitude', fontsize=12)
        #plt.ylabel('Latitude', fontsize=12)
        
        ## Show the plot
        #plt.grid()
        #plt.savefig(f'{output_path}/map_gridmet_{var}.png',dpi=300)
        #plt.show()


if tmap == 'MACA':
    GCMS = ['bcc-csm1-1','HadGEM2-ES365','BNU-ESM','inmcm4','CanESM2','IPSL-CM5A-LR',
            'CNRM-CM5','IPSL-CM5A-MR','CSIRO-Mk3-6-0','IPSL-CM5B-LR','GFDL-ESM2G',
            'MIROC5','GFDL-ESM2M','MIROC-ESM-CHEM','MIROC-ESM','HadGEM2-CC365','MRI-CGCM3']
    #GCMS = ['bcc-csm1-1']
    
    
    #GCMS = ['bcc-csm1-1']
    cmip5 = pd.DataFrame()
    
    for gcm in GCMS:
        if not os.path.exists(f'{output_path}/map_MACA_{gcm}.csv'):
            #df = pd.read_csv(f'{gridmetmaca_path}/{gcm}_VIC_GCM_yearmonth_mean_grid.csv',usecols=['year','month','PPT','TMAX','TMIN','GRID_CODE','scn','region'])
            chunksize = 10000000 #5000000  # Adjust as needed
            df = pd.DataFrame()
            
            filename = f'{gridmetmaca_path}/PNW_{gcm}_VIC_GCM_yearmonth_mean_grid.csv'
            if not os.path.exists(filename):
                filename = f'{gridmetmaca_path2}/PNW_{gcm}_VIC_GCM_yearmonth_mean_grid.csv'
                if not os.path.exists(filename):
                    print(f'Error: file: {filename} not exist!')
                    sys.exit()
            idx = 0
            for chunk in pd.read_csv(filename, chunksize=chunksize):
                # Process each chunk
                #print(chunk.head())
                print(f'{gcm} chunk:{idx}')
                chunk = chunk.drop(['WIND','SPH','SRAD','RMAX','RMIN'], axis=1)
                chunk['monthdays'] = chunk.apply(monhdays,axis=1)
                chunk['TAVG'] = (chunk['TMAX'] + chunk['TMIN']) / 2.0
            
                chunk['period'] = chunk.apply(period,axis=1)
                chunk['wateryear'] = chunk.apply(wateryear,axis=1)
                chunk['PPT'] = chunk['PPT'] * chunk['monthdays'] #PPT is mm/month
                chunk['TAVGsum'] = chunk['TAVG'] * chunk['monthdays']
                
                #precipitation & TAVG
                #df = df[(df['period'] == 1) & (df['region'] == 'CRB')]
                #chunk = chunk[chunk['region'] == 'CRB']
                chunk = chunk.groupby(['period','GRID_CODE','wateryear','scn']).agg({'PPT': 'sum','TAVGsum':'sum'}).reset_index()
            
                if df.empty:
                    df = chunk.copy()
                else:
                    df = pd.concat([df,chunk],ignore_index=True)
                idx += 1
            
            
            df = df.groupby(['period','GRID_CODE','scn']).agg({'PPT': 'mean','TAVGsum':'mean'}).reset_index()
            df['TAVGsum'] = df['TAVGsum']/365.0
            df['model'] = gcm
            df['lat'] = df['GRID_CODE'].apply(lat_from_id)
            df['lon'] = df['GRID_CODE'].apply(lon_from_id)
            df = df.rename(columns={'TAVGsum': 'TAVG'})
        
            df.to_csv(f'{output_path}/map_MACA_{gcm}.csv')
        else:
            df = pd.read_csv(f'{output_path}/map_MACA_{gcm}.csv')
        
        if cmip5.empty:
            cmip5 = df.copy()
        else:
            cmip5 = pd.concat([cmip5,df],ignore_index=True)
    
    alldf = cmip5.groupby(['period','GRID_CODE','scn']).agg({'PPT': 'median','TAVG':'median','lat': 'mean','lon':'mean'}).reset_index()
    alldf.to_csv(f'{output_path}/map_MACA.csv')
    varss = ['TAVG','PPT']
    for scn in ['rcp45','rcp85']:
        for period in period_name:
            for var in varss:
                df = alldf[(alldf['period'] == period) & (alldf['scn'] == scn)]
                if not df.empty:
                    plt.figure(figsize=(10, 6))
                    
                    grid_value = griddata((df['lon'], df['lat']), df[var], (grid_lon, grid_lat), method='linear')
                    plt.imshow(grid_value, extent=(lonmin, lonmax, latmin, latmax), origin='lower', alpha=0.5, cmap=ccmap[var], vmin=vvmin[var],vmax=vvmax[var])
                    plt.colorbar(label=f'{var}')
                    
                    #scatter = plt.scatter(df['lon'], df['lat'], c=df[var], s=16, alpha=0.6, edgecolors='w', linewidth=0.5, cmap = ccmap[var],vmin=vvmin[var],vmax=vvmax[var])
                    
                    # Add color bar
                    #plt.colorbar(scatter, label=f'{var}')
                    
                    # Set titles and labels
                    plt.title(f'MACA {var} {period_name[period]} {scn}', fontsize=15)
                    plt.xlabel('Longitude', fontsize=12)
                    plt.ylabel('Latitude', fontsize=12)
                    
                    # Show the plot
                    plt.grid()
                    
                    plt.savefig(f'{output_path}/map_MACA_{var}_{period_name[period]}_{scn}.png',dpi=300)
                    plt.show()



'''
WRF_vars = ['lw_dwn','sw_dwn','q2','rh','t2','t2max','t2min','prec','wspd10mean']
WRF_vars = ['t2','prec']
#WRF_vars = ['prec','t2']
allWRF = pd.DataFrame()
for filename in os.listdir(wrf_path):
    #print(filename)
    file_path = os.path.join(wrf_path, filename)
    #WRF_prec_access-cm2_r5i1p1f1_historical.yearmonth.mean.grid.csv
    if filename[0:3] == 'WRF':
        
        t = filename.replace('_', ' ').replace('.', ' ')
        tt = t.split()
        var = tt[1]
        # Check if it’s a file (not a subdirectory)
        if os.path.isfile(file_path) and var in WRF_vars and tt[2] in ['access-cm2','earth3','fgoals-g3'] and tt[4] == 'historical' and '_bc.' in filename:
            print(file_path)
            df = pd.read_csv(file_path)  #month,t2,lat2dv,lon2dv,year,gcm,scn,version,bc
            
            df = df[(df['lat2dv'] >= latmin) & (df['lat2dv'] <= latmax) & (df['lon2dv'] >= lonmin) & (df['lon2dv'] <= lonmax)]
            
            df['monthdays'] = df.apply(monhdays,axis=1)
            if var == 't2':
                df[var] = df[var].apply(kelvin_to_celsius)
                df[var] = df[var] * df['monthdays']
        
            df['period'] = df.apply(period,axis=1)
            df['wateryear'] = df.apply(wateryear,axis=1)
            if var == 'prec':
                df[var] = df[var] * df['monthdays'] #PPT is mm/month
            df['lat2dv'] = df['lat2dv'].round(7)
            df['lon2dv'] = df['lon2dv'].round(7)
            df = df[df['period'] > 0]

            
            #precipitation & TAVG
            #df = df[(df['period'] == 1) & (df['region'] == 'CRB')]
            #df = df.drop(['t2','prec'])
            df = df.groupby(['gcm','period','lat2dv','lon2dv','wateryear','scn','version','bc']).agg({var: 'sum'}).reset_index()
            df = df.groupby(['gcm','period','lat2dv','lon2dv','scn','version','bc']).agg({var: 'mean'}).reset_index()
            if var == 't2':
                df[var] = df[var] / 365.0
            df['var'] = var
            df = df.rename(columns={var:'value'})
            
            if allWRF.empty:
                allWRF = df.copy()
            else:
                allWRF = pd.concat([allWRF,df], ignore_index=True)

allWRF.to_csv(f'{output_path}/map_WRF_period_all_gcms.csv',index=False)
allwrfmedian = allWRF.groupby(['period','lat2dv','lon2dv','scn','bc','var']).agg({'value': 'median'}).reset_index()
allwrfmedian.to_csv(f'{output_path}/map_WRF_period_median.csv',index=False)

for period in period_name:
    for var in WRF_vars:
        for bc in ['BC','NonBC']:
            for scn in ['hist','ssp370']:
                df = allwrfmedian[(allwrfmedian['period'] == period) & (allwrfmedian['var'] == var) & (allwrfmedian['scn'] == scn) & (allwrfmedian['bc'] == bc) ]
                if not df.empty:
                    
                    #plt.figure(figsize=(10, 6))
                    if var == 'prec':
                        ccmap = 'YlGnBu'
                        vvmin = 0
                        vvmax = 2000
                        #scatter = plt.scatter(df['lon2dv'], df['lat2dv'], c=df['value'], s=50, alpha=0.6, edgecolors='w', linewidth=0.5, cmap = ccmap, vmin=0,vmax=vvmax)
                    else:
                        ccmap = 'viridis'
                        vvmin = -2
                        vvmax = 15
                        #scatter = plt.scatter(df['lon2dv'], df['lat2dv'], c=df['value'], s=50, alpha=0.6, edgecolors='w', linewidth=0.5, cmap = ccmap)
                    
                    # Add color bar
                    #plt.colorbar(scatter, label=f'{var}')
                    
                    # Set titles and labels
                    #plt.title(f'WRF {var} {scn} {period_name[period]} {bc}', fontsize=15)
                    #plt.xlabel('Longitude', fontsize=12)
                    #plt.ylabel('Latitude', fontsize=12)
                    
                    # Show the plot
                    #plt.grid()                    
                    #plt.savefig(f'{output_path}/map_MACA_{var}_{scn}_{bc}_{period_name[period]}.png',dpi=300)

                    #plt.show()
                    
                    grid_lat, grid_lon = np.mgrid[latmin:latmax:200j, lonmin:lonmax:200j]

                    # Interpolate using griddata
                    grid_value = griddata((df['lon2dv'], df['lat2dv']), df['value'], (grid_lon, grid_lat), method='linear')
                    #grid_value = griddata((df['lat'], df['lon']), df['value'], (grid_lon, grid_lat), method='linear')
                    
                    # Create a heatmap for the interpolated grid
                    plt.figure(figsize=(10, 6))
                    plt.imshow(grid_value, extent=(lonmin, lonmax, latmin, latmax), origin='lower', alpha=0.5, cmap=ccmap, vmin=vvmin,vmax=vvmax)
                    plt.colorbar(label=f'{var}')
                    plt.title(f'WRF {var} {scn} {period_name[period]} {bc}', fontsize=15)
                    plt.xlabel('Longitude')
                    plt.ylabel('Latitude')
                    #plt.gca().invert_yaxis()
                    plt.savefig(f'{output_path}/map_MACA_{var}_{scn}_{bc}_{period_name[period]}.png',dpi=300)

                    plt.show()

'''