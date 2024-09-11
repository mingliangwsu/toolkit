#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 16:31:34 2024

@author: liuming
"""

from ism_default_parameters import *
from ism_irrigationscheduler import *
from ism_precipitation_and_applicationrate import *
from accessagweathernet import *

def updateValues(thisfield, updateFlag, currentYear, todayDOY, row_tblIndividField):
    #todaysDate = date("M d, Y");
    groundWetted = thisfield['groundWetted']/100
    
    cropinfo = thisfield['cropInfo']
    soilinfo = thisfield['soilInfo']
    
    numDays = int(cropinfo['growthDeclineDate'] - cropinfo['growthMaxDate'])
    rootNumDays = cropinfo['growthDeclineDate'] - cropinfo['plantDate']
    rootGrowthPerDay = (cropinfo['rz_val2'] - cropinfo['rz_val1']) / rootNumDays
    rootDepth = cropinfo['rz_val1'] #(ft)
    kc1 = cropinfo['kc1']
    kc2 = cropinfo['kc2']
    kc3 = cropinfo['kc3']
    partA, partB = None,None
    
    soilCapacityField = soilinfo['soilFC'] * groundWetted    #(in/ft) adjust for when not all the soil is used to store water
    soilAvailableWaterContent = soilinfo['soilAWC'] * groundWetted
    #crop = cropinfo['cropID']
    mad = cropinfo['mad']/100
    #fieldYear =     $this->row_FieldInfo['year']
    plantDate = int(cropinfo['plantDate'])
    if 'seasonEndDate' in cropinfo:
        seasonEndDate = int(cropinfo['seasonEndDate'])
    else:
        seasonEndDate = int(cropinfo['growthEndDate']) + 5 #+5 days
    #useOnOff = $this->row_FieldInfo['useOnOff']; //Do we use the on off status 
    #applicationrate = $this->row_FieldInfo['applicationrate']
    kcVal = kc1   #Start season at kc1

    # $time_start_updateValues = microtime(true); 
    #etrArray = $this->getWeatherData($updateFlag);
    lastForage = -1
    
    # Used to revise the entire schedule if someone changes the application rate.
    #$oldAppRate = 0;
    #if (isset($_SESSION['OldAppRate']))  {
    #        $oldAppRate = $_SESSION['OldAppRate'];
    #        unset($_SESSION['OldAppRate']);
    #}

     #Go through and apply any water that is set in a schedule that has not been applied yet
     #updateFlag = $this->applySchedule() || $updateFlag;

     #onOffStatus = 0    #Default to off
     #   $previousOnOffStatus = 0; //Default to off
     #   $onOffModified = 0; //Default to not modified
     #   $this->badETdata = 0;
     #   $todayDOY = date("z")+1;
    if todayDOY < plantDate: todayDOY = plantDate
    if(seasonEndDate < (todayDOY + 7)):
        LoopStopDate = int(seasonEndDate)
    else: 
        LoopStopDate = int(todayDOY + 7)
     
    #get agWeather daily climate data
    sy,sm,sd = get_date_from_YDOY(currentYear,plantDate)
    ey,em,ed = get_date_from_YDOY(currentYear,LoopStopDate)
    start_date = f'{sy}-{sm:02}-{sd:02}'
    end_date = f'{ey}-{em:02}-{ed:02}'
    bdaily = True
    data = fetch_AgWeatherNet_data(thisfield['stationID'],start_date,end_date,bdaily)  #start from plantDate
    lat = float(thisfield['stationInfo']['Latitude(N)'])
    elev = float(thisfield['stationInfo']['Station Elevation (ft)']) #ft

    
    #Main Loop.  Once for every day
    idx = 0
    badETdata = 0
    currentSoilProfileWaterStorage = 100                                       #will be updated in the first day
    availableSoilWaterContentAbovePWP = 100                                    #will be updated in the first day
    calculatedSoilWaterAvailability = 100                                      #will be updated in the first day
    msdPcnt = None
    for cnt in range(plantDate, LoopStopDate + 1):
        print(f'cnt:{cnt}')
        ty,tm,td = get_date_from_YDOY(currentYear,cnt)
        row_tblIndividField[cnt] = dict()
        jd = cnt
        ET = data.at[idx,'ETR']
        prec = data.at[idx,'P_INCHES'] #inch
        todayHasBadData = False
        sumPrecipCurrentDay = 0
        if prec is not None: sumPrecipCurrentDay += prec
        
        if pd.isnull(ET):
            tmax = data.at[idx,'MAX_AT_F']
            tmin = data.at[idx,'MIN_AT_F']
            tdew = data.at[idx,'AVG_DEWPT_F']
            RHmax = data.at[idx,'MAX_REL_HUMIDITY']
            RHmin = data.at[idx,'MIN_REL_HUMIDITY']
            rs_MJM2 = data.at[idx,'SR_MJM2']
            #prec
            AnemomH = 1.5 #m
            if not pd.isnull(rs_MJM2):
                rs = convert_mj_day_m2_to_w_m2(data.at[idx,'SR_MJM2'])
            else:
                rs = None
            wr_MPH = data.at[idx,'WS_MPH']
            if not pd.isnull(wr_MPH):
                wr = data.at[idx,'WS_MPH'] * 24.0                                                  #miles per day
            else:
                wr = None
            
            if pd.isnull(tdew):
                print('calc tdew')
                if not pd.isnull(tmax) and not pd.isnull(tmin) \
                    and not pd.isnull(RHmax) and not pd.isnull(RHmin):
                    tdew = calc_tdew(tmax,tmin,RHmax,RHmin)
            if not pd.isnull(tmax) and not pd.isnull(tmin) and not pd.isnull(tmin) \
                and not pd.isnull(tdew) and not pd.isnull(rs) and not pd.isnull(wr):
                etr,et0 = ETCalc(tmax, tmin, tdew, rs, wr, jd, lat, elev, AnemomH)
            elif not pd.isnull(tmax) and not pd.isnull(tmin):
                #print(f'tmax:{tmax}, tmin:{tmin}, tdew:{tdew}, rs:{rs}, wr:{wr}, jd:{jd}, lat:{lat}, elev:{elev}, AnemomH:{AnemomH},etr:{etr},et0:{et0}')
                etr,et0 = ETHarg(jd, tmax, tmin, lat)
            else:
                etr,et0 = None,None
            if pd.isnull(etr):
                todayHasBadData = True
                ET = 0  #CHECK!!!
            else:
                ET = etr
            if todayHasBadData:
                if cnt<todayDOY:
                    badETdata += 1  #Increment bad data to display the warning message    
                else:
                    todayHasBadData = False    #Need to overwrite because we never have ET values for today and we don't want to flag bad values during the forecast.
        if ET < 0: ET = 0
        oetr = ET                                                              #for output etr
        
        waterStorageAtFieldCapacityCurrentDay = soilCapacityField * (rootDepth/12) #ft?
        waterStorageAtPermanentWiltingPoint = waterStorageAtFieldCapacityCurrentDay - (soilAvailableWaterContent * (rootDepth/12))
        availableWaterAtFieldCapacity = waterStorageAtFieldCapacityCurrentDay - waterStorageAtPermanentWiltingPoint
        waterStorageAtMad = (1 - mad) * availableWaterAtFieldCapacity + waterStorageAtPermanentWiltingPoint
        
        irrigationAppliedCurrentDay = 0 #User set
        if autoirrigation and currentSoilProfileWaterStorage < waterStorageAtMad:
                irrigationAppliedCurrentDay = waterStorageAtFieldCapacityCurrentDay - currentSoilProfileWaterStorage
        #row_tblIndividField[cnt]['irrig'] = irrigationAppliedCurrentDay        #for calculating today's water balance


        #The variable names here are a little off. growthMaxDate is actually 10pcnt date (first day of Kcs begin increasing), growthDeclineDate is actually the first day the Kc reaches max, growthEndDate is actually the date of first growth decline, and season end date is the last day.  
        # However fixing it requires reworking the entire database and it would threaten the historical field data and it works fine as it is.
        kcVal = calculateKC(cnt, kc1, kc2, kc3, plantDate, 
                            int(cropinfo['growthMaxDate']), int(cropinfo['growthDeclineDate']), 
                            int(cropinfo['growthEndDate']), seasonEndDate, lastForage, partA, partB)
        Ks = calcKs(currentSoilProfileWaterStorage,waterStorageAtMad,waterStorageAtPermanentWiltingPoint)
        if cnt > plantDate:
            currentSoilProfileWaterStoragePreviousDay = currentSoilProfileWaterStorage
            waterStorageAtMadPreviousDay = row_tblIndividField[cnt-1]['waterStorageAtMad']

        ET = ET * kcVal * Ks
        deepPercolationCurrentDay = 0 #Initialize
        availableSoilWaterContentAbovePWP,calculatedSoilWaterAvailability, \
               currentSoilProfileWaterStorage,deepPercolationCurrentDay, \
               modifiedCurrentDay = calculateCurrentDay(cnt,plantDate,
                                                        availableSoilWaterContentAbovePWP,
                                                        calculatedSoilWaterAvailability,
                                                        currentSoilProfileWaterStorage,
                                                        waterStorageAtFieldCapacityCurrentDay,
                                                        msdPcnt, 
                                                        sumPrecipCurrentDay, 
                                                        irrigationAppliedCurrentDay,
                                                        ET, 
                                                        deepPercolationCurrentDay, 
                                                        waterStorageAtPermanentWiltingPoint,
                                                        availableWaterAtFieldCapacity,
                                                        row_tblIndividField)
        availableSoilWaterContentAbovePWP = calculateAvailableSoilWaterContentAbovePWP(calculatedSoilWaterAvailability,
                                                                                       availableWaterAtFieldCapacity)
        rootZoneWaterDeficit = waterStorageAtFieldCapacityCurrentDay - currentSoilProfileWaterStorage
        notes = ""
        #if(isset($this->row_tblIndividField[$cnt]['notes']))
        #    $notes = $this->row_tblIndividField[$cnt]['notes'];

        suspend = 0
        #if(isset($this->row_tblIndividField[$cnt]['suspend']))
        #    $suspend = $this->row_tblIndividField[$cnt]['suspend'];
            
        row_tblIndividField[cnt]['doy'] = cnt
        row_tblIndividField[cnt]['fieldYear'] = currentYear
        row_tblIndividField[cnt]['fieldDate'] = f'{ty}-{tm:02}-{td:02}'
        row_tblIndividField[cnt]['individFieldID'] = individFieldID
        row_tblIndividField[cnt]['fcWater'] = waterStorageAtFieldCapacityCurrentDay
        row_tblIndividField[cnt]['wpWater'] = availableWaterAtFieldCapacity
        row_tblIndividField[cnt]['madWater'] = waterStorageAtMad
        row_tblIndividField[cnt]['kc'] = kcVal
        row_tblIndividField[cnt]['etr'] = oetr
        row_tblIndividField[cnt]['etc'] = ET
        row_tblIndividField[cnt]['rain'] = sumPrecipCurrentDay
        row_tblIndividField[cnt]['irrig'] = irrigationAppliedCurrentDay
        row_tblIndividField[cnt]['measdPcntAvail'] = msdPcnt
        row_tblIndividField[cnt]['modified'] = modifiedCurrentDay
        row_tblIndividField[cnt]['rootDepth'] = rootDepth
        row_tblIndividField[cnt]['waterStorageAtFieldCapacity'] = waterStorageAtFieldCapacityCurrentDay
        row_tblIndividField[cnt]['waterStorageAtMad'] = waterStorageAtMad
        row_tblIndividField[cnt]['availableSoilWaterContentAbovePWP'] = availableSoilWaterContentAbovePWP
        row_tblIndividField[cnt]['waterStorageAtPermanentWiltingPoint'] = waterStorageAtPermanentWiltingPoint
        row_tblIndividField[cnt]['rootZoneWaterDeficit'] = rootZoneWaterDeficit
        row_tblIndividField[cnt]['calculatedSoilWaterAvailability'] = calculatedSoilWaterAvailability
        row_tblIndividField[cnt]['deepPercolation'] = deepPercolationCurrentDay
        row_tblIndividField[cnt]['Ks'] = Ks
        row_tblIndividField[cnt]['notes'] = notes
        row_tblIndividField[cnt]['suspend'] = suspend
        #row_tblIndividField[cnt]['simpleOnOffStatus'] = onOffStatus
        #row_tblIndividField[cnt]['simpleOnOffModified'] = onOffModified
        row_tblIndividField[cnt]['todayHasBadData'] = todayHasBadData
        row_tblIndividField[cnt]['currentSoilProfileWaterStorage'] = currentSoilProfileWaterStorage
        #roots grow at end of day
        if cnt < int(cropinfo['growthDeclineDate']): rootDepth += rootGrowthPerDay
        idx += 1
    df = pd.DataFrame.from_dict(row_tblIndividField, orient='index')
    return df




outfile = '/home/liuming/mnt/hydronas3/Projects/CropManagement/test_results/ism_output.csv'

#field infomation
#plon,plat = -120.45332,46.97603  #YKB this is for location-based information

#get info from parameters
fieldInfo = dict()

#one field
fieldName = 'test1'
individFieldID = 0
autoirrigation = True #
fieldInfo[fieldName] = dict()

thisField = fieldInfo[fieldName]
thisField['fieldName'] = fieldName

agWeatherStation = '100031' #McNary
thisField['stationID'] = agWeatherStation
thisField['stationInfo'] = agweathernetstation.loc[int(agWeatherStation)].squeeze()
if int(agWeatherStation) in stationregion.index:
    cropRegionCode = stationregion.loc[int(agWeatherStation)]['regionID']
else:
    print(f'{agWeatherStation} is not in stationRegion Table, set region as default\n')
    cropRegionCode = 720 #default

cropName = 'Tomatoes'
soilType = 'Loamy Sand'
thisField['groundWetted'] = 100 #percentage


#get soil & crop info
if soilType in soilparameter.index:
    thisField['soilInfo'] = soilparameter.loc[soilType].squeeze()
else:
    thisField['soilInfo'] = None
if cropName in cropparameter.index:
    thisField['cropInfo'] = cropparameter.loc[cropName][cropparameter.loc[cropName,'cropRegion'] == cropRegionCode].squeeze()
else:
    thisField['cropInfo'] = None


#def updateValues(thisfield, updateFlag, currentYear, todayDOY):
row_tblIndividField = dict()
thisfield = thisField
currentYear = 2023
todayDOY = 300
updateFlag = True
df = updateValues(thisfield, updateFlag, currentYear, todayDOY, row_tblIndividField)
df.to_csv(outfile, index=False)