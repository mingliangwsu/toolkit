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
#from scipy.optimize import minimize
#from scipy.optimize import dual_annealing
from scipy.optimize import differential_evolution
import numpy as np
import matplotlib.pyplot as plt
from RHESSys_cal_nse_function import *
from pyDOE import *

def get_factor_value(f,data):
    return f * (data[1] - data[0]) + data[0]
    
# define a fitness function
def runRHESSys(item):
    #global idx
    #ts1, ts2, tpa, tgw1, tgw2, tsnowmelt_tcoef = 0, 0, 0, 0, 0, 0
    s1 = item[0]
    s2 = item[1]
    pa = item[2]
    gw1 = item[3]
    gw2 = item[4]
    snowmelt_tcoef = item[5]
    
    #output_pre = output_pre + "_idx_" + str(idx)
    #fname_basin_daily_out = local_pre + "_basin.daily"
    
    runRHESSys = RHESSys + " -netcdfgrid -ncgridinterp 10 -t " + tecfile + " -w " + worldfile \
    + " -whdr " + headfile + " -st " + str(sim_startyear) + " 01 01 01 -ed " + str(sim_endyear) + " 12 31 24 -pre " \
    + output_pre + " -s " + str(s1) + " " + str(s2) + " -sv " + str(s1) + " " + str(s2) \
    + " -svalt " + str(po) + " " + str(pa) + " -gw " + str(gw1) + " " + str(gw2) + " -snowmelt_tcoef " + str(snowmelt_tcoef) \
    + " -r " + flowtable + " -g -b " + " -firespread 100 " + patchgrid + " " + demgrid \
    + " -Ndecayrate 3.0 -firespin " + str(spyrs) + " " + str(spins) 
    
    print(runRHESSys)
    os.system(runRHESSys)
    return 0
             


#Run RHESSys related
cwd = os.getcwd()
RHESSys="/home/liuming/RHESSys_Ning/RHESSys/build/Qt/gcc/Release/RHESSys"
droot="/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979"
#RHESSys_outputdir="/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/Output_calibrations/hydrology"
RHESSys_outputdir="/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/scenarios/historical/gridmet/1979/Output_calibrations/20221129_152952"
if not os.path.exists(RHESSys_outputdir):
    command_line = "mkdir -p " + RHESSys_outputdir  
    os.system(command_line)
os.chdir(droot)


#flowtable = droot + "/cal-brw/" + "cal-brw.flow"
#worldfile = droot + "/cal-brw/" + "cal-brw.state.Y2016M1D1H1.state.Y2015M1D1H1.state.Y1985M1D1H1.state"

#flowtable = droot + "/hill336.flow"
#worldfile = droot + "/hill336.state"

flowtable = droot + "/brw.flow.09282022"
worldfile = droot + "/brw.state.Y2016M1D1H1.state.Y2015M1D1H1.state.Y1985M1D1H1.state"


tecfile = droot + "/" + "calibration.tec"
headfile =  droot + "/" + "br_with_fire.hdr"
#output_pre = RHESSys_outputdir + "/eval_brw"
output_pre = RHESSys_outputdir + "/init"
patchgrid = droot + "/" + "../../../../auxdata/patchgrid.txt"
demgrid = droot + "/" + "../../../../auxdata/demgrid.txt"
sim_startyear = 1980
sim_endyear = 2017
spyrs = 20
#soil_spins=50
#veg_spins=20 #25
spins = 10



#${RHESSys} -netcdfgrid -ncgridinterp 10 -t ${tecfile} -w ${worldfile} -whdr br_with_fire.hdr -start_from_zero_vegpools -st 1980 01 01 01 -ed ${endyear} 12 31 24 -pre ${output_pre} -s ${s1} ${s2} -sv ${s1} ${s2} -svalt ${po} ${pa} -gw ${gw1} ${gw2} -r ${flowtable} -g -b -p -c -firespread 100 ../../../../auxdata/patchgrid.txt ../../../../auxdata/demgrid.txt -Ndecayrate 3.0 -firespin ${spyrs} ${veg_spins} 

