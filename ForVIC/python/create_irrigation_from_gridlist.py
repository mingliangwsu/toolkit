#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get subset of soil parameter depending on a gridid list
"""

import pandas as pd
import numpy as np
import os

croptype = '4001'

workdir = '/home/liuming/Projects/BPA/vic_input/Soil'
soilparameter_file = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/Soil/soil_param_crb_id_sorted.txt'
gridid_list_filename = 'seleted_vic.csv'
out_parameter = '/home/liuming/Projects/BPA/vic_input/Management/irrigation_' + croptype + '.txt'

os.chdir(workdir)

vic_list = pd.read_csv(gridid_list_filename,sep=',',index_col=False)
#soilfile = open(soilparameter_file,'r')
outfile = open(out_parameter,'w')

for index, row in vic_list.iterrows():
    #print(row['gridid'])
    line1 = str(row['gridid']) + ' 1\n'
    outfile.write(line1)
    line2 = '    ' + croptype + ' DEFAULT_CENTER_PIVOT\n'
    outfile.write(line2)
    
outfile.close()
print('finished!')
