#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get subset of soil parameter depending on a gridid list
"""

import pandas as pd
import numpy as np
import os


workdir = '/home/liuming/Projects/BPA/vic_input/Soil'
soilparameter_file = '/home/liuming/Projects/BPA/vic_input/Soil/Umatilla_bigdomain_soil.txt'
out_parameter = '/home/liuming/Projects/BPA/vic_input/Weather/file_list.txt'

os.chdir(workdir)

soilfile = open(soilparameter_file,'r')
outfile = open(out_parameter,'w')

for line in soilfile:
        a = line.split()
        outline = 'data_' + a[2] + '_' + a[3] + '\n'
        outfile.write(outline)
soilfile.close()
outfile.close()
print('finished!')
