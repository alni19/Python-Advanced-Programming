import pandas as pd

class MovieAnalyzer(object):
    def topMovie(self,n):
        #load movie data
        movies=pd.read_table('movies.dat', sep='::', header=None, names=['movie_id', 'title', 'genres'])
        #load rating data
        ratings=pd.read_table('ratings.dat', sep='::', header=None, names=[ 'user_id','movie_id','rating','time_stamp'])
        #average ratings for each movie
        avgrating=pd.DataFrame({'Avg_Rating':ratings['rating'].groupby(ratings['movie_id']).mean()}) 
        #join the two data frames into one data frame
        #split single row with multiple genres into multiple rows with single genres and append into the new data frame splitgentable
        jointable=pd.merge(movies, avgrating, left_on='movie_id', right_index=True,how='inner')
        splitgentable = pd.DataFrame(columns = jointable.columns)
        for i in jointable.index:
            gen = jointable.ix[i,'genres'].split('|')
            row = jointable.ix[i]
            for j in range(0,len(gen)):
                row['genres'] = gen[j]
                splitgentable = splitgentable.append(row, ignore_index=True)
        
        def top(df, k):
            return df.sort_index(by='Avg_Rating')[-k:]          
        df = splitgentable[['title','Avg_Rating','genres']].groupby('genres').apply(top,n)
        df = df.drop(['genres'], axis=1)
        return df
        