#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu July 30, 2019
LIU

    
"""

#import pandas as pd
import sys 
import os

#path_dir = "/home/liuming/Projects/WSU_BPA/CRB_Datasets/LandUseAndIrrigation/Willamette"
path_dir = "/home/liuming/Projects/WSU_BPA/CRB_Datasets/LandUseAndIrrigation/UpperCRB/"
outdir = path_dir + "/outputs"
indir = path_dir + "/inputs"
#vic_veg_parameter_file = indir + "/CRB_vegetation_parameter_Forecast_natveg_2017Crops_calibration.txt"
fraction_file = indir + "/ca_vic_irrigated_crops.csv"
cell_list = indir + "/viclist.txt"

out_veg_file = "veg_parameter_ca.txt"
out_irrig_file = "irrigation_parameter_ca.txt"

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
"""
fraction_list = ["cdl_141", "cdl_142", "cdl_143", "cdl_152", "cdl_176", "cdl_190", "cdl_195", 
                 "cdl_1_corn", "cdl_12_sweetcorn", "cdl_14_mint", "cdl_36_alfalfa", "cdl_43_potato", "cdl_49_onion", "cdl_53_peas", 
                 "cdl_66_cherries", "cdl_68_apples", "cdl_206_carrots", "cdl_59_seedsodgrass", 
                 "cdl_21_barley-irrig", "cdl_21_barley_dryland", "cdl_23_swheat-irrig", "cdl_23_swheat-dryland", 
                 "cdl_24_wwheat-irrig", "cdl_24_wwheat-dryland", "cdl_31_canola-irrig", "cdl_31_canola-dryland", 
                 "cdl_38_camelina-irrig", "cdl_38_camelina_dryland", "cdl_42_drybean-irrig", "cdl_42_drybean-dryland", 
                 "cdl_37_otherhay-irrig", "cdl_37_otherhay-dryland", "_generic-irrig", "_generic-dryland"]
"""
"""
fraction_list = ["irr_fr_lu_1", "irr_fr_lu_12", "irr_fr_lu_13",
                 "irr_fr_lu_14", "irr_fr_lu_176", "irr_fr_lu_205", 
                 "irr_fr_lu_206", "irr_fr_lu_207", "irr_fr_lu_208", 
                 "irr_fr_lu_209", "irr_fr_lu_21", "irr_fr_lu_214", 
                 "irr_fr_lu_216", "irr_fr_lu_219", "irr_fr_lu_22", 
                 "irr_fr_lu_220", "irr_fr_lu_221", "irr_fr_lu_222", 
                 "irr_fr_lu_223", "irr_fr_lu_224", "irr_fr_lu_225", 
                 "irr_fr_lu_226", "irr_fr_lu_227", "irr_fr_lu_229", 
                 "irr_fr_lu_23", "irr_fr_lu_237", "irr_fr_lu_24", 
                 "irr_fr_lu_242", "irr_fr_lu_243", "irr_fr_lu_244", 
                 "irr_fr_lu_246", "irr_fr_lu_247", "irr_fr_lu_249", 
                 "irr_fr_lu_25", "irr_fr_lu_250", "irr_fr_lu_27", 
                 "irr_fr_lu_28", "irr_fr_lu_29", "irr_fr_lu_30", 
                 "irr_fr_lu_31", "irr_fr_lu_32", "irr_fr_lu_33", 
                 "irr_fr_lu_34", "irr_fr_lu_35", "irr_fr_lu_36", 
                 "irr_fr_lu_37", "irr_fr_lu_38", "irr_fr_lu_39", 
                 "irr_fr_lu_4", "irr_fr_lu_41", "irr_fr_lu_42", 
                 "irr_fr_lu_43", "irr_fr_lu_44", "irr_fr_lu_46", 
                 "irr_fr_lu_47", "irr_fr_lu_48", "irr_fr_lu_49", 
                 "irr_fr_lu_5", "irr_fr_lu_50", "irr_fr_lu_51", 
                 "irr_fr_lu_52", "irr_fr_lu_53", "irr_fr_lu_54", 
                 "irr_fr_lu_55", "irr_fr_lu_56", "irr_fr_lu_57", 
                 "irr_fr_lu_58", "irr_fr_lu_59", "irr_fr_lu_6", 
                 "irr_fr_lu_61", "irr_fr_lu_66", "irr_fr_lu_67", 
                 "irr_fr_lu_68", "irr_fr_lu_69", "irr_fr_lu_71", 
                 "irr_fr_lu_76", "irr_fr_lu_77"]
"""

#for Willamette only (major crops, will not simulate other crops)
fraction_list = ["irr_fr_lu_1", 
                 "irr_fr_lu_14",
                 "irr_fr_lu_23",
                 "irr_fr_lu_24", 
                 "irr_fr_lu_28",
                 "irr_fr_lu_42",
                 "irr_fr_lu_56",
                 "irr_fr_lu_58",
                 "irr_fr_lu_59",
                 "irr_fr_lu_176",
                 "irr_fr_lu_246"]



#if there is fractional irrigated crops in grid cell. the irrigated crop is coded as the original crops 
# and the non-irrigated crops are coded as the origincal code + 10,000
# LML: there is an asumption that all crops without "dryland" in the name are irigated, i.e. there is no irrigation (1 or 0) file as input to generate irrigation map
"""
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
"""
lai_default_missed = "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5"

cdl_to_vic_dic = { 
                   "irr_fr_lu_182" : "102", 
                   "irr_fr_lu_145" : "4005", 
                   "irr_fr_lu_146" : "4006",
                   "irr_fr_lu_147" : "4007", 
                   "irr_fr_lu_167" : "4010",
                   "irr_fr_lu_153" : "4101",
                   "irr_fr_lu_136" : "7206",
                   "irr_fr_lu_191" : "7806",
                   "irr_fr_lu_122" : "8205",
                   "irr_fr_lu_192" : "8704",
                   "irr_fr_lu_174" : "8819",
                   
                   "irr_fr_lu_188" : "2505",
                   "irr_fr_lu_190" : "2504",
                   "irr_fr_lu_133" : "4011",
                   "irr_fr_lu_179" : "6002",
                   "irr_fr_lu_162" : "4009",
                   "irr_fr_lu_120" : "6001",
                   "irr_fr_lu_154" : "8514",
                   "irr_fr_lu_197" : "7807",
                   "irr_fr_lu_185" : "198",
                   "irr_fr_lu_177" : "4004",
                   "irr_fr_lu_183" : "103",
                   "irr_fr_lu_137" : "7207",
                   "irr_fr_lu_158" : "8907",
                   "irr_fr_lu_168" : "4010"
                 }

out_veg_list = [
                   "102",
                   "103",
                   "198",
                   "2504",
                   "2505",
                   "4004",
                   "4005", 
                   "4006",
                   "4007",
                   "4009",
                   "4010",
                   "4011",
                   "4101",
                   "6001",
                   "6002",
                   "7206",
                   "7207",
                   "7806",
                   "7807",
                   "8205",
                   "8514",
                   "8704",
                   "8819",
                   "8907"
                 ]

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

irri_type = {}
default_irrig_parameter = "IrrigTP_Sub_surf_drip_perfect"

#vegetation types should be included in veg parameter file
included_types = []

#get cell list
allcell = list()
with open(cell_list) as f:
    for line in f:
        a = line.split()
        if len(a) > 0:
            cellid = a[0]
            if cellid not in allcell:
                allcell.append(cellid)
print("Finish reading cell.\n")

"""
#read old veg dic and creat a dictionary
old_natural_veg_dic = dict()
lai_dic = dict()
with open(vic_veg_parameter_file) as v:
    for line in v:
        a = line.split()
        if (len(a) == 2):
            gridid = a[0]
            t = dict()
        elif (len(a) == 8):
            vegid = a[0]
            area = float(a[1])
            #in old vegetation parameter file, the type 11 is "corn"
            if (int(vegid) <= 10):
                t[vegid] = area
                old_natural_veg_dic[gridid] = t
        elif (len(a) == 12):
            lai_key = gridid + "_" + vegid
            lai_dic.update({lai_key : line})
print("reading old veg parameter is done")
"""


#out_veg_list = ["1", "4", "5", "10", "701", "807", "1401", "1403", "2501", "4004", "4005", "4006", "4007", "4008", "4009", "4010", "4011", "4100", "4101", "4102", "4103", "4104", "6001"]

#out_veg_list = ["1", "4", "5", "10", "701", "807", "1401", "1403", "2501", "4004", 
#                "4005", "4006", "4007", "4008", "4009", "4010", "4011", "4100", 
#                "4101", "4102", "4103", "4104", "6001",
#                "12501", "14005", "14006", "14010", "14011", "14101", "14103", "16001"]


    
outfile_veg = open(out_veg_file,"w")
outfile_irrig = open(out_irrig_file,"w")
outlai = "      " + lai_default_missed + "\n"
recorded_cell = list()
with open(fraction_file) as f:
    for line in f:
        if "vicid" in line:
            cols = line.split(",")
        else:
            #produce veg parameter file
            tot_fractions = []
            for veg in out_veg_list:
                tot_fractions.append(0)
            a = line.split(",")
            if (len(a) > 0 and a[0] in allcell):
                for vegtype in cdl_to_vic_dic:
                    #find fraction for each cdl type
                    array_index = cols.index(vegtype)
                    fraction = float(a[array_index])
                    #find index in tot_fractions
                    veg_out_index = out_veg_list.index(cdl_to_vic_dic[vegtype])
                    tot_fractions[veg_out_index] += fraction
                total_area = 0
                total_veg_num = 0
                for ov in range(0,len(out_veg_list)):
                    total_area += tot_fractions[ov]
                    if (tot_fractions[ov] > 0.00001):
                        total_veg_num += 1
                line = str(a[0]) + " " + str(total_veg_num) + "\n"
                recorded_cell.append(str(a[0]))
                outfile_veg.write(line)
                for ov in range(0,len(out_veg_list)):
                    if (tot_fractions[ov] > 0.00001):
                        if out_veg_list[ov] in paramter_dic:
                            outp = paramter_dic[out_veg_list[ov]]
                        else:
                            outp = default_veg_parameter
                        line = "   " + out_veg_list[ov] + " " + str('%.5f' % tot_fractions[ov]) + " " + outp + "\n"
                        outfile_veg.write(line)
                        outfile_veg.write(outlai)
                    
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
                    if (tot_fractions[ov] > 0.00001):
                        total_veg_num += 1
                
                if total_veg_num > 0:
                    line = str(a[0]) + " " + str(total_veg_num) + "\n"
                    outfile_irrig.write(line)
                for ov in range(0,len(out_veg_list)):
                    if tot_fractions[ov] > 0.00001:
                        if out_veg_list[ov] in irri_type:
                            outp = irri_type[out_veg_list[ov]]
                            line = "   " + out_veg_list[ov] + " " + outp + "\n"
                            outfile_irrig.write(line)
                        else:
                            outp = default_irrig_parameter
                            line = "   " + out_veg_list[ov] + " " + outp + "\n"
                            outfile_irrig.write(line)
#fill no recorded veg paramater
for cell in allcell:
    if cell not in recorded_cell:
        outline = cell + " 0" + "\n"
        outfile_veg.write(outline)
outfile_veg.close()
outfile_irrig.close()
        
            
            
print("Done!")
