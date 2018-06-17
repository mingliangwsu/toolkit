#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu June 13, LIU
Convert VIC veg parametgers into tables with grid cell id and veg type as index
@author: liuming
"""

import pandas as pd
import sys 
import os

outdir = "/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Database/Veg/Kirti_cropmix_irrigation"
fraction_file = "CropMixLiu.txt"
out_file = "Umatila_veg_parameter.txt"


os.chdir(outdir)

fraction_list = ["cdl_1_corn", "cdl_12_sweetcorn", "cdl_14_mint", "cdl_21_barley", "cdl_23_spwheat", "cdl_24_winwheat", "cdl_31_canola", 
                 "cdl_36_alfalfa", "cdl_38_camlina", "cdl_42_drybeans", "cdl_43_potato", "cdl_49_onion", "cdl_53_peas", "cdl_66_cherries", 
                 "cdl_68_apples", "cdl_206_carrots", "cdl_37_otherhay", "cdl_59_seedsodgrass","genericcropfraction", 
                 "cdl_141", "cdl_142", "cdl_143", "cdl_152", "cdl_176", "cdl_190", "cdl_195"]

cdl_to_vic_dic = {"cdl_1_corn"          : "4007", 
                  "cdl_12_sweetcorn"    : "4008", 
                  "cdl_14_mint"         : "807", 
                  "cdl_21_barley"       : "4011", 
                  "cdl_23_spwheat"      : "4006", 
                  "cdl_24_winwheat"     : "4005", 
                  "cdl_31_canola"       : "4101", 
                  "cdl_36_alfalfa"      : "701", 
                  "cdl_38_camlina"      : "4103", 
                  "cdl_42_drybeans"     : "4010", 
                  "cdl_43_potato"       : "4004", 
                  "cdl_49_onion"        : "4100", 
                  "cdl_53_peas"         : "4009", 
                  "cdl_66_cherries"     : "1403", 
                  "cdl_68_apples"       : "1401", 
                  "cdl_206_carrots"     : "4102", 
                  "cdl_37_otherhay"     : "2501", 
                  "cdl_59_seedsodgrass" : "4104",
                  "genericcropfraction" : "6001", 
                  "cdl_141"             : "4", 
                  "cdl_142"             : "1", 
                  "cdl_143"             : "5", 
                  "cdl_152"             : "10", 
                  "cdl_176"             : "2501", 
                  "cdl_190"             : "10", 
                  "cdl_195"             : "10"}


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
                "13" : "0.1 0.1 0.75 0.6 0.5 0.3"}
default_parameter = "0.1 0.1 0.75 0.6 0.5 0.3"


out_veg_list = ["1", "4", "5", "10", "701", "807", "1401", "1403", "2501", "4004", "4005", "4006", "4007", "4008", "4009", "4010", "4011", "4100", "4101", "4102", "4103", "4104", "6001"]

    
outfile = open(out_file,"w")
with open(fraction_file) as f:
    for line in f:
        if "gridid" not in line:
            tot_fractions = []
            for veg in out_veg_list:
                tot_fractions.append(0)
            a = line.split()
            for col in range(0,len(a)):
                if col >= 1 and len(a) > 0:
                    tar_col_cdl = fraction_list[col-1]
                    tar_vic = cdl_to_vic_dic[tar_col_cdl]
                    array_index = out_veg_list.index(tar_vic)
                    tot_fractions[array_index] += float(a[col])
                    print(tar_col_cdl + " " + tar_vic + " " + str(array_index))
            total_area = 0
            total_veg_num = 0
            for ov in range(0,len(out_veg_list)):
                total_area += tot_fractions[ov]
                if (tot_fractions[ov] > 0.0001):
                    total_veg_num += 1
            line = str(a[0]) + " " + str(total_veg_num) + "\n"
            outfile.write(line)
            for ov in range(0,len(out_veg_list)):
                if (tot_fractions[ov] > 0.0001):
                    if out_veg_list[ov] in paramter_dic:
                        outp = paramter_dic[out_veg_list[ov]]
                    else:
                        outp = default_parameter
                    line = "   " + out_veg_list[ov] + " " + str('%.4f' % tot_fractions[ov]) + " " + outp + "\n"
                    outfile.write(line)
outfile.close()
        
            
            
print("reading done!")
