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
    
RHESSys_outputdir="/home/liuming/mnt/hydronas3/Projects/WWS_Oregon/Output_realrun_11072023"
#os.chdir(droot)

outputdir = RHESSys_outputdir
outnse = f'{outputdir}/nse_performace.txt'


#USGS observation
fname_obs = "/home/liuming/mnt/hydronas3/Projects/WWS_Oregon/USGS_gages_observation/usgs_14163000_mm_per_day.csv"

landcover_years = ['2001','2021']
print_start_ends = {1981: 1989, 2021: 2022}

with open(outnse,"w") as foutnse:    
    for landcover_year in landcover_years:
        for print_start in print_start_ends:
            #evaluation_timesteps = ["yearly","monthly","daily"]  #yearly or daily or monthly    yearly: water year
            #evaluation_timesteps = ["monthly"] 
            print(f'landcover_year:{landcover_year} print_start:{print_start}')
            
            obsdata = pd.read_csv(fname_obs,delimiter=",",header=0)
            obsdata['date'] = pd.to_datetime(obsdata[["year", "month", "day"]])
            
            #data
            obs_years = list(set(obsdata["year"].tolist()))
            
            columns_to_keep = ["year", "month", "day", "date", "streamflow", "precip"]
            
            climates = ["daymet","prism","gridmet"] #,"gridmet"]
            climate_color = {'obs' : 'k',
                             'daymet' : 'b', 
                             'gridmet' : 'r',
                             'prism' : 'y'}
            climate_style = {'obs' : 'solid',
                             'daymet' : 'dotted',
                             'gridmet' : 'dashed',
                             'prism' : 'dashdot'}
            
            sel_df = dict()
            for clim in climates:
                #output_pre = RHESSys_outputdir + '/real_run_' + clim
                fname_basin_daily_out = f'{RHESSys_outputdir}/{clim}_{landcover_year}/real_run_{clim}_basin.daily'
                basin_daily_out = pd.read_csv(fname_basin_daily_out,delimiter=" ",header=0)
                basin_daily_out['date'] = pd.to_datetime(basin_daily_out[["year", "month", "day"]])
                #unit is m,/day??
            
                #results after spin ups
                sel = get_sections_with_increasing_dates(basin_daily_out).loc[:, columns_to_keep]
                sel_df[clim] = sel[sel['year'].isin(obs_years)]
                new_stream_name = clim + '_streamflow'
                new_ppt_name = clim + '_precip'
                sel_df[clim].rename(columns={"streamflow": new_stream_name,"precip" : new_ppt_name}, inplace=True)
            
            #Join all climate results and observations
            alldata = pd.DataFrame()
            for index,clim in enumerate(climates):
                if index == 0:
                    alldata = sel_df[clim]
                else:
                    alldata = pd.merge(alldata,sel_df[clim],on="date",how="left")
                    if "year_y" in alldata.columns:
                        alldata = alldata.drop(columns=["year_y","month_y","day_y"])
                    if "year_x" in alldata.columns:
                        alldata = alldata.drop(columns=["year_x","month_x","day_x"])
                    
            
            #join observation
            alldata = pd.merge(alldata,obsdata,on="date",how="left")
            if "year_y" in alldata.columns:
                alldata = alldata.drop(columns=["year_y","month_y","day_y"])
            if "year_x" in alldata.columns:
                alldata = alldata.drop(columns=["year_x","month_x","day_x"])
            alldata.set_index('date', inplace=True)
            
            
            alldata = alldata.loc[f'{print_start}-01-01':f'{print_start_ends[print_start]}-12-31']
            
            monthly_means = alldata.resample('M').sum()
            annual_means = alldata.resample('Y').sum()
            multiyear_monthly_means = alldata.groupby(alldata.index.month).mean()
            
            linew = 0.5
            
            plot_times = ['daily','monthly','annual','mean_monthly']
            climate_vars = ['streamflow','precip']
            #plot_time = 'mean_monthly'
            for plot_time in plot_times:
              #Plot time series
              for var in climate_vars: #climate_vars:
                plt.figure(figsize=(5, 2))
                for index,climate in enumerate(climates):
                  varname = climate + '_' + var
                  if plot_time == 'daily':
                    #daily
                    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
                    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
    
                    plt.plot(alldata.index, alldata[varname], label=climate,color=climate_color[climate],linestyle=climate_style[climate],linewidth=linew)
                    if index == (len(climates)-1) and var == 'streamflow':
                        plt.plot(alldata.index, alldata['obs'], label='obs',color=climate_color['obs'],linestyle=climate_style['obs'],linewidth=linew)
                        
                    if var == 'streamflow':
                        simsubsum = alldata[varname]
                        obssubsum = alldata['obs']
            
                    
                  elif plot_time == 'monthly':
                    #monthly
                    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
                    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
                    plt.plot(monthly_means.index, monthly_means[varname], label=climate,color=climate_color[climate],linestyle=climate_style[climate],linewidth=linew)
                    if index == (len(climates)-1) and var == 'streamflow':
                        plt.plot(monthly_means.index, monthly_means['obs'], label='obs',color=climate_color['obs'],linestyle=climate_style['obs'],linewidth=linew)
                        plt.ylim(0, 500)
                        
                    if var == 'streamflow':
                        simsubsum = monthly_means[varname]
                        obssubsum = monthly_means['obs']
                        
                  elif plot_time == 'annual':
                    #annual
                    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
                    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
                    plt.plot(annual_means.index, annual_means[varname], label=climate, color=climate_color[climate], linestyle=climate_style[climate],linewidth=linew)
                    if index == (len(climates)-1) and var == 'streamflow':
                        plt.plot(annual_means.index, annual_means['obs'], label='obs', color=climate_color['obs'], linestyle=climate_style['obs'],linewidth=linew)
                    if var == 'streamflow':
                        simsubsum = annual_means[varname]
                        obssubsum = annual_means['obs']   
                    
                  elif plot_time == 'mean_monthly':
                    #multi-year monthly average
                    plt.plot(multiyear_monthly_means.index, multiyear_monthly_means[varname], label=climate, color=climate_color[climate],linestyle=climate_style[climate],linewidth=linew)
                    plt.xticks(range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
                    if index == (len(climates)-1) and var == 'streamflow':
                        plt.plot(multiyear_monthly_means.index, multiyear_monthly_means['obs'], label='obs', color=climate_color['obs'],linestyle=climate_style['obs'],linewidth=linew)
                        plt.ylim(0, 500)
                        plt.xticks(range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
                    if var == 'streamflow':
                        simsubsum = multiyear_monthly_means[varname]
                        obssubsum = multiyear_monthly_means['obs']
                  #Calculate NSE
                  if var == 'streamflow':
                      simarray = simsubsum.to_numpy(dtype=np.float64)
                      obsarray = obssubsum.to_numpy(dtype=np.float64)
                      mean_error = hm.nse(simarray, obsarray)
                      outtxt = f'LC{landcover_year} {print_start}-{print_start_ends[print_start]} {climate} NSE {plot_time} = {mean_error:.2f}'
                      print(outtxt)
                      foutnse.write(f'{outtxt}\n')
                
                    
            
            
                plt.xlabel('Time')
                plt.ylabel(var)
                plt.title(f'{var}')
                
                plt.legend(frameon=False,loc='upper left', bbox_to_anchor=(1, 1))
                outpng = f'{outputdir}/calibrated_fig_output_{var}_{plot_time}_landcoveryear_{landcover_year}_f{print_start}_t{print_start_ends[print_start]}.png'
                plt.savefig(outpng,bbox_inches='tight', pad_inches=0.1, dpi=600)
            
                plt.show()