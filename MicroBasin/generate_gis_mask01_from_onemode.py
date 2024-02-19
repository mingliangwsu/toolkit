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



import re
if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1gis_mode> <2output>\n")                  # if gis_mode >= 1; then output is 1; otherwise it is 0
    sys.exit(0)

# Open the input file for reading and the output file for writing
keys = ['ncols','nrows','xllcorner','yllcorner','cellsize','NODATA_value']
#ol_row = int(sys.argv[3])
#ol_col = int(sys.argv[4])
#value = float(sys.argv[3])
nodata = -9999
with open(sys.argv[1], 'r') as input_file, open(sys.argv[2], 'w') as output_file:
    # Read and write the data line by line
    row_id = 0
    for line in input_file:
        elems = re.split(r'[ \t]+', line)
        if elems[0] not in keys:
            row_id += 1
            col_id = 0
            for elem in elems:
                col_id += 1
                if int(elem) >= 1:
                    out = 1
                else:
                    out = 0
                output_file.write(str(out) + ' ')
            output_file.write('\n')
        else:
            output_file.write(line) 
            if elems[0] == 'NODATA_value':
                nodata = int(elems[1])
        
print(sys.argv[0] + ' Done!')
    

    