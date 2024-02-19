#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:03:07 2023

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



if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1input> <2output> <3cell_size> <4xll_corner> <5yll_corner> <6nodata_value>\n")
    sys.exit(0)
    
if len(sys.argv) > 1:
    arguments = sys.argv[1:]
    #print("Arguments passed:", arguments)
else:
    print("No arguments provided.")
# Open the file in read mode ('r')

with open(arguments[0], 'r') as file:
    # Read the entire content of the file
    file_content = file.read()
#print(file_content)

rows = get_rows(file_content)
#print(rows)

#Generate output file
# Open the file in read mode ('r')
with open(arguments[1], 'w') as file:
    outstr = 'ncols ' + str(len(rows[0])) + '\n'
    file.write(outstr)
    
    outstr = 'nrows ' + str(len(rows)) + '\n'
    file.write(outstr)
    
    outstr = 'xllcorner ' + arguments[3] + '\n'
    file.write(outstr)
    
    outstr = 'yllcorner ' + arguments[4] + '\n'
    file.write(outstr)
    
    outstr = 'cellsize ' + arguments[2] + '\n'
    file.write(outstr)
    
    outstr = 'NODATA_value ' + arguments[5] + '\n'
    file.write(outstr)
    
    
    for layer in rows:
        for index,col in enumerate(rows[layer]):
            if col == 'TRUE' or col == 'True':
                out = '1'
            elif col == 'FALSE' or col == 'False':
                out = '0'
            else:
                out = col
            if index < len(rows[layer]) - 1:
                file.write(out + ' ')
            else:
                file.write(out + '\n')
print(sys.argv[0] + ' Done!')
    

    