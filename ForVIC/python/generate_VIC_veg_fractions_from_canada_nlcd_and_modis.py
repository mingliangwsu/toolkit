#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Nov. 12, 2019, LIU
Based on NLCD, impervious surface, and MODIS to generate vegetation fractions for each VIC gridcell 
@author: liuming
"""

#import pandas as pd
import sys 
import os

def sortkey(x): 
    return int(x)

#input lists:
#monthly LAI
#use_old_veg_parameter_lai = True

inout_data_path = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/arcinfo/"
#CA_crop = "/mnt/hydronas/Projects/BPA_CRB/GIS/Canada_BC/CA_Landuse.csv"
#WSDA_crop = "/mnt/hydronas/Projects/BPA_CRB/GIS/WSDA2017_011819/vic_croptype_area_and_fraction.txt"
#USDA_cdl = "/mnt/hydronas/Projects/BPA_CRB/GIS/CDL2017/USCDL_Landuse.csv"
#vic_area = "/mnt/hydronas/Projects/BPA_CRB/GIS/boundary/vicid_areakm2_list.txt"
#wsda_vic_list_file = "/mnt/hydronas/Projects/BPA_CRB/GIS/WSDA2017_011819/vic_in_WA_90percent.txt"

vic_area = inout_data_path + "crbvicida.csv"
vic_modis_nlcd = inout_data_path + "camod2.csv"
#vic_imp = inout_data_path + "impvic.csv"
vic_nlcd = inout_data_path + "canlcdvic.csv"

outdir = "/home/liuming/temp/temp"
out_veg_file = "landcover_fraction_canada_nlcd_modis.txt"
out_log = "landcover_fraction_canada_nlcd_modis_log.txt"


#modis area over PNW region (it is a rough estimation being used when no MODIS fraction is available in VIC gridcell)
default_modis_forest_fraction_dic = {
        "1" : 0.992978,
        "2" : 0.000143,
        "3" : 0.005629,
        "4" : 0.001251}

default_modis_shrub_fraction_dic = {
        "6" : 0.109527,
        "7" : 0.390337,
        "8" : 0.470187,
        "9" : 0.029949}

#nlcd_type_list = ["11","12", "21", "22", "23", "24","31", "41", "42", "43", "52", "71", "81", "82", "90", "95"]
nlcd_type_list = ["10", "20", "30", "34", "35", "50", "80", "110", "120", "122", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "160", "162", "167", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "185", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199", "200", "210", "220", "230"]
nlcd_crops = ["35", "120", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "160", "162", "167", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "185", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199"]
life_forest = ["deciduous", "evergreen"]
leaf_forest = ["needle", "broad"]
#nlcd_shrub = ["52"]
nlcd_shrub = ["50"]
#nlcd_delveloped = ["21", "22", "23", "24"]
nlcd_delveloped = ["34"]
vic_class = ["1","2","3","4","5","6","7","8","9","10","11","12","13", "14"] #12: impervious 13: pasture/hay 14: other land

modis_forest_fraction_dic = dict()  #[grid][41 or 42][0: needle  1: broad]
modis_shrub_fraction_dic = dict()
#modis_sum_forest_fraction_dic = dict()
#modis_sum_shrub_fraction_dic = dict()
vic_area_num30pix_dic = dict()  #in number of 30m X 30m pixels
vic_modis_nlcd_num30pix_dic = dict()
vic_class_num30pix_dic = dict()
vic_nlcd_num30pix_dic = dict()
#vic_imp_persum = dict()



#out_irrig_file = "Umatila_irrigation_parameter_180814.txt"
#if use_old_veg_parameter_lai:
#    old_veg_parameter_filename = "/mnt/hydronas/Projects/Forecast2020/Landuse/vegparam_final2016_with_crp.txt"

MIN_FRACTION = 0.000001

#Read vic area file


os.chdir(outdir)

"""
bc_to_vic_dic = {
                "lu_34": "12",
                "lu_35": "1306",
                "lu_50": "6",
                "lu_80": "13",
                "lu_110": "10",
                "lu_120": "6001",
                "lu_122": "2501",
                "lu_130": "6001",
                "lu_133": "4011",
                "lu_136": "7206",
                "lu_137": "7207",
                "lu_140": "4005",
                "lu_145": "4005",
                "lu_146": "4006",
                "lu_147": "4007",
                "lu_153": "4101",
                "lu_162": "4009",
                "lu_167": "4010",
                "lu_174": "6001",
                "lu_177": "4004",
                "lu_179": "6001",
                "lu_188": "2502",
                "lu_190": "2002",
                "lu_192": "2501",
                "lu_197": "2501",
                "lu_210": "1",
                "lu_220": "4",
                "lu_230": "5"}

