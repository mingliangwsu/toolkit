#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 09:12:25 2020
Generate vegetatioon and irrigation parameters for US and Canada based on cdl and Canada land cover data sets (regenrated from step 1)
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

crop_irrigation_type = {
    "102" : "DRIP",
    "103" : "SPRINKLER",
    "107" : "DRIP",
    "198" : "DRIP",
    "1401" : "SPRINKLER",
    "1402" : "SPRINKLER",
    "1403" : "SPRINKLER",
    "1407" : "SPRINKLER",
    "1409" : "SPRINKLER",
    "1410" : "SPRINKLER",
    "1411" : "SPRINKLER",
    "2001" : "SPRINKLER",
    "2002" : "SPRINKLER",
    "2207" : "CENTER_PIVOT",
    "2502" : "DRIP",
    "2504" : "SPRINKLER",
    "2505" : "DRIP",
    "4004" : "CENTER_PIVOT",
    "4005" : "CENTER_PIVOT",
    "4006" : "CENTER_PIVOT",
    "4007" : "CENTER_PIVOT",
    "4008" : "CENTER_PIVOT",
    "4009" : "CENTER_PIVOT",
    "4010" : "CENTER_PIVOT",
    "4011" : "BIG_GUN",
    "4100" : "CENTER_PIVOT",
    "4101" : "CENTER_PIVOT",
    "4102" : "CENTER_PIVOT",
    "7106" : "BIG_GUN",
    "7202" : "CENTER_PIVOT",
    "7206" : "RILL",
    "7207" : "CENTER_PIVOT",
    "7701" : "CENTER_PIVOT",
    "7708" : "BIG_GUN",
    "7720" : "BIG_GUN",
    "7801" : "CENTER_PIVOT",
    "7806" : "DRIP",
    "7807" : "CENTER_PIVOT",
    "8001" : "CENTER_PIVOT",
    "8002" : "SPRINKLER",
    "8205" : "FLOOD",
    "8518" : "SPRINKLER",
    "8704" : "CENTER_PIVOT",
    "8802" : "CENTER_PIVOT",
    "8804" : "RILL",
    "8807" : "BIG_GUN",
    "8809" : "BIG_GUN",
    "8811" : "BIG_GUN",
    "8815" : "BIG_GUN",
    "8817" : "CENTER_PIVOT",
    "8824" : "CENTER_PIVOT",
    "8826" : "CENTER_PIVOT",
    "8828" : "BIG_GUN",
    "8831" : "CENTER_PIVOT",
    "8832" : "CENTER_PIVOT",
    "8834" : "DRIP",
    "8839" : "CENTER_PIVOT",
    "8841" : "CENTER_PIVOT",
    "8904" : "CENTER_PIVOT",
    "8906" : "CENTER_PIVOT",
    "8907" : "CENTER_PIVOT",
    "9209" : "CENTER_PIVOT"
        }
default_crop_irrigation_type = "CENTER_PIVOT"

default_veg_parameter = "0.1 0.1 0.75 0.6 0.5 0.3"
lai_default_missed = "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5"
croptype = '11'

regions = ['us','ca']
#regions = ['us']
#read combined infomation
for region in regions:
    print(region)
    vic_crop_fraction = datapath + region + "_vicid_crop_fraction.txt" #id,crop,fraction
    crop_fraction = dict() #[grid][crop]
    crop_sum_fraction = dict() #[grid]
    crop_irrig_crops = dict() #[grid]
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
        if grid in crop_irrig_crops:
            if crop_irrig_crops[grid] >= 1:
                firrig.write(grid + " " + str(crop_irrig_crops[grid]) + "\n")
                for crop in sorted(crop_fraction[grid], key=sortkey, reverse=False):
                    if int(crop) < 10000:
                        if crop in crop_irrigation_type:
                            irrtype = crop_irrigation_type[crop]
                        else:
                            irrtype = default_crop_irrigation_type
                        #print(crop + " " + irrtype + "\n")
                        firrig.write("    "+ crop + " " + irrtype + "\n")
                        
    firrig.close()  
print('finished!')

    
    
        