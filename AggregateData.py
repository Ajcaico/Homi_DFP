# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 00:42:46 2018

@author: ajcai
"""
##import each .py file
import YelpDataAPI as yd


def getData():
    
#Call functions from each .py file to get data
    df_yelp = yd.getData() #returns all yelp data
    df_yelpSummary = yd.getSummaryData(df_yelp) #returns summary by zip and category
    


def dataFrametoCSV(df):
    df.to_csv('yelpData.csv')
    

def main():
    getYelpData()
    
    
    
    

if __name__ == '__main__':
    main()