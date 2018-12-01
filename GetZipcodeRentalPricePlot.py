import pandas as pd
from bs4 import BeautifulSoup as bs4
import requests
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

apartmentCount = 0
prices = []
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
        
        nonNullSF = 0
        nonNullSFList = []
        for sf in zipSquareFootage:
            if sf is not np.nan:  
                nonNullSF = nonNullSF + 1
                nonNullSFList.append(float(sf))
        
        #print(len(zipPrices))
        #print(len(zipBedrooms))
        #plt.style.use('seaborn-white')
    
    plt.title("Distribution of Prices in Zip Code " + str(zipcode))
    plt.xlabel("Price")
    plt.ylabel("Number of Listings")
    plt.hist(zipPrices, color = 'r') 
    plt.show()
    
    plt.title("Distribution of Prices in Zip Code " + str(zipcode))
    plt.xlabel("Price")
    plt.ylabel("Number of Listings")
    plt.hist(zipPrices, color = 'r') 
    plt.show()
    
    plt.title("Scatter Plot of Square Footage and Number of Bedrooms")
    plt.xlabel("Number of Bedrooms")
    plt.ylabel("Square Footage")
    plt.scatter(zipBedrooms, zipSquareFootage, alpha=0.5)
    plt.show()
    
    np.random.seed(19680801)

    n_bins = 15
    x = zipPrices
    
    fig, axes = plt.subplots(nrows=2, ncols=2)
    ax0, ax1, ax2, ax3 = axes.flatten()
    
    colors = ['red']
    ax0.hist(x, histtype='bar', color=colors, label=colors)
    ax0.set_title("Prices in Zip Code " + str(zipcode))
    
    ax1.hist(x, n_bins, histtype='bar', stacked=True)
    ax1.set_title("Prices in Zip Code " + str(zipcode))
    
    x_multi1 = [n for n in [zipPrices, zipSquareFootage]]
    ax2.hist(x_multi1, histtype='bar')
    ax2.set_title("Prices and Square Footage in Zip Code " + str(zipcode))
    
    # Make a multiple-histogram of data-sets with different length.
    x_multi = [n for n in [zipPrices, zipSquareFootage, zipBedrooms]]
    
    ax3.hist(x_multi, histtype='bar')
    ax3.set_title('Square Footage and Price')
    
    fig.tight_layout()
    plt.show()
    
    # Fixing random state for reproducibility
    #np.random.seed(19680801)
        
    N = len(zipSquareFootage)
    x = zipSquareFootage
    y = zipBedrooms
    colors = np.random.rand(N)
    area = [n for n in [zipPrices]]
    plt.xlabel("Square Footage")
    plt.ylabel("Number of Bedrooms")
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.show()
    
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
    
    colors = zipPrices
    plt.title("Scatter Plot of Square Footage and Price")
    plt.xlabel("Price")
    plt.ylabel("Square Footage")
    plt.scatter(zipPrices, zipSquareFootage, c=colors, alpha=0.5, cmap='viridis')
    plt.show()
    
    plt.title("Scatter Plot of Number of Bedrooms and Price")
    plt.xlabel("Price")
    plt.ylabel("Number of Bedrooms")
    plt.scatter(zipPrices, zipBedrooms, c=colors, alpha=0.5, cmap='viridis')
    plt.show()
     
    N = len(zipSquareFootage)
    x = [n for n in [zipBedrooms]]
    y = [n for n in [zipPrices]]
    colors = [n for n in [zipBedrooms]]
    area = [n for n in [zipSquareFootage]]
    plt.title("Scatter Plot of Prices, Square Footage, and Num Bedrooms")
    plt.xlabel("Bedrooms")
    plt.ylabel("Price")
    plt.scatter(x, y, s=area, c=colors, alpha=0.4, cmap='gist_stern')
    plt.show()
    
    N = len(zipSquareFootage)
    x = [n for n in [zipSquareFootage]]
    y = [n for n in [zipPrices]]
    colors = [n for n in [zipBedrooms]]
    area = [n for n in [zipBedrooms]]
    plt.title("Scatter Plot of Prices, Square Footage, and Num Bedrooms")
    plt.xlabel("Square Footage")
    plt.ylabel("Price")
    plt.scatter(x, y, c=colors, alpha=0.5, cmap='viridis')
    plt.show()
    
    N = len(zipSquareFootage)
    x = [n for n in [zipSquareFootage]]
    y = [n for n in [zipBedrooms]]
    colors = [n for n in [zipBedrooms]]
    area = [n for n in [zipPrices]]
    plt.title("Scatter Plot of Prices, Square Footage, and Num Bedrooms")
    plt.xlabel("Square Footage")
    plt.ylabel("Bedrooms")
    plt.scatter(x, y, s=area, c=colors, alpha=0.75, cmap='nipy_spectral')
    #plt.legend(bedroomGroups)
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
    
    X = np.array(listOfPrices)
    Y = np.array(listOfSF)
    Z = np.array(listOfBedrooms)
    
    ##Surface plot
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('Prices')
    ax.set_ylabel('Square Footage')
    ax.set_zlabel('Number of Bedrooms')
    #ax.plot_surface(X, Y, Z, cmap='viridis')
    #Axes3D.plot_surface(ax, X, Y, Z, cmap='coolwarm')
   # plt.show()
    
    ##Wireframe plot
    fig2 = plt.figure()
    ax2 = plt.axes(projection='3d')
    ax2.set_xlabel('Prices')
    ax2.set_ylabel('Square Footage')
    ax2.set_zlabel('Number of Bedrooms')
    #Axes3D.plot_wireframe(ax2, X, Y, Z, cmap='plasma_r')
    #plt.show()
    
    
        
def main():
    getZipcodePlot(15237)
         
if __name__ == '__main__':
    main()               
                    
            