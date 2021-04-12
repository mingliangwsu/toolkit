#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
join crop
@author: liuming
"""

#vegfile_name = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/Veg/vic_vegparamegter.txt'
#outfile_name = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/supplement_support_analysis_only/grid_veg_fraction.csv'

path = "/home/liuming/mnt/hydronas1/Projects/Forecast2016/Barik_data"

cropirrig_name = path + "/" + 'grid_fraction_from_crop_paramater.csv'
#head = "gridid landuse irrigation fraction\n"
vegcrop_name = path + "/" + 'grid_fraction_from_veg_paramater.csv'
#head = "gridid landuse fraction\n"

outfile_name = path + "/" + 'grid_fraction_cropirrigation_vegarea.csv'

outfile = open(outfile_name,'w')
head = "gridid landuse irrigation frac_cropp frac_vegp\n"
outfile.write(head)

cropveg = dict()
vegfraction = dict()
with open(cropirrig_name,'r') as fc:
    for line in fc:
        a = line.rstrip().split()
        if (len(a) > 0) and 'gridid' not in a:
            if a[0] not in cropveg:
                cropveg[a[0]] = dict()
            if a[1] not in cropveg[a[0]]:
                cropveg[a[0]][a[1]] = [a[2],a[3]]
                
with open(vegcrop_name,'r') as fc:
    for line in fc:
        a = line.rstrip().split()
        if (len(a) > 0) and 'gridid' not in a:
            if a[0] not in vegfraction:
                vegfraction[a[0]] = dict()
            if a[1] not in vegfraction[a[0]]:
                vegfraction[a[0]][a[1]] = a[2]
                
for grid in cropveg:
    for landuse in cropveg[grid]:
        outline = grid + ' ' + landuse + ' ' + cropveg[grid][landuse][0] + ' ' + cropveg[grid][landuse][1]
        if grid in vegfraction:
            if landuse in vegfraction[grid]:
                outline += ' ' + vegfraction[grid][landuse]
            else: 
                outline += ' 0.0'
        else:
            outline += ' 0.0'
        outline += '\n'
        outfile.write(outline)
        
outfile.close()
print('Done!\n')