#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:16:19 2024

@author: liuming
"""
import pandas as pd
import MethodSoilProcesses as Method
from ExcelDataframeExchange import *
import SoilConfig
def RunSoilTransport():
    #Dim Chem_Conc_In As Single 'Chemical concentration in irrigation water (kg/kg)
    #Dim Water_Content As Single 'Temporary output, can be deleted
    #Dim Chemical_Mass As Single 'Temporary output, can be deleted
    #'Initialize soil profile.  This should be done only once!
    Method.InitializeSoilProfile(SoilConfig.Cells)
    #'Specify Scenario
    #'Specify infiltration flux in mm/day = kg/m2/day
    Water_Flux_In = float(get_excel_value(SoilConfig.Cells,'A9'))
    if Water_Flux_In is None:
        Water_Flux_In = 0.0
    #'Specify chemical concentration in irrigation water (kg/kg)
    Chem_Conc_In = float(get_excel_value(SoilConfig.Cells,'A10'))
    #'Specify number of pulses. If zero, the number of pulses is optimized automatically
    Number_Of_Pulses = int(get_excel_value(SoilConfig.Cells,'A14'))
    Number_Of_Irrigations = int(get_excel_value(SoilConfig.Cells,'J2'))
    #'Set drainage flux to zero
    Sum_Drainage_Flux = 0
    Sum_Leaching = 0
    Sum_Chemical_Balance = 0
    Sum_Water_Balance = 0
    for i in range(1, Number_Of_Irrigations+1):
        Water_Flux_In = float(SoilConfig.Cells.iloc[i + 3 - 1,10 - 1])
        Method.RunCascade(SoilConfig.Number_Of_Layers, Water_Flux_In, Chem_Conc_In, 
                           Number_Of_Pulses)
        Sum_Drainage_Flux += SoilConfig.Drainage
        Sum_Leaching += SoilConfig.Chemical_Leaching * 10000
        Sum_Chemical_Balance += SoilConfig.Chemical_Balance
        Sum_Water_Balance += SoilConfig.Water_Balance
    #'Write output
    Method.set_excel_value(SoilConfig.Cells,'A19', Sum_Drainage_Flux)
    Method.set_excel_value(SoilConfig.Cells,'A20', Sum_Leaching)
    Method.set_excel_value(SoilConfig.Cells,'A21', Sum_Chemical_Balance)
    Method.set_excel_value(SoilConfig.Cells,'A22', Sum_Water_Balance)
    Sum_DZ = 0
    for i in range(1, SoilConfig.Number_Of_Layers+1):
        Sum_DZ += SoilConfig.DZ[i]
        SoilConfig.Cells.iloc[i + 25 - 1, 1 - 1] = Sum_DZ
        SoilConfig.Cells.iloc[i + 25 - 1, 2 - 1] = SoilConfig.WC[i]
        SoilConfig.Cells.iloc[i + 25 - 1, 3 - 1] = SoilConfig.Chem_Mass[i] * 10000
        
#get file
data_path = '/home/liuming/mnt/hydronas3/Projects/CropManagement'
input_from_excel_csv = 'FINAL_Simple_Water_Solute_Transport_Model.csv'
output_file_name = 'soil_process_out.csv'

SoilConfig.Cells = pd.read_csv(f'{data_path}/{input_from_excel_csv}',header=None)
RunSoilTransport()
SoilConfig.Cells.to_csv(f'{data_path}/{output_file_name}', index=False)
