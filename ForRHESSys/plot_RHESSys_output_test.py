#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 15:30:38 2022

@author: liuming
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys 
import os
from os.path import exists
import math
import scipy.stats


from mpl_toolkits import mplot3d

#datafile_dir = "/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar/Outputs"
#pre = "spinup_fire__"

datafile_dir = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/liudebug_output"
#datafile_dir = "/home/liuming/mnt/hydronas1/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/outputs_fromzero_vegc_20X200"
outfig_app = "high_mort_nostartvegpool"
pre = "liutest_output_fire_1990_"

#filename = pre + "basin.daily"
#Index(['day', 'month', 'year', 'basinID', 'pot_surface_infil', 'snow_thr',
#       'sat_def_z', 'sat_def', 'rz_storage', 'unsat_stor', 'rz_drainage',
#       'unsat_drain', 'cap', 'evap', 'snowpack', 'trans', 'baseflow', 'return',
#       'streamflow', 'psn', 'nppcum', 'lai', 'gw.Qout', 'gw.storage',
#       'detention_store', '%sat_area', 'litter_store', 'canopy_store',
#       '%snow_cover', 'snow_subl', 'trans_var', 'acc_trans', 'acctransv_var',
#       'pet', 'dC13', 'precip', 'pcp_assim', 'mortf', 'tmax', 'tmin', 'tavg',
#       'vpd', 'snowfall', 'recharge', 'gpsn', 'resp', 'gs', 'rootdepth',
#       'plantc', 'snowmelt', 'canopysubl', 'routedstreamflow', 'canopy_snow',
#       'height', 'evap_can', 'evap_lit', 'evap_soil', 'litrc', 'Kdown',
#       'Ldown', 'Kup', 'Lup', 'Kstar_can', 'Kstar_soil', 'Kstar_snow',
#       'Lstar_can', 'Lstar_soil', 'Lstar_snow', 'LE_canopy', 'LE_soil',
#       'LE_snow', 'Lstar_strat', 'canopydrip', 'ga', 'litr_decomp',
#       'decom_landclim_daily'],
#      dtype='object')

#filename = pre + "grow_basin.daily"
#Index(['day', 'month', 'year', 'basinID', 'lai', 'lai_b', 'pai', 'pai_b',
#       'gpsn', 'plant_resp', 'leaf_resp', 'soil_resp', 'nitrate', 'sminn',
#       'surfaceN', 'plantc', 'plantn', 'cpool', 'npool', 'litrc', 'litrn',
#       'soilc', 'soiln', 'soiln_noslow', 'gwNO3', 'gwNH4', 'gwDON', 'gwDOC',
#       'streamflow_NO3', 'streamflow_NH4', 'streamflow_DON', 'streamflow_DOC',
#       'gwNO3out', 'gwNH4out', 'gwDONout', 'gwDOCout', 'denitrif', 'nitrif',
#       'DOC', 'DON', 'root_depth', 'nfix', 'nuptake', 'grazingC',
#       'StreamNO3_from_surface', 'StreamNO3_from_sub', 'N_dep',
#       'fertilizer_store', 'understory_leafc', 'understory_stemc',
#       'understory_biomassc', 'understory_height', 'overstory_leafc',
#       'overstory_stemc', 'overstory_biomassc', 'overstory_height', 'burn',
#       'litterc_burned', 'cwdc_to_atoms', 'overstory_biomassc_consumed',
#       'overstory_leafc_consumed', 'overstory_stemc_consumed',
#       'overstory_biomassc_mortality', 'overstory_leafc_mortality',
#       'overstory_stemc_mortality', 'understory_biomassc_consumed',
#       'understory_leafc_consumed', 'understory_stemc_consumed', 'total_snagc',
#       'total_snagn', 'total_redneedlec', 'total_redneedlen',
#       'deadrootc_beetle', 'deadrootn_beetle', 'understory_gpsn',
#       'understory_resp', 'understory_rootdepth', 'understory_npp',
#       'ratio_abg_litter', 'litr1_hr', 'litr2_hr', 'litr3_hr', 'litr4_hr'],
#      dtype='object')

#filename = pre + "stratum.daily"
#Index(['day', 'month', 'year', 'basinID', 'hillID', 'zoneID', 'patchID',
#       'stratumID', 'lai', 'proj_lai_when_red', 'evap', 'APAR_direct',
#       'APAR_diffuse', 'sublim', 'trans', 'ga', 'gsurf', 'gs', 'psi',
#       'leaf_day_mr', 'psn_to_cpool', 'rain_stored', 'snow_stored',
#       'rootzone.S', 'm_APAR', 'm_tavg', 'm_LWP', 'm_CO2', 'm_tmin', 'm_vpd',
#       'dC13', 'Kstar_dir', 'Kstar_dif', 'Lstar', 'surf_heat', 'height',
#       'covfrac', 'vegID', 'wstress_days', 'potential_psn_to_cpool'],

