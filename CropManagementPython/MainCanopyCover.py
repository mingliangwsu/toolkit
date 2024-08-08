#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 08:22:45 2024

@author: liuming
"""
import pandas as pd
from canopycover import *
from ExcelDataframeExchange import *
import math

def runGreenCanopyCover(Cells):
    Shape_Coef_Before_Peak = 9
    Shape_Coef_During_Decline = 9
    Initial_Value = float(get_excel_value(Cells, 'A4')) #[A4]
    Peak_Value = float(get_excel_value(Cells, 'A5')) #[A5]
    End_Season_Value = float(get_excel_value(Cells, 'A6')) #[A6]
    Time_Fraction_At_Half_Peak_Value = float(get_excel_value(Cells, 'A7')) #[A7]
    Time_Fraction_At_Half_Decline = float(get_excel_value(Cells, 'A8')) #[A8]
    DOY_Begin_Season = int(get_excel_value(Cells, 'A9')) #[A9]
    DOY_Peak_Value = int(get_excel_value(Cells, 'A10')) #[A10]
    DOY_Begin_Decline = int(get_excel_value(Cells, 'A11')) #[A11]
    DOY_End_Of_Season = int(get_excel_value(Cells, 'A12')) #[A12]

    #'Derived parameters for the standard green canopy curve
    B1,B2,Asympthotic_Value_max,Actual_Value_max1,Actual_Value_max2,Asymthotic_Value_Decline = \
        get_CC_parameters(Shape_Coef_Before_Peak,Shape_Coef_During_Decline,
                          Initial_Value,Peak_Value,End_Season_Value,Time_Fraction_At_Half_Peak_Value,
                          Time_Fraction_At_Half_Decline,DOY_Begin_Season,DOY_Peak_Value,
                          DOY_Begin_Decline,DOY_End_Of_Season)
    Row_Counter = 19 #'First row for output
    for DOY in range(DOY_Begin_Season, DOY_End_Of_Season + 1):
        Today_GCC_Value = GreenCanopyCover(Shape_Coef_Before_Peak,Shape_Coef_During_Decline,
                     Initial_Value,Peak_Value,End_Season_Value,DOY_Begin_Season,
                     DOY_Peak_Value,DOY_Begin_Decline,DOY_End_Of_Season,B1,B2,
                     Asympthotic_Value_max,Actual_Value_max1,Actual_Value_max2,
                     Asymthotic_Value_Decline,DOY)
        Cells.iloc[Row_Counter-1, 1-1] = DOY 
        Cells.iloc[Row_Counter-1, 2-1] = Today_GCC_Value 
        Row_Counter += 1
        #print(f'{DOY},{Today_GCC_Value}')


###main program            
#get file
data_path = '/home/liuming/mnt/hydronas3/Projects/CropManagement'
input_from_excel_csv = 'FINAL Canopy Cover Using Calendar Time.csv'
output_file_name = 'FINAL Canopy Cover Using Calendar Time_output.csv'

Cells = pd.read_csv(f'{data_path}/{input_from_excel_csv}',header=None)
runGreenCanopyCover(Cells)
Cells.to_csv(f'{data_path}/{output_file_name}', index=False,header=None)

