import streamlit as st
import pandas as pd
import pickle
import requests
import os
import gdown

# Download similarity.pkl from Google Drive if not already present
if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/uc?id=1YNc48cU2cEKvAt-wOspwarlk5oIcmyOw", "similarity.pkl", quiet=False)

# Load pickle files
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Custom styling - NEON aesthetic
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');
        html, body, [class*="css"] {
            font-family: 'Orbitron', sans-serif;
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #ff00cc);
            background-size: 400% 400%;
            animation: gradient 20s ease infinite;
            color: #00ffe7;
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .stApp {
            padding: 2rem;
        }
        .stSelectbox > div {
            font-size: 18px;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #ff00cc;
            color: #ffffff;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            border: none;
        }
        .css-1v0mbdj.ef3psqc12 {
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 0 15px #00ffe7;
        }
    </style>
""", unsafe_allow_html=True)

# Project title
st.markdown("<h1 style='text-align: center; color: #00ffe7;'>🎥 Sarvesh — Project #1: Movie Recommender</h1>", unsafe_allow_html=True)

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=04dd5073afb05c257b84f37903b1b29e'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Movie selector
selected_movie_name = st.selectbox('🎬 What movie do you want recommendations for?', movies['title'].values)

if st.button('🔮 Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx in range(5):
        with cols[idx]:
            st.image(posters[idx])
            st.markdown(f"<h4 style='text-align: center; color: #ffffff;'>{names[idx]}</h4>", unsafe_allow_html=True)
