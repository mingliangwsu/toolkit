#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar. 19, 2020, LIU
Update climate information and soil parameters from gNATSGO data sets.
@author: liuming
"""

original_soil_file = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/vic_soil/wa_soil_ext_neighbor.txt"
gNATSGO_csv_file = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/gNATSGO_gridded/vic_gnasgo.txt"
clm_csvv_file = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/prepostprocess/avg_anntavg_ppt_julytavg.txt"
#elev_file = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/arcinfo/elev.csv"
out_soil_parameter_file = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/vic_soil/wa_soil_ext_neighbor_gNATSGO.txt"

import pandas as pd
import sys 
import os
from os import path
#from simpledbf import Dbf5 
#import geopandas as gpd

def sortkey(x): 
    return int(x)

def lat_from_id(x): 
    lat = (x // 928) * 0.0625 + 25 + 0.0625 / 2.0
    return lat

def lon_from_id(x): 
    lon = ((x - 207873) % 928) * 0.0625 + (-125.0 + 0.0625 / 2.0)
    return lon

def id_from_lat_lon(xlon,ylat): 
    id = ((ylat - 25 - 0.0625 / 2.0) // 0.0625) * 928 + (xlon + 125 - 0.0625 / 2.0) / 0.0625 + 1
    return id

#soil parameter head index (original_soil_file) (text file has no head row)
vicsoil_column_index = {
        "mask" : 0,
        "gridcel" : 1,
        "lat" : 2,
        "lng" : 3,
        "b_infilt" : 4,
        "Ds" : 5,
        "Dsmax" : 6,
        "Ws" : 7,
        "c" : 8,
        "expt1" : 9,
        "expt2" : 10,
        "expt3" : 11,
        "Ksat1" : 12,
        "Ksat2" : 13,
        "Ksat3" : 14,
        "phi_s1" : 15,
        "phi_s2" : 16,
        "phi_s3" : 17,
        "init_moist1" : 18,
        "init_moist2" : 19,
        "init_moist3" : 20,
        "elevation" : 21,
        "depth1" : 22,
        "depth2" : 23,
        "depth3" : 24,
        "avg_temp" : 25,
        "dp" : 26,
        "bubble1" : 27,
        "bubble2" : 28,
        "bubble3" : 29,
        "quartz1" : 30,
        "quartz2" : 31,
        "quartz3" : 32,
        "bulk_density1" : 33,
        "bulk_density2" : 34,
        "bulk_density3" : 35,
        "soil_density1" : 36,
        "soil_density2" : 37,
        "soil_density3" : 38,
        "off_gmt" : 39,
        "Wcr_FRACT1" : 40,
        "Wcr_FRACT2" : 41,
        "Wcr_FRACT3" : 42,
        "Wpwp_FRACT1" : 43,
        "Wpwp_FRACT2" : 44,
        "Wpwp_FRACT3" : 45,
        "rough" : 46,
        "snow_rough" : 47,
        "annual_prec" : 48,
        "resid_moist1" : 49,
        "resid_moist2" : 50,
        "resid_moist3" : 51,
        "FS_ACTIVE" : 52,
        "avgJuly_Temp" : 53
        }
#index of gNATSGO file gNATSGO_csv_file (text file has head row)
gnatsgo_column_index = {
        "vicid" : 0,
        "vbd0_10" : 1,
        "vbd10_40" : 2,
        "vbd40_190" : 3,
        "vfc0_10" : 4,
        "vfc10_40" : 5,
        "vfc40_190" : 6,
        "vks0_10" : 7,
        "vks10_40" : 8,
        "vks40_190" : 9,
        "vsd0_10" : 10,
        "vsd10_40" : 11,
        "vsd40_190" : 12,
        "vwp0_10" : 13,
        "vwp10_40" : 14,
        "vwp40_190" : 15
        }

#index of climate information avg_anntavg_ppt_julytavg
clm_column_index = {
        "lat" : 0,
        "lng" : 1,
        "avg_temp" : 2,
        "annual_prec" : 3,
        "avgJuly_Temp" : 4
        }
#44.96875 -116.46875 5.32261 1077.95 20.0901


#inputdir = "/home/liuming/mnt/hydronas1/Projects/UW_subcontract/GIS/vic_soil"
#outputdir = "/home/liuming/temp/UW"


#dem = "wavicdem10t.csv"   
#VALUE,COUNT,WAVICALL,DEM_WA_T10

#neighbor = "wavicneig.csv"
#VALUE,COUNT,BIGVICPNWG,WANEIGB

#original_soil = "soil_param.0625.PNW.052108"
#original_soil = "wa_soil_original_with_head.csv"
#mask,gridcel,lat,lng,b_infilt,Ds,Dsmax,Ws,c,expt1,expt2,expt3,Ksat1,Ksat2,Ksat3,phi_s1,phi_s2,phi_s3,init_moist1,init_moist2,init_moist3,elevation,depth1,depth2,depth3,avg_temp,dp,bubble1,bubble2,bubble3,quartz1,quartz2,quartz3,bulk_density1,bulk_density2,bulk_density3,soil_density1,soil_density2,soil_density3,off_gmt,Wcr_FRACT1,Wcr_FRACT2,Wcr_FRACT3,Wpwp_FRACT1,Wpwp_FRACT2,Wpwp_FRACT3,rough,snow_rough,annual_prec,resid_moist1,resid_moist2,resid_moist3,FS_ACTIVE,avgJuly_Temp

#outsoil = "wa_soil_ext_neighbor.txt"

#reading original VIC (filled missing data with neighboring cells)
vic_dic = dict()
with open(original_soil_file) as f:
    for line in f:
        if "VALUE" not in line:
            a = line.rstrip().split()
            grid = a[vicsoil_column_index["gridcel"]]
            if grid not in vic_dic:
                vic_dic[grid] = a

#reading gNATSGO_csv_file
gnatsgo_dic = dict()
with open(gNATSGO_csv_file) as f:
    for line in f:
        if "vicid" not in line:
            a = line.rstrip().split(',')
            grid = a[gnatsgo_column_index["vicid"]]
            if grid not in gnatsgo_dic:
                gnatsgo_dic[grid] = a

#reading climate information
clm_dic = dict()
with open(clm_csvv_file) as f:
    for line in f:
        if "mask" not in line:
            a = line.rstrip().split()
            lat = float(a[clm_column_index["lat"]])
            lon = float(a[clm_column_index["lng"]])
            grid = str(int(id_from_lat_lon(lon,lat)))
            if grid not in clm_dic:
                clm_dic[grid] = a

#elev_dic = dict()
#with open(elev_file) as f:
#    for line in f:
#        if "vic" not in line:
#            a = line.rstrip().split(',')
#            grid = a[0]
#            if grid not in elev_dic:
#                elev_dic[grid] = a[1]
                
                
#vic_out_soil = dict()
#for grid in vic_neighbor:
#    neighbor = vic_neighbor[grid]
#    if grid == neighbor:
#        vic_out_soil[grid] = vic_soil[grid].copy()
#    else:
#        vic_out_soil[grid] = vic_soil[neighbor].copy()
#        vic_out_soil[grid][1] = grid
#        vic_out_soil[grid][2] = str('%.5f' % lat_from_id(int(grid)))
#        vic_out_soil[grid][3] = str('%.5f' % lon_from_id(int(grid)))
#        vic_out_soil[grid][21] = str('%.2f' % vic_dem[grid])
#printout
outfile = open(out_soil_parameter_file, "w")
for grid in sorted(vic_dic, key=sortkey, reverse=False):
    out = ""
    index = 0
    for col in vic_dic[grid]:
        outcol = vic_dic[grid][index]
        if index == vicsoil_column_index["Ksat1"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vks0_10"]]) * 0.001 * 24.0 * 3600.0 #um/s -> mm/day 
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["Ksat2"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vks10_40"]]) * 0.001 * 24.0 * 3600.0 #um/s -> mm/day 
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["Ksat3"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vks40_190"]]) * 0.001 * 24.0 * 3600.0 #um/s -> mm/day 
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["bulk_density1"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vbd0_10"]]) * 1000.0 #g/cm3 -> kg/m3 
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["bulk_density2"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vbd10_40"]]) * 1000.0 #g/cm3 -> kg/m3 
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["bulk_density3"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vbd40_190"]]) * 1000.0 #g/cm3 -> kg/m3 
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["Wcr_FRACT1"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vfc0_10"]]) * 0.01 * 0.7  #% -> fraction
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["Wcr_FRACT2"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vfc10_40"]]) * 0.01 * 0.7  #% -> fraction
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["Wcr_FRACT3"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vfc40_190"]]) * 0.01 * 0.7  #% -> fraction
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["Wpwp_FRACT1"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vwp0_10"]]) * 0.01 #% -> fraction  
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["Wpwp_FRACT2"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vwp10_40"]]) * 0.01 #% -> fraction  
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["Wpwp_FRACT3"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vwp40_190"]]) * 0.01 #% -> fraction  
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["quartz1"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vsd0_10"]]) * 0.01 #% -> fraction  
                outcol = str('%.5f' % outvalue)  
        elif index == vicsoil_column_index["quartz2"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vsd10_40"]]) * 0.01 #% -> fraction  
                outcol = str('%.5f' % outvalue) 
        elif index == vicsoil_column_index["quartz3"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vsd40_190"]]) * 0.01 #% -> fraction  
                outcol = str('%.5f' % outvalue) 
        elif index == vicsoil_column_index["init_moist1"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vfc0_10"]]) * 0.01 * float(vic_dic[grid][vicsoil_column_index["depth1"]]) #% -> fraction  
                outcol = str('%.5f' % outvalue)
        elif index == vicsoil_column_index["init_moist2"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vfc10_40"]]) * 0.01 * float(vic_dic[grid][vicsoil_column_index["depth2"]]) #% -> fraction  
                outcol = str('%.5f' % outvalue)         
        elif index == vicsoil_column_index["init_moist3"] :
            if grid in gnatsgo_dic:
                outvalue = float(gnatsgo_dic[grid][gnatsgo_column_index["vfc40_190"]]) * 0.01 * float(vic_dic[grid][vicsoil_column_index["depth3"]]) #% -> fraction  
                outcol = str('%.5f' % outvalue)         
        elif index == vicsoil_column_index["avg_temp"] :
            if grid in clm_dic:
                outvalue = float(clm_dic[grid][clm_column_index["avg_temp"]])   
                outcol = str('%.5f' % outvalue)        
        elif index == vicsoil_column_index["annual_prec"] :
            if grid in clm_dic:
                outvalue = float(clm_dic[grid][clm_column_index["annual_prec"]])   
                outcol = str('%.5f' % outvalue)    
        elif index == vicsoil_column_index["avgJuly_Temp"] :
            if grid in clm_dic:
                outvalue = float(clm_dic[grid][clm_column_index["avgJuly_Temp"]])   
                outcol = str('%.5f' % outvalue)
        #elif index == vicsoil_column_index["elevation"] :
        #    if grid in elev_dic:
        #        outcol = elev_dic[grid]
        out += outcol + " "
        index += 1
    out += "\n"
    outfile.write(out)


outfile.close()


#read fraction file and write to vegetation parameter file:
print("Done\n")