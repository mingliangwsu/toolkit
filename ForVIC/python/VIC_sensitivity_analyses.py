#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 23:34:00 2020

@author: liuming
"""

import pandas as pd 
import numpy as np
#from SALib.analyze import sobol
from sklearn.preprocessing import StandardScaler

#VIC paramater sets
bi = [0.2903,0.3900,0.0509,0.1905,0.2304,0.0309,0.3501,0.0908,0.2504,0.1107,0.3701,0.3102,0.3302,0.1506,0.0708,0.1706,0.2703,0.0110,0.2105,0.1307]
DsMAX = [8.2573,24.7518,9.7568,12.7558,18.7538,29.2503,2.2593,14.2552,21.7528,17.2543,5.2583,26.2512,27.7508,6.7577,0.7598,15.7547,11.2562,20.2533,23.2523,3.7587]
Ds = [0.4751,0.5250,0.8250,0.2251,0.7750,0.9750,0.2751,0.9250,0.8750,0.3751,0.6750,0.5750,0.7250,0.0751,0.1751,0.4251,0.3251,0.1251,0.6250,0.0251]
Ws = [0.4803,0.7278,0.2328,0.3812,0.0348,0.3318,0.9258,0.5298,0.9753,0.4308,0.8268,0.6288,0.0843,0.6783,0.2823,0.5793,0.1833,0.7772,0.1338,0.8762]

#VIC results
#vic_daily_output = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/results/parameter_sensitivity/allmean.csv"
vic_daily_output = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/results/parameter_sensitivity/20200503_results"
outfile = vic_daily_output + "/exp_20_multiyear_average.csv"
outmerged_daily = vic_daily_output + "/exp_20_daily.csv"

# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
#data = pd.read_csv(vic_daily_output) 
data = pd.DataFrame(columns=['YEAR', 'MONTH', 'DAY'])


out_varname_list = list(data)

for experiment in range(0,20):
    fname = vic_daily_output + '/' + str(experiment) + '_mean.txt'
    
    tempdata = pd.read_csv(fname)
    mean_runoff = "s" + str(experiment) + "_TotalR_day"
    
    if experiment == 0:
        data['YEAR'] = tempdata['YEAR']
        data['MONTH'] = tempdata['MONTH']
        data['DAY'] = tempdata['DAY']
    data[mean_runoff] = tempdata['TOTR_AREA'] / tempdata['AREA']
    
out_varname_list = list(data)
data = data.sort_values(by=['YEAR', 'MONTH','DAY'])
#out_varname_list = np.array(list(data))

#add and calculate 7-day-mean flow
for experiment in range(0,20):
    mean_runoff = "s" + str(experiment) + "_TotalR_day"
    item_index = out_varname_list.index(mean_runoff)
    seven_day_avgflow = "s" + str(experiment) + "_7dayAvg"
    data[seven_day_avgflow] = data.iloc[:,item_index].rolling(window=7,center=True).mean()

  
#get annual mean, min, and max value
#ann_std = data.groupby('YEAR').std() 
ann_nstd = data.groupby('YEAR').apply(lambda x: np.std(x) / np.mean(x))   #normalized standard deviation
ann_nstd = ann_nstd.drop(columns=['YEAR'])
ann_mean = data.groupby('YEAR').mean() 
ann_min = data.groupby('YEAR').min()
ann_max = data.groupby('YEAR').max()   

final_out_varname_list = list(data)
final_out_varname_list.remove('YEAR')


#get multi-year average mean, min, and max value
multiyear = dict()
statistical_items = ['mean','min','max','nstd']
multiyear['mean'] = ann_mean.mean() 
multiyear['min'] = ann_min.mean() 
multiyear['max'] = ann_max.mean() 
multiyear['nstd'] = ann_nstd.mean()

    
#estimate sensitivity of each variable
df = pd.DataFrame(columns=['bi', 'DsMAX', 'Ds', 'Ws', \
                           'flow_mean', 'flow_min', 'flow_max', 'flow_nstd', \
                           'flow7d_mean', 'flow7d_min', 'flow7d_max', 'flow7d_nstd'])
df['bi'] = bi
df['DsMAX'] = DsMAX
df['Ds'] = Ds
df['Ws'] = Ws

#add VIC output statistics to df 
for sts in statistical_items:
    streams = list()
    streams_7day = list()
    streams_name = 'flow_' + sts
    streams_name_7day = 'flow7d_' + sts
    for experiment in range(0,20):
        avgflow = "s" + str(experiment) + "_TotalR_day"
        avgflow_7day = "s" + str(experiment) + "_7dayAvg"
        index_avgflow = final_out_varname_list.index(avgflow)
        index_7day = final_out_varname_list.index(avgflow_7day)
        
        #print('experiment ' + str(experiment) + " index:" + str(index_avgflow))
        
        streams.append(multiyear[sts][index_avgflow])
        streams_7day.append(multiyear[sts][index_7day])
    df[streams_name] = streams
    df[streams_name_7day] = streams_7day

#export
df.to_csv(outfile, index = False)    
data.to_csv(outmerged_daily, index = False)   


#
features = ['bi', 'DsMAX', 'Ds', 'Ws']
Y_list = ['flow_mean', 'flow_min', 'flow_max', 'flow_nstd', \
          'flow7d_mean', 'flow7d_min', 'flow7d_max', 'flow7d_nstd']]
from sklearn.datasets import load_iris
rnd_clf = RandomForestClassifier(n_estimators=500, n_jobs=-1, random_state=42)

for y in Y_list:
    # Separating out the target
    rnd_clf.fit(df[features], df[y])
    for name, importance in zip(df[features], rnd_clf.feature_importances_):
        print(name, "=", importance)

