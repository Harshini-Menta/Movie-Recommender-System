import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path and poster_path.strip() != "":
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"

    except Exception:
        return "https://via.placeholder.com/300x450?text=No+Poster"


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

st.set_page_config(page_title="Movie Recommender System", layout="wide")
st.header("🎬 Movie Recommender System")

movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("movies_similarity.pkl", "rb"))

movie_list = movies["title"].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"**{names[0]}**")
        st.image(posters[0], width=230)
    with col2:
        st.markdown(f"**{names[1]}**")
        st.image(posters[1], width=230)
    with col3:
        st.markdown(f"**{names[2]}**")
        st.image(posters[2], width=230)
    with col4:
        st.markdown(f"**{names[3]}**")
        st.image(posters[3], width=230)
    with col5:
        st.markdown(f"**{names[4]}**")
        st.image(posters[4], width=230)
