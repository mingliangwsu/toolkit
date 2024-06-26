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


#use_old_veg_parameter_lai = True

#outdir = "/home/liuming/Projects/GCAM_lucc"
outdir = "/home/liuming/Projects/GCAM_lucc_190902"

forecast2020_path = "/home/liuming/mnt/hydronas1/Projects/Forecast2020"

#inputdir = "/mnt/hydronas/Projects/Forecast2020"
inputdir = forecast2020_path + "/GCAM_landuse_projections_081519"

#timeseries = ["GCAM_landuse_baseline", "GCAM_landuse_projections"]
timeseries = ["Baseline", "GCAM_landuse_projections"]
years = ["2015", "2060"]
rcp_scenarios = ["RCP_4.5","RCP_8.5"]
rcp_file_names = ["RCP_4p5", "RCP_8p5"]
lucc_scenarios = ["expanded", "no_expansion", "max_expansion"]


#timeseries = ["GCAM_landuse_projections"]
#years = ["2060"]
#rcp_scenarios = ["RCP_4.5"]
#rcp_file_names = ["4p5"]
#lucc_scenarios = ["all_expanded"]


#soil_parameter_file = "/mnt/hydronas/Projects/Forecast2020/Landuse/soil_param_crb2.txt"
#old_crop_parameter_file = "/mnt/hydronas/Projects/Forecast2020/Landuse/crop_parameter2016_crb_final.txt"
soil_parameter_file = forecast2020_path + "/Landuse/soil_param_crb2.txt"
old_crop_parameter_file = forecast2020_path + "/Landuse/crop_parameter2016_crb_final.txt"

#if use_old_veg_parameter_lai:
#    old_veg_parameter_filename = "/mnt/hydronas/Projects/Forecast2020/Landuse/vegparam_final2016_with_crp.txt"

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

planting_date_dic = {
                    "102" : "60",
                    "106" : "60",
                    "107" : "60",
                    "201" : "60",
                    "202" : "60",
                    "204" : "60",
                    "206" : "60",
                    "207" : "60",
                    "209" : "60",
                    "210" : "60",
                    "218" : "265",
                    "220" : "60",
                    "222" : "60",
                    "505" : "60",
                    "508" : "60",
                    "509" : "60",
                    "601" : "60",
                    "602" : "60",
                    "603" : "60",
                    "701" : "60",
                    "703" : "60",
                    "708" : "60",
                    "713" : "60",
                    "720" : "60",
                    "721" : "60",
                    "722" : "60",
                    "723" : "60",
                    "724" : "60",
                    "901" : "60",
                    "1001" : "60",
                    "1101" : "60",
                    "1207" : "60",
                    "1208" : "60",
                    "1401" : "1",
                    "1403" : "1",
                    "1407" : "1",
                    "1409" : "1",
                    "1412" : "1",
                    "1498" : "1",
                    "1501" : "1",
                    "1502" : "60",
                    "1503" : "60",
                    "1507" : "60",
                    "1509" : "60",
                    "1513" : "60",
                    "1517" : "60",
                    "1519" : "60",
                    "1520" : "60",
                    "1526" : "60",
                    "1527" : "60",
                    "1802" : "60",
                    "1803" : "60",
                    "1804" : "60",
                    "1807" : "60",
                    "1809" : "60",
                    "1810" : "60",
                    "1811" : "60",
                    "1813" : "60",
                    "1814" : "60",
                    "1817" : "60",
                    "1819" : "60",
                    "1822" : "60",
                    "1824" : "60",
                    "1825" : "60",
                    "1826" : "60",
                    "1827" : "60",
                    "1831" : "60",
                    "1832" : "60",
                    "1839" : "60",
                    "1901" : "60",
                    "1902" : "60",
                    "1904" : "60",
                    "1905" : "60",
                    "1907" : "60",
                    "2001" : "60",
                    "2002" : "1"
                    }

