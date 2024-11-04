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

#historical period comparison: 1980/10 ~ 2005/9:1
#GCM period 2025/10 ~ 2055/9:2 and 2055/10 ~ 2085/9:3

monthdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def monhdays(row):
    return monthdays[row['month'] - 1]

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

output_path = '/home/liuming/mnt/hydronas3/Projects/CMIP6_Data/statistics'
fgridmet = '/home/liuming/mnt/hydronas3/Projects/CMIP6_Data/statistics/WRF_MACA_Gridmet_mean/GRIDMET_VIC_GRIDMET_yearmonth_mean.csv'

gridmet = pd.read_csv(fgridmet)

gridmet['monthdays'] = gridmet.apply(monhdays,axis=1)
gridmet['PPT'] = gridmet['PPT'] * gridmet['monthdays'] #PPT is mm/month
gridmet['TAVG'] = (gridmet['TMAX'] + gridmet['TMIN']) / 2.0
gridmet['period'] = gridmet.apply(period,axis=1)
gridmet['wateryear'] = gridmet.apply(wateryear,axis=1)


GCMS = ['bcc-csm1-1','HadGEM2-ES365','BNU-ESM','inmcm4','CanESM2','IPSL-CM5A-LR',
        'CNRM-CM5','IPSL-CM5A-MR','CSIRO-Mk3-6-0','IPSL-CM5B-LR','GFDL-ESM2G',
        'MIROC5','GFDL-ESM2M','MIROC-ESM-CHEM','MIROC-ESM','HadGEM2-CC365','MRI-CGCM3']
#GCMS = ['bcc-csm1-1','HadGEM2-ES365','BNU-ESM','inmcm4','CanESM2','IPSL-CM5A-LR',
#        'CNRM-CM5','IPSL-CM5A-MR','CSIRO-Mk3-6-0','IPSL-CM5B-LR','GFDL-ESM2G',
#        'MIROC5','GFDL-ESM2M','MIROC-ESM-CHEM','MIROC-ESM','HadGEM2-CC365']

cmip5 = pd.DataFrame()

for gcm in GCMS:
    df = pd.read_csv(f'/home/liuming/mnt/hydronas3/Projects/CMIP6_Data/statistics/WRF_MACA_Gridmet_mean/{gcm}_VIC_GCM_yearmonth_mean.csv')
    if cmip5.empty:
        cmip5 = df.copy()
    else:
        cmip5 = pd.concat([cmip5,df],ignore_index=True)
cmip5['monthdays'] = cmip5.apply(monhdays,axis=1)
cmip5['PPT'] = cmip5['PPT'] * cmip5['monthdays'] #PPT is mm/month
cmip5['TAVG'] = (cmip5['TMAX'] + cmip5['TMIN']) / 2.0
cmip5['period'] = cmip5.apply(period,axis=1)
cmip5['wateryear'] = cmip5.apply(wateryear,axis=1)


WRF_vars = ['lw_dwn','sw_dwn','q2','rh','t2','t2max','t2min','prec','wspd10mean']
#WRF_vars = ['prec','t2']
allWRF = pd.DataFrame()
for WRF_var in WRF_vars:
    df = pd.read_csv(f'/home/liuming/mnt/hydronas3/Projects/CMIP6_Data/statistics/WRF_MACA_Gridmet_mean/new_{WRF_var}.yearmonth.mean.csv')
    df_sorted = df.sort_values(by=['model','version','region', 'scn', 'bc', 'year', 'month'])
    df_sorted['month'] = df_sorted['month'].astype(int)
    df_sorted['monthdays'] = df_sorted.apply(monhdays,axis=1)
    if WRF_var == 'prec':
        df_sorted[WRF_var] = df_sorted[WRF_var] * df_sorted['monthdays'] #PPT is mm/month
    if WRF_var in ['t2','t2max','t2min']:
        df_sorted[WRF_var] = df_sorted[WRF_var].apply(kelvin_to_celsius)
        
    df_sorted['period'] = df_sorted.apply(period,axis=1)
    df_sorted['wateryear'] = df_sorted.apply(wateryear,axis=1)
    df_sorted = df_sorted.reset_index(drop=True)
    if allWRF.empty:
        allWRF = df_sorted.copy()
    else:
        allWRF[WRF_var] = df_sorted[WRF_var]


