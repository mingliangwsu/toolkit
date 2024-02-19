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
def get_substring_after_letter(text, letter):
    index = text.find(letter)
    if index != -1:
        return text[index+1:]
    else:
        return None
#______________________________________________________________________________
def get_positions_with_list_comprehension(lst, value):
    positions = [index for index, element in enumerate(lst) if element == value]
    return positions
#______________________________________________________________________________
def is_string_present_in_list(lst, target_string):
    for element in lst:
        if target_string in element:
            return True
    return False
#______________________________________________________________________________
def get_string_present_in_list(lst, target_string):
    for element in lst:
        if target_string in element:
            return element
    return None
#______________________________________________________________________________



if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1input> <2output> <3mode> <4start_year>\n")
    sys.exit(0)


# Open the file in read mode ('r')
with open(sys.argv[1], 'r') as file:
    # Read the entire content of the file
    file_content = file.read()
    file_content = remove_double_quotes_with_string_manipulation(file_content)
#print(file_content)

paramater_values = dict()
paramater_values['fertilization'] = list()
paramater_values['tillage'] = list()
paramater_values['organic_fertilization'] = list()
paramater_values['irrigation'] = list()

with open(sys.argv[1], 'r') as mfile:
    for line in mfile:
        items = line.rstrip().split('\t')
        if 'Management Schedule' in line:
            paramater_values['description'] = get_string_after_substring(line,"Management Schedule - ")
        if 'Standing Stubble Mass Fraction' in line:
            t = get_word_before_multi_word_string(line,'Standing Stubble Mass Fraction')
            if t != None and is_number_using_builtin_methods(t):
                paramater_values['Standing_Stubble_Mass'] = float(t)
        if 'Surface Residue Mass Fraction' in line:
            t = get_word_before_multi_word_string(line,'Surface Residue Mass Fraction')
            if t != None and is_number_using_builtin_methods(t):
                paramater_values['Surface_Residue_Mass_Fraction'] = float(t)
        if 'Fertilization' in items:
            sel = items[:9]
            paramater_values['fertilization'].append(sel)
            #print(sel)
        if 'Irrigation' in items:
            sel = items[:9]
            paramater_values['irrigation'].append(sel)
            #print(sel)
        if 'Pre-plant' in items:
            #print(items)
            position = get_positions_with_list_comprehension(items,'Pre-plant')[0]
            #print(f'position:{position} {endposition}')
            sel = items[position:position + 9]
            paramater_values['tillage'].append(sel)
            #print(sel)
        if is_string_present_in_list(items,'Manure'):
            #print(items)
            manure_name = get_string_present_in_list(items,'Manure')
            position = get_positions_with_list_comprehension(items,manure_name)[0]
            #print(f'position:{position} {endposition}')
            sel = items[position:position + 5]
            if is_number_using_builtin_methods(sel[1]) and is_number_using_builtin_methods(sel[2]): 
                paramater_values['organic_fertilization'].append(sel)
                #print(sel)
            
#get first year
if len(sys.argv) == 5:
    start_year = int(sys.argv[4])
else:
    #Assume the first year is the simulation year
    start_year = 1000000
    for management in ['fertilization','tillage', 'organic_fertilization', 'irrigation']:
        if len(paramater_values[management]) > 0:
            if int(paramater_values[management][0][1]) < start_year:
                start_year = int(paramater_values[management][0][1])
print(f'start_year:{start_year}')


#get the fertilization items and values
mode_data = dict()
mode_data['tillage'] = dict()
mode_data['irrigation'] = dict()
mode_data['fertilization'] = dict()
mode_data['organic_fertilization'] = dict()

with open(sys.argv[3], 'r') as mfile:
    target = ''
    for line in mfile:
        line = line.rstrip()
        if len(line) > 0:
            
            if line[:1] == '[':
                key_index = ''
                if  ':' in line:
                    key = get_substring_before_letter(line,':')[1:]
                    key_index = get_substring_after_letter(line,':')[:-1]
                    target = key
                else:
                    target = ''
            #print(f'{line}:{target}:key_index:{key_index}')

            varkey = ''
            value = ''
            comments = ''
            if '=' in line:
                varkey = get_substring_before_letter(line,'=')
                t = line.split('=')
                if len(t) > 1:
                    value = t[1].split(' ')[0]
                    comments = remove_first_word(line)
                #print(f'{line}#{varkey}#value:{value}#comments:{comments}')
                if target in mode_data and key_index == '1':
                    mode_data[target][varkey] = [value,comments]


