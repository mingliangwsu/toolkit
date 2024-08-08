#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:37:40 2024

@author: liuming
"""
from BiomassGrowth import *

import pandas as pd
from ExcelDataframeExchange import *
import math

def runBiomassGrowth(Cells):
    First_Simulation_DOY = int(get_excel_value(Cells, 'A3'))
    Last_Simulation_DOY = int(get_excel_value(Cells, 'A4'))
    Transpiration_Use_Efficiency_At_1kpa = float(get_excel_value(Cells, 'A5')) #'TUE
    TUE_Slope = float(get_excel_value(Cells, 'A6'))

    i = 1
    for DOY in range(First_Simulation_DOY, Last_Simulation_DOY + 1):
        Maximum_Temperature = float(Cells.iloc[i + 11 - 1, 2 - 1])
        Minimum_Relative_Humidity = float(Cells.iloc[i + 11 - 1, 3 - 1])
        Crop_Transpiration = float(Cells.iloc[i + 11 - 1, 4 - 1])
        Daytime_VPD = max(0.5, 0.7 * 0.6108 * math.exp(17.27 * Maximum_Temperature / (Maximum_Temperature + 237.3)) * (1 - Minimum_Relative_Humidity / 100))
        Daily_Transpiration_Use_Efficiency = Transpiration_Use_Efficiency_At_1kpa / math.pow(Daytime_VPD, TUE_Slope)
        Biomass_Gain = Crop_Transpiration * Daily_Transpiration_Use_Efficiency
        Cells.iloc[i + 11 - 1, 5 - 1] = Biomass_Gain
        i += 1


###main program            
#get file
data_path = '/home/liuming/mnt/hydronas3/Projects/CropManagement'
input_from_excel_csv = 'Final Biomass Growth Model.csv'
output_file_name = 'Final Biomass Growth Model_output.csv'

Cells = pd.read_csv(f'{data_path}/{input_from_excel_csv}',header=None)
runBiomassGrowth(Cells)
Cells.to_csv(f'{data_path}/{output_file_name}', index=False,header=None)