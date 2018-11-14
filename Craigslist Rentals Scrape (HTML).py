import pandas as pd
from bs4 import BeautifulSoup as bs4
#%pylab inline

import requests
import numpy as np

url_base = 'https://pittsburgh.craigslist.org/d/apts-housing-for-rent/search/apa'

zipcodes = [15106] 
#            15120, 15201, 15203, 15204, 15205, 15206, 15207, 15208, 15210, 
#            15211, 15212, 15213, 15214, 15215, 15216, 15217, 15218, 15219, 15220, 
#            15221, 15222, 15224, 15226, 15227, 15232, 15233, 15234, 15235, 15236, 
#            15238, 15260, 15290]
#for zip in zipcodes:
params = dict(postal=zip)
    
rsp = requests.get(url_base)

# Note that requests automatically created the right URL:
print(rsp.url)

# We can access the content of the response that Craigslist sent back here:
print(rsp.text[:500])

# BS4 can quickly parse our text, make sure to tell it that you're giving html
html = bs4(rsp.text, 'html.parser')

# BS makes it easy to look through a document
print(html.prettify()[65000:75000])

# find_all will pull entries that fit your search criteria.
# Note that we have to use brackets to define the `attrs` dictionary
# Because "class" is a special word in python, so we need to give a string.
apts = html.find_all('p', attrs={'class': 'result-info'})
print(len(apts))

# We can see that there's a consistent structure to a listing.
# There is a 'time', a 'name', a 'housing' field with size/n_brs, etc.
this_appt = apts[15]
print(this_appt.prettify())

# So now we'll pull out a couple of things we might be interested in:
# It looks like "housing" contains size information. We'll pull that.
# Note that `findAll` returns a list, since there's only one entry in
# this HTML, we'll just pull the first item.
size = this_appt.findAll(attrs={'class': 'housing'})[0].text
print(size)

def find_size_and_brs(size):
    split = size.strip().strip('/- ').split(' -\n ')
    if len(split) == 2:
        n_brs = split[0].replace('br', '')
        this_size = split[1].replace('ft2', '')
    elif 'br' in split[0]:
        # It's the n_bedrooms
        n_brs = split[0].replace('br', '')
        this_size = np.nan
    elif 'ft2' in split[0]:
        # It's the size
        this_size = split[0].replace('ft2', '')
        n_brs = np.nan
    return float(this_size), float(n_brs)
this_size, n_brs = find_size_and_brs(size)

# Now we'll also pull a few other things:
this_time = this_appt.find('time')['datetime']
this_time = pd.to_datetime(this_time)
this_price = float(this_appt.find('span', {'class': 'result-price'}).text.strip('$'))
this_title = this_appt.find('a', attrs={'class': 'hdrlnk'}).text
this_neighborhood = this_appt.find('span', {'class': 'result-hood'}).text.strip().strip('(').strip(')')

# Now we've got the n_bedrooms, size, price, and time of listing
print('\n'.join([str(i) for i in [this_size, n_brs, this_time, this_price, this_title, this_neighborhood]]))

loc_prefixes = ['eby', 'nby', 'sfc', 'sby', 'scz']

def find_prices(results):
    prices = []
    for rw in results:
        price = rw.find('span', attrs={'class': 'result-price'})
        if price is not None:
            price = float(price.text.strip('$'))
        else:
            price = np.nan
        prices.append(price)
    return prices

def find_times(results):
    times = []
    for rw in apts:
        if time is not None:
            time = time['datetime']
            time = pd.to_datetime(time)
        else:
            time = np.nan
        times.append(time)
    return times

#print(txt.prettify())

def find_size_and_brs(size):
    split = size.strip().split('\n')
    split = [ii.strip().strip(' -') for ii in split]
    if len(split) == 2:
        n_brs = split[0].replace('br', '')
        this_size = split[1].replace('ft2', '')
    elif 'br' in split[0]:
        # It's the n_bedrooms
        n_brs = split[0].replace('br', '')
        this_size = np.nan
    elif 'ft2' in split[0]:
        # It's the size
        this_size = split[0].replace('ft2', '')
        n_brs = np.nan
    return float(this_size), float(n_brs)

