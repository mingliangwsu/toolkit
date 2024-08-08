#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:06:06 2024
NOT IMPLEMENTED YET!
@author: liuming
"""
import math
import WaterUptakeConfig as WUC

Wilting_Point = WUC.PWP #double check
Water_Content = WUC.WC  #
Field_Capacity = WUC.FC
Layer_Thickness = WUC.Layer_thickness
Number_Of_Layers = WUC.Number_Of_Layers

def Evaporation(Pot_Evaporation, PWP_Top_Layer):
    #'Soil evaporation in mm/day = kg/m2/day
    Air_Dry_Water_Content = Wilting_Point[1] / 3  #'This is an approximation to air-dry water content
    if Water_Content[1] < Wilting_Point[1]:
        Evaporation = Pot_Evaporation * math.pow(((Water_Content[1] - Air_Dry_Water_Content) 
           / (Wilting_Point[1] - Air_Dry_Water_Content)), 2)
    else:
        Evaporation = Pot_Evaporation
    return Evaporation

def CascadeInfiltration(Precipitation, Water_Flux_In):
  #'This subroutine calculates water infiltration using a cascading
  #'approach.  It requires that field capacity, thickness, and
  #'water content of each soil layer are known
    Jl = dict() #(mmax) As Single
    WD = 1000 #'Water density in kg/m3
    Jl[0] = (Precipitation + Water_Flux_In) / WD #'Convert liquid fluxes from kg/m2/day to m/day
    Sum_Drainage = 0
    if Jl[0] > 0:
        for j in range(1, Number_Of_Layers + 1):
            if Jl[j - 1] > (Field_Capacity[j] - Water_Content[j]) * Layer_Thickness[j]:
                Jl[j] = Jl[j - 1] - (Field_Capacity[j] - Water_Content[j]) * Layer_Thickness[j]
                Water_Content[j] = Field_Capacity[j]
            else:
                Water_Content[j] += Jl[j - 1] / (Layer_Thickness[j])
                Jl[j] = 0
        Sum_Drainage += Jl[Number_Of_Layers] * WD
    return Sum_Drainage

