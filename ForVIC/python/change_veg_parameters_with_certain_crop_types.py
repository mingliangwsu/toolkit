#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:52:40 2017
Convert VIC veg parametgers into tables with grid cell id and veg type as index
@author: liuming
"""
workdir = '/home/liuming/Projects/BPA/vic_input/Veg'
vegfile_name = 'um_vic_vegparameter.txt'
outfile_name = 'um_vic_vegparameter_for_calibration.txt'
out_croptype = '204' #corn
os.chdir(workdir)



vegfile = open(vegfile_name,'r')
outfile = open(outfile_name,'w')
count = 0
for line in vegfile:
    a = line.split()
    #print(line)
    if (len(a) == 2):
        cellid = int(a[0])
        num = int(a[1])
        count = num
        crop_fraction = 0
        out = []
    else:
        if (len(a) > 0):
            count -= 1
            
            if (int(a[0]) > 13):
                num -= 1
                crop_fraction += float(a[1])
            else:
                out.append(line)
            if (count == 0):
                if (crop_fraction > 0):
                    num += 1
                firstline = str(cellid) + ' ' + str(num) + '\n'
                outfile.write(firstline)
                for eachveg in out:
                    outfile.write(eachveg)
                if (crop_fraction > 0):
                    outcrop = '   ' + out_croptype + ' ' + str(crop_fraction)[:7] + ' 0.1 0.1 0.75 0.6 0.5 0.3\n'
                    outfile.write(outcrop)
                
vegfile.close()
outfile.close()