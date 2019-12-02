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
#fraction_file = "/home/liuming/temp/temp/landcover_fraction_nlcd_modis.txt"
fraction_file = "/home/liuming/temp/temp/landcover_fraction_canada_nlcd_modis.txt"

out_path = "/home/liuming/temp/temp/"
outfile_name = "vic_type_mean_lai.txt"
#out_veg_parameter_name = "vic_vegetation_parameter_us.txt"
out_veg_parameter_name = "vic_vegetation_parameter_ca.txt"


tol = 0.000001  
paramter_dic = {"1"  : "0.1 0.05 1 0.45 5 0.5",
                "2"  : "0.1 0.05 1 0.45 5 0.5",
                "3"  : "0.1 0.05 1 0.45 5 0.5",
                "4"  : "0.1 0.05 1 0.45 5 0.5",
                "5"  : "0.1 0.05 1 0.45 5 0.5",
                "6"  : "0.1 0.1 1 0.65 1 0.25",
                "7"  : "0.1 0.1 1 0.65 1 0.25",
                "8"  : "0.1 0.1 1 0.65 0.5 0.25",
                "9"  : "0.1 0.1 1 0.65 0.5 0.25",
                "10" : "0.1 0.1 1 0.7 0.5 0.2",
                "11" : "0.1 0.1 0.75 0.6 0.5 0.3",
                "12" : "0.1 0.1 0.75 0.6 0.5 0.3",
                "13" : "0.1 0.1 0.75 0.6 0.5 0.3",
                "14" : "0.1 0.1 1 0.7 0.5 0.2"}
default_veg_parameter = "0.1 0.1 0.75 0.6 0.5 0.3"


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
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
#months = ["01"]


#reading mean lai over PNW region

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
        laicol = 'ALBM' + month + '100'
        #lai = row['ALBM01100']
        lai = row[laicol]
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

#read fraction file and write to vegetation parameter file:
print("Reading fractions and writing to veg parameter file...")
veg_fraction = dict()  #[cell][veg]
veg_index = {"1"  : 1,
             "2"  : 2,
             "3"  : 3,
             "4"  : 4,
             "5"  : 5,
             "6"  : 6,
             "7"  : 7,
             "8"  : 8,
             "9"  : 9,
             "10" : 10,
             "11" : 11,
             "12" : 12,
             "13" : 13,
             "14" : 14}
outfile_veg = open(out_path + "/" + out_veg_parameter_name, "w")
with open(fraction_file) as f:
    for line in f:
        if "vic" in line:
            cols = line.split(",")
        else:
            #produce veg parameter file
            tot_fractions = 0
            total_veg_num = 0
            a = line.split(",")
            if (len(a) > 0):
                cell = a[0]
                for vegtype in veg_index:
                    fraction = float(a[veg_index[vegtype]])
                    if (fraction >= tol):
                        total_veg_num += 1
                        tot_fractions += fraction
                line = str(a[0]) + " " + str(total_veg_num) + "\n"
                outfile_veg.write(line)
                if (total_veg_num >= 1):
                    for vegtype in veg_index:
                        fraction = float(a[veg_index[vegtype]])
                        if fraction >= tol:
                            if vegtype in paramter_dic:
                                vegp = paramter_dic[vegtype]
                            else:
                                vegp = default_veg_parameter
                            line = "   " + vegtype + " " + str('%.6f' % fraction) + " " + vegp + "\n"
                            outfile_veg.write(line)
                            outfile_veg.write("      ")
                            for month in months:
                                if vegtype == '12':
                                    lai = 0.0
                                else:
                                    lai = vic_mon_lai_dic[vegtype][month]
                                if cell in cell_vic_mon_lai_sum_dic:
                                    if (vegtype in cell_vic_mon_lai_sum_dic[cell]) and (vegtype != '12'):
                                        lai = cell_vic_mon_lai_sum_dic[cell][vegtype][month]
                                outfile_veg.write(str('%.3f' % lai) + " ")
                            outfile_veg.write("\n")
outfile_veg.close()
                
print("Done!\n")

