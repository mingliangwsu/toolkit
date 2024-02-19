#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:03:07 2023
The soil file from excel table is complex and need elevation input as mode
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


if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1input> <2output> <3cell_size> <4xll_corner> <5yll_corner> <6nodata_value> <7raw_elev_model_all_data> <8output look up table>\n")
    sys.exit(0)

# Open the file in read mode ('r')
with open(sys.argv[1], 'r') as file:
    # Read the entire content of the file
    file_content_soil = file.read()
rows_soil = get_rows_all(file_content_soil)
#print(file_content)

#mode to get raster infomation
with open(sys.argv[7], 'r') as file:
    # Read the entire content of the file
    file_content = file.read()
rows = get_rows(file_content)
#print(rows)

#Generate soil index if no number in soil type
soil_idx_list = list()
name_id = dict()
for layer in rows:
    for index,col in enumerate(rows[layer]):
        if layer in rows_soil:
            if index <= len(rows_soil[layer]) - 1:
                #soil_filename_prefix
                if rows_soil[layer][index] != '':
                    soil_name = rows_soil[layer][index].split('\\')[-1]
                    soil_name_pre = soil_name #[:-5]
                    outnums = get_numbers_from_string(rows_soil[layer][index])
                    #print(soil_name + ':' + soil_name_pre)
                    #print(f'{rows_soil[layer][index]}:{outnums}')
                    if len(outnums) > 0:
                        if outnums[0] not in soil_idx_list:
                            soil_idx_list.append(outnums[0])
                        name_id[soil_name_pre] = outnums[0] 
                    else:
                        name_id[soil_name_pre] = None

max_id = max(soil_idx_list) + 1
for soil in name_id:
    if name_id[soil] == None:
        name_id[soil] = max_id
        max_id += 1
print('Soil ID dictionary:')
print(name_id)
with open(sys.argv[8], 'w') as file:
    for soil in name_id:
        file.write(soil + ':' + str(name_id[soil]) + '\n')

#Generate output file
# Open the file in read mode ('r')
with open(sys.argv[2], 'w') as file:
    outstr = 'ncols ' + str(len(rows[0])) + '\n'
    file.write(outstr)
    
    outstr = 'nrows ' + str(len(rows)) + '\n'
    file.write(outstr)
    
    outstr = 'xllcorner ' + sys.argv[4] + '\n'
    file.write(outstr)
    
    outstr = 'yllcorner ' + sys.argv[5] + '\n'
    file.write(outstr)
    
    outstr = 'cellsize ' + sys.argv[3] + '\n'
    file.write(outstr)
    
    outstr = 'NODATA_value ' + sys.argv[6] + '\n'
    file.write(outstr)
    
    
    for layer in rows:
        for index,col in enumerate(rows[layer]):
            if layer not in rows_soil:
                out = sys.argv[6]
            else:
                if index > len(rows_soil[layer]) - 1:
                    out = sys.argv[6]
                else:
                    #soil_filename_prefix
                    soil_name = rows_soil[layer][index].split('\\')[-1]
                    soil_name_pre = soil_name #[:-5]
                    outnums = get_numbers_from_string(rows_soil[layer][index])
                    #if len(outnums) > 0 or soil_name != '':
                    #    print(soil_name + ':' + str(len(outnums)))
                    #print(f'{rows_soil[layer][index]}:{outnums}')
                    if soil_name_pre in name_id:
                        out = str(name_id[soil_name_pre])
                    else:
                        out = str(sys.argv[6])
            if index < len(rows[layer]) - 1:
                file.write(out + ' ')
            else:
                file.write(out + '\n')
print(sys.argv[0] + ' Done!')
    

    