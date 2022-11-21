#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu April 5, 2022
Convert veg parametgers csv table to VIC format vegetation file
@author: Mingliang Liu
"""

import pandas as pd
import sys 
import os

def sortkey(x): 
    return int(x)

if len(sys.argv) < 3:
    print("Usage:" + sys.argv[0] + "<veg_fraction_table> <output_VIC_veg_file>\n")
    sys.exit(0)
    
fraction_file = sys.argv[1]  #GRIDID,numofclass,LC_class,frac,rd1,rd2,rd3,rf1,rf2,rf3,Jan,Feb,Mar,Apr,May,Jun,Jul, Aug,Sep,Oct,Nov,Dec
out_file = sys.argv[2]

default_parameter = "0.1 0.1 0.75 0.6 0.5 0.3"

fractions = dict()

outfile = open(out_file,"w")
with open(fraction_file) as f:
    for line in f:
        if "GRIDID" not in line:
            a = line.rstrip().split(',')
            if len(a) > 1:
                tot_fractions = 0
                total_veg_num = 0
                gridid = a[0]
                veg = a[2]
                #f = a[3]
                if gridid not in fractions:
                    fractions[gridid] = dict()
                if veg not in fractions[gridid]:
                    fractions[gridid][veg] = list()
                    for i in range(19):
                        fractions[gridid][veg].append(a[3 + i])
with open(out_file,"w") as f:
    for gridid in sorted(fractions, key=sortkey, reverse=False):
        line = gridid + " " + str(len(fractions[gridid])) + "\n"
        f.write(line)
        for veg in sorted(fractions[gridid], key=sortkey, reverse=False):
            line = "   " + veg + " " + str('%.6f' % float(fractions[gridid][veg][0])) + " "
            if float(fractions[gridid][veg][1]) > 0:
                line += str('%.2f' % float(fractions[gridid][veg][1])) + " " \
                        + str('%.2f' % float(fractions[gridid][veg][2])) + " " + str('%.2f' % float(fractions[gridid][veg][3])) + " " \
                        + str('%.2f' % float(fractions[gridid][veg][4])) + " " + str('%.2f' % float(fractions[gridid][veg][5])) + " " \
                        + str('%.2f' % float(fractions[gridid][veg][6])) + "\n"
            else:
                line += default_parameter + "\n"
            f.write(line)
            line = "      "
            for mon in range(12):
                line += str('%.2f' % float(fractions[gridid][veg][6 + mon])) + " "
            line += "\n"
            f.write(line)       
      
            
print("Done!")
