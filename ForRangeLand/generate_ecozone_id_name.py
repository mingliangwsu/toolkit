#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 09:21:20 2023
Generate fraction of gridMET gridcell in each US ecozone
@author: liuming
"""
import pandas as pd
import csv

in_ecozone_csv = "/home/liuming/mnt/hydronas3/Projects/Rangeland/us_eco_l3_stat.csv"
#"ecozone,gridmet,count"
out_ecozone_unique_id = "/home/liuming/mnt/hydronas3/Projects/Rangeland/ecozone_id_name.csv"

#aggregate and sort
df = pd.read_csv(in_ecozone_csv,sep=',',dtype = 'str',header=0,converters = {'US_L3_ID': int})
df_rename = df.rename({'US_L3NAME': 'ecozone_name', 'US_L3_ID': 'ecozone'}, axis='columns')
dfout = df_rename[['ecozone','ecozone_name']]

dfout = dfout.drop_duplicates()

#export
dfout.to_csv(out_ecozone_unique_id,index=False,quoting=csv.QUOTE_NONNUMERIC)