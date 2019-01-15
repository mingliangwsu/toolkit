#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sum VIC-CropSyst crop daily outputs to annuam mean.

@author: liuming
"""
from datetime import date
import pandas as pd
import os
import os.path

nrnidaily_file = "/mnt/hydronas/Projects/BPA_CRB/GIS/NRNI/NRNI_daily_liu.csv"
out_data_dir = "/home/liuming/temp/NRNI_monthly_flow"
if not os.path.exists(out_data_dir):
    os.mkdir(out_data_dir)

month_days = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31}
station_info = out_data_dir + "/station_start_end_month.txt"
station_info_out = open(station_info,'w')


daily = pd.read_csv(nrnidaily_file,sep=',',index_col=False,header=0)
daily["year"] = -9999
daily["mon"] = -9999
daily["monthday"] = -9999
for index, row in daily.iterrows():
    temp = date(*map(int, row["date"].split('-')))
    #print(temp.month)
    daily.set_value(index,'year',temp.year)
    daily.set_value(index,'mon',temp.month)
    daily.set_value(index,'monthday',temp.day)

stations = list()
for column in daily:
    if column not in ['days','date','year','mon','monthday']:
        print(column)
        stations.append(column)

teststations = ['ALB5N','AUB5N']
for station in stations:
    temp = daily[['year','mon','monthday',station]]
    tempsel = temp[temp[station] != -9999]
    avg_month = tempsel.groupby(['year','mon'],as_index=False)[station].mean()
    avg_c = tempsel.groupby(['year','mon'],as_index=False)[station].count()
    #avg_c.rename(columns={0 : 'year', 1 : 'monmon', 2 : 'counts'},inplace=True)
    t_c = avg_c[station]
    t = pd.concat([avg_month,t_c],axis=1)
    p = t
    p.columns = ['year','mon',station,'count']
    start = 0
    outfile = open(out_data_dir + '/' + station + ".obs.month",'w')
    for i, row in p.iterrows():
        if (row['count'] >= month_days[int(row['mon'])]):
            if (start == 0):
                start_year = int(row['year'])
                start_mon = int(row['mon'])
            outline = str(int(row['year'])) + " " + str(int(row['mon'])) + " " + str("%0.2f" % (row[station],))
            end_year = int(row['year'])
            end_mon = int(row['mon'])
            #str(row[station])
            outfile.write(outline + "\n")
            start += 1
    outfile.close()
    outline_station = station + " " + str(start_year) + " " + str(start_mon) + " " + str(end_year) + " " + str(end_mon) + "\n"
    station_info_out.write(outline_station)

    
#daily["date_f"] = date(*map(int, daily["date"].split('-')))
station_info_out.close()
print("Done!")