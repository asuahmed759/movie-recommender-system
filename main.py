import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Download files from Google Drive if not present
if not os.path.exists('similarity_score.pkl'):
    gdown.download('https://drive.google.com/uc?id=1cjGTgdFpZTV_9ppfrIgmG0g82GHY502-', 'similarity_score.pkl', quiet=False)

if not os.path.exists('movies_dict.pkl'):
    gdown.download('https://drive.google.com/uc?id=1rkN0YZs0gVe6b6GepNtvAYk5R9ffbbaN', 'movies_dict.pkl', quiet=False)

if not os.path.exists('movies.pkl'):
    gdown.download('https://drive.google.com/uc?id=1mw00AA3jldi-P4EQpjGzwzbxm4FMwyGI', 'movies.pkl', quiet=False)



def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=f2eb095fc96b7a0ac72308206ddca773&language=en-US'
        .format(movie_id)
    )
    data = response.json()
    if 'poster_path' not in data or data['poster_path'] is None:
        return "https://via.placeholder.com/500x750?text=No+Poster"
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity_score[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(i[0]))
    return recommended_movies,recommended_movies_posters


movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity_score = pickle.load(open("similarity_score.pkl", "rb"))




st.title('Movie Recommendation System')

selected_movie_name = st.selectbox('Select Movie to recommend', movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
