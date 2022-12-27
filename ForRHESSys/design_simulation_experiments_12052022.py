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
#0-1 to min~max
def f_to_range(d0_1,vmin,vmax):
    return vmin + d0_1 * (vmax - vmin)

path = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min"
outfile = path + "/simulation_list_brw.txt"


v0=[1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000] #fire_year
v1=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]            #fire_pspread
v2=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]            #fire_overstory_mortality_rate
v3=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]            #fire_understory_mortality_rate
v4=[0.01, 0.1, 0.25, 0.5, 1, 2, 5, 10, 25, 50, 100]                   #fire_pc_ku_mort
v5=[0.01, 0.1, 0.25, 0.5, 1, 2, 5, 10, 25, 50, 100]                   #fire_pc_kcons
v6=[-10]                                                    #fire_pc_ko_mort1 (using -10 for all) (K1)
v7=[1]                                                      #fire_pc_ko_mort2 0.2-1.5 (K2)

#baseline (no burn)
with open(outfile,"w") as fout:
    fout.write("0 2019 -9999 0.0 0.0 -9999 0.01 -10 1\n")

#series 1: define pspread (burn intensity), i.e. change byear + pspread + fire_pc_ku_mort + fire_pc_kcons + fire_pc_ko_mort2
sim1 = lhs(5, samples = 50, criterion='maximin')

#series 2: define mortality, i.e. change byear + fire_overstory_mortality_rate + fire_understory_mortality_rate + fire_pc_kcons
sim2 = lhs(6, samples = 60, criterion='maximin')

#series 3: define fire_understory_mortality_rate, i.e. change byear + fire_understory_mortality_rate + fire_pc_kcons + fire_pc_ko_mort1 + fire_pc_ko_mort2
sim3 = lhs(5, samples = 50, criterion='maximin')


idx = 1
with open(outfile,"a") as fout:
    for sample in sim1:
        outv = str(idx) + " " \
        + str(f_to_year(sample[0])) + " " \
        + str('%.2f' % sample[1]) \
        + " -9999" \
        + " -9999 " \
        + str('%.2f' % f_to_k(sample[2])) + " " \
        + str('%.2f' % f_to_k(sample[3])) \
        + " -10 " \
        + str('%.2f' % f_to_range(sample[4],0.2,2)) + "\n"
        fout.write(outv)
        idx += 1
    for sample in sim2:
        outv = str(idx) + " " \
        + str(f_to_year(sample[0])) \
        + " -9999 " \
        + str('%.2f' % sample[1]) + " " \
        + str('%.2f' % sample[2]) + " " \
        + str('%.2f' % f_to_k(sample[3])) + " " \
        + str('%.2f' % f_to_k(sample[4])) \
        + " -10 " \
        + str('%.2f' % f_to_range(sample[5],0.2,2)) + "\n"
        fout.write(outv)
        idx += 1
    for sample in sim3:
        outv = str(idx) + " " \
        + str(f_to_year(sample[0])) \
        + " -9999" \
        + " -9999 " \
        + str('%.2f' % sample[1]) + " " \
        + str('%.2f' % f_to_k(sample[2])) + " " \
        + str('%.2f' % f_to_k(sample[3])) \
        + " -10 " \
        + str('%.2f' % f_to_range(sample[4],0.2,2)) + "\n"
        fout.write(outv)
        idx += 1
        

#print(sim1)
#print(sim2)
#print(sim3)
