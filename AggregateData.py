# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 00:42:46 2018

@author: ajcai
"""
import pandas as pd
import YelpDataAPI as yd


def getYelpData():
    df = yd.getData()
    df_summary = yd.getSummaryData(df)
    
    print('Printing all data')
    print(df)
    
    print('Printing summary data')
    print(df_summary)
    

def printDataFrametoCSV(df):
    df.to_csv('yelpData.csv')
    

def main():
    getYelpData()
    
    
    