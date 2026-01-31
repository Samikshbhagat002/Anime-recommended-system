import streamlit as st
import pickle
import requests
import os

# ---------------- LOAD FILES FROM JUPYTER ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies = pickle.load(open(os.path.join(BASE_DIR, 'movies.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb'))

# ---------------- POSTER USING JIKAN API ----------------
def fetch_poster(title):
    url = "https://api.jikan.moe/v4/anime"
    params = {"q": title, "limit": 1}

    response = requests.get(url, params=params).json()

    if 'data' in response and len(response['data']) > 0:
        return response['data'][0]['images']['jpg']['image_url']

    return None

# ---------------- RECOMMEND FUNCTION ----------------
def recommend_anime(name):
    name = name.lower()

    idx = movies[movies['title'].str.lower() == name].index[0]

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

    result = []
    for i in scores:
        title = movies.iloc[i[0]].title
        poster = fetch_poster(title)
        result.append((title, poster))

    return result

# ---------------- STREAMLIT UI ----------------
st.title("🎬 Anime Recommendation System")

selected = st.selectbox("Select Anime", movies['title'].values)

if st.button("Recommend"):
    data = recommend_anime(selected)

    cols = st.columns(5)

    for col, (name, poster) in zip(cols, data):
        with col:
            if poster:
                st.image(poster, use_container_width=True)
            st.caption(name)
