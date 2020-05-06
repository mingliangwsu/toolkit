#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 09:12:25 2020
Generate vegetation and irrigation parameter file based on WSDA 2018 data (GRID_CODE 	CropType	Irrigation	area_m2	fraction)

@author: liuming
"""

# this block of code copied from https://gist.github.com/ryan-hill/f90b1c68f60d12baea81 
import pandas as pd
import pysal as ps
import numpy as np

def sortkey(x): 
    return int(x)

datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/irrigation/"
vic_natural_vegparameter_file = datapath + "vic_vegetation_parameter_usca_pnw.txt"
wsda_fraction_file = "/home/liuming/Projects/WSU_BPA/CRB_Datasets/LandUseAndIrrigation/WSDA/inputs/vic_crop_irrigation_area_fraction_remove_quote.txt"

wsda_to_vic_dic = {
                 "Alfalfa Hay"                  : "7701",
                 "Alfalfa Seed"                 : "8704",
                 "Alfalfa/Grass Hay"            : "7701",
                 "Apple"                        : "1401",
                 "Apricot"                      : "1409",
                 "Asparagus"                    : "4100",
                 "Barley"                       : "4011",
                 "Barley Hay"                   : "4011",
                 "Bean Seed"                    : "4010",
                 "Bean, Dry"                    : "4010",
                 "Bean, Garbanzo"               : "4010",
                 "Bean, Green"                  : "4010",
                 "Beet Seed"                    : "4006",
                 "Berry, Unknown"               : "102",
                 "Blueberry"                    : "102",
                 "Bluegrass Seed"               : "8704",
                 "Broccoli"                     : "8807",
                 "Bromegrass Seed"              : "8504",
                 "Brussels Sprouts"             : "8808",
                 "Brussels Sprouts Seed"        : "8808",
                 "Buckwheat"                    : "7202",
                 "Cabbage"                      : "8809",
                 "Cabbage Seed"                 : "8506",
                 "Camelina"                     : "4103",
                 "Caneberry"                    : "107",
                 "Canola"                       : "4101",
                 "Cantaloupe"                   : "8002",
                 "Carrot"                       : "4102",
                 "Carrot Seed"                  : "8507",
                 "Cauliflower"                  : "8811",
                 "Cereal Grain, Unknown"        : "4013",
                 "Cherry"                       : "1403",
                 "Chestnut"                     : "1404",
                 "Cilantro Seed"                : "8525",
                 "Clover Hay"                   : "7708",
                 "Clover Seed"                  : "8704",
                 "Clover/Grass Hay"             : "7708",
                 "Corn Seed"                    : "4007",
                 "Corn, Field"                  : "4007",
                 "Corn, Sweet"                  : "4008",
                 "Corn, Unknown"                : "4007",
                 "Cranberry"                    : "103",
                 "Cucumber"                     : "8815",
                 "Currant"                      : "104",
                 "Daffodil"                     : "7502",
                 "Dahlia"                       : "4006",
                 "Dill"                         : "8901",
                 "Driving Range"                : "8205",
                 "Fescue Seed"                  : "8526",
                 "Filbert"                      : "1405",
                 "Garlic"                       : "8817",
                 "Golf Course"                  : "8205",
                 "Grape, Juice"                 : "2001",
                 "Grape, Table"                 : "2001",
                 "Grape, Unknown"               : "2002",
                 "Grape, Wine"                  : "2002",
                 "Grass Hay"                    : "8205",
                 "Grass Seed"                   : "4104",
                 "Green Manure"                 : "8205",
                 "Hay/Silage, Unknown"          : "7701",
                 "Hemp"                         : "7807",
                 "Hops"                         : "7806",
                 "Iris"                         : "4006",
                 "Kale"                         : "4006",
                 "Legume Cover"                 : "6003",
                 "Lentil"                       : "8819",
                 "Marijuana"                    : "7807",
                 "Market Crops"                 : "4100",
                 "Medicinal Herb"               : "7801",
                 "Melon, Unknown"               : "4006",
                 "Mint"                         : "7807",
                 "Mustard"                      : "8904",
                 "Mustard Seed"                 : "8904",
                 "Nectarine/Peach"              : "1407",
                 "Nursery, Caneberry"           : "4006",
                 "Nursery, Greenhouse"          : "4006",
                 "Nursery, Holly"               : "4006",
                 "Nursery, Lavender"            : "4006",
                 "Nursery, Lilac"               : "4006",
                 "Nursery, Orchard/Vineyard"    : "2504",
                 "Nursery, Ornamental"          : "4006",
                 "Nursery, Silviculture"        : "4006",
                 "Oat"                          : "7206",
                 "Oat Hay"                      : "7701",
                 "Onion"                        : "4100",
                 "Onion Seed"                   : "4100",
                 "Orchard, Unknown"             : "2505",
                 "Parsley"                      : "4006",
                 "Pasture"                      : "8205",
                 "Pea Seed"                     : "8824",
                 "Pea, Dry"                     : "8824",
                 "Pea, Green"                   : "4009",
                 "Pear"                         : "1409",
                 "Peony"                        : "4006",
                 "Pepper"                       : "8826",
                 "Plum"                         : "1410",
                 "Potato"                       : "4004",
                 "Potato Seed"                  : "4004",
                 "Pumpkin"                      : "8828",
                 "Quinoa"                       : "4006",
                 "Radish"                       : "8839",
                 "Radish Seed"                  : "8839",
                 "Rhubarb"                      : "8829",
                 "Rutabaga"                     : "8836",
                 "Rye"                          : "7207",
                 "Rye Hay"                      : "7207",
                 "Ryegrass Seed"                : "8704",
                 "Safflower Seed"               : "8518",
                 "Seed, Other"                  : "6004",
                 "Sod Farm"                     : "8205",
                 "Sorghum"                      : "7720",
                 "Soybean"                      : "8907",
                 "Spinach"                      : "4006",
                 "Spinach Seed"                 : "4006",
                 "Squash"                       : "8831",
                 "Strawberry"                   : "7106",
                 "Sudangrass"                   : "8205",
                 "Sugar Beet"                   : "8832",
                 "Sugar Beet Seed"              : "8832",
                 "Sunflower"                    : "8906",
                 "Sunflower Seed"               : "8906",
                 "Swiss Chard Seed"             : "6004",
                 "Tea"                          : "4006",
                 "Timothy"                      : "8205",
                 "Tobacco"                      : "7807",
                 "Tomato"                       : "8834",
                 "Triticale"                    : "9209",
                 "Triticale Hay"                : "9209",
                 "Tulip"                        : "4006",
                 "Unknown"                      : "6001",
                 "Vegetable, Unknown"           : "6002",
                 "Walnut"                       : "1411",
                 "Watermelon"                   : "8001",
                 "Wheat"                        : "4005",
                 "Wildlife Feed"                : "8205",
                 "Yarrow Seed"                  : "4006",
                 "Yellow Mustard"               : "7603"
                 }

irrigation_list = {
                "Big Gun"                                   : "BIG_GUN",
                "Big Gun/Center Pivot"                      : "BIG_GUN",
                "Big Gun/Drip"                              : "BIG_GUN",
                "Big Gun/Sprinkler"                         : "BIG_GUN",
                "Big Gun/Sprinkler/Wheel Line"              : "BIG_GUN",
                "Big Gun/Wheel Line"                        : "BIG_GUN",
                "Center Pivot"                              : "CENTER_PIVOT",
                "Center Pivot/Drip"                         : "CENTER_PIVOT",
                "Center Pivot/Drip/Sprinkler"               : "CENTER_PIVOT",
                "Center Pivot/None"                         : "CENTER_PIVOT",
                "Center Pivot/Rill"                         : "CENTER_PIVOT",
                "Center Pivot/Rill/Sprinkler"               : "CENTER_PIVOT",
                "Center Pivot/Rill/Wheel Line"              : "CENTER_PIVOT",
                "Center Pivot/Sprinkler"                    : "CENTER_PIVOT",
                "Center Pivot/Sprinkler/Wheel Line"         : "CENTER_PIVOT",
                "Center Pivot/Wheel Line"                   : "CENTER_PIVOT",
                "Drip"                                      : "DRIP",
                "Drip/Big Gun"                              : "DRIP",
                "Drip/Micro-Sprinkler"                      : "DRIP",
                "Drip/None"                                 : "DRIP",
                "Drip/Rill"                                 : "DRIP",
                "Drip/Sprinkler"                            : "DRIP",
                "Drip/Sprinkler/Wheel Line"                 : "DRIP",
                "Drip/Wheel Line"                           : "DRIP",
                "Flood"                                     : "FLOOD",
                "Hand"                                      : "FLOOD",
                "Hand/Rill"                                 : "FLOOD",
                "Hand/Sprinkler"                            : "FLOOD",
                "Micro-Sprinkler"                           : "SPRINKLER",
                "Rill"                                      : "RILL",
                "Rill/Sprinkler"                            : "RILL",
                "Rill/Sprinkler/Wheel Line"                 : "RILL",
                "Rill/Wheel Line"                           : "RILL",
                "Sprinkler"                                 : "SPRINKLER",
                "Sprinkler/Wheel Line"                      : "SPRINKLER",
                "Unknown"                                   : "CENTER_PIVOT",
                "Wheel Line"                                : "WHEEL_LINE"
                }

Always_irrigation = ["102","103","107","198","1401","1402","1403","1407","1409"
                     ,"1410","1411","2002","2207","2502","2505","4004","4005"
                     ,"4007","4008","4011","4100","4101","4102","6002","7106"
                     ,"7202","7206","7207","7701","7720","7801","7806","7807"
                     ,"8001","8002","8704","8802","8807","8809","8811","8815"
                     ,"8817","8820","8826","8828","8831","8832","8834","8839"
                     ,"8841","8904","9204","9205","9208"]

default_crop_irrigation_type = "CENTER_PIVOT"

default_veg_parameter = "0.1 0.1 0.75 0.6 0.5 0.3"
lai_default_missed = "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5"
croptype = '11'

regions = ['wsda']
#regions = ['us','ca']
#regions = ['us']
#read combined infomation
for region in regions:
    print(region)
    #vic_crop_fraction = datapath + region + "_vicid_crop_fraction.txt" #id,crop,fraction
    crop_sum_fraction = dict() #[grid]
    #crop_irrig_crops = dict() #[grid]
    
    crop_irrig_fraction = dict() #[grid][crop][irrigation]   including "No_irrigation"
    crop_fraction = dict()       #[grid][crop]  total fraction
    crop_dominant_irrigation_type = dict() #[grid][crop] 
    
    #read wsda information
    with open(wsda_fraction_file) as f:   #GRID_CODE	CropType	Irrigation	area_m2	fraction
        for line in f:
            if "GRID_CODE" not in line:
                a = line.rstrip().split("\t")
                if len(a) > 0:
                    grid = a[0]
                    crop = a[1]
                    irr = a[2]
                    fraction = float(a[4])
                    if int(grid) > 0 and fraction > 0.00001:
                      if crop in wsda_to_vic_dic: #crop
                          vic_crop = wsda_to_vic_dic[crop]
                          if grid not in crop_irrig_fraction:
                              crop_irrig_fraction[grid] = dict()
                          if vic_crop not in crop_irrig_fraction[grid]:
                              crop_irrig_fraction[grid][vic_crop] = dict()
                          if irr in irrigation_list:
                              irri_type = irrigation_list[irr]
                          else:
                              irri_type = "No_irrigation"
                          if vic_crop in Always_irrigation and irri_type == "No_irrigation":
                              irri_type = default_crop_irrigation_type
                          if irri_type not in crop_irrig_fraction[grid][vic_crop]:
                              crop_irrig_fraction[grid][vic_crop][irri_type] = 0.0
                          crop_irrig_fraction[grid][vic_crop][irri_type] += fraction
    print("finished reading fraction!")
    
    #rename crop if not irrigated and identify dominant irrigation type for irrigated crops
    crop_fraction = dict()       #[grid][crop]  irrigated and non_irrigated nonirrigated: 10000 + cropcode
    crop_dominant_irrigation_type = dict()       #[grid][crop]  fraction dominant irrigation type
    for grid in crop_irrig_fraction:
        for vic_crop in crop_irrig_fraction[grid]:
            if grid not in crop_fraction:
                crop_fraction[grid] = dict()
            if grid not in crop_sum_fraction:
                crop_sum_fraction[grid] = 0.0
            for irri in crop_irrig_fraction[grid][vic_crop]:
                newcropcode = vic_crop
                if irri == "No_irrigation":
                    newcropcode = str(10000 + int(vic_crop))
                else:
                    if grid not in crop_dominant_irrigation_type:
                        crop_dominant_irrigation_type[grid] = dict()
                    if vic_crop not in crop_dominant_irrigation_type[grid]:
                        crop_dominant_irrigation_type[grid][vic_crop] = list()
                    if len(crop_dominant_irrigation_type[grid][vic_crop]) == 0:
                        crop_dominant_irrigation_type[grid][vic_crop].append(irri)
                        crop_dominant_irrigation_type[grid][vic_crop].append(crop_irrig_fraction[grid][vic_crop][irri])
                    else:
                        if crop_dominant_irrigation_type[grid][vic_crop][1] < crop_irrig_fraction[grid][vic_crop][irri]:
                            crop_dominant_irrigation_type[grid][vic_crop][0] = irri
                            crop_dominant_irrigation_type[grid][vic_crop][1] = crop_irrig_fraction[grid][vic_crop][irri]
                if newcropcode not in crop_fraction[grid]:
                    crop_fraction[grid][newcropcode] = 0.0
                crop_fraction[grid][newcropcode] += crop_irrig_fraction[grid][vic_crop][irri]
                crop_sum_fraction[grid] += crop_irrig_fraction[grid][vic_crop][irri]
            
            
    
    """
    with open(vic_crop_fraction) as f:
        for line in f:
            a = line.rstrip().split(',')
            if len(a) > 1:
                if a[0] not in crop_fraction:
                    crop_fraction[a[0]] = dict()
                if a[0] not in crop_sum_fraction:
                    crop_sum_fraction[a[0]] = 0.0
                if a[1] not in crop_fraction[a[0]]:
                    crop_fraction[a[0]][a[1]] = float(a[2])
                crop_sum_fraction[a[0]] += float(a[2])
                if a[0] not in crop_irrig_crops:
                    crop_irrig_crops[a[0]] = 0
                if int(a[1]) < 10000:
                    crop_irrig_crops[a[0]] += 1
    print("Reading Done!\n")
    """
    
    #read original vegetation parameter
    #vicveg_crop_totfraction = dict() #[grid]
    vicveg_veg_totfraction = dict() #[grid]
    vicveg_veg_fraction = dict() #[grid][veg]
    vicveg_veg_lai = dict() #[grid][veg] a string with end of line, e.g. 0.501 0.560 0.656 0.802 1.025 1.295 1.273 1.010 0.718 0.534 0.492 0.481"
    vicveg_veg_parameter = dict() #[grid][veg] a string, eg. "0.1 0.1 0.75 0.6 0.5 0.3"
    with open(vic_natural_vegparameter_file) as f:
        for line in f:
            a = line.rstrip().split()
            if len(a) == 2:
                gridid = a[0]
            if len(a) == 8:   #parmeter line
                vegid = a[0]
                if gridid not in vicveg_veg_totfraction:
                    vicveg_veg_totfraction[gridid] = 0.0
                vicveg_veg_totfraction[gridid] += float(a[1])    
                if gridid not in vicveg_veg_fraction:
                    vicveg_veg_fraction[gridid] = dict()
                    vicveg_veg_parameter[gridid] = dict()
                if vegid not in vicveg_veg_fraction[gridid]:
                    vicveg_veg_fraction[gridid][vegid] = float(a[1])
                    vicveg_veg_parameter[gridid][vegid] = a[2] + " " + a[3] + " " + a[4] + " " + a[5] + " " + a[6] + " " + a[7]
            if len(a) == 12:   #LAI line
                if gridid not in vicveg_veg_lai:
                    vicveg_veg_lai[gridid] = dict()
                if vegid not in vicveg_veg_lai[gridid]:
                    vicveg_veg_lai[gridid][vegid] = line
    print("Reading natural veg parameter done!\n")
    
    #print new veg paramater file
    out_veg = datapath + region + "_veg_parameter.txt" 
    fout_veg = open(out_veg,"w")
    for grid in sorted(vicveg_veg_parameter, key=sortkey, reverse=False):
        newcropcount = 0
        newcropfraction = 0.0
        if grid in crop_sum_fraction:
            newcropcount = len(crop_fraction[grid])
            newcropfraction = crop_sum_fraction[grid]
          
        if croptype in vicveg_veg_parameter[grid]: 
            totvegcount = len(vicveg_veg_parameter[grid]) - 1 + newcropcount
            totnat_fraction = vicveg_veg_totfraction[grid] - vicveg_veg_fraction[grid][croptype]
        else:
            totvegcount = len(vicveg_veg_parameter[grid]) + newcropcount
            totnat_fraction = vicveg_veg_totfraction[grid]
            
        #adj for natural vegetation if read crop area larger then natural vegetation total
        adj = 1.0
        if newcropfraction > (1.0 - totnat_fraction):
            if totnat_fraction >= 0.00001:
                adj = (1.0 - newcropfraction) / totnat_fraction
        fout_veg.write(grid + " " + str(totvegcount) + "\n")
        for vegid in sorted(vicveg_veg_parameter[grid], key=sortkey, reverse=False):
            if vegid != croptype:
                newvegf = adj * vicveg_veg_fraction[grid][vegid]
                fout_veg.write("   " + vegid + " " + str('%.5f' % newvegf) + " " + vicveg_veg_parameter[grid][vegid] + "\n")
                fout_veg.write(vicveg_veg_lai[grid][vegid])
        if grid in crop_fraction:
            for crop in sorted(crop_fraction[grid], key=sortkey, reverse=False):
                fout_veg.write("   " + crop + " " + str('%.5f' % crop_fraction[grid][crop]) + " " + default_veg_parameter + "\n")
                if croptype in vicveg_veg_lai[grid]:
                    fout_veg.write(vicveg_veg_lai[grid][croptype])
                else:
                    fout_veg.write("      " + lai_default_missed + "\n")
    fout_veg.close()   
    print("Writing veg parameter done!\n")
    
    
    #print irrigation file
    out_irrig = datapath + region + "_irrigation.txt" #id,crop,fraction
    firrig = open(out_irrig,'w')
    for grid in sorted(crop_fraction, key=sortkey, reverse=False):
        if grid in crop_dominant_irrigation_type:
            if len(crop_dominant_irrigation_type[grid]) >= 1:
                firrig.write(grid + " " + str(len(crop_dominant_irrigation_type[grid])) + "\n")
                for crop in sorted(crop_dominant_irrigation_type[grid], key=sortkey, reverse=False):
                    #if int(crop) < 10000:
                    #    if crop in crop_dominant_irrigation_type[grid]:
                            irrtype = crop_dominant_irrigation_type[grid][crop][0]
                    #    else:
                    #        irrtype = default_crop_irrigation_type
                        #print(crop + " " + irrtype + "\n")
                            firrig.write("    "+ crop + " " + irrtype + "\n")
                        
    firrig.close()  
print('finished!')

    
    
        