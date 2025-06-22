import streamlit as st
import pandas as pd
import pickle
import requests
import os

# Automatically download 'similarity.pkl' if it's not present
if not os.path.exists("similarity.pkl"):
    file_id = "1YNc48cU2cEKvAt-wOspwarlk5oIcmyOw"
    url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(url)
    with open("similarity.pkl", "wb") as f:
        f.write(response.content)

# Load precomputed data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDb poster fetch
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=04dd5073afb05c257b84f37903b1b29e'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Streamlit UI
st.title('Movie Recommender System')
selected_movie_name = st.selectbox('What movie do you like?', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
