#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: liuming

Create a subset of soil parameter file from cell list
"""

import pandas as pd
import sys 
import os

def sortkey(x): 
    return int(x)

if len(sys.argv) != 6:
    print("Usage:" + sys.argv[0] + "<original_soil_parameter_file> <CAlist> <USlist> <CA_outfile> <US_outfile>\n")
    sys.exit(0)

orig_soil_parameter_file = sys.argv[1]
CA_list_file = sys.argv[2]
US_list_file = sys.argv[3]
CA_out = sys.argv[4]
US_out = sys.argv[5]

CA = list()
#read soil parameter to create location dictionary
with open(CA_list_file) as f:
    for line in f:
        cell = line.split()
        if len(cell) > 0:
            CA.append(cell[0])
            #print(location + ':' + cellid)
print("reading CA done!")

US = list()
#read soil parameter to create location dictionary
with open(US_list_file) as f:
    for line in f:
        cell = line.split()
        if len(cell) > 0:
            US.append(cell[0])
            #print(location + ':' + cellid)
print("reading US done!")

US_soil = dict()
CA_soil = dict() 

with open(orig_soil_parameter_file) as f:
    for line in f:
        a = line.split()
        if len(a) > 0:
            cellid = a[1]
            if cellid in CA:
                CA_soil[cellid] = line
            elif cellid in US:
                US_soil[cellid] = line
print("reading soil done!")

if len(US_soil) > 0:
    outfile_soil = open(US_out,"w")
    for cell in sorted(US_soil, key=sortkey, reverse=False):
        outfile_soil.write(US_soil[cell])
    outfile_soil.close()

if len(CA_soil) > 0:
    outfile_soil = open(CA_out,"w")
    for cell in sorted(CA_soil, key=sortkey, reverse=False):
        outfile_soil.write(CA_soil[cell])
    outfile_soil.close()
print("Done!")
