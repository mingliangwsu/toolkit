#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:03:07 2023

@author: liuming
"""
import sys 
import re
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
    print("Usage:" + sys.argv[0] + "<1input_excels_dir> <2input_control_file> <3hourly?:0 or 1> <4start_hour_format 0:0-23; 1:1-24; 2:24-1-...23> <5output_weather_control>\n")
    sys.exit(0)

# Open the file in read mode ('r')
control_file = sys.argv[1] + '/' + sys.argv[2]
with open(control_file, 'r') as file:
    # Read the entire content of the file
    file_content = file.read()
#print(file_content)

#get location file name:
location_filename = sys.argv[1] + '/' + get_word_before_multi_word_string(file_content, "Location Worksheet Name") + ".txt"
print(location_filename)

#read location file
with open(location_filename, 'r') as file:
    lines = file.readlines()
    if len(lines) >= 3:
        third_line = lines[2].strip().split('\t')  # Index 2 corresponds to the third line (0-based indexing)
        
        #output weather control
        
        with open(sys.argv[5], 'w') as wfile:
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
            if sys.argv[3] == '1':
                wfile.write('1\n')
                wfile.write('[Start_Hour_Format] 0:0-23; 1:1-24; 2:24-1-...23\n')
                wfile.write(sys.argv[4] + '\n')
            else:
                wfile.write('24\n')
                wfile.write('[Start_Hour_Format] 0:0-23; 1:1-24; 2:24-1-...23\n0\n')
                
        
        print("Third line:", third_line)
    else:
        print("The file has fewer than three lines.")
"""
soil_values = dict()

#Soil_Profile_Num_Layers
target_string = "Number of soil layers"
soil_values['Soil_Profile_Num_Layers'] = int(get_word_before_multi_word_string(file_content, target_string))
print(f"{target_string}:{soil_values['Soil_Profile_Num_Layers']}")

#Soil_Profile_Bypass
target_string = "Bypass Coefficient"
soil_values['Soil_Profile_Bypass'] = float(get_word_before_multi_word_string(file_content, target_string))
print(f"{target_string}:{soil_values['Soil_Profile_Bypass']}")

#Soil_Profile_Control_Chemical
target_string = "Control layer for Chemical"
soil_values['Soil_Profile_Control_Chemical'] = int(get_word_before_multi_word_string(file_content, target_string))
print(f"{target_string}:{soil_values['Soil_Profile_Control_Chemical']}")

#SCS_CN_Soil_Adjust
target_string = "Bare Soil CN Adjustment Factor"
soil_values['SCS_CN_Soil_Adjust'] = int(get_word_after_multi_word_string(file_content, target_string))
print(f"{target_string}:{soil_values['SCS_CN_Soil_Adjust']}")

#SCS_CN_Residue_Adjust
target_string = "Residue Cover CN Adjustment Factor"
soil_values['SCS_CN_Residue_Adjust'] = int(get_word_after_multi_word_string(file_content, target_string))
print(f"{target_string}:{soil_values['SCS_CN_Residue_Adjust']}")

#SCS_CN_Hydro_Group
target_string = "Hydrologic Group"
soil_values['SCS_CN_Hydro_Group'] = get_word_after_multi_word_string(file_content, target_string)
print(f"{target_string}:{soil_values['SCS_CN_Hydro_Group']}")

#Initial_Standing_Stubble
target_string = "Initial Standing Stubble"
soil_values['Initial_Standing_Stubble'] = float(get_word_after_multi_word_string(file_content, target_string)) * 0.0001  #from kg/ha -> kg/m2
print(f"{target_string}:{soil_values['Initial_Standing_Stubble']}")

#Initial_Standing_Stubble_Type
position = find_position_after_string(file_content,target_string)
#print(f"{target_string}:{position}")
soil_values['Initial_Standing_Stubble_Type'] = get_second_word_after_position(file_content, position)
print(f"Initial_Standing_Stubble_Type:{soil_values['Initial_Standing_Stubble_Type']}")


#Initial_Surface_Residue
target_string = "Initial Surface Residue"
soil_values['Initial_Surface_Residue'] = float(get_word_after_multi_word_string(file_content, target_string)) * 0.0001  #from kg/ha -> kg/m2
print(f"{target_string}:{soil_values['Initial_Surface_Residue']}")

#Initial_Surface_Residue_Type
position = find_position_after_string(file_content,target_string)
#print(f"{target_string}:{position}")
soil_values['Initial_Surface_Residue_Type'] = get_second_word_after_position(file_content, position)
print(f"Initial_Surface_Residue_Type:{soil_values['Initial_Surface_Residue_Type']}")

#Initial_Soil_Root_Residues
target_string = "Initial Soil Root Residues"
amount_str = get_word_after_multi_word_string(file_content, target_string)
if amount_str == 'Amounts':
    soil_values['Initial_Soil_Root_Residues'] = 0
    soil_values['Initial_Soil_Root_Residues_Type'] = get_word_after_multi_word_string(file_content, "Amounts by Layer")
