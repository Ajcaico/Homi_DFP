import pandas as pd
from bs4 import BeautifulSoup as bs4
import requests
import numpy as np
import matplotlib.pyplot as plt

apartmentCount = 0
prices = []
squareFootage = []
bedrooms = []
titles = []
neighborhoods = []
zipPrices = []
zipSquareFootage = []
zipBedrooms = []
zipTitles = []
zipNeighborhoods = []
allDictionary = {}
zipDictionary = {}
   
def find_size_and_brs(size):
    split = size.strip().strip('/- ').split(' -\n ')
    if len(split) == 2:
        n_brs = split[0].replace('br', '')
        this_size = split[1].replace('ft2', '')
        bedrooms.append(n_brs)
        squareFootage.append(this_size)
    elif 'br' in split[0]:
        # It's the n_bedrooms
        n_brs = split[0].replace('br', '')
        bedrooms.append(n_brs)
        this_size = np.nan
        squareFootage.append(this_size)
    elif 'ft2' in split[0]:
        # It's the size
        this_size = split[0].replace('ft2', '')
        squareFootage.append(this_size)
        n_brs = np.nan
        bedrooms.append(n_brs)
    return float(this_size), float(n_brs)

def find_prices(results):
    prices = []
    for rw in results:
        price = rw.find('span', attrs={'class': 'result-price'})
        if price is not None:
            price = float(price.text.strip('$'))
        else:
            price = np.nan
        prices.append(price)
    return prices

def find_neighborhoods(results):
    neighborhoods = []
    for hoods in results:
        neighborhood = hoods.find('span', {'class': 'result-hood'})
        if neighborhood is not None:
            neighborhood = neighborhood.text.strip().strip('(').strip(')')
        else:
            neighborhood = np.nan
        neighborhoods.append(neighborhood)
    return neighborhoods

def getData():
    url_base = 'https://pittsburgh.craigslist.org/d/apts-housing-for-rent/search/apa'
    zipcodes = [15201, 15202, 15204, 15205, 15208, 15210, 15203, 15206, 15207, 15209, 15211, 15214, 15216, 15212, 
                15213, 15215, 15217, 15218, 15219, 15220, 15222, 15223, 15224, 15226, 15221, 15225, 15227, 15229,
                15230, 15231, 15233, 15238, 15228, 15232, 15234, 15235, 15236, 15237, 15239, 15240, 15242, 15243, 
                15253, 15254, 15241, 15244, 15250, 15251, 15252, 15255, 15257, 15258, 15259, 15260, 15261, 15262, 
                15264, 15270, 15272, 15274, 15279, 15281, 15289, 15290, 15295, 15265, 15267, 15268, 15275, 15276, 
                15277, 15278, 15282, 15283, 15286]
    for zipcode in zipcodes:
        params = dict(postal=zipcode)
        
        rsp = requests.get(url_base, params=params)
        
        # BS4 can quickly parse our text, make sure to tell it that you're giving html
        html = bs4(rsp.text, 'html.parser')
        
        # BS makes it easy to look through a document
        print('***************' + str(zipcode) + '*******************')
        
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
            #apartmentCount += 1
                            
            nonNullBedrooms = 0
            nonNullBedroomsList = []
            for beds in zipBedrooms:
                if beds is not np.nan:   
                    nonNullBedrooms = nonNullBedrooms + 1
                    nonNullBedroomsList.append(float(beds))
            
            nonNullSF = 0
            nonNullSFList = []
            for sf in zipSquareFootage:
                if sf is not np.nan:  
                    nonNullSF = nonNullSF + 1
                    nonNullSFList.append(float(sf))
                    
        print('Number of Apartment Listings: ', str(aptCount))
        print('Average price of Apartment Listings: ', "{0:.2f}".format(np.sum(zipPrices)/len(zipPrices)))
        print('Average square footage of Apartment Listings: ', "{0:.2f}".format(np.sum(nonNullSFList)/len(nonNullSFList)))
        print('Average number of bedrooms: ', "{0:.2f}".format(np.sum(nonNullBedroomsList)/len(nonNullBedroomsList)))
        
        zipDictionary[zipcode] = {'NumApartments': aptCount,
                'AptPrices': np.sum(zipPrices)/len(zipPrices), 
                'AptNumBedrooms': np.sum(nonNullBedroomsList)/len(nonNullBedroomsList),
                'AptSquareFeet': np.sum(nonNullSFList)/len(nonNullSFList)}
            
        zipPrices.clear()
        zipSquareFootage.clear()
        zipNeighborhoods.clear()
        zipBedrooms.clear()
        nonNullSFList.clear()
        nonNullBedroomsList.clear()
        
    df = pd.DataFrame(zipDictionary).T
    df.to_excel("AggregateCraigslistData.xlsx")
    return df
    #zipDictionary.clear()
    #allDictionary[zipcode] = {zipDictionary}
    #print('\n'.join([str(i) for i in [this_size, n_brs, this_time, this_price, this_title, this_neighborhood]]))

#Finding all non null price values
def getOverallAggregateData(df):
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
    
    print('******************************************************')        
    print('Total Number of Apartment Listings: ', df['NumApartments'].sum())
    print('Average price of all listings: ', "{0:.2f}".format(np.sum(listPricesNotNull)/pricesNotNull))
    print('Average number of bedrooms per listing: ', "{0:.2f}".format(np.sum(listBedroomsNotNull)/bedroomsNotNull))
    print('Average square footage per listing: ' "{0:.2f}".format(np.sum(listSFNotNull)/sfNotNull))
    print('******************************************************')

def main():
    df = getData()
    getOverallAggregateData(df)

if __name__ == '__main__':
    main()

    
    