#filename = pre + "grow_stratum.daily"
#Index(['day', 'month', 'year', 'basinID', 'hillID', 'zoneID', 'patchID',
#       'stratumID', 'proj_lai', 'proj_lai_when_red', 'proj_pai',
#       'proj_pai_when_red', 'toal_snag_c', 'toal_snag_n', 'total_redneedle_c',
#       'total_redneedle_n', 'deadrootc_beetle', 'deadrootn_beetle', 'leafc',
#       'leafn', 'cpool', 'npool', 'dead_leafc', 'frootc', 'frootn',
#       'live_stemc', 'live_stemn', 'leafc_store', 'leafn_store', 'dead_stemc',
#       'dead_stemn', 'live_crootc', 'live_crootn', 'dead_crootc',
#       'dead_crootn', 'cwdc', 'mresp', 'gresp', 'psn_to_cpool', 'age',
#       'root_depth', 'gwseasonday', 'lfseasonday', 'gsi', 'nlimit', 'fleaf',
#       'froot', 'fwood', 'Nuptake', 'smin2pl', 'retrans2pl', 'mort_fract',
#       'assim_sunlit', 'assim_shade', 'trans_sunlit', 'trans_shade',
#       'leafc_age1', 'leafc_age2', 'proj_lai_sunlit', 'proj_lai_shade'],
#      dtype='object')

filename = pre + "grow_patch.daily"
#Index(['day', 'month', 'year', 'basinID', 'hillID', 'zoneID', 'patchID', 'lai',
#       'plantc', 'tot_leafc', 'tot_frootc', 'tot_woodc', 'plantn', 'net_psn',
#       'plant_resp', 'soil_resp', 'litr1c', 'litr2c', 'litr3c', 'litr4c',
#       'litr1n', 'litr2n', 'litr3n', 'litr4n', 'lit.rain_cap', 'soil1c',
#       'soil2c', 'soil3c', 'soil4c', 'soil1n', 'soil2n', 'soil3n', 'soil4n',
#       'soilDON', 'soilDOC', 'denitrif', 'netleach', 'DON_loss', 'DOC_loss',
#       'soilNO3', 'soilNH4', 'streamNO3', 'streamNH4', 'streamDON',
#      'streamDOC', 'surfaceNO3', 'surfaceNH4', 'surfaceDOC', 'surfaceDON',
#       'height', 'nuptake', 'root_depth', 'nfix', 'grazingC', 'area'],
#      dtype='object')


filename = pre + "grow_stratum.yearly"
#Index(['year', 'basinID', 'hillID', 'zoneID', 'patchID', 'stratumID',
#       'proj_lai', 'leafc', 'leafn', 'frootc', 'frootn', 'stemc', 'stemn',
#       'cwdc', 'cwdn', 'psn_net', 'mr', 'gr', 'minNSC', 'mortfract', 'snagc',
#       'snagn', 'redneedlec', 'redneedlen', 'dead_rootc_beetle',
#       'dead_rootn_beetle', 'height', 'rootdepth_mm'],
#      dtype='object')

#filename = pre + "basin.yearly"
#Index(['year', 'basinID', 'streamflow', 'streamflow_NO3', 'denitrif', 'DOC',
#       'DON', 'et', 'psn', 'lai', 'nitrif', 'mineralized', 'uptake',
#       'num_thresh', 'pet'],
#      dtype='object')

pf = pd.read_csv(datafile_dir+"/"+filename,delimiter=" ",header=0)



strata = 79708
spf = pf
if 'stratumID' in pf:
    spf = pf[pf["stratumID"] == strata]
#spf = spf[(spf.index.values >= 100) & (spf.index.values <= 200)]
#spf = spf[(spf.index.values >= 390000) & (spf.index.values <= 400000)]
#spf = spf[(spf.index.values >= 150000) & (spf.index.values <= 152500)]
#spf = spf[(spf.index.values >= 795000) & (spf.index.values <= 800000)]
#spf = spf[(spf.year == 1982) | (spf.year == 1987)]
#spf.to_csv(datafile_dir + "/subsetnew1982_87.csv")

no_plot = ['day', 'month', 'year', 'basinID', 'hillID', 'zoneID', 'patchID',
           'stratumID', 'vegID']


#ax.plot(pf["year"], pf["lai"])
for col in pf.columns:
    if col not in no_plot:
        fig, ax = plt.subplots(figsize=(20,8))
        ax.plot(spf.index.values,spf[col])
        ax.title.set_text(col)
        if "outputs_fromzero_vegc_20X200" in datafile_dir:
            fig.savefig(datafile_dir + "/" + filename + "_" + col + "_outputs_fromzero_vegc_20X200" + ".png")
        else:
            fig.savefig(datafile_dir + "/" + outfig_app + "_" + filename + "_" + col + ".png")
        
    
    
    #ax.title(col)

#ax.plot(spf["psn"])
