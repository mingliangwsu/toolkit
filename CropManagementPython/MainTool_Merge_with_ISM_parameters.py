#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 6 2024

@author: liuming
"""
import pandas as pd
#import WaterUptakeConfig as Soil
from ExcelDataframeExchange import *
#from CropWaterUptakeClass import *
#from SoilWater import *
from CropParameter import *
from SoilHydrolics import *
from Crop import *
#from canopycover import *
#from CS_ET import *
from accessagweathernet import *
from ism_default_parameters import *
import datetime
from accessssurgo_functions import *
from Balances import *
from AutoIrrigation import *
from OrganicCandN import *

import sys

def is_blank(s):
    return not s or not s.strip()

def mm_to_inch(mm):
    return mm / 25.4  # 1 inch = 25.4 mm

def KgPerSquareMeter_to_KgPerHa(kg_m2):
    return kg_m2 * 10000.0

class CS_Weather:
    Solar_Radiation = dict()                                                   #MJ/m2
    Tmax = dict()                                                              #Celsius degree
    Tmin = dict()
    RHmax = dict()                                                             #%
    RHmin = dict()
    Wind_Speed = dict()                                                        #m/s
    Precipitation = dict()                                                     #mm
    FAO_ETo = dict()                                                           #mm
class CS_Fertilization:
    Fertilization_DOY = dict()
    Mineral_Fertilizer_Name = dict()
    Mineral_Fertilization_Rate = dict()
    Nitrate_Fraction = dict()
    Ammonium_Fraction = dict()
    Ammonia_Fraction = dict()
    Nitrate_Fertilization_Rate = dict()
    Ammonium_Fertilization_Rate = dict()
    Organic_Fertilizer_Name = dict()
    Organic_Fertilizer_Rate = dict()
    Organic_Fertilizer_C_Fraction = dict()
    Organic_Fertilizer_N_Fraction = dict()
    Application_Method_Number = dict()
    
    #and others

def InitFertilization(pCS_Fertilization):
    for i in range(1,367):
        pCS_Fertilization.Fertilization_DOY[i] = i
        pCS_Fertilization.Mineral_Fertilizer_Name[i] = ''
        pCS_Fertilization.Mineral_Fertilization_Rate[i] = 0.
        pCS_Fertilization.Nitrate_Fraction[i] = 0.
        pCS_Fertilization.Ammonium_Fraction[i] = 0.
        pCS_Fertilization.Ammonia_Fraction[i] = 0.
        pCS_Fertilization.Nitrate_Fertilization_Rate[i] = 0.
        pCS_Fertilization.Ammonium_Fertilization_Rate[i] = 0.
        pCS_Fertilization.Organic_Fertilizer_Name[i] = ''
        pCS_Fertilization.Organic_Fertilizer_Rate[i] = 0.
        pCS_Fertilization.Organic_Fertilizer_C_Fraction[i] = 0.
        pCS_Fertilization.Organic_Fertilizer_N_Fraction[i] = 0.
        pCS_Fertilization.Application_Method_Number[i] = 0

def ReadCropParameters(Cells,Crop,col_letter):
    Crop.Crop_Name = get_excel_value(Cells,f'{col_letter}3')
    Crop.Midseason_Crop_Coefficient = float(get_excel_value(Cells,f'{col_letter}5'))
    Crop.Maximum_Crop_Water_Uptake = float(get_excel_value(Cells,f'{col_letter}6'))
    Crop.LWP_Onset_Stomatal_Closure = float(get_excel_value(Cells,f'{col_letter}7'))
    Crop.LWP_Permanent_Wilting = float(get_excel_value(Cells,f'{col_letter}8'))
    Crop.Seeding_Depth = float(get_excel_value(Cells,f'{col_letter}9'))
    Crop.Initial_Root_Depth_From_Germinated_Seed = float(get_excel_value(Cells,f'{col_letter}10'))
    Crop.Maximum_Root_Depth = float(get_excel_value(Cells,f'{col_letter}11'))
    Crop.Maximum_Crop_Height = float(get_excel_value(Cells,f'{col_letter}12'))
    Crop.Initial_Green_Canopy_Cover = float(get_excel_value(Cells,f'{col_letter}14'))
    Crop.Maximum_Green_Canopy_Cover = float(get_excel_value(Cells,f'{col_letter}15'))
    Crop.Maturity_Green_Canopy_Cover = float(get_excel_value(Cells,f'{col_letter}16'))
    Crop.Transpiration_Use_Efficiency_1_kPa = float(get_excel_value(Cells,f'{col_letter}18'))
    Crop.Slope_Daytime_VPD_Function = float(get_excel_value(Cells,f'{col_letter}19'))
    Crop.Maximum_N_Concentration_Emergence = float(get_excel_value(Cells,f'{col_letter}21'))
    Crop.Critical_N_Concentration_Emergence = float(get_excel_value(Cells,f'{col_letter}22'))
    Crop.Minimum_N_Concentration_Emergence = float(get_excel_value(Cells,f'{col_letter}23'))
    Crop.Biomass_Start_Dilution_Maximum_N_Concentration = float(get_excel_value(Cells,f'{col_letter}24'))
    Crop.Biomass_Start_Dilution_Critical_N_Concentration = float(get_excel_value(Cells,f'{col_letter}25'))
    Crop.Biomass_Start_Dilution_Minimum_N_Concentration = float(get_excel_value(Cells,f'{col_letter}26'))
    Crop.N_Dilution_Slope = float(get_excel_value(Cells,f'{col_letter}27'))
    Crop.Maximum_N_Concentration_Maturity = float(get_excel_value(Cells,f'{col_letter}28'))
    Crop.Critical_N_Concentration_Maturity = float(get_excel_value(Cells,f'{col_letter}29'))
    Crop.Minimum_N_Concentration_Maturity = float(get_excel_value(Cells,f'{col_letter}30'))
    #Crop.Potential_N_Uptake = float(get_excel_value(Cells,f'{col_letter}31'))
def ReadSoilHorizonParamegters(Cells,pSoilHorizen):
    #'Soil description
    pSoilHorizen.Number_Of_Horizons = int(get_excel_value(Cells,'A17'))
    for i in range(1, pSoilHorizen.Number_Of_Horizons+1):
        pSoilHorizen.Horizon_Thickness[i] = float(Cells.iloc[22 + i - 1, 3 - 1]) #round(float(Cells.iloc[22 + i - 1, 3 - 1]),1) #'Thickness is rounded to one decimal
        pSoilHorizen.Clay[i] = float(Cells.iloc[22 + i - 1, 4 - 1])
        pSoilHorizen.Silt[i] = float(Cells.iloc[22 + i - 1, 5 - 1])
        pSoilHorizen.Sand[i] = float(Cells.iloc[22 + i - 1, 6 - 1])
        pSoilHorizen.FC_WC[i] = float(Cells.iloc[22 + i - 1, 7 - 1])
        pSoilHorizen.PWP_WC[i] = float(Cells.iloc[22 + i - 1, 8 - 1])
        #pSoilHorizen.Soil_Organic_Carbon[i] = float(Cells.iloc[22 + i - 1, 9 - 1])
        pSoilHorizen.Percent_Soil_Organic_Matter[i] = float(Cells.iloc[22 + i - 1, 9 - 1])
def GetSoilHorizonParamegtersFromSSURGO(df_SSURGO,pSoilHorizen):
    #'Soil description
    pSoilHorizen.Number_Of_Horizons = df_SSURGO.shape[0]
    for i in range(1, pSoilHorizen.Number_Of_Horizons+1):
        t = df_SSURGO.loc[i-1,'hzdept_r']                                        #cm
        b = df_SSURGO.loc[i-1,'hzdepb_r']                                        #cm
        pSoilHorizen.Horizon_Thickness[i] = round((b - t) / 100.0,1)           #'Thickness is rounded to one decimal
        pSoilHorizen.Clay[i] = float(df_SSURGO.loc[i-1, 'claytotal_r'])
        pSoilHorizen.Silt[i] = float(df_SSURGO.loc[i-1, 'silttotal_r'])
        pSoilHorizen.Sand[i] = float(df_SSURGO.loc[i-1, 'sandtotal_r'])
        pSoilHorizen.FC_WP[i] = -33.0 #kPa
        if is_blank(df_SSURGO.loc[i-1, 'wthirdbar_r']):
            pSoilHorizen.FC_WC[i] = -9999.0
        else:
            pSoilHorizen.FC_WC[i] = float(df_SSURGO.loc[i-1, 'wthirdbar_r']) / 100.0
        pSoilHorizen.PWP_WP[i] = -1500.0 #kPa
        if is_blank(df_SSURGO.loc[i-1, 'wfifteenbar_r']):
            pSoilHorizen.PWP_WC[i] = -9999.0
        else:
            pSoilHorizen.PWP_WC[i] = float(df_SSURGO.loc[i-1, 'wfifteenbar_r']) / 100.0
        if is_blank(df_SSURGO.loc[i-1, 'wsatiated_r']):
            pSoilHorizen.Sat_WC[i] = -9999.0
        else:
            pSoilHorizen.Sat_WC[i] = float(df_SSURGO.loc[i-1, 'wsatiated_r']) / 100.0
        if is_blank(df_SSURGO.loc[i-1, 'om_r']):
            pSoilHorizen.Soil_Organic_Carbon[i] = 0.0
            pSoilHorizen.Percent_Soil_Organic_Matter[i] = 0.0
        else:
            pSoilHorizen.Soil_Organic_Carbon[i] = float(df_SSURGO.loc[i-1, 'om_r'])
            pSoilHorizen.Percent_Soil_Organic_Matter[i] = pSoilHorizen.Soil_Organic_Carbon[i]
        if is_blank(df_SSURGO.loc[i-1, 'dbthirdbar_r']):
            pSoilHorizen.Bulk_Dens[i] = -9999.0
        else:
            pSoilHorizen.Bulk_Dens[i] = float(df_SSURGO.loc[i-1, 'dbthirdbar_r'])
def ReadCropGrowth(Cells,pCropGrowth,row_idx):
    #'Soil description
    pCropGrowth.Crop_Name = get_excel_value(Cells,f'A{row_idx}')
    pCropGrowth.Expected_Yield = float(get_excel_value(Cells,f'H{row_idx}'))
    pCropGrowth.Planting_DOY = int(get_excel_value(Cells,f'I{row_idx}'))
    pCropGrowth.Emergence_DOY = int(get_excel_value(Cells,f'J{row_idx}'))
    pCropGrowth.Full_Canopy_DOY = int(get_excel_value(Cells,f'K{row_idx}'))
    pCropGrowth.Beging_Senescence_DOY = int(get_excel_value(Cells,f'L{row_idx}'))
    pCropGrowth.Maturity_DOY = int(get_excel_value(Cells,f'M{row_idx}'))
    pCropGrowth.Harvest_DOY = int(get_excel_value(Cells,f'N{row_idx}'))
    #'Calculate days after emergence for maturity and harvest
    if pCropGrowth.Emergence_DOY > pCropGrowth.Maturity_DOY:
        pCropGrowth.Maturity_DAE = (365 - pCropGrowth.Emergence_DOY) + pCropGrowth.Maturity_DOY 
    else:
        pCropGrowth.Maturity_DAE = pCropGrowth.Maturity_DOY - pCropGrowth.Emergence_DOY
        
    if pCropGrowth.Emergence_DOY > pCropGrowth.Harvest_DOY:
        pCropGrowth.Harvest_DAE = (365 - pCropGrowth.Emergence_DOY) + pCropGrowth.Harvest_DOY 
    else:
        pCropGrowth.Harvest_DAE = pCropGrowth.Harvest_DOY - pCropGrowth.Emergence_DOY
    
def GetISMCropGrowthDOYParameters(agWeatherStationID,ISM_cropname,pCropGrowth):
    if int(agWeatherStationID) in stationregion.index:
        cropRegionCode = stationregion.loc[int(agWeatherStationID)]['regionID']
    else:
        print(f'{agWeatherStationID} is not in stationRegion Table, set region as default\n')
        cropRegionCode = 720 #default
    ISM_cropInfo = cropparameter.loc[ISM_cropname][cropparameter.loc[ISM_cropname,'cropRegion'] == cropRegionCode].squeeze()
    pCropGrowth.Crop_Name = ISM_cropname
    #pCropGrowth.Expected_Yield = 
    pCropGrowth.Planting_DOY = int(ISM_cropInfo['plantDate']) - 10
    pCropGrowth.Emergence_DOY = int(ISM_cropInfo['plantDate'])
    pCropGrowth.Full_Canopy_DOY = int(ISM_cropInfo['growthMaxDate'])
    pCropGrowth.Beging_Senescence_DOY = int(ISM_cropInfo['growthDeclineDate'])
    pCropGrowth.Maturity_DOY = int(ISM_cropInfo['growthEndDate'])
    #pCropGrowth.Harvest_DOY = int(ISM_cropInfo['plantDate'])
    
def ReadFertilization(Cells,pCS_Fertilization):
    start_row_idx = 46 - 1
    end_row_idx = 50 - 1
    for i in range(start_row_idx, end_row_idx + 1):
        doy = get_cell_int(Cells.iloc[i, 2 - 1])
        if doy > 0:
            pCS_Fertilization.Fertilization_DOY[doy] = doy
            pCS_Fertilization.Mineral_Fertilizer_Name[doy] = Cells.iloc[i, 3 - 1]
            pCS_Fertilization.Mineral_Fertilization_Rate[doy] = get_cell_float(Cells.iloc[i, 4 - 1])
            pCS_Fertilization.Nitrate_Fraction[doy] = get_cell_float(Cells.iloc[i, 5 - 1])
            pCS_Fertilization.Ammonium_Fraction[doy] = get_cell_float(Cells.iloc[i, 6 - 1])
            pCS_Fertilization.Ammonia_Fraction[doy] = get_cell_float(Cells.iloc[i, 7 - 1])
            #'Store fertilization rates in kg/m2
            pCS_Fertilization.Nitrate_Fertilization_Rate[doy] = (pCS_Fertilization.Mineral_Fertilization_Rate[doy] * pCS_Fertilization.Nitrate_Fraction[doy] / 100.) / 10000. # 'Convert kg/ha to kg/m2
            pCS_Fertilization.Ammonium_Fertilization_Rate[doy] = (pCS_Fertilization.Mineral_Fertilization_Rate[doy] * (pCS_Fertilization.Ammonium_Fraction[doy] + pCS_Fertilization.Ammonia_Fraction[doy]) / 100.) / 10000. # 'Convert kg/ha to kg/m2
            pCS_Fertilization.Organic_Fertilizer_Name[doy] = get_cell_float(Cells.iloc[i, 8 - 1])
            pCS_Fertilization.Organic_Fertilizer_Rate[doy] = get_cell_float(Cells.iloc[i, 9 - 1])
            pCS_Fertilization.Organic_Fertilizer_C_Fraction[doy] = get_cell_float(Cells.iloc[i, 10 - 1])
            pCS_Fertilization.Organic_Fertilizer_N_Fraction[doy] = get_cell_float(Cells.iloc[i, 11 - 1])
            pCS_Fertilization.Application_Method_Number[doy] = get_cell_int(Cells.iloc[i, 12 - 1])
        
def ReadNetIrrigation(Cells,Irrigation):
    start_row_idx = 58 - 1
    DOY_Last_Scheduled_Irrigation = 0
    for i in range(1, 10):
        doy = get_cell_int(Cells.iloc[start_row_idx + i - 1, 2 - 1])
        if doy > 0:
            Irrigation[doy] = get_cell_float(Cells.iloc[start_row_idx + i - 1, 3 - 1])      #mm
            DOY_Last_Scheduled_Irrigation = doy
    return DOY_Last_Scheduled_Irrigation

def ReadWeather(Cells,pCS_Weather):
    start_row_idx = 74 - 1
    end_row_idx = 438 - 1
    for i in range(start_row_idx, end_row_idx + 1):
        doy = get_cell_int(Cells.iloc[i, 2 - 1])
        if doy > 0:
            pCS_Weather.Solar_Radiation[doy] = float(Cells.iloc[i, 3 - 1])
            pCS_Weather.Tmax[doy] = float(Cells.iloc[i, 4 - 1])
            pCS_Weather.Tmin[doy] = float(Cells.iloc[i, 5 - 1])
            pCS_Weather.RHmax[doy] = float(Cells.iloc[i, 6 - 1])
            pCS_Weather.RHmin[doy] = float(Cells.iloc[i, 7 - 1])
            pCS_Weather.Wind_Speed[doy] = float(Cells.iloc[i, 8 - 1])
            pCS_Weather.Precipitation[doy] = float(Cells.iloc[i, 9 - 1])
            pCS_Weather.FAO_ETo[doy] = float(Cells.iloc[i, 10 - 1])
        
        
def U2WindSpeed(ws_m_s,AnemomH_m):
    return ws_m_s * 4.87 / (math.log(67.8 * AnemomH_m - 5.42))
def GetAgWeatherNetDailyWeather(stationid,AnemomH_m,styear,stdoy,edyear, eddoy,pCS_Weather):
    #get agWeather daily climate data
    sy,sm,sd = get_date_from_YDOY(styear,stdoy)
    ey,em,ed = get_date_from_YDOY(edyear,eddoy)
    start_date = f'{sy}-{sm:02}-{sd:02}'
    end_date = f'{ey}-{em:02}-{ed:02}'
    data = fetch_AgWeatherNet_data(stationid,start_date,end_date,True)
    numdays = (datetime.date(ey,em,ed) - datetime.date(sy,sm,sd)).days + 1
    good_data = True
    validadays = 0
    if data.shape[0] == numdays:
        for index, row in data.iterrows():
            if (row['JULDATE_PST'] != "" and
                not math.isnan(row['SR_MJM2']) and
                not math.isnan(row['MAX_AT_F']) and
                not math.isnan(row['MIN_AT_F']) and
                not math.isnan(row['MAX_REL_HUMIDITY']) and
                not math.isnan(row['MIN_REL_HUMIDITY']) and
                not math.isnan(row['P_INCHES']) and
                not math.isnan(row['ETO'])):
                    tdate = datetime.datetime.strptime(row['JULDATE_PST'], "%Y-%m-%d").date()
                    day_of_year = tdate.timetuple().tm_yday
                    #print(f"{index} {row['JULDATE_PST']} {day_of_year}")
                    doy = int(day_of_year)
                    pCS_Weather.Solar_Radiation[doy] = row['SR_MJM2']
                    pCS_Weather.Tmax[doy] = fahrenheit_to_celsius(row['MAX_AT_F'])
                    pCS_Weather.Tmin[doy] = fahrenheit_to_celsius(row['MIN_AT_F'])
                    pCS_Weather.RHmax[doy] = row['MAX_REL_HUMIDITY']
                    pCS_Weather.RHmin[doy] = row['MIN_REL_HUMIDITY']
                    pCS_Weather.Wind_Speed[doy] = row['WS_MPH'] * 0.44704                  #MPH to m/s
                    pCS_Weather.Precipitation[doy] = row['P_INCHES'] * 25.4                #inch to mm
                    pCS_Weather.FAO_ETo[doy] = row['ETO'] * 25.4                           #inch to mm
                    validadays += 1
            else:
                good_data = False
                print(f'Error: {tdate.year}/{tdate.month}/{tdate.day} has NaN value!')
        if validadays < numdays:
            missing_days = numdays - validadays
            good_data = False
            print(f'Error: {missing_days} days missing climate data\n')
    else:
        good_data = False
        print(f'Error: Returned less days climate data: need {numdays} returned:{data.shape[0]}.\n')
        #exit()
    return good_data
    
def ReadSoilInitial(Run_First_Doy, Run_Last_Doy, Cells,pSoilState,pSoilModelLayer,pSoilHorizen,pSoilFlux):
    InitSoilState(pSoilState)
    start_row_idx = 7 - 1
    end_row_idx = 16 - 1
    Number_Initial_Conditions_Layers = int(get_excel_value(Cells,'B3'))
    Thickness_Model_Layers = 0.1
    
    Thickness = dict()
    Number_Of_Sublayers = dict()
    Water = dict()
    Nitrate = dict()
    Ammonium = dict()
    
    DOY = Run_First_Doy
    
    for i in range(1, Number_Initial_Conditions_Layers + 1):
        Thickness[i] = float(Cells.iloc[i + 6 - 1, 2 - 1])
        Number_Of_Sublayers[i] = int(Thickness[i] / Thickness_Model_Layers + 0.5)
        Water[i] = float(Cells.iloc[i + 6 - 1, 3 - 1])
        Nitrate[i] = float(Cells.iloc[i + 6 - 1, 4 - 1]) / 10000 #'Convert kg/ha to kg/m2
        Ammonium[i] = float(Cells.iloc[i + 6 - 1, 5 - 1]) / 10000 #'Convert kg/ha to kg/m2
    #'Distribute variables for each model layer of thickness 0.1 m
    Cum_J = 1
    for i in range(1, Number_Initial_Conditions_Layers + 1):
        NL = Number_Of_Sublayers[i]
        k = Cum_J
        L = (k + NL - 1)
        for j in range(k, L + 1):
            pSoilModelLayer.Layer_Thickness[j] = Thickness[i] / Number_Of_Sublayers[i]
            if j <= pSoilModelLayer.Number_Model_Layers:
                pSoilState.Water_Content[DOY][j] = Water[i]
                pSoilState.Water_Filled_Porosity[DOY][j] = Water[i] / pSoilModelLayer.Saturation_Water_Content[i]
                #pSoilState.Soil_Water_Potential[j] = WP(pSoilModelLayer.Saturation_Water_Content[i], Water[i], pSoilModelLayer.Air_Entry_Potential[i], pSoilModelLayer.B_value[i])
                pSoilState.Soil_Water_Potential[DOY][j] = WP(pSoilModelLayer.Saturation_Water_Content[i], Water[i], pSoilModelLayer.Air_Entry_Potential[i], pSoilModelLayer.B_value[i])
                pSoilState.Nitrate_N_Content[DOY][j] = Nitrate[i] / Number_Of_Sublayers[i]
                pSoilState.Ammonium_N_Content[DOY][j] = Ammonium[i] / Number_Of_Sublayers[i]
                pSoilModelLayer.Soil_Mass[j] = pSoilModelLayer.Bulk_Density[j] * 1000 * pSoilModelLayer.Layer_Thickness[j] #'kg/m2 in each soil layer. Bulk density converted from Mg/m3 to kg/m3
                SOC = pSoilModelLayer.Soil_Mass[j] * (pSoilModelLayer.Percent_Soil_Organic_Matter[j] / 100.) * Carbon_Fraction_In_SOM #'kg/m2
                pSoilState.Soil_Organic_Carbon[DOY][j] = SOC
                pSoilState.Soil_Organic_Nitrogen[DOY][j] = SOC / SOC_C_N_Ratio
        Cum_J = L + 1
    #Number_Model_Layers = Cum_J - 1
    #'Determine the thickness of the soil water evaporation layer
    #Percent_Sand = ReadInputs.PercentSand(1)
    #Thickness_Evaporative_Layer = Round(-0.001 * Percent_Sand + 0.169, 2)
    #Layer_Thickness(1) = Thickness_Evaporative_Layer
    #'Set accumulators to zero
    
    #'Mingliang: Begin of new section added
    Number_Initialization_Layers = Cum_J - 1 #'Mingliang 4/15/2025
    NML = pSoilModelLayer.Number_Model_Layers #'Mingliang 4/15/2025 'This is the total number of simulation model layers 'Mingliang 4/15/2025
    for i in range(Number_Initialization_Layers + 1, NML + 1):
            pSoilModelLayer.Layer_Thickness[i] = pSoilModelLayer.Layer_Thickness[Number_Initialization_Layers]
            pSoilState.Water_Content[DOY][i] =pSoilState.Water_Content[DOY][Number_Initialization_Layers]
            pSoilState.Water_Filled_Porosity[DOY][i] = pSoilState.Water_Content[DOY][i] / pSoilModelLayer.Saturation_Water_Content[i]
            #'Mingliang Soil water potential was changed to a two-dimensional array
            #'        Soil_Water_Potential(i) = WP(Saturation_Water_Content(i), Water_Content(DOY, i), Air_Entry_Potential(i), B_value(i))
            pSoilState.Soil_Water_Potential[DOY][i] = WP(pSoilModelLayer.Saturation_Water_Content[i], pSoilState.Water_Content[DOY][i], pSoilModelLayer.Air_Entry_Potential[i], pSoilModelLayer.B_value[i])
            pSoilState.Nitrate_N_Content[DOY][i] = pSoilState.Nitrate_N_Content[DOY][Number_Initialization_Layers]
            pSoilState.Ammonium_N_Content[DOY][i] = pSoilState.Ammonium_N_Content[DOY][Number_Initialization_Layers]
            #'        Initialize soil organi carbon and nitrogen
            #'        Convert percent organic matter to soil organic carbon in kg C/m2 soil
            pSoilModelLayer.Soil_Mass[i] = pSoilModelLayer.Bulk_Density[i] * 1000. # * Layer_Thickness(i) 'kg/m2 in each soil layer. Bulk density converted from Mg/m3 to kg/m3
            SOC = pSoilModelLayer.Soil_Mass[i] * (pSoilModelLayer.Percent_Soil_Organic_Matter[i] / 100.) * Carbon_Fraction_In_SOM #'kg/m2
            pSoilState.Soil_Organic_Carbon[DOY][i] = SOC
            pSoilState.Soil_Organic_Nitrogen[DOY][i] = SOC / SOC_C_N_Ratio
    #'Mingliang: End of new section added
    
    
    #Cumulative_Deep_Drainage = 0
    #Cumulative_N_Leaching = 0
    
    #Percent_Sand = pSoilHorizen.Sand[1]
    #Thickness_Evaporative_Layer = round(-0.001 * Percent_Sand + 0.169, 1)
    #pSoilModelLayer.Layer_Thickness[1] = Thickness_Evaporative_Layer           #TODO 11/15/2024LML High risk since the soil properties already initialized with default layer depth
    #'Set simulation period accumulators to zero
    #04252025COS-LML pSoilFlux.Simulation_Total_N_Leaching = 0
    #04252025COS-LML pSoilFlux.Simulation_Total_Deep_Drainage = 0
    #04252025COS-LML pSoilFlux.Simulation_Total_Irrigation = 0
    #04252025COS-LML pSoilFlux.Simulation_Total_Fertilization = 0
    pSoilState.Auto_Irrigation = False
    
    for i in range(Run_First_Doy, Run_Last_Doy + 1):
        pSoilFlux.Net_Irrigation_Depth[DOY] = 0.                                #TODO

def WriteCropSummaryOutput(Crop_Number, DOY, CropSumOutputs, 
                       pSoilFlux, pSoilState, pSoilModelLayer, 
                       pETState, pCropGrowth):
    
    #DOY_Of_Maturity = pCropGrowth.Maturity_DOY
    #DOY_Of_Harvest = pCropGrowth.Harvest_DOY
    #Last_DOY = DOY
    #if DOY_Of_Maturity > DOY_Of_Harvest:
    #    Last_DOY = DOY_Of_Harvest - 1
    #else:
    #    Last_DOY = DOY_Of_Maturity - 1 #'Mingliang 4/23/2025 ADD
        
    Profile_Nitrate_Content = 0.
    Profile_Ammonium_Content = 0.
    for i in range(1, pSoilModelLayer.Number_Model_Layers + 1):
        Profile_Nitrate_Content += pSoilState.Nitrate_N_Content[DOY][i]
        Profile_Ammonium_Content += pSoilState.Ammonium_N_Content[DOY][i]

    CropSumColumns_data = {
        "Cumulative Deep Drainage(mm)": pSoilFlux.Cumulative_Deep_Drainage,
        "Cumulative N Leaching (kg/ha)": pSoilFlux.Cumulative_N_Leaching,
        "Cumulative mineralization, 0.0 m - 0.3 m soil layer (kg/ha)": pSoilFlux.Cumulative_Mineralization_Top_Three_Layers_Crop[Crop_Number] * 10000, #'Convert kg/m2 to kg/ha
        "Cumulative mineralization, 0.3 m - 0.6 m soil layer (kg/ha)": pSoilFlux.Cumulative_Mineralization_Next_Three_Layers_Crop[Crop_Number] * 10000, #'Convert kg/m2 to kg/ha
        "Residual soil profile nitrate (kg/ha)": Profile_Nitrate_Content * 10000., # 'Convert kg/m2 to kg/ha,
        "Residual soil profile ammonium (kg/ha)": Profile_Ammonium_Content * 10000, # 'Convert kg/m2 to kg/ha,
        "Cumulative irrigation (mm)": pSoilFlux.Cumulative_Irrigation,
        "Cumulative N fertilization (kg/ha)": pSoilFlux.Cumulative_Fertilization * 10000, #'Convert kg/m2 to kg/ha,
        "Seasonal Transpiration (mm)": pETState.Total_Transpiration,
        "Seasonal Soil Water Evaporation (mm)": pETState.Crop_Soil_Water_Evaporation,
        "Seasonal N Uptake (kg/ha)": pCropState.Seasonal_N_Uptake * 10000, # 'Convert kg/m2 to kg/ha ,
        "Expected Potential Biomass at maturity (kg/ha)": pCropState.Cumulative_Potential_Crop_Biomass[DOY - 1] * 10000, # 'Convert kg/m2 to kg/ha,
        "Biomass at maturity or harvest, whichever is first (kg/ha)": pCropState.Seasonal_Biomass * 10000 # 'Convert kg/m2 to kg/ha
    }
    CropSumOutputs[Crop_Number].loc[len(CropSumOutputs[Crop_Number])] = CropSumColumns_data
    
def WriteCropOutput(Crop_Number, DOY, DAE, CropOutputs, 
                       pCropState, pETState, pSoilState):
    preday_Cumulative_N_Uptake = 0
    #handle first day issue
    if DOY == 1: 
        if 366 in pCropState.Cumulative_N_Uptake and pCropState.Cumulative_N_Uptake[366] > 1e-12:
            preday_Cumulative_N_Uptake = pCropState.Cumulative_N_Uptake[366]
        else:
            preday_Cumulative_N_Uptake = pCropState.Cumulative_N_Uptake[365]
    else:
        preday_Cumulative_N_Uptake = pCropState.Cumulative_N_Uptake[DOY - 1]
        
    CropOutRow = {
        "DAE": DAE,
        "DOY": DOY,
        "Pot Green Canopy Cover": pCropState.Potential_Green_Canopy_Cover[DOY],
        "Pot crop Transpiration (mm/day)": pETState.Potential_Crop_Transpiration[DOY],
        "Pot Biomass (kg/ha)": pCropState.Cumulative_Potential_Crop_Biomass[DOY] * 10000, #'Convert kg/m2 to kg/ha,
        "Green Canopy Cover": pCropState.Green_Canopy_Cover[DOY],
        "Biomass (kg/ha)": pCropState.Cumulative_Crop_Biomass[DOY] * 10000, #'Convert kg/m2 to kg/ha,
        "Transpiration (mm)": pETState.Actual_Transpiration[DOY],
        "Soil Evap (mm)": pETState.Actual_Soil_Water_Evaporation[DOY],
        "Root Depth (m)": pCropState.Root_Depth[DOY],
        "Height (m)": pCropState.Crop_Height[DOY],
        "Max N Conc (kg/kg)": pCropState.Maximum_N_Concentration[DOY],
        "Crit N Conc (kg/kg)": pCropState.Critical_N_Concentration[DOY],
        "Min N Conc (kg/kg)": pCropState.Minimum_N_Concentration[DOY],
        "Crop N Conc (kg/kg)": pCropState.Crop_N_Concentration[DOY],
        "Crop N Mass (kg/ha)": pCropState.Crop_N_Mass[DOY] * 10000, #'Convert kg/m2 to kg/ha
        "N Uptake (kg/ha)": pCropState.Cumulative_N_Uptake[DOY] * 10000, #'Convert kg/m2 to kg/ha
        "Crop WSI (0-1)": pETState.Water_Stress_Index[DOY],
        "Crop NSI (0-1)": pCropState.Nitrogen_Stress_Index[DOY],
        "PAW Depletion Profile (0-1)": pSoilState.PAW_Depletion[DOY],
        #"PAW Depletion Top 50 cm (0-1)": pSoilState.PAW_Depletion_Top50cm[DOY],
        #"PAW Depletion Mid 50 cm (0-1)": pSoilState.PAW_Depletion_Mid50cm[DOY],
        #"PAW Depletion bottom 50 cm (0-1)": pSoilState.PAW_Depletion_Bottom50cm[DOY],
        "Water Content Top 50 cm (0-1)": pSoilState.Water_Content_Top50cm[DOY],
        "Water Content Mid 50 cm (0-1)": pSoilState.Water_Content_Mid50cm[DOY],
        "Water Content bottom 50 cm (0-1)": pSoilState.Water_Content_Bottom50cm[DOY],
        "N Mass Top 50 cm (kg/ha)": pSoilState.N_Mass_Top50cm[DOY],
        "N Mass Mid 50 cm (kg/ha)": pSoilState.N_Mass_Mid50cm[DOY],
        "N Mass bottom 50 cm (kg/ha)": pSoilState.N_Mass_Bottom50cm[DOY],
        "N Leaching (kg/ha)":pSoilFlux.N_Leaching_Accumulated[DOY] * 10000, #'Convert kg/m2 to kg/ha 'NEW Mingliang
        "Soil N Mass down to 150 cm (kg/ha)": pSoilState.N_Mass_Top50cm[DOY] + pSoilState.N_Mass_Mid50cm[DOY] + pSoilState.N_Mass_Bottom50cm[DOY],
        "N Uptake Rate (kg/ha/day)": (pCropState.Cumulative_N_Uptake[DOY] - preday_Cumulative_N_Uptake) * 10000 #'Convert kg/m2 to kg/ha
    }
    CropOutputs[Crop_Number].loc[len(CropOutputs[Crop_Number])] = CropOutRow
        
def WriteCropSoilOutput(Crop_Number, DOY, DAE, SoilLayers, SoilOutputs, 
                       pCropState, pSoilFlux):
    SoilOutRow = dict()
    SoilOutRow["DAE"] = DAE
    SoilOutRow["DOY"] = DOY
    for i in range(1,SoilLayers + 1):
        SoilOutRow[f'Water (m/m) L{i}'] = pSoilState.Water_Content[DOY][i]
        SoilOutRow[f'NO3-N (kg/ha) L{i}'] = pSoilState.Nitrate_N_Content[DOY][i] * 10000 #'Convert kg/m2 to kg/ha
        SoilOutRow[f'NH4-N (kg/ha) L{i}'] = pSoilState.Ammonium_N_Content[DOY][i] * 10000 #'Convert kg/m2 to kg/ha
    for i in range(1,7):
        SoilOutRow[f'Mineralized-N (kg/ha) L{i}'] = pSoilFlux.Layer_Mineralization[DOY][i] * 10000 #'Convert kg/m2 to kg/ha
    
    if Crop_Number != 0:
        SoilOutputs[Crop_Number].loc[len(SoilOutputs[Crop_Number])] = SoilOutRow
    
def WriteTotalSimPeriodOutput(TotalSimPeriodOutput, RunLastDOY, 
                              SoilLayers, pSoilState, pSoilFlux):
    Profile_Nitrate_Content = 0
    Profile_Ammonium_Content = 0
    Last_Simulation_DOY = RunLastDOY # - 1
    for i in range(1, SoilLayers + 1):
        Profile_Nitrate_Content += pSoilState.Nitrate_N_Content[Last_Simulation_DOY - 1][i]
        Profile_Ammonium_Content += pSoilState.Ammonium_N_Content[Last_Simulation_DOY - 1][i]
    TotalSimPeriodRow = {
        "Cumulative Deep Drainage(mm)": pSoilFlux.Simulation_Total_Deep_Drainage,
        "Cumulative N Leaching (kg/ha)": pSoilFlux.Simulation_Total_N_Leaching,
        "Cumulative mineralization, 0.0 m - 0.3 m soil layer (kg/ha)": pSoilFlux.Cumulative_Mineralization_Top_Three_Layers_All_Days * 10000, # 'Convert kg/m2 to kg/ha,
        "Cumulative mineralization, 0.3 m - 0.6 m soil layer (kg/ha)": pSoilFlux.Cumulative_Mineralization_Next_Three_Layers_All_Days * 10000, # 'Convert kg/m2 to kg/ha,
        "Residual soil profile nitrate (kg/ha)": Profile_Nitrate_Content * 10000, #  'Convert kg/m2 to kg/ha
        "Residual soil profile ammonium (kg/ha)": Profile_Ammonium_Content * 10000, #  'Convert kg/m2 to kg/ha
        "Cumulative irrigation (mm)": pSoilFlux.Simulation_Total_Irrigation,
        "Cumulative N fertilization (kg/ha)": pSoilFlux.Simulation_Total_Fertilization * 10000 #  'Convert kg/m2 to kg/ha
        }
    TotalSimPeriodOutput.loc[len(TotalSimPeriodOutput)] = TotalSimPeriodRow

def WriteDailyWaterAndNitrogenBudgetTable(DailyBudgetOutputs, Crop_Number, DOY, 
                                          DAE, SoilLayers, 
                                          pCropState, pSoilFlux, pETState, 
                                          pSoilState, pCS_Weather, irrigations,
                                          Irrigation_Recommendation,
                                          pCS_Fertilization, Today_Crop_N_Demand, 
                                          Available_For_Active_Uptake):
#Items from "7-day daily budget table" of Irrigation Schedular, plus nitrogen 
#budget
    BudgetOutRow = dict()
    BudgetOutRow["DAE"] = DAE
    BudgetOutRow["DOY"] = DOY
    BudgetOutRow["Water Use (in)"] = mm_to_inch(pETState.Actual_Transpiration[DOY] 
                                                + pETState.Actual_Soil_Water_Evaporation[DOY])
    BudgetOutRow["Rain and Irrig (in)"] = mm_to_inch(pCS_Weather.Precipitation[DOY] + irrigations[DOY])
    BudgetOutRow["PAW Depletion (0-1)"] = pSoilState.PAW_Depletion[DOY]   #"Water Deficit (in)": "float64", 
    BudgetOutRow["Irrigation_Recommendation (in)"] = mm_to_inch(Irrigation_Recommendation)
    BudgetOutRow["Water_Stress_Index (0-1)"] = pETState.Water_Stress_Index[DOY]
    BudgetOutRow["Today_Crop_N_Demand (kg/ha)"] = KgPerSquareMeter_to_KgPerHa(Today_Crop_N_Demand)
    BudgetOutRow["N Uptake (kg/ha)"] = KgPerSquareMeter_to_KgPerHa(pCropState.N_Uptake[DOY])
    BudgetOutRow["N Fertilization (kg/ha)"] = KgPerSquareMeter_to_KgPerHa(pCS_Fertilization.Nitrate_Fertilization_Rate[DOY] 
                                                                          + pCS_Fertilization.Ammonium_Fertilization_Rate[DOY])
    BudgetOutRow["N Aailable (kg/ha)"] = KgPerSquareMeter_to_KgPerHa(Available_For_Active_Uptake)
    BudgetOutRow["N Deficit (kg/ha)"] = max(0.0,BudgetOutRow["Today_Crop_N_Demand (kg/ha)"] - BudgetOutRow["N Uptake (kg/ha)"])
    BudgetOutRow["Nitrogen_Stress_Index (0-1)"] = pCropState.Nitrogen_Stress_Index[DOY]
    DailyBudgetOutputs[Crop_Number].loc[len(DailyBudgetOutputs[Crop_Number])] = BudgetOutRow
    


#Main
#get file
data_path = '/home/liuming/mnt/hydronas3/Projects/CropManagement/VBCode_04262025'
output_path = '/home/liuming/mnt/hydronas3/Projects/CropManagement/test_results'
crop_from_excel_csv = 'Crop_Parameters.csv'
fieldinput_from_excel_csv = 'Field_Input.csv'
soil_initial_excel_csv = 'Initial_Soil_Conditions.csv'

crop_output_excel_csv = 'CropOutput.csv'
soil_output_excel_csv = 'SoilOutput.csv'
budget_output_excel_csv = 'BudgetOutput.csv'

#Soil properties & Crop growth parameters
InputCells = pd.read_csv(f'{data_path}/{fieldinput_from_excel_csv}',header=None)
cropCells = pd.read_csv(f'{data_path}/{crop_from_excel_csv}',header=None)
SoilInitCells = pd.read_csv(f'{data_path}/{soil_initial_excel_csv}',header=None)

#user option
soil_propertities_from_SSURGO = False
crop_growth_parameter_from_ISM = False
weather_from_AgWeatherNet = False

#02072025LML. For irrigation recommendation, the user need select either 
#"PAW Depletion" or "CWSI" or "Refill" 
#The user may choose different options every time
Irrigation_Recommendation_Option = 'PAW Depletion' # 'CWSI' 'Refill' 
Irrigation_Recommendation_Parameter = 0.5

#Farm and field description
Farm_Name = get_excel_value(InputCells,'A5')
Field_Number = int(get_excel_value(InputCells,'A6'))
Farm_Name = get_excel_value(InputCells,'A7')
Field_Name = get_excel_value(InputCells,'D12') #'test1'   #McNary 100031
Area = float(get_excel_value(InputCells,'A12'))
Irrigation_Method = get_excel_value(InputCells,'B12')
Water_Source = int(get_excel_value(InputCells,'C12'))                          #1: River 2: Canal 3: Groundwater
Water_N_Conc = float(get_excel_value(InputCells,'D12'))

ISM_cropnames = {'Triticale': 'Triticale (for forage)','Silage Corn': 'Corn (silage)'}  #TODO

#user define the field boundary or point
#test for point
field_lat = 45.97
field_lon = -119.26
wkt_geometry = f'point ({field_lon} {field_lat})'

#test for polygon
wkt_geometry = 'POLYGON((-119.265 45.972, -119.259 45.972,-119.259 45.968,-119.265 45.969,-119.265 45.972))'

AnemomH = 1.5                                                                  #elevation of anemometer (m)

#'First simulation run day of tghe year
First_DOY = int(get_excel_value(InputCells,'E5'))



if weather_from_AgWeatherNet:
    agWeatherStationID,dist = FindClosestStationAndDistance(field_lat,field_lon,
                                                            agweathernetstation,
                                                            "Latitude(N)",
                                                            "Longitude(W)",
                                                            "Station ID")

#'Soil description
pSoilHorizen = SoilHorizons()
pSoilModelLayer = SoilModelLayer()
if soil_propertities_from_SSURGO == False:                                     #User set soil horizental properties
    ReadSoilHorizonParamegters(InputCells,pSoilHorizen)
else:
    if 'point' in wkt_geometry:
        point = wkt.loads(wkt_geometry)
        mukey,muname,percent = get_mukey_muname_from_geocoordinate(point.x,point.y)
    else:
        mukey,muname,percent = get_dominant_mukey_muname_from_polygon(wkt_geometry, 10)
    if mukey is not None:
        #print(f'{mukey}:{muname}')
        result = get_all_components_soil_properties(mukey)
        result['comppct_r'] = result['comppct_r'].astype(float)
        result['hzdept_r'] = result['hzdept_r'].astype(float)
        result['hzdepb_r'] = result['hzdepb_r'].astype(float)
        max_cmppct = result['comppct_r'].max()
        max_cmppct_rows = result[result['comppct_r'] == max_cmppct]
        max_cmppct_rows_unique_rows = max_cmppct_rows.drop_duplicates(subset=['ch.chkey'], keep='first').sort_values(by='hzdept_r').reset_index(drop=True)
        GetSoilHorizonParamegtersFromSSURGO(max_cmppct_rows_unique_rows,pSoilHorizen)
    else:
        print('Warning: Cannot find SSURGO data for this field!')
CalculateHydraulicProperties(pSoilHorizen.Number_Of_Horizons,pSoilHorizen,pSoilModelLayer)

#'Crop description
Number_Of_Crops = int(get_excel_value(InputCells,'A31'))
CropNames = dict()
CropGrowths = dict()
CropParamaters = dict()

for crop in range(1,Number_Of_Crops + 1):
    if crop == 1:
        CropNames[crop] = get_excel_value(InputCells,'A38')
        col_letter = 'J'                                                       #crop paramater value column
        crop_row_index = 38                                                     #Crop growth parameters
    else:
        CropNames[crop] = get_excel_value(InputCells,'A39')
        col_letter = 'L'  #crop paramater value column
        crop_row_index = 39
    ISM_cropname = ISM_cropnames[CropNames[crop]]
    CropGrowths[crop] = CropGrowth()
    CropParamaters[crop] = CropParameter()
    
    ReadCropParameters(cropCells,CropParamaters[crop],col_letter)
    ReadCropGrowth(InputCells,CropGrowths[crop],crop_row_index)
    
    if crop_growth_parameter_from_ISM:  #update some DOY parameters from ISM
        GetISMCropGrowthDOYParameters(agWeatherStationID,ISM_cropname,pCropGrowth) #TODO

#fertilization
pCS_Fertilization = CS_Fertilization()
InitFertilization(pCS_Fertilization)
ReadFertilization(InputCells,pCS_Fertilization)

#irrigation
DOY_Last_Scheduled_Irrigation = 0
net_irrigations = dict()
for i in range(1,367):
    net_irrigations[i] = 0.
DOY_Last_Scheduled_Irrigation = ReadNetIrrigation(InputCells,net_irrigations)

#'Automatic irrigation
AutoIrrigations = AutoIrrigationEvents()
Emergence_DOY_1 = CropGrowths[1].Emergence_DOY
Maturity_DOY_1 = CropGrowths[1].Maturity_DOY
if Number_Of_Crops == 2:
    Emergence_DOY_2 = CropGrowths[2].Emergence_DOY
    Maturity_DOY_2 = CropGrowths[2].Maturity_DOY
else:
    Emergence_DOY_2 = None
    Maturity_DOY_2 = None
ReadAutoIrrigation(InputCells,AutoIrrigations,DOY_Last_Scheduled_Irrigation,
                   Emergence_DOY_1,Maturity_DOY_1,Emergence_DOY_2,Maturity_DOY_2)

#agWeatherStation = '100031' #McNary
CropColums = {
    "DAE": "int32",
    "DOY": "int32",
    "Pot Green Canopy Cover": "float64",
    "Pot crop Transpiration (mm/day)": "float64",
    "Pot Biomass (kg/ha)": "float64",
    "Green Canopy Cover": "float64",
    "Biomass (kg/ha)": "float64",
    "Transpiration (mm)": "float64",
    "Soil Evap (mm)": "float64",
    "Root Depth (m)": "float64",
    "Height (m)": "float64",
    "Max N Conc (kg/kg)": "float64",
    "Crit N Conc (kg/kg)": "float64",
    "Min N Conc (kg/kg)": "float64",
    "Crop N Conc (kg/kg)": "float64",
    "Crop N Mass (kg/ha)": "float64",
    "N Uptake (kg/ha)": "float64",
    "Crop WSI (0-1)": "float64",
    "Crop NSI (0-1)": "float64",
    "PAW Depletion Profile (0-1)": "float64",
    #"PAW Depletion Top 50 cm (0-1)": "float64", #'NEW Mingliang
    #"PAW Depletion Mid 50 cm (0-1)": "float64", #'NEW Mingliang
    #"PAW Depletion bottom 50 cm (0-1)": "float64", #'NEW Mingliang
    "Water Content Top 50 cm (0-1)": "float64", #'NEW Mingliang
    "Water Content Mid 50 cm (0-1)": "float64", #'NEW Mingliang
    "Water Content bottom 50 cm (0-1)": "float64", #'NEW Mingliang
    "N Mass Top 50 cm (kg/ha)": "float64", #'NEW Mingliang
    "N Mass Mid 50 cm (kg/ha)": "float64", #'NEW Mingliang
    "N Mass bottom 50 cm (kg/ha)": "float64", #'NEW Mingliang
    "N Leaching (kg/ha)": "float64", #'NEW Mingliang
    "Soil N Mass down to 150 cm (kg/ha)": "float64", #'NEW Mingliang
    "N Uptake Rate (kg/ha/day)": "float64"
    }

CropOutputs = dict()
for crop in range(1,Number_Of_Crops + 1):
    CropOutputs[crop] = pd.DataFrame({col: pd.Series(dtype=dt) for col, dt in CropColums.items()})

#output_mode_file_name = 'Water_Uptake_output_mode.csv'
#output_file_name = 'wateruptake_out.csv'

#all crop parameters
#crop_parameters = dict()
#Use the user selected ISM cropname
#crop_parameters[ISM_cropname] = crop_paramater

#Crop growth inputs
#pCropGrowth = CropGrowth()
#CropGrowths = dict()

#Get some growth parameters from user
#crop_row_index = 38
#ReadCropGrowth(InputCells,pCropGrowth,crop_row_index)
#pCropGrowth.Crop_Name = ISM_cropname  #Not using the crop name in the Excel table
#if crop_growth_parameter_from_ISM:  #update some DOY parameters from ISM
#    GetISMCropGrowthDOYParameters(agWeatherStationID,ISM_cropname,pCropGrowth)

#CropGrowths[ISM_cropname] = pCropGrowth




#Soil initial conditions


#SoilOutput
SoilLayers = pSoilModelLayer.Number_Model_Layers
SoilColums = dict()
SoilColums["DAE"] = "int32"
SoilColums["DOY"] = "int32"
for i in range(1,SoilLayers + 1):
    SoilColums[f'Water (m/m) L{i}'] = "float64"
    SoilColums[f'NO3-N (kg/ha) L{i}'] = "float64"
    SoilColums[f'NH4-N (kg/ha) L{i}'] = "float64"
for i in range(1,7):
    SoilColums[f'Mineralized-N (kg/ha) L{i}'] = "float64"
    
SoilOutputs = dict()
for crop in range(1,Number_Of_Crops + 1):
    SoilOutputs[crop] = pd.DataFrame({col: pd.Series(dtype=dt) for col, dt in SoilColums.items()})


#Daily Budget Outputs (From emergence to maturity)
DailyBudgetColums = {
    "DAE": "int32",
    "DOY": "int32",
    "Water Use (in)": "float64",
    "Rain and Irrig (in)": "float64", 
    "PAW Depletion (0-1)": "float64", 
    "Irrigation_Recommendation (in)": "float64", 
    "Water_Stress_Index (0-1)": "float64", 
    "Today_Crop_N_Demand (kg/ha)": "float64",
    "N Uptake (kg/ha)": "float64", 
    "N Fertilization (kg/ha)": "float64",
    "N Aailable (kg/ha)": "float64",
    "N Deficit (kg/ha)": "float64",
    "Nitrogen_Stress_Index (0-1)": "float64"
    }



DailyBudgetOutputs = dict()
for crop in range(1,Number_Of_Crops + 1):
    DailyBudgetOutputs[crop] = pd.DataFrame({col: pd.Series(dtype=dt) for col, dt in DailyBudgetColums.items()})


#CROP OUTPUT (From emergence to maturity)
CropSumColums = {
    "Cumulative Deep Drainage(mm)": "float64",
    "Cumulative N Leaching (kg/ha)": "float64",
    "Cumulative mineralization, 0.0 m - 0.3 m soil layer (kg/ha)": "float64",
    "Cumulative mineralization, 0.3 m - 0.6 m soil layer (kg/ha)": "float64",
    "Residual soil profile nitrate (kg/ha)": "float64",
    "Residual soil profile ammonium (kg/ha)": "float64",
    "Cumulative irrigation (mm)": "float64",
    "Cumulative N fertilization (kg/ha)": "float64",
    "Seasonal Transpiration (mm)": "float64",
    "Seasonal Soil Water Evaporation (mm)": "float64", #'Mingliang 4/17/2025
    "Seasonal N Uptake (kg/ha)": "float64",
    "Expected Potential Biomass at maturity (kg/ha)": "float64",
    "Biomass at maturity or harvest, whichever is first (kg/ha)": "float64"
    }

CropSumOutputs = dict()
for crop in range(1,Number_Of_Crops + 1):
    CropSumOutputs[crop] = pd.DataFrame({col: pd.Series(dtype=dt) for col, dt in CropSumColums.items()})

#TOTALS FOR SIMULATION PERIOD
TotalSimPeriodColumns = {
    "Cumulative Deep Drainage(mm)": "float64",
    "Cumulative N Leaching (kg/ha)": "float64",
    "Cumulative mineralization, 0.0 m - 0.3 m soil layer (kg/ha)": "float64",
    "Cumulative mineralization, 0.3 m - 0.6 m soil layer (kg/ha)": "float64",
    "Residual soil profile nitrate (kg/ha)": "float64",
    "Residual soil profile ammonium (kg/ha)": "float64",
    "Cumulative irrigation (mm)": "float64",
    "Cumulative N fertilization (kg/ha)": "float64",
    }
TotalSimPeriodOutput = pd.DataFrame({col: pd.Series(dtype=dt) for col, dt in TotalSimPeriodColumns.items()})

#RECORD FOR FEILD Irigation & Fertilization events
FieldManagementsLogs = {
    "DOY": "int32",
    "Crop": "int32",
    "Irrigation (mm)": "float64",
    "Fertilizer (kg/ha)": "float64"
    }
FieldManagementsLogsOutput = pd.DataFrame({col: pd.Series(dtype=dt) for col, dt in FieldManagementsLogs.items()})

#Irrigation N concentration
#WaterNConc = float(get_excel_value(InputCells,'D12'))



#for i in range(1, pSoilHorizen.Number_Of_Horizons+1):
#    print(f'i:{i} Horizon_Thickness:{pSoilHorizen.Horizon_Thickness[i]} Clay:{pSoilHorizen.Clay[i]}') #'Thickness is rounded to one decimal
#for i in range(1, pSoilLayer.Number_Model_Layers+1):
#    print(f'i:{i} FC_Water_Content:{pSoilLayer.FC_Water_Content[i]} PWP_Water_Content:{pSoilLayer.PWP_Water_Content[i]}') #'Thickness is rounded to one decimal
    



Number_Of_Days_To_Simulate = 0
Year_Number = 0
DAE = 0
DOY_At_DAE = dict() #(366) As Integer
Crop_Active = False

Run_First_Doy = int(get_excel_value(InputCells,'E5'))
Crop_Active = False

Already_Done_Crop_Sum_Output = {1 : False, 2 : False}                          #04282025LML control crop sum ouputs

#crop_states = dict()

pCropState = CropState()
InitCropState(pCropState)

pETState = ETState()
InitETState(pETState)

pSoilState = SoilState()
InitSoilState(pSoilState)

pSoilFlux = SoilFlux()
InitSoilFlux(pSoilFlux)

pBalance = Balances()

#Number_Of_Crops = int(get_excel_value(InputCells,'A31'))
if Number_Of_Crops == 2: DOY_Planting_Second_Crop = CropGrowths[2].Planting_DOY
if Number_Of_Crops == 1: 
    Run_Last_Doy = CropGrowths[1].Harvest_DOY 
else: 
    Run_Last_Doy = CropGrowths[2].Harvest_DOY
    
    

#Set weather data
sim_st_year = 2023
sim_start_doy = Run_First_Doy

sim_end_doy = Run_Last_Doy
if sim_start_doy > sim_end_doy:
    sim_end_year = sim_st_year + 1
else:
    sim_end_year = sim_start_doy

#Weather data
pCS_Weather = CS_Weather()
if weather_from_AgWeatherNet == False:
    ReadWeather(InputCells,pCS_Weather)
else:
    bdaily = True
    good_data = GetAgWeatherNetDailyWeather(agWeatherStationID,AnemomH,sim_st_year,sim_start_doy,sim_end_year,sim_end_doy,pCS_Weather)
    if good_data == False:
        print('Error: AgWeatherNet data fetch error!\n')
        sys.exit()
    
    
#ReadSoilInitial(Run_First_DOY,SoilInitCells,pSoilState,pSoilModelLayer)
ReadSoilInitial(Run_First_Doy, Run_Last_Doy, SoilInitCells, pSoilState,
                pSoilModelLayer, pSoilHorizen, pSoilFlux)

#First_Crop_Name = pCropGrowth.Crop_Name
#Run_Last_DOY = CropGrowths[First_Crop_Name].Harvest_DOY

#crop_states[First_Crop_Name] = CropState()

#first_crop_growth = CropGrowths[First_Crop_Name]
#first_crop_state = CropState()

#'Begin time loop

#pCropParameter = crop_parameters[First_Crop_Name]
#pCropState = crop_states[First_Crop_Name]
#pCropGrowth = CropGrowths[First_Crop_Name]



#InitETState(pETState)
#ReadSoilInitial(Run_First_DOY,SoilInitCells,pSoilState,pSoilModelLayer)
#InitCropState(pCropState)
if Run_First_Doy > Run_Last_Doy: 
    Number_Of_Days_To_Simulate = (365 - Run_First_Doy) + Run_Last_Doy 
else:
    Number_Of_Days_To_Simulate = Run_Last_Doy - Run_First_Doy
Days_Elapsed = 0
DOY = Run_First_Doy
Year_Number = 1
Crop_Number = 0
DAE = 0

Number_Of_Layers = pSoilModelLayer.Number_Model_Layers
#'Begin time loop
while Days_Elapsed <= (Number_Of_Days_To_Simulate + 1):
    Today_Crop_N_Demand = 0.0
    Available_N = 0.0
    #Crop_Number = ReadInputs.CropOrder(1)
    InitialSoilProfile(DOY,pBalance,pSoilState,pSoilModelLayer)
    #'Set up Crop Number 1
    if DOY == CropGrowths[1].Emergence_DOY:
        Crop_Active = True
        Crop_Number = 1
        DAE = 1
        InitializeCrop(DOY,pCropState,pSoilFlux,CropParamaters[1],pETState)
        #'Convert days of the year to days after emergence
        if CropGrowths[1].Emergence_DOY > CropGrowths[1].Maturity_DOY:
            DAE_At_Maturity = (365 - CropGrowths[1].Emergence_DOY) + CropGrowths[1].Maturity_DOY
        else:
            DAE_At_Maturity = CropGrowths[1].Maturity_DOY - CropGrowths[1].Emergence_DOY
        #'Set state variables for the potential crop for the entire season. The potential crop grows without water and N stress
        Day_Of_The_Year = CropGrowths[1].Emergence_DOY
        for Days_After_Emergence in range(0, DAE_At_Maturity + 1):
            PotentialCanopyCover(Crop_Number, Days_After_Emergence, 
                                 Day_Of_The_Year, CropParamaters[1], 
                                 pCropState, CropGrowths[1]) #Calculate potential green canopy cover for the entire season
            PotET(Day_Of_The_Year, True, Crop_Active, pCropState, CropParamaters[1], pCS_Weather, pETState) #Calculations are for the potential crop and the crop is active
            
            
            Biomass(Day_Of_The_Year, True, pCropState, CropParamaters[1], pCS_Weather, pETState) #Calculate potential biomass for the entire season
            ReferencePlantNConcentration(Day_Of_The_Year, pCropState, CropParamaters[1], CropGrowths[1])
            Day_Of_The_Year += 1
            if Day_Of_The_Year > 365: Day_Of_The_Year = 1
    #'Set up Crop Number 2
    if 2 in CropGrowths and DOY == CropGrowths[2].Emergence_DOY:
        Crop_Active = True
        Crop_Number = 2
        DAE = 1
        InitializeCrop(DOY,pCropState,pSoilFlux,CropParamaters[2],pETState)
        #'Convert days of the year to days after emergence
        if CropGrowths[2].Emergence_DOY > CropGrowths[2].Maturity_DOY:
            DAE_At_Maturity = (365 - CropGrowths[2].Emergence_DOY) + CropGrowths[2].Maturity_DOY
        else:
            DAE_At_Maturity = CropGrowths[2].Maturity_DOY - CropGrowths[2].Emergence_DOY

        #'Set state variables for the potential crop for the entire season. The potential crop grows without water and N stress
        Day_Of_The_Year = CropGrowths[2].Emergence_DOY
        for Days_After_Emergence in range(0, DAE_At_Maturity + 1):
            PotentialCanopyCover(Crop_Number, Days_After_Emergence, 
                                 Day_Of_The_Year, CropParamaters[2], 
                                 pCropState, CropGrowths[2]) #Calculate potential green canopy cover for the entire season
            PotET(Day_Of_The_Year, True, Crop_Active, pCropState, 
                  CropParamaters[2], pCS_Weather, pETState) #Calculations are for the potential crop and the crop is active
            
            Biomass(Day_Of_The_Year, True, pCropState, CropParamaters[2], 
                    pCS_Weather, pETState) #Calculate potential biomass for the entire season
            ReferencePlantNConcentration(Day_Of_The_Year, pCropState, 
                                         CropParamaters[2], CropGrowths[2])
            Day_Of_The_Year += 1
            if Day_Of_The_Year > 365: Day_Of_The_Year = 1

    print(f'DOY:{DOY} DAE:{DAE} Crop_Number:{Crop_Number}')


    if Crop_Number == 1 and (DOY == CropGrowths[1].Maturity_DOY or DOY == CropGrowths[1].Harvest_DOY):
        Crop_Active = False
        #Crop_Number = 0
        #DAE = 0
        pSoilState.Auto_Irrigation = False

    if Crop_Number == 2 and (DOY == CropGrowths[2].Maturity_DOY or DOY == CropGrowths[2].Harvest_DOY):
        Crop_Active = False
        #Crop_Number = 0
        #DAE = 0
        pSoilState.Auto_Irrigation = False


    if Crop_Active: 
        CanopyCover(DOY, DAE, Crop_Number, pCropState, 
                    CropParamaters[Crop_Number], CropGrowths[Crop_Number], 
                    pETState)
        GrowRoot(DOY, pCropState, CropParamaters[Crop_Number])
        GrowHeight(DOY, pCropState, CropParamaters[Crop_Number])

        PotET(DOY, False, Crop_Active, pCropState, CropParamaters[Crop_Number], 
              pCS_Weather, pETState)
        
        ActualTranspiration(DOY, CropParamaters[Crop_Number], pSoilModelLayer, 
                            pCropState, pETState, pSoilState)
        ActEvaporation(DOY,pSoilModelLayer,pSoilState,pETState, Crop_Active)
        Biomass(DOY, False, pCropState, CropParamaters[Crop_Number], 
                pCS_Weather, pETState)
        
        Today_Crop_N_Demand,Available_N = \
            NitrogenUptake(DOY, pCropState, CropParamaters[Crop_Number], 
                       CropGrowths[Crop_Number], pETState, pSoilModelLayer, 
                       pSoilState)
        #'synchronize days after emergence (DAE) and day of the year (DOY)
        DOY_At_DAE[DAE] = DOY
        #DAE += 1
    else:
        PotET(DOY, False, False, pCropState, None, pCS_Weather, pETState) #Crop is not active and only potential evaporation is calculated
        ActEvaporation(DOY,pSoilModelLayer,pSoilState,pETState, False)
        
    SoilTemperature(DOY,pCS_Weather.Tmax[DOY],pCS_Weather.Tmin[DOY],
                    pSoilModelLayer,pSoilState)
    Mineralization(DOY, Crop_Number, pSoilModelLayer, pSoilState, pSoilFlux, Crop_Active)
    Nitrification(DOY,pSoilModelLayer,pSoilState,pSoilFlux)
    
    
    #02072025LML estimate the irrigation recommendations 
    Irrigation_Recommendation = 0.0
    #02252025LML always calculate PAW depletion
    PAW_Depletion_Today,Water_Depth_To_Refill_fc = calc_PAW_depletion(DOY, 
            Number_Of_Layers, pSoilState, pETState, pSoilModelLayer)
    #if Crop_Active and Irrigation_Recommendation_Option != 'PAW Depletion':
    #  SetAutoIrrigation(DOY, True, False, Number_Of_Layers, 
    #                        0.5, -9999, False, 
    #                        -9999, pSoilState, pETState, pSoilModelLayer)
    
    if Crop_Active and Irrigation_Recommendation_Option == 'PAW Depletion':
      Irrigation_Recommendation = \
          SetAutoIrrigation(DOY, True, False, Number_Of_Layers, 
                            Irrigation_Recommendation_Parameter, -9999, False, 
                            -9999, pSoilState, pETState, pSoilModelLayer, Water_Depth_To_Refill_fc)
    elif Crop_Active and Irrigation_Recommendation_Option == 'CWSI':
      Irrigation_Recommendation = \
          SetAutoIrrigation(DOY, False, True, Number_Of_Layers, 
                            -9999, Irrigation_Recommendation_Parameter, False, 
                            -9999, pSoilState, pETState, pSoilModelLayer, Water_Depth_To_Refill_fc)  
    elif Irrigation_Recommendation_Option == 'Refill':
      Irrigation_Recommendation = \
          SetAutoIrrigation(DOY, False, False, Number_Of_Layers, 
                            -9999, -9999, True, 
                            Irrigation_Recommendation_Parameter, pSoilState, 
                            pETState, pSoilModelLayer, Water_Depth_To_Refill_fc)  
          
    net_irrigation_today,fertilizer_today = \
        WaterAndNTransport(DOY, pSoilModelLayer, pSoilState, net_irrigations, 
                           Water_N_Conc, 
                           pCS_Weather.Precipitation[DOY], 
                           pCS_Fertilization.Nitrate_Fertilization_Rate[DOY], 
                           pCS_Fertilization.Ammonium_Fertilization_Rate[DOY], 
                           pCS_Fertilization.Nitrate_Fraction[DOY], 
                           AutoIrrigations, 
                           pSoilFlux, 
                           Crop_Active,
                           pETState,
                           Water_Depth_To_Refill_fc)
    
    #output managements
    if net_irrigation_today >= 1e-12 or fertilizer_today >=1e-12:
        FieldManagementsLogsOutput.loc[len(FieldManagementsLogsOutput)] = {
            "DOY": DOY,
            "Crop": Crop_Number,
            "Irrigation (mm)": net_irrigation_today,
            "Fertilizer (kg/ha)": fertilizer_today * 10000 #  'Convert kg/m2 to kg/ha
            }
    
    BalancesAll(DOY,pBalance,pSoilState,pSoilFlux,pSoilModelLayer,pCS_Weather,
                pETState,pCS_Fertilization,pCropState)
    
    #'Write Daily and summary Outputs by crop number at harvest time
    
    if Crop_Active and DOY != CropGrowths[Crop_Number].Harvest_DOY:
        #CropOutput
        WriteCropOutput(Crop_Number, DOY, DAE, CropOutputs, pCropState, 
                        pETState, pSoilState)
        #SoilOutput
        WriteCropSoilOutput(Crop_Number, DOY, DAE, SoilLayers, SoilOutputs, 
                               pCropState, pSoilFlux)
        
        #Budget output
        WriteDailyWaterAndNitrogenBudgetTable(DailyBudgetOutputs, Crop_Number, DOY, 
                                                  DAE, SoilLayers, 
                                                  pCropState, pSoilFlux, pETState, 
                                                  pSoilState, pCS_Weather, net_irrigations,
                                                  Irrigation_Recommendation,
                                                  pCS_Fertilization, Today_Crop_N_Demand, 
                                                  Available_N)
    
    
    #SummaryOutput
    #if DOY == CropGrowths[1].Maturity_DOY or DOY == CropGrowths[1].Harvest_DOY:
    #if Crop_Number == 1 and DOY == CropGrowths[1].Harvest_DOY: output cumulations before harvest day
    #print(f'DOY:{DOY}')
    if Crop_Number == 1 and (DOY == CropGrowths[1].Maturity_DOY or DOY == CropGrowths[1].Harvest_DOY) and Already_Done_Crop_Sum_Output[1] == False: #max(CropGrowths[1].Maturity_DOY,CropGrowths[1].Harvest_DOY):
        WriteCropSummaryOutput(1, DOY, CropSumOutputs, 
                               pSoilFlux, pSoilState, pSoilModelLayer, 
                               pETState,CropGrowths[1])
        Already_Done_Crop_Sum_Output[1] = True
        #print(f'WriteCropSummaryOutput:{DOY} Crop_Number:{Crop_Number} Maturity_DOY:{CropGrowths[1].Maturity_DOY} Harvest_DOY:{CropGrowths[1].Harvest_DOY}')
        #Crop_Number = 0
    if Crop_Number == 2 and (DOY == CropGrowths[2].Maturity_DOY or DOY == CropGrowths[2].Harvest_DOY) and Already_Done_Crop_Sum_Output[2] == False:
        WriteCropSummaryOutput(2, DOY, CropSumOutputs, 
                               pSoilFlux, pSoilState, pSoilModelLayer, 
                               pETState,CropGrowths[2])
        Already_Done_Crop_Sum_Output[2] = True
        
    if (Crop_Number == 1 and DOY == CropGrowths[1].Harvest_DOY) or \
       (Crop_Number == 2 and DOY == CropGrowths[2].Harvest_DOY):
        Crop_Number = 0
        DAE = 0
        
        
    if Crop_Active: 
        DAE += 1
    DOY += 1
    if DOY > 365:
        DOY = 1
        Year_Number += 1
    Days_Elapsed += 1

WriteTotalSimPeriodOutput(TotalSimPeriodOutput, Run_Last_Doy, SoilLayers, 
                          pSoilState, pSoilFlux)

for crop in range(1,Number_Of_Crops + 1):
    CropOutputs[crop].to_csv(f'{output_path}/FM_{Farm_Name}_FD_{Field_Name}_crop_{crop}_{crop_output_excel_csv}',index=False)
    SoilOutputs[crop].to_csv(f'{output_path}/FM_{Farm_Name}_FD_{Field_Name}_crop_{crop}_{soil_output_excel_csv}',index=False)
    CropSumOutputs[crop].T.reset_index().to_csv(f'{output_path}/FM_{Farm_Name}_FD_{Field_Name}_crop_{crop}_CropSum.csv',index=False,header=True)
    DailyBudgetOutputs[crop].to_csv(f'{output_path}/FM_{Farm_Name}_FD_{Field_Name}_crop_{crop}_{budget_output_excel_csv}',index=False)
TotalSimPeriodOutput.T.reset_index().to_csv(f'{output_path}/FM_{Farm_Name}_FD_{Field_Name}_TotalSimPeriodOutput.csv',index=False,header=True)
FieldManagementsLogsOutput.to_csv(f'{output_path}/FM_{Farm_Name}_FD_{Field_Name}_FieldManagementLogs.csv',index=False)
