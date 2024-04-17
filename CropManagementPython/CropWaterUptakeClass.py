#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:56:40 2024

@author: liuming
"""
import WaterUptakeConfig as Soil

def WaterUptake(
        Reference_Crop_ETo, Crop_Coefficient_Full_Canopy, 
        Water_Intercepted_By_Canopy, Crop_Max_Water_Uptake, 
        LeafWP_OnsetStress, LeafWP_Wilt, 
        Green_Canopy_Cover_Max, Current_green_Canopy_Cover, 
        RootDepth, NumberOfLayers):
    #'Calculate today's potential transpiration rate (kg/m2/d = mm/d)
    Potential_Transpiration_Full_Canopy = (Crop_Coefficient_Full_Canopy 
                                          * Reference_Crop_ETo)
    Soil.Today_Potential_Transpiration = (Potential_Transpiration_Full_Canopy 
                                     * Current_green_Canopy_Cover 
                                     / Green_Canopy_Cover_Max)
    #'Calculate today's crop maximun water uptake rate (kg/m2/d = mm/d)
    Max_CropWater_Uptake_Full_Canopy = Crop_Max_Water_Uptake
    Soil.Today_Crop_Max_Water_Uptake = (Max_CropWater_Uptake_Full_Canopy 
                                   * Current_green_Canopy_Cover 
                                   / Green_Canopy_Cover_Max)
    #'Calculate today's expected crop transpiration rate (kg/m2/d = mm/d)
    Soil.Today_Expected_Crop_Water_Uptake = (
        min(Potential_Transpiration_Full_Canopy, 
            Max_CropWater_Uptake_Full_Canopy)
        * Current_green_Canopy_Cover / Green_Canopy_Cover_Max 
        - Water_Intercepted_By_Canopy)
        #'Calculate plant hydraulic conductivity ((kg^2)/(m2-J-d), 
        #the capacity of the vascular system to conduct water, assumes that 
        #maximum crop uptake takes place at a soil water potential of zero
    Plant_Hydraulic_Conductance = (Soil.Today_Crop_Max_Water_Uptake 
                                       / (-LeafWP_OnsetStress))
    #'Calculate root fraction per soil layer
    Layer_Bottom_depth = 0
    Soil.Root_Fraction_Sum = 0
    for i in range(1, NumberOfLayers+1):
        if Soil.Layer_thickness[i] > 0:
            Layer_Bottom_depth += Soil.Layer_thickness[i]
            Soil.Root_Fraction[i] = CalculateRootFraction(Layer_Bottom_depth, 
                                                     Soil.Layer_thickness[i], 
                                                     RootDepth)
            Soil.Root_Fraction_Sum += Soil.Root_Fraction[i]
        else:
            break;
    #'Adjust root fraction for shallow soils to ensure that the sum of root 
    #fraction of all layers is equal to 1
    if (RootDepth > Layer_Bottom_depth) and (Soil.Root_Fraction_Sum < 1):
        NewRoot_Fraction_Sum = 0
        for i in range(1, NumberOfLayers+1):
            Soil.Root_Fraction[i] /= Soil.Root_Fraction_Sum
            NewRoot_Fraction_Sum += Soil.Root_Fraction[i]
        Soil.Root_Fraction_Sum = NewRoot_Fraction_Sum
    #'Adjust root fraction based on soil dryness or soil near saturation
    Sum_Root_Fraction_Adjustment = 0
    Layer_Root_Fraction_Adjustment = dict()
    for i in range(1, NumberOfLayers+1):
        if Soil.Soil_WP[i] <= Soil.WP_At_FC[i]:
            Soil.Root_Activity_Factor[i] = 1 - pow((Soil.Soil_WP[i] 
                                                    - Soil.WP_At_FC[i]) 
                                                   / (Soil.WP_At_PWP[i] 
                                                      - Soil.WP_At_FC[i]), 
                                                   8) 
            #'Calculate dry end of root activity
        else:
            Soil.Root_Activity_Factor[i] = 1 - pow((Soil.Soil_WP[i] 
                                                    - Soil.WP_At_FC[i]) 
                                              / (Soil.Air_Entry_Potential[i] 
                                              - Soil.WP_At_FC[i]),
                                              20) 
            #'Calculate wet end of root activity
        if Soil.Root_Activity_Factor[i] > 1:
            Soil.Root_Activity_Factor[i] = 1
        elif Soil.Root_Activity_Factor[i] < 0:
            Soil.Root_Activity_Factor[i] = 0
        Layer_Root_Fraction_Adjustment[i] = (Soil.Root_Fraction[i] 
                                            * Soil.Root_Activity_Factor[i])
        Sum_Root_Fraction_Adjustment += Layer_Root_Fraction_Adjustment[i]
    Layer_Plant_Hydraulic_Conductance = dict()
    for i in range(1, NumberOfLayers+1):
        Soil.Adjusted_Root_Fraction[i] = (Layer_Root_Fraction_Adjustment[i] 
                                    / Sum_Root_Fraction_Adjustment)
        Layer_Plant_Hydraulic_Conductance[i] = (Plant_Hydraulic_Conductance 
                                               * Soil.Adjusted_Root_Fraction[i])
    #'Calculate average soil water potential (J/kg)
    Soil.Average_Soil_WP = 0
    #print(f'NumberOfLayers:{NumberOfLayers}')
    for i in range(1, NumberOfLayers+1):
        Soil.Average_Soil_WP += Soil.Soil_WP[i] * Soil.Adjusted_Root_Fraction[i]
    #'Calculate leaf water potential
    Soil.Leaf_Water_Pot = (Soil.Average_Soil_WP 
                     - Soil.Today_Expected_Crop_Water_Uptake 
                     / Plant_Hydraulic_Conductance)
    if Soil.Leaf_Water_Pot < LeafWP_OnsetStress:
        Soil.Leaf_Water_Pot = ((Plant_Hydraulic_Conductance 
                          * Soil.Average_Soil_WP 
                          * (LeafWP_OnsetStress - LeafWP_Wilt) 
                          + LeafWP_Wilt * Soil.Today_Expected_Crop_Water_Uptake
                         ) 
                         / (Plant_Hydraulic_Conductance 
                            * (LeafWP_OnsetStress - LeafWP_Wilt) 
                            + Soil.Today_Expected_Crop_Water_Uptake)
                         )
    if Soil.Leaf_Water_Pot < LeafWP_Wilt:
        Soil.Leaf_Water_Pot = LeafWP_Wilt
    #'Calculate crop water uptake (kg/m2/d = mm/d)
    Soil.Crop_Water_Uptake = 0
    for i in range(1, NumberOfLayers+1):
        Soil.Soil_Water_Uptake[i] = (Layer_Plant_Hydraulic_Conductance[i] 
                               * (Soil.Soil_WP[i] - Soil.Leaf_Water_Pot))
        Soil.Crop_Water_Uptake += Soil.Soil_Water_Uptake[i]
    Soil.Act_Transp = Soil.Crop_Water_Uptake + Water_Intercepted_By_Canopy
    #'This limits in the case that intercepted precipitation is sufficient 
    #to meet the evaporative demand
    if Soil.Act_Transp > Soil.Today_Potential_Transpiration:
        Soil.Act_Transp = Soil.Today_Potential_Transpiration
    Soil.Water_Stress_Index = 1 - (Soil.Crop_Water_Uptake 
                              / Soil.Today_Expected_Crop_Water_Uptake)
        
def CalculateRootFraction(z, dz, Rd):
    if Rd > z: 
        f = dz * (2 * (Rd - z) + dz) / (Rd * Rd)
    elif Rd < (z - dz + 0.00001): 
        f = 0
    else: 
        f = pow((Rd - z + dz) / Rd, 2)
    return f


