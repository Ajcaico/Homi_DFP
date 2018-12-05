#!/usr/bin/env python
# coding: utf-8

# In[149]:


# Team 5: Amanda Baker, Alex Caico, Colton Mouritsen, Daniel Lesser, Joseph Standefer
# Filename: ArrestData.py 
# This code scrapes data from the WPRDC website on Pittsburgh crimes reported, by zipcode.
# The code then takes the data and transforms it into counts of certain crimes types (such as assault, robbery, drug possession)
# and returns a dataframe with counts of each per zip code, plus an aggregate score based on weighted crime values.
# This file is imported by the main module AggregateData.py (import ArrestData as ar)

import requests, zipfile, io, csv
import pandas as pd
import numpy as np
import re
import os
import platform
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

zipCodeList = ['15101','15003','15005','15006','15007','15102','15014','15104','15015','15017',
                 '15018','15020','15106','15024','15025','15026','15108','15028','15030','15046',
                 '15031','15034','15110','15035','15112','15037','15332','15044','15045','15116',
                 '15047','15049','15120','15126','15051','15642','15056','16046','15057','15136',
                 '15131','15132','15133','15135','15063','15146','15064','15668','15065','15068',
                 '15137','15071','15139','15140','15201','15202','15203','15204','15205','15206',
                 '15207','15208','15209','15210','15211','15212','15213','15214','15215','15216',
                 '15217','15218','15219','15220','15221','15222','15223','15224','15225','15226',
                 '15227','15228','15229','15232','15233','15234','15235','15236','15237','15238',
                 '15239','15241','15243','15260','15290','15142','15075','15076','16055','15143',
                 '15129','15144','15082','15084','15085','15145','16059','15147','15086','15088',
                 '15122','15089','15090','15148']

#check creation date of file, system time function
# Reference stackOverflow
def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        time = os.path.getmtime(path_to_file)
        return datetime.datetime.fromtimestamp(time)
    else:
        time = os.stat(path_to_file)
        stat = datetime.datetime.fromtimestamp(time)
        try:
            return datetime.datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
        
# get datetime from yesterday to compare
# yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
# lastLoaded = creation_date('Zip\\Zip_MedianValuePerSqft_AllHomes.csv')

# load and clean data; parse zipcode and offense type
df = pd.read_csv('https://data.wprdc.org/datastore/dump/e03a89dd-134a-4ee8-a2bd-62c40aeebc6f')

df['OFFENSES'] = df['OFFENSES'].fillna(value='NA NA')
df['ARRESTLOCATION'] = df['ARRESTLOCATION'].fillna(value='Pittsburgh, PA 00000')
df['ARRESTLOCATION'] = np.where(df['ARRESTLOCATION'].str.contains("Zone", case=False, na=False), 'Pittsburgh, PA 00000', df['ARRESTLOCATION'].apply(str))
df1 = pd.DataFrame(df.OFFENSES.str.split(' ',1).tolist(), columns = ['OFFENSE_CODE', 'OFFENSE_TYPE'])
df1['ZIPCODE'] = df['ARRESTLOCATION'].str[-5:]

# sorting crime by type
df1['ALL_CRIME'] = np.where(df1['OFFENSE_TYPE'].str.contains(r'', case=False, na=False), 'Y', 0)
df1['ASSAULT_CRIME'] = np.where(df1['OFFENSE_TYPE'].str.contains("Assault", case=False, na=False), 'Y', 0)
df1['SIMP_ASSAULT_CRIME'] = np.where(df1['OFFENSE_TYPE'].str.contains("Simple Assault", case=False, na=False), 'Y', 0)
df1['AGGV_ASSAULT_CRIME'] = np.where(df1['OFFENSE_TYPE'].str.contains("Aggravated Assault", case=False, na=False), 'Y', 0)
df1['DRUG_CRIME'] = np.where(df1['OFFENSE_TYPE'].str.contains("Possession", case=False, na=False), 'Y', 0)
df1['ROBBERY_CRIME'] = np.where(df1['OFFENSE_TYPE'].str.contains("Robbery", case=False, na=False), 'Y', 0)

