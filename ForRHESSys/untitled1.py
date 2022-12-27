#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 22:43:33 2022

@author: liuming
"""
import sys
if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1inout_text_file> <2out_expand_file>\n")
    sys.exit(0)
    
with open(sys.argv[1]) as f,open(sys.argv[2],'w') as fout:  
    for line in f:
        a = line.rstrip().split()
        if len(a) > 0:
            for i in range(int(a[0])):
                fout.write("1")
                index = 0
                for j in a:
                    index += 1
                    if index > 2:
                       fout.write("," + j)
                fout.write("/n")