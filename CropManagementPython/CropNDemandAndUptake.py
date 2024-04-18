#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:44:15 2024

@author: liuming
"""
import pandas as pd
import math
from CropWaterUptakeClass import *
from ExcelDataframeExchange import *
import WaterUptakeConfig as Soil

def CropNDemand(Cells):
    #'Initialize soil and layer N mass
    Number_Of_Layers = 10 #'Soil layering will be setup elsewhere
    Layer_Thickness = 0.1 #'m    Soil layering will be setup elsewhere
    Soil.Layer_Bottom_Depth[0] = 0
    Root_Depth_Max = float(get_excel_value(Cells,'A17'))
    Root_Elongation_Ended = False
    for Layer in range(1, Number_Of_Layers+1):
        Soil.Layer_Bottom_Depth[Layer] = (Soil.Layer_Bottom_Depth[Layer - 1] 
                                          + Layer_Thickness)
        Soil.Soil_N_Mass[Layer] = float(Cells.iloc[22 - 1, Layer + 13 - 1]) / 10000 #'Convert kg/ha to kg/m2
    #'Read input parameters
    N_Critical_Concentration_At_Emergence = float(get_excel_value(Cells,'A3'))
    N_Maximum_Concentration_At_Emergence = float(get_excel_value(Cells,'A4'))
    N_Minimum_Concentration_At_Emergence = float(get_excel_value(Cells,'A5'))
    Biomass_To_Start_Dilution_Maximum_N_Concentration = float(get_excel_value(Cells,'A6'))
    Biomass_To_Start_Dilution_Critical_N_Concentration = float(get_excel_value(Cells,'A7'))
    Biomass_To_Start_Dilution_Minimum_N_Concentration = float(get_excel_value(Cells,'A8'))
    Slope = float(get_excel_value(Cells,'A9'))
    Maximum_N_Concentration_At_Maturity = float(get_excel_value(Cells,'A10'))
    Critical_N_Concentration_At_Maturity = float(get_excel_value(Cells,'A11'))
    Minimum_N_Concentration_At_Maturity = float(get_excel_value(Cells,'A12'))
    Maximum_Daily_N_Uptake = float(get_excel_value(Cells,'A13')) / 10000 # 'Convert kg/ha/day to kg/m2/day
    for i in range(1, 3+1):
        if float(Cells.iloc[i + 13 - 1, 9 - 1]) > 0:
            Soil.Nitrogen_Application_DAE[i] = float(Cells.iloc[i + 13 - 1, 
                                                                8 - 1])
            Soil.Nitrogen_Application_Amount[i] = float(Cells.iloc[i + 13 - 1, 
                                                                   9 - 1])
    Green_Canopy_Cover_Max = float(get_excel_value(Cells,'A18'))
    Season_Length = int(get_excel_value(Cells,'A19'))
    
    #'Start processing
    Amax = (N_Maximum_Concentration_At_Emergence 
             / pow(Biomass_To_Start_Dilution_Maximum_N_Concentration, Slope))
    Acrit = (N_Critical_Concentration_At_Emergence 
              / pow(Biomass_To_Start_Dilution_Critical_N_Concentration, Slope))
    Amin = (N_Minimum_Concentration_At_Emergence 
             / pow(Biomass_To_Start_Dilution_Minimum_N_Concentration, Slope))
     
    Maximum_Green_Canopy_Cover_Reached = False
    Today_Potential_N_Uptake = 0.0
    Cumulative_N_Uptake = 0.0
    Green_Canopy_Cover = 0.0
    Root_Depth_Yesterday = 0.0
    for DAE in range(1, Season_Length+1):  #'DAE = Days after emergence
        Green_Canopy_Cover_Yesterday = Green_Canopy_Cover
        Green_Canopy_Cover = float(Cells.iloc[DAE + 24 - 1, 2 - 1])
        Daily_Top_Biomass = float(Cells.iloc[DAE + 24 - 1, 6 - 1])
        Cumulative_Top_Biomass = float(Cells.iloc[DAE + 24 - 1, 7 - 1])
        if ((Green_Canopy_Cover_Yesterday >= Green_Canopy_Cover) and 
                Maximum_Green_Canopy_Cover_Reached == False): #'This is used to approximate the end of the vegetative period
            Maximum_Green_Canopy_Cover_Reached = True
            DAE_Of_Transition = DAE
            Maximum_N_Concentration_At_Transition = Maximum_N_Concentration
            Critical_N_Concentration_At_Transition = Critical_N_Concentration
            Minimum_N_Concentration_At_Transition = Minimum_N_Concentration
            Daily_Change_Maximum_N_Concentration = ((Maximum_N_Concentration 
                    - Maximum_N_Concentration_At_Maturity) / (152 - DAE))
            Daily_Change_Critical_N_Concentration = ((Critical_N_Concentration 
                    - Critical_N_Concentration_At_Maturity) / (152 - DAE))
            Daily_Change_Minimum_N_Concentration = ((Minimum_N_Concentration 
                    - Minimum_N_Concentration_At_Maturity) / (152 - DAE))
        if not Maximum_Green_Canopy_Cover_Reached:
            Maximum_N_Concentration = min(N_Maximum_Concentration_At_Emergence, 
                                          Amax 
                                          * pow(Cumulative_Top_Biomass, Slope))
            Critical_N_Concentration = (
                min(N_Critical_Concentration_At_Emergence, Acrit 
                    * pow(Cumulative_Top_Biomass, Slope)))
            Minimum_N_Concentration = min(N_Minimum_Concentration_At_Emergence, 
                                          Amin 
                                          * pow(Cumulative_Top_Biomass, Slope))
        else:
            Maximum_N_Concentration = (Maximum_N_Concentration_At_Transition 
                                       - Daily_Change_Maximum_N_Concentration 
                                       * (DAE - DAE_Of_Transition))
            Critical_N_Concentration = (Critical_N_Concentration_At_Transition 
                                        - Daily_Change_Critical_N_Concentration 
                                        * (DAE - DAE_Of_Transition))
            Minimum_N_Concentration = (Minimum_N_Concentration_At_Transition 
                                       - Daily_Change_Minimum_N_Concentration 
                                       * (DAE - DAE_Of_Transition))
        Cells.iloc[DAE + 24 - 1, 8 - 1] = Maximum_N_Concentration
        Cells.iloc[DAE + 24 - 1, 9 - 1] = Critical_N_Concentration
        Cells.iloc[DAE + 24 - 1, 10 - 1] = Minimum_N_Concentration
        #'Calculate daily crop N uptake
        #'Check for nitrogen fertilization. Only 3 fertilization events implemented in this code. This will be setup elesewhere
        for Fertilization_Number in range(1, 3+1):
            if Soil.Nitrogen_Application_DAE[Fertilization_Number] == DAE:
                Napp = Soil.Nitrogen_Application_Amount[Fertilization_Number]
                Soil.Soil_N_Mass[1] += Napp / (3 * 10000) #'Convert kg/ha to kg/m2 and apply 1/3 to each of the top 3 layers
                Soil.Soil_N_Mass[2] += Napp / (3 * 10000) #'Convert kg/ha to kg/m2 and apply 1/3 to each of the top 3 layers
                Soil.Soil_N_Mass[3] += Napp / (3 * 10000) #'Convert kg/ha to kg/m2 and apply 1/3 to each of the top 3 layers
        for Layer in range(1, Number_Of_Layers+1):
            if not Root_Elongation_Ended: 
                Root_Depth = (Root_Depth_Max 
                              * Green_Canopy_Cover 
                              / Green_Canopy_Cover_Max)
            if ((Root_Depth < Root_Depth_Yesterday) 
                    and (Root_Elongation_Ended == False)):
                Root_Elongation_Ended = True
                Root_Depth = Root_Depth_Max
            Soil.Root_Fraction[Layer] = CalculateRootFraction(
                    Soil.Layer_Bottom_Depth[Layer], 
                    Layer_Thickness, 
                    Root_Depth)
            Root_Depth_Yesterday = Root_Depth
            Cells.iloc[DAE + 24 - 1, 13 - 1] = Root_Depth
            Cells.iloc[DAE + 24 - 1, Layer + 13 - 1] = Soil.Root_Fraction[Layer]
            Bulk_Density = 1300.0 #'kg/m3 CAREFUL: This must be implemented elsewhere for each soil layer and hookep up to soil hydraulic properties
            N_Conc_ppm = ((Soil.Soil_N_Mass[Layer] * 1000000) 
                          / (Layer_Thickness * Bulk_Density)) #'Convert kgN/m2 to mgN/kgSoil
            Soil_N_Conc_ppm_Where_N_Uptake_Decreases = 4.0 #'ppm
            Residual_N_Conc_ppm = 2.0
            N_Availability_Coefficient = NAvailabilityFactor(
                    Soil_N_Conc_ppm_Where_N_Uptake_Decreases, 
                    Residual_N_Conc_ppm)
            if N_Conc_ppm > Residual_N_Conc_ppm:
                N_Availability_Adjustment = (1.0 - math.exp(
                    -(N_Conc_ppm - Residual_N_Conc_ppm) 
                    * N_Availability_Coefficient))
            else:
                N_Availability_Adjustment = 0.0

            Water_Availability_Adjustment = 1.0 #'- Exp(-Water_Availability_Coefficient * Plant_Available_Water) 'CAREFUL: TO BE IMPLEMENTED LATER. FOR NOW ASSUME THAT WATER IS NOT LIMITING
            Soil.Potential_N_Uptake[Layer] = (Maximum_Daily_N_Uptake 
                                         * Soil.Root_Fraction[Layer] 
                                         * Water_Availability_Adjustment 
                                         * N_Availability_Adjustment)  #'kg/m2
            if Soil.Potential_N_Uptake[Layer] > Soil.Soil_N_Mass[Layer]:
                Soil.Potential_N_Uptake[Layer] = Soil.Soil_N_Mass[Layer]
            Today_Potential_N_Uptake += Soil.Potential_N_Uptake[Layer]
        #Next Layer
        if DAE == 1:
            Crop_N_Mass = (Daily_Top_Biomass / 10.0) * Maximum_N_Concentration #'initialize crop N mass. Biomass is converted from Mg/ha to kg/m2
        Surplus = max(0.0, Crop_N_Mass - Maximum_N_Concentration 
                      * (Cumulative_Top_Biomass / 10.0)) #'Convert biomass from Mg/ha to kg/m2
        Today_Crop_N_Demand = max(0.0, (Cumulative_Top_Biomass / 10.0) 
                      * Maximum_N_Concentration - Crop_N_Mass - Surplus)  #'Convert biomass from Mg/ha to kg/m2
        Today_Expected_N_Uptake = min(Today_Crop_N_Demand, 
                                      Today_Potential_N_Uptake)
        #'Calculate actual N uptake and update soil layer N mass
        Today_N_Uptake = 0.0
        for Layer in range(1, Number_Of_Layers+1):
            Soil.Layer_N_Uptake[Layer] = min(Soil.Potential_N_Uptake[Layer], 
                                        Today_Expected_N_Uptake 
                                        * Soil.Root_Fraction[Layer])
            Today_N_Uptake += Soil.Layer_N_Uptake[Layer]
            Soil.Soil_N_Mass[Layer] -= Soil.Layer_N_Uptake[Layer]
        
        Cumulative_N_Uptake += Today_N_Uptake
        Crop_N_Mass += Today_N_Uptake
        Crop_N_Concentration = Crop_N_Mass / (Cumulative_Top_Biomass / 10.0)  #'kgN/kgBiomass, but convert biomass from Mg/ha to kg/m2
    
        Cells.iloc[DAE + 24 - 1, 24 - 1] = Today_N_Uptake * 10000 #'Convert kg/m2 to kg/ha
        Cells.iloc[DAE + 24 - 1, 25 - 1] = Cumulative_N_Uptake * 10000 #'Convert kg/m2 to kg/ha
        Cells.iloc[DAE + 24 - 1, 11 - 1] = Crop_N_Concentration #'kg/kg

    
def WaterAvailabilityFactor(PAW_Where_N_Upake_Rate_Decreases):
    #'The constants for water_availability_coef were derived from a fitted power trend.
    return 5.259 * pow(PAW_Where_N_Upake_Rate_Decreases, -1.0246)

def NAvailabilityFactor(Soil_N_Conc_ppm_Where_N_Uptake_Decreases, 
                        Residual_N_Not_Available_For_Uptake):
    #'The constants for N_availability_adj were derived from a fitted power trend.
    N_Conc_Where_N_Uptake_Decreases_Minus_Residual_N = (
        Soil_N_Conc_ppm_Where_N_Uptake_Decreases 
        - Residual_N_Not_Available_For_Uptake)
    NAF = 0.0
    if N_Conc_Where_N_Uptake_Decreases_Minus_Residual_N > 0.00001:
        NAF = (4.9259 
            * pow(N_Conc_Where_N_Uptake_Decreases_Minus_Residual_N, -0.9821))
    else:
        NAF = 0
    return NAF

#get file
data_path = '/home/liuming/mnt/hydronas3/Projects/CropManagement'
input_from_excel_csv = 'FINALCropNDemandandUptake4-17-2024.csv'
output_file_name = 'Ndemand_out.csv'

Soil.Cells = pd.read_csv(f'{data_path}/{input_from_excel_csv}',header=None)
CropNDemand(Soil.Cells)
Soil.Cells.to_csv(f'{data_path}/{output_file_name}', index=False, header=None)