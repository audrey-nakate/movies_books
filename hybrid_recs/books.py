import numpy as np
import pandas as pd
import streamlit as st
from tensorflow.keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity

model = load_model('recommender_model.h5')
books_name = pd.read_pickle(open('D:\OneDrive - FSD Uganda\Desktop\final_yr_deploys\book_recommender\artifacts\books_name.pkl', 'rb'))
final_rating = pd.read_pickle(open('D:\OneDrive - FSD Uganda\Desktop\final_yr_deploys\book_recommender\artifacts\final_rating.pkl', 'rb'))
book_pivot = pd.read_pickle(open('D:\OneDrive - FSD Uganda\Desktop\final_yr_deploys\book_recommender\artifacts\book_pivot.pkl', 'rb'))

def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['img_url']
        poster_url.append(url)

    return poster_url  

def preprocess_input(book_name):
    # Preprocess the input book name to get the required input for the model
    book_id = np.where(book_pivot.index == book_name)[0][0]
    return book_pivot.iloc[book_id, :].values.reshape(1, -1)


def postprocess_output(model_output):
    # Postprocess the model output to get book IDs for recommended books
    distances = cosine_similarity(model_output, book_pivot.values)
    suggestions = np.argsort(-distances[0])[1:6]  # Get 5 similar recommendations
    recommended_book_ids = [book_pivot.index[i] for i in suggestions]
    return recommended_book_ids

def recommend_book(book_name):
    books_list = []

    # Preprocess the input
    model_input = preprocess_input(book_name)

    # Get recommendations 
    model_output = model.predict(model_input)

    # Postprocess output
    recommended_book_ids = postprocess_output(model_output)

    # Fetch poster URLs for the recommended books
    poster_urls = fetch_poster(recommended_book_ids)

    # Get the book names for the recommended books
    for book_id in recommended_book_ids:
        book_name = books[books['book_id'] == book_id]['book_name'].values[0]
        books_list.append(book_name)

    return books_list, poster_urls



# streamlit integration 
selected_books = st.selectbox(
    "Type or select a book from the dropdown ",
    books_name
)

if st.button('Show Recommendation'):
    recommendation_books,poster_url = recommend_book(selected_books)

    def display_book_info(book_name, book_poster):
        st.image(book_poster, width=250)
        st.text(book_name)
          # Adds a horizontal line for separation

    for i in range(5):
        display_book_info(recommendation_books[i], poster_url[i])