cdl_to_vic_dic = {
                "lu_1": "4007",
                "lu_4": "7720",
                "lu_5": "8907",
                "lu_6": "8906",
                "lu_12": "4008",
                "lu_13": "4007",
                "lu_14": "807",
                "lu_21": "4011",
                "lu_22": "4012",
                "lu_23": "4006",
                "lu_24": "4005",
                "lu_25": "6001",
                "lu_27": "7207",
                "lu_28": "7206",
                "lu_29": "9203",
                "lu_30": "6001",
                "lu_31": "4101",
                "lu_32": "8514",
                "lu_33": "8518",
                "lu_34": "9205",
                "lu_35": "8904",
                "lu_36": "701",
                "lu_37": "2501",
                "lu_38": "6001",
                "lu_39": "7202",
                "lu_41": "8832",
                "lu_42": "4010",
                "lu_43": "4004",
                "lu_44": "6001",
                "lu_47": "2502",
                "lu_48": "8001",
                "lu_49": "4100",
                "lu_50": "6002",
                "lu_52": "8819",
                "lu_53": "4009",
                "lu_55": "107",
                "lu_56": "806",
                "lu_57": "898",
                "lu_58": "708",
                "lu_59": "4104",
                "lu_66": "1403",
                "lu_67": "1407",
                "lu_68": "1401",
                "lu_69": "2002",
                "lu_70": "402",
                "lu_71": "402",
                "lu_76": "1411",
                "lu_77": "1409",
                "lu_82": "12",
                "lu_87": "13",
                "lu_88": "10",
                "lu_121": "12",
                "lu_122": "12",
                "lu_123": "12",
                "lu_124": "12",
                "lu_141": "4",
                "lu_142": "1",
                "lu_143": "5",
                "lu_152": "6",
                "lu_176": "10",
                "lu_190": "13",
                "lu_195": "13",
                "lu_205": "9209",
                "lu_206": "4102",
                "lu_207": "8802",
                "lu_208": "8817",
                "lu_209": "6002",
                "lu_214": "8807",
                "lu_216": "6002",
                "lu_218": "2502",
                "lu_219": "2207",
                "lu_220": "1410",
                "lu_221": "106",
                "lu_222": "8831",
                "lu_223": "1402",
                "lu_224": "7602",
                "lu_225": "4005",
                "lu_227": "8820",
                "lu_229": "8828",
                "lu_237": "4011",
                "lu_242": "102",
                "lu_243": "8809",
                "lu_244": "8811",
                "lu_246": "8839",
                "lu_247": "9208",
                "lu_249": "6002"}
                
