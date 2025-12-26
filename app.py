import pickle
import streamlit as st
import requests

API_KEY = "f18f8550e656dca54599c250e3d9eae8"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    names = []
    posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters

st.header("Movies Recommendation System")

movies = pickle.load(open("artifacts/movie_list.pkl", "rb"))
similarity = pickle.load(open("artifacts/similarity.pkl", "rb"))

selected_movie = st.selectbox("Select a movie", movies['title'].values)

if st.button("Show recommendation"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
