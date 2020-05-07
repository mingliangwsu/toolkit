#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 09:12:25 2020

@author: liuming
"""

# this block of code copied from https://gist.github.com/ryan-hill/f90b1c68f60d12baea81 
import pandas as pd
import pysal as ps
import numpy as np

def sortkey(x): 
    return int(x)

datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/irrigation/"
veg_file = datapath + "pnw_veg_parameter_filledzero.txt"
veglib_file = datapath + "veglib_20200506.txt"
outlist_file = datapath + "allveglist.txt"
outveglib_file = datapath + "veglib_20200506_ext.txt"

veglist = list()
veglib = dict()

with open(veg_file) as f:
    for line in f:
        a = line.rstrip().split()
        if len(a) == 8:
            if a[0] not in veglist:
                veglist.append(a[0])
fout = open(outlist_file,"w")
veglist.sort(key = int)

fout_veglib = open(outveglib_file,"w")

#veglib file
with open(veglib_file) as f:
    for line in f:
        a = line.rstrip().split('\t')
        if "COMMENT" not in a:
            if a[0] not in veglib:
                veglib[a[0]] = a
        else:
            fout_veglib.write(line)
fout = open(outlist_file,"w")

for crop in veglist:
    if crop in veglib:
        index = 0
        for col in veglib[crop]:
            if index > 0:
                fout_veglib.write('\t')
            fout_veglib.write(col)
            index += 1
        fout_veglib.write('\n')
    else:
        if int(crop) > 10000:
            scrop = str(int(crop) - 10000)
            if scrop in veglib:
                index = 0
                for col in veglib[scrop]:
                    if index == 0:
                        fout_veglib.write(crop)
                    else:
                        fout_veglib.write('\t' + col)
                    index += 1
                fout_veglib.write('\n')
            else:
                fout.write(crop + "\n")
        else:
            fout.write(crop + "\n")


fout.close()
fout_veglib.close()
print('Done.\n')

    
    
        