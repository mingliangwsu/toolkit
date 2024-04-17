#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 13:34:46 2024

@author: liuming
"""
import math
import sys
if 'SoilConfig' not in sys.modules:
    import SoilConfig

def CascadeInfiltrationPlusSolute(Number_Of_Layers, Water_Flux_In,
        K, Q, Chem_Conc_Irrigation,
        Number_Of_Pulses):
    #CO = dict()
    C = dict() #'Chemical concentration in the soil solution (kg/kg)
    #WD = 1000  #'water density in kg/m3
    SoilConfig.Drainage = 0 #'Initialize drainage flux
    SoilConfig.Chemical_Leaching = 0
   #'Calculates initial soil water profile (kg/m2 or mm) and total chemical mass in the soil profile (kg/m2)
    Initial_Profile_Chemical_Mass = 0
    Initial_Soil_Water_Profile = 0
    for L in range(1, Number_Of_Layers+1):
        Initial_Soil_Water_Profile += (SoilConfig.WC[L] 
                                       * SoilConfig.DZ[L] 
                                       * SoilConfig.WD)
        Initial_Profile_Chemical_Mass += SoilConfig.Chem_Mass[L]
    #'Calculate pore volume equivalent of each water pulse
    if Number_Of_Pulses == 0:
        Water_Depth_Equivalent_Of_One_Pore_Volume = (SoilConfig.WD 
                                                     * SoilConfig.DZ[2] 
                                                     * SoilConfig.FC[2])
        #print(f'Water_Flux_In:{Water_Flux_In} wd:{Water_Depth_Equivalent_Of_One_Pore_Volume}')
        Number_Of_Pulses = 1 + int(Water_Flux_In 
                           / (0.2 * Water_Depth_Equivalent_Of_One_Pore_Volume))
    
    for i in range(1, Number_Of_Pulses+1):
        Win = Water_Flux_In / Number_Of_Pulses
        Conc_In = Chem_Conc_Irrigation #'Chemical concentration in irrigation water (kg/kg)
        #'Equilibrate soil solution
        if (K > 0) and (Q > 0):
            for j in range(1, Number_Of_Layers+1):
                C[j] = EquilibriumConcentration(SoilConfig.Chem_Mass[j], 
                                                SoilConfig.WC[j], 
                                                SoilConfig.DZ[j], 
                                                SoilConfig.BD[j], 
                                                K, 
                                                Q)
        else:
            for j in range(1, Number_Of_Layers+1):
                C[j] = (SoilConfig.Chem_Mass[j] 
                        / (SoilConfig.DZ[j] 
                           * SoilConfig.WC[j] 
                           * SoilConfig.WD))
        j = 1
        while (j <= Number_Of_Layers) and (Win > 0): #'infiltration calculation
            #print(f'j:{j} Win:{Win}\n')
            Original_Water_Depth = (SoilConfig.DZ[j] 
                                    * SoilConfig.WD 
                                    * SoilConfig.WC[j])
            Water_Depth_To_Reach_Field_Capacity = ((SoilConfig.FC[j] 
                                                    - SoilConfig.WC[j]) 
                                                   * SoilConfig.DZ[j] 
                                                   * SoilConfig.WD)
            #'Determine water and chemical transport
            if Win > Water_Depth_To_Reach_Field_Capacity:
                Wout = Win - Water_Depth_To_Reach_Field_Capacity
                if Wout <= Original_Water_Depth:
                    Conc_Out = C[j]
                else:
                    Conc_Out = ((Original_Water_Depth * C[j] 
                                + (Wout - Original_Water_Depth) 
                                * Conc_In
                                ) / Wout)
                SoilConfig.WC[j] = SoilConfig.FC[j]
            else:
                Wout = 0
                Conc_Out = 0
                SoilConfig.WC[j] += Win / (SoilConfig.WD * SoilConfig.DZ[j])
            Mass_change = Win * Conc_In - Wout * Conc_Out
            if Mass_change < 0 and abs(Mass_change) > SoilConfig.Chem_Mass[j]:
                Mass_change = -SoilConfig.Chem_Mass[j]
                Conc_Out = (Win * Conc_In - Mass_change) / Wout
                SoilConfig.Chem_Mass[j] = 0
            else:
                SoilConfig.Chem_Mass[j] += Mass_change
         
            Win = Wout
            Conc_In = Conc_Out
            j += 1
        SoilConfig.Drainage += Wout     #'in mm/day = kg/m2/day
        SoilConfig.Chemical_Leaching += Wout * Conc_Out
        #'Next pulse
    #'Calculates Final total chemical mass in the soil profile (kg/m2)
    Final_Profile_Chemical_Mass = 0
    for L in range(1, Number_Of_Layers+1):
        Final_Profile_Chemical_Mass += SoilConfig.Chem_Mass[L]
    SoilConfig.Chemical_Balance += ((Initial_Profile_Chemical_Mass 
                                     + Water_Flux_In * Chem_Conc_Irrigation 
                                     - (Final_Profile_Chemical_Mass 
                                     + SoilConfig.Chemical_Leaching))
                                    * 10000) #'transform kg/m2 to kg/ha
    #'Calculates final soil water profile (kg/m2 or mm)
    Final_Soil_Water_Profile = 0
    for L in range(1, Number_Of_Layers+1):
        Final_Soil_Water_Profile += (SoilConfig.WC[L] 
                                     * SoilConfig.DZ[L] 
                                     * SoilConfig.WD)
    SoilConfig.Water_Balance += (Initial_Soil_Water_Profile 
                                 + Water_Flux_In 
                                 - (Final_Soil_Water_Profile 
                                    + SoilConfig.Drainage))
    
def EquilibriumConcentration(Chemical_Mass, WC, DZ, 
        BD, K, Q):
    WD = 1000 #'Water density (kg/m3)
    Gravimetric_WC = WC * WD / BD
    Chemical_Mass /= (DZ * BD)
    A = K * Gravimetric_WC
    B = K * Q + Gravimetric_WC - K * Chemical_Mass
    C = -Chemical_Mass
    return (-B + math.sqrt(B * B - 4 * A * C)) / (2 * A)
