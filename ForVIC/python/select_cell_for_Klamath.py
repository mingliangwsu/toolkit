#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: liuming

Create a subset of soil parameter file from cell list
"""

import pandas as pd
import sys 
import os

#if len(sys.argv) != 4:
#    print("Usage:" + sys.argv[0] + "<original_soil_parameter_file> <cell_list> <out_new_soil_parameter_file>\n")
#    sys.exit(0)

orig_soil_parameter_file = "/mnt/hydronas/Projects/BPA_CRB/parameters/newsoil_with_soc_corrected_org_density_newUM.txt"
subset = "/mnt/hydronas/Projects/BPA_CRB/GIS/boundary/Klamath_basin_cells_big.csv"
out_selected = "/home/liuming/temp/temp/Klamath_cell_list.txt"

fout = open(out_selected,"w")

allcell = list()
with open(orig_soil_parameter_file) as f:
    for line in f:
        a = line.split()
        if len(a) > 0:
            cellid = a[1]
            if cellid not in allcell:
                allcell.append(cellid)

subset_list = dict()
#read soil parameter to create location dictionary
with open(subset) as f:
    for line in f:
        cell = line.split(',')
        if len(cell) > 0 and "GRIDID" not in cell: 
            if cell[0] not in allcell:
                fout.write(line)
fout.close()
print("Done!")
