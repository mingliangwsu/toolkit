# -*- coding: utf-8 -*-
"""IrrigationScheduler.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zVitnCcniP7oKiDmrR2uzaWaRlCJcCb8
"""

import math
M_PI = math.pi

def CalcSVP(airTemp):
        #Calculates the saturation vapor pressure at the given air temperature
    #airTemp degree Celsius
    svp = .6108 * math.exp ( (17.27 * airTemp) / (airTemp + 237.3) );
    return svp

def ETHarg(jd, tmax, tmin, lat):
    #Written by Troy Peters March, 2013
        #Calculates grass reference ETo in mm using the Hargreaves temperature method then converts to alfala reference ETr in inches.
        #inputs are: jd is Day of Year. tmax, and tmin are in maximum and minimum temperature delivered in deg F. latitude is in decimal degrees.
        tmax = (tmax - 32.) / 1.8                                                    #convert to deg C
        tmin = (tmin - 32.) / 1.8
        tavg = (tmax + tmin) / 2.0
        LAMBDA = 2.5 - 0.002361 * tavg
        lat = lat * M_PI / 180.                                                     #Convert to radians
        SmallDelta = 0.409 * math.sin (2 * M_PI / 365. * jd - 1.39)
        omega = math.acos(-math.tan(lat) * math.tan(SmallDelta));
        dr = 1. + 0.033 * math.cos(2. * M_PI * jd / 365.)
        Ra = 37.586 * dr * (omega * math.sin(lat) * math.sin(SmallDelta) \
         + math.cos(lat) * math.cos(SmallDelta) * math.sin(omega))
        eto = 0.0023 * (tavg + 17.8) * math.sqrt(tmax - tmin) * Ra / LAMBDA
        eto /= 25.4                                                                 #convert back to inches
        etr = eto * 1.2                                                             #use a constant of 1.2 for converting ETo to ETr.
        return etr,eto #inches

