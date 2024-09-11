#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 10:13:14 2024

@author: liuming
"""
import math
#Soil Hydrologics
Thickness_Model_Layers = 0.1

class SoilHorizons:
    Number_Of_Horizons = 0
    Horizon_Thickness = dict()
    Clay = dict()
    Sand = dict()
    Silt = dict()
    AE_Pot = dict()
    B_Val = dict()
    FC_WP = dict()
    PWP_WP = dict()
    Bulk_Dens = dict()
    Sat_WC = dict()
    FC_WC = dict()
    PWP_WC = dict()
    Soil_Organic_Carbon = dict()
    Number_Of_Sublayers = dict()

class SoilModelLayer:
    Number_Model_Layers = 0
    Air_Entry_Potential = dict()
    B_value = dict()
    WP_At_FC = dict()
    WP_At_PWP = dict()
    FC_Water_Content = dict()
    PWP_Water_Content = dict()
    Plant_Available_Water_Content = dict()
    Bulk_Density = dict()
    Layer_Thickness = dict()
    Saturation_Water_Content = dict()

class SoilState:
    Water_Content = dict() #(365, 20) As Double
    Nitrate_N_Content = dict() #(365, 20) As Double
    Ammonium_N_Content = dict() #(365, 20) As Double
    N_Leaching = dict() #(365) As Double
    Deep_Drainage = dict() #(365) As Double
    Chemical_Balance = dict() #(365) As Double
    Water_Balance = dict() #(365) As Double
    
    Soil_Water_Potential  = dict() # = dict()
    
    Cumulative_Deep_Drainage = 0
    Cumulative_N_Leaching = 0
    Sum_N_Fertilization = 0

def InitSoilState(pSoilState):
    for i in range(1,366):
        pSoilState.Water_Content[i] = dict()
        pSoilState.Nitrate_N_Content[i] = dict()
        pSoilState.Ammonium_N_Content[i] = dict()
        for j in range(1,21):
            pSoilState.Water_Content[i][j] = 0
            pSoilState.Nitrate_N_Content[i][j] = 0
            pSoilState.Ammonium_N_Content[i][j] = 0
        pSoilState.N_Leaching[i] = 0
        pSoilState.Deep_Drainage[i] = 0
        pSoilState.Chemical_Balance[i] = 0
        pSoilState.Water_Balance[i] = 0
    for j in range(1,21):
        pSoilState.Soil_Water_Potential[j] = 0
    Cumulative_Deep_Drainage = 0
    Cumulative_N_Leaching = 0
    Sum_N_Fertilization = 0
def WS(Sand, Clay):
    #'Calculate saturation water content (m3/m3) using Saxton's pedotransfer function
    WS = 0.332 - 0.0007251 * Sand + (math.log(Clay) / math.log(10)) * 0.1276
    return WS
def BD(Sand, Clay):
    #'Calculate bulk density (Mg/m3)
    #'Calculate saturation water content (m3/m3) using Saxton's pedotransfer function
    Saturation_WC = 0.332 - 0.0007251 * Sand + (math.log(Clay) / math.log(10)) * 0.1276
    BD = 2.65 * (1 - Saturation_WC)
    return BD
def B(Sand, Clay):
    #'Calculate b value
    B_value = -(-3.14 - 0.00222 * math.pow(Clay,2) - 0.00003484 * math.pow(Sand, 2) * Clay)
    return B_value
def AE(Sand, Clay):
    #'Calculate air entry potential
    #'Calculate saturation water content (m3/m3)
    Saturation_WC = 0.332 - 0.0007251 * Sand + (math.log(Clay) / math.log(10)) * 0.1276
    #'Calculate a value
    A_Value = 100 * math.exp(-4.396 - 0.0715 * Clay - 0.000488 * math.pow(Sand, 2) - 0.00004285 * math.pow(Sand, 2) * Clay)
    #'Calculate b value
    B_value = -(-3.14 - 0.00222 * math.pow(Clay, 2) - 0.00003484 * math.pow(Sand, 2) * Clay)
    #'Calculate Air Entry Potential
    Air_Entry_Potential = -A_Value * math.pow(Saturation_WC, (-B_value))
    return Air_Entry_Potential
def KS(Sand, Clay):
    #'Calculate saturated hydraulic conductivity
    G = 9.81  #'gravitational acceleration (m/s2)
    Water_Density = 1000  #' (kg/m3)
    #'Calculate saturation water content (m3/m3)
    Saturation_WC = 0.332 - 0.0007251 * Sand + (math.log(Clay) / math.log(10)) * 0.1276
    #'Calculate saturated hydraulic conductivity (kg s/m3)
    Factor = Water_Density / (G * 100 * 3600) #'converts cm/h to Kg s / m3
    Ksat = Factor * math.exp(12.012 - 0.0755 * Sand + (-3.895 + 0.03671 * Sand - 0.1103 * Clay + 0.00087546 * math.pow(Clay, 2)) * (1 / Saturation_WC))
    return Ksat
def WPFC(Clay, Silt):
    #'Calculate water potential at field capacity
    WP_At_FC = -13.833 * math.log(Clay) + 10.356
    if Silt > 70: WP_At_FC = -33
    if WP_At_FC > -10: WP_At_FC = -10
    return WP_At_FC
def WC(WS, WP, AE, B):
    #'Calculate water content from water potential
    WC = WS * (math.pow(WP / AE, (-1 / B)))
    return WC
def WP(WS, WC, AE, B):
    #'Calculate water potential from water content
    WP = AE * math.pow((WC / WS), (-B))
    return WP
def KSAP(B, WS, FC, HTFC):
    Gr = 9.81  #'gravitational acceleration (m/s2)
    WD = 1000  #'water density (kg/m3)
    dz = 0.05  #'soil thickness (m()
    m = 2 * B + 3
    KSAP = dz * WD * math.pow(WS, m) * (math.pow(FC, (1 - m)) - math.pow(WS, (1 - m))) \
                        / (Gr * HTFC * 3600 * (m - 1))
    return KSAP
def k(KS, AE, B, WP):
    #'Calculate hydraulic conductivity as a function of water potential
    n = 2 + 3 / B
    k = KS * math.pow((AE / WP), n)
    return k

def CalculateHydraulicProperties(N_Horz,pSoilHorizons,pSoilModelLayer):
    for i in range(1, N_Horz+1):
        Clay = pSoilHorizons.Clay[i]
        Sand = pSoilHorizons.Sand[i]
        Silt = pSoilHorizons.Silt[i]
        pSoilHorizons.AE_Pot[i] = AE(Sand, Clay)
        pSoilHorizons.B_Val[i] = B(Sand, Clay)
        pSoilHorizons.FC_WP[i] = WPFC(Clay, Silt)
        pSoilHorizons.PWP_WP[i] = -1500
        pSoilHorizons.Bulk_Dens[i] = BD(Sand, Clay)
        pSoilHorizons.Sat_WC[i] = WS(Sand, Clay)
        if pSoilHorizons.FC_WC[i] <= 0: 
            pSoilHorizons.FC_WC[i] = WC(pSoilHorizons.Sat_WC[i], pSoilHorizons.FC_WP[i], pSoilHorizons.AE_Pot[i], pSoilHorizons.B_Val[i])
        if pSoilHorizons.PWP_WC[i] <= 0: 
            pSoilHorizons.PWP_WC[i] = WC(pSoilHorizons.Sat_WC[i], pSoilHorizons.PWP_WP[i], pSoilHorizons.AE_Pot[i], pSoilHorizons.B_Val[i])
        pSoilHorizons.Number_Of_Sublayers[i] = int(pSoilHorizons.Horizon_Thickness[i] / Thickness_Model_Layers + 0.5)
    #'Distribute properties for each model layer of thickness 0.1 m
    Cum_J = 1
    for i in range(1, N_Horz+1):
        NL = pSoilHorizons.Number_Of_Sublayers[i]
        k = Cum_J
        L = (k + NL - 1)
        for j in range(k, L+1):
            pSoilModelLayer.Air_Entry_Potential[j] = pSoilHorizons.AE_Pot[i]
            pSoilModelLayer.B_value[j] = pSoilHorizons.B_Val[i]
            pSoilModelLayer.WP_At_FC[j] = pSoilHorizons.FC_WP[i]
            pSoilModelLayer.WP_At_PWP[j] = pSoilHorizons.PWP_WP[i]
            pSoilModelLayer.FC_Water_Content[j] = pSoilHorizons.FC_WC[i]
            pSoilModelLayer.PWP_Water_Content[j] = pSoilHorizons.PWP_WC[i]
            pSoilModelLayer.Plant_Available_Water_Content[j] = pSoilModelLayer.FC_Water_Content[j] - pSoilModelLayer.PWP_Water_Content[j]
            pSoilModelLayer.Bulk_Density[j] = pSoilHorizons.Bulk_Dens[i]
            pSoilModelLayer.Saturation_Water_Content[j] = pSoilHorizons.Sat_WC[i]
            pSoilModelLayer.Layer_Thickness[j] = Thickness_Model_Layers
        Cum_J = L + 1
    pSoilModelLayer.Number_Model_Layers = Cum_J - 1

def EquilibriumConcentration(Chemical_Mass, WC, DZ, BD, K, Q):
    WD = 1000 #'Water density (kg/m3)
    Gravimetric_WC = WC * WD / BD
    Chemical_Mass /= (DZ * BD)
    A = K * Gravimetric_WC
    B = K * Q + Gravimetric_WC - K * Chemical_Mass
    C = -Chemical_Mass
    return (-B + math.sqrt(B * B - 4 * A * C)) / (2 * A)

def WaterAndNTransport(DOY, pSoilModelLayer, pSoilState, NetIrrigationDepth, WaterNConc, 
                       Prec, Mineral_Fertilization_Rate, Nitrate_Fraction):
    #'This subroutine only transport nitrate N. Ammonium N only moves down the soil when transformed to nitrate
    Chem_Mass = dict()
    WC = dict()
    FC = dict()
    dz = dict()
    BD = dict()
    CO = dict()
    C = dict() #'Chemical concentration in the soil solution (kg/kg)
    WD = 1000  #'water density in kg/m3
    
    Drainage = 0 #'Initialize drainage flux
    Chemical_Leaching = 0
    #'Calculates initial soil water profile (kg/m2 or mm) and total chemical mass in the soil profile (kg/m2)
    Initial_Profile_Chemical_Mass = 0
    Initial_Soil_Water_Profile = 0
    Number_Of_Layers = pSoilModelLayer.Number_Model_Layers
    for Layer in range(1, Number_Of_Layers + 1):
        Chem_Mass[Layer] = pSoilState.Nitrate_N_Content[DOY][Layer]
        WC[Layer] = pSoilState.Water_Content[DOY][Layer]
        FC[Layer] = pSoilModelLayer.FC_Water_Content[Layer]
        dz[Layer] = pSoilModelLayer.Layer_Thickness[Layer]
        BD[Layer] = pSoilModelLayer.Bulk_Density[Layer]
        Initial_Soil_Water_Profile = Initial_Soil_Water_Profile + WC[Layer] * dz[Layer] * WD
        Initial_Profile_Chemical_Mass = Initial_Profile_Chemical_Mass + Chem_Mass[Layer]

    #'Find irrigation events
    NID = NetIrrigationDepth

    #'Find fertilization event. THIS WILL BE LATER IMPLEMENTED IN A FERTILIZATION SUB. NOTE: ONLY NITRATE N IS CONSIDERED HERE
    Nitrate_N_Fertilization = Mineral_Fertilization_Rate * (Nitrate_Fraction / 100) / 10000.0 #'Convert kg/ha to kg/m2
    Chem_Mass[1] += Nitrate_N_Fertilization #'Mineral fertilizer added to the top layer

    Water_Flux_In = NID + Prec
    Irrig_Chemical_Conc = WaterNConc
    Precip_Chemical_Conc = 0
    Water_Chemical_Concentration = 0
    if Water_Flux_In > 0: Water_Chemical_Concentration = (Irrig_Chemical_Conc * NID + Precip_Chemical_Conc * Prec) / Water_Flux_In
    
    Number_Of_Pulses = 0  #CHECK!!!
    
    #'Calculate pore volume equivalent of each water pulse
    
    if Number_Of_Pulses == 0:
        Water_Depth_Equivalent_Of_One_Pore_Volume = WD * dz[2] * FC[2]
        Number_Of_Pulses = 1 + int(Water_Flux_In / (0.2 * Water_Depth_Equivalent_Of_One_Pore_Volume))

    #k & Q !!!
    k = 0
    Q = 0
    
    for i in range(1, Number_Of_Pulses + 1):
        Win = Water_Flux_In / Number_Of_Pulses
        Conc_In = Water_Chemical_Concentration
        #'Equilibrate soil solution
        if (k > 0) and (Q > 0):
            for j in range(1, Number_Of_Layers + 1):
                C[j] = EquilibriumConcentration(Chem_Mass[j], WC[j], dz[j], BD[j], k, Q)
        else:
            for j in range(1, Number_Of_Layers + 1):
                C[j] = Chem_Mass[j] / (dz[j] * WC[j] * WD)

        j = 1
        Wout = 0
        Conc_Out = 0
        while (j <= Number_Of_Layers) and (Win > 0): #'infiltration calculation
            Original_Water_Depth = dz[j] * WD * WC[j]
            Water_Depth_To_Reach_Field_Capacity = (FC[j] - WC[j]) * dz[j] * WD
            #'Determine water and chemical transport
            if Win > Water_Depth_To_Reach_Field_Capacity: 
                Wout = Win - Water_Depth_To_Reach_Field_Capacity
                if Wout <= Original_Water_Depth:
                    Conc_Out = C[j]
                else:
                    Conc_Out = (Original_Water_Depth * C[j] + (Wout - Original_Water_Depth) * Conc_In) / Wout
              
                WC[j] = FC[j]
            else:
                Wout = 0
                Conc_Out = 0
                WC[j] = WC[j] + Win / (WD * dz[j])
            Mass_change = Win * Conc_In - Wout * Conc_Out
            if Mass_change < 0 and abs(Mass_change) > Chem_Mass[j]: 
                Mass_change = -Chem_Mass[j]
                Conc_Out = (Win * Conc_In - Mass_change) / Wout
                Chem_Mass[j] = 0
            else:
                Chem_Mass[j] = Chem_Mass[j] + Mass_change
            
            Win = Wout
            Conc_In = Conc_Out
            j += 1
        Drainage += Wout     #'in mm/day = kg/m2/day
        Chemical_Leaching = Chemical_Leaching + Wout * Conc_Out
    #'Calculates Final total chemical mass in the soil profile (kg/m2)
    Final_Profile_Chemical_Mass = 0
    for L in range(1, Number_Of_Layers + 1):
        Final_Profile_Chemical_Mass += Chem_Mass[L]
    pSoilState.Chemical_Balance[DOY] = (Initial_Profile_Chemical_Mass + Water_Flux_In * Water_Chemical_Concentration + Nitrate_N_Fertilization \
               - (Final_Profile_Chemical_Mass + Chemical_Leaching)) * 10000 #'Convert kg/m2 to kg/ha
    #'Calculates final soil water profile (kg/m2 or mm)
    Final_Soil_Water_Profile = 0
    for L in range(1, Number_Of_Layers + 1):
        Final_Soil_Water_Profile += WC[L] * dz[L] * WD
    pSoilState.Water_Balance[DOY] = (Initial_Soil_Water_Profile + Water_Flux_In - (Final_Soil_Water_Profile + Drainage))
    #'Update water and nitrate content
    for Layer in range(1, Number_Of_Layers + 1):
        pSoilState.Water_Content[DOY + 1][Layer] = WC[Layer]
        pSoilState.Nitrate_N_Content[DOY + 1][Layer] = Chem_Mass[Layer]
        pSoilState.N_Leaching[DOY] = pSoilState.N_Leaching[DOY - 1] + Chemical_Leaching * 10000 #'Convert kg/m2 to kg/ha
        pSoilState.Deep_Drainage[DOY] = pSoilState.Deep_Drainage[DOY - 1] + Drainage #'mm

    pSoilState.Cumulative_Deep_Drainage += Drainage
    pSoilState.Cumulative_N_Leaching += Chemical_Leaching * 10000 #'Convert kg/m2 to kg/ha

