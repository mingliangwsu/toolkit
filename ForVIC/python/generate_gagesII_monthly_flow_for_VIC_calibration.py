#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sum VIC-CropSyst crop daily outputs to annuam mean.

@author: liuming
"""
from datetime import date
import calendar
import pandas as pd
import os
import os.path

stationinfo = "/mnt/hydronas/Projects/BPA_CRB/GIS/GAGES-II_subset/selected33station_liu.txt"
out_data_dir = "/home/liuming/temp/GAGESII_monthly_flow"
if not os.path.exists(out_data_dir):
    os.mkdir(out_data_dir)

month_days = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31}
#station_info = out_data_dir + "/station_start_end_month.txt"
#station_info_out = open(station_info,'w')
drainage_area = out_data_dir + "/" + "drainage_area.txt"
areafout = open(drainage_area,'w')


station_drain = {}
stations = pd.read_csv(stationinfo,sep=',',index_col=False,header=0)
for index, row in stations.iterrows():
    #print(temp.month)
    station_drain[row['STAID']] = row['DRAIN_SQKM']
    outline = str(row['STAID']) + " " + str("%0.2f" % (row['DRAIN_SQKM'],)) + "\n"
    areafout.write(outline)
areafout.close()

flowdata = "/mnt/hydronas/Projects/BPA_CRB/GIS/GAGES-II_subset/usgs_gauge_data_GII.txt"
monthly_flow = pd.read_csv(flowdata,sep=',',index_col=False,header=0)

for key in station_drain:
    print(key)
    outfile = out_data_dir + "/" + str(key) + ".obs.month"
    fout = open(outfile,'w')
    for i, row in monthly_flow.iterrows():
        mondays = month_days[row['MONTH']]
        if calendar.isleap(row['YEAR']) and row['MONTH'] == 2:
            monthdays = 29
            #print(str(row['YEAR']) + " is leapyear\n")
        if row['GAUGE'] == key:
            flow_cfs = row['RO_MM'] * 0.001 * station_drain[key] * 1000000.0 * 35.3147 / (24.0 * 3600.0 * monthdays)
            outline = str("%0.0f" % (row['YEAR'],)) + " " + str("%0.0f" % (row['MONTH'],)) + " " + str("%0.1f" % (flow_cfs,)) + "\n"
            fout.write(outline)
    fout.close()

print("Done!")