crop_col5_dic = {
                    "102" : "0",
                    "106" : "0",
                    "107" : "0",
                    "201" : "0",
                    "202" : "0",
                    "204" : "0",
                    "206" : "0",
                    "207" : "0",
                    "209" : "0",
                    "210" : "0",
                    "218" : "0",
                    "220" : "0",
                    "222" : "0",
                    "505" : "0",
                    "508" : "0",
                    "509" : "0",
                    "601" : "0",
                    "602" : "0",
                    "603" : "0",
                    "701" : "0",
                    "703" : "0",
                    "708" : "0",
                    "713" : "0",
                    "720" : "0",
                    "721" : "0",
                    "722" : "0",
                    "723" : "0",
                    "724" : "0",
                    "901" : "0",
                    "1001" : "0",
                    "1101" : "0",
                    "1207" : "0",
                    "1208" : "0",
                    "1401" : "1",
                    "1403" : "1",
                    "1407" : "1",
                    "1409" : "1",
                    "1412" : "1",
                    "1498" : "1",
                    "1501" : "1",
                    "1502" : "0",
                    "1503" : "0",
                    "1507" : "0",
                    "1509" : "0",
                    "1513" : "0",
                    "1517" : "0",
                    "1519" : "0",
                    "1520" : "0",
                    "1526" : "0",
                    "1527" : "0",
                    "1802" : "0",
                    "1803" : "0",
                    "1804" : "0",
                    "1807" : "0",
                    "1809" : "0",
                    "1810" : "0",
                    "1811" : "0",
                    "1813" : "0",
                    "1814" : "0",
                    "1817" : "0",
                    "1819" : "0",
                    "1822" : "0",
                    "1824" : "0",
                    "1825" : "0",
                    "1826" : "0",
                    "1827" : "0",
                    "1831" : "0",
                    "1832" : "0",
                    "1839" : "0",
                    "1901" : "0",
                    "1902" : "0",
                    "1904" : "0",
                    "1905" : "0",
                    "1907" : "0",
                    "2001" : "0",
                    "2002" : "1"
                    }

defalt_irrigation_dic = {
                    "102" : "35",
                    "106" : "35",
                    "107" : "35",
                    "201" : "35",
                    "202" : "9",
                    "204" : "35",
                    "206" : "9",
                    "209" : "9",
                    "210" : "35",
                    "218" : "71",
                    "222" : "35",
                    "509" : "35",
                    "601" : "35",
                    "603" : "9",
                    "701" : "35",
                    "703" : "35",
                    "708" : "35",
                    "713" : "35",
                    "721" : "9",
                    "722" : "9",
                    "723" : "35",
                    "724" : "35",
                    "901" : "35",
                    "1001" : "35",
                    "1101" : "35",
                    "1207" : "71",
                    "1208" : "35",
                    "1401" : "9",
                    "1403" : "42",
                    "1407" : "42",
                    "1409" : "42",
                    "1412" : "35",
                    "1498" : "42",
                    "1501" : "9",
                    "1502" : "35",
                    "1503" : "9",
                    "1507" : "9",
                    "1509" : "9",
                    "1513" : "9",
                    "1517" : "35",
                    "1519" : "35",
                    "1520" : "9",
                    "1526" : "35",
                    "1527" : "35",
                    "1802" : "9",
                    "1803" : "9",
                    "1804" : "9",
                    "1807" : "35",
                    "1809" : "35",
                    "1810" : "9",
                    "1811" : "35",
                    "1813" : "42",
                    "1814" : "9",
                    "1817" : "35",
                    "1819" : "52",
                    "1822" : "35",
                    "1824" : "9",
                    "1825" : "35",
                    "1826" : "35",
                    "1827" : "35",
                    "1831" : "35",
                    "1832" : "9",
                    "1839" : "35",
                    "1901" : "9",
                    "1902" : "9",
                    "1904" : "9",
                    "1907" : "35",
                    "2001" : "42",
                    "2002" : "9"
                    }

"""
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
"""

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


cell_plant_dic = {}
cell_irrig_dic = {}
cell_col5_dic = {}
#read crop parameter to create crop dictionary (for planting date, irrigation, col5)
with open(old_crop_parameter_file) as f:
    for line in f:
        a = line.split()
        if len(a) == 2:
            cellid = a[0]
        elif len(a) == 6:
            crop = a[0]
            plant = a[2]
            irrig = a[3]
            col5 = a[4]
            key = cellid + "_" + crop
            cell_plant_dic.update({key : plant})
            cell_irrig_dic.update({key : irrig})
            cell_col5_dic.update({key : col5})
            #print(location + ':' + cellid)
print("reading crop parameter done!")



