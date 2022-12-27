#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:05:13 2022

@author: liuming
"""
#import os
#import pandas as pd
import hydrostats.metrics as hm
#from pyeasyga import pyeasyga
#import numpy as np
#import matplotlib.pyplot as plt

def to_yyyymmdd(year,month,day):
    return int(year*10000 + month*100 + day)
def to_water_year(year,month):
    return int(year if month <= 9 else year + 1)

#not rubust!! Febmay not right. But normally should be a complete water year
end_month_day = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

def calculate_nse(obsdf,simdf,evaluation_timestep,start_year,start_month,end_year,end_month):
    start_yyyymmdd = to_yyyymmdd(start_year,start_month,1)
    end_yyyymmdd = to_yyyymmdd(end_year,end_month,end_month_day[end_month])
    obs = obsdf.copy()
    sim = simdf.copy()

    #process obs

    obs["yyyymmdd"] = obs.apply(lambda row : to_yyyymmdd(row["year"],row["month"],row["day"]), axis = 1)
    obs = obs[(obs["yyyymmdd"] >= start_yyyymmdd) & (obs["yyyymmdd"] <= end_yyyymmdd)]
    obs = obs.sort_values(by="yyyymmdd")
    obs["wyear"] = obs.apply(lambda row : to_water_year(row["year"],row["month"]), axis = 1)

    #process basinout
    #basin_daily_out["yyyymmdd"] = basin_daily_out["year"] * 10000 + basin_daily_out["month"] * 100 + basin_daily_out["day"]
    sim["yyyymmdd"] = sim.apply(lambda row : to_yyyymmdd(row["year"],row["month"],row["day"]), axis = 1)
    sim = sim[(sim["yyyymmdd"] >= start_yyyymmdd) & (sim["yyyymmdd"] <= end_yyyymmdd)]
    sim = sim.drop_duplicates(subset=["yyyymmdd"],keep='last')[["yyyymmdd","year","month","day","streamflow"]]
    sim = sim.sort_values(by="yyyymmdd")
    sim["wyear"] = sim.apply(lambda row : to_water_year(row["year"],row["month"]), axis = 1)


    #calclulate NSE for calibration and evaluation period
    simsub = sim[(sim["yyyymmdd"] >= start_yyyymmdd) & (sim["yyyymmdd"] <= end_yyyymmdd)]
    obssub = obs[(obs["yyyymmdd"] >= start_yyyymmdd) & (obs["yyyymmdd"] <= end_yyyymmdd)]

    #print("evaluation_timestep:" + evaluation_timestep)
    if evaluation_timestep == "monthly":
        simsubsum = simsub.groupby(["year","month"])["streamflow"].sum()
        obssubsum = obssub.groupby(["year","month"])["obs"].sum()
    elif evaluation_timestep == "yearly":
        simsubsum = simsub.groupby(["wyear"])["streamflow"].sum()
        obssubsum = obssub.groupby(["wyear"])["obs"].sum()
    else:
        simsubsum = simsub["streamflow"]
        obssubsum = obssub["obs"]
    #display(simsub)
    #display(obssub)
    
    simarray = simsubsum.to_numpy()
    obsarray = obssubsum.to_numpy()
    mean_error = hm.nse(simarray, obsarray)
    return mean_error

def calculate_nse_and_return_dftable(obsdf,simdf,evaluation_timestep,start_year,start_month,end_year,end_month):
    start_yyyymmdd = to_yyyymmdd(start_year,start_month,1)
    end_yyyymmdd = to_yyyymmdd(end_year,end_month,end_month_day[end_month])
    obs = obsdf.copy()
    sim = simdf.copy()

    #process obs

    obs["yyyymmdd"] = obs.apply(lambda row : to_yyyymmdd(row["year"],row["month"],row["day"]), axis = 1)
    obs = obs[(obs["yyyymmdd"] >= start_yyyymmdd) & (obs["yyyymmdd"] <= end_yyyymmdd)]
    obs = obs.sort_values(by="yyyymmdd")
    obs["wyear"] = obs.apply(lambda row : to_water_year(row["year"],row["month"]), axis = 1)

    #process basinout
    #basin_daily_out["yyyymmdd"] = basin_daily_out["year"] * 10000 + basin_daily_out["month"] * 100 + basin_daily_out["day"]
    sim["yyyymmdd"] = sim.apply(lambda row : to_yyyymmdd(row["year"],row["month"],row["day"]), axis = 1)
    sim = sim[(sim["yyyymmdd"] >= start_yyyymmdd) & (sim["yyyymmdd"] <= end_yyyymmdd)]
    sim = sim.drop_duplicates(subset=["yyyymmdd"],keep='last')[["yyyymmdd","year","month","day","streamflow"]]
    sim = sim.sort_values(by="yyyymmdd")
    sim["wyear"] = sim.apply(lambda row : to_water_year(row["year"],row["month"]), axis = 1)


    #calclulate NSE for calibration and evaluation period
    simsub = sim[(sim["yyyymmdd"] >= start_yyyymmdd) & (sim["yyyymmdd"] <= end_yyyymmdd)]
    obssub = obs[(obs["yyyymmdd"] >= start_yyyymmdd) & (obs["yyyymmdd"] <= end_yyyymmdd)]
    
    

    #print("evaluation_timestep:" + evaluation_timestep)
    if evaluation_timestep == "monthly":
        simsubsum = simsub.groupby(["year","month"])["streamflow"].sum()
        obssubsum = obssub.groupby(["year","month"])["obs"].sum()
        outsimsubsum = simsub.groupby(by=["year","month"],as_index=False)["streamflow"].sum()
        outobssubsum = obssub.groupby(by=["year","month"],as_index=False)["obs"].sum()
    elif evaluation_timestep == "yearly":
        simsubsum = simsub.groupby(["wyear"])["streamflow"].sum()
        obssubsum = obssub.groupby(["wyear"])["obs"].sum()
        outsimsubsum = simsub.groupby(by=["wyear"],as_index=False)["streamflow"].sum()
        outobssubsum = obssub.groupby(by=["wyear"],as_index=False)["obs"].sum()
    elif evaluation_timestep == "daily":
        simsubsum = simsub["streamflow"]
        obssubsum = obssub["obs"]
        #print("simsubsum.columns\n" + simsubsum.columns)
        outsimsubsum = simsub[["year","month","day","streamflow"]]
        outobssubsum = obssub[["year","month","day","obs"]]
    #display(simsub)
    #display(obssub)
    
    simarray = simsubsum.to_numpy()
    obsarray = obssubsum.to_numpy()
    mean_error = hm.nse(simarray, obsarray)
    return mean_error,outsimsubsum,outobssubsum