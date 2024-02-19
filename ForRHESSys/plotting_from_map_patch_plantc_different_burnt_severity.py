#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 01:45:46 2018

@author: liuming
"""

import numpy as np
import pandas as pd
import datetime
import sys 
import os
import math
from os import path
import statistics 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import cm

def to_date_column(year,mon,day):
    return datetime.date(int(year),int(mon),int(day))

#indir = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/liudebug_output/"
dict_sbs_type = {2 : 'Low Severity',3 : 'Moderate Severity',4 : 'High Severity'}
sbs_color = {2 : 'gray',3 : 'orange',4 : 'red'}
sbs_linew = {2 : 0.5,3 : 0.7,4 : 0.9}

climate_color = {'B1994' : 'b', 
                 'B1999' : 'r'}
climate_style = {'B1994' : 'solid',
                 'B1999' : 'dotted'}

plotvar = {'B1994' : 'B1994',
           'B1999' : 'B1999'}


df = dict()
for target_year in ["1994","1999"]:
    
    #scale = "patch"
    #target_var = "lai"
    #timestep = "monthly"
    #ccmap='YlGn'
    
    scale = "grow_patch"
    target_var = "plant_c"
    timestep = "yearly"
    ccmap = 'viridis_r'
    
    figure_outdir = "/home/liuming/mnt/hydronas3/Projects/NASA_Mariana/Bullrun"
    
    indir = "/home/liuming/mnt/hydronas2/Projects/UI_NASA_Bullrun/d" + target_year + "/"
    prefix = "d" + target_year
    #scale = "patch"
    
    outfile = indir + prefix + "_" + scale + "." + timestep
    
    #patch_location_file = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/auxdata/patch_location.csv"
    #patch_location_file = "/home/liuming/mnt/hydronas1/Projects/FireEarth/run_RHESSysPreprocessing/BRW/Input/rasters/patch_location_100m.csv"
    
    #patch soil burnt severity table
    #OID_,Value,Count,sbs_eagle_100m_mtbs,patches
    sbs_patch = "/home/liuming/mnt/hydronas3/Projects/NASA_Mariana/Bullrun/patch_sbs_eagle.txt"
    df_sbs_patch = pd.read_csv(sbs_patch, sep=',')
    df_sbs_patch.rename(columns={'patches': 'patchID','sbs_eagle_100m_mtbs':'sbs'}, inplace=True)
    df_sbs_patch = df_sbs_patch.drop(columns=["OID_","Value","Count"])
    
    
    #patch_location = pd.read_csv(patch_location_file, sep=',')
    
    
    df_raw = pd.read_csv(outfile, sep=r"\s+")
    df_sts = df_raw.groupby(['year','patchID'], as_index=False).max()
    sel_sts = df_sts[['patchID','year',target_var]]
    
    #join location
    #df_with_location = sel_sts.join(patch_location.set_index('patchID'), on='patchID')
    sel_sts_with_sbs = sel_sts.join(df_sbs_patch.set_index('patchID'), on='patchID')
    if target_year == '1999':
        tyear = 1998
    else:
        tyear = int(target_year)
    sel_sts_with_sbs["after_burn"] = sel_sts_with_sbs["year"] - tyear
    selsub = sel_sts_with_sbs[(sel_sts_with_sbs['after_burn'] >= -5) & (sel_sts_with_sbs['after_burn'] <= 20)]
    selsub.rename(columns={'plant_c': f'B{target_year}'}, inplace=True)
    selsub = selsub.drop(columns=["year"])
    df[target_year] = selsub.copy()
#merge 
alldf = pd.merge(df['1994'],df['1999'],on=['patchID','after_burn'])
alldf.rename(columns={'sbs_x':'sbs'}, inplace=True)
alldf = alldf.drop(columns=['sbs_y'])   

alldf_means = alldf.groupby(['sbs','after_burn'], as_index=False).mean()
linew = 0.5
plt.figure(figsize=(5, 2))
for sbs in dict_sbs_type:
  scolor = sbs_color[sbs]
  for var in ['B1994','B1999']:
      sub_data = alldf_means[(alldf_means['sbs'] == sbs)]
      plt.plot(sub_data['after_burn'], sub_data[var], label=f'{plotvar[var]} {dict_sbs_type[sbs]}', color=scolor,linestyle=climate_style[var],linewidth=sbs_linew[sbs])
      #ax.legend(fontsize=8)
      
      #plt.gca().xaxis.set_major_locator(YearLocator())
      #plt.xticks(rotation='vertical', fontsize=6, np.arange(-5, 20, step=1))
      plt.xticks(np.arange(-5, 20, step=1), rotation='vertical', fontsize=6)
      
      

 
  
plt.gca().set_ylim(bottom=0,top=32)
#plt.gca().set_ylim(bottom=-20,top=5)
plt.xlabel('After Fire')
#plt.ylabel('Change in %Canopy Cover')
plt.ylabel('Plant Biomass (kgC/m2)')
#plt.title(f'{var}')
  
plt.legend(frameon=False,loc='upper left', bbox_to_anchor=(1, 1))
outpng = f'{figure_outdir}/fig_sbs_plantc_yearly_shift.png'
plt.savefig(outpng,bbox_inches='tight', pad_inches=0.1, dpi=600)
  
plt.show()

