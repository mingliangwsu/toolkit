#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:50:27 2024

@author: liuming
"""

Layer_thickness = dict()
BD = dict()  #'Soil bulk density (kg/m3)
b = dict()
WC = dict()
FC = dict() #'Soil layer field capacity (m3/m3)
PWP = dict() #'Soil layer permanent wilting point (m3/m3)
PAW = dict() 
Soil_WP = dict()
WP_At_FC = dict()
WP_At_PWP = dict()
Air_Entry_Potential = dict()

Root_Fraction = dict()
Soil_Water_Uptake = dict()
Root_Activity_Factor = dict()
Adjusted_Root_Fraction = dict()

#for N demand
Potential_N_Uptake = dict()
Layer_Bottom_Depth = dict()
Soil_N_Mass = dict()
Nitrogen_Application_DAE = dict()
Nitrogen_Application_Amount = dict()
Layer_N_Uptake = dict()

Cells = None

Crop_Water_Uptake = 0
Act_Transp = 0
Root_Fraction_Sum = 0
Leaf_Water_Pot = 0
Today_Potential_Transpiration = 0
Today_Crop_Max_Water_Uptake = 0
Today_Expected_Crop_Water_Uptake = 0
Average_Soil_WP = 0
Water_Stress_Index = 0