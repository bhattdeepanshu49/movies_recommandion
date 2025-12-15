import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"  # Ideally, store this securely
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    
    # Handle missing poster paths
    if data.get("poster_path"):
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies
def recommend(selected_movie):
    index = movies[movies['title'] == selected_movie].index[0]
    distances = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    movie_posters = []
    
    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]]['title'])
        movie_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, movie_posters

# Load movie data and similarity scores
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity_scores = pickle.load(open('similarity.pkl', 'rb'))

# Extract movie titles
movies_list = movies['title'].values

# Streamlit UI
st.title('Movie Recommendation System 🎬')
st.write('This is a simple movie recommendation system that uses a collaborative filtering approach to suggest movies based on similarity scores.')

# Movie selection dropdown
selected_movie = st.selectbox('Select a movie:', movies_list)

# Recommendation button
if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    
    # Display movies in a row
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