#making box plot
#regions = ['WA','CRB']
regions = ['WA','CRB_USA']
outvars = ['prec','tavg','tmax','tmin'] #output name
periods = [1,2,3]

var_vic = {'prec':'PPT','tavg':'TAVG','tmax':'TMAX','tmin':'TMIN'}
var_wrf = {'prec':'prec','tavg':'t2','tmax':'t2max','tmin':'t2min'} 
var_title = {'prec':'Prec (mm/year)','tavg':'Tavg (°C)','tmax':'Tmax (°C)','tmin':'Tmin (°C)'} 

data = dict()
for var in outvars:
    data[var] = pd.DataFrame()
    if var == 'prec':
        #gridmet
        df = gridmet.groupby(['period','wateryear','region']).agg({var_vic[var]: 'sum'}).reset_index()
        df = df[df['period'] == 1]
        df = df.groupby(['period','region']).agg({var_vic[var]: 'mean'}).reset_index()
        df.rename(columns={var_vic[var]: var}, inplace=True)
        df['CLM'] = 'GridMet'
        if data[var].empty:
            data[var] = df.copy()
        
        #CMIP5 MACA
        cdf = cmip5.groupby(['period','wateryear','region','model','scn']).agg({var_vic[var]: 'sum'}).reset_index()
        cdf = cdf[cdf['period'] >= 1]
        cdf = cdf.groupby(['period','region','model','scn']).agg({var_vic[var]: 'mean'}).reset_index()
        cdf['CLM'] = 'MACA'
        cdf.rename(columns={var_vic[var]: var}, inplace=True)
        data[var] = pd.concat([data[var],cdf],ignore_index=True)
        
        #WRF
        wcdf = allWRF.groupby(['period','wateryear','region','model','scn','version','bc']).agg({var_wrf[var]: 'sum'}).reset_index()
        wcdf = wcdf[wcdf['period'] >= 1]
        wcdf.rename(columns={var_wrf[var]: var}, inplace=True)
        wcdf = wcdf.groupby(['period','region','model','scn','bc']).agg({var: 'mean'}).reset_index()  #versions were put input same model
        wcdf['CLM'] = 'WRF'
        wcdf = wcdf[(wcdf['scn'] != 'ssp245') & (wcdf['scn'] != 'ssp585') & (wcdf['region'] != 'WRFDOMAIN')]
        data[var] = pd.concat([data[var],wcdf],ignore_index=True)
    elif var in ['tavg','tmax','tmin']:
        #gridmet
        #gridmet
        #df = gridmet.groupby(['period','wateryear','region']).agg({var_vic[var]: 'sum'}).reset_index()
        
        grouped_df = gridmet.groupby(['period','wateryear','region']).apply(
            lambda x: weighted_mean(x[[var_vic[var],'monthdays']], 'monthdays')
            ).drop(columns='monthdays').reset_index()
        
        
        df = grouped_df[grouped_df['period'] == 1]
        df = df.groupby(['period','region']).agg({var_vic[var]: 'mean'}).reset_index()
        df.rename(columns={var_vic[var]: var}, inplace=True)
        df['CLM'] = 'GridMet'
        if data[var].empty:
            data[var] = df.copy()
        
        #CMIP5 MACA
        #cdf = cmip5.groupby(['period','wateryear','region','model','scn']).agg({var_vic[var]: 'sum'}).reset_index()
        grouped_df = cmip5.groupby(['period','wateryear','region','model','scn']).apply(
            lambda x: weighted_mean(x[[var_vic[var],'monthdays']], 'monthdays')
            ).drop(columns='monthdays').reset_index()
        
        
        
        cdf = grouped_df[grouped_df['period'] >= 1]
        cdf = cdf.groupby(['period','region','model','scn']).agg({var_vic[var]: 'mean'}).reset_index()
        cdf['CLM'] = 'MACA'
        cdf.rename(columns={var_vic[var]: var}, inplace=True)
        data[var] = pd.concat([data[var],cdf],ignore_index=True)
        
        #WRF
        #wcdf = allWRF.groupby(['period','wateryear','region','model','scn','version','bc']).agg({var_wrf[var]: 'sum'}).reset_index()
        grouped_df = allWRF.groupby(['period','wateryear','region','model','scn','version','bc']).apply(
            lambda x: weighted_mean(x[[var_wrf[var],'monthdays']], 'monthdays')
            ).drop(columns='monthdays').reset_index()
        
        
        wcdf = grouped_df[grouped_df['period'] >= 1]
        wcdf.rename(columns={var_wrf[var]: var}, inplace=True)
        wcdf = wcdf.groupby(['period','region','model','scn','bc']).agg({var: 'mean'}).reset_index()  #versions were put input same model
        wcdf['CLM'] = 'WRF'
        wcdf = wcdf[(wcdf['scn'] != 'ssp245') & (wcdf['scn'] != 'ssp585') & (wcdf['region'] != 'WRFDOMAIN')]
        data[var] = pd.concat([data[var],wcdf],ignore_index=True)
        

