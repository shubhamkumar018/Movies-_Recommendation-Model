import streamlit as st
import joblib
import requests
from functools import lru_cache

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================
movies = joblib.load("data.pkl")
similarity = joblib.load("similarity.pkl")

# ==========================================
# TMDB API KEY
# ==========================================
API_KEY = "YOUR_TMDB_API_KEY"

# ==========================================
# DEFAULT POSTER
# ==========================================
DEFAULT_POSTER = (
    "https://placehold.co/500x750/"
    "222222/FFFFFF?text=No+Poster+Available"
)

# ==========================================
# FETCH MOVIE POSTER
# ==========================================
@lru_cache(maxsize=500)
def fetch_poster(movie_id):

    try:

        url = (
            f"https://api.themoviedb.org/3/movie/"
            f"{movie_id}?api_key={API_KEY}&language=en-US"
        )

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=5
        )

        # API request failed
        if response.status_code != 200:
            return DEFAULT_POSTER

        data = response.json()

        # Get poster path
        poster_path = data.get("poster_path")

        # Poster not available
        if not poster_path:
            return DEFAULT_POSTER

        # TMDB poster URL
        poster_url = (
            "https://image.tmdb.org/t/p/w500"
            + poster_path
        )

        return poster_url

    except Exception:
        return DEFAULT_POSTER


# ==========================================
# RECOMMEND MOVIES
# ==========================================
def recommend(movie):

    if movie not in movies["title"].values:
        return [], []

    # Get selected movie index
    index = movies[movies["title"] == movie].index[0]

    # Get similarity scores
    distances = similarity[index]

    # Sort movies according to similarity
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:

        movie_index = i[0]

        movie_id = movies.iloc[movie_index]["id"]
        movie_name = movies.iloc[movie_index]["title"]

        recommended_movies.append(movie_name)

        poster = fetch_poster(movie_id)

        recommended_posters.append(poster)

    return recommended_movies, recommended_posters


# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .movie-title {
        text-align: center;
        font-size: 17px;
        font-weight: bold;
        margin-top: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# TITLE
# ==========================================
st.markdown(
    '<div class="main-title">🎬 Movie Recommender System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Select a movie and discover similar movies 🍿'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# MOVIE SELECTION
# ==========================================
selected_movie = st.selectbox(
    "🎥 Select a movie",
    movies["title"].values
)


# ==========================================
# RECOMMEND BUTTON
# ==========================================
if st.button(
    "🎬 Recommend Movies",
    use_container_width=True
):

    names, posters = recommend(selected_movie)

    if names:

        st.subheader(
            f"Movies similar to **{selected_movie}**"
        )

        cols = st.columns(5)

        for i in range(5):

            with cols[i]:

                # Movie poster
                st.image(
                    posters[i],
                    use_container_width=True
                )

                # Movie name
                st.markdown(
                    f'<div class="movie-title">'
                    f'{names[i]}'
                    f'</div>',
                    unsafe_allow_html=True
                )

    else:

        st.error("❌ Movie not found!")