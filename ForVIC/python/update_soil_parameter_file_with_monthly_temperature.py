#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: liuming

update soil parameter file with new monthly temperature information
"""

import pandas as pd
import sys 
import os

if len(sys.argv) != 4:
    print("Usage:" + sys.argv[0] + "<original_soil_parameter_file> <temperature_input> <out_new_soil_parameter_file>\n")
    sys.exit(0)

orig_soil_parameter_file = sys.argv[1]
tempature = sys.argv[2]
new_orig_soil_parameter_file = sys.argv[3]

soil_file_head = ["mask", "gridcel", "lat", "lng", "b_infilt", "Ds", "Dsmax", "Ws", 
                  "c", "expt1", "expt2", "expt3", "expt4", "expt5", "expt6", "expt7", 
                  "expt8", "expt9", "expt10", "expt11", "expt12", "expt13", "expt14", 
                  "expt15", "expt16", "expt17", "Ksat1", "Ksat2", "Ksat3", "Ksat4", 
                  "Ksat5", "Ksat6", "Ksat7", "Ksat8", "Ksat9", "Ksat10", "Ksat11", 
                  "Ksat12", "Ksat13", "Ksat14", "Ksat15", "Ksat16", "Ksat17", "phi_s1", 
                  "phi_s2", "phi_s3", "phi_s4", "phi_s5", "phi_s6", "phi_s7", "phi_s8", 
                  "phi_s9", "phi_s10", "phi_s11", "phi_s12", "phi_s13", "phi_s14", 
                  "phi_s15", "phi_s16", "phi_s17", "init_moist1", "init_moist2", 
                  "init_moist3", "init_moist4", "init_moist5", "init_moist6", "init_moist7", 
                  "init_moist8", "init_moist9", "init_moist10", "init_moist11", 
                  "init_moist12", "init_moist13", "init_moist14", "init_moist15", 
                  "init_moist16", "init_moist17", "elevation", "depth1", "depth2", 
                  "depth3", "depth4", "depth5", "depth6", "depth7", "depth8", "depth9", 
                  "depth10", "depth11", "depth12", "depth13", "depth14", "depth15", 
                  "depth16", "depth17", "avg_temp", "dp", "bubble1", "bubble2", 
                  "bubble3", "bubble4", "bubble5", "bubble6", "bubble7", "bubble8", 
                  "bubble9", "bubble10", "bubble11", "bubble12", "bubble13", "bubble14", 
                  "bubble15", "bubble16", "bubble17", "quartz1", "quartz2", "quartz3", 
                  "quartz4", "quartz5", "quartz6", "quartz7", "quartz8", "quartz9", 
                  "quartz10", "quartz11", "quartz12", "quartz13", "quartz14", 
                  "quartz15", "quartz16", "quartz17", "bulk_dens_min1", "bulk_dens_min2", 
                  "bulk_dens_min3", "bulk_dens_min4", "bulk_dens_min5", "bulk_dens_min6", 
                  "bulk_dens_min7", "bulk_dens_min8", "bulk_dens_min9", "bulk_dens_min10", 
                  "bulk_dens_min11", "bulk_dens_min12", "bulk_dens_min13", "bulk_dens_min14", 
                  "bulk_dens_min15", "bulk_dens_min16", "bulk_dens_min17", "soil_dens_min1", 
                  "soil_dens_min2", "soil_dens_min3", "soil_dens_min4", "soil_dens_min5", 
                  "soil_dens_min6", "soil_dens_min7", "soil_dens_min8", "soil_dens_min9", 
                  "soil_dens_min10", "soil_dens_min11", "soil_dens_min12", "soil_dens_min13", 
                  "soil_dens_min14", "soil_dens_min15", "soil_dens_min16", "soil_dens_min17", 
                  "organic_1", "organic_2", "organic_3", "organic_4", "organic_5", 
                  "organic_6", "organic_7", "organic_8", "organic_9", "organic_10", 
                  "organic_11", "organic_12", "organic_13", "organic_14", "organic_15", 
                  "organic_16", "organic_17", "bulk_dens_org_1", "bulk_dens_org_2", 
                  "bulk_dens_org_3", "bulk_dens_org_4", "bulk_dens_org_5", "bulk_dens_org_6", 
                  "bulk_dens_org_7", "bulk_dens_org_8", "bulk_dens_org_9", "bulk_dens_org_10", 
                  "bulk_dens_org_11", "bulk_dens_org_12", "bulk_dens_org_13", 
                  "bulk_dens_org_14", "bulk_dens_org_15", "bulk_dens_org_16", 
                  "bulk_dens_org_17", "soil_dens_org_1", "soil_dens_org_2", "soil_dens_org_3", 
                  "soil_dens_org_4", "soil_dens_org_5", "soil_dens_org_6", "soil_dens_org_7", 
                  "soil_dens_org_8", "soil_dens_org_9", "soil_dens_org_10", "soil_dens_org_11", 
                  "soil_dens_org_12", "soil_dens_org_13", "soil_dens_org_14", 
                  "soil_dens_org_15", "soil_dens_org_16", "soil_dens_org_17", "off_gmt", 
                  "Wcr_FRACT1", "Wcr_FRACT2", "Wcr_FRACT3", "Wcr_FRACT4", "Wcr_FRACT5", 
                  "Wcr_FRACT6", "Wcr_FRACT7", "Wcr_FRACT8", "Wcr_FRACT9", "Wcr_FRACT10", 
                  "Wcr_FRACT11", "Wcr_FRACT12", "Wcr_FRACT13", "Wcr_FRACT14", 
                  "Wcr_FRACT15", "Wcr_FRACT16", "Wcr_FRACT17", "Wpwp_FRACT1", 
                  "Wpwp_FRACT2", "Wpwp_FRACT3", "Wpwp_FRACT4", "Wpwp_FRACT5", 
                  "Wpwp_FRACT6", "Wpwp_FRACT7", "Wpwp_FRACT8", "Wpwp_FRACT9", 
                  "Wpwp_FRACT10", "Wpwp_FRACT11", "Wpwp_FRACT12", "Wpwp_FRACT13", 
                  "Wpwp_FRACT14", "Wpwp_FRACT15", "Wpwp_FRACT16", "Wpwp_FRACT17", 
                  "rough", "snow_rough", "annual_prec", "resid_moist1", "resid_moist2", 
                  "resid_moist3", "resid_moist4", "resid_moist5", "resid_moist6", 
                  "resid_moist7", "resid_moist8", "resid_moist9", "resid_moist10", 
                  "resid_moist11", "resid_moist12", "resid_moist13", "resid_moist14", 
                  "resid_moist15", "resid_moist16", "resid_moist17", "FS_ACTIVE", 
                  "avgJuly_Temp", "Clay1", "Clay2", "Clay3", "Clay4", "Clay5", "Clay6", 
                  "Clay7", "Clay8", "Clay9", "Clay10", "Clay11", "Clay12", "Clay13", 
                  "Clay14", "Clay15", "Clay16", "Clay17"]

temp_dic = dict()

#read temperature
with open(tempature) as f:
    for line in f:
        a = line.split()
        if "mon" in a:
            temp_list = a
        else:
            if len(a) > 0:
                index = 0
                for col in temp_list:
                    if col == "mon":
                        mon = a[index]
                    elif col == "lat":
                        lat = a[index]
                    elif col == "lon":
                        lon = a[index]
                    elif col == "TMAX":
                        tmax = float(a[index])
                    elif col == "TMIN":
                        tmin = float(a[index])
                    index += 1
                if mon == "6":
                    tavg = (tmax + tmin) * 0.5
                    lat_lon = lat + lon
                    temp_dic[lat_lon] = tavg
print("reading temperature done!")

outfile_soil = open(new_orig_soil_parameter_file,"w")

with open(orig_soil_parameter_file) as f:
    for line in f:
        a = line.split()
        if len(a) > 0:
            index = 0
            outvalue = a
            outstring = ""
            for col in soil_file_head:
                if col == "lat":
                    lat = a[index]
                elif col == "lng":
                    lon = a[index]
                elif col == "avgJuly_Temp":
                    lat_lon = lat + lon
                    if lat_lon in temp_dic:
                        outvalue[index] = str('%.4f' % temp_dic[lat_lon])
                outstring += outvalue[index] + " "
                index += 1
            outfile_soil.write(outstring + "\n")
outfile_soil.close()
print("Done!")