def ETCalc(tmax, tmin, tdew, rs, wr, jd, lat, elv, AnemomH):
    #return ETr & ETo in inches per day
        #check for valid number of arguments
        #if (func_num_args () != 11) {
      #            print ( "<br /><br />One or more function arguments is missing!<br />Please contact the AWN systems administrator.<br />" );
        #        trigger_error ( "One or more function arguments is missing", E_USER_ERROR );
        #        return (False);
        #}

    #tmax -> max average air tmp (deg F)
    #tmin -> min average air tmp (deg F)
    #tdew -> average dewpoint (deg F)
    #rs -> total solar radiation (W/m^2/day)
    #wr -> wind run (miles/day)
    #jd -> julian day of year
    #lat -> latitude
    #elv -> elevation (ft)
    #AnemomH -> elevation of anemometer (m)
    #P -> pressure (kPa)
    #D -> declination (for Ra calculation) radians, eq 27 Allen et al., 1989
    #WS -> sunset hr angle, radians, eq 29/30: Allen et al 1989
    #RA -> daily values of extraterrestrial radiation
    #RSO -> clear sky radiation MJ m-2 day-1
    #sigma -> Stephen-Boltsmann constant 4.903x10-9 MJ m-2 day-1 K-4
    #Gsc -> 0.08202 MJ m-2 min-1 = 1367 W m-2; Allen et al 1989 (solar constant)
    #TA -> avg of Tmax, Tmin
    #TMAXK -> max air T in Kelvin
    #TMINK -> min air T in Kelvin
    #TMEANK -> avg air T in Kelvin
    #ED -> saturation vapor pressure @dewpt T (kPa)
    #alpha -> albedo, allen et al, Wright (1982)
    #RN -> net radiation (MJ m-2 day-1)
    #RNG -> Grass ref ET, note differences
    #G -> soil heat flux
    #cs -> general heat conductance for soil surface cs = 0.38 MJ m-2 day-1 C-1 for silt loam
    #ETAV -> sat VP @TA
    #LHVP -> patent heat of vaporization Allen et al 1989[35], Harris (1963)
    #GAMMA -> psychromatric constant (kPa C-1) eq [34]
    #DELTA -> slope of sat VP eq [33]
    #ETX -> sat VP @ Tmax
    #ETN -> satVP @Tmin
    #EAV -> avg sat VP @ ETX,ETN
    #EA -> [eq 10] general Penman form alfalfa : wind/vapor term Allen et al 1989
    #EAG -> [eq 10} Allen et al 1989; general Penman Grass, wind/vapor term
    #ETR -> reference ET, general Penman
    #ETO -> ref ET Grass
    #grass or alfalfa ET differ by the way sat VP is handled. Grass is SVP@TA. Alfalfa is SVP@meanSVP@Tmax, SVP@Tmin

    #check for valid data, if not return na
    if ((rs is None) or (wr is None) or (tmax is None) or (tmin is None) or (tdew is None)):
      eto = None    #bad data, return NA
      etr = None
      return etr,eto


    #convert the input values to metric, etc.
    rs *= 0.0864       #this is original:0.0036             #Watts/M2/Day to MJ/M2/Day
    wr /= 53.6865                     #miles/day to m/s
    tmax = (tmax - 32.) / 1.8     #degree F -> degree C
    tmin = (tmin - 32.) / 1.8     #degree F -> degree C
    tdew = (tdew - 32.) / 1.8     #degree F -> degree C
    elv *= 0.3048                     #feet to meters
    ETR = 0                                #initialize values
    ETO = 0
    #if (lat == 0) lat = 46.7        #check if latitude and elevation are there.  If not use some default values.
    #if (elv == 0) elv = 250
    PI = M_PI                         #php constant
    PHI = lat * PI / 180.            #convert to radians
    P = 101.3 * math.pow((293 - .0065 * elv) / 293, 5.26 )    #pressure
    D = 0.409 * math.sin(2. * PI * jd/ 365 - 1.39 )                #solar declination
    DR = 1. + 0.033 * math.cos(2 * PI * jd/ 365)
    WS = math.atan( - (- math.tan(PHI) * math.tan(D)) / math.sqrt (-(-math.tan(PHI) * math.tan(D)) * (-math.tan(PHI)* math.tan(D)) + 1.)) + 2. * math.atan(1)    #sunset angle
    RA = 37.586 * DR * (WS * math.sin(PHI) * math.sin(D) + math.cos(PHI) * math.cos(D) * math.sin(WS)) #daily radiation
    RSO = RA * (0.75 + 0.00002 * elv)    #clear sky radiation
    Rns = 0.77 * rs
    RsRso = rs / RSO
    if (RsRso < .3): RsRso = .3
    if (RsRso > 1): RsRso = 1
    Fcd = 1.35 * RsRso - .35
    if (Fcd < .05): Fcd = .05
    if (Fcd > 1): Fcd = 1
    TMAXK = tmax + 273.16                #convert max and min temps to degree kelvin
    TMINK = tmin + 273.16
    TA = (tmax + tmin) / 2.                #avg of max and min temps
    TMEANK = TA + 273.16                #avg air temp in degree kelvin
    ED = CalcSVP(tdew)        #saturation vapor pressure at dewpoint
    #net radiation
    Rnl = 0.0000000049 * (math.pow(TMAXK, 4) + math.pow(TMINK, 4)) / 2. * (0.34 - 0.14 * math.sqrt(ED)) * Fcd
    RN = Rns - Rnl

    RNG = 0.75 * rs - 0.000000004903 * (math.pow(TMEANK, 4) * (0.34 - 0.139 * math.pow(ED, .5)) * (1.35 * rs / RSO - 0.35))    #grass ref et
    G = 0.                                                #soil heat flux
    ETAV = CalcSVP(TA)        #sat VP @ TA
    LHVP = 2.5002 - 0.002361 * TA    #patent heat of vaporiation
    GAMMA = 0.000665 * P                #pychromatric constant (kPa C-1)
    DELTA = 4099 * (0.6108 * math.exp(17.27 * TA / (TA + 237.3))) / (pow ((TA + 237.3), 2 ))    #slope of sat VP curve
    ETX = CalcSVP (tmax)        #sat VP at tmax
    ETN = CalcSVP (tmin)        #sat VP at tmin
    EAV = (ETX + ETN) / 2.                #avg sta VP @ ETX, ETN
    U2 = wr * 4.87 / (math.log(67.8 * AnemomH - 5.42));    #equivalent wind speed at 2 m
    print(f'rs:{rs} U2:{U2} DELTA:{DELTA} RN:{RN} G:{G} TA:{TA} EAV:{EAV} ED:{ED}')

    #Alfalfa Reference ET (ETr) Cn = 1600, Cd = 0.38
    Numerator = 0.408 * DELTA * (RN - G) + GAMMA * 1600 / (TA + 273) * U2 * (EAV - ED)
    Denominator = DELTA + GAMMA * (1. + 0.38 * U2)
    ETR = Numerator / Denominator

    #Grass Reference ET (Eto) Cn = 900, Cd = 0.34. Reuse variable names.
    Numerator = 0.408 * DELTA * (RN - G) + GAMMA * 900 / (TA + 273) * U2 * (EAV - ED)
    Denominator = DELTA + GAMMA * (1 + 0.34 * U2)
    ETO = Numerator / Denominator

    if (ETR < 0): ETR = 0.
    etr = ETR / 25.4 #convert from mm to inches

    if (ETO < 0): ETO = 0.
    eto = ETO / 25.4 #convert from mm to inches
    return etr,eto #inches

