# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 21:48:31 2018

@author: ajcai
"""
# import individual data sources
import YelpDataAPI as yd
import CraigslistCode as cc
import GetZipcodeRentalPricePlot as rp
import ZillowHousingDataByZip as zd
import ArrestData as ar
import PASchoolPerf_Extraction as ed

# packages
import pandas as pd
import matplotlib.pyplot as plt
from math import pi

# variables
firstZip = ''
secondZip = ''
thirdZip = ''


# grab dataframes from individual sources using there .py files
df_zillowSummary = zd.zillowData()
df_craigslistSummary = cc.getData()
df_arrests = ar.arrestData()
df_education = ed.ReturnAggregate_Rebase()
df_yelp = yd.getOverallRating()

# converting index from ints to string
df_yelp.index = df_yelp.index.astype(str)

#combine dataframes from sources
aggregatedZipData = pd.concat([df_zillowSummary, df_craigslistSummary, df_arrests, df_education, df_yelp]
                            , axis=1, join='outer')
    
#fill in any missing values with 0
aggregatedZipData = aggregatedZipData.fillna(value=0)

#print resulting dataframe out to excel
aggregatedZipData.to_excel('Result.xlsx')

# create dataframe for scores (0 - 5)
zip_scores = aggregatedZipData[['BlendedScore_rebase','restaurantScore', 'barScore', 
                                'groceryScore', 'housingPriceScore', 'CrimeScore']].round(1)


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
    # weighted scores df
    weightScores = zip_scores.copy(deep=True)
    
    # weight scores based on user input
    weightScores['restaurantScore'] = weightScores['restaurantScore']*inputDict['restaurant']
    weightScores['barScore'] = weightScores['barScore']*inputDict['nightlife']
    weightScores['groceryScore'] = weightScores['groceryScore']*inputDict['grocery']
    weightScores['BlendedScore_rebase'] = weightScores['BlendedScore_rebase']*inputDict['education']
    weightScores['housingPriceScore'] = weightScores['housingPriceScore']*4
    #converting crime scores sp highest is the best safety rating
    weightScores['CrimeScore'] = (((weightScores['CrimeScore'] - 5) * -1)*inputDict['crime']).abs()
    
    # sum overall score in column
    weightScores['overallScore'] = weightScores.sum(axis=1)
    weightScores.to_excel('zipScores.xlsx')
    weightScores.sort_values('overallScore', ascending = False, inplace = True)
    
    # save top three zipcodes
    firstZip = str(weightScores.index.values[0])
    secondZip = str(weightScores.index.values[1])
    thirdZip = str(weightScores.index.values[2])
    
    # print top three zipcodes
    print('Here are the top 3 zip codes based on your preferences: \n')
    print('1. ' + str(firstZip))
    print('2. ' + str(secondZip))
    print('3. ' + str(thirdZip))
    
    spyderChart(firstZip, secondZip, thirdZip)

def spyderChart(firstZip, secondZip, thirdZip):
    
    
    # REFERENCE: https://python-graph-gallery.com/391-radar-chart-with-several-individuals/
    firstZipDF = zip_scores.loc[firstZip].T
    firstZipDF.reset_index(drop=True, inplace=True)
    
    secondZipDF = zip_scores.loc[secondZip].T
    secondZipDF.reset_index(drop=True, inplace=True)
    
    thirdZipDF = zip_scores.loc[thirdZip].T
    thirdZipDF.reset_index(drop=True, inplace=True)
    
    

    # ------- PART 1: Create background
     
    # number of variable
    categories=['Education','Restaurants', 'NightLife', 
                                'Groceries', 'Housing', 'Safety']
    N = len(categories)
     
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
     
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
     
    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
     
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)
     
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([1,2,3,4,5], ["0","1","2","3","4","5"], color="grey", size=7)
    plt.ylim(0,6)
    
    # ------- PART 2: Add plots
     
    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable
     
    # Ind1
    values=firstZipDF.values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=firstZip)
    ax.fill(angles, values, 'b', alpha=0.1)
     
    # Ind2
    values=secondZipDF.values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=secondZip)
    ax.fill(angles, values, 'r', alpha=0.1)
    
    ## Ind3
    values=thirdZipDF.values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=thirdZip)
    ax.fill(angles, values, 'g', alpha=0.1)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.show()  
    
    
    
def showGraphs(zipcode):
    
    if zipcode == 'all':
        yd.getMacroChart()
        cc.getOverallAggregateData(cc.getData())
        ed.printMacroChart_M()
    
    else:
        yd.getMicroChart(str(zipcode))
        rp.getZipcodePlot(int(zipcode))
        ed.printZipCodeColumn_M(zipcode)
    
    
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
 
            
