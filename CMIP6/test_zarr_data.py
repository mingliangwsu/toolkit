#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 14:47:33 2024

@author: liuming
"""
import xarray as xr

ds = xr.open_zarr('/home/liuming/mnt/hydronas3/Projects/WDFW_Culvert2024_2025/Data/RMJOC-1/0',consolidated=True)
print(ds)