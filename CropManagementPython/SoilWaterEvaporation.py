#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:16:03 2024

@author: liuming
"""
import math
def SoilWaterEvaporation(Potential_ET,Crop_Fraction_Solar_Interception,
                         Residue_Fraction_Solar_Interception,Permanent_Wilting_Point,
                         Evaporation_Soil_Depth, Water_Content_Top_layer):
    Air_Dry_Water_Content = Permanent_Wilting_Point / 3.
    Potential_Soil_Water_Evaporation = Potential_ET * (1. - Crop_Fraction_Solar_Interception) \
                                       * (1. - Residue_Fraction_Solar_Interception)
    if (Water_Content_Top_layer > Permanent_Wilting_Point):
        Soil_Water_Evaporation = Potential_Soil_Water_Evaporation              #'Soil evaporation in mm/day = kg/m2/day
    elif (Water_Content_Top_layer > Air_Dry_Water_Content):
        Soil_Water_Evaporation = Potential_Soil_Water_Evaporation * math.pow((Water_Content_Top_layer - Air_Dry_Water_Content) 
               / (Permanent_Wilting_Point - Air_Dry_Water_Content), 2.)
    else:
        Soil_Water_Evaporation = 0
  
    Water_Content_Top_layer -= (Soil_Water_Evaporation / 1000) / Evaporation_Soil_Depth
    return Potential_Soil_Water_Evaporation,Soil_Water_Evaporation,Water_Content_Top_layer
