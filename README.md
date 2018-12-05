# Homi_DFP
Homi App for Data Focused Python

GitHub with all code files: https://github.com/Ajcaico/Homi_DFP

Source data files must be located in the folder before running the code (other excel files will be generated when running the code):
SPP.APD.2016.2017.txt - School performance
SPP.FF.2016.2017.txt - School quick fact data
zipcodeCoordinates.csv - coorindates tied to zipcodes


Individual python files to pull data from each data source:
YelpDataAPI.py - Makes API calls to Yelp and creates excel after parsing through JSON responses. Also generates graphs based on data in excel. 
CraigslistCode.py - Scrapes data from craigslists and creates excel after cleaning the data.
ArrestData.py - Retrieves crime data and stores into dataframes
PASchoolPerf_Extraction.py - Reads text files from PA public schools and converts to dataframe


Integrated python files:
AggregateData.py - calls each individual file to generate dataframes for all data. Merges all data files into a combined dataframe
HomiUserInput.py - Gets user inputs for each category used to calculate overall score.
		   Calls each individual file to get combined overall score per category.
		   Gets user inputs to see specific graphs and calls each individual py file to return a graph for each category


Running the code:
Open the HomiUserInput.py file 
During 1st run, keep getData() function uncommented. This will extract all data and save into excel files (takes ~30 minutes to run)
Then the console will prompt for ratings for each category. Enter any number from 1-5. There is error handling to handle any valid inputs, such as non-numeric or numbers outside of range
After entering in all ratings, the top 3 zip codes will show up and console will send a prompt to type in Y or N to see graphs about a specific zip
Type in Y, to see more graphs (there is also error handling for invalid inputs)
Another prompt will appear to type in zipcode to search. Choose one of the 3 zipcodes recommended and type that in. 
Detailed graphs will appear for stats of that zipcode. 
The console will prompt again to see more graphs, type in N. 
There will be a prompt to see overall pittsburgh statistics. Type in Y to see overall statistics
More graphs will appear. 


After the 1st run, comment out the getData() function to avoid waiting for data to be pull from websites.
The code will be pulling data from the excel files that were generated during the first run.

