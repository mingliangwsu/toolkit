#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 12:25:53 2018
Replace crop parameter from txt input
@author: liuming
"""
import pandas as pd
import sys 
import os



outdir = "/home/liuming/Projects/WSU_BPA/VIC-CropSyst/Simulation/Database/Crop/Name"
os.chdir(outdir)
#arguments: original_parameter_filename

crop_parameter_file_name = sys.argv[1]
new_parameter_name = sys.argv[2]
crop_name = crop_parameter_file_name.split('.')[0]

#print(crop_name)

out_script = "replace_" + crop_name + ".sh"
outfile = open(out_script, 'w')
outfile.write("#!/bin/bash" + '\n')
line = "outfilename=" + crop_parameter_file_name + '\n'
outfile.write(line)

line = "if grep -q \"CC_initial\" " + "$outfilename" + "; then\n"
outfile.write(line)
line = "    sed -i " + "'s/^CC_initial=.*/" + "initial=-9999/g' $outfilename\n"
outfile.write(line)
outfile.write("fi\n")

line = "if grep -q \"CC_maximum\" " + "$outfilename" + "; then\n"
outfile.write(line)
line = "    sed -i " + "'s/^CC_maximum=.*/" + "maximum=-9999/g' $outfilename\n"
outfile.write(line)
outfile.write("fi\n")

line = "if grep -q \"CC_mature_green\" " + "$outfilename" + "; then\n"
outfile.write(line)
line = "    sed -i " + "'s/^CC_mature_green=.*/" + "green_season_end=-9999/g' $outfilename\n"
outfile.write(line)
outfile.write("fi\n")

line = "if grep -q \"CC_mature_total\" " + "$outfilename" + "; then\n"
outfile.write(line)
line = "    sed -i " + "'s/^CC_mature_total=.*/" + "total_season_end=-9999/g' $outfilename\n"
outfile.write(line)
outfile.write("fi\n")

line = "if ! grep -q \"thermal_time_season_end\" " + "$outfilename" + "; then\n"
outfile.write(line)
line = "    sed -i '/^total_season_end=.*/athermal_time_season_end=-9999' " + "$outfilename" + "\n"
outfile.write(line)
outfile.write("fi\n")

line = "if ! grep -q \"shape_accrescent=\" " + "$outfilename" + "; then\n"
outfile.write(line)
line = "    sed -i '/^thermal_time_season_end=.*/ashape_accrescent=9' " + "$outfilename" + "\n"
outfile.write(line)
outfile.write("fi\n")

line = "if ! grep -q \"shape_senescent=\" " + "$outfilename" + "; then\n"
outfile.write(line)
line = "    sed -i '/^shape_accrescent=.*/ashape_senescent=9' " + "$outfilename" + "\n"
outfile.write(line)
outfile.write("fi\n")
root = 0

#identify "max_root_depth" sequence in the crop parameter file
line_num = 0
line_phenology = 0
line_root = 0
with open(crop_parameter_file_name) as f:
    for line in f:
        line_num = line_num + 1
        if "[phenology]" in line:
            line_phenology = line_num
        if "[root]" in line:
            line_root = line_num
#print("line_phenology:" + str(line_phenology) + "line_root:" + str(line_root))
#new parameter sequence: [phenology]...[root]
same_sequence = True
if line_phenology > line_root:
    same_sequence = False

with open(new_parameter_name) as f:
    for line in f:
        if "[" not in line:
            line = line.strip('\n')
            all_par = line.split('\t')
            tarvar = all_par[0]
            tarvar_v = all_par[1]
            if tarvar == "max_root_depth":
                root = root + 1
                if root == 1:
                    line = "sed -i " + "'s/^" + tarvar + "=.*/" + tarvar + "/g'" + " $outfilename\n"
                    outfile.write(line)
            
            #print(tarvar + ":" + tarvar_v + "#")
            if len(tarvar_v) > 0 and tarvar != "root_density_distribution_curvature":
                if tarvar_v == "FALSE":
                    tarvar_v = "false"
                if tarvar_v == "TRUE":
                    tarvar_v = "true"
                #print(tarvar + ":" + tarvar_v)
                if tarvar == "max_root_depth":
                    
                    if same_sequence:
                        #line = "sed -i " + "'s/^" + tarvar + "=.*/" + tarvar + "=" + tarvar_v + "/" + str(root) + "'" + " $outfilename\n"
                        line = "sed -i ':a;N;$!ba;s/" + tarvar + "/" + tarvar + "=" + tarvar_v + "/" + str(root) + "'" + " $outfilename\n"
                    else:
                        if root == 1:
                            outroot = 2
                        else:
                            outroot = 1
                        line = "sed -i ':a;N;$!ba;s/" + tarvar + "/" + tarvar + "=" + tarvar_v + "/" + str(outroot) + "'" + " $outfilename\n"
                        #line = "sed -i " + "'s/^" + tarvar + "=.*/" + tarvar + "=" + tarvar_v + "/" + str(outroot) + "'" + " $outfilename\n"
                        #line = "sed -i " + "'s/^" + tarvar + "=.*/" + tarvar + "=" + tarvar_v + "/" + str(outroot) + "'" + " $outfilename\n"
                else:
                    line = "sed -i " + "'s/^" + tarvar + "=.*/" + tarvar + "=" + tarvar_v + "/g' $outfilename\n"
                outfile.write(line)
                #print(line)
            
line = "if ! grep -q \"thermal_response\" " + "\"" + "$outfilename" + "\"" + "; then\n"
outfile.write(line)
line = "    sed -i '/^full_senescence=.*/athermal_response=linear' " + "$outfilename" + "\n"
outfile.write(line)
outfile.write("fi\n")

line = "sed -i '/-9999/d' " + "$outfilename" + "\n"
outfile.write(line)



outfile.close()
print("\n" + new_parameter_name + " Done!\n")
              