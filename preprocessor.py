import pandas as pd

def preprocess():
    # Read data files
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')

    # Filter for Summer Olympics
    df = df[df['Season'] == 'Summer']

    # Merge dataframes, explicitly handling potential duplicate column names with suffixes
    df = df.merge(region_df, on='NOC', how='left', suffixes=('', '_region'))

    # Rename columns that have suffixes to avoid conflicts
    duplicate_columns = ['region', 'notes']
    for col in duplicate_columns:
        if col + '_region' in df.columns:
            df.rename(columns={col + '_region': col + '_extra'}, inplace=True)

    # Drop duplicates to clean the dataset
    df.drop_duplicates(inplace=True)

    # Add Medal columns with dummy variables
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df

