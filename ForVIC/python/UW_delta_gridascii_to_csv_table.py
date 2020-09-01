#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: liuming

Create CDL fraction for VIC grid cells
"""

import pandas as pd
import sys 
import os

"""
#Canada part

asciidir = '/mnt/hydronas/Projects/BPA_CRB/GIS/Canada_BC/lufraction_vicid'
vicidfile = asciidir + '/vicid.asc'
outfile = '/home/liuming/temp/temp/CA_Landuse.csv'
"""

if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<ID> <out> <list...>\n")
    sys.exit(0)

#PNW_Klamath
vicidfile = sys.argv[1]
outfile = sys.argv[2]

#read vicid
vicid = dict()
row = 0
enddata = dict()
with open(vicidfile) as f:
    for line in f:
        a = line.split()
        if len(a) > 2:
            vicid[row] = a
            for col in range(0,len(a)):
                if a[col] != '0' and a[col] != '-9999':
                    t = list()
                    if a[col] not in enddata:
                        enddata[a[col]] = t
            row += 1
print('read vic id done')

#data = dict()
lulist = list()
varnums = len(sys.argv)
for lu in range(3,varnums):
    filename = sys.argv[lu]
    if os.path.exists(filename):
        lulist.append(lu)
        row = 0
        #this_lu = dict()
        with open(filename) as f:
            for line in f:
                a = line.split()
                if len(a) > 2:
                    #this_lu[row] = a
                    for col in range(0,len(a)):
                        gridid = vicid[row][col]
                        if gridid in enddata:
                            enddata[gridid].append(a[col])
                    row += 1
        print(filename + ' done!')
        #data[lu] = this_lu

outfile_table = open(outfile,"w")
head = 'vicid'
for lu in range(0,len(lulist)):
    head += ',lu_' + str(lulist[lu])
outfile_table.write(head + '\n')
for cell in sorted(enddata):
    line = cell
    totalarea = 0
    for lu in range(0,len(lulist)):
        data = float(enddata[cell][lu])
        line += ',' + str(data)
    #if totalarea > 0.000001:
    outfile_table.write(line + '\n')
outfile_table.close()
print("Done!")
