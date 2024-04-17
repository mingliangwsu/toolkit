#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:42:51 2024

@author: liuming
"""
import SoilProcessesClass as SoilP
import SoilConfig
from ExcelDataframeExchange import *

def InitializeSoilProfile(Cells):
    SoilConfig.Number_Of_Layers = int(get_excel_value(Cells, 'A5'))
    #'Read in soil profile
    for i in range(1, SoilConfig.Number_Of_Layers+1):
        SoilConfig.DZ[i] = 0.1
    #'Initialize soil properties
    for i in range(1, SoilConfig.Number_Of_Layers+1):
        SoilConfig.FC[i] = float(get_excel_value(Cells,'A6'))
        SoilConfig.BD[i] = float(get_excel_value(Cells,'A7'))
        SoilConfig.WC[i] = float(get_excel_value(Cells,'A8'))
    #'Initialize chemical mass per soil layer (kg/m2)
    for i in range(1, SoilConfig.Number_Of_Layers+1):
        SoilConfig.Chem_Mass[i] = 0.0
    SoilConfig.Chem_Mass[1] = float(get_excel_value(Cells,'A11')) / 10000.0
    #'Initialize chemical constant for Langmuir isotherm
    K = float(get_excel_value(Cells,'A12'))
    Q = float(get_excel_value(Cells,'A13'))


def RunCascade(Number_Of_Layers, Water_Flux_In, Chem_Conc_In, 
        Number_Of_Pulses):
    SoilP.CascadeInfiltrationPlusSolute(Number_Of_Layers, 
                                  Water_Flux_In, 
                                  SoilConfig.K, 
                                  SoilConfig.Q, 
                                  Chem_Conc_In, 
                                  Number_Of_Pulses)

