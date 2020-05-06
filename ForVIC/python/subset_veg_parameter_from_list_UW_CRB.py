#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:52:40 2017
Convert VIC veg parametgers into tables with grid cell id and veg type as index
@author: liuming
"""
workdir = '/home/liuming/temp/temp'
vegfile_name = 'vic_vegetation_parameter_usca.txt'
#gridid_list_filename = 'wa_viclist.txt'
gridid_list_filename = '/home/liuming/mnt/hydronas1/Projects/UW_subcontract/vegetation_parameters/crb_viclist.txt'
outfile_name = 'vic_vegetation_parameter_crb.txt'

os.chdir(workdir)

#vic_list = pd.read_csv(gridid_list_filename,sep=',',index_col=False)
allcell = dict()
with open(gridid_list_filename) as f:
    for line in f:
        a = line.split()
        if len(a) > 0:
            cellid = int(a[0])
            #print(cellid)
            if cellid not in allcell:
                allcell[cellid] = 0
                #print(str(cellid) + " added")
print("Finish reading cell.\n")

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
        if cellid in allcell:
            selected = True
            allcell[cellid] = 1
            outfile.write(line)
    else:
        if selected:
            outfile.write(line)
            
for cell in allcell:
    if (allcell[cell] == 0):
        outfile.write(str(cell) + " " + "0\n")
vegfile.close()
outfile.close()