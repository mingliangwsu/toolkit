#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu June 13, LIU
Convert VIC irrigation parametgers into tables with grid cell id and veg type as index
@author: liuming
"""

import pandas as pd
import sys 
import os

outdir = "/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Database/Veg/Kirti_cropmix_irrigation"
fraction_file = "Irrig_Liu.txt"
out_file = "Umatila_irrigation_parameter.txt"


os.chdir(outdir)

fraction_list = ["cdl_1_corn", "cdl_12_sweetcorn", "cdl_14_mint", "cdl_21_barley", "cdl_23_spwheat", "cdl_24_winwheat", "cdl_31_canola", 
                 "cdl_36_alfalfa", "cdl_38_camlina", "cdl_42_drybeans", "cdl_43_potato", "cdl_49_onion", "cdl_53_peas", "cdl_66_cherries", 
                 "cdl_68_apples", "cdl_206_carrots", "cdl_37_otherhay", "cdl_59_seedsodgrass"]


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
                  "cdl_59_seedsodgrass" : "4104"}

out_veg_list = ["701", "807", "1401", "1403", "2501", "4004", "4005", "4006", "4007", "4008", "4009", "4010", "4011", "4100", "4101", "4102", "4103", "4104", "6001"]

irri_type = {"701"  : "CENTER_PIVOT", 
             "807"  : "CENTER_PIVOT", 
             "1401" : "DEFAULT_SOLID_SET",
             "1403" : "DEFAULT_SOLID_SET",
             "2501" : "CENTER_PIVOT", 
             "4004" : "CENTER_PIVOT", 
             "4005" : "CENTER_PIVOT", 
             "4006" : "CENTER_PIVOT", 
             "4007" : "CENTER_PIVOT", 
             "4008" : "CENTER_PIVOT", 
             "4009" : "CENTER_PIVOT", 
             "4010" : "CENTER_PIVOT", 
             "4011" : "WHEEL_LINE", 
             "4100" : "CENTER_PIVOT", 
             "4101" : "CENTER_PIVOT", 
             "4102" : "CENTER_PIVOT", 
             "4103" : "CENTER_PIVOT", 
             "4104" : "CENTER_PIVOT", 
             "6001" :  "CENTER_PIVOT"}

default_parameter = "CENTER_PIVOT"

outfile = open(out_file,"w")

with open(fraction_file) as f:
    for line in f:
        if "gridid" not in line:
            tot_fractions = []
            for veg in out_veg_list:
                tot_fractions.append("0")
            a = line.split()
            total_veg_num = 0
            for ov in range(0,len(fraction_list)):
                vicveg = cdl_to_vic_dic[fraction_list[ov]]
                vicveg_index = out_veg_list.index(vicveg)
                tot_fractions[vicveg_index] = a[ov+1]
                if tot_fractions[vicveg_index] == "1":
                    total_veg_num += 1
            if total_veg_num > 0:
                line = str(a[0]) + " " + str(total_veg_num) + "\n"
                outfile.write(line)
            for ov in range(0,len(out_veg_list)):
                if tot_fractions[ov] == "1":
                    if out_veg_list[ov] in irri_type:
                        outp = irri_type[out_veg_list[ov]]
                    else:
                        outp = default_parameter
                    line = "   " + out_veg_list[ov] + " " + outp + "\n"
                    outfile.write(line)
outfile.close()
print("reading done!")
