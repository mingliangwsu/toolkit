#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 16:15:16 2020

@author: liuming
"""

# Standard-ish packages
import requests
import re
import numpy as np
import urllib
import io
import matplotlib.pyplot as plt
import pandas as pd

# Less standard, but all of the following are pip- or conda-installable
import rasterio

# pip install azure-storage-blob
from azure.storage.blob import ContainerClient

from osgeo import gdal,osr

# Storage locations are documented at http://aka.ms/ai4edata-hls
hls_container_name = 'hls'
hls_account_name = 'hlssa'
hls_account_url = 'https://' + hls_account_name + '.blob.core.windows.net/'
hls_blob_root = hls_account_url + hls_container_name

# This file is provided by NASA; it indicates the lat/lon extents of each
# hls tile.
#
# The file originally comes from:
#
# https://hls.gsfc.nasa.gov/wp-content/uploads/2016/10/S2_TilingSystem2-1.txt
#
# ...but as of 8/2019, there is a bug with the column names in the original file, so we
# access a copy with corrected column names.
hls_tile_extents_url = 'https://ai4edatasetspublicassets.blob.core.windows.net/assets/S2_TilingSystem2-1.txt?st=2019-08-23T03%3A25%3A57Z&se=2028-08-24T03%3A25%3A00Z&sp=rl&sv=2018-03-28&sr=b&sig=KHNZHIJuVG2KqwpnlsJ8truIT5saih8KrVj3f45ABKY%3D'

# Load this file into a table, where each row is:
#
# Tile ID, Xstart, Ystart, UZ, EPSG, MinLon, MaxLon, MinLon, MaxLon
print('Reading tile extents...')
s = requests.get(hls_tile_extents_url).content
hls_tile_extents = pd.read_csv(io.StringIO(s.decode('utf-8')),delimiter=r'\s+')
print('Read tile extents for {} tiles'.format(len(hls_tile_extents)))

# Read-only shared access signature (SAS) URL for the hls container
hls_sas_token = 'st=2019-08-07T14%3A54%3A43Z&se=2050-08-08T14%3A54%3A00Z&sp=rl&sv=2018-03-28&sr=c&sig=EYNJCexDl5yxb1TxNH%2FzILznc3TiAnJq%2FPvCumkuV5U%3D'

hls_container_client = ContainerClient(account_url=hls_account_url, 
                                         container_name=hls_container_name,
                                         credential=None)
                                

#%matplotlib inline