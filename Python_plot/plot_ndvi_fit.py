#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep. 30, 2020, LIU
Merge daily VIC simulation results
@author: liuming
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
import os
import math
from os import path
import lmoments3 as lm
from lmoments3 import distr
import statistics 
import seaborn as sns
#from simpledbf import Dbf5 
#import geopandas as gpd

#vicdir = sys.argv[1]
#outfile_path = sys.argv[2]
rootdir = "/home/liuming/mnt/hydronas1/Projects/USDA_Water_Ag/CropSyst_et_sourcecode/ndvi_data"
#crop = "corn"
crops = ["wheat","corn"]

#for cropindex in [1,2,3,4,5,6,7,8,9]:
for crop in crops:
  for cropindex in range(10):
  #for cropindex in [9]:
    mapfile = rootdir + "/fit_vs_obs_" + crop + str(cropindex) + ".txt.csv"
    if os.path.isfile(mapfile): 
      plotdata = pd.read_csv(mapfile, sep=',')
    
      #cfs
      plt.clf()
      plt.figure(figsize=(8,4))
      plt.plot(plotdata["DOY"],plotdata["Model"],"-o",color='blue',markersize=5);
      plt.plot(plotdata["DOY"],plotdata["Data"],"o",color='black');
      #plt.legend(loc='center')
      plt.title(crop + str(cropindex))
      outimage = rootdir + "/fig_" + crop + str(cropindex) + ".png"
    
      plt.savefig(outimage)
  print("Done\n")

plt.close('all')