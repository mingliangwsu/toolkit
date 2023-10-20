#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 09:05:09 2023

@author: liuming
"""
import pandas as pd
import sys 

debug_output = '/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/check_et_pet_ratio_for_pmoisture_fire.txt'
#debug_output = '/home/liuming/temp/test_head.txt'
delimiters = r'\s+|,|;|:|\(|\)|m+'
#aggregate and sort
#header_names = ['dum0','year', 'dum2', 'month','dum4','dum5','dum6','col','dum8','row','dum10','dum11','und_et_pet','dum13','dum14','ovr_et_pet']

#header_names = ['dum0','dum1','dum2','dum3','dum4','dum5','dum6','dum7','dum8','dum9','dum10','dum11','dum12','dum13','dum14','dum15','dum16','dum17','dum18','dum19','dum20','dum21','dum22','dum23','dum24','dum25','dum26','dum27','dum28']

header_names = ['dum0','year','dum2','dum3','month','dum5','dum6','dum7','col','dum9','row','dum11','dum12','und_et','dum14','dum15','und_pet','dum17','dum18','und_et_pet','dum19','dum20','ovr_et','dum23','dum24','ovr_pet','dum26','dum27','ovr_et_pet']


chunk_size = 1000000


data_reader = pd.read_csv(debug_output,sep=delimiters,header=None,names = header_names,engine='python',chunksize=chunk_size)
alldf = pd.DataFrame()

for chunk in data_reader:
    subdf = chunk[['year','month','col','row','und_et','und_pet','und_et_pet','ovr_et','ovr_pet','ovr_et_pet']]
    setsubdf = subdf[(subdf['year'] >= 1990) & (subdf['month'] >= 4) & (subdf['month'] <= 10)]
    #setsubdf = subdf
    if alldf.empty:
        alldf = setsubdf.copy()
    else:
        alldf = pd.concat([alldf,setsubdf],ignore_index=True)


import numpy as np
alldf['ovr_etratio'] = np.where(alldf['ovr_et_pet'] > 1.0, 1.0, alldf['ovr_et_pet'])

import matplotlib.pyplot as plt
# Plot histogram
bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

plt.hist(alldf['ovr_etratio'], bins=bins, edgecolor='black')

# Add labels and title
plt.xlabel('ET/PET')
plt.ylabel('Frequency')
plt.title('Histogram of overcanopy ET/PET of all patches Apr. - Oct. 1990-2015')

# Show the plot
plt.show()


