#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 09:21:20 2023
Generate fraction of gridMET gridcell in each US ecozone
@author: liuming
"""
import pandas as pd
import datetime
from datetime import timedelta
from pathlib import Path
import struct
from pathlib import Path
#import sys 

#VIC binary
VIC_scale = {'PREC' : 40,
             'TMAX' : 100,
             'TMIN' : 100,
             'WIND' : 100,
             'QAIR' : 10000,
             'SHORTWAVE' : 40,
             'RMAX' : 100,
             'RMIN' : 100}
vic_columns = ['date']
for col in VIC_scale:
    vic_columns.append(col)
 
# 90th Percentile
def q90(x):
    return x.quantile(0.9)    

#https://skeptric.com/pandas-aggregate-quantile/
class Quantile:
    def __init__(self, q):
        self.q = q
        
    def __call__(self, x):
        return x.quantile(self.q)
        # Or using numpy
        # return np.quantile(x.dropna(), self.q)
        
#read VIC binary to dataframe
def read_VIC_binary(bin_filename):
    #data = data = Path(bin_filename).read_bytes()
    start_date = datetime.datetime(1979, 1, 1)
    end_date = datetime.datetime(2022, 12, 31)
    struct_fmt = '=1H7h' # unsigned int[1], signed int[7]
    struct_len = struct.calcsize(struct_fmt)
    #print('struct_len:' + str(struct_len))
    struct_unpack = struct.Struct(struct_fmt).unpack_from

    results = pd.DataFrame(columns=vic_columns)
    today = start_date
    with open(bin_filename,'rb') as f:
        while True:
            data = f.read(struct_len)
            if len(data) < struct_len: 
                break
            s = struct_unpack(data)
            temp = dict()
            index = 0
            for dcol in VIC_scale:
                temp[dcol] = s[index] / VIC_scale[dcol]
                index += 1
            temp['date'] = today
            new_row = pd.DataFrame(temp, index=[0])
            results = pd.concat([new_row,results.loc[:]]).reset_index(drop=True)
            #move to next day
            today += datetime.timedelta(days=1)
    #print('results:')
    #print(results)
    results['year'] = pd.DatetimeIndex(results['date']).year
    results['month'] = pd.DatetimeIndex(results['date']).month
    results['day'] = pd.DatetimeIndex(results['date']).day
    results = results.drop(['date','WIND','QAIR','SHORTWAVE'], axis=1)
    return results

#generate climate indices for rangeland
def climate_indices(climate):
    climate['TAVG'] = (climate['TMAX'] + climate['TMIN']) * 0.5
    climate['RAVG'] = (climate['RMAX'] + climate['RMIN']) * 0.5 * 0.01
    climate['THI'] = 0.8 * climate['TAVG'] + climate['RAVG'] * (climate['TAVG'] - 14.4) + 46.4
    climate['Normal'] = climate['THI'].apply(lambda x: 1 if x < 75 else 0)
    climate['Alert'] = climate['THI'].apply(lambda x: 1 if (x >= 75 and x < 79) else 0)
    climate['Danger'] = climate['THI'].apply(lambda x: 1 if (x >= 79 and x < 84) else 0)
    climate['Emergency'] = climate['THI'].apply(lambda x: 1 if x >= 84 else 0)
    results = climate.groupby(['year','month']).agg(RMIN_MIN=('RMIN','min'),
                                          RMIN_AVG=('RMIN','mean'),
                                          TMIN_MIN=('TMIN','min'),
                                          TMIN_AVG=('TMIN','mean'),
                                          Normal=('Normal','sum'),
                                          Alert=('Alert','sum'),
                                          Danger=('Danger','sum'),
                                          Emergency=('Emergency','sum'),
                                          RAVG_AVG=('RAVG','mean'),
                                          TMAX_MAX=('TMAX','max'),
                                          TMAX_AVG=('TMAX','mean'),
                                          RMAX_MAX=('RMAX','max'),
                                          RMAX_AVG=('RMAX','mean'),
                                          TAVG_AVG=('TAVG','mean'),
                                          THI_AVG=('THI','mean'),
                                          PPT=('PREC','sum'),
                                          THI_STD=('THI','std'),
                                          THI_90=('THI',Quantile(0.9))).reset_index()
    return results

#process data

in_gridid_lat_lon = "/home/liuming/mnt/hydronas3/Projects/Rangeland/gridmet_file_list.csv"
#GRID_ID,lat,lon
in_county_gridmet_count_fraction = "/home/liuming/mnt/hydronas3/Projects/Rangeland/county_gridmet_range_count_fraction.csv"
#county,gridmet,count,county_all,fraction

in_gridmet_path = "/home/liuming/mnt/hydronas3/Projects/Rangeland/gridmet_temp/"

out_climate_indicex = "/home/liuming/mnt/hydronas3/Projects/Rangeland/county_gridmet_mean_indices.csv"

#read gridmet filename
gridmet_info = dict()
with open(in_gridid_lat_lon,'r') as f:
    for line in f:
        a = line.rstrip().split(',')
        if 'GRID_ID' not in a:
            #print('grid:' + a[0] + '\tlat:' + a[1] + '\tlon:' + a[2])
            gridmet_info[a[0]] = [a[1],a[2]]
            
#read and generate indexes
#gridmet_data = dict()
gridmet_indexes = dict()
county_indices = dict()
county_total_fraction = dict()
with open(in_county_gridmet_count_fraction,'r') as f:
    for line in f:
        a = line.rstrip().split(',')
        if 'gridmet' not in a:
            county = a[0]
            gridmet = a[1]
            #process all gridmet grid cells
            if gridmet not in gridmet_indexes:
                #read and process this gridmet indices
                if gridmet in gridmet_info:
                    filename = in_gridmet_path + 'data_' + gridmet_info[gridmet][0] + '_' + gridmet_info[gridmet][1]
                    if Path(filename).is_file():
                        print('filename:' + filename)
                        vic_metdata = read_VIC_binary(filename)
                        #gridmet_data[a[1]] = vic_metdata
                        gridmet_indexes[gridmet] = climate_indices(vic_metdata)
                        print('read done!')
            #added into county table
            #for checking total fraction equal one
            fraction = float(a[4])
            if county not in county_total_fraction:
                county_total_fraction[county] = fraction
            else:
                county_total_fraction[county] += fraction
                
            #add gridmet fractional indices into county table
            if county not in county_indices and gridmet in gridmet_indexes:
                county_indices[county] = gridmet_indexes[gridmet]
                for col in county_indices[county].columns:
                    if col not in ['year','month']:
                        county_indices[county][col] = fraction * county_indices[county][col]
            else:
                #add new gridmet indices with weighted by fraction
                if gridmet in gridmet_indexes:
                    for col in county_indices[county].columns:
                        if col not in ['year','month']:
                            county_indices[county][col] = fraction * gridmet_indexes[gridmet][col]
                            
                            
print('Done processing data!')
#merge all conties into one data frame
all_county_indices = pd.DataFrame()
for county in county_indices:
    if county in county_total_fraction:
        if county_total_fraction[county] < 0.9999:
            print("Warning: county:" + county + " total fraction is not 1!")
    county_indices[county]['county'] = county
    if all_county_indices.empty:
        all_county_indices = county_indices[county]
    else:
        all_county_indices = all_county_indices.append(county_indices[county],county_indices[county])
#export
all_county_indices.to_csv(out_climate_indicex,index=False)
print('Done!')