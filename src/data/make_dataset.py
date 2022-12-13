#-------------------------------------------------------------------------------------------------#
# Starter file for fantasy football data analysis project
# Caleb Federman
#-------------------------------------------------------------------------------------------------#

import requests
from bs4 import BeautifulSoup

#-------------------------------------------------------------------------------------------------#

# Function: get_data()
# Parameters : currentyear - the current (or most recent) nfl season
def get_data(currentyear):

    # years - list of years corresponding to each NFL season in the super bowl era
    # statcategory - list of stat categories to search for (0 = passing; 1 = rushing; 2 = receiving)
    years = list(range(1966,currentyear + 1))
    statcategory = ['passing','rushing','receiving']

    # Get attributes //ex: games, yds, tds, etc.

    # iterate through stat categories
    for cat in statcategory:

        # URL to receive html data from using year and statcategory arrays
        URL = "https://www.pro-football-reference.com/years/{}/{}.htm".format(currentyear,cat)

        # get html from web page
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        # find data from html file

        results = soup.find(id = cat)               # find section of html with id = 'passing', 'rushing', or 'receiving'
        table = results.find("tbody")               # find table
        firstrow = table.find("tr")                 # find first table row
        for d in firstrow.find_all("td") :          # for each piece of data (column) in the row...
            print(d.attrs)                          # ...print the html attributes for that line

#-------------------------------------------------------------------------------------------------#

# current (or most recent) nfl season
currentyear = 2022

# get data from profootballreference.com
get_data(currentyear)

#-------------------------------------------------------------------------------------------------#




