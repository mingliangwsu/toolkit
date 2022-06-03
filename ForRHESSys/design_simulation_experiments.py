#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 15:41:38 2022

@author: liuming
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
import os
from os.path import exists
import math
#from scipy.interpolate import make_interp_spline, BSpline
#from scipy.ndimage.filters import gaussian_filter1d
from pyDOE import *

#0-1 to 0.01 - 100
def f_to_k(d0_1):
    return math.pow(10,(d0_1 - 0.5) * 4)
def f_to_year(d0_1):
    return int(1990 + round(d0_1 * (2000 - 1990)))

path = "/home/liuming/mnt/hydronas2/Projects/FireEarth/BullRun"
outfile = path + "/simulation_list_update_after80.txt"


v0=[1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000] #fire_year
v1=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]            #fire_pspread
v2=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]            #fire_overstory_mortality_rate
v3=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]            #fire_understory_mortality_rate
v4=[0.01, 0.1, 0.25, 0.5, 1, 2, 5, 10, 25, 50, 100]                   #fire_pc_ku_mort
v5=[0.01, 0.1, 0.25, 0.5, 1, 2, 5, 10, 25, 50, 100]                   #fire_pc_kcons
v6=[-10]                                                    #fire_pc_ko_mort1
v7=[1]                                                      #fire_pc_ko_mort2

#baseline (no burn)
with open(outfile,"w") as fout:
    fout.write("2019 -9999 0.0 0.0 -9999 0.01 -10 1\n")

#series 1: define pspread (burn intensity), i.e. change byear + pspread + fire_pc_ku_mort + fire_pc_kcons  
sim1 = lhs(4, samples = 40, criterion='maximin')

#series 2: define mortality, i.e. change byear + fire_overstory_mortality_rate + fire_understory_mortality_rate + fire_pc_kcons  
sim2 = lhs(4, samples = 40, criterion='maximin')

#series 3: define fire_understory_mortality_rate, i.e. change byear + fire_understory_mortality_rate + fire_pc_kcons  
sim3 = lhs(3, samples = 40, criterion='maximin')


idx = 0
with open(outfile,"w") as fout:
    for sample in sim1:
        outv = str(idx) + " " \
        + str(f_to_year(sample[0])) + " " \
        + str('%.2f' % sample[1]) \
        + " -9999" \
        + " -9999 " \
        + str('%.2f' % f_to_k(sample[2])) + " " \
        + str('%.2f' % f_to_k(sample[3])) \
        + " -10 1\n"
        fout.write(outv)
        idx += 1
    for sample in sim2:
        outv = str(idx) + " " \
        + str(f_to_year(sample[0])) \
        + " -9999 " \
        + str('%.2f' % sample[1]) + " " \
        + str('%.2f' % sample[2]) \
        + " -9999 " \
        + str('%.2f' % f_to_k(sample[3])) \
        + " -10 1\n"
        fout.write(outv)
        idx += 1
    for sample in sim3:
        outv = str(idx) + " " \
        + str(f_to_year(sample[0])) \
        + " -9999" \
        + " -9999 " \
        + str('%.2f' % sample[1]) \
        + " -9999 " \
        + str('%.2f' % f_to_k(sample[2])) \
        + " -10 1\n"
        fout.write(outv)
        idx += 1
        

#print(sim1)
#print(sim2)
#print(sim3)
