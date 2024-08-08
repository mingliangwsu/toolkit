#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:30:29 2024

@author: liuming
"""
import math
def BiomassGrowth(Maximum_Temperature,Minimum_Relative_Humidity,
                  Transpiration_Use_Efficiency_At_1kpa,TUE_Slope, 
                  Crop_Transpiration):
    Daytime_VPD = math.max(0.5, 0.7 * 0.6108 * math.exp(17.27 * Maximum_Temperature / (Maximum_Temperature + 237.3)) * (1 - Minimum_Relative_Humidity / 100))
    Daily_Transpiration_Use_Efficiency = Transpiration_Use_Efficiency_At_1kpa / (Daytime_VPD ^ TUE_Slope)
    Biomass_Gain = Crop_Transpiration * Daily_Transpiration_Use_Efficiency
    return Biomass_Gain