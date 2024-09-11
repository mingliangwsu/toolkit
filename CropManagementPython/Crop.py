#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 15:38:03 2024

@author: liuming
"""
import math

def InitializeCrop(DOY,pCropState, pCropParameter, pETState):
    pCropState.Green_Canopy_Cover[DOY] = pCropParameter.Initial_Green_Canopy_Cover
    pCropState.Total_Canopy_Cover[DOY] = pCropParameter.Initial_Green_Canopy_Cover
    Depth_Of_Seed = pCropParameter.Seeding_Depth
    Root_Depth_At_Emergence = Depth_Of_Seed + pCropParameter.Initial_Root_Depth_From_Germinated_Seed
    pCropState.Root_Depth[DOY] = Root_Depth_At_Emergence
    pCropState.Cumulative_Crop_Biomass[DOY] = 0
    pCropState.Crop_N_Mass[DOY] = 0
    pETState.Water_Stress_Index[DOY] = 0

def Biomass(DOY, Potential, pCropState, pCropParameter, pCS_Weather, pETState):
    Transpiration_Use_Efficiency_At_1kpa = pCropParameter.Transpiration_Use_Efficiency_1_kPa
    TUE_Slope = pCropParameter.Slope_Daytime_VPD_Function
    
    Maximum_Temperature = pCS_Weather.Tmax[DOY]
    Minimum_Relative_Humidity = pCS_Weather.RHmin[DOY]
    
    if Potential:
        Crop_Transpiration = pETState.Potential_Crop_Transpiration[DOY]
    else:
        Crop_Transpiration = pETState.Actual_Transpiration[DOY]

    
    Daytime_VPD = max(0.5, 0.7 * 0.6108 * math.exp(17.27 * Maximum_Temperature / (Maximum_Temperature + 237.3)) * (1 - Minimum_Relative_Humidity / 100))
    Daily_Transpiration_Use_Efficiency = Transpiration_Use_Efficiency_At_1kpa / math.pow(Daytime_VPD, TUE_Slope)
    Biomass_Gain = Crop_Transpiration * Daily_Transpiration_Use_Efficiency #'kg biomass per m2 ground area
    
    if Potential:
        pCropState.Potential_Crop_Biomass[DOY] = pCropState.Potential_Crop_Biomass[DOY - 1] + Biomass_Gain
    else:
        pCropState.Today_Biomass_Gain[DOY] = Biomass_Gain
        pCropState.Cumulative_Crop_Biomass[DOY] = pCropState.Cumulative_Crop_Biomass[DOY - 1] + Biomass_Gain

def ReferencePlantNConcentration(DOY, pCropState, pCropParameter, pCropGrowth):
    #'Read input parameters
    N_Critical_Concentration_At_Emergence = pCropParameter.Critical_N_Concentration_Emergence
    N_Maximum_Concentration_At_Emergence = pCropParameter.Maximum_N_Concentration_Emergence
    N_Minimum_Concentration_At_Emergence = pCropParameter.Minimum_N_Concentration_Emergence
    Biomass_To_Start_Dilution_Maximum_N_Concentration = pCropParameter.Biomass_Start_Dilution_Maximum_N_Concentration
    Biomass_To_Start_Dilution_Critical_N_Concentration = pCropParameter.Biomass_Start_Dilution_Critical_N_Concentration
    Biomass_To_Start_Dilution_Minimum_N_Concentration = pCropParameter.Biomass_Start_Dilution_Minimum_N_Concentration
    Slope = pCropParameter.N_Dilution_Slope
    Maximum_N_Concentration_At_Maturity = pCropParameter.Maximum_N_Concentration_Maturity
    Critical_N_Concentration_At_Maturity = pCropParameter.Critical_N_Concentration_Maturity
    Minimum_N_Concentration_At_Maturity = pCropParameter.Minimum_N_Concentration_Maturity
    DOY_Begin_Decline = pCropGrowth.Beging_Senescence_DOY
    #'Start processing
    Amax = N_Maximum_Concentration_At_Emergence / math.pow(Biomass_To_Start_Dilution_Maximum_N_Concentration, Slope)
    Acrit = N_Critical_Concentration_At_Emergence / math.pow(Biomass_To_Start_Dilution_Critical_N_Concentration, Slope)
    Amin = N_Minimum_Concentration_At_Emergence / math.pow(Biomass_To_Start_Dilution_Minimum_N_Concentration, Slope)
    
    DOY_Season_End = pCropGrowth.Maturity_DOY
    Cumulative_Top_Biomass = pCropState.Potential_Crop_Biomass[DOY] * 10  #'Convert kg/m2 to Mg/ha
    if DOY <= DOY_Begin_Decline and Cumulative_Top_Biomass > 0:
        tBiomass = math.pow(Cumulative_Top_Biomass, Slope)
        pCropState.Maximum_N_Concentration[DOY] = min(N_Maximum_Concentration_At_Emergence, Amax * tBiomass)
        pCropState.Critical_N_Concentration[DOY] = min(N_Critical_Concentration_At_Emergence, Acrit * tBiomass)
        pCropState.Minimum_N_Concentration[DOY] = min(N_Minimum_Concentration_At_Emergence, Amin * tBiomass)
        if DOY == DOY_Begin_Decline:
            pCropState.Maximum_Green_Canopy_Cover_Reached = True
            pCropState.DOY_Of_Transition = DOY
            pCropState.Maximum_N_Concentration_At_Transition = pCropState.Maximum_N_Concentration[DOY]
            pCropState.Critical_N_Concentration_At_Transition = pCropState.Critical_N_Concentration[DOY]
            pCropState.Minimum_N_Concentration_At_Transition = pCropState.Minimum_N_Concentration[DOY]
            pCropState.Daily_Change_Maximum_N_Concentration = (pCropState.Maximum_N_Concentration_At_Transition - Maximum_N_Concentration_At_Maturity) / (DOY_Season_End - DOY)
            pCropState.Daily_Change_Critical_N_Concentration = (pCropState.Critical_N_Concentration_At_Transition - Critical_N_Concentration_At_Maturity) / (DOY_Season_End - DOY)
            pCropState.Daily_Change_Minimum_N_Concentration = (pCropState.Minimum_N_Concentration_At_Transition - Minimum_N_Concentration_At_Maturity) / (DOY_Season_End - DOY)
    else:
        pCropState.Maximum_N_Concentration[DOY] = pCropState.Maximum_N_Concentration_At_Transition - pCropState.Daily_Change_Maximum_N_Concentration * (DOY - pCropState.DOY_Of_Transition)
        pCropState.Critical_N_Concentration[DOY] = pCropState.Critical_N_Concentration_At_Transition - pCropState.Daily_Change_Critical_N_Concentration * (DOY - pCropState.DOY_Of_Transition)
        pCropState.Minimum_N_Concentration[DOY] = pCropState.Minimum_N_Concentration_At_Transition - pCropState.Daily_Change_Minimum_N_Concentration * (DOY - pCropState.DOY_Of_Transition)

def CanopyCover(DOY, pCropState, pCropParameter, pCropGrowth, pETState):
    DOY_Begin_Decline = pCropGrowth.Beging_Senescence_DOY
    WSF = 1 - pETState.Water_Stress_Index[DOY - 1]
    NSF = 1 - pCropState.Nitrogen_Stress_Index[DOY - 1]
    Canopy_Expansion = (pCropState.Potential_Green_Canopy_Cover[DOY] - pCropState.Potential_Green_Canopy_Cover[DOY - 1]) * min(WSF, NSF)
    pCropState.Green_Canopy_Cover[DOY] = pCropState.Green_Canopy_Cover[DOY - 1] + Canopy_Expansion
    pCropState.Total_Canopy_Cover[DOY] = pCropState.Green_Canopy_Cover[DOY]
    #GCC_Transition = pCropState.Green_Canopy_Cover[DOY]
    #'Senescence
    if DOY >= DOY_Begin_Decline: 
        Canopy_Senescence = (pCropState.Potential_Green_Canopy_Cover[DOY - 1] - pCropState.Potential_Green_Canopy_Cover[DOY])
        pCropState.Green_Canopy_Cover[DOY] = max(0, pCropState.Green_Canopy_Cover[DOY - 1] - Canopy_Senescence)
        pCropState.Total_Canopy_Cover[DOY] = pCropState.Total_Canopy_Cover[DOY - 1]
        
def GrowRoot(DOY, pCropState, pCropParameter): #'OJO OJO Calculate root fraction here
    RD_Max = pCropParameter.Maximum_Root_Depth
    GCC_Max = pCropParameter.Maximum_Green_Canopy_Cover
    GCC_Ini = pCropParameter.Initial_Green_Canopy_Cover
    Root_Depth_At_Emergence = pCropParameter.Seeding_Depth + pCropParameter.Initial_Root_Depth_From_Germinated_Seed
    Rd = Root_Depth_At_Emergence + (RD_Max - Root_Depth_At_Emergence) * (pCropState.Total_Canopy_Cover[DOY] - GCC_Ini) / (GCC_Max - GCC_Ini)
    pCropState.Root_Depth[DOY] = Rd

def GrowHeight(DOY, pCropState, pCropParameter):
    CH_Max = pCropParameter.Maximum_Crop_Height
    GCC_Max = pCropParameter.Maximum_Green_Canopy_Cover
    GCC_Ini = pCropParameter.Initial_Green_Canopy_Cover
    CH = CH_Max * (pCropState.Total_Canopy_Cover[DOY] - GCC_Ini) / (GCC_Max - GCC_Ini)
    pCropState.Crop_Height[DOY] = CH
    
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

def WaterAvailabilityFactor(PAW_Where_N_Upake_Rate_Decreases):
    #'The constants for water_availability_coef were derived from a fitted power trend.
    return 5.259 * pow(PAW_Where_N_Upake_Rate_Decreases, -1.0246)

def NitrogenUptake(DOY, pCropState, pCropParameter, pCropGrowth, pETState, pSoilModelLayer, pSoilState):
    Potential_N_Uptake = dict()
    Root_Fraction = dict()
    Soil_N_Mass = dict()
    Soil_NO3_Mass = dict()
    Soil_NH4_Mass = dict()
    Nitrate_Mass_Fraction = dict()
    Ammonium_Mass_Fraction = dict()
    Layer_N_Uptake = dict()
    
    Crop_N = pCropState.Crop_N_Mass[DOY]
    Maximum_Daily_N_Uptake = pCropParameter.Potential_N_Uptake / 10000  # 'Convert kg/ha/day to kg/m2/day
    Cumulative_Top_Biomass = pCropState.Cumulative_Crop_Biomass[DOY] * 10  #'Convert kg/m2 to Mg/ha
    #'Calculate daily crop N uptake
    Number_Of_Layers = pSoilModelLayer.Number_Model_Layers
    Today_Potential_N_Uptake = 0.0
    for layer in range(1, Number_Of_Layers + 1):
        Root_Fraction[layer] = pETState.Root_Fraction[layer]
        Soil_NO3_Mass[layer] = pSoilState.Nitrate_N_Content[DOY][layer]
        Soil_NH4_Mass[layer] = pSoilState.Ammonium_N_Content[DOY][layer]
        if Soil_NO3_Mass[layer] == 0 and Soil_NH4_Mass[layer] == 0:
            Nitrate_Mass_Fraction[layer] = 0
            Ammonium_Mass_Fraction[layer] = 0
        else:
            Nitrate_Mass_Fraction[layer] = Soil_NO3_Mass[layer] / (Soil_NO3_Mass[layer] + Soil_NH4_Mass[layer])
            Ammonium_Mass_Fraction[layer] = 1 - Nitrate_Mass_Fraction[layer]
        
        Soil_N_Mass[layer] = Soil_NO3_Mass[layer] + Soil_NH4_Mass[layer] #'Implement priority for ammonium uptake
        Bulk_Density = pSoilModelLayer.Bulk_Density[layer]  #'kg/m3 CAREFUL: This must be implemented elsewhere for each soil layer and hookep up to soil hydraulic properties
        Layer_Thickness = pSoilModelLayer.Layer_Thickness[layer]
        N_Conc_ppm = (Soil_N_Mass[layer] * 1000000.0) / (Layer_Thickness * Bulk_Density) #'Convert kgN/m2 to mgN/kgSoil
        #'With better information, unlikely, these two could become crop parameters
        Soil_N_Conc_ppm_Where_N_Uptake_Decreases = 4 #'ppm
        Residual_N_Conc_ppm = 2 #'ppm
        #'Calculate N and water dajustments to N uptake
        N_Availability_Coefficient = NAvailabilityFactor(Soil_N_Conc_ppm_Where_N_Uptake_Decreases, Residual_N_Conc_ppm)
        if N_Conc_ppm > Residual_N_Conc_ppm:
            N_Availability_Adjustment = (1.0 - math.exp(-(N_Conc_ppm - Residual_N_Conc_ppm) * N_Availability_Coefficient))
        else:
            N_Availability_Adjustment = 0
        
        Plant_Available_Water = pSoilModelLayer.Plant_Available_Water_Content[layer]
        PAW_Where_N_Uptake_Rate_Decreases = 0.5
        Water_Availability_Coefficient = WaterAvailabilityFactor(PAW_Where_N_Uptake_Rate_Decreases)
        Water_Availability_Adjustment = 1 - math.exp(-Water_Availability_Coefficient * Plant_Available_Water)
        Potential_N_Uptake[layer] = Maximum_Daily_N_Uptake * Root_Fraction[layer] * Water_Availability_Adjustment * N_Availability_Adjustment  #'kg/m2
        if Potential_N_Uptake[layer] > Soil_N_Mass[layer]: Potential_N_Uptake[layer] = Soil_N_Mass[layer]
        Today_Potential_N_Uptake += Potential_N_Uptake[layer]

    Surplus = max(0, pCropState.Crop_N_Mass[DOY - 1] - pCropState.Maximum_N_Concentration[DOY] * (Cumulative_Top_Biomass / 10)) #'Convert biomass from Mg/ha to kg/m2
    Today_Crop_N_Demand = max(0, (Cumulative_Top_Biomass / 10) * pCropState.Maximum_N_Concentration[DOY] - pCropState.Crop_N_Mass[DOY - 1] - Surplus)  #'Convert biomass from Mg/ha to kg/m2
    Today_Expected_N_Uptake = min(Today_Crop_N_Demand, Today_Potential_N_Uptake)
    #'Calculate actual N uptake and update soil layer N mass
    Today_N_Uptake = 0
    for layer in range(1, Number_Of_Layers + 1):
        Layer_N_Uptake[layer] = min(Potential_N_Uptake[layer], Today_Expected_N_Uptake * Root_Fraction[layer])
        Today_N_Uptake += Layer_N_Uptake[layer]
        Soil_NO3_Mass[layer] -= Layer_N_Uptake[layer] * Nitrate_Mass_Fraction[layer]
        Soil_NH4_Mass[layer] -= Layer_N_Uptake[layer] * Ammonium_Mass_Fraction[layer]
        #'Update N mass
        pSoilState.Nitrate_N_Content[DOY][layer] = Soil_NO3_Mass[layer]
        pSoilState.Ammonium_N_Content[DOY][layer] = Soil_NH4_Mass[layer]

    Cum_N_Upt = pCropState.Cumulative_N_Uptake[DOY - 1] + Today_N_Uptake
    Crop_N = pCropState.Crop_N_Mass[DOY - 1] + Today_N_Uptake #'Crop N mass different to cumulative N uptake only if Crop N mass set at emergence or foliar applications considered
    if Cumulative_Top_Biomass > 0:
        Crop_N_Conc = Crop_N / (Cumulative_Top_Biomass / 10)  #'kgN/kgBiomass, but convert biomass from Mg/ha to kg/m2
    else:
        Crop_N_Conc = 0
    #'Update variables
    pCropState.Crop_N_Mass[DOY] = Crop_N
    pCropState.N_Uptake[DOY] = Today_N_Uptake
    pCropState.Cumulative_N_Uptake[DOY] = Cum_N_Upt
    pCropState.Crop_N_Concentration[DOY] = Crop_N_Conc
    if pCropState.Crop_N_Concentration[DOY] >= pCropState.Critical_N_Concentration[DOY]: 
        pCropState.Nitrogen_Stress_Index[DOY] = 0
    else:
        pCropState.Nitrogen_Stress_Index[DOY] = min(1, 1 - (pCropState.Crop_N_Concentration[DOY] - pCropState.Minimum_N_Concentration[DOY]) / (pCropState.Critical_N_Concentration[DOY] - pCropState.Minimum_N_Concentration[DOY]))


def InitCropState(pCropState):
    for i in range(1,366):
        pCropState.Potential_Green_Canopy_Cover[i] = 0.0
        pCropState.Green_Canopy_Cover[i] = 0.0
        pCropState.Total_Canopy_Cover[i] = 0.0
        pCropState.Potential_Total_Canopy_Cover[i] = 0.0
        pCropState.Root_Depth[i] = 0.0
        pCropState.Crop_Height[i] = 0.0
        pCropState.Root_Depth_At_Emergence[i] = 0.0
        pCropState.Today_Biomass_Gain[i] = 0.0
        pCropState.Cumulative_Crop_Biomass[i] = 0.0
        pCropState.Potential_Crop_Biomass[i] = 0.0
        pCropState.Crop_N_Mass[i] = 0.0
        pCropState.N_Uptake[i] = 0.0
        pCropState.Cumulative_N_Uptake[i] = 0.0
        pCropState.Crop_N_Concentration[i] = 0.0
        pCropState.Maximum_N_Concentration[i] = 0.0
        pCropState.Maximum_N_Concentration_At_Transition = 0
        pCropState.Daily_Change_Maximum_N_Concentration = 0
        pCropState.Critical_N_Concentration[i] = 0.0
        pCropState.Critical_N_Concentration_At_Transition = 0
        pCropState.Daily_Change_Critical_N_Concentration = 0
        pCropState.Minimum_N_Concentration[i] = 0.0
        pCropState.Minimum_N_Concentration_At_Transition = 0
        pCropState.Daily_Change_Minimum_N_Concentration = 0
        pCropState.DOY_Of_Transition = 0
        pCropState.Nitrogen_Stress_Index[i] = 0.0
        pCropState.Maximum_Green_Canopy_Cover_Reached = False
        