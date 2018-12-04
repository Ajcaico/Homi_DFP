# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 21:48:31 2018

@author: ajcai
"""
import YelpDataAPI as yd
import CraigslistCode as cc
import GetZipcodeRentalPricePlot as rp
import ZillowHousingDataByZip as zd

firstZip = 0
secondZip = 0
thirdZip = 0



def getUserInput():
    print("Rate your importance for each category on a scale of 1-5 then press enter, 1 being not important and 5 being very important")
   
    validInput = False
    while (not validInput):
        try:
            educationInput = int(input("Education: ").strip())
            if (educationInput <= 5 and educationInput > 0):
                validInput = True
            else:
               raise Exception()
        except:
            print('Invalid input. Enter an integer between 1 and 5')
            
            
    validInput = False
    while (not validInput):
        try:
            crimeInput = int(input("Crime: ").strip())
            if (crimeInput <= 5 and crimeInput > 0):
                validInput = True
            else:
               raise Exception()
        except:
            print('Invalid input. Enter an integer between 1 and 5')
            
    
    validInput = False
    while (not validInput):
        try:
            restaurantInput = int(input("Restaurant: ").strip())
            if (restaurantInput <= 5 and restaurantInput > 0):
                validInput = True
            else:
               raise Exception()
        except:
            print('Invalid input. Enter an integer between 1 and 5')                
    
    validInput = False
    while (not validInput):
        try:
            nightlifeInput = int(input("Nightlife: ").strip())
            if (nightlifeInput <= 5 and nightlifeInput > 0):
                validInput = True
            else:
               raise Exception()
        except:
            print('Invalid input. Enter an integer between 1 and 5')  
    
    validInput = False
    while (not validInput):
        try:
            groceryInput = int(input("Grocery: ").strip())
            if (groceryInput <= 5 and groceryInput > 0):
                validInput = True
            else:
               raise Exception()
        except:
            print('Invalid input. Enter an integer between 1 and 5')  
    
        
    inputDict = {'education' : int(educationInput), 'crime': int(crimeInput), 'restaurant': int(restaurantInput), 'nightlife': int(nightlifeInput), 'grocery': int(groceryInput)}
    return inputDict



def calculateOverallScore(inputDict):
    df_yelp = yd.getOverallRating()
   

    df_overall = df_yelp
    # result = pd.concat([df_zillowSummary, df_craigslistSummary, df_yelpSummaryTop, df_arrests], axis=1, join='outer')

    df_overall['restaurantScore'] = df_overall['restaurantScore']*inputDict['restaurant']
    df_overall['barScore'] = df_overall['barScore']*inputDict['nightlife']
    df_overall['groceryScore'] = df_overall['groceryScore']*inputDict['grocery']
    
    
    df_overall['overallScore'] = df_overall['restaurantScore'] + df_overall['barScore'] + df_overall['groceryScore'] 
    
    
    df_overall = df_overall.sort_values('overallScore', ascending=False)
    print(df_overall)

    firstZip = df_overall.index.values[0]
    secondZip = df_overall.index.values[1]
    thirdZip = df_overall.index.values[2]

    print('Here are the top 3 zip codes based on your preferences: \n')
    print('1. ' + str(firstZip))
    print('2. ' + str(secondZip))
    print('3. ' + str(thirdZip))


def showGraphs(zipcode):
    
    if zipcode == 'all':
        yd.getMacroChart()
        cc.getOverallAggregateData(cc.getData())
    
    else:
        yd.getMicroChart(str(zipcode))
        rp.getZipcodePlot(int(zipcode))
  
    
    
#Start calling functions 
    
calculateOverallScore(getUserInput())





viewGraph = 'Y'
while(viewGraph == 'Y'):
    validInput = False
    while (not validInput):
        try:
            viewGraph = input('Do you want to see more details about a zip code? Type Y or N \n').strip()
            if (viewGraph == 'Y' or viewGraph == 'N'):
                validInput = True
            else:
               raise Exception()
        except:
            print('Invalid input. Enter Y or N')  
    
    
    if (viewGraph == 'Y'):
        validInput = False
        while (not validInput):
            try:
                zipcode = int(input('Type in zipcode you want to see more details on: ').strip())
                if (zipcode >= 15000 and zipcode <= 16200):
                    validInput = True
                    showGraphs(zipcode)
                else:
                   raise Exception()
            except:
                print('Invalid input. Enter a valid 5 digit Pittsburgh zip code')  
       

viewGraph = 'Y'
while(viewGraph == 'Y'):
    validInput = False
    while (not validInput):
            viewGraph = input('Do you want to see overall details for Pittsburgh? Type Y or N \n').strip()
            if (viewGraph == 'Y'):
                validInput = True
                showGraphs('all')
            elif (viewGraph == 'N'):
                validInput = True
            else:
               print('Invalid input. Enter Y or N') 
 
            
