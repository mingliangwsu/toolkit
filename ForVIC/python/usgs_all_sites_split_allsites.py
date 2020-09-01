#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 09:48:18 2020

@author: liuming
"""

import pandas as pd
import pysal as ps
import numpy as np
from datetime import datetime

def sortkey(x): 
    return int(x)

#ref_sites_file = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/Calibration/refsites_55.txt"
#ref_data = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/Calibration/dv/dv.txt" #USGS	 12010000	1981-05-12	230	A	230	A
#outdata_path = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/Calibration/dv/Allsites/"
#out_site_info = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/Calibration/allsites_withdata_info.txt"

ref_data = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/Calibration/dv_1902_2020/dv.txt" #USGS	 12010000	1981-05-12	230	A	230	A
#ref_data = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/Calibration/dv_1902_2020/dv_test.txt" #USGS	 12010000	1981-05-12	230	A	230	A
outdata_path = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/Calibration/dv_1902_2020/Allsites/"
out_site_info = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/Calibration/allsites_withdata_info_1902_2020new.txt"



#ref_sites = list()
data_sites_dates = dict()
foutdic = dict()


#with open(ref_sites_file) as f:
#    for line in f:
#        a = line.rstrip().split(",")
#        if 'FID' not in a and len(a) > 0:
#            if a[1] not in ref_sites:
#                ref_sites.append(a[1])
last_site = "NONE"
with open(ref_data) as f:
    for line in f:
        a = line.rstrip().split('\t')
        if ('agency_cd' not in a) and ('#' not in a) and ('5s' not in a) and len(a) > 1:
            #if a[1] in ref_sites:
                if a[1] not in data_sites_dates:
                    data_sites_dates[a[1]] = list()
                this_date = datetime.strptime(a[2], '%Y-%M-%d')
                if len(data_sites_dates[a[1]]) == 0:
                    data_sites_dates[a[1]].append(this_date);
                if len(data_sites_dates[a[1]]) == 1:
                    data_sites_dates[a[1]].append(this_date)
                if this_date > data_sites_dates[a[1]][1] and len(a) > 3:
                    data_sites_dates[a[1]][1] = this_date
                if a[1] not in foutdic:
                    if last_site in foutdic:
                        foutdic[last_site].close()
                    outdata = outdata_path + a[1] + ".csv"
                    foutdic[a[1]] = open(outdata,"w")
                    foutdic[a[1]].write("date,streamflow_ft3_per_sec\n")
                    last_site = a[1]
                if len(a) > 3:
                    #print("a[3] " + a[3])
                    #if a[3].replace('.','',1).isdigit():
                    #if len(a[3]) > 0 and a[3].isnumeric():
                        #print("a[3].isnumeric()")
                    if len(a[3]) > 0 and a[3].replace('.','',1).isdigit():
                        foutdic[a[1]].write(this_date.strftime("%Y-%M-%d") + "," + a[3] + "\n")
                    elif len(a) > 6:
                            if a[5].replace('.','',1).isdigit():
                                foutdic[a[1]].write(this_date.strftime("%Y-%M-%d") + "," + a[5] + "\n")
                            else:
                                foutdic[a[1]].write(this_date.strftime("%Y-%M-%d") + "," + "-9999" + "\n")
                    else:
                        foutdic[a[1]].write(this_date.strftime("%Y-%M-%d") + "," + "-9999" + "\n")
                else:
                    foutdic[a[1]].write(this_date.strftime("%Y-%M-%d") + "," +"-9999" + "\n")
if last_site in foutdic:
    foutdic[last_site].close()
fout = open(out_site_info,"w")
fout.write("site,start_date,end_date\n")
for site in sorted(data_sites_dates, key=sortkey, reverse=False):
    start = data_sites_dates[site][0].strftime("%Y-%M-%d")
    end = data_sites_dates[site][1].strftime("%Y-%M-%d")
    fout.write(site + "," + start + "," + end + "\n")
fout.close()

for station in foutdic:
    foutdic[station].close()
print("Done!\n")
                    
                