def find_neighborhoods(results):
    neighborhoods = []
    for hoods in results:
        neighborhood = hoods.find('span', {'class': 'result-hood'})
        if neighborhood is not None:
            neighborhood = neighborhood.text.strip().strip('(').strip(')')
        else:
            neighborhood = np.nan
        neighborhoods.append(neighborhood)
    return neighborhoods

# Now loop through all of this and store the results
results = []  # We'll store the data here
# Careful with this...too many queries == your IP gets banned temporarily
search_indices = np.arange(0, 500, 100)
loc_prefixes = ['eby']
for loc in loc_prefixes:
    print (loc)
    for i in search_indices:
        url = 'https://pittsburgh.craigslist.org/d/apts-housing-for-rent/search/apa'
        resp = requests.get(url, params={'bedrooms': 1, 's': i})
        txt = bs4(resp.text, 'html.parser')
        apts = txt.findAll(attrs={'class': "result-info"})

        # Find the size of all entries
        size_text = [rw.findAll(attrs={'class': 'housing'})[0].text
                     for rw in apts]
        sizes_brs = [find_size_and_brs(stxt) for stxt in size_text]
        sizes, n_brs = zip(*sizes_brs)  # This unzips into 2 vectors

        # Find the title and link
        title = [rw.find('a', attrs={'class': 'hdrlnk'}).text
                      for rw in apts]
        links = [rw.find('a', attrs={'class': 'hdrlnk'})['href']
                 for rw in apts]

        # Find the time
        time = [pd.to_datetime(rw.find('time')['datetime']) for rw in apts]
        price = find_prices(apts)
        hood = find_neighborhoods(apts)

        # We'll create a dataframe to store all the data
        data = np.array([time, price, sizes, n_brs, hood, title, links])
        col_names = ['time', 'price', 'size', 'brs', 'neighborhood', 'title', 'link']
        df = pd.DataFrame(data.T, columns=col_names)
        df = df.set_index('time')

        # Add the location variable to all entries
        #df['loc'] = loc
        results.append(df)
        
# Finally, concatenate all the results
results = pd.concat(results, axis=0)

def seconds_to_days(seconds):
    return seconds / 60. / 60. / 24.

# We'll make sure that the right columns are represented numerically:
results[['price', 'size', 'brs']] = results[['price', 'size', 'brs']].convert_objects(convert_numeric=True)
results.index.name = 'time'

# Add the age of each result
now = pd.datetime.utcnow()
results['age'] = [1. / seconds_to_days((now - ii).total_seconds())
                  for ii in results.index]

# And there you have it:
print(results)

ax = results.hist('price', bins=np.arange(0, 10000, 100))[0, 0]
ax.set_title('Apartments by Price', fontsize=20)
ax.set_xlabel('Price', fontsize=18)
ax.set_ylabel('Count', fontsize=18)

target_price = 2200.
target_size = 1400.
highlight = pd.DataFrame([[target_price, target_size, 2, 'Mine', 'None', 1, results['age'].max()]],
                         columns=['price', 'size', 'brs', 'title', 'link', 'mine', 'age'])
results['mine'] = 0
results = results.append(highlight)

#import altair
#graph = altair.Chart(results)
#graph.mark_circle(size=200).encode(x='size', y='price',
#                                  color='mine:N')

#smin, smax = (1300, 1500)
#n_br = 2
# subset = results.query('size > @smin and size < @smax')
#fig, ax = plt.subplots()
#results.query('brs < 4').groupby('brs').hist('price', bins=np.arange(0, 5000, 200), ax=ax)
#ax.axvline(target_price, c='r', ls='--')

# Finally, we can save this data to a CSV to play around with it later.
# We'll have to remove some annoying characters first:
import string
use_chars = string.ascii_letters +\
    ''.join([str(i) for i in range(10)]) +\
    ' /\.'
results['title'] = results['title'].apply(
    lambda a: ''.join([i for i in a if i in use_chars]))

for zips in zipcodes:
    results.to_csv('C:\\Users\colto\craigslist' + str(zips) + '.csv')
