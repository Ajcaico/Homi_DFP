# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 00:42:46 2018

@author: ajcai
"""
##import each .py file
import pandas as pd
import YelpDataAPI as yd
import CraigslistCode as craig
import ZillowHousingDataByZip as zillow



def getData(): 
#Call functions from each .py file to get data
    
    #df_yelp = yd.getData() #returns all yelp data, 1 row for each business
    #df_yelpSummary = yd.getSummaryData(df_yelp) #returns summary with 1 row for each zip and category
    #df_yelpOverallRating = yd.calculateRating(df_yelp, df_yelpSummary) #returns 1 row per zip with overall ratings
    df_craigslistSummary = craig.getData()
    df_zillowSummary = zillow.zillowData()

    print("zillow df size: ", df_zillowSummary.shape, "\n")
    print("craigslist df size: ", df_craigslistSummary.shape, "\n")
    print()
    
    result = pd.concat([df_zillowSummary, df_craigslistSummary], axis=1, join='inner')

    result.to_excel('Result.xlsx')
#Print to CSV
    #df_yelp.to_csv('AllYelpData.csv')
    #df_yelpSummary.to_csv('SummaryYelpData.csv')
    #df_yelpOverallRating.to_csv('YelpOverallRating.csv')
    
def getDataFromCSV():
    #get data from last CSV/Excel file created instead of pulling directly from online source
    
    df_yelp = pd.read_csv('AllYelpData.csv')
    df_yelpSummary = pd.read_csv('SummaryYelpData.csv')
    df_yelpOverallRating = pd.read_csv('YelpOverallRating.csv')



def main():
    getData()
    getDataFromCSV()
      

if __name__ == '__main__':
    main()