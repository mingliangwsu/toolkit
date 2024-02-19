#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 09:21:20 2023
Generate fraction of gridMET gridcell in each US county
@author: liuming
"""
import pandas as pd
import csv

in_county_csv = "/home/liuming/mnt/hydronas3/Projects/Rangeland/countyp020.csv"
#"county,gridmet,count"
out_county_unique_id = "/home/liuming/mnt/hydronas3/Projects/Rangeland/county_id_name_fips.csv"

#aggregate and sort
df = pd.read_csv(in_county_csv,sep=',',dtype = 'str',header=0,converters = {'FIPS_ID': int})
df_rename = df.rename({'COUNTY': 'county_name', 'FIPS_ID': 'county'}, axis='columns')
dfout = df_rename[['county','county_name','FIPS','STATE']]

dfout = dfout.drop_duplicates()

#export
dfout.to_csv(out_county_unique_id,index=False,quoting=csv.QUOTE_NONNUMERIC)