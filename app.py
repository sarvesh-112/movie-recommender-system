import streamlit as st
import pandas as pd
import pickle
import requests
import os
import gdown

# Set Streamlit page config
st.set_page_config(page_title="Movie Recommender - Sarvesh", layout="wide")

# Custom CSS Styling
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #4facfe, #00f2fe);
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 3rem;
        color: #fff;
        margin-bottom: 0.2em;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #e5e7eb;
        margin-bottom: 2em;
    }
    .recommender-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 2em;
        border-radius: 20px;
        backdrop-filter: blur(8px);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    .stButton>button {
        background-color: #10b981;
        color: white;
        font-size: 1rem;
        border-radius: 8px;
        padding: 0.5em 1.5em;
    }
    .stSelectbox>div {
        background-color: #f9fafb;
        border-radius: 8px;
    }
    .movie-card:hover {
        transform: scale(1.05);
        transition: all 0.2s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown('<h1 class="main-title">🎬 Movie Recommender System</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">By Sarvesh — Project #1 🚀</p>', unsafe_allow_html=True)

# Download similarity.pkl from Google Drive if needed
if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/uc?id=1YNc48cU2cEKvAt-wOspwarlk5oIcmyOw", "similarity.pkl", quiet=False)

# Load pickle files
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Fetch poster from TMDB
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=04dd5073afb05c257b84f37903b1b29e'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Movie recommender function
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

# Main UI Block
with st.container():
    st.markdown('<div class="recommender-box">', unsafe_allow_html=True)

    selected_movie_name = st.selectbox('🎥 Select a movie to get recommendations:', movies['title'].values)

    if st.button('💡 Recommend'):
        names, posters = recommend(selected_movie_name)
        cols = st.columns(5)
        for idx in range(5):
            with cols[idx]:
                st.markdown(f"<div class='movie-card'>", unsafe_allow_html=True)
                st.image(posters[idx])
                st.markdown(f"**{names[idx]}**")
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
