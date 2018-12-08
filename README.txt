GitHub with all code files: https://github.com/Ajcaico/Homi_DFP

Source data files must be located in the working directory folder where the py files are located.
SPP.APD.2016.2017.txt - School performance
SPP.FF.2016.2017.txt - School quick fact data
zipcodeCoordinates.csv - coorindates tied to zipcodes
Zip folder - folder that contains zillow data, folder name must be in working directory since files are written/read from this folder
There are other 


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

All imported modules are included in Anaconda and not other installs were required


Running the code:
HomiUserInput.py file has several functions and some code not in a fucntion that triggers the functions that need to be called. Just running the file will run trigger all functions required 
keep "getData()" (line53 from HomiUserInput.py file) uncommented during first run to get data from Yelp through API calls (~30 mins to run) - RUN ONLY ONCE then comment out, results will write to excel
Occasionally there are timeout/connection errors with the Yelp API and also a limit of number of calls per day. There are two API keys at the top of YelpData.py file that can be swapped if daily limit exceeded
The Yelp data excel output from last run is included in zipfile submitted, so getData() is not required because the rest of the code calls the data from the excel file

outside the functions in line 252 there is "calculateOverallScore(getUserInput())" which triggers these functions that run all the necessary code
Then the console will prompt for ratings for each category. 
Enter any number from 1-5 for each category. There is error handling to handle any valid inputs, such as non-numeric or numbers outside of range 
After entering in all ratings, the top 3 zip codes will show up and console will send a prompt to type in Y or N to see graphs about a specific zip code
Type in Y, to see more graphs (there is also error handling for invalid inputs) 
Another prompt will appear to type in zipcode to search. Choose one of the 3 zipcodes recommended and type that in. 
Detailed graphs will appear for stats of that zipcode. 
The console will prompt again to see more graphs, type in N. 
There will be another prompt to see overall pittsburgh statistics. 
Type in Y to see overall statistics More graphs will appear.
The program will stop running after this. 
