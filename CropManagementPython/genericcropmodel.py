# -*- coding: utf-8 -*-
"""GenericCropModel.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Io0j9qcpO7kWG9r5ONyaeye23PHAP-wM
"""

import math

def B(CCI, CCF, RTT_Half_CC):
    Numerator = (CCF - CCI) / (0.5 * CCF - 1.5 * CCI) - 1
    B = Numerator / math.exp(-10 * RTT_Half_CC)
    return B

def BS(CCmax, CCmat):
    Numerator = (CCmat - CCmax) / (CCmat - 0.5) + 1
    BS = Numerator / math.exp(-10 * 0.5)
    return BS

def CC(B, BS, CCinit, CCmax, CCmaturity, CurrentCC, Relative_Thermal_Time, Cumulative_Thermal_Time,
    Thermal_Time_End_Vegetative_Growth, Thermal_Time_Beginning_Senescence, Thermal_Time_Maturity):
    if Cumulative_Thermal_Time <= Thermal_Time_End_Vegetative_Growth:
        CC = CCinit + (CCmax - CCinit) / (1 + B * math.exp(-10 * Relative_Thermal_Time))
    else:
        if Cumulative_Thermal_Time < Thermal_Time_Maturity and Cumulative_Thermal_Time >= Thermal_Time_Beginning_Senescence:
            Rel_TT_Senescence = (Cumulative_Thermal_Time - Thermal_Time_Beginning_Senescence) / (Thermal_Time_Maturity - Thermal_Time_Beginning_Senescence)
            CC = CCmax + (CCmaturity - CCmax) / (1 + BS * math.exp(-10 * Rel_TT_Senescence))
            if CC < CCmaturity: CC = CCmaturity
        else:
            CC = CurrentCC
    return CC

def TR(Altitude, Screening_Height, Wind, tmean,
    VPD, gc_at_zero_VPD, VPD_Sensitivity, gcmax):
    rco = 0.00081 #'day/m
    VK = 0.41
    if Screening_Height == 2:
      U2 = Wind
    else:
      U2 = Wind * (4.87 / (math.log(67.8 * Screening_Height - 5.42)))
    U2 = U2 * 86400 #'Convert to m/day
    d = 0.08
    zom = 0.01476
    zoh = 0.001476
    Zm = 2
    zh = 2

    Term1 = math.log((Zm - d) / zom)
    Term2 = math.log((zh - d) / zoh)
    Aero_Res = Term1 * Term2 / (VK * VK * U2)
    #'******** Calculate delta
    Es_Tmean = 0.6108 * math.exp(17.27 * tmean / (tmean + 237.3))
    Slope_Sat_FN = 4098 * Es_Tmean / math.pow((tmean + 237.3),2)
    #'******** Calculate lambda
    Latent_Heat_Vap = 2.501 - 0.002361 * tmean
    #'******** Calculate psychrometric constant
    CP = 0.001013
    P = 101.3 * math.pow(((293 - 0.0065 * Altitude) / 293),5.26)
    Psychrometric_Constant = CP * P / (0.622 * Latent_Heat_Vap)

    Increase_Factor = gcmax * (1 + VPD / VPD_Sensitivity) / gc_at_zero_VPD
    if Increase_Factor < 1.0: Increase_Factor = 1.0
    Numerator = (Slope_Sat_FN + Psychrometric_Constant * (1 + rco / Aero_Res))
    Denominator = (Slope_Sat_FN + Psychrometric_Constant * (1 + rco * Increase_Factor / Aero_Res))
    TR = Numerator / Denominator
    return TR

def PMET(DOY, Lat, Altitude, Screening_Height, Tmax, Tmin,
    SRad, RHmax, RHmin, Wind):
    rc = 0.00081 #'day/m

    #'******** Calculate vapor pressure deficit
    tmean = (Tmax + Tmin) / 2
    Es_Tmean = 0.6108 * math.exp(17.27 * tmean / (tmean + 237.3))
    Es_Tmax = 0.6108 * math.exp(17.27 * Tmax / (Tmax + 237.3))
    Es_Tmin = 0.6108 * math.exp(17.27 * Tmin / (Tmin + 237.3))
    Actual_VP = (Es_Tmin * RHmax / 100 + Es_Tmax * RHmin / 100) / 2
    Vap_Pres_Def = (Es_Tmax + Es_Tmin) / 2 - Actual_VP
    #'******** Calculate extraterrestrial radiation
    pi = 3.14159
    Solar_Constant = 118.08
    Lat_Rad = Lat * pi / 180
    DR = 1 + 0.033 * math.cos(2 * pi * DOY / 365)
    SolDec = 0.409 * math.sin(2 * pi * DOY / 365 - 1.39)
    x = -math.tan(Lat_Rad) * math.tan(SolDec)
    SunsetHourAngle = math.atn(-x / math.sqrt(-x * x + 1)) + 2 * math.atn(1)
    #'SunsetHourAngle = f_arccos(-Tan(Lat_Rad) * Tan(SolDec))
    Term = SunsetHourAngle * math.sin(Lat_Rad) * math.sin(SolDec) + math.cos(Lat_Rad) * math.cos(SolDec) * math.sin(SunsetHourAngle)
    Pot_Rad = Solar_Constant * DR * Term / pi
    #'******** Calculate net radiation
    Albedo = 0.23
    Rns = (1 - Albedo) * SRad
    #'Calculate cloud factor
    F_Cloud = 1.35 * (SRad / (Pot_Rad * 0.75)) - 0.35
    #'Calculate humidity factor
    F_Hum = (0.34 - 0.14 * math.sqrt(Actual_VP))
    #'Calculate Isothermal LW net radiation
    LWR = 0.000000004903 * ((Tmax + 273) ^ 4 + (Tmin + 273) ^ 4) / 2
    Rnl = LWR * F_Cloud * F_Hum
    #'Calculate Rn
    Net_Rad = Rns - Rnl
    #'******** Calculate aerodynamic resistance
    VK = 0.41
    if Screening_Height == 2:
        U2 = Wind
    else:
        U2 = Wind * (4.87 / (math.log(67.8 * Screening_Height - 5.42)))
    U2 = U2 * 86400 #'Convert to m/day
    d = 0.08
    zom = 0.01476
    zoh = 0.001476
    Zm = 2
    zh = 2
    Term1 = math.log((Zm - d) / zom)
    Term2 = math.log((zh - d) / zoh)
    Aero_Res = Term1 * Term2 / (VK * VK * U2)
    #'******** Calculate delta
    Slope_Sat_FN = 4098 * Es_Tmean / math.pow((tmean + 237.3),2)
    #'******** Calculate lambda
    Latent_Heat_Vap = 2.501 - 0.002361 * tmean
    #'******** Calculate psychrometric constant
    CP = 0.001013
    P = 101.3 * math.pow(((293 - 0.0065 * Altitude) / 293),5.26)
    Psychrometric_Constant = CP * P / (0.622 * Latent_Heat_Vap)
    #'******** Calculate aerodynamic term
    Tkv = 1.01 * (tmean + 273)
    AirDensity = 3.486 * P / Tkv
    VolHeatCap = CP * AirDensity
    Aero_Term = (VolHeatCap * Vap_Pres_Def / Aero_Res) / (Slope_Sat_FN + Psychrometric_Constant * (1 + rc / Aero_Res))
    #'******** Calculate radiation term
    Rad_Term = Slope_Sat_FN * Net_Rad / (Slope_Sat_FN + Psychrometric_Constant * (1 + rc / Aero_Res))
    #'******** Calculate PMET
    PMET = (Aero_Term + Rad_Term) / Latent_Heat_Vap
    return PMET
