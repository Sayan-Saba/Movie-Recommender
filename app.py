import streamlit as st
import pickle
import pandas as pd

# Load the movie list and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

# Extract the list of movie titles
movies_list = movies['title'].values

# Streamlit header
st.header("Movie Recommender System")

# Dropdown for selecting a movie
select_value = st.selectbox('Select movie from the dropdown', movies_list)

def recommend(movie):
    # Find the index of the selected movie
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key = lambda vector: vector[1])
    
    
    recommend_movie = []
    for i in distance[1:6]:
        recommend_movie.append(movies.iloc[i[0]].title)
    return recommend_movie


    if st.button("Show Recommendations"):
        movie_name = recommend(select_value)
        col1,col2,col3,col4,col5 = st.columns(5)
        with col1:
            st.text(movie_name[0])
        with col2:
            st.text(movie_name[1])
        with col3:
            st.text(movie_name[2])
        with col4:
            st.text(movie_name[3])
        with col5:
            st.text(movie_name[4])

    
    
    # If similarity is a DataFrame, access the relevant row
    if isinstance(similarity, pd.DataFrame):
        similarity_scores = list(enumerate(similarity.iloc[index]))
    else:
        similarity_scores = list(enumerate(similarity[index]))
    
    # Sort movies based on similarity scores
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Get top 5 movie recommendations
    recommend_movies = [movies.iloc[i[0]].title for i in sorted_scores[1:6]]
    
    return recommend_movies

# Display recommendations when button is clicked
if st.button("Show Recommendations"):
    movie_name = recommend(select_value)
    
    # Display recommendations in columns
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if i < len(movie_name):
            col.text(movie_name[i])
