#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Nov. 21, 2019, LIU
generate monthly LAI for each vegetation 
@author: liuming
"""

import pandas as pd
import sys 
import os
from os import path
#from simpledbf import Dbf5 
import geopandas as gpd

def sortkey(x): 
    return int(x)

lai_data_path = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/LAI"


out_path = "/home/liuming/temp/temp/"


modis_to_vic_dic = {
        "1" : "1",
        "2" : "2",
        "3" : "3",
        "4" : "4",
        "5" : "5",
        "6" : "8",
        "7" : "9",
        "8" : "6",
        "9" : "7",
        "10" : "10",
        "12" : "11",
        "16" : "14",
        "18" : "13"}
#months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
months = ["01"]


#reading mean lai over PNW region
outfile_name = "vic_type_mean_lai.txt"
vic_mon_lai_dic = dict()
for modis_type in modis_to_vic_dic:
    if modis_to_vic_dic[modis_type] not in vic_mon_lai_dic:
        vic_mon_lai_dic[modis_to_vic_dic[modis_type]] = dict()
        for month in months:
            vic_mon_lai_dic[modis_to_vic_dic[modis_type]][month] = 0.0

for month in months:
    dbffile = lai_data_path + "/" + "mean_modis_lai_" + month + ".dbf"
    tab = gpd.read_file(dbffile)
    df = pd.DataFrame(tab)
    for index, row in df.iterrows():
        #print(row['CRBMODISUP'], row['MEAN_W_ALB'] / 100.0)
        modis_type = str(row['CRBMODISUP'])
        if modis_type in modis_to_vic_dic:
            vic_type = modis_to_vic_dic[modis_type]
            vic_mon_lai_dic[vic_type][month] = row['MEAN_W_ALB'] / 100.0

#generate mean lai tabkle for each VIC class
if not path.exists(out_path + "/" + outfile_name):
    outf = open(out_path + "/" + outfile_name, "w")

    for vic_type in sorted(vic_mon_lai_dic, key=sortkey, reverse=False):
        outf.write(vic_type + "\n")
        for month in months:
            outf.write(str('%.5f' % vic_mon_lai_dic[vic_type][month]) + " ")
        outf.write("\n")
    outf.close()

#calculating monthly lai for each vic grid cell
outfile_name = "vic_type_lai.txt"
cell_vic_mon_lai_sum_dic = dict()  #[vic_id][vic_class][month]  count * lai
cell_vic_mon_count_dic = dict()    #[vic_id][vic_class][month]  counts for each lai value
for month in months:
    print("Reading month " + month + "...\n")
    dbffile = lai_data_path + "/" + "viclai" + month + ".dbf"
    table = gpd.read_file(dbffile)
    pdtable = pd.DataFrame(table)
    for index, row in pdtable.iterrows():
        vicid = str(row['VICID500'])
        modistype = str(row['CRBMODISUP'])
        lai = row['ALBM01100']
        count = row['COUNT']
        if vicid not in cell_vic_mon_lai_sum_dic:
            cell_vic_mon_lai_sum_dic[vicid] = dict()
        if vicid not in cell_vic_mon_count_dic:
            cell_vic_mon_count_dic[vicid] = dict()
        if modistype in modis_to_vic_dic:
            victype = modis_to_vic_dic[modistype]
            if victype not in cell_vic_mon_lai_sum_dic[vicid]:
                cell_vic_mon_lai_sum_dic[vicid][victype] = dict()
            if victype not in cell_vic_mon_count_dic[vicid]:
                cell_vic_mon_count_dic[vicid][victype] = dict()
                
            if month not in cell_vic_mon_lai_sum_dic[vicid][victype]:
                cell_vic_mon_lai_sum_dic[vicid][victype][month] = 0.0
            cell_vic_mon_lai_sum_dic[vicid][victype][month] += count * lai
            if month not in cell_vic_mon_count_dic[vicid][victype]:
                cell_vic_mon_count_dic[vicid][victype][month] = 0.0
            cell_vic_mon_count_dic[vicid][victype][month] += float(count)
    print("Calculating mean lai for each grid cell and vic vegetation type...\n")
    for cell in cell_vic_mon_lai_sum_dic:
        for veg in cell_vic_mon_lai_sum_dic[cell]:
            if month not in cell_vic_mon_count_dic[cell][veg]:
                print("Error!\n")
                exit()
            else:
                cell_vic_mon_lai_sum_dic[cell][veg][month] /= cell_vic_mon_count_dic[cell][veg][month] * 100.0
                
                
print("Done!\n")

