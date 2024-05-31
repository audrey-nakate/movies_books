import numpy as np
import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from surprise import Dataset, Reader, SVD, BaselineOnly, SVDpp, NMF, SlopeOne, CoClustering
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from surprise.model_selection import cross_validate, train_test_split
from surprise.prediction_algorithms import KNNBaseline, KNNBasic, KNNWithMeans, KNNWithZScore
from surprise import accuracy
from surprise import dump
from sklearn.preprocessing import normalize

movies_df = pd.read_csv("D:\\Year 3 Semester 2\\computerScienceProject\\tmdb_5000_movies.csv")
credits_df = pd.read_csv("D:\\Year 3 Semester 2\\computerScienceProject\\tmdb_5000_credits.csv")
ratings_df = pd.read_excel("D:\\Year 3 Semester 2\\computerScienceProject\\movie_ratings.xlsx")

#merge the two datasets
movies_df = movies_df.merge(credits_df, on='title')
movies_df = movies_df.merge(ratings_df, on='movie_id')

#selecting relevant columns
movies_final = movies_df[[ 'id', 'title', 'genres', 'runtime', 'overview', 'keywords', 'cast', 'crew', 'User_ID', 'RATINGS']]

#check for null values
print(movies_final.isna().sum())

#drop null values
movies_final.dropna(inplace=True)

#function to extract genre name
def convert(obj):
    l = []

    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l

movies_final['genres'] = movies_final['genres'].apply(convert)
movies_final['keywords'] = movies_final['keywords'].apply(convert)

#function to extract first three cast names
def convert3(obj):
    l = []
    counter = 0

    for i in ast.literal_eval(obj):
        if counter != 3:
            l.append(i['name'])
            counter += 1
        else:
            break
    return l

movies_final['cast'] = movies_final['cast'].apply(convert3)

# to extract director's name
def extract_director(obj):
    l = []

    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            l.append(i['name'])
            break
    return l

movies_final['crew'] = movies_final['crew'].apply(extract_director)

movies_final['overview'] = movies_final['overview'].apply(lambda x: x.split()) 

# removing spaces between words
movies_final['genres'] = movies_final['genres'].apply(lambda x : [i.replace(" ", "") for i in x])
movies_final['keywords'] = movies_final['keywords'].apply(lambda x : [i.replace(" ", "") for i in x])
movies_final['cast'] = movies_final['cast'].apply(lambda x : [i.replace(" ", "") for i in x])
movies_final['crew'] = movies_final['crew'].apply(lambda x : [i.replace(" ", "") for i in x])

movies_final['tags'] = movies_final['genres'] + movies_final['keywords'] + movies_final['cast'] + movies_final['crew'] + movies_final['overview']

movies = movies_final[['id', 'title', 'tags', 'User_ID', 'RATINGS']]

movies['tags'] = movies['tags'].apply(lambda x : " ".join(x))
movies['tags'] = movies['tags'].apply(lambda x : x.lower())

movies['RATINGS'] = movies['RATINGS'].replace(0, 1)

reader = Reader(rating_scale = (1, 10))
data = Dataset.load_from_df(movies[['id', 'User_ID', 'RATINGS']], reader)
traindf = data.build_full_trainset()
testdf = traindf.build_anti_testset()

sim_options = {'name' : 'cosine',
               'user_based' : False  #defining similarity measures
              }
               
knnbaseline_model = KNNBaseline(sim_options=sim_options)

knnbaseline_model.fit(traindf)
knnbaseline_predictions = knnbaseline_model.test(testdf)
accuracy.rmse(knnbaseline_predictions)
accuracy.mae(knnbaseline_predictions)

svdpp_model = SVDpp()

svdpp_model.fit(traindf)
svdpp_model_predictions = svdpp_model.test(testdf)

accuracy.rmse(svdpp_model_predictions)
accuracy.mae(svdpp_model_predictions)

