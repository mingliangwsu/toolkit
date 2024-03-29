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
vegfile_name = path + "/" + 'vegparam_final2016_with_crp.txt'
outfile_name = path + "/" + 'grid_fraction_from_veg_paramater.csv'

vegfile = open(vegfile_name,'r')
outfile = open(outfile_name,'w')
count = 0
head = "gridid landuse fraction\n"
outfile.write(head)
for line in vegfile:
    a = line.split()
    #print(line)
    if (len(a) == 2):
        gridid = int(a[0])
    elif (len(a) == 8):
        outline = str(gridid) + ' ' + a[0] + ' ' + a[1] + '\n'
        outfile.write(outline)
vegfile.close()
outfile.close()