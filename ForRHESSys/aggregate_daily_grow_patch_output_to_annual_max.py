#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 01:45:46 2018

@author: liuming
"""

import numpy as np
import pandas as pd
import datetime
import sys 
import os
import math
from os import path
import statistics 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import cm
import subprocess

def to_date_column(year,mon,day):
    return datetime.date(int(year),int(mon),int(day))

def count_lines_in_file(file_path):
    result = subprocess.run(['wc', '-l', file_path], capture_output=True, text=True)
    return int(result.stdout.split()[0])

#indir = "/home/liuming/mnt/hydronas3/Projects/WWS_Oregon/GateCreek_RHESSys_output/patch_daily_pre_post_fire/daymet_2021/"

indir = "/home/liuming/mnt/hydronas1/Users/Mingliang/temp/daymet_2001/"
prefix = "real_run_daymet_"
output = "grow_patch.daily"
outdir = "/home/liuming/mnt/hydronas3/Projects/WWS_Oregon/GateCreek_RHESSys_output/agg_sts_outputs/"
annual_outfile = f'{outdir}agg_annual_max_patch_from_{output}_2001.txt'

#growth patch daily 
#day month year basinID hillID zoneID patchID lai plantc tot_leafc tot_frootc tot_woodc plantn net_psn plant_resp soil_resp litr1c litr2c litr3c litr4c litr1n litr2n litr3n litr4n lit.rain_cap soil1c soil2c soil3c soil4c soil1n soil2n soil3n soil4n soilDON soilDOC denitrif netleach DON_loss DOC_loss soilNO3 soilNH4 streamNO3 streamNH4 streamDON streamDOC surfaceNO3 surfaceNH4 surfaceDOC surfaceDON height nuptake root_depth nfix grazingC area

#patch daily
#day month year basinID hillID zoneID patchID rain_thr detention_store sat_def_z sat_def rz_storage potential_rz_store rz_field_capacity rz_wilting_point unsat_stor rz_drainage unsat_drain sublimation return evap evap_surface soil_evap snow snow_melt trans_sat trans_unsat Qin Qout psn root_zone.S root.depth litter.rain_stor litter.S area tpet pet pe lai baseflow streamflow pcp recharge Kdowndirpch Kdowndiffpch Kupdirpch Kupdifpch Luppch Kdowndirsubcan Kdowndifsubcan Ldownsubcan Kstarcan Kstardirsno Kstardiffsno Lstarcanopy Lstarsnow Lstarsoil wind windsnow windzone ga gasnow trans_reduc_perc pch_field_cap overland_flow height ustar snow_albedo Kstarsoil Kdowndirsurf Kdowndifsurf exfil_unsat snow_Rnet snow_QLE snow_QH snow_Qrain snow_Qmelt LEcanopy SED snow_age psi t_scalar w_scalar rate_scalar litr_decomp rate_landclim_year rate_landclim_daily et_decom_mean Tsoil


modelout_file = f'{indir}{prefix}{output}'


outsub_vars = ['patchID','year','literc','litern','soilc','soiln','soil_DIN','totc','totorgn','lai']
outsub_data = pd.DataFrame()

#lines = count_lines_in_file(modelout_file)
chunksize = 5 * 10 ** 6
#total_chunks = int(lines / chunksize)
#print(f'total_chunks:{total_chunks}')

#all_subs = dict()
index = 0
for outdata in pd.read_csv(modelout_file, sep=' ', chunksize=chunksize):
    outdata['literc'] = outdata['litr1c'] + outdata['litr2c'] + outdata['litr3c'] + outdata['litr4c']
    outdata['litern'] = outdata['litr1n'] + outdata['litr2n'] + outdata['litr3n'] + outdata['litr4n']
    outdata['soilc'] = outdata['soil1c'] + outdata['soil2c'] + outdata['soil3c'] + outdata['soil4c']
    outdata['soiln'] = outdata['soil1n'] + outdata['soil2n'] + outdata['soil3n'] + outdata['soil4n']
    outdata['soil_DIN'] = outdata['soilNO3'] + outdata['soilNH4']
    outdata['totc'] = outdata['plantc'] + outdata['literc'] + outdata['soilc']
    outdata['totorgn'] = outdata['plantn'] + outdata['litern'] + outdata['soiln']
    t = outdata[outsub_vars]
    tt = t.groupby(['year','patchID'],as_index=False).max()
    if len(outsub_data.columns) == 0:
        outsub_data = tt
    else:
        outsub_data = pd.concat([outsub_data,tt], ignore_index = True)
    #print(f'done {index*100/total_chunks} %')
    print(f'done {index}')
    index += 1
    del outdata
    #if index == 3:
    #    break

        
outdata_annual = outsub_data.groupby(['year','patchID'],as_index=False).max()
#outdata_annual['date'] = outdata_annual.apply(lambda x: to_date_column(x.year,x.month,x.day), axis=1)
outdata_annual.to_csv(annual_outfile, index=False)

print("Done!")