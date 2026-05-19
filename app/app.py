import streamlit as st
import pandas as pd
import joblib
import requests

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Zynema",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.stImage img {
    border-radius: 15px;
    transition: 0.3s;
}

.stImage img:hover {
    transform: scale(1.03);
}

.movie-title {
    text-align: center;
    font-size: 16px;
    font-weight: bold;
    margin-top: 10px;
    color: white;
}

.movie-rating {
    text-align: center;
    color: #FFD700;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ---------------- #

joblib.dump(
    similarity_df,
    r"C:\Users\M B Chinmay\Desktop\Zynema\models\movie_similarity_small.pkl"
)

# ---------------- TMDB API ---------------- #

API_KEY = st.secrets["API_KEY"]

# ---------------- FETCH MOVIE DETAILS ---------------- #

def fetch_movie_details(movie_name):

    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"

    response = requests.get(url)

    data = response.json()

    if data['results']:

        movie = data['results'][0]

        poster_path = movie.get('poster_path')

        rating = movie.get('vote_average')

        overview = movie.get('overview')

        # Poster handling
        if poster_path:

            poster = "https://image.tmdb.org/t/p/w500/" + poster_path

        else:

            poster = "https://dummyimage.com/300x450/1c1c1c/ffffff&text=No+Poster"

        return {
            "poster": poster,
            "rating": rating,
            "overview": overview
        }

    return {
        "poster": "https://dummyimage.com/300x450/1c1c1c/ffffff&text=No+Poster",
        "rating": "N/A",
        "overview": "No overview available."
    }

# ---------------- RECOMMENDATION FUNCTION ---------------- #

def recommend_movies(movie_name, num_recommendations=5):

    similar_scores = similarity_df[movie_name].sort_values(
        ascending=False
    )

    return similar_scores[1:num_recommendations + 1]

# ---------------- UI ---------------- #

st.title("🎬 Zynema")

st.subheader("AI-Powered Movie Recommendation System")

st.write("Discover movies similar to your favorites using AI 🚀")

# Movie list
movie_list = similarity_df.columns.tolist()

# Search dropdown
selected_movie = st.selectbox(
    "🎥 Select a movie",
    movie_list
)

# ---------------- BUTTON ---------------- #

if st.button("Recommend", key="recommend_btn"):

    recommendations = recommend_movies(selected_movie)

    st.write("## Recommended Movies")

    cols = st.columns(5)

    for idx, movie in enumerate(recommendations.index):

        details = fetch_movie_details(movie)

        with cols[idx]:

            # Poster
            st.image(
                details["poster"],
                use_container_width=True
            )

            # Movie title
            st.markdown(
                f"<div class='movie-title'>{movie}</div>",
                unsafe_allow_html=True
            )

            # Rating
            st.markdown(
                f"<div class='movie-rating'>⭐ {details['rating']}</div>",
                unsafe_allow_html=True
            )

            # Overview
            with st.expander("Overview"):
                st.write(details["overview"])