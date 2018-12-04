import pandas as pd
from bs4 import BeautifulSoup as bs4
import requests
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ZillowHousingDataByZipWithMedianforBedrooms as zillow

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
        col_names = ["Zipcode", "Title", "Neighborhood", "Price", "Square Footage", "Bedrooms", "Posted Time"]
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
        
        #print(len(zipPrices))
        #print(len(zipBedrooms))
        #plt.style.use('seaborn-white')
    #Distribution of Prices
    plt.title("Distribution of Prices in Zip Code " + str(zipcode))
    plt.xlabel("Price")
    plt.ylabel("Number of Listings")
    plt.hist(zipPrices, bins = 20, color = 'skyblue') 
    plt.show()
        
#    plt.title("Scatter Plot of Square Footage and Number of Bedrooms")
#    plt.xlabel("Number of Bedrooms")
#    plt.ylabel("Square Footage")
#    plt.scatter(zipBedrooms, zipSquareFootage, alpha=0.5)
#    plt.show()
    
#    np.random.seed(19680801)
#
#    n_bins = 15
#    x = zipPrices
#    
#    fig, axes = plt.subplots(nrows=2, ncols=2)
#    ax0, ax1, ax2, ax3 = axes.flatten()
#    
#    colors = ['red']
#    ax0.hist(x, histtype='bar', color=colors, label=colors)
#    ax0.set_title("Prices in Zip Code " + str(zipcode))
#    
#    ax1.hist(x, n_bins, histtype='bar', stacked=True)
#    ax1.set_title("Prices in Zip Code " + str(zipcode))
#    
#    x_multi1 = [n for n in [zipPrices, zipSquareFootage]]
#    ax2.hist(x_multi1, histtype='bar')
#    ax2.set_title("Prices and Square Footage in Zip Code " + str(zipcode))
#    
#    # Make a multiple-histogram of data-sets with different length.
#    x_multi = [n for n in [zipPrices, zipSquareFootage, zipBedrooms]]
#    
#    ax3.hist(x_multi, histtype='bar')
#    ax3.set_title('Square Footage and Price')
#    
#    fig.tight_layout()
#    plt.show()
    
    # Fixing random state for reproducibility
    #np.random.seed(19680801)
        
#    N = len(zipSquareFootage)
#    x = zipSquareFootage
#    y = zipBedrooms
#    colors = np.random.rand(N)
#    area = [n for n in [zipPrices]]
#    plt.xlabel("Square Footage")
#    plt.ylabel("Number of Bedrooms")
#    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
#    plt.show()
    
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
            
    #Scatter plots comparing square footage, prices, and number of bedrooms
#    colors = zipPrices
#    plt.title("Scatter Plot of Square Footage and Price")
#    plt.xlabel("Price")
#    plt.ylabel("Square Footage")
#    plt.scatter(zipPrices, zipSquareFootage, c=colors, alpha=0.5, cmap='viridis')
#    plt.show()
    
#    plt.title("Scatter Plot of Number of Bedrooms and Price")
#    plt.xlabel("Price")
#    plt.ylabel("Number of Bedrooms")
#    plt.scatter(zipPrices, zipBedrooms, c=colors, alpha=0.5, cmap='viridis')
#    plt.show()
    
#    N = len(zipSquareFootage)
#    x = [n for n in [zipBedrooms]]
#    y = [n for n in [zipPrices]]
#    colors = [n for n in [zipBedrooms]]
#    area = [n for n in [zipSquareFootage]]
#    plt.title("Scatter Plot of Prices, Square Footage, and Num Bedrooms")
#    plt.xlabel("Bedrooms")
#    plt.ylabel("Price")
#    plt.scatter(x, y, s=area, c=colors, alpha=0.4, cmap='gist_stern')
#    plt.show()
    
    N = len(zipSquareFootage)
    x = [n for n in [zipSquareFootage]]
    y = [n for n in [zipPrices]]
    colors = [n for n in [zipBedrooms]]
    #area = [n for n in [zipBedrooms]]
    plt.title("Scatter Plot of Prices, Square Footage, and Num Bedrooms\n Colors Are Number of Bedrooms from 1 - " + str(max(zipBedrooms)))
    plt.xlabel("Square Footage")
    plt.ylabel("Price")
    plt.scatter(x, y, c=colors, alpha=0.5, cmap='viridis')
    plt.show()

#    N = len(zipSquareFootage)
#    x = [n for n in [zipSquareFootage]]
#    y = [n for n in [zipBedrooms]]
#    colors = [n for n in [zipBedrooms]]
#    area = [n for n in [zipPrices]]
#    plt.title("Scatter Plot of Prices, Square Footage, and Num Bedrooms")
#    plt.xlabel("Square Footage")
#    plt.ylabel("Bedrooms")
#    plt.scatter(x, y, s=area, c=colors, alpha=0.75, cmap='nipy_spectral')
#    #plt.legend(bedroomGroups)
#    plt.show()
        
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
    plt.show()
    
    #Plot of all average prices per bedroom per zip code
#    avgPrice_df = pd.DataFrame(avgPricePerBedNotNull)
#    avgPrice_df.hist(bins=15, color='navy')
#    plt.title("Distribution of Average Rental Prices Per Bedroom in Zip Code " + str(zipcode))
#    plt.show()
    
    #Find median price, bedrooms, and square footage
    medianPrice = np.median(avgPriceList)
    medianRooms = np.median(nonNullBedroomsList)
    medianSF = np.median(nonNullSFList)
    avgPrice = np.mean(avgPriceList)
    avgRooms = np.mean(nonNullBedroomsList)
    avgSF = np.mean(nonNullSFList)
    
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
        if tmp < min_distance:  # we are searching for the bar with x cordinate
                                # closest to bar_value_to_label
            min_distance = tmp
            index_of_bar_to_label = i
    patch.patches[index_of_bar_to_label].set_color('skyblue')
        
    plt.show()
    #Received above code help from https://stackoverflow.com/questions/35890738/change-color-of-selected-matplotlib-histogram-bin-bar-given-its-value/35894710 


def main():
    getZipcodePlot(zipcode)
         
if __name__ == '__main__':
    main()               
                    
            