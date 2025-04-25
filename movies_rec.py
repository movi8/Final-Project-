
import streamlit as st
import pandas as pd
import requests
import pickle

with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_path

def fetch_movie_details(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    return response.json()

st.title("Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    st.write("Top 10 recommended movies:")
def get_streaming_platforms(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8' 
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    
    platforms = set()
    if 'results' in data:
        for provider in data['results'].values():
            if 'flatrate' in provider:
                for service in provider['flatrate']:
                    provider_name = service['provider_name']
                    if provider_name in PRINCIPAL_PLATFORMS:
                        platforms.add(provider_name)
    return list(platforms)[:5]  # Return only the first 5 platforms
PRINCIPAL_PLATFORMS = [
    "Netflix",
    "Amazon Prime Video",
    "Hulu",
    "Disney+",
    "HBO Max",
    "Apple TV+",
    "Paramount+",
    "Peacock"
]

recommendations = get_recommendations(selected_movie)

for i in range(0, 10, 5):  
    cols = st.columns(5)  
    for col, j in zip(cols, range(i, i+5)):
        if j < len(recommendations):
            movie_title = recommendations.iloc[j]['title']
            movie_id = recommendations.iloc[j]['movie_id']
            poster_url = fetch_poster(movie_id)
            
            with col:
                st.image(poster_url, width=130)
                st.write(movie_title)
                
                # Add a button to show streaming platforms
                if st.button(f'Apps for {movie_title}'):
                    platforms = get_streaming_platforms(movie_id)  # Fetch streaming platforms
                    if platforms:
                        st.write("Available on:")
                        st.write(", ".join(platforms))  # Display unique platforms
                    else:
                        st.write("No streaming information available.")
                
                # Add a new button to show movie details
                if st.button(f'Show Details for {movie_title}'):
                    details = fetch_movie_details(movie_id)  # Fetch movie details
                    st.write("**Overview:**", details.get('overview', 'No overview available.'))
                    st.write("**Release Date:**", details.get('release_date', 'N/A'))
                    st.write("**Rating:**", details.get('vote_average', 'N/A'))
                    st.write("**Genres:**", ", ".join([genre['name'] for genre in details.get('genres', [])]))
