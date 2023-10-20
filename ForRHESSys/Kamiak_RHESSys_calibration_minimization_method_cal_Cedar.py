#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:05:13 2022

@author: liuming
"""
import os,sys
sys.path.append(os.getcwd()) 
import os
import pandas as pd
#import hydrostats.metrics as hm
#from pyeasyga import pyeasyga
#from scipy.optimize import minimize
#from scipy.optimize import dual_annealing
from scipy.optimize import differential_evolution
import numpy as np
import matplotlib.pyplot as plt
from RHESSys_cal_nse_function import *
from pyDOE import *
#sys.path.append(os.getcwd()) 
def get_factor_value(f,data):
    return f * (data[1] - data[0]) + data[0]
    
# define a fitness function
def objective(item):
    global idx
    global evaluation_timestep
    #ts1, ts2, tpa, tgw1, tgw2, tsnowmelt_tcoef = 0, 0, 0, 0, 0, 0
    s1 = pow(10,get_factor_value(item[0],s1r))
    s2 = get_factor_value(item[1],s2r)
    pa = pow(10,get_factor_value(item[2],par))
    gw1 = get_factor_value(item[3],gw1r)
    gw2 = get_factor_value(item[4],gw2r) #07102023LML  gw2 = pow(10,get_factor_value(item[4],gw2r))
    snowmelt_tcoef = get_factor_value(item[5],snowmelt_tcoefr)
    
    local_pre = output_pre + "_idx_" + str(idx)
    local_fname_basin_daily_out = local_pre + "_basin.daily"
    
    runRHESSys = RHESSys + " -netcdfgrid -ncgridinterp 10 -t " + tecfile + " -w " + worldfile \
    + " -whdr " + headfile + " -st " + str(sim_startyear) + " 01 01 01 -ed " + str(sim_endyear) + " 12 31 24 -pre " \
    + local_pre + " -s " + str(s1) + " " + str(s2) + " -sv " + str(s1) + " " + str(s2) \
    + " -svalt " + str(po) + " " + str(pa) + " -gw " + str(gw1) + " " + str(gw2) + " -snowmelt_tcoef " + str(snowmelt_tcoef) \
    + " -r " + flowtable + " -g -b " + " -firespread 100 " + patchgrid + " " + demgrid \
    + " -Ndecayrate 3.0 -firespin " + str(spyrs) + " " + str(spins) 
    
    """
    runRHESSys = RHESSys + " -netcdfgrid -ncgridinterp 10 -t " + tecfile + " -w " + worldfile \
    + " -whdr " + headfile + " -st " + str(sim_startyear) + " 01 01 01 -ed " + str(sim_endyear) + " 12 31 24 -pre " \
    + local_pre + " -s " + str(s1) + " " + str(s2) + " -sv " + str(s1) + " " + str(s2) \
    + " -svalt " + str(po) + " " + str(pa) + " -gw " + str(gw1) + " " + str(gw2) + " -snowmelt_tcoef " + str(snowmelt_tcoef) \
    + " -g -b " + " -firespread 100 " + patchgrid + " " + demgrid \
    + " -Ndecayrate 3.0 -firespin " + str(spyrs) + " " + str(spins) 
    """

    print(runRHESSys)
    os.system(runRHESSys)

    #calculate model performance

    basin_daily_out = pd.read_csv(local_fname_basin_daily_out,delimiter=" ",header=0)
    #obsdata = pd.read_csv(fname_obs,delimiter=",",header=0)
    
   
    cal_nse_value = calculate_nse(obsdata,basin_daily_out,evaluation_timestep,cal_start_year,cal_start_month,cal_end_year,cal_end_month)
    
    #reference only
    evl_nse_value = calculate_nse(obsdata,basin_daily_out,evaluation_timestep,evl_start_year,evl_start_month,evl_end_year,evl_end_month)
    
    out = str(idx) + "," + str(s1) + "," + str(s2) + "," + str(po) + "," + str(pa) + "," + str(gw1) + "," + str(gw2) + "," + str(snowmelt_tcoef) + "," + evaluation_timestep \
    + "," + str(cal_nse_value) + "," + str(evl_nse_value) + "\n"
    
    local_fname_cal_evl_result = fname_cal_evl_result #outputdir + "/" + "cal_evl_nse_" + str(idx) + ".txt"
    outf = open(local_fname_cal_evl_result,"a")
    #outf.write("idx,s1,s2,po,pa,gw1,gw2,snowmelt_tcoef,period,nse_cal,nse_evl\n")
    outf.write(out)
    outf.close
    idx += 1
    return -cal_nse_value
             


#Run RHESSys related
cwd = os.getcwd()
RHESSys="/home/mingliang.liu/scripts/RHESSys_WMFire/RHESSys_WMFire_git/build/Qt/gcc/RHESSys/RHESSys_WMFire_InputFire"
droot="/weka/data/lab/adam/mingliang.liu/Projects/FireEarth/Cedar"
RHESSys_outputdir=sys.argv[1]  #"/scratch/user/mingliang.liu/20221227_162036/Output_calibrations/hydrology"
if not os.path.exists(RHESSys_outputdir):
    command_line = "mkdir -p " + RHESSys_outputdir  
    os.system(command_line)
os.chdir(droot)


flowtable = droot + "/liu_Cedar.flow"
worldfile = droot + "/liu_Cedar.world.Y2015M1D1H1.state.Y2015M1D1H1.state"

#flowtable = droot + "/hill336.flow"
#worldfile = droot + "/hill336.state"


tecfile = droot + "/calibration.tec"
headfile =  droot + "/defFiles.hdr"
output_pre = RHESSys_outputdir + "/calib"
patchgrid = droot + "/patchGrid.txt"
demgrid = droot + "/DemGrid.txt"
sim_startyear = 1980
sim_endyear = 2017
#spyrs = 10 #10
##soil_spins=50
##veg_spins=20 #25
#spins = 2

#06272023
spyrs = 4 #10
#soil_spins=50
#veg_spins=20 #25
spins = 1

#${RHESSys} -netcdfgrid -ncgridinterp 10 -t ${tecfile} -w ${worldfile} -whdr br_with_fire.hdr -start_from_zero_vegpools -st 1980 01 01 01 -ed ${endyear} 12 31 24 -pre ${output_pre} -s ${s1} ${s2} -sv ${s1} ${s2} -svalt ${po} ${pa} -gw ${gw1} ${gw2} -r ${flowtable} -g -b -p -c -firespread 100 ../../../../auxdata/patchgrid.txt ../../../../auxdata/demgrid.txt -Ndecayrate 3.0 -firespin ${spyrs} ${veg_spins} 

#calibration related
calibration_method = "differential_evolution"   #"differential_evolution" "dual_annealing" "minimize"
outputdir = "/weka/data/lab/adam/mingliang.liu/Projects/FireEarth/Cedar/Outputs/Output_calibrations_results"
#unit is mm/day??
#fname_basin_daily_out = output_pre + "_basin.daily"
#unit is m,/day??
fname_obs = droot + "/stream_flow_obs.csv"
fname_cal_evl_result = outputdir + "/" + "cal_evl_nse.txt"
if not os.path.exists(outputdir):
    command_line = "mkdir -p " + outputdir  
    os.system(command_line)
evaluation_timesteps = ["yearly","monthly","daily"]  #yearly or daily or monthly    yearly: water year
evaluation_timestep = "monthly"

obsdata = pd.read_csv(fname_obs,delimiter=",",header=0)

outf = open(fname_cal_evl_result,"w")
outf.write("idx,s1,s2,po,pa,gw1,gw2,snowmelt_tcoef,period,nse_cal,nse_evl\n")
outf.close()

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
par = [-1,2]
gw1r = [0.1,0.8]
#07102023LML gw2r = [-3,3]
gw2r = [0.01,0.9]
snowmelt_tcoefr = [0.0016,0.006]

idx = 0
lhs = lhs(6,samples=1)

if calibration_method == "minimize": #"differential_evolution" "dual_annealing" "minimize"
    #minimization method
    x0 = lhs[0]
    opt = {"maxiter" : 200, "maxfev" : 200}
    result = minimize(objective,x0, method="nelder-mead", tol=1e-2, bounds=((0,1),(0,1),(0,1),(0,1),(0,1),(0,1)),options=opt)
elif calibration_method == "dual_annealing":
    #dual_annealing method
    result = dual_annealing(objective,[[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]],maxiter=50,maxfun=50,no_local_search=True)
elif calibration_method == "differential_evolution":
    result = differential_evolution(objective,[(0,1),(0,1),(0,1),(0,1),(0,1),(0,1)],maxiter=6,popsize=8,tol=1e-3,atol=1e-2)

print(result)

outf = open(fname_cal_evl_result,"w")
outf.write(str(result))
outf.close()

os.chdir(cwd)