#output from mode and new value
with open(sys.argv[2], 'w') as file:
    # Read the entire content of the file
    with open(sys.argv[3], 'r') as mfile:
        target = ''
        for line in mfile:
            line = line.rstrip()
            if len(line) > 0:
                if line[:1] == '[':
                    key_index = ''
                    if  ':' in line:
                        key = get_substring_before_letter(line,':')[1:]
                        key_index = get_substring_after_letter(line,':')[:-1]
                        target = key
                    else:
                        target = ''
                #print(f'{line}:{target}:key_index:{key_index}')
                varkey = ''
                value = ''
                comments = ''
                
                if target == '' or target not in mode_data:
                    if ':count' in line:
                        countkey = get_substring_before_letter(line,':')
                        if countkey not in paramater_values:
                            file.write(line + '\n')
                        else:
                            count = len(paramater_values[countkey])
                            file.write(countkey + ':count=' + str(count) + '\n')
                    else:
                        if "description=" in line and 'description' in paramater_values:
                            file.write('description=' + paramater_values['description'] + '\n')
                        elif 'residue=' in line:
                            comments_residue = remove_first_word(line)
                            file.write('residue=' + str(paramater_values['Surface_Residue_Mass_Fraction'] * 100) + ' ' + comments_residue + '\n')
                        elif 'root_dead=' not in line and 'dead=' in line:
                            comments_residue = remove_first_word(line)
                            file.write('dead=' + str(paramater_values['Standing_Stubble_Mass'] * 100) + ' ' + comments_residue + '\n')
                        else:
                            file.write(line + '\n')
                
     
    for management in ['fertilization','tillage', 'organic_fertilization', 'irrigation']:
        if len(paramater_values[management]) > 0:
            for idx,item in enumerate(paramater_values[management]):
                event_year = int(item[1])
                event_doy = int(item[2])
                relative_date = (event_year - start_year) * 1000 + event_doy
                if management in mode_data:
                    file.write('[' + management + ':' + str(idx+1) + ']' + '\n')
                    for var in mode_data[management]:
                        if var == 'ID':
                            ID = f'{item[1]}{item[2]:03}.{idx}'
                            file.write(var + '=' + ID + '\n')
                        elif var == 'event_date':
                            event_date = f'{relative_date:04}'
                            file.write(var + '=' + event_date + ' (actual date)' + '\n')
                        elif var == 'event_synchronization':
                            file.write(var + '=' + 'actual_date' + '\n')
                        elif var == 'ammonium_source':
                            if item[6] == '1':
                                source = 'urea'
                            elif item[6] == '2':
                                source = 'urea_ammonium_nitrate'
                            else:
                                source = 'ammonium_nitrate'
                            file.write(var + '=' + source + '\n')
                        elif var == 'NH4_appl_method':
                            if item[7] == '1':
                                method = 'surface_broadcast'
                            else:
                                method = 'incorporate'
                            file.write(var + '=' + method + '\n')
                        elif var in ['NO3_N','NO3_amount']:
                            file.write(var + '=' + item[4] + '\n')
                        elif var in ['NH4_N','NH4_amount']:
                            file.write(var + '=' + item[5] + '\n')
                        elif var == 'event_synchronization' and management == 'tillage':
                            if item[0] == 'Pre-plant':
                                file.write(var + '=before_planting' + '\n')
                            else:
                                file.write(var + '=' + mode_data[management][var][0] + ' ' + mode_data[management][var][1] + '\n')
                        elif var == 'dust_mulch_intensity':
                            file.write(var + '=' + item[7] + '\n')
                        elif var == 'dust_mulch_depth':
                            file.write(var + '=' + str(float(item[5]) * 100) + '\n')
                        else:
                            file.write(var + '=' + mode_data[management][var][0] + ' ' + mode_data[management][var][1] + '\n')
                            

print(sys.argv[0] + ' Done!')



