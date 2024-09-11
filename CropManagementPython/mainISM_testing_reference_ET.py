#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 17:37:40 2024

@author: liuming
"""
import pandas as pd
from datetime import datetime
from ism_irrigationscheduler import *
from accessagweathernet import *
from ism_default_parameters import *

def convert_mj_day_m2_to_w_m2(mj_day_m2):
    return mj_day_m2 * 11.5741

#location info
STATION_ID = "100031"
AnemomH = 1.5 #m
lat = agweathernetstation.at[int(STATION_ID),'Latitude(N)']
elev = agweathernetstation.at[int(STATION_ID),'Station Elevation (ft)']        #ft


soilID = 4 #Sandy Loam
cropID = 65 #Grain (Winter)


START = "2017-01-01"
END = "2017-12-31"
bdaily = True

#
data = fetch_AgWeatherNet_data(STATION_ID,START,END,bdaily)
pd.set_option('display.max_columns', None)
#print(data.columns)
#print(data)

if not bdaily:
    daily = aggregate_to_daily(data)
    daily['TIMESTAMP_PST'] = pd.to_datetime(daily['TIMESTAMP_PST'])
    # Format the datetime to the string format 'YYYY-MM-DD'
    daily['TIMESTAMP_PST'] = daily['TIMESTAMP_PST'].dt.strftime('%Y-%m-%d')
else:
    daily = data
    daily = daily.rename(columns={'JULDATE_PST': 'TIMESTAMP_PST'})
    daily = daily.sort_values(by='TIMESTAMP_PST')
    
daily['ET0_ISM'] = .0
daily['ETR_ISM'] = .0
daily['ET0_Harg'] = .0
daily['ETR_Harg'] = .0
daily['jd'] = 0
#print(daily)
for index, row in daily.iterrows():
    tmax = row['MAX_AT_F']
    tmin = row['MIN_AT_F']
    RHmax = row['MAX_REL_HUMIDITY']
    RHmin = row['MIN_REL_HUMIDITY']
    tdew = row['AVG_DEWPT_F']
    
    date_obj = datetime.strptime(row['TIMESTAMP_PST'], '%Y-%m-%d')
    jd = date_obj.timetuple().tm_yday
    #print(f'tmax:{tmax} tmin:{tmin} RHmax:{RHmax} RHmin:{RHmin} tdew:{tdew} jd:{jd}')
    if tdew is None:
        print('calc tdew')
        tdew = calc_tdew(tmax,tmin,RHmax,RHmin)
    rs = convert_mj_day_m2_to_w_m2(row['SR_MJM2'])
    wr = row['WS_MPH'] * 24.0                                                  #miles per day
    etr,et0 = ETCalc(tmax, tmin, tdew, rs, wr, jd, lat, elev, AnemomH)
    #print(f'tmax:{tmax}, tmin:{tmin}, tdew:{tdew}, rs:{rs}, wr:{wr}, jd:{jd}, lat:{lat}, elev:{elev}, AnemomH:{AnemomH},etr:{etr},et0:{et0}')
    etr_Harg,et0_Harg = ETHarg(jd, tmax, tmin, lat)
    
    daily.at[index,'ETR_ISM'] = etr
    daily.at[index,'ET0_ISM'] = et0
    daily.at[index,'ETR_Harg'] = etr_Harg
    daily.at[index,'ET0_Harg'] = et0_Harg
    daily.at[index,'jd'] = jd

print(daily)
"""
print(f'ETHarg(in):{ETHarg(jd, tmax, tmin, lat)}')

RHmax = 90.
RHmin = 70.
tdew = calc_tdew(tmax,tmin,RHmax,RHmin)
print(f'tdew(F):{tdew}')

rs = 300. #W/m2
wr = 100. #miles/day
elv = 300. #ft
AnemomH = 1.5 #m
etr,eto = ETCalc(tmax, tmin, tdew, rs, wr, jd, lat, elv, AnemomH)
print(f'ETCalc(in) etr:{etr} eto:{eto}')

doy = 200
kc1 = 0.1
kc2 = 0.9
kc3 = 0.6
plantDate = 100
maxDate = 150
declineDate = 200
endGrowthDate = 250
seasonEndDate = 300
lastForage = 201
partA = 20
partB = 20
kcdict = dict()
for doy in range(plantDate,seasonEndDate):
  kc = calculateKC(doy, kc1, kc2, kc3, plantDate, maxDate, declineDate,
                     endGrowthDate, seasonEndDate, lastForage, partA, partB)
  kcdict[doy] = kc
  #print(f'doy:{doy} kc:{kc}')


"""
# Example data
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
x = list(daily['jd'])
#y = list(daily['ETO'])
# Plotting the scatter plot

#plt.plot(x, daily['ETO'], color='red', linestyle='-', linewidth=3, label='ETO')
#plt.plot(x, daily['ET0_ISM'], color='blue', linestyle='-', linewidth=3, label='ET0_ISM')
#plt.plot(x, daily['ET0_Harg'], color='yellow', linestyle='-', linewidth=3, label='ET0_Harg')

plt.plot(x, daily['ETR'], color='red', linestyle='-', linewidth=1, label='ETR')
plt.plot(x, daily['ETR_ISM'], color='blue', linestyle='-', linewidth=1, label='ETR_ISM')
plt.plot(x, daily['ETR_Harg'], color='yellow', linestyle='-', linewidth=1, label='ETR_Harg')

# Adding labels and title
plt.xlabel('DOY')
plt.ylabel('Inch/day')
plt.title('ET')
plt.legend()
# Display the plot
plt.show()

