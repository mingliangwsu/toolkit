#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Oct.26 2023
@author: liuming
"""
import sys 
import re
#______________________________________________________________________________
def is_decimal_string(s):
    try:
        float_value = float(s)
        return True
    except ValueError:
        return False
#______________________________________________________________________________
def is_number_using_builtin_methods(s):
    return s.isdigit() or is_decimal_string(s) or s.isnumeric()
#______________________________________________________________________________
def remove_empty_elements_with_list_comprehension(str_list):
    return [s for s in str_list if s.strip()]
#______________________________________________________________________________
#only get valid data (i.e. remove empty rows and empty records)
def get_rows(text):
    # Split the text into lines using newline character as separator
    lines = text.split('\n')
    layers = dict()
    for index,line in enumerate(lines):
        # Count the number of words separated by tabs in each line
        cols = line.split('\t')
        #print(cols[0])
        #print(is_number_using_builtin_methods(cols[0]))
        # Check if the current line has more words than the previous maximum
        if cols[0] != '':
            layers[index] = remove_empty_elements_with_list_comprehension(cols)
    return layers
#______________________________________________________________________________
#everything
def get_rows_all(text):
    # Split the text into lines using newline character as separator
    lines = text.split('\n')
    layers = dict()
    for index,line in enumerate(lines):
        # Count the number of words separated by tabs in each line
        cols = line.split('\t')
        #print(cols[0])
        #print(is_number_using_builtin_methods(cols[0]))
        # Check if the current line has more words than the previous maximum
        layers[index] = cols
    return layers
#______________________________________________________________________________
def get_numbers_from_string(text):
    # Use regex to find all numbers in the string
    numbers = re.findall(r'\d+', text)
    return [int(num) for num in numbers]
#______________________________________________________________________________
def get_word_after_multi_word_string(text, target_string):
    # Escape the target_string to handle any special characters
    escaped_target = re.escape(target_string)
    
    # Create a regular expression pattern to match the target_string followed by word(s)
    pattern = escaped_target + r'\s+(\b[\w.]+\b)' #r'\s+(\b\w+\b)'
    pattern = r'(?<=\b' + re.escape(target_string) + r'\b)\s*(\S+)'
    
    # Search for the pattern in the text
    match = re.search(pattern, text)
    
    if match:
        # Get the word(s) after the target string from the first capturing group
        word_after_string = match.group(1)
        return word_after_string
    else:
        return None  # Target string not found in the text

import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt

import re
if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1gis_elevation> <2output_slope> <3output_aspect>\n")                  # all gridcells (including nodata in mode) will generated a unique ID for each gridcell (start 1 from upper-left corner)
    sys.exit(0)

# Specify the input ESRI ASCII file and output file names
input_dem_file = sys.argv[1]
output_slope_file = sys.argv[2]
output_aspect_file = sys.argv[3]

with open(input_dem_file, 'r') as file:
    mode = file.read()
xll = get_word_after_multi_word_string(mode,'xllcorner')
yll = get_word_after_multi_word_string(mode,'yllcorner')


# Open the DEM file using GDAL
ds = gdal.Open(input_dem_file)

# Read the elevation data into a NumPy array
elevation = ds.ReadAsArray()

# Calculate the slope using NumPy
slope_degrees = np.arctan(np.sqrt(np.square(np.gradient(elevation, axis=0)) + np.square(np.gradient(elevation, axis=1))))

# Convert the slope to degrees
slope_degrees = np.degrees(slope_degrees)

# Calculate the aspect (direction in degrees)
aspect_degrees = np.arctan2(-np.gradient(elevation, axis=0), np.gradient(elevation, axis=1))
aspect_degrees[aspect_degrees < 0] += 360.0  # Ensure values are between 0 and 360

# Save the slope and aspect as ESRI ASCII files
with open(output_slope_file, 'w') as slope_output:
    slope_output.write("ncols {}\n".format(ds.RasterXSize))
    slope_output.write("nrows {}\n".format(ds.RasterYSize))
    slope_output.write("xllcorner {}\n".format(xll)) #ds.GetGeoTransform()[0]))
    slope_output.write("yllcorner {}\n".format(yll)) #ds.GetGeoTransform()[3]))
    slope_output.write("cellsize {}\n".format(ds.GetGeoTransform()[1]))
    slope_output.write("NODATA_value -9999\n")
    np.savetxt(slope_output, slope_degrees, fmt='%10.6f')

with open(output_aspect_file, 'w') as aspect_output:
    aspect_output.write("ncols {}\n".format(ds.RasterXSize))
    aspect_output.write("nrows {}\n".format(ds.RasterYSize))
    aspect_output.write("xllcorner {}\n".format(xll)) #ds.GetGeoTransform()[0]))
    aspect_output.write("yllcorner {}\n".format(yll)) #ds.GetGeoTransform()[3]))
    aspect_output.write("cellsize {}\n".format(ds.GetGeoTransform()[1]))
    aspect_output.write("NODATA_value -9999\n")
    np.savetxt(aspect_output, aspect_degrees, fmt='%10.6f')

# Close the DEM dataset
ds = None


plt.contourf(elevation, cmap='viridis')  # Use 'viridis' colormap or choose another
# Add color bar for reference
plt.colorbar()
# Show the plot
plt.show()

plt.contourf(slope_degrees, cmap='viridis')  # Use 'viridis' colormap or choose another
# Add color bar for reference
plt.colorbar()
# Show the plot
plt.show()

plt.contourf(aspect_degrees, cmap='viridis')  # Use 'viridis' colormap or choose another
# Add color bar for reference
plt.colorbar()
# Show the plot
plt.show()

        
print(sys.argv[0] + ' Done!')
    

    