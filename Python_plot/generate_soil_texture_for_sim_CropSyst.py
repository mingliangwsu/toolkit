#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep. 30, 2020, LIU
Merge daily VIC simulation results
@author: liuming
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
import os
import math
from os import path


def read_avg_texture(fullfilename,datadict):
    datadict.clear()
    with open(fullfilename, "r") as f:
        for line in f:
            if "sand" not in line:
                a = line.rstrip().split('\t')
                if len(a) >= 4:
                    datadict[a[0]] = [float(a[1]),float(a[2]),float(a[3])];
                        
#from simpledbf import Dbf5 
#import geopandas as gpd

#vicdir = sys.argv[1]
#outfile_path = sys.argv[2]
rootdir = "/home/liuming/mnt/hydronas1/Projects/BioEarth/Datasets/gSSURGO/soils/liu_wa"
outdir = "/home/liuming/mnt/hydronas1/Projects/BioEarth/Datasets/gSSURGO/soils/liu_wa/Texture"


avg_desgnmaste_filename = "avg_horizon_mean_texture.txt"                       #designate master
avg_hzname_filename = "avg_hzname_texture_table.txt"                           #horizon name
#name\tsand\tsilt\tclay

avg_desgnmaste_dict = dict()
avg_hzname_dict = dict()

read_avg_texture(rootdir + "/" + avg_desgnmaste_filename,avg_desgnmaste_dict)
read_avg_texture(rootdir + "/" + avg_hzname_filename,avg_hzname_dict)

o_sand = 34.8
o_silt = 53.9
o_clay = 11.3
alltext = dict()
no_text_layer_list = dict()
#input
#cokey:0 	chkey:1	hzname:2	 desgnmaste:3	hzdept_r:4	hzdepb_r:5	hzthk_r:6	sandtotal1:7	 silttotal1:8	claytotal1:9	 mukey:10
#output
#thickness(meter)\tSand(%)\tClay(%)

mukey = ""
with open(rootdir + "/mapunit_hz_texture_new.txt", "r") as infile:
    for line in infile:
        if "cokey" not in line:
            a = line.rstrip().split('\t')
            if len(a) >= 10:
                mukey = a[10]
                if mukey not in alltext:
                    alltext[mukey] = list()
                    layer_index = 0
                
                out_thick = (float(a[5]) - float(a[4])) * 0.01                     #meter
                out_sand = float(a[7])
                out_clay = float(a[9])
                silt = float(a[8])
                sum_text = out_sand + out_clay + silt
                #if sum_text < 1 and (a[3] == "O" or a[2] == "H1"):
                if sum_text < 1:
                    if a[2] in avg_hzname_dict:                            #check hzname (detailed class at first)
                        out_sand = avg_hzname_dict[a[2]][0]
                        silt = avg_hzname_dict[a[2]][1]
                        out_clay = avg_hzname_dict[a[2]][2]
                        sum_text = out_sand + out_clay + silt
                    elif a[3] in avg_desgnmaste_dict:                          #check designated master average
                        out_sand = avg_desgnmaste_dict[a[3]][0]
                        silt = avg_desgnmaste_dict[a[3]][1]
                        out_clay = avg_desgnmaste_dict[a[3]][2]
                        sum_text = out_sand + out_clay + silt
                        
                if sum_text < 1 and a[3] != "R":
                    if mukey not in no_text_layer_list:
                        no_text_layer_list[mukey] = list()
                    no_text_layer_list[mukey].append(layer_index)
                if a[3] != "R":
                    outlist = [layer_index,out_thick,out_sand,out_clay, silt]
                    alltext[mukey].append(outlist)
            
                layer_index += 1

#generate outputs
for mapunit in alltext:
    valid = True
    if len(alltext[mapunit]) > 0:
        for idx,layer in enumerate(alltext[mapunit]):
            totaltext = alltext[mapunit][idx][2] + alltext[mapunit][idx][3] + alltext[mapunit][idx][4]
            if totaltext < 1:
                if mapunit in no_text_layer_list:
                    if alltext[mapunit][idx][0] not in no_text_layer_list[mapunit]:
                        valid = False
                    elif idx == 0:
                        valid = False
                else:
                    valid = False
    else:
        valid = False
   
    if valid == True:
        outfile = outdir + "/s" + mapunit + ".txt"
        with open(outfile,"w") as f:
            for idx,layer in enumerate(alltext[mapunit]):
                totaltext = alltext[mapunit][idx][2] + alltext[mapunit][idx][3] + alltext[mapunit][idx][4]
                if totaltext > 1 and idx == alltext[mapunit][idx][0]:
                    outline = str('%.2f' % alltext[mapunit][idx][1]) + "\t" + str('%.1f' % alltext[mapunit][idx][2]) + "\t" + str('%.1f' % alltext[mapunit][idx][3]) + "\n"
                    f.write(outline) 
                elif idx != alltext[mapunit][idx][0]:
                    print(mapunit + " layer:" + str(idx) + " has inconsistancy!\n")
            


print("Done\n")

