import pandas as pd
import numpy as np


df0 = pd.read_csv('games.csv')
#print(df0.head(3))
#print(df0.info())

df = df0.dropna().query('2000 <= Year_of_Release <= 2022')
#print(df.info())
#print(df.describe())

 # convert age rating from str to int using map
rating_map = {"E": 0, "E10+": 10, "T": 13, "M": 17, "AO": 18, 'RP': 18} # I decide to assign 'Rating Pending' the value 18 like the 'Adults Only' one for now
df["Rating"] = df["Rating"].map(rating_map).astype(int)

df['User_Score'] = df['User_Score'].replace('tbd', np.nan).astype(float) # I want to see the statistics of User_Score var too, I need numeric and nan for the rest
df['Year_of_Release'] = df['Year_of_Release'].astype(int)
print(df.info())
print(df.describe())