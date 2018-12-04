#!/usr/bin/env python
# coding: utf-8

# In[4]:


# See site: https://www.zillow.com/research/data/
# Files to peruse:

# Zip_ZriPerSqft_AllHomes            - Median of the estimated monthly rent price of all homes, per square foot.
# Zip_MedianValuePerSqft_AllHomes    - median of estimate sales price per square foot by zipcode


import requests, zipfile, io, csv
import pandas as pd
import os
import platform
import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as stat


zillowPriceDict = {}
pricePerBedDict = {}
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


# creating dictionary for storing pricing data found in files
for z in zipCodeList:
    zillowPriceDict[str(z)] = {'LAT': np.nan,'LNG': np.nan,'medSalePPSF': np.nan,'medSalePerBed': np.nan}
    # create dictionary for calculating average price per bedroom of all house sales in each zipcode
    pricePerBedDict[str(z)] = {'SumOfSales': 0,'NumOfBedroomsSold': 0}


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
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
lastLoaded = creation_date('Zip\\Zip_MedianValuePerSqft_AllHomes.csv')

# extract zip from zillow to folder once a day
if (yesterday > lastLoaded):
    print("Zillow data file last update: ",lastLoaded)
    print("More than 24 hours since last update")
    print("Updating file...")
    zipUrl = 'http://files.zillowstatic.com/research/public/Zip.zip'
    r = requests.get(zipUrl)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()

