#-------------------------------------------------------------------------------------------------#
# make_dataset.py makes the datasets of fantasy football player stats by year, taken from 
# footballdb.com, and stores them in .csv files in 
#
# Author: Caleb Federman
#-------------------------------------------------------------------------------------------------#

import requests
from bs4 import BeautifulSoup
import pandas as pd

#-------------------------------------------------------------------------------------------------#
#   Function: get_df()
#   Description: Gets dataframe from HTML table at given URL
#   Arguments: URL - url of the web page where the table resides
#-------------------------------------------------------------------------------------------------#
def get_df(URL):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # find table
    table = soup.find_all("table",{"class":"statistics scrollable"}) # Note: in order to use for other tables need to change class

    data_frame = pd.read_html(str(table))[0]

    return(data_frame)

#-------------------------------------------------------------------------------------------------#

# class to create Year objects which store the year and corresponding dataframe
class Year:
    def __init__(self, year, df):
        self.year = year
        self.df = df

#-------------------------------------------------------------------------------------------------#

current_year = 2022
positions = ['QB','RB','WR','TE']

c = 0

for x in range(2010,current_year+1):
    for p in positions:
        data_frame = get_df(f"https://www.footballdb.com/fantasy-football/index.html?pos={p}&yr={x}&wk=all&key=b6406b7aea3872d5bb677f064673c57f")
        data_frame['Pos'] = p
        if c == 0:
            data_frame.to_csv(f'./data/raw/rTotal.csv', index=False)
        else:
            data_frame.to_csv(f'./data/raw/rTotal.csv', mode='a', header=False, index=False)
        c+=1

#-------------------------------------------------------------------------------------------------#

