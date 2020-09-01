#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:52:40 2017
Convert VIC veg parametgers into tables with grid cell id and veg type as index
@author: liuming
"""

import os

def sortkey(x): 
    return int(x)


#workdir = '/home/liuming/Projects/WSU_BPA/CRB_Datasets/LandUseAndIrrigation/entire_CRB/outputs'
workdir = '/home/liuming/temp/temp'
#vegfile_name_1 = '/home/liuming/Projects/WSU_BPA/CRB_Datasets/LandUseAndIrrigation/US_except_WA/outputs/veg_parameter_usa.txt'
#vegfile_name_2 = '/home/liuming/Projects/WSU_BPA/CRB_Datasets/LandUseAndIrrigation/WSDA/outputs/veg_parameter_usa.txt'

vegfile_name_1 = 'vic_vegetation_parameter_ca.txt'
vegfile_name_2 = 'vic_vegetation_parameter_us.txt'
outfile_name_veg = 'vic_vegetation_parameter_usca.txt'
#outfile_name_irrig = 'irrigation_parameter_merg_191123.txt'

#celllist = "/home/liuming/Projects/WSU_BPA/CRB_Datasets/LandUseAndIrrigation/entire_CRB/inputs/viclist.txt"

os.chdir(workdir)

cropdic1 = dict()
cropdic2 = dict()
selected = dict()

output_dic = dict()


default_irrig_parameter = "IrrigTP_Sub_surf_drip_perfect"
default_irrig_parameter_for_vineyard = "IrrigTP_Sub_surf_drip_perfect_eliminate_top"

vinecrops = ["2001","2002","2098", "2504"]

#get cell list
#allcell = list()
#with open(celllist) as f:
#    for line in f:
#        a = line.split()
#        if len(a) > 0:
#            cellid = int(a[0])
#            #print(cellid)
#            if cellid not in allcell:
#                allcell.append(cellid)
#                #print(str(cellid) + " added")
#print("Finish reading cell.\n")



outfile_veg = open(outfile_name_veg,'w')
#outfile_irrig = open(outfile_name_irrig,'w')

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
                    #outfile_veg.write(line)
                    if cellid not in output_dic:
                        output_dic[cellid] = dict()
                    #outfile_irrig.write(line)
        else:
            if bselected:
                if (len(a) == 8): 
                    veg = int(a[0])
                    if str(veg) in vinecrops:
                        out = "    " + str(veg) + " " + default_irrig_parameter_for_vineyard + "\n"
                    else:
                        out = "    " + str(veg) + " " + default_irrig_parameter + "\n"
                    if veg not in output_dic[cellid]:
                        output_dic[cellid][veg] = ''
                    #outfile_irrig.write(out)
                #outfile_veg.write(line)
                output_dic[cellid][veg] += line
            
                
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
                    #outfile_veg.write(line)
                    if cellid not in output_dic:
                        output_dic[cellid] = dict()
                    #outfile_irrig.write(line)
        else:
            if bselected:
                if (len(a) == 8): 
                    veg = int(a[0])
                    if str(veg) in vinecrops:
                        out = "    " + str(veg) + " " + default_irrig_parameter_for_vineyard + "\n"
                    else:
                        out = "    " + str(veg) + " " + default_irrig_parameter + "\n"
                    if veg not in output_dic[cellid]:
                        output_dic[cellid][veg] = ''
                    #outfile_irrig.write(out)
                #outfile_veg.write(line)
                output_dic[cellid][veg] += line

#for cell in allcell:
#    if cell not in selected:
#        line = str(cell) + " 0\n"
#        outfile_veg.write(line)

for cellid in sorted(output_dic, key=sortkey, reverse=False):
    out = str(cellid) + " " + str(len(output_dic[cellid])) + "\n"
    outfile_veg.write(out)
    for veg in sorted(output_dic[cellid], key=sortkey, reverse=False):
        outfile_veg.write(output_dic[cellid][veg])

outfile_veg.close()
#outfile_irrig.close()
print("Done.\n")