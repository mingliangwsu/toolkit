#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 14:04:35 2024

@author: liuming
"""
import pandas as pd
from ExcelDataframeExchange import *
import SoilWaterEvaporation as SWE
import math

def runSoilWaterEvaporation(Cells):
    Crop_Fraction_Solar_Interception = float(get_excel_value(Cells, 'A2'))
    Residue_Fraction_Solar_Interception = float(get_excel_value(Cells, 'A3'))
    Percent_Sand = float(get_excel_value(Cells, 'A4'))
    Initial_Water_Content = float(get_excel_value(Cells, 'A5'))
    Permanent_Wilting_Point = float(get_excel_value(Cells, 'A6'))
    
    Number_Of_Days_To_Run = int(get_excel_value(Cells, 'A8'))                  #'This is a fixed number for this standalone example
    
    Air_Dry_Water_Content = Permanent_Wilting_Point / 3
    Water_Content_Top_layer = Initial_Water_Content
    Evaporation_Soil_Depth = 0.169 - 0.001 * Percent_Sand                      #meter
     
    for Day in range(1, Number_Of_Days_To_Run + 1):
        Potential_ET = float(Cells.iloc[Day+12-1, 2-1])
        Potential_Soil_Water_Evaporation,Soil_Water_Evaporation,newWater_Content_Top_layer = \
            SWE.SoilWaterEvaporation(Potential_ET,Crop_Fraction_Solar_Interception, \
                                 Residue_Fraction_Solar_Interception,Permanent_Wilting_Point, \
                                 Evaporation_Soil_Depth, Water_Content_Top_layer)
        Water_Content_Top_layer = newWater_Content_Top_layer
        Cells.iloc[Day+12-1, 3-1] = Potential_Soil_Water_Evaporation
        Cells.iloc[Day+12-1, 4-1] = Soil_Water_Evaporation
            
            
###main program            
#get file
data_path = '/home/liuming/mnt/hydronas3/Projects/CropManagement'
input_from_excel_csv = 'Final Soil Water Evaporation.csv'
output_file_name = 'Final_Soil_Water_Evaporation_output.csv'

Cells = pd.read_csv(f'{data_path}/{input_from_excel_csv}',header=None)
runSoilWaterEvaporation(Cells)
Cells.to_csv(f'{data_path}/{output_file_name}', index=False,header=None)
        
        
    