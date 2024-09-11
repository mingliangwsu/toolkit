#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 08:35:01 2024

@author: liuming
"""
import pandas as pd
import numpy as np

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
def FindClosestStation(target_lat,target_lon,stations_df,
                       lat_col_name,lon_col_name,id_col_name):
    stations_df['Distance'] = stations_df.apply(lambda row: haversine(
        target_lat, target_lon, row[lat_col_name], row[lon_col_name]), axis=1)
    # Find the ID of the closest location
    closest_location = stations_df.loc[stations_df['Distance'].idxmin()]
    return closest_location[id_col_name],closest_location["Distance"]


defaultPath = "./irrigationtables"
agweathernetstationfile = f'{defaultPath}/AgWeatherNet   Washington State UniversityWSU Cougar HeadWSU Cougar Head.csv'

agweathernetstation = pd.read_csv(agweathernetstationfile,sep=',', header=0)
#agweathernetstation = agweathernetstation.set_index('Station ID')

# Target coordinates
target_lat = 47.0  # Latitude of target point
target_lon = -119.6  # Longitude of target point
df = agweathernetstation
df['Longitude'] = -df['Longitude(W)']
# Calculate distances between the target and each location in the dataframe
closest_location,dist = FindClosestStation(target_lat,target_lon,df,"Latitude(N)",
                                      "Longitude","Station ID")


# Print the closest location's ID
print(f"Closest location ID: {closest_location} dist:{dist} km")
