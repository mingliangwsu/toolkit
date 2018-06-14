#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:52:40 2017
Convert VIC veg parametgers into tables with grid cell id and veg type as index
@author: liuming
"""
workdir = '/home/liuming/Projects/BPA/vic_input/Veg'
vegfile_name = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/Veg/cleaned_veg_parameter.txt'
gridid_list_filename = '/home/liuming/Projects/BPA/vic_input/Soil/umvicid.csv'
outfile_name = 'um_vic_vegparameter.txt'

os.chdir(workdir)

vic_list = pd.read_csv(gridid_list_filename,sep=',',index_col=False)


vegfile = open(vegfile_name,'r')
outfile = open(outfile_name,'w')
count = 0
selected = False

for line in vegfile:
    a = line.split()
    #print(line)
    if (len(a) == 2):
        selected = False
        cellid = int(a[0])
        if any(vic_list.gridid == int(cellid)):
            selected = True
            outfile.write(line)
    else:
        if selected:
            outfile.write(line)
vegfile.close()
outfile.close()