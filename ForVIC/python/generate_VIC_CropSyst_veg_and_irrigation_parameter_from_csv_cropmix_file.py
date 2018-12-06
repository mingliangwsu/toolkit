#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu July 12, LIU
Convert crop fractions into VIC veg and irrigation parametger files
@author: liuming
"""

import pandas as pd
import sys 
import os

outdir = "/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Database/Veg/Kirti_cropmix_irrigation"
#fraction_file = "CropMixLiu.txt"
fraction_file = "LiuCropMix_include_irrigation_fraction.txt"
out_veg_file = "Umatila_veg_parameter_180814.txt"
out_irrig_file = "Umatila_irrigation_parameter_180814.txt"


os.chdir(outdir)

"""
fraction_list = ["cdl_1_corn", "cdl_12_sweetcorn", "cdl_14_mint", "cdl_21_barley", "cdl_23_spwheat", "cdl_24_winwheat", "cdl_31_canola", 
                 "cdl_36_alfalfa", "cdl_38_camlina", "cdl_42_drybeans", "cdl_43_potato", "cdl_49_onion", "cdl_53_peas", "cdl_66_cherries", 
                 "cdl_68_apples", "cdl_206_carrots", "cdl_37_otherhay", "cdl_59_seedsodgrass","genericcropfraction", 
                 "cdl_141", "cdl_142", "cdl_143", "cdl_152", "cdl_176", "cdl_190", "cdl_195"]
