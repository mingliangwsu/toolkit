#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:52:40 2017
Convert VIC veg parametgers into tables with grid cell id and veg type as index
@author: liuming
"""

vegfile_name = '/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Database/Veg/Kirti_cropmix_irrigation/Umatila_irrigation_parameter_180807.txt'
outfile_name = '/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Database/Veg/Kirti_cropmix_irrigation/vic_grid_irrigation_list.asc'
vegfile = open(vegfile_name,'r')
outfile = open(outfile_name,'w')
count = 0
outfile.write("cell_id crop irrigation_type\n")
for line in vegfile:
    a = line.split()
    #print(line)
    if (len(a) == 2):
        if a[1].isdigit():
            gridid = int(a[0])
        else:
            outline = str(gridid) + ' ' + line
            outfile.write(outline)
vegfile.close()
outfile.close()