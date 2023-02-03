#-------------------------------------------------------------------------------------------------#
# process_dataset.py processes and cleans the fantasy football dataset scraped by make_dataset.py
#
# Author: Caleb Federman
#-------------------------------------------------------------------------------------------------#

import pandas as pd

#-------------------------------------------------------------------------------------------------#

#current_year = 2022

#for x in range(2010,current_year+1):
df = pd.read_csv(f"./data/raw/rTotal.csv")

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
df = df.astype({'Pts':'int','passAtt':'int','passCmp':'int','passYds':'int','passTD':'int','passInt':'int',
                'pass2pt':'int','rushAtt':'int','rushYds':'int','rushTD':'int','ru2pt':'int',
                'rec':'int','recYds':'int','recTD':'int','rec2pt':'int','FL':'int','FLTD':'int'})
df = df.astype({'Player':'string'})

#-----------------------------------------------------------#

# sort by descending point totals
df = df.sort_values(by='Pts', ascending=False)

#-----------------------------------------------------------#

df.to_csv(f'./data/processed/pTotal.csv', index=False)

#-------------------------------------------------------------------------------------------------#