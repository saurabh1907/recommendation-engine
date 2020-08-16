"""
This module comprises of all the functions that are used in choice_based_recommendation.py file
"""

import pickle
import pandas as pd


def reading_movie_title_csv(path):
    """
    It reads the csv file having list of all the movies either watched or recommended
    Returns: Dataframe containing movie details: movie_id, year of release, title, display
    """
    movies_df = pd.read_csv(path, sep=",")
    movies_df.sort_values(by='Final_title', ascending=True, inplace=True)
    return movies_df


def get_options(movies_df):
    """
    List all the unique elements of a column in dropdown
    Args:
        movies_df: Movies dataframe containing the column whose rows are used as dropdown options
    Returns: list of columns
    """
    dict_list = []
    for i in movies_df:
        dict_list.append({'label': i, 'value': i})
    return dict_list


def get_movie_id(movies_df, selected_movie):
    """
    This function returns the movie details associated with a particular movie-id
    Args:
        movies_df: pandas dataframe containing details of all movies
        selected_movie: movie id selected by users based on which he/she wants recommendations
    Returns: Movie id to generate recommendation
    """
    if isinstance(selected_movie, list):
        movie_details = movies_df[movies_df['Display'] == selected_movie[0]]
    else:
        movie_details = movies_df[movies_df['Display'] == selected_movie]
    movie_id = movie_details['Sno'].iloc[0]
    return movie_id


def recommendation_for_movies(path):
    """
    It reads the dictionary containing the list of recommended movie ids for
    each of the movies present in our dataset
    Args:
        path: path where file is stored
    Returns: Dictionary containing the list of movie ids recommended for all movie ids
    """
    dict_rec = {}
    with open(path, 'rb') as filename:
        dict_rec = pickle.load(filename)
    return dict_rec


def get_top10_movies(movies_df, recommended_movie_ids, recommended_movie_scores):
    """
    This function generates details of the top 10 movies recommended to the user
    Args:
        movies_df: pandas dataframe containing details of all movies
        recommended_movie_ids: list of movie ids generated from recommendation_for_movies()
        recommended_movie_scores: list of scores for movie ids from recommendation_for_movies()
    Returns: pandas dataframe containing the movie details
    """
    top10_movies = movies_df[movies_df.Sno.isin(recommended_movie_ids)]
    top10_movies['Match%'] = recommended_movie_scores.copy()
    top10_movies['Match%'] = round(round(top10_movies['Match%'], 2) * 100)
    top10_movies = top10_movies.drop(['Sno', 'Final_title'], axis=1)
    top10_movies.columns = ['Year of Release', 'Movie Title', 'Match%']
    return top10_movies


def userchoice_based_movie_recommendation(selected_movie, movies_df, dict_rec):
    """
    This function recommends movies based a user selected movie id
    Args:
         selected_movie: movie-id input by user
         movies_df: dataframe containing all movies'
         dict_rec: dictionary containing list of recommended movies for each movie
    Returns: Dataframe containing top 10 recommended movies
    """
    movie_id = get_movie_id(movies_df, selected_movie)
    recommended_movie_ids = dict_rec[movie_id][0][:10]
    recommended_movie_scores = dict_rec[movie_id][1][:10]
    top10_movies = get_top10_movies(movies_df, recommended_movie_ids, recommended_movie_scores)
    return top10_movies


