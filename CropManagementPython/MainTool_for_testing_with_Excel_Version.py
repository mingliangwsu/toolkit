#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 6 2024

@author: liuming
"""
import pandas as pd
import WaterUptakeConfig as Soil
from ExcelDataframeExchange import *
from CropWaterUptakeClass import *
from SoilWater import *
from CropParameter import *
from SoilHydrolics import *
from Crop import *
from canopycover import *
from CS_ET import *

class CS_Weather:
    Solar_Radiation = dict()
    Tmax = dict()
    Tmin = dict()
    RHmax = dict()
    RHmin = dict()
    Wind_Speed = dict()
    Precipitation = dict()
    FAO_ETo = dict()
class CS_Fertilization:
    Fertilization_DOY = dict()
    Mineral_Fertilizer_Name = dict()
    Mineral_Fertilization_Rate = dict()
    Nitrate_Fraction = dict()
    Ammonium_Fraction = dict()
    Ammonia_Fraction = dict()
    Organic_Fertilizer_Name = dict()
    Organic_Fertilizer_Rate = dict()
    Organic_Fertilizer_C_Fraction = dict()
    Organic_Fertilizer_N_Fraction = dict()
    Application_Method_Number = dict()
    
    #and others

def ReadCropParameters(Cells,Crop,col_letter):
    Crop.Crop_Name = get_excel_value(Cells,f'{col_letter}3')
    Crop.Midseason_Crop_Coefficient = float(get_excel_value(Cells,f'{col_letter}5'))
    Crop.Maximum_Crop_Water_Uptake = float(get_excel_value(Cells,f'{col_letter}6'))
    Crop.LWP_Onset_Stomatal_Closure = float(get_excel_value(Cells,f'{col_letter}7'))
    Crop.LWP_Permanent_Wilting = float(get_excel_value(Cells,f'{col_letter}8'))
    Crop.Seeding_Depth = float(get_excel_value(Cells,f'{col_letter}9'))
    Crop.Initial_Root_Depth_From_Germinated_Seed = float(get_excel_value(Cells,f'{col_letter}10'))
    Crop.Maximum_Root_Depth = float(get_excel_value(Cells,f'{col_letter}11'))
    Crop.Maximum_Crop_Height = float(get_excel_value(Cells,f'{col_letter}12'))
    Crop.Initial_Green_Canopy_Cover = float(get_excel_value(Cells,f'{col_letter}14'))
    Crop.Maximum_Green_Canopy_Cover = float(get_excel_value(Cells,f'{col_letter}15'))
    Crop.Maturity_Green_Canopy_Cover = float(get_excel_value(Cells,f'{col_letter}16'))
    Crop.Transpiration_Use_Efficiency_1_kPa = float(get_excel_value(Cells,f'{col_letter}18'))
    Crop.Slope_Daytime_VPD_Function = float(get_excel_value(Cells,f'{col_letter}19'))
    Crop.Maximum_N_Concentration_Emergence = float(get_excel_value(Cells,f'{col_letter}21'))
    Crop.Critical_N_Concentration_Emergence = float(get_excel_value(Cells,f'{col_letter}22'))
    Crop.Minimum_N_Concentration_Emergence = float(get_excel_value(Cells,f'{col_letter}23'))
    Crop.Biomass_Start_Dilution_Maximum_N_Concentration = float(get_excel_value(Cells,f'{col_letter}24'))
    Crop.Biomass_Start_Dilution_Critical_N_Concentration = float(get_excel_value(Cells,f'{col_letter}25'))
    Crop.Biomass_Start_Dilution_Minimum_N_Concentration = float(get_excel_value(Cells,f'{col_letter}26'))
    Crop.N_Dilution_Slope = float(get_excel_value(Cells,f'{col_letter}27'))
    Crop.Maximum_N_Concentration_Maturity = float(get_excel_value(Cells,f'{col_letter}28'))
    Crop.Critical_N_Concentration_Maturity = float(get_excel_value(Cells,f'{col_letter}29'))
    Crop.Minimum_N_Concentration_Maturity = float(get_excel_value(Cells,f'{col_letter}30'))
    Crop.Potential_N_Uptake = float(get_excel_value(Cells,f'{col_letter}31'))
def ReadSoilHorizonParamegters(Cells,pSoilHorizen):
    #'Soil description
    pSoilHorizen.Number_Of_Horizons = int(get_excel_value(Cells,'A17'))
    total_horizon_depth = 0  #05192025LML
    for i in range(1, pSoilHorizen.Number_Of_Horizons+1):
        pSoilHorizen.Horizon_Thickness[i] = float(Cells.iloc[22 + i - 1, 3 - 1]) #'Thickness is rounded to one decimal
        pSoilHorizen.Clay[i] = float(Cells.iloc[22 + i - 1, 4 - 1])
        pSoilHorizen.Silt[i] = float(Cells.iloc[22 + i - 1, 5 - 1])
        pSoilHorizen.Sand[i] = float(Cells.iloc[22 + i - 1, 6 - 1])
        pSoilHorizen.FC_WC[i] = float(Cells.iloc[22 + i - 1, 7 - 1])
        pSoilHorizen.PWP_WC[i] = float(Cells.iloc[22 + i - 1, 8 - 1])
        pSoilHorizen.Soil_Organic_Carbon[i] = float(Cells.iloc[22 + i - 1, 9 - 1])
        total_horizon_depth += pSoilHorizen.Horizon_Thickness[i]
        
    depth_deficit = MAX_Number_Model_Layers * Thickness_Model_Layers - total_horizon_depth #05192025LML
    if depth_deficit < 0.: #05192025LML in case total horizon depth less than model required depth, extent the bottom horizon
       pSoilHorizen.Horizon_Thickness[pSoilHorizen.Number_Of_Horizons] += -depth_deficit
    
        
def ReadCropGrowth(Cells,pCropGrowth,row_idx):
    #'Soil description
    pCropGrowth.Crop_Name = get_excel_value(Cells,f'A{row_idx}')
    pCropGrowth.Expected_Yield = float(get_excel_value(Cells,f'H{row_idx}'))
    pCropGrowth.Planting_DOY = int(get_excel_value(Cells,f'I{row_idx}'))
    pCropGrowth.Emergence_DOY = int(get_excel_value(Cells,f'J{row_idx}'))
    pCropGrowth.Full_Canopy_DOY = int(get_excel_value(Cells,f'K{row_idx}'))
    pCropGrowth.Beging_Senescence_DOY = int(get_excel_value(Cells,f'L{row_idx}'))
    pCropGrowth.Maturity_DOY = int(get_excel_value(Cells,f'M{row_idx}'))
    pCropGrowth.Harvest_DOY = int(get_excel_value(Cells,f'N{row_idx}'))
def ReadFertilization(Cells,pCS_Fertilization):
    start_row_idx = 46 - 1
    end_row_idx = 50 - 1
    for i in range(start_row_idx, end_row_idx + 1):
        doy = int(Cells.iloc[i, 2 - 1])
        if doy > 0:
            pCS_Fertilization.Fertilization_DOY[doy] = doy
            pCS_Fertilization.Mineral_Fertilizer_Name[doy] = Cells.iloc[i, 3 - 1]
            pCS_Fertilization.Mineral_Fertilization_Rate[doy] = float(Cells.iloc[i, 4 - 1])
            pCS_Fertilization.Nitrate_Fraction[doy] = float(Cells.iloc[i, 5 - 1])
            pCS_Fertilization.Ammonium_Fraction[doy] = float(Cells.iloc[i, 6 - 1])
            pCS_Fertilization.Ammonia_Fraction[doy] = float(Cells.iloc[i, 7 - 1])
            pCS_Fertilization.Organic_Fertilizer_Name[doy] = float(Cells.iloc[i, 8 - 1])
            pCS_Fertilization.Organic_Fertilizer_Rate[doy] = float(Cells.iloc[i, 9 - 1])
            pCS_Fertilization.Organic_Fertilizer_C_Fraction[doy] = float(Cells.iloc[i, 10 - 1])
            pCS_Fertilization.Organic_Fertilizer_N_Fraction[doy] = float(Cells.iloc[i, 11 - 1])
            pCS_Fertilization.Application_Method_Number[doy] = int(Cells.iloc[i, 12 - 1])
        
def ReadNetIrrigation(Cells,Irrigation):
    start_row_idx = 58 - 1
    for i in range(1, 10):
        doy = int(Cells.iloc[start_row_idx + i - 1, 2 - 1])
        Irrigation[doy] = float(Cells.iloc[start_row_idx + i - 1, 3 - 1])      #mm
def ReadWeather(Cells,pCS_Weather):
    start_row_idx = 74 - 1
    end_row_idx = 438 - 1
    for i in range(start_row_idx, end_row_idx + 1):
        doy = int(Cells.iloc[i, 2 - 1])
        pCS_Weather.Solar_Radiation[doy] = float(Cells.iloc[i, 3 - 1])
        pCS_Weather.Tmax[doy] = float(Cells.iloc[i, 4 - 1])
        pCS_Weather.Tmin[doy] = float(Cells.iloc[i, 5 - 1])
        pCS_Weather.RHmax[doy] = float(Cells.iloc[i, 6 - 1])
        pCS_Weather.RHmin[doy] = float(Cells.iloc[i, 7 - 1])
        pCS_Weather.Wind_Speed[doy] = float(Cells.iloc[i, 8 - 1])
        pCS_Weather.Precipitation[doy] = float(Cells.iloc[i, 9 - 1])
        pCS_Weather.FAO_ETo[doy] = float(Cells.iloc[i, 10 - 1])
def ReadSoilInitial(DOY, Cells,pSoilState,pSoilModelLayer):
    InitSoilState(pSoilState)
    start_row_idx = 7 - 1
    end_row_idx = 16 - 1
    Number_Initial_Conditions_Layers = int(get_excel_value(Cells,'B3'))
    Thickness_Model_Layers = 0.1
    
    Thickness = dict()
    Number_Of_Sublayers = dict()
    Water = dict()
    Nitrate = dict()
    Ammonium = dict()
    
    for i in range(1, Number_Initial_Conditions_Layers + 1):
        Thickness[i] = float(Cells.iloc[i + 6 - 1, 2 - 1])
        Number_Of_Sublayers[i] = round(Thickness[i] / Thickness_Model_Layers)
        Water[i] = float(Cells.iloc[i + 6 - 1, 3 - 1])
        Nitrate[i] = float(Cells.iloc[i + 6 - 1, 4 - 1]) / 10000 #'Convert kg/ha to kg/m2
        Ammonium[i] = float(Cells.iloc[i + 6 - 1, 5 - 1]) / 10000 #'Convert kg/ha to kg/m2
    #'Distribute variables for each model layer of thickness 0.1 m
    Cum_J = 1
    for i in range(1, Number_Initial_Conditions_Layers + 1):
        NL = Number_Of_Sublayers[i]
        k = Cum_J
        L = (k + NL - 1)
        for j in range(k, L + 1):
            #Layer_Thickness[j] = Thickness[i] / Number_Of_Sublayers[i]
            pSoilState.Water_Content[DOY][j] = Water[i]
            pSoilState.Soil_Water_Potential[j] = WP(pSoilModelLayer.Saturation_Water_Content[j], Water[i], pSoilModelLayer.Air_Entry_Potential[j], pSoilModelLayer.B_value[j])
            pSoilState.Nitrate_N_Content[DOY][j] = Nitrate[i] / Number_Of_Sublayers[i]
            pSoilState.Ammonium_N_Content[DOY][j] = Ammonium[i] / Number_Of_Sublayers[i]
        Cum_J = L + 1
    Number_Model_Layers = Cum_J - 1
    #'Determine the thickness of the soil water evaporation layer
    #Percent_Sand = ReadInputs.PercentSand(1)
    #Thickness_Evaporative_Layer = Round(-0.001 * Percent_Sand + 0.169, 2)
    #Layer_Thickness(1) = Thickness_Evaporative_Layer
    #'Set accumulators to zero
    Cumulative_Deep_Drainage = 0
    Cumulative_N_Leaching = 0
        
        
    
#get file
data_path = '/home/liuming/mnt/hydronas3/Projects/CropManagement'
crop_from_excel_csv = 'Crop_Tool Inputs-Outputs 9-2-24 For Min.csv'
fieldinput_from_excel_csv = 'Input_Tool Inputs-Outputs 9-2-24 For Min.csv'
soil_initial_excel_csv = 'InitSoil_Tool Inputs-Outputs 9-2-24 For Min.csv'

crop_output_excel_csv = 'CropOutput.csv'
soil_output_excel_csv = 'SoilOutput.csv'

CropColums = {
    "DOY": "int32",
    "Pot Green Canopy Cover": "float64",
    "Pot crop Transpiration (mm/day)": "float64",
    "Pot Biomass (kg/ha)": "float64",
    "Green Canopy Cover": "float64",
    "Biomass (kg/ha)": "float64",
    "Transpiration (mm)": "float64",
    "Soil Evap (mm)": "float64",
    "Root Depth (m)": "float64",
    "Height (m)": "float64",
    "Max N Conc (kg/kg)": "float64",
    "Crit N Conc (kg/kg)": "float64",
    "Min N Conc (kg/kg)": "float64",
    "Crop N Conc (kg/kg)": "float64",
    "Crop N Mass (kg/ha)": "float64",
    "N Uptake (kg/ha)": "float64",
    "Water_Stress_Index": "float64",
    "Nitrogen_Stress_Index": "float64"
    }
CropOutput = pd.DataFrame({col: pd.Series(dtype=dt) for col, dt in CropColums.items()})

#output_mode_file_name = 'Water_Uptake_output_mode.csv'
#output_file_name = 'wateruptake_out.csv'

#Crop parameters
crop_paramater = CropParameter()
cropCells = pd.read_csv(f'{data_path}/{crop_from_excel_csv}',header=None)

#one specific crop
col_letter = 'J'
ReadCropParameters(cropCells,crop_paramater,col_letter)

#all crop parameters
crop_parameters = dict()
crop_parameters[crop_paramater.Crop_Name] = crop_paramater

#Soil parameters
InputCells = pd.read_csv(f'{data_path}/{fieldinput_from_excel_csv}',header=None)
SoilInitCells = pd.read_csv(f'{data_path}/{soil_initial_excel_csv}',header=None)



pSoilHorizen = SoilHorizons()
pSoilModelLayer = SoilModelLayer()
ReadSoilHorizonParamegters(InputCells,pSoilHorizen)
CalculateHydraulicProperties(pSoilHorizen.Number_Of_Horizons,pSoilHorizen,pSoilModelLayer)


#SoilOutput
SoilLayers = pSoilModelLayer.Number_Model_Layers
SoilColums = dict()
SoilColums["DOY"] = "int32"
for i in range(1,SoilLayers + 1):
    SoilColums[f'Water (m/m) L{i}'] = "float64"
    SoilColums[f'NO3-N (kg/ha) L{i}'] = "float64"
    SoilColums[f'NH4-N (kg/ha) L{i}'] = "float64"
SoilOutput = pd.DataFrame({col: pd.Series(dtype=dt) for col, dt in SoilColums.items()})

#Crop growth inputs
pCropGrowth = CropGrowth()

crop_row_index = 38
ReadCropGrowth(InputCells,pCropGrowth,crop_row_index)

CropGrowths = dict()
CropGrowths[pCropGrowth.Crop_Name] = pCropGrowth

#fertilization
pCS_Fertilization = CS_Fertilization()
ReadFertilization(InputCells,pCS_Fertilization)

#irrigation
irrigations = dict()
ReadNetIrrigation(InputCells,irrigations)
    
#Irrigation N concentration
WaterNConc = float(get_excel_value(InputCells,'D12'))

#Weather data
pCS_Weather = CS_Weather()
ReadWeather(InputCells,pCS_Weather)

#for i in range(1, pSoilHorizen.Number_Of_Horizons+1):
#    print(f'i:{i} Horizon_Thickness:{pSoilHorizen.Horizon_Thickness[i]} Clay:{pSoilHorizen.Clay[i]}') #'Thickness is rounded to one decimal
#for i in range(1, pSoilLayer.Number_Model_Layers+1):
#    print(f'i:{i} FC_Water_Content:{pSoilLayer.FC_Water_Content[i]} PWP_Water_Content:{pSoilLayer.PWP_Water_Content[i]}') #'Thickness is rounded to one decimal
    
Run_First_DOY = int(get_excel_value(InputCells,'F15'))
Crop_Active = False

crop_states = dict()

First_Crop_Name = pCropGrowth.Crop_Name
Run_Last_DOY = CropGrowths[First_Crop_Name].Harvest_DOY

crop_states[First_Crop_Name] = CropState()

first_crop_growth = CropGrowths[First_Crop_Name]
#first_crop_state = CropState()

#'Begin time loop

pCropParameter = crop_parameters[First_Crop_Name]
pCropState = crop_states[First_Crop_Name]
pCropGrowth = CropGrowths[First_Crop_Name]
pSoilState = SoilState()
pETState = ETState()

InitETState(pETState)
ReadSoilInitial(Run_First_DOY,SoilInitCells,pSoilState,pSoilModelLayer)
InitCropState(pCropState)

for DOY in range(Run_First_DOY, Run_Last_DOY+1):
    #Crop_Number = ReadInputs.CropOrder(1)
    if DOY == first_crop_growth.Emergence_DOY:
        Crop_Active = True
        #pCropParameter = crop_parameters[First_Crop_Name]
        #pCropState = crop_states[First_Crop_Name]
        #pCropGrowth = CropGrowths[First_Crop_Name]
        
        InitializeCrop(DOY,pCropState,pCropParameter,pETState)
        
        #get CC paraemters
        Shape_Coef_Before_Peak = 9
        Shape_Coef_During_Decline = 9
        Initial_Value = pCropParameter.Initial_Green_Canopy_Cover
        Peak_Value = pCropParameter.Maximum_Green_Canopy_Cover
        End_Season_Value = pCropParameter.Maturity_Green_Canopy_Cover
        Time_Fraction_At_Half_Peak_Value = 0.5
        Time_Fraction_At_Half_Decline = 0.5
        DOY_Begin_Season = pCropGrowth.Emergence_DOY
        DOY_Peak_Value = pCropGrowth.Full_Canopy_DOY
        DOY_Begin_Decline = pCropGrowth.Beging_Senescence_DOY
        DOY_End_Of_Season = pCropGrowth.Maturity_DOY
        
        #'Derived parameters for the standard green canopy curve
        B1,B2,Asympthotic_Value_max,Actual_Value_max1,Actual_Value_max2,Asymthotic_Value_Decline = \
            get_CC_parameters(Shape_Coef_Before_Peak,Shape_Coef_During_Decline,
                              Initial_Value,Peak_Value,End_Season_Value,Time_Fraction_At_Half_Peak_Value,
                              Time_Fraction_At_Half_Decline,DOY_Begin_Season,DOY_Peak_Value,
                              DOY_Begin_Decline,DOY_End_Of_Season)

        #'Set state variable for the potential crop, which grow without water and N stress
        for i in range(pCropGrowth.Emergence_DOY, pCropGrowth.Maturity_DOY + 1):
            Today_GCC_Value = GreenCanopyCover(Shape_Coef_Before_Peak,Shape_Coef_During_Decline,
                         Initial_Value,Peak_Value,End_Season_Value,DOY_Begin_Season,
                         DOY_Peak_Value,DOY_Begin_Decline,DOY_End_Of_Season,B1,B2,
                         Asympthotic_Value_max,Actual_Value_max1,Actual_Value_max2,
                         Asymthotic_Value_Decline,i)
            pCropState.Potential_Green_Canopy_Cover[i] = Today_GCC_Value #'Calculate potential green canopy cover for the entire season
            PotET(i, True, pCropState, pCropParameter, pCS_Weather, pETState)
            Biomass(i, True, pCropState, pCropParameter, pCS_Weather, pETState) #'Calculate potential biomass for the entire season
            ReferencePlantNConcentration(i, pCropState, pCropParameter, pCropGrowth)

        InitializeCrop(DOY,pCropState,pCropParameter,pETState)

    if DOY == first_crop_growth.Maturity_DOY: 
        Crop_Active = False
    if Crop_Active: 
        CanopyCover(DOY, pCropState, pCropParameter, pCropGrowth, pETState)
        GrowRoot(DOY, pCropState, pCropParameter)
        GrowHeight(DOY, pCropState, pCropParameter)

    PotET(DOY, False, pCropState, pCropParameter, pCS_Weather, pETState)
    ActEvaporation(DOY,pSoilModelLayer,pSoilState,pETState, Crop_Active)
    if Crop_Active:
        ActualTranspiration(DOY, pCropParameter, pSoilModelLayer, pCropState, pETState, pSoilState)
        Biomass(DOY, False, pCropState, pCropParameter, pCS_Weather, pETState)
        NitrogenUptake(DOY, pCropState, pCropParameter, pCropGrowth, pETState, pSoilModelLayer, pSoilState)
    
    NetIrrigationDepth = 0
    Mineral_Fertilization_Rate = 0
    Nitrate_Fraction = 0
    if DOY in irrigations:
        NetIrrigationDepth = irrigations[DOY]
    if DOY in pCS_Fertilization.Fertilization_DOY:
        Mineral_Fertilization_Rate = pCS_Fertilization.Mineral_Fertilization_Rate[DOY]
        Nitrate_Fraction = pCS_Fertilization.Nitrate_Fraction[DOY]
    WaterAndNTransport(DOY, pSoilModelLayer, pSoilState, NetIrrigationDepth, WaterNConc, \
                           pCS_Weather.Precipitation[DOY], Mineral_Fertilization_Rate, Nitrate_Fraction)

    #CropOutput
    CropOutRow = {
        "DOY": DOY,
        "Pot Green Canopy Cover": pCropState.Potential_Green_Canopy_Cover[DOY],
        "Pot crop Transpiration (mm/day)": pETState.Potential_Crop_Transpiration[DOY],
        "Pot Biomass (kg/ha)": pCropState.Potential_Crop_Biomass[DOY] * 10000, #'Convert kg/m2 to kg/ha,
        "Green Canopy Cover": pCropState.Green_Canopy_Cover[DOY],
        "Biomass (kg/ha)": pCropState.Cumulative_Crop_Biomass[DOY] * 10000, #'Convert kg/m2 to kg/ha,
        "Transpiration (mm)": pETState.Actual_Transpiration[DOY],
        "Soil Evap (mm)": pETState.Actual_Soil_Water_Evaporation[DOY],
        "Root Depth (m)": pCropState.Root_Depth[DOY],
        "Height (m)": pCropState.Crop_Height[DOY],
        "Max N Conc (kg/kg)": pCropState.Maximum_N_Concentration[DOY],
        "Crit N Conc (kg/kg)": pCropState.Critical_N_Concentration[DOY],
        "Min N Conc (kg/kg)": pCropState.Minimum_N_Concentration[DOY],
        "Crop N Conc (kg/kg)": pCropState.Crop_N_Concentration[DOY],
        "Crop N Mass (kg/ha)": pCropState.Crop_N_Mass[DOY] * 10000, #'Convert kg/m2 to kg/ha
        "N Uptake (kg/ha)": pCropState.Cumulative_N_Uptake[DOY] * 10000, #'Convert kg/m2 to kg/ha
        "Water_Stress_Index": pETState.Water_Stress_Index[DOY],
        "Nitrogen_Stress_Index": pCropState.Nitrogen_Stress_Index[DOY]
    }
    CropOutput.loc[len(CropOutput)] = CropOutRow
    #SoilOutput
    SoilOutRow = dict()
    SoilOutRow["DOY"] = DOY
    for i in range(1,SoilLayers + 1):
        SoilOutRow[f'Water (m/m) L{i}'] = pSoilState.Water_Content[DOY][i]
        SoilOutRow[f'NO3-N (kg/ha) L{i}'] = pSoilState.Nitrate_N_Content[DOY][i] * 10000 #'Convert kg/m2 to kg/ha
        SoilOutRow[f'NH4-N (kg/ha) L{i}'] = pSoilState.Ammonium_N_Content[DOY][i] * 10000 #'Convert kg/m2 to kg/ha
    SoilOutput.loc[len(SoilOutput)] = SoilOutRow
    
    

SoilOutput.to_csv(f'{data_path}/{soil_output_excel_csv}',index=False)
CropOutput.to_csv(f'{data_path}/{crop_output_excel_csv}',index=False)