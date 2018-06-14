#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 14:35:09 2018

@author: liuming
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 08:50:46 2018
Convert excel annual daily averaged VIC-CropSyst (hydro- and 
irrigation-related variables)


@author: liuming
"""

import pandas as pd
import os
import glob
from pyGDsandbox.dataIO import df2dbf, dbf2df

indir = "/home/liuming/data/BPA_output/crop4001"
outdir = "/home/liuming/data/BPA_output/crop4001_processed"
output_file = "irrigation_annual_daymean.csv"
os.chdir(indir)

crop_name = ['corn_grain-irrigated','potato-irrigated','wheat_winter-irrigated']


#cell_avgdata = {}
#cell_anntotaldata = {}

#region_avgdata = {}
#for crop in crop_name:
    #region_avgdata[crop] = avgdata[crop].groupby(region_key,as_index=False)[sum_list].mean()
    #region_avgdata[crop].to_csv(outdir + '/region_mean' + crop + '.csv',index = False)
    
    
for crop in crop_name:
    #cell_avgdata[crop] = avgdata[crop].groupby(cell_key,as_index=False)[sum_list].mean()
    #cell_avgdata[crop].to_csv(outdir + '/cellmap_mon_mean' + crop + '.csv',index = False)
    #cell_anntotaldata[crop] = cell_avgdata[crop].groupby(cell_ann_key,as_index=False)[sum_list].sum()
    #cell_anntotaldata[crop].to_csv(outdir + '/cellmap_annual' + crop + '.csv',index = False)
    df2dbf(cell_anntotaldata[crop],outdir + "/cellmapann.dbf")