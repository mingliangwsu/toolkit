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

clm_years = ['daymet_2001','daymet_2021']
for clm_year in clm_years:
    indir = f"/home/liuming/mnt/hydronas3/Projects/WWS_Oregon/GateCreek_RHESSys_output/Output_realrun/{clm_year}/"
    prefix = "real_run_daymet"
    output = "grow_hillslope.daily"
    annual_mean_outfile = f'{indir}Annual_max_{clm_year}_from_{prefix}_{output}.txt'
    #Out[11]: Index(['day month year basinID lai gpsn plant_resp soil_resp nitrate sminn surfaceN plantc plantn cpool npool litrc litrn soilc soiln gwNO3 gwNH4 gwDON gwDOC streamflow_NO3 streamflow_NH4 streamflow_DON streamflow_DOC gwNO3out gwNH4out gwDONout gwDOCout denitrif nitrif DOC DON root_depth nfix nuptake grazingC StreamNO3_from_surface StreamNO3_from_sub litr_decomp decom_landclim_daily'], dtype='object')
    
    modelout_file = indir + prefix + '_' + output
    all_statistics = pd.read_csv(modelout_file,sep=' ')
    
    all_statistics_2021 = all_statistics[all_statistics['year'] == 2021]
    outdata_annual = all_statistics_2021.groupby(['basinID'],as_index=False).max()
    
    outdata_annual.to_csv(annual_mean_outfile, index=False)

print("Done!")