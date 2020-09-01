#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 18:08:39 2020

@author: liuming
"""
import os

fraction_data_path = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/GCAM_scenario_land_use"
script_path = "/home/liuming/dev/toolkit/ForVIC/python"
script = "generate_cropirrigation_parameter_from_original_veg_irigation_parameter_and_updated_fraction_GCM.py"
veg_irrigation_path = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/irrigation"

"""
scenarios = {
    "baseline_2015_new_CropSyst.csv"                : "baseline_2015",
    "RCP_4p5_2060_expanded_new_CropSyst.csv"        : "RCP_4p5_2060_expanded",
    "RCP_4p5_2060_max_expansion_new_CropSyst.csv"   : "RCP_4p5_2060_max_expansion",
    "RCP_4p5_2060_no_expansion_new_CropSyst.csv"    : "RCP_4p5_2060_no_expansion",
    "RCP_8p5_2060_expanded_new_CropSyst.csv"        : "RCP_8p5_2060_expanded",
    "RCP_8p5_2060_max_expansion_new_CropSyst.csv"   : "RCP_8p5_2060_max_expansion",
    "RCP_8p5_2060_no_expansion_new_CropSyst.csv"    : "RCP_8p5_2060_no_expansion"
        }
"""
scenarios = {
    "baseline_2015_new_CropSyst.csv"                : "baseline_2015"
        }

invegfile = veg_irrigation_path + "/pnw_veg_parameter_filledzero.txt"
inirrfile = veg_irrigation_path + "/pnw_irrigation.txt"

for scenerio in scenarios:
    newfractionfile = fraction_data_path + "/" + scenerio
    outvegfile = fraction_data_path + "/" + scenarios[scenerio] + "_veg_parameter.txt"
    outirrfile = fraction_data_path + "/" + scenarios[scenerio] + "_irrigation.txt"
    pyscript_cmd = "python " + script_path + "/" + script + " " + newfractionfile + " " + \
               invegfile + " " + inirrfile + " " + outvegfile  + " " + outirrfile
    print(pyscript)
    print("\n")
    os.system(pyscript_cmd)
print("Done All!\n")