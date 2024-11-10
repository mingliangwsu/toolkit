#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 12:52:17 2024

@author: liuming
"""
from ExcelDataframeExchange import *
import pandas as pd

class AutoIrrigationEvent:
    DOY_Event = None
    Event_Type = None
    Scheduling_Method = None #1:PAW 2:CWSI
    Maximum_Allowable_PAW_Depletion = None
    Maximum_Allowable_CWSI = None
    Refill_Depth = None #meter
    Irrigated_Crop_Number = None
    
    DOY_To_Start_Auto_Irrigation = None
    DOY_To_Stop_Auto_Irrigation = None
    DOY_For_Refill_Irrigation = None
    
class AutoIrrigationEvents:
    Number_Of_Auto_Entries = 0
    Events = dict()

def ReadAutoIrrigation(Cells,AutoIrrigation,DOY_Last_Scheduled_Irrigation,
                       Emergence_DOY_1,Maturity_DOY_1,Emergence_DOY_2,Maturity_DOY_2):
    
    start_row_idx = 56 - 1
    AutoIrrigation.Number_Of_Auto_Entries = int(get_excel_value(Cells,'F55'))
    for i in range(1, AutoIrrigation.Number_Of_Auto_Entries + 1):
        irrigation = AutoIrrigationEvent()
        irrigation.DOY_Event = int(Cells.iloc[start_row_idx + i, 6 - 1])
        irrigation.Event_Type = Cells.iloc[start_row_idx + i, 7 - 1]
        if not pd.isna(Cells.iloc[start_row_idx + i, 8 - 1]):
            irrigation.Scheduling_Method = int(Cells.iloc[start_row_idx + i, 8 - 1])
        if not pd.isna(Cells.iloc[start_row_idx + i, 9 - 1]):
            irrigation.Maximum_Allowable_PAW_Depletion = float(Cells.iloc[start_row_idx + i, 9 - 1])
        if not pd.isna(Cells.iloc[start_row_idx + i, 10 - 1]):
            irrigation.Maximum_Allowable_CWSI = float(Cells.iloc[start_row_idx + i, 10 - 1])
        if not pd.isna(Cells.iloc[start_row_idx + i, 11 - 1]):
            irrigation.Refill_Depth = float(Cells.iloc[start_row_idx + i, 11 - 1])
        if not pd.isna(Cells.iloc[start_row_idx + i, 12 - 1]):
            irrigation.Irrigated_Crop_Number = int(Cells.iloc[start_row_idx + i, 12 - 1])
            
            
        if irrigation.Event_Type == "START":
            irrigation.DOY_To_Start_Auto_Irrigation = irrigation.DOY_Event
            if irrigation.Irrigated_Crop_Number == 1:
                if (DOY_Last_Scheduled_Irrigation > Emergence_DOY_1 or DOY_Last_Scheduled_Irrigation > 1) and (DOY_Last_Scheduled_Irrigation <= Maturity_DOY_1):
                    irrigation.DOY_To_Start_Auto_Irrigation = DOY_Last_Scheduled_Irrigation + 1
            else:
                if (DOY_Last_Scheduled_Irrigation > Emergence_DOY_2) and (DOY_Last_Scheduled_Irrigation <= Maturity_DOY_2):
                    irrigation.DOY_To_Start_Auto_Irrigation = DOY_Last_Scheduled_Irrigation + 1
        elif irrigation.Event_Type == "STOP":
            irrigation.DOY_To_Stop_Auto_Irrigation = irrigation.DOY_Event 
        elif irrigation.Event_Type == "REFILL":
            irrigation.DOY_For_Refill_Irrigation = irrigation.DOY_Event 

        AutoIrrigation.Events[i] = irrigation
        


#testing...

input_file = '/home/liuming/mnt/hydronas3/Projects/CropManagement/VBCode_11022024/Field_Input.csv'
InputCells = pd.read_csv(input_file,header=None)


DOY_Last_Scheduled_Irrigation = 135
Emergence_DOY_1 = 284
Maturity_DOY_1 = 105
Emergence_DOY_2 = 135
Maturity_DOY_2 = 258

AutoIrrigation = AutoIrrigationEvents()

ReadAutoIrrigation(InputCells,AutoIrrigation,DOY_Last_Scheduled_Irrigation,
                   Emergence_DOY_1,Maturity_DOY_1,Emergence_DOY_2,Maturity_DOY_2)