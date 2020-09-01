import pandas as pd
import pysal as ps
import numpy as np
import os
import datetime
import statistics

#datapath = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/Calibration/VIC_vs_gauges_observation/gauge_observation_allsimulations_evaluation_20200717"
datapath = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/Calibration/VIC_vs_gauges_observation/gauge_observation_allsimulations_evaluation"
basin_area_file = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/Calibration/BasinBNDWA/basin_area_km2.txt"
#simulations = 20
simulations = 40


#target_variables = ["annual_peak","annual_min_7day","monthly_mean","daily_mean"]

#Can do each target temporal scale

evaluation_filename = datapath + "/" + "all_performance_daily_mean.csv"
obs_vs_sim_file_prefix = "daily_obs_vs_vic_g"                                         #12135000.csv

outfile = datapath + "/" + "for_mapping_statistics_with_ensemble_mean.csv"
fout = open(outfile,"w")

temp = pd.read_csv(evaluation_filename,sep=',',header=0,low_memory=False)


#test
#obsvssim_file = datapath + "/" + obs_vs_sim_file_prefix + "12135000" + ".csv"
#df = pd.read_csv(obsvssim_file,sep=',',header=0,low_memory=False)
#dfsub = df[df['obs_cfs'].notnull()]
#dfmean = dfsub.mean(axis = 0) 


#mean and diviation of observations and simulation
target = ["median","max","min","simmean"]
evaluation_metrics = ["relative_bias","std","nse","kge","nselog","nse","r"] 
#sim_mean = dict() #[gauge][sim] average for observation not NA
obs_mean = dict() #[gauge]
obs_std = dict() #[gauge]
all_data = dict() #[gauge][target][evaluation_metrics]

basinarea = dict()
with open(basin_area_file,"r") as f:
    for line in f:
        a = line.rstrip().split(",")
        if "basin" not in a:
            if a[0] not in basinarea:
                basinarea[a[0]] = a[1]


#out head
fout.write("gauge,area_km2,obs_cfs,obs_cfs_std")
for t in target:
    for e in evaluation_metrics:
        fout.write("," + t + "_" + e)
fout.write("\n")


for index, row in temp.iterrows():
    gauge = str(int(row["gauge"]))
    print(gauge)
    if gauge not in all_data:
        all_data[gauge] = dict()
    for t in target:
        if t not in all_data[gauge]:
            all_data[gauge][t] = dict()
        for e in evaluation_metrics:
            if e not in all_data[gauge][t]:
                all_data[gauge][t][e] = None
                
    if gauge not in obs_mean:
        obs_mean[gauge] = None
    
    #get the average value
    obsvssim_file = datapath + "/" + obs_vs_sim_file_prefix + str(int(gauge)) + ".csv"
    df = pd.read_csv(obsvssim_file,sep=',',header=0,low_memory=False)
    dfsub = df[df['obs_cfs'].notnull()]
    dfmean = dfsub.mean(axis = 0)
    dfstd = dfsub.std(axis = 0)
    obs_mean[gauge] = dfmean['obs_cfs']
    obs_std[gauge] = dfstd['obs_cfs']
    #simmean = 0.0
    rbias = list()
    
    meanallsims = 0.0
    for sim in range(simulations):
        nindex = "vic_cfs_s" + str(sim)
        relative_bias_percent = (dfmean[nindex] - obs_mean[gauge]) * 100.0 / obs_mean[gauge]
        rbias.append(relative_bias_percent)
        meanallsims += dfmean[nindex]
        #simmean += dfmean[nindex]
    #simmean /= 20.0
    all_data[gauge]["median"]["relative_bias"] = statistics.median(rbias)
    all_data[gauge]["max"]["relative_bias"] = max(rbias)
    all_data[gauge]["min"]["relative_bias"] = min(rbias)
    
    #mean of ensemble simulations
    meanallsims /= simulations
    relative_bias_percent = (meanallsims - obs_mean[gauge]) * 100.0 / obs_mean[gauge]
    all_data[gauge]["simmean"]["relative_bias"] = relative_bias_percent
    
    for e in evaluation_metrics:
        if e != "relative_bias":
            elist = list()
            for sim in range(simulations):
                nindex = e + "_" + str(sim)
                elist.append(row[nindex])
            all_data[gauge]["median"][e] = statistics.median(elist)
            all_data[gauge]["max"][e] = max(elist)
            all_data[gauge]["min"][e] = min(elist)
            
            #mean of ensemble simulations
            nindex = e + "_" + str(simulations)
            all_data[gauge]["simmean"][e] = row[nindex]

for gauge in all_data:        
    fout.write(gauge + "," + basinarea[gauge] + "," + str(obs_mean[gauge]) + "," + str(obs_std[gauge]))  
    for t in target:
        for e in evaluation_metrics:
            fout.write("," + str(all_data[gauge][t][e]))
    fout.write("\n")    
#fout.write(str(gauge) + "," + )
fout.close()
    