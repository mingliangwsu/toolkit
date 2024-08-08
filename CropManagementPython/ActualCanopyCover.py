#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 16:21:22 2024

@author: liuming
"""
def ActualCanopyExpansion(Potential_Canopy_Cover,Preday_Potential_Canopy_Cover,Preday_Actual_Canopy_Cover,
                          DailyLeafWaterPotential,Leaf_Water_Potential_That_Reduces_Canopy_Expansion,
                          Leaf_Water_Potential_That_Stops_Canopy_Expansion):
    Today_Potential_Canopy_Expansion = Potential_Canopy_Cover - Preday_Potential_Canopy_Cover
    Today_Leaf_Water_Potential = DailyLeafWaterPotential

    if Today_Potential_Canopy_Expansion > 0:
        if Today_Leaf_Water_Potential >= Leaf_Water_Potential_That_Reduces_Canopy_Expansion:
            Today_Actual_Canopy_Expansion = Today_Potential_Canopy_Expansion
        else:
            if Today_Leaf_Water_Potential > Leaf_Water_Potential_That_Stops_Canopy_Expansion:
                Today_Actual_Canopy_Expansion = Today_Potential_Canopy_Expansion * (Today_Leaf_Water_Potential - Leaf_Water_Potential_That_Stops_Canopy_Expansion) \
                                                / (Leaf_Water_Potential_That_Reduces_Canopy_Expansion - Leaf_Water_Potential_That_Stops_Canopy_Expansion)
            else:
                Today_Actual_Canopy_Expansion = 0
    else:
        Today_Actual_Canopy_Expansion = Today_Potential_Canopy_Expansion

    Actual_Canopy_Cover = Preday_Actual_Canopy_Cover + Today_Actual_Canopy_Expansion
    if Actual_Canopy_Cover < 0: Actual_Canopy_Cover = 0
    return Actual_Canopy_Cover