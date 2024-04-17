#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:24:57 2024
For CropManagement 
@author: liuming
"""
import math

def GetSoilWaterPotential(
        BD, AirEntryPot, Campbell_b, WC):
    SaturationWC = 1 - BD / 2.65
    WatPot = AirEntryPot * pow(WC / SaturationWC, -Campbell_b)
    return WatPot

def GetSoilWaterContent(
        BD, AirEntryPot, Campbell_b, WatPot):
    SaturationWC = 1 - BD / 2.65
    WC = SaturationWC * pow(WatPot / AirEntryPot, -1 / Campbell_b)
    return WC

def GetPlantAvailableWater(
        BD, AirEntryPot, Campbell_b, WC,
        WatPotFC, WatPotPWP):
    SaturationWC = 1 - BD / 2.65
    WC_FC = SaturationWC * pow(WatPotFC / AirEntryPot, -1 / Campbell_b)
    WC_PWP = SaturationWC * pow(WatPotPWP / AirEntryPot, -1 / Campbell_b)
    PAW = (WC - WC_PWP) / (WC_FC - WC_PWP)
    if PAW > 1:
        PAW = 1
    elif PAW < 0:
        PAW = 0
    return PAW

def GetWaterPotentialAtFieldCapacity(Clay):
    WPFC = 10.356 - 13.83 * math.log(Clay)
    return WPFC
