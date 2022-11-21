#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:05:13 2022

@author: liuming
"""
import os
import pandas as pd
import hydrostats.metrics as hm
#from pyeasyga import pyeasyga
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
from RHESSys_cal_nse_function import *
from pyDOE import *

def get_factor_value(f,data):
    return f * (data[1] - data[0]) + data[0]
    
# define a fitness function
def objective(item):
    global idx
    #ts1, ts2, tpa, tgw1, tgw2, tsnowmelt_tcoef = 0, 0, 0, 0, 0, 0
    s1 = pow(10,get_factor_value(item[0],s1r))
    s2 = get_factor_value(item[1],s2r)
    pa = pow(10,get_factor_value(item[2],par))
    gw1 = get_factor_value(item[3],gw1r)
    gw2 = pow(10,get_factor_value(item[4],gw2r))
    snowmelt_tcoef = get_factor_value(item[5],snowmelt_tcoefr)
    runRHESSys = RHESSys + " -netcdfgrid -ncgridinterp 10 -t " + tecfile + " -w " + worldfile \
    + " -whdr " + headfile + " -st " + str(sim_startyear) + " 01 01 01 -ed " + str(sim_endyear) + " 12 31 24 -pre " \
    + output_pre + " -s " + str(s1) + " " + str(s2) + " -sv " + str(s1) + " " + str(s2) \
    + " -svalt " + str(po) + " " + str(pa) + " -gw " + str(gw1) + " " + str(gw2) + " -snowmelt_tcoef " + str(snowmelt_tcoef) \
    + " -r " + flowtable + " -g -b " + " -firespread 100 " + patchgrid + " " + demgrid \
    + " -Ndecayrate 3.0 -firespin " + str(spyrs) + " " + str(spins) 

    #print(runRHESSys)
    os.system(runRHESSys)

    #calculate model performance

    basin_daily_out = pd.read_csv(fname_basin_daily_out,delimiter=" ",header=0)
    obsdata = pd.read_csv(fname_obs,delimiter=",",header=0)
    
    evaluation_timestep = "monthly"
    
    cal_nse_value = calculate_nse(obsdata,basin_daily_out,evaluation_timestep,cal_start_year,cal_start_month,cal_end_year,cal_end_month)
    
    #reference only
    evl_nse_value = calculate_nse(obsdata,basin_daily_out,evaluation_timestep,evl_start_year,evl_start_month,evl_end_year,evl_end_month)
    
    out = str(idx) + "," + str(s1) + "," + str(s2) + "," + str(po) + "," + str(pa) + "," + str(gw1) + "," + str(gw2) + "," + str(snowmelt_tcoef) + "," + evaluation_timestep \
    + "," + str(cal_nse_value) + "," + str(evl_nse_value) + "\n"

    outf.write(out)
    idx += 1
    return -cal_nse_value
             


#Run RHESSys related
cwd = os.getcwd()
RHESSys="/home/liuming/RHESSys_Ning/RHESSys/build/Qt/gcc/Release/RHESSys"
droot="/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979"
RHESSys_outputdir="/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/Output_calibrations"
if not os.path.exists(RHESSys_outputdir):
    command_line = "mkdir -p " + RHESSys_outputdir  
    os.system(command_line)
os.chdir(droot)


flowtable = droot + "/" + "patch_29586.flow"
worldfile = droot + "/" + "patch_29586.state"
tecfile = droot + "/" + "calibration.tec"
headfile =  droot + "/" + "br_with_fire.hdr"
output_pre = RHESSys_outputdir + "/calib"
patchgrid = droot + "/" + "../../../../auxdata/patchgrid.txt"
demgrid = droot + "/" + "../../../../auxdata/demgrid.txt"
sim_startyear = 1980
sim_endyear = 2017
spyrs = 20
#soil_spins=50
#veg_spins=20 #25
spins = 1

#${RHESSys} -netcdfgrid -ncgridinterp 10 -t ${tecfile} -w ${worldfile} -whdr br_with_fire.hdr -start_from_zero_vegpools -st 1980 01 01 01 -ed ${endyear} 12 31 24 -pre ${output_pre} -s ${s1} ${s2} -sv ${s1} ${s2} -svalt ${po} ${pa} -gw ${gw1} ${gw2} -r ${flowtable} -g -b -p -c -firespread 100 ../../../../auxdata/patchgrid.txt ../../../../auxdata/demgrid.txt -Ndecayrate 3.0 -firespin ${spyrs} ${veg_spins} 

#calibration related
outputdir = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/Output_calibrations_results"
#unit is mm/day??
fname_basin_daily_out = output_pre + "_basin.daily"
#unit is m,/day??
fname_obs = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/calibration/brw_obs_str.csv"
fname_cal_evl_result = outputdir + "/" + "cal_evl_nse.txt"
if not os.path.exists(outputdir):
    command_line = "mkdir -p " + outputdir  
    os.system(command_line)
evaluation_timesteps = ["yearly","monthly","daily"]  #yearly or daily or monthly    yearly: water year
outf = open(fname_cal_evl_result,"w")
outf.write("idx,s1,s2,po,pa,gw1,gw2,snowmelt_tcoef,period,nse_cal,nse_evl\n")

#target_period = ["cal","evl"]

cal_start_year = 1985
cal_start_month = 10
cal_end_year = 2006
cal_end_month = 9
evl_start_year = cal_end_year
evl_start_month = 10
evl_end_year = 2017  #2017
evl_end_month = 9


#run RHESSys



s1 = 1000.0
s2 = 5.241 #0.2-10
po = 0.622 #no change
pa = 0.50  #0.1-5
gw1 = 0.2  #0.1-0.8
gw2 = 0.049 #0.01-0.8

s1r = [-2,3]
s2r = [0.2,10]
par = [-1,1]
gw1r = [0.1,0.8]
gw2r = [-2,2]
snowmelt_tcoefr = [0.0016,0.006]

idx = 0
lhs = lhs(6,samples=1)
x0 = lhs[0]
opt = {"maxiter" : 200}
result = minimize(objective,x0, method="nelder-mead", tol=1e-3, bounds=((0,1),(0,1),(0,1),(0,1),(0,1),(0,1)),options=opt)
print(result)

os.chdir(cwd)