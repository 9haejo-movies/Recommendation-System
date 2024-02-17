import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

def get_movie_details(movie_id, api_key='c24a5b64e7186cfcf4a4b840c3138e12'):
    movie = Movie()
    tmdb = TMDb()
    tmdb.api_key = api_key
    details = movie.details(movie_id)
    return details

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
    ids = []
    
    for movie_index in recommended_movies.index:
        movie_id = movies['id'].iloc[movie_index]
        details = get_movie_details(movie_id, 'c24a5b64e7186cfcf4a4b840c3138e12')
        image_path = details.get('poster_path')
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else: 
            image_path = 'no_image.jpg'
        images.append(image_path)
        titles.append(details.get('title'))
        genres.append([genre['name'] for genre in details.get('genres', [])])  # Extract all genres
        ids.append(movie_id)
    
    return images, titles, genres, ids

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
    ids = []
    
    for movie_index in recommended_movies.index:
        movie_id = movies['id'].iloc[movie_index]
        details = get_movie_details(movie_id, 'c24a5b64e7186cfcf4a4b840c3138e12')
        image_path = details.get('poster_path')
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else: 
            image_path = 'no_image.jpg'
        images.append(image_path)
        titles.append(details.get('title'))
        genres.append([genre['name'] for genre in details.get('genres', [])])  # Extract all genres
        ids.append(movie_id)
    
    return images, titles, genres, ids

# Load movies and cosine similarity matrix
movies = pickle.load(open('movies_final.pickle','rb'))
cosine_sim = pickle.load(open('cosine_sim_final.pickle','rb'))

st.set_page_config(layout='wide')
st.header('🎥 Movie Recommendation System 🎥')

title = st.selectbox('Choose a movie you like', movies['title'].values)
sorting_method = st.radio("Select sorting method:", ('Popular', 'Latest'))

if st.button('Recommend'):
    with st.spinner('Wait for it...'):
        if sorting_method == 'Popular':
            images, titles, genres, ids = get_recommendations_pop(title)
        else:
            images, titles, genres, ids = get_recommendations_year(title)
        
        idx = 0
        for i in range(0, 2):
            cols = st.columns(5)
            for j in range(0, 5):
                # Display the image with column width
                cols[j].image(images[idx], use_column_width=True, output_format='JPEG')
                
                # Display title and genres next to the image
                cols[j].write("**✔️[Title]** " + titles[idx])
                cols[j].write("**✔️[Genres]** " + ", ".join(genres[idx]))  # Display all genres
                
                idx += 1
