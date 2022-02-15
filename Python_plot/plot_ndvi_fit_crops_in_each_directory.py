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
trootdir = "/home/liuming/mnt/hydronas1/Projects/USDA_Water_Ag/METRIC/CBP_EEFlux_04012021"
#crop = "corn"
#crops = ["Corn", "Potato", "Wheat"]
crops = ["CornNew", "Potato", "Wheat"]
#crops = ["Potato"]

#for cropindex in [1,2,3,4,5,6,7,8,9]:
for crop in crops:
    rootdir = trootdir + "/" + crop
    for file in os.listdir(rootdir):
        #print(file)
        if file[0:11] == "fit_vs_obs_" or file[0:8] == "HarmFit_":
            print(file)
            mapfile = rootdir + "/" + file
            plotdata = pd.read_csv(mapfile, sep=',')
            if file[0:8] == "HarmFit_":
                tcolor = 'orange'
            else:
                tcolor = 'blue'
            
            #cfs
            plt.clf()
            plt.figure(figsize=(8,4))
            plt.plot(plotdata["DOY"],plotdata["Model"],"-o",color=tcolor,markersize=5,label="Fitted Curve");
            plt.plot(plotdata["DOY"],plotdata["Data"],"o",color='black',label="Data");
            #plt.legend(loc='center')
            stitle = crop + " " + file[0:-4]
            plt.legend(framealpha=1, frameon=True);
            plt.title(stitle)
            outimage = rootdir + "/fig_" + file[0:-4] + ".png"
    
            plt.savefig(outimage)
print("Done\n")

plt.close('all')