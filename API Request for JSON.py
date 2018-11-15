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
"""
category_list = ['American', 'Asian', 'Latin', 'Indian', 'Bar', 'Grocery']
zipcode_list = [15201, 15202, 15204, 15205, 15208, 15210, 15203, 15206, 15207, 15209, 15211, 15214, 15216, 15212, 
            15213, 15215, 15217, 15218, 15219, 15220, 15222, 15223, 15224, 15226, 15221, 15225, 15227, 15229,
            15230, 15231, 15233, 15238, 15228, 15232, 15234, 15235, 15236, 15237, 15239, 15240, 15242, 15243, 
            15253, 15254, 15241, 15244, 15250, 15251, 15252, 15255, 15257, 15258, 15259, 15260, 15261, 15262, 
            15264, 15270, 15272, 15274, 15279, 15281, 15289, 15290, 15295, 15265, 15267, 15268, 15275, 15276, 
            15277, 15278, 15282, 15283, 15286]
"""
zipcode_list = [15235, 15237, 15232]
category_list = ['American', 'Asian']


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

#    print(u'{0} businesses found, querying business info ' \
#        'for the top result "{1}" ...'.format(
#            len(businesses), business_id))
    response = get_business(API_KEY, business_id)
#   print(u'Result for business "{0}" found:'.format(business_id))
#    pprint.pprint(response, indent=2)

    return businesses

def addResultsToList(businesses, location, category):
    
    for i in businesses:
       value = i.get('location')
       if (int(value.get('zip_code')) == int(location)):
          result = [value.get('zip_code'), category, i.get('name'), i.get('rating'), i.get('review_count') ]
          result_list.append(result)
       
    for i in range(0, len(result_list)):
        i= i +1


def resultsToDataFrame():
    
    col_names = ['Zip Code', 'Category', 'Name', 'Rating', 'Reviews']
    df = pd.DataFrame(result_list, columns = col_names)
    df = df.set_index('Zip Code')
    print(df)
    
    print(df.groupby(['Zip Code', 'Category']).mean())
        
    
    
    
def calculateAverage():
    for zipcode in zipcode_list:
        count = 0; sumRating = 0; avgRating = 0; sumReviews = 0; resultSummaryList = []
        for category in category_list:
            for result in result_list:
                if (int(result[0]) == zipcode and result[1] == category):
                    count += 1
                    sumRating = sumRating + float(result[3])
                    sumReviews = sumReviews + int(result[4])
            if (count == 0):
                avgRating = 0
            else:
                avgRating = sumRating / count
            resultSummaryList.extend([category, count, avgRating, sumReviews])
            zip_summary[zipcode] = resultSummaryList
            print('Zipcode: ' + str(zipcode) + ' Category: ' + resultSummaryList[0], 'Count: ' + str(resultSummaryList[1]) + ', Avg Rating: ' + "%.2f" % resultSummaryList[2] + ', Total Reviews: ' + str(resultSummaryList[3]))
       

 
def main():
    
    for category in category_list:
        for zipcode in zipcode_list:
            searchZip = str(zipcode)    
            parser = argparse.ArgumentParser()
            parser.add_argument('-q', '--term', dest='term', default=category,
                            type=str, help='Search term (default: %(default)s)')
            parser.add_argument('-l', '--location', dest='location',
                            default=searchZip, type=str,
                            help='Search location (default: %(default)s)')
            input_values = parser.parse_args()
            addResultsToList(query_api(input_values.term, input_values.location), zipcode, category)
    resultsToDataFrame()    
   # print(len(result_list))
   #calculateAverage()    
    
if __name__ == '__main__':
    main()