def calc_tdew(Tmax,Tmin,RHmax,RHmin):
    #Tmax: F
    #Tmin: F
    #RHmax,RHmin: %
    TAvg = (Tmax + Tmin)/2.
    RHAvg = (RHmax + RHmin)/2.
    if (TAvg > 150 or TAvg < -50 or RHAvg > 100 or RHAvg < 0):
        dewPoint = None
    else:
        if (RHAvg == 100.):
            dewPoint = TAvg
        else:
                TAvgc = (TAvg - 32.) * 5. / 9.

                MySVP = (6.107799961
                  + 4.436518521E-1 * TAvgc
                  + 1.428945805E-2 * TAvgc * TAvgc
                  + 2.650648471E-4 * TAvgc * TAvgc * TAvgc
                  + 3.031240396E-6 * TAvgc * TAvgc * TAvgc * TAvgc
                  + 2.034080948E-8 * TAvgc * TAvgc * TAvgc * TAvgc * TAvgc
                  + 6.136820929E-11 * TAvgc * TAvgc * TAvgc * TAvgc * TAvgc * TAvgc) / 10.
                if(TAvgc < 0): MySVP = -0.00486 + 0.85471 * MySVP + 0.2441 * MySVP * MySVP
                MyVp = RHAvg * MySVP/ 100.
                dewPointC = (241.88 * math.log(MyVp / 0.61078)) / (17.558 - math.log(MyVp / 0.61078))
                dewPoint = dewPointC * 9. / 5. + 32. #F
    return dewPoint #F

def calculateKC(doy, kc1, kc2, kc3, plantDate, maxDate, declineDate,
                     endGrowthDate, seasonEndDate, lastForage, partA, partB):
    #kc1: initial crop coefficient
    #kc2: full cover crop coefficient
    #kc3: final crop coefficient
    #maxDate: 10pcnt date
    #declineDate: the first day the Kc reaches max
    #endGrowthDate: the date of first growth decline
    #seasonEndDate: the last day
    #partA: postCuttingFlatDays
    #partB: postCuttingRecoveryDays
    #lastForage: when the last cut was

    if (doy < maxDate):
        kcVal = kc1
        maxBeforeMax = kcVal
        #kc2rate = 0
    elif (doy > endGrowthDate):
        mult = doy - endGrowthDate
        kc3days = seasonEndDate - endGrowthDate
        rate = (kc3 - kc2)/kc3days
        increment = rate * mult
        kcVal = kc2 + increment
        maxAfterEnd = kcVal
        #kc2rate = 0
    elif (doy >= maxDate and doy < declineDate):
        mult = doy - maxDate
        numDays =  declineDate - maxDate
        if (numDays == 0): numDays = 1
        rate = (kc2-kc1)/numDays
        increment = rate * mult
        kcVal = kc1 + increment
        maxBeforeDecline = kcVal
        #kc2rate = 0
    elif (doy >= declineDate and doy <= endGrowthDate):
        kcVal = kc2
        maxBeforeEnd = kcVal
        #kc2rate = 0
    #cutting events
    if (partA is not None and partB is not None and lastForage is not None
        and doy >= lastForage and doy <= (lastForage + partA + partB)):
        if (doy <= (lastForage + partA)):
            kcVal = kc1
            #kc2rate = 0
        else:
            mult = doy - (lastForage + partA)
            rate = (kc2 - kc1)/partB
            increment = rate * mult
            kcVal = kc1 + increment
            #kc2rate = 0
        if (doy < maxDate and kcVal > maxBeforeMax):
            kcVal = maxBeforeMax
        if (doy >= maxDate and doy < declineDate and kcVal > maxBeforeDecline):
            kcVal = maxBeforeDecline
        if (doy >= declineDate and doy < endGrowthDate and kcVal > maxBeforeEnd):
            kcVal = maxBeforeEnd
        if (doy > endGrowthDate and kcVal > maxAfterEnd):
            kcVal = maxAfterEnd
    return kcVal

def rootGrowthRate(maxRootDepth, startingRootDepth, growthMaxDate, plantDate):
    return (maxRootDepth - startingRootDepth)/(growthMaxDate - plantDate)

