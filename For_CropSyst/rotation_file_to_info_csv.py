#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 16:49:09 2022

@author: liuming
"""

import pandas as pd
import sys 
import os


scndir = "/home/liuming/mnt/hydronas2/Projects/SmartFarm/temp/Grower standard 1/Scenarios"


scns = ["Alternate_1","Alternate_2","Alternate_3","Alternate_4","Alternate_4_Organic","Current","Grower standard_1"]

for scn in scns:
    #scn = "Current"
    rfile = scndir + "/" + scn + "/" + "specific.rot" 

    outdir = "/home/liuming/mnt/hydronas2/Projects/SmartFarm/CropSyst_setups"
    outfile = outdir + "/" + scn + "_rot_crop.txt"


    with open(outfile,"w") as fout:
        fout.write("Year,DOY,Crop\n");
        with open(rfile,"r") as rotfile:
            for wline in rotfile:
                line = wline.rstrip()
                if "event_date" in line:
                    year = line[11:15]
                    #print(year)
                    doy = line[15:18]
                    #print(year + " " + doy)
                if ".crp" in line:
                    #print(line)
                    t1 = line.rfind('.')
                    t2 = line.rfind('/') + 1
                    #print("t1:" + str(t1) + " t2:" + str(t2) + "\n")
                    crop = line[t2:t1]
                    #print(crop)
                if "management" in line:
                    if crop != "Fallow":
                        print(year + "," + doy + "," + crop + "\n")
                        fout.write(year + "," + doy + "," + crop + "\n");
                