#calibration related
#calibration_method = "differential_evolution"   #"differential_evolution" "dual_annealing" "minimize"
outputdir = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/Output_calibrations_results"
#unit is mm/day??
fname_basin_daily_out = output_pre + "_basin.daily"
#unit is m,/day??
fname_obs = "/home/liuming/mnt/hydronas3/Projects/FireEarth/for_min/calibration/brw_obs_str.csv"
#fname_cal_evl_result = outputdir + "/" + "cal_evl_nse.txt"
if not os.path.exists(outputdir):
    command_line = "mkdir -p " + outputdir  
    os.system(command_line)
#evaluation_timesteps = ["yearly","monthly","daily"]  #yearly or daily or monthly    yearly: water year
evaluation_timesteps = ["monthly"] 
#evaluation_timestep = ["monthly"]

obsdata = pd.read_csv(fname_obs,delimiter=",",header=0)

#outf = open(fname_cal_evl_result,"w")
#outf.write("idx,s1,s2,po,pa,gw1,gw2,snowmelt_tcoef,period,nse_cal,nse_evl\n")
#outf.close()

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
#parameter from hill336 with unadjusted ppt
#s1 = 85.45
#s2 = 3.739 #0.2-10
#po = 0.622 #no change
#pa = 91.649  #0.1-5
#gw1 = 0.509  #0.1-0.8
#gw2 = 0.198 #0.01-0.8
#snowmelt_tcoefr = 0.00265


#parameter from John with adjusted ppt
s1 = 925.0
s2 = 0.677 #0.2-10
po = 0.622 #no change
pa = 1.43  #0.1-5
gw1 = 0.297  #0.1-0.8
gw2 = 0.096 #0.01-0.8
snowmelt_tcoefr = 0.0016

#s1r = [-2,3]
#s2r = [0.2,10]
#par = [-1,2]
#gw1r = [0.1,0.8]
#gw2r = [-3,3]
#snowmelt_tcoefr = [0.0016,0.006]

#idx = 0
#lhs = lhs(6,samples=1)

hydro_param = [s1,s2,pa,gw1,gw2,snowmelt_tcoefr]
#t = runRHESSys(hydro_param)
#calculate model performance

basin_daily_out = pd.read_csv(fname_basin_daily_out,delimiter=" ",header=0)
    #obsdata = pd.read_csv(fname_obs,delimiter=",",header=0)
    
    
keys = {"yearly" : ["wyear"],
        "monthly" : ["year","month"],
        "daily" : ["year","month","day"]}    
    
for evaluation_timestep in evaluation_timesteps:   
    print("evaluation_timestep:" + evaluation_timestep)
    cal_nse_value,dcalsim,dcalobs = calculate_nse_and_return_dftable(obsdata,basin_daily_out,evaluation_timestep,cal_start_year,cal_start_month,cal_end_year,cal_end_month)
    evl_nse_value,devlsim,devlobs = calculate_nse_and_return_dftable(obsdata,basin_daily_out,evaluation_timestep,evl_start_year,evl_start_month,evl_end_year,evl_end_month)
    print("NSE (" + str(cal_start_year) + "/" + str(cal_start_month) + "-" + str(cal_end_year) + "/" + str(cal_end_month) + "):" + str("%.3f" % cal_nse_value))
    print("NSE (" + str(evl_start_year) + "/" + str(evl_start_month) + "-" + str(evl_end_year) + "/" + str(evl_end_month) + "):" + str("%.3f" % evl_nse_value) + "\n")
    t = [dcalsim,devlsim]
    allsim = pd.concat(t)
    t = [dcalobs,devlobs]
    allobs = pd.concat(t)
    all = pd.merge(allsim,allobs, how="left", left_on=keys[evaluation_timestep],right_on=keys[evaluation_timestep])
    plt.plot(all["obs"])
    plt.plot(all["streamflow"])
    

#outf = open(fname_cal_evl_result,"w")
#outf.write(str(result))
#outf.close()

os.chdir(cwd)