#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 08:50:59 2024

@author: liuming
"""

#import sys
#print("Initiate SoilConfig")
Number_Of_Layers = None #'Number of soil layers
FC = dict() #'Soil layer field capacity (m3/m3)
PWP = dict() #'Soil layer permanent wilting point (m3/m3)
BD = dict()  #'Soil bulk density (kg/m3)
WC = dict()  #'Soil layer water content (m3/m3)
Chem_Mass = dict()  #'Chemical mass per soil layer (kg/m2)
DZ = dict()  #'Soil layer thickness (m)
K = 0.0 #'Initialize chemical constant for Langmuir isotherm
Q = 0.0 #'Initialize chemical constant for Langmuir isotherm
Drainage = 0.0 #'drainage flux in mm/day = kg/m2/day
Chemical_Leaching = 0.0 #'Leaching in kg Salt/m2
Chemical_Balance = 0.0 #'Chemical Balance in kg/m2
Water_Balance = 0.0 #'Water Balance in kg/m2 or mm
Cells = None

WD = 1000 ##'water density in kg/m3
