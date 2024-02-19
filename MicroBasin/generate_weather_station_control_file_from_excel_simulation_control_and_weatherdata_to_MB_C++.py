#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:03:07 2023

@author: liuming
"""
import sys 
import re
import pandas as pd
#______________________________________________________________________________
def get_word_before_multi_word_string(text, target_string):
    # Escape the target_string to handle any special characters
    #escaped_target = re.escape(target_string)
    pattern = r'(?:^|\s)((?:[+-]?\d+\.\d+|[+-]?\d+\b|\w+(?:-+\w+)*))(?=\s*' + re.escape(target_string) + ')'

    # Search for the pattern in the text
    #match = re.search(pattern, text)
    matching_words = re.findall(pattern, text)
    
    #if match:
    if matching_words:
        # Get the word(s) before the target string from the first capturing group
        #word_before_string = match.group(1)
        #return word_before_string
        return matching_words[-1]
    else:
        return None  # Target string not found in the text
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
#______________________________________________________________________________
def get_word_after_position(text, position):
    # Find the next whitespace after the given position
    next_space = text.find(" ", position)
    if next_space != -1:
        # Extract the word using slicing
        word = text[position:next_space]
    else:
        # If no whitespace is found, extract the last word
        word = text[position:]
    return word
#______________________________________________________________________________
def get_word_before_position(text, position):
    # Find the previous whitespace before the given position
    prev_space = text.rfind(" ", 0, position)
    if prev_space != -1:
        # Extract the word using slicing
        word = text[prev_space+1:position]
    else:
        # If no whitespace is found, extract the first word
        word = text[:position]
    return word
#______________________________________________________________________________
def find_position_after_string(text, search_string):
    position = text.find(search_string)
    position_after_string = -1
    if position != -1:
        # If the string is found, print the position after the search string
        position_after_string = position + len(search_string)
        #print(f"'{search_string}' found at position: {position}")
        #print(f"Position after '{search_string}': {position_after_string}")
    else:
        print(f"'{search_string}' not found in the text.")
    return position_after_string
#______________________________________________________________________________
def get_first_word_after_position(text, position):
    # Find the next word after the given position using regex
    match = re.search(r'\s*(\S+)', text[position:])
    if match:
      return match.group(1)
    else:
      return None
#______________________________________________________________________________
def get_second_word_after_position(text, position):
    # Find the second word after the given position using regex
    matches = re.findall(r'\s*(\S+)', text[position:])
    if len(matches) >= 2:
        return matches[1]
    else:
        return None
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
def get_first_layer(text):
    # Split the text into lines using newline character as separator
    lines = text.split('\n')
    pass_layer_name = False
    layers = dict()
    for line in lines:
        # Count the number of words separated by tabs in each line
        cols = line.split('\t')
        # Check if the current line has more words than the previous maximum
        if cols[0] == 'Layer':
            pass_layer_name = True
        if pass_layer_name and is_number_using_builtin_methods(cols[0]):
            layers[cols[0]] = remove_empty_elements_with_list_comprehension(cols)
    return layers



if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1input_excels_dir> <2input_control_file> <3input_one_weather_data_file> <4output_weather_control> <5centroid_geocoordinate>\n")
    sys.exit(0)

if len(sys.argv) > 1:
    arguments = sys.argv[1:]
    #print("Arguments passed:", arguments)
else:
    print("No arguments provided.")


# Open the file in read mode ('r')
control_file = arguments[0] + '/' + arguments[1]
with open(control_file, 'r') as file:
    # Read the entire content of the file
    file_content = file.read()
#print(file_content)

#get location file name:
location_filename = arguments[0] + '/' + get_word_before_multi_word_string(file_content, "Location Worksheet Name") + ".txt"
#print(location_filename)


#getinformation from weather data file
weather = pd.read_csv(arguments[2], sep='\t', header=None)
hourly = False
fourly_format = 0
if len(weather) > 365 or len(weather.columns) == 7:
    hourly = True
    if weather.iloc[:, 0].min() == 0:
        fourly_format = 0
    else:
        if weather.iloc[0, 0] == 1:
            fourly_format = 1
        else:
            fourly_format = 2
            
    
#read location file
with open(location_filename, 'r') as file:
    lines = file.readlines()
    if len(lines) >= 3:
        third_line = lines[2].strip().split('\t')  # Index 2 corresponds to the third line (0-based indexing)
        
        #output weather control
        with open(arguments[3], 'w') as wfile:
            wfile.write('[Num_Stations]\n1\n')
            wfile.write('[station_id]\n1\n')
            wfile.write('[Latitude]\n' + third_line[1] + '\n')
            wfile.write('[Longitude]\n' + third_line[2] + '\n')
            wfile.write('[Altitude]\n' + third_line[3] + '\n')
            wfile.write('[proj_x]\n0\n')
            wfile.write('[proj_y]\n0\n')
            wfile.write('[Screening_Height]\n' + third_line[4] + '\n')
            wfile.write('[Weather_File_Path]\n' + third_line[5] + '\n')
            wfile.write('[Weather_File_Prefix]\n' + third_line[6] + '\n')
            wfile.write('[Time_Step_Hours]\n')
            if hourly == True:
                wfile.write('1\n')
                wfile.write('[Start_Hour_Format] 0:0-23; 1:1-24; 2:24-1-...23\n')
                wfile.write(str(fourly_format) + '\n')
            else:
                wfile.write('24\n')
                wfile.write('[Start_Hour_Format] 0:0-23; 1:1-24; 2:24-1-...23\n0\n')
        #output centroid file
        with open(arguments[4], 'w') as wfile:
            wfile.write('[location]\n')
            wfile.write(f'latitude={third_line[1]}\n')
            wfile.write(f'longitude={third_line[2]}\n')
            wfile.write(f'elevation={third_line[3]}\n')
        
        #print("Third line:", third_line)
    else:
        print("The file has fewer than three lines.")
print(sys.argv[0] + ' Done!')