def rootZone(doy, prevRootZone, rz_val1, rz_val2, plantDate, growthMaxDate):
    #rz_val1: startingRootDepth
    #rz_val2: maxRootDepth
    if (doy > growthMaxDate):
        rootZone = prevRootZone
    elif (doy < plantDate):
        rootZone = 0
    else:
        rootZone = (doy - plantDate) * rootGrowthRate(rz_val2, rz_val1, growthMaxDate, plantDate) + rz_val1
    return rootZone

def calcKs(currentSoilProfileWaterStorage,
           waterStorageAtMad,waterStorageAtPermanentWiltingPoint):
    Ks = (currentSoilProfileWaterStorage - waterStorageAtPermanentWiltingPoint) \
          / (waterStorageAtMad - waterStorageAtPermanentWiltingPoint)
    if Ks > 1: 
        Ks = 1
    elif Ks < 0:
        Ks = 0
    return Ks

def calculateAvailableSoilWaterContentAbovePWP(calculatedSoilWaterAvailability,availableWaterAtFieldCapacity):
    if(((calculatedSoilWaterAvailability/100) * availableWaterAtFieldCapacity) < 0):
        availableSoilWaterContentAbovePWP = 0
    else:
        availableSoilWaterContentAbovePWP = (calculatedSoilWaterAvailability/100) * availableWaterAtFieldCapacity
    return availableSoilWaterContentAbovePWP

def calculateCurrentDay(cnt,plantDate,availableSoilWaterContentAbovePWP,
                        calculatedSoilWaterAvailability,currentSoilProfileWaterStorage,
                        waterStorageAtFieldCapacityCurrentDay,msdPcnt, sumPrecipCurrentDay, irrigationAppliedCurrentDay, 
                        ET, deepPercolationCurrentDay, waterStorageAtPermanentWiltingPoint, 
                        availableWaterAtFieldCapacity,row_tblIndividField):
        modifiedCurrentDay = 0
        #//On the first day of the season, assume 100 percent available water unless there is a measured percent
        if (cnt == plantDate and msdPcnt is None):
            #// error_log("Assuming 100 percent");
            availableSoilWaterContentAbovePWP = 100
            calculatedSoilWaterAvailability = 100
            currentSoilProfileWaterStorage = waterStorageAtFieldCapacityCurrentDay
        elif msdPcnt is None:  #it is not the first day, and we don't use a measured percent
            #// yesterdays water storage ($v1)
            #// + todays rain 
            #// + todays irrigation ($v2)
            #// - todays evapotranspiration 
            #// + the water storage at field capacity 
            #// - yesterdays water storage at field capacity ($V3) = 
            #// potential current soil profile water storage???
            v1 = row_tblIndividField[cnt-1]['currentSoilProfileWaterStorage']
            v2 = irrigationAppliedCurrentDay
            v3 = row_tblIndividField[cnt-1]['waterStorageAtFieldCapacity']
            sumValue = v1 \
                                    + sumPrecipCurrentDay \
                                    + v2 \
                                    - ET \
                                    + waterStorageAtFieldCapacityCurrentDay \
                                    - v3
            if (sumValue < 0): #//if that is negative, then 0
                sumValue = 0
            
            if (waterStorageAtFieldCapacityCurrentDay > sumValue): #//if todays water stoarage is less than the max
                currentSoilProfileWaterStorage = sumValue  #//then currentSoilProfileWaterStorage = the calculate value
            else:
                #//If there was more water than the field could hold, the extra water is the calculated value - the total field capacity
                deepPercolationCurrentDay = sumValue - waterStorageAtFieldCapacityCurrentDay
                #//and currentSoilProfileWaterStorage = the field capacity
                currentSoilProfileWaterStorage = waterStorageAtFieldCapacityCurrentDay
            
            calculatedSoilWaterAvailability = (currentSoilProfileWaterStorage - waterStorageAtPermanentWiltingPoint) \
                                               / (waterStorageAtFieldCapacityCurrentDay - waterStorageAtPermanentWiltingPoint)
            if calculatedSoilWaterAvailability > 1:
                calculatedSoilWaterAvailability = 100
            elif calculatedSoilWaterAvailability > 0:
                calculatedSoilWaterAvailability *= 100
            else:
                calculatedSoilWaterAvailability = 0
        else: #// The user entered a measured or corrected percent value
            currentSoilProfileWaterStorage = msdPcnt/100 * availableWaterAtFieldCapacity + waterStorageAtPermanentWiltingPoint
            calculatedSoilWaterAvailability = msdPcnt #//$this->row_tblIndividField[$cnt]['measdPcntAvail']
            modifiedCurrentDay = True
        return availableSoilWaterContentAbovePWP,calculatedSoilWaterAvailability, \
               currentSoilProfileWaterStorage,deepPercolationCurrentDay,modifiedCurrentDay