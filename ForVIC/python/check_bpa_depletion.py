#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:52:40 2017
Convert VIC veg parametgers into tables with grid cell id and veg type as index
@author: liuming
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

outdir = "/mnt/nas2/Projects/users/liuming/BPA/FoldertoSendBPA"

watersheds = ["JDP","UMP","UMR","UMW"]
#watersheds = ["JDP"]
#watersheds = ["UMP"]
#watersheds = ["UMR"]
#watersheds = ["UMW"]

datalist = ["Acres200Updated", "Acres211Updated", "Acres235Updated", "Acres260Updated", "BPA2010", 
            "CWDandDivEffandSWGWSplitandAcres211Updated","CWDandDivEffandSWGWSplitUpdated","CWDandDivEffUpdated",
            "CWDUpdated","DivEffUpdated","SWGWSplitAllyearUpdated","SWGWSplitOnly2008Updated"]

#datalist = ["Acres200Updated"]


color_list = {
        "Acres200Updated" : "#ccffcc",
        "Acres211Updated" : "#66ff66",
        "Acres235Updated" : "#00ff00",
        "Acres260Updated" : "#009900",
        "BPA2010" : "#000000", 
        "CWDandDivEffandSWGWSplitandAcres211Updated" : "#ffc6b3",
        "CWDandDivEffandSWGWSplitUpdated" : "#ff6633",
        "CWDandDivEffUpdated" :  "#cc3300",
        "CWDUpdated" :  "#661a00",
        "DivEffUpdated" : "#990073",
        "SWGWSplitAllyearUpdated" : "#ff66ff",
        "SWGWSplitOnly2008Updated" : "#660066"
        }

line_width = {
        "Acres200Updated" : 1,
        "Acres211Updated" : 1,
        "Acres235Updated" : 1,
        "Acres260Updated" : 1,
        "BPA2010" : 3, 
        "CWDandDivEffandSWGWSplitandAcres211Updated" : 2,
        "CWDandDivEffandSWGWSplitUpdated" : 2,
        "CWDandDivEffUpdated" :  1,
        "CWDUpdated" :  1,
        "DivEffUpdated" : 1,
        "SWGWSplitAllyearUpdated" : 2,
        "SWGWSplitOnly2008Updated" : 2
        }

line_style = {
        "Acres200Updated" : "-",
        "Acres211Updated" : "-",
        "Acres235Updated" : "-",
        "Acres260Updated" : "-",
        "BPA2010" : "-", 
        "CWDandDivEffandSWGWSplitandAcres211Updated" : ":",
        "CWDandDivEffandSWGWSplitUpdated" : "-.",
        "CWDandDivEffUpdated" :  "-",
        "CWDUpdated" :  "-",
        "DivEffUpdated" : ":",
        "SWGWSplitAllyearUpdated" : ":",
        "SWGWSplitOnly2008Updated" : "-"
        }





os.chdir(outdir)

for watershed in watersheds:
    fig, ax = plt.subplots()
    for data in datalist:
        print(watershed + "#" + data)
        filename = outdir + "/" + watershed + "5D" + "/" + data
        depletion = pd.read_csv(filename,sep=',',encoding='utf-8-sig')
        
        depletion['DateTime'] = pd.to_datetime(depletion['Date'])
        depletion['Year'] = pd.DatetimeIndex(depletion['DateTime']).year
        
        #depletion.set_index('DateTime', inplace=True)
        #depletion = depletion.resample('1M').mean()
        value = depletion[data]
        x = depletion["DateTime"]
        plt.rcParams["figure.figsize"] = [12,6.75]
        
        temp = depletion.groupby('Year')[['Year',data]].mean()
        sy = temp.loc[(temp['Year'] >= 1929) & (temp['Year'] <= 2007)]
        ax.set_ylabel('Annual average irrigation depletion adjustment (cfs)', size = 12)
        ax.plot(sy['Year'],sy[data], color=color_list[data], linewidth = line_width[data], linestyle = line_style[data], label=data)
    legend = ax.legend(loc='upper center', shadow=True, fontsize='large',bbox_to_anchor=(0.5, -0.05),ncol=2)
    legend.get_frame().set_facecolor('#FFFFFF')
    plt.savefig('/home/liuming/temp/' + watershed + '.png',bbox_extra_artists=(legend,), bbox_inches='tight',dpi=300)
print("done")