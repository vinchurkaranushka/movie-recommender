import pickle
import streamlit as st
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

API_KEY = "f18f8550e656dca54599c250e3d9eae8"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    if data.get("poster_path"):
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    return None

@st.cache_data
def load_and_compute():
    movies = pickle.load(open("artifacts/movie_list.pkl", "rb"))

    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(movies["tags"]).toarray()
    similarity = cosine_similarity(vectors)

    return movies, similarity

movies, similarity = load_and_compute()

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

selected_movie = st.selectbox("Select a movie", movies['title'].values)

if st.button("Show recommendation"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            if posters[i]:
                st.image(posters[i])
