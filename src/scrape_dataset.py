#-------------------------------------------------------------------------------------------------#
# scrape_dataset.py holds the functions that make the datasets of fantasy football player 
# stats by year, scraped from footballdb.com, and stores them in .csv files
#
# Author: Caleb Federman
#-------------------------------------------------------------------------------------------------#

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

#-------------------------------------------------------------------------------------------------#
#   Function: get_df()
#   Description: Gets dataframe from HTML table at given URL
#   Arguments: URL - url of the web page where the table resides
#-------------------------------------------------------------------------------------------------#
def get_df(URL):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find_all("table",{"class":"statistics scrollable"}) # Note: in order to use for other tables need to change class

    df = pd.read_html(str(table))[0]

    return(df)


#-------------------------------------------------------------------------------------------------#
#   Function: create_raw_csvs()
#   Description: Creates raw csv files from dataframes
#   Arguments: current_year - year of the most recent NFL season
#-------------------------------------------------------------------------------------------------#

def create_raw_csvs():

    positions = ['QB','RB','WR','TE']
    c = 0

    for x in range(2010,datetime.date.today().year+1):
        for p in positions:

            df = get_df(f"https://www.footballdb.com/fantasy-football/index.html?pos={p}&yr={x}&wk=all&key=b6406b7aea3872d5bb677f064673c57f")
            df['Pos'] = p

            # yearly csv
            if p == 'QB':
                df.to_csv(f'./data/raw/r{x}.csv', index=False)
            else: 
                df.to_csv(f'./data/raw/r{x}.csv', mode='a', header=False, index = False)

            # total csv
            if c == 0:
                df.to_csv(f'./data/raw/rTotal.csv', index=False)
            else:
                df.to_csv(f'./data/raw/rTotal.csv', mode='a', header=False, index=False)
            c+=1

#-------------------------------------------------------------------------------------------------#
