# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 19:02:49 2018

@author: ajcai
"""
from __future__ import print_function
import argparse
import requests
from urllib.parse import quote
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches


#Sends Yelp API requests, which returns JSONs for each business that meets the search criteria
#Retrieves necessary data from JSONs and creates a dataframe, which is written to excel
#Creates graph based data cleaned data from Yelp responses

#Credit: Yelp API functions (request, search, get_business, and query_api) taken from Yelp developer github. 
#These functions were copied and adjusted to fit the needs for this program
#https://github.com/Yelp/yelp-fusion/tree/master/fusion/python


#Yelp API keys required for sending requests, 5,000 limit per day. Switch to other API_KEY if limit is reached
API_KEY= 'ag6RO1gG16UhJzSO-88XdFrpzaNgOpUwaxOkkXco4QvyOXyAdkyih7yGiq5iIGCbZ6rsSPJedkakFpeX0rZGeUfAr7zuWsXkwT6XCZGYSKi2ntPRsJkV00anQCjmW3Yx' 
#API_KEY = 'Zuso4ntCFv_QaB4i4a6K4j0R0meRcdJ6Lum873qy36Y6gN2diK9iCLlnqFX-GYtWH5fSN-I8NUFYhTyTcx8PhamgxYkCSD4MkmJ4lzTasDn99cWZjV9f9bgLFHD0W3Yx'


# API constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/' 
SEARCH_LIMIT = 40

zip_summary = {}
result_list = []

#Search terms
category_list = ['American', 'Asian', 'Latin', 'Indian', 'Bar', 'Grocery']
zipcode_list = ['15101','15003','15005','15006','15007','15102','15014','15104','15015','15017',
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


#Method to generate API requests and create spreadsheets with data generated
def getData():
    
    print('Starting Yelp API requests')
    totalRequests = len(zipcode_list) * len(category_list)
    print('Approximately 3-5 minutes for each 100 API requests')
    print(str(totalRequests) + ' API requests will be made')
    
    count = 0
    for zipcode in zipcode_list:
        for category in category_list:
            count += 1
            print('Making request number: ' + str(count))
            searchZip = str(zipcode)    
            parser = argparse.ArgumentParser()
            parser.add_argument('-q', '--term', dest='term', default=category,
                            type=str, help='Search term (default: %(default)s)')
            parser.add_argument('-l', '--location', dest='location',
                            default=searchZip, type=str,
                            help='Search location (default: %(default)s)')
            input_values = parser.parse_args()
            addResultsToList(query_api(input_values.term, input_values.location), zipcode, category)
    
    print('API Requests Complete')
    df = resultsToDataFrame()
    summaryDict = getSummaryData(df)
    df_summaryTop = summaryDict['topSummary']
    df_summary = summaryDict['summary']
    print( df_summary.head())
    print(df_summaryTop.head())
    calculateRating(df, df_summary)
    
    return df_summaryTop


def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()


def search(api_key, term, location):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)

def query_api(term, location):
    response = search(API_KEY, term, location)
    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return
    
    business_id = businesses[0]['id']
    response = get_business(API_KEY, business_id)

    return businesses

#Go through JSONs returned be API and pull out data needed into a list of lists
def addResultsToList(businesses, location, category):
    
    if businesses is not None:
        for i in businesses:
           value = i.get('location')
    
           if value.get('zip_code') == '':
               businessZip = location
           else:
               businessZip = value.get('zip_code')
    
           if (int(businessZip) == int(location)):
              result = [businessZip, category, i.get('name'), i.get('rating'), i.get('review_count') ]
              result_list.append(result)
           
#convert lists to pandas data frame
def resultsToDataFrame():
    
    col_names = ['zipcode', 'category', 'name', 'rating', 'review']
    df = pd.DataFrame(result_list, columns = col_names)
    df.head()
    
    df.to_excel('AllYelpData.xlsx')
    print('AllYelpData.xlsx updated')
    return df
    

#get summary level data for raw data acorss zips
def getSummaryData(df):
  
    summaryResultList = []   
    df['zipcode'] = (df['zipcode']).astype(int)
    df['rating_reviews'] = df['rating']*df['review'] 
    

    for zipcode in zipcode_list:
        
        #summary across all restaurant categories in a zip
        df_filteredAll = df[(df.category != 'Bar') & (df.category != 'Grocery') & (df.zipcode == int(zipcode))] 
        count = df_filteredAll['rating'].count()
        ratingAverage = df_filteredAll['rating_reviews'].sum() / df_filteredAll['review'].sum() 
        reviewCountAverage = df_filteredAll['review'].mean()
        summaryResult = [str(zipcode), 'All Restaurants', count, ratingAverage, reviewCountAverage]
        summaryResultList.append(summaryResult)
        
        #summary for each category within a zipcode
        for category in category_list:
            df_filteredCategories = df[(df.category == category) & (df.zipcode == int(zipcode))]
            count = df_filteredCategories['rating'].count()
            ratingAverage = df_filteredCategories['rating'].mean()
            reviewCountAverage = df_filteredCategories['review'].mean()
            summaryResult = [str(zipcode), category, count, ratingAverage, reviewCountAverage]
            summaryResultList.append(summaryResult)
            
    col_names = ['zipcode', 'category', 'count', 'average_rating', 'average_review_count']
    df_summary = pd.DataFrame(summaryResultList, columns = col_names)
 
    df_summary.to_excel('YelpSummaryData.xlsx') 
    print('YelpSummaryData.xlsx updated')
    
    df_summaryTop = df_summary[df_summary.category == 'All Restaurants'] # returns 1 row for zipcode for all records cumulative
    df_summaryTop = df_summaryTop.set_index('zipcode')
    df_summaryTop.to_excel('YelpSummaryTop.xlsx') 
    print('YelpSummaryTop.xlsx updated')
    
    return {'topSummary': df_summaryTop, 'summary': df_summary}
 
    
#calculate rating for each zip code
def calculateRating(df, df_summary):
    
    ratings = []
    #determine variety of restaurant types
    for zipcode in zipcode_list:
        df_filtered = df[df.zipcode == int(zipcode)]
        counts = df_filtered['category'].value_counts().to_dict()
        
        highestPercent = 0; restaurantVariety = 0;
        for category, count in counts.items():
            if (category != 'Bar' and category != 'Grocery'):
                totalCount = df_filtered[(df.category != 'Bar') & (df.category != 'Grocery')]['category'].count()
                percent = count / totalCount
                if (percent > highestPercent):
                    highestPercent = percent
                    
            restaurantVariety = 5 - ((highestPercent - 0.25) * 5)
        
        df_summaryFiltered = df_summary[(df_summary.zipcode == zipcode) & ((df_summary.category == 'All Restaurants'))]
        restuarantRating = df_summaryFiltered['average_rating'].mean()
        restaurantCount = df_summaryFiltered['count'].sum()
        restaurantScore = (restaurantVariety + restuarantRating) / 2
        
        df_summaryBar = df_summary[(df_summary.zipcode == zipcode) & ((df_summary.category == 'Bar'))]
        barScore = df_summaryBar['average_rating'].mean() * 0.5 + df_summaryBar['count'].sum() / 10
        barCount = df_summaryBar['count'].sum()
        barRating = df_summaryBar['average_rating'].mean()
        
        df_summaryGrocery = df_summary[(df_summary.zipcode == zipcode) & ((df_summary.category == 'Grocery'))]
        groceryScore = df_summaryGrocery['average_rating'].mean() *0.5 + df_summaryGrocery['count'].sum() / 5
        groceryCount = df_summaryGrocery['count'].sum()
        groceryRating = df_summaryGrocery['average_rating'].mean()
        
        rating = [zipcode, restaurantCount, restaurantVariety, restuarantRating, restaurantScore, barCount, barRating, barScore, groceryCount, groceryRating, groceryScore]
        ratings.append(rating)
       
    col_names = ['zipcode', 'restaurantCount', 'restaurantVariety', 'restuarantRating', 'restaurantScore', 'barCount', 'barRating', 'barScore', 'groceryCount', 'groceryRating', 'groceryScore']
    df_ratings = pd.DataFrame(ratings, columns = col_names)
    df_ratings = df_ratings.set_index('zipcode')
    
    print('YelpOverallRating.xlsx updated')
    df_ratings.to_excel('YelpOverallRating.xlsx') 
    return df_ratings

#returns simple form of ratings to use for weighted calculation
def getOverallRating():
    df_yelpOverallScore = pd.read_excel('YelpOverallRating.xlsx')
    df_yelpOverallScore = df_yelpOverallScore[['zipcode', 'restaurantScore', 'barScore', 'groceryScore']]
    df_yelpOverallScore = df_yelpOverallScore.set_index('zipcode')
    df_yelpOverallScore['restaurantScore'] = df_yelpOverallScore['restaurantScore'].fillna(value=0)
    df_yelpOverallScore['barScore'] = df_yelpOverallScore['barScore'].fillna(value=0)
    df_yelpOverallScore['groceryScore'] = df_yelpOverallScore['groceryScore'].fillna(value=0)
    return df_yelpOverallScore

#Get data from excel after intial API calls have been made, instead of making new API calls
def getDatafromExcel():
    
    df_yelpSummaryTop = pd.read_excel('YelpSummaryTop.xlsx')
    df_yelpSummaryTop = df_yelpSummaryTop.set_index('zipcode')
    
    df_allYelpData = pd.read_excel('AllYelpData.xlsx')
    df_allYelpData = df_allYelpData.set_index('zipcode')
    
    df_yelpSummary = pd.read_excel('YelpSummaryData.xlsx')
    
    df_yelpOverallScore = pd.read_excel('YelpOverallRating.xlsx')
    df_yelpOverallScore = df_yelpOverallScore.set_index('zipcode')
    
    return {'allData' : df_allYelpData, 'summaryData': df_yelpSummary, 'topSummaryData' : df_yelpSummaryTop, 'overallScore' : df_yelpOverallScore}
    
#generate pittsburgh stats charts
def getMacroChart():
    
    dataDict = getDatafromExcel()
    df = dataDict['overallScore']
    df = df.dropna()
    df = df[(df.restaurantCount !=0) & (df.barCount != 0) & (df.groceryCount !=0)]
    df_restaurantCount = df['restaurantCount']
    
    num_bins = 16
    plt.title("Distribution of Restaurants by Zip")
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Frequency")
    plt.hist(df_restaurantCount, num_bins, color = 'skyblue') 
    plt.show()
    
    df_barCount = df['barCount']
    plt.title("Distribution of Bars by Zip")
    plt.xlabel("Number of Bars")
    plt.ylabel("Frequency")
    plt.hist(df_barCount, num_bins, color = 'skyblue') 
    plt.show()
    
    df_groceryCount = df['groceryCount']
    plt.title("Distribution of Grocery Stores by Zip")
    plt.xlabel("Number of Grocery Stores")
    plt.ylabel("Frequency")
    plt.hist(df_groceryCount, num_bins, color = 'skyblue') 
    plt.show()
    
    
#generate zipcode specific charts
def getMicroChart(zipcode):
    
    dataDict = getDatafromExcel()
    df = dataDict['summaryData']
    df_count = df[(df.zipcode == int(zipcode)) & (df.category != 'All Restaurants')]
    df_count = df_count[['category', 'count', 'average_rating']]
    df_count=df_count.set_index('category')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    width = 0.3
    
    df_count['count'].plot(kind='bar', color = 'skyblue', ax=ax, width=width, position = 1, align = 'center')
    df_count['average_rating'].plot(kind='bar', color = 'navy', ax=ax2, width = width, position = 0, align = 'center')
    
    ax.set_ylabel('Count (Light Blue)')
    ax2.set_ylabel('Average Rating (Dark Blue)')
    ax.set_xlabel('Category')
    ax.set_title('Restaurants by Count and Rating for Zip Code: ' + str(zipcode))
    plt.show()

'''    
    key1 = patches.Patch(color = 'skyblue', label = 'Count')
    key2 = patches.Patch (Color = 'navy', label = 'Rating')
    plt.legend(handles = [key1, key2])
 '''   
    

def main():
 
  #  getData()
    getMacroChart()
    getMicroChart('15000')

    
if __name__ == '__main__':
    main()