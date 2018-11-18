# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 19:02:49 2018

@author: ajcai
"""
from __future__ import print_function
import argparse
import json
import pprint
import requests
import sys
import urllib
from urllib.parse import quote
from urllib.parse import urlencode
import numpy as np
import pandas as pd


API_KEY= 'ag6RO1gG16UhJzSO-88XdFrpzaNgOpUwaxOkkXco4QvyOXyAdkyih7yGiq5iIGCbZ6rsSPJedkakFpeX0rZGeUfAr7zuWsXkwT6XCZGYSKi2ntPRsJkV00anQCjmW3Yx' 

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
##DEFAULT_TERM = 'american'
##DEFAULT_LOCATION = '15232'
SEARCH_LIMIT = 50

zip_summary = {}
result_list = []


category_list = ['American', 'Asian', 'Latin', 'Indian', 'Bar', 'Grocery']
'''
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
'''

zipcode_list = [15108]
#category_list = ['American', 'Asian']


def request(host, path, api_key, url_params=None):

    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()

def search(api_key, term, location):

    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):

    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)

def query_api(term, location):

    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)
    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return
    
    business_id = businesses[0]['id']
    response = get_business(API_KEY, business_id)

    return businesses

def addResultsToList(businesses, location, category):
    
    
    for i in businesses:
       value = i.get('location')

       if value.get('zip_code') == '':
           businessZip = int(location)
       else:
           businessZip = int(value.get('zip_code')) 

       if (businessZip == int(location)):
          result = [businessZip, category, i.get('name'), i.get('rating'), i.get('review_count') ]
          result_list.append(result)
       

def resultsToDataFrame():
    
    col_names = ['zipcode', 'category', 'name', 'rating', 'review']
    df = pd.DataFrame(result_list, columns = col_names)
    df.head()
    
    #print(df.groupby(['ZipCode', 'Category']).mean())
        
    return df
    
    
def getSummaryData(df):
  
    summaryResultList = []
    
    for zipcode in zipcode_list:
        
        #summary across all restaurant categories in a zip
        df_filteredAll = df[str(df.zipcode) == str(zipcode)]
        count = df_filteredAll['rating'].count()
        ratingAverage = df_filteredAll['rating'].mean()
        reviewCountAverage = df_filteredAll['review'].mean()
        summaryResult = [zipcode, 'All', count, ratingAverage, reviewCountAverage]
        summaryResultList.append(summaryResult)
        
        #summary for each category within a zipcode
        for category in category_list:
            df_filteredCategories = df[(df.category == category) & (df.zipcode == str(zipcode))]
            count = df_filteredCategories['rating'].count()
            ratingAverage = df_filteredCategories['rating'].mean()
            reviewCountAverage = df_filteredCategories['review'].mean()
            summaryResult = [zipcode, category, count, ratingAverage, reviewCountAverage]
            summaryResultList.append(summaryResult)
            
    
    col_names = ['zipcode', 'category', 'count', 'average_rating', 'average_review_count']
    df_summary = pd.DataFrame(summaryResultList, columns = col_names)
    
    return df_summary
 
    

def getData():
    
    for zipcode in zipcode_list:
        for category in category_list:
                searchZip = str(zipcode)    
                parser = argparse.ArgumentParser()
                parser.add_argument('-q', '--term', dest='term', default=category,
                                type=str, help='Search term (default: %(default)s)')
                parser.add_argument('-l', '--location', dest='location',
                                default=searchZip, type=str,
                                help='Search location (default: %(default)s)')
                input_values = parser.parse_args()
                addResultsToList(query_api(input_values.term, input_values.location), zipcode, category)
    
    return resultsToDataFrame()
        

def main():
   
    df = getData()
    df_summary = getSummaryData(df)
    
    print('Printing all data')
    print(df)
    
    print('Printing summary data')
    print(df_summary)
    

    
if __name__ == '__main__':
    main()