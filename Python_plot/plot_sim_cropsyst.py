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

import matplotlib.pylab as pl
import itertools

#from simpledbf import Dbf5 
#import geopandas as gpd

#vicdir = sys.argv[1]
#outfile_path = sys.argv[2]
rootdir = "/home/liuming/mnt/hydronas1/Projects/USDA_Water_Ag/CropSyst_et_sourcecode/c_output"
#crop = "corn"
#models = ["WETPROFILE","WETTOP","WETCOS"]
models = ["WETPROFILE"]
params = np.arange(0.1, 1.1, 0.1) #["0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1.0"]
maxirrigs = np.arange(5, 51, 5)
colors = pl.cm.jet(np.linspace(0,1,len(maxirrigs) + 1))
alldata = pd.DataFrame()
#for cropindex in [1,2,3,4,5,6,7,8,9]:
for model in models:
  for param in params:
      for maxirrig in maxirrigs:
      #for cropindex in [9]:
        sparam = '{:1.1f}_max{:02d}'.format(param,maxirrig)    ##WETPROFILE_1.0_max20DailyOut.csv
        mapfile = rootdir + "/" + model + "_" + sparam + "SeasonOut.csv"
        if os.path.isfile(mapfile): 
          plotdata = pd.read_csv(mapfile, sep=',', header=None)
          plotdata = plotdata.T
          plotdata.columns = plotdata.iloc[0]
          plotdata = plotdata.iloc[1:]
          plotdata["mode"] = model
          plotdata["WF"] = param
          plotdata["maxirrig"] = maxirrig
          alldata = alldata.append(plotdata)

print("Done\n")

#Ploting
vars = ["ActET","ActTrans","ActSoilEvap","Irrig","IrrigNum","AvgWSI","AccBiomass"]

wetprofile = alldata[alldata["mode"] == "WETPROFILE"]
#wettop = alldata[alldata["mode"] == "WETTOP"]
#wetcos = alldata[alldata["mode"] == "WETCOS"]

wetdata = dict()
for maxirrig in maxirrigs:
    wetdata[maxirrig] = alldata[(alldata["mode"] == "WETPROFILE") & (alldata["maxirrig"] == maxirrig)]
marker = itertools.cycle((',', '+', '.', 'o', '*')) 
for var in vars:
      #cfs
     
      plt.clf()
      plt.figure(figsize=(8,4))
      #if "WETPROFILE" in models:
      #    plt.plot(wetprofile["WF"],wetprofile[var],"-o",color='blue',label='WETPROFILE',linewidth=4);
      #if "WETCOS" in models:
      #    plt.plot(wettop["WF"],wetcos[var],"-v",color='red', label="WETCOS",linewidth=3);
      #if "WETTOP" in models:
      #    plt.plot(wettop["WF"],wettop[var],"-*",color='orange', label="WETTOP",linewidth=2);
      for maxirrig in maxirrigs:
          strlab = str(maxirrig)
          index = int(maxirrig/5)
          #plt.plot(wetdata[maxirrig]["WF"],wetdata[maxirrig][var],"-*",color=colors[index], label=strlab,linewidth=0.5);
          plt.plot(wetdata[maxirrig]["WF"],wetdata[maxirrig][var],marker = next(marker), linestyle='-',color=colors[index], label=strlab,linewidth=1,markersize=4);
      
      plt.xlabel('Fraction of surface area wetted by irrigation system')
      #plt.legend(loc='center')
      plt.title(var)
      plt.legend(framealpha=1, frameon=True);
      outimage = rootdir + "/Season_" + var + ".png"
      plt.savefig(outimage)
alldata.to_csv("/home/liuming/mnt/hydronas1/Projects/USDA_Water_Ag/CropSyst_et_sourcecode/c_output/alloutput.csv",index=False)
plt.close('all')