# aggregate crime counts per zipcode
df2 = pd.DataFrame(df1[df1['OFFENSE_TYPE'].str.contains("Assault")].groupby('ZIPCODE')['ASSAULT_CRIME'].count())
df3 = pd.DataFrame(df1[df1['OFFENSE_TYPE'].str.contains("Simple Assault")].groupby('ZIPCODE')['SIMP_ASSAULT_CRIME'].count())
df4 = pd.DataFrame(df1[df1['OFFENSE_TYPE'].str.contains("Aggravated Assault")].groupby('ZIPCODE')['AGGV_ASSAULT_CRIME'].count())
df4 = df4.multiply(2, axis='ZIPCODE', level=None, fill_value=0)
df5 = pd.DataFrame(df1[df1['OFFENSE_TYPE'].str.contains("Possession")].groupby('ZIPCODE')['DRUG_CRIME'].count())
df5 = df5.multiply(.25, axis='ZIPCODE', level=None, fill_value=0)
df6 = pd.DataFrame(df1[df1['OFFENSE_TYPE'].str.contains("Robbery")].groupby('ZIPCODE')['ROBBERY_CRIME'].count())
df6 = df6.multiply(.5, axis='ZIPCODE', level=None, fill_value=0)
df7 = pd.DataFrame(df1[df1['OFFENSE_TYPE'].str.contains(r'')].groupby('ZIPCODE')['ALL_CRIME'].count())

# organize crime count per zipcode, by crime type
dfZ = pd.DataFrame(zipCodeList, columns=['ZIPCODE'])
dfM = dfZ.merge(df2, how='left', on='ZIPCODE')
dfM = dfM.merge(df3, how='left', on='ZIPCODE')
dfM = dfM.merge(df4, how='left', on='ZIPCODE')
dfM = dfM.merge(df5, how='left', on='ZIPCODE')
dfM = dfM.merge(df6, how='left', on='ZIPCODE')
dfM = dfM.merge(df7, how='left', on='ZIPCODE')
dfM = dfM.set_index('ZIPCODE')
dfM = dfM.fillna(0)


# aggregate crime stats across crime type by zipcode
# weights: Aggravated = .6, Simple = .2, Robbery = .15, Possession = .05
dfM['CrimeScoreP'] = (dfM['SIMP_ASSAULT_CRIME']*.2) + (dfM['AGGV_ASSAULT_CRIME']*.6) + (dfM['DRUG_CRIME']*.05) + (dfM['ROBBERY_CRIME']*.15)
dfM['CrimeScore'] = (dfM['CrimeScoreP']/(dfM['CrimeScoreP'].max()))*5

# returns the dataframe with arrest statistics
def arrestData():
    return dfM

# returns a dataframe with just the zipcodes and their crime score
def arrestDataScore():
    # dropping all columns and keeping just the crime score
    #dfM.drop(['ASSAULT_CRIME','SIMP_ASSAULT_CRIME','AGGV_ASSAULT_CRIME','DRUG_CRIME','ROBBERY_CRIME','ALL_CRIME','CrimeScoreP'], axis=1, inplace=True)
    return dfM

# shows a bar chart for all zipcodes and corresponding crime scores
def macroCrimeStats():
    dfC = dfM[dfM['CrimeScore'] != 0]
    dfChart = dfC.plot.bar( y='CrimeScore', rot=0)
    plt.show()
    
# shows a bar chart for a specific zip code, across the measures of total reported crimes, assault counts, possession crime counts, and robbery crime counts    
def microCrimeStats(zipcode):
    listTotalCrime = ['Total Crime', (dfM['ALL_CRIME'].loc[str(zipcode)])]
    listAssault = ['Assaults', (dfM['ASSAULT_CRIME'].loc[str(zipcode)])]
    listDrugs = ['Possession', (dfM['DRUG_CRIME'].loc[str(zipcode)])]
    listRobbery = ['Robbery', (dfM['ROBBERY_CRIME'].loc[str(zipcode)])]    

    listOfMetrics = [listTotalCrime, listAssault, listDrugs, listRobbery]

    col_names = ['Crime Type', 'count']
    df = pd.DataFrame(listOfMetrics, columns = col_names)
    df = df.set_index('Crime Type')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel("Count")
    ax2 = ax.twinx()
    width = 0.3

    df['count'].plot(kind='bar', color='skyblue', ax=ax,width=width, position=1, align='center')

    local_patch = mpatches.Patch(color='skyblue', label='Local Count')
    plt.legend(handles=[local_patch])

    plt.title("Allegheny County Crime Data")
    plt.show()
    

    
if __name__ == '__main__':         
    # write dictionary to csv
    dfM.to_excel('AggregatedPittsburghCrimeData.xlsx')

