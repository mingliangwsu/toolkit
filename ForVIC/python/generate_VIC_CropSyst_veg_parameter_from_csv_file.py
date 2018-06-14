#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu June 13, LIU
Convert VIC veg parametgers into tables with grid cell id and veg type as index
@author: liuming
"""

import pandas as pd
import sys 
import os

outdir = "/home/liuming/Projects/BPA/Kirti_cropmix_irrigation"
fraction_file = "CropMixLiu.txt"
out_file = "Umatila_veg_parameter.txt"


os.chdir(outdir)

fraction_list = ["cdl_1_corn", "cdl_12_sweetcorn", "cdl_14_mint", "cdl_21_barley", "cdl_23_spwheat", "cdl_24_winwheat", "cdl_31_canola", 
                 "cdl_36_alfalfa", "cdl_38_camlina", "cdl_42_drybeans", "cdl_43_potato", "cdl_49_onion", "cdl_53_peas", "cdl_66_cherries", 
                 "cdl_68_apples", "cdl_206_carrots", "cdl_37_otherhay", "cdl_59_seedsodgrass","genericcropfraction", 
                 "cdl_141", "cdl_142", "cdl_143", "cdl_152", "cdl_176", "cdl_190", "cdl_195"]

cdl_to_vic_dic = {"cdl_1_corn" : "4007", 
                  "cdl_12_sweetcorn" : "4008", 
                  "cdl_14_mint" : "", 
                  "cdl_21_barley", 
                  "cdl_23_spwheat", 
                  "cdl_24_winwheat", 
                  "cdl_31_canola", 
                  "cdl_36_alfalfa", 
                  "cdl_38_camlina", 
                  "cdl_42_drybeans", 
                  "cdl_43_potato", 
                  "cdl_49_onion", 
                  "cdl_53_peas", 
                  "cdl_66_cherries", 
                  "cdl_68_apples", 
                  "cdl_206_carrots", 
                  "cdl_37_otherhay", 
                  "cdl_59_seedsodgrass,
                  "genericcropfraction", 
                  "cdl_141", 
                  "cdl_142", 
                  "cdl_143", 
                  "cdl_152", 
                  "cdl_176", 
                  "cdl_190", 
                  "cdl_195"}

with open(crop_parameter_file_name) as f:



#veg_list = [102,103,104,106,107,198,201,202,204,205,206,207,209,210,211,218,298,401,402,403,501,502,503,504,505,506,601,602,603,702,703,704,705,708,713,720,721,722,798,801,802,804,806,807,898,1001,1002,1098,1202,1205,1303,1304,1306,1307,1308,1309,1311,1312,1401,1402,1403,1404,1405,1407,1409,1410,1411,1498,1501,1502,1503,1504,1506,1507,1509,1510,1512,1513,1514,1516,1517,1518,1519,1520,1521,1522,1523,1525,1526,1527,1531,1532,1598,1701,1702,1704,1801,1802,1803,1804,1807,1808,1809,1810,1811,1813,1814,1815,1816,1817,1819,1820,1821,1822,1824,1825,1826,1827,1828,1829,1830,1831,1832,1834,1835,1836,1839,1840,1898,1901,1902,1903,1904,1905,1906,1907,2001,2002,2098,2104,2203,2204,2205,2206,2207,2208,3001,3002,3003,4001,4002,5701]
veg_list = [3001,3002,3003,4001,4002]


for veg in veg_list:
    vegfile_name = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/Veg/veg_parameter_grain_crops.txt'
    vegfile = open(vegfile_name,'r')
    #outfile_name = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/supplement_support_analysis_only/vic_grid_veg_fraction/list_grid_fraction_veg_' + str(veg) + '.txt' 
    outfile_name = '/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/supplement_support_analysis_only/vic_grain_crop_fraction/list_grid_fraction_veg_' + str(veg) + '.txt' 
    outfile = open(outfile_name,'w')
    for line in vegfile:
        a = line.split()
        if (len(a) == 2):
            gridid = int(a[0])
        else:
            if (int(a[0]) == veg):
                outline = str(gridid) + ' ' + str(a[1]) + '\n'
                outfile.write(outline)
    vegfile.close()
    outfile.close()
print('finished!')