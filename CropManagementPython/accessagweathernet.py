# -*- coding: utf-8 -*-
"""accessAgWeatherNet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1p6zZoVAudFAvH33CLU4lxh-MCAYAlZAW
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def fahrenheit_to_celsius(fahrenheit):
    # Apply the conversion formula
    celsius = (fahrenheit - 32) * 5.0 / 9.0
    return celsius

def get_date_from_YDOY(year, day_of_year):
    # Create a date object for January 1st of the given year
    jan_first = datetime(year, 1, 1)
    # Add the day_of_year - 1 to get the correct date
    date = jan_first + timedelta(days=day_of_year - 1)
    # Extract year, month, and day from the date
    return date.year, date.month, date.day

def fetch_AgWeatherNet_data(STATION_ID,START,END,bdaily=False):
    #15 min data:
    #AT_F (Degrees Fahrenheit) air temperature observed at 1.5 meters above the ground
    #DEWPT_F
    #RH_PCNT (%) relative humidity
    #P_INCHES (inch) sum of precipitation
    #WS_MPH (miles per hour)
    #LW_UNITIY (0-1) leaf wetness Unity (values between 0 and 1, 0.4 considered wet)
    #SR_WM2 (W/m2)

    #daily data
    #MIN_AT_F,AVG_AT_F,MAX_AT_F
    #MIN_REL_HUMIDITY,AVG_REL_HUMIDITY,MAX_REL_HUMIDITY
    #MIN_DEWPT_F,AVG_DEWPT_F,MAX_DEWPT_F
    #P_INCHES
    #WS_MPH,WS_MAX_MPH
    #WD_DEGREE
    #LW_UNITY
    #SR_MJM2
    #MIN_ST2_F,ST2_F,MAX_ST2_F
    #MIN_ST8_F,ST8_F,MAX_ST8_F
    #SM8_PCNT
    #SWP8_KPA
    #SWP2_KPA
    #MSLP_HPA
    #ETO
    #ETR

    base_url = "https://weather.wsu.edu/webservice/stationdata/?"
    #START and END should put into the url, not the params!
    if not bdaily:
        if len(START) == 10:
            START += '+00:00:00'
        if len(END) == 10:
            END += '+23:45:00'
        url = f"{base_url}&START={START}&END={END}"
    else:
        #daily
        if len(START) > 10:
            START = START[:10]
        if len(END) > 10:
            END = END[:10]
        url = f"{base_url}&START={START}&END={END}&BASIS=daily"
    #print(url)
    params = {
        "UNAME": "liumingwsu",
        "PASS": "AgweatherWSU",
        "STATION_ID": "100031"
    }
    response = requests.get(url,params=params)
    if response.status_code == 200:
      if response.json()['status'] == 1:
        data = response.json()['message'][0]['DATA']
        df = pd.DataFrame(data)
        column_to_exclude = ['TIMESTAMP_PST','JULDATE_PST']
        for col in df.columns:
            if col not in column_to_exclude:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        if 'JULDATE_PST' in df.columns:
            df = df.sort_values(by='JULDATE_PST')
        else:
            df = df.sort_values(by='TIMESTAMP_PST')
        return df
      else:
        return None
    else:
      return None

def aggregate_to_daily(data_15min):
  df = pd.DataFrame(data_15min)
  df['TIMESTAMP_PST'] = pd.to_datetime(df['TIMESTAMP_PST'])
  df = df[['TIMESTAMP_PST','AT_F','RH_PCNT','P_INCHES','WS_MPH','SR_WM2','DEWPT_F']]
  df.set_index('TIMESTAMP_PST', inplace=True)
  #df = df.apply(pd.to_numeric, errors='coerce')
  #daily_avg = df.resample('D').mean()
  daily_avg = df.resample('D').mean()
  daily_avg = daily_avg.rename(columns={'AT_F': 'AVG_AT_F', 'RH_PCNT': 'AVG_REL_HUMIDITY', 'DEWPT_F': 'AVG_DEWPT_F'})
  daily_max = df.resample('D').max()
  daily_max = daily_max.rename(columns={'RH_PCNT': 'MAX_REL_HUMIDITY', 'AT_F': 'MAX_AT_F', 'DEWPT_F': 'MAX_DEWPT_F', 'WS_MPH': 'WS_MAX_MPH'})
  daily_min = df.resample('D').min()
  daily_min = daily_min.rename(columns={'RH_PCNT': 'MIN_REL_HUMIDITY', 'AT_F': 'MIN_AT_F', 'DEWPT_F': 'MIN_DEWPT_F'})
  daily_sum = df.resample('D').sum()
  merged_df = pd.merge(daily_avg[['AVG_AT_F','AVG_REL_HUMIDITY','WS_MPH','SR_WM2','AVG_DEWPT_F']], daily_sum[['P_INCHES']], left_index=True, right_index=True)
  merged_df = pd.merge(merged_df,daily_min[['MIN_REL_HUMIDITY','MIN_AT_F','MIN_DEWPT_F']], left_index=True, right_index=True)
  merged_df = pd.merge(merged_df,daily_max[['MAX_REL_HUMIDITY','MAX_AT_F','MAX_DEWPT_F','WS_MAX_MPH']], left_index=True, right_index=True)
  merged_df = merged_df.reset_index()
  merged_df = merged_df.rename(columns={'index': 'TIMESTAMP_PST'})
  merged_df['SR_MJM2'] = merged_df['SR_WM2'] * 0.0864
  return merged_df

# Function to calculate the Haversine distance between two points
def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0 
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Distance in kilometers
    return R * c

def FindClosestStationAndDistance(target_lat,target_lon,stations_df,
                       lat_col_name,lon_col_name,id_col_name):
    stations_df['Distance'] = stations_df.apply(lambda row: haversine(
        target_lat, target_lon, row[lat_col_name], row[lon_col_name]), axis=1)
    # Find the ID of the closest location
    closest_location = stations_df.loc[stations_df['Distance'].idxmin()]
    return closest_location[id_col_name],closest_location["Distance"]

#Testing
"""
START = "2017-08-01"
END = "2017-08-02"
STATION_ID = "100031"
bdaily = False
data = fetch_AgWeatherNet_data(STATION_ID,START,END,bdaily)
pd.set_option('display.max_columns', None)
#print(data.columns)
print(data)

if not bdaily:
    daily = aggregate_to_daily(data)
else:
    daily = data
    daily = daily.rename(columns={'JULDATE_PST': 'TIMESTAMP_PST'})
    daily = daily.sort_values(by='TIMESTAMP_PST')
print(daily)
"""