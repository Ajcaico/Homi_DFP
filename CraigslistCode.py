import pandas as pd
from bs4 import BeautifulSoup as bs4
import requests
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat

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
            #apartmentCount += 1
            
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
                    
        zipDictionary[zipcode] = {'NumApartments': aptCount,
                'RentalAptPrices': np.sum(zipPrices)/len(zipPrices), 
                'RentalAptNumBedrooms': np.sum(nonNullBedroomsList)/len(nonNullBedroomsList),
                'RentalAptSquareFeet': np.sum(nonNullSFList)/len(nonNullSFList),
                'RentalPricePerBedroom': np.sum(zipPrices)/np.sum(nonNullBedroomsList)}
        
#        print('Number of Apartment Listings: ', str(aptCount))
#        print('Average price of Apartment Listings: ', "{0:.2f}".format(np.sum(zipPrices)/len(zipPrices)))
#        print('Average square footage of Apartment Listings: ', "{0:.2f}".format(np.sum(nonNullSFList)/len(nonNullSFList)))
#        print('Average number of bedrooms: ', "{0:.2f}".format(np.sum(nonNullBedroomsList)/len(nonNullBedroomsList)))
#        print('Average price per bedroom: ', "{0:.2f}".format(np.sum(zipPrices)/np.sum(nonNullBedroomsList)))
        
        #clear all zip code specific lists to then fill with the new zip code that is next in the list
        avgPricePerBedroom.append(np.sum(zipPrices)/np.sum(nonNullBedroomsList))
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
    
#Finding all non null price values
def getOverallAggregateData():
    pricesNotNull = 0
    listPricesNotNull = []
    for price in prices:
        if price is not np.nan:
            pricesNotNull = pricesNotNull + 1
            listPricesNotNull.append(float(price))
            
    #Finding all non null bedroom values        
    bedroomsNotNull = 0
    listBedroomsNotNull = []
    for beds in bedrooms:
        if beds is not np.nan:   
            bedroomsNotNull = bedroomsNotNull + 1
            listBedroomsNotNull.append(float(beds))
            
    #Finding all non null square footage values        
    sfNotNull = 0
    listSFNotNull = []
    for sf in squareFootage:
        if sf is not np.nan:  
            sfNotNull = sfNotNull + 1
            listSFNotNull.append(float(sf))
    
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
    avgAllPrices_df.hist(bins = 30, color = 'skyblue')
    plt.title("Distribution of Average Rental Prices\nAllegheny County Zip Codes Listings (Removing Outliers)")
    plt.show()
    
    #Plot of all average prices per bedroom per zip code
    avgPrice_df = pd.DataFrame(avgPricePerBedNotNull)
    avgPrice_df.hist(bins=50, color = 'navy')
    plt.title("Distribution of Average Prices Per Bedroom")
    plt.show()
  
#    print('******************************************************')        
#    print('Total Number of Apartment Listings: ', df['NumApartments'].sum())
#    print('Average price of all listings: ', "{0:.2f}".format(np.sum(listPricesNotNull)/pricesNotNull))
#    print('Average number of bedrooms per listing: ', "{0:.2f}".format(np.sum(listBedroomsNotNull)/bedroomsNotNull))
#    print('Average square footage per listing: ' "{0:.2f}".format(np.sum(listSFNotNull)/sfNotNull))
#    print('Average price per bedroom: ', "{0:.2f}".format(np.sum(listPricesNotNull)/np.sum(listBedroomsNotNull)))
#    print('******************************************************')


def main():
    df = getData()
    getOverallAggregateData()

if __name__ == '__main__':
    main()

    
    