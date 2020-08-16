"""
This module executes the preprocessing of the datasets obtained from the
IMDb website and the Netflix Prize Dataset from Kaggle. Please look at
the instructions on how to obtain the Netflix dataset before executing
this script.
"""
import shutil
import os

import pandas as pd

import helper_functions as hf

PROCESSED_DIR = 'pre_processed'
TXT_EXT = '.txt'
CSV_EXT = '.csv'
PKL_EXT = '.pkl'

# NETFLIX Constants
NF_KAGGLE_USER = 'netflix-inc'
NF_DIRECTORY = 'netflix-prize-data'
NF_FILE_NAME = 'combined_data_'
FILE_I = list(range(1, 5))
LIST_NF_FILES = [NF_FILE_NAME+str(i)+TXT_EXT for i in FILE_I]
DF_NF_COLS = ['movie_id', 'user_id', 'rating', 'rating_date']
DICT_NAME = 'dict_recommendations'
TITLE_FILE_NAME = 'movie_titles'
TITLES_PATH = os.path.join(NF_DIRECTORY, TITLE_FILE_NAME+CSV_EXT)

# IMDb Constants
IMDB_TITLES_URL = 'https://datasets.imdbws.com/title.basics.tsv.gz'
IMDB_RATINGS_URL = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
IMDB_FILE_NAME = 'imdb_df'
GENRES_FILE_NAME = 'set_genres'


def process_netflix():
    """
    Processing Netflix dataset: download and parse data, create final
    files and storing them
    """
    # Download the files, unzip them and get the data in a dataframe.
    hf.download_netflix_data(NF_KAGGLE_USER, NF_DIRECTORY)
    list_nf_data = []

    for file in LIST_NF_FILES:
        list_nf_data += hf.parse_data(os.path.join(NF_DIRECTORY, file))
        df_netflix = pd.DataFrame(list_nf_data, columns=DF_NF_COLS)

    # Get the movie recommendation dictionary and store in data folder.
    dict_recommendations = hf.get_recommended_movies(df_netflix)
    hf.save_file(dict_recommendations, PROCESSED_DIR, DICT_NAME, PKL_EXT)

    # Cleaning the movie_titles file
    df_titles = hf.format_movie_titles(TITLES_PATH)
    hf.save_file(df_titles, PROCESSED_DIR, TITLE_FILE_NAME, CSV_EXT)

    #Deleting original Netflix dataset directory
    shutil.rmtree(NF_DIRECTORY)


def process_imdb():
    """
    Processing IMDb dataset: download, merge and clean data, store
    final dataframe and unique genres.
    """
    # Download the data and store the cleaned and merged datasets.
    df_imdb_titles = hf.download_gz_file(IMDB_TITLES_URL)
    df_imdb_ratings = hf.download_gz_file(IMDB_RATINGS_URL)
    df_imdb = hf.clean_imdb_data(df_imdb_titles, df_imdb_ratings)
    hf.save_file(df_imdb, PROCESSED_DIR, IMDB_FILE_NAME, CSV_EXT)

    # Get unique genres and storing them in data folder.
    genres = hf.get_unique_genres(df_imdb)
    hf.save_file(genres, PROCESSED_DIR, GENRES_FILE_NAME, PKL_EXT)


process_netflix()
process_imdb()
