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

#USA CDL
#asciidir = '/mnt/hydronas/Projects/BPA_CRB/GIS/CDL2017/lufraction_vicid'
#vicidfile = asciidir + '/vicid.asc'
#outfile = '/home/liuming/temp/temp/USCDL_Landuse.csv'

#Klamath
#asciidir = '/mnt/hydronas/Projects/BPA_CRB/GIS/CDL2017_Klamath/lufraction_vicid'
#vicidfile = asciidir + '/vicid.asc'
#outfile = '/home/liuming/temp/temp/Klamath_Landuse.csv'

#PNW_Klamath
asciidir = '/mnt/hydronas/Projects/BPA_CRB/GIS/CDL_2017_pnwkla/ascii'
vicidfile = '/mnt/hydronas/Projects/BPA_CRB/GIS/CDL_2017_pnwkla' + '/vicid.asc'
outfile = '/home/liuming/temp/temp/PNWKlamath_Landuse.csv'


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
for lu in range(0,300):
    filename = asciidir + '/cdl' + str(lu) + '.asc'
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
        line += ',' + enddata[cell][lu]
        totalarea += float(enddata[cell][lu])
    if totalarea > 0.000001:
        outfile_table.write(line + '\n')
outfile_table.close()
print("Done!")
