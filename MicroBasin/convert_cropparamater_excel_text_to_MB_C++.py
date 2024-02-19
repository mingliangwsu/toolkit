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
    escaped_target = re.escape(target_string)
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
def remove_double_quotes_with_string_manipulation(s):
    return s.replace('"', '')
#______________________________________________________________________________
def remove_first_word(sentence):
    # Split the sentence into words
    words = sentence.split()
    # Join the words starting from the second word
    new_sentence = ' '.join(words[1:])
    return new_sentence
#______________________________________________________________________________
def get_string_after_substring(text, substring):
    first_line = text.split('\n', 1)[0]
    return first_line.split(substring, 1)[-1].replace('\t', '')
#______________________________________________________________________________
def get_substring_before_letter(text, letter):
    index = text.find(letter)
    if index != -1:
        return text[:index]
    else:
        return None
#______________________________________________________________________________


if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1input> <2output> <3mode>\n")
    sys.exit(0)


# Open the file in read mode ('r')
with open(sys.argv[1], 'r') as file:
    # Read the entire content of the file
    file_content = file.read()
    file_content = remove_double_quotes_with_string_manipulation(file_content)
#print(file_content)

crop_paramater_values = dict()

excel_crop_match = {
    #crop growth
    'Radiation-Use Efficiency': 'RUE_PAR',
    'Water-Use Efficiency at 1 kPa': 'TUE_at_1pKa_VPD',
    # not used
    'Slope of Water-Use Efficiency Function of VPD': 'Slope_of_WUE',
    'Optimum Mean Daily Temperature for Growth': 'optimal_temp',

    # Morphology
    'Initial Canopy Ground Cover': 'CC_initial',
    'Maximum Canopy Ground Cover': 'CC_maximum',
    # not used
    'Green Canopy Ground Cover at Maturity': 'Green_Canopy_Ground_Cover_at Maturity',
    'Total Canopy Ground Cover  at Maturity': 'CC_mature_total',
    'Maximum Crop Height': 'max_canopy_height',
    'Leaf Water Potential That Begin Reducing Canopy Expansion': 'LWP_reduces_canopy_expansion',
    'Leaf Water Potential That Stops Canopy Expansion': 'LWP_stops_canopy_expansion',
    'Maximum Rooting Depth': 'max_root_depth',
    'Maximum Surface Root Density': 'surface_root_density',
    'Curvature of Root Density Distribution': 'root_density_distribution_curvature',
    'Root Length Per Unit Root Mass': 'root_length_per_unit_mass',
    'Root Growth Sensitivity to Stress': 'root_sensitivity_water_stress',

    # Crop Development
    'Base Temperature for Development': 'base_temp',
    'Maximum Temperature for Development': 'maximum_temp',
    'Thermal Time at Emergence or  budbreak': 'emergence',
    # not used
    'Thermal time for budbreak if chill requirements not satisfied': 'Thermal_chill',
    'Thermal Time at Flowering': 'flowering',
    'Thermal Time at the Beginning of Grain Filling': 'filling',
    'Thermal Time at the End of Canopy Growth': 'peak_LAI',
    'Thermal Time at the Beginning of Canopy Senescence': 'senescence',
    'Thermal Time at Physiological Maturity or Crop Harvestable': 'maturity',

    # Plant-Water Relations
    'Crop ET Coefficient assuming full ground shading': 'ET_crop_coef',
    'Maximum Water Uptake': 'max_water_uptake',
    'Leaf Water Potential at the Onset of Stomatal Closure': 'stomatal_closure_leaf_water_pot',
    'Wilting Leaf Water Potential': 'wilt_leaf_water_pot',

    # Plant-Nitrogen Relations
    'Maximum Nitrogen Uptake during rapid linear growth': 'max_uptake_daily_rate',
    'Plant Available Water at which N Uptake Limitation Begins': 'PAW_where_N_uptake_rate_decreases',
    'Soil N Concentration at which N Uptake Limitation Begins': 'soil_N_conc_where_N_uptake_decreases',
    'Residual Soil N Not Available For Uptake': 'residual_N_not_available_for_uptake',
    'Standard Root Nitrogen Concentration': 'root_conc',
    # not used
    'Grain Nitrogen Coefficient': 'Grain_Nitrogen_Coefficient',

    # Harvest
    'Unstressed Harvest Index': 'unstressed',
    'Maximum Fraction of Carbon Translocated to Grains': 'translocation_max',

    # Tree-Fruit Crops Only
    'Fresh Mass Fruit Load': 'max_fruit_load',
    'Fraction of Solids in Fruits': 'fract_total_solids',

    # Perennial Crops
    # Need double-check
    'Day of the Year to Start Searching for Beginning of Dormancy': 'start_valid_date',
    'Day of the Year to Start Searching for End of Dormancy': 'end_valid_date',

    # Initialization
    'Root depth at emergence': 'initial_depth',
    # not used
    'Planting depth': 'Planting_depth',

    # Type of crop
    # Use this to initialize photosynthetic_pathway
    'Is this a C3 crop': 'C_species',
    'Is this a perennial crop': 'life_cycle',
    # not used
    'Is this a root crop': 'root_crop',
    'Is this a tree-fruit crop': 'fruit_crop',
    # not used
    'Is this a grain crop': 'grain_crop',
    # double check
    'Is this a vegetable crop': 'vegetatble_crop',
    'Is this a leguminous': 'fixation',

    # Crop Response to Elevated Atmospheric Carbon Dioxide
    # double check
    'Baseline CO2 Concentration' : 'TUE_reference_conc',
    # double check
    'Elevated CO2 Concentration' : 'RUE_reference_conc',
    'Biomass Gain Ratio due to CO2 Increase in the experiment' : 'growth_ratio_asymptotic',

    # Maintenance Respiration - Biosynthesis efficiency
    # Not used
    'Maintenance Coef Leaves': 'Maintenance_Coef_Leaves',
    'Maintenance Coef Stems': 'Maintenance_Coef_Stems',
    'Maintenance Coef Roots': 'Maintenance_Coef_Roots',
    'Biosynthesis efficiency Leaves': 'Biosynthesis_efficiency_Leaves',
    'Biosynthesis efficiency Stems': 'Biosynthesis_efficiency_Stems',
    'Biosynthesis efficiency Roots': 'Biosynthesis_efficiency_Roots'
}

