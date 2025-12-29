import pickle
import streamlit as st
import requests

#CONFIG
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
BASE_POSTER_URL = "https://image.tmdb.org/t/p/w500"
FALLBACK_POSTER = "https://via.placeholder.com/500x750?text=No+Image"

st.set_page_config(page_title="Movie Recommender", layout="wide")

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()

        poster_path = data.get("poster_path")
        if poster_path:
            return BASE_POSTER_URL + poster_path
        else:
            return FALLBACK_POSTER

    except Exception:
        return FALLBACK_POSTER


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []
    recommended_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title

        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# LOAD DATA 
movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("movies_similarity.pkl", "rb"))

# UI 
st.title("🎬 Movie Recommender System")
st.markdown("Get movie recommendations based on your favorite movie 🍿")

movie_list = movies["title"].values
selected_movie = st.selectbox(
    "🔍 Type or select a movie",
    movie_list
)

if st.button("Show Recommendations"):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_column_width=True)
            st.markdown(f"**{names[i]}**")
