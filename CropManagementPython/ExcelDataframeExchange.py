#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:54:17 2024

@author: liuming
"""
import pandas as pd

def excel_cell_to_indices(cell_reference):
    col_str, row_str = "", ""
    for char in cell_reference:
        if char.isalpha():
            col_str += char.upper()
        elif char.isdigit():
            row_str += char
    col_index = sum((ord(c) - ord('A') + 1) * (26 ** i) for i, c in enumerate(reversed(col_str))) - 1
    row_index = int(row_str) - 1
    return row_index, col_index

def get_excel_value(Cells, cell_reference):
    row_index, col_index = excel_cell_to_indices(cell_reference)
    return Cells.iloc[row_index, col_index]

def set_excel_value(Cells, cell_reference, value):
    row_index, col_index = excel_cell_to_indices(cell_reference)
    Cells.iloc[row_index, col_index] = value
    
def get_cell_float(cellvalue,default = 0.0):
    if not pd.isna(cellvalue):
        return float(cellvalue)
    else:
        return default
    
def get_cell_int(cellvalue,default = 0):
    if not pd.isna(cellvalue):
        return int(cellvalue)
    else:
        return default