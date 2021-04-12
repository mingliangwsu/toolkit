# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from scipy.interpolate import make_interp_spline, BSpline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
import os
import math
from os import path
import statistics 

#x: list
def expand_monthlydata(x):
    #m: 1-12
    ext = x.copy()
    ext.insert(0,x[11])
    ext.insert(0,x[10])
    ext.append(x[0])
    ext.append(x[1])
    return ext

#month = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
monthext = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
#data = [5, 10, 15, 20, 30, 20, 10, 2, 1, 2, 4, 5]
data = [5, 10, 5, 50, 30, 20, 10, 2, 1, 30, 4, 30]

datav = np.asarray(data)
monthv = np.asarray(month)
monthextv = np.asarray(monthext)

minv = datav * 0.8
maxv = datav * 1.2
minvl = minv.tolist()
maxvl = maxv.tolist()
plt.clf()

dataext = expand_monthlydata(data)
dataextv = np.asarray(dataext)

minext = expand_monthlydata(minvl)
minextv = np.asarray(minext)
maxext = expand_monthlydata(maxvl)
maxextv = np.asarray(maxext)

#smoothing
xnew = np.linspace(monthextv.min(), monthextv.max(), 300)  #20 per month
spl = make_interp_spline(monthextv, dataextv, k=5)  # type: BSpline
data_smooth = spl(xnew)
plt.figure(0)
plt.ylim(-10,80)
plt.plot(xnew[40:260], data_smooth[40:260])
plt.show()

minspl = make_interp_spline(monthextv, minextv, k=5)  # type: BSpline
min_smooth = minspl(xnew)
maxspl = make_interp_spline(monthextv, maxextv, k=5)  # type: BSpline
max_smooth = maxspl(xnew)

plt.fill_between(xnew[40:260],min_smooth[40:260], max_smooth[40:260], 
#plt.fill_between(xnew[0:299],min_smooth[0:299], max_smooth[0:299], 
                 facecolor="orange", # The fill color
                 color='blue',       # The outline color
                 alpha=0.2)          # Transparency of the fill
outimage = "/home/liuming/temp/" + "cline.png"
plt.savefig(outimage)

plt.figure(1)
plt.ylim(-10,80)
plt.plot(monthv, datav)
plt.fill_between(monthv,minv, maxv, 
                 facecolor="orange", # The fill color
                 color='blue',       # The outline color
                 alpha=0.2)          # Transparency of the fill
outimage = "/home/liuming/temp/" + "raw.png"
plt.savefig(outimage)