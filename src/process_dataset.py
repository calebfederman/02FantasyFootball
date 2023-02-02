import pandas as pd

current_year = 2022

for x in range(2010,current_year+1):
    df = pd.read_csv(f"./data/raw/r{x}.csv")

    columns = ['Player','Bye','Pts','passAtt','passCmp','passYds','passTD','passInt','pass2pt',
            'rushAtt','rushYds','rushTD','ru2pt','rec','recYds','recTD','rec2pt','FL','FLTD']

    df.columns = columns
    df = df.drop(labels=0, axis=0)


    for ind in df.index:
        df.loc[ind].at['Player'] = df.loc[ind].at['Player'][:df.loc[ind].at['Player'].find('.')-1]

    df.to_csv(f'./data/processed/p{x}.csv', index=False)