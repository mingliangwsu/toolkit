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

def kelvin_to_celsius_df(row):
    return row['TAVG'] - 273.15

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

tmap = 'WRF'
if tmap in ['GRIDMET','Livneh']:
    if tmap == 'GRIDMET':
        fn = fgridmet
    elif tmap == 'Livneh':
        fn = flivneh
    if not os.path.exists(f'{output_path}/map_{tmap}.csv'):
        chunksize = 20000000 #5000000  # Adjust as needed
        df = pd.DataFrame()
        idx = 0
        for chunk in pd.read_csv(fn, chunksize=chunksize):
            # Process each chunk
            #print(chunk.head())
            print(f'{tmap} chunk:{idx}')
            #chunk = chunk.drop(['WIND','SPH','SRAD','RMAX','RMIN'], axis=1)
            chunk['monthdays'] = chunk.apply(monhdays,axis=1)
            chunk['TAVG'] = (chunk['TMAX'] + chunk['TMIN']) / 2.0
        
            chunk['period'] = chunk.apply(period,axis=1)
            chunk['wateryear'] = chunk.apply(wateryear,axis=1)
            chunk['PPT'] = chunk['PPT'] * chunk['monthdays'] #PPT is mm/month
            chunk['TAVGsum'] = chunk['TAVG'] * chunk['monthdays']
            
            #chunk['lat'] = chunk['GRID_CODE'].apply(lat_from_id)
            #chunk['lon'] = chunk['GRID_CODE'].apply(lon_from_id)
            
            #precipitation & TAVG
            #df = df[(df['period'] == 1) & (df['region'] == 'CRB')]
            #chunk = chunk[chunk['region'] == 'CRB']
            chunk = chunk.groupby(['period','GRID_CODE','wateryear']).agg({'PPT': 'sum','TAVGsum':'sum'}).reset_index()
        
            if df.empty:
                df = chunk.copy()
            else:
                df = pd.concat([df,chunk],ignore_index=True)
            idx += 1
        
        df = df.groupby(['period','GRID_CODE','wateryear']).agg({'PPT': 'sum','TAVGsum':'sum'}).reset_index()
        df = df.groupby(['period','GRID_CODE']).agg({'PPT': 'mean','TAVGsum':'mean'}).reset_index()
        df['TAVGsum'] = df['TAVGsum']/365.0
        #df['model'] = gcm
        df['lat'] = df['GRID_CODE'].apply(lat_from_id)
        df['lon'] = df['GRID_CODE'].apply(lon_from_id)
        df = df.rename(columns={'TAVGsum': 'TAVG'})
    
        df.to_csv(f'{output_path}/map_{tmap}.csv')
    else:
        df = pd.read_csv(f'{output_path}/map_{tmap}.csv')

    
    #precipitation & TAVG
    df = df[df['period'] == 1]
    #df = df.groupby(['period','GRID_CODE']).agg({'PPT': 'mean','TAVGsum':'mean','lat': 'mean','lon':'mean'}).reset_index()
    #df['TAVGsum'] = df['TAVGsum']/365.0
    #df = df.rename(columns={'TAVGsum': 'TAVG'})
    
    df.to_csv(f'{output_path}/map_{tmap}_1990s.csv',index=False)
    
    varss = ['TAVG','PPT']
    for var in varss:
        plt.figure(figsize=(10, 6))
        
        grid_value = griddata((df['lon'], df['lat']), df[var], (grid_lon, grid_lat), method='linear')
        #grid_value = griddata((df['lat'], df['lon']), df['value'], (grid_lon, grid_lat), method='linear')
        
        # Create a heatmap for the interpolated grid
        plt.figure(figsize=(10, 6))
        plt.imshow(grid_value, extent=(lonmin, lonmax, latmin, latmax), origin='lower', alpha=1.0, cmap=ccmap[var], vmin=vvmin[var],vmax=vvmax[var])
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
            chunksize = 20000000 #5000000  # Adjust as needed
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
            df = df.groupby(['period','GRID_CODE','wateryear','scn']).agg({'PPT': 'sum','TAVGsum':'sum'}).reset_index()
            #df = df.groupby(['period','GRID_CODE','scn']).agg({'PPT': 'mean','TAVGsum':'mean'}).reset_index()
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
                    plt.imshow(grid_value, extent=(lonmin, lonmax, latmin, latmax), origin='lower', alpha=1.0, cmap=ccmap[var], vmin=vvmin[var],vmax=vvmax[var])
                    plt.colorbar(label=f'{var}')
                    
                    #scatter = plt.scatter(df['lon'], df['lat'], c=df[var], s=16, alpha=0.6, edgecolors='w', linewidth=0.5, cmap = ccmap[var],vmin=vvmin[var],vmax=vvmax[var])
                    
                    # Add color bar
                    #plt.colorbar(scatter, label=f'{var}')
                    
                    # Set titles and labels
                    plt.title(f'MACA {var} {period_name[period]} {scn}', fontsize=15)
                    plt.xlabel('Longitude', fontsize=12)
                    plt.ylabel('Latitude', fontsize=12)
                    
                    # Show the plot
                    #plt.grid()
                    
                    plt.savefig(f'{output_path}/map_MACA_{var}_{period_name[period]}_{scn}.png',dpi=300)
                    plt.show()

