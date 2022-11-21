#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:05:13 2022

@author: liuming
"""
import os
import pandas as pd
import hydrostats.metrics as hm
from pyeasyga import pyeasyga
import numpy as np
import matplotlib.pyplot as plt

def to_yyyymmdd(year,month,day):
    return year*10000 + month*100 + day
def to_water_year(year,month):
    return year if month <= 9 else year + 1

#not rubust!!
end_month_day = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

outputdir = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/Output_calibrations_results"
#unit is mm/day??
fname_basin_daily_out = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/Output_calibrations/patch76620/calib_basin.daily"
#unit is m,/day??
fname_obs = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/calibration/brw_obs_str.csv"
fname_cal_evl_result = outputdir + "/" + "cal_evl_nse.txt"

evaluation_timestep = "monthly"  #yearly or daily or monthly    yearly: water year

#target_period = ["cal","evl"]
target_period = ["cal"]

cal_start_year = 1985
cal_start_month = 10
cal_end_year = 2006
cal_end_month = 9
evl_start_year = cal_end_year
evl_start_month = 10
evl_end_year = 2015  #2017
evl_end_month = 9

cal_start_yyyymmdd = to_yyyymmdd(cal_start_year,cal_start_month,1)
cal_end_yyyymmdd = to_yyyymmdd(cal_end_year,cal_end_month,end_month_day[cal_end_month])
evl_start_yyyymmdd = to_yyyymmdd(evl_start_year,evl_start_month,1)
evl_end_yyyymmdd = to_yyyymmdd(evl_end_year,evl_end_month,end_month_day[evl_end_month])

basin_daily_out = pd.read_csv(fname_basin_daily_out,delimiter=" ",header=0)
obs = pd.read_csv(fname_obs,delimiter=",",header=0)

if not os.path.exists(outputdir):
    command_line = "mkdir -p " + outputdir  
    os.system(command_line)
#if os.path.exists(fname_cal_evl_result):
#    command_line = "rm " + fname_cal_evl_result 
#    os.system(command_line)

#process obs
#obs["yyyymmdd"] = obs["year"] * 10000 + obs["month"] * 100 + obs["day"]
obs["yyyymmdd"] = obs.apply(lambda row : to_yyyymmdd(row["year"],row["month"],row["day"]), axis = 1)
obs = obs[(obs["yyyymmdd"] >= cal_start_yyyymmdd) & (obs["yyyymmdd"] <= evl_end_yyyymmdd)]
obs = obs.sort_values(by="yyyymmdd")
obs["wyear"] = obs.apply(lambda row : to_water_year(row["year"],row["month"]), axis = 1)

#process basinout
#basin_daily_out["yyyymmdd"] = basin_daily_out["year"] * 10000 + basin_daily_out["month"] * 100 + basin_daily_out["day"]
basin_daily_out["yyyymmdd"] = basin_daily_out.apply(lambda row : to_yyyymmdd(row["year"],row["month"],row["day"]), axis = 1)
sim = basin_daily_out[(basin_daily_out["yyyymmdd"] >= cal_start_yyyymmdd) & (basin_daily_out["yyyymmdd"] <= evl_end_yyyymmdd)]
sim = sim.drop_duplicates(subset=["yyyymmdd"],keep='last')[["yyyymmdd","year","month","day","streamflow"]]
sim = sim.sort_values(by="yyyymmdd")
sim["wyear"] = sim.apply(lambda row : to_water_year(row["year"],row["month"]), axis = 1)


#calclulate NSE for calibration and evaluation period
with open(fname_cal_evl_result,"w") as fout:
  for period in target_period:
    if period == "cal":
        simsub = sim[(sim["yyyymmdd"] >= cal_start_yyyymmdd) & (sim["yyyymmdd"] <= cal_end_yyyymmdd)]
        obssub = obs[(obs["yyyymmdd"] >= cal_start_yyyymmdd) & (obs["yyyymmdd"] <= cal_end_yyyymmdd)]
    else:
        simsub = sim[(sim["yyyymmdd"] >= evl_start_yyyymmdd) & (sim["yyyymmdd"] <= evl_end_yyyymmdd)]
        obssub = obs[(obs["yyyymmdd"] >= evl_start_yyyymmdd) & (obs["yyyymmdd"] <= evl_end_yyyymmdd)]
    if evaluation_timestep == "monthly":
        simsubsum = simsub.groupby(["year","month"])["streamflow"].sum()
        obssubsum = obssub.groupby(["year","month"])["obs"].sum()
    elif evaluation_timestep == "yearly":
        simsubsum = simsub.groupby(["wyear"])["streamflow"].sum()
        obssubsum = obssub.groupby(["wyear"])["obs"].sum()
    else:
        simsubsum = simsub["streamflow"]
        obssubsum = obssub["obs"]
        
    simarray = simsubsum.to_numpy()
    obsarray = obssubsum.to_numpy()
    mean_error = hm.nse(simarray, obsarray)
    print(period + "_nse:" + str("%.3f" % mean_error))
    fout.write(period + "_nse: " + str("%.3f" % mean_error) + "\n")

#sim = np.array([5, 7, 9, 2, 4.5, 6.7])
#obs = np.array([4.7, 6, 10, 2.5, 4, 6.8])
#mean_error = hm.nse(sim, obs)

#fig, ax = plt.subplots()
#ax.plot(obs, sim, 'o', color='black')

#print(mean_error)