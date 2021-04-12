#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
join crop
@author: liuming
"""

#vegfile_name = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/Veg/vic_vegparamegter.txt'
#outfile_name = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/supplement_support_analysis_only/grid_veg_fraction.csv'

#path = "/home/liuming/mnt/hydronas1/Projects/Forecast2016/Barik_data"
path = "/home/liuming/mnt/hydronas1/Projects/Forecast2016/Liu_forecast2021"

cropirrig_name = path + "/" + 'pnw_irrigation_state_reclassified.txt'
#head = "gridid landuse irrigation fraction\n"
vegcrop_name = path + "/" + 'pnw_veg_parameter_filledzero_state_reclassified.txt'
#head = "gridid landuse fraction\n"

outfile_name = path + "/" + 'grid_fraction_cropirrigation_vegarea_liuforcast2021landuse.txt'

outfile = open(outfile_name,'w')
head = "gridid landuse irrigation frac_vegp\n"
outfile.write(head)

cropveg = dict() #[gridid][crop] irrigation type
vegfraction = dict() #[gridid][crop] fraction
with open(cropirrig_name,'r') as fc:
    for line in fc:
        a = line.rstrip().split()
        if (len(a) > 0):
            if a[1].isnumeric():
                gridid = a[0]
                if gridid not in cropveg:
                    cropveg[gridid] = dict()
            else:
                cropveg[gridid][a[0]] = a[1]
                
with open(vegcrop_name,'r') as fc:
    for line in fc:
        a = line.rstrip().split()
        if (len(a) == 2):
            gridid = a[0]
            if gridid not in vegfraction:
                vegfraction[gridid] = dict()
        elif (len(a) == 8):
            if a[0] not in vegfraction[gridid]:
                vegfraction[gridid][a[0]] = a[1]
                
for grid in cropveg:
    for landuse in cropveg[grid]:
        outline = grid + ' ' + landuse + ' ' + cropveg[grid][landuse] + ' ' + vegfraction[grid][landuse]
        outline += '\n'
        outfile.write(outline)
        
outfile.close()
print('Done!\n')