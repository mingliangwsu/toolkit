#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26, 2018 LIU 
Convert crop fractions into VIC veg parametger files for running VIC-CropSyst V2 (Forecast project)
@author: liuming
"""

#import pandas as pd
import sys 
import os


use_old_veg_parameter_lai = True

forecast2020_path = "/home/liuming/mnt/hydronas1/Projects/Forecast2020"

outdir = "/home/liuming/Projects/GCAM_lucc_190902"

#inputdir = "/mnt/hydronas/Projects/Forecast2020"
inputdir = forecast2020_path + "/GCAM_landuse_projections_081519"

timeseries = ["Baseline", "GCAM_landuse_projections"]
years = ["2015", "2060"]
rcp_scenarios = ["RCP_4.5","RCP_8.5"]
rcp_file_names = ["RCP_4p5", "RCP_8p5"]
lucc_scenarios = ["expanded", "no_expansion", "max_expansion"]

#soil_parameter_file = "/mnt/hydronas/Projects/Forecast2020/Landuse/soil_param_crb2.txt"
soil_parameter_file = forecast2020_path + "/Landuse/soil_param_crb2.txt"

if use_old_veg_parameter_lai:
    #old_veg_parameter_filename = "/mnt/hydronas/Projects/Forecast2020/Landuse/vegparam_final2016_with_crp.txt"
    old_veg_parameter_filename = forecast2020_path + "/Landuse/vegparam_final2016_with_crp.txt"

os.chdir(outdir)

col_list = ["FID", "Shrubland", "Wetland", "Switchgrass", "Urban", "Deciduous Forest "
                 , "Coniferous Forest", "Alfalfa", "Apples", "Apricots", "Asparagus", "Barley"
                 , "Barren", "Blueberry", "Broccoli", "Buckwheat", "Cabbage", "Camelina"
                 , "Caneberry", "Canola", "Carrots", "Cauliflower", "CherryOrchard"
                 , "Chickpea", "ChristmasTrees", "CloverWildflowers", "Corn", "Cucumber"
                 , "DryBeans", "DurWheat", "Flaxseed", "Garlic", "Grapes", "GrassSeed"
                 , "Greens", "Herbs", "Hops", "Lentils", "Lettuce", "MarketCrops", "Millet"
                 , "Mint", "MiscVegs.Fruits", "Mustard", "NectarineOrPeach", "NurseryOrchardVineyard"
                 , "Oats", "Onions", "OrchardUnknown", "OtherCrops", "OtherHays", "Pasture_Grass"
                 , "Peaches", "Pear", "Peas", "Pepper", "Plum", "Poplar", "PoporOrnCorn"
                 , "Potatoes", "Pumpkin", "Radish", "RapeSeed", "Rye", "Safflower", "Seed_SodGrass"
                 , "Sorghum", "Soybeans", "Speltz", "SpgWheat", "Squash", "Strawberries"
                 , "Sugarbeets", "Sunflowers", "SweetCorn", "Triticale", "Turnips"
                 , "Vetch", "Walnuts", "Watermelon", "WinWheat", "Latcoord", "Loncoord"]

#if there is fractional irrigated crops in grid cell. the irrigated crop is coded as the original crops 
# and the non-irrigated crops are coded as the origincal code + 10,000
# LML: there is an asumption that all crops without "dryland" in the name are irigated, i.e. there is no irrigation (1 or 0) file as input to generate irrigation map

cdl_to_vic_dic = {
                    "Shrubland"         : "6",
                    "Wetland"           : "6",
                    "Switchgrass"       : "713",
                    "Deciduous Forest " : "4",
                    "Coniferous Forest" : "1",
                    "Alfalfa"           : "701",
                    "Apples"            : "1401",
                    "Apricots"          : "1412",
                    "Asparagus"         : "1802",
                    "Barley"            : "201",
                    "Blueberry"         : "102",
                    "Broccoli"          : "1807",
                    "Buckwheat"         : "202",
                    "Cabbage"           : "1809",
                    "Camelina"          : "1905",
                    "Caneberry"         : "107",
                    "Canola"            : "1902",
                    "Carrots"           : "1810",
                    "Cauliflower"       : "1811",
                    "CherryOrchard"     : "1403",
                    "Chickpea"          : "1813",
                    "ChristmasTrees"    : "402",
                    "CloverWildflowers" : "508",
                    "Corn"              : "204",
                    "Cucumber"          : "1815",
                    "DryBeans"          : "1803",
                    "DurWheat"          : "220",
                    "Flaxseed"          : "1514",
                    "Garlic"            : "1817",
                    "Grapes"            : "2002",
                    "GrassSeed"         : "1527",
                    "Greens"            : "1841",
                    "Herbs"             : "723",
                    "Hops"              : "901",
                    "Lentils"           : "1819",
                    "Lettuce"           : "1820",
                    "MarketCrops"       : "1821",
                    "Millet"            : "223",
                    "Mint"              : "1101",
                    "MiscVegs.Fruits"   : "1450",
                    "Mustard"           : "1904",
                    "NectarineOrPeach"  : "1407",
                    "NurseryOrchardVineyard" : "1304",
                    "Oats"              : "206",
                    "Onions"            : "1822",
                    "OrchardUnknown"    : "1498",
                    "OtherCrops"        : "724",
                    "OtherHays"         : "1207",
                    "Pasture_Grass"     : "1208",
                    "Peaches"           : "1408",
                    "Pear"              : "1409",
                    "Peas"              : "1824",
                    "Pepper"            : "1826",
                    "Plum"              : "1410",
                    "Poplar"            : "403",
                    "PoporOrnCorn"      : "224",
                    "Potatoes"          : "1827",
                    "Pumpkin"           : "1828",
                    "Radish"            : "1839",
                    "RapeSeed"          : "1536",
                    "Rye"               : "207",
                    "Safflower"         : "1907",
                    "Seed_SodGrass"     : "509",
                    "Sorghum"           : "720",
                    "Soybeans"          : "806",
                    "Speltz"            : "807",
                    "SpgWheat"          : "210",
                    "Squash"            : "1831",
                    "Strawberries"      : "106",
                    "Sugarbeets"        : "1832",
                    "Sunflowers"        : "222",
                    "SweetCorn"         : "1814",
                    "Triticale"         : "209", 
                    "Turnips"           : "808",
                    "Vetch"             : "602", 
                    "Walnuts"           : "1411",
                    "Watermelon"        : "1001",
                    "WinWheat"          : "218"
                    }

paramter_dic = {"1"  : "0.1 0.05 1 0.45 5 0.5",
                "2"  : "0.1 0.05 1 0.45 5 0.5",
                "3"  : "0.1 0.05 1 0.45 5 0.5",
                "4"  : "0.1 0.05 1 0.45 5 0.5",
                "5"  : "0.1 0.05 1 0.45 5 0.5",
                "6"  : "0.1 0.1 1 0.65 1 0.25",
                "7"  : "0.1 0.1 1 0.65 1 0.25",
                "8"  : "0.1 0.1 1 0.65 0.5 0.25",
                "9"  : "0.1 0.1 1 0.65 0.5 0.25",
                "10" : "0.1 0.1 1 0.7 0.5 0.2",
                "11" : "0.1 0.1 0.75 0.6 0.5 0.3",
                "12" : "0.1 0.1 0.75 0.6 0.5 0.3",
                "13" : "0.1 0.1 0.75 0.6 0.5 0.3"}
default_veg_parameter = "0.1 0.1 0.75 0.6 0.5 0.3"

if use_old_veg_parameter_lai:
    lai_dic_default = {
            "1"    : "3.4 3.4 3.5 3.7 4 4.4 4.4 4.3 4.2 3.7 3.5 3.4",
            "2"    : "3.4 3.4 3.5 3.7 4 4.4 4.4 4.3 4.2 3.7 3.5 3.4",
            "3"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "4"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "5"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "6"    : "1.68 1.52 1.68 2.9 4.9 5 5 4.6 3.44 3.04 2.16 2",
            "7"    : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "8"    : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "9"    : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "10"   : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "11"   : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "102"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "103"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "106"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "107"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "201"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "202"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "204"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "206"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "207"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "209"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "210"  : "0 0 0 0 0 0 0 0 0 0 0 0",
            "218"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "220"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "221"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "222"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "223"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "224"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "401"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "402"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "403"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "502"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "505"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "508"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "509"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "601"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "602"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "603"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "701"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "702"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "703"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "708"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "713"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "720"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "721"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "722"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "723"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "724"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "806"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "807"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "808"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "901"  : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1001" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1101" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1207" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1208" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1303" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1304" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1311" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1401" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1403" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1407" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1408" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1409" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1410" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1411" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1412" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1413" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1450" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1498" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1501" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1502" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1503" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1507" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1509" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1510" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1513" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1514" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1517" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1519" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1520" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1526" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1527" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1531" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1536" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1802" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1803" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1804" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1807" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1809" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1810" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1811" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1813" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1814" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1815" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1817" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1819" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1820" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1821" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1822" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1824" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1825" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1826" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1827" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1828" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1831" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1832" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1839" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1841" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1901" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1902" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1904" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1905" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "1907" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "2001" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "2002" : "0.5 0.5 0.5 0.5 1.5 3 4.5 5 2.5 0.5 0.5 0.5",
            "9803" : "2 2.25 2.95 3.85 3.75 3.5 3.55 3.2 3.3 2.85 2.6 2.2",
            "9898" : "0 0 0 0 0 0 0 0 0 0 0 0"
            }


location_dic = {}
#read soil parameter to create location dictionary
with open(soil_parameter_file) as f:
    for line in f:
        a = line.split()
        if len(a) > 0:
            cellid = a[1]
            lat = a[2]
            lon = a[3]
            location=lat + '_' + lon
            location_dic.update({location : cellid})
            #print(location + ':' + cellid)
print("reading soil done!")

#read old veg dic and creat a dictionary
lai_dic = {}
if use_old_veg_parameter_lai:
    with open(old_veg_parameter_filename) as v:
        for line in v:
            a = line.split()
            if (len(a) == 2):
                gridid = a[0]
            elif (len(a) == 8):
                vegid = a[0]
            elif (len(a) == 12):
                lai_key = gridid + "_" + vegid
                lai_dic.update({lai_key : line})
    print("reading veg parameter is done")


#snap to the center of VIC grid cell
def float_to_vic_center_loc(x):
    number_dec = abs(x) % 1
    dec = int((number_dec - 0.03125 ) / 0.0625 + 0.5) * 0.0625 + 0.03125
    if x > 0:
        out_cell_loc = str(int(x) + dec)
    else:
        out_cell_loc = str(int(x) - dec)
    return out_cell_loc


#out_veg_list = ["1", "4", "5", "10", "701", "807", "1401", "1403", "2501", "4004", "4005", "4006", "4007", "4008", "4009", "4010", "4011", "4100", "4101", "4102", "4103", "4104", "6001"]

out_veg_list = ["1", "4", "6", "102", "106", "107", "201", "202", "204", "206"
                , "207", "209", "210", "218", "220", "222", "223", "224", "402"
                , "403", "508", "509", "602", "701", "713", "720", "723", "724"
                , "806", "807", "808", "901", "1001", "1101", "1207", "1208"
                , "1304", "1401", "1403", "1407", "1408", "1409", "1410", "1411"
                , "1412", "1450", "1498", "1514", "1527", "1536", "1802", "1803"
                , "1807", "1809", "1810", "1811", "1813", "1814", "1815", "1817"
                , "1819", "1820", "1821", "1822", "1824", "1826", "1827", "1828"
                , "1831", "1832", "1839", "1841", "1902", "1904", "1905", "1907"
                , "2002"]
for time_i in range(len(timeseries)):
    time = timeseries[time_i]
    year = years[time_i]
    if time == "Baseline":
        trcp_scenarios = ["baseline"]
        #trcp_scenarios = ["Baseline"]
        year = "2015"
    else:
        trcp_scenarios = rcp_scenarios
    for scn_i in range(len(trcp_scenarios)):
        if time == "Baseline":
            tlucc_scenarios = ["fractions"]
        else:
            tlucc_scenarios = lucc_scenarios
        for lucc in tlucc_scenarios:
            print(time + ":" + trcp_scenarios[scn_i] + ":" + lucc)
            if time == "Baseline":
                fraction_filename = inputdir + "/" + time + "/" + trcp_scenarios[scn_i] + "_" + year + "_all_" + lucc + ".csv"
            else:
                fraction_filename = inputdir + "/" + time + "/" + trcp_scenarios[scn_i] + "/" + rcp_file_names[scn_i] + "_" + year + "_all_" + lucc + ".csv"

            out_veg_parameter_filename = outdir + "/veg_parameter_" + time + "_" + trcp_scenarios[scn_i] + "_" + year + "_" + lucc + ".txt"
            outfile_veg = open(out_veg_parameter_filename,"w")
            #outfile_irrig = open(out_irrig_file,"w")
            with open(fraction_filename) as f:
                for line in f:
                    if "FID" not in line:
                        if len(line) > 0:
                            #produce veg parameter file
                            tot_fractions = []
                            for veg in out_veg_list:
                                tot_fractions.append(0)
                            a = line.split(',')
                            snaplat = ""
                            snaplon = ""
                            for col in range(0,len(a)):
                                tar_col_cdl = col_list[col]
                                #print("col:" + str(col) + " tar_col_cdl:" + tar_col_cdl + " value:" + a[col])
                                if tar_col_cdl in cdl_to_vic_dic:
                                    tar_vic = cdl_to_vic_dic[tar_col_cdl]
                                    array_index = out_veg_list.index(tar_vic)
                                    tot_fractions[array_index] += float(a[col])
                                elif tar_col_cdl == "Latcoord":
                                    lat = float(a[col])
                                    snaplat = float_to_vic_center_loc(lat)
                                elif tar_col_cdl == "Loncoord":
                                    lon = float(a[col])
                                    snaplon = float_to_vic_center_loc(lon)
                            gridcell_loc = snaplat + "_" + snaplon
                            if gridcell_loc in location_dic:
                                cellid = location_dic[snaplat + "_" + snaplon]
                                total_area = 0
                                total_veg_num = 0
                                for ov in range(0,len(out_veg_list)):
                                    total_area += tot_fractions[ov]
                                    if (tot_fractions[ov] > 0.001):
                                        total_veg_num += 1
                                line = cellid + " " + str(total_veg_num) + "\n"
                                outfile_veg.write(line)
                                for ov in range(0,len(out_veg_list)):
                                    if (tot_fractions[ov] > 0.001):
                                        if out_veg_list[ov] in paramter_dic:
                                            outp = paramter_dic[out_veg_list[ov]]
                                        else:
                                            outp = default_veg_parameter
                                        line = "   " + out_veg_list[ov] + " " + str('%.4f' % tot_fractions[ov]) + " " + outp + "\n"
                                        outfile_veg.write(line)
                                        if use_old_veg_parameter_lai:
                                            laikey = cellid + "_" + out_veg_list[ov]
                                            if laikey in lai_dic:
                                                outlai = lai_dic[laikey]
                                            else:
                                                outlai = "      " + lai_dic_default[out_veg_list[ov]] + "\n"
                                            outfile_veg.write(outlai)
            outfile_veg.close()
#outfile_irrig.close()
        
            
            
print("Done!")
