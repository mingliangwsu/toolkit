# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import pysal as ps
import numpy as np

def sortkey(x): 
    return int(x)

'''
Arguments
---------
dbfile  : DBF file - Input to be imported
upper   : Condition - If true, make column heads upper case
'''
def dbf2DF(dbfile, upper=True): #Reads in DBF files and returns Pandas DF
    db = ps.open(dbfile) #Pysal to open DBF
    d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
    #pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
    pandasDF = pd.DataFrame(d) #Convert to Pandas DF
    if upper == True: #Make columns uppercase if wanted 
        pandasDF.columns = map(str.upper, db.header) 
    db.close() 
    return pandasDF


datapath = "/home/liuming/mnt/hydronas1/Projects/WallaWalla"
vicfraction = "vicw.dbf"
vicveg = "pnw_veg_parameter.txt"
vicirrig = "pnw_irrigation.txt"
output_file = "total_irrigation_km2.txt"

total_irrig_area = dict() #[crop]
cell_irrig = dict()  #[grid][crop]
cell_area_km2 = dict() #[grid]
cell_vic_irrig_area_km2 = dict() #[grid][crop]

#read grid total area
df = dbf2DF(datapath + "/" + vicfraction)

for index,row in df.iterrows():
    gridid = int(row["GRID_CODE"])
    if gridid not in cell_area_km2:
        cell_area_km2[gridid] = 0.0
    cell_area_km2[gridid] += row["SHAPE_AREA"] / 1000000.0

#read irrigation file
with open(datapath + "/" + vicirrig) as f:
    for line in f:
        a = line.rstrip().split()
        if len(a) >= 2:
            if a[1].isdigit():
                gridid = int(a[0])
            else:
                crop = int(a[0])
                if gridid not in cell_irrig:
                    cell_irrig[gridid] = dict()
                if crop not in cell_irrig[gridid]:
                    cell_irrig[gridid][crop] = True
#read veg parameter
with open(datapath + "/" + vicveg) as f:
    for line in f:
        a = line.rstrip().split()
        if len(a) == 2:
            gridid = int(a[0])
        elif len(a) == 8:
            crop = int(a[0])
            fraction = float(a[1])
            if gridid in cell_area_km2 and gridid in cell_irrig:
                if crop in cell_irrig[gridid]:
                    if gridid not in cell_vic_irrig_area_km2:
                        cell_vic_irrig_area_km2[gridid] = dict()
                    if crop not in cell_vic_irrig_area_km2[gridid]:
                        cell_vic_irrig_area_km2[gridid][crop] = 0.0
                    cell_vic_irrig_area_km2[gridid][crop] += fraction * cell_area_km2[gridid] 

for gridid in cell_vic_irrig_area_km2:
    for crop in cell_vic_irrig_area_km2[gridid]:
        if crop not in total_irrig_area:
            total_irrig_area[crop] = 0.0
        total_irrig_area[crop] += cell_vic_irrig_area_km2[gridid][crop]

with open(datapath + "/" + output_file,"w") as f:
    f.write("crop,area_km2\n")
    for crop in sorted(total_irrig_area):
        f.write(str(crop) + "," + str(total_irrig_area[crop]) + "\n")
        
print("Done!")
