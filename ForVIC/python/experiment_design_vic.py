#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 16:51:51 2020

@author: liuming
"""

from datetime import date
import pandas as pd
import numpy as np
#import os
#import os.path
import math
import array
from pyDOE import *

#range of 4 parameters need to be calibrated 
#bi = np.array([0.001,0.4])
#DsMAX = np.array([0.01,30]) 
#Ds = np.array([0.0001,1.0])
#Ws = np.array([0.01,1.0])

outfilename = "/home/liuming/temp/UW/parameter_list.txt"

fnumsample = 20
factors = 4

actor_ranges = np.array([[0.001,0.4],[0.01,30],[0.0001,1.0],[0.01,1.0]])
factor_name = np.array(["bi","DsMAX","Ds","Ws"])

experiments = lhs(4, samples=numsample, criterion='center')

outfile = open(outfilename, "w")

out = ""
for factor in range(factors):
    out += factor_name[factor] + ":"
    for expidx in range(fnumsample):
        #print("experiment:" + str(experiment) + "\n")
        maxv = actor_ranges[factor][1]
        minv = actor_ranges[factor][0]
        parameter = minv + experiments[expidx][factor] * (maxv - minv)
        out += " \"" + str('%.4f' % parameter) + "\"" 
    out += "\n"
print(out)
outfile.write(out)
outfile.close()
print("Done!")