with open('ZipcodeCoordinates.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if row['ZIP'] in zillowPriceDict:
            zillowPriceDict[row['ZIP']]['LAT'] = float(row['LAT'])
            zillowPriceDict[row['ZIP']]['LNG'] = float(row['LNG'])
    
#getting Sales prices and saving them to dictionary
# sale price per sqft
with open('Zip\\Zip_MedianValuePerSqft_AllHomes.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if (row['State'] == 'PA') and (row['RegionName'] in zillowPriceDict) and (row['2018-09'] != ""):
            zillowPriceDict[row['RegionName']]['medSalePPSF'] = float(row['2018-09'])
            
# med sale of 1 bed   
with open('Zip\\Zip_Zhvi_1bedroom.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader: 
        if (row['State'] == 'PA') and (row['RegionName'] in zillowPriceDict) and (row['2018-09'] != ""):
            pricePerBedDict[row['RegionName']]['SumOfSales'] += float(row['2018-09'])
            pricePerBedDict[row['RegionName']]['NumOfBedroomsSold'] += 1
                
# med sale of 2 bed
with open('Zip\\Zip_Zhvi_2bedroom.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader: 
        if (row['State'] == 'PA') and (row['RegionName'] in zillowPriceDict) and (row['2018-09'] != ""):
            pricePerBedDict[row['RegionName']]['SumOfSales'] += float(row['2018-09'])/2
            pricePerBedDict[row['RegionName']]['NumOfBedroomsSold'] += 1

# med sale of 3 bed
with open('Zip\\Zip_Zhvi_3bedroom.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader: 
        if (row['State'] == 'PA') and (row['RegionName'] in zillowPriceDict) and (row['2018-09'] != ""):
            pricePerBedDict[row['RegionName']]['SumOfSales'] += float(row['2018-09'])/3
            pricePerBedDict[row['RegionName']]['NumOfBedroomsSold'] += 1
                
# med sale of 4 bed
with open('Zip\\Zip_Zhvi_4bedroom.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader: 
        if (row['State'] == 'PA') and (row['RegionName'] in zillowPriceDict) and (row['2018-09'] != ""):
            pricePerBedDict[row['RegionName']]['SumOfSales'] += float(row['2018-09'])/4
            pricePerBedDict[row['RegionName']]['NumOfBedroomsSold'] += 1     
# med sale of 5plus beds 
with open('Zip\\Zip_Zhvi_5BedroomOrMore.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader: 
        if (row['State'] == 'PA') and (row['RegionName'] in zillowPriceDict) and (row['2018-09'] != ""):
            pricePerBedDict[row['RegionName']]['SumOfSales'] += float(row['2018-09'])/5
            pricePerBedDict[row['RegionName']]['NumOfBedroomsSold'] += 1
                
            
# append average price per room info to zillow price dictionary
for key in zillowPriceDict:
    if pricePerBedDict[key]['NumOfBedroomsSold'] != 0:
        zillowPriceDict[key]['medSalePerBed'] = round(pricePerBedDict[key]['SumOfSales'] / pricePerBedDict[key]['NumOfBedroomsSold'], 2)
    

#convert dictionary to dataframe
df = pd.DataFrame(zillowPriceDict).T

# fill in empty pricing values with min because they're likely rural
df['medSalePPSF'] = df['medSalePPSF'].fillna(value=min(df['medSalePPSF']))
df['medSalePerBed'] = df['medSalePerBed'].fillna(value=min(df['medSalePerBed']))



#function to return zillowDataDictionary when called from main file
def zillowData():
    return df

def zillowDataDict():
    return zillowPriceDict

def housingHeatMap():
    lat = np.array(df['LAT'].tolist())
    lng = np.array(df['LNG'].tolist())
    prices = np.array(df['medSalePerBed'].tolist())
    data = pd.DataFrame(data={'x':lat, 'y':lng, 'z':prices})
    data = data.dropna(how='any',axis=0) 
    print(data)
    data = data.pivot(index='x', columns='y', values='z')
    
    sns.heatmap(data)
    plt.show()

def zillowBarChart():
    args = ['15232', '15133', '15063']
    zips = []
    PPSF = []
    PricePerBed = []
    
    # data to plot
    for i in args:
        if i in df.index.values:
            zips.append(i)
            PPSF.append(df.loc[i, 'medSalePPSF'])
            PricePerBed.append(df.loc[i, 'medSalePerBed'])
    print(zips)
    print(PPSF)
    
    zipsBarDF = pd.DataFrame({'zips': zips, 'PPSF': PPSF, 'medSalePrice': PricePerBed})
    print(zipsBarDF)
    
    fig = plt.figure()
    
    ax = zipsBarDF['PPSF'].plot(kind="bar", alpha=0.7)
    ax = fig.add_subplot(111)
    
    ax2 = ax.twinx()
    ax2 = zipsBarDF['medSalePrice'].plot(kind="bar", alpha=0.7)
#    ax2.plot(ax.get_xticks(),zipsBarDF['medSalePrice'],marker='o', linewidth=4)
    
    ax.set_xticklabels(zipsBarDF['zips'])
    ax.set_ylim(0,1.3*zipsBarDF['PPSF'].max())
    ax2.set_ylim(0,1.3*zipsBarDF['medSalePrice'].max())
    ax2.grid(False)
    plt.show()
    
    
    
    
    
    index = np.arange(len(args))
    bar_width = 0.35
    
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    
    fig = plt.figure() # Create matplotlib figure
    ax = fig.add_subplot(111) # Create matplotlib axes
    ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.
    
    width = 0.2
    
    zipsBarDF['PPSF'].plot(kind='bar', color='red', ax=ax, width=width, position=1)
    zipsBarDF['medSalePrice'].plot(kind='bar', color='blue', ax=ax2, width=width, position=0)
    ax.set_xticklabels(zipsBarDF['zips'])
    ax.set_ylim(0,1.3*zipsBarDF['PPSF'].max())
    ax2.set_ylim(0,1.3*zipsBarDF['medSalePrice'].max())
    
    ax.set_ylabel('Price / SqFoot')
    ax2.set_ylabel('Price Per Bedroom')
    plt.legend(loc='best')
    
    plt.show()
        
#    ind = np.arange(3) 
#    width = 0.35       
#    plt.bar(ind, PPSF, width, label='Price/SqFoot')
#    plt.bar(ind + width, PricePerBed, width, label='PricePerBed')
#    
#    plt.ylabel('Scores')
#    plt.title('Scores by group and gender')
#    
#    plt.xticks(ind + width / 2, args)
#    
#    plt.show()
    
    
    
    
#    n_groups = 4
#    means_frank = (90, 55, 40, 65)
#    means_guido = (85, 62, 54, 20)
# 
#    # create plot
#    fig, ax = plt.subplots()
#    index = np.arange(n_groups)
#    bar_width = 0.35
#    opacity = 0.8
# 
#    rects1 = plt.bar(index, means_frank, bar_width,
#                 alpha=opacity,
#                 color='b',
#                 label='Frank')
# 
#    rects2 = plt.bar(index + bar_width, means_guido, bar_width,
#                 alpha=opacity,
#                 color='g',
#                 label='Guido')
# 
#    plt.xlabel('Person')
#    plt.ylabel('Scores')
#    plt.title('Scores by person')
#    plt.xticks(index + bar_width, ('A', 'B', 'C', 'D'))
#    plt.legend()
# 
#    plt.tight_layout()
#    plt.show()

if __name__ == '__main__':  
    zillowPriceDict
    for i in zillowPriceDict:
        print(i,zillowPriceDict[i])
    zillowBarChart()
    
    # write dictionary to csv
    df.to_excel('ZipCodeMedHousingPrice.xlsx')
            


# In[ ]:





# In[ ]:




