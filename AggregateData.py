##import each .py file
import pandas as pd
import YelpDataAPI as yd
import CraigslistCode as craig
import ZillowHousingDataByZip as zillow
import ArrestData as arrests

def getData(): 
#Call functions from each .py file to get data
    
    # used to get initial yelp dataset, after which it is saved to a file and pulled from there
#    df_yelp = yd.getData() #returns all yelp data, 1 row for each business
#    df_yelpSummary = yd.getSummaryData(df_yelp) #returns summary with 1 row for each zip and category
#    df_yelpOverallRating = yd.calculateRating(df_yelp, df_yelpSummary) #returns 1 row per zip with overall ratings
#    df_yelpSummaryTop = df_yelpSummary[df_yelpSummary.category == 'All Restaurants'] # returns 1 row for zipcode for all records cumulative
#    df_yelpSummaryTop = df_yelpSummaryTop.set_index('zipcode')
#    df_yelpSummaryTop.to_excel('df_yelpSummaryTop.xlsx')


    
    #DataFrames to use for aggregation
    df_yelpSummaryTop = pd.read_excel('df_yelpSummaryTop.xlsx')
    df_yelpSummaryTop = df_yelpSummaryTop.set_index('zipcode')
    
    df_craigslistSummary = craig.getData()
    df_zillowSummary = zillow.zillowData()
    df_arrests = arrests.arrestData()
    
    # checking size of dataFRames to be combined
    print("zillow df size: ", df_zillowSummary.shape, "\n")
    print("craigslist df size: ", df_craigslistSummary.shape, "\n")
    print("Yelp df size: ", df_yelpSummaryTop.shape, "\n")
    print("Arrests df size: ", df_arrests.shape, "\n")
    print()
        
    result = pd.concat([df_zillowSummary, df_craigslistSummary, df_yelpSummaryTop, df_arrests], axis=1, join='outer')
    result.to_excel('Result.xlsx')


    
def main():
    getData()
 
      
if __name__ == '__main__':
    main()
