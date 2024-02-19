#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:03:07 2023
The soil file from excel table is complex and need elevation input as mode
@author: liuming
"""
import sys 
import re
import pandas as pd
import csv
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
    print("Usage:" + sys.argv[0] + "<1input> <2output> <3cell_size> <4xll_corner> <5yll_corner> <6nodata_value> <7raw_elev_model_all_data> <8Rotation_index_file> <9Rotation_file_prefix>\n")
    sys.exit(0)

# Open the file in read mode ('r')
with open(sys.argv[1], 'r') as file:
    # Read the entire content of the file
    #print('Reading ' + sys.argv[1])
    file_content_soil = file.read()
rows_soil = get_rows_all(file_content_soil)
#print(file_content)

#mode to get raster infomation
with open(sys.argv[7], 'r') as file:
    # Read the entire content of the file
    file_content = file.read()
rows = get_rows(file_content)
#print(rows)

rot = pd.read_csv(sys.argv[1],sep='\t',header=(0))
rot = rot.dropna(subset=['Crop1'])
#grid id list
gridids = rot.iloc[:,0].tolist()
#get rotation combination
#get years in rotation
year_rot = int((rot.shape[1] - 2)/3)

#combination col list
cols_key = list()

plant_years_cols = list()
crop_manage_list = list()

for col_idx in range(1,year_rot+1):
    cols_key.append(f'Crop{col_idx}')    
    cols_key.append(f'Management{col_idx}')
    cols_key.append(f'Planting Year_DOY{col_idx}')
    
    crop_manage_list.append(f'Crop{col_idx}')
    crop_manage_list.append(f'Management{col_idx}')
    
    plant_years_cols.append(f'Planting Year_DOY{col_idx}')

#get unique combinations on rotation
t = rot[cols_key].drop_duplicates().sort_values(['Crop1', 'Management1'])
t['Rot_Index'] = t.reset_index().index + 1
t.to_csv(sys.argv[8],sep='\t',index=False)



#updated rotation with index
rot_with_idx = pd.merge(rot, t,  how='left', left_on=cols_key, right_on = cols_key)
rot_with_idx = rot_with_idx.dropna(subset=['Grid_ID'])




#get earliest year
"""
years_list = rot_with_idx[plant_years_cols].values.flatten().tolist()
min_year = 9999
for year_doy in years_list:
    year = int(year_doy[:4])
    if year < min_year:
        min_year = year
"""

crops = list()
managements = list()

delimiter = '-'  # The character you want to use as a delimiter

for index, row in rot_with_idx.iterrows():   
    rot_id = row['Rot_Index']
    rot_filename = f'{sys.argv[9]}_{rot_id}.rot'
    crops_name = delimiter.join(row[crop_manage_list].values.flatten().tolist())
    

    
    with open(rot_filename, 'w') as file:
        start_year = int(row['Planting Year_DOY1'][:4])
        file.write('[rotation]\n')
        file.write(f'description={crops_name}')
        file.write(f'years={year_rot}\n')
        file.write(f'sowing:count={year_rot}\n')
        file.write('[version]\n')
        file.write('major=4\n')
        for col_idx in range(1,year_rot+1):
            year = int(row[f'Planting Year_DOY{col_idx}'][:4])
            doy = int(row[f'Planting Year_DOY{col_idx}'][5:])
            #print(f'{year}_{doy}')
            file.write(f'[sowing:{col_idx}]\n')
            id = row[f'Crop{col_idx}'] + '-' + row[f'Management{col_idx}']
            #print(f'{id}')
            file.write(f'ID={id}\n')
            file.write(f'event_synchronization=relative_date\n')
            rel_year = year - start_year
            
            file.write(f'event_date={(rel_year * 1000 + doy):04} (relative date)\n')
            file.write(f'enabled=true\n')
            file.write(f'description={id}\n')
            crop = row[f'Crop{col_idx}']
            file.write(f'crop=../Crop/{crop}.crp\n')
            management = row[f'Management{col_idx}']
            file.write(f'management=../Management/{management}.mgt\n')
            
            if row[f'Crop{col_idx}'] not in crops:
                crops.append(row[f'Crop{col_idx}'])
            if row[f'Management{col_idx}'] not in managements:
                managements.append(row[f'Management{col_idx}'])
        
#Generate rotation parameter files
# Open the file in read mode ('r')

#Generate ESRI format rotation raster ascii file
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
    
    #for each row
    for row,layer in enumerate(rows):
        for index,col in enumerate(rows[layer]):
            gridid = f'{row + 1}_{index + 1}'
            #print(gridid)
            
            
            if gridid not in gridids:
                out = sys.argv[6]
            else:
                #print(rot_with_idx.loc[rot_with_idx['Grid_ID'] == gridid]['Rot_Index'].values[0])
                out = str(rot_with_idx.loc[rot_with_idx['Grid_ID'] == gridid]['Rot_Index'].values[0])

            if index < len(rows[layer]) - 1:
                file.write(out + ' ')
            else:
                file.write(out + '\n')
            
            
# Append the list of values to the existing CSV file
with open(sys.argv[8], 'a', newline='') as csv_file:
    #csv_writer = csv.writer(csv_file)
    csv_file.write(f'\nCrop list ({len(crops)}):\n')
    for crop in crops:
        csv_file.write(crop + "\n")
    csv_file.write(f'\nManagement list ({len(managements)}):\n')
    for manage in managements:
        csv_file.write(manage + "\n")
print(sys.argv[0] + ' Done!')
 

    