if tmap == 'WRF':
    dpath = '/media/liuming/Elements/CMIP6_usb_wrf'
    GCMS = ['access-cm2', 
            'canesm5', 
            'cesm2',       
            'cnrm-esm2-1',  
            'ec-earth3',  
            'ec-earth3-veg',
            'fgoals-g3',      
            'giss-e2-1-g',    
            'miroc6',         
            'mpi-esm1-2-hr',
            'mpi-esm1-2-lr',
            'noresm2-mm',
            'taiesm1',
            'ukesm1-0-ll']
    #GCMS = ['bcc-csm1-1']
    
    
    #GCMS = ['bcc-csm1-1']
    cmip6 = dict()
    cmip6['PPT'] = pd.DataFrame()
    cmip6['TAVG'] = pd.DataFrame()
    
    varss = {'TAVG' : 't2','PPT' : 'prec'}
    varss = {'PPT' : 'prec'}
    for var in varss:
        if not os.path.exists(f'{output_path}/map_WRF_{var}.csv'):
            for root, dirs, files in os.walk(dpath):
                for file in files:
                    file_path = os.path.join(root, file)
                    items = file.split('_')
                    varname = items[1]
                    print(file)
                    sts_name = f'mean_{file}'
                    if varname == varss[var]:
                        if not os.path.exists(f'{output_path}/mean_{file}.csv'):
                            df = pd.DataFrame()
                            
                            chunksize = 20000000
                            idx = 0
                            for chunk in pd.read_csv(file_path, chunksize=chunksize):
                                print(f'chunk:{idx}')
                                chunk['month'] = chunk['month'].astype(int)
                                chunk['monthdays'] = chunk.apply(monhdays,axis=1)
                                chunk['period'] = chunk.apply(period,axis=1)
                                chunk['wateryear'] = chunk.apply(wateryear,axis=1)
                                
                                if varname == 't2':
                                    chunk = chunk.rename(columns={varname: 'TAVG'})
                                    chunk['TAVGsum'] = chunk['TAVG'] * chunk['monthdays']
                                    chunk = chunk.groupby(['period','lat2dv','lon2dv','wateryear','scn','gcm','version','bc']).agg({'TAVGsum':'sum'}).reset_index()
                                    
                                    
                                    
                                elif varname == 'prec':
                                    chunk = chunk.rename(columns={varname: 'PPT'})
                                    chunk['PPT'] = chunk['PPT'] * chunk['monthdays'] #PPT is mm/month
                                    chunk = chunk.groupby(['period','lat2dv','lon2dv','wateryear','scn','gcm','version','bc']).agg({'PPT': 'sum'}).reset_index()
                                    
                                    
                                    
                                        
                                if df.empty:
                                    df = chunk.copy()
                                else:
                                    df = pd.concat([df,chunk],ignore_index=True)
                                idx += 1
                            
                            if varname == 't2':
                                df = df.groupby(['period','lat2dv','lon2dv','wateryear','scn','gcm','version','bc']).agg({'TAVGsum':'sum'}).reset_index()
                                df = df.groupby(['period','lat2dv','lon2dv','scn','gcm','version','bc']).agg({'TAVGsum':'mean'}).reset_index()
                                df = df.groupby(['period','lat2dv','lon2dv','scn','gcm','bc']).agg({'TAVGsum':'mean'}).reset_index()
                                df['TAVGsum'] = df['TAVGsum']/365.0
                                df = df.rename(columns={'TAVGsum': 'TAVG'})
                                    
                            elif varname == 'prec':
                                df = df.groupby(['period','lat2dv','lon2dv','wateryear','scn','gcm','version','bc']).agg({'PPT': 'sum'}).reset_index()
                                df = df.groupby(['period','lat2dv','lon2dv','scn','gcm','version','bc']).agg({'PPT': 'mean'}).reset_index()
                                df = df.groupby(['period','lat2dv','lon2dv','scn','gcm','bc']).agg({'PPT': 'mean'}).reset_index()

                            
                            df.to_csv(f'{output_path}/mean_{file}.csv')
                        else:
                            df = pd.read_csv(f'{output_path}/mean_{file}.csv')
                            
                        if varname == 't2':
                            #convert from K to celius
                            df['TAVG'] = df.apply(kelvin_to_celsius_df,axis=1)
                            if cmip6['TAVG'].empty:
                                cmip6['TAVG'] = df.copy()
                            else:
                                cmip6['TAVG'] = pd.concat([cmip6['TAVG'],df],ignore_index=True)
                        elif varname == 'prec':
                            if cmip6['PPT'].empty:
                                cmip6['PPT'] = df.copy()
                            else:
                                cmip6['PPT'] = pd.concat([cmip6['PPT'],df],ignore_index=True)
                        
            
            cmip6[var].to_csv(f'{output_path}/map_WRF_{var}.csv')
        else:
            cmip6[var] = pd.read_csv(f'{output_path}/map_WRF_{var}.csv')
            if var == 'TAVG':
                if cmip6[var][var].mean() > 200: #K
                    cmip6[var][var] = cmip6[var].apply(kelvin_to_celsius_df,axis=1)
    
       
        #hist,ssp370,
        for scn in ['hist','ssp370']:
            for period in period_name:
                for bc in ['BC','NonBC']:
                    alldf = cmip6[var]
                    df = alldf[(alldf['period'] == period) & (alldf['scn'] == scn) & (alldf['bc'] == bc)]
                    
                    df = df.groupby(['period','lat2dv','lon2dv','scn','bc']).agg({var: 'median'}).reset_index()
                    if not df.empty:
                        plt.figure(figsize=(10, 6))
                        
                        grid_value = griddata((df['lon2dv'], df['lat2dv']), df[var], (grid_lon, grid_lat), method='linear')
                        plt.imshow(grid_value, extent=(lonmin, lonmax, latmin, latmax), origin='lower', alpha=1.0, cmap=ccmap[var], vmin=vvmin[var],vmax=vvmax[var])
                        plt.colorbar(label=f'{var}')
                        
                        #scatter = plt.scatter(df['lon'], df['lat'], c=df[var], s=16, alpha=0.6, edgecolors='w', linewidth=0.5, cmap = ccmap[var],vmin=vvmin[var],vmax=vvmax[var])
                        
                        # Add color bar
                        #plt.colorbar(scatter, label=f'{var}')
                        
                        # Set titles and labels
                        plt.title(f'WRF {var} {period_name[period]} {scn} {bc}', fontsize=15)
                        plt.xlabel('Longitude', fontsize=12)
                        plt.ylabel('Latitude', fontsize=12)
                        
                        # Show the plot
                        #plt.grid()
                        
                        plt.savefig(f'{output_path}/map_WRF_{var}_{period_name[period]}_{scn}_{bc}.png',dpi=300)
                        plt.show()