wsda_to_vic_dic = {
                    "Alfalfa Hay": "701",
                    "Alfalfa Seed": "1501",
                    "Alfalfa/Grass Hay": "703",
                    "Alkali Bee Bed": "713",
                    "Allium": "2501",
                    "Apple": "1401",
                    "Apricot": "1402",
                    "Artichoke": "1801",
                    "Asparagus": "8802",
                    "Barley": "4011",
                    "Barley Hay": "7702",
                    "Bean Seed": "4010",
                    "Bean, Dry": "4010",
                    "Bean, Green": "8804",
                    "Beet Seed": "8502",
                    "Berry, Unknown": "198",
                    "Blueberry": "102",
                    "Bluegrass Seed": "8503",
                    "Broccoli": "8807",
                    "Bromegrass Seed": "8504",
                    "Brussels Sprouts": "8808",
                    "Buckwheat": "7202",
                    "Cabbage": "8809",
                    "Cabbage Seed": "8506",
                    "Caneberry": "107",
                    "Canola": "4101",
                    "Cantaloupe": "8002",
                    "Carrot": "4102",
                    "Carrot Seed": "8507",
                    "Cauliflower": "8811",
                    "Cereal Grain, Unknown": "6001",
                    "Cherry": "1403",
                    "Chestnut": "1404",
                    "Chickpea": "8813",
                    "Christmas Tree": "402",
                    "Cilantro Seed": "8525",
                    "Clover Hay": "708",
                    "Clover Seed": "4101",
                    "Clover/Grass Hay": "708",
                    "Conifer Seed": "1510",
                    "Corn Seed": "4007",
                    "Corn, Field": "4007",
                    "Corn, Sweet": "4008",
                    "Corn, Unknown": "4007",
                    "Cranberry": "103",
                    "Cucumber": "8815",
                    "Currant": "104",
                    "Daffodil": "7502",
                    "Dahlia": "2501",
                    "Dill": "8901",
                    "Driving Range": "2501",
                    "Fescue Seed": "8526",
                    "Filbert": "1405",
                    "Flax": "6001",
                    "Flax Seed": "6001",
                    "Garlic": "8817",
                    "Golf Course": "1702",
                    "Grape, Juice": "2001",
                    "Grape, Table": "2098",
                    "Grape, Unknown": "2098",
                    "Grape, Wine": "2002",
                    "Grass Hay": "713",
                    "Grass Seed, Other": "4104",
                    "Green Manure": "601",
                    "Hay/Silage, Unknown": "703",
                    "Hemp": "2501",
                    "Hops": "806",
                    "Iris": "2501",
                    "Kale": "6002",
                    "Leek": "6002",
                    "Legume Cover": "6003",
                    "Lentil": "8819",
                    "Marijuana": "2400",
                    "Market Crops": "6002",
                    "Medicinal Herb": "7801",
                    "Melon, Unknown": "8001",
                    "Mint": "807",
                    "Mustard": "8904",
                    "Nectarine/Peach": "1407",
                    "Nursery, Caneberry": "1312",
                    "Nursery, Greenhouse": "1306",
                    "Nursery, Holly": "1307",
                    "Nursery, Lavender": "1308",
                    "Nursery, Lilac": "1308",
                    "Nursery, Orchard/Vineyard": "1304",
                    "Nursery, Ornamental": "1311",
                    "Nursery, Silviculture": "1303",
                    "Oat": "7206",
                    "Oat Hay": "705",
                    "Onion": "4100",
                    "Onion Seed": "6004",
                    "Orchard, Unknown": "2502",
                    "Parsley": "6002",
                    "Pasture": "1205",
                    "Pea Seed": "8824",
                    "Pea, Dry": "8824",
                    "Pea, Green": "4009",
                    "Pear": "1409",
                    "Peony": "6005",
                    "Pepper": "8826",
                    "Plum": "1410",
                    "Poplar": "403",
                    "Potato": "4004",
                    "Potato Seed": "4004",
                    "Pumpkin": "8828",
                    "Quinoa": "6001",
                    "Radish Seed": "6001",
                    "Reclamation Seed": "6001",
                    "Research Station": "6001",
                    "Rhubarb": "8829",
                    "Rosemary": "2501",
                    "Rutabaga": "8836",
                    "Rye": "7207",
                    "Rye Hay": "6006",
                    "Ryegrass Seed": "1517",
                    "Seed, Other": "6004",
                    "Shellfish": "1601",
                    "Silviculture": "401",
                    "Sod Farm": "1704",
                    "Sorghum": "7720",
                    "Soybean": "8907",
                    "Spinach": "6002",
                    "Spinach Seed": "6004",
                    "Squash": "8831",
                    "Strawberry": "106",
                    "Sudangrass": "721",
                    "Sugar Beet": "8832",
                    "Sugar Beet Seed": "8520",
                    "Sunflower": "8906",
                    "Sunflower Seed": "8906",
                    "Tea": "804",
                    "Timothy": "722",
                    "Tobacco": "802",
                    "Tomato": "8834",
                    "Triticale": "9209",
                    "Triticale Hay": "9210",
                    "Tulip": "505",
                    "Unknown": "6001",
                    "Vegetable, Unknown": "6002",
                    "Walnut": "1411",
                    "Watermelon": "8001",
                    "Wheat": "4005",
                    "Wildlife Feed": "2501",
                    "Yarrow Seed": "6004",
                    "Yellow Mustard": "7603"}
