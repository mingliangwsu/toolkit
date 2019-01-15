#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26, 2018 LIU 
Convert crop fractions into VIC veg parametger files for running VIC-CropSyst V2 (Forecast project)
@author: liuming
"""

import pandas as pd
import sys 
import os

os.chdir("/mnt/hydronas/Projects/BPA_CRB/GIS/CCSP_natualizedflow_fromKirti");

station_list_file = "station_list_NatBC"
start_year_file = "startwy_list_NatBC"
end_year_file = "endwy_list_NatBC"

out_data_dir = "/home/liuming/temp/CCSP_naturliazed_monthly_flow"

stationlist = list()
startlist = list()
endlist = list()

with open(station_list_file) as f:
    for line in f:
        a = line.split()
        stationlist.append(a[0])
with open(start_year_file) as f:
    for line in f:
        a = line.split()
        startlist.append(a[0])
with open(end_year_file) as f:
    for line in f:
        a = line.split()
        endlist.append(a[0])
print("Read Done!")


stationindex = 0
for station in stationlist:
    filename = "./training_data_all/" + station + ".month.obs"
    outfile = out_data_dir + "/" + station + ".obs.month"
    year_start = int(startlist[stationindex]) - 1
    start_month = 10
    outfile = open(outfile,"w")
    with open(filename) as f:
        for line in f:
            if (len(line) >= 1):
                outline = str(year_start) + " " + str(start_month) + " " + line
                outfile.write(outline)
                start_month += 1
                if (start_month == 13):
                    start_month = 1
                    year_start += 1
    outfile.close()
    stationindex += 1


outfileinfo = out_data_dir + "/stations_start_end_calendar_year.txt"
foutfile = open(outfileinfo,"w")
stationindex = 0
for station in stationlist:
    year_start = int(startlist[stationindex]) - 1
    end_start = int(endlist[stationindex])
    outline = station + " " + str(year_start) + " " + str(end_start)
    foutfile.write(outline + "\n")
    stationindex += 1
foutfile.close()