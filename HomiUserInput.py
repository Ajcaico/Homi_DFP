# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 21:48:31 2018

@author: ajcai
"""
import YelpDataAPI as yd

firstZip = 0
secondZip = 0
thirdZip = 0

def getUserInput():
    print("Rate your importance for each category on a scale of 1-5 then press enter, 1 being not important and 5 being very important")
    educationInput = input("Education: ")
    crimeInput = input("Crime: ")
    restaurantInput = input("Restaurant Quality: ")
    nightlifeInput = input("Nightlife: ")
    groceryInput = input("Grocery Stores: ")
    
    inputDict = {'education' : int(educationInput), 'crime': int(crimeInput), 'restaurant': int(restaurantInput), 'nightlife': int(nightlifeInput), 'grocery': int(groceryInput)}
    return inputDict



def calculateOverallScore(inputDict):
    df_yelp = yd.getOverallRating()
    df_yelp = df_yelp.dropna()
    print(df_yelp)


    df_overall = df_yelp


    df_overall['restaurantScore'] = df_overall['restaurantScore']*inputDict['restaurant']
    df_overall['barScore'] = df_overall['barScore']*inputDict['nightlife']
    df_overall['groceryScore'] = df_overall['groceryScore']*inputDict['grocery']
    df_overall['overallScore'] = df_overall['restaurantScore'] + df_overall['barScore'] + df_overall['groceryScore'] 
    df_overall = df_overall.sort_values('overallScore', ascending=False)
    print(df_overall)
    
    
    firstZip = df_overall.index.values[0]
    secondZip = df_overall.index.values[1]
    thirdZip = df_overall.index.values[2]

    print(firstZip)
    print(secondZip)
    print(thirdZip)


def showGraphs():
    
 #   yd.getMicroChart(str(firstZip))
    yd.getMacroChart()
    
    
    
calculateOverallScore(getUserInput())
showGraphs()