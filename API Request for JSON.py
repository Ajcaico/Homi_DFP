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


API_KEY= 'ag6RO1gG16UhJzSO-88XdFrpzaNgOpUwaxOkkXco4QvyOXyAdkyih7yGiq5iIGCbZ6rsSPJedkakFpeX0rZGeUfAr7zuWsXkwT6XCZGYSKi2ntPRsJkV00anQCjmW3Yx' 

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
DEFAULT_TERM = 'american'
DEFAULT_LOCATION = '15232'
SEARCH_LIMIT = 50

zip_summary = {}
result_list = []
#category_list = ['American', 'Asian', 'Latin', 'Indian', 'Bar', 'Grocery']
#zipcode_list = [15237, 15235, 15221, 15213, 15236, 15206, 15227, 15212, 15217, 15210, 15216, 15205, 15239, 15241, 15122]
zipcode_list = [15235, 15237, 15221, 15213, 15206, 15227, 15212]
category_list = ['American']


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

def addResultsToList(businesses, DEFAULT_LOCATION):
    
    ##Add responses to a list / dict

    for i in businesses:
       value = i.get('location')
       if (int(value.get('zip_code')) == int(DEFAULT_LOCATION)):
          result = [value.get('zip_code'), i.get('name'), i.get('rating'), i.get('review_count') ]
          result_list.append(result)
       
    for i in range(0, len(result_list)):
       # print(result_list[i])
        i = i +1

 #   for key, value in businesses[0].items():
 #      print(key), print(type(value))
    
    
 
def calculateAverage():
    for zipcode in zipcode_list:
        zipCount = 0
        sumRating = 0
        avgRating = 0
        sumReviews = 0
        resultSummaryList = []
        for result in result_list:
            if (int(result[0]) == zipcode):
                zipCount = zipCount + 1
                sumRating = sumRating + float(result[2])
                sumReviews = sumReviews + int(result[3])
        avgRating = sumRating / zipCount
        resultSummaryList.extend([zipCount, avgRating, sumReviews])
        zip_summary[zipcode] = resultSummaryList
    
        print('Zipcode: ' + str(zipcode) + ', # of Restaurants: ' + str(zipCount) + ', Avg Rating: ' + "%.2f" % avgRating + ', Total Reviews: ' + str(sumReviews))
   # print(zip_summary)

    
    
 
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
        
            addResultsToList(query_api(input_values.term, input_values.location), zipcode)
            
    print(len(result_list))
    calculateAverage()    
    
if __name__ == '__main__':
    main()