"""
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
"""

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
        year = "2015"
    else:
        trcp_scenarios = rcp_scenarios
    for scn_i in range(len(trcp_scenarios)):
        if time == "Baseline":
            tlucc_scenarios = ["fractions"]
        else:
            tlucc_scenarios = lucc_scenarios
        for lucc in tlucc_scenarios:
            print(time + ":" + rcp_scenarios[scn_i] + ":" + lucc)
            if time == "Baseline":
                fraction_filename = inputdir + "/" + time + "/" + trcp_scenarios[scn_i] + "_" + year + "_all_" + lucc + ".csv"
                irrigation_filename = inputdir + "/" + time + "/" + trcp_scenarios[scn_i] + "_" + year + "_irrigated_" + lucc + ".csv"
            else:
                fraction_filename = inputdir + "/" + time + "/" + trcp_scenarios[scn_i] + "/" + rcp_file_names[scn_i] + "_" + year + "_all_" + lucc + ".csv"
                irrigation_filename = inputdir + "/" + time + "/" + trcp_scenarios[scn_i] + "/" + rcp_file_names[scn_i] + "_" + year + "_irrigated_" + lucc + ".csv"
            out_crop_parameter_filename = outdir + "/crop_parameter_" + time + "_" + trcp_scenarios[scn_i] + "_" + year + "_" + lucc + ".txt"
            outfile_crop = open(out_crop_parameter_filename,"w")
            
            
            #read irrigation file at first to create irrigation fraction dictionary
            #irrigation_filename = inputdir + "/" + time + "/" + trcp_scenarios[scn_i] + "/" + rcp_file_names[scn_i] + "_" + year + "_irrigated_" + lucc + ".csv"
            
            cell_irrigated_area_dic = {}
            with open(irrigation_filename) as f:
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
                                #total_area = 0
                                #total_veg_num = 0
                                #for ov in range(0,len(out_veg_list)):
                                    #total_area += tot_fractions[ov]
                                #    if (tot_fractions[ov] > 0.001):
                                #        total_veg_num += 1
                                #line = cellid + " " + str(total_veg_num) + "\n"
                                #outfile_crop.write(line)
                                for ov in range(0,len(out_veg_list)):
                                    if (tot_fractions[ov] > 0.001):
                                        dickey = cellid + "_" + out_veg_list[ov]
                                        cell_irrigated_area_dic.update({dickey : tot_fractions[ov]})
            print(irrigation_filename + " read finished!\n")
            
            
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
                                    if int(out_veg_list[ov]) > 100:
                                        total_area += tot_fractions[ov]
                                        if (tot_fractions[ov] > 0.001):
                                            total_veg_num += 1
                                line = cellid + " " + str(total_veg_num) + "\n"
                                outfile_crop.write(line)
                                for ov in range(0,len(out_veg_list)):
                                    if ((tot_fractions[ov] > 0.001) and (int(out_veg_list[ov]) > 100)):
                                        cell_key = cellid + "_" + out_veg_list[ov]
                                        #identify planting date
                                        if cell_key in cell_plant_dic:
                                            plant = cell_plant_dic[cell_key]
                                        elif out_veg_list[ov] in planting_date_dic:
                                            plant = planting_date_dic[out_veg_list[ov]]
                                        else:
                                            plant = "60"
                                        #identify irrigation type
                                        irrigated_fraction = 0.0
                                        if cell_key in cell_irrigated_area_dic:
                                            irrigated_fraction = cell_irrigated_area_dic[cell_key]
                                        dry = tot_fractions[ov] - irrigated_fraction
                                        if irrigated_fraction >= dry:
                                            if cell_key in cell_irrig_dic:
                                                if cell_irrig_dic[cell_key] != "0":
                                                    irrig = cell_irrig_dic[cell_key]
                                                elif out_veg_list[ov] in defalt_irrigation_dic:
                                                    irrig = defalt_irrigation_dic[out_veg_list[ov]]
                                                else:
                                                    irrig = "35"
                                        else:
                                            irrig = "0"
                                        #identify col5
                                        if cell_key in cell_col5_dic:
                                            col5v = cell_col5_dic[cell_key]
                                        elif out_veg_list[ov] in crop_col5_dic:
                                            col5v = crop_col5_dic[out_veg_list[ov]]
                                        else:
                                            col5v = "0"
                                        col6v = "1"
                                        
                                        line = "   " + out_veg_list[ov] + " " + str('%.4f' % tot_fractions[ov]) + " " + plant + " " + irrig + " " + col5v + " " + col6v + "\n"
                                        outfile_crop.write(line)
            outfile_crop.close()
#outfile_irrig.close()
        
            
            
print("Done!")
