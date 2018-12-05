# Homi_DFP
Homi App for Data Focused Python

GitHub with all code files: https://github.com/Ajcaico/Homi_DFP

Individual python files to pull data from each data source:
YelpDataAPI.py - Makes API calls to Yelp and creates excel after parsing through JSON responses. Also generates graphs based on data in excel. 
CraigslistCode.py - Scrapes data from craigslists and creates excel after cleaning the data.
ArrestData.py - Retrieves crime data and stores into dataframes



Integrated python files:
AggregateData.py - calls each individual file to generate dataframes for all data. Merges all data files into a combined dataframe
HomiUserInput.py - Gets user inputs for each category used to calculate overall score.
		   Calls each individual file to get combined overall score per category.
		   Gets user inputs to see specific graphs and calls each individual py file to return a graph for each category


Running the code:
execute getData() function from HomiUserInput.py file to get data from each data source - RUN ONLY ONCE then comment out, results will write to excel.

execute getUserInput() function to prompt for user input then perform calculations to determine top rated zip codes, additional prompts 
