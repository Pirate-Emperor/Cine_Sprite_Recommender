import numpy as np
import pandas as pd 
from collections import defaultdict
df = pd.read_csv('ratings_small.csv', index_col=False)
print(df)
print(df.iloc[1])
d1=dict()
d2=dict()
d=defaultdict(set)
for i in df.userId: d2[i]=df.index
for i in df.movieId: d1[i]=df.index
print(len(d1))
print(len(d2))
df_rat= pd.DataFrame()
for i in d2.keys():
    df_rat[str(i)]=""
    dfi=df[(df['userId']==i)]
    print(i)
    if (i>20): break
    for j in d1.keys():
        #print(df[(df['userId']==i) & (df['movieId']==j) ]['rating'].tolist()[0])
        val = dfi[(dfi['movieId']==j)]['rating'].tolist()
        #val = df[(df['userId']==i) & (df['movieId']==j) ]['rating'].tolist()
        df_rat.loc[str(j),str(i)]=val[0] if (len(val)>0)  else None
        #df_rat.loc[str(j),str(i)]=df.iloc[df.movieId==j and df.userId==i]['rating']
        #print(df_rat.loc[str(j),str(i)])
df_rat.index.name="movie"
print(df_rat)
df_rat.to_csv('small_movie_ratings1.csv')
"""for i in df.index:
    d[df.loc[i].movieId]|={df.loc[i].userId}"""


"""for i in df.movieId:
    d[i]|={}
for i in df.userId:
    print(i)"""