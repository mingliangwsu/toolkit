#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:48:10 2024

@author: liuming
"""
import pandas as pd
import WaterUptakeConfig as Soil
from ExcelDataframeExchange import *
from CropWaterUptakeClass import *


def CropWaterUptakeInterface(Cells,Outcells):
    #'Read evapotranspiration Parameters
    Reference_Crop_ETo = float(get_excel_value(Cells,'A4'))
    Crop_Coefficient_Full_Canopy = float(get_excel_value(Cells,'A5'))
    #'CO2_adjustment_To_Potential_Transpiration = [E4]
    Water_Intercepted_By_Canopy = float(get_excel_value(Cells,'H5'))
    
    #'Read Crop Parameters
    Crop_Max_Water_Uptake = float(get_excel_value(Cells,'A7'))                 #'Maximum crop water uptake when the canopy completely shades the soil
    LeafWP_OnsetStress = float(get_excel_value(Cells,'A8'))                    #'leaf water potential at the onset of stomatal closure (J/kg)
    LeafWP_Wilt = float(get_excel_value(Cells,'A9'))                           #'leaf water potential at wilting (zero transpiration)(J/kg)
    Green_Canopy_Cover_Max = float(get_excel_value(Cells,'A10'))               #'Green canopy cover at full canopy
    Current_green_Canopy_Cover = float(get_excel_value(Cells,'A11'))           #'Current green canopy cover
    RootDepth = float(get_excel_value(Cells,'H7'))                             #'Rooting depth (m)
    
    N_Layers = int(get_excel_value(Cells,'A14'))                             #'Number of soil layers
    
    #'Read layer thickness (m) and soil water potential per layer (J/kg)
    
    for i in range(1, N_Layers+1):
        Soil.Layer_thickness[i] = float(Cells.iloc[i + 16 - 1, 2 - 1])
        Soil.Air_Entry_Potential[i] = float(Cells.iloc[i + 16 - 1, 4 - 1])
        Soil.Soil_WP[i] = float(Cells.iloc[i + 16 - 1, 7 - 1])
        Soil.WP_At_FC[i] = float(Cells.iloc[i + 16 - 1, 8 - 1])
        Soil.WP_At_PWP[i] = float(Cells.iloc[i + 16 - 1, 9 - 1])
    
    #'Calculate actual transpiration (kg/m2/d = mm/d)
    #print(f'Nlayers:{N_Layers}')
    WaterUptake(Reference_Crop_ETo, 
                Crop_Coefficient_Full_Canopy, 
                Water_Intercepted_By_Canopy, 
                Crop_Max_Water_Uptake, 
                LeafWP_OnsetStress, 
                LeafWP_Wilt, 
                Green_Canopy_Cover_Max, 
                Current_green_Canopy_Cover, 
                RootDepth, 
                N_Layers)
    
    #'Write to the output worksheet
    set_excel_value(Outcells, 'A2', Soil.Today_Potential_Transpiration)
    set_excel_value(Outcells, 'A3', Soil.Today_Crop_Max_Water_Uptake)
    set_excel_value(Outcells, 'A4', Soil.Today_Expected_Crop_Water_Uptake)
    set_excel_value(Outcells, 'A5', Soil.Crop_Water_Uptake)
    set_excel_value(Outcells, 'A6', Soil.Act_Transp)
    set_excel_value(Outcells, 'A7', Soil.Water_Stress_Index)
    set_excel_value(Outcells, 'A25', Soil.Leaf_Water_Pot)
    set_excel_value(Outcells, 'A26', Soil.Average_Soil_WP)
    test_sum_fraction = 0
    test_sum_root_fraction = 0
    test_sum_uptake = 0
    for i in range(1, N_Layers+1):
        Outcells.iloc[11 + i - 1, 1 - 1] = i
        Outcells.iloc[11 + i - 1, 2 - 1] = Soil.Root_Fraction[i]
        Outcells.iloc[11 + i - 1, 3 - 1] = Soil.Root_Activity_Factor[i]
        Outcells.iloc[11 + i - 1, 4 - 1] = Soil.Adjusted_Root_Fraction[i]
        Outcells.iloc[11 + i - 1, 5 - 1] = Soil.Soil_WP[i]
        Outcells.iloc[11 + i - 1, 6 - 1] = Soil.Soil_Water_Uptake[i]
        test_sum_fraction += Soil.Root_Fraction[i]
        test_sum_root_fraction += Soil.Adjusted_Root_Fraction[i]
        test_sum_uptake += Soil.Soil_Water_Uptake[i]
    Outcells.iloc[11 + N_Layers + 2 - 1, 2 - 1] = test_sum_fraction
    Outcells.iloc[11 + N_Layers + 2 - 1, 4 - 1] = test_sum_root_fraction
    Outcells.iloc[11 + N_Layers + 2 - 1, 6 - 1] = test_sum_uptake
    
#get file
data_path = '/home/liuming/mnt/hydronas3/Projects/CropManagement'
input_from_excel_csv = 'FINALWaterUptake_Input.csv'
output_mode_file_name = 'Water_Uptake_output_mode.csv'
output_file_name = 'wateruptake_out.csv'

Soil.Cells = pd.read_csv(f'{data_path}/{input_from_excel_csv}',header=None)
Outcells = pd.read_csv(f'{data_path}/{output_mode_file_name}',header=None)
CropWaterUptakeInterface(Soil.Cells,Outcells)
Outcells.to_csv(f'{data_path}/{output_file_name}', index=False, header=None)