new_xtick_labels = ['GridMet Hist', 'MACA Hist', 'WRF BC Hist ', 'WRF NoBC Hist',
                    'MACA RCP45 2040s', 'MACA RCP85 2040s', 
                    'WRF BC 2040s', 'WRF NonBC 2040s',
                    'MACA RCP45 2070s', 'MACA RCP85 2070s', 
                    'WRF BC 2070s', 'WRF NonBC 2070s'
                    ]

for var in outvars:
    for region in regions:
        subregion = data[var][data[var]['region'] == region]
        subregion = subregion.sort_values(by=['period','CLM','scn', 'bc', 'model'])
        # Group by 4 columns
        subregion['scn'].fillna('N/A', inplace=True)
        subregion['bc'].fillna('N/A', inplace=True)
        subregion['model'].fillna('N/A', inplace=True)
        
        outdf = subregion.groupby(['period','CLM','scn','bc']).agg({var: 'mean'}).reset_index()  #versions were put input same model
        outdf.to_csv(f'{output_path}/{region}_{var}_mean_all.csv', index=False)
        
        plt.figure(figsize=(25, 14), dpi=300) 
        subregion.boxplot(column=var, by=['period','CLM','scn', 'bc'], grid=False, rot=90)
        
        plt.axvline(x=4.5, color='red', linestyle='--', label='')
        plt.axvline(x=6.5, color='gray', linestyle='--', label='', linewidth=0.5)
        plt.axvline(x=8.5, color='blue', linestyle='--', label='')
        plt.axvline(x=10.5, color='gray', linestyle='--', label='', linewidth=0.5)
        ax = plt.gca()
        
        for i, label in enumerate(new_xtick_labels):
            ax.set_xticklabels([label if j == i else tick for j, tick in enumerate(ax.get_xticklabels())], rotation=90)
        # Show the plot
        plt.xticks(fontsize=8)
        plt.suptitle(region)  # Suppress the default 'Boxplot grouped by' title
        plt.title('')
        plt.xlabel('Groups')
        plt.ylabel(var_title[var])
        if var == 'prec':
            plt.ylim(bottom=0)
        
        plt.savefig(f'{output_path}/{region}_{var}_boxplot.png',format='png', dpi=300, bbox_inches='tight')

        plt.tight_layout()
        plt.show()