else:
    soil_values['Initial_Soil_Root_Residues'] = float(amount_str) * 0.0001  #from kg/ha -> kg/m2
    position = find_position_after_string(file_content,target_string)
    soil_values['Initial_Soil_Root_Residues_Type'] = get_second_word_after_position(file_content, position)
print(f"{target_string}:{soil_values['Initial_Soil_Root_Residues']}\nInitial_Soil_Root_Residues_Type:{soil_values['Initial_Soil_Root_Residues_Type']}")

#Get soil layers infomation
soil_layers = get_first_layer(file_content)
#print(f"layer1:{soil_layers}")

soil_values['Water_Table_At_Layer'] = int(soil_layers['1'][-6])
soil_values['WT_Solute_Conc'] = float(soil_layers['1'][-5])
free_drain = soil_layers['1'][-4]
if free_drain == 'TRUE':
    soil_values['Free_Drainage'] = True
else:
    soil_values['Free_Drainage'] = False
soil_values['Surface_Water_Store'] = float(soil_layers['1'][-3])
soil_values['Manning_Coef'] = float(soil_layers['1'][-2])
soil_values['Percentage_of_surface_water_still_in_cell'] = float(soil_layers['1'][-1])
#TODO later!
soil_values['Max_Number_Of_Layer_Pot_Explored_By_Roots'] = soil_values['Soil_Profile_Num_Layers']

#remove extra columns
soil_layers['1'] = soil_layers['1'][:-6]
#print(soil_layers['1'])

#Generate output soil file
# Open the file in read mode ('r')
with open(sys.argv[2], 'w') as file:
    # Read the entire content of the file
    file.write('[Soil_Profile_Num_Layers]\n')
    outstr = str(soil_values['Soil_Profile_Num_Layers']) + '\n'
    file.write(outstr)
    
    file.write('[Soil_Profile_Bypass]\n')
    outstr = str(soil_values['Soil_Profile_Bypass']) + '\n'
    file.write(outstr)
    
    file.write('[Soil_Profile_Control_Chemical]\n')
    outstr = str(soil_values['Soil_Profile_Control_Chemical']) + '\n'
    file.write(outstr)
    
    file.write('[SCS_CN_Soil_Adjust]\n')
    outstr = str(soil_values['SCS_CN_Soil_Adjust']) + '\n'
    file.write(outstr)
    
    file.write('[SCS_CN_Residue_Adjust]\n')
    outstr = str(soil_values['SCS_CN_Residue_Adjust']) + '\n'
    file.write(outstr)
    
    file.write('[SCS_CN_Hydro_Group]\n')
    outstr = str(soil_values['SCS_CN_Hydro_Group']) + '\n'
    file.write(outstr)
    
    file.write('[Initial_Residue]\n')
    outstr = 'Initial_Standing_Stubble\t' + str(soil_values['Initial_Standing_Stubble']) + '\t' + soil_values['Initial_Standing_Stubble_Type'] + '\n'
    file.write(outstr)
    
    file.write('[Initial_Residue]\n')
    outstr = 'Initial_Surface_Residue\t' + str(soil_values['Initial_Surface_Residue']) + '\t' + soil_values['Initial_Surface_Residue_Type'] + '\n'
    file.write(outstr)
    
    file.write('[Initial_Residue]\n')
    #may missed one parameter after the residue type
    outstr = 'Initial_Soil_Root_Residues\t' + str(soil_values['Initial_Soil_Root_Residues']) + '\t' + soil_values['Initial_Soil_Root_Residues_Type'] + '\n'
    file.write(outstr)
    
    file.write('[Water_Table_At_Layer]\n')
    outstr = str(soil_values['Water_Table_At_Layer']) + '\n'
    file.write(outstr)
    
    file.write('[WT_Solute_Conc]\n')
    outstr = str(soil_values['WT_Solute_Conc']) + '\n'
    file.write(outstr)
    
    file.write('[Free_Drainage]\n')
    if soil_values['Free_Drainage']:
        outstr = '1\n'
    else:
        outstr = '0\n'
    file.write(outstr)
    
    file.write('[Surface_Water_Store]\n')
    outstr = str(soil_values['Surface_Water_Store']) + '\n'
    file.write(outstr)
    
    file.write('[Manning_Coef]\n')
    outstr = str(soil_values['Manning_Coef']) + '\n'
    file.write(outstr)
    
    file.write('[Max_Number_Of_Layer_Pot_Explored_By_Roots]\n')
    outstr = str(soil_values['Max_Number_Of_Layer_Pot_Explored_By_Roots']) + '\n'
    file.write(outstr)
    
    file.write('[Layers]\n')
    
    for layer in soil_layers:
        for index,col in enumerate(soil_layers[layer]):
            if index < len(soil_layers[layer]) - 1:
                file.write(col + '\t')
            else:
                file.write(col + '\n')
print('Done!')
    
"""  
    