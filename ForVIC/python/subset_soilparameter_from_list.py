#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get subset of soil parameter depending on a gridid list
"""

import pandas as pd
import numpy as np
import os


workdir = '/home/liuming/Projects/BPA/vic_input/Soil'
soilparameter_file = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/Soil/newsoil_with_soc.txt'
gridid_list_filename = 'umvicid.csv'
out_soil_parameter = 'um_for_calibration.txt'

os.chdir(workdir)

vic_list = pd.read_csv(gridid_list_filename,sep=',',index_col=False)
soilfile = open(soilparameter_file,'r')
outfile = open(out_soil_parameter,'w')

for line in soilfile:
        a = line.split()
        cellid = a[1]
        print(cellid)
        if any(vic_list.gridid == int(cellid)):
            outfile.write(line)
soilfile.close()
outfile.close()
print('finished!')
