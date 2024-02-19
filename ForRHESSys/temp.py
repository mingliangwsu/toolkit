#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:05:13 2022

@author: liuming
"""
import os
import pandas as pd
import hydrostats.metrics as hm
#from scipy.optimize import differential_evolution
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator
#from RHESSys_cal_nse_function import *
#from pyDOE import *
def get_sections_with_increasing_dates(df):
    increasing_sections = []

    # Iterate through the DataFrame to find increasing sections
    for index, row in df.iterrows():
        if index == 0:
            increasing_sections.append(pd.DataFrame(row).T)
        elif row["date"] > df.loc[index - 1, "date"]:
            increasing_sections.append(pd.DataFrame(row).T)
        else:
            increasing_sections = []
            increasing_sections.append(pd.DataFrame(row).T)
    # Concatenate the list of DataFrames
    result_df = pd.concat(increasing_sections, ignore_index=True)
    return result_df

model_output_root = "/home/liuming/mnt/hydronas2/Projects/UI_NASA_Bullrun"
figure_outdir = "/home/liuming/mnt/hydronas3/Projects/NASA_Mariana/Bullrun"

#climate_color = {'precip' : 'k',
#                 'b1994' : 'b', 
#                 'b1999' : 'r',
#                 'bnone' : 'y'}
#climate_style = {'precip' : 'solid',
#                 'b1994' : 'dotted',
#                 'b1999' : 'dashed',
#                 'bnone' : 'dashdot'}

climate_color = {'precip' : 'k',
                 'b1994' : 'b', 
                 'b1999' : 'r',
                 'bnone_1994' : 'k',
                 'bnone_1999' : 'g'}
climate_style = {'precip' : 'solid',
                 'b1994' : 'dotted',
                 'b1999' : 'dashed',
                 'bnone_1994' : 'dashdot',
                 'bnone_1999' : 'dashdot'}

plotvar = {'b1994' : 'B1994',
           'b1999' : 'B1999',
           'bnone_1994' : "bnone_1994",
           'bnone_1999' : "bnone_1999"}

#USGS observation
#fname_obs = "/home/liuming/mnt/hydronas3/Projects/WWS_Oregon/USGS_gages_observation/usgs_14163000_mm_per_day.csv"

#evaluation_timesteps = ["yearly","monthly","daily"]  #yearly or daily or monthly    yearly: water year

output_file = 'grow_basin.daily'
output_var = "lai"
k = 0.3
#output_var = "litrc" # "plantc"
#outunit = "m2/m2"
#outunit = "KgC/m2"
outunit = "%"
plot_ouput_var = "CanopyCover"
#if output_var = "lai":
#   plot_ouput_var = "CanopyCover" 
monthly_cal_use_mean = "max" #"mean" "sum"


columns_to_keep = ["year", "month", "day", "date", output_var]
#evaluation_timesteps = ["monthly"] 
obs_years = list(range(1979, 2023))
byears = ['1994','1999','none']
sel_df = dict()

def lai_to_cc(row):
    return 100 * (1.0 - np.exp(-row['lai'] * k))



for c_burnt_year in byears:
    if c_burnt_year in ['none']:
      RHESSys_outputdir = model_output_root + "/b" + c_burnt_year 
    else:
      RHESSys_outputdir = model_output_root + "/d" + c_burnt_year   
    #os.chdir(droot)
    
    if True:
        #output_pre = RHESSys_outputdir + '/real_run_' + clim
        if c_burnt_year in ['none']:
          fname_basin_daily_out = RHESSys_outputdir + '/b' + c_burnt_year + "_" + output_file
        else:
          fname_basin_daily_out = RHESSys_outputdir + '/d' + c_burnt_year + "_" + output_file  
        basin_daily_out = pd.read_csv(fname_basin_daily_out,delimiter=" ",header=0)
        
        #in some case the basin output's last row is wrong, need double check!
        if (basin_daily_out.iloc[-1]['year'] != basin_daily_out.iloc[-2]['year']) or (basin_daily_out.iloc[-1]['day'] == 0) or (basin_daily_out.iloc[-1]['month'] == 0) :
          basin_daily_out = basin_daily_out.drop(basin_daily_out.index[-1])
        
        basin_daily_out['date'] = pd.to_datetime(basin_daily_out[["year", "month", "day"]])
        #unit is m,/day??
    
        #results after spin ups
        sel = get_sections_with_increasing_dates(basin_daily_out).loc[:, columns_to_keep]
        sel_df[c_burnt_year] = sel[sel['year'].isin(obs_years)]
        new_stream_name = 'b' + c_burnt_year
        sel_df[c_burnt_year][output_var] = sel_df[c_burnt_year].apply(lai_to_cc, axis=1)
        sel_df[c_burnt_year].rename(columns={output_var: new_stream_name}, inplace=True)
    
    #Join all climate results and observations
if True:
    alldata = pd.DataFrame()
    for index,byear in enumerate(byears):
        if index == 0:
            alldata = sel_df[byear]
        else:
            alldata = pd.merge(alldata,sel_df[byear],on="date",how="left")
            if "year_y" in alldata.columns:
                alldata = alldata.drop(columns=["year_y","month_y","day_y"])
            if "year_x" in alldata.columns:
                alldata = alldata.drop(columns=["year_x","month_x","day_x"])
            
    
    
    if "year_y" in alldata.columns:
        alldata = alldata.drop(columns=["year_y","month_y","day_y"])
    if "year_x" in alldata.columns:
        alldata = alldata.drop(columns=["year_x","month_x","day_x"])
    alldata.set_index('date', inplace=True)
    #alldata = alldata.drop(columns=["precip_y"])
    #alldata.rename(columns={"precip_x": "precip"}, inplace=True)
    #remove all duplicated columns
    alldata = alldata.loc[:, ~alldata.columns.duplicated()]
    if monthly_cal_use_mean == "mean":
      monthly_means = alldata.resample('M').mean()
      annual_means = alldata.resample('Y').mean()
      multiyear_monthly_means = alldata.groupby(alldata.index.month).mean()
    elif monthly_cal_use_mean == "sum":
      monthly_means = alldata.resample('M').sum()
      annual_means = alldata.resample('Y').sum()
      multiyear_monthly_means = alldata.groupby(alldata.index.month).mean() 
    elif monthly_cal_use_mean == "max":
      monthly_means = alldata.resample('M').max()
      annual_means = alldata.resample('Y').max()
      multiyear_monthly_means = alldata.groupby(alldata.index.month).mean()
      
    annual_means_1994 = annual_means[["year","b1994",'bnone']]
    annual_means_1994["after_burn"] = annual_means["year"] - 1994
    annual_means_1994["bnone_1994"] = annual_means["bnone"]
    annual_means_1994 = annual_means_1994.drop(columns=["year","bnone"])
    
    annual_means_1999 = annual_means[["year",'b1999','bnone']]
    annual_means_1999["after_burn"] = annual_means["year"] - 1999
    annual_means_1999["bnone_1999"] = annual_means["bnone"]
    annual_means_1999 = annual_means_1999.drop(columns=["year","bnone"])
    
    annual_means_1994_sub = annual_means_1994[(annual_means_1994['after_burn'] >= -5) & (annual_means_1994['after_burn'] <= 20)]
    annual_means_1999_sub = annual_means_1999[(annual_means_1994['after_burn'] >= -5) & (annual_means_1999['after_burn'] <= 20)]
    merged_df = pd.merge(annual_means_1994_sub, annual_means_1999_sub, on='after_burn', how='inner')
    
    #merged_df['b1994'] = merged_df['b1994'] - merged_df['bnone_1994']
    #merged_df['b1999'] = merged_df['b1999'] - merged_df['bnone_1999']


    linew = 0.5

    #plot_times = ['daily','monthly','annual','mean_monthly']
    plot_times = ['annual']
    #plot_times = ['mean_monthly']
    climate_vars = list(plotvar.keys()) #['precip','b1994_streamflow','b1999_streamflow'] #alldata.columns.tolist()
    outstyle = dict()
    for var in climate_vars:
        outstyle[var] = 'precip'
        for style in climate_color:
            if style in var:
                outstyle[var] = style
    #plot_time = 'mean_monthly'
    for plot_time in plot_times:
      #Plot time series
      plt.figure(figsize=(5, 2))
      if plot_time == 'annual':
            #annual
            #for var in climate_vars:
            for var in ['b1994','b1999']:
              plt.plot(merged_df['after_burn'], merged_df[var], label=plotvar[var], color=climate_color[outstyle[var]],linestyle=climate_style[outstyle[var]],linewidth=linew)
            #plt.gca().xaxis.set_major_locator(YearLocator())
            #plt.xticks(rotation='vertical', fontsize=6, np.arange(-5, 20, step=1))
            plt.xticks(np.arange(-5, 20, step=1), rotation='vertical', fontsize=6)
            
  
       
    
      plt.gca().set_ylim(bottom=70,top=100)
      #plt.gca().set_ylim(bottom=-20,top=5)
      plt.xlabel('After Fire')
      #plt.ylabel('Change in %Canopy Cover')
      plt.ylabel('Canopy Cover (%)')
      #plt.title(f'{var}')
        
      plt.legend(frameon=False,loc='upper left', bbox_to_anchor=(1, 1))
      #outpng = f'{figure_outdir}/fig_{plot_ouput_var}_{plot_time}_shift.png'
      outpng = f'{figure_outdir}/test_fig_{plot_ouput_var}_{plot_time}_shift.png'
      plt.savefig(outpng,bbox_inches='tight', pad_inches=0.1, dpi=600)
    
      plt.show()