#  content-based filtering
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
content_matrix = tfidf_vectorizer.fit_transform(movies['tags'])
content_similarity = linear_kernel(content_matrix, content_matrix)

mappings = pd.Series(movies.index, index=movies['title'])

def get_recommendations_new(title):
    idx = mappings[title]
    if type(idx) != np.int64:
        if len(idx)>1:
            print("ALERT: Multiple values")
            idx = idx[0]
    sim_scores = list(enumerate(content_similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies['id'].iloc[movie_indices]

def hybrid(userId):
    user_movies = pd.DataFrame(testdf, columns=['id', 'User_ID', 'RATINGS'])
    user_movies = user_movies[user_movies['User_ID'] == userId]
    user_movies['est'] = user_movies['id'].apply(lambda x: 0.6*knnbaseline_model.predict(userId,x).est + 0.4*svdpp_model.predict(userId, x).est)    
    user_movies = user_movies.sort_values(by ='est', ascending=False).head(4)
    user_movies['Model'] = 'SVD + CF'
#     user_movies = user_movies['movieId'].values.tolist()
#     print("User liked movies list: ", user_movies)
    
    recommend_list = user_movies[['id', 'est', 'Model']]
    print(recommend_list.head())

#     top_movie = user_movies['movieId'].iloc[0]
#     print("Top movie id", top_movie)
#     top_movie_title = movies['title'][movies['movieId'] == top_movie].values[0]
#     print("Top movie title", top_movie_title)

    
    movie_list = recommend_list['id'].values.tolist()
    print(movie_list)
    sim_movies_list = []
    for movie_id in movie_list:
        # Call content based 
        movie_title = movies['title'][movies['id'] == movie_id].values[0]
        sim_movies = get_recommendations_new(movie_title)
#         print(sim_movies.values.tolist())
        sim_movies_list.extend(sim_movies)
    
    
    # Compute ratings for the popular movies
    for movie_id in sim_movies_list:
        pred_rating = 0.6*knnbaseline_model.predict(userId, movie_id).est + 0.4*svdpp_model.predict(userId, movie_id).est
        row_df = pd.DataFrame([[movie_id, pred_rating, 'Movie similarity']], columns=['id', 'est','Model'])
        recommend_list = pd.concat([recommend_list, row_df], ignore_index=True)
    
    # # Popular based movies
    # top_genre_list = user_top_genre(userId)
    # print("User top genre list: ", top_genre_list)
    
    # popular_movies = []
    # for top_genre in top_genre_list:
    #     popular_movies.extend(genre_based_popularity(top_genre))
    # print("Final list: ", popular_movies)
    
    # Compute ratings for the popular movies
    # for movie_id in popular_movies:
    #     pred_rating = 0.6*knnbaseline_algo.predict(userId, movie_id).est + 0.4*svdpp_algo.predict(userId, movie_id).est
    #     row_df = pd.DataFrame([[movie_id, pred_rating, 'Popularity']], columns=['movieId', 'est','Model'])
    #     recommend_list = pd.concat([recommend_list, row_df], ignore_index=True)
    # recommend_list = recommend_list.drop_duplicates(subset=['movieId'])
    # train_movie_list = traindf[traindf['userId']==userId]['movieId'].values.tolist()
    
    # Remove movies in training for this user
    # mask = recommend_list.movieId.apply(lambda x: x not in train_movie_list)
    # recommend_list = recommend_list[mask]
    
    return recommend_list

movie_ids = hybrid(250634)

def get_title(x):
    mid = x['id']
    return movies['title'][movies['id'] == mid].values

def get_tags(x):
    mid = x['id']
    return movies['tags'][movies['id'] == mid].values

movie_ids['title'] = movie_ids.apply(get_title, axis=1)
movie_ids['tags'] = movie_ids.apply(get_tags, axis=1)

movie_ids.sort_values(by='est', ascending = False).head(10)