#harvested_part:  "grain" "root" "tuber" "bulb" "leaf" "fruit" 
#model: "crop" "fruit"
#stem_type:  "herbaceous" "woody"

for item in excel_crop_match:
    cs_item = excel_crop_match[item]
    value = get_word_before_multi_word_string(file_content, item)
    if value != None:
        if cs_item == 'C_species':
            if value == 'TRUE':
                value = 'C3'
            else:
                value = 'C4'
        elif cs_item in ['start_valid_date','end_valid_date']:
            if not is_number_using_builtin_methods(value):
                value = '365'
        elif cs_item == 'fixation':
            if value == 'FALSE':
                value = 'false'
            else:
                value = 'true'
        elif cs_item == 'life_cycle':
            if value == 'FALSE':
                value = 'annual'
            else:
                value = 'perennial'
        elif cs_item == 'grain_crop':
            if value == 'TRUE':
                crop_paramater_values['harvested_part'] = 'seed'
        elif cs_item == 'vegetatble_crop':
            if value == 'TRUE':
                crop_paramater_values['harvested_part'] = 'leaf'
        elif cs_item == 'root_crop':
            if value == 'TRUE':
                crop_paramater_values['harvested_part'] = 'root'
        elif cs_item == 'fruit_crop':
            if value == 'TRUE':
                crop_paramater_values['harvested_part'] = 'fruit'
                crop_paramater_values['model'] = 'fruit'
            else:
                crop_paramater_values['model'] = 'crop'
        elif cs_item == 'Thermal_chill':
            if not is_number_using_builtin_methods(value):
                value = None
        elif cs_item == 'max_fruit_load':
            if not is_number_using_builtin_methods(value):
                value = None
            
    #print(f'{item}:{value}')
    crop_paramater_values[cs_item] = value 
    
crop_paramater_values['description'] = get_string_after_substring(file_content,"Crop Input Parameters - ")
        

#output from mode and new value
with open(sys.argv[2], 'w') as file:
    # Read the entire content of the file
    with open(sys.argv[3], 'r') as mfile:
        for line in mfile:
            if len(line) > 0:
                if line[:1] != '[':
                    key = get_substring_before_letter(line,'=')
                    #print(f'{line}:{key}')
                    if key in crop_paramater_values:
                        #print(f'{line}:{key}:{crop_paramater_values[key]}')
                        if crop_paramater_values[key] != None:
                            if key == 'description':
                                comments = ''
                            else:
                                comments = remove_first_word(line)
                            outline = key + '=' + crop_paramater_values[key] + " " + comments + '\n'
                            #print(f'{line}:{key}:{crop_paramater_values[key]}')
                        else:
                            outline = line
                    else:
                        outline = line
                else:
                    outline = line
                file.write(outline)


print('Done!')
    
    
