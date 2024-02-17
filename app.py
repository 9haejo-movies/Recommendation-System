import pickle
import streamlit as st
import pandas as pd
import numpy as np
from tmdbv3api import Movie, TMDb

def get_recommendations_pop(title):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    recommended_movies = movies.iloc[movie_indices].nlargest(10, 'popularity')
    recommended_movies = recommended_movies.sort_values(by='popularity', ascending=False)
    
    images = []
    titles = []
    genres = []
    
    for movie_index in recommended_movies.index:
        movie_id = movies['id'].iloc[movie_index]
        details = movie.details(movie_id)
        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else: 
            image_path = 'no_image.jpg'
        images.append(image_path)
        titles.append(details.title)
        genres.append(details.genres)
    
    return images, titles, genres

def get_recommendations_year(title):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    recommended_movies = movies.iloc[movie_indices].nlargest(10, 'release_date')
    
    images = []
    titles = []
    genres = []
    
    for movie_index in recommended_movies.index:
        movie_id = movies['id'].iloc[movie_index]
        details = movie.details(movie_id)
        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else: 
            image_path = 'no_image.jpg'
        images.append(image_path)
        titles.append(details.title)
        genres.append(details.genres)
    
    return images, titles, genres

movie = Movie()
tmdb = TMDb()
tmdb.api_key = ''
#tmdb.language = 'ko-KR'

# cosine similarity load
movies = pickle.load(open('movies_final.pickle','rb'))
cosine_sim = pickle.load(open('cosine_sim_final.pickle','rb'))

st.set_page_config(layout='wide')
st.header('🎥Movie Recommendation System🎥')

movie_list = movies['title'].values

title = st.selectbox('Choose a movie you like', movie_list)

sorting_method = st.radio("Select sorting method:", ('Popular', 'Latest'))

if st.button('Recommend'):
    with st.spinner('Wait for it...'):
        if sorting_method == 'Popularity':
            images, titles, genres = get_recommendations_pop(title)
        else:
            images, titles, genres = get_recommendations_year(title)

        tab_titles = ['추천 영화 10개 목록', '영화 정보']
        tabs = st.tabs(tab_titles)

        with tabs[0]:
            idx = 0
            for i in range(0,2):
                cols = st.columns(5)
                for j in range(0,5):
                    cols[j].image(images[idx], width=100, use_column_width=True, caption=titles[idx])
                    checkbox_key = f"checkbox_{idx}"
                    if cols[j].write("",key=checkbox_key):
                        cols[j].image(images[idx], width=300, use_column_width=True, caption=titles[idx])
                    idx += 1
        
        with tabs[1]:
            idx = 0
            for i in range(0,2):
                cols = st.columns(5)
                for j in range(0,5):
                    cols[j].image(images[idx], width=150)
                    cols[j].write(f'✔️제목 : {titles[idx]}')
                    genre_names = ', '.join([genre['name'] for genre in genres[idx]])
                    cols[j].write(f'✔️장르 : {genre_names}')
                    cols[j].write(f'✔️개봉연도 : {movies["release_date"][idx]}')
                    idx += 1         