"""
"""
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
"""

fraction_list = ["cdl_141", "cdl_142", "cdl_143", "cdl_152", "cdl_176", "cdl_190", "cdl_195", 
                 "cdl_1_corn", "cdl_12_sweetcorn", "cdl_14_mint", "cdl_36_alfalfa", "cdl_43_potato", "cdl_49_onion", "cdl_53_peas", 
                 "cdl_66_cherries", "cdl_68_apples", "cdl_206_carrots", "cdl_59_seedsodgrass", 
                 "cdl_21_barley-irrig", "cdl_21_barley_dryland", "cdl_23_swheat-irrig", "cdl_23_swheat-dryland", 
                 "cdl_24_wwheat-irrig", "cdl_24_wwheat-dryland", "cdl_31_canola-irrig", "cdl_31_canola-dryland", 
                 "cdl_38_camelina-irrig", "cdl_38_camelina_dryland", "cdl_42_drybean-irrig", "cdl_42_drybean-dryland", 
                 "cdl_37_otherhay-irrig", "cdl_37_otherhay-dryland", "_generic-irrig", "_generic-dryland"]

#if there is fractional irrigated crops in grid cell. the irrigated crop is coded as the original crops 
# and the non-irrigated crops are coded as the origincal code + 10,000
# LML: there is an asumption that all crops without "dryland" in the name are irigated, i.e. there is no irrigation (1 or 0) file as input to generate irrigation map

cdl_to_vic_dic = {"cdl_141"             : "4", 
                  "cdl_142"             : "1", 
                  "cdl_143"             : "5", 
                  "cdl_152"             : "10", 
                  "cdl_176"             : "10", 
                  "cdl_190"             : "10", 
                  "cdl_195"             : "10", 
                  "cdl_1_corn"          : "4007", 
                  "cdl_12_sweetcorn"    : "4008", 
                  "cdl_14_mint"         : "807", 
                  "cdl_36_alfalfa"      : "701", 
                  "cdl_43_potato"       : "4004", 
                  "cdl_49_onion"        : "4100", 
                  "cdl_53_peas"         : "4009", 
                  "cdl_66_cherries"     : "1403", 
                  "cdl_68_apples"       : "1401", 
                  "cdl_206_carrots"     : "4102", 
                  "cdl_59_seedsodgrass" : "4104",
                  "cdl_21_barley-irrig"     :  "4011",
                  "cdl_21_barley_dryland"   : "14011",
                  "cdl_23_swheat-irrig"     :  "4006",
                  "cdl_23_swheat-dryland"   : "14006",
                  "cdl_24_wwheat-irrig"     :  "4005",
                  "cdl_24_wwheat-dryland"   : "14005",
                  "cdl_31_canola-irrig"     :  "4101",
                  "cdl_31_canola-dryland"   : "14101",
                  "cdl_38_camelina-irrig"   :  "4103",
                  "cdl_38_camelina_dryland" : "14103",
                  "cdl_42_drybean-irrig"    :  "4010",
                  "cdl_42_drybean-dryland"  : "14010",
                  "cdl_37_otherhay-irrig"   :  "2501",
                  "cdl_37_otherhay-dryland" : "12501",
                  "_generic-irrig"          :  "6001",
                  "_generic-dryland"        : "16001"}

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
default_veg_parameter = "0.1 0.1 0.75 0.6 0.5 0.3"

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
             "4011" : "CENTER_PIVOT", 
             "4100" : "CENTER_PIVOT", 
             "4101" : "CENTER_PIVOT", 
             "4102" : "CENTER_PIVOT", 
             "4103" : "CENTER_PIVOT", 
             "4104" : "CENTER_PIVOT", 
             "6001" : "CENTER_PIVOT"}
default_irrig_parameter = "CENTER_PIVOT"


#out_veg_list = ["1", "4", "5", "10", "701", "807", "1401", "1403", "2501", "4004", "4005", "4006", "4007", "4008", "4009", "4010", "4011", "4100", "4101", "4102", "4103", "4104", "6001"]

out_veg_list = ["1", "4", "5", "10", "701", "807", "1401", "1403", "2501", "4004", 
                "4005", "4006", "4007", "4008", "4009", "4010", "4011", "4100", 
                "4101", "4102", "4103", "4104", "6001",
                "12501", "14005", "14006", "14010", "14011", "14101", "14103", "16001"]


    
outfile_veg = open(out_veg_file,"w")
outfile_irrig = open(out_irrig_file,"w")

with open(fraction_file) as f:
    for line in f:
        if "gridid" not in line:
            
            #produce veg parameter file
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
            outfile_veg.write(line)
            for ov in range(0,len(out_veg_list)):
                if (tot_fractions[ov] > 0.0001):
                    if out_veg_list[ov] in paramter_dic:
                        outp = paramter_dic[out_veg_list[ov]]
                    else:
                        outp = default_veg_parameter
                    line = "   " + out_veg_list[ov] + " " + str('%.4f' % tot_fractions[ov]) + " " + outp + "\n"
                    outfile_veg.write(line)
                    
            #produce irrigation parameter file
            #tot_fractions = []
            #for veg in out_veg_list:
            #    tot_fractions.append("0")
            #a = line.split()
            total_veg_num = 0
            #for ov in range(0,len(fraction_list)):
            #    vicveg = cdl_to_vic_dic[fraction_list[ov]]
            #    vicveg_index = out_veg_list.index(vicveg)
            #    tot_fractions[vicveg_index] = a[ov+1]
            #    if tot_fractions[vicveg_index] == "1":
            #        total_veg_num += 1
            for ov in range(0,len(out_veg_list)):
                if (tot_fractions[ov] > 0.0001):
                    if out_veg_list[ov] in irri_type:
                        total_veg_num += 1
            
            if total_veg_num > 0:
                line = str(a[0]) + " " + str(total_veg_num) + "\n"
                outfile_irrig.write(line)
            for ov in range(0,len(out_veg_list)):
                if tot_fractions[ov] > 0.0001:
                    if out_veg_list[ov] in irri_type:
                        outp = irri_type[out_veg_list[ov]]
                        line = "   " + out_veg_list[ov] + " " + outp + "\n"
                        outfile_irrig.write(line)
                    
outfile_veg.close()
outfile_irrig.close()
        
            
            
print("reading done!")
