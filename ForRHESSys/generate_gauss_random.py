#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 20:40:56 2022

@author: liuming
"""

#import numpy as np
#import pandas as pd
import sys 
import random

if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<mean> <stddev> <out_file>\n")
    sys.exit(0)
    
target = float(sys.argv[1]) 
stddev = float(sys.argv[2]) 
# = 0.5
outdist = sys.argv[3] 

dist = random.gauss(target, stddev)

with open(outdist, 'w') as fh:
    fh.write(str('%.6f' % dist) + '\n')