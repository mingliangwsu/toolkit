#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:52:40 2017
Convert VIC veg parametgers into tables with grid cell id and veg type as index
@author: liuming
"""

#vegfile_name = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/Veg/vic_vegparamegter.txt'
#outfile_name = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/supplement_support_analysis_only/grid_veg_fraction.csv'

path = "/home/liuming/mnt/hydronas1/Projects/Forecast2016/Barik_data"
vegfile_name = path + "/" + 'crop_parameter2016_crb_final.txt'
outfile_name = path + "/" + 'grid_fraction_from_crop_paramater.csv'

vegfile = open(vegfile_name,'r')
outfile = open(outfile_name,'w')

head = "gridid landuse irrigation fraction\n"
outfile.write(head)

count = 0
for line in vegfile:
    a = line.split()
    #print(line)
    if (len(a) == 2):
        gridid = int(a[0])
    elif (len(a) == 6):
        outline = str(gridid) + ' ' + a[0] + ' ' + a[3] + ' ' + a[1] + '\n'
        outfile.write(outline)
vegfile.close()
outfile.close()