"""Group 5, Colton Mouritsen, Amanda Baker, Alex Caico, Dan Lesser, Joe Standerfer
    File Name:  CraigslistCode.py
    This file is for scraping data from https://pittsburgh.craigslist.org/d/apts-housing-for-rent/search/apa with getData() function
    This file also creates a raw data excel file and aggregate data excel file
    This file also creates specific zip code graphs with getZipcodePlot() function
    This file also creates aggregated graphs for all zip codes with getOverallAggregateData() function
    This file is imported by HomiUserInput.py
    This file imports ZillowHousingDataByZipWithMedianforBedrooms, pandas, BeautifulSoup, requests, numpy, matplotlib.pyplot, and statistics
"""

import pandas as pd
from bs4 import BeautifulSoup as bs4
import requests
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat
import ZillowHousingDataByZipWithMedianforBedrooms as zillow

##ALl variables used in code
apartmentCount = 0
prices = []
avgPricePerBedroom = []
squareFootage = []
bedrooms = []
titles = []
neighborhoods = []
allData = []
allData_list = []
zipPrices = []
zipSquareFootage = []
zipBedrooms = []
zipTitles = []
zipNeighborhoods = []
allDictionary = {}
zipDictionary = {}
zipcodes = ['15101','15003','15005','15006','15007','15102','15014','15104','15015','15017',
            '15018','150220','15106','15024','15025','15026','15108','15028','15030','15046',
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

##function called to determine square footage and number of bedrooms in listing  
def find_size_and_brs(size):
    split = size.strip().strip('/- ').split(' -\n ')
    if len(split) == 2:
        n_brs = split[0].replace('br', '')
        this_size = split[1].replace('ft2', '')
        bedrooms.append(n_brs)
        squareFootage.append(this_size)
    elif 'br' in split[0]: #if the section contains "br" then the number of bedrooms were not left empty
        # It's the n_bedrooms
        n_brs = split[0].replace('br', '')
        bedrooms.append(n_brs)
        this_size = np.nan
        squareFootage.append(this_size)
    elif 'ft2' in split[0]: #if the section contains "ft2" then the square footage was not left empty
        # It's the size
        this_size = split[0].replace('ft2', '')
        squareFootage.append(this_size)
        n_brs = np.nan
        bedrooms.append(n_brs)
    return float(this_size), float(n_brs)

#Function to return dataframe and csv containing all data (raw), and all aggregated zip code data.  Also prints data to consol.
def getData():
    url_base = 'https://pittsburgh.craigslist.org/d/apts-housing-for-rent/search/apa'
    for zipcode in zipcodes:
        params = dict(postal=zipcode)
        
        #Loop through all zip codes by changing the parameters in the URl to contain each zip
        rsp = requests.get(url_base, params=params)
        
        html = bs4(rsp.text, 'html.parser')

#        print('***************' + str(zipcode) + '*******************')
        
        #find all sections of HTML code that contains listing data ("result info")
        apts = html.find_all('p', attrs={'class': 'result-info'})
           
        aptCount = 0
        #Loop through all apartments in the "result info" section and find specifics regarding each listing
        for apt in apts:
            this_appt = apts[aptCount]
            if this_appt.find('span', attrs={'class': 'housing'}) is None:
                this_size = np.nan
                n_brs = np.nan
                bedrooms.append(n_brs)
                squareFootage.append(this_size)
            else:
                size = this_appt.findAll('span', attrs={'class': 'housing'})[0].text
                this_size, n_brs = find_size_and_brs(size)
                zipBedrooms.append(n_brs)
                zipSquareFootage.append(this_size)
                
            this_time = this_appt.find('time')['datetime']
            this_time = pd.to_datetime(this_time)
            
            if this_appt.find('span', {'class': 'result-price'}) is None:
                this_price = np.nan
                prices.append(this_price)
            else:
                this_price = float(this_appt.find('span', {'class': 'result-price'}).text.strip('$'))
                prices.append(this_price)
                zipPrices.append(this_price)
                
            if this_appt.find('a', attrs={'class': 'hdrlnk'}).text is None:
                this_title = np.nan
                titles.append(this_title)
            else:
                this_title = this_appt.find('a', attrs={'class': 'hdrlnk'}).text
                titles.append(this_title)
                zipTitles.append(this_title)
                
            if this_appt.find('span', {'class': 'result-hood'}) is None:
                this_neighborhood = np.nan
                neighborhoods.append(this_neighborhood)
            else:
                this_neighborhood = this_appt.find('span', {'class': 'result-hood'}).text.strip().strip('(').strip(')')
                neighborhoods.append(this_neighborhood)
                zipNeighborhoods.append(this_neighborhood)
            
            aptCount = aptCount + 1
            
            #Set list to then add to the dataframe
            allData = [zipcode, this_title, this_neighborhood, this_price, this_size, n_brs, this_time]
            col_names = ["Zipcode", "Title", "Neighborhood", "Price", "Square Footage", "Bedrooms", "Posted Time"]
            allData_list.append(allData)
            
            # filter out all bedrooms that are null so that the calculation can be made on each zipcode
            nonNullBedrooms = 0
            nonNullBedroomsList = []
            for beds in zipBedrooms:
                if beds is not np.nan:   
                    nonNullBedrooms = nonNullBedrooms + 1
                    nonNullBedroomsList.append(float(beds))
            
            # filter out all square footage data that is null so that the calculation can be made on each zipcode
            nonNullSF = 0
            nonNullSFList = []
            for sf in zipSquareFootage:
                if sf is not np.nan:  
                    nonNullSF = nonNullSF + 1
                    nonNullSFList.append(float(sf))   
        
        rentalAptPrices = 0
        rentalAptNumBedrooms = 0
        rentalAptSquareFeet = 0
        rentalPricePerBedroom = 0
        
        if (len(zipPrices) == 0):
            rentalAptPrices = np.nan
        elif (np.sum(zipPrices)/len(zipPrices) >= 0):
            rentalAptPrices = np.sum(zipPrices)/len(zipPrices)
            
        if (len(nonNullBedroomsList) == 0):
            rentalAptNumBedrooms = np.nan
        elif (np.sum(nonNullBedroomsList)/len(nonNullBedroomsList) >= 0):
            rentalAptNumBedrooms = np.sum(nonNullBedroomsList)/len(nonNullBedroomsList)
            
        if (len(nonNullSFList) == 0):
            rentalAptSquareFeet = np.nan
        elif (np.sum(nonNullSFList)/len(nonNullSFList) >= 0):
            rentalAptSquareFeet = np.sum(nonNullSFList)/len(nonNullSFList) 
            
        if (np.sum(nonNullBedroomsList) == 0):
            rentalPricePerBedroom = np.nan
        elif (np.sum(zipPrices)/np.sum(nonNullBedroomsList) >= 0):
            rentalPricePerBedroom = np.sum(zipPrices)/np.sum(nonNullBedroomsList)  
         
        zipDictionary[zipcode] = {'Zipcode' : zipcode,
                'NumApartments': aptCount,
                'RentalAptPrices': rentalAptPrices, 
                'RentalAptNumBedrooms': rentalAptNumBedrooms,
                'RentalAptSquareFeet': rentalAptSquareFeet,
                'RentalPricePerBedroom': rentalPricePerBedroom}
        
#        print('Number of Apartment Listings: ', str(aptCount))
#        print('Average price of Apartment Listings: ', "{0:.2f}".format(np.sum(zipPrices)/len(zipPrices)))
#        print('Average square footage of Apartment Listings: ', "{0:.2f}".format(np.sum(nonNullSFList)/len(nonNullSFList)))
#        print('Average number of bedrooms: ', "{0:.2f}".format(np.sum(nonNullBedroomsList)/len(nonNullBedroomsList)))
#        print('Average price per bedroom: ', "{0:.2f}".format(np.sum(zipPrices)/np.sum(nonNullBedroomsList)))
        
        #Append average price per bedroom from all non null values to the nonNullBedroomsList
        if (np.sum(nonNullBedroomsList) == 0):
            nonNullBedroomsList == np.nan
        elif (np.sum(zipPrices)/np.sum(nonNullBedroomsList) >= 0):
            avgPricePerBedroom.append(np.sum(zipPrices)/np.sum(nonNullBedroomsList))
        #clear all zip code specific lists to then fill with the new zip code that is next in the list    
        zipPrices.clear()
        zipSquareFootage.clear()
        zipNeighborhoods.clear()
        zipBedrooms.clear()
        nonNullSFList.clear()
        nonNullBedroomsList.clear()
    
    # filter out all null prices for graphing ability
    notNull = 0
    avgPricePerBedNotNull = []
    for avgPrices in avgPricePerBedroom:
        if avgPrices is not np.nan:
            notNull = notNull + 1
            avgPricePerBedNotNull.append(float(avgPrices))
            
    # filter out all null prices for graphing ability        
    notNullPrice = 0
    avgPriceList = []
    for avgPrices in prices:
        if avgPrices is not np.nan:
            notNullPrice = notNullPrice + 1
            avgPriceList.append(float(avgPrices))
       
    df_raw = pd.DataFrame(allData_list, columns = col_names)
    df_raw.to_excel("RawCraigslistData.xlsx")
    
    df_summary = pd.DataFrame(zipDictionary).T
    df_summary.to_excel("AggregateCraigslistData.xlsx")
    
    return df_summary
 
def getExcelData():
    df_CraigslistExcelData = pd.read_excel("AggregateCraigslistData.xlsx")
    df_CraigslistExcelData = df_CraigslistExcelData.set_index('Zipcode')
    
    df_AllCraigslistExcelData = pd.read_excel("RawCraigslistData.xlsx")
    df_AllCraigslistExcelData = df_AllCraigslistExcelData.set_index('Zipcode')
    
    return {'alldata' : df_AllCraigslistExcelData, 'aggregateData' : df_CraigslistExcelData}

    
#Finding all non null price values
def getOverallAggregateData():
    dataDict = getExcelData()
    df = dataDict['aggregateData']
    df = df.dropna()
    df = df[(df.NumApartments !=0) & (df.RentalAptNumBedrooms != 0) & (df.RentalAptPrices !=0) & (df.RentalAptSquareFeet !=0) & (df.RentalPricePerBedroom !=0)]
    
    num_bins = 25
    
    df_RentalAptPrices = df['RentalAptPrices']
    plt.title("Distribution of Average Rental Prices by Zip")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.hist(df_RentalAptPrices, num_bins, color = 'skyblue') 
    plt.show()
    
    df_PricePerBedroom = df['RentalPricePerBedroom']
    plt.title("Distribution of Average Rental Price Per Bedroom by Zip")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.hist(df_PricePerBedroom, num_bins, color = 'skyblue') 
    plt.show()
    
    df_SquareFootage = df['RentalAptSquareFeet']
    x = [n for n in df_RentalAptPrices]
    y = [n for n in df_SquareFootage]
    plt.title("Average Rental Price and Square Footage by Zip")
    plt.xlabel("Price")
    plt.ylabel("Square Footage")
    plt.scatter(x, y, num_bins, color = 'skyblue') 
    plt.show()
    
def getZipcodePlot(zipcode):
    zip = zipcode
    url_base = 'https://pittsburgh.craigslist.org/d/apts-housing-for-rent/search/apa'
    params = dict(postal=zip)
        
    rsp = requests.get(url_base, params=params)
    
    html = bs4(rsp.text, 'html.parser')
    
    apts = html.find_all('p', attrs={'class': 'result-info'})
       
    aptCount = 0
    for apt in apts:
        this_appt = apts[aptCount]
        if this_appt.find('span', attrs={'class': 'housing'}) is None:
            this_size = np.nan
            n_brs = np.nan
            bedrooms.append(n_brs)
            squareFootage.append(this_size)
        else:
            size = this_appt.findAll('span', attrs={'class': 'housing'})[0].text
            this_size, n_brs = find_size_and_brs(size)
            zipBedrooms.append(n_brs)
            zipSquareFootage.append(this_size)
            
        this_time = this_appt.find('time')['datetime']
        this_time = pd.to_datetime(this_time)
        
        if this_appt.find('span', {'class': 'result-price'}) is None:
            this_price = np.nan
            prices.append(this_price)
        else:
            this_price = float(this_appt.find('span', {'class': 'result-price'}).text.strip('$'))
            prices.append(this_price)
            zipPrices.append(this_price)
            
        if this_appt.find('a', attrs={'class': 'hdrlnk'}).text is None:
            this_title = np.nan
            titles.append(this_title)
        else:
            this_title = this_appt.find('a', attrs={'class': 'hdrlnk'}).text
            titles.append(this_title)
            zipTitles.append(this_title)
            
        if this_appt.find('span', {'class': 'result-hood'}) is None:
            this_neighborhood = np.nan
            neighborhoods.append(this_neighborhood)
        else:
            this_neighborhood = this_appt.find('span', {'class': 'result-hood'}).text.strip().strip('(').strip(')')
            neighborhoods.append(this_neighborhood)
            zipNeighborhoods.append(this_neighborhood)
        
        aptCount = aptCount + 1
        
        allData = [zipcode, this_title, this_neighborhood, this_price, this_size, n_brs, this_time]
        allData_list.append(allData)
        
        nonNullBedrooms = 0
        nonNullBedroomsList = []
        for beds in zipBedrooms:
            if beds is not np.nan:   
                nonNullBedrooms = nonNullBedrooms + 1
                nonNullBedroomsList.append(float(beds))
                
        avgPricePerBedroom.append(np.sum(zipPrices)/np.sum(nonNullBedroomsList))
        
        nonNullSF = 0
        nonNullSFList = []
        for sf in zipSquareFootage:
            if sf is not np.nan:  
                nonNullSF = nonNullSF + 1
                nonNullSFList.append(float(sf))
    
    if len(zipSquareFootage) < len(zipPrices):
        diff = len(zipPrices) - len(zipSquareFootage)
        i = 0
        while i < diff:
            zipSquareFootage.append(np.average(zipSquareFootage))
            i = i + 1
    
    if len(zipBedrooms) < len(zipPrices):
        diff = len(zipPrices) - len(zipBedrooms)
        i = 0
        while i < diff:
            zipBedrooms.append(np.average(zipBedrooms))
            i = i + 1
    
    bedroomGroups = []
    for rooms in zipBedrooms:
        if rooms not in bedroomGroups:
            bedroomGroups.append(rooms)
    
    N = len(zipSquareFootage)
    x = [n for n in [zipSquareFootage]]
    y = [n for n in [zipPrices]]
    colors = [n for n in [zipBedrooms]]
    #area = [n for n in [zipBedrooms]]
    plt.title("Scatter Plot of Prices, Square Footage, and Bedrooms for " + str(zipcode) + "\n Colors Are Number of Bedrooms from 1 - " + str(max(zipBedrooms)))
    plt.xlabel("Square Footage")
    plt.ylabel("Price")
    plt.scatter(x, y, c=colors, alpha=0.5, cmap='viridis')
    plt.show()
        
    numCols = [[1],[2]]
    listBedrooms = []
    listPrices = []
    listSF = []
    listOfBedrooms = []
    listOfPrices = []
    listOfSF = []
    
    for room in bedrooms:
        for num in numCols:
            listBedrooms.append(room)
            if len(listBedrooms) == 2:
                listOfBedrooms.append(listBedrooms.copy())
                listBedrooms.clear()        
            
    for thePrice in prices:
        for num in numCols:
            listPrices.append(thePrice)
            if len(listPrices) == 2:
                listOfPrices.append(listPrices.copy())
                listPrices.clear() 
    
    for sf in squareFootage:
        for num in numCols:
            listSF.append(sf)
            if len(listSF) == 2:
                listOfSF.append(listSF.copy())
                listSF.clear()
        
    # filter out all null prices for graphing ability
    notNull = 0
    avgPricePerBedNotNull = []
    for avgPrices in avgPricePerBedroom:
        if avgPrices is not np.nan:
            notNull = notNull + 1
            avgPricePerBedNotNull.append(float(avgPrices))
    
    # filter out all null prices for graphing ability        
    notNullPrice = 0
    avgPriceList = []
    for avgPrices in prices:
        if avgPrices is not np.nan:
            notNullPrice = notNullPrice + 1
            avgPriceList.append(float(avgPrices))
       
    #Removing outliers for prices histogram
    mean = np.mean(avgPriceList)
    sd = np.std(avgPriceList)
    final_prices = [x for x in prices if (x > mean - 2 * sd)]
    final_prices = [x for x in final_prices if (x < mean + 2 * sd)]
    
    #Plot of all average prices per zipcode
    avgAllPrices_df = pd.DataFrame(final_prices)
    avgAllPrices_df.hist(bins=15, color='skyblue')
    plt.title("Distribution of Rental Prices for " + str(zipcode) + " (Removing Outliers)")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.grid(False)
    plt.show()
    
    #Find median price, bedrooms, and square footage
    medianPrice = np.median(avgPriceList)
#    medianRooms = np.median(nonNullBedroomsList)
#    medianSF = np.median(nonNullSFList)
    avgPrice = np.mean(avgPriceList)
    avgRooms = np.mean(nonNullBedroomsList)
#    avgSF = np.mean(nonNullSFList)
    
    buyDict = zillow.zillowDataDictBedrooms()
    
    medSale1Bed = buyDict[str(zipcode)]['medSale1Bed']
    medSale2Bed = buyDict[str(zipcode)]['medSale2Bed']
    medSale3Bed = buyDict[str(zipcode)]['medSale3Bed']
    medSale4Bed = buyDict[str(zipcode)]['medSale4Bed']
    medSale5pBed = buyDict[str(zipcode)]['medSale5pBed']
    
#    print(medSale1Bed)
#    print(medSale2Bed)
#    print(medSale3Bed)
#    print(medSale4Bed)
#    print(medSale5pBed)
    

#    print("Median Square Footage: " + str(round(medianSF,2)))
#    print("Average Square Footage: " + str(round(avgSF,2)))
#    print("Median bedrooms: " + str(round(medianRooms,2)))
#    print("Average bedrooms: " + str(round(avgRooms,2)))
#    print("Median rent price: " + str(round(medianPrice,2)))
#    print("Average rent price: " + str(round(avgPrice,2)))
    
    #Using typical 30 year fixed mortgage, 5% interest rate, $3,000 Annual Real Estate Taxes, $1500 annual insurance, $1675 annual PMI
    interestRate = 5
    term = 30
    monthlyPropTaxes = 250
    monthlyInsurance = 125
    monthlyPMI = 139.67
    
    #Printing monthly payments for each size home
    monthlyPMT1Bed = float(((float(medSale1Bed)*(float(interestRate)/100/12))/(1-
                            ((1+(float(interestRate)/100/12))**(float(term)*(-12))))))+monthlyPropTaxes+monthlyInsurance+monthlyPMI
#    print("Median 1 Bed PMT: " + str(round(monthlyPMT1Bed,2)))
    monthlyPMT2Bed = float(((float(medSale2Bed)*(float(interestRate)/100/12))/(1-
                            ((1+(float(interestRate)/100/12))**(float(term)*(-12))))))+monthlyPropTaxes+monthlyInsurance+monthlyPMI
#    print("Median 2 Bed PMT: " + str(round(monthlyPMT2Bed,2)))
    monthlyPMT3Bed = float(((float(medSale3Bed)*(float(interestRate)/100/12))/(1-
                            ((1+(float(interestRate)/100/12))**(float(term)*(-12))))))+monthlyPropTaxes+monthlyInsurance+monthlyPMI
#    print("Median 3 Bed PMT: " + str(round(monthlyPMT3Bed,2)))
    monthlyPMT4Bed = float(((float(medSale4Bed)*(float(interestRate)/100/12))/(1-
                            ((1+(float(interestRate)/100/12))**(float(term)*(-12))))))+monthlyPropTaxes+monthlyInsurance+monthlyPMI
#    print("Median 4 Bed PMT: " + str(round(monthlyPMT4Bed,2)))
    monthlyPMT5pBed = float(((float(medSale5pBed)*(float(interestRate)/100/12))/(1-
                             ((1+(float(interestRate)/100/12))**(float(term)*(-12))))))+monthlyPropTaxes+monthlyInsurance+monthlyPMI
#    print("Median 5+ Bed PMT: " + str(round(monthlyPMT5pBed,2)))
    
    #Combining list of all prices (averages and medians)
    paymentList = [avgPrice, medianPrice, monthlyPMT1Bed, monthlyPMT2Bed, monthlyPMT3Bed, monthlyPMT4Bed, monthlyPMT5pBed]
    
    #Plot showing comparison between renting and buying
    payList_df = pd.DataFrame(paymentList)
    patch = payList_df.plot(kind = 'bar', color = 'navy')
    plt.ylabel('Price')
    plt.xticks(np.arange(7), ('Avg Rent', 'Med Rent', 'Med 1 Bed Buy', 'Med 2 Bed Buy', 'Med 3 Bed Buy', 'Med 4 Bed Buy', 'Med 5+ Bed Buy'))
    plt.title("Rent vs Buy Comparison in Zip Code " + str(zipcode) + "\nAvgerage Number of Bedrooms for Rental is " + str(round(avgRooms, 2)))
    bar_value_to_label = avgPrice
    min_distance = min(paymentList)  # initialize min_distance with infinity
    index_of_bar_to_label = 0
    for i, rectangle in enumerate(patch.patches):  # iterate over every bar
        tmp = abs(  # tmp = distance from middle of the bar to bar_value_to_label
            (rectangle.get_x() +
                (rectangle.get_width() * (1 / 2))) - bar_value_to_label)
        if tmp < min_distance:  # searching for the bar with x cordinate
                                # closest to bar_value_to_label
            min_distance = tmp
            index_of_bar_to_label = i
    patch.patches[index_of_bar_to_label].set_color('skyblue')
    
    plt.show()
    #Received above code help from https://stackoverflow.com/questions/35890738/change-color-of-selected-matplotlib-histogram-bin-bar-given-its-value/35894710 

def main():
    df = getData()
    getOverallAggregateData()
    getZipcodePlot()

if __name__ == '__main__':
    main()

    
    