if use_old_veg_parameter_lai:
    lai_dic_default = {
            "1"    : "3.4 3.4 3.5 3.7 4 4.4 4.4 4.3 4.2 3.7 3.5 3.4",
            "2"    : "3.4 3.4 3.5 3.7 4 4.4 4.4 4.3 4.2 3.7 3.5 3.4",
            "3"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "4"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "5"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "6"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "7"    : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "8"    : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "9"    : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "10"   : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "11"   : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "12"   : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "13"   : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2"}
    lai_default_missed = "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5"


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
"""

"""
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
"""

#out_veg_list = ["1", "4", "5", "10", "701", "807", "1401", "1403", "2501", "4004", "4005", "4006", "4007", "4008", "4009", "4010", "4011", "4100", "4101", "4102", "4103", "4104", "6001"]

out_veg_list = list()
    
outfile_veg = open(out_veg_file,"w")
fout_log = open(out_log,"w")
#outfile_irrig = open(out_irrig_file,"w")

#get vic area for each grid
#vic_area_dic = dict()
with open(vic_area) as f:
    for line in f:
        a = line.split(",")
        if len(a) > 0:
            if a[0] not in vic_area_num30pix_dic and a[0] != "VALUE":
                vic_area_num30pix_dic[a[0]] = float(a[1])
print("reading vic area done!")

#initialize VIC modis fractions

for grid in vic_area_num30pix_dic:
    if grid not in modis_forest_fraction_dic:
        modis_forest_fraction_dic[grid] = dict()
    for life in life_forest:
        modis_forest_fraction_dic[grid][life] = dict()
        for leaf in leaf_forest:
            modis_forest_fraction_dic[grid][life][leaf] = 0
        
        
    if grid not in modis_shrub_fraction_dic:
        modis_shrub_fraction_dic[grid] = dict()
    #if grid not in modis_sum_forest_fraction_dic:
    #    modis_sum_forest_fraction_dic[grid] = 0
    #if grid not in modis_sum_shrub_fraction_dic:
    #    modis_sum_shrub_fraction_dic[grid] = 0    
    
    if grid not in vic_nlcd_num30pix_dic:
        vic_nlcd_num30pix_dic[grid] = dict()
    #if grid not in vic_imp_persum:
    #    vic_imp_persum[grid] = 0
    if grid not in vic_class_num30pix_dic:    
        vic_class_num30pix_dic[grid] = dict()
        
    #for forest in default_modis_forest_fraction_dic:
    #    if forest not in modis_forest_fraction_dic[grid]:
    #        modis_forest_fraction_dic[grid][forest] = 0
    for shrub in default_modis_shrub_fraction_dic:
        if shrub not in modis_shrub_fraction_dic[grid]:
            modis_shrub_fraction_dic[grid][shrub] = 0
    for nlcd in nlcd_type_list:
        if nlcd not in vic_nlcd_num30pix_dic[grid]:
            vic_nlcd_num30pix_dic[grid][nlcd] = 0
    for vicclass in vic_class:
        if vicclass not in vic_class_num30pix_dic[grid]:
            vic_class_num30pix_dic[grid][vicclass] = 0
print("initialize vic area done!")

#reading impervious surface area data
#with open(vic_imp) as f:
#    for line in f:
#        a = line.rstrip().split(",")
#        if len(a) > 0:
#            if a[2] in vic_imp_persum and a[0] != "VALUE":
#                vic_imp_persum[a[2]] += float(a[1]) * float(a[3])
#print("initialize imp done!")
#"vic_imp_persum * 0.01 / vic_area_num30pix_dic" is the fraction of impervious surface in each VIC grid cell

#read modis and nlcd combination data
with open(vic_modis_nlcd) as f:
    for line in f:
        a = line.rstrip().split(",")
        if len(a) > 0:
            if a[0] != "VALUE":
                #forest
                count = float(a[1]);
                if a[2] in modis_forest_fraction_dic and a[3] in default_modis_forest_fraction_dic:
                    if a[4] == "210": #needle
                        if a[3] == "1":
                            modis_forest_fraction_dic[a[2]]["evergreen"]["needle"] += count
                        elif a[3] == "3":
                            modis_forest_fraction_dic[a[2]]["deciduous"]["needle"] += count
                    elif a[4] == "220": #broadleaf
                        if a[3] == "2":
                            modis_forest_fraction_dic[a[2]]["evergreen"]["broad"] += count
                        elif a[3] == "4":
                            modis_forest_fraction_dic[a[2]]["deciduous"]["broad"] += count
                    #modis_sum_forest_fraction_dic[a[2]] += float(a[1])
                #shrub
                if a[2] in modis_shrub_fraction_dic and a[3] in default_modis_shrub_fraction_dic and a[4] in nlcd_shrub:
                    modis_shrub_fraction_dic[a[2]][a[3]] += float(a[1])
                    #modis_sum_shrub_fraction_dic[a[2]] += float(a[1])
print("read modis nlcd combination done!")

#read VIC each nlcd class
with open(vic_nlcd) as f:
    for line in f:
        a = line.rstrip().split(",")
        #print(a[2])
        if len(a) > 0:
            if a[0] != "VALUE":
                #sum other types directly from nlcd classes
                if a[2] in vic_nlcd_num30pix_dic and a[3] in nlcd_type_list:
                    #print(a[2] + " " + a[3])
                    vic_nlcd_num30pix_dic[a[2]][a[3]] += float(a[1])
print("read vic nlcd combination done!")

#calculating fractions
for grid in vic_area_num30pix_dic:
    #calculating total land pixels from nlcd
    total_land = 0
    total_developed = 0
    
    for nlcd in nlcd_type_list:
        if nlcd != "20":
            total_land += vic_nlcd_num30pix_dic[grid][nlcd]
        if nlcd in nlcd_delveloped:
            total_developed += vic_nlcd_num30pix_dic[grid][nlcd]
        elif nlcd == "210" or nlcd == "220":
            sum_needle = modis_forest_fraction_dic[a[2]]["evergreen"]["needle"] + modis_forest_fraction_dic[a[2]]["deciduous"]["needle"]
            if sum_needle >= 1:
                frac_needle_dec = float(modis_forest_fraction_dic[a[2]]["deciduous"]["needle"] / sum_needle)
            else:
                frac_needle_dec = default_modis_forest_fraction_dic["3"] / (default_modis_forest_fraction_dic["1"] + default_modis_forest_fraction_dic["3"])
            frac_needle_evg = 1.0 - frac_needle_dec
            
            sum_broadleaf = modis_forest_fraction_dic[a[2]]["evergreen"]["broad"] + modis_forest_fraction_dic[a[2]]["deciduous"]["broad"]
            if sum_broadleaf >= 1:
                frac_broad_dec = float(modis_forest_fraction_dic[a[2]]["deciduous"]["broad"] / sum_broadleaf)
            else:
                frac_broad_dec = default_modis_forest_fraction_dic["4"] / (default_modis_forest_fraction_dic["2"] + default_modis_forest_fraction_dic["4"])
            frac_broad_evg = 1.0 - frac_broad_dec
            
            if nlcd == "210":
                vic_class_num30pix_dic[grid]["3"] += vic_nlcd_num30pix_dic[grid][nlcd] * frac_needle_dec
                vic_class_num30pix_dic[grid]["1"] += vic_nlcd_num30pix_dic[grid][nlcd] * frac_needle_evg
            elif nlcd == "220":
                vic_class_num30pix_dic[grid]["4"] += vic_nlcd_num30pix_dic[grid][nlcd] * frac_broad_dec
                vic_class_num30pix_dic[grid]["2"] += vic_nlcd_num30pix_dic[grid][nlcd] * frac_broad_evg

        elif nlcd == "230":
            vic_class_num30pix_dic[grid]["5"] += vic_nlcd_num30pix_dic[grid][nlcd]
        elif nlcd == "50":
            sum_shrub = 0 
            for shrub in default_modis_shrub_fraction_dic:
                sum_shrub += modis_shrub_fraction_dic[grid][shrub]
            for shrub in default_modis_shrub_fraction_dic:
                if sum_shrub >= 1:
                    fraction = modis_shrub_fraction_dic[grid][shrub] / sum_shrub
                else:
                    fraction = default_modis_shrub_fraction_dic[shrub]
                if shrub == "6": #close shrub
                    vic_class_num30pix_dic[grid]["8"] += vic_nlcd_num30pix_dic[grid][nlcd] * fraction
                elif shrub == "7": #open shrub
                    vic_class_num30pix_dic[grid]["9"] += vic_nlcd_num30pix_dic[grid][nlcd] * fraction
                elif shrub == "8": #wood savana
                    vic_class_num30pix_dic[grid]["6"] += vic_nlcd_num30pix_dic[grid][nlcd] * fraction
                elif shrub == "9": #savana
                    vic_class_num30pix_dic[grid]["7"] += vic_nlcd_num30pix_dic[grid][nlcd] * fraction
        elif nlcd == "110":
            vic_class_num30pix_dic[grid]["10"] += vic_nlcd_num30pix_dic[grid][nlcd]
        elif nlcd == "122":
            vic_class_num30pix_dic[grid]["13"] += vic_nlcd_num30pix_dic[grid][nlcd]
        elif nlcd in nlcd_crops:
            vic_class_num30pix_dic[grid]["11"] += vic_nlcd_num30pix_dic[grid][nlcd]
        elif nlcd == "230":
            vic_class_num30pix_dic[grid]["6"] += vic_nlcd_num30pix_dic[grid][nlcd]
        elif nlcd == "80":
            vic_class_num30pix_dic[grid]["10"] += vic_nlcd_num30pix_dic[grid][nlcd]
        elif nlcd == "10" or nlcd == "30" or nlcd == "130" or nlcd == "131":
            vic_class_num30pix_dic[grid]["14"] += vic_nlcd_num30pix_dic[grid][nlcd]
    #if total_developed >= total_impervious:
    vic_class_num30pix_dic[grid]["12"] += total_developed * 0.246  #the fractions is from the average over USA (number of 30mX30m pixel)
    vic_class_num30pix_dic[grid]["13"] += total_developed * (1.0 - 0.246)
    #else:
        #vic_class_num30pix_dic[grid]["12"] += total_developed
print("generate total pixels VIC classes done!")          

#generate fraction:
outfile_veg.write("grid")
for victype in vic_class:
    outfile_veg.write(",vic_" + victype)
outfile_veg.write("\n")
for grid in sorted(vic_area_num30pix_dic, key=sortkey, reverse=False):
    total_area = 0
    for victype in vic_class:
        if victype != "20":
            total_area += vic_class_num30pix_dic[grid][victype]
    if vic_area_num30pix_dic[grid] >= (32543 * 0.9):
        if total_area / vic_area_num30pix_dic[grid] > MIN_FRACTION:
            outfile_veg.write(grid)
            for victype in sorted(vic_class,key=sortkey, reverse=False):
                vic_class_num30pix_dic[grid][victype] /= vic_area_num30pix_dic[grid]
                outfile_veg.write("," + str('%.6f' % vic_class_num30pix_dic[grid][victype]))
            outfile_veg.write("\n")


"""
#read old veg dic and creat a dictionary
lai_dic = {}
if use_old_veg_parameter_lai:
    with open(old_veg_parameter_filename) as v:
        for line in v:
            a = line.split()
            if (len(a) == 2):
                gridid = a[0]
            elif (len(a) == 8):
                vegid = a[0]
            elif (len(a) == 12):
                lai_key = gridid + "_" + vegid
                lai_dic.update({lai_key : line})
    print("reading veg parameter is done")



#each dataset fraction (vegetation library code); the "total" is original total fraction
bc_frac = dict()
cdl_frac = dict()
wsda_frac = dict()

#read bc:
head_list = list()
with open(CA_crop) as f:
    for line in f:
        a = line.split(",")
        if "vicid" in a:
            head_list = a
        else:
            orig_data = dict()
            total_area = 0.0
            col = 0
            for var in head_list:
                if var != "vicid":
                    orig_data[var] = float(a[col])
                    total_area += orig_data[var]
                else:
                    orig_data[var] = a[col]
                col += 1
            t = dict()
            t["total"] = total_area
            if total_area > MIN_FRACTION:
                for var in orig_data:
                    if var in bc_to_vic_dic:
                        if bc_to_vic_dic[var] not in t:
                            t[bc_to_vic_dic[var]] = orig_data[var]
                        else:
                            t[bc_to_vic_dic[var]] += orig_data[var]
                bc_frac[orig_data["vicid"]] = t
print("bc done!")

#read wsda:
#head_list = list()

with open(WSDA_crop) as f:
    for line in f:
        a = line.split("\t")
        if "GRID_CODE" not in a:
            if len(a) > 0:
                if a[0] not in wsda_frac:
                    t = dict()
                    t["total"] = 0
                    wsda_frac[a[0]] = t
                wsda_frac[a[0]]["total"] += float(a[3])
                if a[1] in wsda_to_vic_dic:
                    if wsda_to_vic_dic[a[1]] not in wsda_frac[a[0]]:
                        wsda_frac[a[0]][wsda_to_vic_dic[a[1]]] = float(a[3])
                    else:
                        wsda_frac[a[0]][wsda_to_vic_dic[a[1]]] += float(a[3])
print("WSDA done!")

#read cdl:
head_list = list()
with open(USDA_cdl) as f:
    for line in f:
        a = line.split(",")
        if "vicid" in a:
            head_list = a
        else:
            orig_data = dict()
            total_area = 0.0
            col = 0
            for var in head_list:
                if var != "vicid":
                    orig_data[var] = float(a[col])
                    total_area += orig_data[var]
                else:
                    orig_data[var] = a[col]
                col += 1
            t = dict()
            t["total"] = total_area
            if total_area > MIN_FRACTION:
                for var in orig_data:
                    if var in cdl_to_vic_dic:
                        if cdl_to_vic_dic[var] not in t:
                            t[cdl_to_vic_dic[var]] = orig_data[var]
                        else:
                            t[cdl_to_vic_dic[var]] += orig_data[var]
                cdl_frac[orig_data["vicid"]] = t
print("cdl done!")

#get WSDA VIC gridcell list (the grid cell has 90% area in WA state)
wsda_valid_list = list()
with open(wsda_vic_list_file) as f:
    for line in f:
        a = line.split()
        if len(a) > 0:
            wsda_valid_list.append(a[0])
print("add wsda vic cell list done!")

##generate final output
final_data = dict()
for cell in cdl_frac:
    if cdl_frac[cell]["total"] >= MIN_FRACTION:
        if cell not in final_data:
            t = dict()
            final_data[cell] = t
        #check if WSDA information should be used
        wsda_crop = 0
        if cell in wsda_frac:
            wsda_crop = wsda_frac[cell]["total"]
        cdl_crop = 0
        cdl_natveg = 0
        for crop in cdl_frac[cell]:
            if crop != "total":
                if int(crop) > 13:
                    cdl_crop += cdl_frac[cell][crop]
                else:
                    cdl_natveg += cdl_frac[cell][crop]
        #if ((wsda_crop >= 0.5 * cdl_crop) and (wsda_crop > MIN_FRACTION)):
        #if cell in wsda_valid_list and cell in wsda_frac:
        if cell in wsda_valid_list:
            #use crop area from wsda_crop
            print(cell + " use WSDA")
            fout_log.write(cell + " use WSDA")
            if cell in wsda_frac:
                for crop in wsda_frac[cell]:
                    if crop != "total":
                        final_data[cell][crop] = wsda_frac[cell][crop]
            adj = 1.0
            if ((cdl_natveg > (1.0 - wsda_crop)) and (cdl_natveg > MIN_FRACTION)):
                adj = (1.0 - wsda_crop) / cdl_natveg;
            #get natural veg cover from cdl
            for crop in cdl_frac[cell]:
                if crop != "total":
                    if int(crop) <= 13:
                        final_data[cell][crop] = cdl_frac[cell][crop] * adj;
        else:
            #use cdl all fractions
            print(cell + " use CDL")
            fout_log.write(cell + " use CDL")
            for crop in cdl_frac[cell]:
                if crop != "total":
                    final_data[cell][crop] = cdl_frac[cell][crop];
print("merge WSDA & CDL data done")

#use CA data:
for cell in bc_frac:
    total_bc_area = bc_frac[cell]["total"]
    if cell in final_data:
        #total_final = 0.0
        #for crop in final_data[cell]:
        #    total_final += final_data[cell][crop]
        #if ((total_bc_area > total_final) and (total_bc_area > MIN_FRACTION)):
        if (int(cell) >= 356383):
            print(cell + " use BC")
            fout_log.write(cell + " use BC")
            final_data.pop(cell)
            t = dict()
            for crop in bc_frac[cell]:
                if crop != "total":
                    t[crop] = bc_frac[cell][crop]
            final_data[cell] = t;
    else:
        t = dict()
        for crop in bc_frac[cell]:
            if crop != "total":
                t[crop] = bc_frac[cell][crop]
        final_data[cell] = t;
print("merge WSDA & CDL & BC data done")

#special case for shrub_lai:
shrubs = ["6", "7", "8", "9"]

#output final vegetation parameter
for cell in sorted(final_data):
    sum_f = 0.0
    types = 0
    for crop in sorted(final_data[cell]):
        if final_data[cell][crop] > MIN_FRACTION:
            sum_f += final_data[cell][crop]
            types += 1
    outfile_veg.write(cell + " " + str(types) + "\n")
    if types > 0:
        for crop in sorted(final_data[cell], key=sortkey, reverse=False):
            if final_data[cell][crop] > MIN_FRACTION:
                if crop in paramter_dic:
                    outp = paramter_dic[crop]
                else:
                    outp = default_veg_parameter
                line = "   " + crop + " " + str('%.4f' % final_data[cell][crop]) + " " + outp + "\n"
                outfile_veg.write(line)
                if use_old_veg_parameter_lai:
                    laikey = cell + "_" + crop
                    if laikey in lai_dic and int(crop) < 100:
                        outlai = lai_dic[laikey]
                    elif crop in shrubs and (((cell + "_6") in lai_dic) or ((cell + "_7") in lai_dic) or ((cell + "_8") in lai_dic) or ((cell + "_9") in lai_dic)):
                        if (cell + "_6") in lai_dic:
                            outlai = lai_dic[cell + "_6"]
                        elif (cell + "_7") in lai_dic:
                            outlai = lai_dic[cell + "_7"]
                        elif (cell + "_8") in lai_dic:
                            outlai = lai_dic[cell + "_8"]
                        elif (cell + "_9") in lai_dic:
                            outlai = lai_dic[cell + "_9"]
                    elif crop in lai_dic_default:
                        outlai = "      " + lai_dic_default[crop] + "\n"
                    else:
                        outlai = "      " + lai_default_missed + "\n"
                    outfile_veg.write(outlai)
print("write output done")
"""

"""
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
                if (tot_fractions[ov] > MIN_FRACTION):
                    total_veg_num += 1
            line = str(a[0]) + " " + str(total_veg_num) + "\n"
            outfile_veg.write(line)
            for ov in range(0,len(out_veg_list)):
                if (tot_fractions[ov] > MIN_FRACTION):
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
"""
"""
            total_veg_num = 0
            #for ov in range(0,len(fraction_list)):
            #    vicveg = cdl_to_vic_dic[fraction_list[ov]]
            #    vicveg_index = out_veg_list.index(vicveg)
            #    tot_fractions[vicveg_index] = a[ov+1]
            #    if tot_fractions[vicveg_index] == "1":
            #        total_veg_num += 1
            for ov in range(0,len(out_veg_list)):
                if (tot_fractions[ov] > MIN_FRACTION):
                    if out_veg_list[ov] in irri_type:
                        total_veg_num += 1
            
            if total_veg_num > 0:
                line = str(a[0]) + " " + str(total_veg_num) + "\n"
                outfile_irrig.write(line)
            for ov in range(0,len(out_veg_list)):
                if tot_fractions[ov] > MIN_FRACTION:
                    if out_veg_list[ov] in irri_type:
                        outp = irri_type[out_veg_list[ov]]
                        line = "   " + out_veg_list[ov] + " " + outp + "\n"
                        outfile_irrig.write(line)
                    
"""
outfile_veg.close()
fout_log.close()
#outfile_irrig.close()
        
            
            
print("reading done!")
