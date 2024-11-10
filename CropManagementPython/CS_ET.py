#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 20:57:26 2024

@author: liuming
"""
import math
from SoilHydrolics import *

class ETState:
    Potential_Transpiration = dict()
    Potential_Crop_Transpiration = dict()
    Potential_Soil_Water_Evaporation = dict()
    Potential_ET = dict()
    Actual_Transpiration = dict()
    Actual_Soil_Water_Evaporation = dict()
    Water_Stress_Index = dict()
    Root_Fraction = dict()
    Adjusted_Root_Fraction = dict() #(20) As Double
    Soil_Water_Uptake = dict() #(366,20)
    Total_Transpiration = 0
    
def PotET(DOY, Potential, Potential_Crop, Crop_Active, pCropState, pCropParameter, pCS_Weather, pETState):
    Reference_crop_ET = pCS_Weather.FAO_ETo[DOY]
    if Reference_crop_ET < 0.01: Reference_crop_ET = 0.01
    Wind_Speed = pCS_Weather.Wind_Speed[DOY]
    Minimum_Relative_Humidity = pCS_Weather.RHmin[DOY]
    if Crop_Active:
        if Potential_Crop:
            Potential_Total_Canopy_Cover = pCropState.Potential_Total_Canopy_Cover[DOY]
            Potential_Green_Canopy_Cover = pCropState.Potential_Green_Canopy_Cover[DOY]
        else:
            Total_Canopy_Cover = pCropState.Total_Canopy_Cover[DOY]
            Green_Canopy_Cover = pCropState.Green_Canopy_Cover[DOY]
    
        Crop_Height = pCropState.Crop_Height[DOY]

        Midseason_ET_Crop_Coefficient = pCropParameter.Midseason_Crop_Coefficient
        Maximum_Canopy_Cover = pCropParameter.Maximum_Green_Canopy_Cover
        
        #'If Main.GetTreeFruitCrop And (DAP >= Main.GetFruitHarvestDay) Then Today_Kc_transp = 0.2  THIS WILL BE ACTIVATED IF DEALING WITH TREE FRUITS AFTER HARVEST
        #'    Else
        
        #'End If
        if Potential_Crop:
            Today_Kc_transp = Midseason_ET_Crop_Coefficient * Potential_Green_Canopy_Cover / Maximum_Canopy_Cover
            pETState.Potential_Crop_Transpiration[DOY] = Reference_crop_ET * Today_Kc_transp
            Kcmax = max(1.1 + (0.04 * (Wind_Speed - 2) - 0.004 * (Minimum_Relative_Humidity - 45)) * math.pow(Crop_Height / 3, 0.3), 0.05 + Today_Kc_transp)
            Today_Kc_evap = max(0.05, Kcmax - Midseason_ET_Crop_Coefficient * Total_Canopy_Cover / Maximum_Canopy_Cover) #'accounts for total shading from the canopy (green + senesced)
            pETState.Potential_Soil_Water_Evaporation[DOY] = Reference_crop_ET * Today_Kc_evap
            pETState.Potential_ET[DOY] = pETState.Potential_Crop_Transpiration[DOY] + pETState.Potential_Soil_Water_Evaporation[DOY]
        else:
            Today_Kc_transp = Midseason_ET_Crop_Coefficient * Green_Canopy_Cover / Maximum_Canopy_Cover
            Kcmax = max(1.1 + (0.04 * (Wind_Speed - 2) - 0.004 * (Minimum_Relative_Humidity - 45)) * math.pow((Crop_Height / 3), 0.3), 0.05 + Today_Kc_transp)
            Today_Kc_evap = max(0.05, Kcmax - Midseason_ET_Crop_Coefficient * Total_Canopy_Cover / Maximum_Canopy_Cover) #'accounts for total shading from the canopy (green + senesced)
            pETState.Potential_Transpiration[DOY] = Reference_crop_ET * Today_Kc_transp
            pETState.Potential_Soil_Water_Evaporation[DOY] = Reference_crop_ET * Today_Kc_evap
            pETState.Potential_ET[DOY] = pETState.Potential_Transpiration[DOY] + pETState.Potential_Soil_Water_Evaporation[DOY]
    else:
        Today_Kc_transp = 0
        Crop_Height = 0
        Kcmax = max(1.1 + (0.04 * (Wind_Speed - 2.) - 0.004 * (Minimum_Relative_Humidity - 45.)) * math.pow(Crop_Height / 3., 0.3), 0.05 + Today_Kc_transp)
        Today_Kc_evap = Kcmax
        pETState.Potential_Soil_Water_Evaporation[DOY] = Reference_crop_ET * Today_Kc_evap
        pETState.Potential_ET[DOY] = pETState.Potential_Soil_Water_Evaporation[DOY]


def ActualTranspiration(DOY, pCropParameter, pSoilModelLayer, pCropState, pETState, pSoilState):
    #'Calculate water uptake assumed equal to actual transpiration
    
    Layer_Plant_Hydraulic_Conductance = dict()
    Layer_Root_Fraction_Adjustment = dict()
    #Adjusted_Root_Fraction = dict()
    Soil_WP = dict()
    WP_At_FC = dict()
    WP_At_PWP = dict()
    Air_Entry_Potential = dict()
    Root_Activity_Factor = dict()
    Soil_Water_Uptake = dict()
    
    
    WD = 1000 #'Water density in kg/m3
    #'Read parameters
    LeafWP_Wilt = pCropParameter.LWP_Permanent_Wilting
    Number_Of_Soil_Layers = pSoilModelLayer.Number_Model_Layers
    for i in range(2, Number_Of_Soil_Layers + 1):
        WP_At_FC[i] = pSoilModelLayer.WP_At_FC[i]
        WP_At_PWP[i] = pSoilModelLayer.WP_At_PWP[i]
        Air_Entry_Potential[i] = pSoilModelLayer.Air_Entry_Potential[i]
    
    Today_Potential_Transpiration = pETState.Potential_Transpiration[DOY]
    Current_green_Canopy_Cover = pCropState.Green_Canopy_Cover[DOY] #'Use yesterday value. Today value not calculated et
    Green_Canopy_Cover_Max = pCropParameter.Maximum_Green_Canopy_Cover
    LeafWP_OnsetStress = pCropParameter.LWP_Onset_Stomatal_Closure
    Root_Depth = pCropState.Root_Depth[DOY]
    
    #'Calculate today's crop maximun water uptake rate (kg/m2/d = mm/d)
    Max_CropWater_Uptake_Full_Canopy = pCropParameter.Maximum_Crop_Water_Uptake
    Today_Crop_Max_Water_Uptake = Max_CropWater_Uptake_Full_Canopy * Current_green_Canopy_Cover / Green_Canopy_Cover_Max
    
    #'Calculate today's expected crop transpiration rate (kg/m2/d = mm/d)
    #'Today_Expected_Crop_Water_Uptake = Minimum(Potential_Transpiration_Full_Canopy, Max_CropWater_Uptake_Full_Canopy) * Current_green_Canopy_Cover / Green_Canopy_Cover_Max
    
    Today_Expected_Crop_Water_Uptake = min(Today_Potential_Transpiration, Today_Crop_Max_Water_Uptake)
    
    #'Calculate plant hydraulic conductivity ((kg^2)/(m2-J-d), the capacity of the vascular system to conduct water, assumes that maximum crop uptake takes place at a soil water potential of zero
    Plant_Hydraulic_Conductance = Today_Crop_Max_Water_Uptake / (-LeafWP_OnsetStress)
                                       
    #'Calculate root fraction per soil layer
    Layer_Bottom_Depth = 0
    Root_Fraction_Sum = 0
    Effective_Root_Depth = max(0, Root_Depth - pSoilModelLayer.Layer_Thickness[i])
    for i in range(2, Number_Of_Soil_Layers + 1):
        Layer_Thickness = pSoilModelLayer.Layer_Thickness[i]
        if Layer_Thickness > 0: 
          Layer_Bottom_Depth += Layer_Thickness
          pETState.Root_Fraction[i] = CalculateRootFraction(Layer_Bottom_Depth, Layer_Thickness, Root_Depth)
          Root_Fraction_Sum = Root_Fraction_Sum + pETState.Root_Fraction[i]
        else:
          i = Number_Of_Soil_Layers
        
    #print(f'DOY:{DOY} Root_Fraction_Sum:{Root_Fraction_Sum}')
    #'Adjust root fraction for shallow soils to ensure that the sum of root fraction of all layers is equal to 1
    if (Root_Depth > Layer_Bottom_Depth) and (Root_Fraction_Sum < 1):
        NewRoot_Fraction_Sum = 0
        for i in range(2, Number_Of_Soil_Layers + 1):
            pETState.Root_Fraction[i] /= Root_Fraction_Sum
            NewRoot_Fraction_Sum += pETState.Root_Fraction[i]
        Root_Fraction_Sum = NewRoot_Fraction_Sum

    
    #'Adjust root fraction based on soil dryness or soil near saturation
    Sum_Root_Fraction_Adjustment = 0
    for i in range(2, Number_Of_Soil_Layers + 1):
        
        #in some cases Soil_Water_Potential not being updated
        #WC = pSoilState.Water_Content[DOY][i]
        #Sat_WC = pSoilModelLayer.Saturation_Water_Content[i]
        #AEP = pSoilModelLayer.Air_Entry_Potential[i]
        #B_Val = pSoilModelLayer.B_value[i]
        #pSoilState.Soil_Water_Potential[i] = WP(Sat_WC, WC, AEP, B_Val)
        
        
        Soil_WP[i] = pSoilState.Soil_Water_Potential[i]
        if Soil_WP[i] <= WP_At_FC[i]:
            Root_Activity_Factor[i] = 1 - math.pow(((Soil_WP[i] - WP_At_FC[i]) / (WP_At_PWP[i] - WP_At_FC[i])), 8) #'Calculate dry end of root activity
        else:
            Root_Activity_Factor[i] = 1 - math.pow(((Soil_WP[i] - WP_At_FC[i]) / (Air_Entry_Potential[i] - WP_At_FC[i])), 20) #'Calculate wet end of root activity
        
        if Root_Activity_Factor[i] > 1: Root_Activity_Factor[i] = 1
        if Root_Activity_Factor[i] < 0: Root_Activity_Factor[i] = 0
        Layer_Root_Fraction_Adjustment[i] = pETState.Root_Fraction[i] * Root_Activity_Factor[i]
        Sum_Root_Fraction_Adjustment += Layer_Root_Fraction_Adjustment[i]
    
    for i in range(2, Number_Of_Soil_Layers + 1):
        if Sum_Root_Fraction_Adjustment == 0:
            pETState.Adjusted_Root_Fraction[i] = 0
            Layer_Plant_Hydraulic_Conductance[i] = 0
        else:
            pETState.Adjusted_Root_Fraction[i] = Layer_Root_Fraction_Adjustment[i] / Sum_Root_Fraction_Adjustment
            Layer_Plant_Hydraulic_Conductance[i] = Plant_Hydraulic_Conductance * pETState.Adjusted_Root_Fraction[i]
    
    #'Calculate average soil water potential (J/kg)
    Average_Soil_WP = 0
    for i in range(2, Number_Of_Soil_Layers + 1):
        Average_Soil_WP += Soil_WP[i] * pETState.Adjusted_Root_Fraction[i]
    
    #'Calculate leaf water potential
    if Plant_Hydraulic_Conductance == 0: 
        Leaf_Water_Pot = LeafWP_Wilt
    else:
        Leaf_Water_Pot = Average_Soil_WP - Today_Expected_Crop_Water_Uptake / Plant_Hydraulic_Conductance
        if Leaf_Water_Pot < LeafWP_OnsetStress:
            Leaf_Water_Pot = (Plant_Hydraulic_Conductance * Average_Soil_WP * (LeafWP_OnsetStress - \
                LeafWP_Wilt) + LeafWP_Wilt * Today_Expected_Crop_Water_Uptake) / (Plant_Hydraulic_Conductance * \
                (LeafWP_OnsetStress - LeafWP_Wilt) + Today_Expected_Crop_Water_Uptake)
        if Leaf_Water_Pot < LeafWP_Wilt: Leaf_Water_Pot = LeafWP_Wilt

        
    #'Calculate crop water uptake (kg/m2/d = mm/d)
    Crop_Water_Uptake = 0
    for i in range(2, Number_Of_Soil_Layers + 1):
        pETState.Soil_Water_Uptake[DOY][i] = Layer_Plant_Hydraulic_Conductance[i] * (Soil_WP[i] - Leaf_Water_Pot)
        Crop_Water_Uptake = Crop_Water_Uptake + pETState.Soil_Water_Uptake[DOY][i]
        #'Update water content and potential
        pSoilState.Water_Content[DOY][i] -= pETState.Soil_Water_Uptake[DOY][i] / (pSoilModelLayer.Layer_Thickness[i] * WD)
        WC = pSoilState.Water_Content[DOY][i]
        Sat_WC = pSoilModelLayer.Saturation_Water_Content[i]
        AEP = pSoilModelLayer.Air_Entry_Potential[i]
        B_Val = pSoilModelLayer.B_value[i]
        pSoilState.Soil_Water_Potential[i] = WP(Sat_WC, WC, AEP, B_Val)
        pSoilState.Water_Filled_Porosity[DOY][i] = WC / Sat_WC

    Act_Transp = Crop_Water_Uptake
    #print(f'DOY:{DOY} Act_Transp:{Act_Transp} Today_Potential_Transpiration:{Today_Potential_Transpiration}')
    #'This limits in the case that intercepted precipitation is sufficient to meet the evaporative demand
    #if Act_Transp > Today_Potential_Transpiration: Act_Transp = Today_Potential_Transpiration
    if Crop_Water_Uptake > 0:
        pETState.Water_Stress_Index[DOY] = 1 - (Crop_Water_Uptake / Today_Expected_Crop_Water_Uptake)
        pETState.Actual_Transpiration[DOY] = Crop_Water_Uptake
    else: #'Crop water uptake is negative due to layer water redistribution by roots
        pETState.Actual_Transpiration[DOY] = 0
        pETState.Water_Stress_Index[DOY] = 0

    if pETState.Water_Stress_Index[DOY] < 0.00000001: pETState.Water_Stress_Index[DOY] = 0
    pETState.Total_Transpiration += pETState.Actual_Transpiration[DOY]
    
def CalculateRootFraction(z, dz, Rd):
    if Rd > z: 
        f = dz * (2 * (Rd - z) + dz) / (Rd * Rd)
    elif Rd < (z - dz + 0.00001): 
        f = 0
    else: 
        f = math.pow(((Rd - z + dz) / Rd), 2)
    return f


def ActEvaporation(DOY,pSoilModelLayer,pSoilState,pETState):
    WD = 1000 #'kg/m3
    Residue_Fraction_Solar_Interception = 0 #'Currently not implemented
    #Percent_Sand_Top_Layer = pSoilModelLayer.Percent_Sand[1]
    Water_Content_Top_layer = pSoilState.Water_Content[DOY][1]
    Permanent_Wilting_Point = pSoilModelLayer.PWP_Water_Content[1]
    Air_Dry_Water_Content = Permanent_Wilting_Point / 3
    #'Evaporation_Soil_Depth = Round(0.169 - 0.001 * Percent_Sand_Top_Layer, 2)
    Pot_Soil_Water_Evap = pETState.Potential_Soil_Water_Evaporation[DOY] * (1 - Residue_Fraction_Solar_Interception)
    if Water_Content_Top_layer > Permanent_Wilting_Point: 
        pETState.Actual_Soil_Water_Evaporation[DOY] = Pot_Soil_Water_Evap  #'Soil evaporation in mm/day = kg/m2/day
    elif Water_Content_Top_layer > Air_Dry_Water_Content:
          pETState.Actual_Soil_Water_Evaporation[DOY] = Pot_Soil_Water_Evap * math.pow(((Water_Content_Top_layer - Air_Dry_Water_Content) \
                 / (Permanent_Wilting_Point - Air_Dry_Water_Content)), 2)
    else:
          pETState.Actual_Soil_Water_Evaporation[DOY] = 0

    #'Update water content and potential of top layer
    pSoilState.Water_Content[DOY][1] -= pETState.Actual_Soil_Water_Evaporation[DOY] / (pSoilModelLayer.Layer_Thickness[1] * WD)
    
    #Testing?
    WC = pSoilState.Water_Content[DOY][1]
    Sat_WC = pSoilModelLayer.Saturation_Water_Content[1]
    AEP = pSoilModelLayer.Air_Entry_Potential[1]
    B_Val = pSoilModelLayer.B_value[1]
    pSoilState.Soil_Water_Potential[1] = WP(Sat_WC, WC, AEP, B_Val)
    pSoilState.Water_Filled_Porosity[DOY][1] = WC / Sat_WC
    
def InitETState(pETState):
    for i in range(1,367):
        pETState.Potential_Transpiration[i] = 0.0
        pETState.Potential_Crop_Transpiration[i] = 0.0
        pETState.Potential_Soil_Water_Evaporation[i] = 0.0
        pETState.Potential_ET[i] = 0.0
        pETState.Actual_Transpiration[i] = 0.0
        pETState.Actual_Soil_Water_Evaporation[i] = 0.0
        pETState.Water_Stress_Index[i] = 0.0
        pETState.Soil_Water_Uptake[i] = dict()
        for j in range(1,21):
            pETState.Soil_Water_Uptake[i][j] = 0.0
    for i in range(1,31):
        pETState.Root_Fraction[i] = 0.0
        pETState.Adjusted_Root_Fraction[i] = 0.
    pETState.Total_Transpiration = 0.

def ClearETState(pETState):
    for i in range(1,367):
        pETState.Potential_Transpiration[i] = 0.0
        pETState.Potential_Crop_Transpiration[i] = 0.0
        pETState.Potential_Soil_Water_Evaporation[i] = 0.0
        pETState.Potential_ET[i] = 0.0
        pETState.Actual_Transpiration[i] = 0.0
        pETState.Actual_Soil_Water_Evaporation[i] = 0.0
        pETState.Water_Stress_Index[i] = 0.0
    pETState.Total_Transpiration = 0