#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 09:21:20 2023
Generate fraction of gridMET gridcell in each US ecozone
@author: liuming
"""
import pandas as pd
#import sys 

in_combined_ecozone_gridmet_count = "/home/liuming/mnt/hydronas3/Projects/Rangeland/comb_ecozone_gridmet_range.csv"
#"ecozone,gridmet,count"
out_ecozone_gridmet_count_fraction = "/home/liuming/mnt/hydronas3/Projects/Rangeland/ecozone_gridmet_range_count_fraction.csv"

#aggregate and sort
df = pd.read_csv(in_combined_ecozone_gridmet_count,sep=',',header=0)
df_all = df.groupby(['ecozone','gridmet']).agg(count=('count','sum')).reset_index()
df_all = df_all.sort_values(by=['ecozone','gridmet'],ascending=[True,True],na_position='first')

#calculate fraction
df_ecozone = df.groupby(['ecozone']).agg(ecozone_all=('count','sum')).reset_index()

#join
joindf = pd.merge(df_all,df_ecozone,on=['ecozone'])
joindf['fraction'] = joindf['count'] / joindf['ecozone_all']

#export
joindf.to_csv(out_ecozone_gridmet_count_fraction,index=False)