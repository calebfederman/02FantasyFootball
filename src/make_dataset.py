#-------------------------------------------------------------------------------------------------#
# create_dataset.py calls the functions to scrape and clean the dataset in order to have
# clean data for analysis
#
# Author: Caleb Federman
#-------------------------------------------------------------------------------------------------#

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

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

#-------------------------------------------------------------------------------------------------#
#   Function: clean_data()
#   Description: cleans data into format with proper headers and ordering
#   Arguments: URL - url of the web page where the table resides
#-------------------------------------------------------------------------------------------------#

def clean_data():

    files = list(range(2010,datetime.date.today().year+1))
    files.append('Total')

    for x in files:

        df = pd.read_csv(f"./data/raw/r{x}.csv")
        if (len(df.index)<5):
                os.remove(f"./data/raw/r{x}.csv")
                continue

        #-----------------------------------------------------------#

        # rename columns
        columns = ['Player','Bye','Pts','passAtt','passCmp','passYds','passTD','passInt','pass2pt',
                'rushAtt','rushYds','rushTD','ru2pt','rec','recYds','recTD','rec2pt','FL','FLTD','Pos']
        df.columns = columns

        #-----------------------------------------------------------#

        # add position column and move it to second from far left
        df = df[['Player','Pos','Bye','Pts','passAtt','passCmp','passYds','passTD','passInt','pass2pt',
                'rushAtt','rushYds','rushTD','ru2pt','rec','recYds','recTD','rec2pt','FL','FLTD']]

        #-----------------------------------------------------------#

        # drop row with old headers
        df = df.drop(labels=0, axis=0)

        #-----------------------------------------------------------#

        # cut off second iteration of player names
        for ind in df.index:
            df.loc[ind].at['Player'] = df.loc[ind].at['Player'][:df.loc[ind].at['Player'].rfind(df.loc[ind].at['Player'][0]+'.')]

        #-----------------------------------------------------------#

        # convert types where necessary

        df = df.astype({'Pts':'float'})
        df = df.astype({'passAtt':'int','passCmp':'int','passYds':'int','passTD':'int','passInt':'int',
                        'pass2pt':'int','rushAtt':'int','rushYds':'int','rushTD':'int','ru2pt':'int',
                        'rec':'int','recYds':'int','recTD':'int','rec2pt':'int','FL':'int','FLTD':'int'})
        df = df.astype({'Player':'string'})

        #-----------------------------------------------------------#

        # adjust point totals to account for the following scoring system
        pts = []
        for ind in df.index:
                pts.append(round((df.loc[ind].at['passYds'] * 0.04) +   # 25 pass yds / pt
                                 (df.loc[ind].at['passTD'] * 4) -       # 4 pts / pass TD
                                 (df.loc[ind].at['passInt'] * 2) +      # -2 pts / interception
                                 (df.loc[ind].at['pass2pt'] * 2) +      # 2 pts / two point conversion
                                 (df.loc[ind].at['rushYds'] * 0.1) +    # 10 rush yds / pt
                                 (df.loc[ind].at['rushTD'] * 6) +       # 6 pts / rush TD
                                 (df.loc[ind].at['ru2pt'] * 2) +        # 2 pts / two point conversion
                                 (df.loc[ind].at['rec'] * 1) +          # 1 ppr
                                 (df.loc[ind].at['recYds'] * 0.1) +     # 10 rec yds / pt
                                 (df.loc[ind].at['recTD'] * 6) +        # 6 pts / rec TD
                                 (df.loc[ind].at['rec2pt'] * 2) -       # 2 pts / two point conversion
                                 (df.loc[ind].at['FL'] * 2)             # -2 pts / fumble lost
                                                                ,1))    # round to nearest tenth
        df.Pts = pts

        # sort by descending point totals
        df = df.sort_values(by='Pts', ascending=False)

        #-----------------------------------------------------------#

        df.to_csv(f'./data/processed/p{x}.csv', index=False)

#-------------------------------------------------------------------------------------------------#

# run functions to create the datasets (in the future create shell script to run this?)

create_raw_csvs()
clean_data()

