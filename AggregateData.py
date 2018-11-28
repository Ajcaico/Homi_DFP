##import each .py file
import pandas as pd
import YelpDataAPI as yd
import CraigslistCode as craig
import ZillowHousingDataByZip as zillow
import ArrestData as arrests

def getData(): 
#Call functions from each .py file to get data
    
    
    #DataFrames to use for aggregation
    df_yelpSummaryTop = yd.getData()
    df_craigslistSummary = craig.getData()
    df_zillowSummary = zillow.zillowData()
    df_arrests = arrests.arrestData()
    
    # checking size of dataFRames to be combined
    print("zillow df size: ", df_zillowSummary.shape, "\n")
    print("craigslist df size: ", df_craigslistSummary.shape, "\n")
    print("Yelp df size: ", df_yelpSummaryTop.shape, "\n")
    print("Arrests df size: ", df_arrests.shape, "\n")
            
    result = pd.concat([df_zillowSummary, df_craigslistSummary, df_yelpSummaryTop, df_arrests], axis=1, join='outer')
    result.to_excel('Result.xlsx')


    
def main():
    getData()
 
      
if __name__ == '__main__':
    main()
