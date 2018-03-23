#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 13:37:50 2017

Read VIC-CropSyst crop daily outputs.

@author: liuming
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

outdir = "/home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Scenarios/Liu_Linux_262790_204/VIC_output"
vic_crop_outputs = "vic_crop_daily.csv"
os.chdir(outdir)

vic_crop = pd.read_csv(vic_crop_outputs,sep=',')

#Print the targetted variable for calibration
max_yield = max(vic_crop['Yield_kg_m2'])
max_LAI = max(vic_crop['LAI'])
total_irrig_total_mm =  sum(vic_crop['irrig_total_mm'])
outline = "\nmax_LAI:" + str(max_LAI) + \
          "\tmax_yield:" + str(max_yield) + \
          "\ttotal_irrigation:" + str(total_irrig_total_mm) + \
          "\n" 
print(outline)

#Display the daily output
#fig, ax = plt.subplots(1, 1, figsize=(12,5))
#ax.plot(vic_crop['Year'],vic_crop['LAI'])
#ax.plot(vic_crop['Year'],vic_crop['Yield_kg_m2'])
x_axis = vic_crop['Year']
lai = vic_crop['LAI']
yld = vic_crop['Yield_kg_m2']
irrig = vic_crop['irrig_total_mm']
plt.figure(figsize=(6,8))
plt.grid(True)

x = range(len(x_axis))

ax1 = plt.subplot(311)
plt.title('LAI')
plt.ylabel('m2/m2')
#plt.xticks(np.arange(min(x_axis), max(x_axis)+1, 1.0))
plt.plot(x, lai,'r-')
#ax1.scatter(range(len(lai)),lai,color='r')
#ax1.set_xlim(0,len(lai)-1)
#ax1.set_xticks(range(len(lai)))
#ax1.set_xticklabels(x_axis)

ax2 = plt.subplot(312)
plt.title('Yield')
plt.ylabel('kg/m2')
plt.plot(x, yld,'g-')

ax3 = plt.subplot(313)
plt.title('Irrigation')
plt.ylabel('mm')
plt.plot(x, irrig,'b-')
plt.show()

plt.close()
