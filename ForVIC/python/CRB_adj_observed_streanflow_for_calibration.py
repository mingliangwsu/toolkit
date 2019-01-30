#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jan. 28, 2019

Adjust observed streamflow for model calibration (based on drainage area)
@author: liuming


Use original vegetation parameter (for Forecast project) as natural vegetation
"""

import pandas as pd
import sys 
import os

def sortkey(x): 
    return int(x)

#input lists:
#monthly LAI
#always ture!!!

selected_gauge_info = "/mnt/hydronas/Projects/BPA_CRB/GIS/final_selected_gauges_for_calibration_info.csv"
out_dir = "/home/liuming/temp/adjusted_streamflow_for_calibration"
log_file = out_dir + "/log.txt"
flog = open(log_file,"w")

gauges_path = {
        "CBCCSP" : "/mnt/hydronas/Projects/BPA_CRB/GIS/CBCCSP_natualizedflow_fromKirti/CCSP_naturliazed_monthly_flow",
        "Kirti"  : "/mnt/hydronas/Projects/BPA_CRB/GIS/UMATI",
        "NRNI"   : "/mnt/hydronas/Projects/BPA_CRB/GIS/NRNI/NRNI_monthly_flow",
        "USGS_GAGES" : "/mnt/hydronas/Projects/BPA_CRB/GIS/GAGES-II_subset/GAGESII_monthly_flow"
        }

with open(selected_gauge_info) as f:
    for line in f:
        a = line.split(",")
        if len(a) > 0:
            if "data_source" not in a:
                data_path = gauges_path[a[0]]
                file_name = data_path + "/" + a[1] + ".obs.month"
                outfile = out_dir + "/" + a[2] + ".obs.month"
                adj = float(a[5])
                if os.path.isfile(file_name):
                    outf = open(outfile,"w")
                    with open(file_name) as fdata:
                        for dataline in fdata:
                            data = dataline.split()
                            if len(data) > 0:
                                outline = data[0] + " " + data[1] + " " + str('%.1f' % (float(data[2]) * adj)) + "\n"
                                outf.write(outline)
                    outf.close()
                    print(a[1] + " done!")
                else:
                    print("cannot open file:" + file_name)
                    flog.write("cannot open file:" + file_name + "\n")
flog.close()
print("reading done!")
