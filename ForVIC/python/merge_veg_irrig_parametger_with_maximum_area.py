#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:52:40 2017
Convert VIC veg parametgers into tables with grid cell id and veg type as index
@author: liuming
"""
workdir = '/home/liuming/Projects/WSU_BPA/CRB_Datasets/LandUseAndIrrigation/UpperCRB/outputs'
vegfile_name_1 = 'veg_parameter_ca.txt'
vegfile_name_2 = 'veg_parameter_usa.txt'
outfile_name_veg = 'veg_parameter_merg.txt'
outfile_name_irrig = 'irrigation_parameter_merg.txt'

celllist = "/home/liuming/Projects/WSU_BPA/CRB_Datasets/LandUseAndIrrigation/UpperCRB/inputs/viclist.txt"

os.chdir(workdir)

cropdic1 = dict()
cropdic2 = dict()
selected = dict()

#get cell list
allcell = list()
with open(cell_list) as f:
    for line in f:
        a = line.split()
        if len(a) > 0:
            cellid = int(a[0])
            if cellid not in allcell:
                allcell.append(cellid)
print("Finish reading cell.\n")



outfile_veg = open(outfile_name_veg,'w')
outfile_irrig = open(outfile_name_irrig,'w')

with open(vegfile_name_1) as f:
    for line in f:
        a = line.split()
        #print(line)
        if (len(a) == 2):
            cellid = int(a[0])
            num = int(a[1])
            crop_fraction = 0
        else:
            if (len(a) > 0):
                if (len(a) == 8):
                    num -= 1
                    crop_fraction += float(a[1])
                if (num == 0):
                    cropdic1[cellid] = crop_fraction

with open(vegfile_name_2) as f:
    for line in f:
        a = line.split()
        #print(line)
        if (len(a) == 2):
            cellid = int(a[0])
            num = int(a[1])
            crop_fraction = 0
        else:
            if (len(a) > 0):
                if (len(a) == 8):
                    num -= 1
                    crop_fraction += float(a[1])
                if (num == 0):
                    cropdic2[cellid] = crop_fraction

for grid in cropdic1:
    if grid in cropdic2:
        if cropdic1[grid] >= cropdic2[grid]:
            selected[grid] = 1
        else:
            selected[grid] = 2
    else:
        selected[grid] = 1
        
for grid in cropdic2:
    if grid in cropdic1:
        if cropdic1[grid] >= cropdic2[grid]:
            if grid not in selected:
               selected[grid] = 1
        else:
            if grid not in selected:
              selected[grid] = 2
    else:
        if grid not in selected:
            selected[grid] = 2

with open(vegfile_name_1) as f:
    for line in f:
        a = line.split()
        #print(line)
        if (len(a) == 2):
            bselected = 0
            cellid = int(a[0])
            num = int(a[1])
            crop_fraction = 0
            if cellid in selected:
                if selected[cellid] == 1:
                    bselected = 1
                    outfile_veg.write(line)
                    outfile_irrig.write(line)
        else:
            if bselected:
                if (len(a) == 8): 
                    veg = int(a[0])
                    out = "    " + str(veg) + " IrrigTP_Sub_surf_drip_perfect\n"
                    outfile_irrig.write(out)
                outfile_veg.write(line)
            
                
with open(vegfile_name_2) as f:
    for line in f:
        a = line.split()
        #print(line)
        if (len(a) == 2):
            bselected = 0
            cellid = int(a[0])
            num = int(a[1])
            crop_fraction = 0
            if cellid in selected:
                if selected[cellid] == 2:
                    bselected = 1
                    outfile_veg.write(line)
                    outfile_irrig.write(line)
        else:
            if bselected:
                if (len(a) == 8): 
                    veg = int(a[0])
                    out = "    " + str(veg) + " IrrigTP_Sub_surf_drip_perfect\n"
                    outfile_irrig.write(out)
                outfile_veg.write(line)

for cell in allcell:
    if cell not in selected:
        line = str(cell) + " 0\n"
        outfile_veg.write(line)

outfile_veg.close()
outfile_irrig.close()