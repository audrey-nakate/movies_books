import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import streamlit as st
import requests

model = load_model('recommender.h5')
movies = pd.read_pickle(open('D:\OneDrive - FSD Uganda\Desktop\final_yr_deploys\movie_recommender\artifacts3\movie_list2.pkl', 'rb'))

def preprocess_input(movie_id):
    return np.array([[movie_id]])

def postprocess_output(model_output):
    # Get the indices of the top 5 recommended movies
    top_indices = np.argsort(model_output[0])[-5:][::-1]
    recommended_movie_ids = [movies.iloc[i].movie_id for i in top_indices]
    return recommended_movie_ids

def fetch_poster(movie_id):
    url = "http://api.themoviedb.org/3/movie/{}?api_key=976353e3f8f390ccba422c8ba896383c&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "http://image.tmdb.org/t/p/w500/" + poster_path

    return full_path

def fetch_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=976353e3f8f390ccba422c8ba896383c&language=en-US".format(movie_id)
    details = requests.get(url)
    details = details.json()
    overview = details['overview']

    return overview

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movie_id = movies.iloc[index].movie_id
    model_input = preprocess_input(movie_id)
    # Get recommendations from the model
    model_output = model.predict(model_input)
    recommended_movie_ids = postprocess_output(model_output)

    recommended_movies_name = []
    recommended_movies_poster = []
    recommended_movie_details = []

    for movie_id in recommended_movie_ids:
        recommended_movie_details.append(fetch_movie_details(movie_id))
        recommended_movies_poster.append(fetch_poster(movie_id))    
        recommended_movies_name.append(movies[movies['movie_id'] == movie_id].title.values[0])
    
    return recommended_movies_name, recommended_movies_poster, recommended_movie_details

# Streamlit integration
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie to get a recommendation",
    movie_list
)

if st.button("Show recommendation"):
    recommended_movies_name,recommended_movies_poster,recommended_movie_details = recommend(selected_movie)
    
    def display_movie_info(movie_name, movie_poster, movie_details):
        st.image(movie_poster, width=250)
        st.text(movie_name)
        with st.expander("Overview"):
            st.write(movie_details)
        st.markdown("---")  # Adds a horizontal line for separation

    for i in range(5):
        display_movie_info(recommended_movies_name[i], recommended_movies_poster[i], recommended_movie_details[i])


# col1,col2,col3,col4,col5 = st.columns(5)

    # def display_movie_info(column, name, poster, details):
    #     with column:
    #         st.text(name)
    #         st.image(poster)
    #         with st.expander("Overview"):
    #             st.write(details)
    
    # display_movie_info(col1, recommended_movies_name[0], recommended_movies_poster[0], recommended_movie_details[0])
    # display_movie_info(col2, recommended_movies_name[1], recommended_movies_poster[1], recommended_movie_details[1])
    # display_movie_info(col3, recommended_movies_name[2], recommended_movies_poster[2], recommended_movie_details[2])
    # display_movie_info(col4, recommended_movies_name[3], recommended_movies_poster[3], recommended_movie_details[3])
    # display_movie_info(col5, recommended_movies_name[4], recommended_movies_poster[4], recommended_movie_details[4])




    # with col1:
    #     st.text(recommended_movies_name[0])
    #     st.image(recommended_movies_poster[0])
    #     st.text(recommended_movie_details[0],)
    
    # with col2:
    #     st.text(recommended_movies_name[1])
    #     st.image(recommended_movies_poster[1])
    #     st.text(recommended_movie_details[1])
    
    # with col3:
    #     st.text(recommended_movies_name[2])
    #     st.image(recommended_movies_poster[2])
    #     st.text(recommended_movie_details[2])
    
    # with col4:
    #     st.text(recommended_movies_name[3])
    #     st.image(recommended_movies_poster[3])
    #     st.text(recommended_movie_details[3])
    
    # with col5:
    #     st.text(recommended_movies_name[4])
    #     st.image(recommended_movies_poster[4])
    #     st.text(recommended_movie_details[4])

