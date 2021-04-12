#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 09:12:25 2020
Read dbf file (converted from ESRI Grid combined VAT info) which contains the VIC ID, 
land cover type (including crops), and irrigation (0 or 1) at 30 meter resolution

US & Canada with different land cover maps

Output: csv file with columns
VIC_ID, crop, fraction

crop > 10000 is dry crops

@author: liuming
"""

# this block of code copied from https://gist.github.com/ryan-hill/f90b1c68f60d12baea81 
import pandas as pd
import pysal as ps
import numpy as np

def sortkey(x): 
    return int(x)

'''
Arguments
---------
dbfile  : DBF file - Input to be imported
upper   : Condition - If true, make column heads upper case
'''
def dbf2DF(dbfile, upper=True): #Reads in DBF files and returns Pandas DF
    db = ps.open(dbfile) #Pysal to open DBF
    d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
    #pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
    pandasDF = pd.DataFrame(d) #Convert to Pandas DF
    if upper == True: #Make columns uppercase if wanted 
        pandasDF.columns = map(str.upper, db.header) 
    db.close() 
    return pandasDF



datapath = "/home/liuming/mnt/hydronas1/Projects/Forecast2020/irrigation/"

region_dbfs = {'us' : 'viccdlirr.dbf', 
               'ca' : 'vicbcirr.dbf'}
#region_dbfs = {'us' : 'viccdlirr.dbf'}
vic_dbf = "viccrbalbg.dbf"



bc_to_vic_dic = { 
                   "120" : "6001",
                   "122" : "8205",
                   "132" : "6001",
                   "133" : "4011",
                   "134" : "6001",
                   "135" : "9203",
                   "136" : "7206",
                   "137" : "7207",
                   "139" : "9209",
                   "140" : "4006",
                   "141" : "8205",
                   "142" : "7720",
                   "143" : "6001",
                   "145" : "4005", 
                   "146" : "4006",
                   "147" : "4007", 
                   "148" : "6002",
                   "149" : "6002",
                   "150" : "6004",
                   "151" : "6002",
                   "152" : "4103",
                   "153" : "4101",
                   "154" : "8514",
                   "156" : "8518",
                   "157" : "8906",
                   "158" : "8907",
                   "160" : "6003",
                   "161" : "6001",
                   "162" : "4009",
                   "163" : "6001",
                   "167" : "4010",
                   "168" : "4010",
                   "174" : "8819",
                   "177" : "4004",
                   "179" : "6002",
                   "182" : "102",
                   "183" : "103",
                   "185" : "198",
                   "188" : "2505",
                   "190" : "2002",
                   "191" : "7806",
                   "192" : "8704",
                   "195" : "7202",
                   "196" : "6004",
                   "197" : "7807",
                   "198" : "7602",
                   "199" : "6001"
                 }
cdl_to_vic_dic = {
                 "1" : "4007", 
                 "4" : "7720", 
                 "5" : "8907", 
                 "6" : "8906", 
                 "12" : "4008", 
                 "13" : "4007", 
                 "14" : "7807",
                 "21" : "4011",
                 "22" : "4012",
                 "23" : "4006",
                 "24" : "4005", 
                 "25" : "4013", 
                 "27" : "7207",
                 "28" : "7206",
                 "29" : "9203",
                 "30" : "9204",
                 "31" : "4101",
                 "32" : "8514",
                 "33" : "8518",
                 "34" : "9205",
                 "35" : "8904",
                 "36" : "7701",
                 "37" : "8205",
                 "38" : "4103",
                 "39" : "7202",
                 "41" : "8832",
                 "42" : "4010",
                 "43" : "4004",
                 "44" : "6001",
                 "46" : "8841",
                 "47" : "6002",
                 "48" : "8001",
                 "49" : "4100",
                 "50" : "8815",
                 "51" : "8813",
                 "52" : "8819",
                 "53" : "4009",
                 "54" : "8834",
                 "55" : "107",
                 "56" : "7806",
                 "57" : "7801",
                 "58" : "7708",
                 "59" : "8704",
#                 "62" : "8205",
                 "66" : "1403",
                 "67" : "1407",
                 "68" : "1401",
                 "69" : "2002",
                 "71" : "2502",
                 "76" : "1411",
                 "77" : "1409",
                 "176" : "8205",
#                 "181" : "8205",
                 "205" : "9209",
                 "206" : "4102",
                 "207" : "8802",
                 "208" : "8817",
                 "209" : "8002",
                 "214" : "8807",
                 "216" : "8826",
                 "219" : "2207",
                 "220" : "1410",
                 "221" : "7106",
                 "222" : "8831",
                 "223" : "1402",
                 "224" : "7602",
                 "225" : "4005",
                 "226" : "7206",
                 "227" : "8820",
                 "229" : "8828",
                 "237" : "4011",
                 "242" : "102",
                 "243" : "8809",
                 "244" : "8811",
                 "246" : "8839",
                 "247" : "9208",
                 "249" : "9211",
                 "250" : "103"
                 }

out_veg_list = [
        "102",
        "103",
        "107",
        "198",
        "1401",
        "1402",
        "1403",
        "1407",
        "1409",
        "1410",
        "1411",
        "2001",
        "2002",
        "2207",
        "2502",
        "2504",
        "2505",
        "4004",
        "4005",
        "4006",
        "4007",
        "4008",
        "4009",
        "4010",
        "4011",
        "4012",
        "4013",
        "4100",
        "4101",
        "4102",
        "4103",
        "6001",
        "6002",
        "6003",
        "6004",
        "7106",
        "7202",
        "7206",
        "7207",
        "7602",
        "7701",
        "7708",
        "7720",
        "7801",
        "7806",
        "7807",
        "8001",
        "8002",
        "8205",
        "8514",
        "8518",
        "8704",
        "8802",
        "8804",
        "8807",
        "8809",
        "8811",
        "8813",
        "8815",
        "8817",
        "8819",
        "8820",
        "8824",
        "8826",
        "8828",
        "8831",
        "8832",
        "8834",
        "8839",
        "8841",
        "8904",
        "8906",
        "8907",
        "9203",
        "9204",
        "9205",
        "9208",
        "9209",
        "9211"
        ]

#20201221 removed alfalfa 7701 seed 8704
Always_irrigation = ["102","103","107","198","1401","1402","1403","1407","1409"
                     ,"1410","1411","2002","2207","2502","2505","4004"
                     ,"4007","4008","4100","4101","4102","6002","7106"
                     ,"7207","7720","7801","7806","7807"
                     ,"8001","8002","8802","8807","8809","8811","8815"
                     ,"8817","8820","8826","8828","8831","8832","8834","8839"
                     ,"8841","8904","9204","9205","9208"]

#read combined infomation
outrec=dict()

df = dict()
for region in region_dbfs:
    print(region)
    dbf_filename = datapath + region_dbfs[region]
    vic_idfile = datapath + vic_dbf
    #dbf = Dbf5(dbf_filename)
    #df[region] = dbf.to_dataframe()
    df[region] = dbf2DF(dbf_filename)
    total_vic = dbf2DF(vic_idfile).rename(columns={'VALUE' : 'VICCRBALBG','COUNT':'TVIC_COUNT'})
    if region == 'us':
        lc = 'CDL2018'
        irr = 'USIRRF01'
        lcdic = cdl_to_vic_dic
    else:
        lc = 'BC2018'
        irr = 'BCIRRF01'
        lcdic = bc_to_vic_dic
    df[region]['clc'] = df[region][lc].apply(str)

        
    total_lc = df[region][df[region]['clc'].isin(lcdic)].groupby(['VICCRBALBG'])['COUNT'].sum().reset_index().rename(columns={'COUNT':'TLC_COUNT'})
    total_irr = df[region][df[region][irr] == 1].groupby(['VICCRBALBG'])['COUNT'].sum().reset_index().rename(columns={'COUNT':'TIRR_COUNT'})
    #total_lc_irr = df[region][df[region][irr] == 1][['VICCRBALBG',lc,"COUNT"]].rename(columns={'COUNT':'TLC_IRR_COUNT'})
    
    #joint = df[region].join(total_vic,on=['VICCRBALBG'],how='left',lsuffix='l',rsuffix='r')
    #DataFrame.join(self, other, on=None, how='left', lsuffix='', rsuffix='', sort=False) → 'DataFrame'
    joint = pd.merge(df[region],total_vic,on=['VICCRBALBG'],how='left',suffixes=('_l', '_y')).replace(np.nan, 0)
    joint = pd.merge(joint,total_lc,on=['VICCRBALBG'],how='left',suffixes=('_l', '_y')).replace(np.nan, 0)
    joint = pd.merge(joint,total_irr,on=['VICCRBALBG'],how='left',suffixes=('_l', '_y')).replace(np.nan, 0)
    index_t = 0
    for index, row in joint.iterrows():
        #if  index_t == 300:
        #    break
        #print(index_t,row["VICCRBALBG"], row[lc], row[irr], row['TVIC_COUNT'])
        row_lc = str(row[lc])
        if row_lc in lcdic:
            vic_crop = lcdic[row_lc]
            vic_crop_fraction = row['COUNT'] / row['TVIC_COUNT']
            vic_crop_dry = '-1'
            #dry crop code 
            if vic_crop not in Always_irrigation and row[irr] == 0:
                vic_crop_dry = str(10000 + int(vic_crop))
                
            if row["VICCRBALBG"] not in outrec:
                outrec[row["VICCRBALBG"]] = dict()
            if vic_crop not in outrec[row["VICCRBALBG"]]:
                outrec[row["VICCRBALBG"]][vic_crop] = 0.0
            if vic_crop_dry != '-1' and vic_crop_dry not in outrec[row["VICCRBALBG"]]:
                outrec[row["VICCRBALBG"]][vic_crop_dry] = 0.0
            
            if vic_crop in Always_irrigation:
                outrec[row["VICCRBALBG"]][vic_crop] += vic_crop_fraction
            else:
                if row["TIRR_COUNT"] > row["TLC_COUNT"]:
                    outrec[row["VICCRBALBG"]][vic_crop] += vic_crop_fraction
                else:
                    if row[irr] == 1:
                        outrec[row["VICCRBALBG"]][vic_crop] += vic_crop_fraction
                    else:
                        outrec[row["VICCRBALBG"]][vic_crop_dry] += vic_crop_fraction
                    
        index_t += 1
    #output textfile
    outfile = datapath + region + "_vicid_crop_fraction.txt"
    file1 = open(outfile,"w") 
    for grid in sorted(outrec, key=sortkey, reverse=False):
        for crop in sorted(outrec[grid], key=sortkey, reverse=False):
            if outrec[grid][crop] > 0.00001:
                file1.write(str(grid) + ',' + crop + ',' + str('%.5f' % outrec[grid][crop]) + "\n")
                #print(str(grid) + ',' + crop + ',' + str('%.5f' % outrec[grid][crop]) + "\n")
    file1.close()
    print("Done!\n")

#for grid in sorted(vic_neighbor, key=sortkey, reverse=False):
    

    
    
        