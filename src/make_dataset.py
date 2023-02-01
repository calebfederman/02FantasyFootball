#-------------------------------------------------------------------------------------------------#
# Starter file for fantasy football data analysis project
# Caleb Federman
#-------------------------------------------------------------------------------------------------#

import requests
from bs4 import BeautifulSoup
import pandas as pd

#-------------------------------------------------------------------------------------------------#
#   Function: get_df()
#   Description: Gets dataframe from HTML table at given URL
#   Arguments: URL - url of the web page where the table resides
#
#   Note: in order to use for other tables, need to change class in soup.find_all() function
#-------------------------------------------------------------------------------------------------#
def get_df(URL):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # find table
    table = soup.find_all("table",{"class":"statistics scrollable"})

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

years = []

outdir = './raw'

for x in range(2010,current_year+1):
    data_frame = get_df(f"https://www.footballdb.com/fantasy-football/index.html?pos=OFF&yr={x}&wk=all&key=b6406b7aea3872d5bb677f064673c57f")
    data_frame.to_csv(f'./data/raw/{x}.csv', index=False)
    years.append(Year(x,data_frame))

#-------------------------------------------------------------------------------------------------#

