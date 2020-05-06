#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 02:29:37 2020

@author: liuming
"""


from datetime import date
import pandas as pd
import numpy as np
from numpy import genfromtxt

#import os
#import os.path
import math
import array

datapath="/home/liuming/mnt/hydronas1/Projects/UW_subcontract/results/parameter_sensitivity"
outfile_annual=datapath + "/all_annual_daily_mean.csv"
outfile_monthmean=datapath + "/all_month_mean.csv"
outfile_annualmean=datapath + "/all_annual_mean.csv"
outfile_annualpeak=datapath + "/all_annual_peak.csv"
outfile_annuallow=datapath + "/all_annual_low.csv"
outfile_annualmonthpeak=datapath + "/all_annual_month_peak.csv"
outfile_annualmonthlow=datapath + "/all_annual_month_low.csv"

#experiments = [*range(0, 20, 1)]
experiments = [*range(0, 20, 1)]
dateidx = ["YEAR","MONTH","DAY"]

alldf = pd.DataFrame()

for sim in experiments:
    filename = datapath + "/" + str(sim) + "_mean.txt"
    #my_data = genfromtxt(filename, delimiter=',',skip_header=1)
    my_data = pd.read_csv(filename)  
    my_data["s" + str(sim) + "_Runoff_day"] = my_data["RUNOFF_AREA"] / my_data["AREA"]
    my_data["s" + str(sim) + "_Baseflow_day"] = my_data["BASEFLOW_AREA"] / my_data["AREA"]
    my_data["s" + str(sim) + "_TotalR_day"] = my_data["TOTR_AREA"] / my_data["AREA"]
    selyears = my_data[my_data.YEAR >= 1985]
    cols = ["YEAR","MONTH","DAY","s" + str(sim) + "_Runoff_day","s" + str(sim) + "_Baseflow_day","s" + str(sim) + "_TotalR_day"]
    selected = selyears[cols]
    if sim == 0:
        alldf = selected
    else:
        alldf = alldf.merge(selected,left_on=dateidx, right_on=dateidx)
        
alldf_monthmean = alldf.groupby(['MONTH']).mean().reset_index().drop(columns=["YEAR","DAY"])
alldf_annualmean = alldf.groupby(['YEAR']).mean().reset_index().drop(columns=["MONTH","DAY"])
alldf_annualpeak = alldf.groupby(['YEAR']).max().reset_index().drop(columns=["MONTH","DAY"])
alldf_annuallow = alldf.groupby(['YEAR']).min().reset_index().drop(columns=["MONTH","DAY"])
alldf_annualmonthpeak = alldf.groupby(['YEAR','MONTH']).max().reset_index().drop(columns=["DAY"])
alldf_annualmonthlow = alldf.groupby(['YEAR','MONTH']).min().reset_index().drop(columns=["DAY"])

#export to csv files
alldf.to_csv(outfile_annual, index=False)
alldf_monthmean.to_csv(outfile_monthmean, index=False)
alldf_annualmean.to_csv(outfile_annualmean, index=False)
alldf_annualpeak.to_csv(outfile_annualpeak, index=False)
alldf_annuallow.to_csv(outfile_annuallow, index=False)
alldf_annualmonthpeak.to_csv(outfile_annualmonthpeak, index=False)
alldf_annualmonthlow.to_csv(outfile_annualmonthlow, index=False)