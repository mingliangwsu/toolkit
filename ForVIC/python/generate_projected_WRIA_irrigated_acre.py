import pandas as pd
import pysal as ps
import numpy as np

def sortkey(x): 
    return int(x)

datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/Landuse/"
projlanduse_filename = datapath + "irrig2018_WRIA_croptype_irrigated.txt"
out_filename = datapath + "Forecast_and_baseline_WRIA_irrigated_croptype_acre.txt"
gencroptype_filename = datapath + "GeneralCro_CropType.txt"

other_fruit = ["Apricot","Berry, Unknown","Caneberry","Cranberry","Currant","Kiwi", "Grape, Juice","Grape, Table","Grape, Unknown","Pear"]
change_rate = {
    "other_fruit" : -0.2316,
    "Hay/Silage" : 0.0028,
    "Cereal Grain" : 0.0695,
    "Vegetable" : 0.003,
    "Apple" : 0.0982,
    "Cherry" : 0.1704,
    "Grape, Wine" : 0.1546,
    "Blueberry" : 1.6983,
    "Hops" : -0.2687
        }
total_irrig_baseline = dict()
total_unchanged_baseline = dict()
total_forecast = dict()
total_adj_crop_list = dict()

change_rate_unadjusted_crop = dict()

#read combined infomation
with open(out_filename, "w") as outf:
    outhead = "WRIA_NR\tWRIA_NM\tGeneralCro\tCropType\tbaseline_totAcre\tForecast2040_Acre\n"
    outf.write(outhead)
    #First round
    with open(projlanduse_filename,"r") as f:
        for line in f:
            a = line.rstrip().split('\t')
            if len(a) > 1 and "WRIA_NR" not in a:
                WRIA_ID = int(float(a[0]))
                WRIA_NM = a[1]
                gencrop = a[2]
                crop = a[3]
                baseline = float(a[4])
                rate = 0.0
                
                if WRIA_ID not in total_irrig_baseline:
                    total_irrig_baseline[WRIA_ID] = 0.0
                total_irrig_baseline[WRIA_ID] += baseline
                if WRIA_ID not in total_forecast:
                    total_forecast[WRIA_ID] = 0.0
                if WRIA_ID not in total_unchanged_baseline:
                    total_unchanged_baseline[WRIA_ID] = 0.0
                    
                if crop in change_rate:
                    rate = change_rate[crop]
                elif crop in other_fruit:
                    rate = change_rate["other_fruit"]
                elif gencrop in other_fruit:
                    rate = change_rate["other_fruit"]
                elif gencrop in change_rate:
                    rate = change_rate[gencrop]
                    
                if WRIA_ID not in total_adj_crop_list:
                    total_adj_crop_list[WRIA_ID] = list()

                if abs(rate) >= 0.0001:
                    total_adj_crop_list[WRIA_ID].append(crop)
                else:
                    total_unchanged_baseline[WRIA_ID] += baseline
                    
                print(crop + ":" + str(rate))
                forecast = baseline * (1.0 + rate)
                total_forecast[WRIA_ID] += forecast
                
                #outrecord = str(WRIA_ID) + "\t" + WRIA_NM + "\t" + gencrop + "\t" + crop + "\t" + str('%.2f' % baseline) + "\t" + str('%.2f' % forecast)  + "\n"
                #outf.write(outrecord)
    print("Reading Done!\n")
    
    #check balance
    for wria in total_irrig_baseline:
        total_unchanged_should_change = total_irrig_baseline[wria] - total_forecast[wria]
        rate = 0.0
        if total_unchanged_baseline[wria] >= 0.01:
            rate = total_unchanged_should_change / total_unchanged_baseline[wria]
        if rate < -1.0:
            rate = -1.0
        if wria not in change_rate_unadjusted_crop:
            change_rate_unadjusted_crop[wria] = rate
        print(str(wria) + " baseline:" + str(total_irrig_baseline[wria]) + " Forecast:" + str('%.2f' % total_forecast[wria]) + " other_rate:" + str('%.4f' % rate))
    #repeat with new rate
    with open(projlanduse_filename,"r") as f:
        for line in f:
            a = line.rstrip().split('\t')
            if len(a) > 1 and "WRIA_NR" not in a:
                WRIA_ID = int(float(a[0]))
                WRIA_NM = a[1]
                gencrop = a[2]
                crop = a[3]
                baseline = float(a[4])
                rate = 0.0
                
                if crop in change_rate:
                    rate = change_rate[crop]
                elif crop in other_fruit:
                    rate = change_rate["other_fruit"]
                elif gencrop in other_fruit:
                    rate = change_rate["other_fruit"]
                elif gencrop in change_rate:
                    rate = change_rate[gencrop]
                elif crop not in total_adj_crop_list[WRIA_ID]:
                    rate = change_rate_unadjusted_crop[WRIA_ID]
                    
                #print(crop + ":" + str(rate))
                forecast = baseline * (1.0 + rate)
                total_forecast[WRIA_ID] += forecast
                
                outrecord = str(WRIA_ID) + "\t" + WRIA_NM + "\t" + gencrop + "\t" + crop + "\t" + str('%.2f' % baseline) + "\t" + str('%.2f' % forecast)  + "\n"
                outf.write(outrecord)
    print("Reading Done!\n")
print("Done!\n")
